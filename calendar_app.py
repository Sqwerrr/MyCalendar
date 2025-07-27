import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLabel, QPushButton, QGridLayout)
from PySide6.QtCore import QDate, Qt, QPoint
from PySide6.QtGui import (QFont, QLinearGradient, QColor, 
                          QPainter, QBrush, QPainterPath)


class GradientWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Градиент фона (сверху слева светлее, снизу справа темнее)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(30, 50, 100))  # Верхний левый (светлый)
        gradient.setColorAt(1, QColor(10, 20, 50))   # Нижний правый (темный)
        
        # Закругленные углы со всех сторон
        path = QPainterPath()
        rect = self.rect()
        radius = 10
        path.addRoundedRect(rect, radius, radius)
        
        painter.fillPath(path, QBrush(gradient))
        painter.end()


class CalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(380, 400)
        
        # Основной виджет с закруглением
        self.main_widget = QWidget()
        self.main_widget.setObjectName("MainWidget")
        self.setCentralWidget(self.main_widget)
        
        # Градиентный фон
        self.background = GradientWidget()
        
        # Основной layout
        main_layout = QVBoxLayout(self.main_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.background)
        
        # Устанавливаем текущую дату
        self.current_date = QDate.currentDate()
        
        # Layout календаря
        self.calendar_layout = QVBoxLayout(self.background)
        self.calendar_layout.setSpacing(15)
        self.calendar_layout.setContentsMargins(20, 15, 20, 20)
        
        # Верхняя строка (месяц, год и крестик)
        self.setup_header()
        
        # Дни недели
        self.setup_week_days()
        
        # Сетка календаря
        self.calendar_grid = QGridLayout()
        self.calendar_grid.setHorizontalSpacing(10)
        self.calendar_grid.setVerticalSpacing(10)
        
        self.calendar_layout.addLayout(self.calendar_grid)
        self.update_calendar()
        self.apply_styles()
    
    def setup_header(self):
        header_layout = QHBoxLayout()
        
        self.month_label = QLabel()
        self.month_label.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        
        year_nav_layout = QHBoxLayout()
        year_nav_layout.setSpacing(5)
        
        self.prev_button = QPushButton("◀")
        self.prev_button.clicked.connect(self.prev_month)
        self.prev_button.setFixedSize(30, 30)
        self.prev_button.setObjectName("NavButton")
        
        self.year_label = QLabel()
        self.year_label.setFont(QFont('Segoe UI', 14, QFont.Weight.Bold))
        
        self.next_button = QPushButton("▶")
        self.next_button.clicked.connect(self.next_month)
        self.next_button.setFixedSize(30, 30)
        self.next_button.setObjectName("NavButton")
        
        # Крестик закрытия (встроенный в интерфейс)
        self.close_button = QPushButton("✕")
        self.close_button.clicked.connect(self.close)
        self.close_button.setFixedSize(30, 30)
        
        year_nav_layout.addWidget(self.prev_button)
        year_nav_layout.addWidget(self.year_label)
        year_nav_layout.addWidget(self.next_button)
        
        header_layout.addWidget(self.month_label)
        header_layout.addStretch()
        header_layout.addLayout(year_nav_layout)
        header_layout.addWidget(self.close_button)
        
        self.calendar_layout.addLayout(header_layout)
    
    def setup_week_days(self):
        week_days = QHBoxLayout()
        week_days.setSpacing(10)
        
        for day in ["S", "M", "T", "W", "T", "F", "S"]:
            label = QLabel(day)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFont(QFont('Segoe UI', 10))
            label.setFixedWidth(30)
            week_days.addWidget(label)
        
        self.calendar_layout.addLayout(week_days)
    
    def apply_styles(self):
        self.main_widget.setStyleSheet("""
            #MainWidget {
                background-color: transparent;
                border: 1px solid #444466;
                border-radius: 10px;
            }
            QLabel {
                color: #E0E0E0;
            }
            #NavButton {
                color: #A0B0C0;
                background: transparent;
                border: 1px solid transparent;
                border-radius: 15px;
                font-size: 14px;
            }
            #NavButton:hover {
                color: #6D8CB0;
                border: 1px solid #6D8CB0;
                background: rgba(109, 140, 176, 0.1);
            }
            QPushButton {
                color: #A0B0C0;
                background: transparent;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #6D8CB0;
            }
            #CloseButton {
                color: #AAAAAA;
                font-size: 16px;
            }
            #CloseButton:hover {
                color: #FFFFFF;
            }
            .current-day {
                background: qradialgradient(
                    cx:0.5, cy:0.5, radius: 0.5,
                    fx:0.4, fy:0.4,
                    stop:0 #3A5F8A, stop:0.7 #5078AA, stop:1 #6D8CB0
                );
                border-radius: 15px;
                color: white;
                font-weight: bold;
            }
        """)
        self.close_button.setObjectName("CloseButton")
    
    def update_calendar(self):
        for i in reversed(range(self.calendar_grid.count())): 
            self.calendar_grid.itemAt(i).widget().setParent(None)
        
        month_name = self.current_date.toString("MMMM")
        year = self.current_date.toString("yyyy")
        self.month_label.setText(month_name)
        self.year_label.setText(year)
        
        first_day = QDate(self.current_date.year(), self.current_date.month(), 1)
        days_in_month = first_day.daysInMonth()
        week_day = first_day.dayOfWeek() % 7
        
        row, col = 0, week_day
        for day in range(1, days_in_month + 1):
            day_label = QLabel(str(day))
            day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            day_label.setFont(QFont('Segoe UI', 10))
            day_label.setFixedSize(30, 30)
            
            if (day == QDate.currentDate().day() and 
                self.current_date.month() == QDate.currentDate().month() and 
                self.current_date.year() == QDate.currentDate().year()):
                day_label.setProperty("class", "current-day")
            
            self.calendar_grid.addWidget(day_label, row, col)
            col += 1
            if col > 6:
                col = 0
                row += 1
        
        self.style().unpolish(self)
        self.style().polish(self)
    
    def prev_month(self):
        self.current_date = self.current_date.addMonths(-1)
        self.update_calendar()
    
    def next_month(self):
        self.current_date = self.current_date.addMonths(1)
        self.update_calendar()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()
    
    def mouseMoveEvent(self, event):
        if hasattr(self, 'drag_pos'):
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = CalendarApp()
    window.show()
    
    sys.exit(app.exec())