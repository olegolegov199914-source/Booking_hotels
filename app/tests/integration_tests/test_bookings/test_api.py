

import pytest
from httpx import AsyncClient

@pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms,status_code", *[
    [(4, "2030-05-01", "2030-05-15", i, 200) for i in range(3, 11)] +
    [(4, "2030-05-01", "2030-05-15", 10, 409)] * 2
])
async def test_add_and_get_booking(room_id, date_from, date_to, booked_rooms, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })

    assert response.status_code == status_code

    response = await authenticated_ac.get("/bookings")

    assert len(response.json()) == booked_rooms

@pytest.mark.parametrize("email,password", [
    ("user@example.com", "string")
])
async def test_add_and_delete_bookings(email, password, ac: AsyncClient):
    login_response = await ac.post("/auth/login", json={
        "email": email,
        "password": password
    })
    if login_response.status_code != 200:
        register_response = await ac.post("/auth/register", json={
            "email": email,
            "password": password
        })
        
        
        if register_response.status_code == 409:  
            pytest.skip(f"Пользователь {email} уже существует, но логин не удался")
        
        assert register_response.status_code == 200, f"Ошибка регистрации: {register_response.text}"
        
        # Повторно логинимся
        login_response = await ac.post("/auth/login", json={
            "email": email,
            "password": password
        })
        assert login_response.status_code == 200, f"Логин не удался: {login_response.text}"
    
    try:
        login_data = login_response.json()
    except Exception as e:
        print(f"Ошибка парсинга JSON: {e}")
        print(f"Ответ сервера: {login_response.text}")
        pytest.fail(f"Сервер вернул не JSON: {login_response.text}")
    
    token = login_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    
    # ШАГ 4: Получаем бронирования
    get_response = await ac.get("/bookings", headers=headers)
    assert get_response.status_code == 200, f"Ошибка получения бронирований: {get_response.text}"
    bookings = get_response.json()
    
    
    if not bookings:
        return
    
    # ШАГ 5: Удаляем все бронирования
    for booking in bookings:
        booking_id = booking.get("id")
        if booking_id:
            delete_response = await ac.delete(
                f"/bookings/{booking_id}",
                headers=headers
            )
            assert delete_response.status_code in [204, 404], f"Ошибка удаления: {delete_response.text}"

    
    # ШАГ 6: Проверяем, что бронирований нет
    final_response = await ac.get("/bookings", headers=headers)
    assert final_response.status_code == 200
    remaining_bookings = final_response.json()
    
    assert len(remaining_bookings) == 0, f"Остались бронирования: {remaining_bookings}"
