from utils import split_by_suffix, check_for_multiple_versions, merging_syllables, clean_output


def check_for_rule_based_ski_stvo_stven(word):
    suffixes = ['ски', 'ство', 'ствен']
    for suffix in suffixes:
        if (suffix == 'ски' and suffix in word) or (suffix == 'ство' and suffix in word):
            return split_by_suffix(word, suffix)
        if suffix == 'ствен' and suffix in word:
            return [split_by_suffix(word, suffix), [word]]


def phoneme_rule_based(word):
    suffixes = ('ски', 'ство', 'ствен',)
    has_suffix = any(s in word for s in suffixes)

    divided_strings = []
    # has suffixes
    # rule 6
    if has_suffix:
        suffixes_divided_strings = check_for_rule_based_ski_stvo_stven(word)
        temp_suffixes = [suffixes_substring for suffixes_substring in suffixes_divided_strings]
        if check_for_multiple_versions(suffixes_divided_strings):
            divided_strings.extend(temp_suffixes)
        else:
            divided_strings.append(temp_suffixes)

    # no prefix nor suffixes
    else:
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


class RuleBasedPhonemeSyllabification:
    # def __init__(self):
    @staticmethod
    def split(word):
        return "".join(phoneme_rule_based(word))
