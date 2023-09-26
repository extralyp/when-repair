
from pipe_function.pipe_factory_request import get_pipe_field_model, SOURCE, PIPE, FLUID
if __name__ == "__main__":
    # get_pipe_field_model(
    #     Source=SOURCE(p=10, q=1000, temp=15),
    #     Pipe=PIPE(length=1000, angle=0, diam=100),
    #     Fluid=FLUID(api=870, wc=0.4, gor=50, gas_spgr=0.64),
    #     P_start=30
    # )

    # ERROR
    # get_pipe_field_model(
    #     SOURCE(p=25, q=2656, temp=40.6), 
    #     PIPE(length=9530, angle=0, diam=323.8), 
    #     FLUID(api=858.87, wc=0.1087862575384495, gor=0.0000001, gas_spgr=0.64), 
    #     P_start=30
    # )

    # OK
    # get_pipe_field_model(
    # SOURCE(p=10.8, q=1835, temp=50.6), 
    # PIPE(length=9500, angle=0, diam=323.8), 
    # FLUID(api=858.87, wc=0.8343936423148228, gor=1e-09, gas_spgr=0.64), 
    # P_start=11.6
    # )

    # get_pipe_field_model(
    #     SOURCE(p=1e-09, q=1e-09, temp=1e-09), PIPE(length=1030, angle=0, diam=325.0), FLUID(api=858.87, wc=1e-09, gor=1e-09, gas_spgr=0.64), P_start=1e-09
    # )
    # get_pipe_field_model(
    #     SOURCE(p=1e-09, q=1e-09, temp=1e-09), PIPE(length=2760, angle=0, diam=426.0), FLUID(api=858.87, wc=1e-09, gor=1e-09, gas_spgr=0.64), P_start=7.4
    # )
    # 30 G1-C2/D2
    # get_pipe_field_model(
    #     SOURCE(p=1e-09, q=485.0, temp=1e-09), PIPE(length=2970, angle=0, diam=532.5), FLUID(api=858.87, wc=0.7935431583023438, gor=1e-09, gas_spgr=0.64), P_start=20.8
    # )
    # 17 C3/E - X4
# SOURCE(p=1e-09, q=1e-09, temp=1e-09) PIPE(length=2760, angle=0, diam=426.0) FLUID(api=858.87, wc=1e-09, gor=1e-09, gas_spgr=0.64) 7.4
    get_pipe_field_model(
    SOURCE(p=27.8, q=1798.0, temp=38.5), PIPE(length=2440, angle=0, diam=323.8), FLUID(api=858.87, wc=0.2073813312893097, gor=1e-09, gas_spgr=0.64), P_start=26.0
    )