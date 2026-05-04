from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit
from PySide6.QtCore import Qt


class RecordDetailWindow(QWidget):
    """Окно для отображения деталей записи"""
    
    def __init__(self, title, html_content, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle(title)
        self.resize(800, 600)
        self.setWindowFlag(Qt.Window, True)
        
        # Создаем главный layout
        layout = QVBoxLayout(self)
        
        # Создаем текстовое поле для отображения HTML
        self.text = QTextEdit(self)
        self.text.setReadOnly(True)
        self.text.setStyleSheet("""
            QTextEdit {
                font-size: 10pt;
                font-family: Arial;
            }
        """)
        
        # Отображаем HTML
        self.text.setHtml(html_content)
        layout.addWidget(self.text)
        
        # Кнопка закрытия
        btn_close = QPushButton("Закрыть")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)
        
        self.setLayout(layout)
