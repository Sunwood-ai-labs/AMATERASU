# 自己署名証明書の設定ガイド

このドキュメントでは、VPC内での内部ドメイン（`.internal`）で使用される自己署名証明書を信頼するための設定方法を説明します。

## 背景

内部ドメイン（例: `litellm-beta.sunwood-ai-labs.internal`）にアクセスする際、自己署名証明書が使用されているため、デフォルトではSSL証明書エラーが発生します。このガイドではこの問題を解決するための手順を説明します。

## 証明書エラーの例

```
curl: (60) SSL certificate problem: self-signed certificate
More details here: https://curl.se/docs/sslcerts.html

curl failed to verify the legitimacy of the server and therefore could not
establish a secure connection to it.
```

## 解決方法

### 1. 一時的な回避策 (推奨しない)

証明書検証をスキップする方法:

```bash
curl -k https://litellm-beta.sunwood-ai-labs.internal
```

### 2. 証明書を信頼ストアに追加する (推奨)

#### 2.1 証明書の取得

```bash
echo -n | openssl s_client -connect litellm-beta.sunwood-ai-labs.internal:443 \
    -servername litellm-beta.sunwood-ai-labs.internal \
    | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > internal-cert.pem
```

#### 2.2 証明書を信頼ストアに追加

**Ubuntu/Debian系の場合:**

```bash
sudo cp internal-cert.pem /usr/local/share/ca-certificates/internal-cert.crt
sudo update-ca-certificates
```

**CentOS/RHEL系の場合:**

```bash
sudo cp internal-cert.pem /etc/pki/ca-trust/source/anchors/
sudo update-ca-trust extract
```

#### 2.3 環境変数を設定

```bash
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
```

#### 2.4 設定の確認

```bash
curl https://litellm-beta.sunwood-ai-labs.internal
```

エラーメッセージなしで接続できれば成功です。

## 永続的な設定

### 1. シェル設定ファイルに環境変数を追加

```bash
echo 'export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt' >> ~/.bashrc
source ~/.bashrc
```

### 2. curl専用の設定

`~/.curlrc` ファイルを作成または編集:

```bash
echo "cafile = /path/to/internal-cert.pem" >> ~/.curlrc
```

### 3. プログラムごとの設定例

#### Python (requests)

```python
import requests

# 証明書を指定する場合
response = requests.get('https://litellm-beta.sunwood-ai-labs.internal', 
                        verify='/path/to/internal-cert.pem')

# 環境変数を使用する場合（SSL_CERT_FILE が設定されていること）
response = requests.get('https://litellm-beta.sunwood-ai-labs.internal')
```

#### Node.js

```javascript
const https = require('https');
const fs = require('fs');

const options = {
  hostname: 'litellm-beta.sunwood-ai-labs.internal',
  port: 443,
  path: '/',
  method: 'GET',
  ca: fs.readFileSync('/path/to/internal-cert.pem')
};

const req = https.request(options, (res) => {
  console.log('statusCode:', res.statusCode);
  res.on('data', (d) => {
    process.stdout.write(d);
  });
});

req.end();
```

## 注意事項

- 自己署名証明書は通常1年間有効です
- 証明書の有効期限が切れた場合は、上記の手順を再度実行して新しい証明書を取得し、信頼ストアを更新する必要があります
- 証明書は適切に管理し、不要になった場合は信頼ストアから削除してください

## トラブルシューティング

### 証明書が正しく更新されない場合

1. キャッシュをクリアします:

```bash
sudo rm -rf /var/lib/ca-certificates/
sudo update-ca-certificates --fresh
```

2. ブラウザのキャッシュもクリアします（ブラウザからアクセスする場合）

### 証明書が見つからない場合

```bash
# 証明書の場所を確認
find /etc/ssl -name "internal-cert*"
```

### 証明書の内容を確認

```bash
openssl x509 -in internal-cert.pem -text -noout
```
