#!/usr/bin/env python3
"""The 13 new word art prints from Ben's Dropbox folder (9 Oct 2026): rainbow age numbers + Mum/Mam hearts.
Writes products.json (title, handle, copy, SEO, tags, SKU base, images) for the create step."""
import json, sys

SIZES = [('A4 Print Only', '4.99', 'A4'), ('A3 Print Only', '9.99', 'A3'), ('A2 Print Only', '12.99', 'A2'),
         ('A1 Print Only', '19.99', 'A1'), ('A4 Print + Black Frame', '19.99', 'A4-BLK'),
         ('A4 Print + Silver Frame', '19.99', 'A4-SLV'), ('A3 Print + Black Frame', '29.99', 'A3-BLK'),
         ('A3 Print + Silver Frame', '29.99', 'A3-SLV')]

SPEC = ('<h3>Size &amp; details</h3>\n<ul>\n<li>Design: {design}</li>\n'
        '<li>Print only: A4 (210 x 297 mm), A3 (297 x 420 mm), A2 (420 x 594 mm) or A1 (594 x 841 mm)</li>\n'
        '<li>Paper: A4 on 350gsm card, A3 on 170gsm gloss, A2 and A1 on 210gsm gloss</li>\n'
        '<li>Framed: A4 (with a stand) or A3 (with a hanging clip) in a black or silver Premium Display frame</li>\n</ul>\n'
        '<h3>Delivery</h3>\n<p>{delivery}</p>\n')

AGES = {
 16: ('sweet sixteen', 'Sweet sixteen deserves more than a card. This personalised 16th birthday word art print turns the number 16 into a rainbow of their name, their friends and everything they love right now.',
      'school friends, favourite bands, nicknames, the dog\'s name, in-jokes from the group chat', 'Pair it with a birthday mug for a 16th they\'ll remember.'),
 18: ('18th', 'Eighteen is a big one, and this personalised 18th birthday word art print marks it in full colour: a rainbow number 18 filled with their name and the words that sum them up.',
      'mates, first car, holidays, uni plans, favourite food, family names', 'Hang it at the party, then take it home for their bedroom wall.'),
 21: ('21st', 'Celebrate a 21st with a print they will keep long after the party. This personalised 21st birthday word art fills a rainbow number 21 with their name and a list of words you choose.',
      'uni friends, places they have lived, nights out, hobbies, family nicknames', 'A keepsake 21st birthday gift that will outlast the balloons.'),
 30: ('30th', 'Turning thirty? Mark the milestone with this personalised 30th birthday word art print, a rainbow number 30 built from their name and thirty years of memories.',
      'partner and children, best friends, travels, jobs, teams they support', 'A thoughtful 30th birthday present for a partner, sibling or best friend.'),
 40: ('40th', 'Forty and fabulous: this personalised 40th birthday word art print turns the number 40 into a colourful collage of their name and the words that tell their story.',
      'family names, places, pets, favourite sayings, hobbies, holidays', 'Add a 40th birthday card and you have the whole gift sorted.'),
 50: ('50th', 'Half a century is worth celebrating properly. This personalised 50th birthday word art print fills a rainbow number 50 with their name and fifty years of family, friends and favourite things.',
      'children and grandchildren, wedding year, homes, teams, hobbies', 'A lovely 50th birthday gift from the whole family.'),
 60: ('60th', 'For a 60th birthday, this personalised word art print gathers a lifetime of names, places and memories into a bright rainbow number 60.',
      'grandchildren, old friends, places they grew up, favourite holidays, hobbies', 'A thoughtful 60th birthday present for Mum, Dad, Nan or Grandad.'),
 70: ('70th', 'Seventy years of stories in one print: this personalised 70th birthday word art turns the number 70 into a rainbow of their name and the people and places that matter to them.',
      'children, grandchildren, great-grandchildren, home towns, pets, pastimes', 'Sign it from all the family for a 70th birthday to remember.'),
 80: ('80th', 'An 80th birthday deserves a gift full of love. This personalised 80th birthday word art print fills a rainbow number 80 with their name and the names of everyone who loves them.',
      'every grandchild\'s name, family nicknames, special places, favourite sayings', 'A treasured 80th birthday keepsake for Nan, Grandad or a great-aunt.'),
 90: ('90th', 'Ninety years is a remarkable milestone. This personalised 90th birthday word art print turns the number 90 into a colourful tribute made from their name and a lifetime of family and memories.',
      'children, grandchildren, great-grandchildren, wartime or home towns, lifelong friends', 'A heartfelt 90th birthday gift the whole family can add words to.'),
 100: ('100th', 'A hundredth birthday calls for something special. This personalised 100th birthday word art print fills a rainbow number 100 with their name and a century of family, friends and memories.',
      'every generation of the family, places, decades, favourite sayings, hobbies', 'A once-in-a-lifetime 100th birthday keepsake.'),
}


def age_product(n):
    word, intro, ideas, close = AGES[n]
    title = f'Personalised {word.capitalize() if word != "sweet sixteen" else "Sweet 16"} Birthday Rainbow Word Art Print – Number {n}'
    if n in (16,):
        title = 'Personalised Sweet 16 Birthday Rainbow Word Art Print – Number 16'
    pk = f'personalised {"16th" if n == 16 else word} birthday word art print'
    body = (f'<p>{intro}</p>\n'
            f'<h2>Personalised {"16th" if n == 16 else word} birthday word art print in rainbow colours</h2>\n'
            f'<p>Fill in two boxes: the name, which appears once nice and big, and your word list of 20 to 30 words separated by commas, such as {ideas}. '
            f'We repeat your words in different sizes and fonts across the number {n}, shading from red through orange, yellow, green and blue to purple, until it is full. '
            'The preview shows what you have typed next to the print photo.</p>\n'
            '<p>Keep to single words or short phrases of three words at most, put a comma between each, and leave out emoji and accented letters. We print exactly what you type, so check the spelling once more.</p>\n'
            '<h3>Why you\'ll love it</h3>\n<ul>\n'
            f'<li>A rainbow number {n} made only from words you choose, so no two prints are the same</li>\n'
            '<li>The name stands out once, and your other words fill every gap in different sizes</li>\n'
            '<li>Premium Display frames in black or silver: thick, chunky and very professional, not cheap thin frames</li>\n'
            '<li>Four print-only sizes, from a shelf-sized A4 to a statement A1</li>\n</ul>\n'
            + SPEC.format(design=f'a rainbow number {n}, filled with your name and 20–30 words',
                          delivery=f'Your personalised {"16th" if n == 16 else word} birthday word art print is posted the next working day, or the same day if you order before 12pm, by Royal Mail.')
            + f'<p>{close}</p>')
    seo_t = f'Personalised {"16th" if n == 16 else word.capitalize()} Birthday Word Art Print | Foxy Printing'
    if len(seo_t) > 60:
        seo_t = f'{"16th" if n == 16 else word.capitalize()} Birthday Rainbow Word Art | Foxy Printing'
    seo_d = (f'A personalised {"16th" if n == 16 else word} birthday word art print: a rainbow number {n} made from a name and 20–30 words. A4 to A1 or framed, posted next working day.')
    return dict(key=f'age-{n}', title=title, handle=f'personalised-{n}-birthday-rainbow-word-art-print',
                body=body, seo_title=seo_t, seo_desc=seo_d, colour='Multicolor', tag='wa-ages',
                tags=['Word Art', 'Personalised Word Art', 'io-word-art', 'wa-ages', 'rainbow word art', f'{n}th birthday' if n not in (21,) else '21st birthday', 'birthday word art'],
                sku=f'FOXY-POSTER-WA-RAINBOW-{n}', alt=f'Personalised {"16th" if n == 16 else word} birthday rainbow word art print, number {n}')


HEARTS = {
 'mum-1': dict(title='Personalised Mum Heart Word Art Print – Pink Love Heart with Your Words',
    handle='personalised-mum-heart-word-art-print', colour='Pink',
    intro='Tell Mum exactly what she means to you with this personalised Mum heart word art print: a big pink love heart packed with the words that remind you of her.',
    h2='Personalised Mum heart word art print', pk='personalised mum heart word art print',
    ideas='Best Mum Ever, cuddles, home, laughs, the children\'s names, her favourite sayings',
    design='a pink love heart, filled with your words in bold shades of pink',
    close='A Mother\'s Day, birthday or just-because gift she will hang with pride.',
    seo_t='Personalised Mum Heart Word Art Print | Foxy Printing',
    seo_d='A personalised Mum heart word art print: a pink love heart made from 20–30 words you choose. A4 to A1 or framed. A gift for Mother\'s Day or her birthday.'),
 'mam-2': dict(title='Personalised MAM Word Art Print – Pink Letters and Heart with Your Words',
    handle='personalised-mam-word-art-print-pink-heart', colour='Pink',
    intro='For the Mams of the North East and Wales, this personalised MAM word art print spells out M, heart, M in soft pink, filled with all the little words that make her your Mam.',
    h2='Personalised MAM word art print', pk='personalised mam word art print',
    ideas='Best Mam Ever, kisses, cuddles, good times, family names, things only she says',
    design='the word MAM with a heart in the middle, filled with your words in shades of pink',
    close='Perfect for Mother\'s Day, her birthday or a thank-you from the whole family.',
    seo_t='Personalised MAM Word Art Print | Foxy Printing',
    seo_d='A personalised MAM word art print: M, heart, M in pink, made from 20–30 words you choose. A4 to A1 or framed. A gift your Mam will love.'),
}


def heart_product(key):
    h = HEARTS[key]
    body = (f'<p>{h["intro"]}</p>\n<h2>{h["h2"]}</h2>\n'
            f'<p>Fill in two boxes: the name or main word, shown once and largest, and your word list of 20 to 30 words separated by commas, such as {h["ideas"]}. '
            'We repeat your words in different sizes, fonts and shades until the shape is full, and the preview shows what you have typed next to the print photo.</p>\n'
            '<p>Use single words or short phrases of three words at most, with a comma between each. No emoji or accented letters, please. We print exactly what you type.</p>\n'
            '<h3>Why you\'ll love it</h3>\n<ul>\n<li>Every word comes from you, so it is one of a kind</li>\n'
            '<li>Premium Display frames in black or silver: thick, chunky and very professional, not cheap thin frames</li>\n'
            '<li>High-quality full-colour print, made to order</li>\n<li>Four print-only sizes, from A4 up to A1</li>\n</ul>\n'
            + SPEC.format(design=h['design'], delivery=f'Your {h["pk"]} is posted the next working day, or the same day if you order before 12pm, by Royal Mail.')
            + f'<p>{h["close"]}</p>')
    return dict(key=key, title=h['title'], handle=h['handle'], body=body, seo_title=h['seo_t'], seo_desc=h['seo_d'],
                colour=h['colour'], tag='wa-love-family',
                tags=['Word Art', 'Personalised Word Art', 'io-word-art', 'wa-love-family', 'mothers day', 'mum gift', 'heart word art'],
                sku='FOXY-POSTER-WA-' + key.upper().replace('-1', '-HEART').replace('-2', '-HEART'),
                alt=h['h2'].replace('Personalised', 'Personalised').lower().capitalize() + ' in pink')


def main(out):
    P = [age_product(n) for n in AGES] + [heart_product(k) for k in HEARTS]
    for p in P:
        assert len(p['seo_title']) <= 70, p['seo_title']
        assert len(p['title']) <= 150
        p['variants'] = [{'option': s, 'price': pr, 'sku': f'{p["sku"]}-{suf}'} for s, pr, suf in SIZES]
    json.dump(P, open(out, 'w'), indent=1, ensure_ascii=False)
    for p in P:
        print(len(p['seo_title']), len(p['seo_desc']), p['title'])


if __name__ == '__main__':
    main(sys.argv[1])
