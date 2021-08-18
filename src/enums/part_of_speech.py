from enum import Enum


class PartOfSpeech(Enum):
    Unknown = 0
    Adjective= 1
    Adposition = 2
    Adverb = 3
    Conjunction = 4
    Determiner = 5
    Noun = 6
    Numeral = 7
    Particle = 8
    Pronoun = 9
    Verb = 10

    @staticmethod
    def from_str(label):
        if label == 'ADJ':
            return PartOfSpeech.Adjective
        elif label == 'ADP':
            return PartOfSpeech.Adposition
        elif label == 'ADV':
            return PartOfSpeech.Adverb
        elif label == 'CONJ':
            return PartOfSpeech.Conjunction
        elif label == 'DET':
            return PartOfSpeech.Determiner
        elif label == 'NOUN':
            return PartOfSpeech.Noun
        elif label == 'NUM':
            return PartOfSpeech.Numeral
        elif label == 'PRT':
            return PartOfSpeech.Particle
        elif label == 'PRON':
            return PartOfSpeech.Pronoun
        elif label == 'VERB':
            return PartOfSpeech.Verb
        else:
            return PartOfSpeech.Unknown