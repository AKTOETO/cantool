from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from core_logic.app_core import core

class RawTransmitTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # ID
        id_lay = QHBoxLayout()
        id_lay.addWidget(QLabel("ID (Hex):"))
        self.id_input = QLineEdit("123")
        id_lay.addWidget(self.id_input)
        layout.addLayout(id_lay)
        
        # Data
        data_lay = QHBoxLayout()
        data_lay.addWidget(QLabel("Data (Hex):"))
        self.data_input = QLineEdit("DE AD BE EF")
        data_lay.addWidget(self.data_input)
        layout.addLayout(data_lay)
        
        self.btn_send = QPushButton("Send Frame")
        self.btn_send.clicked.connect(self.on_send)
        layout.addWidget(self.btn_send)
        
        layout.addStretch()

    def on_send(self):
        try:
            f_id = int(self.id_input.text(), 16)
            # Убираем пробелы и переводим в байты
            f_data = bytes.fromhex(self.data_input.text().replace(" ", ""))

            # Отправляем через системный менеджер
            core.system_manager.send_frame(f_id, f_data)

        except ValueError:
            print("Ошибка: Неверный формат ID или Data")

class DBCTransmitTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("DBC Message Generator - Coming Soon..."))

class VSSTransmitTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("VSS Node Selector - Coming Soon..."))