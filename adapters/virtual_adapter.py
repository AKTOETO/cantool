import threading
import can
from .base_adapter import CANAdapter

class VirtualAdapter(CANAdapter):
    def __init__(self):
        super().__init__()
        self.bus = None
        self.stop_event = threading.Event()
        self.read_thread = None

    def connect(self, params: dict) -> bool:
        interface = params.get("interface", "vcan0")
        try:
            # Убеждаемся, что флаг остановки сброшен перед запуском
            self.stop_event.clear()
            
            self.bus = can.interface.Bus(channel=interface, bustype='socketcan')
            
            self.read_thread = threading.Thread(target=self._read_loop, daemon=True)
            self.read_thread.start()
            
            print(f"Connected to {interface}")
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def _read_loop(self):
        while not self.stop_event.is_set():
            try:
                # Если шина была закрыта извне, recv может выкинуть ошибку
                if self.bus is None:
                    print("Virtual Adapter: Bus is None, stopping read loop.")
                    break
                    
                msg = self.bus.recv(0.1)
                if msg:
                    self.frame_received.emit({
                        'id': msg.arbitration_id,
                        'data': bytes(msg.data),
                        'dlc': msg.dlc
                    })
            except Exception as e:
                # Если мы в процессе остановки, игнорируем ошибки сокета
                if self.stop_event.is_set():
                    break
                print(f"Read error: {e}")

    def disconnect(self):
        # 1. Сначала сигнализируем потоку о необходимости остановиться
        self.stop_event.set()
        
        # 2. Ждем завершения потока (необязательно, но надежно)
        if self.read_thread and self.read_thread.is_alive():
            self.read_thread.join(timeout=0.2)
        
        # 3. Только теперь закрываем шину и удаляем объект
        if self.bus:
            try:
                self.bus.shutdown()
            except:
                pass
            self.bus = None
        print("Virtual adapter disconnected safely")

    def send(self, frame_id: int, data: bytes):
        if self.bus:
            msg = can.Message(arbitration_id=frame_id, data=data, is_extended_id=False)
            self.bus.send(msg)