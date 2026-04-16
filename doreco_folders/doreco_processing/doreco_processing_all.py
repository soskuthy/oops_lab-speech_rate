from polyglotdb import CorpusContext
import polyglotdb.io as pgio
from polyglotdb.query.base.func import Count

from panphon import FeatureTable
from panphon.permissive import PermissiveFeatureTable

from doreco_parsing import inspect_doreco
import doreco_helper


SILENT_PAUSE_REGEX = '^<p:>$'
NONALIGNED_REGEX = '^<<.*>.*>$'
NONALIGNED_CODED_REGEX = '^<<(bc|id|fm|fp|fs|on|pr|sg|ui|wip)>.*>$'
NONALIGNED_OTHER_REGEX = '^<<(?!(bc|id|fm|fp|fs|on|pr|sg|ui|wip)).*>.*>$'
NONALIGNED_REGEX_DICT = {'backchannel':'^<<bc>.*>$',
                         'ideophone':'^<<id>.*>$',
                         'foreign_material':'^<<fm>.*>$',
                         'filled_pause':'^<<fp>.*>$',
                         'false_start':'^<<fs>.*>$',
                         'onomatopoeic':'^<<on>.*>$',
                         'prolongation':'^<<pr>.*>$',
                         'singing':'^<<sg>.*>$',
                         'unidentifiable':'^<<ui>.*>$',
                         'word-internal_pause':'^<<wip>.*>$'}
NONSPEECH_REGEX = '^<.*'
SPEECH_REGEX = '(?!'+NONSPEECH_REGEX+').*'

CORPUS_CODES = ['apah1238',
                'arap1274',
                'bain1259',
                'beja1238',
                'bora1263',
                'dolg1241',
                'even1259',
                'guri1247', # missing all audio files
                'jeju1234',
                'kama1351',
                'lowe1385',
                'movi1243', # missing some audio files
                'ngal1292',
                'nngg1234',
                'orko1234',
                'resi1247',
                'ruul1235',
                'sadu1234',
                'sanz1248', # missing some phonological feature specifications (e.g. vl epiglottal plosive <\)
                'sout3282',
                'svan1243',
                'trin1278', # one discourse (T20) is missing a phone tier for one speaker (FCT)
                'urum1249', # check liquid 'r\\_r'
                'vera1241', # has bad non-speech phone '<<fs>'
                'yong1270'
                ]

SHORT_CORPUS_CODES = ['trin1278']

for corpus_code in CORPUS_CODES:
#for corpus_code in SHORT_CORPUS_CODES:
    corpus_root = '../doreco_corpora/doreco_'+corpus_code+'_core_v'
    if corpus_code in ['kama1351','urum1249']:
        corpus_root += '2.0/'
    elif corpus_code == 'orko1234':
        corpus_root += '1-1.3/'
    else:
        corpus_root += '1.3/'
    corpus_name = 'doreco_'+corpus_code
    file_name_prefix = corpus_name+"_"
    metadata_csv_path = corpus_root + corpus_name + '_metadata.csv'
    discourse_csv_path = corpus_root + corpus_name + '_metadata_discourse.csv'
    speakers_csv_path = corpus_root + corpus_name + '_metadata_speakers.csv'

    # Initializing
    doreco_helper.subset_discourse_metadata(metadata_csv_path,discourse_csv_path)
    doreco_helper.subset_speaker_metadata(metadata_csv_path,speakers_csv_path)

    parser = inspect_doreco(corpus_root, discourse_csv_path, file_name_prefix=file_name_prefix)
    parser.call_back = print

    with CorpusContext(corpus_name) as c:
        c.reset()

    with CorpusContext(corpus_name) as c:
        c.load(parser, corpus_root)

    with CorpusContext(corpus_name) as c:
        print(corpus_code+": Renaming Discourses...")
        q = c.query_discourses()
        for filename in c.discourses:
            filt_q = q.filter(c.discourse.name == filename)
            filt_q.set_properties(name = filename.replace(file_name_prefix,""))

    # Enriching
    with CorpusContext(corpus_name) as c:
        print(corpus_code+": Enriching Speaker Metadata...")
        c.enrich_speakers_from_csv(speakers_csv_path)

    with CorpusContext(corpus_name) as c:
        print(corpus_code+": Enriching Discourse Metadata...")
        c.enrich_discourses_from_csv(discourse_csv_path)

    with CorpusContext(corpus_name) as c:
        print(corpus_code+": Enriching Nonspeech Segments...")

        q = c.query_lexicon(c.lexicon_phone)
        q = q.filter(c.lexicon_phone.label.regex(NONSPEECH_REGEX))
        q.create_subset('nonspeech')
        q.set_properties(seg_type='nonspeech')

        q = c.query_lexicon(c.lexicon_phone)
        q = q.filter(c.lexicon_phone.label.regex(SILENT_PAUSE_REGEX))
        #q.create_subset('silent_pause')
        q.set_properties(seg_type_nonsp='silent_pause')

        q = c.query_lexicon(c.lexicon_phone)
        q = q.filter(c.lexicon_phone.label.regex(NONALIGNED_CODED_REGEX))
        #q.create_subset('nonaligned')
        q.set_properties(seg_type_nonsp='nonaligned')

        q = c.query_lexicon(c.lexicon_phone)
        q = q.filter(c.lexicon_phone.label.regex(NONALIGNED_OTHER_REGEX))
        #q.create_subset('nonspeech_other')
        q.set_properties(seg_type_nonsp='other')

        for nonal_name,nonal_regex in NONALIGNED_REGEX_DICT.items():
            q = c.query_lexicon(c.lexicon_phone)
            q = q.filter(c.lexicon_phone.label.regex(nonal_regex))
            #q.create_subset(nonal_name)
            q.set_properties(seg_type_nonsp_nonal=nonal_name)

    with CorpusContext(corpus_name) as c:
        print(corpus_code+": Enriching Phonological Features...")
        c.reset_features('feature')
        c.reset_class('complex_segment')
        ft = FeatureTable()
        ft_2 = PermissiveFeatureTable()
        q = c.query_lexicon(c.lexicon_phone)
        q = q.filter(c.lexicon_phone.label.regex(SPEECH_REGEX))
        q = q.columns(c.lexicon_phone.label.column_name('phone'))
        phone_labels = [r['phone'] for r in q.all()]
        #print(phone_labels)
        for phone_label in phone_labels:
            q_filt = c.query_lexicon(c.lexicon_phone)
            q_filt = q_filt.filter(c.lexicon_phone.label == phone_label)
            phon_features_dict, complex_type = doreco_helper.get_phon_features(
                                                        phone_label,
                                                        ft,
                                                        permissive_feature_table=ft_2,
                                                        prefix='phon_feat_')
            if complex_type == 'unknown':
                print("UNKNOWN COMPLEX SEGMENT \'"+phone_label+"\'. ENCODING AS NON-SPEECH.")
                q_filt.create_subset('nonspeech')
                q_filt.set_properties(seg_type='nonspeech')
                q_filt.set_properties(seg_type_nonsp='other')
            elif complex_type:
                #q_filt.create_subset('complex_seg')
                #q_filt.create_subset('complex_seg_'+complex_type)
                q_filt.set_properties(seg_type_complex=complex_type)
            else:
                q_filt.set_properties(seg_type_complex='simple')
            q_filt.set_properties(**phon_features_dict)
            ipa_label = doreco_helper.to_ipa_normed(phone_label,ft)
            q_filt.set_properties(ipa=ipa_label)


        
    with CorpusContext(corpus_name) as c:
    #     print(corpus_code+": Getting Segment Classes...")

        # All Speech Phones
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset != 'nonspeech') # only include speech segments
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        speech_phones_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        #print(corpus_code+": all phones",speech_phones_list)

        # Syllabic
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset != 'nonspeech') # only include speech segments
        q = q.filter(c.phone.phon_feat_syl == 1) # syllabic phones have the feature +syl
        q.create_subset('syllabic')
        q.set_properties(seg_type='syllabic')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        syllabic_phones_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        #print(corpus_code+": syllabics",syllabic_phones_list)

        # Consonant (Non-Syllabic)
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset != 'nonspeech') # only include speech segments
        q = q.filter(c.phone.phon_feat_syl == -1) # nonsyllabic phones have the feature -syl
        q.create_subset('consonant')
        q.set_properties(seg_type='consonant')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        consonants_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        #print(corpus_code+": consonants",consonants_list)

        # Check that Syllabic and Consonant partition all speech phones
        phone_classes = {"syllabic" : syllabic_phones_list,
                         "consonant" : consonants_list}
        phone_super_list = speech_phones_list
        phone_super_name = "all"
        all_found = []
        for phone_class_name,phone_class_list in phone_classes.items():
            for phone_label in phone_class_list:
                all_found.append(phone_label)
                for phone_class_name_2,phone_class_list_2 in phone_classes.items():
                    if phone_class_name != phone_class_name_2 and phone_label in phone_class_list_2:
                        print("OOPS!",phone_label,"in both",phone_class_name,"and",phone_class_name_2)
        for phone_label in phone_super_list:
            if phone_label not in all_found:
                print("OOPS!",phone_label,"in",phone_super_name,"but not in any subset")
        for phone_label in all_found:
            if phone_label not in phone_super_list:
                print("OOPS!",phone_label,"in a subset but not in",phone_super_name)


        # Vowel < Syllabic
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'syllabic') # only include syllabic phones
        q = q.filter(c.phone.phon_feat_tense != 0) # vowels are specified for tenseness (excludes syllabic rhotics)
        q.create_subset('vowel')
        q.set_properties(seg_type_syll='vowel')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        vowels_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        #print(corpus_code+": vowels",vowels_list)

        # Syllabic Consonant < Syllabic
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'syllabic') # only include syllabic phones
        q = q.filter(c.phone.phon_feat_tense == 0) # syllabic consonants are unspecified for tenseness (includes syllabic rhotics)
        q.create_subset('syll_c')
        q.set_properties(seg_type_syll='syll_c')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        syll_c_phones_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        print(corpus_code+": syllabic consonants",syll_c_phones_list)

        # Check that Vowel and Syllabic Consonant partition Syllabic
        phone_classes = {"vowel" : vowels_list,
                         "syll_c" : syll_c_phones_list}
        phone_super_list = syllabic_phones_list
        phone_super_name = "syllabic"
        all_found = []
        for phone_class_name,phone_class_list in phone_classes.items():
            for phone_label in phone_class_list:
                all_found.append(phone_label)
                for phone_class_name_2,phone_class_list_2 in phone_classes.items():
                    if phone_class_name != phone_class_name_2 and phone_label in phone_class_list_2:
                        print("OOPS!",phone_label,"in both",phone_class_name,"and",phone_class_name_2)
        for phone_label in phone_super_list:
            if phone_label not in all_found:
                print("OOPS!",phone_label,"in",phone_super_name,"but not in any subset")
        for phone_label in all_found:
            if phone_label not in phone_super_list:
                print("OOPS!",phone_label,"in a subset but not in",phone_super_name)

        # Sonorant < Consonant
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'consonant') # only include consonants
        q = q.filter(c.phone.phon_feat_son == 1) # sonorants have the feature +son
        q.create_subset('sonorant')
        q.set_properties(seg_type_cons='sonorant')
        q.set_properties(seg_type_cons_son='approximant') # this will be changed later for certain sonorants
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        sonorants_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        #print(corpus_code+": consonants",sonorants_list)

        # Obstruent < Consonant
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'consonant') # only include consonants
        q = q.filter(c.phone.phon_feat_son == -1) # obstruents have the feature -son
        q.create_subset('obstruent')
        q.set_properties(seg_type_cons='obstruent')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        obstruents_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        #print(corpus_code+": obstruents",obstruents_list)

        # Check that Sonorant and Obstruent partition Consonant
        phone_classes = {"sonorant" : sonorants_list,
                         "obstruent" : obstruents_list}
        phone_super_list = consonants_list
        phone_super_name = "consonant"
        all_found = []
        for phone_class_name,phone_class_list in phone_classes.items():
            for phone_label in phone_class_list:
                all_found.append(phone_label)
                for phone_class_name_2,phone_class_list_2 in phone_classes.items():
                    if phone_class_name != phone_class_name_2 and phone_label in phone_class_list_2:
                        print("OOPS!",phone_label,"in both",phone_class_name,"and",phone_class_name_2)
        for phone_label in phone_super_list:
            if phone_label not in all_found:
                print("OOPS!",phone_label,"in",phone_super_name,"but not in any subset")
        for phone_label in all_found:
            if phone_label not in phone_super_list:
                print("OOPS!",phone_label,"in a subset but not in",phone_super_name)

        # High Vowel < Vowel
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'vowel') # only include vowels
        q = q.filter(c.phone.phon_feat_hi == 1) # high vowels have the feature +hi
        q.create_subset('high_vowel')
        q.set_properties(seg_type_vowel_ht='high')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        high_vowels_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        print(corpus_code+": high vowels",high_vowels_list)

        # Nonhigh Vowel < Vowel
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'vowel') # only include vowels
        q = q.filter(c.phone.phon_feat_hi == -1) # nonhigh vowels have the feature -hi
        q.create_subset('nonhigh_vowel')
        q.set_properties(seg_type_vowel_ht='nonhigh')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        nonhigh_vowels_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        print(corpus_code+": nonhigh vowels",nonhigh_vowels_list)

        # Check that High Vowel and Nonhigh Vowel partition Vowel
        phone_classes = {"high vowel" : high_vowels_list,
                         "nonhigh vowel" : nonhigh_vowels_list}
        phone_super_list = vowels_list
        phone_super_name = "vowel"
        all_found = []
        for phone_class_name,phone_class_list in phone_classes.items():
            for phone_label in phone_class_list:
                all_found.append(phone_label)
                for phone_class_name_2,phone_class_list_2 in phone_classes.items():
                    if phone_class_name != phone_class_name_2 and phone_label in phone_class_list_2:
                        print("OOPS!",phone_label,"in both",phone_class_name,"and",phone_class_name_2)
        for phone_label in phone_super_list:
            if phone_label not in all_found:
                print("OOPS!",phone_label,"in",phone_super_name,"but not in any subset")
        for phone_label in all_found:
            if phone_label not in phone_super_list:
                print("OOPS!",phone_label,"in a subset but not in",phone_super_name)

        # Long Vowel < Vowel
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'vowel') # only include vowels
        q = q.filter(c.phone.phon_feat_long == 1) # long vowels have the feature +long
        q.create_subset('long_vowel')
        q.set_properties(seg_type_vowel_ln='long')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        long_vowels_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        #print(corpus_code+": long vowels",long_vowels_list)

        # Short Vowel < Vowel
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'vowel') # only include vowels
        q = q.filter(c.phone.phon_feat_long == -1) # short vowels have the feature -long
        q.create_subset('short_vowel')
        q.set_properties(seg_type_vowel_ln='short')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        short_vowels_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        #print(corpus_code+": short vowels",short_vowels_list)

        # Check that Long Vowel and Short Vowel partition Vowel
        phone_classes = {"long vowel" : long_vowels_list,
                         "short vowel" : short_vowels_list}
        phone_super_list = vowels_list
        phone_super_name = "vowel"
        all_found = []
        for phone_class_name,phone_class_list in phone_classes.items():
            for phone_label in phone_class_list:
                all_found.append(phone_label)
                for phone_class_name_2,phone_class_list_2 in phone_classes.items():
                    if phone_class_name != phone_class_name_2 and phone_label in phone_class_list_2:
                        print("OOPS!",phone_label,"in both",phone_class_name,"and",phone_class_name_2)
        for phone_label in phone_super_list:
            if phone_label not in all_found:
                print("OOPS!",phone_label,"in",phone_super_name,"but not in any subset")
        for phone_label in all_found:
            if phone_label not in phone_super_list:
                print("OOPS!",phone_label,"in a subset but not in",phone_super_name)

        # Diphthong < Vowel
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'vowel') # only include vowels
        q = q.filter(c.phone.seg_type_complex == 'diphthong') # diphthongs are complex segments of type 'diphthong'
        q.create_subset('diphthong')
        q.set_properties(seg_type_vowel_dt='diphthong')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        diphthongs_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        #print(corpus_code+": diphthongs",diphthongs_list)

        # Monophthong < Vowel
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'vowel') # only include vowels
        q = q.filter(c.phone.seg_type_complex == 'simple') # monopthongs are not complex segments
        q.create_subset('monophthong')
        q.set_properties(seg_type_vowel_dt='monophthong')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        monophthongs_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        #print(corpus_code+": monopthongs",monophthongs_list)

        # Check that Diphthong and Monophthong partition Vowel
        phone_classes = {"diphthong" : diphthongs_list,
                         "monophthong" : monophthongs_list}
        phone_super_list = vowels_list
        phone_super_name = "vowel"
        all_found = []
        for phone_class_name,phone_class_list in phone_classes.items():
            for phone_label in phone_class_list:
                all_found.append(phone_label)
                for phone_class_name_2,phone_class_list_2 in phone_classes.items():
                    if phone_class_name != phone_class_name_2 and phone_label in phone_class_list_2:
                        print("OOPS!",phone_label,"in both",phone_class_name,"and",phone_class_name_2)
        for phone_label in phone_super_list:
            if phone_label not in all_found:
                print("OOPS!",phone_label,"in",phone_super_name,"but not in any subset")
        for phone_label in all_found:
            if phone_label not in phone_super_list:
                print("OOPS!",phone_label,"in a subset but not in",phone_super_name)

        # Nasal < Sonorant
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'sonorant') # only include sonorants
        q = q.filter(c.phone.phon_feat_nas == 1) # nasals have the feature +nas
        q.create_subset('nasal')
        q.set_properties(seg_type_cons_son='nasal')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        nasals_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        print(corpus_code+": nasals",nasals_list)

        LIQUIDS_REGEX = '^(5|r\\\\|l(?!\\\\)).*' # starts with '5' or 'r\\' or 'l' but not 'l\\'

        # Liquid < Sonorant
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'sonorant') # only include sonorants
        q = q.filter(c.phone.label.regex(LIQUIDS_REGEX)) # liquids are part of a special list
        q.create_subset('liquid')
        q.set_properties(seg_type_cons_son='liquid')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        liquids_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        if liquids_list:
            print(corpus_code+": liquids",liquids_list)

        TRILLS_REGEX = '^((R|B)\\\\|r(?!\\\\|`)).*' # starts with 'R\\' or 'B\\' or 'r' but not 'r\\' nor 'r`'

        # Trill < Sonorant
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'sonorant') # only include sonorants
        q = q.filter(c.phone.label.regex(TRILLS_REGEX)) # trills are part of a special list
        q.create_subset('trill')
        q.set_properties(seg_type_cons_son='trill')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        trills_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        if trills_list:
            print(corpus_code+": trills",trills_list)

        FLAPS_REGEX = '^(4|r`|l\\\\).*' # starts with '4' or 'r`' or 'l\\'

        # Flap < Sonorant
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'sonorant') # only include sonorants
        q = q.filter(c.phone.label.regex(FLAPS_REGEX)) # flaps are part of a special list
        q.create_subset('flap')
        q.set_properties(seg_type_cons_son='flap')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        flaps_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        if flaps_list:
            print(corpus_code+": flaps",flaps_list)

        GLOTTALS_REGEX = '^(\\?|h).*' # starts with '?' or 'h'

        # Glottal < Sonorant
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'sonorant') # only include sonorants
        q = q.filter(c.phone.label.regex(GLOTTALS_REGEX)) # glottals are part of a special list
        q.create_subset('glottal')
        q.set_properties(seg_type_cons_son='glottal')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        glottals_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        if glottals_list:
            print(corpus_code+": glottals",glottals_list)

        # Approximant < Sonorant
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'sonorant') # only include sonorants
        q = q.filter(c.phone.seg_type_cons_son == 'approximant') # only include segments which still have the default sonorant type 'apprixmant'
        #q = q.filter(c.phone.seg_type_cons_son.not_in_(['nasal','liquid','trill','flap','glottal'])) # exclude nasals, liquids, trills, flaps, and glottals
        q.create_subset('approximant')
        #q.set_properties(seg_type_cons_son='approximant')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        approximants_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        print(corpus_code+": approximants",approximants_list)

        # Check that Nasal, Liquid, Trill, Flap, and Approximant partition Sonorant
        phone_classes = {"nasal" : nasals_list,
                         "liquid" : liquids_list,
                         "trill" : trills_list,
                         "flap" : flaps_list,
                         "glottal" : glottals_list,
                         "approximant" : approximants_list}
        phone_super_list = sonorants_list
        phone_super_name = "sonorant"
        all_found = []
        for phone_class_name,phone_class_list in phone_classes.items():
            for phone_label in phone_class_list:
                all_found.append(phone_label)
                for phone_class_name_2,phone_class_list_2 in phone_classes.items():
                    if phone_class_name != phone_class_name_2 and phone_label in phone_class_list_2:
                        print("OOPS!",phone_label,"in both",phone_class_name,"and",phone_class_name_2)
        for phone_label in phone_super_list:
            if phone_label not in all_found:
                print("OOPS!",phone_label,"in",phone_super_name,"but not in any subset")
        for phone_label in all_found:
            if phone_label not in phone_super_list:
                print("OOPS!",phone_label,"in a subset but not in",phone_super_name)



        # Click < Obstruent
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'obstruent') # only include obstruents
        q = q.filter(c.phone.phon_feat_velaric == 1) # clicks have the feature +vel
        q.create_subset('click')
        q.set_properties(seg_type_cons_obs='click')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        clicks_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        #print(corpus_code+": clicks",clicks_list)

        # Affricate < Obstruent
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'obstruent') # only include obstruents
        q = q.filter(c.phone.phon_feat_velaric == -1) # affricates have the feature -vel (excludes clicks)
        # for some reason a few fricatives 'ʑ', 'ɕ', 'ɬ' have the feature +delrel, so use seg_type_complex instead
        # q = q.filter(c.phone.phon_feat_delrel == 1) # affricates have the feature +delrel
        q = q.filter(c.phone.seg_type_complex == 'affricate') # affricates are complex segments of type 'affricate'
        q.create_subset('affricate')
        q.set_properties(seg_type_cons_obs='affricate')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        affricates_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        if affricates_list:
            print(corpus_code+": affricates",affricates_list)

        # Fricative < Obstruent
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'obstruent') # only include obstruents
        q = q.filter(c.phone.phon_feat_velaric == -1) # fricatives have the feature -vel (excludes clicks)
        # for some reason a few fricatives 'ʑ', 'ɕ', 'ɬ' have the feature +delrel, so use seg_type_complex instead
        # q = q.filter(c.phone.phon_feat_delrel == -1) # fricatives have the feature -delrel (excludes affricates)
        q = q.filter(c.phone.seg_type_complex == 'simple') # fricatives are not complex segments (excludes affricates)
        q = q.filter(c.phone.phon_feat_cont == 1) # fricatives have the feature +cont
        q.create_subset('fricative')
        q.set_properties(seg_type_cons_obs='fricative')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        fricatives_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        print(corpus_code+": fricatives",fricatives_list)

        # Plosive < Obstruent
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'obstruent') # only include obstruents
        q = q.filter(c.phone.phon_feat_velaric == -1) # plosives have the feature -vel (excludes clicks)
        q = q.filter(c.phone.phon_feat_delrel == -1) # plosives have the feature -delrel (excludes affricates)
        q = q.filter(c.phone.phon_feat_cont == -1) # plosives have the feature -cont
        q.create_subset('plosive')
        q.set_properties(seg_type_cons_obs='plosive')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        plosives_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        print(corpus_code+": plosives",plosives_list)

        # Check that Click, Affricate, Fricative, and Plosive partition Obstruent
        phone_classes = {"click" : clicks_list,
                         "affricate" : affricates_list,
                         "fricative" : fricatives_list,
                         "plosive" : plosives_list}
        phone_super_list = obstruents_list
        phone_super_name = "obstruent"
        all_found = []
        for phone_class_name,phone_class_list in phone_classes.items():
            for phone_label in phone_class_list:
                all_found.append(phone_label)
                for phone_class_name_2,phone_class_list_2 in phone_classes.items():
                    if phone_class_name != phone_class_name_2 and phone_label in phone_class_list_2:
                        print("OOPS!",phone_label,"in both",phone_class_name,"and",phone_class_name_2)
        for phone_label in phone_super_list:
            if phone_label not in all_found:
                print("OOPS!",phone_label,"in",phone_super_name,"but not in any subset")
        for phone_label in all_found:
            if phone_label not in phone_super_list:
                print("OOPS!",phone_label,"in a subset but not in",phone_super_name)

        # Double Nasal < Nasal
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'nasal') # only include sonorants
        q = q.filter(c.phone.seg_type_complex == 'double_stop') # nasals have the feature +nas
        q.create_subset('double_nasal')
        q.set_properties(seg_type_cons_son_nas='double')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        double_nasals_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        if double_nasals_list:
            print(corpus_code+": double nasals",double_nasals_list)

        # Single Nasal < Nasal
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'nasal') # only include sonorants
        q = q.filter(c.phone.seg_type_complex == 'simple') # nasals have the feature +nas
        q.create_subset('single_nasal')
        q.set_properties(seg_type_cons_son_nas='single')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        single_nasals_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        if double_nasals_list:
            print(corpus_code+": single nasals",single_nasals_list)

        # Check Double Nasal and Single Nasal partition Nasal
        phone_classes = {"double nasal" : double_nasals_list,
                         "single nasal" : single_nasals_list}
        phone_super_list = nasals_list
        phone_super_name = "nasals"
        all_found = []
        for phone_class_name,phone_class_list in phone_classes.items():
            for phone_label in phone_class_list:
                all_found.append(phone_label)
                for phone_class_name_2,phone_class_list_2 in phone_classes.items():
                    if phone_class_name != phone_class_name_2 and phone_label in phone_class_list_2:
                        print("OOPS!",phone_label,"in both",phone_class_name,"and",phone_class_name_2)
        for phone_label in phone_super_list:
            if phone_label not in all_found:
                print("OOPS!",phone_label,"in",phone_super_name,"but not in any subset")
        for phone_label in all_found:
            if phone_label not in phone_super_list:
                print("OOPS!",phone_label,"in a subset but not in",phone_super_name)

        # Double Plosive < Plosive
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'plosive') # only include sonorants
        q = q.filter(c.phone.seg_type_complex == 'double_stop') # nasals have the feature +nas
        q.create_subset('double_plosive')
        q.set_properties(seg_type_cons_obs_plos='double')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        double_plosives_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        if double_plosives_list:
            print(corpus_code+": double plosives",double_plosives_list)

        # Single Plosive < Plosive
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'plosive') # only include sonorants
        q = q.filter(c.phone.seg_type_complex == 'simple') # nasals have the feature +nas
        q.create_subset('single_plosive')
        q.set_properties(seg_type_cons_obs_plos='single')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        single_plosives_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        if double_plosives_list:
            print(corpus_code+": single plosives",single_plosives_list)

        # Check Double Plosive and Single Plosive partition Plosive
        phone_classes = {"double plosive" : double_plosives_list,
                         "single nasal" : single_plosives_list}
        phone_super_list = plosives_list
        phone_super_name = "plosives"
        all_found = []
        for phone_class_name,phone_class_list in phone_classes.items():
            for phone_label in phone_class_list:
                all_found.append(phone_label)
                for phone_class_name_2,phone_class_list_2 in phone_classes.items():
                    if phone_class_name != phone_class_name_2 and phone_label in phone_class_list_2:
                        print("OOPS!",phone_label,"in both",phone_class_name,"and",phone_class_name_2)
        for phone_label in phone_super_list:
            if phone_label not in all_found:
                print("OOPS!",phone_label,"in",phone_super_name,"but not in any subset")
        for phone_label in all_found:
            if phone_label not in phone_super_list:
                print("OOPS!",phone_label,"in a subset but not in",phone_super_name)


        # Simple Click < Click
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'click') # only include clicks
        q = q.filter(c.phone.seg_type_complex == 'simple') # simple clicks are not complex segments (excludes contour clicks)
        q.create_subset('simple_click')
        q.set_properties(seg_type_cons_obs_click='simple')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        simple_clicks_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        if simple_clicks_list:
            print(corpus_code+": simple clicks",simple_clicks_list)

        # Fricative Contour Click < Click
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'click') # only include clicks
        q = q.filter(c.phone.seg_type_complex == 'contour_click_fric') # contour fricative clicks are complex segments of type 'contour_click_fric'
        q.create_subset('contfric_click')
        q.set_properties(seg_type_cons_obs_click='contfric')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        contfric_clicks_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        if contfric_clicks_list:
            print(corpus_code+": contour fricative clicks",contfric_clicks_list)

        # Plosive Contour Click < Click
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'click') # only include clicks
        q = q.filter(c.phone.seg_type_complex == 'contour_click_stop') # contour plosive clicks are complex segments of type 'contour_click_stop'
        q.create_subset('contstop_click')
        q.set_properties(seg_type_cons_obs_click='contstop')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        contstop_clicks_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        if contstop_clicks_list:
            print(corpus_code+": contour plosive clicks",contstop_clicks_list)

        # Affricate Contour Click < Click
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'click') # only include clicks
        q = q.filter(c.phone.seg_type_complex == 'contour_click_affr') # contour plosive clicks are complex segments of type 'contour_click_stop'
        q.create_subset('contaffr_click')
        q.set_properties(seg_type_cons_obs_click='contaffr')
        q = q.group_by(c.phone.label.column_name('phone'))
        q = q.aggregate(Count().column_name('count'))
        contaffr_clicks_list = [x['phone'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        if contaffr_clicks_list:
            print(corpus_code+": contour affricate clicks",contaffr_clicks_list)

        # Check that Simple, Contour Fricative, Contour Plosive, and Contour Affricate partition Click
        phone_classes = {"simple click" : simple_clicks_list,
                         "contour fricative click" : contfric_clicks_list,
                         "contour plosive click" : contstop_clicks_list,
                         "contour affrcate click" : contaffr_clicks_list}
        phone_super_list = clicks_list
        phone_super_name = "click"
        all_found = []
        for phone_class_name,phone_class_list in phone_classes.items():
            for phone_label in phone_class_list:
                all_found.append(phone_label)
                for phone_class_name_2,phone_class_list_2 in phone_classes.items():
                    if phone_class_name != phone_class_name_2 and phone_label in phone_class_list_2:
                        print("OOPS!",phone_label,"in both",phone_class_name,"and",phone_class_name_2)
        for phone_label in phone_super_list:
            if phone_label not in all_found:
                print("OOPS!",phone_label,"in",phone_super_name,"but not in any subset")
        for phone_label in all_found:
            if phone_label not in phone_super_list:
                print("OOPS!",phone_label,"in a subset but not in",phone_super_name)

        # All Nonspeech Segments
        q = c.query_graph(c.phone)
        q = q.filter(c.phone.subset == 'nonspeech') # only include nonspeech segments
        q = q.group_by(c.phone.label.column_name('segment'))
        q = q.aggregate(Count().column_name('count'))
        nonspeech_segments_list = [x['segment'] for x in q] # [x['phone'] for x in sorted(q, key = lambda x: x['count'], reverse = True)]
        #print(corpus_code+": all nonspeech segments",nonspeech_segments_list)

        # All Speech Words
        q = c.query_graph(c.word)
        q = q.filter(c.word.label.not_in_(nonspeech_segments_list)) # exclude words whose labels are nonspeech segments
        q.create_subset('speech_words')

    with CorpusContext(corpus_name) as c:
        print(corpus_code+": Encoding Pauses...")
        c.encode_pauses(nonspeech_segments_list)

    with CorpusContext(corpus_name) as c:
        print(corpus_code+": Encoding Syllabic Segments...")
        c.encode_syllabic_segments(syllabic_phones_list)
        print(corpus_code+": Encoding Syllables...")
        c.encode_syllables()

    with CorpusContext(corpus_name) as c:
        print(corpus_code+": Encoding Counts...")
        c.encode_count('utterance', 'phone', 'num_phones_uttr')
        c.encode_count('utterance', 'syllable', 'num_sylls_uttr')
        #c.encode_count('utterance', 'word', 'num_words_uttr')
        c.encode_count('utterance', 'word', 'num_words_uttr',subset='speech_words')
        c.encode_count('word', 'phone', 'num_phones_word')
        c.encode_count('word', 'syllable', 'num_sylls_word')
        c.encode_count('syllable', 'phone', 'num_phones_syll')