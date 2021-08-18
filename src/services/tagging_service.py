from typing import List
from enums.part_of_speech import PartOfSpeech
import nltk

class TaggingService:
    def __init__(self):
        self._download_nltk_resources()
        pass

    def get_part_of_speech_tag(self, word: str) -> PartOfSpeech:
        """Get the Part-of-Speech tag for a given `word`

        :param word: The word to be tagged
        :type word: str
        :return: Tag enum value
        :rtype: PartOfSpeech
        """
        pos_tags = nltk.pos_tag([word], tagset='universal')
        pos_tag = PartOfSpeech.from_str(pos_tags[0][1])
        return pos_tag

    def word_is_specific_tag(self, word:str, pos_tags: List[PartOfSpeech]) -> bool:
        """Validate if a word is part of a list of specific Part-of-Speech tags

        :param word: The word to be validated
        :type word: str
        :param pos_tags: List of PartOfSpeech enum values
        :type pos_tags: List[PartOfSpeech]
        :return: Whether the word tag is in the given list of values
        :rtype: bool
        """
        if pos_tags is None or len(pos_tags) == 0:
            return False

        if self.get_part_of_speech_tag(word) in pos_tags:
            return True

        return False

    def _download_nltk_resources(self):
        self._download_nltk_resource('universal_tagset')

    def _download_nltk_resource(self, resource_name):
        try:
            nltk.data.find(f'taggers/{resource_name}')
        except LookupError:
            nltk.download(resource_name)