"""Базовый интерфейс для обработчиков результатов проверки."""

from abc import ABC, abstractmethod
from ..models.verification_result import ThermalVerificationResult


class IVerificationResultHandler(ABC):
    """
    Абстрактный базовый класс для обработчиков результатов.
    Примеры реализации:
    - ConsoleResultHandler - вывод в консоль
    - FileResultHandler - сохранение в файл
    - LoggerResultHandler - логирование
    - DatabaseResultHandler - сохранение в БД
    """
    
    @abstractmethod
    def handle(self, result: ThermalVerificationResult) -> None:
        """
        Обработать результат проверки.        
        Args:
            result: объект ThermalVerificationResult с результатами проверки
            
        Returns:
            None
            
        Raises:
            NotImplementedError: если метод не реализован в подклассе
        """
        pass
