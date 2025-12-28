import json
import os

_current_lang = "pt_BR"
_translations = {}


def load_language(lang_code):
    global _current_lang, _translations
    path = os.path.join("locales", f"{lang_code}.json")

    with open(path, "r", encoding="utf-8") as f:
        _translations = json.load(f)

    _current_lang = lang_code


def t(key, **kwargs):
    text = _translations.get(key, key)
    return text.format(**kwargs)
