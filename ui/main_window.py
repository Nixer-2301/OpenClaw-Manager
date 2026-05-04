from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QStatusBar,
    QMenuBar, QToolBar, QWidget, QVBoxLayout, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QKeySequence

from ui.skills_tab import SkillsTab
from ui.config_tab import ConfigTab
from ui.models_tab import ModelsTab
from ui.plugins_tab import PluginsTab
from ui.settings_tab import SettingsTab
from ui.log_tab import LogTab
from ui.stats_tab import StatsTab
from ui.process_tab import ProcessTab
from ui.session_tab import SessionTab
from ui.template_dialog import TemplateDialog
from ui.command_palette import CommandPalette
from utils.file_watcher import FileWatcher
from utils.translator import tr
from core.settings_manager import SettingsManager
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, APP_NAME,
    CONFIG_FILE, USER_SKILLS_DIR, SYSTEM_SKILLS_DIR
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr('app.name'))
        self.setMinimumSize(QSize(WINDOW_WIDTH, WINDOW_HEIGHT))

        self.settings_manager = SettingsManager()

        self._initMenuBar()
        self._initCentralWidget()
        self._initStatusBar()
        self._initFileWatcher()
        self._applySettings()

    def _initMenuBar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu(tr('menu.file'))

        refresh_action = QAction(tr('action.refresh') + '(&R)', self)
        refresh_action.setShortcut(QKeySequence('F5'))
        refresh_action.triggered.connect(self._onRefresh)
        file_menu.addAction(refresh_action)

        file_menu.addSeparator()

        save_action = QAction(tr('action.save') + '(&S)', self)
        save_action.setShortcut(QKeySequence('Ctrl+S'))
        save_action.triggered.connect(self._onSave)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        template_action = QAction(tr('template.title') + '(&T)', self)
        template_action.triggered.connect(self._onShowTemplates)
        file_menu.addAction(template_action)

        file_menu.addSeparator()

        exit_action = QAction(tr('action.close') + '(&X)', self)
        exit_action.setShortcut(QKeySequence('Alt+F4'))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu(tr('menu.edit'))

        find_action = QAction(tr('action.find') + '(&F)', self)
        find_action.setShortcut(QKeySequence('Ctrl+F'))
        find_action.triggered.connect(self._onFind)
        edit_menu.addAction(find_action)

        select_all_action = QAction(tr('action.selectAll') + '(&A)', self)
        select_all_action.setShortcut(QKeySequence('Ctrl+A'))
        select_all_action.triggered.connect(self._onSelectAll)
        edit_menu.addAction(select_all_action)

        view_menu = menubar.addMenu(tr('menu.view'))

        tab_shortcuts = ['Ctrl+1', 'Ctrl+2', 'Ctrl+3', 'Ctrl+4', 'Ctrl+5', 'Ctrl+6', 'Ctrl+7', 'Ctrl+8', 'Ctrl+9']
        tab_names = [
            tr('tab.skills') + '(&1)',
            tr('tab.config') + '(&2)',
            tr('tab.models') + '(&3)',
            tr('tab.plugins') + '(&4)',
            '进程管理(&5)',
            '会话监控(&6)',
            tr('tab.logs') + '(&7)',
            tr('tab.stats') + '(&8)',
            tr('tab.settings') + '(&9)'
        ]
        for i, (shortcut, name) in enumerate(zip(tab_shortcuts, tab_names)):
            action = QAction(name, self)
            action.setShortcut(QKeySequence(shortcut))
            action.triggered.connect(lambda checked, idx=i: self.tab_widget.setCurrentIndex(idx))
            view_menu.addAction(action)

        view_menu.addSeparator()

        toggle_watcher_action = QAction(tr('status.fileMonitor') + '(&W)', self)
        toggle_watcher_action.setCheckable(True)
        toggle_watcher_action.setChecked(True)
        toggle_watcher_action.triggered.connect(self._onToggleWatcher)
        view_menu.addAction(toggle_watcher_action)
        self.toggle_watcher_action = toggle_watcher_action

        help_menu = menubar.addMenu(tr('menu.help'))

        about_action = QAction(tr('dialog.about') + '(&A)', self)
        about_action.triggered.connect(self._onAbout)
        help_menu.addAction(about_action)

        shortcuts_action = QAction(tr('dialog.shortcuts') + '(&K)', self)
        shortcuts_action.setShortcut(QKeySequence('F1'))
        shortcuts_action.triggered.connect(self._onShowShortcuts)
        help_menu.addAction(shortcuts_action)

    def _initCentralWidget(self):
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)

        self.skills_tab = SkillsTab()
        self.config_tab = ConfigTab()
        self.models_tab = ModelsTab()
        self.plugins_tab = PluginsTab()
        self.process_tab = ProcessTab()
        self.session_tab = SessionTab()
        self.log_tab = LogTab()
        self.stats_tab = StatsTab()
        self.settings_tab = SettingsTab()
        self.settings_tab.theme_changed.connect(self._onThemeChanged)

        self.tab_widget.addTab(self.skills_tab, tr('tab.skills'))
        self.tab_widget.addTab(self.config_tab, tr('tab.config'))
        self.tab_widget.addTab(self.models_tab, tr('tab.models'))
        self.tab_widget.addTab(self.plugins_tab, tr('tab.plugins'))
        self.tab_widget.addTab(self.process_tab, '进程管理')
        self.tab_widget.addTab(self.session_tab, '会话监控')
        self.tab_widget.addTab(self.log_tab, tr('tab.logs'))
        self.tab_widget.addTab(self.stats_tab, tr('tab.stats'))
        self.tab_widget.addTab(self.settings_tab, tr('tab.settings'))

        self.setCentralWidget(self.tab_widget)

    def _initStatusBar(self):
        self.statusBar().showMessage(tr('status.ready'))

        self.watcher_status = QLabel(tr('status.fileMonitor') + ': ' + tr('status.enabled'))
        self.statusBar().addPermanentWidget(self.watcher_status)

    def _initFileWatcher(self):
        try:
            skills_dirs = [str(USER_SKILLS_DIR), str(SYSTEM_SKILLS_DIR)]
            self.file_watcher = FileWatcher(str(CONFIG_FILE), skills_dirs)
            self.file_watcher.config_changed.connect(self._onConfigChanged)
            self.file_watcher.skills_changed.connect(self._onSkillsChanged)

            watcher_settings = self.settings_manager.get_file_watcher_settings()
            if watcher_settings.get('enabled', True):
                self.file_watcher.start()
        except Exception as e:
            print(f'File watcher start failed: {e}')

    def _applySettings(self):
        general = self.settings_manager.get_general_settings()
        default_tab = general.get('default_tab', 0)
        if 0 <= default_tab < self.tab_widget.count():
            self.tab_widget.setCurrentIndex(default_tab)

    def _onConfigChanged(self, path):
        self.statusBar().showMessage(f'Config changed: {path}', 3000)
        current_tab = self.tab_widget.currentWidget()
        if isinstance(current_tab, ConfigTab):
            current_tab.refresh()

    def _onSkillsChanged(self):
        self.statusBar().showMessage('Skills directory changed', 3000)
        current_tab = self.tab_widget.currentWidget()
        if isinstance(current_tab, SkillsTab):
            current_tab.refresh()

    def _onToggleWatcher(self, checked):
        if checked:
            if not self.file_watcher.is_running():
                self.file_watcher.start()
            self.watcher_status.setText(tr('status.fileMonitor') + ': ' + tr('status.enabled'))
        else:
            if self.file_watcher.is_running():
                self.file_watcher.stop()
            self.watcher_status.setText(tr('status.fileMonitor') + ': ' + tr('status.disabled'))

    def _onRefresh(self):
        current_tab = self.tab_widget.currentWidget()
        if hasattr(current_tab, 'refresh'):
            current_tab.refresh()
            self.statusBar().showMessage(tr('status.refreshed'), 2000)

    def _onSave(self):
        current_tab = self.tab_widget.currentWidget()
        if isinstance(current_tab, ConfigTab):
            current_tab.save()
        elif isinstance(current_tab, SettingsTab):
            current_tab._onSave()

    def _onFind(self):
        current_tab = self.tab_widget.currentWidget()
        if isinstance(current_tab, SkillsTab):
            current_tab.search_input.setFocus()
            current_tab.search_input.selectAll()

    def _onSelectAll(self):
        current_tab = self.tab_widget.currentWidget()
        if isinstance(current_tab, (SkillsTab, PluginsTab)):
            current_tab.select_all_cb.setChecked(True)

    def _onShowTemplates(self):
        dialog = TemplateDialog(self)
        dialog.exec()

    def _showCommandPalette(self):
        palette = CommandPalette(self)
        palette.command_executed.connect(self._executeCommand)
        palette.show()

    def _executeCommand(self, action):
        if action == 'refreshAll':
            for i in range(self.tab_widget.count()):
                tab = self.tab_widget.widget(i)
                if hasattr(tab, 'refresh'):
                    tab.refresh()
        elif action == 'openConfigDir':
            import os
            os.startfile(str(CONFIG_FILE.parent))
        elif action == 'openSkillsDir':
            import os
            os.startfile(str(USER_SKILLS_DIR))
        elif action == 'clearBackups':
            from core.config_manager import ConfigManager
            cm = ConfigManager()
            backups = cm.list_backups()
            if len(backups) > 10:
                for backup in backups[10:]:
                    try:
                        import os
                        os.remove(backup['path'])
                    except Exception:
                        pass
        elif action == 'resetSettings':
            reply = QMessageBox.question(
                self, tr('dialog.confirm'),
                'Reset all settings to default?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.settings_manager.reset_to_defaults()
                self.settings_tab.refresh()
        elif action.startswith('switchTo'):
            tab_map = {
                'switchToSkills': 0,
                'switchToConfig': 1,
                'switchToModels': 2,
                'switchToPlugins': 3,
                'switchToLogs': 4,
                'switchToStats': 5,
                'switchToSettings': 6
            }
            idx = tab_map.get(action, 0)
            self.tab_widget.setCurrentIndex(idx)

    def _onAbout(self):
        QMessageBox.about(
            self, tr('dialog.about'),
            f'{tr("app.name")}\n\n'
            f'{tr("app.version")}: 2.0.0\n\n'
            'Features:\n'
            f'- {tr("tab.skills")} (batch operations)\n'
            f'- {tr("tab.config")} (JSON editor, tree view)\n'
            f'- {tr("tab.models")}\n'
            f'- {tr("tab.plugins")} (batch operations)\n'
            f'- {tr("tab.logs")}\n'
            f'- {tr("tab.stats")}\n'
            f'- {tr("template.title")}\n'
            f'- {tr("status.fileMonitor")}\n'
            f'- {tr("dialog.commandPalette")}'
        )

    def _onShowShortcuts(self):
        shortcuts_text = f"""
{tr('dialog.shortcuts')}:

File:
  F5          - {tr('action.refresh')}
  Ctrl+S      - {tr('action.save')}
  Alt+F4      - {tr('action.close')}

Edit:
  Ctrl+F      - {tr('action.find')}
  Ctrl+A      - {tr('action.selectAll')}
  Delete      - {tr('action.delete')}

Skills/Plugins:
  Ctrl+E      - {tr('action.enable')}/{tr('action.disable')}
  Ctrl+Shift+E - {tr('action.batchExport')}
  Ctrl+Enter  - Edit Skill

Tabs:
  Ctrl+1      - {tr('tab.skills')}
  Ctrl+2      - {tr('tab.config')}
  Ctrl+3      - {tr('tab.models')}
  Ctrl+4      - {tr('tab.plugins')}
  Ctrl+5      - Process Manager
  Ctrl+6      - Session Monitor
  Ctrl+7      - {tr('tab.logs')}
  Ctrl+8      - {tr('tab.stats')}
  Ctrl+9      - {tr('tab.settings')}

Other:
  Ctrl+Shift+P - {tr('dialog.commandPalette')}
  F1          - {tr('dialog.shortcuts')}
"""
        QMessageBox.information(self, tr('dialog.shortcuts'), shortcuts_text)

    def _onThemeChanged(self, theme):
        from main import load_stylesheet
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            load_stylesheet(app, theme)
            self.statusBar().showMessage(f'Theme changed to: {theme}', 2000)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_P and event.modifiers() == Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier:
            self._showCommandPalette()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        if hasattr(self, 'file_watcher') and self.file_watcher.is_running():
            self.file_watcher.stop()
        event.accept()
