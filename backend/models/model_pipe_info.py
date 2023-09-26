from typing import Any, Union, Optional, Dict, List
from pydantic import BaseModel
#POIN standart
class Response_Dict(BaseModel):
    result: bool
    error: str
    info_pipe: Dict[Any, Any]

#YEAR
class Request_Test_InfoPipeYearModel(BaseModel):
    year: int

class Response_Test_InfoPipeYearModel(BaseModel):
    result: bool
    error: str
    info_pipe: Dict[Any, Any]
    # info_pipe: Dict[str, Dict[int, Any]]

class Request_Test_gradient(BaseModel):
    name: str
    year: int

class Response_Test_gradient(BaseModel):
    result: bool
    error: str
    gradient: Dict[str, str]

class Request_AllInfoPipeYearModel(BaseModel):
    year: int

class PipesFieldModel(BaseModel):
    # stats_in_tube: Dict[str,str] = None
    min_stats : Dict[str,float] = {}
    max_stats : Dict[str,float] = {}
    mean_stats: Dict[str, float] = {}
    gradient: Dict[str,str] = {}
    max_grad: float = 0
    min_grad: float = 0
    chart: Dict[str,List[List[float]]] = {}

class PipeFieldParamModel(BaseModel):
    mean_stats: Dict[str, float] = {}
    gradient: Dict[str,str] = {}
    max_grad: float = 0
    min_grad: float = 0

class PipeWearParam (BaseModel):
    mean_stats: Dict[str, float] = {}
    gradient: Dict[str,str] = {}
    max_grad: float = 0
    min_grad: float = 0
class Response_AllInfoPipeYearModel(BaseModel):
    result: bool = False
    error: str = ""
    mean_speed: Union[PipesFieldModel, None] = PipesFieldModel()
    mean_p: Union[PipesFieldModel, None] = PipesFieldModel()
    mean_liq_exp: Union[PipesFieldModel, None] = PipesFieldModel()
    mean_gas_exp: Union[PipesFieldModel, None] = PipesFieldModel()
    mean_wat_exp: Union[PipesFieldModel, None] = PipesFieldModel()
    mean_oil_exp: Union[PipesFieldModel, None] = PipesFieldModel()
    mean_temp_exp : Union[PipesFieldModel, None] = PipesFieldModel()
    mode: Union[PipeFieldParamModel, None] = PipeFieldParamModel()
    v_crit: Union[PipeFieldParamModel, None] = PipeFieldParamModel()

class Response_life(BaseModel):
    year_life: Union[PipeWearParam, None] = PipeWearParam()
class Request_Pipe(BaseModel):
    name: str
    year: int

class Response_Pipe(BaseModel):
    result: bool = False
    error: str = ""
    pipe_info: Dict[Any, Any]




    

