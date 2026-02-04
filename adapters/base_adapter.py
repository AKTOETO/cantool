from abc import ABC, ABCMeta, abstractmethod
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.sip import wrappertype

class CombinedMeta(wrappertype, ABCMeta):
    pass

class CANAdapter(QObject, metaclass=CombinedMeta):
    # Сигнал, который GUI будет слушать для получения кадров
    # dict содержит: {'id': int, 'data': bytes, 'dlc': int}
    frame_received = pyqtSignal(dict)

    @abstractmethod
    def connect(self, params: dict) -> bool:
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def send(self, frame_id: int, data: bytes):
        pass