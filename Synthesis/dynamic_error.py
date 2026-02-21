from dataclasses import dataclass

@dataclass
class ErrorData:
    """Класс для хранения данных об ошибках."""
    first_error: float
    second_error: float
    third_error: float
    fourth_error: float
    fifth_error: float


class DynamicErrorCalculator:
    def __init__(self, source_data, motor_data, gear_data):
        self.source_data = source_data
        self.motor_data = motor_data
        self.gear_data = gear_data

    @property
    def first_error(self):
        #sum_torque = (self.source_data.max_stat_torque + self.source_data.max_dyn_torque) 
        first_error = self.source_data.max_stat_torque / (self.gear_data.kpd*self.gear_data.c)
        return first_error

    @property
    def second_error(self):
        return self.gear_data.clearance / 2
    
    @property
    def third_plus_fourth_error(self):
        return self.source_data.max_error - self.first_error - self.second_error

    @property
    def third_error(self):
        return self.third_plus_fourth_error * 0.05
    
    @property
    def fourth_error(self):
        return self.third_plus_fourth_error * 0.95

    @property
    def fifth_error(self):
        return 0 
    
    def get_data(self):
        return ErrorData(
            first_error=self.first_error,
            second_error=self.second_error,
            third_error=self.third_error,
            fourth_error=self.fourth_error,
            fifth_error=self.fifth_error
        )

    def __str__(self):
        """
        Возвращает строковое представление объекта с информацией об ошибках.
        """
        total_error = (self.first_error + self.second_error + self.third_error + 
                       self.fourth_error + self.fifth_error)

        return (
            f'Первая допустимая ошибка: {self.first_error}\n'
            f'Вторая допустимая ошибка: {self.second_error}\n'
            f'Третья допустимая ошибка: {self.third_error}\n'
            f'Четвертая допустимая ошибка: {self.fourth_error}\n'
            f'Пятая допустимая ошибка: {self.fifth_error}\n'
            f'Суммарная допустимая ошибка: {total_error}'
        )


