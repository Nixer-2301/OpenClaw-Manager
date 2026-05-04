from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit, QComboBox,
    QHeaderView, QSplitter, QTextEdit, QLabel, QGroupBox,
    QMessageBox, QFileDialog, QAbstractItemView, QFormLayout,
    QCheckBox, QMenu, QApplication
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QColor, QFont, QDragEnterEvent, QDropEvent, QAction

from core.skill_manager import SkillManager
from ui.skill_editor import SkillEditorDialog


class SkillsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.skill_manager = SkillManager()
        self.current_skills = []
        self.displayed_skills = []
        self.setAcceptDrops(True)
        self._initUI()
        self._loadSkills()

    def _initUI(self):
        layout = QVBoxLayout(self)

        toolbar_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('搜索Skills... (Ctrl+F)')
        self.search_input.textChanged.connect(self._onSearch)
        toolbar_layout.addWidget(self.search_input)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(['全部', '用户Skills', '系统Skills'])
        self.filter_combo.currentTextChanged.connect(self._onFilter)
        toolbar_layout.addWidget(self.filter_combo)

        self.refresh_btn = QPushButton('刷新')
        self.refresh_btn.setShortcut('F5')
        self.refresh_btn.clicked.connect(self._loadSkills)
        toolbar_layout.addWidget(self.refresh_btn)

        self.import_btn = QPushButton('导入')
        self.import_btn.setShortcut('Ctrl+I')
        self.import_btn.clicked.connect(self._onImport)
        toolbar_layout.addWidget(self.import_btn)

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

        self.batch_export_btn = QPushButton('批量导出')
        self.batch_export_btn.setShortcut('Ctrl+Shift+E')
        self.batch_export_btn.clicked.connect(self._onBatchExport)
        batch_toolbar.addWidget(self.batch_export_btn)

        self.batch_delete_btn = QPushButton('批量删除')
        self.batch_delete_btn.setShortcut('Delete')
        self.batch_delete_btn.clicked.connect(self._onBatchDelete)
        batch_toolbar.addWidget(self.batch_delete_btn)

        batch_toolbar.addStretch()

        self.selected_label = QLabel('已选: 0')
        batch_toolbar.addWidget(self.selected_label)

        layout.addLayout(batch_toolbar)

        self.drop_zone = QLabel('拖拽ZIP文件到此处导入Skills')
        self.drop_zone.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drop_zone.setStyleSheet('''
            QLabel {
                border: 2px dashed #666;
                border-radius: 10px;
                padding: 20px;
                color: #666;
                font-size: 14px;
            }
        ''')
        self.drop_zone.hide()
        layout.addWidget(self.drop_zone)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        self.skills_table = QTableWidget()
        self.skills_table.setColumnCount(6)
        self.skills_table.setHorizontalHeaderLabels(['✓', '名称', '描述', '版本', '位置', '状态'])
        self.skills_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.skills_table.setColumnWidth(0, 30)
        self.skills_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.skills_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.skills_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.skills_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.skills_table.itemSelectionChanged.connect(self._onSelectionChanged)
        self.skills_table.setSortingEnabled(True)
        self.skills_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.skills_table.customContextMenuRequested.connect(self._showContextMenu)

        left_layout.addWidget(self.skills_table)
        splitter.addWidget(left_widget)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        action_group = QGroupBox('单个操作')
        action_layout = QHBoxLayout(action_group)

        self.edit_btn = QPushButton('编辑')
        self.edit_btn.setShortcut('Ctrl+Enter')
        self.edit_btn.clicked.connect(self._onEdit)
        action_layout.addWidget(self.edit_btn)

        self.enable_btn = QPushButton('启用/禁用')
        self.enable_btn.setShortcut('Ctrl+E')
        self.enable_btn.clicked.connect(self._onToggleEnable)
        action_layout.addWidget(self.enable_btn)

        self.export_btn = QPushButton('导出')
        self.export_btn.clicked.connect(self._onExport)
        action_layout.addWidget(self.export_btn)

        self.delete_btn = QPushButton('删除')
        self.delete_btn.clicked.connect(self._onDelete)
        action_layout.addWidget(self.delete_btn)

        right_layout.addWidget(action_group)

        metadata_group = QGroupBox('元数据')
        metadata_layout = QFormLayout(metadata_group)
        metadata_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.metadata_labels = {}
        metadata_fields = ['名称', '描述', '版本', '位置', '状态', '用户可调用',
                          '参数提示', '允许的工具', '许可证', '作者']

        for field in metadata_fields:
            label = QLabel('-')
            label.setWordWrap(True)
            self.metadata_labels[field] = label
            metadata_layout.addRow(f'{field}:', label)

        right_layout.addWidget(metadata_group)

        detail_group = QGroupBox('SKILL.md 内容')
        detail_layout = QVBoxLayout(detail_group)

        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setFont(QFont('Consolas', 10))
        detail_layout.addWidget(self.detail_text)

        right_layout.addWidget(detail_group)

        splitter.addWidget(right_widget)
        splitter.setSizes([500, 500])

        layout.addWidget(splitter)

        self.status_label = QLabel('就绪')
        layout.addWidget(self.status_label)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith('.zip'):
                    event.acceptProposedAction()
                    self._showDropZone(True)
                    return
        event.ignore()

    def dragLeaveEvent(self, event):
        self._showDropZone(False)

    def dropEvent(self, event: QDropEvent):
        self._showDropZone(False)
        imported_count = 0
        failed_count = 0

        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith('.zip'):
                success = self.skill_manager.import_skill(file_path)
                if success:
                    imported_count += 1
                else:
                    failed_count += 1

        self._loadSkills()

        if imported_count > 0:
            QMessageBox.information(self, '导入完成',
                f'成功导入 {imported_count} 个Skills' +
                (f'\n失败 {failed_count} 个' if failed_count > 0 else ''))

    def _showDropZone(self, show):
        if show:
            self.drop_zone.show()
            self.drop_zone.setStyleSheet('''
                QLabel {
                    border: 2px dashed #0078d4;
                    border-radius: 10px;
                    padding: 20px;
                    color: #0078d4;
                    font-size: 14px;
                    background-color: rgba(0, 120, 212, 0.1);
                }
            ''')
        else:
            self.drop_zone.hide()

    def _loadSkills(self):
        self.skills_table.setRowCount(0)
        self.current_skills = self.skill_manager.scan_skills()
        self.displayed_skills = self.current_skills.copy()
        self._displaySkills(self.current_skills)
        self.select_all_cb.setChecked(False)
        self.status_label.setText(f'已加载 {len(self.current_skills)} 个Skills')

    def _displaySkills(self, skills):
        self.skills_table.setSortingEnabled(False)
        self.skills_table.setRowCount(len(skills))
        self.displayed_skills = skills

        for row, skill in enumerate(skills):
            checkbox = QTableWidgetItem()
            checkbox.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            checkbox.setCheckState(Qt.CheckState.Unchecked)
            self.skills_table.setItem(row, 0, checkbox)

            self.skills_table.setItem(row, 1, QTableWidgetItem(skill.get('name', '')))
            self.skills_table.setItem(row, 2, QTableWidgetItem(skill.get('description', '')[:60]))
            self.skills_table.setItem(row, 3, QTableWidgetItem(skill.get('version', '')))

            location_text = '用户' if skill.get('location') == 'user' else '系统'
            location_item = QTableWidgetItem(location_text)
            if skill.get('location') == 'system':
                location_item.setForeground(QColor('gray'))
            self.skills_table.setItem(row, 4, location_item)

            status_text = '启用' if skill.get('enabled', False) else '禁用'
            status_item = QTableWidgetItem(status_text)
            if not skill.get('enabled', False):
                status_item.setForeground(QColor('#ff6b6b'))
            else:
                status_item.setForeground(QColor('#51cf66'))
            self.skills_table.setItem(row, 5, status_item)

        self.skills_table.setSortingEnabled(True)

    def _getCheckedSkills(self):
        checked = []
        for row in range(self.skills_table.rowCount()):
            checkbox = self.skills_table.item(row, 0)
            if checkbox and checkbox.checkState() == Qt.CheckState.Checked:
                name = self.skills_table.item(row, 1).text()
                for skill in self.displayed_skills:
                    if skill.get('name') == name:
                        checked.append(skill)
                        break
        return checked

    def _updateSelectedCount(self):
        checked = self._getCheckedSkills()
        selected_rows = self.skills_table.selectionModel().selectedRows()
        count = max(len(checked), len(selected_rows))
        self.selected_label.setText(f'已选: {count}')

    def _showContextMenu(self, position):
        selected_rows = self.skills_table.selectionModel().selectedRows()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        if row >= len(self.displayed_skills):
            return

        skill = self.displayed_skills[row]
        menu = QMenu(self)

        edit_action = QAction('编辑 (Ctrl+Enter)', self)
        edit_action.triggered.connect(self._onEdit)
        menu.addAction(edit_action)

        enable_action = QAction('启用/禁用 (Ctrl+E)', self)
        enable_action.triggered.connect(self._onToggleEnable)
        menu.addAction(enable_action)

        menu.addSeparator()

        export_action = QAction('导出', self)
        export_action.triggered.connect(self._onExport)
        menu.addAction(export_action)

        export_selected_action = QAction('导出选中', self)
        export_selected_action.triggered.connect(self._onBatchExport)
        menu.addAction(export_selected_action)

        menu.addSeparator()

        copy_name_action = QAction('复制名称', self)
        copy_name_action.triggered.connect(lambda: self._copyToClipboard(skill.get('name', '')))
        menu.addAction(copy_name_action)

        copy_path_action = QAction('复制路径', self)
        copy_path_action.triggered.connect(lambda: self._copyToClipboard(skill.get('path', '')))
        menu.addAction(copy_path_action)

        menu.addSeparator()

        open_dir_action = QAction('打开目录', self)
        open_dir_action.triggered.connect(lambda: self._openDirectory(skill.get('base_dir', '')))
        menu.addAction(open_dir_action)

        menu.addSeparator()

        delete_action = QAction('删除 (Delete)', self)
        delete_action.triggered.connect(self._onDelete)
        menu.addAction(delete_action)

        menu.exec(self.skills_table.viewport().mapToGlobal(position))

    def _copyToClipboard(self, text):
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            self.status_label.setText(f'已复制: {text}')

    def _openDirectory(self, dir_path):
        if dir_path:
            import os
            import subprocess
            if os.path.exists(dir_path):
                if os.name == 'nt':
                    subprocess.run(['explorer', dir_path])
                else:
                    subprocess.run(['xdg-open', dir_path])

    def _onSelectAll(self, state):
        check_state = Qt.CheckState.Checked if state == 2 else Qt.CheckState.Unchecked
        for row in range(self.skills_table.rowCount()):
            checkbox = self.skills_table.item(row, 0)
            if checkbox:
                checkbox.setCheckState(check_state)
        self._updateSelectedCount()

    def _onSearch(self, text):
        if not text:
            self._displaySkills(self.current_skills)
            return

        filtered = [s for s in self.current_skills
                    if text.lower() in s.get('name', '').lower()
                    or text.lower() in s.get('description', '').lower()]
        self._displaySkills(filtered)

    def _onFilter(self, filter_text):
        if filter_text == '全部':
            self._displaySkills(self.current_skills)
        elif filter_text == '用户Skills':
            filtered = [s for s in self.current_skills if s.get('location') == 'user']
            self._displaySkills(filtered)
        elif filter_text == '系统Skills':
            filtered = [s for s in self.current_skills if s.get('location') == 'system']
            self._displaySkills(filtered)

    def _onSelectionChanged(self):
        self._updateSelectedCount()
        selected_rows = self.skills_table.selectionModel().selectedRows()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        if row < len(self.displayed_skills):
            skill = self.displayed_skills[row]
            self._showSkillDetail(skill)

    def _showSkillDetail(self, skill):
        metadata = self.skill_manager.get_skill_metadata(skill)
        for field, label in self.metadata_labels.items():
            value = metadata.get(field, '-')
            if isinstance(value, list):
                value = ', '.join(str(v) for v in value)
            elif not isinstance(value, str):
                value = str(value)
            label.setText(value)

        content = self.skill_manager.read_skill_content(skill.get('path', ''))
        self.detail_text.setPlainText(content)

    def _onEdit(self):
        selected_rows = self.skills_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, '警告', '请先选择一个Skill')
            return

        row = selected_rows[0].row()
        if row < len(self.displayed_skills):
            skill = self.displayed_skills[row]
            skill_path = skill.get('path', '')
            if skill_path:
                dialog = SkillEditorDialog(self, skill_path=skill_path)
                dialog.exec()
                self._loadSkills()

    def _onToggleEnable(self):
        selected_rows = self.skills_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, '警告', '请先选择一个Skill')
            return

        row = selected_rows[0].row()
        if row < len(self.displayed_skills):
            skill = self.displayed_skills[row]
            if skill.get('location') == 'system':
                QMessageBox.warning(self, '警告', '无法修改系统Skills')
                return

            success = self.skill_manager.toggle_skill(skill)
            if success:
                self._loadSkills()
            else:
                QMessageBox.critical(self, '错误', '更新Skill状态失败')

    def _onExport(self):
        selected_rows = self.skills_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, '警告', '请先选择一个Skill')
            return

        row = selected_rows[0].row()
        if row < len(self.displayed_skills):
            skill = self.displayed_skills[row]
            file_path, _ = QFileDialog.getSaveFileName(
                self, '导出Skill',
                f"{skill.get('name', 'skill')}.zip",
                'ZIP文件 (*.zip)'
            )
            if file_path:
                success = self.skill_manager.export_skill(skill, file_path)
                if success:
                    QMessageBox.information(self, '成功', f'Skill已导出到: {file_path}')
                else:
                    QMessageBox.critical(self, '错误', '导出Skill失败')

    def _onDelete(self):
        selected_rows = self.skills_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, '警告', '请先选择一个Skill')
            return

        row = selected_rows[0].row()
        if row < len(self.displayed_skills):
            skill = self.displayed_skills[row]
            if skill.get('location') == 'system':
                QMessageBox.warning(self, '警告', '无法删除系统Skills')
                return

            reply = QMessageBox.question(
                self, '确认删除',
                f"确定要删除Skill '{skill.get('name', '')}' 吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                success = self.skill_manager.delete_skill(skill)
                if success:
                    self._loadSkills()

    def _onBatchEnable(self):
        skills = self._getCheckedSkills()
        if not skills:
            QMessageBox.warning(self, '警告', '请先勾选要操作的Skills')
            return

        user_skills = [s for s in skills if s.get('location') == 'user']
        if not user_skills:
            QMessageBox.warning(self, '警告', '没有可操作的用户Skills')
            return

        success_count = 0
        for skill in user_skills:
            if not skill.get('enabled', False):
                if self.skill_manager.toggle_skill(skill):
                    success_count += 1

        self._loadSkills()
        QMessageBox.information(self, '完成', f'已启用 {success_count} 个Skills')

    def _onBatchDisable(self):
        skills = self._getCheckedSkills()
        if not skills:
            QMessageBox.warning(self, '警告', '请先勾选要操作的Skills')
            return

        user_skills = [s for s in skills if s.get('location') == 'user']
        if not user_skills:
            QMessageBox.warning(self, '警告', '没有可操作的用户Skills')
            return

        success_count = 0
        for skill in user_skills:
            if skill.get('enabled', False):
                if self.skill_manager.toggle_skill(skill):
                    success_count += 1

        self._loadSkills()
        QMessageBox.information(self, '完成', f'已禁用 {success_count} 个Skills')

    def _onBatchExport(self):
        skills = self._getCheckedSkills()
        if not skills:
            QMessageBox.warning(self, '警告', '请先勾选要导出的Skills')
            return

        dir_path = QFileDialog.getExistingDirectory(self, '选择导出目录')
        if not dir_path:
            return

        success_count = 0
        for skill in skills:
            output_path = f"{dir_path}/{skill.get('name', 'skill')}.zip"
            if self.skill_manager.export_skill(skill, output_path):
                success_count += 1

        QMessageBox.information(self, '完成', f'已导出 {success_count} 个Skills到: {dir_path}')

    def _onBatchDelete(self):
        skills = self._getCheckedSkills()
        if not skills:
            QMessageBox.warning(self, '警告', '请先勾选要删除的Skills')
            return

        user_skills = [s for s in skills if s.get('location') == 'user']
        if not user_skills:
            QMessageBox.warning(self, '警告', '没有可删除的用户Skills')
            return

        reply = QMessageBox.question(
            self, '确认批量删除',
            f"确定要删除选中的 {len(user_skills)} 个Skills吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success_count = 0
            for skill in user_skills:
                if self.skill_manager.delete_skill(skill):
                    success_count += 1

            self._loadSkills()
            QMessageBox.information(self, '完成', f'已删除 {success_count} 个Skills')

    def _onImport(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, '导入Skill', '',
            'ZIP文件 (*.zip);;所有文件 (*)'
        )
        if file_path:
            success = self.skill_manager.import_skill(file_path)
            if success:
                self._loadSkills()
                QMessageBox.information(self, '成功', 'Skill已导入')
            else:
                QMessageBox.critical(self, '错误', '导入Skill失败')

    def refresh(self):
        self._loadSkills()
