from httpx import AsyncClient
import pytest

@pytest.mark.parametrize("location,date_from,date_to,status_code", [
    ("Алтай", "2026-08-12", "2026-08-10", 400),
    ("Алтай", "2026-08-01", "2026-09-01", 400),
    ("Алтай", "2026-08-15", "2026-08-25", 200)
])
async def test_get_hotels(location,date_from,date_to,status_code, ac:AsyncClient):
    response = await ac.get(
        f"/hotels/{location}",
        params={
            "date_from": date_from,
            "date_to": date_to
        }
    )

    assert response.status_code == status_code