from utils.SourData import SourceDataDriver, DataDriver, DataGear
from DriverCalculation.Facade import DCMotorEnergyFacade, DBFacade, FindEngineFacade
from DriverCalculation.GearCalculate import GearCalulator
from DataBase.ORMModel import EngineDC, Gear, EngineType
from DriverCalculation.EnergyCalulation import DCMotorPowerTorqueReCalculator
from DriverCalculation.VerificationCalculation import VerificationCalculation
from Graphics.PlotGivenLoadDiagram import PlotLoadDiagram, DataGivenLoadDiagram

import math

def main():
    # Инициализация репозитория для работы с базой данных

    ###для теста###
    engine_dc = EngineDC
    gear = Gear
    ###конец теста###

    engine_bd = DBFacade(engine_dc)
    gear_bd = DBFacade(gear)
    source_data = SourceDataDriver(
        max_angl_speed=0.66,
        max_angl_acc=1.9,
        max_angle_speed_wm=0.4,
        max_angle_acc_wm=0.2,
        tp=0.35,
        tp_rel=0.2,
        max_stat_torque=235.2,
        max_dyn_torque=39.672,
        eq_torque_intertia=20.88
    )


    # Использование фасада для расчетов
    calculator = DCMotorEnergyFacade(source_data)
    results = calculator.get_all_calculations()
    

    # Вывод результатов
    print("=== РЕЗУЛЬТАТЫ РАСЧЕТОВ ===")
    print(f"Требуемая мощность: {results['power']:.2f} Вт")
    print(f"Требуемый момент: {results['torque']:.2f} Нм")
    ###ДЛЯ ТЕСТА###
    find_engine_facade = FindEngineFacade()
    closest_engine = find_engine_facade.find_closest_engine_power(engine_dc, results['power'])
    k = (closest_engine["u_nom"] - closest_engine["i_nom"] * closest_engine["r_nom"]) / (closest_engine["n_nom"] * math.pi / 30)
    print(k)
    print("=== НАЙДЕННЫЙ ДВИГАТЕЛЬ ===")
    motor_data = DataDriver(
        name=closest_engine["model"],
        p_nom=closest_engine["p_nom"],
        torque_nom=closest_engine["m_nom"],
        n_nom=closest_engine["n_nom"],
        U_nom=closest_engine["u_nom"],
        I_nom=closest_engine["i_nom"],
        R=closest_engine["r_nom"],
        J=closest_engine["j_nom"],
        m=closest_engine["m"],
        k=k)
    print(motor_data.__dict__)


    ##Редуктор###
    gear_calculator = GearCalulator(source_data, motor_data)
    optimal_gear_ratio = gear_calculator.gear_ratio_optimal
    print(f"Оптимальное передаточное отношение: {optimal_gear_ratio:.2f}")
    closest_gear = find_engine_facade.find_closest_gear_i(gear, optimal_gear_ratio)
    print("=== НАЙДЕННЫЙ РЕДУКТОР ===")
    gear_data = DataGear(
        name=closest_gear["gear_name"],
        i_nom=closest_gear["i"],
        m=closest_gear["mass"],
        kpd=closest_gear["efficiency"]
    )
    print(gear_data.__dict__)
    dc_motor_power_Torque_Re_Calculator = DCMotorPowerTorqueReCalculator(source_data, gear_data)
    print("=== РАСЧЕТЫ С УЧЕТОМ РЕДУКТОРА ===")
    print(f"Максимальная мощность с учетом КПД редуктора: {dc_motor_power_Torque_Re_Calculator.required_power_with_gear:.2f}")
    print(f"Максимальный необходимый момент с учетом КПД редуктора: {dc_motor_power_Torque_Re_Calculator.required_torque_with_gear:.2f}")
    ###КОНЕЦ ТЕСТА###
    verify = VerificationCalculation(source_data, motor_data, gear_data)
    torque_ok = verify.verify_torque()
    speed_ok = verify.verify_speed()
    print("=== ВЕРИФИКАЦИЯ ===")
    print(f"Проверка момента: {'ОК' if torque_ok else 'НЕ ОК'}")
    print(f"Проверка скорости: {'ОК' if speed_ok else 'НЕ ОК'}")

    # print(f"Максимальный необходимы момент с учетом КПД редуктора: {results['max torque_with kpd']:.2f}")
    #print(gear_bd.get_all())
    ###ТЕСТ ОРМС###
    orms = DataGivenLoadDiagram(source_data, motor_data, gear_data)
    print(orms.get_result())
    plot = PlotLoadDiagram(motor_data, source_data, gear_data)
    plot.plot_orms()
    

if __name__ == "__main__":
    main()