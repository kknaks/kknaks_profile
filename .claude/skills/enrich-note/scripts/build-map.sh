#!/usr/bin/env bash
# enrich-note SKILL helper: persona/_map.md 갱신.
#
# 단일 파일 enrich 후 매번 호출. 또는 일괄 처리 끝에 한 번만 호출.
#
# Skip 옵션: ENRICH_SKIP_MAP=1 환경 변수 시 no-op (loop 처리 중 매번 갱신 회피용).

set -euo pipefail

if [[ "${ENRICH_SKIP_MAP:-0}" == "1" ]]; then
  echo "// build-map skipped (ENRICH_SKIP_MAP=1)"
  exit 0
fi

# CLAUDE_PROJECT_DIR 가 박혀있으면 사용, 아니면 스크립트 위치에서 추정
if [[ -n "${CLAUDE_PROJECT_DIR:-}" ]]; then
  REPO="${CLAUDE_PROJECT_DIR}"
else
  REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
fi

MAP_SCRIPT="${REPO}/scripts/build_persona_map.py"
PYTHON="${REPO}/back/.venv/bin/python"

if [[ ! -x "${PYTHON}" ]]; then
  PYTHON="python3"
fi

if [[ ! -f "${MAP_SCRIPT}" ]]; then
  echo "! build_persona_map.py not found: ${MAP_SCRIPT}" >&2
  exit 1
fi

"${PYTHON}" "${MAP_SCRIPT}"
