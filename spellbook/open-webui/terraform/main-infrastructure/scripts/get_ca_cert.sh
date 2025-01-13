#!/bin/bash

# CA ARNを取得
CA_ARN=$CA_ARN

# CA証明書を取得
aws acm-pca get-certificate-authority-certificate \
  --certificate-authority-arn $CA_ARN \
  --output text > ca_cert.pem

# 証明書を適切な場所に配置
sudo cp ca_cert.pem /etc/ssl/certs/
sudo update-ca-certificates
