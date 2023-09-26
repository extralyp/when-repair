import pandas as pd
import os
from collections import namedtuple
import pickle


def load_data_pic(path_file=os.path.join(os.getcwd(),'server_memory','src','data_2019.pickle')):
    with open(path_file, 'rb') as f:
        data_pic = pickle.load(f)
    return data_pic


data_pic_2019 = load_data_pic()

DATA_Pickle = {
    2014 : load_data_pic(os.path.join(os.getcwd(),'server_memory','src','data_2014.pickle')),
    2015 : load_data_pic(os.path.join(os.getcwd(),'server_memory','src','data_2015.pickle')),
    2016 : load_data_pic(os.path.join(os.getcwd(),'server_memory','src','data_2016.pickle')),
    2017 : load_data_pic(os.path.join(os.getcwd(),'server_memory','src','data_2017.pickle')),
    2018 : load_data_pic(os.path.join(os.getcwd(),'server_memory','src','data_2018.pickle')),
    2019 : load_data_pic(os.path.join(os.getcwd(),'server_memory','src','data_2019.pickle')),
    2020 : load_data_pic(os.path.join(os.getcwd(),'server_memory','src','data_2020.pickle')),
    2021 : load_data_pic(os.path.join(os.getcwd(),'server_memory','src','data_2021.pickle')),
    2022 : load_data_pic(os.path.join(os.getcwd(),'server_memory','src','data_2022.pickle')),
    2023 : load_data_pic(os.path.join(os.getcwd(),'server_memory','src','data_2023.pickle')),
}

# df_oil = pd.read_excel("./src/config.xlsx", sheet_name="oil")
path_config = os.path.join(os.getcwd(), 'server_memory','src','config.xlsx')

sheets = ["coord", "PVT", "construct", "oil","liq","w_cut","gas", "gor", "T_0","T_1","P_0","P_1"]
data_s = namedtuple("data",sheets)

sheet_year  =   namedtuple("sheet_year",    
                ["key_name",    "view_column",  "df",])

sheet_point =   namedtuple("sheet_point",   
                ["key_name",  "col_x", "col_y",  "view_column",  "df",])

sheet_PVT =   namedtuple("sheet_PVT",   
                ["key_name", "col_api", "col_gas_spgr", "view_column",  "df",])

sheet_construct =   namedtuple("sheet_param",   
                ["key_name", "col_diam", "col_length", "col_angle", "view_column",  "df",])

loadConfig = lambda sheet_name: pd.read_excel(path_config, sheet_name=sheet_name).fillna(0)

DATA = data_s(
    #   sheet_point
    coord=  sheet_point(key_name="coord", col_x="X", col_y="Y", view_column=["points", "X", "Y"],                                       
    df=loadConfig("coord")),

    #   sheet_param
    PVT=    sheet_PVT(key_name="PVT", col_api="oil_grav, kg/m3 (api)",  col_gas_spgr="gas_grav (gas_spgr)", view_column=["pipes", "oil_grav, kg/m3 (api)", "wtr_grav", "gas_grav (gas_spgr)"],    
    df=loadConfig("PVT")),

    construct=  sheet_construct(key_name="construct", col_diam="diam, mm", col_length="length, m", col_angle="angle, grad", view_column=["pipes", "diam, mm", "thickness, mm", "length, m", "angle, grad"], 
    df=loadConfig("construct")),

    #   sheet_year
    oil=    sheet_year(key_name="oil",          view_column=["pipes/oil_t_day"], 
    df=loadConfig(sheet_name="oil")),
    liq=    sheet_year(key_name="liq",          view_column=["pipes/liq_m3_day"], 
    df=loadConfig("liq (q)")),
    w_cut=  sheet_year(key_name="w_cut",        view_column=["pipes/w_cut_vol"], 
    df=loadConfig("w_cut (wc)")),
    gas=    sheet_year(key_name="gas",          view_column=["pipes/gas_m3_day"], 
    df=loadConfig("gas")),
    gor=    sheet_year(key_name="gor",          view_column=["pipes/gas_m3_day"], 
    df=loadConfig("gor")),
    T_0=    sheet_year(key_name="T_0",          view_column=["pipes/temp C"], 
    df=loadConfig("T_0")),
    T_1=    sheet_year(key_name="T_1",          view_column=["pipes/temp C"], 
    df=loadConfig("T_1 (temp)")),
    P_0=    sheet_year(key_name="P_0",          view_column=["pipes/press atm"], 
    df=loadConfig("P_0")),
    P_1=    sheet_year(key_name="P_1",          view_column=["pipes/press atm"],
    df=loadConfig("P_1 (p)")),
)

def get_data_info_pipe_POINT():
    request_dict = {
        DATA.coord.key_name : DATA.coord.df[DATA.coord.view_column].to_dict()
    }
    return request_dict

def get_data_info_pipe_PARAM():
    request_dict = {
        DATA.PVT.key_name : DATA.PVT.df[DATA.PVT.view_column].to_dict(),
        DATA.construct.key_name : DATA.construct.df[DATA.construct.view_column].to_dict()
        }

    return  request_dict

def get_data_info_pipe_YEAR(year=None):
    request_dict = {}
    for sheet in DATA:
        if "sheet_year" in type(sheet).__name__:
            print(sheet is sheet_year)
        # if type(sheet) == sheet_year:
            print(sheet.key_name)
            if year == None:
                request_dict[sheet.key_name]=sheet.df.to_dict()
            
            if year != None:
                request_dict[sheet.key_name]=sheet.df[sheet.view_column + [year]].to_dict()

    return request_dict

def get_result_year_PICKLE(year=None):
    return DATA_Pickle[year]

# def get_data_info_pipe_year(year):
#     years_result = {
#         "oil": DATA.oil.df[DATA.oil.view_column + [year]].to_dict(),
#         "liq": DATA.liq.df[DATA.liq.view_column + [year]].to_dict(),
#         "w_cut": DATA.w_cut.df[DATA.w_cut.view_column + [year]].to_dict(),
#         "gas": DATA.gas.df[DATA.gas.view_column + [year]].to_dict(),
#         "T_0": DATA.T_0.df[DATA.T_0.view_column + [year]].to_dict(),
#         "T_1": DATA.T_1.df[DATA.T_1.view_column + [year]].to_dict(),
#         "P_0": DATA.P_0.df[DATA.P_0.view_column + [year]].to_dict(),
#         "P_1": DATA.P_1.df[DATA.P_1.view_column + [year]].to_dict(),
#     }
#     return years_result

# async def get_info_pipe_year(year):
#     return df[[str(year) + ".7"]].to_dict()

if __name__ == "__main__":
    # print(get_info_pipe_year(2014))
    print(get_data_info_pipe_POINT())
    print(get_data_info_pipe_PARAM())
    print(get_data_info_pipe_YEAR(2014))