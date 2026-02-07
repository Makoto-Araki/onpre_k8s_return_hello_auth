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
# トークン有効期限(秒)
# --------------------------------------------------
ACCESS_TOKEN_EXPIRE_SECONDS = 300 # 300秒(5分)
REFRESH_TOKEN_EXPIRE_SECONDS = 3600 # 3600秒(60分)

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
    if not redis_client.exists(f"access:{token}"):
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
# リフレッシュ
# --------------------------------------------------
@app.post("/refresh")
def refresh(refresh_token: str):
    key = f"refresh:{refresh_token}"

    # リフレッシュトークン確認
    if not redis_client.exists(key):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid or expired refresh token",
        )

    # 新しいアクセストークン発行
    new_access_token = generate_token()

    # Redis登録
    redis_client.setex(
        name = f"access:{new_access_token}",
        time = ACCESS_TOKEN_EXPIRE_SECONDS,
        value = 1
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expire_in": ACCESS_TOKEN_EXPIRE_SECONDS,
    }

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
    access_token = generate_token()
    refresh_token = generate_token()

    # Redisに有効期限付き保存
    redis_client.setex(
        name = f"access:{access_token}",
        time = ACCESS_TOKEN_EXPIRE_SECONDS,
        value = 1
    )
    redis_client.setex(
        name = f"refresh:{refresh_token}",
        time = REFRESH_TOKEN_EXPIRE_SECONDS,
        value = 1
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
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
    redis_client.delete(f"access:{token}")

    return {"message": "Logged out"}

# --------------------------------------------------
# 生存確認
# --------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}
