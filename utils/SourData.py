from dataclasses import dataclass
from .Interfaces import ISourceData, IMotorData, IGearData

@dataclass
class SourceDataDriver(ISourceData):
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
    max_angl_acc: float
    max_angle_speed_wm: float
    max_angle_acc_wm: float
    tp: float
    tp_rel: float
    max_stat_torque: float
    max_dyn_torque: float
    eq_torque_intertia: float
    max_error: float


@dataclass
class DataDriver(IMotorData):
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

    name: str
    p_nom: float
    torque_nom: float
    n_nom: float
    U_nom: float
    I_nom: float
    R: float
    J: float
    m: float
    k: float

        

@dataclass
class DataGear(IGearData):
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

    name: str
    i_nom: float
    m: float
    kpd: float
    c: float
    clearance: float
    speed_norm: float
    torque_nom: float

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
