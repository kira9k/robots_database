import math

from dataclasses import dataclass
#from .Interfaces import ISourceData, IMotorData, IGearData
from DataBase.repository import DatabaseRepository
from DataBase.ORMModel import EngineDC, Gear, Encoder, SourceData, CoefRegulators, Utils

@dataclass
class SourceDataDriver:
    """
    Исходные данные для расчета привода
    
    Attributes:
        max_angl_speed: максимальная угловая скорость, 1/c
        max_angl_acc: максимальное угловое ускорение, 1/c^-2
        max_angl_speed_wm: максимальная угловая скорость рабочего движения, 1/с
        max_angl_acc_wm: максимальное угловое ускорение рабочего движения, 1/с^-2
        tp: длительность разгона до максимальной скорости, с
        tp_rel: относительная длительность "переброски" в рабочем цикле, с  
        max_stat_torque: максимальный статический момент сил, Нм
        max_dyn_torque: максимальный динамический момент, Нм
        eq_torque_intertia: эквивалентный момент инерции, кг*м^2,
        max_error: допускаемая погрешность привода, рад
    """
    
    max_angl_speed: float
    max_angle_speed_wm: float
    max_angle_acc_wm: float
    tp: float
    tp_rel: float
    max_stat_torque: float
    eq_torque_intertia: float
    max_error: float
    reg_angle: int = 1
    reg_speed: int = 0
    reg_current: int = 0
    non_linear_correction: bool = False
    feedforward: bool = False
    transition_time: float = 0.1
    overshoot: float = 5
    
    def __post_init__(self):
        self.max_angl_acc = self.max_angl_speed / self.tp
        self.max_dyn_torque = self.max_angl_acc * self.eq_torque_intertia


@dataclass
class DataDriver():
    """
    Характеристики выбранного двигателя

    Attributes:
        name: Название двигателя,
        p_nom: Номинальная мощность двигателя, Вт
        torque_nom: Номинальный момент двигателя, Нм
        n_nom: Номинальная частотка вращения, об/мин
        U_nom: Номинальное напряжение якоря, В
        I_nom: Номинальный ток якоря, А
        R: Активное сопротивление якоря, Ом,
        J: Момент инерции ротора, кг*м^2
        m: Масса двигателя
    """
    id: int
    name: str
    p_nom: float
    torque_nom: float
    n_nom: float
    U_nom: float
    I_nom: float
    R: float
    J: float
    m: float
    L_a: float
    max_current: float
    drawing: str = None
    
    def __post_init__(self):        
        self.k = (self.U_nom - self.I_nom * self.R) / (self.n_nom * math.pi / 30)
        self.T_e = self.L_a / self.R
        self.T_m = self.J * self.R / self.k**2
        self.type = DatabaseRepository().get_type_elements(EngineDC, self.id)
        self.company = DatabaseRepository().get_company_name(EngineDC, self.id)

@dataclass
class DataGear():
    """
    Характеристики волнового редуктора
    
    Attributes:
        name: Название редуктора
        i_nom: Передаточное число редуктора,
        m: Масса редуктора, кг
        kpd: КПД редуктора
        c: Жесткость редуктора, Нм/рад
        clearance: Люфт редуктора, рад
        speed_norm: Номинальная скорость вращения редуктора, об/мин
        torque_norm: Номинальный момент выходного вала редуктора, Нм
    """ 
    id: int
    name: str
    i_nom: float
    m: float
    kpd: float
    c: float
    clearance: float
    speed_norm: float
    torque_nom: float
    efficiency: float
    drawing: str = None

    def __post_init__(self):
        self.type = DatabaseRepository().get_type_elements(Gear, self.id)
        self.company = DatabaseRepository().get_company_name(Gear, self.id)

@dataclass
class DataEncoder:

    id: int
    name: str
    N: float
    m: float 
    max_speed: float
    j: float
    drawing: str = None

    def __post_init__(self):
        self.type = DatabaseRepository().get_type_elements(Encoder, self.id)
        self.company = DatabaseRepository().get_company_name(Encoder, self.id)

@dataclass
class MechanicalSystemData:
    """Отвечает только за хранение расчетных данных"""
    torque_stat_gear: float
    torque_dyn_gear: float
    j_sum: float
    acceleration_engine_with_gear: float
    torque_start: float
    torque_stop: float
    coef_forcing: float
    torque_nom_with_coef: float
    torque_nom: float
    emf_coef: float
    idle_speed: float
    max_speed_with_gear: float
    launch_moment: float
    nom_speed: float

@dataclass
class EqvParametr:
    A_eqv: float
    omega_eqv: float

@dataclass
class CoefRegulators:
    k_a: float
    k_da: float
    k_ai: float
    k_c: float
    k_dc: float
    k_ci: float
    k_ds: float
    k_s: float
    k_si: float
    k_pwm: float
    T_pwm: float
    k_feedforward: float = 0.01

@dataclass
class Utils:
    """Класс для хранения утилитных данных, которые не подходят ни под одну из других категорий"""
    id: int
    A_e: float
    omega_e: float
    dyn_error: float
    stat_error: float