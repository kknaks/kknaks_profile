#!/usr/bin/env bash
# 시술현황 화면 정의서 맵 → medikit.fig 「시술현황 맵」 페이지(headless · 파일에 직접 쓰기). 다시 돌리면 같은 결과(멱등).
#   0) 백업 medikit.before-map.fig(없을 때만 — 맵을 처음 그리기 전 상태를 지킨다)
#   1) 「시술현황 맵」 페이지를 지운다(다른 페이지 · 변수 · 세트는 건드리지 않는다)
#   2) 섹션 스크립트를 순서대로(eval 한 번에 하나 · 직렬) → 3) edges.js(화살표 · 마지막)
#   4) 맵 노드 수 · info
# 데이터 원본 = screens.json · edges.json · notes.json · layout.json(gen-layout.py 생성). 캔버스는 결과물이다.
# ⚠ 앱 모드 eval 금지(앱 WASM 메모리 오류 3회 · 2026-11-12). 앱에 이 파일이 열려 있으면 저장 없이 닫고 돌린 뒤 다시 연다.
set -euo pipefail
cd "$(dirname "$0")"
OP="bun $HOME/.bun/bin/openpencil"
export PENCIL_FILE="${PENCIL_FILE:-$(cd ../medikit && pwd)/medikit.fig}"
BACKUP="$(dirname "$PENCIL_FILE")/medikit.before-map.fig"
[ -f "$BACKUP" ] || cp "$PENCIL_FILE" "$BACKUP"
EVAL=(eval "$PENCIL_FILE" -w --stdin)

printf '%s' 'const p = figma.root.children.find((x) => x.name === "시술현황 맵"); if (p) p.remove(); "reset";' | $OP "${EVAL[@]}" >/dev/null

ORDER=(1-1a 1-1b 1-2 1-3 2-1 2-2 3-1 3-2 4-1 4-2 5-1 6-1 7-1 M)
./run-section.sh "${ORDER[@]}"

out=$( { printf 'globalThis.TARGET_PAGE = "components";\nconst DATA = { edges: %s };\n' "$(cat edges.json)"; cat ../medikit/components/_icons.js ../medikit/components/_lib.js edges.js; } | $OP "${EVAL[@]}" 2>&1 ) || true
case "$out" in *rror*|*"timed out"*) echo "edges: $out" >&2; exit 1;; *) echo "edges: $out";; esac

printf '%s' 'const p=figma.root.children.find(x=>x.name==="시술현황 맵"); let n=0, inst=0, scr=0, mk=0, nt=0, ed=0; const w=(x)=>{n++; if(x.type==="INSTANCE") inst++; const m=x.name||""; if(m.startsWith("screen/")) scr++; else if(m.startsWith("marker/")) mk++; else if(m.startsWith("note/")) nt++; else if(m.startsWith("edge/")) ed++; if("children" in x) for(const c of x.children) w(c);}; for(const c of p.children) w(c); JSON.stringify({nodes:n, instances:inst, screens:scr, markers:mk, notes:nt, edges:ed})' | $OP eval "$PENCIL_FILE" --stdin | tr -d '\n '
echo
$OP info "$PENCIL_FILE" | sed -n '1,8p'
