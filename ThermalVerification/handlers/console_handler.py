"""Обработчик вывода результатов в консоль."""

from .base import IVerificationResultHandler
from ..models.verification_result import ThermalVerificationResult


class ConsoleResultHandler(IVerificationResultHandler):
    """Выводит результаты проверки в консоль."""
    
    def handle(self, result: ThermalVerificationResult) -> None:
        """Вывод результата в консоль."""
        print(result)
