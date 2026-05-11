import matlab.engine
import matplotlib.pyplot as plt
import numpy as np

class MatlabEngine:
    def __init__(self):
        self.eng = matlab.engine.start_matlab()
        self.eng.addpath(r'MatlabTest\matlab_models', nargout=0)

    def run_simulation(self, model_name, source_data, thermal_data, motor_data, gear_data):
        speed_max_pereb = getattr(source_data, 'max_angl_speed', 0)
        tp = getattr(source_data, 'tp', 0)
        tp_sl = thermal_data.get('t_cycle', 0)
        A_eqv = thermal_data.get('A_eqv', 0)
        omega_eqv = thermal_data.get('omega_eqv', 0)
        
        max_stat_torque = getattr(source_data, 'max_stat_torque', 0)
        j_0 = getattr(source_data, 'eq_torque_intertia', 0)
        i_nom = getattr(motor_data, 'I_nom', 0) 
        j_a = getattr(motor_data, 'J', 0)
        r = getattr(motor_data, 'R', 0)
        km = getattr(motor_data, 'k', 0)
        i_gear = getattr(gear_data, 'i_nom', 0)

        self.eng.load_system(model_name, nargout=0)
        print("Запуск симуляции...")
        self.eng.set_param(f'{model_name}/Speed_max', 'Value', str(speed_max_pereb), nargout=0)
        self.eng.set_param(f'{model_name}/Trazg.', 'Value', str(tp), nargout=0)
        self.eng.set_param(f'{model_name}/Ttorm.', 'Value', str(tp), nargout=0)
        self.eng.set_param(f'{model_name}/Tsin', 'Value', str(tp_sl), nargout=0)
        self.eng.set_param(f'{model_name}/Amplituda', 'Value', str(A_eqv), nargout=0)
        self.eng.set_param(f'{model_name}/Chastota', 'Value', str(omega_eqv), nargout=0)

        self.eng.set_param(f'{model_name}/I_nom', 'Value', str(i_nom), nargout=0)
        self.eng.set_param(f'{model_name}/Mext', 'Value', str(max_stat_torque), nargout=0)
        self.eng.set_param(f'{model_name}/Jo', 'Value', str(j_0), nargout=0)
        self.eng.set_param(f'{model_name}/Ja', 'Value', str(j_a), nargout=0)
        self.eng.set_param(f'{model_name}/R', 'Value', str(r), nargout=0)
        self.eng.set_param(f'{model_name}/Km', 'Value', str(km), nargout=0)
        self.eng.set_param(f'{model_name}/i', 'Value', str(i_gear), nargout=0)
        self.eng.set_param(f'{model_name}/R', 'Value', str(r), nargout=0)

        self.eng.eval(f"sim('{model_name}')", nargout=0)

        moment_struct = self.eng.workspace['md']
        self.time = np.array(moment_struct['time']).flatten()
        signal_values = np.array(moment_struct['signals']['values'])
        
        self.current = signal_values[:, 0]
        self.moment = signal_values[:, 1]
        self.speed_engine = signal_values[:, 2]

        speed_acc_mo_struct = self.eng.workspace['speed_acc_mo']
        signal_values_speed_acc_mo = np.array(speed_acc_mo_struct['signals']['values'])
        
        self.speed = signal_values_speed_acc_mo[:, 0]
        self.acceleration = signal_values_speed_acc_mo[:, 1]
        self.mo = signal_values_speed_acc_mo[:, 2]

        current_for_thermal_struct = self.eng.workspace['i_isred']
        current_for_thermal = np.array(current_for_thermal_struct['signals']['values'])

        self.i_sred_2 = current_for_thermal[:, 0]
        self.i_nom_2 = current_for_thermal[:, 1]

        self.plot_current_torque_engine()
        self.plot_speed_acc_mo()

    def plot_current_torque_engine(self):
        plt.figure(figsize=(12, 8))
        plt.subplot(2, 2, 1)
        plt.plot(self.time, self.moment, 'r-', linewidth=2)
        plt.title('Момент двигателя')
        plt.xlabel('Время (с)')
        plt.ylabel('Момент (Н·м)')
        plt.grid(True)

        plt.subplot(2, 2, 2)
        plt.plot(self.time, self.current, 'b-', linewidth=2)
        plt.title('Ток якоря')
        plt.xlabel('Время (с)')
        plt.ylabel('Ток (А)')
        plt.grid(True)

        plt.subplot(2, 2, 3)
        plt.plot(self.time, self.speed_engine, 'g-', linewidth=2)
        plt.title('Скорость двигателя')
        plt.xlabel('Время (с)')
        plt.ylabel('Скорость (об/мин)')
        plt.grid(True)

        plt.subplot(2, 2, 4)
        plt.plot(self.time, self.i_nom_2, 'g-', linewidth=2, label='I_nom^2')
        plt.plot(self.time, self.i_sred_2, 'm-', linewidth=2, label='I_sred^2')
        plt.title('Квадраты токов для теплового расчёта')
        plt.xlabel('Время (с)')
        plt.ylabel('Ток (А)')
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.savefig('image_graphic/simulation_results.png')

    def plot_speed_acc_mo(self):
        plt.figure(figsize=(12, 8))
        plt.subplot(3, 1, 1)
        plt.plot(self.time, self.speed, 'r-', linewidth=2)
        plt.title('Скорость объекта управления')
        plt.xlabel('Время (с)')
        plt.ylabel('Скорость (рад/с)')
        plt.grid(True)

        plt.subplot(3, 1, 2)
        plt.plot(self.time, self.acceleration, 'b-', linewidth=2)
        plt.title('Ускорение объекта управления')
        plt.xlabel('Время (с)')
        plt.ylabel('Ускорение (рад/с²)')
        plt.grid(True)

        plt.subplot(3, 1, 3)
        plt.plot(self.time, self.mo, 'g-', linewidth=2)
        plt.title('Момент объекта управления')
        plt.xlabel('Время (с)')
        plt.ylabel('Момент (Н·м)')
        plt.grid(True)

        plt.tight_layout()
        plt.savefig('image_graphic/simulation_results_acc_speed_mo.png')

        
    def quit(self):
        self.eng.quit()