#!/usr/bin/env bash
# 섹션 스크립트 하나씩 headless eval(파일에 직접 쓰기). 사용: ./run-section.sh <절> [<절> …]   예) ./run-section.sh 1-1a 1-2
# 한 이름 = eval 한 번(20초 제한) · 직렬. 앱 모드 금지(앱 WASM 메모리 오류 · 2026-11-12).
# 앞에 붙는 것: DATA(layout.json 의 그 섹션 + 화면 · 메모) → components/_icons.js · _lib.js(TARGET_PAGE=components) → _maplib.js → sections/<절>.js
set -euo pipefail
cd "$(dirname "$0")"
OP="bun $HOME/.bun/bin/openpencil"
FILE="${PENCIL_FILE:-$(cd ../medikit && pwd)/medikit.fig}"
[ -f "$FILE" ] || { echo "파일 없음: $FILE" >&2; exit 1; }
LIB=../medikit/components
for n in "$@"; do
  key="${n:0:1}"   # 1-1a → 1 · M → M
  [ -f "sections/$n.js" ] || { echo "스크립트 없음: sections/$n.js" >&2; exit 1; }
  data=$(python3 - "$key" <<'PY'
import json, sys
k = sys.argv[1]
L = json.load(open("layout.json")); S = json.load(open("screens.json")); N = json.load(open("notes.json"))
sec = next(s for s in L["sections"] if s["key"] == k)
ids = {s["screenId"] for s in sec["slots"]}
print(json.dumps({"section": sec, "screens": [s for s in S if s["screenId"] in ids], "notes": [x for x in N if x["screenId"] in ids]}, ensure_ascii=False))
PY
)
  start=$(date +%s)
  out=$( { printf 'globalThis.TARGET_PAGE = "components";\nconst DATA = %s;\n' "$data"; cat $LIB/_icons.js $LIB/_lib.js _maplib.js "sections/$n.js"; printf '\nJSON.stringify(mapDone());\n'; } | $OP eval "$FILE" -w --stdin 2>&1 ) || true
  sec=$(( $(date +%s) - start ))
  case "$out" in
    *"RPC timeout"*|*"timed out"*) echo "$n: 시간 초과(${sec}s) — 쪼개라" >&2; exit 2;;
    *rror*) echo "$n: $out" >&2; exit 1;;
    *) echo "$n (${sec}s): $out";;
  esac
done
