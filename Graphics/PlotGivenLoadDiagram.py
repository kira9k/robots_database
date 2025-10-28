import matplotlib.pyplot as plt
import math

from utils.Interfaces import IMotorData, IGearData, ISourceData
from DriverCalculation.VerificationCalculation import VerificationCalculation

class DataGivenLoadDiagram:
    def __init__(self, source_data: ISourceData, motor_data: IMotorData, gear_data: IGearData):
        self.motor_data = motor_data
        self.source_data = source_data
        self.gear_data = gear_data
        self.max_torque_with_gear = VerificationCalculation(self.source_data, self.motor_data, self.gear_data).max_torque_with_gear
        self.max_speed_with_gear = VerificationCalculation(self.source_data, self.motor_data, self.gear_data).max_speed_with_gear

    @property
    def _acceleration_engine_with_gear(self):
        return self.source_data.max_angl_acc * self.gear_data.i_nom
    
    @property
    def _torque_stat_gear(self):
        return self.source_data.max_stat_torque / (self.gear_data.i_nom * self.gear_data.kpd)
    
    @property
    def emf_coef(self):
        return (self.motor_data.U_nom - self.motor_data.R * self.motor_data.I_nom) / (self.motor_data.n_nom * 3.14 / 30)
    
    @property
    def launch_moment(self):
        return self.motor_data.U_nom * self.emf_coef / self.motor_data.R
    
    @property
    def _j_sum(self):
        return self.source_data.eq_torque_intertia / (self.gear_data.i_nom**2 * self.gear_data.kpd) + self.motor_data.J

    @property
    def _torque_dyn_gear(self):
        return self._j_sum * self._acceleration_engine_with_gear
    
    @property
    def torque_start(self):
        return self._torque_stat_gear + self._torque_dyn_gear
    
    @property   
    def torque_stop(self):
        return self._torque_stat_gear - self._torque_dyn_gear
    
    @property
    def torque_nom_with_coef(self):
        return self.motor_data.torque_nom * self.coef_forcing
    
    @property
    def torque_nom(self):
        return self.motor_data.torque_nom
    @property
    def idle_speed(self):
        return self.motor_data.U_nom / self.emf_coef
    
    @property
    def nom_speed(self):
        return self.motor_data.n_nom * math.pi / 30
    
    @property
    def coef_forcing(self):
        return math.ceil((self.max_torque_with_gear / self.motor_data.torque_nom) * 10) / 10 if self.max_torque_with_gear / self.motor_data.torque_nom > 1 else 1 
    
    def get_result(self):
        return {
            "torque_stat_gear": self._torque_stat_gear,
            "torque_dyn_gear": self._torque_dyn_gear,
            "j_sum": self._j_sum,
            "acceleration_engine_with_gear": self._acceleration_engine_with_gear,
            "torque_start": self.torque_start,
            "torque_stop": self.torque_stop,
            'coef_forcing': self.coef_forcing,
            'torque_nom_with_coef': self.torque_nom_with_coef,
            'torque_nom': self.motor_data.torque_nom,
            'emf_coef': self.emf_coef,
            'idle_speed': self.idle_speed,
            'max_speed_with_gear': self.max_speed_with_gear,
            'launch_moment': self.launch_moment,
            'nom_speed': self.nom_speed,
            'torque_nom': self.torque_nom
        }

class PlotLoadDiagram:
    def __init__(self, motor_data: IMotorData, source_data: ISourceData, gear_data: IGearData):
        self.source_data = source_data
        self.motor_data = motor_data
        self.gear_data = gear_data
        self.data_for_orms = DataGivenLoadDiagram(self.source_data, self.motor_data, self.gear_data).get_result()
        self.k, self.b = self._find_line_equation(0, self.data_for_orms['idle_speed'], self.data_for_orms["torque_nom"], self.data_for_orms['nom_speed'])
    
    ##TODO разделить функцию для точек и линий, добавить фасад, вынести функцию линии в utils
    def plot_orms(self):
        plt.plot([self.data_for_orms['torque_stat_gear'], self.data_for_orms['torque_stat_gear']], [0, self.data_for_orms["max_speed_with_gear"]], 'r--')
        plt.plot([self.data_for_orms['torque_start'], self.data_for_orms['torque_start']], [0, self.data_for_orms["max_speed_with_gear"]], color='black')
        plt.plot([self.data_for_orms['torque_stop'], self.data_for_orms['torque_stop']], [0, self.data_for_orms["max_speed_with_gear"]], color='black' )
        plt.plot([0, self.data_for_orms['torque_stat_gear']], [self.data_for_orms['max_speed_with_gear'],self.data_for_orms['max_speed_with_gear']], 'r--')
        plt.plot([self.data_for_orms['torque_stop'], self.data_for_orms['torque_start']], [0,0], color='black')
        plt.plot([self.data_for_orms['torque_start'], self.data_for_orms['torque_stop']], [self.data_for_orms["max_speed_with_gear"],self.data_for_orms["max_speed_with_gear"]], color='black')
        plt.plot([self.data_for_orms['torque_nom_with_coef'], self.data_for_orms['torque_nom_with_coef']], [0, self.k*self.data_for_orms["torque_nom_with_coef"]+self.b], 'g--')
        plt.plot([0, self.data_for_orms["torque_nom_with_coef"]], [self.data_for_orms["idle_speed"], self.k*self.data_for_orms["torque_nom_with_coef"]+self.b], 'g--')
        plt.plot([0, self.data_for_orms['torque_nom']], [self.data_for_orms['nom_speed'],self.data_for_orms['nom_speed']], 'r--')
        plt.plot([self.data_for_orms['torque_nom'], self.data_for_orms['torque_nom']], [0,self.data_for_orms['nom_speed']], 'b--')
        plt.plot([0, self.data_for_orms['torque_nom']], [self.data_for_orms['nom_speed'],self.data_for_orms['nom_speed']], 'b--')
        plt.plot([self.data_for_orms['torque_nom'], self.data_for_orms['torque_nom']], [0,self.data_for_orms['nom_speed']], 'b--')
 
        plt.scatter(self.data_for_orms['torque_stat_gear'], 0, label='Мст')
        plt.scatter(self.data_for_orms['torque_start'], 0, label='Ммакс')
        plt.scatter(self.data_for_orms['torque_stop'],0, label='Мторм')
        plt.scatter(0,self.data_for_orms['idle_speed'], label=r"$\omega$хх")
        plt.scatter(0, self.data_for_orms['nom_speed'], label=r"$\omega$ном")
        plt.scatter(self.data_for_orms['torque_nom_with_coef'], 0, label=r'Мном*$lambda$')
        plt.scatter(self.data_for_orms['torque_nom'], 0, label='Мном')
        plt.scatter(0, self.data_for_orms['max_speed_with_gear'], label=r"$\omega$max")       

        plt.xlabel(r"$M_д$, Нм")
        plt.ylabel(r"$\omega$, рад/с")
        plt.grid()
        plt.legend()
        plt.title("Приведённая диаграмма нагрузки и ОРМС двигателя.")
        plt.show()
    
    @staticmethod
    def _find_line_equation(x1, y1, x2, y2):
        """Находит уравнение прямой по двум точкам"""
        if x1 == x2:
            return None, x1
        k = (y2 - y1) / (x2 - x1)

        b = y1 - k * x1


        return k,b