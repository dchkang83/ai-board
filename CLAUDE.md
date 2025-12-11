# AI Board Project

## Project Overview
AI Board는 FastAPI 백엔드와 Next.js 프론트엔드로 구성된 웹 애플리케이션입니다.

## Tech Stack
- **Backend**: FastAPI (Python 3.11+), Pydantic, Uvicorn
- **Database**: Supabase (PostgreSQL)
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS
- **MCP Servers**: Playwright (브라우저 자동화), Notion (노션 연동), Supabase (DB 관리)

## Project Structure
```
ai-board/
├── backend/
│   ├── main.py           # FastAPI 앱 및 API 엔드포인트
│   ├── database.py       # Supabase 클라이언트 설정
│   ├── requirements.txt  # Python 의존성
│   ├── .env              # 환경변수 (git 제외)
│   ├── .env.example      # 환경변수 예시
│   ├── pytest.ini        # pytest 설정
│   ├── tests/            # 테스트 디렉토리
│   │   ├── conftest.py   # pytest fixtures
│   │   └── test_*.py     # 테스트 파일들
│   └── venv/             # Python 가상환경
├── frontend/
│   ├── src/
│   │   └── app/
│   │       ├── layout.tsx    # 루트 레이아웃
│   │       ├── page.tsx      # 메인 페이지
│   │       └── globals.css   # 글로벌 스타일
│   ├── package.json
│   └── tailwind.config.js
├── .claude/
│   └── commands/
│       └── notion-dev.md # Notion 사양서 기반 개발 스킬
└── CLAUDE.md             # 프로젝트 문서
```

## API Endpoints
- `GET /health` - 서버 상태 확인
- `GET /api/items` - 모든 아이템 조회
- `GET /api/items/{id}` - 특정 아이템 조회
- `POST /api/items` - 아이템 생성
- `DELETE /api/items/{id}` - 아이템 삭제

## Common Commands

### Backend
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 9010
```

### Backend 테스트 (TDD)
```bash
cd backend
source venv/bin/activate
pytest                    # 전체 테스트 실행
pytest -v                 # 상세 출력
pytest --cov=.            # 커버리지 포함
pytest tests/test_xxx.py  # 특정 파일만 실행
```

### Frontend
```bash
cd frontend
npm run dev
```

## Ports
- Backend: http://localhost:9010
- Frontend: http://localhost:3010
- API Docs (Swagger): http://localhost:9010/docs

## Database Setup (Supabase)

### 1. Supabase 프로젝트 설정
1. [Supabase](https://supabase.com)에서 프로젝트 생성
2. Project Settings > API에서 URL과 anon key 확인

### 2. 환경변수 설정
```bash
cd backend
cp .env.example .env
# .env 파일에 SUPABASE_URL과 SUPABASE_KEY 입력
```

### 3. items 테이블 생성 (Supabase SQL Editor)
```sql
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);
```

## Slash Commands (Skills)

### /notion-dev
Notion 사양서를 읽고 개발을 진행하는 스킬

**사용법:**
```
/notion-dev <Notion 페이지 URL 또는 ID>
```

**예시:**
```
/notion-dev https://notion.so/my-spec-page-abc123
/notion-dev abc123def456
```

**기능:**
1. Notion 페이지에서 사양서 읽기
2. 요구사항/데이터모델/API 분석
3. 개발 범위 선택 (Frontend / Backend / Fullstack)
4. 자동 코드 생성 및 구현

## Backend 개발 방식 (TDD)

Backend는 TDD(Test-Driven Development) 방식으로 개발합니다.

### Red-Green-Refactor 사이클
1. **Red**: 실패하는 테스트 먼저 작성
2. **Green**: 테스트를 통과하는 최소한의 코드 작성
3. **Refactor**: 코드 정리 (테스트는 계속 통과해야 함)

### 테스트 작성 규칙
- 각 API 엔드포인트마다 테스트 작성
- 정상 케이스 + 에러 케이스 모두 커버
- 테스트 파일: `backend/tests/test_<기능>.py`

## Notes
- Backend과 Frontend는 CORS 설정으로 연동됨
- Node.js 18.x 사용 중 (Next.js 14 호환)
- Supabase 연동 시 .env 파일에 환경변수 필수 설정
- Backend 개발 시 반드시 테스트 먼저 작성 (TDD)
