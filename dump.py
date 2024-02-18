"""
Usage:

clone repo from https://github.com/caris-events/baka-invade

# extract Chinese phrases
python dump.py | awk '{print $1'} > 1.txt

# search in fcitx5-mcbopomofo-git dict
./check.sh | awk '{print $2" "$1}' > check.txt

# patch with suggested phrases
python patch.py | sort -k2,2 > 2.txt

# add 2.txt to fcitx5-mcbopomofo-git user dict
vim ~/.local/share/fcitx5/mcbopomofo/data.txt
"""

import pathlib

import yaml

p = pathlib.Path('database/dict/')

for f in p.glob('*.yml'):
    y = yaml.safe_load(f.open())
    word = y['word']
    print(f'{word} -> ', end='')
    for e in y['examples']:
        for w in e['words']:
            print(w, end=', ')

    print()
