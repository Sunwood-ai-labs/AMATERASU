# GitLab SSH設定ガイド

このガイドでは、AWS Systems Manager Session Manager経由でGitLabにSSHアクセスする方法を説明します。

## 📋 前提条件

- AWS Systems Manager Session Managerが設定済み
- AWS CLIがインストール済み
- GitLabインスタンスへのアクセス権限

## 🔑 SSH設定手順

### 1. SSH鍵の生成

GitLab専用のSSH鍵を生成します：

```bash
ssh-keygen -t ed25519 -C "your.email@example.com" -f ~/.ssh/id_ed25519_amaterasu_gitlab
```

### 2. SSH設定ファイルの設定

`~/.ssh/config` に以下の設定を追加します：

```bash
# AWS SSM経由でのインスタンスアクセス
Host i-* mi-*
    ProxyCommand aws ssm start-session --target %h --document-name AWS-StartSSHSession --parameters "portNumber=%p"

# GitLabインスタンスへの直接アクセス用
Host gitlab-instance
    HostName i-027ae837f6f4f81e9  # GitLabインスタンスのID
    User ubuntu
    ProxyCommand aws ssm start-session --target %h --document-name AWS-StartSSHSession --parameters "portNumber=%p"
    IdentityFile ~/.ssh/AMATERASU-terraform-keypair-tokyo-PEM.pem  # AWS接続用の鍵

# GitLab用のSSH設定
Host amaterasu-gitlab-dev.sunwood-ai-labs.click
    HostName localhost
    Port 2222
    User git
    IdentityFile ~/.ssh/id_ed25519_amaterasu_gitlab
    ProxyCommand ssh -W %h:%p gitlab-instance
```

### 3. GitLabへの公開鍵の追加

1. 公開鍵の内容をコピー：
```bash
cat ~/.ssh/id_ed25519_amaterasu_gitlab.pub
```

2. GitLabのWeb UIで設定：
   - GitLabにログイン
   - Settings → SSH Keys に移動
   - コピーした公開鍵を "Key" 欄に貼り付け
   - タイトルを設定（例：「Amaterasu GitLab Key」）
   - "Add key" をクリック

### 4. 接続テスト

設定が完了したら、接続テストを実行：

```bash
ssh -T git@amaterasu-gitlab-dev.sunwood-ai-labs.click
```

成功すると以下のようなメッセージが表示されます：
```
Welcome to GitLab, @username!
```

## 💡 使用例

### リポジトリのクローン
```bash
git clone git@amaterasu-gitlab-dev.sunwood-ai-labs.click:group/project.git
```

### リモートの追加
```bash
git remote add origin git@amaterasu-gitlab-dev.sunwood-ai-labs.click:group/project.git
```

## 🔍 トラブルシューティング

### 接続エラーの場合
- Session Managerの接続状態を確認
- AWS CLIの認証情報を確認
- SSHキーのパーミッションを確認（600推奨）
- GitLabインスタンスのIDが正しいか確認

### 認証エラーの場合
- 公開鍵がGitLabに正しく登録されているか確認
- SSH設定ファイルのパスが正しいか確認
- GitLabのユーザー権限を確認
