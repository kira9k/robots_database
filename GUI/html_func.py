import math
import os

def html_source_data(source_data):
        html = "<h2>Исходные данные для проектирования</h2>"
        html += """
            <table border="1" style="border-collapse: collapse; width: 400px;">
                <tr>
                    <th style="padding: 8px; text-align: left;">Параметр</th>
                    <th style="padding: 8px; text-align: left;">Условное обозначение</th>
                    <th style="padding: 8px; text-align: left;">Значение</th>
                </tr>
            """
        html += f"""
                <tr>
                    <td style="padding: 8px;"><b>Максимальная угловая скорость</b></td>
                    <td style="padding: 8px;">ω<sub>макс</sub></td>
                    <td style="padding: 8px;">{getattr(source_data, 'max_angl_speed', 0):.2f} рад/с</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Максимальное угловое ускорение</b></td>
                    <td style="padding: 8px;">a<sub>макс</sub></td>
                    <td style="padding: 8px;">{getattr(source_data, 'max_angl_acc', 0):.2f} рад/с²</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Максимальная угловая скорость рабочего движения</b></td>
                    <td style="padding: 8px;">ω<sub>раб.макс</sub></td>
                    <td style="padding: 8px;">{getattr(source_data, 'max_angle_speed_wm', 0):.2f} рад/с</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Максимальное угловое ускорение рабочего движения</b></td>
                    <td style="padding: 8px;">a<sub>раб.макс</sub></td>
                    <td style="padding: 8px;">{getattr(source_data, 'max_angle_acc_wm', 0):.2f} рад/с²</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Длительность разгона до максимальной скорости</b></td>
                    <td style="padding: 8px;">t<sub>р</sub></td>
                    <td style="padding: 8px;">{getattr(source_data, 'tp', 0):.2f} с</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Относительная длительность 'переброски' в рабочем цикле</b></td>
                    <td style="padding: 8px;">t<sub>р.отн</sub></td>
                    <td style="padding: 8px;">{getattr(source_data, 'tp_rel', 0):.2f} с</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Максимальный статический момент сил</b></td>
                    <td style="padding: 8px;">M<sub>ст</sub></td>
                    <td style="padding: 8px;">{getattr(source_data, 'max_stat_torque', 0):.2f} Нм</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Максимальный динамический момент сил</b></td>
                    <td style="padding: 8px;">M<sub>дин</sub></td>
                    <td style="padding: 8px;">{getattr(source_data, 'max_dyn_torque', 0):.2f} Нм</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Эквивалентный момент инерции</b></td>
                    <td style="padding: 8px;">J<sub>экв</sub></td>
                    <td style="padding: 8px;">{getattr(source_data, 'eq_torque_intertia', 0):.2f} кг·м²</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Максимальная допустимая ошибка</b></td>
                    <td style="padding: 8px;">ε<sub>макс</sub></td>
                    <td style="padding: 8px;">{getattr(source_data, 'max_error', 0):.2f} рад</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Максимальная допустимая ошибка</b></td>
                    <td style="padding: 8px;">ε<sub>макс</sub></td>
                    <td style="padding: 8px;">{getattr(source_data, 'max_error', 0):.2f} рад</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Максимальное перерегулирование</b></td>
                    <td style="padding: 8px;">δ<sub>макс</sub></td>
                    <td style="padding: 8px;">{getattr(source_data, 'overshoot', 0):.2f} %</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Время переходного процесса</b></td>
                    <td style="padding: 8px;">t<sub>п</sub></td>
                    <td style="padding: 8px;">{getattr(source_data, 'transition_time', 0):.2f} с</td>
                </tr>
                """
        html += "</table>"
        return html

def html_found_motor(motor):
        if motor:
            html = "<h3>Двигатель</h3>"
            html += """
            <table border="1" style="border-collapse: collapse; width: 400px;">
                <tr>
                    <th style="padding: 8px; text-align: left;">Характеристика</th>
                    <th style="padding: 8px; text-align: left;">Значение</th>
                </tr>
            """
            html += f"""
                <tr>
                    <td style="padding: 8px;"><b>Модель</b></td>
                    <td style="padding: 8px;">{getattr(motor, 'name', '')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Тип двигателя</b></td>
                    <td style="padding: 8px;">{getattr(motor, 'type', '')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Номинальная мощность P<sub>ном</sub></b></td>
                    <td style="padding: 8px;">{getattr(motor, 'p_nom', '')} Вт</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Номинальный момент M<sub>ном</sub></b></td>
                    <td style="padding: 8px;">{getattr(motor, 'torque_nom', '')} Нм</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Номинальная частота вращения n<sub>ном</sub></b></td>
                    <td style="padding: 8px;">{getattr(motor, 'n_nom', '')} об/мин</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Номинальный ток якоря I<sub>ном</sub></b></td>
                    <td style="padding: 8px;">{getattr(motor, 'I_nom', '')} А</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Максимальный ток якоря I<sub>макс</sub></b></td>
                    <td style="padding: 8px;">{getattr(motor, 'max_current', '')} А</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Сопротивление якоря R<sub>я</sub></b></td>
                    <td style="padding: 8px;">{getattr(motor, 'R', '')} Ом</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Индуктивность якоря L<sub>я</sub></b></td>
                    <td style="padding: 8px;">{getattr(motor, 'L_a', '')} Гн</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Номинальное напряжение U<sub>ном</sub></b></td>
                    <td style="padding: 8px;">{getattr(motor, 'U_nom', '')} В</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Момент инерции ротора J<sub>дв</sub></b></td>
                    <td style="padding: 8px;">{getattr(motor, 'J', '')} кг·м²</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Масса двигателя</b></td>
                    <td style="padding: 8px;">{getattr(motor, 'm', '')} кг</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Чертеж двигателя</b></td>
                    <td style="padding: 8px;"><img src={getattr(motor, 'drawing', '')} alt="Чертеж двигателя" style="max-width: 700px; max-height: 700px;"></td>
                </tr>
            """
            html += "</table>"
        else:
            pass
        return html
    

def html_found_gear(gear):
    html = ""
    if gear:
        html += "<h3>Редуктор</h3>"
        html += """
        <table border="1" style="border-collapse: collapse; width: 400px;">
            <tr>
                <th style="padding: 8px; text-align: left;">Характеристика</th>
                <th style="padding: 8px; text-align: left;">Значение</th>
            </tr>
        """
        html += f"""
            <tr>
                <td style="padding: 8px;"><b>Модель</b></td>
                <td style="padding: 8px;">{gear.name}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Тип редуктора</b></td>
                <td style="padding: 8px;">{gear.type}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Передаточное отношение i<sub>ред</sub></b></td>
                <td style="padding: 8px;">{gear.i_nom}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Номинальный момент M<sub>ном.ред</sub></b></td>
                <td style="padding: 8px;">{gear.torque_nom} Нм</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Номинальная частота вращения n<sub>ном.ред</sub></b></td>
                <td style="padding: 8px;">{gear.speed_norm} об/мин</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Жесткость редуктора C</b></td>
                <td style="padding: 8px;">{gear.c}  Нм/рад</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Люфт редуктора &sigma;</b></td>
                <td style="padding: 8px;">{gear.clearance} рад</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Масса редуктора m</b></td>
                <td style="padding: 8px;">{gear.m} кг</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Чертеж редуктора</b></td>
                <td style="padding: 8px;"><img src={getattr(gear, 'drawing', '')} alt="Чертеж редуктора" style="max-width: 700px; max-height: 700px;"></td>
            </tr>
        """
        html += "</table>"
    return html

def html_found_encoder(closest_encoder):
    html= f"""<h3>Энкодер</h3>"""
    html += """
        <table border="1" style="border-collapse: collapse; width: 400px;">
            <tr>
                <th style="padding: 8px; text-align: left;">Характеристика</th>
                <th style="padding: 8px; text-align: left;">Значение</th>
            </tr>
        """
    html += f"""
            <tr>
                <td style="padding: 8px;"><b>Модель</b></td>
                <td style="padding: 8px;">{closest_encoder.name}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Тип энкодера</b></td>
                <td style="padding: 8px;">{closest_encoder.type}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Количество дискрет на оборот N<sub>имп</sub></b></td>
                <td style="padding: 8px;">{closest_encoder.N}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Масса, m<sub>датч</sub></b></td>
                <td style="padding: 8px;">{closest_encoder.m} кг</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Максимальная частота вращения n<sub>макс.датч</sub></b></td>
                <td style="padding: 8px;">{closest_encoder.max_speed} об/мин</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Момент инерции энкодера J<sub>датч</sub></b></td>
                <td style="padding: 8px;">{closest_encoder.j} кг*м^2</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Чертеж энкодера</b></td>
                <td style="padding: 8px;"><img src={getattr(closest_encoder, 'drawing', '')} alt="Чертеж энкодера" style="max-width: 700px; max-height: 700px;"></td>
            </tr>
        """
    html += "</table>"
    return html

def html_coef_regulators(coef_regulators):
    html= f"""<h4>Коэффициенты регуляторов</h4>"""
    html += """
        <table border="1" style="border-collapse: collapse; width: 400px;">
            <tr>
                <th style="padding: 8px; text-align: left;">Коэффициент</th>
                <th style="padding: 8px; text-align: left;">Значение</th>
            </tr>
        """
    html += f"""
            <tr>
                <td style="padding: 8px;"><b>Коэффициент П сотавляющей регулятора тока</b></td>
                <td style="padding: 8px;">{coef_regulators.k_c}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Коэффициент И сотавляющей регулятора тока</b></td>
                <td style="padding: 8px;">{coef_regulators.k_ci}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Коэффициент обратной связи по току</b></td>
                <td style="padding: 8px;">{coef_regulators.k_dc}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Коэффициент П сотавляющей регулятора скорости</b></td>
                <td style="padding: 8px;">{coef_regulators.k_s}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Коэффициент И сотавляющей регулятора скорости</b></td>
                <td style="padding: 8px;">{coef_regulators.k_si}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Коэффициент обратной связи по скорости</b></td>
                <td style="padding: 8px;">{coef_regulators.k_ds}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Коэффициент П сотавляющей регулятора положения</b></td>
                <td style="padding: 8px;">{coef_regulators.k_a}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Коэффициент И сотавляющей регулятора положения</b></td>
                <td style="padding: 8px;">{coef_regulators.k_ai}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Коэффициент датчика положения</b></td>
                <td style="padding: 8px;">{coef_regulators.k_ds}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Коэффициент усиления силового преобразователя</b></td>
                <td style="padding: 8px;">{coef_regulators.k_pwm}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Постоянная времени силового преобразователя</b></td>
                <td style="padding: 8px;">{coef_regulators.T_pwm}</td>
            <tr>
                <td style="padding: 8px;"><b>Коэффициент feedforward</b></td>
                <td style="padding: 8px;">{coef_regulators.k_feedforward}</td>
            </tr>
        """
    html += "</table>"
    return html

def html_utils_data(utils):
    html= f"""<h4>Справочные данные</h4>"""
    html += """
        <table border="1" style="border-collapse: collapse; width: 400px;">
            <tr>
                <th style="padding: 8px; text-align: left;">Характеристика</th>
                <th style="padding: 8px; text-align: left;">Значение</th>
            </tr>
        """
    html += f"""
            <tr>
                <td style="padding: 8px;"><b>Амплитуда эквивалентного гармонического движения</b></td>
                <td style="padding: 8px;">{utils.A_e}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Частота эквивалентного гармонического движения</b></td>
                <td style="padding: 8px;">{utils.omega_e}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Допустимая динамическая ошибка</b></td>
                <td style="padding: 8px;">{utils.dyn_error}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><b>Допустимая статическая ошибка</b></td>
                <td style="padding: 8px;">{utils.stat_error}</td>
            </tr>
        """
    html += "</table>"
    return html

def html_matlab_test():
        html = f"""<h3>Моделирование электропривода</h3><br>"""
        html += f"""<img src="{os.path.join(os.getcwd(), 'image_graphic', 'angle_plot.png')}"></p><br>"""
        return html


def html_calculation_results(source_data, results):
        html = "<h2>Расчетные результаты</h2>"
        html += f"""
                <h3>Максимальный момент</h3>
                <p>M<sub>макс</sub> = M<sub>ст</sub> + M<sub>дин</sub> = 
                {getattr(source_data, 'max_stat_torque', 0)} + {getattr(source_data, 'max_dyn_torque', 0)} = 
                {results.get('torque', 0):.2f} Нм</p>
                """
        html += f"""
                <h3>Максимальная мощность</h3>
                <p>P<sub>макс</sub> = M<sub>макс</sub> * ω<sub>макс</sub> = 
                {results.get('torque', 0):.2f} * {getattr(source_data, 'max_angl_speed', 0):.2f} = {results.get('original_power', 0):.2f} Вт</p>
        """
        return html

def html_required_power(source_data, results):
        html = f"""
                <h3>Требуемая мощность с двигателя</h3>
                <p>P<sub>треб</sub> = P<sub>макс</sub> * (2,5...3) = 
                {results.get('original_power', 0):.2f} * {results.get('power_margin', 0):.2f} = 
                {results.get('power', 0):.2f} Вт</p>
                """
        return html

def html_optimal_gear_ratio(results, source_data, motor, gear_ratio):
        html = f"""<h3>Оптимальное передаточное отношение</h3>
                        <p>i<sub>opt</sub> = 
                        √(P<sub>макс</sub> / (J<sub>дв</sub> * ω<sub>макс</sub> * a<sub>макс</sub>)) =
                        √({results.get('original_power', 0):.2f} / ({getattr(motor, 'J', ''):.7f} * {getattr(source_data, 'max_angl_speed', 0):.2f} * {getattr(source_data, 'max_angl_acc', 0):.2f})) = 
                        {gear_ratio:.2f}</p>
                    """
        return html

def html_check_motor(source_data, results, gear, motor, recalc_results):
        html = "<h3>Проверка правильности выбора двигателя</h3>"
        html += f"""Проверка по моменту:<br>
                    M<sub>треб</sub> = M<sub>макс</sub> / (η * i<sub>р</sub>) = 
                    {results.get('torque', 0):.2f} / ({gear.efficiency:.2f} * {gear.i_nom:.2f}) = 
                    {recalc_results.get('required_torque_with_gear', 0):.2f} Нм &le; M<sub>ном</sub> = {getattr(motor, 'torque_nom', '')} Нм<br><br>
        """
        html += f"""Проверка по частоте вращения:<br>
                    ω<sub>треб</sub> = ω<sub>макс</sub> * i<sub>р</sub> = 
                    {getattr(source_data, 'max_angl_speed', 0):.2f} * {gear.i_nom:.2f} = 
                    {recalc_results.get('required_speed_with_gear', 0):.2f} рад/с &le; ω<sub>ном</sub> = {getattr(motor, 'n_nom', 0) * math.pi / 30:.2f} рад/с<br>
                """
        return html

def html_orms(motor, source_data, gear, orms_results):
        html = f"""<h3>Построение области располагаемых моментов и скоростей и приведенной диаграммы нагрузки привода</h3>"""
        html += f"""J<sub>сум</sub> = J<sub>дв</sub> + J<sub>экв.прив</sub> = 
                J<sub>дв</sub> + J<sub>экв</sub> / (i<sub>р</sub><sup>2</sup> * η) = 
                {getattr(motor, 'J', ''):.5f} + {getattr(source_data, 'eq_torque_intertia', 0):.5f} / ({gear.i_nom}<sup>2</sup> * {gear.efficiency}) =
                {orms_results.get('j_sum', 0):.7f} кг·м²<br>
                a<sub>дв.макс</sub> = i<sub>р</sub> * a<sub>макс</sub> = 
                {gear.i_nom} * {getattr(source_data, 'max_angl_acc', 0):.2f} =
                {orms_results.get('acceleration_engine_with_gear', 0):.2f} рад/с²<br>
                M<sub>ст.прив</sub> = M<sub>ст</sub> / (i<sub>р</sub> * η) = 
                {getattr(source_data, 'max_stat_torque', 0):.2f} / {gear.i_nom} * {gear.efficiency}) =
                {orms_results.get('torque_stat_gear', 0):.2f} Нм<br>
                M<sub>дин.прив</sub> = J<sub>сум</sub> * a<sub>дв.макс</sub> = 
                {orms_results.get('j_sum', 0):.7f} * {orms_results.get('acceleration_engine_with_gear', 0):.2f} =
                {orms_results.get('torque_dyn_gear', 0):.2f} Нм<br>
                M<sub>разог</sub> = M<sub>ст.прив</sub> + M<sub>дин.прив</sub> = 
                {orms_results.get('torque_stat_gear', 0):.2f} + {orms_results.get('torque_dyn_gear', 0):.2f} = 
                {orms_results.get('torque_start', 0):.2f} Нм <br>
                M<sub>торможение</sub> = M<sub>ст.прив</sub> - M<sub>дин.прив</sub> = 
                {orms_results.get('torque_stat_gear', 0):.2f} - {orms_results.get('torque_dyn_gear', 0):.2f} = 
                {orms_results.get('torque_stop', 0):.2f} Нм<br>
                k<sub>e</sub> = (U<sub>я</sub> - I<sub>я</sub> * R<sub>я</sub>) / (n<sub>ном</sub> * π / 30) =
                ({getattr(motor, 'U_nom', 0):.2f} - {getattr(motor, 'I_nom', 0):.2f} * {getattr(motor, 'R', 0):.2f}) / ({getattr(motor, 'n_nom', 0) * math.pi / 30:.2f}) =
                {orms_results.get('emf_coef', 0):.2f} В * c/рад<br>
                ω<sub>д.хх</sub> = U<sub>я</sub> / k<sub>e</sub> = 
                {getattr(motor, 'U_nom', 0):.2f} / {orms_results.get('emf_coef', 0):.2f} =
                {orms_results.get('idle_speed', 0):.2f} рад/с</p>
                <h4>Коэффициент форсирования</h4>
                    <p>λ = M<sub>макс</sub> / M<sub>ном</sub><br> 
                    λ = {orms_results.get('torque_start', 0):.2f} / {getattr(motor, 'torque_nom', '')} = 
                    {orms_results.get('torque_start', 0) / getattr(motor, 'torque_nom', 1):.2f}<br>
                    Принимаем λ = {orms_results.get('coef_forcing', 0):.2f}</p>
                <p>Приведенная диаграмма нагрузки и ОРМС представлены ниже и содержит следующие характерные точки:<br>
                - M<sub>ст.прив</sub> = {orms_results.get('torque_stat_gear', 0):.2f} Нм<br>
                - M<sub>дин.прив</sub> = {orms_results.get('torque_dyn_gear', 0):.2f} Нм<br>
                - M<sub>разгон</sub> = {orms_results.get('torque_start', 0):.2f} Нм<br>
                - M<sub>торможение</sub> = {orms_results.get('torque_stop', 0):.2f} Нм<br>
                - ω<sub>д.хх</sub> = {orms_results.get('idle_speed', 0):.2f} рад/с<br>
                - ω<sub>ном</sub> = {getattr(motor, 'n_nom', 0) * math.pi / 30:.2f} рад/с<br>
                - ω<sub>треб</sub> = {orms_results.get('required_speed_with_gear', 0):.2f} рад/с<br>
                - M<sub>ном</sub> * λ = {orms_results.get('torque_nom_with_coef', 0):.2f} Нм<br></p>
                """
        html += f"""График приведенной диаграммы нагрузки и ОРМС представлен ниже:<br>"""
        html += f"""<img src="{os.path.join(os.getcwd(), 'image_graphic', 'chart.png')}"></p><br>"""
        return html

def html_thermal_calc(source_data, orms_results, thermal_data, motor, gear):
        html = f"""<h3>Тепловой расчет</h3>"""
        html += f"""<h4>Метод эквивалентного момента</h4>"""
        html += f"""<p>Условие выполнения: M<sub>дв.экв</sub><sup>2</sup> &le; M<sub>ном</sub><sup>2</sup><br>
                M<sub>дв.экв</sub><sup>2</sup> = 1/t<sub>ц</sub>(∫<sub>0</sub><sup>t<sub>ц</sub></sup> M<sub>дв</sub><sup>2</sup>(t) dt)<br>
                t<sub>ц</sub> = (t<sub>разг</sub> + t<sub>торм</sub>) / T<sub>пер.отн</sub> = 
                {getattr(source_data, 'tp', 0)} + {getattr(source_data, 'tp', 0)} / {getattr(source_data, 'tp_rel', 0)} = 
                {thermal_data.get('t_cycle', 0):.2f} с<br>
                t<sub>сл</sub> = t<sub>ц</sub> * (1 - T<sub>пер.отн</sub>) = 
                {thermal_data.get('t_cycle', 0):.2f} * (1 - {getattr(source_data, 'tp_rel', 0)}) =
                {thermal_data.get('t_s', 0):.2f} с<br>
                A<sub>экв</sub> = (ω<sub>макс.раб</sub><sup>2</sup>) / a<sub>макс.раб</sub> = 
                ({getattr(source_data, 'max_angle_speed_wm', 0):.2f}<sup>2</sup>) / {getattr(source_data, 'max_angle_acc_wm', 0):.2f} =
                {thermal_data.get('A_eqv', 0):.2f}<br>
                ω<sub>экв</sub> = a<sub>макс.раб</sub> / ω<sub>макс.раб</sub> = 
                {getattr(source_data, 'max_angle_acc_wm', 0):.2f} / {getattr(source_data, 'max_angle_speed_wm', 0):.2f} = 
                {thermal_data.get('omega_eqv', 0):.2f} рад/с<br>
                M<sub>сл</sub> = M<sub>ст1</sub> + M<sub>дин1</sub> = 
                M<sub>ст</sub> / (i<sub>р</sub> * η) + (J<sub>сум</sub> * A<sub>экв</sub> * ω<sub>экв</sub><sup>2</sup>) = 
                {getattr(source_data, 'max_stat_torque', 0):.2f} / ({getattr(gear, 'i_nom', 0)} * {getattr(gear, 'efficiency', 0)}) + 
                ({getattr(orms_results, 'j_sum', 0):.7f} * {thermal_data.get('A_eqv', 0):.2f} * {thermal_data.get('omega_eqv', 0):.2f}<sup>2</sup>) =
                {thermal_data.get('M_c', 0):.2f} Нм<br>
                M<sub>дв.экв</sub><sup>2</sup> = 1/t<sub>ц</sub>(M<sub>разгон</sub><sup>2</sup> * t<sub>разг</sub> + M<sub>торм</sub><sup>2</sup> * t<sub>торм</sub> + M<sub>сл</sub><sup>2</sup> * t<sub>сл</sub>) =
                1/{thermal_data.get('t_cycle', 0):.2f} * ({orms_results.get('torque_start', 0):.2f}<sup>2</sup> * {getattr(source_data, 'tp', 0):.2f} + 
                {orms_results.get('torque_stop', 0):.2f}<sup>2</sup> * {getattr(source_data, 'tp', 0):.2f} + 
                {thermal_data.get('M_c', 0):.2f}<sup>2</sup> * {thermal_data.get('t_s', 0):.2f}) = 
                {thermal_data.get('M_eqv_square', 0):.2f} Нм<br>
                Таким образом,<br>
                M<sub>дв.экв</sub><sup>2</sup> = {thermal_data.get('M_eqv_square', 0):.2f} Нм &le; M<sub>ном</sub><sup>2</sup> = {getattr(motor, 'torque_nom', 0)**2:.2f} Нм<br>
                """
        return html

def html_encoder_calc(source_data, error, gear):
        html = f"""<h3>Расчет параметров энкодера</h3>"""
        html += f"""<h4>Анализ точности привода</h4>"""
        html += f"""<p>Условие выполнения:<br>
                δ<sub>доп</sub> &ge; δ<sub>макс</sub> <br>
                δ<sub>макс</sub> = δ<sub>1</sub> + δ<sub>2</sub> + δ<sub>3</sub> + δ<sub>4</sub> + δ<sub>5</sub> = 
                M<sub>вн.макс</sub>/C + σ/2 + Δ<sub>датч</sub> + δ<sub>д.дин</sub> + δ<sub>д.м</sub> <br>
                Будем считать, что система управления манипулятором обеспечивает вычисление моментов нагрузки и формирование корректирующих воздействий, 
                которые на 95% компенсируют погрешность привода, обусловленную упругой податливостью редуктора <br>
                δ<sub>1.доп</sub> = 0.05 * {getattr(source_data, 'max_stat_torque', 0):.2f} / {getattr(gear, 'c', 0):.2f} = {getattr(error, 'first_error', 0):.8f} рад<br>
                δ<sub>2.доп</sub> = σ/2 = {getattr(gear, 'clearance', 0):.8f}/2 = {getattr(error, 'second_error', 0):.8f} рад<br>
                Считаем, что внешний момент изменяется настолько медленно, что динамическая ошибка, вызванная изменением момента, также равна нулю<br>
                δ<sub>5.доп</sub> = 0 рад<br>
                δ<sub>3.доп</sub> + δ<sub>4.доп</sub> = δ<sub>доп</sub> - δ<sub>1.доп</sub> - δ<sub>2.доп</sub> - δ<sub>5.доп</sub> = 
                {getattr(source_data, 'max_error', 0):.2f} - {getattr(error, 'first_error', 0):.8f} - {getattr(error, 'second_error', 0):.8f} - 0 =
                {getattr(error, 'third_fourth_error', 0):.8f} рад<br>
                Из соображений обеспечения точности привода целесообразно принять δ<sub>3.доп</sub> &lt; &lt; δ<sub>4.доп</sub> <br>
                δ<sub>3.доп</sub>= 0.05 * δ<sub>4.доп</sub><br>
                δ<sub>3.доп</sub> = {getattr(error, 'third_error', 0):.8f} рад<br>
                δ<sub>4.доп</sub> = {getattr(error, 'fourth_error', 0):.8f} рад<br>
                """
        return html

def html_found_encoder(closest_encoder, error, gear, enc_min):
        html= f"""<h4>Подбор энкодера</h4>"""
        html += f"""<p>Условие выполнения:<br>
                Δ<sub>датч</sub> = 2π / (N<sub>датч</sub> * 4) &le; δ<sub>3.доп</sub> * i<sub>ред</sub><br>
                N<sub>имп.треб</sub> &ge; π / (2 * δ<sub>3.доп</sub> * i<sub>ред</sub>) = π / (2 * {getattr(error, 'third_error', 0):.8f} * {getattr(gear, 'i_nom', 0):.2f}) = {enc_min} дискрет/об<br>
                 <h4>Выбранный энкодер</h4>
        """
        return html