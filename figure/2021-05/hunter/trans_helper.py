#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
from opencc import OpenCC
from googletrans import Translator
translator = Translator()

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
    with open(cardType.replace(' ', '_').lower()+'_cn.json', 'w') as f:
        json.dump(res, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    # translate('all_cards.json', 'Spell Card')
