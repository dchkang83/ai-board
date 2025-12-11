#!/bin/bash
# Hook: 환경 설정 변경 감지 및 README.md, .gitignore 업데이트 알림
# 이 스크립트는 Claude Code의 PostToolUse hook으로 실행됩니다.

# stdin에서 JSON 입력 읽기
INPUT=$(cat)

# 도구 이름과 파일 경로 추출
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

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

# 메시지 출력 함수
output_message() {
    local msg="$1"
    echo "{\"result\": \"continue\", \"message\": \"$msg\"}"
}

# Write/Edit 도구로 환경 설정 파일이 변경된 경우
if [[ "$TOOL_NAME" == "Write" || "$TOOL_NAME" == "Edit" ]]; then
    if check_env_file "$FILE_PATH"; then
        output_message "[Hook] 환경 설정 파일이 변경되었습니다: $FILE_PATH - README.md와 .gitignore 업데이트를 고려하세요."
        exit 0
    fi
fi

# Bash 도구로 MCP 관련 명령이 실행된 경우
if [[ "$TOOL_NAME" == "Bash" ]]; then
    if check_mcp_command "$COMMAND"; then
        output_message "[Hook] MCP 서버 설정이 변경되었습니다 - README.md 업데이트를 고려하세요."
        exit 0
    fi
fi

# 해당 없으면 빈 출력
echo "{}"
