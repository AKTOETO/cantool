from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget,
                             QTableWidgetItem, QHeaderView, QTreeWidget,
                             QTreeWidgetItem, QPushButton, QVBoxLayout,
                             QLabel, QWidget, QStackedWidget)
from PyQt6.QtCore import Qt
from datetime import datetime
from core_logic.app_core import core

class ConfigPlaceholder(QWidget):
    """Простой виджет-заглушка для вкладок, которые еще не реализованы."""
    def __init__(self, text):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(QLabel(text + "\n\nНастройте соответствующий файл в настройках."))
        btn = QPushButton("Открыть настройки")

        btn.clicked.connect(self.open_settings)
        layout.addWidget(btn)

    def open_settings(self):
        from core_logic.settings_dialog import SettingsDialog
        SettingsDialog(self).exec()

class RawMonitorTab(QWidget):
    """Вкладка для отображения сырых кадров в виде таблицы."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Таблица на 4 колонки: Time, ID, DLC, Data
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Time", "ID (Hex)", "DLC", "Data (Hex)"])

        # Растягиваем колонки, чтобы они занимали всё место
        header = self.table.horizontalHeader()
        assert header is not None
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # Подписываемся на DBC менеджер 
        core.raw.frame_processed.connect(self.add_frame)

    def add_frame(self, frame: dict):
        """
        frame: {'id': int, 'data': bytes, 'dlc': int}
        """
        # Если загружен DBC, можем сразу попробовать декодировать
        if core.dbc.is_loaded():
            decoded = core.dbc.process_frame(frame['id'], frame['data'])
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(datetime.now().strftime("%H:%M:%S.%f")[:-3]))
        self.table.setItem(row, 1, QTableWidgetItem(f"0x{frame['id']:03X}"))
        self.table.setItem(row, 2, QTableWidgetItem(str(frame['dlc'])))
        self.table.setItem(row, 3, QTableWidgetItem(frame['data'].hex(' ').upper()))
        self.table.scrollToBottom()

class DBCMonitorTab(QWidget):
    """Вкладка для отображения декодированных сигналов из DBC."""
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.stack = QStackedWidget()
        
        # Виджет 0: Заглушка
        self.placeholder = ConfigPlaceholder("DBC файл не загружен")
        
        # Виджет 1: Дерево данных
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Message / Signal", "Value", "Unit"])
        
        self.stack.addWidget(self.placeholder)
        self.stack.addWidget(self.tree)
        self.main_layout.addWidget(self.stack)
        
        self.msg_items = {}

        # Подписки
        core.dbc.frame_processed.connect(self.update_view)
        core.dbc.config_updated.connect(self.refresh_state)
        
        # Устанавливаем начальное состояние
        self.refresh_state()

    def refresh_state(self):
        """Переключает виджет в зависимости от наличия конфига"""
        if core.dbc.is_loaded():
            self.stack.setCurrentIndex(1)
        else:
            self.stack.setCurrentIndex(0)

    def update_view(self, data: dict):
        """
        data приходит в формате: {'raw': {...}, 'signals': {'SignalName': Value, ...}}
        """
        raw_frame = data['raw']
        signals = data['signals']
        msg_id = raw_frame['id']
        
        # Если такого сообщения еще нет в дереве, создаем корневой элемент
        if msg_id not in self.msg_items:
            root = QTreeWidgetItem(self.tree)
            root.setText(0, f"ID: {hex(msg_id)}")
            self.msg_items[msg_id] = root
        
        root_item = self.msg_items[msg_id]
        
        # Обновляем сигналы (дочерние элементы)
        # В реальном DBC тут еще будут Unit (физ. величины)
        for sig_name, val in signals.items():
            # Ищем, есть ли уже такой сигнал в ветке
            found = False
            for i in range(root_item.childCount()):
                child = root_item.child(i)
                if child.text(0) == sig_name:
                    child.setText(1, str(val))
                    found = True
                    break
            
            if not found:
                child = QTreeWidgetItem(root_item)
                child.setText(0, sig_name)
                child.setText(1, str(val))
                child.setText(2, "-") # Заглушка для Unit

class VSSMonitorTab(QWidget):
    """Вкладка для отображения данных из VSS в виде дерева."""
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.stack = QStackedWidget()
        
        self.placeholder = ConfigPlaceholder("VSS файл не загружен")
        
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["VSS Path", "Value"])
        
        self.stack.addWidget(self.placeholder)
        self.stack.addWidget(self.tree)
        self.main_layout.addWidget(self.stack)
        
        self.nodes = {}

        core.vss.frame_processed.connect(self.update_tree)
        core.vss.config_updated.connect(self.refresh_state)
        
        self.refresh_state()

    def refresh_state(self):
        if core.vss.is_loaded():
            self.stack.setCurrentIndex(1)
        else:
            self.stack.setCurrentIndex(0)

    def update_tree(self, vss_data: dict):
        """
        vss_data приходит в формате: {"Vehicle.Speed": 100, ...}
        """
        for path, value in vss_data.items():
            if path not in self.nodes:
                item = QTreeWidgetItem(self.tree)
                item.setText(0, path)
                self.nodes[path] = item
            
            self.nodes[path].setText(1, str(value))