import math

class LAFC:
    """Класс для поиска желаемых частот среза"""
    def __init__(self, motor_data, gear_data, source_data, error_data, iven_load_diagram_data, thermal_data):
        self.motor_data = motor_data
        self.gear_data = gear_data
        self.source_data = source_data
        self.error_data = error_data
        self.iven_load_diagram_data = iven_load_diagram_data
        self.thermal_calculator = thermal_data

    @property
    def _Tm(self):
        """Электромеханическая постоянная времени"""
        return (self.motor_data.J + self.source_data.eq_torque_intertia / self.gear_data.i_nom**2) * \
              self.motor_data.R / (self.motor_data.k **2)
    
    @property
    def _Lk(self):
        """Контрольная точка"""
        return 20 * math.log10(self.thermal_calculator.get("A_eqv") / self.error_data.fourth_error)
    
    @property
    def _freq_srez_1(self):
        """Частота среза разомкнутого привода"""
        return math.ceil(self.thermal_calculator.get("omega_eqv") * self.thermal_calculator.get("A_eqv")  / (self.error_data.fourth_error * self.gear_data.i_nom))

    @property
    def _freq_srez_2(self):
        """Минимальная частота среза разомкнутого привода"""
        return math.ceil(2.5 / self.source_data.transition_time)
    
    @property
    def _freq_srez_res(self):
        """Результирующая частота среза разомкнутого привода"""
        return max(self._freq_srez_1, self._freq_srez_2)
    
    @property
    def _freq_2(self):
        """Желаемая частота среза разомкнутой подсистемы скорости"""
        return 3.2 * self._freq_srez_res
    
    @property
    def _freq_3(self):
        """Желаемая частота среза разомкнутой подсистемы тока"""
        return 16 * self._freq_srez_res
    
class PWM:
    """Класс для расчета параметров СП"""
    def __init__(self, motor_data, gear_data, source_data, error_data, iven_load_diagram_data, thermal_data):
        self.motor_data = motor_data
        self.freq_3 = LAFC(motor_data, gear_data, source_data, error_data, iven_load_diagram_data, thermal_data)._freq_3

    @property
    def k_pwm(self):
        """Коэффициент усиления СП"""
        return self.motor_data.U_nom / 10
    
    @property
    def T_u(self):
        """Некомпенсируемая постоянная времени"""
        return 1 / (2*self.freq_3)