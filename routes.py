import uvicorn
import os
from starlette.websockets import WebSocket, WebSocketDisconnect
from setup.settings import app
from fastapi.responses import RedirectResponse
from fastapi import Depends
from sqlmodel import Session, SQLModel
from database.database import get_db, engine
from database.models import EnqueteRead
from typing import Annotated, List
from requests.enquete_requests import *
from controller.enquete_controller import *
from infrastructure.broadcaster import broadcaster

db = Annotated[Session, Depends(get_db)]
SQLModel.metadata.create_all(engine)

@app.get("/")
def redirect_index():
    return RedirectResponse("/docs")

@app.post("/enquetes")
async def rota_cria_enquetes(enquete_request: CriaEnqueteRequest, opcao_request: CriaOpcoesRequest, db: Session = Depends(get_db)):
    enquete = await cria_enquete(enquete_request.pergunta, enquete_request.data_inicio, enquete_request.data_fim, opcao_request, db)
    return enquete

@app.patch("/enquetes")
async def rota_edita_enquetes(id: str, enquete_request: EditaEnqueteRequest, opcao_request: EditaOpcoesRequest, db: Session = Depends(get_db)):
    enquete = await edita_enquete(id, enquete_request.pergunta, enquete_request.data_inicio, enquete_request.data_fim, enquete_request.status, opcao_request, db)
    return enquete

@app.delete("/enquetes")
async def rota_deleta_enquetes(id: str, db: Session = Depends(get_db)):
    enquete = await deleta_enquete(id, db)
    return enquete

@app.get("/enquetes", response_model=List[EnqueteRead])
async def rota_retorna_enquetes(status: Optional[str] = None, db: Session = Depends(get_db)):
    enquete = await retorna_enquete(status, db)
    return enquete

@app.put("/voto")
async def rota_vota_opcao(id: str, db: Session = Depends(get_db)):
    enquete = await vota_opcao(id, db)
    return enquete

@app.websocket("/ws/enquetes")
async def websocket_enquetes(websocket: WebSocket):
    await broadcaster.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        print("Cliente desconectado do WebSocket")
    finally:
        broadcaster.disconnect(websocket)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
