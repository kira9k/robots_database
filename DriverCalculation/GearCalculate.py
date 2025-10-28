import math
from utils.Interfaces import ISourceData, IMotorData
from DriverCalculation.EnergyCalulation import DCMotorPowerTorqueCalculator
from utils.Interfaces import IGearRatioCalculator


class GearCalulator(IGearRatioCalculator):
    def __init__(self, source_data: ISourceData, motor_data: IMotorData):
        self.source_data = source_data
        self.motor_data = motor_data

    @property
    def gear_ratio_optimal(self) -> float:
        """Расчет оптимального передаточного отношения"""
        power_calculator = DCMotorPowerTorqueCalculator(self.source_data)
        max_power = power_calculator.max_power

        denominator = (
            self.motor_data.J *
            self.source_data.max_angl_speed *
            self.source_data.max_angl_acc
        )
        if denominator == 0:
            raise ValueError("Знаменатель не может быть равен нулю")
        return math.sqrt(max_power / denominator)