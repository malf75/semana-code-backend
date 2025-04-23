from starlette.websockets import WebSocket
from typing import List

class EnqueteBroadcaster:
    def __init__(self):
        self.conexoes: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.conexoes.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.conexoes.remove(websocket)

    async def broadcast(self, dados: list):
        print(f"Broadcasting para {len(self.conexoes)} conexões.")
        for ws in self.conexoes:
            await ws.send_json(dados)

broadcaster = EnqueteBroadcaster()