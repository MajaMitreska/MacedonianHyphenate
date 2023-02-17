import nltk
import pickle as p
import math
import pandas as pd
from collections import deque
import re
import itertools

consonants = ['б', 'в', 'г', 'д', 'ѓ', 'ж', 'з', 'ѕ', 'ј', 'к', 'л', 'љ', 'м', 'н', 'њ', 'п', 'р', 'с', 'т', 'ќ', 'ф',
              'х', 'ц', 'ч', 'џ', 'ш']
vowels = ['а', 'е', 'и', 'о', 'у']

"""# Functions"""


def is_vowel(letter):
    return letter.lower() in vowels


def is_const(letter):
    return letter.lower() in consonants


def name_each_letter(list_of_letters):
    letters_dict = []
    for letter in list_of_letters:
        if is_vowel(letter):
            letters_dict.append((letter, 'vowel'))
        elif is_const(letter):
            letters_dict.append((letter, 'consonant'))
        else:
            letters_dict.append((letter, 'consonant'))
    return letters_dict


def check_for_samoglasno_r(letters_dict):
    for i in range(len(letters_dict) - 1):
        letter = letters_dict[i][0]
        # r between two consonants
        if letter == 'р' and letters_dict[i - 1][1] == 'consonant' and letters_dict[i + 1][1] == 'consonant':
            letters_dict[i] = (letter, 'vowel')
        # r at the end of the word ex: tembr
        elif i == (len(letters_dict) - 2) and letters_dict[i + 1][0] == 'р' and letters_dict[i][1] == 'consonant' and \
                letters_dict[i - 1][1] == 'consonant':
            letters_dict[i + 1] = (letters_dict[i + 1][0], 'vowel')
        # r at the end of the word ex: zanr, obr
        elif i == (len(letters_dict) - 2) and letters_dict[i + 1][0] == 'р' and letters_dict[i][
            1] == 'consonant' and letter in ['н', 'б']:
            letters_dict[i + 1] = (letters_dict[i + 1][0], 'consonant')
        # r at the end of the word
        elif i == (len(letters_dict) - 2) and letters_dict[i + 1][0] == 'р' and letters_dict[i][1] == 'consonant':
            letters_dict[i + 1] = (letters_dict[i + 1][0], 'vowel')
    return letters_dict


def count_vowels(letters_dict):
    number_of_vowels = 0
    for t in letters_dict:
        if t[1] == 'vowel':
            number_of_vowels += 1
    return number_of_vowels


def find_position_of_vowels_in_dictionary(letters_dict):
    positions_dict = {}
    for num, t in enumerate(letters_dict):
        if t[1] == 'vowel':
            positions_dict[num] = t[0]
    return positions_dict


def check_for_two_continuous_vowels(letters_dict):
    check = False
    for i in range(len(letters_dict) - 1):
        type_letter_1 = letters_dict[i][1]
        type_letter_2 = letters_dict[i + 1][1]
        if type_letter_1 == type_letter_2 == 'vowel':
            check = True
    return check


def check_for_two_continuous_vowels_2(letters_dict):
    check = False
    positions = []
    for i in range(len(letters_dict) - 1):
        type_letter_1 = letters_dict[i][1]
        type_letter_2 = letters_dict[i + 1][1]
        if type_letter_1 == type_letter_2 == 'vowel':
            check = True
            positions.append(i + len(positions) + 1)
    return check, positions


def letters_to_pop(letters, letters_queue, syllabels, position, increment):
    j = 0
    if len(letters) == len(letters_queue):
        range_to_pop = position + increment
    else:
        range_to_pop = len(letters_queue) + position + increment - len(letters)
    while j < range_to_pop:
        syllabels.append(letters_queue.popleft())
        j += 1
    syllabels.append('-')

    return letters_queue, syllabels


def split_into_syllables(word):
    letters = list(word)
    letters_dict = name_each_letter(letters)
    letters_dict = check_for_samoglasno_r(letters_dict)
    number_of_vowels = count_vowels(letters_dict)
    position_of_vowels = list(find_position_of_vowels_in_dictionary(letters_dict).keys())
    position_of_vowels.sort()
    two_vowels = check_for_two_continuous_vowels(letters_dict)
    checking_number_of_vowels = number_of_vowels

    syllables = []
    letters_queue = deque(letters)

    for position in position_of_vowels:

        """ find the appropriate range to iterate the letters """
        if len(letters) <= 4 and two_vowels:
            len_letters = len(letters) - 1
        elif two_vowels:
            len_letters = len(letters)
        else:
            len_letters = len(letters) - 2

        for i in range(len_letters):

            if i == position:

                if checking_number_of_vowels == 1:
                    break
                checking_number_of_vowels -= 1

                #     First case: VCV -> V-CV
                if letters_dict[i + 1][1] == 'consonant' and letters_dict[i + 2][1] == 'vowel':
                    letters_queue, syllables = letters_to_pop(letters, letters_queue, syllables, position, 1)

                #     Second case: VCC -> VC-C
                elif letters_dict[i + 1][1] == 'consonant' and letters_dict[i + 2][1] == 'consonant':
                    letters_queue, syllables = letters_to_pop(letters, letters_queue, syllables, position, 2)

                #     Third case: VV -> V-V
                elif letters_dict[i][1] == 'vowel' and letters_dict[i + 1][1] == 'vowel':
                    letters_queue, syllables = letters_to_pop(letters, letters_queue, syllables, position, 1)

    """If the remainder of the word does not contain vowels just add it to the list"""
    if len(syllables) < len(letters) + number_of_vowels - 1:
        while letters_queue:
            syllables.append(letters_queue.popleft())

    return syllables


# 'r','i','-','b','a' = ri-ba
def hyphenate_syllables(syllables):
    print_string = ''.join(syllables)
    return print_string


def split_by_suffix(word, suffix):
    position = word.find(suffix)
    start = position
    end = len(suffix)
    return [word[0:start], word[start:start + end], word[start + end:]]


def check_for_two_suffixes(word, suffixes):
    pairs = list(itertools.combinations(suffixes, 2))
    for pair in pairs:
        if all(x in word for x in pair):
            return True, pair
    return False, tuple()


def check_for_ski_stvo_stven(word, type=['morpheme', 'all']):
    suffixes = ['што', 'ски', 'ство', 'ствен']
    two_suffixes, pair = check_for_two_suffixes(word, suffixes)
    for suffix in suffixes:
        if (suffix == 'ски' and suffix in word) or (suffix == 'ство' and suffix in word):
            return split_by_suffix(word, suffix)
        if suffix == 'ствен' and suffix in word:
            if type == 'morpheme': return split_by_suffix(word, suffix)
            if type == 'all': return [split_by_suffix(word, suffix), [word]]
        if (suffix == 'што' and suffix in word) and two_suffixes:
            split_string = split_by_suffix(word, suffix)
            second_suffix = pair[1 - pair.index('што')]
            modified_string = split_string[:-1]
            modified_string.extend(split_by_suffix(split_string[-1], second_suffix))
            return [modified_string, split_by_suffix(word, second_suffix)]
        if suffix == 'што' and suffix in word:
            return [split_by_suffix(word, suffix), [word]]


def check_for_prefixes(word, prefixes):
    for prefix in prefixes:
        two_syllable_prefix = False
        if word.startswith(prefix):
            letters_dict = name_each_letter(list(prefix))
            letters_dict = check_for_samoglasno_r(letters_dict)
            number_of_vowels = count_vowels(letters_dict)
            len_prefix = len(prefix)
            if number_of_vowels >= 2:
                two_syllable_prefix = True
                syllables = hyphenate_syllables(split_into_syllables(prefix))
                return [syllables, word[len_prefix:]], two_syllable_prefix
            else:
                return [word[0:len_prefix], word[len_prefix:]], two_syllable_prefix


# def check_for_exceptions_2(word):
#     prefiksi = (
#         'ис', 'против', 'пред', 'прет', 'пре', 'над', 'нај', 'над', 'нат', 'на', 'не', 'ни', 'обез', 'по', 'се', 'пре',
#         'из', 'до', 'баш', 'без', 'бес', 'благо', 'бе', 'високо', 'вон', 'едно', 'жолто', 'за', 'зат', 'зелено', 'едно',
#         'зад', 'казнено', 'кусо', 'меѓу', 'многу', 'обес', 'оловно', 'пет', 'повеќе', 'подиз', 'под', 'пот', 'поизна',
#         'поиз', 'полу', 'поне', 'пораз', 'порас', 'прaво', 'прво', 'прa', 'при', 'про', 'разно', 'раз', 'рас', 'рамно',
#         'само', 'светло', 'себе', 'сино', 'ситно', 'сребро', 'слабо', 'танко', 'тенко', 'темно', 'три', 'триста',
#         'широко')
#     sufiksi = ('ски', 'ство', 'ствен', 'што')
#     has_prefiks = any(word.startswith(p) for p in prefiksi)
#     has_sufiks = any(s in word for s in sufiksi)
#
#     divided_strings = []
#
#     # prefiksi
#     if word.startswith(prefiksi):
#
#         prefiksi_divided_strings, two_syllabel_prefix = check_for_prefiksi(word, prefiksi)
#         if not two_syllabel_prefix:
#             divided_strings.append([word])
#
#         prefiks = prefiksi_divided_strings[0]
#         prefiksi_divided_strings.pop(0)
#
#         for substring in prefiksi_divided_strings:
#             if any(s in substring for s in sufiksi):
#                 sufiksi_divided_strings = check_for_ski_stvo_stven(substring, 'all')
#                 two_versions = all(isinstance(n, list) for n in sufiksi_divided_strings)
#                 if two_versions:
#                     for sufiksi_substring in sufiksi_divided_strings:
#                         prefiks_sufiksi_substring = [prefiks]
#                         prefiks_sufiksi_substring.extend(sufiksi_substring)
#                         divided_strings.append(prefiks_sufiksi_substring)
#                 else:
#                     prefiks_sufiksi_substring = [prefiks]
#                     prefiks_sufiksi_substring.extend(prefiksi_divided_strings)
#                     divided_strings.append(prefiks_sufiksi_substring)
#
#             else:
#                 prefiks_sufiksi_substring = [prefiks]
#                 prefiks_sufiksi_substring.extend(prefiksi_divided_strings)
#                 divided_strings.append(prefiks_sufiksi_substring)
#
#     # sufiksi
#     if has_sufiks:
#         sufiksi_divided_strings = check_for_ski_stvo_stven(word, 'all')
#         temp_sufiks = []
#         for sufiksi_substring in sufiksi_divided_strings:
#             temp_sufiks.append(sufiksi_substring)
#         if all(isinstance(n, list) for n in sufiksi_divided_strings):
#             divided_strings.extend(temp_sufiks)
#         else:
#             divided_strings.append(temp_sufiks)
#
#     # nema ni prefiksi i sufiksi
#     if (not has_sufiks) and (not has_prefiks):
#         divided_strings.append(word)
#
#     two_versions = all(isinstance(n, list) for n in divided_strings)
#     versions = []
#     hyphenate_string = ''
#
#     if two_versions:
#         for version in divided_strings:
#             hyphenate_string = ''
#             for substring in version:
#                 hyphenate_string += hyphenate_syllabels(split_into_syllables(substring)) + '-'
#             versions.append(hyphenate_string)
#     else:
#         for substring in divided_strings:
#             hyphenate_string += hyphenate_syllabels(split_into_syllables(substring)) + '-'
#         versions.append(hyphenate_string)
#
#     for i in range(len(versions)):
#         v = versions[i]
#         hyphenate_string = v.strip('-')
#         hyphenate_string = re.sub('--', '-', hyphenate_string)
#         versions[i] = hyphenate_string
#
#     return set(versions)

def iterate_strings(prefix, string, divided_strings):
    prefiks_sufiksi_substring = [prefix]
    prefiks_sufiksi_substring.extend(string)
    divided_strings.append(prefiks_sufiksi_substring)
    return divided_strings


def check_for_multiple_versions(syll_list):
    return all(isinstance(n, list) for n in syll_list)


def merging_syllables(string):
    hyphenate_string = ''
    for substring in string:
        hyphenate_string += hyphenate_syllables(split_into_syllables(substring)) + '-'
    return hyphenate_string


def clean_output(lists):
    for i in range(len(lists)):
        v = lists[i]
        hyphenate_string = v.strip('-')
        hyphenate_string = re.sub('--', '-', hyphenate_string)
        lists[i] = hyphenate_string
    return lists
