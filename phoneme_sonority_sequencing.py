from utils import name_each_letter
from utils import check_for_samoglasno_r

phoneme_weights = {
    'А': 12,
    'Б': 2,
    'В': 2,
    'Г': 2,
    'Д': 2,
    'Ѓ': 2,
    'Е': 12,
    'Ж': 2,
    'З': 2,
    "Ѕ": 2,
    'И': 12,
    'Ј': 3,
    'К': 1,
    'Л': 3,
    'Љ': 3,
    'М': 3,
    'Н': 3,
    'Њ': 3,
    'О': 12,
    'П': 1,
    'Р': 5,
    'С': 1,
    'Т': 1,
    'Ќ': 1,
    'У': 12,
    'Ф': 1,
    'Х': 1,
    'Ц': 1,
    'Ч': 1,
    'Џ': 2,
    'Ш': 1,
    'F': 0,
    'S': 0,
    "'": 0,
    "`": 0,
}


def check_for_two_continuous_vowels_2(letters_dict):
    check = False
    position = -1
    for i in range(len(letters_dict) - 1):
        type_letter_1 = letters_dict[i][1]
        type_letter_2 = letters_dict[i + 1][1]
        if type_letter_1 == type_letter_2 == 'vowel':
            check = True
            position = i + 1
    return check, position


def append_special_characters(word, letters_dict):
    check, position = check_for_two_continuous_vowels_2(letters_dict)
    if check:
        word = ''.join(word[:position]) + 'F' + ''.join(word[position:])
    return 'S' + word + 'S'


def phoneme_sonority(word, weights):
    letters = list(word)
    letter_weights = []
    for letter in letters:
        letter_weights.append(weights[letter.upper()])
    return letter_weights


def triplet_differences(weights):
    differences = []
    for i in range(1, len(weights) - 1):
        curr = weights[i]
        previous = weights[i - 1]
        successor = weights[i + 1]
        difference = curr - previous - successor
        differences.append(difference)
    return differences


def sonority_differences(weights):
    differences = [0]
    for i in range(1, len(weights) - 1):
        curr_weight = weights[i]
        previous_sonority_diff = differences[i - 1]
        difference = curr_weight - previous_sonority_diff
        differences.append(difference)
    differences.append(0)
    return differences


def find_position_of_vowels_in_triplets(triplet_difference):
    temp_list = [0]
    temp_list.extend(triplet_difference)
    temp_list.append(0)
    return [i for i, element in enumerate(temp_list) if element > 0]


# longest strictly monotonic decreasing sequence
def lsmds(arr, triplet_difference):
    new_list = [0] * len(arr)
    if triplet_difference:
        for i in range(len(arr) - 1):
            if arr[i] > arr[i + 1]:
                new_list[i] = True
            else:
                new_list[i] = False
        if triplet_difference[-1] > 0:
            new_list[-1] = True
        else:
            new_list[-1] = False
    return new_list


def find_position_of_true(true_false_list):
    return [i for i, element in enumerate(true_false_list) if element]


def split_positions_of_false(tmp, positions_of_true):
    split_positions = []
    for t in range(len(positions_of_true) - 1):
        curr = positions_of_true[t]
        following = positions_of_true[t + 1]
        sub_list = tmp[curr:following]
        if sub_list.count(False) == 1:
            split_positions.append(following - 1)
        elif sub_list.count(False) >= 2:
            split_positions.append(curr + 2)

    return split_positions


def remove_special_characters(syllables):
    for i in range(len(syllables)):
        syll = syllables[i]
        syll = syll.replace('S', '')
        syll = syll.replace('F', '')
        syllables[i] = syll
    return syllables


def find_clusters(word):
    letters = list(word)
    letters_dict = name_each_letter(letters)
    letters_dict = check_for_samoglasno_r(letters_dict)
    word = append_special_characters(word, letters_dict)

    word_weights = phoneme_sonority(word, phoneme_weights)
    triplet_difference = triplet_differences(word_weights)

    decreasing_sequences = lsmds(word_weights[:-1], triplet_difference)
    positions_of_true = find_position_of_true(decreasing_sequences)
    positions = split_positions_of_false(decreasing_sequences, positions_of_true)

    # multi-syllable words, prefixes or suffixes
    if positions:
        syllables = [word[0:positions[0]]]
        for i in range(len(positions) - 1):
            syllables.append(word[positions[i]: positions[i + 1]])
        syllables.append(word[positions[-1]:])

    # one syllable word, prefix, or suffix
    else:
        syllables = [word]

    syllables = remove_special_characters(syllables)

    return syllables


def add_hyphen(list_of_syllables):
    syllables = '-'.join(list_of_syllables)
    syllables = syllables.strip('-')
    return syllables


def phoneme_SSP(word):
    clusters = find_clusters(word)
    hyphened_string = add_hyphen(clusters)
    return hyphened_string


class PhonemeSonoritySequencing:

    @staticmethod
    def word_to_phoneme_SSP(word):
        return phoneme_SSP(word)
