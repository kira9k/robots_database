from Synthesis.LAFC import LAFC
from Synthesis.LAFC import PWM

class CurrentControlPI:
    """Класс для расчета параметров регулятора тока"""
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
        """Коэффициент обратной связи по скорости"""
        return 10 / (self.motor_data.max_current)
    
    @property
    def k_rc(self):
        """Коэффициент пропорциональной составляющей РТ"""
        return self.LAFC._freq_3 * self.motor_data.T_e * self.motor_data.R / (self.k_osc * self.PWM.k_pwm)
    
    @property
    def k_ric(self):
        """Коэффициент интегральной составляющей РТ"""
        return 1 / self.motor_data.T_e

    
class SpeedControlPI:
    """Класс для расчета параметров регулятора скорости"""
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
        """Коэффициент обратной связи по скорости"""
        return 10 / self.iven_load_diagram_data.get("idle_speed")

    @property
    def k_rs(self):
        """Коэффициент пропорциональной составляющей регулятора скорости"""
        return (self.LAFC._freq_2 * self.k_osc * self.iven_load_diagram_data.get("j_sum")) / (self.motor_data.k * self.k_oss)
        
    
    @property
    def k_ris(self):
        """Коэффициент интегральной составляющей регулятора скорости"""
        return self.LAFC._freq_2 / 4 
    
class PositionComtrolP:
    """Класс для расчета параметров регулятора положения"""
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
        """Коэффициент обратной связи по положению"""
        return 2 * self.encoder_data / 3.14
    
    @property
    def k_rai(self):
        """Коэффициент интегральной составляющей регулятора положения"""
        return 0 
    
    @property
    def k_ra(self):
        """Коэффициент пропорциональной составляющей регулятора положения"""
        return self.LAFC._freq_2 * self.SpeedControl.k_oss  / self.k_osa