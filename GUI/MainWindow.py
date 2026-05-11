from json import encoder

from PySide6.QtWidgets import (
 QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QGroupBox
)   
from .ResultWindow import ResultWindow
from utils.SourData import  DataDriver, DataGear, CoefRegulators, DataEncoder
from DriverCalculation.Facade import DCMotorEnergyFacade, FindEngineFacade, FindEncoderFacade, EncoderFacade
from DriverCalculation.GearCalculate import GearCalulator
from DriverCalculation.EnergyCalulation import DCMotorPowerTorqueReCalculator
from Graphics.PlotGivenLoadDiagram import PlotLoadDiagram, DataGivenLoadDiagram
from ThermalVerification import ThermalCalculator
from Synthesis.dynamic_error import DynamicErrorCalculator
from .DesignWindow import DesignWindow
from .TableWindow import TableWindow
from DataBase.ORMModel import EngineDC, Gear, Encoder, Result, SourceData, Utils
from DataBase.ORMModel import CoefRegulators as CoefRegulatorsORM
from Synthesis.LAFC import LAFC, PWM
from Synthesis.CurrentControl import CurrentControlPI, SpeedControlPI, PositionComtrolP
from MatlabTest.MatlabLAB2 import MatlabLAB2

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Электропривод")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Группа для таблиц
        tables_group = QGroupBox("Базы данных")
        tables_layout = QVBoxLayout(tables_group)
        
        self.TableWindow = TableWindow
        
        # Список кнопок для удобного добавления
        buttons_info = [
            ("Двигателей", EngineDC),
            ("Редукторов", Gear),
            ("Энкодеров", Encoder),
            ("Электроприводов", Result),
            ("Коэффициентов регуляторов", CoefRegulatorsORM),
            ("Вспомогательных данных", Utils),
            ("Исходных данных", SourceData)
        ]
        
        for btn_text, table_class in buttons_info:
            btn = QPushButton(f"Открыть таблицу {btn_text.lower()}")
            btn.clicked.connect(lambda checked, tc=table_class: self.create_table_window(tc))
            tables_layout.addWidget(btn)
        
        main_layout.addWidget(tables_group)
        
        # Группа для расчётов
        design_group = QGroupBox("Расчёт")
        design_layout = QVBoxLayout(design_group)
        
        self.btn_design = QPushButton("Спроектировать электропривод")
        self.btn_design.clicked.connect(self.create_design_window)
        design_layout.addWidget(self.btn_design)
        
        main_layout.addWidget(design_group)
        
        # Растягивающийся элемент в конце
        main_layout.addStretch()
        
        self.matlab_lab2 = MatlabLAB2()

    def create_table_window(self, orm_model):
        self.table_window = self.TableWindow(orm_model)
        self.table_window.show()

    def create_design_window(self):
        self.design_window = DesignWindow()
        self.design_window.data_ready.connect(self.on_design_data)
        self.design_window.show()

    def on_design_data(self, data):
        sd = data
        calculator = DCMotorEnergyFacade(sd)
        while True:
            #print(sd.__dict__)
            results = calculator.get_all_calculations()
            print(results)
            power = results.get('power')
            torque = results.get('torque')

            # Поиск двигателя в БД
            find_engine_facade = FindEngineFacade()
            closest_engine = find_engine_facade.find_closest_engine_power(EngineDC, power)

            if closest_engine:
                motor_data = DataDriver(
                    id = closest_engine["id"],
                    name=closest_engine["model"],
                    p_nom=closest_engine["p_nom"],
                    torque_nom=closest_engine["m_nom"],
                    n_nom=closest_engine["n_nom"],
                    U_nom=closest_engine["u_nom"],
                    I_nom=closest_engine["i_nom"],
                    R=closest_engine["r_nom"],
                    J=closest_engine["j_nom"],
                    m=closest_engine.get("m", 0),
                    L_a=closest_engine.get("l_a", 0),
                    max_current=closest_engine.get("max_current", closest_engine["i_nom"]*5),
                    drawing=closest_engine.get("drawing")
                )
            else:            
                QMessageBox.warning(self, "Предупреждение", "Не найден подходящий двигатель в базе данных.")
                return

            # Редуктор
            if motor_data:
                gear_calculator = GearCalulator(sd, motor_data)
                optimal_gear_ratio = getattr(gear_calculator, 'gear_ratio_optimal', None)
                print(optimal_gear_ratio)
            else:
                optimal_gear_ratio = None
            closest_gear = find_engine_facade.find_closest_gear_i(Gear, optimal_gear_ratio, sd, results)
            gear_data = DataGear(
                id = closest_gear["id"],
                name=closest_gear["gear_name"],
                i_nom=closest_gear["i"],
                m=closest_gear["mass"],
                kpd=closest_gear["efficiency"],
                c = closest_gear["c"],
                clearance = closest_gear["clearance"],
                speed_norm = closest_gear["speed_norm"],
                torque_nom = closest_gear["torque_nom"],
                efficiency=closest_gear["efficiency"],
                drawing=closest_gear.get("drawing")
                )

            dc_motor_power_Torque_Re_Calculator = DCMotorPowerTorqueReCalculator(sd, gear_data, motor_data)

            orms = DataGivenLoadDiagram(sd, motor_data, gear_data)
            orms_res = orms.get_result()
            if orms_res["torque_start"] > motor_data.torque_nom * gear_data.kpd:
                calculator.change_required_power_margin()
                continue
            if orms_res["max_speed_with_gear"] > orms_res["nom_speed"]:
                calculator.change_required_power_margin()
                continue
            orms_chart = PlotLoadDiagram(motor_data, sd, gear_data)
            orms_chart.save_plot()

            # Показать результаты в отдельном окне
            recalc_results = {
                'required_power_with_gear': dc_motor_power_Torque_Re_Calculator.required_power_with_gear,
                'required_torque_with_gear': dc_motor_power_Torque_Re_Calculator.required_torque_with_gear,
                'required_speed_with_gear': dc_motor_power_Torque_Re_Calculator.required_speed_with_gear
            }
            self.source_input_data = sd
            thermal_calculator = ThermalCalculator(sd, motor_data, gear_data)
            thermal_data = thermal_calculator.get_data()
            thermal_is_ok = thermal_calculator.run()
            if not thermal_is_ok:
                calculator.change_required_power_margin()
                continue
            error = DynamicErrorCalculator(sd, motor_data, gear_data)
            calculator_enc = EncoderFacade(error, gear_data)
            results_enc = calculator_enc.get_minimal_lines_count
            find_encoder_facade = FindEncoderFacade()
            closest_encoder = find_encoder_facade.find_closest_encoder_lines(Encoder, results_enc, sd, gear_data)
            if closest_encoder is None:
                QMessageBox.warning(self, "Предупреждение", "Не найден подходящий энкодер в базе данных.")
                return
            
            closest_encoder_data = DataEncoder(
                id=closest_encoder["id"],
                name=closest_encoder["encoder_name"],
                m=closest_encoder["weight"],
                j=closest_encoder["rotor_moment_of_inertia"],
                max_speed=closest_encoder["maximum_rotation_speed"],
                N=closest_encoder["lines_count"],
                drawing=closest_encoder["drawing"]
            )
            break

        LAFC_calc = LAFC(motor_data, gear_data, sd, error.get_data(), orms_res, thermal_data)
        PWM_calc = PWM(motor_data, gear_data, sd, error.get_data(), orms_res, thermal_data) 
        current_control_calc = CurrentControlPI(motor_data, gear_data, sd, error.get_data(), orms_res, thermal_data) 
        speed_control_calc = SpeedControlPI(motor_data, gear_data, sd, error.get_data(), orms_res, thermal_data)
        position_control_calc = PositionComtrolP(motor_data, gear_data, sd, error.get_data(), orms_res, thermal_data, closest_encoder)
        print(f"""Tm = {LAFC_calc._Tm}\n
              T_e = {motor_data.T_e}\n
              Lk = {LAFC_calc._Lk}\n 
              freq_srez_1 = {LAFC_calc._freq_srez_1}\n
              transition_duration = {LAFC_calc._transition_duration}\n
              freq_srez_2 = {LAFC_calc._freq_srez_2}\n
              freq_2 = {LAFC_calc._freq_2}\n
              freq_srez_3 = {LAFC_calc._freq_3}\n
              T_u = {PWM_calc.T_u}\n
              k_pwm = {PWM_calc.k_pwm}\n
              k_rc = {current_control_calc.k_rc}\n
              k_osc = {current_control_calc.k_osc}\n
              k_ric = {current_control_calc.k_ric}\n
              k_oss = {speed_control_calc.k_oss}\n
              k_rs = {speed_control_calc.k_rs}\n
              k_ris = {speed_control_calc.k_ris}\n
              k_osa = {position_control_calc.k_osa}\n
              k_ra = {position_control_calc.k_ra}
              k_rai = {position_control_calc.k_rai}
              """)
        self.coef_regulators = CoefRegulators(
            k_a=position_control_calc.k_ra,
            k_da =position_control_calc.k_osa,
            k_ai=position_control_calc.k_rai,
            k_c=current_control_calc.k_rc,
            k_dc=current_control_calc.k_osc,
            k_ci=current_control_calc.k_ric,
            k_ds=speed_control_calc.k_oss,
            k_s=speed_control_calc.k_rs,
            k_si=speed_control_calc.k_ris,
            k_pwm=PWM_calc.k_pwm,
            T_pwm=PWM_calc.T_u,
        )

        self.utils = Utils(
            A_e=thermal_data.get('A_eqv'),
            omega_e=thermal_data.get('omega_eqv'),
            dyn_error=error.get_data().fourth_error,
            stat_error=error.stat_error
        )

        self.matlab_lab2.run_simulation("lab12_a", sd, orms_res, thermal_data, motor_data, gear_data, self.coef_regulators, flag_calc=True)
        self.coef_regulators.k_a = self.matlab_lab2.value
        self.coef_regulators.k_ai = self.matlab_lab2.value_i
        self.coef_regulators.k_feedforward = self.matlab_lab2.value_ff
        self.result_window = ResultWindow(results, motor_data, optimal_gear_ratio, source_data=sd, gear=gear_data, recalc_results=recalc_results, orms_results=orms_res, thermal_data=thermal_data, error=error.get_data(), enc_min=results_enc, closest_encoder=closest_encoder_data, coef_regulators=self.coef_regulators, utils=self.utils)
        self.result_window.show()
