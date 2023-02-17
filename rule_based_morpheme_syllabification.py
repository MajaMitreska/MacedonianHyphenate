from utils import check_for_prefixes, check_for_ski_stvo_stven, check_for_multiple_versions, iterate_strings, merging_syllables, clean_output


def morpheme_rule_based(word):
    prefixes = {
        'ис', 'против', 'пред', 'прет', 'пре', 'над', 'нај', 'над', 'нат', 'на', 'не', 'ни', 'обез', 'по', 'се', 'пре',
        'из', 'до', 'баш', 'без', 'бес', 'благо', 'бе', 'високо', 'вон', 'едно', 'жолто', 'за', 'зат', 'зелено', 'едно',
        'зад', 'казнено', 'кусо', 'меѓу', 'многу', 'обес', 'оловно', 'пет', 'повеќе', 'подиз', 'под', 'пот', 'поизна',
        'поиз', 'полу', 'поне', 'пораз', 'порас', 'прaво', 'прво', 'прa', 'при', 'про', 'разно', 'раз', 'рас', 'рамно',
        'само', 'светло', 'себе', 'сино', 'ситно', 'сребро', 'слабо', 'танко', 'тенко', 'темно', 'три', 'триста',
        'широко'}
    suffixes = ('ски', 'ство', 'ствен', 'што')

    has_prefix = any(word.startswith(p) for p in prefixes)
    has_suffix = any(s in word for s in suffixes)

    divided_strings = []

    # prefixes
    if has_prefix:

        prefixes_divided_strings, two_syllable_prefix = check_for_prefixes(word, prefixes)

        prefix = prefixes_divided_strings.pop(0)
        for substring in prefixes_divided_strings:
            if any(s in substring for s in suffixes):
                suffixes_divided_strings = check_for_ski_stvo_stven(substring, 'morpheme')
                two_versions = check_for_multiple_versions(suffixes_divided_strings)
                if two_versions:
                    for suffixes_substring in suffixes_divided_strings:
                        divided_strings = iterate_strings(prefix, suffixes_substring, divided_strings)
                else:
                    divided_strings = iterate_strings(prefix, suffixes_divided_strings, divided_strings)
            else:
                divided_strings = iterate_strings(prefix, prefixes_divided_strings, divided_strings)


    #only suffixes
    elif has_suffix:
        suffixes_divided_strings = check_for_ski_stvo_stven(word, 'morpheme')
        temp_suffix = [suffixes_substring for suffixes_substring in suffixes_divided_strings]
        if check_for_multiple_versions(suffixes_divided_strings):
            divided_strings.extend(temp_suffix)
        else:
            divided_strings.append(temp_suffix)

    # no prefix nor suffix
    else:  # (not has_suffix) and (not has_prefix):
        divided_strings.append(word)

    two_versions = check_for_multiple_versions(divided_strings)
    versions = []

    if two_versions:
        for version in divided_strings:
            hyphenate_string = merging_syllables(version)
            versions.append(hyphenate_string)
    else:
        hyphenate_string = merging_syllables(divided_strings)
        versions.append(hyphenate_string)

    versions = clean_output(versions)

    return versions


class RuleBasedMorphemeSyllabification:
    # def __init__(self):
    @staticmethod
    def split(word):
        return ", ".join(morpheme_rule_based(word))
