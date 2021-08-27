import re

from typing import List


class StringProcessService:
    def __init__(self):
        self._charmap = {
            0x201c: u'"',
            0x201d: u'"',
            0x2018: u"'",
            0x2019: u"'",
            'ﬀ': u'ff',
            'ﬁ': u'fi',
            'ﬂ': u'fl',
            'ﬃ': u'ffi',
            'ﬄ': u'ffl',
            '″': u'"',
            '′': u"'",
            '„': u'"',
            '«': u'"',
            '»': u'"'
        }

        self._number_regex = '^(((([0-9]*)(\.|,)([0-9]+))+)|([0-9]+))'

    def convert_string_unicode_symbols(self, text: str) -> str:
        result = text.translate(self._charmap)
        return result

    def convert_strings_unicode_symbols(self, texts: List[str]) -> List[str]:
        result = [self.convert_string_unicode_symbols(x) for x in texts]
        return result

    def replace_string_numbers(self, text: str) -> str:
        result = re.sub(self._number_regex, '0', text)
        return result

    def replace_strings_numbers(self, texts: List[str]) -> List[str]:
        result = [self.replace_string_numbers(x) for x in texts]
        return result

    def remove_string_characters(self, text: str, characters: List[str]) -> str:
        result = text
        for character in characters:
            result = result.replace(character, '')

        return result

    def remove_strings_characters(self, texts: List[str], characters: List[str]) -> List[str]:
        result = [self.remove_string_characters(x, characters) for x in texts]
        return result

    def clean_up_words(self, words: List[str]) -> List[str]:
        result = [self._clean_up_word(x) for x in words]
        return result

    def _clean_up_word(self, word):
        '''
            This function cleans up the words before saving them as tokens.
            It only looks into the beginning or the end of the words, so if a word
            contains an invalid symbol inside this will not be cleaned.
        '''
        result = word.strip()

        invalid_chars = [',', '„', ':', '’', '.', ';', '=', '-', "'", '/', '\\', '(', ')', '[', ']', '{', '}', '-', '—', '_']
        for invalid_char in invalid_chars:
            # we clean recursively, so that if a word ends in :,' all three symbols will be removed
            if result.startswith(invalid_char):
                result = self._clean_up_word(result[1:])
            elif result.endswith(invalid_char):
                result = self._clean_up_word(result[:-1])

        return result
