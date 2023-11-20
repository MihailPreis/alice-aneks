# coding: utf-8
from __future__ import unicode_literals
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from tqdm import tqdm
import requests
import sqlite3

con = sqlite3.connect('aneks.db')

if __name__ == '__main__':
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS aneks
                (
                    id INTEGER PRIMARY KEY, 
                    anek text
                )
                ''')

    aneks = []
    for i in range(1, 69):
        r = requests.get(f'https://baneks.site/best/?p={i}')
        s = BeautifulSoup(r.text, 'html.parser')
        for a in tqdm(s.find_all('div', 'joke'), desc=f'Page {i}'):
            _h = a.find('div', 'card-bottom').find('div', 'actions-container').a.get('href')
            r2 = requests.get('https://baneks.site' + _h)
            s2 = BeautifulSoup(r2.text, 'html.parser')
            res = []
            for item in s2.find('article').section.p.contents:
                if item.__class__ is NavigableString:
                    res.append(str(item))
            res = "\n".join(res)
            if len(res) < 1024:
                aneks.append((len(aneks) + 1, res))

    cur.executemany("INSERT INTO aneks values (?, ?)", aneks)
    con.commit()
    con.close()
