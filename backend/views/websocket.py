from fastapi import APIRouter, WebSocket, Response


ws = APIRouter()

wbsocket_client = {}
async def send_clients(current_ws, msg):
    if msg == "info":
        info_current_ws = wbsocket_client[current_ws]['coord_x_y']
        await wbsocket_client[current_ws]['ws'].send_text(f'info_coord: {info_current_ws}')
        return
    
    if msg == "move":
        wbsocket_client[current_ws]['coord_x_y'] += 1
        info_current_ws = wbsocket_client[current_ws]['coord_x_y']
        await wbsocket_client[current_ws]['ws'].send_text(f'info_coord: {info_current_ws}')
        return

    for ws in wbsocket_client:
        await wbsocket_client[ws]['ws'].send_text(f'send_text: {msg}')
    return

@ws.websocket("/ws_test")
async def websocket_endpoint_test(websocket: WebSocket):
    await websocket.accept()
    wbsocket_client[websocket] = {'ws':websocket, 'coord_x_y': 0}
    print(wbsocket_client)
    while True:
        print(1)
        data = await websocket.receive_text()
        print(data)
        # await websocket.send_text(f'send_text {data}')
        await send_clients(current_ws=websocket, msg=data)