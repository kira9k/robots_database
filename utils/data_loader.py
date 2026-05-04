from sqlalchemy.orm import sessionmaker
from DataBase.connection_db import engine
from DataBase.ORMModel import (
    EngineCompany, EngineType, 
    GearCompany, GearType,
    EncoderCompany, EncoderType
)

class DataLoader:
    """Загрузчик данных для выпадающих списков"""
    
    def __init__(self):
        self.Session = sessionmaker(bind=engine())
    
    # ============ GET методы (существующие) ============
    
    def get_engine_companies(self):
        """Получить список компаний для двигателей"""
        with self.Session() as session:
            companies = session.query(EngineCompany).all()
            return [(c.id_company, c.name) for c in companies]
    
    def get_engine_types(self):
        """Получить список типов для двигателей"""
        with self.Session() as session:
            types = session.query(EngineType).all()
            return [(t.id_engine, t.type_name) for t in types]
    
    def get_gear_companies(self):
        """Получить список компаний для редукторов"""
        with self.Session() as session:
            companies = session.query(GearCompany).all()
            return [(c.company_id, c.name_company) for c in companies]
    
    def get_gear_types(self):
        """Получить список типов для редукторов"""
        with self.Session() as session:
            types = session.query(GearType).all()
            return [(t.type_gear_id, t.type_gear) for t in types]
    
    def get_encoder_companies(self):
        """Получить список компаний для энкодеров"""
        with self.Session() as session:
            companies = session.query(EncoderCompany).all()
            return [(c.id_company_encoder, c.company_name) for c in companies]
    
    def get_encoder_types(self):
        """Получить список типов для энкодеров"""
        with self.Session() as session:
            types = session.query(EncoderType).all()
            return [(t.id_type, t.encoder_type) for t in types]
    
    # ============ ADD методы для добавления ============
    
    def add_engine_company(self, name, country=None):
        """Добавить новую компанию для двигателей"""
        with self.Session() as session:
            try:
                new_company = EngineCompany(name=name, country=country)
                session.add(new_company)
                session.commit()
                session.refresh(new_company)
                return new_company.id_company, new_company.name
            except Exception as e:
                session.rollback()
                raise Exception(f"Ошибка при добавлении компании: {e}")
    
    def add_engine_type(self, type_name):
        """Добавить новый тип для двигателей"""
        with self.Session() as session:
            try:
                new_type = EngineType(type_name=type_name)
                session.add(new_type)
                session.commit()
                session.refresh(new_type)
                return new_type.id_engine, new_type.type_name
            except Exception as e:
                session.rollback()
                raise Exception(f"Ошибка при добавлении типа: {e}")
    
    def add_gear_company(self, name, country=None):
        """Добавить новую компанию для редукторов"""
        with self.Session() as session:
            try:
                new_company = GearCompany(name_company=name, country=country)
                session.add(new_company)
                session.commit()
                session.refresh(new_company)
                return new_company.company_id, new_company.name_company
            except Exception as e:
                session.rollback()
                raise Exception(f"Ошибка при добавлении компании: {e}")
    
    def add_gear_type(self, type_name):
        """Добавить новый тип для редукторов"""
        with self.Session() as session:
            try:
                new_type = GearType(type_gear=type_name)
                session.add(new_type)
                session.commit()
                session.refresh(new_type)
                return new_type.type_gear_id, new_type.type_gear
            except Exception as e:
                session.rollback()
                raise Exception(f"Ошибка при добавлении типа: {e}")
    
    def add_encoder_company(self, name, country=None):
        """Добавить новую компанию для энкодеров"""
        with self.Session() as session:
            try:
                new_company = EncoderCompany(company_name=name, company_country=country)
                session.add(new_company)
                session.commit()
                session.refresh(new_company)
                return new_company.id_company_encoder, new_company.company_name
            except Exception as e:
                session.rollback()
                raise Exception(f"Ошибка при добавлении компании: {e}")
    
    def add_encoder_type(self, type_name):
        """Добавить новый тип для энкодеров"""
        with self.Session() as session:
            try:
                new_type = EncoderType(encoder_type=type_name)
                session.add(new_type)
                session.commit()
                session.refresh(new_type)
                return new_type.id_type, new_type.encoder_type
            except Exception as e:
                session.rollback()
                raise Exception(f"Ошибка при добавлении типа: {e}")