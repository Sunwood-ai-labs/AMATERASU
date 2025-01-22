# ベースイメージとしてPython 3.9を使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Pythonパッケージをインストール
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . .

# Streamlitアプリを実行
EXPOSE 80
HEALTHCHECK CMD curl --fail http://localhost:80/_stcore/health
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=80", "--server.address=0.0.0.0", "--server.maxUploadSize=200", "--server.maxMessageSize=200", "--server.enableWebsocketCompression=false", "--server.enableXsrfProtection=false", "--server.enableCORS=false"]
