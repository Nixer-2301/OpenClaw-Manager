import json
import urllib.request
import urllib.error
from pathlib import Path
from config import OPENCLAW_DIR


class OpenclawAPI:
    def __init__(self, base_url=None, token=None):
        if base_url is None:
            config = self._load_config()
            port = config.get('port', 18789)
            base_url = f'http://localhost:{port}'

        self.base_url = base_url.rstrip('/')
        self.token = token

        if self.token is None:
            self.token = self._load_token()

    def _load_config(self):
        config_file = OPENCLAW_DIR / 'openclaw.json'
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                gateway = config.get('gateway', {})
                return {
                    'port': gateway.get('port', 18789),
                    'bind': gateway.get('bind', 'loopback')
                }
        except:
            return {'port': 18789, 'bind': 'loopback'}

    def _load_token(self):
        config_file = OPENCLAW_DIR / 'openclaw.json'
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('gateway', {}).get('auth', {}).get('token', '')
        except:
            return ''

    def _request(self, endpoint, method='GET', data=None):
        url = f'{self.base_url}{endpoint}'
        headers = {
            'Content-Type': 'application/json'
        }

        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        try:
            if data:
                req = urllib.request.Request(
                    url,
                    headers=headers,
                    data=json.dumps(data).encode('utf-8'),
                    method=method
                )
            else:
                req = urllib.request.Request(
                    url,
                    headers=headers,
                    method=method
                )

            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                return {'success': True, 'data': result}
        except urllib.error.HTTPError as e:
            return {'success': False, 'error': f'HTTP {e.code}: {e.reason}'}
        except urllib.error.URLError as e:
            return {'success': False, 'error': f'Connection failed: {str(e.reason)}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_status(self):
        return self._request('/api/status')

    def get_sessions(self):
        return self._request('/api/sessions')

    def get_session(self, session_id):
        return self._request(f'/api/sessions/{session_id}')

    def get_session_messages(self, session_id):
        return self._request(f'/api/sessions/{session_id}/messages')

    def test_connection(self):
        result = self.get_status()
        return result.get('success', False)
