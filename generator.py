import string
import re


def regex_pattern(vowel: str, consonant: str):
    return vowel+consonant, consonant+vowel


def get_pattern_combinations(pttrn:tuple):
    combination_1 = (pttrn[0], pttrn[0])
    combination_2 = (pttrn[0], pttrn[1])
    combination_3 = (pttrn[1], pttrn[0])
    combination_4 = (pttrn[1], pttrn[1])

    return [combination_1,combination_2,combination_3,combination_4]


class Generator:
    def __init__(self):
        self.patterns = {
            "a" : [], # "a" : [ [('ab, 'ab'), (
            "e" : [],
            "i" : [],
            "o" : [],
            "u" : []
        }
        self.lowercase_alphabet = string.ascii_lowercase
        self.lowercase_vowels = re.findall("[aeiou]",self.lowercase_alphabet)
        self.lowercase_consonants = re.findall("[^aeiou]", self.lowercase_alphabet)

    def get_patterns(self, num_elements: int):
        [self.patterns[v].append(get_pattern_combinations(regex_pattern(v,c))) for v in self.lowercase_vowels for c in self.lowercase_consonants]

        if num_elements:
            for vowel, patterns in self.patterns.items():
                sliced = patterns[0:num_elements]
                self.patterns[vowel] = sliced
        return self.patterns