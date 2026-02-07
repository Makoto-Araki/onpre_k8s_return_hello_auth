from fastapi.testclient import TestClient
import fakeredis

from app.main import app, redis_client

# --------------------------------------------------
# テスト用Redisに差替
# --------------------------------------------------
fake_redis = fakeredis.FakeRedis(decode_responses=True)

# main.pyのredis_clientを上書き
redis_client.connection_pool = fake_redis.connection_pool

# --------------------------------------------------
# TestClient
# --------------------------------------------------
client = TestClient(app)

FIXED_USER = "admin"
FIXED_PASS = "password"

# --------------------------------------------------
# ログイン成功
# --------------------------------------------------
def test_login_success():
    response = client.post(
        "/login",
        params={
            "username": FIXED_USER,
            "password": FIXED_PASS,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Redis保存を確認
    token = data["access_token"]
    assert fake_redis.exists(token) == 1

# --------------------------------------------------
# ログイン失敗
# --------------------------------------------------
def test_login_fail():
    response = client.post(
        "/login",
        params={
            "username": "admin",
            "password": "invalid",
        },
    )

    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid username or password"

# --------------------------------------------------
# 認証付きエンドポイント(成功)
# --------------------------------------------------
def test_hello1_with_valid_token():
    login = client.post(
        "/login",
        params = {
            "username": FIXED_USER,
            "password": FIXED_PASS,
        },
    )

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/hello1", headers=headers)

    assert response.status_code == 200
    assert response.json() == {"message": "Hello1"}

# --------------------------------------------------
# 認証付きエンドポイント(トークン不正)
# --------------------------------------------------
def test_hello1_with_invalid_token():
    headers = {"Authorization": "Bearer invalid-token"}
    response = client.get("/hello1", headers=headers)

    assert response.status_code == 401
    assert response.json() == {"detail":"Invalid or expired token"}

# --------------------------------------------------
# ログアウト
# --------------------------------------------------
def test_logout():
    login = client.post(
        "/login",
        params={
            "username": FIXED_USER,
            "password": FIXED_PASS,
        },
    )

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/logout", headers=headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Logged out"

    # Redisからの削除確認
    assert fake_redis.exists(token) == 0

    # 以降アクセス不可
    response = client.get("/hello1", headers=headers)
    assert response.status_code == 401
