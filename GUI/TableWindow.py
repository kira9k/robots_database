from PySide6.QtWidgets import QTableView, QVBoxLayout, QWidget
from .DBModelGUI import SQLAlchemyTableModel
from DataBase.connection_db import engine as db_engine
from DataBase.ORMModel import EngineDC, Encoder, Gear
from sqlalchemy.orm import sessionmaker
from DataBase.repository import DatabaseRepository
from typing import Type
from sqlalchemy.orm import DeclarativeBase

class TableWindow(QWidget):
    def __init__(self, ORMModel: Type[DeclarativeBase]):
        super().__init__()
        self.setWindowTitle("База данных PostgreSQL")
        self.setGeometry(100, 100, 1000, 600)
        
        # Создаем репозиторий
        self.repository = DatabaseRepository(session_factory=sessionmaker(bind=db_engine()))
        
        self.table = QTableView()
        self.ORM_Model = ORMModel
        
        # Центральный виджет с layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
        
        # Загружаем данные
        self.load_data()
    
    def load_data(self):
        """Загружает данные из БД через репозиторий"""
        if self.ORM_Model == Encoder:
            orm_model = Encoder
        elif self.ORM_Model == EngineDC:
            orm_model = EngineDC
        elif self.ORM_Model == Gear:
            orm_model = Gear
        else:
            orm_model = self.ORM_Model
        
        data = self.repository.get_data_with_relations(orm_model)
        columns = [col.name for col in self.ORM_Model.__table__.columns]
        
        model = SQLAlchemyTableModel(data, columns)
        self.table.setModel(model)