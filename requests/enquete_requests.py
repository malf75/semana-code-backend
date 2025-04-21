from pydantic import BaseModel, conlist
from datetime import datetime
from typing import Optional

class CriaEnqueteRequest(BaseModel):
    pergunta: str
    data_inicio: Optional[datetime] = None
    data_fim: datetime

class CriaOpcoesRequest(BaseModel):
    opcoes: conlist(dict[str, str], min_length=3)