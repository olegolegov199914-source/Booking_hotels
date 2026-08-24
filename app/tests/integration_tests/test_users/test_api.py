from httpx import AsyncClient
import pytest

@pytest.mark.parametrize("email,password,status_code", [
    ("cot@pes.com", "kotopes", 200),
    ("cot@pes.com", "kot0pes", 409),
    ("pes@cot.com", "peskot", 200)
])
async def test_register_user(email,password,status_code,ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code

@pytest.mark.parametrize("email,password,status_code", [
    ("user@example.com", "string", 200)
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password,
    })
    
    assert response.status_code == status_code