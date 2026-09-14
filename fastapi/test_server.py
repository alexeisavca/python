import pytest
from fastapi.testclient import TestClient 
from sqlmodel import SQLModel, create_engine, Session, select
from sqlmodel.pool import StaticPool
from server import app, get_db, User

import_engine = create_engine(
    "sqlite:///:memory:", 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

def override_get_db():
    with Session(import_engine) as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    SQLModel.metadata.create_all(import_engine)
    yield
    SQLModel.metadata.drop_all(import_engine)

def test_register_user_sucess():
    test_email = "test@example.com"
    response = client.post(
        "/register",
        json={
            "email": test_email,
            "password": "abc"
        }
    )

    assert response.status_code == 201

    with Session(import_engine) as db:
        statement = select(User).where(User.email == test_email)
        results = db.exec(statement).all()

        assert len(results) == 1
        assert results[0].email == test_email

