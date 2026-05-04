import json
from pathlib import Path
from config import OPENCLAW_DIR


class TemplateManager:
    def __init__(self):
        self.templates_dir = Path(__file__).parent.parent / 'resources' / 'templates'
        self.config_file = OPENCLAW_DIR / 'openclaw.json'
        self.templates = self._load_templates()

    def _load_templates(self):
        templates = {}
        if self.templates_dir.exists():
            for template_file in self.templates_dir.glob('*.json'):
                try:
                    with open(template_file, 'r', encoding='utf-8') as f:
                        template = json.load(f)
                        templates[template.get('name', template_file.stem)] = template
                except Exception:
                    pass
        return templates

    def get_all_templates(self):
        return self.templates

    def get_template(self, name):
        return self.templates.get(name)

    def apply_template(self, template_name, api_key=None):
        template = self.templates.get(template_name)
        if not template:
            return False

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except Exception:
            config = {}

        providers = config.setdefault('models', {}).setdefault('providers', {})
        provider_name = template.get('provider', '')
        provider_config = template.get('provider_config', {}).copy()

        if api_key:
            provider_config['apiKey'] = api_key

        providers[provider_name] = provider_config

        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def save_as_template(self, provider_name, template_name, description=''):
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except Exception:
            return False

        providers = config.get('models', {}).get('providers', {})
        if provider_name not in providers:
            return False

        provider_config = providers[provider_name].copy()
        if 'apiKey' in provider_config:
            provider_config['apiKey'] = ''

        template = {
            'name': template_name,
            'description': description,
            'version': '1.0',
            'provider': provider_name,
            'provider_config': provider_config
        }

        template_file = self.templates_dir / f'{template_name.lower().replace(" ", "_")}.json'
        try:
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=2, ensure_ascii=False)
            self.templates[template_name] = template
            return True
        except Exception:
            return False

    def delete_template(self, name):
        template = self.templates.get(name)
        if not template:
            return False

        template_file = self.templates_dir / f'{name.lower().replace(" ", "_")}.json'
        try:
            if template_file.exists():
                template_file.unlink()
            del self.templates[name]
            return True
        except Exception:
            return False

    def get_template_names(self):
        return list(self.templates.keys())
