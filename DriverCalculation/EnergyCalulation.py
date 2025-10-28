from abc import ABC, abstractmethod
from utils.SourData import SourceDataDriver, DataDriver
from utils.Interfaces import IPowerCalculator, ISourceData, IGearRatioCalculator, IMotorData, ITorqueCalculator, IGearData
import math


class DCMotorPowerTorqueCalculator(IPowerCalculator):
    """
    Калькулятор мощности и момента для DC двигателя
    Пример использования:
        calc = DCMotorPowerCalculator(source_data)
        power = calc.required_power
    """
    POWER_MARGIN = 2.5

    def __init__(self, source_data: ISourceData) -> None:
        self.source_data = source_data

    @property
    def max_torque(self) -> float:
        """Максимальный момент"""
        return self.source_data.max_dyn_torque + self.source_data.max_stat_torque

    @property
    def max_power(self) -> float:
        """Максимальная мощность"""
        return self.max_torque * self.source_data.max_angl_speed
    
    @property
    def required_power(self) -> float:
        """Расчет требуемой мощности привода"""
        return self.max_power * self.POWER_MARGIN


class DCMotorPowerTorqueReCalculator(DCMotorPowerTorqueCalculator):
    """
    Калькулятор мощности и момента для DC двигателя с учетом редуктора
    """

    def __init__(self, source_data: ISourceData, gear_data: IGearData) -> None:
        super().__init__(source_data)
        self.gear_data = gear_data

    @property
    def required_torque_with_gear(self) -> float:
        """Максимальный момент с учетом редуктора"""
        if self.gear_data.i_nom == 0:
            raise ValueError("Передаточное число редуктора не может быть равно нулю")
        return super().max_torque / self.gear_data.kpd
    
    @property
    def required_power_with_gear(self) -> float:
        """Расчет требуемой мощности привода с учетом редуктора"""
        return super().required_power / self.gear_data.kpd
    
    


    