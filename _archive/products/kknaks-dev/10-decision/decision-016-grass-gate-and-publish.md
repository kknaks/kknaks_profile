---
type: decision
id: KDEV-DEC-016
title: "잔디 승인 게이트 편입과 발행부 확장"
status: proposed
product: kknaks-dev
created_at: 2026-07-31
updated_at: 2026-07-31
tags:
  - product/kknaks-dev
  - doc/decision
  - status/proposed
links:
  baselines:
    - "[[baseline-004-commit-pipeline-and-career|KDEV-BL-004]]"
  decisions:
    - "[[decision-014-commit-source-and-repo-registry|KDEV-DEC-014]]"
    - "[[decision-015-grass-destinations-and-formats|KDEV-DEC-015]]"
    - "[[decision-011-approval-gate-chain|KDEV-DEC-011]]"
    - "[[decision-012-draft-storage-and-publish-boundary|KDEV-DEC-012]]"
  specs:
    - "[[spec-008-gate-chain|KDEV-SPEC-008]]"
    - "[[spec-009-gate-feedback|KDEV-SPEC-009]]"
    - "[[spec-010-apply-executor|KDEV-SPEC-010]]"
  works: []
  releases: []
  related:
    - "[[baseline-003-inbox-approval-pipeline|KDEV-BL-003]]"
    - "[[work-016-async-execution-and-progress-ui|KDEV-WORK-016]]"
up:
  - workflow-orchestration
  - async-io
---

# 잔디 승인 게이트 편입과 발행부 확장 (ADR-016)

잔디 잡을 기존 승인 게이트 위에 얹는다. 게이트·드라이버·API·화면은 **그대로 재사용**하고, 손대는 곳은 **체인 진행부와 발행부**다. [[decision-011-approval-gate-chain|KDEV-DEC-011]] 이 보류했던 "커밋 파이프라인 정의" 를 해소한다.

> 조사 원천은 [[decision-014-commit-source-and-repo-registry|KDEV-DEC-014]], 착지 경로는 [[decision-015-grass-destinations-and-formats|KDEV-DEC-015]].

## Context

- 관련 baseline: [[baseline-004-commit-pipeline-and-career|KDEV-BL-004]]
- **잔디는 BL-003 이 진단한 auto-commit 경로 4개 중 유일하게 남은 것이다.** Slack 지식캡처는 WORK-012~016 으로 게이트에 편입됐고, 잔디·algorithm·content_enrich 셋이 남았다. 이번 대상은 잔디다.
- **LLM 호출이 요청 안에서 블로킹한다.** `llm.py:181` `await client.result(...)`. WORK-016 이 게이트 경로 전체에 세운 "실행은 비동기다"(SPEC-009) 규율 밖이다.
- **push 에 롤백이 없다.** `commit_and_push_with_retry` 는 commit → rebase → push 순서라 push 실패 시 로컬 커밋이 남고, 다음 `POST /admin/reload` 의 `git reset --hard origin/main` 이 그것을 조용히 삭제한다. `apply/git.py:3-9` 가 이 함수를 쓰지 않는 이유로 명시해 둔 것이다.
- **게이트 코어는 재사용 가능하다.** `models.py:11-13` 이 `source_kind`·`stage_name`·`kind` 에 CHECK 를 일부러 안 걸었다 — 새 파이프라인 추가에 **마이그레이션이 없다**.

  | 모듈 | 손댈 것 |
  |---|---|
  | `core/models.py` 8테이블 · `gates.py` · `driver.py` · `queue.py` · admin FE | **없음** |
  | `definitions.py` · `runtime.py` | 등록 |
  | `executor.py AgentStage` | 서브클래스 |

- **`chain.py` 가 route 를 전제한다.** `enabled_stages(None)` 이 `()` 를 돌려주므로(`chain.py:40-41`) route 게이트가 없는 파이프라인은 `next_stage` 가 항상 `None` → 첫 승인에서 `chain_complete` → 즉시 발행. **게이트 1개면 우연히 맞고 2개 이상이면 두 번째가 조용히 건너뛰어진다.**
- **발행부가 지식 4층 전용이다.** `ALLOWED_PREFIXES`(`plan.py:25`)에 `persona/daily/`·`persona/career/` 없음 → `PATH_NOT_ALLOWED`. `LAYER_PREFIX`(`plan.py:32-39`)에 `daily`·`career` 없음 → `UNKNOWN_TYPE`. `build_actions()`(`plan.py:102·118`)는 `source_note`·`derived`·`concept` 하드코딩. `create` 는 파일 있으면 `ALREADY_EXISTS`, `replace` 는 없으면 `TARGET_MISSING`. `graph_check.virtual_nodes()`(`graph_check.py:44-54`)는 모든 액션을 그래프 노드로 얹는다. `_write_all()` 에 `auto:false` 보호가 없다.
- **중복 판정 축이 다르다.** `QueueItem` unique index 는 `normalized_url` 기준(`models.py:116-124`)인데 잔디는 URL 이 없고 날짜가 축이다.
- **스케줄러용 접수 진입점이 없다.** `intake()` 는 source_url/note 를 받는 사람·Slack 전제다.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[workflow-orchestration]] — `daily_commit` 을 **Stage 목록으로 등록**해 기존 게이트·드라이버·화면을 그대로 재사용한다 — 파이프라인이 데이터라서 가능한 일이다
- [[async-io]] — `investigate` 스테이지가 레포별로 **×N fan-out** 한다 — 겹쳐 돌려야 전체 시간이 「합」이 아니라 「가장 긴 하나」가 된다

## Options

### fan-out(레포별 상세조사 N건)을 어디에 둘 것인가

| Option | Description | Pros | Cons |
|---|---|---|---|
| A | `gates.py` 를 fan-out 지원하도록 확장 | 게이트에서 레포별 검토 가능 | `_submit()` 의 revision 1:1 과 `harvest()` 의 `drafting` `FOR UPDATE` 멱등 전제가 깨진다 |
| B | 레포마다 `QueueItem` 생성 | 기존 구조 그대로 | 하루치로 취합할 주체가 없다. 잔디는 하루 1파일 |
| **C** | **`kind="auto"` 스테이지 안에서 N건 실행** | **게이트 코어 무변경.** `GateRevision` 을 안 쓴다 | 레포별 개별 승인 불가(필요 없다) |

### 승인이 밀리면 잔디에 구멍이 난다

| Option | Description | Pros | Cons |
|---|---|---|---|
| **A** | **쌓이게 둔다** | 게이트 원칙 유지. 나중에 승인하면 채워진다 | 승인 전까지 잔디 칸이 빈다 |
| B | 타임아웃 자동 승인 | 잔디가 매일 나간다 | 게이트가 형해화된다 |
| C | 낙관 발행 + 사후 수정 | 지금과 동일한 즉시성 | `intake.py:3`("이 시점에 레포에는 아무 파일도 생기지 않는다")과 정면 충돌 |

## Decision

### D1. `daily_commit` 파이프라인을 등록한다

```python
DAILY_COMMIT = Pipeline("daily_commit", (
    Stage("collect",     "auto"),   # git 조사·career 귀속·counts (LLM 없음)
    Stage("investigate", "auto"),   # ×N fan-out — 레포별 diff 조사
    Stage("compose",     "auto"),   # 취합 — daily·career·concept 초안
    Stage("daily",       "gate"),   # 하루 1개. 승인 = 발행
))
```

youtube + 이것 = **2개**. `definitions.py:10-11` 이 정의 이관 시점을 "소스 종류 3개 초과" 로 못 박아 뒀으므로 **코드 상수를 유지한다.**

[[decision-011-approval-gate-chain|KDEV-DEC-011]] 이 보류했던 "커밋 파이프라인 정의" 를 이것으로 해소한다(블로그·스케줄은 여전히 보류).

### D2. fan-out 은 게이트 밖 `auto` 스테이지에 둔다

`gates.py:300-319 _submit()` 이 게이트당 revision 1개 + AITask 1개를 만들고, `harvest()` 가 `drafting` 하나를 `FOR UPDATE` 로 잡아 멱등성을 얻는다(`gates.py:356-362`). 여기에 N 개를 매달면 그 전제가 무너진다.

`kind="auto"` 스테이지는 승인 대상이 아니라 `GateRevision` 을 쓰지 않는다. 레포별 조사 결과는 `ItemPreparation` payload 에 누적한다. **`gates.py` 는 한 줄도 고치지 않는다.**

워커 동시성은 현재 부하 때문에 1이라 실제로는 순차 실행이다. 설계는 병렬을 전제하지 않는다.

**일부 레포 조사가 실패해도 부분 결과로 진행한다** (OQ-1 해소). 레포 하나가 막혔다고 그날 잔디를 통째로 못 내보내는 것은 과하다. 실패한 레포는 payload 에 남기고 게이트 화면이 "레포 N개 조사 실패" 로 표시한다 — `prepare.py:9-11` 이 이미 같은 판단을 했다("수집 실패가 항목을 죽이지 않는다"). 전 레포가 실패하면 그때는 스테이지 실패다.

### D3. route 게이트를 두지 않고, `chain.py` 를 일반화한다

잔디는 목적지가 고정이라 route 가 고를 것이 없다. 대신 **잠복 결함을 지금 고친다.**

```text
enabled_stages(route_payload=None)   →  파이프라인 정의의 게이트 스테이지 전부
enabled_stages(exclusive 있음)        →  ()            (기존과 동일)
enabled_stages(destinations 있음)     →  켜진 것만      (기존과 동일)
```

"route 결과가 없으면 끄는 주체가 없는 것" 이므로 전부 켜진 것으로 읽는다. daily 는 게이트가 1개라 지금 고치지 않아도 동작하지만, 다음 파이프라인이 밟는다. **파이프라인이 2개일 때 일반화하는 비용이 4개일 때보다 싸다** — `definitions.py:10-11` 이 정의 이관 시점을 미리 정해 둔 것과 같은 판단이다.

폐기 대응은 `QueueItem.status="discarded"` 로 이미 있다.

### D4. 활동 0 과 `auto:false` 는 `collect` 에서 끝낸다

게이트까지 올라온 항목은 **"발행할 내용이 있는 날"만**이어야 한다.

- 활동 0 → 항목을 만들지 않는다. LLM 을 부르지 않는다(현행 `llm.py:167` 과 같은 판단을 접수 앞으로 옮긴다).
- 대상 날짜의 daily 가 `auto:false`(본인 작성) → 접수하지 않는다. 현행 `main_job.py:45` 검사의 이전.

승인할 것이 없는 카드가 매일 쌓이면 화면이 무의미해진다.

### D5. "변경 없음" 이 정상 출력이다

career 는 매일 갱신 대상이지만 크게 바뀔 일이 드물다. 두 층에서 막는다.

1. **결정적 skip** — 그날 그 career 에 귀속된 커밋이 0이면 스테이지를 **만들지 않는다.** `collect` 이 이미 계산하므로 LLM 을 부르지 않는다.
2. **`changed: false`** — 커밋은 있으나 더할 게 없으면(같은 일 반복, 기존 줄에 이미 포함) 갱신안 없이 돌아온다. 액션을 만들지 않는다.

안전망은 이미 있다 — `apply/git.py:81-86` 의 `git diff --cached --quiet` 가 내용 동일 시 빈 커밋을 막는다.

### D6. 발행부(`apply/`)를 6가지로 확장한다

| # | 대상 | 변경 |
|---|---|---|
| 1 | `ALLOWED_PREFIXES` | `persona/daily/` · `persona/career/` 추가 |
| 2 | `LAYER_PREFIX` | `daily` → `persona/daily/`, `career` → `persona/career/` |
| 3 | `build_actions()` | 스테이지별 하드코딩에 daily·career 분기 추가 |
| 4 | 액션 종류 | **`upsert` 신설** — 경로 allowlist·층 정합만 보고 존재 여부는 안 본다 |
| 5 | `graph_check` | **daily·career 를 대상에서 제외.** concept 는 기존 규율 그대로 받는다 |
| 6 | 검증 | **`auto:false` 보호를 검증 항목으로 이관** — 대상 daily 가 본인 작성이면 위반으로 거부 |

`products/` 를 열지 않으므로(DEC-015 D8 기각 항목) `plan.py:23-24` 가 allowlist 를 좁게 잡은 의도("경로 조립에 버그가 있어도 `app/`·`.github/` 를 못 건드리게")를 유지한 채 **prefix 2개 추가로 끝난다.** 패턴 매칭 도입이 불필요해졌다.

`upsert` 가 필요한 이유 — daily·career 는 **첫 회 생성·이후 덮어쓰기가 둘 다 정상**이다. `create` 는 `ALREADY_EXISTS`(`plan.py:224-228`), `replace` 는 첫 회 `TARGET_MISSING`(`plan.py:235`) 이라 지금 구조로는 매일 액션 종류가 갈린다.

`graph_check` 제외 근거 — daily·career 는 지식그래프 노드가 아니다(`_build_graph_nodes()` 도 notes+products+permanent 만 넣는다). `up:` 이 없어 얹으면 L2 ERROR 로 발행이 막힌다. 그래프 재정비는 별도 범위이므로 여기서는 **제외로 통과시킨다.**

### D7. 발행은 `publish_atomic` 으로 간다

잔디가 `commit_and_push_with_retry` 를 떠난다. 승인분이 조용히 소실되는 경로([[decision-012-draft-storage-and-publish-boundary|KDEV-DEC-012]] D5 가 이미 판정)를 잔디에도 닫는다.

**승인 1회 = 커밋 1개** — daily·career·concept 가 한 커밋으로 나간다(DEC-012 D3 계승).

### D8. 접수 진입점과 중복 판정

- **스케줄러 접수** — `intake()` 에 잡 경로를 연다. `intake.py:5` 가 이미 "Slack·화면·**잡이** 같은 큐로 들어온다" 고 써 두었으나 경로가 없었다.
- **날짜 축 중복** — `normalized_url = "daily:{YYYY-MM-DD}"` 합성 키를 쓴다. `uq_queue_items_pending_url` 부분 인덱스가 그대로 먹어 **마이그레이션이 없다.** `models.py:133` 주석에 "URL 이 아닌 합성 키도 들어간다" 를 명시한다. 스케줄러가 `coalesce=True, max_instances=1`(`scheduler.py:26-27`)이라 실제 경합은 백필·수동 재실행뿐이고 그것을 이 키가 막는다.
- **백필을 이번에 연다** (OQ-4 해소). 접수 API 에 날짜 파라미터 하나를 둔다 — `run_daily_activity_job` 에 `target_date` override 가 이미 있고(`main_job.py:33`), 합성 키가 중복을 막아 준다. 나중에 붙이면 접수 진입점을 두 번 짜게 된다.

### D9. 승인 대기가 쌓이는 것을 받아들이고, 알림을 바꾼다

승인이 밀리면 그날 잔디 칸이 빈다. 지금은 그날 바로 push 하니 없던 갭이다. **그대로 둔다** — 승인 게이트를 붙이는 이유가 "AI 가 쓴 것을 그대로 내보내지 않겠다" 이고, 구멍이 나는 편이 정직하다.

대신 `notify_slack` 을 **발행 완료 알림에서 승인 대기 알림으로** 바꾼다. 안 그러면 쌓인 것을 모른다.

**주기는 발동 시 1회 + 미승인이 2건 이상 쌓였을 때만 재알림** (OQ-2 해소). 매일 "승인 대기 1건" 이 오면 소음이 되어 안 읽는다. 밀리기 시작한 시점에만 울리는 것이 신호다.

### D10. 게이트 화면이 갖춰야 할 것

- `summary[]` **줄 단위** 편집·삭제 (`payload_override`, `gates.py:549-550`)
- career 본문 **문장 단위** 승인 — concept 게이트의 `excluded` 토글(`plan.py:118-121`)과 같은 패턴. career 는 이력서라 다른 목적지보다 촘촘해야 한다
- 회사 레포 내용 절삭 — 조사는 균일하게 깊게 하고(DEC-014 D8) **공개 수준은 여기서 정한다**
- 토글: `daily`(항상) · `career` · `concept`
- DEC-014 D7 의 입력 상한에 걸렸다는 표시

### 기각

- **`gates.py` fan-out 확장** — 멱등 전제가 깨진다. 지금 도는 것을 위험에 빠뜨린다.
- **레포마다 `QueueItem`** — 하루치 취합 주체가 사라진다.
- **route 게이트 도입** — 목적지가 고정이라 고를 것이 없다.
- **타임아웃 자동 승인 / 낙관 발행** — 게이트 원칙과 충돌.
- **`chain.py` 를 daily 전용 예외로 우회** — 잠복 결함을 남긴다.

## Rationale

- **판단 기준** — 재사용 경계를 실측으로 그었다. **"사람이 AI 산출물을 검토·수정·승인하는 절차" 는 재사용 가능하고, "승인된 것을 무엇으로 만드는가" 는 코드를 늘려야 한다.** 그래서 이 작업의 실제 분량은 게이트가 아니라 `apply/` 에 있다.
- **대안 대비** — fan-out 을 게이트 안에 넣으면 표현력은 얻지만 WORK-016 이 세운 멱등 전제를 다시 검증해야 한다. auto 스테이지는 그 전제를 건드리지 않고 같은 결과를 낸다. 레포별 개별 승인은 매일 13번 누르는 기능이 되어 안 쓰인다.
- **리스크**
  - `chain.py` 일반화가 youtube 파이프라인에 회귀를 낼 수 있다 → route 승인분은 `destinations` 가 있어 기존 분기를 그대로 타므로 영향 없음. 테스트로 고정한다.
  - `graph_check` 제외가 구멍이 될 수 있다 → daily·career 는 원래 그래프 밖이다. concept 는 제외하지 않는다.
  - 승인 지연으로 잔디에 구멍 → D9 로 받아들이되 알림으로 보완.
  - `upsert` 도입이 기존 검증을 느슨하게 만들 수 있다 → daily·career 액션에만 허용하고 knowledge 계열은 기존 create/replace 를 유지한다.

## Scope

- **In** — `daily_commit` 파이프라인 정의와 스테이지 실행기, `chain.enabled_stages` 일반화, `apply/` 확장 6종, `publish_atomic` 전환, 스케줄러 접수 진입점, 합성 키 중복 판정, Slack 알림 전환, 게이트 화면 요구.
- **Out** — 조사 원천(DEC-014), 착지 경로·양식(DEC-015), `algorithms`·`content_enrich` 잡의 게이트 편입(남은 auto-commit 경로 2개), 그래프 재정비.
- **영향을 받는 spec 후보** — `KDEV-SPEC-008`(파이프라인 정의에 daily_commit 추가, route 없는 체인), `KDEV-SPEC-010`(allowlist·`upsert`·graph_check 제외·`auto:false` 검증), 신규 spec(잔디 게이트 계약).

## Open Questions

**spec 을 막는 것은 없다.**

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-3 | `algorithms`·`content_enrich` 의 게이트 편입 시점 — 남은 auto-commit 경로 2개 | kknaks | 후속 baseline |

### 해소됨

| ID | Question | 결론 |
|---|---|---|
| ~~OQ-1~~ | `investigate` 부분 실패 처리 | **부분 결과로 진행** (D2). 레포 하나로 그날 전체를 막지 않는다. 전 레포 실패면 스테이지 실패 |
| ~~OQ-2~~ | 승인 대기 알림 주기 | **발동 시 1회 + 미승인 2건 이상일 때 재알림** (D9). 매일 울리면 소음이 되어 안 읽는다 |
| ~~OQ-4~~ | 백필 경로를 이번에 열지 | **연다** (D8). `target_date` override 가 이미 있고 합성 키가 중복을 막는다. 나중에 붙이면 접수 진입점을 두 번 짠다 |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| 잔디 게이트 계약 (신규) | create | 파이프라인 정의 · 스테이지 계약 · 게이트 화면 |
| `KDEV-SPEC-008` | update | route 없는 체인, `enabled_stages` 일반화 |
| `KDEV-SPEC-010` | update | allowlist 2종 · `upsert` 액션 · graph_check 제외 · `auto:false` 검증 |
