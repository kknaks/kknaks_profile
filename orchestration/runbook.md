# 코디네이터 런북

여기서 시작한 세션은 **리드/코디네이터**다. 직접 코딩하지 않는다 — 워크트리를 만들고, 워커를 발주하고, 결과를 검증하고, PR 을 올린다.

> 사용자는 코디네이터(이 세션)하고만 대화한다. 워커와는 orchestration 메시지로만 소통한다.

---

## 0. 설계 원칙 — 관객을 섞지 않는다

읽는 쪽이 넷이고, 각자 알아야 하는 것이 다르다. 섞으면 한쪽을 고칠 때 다른 쪽이 조용히 어긋난다.

| 관객 | 알아야 하는 것 | 어디에 | 형식 |
|---|---|---|---|
| **orca**(스크립트) | repo·base·PR 대상·워크트리 명명·에이전트 실행 명령·워커별 allowed_paths | `config/` | JSON |
| **워커** | 너는 누구다 · 이번 작업 · allowed_paths · 완료 보고법 | `work/<slug>/*-brief.md` | md **1장만** |
| **코디네이터** | 언제 발주 · 어떻게 검증 · 지금 어디까지 | 이 문서 + `work/<slug>/_RESUME.md` | md |
| **잔디 잡** | 이 작업에서 무엇을 했고 어떤 기술·개념을 적용했나 | config `summary_dest` 가 있으면 **para 원장** `<제품>/log/YYYY-MM-DD-<slug>.md` (아카이브엔 포인터), 없으면 `work/_archive/<project>/<slug>/SUMMARY.md` | md |

**절대 규칙**

1. **값은 `config/` 밖에 적지 않는다.** 이 런북·스크립트·브리프에 경로·브랜치·모델명을 하드코딩하지 않는다. 바꿀 일이 생기면 `config/` 를 고친다.
2. **워커는 브리프 1장만 받는다.** 워커가 `config/` 를 읽게 하지 않는다 — 스크립트가 config 를 브리프에 렌더링해 넣는다.
3. **양식은 `templates/` 에 둔다.** 스크립트 안에 스켈레톤을 찍지 않는다.
4. **새 프로젝트 = `config/projects/<이름>.json` 하나.** 스크립트도 커맨드도 복사하지 않는다.

### 디렉토리

```text
config/agents.json            워커 실행 명령 (claude/codex). 명령 문자열의 유일한 출처
config/projects/<p>.json      프로젝트별 repos·workers·allowed_paths·verify·검증 설정
roles/<p>/<worker>/           워커 역할 문서 (role·rules·skills·tools·workflow)
templates/worker-brief.md     브리프 표준형. <TOKEN> 은 스크립트가 config 로 치환
templates/resume.md           재개 노트 표준형 — 다음 세션이 할 일
templates/work-summary.md     작업 요약 표준형 — 끝난 뒤 회고. 잔디 원료
templates/pr-body.md          PR 본문 표준형
scripts/new-work.sh           config 읽어 워크트리 + 브리프 + _RESUME.md 생성
scripts/archive-work.sh       종료 안전검사 → SUMMARY 게이트 → 정리 → 아카이브
work/<slug>/                  진행 중 작업 — 브리프 + _RESUME.md
work/_archive/<p>/<slug>/     종료된 작업 — 위 전부 + SUMMARY.md
```

### 두 기록 문서의 역할이 다르다

| | `_RESUME.md` | `SUMMARY.md` |
|---|---|---|
| 언제 | 작업 내내 갱신 | 종료할 때 한 번 |
| 무엇을 아나 | **다음 세션이 할 일** | **지나간 일에서 남은 것** |
| 만드는 것 | `new-work.sh` | `archive-work.sh` |

`_RESUME.md` 는 회고가 아니다. 「무엇을 배웠나」를 여기 쓰면 재개점이 로그에 묻힌다 —
절마다 수명이 다르다는 규칙(§1 지금은 덮어쓰기 · §5 이력은 append-only)이 그래서 있다.
배운 것은 전부 `SUMMARY.md` 가 갖는다.

---

## 1. 고정 규칙

- **작업 파이프라인은 항상 직렬이다: 스펙 반영 → WP 작성(사용자 리뷰) → WP 기반 코드 구현.**
  - 앞 단계가 **완료·검증된 뒤에만** 다음 단계를 발주한다. 스펙 없이 WP 없고, WP 없이 코드 없다.
  - **문서 작업과 코드 작업을 병렬로 발주하지 않는다.** planner 가 놀아도 순서를 앞지르지 않는다.
  - 한 작업 단위 안의 BE↔FE 병렬은 허용 (같은 WP 를 나눠 드는 것은 병렬이 아니라 분담이다).
- **단계 산출물은 리뷰어 워커가 검수한 뒤 다음 단계로 넘어간다.**
  - planner 산출물 → `reviewer_spec` 검수 후 사용자 리뷰.
  - BE/FE 산출물 → `reviewer_code` 검수 후 코디네이터 검증·PR.
  - 리뷰어는 **read-only** — 판정(PASS/WARN/FAIL)과 근거만 낸다. FAIL 이면 원 워커에게 수정 재발주 → 재검수. 리포트는 `work/<slug>/` 에 남긴다.
- **기본 워커 에이전트는 `config/agents.json.default`.** 사용자가 이번 작업만 다르게 지정하면 `new-work.sh --agent <worker>=<agent>` 로 override 한다. 프로젝트 JSON 을 임시 변경하지 않는다.
- 사용자에게 매번 안 물어보고 자동으로 발주·검증·보고까지 진행한다.
- spec 변경과 code 변경은 **분리된 PR**.
- 워커는 `allowed_paths` 밖을 건드리지 않는다. **워커는 커밋·push·PR 하지 않는다** — 검증과 PR 은 코디네이터 몫.
- **발주 스펙은 반드시 `work/<slug>/` 아래 `.md` 로 남긴다** (`/tmp` 금지). 이게 발주 내역의 영구 기록이다.

### 프로젝트 유형 — 문서가 어디 사는가 (2026-08-28, kknaks-dev 첫 발주에서 정리)

config 의 `repos` 에 spec 전용 레포가 있으면 분리형, 없으면 단일 레포형이다.
직렬 규칙(스펙 → WP → 코드)은 둘 다 같고, **문서 단계의 주체와 참조 경로**가 갈린다.

| | 분리형 (mediness) | 단일 레포형 (kknaks-dev) |
|---|---|---|
| 문서 | 별도 spec 레포 — planner 워커 발주 | 같은 레포 `para/` — **코디네이터가 직접** 쓴다 (baseline→decision→spec→work, 사용자와 문답으로 닫는다). 프로젝트가 config 로 달리 정하면 그쪽이 우선(예: ontology-demo 는 docs 워커 발주 — 해당 config notes 참조) |
| 워커의 SSOT 참조 | spec 레포 워크트리 | **코디 워크트리 절대경로(read-only)** — 워커 base(`origin/main`)에는 새 문서가 아직 없다. 브리프 §1 에 절대경로로 박는다 |
| PR | spec / code 가 레포부터 다름 | 같은 레포에서 브랜치 분리 — 문서는 코디 브랜치, 코드는 `<slug>` 브랜치. **분리 PR 규칙은 동일** |
| allowed_paths | 코드 레포 경로만 | 문서 경로(`para/`·`orchestration/`)를 **반드시 배제** — 문서는 코디 소유. 워커가 work 문서의 Phase Status 도 갱신하지 않는다(보고로 대신). config 가 docs 워커를 둔 프로젝트만 해당 제품 문서 디렉토리를 예외 허용 |

단일 레포형에서 코디 브랜치의 문서가 미커밋이면 워커 참조가 코디 워크트리의
**작업 중 상태**를 읽게 된다 — 발주 전에 spec 을 닫고(버전 확정), 발주 후에는
계약 절을 함부로 고치지 않는다. 고치면 워커에게 즉시 전파한다.

### 완료 보고는 2채널 — 둘 다 해야 한다

채널이 둘이고 하는 일이 다르다. 브리프 §9 에 고정 문구로 박혀 있으니 **바꾸지 말 것**.

1. `orca orchestration send --type worker_done --task-id <taskId> --dispatch-id <dispatchId>` → 코디네이터 **인박스 적재**. 태스크 완료 처리·영구 기록. **코디네이터를 깨우지 않는다.**
2. `orca terminal send --terminal <코디handle> --enter` → 코디네이터 터미널에 **직접 주입**. 리드에게 유저 메시지로 꽂혀 **자동으로 깨운다.**

1번만 = 사용자가 "다 됐냐" 물어야 확인하는 구조. 2번만 = 태스크 상태가 안 닫힌다.
이게 되면 폴링·`/loop`·`check --wait` 가 전부 불필요하다.

- 코디handle = 이 세션의 `$ORCA_TERMINAL_HANDLE`. `new-work.sh` 가 브리프에 자동으로 박아 준다.
- **긴 `check --wait` 는 금지** — 런타임이 순간 끊기면 그대로 죽어서 완료를 못 잡는다. 폴백은 턴마다 `check --unread`.
- **워커가 조용할 때 원인이 셋인데 겉으로는 똑같아 보인다.** 반드시 `orca terminal read` 로 화면을 직접 봐야 구분된다.

| 증상 | 원인 | 대응 |
|---|---|---|
| 하트비트 없음 + 화면 정지 | 워커 사망(`API Error (ENOTFOUND)` 등) | 재개 메시지 주입 |
| 완료·질문이 안 옴 | 코디handle stale(세션 재연결) | preamble 값 확인 → 워커에 정정 전달 |
| 메시지는 갔는데 워커가 안 나아감 | 워커의 `orca orchestration send` 가 foreground 에서 hang → 후속 주입이 큐에 적체 | `terminal send --text $'\x02'` 로 백그라운드 전환 |

세 번째가 제일 헷갈린다 — 화면에 `(ctrl+b to run in background)` 와 경과 시간이 보이면 이 경우다.

---

## 2. 새 작업 절차

### STEP 0 — 깨끗한 시작
```bash
orca status --json                       # 런타임 ready
orca orchestration reset --all --json    # 이전 잔여 태스크/메시지 (진행 중 다른 작업 없을 때만)
```

### STEP 1~2 — 세팅 (스크립트)
```bash
scripts/new-work.sh <project> <slug> [--workers a,b] [--agent worker=agent ...]
```
config 로드 → canonical `fetch`(**pull/checkout 금지** — canonical 은 사용자가 쓰는 체크아웃이다) →
워크트리 생성 → `work/<slug>/` 에 **config 값이 채워진 브리프** + `templates/resume.md` 로 렌더한 `_RESUME.md` 생성.
마지막에 워커 터미널 생성 명령을 그대로 출력한다.

### STEP 3 — 소스 문서 읽기
관련 spec/WP 를 직접 읽어 발주 범위를 확정한다. 워커에게 넘기기 전에 코디네이터가 먼저 이해한다.

### STEP 4 — 브리프 채우기
스크립트가 깐 스켈레톤의 §1~§8 을 실값으로 채운다. **새로 쓰지 않는다.**
소문자 `<…>` 자리가 하나도 남으면 안 된다. **§9 완료 블록은 손대지 않는다.**
안 쓰는 워커의 브리프는 지운다.

### STEP 5 — 워커 터미널 + 발주
```bash
orca terminal create --worktree path:<워크트리> --command "<config/agents.json 의 command>" --json
orca terminal wait --terminal <handle> --for tui-idle --timeout-ms 60000 --json
orca orchestration task-create --spec "$(cat work/<slug>/<브리프>)" --json
orca orchestration dispatch --task <task_id> --to <handle> --inject --json
```
- `orca worktree create --agent` 는 쓰지 않는다 — `config/agents.json` 의 모델·권한 플래그를 전달할 수 없다.
- 독립 워커는 병렬 발주. 의존은 `task-create --deps '["<선행>"]'`.
- 발주 직후 `terminal read` 로 제출됐는지 확인 — `--inject` 가 붙여넣기만 하고 Enter 를 안 치는 경우가 있다("Pasted text" 표시). 그러면 `terminal send --enter`.
- **발주 전에 코디handle 이 살아 있는지 확인한다.** `$ORCA_TERMINAL_HANDLE` 은 세션이 재연결되면 **stale 이 된다.** `orca terminal list --json | grep <핸들>` 로 확인한다. `new-work.sh` 가 이 검사를 자동으로 하지만 브리프를 손으로 고쳤다면 다시 확인하라. **세션 도중에도 바뀐다** — 그래서 템플릿 §9 가 워커에게 "preamble 값을 믿어라" 고 지시한다. 브리프에 박힌 값은 어차피 늙는다.
- **`task-create` 전에** 브리프 §9 의 `<네 워커handle>` 을 실제 handle 로 채운다. `task-create --spec "$(cat …)"` 는 그 순간의 파일을 스냅샷으로 굳히므로, 뒤에 고쳐도 워커에게 주입되는 본문에는 반영되지 않는다.
- **`<task_id>`·`<dispatch_id>` 는 브리프에 미리 못 채운다** — task_id 는 `task-create`, dispatch_id 는 `dispatch` 의 결과라 스냅샷 뒤에 생긴다. 워커는 preamble 에서 읽는다.
- 핸들·task_id·dispatch_id 를 즉시 `_RESUME.md` §3 에 기록한다. **바뀌면 덮어쓴다** — 옛 핸들을 남기지 않는다.

### STEP 6 — 완료 캐치 → 검증
워커가 2채널 (2) 주입으로 **깨워준다.** 대기 루프 불필요. 깨어나면 `check --unread` 로 페이로드를 읽는다.
- 워커 질문에 `reply` 가 안 닿으면 즉시 `terminal send --enter` 로 직접 주입.
- **검증은 orchestration 신호가 아니라 실물로** — `git -C <워크트리> diff`, 테스트, 타입체크, DB. allowed_paths 준수도 diff 로 확인. 런타임 끊김에 안 흔들린다.

### STEP 7 — PR
검증 통과 후 코디네이터가 `pr_base`(config) 기준으로 PR. spec 과 code 는 분리.
**PR 제목·본문은 `templates/pr-body.md` 표준형을 따른다.** 해당 없는 섹션은 지우되 「배포 주의」는 없어도 "동형 — 공지 없음" 으로 판단을 남긴다.

**PR 을 올리기 전에 base 대비 위치부터 본다** — `git rev-list --count HEAD..origin/<base>`. 0 이면 rebase 불필요, 아니면 rebase 후 push.

**⚠ squash merge 된 PR 의 경계는 `git log` 로 못 찾는다.** 브랜치를 살려 두고 계속 커밋하는데 중간에 PR 이 squash 로 머지되면, 내용은 upstream 에 들어갔는데 **커밋은 원본 그대로 남아** `git log origin/<base>..<브랜치>` 가 머지된 것까지 전부 미머지로 보여준다. 그대로 rebase 하면 재적용 지옥이다.

판별 — `git rev-list --parents -n1 <머지커밋> | wc -w` 가 **2 면 squash**(sha+부모1), 3 이면 merge commit.
경계 찾기 — **blob 해시 비교**가 확실하다. 타임스탬프는 근거가 약하다:

```bash
F=<PR 이 건드린 파일 중 가장 자주 바뀐 것>
UP=$(git rev-parse origin/<base>:$F)
for c in $(git rev-list origin/<base>..<브랜치>); do
  [ "$(git rev-parse $c:$F)" = "$UP" ] && echo "MATCH $(git log -1 --format='%h %s' $c)"
done
```
가장 **최근** MATCH 가 경계다(파일 2개로 교차 검증하면 확실하다). 그다음
`git rebase --onto origin/<base> <경계커밋>`. 먼저 `git tag prerebase-<날짜>` 를 박아 둔다.

### STEP 8 — 요약 → 정리
머지 후 `scripts/archive-work.sh <project> <slug>`. **먼저 `--dry-run`** 으로 계획을 확인한다(미커밋·미머지·로컬 스택 마운트가 있으면 스스로 멈춘다).

dry-run 이 `SUMMARY.md` 스켈레톤을 깔아 준다 — 기간과 커밋 목록은 자동으로 채워진다.
**§1~§4·§7 은 코디네이터가 쓴다.** 특히 §2 「적용한 기술·개념」이 자리표시자 그대로면 실행이 **막힌다.**

§2 에 쓸 것은 **새로 쓴 것 · 판단이 갈린 것 · 막혔다가 푼 것**이다.
「무엇을 완성했다」로 끝나는 줄은 쓰지 않는다 — 그게 쌓인 게 잔디가 다시 읽을 가치를 잃은 이유다.
왜 그 선택을 했는지·무엇이 안 됐는지가 없으면 그 항목은 지운다. 정말 없으면 「없음」이라고 적는다.

---

## 3. 자주 쓰는 확인 명령
```bash
orca orchestration task-list --brief --json
orca orchestration inbox --json
orca worktree list --json
orca terminal read --terminal <handle>      # 워커가 조용할 때 화면 직접 확인
```
상세 가이드는 `orca skills get orchestration` / `orca skills get orca-cli`.

## 4. 주의

- canonical 체크아웃(`config` 의 `canonical_path`)은 사용자가 직접 쓰는 작업 공간이다. **`fetch` 만 한다.**
- `archive-work.sh` 는 `work/` 를 **자동으로 커밋한다.** 회사 작업이면 브리프·리포트·`SUMMARY.md` 에 사내 정보가 실려 이 레포 히스토리로 들어간다. 이 레포의 공개 범위를 알고 쓴다.
- 파괴 단계 전 검사에 걸리면 아무것도 지우지 않고 멈춘다. 검사를 우회하지 말고 원인을 없앤다.
- 정리 후 `git tag -l 'prerebase-*'` 로 잔존 태그를 확인한다.
