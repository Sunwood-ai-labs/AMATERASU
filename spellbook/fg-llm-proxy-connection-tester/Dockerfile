FROM python:3.11-slim

WORKDIR /app

# 必要なパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . .

# Streamlitアプリを実行
EXPOSE 80
ENV GLOBAL_ACCELERATOR_DNS_NAME=ae3f7bf8e8e3d659b.awsglobalaccelerator.com

HEALTHCHECK CMD curl --fail http://localhost:80/_stcore/health
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=80", "--server.address=0.0.0.0", "--server.maxUploadSize=200", "--server.maxMessageSize=200", "--server.enableWebsocketCompression=false", "--server.enableXsrfProtection=false", "--server.enableCORS=false"]
