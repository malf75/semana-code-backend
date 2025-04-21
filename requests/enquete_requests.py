from pydantic import BaseModel, conlist, conset
from datetime import datetime
from typing import Optional

class CriaEnqueteRequest(BaseModel):
    pergunta: str
    data_inicio: Optional[datetime] = None
    data_fim: datetime

class Opcao(BaseModel):
    descricao: str

class CriaOpcoesRequest(BaseModel):
    opcoes: conlist(Opcao, min_length=3)