from pydantic import BaseModel, conlist
from datetime import datetime
from typing import Optional

class CriaEnqueteRequest(BaseModel):
    pergunta: str
    data_inicio: Optional[datetime] = None
    data_fim: datetime

class EditaEnqueteRequest(BaseModel):
    pergunta: Optional[str] = None
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    status: Optional[str] = None

class Opcao(BaseModel):
    descricao: str

class OpcaoEdita(BaseModel):
    id: Optional[str] = None
    descricao: str

class CriaOpcoesRequest(BaseModel):
    opcoes: conlist(Opcao, min_length=3)

class EditaOpcoesRequest(BaseModel):
    opcoes: Optional[list[OpcaoEdita]] = None

