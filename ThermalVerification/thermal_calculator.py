"""Главный модуль координации тепловой проверки."""

from utils.Interfaces import IGearData, ISourceData, IMotorData
from DriverCalculation.VerificationCalculation import VerificationCalculation 
from Graphics.PlotGivenLoadDiagram import DataGivenLoadDiagram

from .calculators.thermal_torque_calculator import ThermalEquivalentTorqueCalculator
from .strategies.motor_torque_strategy import MotorTorqueVerificationStrategy
from .strategies.base import IThermalVerificationStrategy
from .handlers.base import IVerificationResultHandler
from .handlers.console_handler import ConsoleResultHandler
from .models.verification_result import ThermalVerificationResult


class ThermalCalculator:
    """
    Координирует процесс тепловой проверки
    """
    
    def __init__(self, 
                 source_data: ISourceData, 
                 motor_data: IMotorData, 
                 gear_data: IGearData,
                 verification_strategy: IThermalVerificationStrategy = None,
                 result_handler: IVerificationResultHandler = None):
        """        
        Args:
            source_data: исходные данные
            motor_data: данные двигателя
            gear_data: данные редуктора
            verification_strategy: стратегия проверки (опционально)
            result_handler: обработчик результатов (опционально)
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
        """
        
        if not self._verification_calc.verify_torque():
            result = self.execute_verification()
            self._result_handler.handle(result)
