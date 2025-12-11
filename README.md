# AI Board

FastAPI 백엔드와 Next.js 프론트엔드로 구성된 웹 애플리케이션입니다.

## Tech Stack

- **Backend**: FastAPI, Python 3.11+, Pydantic, Uvicorn
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm

## Getting Started

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 9010
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Ports

| Service | URL |
|---------|-----|
| Backend API | http://localhost:9010 |
| Frontend | http://localhost:3010 |
| API Docs (Swagger) | http://localhost:9010/docs |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |
| GET | /api/items | Get all items |
| GET | /api/items/{id} | Get item by ID |
| POST | /api/items | Create item |
| DELETE | /api/items/{id} | Delete item |

## MCP Servers

이 프로젝트는 다음 MCP 서버를 사용합니다:

- **Playwright**: 브라우저 자동화
- **Notion**: 노션 연동 (NOTION_TOKEN 환경변수 필요)

## Project Structure

```
ai-board/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── venv/
├── frontend/
│   ├── src/app/
│   ├── package.json
│   └── tailwind.config.js
├── .claude/
│   ├── hooks/
│   └── settings.local.json
├── CLAUDE.md
└── README.md
```
