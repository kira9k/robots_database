"""Модель результата проверки."""

class ThermalVerificationResult:
    """
    Value Object для хранения результатов проверки.
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
