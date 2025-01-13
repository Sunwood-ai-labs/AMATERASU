# CA ARNを取得
$CA_ARN = $env:CA_ARN

# CA証明書を取得
aws acm-pca get-certificate-authority-certificate `
  --certificate-authority-arn $CA_ARN `
  --output text > ca_cert.pem

# 証明書を適切な場所に配置
Copy-Item -Path .\ca_cert.pem -Destination C:\ProgramData\SSL\Certs\
certutil -addstore -f "Root" C:\ProgramData\SSL\Certs\ca_cert.pem
