from server_memory.memory_DF import DATA, DATA_Pickle
from pipe_function.pipe_factory_request import get_pipe_field_model, SOURCE, PIPE, FLUID
from models.model_pipe_info import PipesFieldModel, PipeFieldParamModel, Response_AllInfoPipeYearModel
import pandas as pd
import pickle
from tool_color.gradient import get_colore_gradient
from calculate_V_cor import calculate_V_cor

VALUE_MIN = 0.000000001

# get_pipe_field_model(
#         Source=SOURCE(p=10, q=1000, temp=15),
#         Pipe=PIPE(length=1000, angle=0, diam=100),
#         Fluid=FLUID(api=870, wc=0.4, gor=50, gas_spgr=0.64),
#         P_start=30
#     )

def Get_Response_AllInfoPipeYearModel(year=2019):
    get_df_year_l = lambda DataSheet : DataSheet.df[DataSheet.view_column + [year]]
    rename_df_year_l = lambda DataSheet, df_year, param_name :  df_year.rename(columns={DataSheet.view_column[0]: "pipe", year: param_name})

    # get_rename_col_pipe_l = lambda DataSheet:  DataSheet.df[DataSheet.view_column].rename(columns={DataSheet.view_column[0]: "pipe"})
    
    def get_df_year(data_sheet, param_name):
        df = get_df_year_l(data_sheet)
        df = rename_df_year_l(data_sheet, df, param_name)
        return df
    # df_p = DATA.P_1.df[DATA.P_1.view_column + [year]]
    # df_p = get_df_year(DATA.P_1)
    # df_p = df_p.rename(columns={DATA.P_1.view_column[0]: "pipe", year: "p"})
    # df_p = rename_df_year(DATA.P_1, df_p, "p")
    df_p = get_df_year(DATA.P_1, "p")
    df_p.loc[(df_p["p"] <= 0), "p"] = VALUE_MIN

    df_temp = get_df_year(DATA.T_1, "temp")
    df_temp.loc[(df_temp["temp"] <= 0), "temp"] = VALUE_MIN
    
    df_temp_start = get_df_year(DATA.T_0, "temp_start")
    df_temp_start.loc[(df_temp_start["temp_start"] <= 0), "temp_start"] = VALUE_MIN


    df_q = get_df_year(DATA.liq, "q")
    df_q.loc[(df_q["q"] <= 0), "q"] = VALUE_MIN

    df_gor = get_df_year(DATA.gor, "gor") 
    df_gor.loc[(df_gor["gor"] <= 0), "gor"] = VALUE_MIN

    df_P_start = get_df_year(DATA.P_0, "P_start")
    df_P_start.loc[(df_P_start["P_start"] <= 0), "P_start"] = VALUE_MIN

    df_wc = get_df_year(DATA.w_cut, "wc")
    #зануление значения меньше нуля по колонке года
    df_wc.loc[(df_wc["wc"] <= 0), "wc"] = VALUE_MIN

    df_lenght_angle_diam =  DATA.construct.df[DATA.construct.view_column]
    df_lenght_angle_diam = df_lenght_angle_diam.rename(columns={
        DATA.construct.view_column[0]: "pipe", DATA.construct.col_length: "length", DATA.construct.col_angle:"angle", DATA.construct.col_diam:"diam"})
    # df_lenght_angle_diam = get_rename_col_pipe_l(DATA.construct)

    df_api_gas_sqgr = DATA.PVT.df[DATA.PVT.view_column]
    df_api_gas_sqgr = df_api_gas_sqgr.rename(columns={DATA.PVT.view_column[0]: "pipe", DATA.PVT.col_api:"api",  DATA.PVT.col_gas_spgr: "gas_spgr"})
    # df_api_gas_sqgr = get_rename_col_pipe_l(DATA.PVT)

    merge_df = df_p
    list_df_merge = [df_temp, df_q, df_gor, df_P_start, df_wc, df_lenght_angle_diam, df_api_gas_sqgr, df_temp_start]
    # , df_q, df_gor, df_P_start, df_wc
    # merge_df = pd.concat([df_p, df_temp], axis=1)
    count=0
    for df in list_df_merge:
        # merge_df = pd.merge(merge_df, df, how='left',  on=['pipe'], validate='many_to_one')
        merge_df = merge_df.join(df, rsuffix=f'_add_{count}')
        count +=1


    return merge_df

def build_to_dict_field(save_model:Response_AllInfoPipeYearModel, name_pipe:str, funct_res):
    save_model.mean_gas_exp.mean_stats[name_pipe] = funct_res['Средний газовый расход']
    save_model.mean_gas_exp.max_stats[name_pipe] = funct_res['Макс газовай расход']
    save_model.mean_gas_exp.min_stats[name_pipe] = funct_res['Мин газовай расход']
    save_model.mean_gas_exp.chart[name_pipe] = funct_res['Газ chart']

    save_model.mean_oil_exp.mean_stats[name_pipe] = funct_res['Средний нефтяной расход']
    save_model.mean_oil_exp.max_stats[name_pipe] = funct_res['Макс нефтяной расход']
    save_model.mean_oil_exp.min_stats[name_pipe] = funct_res['Мин нефтяной расход']
    save_model.mean_oil_exp.chart[name_pipe] = funct_res['Нефть chart']

    save_model.mean_wat_exp.mean_stats[name_pipe] = funct_res['Средний водяной расход']
    save_model.mean_wat_exp.max_stats[name_pipe] = funct_res['Макс водяной расход']
    save_model.mean_wat_exp.min_stats[name_pipe] = funct_res['Мин водяной расход']
    save_model.mean_wat_exp.chart[name_pipe] = funct_res['Вода chart']

    save_model.mean_liq_exp.mean_stats[name_pipe] = funct_res['Средний расход жидкости']
    save_model.mean_liq_exp.max_stats[name_pipe] = funct_res['Макс расход жидкости']
    save_model.mean_liq_exp.min_stats[name_pipe] = funct_res['Мин расход жидкости']
    save_model.mean_liq_exp.chart[name_pipe] = funct_res['Жидкость chart']

    save_model.mean_p.mean_stats[name_pipe] = funct_res['Среднее давление']
    save_model.mean_p.max_stats[name_pipe] = funct_res['Макс давление']
    save_model.mean_p.min_stats[name_pipe] = funct_res['Мин давление']
    save_model.mean_p.chart[name_pipe] = funct_res['Давление chart']

    save_model.mean_speed.mean_stats[name_pipe] = funct_res['Средняя скорость']
    save_model.mean_speed.max_stats[name_pipe] = funct_res['Макс скорость']
    save_model.mean_speed.min_stats[name_pipe] = funct_res['Мин скорость']
    save_model.mean_speed.chart[name_pipe] = funct_res['Скорость chart']

    save_model.mean_temp_exp.mean_stats[name_pipe] = funct_res['Средняя температура']
    save_model.mean_temp_exp.max_stats[name_pipe] = funct_res['Макс температура']
    save_model.mean_temp_exp.min_stats[name_pipe] = funct_res['Мин температура']
    save_model.mean_temp_exp.chart[name_pipe] = funct_res['Teмпература chart']

    save_model.mode.mean_stats[name_pipe] = funct_res['Режим течения']
    save_model.v_crit.mean_stats[name_pipe] = funct_res['Критическая скорость']
    
    return save_model

def build_gradient_field(save_model:Response_AllInfoPipeYearModel):
    print(save_model.mean_gas_exp.mean_stats)
    save_model.mean_gas_exp.gradient, save_model.mean_gas_exp.max_grad, save_model.mean_gas_exp.min_grad = get_colore_gradient(save_model.mean_gas_exp.mean_stats)
    save_model.mean_oil_exp.gradient, save_model.mean_oil_exp.max_grad, save_model.mean_oil_exp.min_grad= get_colore_gradient(save_model.mean_oil_exp.mean_stats)
    save_model.mean_wat_exp.gradient, save_model.mean_wat_exp.max_grad, save_model.mean_wat_exp.min_grad = get_colore_gradient(save_model.mean_wat_exp.mean_stats)
    save_model.mean_liq_exp.gradient, save_model.mean_liq_exp.max_grad, save_model.mean_liq_exp.min_grad = get_colore_gradient(save_model.mean_liq_exp.mean_stats)
    save_model.mean_p.gradient, save_model.mean_p.max_grad, save_model.mean_p.min_grad = get_colore_gradient(save_model.mean_p.mean_stats)
    save_model.mean_speed.gradient, save_model.mean_speed.max_grad, save_model.mean_speed.min_grad = get_colore_gradient(save_model.mean_speed.mean_stats)
    save_model.mean_temp_exp.gradient, save_model.mean_temp_exp.max_grad, save_model.mean_temp_exp.min_grad = get_colore_gradient(save_model.mean_temp_exp.mean_stats)

    save_model.mode.gradient, save_model.mode.max_grad, save_model.mode.min_grad = get_colore_gradient(save_model.mode.mean_stats, revers=True)

    save_model.v_crit.gradient, save_model.v_crit.max_grad, save_model.v_crit.min_grad = get_colore_gradient(save_model.v_crit.mean_stats)

    return save_model

def calculate_pipe_year(year):
    save_model = Response_AllInfoPipeYearModel()
    save_model.result = True

    df = Get_Response_AllInfoPipeYearModel(year)
    for index, row in df.iterrows():

        if (row["pipe"]) in ["G1-C2/D2", "G8-G1", "D3-D2"]:
            print("---add Pipe bb---")
            continue

        if (row["pipe"]) in ["C3/E-X4"] :
            print("---add Hz ---")
            continue
        # row_p = row.p
        # row_temp = row.temp
        if row.q == VALUE_MIN or row.p == VALUE_MIN:
            print("---add Zero result value---")
            continue
        
        
            # row_q = 0
            # row_p = 0
            # row_temp = 0

        print(index, row["pipe"])
        print(SOURCE(p=row.p, q=row.q, temp=row.temp), PIPE(length=row.length, angle= row.angle, diam= row.diam), FLUID(api=row.api, wc=row.wc, gor=row.gor, gas_spgr=row.gas_spgr) , row.P_start)
        res_fuc = get_pipe_field_model(
            Source=SOURCE(p=row.p, q=row.q, temp=row.temp),
            Pipe=PIPE(length=row.length, angle= row.angle, diam= row.diam),
            Fluid=FLUID(api=row.api, wc=row.wc, gor=row.gor, gas_spgr=row.gas_spgr),
            P_start=row.P_start
            )
        
        mean_temp_k = ((row.temp_start/ row.P_start) + (row.temp / row.p)) / 2
        # res_fuc["Средняя температура"] = mean_temp_k # 
        res_fuc["Teмпература chart"] = [(x, y * mean_temp_k) for x, y in res_fuc["Давление chart"]]
        smooth_Temp = [ i[1] for i in res_fuc["Teмпература chart"]]
        res_fuc["Средняя температура"] = sum(smooth_Temp)/ len(res_fuc["Teмпература chart"])
        # res_fuc["Макс температура"] = res_fuc["Макс давление"] * mean_temp_k
        # res_fuc["Макс температура"] = res_fuc["Teмпература chart"][-1][1]
        res_fuc["Макс температура"] = max(smooth_Temp)
        # res_fuc["Мин температура"] = res_fuc["Мин давление"] * mean_temp_k
        res_fuc["Мин температура"] = min(smooth_Temp)

        if year >= 2020 and (row["pipe"] in ['G7-G5','G5-G3','G3-G4','G4-G9','G9-D3','D3-D2','D2-EZ3','D3-G1','D1/10-D2','D6-D2','B6-J1','J3-J2','J2-K6','K6-K3','F1-D14','D14-D9','D9-Z3','Y2-G8','G8-G1','G1-D2','Z1-J2','A-B4','B4-B5','B5-J1','J1-K-6',]):
            res_fuc["Максимальная скорость коррозии"] = 0.035 + 0.065

        print(res_fuc)
        # print(type(res_fuc))
        save_model= build_to_dict_field(save_model=save_model, name_pipe=row["pipe"], funct_res= res_fuc)
        
        
        # print("---add result value---")
        # print(save_model)
        # break
        # print(row["pipe"])
    
    # save_model= build_gradient_field(save_model=save_model)
    with open(f'data_{year}.pickle', 'wb') as f:
            pickle.dump(save_model, f)
    

def loadPic():
    print(DATA_Pickle[2023].v_crit.gradient)
    
    # for key, value in DATA_Pickle[2021].v_crit.mean_stats.items():
    #     if type(value) == complex:
    #         print(key, type(value))

# # 'C3/E-C2/E'
    # DATA_Pickle[2023].v_crit.mean_stats['B3-J2'] = 0
    
    # save_model = DATA_Pickle[2021]
    # save_model.v_crit.gradient, save_model.v_crit.max_grad, save_model.v_crit.min_grad = get_colore_gradient(save_model.v_crit.mean_stats)
    # save_model =build_gradient_field(save_model)
    # with open(f'data_2021.pickle', 'wb') as f:
    #         pickle.dump(save_model, f)
    # mean_speed: Union[PipesFieldModel, None] = PipesFieldModel()
    # mean_p: Union[PipesFieldModel, None] = PipesFieldModel()
    # mean_liq_exp: Union[PipesFieldModel, None] = PipesFieldModel()
    # mean_gas_exp: Union[PipesFieldModel, None] = PipesFieldModel()
    # mean_wat_exp: Union[PipesFieldModel, None] = PipesFieldModel()
    # mean_oil_exp: Union[PipesFieldModel, None] = PipesFieldModel()
    # mean_temp_exp : Union[PipesFieldModel, None] = PipesFieldModel()
    # mode: Union[PipeFieldParamModel, None] = PipeFieldParamModel()
    # v_crit: Union[PipeFieldParamModel, None] = PipeFieldParamModel()
def pp():
    dd = Response_AllInfoPipeYearModel()
    dd.mean_speed.max_stats = {"ss":44}
    dd.mean_speed.max_stats["ff"] = 55
    print(dd)

pipe_dict = {
 'D8-D4': 0,
 'D4-C3/E': 0,
 'C3/E-X4': 0,
 'C3/E-C2/E': 0,
 'H7/D14-C3/E': 0,
 'H7/D14-D9': 0,
 'D9-C3': 0,
 'D20-C3': 0,
 'D6-C3': 0,
 'D6-C2/D2': 0,
 'D1/10-C2/D2': 0,
 'D5-C2/D2': 0,
 'C2/D2-I3/E': 0,
 'G1-C2/D2': 0,
 'C2/D2-G1': 0,
 'D3-D2': 0,
 'D3-G1': 0,
 'D2-D3': 0,
 'G9-D3': 0,
 'G8-G9': 0,
 'G8-G1': 0,
 'G1-G8': 0,
 'Y2-G8': 0,
 'G10-G9': 0,
 'G10-G5': 0,
 'G4-G8': 0,
 'D15-G10': 0,
 'G7-G5': 0,
 'G5-G3': 0,
 'G3-G4': 0,
 'G4-G9': 0,
 'G6-G4': 0,
 'Y1-G6': 0,
 'K-G-6': 0,
 'D19-K': 0,
 'D21-K': 0,
 'F1-D14': 0,
 'D16-D14': 0,
 'A-B4': 0,
 'B4-B5': 0,
 'B5-J1': 0,
 'B6-J1': 0,
 'J1-KX6': 0,
 'J1-KX3': 0,
 'Z1-J2': 0,
 'J2-KX3/X6': 0,
 'B3-J2': 0,
 'J3-J2': 0
 }

  
pipe_dict_proch = {
 'D8-D4': 0,
 'D4-C3/E': 0,
 'C3/E-X4': 0,
 'C3/E-C2/E': 0,
 'H7/D14-C3/E': 0,
 'H7/D14-D9': 0,
 'D9-C3': 0,
 'D20-C3': 0,
 'D6-C3': 0,
 'D6-C2/D2': 0,
 'D1/10-C2/D2': 0,
 'D5-C2/D2': 0,
 'C2/D2-I3/E': 0,
 'G1-C2/D2': 0,
 'C2/D2-G1': 0,
 'D3-D2': 0,
 'D3-G1': 0,
 'D2-D3': 0,
 'G9-D3': 0,
 'G8-G9': 0,
 'G8-G1': 0,
 'G1-G8': 0,
 'Y2-G8': 0,
 'G10-G9': 0,
 'G10-G5': 0,
 'G4-G8': 0,
 'D15-G10': 0,
 'G7-G5': 0,
 'G5-G3': 0,
 'G3-G4': 0,
 'G4-G9': 0,
 'G6-G4': 0,
 'Y1-G6': 0,
 'K-G-6': 0,
 'D19-K': 0,
 'D21-K': 0,
 'F1-D14': 0,
 'D16-D14': 0,
 'A-B4': 0,
 'B4-B5': 0,
 'B5-J1': 0,
 'B6-J1': 0,
 'J1-KX6': 0,
 'J1-KX3': 0,
 'Z1-J2': 0,
 'J2-KX3/X6': 0,
 'B3-J2': 0,
 'J3-J2': 0
 }


def get_cor(mean_speed_pipe, maen_p_pipe, cryt_speed):
    water_comp = dict(CL=19.104, HCO3=134, Ca=406, pH=7.7)
    # v_corr=Vc.calculate_V_cor(water_comp['CL'],water_comp['HCO3'],water_comp['Ca'],water_comp['pH'], average_values['Средняя скорость'], v_cr, average_values['Среднее давление'], 354)
    v_corr=calculate_V_cor(water_comp['CL'],water_comp['HCO3'],water_comp['Ca'],water_comp['pH'], mean_speed_pipe, cryt_speed, maen_p_pipe, 354)
    return v_corr

def re_save_picle():
    # print(get_cor(1,2,3))
    result_year = {}
    result_pipe = {}
    for name_year in DATA_Pickle:
        for pipe_name in pipe_dict:
            mean_speed_pipe=DATA_Pickle[name_year].mean_speed.mean_stats.get(pipe_name, 0)
            maen_p_pipe=DATA_Pickle[name_year].mean_p.mean_stats.get(pipe_name, 0)
            cryt_speed=DATA_Pickle[name_year].v_crit.mean_stats.get(pipe_name, 0)
            print(mean_speed_pipe, maen_p_pipe, cryt_speed)
            if mean_speed_pipe == 0 or mean_speed_pipe == 0 or mean_speed_pipe == 0:
                result_pipe[pipe_name] = 0
            else:
                print(get_cor(mean_speed_pipe=mean_speed_pipe ,maen_p_pipe=maen_p_pipe ,cryt_speed=cryt_speed))
                result_pipe[pipe_name] = get_cor(mean_speed_pipe=mean_speed_pipe ,maen_p_pipe=maen_p_pipe ,cryt_speed=cryt_speed)
        result_year[name_year] = result_pipe
        result_pipe = {}
    # print(result_year)
    return result_year

def create_chart():
    # DATA_Pickle[2015].v_crit.gradient
    # DATA_Pickle[2016].v_crit.gradient
    # DATA_Pickle[2023].v_crit.gradient
    # DATA_Pickle[2023].v_crit.gradient
    # DATA_Pickle[2023].v_crit.gradient
    # DATA_Pickle[2023].v_crit.gradient
    corr_year_dict = re_save_picle()
    print(corr_year_dict)
    # res ={}
    # print(len(pipe_dict))
    for name_year, data_year in DATA_Pickle.items():
        print(name_year)
        print(data_year.v_crit.mean_stats)

        corr_pipe = corr_year_dict[name_year]
        print(corr_pipe)

        for key, value in data_year.v_crit.mean_stats.items():
            
            # pipe_dict_proc[key] += ((corr_pipe[key] + 0.7) / 17.2) * 100
            # pipe_dict[key] += ((corr_pipe[key] + 0.7) / 17.2) * 100
            pipe_dict[key] += corr_pipe[key] + 0.7
            # pipe_dict[key] +=  (17.2 - (corr_pipe[key] + 0.7 )) / 0.55

    
    # return pipe_dict
    for key, value in pipe_dict.items():
        pipe_dict[key] = (17.2 - (pipe_dict[key])) / 0.55

    # print(pipe_dict)
    return pipe_dict, get_colore_gradient(pipe_dict, revers=True)

def create_chart_proch():
    # DATA_Pickle[2015].v_crit.gradient
    # DATA_Pickle[2016].v_crit.gradient
    # DATA_Pickle[2023].v_crit.gradient
    # DATA_Pickle[2023].v_crit.gradient
    # DATA_Pickle[2023].v_crit.gradient
    # DATA_Pickle[2023].v_crit.gradient
    corr_year_dict = re_save_picle()
    print(corr_year_dict)
    # res ={}
    # print(len(pipe_dict))
    for name_year, data_year in DATA_Pickle.items():
        print(name_year)
        print(data_year.v_crit.mean_stats)

        corr_pipe = corr_year_dict[name_year]
        print(corr_pipe)

        for key, value in data_year.v_crit.mean_stats.items():
            
            # pipe_dict_proc[key] += ((corr_pipe[key] + 0.7) / 17.2) * 100
            pipe_dict_proch[key] += ((corr_pipe[key] + 0.7) / 17.2) * 100
            # pipe_dict[key] += corr_pipe[key] + 0.7
            # pipe_dict[key] +=  (17.2 - (corr_pipe[key] + 0.7 )) / 0.55

    print(pipe_dict_proch)
    return pipe_dict_proch
    # for key, value in pipe_dict.items():
    #     pipe_dict[key] = (17.2 - (pipe_dict[key])) / 0.55

    # print(pipe_dict)
    


    

    



        


if __name__ == "__main__":
    # print(Get_Response_AllInfoPipeYearModel())
    # calculate_pipe_year(2015)
    # calculate_pipe_year(2016)
    # calculate_pipe_year(2017)
    # calculate_pipe_year(2018)

    # calculate_pipe_year(2020)
    # calculate_pipe_year(2021)

    # calculate_pipe_year(2022)
    # calculate_pipe_year(2023)
    # print(pp())]
    # loadPic()
    print(create_chart())
    # create_chart_proch()
    # re_save_picle()