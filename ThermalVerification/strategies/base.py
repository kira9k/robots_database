"""Базовые интерфейсы для стратегий проверки."""

from abc import ABC, abstractmethod


class IThermalVerificationStrategy(ABC):
    """
    Абстрактный интерфейс для стратегий проверки.
    """
    
    @abstractmethod
    def verify(self, torque_eqv_square: float) -> bool:
        """
        Выполнить проверку тепловых условий.
        
        Args:
            torque_eqv_square: квадрат эквивалентного момента
            
        Returns:
            True если проверка пройдена, False иначе
        """
        pass
