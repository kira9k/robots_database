import math
import os 

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from DataBase.ORMModel import Result, SourceData, CoefRegulators, Utils
from DataBase.repository import DatabaseRepository
from GUI import html_func


class ResultWindow(QWidget):
    """Окно для отображения результатов расчёта и сохранения их в базу данных"""
    def __init__(self, results: dict, motor=None, gear_ratio=None, parent=None, source_data=None, gear=None, recalc_results=None, orms_results=None, thermal_data=None, error=None, enc_min=None, closest_encoder=None, coef_regulators=None, utils=None):
        super().__init__(parent)
        self.setWindowTitle("Результаты расчёта")
        self.resize(600, 400)
        self.setWindowFlag(Qt.Window, True)
        
        self.source_data = source_data
        self.gear_ratio = gear_ratio
        self.results = results
        self.motor = motor
        self.gear = gear
        self.error = error
        self.enc_min = enc_min
        self.closest_encoder = closest_encoder
        self.coef_regulators = coef_regulators
        self.utils = utils
        self.recalc_results = recalc_results
        self.orms_results = orms_results
        self.thermal_data = thermal_data

        layout = QVBoxLayout(self)
        self.text = QTextEdit(self)        
        self.text.setReadOnly(True)
        self.text.setStyleSheet("""
            QTextEdit {
                font-size: 10pt;
                }
            """)
        
        # Формирование HTML для отображения результатов
        html = html_func.html_source_data(self.source_data)
        html += html_func.html_calculation_results(self.source_data, self.results)
        html += html_func.html_found_motor(self.motor)
        html += html_func.html_optimal_gear_ratio(self.results, self.source_data, self.motor, self.gear_ratio)
        html += html_func.html_found_gear(self.gear)
        html += html_func.html_check_motor(self.source_data, self.results, self.gear, self.motor, self.recalc_results)
        html += html_func.html_orms(self.motor, self.source_data, self.gear, self.orms_results)
        html += html_func.html_thermal_calc(self.source_data, self.orms_results, self.thermal_data, self.motor, self.gear)
        html += html_func.html_encoder_calc(self.source_data, self.error, self.gear)
        html += html_func.html_found_encoder(self.closest_encoder, self.error, self.gear, self.enc_min)
        html += html_func.html_coef_regulators(self.coef_regulators)
        html += html_func.html_matlab_test()

        self.text.setHtml(html)
        layout.addWidget(self.text)
        
        # Кнопки для сохранения результатов и закрытия окна
        btn_close = QPushButton("Закрыть")
        btn_save = QPushButton("Сохранить результаты в базу данных")
        
        btn_close.clicked.connect(self.close)
        btn_save.clicked.connect(self.save_results)
        
        layout.addWidget(btn_close)
        layout.addWidget(btn_save)
    
    # def _html_calculation_results(self):
    #     html = "<h2>Расчетные результаты</h2>"
    #     html += f"""
    #             <h3>Максимальный момент</h3>
    #             <p>M<sub>макс</sub> = M<sub>ст</sub> + M<sub>дин</sub> = 
    #             {getattr(self.source_data, 'max_stat_torque', 0)} + {getattr(self.source_data, 'max_dyn_torque', 0)} = 
    #             {self.results.get('torque', 0):.2f} Нм</p>
    #             """
    #     html += f"""
    #             <h3>Максимальная мощность</h3>
    #             <p>P<sub>макс</sub> = M<sub>макс</sub> * ω<sub>макс</sub> = 
    #             {self.results.get('torque', 0):.2f} * {getattr(self.source_data, 'max_angl_speed', 0):.2f} = {self.results.get('original_power', 0):.2f} Вт</p>
    #     """
    #     return html
    
    # def _html_required_power(self):
    #     html = f"""
    #             <h3>Требуемая мощность с двигателя</h3>
    #             <p>P<sub>треб</sub> = P<sub>макс</sub> * (2,5...3) = 
    #             {self.results.get('original_power', 0):.2f} * {self.results.get('power_margin', 0):.2f} = 
    #             {self.results.get('power', 0):.2f} Вт</p>
    #             """
    #     return html
    
    # def _html_optimal_gear_ratio(self):
    #     html = f"""<h3>Оптимальное передаточное отношение</h3>
    #                     <p>i<sub>opt</sub> = 
    #                     √(P<sub>макс</sub> / (J<sub>дв</sub> * ω<sub>макс</sub> * a<sub>макс</sub>)) =
    #                     √({self.results.get('original_power', 0):.2f} / ({getattr(self.motor, 'J', ''):.7f} * {getattr(self.source_data, 'max_angl_speed', 0):.2f} * {getattr(self.source_data, 'max_angl_acc', 0):.2f})) = 
    #                     {self.gear_ratio:.2f}</p>
    #                 """
    #     return html
    
    
    # def _html_check_motor(self):
    #     html = "<h3>Проверка правильности выбора двигателя</h3>"
    #     html += f"""Проверка по моменту:<br>
    #                 M<sub>треб</sub> = M<sub>макс</sub> / (η * i<sub>р</sub>) = 
    #                 {self.results.get('torque', 0):.2f} / ({self.gear.efficiency:.2f} * {self.gear.i_nom:.2f}) = 
    #                 {self.recalc_results.get('required_torque_with_gear', 0):.2f} Нм &le; M<sub>ном</sub> = {getattr(self.motor, 'torque_nom', '')} Нм<br><br>
    #     """
    #     html += f"""Проверка по частоте вращения:<br>
    #                 ω<sub>треб</sub> = ω<sub>макс</sub> * i<sub>р</sub> = 
    #                 {getattr(self.source_data, 'max_angl_speed', 0):.2f} * {self.gear.i_nom:.2f} = 
    #                 {self.recalc_results.get('required_speed_with_gear', 0):.2f} рад/с &le; ω<sub>ном</sub> = {getattr(self.motor, 'n_nom', 0) * math.pi / 30:.2f} рад/с<br>
    #             """
    #     return html
    
    # def _html_orms(self):
    #     html = f"""<h3>Построение области располагаемых моментов и скоростей и приведенной диаграммы нагрузки привода</h3>"""
    #     html += f"""J<sub>сум</sub> = J<sub>дв</sub> + J<sub>экв.прив</sub> = 
    #             J<sub>дв</sub> + J<sub>экв</sub> / (i<sub>р</sub><sup>2</sup> * η) = 
    #             {getattr(self.motor, 'J', ''):.5f} + {getattr(self.source_data, 'eq_torque_intertia', 0):.5f} / ({self.gear.i_nom}<sup>2</sup> * {self.gear.efficiency}) =
    #             {self.orms_results.get('j_sum', 0):.7f} кг·м²<br>
    #             a<sub>дв.макс</sub> = i<sub>р</sub> * a<sub>макс</sub> = 
    #             {self.gear.i_nom} * {getattr(self.source_data, 'max_angl_acc', 0):.2f} =
    #             {self.orms_results.get('acceleration_engine_with_gear', 0):.2f} рад/с²<br>
    #             M<sub>ст.прив</sub> = M<sub>ст</sub> / (i<sub>р</sub> * η) = 
    #             {getattr(self.source_data, 'max_stat_torque', 0):.2f} / {self.gear.i_nom} * {self.gear.efficiency}) =
    #             {self.orms_results.get('torque_stat_gear', 0):.2f} Нм<br>
    #             M<sub>дин.прив</sub> = J<sub>сум</sub> * a<sub>дв.макс</sub> = 
    #             {self.orms_results.get('j_sum', 0):.7f} * {self.orms_results.get('acceleration_engine_with_gear', 0):.2f} =
    #             {self.orms_results.get('torque_dyn_gear', 0):.2f} Нм<br>
    #             M<sub>разог</sub> = M<sub>ст.прив</sub> + M<sub>дин.прив</sub> = 
    #             {self.orms_results.get('torque_stat_gear', 0):.2f} + {self.orms_results.get('torque_dyn_gear', 0):.2f} = 
    #             {self.orms_results.get('torque_start', 0):.2f} Нм <br>
    #             M<sub>торможение</sub> = M<sub>ст.прив</sub> - M<sub>дин.прив</sub> = 
    #             {self.orms_results.get('torque_stat_gear', 0):.2f} - {self.orms_results.get('torque_dyn_gear', 0):.2f} = 
    #             {self.orms_results.get('torque_stop', 0):.2f} Нм<br>
    #             k<sub>e</sub> = (U<sub>я</sub> - I<sub>я</sub> * R<sub>я</sub>) / (n<sub>ном</sub> * π / 30) =
    #             ({getattr(self.motor, 'U_nom', 0):.2f} - {getattr(self.motor, 'I_nom', 0):.2f} * {getattr(self.motor, 'R', 0):.2f}) / ({getattr(self.motor, 'n_nom', 0) * math.pi / 30:.2f}) =
    #             {self.orms_results.get('emf_coef', 0):.2f} В * c/рад<br>
    #             ω<sub>д.хх</sub> = U<sub>я</sub> / k<sub>e</sub> = 
    #             {getattr(self.motor, 'U_nom', 0):.2f} / {self.orms_results.get('emf_coef', 0):.2f} =
    #             {self.orms_results.get('idle_speed', 0):.2f} рад/с</p>
    #             <h4>Коэффициент форсирования</h4>
    #                 <p>λ = M<sub>макс</sub> / M<sub>ном</sub><br> 
    #                 λ = {self.orms_results.get('torque_start', 0):.2f} / {getattr(self.motor, 'torque_nom', '')} = 
    #                 {self.orms_results.get('torque_start', 0) / getattr(self.motor, 'torque_nom', 1):.2f}<br>
    #                 Принимаем λ = {self.orms_results.get('coef_forcing', 0):.2f}</p>
    #             <p>Приведенная диаграмма нагрузки и ОРМС представлены ниже и содержит следующие характерные точки:<br>
    #             - M<sub>ст.прив</sub> = {self.orms_results.get('torque_stat_gear', 0):.2f} Нм<br>
    #             - M<sub>дин.прив</sub> = {self.orms_results.get('torque_dyn_gear', 0):.2f} Нм<br>
    #             - M<sub>разгон</sub> = {self.orms_results.get('torque_start', 0):.2f} Нм<br>
    #             - M<sub>торможение</sub> = {self.orms_results.get('torque_stop', 0):.2f} Нм<br>
    #             - ω<sub>д.хх</sub> = {self.orms_results.get('idle_speed', 0):.2f} рад/с<br>
    #             - ω<sub>ном</sub> = {getattr(self.motor, 'n_nom', 0) * math.pi / 30:.2f} рад/с<br>
    #             - ω<sub>треб</sub> = {self.recalc_results.get('required_speed_with_gear', 0):.2f} рад/с<br>
    #             - M<sub>ном</sub> * λ = {self.orms_results.get('torque_nom_with_coef', 0):.2f} Нм<br></p>
    #             """
    #     html += f"""График приведенной диаграммы нагрузки и ОРМС представлен ниже:<br>"""
    #     html += f"""<img src="{os.path.join(os.getcwd(), 'image_graphic', 'chart.png')}"></p><br>"""
    #     return html
    
    # def _html_thermal_calc(self):
    #     html = f"""<h3>Тепловой расчет</h3>"""
    #     html += f"""<h4>Метод эквивалентного момента</h4>"""
    #     html += f"""<p>Условие выполнения: M<sub>дв.экв</sub><sup>2</sup> &le; M<sub>ном</sub><sup>2</sup><br>
    #             M<sub>дв.экв</sub><sup>2</sup> = 1/t<sub>ц</sub>(∫<sub>0</sub><sup>t<sub>ц</sub></sup> M<sub>дв</sub><sup>2</sup>(t) dt)<br>
    #             t<sub>ц</sub> = (t<sub>разг</sub> + t<sub>торм</sub>) / T<sub>пер.отн</sub> = 
    #             {getattr(self.source_data, 'tp', 0)} + {getattr(self.source_data, 'tp', 0)} / {getattr(self.source_data, 'tp_rel', 0)} = 
    #             {self.thermal_data.get('t_cycle', 0):.2f} с<br>
    #             t<sub>сл</sub> = t<sub>ц</sub> * (1 - T<sub>пер.отн</sub>) = 
    #             {self.thermal_data.get('t_cycle', 0):.2f} * (1 - {getattr(self.source_data, 'tp_rel', 0)}) =
    #             {self.thermal_data.get('t_s', 0):.2f} с<br>
    #             A<sub>экв</sub> = (ω<sub>макс.раб</sub><sup>2</sup>) / a<sub>макс.раб</sub> = 
    #             ({getattr(self.source_data, 'max_angle_speed_wm', 0):.2f}<sup>2</sup>) / {getattr(self.source_data, 'max_angle_acc_wm', 0):.2f} =
    #             {self.thermal_data.get('A_eqv', 0):.2f}<br>
    #             ω<sub>экв</sub> = a<sub>макс.раб</sub> / ω<sub>макс.раб</sub> = 
    #             {getattr(self.source_data, 'max_angle_acc_wm', 0):.2f} / {getattr(self.source_data, 'max_angle_speed_wm', 0):.2f} = 
    #             {self.thermal_data.get('omega_eqv', 0):.2f} рад/с<br>
    #             M<sub>сл</sub> = M<sub>ст1</sub> + M<sub>дин1</sub> = 
    #             M<sub>ст</sub> / (i<sub>р</sub> * η) + (J<sub>сум</sub> * A<sub>экв</sub> * ω<sub>экв</sub><sup>2</sup>) = 
    #             {getattr(self.source_data, 'max_stat_torque', 0):.2f} / ({self.gear.i_nom} * {self.gear.efficiency}) + 
    #             ({self.orms_results.get('j_sum', 0):.7f} * {self.thermal_data.get('A_eqv', 0):.2f} * {self.thermal_data.get('omega_eqv', 0):.2f}<sup>2</sup>) =
    #             {self.thermal_data.get('M_c', 0):.2f} Нм<br>
    #             M<sub>дв.экв</sub><sup>2</sup> = 1/t<sub>ц</sub>(M<sub>разгон</sub><sup>2</sup> * t<sub>разг</sub> + M<sub>торм</sub><sup>2</sup> * t<sub>торм</sub> + M<sub>сл</sub><sup>2</sup> * t<sub>сл</sub>) =
    #             1/{self.thermal_data.get('t_cycle', 0):.2f} * ({self.orms_results.get('torque_start', 0):.2f}<sup>2</sup> * {getattr(self.source_data, 'tp', 0):.2f} + 
    #             {self.orms_results.get('torque_stop', 0):.2f}<sup>2</sup> * {getattr(self.source_data, 'tp', 0):.2f} + 
    #             {self.thermal_data.get('M_c', 0):.2f}<sup>2</sup> * {self.thermal_data.get('t_s', 0):.2f}) = 
    #             {self.thermal_data.get('M_eqv_square', 0):.2f} Нм<br>
    #             Таким образом,<br>
    #             M<sub>дв.экв</sub><sup>2</sup> = {self.thermal_data.get('M_eqv_square', 0):.2f} Нм &le; M<sub>ном</sub><sup>2</sup> = {getattr(self.motor, 'torque_nom', 0)**2:.2f} Нм<br>
    #             """
    #     return html
    
    # def _html_encoder_calc(self):
    #     html = f"""<h3>Расчет параметров энкодера</h3>"""
    #     html += f"""<h4>Анализ точности привода</h4>"""
    #     html += f"""<p>Условие выполнения:<br>
    #             δ<sub>доп</sub> &ge; δ<sub>макс</sub> <br>
    #             δ<sub>макс</sub> = δ<sub>1</sub> + δ<sub>2</sub> + δ<sub>3</sub> + δ<sub>4</sub> + δ<sub>5</sub> = 
    #             M<sub>вн.макс</sub>/C + σ/2 + Δ<sub>датч</sub> + δ<sub>д.дин</sub> + δ<sub>д.м</sub> <br>
    #             Будем считать, что система управления манипулятором обеспечивает вычисление моментов нагрузки и формирование корректирующих воздействий, 
    #             которые на 95% компенсируют погрешность привода, обусловленную упругой податливостью редуктора <br>
    #             δ<sub>1.доп</sub> = 0.05 * {getattr(self.source_data, 'max_stat_torque', 0):.2f} / {self.gear.c:.2f} = {getattr(self.error, 'first_error', 0):.8f} рад<br>
    #             δ<sub>2.доп</sub> = σ/2 = {self.gear.clearance:.8f}/2 = {getattr(self.error, 'second_error', 0):.8f} рад<br>
    #             Считаем, что внешний момент изменяется настолько медленно, что динамическая ошибка, вызванная изменением момента, также равна нулю<br>
    #             δ<sub>5.доп</sub> = 0 рад<br>
    #             δ<sub>3.доп</sub> + δ<sub>4.доп</sub> = δ<sub>доп</sub> - δ<sub>1.доп</sub> - δ<sub>2.доп</sub> - δ<sub>5.доп</sub> = 
    #             {getattr(self.source_data, 'max_error', 0):.2f} - {getattr(self.error, 'first_error', 0):.8f} - {getattr(self.error, 'second_error', 0):.8f} - 0 =
    #             {getattr(self.error, 'third_fourth_error', 0):.8f} рад<br>
    #             Из соображений обеспечения точности привода целесообразно принять δ<sub>3.доп</sub> &lt; &lt; δ<sub>4.доп</sub> <br>
    #             δ<sub>3.доп</sub>= 0.05 * δ<sub>4.доп</sub><br>
    #             δ<sub>3.доп</sub> = {getattr(self.error, 'third_error', 0):.8f} рад<br>
    #             δ<sub>4.доп</sub> = {getattr(self.error, 'fourth_error', 0):.8f} рад<br>
    #             """
    #     return html
    
    # def _html_found_encoder(self):
    #     html= f"""<h4>Подбор энкодера</h4>"""
    #     html += f"""<p>Условие выполнения:<br>
    #             Δ<sub>датч</sub> = 2π / (N<sub>датч</sub> * 4) &le; δ<sub>3.доп</sub> * i<sub>ред</sub><br>
    #             N<sub>имп.треб</sub> &ge; π / (2 * δ<sub>3.доп</sub> * i<sub>ред</sub>) = π / (2 * {getattr(self.error, 'third_error', 0):.8f} * {self.gear.i_nom:.2f}) = {self.enc_min} дискрет/об<br>
    #              <h4>Выбранный энкодер</h4>
    #     """
    #     return html

    def save_results(self):
        """Сохранение результатов проектирования в базу данных"""
        try:
            # Проверяем наличие всех необходимых данных
            if not self.motor:
                QMessageBox.warning(self, "Ошибка", "Не найден двигатель")
                return
            if not self.gear:
                QMessageBox.warning(self, "Ошибка", "Не найден редуктор")
                return
            if not self.closest_encoder:
                QMessageBox.warning(self, "Ошибка", "Не найден энкодер")
                return
            
            repo = DatabaseRepository()
            duplicates = []  # Список для сохранения информации о найденных дубликатах
            
            # ===== Проверяем и сохраняем исходные данные (SourceData) =====
            id_source_data = None
            if self.source_data:
                source_data_dict = {
                    'max_speed': getattr(self.source_data, 'max_angl_speed', 0),
                    'max_acc': getattr(self.source_data, 'max_angle_acc_wm', 0),
                    'max_speed_work': getattr(self.source_data, 'max_angle_speed_wm', 0),
                    'acc_duration': getattr(self.source_data, 'tp', 0),
                    'rel_duration': getattr(self.source_data, 'tp_rel', 0),
                    'max_torque': getattr(self.source_data, 'max_stat_torque', 0),
                    'max_inertia_torque': getattr(self.source_data, 'eq_torque_intertia', 0),
                    'max_error': getattr(self.source_data, 'max_error', 0),
                    'overshoot': getattr(self.source_data, 'overshoot', 0),
                    'transition_time': getattr(self.source_data, 'transition_time', 0)
                }
                print(f"DEBUG: Ищем SourceData: {source_data_dict}")
                # Проверяем наличие дубликата
                duplicate_id = repo.find_duplicate(SourceData, source_data_dict)
                if duplicate_id:
                    print(f"DEBUG: Найден дубликат SourceData с ID {duplicate_id}")
                    duplicates.append(f"Исходные данные (ID: {duplicate_id})")
                    id_source_data = duplicate_id
                else:
                    print(f"DEBUG: Дубликат SourceData не найден, добавляем новую запись")
                    id_source_data = repo.add(SourceData, source_data_dict)
            
            # ===== Проверяем и сохраняем коэффициенты регуляторов (CoefRegulators) =====
            id_coef_regulators = None
            if self.coef_regulators:
                coef_dict = {
                    'k_a': getattr(self.coef_regulators, 'k_a', 0),
                    'k_ai': getattr(self.coef_regulators, 'k_ai', 0),
                    'k_c': getattr(self.coef_regulators, 'k_c', 0),
                    'k_dc': getattr(self.coef_regulators, 'k_dc', 0),
                    'k_ci': getattr(self.coef_regulators, 'k_ci', 0),
                    'k_ds': getattr(self.coef_regulators, 'k_ds', 0),
                    'k_s': getattr(self.coef_regulators, 'k_s', 0),
                    'k_si': getattr(self.coef_regulators, 'k_si', 0),
                    'k_pwm': getattr(self.coef_regulators, 'k_pwm', 0),
                    'T_pwm': getattr(self.coef_regulators, 'T_pwm', 0),
                    'k_feedforward': getattr(self.coef_regulators, 'k_feedforward', 0),
                }
                # Проверяем наличие дубликата
                duplicate_id = repo.find_duplicate(CoefRegulators, coef_dict)
                if duplicate_id:
                    duplicates.append(f"Коэффициенты регуляторов (ID: {duplicate_id})")
                    id_coef_regulators = duplicate_id
                else:
                    id_coef_regulators = repo.add(CoefRegulators, coef_dict)

            # ===== Проверяем и сохраняем вспомогательные данные (Utils) =====
            id_utils = None
            if self.utils:
                utils_dict = {
                    'A_e': getattr(self.utils, 'A_e', 0),
                    'omega_e': getattr(self.utils, 'omega_e', 0),
                    'dyn_error': getattr(self.utils, 'dyn_error', 0),
                    'stat_error': getattr(self.utils, 'stat_error', 0)
                }
                # Проверяем наличие дубликата
                duplicate_id = repo.find_duplicate(Utils, utils_dict)
                if duplicate_id:
                    duplicates.append(f"Вспомогательные данные (ID: {duplicate_id})")
                    id_utils = duplicate_id
                else:
                    id_utils = repo.add(Utils, utils_dict)

            # ===== Получаем ID компонентов =====
            if isinstance(self.motor, dict):
                id_engine = self.motor.get('id')
            else:
                id_engine = getattr(self.motor, 'id', None)
                
            if isinstance(self.gear, dict):
                id_gear = self.gear.get('id')
            else:
                id_gear = getattr(self.gear, 'id', None)
                
            if isinstance(self.closest_encoder, dict):
                id_encoder = self.closest_encoder.get('id')
            else:
                id_encoder = getattr(self.closest_encoder, 'id', None)
            
            # Проверяем наличие ID компонентов
            if not id_engine or not id_gear or not id_encoder:
                QMessageBox.warning(self, "Ошибка", "Не удалось получить ID компонентов")
                return
            
            # ===== Сохраняем результат =====
            result_data = {
                'id_engine': id_engine,
                'id_gear': id_gear,
                'id_encoder': id_encoder,
                'id_source_data': id_source_data,
                'id_coef_regulators': id_coef_regulators,
                'id_utils': id_utils
            }

            duplicate_id_result = repo.find_duplicate(Result, result_data)
            if duplicate_id_result:
                duplicates.append(f"Результат (ID: {duplicate_id_result})")
                print(f"DEBUG: Найден дубликат Result с ID {duplicate_id_result}, не добавляем новую запись")
            
            else:
                repo.add(Result, result_data)
            
            # Формируем сообщение с информацией о сохранении
            if duplicate_id_result:
                message = f"Результат уже существует в базе данных (ID: {duplicate_id_result}) и не был добавлен повторно."
                QMessageBox.warning(self, "Результат уже существует", message)

            elif duplicates:
                message = "Результаты сохранены в базу данных\n\n Найдены существующие записи:\n"
                message += "\n".join(duplicates)
                QMessageBox.warning(self, "Результаты сохранены с предупреждением", message)
            else:
                message = (
                    f"Результаты сохранены в базу данных:\n"
                    f"- Исходные данные (ID: {id_source_data})\n"
                    f"- Коэффициенты регуляторов (ID: {id_coef_regulators})\n"
                    f"- Вспомогательные данные (ID: {id_utils})"
                )
                QMessageBox.information(self, "Успех", message)
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении: {str(e)}")
    
    