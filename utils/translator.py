import json
from pathlib import Path


class Translator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.current_lang = 'zh'
            cls._instance.translations = {}
            cls._instance._load_translations()
        return cls._instance

    def _load_translations(self):
        translations_dir = Path(__file__).parent / 'translations'
        for lang_file in translations_dir.glob('*.json'):
            lang_code = lang_file.stem
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.translations[lang_code] = json.load(f)
            except Exception:
                self.translations[lang_code] = {}

    def tr(self, key, default=None):
        if default is None:
            default = key
        return self.translations.get(self.current_lang, {}).get(key, default)

    def set_language(self, lang):
        if lang in self.translations:
            self.current_lang = lang
            return True
        return False

    def get_language(self):
        return self.current_lang

    def get_available_languages(self):
        return list(self.translations.keys())

    def reload(self):
        self.translations.clear()
        self._load_translations()


def tr(key, default=None):
    return Translator().tr(key, default)
