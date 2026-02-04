from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, 
                             QLabel, QPushButton, QFrame, QDialog, QFileDialog)
from PyQt6.QtCore import Qt, pyqtSignal
from core_logic.system_manager import SystemManager
from tabs.monitor_tabs import RawMonitorTab, DBCMonitorTab, VSSMonitorTab
from tabs.transmit_tabs import RawTransmitTab, DBCTransmitTab, VSSTransmitTab

class WorkspaceScene(QWidget):
    # Сигнал для уведомления главного окна о необходимости сменить сцену
    exit_requested = pyqtSignal()

    def __init__(self, system_manager: SystemManager):
        super().__init__()
        self.sm = system_manager
        
        # Основной вертикальный макет
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)

        # 1. Верхняя панель управления
        top_panel = QHBoxLayout()
        
        # Кнопка выхода
        self.exit_btn = QPushButton("🚪 Выход")
        self.exit_btn.setToolTip("Отключиться и выйти в меню")
        self.exit_btn.clicked.connect(self.on_exit_clicked)
        top_panel.addWidget(self.exit_btn)
        
        top_panel.addStretch()
        
        #  Настройки системы
        self.settings_btn = QPushButton("⚙ Настройки")
        self.settings_btn.setToolTip("Настройки системы")
        self.settings_btn.clicked.connect(self.open_settings)
        top_panel.addWidget(self.settings_btn)
        
        main_layout.addLayout(top_panel)
        # 2. Область контента
        content_layout = QHBoxLayout()
        
        # Левая колонка: Мониторинг
        self.monitor_tabs = QTabWidget()
        self.monitor_tabs.addTab(RawMonitorTab(), "RAW monitor")
        self.monitor_tabs.addTab(DBCMonitorTab(), "DBC monitor")
        self.monitor_tabs.addTab(VSSMonitorTab(), "VSS monitor")
        
        # Центральная колонка: Отправка
        self.transmit_tabs = QTabWidget()
        self.transmit_tabs.addTab(RawTransmitTab(), "RAW transmit")
        self.transmit_tabs.addTab(DBCTransmitTab(), "DBC transmit")
        self.transmit_tabs.addTab(VSSTransmitTab(), "VSS transmit")

        # Правая колонка: Статус адаптера
        self.status_panel = QFrame()
        self.status_panel.setFrameShape(QFrame.Shape.StyledPanel)
        self.status_panel.setFixedWidth(200)
        status_layout = QVBoxLayout(self.status_panel)
        status_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Статусные метки для отображения информации об адаптере и статистики
        self.lbl_status = QLabel("Status: Connected")
        self.lbl_rx = QLabel("RX: 0")
        self.lbl_tx = QLabel("TX: 0")
        self.lbl_avg_size = QLabel("Avg Data: 0 b")

        # Добавляем их в статусную панель
        status_layout.addWidget(QLabel("<b>Adapter Info</b>"))
        status_layout.addWidget(self.lbl_status)
        status_layout.addWidget(QLabel("<br><b>Statistics</b>"))
        status_layout.addWidget(self.lbl_rx)
        status_layout.addWidget(self.lbl_tx)
        status_layout.addWidget(self.lbl_avg_size)

        # Добавляем все колонки в основной контент
        content_layout.addWidget(self.monitor_tabs, 1)
        content_layout.addWidget(self.transmit_tabs, 1)
        content_layout.addWidget(self.status_panel)
        
        main_layout.addLayout(content_layout)

        # Подписываемся на обновление статистики
        self.sm.stats.updated.connect(self.update_stats_ui)
        # Первичная отрисовка
        self.update_stats_ui()

    def update_stats_ui(self):
        """Обновление правой панели напрямую из объекта статистики"""
        stats = self.sm.stats
        rx_bytes = stats.format_size(stats.rx_bytes)
        tx_bytes = stats.format_size(stats.tx_bytes)

        self.lbl_rx.setText(f"RX: count: {stats.rx_count} (bytes: {rx_bytes})")
        self.lbl_tx.setText(f"TX: count: {stats.tx_count} (bytes: {tx_bytes})")
        self.lbl_avg_size.setText(f"Avg Data: {stats.avg_tx_size:.1f} b")

    def send_frame_with_stats(self, frame_id, data):
        """Метод отправки с обновлением статистики TX"""
        self.sm.send_frame(frame_id, data)
        self.lbl_tx.setText(f"TX: {self.sm.stats.tx_count}")
        self.lbl_avg_size.setText(f"Avg Data: {self.sm.stats.avg_tx_size:.1f} b")

    def open_settings(self):
        """Открытие диалога настроек из папки core_logic"""
        from core_logic.settings_dialog import SettingsDialog
        SettingsDialog(self).exec()

    def on_exit_clicked(self):
        """Логика выхода"""
        # 1. Отключаем адаптер
        if self.sm.adapter:
            self.sm.adapter.disconnect()
            self.sm.adapter = None
        
        # 2. Сбрасываем статистику для следующего подключения
        self.sm.stats.reset()
        
        # 3. Переключаем сцену в главное меню
        self.exit_requested.emit()