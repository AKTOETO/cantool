from PyQt6.QtCore import QObject, pyqtSignal

class AdapterStats(QObject):
    updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.rx_count = 0
        self.rx_bytes = 0
        self.tx_count = 0
        self.tx_bytes = 0
        self.updated.emit()

    def record_rx(self, frame):
        self.rx_count += 1
        # В CAN DLC — это длина данных в байтах
        self.rx_bytes += len(frame.get('data', b''))
        self.updated.emit()

    def record_tx(self, data: bytes):
        self.tx_count += 1
        self.tx_bytes += len(data)
        self.updated.emit()

    @property
    def avg_tx_size(self):
        """Средний размер отправленных данных в байтах"""
        return self.tx_bytes / self.tx_count if self.tx_count > 0 else 0

    @staticmethod
    def format_size(bytes_count):
        """Вспомогательный метод для красивого вывода"""
        if bytes_count < 1024:
            return f"{bytes_count} B"
        elif bytes_count < 1024**2:
            return f"{bytes_count/1024:.2f} KB"
        else:
            return f"{bytes_count/1024**2:.2f} MB"