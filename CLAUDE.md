# AI Board Project

## Project Overview
AI Board는 FastAPI 백엔드와 Next.js 프론트엔드로 구성된 웹 애플리케이션입니다.

## Tech Stack
- **Backend**: FastAPI (Python 3.11+), Pydantic, Uvicorn
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS
- **MCP Servers**: Playwright (브라우저 자동화), Notion (노션 연동)

## Project Structure
```
ai-board/
├── backend/
│   ├── main.py           # FastAPI 앱 및 API 엔드포인트
│   ├── requirements.txt  # Python 의존성
│   └── venv/             # Python 가상환경
├── frontend/
│   ├── src/
│   │   └── app/
│   │       ├── layout.tsx    # 루트 레이아웃
│   │       ├── page.tsx      # 메인 페이지
│   │       └── globals.css   # 글로벌 스타일
│   ├── package.json
│   └── tailwind.config.js
├── .claude/              # Claude Code 설정
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

### Frontend
```bash
cd frontend
npm run dev
```

## Ports
- Backend: http://localhost:9010
- Frontend: http://localhost:3010
- API Docs (Swagger): http://localhost:9010/docs

## Notes
- Backend과 Frontend는 CORS 설정으로 연동됨
- Node.js 18.x 사용 중 (Next.js 14 호환)
