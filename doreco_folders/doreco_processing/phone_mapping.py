import pandas as pd
from collections import defaultdict


MAPPING = {
    'a': 'non-high monophthong', 'ai': 'diphthong', 'aɪ': 'diphthong', 'aʊ': 'diphthong', 'aː': 'non-high monophthong',
    'aˤ': 'non-high monophthong', 'ã': 'non-high monophthong', 'ãˤ': 'non-high monophthong',
    'b': 'stop', 'bʲ': 'stop', 'bʷ': 'stop', 'bː': 'stop',
    'c': 'stop', 'cx': 'affricate', 'cʰ': 'stop', 'cː': 'stop',
    'd': 'stop', 'dz': 'affricate', 'dʐ': 'affricate', 'dʑ': 'affricate', 'dʒ': 'affricate', 'dʒʲ': 'affricate',
    'dʲ': 'stop', 'dː': 'stop',
    'e': 'non-high monophthong', 'ei': 'diphthong', 'eiː': 'diphthong', 'eə': 'diphthong', 'eɪ': 'diphthong',
    'eː': 'non-high monophthong', 'eˤ': 'non-high monophthong', 'ẽ': 'non-high monophthong', 'e̝': 'non-high monophthong',
    'f': 'fricative', 'fʲ': 'fricative', 'fʷ': 'fricative', 'fː': 'fricative', 'h': 'fricative',
    'i': 'high monophthong', 'ie': 'diphthong', 'iː': 'high monophthong', 'ĩ': 'high monophthong',
    'j': 'approximant', 'jː': 'approximant',
    'k': 'stop', 'kp': 'stop', 'ks': 'affricate', 'kxʼ': 'affricate', 'kʰ': 'stop', 'kʲ': 'stop', 'kʲʰ': 'stop',
    'kʷ': 'stop', 'kʷʼ': 'stop', 'kʼ': 'stop', 'kː': 'stop', 'kːʷ': 'stop',
    'l': 'liquid', 'lʲ': 'liquid', 'lː': 'liquid',
    'm': 'nasal', 'mp': 'nasal', 'mʲ': 'nasal', 'mʷ': 'nasal', 'mː': 'nasal', 'm̥': 'nasal',
    'n': 'nasal', 'np': 'nasal', 'nʲ': 'nasal', 'nː': 'nasal', 'nːʲ': 'nasal', 'n̥': 'nasal',
    'o': 'non-high monophthong', 'oi': 'diphthong', 'oɪ': 'diphthong', 'oʉ': 'diphthong', 'oʉː': 'diphthong',
    'oː': 'non-high monophthong', 'oˤ': 'non-high monophthong', 'õ': 'non-high monophthong', 'õˤ': 'non-high monophthong',
    'o̝': 'non-high monophthong',
    'p': 'stop', 'pʰ': 'stop', 'pʲ': 'stop', 'pʲʰ': 'stop', 'pʼ': 'stop', 'pː': 'stop',
    'q': 'stop', 'qʰ': 'stop', 'qʼ': 'stop', 'qː': 'stop',
    'r': 'liquid', 'rʲ': 'liquid', 'rː': 'liquid',
    's': 'fricative', 'sʰ': 'fricative', 'sʲ': 'fricative', 'sː': 'fricative',
    't': 'stop', 'ts': 'affricate', 'tsʰ': 'affricate', 'tsʼ': 'affricate', 'tɕ': 'affricate', 'tɕʰ': 'affricate',
    'tɕː': 'affricate', 'tʃ': 'affricate', 'tʃʰ': 'affricate', 'tʃʲ': 'affricate', 'tʃʼ': 'affricate', 'tʰ': 'stop',
    'tʲ': 'stop', 'tʲʰ': 'stop', 'tʼ': 'stop', 'tː': 'stop', 'tːs': 'affricate', 'tːʃ': 'affricate', 'tːʲ': 'stop',
    'u': 'high monophthong', 'ua': 'diphthong', 'ui': 'diphthong', 'uo': 'diphthong', 'uː': 'high monophthong',
    'uˤ': 'high monophthong', 'ũ': 'high monophthong',
    'v': 'fricative', 'vʲ': 'fricative', 'v̩': 'syllabic C', 'ṽ̩': 'syllabic C',
    'w': 'approximant', 'wʲ': 'approximant', 'wː': 'approximant', 'w̃': 'approximant',
    'x': 'fricative', 'xː': 'fricative',
    'y': 'high monophthong', 'yø': 'diphthong', 'yː': 'high monophthong',
    'z': 'fricative', 'zʲ': 'fricative', 'z̩': 'syllabic C',
    'æ': 'non-high monophthong', 'æː': 'non-high monophthong', 'æ̃': 'non-high monophthong',
    'ç': 'fricative', 'ð': 'fricative',
    'ø': 'non-high monophthong', 'øː': 'non-high monophthong',
    'ħ': 'fricative',
    'ŋ': 'nasal', 'ŋm': 'nasal', 'ŋː': 'nasal', 'ŋ̥': 'nasal',
    'œ': 'non-high monophthong',
    'ǀ': 'click', 'ǀq': 'click', 'ǀqʰ': 'click', 'ǀqχʼ': 'click', 'ǀʰ': 'click', 'ǀʼ': 'click', 'ǀ̃': 'click',
    'ǀ̃ʰ': 'click', 'ǀ̬': 'click', 'ǀχ': 'click', 'ǁ': 'click', 'ǁq': 'click', 'ǁqʰ': 'click', 'ǁqχʼ': 'click',
    'ǁʰ': 'click', 'ǁʼ': 'click', 'ǁ̃': 'click', 'ǁ̬': 'click', 'ǁχ': 'click', 'ǂ': 'click', 'ǂq': 'click',
    'ǂqʰ': 'click', 'ǂqχʼ': 'click', 'ǂʰ': 'click', 'ǂʼ': 'click', 'ǂ̃': 'click', 'ǂ̃ʰ': 'click', 'ǂ̬': 'click',
    'ǂχ': 'click', 'ǃ': 'click', 'ǃq': 'click', 'ǃqʰ': 'click', 'ǃqχʼ': 'click', 'ǃʰ': 'click', 'ǃʼ': 'click',
    'ǃ̃': 'click', 'ǃ̃ʰ': 'click', 'ǃ̬': 'click', 'ǃχ': 'click',
    'ɐ': 'non-high monophthong', 'ɐɪ': 'diphthong', 'ɐʊ': 'diphthong',
    'ɑ': 'non-high monophthong', 'ɑi': 'diphthong', 'ɑiː': 'diphthong', 'ɑː': 'non-high monophthong',
    'ɑ̃': 'non-high monophthong', 'ɒ': 'non-high monophthong',
    'ɓ': 'stop',
    'ɔ': 'non-high monophthong', 'ɔɪ': 'diphthong', 'ɔː': 'non-high monophthong',
    'ɕ': 'fricative', 'ɕʰ': 'fricative', 'ɕː': 'fricative', 'ɖ': 'stop', 'ɗ': 'stop',
    'ə': 'non-high monophthong', 'əe': 'diphthong', 'əʊ': 'diphthong', 'əː': 'non-high monophthong',
    'əːe': 'diphthong', 'ə˞': 'non-high monophthong', 'ɛ': 'non-high monophthong', 'ɛː': 'non-high monophthong',
    'ɜː': 'non-high monophthong',
    'ɟ': 'stop', 'ɟː': 'stop',
    'ɡ': 'stop', 'ɡʲ': 'stop', 'ɡʷ': 'stop', 'ɡː': 'stop', 'ɡːʷ': 'stop',
    'ɣ': 'fricative', 'ɤ': 'non-high monophthong', 'ɦ': 'fricative',
    'ɨ': 'high monophthong', 'ɨa': 'diphthong', 'ɨː': 'high monophthong', 'ɪ': 'high monophthong', 'ɪə': 'diphthong',
    'ɪː': 'high monophthong',
    'ɫ': 'liquid', 'ɬ': 'fricative', 'ɭ': 'liquid',
    'ɯ': 'high monophthong', 'ɯː': 'high monophthong',
    'ɲ': 'nasal', 'ɲ̟': 'nasal', 'ɲ̥': 'nasal', 'ɳ': 'nasal', 'ɸ': 'fricative',
    'ɹ': 'approximant', 'ɹ̝': 'approximant', 'ɹ̩': 'syllabic C', 'ɻ': 'approximant',
    'ɾ': 'liquid', 'ʁ': 'liquid', 'ʁʲ': 'liquid',
    'ʂ': 'fricative', 'ʃ': 'fricative', 'ʃʲ': 'fricative', 'ʃː': 'fricative',
    'ʈ': 'stop', 'ʈʂ': 'affricate', 'ʈʂʰ': 'affricate', 'ʈʰ': 'stop',
    'ʉ': 'high monophthong', 'ʉː': 'high monophthong', 'ʊ': 'high monophthong', 'ʊə': 'diphthong',
    'ʊː': 'high monophthong', 'ʌ': 'non-high monophthong',
    'ʐ': 'fricative', 'ʑ': 'fricative', 'ʒ': 'fricative',
    'ʔ': 'stop', 'ʔʲ': 'stop',
    'ʘ': 'click', 'ʘq': 'click', 'ʘʼ': 'click', 'ʘ̃': 'click', 'ʘχ': 'click',
    'ʝ': 'fricative', 'β': 'fricative', 'βʲ': 'fricative', 'θ': 'fricative', 'χ': 'fricative', 'χʷ': 'fricative',
    'χː': 'fricative', 'χːʷ': 'fricative'
}

df = pd.read_csv('../doreco_data/DoReCo.csv')
lang_dict = defaultdict(set)

for index, row in df.iterrows():
    lang_dict[row['language']].add((row['phone'], row['phone_ipa']))

records = []

for lang, phones in lang_dict.items():
    for phone in phones:
        records.append({'lang': lang, 'phone': phone[0], 'phone_ipa': phone[1], 'c_type': MAPPING[phone[1]] if pd.notnull(phone[1]) else None})

df = pd.DataFrame.from_records(records)
df.to_csv('../doreco_data/phone_mapping.csv', index=False)