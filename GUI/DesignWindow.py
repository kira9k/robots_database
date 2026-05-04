from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QGroupBox, QCheckBox
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDoubleValidator

from utils.SourData import SourceDataDriver  

class DesignWindow(QWidget):
    data_ready = Signal(object)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Исходные данные для проектирования")
        self.resize(600, 600)
        
        # --------------- Главный layout ---------------
        layout = QVBoxLayout()
        
        self.label = QLabel("Исходные данные для проектирования", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.label)

        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        validator.setBottom(0.0)

        # --------------- Требования к исполнительной сиситеме ---------------
        design_group = QGroupBox("Требования к исполнительной системе")
        design_layout = QVBoxLayout()

        self.input_max_angl_speed = QLineEdit()
        design_layout.addWidget(QLabel("Максимальная угловая скорость, рад/с"))
        design_layout.addWidget(self.input_max_angl_speed)
        self.input_max_angl_speed.setText("3.75")
        #self.input_max_angl_speed.setText("2.49")  
        self.input_max_angl_speed.setValidator(validator)

        self.input_max_angle_speed_wm = QLineEdit()
        design_layout.addWidget(QLabel("Максимальная угловая скорость рабочего движения, рад/с"))
        design_layout.addWidget(self.input_max_angle_speed_wm)
        self.input_max_angle_speed_wm.setText("1.8754")
        #self.input_max_angle_speed_wm.setText("1.245")
        self.input_max_angle_speed_wm.setValidator(validator)

        self.input_max_angle_acc_wm = QLineEdit()
        design_layout.addWidget(QLabel("Максимальное угловое ускорение рабочего движения, рад/с²"))
        design_layout.addWidget(self.input_max_angle_acc_wm)
        self.input_max_angle_acc_wm.setText("7.5")
        #self.input_max_angle_acc_wm.setText("4.983")
        self.input_max_angle_acc_wm.setValidator(validator)

        self.input_tp = QLineEdit()
        design_layout.addWidget(QLabel("Длительность разгона до максимальной скорости, с"))
        design_layout.addWidget(self.input_tp)
        self.input_tp.setText("0.35")
        self.input_tp.setValidator(validator)

        self.input_tp_rel = QLineEdit()
        design_layout.addWidget(QLabel("Относительная длительность 'переброски' в рабочем цикле (0...1)"))
        design_layout.addWidget(self.input_tp_rel)
        self.input_tp_rel.setText("0.05")
        self.input_tp_rel.setValidator(validator)

        self.input_max_stat_torque = QLineEdit()
        design_layout.addWidget(QLabel("Максимальный внешний момент, Нм"))
        design_layout.addWidget(self.input_max_stat_torque)
        self.input_max_stat_torque.setText("15.2")
        #self.input_max_stat_torque.setText("84.86")
        self.input_max_stat_torque.setValidator(validator)

        self.input_eq_torque_intertia = QLineEdit()
        design_layout.addWidget(QLabel("Максимальный момент инерции, кг*м²"))
        design_layout.addWidget(self.input_eq_torque_intertia)
        self.input_eq_torque_intertia.setText("0.408")
        #self.input_eq_torque_intertia.setText("4.607")
        self.input_eq_torque_intertia.setValidator(validator)

        design_group.setLayout(design_layout)
        layout.addWidget(design_group)
        
        # --------------- Требования к системе управления ---------------
        control_group = QGroupBox("Требования к системе управления")
        control_layout = QVBoxLayout()

        self.input_max_error = QLineEdit()
        control_layout.addWidget(QLabel("Допустимая погрешность привода, рад"))
        control_layout.addWidget(self.input_max_error)
        self.input_max_error.setText("0.01")
        self.input_max_error.setValidator(validator)

        # --- Положение ---
        self.checkbox1 = QCheckBox("Feedforward")
        self.checkbox2 = QCheckBox("Скорректировать коэффициент")
        
        self.checkbox1.stateChanged.connect(self.onStateChangeFeedforward)
        self.checkbox2.stateChanged.connect(self.onStateChangeNonlinearCorrection)
        
        checkboxes_layout = QHBoxLayout()
        checkboxes_layout.addWidget(self.checkbox1)
        checkboxes_layout.addWidget(self.checkbox2)
        checkboxes_layout.addStretch()
        control_layout.addLayout(checkboxes_layout)

        # --- Время переходного процесса
        #row = QHBoxLayout()
        self.input_tp_control = QLineEdit()
        control_layout.addWidget(QLabel("Время переходного процесса, с"))
        control_layout.addWidget(self.input_tp_control)
        self.input_tp_control.setText("0.116")
        #self.input_tp_control.setValidator(validator)
        #control_layout.addLayout(row)

        # --- Перерегулирование
        # row = QHBoxLayout()
        # self.input_overshoot = QLineEdit()
        # row.addWidget(QLabel("Перерегулирование, %"))
        # row.addWidget(self.input_overshoot)
        # self.input_overshoot.setText("5")
        # #self.input_overshoot.setValidator(validator)
        # control_layout.addLayout(row)

        control_group.setLayout(control_layout)
        layout.addWidget(control_group)
        
        # --------------- КНОПКА ---------------
        self.button = QPushButton("Рассчитать")
        self.button.clicked.connect(self.on_click)
        layout.addWidget(self.button)

        layout.addStretch()

        self.setLayout(layout)

    def onStateChangeFeedforward(self, state):
        if state == Qt.CheckState.Checked.value:
            print("Feedforward включен")
        else:
            print("Feedforward выключен")

    def onStateChangeNonlinearCorrection(self, state):
            if state == Qt.CheckState.Checked.value:
                print("Нелинейная коррекция включена")
            else:
                print("Нелинейная коррекция выключена")


    def get_input_data(self):
        return SourceDataDriver(
            max_angl_speed=float(self.input_max_angl_speed.text() or 0),
            max_angle_speed_wm=float(self.input_max_angle_speed_wm.text() or 0),
            max_angle_acc_wm=float(self.input_max_angle_acc_wm.text() or 0),
            tp=float(float(self.input_tp.text()) or 0),
            tp_rel=float(self.input_tp_rel.text() or 0),
            max_stat_torque=float(self.input_max_stat_torque.text() or 0),
            eq_torque_intertia=float(self.input_eq_torque_intertia.text() or 0),
            max_error=float(self.input_max_error.text() or 0),
            reg_angle=1,#self.combo_box_angle.currentIndex(),
            reg_speed=0,#self.combo_box_speed.currentIndex(),
            reg_current=0,#self.combo_box_current.currentIndex(),
            non_linear_correction=self.checkbox2.isChecked(),
            feedforward=self.checkbox1.isChecked(),
            transition_time=float(self.input_tp_control.text() or 0),
            overshoot=5.#float(self.input_overshoot.text() or 0)
        )
    
    def on_click(self):
        data = self.get_input_data()
        self.data_ready.emit(data)
        return self.get_input_data()