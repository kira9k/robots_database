"""Стратегия проверки по номинальному моменту двигателя."""

from utils.Interfaces import IMotorData
from .base import IThermalVerificationStrategy


class MotorTorqueVerificationStrategy(IThermalVerificationStrategy):
    """
    Конкретная реализация стратегии проверки.
    """
    
    def __init__(self, motor_data: IMotorData):
        self._motor_data = motor_data
    
    def verify(self, torque_eqv_square: float) -> bool:
        """Проверка: квадрат номинального момента должен быть больше эквивалентного."""
        return self._motor_data.torque_nom ** 2 > torque_eqv_square
