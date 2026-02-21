from .EnergyCalulation import DCMotorPowerTorqueCalculator
from utils.SourData import IMotorData, ISourceData, IGearData
from DataBase.repository import DatabaseRepository
from DataBase.FindEngine import FindEngine 
from DataBase.connection_db import engine as db_engine
from sqlalchemy.orm import sessionmaker
from SearchAlgorithm import FindEncoder
from Encoders import EncoderCalculator

class DCMotorEnergyFacade:
    """
    Фасад для упрощенного доступа ко всем расчетам DC двигателя
    Реализует принцип единой точки входа
    """
    
    def __init__(self, source_data: ISourceData):
        self.source_data = source_data
        self.required_power_torque_calculator = DCMotorPowerTorqueCalculator(source_data) 
    
    def get_all_calculations(self) -> dict:
        """
        Возвращает все расчеты в виде словаря
        """
        return {
            'power': self.required_power_torque_calculator.required_power,
            'torque': self.required_power_torque_calculator.max_torque,
        }
    
class EncoderFacade:
    def __init__(self, error, gear_data: IGearData):
        self.minimal_lines_count = EncoderCalculator(error, gear_data)

    @property
    def get_minimal_lines_count(self) -> int:
        """Получить минимальную разрешающую способность энкодера"""
        return self.minimal_lines_count.dicrete_number

class DBFacade:
    """
    Фасад для работы с таблицами
    Предоставляет методы для CRUD-операций
    """
    def __init__(self, TABLE_NAME):
        SessionFactory = sessionmaker(bind=db_engine())
        self.repo = DatabaseRepository(session_factory=SessionFactory)
        self.TABLE_NAME = TABLE_NAME

    def get_all(self):
        """Получить все записи из engine_dc"""
        return self.repo.get_all(self.TABLE_NAME)

    def add(self, data):
        """Добавить запись в engine_dc
        data: dict с параметрами двигателя
        """
        self.repo.add(self.TABLE_NAME, data)

    def update(self, engine_id, data):
        """Обновить запись по id
        engine_id: int
        data: dict с новыми параметрами
        """
        self.repo.update(self.TABLE_NAME, engine_id, data)

    def delete(self, engine_id):
        """Удалить запись по id
        engine_id: int
        """
        self.repo.delete(self.TABLE_NAME, engine_id)


class FindEngineFacade:
    def __init__(self):
        SessionFactory = sessionmaker(bind=db_engine())
        self.find_engine = FindEngine(session_factory=SessionFactory)

    def find_closest_engine_power(self, orm_model, target_value):
        """Поиск двигателя с мощностью, наиболее близкой к требуемой"""
        return self.find_engine.find_closest_engine_power(orm_model, target_value)
    
    def find_closest_gear_i(self, orm_model, target_value, source_data, results_moment):
        """Поиск редуктора с передаточным отношением, наиболее близким к оптимальному значению"""
        return self.find_engine.find_closest_gear_i(orm_model, target_value,source_data, results_moment)
    
class FindEncoderFacade:
    def __init__(self):
        SessionFactory = sessionmaker(bind=db_engine())
        self.find_encoder = FindEncoder(session_factory=SessionFactory)

    def find_closest_encoder_lines(self, orm_model, target_value, source_data, gear_data):
        """Поиск энкодера с разрешающей способностью, наиболее близкой к требуемой"""
        return self.find_encoder.find_closest_encoder_lines_count_ceil(orm_model, target_value, source_data, gear_data)