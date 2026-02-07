from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import secrets
import redis

# --------------------------------------------------
# Redis接続
# --------------------------------------------------
redis_client = redis.Redis(
    host = "redis", # Service名
    port = 6379,
    db = 0,
    decode_responses = True, # strで取扱可能
)

# --------------------------------------------------
# FastAPI
# --------------------------------------------------
app = FastAPI()
security = HTTPBearer()

FIXED_USER = "admin"
FIXED_PASS = "password"

# --------------------------------------------------
# ランダムトークン生成用関数
# --------------------------------------------------
def generate_token() -> str:
    return secrets.token_urlsafe(32)

# --------------------------------------------------
# 認証チェック
# --------------------------------------------------
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    # Redisに存在しなければ無効または期限切れ
    if not redis_client.exists(token):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid or expired token",
        )

# --------------------------------------------------
# 認証必須Router
# --------------------------------------------------
router = APIRouter(dependencies=[Depends(verify_token)])

@router.get("/hello1")
def read_hello1():
    return {"message": "Hello1"}

@router.get("/hello2")
def read_hello2():
    return {"message": "Hello2"}

@router.get("/hello3")
def read_hello3():
    return {"message": "Hello3"}

app.include_router(router)

# --------------------------------------------------
# ログイン
# --------------------------------------------------
@app.post("/login")
def login(username: str, password: str):
    if username != FIXED_USER or password != FIXED_PASS:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid username or password",
        )

    # 新しいトークン生成
    token = generate_token()

    # トークン有効期限(秒)
    ACCESS_TOKEN_EXPIRE_SECONDS = 300 # 300秒(5分)

    # Redisに有効期限付き保存
    redis_client.setex(
        name = token,
        time = ACCESS_TOKEN_EXPIRE_SECONDS,
        value = 1
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_SECONDS,
    }

# --------------------------------------------------
# ログアウト
# --------------------------------------------------
@app.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    # Redisから削除(失効)
    redis_client.delete(token)

    return {"message": "Logged out"}

# --------------------------------------------------
# 生存確認
# --------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}
