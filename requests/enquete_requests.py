from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CriaEnqueteRequest(BaseModel):
    pergunta: str
    data_inicio: Optional[datetime] = None
    data_fim: datetime

class CriaOpcoesRequest(BaseModel):
    opcoes: list[dict[str, str]] = [{}]