# AI Board - 익명 게시판

FastAPI 백엔드와 Next.js 프론트엔드로 구성된 익명 게시판 웹 애플리케이션입니다.

## 주요 기능

- 게시글 CRUD (목록/상세/등록/수정/삭제)
- 댓글 및 대댓글 기능
- 비밀번호 기반 익명 인증 (수정/삭제 시 필요)
- 조회수 카운팅

## Tech Stack

| 구분 | 기술 |
|------|------|
| Backend | FastAPI, Python 3.11+, Pydantic, bcrypt |
| Database | Supabase (PostgreSQL) |
| Frontend | Next.js 14, React 18, TypeScript, Tailwind CSS |
| MCP Servers | Playwright (브라우저 자동화), Notion (노션 연동) |

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm
- Supabase 계정

## 프로젝트 구조

```
ai-board/
├── backend/
│   ├── main.py              # FastAPI 앱 및 API 엔드포인트
│   ├── database.py          # Supabase 클라이언트 설정
│   ├── schema.sql           # 데이터베이스 스키마
│   ├── requirements.txt     # Python 의존성
│   └── tests/               # 테스트 (TDD)
│       ├── test_posts.py    # 게시글 API 테스트
│       └── test_comments.py # 댓글 API 테스트
├── frontend/
│   └── src/
│       ├── app/             # Next.js 페이지
│       │   ├── page.tsx           # 게시글 목록
│       │   └── posts/
│       │       ├── new/page.tsx   # 글쓰기
│       │       └── [id]/
│       │           ├── page.tsx   # 글 상세
│       │           └── edit/page.tsx # 글 수정
│       ├── components/      # React 컴포넌트
│       │   └── CommentSection.tsx
│       ├── lib/api.ts       # API 호출 함수
│       └── types/board.ts   # TypeScript 타입
├── .claude/
│   ├── commands/            # Claude Code 슬래시 커맨드
│   └── hooks/               # Claude Code 훅
├── CLAUDE.md
└── README.md
```

## Getting Started

### 1. 데이터베이스 설정

Supabase SQL Editor에서 `backend/schema.sql` 실행:

```sql
-- 게시글 테이블
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author_name VARCHAR(100) NOT NULL DEFAULT '익명',
    password VARCHAR(255) NOT NULL,
    view_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 댓글 테이블 (대댓글 지원)
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    parent_id INTEGER REFERENCES comments(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    author_name VARCHAR(100) NOT NULL DEFAULT '익명',
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS 정책
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable all for posts" ON posts FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable all for comments" ON comments FOR ALL USING (true) WITH CHECK (true);
```

### 2. 환경변수 설정

```bash
cd backend
cp .env.example .env
# .env 파일에 SUPABASE_URL과 SUPABASE_KEY 입력
```

### 3. Backend 실행

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 9010
```

### 4. Frontend 실행

```bash
cd frontend
npm install
npm run dev
```

## Ports

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3010 |
| Backend API | http://localhost:9010 |
| API Docs (Swagger) | http://localhost:9010/docs |

## API Endpoints

### 기본

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |

### 게시글 (Posts)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/posts | 게시글 목록 조회 (최신순) |
| GET | /api/posts/{id} | 게시글 상세 조회 (조회수 증가) |
| POST | /api/posts | 게시글 등록 |
| PUT | /api/posts/{id} | 게시글 수정 (비밀번호 필요) |
| DELETE | /api/posts/{id} | 게시글 삭제 (비밀번호 필요) |
| POST | /api/posts/{id}/verify-password | 비밀번호 검증 |

### 댓글 (Comments)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/posts/{post_id}/comments | 댓글 목록 조회 |
| POST | /api/posts/{post_id}/comments | 댓글/대댓글 등록 |
| PUT | /api/comments/{id} | 댓글 수정 (비밀번호 필요) |
| DELETE | /api/comments/{id} | 댓글 삭제 (비밀번호 필요) |

### Items (샘플)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/items | Get all items |
| GET | /api/items/{id} | Get item by ID |
| POST | /api/items | Create item |
| DELETE | /api/items/{id} | Delete item |

## 테스트

```bash
cd backend
source venv/bin/activate
python -m pytest -v                        # 전체 테스트
python -m pytest tests/test_posts.py -v    # 게시글 테스트만
python -m pytest tests/test_comments.py -v # 댓글 테스트만
```

## 개발 방식

- **Backend**: TDD (Test-Driven Development) - Red/Green/Refactor 사이클
- **Frontend**: Next.js App Router + TypeScript

## MCP Servers

이 프로젝트는 다음 MCP 서버를 사용합니다:

- **Playwright**: 브라우저 자동화
- **Notion**: 노션 연동 (NOTION_TOKEN 환경변수 필요)
- **Supabase**: 데이터베이스 관리
