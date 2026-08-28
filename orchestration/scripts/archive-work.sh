#!/usr/bin/env bash
# archive-work.sh — 오케스트레이션 작업 정리·아카이브 (new-work.sh 의 짝, config 기반)
#
#   scripts/archive-work.sh <project> <slug> [--dry-run] [--yes]
#
# 하는 일 (안전 우선 — 검사 실패 시 아무것도 지우지 않고 멈춘다):
#   1. config 로드 → 이 slug 의 워크트리 경로들 계산 (use_worktree=false repo 는 건너뜀)
#   2. [검사] 각 워크트리: 미커밋 변경(untracked 제외) 있으면 중단
#   3. [검사] 각 워크트리의 브랜치: upstream/pr_base 에 미머지 커밋 있으면 중단
#      (detached HEAD 는 브랜치 검사 생략)
#   4. [검사] 로컬 docker 스택이 이 워크트리를 마운트 중이면 중단 (스택 먼저 옮겨라)
#   5. SUMMARY.md 스켈레톤 생성 (templates/work-summary.md, 기간·커밋 자동) —
#      워크트리 제거 전에 만든다. §2 가 안 채워져 있으면 여기서 멈춘다
#   6. 워크트리에 붙은 orca 터미널 전부 close
#   7. git worktree remove (+ 로컬 브랜치 삭제, 원격 브랜치는 --yes 일 때만 삭제)
#   8. work/<slug>/ → work/_archive/<project>/<slug>/ 이동 + git 커밋
#
# --dry-run: 검사·계획만 출력, 아무것도 안 지움
# --yes:     원격 브랜치 삭제까지 수행 (기본은 로컬만)
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_DIR="$HERE/config"

die() { echo "ERROR: $*" >&2; exit 1; }
say() { echo "  $*"; }

PROJECT=""; SLUG=""; DRY=0; YES=0
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1 ;;
    --yes) YES=1 ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    -*) die "unknown option: $1" ;;
    *) if [ -z "$PROJECT" ]; then PROJECT="$1"
       elif [ -z "$SLUG" ]; then SLUG="$1"
       else die "인자가 너무 많다: $1"; fi ;;
  esac
  shift
done

[ -n "$PROJECT" ] && [ -n "$SLUG" ] || {
  echo "사용법: $0 <project> <slug> [--dry-run] [--yes]"
  echo "사용 가능한 project:"; ls "$CONFIG_DIR/projects" | sed 's/\.json$//;s/^/  - /'
  exit 1
}

PROJECT_JSON="$CONFIG_DIR/projects/$PROJECT.json"
[ -f "$PROJECT_JSON" ] || die "설정 없음: $PROJECT_JSON"
command -v orca >/dev/null || die "orca CLI 없음"

WORK_DIR="$HERE/work/$SLUG"
ARCHIVE_DIR="$HERE/work/_archive/$PROJECT/$SLUG"
[ -d "$WORK_DIR" ] || say "⚠ work/$SLUG 없음 — 워크트리 정리만 진행"
[ -d "$ARCHIVE_DIR" ] && die "아카이브가 이미 있다: $ARCHIVE_DIR"

# ── config → 이 slug 의 (canonical, 워크트리경로, pr_base) 목록 ────────────────
PLAN="$(python3 - "$PROJECT_JSON" "$SLUG" <<'PY'
import json, sys
cfg = json.load(open(sys.argv[1])); slug = sys.argv[2]
if not cfg.get('use_worktree', True):
    sys.exit(0)  # canonical 직접 작업 프로젝트 — 지울 워크트리 없음
root = cfg['worktree_root']
for name, repo in cfg['repos'].items():
    wt = f"{root}/{repo['orca_name']}/{slug}{repo.get('worktree_suffix','')}"
    print('\t'.join([repo['canonical_path'], wt, repo.get('pr_base','')]))
PY
)"

echo "== archive-work: $PROJECT / $SLUG $( [ $DRY = 1 ] && echo '(dry-run)' )"

# ── 검사 단계 (전부 통과해야 파괴 단계 진입) ──────────────────────────────────
STACK_MOUNTS="$(docker ps -q 2>/dev/null | xargs -r docker inspect --format '{{range .Mounts}}{{.Source}} {{end}}' 2>/dev/null || true)"

TARGETS=()  # "canonical<TAB>worktree<TAB>branch<TAB>pr_base" 실재하는 것만
while IFS=$'\t' read -r CANON WT PRBASE; do
  [ -n "${WT:-}" ] || continue
  if [ ! -d "$WT" ]; then say "skip (워크트리 없음): $WT"; continue; fi
  if ! git -C "$WT" rev-parse --git-dir >/dev/null 2>&1; then
    say "⚠ skip (git 워크트리 아님 — 잔존 디렉토리, 수동 확인 필요): $WT"
    continue
  fi

  # 미커밋 검사 (untracked 제외 — 리포트 파일 등은 허용)
  DIRTY=$(git -C "$WT" status --porcelain | grep -cv '^??' || true)
  [ "$DIRTY" = "0" ] || die "미커밋 변경 $DIRTY 건: $WT — 커밋/폐기 후 다시 실행"

  # 미머지 검사 (detached 면 생략)
  BR=$(git -C "$WT" branch --show-current || true)
  if [ -n "$BR" ] && [ -n "$PRBASE" ]; then
    git -C "$WT" fetch origin "$PRBASE" --quiet 2>/dev/null || true
    AHEAD=$(git -C "$WT" rev-list --count "origin/$PRBASE..HEAD" 2>/dev/null || echo "?")
    if [ "$AHEAD" != "0" ]; then
      # squash 머지면 커밋은 남아도 내용은 들어가 있을 수 있다 — 트리 동일성으로 재검사
      if git -C "$WT" diff --quiet "origin/$PRBASE" HEAD -- 2>/dev/null; then
        say "브랜치 $BR: origin/$PRBASE 대비 커밋 ${AHEAD}건 앞서지만 내용 동일(squash 머지) — 통과"
      else
        die "미머지 의심: $WT ($BR 이 origin/$PRBASE 보다 ${AHEAD}건 앞서고 내용도 다름) — 머지 확인 후 다시"
      fi
    fi
  fi

  # 로컬 스택 마운트 검사
  case "$STACK_MOUNTS" in *"$WT"*) die "로컬 docker 스택이 마운트 중: $WT — 스택을 먼저 옮겨라" ;; esac

  TARGETS+=("$CANON"$'\t'"$WT"$'\t'"$BR"$'\t'"$PRBASE")
done <<< "$PLAN"

# ── SUMMARY.md 스켈레톤 (templates/work-summary.md 렌더) ──────────────────────
# 잔디 잡이 읽는 회고다. **워크트리를 지우기 전에** 만든다 — 커밋 목록이 워크트리에 있다.
# 스크립트는 사실값(기간·커밋)만 채우고 멈춘다. §2 「적용한 기술·개념」은 판단이라
# 기계가 못 쓴다. 코디네이터가 채우기 전에는 아카이브로 넘어가지 않는다(아래 게이트).
SUMMARY="$WORK_DIR/SUMMARY.md"
SUMMARY_TEMPLATE="$HERE/templates/work-summary.md"
if [ -d "$WORK_DIR" ] && [ ! -f "$SUMMARY" ]; then
  [ -f "$SUMMARY_TEMPLATE" ] || die "템플릿 없음: $SUMMARY_TEMPLATE"
  START="$(git -C "$HERE" log --diff-filter=A --format=%ad --date=short -1 -- "work/$SLUG" 2>/dev/null | head -1)"
  [ -n "$START" ] || START="$(date -r "$WORK_DIR" +%Y-%m-%d 2>/dev/null || date +%Y-%m-%d)"
  COMMITS=""
  for T in "${TARGETS[@]:-}"; do
    [ -n "$T" ] || continue
    WT=$(echo "$T" | cut -f2); BR=$(echo "$T" | cut -f3); PRB=$(echo "$T" | cut -f4)
    [ -n "$BR" ] && [ -n "$PRB" ] || continue
    C="$(git -C "$WT" log --format='  - `%h` %s' "origin/$PRB..HEAD" 2>/dev/null || true)"
    [ -n "$C" ] && COMMITS="$COMMITS
- \`$BR\` → \`$PRB\`
$C"
  done
  [ -n "$COMMITS" ] || COMMITS="- 커밋: <없음 — 조사 전용 작업이면 그대로 둔다>"
  awk 'f{print} /^---$/{f=1}' "$SUMMARY_TEMPLATE" \
  | SLUG="$SLUG" PROJECT="$PROJECT" START="$START" END="$(date +%Y-%m-%d)" \
    COMMITS="$COMMITS" python3 -c "
import os, sys
t = sys.stdin.read()
e = os.environ
for k, v in {
    '<SLUG>': e['SLUG'], '<PROJECT>': e['PROJECT'],
    '<시작일>': e['START'], '<종료일>': e['END'],
    '<PR목록>': '- spec PR: <링크>\n- code PR: <링크>',
    '<커밋목록>': e['COMMITS'],
}.items():
    t = t.replace(k, v)
sys.stdout.write(t)
" > "$SUMMARY"
  say "SUMMARY.md 생성 (기간 $START ~ $(date +%Y-%m-%d), 커밋 자동 수집) — §1~§4·§7 은 코디가 채운다"
fi

# 이 워크트리들에 붙은 orca 터미널
TERMS="$(orca terminal list --json 2>/dev/null | python3 -c "
import json,sys
slug='$SLUG'
try: ts=json.load(sys.stdin)['result']['terminals']
except Exception: ts=[]
for t in ts:
    p=t.get('worktreePath','')
    # 현재 코디네이터 세션은 아카이브 실행 주체이므로 닫지 않는다.
    # 같은 slug 의 외부 repo 워커/서버 터미널만 정리한다.
    if t.get('handle') == '${ORCA_TERMINAL_HANDLE:-}':
        continue
    if ('/'+slug) in p or p.endswith(slug) or (slug+'-') in p.split('/')[-1]:
        print(t['handle'])" || true)"

echo "-- 계획:"
for T in "${TARGETS[@]:-}"; do [ -n "$T" ] && say "워크트리 제거: $(echo "$T" | cut -f2) (브랜치: $(echo "$T" | cut -f3))"; done
[ -n "$TERMS" ] && say "터미널 close: $(echo "$TERMS" | tr '\n' ' ')"
[ -d "$WORK_DIR" ] && say "아카이브: work/$SLUG → work/_archive/$PROJECT/$SLUG"

[ $DRY = 1 ] && { echo "== dry-run 끝 (워크트리·터미널 변경 없음. SUMMARY.md 는 깔아 뒀다)"; exit 0; }

# ── SUMMARY 게이트 ───────────────────────────────────────────────────────────
# §2 가 자리표시자 그대로면 멈춘다. 이 절이 비면 잔디는 「무엇을 완성했다」로 되돌아간다 —
# 원료가 없으니까. 아카이브는 되돌리기 번거로우므로 여기서 막는 게 싸다.
if [ -f "$SUMMARY" ] && grep -q '<기술·개념 이름>' "$SUMMARY"; then
  die "SUMMARY.md §2 「적용한 기술·개념」이 비어 있다: $SUMMARY
  → 이 작업에서 새로 쓴 것·판단이 갈린 것·막혔다가 푼 것을 채우고 다시 실행하라.
  → 정말 쓸 게 없으면 §2 자리표시자를 지우고 「없음」이라고 적어라 (판단을 남기는 것이다)."
fi

# ── SUMMARY 착지 (config `summary_dest` — 회고를 원장(para)에 축적) ────────────
# summary_dest 가 있으면 그 디렉토리가 **원본**이다(YYYY-MM-DD-<slug>.md).
# _archive 에는 포인터 한 줄만 남긴다 — 같은 사실을 두 곳에 두지 않는다.
# 없으면 종전대로 _archive 안에 원본이 남는다(분리형 프로젝트).
SUMMARY_DEST="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1])).get('summary_dest',''))" "$PROJECT_JSON")"
if [ -n "$SUMMARY_DEST" ] && [ -f "$SUMMARY" ]; then
  mkdir -p "$SUMMARY_DEST"
  SUMMARY_FINAL="$SUMMARY_DEST/$(date +%Y-%m-%d)-$SLUG.md"
  [ -f "$SUMMARY_FINAL" ] && die "회고가 이미 있다: $SUMMARY_FINAL — 덮어쓰지 않는다"
  mv "$SUMMARY" "$SUMMARY_FINAL"
  printf '원본: %s\n(작업 회고는 para 원장에 축적한다 — config summary_dest)\n' "$SUMMARY_FINAL" > "$SUMMARY"
  say "SUMMARY 착지: $SUMMARY_FINAL (원본. _archive 에는 포인터만)"
fi

# ── 파괴 단계 ─────────────────────────────────────────────────────────────────
for H in $TERMS; do orca terminal close --terminal "$H" >/dev/null 2>&1 && say "closed $H" || say "⚠ close 실패(이미 닫힘?): $H"; done

for T in "${TARGETS[@]:-}"; do
  [ -n "$T" ] || continue
  CANON=$(echo "$T" | cut -f1); WT=$(echo "$T" | cut -f2); BR=$(echo "$T" | cut -f3)
  git -C "$CANON" worktree remove --force "$WT" && say "removed $WT"
  if [ -n "$BR" ]; then
    git -C "$CANON" branch -D "$BR" >/dev/null 2>&1 && say "branch -D $BR" || true
    if [ $YES = 1 ]; then
      git -C "$CANON" push origin --delete "$BR" >/dev/null 2>&1 && say "원격 삭제 $BR" || say "⚠ 원격 삭제 실패/없음: $BR"
    fi
  fi
done

if [ -d "$WORK_DIR" ]; then
  mkdir -p "$(dirname "$ARCHIVE_DIR")"
  mv "$WORK_DIR" "$ARCHIVE_DIR"
  git -C "$HERE" add -A "work/"
  git -C "$HERE" commit -m "work: $SLUG 아카이브 → _archive/$PROJECT/ (archive-work.sh)" >/dev/null && say "아카이브 커밋 완료"
fi

echo "== 완료. 남은 확인: 남의 세션 터미널을 닫지 않았는지, prerebase-* 태그 잔존 여부(git tag -l 'prerebase-*')"
