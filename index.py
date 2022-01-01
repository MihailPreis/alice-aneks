# coding: utf-8
from __future__ import unicode_literals
from random import seed, shuffle, randrange
import logging
import sqlite3

logging.getLogger().setLevel(logging.DEBUG)


def handler(event, context):
    response = {
        "version": event['version'],
        "session": event['session'],
        "response": {
            "end_session": False
        }
    }
    handle_dialog(event['state'], response)
    logging.debug('Response: %r', response)
    return response


def handle_dialog(state, res):
    state = state.get('user')
    if not state:
        state = {
            'seed': randrange(0, 1000),
            'last': 0
        }

    try:
        state['last'] += 1

        con = sqlite3.connect('aneks.db')
        cur = con.cursor()

        cur.execute('SELECT COUNT(*) FROM aneks')
        _ln = cur.fetchone()[0]

        seed(state['seed'], version=2)
        _list = list(range(1, _ln))
        shuffle(_list)
        _id = _list[state['last'] % len(_list)]

        cur.execute('SELECT anek FROM aneks WHERE id = :id', {'id': _id})
        res['response']['text'] = cur.fetchone()[0]

        con.close()
    except Exception as err:
        logging.error(err)
        res['response']['text'] = 'На сегодня анекдотов хватит, иди погуляй, кожанный.'

    res['user_state_update'] = state
    res['response']['end_session'] = True
