# scenes/connection_scene.py
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QTableWidget, 
                             QTableWidgetItem, QGroupBox, QFormLayout, QComboBox, 
                             QPushButton, QLineEdit, QHeaderView, QDialog, QMessageBox)
from PyQt6.QtCore import pyqtSignal
from adapters.registry import ADAPTER_TYPES
from core_logic.system_manager import SystemManager

class AddAdapterDialog(QDialog):
    def __init__(self, existing_names, parent=None):
        super().__init__(parent)
        self.existing_names = existing_names
        self.setWindowTitle("Создать новый адаптер")
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Напр: MyCAN_Adapter")
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(ADAPTER_TYPES.keys())
        
        form.addRow("Имя адаптера:", self.name_input)
        form.addRow("Тип адаптера:", self.type_combo)
        layout.addLayout(form)
        
        # Кнопки
        btns = QHBoxLayout()
        self.btn_ok = QPushButton("Добавить")
        self.btn_ok.clicked.connect(self.validate_and_accept)
        btn_cancel = QPushButton("Отмена")
        btn_cancel.clicked.connect(self.reject)
        
        btns.addWidget(self.btn_ok)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)

    def validate_and_accept(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Имя не может быть пустым")
            return
        
        if name in self.existing_names:
            QMessageBox.warning(self, "Ошибка", f"Адаптер с именем '{name}' уже существует")
            return
            
        self.accept()

    def get_data(self):
        return self.name_input.text().strip(), self.type_combo.currentText()

"""Сцена подключения CAN адаптера"""
class ConnectionScene(QWidget):
    connected = pyqtSignal()

    def __init__(self, system_manager : SystemManager):
        super().__init__()
        self.sm = system_manager
        self.params_widgets = {}

        main_layout = QHBoxLayout(self)

        # Левая часть: Список и кнопки
        left_layout = QVBoxLayout()
        
        self.adapter_table = QTableWidget(0, 2)
        self.adapter_table.setHorizontalHeaderLabels(["Имя", "Тип"])
        header = self.adapter_table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.adapter_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.adapter_table.itemSelectionChanged.connect(self.on_adapter_selected)
        
        # Кнопки под таблицей
        btn_layout = QHBoxLayout()
        self.btn_connect = QPushButton("Connect")
        self.btn_connect.clicked.connect(self.try_connect)
        
        self.btn_create = QPushButton("Создать")
        self.btn_create.clicked.connect(self.add_virtual_adapter)
        
        btn_layout.addWidget(self.btn_connect)
        btn_layout.addWidget(self.btn_create)

        left_layout.addWidget(self.adapter_table)
        left_layout.addLayout(btn_layout)

        # Правая часть: Настройки
        self.settings_group = QGroupBox("Adapter Settings")
        self.form = QFormLayout(self.settings_group)
        
        main_layout.addLayout(left_layout, 2)
        main_layout.addWidget(self.settings_group, 1)

        # Добавим дефолтный адаптер для теста
        self.add_to_table("System VCAN", "Virtual (SocketCAN)")
        self.add_to_table("Loopback 1", "Loopback")

    def add_to_table(self, name, a_type):
        row = self.adapter_table.rowCount()
        self.adapter_table.insertRow(row)
        self.adapter_table.setItem(row, 0, QTableWidgetItem(name))
        self.adapter_table.setItem(row, 1, QTableWidgetItem(a_type))

    def add_virtual_adapter(self):
        # Логика создания нового программного адаптера
        # 1. Собираем список всех текущих имен из таблицы для проверки уникальности
        existing_names = []
        for row in range(self.adapter_table.rowCount()):
            item = self.adapter_table.item(row, 0)
            if item:
                existing_names.append(item.text())
        
        # 2. Вызываем диалог
        dialog = AddAdapterDialog(existing_names, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, a_type = dialog.get_data()
            # 3. Добавляем в таблицу
            self.add_to_table(name, a_type)
            
            # Опционально: сразу выбираем новую строку
            last_row = self.adapter_table.rowCount() - 1
            self.adapter_table.selectRow(last_row)

    def on_adapter_selected(self):
        selection_model = self.adapter_table.selectionModel()
        if selection_model is None: return
        selected_rows = selection_model.selectedRows()
        if not selected_rows: return
        
        item = self.adapter_table.item(selected_rows[0].row(), 1)
        if item is None:
            return
        a_type = item.text()
        self.update_settings_ui(a_type)

    def update_settings_ui(self, adapter_type):
        while self.form.count():
            item = self.form.takeAt(0)
            widget = item.widget() if item else None
            if widget is not None:
                widget.deleteLater()
        self.params_widgets = {}

        from adapters.registry import ADAPTER_TYPES
        config = ADAPTER_TYPES.get(adapter_type, {"params": {}})
        
        for param_name, value in config["params"].items():
            if isinstance(value, list):
                widget = QComboBox()
                widget.addItems(value)
            else:
                widget = QLineEdit(str(value))
            
            self.form.addRow(f"{param_name.capitalize()}:", widget)
            self.params_widgets[param_name] = widget

    def try_connect(self):
        selection_model = self.adapter_table.selectionModel()
        if selection_model is None: return
        selected_rows = selection_model.selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            name_item = self.adapter_table.item(row, 0)
            type_item = self.adapter_table.item(row, 1)
            if name_item is None or type_item is None: return
            name = name_item.text()
            a_type = type_item.text()
            
            params = {k: (v.currentText() if isinstance(v, QComboBox) else v.text()) 
                      for k, v in self.params_widgets.items()}
            
            if self.sm.set_adapter(a_type, params):
                self.connected.emit()