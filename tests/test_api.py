from fastapi.testclient import TestClient
from main import app, fila

client = TestClient(app)


def test_add_and_list():
    fila.clear()

    r = client.post("/fila", json={"nome": "Ana", "tipo": "N"})
    assert r.status_code == 201

    r2 = client.post("/fila", json={"nome": "Joao", "tipo": "P"})
    assert r2.status_code == 201

    r = client.get("/fila")
    assert r.status_code == 200

    data = r.json()
    assert len(data) == 2

    assert data[0]["nome"] == "Joao"
    assert data[0]["posicao"] == 1

    assert data[1]["nome"] == "Ana"
    assert data[1]["posicao"] == 2


def test_get_by_position_and_404():
    fila.clear()

    client.post("/fila", json={"nome": "A", "tipo": "N"})

    res = client.get("/fila/1")
    assert res.status_code == 200
    assert res.json()["nome"] == "A"

    res2 = client.get("/fila/5")
    assert res2.status_code == 404


def test_put_advance_and_delete():
    fila.clear()

    client.post("/fila", json={"nome": "A", "tipo": "N"})
    client.post("/fila", json={"nome": "B", "tipo": "N"})
    client.post("/fila", json={"nome": "C", "tipo": "N"})

    r = client.get("/fila")
    assert len(r.json()) == 3

 
    r = client.put("/fila")
    assert r.status_code == 200

    remaining = r.json()
    assert len(remaining) == 2
    assert remaining[0]["nome"] == "B"
    assert remaining[0]["posicao"] == 1

    r = client.delete("/fila/1")
    assert r.status_code == 200

    remaining = r.json()
    assert len(remaining) == 1
    assert remaining[0]["nome"] == "C"
    assert remaining[0]
