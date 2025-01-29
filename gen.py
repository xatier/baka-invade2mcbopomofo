"""
Usage:

clone repo from https://github.com/caris-events/baka-invade

python gen.py | sort -k2,2 > output.txt

# add output.txt to fcitx5-mcbopomofo-git user dict
vim ~/.local/share/fcitx5/mcbopomofo/data.txt
"""

import collections
import contextlib
import itertools
import pathlib
import string

import yaml

DICT = "/usr/share/fcitx5/data/mcbopomofo-data.txt"
BPMF_FILE = '/usr/share/fcitx5/data/mcbopomofo-data-plain-bpmf.txt'
p = pathlib.Path('database/vocabs/')


# possible bpmf combinations for the given phrase
def word2bpmf(phrase: str) -> list[str]:
    lookup: dict[str, list[str]] = {}
    with open(BPMF_FILE) as f:
        lines: list[str] = f.readlines()[508:]

    for line in lines:
        phonetic: str
        char: str
        phonetic, char = line.split()[:2]
        if char not in lookup:
            lookup[char] = [phonetic]
        else:
            lookup[char].append(phonetic)

    with contextlib.suppress(KeyError):
        combo: list[list[str]] = [lookup[c] for c in phrase]
        return [f'{"-".join(t)}' for t in itertools.product(*combo)]

    return []


# extract Chinese phrases and replacements from yaml files
baka_dict: dict[str, list[str]] = collections.defaultdict(list)
baka_dict_bpmf: dict[str, str] = {}
for f in p.glob('*.yml'):
    y = yaml.safe_load(f.open())
    word: str = y['word']
    bpmf: str | None = y['bopomofo']
    baka_dict_bpmf[word] = bpmf.replace(' ', '-') if bpmf is not None else ''
    for e in y['examples']:
        for w in e['words']:
            baka_dict[word].append(w)

# load fcitx5-mcbopomofo-git dictionary
mcbopomofo_dict: dict[str, list[str]] = collections.defaultdict(list)
with open(DICT) as f:
    for line in f:
        # skip comments
        if '#' in line:
            continue

        with contextlib.suppress(ValueError):
            bpmf, word, freq = line.split()
            mcbopomofo_dict[word].append(bpmf)

# lookup the collected Chinese phrases from fcitx5-mcbopomofo-git dict
for word, replacements in baka_dict.items():
    # stuff we don't have
    if word not in mcbopomofo_dict and all(
        c not in word.upper() for c in string.ascii_uppercase
    ):
        # patch bpmf from baka dict with suggested phrases
        bpmf = baka_dict_bpmf[word]
        for replacement in replacements:
            print(f'{replacement} {bpmf}')

        # attempt to compose possible bpmf for the phrase not in the dictionary
        # patch with suggested phrases
        combos: list[str] = word2bpmf(word)

        # skip if we have seen this, this avoids unnecessary terms
        if bpmf not in combos:
            for combo in combos:
                for replacement in replacements:
                    print(f'{replacement} {combo}')

    # stuff we have
    if word in mcbopomofo_dict:
        for bpmf in mcbopomofo_dict[word]:
            # patch with suggested phrases
            for replacement in replacements:
                print(f'{replacement} {bpmf}')
