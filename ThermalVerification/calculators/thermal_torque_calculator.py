"""Модуль для расчёта эквивалентного крутящего момента."""

from utils.Interfaces import ISourceData, IGearData
from Graphics.PlotGivenLoadDiagram import DataGivenLoadDiagram


class ThermalEquivalentTorqueCalculator:
    """
    Расчёт эквивалентного крутящего момента.
    """
    
    def __init__(self, source_data: ISourceData, gear_data: IGearData, 
                 given_load_diagram_data: DataGivenLoadDiagram):
        self._source_data = source_data
        self._gear_data = gear_data
        self._given_load_diagram_data = given_load_diagram_data
    
    def calculate_time_cycle(self) -> float:
        """Расчёт длительности цикла tц"""
        return (self._source_data.tp + self._source_data.tp) / self._source_data.tp_rel
    
    def calculate_time_tracking(self, time_cycle: float) -> float:
        """Расчёт времени слежения tс"""
        return time_cycle - 2 * self._source_data.tp
    
    def calculate_equivalent_acceleration(self) -> float:
        """Расчёт амлпитуды изменения объекта управления Аэ"""
        return (self._source_data.max_angle_speed_wm ** 2) / self._source_data.max_angle_acc_wm
    
    def calculate_omega_equivalent(self) -> float:
        """Расчёт угловой частоты изменения объекта управления omega_э"""
        return self._source_data.max_angle_acc_wm / self._source_data.max_angle_speed_wm
    
    def calculate_tracking_torque(self, a_eqv: float, omega_eqv: float) -> float:
        """Расчёт момента слежения Mс"""
        return (self._given_load_diagram_data._torque_stat_gear + 
                (self._given_load_diagram_data._j_sum * a_eqv * omega_eqv ** 2) / 
                self._gear_data.kpd)
    
    def calculate_equivalent_torque_square(self) -> float:
        """Расчет квадрата эквивалетного момента нагрузки двигателя привода"""
        time_cycle = self.calculate_time_cycle()
        time_tracking = self.calculate_time_tracking(time_cycle)
        a_eqv = self.calculate_equivalent_acceleration()
        omega_eqv = self.calculate_omega_equivalent()
        torque_tracking = self.calculate_tracking_torque(a_eqv, omega_eqv)
        
        torque_eqv_square = (1 / time_cycle * (
            (self._given_load_diagram_data.torque_start ** 2) * self._source_data.tp +
            (self._given_load_diagram_data.torque_stop ** 2) * self._source_data.tp +
            (torque_tracking ** 2) * time_tracking
        ))
        
        return torque_eqv_square