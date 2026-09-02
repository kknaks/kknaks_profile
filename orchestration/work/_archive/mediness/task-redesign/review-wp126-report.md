# 리뷰 리포트 — WP-126(incident 재정비) / planner 모드 (2026-08-31)

## 판정: WARN

FAIL 사유 없음 — lint ERROR 0, allowed_paths 이탈 0, 30-work.md 3표·log.md 동기 있음, 상대링크 전부 실재, SPEC-152 계약과 WP 본문이 축·용어 단위로 일치한다. 다만 **코드 실측이 따라오지 않은 자리 2건**(W1·W2)과 **로그 행이 같은 워크트리의 정정과 어긋나는 자리 1건**(W3)이 있어 PR 전 손봐야 한다. W1 은 P2 의 전제(«run 감사 신설» · «migration 0»)를 흔드는 축이라 WARN 중 가장 무겁다.

## 검수 범위

- 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec` (HEAD `84c824f86`, 미커밋 변경분이 검수 대상)
- diff: tracked 4파일(`spec-152` 1줄 · `30-work.md` +4/-2 · `work-125` 2줄 · `log.md` +2/-1) + untracked 1파일(`30-work/work-126-incident-workflow-realign.md`, 300줄)
- 브리프 §5 allowed_paths(`products/mediness/`·`context/`) **이탈 0** — 5파일 전부 `products/mediness/` 안
- 실행한 검사:
  - `python3 scripts/lint-pipeline.py --strict` (repo root)
  - `git diff -U0` / `git status --porcelain`
  - doc_no·WP 번호 전역 스캔(현행 + `90-archive/`)
  - 상대링크 9건 존재 확인 스크립트
  - **코드 레포 read-only 대조** — `~/orca/workspaces/mediness-app/task-redesign`(HEAD `9585efbc`) + 타 워크트리 3곳 교차 확인
  - SPEC-152 §heading 전수 + 인용 절 본문 대조(§라운드 판정 정본 :1507 · §run 감사 :1545 · §종결 시 태스크 정리 :1556 · §U-2 :202 · §케이스 매트릭스 :1722 · §담당자 축과 참조자 :1428 · §TK-1 :1437 · OQ-1/2/13/14/15/16 :2053~)

## 위반 (FAIL 사유)

없음.

## 경미 (WARN)

### W1. run 감사 「신설」 전제가 실측과 어긋난다 — 원장은 이미 있고, 그 원장은 payload 를 의도적으로 두지 않는다 ⚠ 가장 무거움

- `products/mediness/30-work/work-126-incident-workflow-realign.md:170` — 「`engine/runtime.py::set_run_status` 에 **run 감사 이벤트** 신설」
- 같은 파일 `:177` · `:86`(Code Surface note) · `:284`(OI-5 「저장 자리는 P2 의 설계 판단 … 어느 테이블에 쓰는가는 정하지 않았다」)

실측(코드 레포 HEAD, 이 파일은 미커밋 변경 대상 아님):

- `back/app/services/action_runtime/engine/runtime.py:363-411` — `set_run_status` 가 **이미** `WorkflowRunEvent` 행을 쓴다(`from_status`·`to_status`·`stage`·`cause`·`actor_id`·`actor_member_id`·`actor_kind`·`actor_label`·`action_id`). docstring: 「run 상태의 **유일한** 쓰기 경로이자 **전이 원장의 유일한 쓰기 지점**(SPEC-150 §5.2a ② · WP-118 P0)」.
- `back/app/models/action_runtime.py:435` `class WorkflowRunEvent` / `__tablename__ = "workflow_run_events"` — 클래스 docstring에 **「`payload` 가 없다. 사유는 `cause` 라는 유한 어휘로 적지 자유 본문으로 적지 않는다」** 가 명시돼 있다.
- `back/app/models/action_runtime.py:245-250` `RUN_TRANSITION_CAUSES` = 4종 닫힌 어휘. `runtime.py:392` 이 어휘 밖 값을 `InvalidActionState` 로 **세운다**(「«기타» 는 없습니다」).

⇒ 세 갈래로 어긋난다.

1. **「신설」이 아니다.** P2 의 실제 델타는 훨씬 좁다 — 종결 사유를 어떤 `cause` 로 표현할지 + 추적 Task 정리 배선. OI-5 의 「저장 자리 미정」은 실측 한 번으로 닫히는 질문이었다(브리프 §1 「조사는 지도, 코드가 정본」 · WP 자기 §메타 :32 도 같은 규율을 선언한다).
2. **payload 축이 정면 충돌한다.** WP `:170`·`:177` 이 「정리한 Task id 목록을 감사 이벤트 payload 에 싣는다」를 두 번 요구하는데, 현행 원장은 **payload 컬럼을 의도적으로 두지 않는 것이 계약**이다. 같은 요구가 `products/mediness/20-spec/spec-152-incident-response-workflow.md:1545~`(§run 감사 「남기는 것 … 종결 시 정리한 Task id 목록」)에도 있으므로 이건 **WP 의 발명이 아니라 SPEC ↔ 현행 코드 계약의 모순**이다. 브리프 §7 은 이런 모순을 「질문 채널로 보고」하라 했고 planner 는 OI-1·OI-9 는 그렇게 처리했는데 이 건은 잡지 못했다.
3. **`migration 0` 전제가 흔들린다.** frontmatter/Board/log 가 모두 「migration 0」을 표제 사실로 싣는데(`30-work.md:112` · `log.md:18` · `work-126:98`), Task id 목록을 원장에 실으려면 컬럼 추가 = migration 1건이거나, 「id 목록은 원장에 싣지 않는다」로 SPEC 을 되돌려야 한다.

- **권장 수정**: P2 작업 문구를 「신설」→「기존 `workflow_run_events`(WP-118) 위에서 종결 `cause` 어휘 확정 + 정리 배선」으로 고치고, OI-5 를 「저장 자리 미정」이 아니라 **「정리한 Task id 목록을 payload 없는 원장에 어떻게 남길 것인가 — SPEC-152 §run 감사 환류 필요」** 로 다시 세운다. `migration 0` 표제는 그 결론이 나올 때까지 조건부로 표기.

### W2. 죽은 코드 목록이 재실측되지 않았다 — 살아 있는 상수 1건 · 사라진 pyc 4건

- `work-126:76`·`:245` — 참조 0 상수 목록에 `STATUS_FAILED` 포함
  - 실측: `back/app/services/action_runtime/workflow/incident/const.py:42` `STATUS_FAILED = "failed"` 는 **살아 있다** — `workflow/incident/surface.py:70` `_TERMINAL_RUN_STATUSES = (C.STATUS_DONE, C.STATUS_REJECTED, C.STATUS_FAILED)` 이고 그 튜플은 `surface.py:56` dedupe 판정에 쓰인다. 삭제하면 회귀.
  - 같은 목록의 나머지는 확인됨(참조 = 정의 1줄뿐): `EV/ERR_ASSIGNEE_RESOLUTION_FAILED`(const.py:63·96) · `ERR_ACTION_STALE_PLAN_VERSION`(const.py:92) · `META_DECLARE_SUBJECT_ID`(const.py:122).
- `work-126:84`·`:247` — 고아 `.pyc` 4건(`ai_review`·`reviewed_gate`·`slack_channel`·`task_round`)
  - 실측: `find back -name "*.pyc"` 에서 그 4건 **0건**. 현행 `actions/__pycache__/` 는 `__init__`·`card`·`commands`·`execution`·`regen_gate` 5건뿐이고 전부 소스가 있다. 조사 스냅샷 이후 캐시가 재생성된 것으로 보인다.
- 근거 규칙: 브리프 §1 「조사는 계약이 아니라 지도 — 어긋나면 코드 실물이 맞다」 / `@mediness-planner` 규율(발주 문서는 dev 가 그대로 실행하는 목록).
- 완화: P6 에 「삭제 전 grep 으로 참조 0 을 각각 확인」(`work-126:245`)이 이미 박혀 있어 dev 단계에서 걸린다. 그래서 FAIL 이 아니라 WARN.
- **권장 수정**: `STATUS_FAILED` 를 목록에서 빼고(또는 「surface.py:70 소비 있음 — 존치」로 표기), 고아 pyc 항목은 「P0 재실측 후 대상 있으면」 조건부로 낮춘다.

### W3. log.md 새 행이 같은 워크트리의 정정과 어긋난다 — 영향 ID·종류 누락

- `products/mediness/log.md:18` 요약 말미: 「… 이 라운드는 **WP 문서에 기록만 하고 SPEC 본문은 고치지 않았다**(계약 수정은 문서 소관자 판단)」
  - 그런데 같은 미커밋 diff 가 `products/mediness/20-spec/spec-152-incident-response-workflow.md:1930` 을 **실제로 개정**했고(「DB 에 아직 남아 있다」 → 「`0066` 로 이미 drop 됐다」), `products/mediness/30-work/work-125-task-ledger-unification.md:62`·`:319` 도 함께 고쳤다. 로그 행이 워크트리와 반대를 말한다.
- 같은 행 `영향 ID` = `MEDINESS-WP-126, MEDINESS-SPEC-152` — **`MEDINESS-WP-125` 누락**. `종류` = `wp-add` 단독 — `spec-change`·`wp-change` 누락.
- 근거: `rules/document-pipeline.md` §`log.md` — 「한 PR에서 SPEC과 WP를 함께 바꾸면 `영향 ID` 컬럼에 관련 SPEC/WP/DEC/OPEN ID를 모두 넣습니다」 / 「복합 변경 시 `종류` 콤마 결합」.
- 정황: 이 정정 3곳은 **코디네이터가 planner 산출 뒤에 넣은 것**이라 planner 가 쓴 시점엔 참이었다. 그래도 PR 로 나가면 장부가 틀린 사실을 남긴다.
- **권장 수정**: `종류` → `wp-add, spec-change, wp-change`, `영향 ID` 에 `MEDINESS-WP-125` 추가, 말미 문장을 「정정을 SPEC-152 §Functional Rule·WP-125 §Scope/OI-4 에 함께 반영했다」로 교체.

### W4. Code Surface 좌표 드리프트 (경미 — 표 성격이 「경로 후보」라 실질 영향 낮음)

`work-126:64-84` 표의 줄번호가 코드 레포 HEAD(`9585efbc`)와 어긋난다.

| WP 기재 | 실측(HEAD) |
|---|---|
| `tasks_surface.round_complete()` :340 | `:321` (`async def round_complete`) |
| `engine/runtime.py::set_run_status()` :220 | `:363` (구현). `:289` 는 Protocol stub(`...`) — 「유일 쓰기 경로」 주장 자체는 참 |
| `regen_gate.on_event` :88~ | `:80` |
| `action_runtime_v2.py` `POST /incidents/slack/complete` :797 | HEAD `:830`. ⚠ **app 워크트리 `task-redesign` 의 미커밋 작업본에는 이미 제거돼 있다**(WP-125 BE 진행 중, 31파일 미커밋). 타 워크트리(`mcp-library-publish`·`meeting-minutes-ledger-fix` :830 / `user-dashboard` :714)에는 존재 |
| `factory.has_open_in_run_chain()` :180 | `:180` ✔ 정확 |
| `definitions.py` Slack 3단 :164~ | 조사 §B-172 와 동일 좌표 — 별도 반증 없음 |

- **권장 수정**: 표 머리에 「좌표는 스냅샷 — P0 에서 재확인」 한 줄을 넣거나 줄번호를 떼고 심볼명만 남긴다.

## 기존 부채 (이번 판정 제외)

- `products/mediness/30-work.md:234` — `MEDINESS-SPEC-030` Spec Coverage 구현 상태 `in_dev` ≠ derive 값 `done` (lint WARN). **이번 diff 밖**(SPEC-030 행은 손대지 않음).
- 타 제품 WARN 다수(charty·selly 등 `doc_no` 누락, `Touching Domains` 형식) — mediness 무관. 전체 `0 error, 255 warning`.
- 코드 레포: `back/alembic/versions/0066_task_scope_slug_dates.py` 의 파일명은 `0066_*` 인데 내부 `revision: str = "0061_task_scope_slug_dates"`(down_revision `0060_*`). 문서 3곳이 「`0066_task_scope_slug_dates`」로 인용하는데 **파일명 기준으론 맞고 revision id 기준으론 다르다.** app 레포 부채이며 이번 판정 대상 아님 — 다만 P0 실측 때 혼선 가능.
- 코드 레포: `back/app/routers/action_runtime_common.py:42` 이 이미 사라진 `POST /incidents/slack/complete` 를 docstring 으로 참조(작업본 기준). WP-126 P3/P6 이 닿는 자리라 참고로만.

## 확인한 것 (PASS 근거)

**① 브리프 §3 포함 축 8건 — 전부 실림 (8/8)**

| 브리프 축 | WP-126 자리 | 판정 |
|---|---|---|
| 1 라운드 판정 1벌(활성 라운드) | Phase 1 (`:147-163`) + Scope `:38` + invariant `:92` | ✔ 3벌(`round_piece._active_round_complete` / `tasks_surface.round_complete` / `factory.has_open_in_run_chain`) 전부 명시 · 「역할 분리」까지 |
| 2 run 감사 + 종결 시 추적 태스크 정리 | Phase 2 (`:165-185`) | ✔ 실림 (전제는 W1) |
| 3 Slack fail-loud + `/incidents/slack/complete` 폐쇄 | Phase 3 (`:187-205`) | ✔ |
| 4 RegenGate 이벤트 이름 가드 | Phase 4 (`:207-219`) + OI-3 | ✔ (계약 절 부재 → OQ 대신 OI 로 처리, 브리프 문구 「없으면 OQ 로」에 부합) |
| 5 죽은 코드 정리(BFF 3·상수·pyc) | Phase 6 (`:239-255`) | ✔ 실림 (목록 정확도는 W2) |
| 6 `is_required`·`scope_slug` drop migration | Scope 제외 `:57` + OI-1 `:280` | ✔ **실측 근거로 제외** — 아래 ⑥ |
| 7 is_lead 게이트 · 추적 Task cc | Phase 5 (`:221-237`) + OI-4 | ✔ OQ-13 을 발명하지 않고 「특정 못 하면 cc 를 비운다」까지만 |
| 8 범위 밖 유지 | Scope 제외 `:51-59` | ✔ OQ-1·2·14·15·16 각각 링크 |

**② SPEC-152 ↔ WP-126 정합 — 발명 0, 누락 0**

- §라운드 판정 정본(spec-152:1507 표)의 4축(모수=최대 `round_no` / 제외=round 0·`deleted_at`·`manual.*`·`ai.*` / terminal=`done`·`canceled` 조건 없음 / 판정 자리=전이 seam 안쪽)이 `work-126:92`·`:152`·`:156` 에 **문언 단위로 일치**. 「4 표면 전부 발화」 검증(`:162`)도 SPEC 각주(spec-152:1519)와 대응.
- §U-2 Slack fail-loud 표(spec-152:212~)의 새 계약(`failed_retryable` · run `awaiting_declare` 유지 · 카드 잔존 · retry 이어짐 · 초대 `slack_id` 미해소는 감사)이 `work-126:41`·`:192-196` 에 1:1.
- §케이스 매트릭스(spec-152:1745) `SLACK_NOT_CONFIGURED` **503** ↔ `work-126:193` 503 일치. 코드 grep 결과 현행 부재 → 「신설」 표기 정확.
- §담당자 축과 참조자(spec-152:1428~)의 resolver 4단·cc=제품·버전 참여자 전원−담당자·TK-2/TK-3 cc 없음·미특정 시 cc 비움 ↔ `work-126:226-231` 전부 일치.
- §종결 시 태스크 정리(spec-152:1556 표)의 4행(round 0 = 시스템 `canceled` / 열린 예방 Task = 422 거부 / finalize `[완료]` 도 같은 검사 / `rejected` 는 대상 0) ↔ `work-126:173-176` 4행 일치. 두 처분을 섞지 않는 것까지.
- §TaskEvent 어휘(spec-152:1529 표)가 `workflow_closed` 를 「이관 — TaskEvent 가 아니다」로 확정 ↔ `work-126:171` 이 같은 경고를 싣는다.
- SPEC 이 계약한 축 중 **WP 에서 빠진 것 없음**. 반대로 WP 가 계약 밖 설계를 세운 곳도 없음(P2 payload 요구는 SPEC 본문 유래 — W1 참조).

**③ frontmatter · 번호 · 링크**

- `depends_on: [MEDINESS-WP-125]` ✔ (`work-126:11-12`), `covers: [MEDINESS-SPEC-152]` ✔, `status: proposed` ✔ (전 Phase `Status: TODO` 와 정합 — lint 7→8 게이트 통과)
- `Status:` 라인 7개 전부 깨끗한 enum 단독 형식 ✔ (형식 위반 ERROR 0)
- WP 번호 126 = `30-work/` 다음 빈 번호 ✔ (기존 최대 125, `work-200-desktop.md` 는 예약 대역)
- `doc_no: MEDINESS-DOC-246` ✔ — 현행+`90-archive/` 전체 스캔 max 가 245(`work-125`), 246 은 유일(전 레포 1건)
- 상대링크 9종 전부 실재 ✔ (`../20-spec/spec-150/152/153`, `../30-work.md`, `../40-architecture/domains/runtime_task.md`, `../40-architecture/erd.md`, `work-074`, `work-078`, `work-125`)

**④ 30-work.md 3표 + log.md 동기**

- Status Board `:112` 신규 행 ✔ (11컬럼 = 표준 10컬럼 정합, `proposed`/`TBD`/`1.5w`/`TBD`/`—`/`—`)
- WP List `:198` 신규 행 ✔ (`proposed` · `TBD` · 파일 링크 · Covers `MEDINESS-SPEC-152`)
- Spec Coverage `:277` SPEC-152 행에 `MEDINESS-WP-126` 추가 ✔ / 구현 상태 `in_dev` = covering WP derive 값과 일치(lint WARN 없음 — SPEC-152 행에 대한 derive 경고 0)
- frontmatter `status: proposed` ↔ Board ↔ WP List **3자 일치** ✔ (lint ERROR 0)
- log.md 변경 이력 표에 `wp-add` 행 1건 prepend ✔ (역시간순 유지, PR 칸 `—` 는 미PR 행의 기존 관례와 동형) — 다만 W3
- 「Spec Coverage 상태는 covering WP 전부 done 일 때만 `done`」 규칙 ✔ (SPEC-152 는 `in_dev` 유지, WP-126 추가로 바뀌지 않음)

**⑤ planner OI 처분 판단 — 3건 모두 적정**

- **OI-1**(`is_required` 대상 없음) — ✔ **실측 일치**. `back/alembic/versions/0066_task_scope_slug_dates.py:32` `op.drop_column("tasks", "is_required")` · `:27` `op.add_column("tasks", scope_slug)`. 파일 docstring 이 「예방 Task 는 전량 필수 → is_required 컬럼 제거」로 의도까지 명시. `scope_slug` 는 SPEC-152 §TK-2·`runtime_task.md` §Schema 가 들고 있는 살아 있는 계약 컬럼 ⇒ drop 대상 아님. **판단 정확.**
- **OI-2**(`/incidents/slack/complete` 소유 중복 → P0 조건부) — ✔ **적정**. app HEAD 에는 라우트가 **존재**(`action_runtime_v2.py:830`)하고, 같은 워크트리 **미커밋 작업본에서는 이미 제거**돼 있다(WP-125 BE 진행 중, 31파일 미커밋). 즉 지금 이 순간 「착지 중」이라 「P0 에서 확인 → 미착지면 P3 에서 닫는다」가 **정확히 맞는 처분**이다. 정본 소유를 WP-125 P3 에 두고 이 WP 를 조건부로 둔 것도 중복 착지 방지로 타당.
- **OI-3**(RegenGate = SPEC-150 소유 공용 조각, 버그 수정 범위만) — ✔ **적정**. ⓐ `regen_gate.py:80-105` `on_event` 가 `event.name` 을 **한 번도 읽지 않는다**(payload 의 `feedback`·`actor_id` 만 사용) → 「어떤 이벤트든 접수」 진단 정확. ⓑ SPEC-152 전문에 `regen_gate`/`RegenGate` 언급 **0건** → 「계약 절이 없다」 정확. ⓒ 조각 계약은 `spec-150:327` §5.5 조각 라이브러리 소유 확인 → 「그 이상은 SPEC-150 개정 사안」 라우팅이 `rules/document-pipeline.md` §변경 라우팅과 부합.
- (추가) OI-9(`task_scope_changed` 구현 0) 도 계약↔코드 갭을 **고치지 않고 보고만** 한 처리라 브리프 §7 준수.

**⑥ 코디네이터 정정 3곳 — 실측(alembic 0066)과 일치**

| 정정 위치 | 정정 후 문면 | 실측 |
|---|---|---|
| `spec-152:1930` §Functional Rule | 「`0066_task_scope_slug_dates` 로 이미 drop 됐다(구 서술은 오기)」 | ✔ `0066:32` `drop_column("tasks","is_required")` |
| `work-125:62` §Scope 제외 | 「대상 없음 확인 — `0066` 이 이미 drop, `scope_slug` 는 살아 있는 계약」 | ✔ `0066:27` `add_column(scope_slug)` + SPEC-152 §TK-2 존치 |
| `work-125:319` OI-4 | 「해소 — 대상 없음」 취소선 처리 + 근거 | ✔ 동일 근거 |

세 문장 모두 사실과 일치. 취소선(`~~…~~`) + 「해소」 표기로 원문을 보존한 것도 forward-only 규율에 맞다. (단 W3 — 이 정정이 log.md 행에 반영되지 않았다.)

**⑦ lint**

```
python3 scripts/lint-pipeline.py --strict  → exit 0
0 error, 255 warning
mediness 범위 ERROR: 0
mediness 범위 WARN: 1 (30-work.md:234 SPEC-030 — 기존 부채, 이번 diff 밖)
타 제품 WARN: 254 (charty/linky/selly/procedure-hub 등 doc_no 누락 — 무관)
```

**⑧ 확인 안 한 것 (숨기지 않음)**

- **P0 실측 항목 자체**(prod·stage 의 열린 round 0 추적 Task 수 · `responding` 좌초 run 수 · Slack 토큰 현행 설정값) — 운영 DB·환경 접근이 필요해 검수 범위 밖. WP 가 P0 에 배치한 것이 맞는 처리다.
- **`definitions.py:164~` Slack 3단 본문**과 `tools/steps.py` 멱등 앵커(`execution.result.external_refs`)의 실물 — 파일·심볼 존재만 확인했고 로직 정합은 미검증(코드 리뷰가 아니라 계획 검수 범위).
- **도메인 이벤트 상수 12종**의 참조 0 여부 — 4개만 표본 확인(3개 참조 0 · `STATUS_FAILED` 는 살아 있음 = W2). 나머지는 P6 의 per-symbol grep 게이트에 맡긴다.
- **SPEC-152 본문 ↔ 상위기획 정합**(사람 판단 영역, lint 대상 아님) — 이번 라운드에서 SPEC 은 1줄만 바뀌어 재검증 불요로 봤다.

## 코디네이터에게 — 처분 제안

| 항목 | 제안 |
|---|---|
| W1 | **PR 전 수정 권장.** planner 재발주 1턴이면 충분(P2 문구 + OI-5 재정의 + `migration 0` 조건부화). SPEC-152 §run 감사의 「Task id 목록」 축은 **사용자 결정 대상**(원장에 payload 를 열 것인가 vs 목록을 안 남길 것인가)이라 질문으로 올릴 값어치가 있다 |
| W2 | **PR 전 수정 권장.** `STATUS_FAILED` 한 줄 제거 + pyc 항목 조건부화. 1분 작업 |
| W3 | **PR 전 수정 필수 수준.** 장부가 틀린 사실을 남긴다. 코디 본인이 넣은 정정이라 코디가 직접 log.md 한 행 고치는 게 빠름 |
| W4 | 선택. 고칠 거면 줄번호를 떼는 쪽을 권함(다음 라운드에 또 낡는다) |
