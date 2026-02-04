# scenes/connection_scene.py
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QListWidget, QGroupBox, QFormLayout, QComboBox, QPushButton, QLineEdit

class ConnectionScene(QWidget):
    def __init__(self, system_manager, on_connected):
        super().__init__()
        self.sm = system_manager
        self.on_connected = on_connected
        
        layout = QHBoxLayout(self)
        self.adapter_list = QListWidget()
        self.adapter_list.addItems(["Loopback", "Candlelight", "Virtual"])
        self.adapter_list.currentTextChanged.connect(self.update_settings_ui)
        layout.addWidget(self.adapter_list)

        self.settings_group = QGroupBox("Adapter Settings")
        self.form = QFormLayout(self.settings_group)
        self.params_widgets = {} # Храним виджеты настроек
        layout.addWidget(self.settings_group)

        self.btn_connect = QPushButton("Connect")
        self.btn_connect.clicked.connect(self.try_connect)
        layout.addWidget(self.btn_connect)
        
        self.update_settings_ui("Loopback")

    def update_settings_ui(self, adapter_type):
        # Очистка старых настроек
        while self.form.count():
            child = self.form.takeAt(0)
            if child:
                widget = child.widget()
                if widget: widget.deleteLater()
        self.params_widgets = {}

        # Формируем поля под конкретный тип
        if adapter_type == "Loopback":
            label = QLineEdit("Internal")
            label.setEnabled(False)
            self.form.addRow("Mode:", label)
        elif adapter_type == "Candlelight":
            port = QComboBox(); port.addItems(["can0", "can1"])
            br = QComboBox(); br.addItems(["500000", "1000000"])
            self.form.addRow("Port:", port)
            self.form.addRow("Baudrate:", br)
            self.params_widgets = {"port": port, "br": br}

    def try_connect(self):
        selected = self.adapter_list.currentItem()
        if selected:
            # Собираем параметры из виджетов
            params = {k: v.currentText() if isinstance(v, QComboBox) else v.text() 
                      for k, v in self.params_widgets.items()}
            
            # Теперь вызываем с правильным количеством аргументов
            if self.sm.set_adapter(selected.text(), params):
                self.on_connected()