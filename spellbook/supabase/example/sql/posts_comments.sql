-- 投稿テーブルの作成
create table posts (
  id uuid default uuid_generate_v4() primary key,
  user_id uuid references profiles(id) not null,
  title text not null,
  content text not null,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- コメントテーブルの作成
create table comments (
  id uuid default uuid_generate_v4() primary key,
  post_id uuid references posts(id) not null,
  user_id uuid references profiles(id) not null,
  content text not null,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- Row Level Security の設定
alter table posts enable row level security;
alter table comments enable row level security;

-- 誰でも閲覧可能なポリシー
create policy "Anyone can view posts" on posts
  for select using (true);

create policy "Anyone can view comments" on comments
  for select using (true);

-- 作成者のみ編集・削除可能なポリシー
create policy "Users can create their own posts" on posts
  for insert with check (auth.uid() = user_id);

create policy "Users can update their own posts" on posts
  for update using (auth.uid() = user_id);

create policy "Users can delete their own posts" on posts
  for delete using (auth.uid() = user_id);

create policy "Users can create their own comments" on comments
  for insert with check (auth.uid() = user_id);

create policy "Users can update their own comments" on comments
  for update using (auth.uid() = user_id);

create policy "Users can delete their own comments" on comments
  for delete using (auth.uid() = user_id);

-- テストデータの投入
insert into posts (id, user_id, title, content) values
  ('550e8400-e29b-41d4-a716-446655440000', 'd0fc4c64-a3d6-4b08-a9b7-e05b6fd25c34', '技術ブログ: Supabaseの始め方', 'Supabaseは優れたBaaSプラットフォームです。以下のステップで簡単に始められます...'),
  ('6ba7b810-9dad-11d1-80b4-00c04fd430c8', 'f8b4c42d-e5a7-4c09-b8c8-f16c7fd36e45', '料理レシピ共有', '今日は私のお気に入りの和食レシピを共有します...'),
  ('6ba7b811-9dad-11d1-80b4-00c04fd430c8', 'a2c9d8e7-f6b5-4a3c-9d2e-1b8c7f6d5e4a', 'プログラミング入門', 'プログラミングを始めたい人向けのガイドを書きました...');

insert into comments (id, post_id, user_id, content) values
  ('7ba7b810-9dad-11d1-80b4-00c04fd430c8', '550e8400-e29b-41d4-a716-446655440000', 'f8b4c42d-e5a7-4c09-b8c8-f16c7fd36e45', 'とても分かりやすい記事ですね！'),
  ('7ba7b811-9dad-11d1-80b4-00c04fd430c8', '6ba7b810-9dad-11d1-80b4-00c04fd430c8', 'd0fc4c64-a3d6-4b08-a9b7-e05b6fd25c34', 'レシピ参考にさせていただきます！'),
  ('7ba7b812-9dad-11d1-80b4-00c04fd430c8', '6ba7b811-9dad-11d1-80b4-00c04fd430c8', 'f8b4c42d-e5a7-4c09-b8c8-f16c7fd36e45', '初心者にも分かりやすいです');
