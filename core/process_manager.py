import subprocess
import json
import os
import signal
from pathlib import Path
from datetime import datetime
from config import OPENCLAW_DIR


class ProcessManager:
    def __init__(self):
        self.process = None
        self.pid = None
        self.start_time = None
        self.config_file = OPENCLAW_DIR / 'openclaw.json'

    def _get_openclaw_command(self):
        try:
            result = subprocess.run(
                ['where', 'openclaw'],
                capture_output=True,
                text=True,
                shell=True
            )
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0]
        except:
            pass
        return 'openclaw'

    def start(self):
        if self.is_running():
            return {'success': False, 'message': '进程已在运行中'}

        try:
            cmd = self._get_openclaw_command()
            self.process = subprocess.Popen(
                [cmd, 'start'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            self.pid = self.process.pid
            self.start_time = datetime.now()
            return {'success': True, 'message': f'进程已启动 PID: {self.pid}'}
        except Exception as e:
            return {'success': False, 'message': f'启动失败: {str(e)}'}

    def stop(self):
        if not self.is_running():
            return {'success': False, 'message': '进程未运行'}

        try:
            if os.name == 'nt':
                subprocess.run(['taskkill', '/F', '/PID', str(self.pid)], capture_output=True)
            else:
                os.kill(self.pid, signal.SIGTERM)

            self.process = None
            self.pid = None
            self.start_time = None
            return {'success': True, 'message': '进程已停止'}
        except Exception as e:
            return {'success': False, 'message': f'停止失败: {str(e)}'}

    def restart(self):
        stop_result = self.stop()
        if not stop_result['success'] and '未运行' not in stop_result['message']:
            return stop_result

        import time
        time.sleep(1)

        return self.start()

    def is_running(self):
        if self.process is not None:
            poll = self.process.poll()
            if poll is None:
                return True
            else:
                self.process = None
                self.pid = None
                self.start_time = None
                return False

        if self.pid:
            try:
                if os.name == 'nt':
                    result = subprocess.run(
                        ['tasklist', '/FI', f'PID eq {self.pid}'],
                        capture_output=True,
                        text=True
                    )
                    return str(self.pid) in result.stdout
                else:
                    os.kill(self.pid, 0)
                    return True
            except:
                self.pid = None
                self.start_time = None
                return False

        return False

    def get_status(self):
        running = self.is_running()
        status = {
            'running': running,
            'pid': self.pid if running else None,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'uptime': None
        }

        if running and self.start_time:
            delta = datetime.now() - self.start_time
            hours, remainder = divmod(int(delta.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            status['uptime'] = f'{hours}h {minutes}m {seconds}s'

        return status

    def get_config(self):
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                gateway = config.get('gateway', {})
                return {
                    'port': gateway.get('port', 18789),
                    'bind': gateway.get('bind', 'loopback'),
                    'auth_mode': gateway.get('auth', {}).get('mode', 'token'),
                    'mode': gateway.get('mode', 'local')
                }
        except:
            return {
                'port': 18789,
                'bind': 'loopback',
                'auth_mode': 'token',
                'mode': 'local'
            }

    def get_logs(self, lines=100):
        log_dir = OPENCLAW_DIR / 'logs'
        log_files = sorted(log_dir.glob('*.log'), reverse=True) if log_dir.exists() else []

        if not log_files:
            return []

        try:
            with open(log_files[0], 'r', encoding='utf-8', errors='ignore') as f:
                all_lines = f.readlines()
                return all_lines[-lines:]
        except:
            return []
