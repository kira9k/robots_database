from utils.Interfaces import ISourceData, IMotorData, IGearData
from DriverCalculation.EnergyCalulation import DCMotorPowerTorqueReCalculator
import math

class VerificationCalculation:
    def __init__(self, source_data: ISourceData, motor_data: IMotorData, gear_data: IGearData):
        self.source_data = source_data
        self.motor_data = motor_data
        self.gear_data = gear_data
        self.required_torque = DCMotorPowerTorqueReCalculator(self.source_data, self.gear_data).required_torque_with_gear

    @property
    def max_torque_with_gear(self) -> float:
        """Максимальный момент двигателя с учетом редуктора"""
        return self.motor_data.J * self.source_data.max_angl_acc * self.gear_data.i_nom + self.required_torque / self.gear_data.i_nom

    @property
    def max_speed_with_gear(self) -> float:
        """Максимальная скорость двигателя с учетом редуктора"""
        return self.source_data.max_angl_speed * self.gear_data.i_nom
    def verify_torque(self) -> bool:
        
        """Проверка, что рассчитанный момент не превышает максимальный момент двигателя с учетом редуктора"""
        return self.max_torque_with_gear <= self.motor_data.torque_nom
    
    def verify_speed(self) -> bool:
        """Проверка, что расчетная скорость не превышает максимальную скорость двигателя с учетом редуктора"""
        #print(speed_with_gear * 30/math.pi, self.motor_data.n_nom)
        return self.max_speed_with_gear * math.pi /30 <= self.motor_data.n_nom