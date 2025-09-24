from DriverCalculation.SourData import SourceDataDriver, DataDriver, DataGear
from DriverCalculation.Facade import DCMotorEnergyFacade, EngineDCFacade



def main():
    # Инициализация репозитория для работы с базой данных
    engine_bd = EngineDCFacade()
   
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

    # Создание данных двигателя
    motor_data = DataDriver(
        name='Example Motor',
        p_nom=660,
        torque_nom=2.1,
        n_nom=3000,
        U_nom=48,
        I_nom=15.3,
        R=0.16,
        J=2.4e-3,
        m=4
    )

    gear_data = DataGear(
        name="name",
        i_nom=160,
        m=0.69,
        kpd=0.83
    )

    # Использование фасада для расчетов
    calculator = DCMotorEnergyFacade(source_data, motor_data, gear_data)
    results = calculator.get_all_calculations()

    # Вывод результатов
    print("=== РЕЗУЛЬТАТЫ РАСЧЕТОВ ===")
    print(f"Требуемая мощность: {results['power']:.2f} Вт")
    print(f"Требуемый момент: {results['torque']:.2f} Нм")
    print(f"Оптимальное передаточное отношение: {results['gear_ratio']:.2f}")
    print(f"Максимальный необходимы момент с учетом КПД редуктора: {results['max torque_with kpd']:.2f}")
    print(engine_bd.get_all_engines())
    

if __name__ == "__main__":
    main()