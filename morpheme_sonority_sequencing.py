from syllabels import split_by_sufiks, check_for_two_sufiksi
from phoneme_sonority_sequencing import find_clusters, add_hyphen


def check_for_ski_stvo_stven_2(word):
    suffixes = ['што', 'ски', 'ство', 'ствен']
    two_suffixes, pair = check_for_two_sufiksi(word, suffixes)
    for suffix in suffixes:
        if (suffix == 'ски' and suffix in word) or (suffix == 'ство' and suffix in word):
            return split_by_sufiks(word, suffix)
        if suffix == 'ствен' and suffix in word:
            return split_by_sufiks(word, suffix)
        if (suffix == 'што' and suffix in word) and two_suffixes:
            split_string = split_by_sufiks(word, suffix)
            second_suffix = pair[1 - pair.index('што')]
            modified_string = split_string[:-1]
            modified_string.extend(split_by_sufiks(split_string[-1], second_suffix))
            return modified_string
        if suffix == 'што' and suffix in word:
            return split_by_sufiks(word, suffix)


def check_for_prefixes_2(word, prefixes):
    for prefix in prefixes:
        if word.startswith(prefix):
            len_prefix = len(prefix)
            syllables = find_clusters(prefix)
            return syllables, word[len_prefix:]


def clean_list(list_with_empty_strings):
    return list(filter(None, list_with_empty_strings))


def morpheme_SSP(word):
    prefixes = (
    'ис', 'против', 'пред', 'прет', 'пре', 'над', 'нај', 'над', 'нат', 'на', 'не', 'ни', 'обез', 'по', 'се', 'пре',
    'из', 'до', 'баш', 'без', 'бес', 'благо', 'бе', 'високо', 'вон', 'едно', 'жолто', 'за', 'зат', 'зелено', 'едно',
    'зад', 'казнено', 'кусо', 'меѓу', 'многу', 'обес', 'оловно', 'пет', 'повеќе', 'подиз', 'под', 'пот', 'поизна',
    'поиз', 'полу', 'поне', 'пораз', 'порас', 'прaво', 'прво', 'прa', 'при', 'про', 'разно', 'раз', 'рас', 'рамно',
    'само', 'светло', 'себе', 'сино', 'ситно', 'сребро', 'слабо', 'танко', 'тенко', 'темно', 'три', 'триста', 'широко')

    suffixes = ('ски', 'ство', 'ствен', 'што')

    has_prefix = any(word.startswith(p) for p in prefixes)
    has_sufix = any(s in word for s in suffixes)

    divided_strings = []

    # prefixes
    if has_prefix:

        prefixes_divided_strings, remainder_of_word = check_for_prefixes_2(word, prefixes)
        divided_strings.extend(prefixes_divided_strings)

        # check for suffix in the remainder of the word
        if any(s in remainder_of_word for s in suffixes):
            suffixes_divided_strings = check_for_ski_stvo_stven_2(remainder_of_word)
            suffixes_divided_strings = clean_list(suffixes_divided_strings)
            divided_strings.extend(suffixes_divided_strings)

        else:
            divided_strings.append(remainder_of_word)

    # suffixes
    elif has_sufix:
        suffixes_divided_strings = check_for_ski_stvo_stven_2(word)
        suffixes_divided_strings = clean_list(suffixes_divided_strings)
        divided_strings.extend(suffixes_divided_strings)

    # nor prefixes nor suffixes
    else:
        divided_strings.append(word)

    hyphenate_string = []
    for string in divided_strings:
        hyphenate_string.extend(find_clusters(string))

    return add_hyphen(hyphenate_string)


class MorphemeSonoritySequencing:

    @staticmethod
    def word_to_morpheme_SSP(word):
        return morpheme_SSP(word)
