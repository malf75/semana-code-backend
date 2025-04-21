from sqlmodel import select
from sqlalchemy import or_
from database.models import Enquete, Opcao
from fastapi import HTTPException
from starlette import status
from fastapi.responses import JSONResponse
from datetime import datetime, timezone

async def cria_enquete(pergunta, data_inicio, data_fim, opcoes, db):
    try:
        status_enquete = "iniciado"
        if data_inicio > datetime.now(timezone.utc):
            status_enquete = "não iniciado"
        objeto_enquete = Enquete(
            pergunta=pergunta,
            status=status_enquete,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        for opcao in opcoes.opcoes:
            print(opcao)
            objeto_opcao = Opcao(
                enquete_id=objeto_enquete.id,
                descricao=opcao["descricao"],
                votos=0
            )
            db.add(objeto_opcao)
        db.add(objeto_enquete)
        db.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content="Enquete Criada!")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao criar enquete! {e}")
