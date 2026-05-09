# OpenClaw Manager

### 一款用于管理OpenClaw的GUI管理器, 可用于代替OpenClaw原版的WebUI界面, 支持中英语言. 

开发环境

[![Node.JS 20+](https://img.shields.io/badge/Node.JS-20+-green)](https://nodejs.org/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green?logo=python&logoColor=white)](http://www.python.org)

辅助AI模型及工具

[![Xiaomi MiMo V2.5 Pro](https://img.shields.io/badge/Xiaomi%20MiMo-V2.5%20Pro-blue?logo=xiaomi&logoColor=white)](https://mimo.mi.com/)
<a href="https://www.deepseek.com/" target="_blank">
    <img alt="DeepSeek" src="https://github.com/deepseek-ai/DeepSeek-OCR-2/blob/main/assets/badge.svg?raw=true" />
<a href="https://opencode.ai" target="_blank">

[![OpenClaw Manager](https://img.shields.io/badge/OpenCode-HomePage-blue?logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB2ZXJzaW9uPSIxLjEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgd2lkdGg9IjQ4IiBoZWlnaHQ9IjQ4Ij4KPHBhdGggZD0iTTAgMCBDMTUuODQgMCAzMS42OCAwIDQ4IDAgQzQ4IDE1Ljg0IDQ4IDMxLjY4IDQ4IDQ4IEMzMi4xNiA0OCAxNi4zMiA0OCAwIDQ4IEMwIDMyLjE2IDAgMTYuMzIgMCAwIFogIiBmaWxsPSIjMTMxMDEwIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgwLDApIi8+CjxwYXRoIGQ9Ik0wIDAgQzcuOTIgMCAxNS44NCAwIDI0IDAgQzI0IDkuOSAyNCAxOS44IDI0IDMwIEMxNi4wOCAzMCA4LjE2IDMwIDAgMzAgQzAgMjAuMSAwIDEwLjIgMCAwIFogIiBmaWxsPSIjRkZGRkZGIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgxMiw5KSIvPgo8cGF0aCBkPSJNMCAwIEMzLjk2IDAgNy45MiAwIDEyIDAgQzEyIDUuOTQgMTIgMTEuODggMTIgMTggQzguMDQgMTggNC4wOCAxOCAwIDE4IEMwIDEyLjA2IDAgNi4xMiAwIDAgWiAiIGZpbGw9IiM1QTU4NTgiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDE4LDE1KSIvPgo8cGF0aCBkPSJNMCAwIEMzLjk2IDAgNy45MiAwIDEyIDAgQzEyIDEuOTggMTIgMy45NiAxMiA2IEM4LjA0IDYgNC4wOCA2IDAgNiBDMCA0LjAyIDAgMi4wNCAwIDAgWiAiIGZpbGw9IiMxMzEwMTAiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDE4LDE1KSIvPgo8L3N2Zz4K&logoColor=white)](https://github.com/Nixer-2301/OpenClaw-Manager)
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
