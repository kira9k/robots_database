from json import encoder

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox
)   
from .ResultWindow import ResultWindow
from utils.SourData import SourceDataDriver, DataDriver, DataGear
from DriverCalculation.Facade import DCMotorEnergyFacade, FindEngineFacade, FindEncoderFacade, EncoderFacade
from DriverCalculation.GearCalculate import GearCalulator
from DriverCalculation.EnergyCalulation import DCMotorPowerTorqueReCalculator
from DriverCalculation.VerificationCalculation import VerificationCalculation
from Graphics.PlotGivenLoadDiagram import PlotLoadDiagram, DataGivenLoadDiagram
from ThermalVerification import ThermalCalculator
from Synthesis.dynamic_error import DynamicErrorCalculator, ErrorData
import math
from sqlalchemy import select
from .DesignWindow import DesignWindow
from .TableWindow import TableWindow
from DataBase.connection_db import engine as db_engine
from sqlalchemy.orm import sessionmaker
import sys
from DataBase.ORMModel import EngineDC, Gear, Encoder



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("База данных PostgreSQL")
        self.setGeometry(100, 100, 800, 600)
        
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        self.TableWindow = TableWindow
        
        self.btn_open_table = QPushButton("Открыть таблицу двигателей")
        self.btn_open_table.clicked.connect(lambda: self.create_table_window(EngineDC))
        layout.addWidget(self.btn_open_table)
        
        self.btn_open_table = QPushButton("Открыть таблицу редукторов")
        self.btn_open_table.clicked.connect(lambda: self.create_table_window(Gear))
        layout.addWidget(self.btn_open_table)

        self.btn_open_table = QPushButton("Открыть таблицу энкодеров")
        self.btn_open_table.clicked.connect(lambda: self.create_table_window(Encoder))
        layout.addWidget(self.btn_open_table)

        self.btn_design = QPushButton("Спроектировать электропривод")
        self.btn_design.clicked.connect(lambda: self.create_design_window())
        layout.addWidget(self.btn_design)

    def create_table_window(self, orm_model):
        self.table_window = self.TableWindow(orm_model)
        self.table_window.show()

    def create_design_window(self):
        self.design_window = DesignWindow()
        self.design_window.data_ready.connect(self.on_design_data)
        self.design_window.show()

    def on_design_data(self, data):
        sd = data

        # Запускаем расчёты (по аналогии с main.py)
        calculator = DCMotorEnergyFacade(sd)
        results = calculator.get_all_calculations()

        power = results.get('power')
        torque = results.get('torque')

        # Поиск двигателя в БД
        find_engine_facade = FindEngineFacade()
        closest_engine = find_engine_facade.find_closest_engine_power(EngineDC, power)

        if closest_engine:
            k = (closest_engine["u_nom"] - closest_engine["i_nom"] * closest_engine["r_nom"]) / (closest_engine["n_nom"] * math.pi / 30)
            motor_data = DataDriver(
                name=closest_engine["model"],
                p_nom=closest_engine["p_nom"],
                torque_nom=closest_engine["m_nom"],
                n_nom=closest_engine["n_nom"],
                U_nom=closest_engine["u_nom"],
                I_nom=closest_engine["i_nom"],
                R=closest_engine["r_nom"],
                J=closest_engine["j_nom"],
                m=closest_engine.get("m", 0),
                k=k,
            )
        else:
            motor_data = None

        # Редуктор
        if motor_data:
            gear_calculator = GearCalulator(sd, motor_data)
            optimal_gear_ratio = getattr(gear_calculator, 'gear_ratio_optimal', None)
        else:
            optimal_gear_ratio = None
        closest_gear = find_engine_facade.find_closest_gear_i(Gear, optimal_gear_ratio, sd, results)
        gear_data = DataGear(
            name=closest_gear["gear_name"],
            i_nom=closest_gear["i"],
            m=closest_gear["mass"],
            kpd=closest_gear["efficiency"],
            c = closest_gear["c"],
            clearance = closest_gear["clearance"],
            speed_norm = closest_gear["speed_norm"],
            torque_nom = closest_gear["torque_nom"]
            )

        dc_motor_power_Torque_Re_Calculator = DCMotorPowerTorqueReCalculator(sd, gear_data, motor_data)

        orms = DataGivenLoadDiagram(sd, motor_data, gear_data)
        orms_res = orms.get_result()
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
        error = DynamicErrorCalculator(sd, motor_data, gear_data)
        calculator_enc = EncoderFacade(error, gear_data)
        results_enc = calculator_enc.get_minimal_lines_count
        find_encoder_facade = FindEncoderFacade()
        closest_encoder = find_encoder_facade.find_closest_encoder_lines(Encoder, results_enc, sd, gear_data)
        # create as independent top-level window (no parent)
        
        self.result_window = ResultWindow(results, motor_data, optimal_gear_ratio, source_data=sd, gear=closest_gear, recalc_results=recalc_results, orms_results=orms_res, thermal_data=thermal_data, error=error.get_data(), enc_min=results_enc, closest_encoder=closest_encoder)
        self.result_window.show()
