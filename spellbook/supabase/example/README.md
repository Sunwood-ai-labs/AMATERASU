# 📚 Supabaseテストデータセットアップガイド

このディレクトリには、Supabase環境で使用できるテストデータとサンプル実装が含まれています。

## 📁 ディレクトリ構造

```plaintext
example/
└── sql/
    ├── test_data.sql      # ユーザープロフィールデータ
    ├── posts_comments.sql # 投稿とコメント機能
    └── tags.sql          # タグシステム
```

## 🚀 テストデータのセットアップ

### 1. ベーシックなユーザープロフィール
```bash
docker cp example/sql/test_data.sql supabase-db:/docker-entrypoint-initdb.d/ && \
docker compose exec db psql -U postgres -f /docker-entrypoint-initdb.d/test_data.sql
```

作成されるデータ:
- ユーザープロフィール（3名）
- アバター用ストレージバケット

### 2. 投稿とコメント機能
```bash
docker cp example/sql/posts_comments.sql supabase-db:/docker-entrypoint-initdb.d/ && \
docker compose exec db psql -U postgres -f /docker-entrypoint-initdb.d/posts_comments.sql
```

作成されるデータ:
- 投稿テーブル（posts）
- コメントテーブル（comments）
- 各テーブルのRow Level Security設定
- サンプル投稿とコメント

### 3. タグシステム
```bash
docker cp example/sql/tags.sql supabase-db:/docker-entrypoint-initdb.d/ && \
docker compose exec db psql -U postgres -f /docker-entrypoint-initdb.d/tags.sql
```

作成されるデータ:
- タグテーブル（tags）
- 投稿とタグの関連テーブル（post_tags）
- タグ付け機能のアクセス制御
- サンプルタグデータ

## 🔒 セキュリティ設定

各テーブルには以下のセキュリティ設定が実装されています：

1. Row Level Security（RLS）
   - すべてのテーブルでRLSが有効
   - 適切な権限を持つユーザーのみがデータにアクセス可能

2. アクセス制御ポリシー
   - 閲覧：誰でも可能
   - 作成：認証済みユーザーのみ
   - 更新/削除：コンテンツ作成者のみ

## 📝 データモデル

### プロフィール（profiles）
```sql
id: uuid (primary key, references auth.users)
username: text (unique)
avatar_url: text
website: text
```

### 投稿（posts）
```sql
id: uuid (primary key)
user_id: uuid (references profiles)
title: text
content: text
created_at: timestamp
updated_at: timestamp
```

### コメント（comments）
```sql
id: uuid (primary key)
post_id: uuid (references posts)
user_id: uuid (references profiles)
content: text
created_at: timestamp
updated_at: timestamp
```

### タグ（tags）
```sql
id: uuid (primary key)
name: text (unique)
created_at: timestamp
```

### 投稿タグ（post_tags）
```sql
post_id: uuid (references posts)
tag_id: uuid (references tags)
created_at: timestamp
primary key (post_id, tag_id)
