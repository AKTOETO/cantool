from .base_adapter import CANAdapter

class LoopbackAdapter(CANAdapter):
    def connect(self, params: dict) -> bool:
        print("Loopback подключен")
        return True

    def disconnect(self):
        print("Loopback отключен")

    def send(self, frame_id: int, data: bytes):
        # Эмулируем мгновенный прием отправленного кадра
        self.frame_received.emit({
            'id': frame_id,
            'data': data,
            'dlc': len(data)
        })