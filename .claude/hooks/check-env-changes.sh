#!/bin/bash
# Hook: 환경 설정 변경 감지 시 Claude에게 README.md 업데이트 요청
# 이 스크립트는 Claude Code의 PostToolUse hook으로 실행됩니다.

# stdin에서 JSON 입력 읽기
INPUT=$(cat)

# 도구 이름과 파일 경로 추출
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# 프로젝트 루트 디렉토리 (스크립트 위치 기준)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# 환경 설정 관련 패턴
ENV_PATTERNS=(
    "\.env"
    "\.env\."
    "config\."
    "settings\."
    "\.claude"
    "mcp"
    "requirements\.txt"
    "package\.json"
    "docker"
    "Dockerfile"
    "docker-compose"
    "schema\.sql"
    "main\.py"
)

# 파일 경로가 환경 설정 관련인지 확인
check_env_file() {
    local path="$1"
    for pattern in "${ENV_PATTERNS[@]}"; do
        if echo "$path" | grep -qiE "$pattern"; then
            return 0
        fi
    done
    return 1
}

# MCP 명령어인지 확인
check_mcp_command() {
    local cmd="$1"
    if echo "$cmd" | grep -qE "claude mcp (add|remove|add-json)"; then
        return 0
    fi
    return 1
}

# Claude에게 README.md 업데이트 요청 (block하지 않음)
request_readme_update() {
    local reason="$1"
    local details="$2"

    # JSON 출력으로 Claude에게 작업 요청
    cat << EOF
{
  "result": "continue",
  "message": "[Hook] $reason\n\n**README.md 업데이트가 필요합니다.**\n변경 내용: $details\n\nREADME.md 파일에 다음 내용을 반영해주세요:\n- 새로운 API 엔드포인트\n- 변경된 설치/실행 방법\n- 새로운 환경변수\n- 데이터베이스 스키마 변경사항"
}
EOF
}

# Write/Edit 도구로 환경 설정 파일이 변경된 경우
if [[ "$TOOL_NAME" == "Write" || "$TOOL_NAME" == "Edit" ]]; then
    if check_env_file "$FILE_PATH"; then
        # README.md 자체 수정은 무시
        if echo "$FILE_PATH" | grep -qiE "README\.md|CLAUDE\.md"; then
            echo "{}"
            exit 0
        fi

        request_readme_update "환경 설정 파일이 변경되었습니다" "$FILE_PATH"
        exit 0
    fi
fi

# Bash 도구로 MCP 관련 명령이 실행된 경우
if [[ "$TOOL_NAME" == "Bash" ]]; then
    if check_mcp_command "$COMMAND"; then
        request_readme_update "MCP 서버 설정이 변경되었습니다" "$COMMAND"
        exit 0
    fi
fi

# 해당 없으면 빈 출력
echo "{}"
