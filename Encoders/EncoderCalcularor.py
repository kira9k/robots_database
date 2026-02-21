import math

class EncoderCalculator:
    def __init__(self, error, gear_data):
        self.error = error.third_error
        self.i = gear_data.i_nom

    @property
    def dicrete_number(self):
        self.number_of_discrete = math.pi/ (2 * self.error * self.i) 
        return math.ceil(self.number_of_discrete)

    def __str__(self):
        return f"Минимальное необходимое количество дискрет: {self.dicrete_number}"