-- 익명 게시판 스키마
-- Supabase SQL Editor에서 실행하세요

-- 게시글 테이블
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author_name VARCHAR(100) NOT NULL DEFAULT '익명',
    password VARCHAR(255) NOT NULL,  -- 수정/삭제용 비밀번호 (해시 저장)
    view_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 댓글 테이블 (대댓글 지원: parent_id로 계층 구조)
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    parent_id INTEGER REFERENCES comments(id) ON DELETE CASCADE,  -- NULL이면 댓글, 값이 있으면 대댓글
    content TEXT NOT NULL,
    author_name VARCHAR(100) NOT NULL DEFAULT '익명',
    password VARCHAR(255) NOT NULL,  -- 수정/삭제용 비밀번호 (해시 저장)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스 생성
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
CREATE INDEX idx_comments_post_id ON comments(post_id);
CREATE INDEX idx_comments_parent_id ON comments(parent_id);

-- RLS(Row Level Security) 비활성화 (익명 게시판이므로 공개)
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;

-- 모든 사용자가 읽기/쓰기 가능하도록 정책 설정
CREATE POLICY "Enable read access for all users" ON posts FOR SELECT USING (true);
CREATE POLICY "Enable insert for all users" ON posts FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for all users" ON posts FOR UPDATE USING (true);
CREATE POLICY "Enable delete for all users" ON posts FOR DELETE USING (true);

CREATE POLICY "Enable read access for all users" ON comments FOR SELECT USING (true);
CREATE POLICY "Enable insert for all users" ON comments FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for all users" ON comments FOR UPDATE USING (true);
CREATE POLICY "Enable delete for all users" ON comments FOR DELETE USING (true);
