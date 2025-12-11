# Notion 사양서 기반 개발 스킬

Notion 페이지에서 사양서를 읽고 개발을 진행합니다.

## 입력
- $ARGUMENTS: Notion 페이지 URL 또는 페이지 ID

## 실행 절차

### 1단계: Notion 사양서 읽기
1. Notion MCP를 사용하여 페이지 내용을 가져옵니다
2. 페이지의 모든 블록(children)을 재귀적으로 읽습니다
3. 하위 페이지가 있다면 함께 읽습니다

### 2단계: 사양 분석
다음 항목을 파악합니다:
- **기능 요구사항**: 구현해야 할 기능 목록
- **데이터 모델**: 필요한 테이블/스키마 구조
- **API 설계**: 필요한 엔드포인트
- **UI/UX**: 화면 구성 및 사용자 흐름
- **기술 스택**: 특별히 지정된 기술이 있는지

### 3단계: 개발 범위 확인
사용자에게 질문합니다:
- Frontend만 개발할지
- Backend만 개발할지
- Fullstack으로 둘 다 개발할지

### 4단계: 작업 계획 수립
TodoWrite를 사용하여 구체적인 작업 목록을 생성합니다.

### 5단계: 구현

#### Frontend (Next.js + TypeScript + Tailwind CSS)
- 경로: `frontend/src/`
- 컴포넌트: `frontend/src/components/`
- 페이지: `frontend/src/app/`
- API 호출: fetch 또는 필요시 라이브러리 추가

#### Backend (FastAPI + Python) - TDD 방식
- 경로: `backend/`
- 테스트: `backend/tests/`
- 엔드포인트: `backend/main.py` 또는 라우터 분리
- 데이터베이스: Supabase (PostgreSQL)
- 스키마: Supabase MCP로 테이블 생성

**TDD 사이클 (Red-Green-Refactor):**
1. **Red**: 실패하는 테스트 먼저 작성
   - `backend/tests/test_*.py` 에 테스트 케이스 작성
   - pytest 실행하여 실패 확인
2. **Green**: 테스트를 통과하는 최소한의 코드 작성
   - 테스트가 통과할 만큼만 구현
   - pytest 실행하여 통과 확인
3. **Refactor**: 코드 정리 및 개선
   - 중복 제거, 가독성 개선
   - 테스트가 여전히 통과하는지 확인

**테스트 구조:**
```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py      # pytest fixtures
│   ├── test_*.py        # 테스트 파일들
├── main.py
└── ...
```

**테스트 실행:**
```bash
cd backend
source venv/bin/activate
pytest -v
pytest -v --cov=.  # 커버리지 포함
```

#### Database (Supabase)
- Supabase MCP를 사용하여 테이블 생성
- RLS(Row Level Security) 정책 설정 필요시 적용

### 6단계: 검증
- 코드가 기존 프로젝트 구조와 일관성 있는지 확인
- 타입 에러 없는지 확인
- API 연동이 올바른지 확인

## 프로젝트 컨텍스트
- Backend: FastAPI (port 9010)
- Frontend: Next.js 14 (port 3010)
- Database: Supabase
- 스타일링: Tailwind CSS

## 주의사항
- 기존 코드 스타일을 따릅니다
- 새 파일보다 기존 파일 수정을 우선합니다
- 불필요한 주석이나 console.log를 남기지 않습니다
- 보안 취약점(SQL injection, XSS 등)에 주의합니다
