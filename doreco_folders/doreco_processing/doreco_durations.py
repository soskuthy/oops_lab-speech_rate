import polyglotdb
from polyglotdb import CorpusContext

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
    corpus_name = 'doreco_'+corpus_code

    durations_output_filename = corpus_name+'_durations.csv'
    durations_output_path = '../doreco_data/'+durations_output_filename

    
    with CorpusContext(corpus_name) as c:
        print(corpus_code+": Querying Corpus")
        q = c.query_graph(c.phone)
        q = q.columns(c.phone.speaker.name.column_name('speaker'),
                    c.phone.speaker.sex.column_name('sex'),
                    c.phone.speaker.age.column_name('age'),
                    c.phone.speaker.age_c.column_name('age_c'),
                    c.phone.discourse.name.column_name('discourse'),
                    c.phone.discourse.spk_code.column_name('all_speakers'),
                    c.phone.discourse.genre.column_name('genre'),
                    c.phone.discourse.sound_quality.column_name('sound_quality'),
                    c.phone.discourse.background_noise.column_name('background_noise'),
                    c.phone.utterance.id.column_name('uttr_id'),
                    c.phone.utterance.num_phones_uttr.column_name('num_phones_uttr'),
                    c.phone.utterance.num_sylls_uttr.column_name('num_sylls_uttr'),
                    c.phone.utterance.num_words_uttr.column_name('num_words_uttr'),
                    c.phone.utterance.begin.column_name('uttr_start'),
                    c.phone.utterance.end.column_name('uttr_end'),
                    c.phone.utterance.duration.column_name('uttr_dur'),
                    c.phone.word.id.column_name('word_id'),
                    c.phone.word.label.column_name('word'),
                    c.phone.word.num_phones_word.column_name('num_phones_word'),
                    c.phone.word.num_sylls_word.column_name('num_sylls_word'),
                    c.phone.word.begin.column_name('word_start'),
                    c.phone.word.end.column_name('word_end'),
                    c.phone.word.duration.column_name('word_dur'),
                    c.phone.syllable.id.column_name('syll_id'),
                    c.phone.syllable.label.column_name('syllable'),
                    c.phone.syllable.num_phones_syll.column_name('num_phones_syll'),
                    c.phone.syllable.begin.column_name('syll_start'),
                    c.phone.syllable.end.column_name('syll_end'),
                    c.phone.syllable.duration.column_name('syll_dur'),
                    c.phone.label.column_name('phone'),
                    c.phone.ipa.column_name('phone_ipa'),
                    c.phone.phon_feat_syl.column_name('phon_feat_syl'),
                    c.phone.phon_feat_son.column_name('phon_feat_son'),
                    c.phone.phon_feat_cons.column_name('phon_feat_cons'),
                    c.phone.phon_feat_cont.column_name('phon_feat_cont'),
                    c.phone.phon_feat_delrel.column_name('phon_feat_delrel'),
                    c.phone.phon_feat_lat.column_name('phon_feat_lat'),
                    c.phone.phon_feat_nas.column_name('phon_feat_nas'),
                    c.phone.phon_feat_strid.column_name('phon_feat_strid'),
                    c.phone.phon_feat_voi.column_name('phon_feat_voi'),
                    c.phone.phon_feat_sg.column_name('phon_feat_sg'),
                    c.phone.phon_feat_cg.column_name('phon_feat_cg'),
                    c.phone.phon_feat_ant.column_name('phon_feat_ant'),
                    c.phone.phon_feat_cor.column_name('phon_feat_cor'),
                    c.phone.phon_feat_distr.column_name('phon_feat_distr'),
                    c.phone.phon_feat_lab.column_name('phon_feat_lab'),
                    c.phone.phon_feat_hi.column_name('phon_feat_hi'),
                    c.phone.phon_feat_lo.column_name('phon_feat_lo'),
                    c.phone.phon_feat_back.column_name('phon_feat_back'),
                    c.phone.phon_feat_round.column_name('phon_feat_round'),
                    c.phone.phon_feat_velaric.column_name('phon_feat_velaric'),
                    c.phone.phon_feat_tense.column_name('phon_feat_tense'),
                    c.phone.phon_feat_long.column_name('phon_feat_long'),
                    c.phone.phon_feat_hitone.column_name('phon_feat_hitone'),
                    c.phone.phon_feat_hireg.column_name('phon_feat_hireg'),
                    c.phone.previous.label.column_name('previous_phone'),
                    c.phone.following.label.column_name('following_phone'),
                    c.phone.seg_type.column_name('segtype'),
                    c.phone.seg_type_nonsp.column_name('segtype_nonspeech'),
                    c.phone.seg_type_nonsp_nonal.column_name('segtype_nonaligned'),
                    c.phone.seg_type_complex.column_name('segtype_complex'),
                    c.phone.seg_type_syll.column_name('segtype_syllabic'),
                    c.phone.seg_type_cons.column_name('segtype_consonant'),
                    c.phone.seg_type_vowel_ht.column_name('segtype_vowel_height'),
                    c.phone.seg_type_vowel_ln.column_name('segtype_vowel_length'),
                    c.phone.seg_type_vowel_dt.column_name('segtype_vowel_dipthongality'),
                    c.phone.seg_type_cons_son.column_name('segtype_sonorant'),
                    c.phone.seg_type_cons_obs.column_name('segtype_obstruent'),
                    c.phone.seg_type_cons_obs_click.column_name('segtype_click'),
                    c.phone.begin.column_name('phone_start'), 
                    c.phone.end.column_name('phone_end'),
                    c.phone.duration.column_name('phone_dur')
        )
        results = q.all()
        print(corpus_code+": Writing results to CSV",durations_output_filename)
        q.to_csv(durations_output_path)