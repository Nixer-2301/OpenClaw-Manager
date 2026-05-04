from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QComboBox, QTextEdit, QPushButton,
    QGroupBox, QLineEdit, QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from core.model_manager import ModelManager
from core.model_tester import ModelTester


class TestWorker(QThread):
    finished = pyqtSignal(dict)

    def __init__(self, tester, test_type, base_url, api_key, model_id, prompt):
        super().__init__()
        self.tester = tester
        self.test_type = test_type
        self.base_url = base_url
        self.api_key = api_key
        self.model_id = model_id
        self.prompt = prompt

    def run(self):
        if self.test_type == 'connection':
            result = self.tester.test_connection(self.base_url, self.api_key)
        else:
            result = self.tester.send_test_request(
                self.base_url, self.api_key, self.model_id, self.prompt
            )
        self.finished.emit(result)


class ModelTestDialog(QDialog):
    def __init__(self, parent=None, model_data=None):
        super().__init__(parent)
        self.model_manager = ModelManager()
        self.tester = ModelTester()
        self.model_data = model_data
        self.worker = None
        self.setWindowTitle('模型测试')
        self.setMinimumSize(600, 500)
        self._initUI()
        self._loadModels()

    def _initUI(self):
        layout = QVBoxLayout(self)

        config_group = QGroupBox('配置')
        config_layout = QFormLayout(config_group)

        self.model_combo = QComboBox()
        self.model_combo.currentTextChanged.connect(self._onModelChanged)
        config_layout.addRow('模型:', self.model_combo)

        self.base_url_input = QLineEdit()
        config_layout.addRow('Base URL:', self.base_url_input)

        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        config_layout.addRow('API Key:', self.api_key_input)

        self.model_id_input = QLineEdit()
        config_layout.addRow('Model ID:', self.model_id_input)

        layout.addWidget(config_group)

        prompt_group = QGroupBox('测试提示词')
        prompt_layout = QVBoxLayout(prompt_group)

        self.prompt_input = QTextEdit()
        self.prompt_input.setPlainText("Hello, please respond with 'OK' to confirm you are working.")
        self.prompt_input.setMaximumHeight(100)
        prompt_layout.addWidget(self.prompt_input)

        layout.addWidget(prompt_group)

        button_layout = QHBoxLayout()

        self.test_connection_btn = QPushButton('测试连接')
        self.test_connection_btn.clicked.connect(self._onTestConnection)
        button_layout.addWidget(self.test_connection_btn)

        self.test_request_btn = QPushButton('发送请求')
        self.test_request_btn.clicked.connect(self._onTestRequest)
        button_layout.addWidget(self.test_request_btn)

        self.clear_btn = QPushButton('清除')
        self.clear_btn.clicked.connect(self._onClear)
        button_layout.addWidget(self.clear_btn)

        layout.addLayout(button_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        result_group = QGroupBox('结果')
        result_layout = QVBoxLayout(result_group)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont('Consolas', 10))
        result_layout.addWidget(self.result_text)

        self.stats_label = QLabel('')
        result_layout.addWidget(self.stats_label)

        layout.addWidget(result_group)

        self.status_label = QLabel('就绪')
        layout.addWidget(self.status_label)

    def _loadModels(self):
        self.model_combo.clear()
        models = self.model_manager.get_all_models()
        for model in models:
            display_text = f"{model.get('provider', '')}/{model.get('id', '')}"
            self.model_combo.addItem(display_text, model)

        if self.model_data:
            for i in range(self.model_combo.count()):
                data = self.model_combo.itemData(i)
                if data and data.get('id') == self.model_data.get('id'):
                    self.model_combo.setCurrentIndex(i)
                    break

    def _onModelChanged(self, text):
        model = self.model_combo.currentData()
        if model:
            self.base_url_input.setText(model.get('base_url', ''))
            self.model_id_input.setText(model.get('id', ''))

    def _onTestConnection(self):
        base_url = self.base_url_input.text().strip()
        if not base_url:
            QMessageBox.warning(self, '警告', '请输入Base URL')
            return

        self._setTesting(True)
        self.result_text.setPlainText('正在测试连接...')
        self.stats_label.setText('')

        self.worker = TestWorker(
            self.tester, 'connection',
            base_url, self.api_key_input.text().strip(),
            self.model_id_input.text().strip(), ''
        )
        self.worker.finished.connect(self._onConnectionResult)
        self.worker.start()

    def _onTestRequest(self):
        base_url = self.base_url_input.text().strip()
        api_key = self.api_key_input.text().strip()
        model_id = self.model_id_input.text().strip()
        prompt = self.prompt_input.toPlainText().strip()

        if not base_url or not api_key or not model_id:
            QMessageBox.warning(self, '警告', '请填写所有必填字段')
            return

        self._setTesting(True)
        self.result_text.setPlainText('正在发送请求...')
        self.stats_label.setText('')

        self.worker = TestWorker(
            self.tester, 'request',
            base_url, api_key, model_id, prompt
        )
        self.worker.finished.connect(self._onRequestResult)
        self.worker.start()

    def _onConnectionResult(self, result):
        self._setTesting(False)
        if result.get('success'):
            self.result_text.setPlainText(
                f"连接成功!\n\n"
                f"状态码: {result.get('status_code')}\n"
                f"响应时间: {result.get('elapsed')}ms\n"
                f"消息: {result.get('message')}"
            )
            self.result_text.setStyleSheet('color: #51cf66;')
        else:
            self.result_text.setPlainText(
                f"连接失败!\n\n"
                f"响应时间: {result.get('elapsed')}ms\n"
                f"错误: {result.get('message')}"
            )
            self.result_text.setStyleSheet('color: #ff6b6b;')

        self.status_label.setText('测试完成')

    def _onRequestResult(self, result):
        self._setTesting(False)
        if result.get('success'):
            self.result_text.setPlainText(
                f"请求成功!\n\n"
                f"响应内容:\n{result.get('content', '')}\n\n"
                f"模型: {result.get('model', '')}"
            )
            self.result_text.setStyleSheet('color: #51cf66;')

            self.stats_label.setText(
                f"响应时间: {result.get('elapsed')}ms | "
                f"输入tokens: {result.get('input_tokens', 0)} | "
                f"输出tokens: {result.get('output_tokens', 0)} | "
                f"总计tokens: {result.get('total_tokens', 0)}"
            )
        else:
            self.result_text.setPlainText(
                f"请求失败!\n\n"
                f"响应时间: {result.get('elapsed')}ms\n"
                f"错误: {result.get('message')}"
            )
            self.result_text.setStyleSheet('color: #ff6b6b;')
            self.stats_label.setText('')

        self.status_label.setText('测试完成')

    def _setTesting(self, testing):
        self.test_connection_btn.setEnabled(not testing)
        self.test_request_btn.setEnabled(not testing)
        self.clear_btn.setEnabled(not testing)

        if testing:
            self.progress_bar.show()
        else:
            self.progress_bar.hide()

    def _onClear(self):
        self.result_text.clear()
        self.result_text.setStyleSheet('')
        self.stats_label.setText('')
        self.status_label.setText('就绪')
