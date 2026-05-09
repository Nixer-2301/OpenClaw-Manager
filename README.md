# OpenClaw Manager

OpenClaw 管理器的 Tauri/Vue 3 重构版本。

## 技术栈

| 层 | 技术 |
|----|------|
| 前端 | Vue 3 + TypeScript + Tailwind CSS |
| 后端 | Python 3 + FastAPI |
| 构建 | Vite + PyInstaller |

## 项目结构

```
├── src/                  # Vue 3 前端源码
│   ├── views/            # 页面组件
│   ├── components/       # UI 组件
│   ├── stores/           # Pinia 状态管理
│   ├── api/              # API 客户端
│   ├── composables/      # 组合式函数 (i18n)
│   └── assets/           # 样式资源
├── python-backend/       # FastAPI 后端
│   ├── api/              # API 路由
│   └── core/             # 核心业务逻辑
├── src-tauri/            # Tauri 配置 (备用)
├── app.py                # 主入口 (FastAPI + 静态服务)
├── config.py             # 路径常量
└── dist/                 # Vite 构建输出
```

## 开发

### 环境要求

- Node.js 20+
- Python 3.10+

### 前端开发

```bash
npm install
npm run dev          # Vite 开发服务器 (localhost:1420)
npm run build        # 生产构建
```

### 后端

```bash
cd python-backend
pip install fastapi uvicorn
python -m uvicorn main:app --reload
```

### 打包

```bash
cd release-build
pyinstaller --onefile --windowed --name "OpenClawManager" ^
  --add-data "dist-files;dist" ^
  --add-data "python-backend;python-backend" ^
  --add-data "config.py;." ^
  --hidden-import=uvicorn.logging ^
  --hidden-import=uvicorn.loops ^
  --hidden-import=uvicorn.loops.auto ^
  app.py
```

## 功能

- Skills 管理 (扫描/启用/禁用/导入/导出)
- 模型管理 (查看/添加/删除)
- 插件管理 (启用/禁用)
- 进程管理 (启动/停止/重启/状态监控)
- 会话监控 (Gateway API 连接)
- 日志查看器 (多格式支持)
- 数据统计 (每日趋势)
- 配置编辑器 (JSON/验证/备份)
- 设置管理 (主题/语言/路径/文件监控)
- 深色/浅色主题
- 中英文双语

## 版本

v1.2.0 — 2026-05-08

## 许可证

GNU General Public License v3.0
