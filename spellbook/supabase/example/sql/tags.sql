-- タグテーブルの作成
create table tags (
  id uuid default uuid_generate_v4() primary key,
  name text not null unique,
  created_at timestamp with time zone default now()
);

-- 投稿とタグの関連テーブルの作成
create table post_tags (
  post_id uuid references posts(id) on delete cascade,
  tag_id uuid references tags(id) on delete cascade,
  created_at timestamp with time zone default now(),
  primary key (post_id, tag_id)
);

-- Row Level Security の設定
alter table tags enable row level security;
alter table post_tags enable row level security;

-- 誰でも閲覧可能なポリシー
create policy "Anyone can view tags" on tags
  for select using (true);

create policy "Anyone can view post_tags" on post_tags
  for select using (true);

-- タグの作成は認証済みユーザーのみ可能
create policy "Authenticated users can create tags" on tags
  for insert with check (auth.role() = 'authenticated');

-- 投稿者のみタグ付け可能
create policy "Post authors can add tags" on post_tags
  for insert with check (
    auth.uid() in (
      select user_id from posts where id = post_id
    )
  );

-- テストデータの投入
insert into tags (id, name) values
  ('550e8400-e29b-41d4-a716-446655440001', 'テクノロジー'),
  ('550e8400-e29b-41d4-a716-446655440002', '料理'),
  ('550e8400-e29b-41d4-a716-446655440003', 'プログラミング'),
  ('550e8400-e29b-41d4-a716-446655440004', 'Supabase'),
  ('550e8400-e29b-41d4-a716-446655440005', '初心者向け');

insert into post_tags (post_id, tag_id) values
  ('550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440001'),  -- 技術ブログ - テクノロジー
  ('550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440004'),  -- 技術ブログ - Supabase
  ('6ba7b810-9dad-11d1-80b4-00c04fd430c8', '550e8400-e29b-41d4-a716-446655440002'),  -- 料理レシピ - 料理
  ('6ba7b811-9dad-11d1-80b4-00c04fd430c8', '550e8400-e29b-41d4-a716-446655440003'),  -- プログラミング入門 - プログラミング
  ('6ba7b811-9dad-11d1-80b4-00c04fd430c8', '550e8400-e29b-41d4-a716-446655440005');  -- プログラミング入門 - 初心者向け
