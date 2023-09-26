from fastapi import APIRouter, Response

from tool_color.gradient import get_colore_gradient, test_grad

from models.model_pipe_info import Request_Test_InfoPipeYearModel, Response_Test_InfoPipeYearModel
from models.model_pipe_info import Request_Test_gradient, Response_Test_gradient
from models.model_pipe_info import Response_Dict
from models.model_pipe_info import Request_AllInfoPipeYearModel, Response_AllInfoPipeYearModel
from models.model_pipe_info import Response_life, PipeWearParam

from models.model_pipe_info import Request_Pipe, Response_Pipe

from server_memory.memory_DF import get_data_info_pipe_POINT, get_data_info_pipe_PARAM, get_data_info_pipe_YEAR, get_result_year_PICKLE
from build_data import create_chart, create_chart_proch

pipe_info = APIRouter()

@pipe_info.post(path="/point", response_model=Response_Dict, status_code=200)
def Test_info_pipe_POINT__view(response: Response):
    info_pipe = get_data_info_pipe_POINT()
    print(info_pipe)
    return Response_Dict(result=True, error="", info_pipe=info_pipe)

@pipe_info.post(path="/param", response_model=Response_Dict, status_code=200)
def Test_info_pipe_PARAM__view(response: Response):
    info_pipe = get_data_info_pipe_PARAM()
    print(info_pipe)
    return Response_Dict(result=True, error="", info_pipe=info_pipe)

@pipe_info.post(path="/year", response_model=Response_Test_InfoPipeYearModel, status_code=200)
def Test_info_pipe_YEAR__view(response: Response, requestBody: Request_Test_InfoPipeYearModel):
    if requestBody.year < 2014 or requestBody.year > 2023:
        response.status_code = 400
        return Response_Test_InfoPipeYearModel(result=False, error="Год должен быть между 2014 и 2023 включительно", info_pipe={})
    info_pipe = get_data_info_pipe_YEAR(requestBody.year)
    print(info_pipe)
    return Response_Test_InfoPipeYearModel(result=True, error="", info_pipe=info_pipe)

@pipe_info.post(path="/gradient", response_model=Response_Test_gradient, status_code=200)
def Test_gradient_view(response: Response, requestBody: Request_Test_gradient):
    if requestBody.year < 2014 or requestBody.year > 2023:
        response.status_code = 400
        return Response_Test_gradient(result=False, error="Год должен быть между 2014 и 2023 включительно", info_pipe={})
    gradient_dict = get_colore_gradient(test_grad)
    return Response_Test_gradient(result=True, error="",  gradient= gradient_dict)

@pipe_info.post(path="/all_info_year", response_model=Response_AllInfoPipeYearModel, status_code=200)
def all_info_pipe_year(response: Response, requestBody: Request_AllInfoPipeYearModel):
    if requestBody.year < 2014 or requestBody.year > 2023:
        response.status_code = 400
        return Response_Test_gradient(result=False, error="Год должен быть между 2014 и 2023 включительно", info_pipe={})
    Response_info_year_pipe = get_result_year_PICKLE(requestBody.year)
    return Response_info_year_pipe

# @pipe_info.post(path="/pipe", response_model=Response_Pipe, status_code=200)
# def info_pipe(response: Response, requestBody: Request_AllInfoPipeYearModel):
#     if requestBody.year < 2014 or requestBody.year > 2023:
#         response.status_code = 400

@pipe_info.post(path="/life_pipe", response_model=Response_life, status_code=200)
def life_pipe(response: Response):
    resp = PipeWearParam()
    resp.mean_stats, (resp.gradient, resp.max_grad, resp.min_grad) = create_chart()
    return Response_life(year_life=resp)

@pipe_info.post(path="/life_pipe_proc", response_model=Response_Dict, status_code=200)
def life_pipe_proc(response: Response):
    respDic = create_chart_proch()
    return Response_Dict(result=True, error="", info_pipe=respDic)

# import sys
# from typing import Annotated, Any, Union, Optional, Dict

# from fastapi import FastAPI, Body, WebSocket, Response
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from fastapi.encoders import jsonable_encoder
# from pydantic import BaseModel, Json