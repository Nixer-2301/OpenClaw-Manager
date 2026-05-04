import json
from pathlib import Path
from config import OPENCLAW_DIR


SETTINGS_FILE = OPENCLAW_DIR / 'manager_settings.json'

DEFAULT_SETTINGS = {
    'general': {
        'default_tab': 0,
        'auto_refresh': True,
        'confirm_delete': True,
        'confirm_batch': True
    },
    'paths': {
        'openclaw_dir': str(OPENCLAW_DIR),
        'user_skills_dir': str(OPENCLAW_DIR / 'skills'),
        'backup_dir': str(OPENCLAW_DIR / 'backups'),
        'max_backups': 10
    },
    'interface': {
        'theme': 'dark',
        'font_size': 10,
        'table_row_height': 30
    },
    'file_watcher': {
        'enabled': True,
        'refresh_interval': 5
    }
}


class SettingsManager:
    def __init__(self):
        self.settings_file = SETTINGS_FILE
        self.settings = self._load_settings()

    def _load_settings(self):
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    return self._merge_settings(DEFAULT_SETTINGS, loaded)
            except Exception:
                pass
        return DEFAULT_SETTINGS.copy()

    def _merge_settings(self, defaults, loaded):
        result = defaults.copy()
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_settings(result[key], value)
            else:
                result[key] = value
        return result

    def save_settings(self):
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def get(self, section, key=None, default=None):
        if section not in self.settings:
            return default
        if key is None:
            return self.settings[section]
        return self.settings[section].get(key, default)

    def set(self, section, key, value):
        if section not in self.settings:
            self.settings[section] = {}
        self.settings[section][key] = value

    def get_all(self):
        return self.settings.copy()

    def reset_to_defaults(self):
        self.settings = DEFAULT_SETTINGS.copy()
        return self.save_settings()

    def get_general_settings(self):
        return self.settings.get('general', {})

    def get_path_settings(self):
        return self.settings.get('paths', {})

    def get_interface_settings(self):
        return self.settings.get('interface', {})

    def get_file_watcher_settings(self):
        return self.settings.get('file_watcher', {})
