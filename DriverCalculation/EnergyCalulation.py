from abc import ABC, abstractmethod
from .SourData import SourceDataDriver, DataDriver
from .Interfaces import IPowerCalculator, ISourceData, IGearRatioCalculator, IMotorData, ITorqueCalculator, IGearData
import math


class DCMotorPowerCalculator(IPowerCalculator):
    """
    Калькулятор мощности для DC двигателя
    Пример использования:
        calc = DCMotorPowerCalculator(source_data, gear_data)
        power = calc.calculate_power()
    """
    POWER_MARGIN = 2.5

    def __init__(self, source_data: ISourceData, gear_data: IGearData) -> None:
        self.source_data = source_data
        self.gear_data = gear_data

    @property
    def max_torque(self) -> float:
        """Максимальный момент"""
        return self.source_data.max_dyn_torque + self.source_data.max_stat_torque

    @property
    def max_torque_with_gear(self) -> float:
        """Максимальный момент с учетом КПД редуктора"""
        if self.gear_data.kpd == 0:
            raise ValueError("КПД редуктора не может быть равен нулю")
        return self.max_torque / self.gear_data.kpd

    @property
    def max_power(self) -> float:
        """Максимальная мощность"""
        return self.max_torque * self.source_data.max_angl_speed

    def calculate_power(self) -> float:
        """Расчет требуемой мощности с привода"""
        return self.max_power * self.POWER_MARGIN



class DCMotorGearRatioCalculator(IGearRatioCalculator):
    """
    Калькулятор передаточного отношения для DC двигателя
    Пример использования:
        calc = DCMotorGearRatioCalculator(source_data, motor_data, gear_data)
        ratio = calc.calculate_gear_ratio()
    """

    def __init__(self, source_data: ISourceData, motor_data: IMotorData, gear_data: IGearData) -> None:
        self.source_data = source_data
        self.motor_data = motor_data
        self.gear_data = gear_data

    def calculate_gear_ratio(self) -> float:
        """Расчет оптимального передаточного отношения"""
        power_calculator = DCMotorPowerCalculator(self.source_data, self.gear_data)
        max_power = power_calculator.max_power

        denominator = (
            self.motor_data.J *
            self.source_data.max_angl_speed *
            self.source_data.max_angl_acc
        )
        if denominator == 0:
            raise ValueError("Знаменатель не может быть равен нулю")
        return math.sqrt(max_power / denominator)


class DCMotorTorqueCalculator(ITorqueCalculator):
    """
    Калькулятор момента для DC двигателя
    Пример использования:
        calc = DCMotorTorqueCalculator(source_data, motor_data, gear_data)
        torque = calc.calculate_torque()
    """

    def __init__(self, source_data: ISourceData, motor_data: IMotorData, gear_data: IGearData) -> None:
        self.source_data = source_data
        self.motor_data = motor_data
        self.gear_data = gear_data

    def calculate_torque(self) -> float:
        """Расчет момента для DC двигателя"""
        power_calculator = DCMotorPowerCalculator(self.source_data, self.gear_data)
        if self.gear_data.i_nom == 0:
            raise ValueError("Передаточное число редуктора не может быть равно нулю")
        max_torque = power_calculator.max_torque_with_gear
        torque_calculate = (
            self.motor_data.J * self.gear_data.i_nom * self.source_data.max_angl_acc
            + max_torque / self.gear_data.i_nom
        )
        return torque_calculate

    