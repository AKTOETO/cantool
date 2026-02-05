import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from core_logic.system_manager import SystemManager
from scenes.connection_scene import ConnectionScene
from scenes.workspace_scene import WorkspaceScene
from core_logic.app_core import core

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAN Tool")
        self.resize(1200, 800)

        # Применяем глобальный стиль
        self.apply_global_style()

        # Создаем сердце системы
        self.system_manager = core.system_manager

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
    
    def apply_global_style(self):
        self.setStyleSheet("""
            /* Базовый цвет фона и текста */
            QWidget {
                font-size: 14px;
                background-color: #1e1e1e;
                color: #d4d4d4;
            }

            /* Кнопки: темный градиент и скругление */
            QPushButton {
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #454545;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #454545;
                border-color: #007acc; /* Синий акцент при наведении */
            }
            QPushButton:pressed {
                background-color: #252525;
            }

            /* Поля ввода и комбобоксы */
            QLineEdit, QComboBox, QSpinBox {
                background-color: #2d2d2d;
                border: 1px solid #3c3c3c;
                border-radius: 6px;
                padding: 5px;
                color: #569cd6; /* Светло-синий цвет для вводимых данных */
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                selection-background-color: #007acc;
            }

            /* Таблицы и деревья мониторинга */
            QTableWidget, QTreeWidget, QHeaderView::section {
                background-color: #252525;
                alternate-background-color: #2a2a2a;
                border: 1px solid #3c3c3c;
                gridline-color: #333333;
            }
            QTableWidget {
                border-radius: 10px;
            }
            QHeaderView::section {
                background-color: #333333;
                color: #858585;
                padding: 5px;
                font-weight: bold;
            }

            /* Вкладки (Tabs) */
            QTabWidget::pane {
                border: 1px solid #3c3c3c;
                border-radius: 10px;
                top: -1px;
                background-color: #252525;
            }
            QTabBar::tab {
                background-color: #1e1e1e;
                border: 1px solid #3c3c3c;
                border-bottom: none;
                padding: 10px 20px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                color: #858585;
            }
            QTabBar::tab:selected {
                background-color: #252525;
                color: #007acc;
                font-weight: bold;
            }

            /* Панели и карточки */
            QGroupBox, QFrame#status_panel {
                border: 2px solid #3c3c3c;
                border-radius: 12px;
                margin-top: 15px;
                background-color: #252525;
            }
            QGroupBox::title {
                color: #007acc;
                subcontrol-origin: margin;
                left: 15px;
                padding: 3px 3px;
                margin-top: -10px;
                font-weight: bold;
                border: 1px solid #3c3c3c;
                border-radius: 8px;
                background-color: #1e1e1e;
            }

            /* Скроллбары (сделаем их менее заметными) */
            QScrollBar:vertical {
                background: #1e1e1e;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #454545;
                min-height: 20px;
                border-radius: 6px;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())