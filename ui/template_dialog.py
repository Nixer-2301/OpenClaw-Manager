from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QComboBox, QTextEdit, QLineEdit,
    QPushButton, QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from core.template_manager import TemplateManager
from utils.translator import tr


class TemplateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.template_manager = TemplateManager()
        self.setWindowTitle(tr('template.title'))
        self.setMinimumSize(600, 500)
        self._initUI()
        self._loadTemplates()

    def _initUI(self):
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        self.template_combo = QComboBox()
        self.template_combo.currentTextChanged.connect(self._onTemplateChanged)
        form_layout.addRow(tr('template.select') + ':', self.template_combo)

        layout.addLayout(form_layout)

        preview_label = QLabel(tr('template.preview') + ':')
        layout.addWidget(preview_label)

        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setFont(QFont('Consolas', 10))
        layout.addWidget(self.preview_text)

        api_key_layout = QHBoxLayout()
        api_key_label = QLabel(tr('template.apiKey') + ':')
        api_key_layout.addWidget(api_key_label)
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setPlaceholderText('Enter API Key (optional)')
        api_key_layout.addWidget(self.api_key_input)
        layout.addLayout(api_key_layout)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._onApply)
        button_box.rejected.connect(self.reject)

        apply_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        apply_button.setText(tr('template.apply'))

        layout.addWidget(button_box)

    def _loadTemplates(self):
        self.template_combo.clear()
        templates = self.template_manager.get_all_templates()
        for name in templates:
            self.template_combo.addItem(name)

    def _onTemplateChanged(self, template_name):
        template = self.template_manager.get_template(template_name)
        if template:
            import json
            preview = json.dumps(template, indent=2, ensure_ascii=False)
            self.preview_text.setPlainText(preview)

    def _onApply(self):
        template_name = self.template_combo.currentText()
        if not template_name:
            return

        api_key = self.api_key_input.text().strip()

        reply = QMessageBox.question(
            self, tr('dialog.confirm'),
            f"Apply template '{template_name}'?\nThis will modify your configuration.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success = self.template_manager.apply_template(template_name, api_key)
            if success:
                QMessageBox.information(self, tr('dialog.success'), 'Template applied successfully')
                self.accept()
            else:
                QMessageBox.critical(self, tr('dialog.error'), 'Failed to apply template')
