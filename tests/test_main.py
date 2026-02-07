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
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

    # Redis保存を確認
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]
    assert fake_redis.exists(f"access:{access_token}") == 1
    assert fake_redis.exists(f"refresh:{refresh_token}") == 1

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

    access_token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/logout", headers=headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Logged out"

    # Redisからの削除確認
    assert fake_redis.exists(f"access:{access_token}") == 0

    # 以降アクセス不可
    response = client.get("/hello1", headers=headers)
    assert response.status_code == 401

# --------------------------------------------------
# リフレッシュ成功
# --------------------------------------------------
def test_refresh_success():
    login = client.post(
        "/login",
        params = {
            "username": FIXED_USER,
            "password": FIXED_PASS,
        },
    )

    data = login.json()
    refresh_token = data["refresh_token"]

    response = client.post(
        "/refresh",
        params = {
            "refresh_token": refresh_token
        }
    )

    assert response.status_code == 200
    new_data = response.json()
    assert "access_token" in new_data

# --------------------------------------------------
# リフレッシュトークンのローテーション
# --------------------------------------------------
def test_refresh_rotation():
    login = client.post(
        "/login",
        params = {
            "username": FIXED_USER,
            "password": FIXED_PASS,
        },
    )

    data = login.json()
    old_refresh_token = data["refresh_token"]

    # リフレッシュ(1回目)
    r1 = client.post(
        "/refresh",
        params = {
            "refresh_token": old_refresh_token
        }
    )
    assert r1.status_code == 200
    new_refresh_token = r1.json()["refresh_token"]

    # リフレッシュ(2回目)
    r2 = client.post(
        "/refresh",
        params = {
            "refresh_token": old_refresh_token
        }
    )
    assert r2.status_code == 401  # 古いリフレッシュトークンは使用不可

    # リフレッシュ(3回目)
    r3 = client.post(
        "/refresh",
        params = {
            "refresh_token": new_refresh_token
        }
    )
    assert r3.status_code == 200  # 新しいリフレッシュトークンは使用可能
