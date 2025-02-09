FROM python:3.11-slim

WORKDIR /app

# 必要なパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . .

# Gradioアプリを実行
EXPOSE 80

HEALTHCHECK CMD curl --fail http://localhost:80/healthz || exit 1
ENTRYPOINT ["python", "app.py"]
