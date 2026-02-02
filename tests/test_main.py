from fastapi.testclient import TestClient
from app.main import app

# テストクライアントにFastAPIアプリを読み込ませてインスタンス生成
client = TestClient(app)

# 固定トークン
VALID_TOKEN = "my-secret-token"

# テスト関数(正しいトークン送信時のテスト)
def test_read_hello1_success():

    # AuthorizationヘッダーにBearerトークン設定
    headers = {"Authorization": f"Bearer {VALID_TOKEN}"}

    # エンドポイント "/hello1" にGETリクエスト送信、実際のWebサーバー通信は発生しない
    response = client.get("/hello1", headers=headers)

    # APIの戻り値を確認
    assert response.status_code == 200
    assert response.json() == {"message": "Hello1"}

# テスト関数(正しいトークン送信時のテスト)
def test_read_hello2_success():

    # AuthorizationヘッダーにBearerトークン設定
    headers = {"Authorization": f"Bearer {VALID_TOKEN}"}

    # エンドポイント "/hello2" にGETリクエスト送信、実際のWebサーバー通信は発生しない
    response = client.get("/hello2", headers=headers)

    # APIの戻り値を確認
    assert response.status_code == 200
    assert response.json() == {"message": "Hello2"}

# テスト関数(正しいトークン送信時のテスト)
def test_read_hello3_success():

    # AuthorizationヘッダーにBearerトークン設定
    headers = {"Authorization": f"Bearer {VALID_TOKEN}"}

    # エンドポイント "/hello3" にGETリクエスト送信、実際のWebサーバー通信は発生しない
    response = client.get("/hello3", headers=headers)

    # APIの戻り値を確認
    assert response.status_code == 200
    assert response.json() == {"message": "Hello3"}

# テスト関数(間違えたトークン送信時のテスト)
def test_read_hello1_fail():

    # AuthorizationヘッダーにBearerトークン設定
    headers = {"Authorization": "Bearer invalid-token"}

    # エンドポイント "/hello1" にGETリクエスト送信、実際のWebサーバー通信は発生しない
    response = client.get("/hello1", headers=headers)

    # APIの戻り値を確認
    assert response.status_code == 401
    assert response.json() == {"detail":"Invalid Token"}

# テスト関数(間違えたトークン送信時のテスト)
def test_read_hello2_fail():

    # AuthorizationヘッダーにBearerトークン設定
    headers = {"Authorization": "Bearer invalid-token"}

    # エンドポイント "/hello2" にGETリクエスト送信、実際のWebサーバー通信は発生しない
    response = client.get("/hello2", headers=headers)

    # APIの戻り値を確認
    assert response.status_code == 401
    assert response.json() == {"detail":"Invalid Token"}

# テスト関数(間違えたトークン送信時のテスト)
def test_read_hello3_fail():

    # AuthorizationヘッダーにBearerトークン設定
    headers = {"Authorization": "Bearer invalid-token"}

    # エンドポイント "/hello3" にGETリクエスト送信、実際のWebサーバー通信は発生しない
    response = client.get("/hello3", headers=headers)

    # APIの戻り値を確認
    assert response.status_code == 401
    assert response.json() == {"detail":"Invalid Token"}

# テスト関数(トークン無しの場合のテスト)
def test_read_hello1_no_token():

    # エンドポイント "/hello1" にGETリクエスト送信、実際のWebサーバー通信は発生しない
    response = client.get("/hello1")

    # APIの戻り値を確認
    assert response.status_code == 401
    assert response.json() == {"detail":"Not authenticated"}

# テスト関数(トークン無しの場合のテスト)
def test_read_hello2_no_token():

    # エンドポイント "/hello2" にGETリクエスト送信、実際のWebサーバー通信は発生しない
    response = client.get("/hello2")

    # APIの戻り値を確認
    assert response.status_code == 401
    assert response.json() == {"detail":"Not authenticated"}

# テスト関数(トークン無しの場合のテスト)
def test_read_hello3_no_token():

    # エンドポイント "/hello3" にGETリクエスト送信、実際のWebサーバー通信は発生しない
    response = client.get("/hello3")

    # APIの戻り値を確認
    assert response.status_code == 401
    assert response.json() == {"detail":"Not authenticated"}
