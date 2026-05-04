import json
import time
import urllib.request
import urllib.error


class ModelTester:
    def __init__(self):
        self.timeout = 30

    def test_connection(self, base_url, api_key=None):
        start_time = time.time()
        try:
            url = f"{base_url}/models"
            headers = {'Content-Type': 'application/json'}
            if api_key:
                headers['Authorization'] = f'Bearer {api_key}'

            req = urllib.request.Request(url, headers=headers, method='GET')
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                elapsed = time.time() - start_time
                return {
                    'success': True,
                    'status_code': response.status,
                    'elapsed': round(elapsed * 1000, 2),
                    'message': 'Connection successful'
                }
        except urllib.error.HTTPError as e:
            elapsed = time.time() - start_time
            return {
                'success': False,
                'status_code': e.code,
                'elapsed': round(elapsed * 1000, 2),
                'message': f'HTTP Error: {e.code} {e.reason}'
            }
        except urllib.error.URLError as e:
            elapsed = time.time() - start_time
            return {
                'success': False,
                'status_code': None,
                'elapsed': round(elapsed * 1000, 2),
                'message': f'Connection failed: {str(e.reason)}'
            }
        except Exception as e:
            elapsed = time.time() - start_time
            return {
                'success': False,
                'status_code': None,
                'elapsed': round(elapsed * 1000, 2),
                'message': f'Error: {str(e)}'
            }

    def send_test_request(self, base_url, api_key, model_id, prompt="Hello, please respond with 'OK' to confirm you are working."):
        start_time = time.time()
        try:
            url = f"{base_url}/chat/completions"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }

            data = {
                'model': model_id,
                'messages': [
                    {'role': 'user', 'content': prompt}
                ],
                'max_tokens': 100
            }

            req = urllib.request.Request(
                url,
                headers=headers,
                data=json.dumps(data).encode('utf-8'),
                method='POST'
            )

            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                elapsed = time.time() - start_time
                result = json.loads(response.read().decode('utf-8'))

                content = ''
                if 'choices' in result and len(result['choices']) > 0:
                    message = result['choices'][0].get('message', {})
                    content = message.get('content', '')

                usage = result.get('usage', {})

                return {
                    'success': True,
                    'elapsed': round(elapsed * 1000, 2),
                    'content': content,
                    'input_tokens': usage.get('prompt_tokens', 0),
                    'output_tokens': usage.get('completion_tokens', 0),
                    'total_tokens': usage.get('total_tokens', 0),
                    'model': result.get('model', model_id),
                    'message': 'Request successful'
                }
        except urllib.error.HTTPError as e:
            elapsed = time.time() - start_time
            error_body = ''
            try:
                error_body = e.read().decode('utf-8')
            except:
                pass
            return {
                'success': False,
                'elapsed': round(elapsed * 1000, 2),
                'message': f'HTTP Error: {e.code} {e.reason}\n{error_body}'
            }
        except Exception as e:
            elapsed = time.time() - start_time
            return {
                'success': False,
                'elapsed': round(elapsed * 1000, 2),
                'message': f'Error: {str(e)}'
            }
