
from utils.Interfaces import IDatabaseEditer
from DataBase.connection_db import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from typing import Dict, Any, List
from DataBase.ORMModel import EngineDC


class DatabaseRepository(IDatabaseEditer):
    """
    Универсальный ORM-репозиторий для работы с любыми таблицами
    """
    def __init__(self):
        self.engine = engine()
        self.Session = sessionmaker(bind=self.engine)

    def get_all(self, model) -> List[Dict[str, Any]]:
        stmt = select(model)
        with self.Session() as session:
            result = session.scalars(stmt)
            data = []
            for item in result.all():
                d = item.__dict__.copy() 
                d.pop('_sa_instance_state', None)  
                data.append(d)
        
            return data

    def add(self, model, data: Dict[str, Any]) -> None:
        """
        Добавить запись в таблицу
        model: класс ORM-модели
        data: dict с параметрами
        """
        with self.Session() as session:
            obj = model(**data)
            session.add(obj)
            session.commit()
            
    def update(self, model, obj_id: int, data: Dict[str, Any]) -> None:
        """
        Обновить запись по id
        model: класс ORM-модели
        obj_id: int
        data: dict с новыми параметрами
        """
        with self.Session() as session:
            obj = session.query(model).get(obj_id)
            if obj:
                for key, value in data.items():
                    setattr(obj, key, value)
                session.commit()

    def delete(self, model, obj_id: int) -> None:
        """
        Удалить запись по id
        model: класс ORM-модели
        obj_id: int
        """
        with self.Session() as session:
            obj = session.query(model).get(obj_id)
            if obj:
                session.delete(obj)
                session.commit()
