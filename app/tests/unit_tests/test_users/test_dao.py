from app.users.dao import UserDAO
import pytest

@pytest.mark.parametrize("user_id,email,exists",[
    (1, "user@example.com", True),
    (2, "i@test.com", True),
    (3, "...", False)
])
async def test_find_user_by_id(user_id,email,exists):
    user = await UserDAO.find_by_id(user_id)

    if exists:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
    