
from DataBase.connection_db import engine
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import select
from typing import Dict, Any, List
from DataBase.ORMModel import  EngineDC, Encoder, Gear, Result


class DatabaseRepository():
    """ORM-репозиторий для работы с любыми таблицами"""
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

    def add(self, model, data: Dict[str, Any]) -> int:
        """Добавить запись в таблицу"""
        with self.Session() as session:
            obj = model(**data)
            session.add(obj)
            session.flush()  
            obj_id = obj.id
            session.commit()
            return obj_id
            
    def update(self, model, obj_id: int, data: Dict[str, Any]) -> None:
        """Обновить запись по id"""
        with self.Session() as session:
            obj = session.query(model).get(obj_id)
            if obj:
                for key, value in data.items():
                    setattr(obj, key, value)
                session.commit()

    def delete(self, model, obj_id: int) -> None:
        """Удалить запись по id"""
        with self.Session() as session:
            obj = session.query(model).get(obj_id)
            if obj:
                session.delete(obj)
                session.commit()
    
    def get_data_with_relations(self, model) -> List[Dict[str, Any]]:
        """Метод для получения всех данных с связанными данными"""
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
            elif model == Result:
                results = session.query(Result)\
                    .options(
                        joinedload(Result.engine_rel),
                        joinedload(Result.gear_rel),
                        joinedload(Result.encoder_rel),
                        joinedload(Result.source_data_rel),
                        joinedload(Result.coef_regulators_rel),
                        joinedload(Result.utils_rel)
                    ).all()
                result = results
            else:
                result = session.query(model).all()
            
        return result
            
    def get_first_data_by_id_with_relations(self, model, id: int) -> List[Dict[str, Any]]:
        """Метод для получения данных по id с связанными данными"""
        with self.Session() as session:
            if model == Encoder:
                encoders = session.query(Encoder)\
                    .options(
                        joinedload(Encoder.company_rel),
                        joinedload(Encoder.type_rel)
                    ).filter(Encoder.id == id).first()
                result = encoders
            elif model == EngineDC:
                engines = session.query(EngineDC)\
                    .options(
                        joinedload(EngineDC.company_rel),
                        joinedload(EngineDC.engine_type)
                    ).filter(EngineDC.id == id).first()
                result = engines
            elif model == Gear:
                gears = session.query(Gear)\
                    .options(
                        joinedload(Gear.company_rel),
                        joinedload(Gear.type_rel)
                    ).filter(Gear.id == id).first()
                result = gears
            elif model == Result:
                results = session.query(Result)\
                    .options(
                        joinedload(Result.engine_rel),
                        joinedload(Result.gear_rel),
                        joinedload(Result.encoder_rel),
                        joinedload(Result.source_data_rel),
                        joinedload(Result.coef_regulators_rel),
                        joinedload(Result.utils_rel)
                    ).filter(Result.id == id).first()
                result = results

            else:
                id_column = getattr(model, 'id')
                result = session.query(model).filter(id_column == id).first()
            
        return result
    
    def get_company_name(self, model, id):
        with self.Session() as session:
            if model == Encoder:
                encoder = session.query(Encoder).options(joinedload(Encoder.company_rel)).filter(Encoder.id == id).first()
                return encoder.company_rel.company_name if encoder and encoder.company_rel else None
            elif model == EngineDC:
                engine = session.query(EngineDC).options(joinedload(EngineDC.company_rel)).filter(EngineDC.id == id).first()
                return engine.company_rel.name if engine and engine.company_rel else None
            elif model == Gear:
                gear = session.query(Gear).options(joinedload(Gear.company_rel)).filter(Gear.id == id).first()
                return gear.company_rel.name_company if gear and gear.company_rel else None
        return None

    def get_country_name(self, model, id):
        with self.Session() as session:
            if model == Encoder:
                encoder = session.query(Encoder).options(joinedload(Encoder.company_rel)).filter(Encoder.id == id).first()
                return encoder.company_rel.company_country if encoder and encoder.company_rel else None
            elif model == EngineDC:
                engine = session.query(EngineDC).options(joinedload(EngineDC.company_rel)).filter(EngineDC.id == id).first()
                return engine.company_rel.country if engine and engine.company_rel else None
            elif model == Gear:
                gear = session.query(Gear).options(joinedload(Gear.company_rel)).filter(Gear.id == id).first()
                return gear.company_rel.country if gear and gear.company_rel else None
        return None
    
    def get_type_elements(self, model, id):
        with self.Session() as session:
            if model == Encoder:
                encoder = session.query(Encoder).options(joinedload(Encoder.type_rel)).filter(Encoder.id == id).first()
                return encoder.type_rel.encoder_type if encoder and encoder.type_rel else None
            elif model == EngineDC:
                engine = session.query(EngineDC).options(joinedload(EngineDC.engine_type)).filter(EngineDC.id == id).first()
                return engine.engine_type.type_name if engine and engine.engine_type else None
            elif model == Gear:
                gear = session.query(Gear).options(joinedload(Gear.type_rel)).filter(Gear.id == id).first()
                return gear.type_rel.type_gear if gear and gear.type_rel else None
        return None
    
    def find_duplicate(self, model, data: Dict[str, Any]) -> int:
        """Ищет существующую запись с такими же параметрами"""
        def float_equals(a, b, rel_tol=1e-3, abs_tol=1e-3):
            if a == b:
                return True
            if abs(a - b) < abs_tol:
                return True
            if abs(a) > abs_tol or abs(b) > abs_tol:
                return abs(a - b) / max(abs(a), abs(b)) < rel_tol
            return False
        
        with self.Session() as session:
            # Получаем все записи модели
            all_records = session.query(model).all()
                        
            for record in all_records:
                match = True
                
                # Сравниваем каждое поле
                for key, value in data.items():
                    if key == 'id':
                        continue
                    
                    record_value = getattr(record, key, None)
                    
                    # Для float значений - сравниваем с относительной и абсолютной погрешностью
                    if isinstance(value, float) and isinstance(record_value, float):
                        if not float_equals(value, record_value):
                            match = False
                    else:
                        # Для остальных типов - точное сравнение
                        if record_value != value:
                            match = False                
                # Если все поля совпали - найден дубликат
                if match:
                    return record.id
            
            return None