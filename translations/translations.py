from flask import session
import json
import os

available_langs = ('ru', 'by')
default_lang = 'ru'

def get_translation():
    lang = session.get('lang', default_lang)
    if lang not in available_langs:
        lang = default_lang

    base_dir = os.path.dirname(__file__)   
    path = os.path.join(base_dir, '..', 'translations', f'{lang}.json')

    with open(path, encoding='utf-8') as f:
        return json.load(f), lang  #load преобразует строку в формате JSON в объект Python