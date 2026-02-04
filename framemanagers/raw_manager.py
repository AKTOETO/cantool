from PyQt6.QtCore import pyqtSignal
from .base_manager import BaseFrameManager

class RawManager(BaseFrameManager):
    # Сигнал для вкладки RAW мониторинга 
    frame_processed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.history = []  # Хранилище для истории кадров 

    def process_incoming(self, frame: dict):
        print(f"RawManager: Обработка входящего кадра: {frame}")
        """
        Принимает сырой кадр от SystemManager и транслирует его подписчикам.
        Здесь можно добавить логику записи в лог или расчет битрейта.
        """
        # В базовой реализации просто пересылаем кадр 
        self.frame_processed.emit(frame)

    def load_config(self):
        """Для RawManager конфигурационный файл обычно не требуется."""
        return True