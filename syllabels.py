import itertools

import nltk

import pickle as p
import math
import pandas as pd
from collections import deque
import re

consonants = ['б', 'в', 'г', 'д', 'ѓ', 'ж', 'з', 'ѕ', 'ј', 'к', 'л', 'љ', 'м', 'н', 'њ', 'п', 'р', 'с', 'т', 'ќ', 'ф',
              'х', 'ц', 'ч', 'џ', 'ш']
vowels = ['а', 'е', 'и', 'о', 'у']


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
        type_of_letter = letters_dict[i][1]
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
        # L at the end of the word, but ends with rl, jl or fl
        elif i == (len(letters_dict) - 2) and letters_dict[i + 1][0] == 'л' and letters_dict[i][
            1] == 'consonant' and letter in ['р', 'ф', 'ј']:
            letters_dict[i + 1] = (letters_dict[i + 1][0], 'consonant')
        # L at the end of the word
        elif i == (len(letters_dict) - 2) and letters_dict[i + 1][0] == 'л' and letters_dict[i][1] == 'consonant':
            letters_dict[i + 1] = (letters_dict[i + 1][0], 'vowel')
    return letters_dict


def count_vowels(letters_dict):
    number_of_vowels = 0
    for t in letters_dict:
        if t[1] == 'vowel':
            number_of_vowels += 1
    return number_of_vowels


def find_position_of_vowels(letters_dict):
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
    letters_dict = name_each_letter(list(word))
    letters_dict = check_for_samoglasno_r(letters_dict)
    number_of_vowels = count_vowels(letters_dict)
    position_of_vowels = list(find_position_of_vowels(letters_dict).keys())
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

                #     Second sub-case: VCC -> V-CV agrikultura
                # elif letters_dict[i+1][1] == 'consonant' and letters_dict[i+2][1] == 'consonant' and position == 0:
                #  letters_queue, syllables = letters_to_pop(letters, letters_queue, syllables, position, 1)

                #     Second case: VCC -> VC-V
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


def split_by_sufiks(word, sufiks):
    position = word.find(sufiks)
    start = position
    end = len(sufiks)
    return [word[0:start], word[start:start + end], word[start + end:]]


def check_for_two_sufiksi(word, sufiksi):
    pairs = list(itertools.combinations(sufiksi, 2))
    for pair in pairs:
        if all(x in word for x in pair):
            return True, pair
    return False, tuple()


def check_for_ski_stvo_stven(word):
    sufiksi = ['што', 'ски', 'ство', 'ствен']
    two_sufiksi, pair = check_for_two_sufiksi(word, sufiksi)
    for sufiks in sufiksi:
        if (sufiks == 'ски' and sufiks in word) or (sufiks == 'ство' and sufiks in word):
            return split_by_sufiks(word, sufiks)
        if (sufiks == 'ствен' and sufiks in word):
            return [split_by_sufiks(word, sufiks), [word]]
        if (sufiks == 'што' and sufiks in word) and two_sufiksi:
            splitted_string = split_by_sufiks(word, sufiks)
            second_sufiks = pair[1 - pair.index('што')]
            modifed_string = splitted_string[:-1]
            modifed_string.extend(split_by_sufiks(splitted_string[-1], second_sufiks))
            return [modifed_string, split_by_sufiks(word, second_sufiks)]
        if (sufiks == 'што' and sufiks in word):
            return [split_by_sufiks(word, sufiks), [word]]


def check_for_prefiksi(word, prefiksi):
  for prefiks in prefiksi:
    two_syllabel_prefix = False
    if word.startswith(prefiks):
      letters_dict = name_each_letter(list(prefiks))
      letters_dict = check_for_samoglasno_r(letters_dict)
      number_of_vowels = count_vowels(letters_dict)
      len_prefiks = len(prefiks)
      if number_of_vowels >= 2:
        two_syllabel_prefix = True
        syllables =  hyphenate_syllables(split_into_syllables(prefiks))
        return [syllables, word[len_prefiks:]], two_syllabel_prefix
      else:
        return [word[0:len_prefiks], word[len_prefiks:]], two_syllabel_prefix

def check_for_exceptions(word: str) -> str:
    prefiksi = ('пред', 'над', 'нај', 'на', 'по', 'се', 'пре', 'из', 'екс', 'за', 'до')
    sufiksi = ('ски', 'ство', 'ствен')

    hyphenate_string = ''

    if word.startswith(prefiksi):
        if word[-1] == 'л':
            hyphenate_string = hyphenate_syllables(split_into_syllables(word))
        else:
            divided_strings = check_for_prefiksi(word)
            for substring in divided_strings:
                hyphenate_string += hyphenate_syllables(split_into_syllables(substring)) + '-'

    if 'ски' in word or 'ство' in word or 'ствен' in word:
        divided_strings = check_for_ski_stvo_stven(word)
        for substring in divided_strings:
            hyphenate_string += hyphenate_syllables(split_into_syllables(substring)) + '-'
    else:
        hyphenate_string = hyphenate_syllables(split_into_syllables(word))
    return hyphenate_string.strip('-')


def check_for_exceptions_1(word):
    prefiksi = ('пред', 'над', 'нај', 'на', 'по', 'се', 'пре', 'из', 'екс', 'за', 'до')
    sufiksi = ('ски', 'ство', 'ствен')

    hyphenate_string = ''

    divided_strings = []
    if word.startswith(prefiksi):
        if word[-1] == 'л' or word.startswith('дој'):
            divided_strings.append(word)
        else:
            prefiksi_divided_strings = check_for_prefiksi(word)
            divided_strings.append(prefiksi_divided_strings[0])
            prefiksi_divided_strings.pop(0)
            for substring in prefiksi_divided_strings:
                if 'ски' in substring or 'ство' in substring or 'ствен' in substring:
                    sufiksi_divided_strings = check_for_ski_stvo_stven(substring)
                    for sufiksi_substring in sufiksi_divided_strings:
                        divided_strings.append(sufiksi_substring)
                else:
                    divided_strings.extend(prefiksi_divided_strings)

    elif 'ски' in word or 'ство' in word or 'ствен' in word:
        sufiksi_divided_strings = check_for_ski_stvo_stven(word)
        for sufiksi_substring in sufiksi_divided_strings:
            divided_strings.append(sufiksi_substring)
    else:
        divided_strings.append(word)

    for substring in divided_strings:
        hyphenate_string += hyphenate_syllables(split_into_syllables(substring)) + '-'

    return hyphenate_string.strip('-')


def check_for_exceptions_2(word):
    prefiksi = (
    'против', 'пред', 'прет', 'пре', 'над', 'нај', 'над', 'нат', 'на', 'не', 'ни', 'обез', 'по', 'се', 'пре', 'из',
    'до', 'баш', 'без', 'бес', 'благо', 'бе', 'високо', 'вон', 'едно', 'жолто', 'за', 'зат', 'зелено', 'ис', 'едно',
    'зад', 'казнено', 'кусо', 'меѓу', 'многу', 'обес', 'оловно', 'пет', 'повеќе', 'подиз', 'под', 'пот', 'поизна',
    'поиз', 'полу', 'поне', 'пораз', 'порас', 'прaво', 'прво', 'прa', 'при', 'про', 'разно', 'раз', 'рас', 'рамно',
    'само', 'светло', 'себе', 'сино', 'ситно', 'сребро', 'слабо', 'танко', 'тенко', 'темно', 'три', 'триста', 'широко', 'брзо')

    sufiksi = ('ски', 'ство', 'ствен', 'што')

    has_prefiks = any(s in word for s in prefiksi)
    has_sufiks = any(s in word for s in sufiksi)

    divided_strings = []
    if word.startswith(prefiksi):
        prefiksi_divided_strings, two_syllabel_prefix = check_for_prefiksi(word, prefiksi)

        if not two_syllabel_prefix:
            divided_strings.append([word])

        prefiks = prefiksi_divided_strings[0]
        prefiksi_divided_strings.pop(0)

        for substring in prefiksi_divided_strings:
            if has_sufiks:
                sufiksi_divided_strings = check_for_ski_stvo_stven(substring)
                two_versions = all(isinstance(n, list) for n in sufiksi_divided_strings)
                if two_versions:
                    for sufiksi_substring in sufiksi_divided_strings:
                        prefiks_sufiksi_substring = [prefiks]
                        prefiks_sufiksi_substring.extend(sufiksi_substring)
                        divided_strings.append(prefiks_sufiksi_substring)
                else:
                    prefiks_sufiksi_substring = [prefiks]
                    prefiks_sufiksi_substring.extend(prefiksi_divided_strings)
                    divided_strings.append(prefiks_sufiksi_substring)

            else:
                prefiks_sufiksi_substring = [prefiks]
                prefiks_sufiksi_substring.extend(prefiksi_divided_strings)
                divided_strings.append(prefiks_sufiksi_substring)

    elif has_sufiks:
        sufiksi_divided_strings = check_for_ski_stvo_stven(word)
        for sufiksi_substring in sufiksi_divided_strings:
            divided_strings.append(sufiksi_substring)
    else:
        divided_strings.append(word)

    two_versions = all(isinstance(n, list) for n in divided_strings)
    versions = []
    hyphenate_string = ''

    if two_versions:
        for version in divided_strings:
            hyphenate_string = ''
            for substring in version:
                hyphenate_string += hyphenate_syllables(split_into_syllables(substring)) + '-'
            versions.append(hyphenate_string)
    else:
        for substring in divided_strings:
            hyphenate_string += hyphenate_syllables(split_into_syllables(substring)) + '-'
        versions.append(hyphenate_string)

    for i in range(len(versions)):
        v = versions[i]
        hyphenate_string = v.strip('-')
        hyphenate_string = re.sub('--', '-', hyphenate_string)
        versions[i] = hyphenate_string

    return set(versions)


class SplitIntoSyllables:

    #def __init__(self):

    @staticmethod
    def hyphenate(word):
        print(check_for_exceptions_2(word))
