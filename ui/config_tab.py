import json
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QComboBox, QMessageBox, QSplitter,
    QTreeWidget, QTreeWidgetItem, QTextEdit, QInputDialog,
    QMenu, QDialog, QLineEdit, QFormLayout, QDialogButtonBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QTextCharFormat, QSyntaxHighlighter, QAction

from core.config_manager import ConfigManager


class JsonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlightingRules = []

        stringFormat = QTextCharFormat()
        stringFormat.setForeground(QColor('#ce9178'))
        self.highlightingRules.append((r'"[^"]*"', stringFormat))

        numberFormat = QTextCharFormat()
        numberFormat.setForeground(QColor('#b5cea8'))
        self.highlightingRules.append((r'\b\d+\.?\d*\b', numberFormat))

        boolFormat = QTextCharFormat()
        boolFormat.setForeground(QColor('#569cd6'))
        self.highlightingRules.append((r'\b(true|false|null)\b', boolFormat))

    def highlightBlock(self, text):
        import re
        for pattern, fmt in self.highlightingRules:
            for match in re.finditer(pattern, text):
                start = match.start()
                length = match.end() - start
                self.setFormat(start, length, fmt)


class EditValueDialog(QDialog):
    def __init__(self, key, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f'编辑值 - {key}')
        self.setMinimumWidth(400)

        layout = QFormLayout(self)

        self.key_label = QLabel(key)
        layout.addRow('键:', self.key_label)

        self.value_edit = QLineEdit(str(value))
        layout.addRow('值:', self.value_edit)

        self.type_label = QLabel(type(value).__name__)
        layout.addRow('类型:', self.type_label)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)

    def get_value(self):
        text = self.value_edit.text()
        original_type = self.type_label.text()

        if original_type == 'bool':
            return text.lower() in ('true', '1', 'yes')
        elif original_type == 'int':
            try:
                return int(text)
            except ValueError:
                return text
        elif original_type == 'float':
            try:
                return float(text)
            except ValueError:
                return text
        return text


class ConfigTab(QWidget):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.config_data = None
        self._initUI()
        self._loadConfig()

    def _initUI(self):
        layout = QVBoxLayout(self)

        toolbar_layout = QHBoxLayout()

        self.save_btn = QPushButton('保存')
        self.save_btn.clicked.connect(self._onSave)
        toolbar_layout.addWidget(self.save_btn)

        self.reload_btn = QPushButton('重新加载')
        self.reload_btn.clicked.connect(self._loadConfig)
        toolbar_layout.addWidget(self.reload_btn)

        self.validate_btn = QPushButton('验证')
        self.validate_btn.clicked.connect(self._onValidate)
        toolbar_layout.addWidget(self.validate_btn)

        self.backup_btn = QPushButton('备份')
        self.backup_btn.clicked.connect(self._onBackup)
        toolbar_layout.addWidget(self.backup_btn)

        self.format_btn = QPushButton('格式化')
        self.format_btn.clicked.connect(self._onFormat)
        toolbar_layout.addWidget(self.format_btn)

        toolbar_layout.addStretch()

        view_label = QLabel('视图:')
        toolbar_layout.addWidget(view_label)

        self.view_combo = QComboBox()
        self.view_combo.addItems(['代码视图', '树形视图'])
        self.view_combo.currentTextChanged.connect(self._onViewChanged)
        toolbar_layout.addWidget(self.view_combo)

        layout.addLayout(toolbar_layout)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        self.code_editor = QTextEdit()
        self.code_editor.setFont(QFont('Consolas', 10))
        self.highlighter = JsonHighlighter(self.code_editor.document())

        self.tree_view = QTreeWidget()
        self.tree_view.setHeaderLabels(['键', '值', '类型'])
        self.tree_view.setColumnWidth(0, 250)
        self.tree_view.setColumnWidth(1, 400)
        self.tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self._onTreeContextMenu)
        self.tree_view.itemDoubleClicked.connect(self._onItemDoubleClicked)

        self.splitter.addWidget(self.code_editor)
        self.splitter.addWidget(self.tree_view)
        self.splitter.setSizes([600, 400])

        layout.addWidget(self.splitter)

        self.status_label = QLabel('就绪')
        layout.addWidget(self.status_label)

        self.tree_view.hide()

    def _loadConfig(self):
        config_content = self.config_manager.read_config()
        if config_content:
            self.code_editor.setPlainText(config_content)
            try:
                self.config_data = json.loads(config_content)
            except json.JSONDecodeError:
                self.config_data = None
            self._updateTreeView(config_content)
            self.status_label.setText('配置已加载')
        else:
            self.status_label.setText('无法加载配置文件')

    def _updateTreeView(self, json_content):
        self.tree_view.clear()
        try:
            data = json.loads(json_content)
            self._addTreeItems(self.tree_view.invisibleRootItem(), data)
            self.tree_view.expandAll()
        except json.JSONDecodeError:
            pass

    def _addTreeItems(self, parent, data, path=''):
        if isinstance(data, dict):
            for k, v in data.items():
                item = QTreeWidgetItem(parent)
                item.setText(0, str(k))
                item.setText(2, type(v).__name__)
                item.setData(0, Qt.ItemDataRole.UserRole, f'{path}.{k}' if path else k)
                self._addTreeItems(item, v, f'{path}.{k}' if path else k)
        elif isinstance(data, list):
            for i, v in enumerate(data):
                item = QTreeWidgetItem(parent)
                item.setText(0, f'[{i}]')
                item.setText(2, type(v).__name__)
                item.setData(0, Qt.ItemDataRole.UserRole, f'{path}[{i}]')
                self._addTreeItems(item, v, f'{path}[{i}]')
        else:
            parent.setText(1, str(data))

    def _onTreeContextMenu(self, position):
        item = self.tree_view.itemAt(position)
        if not item:
            return

        menu = QMenu()

        if item.text(2) in ('dict', 'list'):
            add_action = QAction('添加子项', self)
            add_action.triggered.connect(lambda: self._onAddChild(item))
            menu.addAction(add_action)

        if item.text(1):
            edit_action = QAction('编辑值', self)
            edit_action.triggered.connect(lambda: self._onEditValue(item))
            menu.addAction(edit_action)

        if item.parent():
            delete_action = QAction('删除', self)
            delete_action.triggered.connect(lambda: self._onDeleteItem(item))
            menu.addAction(delete_action)

        menu.exec(self.tree_view.viewport().mapToGlobal(position))

    def _onItemDoubleClicked(self, item, column):
        if item.text(1):
            self._onEditValue(item)

    def _onEditValue(self, item):
        key = item.text(0)
        old_value = item.text(1)

        dialog = EditValueDialog(key, old_value, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_value = dialog.get_value()
            item.setText(1, str(new_value))

            self._syncTreeToCode()

    def _onAddChild(self, parent_item):
        key, ok = QInputDialog.getText(self, '添加子项', '键名:')
        if ok and key:
            item = QTreeWidgetItem(parent_item)
            item.setText(0, key)
            item.setText(1, 'null')
            item.setText(2, 'NoneType')

            parent_item.setExpanded(True)
            self._syncTreeToCode()

    def _onDeleteItem(self, item):
        parent = item.parent()
        if parent:
            index = parent.indexOfChild(item)
            parent.takeChild(index)
            self._syncTreeToCode()

    def _syncTreeToCode(self):
        data = self._treeToDict(self.tree_view.invisibleRootItem())
        formatted = json.dumps(data, indent=2, ensure_ascii=False)
        self.code_editor.setPlainText(formatted)
        self.config_data = data

    def _treeToDict(self, parent):
        result = {}
        for i in range(parent.childCount()):
            child = parent.child(i)
            key = child.text(0)

            if child.text(2) == 'dict':
                value = self._treeToDict(child)
            elif child.text(2) == 'list':
                value = self._treeToList(child)
            else:
                value_str = child.text(1)
                if value_str == 'true':
                    value = True
                elif value_str == 'false':
                    value = False
                elif value_str == 'null':
                    value = None
                else:
                    try:
                        value = int(value_str)
                    except ValueError:
                        try:
                            value = float(value_str)
                        except ValueError:
                            value = value_str

            if key.startswith('[') and key.endswith(']'):
                key = key[1:-1]

            result[key] = value

        return result

    def _treeToList(self, parent):
        result = []
        for i in range(parent.childCount()):
            child = parent.child(i)
            if child.text(2) == 'dict':
                result.append(self._treeToDict(child))
            elif child.text(2) == 'list':
                result.append(self._treeToList(child))
            else:
                value_str = child.text(1)
                if value_str == 'true':
                    result.append(True)
                elif value_str == 'false':
                    result.append(False)
                elif value_str == 'null':
                    result.append(None)
                else:
                    try:
                        result.append(int(value_str))
                    except ValueError:
                        try:
                            result.append(float(value_str))
                        except ValueError:
                            result.append(value_str)
        return result

    def _onSave(self):
        content = self.code_editor.toPlainText()
        success = self.config_manager.save_config(content)
        if success:
            self.status_label.setText('配置已保存')
            QMessageBox.information(self, '成功', '配置已保存')
        else:
            QMessageBox.critical(self, '错误', '保存配置失败')

    def _onValidate(self):
        content = self.code_editor.toPlainText()
        is_valid, message = self.config_manager.validate_config(content)
        if is_valid:
            QMessageBox.information(self, '验证通过', '配置文件格式正确')
        else:
            QMessageBox.warning(self, '验证失败', f'配置文件错误:\n{message}')

    def _onBackup(self):
        success = self.config_manager.create_backup()
        if success:
            QMessageBox.information(self, '成功', '备份已创建')
        else:
            QMessageBox.critical(self, '错误', '创建备份失败')

    def _onFormat(self):
        content = self.code_editor.toPlainText()
        try:
            data = json.loads(content)
            formatted = json.dumps(data, indent=2, ensure_ascii=False)
            self.code_editor.setPlainText(formatted)
            self.status_label.setText('已格式化')
        except json.JSONDecodeError as e:
            QMessageBox.warning(self, '格式化失败', f'JSON格式错误:\n{str(e)}')

    def _onViewChanged(self, view_text):
        if view_text == '代码视图':
            self.code_editor.show()
            self.tree_view.hide()
        else:
            self.code_editor.hide()
            self.tree_view.show()
            content = self.code_editor.toPlainText()
            self._updateTreeView(content)

    def save(self):
        self._onSave()

    def refresh(self):
        self._loadConfig()
