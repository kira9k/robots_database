from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QLineEdit
from PySide6.QtCore import Qt

class DesignWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Исходные данные для проектирования")
        self.resize(600, 600)
        
        layout = QVBoxLayout()
        
        self.label = QLabel("Исходные данные для проектирования", self)
        
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)


        layout.addWidget(self.label)
        self.setLayout(layout)
        
# ────────────── Примеры полей ввода ──────────────

        self.max_angl_speed = QLineEdit()
        layout.addWidget(QLabel("Максимальная угловая скорость, рад/с"))
        layout.addWidget(self.max_angl_speed)

        self.input_max_angl_acc = QLineEdit()
        layout.addWidget(QLabel("Максимальное угловое ускорение, рад/с²"))
        layout.addWidget(self.input_max_angl_acc)

        self.max_angle_speed_wm = QLineEdit()
        layout.addWidget(QLabel("Максимальная угловая скорость рабочего движения, рад/с"))
        layout.addWidget(self.max_angle_speed_wm)

        self.max_angle_acc_wm = QLineEdit()
        layout.addWidget(QLabel("Максимальное угловое ускорение рабочего движения, рад/с²"))
        layout.addWidget(self.max_angle_acc_wm)

        self.tp = QLineEdit()
        layout.addWidget(QLabel("Длительность разгона до максимальной скорости, с"))
        layout.addWidget(self.tp)

        self.tp_rel = QLineEdit()
        layout.addWidget(QLabel("Относительная длительность 'переброски' в рабочем цикле, с"))
        layout.addWidget(self.tp_rel)

        self.max_stat_torque = QLineEdit()
        layout.addWidget(QLabel("Максимальный статический момент сил, Нм"))
        layout.addWidget(self.max_stat_torque)

        self.max_dyn_torque = QLineEdit()
        layout.addWidget(QLabel("Максимальный динамический момент, Нм"))
        layout.addWidget(self.max_dyn_torque)

        self.eq_torque_intertia = QLineEdit()
        layout.addWidget(QLabel("Эквивалентный момент инерции, кг*м²"))
        layout.addWidget(self.eq_torque_intertia)

        self.max_error = QLineEdit()
        layout.addWidget(QLabel("Допускаемая погрешность привода, рад"))
        layout.addWidget(self.max_error)
        # Пустое пространство внизу (чтобы поля не прилипали к низу)
        layout.addStretch()

        # Применяем layout к окну
        self.setLayout(layout)