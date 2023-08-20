from fastapi import status
from fastapi.testclient import TestClient
import pytest
from sqlmodel import SQLModel, Session, create_engine

from sqlmodel_tutorial_fastapi.models import Hero

from .main import app
from .db import get_session
from .config import settings


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        f"postgresql://{settings.username}:{settings.password}@{settings.address}/{settings.dbname_test}",
    )
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_hero(client: TestClient):
    response = client.post("/heroes", json={"name": "xiao 3", "secret_name": "zhu xi"})
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["name"] == "xiao 3"
    assert data["secret_name"] == "zhu xi"
    assert data["id"] is not None
    assert data["age"] is None


def test_create_hero_incomplete(client: TestClient):
    response = client.post("/heroes", json={"name": "hero1"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_hero_invalid(client: TestClient):
    response = client.post(
        "/heroes", json={"name": "namename", "secret_name": {"strange": 1}}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_read_heroes_empyt(client: TestClient):
    response = client.get("/heroes")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


def test_read_heroes(session: Session, client: TestClient):
    hero_1 = Hero(name="hero1", secret_name="fast")
    hero_2 = Hero(name="her2", secret_name="hard", age=30)
    session.add(hero_1)
    session.add(hero_2)
    session.commit()

    response = client.get("/heroes")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK

    assert len(data) == 2
    assert data[0]["name"] == hero_1.name
    assert data[0]["secret_name"] == hero_1.secret_name
    assert data[0]["age"] == hero_1.age
    assert data[0]["id"] == hero_1.id
    assert data[1]["name"] == hero_2.name
    assert data[1]["secret_name"] == hero_2.secret_name
    assert data[1]["age"] == hero_2.age
    assert data[1]["id"] == hero_2.id


def test_read_hero(session: Session, client: TestClient):
    zhizi = Hero(name="zhizi", secret_name="liuzhi")
    session.add(zhizi)
    session.commit()

    rsp = client.get(f"/heroes/{zhizi.id}")
    data = rsp.json()

    assert rsp.status_code == status.HTTP_200_OK
    assert data["name"] == zhizi.name
    assert data["secret_name"] == zhizi.secret_name


def test_update_hero(session: Session, client: TestClient):
    zhizi = Hero(name="zhizi", secret_name="liuzhi")
    session.add(zhizi)
    session.commit()

    rsp = client.patch(f"/heroes/{zhizi.id}", json={"age": 20, "secret_name": "li zhi"})
    data = rsp.json()

    updated_zhizi = session.get(Hero, zhizi.id)

    assert rsp.status_code == status.HTTP_200_OK
    assert data["id"] == zhizi.id
    assert data["age"] is not None and data["age"] == 20
    assert data["secret_name"] == updated_zhizi.secret_name


def test_delete_hero(session: Session, client: TestClient):
    zhizi = Hero(name="zhizi", secret_name="liuzhi")
    session.add(zhizi)
    session.commit()

    rsp = client.delete(f"/heroes/{zhizi.id}")

    assert rsp.status_code == status.HTTP_204_NO_CONTENT
    zhizi_db = session.get(Hero, zhizi.id)
    assert zhizi_db is None
