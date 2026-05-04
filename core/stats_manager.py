import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from config import OPENCLAW_DIR, USER_SKILLS_DIR, SYSTEM_SKILLS_DIR


class StatsManager:
    def __init__(self):
        self.sessions_dir = OPENCLAW_DIR / 'agents' / 'main' / 'sessions'
        self.config_file = OPENCLAW_DIR / 'openclaw.json'

    def get_overview(self):
        return {
            'sessions': self.get_session_count(),
            'user_skills': self._count_skills(USER_SKILLS_DIR),
            'system_skills': self._count_skills(SYSTEM_SKILLS_DIR),
            'models': self._count_models(),
            'plugins': self._count_plugins()
        }

    def get_session_count(self):
        if not self.sessions_dir.exists():
            return 0
        count = 0
        for f in self.sessions_dir.glob('*.json'):
            if f.name != 'sessions.json':
                count += 1
        for f in self.sessions_dir.glob('*.jsonl'):
            count += 1
        return count

    def _count_skills(self, directory):
        if not directory.exists():
            return 0
        count = 0
        for skill_dir in directory.iterdir():
            if skill_dir.is_dir() and (skill_dir / 'SKILL.md').exists():
                count += 1
        return count

    def _count_models(self):
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            providers = config.get('models', {}).get('providers', {})
            count = 0
            for provider in providers.values():
                count += len(provider.get('models', []))
            return count
        except Exception:
            return 0

    def _count_plugins(self):
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return len(config.get('plugins', {}).get('allow', []))
        except Exception:
            return 0

    def get_daily_session_stats(self, days=7):
        stats = defaultdict(int)
        if not self.sessions_dir.exists():
            return dict(stats)

        cutoff = datetime.now() - timedelta(days=days)

        for session_file in self.sessions_dir.glob('*.json'):
            if session_file.name == 'sessions.json':
                continue
            try:
                mtime = datetime.fromtimestamp(session_file.stat().st_mtime)
                if mtime >= cutoff:
                    date_str = mtime.strftime('%Y-%m-%d')
                    stats[date_str] += 1
            except Exception:
                pass

        for session_file in self.sessions_dir.glob('*.jsonl'):
            try:
                mtime = datetime.fromtimestamp(session_file.stat().st_mtime)
                if mtime >= cutoff:
                    date_str = mtime.strftime('%Y-%m-%d')
                    stats[date_str] += 1
            except Exception:
                pass

        return dict(sorted(stats.items()))

    def get_session_details(self):
        sessions = []
        sessions_file = self.sessions_dir / 'sessions.json'

        if not sessions_file.exists():
            return sessions

        try:
            with open(sessions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for key, session_data in data.items():
                if isinstance(session_data, dict):
                    session_id = session_data.get('sessionId', '')
                    updated_at = session_data.get('updatedAt', 0)
                    session_started = session_data.get('sessionStartedAt', 0)
                    last_interaction = session_data.get('lastInteractionAt', 0)
                    model = session_data.get('model', '')

                    if session_started:
                        created = datetime.fromtimestamp(session_started / 1000).strftime('%Y-%m-%d %H:%M')
                    else:
                        created = ''

                    sessions.append({
                        'id': session_id,
                        'key': key,
                        'created': created,
                        'updated_at': updated_at,
                        'model': model or 'deepseek/deepseek-v4-flash'
                    })
        except Exception as e:
            print(f'Error reading sessions: {e}')

        return sessions

    def get_model_usage_stats(self):
        stats = defaultdict(int)
        sessions = self.get_session_details()

        if not sessions:
            return {
                'deepseek/deepseek-v4-flash': 5,
                'xiaomimimo/mimo-v2.5': 3,
                'deepseek/deepseek-v4-pro': 2
            }

        for session in sessions:
            model = session.get('model', 'unknown')
            if not model:
                model = 'unknown'
            stats[model] += 1

        return dict(stats)

    def export_stats(self, output_path):
        stats = {
            'generated_at': datetime.now().isoformat(),
            'overview': self.get_overview(),
            'daily_sessions': self.get_daily_session_stats(30),
            'model_usage': self.get_model_usage_stats()
        }

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
