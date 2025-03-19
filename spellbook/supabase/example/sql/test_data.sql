-- テストユーザーデータの作成
INSERT INTO auth.users (id, email, encrypted_password, email_confirmed_at, created_at, updated_at)
VALUES 
  ('d0fc4c64-a3d6-4b08-a9b7-e05b6fd25c34', 'tanaka.taro@example.com', '$2a$10$abcdefghijklmnopqrstuvwxyz123456', NOW(), NOW(), NOW()),
  ('f8b4c42d-e5a7-4c09-b8c8-f16c7fd36e45', 'suzuki.hanako@example.com', '$2a$10$abcdefghijklmnopqrstuvwxyz123456', NOW(), NOW(), NOW()),
  ('a2c9d8e7-f6b5-4a3c-9d2e-1b8c7f6d5e4a', 'sato.jiro@example.com', '$2a$10$abcdefghijklmnopqrstuvwxyz123456', NOW(), NOW(), NOW());

-- プロフィールデータの作成
INSERT INTO public.profiles (id, updated_at, username, avatar_url, website)
VALUES
  ('d0fc4c64-a3d6-4b08-a9b7-e05b6fd25c34', NOW(), 'tanaka_taro', 'https://example.com/avatars/tanaka.jpg', 'https://tanaka-blog.example.com'),
  ('f8b4c42d-e5a7-4c09-b8c8-f16c7fd36e45', NOW(), 'hanako_s', 'https://example.com/avatars/hanako.jpg', 'https://hanako-portfolio.example.com'),
  ('a2c9d8e7-f6b5-4a3c-9d2e-1b8c7f6d5e4a', NOW(), 'jiro_sato', 'https://example.com/avatars/jiro.jpg', 'https://jiro-tech.example.com');

-- アバターファイルのストレージデータ
INSERT INTO storage.objects (id, bucket_id, name, owner, created_at, updated_at, last_accessed_at, metadata)
VALUES
  ('obj_tanaka', 'avatars', 'tanaka.jpg', 'd0fc4c64-a3d6-4b08-a9b7-e05b6fd25c34', NOW(), NOW(), NOW(), '{"size": 102400, "mimetype": "image/jpeg"}'),
  ('obj_hanako', 'avatars', 'hanako.jpg', 'f8b4c42d-e5a7-4c09-b8c8-f16c7fd36e45', NOW(), NOW(), NOW(), '{"size": 153600, "mimetype": "image/jpeg"}'),
  ('obj_jiro', 'avatars', 'jiro.jpg', 'a2c9d8e7-f6b5-4a3c-9d2e-1b8c7f6d5e4a', NOW(), NOW(), NOW(), '{"size": 81920, "mimetype": "image/jpeg"}');
