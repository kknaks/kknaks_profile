#!/usr/bin/env bash
# 컴포넌트 스크립트를 하나씩 eval(앱 모드 · 활성 문서). 사용:
#   ./run-one.sh [--page <페이지>] [--reset] <Name> [<Name> …]
#   --page  대상 페이지(기본 components). 서브에이전트 시험 = --page draft/<그룹>
#   --reset 대상 페이지를 먼저 비운다(없으면 만든다)
# 한 이름 = eval 한 번(20초 제한). 앞 이름이 만든 세트를 뒤 이름이 inst() 로 쓴다 → 의존 순서대로 적는다.
# headless(기본 · 2026-11-12 코디): PENCIL_FILE=<.fig> 이면 앱이 아니라 그 파일에 eval -w 로 쓴다.
#   앱 모드(PENCIL_FILE=app)는 같은 세션에서 생성·삭제를 반복하면 앱 WASM 메모리가 깨져(Out of bounds memory access) 쓰지 않는다.
set -euo pipefail
cd "$(dirname "$0")"
OP="bun $HOME/.bun/bin/openpencil"
PAGE=components; RESET=0; NAMES=()
while [ $# -gt 0 ]; do case "$1" in --page) PAGE="$2"; shift 2;; --reset) RESET=1; shift;; *) NAMES+=("$1"); shift;; esac; done
FILE="${PENCIL_FILE:-$(cd .. && pwd)/medikit.fig}"
if [ "$FILE" = app ]; then EVAL=(eval --stdin); $OP documents list | grep -q 'medikit/medikit.fig' || { echo "활성 문서가 medikit.fig 가 아니다" >&2; exit 1; }
else [ -f "$FILE" ] || { echo "파일 없음: $FILE" >&2; exit 1; }; EVAL=(eval "$FILE" -w --stdin); fi
if [ $RESET = 1 ]; then
  printf 'const N=%s; for (const p of [...figma.root.children]) if (p.name===N) { for (const c of [...p.children]) c.remove(); }\nlet p=figma.root.children.find(x=>x.name===N); if(!p){p=figma.createPage(); p.name=N;} p.backgrounds=[{type:"SOLID",color:{r:1,g:1,b:1},opacity:1}]; "reset "+N;' "\"$PAGE\"" | $OP "${EVAL[@]}" >/dev/null
fi
for n in "${NAMES[@]}"; do
  start=$(date +%s)
  out=$( { printf 'globalThis.TARGET_PAGE = "%s";\n' "$PAGE"; cat _icons.js _lib.js "$n.js"; } | $OP "${EVAL[@]}" 2>&1 ) || true
  sec=$(( $(date +%s) - start ))
  case "$out" in
    *"RPC timeout"*|*"timed out"*) echo "$n: 시간 초과(${sec}s) — 쪼개라" >&2; exit 2;;
    *rror*) echo "$n: $out" >&2; exit 1;;
    *) echo "$n (${sec}s): $(echo "$out" | tr -d '\n ' | head -c 200)";;
  esac
done
