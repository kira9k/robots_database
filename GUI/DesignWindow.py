from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDoubleValidator

class DesignWindow(QWidget):
    data_ready = Signal(dict)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Исходные данные для проектирования")
        self.resize(600, 600)
        
        layout = QVBoxLayout()
        validator = QDoubleValidator()

        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        validator.setBottom(0.0)

        self.label = QLabel("Исходные данные для проектирования", self)
        
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(self.label)
        self.setLayout(layout)
        
        # ────────────── Поля ввода ──────────────

        self.input_max_angl_speed = QLineEdit()
        layout.addWidget(QLabel("Максимальная угловая скорость, рад/с"))
        layout.addWidget(self.input_max_angl_speed)
        self.input_max_angl_speed.setText("2.491")  
        self.input_max_angl_speed.setValidator(validator)

        self.input_max_angl_acc = QLineEdit()
        layout.addWidget(QLabel("Максимальное угловое ускорение, рад/с²"))
        layout.addWidget(self.input_max_angl_acc)
        self.input_max_angl_acc.setText("7.118")
        self.input_max_angl_acc.setValidator(validator)

        self.input_max_angle_speed_wm = QLineEdit()
        layout.addWidget(QLabel("Максимальная угловая скорость рабочего движения, рад/с"))
        layout.addWidget(self.input_max_angle_speed_wm)
        self.input_max_angle_speed_wm.setText("1.245")
        self.input_max_angle_speed_wm.setValidator(validator)

        self.input_max_angle_acc_wm = QLineEdit()
        layout.addWidget(QLabel("Максимальное угловое ускорение рабочего движения, рад/с²"))
        layout.addWidget(self.input_max_angle_acc_wm)
        self.input_max_angle_acc_wm.setText("4.983")
        self.input_max_angle_acc_wm.setValidator(validator)

        self.input_tp = QLineEdit()
        layout.addWidget(QLabel("Длительность разгона до максимальной скорости, с"))
        layout.addWidget(self.input_tp)
        self.input_tp.setText("0.35")
        self.input_tp.setValidator(validator)

        self.input_tp_rel = QLineEdit()
        layout.addWidget(QLabel("Относительная длительность 'переброски' в рабочем цикле, с"))
        layout.addWidget(self.input_tp_rel)
        self.input_tp_rel.setText("0.05")
        self.input_tp_rel.setValidator(validator)

        self.input_max_stat_torque = QLineEdit()
        layout.addWidget(QLabel("Максимальный статический момент сил, Нм"))
        layout.addWidget(self.input_max_stat_torque)
        self.input_max_stat_torque.setText("84.86")
        self.input_max_stat_torque.setValidator(validator)

        self.input_max_dyn_torque = QLineEdit()
        layout.addWidget(QLabel("Максимальный динамический момент, Нм"))
        layout.addWidget(self.input_max_dyn_torque)
        self.input_max_dyn_torque.setText("23.23")
        self.input_max_dyn_torque.setValidator(validator)

        self.input_eq_torque_intertia = QLineEdit()
        layout.addWidget(QLabel("Эквивалентный момент инерции, кг*м²"))
        layout.addWidget(self.input_eq_torque_intertia)
        self.input_eq_torque_intertia.setText("4.61")
        self.input_eq_torque_intertia.setValidator(validator)

        self.input_max_error = QLineEdit()
        layout.addWidget(QLabel("Допускаемая погрешность привода, рад"))
        layout.addWidget(self.input_max_error)
        self.input_max_error.setText("0.01")
        self.input_max_error.setValidator(validator)
        
        # ────────────── КНОПКА ──────────────

        self.button = QPushButton("Рассчитать")
        self.button.clicked.connect(self.on_click)
        layout.addWidget(self.button)

        layout.addStretch()

        # Применяем layout к окну
        self.setLayout(layout)
    
    def get_input_data(self):
        input_data = {
            "max_angl_speed": self.input_max_angl_speed.text(),
            "max_angl_acc": self.input_max_angl_acc.text(),
            "max_angle_speed_wm": self.input_max_angle_speed_wm.text(),
            "max_angle_acc_wm": self.input_max_angle_acc_wm.text(),
            "tp": self.input_tp.text(),
            "tp_rel": self.input_tp_rel.text(),
            "max_stat_torque": self.input_max_stat_torque.text(),
            "max_dyn_torque": self.input_max_dyn_torque.text(),
            "eq_torque_intertia": self.input_eq_torque_intertia.text(),
            "max_error": self.input_max_error.text()
        }
        return input_data
    
    def on_click(self):
        data = self.get_input_data()
        self.data_ready.emit(data)
        return self.get_input_data()