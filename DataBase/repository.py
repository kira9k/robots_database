
from utils.Interfaces import IDatabaseEditer
from DataBase.connection_db import engine
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import select
from typing import Dict, Any, List
from DataBase.ORMModel import EngineDC, Encoder, Gear


class DatabaseRepository(IDatabaseEditer):
    """
    ORM-репозиторий для работы с любыми таблицами.
    """
    def __init__(self, session_factory=None):
        if session_factory is None:
            self.engine = engine()
            self.Session = sessionmaker(bind=self.engine)
        else:
            self.Session = session_factory

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
    
    def get_data_with_relations(self, model) -> List[Dict[str, Any]]:
        """
        Метод для получения всех данных с связанными данными
        """
        
        with self.Session() as session:
            if model == Encoder:
                encoders = session.query(Encoder)\
                    .options(
                        joinedload(Encoder.company_rel),
                        joinedload(Encoder.type_rel)
                    ).all()
                result = encoders
            elif model == EngineDC:
                engines = session.query(EngineDC)\
                    .options(
                        joinedload(EngineDC.company_rel),
                        joinedload(EngineDC.engine_type)
                    ).all()
                result = engines
            elif model == Gear:
                gears = session.query(Gear)\
                    .options(
                        joinedload(Gear.company_rel),
                        joinedload(Gear.type_rel)
                    ).all()
                result = gears
            
        return result
            
