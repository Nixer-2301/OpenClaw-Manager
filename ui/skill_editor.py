from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QSplitter,
    QTextEdit, QPushButton, QLabel, QGroupBox,
    QFormLayout, QLineEdit, QCheckBox, QMessageBox,
    QFileDialog, QTabWidget, QWidget
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor, QTextCharFormat, QSyntaxHighlighter

import re
import yaml


class YamlHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlightingRules = []

        keyFormat = QTextCharFormat()
        keyFormat.setForeground(QColor('#569cd6'))
        self.highlightingRules.append((r'^[\w\-]+:', keyFormat))

        stringFormat = QTextCharFormat()
        stringFormat.setForeground(QColor('#ce9178'))
        self.highlightingRules.append((r'"[^"]*"', stringFormat))
        self.highlightingRules.append((r"'[^']*'", stringFormat))

        commentFormat = QTextCharFormat()
        commentFormat.setForeground(QColor('#6a9955'))
        self.highlightingRules.append((r'#[^\n]*', commentFormat))

        numberFormat = QTextCharFormat()
        numberFormat.setForeground(QColor('#b5cea8'))
        self.highlightingRules.append((r'\b\d+\.?\d*\b', numberFormat))

        boolFormat = QTextCharFormat()
        boolFormat.setForeground(QColor('#569cd6'))
        self.highlightingRules.append((r'\b(true|false|null|yes|no)\b', boolFormat))

        separatorFormat = QTextCharFormat()
        separatorFormat.setForeground(QColor('#d4d4d4'))
        self.highlightingRules.append((r'^---$', separatorFormat))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlightingRules:
            for match in re.finditer(pattern, text, re.MULTILINE):
                start = match.start()
                length = match.end() - start
                self.setFormat(start, length, fmt)


class SkillEditorDialog(QDialog):
    def __init__(self, parent=None, skill_path=None):
        super().__init__(parent)
        self.skill_path = skill_path
        self.modified = False
        self.setWindowTitle('Skill编辑器')
        self.setMinimumSize(900, 700)
        self._initUI()
        if skill_path:
            self._loadSkill()

    def _initUI(self):
        layout = QVBoxLayout(self)

        toolbar_layout = QHBoxLayout()

        self.save_btn = QPushButton('保存')
        self.save_btn.setShortcut('Ctrl+S')
        self.save_btn.clicked.connect(self._onSave)
        toolbar_layout.addWidget(self.save_btn)

        self.reload_btn = QPushButton('重新加载')
        self.reload_btn.clicked.connect(self._onReload)
        toolbar_layout.addWidget(self.reload_btn)

        toolbar_layout.addWidget(QLabel('|'))

        self.undo_btn = QPushButton('撤销')
        self.undo_btn.setShortcut('Ctrl+Z')
        self.undo_btn.clicked.connect(self._onUndo)
        toolbar_layout.addWidget(self.undo_btn)

        self.redo_btn = QPushButton('重做')
        self.redo_btn.setShortcut('Ctrl+Y')
        self.redo_btn.clicked.connect(self._onRedo)
        toolbar_layout.addWidget(self.redo_btn)

        toolbar_layout.addStretch()

        self.file_label = QLabel('未打开文件')
        toolbar_layout.addWidget(self.file_label)

        layout.addLayout(toolbar_layout)

        self.tab_widget = QTabWidget()

        editor_tab = QWidget()
        editor_layout = QVBoxLayout(editor_tab)

        self.editor = QTextEdit()
        self.editor.setFont(QFont('Consolas', 11))
        self.highlighter = YamlHighlighter(self.editor.document())
        self.editor.textChanged.connect(self._onTextChanged)
        editor_layout.addWidget(self.editor)

        self.tab_widget.addTab(editor_tab, '编辑器')

        preview_tab = QWidget()
        preview_layout = QVBoxLayout(preview_tab)

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setFont(QFont('Consolas', 11))
        preview_layout.addWidget(self.preview)

        self.tab_widget.addTab(preview_tab, '预览')

        metadata_tab = QWidget()
        metadata_layout = QFormLayout(metadata_tab)

        self.name_input = QLineEdit()
        metadata_layout.addRow('名称:', self.name_input)

        self.description_input = QLineEdit()
        metadata_layout.addRow('描述:', self.description_input)

        self.version_input = QLineEdit()
        metadata_layout.addRow('版本:', self.version_input)

        self.user_invocable_cb = QCheckBox('用户可调用')
        metadata_layout.addRow('可调用:', self.user_invocable_cb)

        self.argument_hint_input = QLineEdit()
        metadata_layout.addRow('参数提示:', self.argument_hint_input)

        self.allowed_tools_input = QLineEdit()
        metadata_layout.addRow('允许的工具:', self.allowed_tools_input)

        self.apply_metadata_btn = QPushButton('应用元数据到编辑器')
        self.apply_metadata_btn.clicked.connect(self._onApplyMetadata)
        metadata_layout.addRow(self.apply_metadata_btn)

        self.tab_widget.addTab(metadata_tab, '元数据')

        layout.addWidget(self.tab_widget)

        self.status_label = QLabel('就绪')
        layout.addWidget(self.status_label)

        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self._autoSave)
        self.auto_save_timer.start(30000)

    def _loadSkill(self):
        try:
            with open(self.skill_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.editor.setPlainText(content)
            self._updatePreview()
            self._parseMetadata(content)
            self.file_label.setText(self.skill_path)
            self.modified = False
            self.status_label.setText('已加载')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'加载文件失败: {str(e)}')

    def _parseMetadata(self, content):
        pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(pattern, content, re.DOTALL)
        if match:
            try:
                metadata = yaml.safe_load(match.group(1))
                if metadata:
                    self.name_input.setText(metadata.get('name', ''))
                    self.description_input.setText(metadata.get('description', ''))
                    self.version_input.setText(metadata.get('version', ''))
                    self.user_invocable_cb.setChecked(metadata.get('user-invocable', False))
                    self.argument_hint_input.setText(metadata.get('argument-hint', ''))
                    allowed_tools = metadata.get('allowed-tools', '')
                    if isinstance(allowed_tools, list):
                        allowed_tools = ', '.join(allowed_tools)
                    self.allowed_tools_input.setText(str(allowed_tools))
            except:
                pass

    def _onApplyMetadata(self):
        name = self.name_input.text()
        description = self.description_input.text()
        version = self.version_input.text()
        user_invocable = self.user_invocable_cb.isChecked()
        argument_hint = self.argument_hint_input.text()
        allowed_tools = self.allowed_tools_input.text()

        metadata = {
            'name': name,
            'description': description,
            'version': version,
            'user-invocable': user_invocable
        }

        if argument_hint:
            metadata['argument-hint'] = argument_hint

        if allowed_tools:
            tools_list = [t.strip() for t in allowed_tools.split(',')]
            metadata['allowed-tools'] = tools_list

        yaml_content = yaml.dump(metadata, default_flow_style=False, allow_unicode=True)

        content = self.editor.toPlainText()
        pattern = r'^---\s*\n.*?\n---\s*\n'
        if re.match(pattern, content, re.DOTALL):
            new_content = re.sub(pattern, f'---\n{yaml_content}---\n', content, flags=re.DOTALL)
        else:
            new_content = f'---\n{yaml_content}---\n\n{content}'

        self.editor.setPlainText(new_content)
        self.status_label.setText('元数据已应用')

    def _onTextChanged(self):
        self.modified = True
        self._updatePreview()

    def _updatePreview(self):
        content = self.editor.toPlainText()
        self.preview.setPlainText(content)

    def _onSave(self):
        if not self.skill_path:
            file_path, _ = QFileDialog.getSaveFileName(
                self, '保存Skill', '', 'SKILL.md (SKILL.md);;所有文件 (*)'
            )
            if not file_path:
                return
            self.skill_path = file_path

        try:
            content = self.editor.toPlainText()
            with open(self.skill_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.modified = False
            self.file_label.setText(self.skill_path)
            self.status_label.setText('已保存')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'保存文件失败: {str(e)}')

    def _onReload(self):
        if self.skill_path and self.modified:
            reply = QMessageBox.question(
                self, '确认重新加载',
                '文件已修改，重新加载将丢失未保存的更改。确定要重新加载吗？',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        if self.skill_path:
            self._loadSkill()

    def _onUndo(self):
        self.editor.undo()

    def _onRedo(self):
        self.editor.redo()

    def _autoSave(self):
        if self.skill_path and self.modified:
            try:
                content = self.editor.toPlainText()
                with open(self.skill_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.status_label.setText('自动保存完成')
            except:
                pass

    def closeEvent(self, event):
        if self.modified:
            reply = QMessageBox.question(
                self, '确认关闭',
                '文件已修改但未保存。确定要关闭吗？',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                event.ignore()
                return

        self.auto_save_timer.stop()
        event.accept()
