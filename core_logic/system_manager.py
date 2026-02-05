from PyQt6.QtCore import QObject, pyqtSignal
from adapters.loopback_adapter import LoopbackAdapter
from adapters.virtual_adapter import VirtualAdapter
from core_logic.adapter_stats import AdapterStats

class SystemManager(QObject):
    # Сигнал для GUI. Передает расширенный словарь с данными.
    received = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.adapter = None
        self.stats = AdapterStats() # Добавляем объект статистики

    def set_adapter(self, adapter_type, params):
        """
        Устанавливает и подключает адаптер по типу и параметрам.
        
        :param adapter_type: Тип адаптера (например, "Loopback", "Virtual")
        :param params: Параметры подключения адаптера
        :return: True при успешном подключении, иначе False
        :rtype: bool
        """

        # Импортируем здесь, чтобы избежать циклического импорта
        from .app_core import core
        
        if "Loopback" in adapter_type:
            self.adapter = LoopbackAdapter()
        elif "Virtual" in adapter_type:
            self.adapter = VirtualAdapter()
        else:
            self.adapter = None
            print(f"Неизвестный тип адаптера: {adapter_type}")
            return False
        # Тут добавятся другие адаптеры (Candlelight и т.д.)
        
        if self.adapter:
            self.adapter.frame_received.connect(self._handle_incoming_frame)
            return self.adapter.connect(params)
        return False

    def _handle_incoming_frame(self, frame: dict):
        """Внутренний обработчик: обогащение данных через DBC/VSS"""
        self.stats.record_rx(frame) # Увеличиваем счетчик принятых кадров

        # Рассылка всем менеджерам
        from .app_core import core
        core.raw.process_incoming(frame)
        core.dbc.process_incoming(frame)
        core.vss.process_incoming(frame)

        # Отправляем в GUI уже 'умный' кадр
        self.received.emit(frame)

    def send_frame(self, frame_id, data):
        if self.adapter:
            self.adapter.send(frame_id, data)
            self.stats.record_tx(data) # Увеличиваем счетчик отправленных кадров
        else:
            print("Нет подключенного адаптера для отправки кадра.")