import json
import os
import sys

_current_lang = "pt_BR"
_translations = {}


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def load_language(lang_code):
    global _current_lang, _translations

    path = resource_path(os.path.join("locales", f"{lang_code}.json"))

    with open(path, "r", encoding="utf-8") as f:
        _translations = json.load(f)

    _current_lang = lang_code


def t(key, **kwargs):
    text = _translations.get(key, key)
    return text.format(**kwargs)
