import math
import os 

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
from PySide6.QtCore import Qt
from Graphics.PlotGivenLoadDiagram import PlotLoadDiagram
from GUI.ShowGraphic import MplCanvas
from utils.SourData import DataGear

class ResultWindow(QWidget):
    def __init__(self, results: dict, motor=None, gear_ratio=None, parent=None, source_data=None, gear=None, recalc_results=None, orms_results=None, thermal_data=None):
        super().__init__(parent)
        self.setWindowTitle("Результаты расчёта")
        self.resize(600, 400)
        self.setWindowFlag(Qt.Window, True)
        
        self.canvas = MplCanvas()
        self.source_data = source_data
        self.gear_ratio = gear_ratio
        self.results = results
        self.motor = motor
        self.gear = gear
        
        self.recalc_results = recalc_results
        self.orms_results = orms_results
        self.thermal_data = thermal_data

        layout = QVBoxLayout(self)
        self.text = QTextEdit(self)        
        self.text.setReadOnly(True)
        
        html = self._html_source_data()
        html += self._html_calculation_results()
        html += self._html_found_motor()
        html += self._html_optimal_gear_ratio()
        html += self._html_found_gear()
        html += self._html_check_motor()
        html += self._html_orms()
        html += self._html_thermal_calc()
        
        # self.gear_data = DataGear(
        #         name=gear["gear_name"],
        #         i_nom=gear["i"],
        #         m=gear["mass"],
        #         kpd=gear["efficiency"],
        #         c =gear["c"],
        #         clearance =gear["clearance"],
        #         speed_norm =gear["speed_norm"],
        #         torque_nom =gear["torque_nom"]
        #         )


        

        
        html += "<h2>Результаты расчёта</h2>"
        html += f"<p><b>Требуемая мощность:</b> {self.results.get('power', 0):.2f} Вт<br>"
        html += f"<b>Требуемый момент:</b> {self.results.get('torque', 0):.2f} Нм</p>"

        

      
        
        self.text.setHtml(html)
        layout.addWidget(self.text)
        
        btn_close = QPushButton("Закрыть")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)
    
    def _html_source_data(self):
        html = "<h2>Исходные данные для проектирования</h2>"
        html += f"<p><b>Макс. угловая скорость:</b> {getattr(self.source_data, 'max_angl_speed', 0):.2f} рад/с<br>"
        html += f"<b>Макс. угловое ускорение:</b> {getattr(self.source_data, 'max_angl_acc', 0):.2f} рад/с²<br>"
        html += f"<b>Макс. угловая скорость рабочего движения:</b> {getattr(self.source_data, 'max_angle_speed_wm', 0):.2f} рад/с<br>"
        html += f"<b>Макс. угловое ускорение рабочего движения:</b> {getattr(self.source_data, 'max_angle_acc_wm', 0):.2f} рад/с²<br>"
        html += f"<b>Длительность разгона до макс. скорости:</b> {getattr(self.source_data, 'tp', 0):.2f} с<br>"
        html += f"<b>Относительная длительность 'переброски' в рабочем цикле:</b> {getattr(self.source_data, 'tp_rel', 0):.2f} с<br>"
        html += f"<b>Макс. статический момент сил:</b> {getattr(self.source_data, 'max_stat_torque', 0):.2f} Нм<br>"
        html += f"<b>Макс. динамический момент сил:</b> {getattr(self.source_data, 'max_dyn_torque', 0):.2f} Нм<br>"
        html += f"<b>Эквивалентный момент инерции:</b> {getattr(self.source_data, 'eq_torque_intertia', 0):.2f} кг·м²<br>"
        html += f"<b>Макс. допустимая ошибка:</b> {getattr(self.source_data, 'max_error', 0):.2f} рад</p>"
        return html
    
    def _html_calculation_results(self):
        html = "<h2>Расчетные результаты</h2>"
        html += f"""
                <h3>Максимальный момент</h3>
                <p>M<sub>макс</sub> = M<sub>ст</sub> + M<sub>дин</sub> = 
                {getattr(self.source_data, 'max_stat_torque', 0)} + {getattr(self.source_data, 'max_dyn_torque', 0)} = 
                {self.results.get('torque', 0):.2f} Нм</p>
                """
        html += f"""
                <h3>Максимальная мощность</h3>
                <p>P<sub>макс</sub> = M<sub>макс</sub> * ω<sub>макс</sub> = 
                {self.results.get('torque', 0):.2f} * {getattr(self.source_data, 'max_angl_speed', 0):.2f} = {self.results.get('original_power', 0):.2f} Вт</p>
        """
        return html
    
    def _html_required_power(self):
        html += f"""
                <h3>Требуемая мощность с двигателя</h3>
                <p>P<sub>треб</sub> = P<sub>макс</sub> * (2,5...3) = 
                {self.results.get('original_power', 0):.2f} * {self.results.get('power_margin', 0):.2f} = 
                {self.results.get('power', 0):.2f} Вт</p>
                """
        return html
    
    def _html_found_motor(self):
        if self.motor:
            html = "<h3>Найденный двигатель</h3>"
            html += f"<p><b>Модель:</b> {getattr(self.motor, 'name', '')}<br>"
            html += f"<b>Номинальная мощность:</b> {getattr(self.motor, 'p_nom', '')} Вт<br>"
            html += f"<b>Номинальный момент:</b> {getattr(self.motor, 'torque_nom', '')} Нм</p>"
        else:
            pass
        return html
    
    def _html_optimal_gear_ratio(self):
        html = ""
        if self.gear_ratio is not None:
            html += f"""<h3>Оптимальное передаточное отношение</h3>
                        <p>i<sub>opt</sub> = 
                        √(P<sub>треб</sub> / (J<sub>дв</sub> * ω<sub>макс</sub> * a<sub>макс</sub>)) =
                        √({self.results.get('power', 0):.2f} / ({getattr(self.motor, 'J', ''):.7f} * {getattr(self.source_data, 'max_angl_speed', 0):.2f} * {getattr(self.source_data, 'max_angl_acc', 0):.2f})) = 
                        {self.gear_ratio:.2f}</p>
                    """
        return html
    
    def _html_found_gear(self):
        html = ""
        if self.gear:
            html += "<h3>Найденный редуктор</h3>"
            html += f"<p><b>Модель:</b> {self.gear.get('gear_name', '')}<br>"
            html += f"<b>Передаточное отношение:</b> {self.gear.get('i', '')}<br>"
            html += f"<b>КПД:</b> {self.gear.get('efficiency', '')}<br>"
            html += f"<b>Номинальная скорость вращения на входном валу:</b> {self.gear.get('speed_norm', '')} об/мин<br>"
            html += f"<b>Макс. момент на выходном валу:</b> {self.gear.get('torque_nom', '')} Нм<br></p>"
        return html
    
    def _html_check_motor(self):
        html = "<h3>Проверка правильности выбора двигателя</h3>"
        html += f"""Проверка по моменту:<br>
                    M<sub>треб</sub> = M<sub>макс</sub> / η = 
                    {self.results.get('torque', 0):.2f} / {getattr(self.gear, 'efficiency', 0):.2f} = 
                    {self.recalc_results.get('required_torque_with_gear', 0):.2f} Нм &le; M<sub>ном</sub> = {getattr(self.motor, 'torque_nom', '')} Нм<br><br>
        """
        html += f"""Проверка по частоте вращения:<br>
                    ω<sub>треб</sub> = ω<sub>макс</sub> * i<sub>р</sub> = 
                    {getattr(self.source_data, 'max_angl_speed', 0):.2f} * {getattr(self.gear, 'i', 0):.2f} = 
                    {self.recalc_results.get('required_speed_with_gear', 0):.2f} рад/с &le; ω<sub>ном</sub> = {getattr(self.motor, 'n_nom', 0) * math.pi / 30:.2f} рад/с<br>
                """
        return html
    
    def _html_orms(self):
        html = f"""<h3>Построение области располагаемых моментов и скоростей и преведенной диаграммы нагрузки привода</h3>"""
        html += f"""J<sub>сум</sub> = J<sub>дв</sub> + J<sub>экв.прив</sub> = 
                J<sub>дв</sub> + J<sub>экв</sub> / (i<sub>р</sub><sup>2</sup> * η) = 
                {getattr(self.motor, 'J', ''):.5f} + {getattr(self.source_data, 'eq_torque_intertia', 0):.5f} / ({getattr(self.gear, 'i', '')}<sup>2</sup> * {getattr(self.gear, 'efficiency', '')}) =
                {self.orms_results.get('j_sum', 0):.7f} кг·м²<br>
                a<sub>дв.макс</sub> = i<sub>р</sub> * a<sub>макс</sub> = 
                {getattr(self.gear, 'i', '')} * {getattr(self.source_data, 'max_angl_acc', 0):.2f} =
                {self.orms_results.get('acceleration_engine_with_gear', 0):.2f} рад/с²<br>
                M<sub>ст.прив</sub> = M<sub>ст</sub> / (i<sub>р</sub> * η) = 
                {getattr(self.source_data, 'max_stat_torque', 0):.2f} / ({getattr(self.gear, 'i', '')} * {getattr(self.gear, 'efficiency', '')}) =
                {self.orms_results.get('torque_stat_gear', 0):.2f} Нм<br>
                M<sub>дин.прив</sub> = J<sub>сум</sub> * a<sub>дв.макс</sub> = 
                {self.orms_results.get('j_sum', 0):.7f} * {self.orms_results.get('acceleration_engine_with_gear', 0):.2f} =
                {self.orms_results.get('torque_dyn_gear', 0):.2f} Нм<br>
                M<sub>разог</sub> = M<sub>ст.прив</sub> + M<sub>дин.прив</sub> = 
                {self.orms_results.get('torque_stat_gear', 0):.2f} + {self.orms_results.get('torque_dyn_gear', 0):.2f} = 
                {self.orms_results.get('torque_start', 0):.2f} Нм <br>
                M<sub>торможение</sub> = M<sub>ст.прив</sub> - M<sub>дин.прив</sub> = 
                {self.orms_results.get('torque_stat_gear', 0):.2f} - {self.orms_results.get('torque_dyn_gear', 0):.2f} = 
                {self.orms_results.get('torque_stop', 0):.2f} Нм<br>
                k<sub>e</sub> = (U<sub>я</sub> - I<sub>я</sub> * R<sub>я</sub>) / (n<sub>ном</sub> * π / 30) =
                ({getattr(self.motor, 'U_nom', 0):.2f} - {getattr(self.motor, 'I_nom', 0):.2f} * {getattr(self.motor, 'R', 0):.2f}) / ({getattr(self.motor, 'n_nom', 0) * math.pi / 30:.2f}) =
                {self.orms_results.get('emf_coef', 0):.2f} В * c/рад<br>
                ω<sub>д.хх</sub> = U<sub>я</sub> * k<sub>e</sub> = 
                {getattr(self.motor, 'U_nom', 0):.2f} * {self.orms_results.get('emf_coef', 0):.2f} =
                {self.orms_results.get('idle_speed', 0):.2f} рад/с<br></p>
                <h4>Коэффициент форсирования</h4>
                    <p>λ = M<sub>треб</sub> / M<sub>ном</sub><br> 
                    λ ={self.recalc_results.get('required_torque_with_gear', 0):.2f} / {getattr(self.motor, 'torque_nom', '')} = 
                    {self.recalc_results.get('required_torque_with_gear', 0) / getattr(self.motor, 'torque_nom', 1):.2f}<br>
                    Принимаем λ = {self.orms_results.get('coef_forcing', 0):.2f}</p>
                <p>Приведенная диаграмма нагрузки и ОРМС представлены ниже и содержит следующие характерные точки:<br>
                - M<sub>ст.прив</sub> = {self.orms_results.get('torque_stat_gear', 0):.2f} Нм<br>
                - M<sub>дин.прив</sub> = {self.orms_results.get('torque_dyn_gear', 0):.2f} Нм<br>
                - M<sub>разог</sub> = {self.orms_results.get('torque_start', 0):.2f} Нм<br>
                - M<sub>торможение</sub> = {self.orms_results.get('torque_stop', 0):.2f} Нм<br>
                - ω<sub>д.хх</sub> = {self.orms_results.get('idle_speed', 0):.2f} рад/с<br>
                - ω<sub>ном</sub> = {getattr(self.motor, 'n_nom', 0) * math.pi / 30:.2f} рад/с<br>
                - ω<sub>треб</sub> = {self.recalc_results.get('required_speed_with_gear', 0):.2f} рад/с<br>
                - M<sub>ном</sub> * λ = {self.orms_results.get('torque_nom_with_coef', 0):.2f} Нм<br></p>
                """
        html += f"""График приведенной диаграммы нагрузки и ОРМС представлен ниже:<br>"""
        html += f"""<img src="{os.path.join(os.getcwd(), 'image_graphic', 'chart.png')}"></p><br>"""
        return html
    
    def _html_thermal_calc(self):
        html = f"""<h3>Тепловой расчет</h3>"""
        html += f"""<h4>Метод эквивалентного момента</h4>"""
        html += f"""<p>Условиие выполнения: M<sub>дв.экв</sub><sup>2</sup> &le; M<sub>ном</sub><sup>2</sup><br>
                M<sub>дв.экв</sub><sup>2</sup> = 1/t<sub>ц</sub>(∫<sub>0</sub><sup>t<sub>ц</sub></sup> M<sub>дв</sub><sup>2</sup>(t) dt)<br>
                t<sub>ц</sub> = (t<sub>разг</sub> + t<sub>торм</sub>) / T<sub>пер.отн</sub> = 
                {getattr(self.source_data, 'tp', 0)} + {getattr(self.source_data, 'tp', 0)} / {getattr(self.source_data, 'tp_rel', 0)} = 
                {self.thermal_data.get('t_cycle', 0):.2f} с<br>
                t<sub>сл</sub> = t<sub>ц</sub> * (1 - T<sub>пер.отн</sub>) = 
                {self.thermal_data.get('t_cycle', 0):.2f} * (1 - {getattr(self.source_data, 'tp_rel', 0)}) =
                {self.thermal_data.get('t_s', 0):.2f} с<br>
                A<sub>экв</sub> = (ω<sub>макс.раб</sub><sup>2</sup>) / a<sub>макс.раб</sub> = 
                ({getattr(self.source_data, 'max_angle_speed_wm', 0):.2f}<sup>2</sup>) / {getattr(self.source_data, 'max_angle_acc_wm', 0):.2f} =
                {self.thermal_data.get('A_eqv', 0):.2f}<br>
                ω<sub>экв</sub> = a<sub>макс.раб</sub> / ω<sub>макс.раб</sub> = 
                {getattr(self.source_data, 'max_angle_acc_wm', 0):.2f} / {getattr(self.source_data, 'max_angle_speed_wm', 0):.2f} = 
                {self.thermal_data.get('omega_eqv', 0):.2f} рад/с<br>
                M<sub>сл</sub> = M<sub>ст1</sub> + M<sub>дин1</sub> / η = 
                M<sub>ст</sub> / (i<sub>р</sub> * η) + (J<sub>сум</sub> * A<sub>экв</sub> * ω<sub>экв</sub><sup>2</sup>) / η = 

                """
        return html