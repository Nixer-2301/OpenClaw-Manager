import json
import shutil
from datetime import datetime
from pathlib import Path
from config import CONFIG_FILE, OPENCLAW_DIR


class ConfigManager:
    def __init__(self):
        self.config_file = CONFIG_FILE
        self.backup_dir = OPENCLAW_DIR / 'backups'
        self.backup_dir.mkdir(exist_ok=True)

    def read_config(self):
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return None

    def save_config(self, content):
        try:
            json.loads(content)
            self.create_backup()
            with open(self.config_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception:
            return False

    def validate_config(self, content):
        try:
            json.loads(content)
            return True, '配置文件格式正确'
        except json.JSONDecodeError as e:
            return False, str(e)

    def create_backup(self):
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = self.backup_dir / f'openclaw_{timestamp}.json'
            shutil.copy2(self.config_file, backup_file)
            return True
        except Exception:
            return False

    def restore_backup(self, backup_file):
        try:
            shutil.copy2(backup_file, self.config_file)
            return True
        except Exception:
            return False

    def list_backups(self):
        backups = []
        if self.backup_dir.exists():
            for backup_file in self.backup_dir.glob('*.json'):
                backups.append({
                    'path': str(backup_file),
                    'name': backup_file.name,
                    'time': datetime.fromtimestamp(backup_file.stat().st_mtime)
                })
        return sorted(backups, key=lambda x: x['time'], reverse=True)
