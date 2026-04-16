import pandas as pd
from panphon.segment import Segment

NA_VALUE_LIST = ['na','none']
NA_SUFFIX = '_from_doreco_metadata'

IPA_REPLACEMENTS = {'ɚ' : 'ə˞',
                    '͡':'',
                    'ʡ':'q', # this is a stopgap for ʡ missing from panphon feature table
                    #'ts' : 't͡s',
                    #'dz' : 'd͡z',
                    #'kx' : 'k͡x',
                    }
XSAMPA_REPLACEMENTS = {'n_jn' : 'n:_j',
                       '_j' : "'",
                       }

STRONG_FEATURES = {'cont':-1,
                   'sg':1, # not proven to be necessary
                   'cg':1,
                   #'ant':1,
                   #'distr':1,
                   'lab':1,
                   'hi':1,
                   'lo':1, # not proven to be necessary
                   'back':1,
                   'round':1, # not proven to be necessary
                   'velaric':1, # for clicks
                   'tense':1, # not proven to be necessary
                   }

def subset_discourse_metadata(input_csv_path,output_csv_path):
    df = pd.read_csv(input_csv_path,
                     dtype = str,
                     usecols=[#'id',
                              'name',
                              'spk_code',#'spk_age','spk_age_c','spk_sex',
                              'rec_date','rec_date_c',
                              'genre','genre_stim',
                              #'gloss','transl',
                              'sound_quality','background_noise',
                              'word_tokens','word_tokens_core',
                              'extended'
                              ])
    df.replace(NA_VALUE_LIST,[v+NA_SUFFIX for v in NA_VALUE_LIST],inplace=True)
    df.to_csv(output_csv_path,na_rep="ERROR (this shouldn't be here)",index=False)

def subset_speaker_metadata(input_csv_path,output_csv_path,split_char='/',name_col='code'):
    df = pd.read_csv(input_csv_path,
                     dtype = str,
                     usecols=[#'id',
                              #'name',
                              'spk_code','spk_age','spk_age_c','spk_sex',
                              #'rec_date','rec_date_c',
                              #'genre',#'genre_stim',
                              #'gloss','transl',
                              #'sound_quality','background_noise',
                              #'word_tokens','word_tokens_core',
                              #'extended'
                              ])
    df.replace(NA_VALUE_LIST,[v+NA_SUFFIX for v in NA_VALUE_LIST],inplace=True)
    df = df.rename(lambda column_label: column_label.replace("spk_",""), axis="columns")
    df.drop_duplicates(keep='first', inplace=True, ignore_index=True)
    old_names = df[name_col].to_list()
    split_names = []
    new_rows_dict = {}
    for field in list(df):
        new_rows_dict[field] = []
    for row in df.itertuples(index=False):
        names = row[0]
        if split_char not in str(names):
            continue
        else:
            split_names.append(row.code)
            for spk_ind,name in enumerate(names.split(split_char)):
                if name in old_names or name in new_rows_dict[name_col]:
                    continue
                else:
                    for col_ind,col in enumerate(row):
                        field = row._fields[col_ind]
                        if split_char in col:
                            new_entry = row[col_ind].split(split_char)[spk_ind]
                        elif split_char not in col:
                            new_entry = row[col_ind]
                        new_rows_dict[field].append(new_entry)
    new_rows_df = pd.DataFrame(new_rows_dict)
    split_names_removed_df = df[~df[name_col].isin(split_names)]
    new_df = pd.concat([split_names_removed_df,new_rows_df])
    new_df.to_csv(output_csv_path,na_rep="ERROR (this shouldn't be here)",index=False)

def get_phon_features(xsampa_str,feature_table,permissive_feature_table=None,
                        prefix=None,return_complex=True,
                        complex_tests={'diphthong':[{'syl':1},{'syl':1}],
                                       'affricate':[{'cons':1,'cont':-1,'velaric':-1},{'cons':1,'cont':1}],
                                       'double_stop':[{'cons':1,'cont':-1,'velaric':-1},{'cons':1,'cont':-1}],
                                       'contour_click_fric':[{'cons':1,'cont':-1,'velaric':1},{'cons':1,'cont':1,'velaric':-1}],
                                       'contour_click_stop':[{'cons':1,'cont':-1,'velaric':1},{'cons':1,'cont':-1,'velaric':-1}],
                                       'contour_click_affr':[{'cons':1,'cont':-1,'velaric':1},{'cons':1,'cont':-1,'velaric':-1},{'cons':1,'cont':1,'velaric':-1}],
                                       },
                        complex_params={'diphthong':{'strong_features':STRONG_FEATURES},
                                        'affricate':{'forced_features':{'delrel':1},
                                                     'strong_features':STRONG_FEATURES},
                                        'double_stop':{'strong_features':STRONG_FEATURES},
                                        'contour_click_fric':{'forced_features':{'delrel':1},
                                                              'strong_features':STRONG_FEATURES},
                                        'contour_click_stop':{'forced_features':{'delrel':1},
                                                              'strong_features':STRONG_FEATURES},
                                        'contour_click_affr':{'forced_features':{'delrel':1},
                                                              'strong_features':STRONG_FEATURES}}):
    segment,complex_type = get_segment(xsampa_str=xsampa_str,
                                       feature_table=feature_table,
                                       permissive_feature_table=permissive_feature_table,
                                       complex_tests=complex_tests,
                                       complex_params=complex_params)
    phon_features_dict = {prefix+key:val for key,val in segment.data.items()}
    if not return_complex:
        return phon_features_dict
    else:
        return phon_features_dict,complex_type

def get_segment(xsampa_str,feature_table,permissive_feature_table=None,
                        complex_tests={'diphthong':[{'syl':1},{'syl':1}],
                                       'affricate':[{'cons':1,'cont':-1,'velaric':-1},{'cons':1,'cont':1}],
                                       'double_stop':[{'cons':1,'cont':-1,'velaric':-1},{'cons':1,'cont':-1}],
                                       'contour_click_fric':[{'cons':1,'cont':-1,'velaric':1},{'cons':1,'cont':1,'velaric':-1}],
                                       'contour_click_stop':[{'cons':1,'cont':-1,'velaric':1},{'cons':1,'cont':-1,'velaric':-1}],
                                       'contour_click_affr':[{'cons':1,'cont':-1,'velaric':1},{'cons':1,'cont':-1,'velaric':-1},{'cons':1,'cont':1,'velaric':-1}],
                                       },
                        complex_params={'diphthong':{'strong_features':STRONG_FEATURES},
                                        'affricate':{'forced_features':{'delrel':1},
                                                     'strong_features':STRONG_FEATURES},
                                        'double_stop':{'strong_features':STRONG_FEATURES},
                                        'contour_click_fric':{'forced_features':{'delrel':1},
                                                              'strong_features':STRONG_FEATURES},
                                        'contour_click_stop':{'forced_features':{'delrel':1},
                                                              'strong_features':STRONG_FEATURES},
                                        'contour_click_affr':{'forced_features':{'delrel':1},
                                                              'strong_features':STRONG_FEATURES}}):
    print_segment_info = {'reg': False,
                          'spec': False,
                          'comp': False,
                          'comp_sub': False,
                          'comp_unk': False}
    is_complex = False
    complex_type = None
    ipa_str = to_ipa_normed(xsampa_str,feature_table)
    ipa_str_list = feature_table.ipa_segs(ipa_str)
    #print("X-SAMPA:",xsampa_str,"IPA:",ipa_str)
    assert(len(ipa_str_list) > 0)
    if len(ipa_str_list) == 1:
        if feature_table.seg_known(ipa_str):
            segment = get_segment_from_ft(ipa_str,feature_table)
            if print_segment_info['reg']:
                print("REGULAR SEGMENT X-SAMPA:",xsampa_str,"IPA:",ipa_str)
                print(segment)
        elif not feature_table.seg_known(ipa_str):
            segment = get_segment_from_permissive_ft(ipa_str,feature_table,permissive_feature_table)
            if print_segment_info['spec']:
                print("SPECIALLY PARSED! X-SAMPA:",xsampa_str,"IPA:",ipa_str)
                print(segment)
    elif len(ipa_str_list) > 1:
        #assert(len(ipa_str_list) == 2)
        complex_type = complex_segment_tests(ipa_str,complex_tests,feature_table)
        if complex_type:
            segment = get_complex_segment(ipa_str_list,
                                          feature_table,
                                          **complex_params[complex_type])
            if print_segment_info['comp']:
                print("COMPLEX",complex_type,"X-SAMPA:",xsampa_str,"IPA:",ipa_str)
                if print_segment_info['comp_sub']:
                    for i,s in enumerate(ipa_str_list):
                        print("SEGMENT #"+str(i+1)+":",feature_table.fts(s))
                    print("COMBINED:  ",segment)
                else:
                    print(segment)
        else:
            segment = Segment(feature_table.names)
            complex_type = 'unknown'
            if print_segment_info['comp_unk']:
                print("UNKNOWN COMPLEX SEGMENT.")
                print("X-SAMPA:",xsampa_str,"IPA:",ipa_str)
                if print_segment_info['comp_sub']:
                    for i,s in enumerate(ipa_str_list):
                        print("SEGMENT #"+str(i+1)+":",feature_table.fts(s))
                    print("COMBINED:  ",segment)
                else:
                    print(segment)
            # if feature_table.seg_known(ipa_str):
            #     segment = get_segment_from_ft(ipa_str,feature_table)
            #     if print_segment_info['comp_reg']:
            #         print("COMPOUND REGULAR X-SAMPA:",xsampa_str,"IPA:",ipa_str)
            #         if print_segment_info['comp_sub']:
            #             for i,s in enumerate(ipa_str_list):
            #                 print("SEGMENT #"+str(i+1)+":",get_segment_from_ft(s,feature_table))
            #             print("COMBINED:  ",segment)
            #         else:
            #             print(segment)
            # elif not feature_table.seg_known(ipa_str):
            #     segment = get_segment_from_permissive_ft(ipa_str,
            #                                              feature_table,
            #                                              permissive_feature_table)
            #     if print_segment_info['comp_spec']:
            #         print("COMPOUND SPECIALLY PARSED X-SAMPA:",xsampa_str,"IPA:",ipa_str)
            #         if print_segment_info['comp_sub']:
            #             for i,s in enumerate(ipa_str_list):
            #                 #print("SEGMENT #"+str(i+1)+":",feature_table.fts(s))
            #                 print("SEGMENT #"+str(i+1)+"p:",get_segment_from_permissive_ft(s,
            #                                                                               feature_table,
            #                                                                               permissive_feature_table))
            #             print("COMBINED:  ",segment)
            #         else:
            #             print(segment)
            
    return segment,complex_type

def get_segment_from_ft(ipa_str,feature_table):
    assert(feature_table.seg_known(ipa_str))
    return feature_table.fts(ipa_str)

def get_segment_from_permissive_ft(ipa_str,feature_table,permissive_feature_table):
    assert(permissive_feature_table.seg_known(ipa_str))
    feature_set = permissive_feature_table.fts(ipa_str)
    feature_dict = dict((name,spec) for spec,name in feature_set)
    segment = Segment(feature_table.names)
    for feature_name in feature_table.names:
        segment.data[feature_name] = segment.s2n[feature_dict[feature_name]]
    return segment

def complex_segment_test(ipa_str,complex_test,feature_table):
    test_results = feature_table.match_pattern(complex_test,ipa_str)
    if test_results:
        return(all(test_results))
    else:
        return(False)

def complex_segment_tests(ipa_str,complex_tests,feature_table):
    for complex_type,complex_test in complex_tests.items():
        if complex_segment_test(ipa_str,complex_test,feature_table):
            return complex_type
    return None

def get_complex_segment(ipa_str_list,feature_table,
                        strong_features=None,
                        forced_features=None,
                        #first_features=None,
                        #last_features=None
                        ):
    segment = Segment(feature_table.names)
    #intersection = feature_table.fts_intersection(ipa_str_list).data
    #first = feature_table.fts(ipa_str_list[0]).data
    last = feature_table.fts(ipa_str_list[-1]).data
    for feature_name in feature_table.names:
        segment.data[feature_name] = last[feature_name]
        # if feature_name in intersection:
        #     segment.data[feature_name] = intersection[feature_name]
        if strong_features and feature_name in strong_features and feature_table.fts_match_any({feature_name:strong_features[feature_name]},ipa_str_list):
            segment.data[feature_name] = strong_features[feature_name]
        # elif first_features and feature_name in first_features:
        #     segment.data[feature_name] = first[feature_name]
        #     if last_features:
        #         assert(feature_name not in last_features)
        # elif last_features and feature_name in last_features:
        #     segment.data[feature_name] = last[feature_name]
        if forced_features and feature_name in forced_features.keys():
            segment.data[feature_name] = forced_features[feature_name]
    return segment

def normalize_xsampa(xsampa_str):
    new_xsampa_str = xsampa_str
    if new_xsampa_str[0] == "=":
        new_xsampa_str = "'"+new_xsampa_str
    for old,new in XSAMPA_REPLACEMENTS.items():
        new_xsampa_str = new_xsampa_str.replace(old,new)
    return new_xsampa_str

def normalize_ipa(ipa_str):
    new_ipa_str = ipa_str
    for old,new in IPA_REPLACEMENTS.items():
        new_ipa_str = new_ipa_str.replace(old,new)
    return new_ipa_str

def to_ipa_normed(xsampa_str,feature_table):
    xsampa_str = normalize_xsampa(xsampa_str)
    ipa_str = feature_table.xsampa.convert(xsampa_str)
    ipa_str = normalize_ipa(ipa_str)
    return ipa_str
