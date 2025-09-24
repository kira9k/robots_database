from .EnergyCalulation import DCMotorGearRatioCalculator, DCMotorTorqueCalculator, DCMotorPowerCalculator
from .SourData import IMotorData, ISourceData, IGearData
from DataBase.repository import DatabaseRepository


class DCMotorEnergyFacade:
    """
    Фасад для упрощенного доступа ко всем расчетам DC двигателя
    Реализует принцип единой точки входа
    """
    
    def __init__(self, source_data: ISourceData, motor_data: IMotorData, gear_data: IGearData):
        self.source_data = source_data
        self.motor_data = motor_data
        self.gear_data = gear_data
        
        # Инициализация калькуляторов
        self.power_calculator = DCMotorPowerCalculator(source_data, gear_data)
        self.torque_calculator = DCMotorTorqueCalculator(source_data, motor_data, gear_data)
        self.gear_ratio_calculator = DCMotorGearRatioCalculator(source_data, motor_data, gear_data)
        
    
    def get_all_calculations(self) -> dict:
        """
        Возвращает все расчеты в виде словаря
        
        Returns:
            dict: Словарь с результатами расчетов
        """
        return {
            'power': self.power_calculator.calculate_power(),
            'torque': self.torque_calculator.calculate_torque(),
            'gear_ratio': self.gear_ratio_calculator.calculate_gear_ratio(),
            'max torque_with kpd': self.get_torque_with_gear()
        }
    
    def get_power(self) -> float:
        """Возвращает расчетную мощность"""
        return self.power_calculator.calculate_power()
    
    def get_torque(self) -> float:
        """Возвращает расчетный момент"""
        return self.torque_calculator.calculate_torque()
    
    def get_torque_with_gear(self) -> float:
        """Возвращает расчетный момент с учетом КПД редуктора"""
        return self.power_calculator.max_torque_with_gear
    
    def get_gear_ratio(self) -> float:
        """Возвращает расчетное передаточное отношение"""
        return self.gear_ratio_calculator.calculate_gear_ratio()
    

class EngineDCFacade:
    """
    Фасад для работы с таблицей engine_dc
    Предоставляет методы для CRUD-операций
    """
    TABLE_NAME = "engine_dc"

    def __init__(self):
        self.repo = DatabaseRepository()

    def get_all_engines(self):
        """Получить все записи из engine_dc"""
        return self.repo.get_all_data_from_table(self.TABLE_NAME)

    def add_engine(self, data):
        """Добавить запись в engine_dc
        data: dict с параметрами двигателя
        """
        self.repo.add_data(self.TABLE_NAME, data)

    def update_engine(self, engine_id, data):
        """Обновить запись по id
        engine_id: int
        data: dict с новыми параметрами
        """
        self.repo.update_data(self.TABLE_NAME, engine_id, data)

    def delete_engine(self, engine_id):
        """Удалить запись по id
        engine_id: int
        """
        self.repo.delete_data(self.TABLE_NAME, engine_id, {})
    