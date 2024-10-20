import polyglotdb 
from polyglotdb import CorpusContext
from polyglotdb.io.parsers.speaker import DirectorySpeakerParser
import polyglotdb.io as pgio
from polyglotdb.query.base.func import Count, Average
from polyglotdb.acoustics.formants.base import analyze_formant_points
from polyglotdb.acoustics.formants.refined import analyze_formant_points_refinement
from polyglotdb.acoustics.formants.helper import save_formant_point_data

# path to forced aligned files + speaker info csv (these shouldn't be in the github folder!)
corpus_root = '/Users/soskuthy/Documents/Research/Data/xling-corpus/forced_aligned/taiwanese_mandarin'
speaker_csv_path = '/Users/soskuthy/Documents/Research/data/xling-corpus/forced_aligned/taiwanese_mandarin_demographic.csv'

# reading in Mandarin data - would normally use inspect_mfa here,
# but using custom textgrid import instead so that the tone tier
# in the Taiwanese Mandarin textgrids can also be imported
parser = pgio.inspect_textgrid(corpus_root)
# for some reason, we get errors if the parser doesn't have a name...
# so polite!
parser.name = "friendly textgrid parser"
# we need this so that each speaker is parsed separately
parser.speaker_parser = DirectorySpeakerParser()
# this enables the parser to read the tone tier
parser.annotation_tiers[2].type_property = True

# for verbose output during corpus import:
parser.call_back = print

# uncomment this if reimporting data
# with CorpusContext('taiwanese_mandarin') as c:
#     c.reset()

# importing data
with CorpusContext('taiwanese_mandarin') as c:
    c.load(parser, corpus_root)

# checking if everything is as it should be
# speakers, files, list of phones
with CorpusContext('taiwanese_mandarin') as c:
    print('Speakers:', c.speakers)
    print('Discourses:', c.discourses)

    q = c.query_lexicon(c.lexicon_phone)
    q = q.order_by(c.lexicon_phone.label)
    q = q.columns(c.lexicon_phone.label.column_name('phone'))
    results = q.all()
    print(results)

###
### corpus enrichment
###

# here is the set of non-phone labels
pause_labels = ['<SIL>','<sil>','sp','','sil','spn']

# we get the vowel labels by finding all phones with tones
with CorpusContext('taiwanese_mandarin') as c:
    q = c.query_graph(c.phone)
    q = q.filter(c.phone.tones != "NULL")
    q = q.group_by(c.phone.label.column_name('phone'))
    q = q.aggregate(Count().column_name('count'))
    vowels = [x['phone'] for x in q]

# we encode vowels as a phone subset
with CorpusContext('taiwanese_mandarin') as c:
    c.encode_type_subset('phone', vowels, 'vowel')

# we encode a new phone property that tells us
# if the phone is a vowel / consonant / pause
with CorpusContext('taiwanese_mandarin') as c:
    q = c.query_graph(c.phone)
    q.set_properties(segtype='consonant')

with CorpusContext('taiwanese_mandarin') as c:
    q = c.query_graph(c.phone)
    q = q.filter(c.phone.label.in_(vowels))
    q.set_properties(segtype='vowel')

with CorpusContext('taiwanese_mandarin') as c:
    q = c.query_graph(c.phone)
    q = q.filter(c.phone.label.in_(pause_labels))
    q.set_properties(segtype='pause')

# we now encode pauses & utterances
with CorpusContext('taiwanese_mandarin') as c:
    c.encode_pauses(pause_labels)
    c.encode_utterances(min_pause_length=0.15)

# we now encode syllabels
with CorpusContext('taiwanese_mandarin') as c:
    c.encode_syllables(syllabic_label='vowel')

# we now encode speech rate (syllables/sec within an utterance)
with CorpusContext('taiwanese_mandarin') as c:
    c.encode_rate('utterance', 'syllable', 'speech_rate')

# we now encode various counts of smaller units
# within larger units as properties of the larger
# units
print("Encoding counts")
with CorpusContext('taiwanese_mandarin') as c:
    c.encode_count('word', 'syllable', 'num_syllables_word')
    c.encode_count('utterance', 'syllable', 'num_syllables_uttr')
    c.encode_count('syllable', 'phone', 'num_phones_syll')
    c.encode_count('word', 'phone', 'num_phones_word')
    c.encode_count('utterance', 'word', 'num_words_uttr')

# we now encode speaker demographic info
with CorpusContext('taiwanese_mandarin') as c:
    c.enrich_speakers_from_csv(speaker_csv_path)


# for the current project, we don't need anything else!
# some notes here on further things to do in the future:

# formant measurements: to be filled in; strategy:
    # (1) automatically calculated prototypes with pgdb
    # (2) further filtering in R, manual prototypes
    # (3) a further round of f measurements with R-based prototypes
# (also, we want full tracks on the second go!)

# for refined measurements
#with CorpusContext('taiwanese_mandarin') as c:
#    c.config.praat_path = "/Applications/Praat.app/Contents/MacOS/Praat"
#    analyze_formant_points_refinement(c, 
#        vowel_prototypes_path="/Users/soskuthy/Documents/Research/data/xling-corpus/mandarin_processing/taiwanese_mandarin_prototypes.csv"
#    )

# for refined formant tracks
#with CorpusContext('taiwanese_mandarin') as c:
#    c.config.praat_path = "/Applications/Praat.app/Contents/MacOS/Praat"
#    analyze_formant_points_refinement(c,
#        output_tracks=True, 
#        vowel_prototypes_path="/Users/soskuthy/Documents/Research/data/xling-corpus/mandarin_processing/taiwanese_mandarin_prototypes.csv"
#    )





