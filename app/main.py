from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# アプリ(ASGI)のインスタンス生成
app = FastAPI()

# トークン抽出のインスタンス生成
security = HTTPBearer()

# 固定トークン
FIXED_TOKEN = "my-secret-token"

# 認証用関数
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != FIXED_TOKEN:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid Token",
        )

# HTTP-GETメソッドでヘルスチェック用エンドポイント
@app.get("/health")
def health_check():
    return {"status": "ok"}

# HTTP-GETメソッドで "/" にアクセス時の処理
@app.get("/")
def read_root(_: None = Depends(verify_token)):
    # 辞書を返すと自動的にJSONに変換
    return {"message": "Hello"}

