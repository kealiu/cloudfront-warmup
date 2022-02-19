#encoding:utf-8
# -*- coding: utf-8 -*-
import os
import sys
import requests
import json
from bs4 import BeautifulSoup

CODESOURCE="https://www.feitsui.com/zh-hans/article/3"

def cf_pops_code_get(mainland=False):
    # china cloudfront pop, hardcode now
    if mainland:
        return ['BJS9-E1', 'PVG52-E1', 'SZX51-E1', 'ZHY50-E1']

    # global cloudfront pop 
    codes = []
    r = requests.get(CODESOURCE)
    soup = BeautifulSoup(r.text, 'html.parser')
    for tr in soup.find_all('tr'):
        c = tr.find('td')
        if c:
            codes.append(c.text)
    return codes

def cf_pops_save(filename, codes):
    if not codes:
        return
    with open(filename, 'w') as popfs:
        popfs.write(json.dumps(codes))

if __name__ == '__main__':
    print("usage: %s [mainland]")
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'mainland':
        print("mainland cloudfront edge code is updating")
        cf_pops_save('edges.mainland.json', cf_pops_code_get(True))
    else:
        print("cloudfront edge code is updating")
        cf_pops_save('edges.global.json', cf_pops_code_get())

