from .MatlabEngine import MatlabEngine
import matplotlib.pyplot as plt
import numpy as np
import math
import matlab.engine


class MatlabLAB2():
    def __init__(self):
        self.eng = matlab.engine.start_matlab()
        self.eng.addpath(r'MatlabTest\matlab_models', nargout=0)

    def run_simulation(self, model_name, sd, orms_res, thermal_data, motor_data, gear_data, coef_regulators, flag_calc=False):
        i_gear = getattr(gear_data, 'i_nom', 0)
        clearence = getattr(gear_data, 'clearance', 0)
        
        j_a = orms_res.get("j_sum", 0)
        t_e = getattr(motor_data, 'T_e', 0)
        km = getattr(motor_data, 'k', 0)
        ra = getattr(motor_data, 'R', 0)

        m_ext = orms_res.get("torque_stat_gear")

        t_sh = getattr(coef_regulators, 'T_pwm', 0)
        k_sh = getattr(coef_regulators, 'k_pwm', 0)

        k_ds = getattr(coef_regulators, 'k_ds', 0)
        k_s = getattr(coef_regulators, 'k_s', 0)
        k_is = getattr(coef_regulators, 'k_si', 0)

        k_dc = getattr(coef_regulators, 'k_dc', 0)
        k_c = getattr(coef_regulators, 'k_c', 0)
        k_ic = getattr(coef_regulators, 'k_ci', 0)

        k_a = getattr(coef_regulators, 'k_a', 0)
        k_ai = getattr(coef_regulators, 'k_ai', 0)
        
        try:
            a_eqv = thermal_data.get('A_eqv', 0)
            omega_eqv = thermal_data.get('omega_eqv', 0)
        except:
            pass

        try:
            a_eqv = thermal_data.A_e
            omega_eqv = thermal_data.omega_e
        except:
            pass

        self.eng.load_system(model_name, nargout=0)
        print(f"Запуск симуляции {model_name}...")

        self.eng.set_param(f'{model_name}/Input_signals/a_eqv', 'Value', str(a_eqv), nargout=0)
        self.eng.set_param(f'{model_name}/Input_signals/omega_eqv', 'Value', str(omega_eqv), nargout=0)
        
        self.eng.eval(f"assignin('base', 'kdc', {k_dc})", nargout=0)
        self.eng.set_param(f'{model_name}/kdc', 'Gain', str(k_dc), nargout=0)
        self.eng.set_param(f'{model_name}/kds', 'Gain', str(k_ds), nargout=0)

        #self.eng.set_param(f'{model_name}/angle_control/kp', 'Gain', str(k_a), nargout=0)
        self.eng.workspace['kp'] = k_a
        #self.eng.set_param(f'{model_name}/angle_control/kpi', 'Gain', str(k_ai), nargout=0)
        self.eng.workspace['kpi'] = k_ai

        #self.eng.set_param(f'{model_name}/angle_control1/kp', 'Gain', str(k_a), nargout=0)
        #self.eng.set_param(f'{model_name}/angle_control1/kpi', 'Gain', str(k_ai), nargout=0)

        self.eng.set_param(f'{model_name}/speed_control/ks', 'Gain', str(k_s), nargout=0)
        self.eng.set_param(f'{model_name}/speed_control/ksi', 'Gain', str(k_is), nargout=0)

        self.eng.set_param(f'{model_name}/current_control/kc', 'Gain', str(k_c), nargout=0)
        self.eng.set_param(f'{model_name}/current_control/kci', 'Gain', str(k_ic), nargout=0)    

        self.eng.set_param(f'{model_name}/DC/T_pwm', 'Denominator', f"[{str(t_sh)} 1]", nargout=0)
        self.eng.set_param(f'{model_name}/DC/T_pwm', 'Numerator', f"{str(k_sh)}", nargout=0)
        
        self.eng.set_param(f'{model_name}/DC/dc', 'Numerator', f"{str(1/ra)}", nargout=0)
        self.eng.set_param(f'{model_name}/DC/dc', 'Denominator', f"[{str(t_e)} 1]", nargout=0)

        self.eng.set_param(f'{model_name}/DC/j_d', 'Denominator', f"[{str(j_a)} 0]", nargout=0)

        self.eng.set_param(f"{model_name}/DC/ke", 'Gain', str(km), nargout=0)
        self.eng.set_param(f'{model_name}/DC/km', 'Gain', str(km), nargout=0)

        self.eng.set_param(f'{model_name}/Mext', 'Value', str(m_ext), nargout=0)

        self.eng.set_param(f'{model_name}/backlash', 'BacklashWidth', str(clearence), nargout=0)

        path_to_func = r'D:\master_dis\robots_database\MatlabTest\matlab_m_files'
        self.eng.addpath(path_to_func, nargout=0)
        

        self.eng.workspace['index'] = 1
        self.value = 1000000
        self.eng.workspace['k_feedforward'] = 0
        self.value_ff = 0
        self.value_i = 0
        
        if sd.non_linear_correction and flag_calc:
            self.eng.set_param(model_name, 'StopTime', '1', nargout=0)
            self.eng.set_param(model_name, 'StartTime', '0', nargout=0)
            if coef_regulators.k_ai == 0:
                OptDesign, Info = self.eng.non_linear_optimize([], sd.overshoot, sd.transition_time, nargout=2)
                self.eng.workspace['OptDesign'] = OptDesign
                self.value = self.eng.eval("OptDesign.Value", nargout=1)
                self.eng.workspace['kp'] = self.value
                print(f"Value = {self.value}")
            else:
                OptDesign, Info = self.eng.pi_angle_optimize([], sd.overshoot, sd.transition_time, nargout=2)
                self.eng.workspace['OptDesign'] = OptDesign
                self.value = self.eng.eval("OptDesign(1,1).Value", nargout=1)
                self.value_i = self.eng.eval("OptDesign(2,1).Value", nargout=1)
                self.eng.workspace['kp'] = self.value
                self.eng.workspace['kpi'] = self.value_i
                print(f"Value = {self.value}")
        elif not flag_calc:
            self.eng.workspace['kp'] = coef_regulators.k_a
            self.eng.workspace['kpi'] = coef_regulators.k_ai

        if sd.feedforward and flag_calc:
            self.eng.set_param(model_name, 'StopTime', '3', nargout=0)
            self.eng.set_param(model_name, 'StartTime', '0', nargout=0)
            self.eng.workspace['index'] = 2
            self.eng.workspace['k_feedforward'] = 0.1
            time_vector = np.arange(0, 3.01, 0.01).reshape(-1, 1)
            y = a_eqv * np.sin(omega_eqv * time_vector)

            OptDesignFF, InfoFF = self.eng.feedforward_optimize([], time_vector, y, nargout=2)
            self.eng.workspace['OptDesignFF'] = OptDesignFF
            self.value_ff = self.eng.eval("OptDesignFF.Value", nargout=1)
            self.eng.workspace['k_feedforward'] = self.value_ff
            print(f"Value = {self.value_ff}")
        elif not flag_calc:
            self.eng.workspace['k_feedforward'] = coef_regulators.k_feedforward


            

        self.eng.workspace['index'] = 3

        
        self.eng.set_param(model_name, 'StopTime', '10', nargout=0)
        self.eng.set_param(model_name, 'StartTime', '0', nargout=0)
        self.eng.eval(f"sim('{model_name}')", nargout=0)

        self.time = np.array(self.eng.eval("ans.angle.time")).flatten()
        self.angle = np.array(self.eng.eval("ans.angle.signals.values")).flatten()
        self.input = np.array(self.eng.eval("ans.input.signals.values")).flatten()
       

        self.eng.workspace['index'] = 1

        self.eng.set_param(model_name, 'StopTime', '1', nargout=0)
        self.eng.set_param(model_name, 'StartTime', '0', nargout=0)

        self.eng.eval(f"sim('{model_name}')", nargout=0)

        self.time_2 = np.array(self.eng.eval("ans.angle.time")).flatten()
        self.angle_2 = np.array(self.eng.eval("ans.angle.signals.values")).flatten()
        self.input_2 = np.array(self.eng.eval("ans.input.signals.values")).flatten()

        self.eng.workspace['index'] = 2

        self.eng.set_param(model_name, 'StopTime', '10', nargout=0)
        self.eng.set_param(model_name, 'StartTime', '0', nargout=0)

        self.eng.eval(f"sim('{model_name}')", nargout=0)

        self.time_sin = np.array(self.eng.eval("ans.angle.time")).flatten()
        self.angle_sin= np.array(self.eng.eval("ans.angle.signals.values")).flatten()
        self.input_sin = np.array(self.eng.eval("ans.input.signals.values")).flatten()

        self.eng.workspace['index'] = 4

        self.eng.set_param(model_name, 'StopTime', '3', nargout=0)
        self.eng.set_param(model_name, 'StartTime', '0', nargout=0)

        self.eng.eval(f"sim('{model_name}')", nargout=0)

        self.time_esc = np.array(self.eng.eval("ans.angle.time")).flatten()
        self.angle_esc= np.array(self.eng.eval("ans.angle.signals.values")).flatten()
        self.input_esc = np.array(self.eng.eval("ans.input.signals.values")).flatten()
        
        self.plot_angle()
    
    def plot_angle(self):
        plt.figure(figsize=(12, 8))

        plt.subplot(4, 2, 1)
        plt.plot(self.time_2, self.angle_2, 'r-', linewidth=2, label='Угол поворота')
        plt.axhline(y=self.input_2[0], color='b', linestyle='--', linewidth=2, label='Заданный угол')
        plt.title('Угол поворота при ступенчатом воздействии')
        plt.xlabel('Время (с)')
        plt.ylabel('Угол (рад)')
        plt.grid(True)
        plt.legend()

        plt.subplot(4, 2, 2)
        plt.plot(self.time_2, (self.input_2[0] - self.angle_2), 'r-', linewidth=2, label='Угол поворота')
        plt.title('Ошибка при ступенчатом воздействии')
        plt.xlabel('Время (с)')
        plt.ylabel('Угол (рад)')
        plt.grid(True)
        
        plt.subplot(4, 2, 3)
        plt.plot(self.time, self.angle, 'r-', linewidth=2, label='Угол поворота')
        plt.plot(self.time, self.input, 'b--', linewidth=2, label='Заданный угол')
        plt.title('Угол поворота при импульсном воздействии')
        plt.xlabel('Время (с)')
        plt.ylabel('Угол (рад)')
        plt.grid(True)
        plt.legend()

        plt.subplot(4, 2, 4)
        plt.plot(self.time, (self.input - self.angle), 'r-', linewidth=2, label='Угол поворота')
        plt.title('Ошибка при импульсном воздействии')
        plt.xlabel('Время (с)')
        plt.ylabel('Угол (рад)')
        plt.grid(True)
        
        plt.subplot(4, 2, 5)
        plt.plot(self.time_esc, self.angle_esc, 'r-', linewidth=2, label='Угол поворота')
        plt.plot(self.time_esc, self.input_esc, 'b--', linewidth=2, label='Заданный угол')
        plt.title('Угол поворота при нарастающем воздействии')
        plt.xlabel('Время (с)')
        plt.ylabel('Угол (рад)')
        plt.grid(True)
        plt.legend()

        plt.subplot(4, 2, 6)
        plt.plot(self.time_esc, (self.input_esc - self.angle_esc), 'r-', linewidth=2, label='Угол поворота')
        plt.title('Ошибка при нарастающем воздействии')
        plt.xlabel('Время (с)')
        plt.ylabel('Угол (рад)')
        plt.grid(True)

        plt.subplot(4, 2, 7)
        plt.plot(self.time_sin, self.angle_sin, 'r-', linewidth=2, label='Угол поворота')
        plt.plot(self.time_sin, self.input_sin, 'b--', linewidth=2, label='Заданный угол')
        plt.title('Угол поворота при гармоническом воздействии')
        plt.xlabel('Время (с)')
        plt.ylabel('Угол (рад)')
        plt.grid(True)
        plt.legend()

        plt.subplot(4, 2, 8)
        plt.plot(self.time_sin, (self.input_sin - self.angle_sin), 'r-', linewidth=2, label='Угол поворота')
        plt.title('Ошибка при гармоническом воздействии')
        plt.xlabel('Время (с)')
        plt.ylabel('Угол (рад)')
        plt.grid(True)

        plt.tight_layout()
        plt.savefig('image_graphic/angle_plot.png')

        