import re
from pathlib import Path
from datetime import datetime
from config import OPENCLAW_DIR


class LogManager:
    def __init__(self):
        self.logs_dir = OPENCLAW_DIR / 'logs'

    def get_log_files(self):
        log_files = []
        if self.logs_dir.exists():
            for log_file in sorted(self.logs_dir.glob('*.log'), reverse=True):
                log_files.append({
                    'name': log_file.name,
                    'path': str(log_file),
                    'size': log_file.stat().st_size,
                    'modified': datetime.fromtimestamp(log_file.stat().st_mtime)
                })
        return log_files

    def read_log(self, file_path, level_filter=None, keyword=None, max_lines=1000):
        lines = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f):
                    if i >= max_lines:
                        break
                    if level_filter and level_filter != 'ALL' and level_filter not in line:
                        continue
                    if keyword and keyword.lower() not in line.lower():
                        continue
                    parsed = self.parse_log_line(line)
                    if parsed:
                        lines.append(parsed)
                    else:
                        lines.append({
                            'timestamp': '',
                            'level': '',
                            'message': line.strip()
                        })
        except Exception:
            pass
        return lines

    def parse_log_line(self, line):
        patterns = [
            r'\[(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}[^\]]*)\]\s*\[(\w+)\]\s*(.*)',
            r'(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}[^\s]*)\s+(\w+)\s+(.*)',
            r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] \[(\w+)\] (.*)',
        ]

        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                return {
                    'timestamp': match.group(1),
                    'level': match.group(2).upper(),
                    'message': match.group(3).strip()
                }

        if line.strip():
            return {
                'timestamp': '',
                'level': 'INFO',
                'message': line.strip()
            }
        return None

    def get_log_stats(self, file_path):
        stats = {'INFO': 0, 'WARN': 0, 'ERROR': 0, 'DEBUG': 0, 'TOTAL': 0}
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    stats['TOTAL'] += 1
                    for level in ['INFO', 'WARN', 'ERROR', 'DEBUG']:
                        if level in line:
                            stats[level] += 1
                            break
        except Exception:
            pass
        return stats

    def clear_old_logs(self, days=30):
        if not self.logs_dir.exists():
            return 0

        cutoff = datetime.now().timestamp() - (days * 86400)
        count = 0

        for log_file in self.logs_dir.glob('*.log'):
            if log_file.stat().st_mtime < cutoff:
                try:
                    log_file.unlink()
                    count += 1
                except Exception:
                    pass

        return count
