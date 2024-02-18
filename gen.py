"""
Usage:

clone repo from https://github.com/caris-events/baka-invade

python gen.py | sort -k2,2 > output.txt

# add output.txt to fcitx5-mcbopomofo-git user dict
vim ~/.local/share/fcitx5/mcbopomofo/data.txt
"""

import collections
import contextlib
import pathlib

import yaml

DICT = "/usr/share/fcitx5/data/mcbopomofo-data.txt"
p = pathlib.Path('database/dict/')

# extract Chinese phrases and replacements from yaml files
baka_dict = collections.defaultdict(list)
for f in p.glob('*.yml'):
    y = yaml.safe_load(f.open())
    word = y['word']
    for e in y['examples']:
        for w in e['words']:
            baka_dict[word].append(w)

# load fcitx5-mcbopomofo-git dictionary
mcbopomofo_dict = collections.defaultdict(list)
with open(DICT) as f:
    for line in f.readlines():
        # skip comments
        if '#' in line:
            continue

        with contextlib.suppress(ValueError):
            bpmf, word, freq = line.split()

        mcbopomofo_dict[word].append(bpmf)

# lookup the collected Chinese phrases from fcitx5-mcbopomofo-git dict
for word, replacements in baka_dict.items():
    if word in mcbopomofo_dict:
        for bpmf in mcbopomofo_dict[word]:
            # patch with suggested phrases
            for replacement in replacements:
                print(f'{replacement} {bpmf}')
