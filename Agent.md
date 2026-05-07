# Openclaw Manager - Agent文档

## 项目概述

**Openclaw Manager** 是一个用于管理Openclaw配置、Skills、模型和插件的Windows桌面应用程序。

- **版本**: 1.0
- **许可证**: GPL v3
- **技术栈**: Python 3.14 + PyQt6
- **位置**: `C:\Users\Administrator\openclaw-manager\`

---

## 目录结构

```
openclaw-manager/
├── main.py                      # 主程序入口（含启动画面、DPI支持）
├── config.py                    # 配置常量
├── requirements.txt             # 依赖列表
├── run.bat                      # 启动脚本
├── build.bat                    # 打包脚本
├── list.md                      # 已知问题清单
├── Agent.md                     # 本文档
│
├── core/                        # 核心模块（11个）
│   ├── skill_manager.py         # Skills管理器
│   ├── config_manager.py        # 配置管理器
│   ├── model_manager.py         # 模型管理器
│   ├── plugin_manager.py        # 插件管理器
│   ├── settings_manager.py      # 设置管理器
│   ├── template_manager.py      # 模板管理器
│   ├── log_manager.py           # 日志管理器
│   ├── stats_manager.py         # 统计管理器
│   ├── model_tester.py          # 模型测试器
│   ├── process_manager.py       # 进程管理器
│   └── openclaw_api.py          # Openclaw API客户端
│
├── ui/                          # 界面模块（15个）
│   ├── main_window.py           # 主窗口（9个标签页）
│   ├── skills_tab.py            # Skills管理（拖拽导入、批量操作、右键菜单）
│   ├── config_tab.py            # 配置文件（JSON编辑器、树形视图编辑）
│   ├── models_tab.py            # 模型管理（测试连接、右键菜单）
│   ├── plugins_tab.py           # 插件管理（批量操作、右键菜单）
│   ├── settings_tab.py          # 设置（主题切换）
│   ├── log_tab.py               # 日志查看器
│   ├── stats_tab.py             # 数据统计（折线图）
│   ├── process_tab.py           # 进程管理
│   ├── session_tab.py           # 会话监控
│   ├── skill_editor.py          # Skill编辑器（YAML高亮）
│   ├── model_test_dialog.py     # 模型测试对话框
│   ├── template_dialog.py       # 配置模板对话框
│   ├── command_palette.py       # 命令面板（Ctrl+Shift+P）
│   ├── splash_screen.py         # 启动画面（1.5秒）
│   └── widgets/
│       └── chart_widget.py      # 图表组件（折线图、柱状图、饼图）
│
├── utils/                       # 工具模块
│   ├── file_watcher.py          # 文件监控（watchdog）
│   ├── translator.py            # 翻译管理器（单例模式）
│   └── translations/
│       ├── zh.json              # 中文翻译（133个键值）
│       └── en.json              # 英文翻译
│
├── resources/                   # 资源文件
│   ├── styles/
│   │   ├── dark.qss             # 深色主题
│   │   └── light.qss            # 浅色主题
│   └── templates/
│       ├── deepseek.json        # DeepSeek模板
│       ├── xiaomimimo.json      # Xiaomi Mimo模板
│       └── openai.json          # OpenAI模板
│
├── release/                     # 发布版源代码
├── release-exe/                 # 打包后的EXE
│   ├── OpenclawManager.exe      # 37MB
│   ├── README.md
│   └── LICENSE
└── dist/                        # PyInstaller输出
```

---

## 功能模块

### 1. Skills管理 (`skills_tab.py`)
- 扫描用户/系统Skills
- 启用/禁用、删除、导入/导出
- 批量操作（启用、禁用、删除、导出）
- 拖拽ZIP文件导入
- 内置编辑器（`skill_editor.py`）
- 右键菜单（编辑、复制、打开目录）

### 2. 配置文件管理 (`config_tab.py`)
- JSON编辑器（语法高亮）
- 树形视图（可视化编辑节点）
- 配置验证、备份/恢复、格式化

### 3. 模型管理 (`models_tab.py`)
- 添加/编辑/删除模型
- 测试连接（`model_tester.py`）
- 右键菜单（复制ID、复制URL）

### 4. 插件管理 (`plugins_tab.py`)
- 启用/禁用插件
- 批量操作
- 右键菜单

### 5. 进程管理 (`process_tab.py`)
- 启动/停止/重启Openclaw
- 查看状态、配置、日志
- **已知问题**: 启动功能有问题

### 6. 会话监控 (`session_tab.py`)
- 连接Openclaw Gateway API
- 查看会话列表、消息历史

### 7. 日志查看器 (`log_tab.py`)
- 日志文件浏览
- 级别过滤、关键词搜索

### 8. 数据统计 (`stats_tab.py`)
- 概览卡片
- 每日会话趋势图（折线图）

### 9. 设置 (`settings_tab.py`)
- 常规、路径、界面、文件监控设置
- 主题切换（深色/浅色）

### 10. 其他功能
- 启动画面（1.5秒）
- 命令面板（Ctrl+Shift+P）
- 配置模板系统
- 国际化（中英文）
- 文件监控（watchdog）
- 高DPI支持

---

## 快捷键

| 快捷键 | 功能 |
|--------|------|
| F5 | 刷新 |
| Ctrl+S | 保存 |
| Ctrl+F | 搜索 |
| Ctrl+A | 全选 |
| Ctrl+E | 启用/禁用 |
| Ctrl+Enter | 编辑Skill |
| Ctrl+Shift+E | 批量导出 |
| Ctrl+1-9 | 切换标签页 |
| Ctrl+Shift+P | 命令面板 |
| F1 | 快捷键列表 |

---

## Openclaw配置路径

| 路径 | 说明 |
|------|------|
| `~/.openclaw/openclaw.json` | 主配置文件 |
| `~/.openclaw/skills/` | 用户Skills |
| `~/AppData/Roaming/npm/node_modules/openclaw/skills/` | 系统Skills |
| `~/.openclaw/plugins/` | 插件目录 |
| `~/.openclaw/logs/` | 日志目录 |
| `~/.openclaw/agents/main/sessions/` | 会话数据 |

---

## 已知问题

见 `list.md`

---

## V1.1 更新说明

### 进程管理功能修复 (2026-05-07)

**问题描述：**
- 程序内部启动Openclaw功能存在问题，无法正常启动/停止进程
- 只能检测自己启动的进程，无法检测外部启动的Openclaw进程
- 日志读取只支持.log格式，不支持.jsonl和.json格式

**修复内容：**

1. **添加端口扫描检测外部进程**
   - 新增 `_scan_running_processes()` 方法
   - 通过 `netstat -ano` 查找监听端口18789的进程
   - 验证进程是否为node.exe（Openclaw运行时）

2. **改进进程检测逻辑**
   - 优先检查自己启动的进程
   - 如果没有，调用端口扫描检测外部进程
   - 自动更新PID信息

3. **改进日志读取功能**
   - 支持 `.log`、`.jsonl`、`.json` 三种格式
   - 新增 `_parse_log_file()` 方法
   - 自动解析不同格式的日志条目
   - 统一日志输出格式：`{timestamp, level, message}`

4. **更新进程状态显示**
   - 增加端口监听状态显示
   - 优化状态栏信息

**修改的文件：**
- `core/process_manager.py` - 核心进程管理逻辑
- `ui/process_tab.py` - 进程管理界面

**测试结果：**
- 进程检测正常：能检测到PID 27544的Openclaw进程
- 配置读取正常：端口18789，绑定loopback
- 日志读取正常：成功读取多种格式的日志文件
- 端口扫描正常：端口18789正在被监听

---

## 打包命令

```bash
cd C:\Users\Administrator\openclaw-manager\release
pyinstaller --onefile --windowed --name "OpenclawManager" --add-data "resources;resources" --add-data "utils/translations;utils/translations" main.py
```

输出: `release/dist/OpenclawManager.exe` (37MB)

---

## 依赖包

```
PyQt6>=6.0.0
PyYAML>=6.0
watchdog>=3.0.0
pyinstaller>=6.0.0
```

---

## 开发备忘

1. **添加新标签页**:
   - 在 `ui/` 创建新的 `xxx_tab.py`
   - 在 `main_window.py` 导入并添加到 `tab_widget`
   - 更新快捷键和翻译文件

2. **添加新功能模块**:
   - 在 `core/` 创建管理器
   - 在 `ui/` 创建界面
   - 更新翻译文件

3. **修改主题**:
   - 编辑 `resources/styles/dark.qss` 或 `light.qss`
   - 重启应用生效

4. **添加翻译**:
   - 编辑 `utils/translations/zh.json` 和 `en.json`
   - 使用 `tr('key')` 函数
