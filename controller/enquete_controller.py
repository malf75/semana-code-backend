from sqlalchemy.orm import joinedload
from sqlmodel import select
from database.models import Enquete, Opcao, EnqueteRead
from fastapi import HTTPException
from starlette import status
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from infrastructure.broadcaster import broadcaster

async def cria_enquete(pergunta, data_inicio, data_fim, opcoes, db):
    try:
        status_enquete = "iniciada"
        if data_inicio > datetime.now(timezone.utc):
            status_enquete = "não iniciada"
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
                descricao=opcao.descricao,
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

async def retorna_enquete(status_enquete, db):
    try:
        query = select(Enquete).options(joinedload(Enquete.opcoes))
        if status_enquete:
            query = query.where(Enquete.status == status_enquete)
        objetos = db.exec(query).unique().all()
        return objetos
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao listar enquetes: {e}")

async def retorna_enquete_por_id(id, db):
    try:
        query = select(Enquete).where(Enquete.id == id).options(joinedload(Enquete.opcoes))
        objetos = db.exec(query).unique().first()
        return objetos
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao listar enquetes: {e}")

async def vota_opcao(id, db):
    try:
        query = select(Opcao).where(Opcao.id == id)
        objeto_opcao = db.exec(query).first()
        enquete = await retorna_enquete_por_id(objeto_opcao.enquete_id, db)
        if enquete.status == "não iniciada":
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Enquete não iniciada!")
        if enquete.data_fim <= datetime.now():
            enquete.status = "finalizada"
            db.commit()
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Enquete finalizada!")
        objeto_opcao.votos += 1
        enquete.status = "em andamento"
        db.commit()
        db.refresh(objeto_opcao)

        todas_enquetes_atualizadas = await retorna_enquete(None, db)
        enquetes_serializadas = [EnqueteRead.model_validate(e).model_dump(mode="json") for e in todas_enquetes_atualizadas]
        await broadcaster.broadcast(enquetes_serializadas)
        return JSONResponse(status_code=status.HTTP_200_OK, content="Voto registrado com sucesso!")
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao votar na opção: {e}")