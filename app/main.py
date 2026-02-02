from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
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

# Routerを作成し、dependenciesで一括適用
router = APIRouter(dependencies=[Depends(verify_token)])

# HTTP-GETメソッドで "/hello1" にアクセス時の処理
@router.get("/hello1")
def read_hello1():
    # 辞書を返すと自動的にJSONに変換
    return {"message": "Hello1"}

# HTTP-GETメソッドで "/hello2" にアクセス時の処理
@router.get("/hello2")
def read_hello2():
    # 辞書を返すと自動的にJSONに変換
    return {"message": "Hello2"}

# HTTP-GETメソッドで "/hello3" にアクセス時の処理
@router.get("/hello3")
def read_hello3():
    # 辞書を返すと自動的にJSONに変換
    return {"message": "Hello3"}

# Routerをアプリに登録
app.include_router(router)

# HTTP-GETメソッドでヘルスチェック用エンドポイント
@app.get("/health")
def health_check():
    return {"status": "ok"}
