from abc import ABC, abstractmethod
from utils.Interfaces import IGearData, ISourceData, IMotorData
from .VerificationCalculation import VerificationCalculation 
from Graphics.PlotGivenLoadDiagram import DataGivenLoadDiagram
import numpy as np

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


class MotorTorqueVerificationStrategy:
    """
    Сравнивает квадрат эквивалентного момента с квадратом номинального момента двигателя
    """
    
    def __init__(self, motor_data: IMotorData):
        self._motor_data = motor_data
    
    def verify(self, torque_eqv_square: float) -> bool:
        """
        Проверка: квадрат номинального момента должен быть больше квадрата эквивалентного момента
        """
        return self._motor_data.torque_nom ** 2 > torque_eqv_square

class ThermalVerificationResult:
    """
    Класс для хранения результатов проверки.
    """
    
    def __init__(self, is_valid: bool, torque_eqv_square: float, 
                 motor_torque_square: float = None):
        self.is_valid = is_valid
        self.torque_eqv_square = torque_eqv_square
        self.motor_torque_square = motor_torque_square
    
    def __str__(self) -> str:
        """Форматированный вывод результата."""
        status = "УСПЕШНО" if self.is_valid else "НЕ ПРОЙДЕНО"
        return (f"Тепловая проверка: {status}\n"
                f"Квадрат эквивалентного момента: {self.torque_eqv_square:.4f}\n"
                f"Квадрат момента двигателя: {self.motor_torque_square:.4f}")

class ThermalCalculator:
    """Координирует процесс тепловой проверки"""

    
    def __init__(self, 
                 source_data: ISourceData, 
                 motor_data: IMotorData, 
                 gear_data: IGearData,
                 verification_strategy: IThermalVerificationStrategy = None,
                 result_handler: IVerificationResultHandler = None):
        """        
        Args:
            source_data: ихсодные данные
            motor_data: данные двигателя
            gear_data: данные редуктора
            verification_strategy: стратегия проверки (по умолчанию - проверка по номинальному моменту)
            result_handler: обработчик результатов (по умолчанию - вывод в консоль)
        """
        self._source_data = source_data
        self._motor_data = motor_data
        self._gear_data = gear_data
        
        # Инициализация существующих зависимостей
        self._verification_calc = VerificationCalculation(
            source_data, motor_data, gear_data
        )
        self._given_load_diagram_data = DataGivenLoadDiagram(
            source_data, motor_data, gear_data
        )
        
        # Инъекция зависимостей с дефолтными значениями
        self._torque_calculator = ThermalEquivalentTorqueCalculator(
            source_data, gear_data, self._given_load_diagram_data
        )
        self._verification_strategy = verification_strategy or MotorTorqueVerificationStrategy(motor_data)
        self._result_handler = result_handler or ConsoleResultHandler()
    
    def execute_verification(self) -> ThermalVerificationResult:
        """
        Выполняет процесс тепловой проверки.
        
        Returns:
            ThermalVerificationResult: объект с результатами проверки
        """
        # Шаг 1: Вычисляем эквивалентный момент
        torque_eqv_square = self._torque_calculator.calculate_equivalent_torque_square()
        
        # Шаг 2: Проверяем с помощью стратегии
        is_valid = self._verification_strategy.verify(torque_eqv_square)
        
        # Шаг 3: Формируем результат
        result = ThermalVerificationResult(
            is_valid=is_valid,
            torque_eqv_square=torque_eqv_square,
            motor_torque_square=self._motor_data.torque_nom ** 2
        )
        
        return result
    
    def run(self) -> None:
        """
        Запускает тепловую проверку и обрабатывает результат.
        Выполняется только если базовая проверка момента не пройдена.
        """
        if not self._verification_calc.verify_torque():
            result = self.execute_verification()
            self._result_handler.handle(result)

# class ThermalCalculator:
#     def __init__(self, source_data: ISourceData, motor_data: IMotorData, gear_data: IGearData):
#         self.source_data = source_data
#         self.motor_data = motor_data
#         self.gear_data = gear_data
#         self.verification_calc = VerificationCalculation(self.source_data, self.motor_data, self.gear_data)
#         self.given_load_diagram_data = DataGivenLoadDiagram(source_data, motor_data, gear_data)
#         if not self.verification_calc.verify_torque():
#             print(self.verify_thermal_eqv_torque())
    
#     def verify_thermal_eqv_torque(self):
#         time_cycle = (self.source_data.tp + self.source_data.tp) / self.source_data.tp_rel
#         time_tracking = time_cycle - 2 * self.source_data.tp
#         a_eqv = (self.source_data.max_angle_speed_wm ** 2) / self.source_data.max_angle_acc_wm
#         omega_egv = self.source_data.max_angle_acc_wm/self.source_data.max_angle_speed_wm

#         torque_tracking = self.given_load_diagram_data._torque_stat_gear + (self.given_load_diagram_data._j_sum * a_eqv * omega_egv ** 2) / self.gear_data.kpd
#         torque_eqv_square = 1 / time_cycle * ((self.given_load_diagram_data.torque_start**2) * self.source_data.tp 
#                                                      + (self.given_load_diagram_data.torque_stop**2) * self.source_data.tp
#                                                      + (torque_tracking **2) * time_tracking)
#         print(torque_eqv_square)
#         return self.motor_data.torque_nom ** 2 >  torque_eqv_square