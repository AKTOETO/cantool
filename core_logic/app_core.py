from .system_manager import SystemManager
from framemanagers.dbc_manager import DBCManager
from framemanagers.vss_manager import VSSManager
from framemanagers.raw_manager import RawManager

class AppCore:
    _instance = None
    system_manager: SystemManager
    dbc: DBCManager
    vss: VSSManager
    raw: RawManager

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppCore, cls).__new__(cls)
            # Инициализируем менеджеры один раз
            cls._instance.system_manager = SystemManager()
            cls._instance.dbc = DBCManager()
            cls._instance.vss = VSSManager()
            cls._instance.raw = RawManager()
        return cls._instance

# Глобальный объект для импорта
core = AppCore()