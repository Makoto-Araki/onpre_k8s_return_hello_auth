from fastapi import FastAPI

# アプリ(ASGI)のインスタンス生成
app = FastAPI()

# HTTP-GETメソッドで "/" にアクセス時の処理
@app.get("/")
def read_root():
    # 辞書を返すと自動的にJSONに変換
    return {"message": "Hello"}

