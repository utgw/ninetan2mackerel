#!/usr/bin/python
import os
import re
import time
import json
import requests

SX9_URL = 'http://sx9.jp/weather/kyoto-yoshida.js'
p = re.compile(r'\((\d+), (\d+), (\d+)\)')

MACKEREL_URL = os.environ['MACKEREL_URL']
MACKEREL_API_KEY = os.environ['MACKEREL_API_KEY']

def parse(text, minute=0):
    data = [x.strip() for x in text.splitlines() if 'data.setValue({},'.format(minute) in x][1:]
    poe = []

    for line in data:
        m = p.search(line)
        poe.append(int(m.group(3)))

    return max(poe)

def main():
    r = requests.get(SX9_URL)
    r.raise_for_status()
    text = r.text
    yoshida = parse(text, 5)
    yoshida_1h = parse(text, 60)

    headers = {
        'X-Api-Key': MACKEREL_API_KEY,
        'Content-Type': 'application/json'
        }
    payload = [
        {
            'name': 'sx9.yoshida', 
            'time': int(time.strftime('%s', time.localtime())),
            'value': yoshida
        },
        {
            'name': 'sx9.yoshida_1h', 
            'time': int(time.strftime('%s', time.localtime())),
            'value': yoshida_1h
        },
    ]
    r = requests.post(MACKEREL_URL, data=json.dumps(payload), headers=headers)
    print(r.status_code)
    print(r.text)


if __name__ == '__main__':
    main()
