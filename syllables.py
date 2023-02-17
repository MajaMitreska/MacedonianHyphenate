from rule_based_phoneme_syllabification import phoneme_rule_based
from rule_based_morpheme_syllabification import morpheme_rule_based
from phoneme_sonority_sequencing import phoneme_SSP
from morpheme_sonority_sequencing import morpheme_SSP


def syllabification_dictionary(word):
    syllables_dict = dict()
    syllables_dict['Phoneme Rule-Based Syllables'] = "".join(phoneme_rule_based(word))
    syllables_dict['Morpheme Rule-Based Syllables'] = "".join(morpheme_rule_based(word))
    syllables_dict['Phoneme Sonority Syllables'] = phoneme_SSP(word)
    syllables_dict['Morpheme Sonority Syllables'] = morpheme_SSP(word)
    return syllables_dict


class Syllables:
    @staticmethod
    def split(word):
        return syllabification_dictionary(word)
