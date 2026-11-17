#!/usr/bin/env bash
# 시술현황 시안 컴포넌트 세트 → medikit.fig 「components」 페이지(앱 모드 · 활성 문서). 다시 돌리면 같은 결과(멱등).
#   1) _vars.js   시안 변수(status/* · crm/*)를 컬렉션 medikit 에 추가(있으면 그대로)
#   2) _reset.js  「components」 페이지를 비운다(페이지는 지우지 않는다)
#   3) 세트 스크립트를 순서대로 — 순서가 계약이다(뒤 세트가 앞 세트를 inst() 로 쓴다)
# ⚠ eval 은 한 번에 하나만(병렬 eval 이 앱 엔진을 망가뜨린 적 있다 · 2026-11-12). 한 eval 20초 안.
# 끝에 「components」 노드 수를 찍는다(두 번 돌려 같으면 멱등).
set -euo pipefail
cd "$(dirname "$0")"
OP="bun $HOME/.bun/bin/openpencil"
# 기본 = headless: medikit.fig 파일에 직접 쓴다(eval <파일> -w). 앱에서 열려 있으면 앱 탭을 저장 없이 닫고 돌린 뒤 다시 연다.
# PENCIL_FILE=app 이면 앱 모드(비권장 — 앱 WASM 메모리 오류 3회 · 2026-11-12).
export PENCIL_FILE="${PENCIL_FILE:-$(cd .. && pwd)/medikit.fig}"
if [ "$PENCIL_FILE" = app ]; then EVAL=(eval --stdin); else EVAL=(eval "$PENCIL_FILE" -w --stdin); fi
echo "vars: $($OP "${EVAL[@]}" < _vars.js | tr -d '\n ')"
$OP "${EVAL[@]}" < _reset.js >/dev/null
ORDER=(
  Icon Checkbox SelectAll Search Textarea          # G1 기본 입력류
  Badge Avatar Tooltip Notify                       # G2 배지 · 아바타 · 알림
  Button IconButton Tab MenuRow                     # G3 버튼 · 탭 · 메뉴 줄
  ProcRow LinkBar RoomCard                          # G4 방 카드
  CardRow InboxSectionHead InboxCard EmptyState     # G5 인박스
  PopOption Popover ComboOption MoreMenu ChartModal ConfirmDialog  # G6 팝오버 · 모달
)
./run-one.sh "${ORDER[@]}"
printf '%s' 'const p=figma.root.children.find(x=>x.name==="components"); let n=0; const w=(x)=>{n++; if("children" in x) for(const c of x.children) w(c);}; for(const c of p.children) w(c); ({sections:p.children.length, nodes:n})' | $OP "${EVAL[@]}" | tr -d '\n '
echo
