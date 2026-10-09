#!/usr/bin/env python3
"""Sort the word art range into sub-categories (tags wa-*) for the Word Art sub-collections (9 Oct 2026).
Usage: python3 -I subcategories.py <active_products.jsonl> <out.csv>"""
import csv, json, re, sys

GROUPS = [  # (tag, collection title, rule on the title) - first match wins
    ('wa-pop', 'Pop Character Word Art', r'inspired by pop figures|\b(ariel|aurora|belle|cinderella|jasmine|merida|mulan|rapunzel|snow white|'
     r'chandler|joey|monica|pheobe|phoebe|rachel|ross|dobby|draco|dumbledor|ginny|hagrid|harry potter|luna|mcgonagol|moaning|'
     r'ron weasley|sirius|snape|voldermort)\b'),
    ('wa-names', 'Name Letter Word Art', r'\bletter [a-z]\b'),
    ('wa-ages', 'Age & Birthday Word Art', r'\bnumber \d+|\bage \d+|\d+(st|nd|rd|th) birthday|rainbow age'),
    ('wa-love-family', 'Love & Family Word Art', r'\b(heart|couple|family|lips|wine glass|mum|mam|nanna|wedding|love)\b'),
    ('wa-pets-animals', 'Pets & Animals Word Art', r'\b(cat|dog|beagle|collie|bulldog|spaniel|chihuahua|cockapoo|corgi|dachshund|dalmatian|'
     r'shepard|shepherd|husky|ihasa|lhasa|jack russell|labrador|schnauzer|pug|shiatsu|shih|paw|elephant|dolphin|owl|penguin|fox|'
     r'racoon|seahorse|butterfly|panda|flamingo|lion)\b'),
    ('wa-hobbies-sport', 'Hobbies & Sport Word Art', r'\b(ballet|golf|golfer|cricket|footballer|runner|horse racer|dancer|guitar|'
     r'saxophone|car|train|basketball|football)\b'),
    ('wa-kids', 'Kids & Fantasy Word Art', r'\b(unicorn|fairy|princess|crown|dino|dinosaur|superhero|teddy|rainbow|dress|donut|flower)\b'),
    ('wa-places', 'Places & Home Word Art', r'\b(eiffel|liberty|staue|house)\b'),
]


def group(title):
    t = title.lower()
    for tag, _, rule in GROUPS:
        if re.search(rule, t):
            return tag
    return ''


def main(src, out):
    rows = []
    for line in open(src):
        o = json.loads(line)
        if 'Word Art' not in o.get('tags', []) and 'word art' not in o['title'].lower():
            continue
        rows.append({'id': o['id'], 'title': o['title'], 'tag': group(o['title'])})
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, ['id', 'title', 'tag']); w.writeheader(); w.writerows(rows)
    from collections import Counter
    print(Counter(r['tag'] for r in rows))
    for r in rows:
        if not r['tag']:
            print('UNSORTED', r['title'])


if __name__ == '__main__':
    main(*sys.argv[1:])
