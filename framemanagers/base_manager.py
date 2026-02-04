from abc import ABCMeta, abstractmethod
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.sip import wrappertype

class CombinedMeta(wrappertype, ABCMeta):
    pass

class BaseFrameManager(QObject, metaclass=CombinedMeta):
    # Сигнал, на который подписываются соответствующие вкладки
    # Передает словарь с обработанными данными
    frame_processed = pyqtSignal(dict)
    # Новый сигнал для уведомления об обновлении конфигурации
    config_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.file_path = None

    def is_loaded(self) -> bool:
        """Проверка, загружен ли файл конфигурации (DBC/VSS)"""
        return self.file_path is not None

    @abstractmethod
    def process_incoming(self, frame: dict):
        """Метод для обработки входящего CAN-кадра"""
        pass

    def set_config(self, path: str):
        """Установка пути к файлу конфигурации"""
        self.file_path = path
        if self.load_config():
            self.config_updated.emit()
        else:
            print(f"Ошибка загрузки конфигурации из {path}")

    @abstractmethod
    def load_config(self) -> bool:
        """
        Логика парсинга файла конфигурации
        
        :return: True при успешной загрузке, иначе False
        :rtype: bool
        """
        pass