import json
from config import CONFIG_FILE


class ModelManager:
    def __init__(self):
        self.config_file = CONFIG_FILE

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

    def get_all_models(self):
        config = self._read_config()
        models = []

        providers = config.get('models', {}).get('providers', {})
        for provider_name, provider_data in providers.items():
            for model in provider_data.get('models', []):
                models.append({
                    'provider': provider_name,
                    'id': model.get('id', ''),
                    'name': model.get('name', ''),
                    'api': model.get('api', provider_data.get('api', '')),
                    'enabled': True,
                    'base_url': provider_data.get('baseUrl', ''),
                    'context_window': model.get('contextWindow', 0),
                    'max_tokens': model.get('maxTokens', 0),
                    'reasoning': model.get('reasoning', False)
                })

        return models

    def add_model(self, model_data):
        config = self._read_config()
        providers = config.setdefault('models', {}).setdefault('providers', {})
        provider_name = model_data.get('provider', '')

        if provider_name not in providers:
            providers[provider_name] = {
                'baseUrl': model_data.get('baseUrl', ''),
                'apiKey': model_data.get('apiKey', ''),
                'api': 'openai-completions',
                'models': []
            }

        providers[provider_name]['models'].append({
            'id': model_data.get('id', ''),
            'name': model_data.get('name', ''),
            'reasoning': False,
            'input': ['text']
        })

        return self._write_config(config)

    def delete_model(self, provider, model_id):
        config = self._read_config()
        providers = config.get('models', {}).get('providers', {})

        if provider in providers:
            models = providers[provider].get('models', [])
            providers[provider]['models'] = [m for m in models if m.get('id') != model_id]
            return self._write_config(config)

        return False

    def get_providers(self):
        config = self._read_config()
        return list(config.get('models', {}).get('providers', {}).keys())
