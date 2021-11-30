#encoding:utf-8
# -*- coding: utf-8 -*-
import os
import sys
import requests
from multiprocessing.pool import ThreadPool
from bs4 import BeautifulSoup

_gcfg = {
    "pops": {
        "addones": [],  # in case you find new edge-pop code
        "source": "https://www.feitsui.com/zh-hans/article/3",  # the sources of edge-pop code
        "china": ['BJS9-E1', 'PVG52-E1', 'SZX51-E1', 'ZHY50-E1']  # the sources of edge-pop code for china
     },
    "http": True,   # enable http url
    "https": False,  # enable https url
    "china": False,  # in case china cloudfront
    "threads": 200,  # how many threads 
    "timeout": (3,3),  # url connection timeout
    "origin": "",   # origin domain(optional)
    "cname" : "",    # the cname
    "action": "GET" # the http action
}

def cf_pops_code_get():
    codes = []

    # china cloudfront pop, hardcode now
    if _gcfg['china']:
        return _gcfg['pops']['china']

    # global cloudfront pop 
    r = requests.get(_gcfg['pops']['source'])
    soup = BeautifulSoup(r.text, 'html.parser')
    for tr in soup.find_all('tr'):
        c = tr.find('td')
        if c:
            codes.append(c.text)
    if _gcfg['pops']['addones']:
        codes += _gcfg['pops']['addones']
    return codes

def cf_pops_domain_gen(origin):
    doaminparts = origin.split('.')
    distri = doaminparts[0]
    cfdomain = '.'.join(doaminparts[1:])
    return [distri+"."+code+"."+cfdomain for code in cf_pops_code_get()];

def cf_url_gen(origin, urls):
    cfurls = []
    for dn in cf_pops_domain_gen(origin):
        if _gcfg['http']:
            cfurls += ["http://"+dn+u for u in urls]
        if _gcfg['https']:
            cfurls += ["https://"+dn+u for u in urls]
    return cfurls

def cf_pops_url_warmup(url):
    try:
        r = requests.request(_gcfg['action'], url, headers={"Host": _gcfg['cname']}, verify=False, timeout=_gcfg['timeout'])
        if r.status_code >= 400:
            print("warning: %s refreshing failing, ignore!!!"%url)
        else:
            print("SUCCESS: %s warmup done!"%url)
    except Exception as e:
        print("error: %s %s"%(str(e), url)) # didn't care the output
    return None

def cf_refresh_task(origin, urls):
    # for multi processing
    with ThreadPool(_gcfg['threads']) as p:
        p.map(cf_pops_url_warmup, cf_url_gen(origin, urls))

    # for single thread
    #for url in cf_url_gen(origin, urls):
    #    cf_pops_url_warmup(url)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: %s <dxxxxxxxx.cloudfront.net-of-cloudfront-distribution> <file-named-as-domain-with-url-per-line-in-it> [GET|HEAD|OPTION]')
        exit(-1)
    urls = []
    with open(sys.argv[2], 'r') as uf:
        urls = [u.strip() if u.startswith('/') else '/'+u.strip() for u in uf.readlines()]
    _gcfg['origin'] = sys.argv[1]
    _gcfg['cname'] = sys.argv[2]
    _gcfg['action'] = 'GET'
    if len(sys.argv) == 4 and sys.argv[3] in ['GET', 'HEAD', 'OPTION']:
        _gcfg['action'] = sys.argv[3]
    cf_refresh_task(sys.argv[1], urls)
