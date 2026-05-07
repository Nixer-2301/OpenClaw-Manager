# Openclaw Manager

一个用于管理Openclaw配置、Skills、模型和插件的Windows桌面应用程序。

## 功能特性

### Skills管理
- 扫描用户和系统Skills
- 查看Skill详情（元数据、SKILL.md内容）
- 启用/禁用、删除、导入/导出
- 批量操作（启用、禁用、删除、导出）
- 拖拽ZIP文件导入
- 内置SKILL.md编辑器（YAML高亮、实时预览）
- 右键菜单增强

### 配置文件管理
- JSON编辑器（语法高亮）
- 树形视图（可视化编辑）
- 配置验证、备份/恢复
- JSON格式化

### 模型管理
- 查看、添加、编辑、删除模型
- 测试模型连接
- 发送测试请求
- 右键菜单（复制ID、复制URL）

### 插件管理
- 查看、启用/禁用插件
- 批量操作
- 右键菜单增强

### 进程管理
- 启动/停止/重启Openclaw
- 查看进程状态（PID、运行时间）
- 查看配置信息（端口、绑定、认证）
- 查看进程日志
- 自动刷新状态
- **端口扫描检测外部进程**（新增）
- **多格式日志读取**（新增：支持.log、.jsonl、.json）

### 会话监控
- 连接Openclaw Gateway API
- 查看会话列表
- 查看会话消息历史
- 连接测试、自动刷新

### 日志查看器
- 日志文件列表
- 级别过滤（INFO、WARN、ERROR、DEBUG）
- 关键词搜索
- 自动刷新

### 数据统计
- 概览卡片（会话数、Skills数、模型数）
- 每日会话趋势图（折线图）
- 每日数据表格
- 时间范围选择
- 导出统计报告

### 配置模板系统
- 预设模板（DeepSeek、Xiaomi Mimo、OpenAI）
- 一键应用模板
- 模板预览

### 设置管理
- 常规设置（默认标签页、自动刷新、确认对话框）
- 路径设置（Openclaw目录、Skills目录、备份目录）
- 界面设置（主题、字体大小、行高）
- 文件监控设置（启用、刷新间隔）

### 其他功能
- 深色/浅色主题
- 中英文界面
- 快捷键支持
- 命令面板（Ctrl+Shift+P）
- 文件监控（实时刷新）
- 启动画面（1.5秒）

## 安装要求

- Python 3.8+
- Windows 10/11

## 安装步骤

### 方式一：从源码运行

1. 克隆仓库
```bash
git clone https://github.com/yourusername/openclaw-manager.git
cd openclaw-manager
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行程序
```bash
python main.py
```

### 方式二：使用启动脚本

双击 `run.bat` 文件即可运行。

### 方式三：使用预编译EXE

下载 `release-exe/OpenclawManager.exe` 直接运行。

## 依赖包

```
PyQt6>=6.0.0
PyYAML>=6.0
watchdog>=3.0.0
```

## 使用说明

### 快捷键

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

### 右键菜单

在表格中右键点击可显示上下文菜单，提供常用操作。

### 拖拽导入

将ZIP文件拖拽到Skills列表区域可直接导入。

### 命令面板

按 `Ctrl+Shift+P` 打开命令面板，可快速执行常用操作。

## 项目结构

```
openclaw-manager/
├── main.py                      # 主程序入口
├── config.py                    # 配置
├── requirements.txt             # 依赖列表
├── run.bat                      # 启动脚本
├── core/                        # 核心模块
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
│   └── openclaw_api.py          # API客户端
├── ui/                          # 界面模块
│   ├── main_window.py           # 主窗口
│   ├── skills_tab.py            # Skills标签页
│   ├── config_tab.py            # 配置标签页
│   ├── models_tab.py            # 模型标签页
│   ├── plugins_tab.py           # 插件标签页
│   ├── settings_tab.py          # 设置标签页
│   ├── log_tab.py               # 日志标签页
│   ├── stats_tab.py             # 统计标签页
│   ├── process_tab.py           # 进程标签页
│   ├── session_tab.py           # 会话标签页
│   ├── skill_editor.py          # Skill编辑器
│   ├── model_test_dialog.py     # 模型测试对话框
│   ├── template_dialog.py       # 模板对话框
│   ├── command_palette.py       # 命令面板
│   ├── splash_screen.py         # 启动画面
│   └── widgets/                 # 自定义组件
│       └── chart_widget.py      # 图表组件
├── utils/                       # 工具模块
│   ├── file_watcher.py          # 文件监控
│   ├── translator.py            # 翻译管理器
│   └── translations/            # 翻译文件
│       ├── zh.json              # 中文
│       └── en.json              # 英文
└── resources/                   # 资源文件
    ├── styles/                  # 样式表
    │   ├── dark.qss             # 深色主题
    │   └── light.qss            # 浅色主题
    └── templates/               # 配置模板
        ├── deepseek.json        # DeepSeek模板
        ├── xiaomimimo.json      # Xiaomi Mimo模板
        └── openai.json          # OpenAI模板
```

## 配置文件位置

Openclaw配置文件位于：`~/.openclaw/openclaw.json`

Skills目录：
- 用户Skills：`~/.openclaw/skills/`
- 系统Skills：`~/AppData/Roaming/npm/node_modules/openclaw/skills/`

## 开发

### 技术栈

| 组件 | 技术 |
|------|------|
| 语言 | Python 3.x |
| GUI框架 | PyQt6 |
| 配置管理 | JSON |
| 文件监控 | watchdog |
| HTTP请求 | urllib |

### 添加新功能

1. 在 `core/` 目录创建管理器模块
2. 在 `ui/` 目录创建界面模块
3. 在 `main_window.py` 中集成新标签页
4. 更新翻译文件 `utils/translations/`

## 更新日志

### V1.1 (2026-05-07)
- 修复进程管理功能，支持检测外部启动的Openclaw进程
- 改进日志读取，支持.log、.jsonl、.json多种格式
- 添加端口扫描功能，自动检测运行中的Openclaw进程
- 更新进程状态显示，增加端口监听状态

### V1.0 (2026-05-05)
- 初始版本发布
- 完整的Skills管理功能
- 配置文件编辑器
- 模型管理和测试
- 插件管理
- 进程管理
- 会话监控
- 日志查看器
- 数据统计
- 深色/浅色主题
- 中英文界面

## 许可证

本项目采用 [GNU General Public License v3.0](LICENSE) 开源许可证。

这意味着您可以自由地：
- 使用、复制、分发本软件
- 修改本软件并分发修改后的版本
- 将本软件用于商业用途

但您必须：
- 在修改后的版本中保留相同的许可证
- 公开源代码（如果您分发修改后的版本）
- 保留版权声明和许可证通知

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题，请在GitHub上提交Issue。
