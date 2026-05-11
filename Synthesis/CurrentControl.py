from Synthesis.LAFC import LAFC
from Synthesis.LAFC import PWM

class CurrentControlPI:
    def __init__(self, motor_data, gear_data, source_data, error_data, iven_load_diagram_data, thermal_data):
        self.motor_data = motor_data
        self.gear_data = gear_data
        self.source_data = source_data
        self.error_data = error_data
        self.iven_load_diagram_data = iven_load_diagram_data
        self.thermal_calculator = thermal_data
        self.LAFC = LAFC(motor_data, gear_data, source_data, error_data, iven_load_diagram_data, thermal_data)
        self.PWM = PWM(motor_data, gear_data, source_data, error_data, iven_load_diagram_data, thermal_data)

    @property
    def k_osc(self):
        if self.source_data.reg_current == 2:
            return 0
        return 10 / (self.motor_data.max_current)
    
    @property
    def k_rc(self):
        if self.source_data.reg_current == 2:
            return 1
        return self.LAFC._freq_3 * self.motor_data.T_e * self.motor_data.R / (self.k_osc * self.PWM.k_pwm)
    
    @property
    def k_ric(self):
        if self.source_data.reg_current == 0:
            return 1 / self.motor_data.T_e
        return 0
    
class SpeedControlPI:
    def __init__(self, motor_data, gear_data, source_data, error_data, iven_load_diagram_data, thermal_data):
        self.motor_data = motor_data
        self.gear_data = gear_data
        self.source_data = source_data
        self.error_data = error_data
        self.iven_load_diagram_data = iven_load_diagram_data
        self.thermal_calculator = thermal_data
        self.LAFC = LAFC(motor_data, gear_data, source_data, error_data, iven_load_diagram_data, thermal_data)
        self.PWM = PWM(motor_data, gear_data, source_data, error_data, iven_load_diagram_data, thermal_data)
        self.k_osc = CurrentControlPI(motor_data, gear_data, source_data, error_data, iven_load_diagram_data, thermal_data).k_osc

    @property
    def k_oss(self):
        if self.source_data.reg_speed == 2:
            return 0
        return 10 / self.iven_load_diagram_data.get("idle_speed")

    @property
    def k_rs(self):
        k_osc = self.k_osc

        if self.source_data.reg_speed == 2:
            return 1
        
        if k_osc == 0:
            k_osc = 1
        return (self.LAFC._freq_2 * k_osc * self.iven_load_diagram_data.get("j_sum")) / (self.motor_data.k * self.k_oss)
        
    
    @property
    def k_ris(self):
        if self.source_data.reg_speed == 0:
            return self.LAFC._freq_2 / 4#1 / (1 / (4 * self.LAFC._freq_2))
        return 0 
    
class PositionComtrolP:
    def __init__(self, motor_data, gear_data, source_data, error_data, iven_load_diagram_data, thermal_data, encoder_data):
        self.motor_data = motor_data
        self.gear_data = gear_data
        self.source_data = source_data
        self.error_data = error_data
        self.iven_load_diagram_data = iven_load_diagram_data
        self.thermal_calculator = thermal_data
        self.encoder_data = encoder_data.get('lines_count', 0)
        self.LAFC = LAFC(motor_data, gear_data, source_data, error_data, iven_load_diagram_data, thermal_data)
        self.SpeedControl = SpeedControlPI(motor_data, gear_data, source_data, error_data, iven_load_diagram_data, thermal_data)

    @property
    def k_osa(self):
        return 2 * self.encoder_data / 3.14
    
    @property
    def k_rai(self):
        if self.source_data.reg_angle == 0:
            return 4 / self.LAFC._freq_2
        return 0 
    
    @property
    def k_ra(self):
        k_oss = self.SpeedControl.k_oss
        if k_oss == 0:
            k_oss = 1
        return self.LAFC._freq_2 * k_oss  / self.k_osa