from syllabels import SplitIntoSyllables
from phoneme_sonority_sequencing import PhonemeSonoritySequencing
from morpheme_sonority_sequencing import MorphemeSonoritySequencing
import pandas as pd
import pickle as p

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    splitter = SplitIntoSyllables()
    splitter.hyphenate("предодреден")

    phoneme_SSP_splitter = PhonemeSonoritySequencing()
    phoneme_SSP_splitter.word_to_phoneme_SSP('противавионски')

    morpheme_SSP_splitter = MorphemeSonoritySequencing()
    morpheme_SSP_splitter.word_to_morpheme_SSP('противавионски')







