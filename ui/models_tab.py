from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLabel, QGroupBox,
    QFormLayout, QMessageBox, QHeaderView, QAbstractItemView,
    QDialog, QDialogButtonBox, QLineEdit, QCheckBox, QSpinBox,
    QMenu, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from core.model_manager import ModelManager
from ui.model_test_dialog import ModelTestDialog


class AddModelDialog(QDialog):
    def __init__(self, parent=None, model_data=None):
        super().__init__(parent)
        self.setWindowTitle('编辑模型' if model_data else '添加模型')
        self.setMinimumWidth(500)

        layout = QFormLayout(self)

        self.provider_input = QLineEdit()
        if model_data:
            self.provider_input.setText(model_data.get('provider', ''))
        layout.addRow('提供商:', self.provider_input)

        self.model_id_input = QLineEdit()
        if model_data:
            self.model_id_input.setText(model_data.get('id', ''))
        layout.addRow('模型ID:', self.model_id_input)

        self.name_input = QLineEdit()
        if model_data:
            self.name_input.setText(model_data.get('name', ''))
        layout.addRow('显示名称:', self.name_input)

        self.base_url_input = QLineEdit()
        if model_data:
            self.base_url_input.setText(model_data.get('base_url', ''))
        layout.addRow('Base URL:', self.base_url_input)

        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        if model_data:
            self.api_key_input.setText(model_data.get('api_key', ''))
        layout.addRow('API Key:', self.api_key_input)

        self.api_type_input = QLineEdit()
        self.api_type_input.setPlaceholderText('openai-completions')
        if model_data:
            self.api_type_input.setText(model_data.get('api', ''))
        layout.addRow('API类型:', self.api_type_input)

        self.context_window_input = QSpinBox()
        self.context_window_input.setRange(0, 10000000)
        self.context_window_input.setSingleStep(1000)
        if model_data:
            self.context_window_input.setValue(model_data.get('context_window', 0))
        layout.addRow('上下文窗口:', self.context_window_input)

        self.max_tokens_input = QSpinBox()
        self.max_tokens_input.setRange(0, 10000000)
        self.max_tokens_input.setSingleStep(1000)
        if model_data:
            self.max_tokens_input.setValue(model_data.get('max_tokens', 0))
        layout.addRow('最大Token:', self.max_tokens_input)

        self.reasoning_input = QCheckBox('支持推理')
        if model_data:
            self.reasoning_input.setChecked(model_data.get('reasoning', False))
        layout.addRow('推理能力:', self.reasoning_input)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)

    def get_data(self):
        return {
            'provider': self.provider_input.text(),
            'id': self.model_id_input.text(),
            'name': self.name_input.text(),
            'baseUrl': self.base_url_input.text(),
            'apiKey': self.api_key_input.text(),
            'api': self.api_type_input.text() or 'openai-completions',
            'contextWindow': self.context_window_input.value(),
            'maxTokens': self.max_tokens_input.value(),
            'reasoning': self.reasoning_input.isChecked()
        }


class ModelsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.model_manager = ModelManager()
        self.current_models = []
        self._initUI()
        self._loadModels()

    def _initUI(self):
        layout = QVBoxLayout(self)

        toolbar_layout = QHBoxLayout()

        self.add_btn = QPushButton('添加模型')
        self.add_btn.clicked.connect(self._onAdd)
        toolbar_layout.addWidget(self.add_btn)

        self.edit_btn = QPushButton('编辑')
        self.edit_btn.clicked.connect(self._onEdit)
        toolbar_layout.addWidget(self.edit_btn)

        self.delete_btn = QPushButton('删除')
        self.delete_btn.clicked.connect(self._onDelete)
        toolbar_layout.addWidget(self.delete_btn)

        self.test_btn = QPushButton('测试连接')
        self.test_btn.clicked.connect(self._onTest)
        toolbar_layout.addWidget(self.test_btn)

        toolbar_layout.addStretch()

        self.refresh_btn = QPushButton('刷新')
        self.refresh_btn.clicked.connect(self._loadModels)
        toolbar_layout.addWidget(self.refresh_btn)

        layout.addLayout(toolbar_layout)

        self.models_table = QTableWidget()
        self.models_table.setColumnCount(6)
        self.models_table.setHorizontalHeaderLabels(['提供商', '模型ID', '名称', 'API类型', '上下文窗口', '推理'])
        self.models_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.models_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.models_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.models_table.itemSelectionChanged.connect(self._onSelectionChanged)
        self.models_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.models_table.customContextMenuRequested.connect(self._showContextMenu)

        layout.addWidget(self.models_table)

        detail_group = QGroupBox('模型详情')
        detail_layout = QFormLayout(detail_group)

        self.detail_provider = QLabel()
        detail_layout.addRow('提供商:', self.detail_provider)

        self.detail_model_id = QLabel()
        detail_layout.addRow('模型ID:', self.detail_model_id)

        self.detail_name = QLabel()
        detail_layout.addRow('名称:', self.detail_name)

        self.detail_base_url = QLabel()
        detail_layout.addRow('Base URL:', self.detail_base_url)

        self.detail_api = QLabel()
        detail_layout.addRow('API类型:', self.detail_api)

        self.detail_context_window = QLabel()
        detail_layout.addRow('上下文窗口:', self.detail_context_window)

        self.detail_max_tokens = QLabel()
        detail_layout.addRow('最大Token:', self.detail_max_tokens)

        self.detail_reasoning = QLabel()
        detail_layout.addRow('推理能力:', self.detail_reasoning)

        layout.addWidget(detail_group)

        self.status_label = QLabel('就绪')
        layout.addWidget(self.status_label)

    def _loadModels(self):
        self.current_models = self.model_manager.get_all_models()
        self.models_table.setRowCount(len(self.current_models))

        for row, model in enumerate(self.current_models):
            self.models_table.setItem(row, 0, QTableWidgetItem(model.get('provider', '')))
            self.models_table.setItem(row, 1, QTableWidgetItem(model.get('id', '')))
            self.models_table.setItem(row, 2, QTableWidgetItem(model.get('name', '')))
            self.models_table.setItem(row, 3, QTableWidgetItem(model.get('api', '')))

            context_window = model.get('context_window', 0)
            self.models_table.setItem(row, 4, QTableWidgetItem(f'{context_window:,}'))

            reasoning = '是' if model.get('reasoning', False) else '否'
            self.models_table.setItem(row, 5, QTableWidgetItem(reasoning))

        self.status_label.setText(f'已加载 {len(self.current_models)} 个模型')

    def _onSelectionChanged(self):
        selected_rows = self.models_table.selectionModel().selectedRows()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        if row < len(self.current_models):
            model = self.current_models[row]
            self._showModelDetail(model)

    def _showModelDetail(self, model):
        self.detail_provider.setText(model.get('provider', ''))
        self.detail_model_id.setText(model.get('id', ''))
        self.detail_name.setText(model.get('name', ''))
        self.detail_base_url.setText(model.get('base_url', ''))
        self.detail_api.setText(model.get('api', ''))

        context_window = model.get('context_window', 0)
        self.detail_context_window.setText(f'{context_window:,}')

        max_tokens = model.get('max_tokens', 0)
        self.detail_max_tokens.setText(f'{max_tokens:,}')

        self.detail_reasoning.setText('是' if model.get('reasoning', False) else '否')

    def _showContextMenu(self, position):
        selected_rows = self.models_table.selectionModel().selectedRows()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        if row >= len(self.current_models):
            return

        model = self.current_models[row]
        menu = QMenu(self)

        edit_action = QAction('编辑', self)
        edit_action.triggered.connect(self._onEdit)
        menu.addAction(edit_action)

        test_action = QAction('测试连接', self)
        test_action.triggered.connect(self._onTest)
        menu.addAction(test_action)

        menu.addSeparator()

        copy_id_action = QAction('复制模型ID', self)
        copy_id_action.triggered.connect(lambda: self._copyToClipboard(model.get('id', '')))
        menu.addAction(copy_id_action)

        copy_url_action = QAction('复制Base URL', self)
        copy_url_action.triggered.connect(lambda: self._copyToClipboard(model.get('base_url', '')))
        menu.addAction(copy_url_action)

        menu.addSeparator()

        delete_action = QAction('删除', self)
        delete_action.triggered.connect(self._onDelete)
        menu.addAction(delete_action)

        menu.exec(self.models_table.viewport().mapToGlobal(position))

    def _copyToClipboard(self, text):
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            self.status_label.setText(f'已复制: {text}')

    def _onAdd(self):
        dialog = AddModelDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            model_data = dialog.get_data()
            success = self.model_manager.add_model(model_data)
            if success:
                self._loadModels()
                QMessageBox.information(self, '成功', '模型已添加')
            else:
                QMessageBox.critical(self, '错误', '添加模型失败')

    def _onEdit(self):
        selected_rows = self.models_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, '警告', '请先选择一个模型')
            return

        row = selected_rows[0].row()
        if row < len(self.current_models):
            model = self.current_models[row]

            dialog = AddModelDialog(self, model_data=model)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_data = dialog.get_data()

                self.model_manager.delete_model(model.get('provider', ''), model.get('id', ''))
                self.model_manager.add_model(new_data)

                self._loadModels()
                QMessageBox.information(self, '成功', '模型已更新')

    def _onDelete(self):
        selected_rows = self.models_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, '警告', '请先选择一个模型')
            return

        row = selected_rows[0].row()
        provider = self.models_table.item(row, 0).text()
        model_id = self.models_table.item(row, 1).text()

        reply = QMessageBox.question(
            self, '确认删除',
            f"确定要删除模型 '{model_id}' 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success = self.model_manager.delete_model(provider, model_id)
            if success:
                self._loadModels()
                QMessageBox.information(self, '成功', '模型已删除')
            else:
                QMessageBox.critical(self, '错误', '删除模型失败')

    def _onTest(self):
        selected_rows = self.models_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, '警告', '请先选择一个模型')
            return

        row = selected_rows[0].row()
        if row < len(self.current_models):
            model = self.current_models[row]
            dialog = ModelTestDialog(self, model_data=model)
            dialog.exec()

    def refresh(self):
        self._loadModels()
