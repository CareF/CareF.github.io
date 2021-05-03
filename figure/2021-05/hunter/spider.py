#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import requests
import urllib
import re
import html
import json
from opencc import OpenCC
from googletrans import Translator
translator = Translator()

baseURL = 'https://hunterxhunter.fandom.com'
jenny = (re.escape(r'<span style="white-space:nowrap;"><a href="/wiki/Currencies_in_Hunter_%C3%97_Hunter#Jenny" title="Currencies in Hunter × Hunter#Jenny"><img alt="Jenny Symbol 2011.svg" src="data:image/gif;base64,R0lGODlhAQABAIABAAAAAP///yH5BAEAAAEALAAAAAABAAEAQAICTAEAOw%3D%3D" decoding="async" width="10" height="15" data-image-name="Jenny Symbol 2011.svg" data-image-key="Jenny_Symbol_2011.svg" data-src="https://static.wikia.nocookie.net/hunterxhunter/images/4/42/Jenny_Symbol_2011.svg/revision/latest/scale-to-width-down/10?cb=20191111075333" class="lazyload" /></a></span>'),
         re.escape(r'<sup id="cite_ref-chap129_1-2" class="reference"><a href="#cite_note-chap129-1">&#91;1&#93;</a></sup>'))

def get_card_url():
    url = 'https://hunterxhunter.fandom.com/wiki/Greed_Island_Card_Lists'
    page = urllib.request.urlopen(url)
    content = page.read().decode()
    card_url = re.compile(r'''href="(/wiki/([^"]*)_\(G\.I_card\))"''')
    for url, name in card_url.findall(content):
        name = urllib.parse.unquote(name).replace('_', ' ')
        yield name, baseURL+url


def parse_card(url):
    page = urllib.request.urlopen(url)
    content = page.read().decode()
    linkMatch = r'(?:[^<]|<a href=[^>]*>[^<]*</a>|<i>[^<]*</i>|%s|%s)*'%jenny
    rubyMatch = r'(?:[^<]|<ruby><rb>[^<]*</rb><rp>\(</rp><rt>[^<]*</rt><rp>\)</rp></ruby>)*'
    pic = re.compile(r"""<meta property="og:image" content="([^"]*\.png)/revision/latest\?cb=\d*"/>
""")
    itemType = re.compile(r"""<th>Type:
</th>
<td[^>]*><b>([^<]*)</b>
</td>""", re.MULTILINE)
    itemName = re.compile(
        r"""<div class="pi-item pi-data pi-item-spacing pi-border-color" data-source="Name">
\t
\t\t<h3 class="pi-data-label pi-secondary-font">Name \(EN\)</h3>
\t
\t<div class="pi-data-value pi-font">(%s)(?:<br/>)?</div>
</div>"""%rubyMatch, re.MULTILINE)

    itemName_JP = re.compile(
        r"""<div class="pi-item pi-data pi-item-spacing pi-border-color" data-source="Name2">
\t
\t\t<h3 class="pi-data-label pi-secondary-font">Name \(JP\)</h3>
\t
\t<div class="pi-data-value pi-font">(%s)(?:<br/>)?</div>
</div>"""%rubyMatch, re.MULTILINE)
    itemNumber = re.compile(r"""<th>Number:
</th>
<td[^>]*>#([-\d]*)
</td>""", re.MULTILINE)
    itemRank = re.compile(
        r"""<div class="pi-item pi-data pi-item-spacing pi-border-color" data-source="Rank">
\t
\t\t<h3 class="pi-data-label pi-secondary-font">Rank</h3>
\t
\t<div class="pi-data-value pi-font">([A-Z]*|N/A)</div>
</div>

<div class="pi-item pi-data pi-item-spacing pi-border-color" data-source="Transform">
\t
\t\t<h3 class="pi-data-label pi-secondary-font">Transform</h3>
\t
\t<div class="pi-data-value pi-font">(\d*|∞|N/A)</div>
</div>""")
    itemEffect = re.compile(r"""<th>Card Effect:
</th>
<td[^>]*>(?:\n<p>)?(%s)(?:\n</p>)?
</td>"""%linkMatch, re.MULTILINE)
    itemObtain = re.compile(r"""<th>How to Obtain:
</th>
<td[^>]*>(?:\n<p>)?(%s)(?:\n</p>)?
</td>"""%linkMatch, re.MULTILINE)
    itemJap = re.compile(r"""<th>\[Jap\]
</th>
<td>[^\n]*<br />(?:\n<p>)?(%s)(?:\n</p>)?
</td></tr>"""%linkMatch, re.MULTILINE)
    itemEng = re.compile(r"""<th>\[Eng\]
</th>
<td>[^\n]*<br />(?:\n<p>)?(%s)(?:\n</p>)?
</td></tr>"""%linkMatch, re.MULTILINE)
    spellClasses = re.compile(r"""<th>Class
</th>
<td [^>]*>((?:<i>[^<]*</i>\s*<br />\s*)*<i>[^<]*</i>)
</td>""")
    spellClass = re.compile(r'<i>([^<]*)</i>')
    res = {
        "type": itemType.search(content).group(1),
        "number": itemNumber.search(content).group(1),
        "name": itemName.search(content).group(1),
        "name_JP": jpEscape(itemName_JP.search(content).group(1)),
        "rank": "{}-{}".format(*itemRank.search(content).groups()),
        "effect": jpEscape(itemEffect.search(content).group(1)),
        "effect_JP": jpEscape(itemJap.search(content).group(1)),
        "effect_EN": jpEscape(itemEng.search(content).group(1)),
        "obtain": jpEscape(itemObtain.search(content).group(1)),
        "picURL": pic.search(content).group(1)
        }
    if res["type"] == "Spell Card":
        allClasses = spellClasses.search(content).group(1)
        res['class'] = spellClass.findall(allClasses)
    return res


def jpEscape(jpWords):
    jpWords = html.unescape(jpWords)
    rubies = re.findall(
        r'<ruby><rb>([^<]*)</rb><rp>\(</rp><rt>([^<]*)</rt><rp>\)</rp></ruby>',
        jpWords)
    if rubies:
        jpWords = ''.join(
            '{}({})'.format(*w) if w[1] else w[0] for w in rubies if w[0])
    return jpWords


def getJson(filename):
    res = []
    seen = set()
    for card, url in get_card_url():
        if card in seen:
            continue
        seen.add(card)
        print(card)
        detail = parse_card(url)
        if card != detail['name']:
            print('   name: {}'.format(detail['name']))
            detail['link_name'] = card
        res.append(detail)
        # assert card == res[-1][card]["name"]
    res.sort(key=lambda card:card['number'])
    with open(filename, 'w') as f:
        json.dump(res, f, indent=2, ensure_ascii=False)


def getFigs(filename):
    import os
    with open(filename, 'r') as f:
        data = json.load(f)
    for card in data:
        picFile = card['number']+'.png'
        if not os.path.exists(picFile):
            print("Downloading {}.{}".format(card['number'], card['name']))
            count = 0
            succeed = False
            while not succeed and count < 1:
                try:
                    urllib.request.urlretrieve(
                        card['picURL'], picFile)
                    succeed = True
                except urllib.error.ContentTooShortError:
                    os.remove(picFile)
                    count += 1
                    print('  {}-th trail failed...'.format(count))
            # assert succeed


def translate(filename, cardType):
    with open(filename, 'r') as f:
        data = json.load(f)
    res = []
    toTrans = []
    for card in data:
        if card['type'] == cardType:
            card['name_CN'] = OpenCC('t2s').convert(card['name_JP'])
            toTrans.append(card['effect_JP'])
            res.append(card)
    # run it once to avoid banning from the open API
    transed = translator.translate(toTrans, src='ja', dest='zh-CN')
    for n, item in enumerate(transed):
        assert item.origin == res[n]['effect_JP']
        assert item.src == 'ja'
        res[n]['effect_CN'] = item.text
    res.sort(key=lambda card: int(card["number"]))
    with open(cardType.replace(' ', '_').lower()+'_CN.json', 'w') as f:
        json.dump(res, f, indent=2, ensure_ascii=False)


def toTable(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    result = ''
    fig = "{{{{ __site__ }}}}/figure/2021-05/hunter/spell/{0}.png"
    fighosted = "https://www.caref.xyz/figures/hunter_spell/{0}.png"
    # line = """|[![]({5})]({4})  | **NO.{0} {1}** <br> {2} <br> {3} |\n"""
    line = """    <tr>
        <td><a href="{4}"><img src="{5}" alt="" /></a></td>
        <td><strong>NO.{0} {1}</strong> <br /> {2} <br /> {3} </td>
    </tr>
"""
    for card in data:
        result += line.format(card['number'], card['name_CN'], card['rank'], 
                              card['effect_CN'],
                              # card['picURL']
                              fighosted.format(card['number']),
                              fig.format(card['number'])
                              )
    return result


if __name__ == '__main__':
    # getJson('all_cards.json')
    # getFigs('all_cards.json')
    # translate('all_cards.json', 'Spell Card')
    print(toTable('spell_card_CN_proofed.json'))

