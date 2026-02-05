from fastapi.testclient import TestClient
from app.main import app

# テストクライアントにFastAPIアプリを読み込ませてインスタンス生成
client = TestClient(app)

# 固定トークン
#VALID_TOKEN = "my-secret-token"

# 正しいトークン取得
def get_valid_token() -> str:
    response = client.post(
        "/login",
        params = {
            "username": "admin",
            "password": "password",
        },
    )
    assert response.status_code == 200
    return response.json()["access_token"]

# テスト関数(正しいトークン送信時のテスト)
def test_read_hello1_success():
    token = get_valid_token()

    # AuthorizationヘッダーにBearerトークン設定
    headers = {"Authorization": f"Bearer {token}"}

    # エンドポイント "/hello1" にGETリクエスト送信、実際のWebサーバー通信は発生しない
    response = client.get("/hello1", headers=headers)

    # APIの戻り値を確認
    assert response.status_code == 200
    assert response.json() == {"message": "Hello1"}

# テスト関数(正しいトークン送信時のテスト)
def test_read_hello2_success():
    token = get_valid_token()

    # AuthorizationヘッダーにBearerトークン設定
    headers = {"Authorization": f"Bearer {token}"}

    # エンドポイント "/hello2" にGETリクエスト送信、実際のWebサーバー通信は発生しない
    response = client.get("/hello2", headers=headers)

    # APIの戻り値を確認
    assert response.status_code == 200
    assert response.json() == {"message": "Hello2"}

# テスト関数(正しいトークン送信時のテスト)
def test_read_hello3_success():
    token = get_valid_token()

    # AuthorizationヘッダーにBearerトークン設定
    headers = {"Authorization": f"Bearer {token}"}

    # エンドポイント "/hello3" にGETリクエスト送信、実際のWebサーバー通信は発生しない
    response = client.get("/hello3", headers=headers)

    # APIの戻り値を確認
    assert response.status_code == 200
    assert response.json() == {"message": "Hello3"}

# テスト関数(間違えたトークン送信時のテスト)
def test_read_hello_invalid_token():

    # AuthorizationヘッダーにBearerトークン設定
    headers = {"Authorization": "Bearer invalid-token"}

    # エンドポイント "/hello1" にGETリクエスト送信、実際のWebサーバー通信は発生しない
    response = client.get("/hello1", headers=headers)

    # APIの戻り値を確認
    assert response.status_code == 401
    assert response.json() == {"detail":"Invalid or expired token"}

# テスト関数(トークン無しの場合のテスト)
def test_read_hello_no_token():

    # エンドポイント "/hello1" にGETリクエスト送信、実際のWebサーバー通信は発生しない
    response = client.get("/hello1")

    # APIの戻り値を確認
    assert response.status_code == 401
    assert response.json() == {"detail":"Not authenticated"}

# テスト関数(正規ユーザーと正規パスワードのテスト)
def test_login_success():

    # エンドポイント "/login" にPOSTリクエスト送信
    response = client.post(
        "/login",
        params={
            "username": "admin",
            "password": "password",
        },
    )

    # リターンステータスコード
    assert response.status_code == 200

    # レスポンスJSON取得
    data = response.json()

    # トークン
    assert "access_token" in data
    assert data["token_type"] == "bearer"

# テスト関数(不正ユーザーと不正パスワードのテスト)
def test_login_failure():

    # エンドポイント "/login" にPOSTリクエスト送信
    response = client.post(
        "/login",
        params={
            "username": "admin",
            "password": "invalid",
        },
    )

    # リターンステータスコード
    assert response.status_code == 401

    # レスポンスJSON取得
    data = response.json()

    # トークン
    assert data["detail"] == "Invalid username or password"
