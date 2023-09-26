from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from views.views_pipe_info import pipe_info

from views.websocket import ws


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:80",
    "http://localhost:8080",
    "http://10.107.21.15:8080",
    "http://10.107.21.15:8081",
    "https://10.107.21.15:8080",
    "http://192.168.56.60:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pipe_info, prefix="/pipe_info")
app.include_router(ws, prefix="/ws")

# app.include_router(novelroute, prefix="/novel")

# @app.post(path="/info_pipe_year", response_model=Response_InfoPipeYearModel, status_code=200)
# def pd(**kwargs):
#     return info_pipe_year(kwargs)

# @app.post(path="/info_pipe_year", response_model=Response_InfoPipeYearModel, status_code=200)
# def info_pipe_year(response: Response, requestBody: Request_InfoPipeYearModel):
#     if requestBody.year < 2014 or requestBody.year > 2023:
#         response.status_code = 400
#         return Response_InfoPipeYearModel(result=False, error="Год должен быть между 2014 и 2023 включительно", info_pipe={})
#     info_pipe = get_info_pipe_year(requestBody.year)
#     print(info_pipe)
#     return Response_InfoPipeYearModel(result=True, error="", info_pipe=info_pipe)

# @app.post(path="/info_pipe_year", response_model=Response_InfoPipeYearModel, status_code=200)
# def view_info_pipe_year(response: Response, requestBody: Request_InfoPipeYearModel):
#     return info_pipe_year(response=Response, requestBody=requestBody)

# @app.get("/")
# def root_test():
#     return JSONResponse(content={"test":"test"}, status_code=200)

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "qqqg": q}

# @app.post("/test_body")
# def test_body(data=Body()):
#     print(data)
#     return JSONResponse(content={"test":1, "data": data}, status_code=200)

# class getPipeModel(BaseModel):
#     name: Union[str, None] = None

# @app.post("/pipe_test")
# def pipe_test(requestPipe: getPipeModel):
#     graph_pip = {
#         'name': 'ЦПС - Харьяга',
#         'children': [{'name': 'Труба-EP-1+EP-2+EP-3',
#         'children': [{'name': 'Труба-EP-1+EP-3',
#             'children': [{'name': 'Труба-EP-1',
#             'children': [{'name': 'Куст-EP-1', 'children': []}]},
#             {'name': 'Труба-EP-3',
#             'children': [{'name': 'Куст-EP-3', 'children': []}]}]},
#             {'name': 'Труба-EP-2',
#             'children': [{'name': 'Куст-EP-2', 'children': []}]}]},
#         {'name': 'Труба-NP-1', 'children': [{'name': 'Куст-NP-1', 'children': []}]},
#         {'name': 'Куст-NP-2', 'children': []},
#         {'name': 'Труба-NP-3+WP-1',
#         'children': [{'name': 'Труба-NP-3',
#             'children': [{'name': 'Куст-NP-3', 'children': []}]},
#             {'name': 'Труба-WP-1',
#             'children': [{'name': 'Куст-WP-1', 'children': []}]}]}]
#         }
    
#     if requestPipe.name == None:
#         return JSONResponse(content={"graph": None}, status_code=200)
    
#     if requestPipe.name == "ЦПС - Харьяга":
#         return JSONResponse(content={"graph":graph_pip}, status_code=200)

#     return JSONResponse(content={"graph": "No name"}, status_code=200)

# wbsocket_client = []
# async def send_clients(msg):
#     for ws in wbsocket_client:
#         await ws.send_text(f'send_text: {msg}')

# @app.websocket("/ws_test")
# async def websocket_endpoint_test(websocket: WebSocket):
#     await websocket.accept()
#     wbsocket_client.append(websocket)
#     while True:
#         print(1)
#         data = await websocket.receive_text()
#         print(data)
#         # await websocket.send_text(f'send_text {data}')
#         send_clients(data)

# class Request_InfoPipeYearModel(BaseModel):
#     year: int

# class Response_InfoPipeYearModel(BaseModel):
#     result: bool
#     error: str
#     info_pipe: Dict[Any, Any]
#     # info_pipe: Dict[str, Dict[int, Any]]

# @app.post(path="/info_pipe_year", response_model=Response_InfoPipeYearModel, status_code=200)
# def info_pipe_year(response: Response, requestBody: Request_InfoPipeYearModel):
#     if requestBody.year < 2014 or requestBody.year > 2023:
#         response.status_code = 400
#         return Response_InfoPipeYearModel(result=False, error="Год должен быть между 2014 и 2023 включительно", info_pipe={})
#     info_pipe = get_info_pipe_year(requestBody.year)
#     print(info_pipe)
#     return Response_InfoPipeYearModel(result=True, error="", info_pipe=info_pipe)

# @app.get(path="/gradient", response_model=Response_InfoPipeYearModel, status_code=200)
# def info_pipe_year(response: Response, requestBody: Request_InfoPipeYearModel):
#     if requestBody.year < 2014 or requestBody.year > 2023:
#         response.status_code = 400
#         return Response_InfoPipeYearModel(result=False, error="Год должен быть между 2014 и 2023 включительно", info_pipe={})
#     info_pipe = get_info_pipe_year(requestBody.year)
#     print(info_pipe)
#     return Response_InfoPipeYearModel(result=True, error="", info_pipe=info_pipe)

# @app.post(path="/info_pipe_year", response_model=ResponseInfoPipeModel, status_code=200)
# async def info_pipe_year(requestBody: RequestInfoPipeYearModel):
#     info_pipe = await get_info_pipe_year(requestBody.year)
#     return ResponseInfoPipeModel(result=True, error="", infopipe=info_pipe)