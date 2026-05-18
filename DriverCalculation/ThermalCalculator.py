from Graphics.PlotGivenLoadDiagram import DataGivenLoadDiagram

class ThermalCalculator:
    """Тепловой расчёт"""
    def __init__(self, source_data, motor_data, gear_data):
        self._source_data = source_data
        self._motor_data = motor_data
        self._gear_data = gear_data
        self._given_load_diagram_data = DataGivenLoadDiagram(source_data, motor_data, gear_data)
    
    @property
    def calculate_time_cycle(self) -> float:
        """Расчёт длительности цикла tц"""
        return (self._source_data.tp + self._source_data.tp) / self._source_data.tp_rel
    
    @property
    def calculate_time_tracking(self) -> float:
        """Расчёт времени слежения tс"""
        return self.calculate_time_cycle * (1 - self._source_data.tp_rel)
    
    @property
    def calculate_equivalent_amplitude(self) -> float:
        """Расчёт амлпитуды изменения объекта управления Аэ"""
        return (self._gear_data.i_nom * self._source_data.max_angle_speed_wm ** 2) / self._source_data.max_angle_acc_wm
    
    @property
    def calculate_omega_equivalent(self) -> float:
        """Расчёт угловой частоты изменения объекта управления omega_э"""
        return self._source_data.max_angle_acc_wm / self._source_data.max_angle_speed_wm
    
    @property
    def calculate_tracking_torque(self) -> float:
        """Расчёт момента слежения Mс"""
        return (self._given_load_diagram_data._torque_stat_gear + 
                (self._given_load_diagram_data._j_sum * self.calculate_equivalent_amplitude * self.calculate_omega_equivalent ** 2))
    
    @property
    def calculate_equivalent_torque_square(self) -> float:
        """Расчет квадрата эквивалетного момента нагрузки двигателя привода"""
        
        torque_eqv_square = (1 / self.calculate_time_cycle * (
            (self._given_load_diagram_data.torque_start ** 2) * self._source_data.tp +
            (self._given_load_diagram_data.torque_stop ** 2) * self._source_data.tp +
            (self.calculate_tracking_torque ** 2) * self.calculate_time_tracking
        ))

        return torque_eqv_square
    
    def verify(self) -> bool:
        """Проверка: квадрат номинального момента должен быть больше эквивалентного."""
        return self._motor_data.torque_nom ** 2 > self.calculate_equivalent_torque_square

    def get_data(self):
        """Возвращает данные для отображения в результатах."""
        return {"t_cycle": self.calculate_time_cycle,
                "t_s": self.calculate_time_tracking,
                "A_eqv": self.calculate_equivalent_amplitude,
                "omega_eqv": self.calculate_omega_equivalent,
                "M_c": self.calculate_tracking_torque,
                "M_eqv_square": self.calculate_equivalent_torque_square,
            
        }
