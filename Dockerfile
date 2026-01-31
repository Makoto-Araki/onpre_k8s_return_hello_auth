FROM python:3.12-slim

# デフォルトの作業ディレクトリ設定
WORKDIR /app

# パッケージ更新と不要パッケージの削除
RUN apt-get update \
 && apt-get remove -y python3-wheel \
 && rm -rf /var/lib/apt/lists/*

# ライブラリ一覧をコピー
COPY requirements.txt .

# ライブラリ一覧をインストール
RUN pip install --no-cache-dir -r requirements.txt

# 全ファイルを/app配下にコピー
COPY . .

# デフォルトコマンド
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# デフォルトコマンド
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "3", "-b", "0.0.0.0:8000"]
