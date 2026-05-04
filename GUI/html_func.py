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