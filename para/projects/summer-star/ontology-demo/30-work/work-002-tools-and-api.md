---
type: work
id: WORK-002
title: "조회 도구 4종과 API 서버 — FastMCP · 계층/KPI/그래프/예보 · 접속 게이트"
status: todo
product: ontology-demo
work_type: new-feature
owner: kknaks
roles:
  pm: "kknaks"
  design: "—"
  fe: "—"
  be: "@ontology-be"
  qa: "coordinator"
  ops: "kknaks"
progress: 0
created_at: 2026-09-02
updated_at: 2026-09-02
tags:
  - product/ontology-demo
  - doc/work
  - status/todo
links:
  baselines:
    - "[[baseline-001-demo-agent-app|BASE-001]]"
  decisions:
    - "[[decision-002-pii-masking-boundary|DEC-002]]"
    - "[[decision-003-llm-via-open-kknaks-mcp|DEC-003]]"
    - "[[decision-004-web-three-pages-in-front|DEC-004]]"
    - "[[decision-005-internal-demo-deploy|DEC-005]]"
  specs:
    - "[[spec-002-mcp-tools-contract|SPEC-002]]"
    - "[[spec-003-api-and-chat-contract|SPEC-003]]"
  works:
    - "[[work-001-data-foundation|WORK-001]]"
  releases: []
  related: []
---

# 조회 도구 4종과 API 서버

WORK-001 이 세운 DB 위에 **읽는 표면 둘**을 만든다 — 에이전트가 쓰는 FastMCP 도구 4종과
프론트가 쓰는 HTTP API(계층·KPI·그래프·예보 + 접속 게이트). 둘 다 **마스킹 뷰·골드 View
만** 읽고 원 테이블에 닿지 않는다.
**비목표**: 채팅 API·에이전트 루프(WORK-003) · 화면(WORK-004) · 배포(WORK-005).

## Meta

- Baseline: BASE-001
- Covers spec: SPEC-002 전체 · SPEC-003 (채팅 절 제외 — 접속 게이트 · 계층 · KPI ·
  그래프 · 예보)
- Depends on work: WORK-001 (DB·뷰·읽기 전용 커넥션 헬퍼)
- Parallel work: WORK-004 P1~P3 (FE 는 SPEC-003·004 계약을 보고 mock 으로 병행)
- Follow-up work: WORK-003(에이전트·채팅)
- External dependency: FastMCP(Streamable HTTP). 모범 구현은 이 레포의 `app/mcp/` —
  구조만 참고하고 tool 목록은 SPEC-002 를 따른다.

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | @ontology-be |
| Status | todo |
| Progress | 0% |
| Branch/PR | - |
| Blocker | WORK-001 완료 대기 |
| Next | WORK-001 Phase 5 통과 후 Phase 1 착수 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위와 요구사항 | todo |
| Design | — | 해당 없음(응답 계약만) | todo |
| FE | — | 소비자 — WORK-004 | todo |
| BE | @ontology-be | 도구·API 구현 | todo |
| QA | coordinator | 계약 일치·거부 경로 검증 | todo |
| Ops | kknaks | env(비밀번호·포트) | todo |

## Scope

포함:

- FastMCP(Streamable HTTP) 서버 + allowlist 판정·상한 검증 계층
- 도구 4종 — `query_kpi` · `query_layer` · `trace_ontology` · `get_definition`
- FastAPI 앱 + **접속 게이트 인증**(env 비밀번호 1개 → 세션 쿠키 `ontology_demo_sid`)
- 계층 조회 API — `tables`(+`flows_to`) · 행 조회 · `lineage`(`rule_id`·`gate`·
  `downstream`·`is_provisional`)
- KPI API — `cards`(`dod`·`unit`·`format`·`grain`·`spark[7]`·`node_id`·기간) · `series`
- 그래프 API(`edge_id`·`kind`·`note`·노드 `source`) · 예보 API(`title`·`message`·
  `edge.evidence`)
- 에러 코드 단일 표 구현(SPEC-002 §4 · SPEC-003 Case Matrix)

제외:

- 채팅 API·제출부·소비자 → WORK-003
- rate limit·계정·권한 등급 — **두지 않기로 확정**(DEC-005 D2)
- 컬럼 값 분포 엔드포인트 — SPEC-003 OQ-8 미결(제거 권고)

## Code Surface

- Repo / module: `kknaks_profile` — `app/ontology-agent/`
- 만질 파일 후보:

| 경로 후보 | 설명 |
|---|---|
| `app/ontology-agent/tools/` | FastMCP 서버 · 도구 4종 · allowlist |
| `app/ontology-agent/api/` | 라우터 — auth · layers · kpi · graph · forecast |
| `app/ontology-agent/main.py` | 앱 조립 · 미들웨어(세션 검증) |
| `app/ontology-agent/config.py` | `ONTOLOGY_DEMO_PASSWORD` 등 env |
| `app/ontology-agent/tests/` | 계약·거부 경로 테스트 |

- Domain / schema note: **스키마를 만들지 않는다.** WORK-001 의 테이블·뷰를 읽기만 한다.
  migration 없음.

## Domain / Schema

해당 없음 — 읽기 전용 표면이다. 세션은 서버 메모리/쿠키 검증으로 충분하며 테이블을
새로 만들지 않는다(내부 공유 데모 · DEC-005).

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| WORK-003 에이전트 | MCP 도구 4종 | 이름·파라미터·응답 = SPEC-002 §4. 임의 변경 금지 |
| WORK-004 FE | HTTP API | 응답 필드명 임의 변경 금지 — 어긋나면 spec 개정 보고 |
| WORK-005 통합 | 세션·에러 코드 | 배포 검증이 같은 계약을 친다 |

## Internal Interface Contract

- 도구 서버와 API 서버는 **같은 읽기 전용 커넥션 헬퍼**(WORK-001)를 쓴다. 쓰기 권한 없이
  DB 를 연다.
- `/api/kpi/series` 는 `query_kpi` 와 **같은 골드 View 를 같은 규칙으로** 읽는다 —
  화면용 집계 로직을 따로 만들지 않는다(도구와 화면이 다른 수치를 보면 안 된다).
- 허용 목록(테이블·필드·지표)은 **한 곳에 정의**하고 도구와 API 가 공유한다.
  blocklist 방식을 쓰지 않는다 — 새 컬럼이 생기면 자동으로 새는 쪽이 된다.

## Execution

### Phase 1 — FastMCP 서버 골격과 검증 계층

- **Status**: TODO
- **설명**: 도구가 쥘 수 있는 것의 상한을 먼저 세운다. 여기가 뚫리면 뒤의 도구가 전부
  뚫린다.
- **작업**:
  - [ ] FastMCP(Streamable HTTP) 서버 기동 · codex 가 MCP 클라이언트로 붙는 경로 확인
  - [ ] allowlist 판정 — 허용 테이블·필드·지표 화이트리스트, 목록 밖은 거부
  - [ ] 상한 검증 — `limit` 1~200, 필터 최대 5개, `depth` 1~3. **초과는 절단이 아니라 거부**
  - [ ] 읽기 전용 커넥션 사용 · `sql`/`path` 류 자유 입력 파라미터 부재
- **검증**:
  - [ ] PII 컬럼(`patientName`·`phone`·`birthday`·`authorName`)을 `field`·`filters`·
        `order_by` 에 **지정할 수 있고**, 필터·정렬이 **마스킹값 기준**으로 동작한다 —
        원값을 조건으로 준 조회는 **매치 0건**이고 응답에 원값이 없다(SPEC-002 AC-3)
  - [ ] `limit=201` 이 `LIMIT_EXCEEDED` 로 거부되고 조용히 잘리지 않는다
  - [ ] 쓰기 시도가 DB 레벨에서 실패한다
- **완료 증거**: 미작성 — 거부 경로 테스트 통과 목록 + 도구 목록이 정확히 4종이고 자유
  SQL·파일·쉘 도구 **0개**임을 출력으로 확인 (SPEC-002 AC-1·AC-2·AC-3·AC-9·AC-11)

### Phase 2 — 도구 4종 구현

- **Status**: TODO
- **설명**: 에이전트가 쥐는 네 개의 손. 집계는 View 가 하고 도구는 돌려주기만 한다.
- **작업**:
  - [ ] `query_kpi` — `grain` 4값이 각각 골드 View **조회**(도구가 집계하지 않는다).
        `formulas`·`status_thresholds`·`source` 동봉
  - [ ] `query_layer` — 마스킹 뷰만 조회, `masked_fields`·`total` 항상 동봉
  - [ ] `trace_ontology` — 판정 5종·사유·`usable_for_causal_claim`·`edge_id`·
        `lag`(정본 원형 보존) + `lag_days`(정수). 기본 호출은 채택·자동 확정·선언만
  - [ ] `get_definition` — 글로서리 판정 표 + KPI 컬럼 + enum(폐쇄 목록 13종·감성 4값)
- **검증**:
  - [ ] `query_kpi` 값이 골드 재조회값과 오차 0
  - [ ] 관측 없음(`null`)과 실제 0 이 구분된다(`naver_reviews` 2026-03-21 이전 vs 유기 신호)
  - [ ] 빈 결과가 에러가 아니라 200 + 빈 배열
  - [ ] 기각·보류 엣지가 `usable_for_causal_claim: false` 로 온다
- **완료 증거**: 미작성 — 도구 4종 호출 샘플 응답(마스킹 표기 포함) + 골드 대조 오차 0
  (SPEC-002 AC-4~AC-8·AC-10)

### Phase 3 — API 앱과 접속 게이트 인증

- **Status**: TODO
- **설명**: 내부 공유용 가드 하나. 얇게 만들되 모든 API 앞에 선다.
- **작업**:
  - [ ] FastAPI 앱 조립 · 라우터 등록 · **static 페이지 없음**(백은 API 서버 — DEC-004 D3)
  - [ ] `POST/GET /api/auth/session` — env `ONTOLOGY_DEMO_PASSWORD` 비교,
        쿠키 `ontology_demo_sid`(httpOnly · SameSite=Lax · Secure · 30일)
  - [ ] 세션 미들웨어 — 세션 없으면 전 API 401 `NO_SESSION`
  - [ ] 에러 본문 `{"detail": "<코드>"}` 통일
- **검증**:
  - [ ] 쿠키 없이 부른 모든 API 가 401
  - [ ] 비밀번호 값이 레포·문서·응답 어디에도 없다(env 로만 주입)
  - [ ] rate limit·계정 표면이 없다(DEC-005 D2 — 두지 않기로 확정)
- **완료 증거**: 미작성 — 401 경로 테스트 + env 미주입 시 기동 실패(또는 명시적 거부)
  로그 (SPEC-003 AC-1·AC-2)

### Phase 4 — 계층 조회 API

- **Status**: TODO
- **설명**: 데이터 화면이 딛는 표면. 상류·하류가 다 나와야 역추적이 화면에서 끊기지 않는다.
- **작업**:
  - [ ] `GET /api/layers/{layer}/tables` — `row_count`·`masked`·`note_ref`·**`flows_to[]`**
  - [ ] `GET /api/layers/{layer}/{table}` — 마스킹 뷰 경유, `total`·`returned`·`offset`·
        `masked_fields`·`columns`·`rows`
  - [ ] `GET /api/layers/{layer}/{table}/lineage` — `formula`·`note`·**`rule_id`**·
        **`gate`**·`source_columns`·**`downstream`**·**`is_provisional`**·`note_ref`·
        `status_thresholds`
  - [ ] 근거 기록 참조 — 브론즈→02 · 실버→04 · 골드→05
- **검증**:
  - [ ] 브론즈·실버 응답이 마스킹 표기로만 오고 원값 0건
  - [ ] `is_provisional`(미확정)과 `null`(관측 없음)이 구분된다
  - [ ] `limit` 상한 초과가 거부되고 `total` 로 전체 건수가 드러난다
- **완료 증거**: 미작성 — 3계층 샘플 응답 + `flows_to`/`downstream` 로 골드→실버→브론즈
  경로가 이어짐을 1건 실증 (SPEC-003 AC-3·AC-4·AC-11·AC-16)

### Phase 5 — KPI · 그래프 · 예보 API

- **Status**: TODO
- **설명**: 모니터링 화면이 딛는 표면. 화면이 숫자를 만들지 않도록 서버가 다 준다.
- **작업**:
  - [ ] `GET /api/kpi/cards` — `grain`·`dod`·`dod_pct`·`unit`·`format`·`spark[7]`·
        `alert_days`·`node_state`·`node_id`·`thresholds`·`direction`·`period`·
        `has_prev_period`·`has_next_period`. `naver_reviews` 는 상태 미부여
  - [ ] `GET /api/kpi/series` — `query_kpi` 와 같은 shape·같은 View
  - [ ] `GET /api/graph` — 노드(`source`·`observed`·`node_state`) · 엣지(`edge_id`·
        `kind`·`note`·`evidence`·`reason`·`usable_for_causal_claim`) · `counts`.
        보류·기각은 `verdicts` 명시 시에만
  - [ ] `GET /api/forecast` — 확정 엣지 2건, `title`·`message`·`edge.evidence`.
        **수치·신뢰도·lag 는 기록 07 정본값**(취소율→예약 `0d`·중간·r=−0.583 /
        강남언니→신환 `14d`·낮음·r=0.691 n=30)
- **검증**:
  - [ ] `/api/kpi/series` 값 = `query_kpi` 값(오차 0)
  - [ ] `node_state` 산정 = 최근 `window_days` 중 주의·경고인 날 수(알림 ≥3 · 관찰 ≥1)
  - [ ] 예보 응답에 하드코딩 수치가 없다(전부 DB 파생)
- **완료 증거**: 미작성 — cards/graph/forecast 샘플 응답 + 도구↔API 수치 대조 오차 0
  (SPEC-003 AC-5·AC-6·AC-7·AC-13·AC-14·AC-15)

## Pre-deploy Check

- [ ] 원 테이블(브론즈·실버)을 직접 읽는 조회 경로가 0개다 — 코드 경로 목록으로 확인
- [ ] 응답에 PII 원값·내부 경로·env 값이 없다
- [ ] 비밀번호가 로그에 원문으로 남지 않는다
- [ ] 기존 `app/back` 서비스에 영향 없음(별도 앱·별도 포트)

## Rollback

- 라우터 미등록 + MCP 서버 미기동으로 표면이 사라진다. **DB 를 건드리지 않으므로 데이터
  롤백이 필요 없다.**

## Done Criteria

- [ ] 모든 Phase 가 `DONE`
- [ ] SPEC-002 AC-1~AC-11 · SPEC-003 AC-1~AC-7·AC-11·AC-13~AC-16 이 테스트로 커버
- [ ] product `log.md` · `30-work/README.md` 갱신(코디네이터)

## Open Issues

- 세션 저장 방식(서명 쿠키 vs 서버 보관)은 코드 조사 후 워커가 정하고 근거를 보고에
  남긴다 — **테이블을 새로 만들지 않는 범위**여야 한다.
- SPEC-003 OQ-8(컬럼 값 분포 엔드포인트)은 미결이다. **제거 권고 상태이므로 만들지
  않는다** — 필요해지면 spec 개정 후 별도 phase 로 온다.

## Related

- SPEC: frontmatter `links.specs` · Work: 선행 WORK-001 · 후속 WORK-003 · 병렬 WORK-004
