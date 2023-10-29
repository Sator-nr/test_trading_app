from sqlalchemy import insert, select
from src.auth.models import role
from tests.conftest import client, async_session_maker


async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(role).values(id=1, name="admin", permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(role)
        result = await session.execute(query)
        assert result.all() == [(1, 'admin', None)], "No role added"


def test_register():
    response = client.post("/auth/register", json={
      "email": "string@string.string",
      "password": "string",
      "is_active": True,
      "is_superuser": False,
      "is_verified": False,
      "username": "stringstring",
      "role_id": 1
    })
    assert response.status_code == 201


def test_auth_real():
    headers = {
        'accept': 'application/json',
    }
    data = {
        'grant_type': '',
        'username': 'string@string.string',
        'password': 'string',
        'scope': '',
        'client_id': '',
        'client_secret': '',
    }
    response = client.post("/auth/jwt/login", headers=headers, data=data)
    assert response.status_code == 204


def test_auth_fake_user():
    headers = {
        'accept': 'application/json',
    }
    data = {
        'grant_type': '',
        'username': 'fake@email.nope',
        'password': 'just_nope',
        'scope': '',
        'client_id': '',
        'client_secret': '',
    }
    response = client.post("/auth/jwt/login", headers=headers, data=data)
    assert response.status_code == 400


def test_auth_fake_email():
    headers = {
        'accept': 'application/json',
    }
    data = {
        'grant_type': '',
        'username': 'fake@email.nope',
        'password': 'string',
        'scope': '',
        'client_id': '',
        'client_secret': '',
    }
    response = client.post("/auth/jwt/login", headers=headers, data=data)
    assert response.status_code == 400


def test_auth_fake_password():
    headers = {
        'accept': 'application/json',
    }
    data = {
        'grant_type': '',
        'username': 'string@string.string',
        'password': 'just_nope',
        'scope': '',
        'client_id': '',
        'client_secret': '',
    }
    response = client.post("/auth/jwt/login", headers=headers, data=data)
    assert response.status_code == 400

