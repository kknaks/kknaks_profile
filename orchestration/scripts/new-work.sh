#!/usr/bin/env bash
# new-work.sh — 오케스트레이션 작업 세팅 (프로젝트 무관, config 기반)
#
#   scripts/new-work.sh <project> <slug> [--workers be,fe,...] [--agent worker=agent ...]
#
# config/projects/<project>.json 하나만 읽는다. 값 하드코딩 없음.
# 새 프로젝트 = config/projects/<이름>.json 추가로 끝. 이 스크립트는 손대지 않는다.
#
# 하는 일 (idempotent):
#   1. config 로드 + 워커 선택 → 필요한 repo 만 추림
#   2. 각 repo canonical fetch (pull/checkout 안 함)
#   3. 워크트리 생성 (use_worktree=false 면 canonical 을 그대로 씀)
#   4. work/<slug>/ 에 워커별 브리프를 **config 값이 채워진 채로** 생성 + _RESUME.md
#   5. 워커별 `orca terminal create` 명령을 그대로 복사해 쓸 수 있게 출력
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_DIR="$HERE/config"
TEMPLATE="$HERE/templates/worker-brief.md"

die() { echo "ERROR: $*" >&2; exit 1; }
say() { echo "  $*"; }

PROJECT=""; SLUG=""; WORKERS_CSV=""; AGENT_OVERRIDES=""
while [ $# -gt 0 ]; do
  case "$1" in
    --workers) WORKERS_CSV="${2:-}"; shift ;;
    --agent)
      [ -n "${2:-}" ] || die "--agent 값이 필요하다 (예: --agent backend=codex)"
      AGENT_OVERRIDES="${AGENT_OVERRIDES}${AGENT_OVERRIDES:+,}$2"
      shift
      ;;
    -h|--help) sed -n '2,16p' "$0"; exit 0 ;;
    -*) die "unknown option: $1" ;;
    *) if [ -z "$PROJECT" ]; then PROJECT="$1"
       elif [ -z "$SLUG" ]; then SLUG="$1"
       else die "인자가 너무 많다: $1"; fi ;;
  esac
  shift
done

[ -n "$PROJECT" ] && [ -n "$SLUG" ] || {
  echo "사용법: $0 <project> <slug> [--workers a,b] [--agent worker=agent ...]"
  echo "사용 가능한 project:"; ls "$CONFIG_DIR/projects" | sed 's/\.json$/  /;s/^/  - /'
  exit 1
}

PROJECT_JSON="$CONFIG_DIR/projects/$PROJECT.json"
[ -f "$PROJECT_JSON" ] || die "설정 없음: $PROJECT_JSON (사용 가능: $(ls "$CONFIG_DIR/projects" | tr '\n' ' '))"
[ -f "$CONFIG_DIR/agents.json" ] || die "설정 없음: $CONFIG_DIR/agents.json"
[ -f "$TEMPLATE" ] || die "템플릿 없음: $TEMPLATE"
echo "$SLUG" | grep -Eq '^[a-z0-9][a-z0-9._-]*[a-z0-9]$' \
  || die "slug 는 kebab-case 소문자 (예: feat-medi-department-space). 받은 값: '$SLUG'"

command -v orca >/dev/null || die "orca CLI 없음"
orca status --json >/dev/null 2>&1 || die "orca 런타임이 ready 가 아니다"

COORD_HANDLE="${ORCA_TERMINAL_HANDLE:-}"
[ -n "$COORD_HANDLE" ] || say "⚠ \$ORCA_TERMINAL_HANDLE 없음 — 브리프의 코디handle 을 직접 채워야 한다"

# $ORCA_TERMINAL_HANDLE 은 세션이 재연결되면 stale 이 된다(2026-07-28 실제로 겪음 —
# 브리프에 죽은 핸들이 박혀 워커의 완료 보고 채널이 끊겼다). 살아 있는지만 확인한다.
#
# **자동 대체는 하지 않는다.** 한때 "cwd 로 시작하는 워크트리의 connected 터미널" 을 골랐는데,
# 이 스크립트는 orca_settings 리포에서 실행되므로 거기 붙은 **남의 세션**을 집어왔다(2026-07-29).
# 잘못 고르면 워커의 완료 보고가 엉뚱한 세션으로 가서 조용히 유실된다 — 추측이 안 하느니만 못하다.
# 스크립트는 호출한 세션의 터미널을 알 방법이 없으므로, stale 이면 멈추고 코디가 직접 채우게 한다.
if [ -n "$COORD_HANDLE" ]; then
  if ! orca terminal list --json 2>/dev/null | grep -q "$COORD_HANDLE"; then
    say "⚠ \$ORCA_TERMINAL_HANDLE ($COORD_HANDLE) 이 terminal list 에 없다 — stale"
    say "  → 브리프 §9 의 코디handle 을 **직접** 확인해 채워라. 자동 추측은 하지 않는다"
    say "  → 확인법: orca terminal list --json 에서 이 세션의 제목·워크트리와 맞는 handle 을 고른다"
    COORD_HANDLE="<코디handle — stale 이라 미치환. 직접 확인해 채울 것>"
  fi
fi

WORK_DIR="$HERE/work/$SLUG"
mkdir -p "$WORK_DIR"

# ── config 파싱 → 워커/repo 계획 (탭 구분 레코드로 셸에 넘김) ──────────────────
PLAN="$(PROJECT_JSON="$PROJECT_JSON" AGENTS_JSON="$CONFIG_DIR/agents.json" \
        WORKERS_CSV="$WORKERS_CSV" AGENT_OVERRIDES="$AGENT_OVERRIDES" SLUG="$SLUG" python3 - <<'PY'
import json, os, sys

cfg = json.load(open(os.environ['PROJECT_JSON']))
agents_cfg = json.load(open(os.environ['AGENTS_JSON']))
agents = agents_cfg['agents']
default_agent = agents_cfg.get('default')
slug = os.environ['SLUG']
sel = [w.strip() for w in os.environ['WORKERS_CSV'].split(',') if w.strip()]
if not sel:
    sel = cfg.get('default_workers') or list(cfg['workers'])

overrides = {}
for item in (x.strip() for x in os.environ['AGENT_OVERRIDES'].split(',') if x.strip()):
    if '=' not in item:
        sys.exit("잘못된 --agent 형식: %s (예: --agent backend=codex)" % item)
    worker, agent = (x.strip() for x in item.split('=', 1))
    if not worker or not agent:
        sys.exit("잘못된 --agent 형식: %s (worker와 agent가 모두 필요)" % item)
    overrides[worker] = agent

unknown = [w for w in sel if w not in cfg['workers']]
if unknown:
    sys.exit("알 수 없는 워커: %s (사용 가능: %s)" % (
        ', '.join(unknown), ', '.join(cfg['workers'])))

unknown_overrides = [w for w in overrides if w not in cfg['workers']]
if unknown_overrides:
    sys.exit("--agent의 알 수 없는 워커: %s (사용 가능: %s)" % (
        ', '.join(unknown_overrides), ', '.join(cfg['workers'])))
unselected_overrides = [w for w in overrides if w not in sel]
if unselected_overrides:
    sys.exit("--agent로 지정한 워커가 --workers 선택에 없다: %s" % ', '.join(unselected_overrides))

use_wt = cfg.get('use_worktree', True)
root = cfg.get('worktree_root', '')

# 선택된 워커가 쓰는 repo 만
repo_keys = []
for w in sel:
    rk = cfg['workers'][w]['repo']
    if rk not in repo_keys:
        repo_keys.append(rk)

out = []
for rk in repo_keys:
    r = cfg['repos'][rk]
    name = slug + (r.get('worktree_suffix') or '')
    path = r['canonical_path'] if not use_wt else '%s/%s/%s' % (root, r['orca_name'], name)
    out.append('\t'.join(['REPO', rk, r['orca_name'], r['canonical_path'],
                          r['base'], r.get('pr_base', ''), name, path,
                          '1' if use_wt else '0']))
for w in sel:
    wk = cfg['workers'][w]
    agent_name = overrides.get(w) or wk.get('agent') or default_agent
    if not agent_name:
        sys.exit("agent 선택값이 없다: worker=%s (worker.agent 또는 agents.json.default 필요)" % w)
    a = agents.get(agent_name)
    if a is None:
        sys.exit("agents.json 에 없는 agent: %s (worker=%s)" % (agent_name, w))
    if a.get('retired'):
        sys.exit("폐기된 agent 를 골랐다: %s (%s)" % (agent_name, a['retired']))
    out.append('\t'.join(['WORKER', w, wk['repo'], wk.get('brief_suffix') or w,
                          wk['roles_dir'], ','.join(wk.get('allowed_paths') or []),
                          agent_name, a['command'], (wk.get('verify') or '')]))
print('\n'.join(out))
PY
)" || die "config 파싱 실패"

echo "▶ 프로젝트 $PROJECT / 작업 $SLUG"
echo "$PLAN" | awk -F'\t' '$1=="WORKER"{printf "  워커 %-9s agent=%-7s repo=%-6s roles=%s\n", $2, $7, $3, $5}'

# ── 2·3. fetch + 워크트리 ────────────────────────────────────────────────────
declare -a REPO_LINES=()
while IFS= read -r line; do
  case "$line" in REPO*) REPO_LINES+=("$line") ;; esac
done <<< "$PLAN"

# macOS 기본 bash 3.2 는 연관배열(declare -A)이 없다 → 탭 레코드 + awk 조회로 대체.
# RESOLVED 각 줄: <repo_key>\t<path>\t<branch>\t<base>\t<pr_base>
RESOLVED=""
resolved_field() {  # resolved_field <repo_key> <field_no(2..5)>
  printf '%s\n' "$RESOLVED" | awk -F'\t' -v k="$1" -v n="$2" '$1==k{print $n; exit}'
}

for line in "${REPO_LINES[@]}"; do
  IFS=$'\t' read -r _ rk orca_name canonical base pr_base wt_name wt_path use_wt <<< "$line"
  git -C "$canonical" rev-parse --git-dir >/dev/null 2>&1 \
    || die "$rk canonical 이 git 저장소가 아니다: $canonical"

  echo "▶ [$rk] $orca_name — fetch (canonical 체크아웃은 건드리지 않는다)"
  git -C "$canonical" fetch origin --prune -q
  git -C "$canonical" rev-parse --verify -q "$base" >/dev/null || die "base ref 없음: $base ($rk)"
  say "base $base = $(git -C "$canonical" rev-parse --short "$base")"

  if [ "$use_wt" = "0" ]; then
    r_path="$canonical"
    r_branch="$(git -C "$canonical" rev-parse --abbrev-ref HEAD)"
    say "워크트리 미사용(use_worktree=false) → canonical 직접: $canonical"
  else
    repo_id="$(orca repo list --json | python3 -c "
import sys, json
for r in json.load(sys.stdin)['result']['repos']:
    if r.get('displayName') == sys.argv[1]:
        print(r['id']); break
" "$orca_name")"
    [ -n "$repo_id" ] || die "orca 에 repo '$orca_name' 미등록 — orca repo add --path $canonical --json"

    found="$(orca worktree list --json | python3 -c "
import sys, json
rid, name = sys.argv[1], sys.argv[2]
for w in json.load(sys.stdin)['result']['worktrees']:
    if w.get('repoId') == rid and w.get('displayName') == name and not w.get('isArchived'):
        br = w.get('branch') or ''
        print('%s\t%s' % (w.get('path'), br.removeprefix('refs/heads/')))
        break
" "$repo_id" "$wt_name")"

    if [ -n "$found" ]; then
      say "워크트리 재사용: $wt_name"
    else
      say "워크트리 생성: $wt_name (base $base)"
      found="$(orca worktree create --repo "name:$orca_name" --name "$wt_name" \
        --base-branch "$base" --no-parent --json | python3 -c "
import sys, json
d = json.load(sys.stdin)
if not d.get('ok', True):
    sys.exit('orca worktree create 실패: %s' % json.dumps(d)[:800])
w = d['result']['worktree']
br = (w.get('branch') or '')
print('%s\t%s' % (w['path'], br.removeprefix('refs/heads/')))
")"
    fi
    IFS=$'\t' read -r r_path r_branch <<< "$found"
    [ -n "$r_path" ] || die "$rk 워크트리 확보 실패"
    say "$r_path  [$r_branch]"
  fi
  RESOLVED="$RESOLVED$rk	$r_path	$r_branch	$base	$pr_base
"
done

# ── 4. 브리프 생성 (config 값이 채워진 채로) ─────────────────────────────────
echo "▶ work/$SLUG"
BRIEFS=""; TERMCMDS=""
while IFS= read -r line; do
  case "$line" in WORKER*) ;; *) continue ;; esac
  IFS=$'\t' read -r _ wname rk suffix roles_dir allowed_csv agent_name agent_cmd verify <<< "$line"
  wt_path="$(resolved_field "$rk" 2)"
  wt_base="$(resolved_field "$rk" 4)"
  wt_prbase="$(resolved_field "$rk" 5)"
  dst="$WORK_DIR/$SLUG-$suffix-brief.md"
  BRIEFS="$BRIEFS $SLUG-$suffix-brief.md"
  TERMCMDS="$TERMCMDS
# [$wname / $agent_name]
orca terminal create --worktree path:$wt_path --command \"$agent_cmd\" --json"

  if [ -f "$dst" ]; then
    say "브리프 이미 있음 — 유지: $(basename "$dst")"
    continue
  fi
  ALLOWED_MD="$(printf '%s' "$allowed_csv" | tr ',' '\n' | sed '/^$/d;s|^|- `|;s|$|`|')"
  [ -n "$ALLOWED_MD" ] || ALLOWED_MD="- (제한 없음 — 코디네이터가 채울 것)"
  ROLE_ABS="$HERE/$roles_dir"

  # 템플릿의 안내 블록(--- 구분선까지) 제거 후 config 값 치환
  awk 'f{print} /^---$/{f=1}' "$TEMPLATE" \
  | WNAME="$wname" ROLE_ABS="$ROLE_ABS" WT="$wt_path" BASE="$wt_base" \
    PRBASE="$wt_prbase" ALLOWED="$ALLOWED_MD" VERIFY="$verify" \
    COORD="${COORD_HANDLE:-<코디handle>}" SLUG="$SLUG" PROJECT="$PROJECT" python3 -c "
import os, sys
t = sys.stdin.read()
e = os.environ
for k, v in {
    '<WORKER>': e['WNAME'], '<ROLE_DIR>': e['ROLE_ABS'], '<WORKTREE>': e['WT'],
    '<BASE>': e['BASE'], '<PR_BASE>': e['PRBASE'], '<ALLOWED_PATHS>': e['ALLOWED'],
    '<VERIFY>': e['VERIFY'] or '<검증 명령 — 코디네이터가 채움>',
    '<코디handle>': e['COORD'], '<SLUG>': e['SLUG'], '<PROJECT>': e['PROJECT'],
}.items():
    t = t.replace(k, v)
sys.stdout.write(t)
" > "$dst"
  say "브리프 생성: $(basename "$dst")  (역할·allowed_paths·워크트리·검증 채워짐)"
done <<< "$PLAN"

# ── _RESUME.md (templates/resume.md 렌더) ────────────────────────────────────
# 종전에는 이 스켈레톤을 스크립트 안 heredoc 으로 찍었다. 그러면 양식을 고칠 때
# 스크립트를 고쳐야 해서 「양식은 templates/ 에 둔다」는 규칙이 _RESUME 에만 안 지켜졌다.
# worker-brief 와 같은 방식(안내 블록 절단 + <TOKEN> 치환)으로 통일한다.
RESUME="$WORK_DIR/_RESUME.md"
RESUME_TEMPLATE="$HERE/templates/resume.md"
[ -f "$RESUME_TEMPLATE" ] || die "템플릿 없음: $RESUME_TEMPLATE"
if [ ! -f "$RESUME" ]; then
  WORKTREES_MD="$(printf '%s\n' "$RESOLVED" \
    | awk -F'\t' 'NF>=5{printf "- `%s`: `%s` (branch `%s`, base `%s` → PR `%s`)\n", $1, $2, $3, $4, $5}')"
  awk 'f{print} /^---$/{f=1}' "$RESUME_TEMPLATE" \
  | SLUG="$SLUG" PROJECT="$PROJECT" WORKTREES="$WORKTREES_MD" \
    COORD="${COORD_HANDLE:-<코디handle>}" BRIEFS="$BRIEFS" python3 -c "
import os, sys
t = sys.stdin.read()
e = os.environ
for k, v in {
    '<SLUG>': e['SLUG'], '<PROJECT>': e['PROJECT'],
    '<WORKTREES>': e['WORKTREES'], '<코디handle>': e['COORD'],
}.items():
    t = t.replace(k, v)
sys.stdout.write(t)
" > "$RESUME"
  say "_RESUME.md 생성 (templates/resume.md — 브리프 채울 것:$BRIEFS)"
else
  say "_RESUME.md 이미 있음 — 유지"
fi

# ── 5. 출력 ──────────────────────────────────────────────────────────────────
echo
echo "▶ 코디handle: ${COORD_HANDLE:-<미확인>}"
echo "▶ 브리프 채운 뒤 아래 명령으로 워커를 띄운다:"
echo "$TERMCMDS"
echo
echo "▶ 발주:"
echo "  orca orchestration task-create --spec \"\$(cat $WORK_DIR/<브리프>)\" --json"
echo "  orca orchestration dispatch --task <task_id> --to <handle> --inject --json"
echo
WORK_DIR="$WORK_DIR" PROJECT="$PROJECT" SLUG="$SLUG" python3 -c "
import json, os
e = os.environ
print('SETUP_SUMMARY_JSON ' + json.dumps(
    {'project': e['PROJECT'], 'slug': e['SLUG'], 'work_dir': e['WORK_DIR']},
    ensure_ascii=False))
"
