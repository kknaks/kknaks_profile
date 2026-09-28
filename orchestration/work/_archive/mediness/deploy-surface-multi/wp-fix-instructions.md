# [planner · micro] WP-131 정정 — migration 번호 stale + 대시보드 결정 기록

**WP-131 로 BE·FE 가 실제로 굴렀고, 네가 잡아 둔 §Code Surface·§Domain/Schema 가 그대로 먹혔다.** 특히 5단계 migration 순서와 down 중복가드는 BE 가 테스트로 실증했다(왕복 8/8, `charty/prod(2건)` 이 RuntimeError 메시지에 실리는 것까지).

두 가지를 고친다. **`spec PR #762` 브랜치 `kknaksss/deploy-surface-multi-spec` 이 아직 미머지라 같은 브랜치에 얹는다.**

## 1. migration 번호가 stale 이다 — 네 잘못이 아니다

WP 가 `head = 0124_meeting_v2_topic_evidence` → 신규 `0125_deployment_surface_key` 로 잡았는데, **실제 `origin/dev` head 는 `0138_task_body_and_references`** 다. BE 가 직접 확인해 **`0139_deployment_surface_key`** 로 만들었고 그게 맞다.

**원인**: 네가 읽은 `/Users/kknaks/git/harness_works/mediness-app` 은 **canonical 체크아웃이고 사용자 피처 브랜치 상태**라 `origin/dev` 보다 뒤처져 있었다(`0134`~`0138` 이 없었다). 그 레포 config 노트가 「canonical 은 사용자 피처 브랜치 체크아웃 중」이라 경고하는 자리다. **네가 실측한 것은 맞고, 실측 대상이 낡았다.**

### 할 것

`products/mediness/30-work/work-131-deploy-surface-axis.md` 에서 **migration 번호·head 를 말하는 자리를 전수로** 찾아 고쳐라. 내가 본 것은 §Code Surface 표와 §Domain/Schema 의 `Migration 필요 여부` 두 곳이고 **전수가 아니다** — Phase 1 본문·Pre-deploy·Rollback·Related 까지 네가 다시 grep 해라.

- `0124_meeting_v2_topic_evidence` → **`0138_task_body_refs`**(⚠ `down_revision` 문자열은 파일명이 아니라 **`0138_task_body_refs`** 다. 파일명은 `0138_task_body_and_references.py` — 혼동하지 마라. BE 가 만든 `0139` 파일의 `down_revision` 값을 그대로 확인해 써라)
- `0125_deployment_surface_key` → **`0139_deployment_surface_key`**
- 「`back/alembic/versions/` 124개」 같은 **개수 실측값도 지워라** — 코드가 SoT 인 숫자를 문서에 박으면 또 굳는다(W-14 에서 「17 row」에 한 그 판단과 같다).
- **왜 어긋났는지 한 줄** 남겨라 — 「착수 시점 실측이 canonical(피처 브랜치) 기준이라 `origin/dev` 보다 뒤처져 있었다. **alembic head 는 워크트리 base 에서 재확인한다**」. 다음 WP 가 같은 함정을 밟는다.

## 2. 대시보드 결정을 기록한다 — 사용자 판단 2026-09-22

BE 가 구현 중 찾아 미결로 올린 건이다:

`back/app/services/dashboard/db_source.py:134-136` 이 배포 행을 `{slug: {env: url}}` **2축 dict** 로 접는다. 한 (제품, 환경)에 행이 여럿이면 **마지막이 앞을 덮고 어느 게 남는지가 조회 순서에 달려 있다.** 소비처 `ProductLinks(dev=…, prod=…)` 는 환경당 링크 한 칸이다. nexus prod 6행이 들어오면 5개가 조용히 사라진다.

**사용자 결정**: 카드는 **환경당 1개 유지**하되, **어느 것이 뜰지를 결정적으로 고정**한다 — `surface_key == "기본"` 우선, 없으면 `surface_key` 오름차순 첫째. **「대표 surface」 개념 신설은 하지 않는다**(스펙 판으로 남긴다).

### 할 것

- **WP §Scope 또는 §Execution 에 Phase 를 하나 추가**해라(번호는 네 판단 — BE 몫이고 이미 발주됐다). 내용 = 위 결정 + 회귀 테스트(행 2~3개일 때 항상 같은 값 · `기본` 부재 시 오름차순 첫째 · **행 1건 제품은 결과 불변**).
- **§Open Issues 에 남은 것**을 적어라 — 「카드가 6개를 다 보여주지 않는다. 표면 여럿을 대시보드에 어떻게 드러낼지는 **SPEC-100/101 소유**이며 SPEC-051 §6 OQ-3(대시보드가 레지스트리를 SoT 로 읽는 방향)과 같은 층이다. 이번 판은 **비결정성만 제거**한다.」
- **`기본` 우선은 표시 우선순위지 sentinel 이 아니다** — SPEC-051 §4 Functional Rule 이 「`기본` 은 sentinel 아님」을 계약으로 갖고 있으니, 그 계약과 충돌하지 않게 **「서버 분기가 아니라 표시 정렬 규칙」**임을 명시해라.

## 하지 말 것

- **`spec-051`·`21-html`·`log.md`·`30-work.md` 를 고치지 마라.** WP-131 한 파일만이다. (SPEC 계약은 안 바뀐다 — 대시보드 결정은 구현 층이다.)
- **「대표 surface」를 SPEC 에 신설하지 마라.**
- 코드 레포 수정 금지 — 읽기만(`0139` 파일의 `down_revision` 확인용).
- 커밋·push·PR 금지. **코디가 같은 브랜치에 얹는다.**

## 검증

```
cd /Users/kknaks/orca/workspaces/mediness-mediness/deploy-surface-multi-spec
python3 scripts/lint-pipeline.py --strict
```

- **0 error / 263 warning 유지.**
- grep 전수: `0124` · `0125` 잔존 0 · 「124개」류 개수 실측값 잔존 0.

## 리포트

`planner-report.md` 에 「8차 — WP 정정」 절로. 고친 자리 전수 + grep 결과.

끝나면 §9 완료 보고 두 채널. **코디handle 은 preamble 값을 믿어라.**
