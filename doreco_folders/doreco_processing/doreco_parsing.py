#from polyglotdb.io.parsers.aligner import AlignerParser
from polyglotdb.io.parsers.textgrid import TextgridParser
from polyglotdb.exceptions import TextGridError
from polyglotdb.io.parsers.speaker import SpeakerParser
from polyglotdb.io.discoursedata import DiscourseData
from polyglotdb.structure import Hierarchy
from polyglotdb.io.types.parsing import OrthographyTier

import os
from polyglotdb.io.enrichment.helper import parse_file
from polyglotdb.io.helper import find_wav_path

def inspect_doreco(path, speaker_name_csv_path, file_name_prefix=None):
    """
    Generate an :class:`DorecoParser`
    for a specified text file for parsing it as a Doreco file

    Parameters
    ----------
    path : str
        Full path to text file
    speaker_name_csv_path : str
        Path to CSV file containing speaker names
    file_name_prefix : str
        Substring to exclude from the left of TextGrid file names, set to None to get the full file name

    Returns
    -------
    :class:`DorecoParser`
        Parser for DoReCo
    """
    annotation_types = [OrthographyTier(DorecoParser.uttr_label, 'utterance'),
                        OrthographyTier(DorecoParser.word_label, 'word'),
                        OrthographyTier(DorecoParser.phone_label, 'phone')]

    annotation_types[0].label = True
    annotation_types[1].label = True
    annotation_types[2].label = True
    hierarchy = Hierarchy({'phone': 'word', 'word': 'utterance', 'utterance': None})

    return DorecoParser(annotation_types, hierarchy, speaker_name_csv_path, file_name_prefix)


class DorecoParser(TextgridParser):
    """
    Parser for TextGrids in the DoReCo corpus collection..

    Parameters
    ----------
    annotation_tiers : list
        List of the annotation tiers to store data from the TextGrid
    hierarchy : Hierarchy
        Basic hierarchy of the TextGrid
    speaker_name_csv_path : str
        Path to CSV file containing speaker names
    file_name_prefix : str
        Substring to exclude from the left of TextGrid file names, set to None to get the full file name
    make_transcription : bool
        Flag for whether to add a transcription property to words based on phones they contain
    stop_check : callable
        Function to check for whether parsing should stop
    call_back : callable
        Function to report progress in parsing

    Attributes
    ----------
    word_label : str
        Label identifying word tiers
    phone_label : str
        Label identifying phone tiers
    uttr_label : str
        Label identifying utterance tiers
    split_char : str
        Character separating labels from speaker names in tier names
    name : str
        Name of the collection the TextGrids are from
    """
    uttr_label = 'tx'
    word_label = 'wd'
    phone_label = 'ph'
    split_char = '@'
    name = 'DoReCo'

    def __init__(self, annotation_tiers, hierarchy,
                 speaker_name_csv_path, file_name_prefix=None,
                 make_transcription=True,
                 stop_check=None, call_back=None):
        super(DorecoParser, self).__init__(annotation_tiers, hierarchy, make_transcription,
                                           stop_check, call_back)
        self.speaker_parser = DorecoCSVSpeakerParser(speaker_name_csv_path, file_name_prefix=file_name_prefix)

    def _is_valid(self, tg, speaker_names, error_message = False):
        found_word = False
        found_phone = False
        found_uttr = False
        invalid = True
        speakers = set(speaker_names)
        #print("SPEAKERS:",speakers)
        found_words = {x: False for x in speakers}
        found_phones = {x: False for x in speakers}
        found_uttrs = {x: False for x in speakers}
        for i, tier_name in enumerate(tg.tierNames):
            #print("TIER NAME:",tier_name)
            if self.split_char not in tier_name:
                #print("No split character found. Continuing...")
                continue
            name, speaker = tier_name.split(self.split_char)
            speaker = speaker.strip().replace('/', '_').replace('\\', '_')
            name = name.strip()
            #print("NAME:",name,"SPEAKER:",speaker)
            if name.lower().startswith(self.uttr_label):
                found_uttrs[speaker] = True
            elif name.lower().startswith(self.word_label):
                found_words[speaker] = True
            elif name.lower().startswith(self.phone_label):
                found_phones[speaker] = True

        if error_message:
            error_text = ''
            for speaker in speakers:
                if not found_uttrs[speaker]:
                    error_text += "\nCould not find utterances for speaker "+speaker
                elif not found_words[speaker]:
                    error_text += "\nCould not find words for speaker "+speaker
                elif not found_phones[speaker]:
                    error_text += "\nCould not find phones for speaker "+speaker

        found_uttr = all(found_uttrs.values())
        found_word = all(found_words.values())
        found_phone = all(found_phones.values())
        if not error_message:
            return found_uttr and found_word and found_phone
        elif error_message:
            return error_text


    def parse_discourse(self, path, types_only=False):
        """
        Parse a TextGrid file for later importing.

        Parameters
        ----------
        path : str
            Path to TextGrid file
        types_only : bool
            Flag for whether to only save type information, ignoring the token information

        Returns
        -------
        :class:`~polyglotdb.io.discoursedata.DiscourseData`
            Parsed data from the file
        """

        tg = self.load_textgrid(path)
        speaker_names = self.speaker_parser.parse_path(path)
        is_valid = self._is_valid(tg,speaker_names)

        if not is_valid:
            raise (TextGridError('This file ({}) cannot be parsed by the {} parser.{}'.format(path, self.name,self._is_valid(tg,speaker_names,error_message=True))))
        name = os.path.splitext(os.path.split(path)[1])[0]


        dummy = self.annotation_tiers
        self.annotation_tiers = []

        # Parse the tiers
        for i, tier_name in enumerate(tg.tierNames):
            ti = tg.getTier(tier_name)
            try:
                type, speaker = tier_name.split(self.split_char)
                speaker = speaker.strip().replace('/', '_').replace('\\', '_')
                assert(speaker in speaker_names)
            except ValueError:
                continue
            except AssertionError:
                continue
            if type.lower().startswith(self.uttr_label):
                type = 'utterance'
            elif type.lower().startswith(self.word_label):
                type = 'word'
            elif type.lower().startswith(self.phone_label):
                type = 'phone'
            if len(ti.entries) == 1 and ti.entries[0][2].strip() == '':
                continue
            at = OrthographyTier(type, type)
            at.speaker = speaker
            at.add(( (text.strip(), begin, end) for (begin, end, text) in ti.entries))
            self.annotation_tiers.append(at)
        pg_annotations = self._parse_annotations(types_only)
        data = DiscourseData(name, pg_annotations, self.hierarchy)

        self.annotation_tiers = dummy

        data.wav_path = find_wav_path(path)
        return data


class DorecoCSVSpeakerParser(SpeakerParser):
    """
    Class for parsing a speaker name from a file path and a CSV file that looks up the speaker name
    corresponding to the file name from the CSV file

    Parameters
    ----------
    csv_path : str
        Path to CSV file
    file_name_prefix : str
        Substring to exclude from the left of the file name, set to None to get the full file name

    Attributes
    ----------
    file_name_col : str
        Header of the column in the CSV containing the file name
    speaker_col : str
        Header of the column in the CSV containing the speaker
    split_char : str
        Character separating speaker names
    """
    file_name_col = 'name'
    speaker_col = 'spk_code'
    split_char = '/'

    def __init__(self, csv_path, file_name_prefix=None):
        self.file_name_prefix = file_name_prefix
        self.csv_path = csv_path

    def parse_path(self, path):
        """
        Parses a file path and returns a list of speakers names

        Parameters
        ----------
        path : str
            file path

        Returns
        -------
        speakers : list:str
            list of speaker names corresponding to the file name in the csv file
        """
        file_name = os.path.basename(path)
        file_name, ext = os.path.splitext(file_name)

        if not self.file_name_prefix:
            discourse_name = file_name
        else:
            discourse_name = file_name.replace(self.file_name_prefix,"")
        
        csv_data, csv_type_data = parse_file(self.csv_path, labels=[discourse_name])

        speakers = csv_data[discourse_name][self.speaker_col]
        speakers = str(speakers)
        speakers = speakers.split(self.split_char)

        return speakers
        

