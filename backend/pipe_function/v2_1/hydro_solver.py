#В этом модуле происходит расчет основных технологических параметров (Qн, Qг, Qв, P)

from . import BeggsandBrill as BB
from . import check_anticoorosion_compliance as ac
import numpy as np
import matplotlib.pyplot as plt
from . import calculate_V_cor as Vc

def hydro_solver (source,P_start, pipe,fluid):
    pressures = [0]
    oil_flowrate = []
    water_flowrate = []
    gas_flowrate = []
    liq_flowrate = []
    holdups = []
    velocities = []
    # Инициализация текущего давления
    p_current = source['p'] * 14.7  # Перевод в расчетные единицы [psi]
    # Инициализация f_user
    f_user = 0.1  # Начальное значение, предназначен для автонастройки
    pipeline_range = list(range(0, pipe['length'], 10)) # Настройки дискретизации
    while pressures[-1] < P_start:  # Условие настройки
        # print( pressures[-1], "<" ,P_start,"=",pressures[-1] < P_start)
        pressures.clear()
        oil_flowrate.clear()
        water_flowrate.clear()
        gas_flowrate.clear()
        liq_flowrate.clear()
        holdups.clear()
        velocities.clear()
        for length in pipeline_range:
            grad, hold, muo, usl, sigl, qg, regime, usg, qo, qw, ql = BB.Pgrad(
                f_user,
                p_current,
                source['temp'] * (9 / 5) + 32,
                source['q'] * 6.2898 * (1 - fluid['wc']),
                source['q'] * 6.2898 * fluid['wc'],
                fluid['gor'] * 5.614583,
                fluid['gas_spgr'],
                141.5 / (fluid['api'] / 1000) - 131.5,
                1,
                pipe['diam'] * 0.0393701,
                pipe['angle']
            )

            if length == 0:
                pressures.append(source['p'])
            else:
                p_current = source['p'] * 14.7 + (grad * length * (1 / 0.3048))
                p_current1 = p_current * 0.068046
                pressures.append(p_current1)
            # print(qg)
            Fr_cr = ac.Frudo_critical(fluid['wc'], (qg / (qg + source['q'] * 6.2898 * (1 - fluid['wc']))))
            v_cr = ac.check_anticoorosion_compliance(
                muo,
                Fr_cr,
                pipe['diam'],
                fluid['wc'] * 1000 / (fluid['wc'] * 1000 + (1 - fluid['wc']) * 870),
                (qg / (qg + source['q'] * (1 - fluid['wc']))),
                fluid['api'],
                sigl
            )

            holdups.append(hold * 100)
            velocities.append(usl*0.3048)
            gas_flowrate.append(qg)
            oil_flowrate.append(qo)
            water_flowrate.append(qw)
            liq_flowrate.append(ql)

        # Увеличение f_user
        f_user += 0.1

    # Сглаживание данных
    def smooth_data(data, window_size): #функция для сглаживания графиков
        # print(data)
        return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

    window_size = 10  # Размер окна для скользящего среднего

    smoothed_pressures = smooth_data(pressures, window_size)
    smoothed_oil_flowrate = smooth_data(oil_flowrate, window_size)
    smoothed_water_flowrate = smooth_data(water_flowrate, window_size)
    smoothed_gas_flowrate = smooth_data(gas_flowrate, window_size)
    smoothed_liq_flowrate = smooth_data(liq_flowrate, window_size)
    smoothed_velocities = smooth_data(velocities, window_size)

    # выводить на прод (y)
    # print(len(pressures))
    # print("gg", len(pressures))
    # print("dd",pipe['length'])
    # Cловарь, в котором будут храниться средние значения
    # average_values = {
    #     'Средний газовый расход': sum(smoothed_gas_flowrate) / len(smoothed_gas_flowrate),
    #     # 
    #     'Макс газовай расход': max(smoothed_gas_flowrate),
    #     'Мин газовай расход': min(smoothed_gas_flowrate),
    #     'Средний нефтяной расход': sum(smoothed_oil_flowrate) / len(smoothed_oil_flowrate),
    #     'Средний водяной расход': sum(smoothed_water_flowrate) / len(smoothed_water_flowrate),
    #     'Средний расход жидкости': sum(smoothed_liq_flowrate) / len(smoothed_liq_flowrate),
    #     'Среднее давление': sum(smoothed_pressures) / len(smoothed_pressures),
    #     'Средняя скорость': sum(smoothed_velocities) / len(smoothed_velocities),
    #     # 'Давление графикY' : pressures,
    #     # 'Давление графикX': [i for i in range(0, pipe["length"] + 1, int(pipe['length']/len(pressures)))],
    #     'pressures_chare': list(zip([i for i in range(0, pipe["length"] + 1, int(pipe['length']/len(pressures)))],pressures)),
    #     'Средний нефтяной расходY' : oil_flowrate,
    #     'Средний нефтяной расходX': [i for i in range(0, pipe["length"] + 1, int(pipe['length']/len(oil_flowrate)))],
    #     'Режим течения': regime
    # }

    chart_f = lambda param : list(zip([i for i in range(0, pipe["length"] + 1, int(pipe['length']/len(param)))],param))
    average_values = {
        'Средний газовый расход': sum(smoothed_gas_flowrate) / len(smoothed_gas_flowrate),
        'Макс газовай расход': max(smoothed_gas_flowrate),
        'Мин газовай расход': min(smoothed_gas_flowrate),
        'Газ chart': chart_f(gas_flowrate),

        'Средний нефтяной расход': sum(smoothed_oil_flowrate) / len(smoothed_oil_flowrate),
        'Макс нефтяной расход': max(smoothed_oil_flowrate),
        'Мин нефтяной расход': min(smoothed_oil_flowrate),
        'Нефть chart': chart_f(oil_flowrate),

        'Средний водяной расход': sum(smoothed_water_flowrate) / len(smoothed_water_flowrate),
        'Макс водяной расход': max(smoothed_water_flowrate),
        'Мин водяной расход': min(smoothed_water_flowrate),
        'Вода chart': chart_f(water_flowrate),

        'Средний расход жидкости': sum(smoothed_liq_flowrate) / len(smoothed_liq_flowrate),
        'Макс расход жидкости': max(smoothed_liq_flowrate),
        'Мин расход жидкости': min(smoothed_liq_flowrate),
        'Жидкость chart': chart_f(liq_flowrate),

        'Среднее давление': sum(smoothed_pressures) / len(smoothed_pressures),
        'Макс давление': max(smoothed_pressures),
        'Мин давление': min(smoothed_pressures),
        'Давление chart': chart_f(pressures),

        'Средняя скорость': sum(smoothed_velocities) / len(smoothed_velocities),
        'Макс скорость': max(smoothed_velocities),
        'Мин скорость' : min(smoothed_velocities),
        'Скорость chart': chart_f(velocities),


        # # 'Давление графикY' : pressures,
        # # 'Давление графикX': [i for i in range(0, pipe["length"] + 1, int(pipe['length']/len(pressures)))],
        # 'Давление chart': chart_f(pressures),
        
        # 'Задержка chart': chart_f(holdups),
        
        # 'Средний нефтяной chart': [i for i in range(0, pipe["length"] + 1, int(pipe['length']/len(oil_flowrate)))],
        'Режим течения': regime,
        'Критическая скорость': v_cr,
    }

    water_comp = dict(CL=19.104, HCO3=134, Ca=406, pH=7.7)
    v_corr=Vc.calculate_V_cor(water_comp['CL'],water_comp['HCO3'],water_comp['Ca'],water_comp['pH'], average_values['Средняя скорость'], v_cr, average_values['Среднее давление'],pipe['diam'])
    # print(v_corr)

    average_values['Максимальная скорость коррозии']= v_corr

    # Вывод средних значений
    # for key, value in average_values.items():
    #     print(key + ':', value)
    return average_values

if __name__ == "__main__":

    # Параметры для расчета/ тест расчета
    source = dict(p=10, q=1000, temp=15)  # P - Давление в конце трубопровода, q - расход жидкости, temp - Температура в конце трубопровода

    #P_0
    P_start = 30  # Давление в начале трубопровода

    #construct (lenth_m)
    pipe = dict(length=1000, angle=0, diam=100)  # Длина трубопровода, угол наколна, внутренний диаметр (мм)

    #вкладка PVT (api) вкладка W_cut (wc)(занулсять ) gor (gor) PVT gas_sqgr()
    fluid = dict(api=870, wc=0.4, gor=50, gas_spgr=0.64)  # Плотность нефти, обводненность, газовый фактор, относительная плотность газа

    a=hydro_solver(source,P_start,pipe,fluid)








#
#
# Создаем окно с несколькими графиками
# fig, axs = plt.subplots(3, 1, figsize=(10, 15))
#
# График скорости
#
# axs[0].plot(pipeline_range[:len(smoothed_velocities)], smoothed_velocities, label='Сглаженная скорость', linestyle='--')
# axs[0].set_xlabel('Длина трубопровода (футы)')
# axs[0].set_ylabel('Скорость')
# axs[0].legend()
# axs[0].set_title('Скорость вдоль трубопровода')
# axs[0].grid(True)
#
# График давления
#
# axs[1].plot(pipeline_range[:len(smoothed_pressures)], smoothed_pressures, label='Сглаженное давление', linestyle='--')
# axs[1].set_xlabel('Длина трубопровода (футы)')
# axs[1].set_ylabel('Давление')
# axs[1].legend()
# axs[1].set_title('Давление вдоль трубопровода')
# axs[1].grid(True)
#
# # График скорости
#
# axs[2].plot(pipeline_range[:len(smoothed_liq_flowrate)], smoothed_liq_flowrate, label='Сглаженный расход жидкости', linestyle='--')
# axs[2].set_xlabel('Длина трубопровода (футы)')
# axs[2].set_ylabel('Расход')
# axs[2].set_ylim(0, 10)
# axs[2].legend()
# axs[2].set_title('Жидкость')
# axs[2].grid(True)
#
# # Отображаем все графики в одном окне
# plt.tight_layout()
# plt.show()
