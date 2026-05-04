from pathlib import Path

# Openclaw目录路径
OPENCLAW_DIR = Path.home() / '.openclaw'
USER_SKILLS_DIR = OPENCLAW_DIR / 'skills'
SYSTEM_SKILLS_DIR = Path.home() / 'AppData' / 'Roaming' / 'npm' / 'node_modules' / 'openclaw' / 'skills'
CONFIG_FILE = OPENCLAW_DIR / 'openclaw.json'
PLUGINS_DIR = OPENCLAW_DIR / 'plugins'
EXTENSIONS_DIR = OPENCLAW_DIR / 'extensions'

# 应用配置
APP_NAME = "Openclaw Manager"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# 支持的文件编码
DEFAULT_ENCODING = 'utf-8'
