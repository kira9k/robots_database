import math

class LAFC:
    def __init__(self, motor_data, gear_data, source_data, error_data, iven_load_diagram_data, thermal_data):
        self.motor_data = motor_data
        self.gear_data = gear_data
        self.source_data = source_data
        self.error_data = error_data
        self.iven_load_diagram_data = iven_load_diagram_data
        self.thermal_calculator = thermal_data

    @property
    def _Tm(self):
        return (self.motor_data.J + self.source_data.eq_torque_intertia / self.gear_data.i_nom**2) * \
              self.motor_data.R / (self.motor_data.k **2)
    
    @property
    def _Lk(self):
        return 20 * math.log10(self.thermal_calculator.get("A_eqv") / self.error_data.fourth_error)
    
    @property
    def _freq_srez_1(self):
        if self.source_data.reg_angle == 1:
            return math.ceil(self.thermal_calculator.get("omega_eqv") * self.thermal_calculator.get("A_eqv")  / (self.error_data.fourth_error * self.gear_data.i_nom))
        else:
            return math.ceil(math.sqrt(4 * ((self.thermal_calculator.get("omega_eqv")**2) * self.thermal_calculator.get("A_eqv"))  / (self.error_data.fourth_error * self.gear_data.i_nom)))


        
    @property
    def _transition_duration(self):
        return self.source_data.tp / 3

    @property
    def _freq_srez_2(self):
        return math.ceil(2.6 / self._transition_duration)
    
    @property
    def _freq_srez_res(self):
        return max(self._freq_srez_1, self._freq_srez_2)
    
    @property
    def _freq_2(self):
        return 3.2 * self._freq_srez_res
    
    @property
    def _freq_3(self):
        return 16 * self._freq_srez_res
    
class PWM:
    def __init__(self, motor_data, gear_data, source_data, error_data, iven_load_diagram_data, thermal_data):
        self.motor_data = motor_data
        self.freq_3 = LAFC(motor_data, gear_data, source_data, error_data, iven_load_diagram_data, thermal_data)._freq_3

    @property
    def k_pwm(self):
        return self.motor_data.U_nom / 10
    
    @property
    def T_u(self):
        return 1 / (2*self.freq_3)