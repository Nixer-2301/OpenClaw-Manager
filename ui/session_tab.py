from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLabel, QGroupBox,
    QTextEdit, QHeaderView, QAbstractItemView, QMessageBox,
    QCheckBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor

from core.openclaw_api import OpenclawAPI


class SessionTab(QWidget):
    def __init__(self):
        super().__init__()
        self.api = OpenclawAPI()
        self.sessions = []
        self._initUI()
        self._loadSessions()

    def _initUI(self):
        layout = QVBoxLayout(self)

        toolbar_layout = QHBoxLayout()

        self.refresh_btn = QPushButton('刷新')
        self.refresh_btn.clicked.connect(self._loadSessions)
        toolbar_layout.addWidget(self.refresh_btn)

        self.test_btn = QPushButton('测试连接')
        self.test_btn.clicked.connect(self._testConnection)
        toolbar_layout.addWidget(self.test_btn)

        toolbar_layout.addStretch()

        self.auto_refresh_cb = QCheckBox('自动刷新')
        self.auto_refresh_cb.stateChanged.connect(self._onAutoRefreshChanged)
        toolbar_layout.addWidget(self.auto_refresh_cb)

        layout.addLayout(toolbar_layout)

        status_group = QGroupBox('连接状态')
        status_layout = QHBoxLayout(status_group)

        self.connection_label = QLabel('未连接')
        self.connection_label.setStyleSheet('font-weight: bold;')
        status_layout.addWidget(QLabel('状态:'))
        status_layout.addWidget(self.connection_label)

        self.server_label = QLabel('-')
        status_layout.addWidget(QLabel('服务器:'))
        status_layout.addWidget(self.server_label)

        status_layout.addStretch()

        layout.addWidget(status_group)

        splitter = QSplitter(Qt.Orientation.Vertical)

        sessions_group = QGroupBox('会话列表')
        sessions_layout = QVBoxLayout(sessions_group)

        self.sessions_table = QTableWidget()
        self.sessions_table.setColumnCount(5)
        self.sessions_table.setHorizontalHeaderLabels(['ID', '创建时间', '模型', '消息数', '状态'])
        self.sessions_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.sessions_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.sessions_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.sessions_table.itemSelectionChanged.connect(self._onSelectionChanged)
        sessions_layout.addWidget(self.sessions_table)

        splitter.addWidget(sessions_group)

        messages_group = QGroupBox('会话消息')
        messages_layout = QVBoxLayout(messages_group)

        self.messages_text = QTextEdit()
        self.messages_text.setReadOnly(True)
        self.messages_text.setFont(QFont('Consolas', 10))
        messages_layout.addWidget(self.messages_text)

        splitter.addWidget(messages_group)
        splitter.setSizes([300, 300])

        layout.addWidget(splitter)

        self.status_label = QLabel('就绪')
        layout.addWidget(self.status_label)

        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self._loadSessions)

    def _testConnection(self):
        success = self.api.test_connection()
        if success:
            self.connection_label.setText('已连接')
            self.connection_label.setStyleSheet('color: #51cf66; font-weight: bold;')
            self.server_label.setText(self.api.base_url)
            QMessageBox.information(self, '成功', '连接成功')
        else:
            self.connection_label.setText('连接失败')
            self.connection_label.setStyleSheet('color: #ff6b6b; font-weight: bold;')
            QMessageBox.critical(self, '错误', '连接失败，请检查Openclaw是否运行')

    def _loadSessions(self):
        result = self.api.get_sessions()

        if not result.get('success'):
            self.status_label.setText(f'加载失败: {result.get("error", "Unknown error")}')
            return

        self.sessions = result.get('data', [])
        if isinstance(self.sessions, dict):
            self.sessions = list(self.sessions.values())

        self.sessions_table.setRowCount(len(self.sessions))

        for row, session in enumerate(self.sessions):
            if isinstance(session, dict):
                session_id = session.get('sessionId', session.get('id', ''))[:8]
                created = session.get('sessionStartedAt', '')
                if created:
                    from datetime import datetime
                    try:
                        created = datetime.fromtimestamp(created / 1000).strftime('%Y-%m-%d %H:%M')
                    except:
                        created = str(created)

                model = session.get('model', 'N/A')
                messages = session.get('messageCount', session.get('compactionCount', 0))
                status = '活跃' if session.get('systemSent', False) else '空闲'

                self.sessions_table.setItem(row, 0, QTableWidgetItem(str(session_id)))
                self.sessions_table.setItem(row, 1, QTableWidgetItem(str(created)))
                self.sessions_table.setItem(row, 2, QTableWidgetItem(str(model)))
                self.sessions_table.setItem(row, 3, QTableWidgetItem(str(messages)))

                status_item = QTableWidgetItem(status)
                if status == '活跃':
                    status_item.setForeground(QColor('#51cf66'))
                else:
                    status_item.setForeground(QColor('#ffd43b'))
                self.sessions_table.setItem(row, 4, status_item)

        self.status_label.setText(f'已加载 {len(self.sessions)} 个会话')

    def _onSelectionChanged(self):
        selected_rows = self.sessions_table.selectionModel().selectedRows()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        if row < len(self.sessions):
            session = self.sessions[row]
            self._showSessionMessages(session)

    def _showSessionMessages(self, session):
        session_id = session.get('sessionId', session.get('id', ''))

        self.messages_text.clear()
        self.messages_text.setPlainText(f'加载会话 {session_id} 的消息...\n\n')

        session_file = session.get('sessionFile', '')
        if session_file:
            try:
                from pathlib import Path
                if Path(session_file).exists():
                    with open(session_file, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()

                    self.messages_text.clear()
                    for line in lines[-100:]:
                        try:
                            msg = json.loads(line.strip())
                            role = msg.get('role', 'unknown')
                            content = msg.get('content', '')

                            if role == 'user':
                                self.messages_text.append(f'<span style="color: #74c0fc;">[User]</span>')
                            elif role == 'assistant':
                                self.messages_text.append(f'<span style="color: #51cf66;">[Assistant]</span>')
                            else:
                                self.messages_text.append(f'<span style="color: #ffd43b;">[{role}]</span>')

                            self.messages_text.append(content[:500])
                            self.messages_text.append('')
                        except:
                            pass
                    return
            except Exception as e:
                self.messages_text.setPlainText(f'无法读取消息文件: {str(e)}')

        self.messages_text.setPlainText('无法加载消息，会话文件不存在或格式不支持')

    def _onAutoRefreshChanged(self, state):
        if state == 2:
            self.refresh_timer.start(10000)
        else:
            self.refresh_timer.stop()

    def refresh(self):
        self._loadSessions()


import json
from PyQt6.QtWidgets import QSplitter
