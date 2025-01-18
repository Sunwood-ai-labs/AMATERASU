#!/bin/bash

# ベースのセットアップスクリプトをダウンロードして実行
curl -fsSL https://raw.githubusercontent.com/Sunwood-ai-labs/AMATERASU/refs/heads/main/scripts/docker-compose_setup_script.sh -o /tmp/base_setup.sh
chmod +x /tmp/base_setup.sh
/tmp/base_setup.sh

# AMATERASUリポジトリのクローン
git clone https://github.com/Sunwood-ai-labs/AMATERASU.git /home/ubuntu/AMATERASU

# Terraformから提供される環境変数ファイルの作成
# 注: .envファイルの内容はTerraformから提供される
echo "${env_content}" > /home/ubuntu/AMATERASU/spellbook/langfuse3/.env

# ファイルの権限設定
chmod 777 -R /home/ubuntu/AMATERASU

# AMATERASUディレクトリに移動
cd /home/ubuntu/AMATERASU/spellbook/langfuse3

# 指定されたdocker-composeファイルでコンテナを起動
sudo docker-compose up -d

echo "AMATERASUのセットアップが完了し、docker-composeを起動しました!"

# 一時ファイルの削除
rm /tmp/base_setup.sh
