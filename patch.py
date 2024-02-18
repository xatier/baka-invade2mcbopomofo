import pathlib

import yaml

d = {}
with open('check.txt') as f:
    for line in f.readlines():
        word, bpmf = line.split()
        d[word] = bpmf

p = pathlib.Path('database/dict/')

for f in p.glob('*.yml'):
    y = yaml.safe_load(f.open())
    word = y['word']
    if word in d:
        for e in y['examples']:
            for w in e['words']:
                print(f'{w} {d[word]}')
