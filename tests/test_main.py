from fastapi.testclient import TestClient
from app.main import app

# テストクライアントにFastAPIアプリを読み込ませてインスタンス生成
client = TestClient(app)

# 固定トークン
VALID_TOKEN = "my-secret-token"

# テスト関数(正しいトークン送信時のテスト)
def test_read_root_success():

    # AuthorizationヘッダーにBearerトークン設定
    headers = {"Authorization": f"Bearer {VALID_TOKEN}"}

    # エンドポイント "/" にGETリクエスト送信、実際のWebサーバー通信は発生しない
    response = client.get("/", headers=headers)

    # APIの戻り値を確認
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}

# テスト関数(間違えたトークン送信時のテスト)
def test_read_root_fail():

    # AuthorizationヘッダーにBearerトークン設定
    headers = {"Authorization": "Bearer invalid-token"}

    # エンドポイント "/" にGETリクエスト送信、実際のWebサーバー通信は発生しない
    response = client.get("/", headers=headers)

    # APIの戻り値を確認
    assert response.status_code == 401
    assert response.json() == {"detail":"Invalid Token"}

# テスト関数(トークン無しの場合のテスト)
def test_read_root_no_token():

    # エンドポイント "/" にGETリクエスト送信、実際のWebサーバー通信は発生しない
    response = client.get("/")

    # APIの戻り値を確認
    assert response.status_code == 401
    assert response.json() == {"detail":"Not authenticated"}
