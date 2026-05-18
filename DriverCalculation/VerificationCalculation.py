from DriverCalculation.EnergyCalulation import DCMotorPowerTorqueReCalculator
import math

class VerificationCalculation:
    """Класс для верификации расчетов скорости и момента с учетом редуктора"""
    def __init__(self, source_data, motor_data, gear_data) -> None:
        self.source_data = source_data
        self.motor_data = motor_data
        self.gear_data = gear_data
        self.max_torque_with_gear = DCMotorPowerTorqueReCalculator(self.source_data, self.gear_data, self.motor_data).required_torque_with_gear

    @property
    def max_speed_with_gear(self) -> float:
        """Максимальная скорость двигателя с учетом редуктора"""
        return self.source_data.max_angl_speed * self.gear_data.i_nom
    
    def verify_torque(self) -> bool:
        """Проверка, что рассчитанный момент не превышает максимальный момент двигателя с учетом редуктора"""
        return self.max_torque_with_gear <= self.motor_data.torque_nom
    
    def verify_speed(self) -> bool:
        """Проверка, что расчетная скорость не превышает максимальную скорость двигателя с учетом редуктора"""
        print(self.max_speed_with_gear* 30 /math.pi)
        return self.max_speed_with_gear * 30 /math.pi <= self.motor_data.n_nom