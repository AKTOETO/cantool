from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, 
                             QHBoxLayout, QFileDialog, QFrame)
from PyQt6.QtCore import Qt
from core_logic.app_core import core

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Системные настройки")
        self.setModal(True)
        self.setMinimumWidth(550)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # --- Секция DBC ---
        layout.addWidget(QLabel("<b>Конфигурация DBC</b>"))
        dbc_frame = QFrame()
        dbc_frame.setFrameShape(QFrame.Shape.StyledPanel)
        dbc_lay = QHBoxLayout(dbc_frame)
        
        self.dbc_label = QLabel(core.dbc.file_path if core.dbc.is_loaded() else "Файл не выбран")
        self.dbc_label.setWordWrap(True)
        btn_dbc = QPushButton("Обзор...")
        btn_dbc.clicked.connect(lambda: self.select_file("DBC"))
        
        dbc_lay.addWidget(self.dbc_label, 1)
        dbc_lay.addWidget(btn_dbc)
        layout.addWidget(dbc_frame)

        # --- Секция VSS ---
        layout.addWidget(QLabel("<b>Конфигурация VSS</b>"))
        vss_frame = QFrame()
        vss_frame.setFrameShape(QFrame.Shape.StyledPanel)
        vss_lay = QHBoxLayout(vss_frame)
        
        self.vss_label = QLabel(core.vss.file_path if core.vss.is_loaded() else "Файл не выбран")
        self.vss_label.setWordWrap(True)
        btn_vss = QPushButton("Обзор...")
        btn_vss.clicked.connect(lambda: self.select_file("VSS"))
        
        vss_lay.addWidget(self.vss_label, 1)
        vss_lay.addWidget(btn_vss)
        layout.addWidget(vss_frame)

        # --- Кнопки управления ---
        spacer = QFrame()
        layout.addWidget(spacer)
        
        btns_layout = QHBoxLayout()
        btn_close = QPushButton("Закрыть")
        btn_close.clicked.connect(self.accept)
        btn_close.setDefault(True)
        
        btns_layout.addStretch()
        btns_layout.addWidget(btn_close)
        layout.addLayout(btns_layout)

    def select_file(self, mode):
        """Метод выбора файла и обновления соответствующего менеджера"""
        filters = {
            "DBC": "CAN Database (*.dbc)",
            "VSS": "Vehicle Signal Spec (*.json *.vspec *.vss)"
        }
        
        path, _ = QFileDialog.getOpenFileName(
            self, 
            f"Выберите файл {mode}", 
            "", 
            filters.get(mode, "All Files (*)")
        )

        if path:
            if mode == "DBC":
                core.dbc.set_config(path)
                self.dbc_label.setText(path)
            elif mode == "VSS":
                core.vss.set_config(path)
                self.vss_label.setText(path)