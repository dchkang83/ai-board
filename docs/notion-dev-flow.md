# /notion-dev 스킬 실행 흐름

## 개요

Notion에 작성된 사양서를 읽고 자동으로 개발을 진행하는 스킬입니다.

## 사용법

```
/notion-dev <Notion 페이지 URL 또는 ID>
```

**예시:**
```
/notion-dev https://notion.so/my-spec-page-abc123
/notion-dev abc123def456
```

---

## 실행 흐름

### 1단계: Notion 사양서 읽기

```
Notion MCP 사용
├── mcp__notion__API-retrieve-a-page (페이지 정보)
├── mcp__notion__API-get-block-children (블록 내용)
└── 하위 페이지가 있으면 재귀적으로 읽기
```

**읽어오는 내용:**
- 페이지 제목
- 본문 텍스트
- 체크리스트, 테이블 등 모든 블록
- 연결된 하위 페이지

---

### 2단계: 사양 분석

사양서에서 다음 항목을 파악합니다:

| 항목 | 설명 | 예시 |
|------|------|------|
| 기능 요구사항 | 구현해야 할 기능 목록 | 회원가입, 로그인, 게시글 작성 |
| 데이터 모델 | 테이블/스키마 구조 | users(id, email, name) |
| API 설계 | 필요한 엔드포인트 | POST /api/users, GET /api/posts |
| UI/UX | 화면 구성 및 흐름 | 로그인 페이지 → 대시보드 |
| 기술 스택 | 특별히 지정된 기술 | (기본: FastAPI, Next.js, Supabase) |

---

### 3단계: 개발 범위 확인

사용자에게 질문:

```
"어떤 범위로 개발할까요?"

┌─────────────┬────────────────────────────────┐
│ Frontend    │ Next.js + TypeScript + Tailwind│
├─────────────┼────────────────────────────────┤
│ Backend     │ FastAPI + Python (TDD 방식)    │
├─────────────┼────────────────────────────────┤
│ Fullstack   │ Frontend + Backend 둘 다       │
└─────────────┴────────────────────────────────┘
```

---

### 4단계: 작업 계획 수립

TodoWrite를 사용하여 구체적인 작업 목록 생성:

**예시 (Fullstack 선택 시):**

```
□ Supabase에 users 테이블 생성
□ [Red] POST /api/users 테스트 작성
□ [Green] POST /api/users 엔드포인트 구현
□ [Refactor] 코드 정리
□ [Red] GET /api/users 테스트 작성
□ [Green] GET /api/users 엔드포인트 구현
□ Frontend 회원가입 페이지 구현
□ Frontend 회원목록 페이지 구현
□ API 연동 테스트
```

---

### 5단계: 구현

#### Backend (TDD 방식)

```
┌─────────────────────────────────────────────────────────┐
│                    TDD 사이클                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌───────┐      ┌───────┐      ┌──────────┐           │
│   │  Red  │ ───► │ Green │ ───► │ Refactor │ ──┐       │
│   └───────┘      └───────┘      └──────────┘   │       │
│       ▲                                         │       │
│       └─────────────────────────────────────────┘       │
│                                                         │
└─────────────────────────────────────────────────────────┘

1. Red (실패하는 테스트 작성)
   └── tests/test_users.py 작성
   └── pytest 실행 → 실패 확인

2. Green (테스트 통과하는 최소 코드)
   └── main.py에 엔드포인트 구현
   └── pytest 실행 → 통과 확인

3. Refactor (코드 정리)
   └── 중복 제거, 가독성 개선
   └── pytest 실행 → 여전히 통과 확인
```

**파일 구조:**
```
backend/
├── main.py              # API 엔드포인트
├── database.py          # Supabase 연결
└── tests/
    ├── conftest.py      # pytest fixtures
    ├── test_health.py   # 헬스체크 테스트
    └── test_users.py    # 새로 추가되는 테스트
```

#### Frontend

```
frontend/src/
├── app/
│   ├── page.tsx              # 메인 페이지
│   ├── users/
│   │   └── page.tsx          # 회원 목록 페이지
│   └── signup/
│       └── page.tsx          # 회원가입 페이지
└── components/
    └── UserForm.tsx          # 재사용 컴포넌트
```

#### Database (Supabase)

```sql
-- Supabase MCP 또는 SQL Editor로 실행
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

### 6단계: 검증

```
검증 항목:
├── pytest 실행 → 모든 테스트 통과
├── 타입 에러 없음 확인
├── API 연동 정상 동작 확인
└── 기존 코드 스타일과 일관성 확인
```

---

## 예시 시나리오

### Notion 사양서 예시

```markdown
# 회원 관리 기능

## 기능 요구사항
- 회원 가입
- 회원 목록 조회
- 회원 정보 수정
- 회원 탈퇴

## 데이터 모델
| 필드 | 타입 | 설명 |
|------|------|------|
| id | int | PK |
| email | string | 이메일 (unique) |
| name | string | 이름 |
| created_at | timestamp | 생성일 |

## API
- POST /api/users - 회원 생성
- GET /api/users - 회원 목록
- GET /api/users/{id} - 회원 상세
- PATCH /api/users/{id} - 회원 수정
- DELETE /api/users/{id} - 회원 삭제
```

### 실행 결과

```
/notion-dev https://notion.so/user-management

[1/6] Notion 사양서 읽기 완료
      - 기능: 회원 가입, 목록, 수정, 삭제
      - 테이블: users (id, email, name, created_at)
      - API: 5개 엔드포인트

[2/6] 사양 분석 완료

[3/6] 개발 범위 선택
      → 사용자: "Fullstack"

[4/6] 작업 계획 생성 (TodoWrite)
      □ Supabase users 테이블 생성
      □ [Red] POST /api/users 테스트
      □ [Green] POST /api/users 구현
      ... (총 12개 작업)

[5/6] 구현 진행
      ✓ 테이블 생성 완료
      ✓ Backend TDD 완료 (5개 엔드포인트)
      ✓ Frontend 페이지 완료

[6/6] 검증
      ✓ pytest 통과 (12 passed)
      ✓ 타입 에러 없음
      ✓ API 연동 정상
```

---

## 주의사항

1. **기존 코드 스타일 준수** - 프로젝트 컨벤션 따르기
2. **TDD 필수 (Backend)** - 테스트 없이 구현하지 않음
3. **보안 고려** - SQL Injection, XSS 등 방지
4. **최소 구현** - 요청된 기능만 구현, 과도한 추상화 금지

---

## 관련 파일

- 스킬 정의: `.claude/commands/notion-dev.md`
- 프로젝트 문서: `CLAUDE.md`
- Backend 테스트: `backend/tests/`
