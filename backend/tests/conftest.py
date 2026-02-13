from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import hash_password
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.role import Role, RoleName
from app.models.user import User

SQLALCHEMY_DATABASE_URL = "sqlite+pysqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database() -> Generator[None, None, None]:
    Base.metadata.create_all(bind=engine)
    with TestingSessionLocal() as db:
        for role_name in RoleName:
            db.add(Role(name=role_name))
        db.commit()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


def create_user(db: Session, email: str, password: str, roles: list[RoleName]) -> User:
    role_rows = db.scalars(select(Role).where(Role.name.in_(roles))).all()
    user = User(email=email, password_hash=hash_password(password), roles=role_rows)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    with TestingSessionLocal() as db:
        yield db


@pytest.fixture()
def create_user_factory(db_session: Session):
    def _create(email: str, password: str, roles: list[RoleName]) -> User:
        return create_user(db_session, email, password, roles)

    return _create


def auth_headers(client: TestClient, email: str, password: str) -> dict[str, str]:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
