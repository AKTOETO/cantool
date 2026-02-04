import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from core_logic.system_manager import SystemManager
from scenes.connection_scene import ConnectionScene
from scenes.workspace_scene import WorkspaceScene

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gemini CAN Analyzer")
        self.resize(1200, 800)

        # Создаем сердце системы
        self.system_manager = SystemManager()

        # Запускаем первую сцену
        self.show_connection_scene()

    def show_connection_scene(self):
        """Окно выбора адаптера"""
        # Создаем сцену (больше не передаем callback в __init__)
        self.connection_scene = ConnectionScene(self.system_manager)
        
        # Подписываемся на сигнал успешного подключения
        self.connection_scene.connected.connect(self.show_workspace_scene)
        
        self.setCentralWidget(self.connection_scene)

    def show_workspace_scene(self):
        """Основное рабочее окно мониторинга"""
        # Создаем рабочую сцену
        self.workspace_scene = WorkspaceScene(self.system_manager)
        
        # Подписываемся на сигнал выхода
        self.workspace_scene.exit_requested.connect(self.show_connection_scene)
        
        self.setCentralWidget(self.workspace_scene)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())