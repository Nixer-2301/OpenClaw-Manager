from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLabel, QGroupBox,
    QMessageBox, QHeaderView, QAbstractItemView, QTextEdit,
    QCheckBox, QMenu, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QAction

from core.plugin_manager import PluginManager


class PluginsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.plugin_manager = PluginManager()
        self.current_plugins = []
        self._initUI()
        self._loadPlugins()

    def _initUI(self):
        layout = QVBoxLayout(self)

        toolbar_layout = QHBoxLayout()

        self.refresh_btn = QPushButton('刷新')
        self.refresh_btn.setShortcut('F5')
        self.refresh_btn.clicked.connect(self._loadPlugins)
        toolbar_layout.addWidget(self.refresh_btn)

        toolbar_layout.addStretch()

        layout.addLayout(toolbar_layout)

        batch_toolbar = QHBoxLayout()

        self.select_all_cb = QCheckBox('全选')
        self.select_all_cb.stateChanged.connect(self._onSelectAll)
        batch_toolbar.addWidget(self.select_all_cb)

        batch_toolbar.addWidget(QLabel('|'))

        self.batch_enable_btn = QPushButton('批量启用')
        self.batch_enable_btn.clicked.connect(self._onBatchEnable)
        batch_toolbar.addWidget(self.batch_enable_btn)

        self.batch_disable_btn = QPushButton('批量禁用')
        self.batch_disable_btn.clicked.connect(self._onBatchDisable)
        batch_toolbar.addWidget(self.batch_disable_btn)

        batch_toolbar.addStretch()

        self.selected_label = QLabel('已选: 0')
        batch_toolbar.addWidget(self.selected_label)

        layout.addLayout(batch_toolbar)

        self.plugins_table = QTableWidget()
        self.plugins_table.setColumnCount(5)
        self.plugins_table.setHorizontalHeaderLabels(['✓', '名称', '描述', '版本', '状态'])
        self.plugins_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.plugins_table.setColumnWidth(0, 30)
        self.plugins_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.plugins_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.plugins_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.plugins_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.plugins_table.itemSelectionChanged.connect(self._onSelectionChanged)
        self.plugins_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.plugins_table.customContextMenuRequested.connect(self._showContextMenu)

        layout.addWidget(self.plugins_table)

        action_group = QGroupBox('单个操作')
        action_layout = QHBoxLayout(action_group)

        self.enable_btn = QPushButton('启用/禁用')
        self.enable_btn.setShortcut('Ctrl+E')
        self.enable_btn.clicked.connect(self._onToggleEnable)
        action_layout.addWidget(self.enable_btn)

        layout.addWidget(action_group)

        detail_group = QGroupBox('插件详情')
        detail_layout = QVBoxLayout(detail_group)

        self.detail_label = QLabel('选择一个插件查看详情')
        detail_layout.addWidget(self.detail_label)

        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        detail_layout.addWidget(self.detail_text)

        layout.addWidget(detail_group)

    def _loadPlugins(self):
        self.current_plugins = self.plugin_manager.get_all_plugins()
        self.plugins_table.setRowCount(len(self.current_plugins))
        self.select_all_cb.setChecked(False)

        for row, plugin in enumerate(self.current_plugins):
            checkbox = QTableWidgetItem()
            checkbox.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            checkbox.setCheckState(Qt.CheckState.Unchecked)
            self.plugins_table.setItem(row, 0, checkbox)

            self.plugins_table.setItem(row, 1, QTableWidgetItem(plugin.get('name', '')))
            self.plugins_table.setItem(row, 2, QTableWidgetItem(plugin.get('description', '')[:80]))
            self.plugins_table.setItem(row, 3, QTableWidgetItem(plugin.get('version', '')))

            status = '启用' if plugin.get('enabled', False) else '禁用'
            status_item = QTableWidgetItem(status)
            if plugin.get('enabled', False):
                status_item.setForeground(QColor('#51cf66'))
            else:
                status_item.setForeground(QColor('#ff6b6b'))
            self.plugins_table.setItem(row, 4, status_item)

        self._updateSelectedCount()

    def _getCheckedPlugins(self):
        checked = []
        for row in range(self.plugins_table.rowCount()):
            checkbox = self.plugins_table.item(row, 0)
            if checkbox and checkbox.checkState() == Qt.CheckState.Checked:
                if row < len(self.current_plugins):
                    checked.append(self.current_plugins[row])
        return checked

    def _updateSelectedCount(self):
        checked = self._getCheckedPlugins()
        selected_rows = self.plugins_table.selectionModel().selectedRows()
        count = max(len(checked), len(selected_rows))
        self.selected_label.setText(f'已选: {count}')

    def _onSelectAll(self, state):
        check_state = Qt.CheckState.Checked if state == 2 else Qt.CheckState.Unchecked
        for row in range(self.plugins_table.rowCount()):
            checkbox = self.plugins_table.item(row, 0)
            if checkbox:
                checkbox.setCheckState(check_state)
        self._updateSelectedCount()

    def _onSelectionChanged(self):
        self._updateSelectedCount()
        selected_rows = self.plugins_table.selectionModel().selectedRows()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        if row < len(self.current_plugins):
            plugin = self.current_plugins[row]
            self._showPluginDetail(plugin)

    def _showPluginDetail(self, plugin):
        self.detail_label.setText(f"名称: {plugin.get('name', '')}")

        detail_text = f"描述: {plugin.get('description', '')}\n"
        detail_text += f"版本: {plugin.get('version', '')}\n"
        detail_text += f"状态: {'启用' if plugin.get('enabled', False) else '禁用'}\n"
        detail_text += f"路径: {plugin.get('path', '')}\n"

        self.detail_text.setPlainText(detail_text)

    def _showContextMenu(self, position):
        selected_rows = self.plugins_table.selectionModel().selectedRows()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        if row >= len(self.current_plugins):
            return

        plugin = self.current_plugins[row]
        menu = QMenu(self)

        enable_action = QAction('启用/禁用 (Ctrl+E)', self)
        enable_action.triggered.connect(self._onToggleEnable)
        menu.addAction(enable_action)

        menu.addSeparator()

        copy_name_action = QAction('复制名称', self)
        copy_name_action.triggered.connect(lambda: self._copyToClipboard(plugin.get('name', '')))
        menu.addAction(copy_name_action)

        copy_path_action = QAction('复制路径', self)
        copy_path_action.triggered.connect(lambda: self._copyToClipboard(plugin.get('path', '')))
        menu.addAction(copy_path_action)

        menu.exec(self.plugins_table.viewport().mapToGlobal(position))

    def _copyToClipboard(self, text):
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)

    def _onToggleEnable(self):
        selected_rows = self.plugins_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, '警告', '请先选择一个插件')
            return

        row = selected_rows[0].row()
        if row < len(self.current_plugins):
            plugin = self.current_plugins[row]
            success = self.plugin_manager.toggle_plugin(plugin)
            if success:
                self._loadPlugins()

    def _onBatchEnable(self):
        plugins = self._getCheckedPlugins()
        if not plugins:
            QMessageBox.warning(self, '警告', '请先勾选要操作的插件')
            return

        success_count = 0
        for plugin in plugins:
            if not plugin.get('enabled', False):
                if self.plugin_manager.toggle_plugin(plugin):
                    success_count += 1

        self._loadPlugins()
        QMessageBox.information(self, '完成', f'已启用 {success_count} 个插件')

    def _onBatchDisable(self):
        plugins = self._getCheckedPlugins()
        if not plugins:
            QMessageBox.warning(self, '警告', '请先勾选要操作的插件')
            return

        success_count = 0
        for plugin in plugins:
            if plugin.get('enabled', False):
                if self.plugin_manager.toggle_plugin(plugin):
                    success_count += 1

        self._loadPlugins()
        QMessageBox.information(self, '完成', f'已禁用 {success_count} 个插件')

    def refresh(self):
        self._loadPlugins()
