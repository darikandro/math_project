import json
import os

from flask import session

from settings import available_langs, default_lang


def get_current_lang():
    return session.get("lang", default_lang)


def get_translation():
    lang = get_current_lang()
    if lang not in available_langs:
        lang = default_lang

    base_dir = os.path.dirname(__file__)   
    path = os.path.join(base_dir, '..', 'translations', f'{lang}.json')

    with open(path, encoding='utf-8') as f:
        return json.load(f), lang  #load преобразует строку в формате JSON в объект Python
    

def translate(key):
    t, _ = get_translation()
    return t.get(key, key)


def get_translation_db(obj, lang, fallback=default_lang): #перевод из бд
    tr = obj.translations.filter_by(lang=lang).first()

    if not tr and fallback:
        tr = obj.translations.filter_by(lang=fallback).first()

    return tr
