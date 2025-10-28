from .EnergyCalulation import DCMotorPowerTorqueCalculator
from utils.SourData import IMotorData, ISourceData, IGearData
from DataBase.repository import DatabaseRepository
from DataBase.FindEngine import FindEngine 


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
        
        Returns:
            dict: Словарь с результатами расчетов
        """
        return {
            'power': self.required_power_torque_calculator.required_power,
            'torque': self.required_power_torque_calculator.max_torque,
        }

    

class DBFacade:
    """
    Фасад для работы с таблицами
    Предоставляет методы для CRUD-операций
    """

    def __init__(self, TABLE_NAME):
        self.repo = DatabaseRepository()
        self.TABLE_NAME = TABLE_NAME

    def get_all(self):
        """Получить все записи из engine_dc"""
        return self.repo.get_all(self.TABLE_NAME)

    def add(self, data):
        """Добавить запись в engine_dc
        data: dict с параметрами двигателя
        """
        self.repo.add_data(self.TABLE_NAME, data)

    def update(self, engine_id, data):
        """Обновить запись по id
        engine_id: int
        data: dict с новыми параметрами
        """
        self.repo.update_data(self.TABLE_NAME, engine_id, data)

    def delete(self, engine_id):
        """Удалить запись по id
        engine_id: int
        """
        self.repo.delete_data(self.TABLE_NAME, engine_id, {})

class FindEngineFacade:
    def __init__(self):
        self.find_engine = FindEngine()

    def find_closest_engine_power(self, orm_model, target_value):
        """Поиск двигателя с мощностью, наиболее близкой к требуемой"""
        return self.find_engine.find_closest_engine_power(orm_model, target_value)
    
    def find_closest_gear_i(self, orm_model, target_value):
        """Поиск редуктора с передаточным отношением, наиболее близким к оптимальному значению"""
        return self.find_engine.find_closest_gear_i(orm_model, target_value)
    