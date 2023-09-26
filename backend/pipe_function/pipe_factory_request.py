from pipe_function.v2_1.hydro_solver import hydro_solver
from collections import namedtuple
from server_memory.memory_DF import get_data_info_pipe_POINT

SOURCE = namedtuple("SOURCE", ["p", "q", "temp"])
PIPE = namedtuple("PIPE", ["length", "angle", "diam"])
FLUID = namedtuple("FLUID", ["api", "wc", "gor", "gas_spgr"])

def get_pipe_field_model(Source : SOURCE, Pipe: PIPE, Fluid: FLUID, P_start):
    # Параметры для расчета/ тест расчета
    source = dict(p=Source.p, q=Source.q, temp=Source.temp)  # P - Давление в конце трубопровода, q - расход жидкости, temp - Температура в конце трубопровода

    #P_0
    P_start = P_start  # Давление в начале трубопровода

    #construct (lenth_m)
    pipe = dict(length=Pipe.length, angle=Pipe.angle, diam=Pipe.diam)  # Длина трубопровода, угол наколна, внутренний диаметр (мм)

    #вкладка PVT (api) вкладка W_cut (wc)(занулсять ) gor (gor) PVT gas_sqgr()
    fluid = dict(api=Fluid.api, wc=Fluid.wc, gor=Fluid.gor, gas_spgr=Fluid.gas_spgr)  # Плотность нефти, обводненность, газовый фактор, относительная плотность газа

    res=hydro_solver(source,P_start,pipe,fluid)

    return res

# pipe_drop_down(
#     Source=SOURCE(p=10, q=1000, temp=15),
#     Pipe=PIPE(length=1000, angle=0, diam=100),
#     Fluid=FLUID(api=870, wc=0.4, gor=50, gas_spgr=0.64),
#     P_start=30
# )