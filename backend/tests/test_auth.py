from sqlalchemy import select

from app.models.user import User


def test_register_login_me_and_ban_flow(client, db_session):
    register = client.post(
        "/api/v1/auth/register",
        json={"email": "buyer@example.com", "password": "StrongPass123"},
    )
    assert register.status_code == 201
    assert "access_token" in register.json()
    assert register.cookies.get("refresh_token") is not None

    access_token = register.json()["access_token"]
    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "buyer@example.com"

    refresh = client.post("/api/v1/auth/refresh")
    assert refresh.status_code == 200
    assert "access_token" in refresh.json()

    logout = client.post("/api/v1/auth/logout")
    assert logout.status_code == 200

    user = db_session.scalar(select(User).where(User.email == "buyer@example.com"))
    user.is_banned = True
    db_session.add(user)
    db_session.commit()

    banned_login = client.post(
        "/api/v1/auth/login",
        json={"email": "buyer@example.com", "password": "StrongPass123"},
    )
    assert banned_login.status_code == 403
