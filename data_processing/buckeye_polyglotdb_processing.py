import polyglotdb 
from polyglotdb import CorpusContext
from polyglotdb.io.parsers.speaker import DirectorySpeakerParser
import polyglotdb.io as pgio
from polyglotdb.query.base.func import Count, Average
from polyglotdb.acoustics.formants.base import analyze_formant_points
from polyglotdb.acoustics.formants.refined import analyze_formant_points_refinement
from polyglotdb.acoustics.formants.helper import save_formant_point_data

# todo: change phones -> phone and words -> word in textgrid tier names

# change this path to where you put the pg_tutorial directory after downloading, unzipping from tutorial site
corpus_root = '/Users/soskuthy/Documents/Research/current/2017/mfcc_word_sim/buckeye'

parser = pgio.inspect_buckeye(corpus_root)

# for verbose output during corpus import:
parser.call_back = print

with CorpusContext('buckeye') as c:
    c.reset()

with CorpusContext('buckeye') as c:
    c.load(parser, corpus_root)

# checking if everything is as it should be
# speakers, files, list of phones
with CorpusContext('buckeye') as c:
    print('Speakers:', c.speakers)
    print('Discourses:', c.discourses)
    q = c.query_lexicon(c.lexicon_phone)
    q = q.order_by(c.lexicon_phone.label)
    q = q.columns(c.lexicon_phone.label.column_name('phone'))
    results = q.all()
    print(results)

# enrichment time! encoding utterances
pause_labels = ['<SIL>','<sil>','sp','','sil','spn', '<EXCLUDE-name>',
'<EXCLUDE>', '<exclude-Name>', '?', 'EXCLUDE', 'IVER', 'IVER y', 'IVER-LAUGH',
'LAUGH', 'NOISE', 'SIL', 'UNKNOWN', 'VOCNOISE', '{B_TRANS}', '{E_TRANS}']

with CorpusContext('buckeye') as c:
    c.encode_pauses(pause_labels)
    c.encode_utterances(min_pause_length=0.15)

with CorpusContext('buckeye') as c:
    q = c.query_graph(c.utterance)
    results = q.aggregate(Count().column_name('count'), Average(c.utterance.duration).column_name('average_duration'))


vowels = ["aa", "ae", "ay", "aw", "ao", "oy", "ow", "eh", "ey", "er", "ah", "uw", "ih", "iy", "uh",
          "aan", "aen", "ayn", "awn", "aon", "oyn", "own", "ehn", "eyn", "ern", "ahn", "uwn", "ihn", "iyn", "uhn"]
syllabic = vowels + ["en", "em", "eng", "el"]

with CorpusContext('buckeye') as c:
    c.encode_type_subset('phone', vowels, 'vowel')

with CorpusContext('buckeye') as c:
    c.encode_type_subset('phone', syllabic, 'syllabic')

with CorpusContext('buckeye') as c:
    q = c.query_graph(c.phone)
    q.set_properties(segtype='consonant')

with CorpusContext('buckeye') as c:
    q = c.query_graph(c.phone)
    q = q.filter(c.phone.label.in_(vowels))
    q.set_properties(segtype='vowel')

with CorpusContext('buckeye') as c:
    q = c.query_graph(c.phone)
    q = q.filter(c.phone.label.in_(pause_labels))
    q.set_properties(segtype='non-speech')


with CorpusContext('buckeye') as c:
    c.encode_syllables(syllabic_label='vowel')

with CorpusContext('buckeye') as c:
    c.encode_rate('utterance', 'syllable', 'speech_rate')
    c.encode_rate('utterance', 'phone', 'speech_rate_phone')

print("Encoding counts")
with CorpusContext('buckeye') as c:
    c.encode_count('word', 'syllable', 'num_syllables_word')
    c.encode_count('utterance', 'syllable', 'num_syllables_uttr')
    c.encode_count('syllable', 'phone', 'num_phones_syll')
    c.encode_count('word', 'phone', 'num_phones_word')
    c.encode_count('utterance', 'word', 'num_words_uttr')


# formant measurements: to be filled in; strategy:
    # (1) automatically calculated prototypes with pgdb
    # (2) further filtering in R, manual prototypes
    # (3) a further round of f measurements with R-based prototypes
# (also, we want full tracks on the second go!)

# for refined measurements
#with CorpusContext('buckeye') as c:
#    c.config.praat_path = "/Applications/Praat.app/Contents/MacOS/Praat"
#    analyze_formant_points_refinement(c, 
#        vowel_prototypes_path="/Users/soskuthy/Documents/Research/data/xling-corpus/mandarin_processing/buckeye_prototypes.csv"
#    )

# for refined formant tracks
#with CorpusContext('buckeye') as c:
#    c.config.praat_path = "/Applications/Praat.app/Contents/MacOS/Praat"
#    analyze_formant_points_refinement(c,
#        output_tracks=True, 
#        vowel_prototypes_path="/Users/soskuthy/Documents/Research/data/xling-corpus/mandarin_processing/buckeye_prototypes.csv"
#    )

#speaker_csv_path = '/Users/soskuthy/Documents/Research/data/xling-corpus/forced_aligned/buckeye_demographic.csv'
#with CorpusContext('buckeye') as c:
#    c.enrich_speakers_from_csv(speaker_csv_path)



