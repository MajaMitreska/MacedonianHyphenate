from phoneme_sonority_sequencing import PhonemeSonoritySequencing
from morpheme_sonority_sequencing import MorphemeSonoritySequencing
from rule_based_morpheme_syllabification import RuleBasedMorphemeSyllabification
from rule_based_phoneme_syllabification import RuleBasedPhonemeSyllabification
from syllables import Syllables

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    word = "поопштословенскиот"

    phoneme_rule_based_splitter = RuleBasedPhonemeSyllabification()
    print(phoneme_rule_based_splitter.split(word))

    morpheme_rule_based_splitter = RuleBasedMorphemeSyllabification()
    print(morpheme_rule_based_splitter.split(word))

    phoneme_SSP_splitter = PhonemeSonoritySequencing()
    print(phoneme_SSP_splitter.word_to_phoneme_SSP(word))

    morpheme_SSP_splitter = MorphemeSonoritySequencing()
    print(morpheme_SSP_splitter.word_to_morpheme_SSP(word))

    print()

    syllables = Syllables()
    print(syllables.split(word))








