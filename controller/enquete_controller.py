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

async def edita_enquete(id, pergunta, data_inicio, data_fim, status_enquete, opcoes, db):
    try:
        if pergunta or data_inicio or data_fim:
            query = select(Enquete).where(Enquete.id == id)
            objeto_enquete = db.exec(query).first()
            print(objeto_enquete)
            if pergunta:
                objeto_enquete.pergunta = pergunta
            if data_inicio:
                objeto_enquete.data_inicio = data_inicio
            if data_fim:
                objeto_enquete.data_fim = data_fim
            if status_enquete:
                objeto_enquete.status = status_enquete
        if opcoes:
            for opcao in opcoes.opcoes:
                query = select(Opcao).where(Opcao.id == opcao.id)
                objeto_opcao = db.exec(query).first()
                if objeto_opcao:
                    objeto_opcao.descricao = opcao.descricao
                else:
                    nova_opcao = Opcao(
                        enquete_id=id,
                        descricao=opcao.descricao,
                        votos=0
                    )
                    db.add(nova_opcao)
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content="Enquete editada com sucesso!")
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao editar enquete: {e}")

async def deleta_enquete(id, db):
    try:
        objeto_enquete = db.exec(select(Enquete).where(Enquete.id == id)).first()
        objeto_opcoes = db.exec(select(Opcao).where(Opcao.enquete_id == id)).all()
        db.delete(objeto_enquete)
        for objeto in objeto_opcoes:
            db.delete(objeto)
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content="Enquete deletada com sucesso!")
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao deletar enquete: {e}")

