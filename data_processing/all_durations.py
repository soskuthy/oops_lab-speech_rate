import polyglotdb 
from polyglotdb import CorpusContext

with CorpusContext('taiwanese_mandarin') as c:
    q = c.query_graph(c.phone)
    q = q.columns(c.phone.speaker.name.column_name('speaker'),
                  c.phone.speaker.gender.column_name('sex'),
                  c.phone.speaker.age.column_name('age'),
                  c.phone.discourse.name.column_name('file'),
                  c.phone.utterance.id.column_name('uttr_id'),
                  c.phone.utterance.speech_rate.column_name('speech_rate'),
                  c.phone.utterance.speech_rate_phone.column_name('speech_rate_phone'),
                  c.phone.utterance.num_words_uttr.column_name('num_words_uttr'),
                  c.phone.utterance.num_syllables_uttr.column_name('num_syllables_uttr'),
                  c.phone.utterance.begin.column_name('uttr_start'),
                  c.phone.utterance.end.column_name('uttr_end'),
                  c.phone.utterance.duration.column_name('uttr_dur'),
                  c.phone.word.label.column_name('word'),
                  c.phone.word.num_phones_word.column_name('num_phones_word'),
                  c.phone.word.num_syllables_word.column_name('num_syllables_word'),
                  c.phone.word.begin.column_name('word_start'),
                  c.phone.word.end.column_name('word_end'),
                  c.phone.word.duration.column_name('word_dur'),
                  c.phone.label.column_name('phone'),
                  c.phone.previous.label.column_name('previous'),
                  c.phone.following.label.column_name('following'),
                  c.phone.segtype.column_name('segment_type'),
                  c.phone.begin.column_name('phone_start'), 
                  c.phone.end.column_name('phone_end'),
                  c.phone.duration.column_name('phone_dur')
    )
    results = q.all()
    q.to_csv('/Users/soskuthy/Documents/Research/current/2021/oops_lab-speech_rate/oops_lab-speech_rate/data/taiwanese_mandarin_durations.csv')

with CorpusContext('korean') as c:
    q = c.query_graph(c.phone)
    q = q.columns(c.phone.speaker.name.column_name('speaker'),
                  c.phone.speaker.gender.column_name('sex'),
                  c.phone.speaker.age.column_name('age'),
                  c.phone.discourse.name.column_name('file'),
                  c.phone.utterance.id.column_name('uttr_id'),
                  c.phone.utterance.speech_rate.column_name('speech_rate'),
                  c.phone.utterance.speech_rate_phone.column_name('speech_rate_phone'),
                  c.phone.utterance.num_words_uttr.column_name('num_words_uttr'),
                  c.phone.utterance.num_syllables_uttr.column_name('num_syllables_uttr'),
                  c.phone.utterance.begin.column_name('uttr_start'),
                  c.phone.utterance.end.column_name('uttr_end'),
                  c.phone.utterance.duration.column_name('uttr_dur'),
                  c.phone.word.label.column_name('word'),
                  c.phone.word.num_phones_word.column_name('num_phones_word'),
                  c.phone.word.num_syllables_word.column_name('num_syllables_word'),
                  c.phone.word.begin.column_name('word_start'),
                  c.phone.word.end.column_name('word_end'),
                  c.phone.word.duration.column_name('word_dur'),
                  c.phone.label.column_name('phone'),
                  c.phone.previous.label.column_name('previous'),
                  c.phone.following.label.column_name('following'),
                  c.phone.segtype.column_name('segment_type'),
                  c.phone.begin.column_name('phone_start'), 
                  c.phone.end.column_name('phone_end'),
                  c.phone.duration.column_name('phone_dur')
    )
    results = q.all()
    q.to_csv('/Users/soskuthy/Documents/Research/current/2021/oops_lab-speech_rate/oops_lab-speech_rate/data/korean_durations.csv')

with CorpusContext('kapampangan') as c:
    q = c.query_graph(c.phone)
    q = q.columns(c.phone.speaker.name.column_name('speaker'),
                  c.phone.speaker.gender.column_name('sex'),
                  c.phone.speaker.age.column_name('age'),
                  c.phone.discourse.name.column_name('file'),
                  c.phone.utterance.id.column_name('uttr_id'),
                  c.phone.utterance.speech_rate.column_name('speech_rate'),
                  c.phone.utterance.speech_rate_phone.column_name('speech_rate_phone'),
                  c.phone.utterance.num_words_uttr.column_name('num_words_uttr'),
                  c.phone.utterance.num_syllables_uttr.column_name('num_syllables_uttr'),
                  c.phone.utterance.begin.column_name('uttr_start'),
                  c.phone.utterance.end.column_name('uttr_end'),
                  c.phone.utterance.duration.column_name('uttr_dur'),
                  c.phone.word.label.column_name('word'),
                  c.phone.word.num_phones_word.column_name('num_phones_word'),
                  c.phone.word.num_syllables_word.column_name('num_syllables_word'),
                  c.phone.word.begin.column_name('word_start'),
                  c.phone.word.end.column_name('word_end'),
                  c.phone.word.duration.column_name('word_dur'),
                  c.phone.label.column_name('phone'),
                  c.phone.previous.label.column_name('previous'),
                  c.phone.following.label.column_name('following'),
                  c.phone.segtype.column_name('segment_type'),
                  c.phone.begin.column_name('phone_start'), 
                  c.phone.end.column_name('phone_end'),
                  c.phone.duration.column_name('phone_dur')
    )
    results = q.all()
    q.to_csv('/Users/soskuthy/Documents/Research/current/2021/oops_lab-speech_rate/oops_lab-speech_rate/data/kapampangan_durations.csv')