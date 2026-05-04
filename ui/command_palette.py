from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QListWidget,
    QListWidgetItem, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeySequence

from utils.translator import tr


class CommandPalette(QDialog):
    command_executed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr('dialog.commandPalette'))
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.setMinimumSize(500, 400)
        self.commands = []
        self._initUI()
        self._loadCommands()

    def _initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Type a command...')
        self.search_input.textChanged.connect(self._onTextChanged)
        self.search_input.returnPressed.connect(self._onExecute)
        layout.addWidget(self.search_input)

        self.command_list = QListWidget()
        self.command_list.itemDoubleClicked.connect(self._onExecute)
        layout.addWidget(self.command_list)

        self.hint_label = QLabel('Press Enter to execute, Esc to close')
        self.hint_label.setStyleSheet('color: gray; font-size: 11px;')
        layout.addWidget(self.hint_label)

    def _loadCommands(self):
        self.commands = [
            {
                'name': tr('command.refreshAll'),
                'action': 'refreshAll',
                'shortcut': 'F5'
            },
            {
                'name': tr('command.openConfigDir'),
                'action': 'openConfigDir',
                'shortcut': ''
            },
            {
                'name': tr('command.openSkillsDir'),
                'action': 'openSkillsDir',
                'shortcut': ''
            },
            {
                'name': tr('command.clearBackups'),
                'action': 'clearBackups',
                'shortcut': ''
            },
            {
                'name': tr('command.resetSettings'),
                'action': 'resetSettings',
                'shortcut': ''
            },
            {
                'name': tr('command.switchToSkills'),
                'action': 'switchToSkills',
                'shortcut': 'Ctrl+1'
            },
            {
                'name': tr('command.switchToConfig'),
                'action': 'switchToConfig',
                'shortcut': 'Ctrl+2'
            },
            {
                'name': tr('command.switchToModels'),
                'action': 'switchToModels',
                'shortcut': 'Ctrl+3'
            },
            {
                'name': tr('command.switchToPlugins'),
                'action': 'switchToPlugins',
                'shortcut': 'Ctrl+4'
            },
            {
                'name': tr('command.switchToSettings'),
                'action': 'switchToSettings',
                'shortcut': 'Ctrl+5'
            },
        ]
        self._updateList()

    def _updateList(self, filter_text=''):
        self.command_list.clear()
        for cmd in self.commands:
            if filter_text.lower() in cmd['name'].lower():
                item_text = cmd['name']
                if cmd['shortcut']:
                    item_text += f'  ({cmd["shortcut"]})'
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, cmd['action'])
                self.command_list.addItem(item)

        if self.command_list.count() > 0:
            self.command_list.setCurrentRow(0)

    def _onTextChanged(self, text):
        self._updateList(text)

    def _onExecute(self):
        current_item = self.command_list.currentItem()
        if current_item:
            action = current_item.data(Qt.ItemDataRole.UserRole)
            self.command_executed.emit(action)
            self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.key() == Qt.Key.Key_Up:
            current_row = self.command_list.currentRow()
            if current_row > 0:
                self.command_list.setCurrentRow(current_row - 1)
        elif event.key() == Qt.Key.Key_Down:
            current_row = self.command_list.currentRow()
            if current_row < self.command_list.count() - 1:
                self.command_list.setCurrentRow(current_row + 1)
        elif event.key() == Qt.Key.Key_Return:
            self._onExecute()
        else:
            super().keyPressEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        self.search_input.clear()
        self._updateList()
        self.search_input.setFocus()

        if self.parent():
            parent_rect = self.parent().geometry()
            x = parent_rect.x() + (parent_rect.width() - self.width()) // 2
            y = parent_rect.y() + (parent_rect.height() - self.height()) // 3
            self.move(x, y)
