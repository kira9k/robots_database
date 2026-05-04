import math
import os 

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from DataBase.ORMModel import Result, SourceData, CoefRegulators, Utils, EngineDC, Gear, Encoder
from Graphics.PlotGivenLoadDiagram import DataGivenLoadDiagram
from DataBase.repository import DatabaseRepository
from MatlabTest.MatlabLAB2 import MatlabLAB2
from utils.SourData import SourceDataDriver, DataDriver, DataGear, CoefRegulators, DataEncoder
from GUI import html_func


class ResultShowWindow(QWidget):
    def __init__(self, motor=None, source_data=None, gear=None, closest_encoder=None, coef_regulators=None, utils=None):
        super().__init__()
        self.setWindowTitle("Результаты расчёта")
        self.resize(600, 400)
        self.setWindowFlag(Qt.Window, True)
        
        self.matlab_lab2 = MatlabLAB2()

        self.source_data = SourceDataDriver(max_angl_speed=getattr(source_data, 'max_speed', 0),
                                            max_angle_speed_wm=getattr(source_data, 'max_speed_work', 0),
                                            max_angle_acc_wm=getattr(source_data, 'max_acc', 0),
                                            tp=getattr(source_data, 'acc_duration', 0),
                                            tp_rel=getattr(source_data, 'rel_duration', 0),
                                            max_stat_torque=getattr(source_data, 'max_torque', 0),
                                            eq_torque_intertia=getattr(source_data, 'max_inertia_torque', 0),
                                            max_error=getattr(source_data, 'max_error', 0),
                                            overshoot=getattr(source_data, 'overshoot', 0),
                                            transition_time=getattr(source_data, 'transition_time', 0))
        self.motor_data = DataDriver(
                id = getattr(motor, 'id', 0),
                name=getattr(motor, 'model', ''),
                p_nom=getattr(motor, 'p_nom', 0),
                torque_nom=getattr(motor, 'm_nom', 0),
                n_nom=getattr(motor, 'n_nom', 0),
                U_nom=getattr(motor, 'u_nom', 0),
                I_nom=getattr(motor, 'i_nom', 0),
                R=getattr(motor, 'r_nom', 0),
                J=getattr(motor, 'j_nom', 0),
                m=getattr(motor, 'm', 0),
                L_a=getattr(motor, 'l_a', 0),
                max_current=getattr(motor, 'max_current', getattr(motor, 'i_nom', 0) * 5),
                drawing=getattr(motor, 'drawing', None)
            )
        
        self.gear =  DataGear(
            id = getattr(gear, 'id', 0),
            name=getattr(gear, 'gear_name', ''),
            i_nom=getattr(gear, 'i', 0),
            m=getattr(gear, 'mass', 0),
            kpd=getattr(gear, 'efficiency', 0),
            c = getattr(gear, 'c', 0),
            clearance = getattr(gear, 'clearance', 0),
            speed_norm = getattr(gear, 'speed_norm', 0),
            torque_nom = getattr(gear, 'torque_nom', 0),
            efficiency=getattr(gear, 'efficiency', 0),
            drawing=getattr(gear, 'drawing', None)
            )

        
        
        self.closest_encoder = DataEncoder(
            id=getattr(closest_encoder, 'id', 0),
            name=getattr(closest_encoder, 'encoder_name', ''),
            m=getattr(closest_encoder, 'weight', 0),
            j=getattr(closest_encoder, 'rotor_moment_of_inertia', 0),
            max_speed=getattr(closest_encoder, 'maximum_rotation_speed', 0),
            N=getattr(closest_encoder, 'lines_count', 0),
            drawing=getattr(closest_encoder, 'drawing', None)
        )
        
        self.coef_regulators = coef_regulators
        self.utils = utils
        
        orms = DataGivenLoadDiagram(self.source_data, self.motor_data, self.gear)
        orms_res = orms.get_result()
        self.matlab_lab2.run_simulation("lab12_a", self.source_data,orms_res, self.utils, self.motor_data, self.gear, self.coef_regulators, flag_calc=False)

        layout = QVBoxLayout(self)
        self.text = QTextEdit(self)        
        self.text.setReadOnly(True)
        self.text.setStyleSheet("""
            QTextEdit {
                font-size: 10pt;
                }
            """)
        
        html = html_func.html_source_data(self.source_data)
        html += html_func.html_found_motor(self.motor_data)
        html += html_func.html_found_gear(self.gear)
        html += html_func.html_found_encoder(self.closest_encoder)
        html += html_func.html_coef_regulators(self.coef_regulators)
        html += html_func.html_utils_data(self.utils)
        html += html_func.html_matlab_test()

        self.text.setHtml(html)
        layout.addWidget(self.text)
        
        btn_close = QPushButton("Закрыть")
        
        btn_close.clicked.connect(self.close)
        
        layout.addWidget(btn_close)