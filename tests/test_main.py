from fastapi.testclient import TestClient
from app.main import app

# テストクライアントにFastAPIアプリを読み込ませてインスタンス生成
client = TestClient(app)

# テスト関数
def test_read_root():

    # エンドポイント "/" にGETリクエスト送信、実際のWebサーバー通信は発生しない
    response = client.get("/")

    # APIの戻り値を確認
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}
