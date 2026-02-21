from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
)
from sqlalchemy import select
from .DesignWindow import DesignWindow
from .TableWindow import TableWindow
from DataBase.connection_db import engine as db_engine
from sqlalchemy.orm import sessionmaker
import sys
from DataBase.ORMModel import EngineDC, Gear, Encoder



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("База данных PostgreSQL")
        self.setGeometry(100, 100, 800, 600)
        
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        self.TableWindow = TableWindow
        
        self.btn_open_table = QPushButton("Открыть таблицу двигателей")
        self.btn_open_table.clicked.connect(lambda: self.create_table_window(EngineDC))
        layout.addWidget(self.btn_open_table)
        
        self.btn_open_table = QPushButton("Открыть таблицу редукторов")
        self.btn_open_table.clicked.connect(lambda: self.create_table_window(Gear))
        layout.addWidget(self.btn_open_table)

        self.btn_open_table = QPushButton("Открыть таблицу энкодеров")
        self.btn_open_table.clicked.connect(lambda: self.create_table_window(Encoder))
        layout.addWidget(self.btn_open_table)

        self.btn_design = QPushButton("Спроектировать электропривод")
        self.btn_design.clicked.connect(lambda: self.create_design_window())
        layout.addWidget(self.btn_design)

    def create_table_window(self, orm_model):
        self.table_window = self.TableWindow(orm_model)
        self.table_window.show()

    def create_design_window(self):
        self.design_window = DesignWindow()
        self.design_window.show()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())