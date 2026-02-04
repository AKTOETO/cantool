import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
# from core_logic.system_manager import SystemManager
from scenes.connection_scene import ConnectionScene
from scenes.workspace_scene import WorkspaceScene
from core_logic.app_core import core

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAN Tool Pro")
        self.resize(1200, 800)
        
        self.system_manager = core.system_manager # Берем из единого ядра
        
        # Стэк для переключения сцен
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        # Инициализация сцен
        self.conn_scene = ConnectionScene(self.system_manager, self.show_workspace)
        self.work_scene = WorkspaceScene(self.system_manager)
        
        self.stack.addWidget(self.conn_scene)
        self.stack.addWidget(self.work_scene)

    def show_workspace(self):
        self.stack.setCurrentWidget(self.work_scene)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())