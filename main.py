from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

app = FastAPI(title="API Fila de Atendimento")


class ClienteEntrada(BaseModel):
    nome: str = Field(..., max_length=20)
    tipo: str = Field(..., min_length=1, max_length=1, description="N ou P")


class Cliente(BaseModel):
    posicao: int
    nome: str
    data_chegada: str
    tipo: str
    atendido: bool


fila: List[Cliente] = []


def atualizar_posicoes():
    pos = 1
    for cliente in fila:
        if not cliente.atendido:
            cliente.posicao = pos
            pos += 1
        else:
            cliente.posicao = 0


@app.get("/fila", response_model=List[Cliente])
def listar_fila():
    return [c for c in fila if not c.atendido]


@app.get("/fila/{id}", response_model=Cliente)
def listar_por_posicao(id: int):
    for cliente in fila:
        if cliente.posicao == id and not cliente.atendido:
            return cliente

    raise HTTPException(
        status_code=404,
        detail={"mensagem": f"Nenhum cliente encontrado na posição {id}"}
    )


@app.post("/fila", response_model=Cliente, status_code=201)
def adicionar_cliente(cliente: ClienteEntrada):

    if cliente.tipo.upper() not in ("N", "P"):
        raise HTTPException(status_code=400, detail={"mensagem": "Tipo deve ser N ou P"})

    novo = Cliente(
        nome=cliente.nome,
        tipo=cliente.tipo.upper(),
        data_chegada=datetime.now().isoformat(),
        posicao=0,
        atendido=False
    )


    if novo.tipo == "P":
        index_insercao = 0
        for i, c in enumerate(fila):
            if c.tipo == "P" and not c.atendido:
                index_insercao = i + 1
        fila.insert(index_insercao, novo)
    else:
        fila.append(novo)

    atualizar_posicoes()
    return novo


@app.put("/fila", response_model=List[Cliente])
def avancar_fila():

    primeiro = next((c for c in fila if not c.atendido), None)

    if not primeiro:
        return [] 

    primeiro.atendido = True
    primeiro.posicao = 0

    atualizar_posicoes()

    return [c for c in fila if not c.atendido]


@app.delete("/fila/{id}", response_model=List[Cliente])
def remover_cliente(id: int):

    for c in fila:
        if c.posicao == id and not c.atendido:
            fila.remove(c)
            atualizar_posicoes()
            return [cliente for cliente in fila if not cliente.atendido]

    raise HTTPException(
        status_code=404,
        detail={"mensagem": f"Nenhum cliente encontrado na posição {id}"}
    )
