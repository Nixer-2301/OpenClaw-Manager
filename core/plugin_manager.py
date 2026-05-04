import json
from pathlib import Path
from config import CONFIG_FILE, PLUGINS_DIR, EXTENSIONS_DIR


class PluginManager:
    def __init__(self):
        self.config_file = CONFIG_FILE
        self.plugins_dir = PLUGINS_DIR
        self.extensions_dir = EXTENSIONS_DIR

    def _read_config(self):
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def _write_config(self, config):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def get_all_plugins(self):
        config = self._read_config()
        plugins = []

        plugins_config = config.get('plugins', {})
        allowed = plugins_config.get('allow', [])
        entries = plugins_config.get('entries', {})

        for plugin_name in allowed:
            enabled = entries.get(plugin_name, {}).get('enabled', False)
            plugin_info = self._get_plugin_info(plugin_name)
            plugins.append({
                'name': plugin_name,
                'description': plugin_info.get('description', ''),
                'version': plugin_info.get('version', ''),
                'enabled': enabled,
                'path': plugin_info.get('path', '')
            })

        return plugins

    def _get_plugin_info(self, plugin_name):
        info = {'description': '', 'version': '', 'path': ''}

        extension_dir = self.extensions_dir / plugin_name
        if extension_dir.exists():
            info['path'] = str(extension_dir)
            plugin_json = extension_dir / 'openclaw.plugin.json'
            if plugin_json.exists():
                try:
                    with open(plugin_json, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        info['description'] = data.get('description', '')
                        info['version'] = data.get('version', '')
                except Exception:
                    pass

        return info

    def toggle_plugin(self, plugin):
        config = self._read_config()
        entries = config.setdefault('plugins', {}).setdefault('entries', {})
        plugin_name = plugin.get('name', '')

        if plugin_name in entries:
            current = entries[plugin_name].get('enabled', False)
            entries[plugin_name]['enabled'] = not current
        else:
            entries[plugin_name] = {'enabled': True}

        return self._write_config(config)
