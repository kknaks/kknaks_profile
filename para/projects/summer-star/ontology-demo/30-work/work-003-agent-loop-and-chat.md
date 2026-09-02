---
type: work
id: WORK-003
title: "에이전트 루프와 채팅 — open-kknaks 제출 · 폴딩 소비자 · 회귀 3본 (게이트 4·5)"
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
    - "[[decision-003-llm-via-open-kknaks-mcp|DEC-003]]"
    - "[[decision-002-pii-masking-boundary|DEC-002]]"
  specs:
    - "[[spec-005-agent-loop-and-gates|SPEC-005]]"
    - "[[spec-003-api-and-chat-contract|SPEC-003]]"
  works:
    - "[[work-002-tools-and-api|WORK-002]]"
  releases: []
  related:
    - "[[decision-027-chat-ai-execution-and-tool-boundary|KDEV-DEC-027]]"
---

# 에이전트 루프와 채팅

질문을 open-kknaks(codex) 태스크로 내보내고, 도구 4종만 쥔 에이전트가 **전제 검증 →
엣지 역추적 → 근거 수치 병기**로 답하게 한다. 답변은 `used_edges`·`citations` 를 필수로
싣고, 회귀 3본이 그것을 지킨다.
**비목표**: 화면(WORK-004) · 배포(WORK-005) · 계수 기반 정량 추정(범위 밖 — DEC-003 확정).

## Meta

- Baseline: BASE-001
- Covers spec: SPEC-005 전체 · SPEC-003 채팅 절(§4 채팅 · 상태기계 · 폴링)
- Depends on work: WORK-002 (도구 4종이 있어야 에이전트가 쥘 손이 생긴다)
- Parallel work: WORK-004 P1~P3 (FE 는 계약 mock 으로 병행. P4 채팅은 이 work 이후)
- Follow-up work: WORK-005(통합·배포)
- External dependency: open-kknaks(AgentClient + RedisBroker) · codex 런타임 ·
  `app/back` compose 의 redis. **큐는 `ontology` 로 분리**해 기존 파이프라인·채팅 큐와
  줄 세우지 않는다. 검증된 계약의 레퍼런스는 [[decision-027-chat-ai-execution-and-tool-boundary|KDEV-DEC-027]] 이다.

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | @ontology-be |
| Status | todo |
| Progress | 0% |
| Branch/PR | - |
| Blocker | WORK-002 완료 대기 |
| Next | WORK-002 Phase 5 통과 후 Phase 1 착수 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위와 요구사항 | todo |
| Design | — | 해당 없음(응답 계약만) | todo |
| FE | — | 소비자 — WORK-004 P4 | todo |
| BE | @ontology-be | 제출·소비자·루프·회귀 | todo |
| QA | coordinator | 게이트 4·5 재현 검증 | todo |
| Ops | kknaks | 워커 컨테이너·큐·env | todo |

## Scope

포함:

- open-kknaks 제출부 — provider `codex`, 모델 `gpt-5.6-terra`, `queue=ontology`,
  timeout 180초, MCP 도구 4종 allowlist, **쉘·웹검색 off**
- compose 에 codex 워커 서비스 추가(큐·CODEX_HOME 분리, 기존 서비스 무변경)
- 채팅 API — conversations·messages·retry, 상태기계 `pending → done/failed`
- 이벤트 폴딩 상주 소비자 — 부분 텍스트 누적 · `steps` 멱등 upsert · result 마감
- 답변 객체 검증·강제 — `used_edges` ⊆ 확정 · `citations` 재조회 일치 ·
  **정량 추정 금지** · `drilldown`·`followups`·`edge_id`
- **게이트 4(회귀 3본)** · **게이트 5(근거 무결성)**

제외:

- 화면·칩·폴링 UI → WORK-004 P4
- 게이트 1·2·3 전건 재실행·PII 스캔·배포 → WORK-005
- 계수(β) 산출 도구 — **범위 밖**(파이프라인 단계 검토)

## Code Surface

- Repo / module: `kknaks_profile` — `app/ontology-agent/` · `app/back/docker-compose*.yml`
- 만질 파일 후보:

| 경로 후보 | 설명 |
|---|---|
| `app/ontology-agent/agent/`(신설 후보) | 제출부 · 소비자 · 프롬프트 · 응답 검증 |
| `app/ontology-agent/api/` | 채팅 라우터(conversations · messages · retry) |
| `app/ontology-agent/config.py` | `ai_queue`·`ai_model`·`ai_timeout_sec`·`redis_url` |
| `app/back/docker-compose*.yml` | `queue=ontology` codex 워커 서비스 추가 |
| `app/ontology-agent/tests/` | 스키마 검증 · 폴딩 멱등 · 회귀 3본 |

- Domain / schema note: 대화·메시지 저장이 필요하다. **온톨로지 DB(브론즈~골드)와 섞지
  않는다** — 채팅 저장소는 별도 파일/스키마로 두고 데이터 계층을 오염시키지 않는다.

## Domain / Schema

| Entity | 역할 |
|---|---|
| `conversation` | 대화 1건 — 제목 · `ai_session_id`(내부, 비노출) · 시각 |
| `message` | role · status(`pending`/`done`/`failed`) · content · `steps[]` · `result` |

- 상태 / invariant: 한 conversation 에 `pending` assistant 는 **최대 1** — 동시 질문은
  409 `CONVERSATION_BUSY`. 다른 대화끼리는 병렬 허용.
- Migration 필요 여부: 채팅 저장소 신규. 파괴적 변경 없음(재생성 가능).
- SPEC 환류: 답변 객체 필드가 SPEC-005 §4 와 어긋나면 **임의 변경 금지** — 보고 후 spec 을
  먼저 고친다.

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| WORK-004 P4 | 채팅 API + `result` | 필드명 임의 변경 금지 |
| WORK-004 P2 | `used_edges[].edge_id` | 칩 클릭 → `?edge=` 점프의 키 |
| WORK-005 | 회귀 3본 스크립트 | 통합 검증이 그대로 재실행한다 |

## Internal Interface Contract

- 제출 옵션(모델·큐·timeout·MCP url/allowlist·쉘 off)은 **한 곳에서 조립**하고 테스트가
  그 조립 결과를 단언한다.
- 소비자는 이벤트를 DB 에 **폴딩**한다 — 같은 이벤트를 두 번 받아도 결과가 같아야 한다
  (`tool_use_id` 멱등). 중복 수신은 정상 경로다.
- 응답 검증기는 **API 경계에서** 돈다 — 스키마 위반은 1회 재시도 후 `failed` 표시.

## Execution

### Phase 1 — 제출부와 codex 워커

- **Status**: TODO
- **설명**: 실행 경로를 세운다. SDK 를 직접 import 하지 않는다(ADR-04).
- **작업**:
  - [ ] open-kknaks AgentClient + RedisBroker 제출 — `queue=ontology`,
        모델 `gpt-5.6-terra`, timeout 180초
  - [ ] MCP 접속 설정 — 도구 4종 allowlist, `features.shell_tool=false` ·
        `web_search` off · `sandbox=read-only`
  - [ ] compose 에 codex 워커 추가(전용 큐·CODEX_HOME, **기존 서비스 무변경**)
  - [ ] 시스템 프롬프트 — 도구 사용 규칙과 답변 형식만. **노드·엣지·인과 관계를 넣지 않는다**
- **검증**:
  - [ ] LLM SDK 직접 import 가 코드에 0건
  - [ ] 제출 옵션 조립 단언(모델·큐·timeout·allowlist·쉘 off)
  - [ ] 시스템 프롬프트에 노드·엣지·인과 관계 문자열 0건
- **완료 증거**: 미작성 — 제출 옵션 스냅샷 + 프롬프트 검사 통과 + 기존 compose 서비스
  diff 무변경 (SPEC-005 AC-보조 2)

### Phase 2 — 채팅 API와 폴딩 소비자

- **Status**: TODO
- **설명**: `pending` 동안 화면이 볼 것이 자라야 한다. 스피너만 도는 구간을 만들지 않는다.
- **작업**:
  - [ ] conversations 생성·목록·상세, messages 추가, retry(재제출)
  - [ ] 상태기계 `pending → done/failed`, 180초 초과 시 `failed`
  - [ ] 상주 소비자 — 부분 텍스트 누적 · `steps` `tool_use_id` 멱등 upsert(+`duration_ms`·
        서버 생성 `args_summary`) · result 로 본문 교체 · 실패 마감
  - [ ] Case Matrix 에러 — `EMPTY_QUESTION`·`QUESTION_TOO_LONG`(1,000자)·`NOT_FOUND`·
        `CONVERSATION_BUSY`(409)·`AI_FAILED`·`AI_TIMEOUT`
- **검증**:
  - [ ] 같은 이벤트를 두 번 넣어도 폴딩 결과가 같다(멱등)
  - [ ] `pending` 중 폴링 응답의 `content`·`steps` 가 자란다
  - [ ] `pending` 있는 대화에 질문하면 409, retry 가 실패 답변을 되살린다
- **완료 증거**: 미작성 — 폴딩 멱등 테스트 + 2초 폴링으로 본문·단계가 자라는 로컬 실행
  기록(첫 응답 소요시간 실측 포함) (SPEC-003 AC-8·AC-10·AC-17)

### Phase 3 — 응답 스키마 강제와 루프 규칙

- **Status**: TODO
- **설명**: 이 제품이 증명하려는 명제(S-001·S-002)가 지켜지는지는 여기서 갈린다.
- **작업**:
  - [ ] 답변 객체 조립·검증 — `answer`·`premise_correction`(항상 존재)·`used_edges`·
        `excluded_edges`·`citations`(+`row_count`)·`drilldown`·`followups`·`unknowns`
  - [ ] `used_edges` ⊆ 확정(채택·산출0·외생) 강제 — 보류·기각은 `excluded_edges` 로만
  - [ ] `citations` 재조회 검증 — `source.table`·`column` 으로 다시 읽어 값 일치
  - [ ] **정량 추정 금지** — 도구가 주지 않은 수치를 만들면 위반. 엣지는 방향·부호·시차·
        신뢰도·근거(r·n·p)까지만 제시
  - [ ] `drilldown.rows` 는 마스킹 뷰 산출 그대로, `total` 동봉
  - [ ] 스키마 위반 시 1회 재시도 후 `failed`
- **검증**:
  - [ ] 보류·기각 엣지를 `used_edges` 에 넣으면 검증이 거부한다
  - [ ] `citations` 값이 DB 재조회와 오차 0
  - [ ] `drilldown` 응답에 PII 원값 0건
- **완료 증거**: 미작성 — 검증기 단위 테스트(위반 케이스 전건 거부) + 답변 샘플 1건의
  `used_edges`·`citations` 재조회 대조표 (SPEC-005 §4 Validation)

### Phase 4 — 회귀 3본과 **게이트 4·5**

- **Status**: TODO
- **설명**: 기록 08 의 시나리오를 자동화해 「같은 질문에 같은 근거로 답한다」를 반복
  검증 가능하게 만든다.
- **작업**:
  - [ ] **R-1 현황** 「최근 4주 노쇼율 추이는?」 — 주별 4행, `used_edges` 빈 배열,
        계산식 인용 존재
  - [ ] **R-2 원인·전제 교정** 「8월 매출이 왜 떨어졌어?」 — `premise_correction.corrected`
        = true, 확정 엣지만, 보류·기각 미포함
  - [ ] **R-3 드릴다운** 「8월 취소 원본 20건 보여줘」 — 20행·전 행 8월/`취소`·마스킹 표기·
        `masked_fields` 동봉
  - [ ] 판정은 사람 눈이 아니라 **단언**으로 — 수치는 정확 일치, 서술은 키워드 포함
- **검증**:
  - [ ] 3본을 반복 실행해도 통과한다
  - [ ] 게이트 5 — 답변 수치 = DB 재조회 일치 · `used_edges` ⊆ 확정 ·
        도구가 주지 않은 추정치 0건
- **완료 증거**: 미작성 — **게이트 4 통과**: R-1 노쇼율 **5.3% / 4.8% / 5.2% / 5.0%**
  (54/958 · 46/921 · 53/961 · 56/1,066, 전 주 「양호」) · R-2 8월 매출 **3.69억**
  (7월 2.91억 대비 **+27%**) 교정 후 내원 **5,428 → 4,196** · 예약 **9,057 → 6,852**,
  근거 수치(결제 내원 +23% 641건 · 객단가 58만 원 · 취소율 7월 36.3% → 8월 35.5% ·
  네이버 리뷰 96 → 12 → 8 → 4건) · R-3 20행 마스킹.
  **게이트 5 통과**: 재조회 오차 0 · `used_edges` ⊆ 확정 · 추정치 0건.
  (게이트 5-③ 하이라이트 대조는 화면이 붙는 WORK-005 에서 확인)

## Pre-deploy Check

- [ ] 기존 `queue=default`·`queue=chat` 워커 계약 무변경 — diff 로 확인
- [ ] 답변·로그에 PII 원값이 없다
- [ ] MCP 토큰·비밀번호가 로그에 원문으로 남지 않는다
- [ ] 채팅 저장소가 온톨로지 DB 를 오염시키지 않는다(별도 파일/스키마)

## Rollback

- 라우터 미등록 + compose 워커 서비스 제거로 표면이 사라진다. 채팅 저장소는 재생성
  가능하고 **온톨로지 DB 는 건드리지 않으므로** 데이터 롤백이 필요 없다.

## Done Criteria

- [ ] 모든 Phase 가 `DONE`
- [ ] 게이트 4·5 수치가 보고에 있다
- [ ] SPEC-005 AC(G1~G5 중 4·5 · R-1~R-3 · AC-보조 1·2)와 SPEC-003 채팅 AC 커버
- [ ] product `log.md` · `30-work/README.md` 갱신(코디네이터)

## Open Issues

- 첫 응답 지연(큐 왕복 + codex 기동 + 도구 왕복)의 실측값은 Phase 2 에서 재고 보고한다 —
  180초 timeout 이 충분한지 판단 근거가 된다(SPEC-005 OQ-6).
- 대화 이력은 세션 단위 보존이다. **공용 비밀번호라 사실상 공용 이력**이 된다는 전제를
  운영 시 다시 본다(SPEC-003 OQ-7 확정 사항의 부작용).

## Related

- SPEC: frontmatter `links.specs` · Work: 선행 WORK-002 · 후속 WORK-005 · 소비 WORK-004 P4
