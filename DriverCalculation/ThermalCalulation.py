from utils.Interfaces import IGearData, ISourceData, IMotorData
from .VerificationCalculation import VerificationCalculation 

class ThermalCalculation:
    def __init__(self, source_data: ISourceData, motor_data: IMotorData, gear_data: IGearData):
        self.source_data = source_data
        self.motor_data = motor_data
        self.gear_data = gear_data
        self.verification_calc = VerificationCalculation(self.source_data, self.motor_data, self.gear_data)
        if not self.verification_calc.verify_torque():
            self.verify_thermal_eqv_torque()
    
    def verify_thermal_eqv_torque(self):
        time_cycle = (self.source_data.tp + self.source_data.tp) / self.source_data.tp_rel
        time_tracking = time_cycle - 2 * self.source_data.tp
        #torque_tracking
        #TODO доделать тепловой расчет
