import uuid
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional, List

class Enquete(SQLModel, table=True):
    __tablename__ = 'enquetes'

    id: uuid.UUID = Field(default_factory=uuid.uuid4,primary_key=True)
    pergunta: str = Field(max_length=200)
    status: str = Field(max_length=40)
    data_inicio: Optional[datetime] = Field(default_factory=datetime.now)
    data_fim: datetime = Field()

    opcoes: List["Opcao"] = Relationship(
        back_populates="enquete",
        sa_relationship=relationship("Opcao", back_populates="enquete", cascade="all, delete-orphan")
    )

class Opcao(SQLModel, table=True):
    __tablename__ = 'opcoes'

    id: uuid.UUID = Field(default_factory=uuid.uuid4,primary_key=True)
    enquete_id: uuid.UUID = Field(foreign_key="enquetes.id")
    enquete: Optional[Enquete] = Relationship(back_populates="opcoes")
    descricao: str = Field(max_length=50)
    votos: int = Field()

class OpcaoBase(SQLModel):
    descricao: str
    votos: int

class OpcaoRead(OpcaoBase):
    id: uuid.UUID
    enquete_id: uuid.UUID

class EnqueteRead(SQLModel):
    id: uuid.UUID
    pergunta: str
    status: str
    data_inicio: Optional[datetime]
    data_fim: datetime
    opcoes: List[OpcaoRead] = []