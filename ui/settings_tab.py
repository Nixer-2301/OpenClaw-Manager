from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QFormLayout, QLabel, QComboBox, QCheckBox,
    QPushButton, QSpinBox, QLineEdit, QMessageBox,
    QFileDialog, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal

from core.settings_manager import SettingsManager


class SettingsTab(QWidget):
    theme_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.settings_manager = SettingsManager()
        self._initUI()
        self._loadSettings()

    def _initUI(self):
        main_layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        layout = QVBoxLayout(scroll_widget)

        general_group = QGroupBox('常规设置')
        general_layout = QFormLayout(general_group)

        self.default_tab_combo = QComboBox()
        self.default_tab_combo.addItems(['Skills管理', '配置文件', '模型管理', '插件管理', '日志', '统计', '设置'])
        general_layout.addRow('默认标签页:', self.default_tab_combo)

        self.auto_refresh_cb = QCheckBox('启动时自动刷新')
        general_layout.addRow('自动刷新:', self.auto_refresh_cb)

        self.confirm_delete_cb = QCheckBox('删除前确认')
        general_layout.addRow('确认删除:', self.confirm_delete_cb)

        self.confirm_batch_cb = QCheckBox('批量操作前确认')
        general_layout.addRow('确认批量操作:', self.confirm_batch_cb)

        layout.addWidget(general_group)

        paths_group = QGroupBox('路径设置')
        paths_layout = QFormLayout(paths_group)

        openclaw_dir_layout = QHBoxLayout()
        self.openclaw_dir_input = QLineEdit()
        openclaw_dir_layout.addWidget(self.openclaw_dir_input)
        self.openclaw_dir_btn = QPushButton('浏览')
        self.openclaw_dir_btn.clicked.connect(lambda: self._browse_dir(self.openclaw_dir_input))
        openclaw_dir_layout.addWidget(self.openclaw_dir_btn)
        paths_layout.addRow('Openclaw目录:', openclaw_dir_layout)

        skills_dir_layout = QHBoxLayout()
        self.skills_dir_input = QLineEdit()
        skills_dir_layout.addWidget(self.skills_dir_input)
        self.skills_dir_btn = QPushButton('浏览')
        self.skills_dir_btn.clicked.connect(lambda: self._browse_dir(self.skills_dir_input))
        skills_dir_layout.addWidget(self.skills_dir_btn)
        paths_layout.addRow('Skills目录:', skills_dir_layout)

        backup_dir_layout = QHBoxLayout()
        self.backup_dir_input = QLineEdit()
        backup_dir_layout.addWidget(self.backup_dir_input)
        self.backup_dir_btn = QPushButton('浏览')
        self.backup_dir_btn.clicked.connect(lambda: self._browse_dir(self.backup_dir_input))
        backup_dir_layout.addWidget(self.backup_dir_btn)
        paths_layout.addRow('备份目录:', backup_dir_layout)

        self.max_backups_spin = QSpinBox()
        self.max_backups_spin.setRange(1, 100)
        paths_layout.addRow('最大备份数:', self.max_backups_spin)

        layout.addWidget(paths_group)

        interface_group = QGroupBox('界面设置')
        interface_layout = QFormLayout(interface_group)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['dark', 'light'])
        interface_layout.addRow('主题:', self.theme_combo)

        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        interface_layout.addRow('字体大小:', self.font_size_spin)

        self.row_height_spin = QSpinBox()
        self.row_height_spin.setRange(20, 60)
        interface_layout.addRow('表格行高:', self.row_height_spin)

        layout.addWidget(interface_group)

        watcher_group = QGroupBox('文件监控设置')
        watcher_layout = QFormLayout(watcher_group)

        self.watcher_enabled_cb = QCheckBox('启用文件监控')
        watcher_layout.addRow('文件监控:', self.watcher_enabled_cb)

        self.refresh_interval_spin = QSpinBox()
        self.refresh_interval_spin.setRange(1, 60)
        self.refresh_interval_spin.setSuffix(' 秒')
        watcher_layout.addRow('刷新间隔:', self.refresh_interval_spin)

        layout.addWidget(watcher_group)

        button_layout = QHBoxLayout()

        self.save_btn = QPushButton('保存设置')
        self.save_btn.clicked.connect(self._onSave)
        button_layout.addWidget(self.save_btn)

        self.reset_btn = QPushButton('恢复默认')
        self.reset_btn.clicked.connect(self._onReset)
        button_layout.addWidget(self.reset_btn)

        self.refresh_btn = QPushButton('刷新')
        self.refresh_btn.clicked.connect(self._loadSettings)
        button_layout.addWidget(self.refresh_btn)

        button_layout.addStretch()

        layout.addLayout(button_layout)

        self.status_label = QLabel('就绪')
        layout.addWidget(self.status_label)

        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)

    def _browse_dir(self, line_edit):
        dir_path = QFileDialog.getExistingDirectory(self, '选择目录')
        if dir_path:
            line_edit.setText(dir_path)

    def _loadSettings(self):
        settings = self.settings_manager.get_all()

        general = settings.get('general', {})
        self.default_tab_combo.setCurrentIndex(general.get('default_tab', 0))
        self.auto_refresh_cb.setChecked(general.get('auto_refresh', True))
        self.confirm_delete_cb.setChecked(general.get('confirm_delete', True))
        self.confirm_batch_cb.setChecked(general.get('confirm_batch', True))

        paths = settings.get('paths', {})
        self.openclaw_dir_input.setText(paths.get('openclaw_dir', ''))
        self.skills_dir_input.setText(paths.get('user_skills_dir', ''))
        self.backup_dir_input.setText(paths.get('backup_dir', ''))
        self.max_backups_spin.setValue(paths.get('max_backups', 10))

        interface = settings.get('interface', {})
        theme_index = self.theme_combo.findText(interface.get('theme', 'dark'))
        if theme_index >= 0:
            self.theme_combo.setCurrentIndex(theme_index)
        self.font_size_spin.setValue(interface.get('font_size', 10))
        self.row_height_spin.setValue(interface.get('table_row_height', 30))

        watcher = settings.get('file_watcher', {})
        self.watcher_enabled_cb.setChecked(watcher.get('enabled', True))
        self.refresh_interval_spin.setValue(watcher.get('refresh_interval', 5))

        self.status_label.setText('设置已加载')

    def _onSave(self):
        old_theme = self.settings_manager.get('interface', 'theme', 'dark')
        new_theme = self.theme_combo.currentText()

        self.settings_manager.set('general', 'default_tab', self.default_tab_combo.currentIndex())
        self.settings_manager.set('general', 'auto_refresh', self.auto_refresh_cb.isChecked())
        self.settings_manager.set('general', 'confirm_delete', self.confirm_delete_cb.isChecked())
        self.settings_manager.set('general', 'confirm_batch', self.confirm_batch_cb.isChecked())

        self.settings_manager.set('paths', 'openclaw_dir', self.openclaw_dir_input.text())
        self.settings_manager.set('paths', 'user_skills_dir', self.skills_dir_input.text())
        self.settings_manager.set('paths', 'backup_dir', self.backup_dir_input.text())
        self.settings_manager.set('paths', 'max_backups', self.max_backups_spin.value())

        self.settings_manager.set('interface', 'theme', new_theme)
        self.settings_manager.set('interface', 'font_size', self.font_size_spin.value())
        self.settings_manager.set('interface', 'table_row_height', self.row_height_spin.value())

        self.settings_manager.set('file_watcher', 'enabled', self.watcher_enabled_cb.isChecked())
        self.settings_manager.set('file_watcher', 'refresh_interval', self.refresh_interval_spin.value())

        if self.settings_manager.save_settings():
            self.status_label.setText('设置已保存')
            if old_theme != new_theme:
                self.theme_changed.emit(new_theme)
            QMessageBox.information(self, '成功', '设置已保存')
        else:
            QMessageBox.critical(self, '错误', '保存设置失败')

    def _onReset(self):
        reply = QMessageBox.question(
            self, '确认恢复默认',
            '确定要恢复所有设置为默认值吗？',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self.settings_manager.reset_to_defaults():
                self._loadSettings()
                old_theme = 'dark'
                new_theme = self.settings_manager.get('interface', 'theme', 'dark')
                if old_theme != new_theme:
                    self.theme_changed.emit(new_theme)
                QMessageBox.information(self, '成功', '设置已恢复为默认值')
            else:
                QMessageBox.critical(self, '错误', '恢复默认设置失败')

    def refresh(self):
        self._loadSettings()
