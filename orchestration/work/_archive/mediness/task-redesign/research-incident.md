# 사전 조사 — mediness incident 워크플로 재정비

> task-redesign(전체 재정비) 발주 스펙의 근거 문서 2/2. 렌즈 6개는 사용자 지정:
> ① 슬랙 연결·형식 ② 슬랙으로 작업 생성 ③ 후속 테스크 생성 ④ 후속 테스크 피드백 ⑤ 루프 구조 ⑥ 완료처리
> §A = spec 레포 문서 조사 (2026-08-31 완료) / §B = app 코드 조사 (진행 중 — 완료 시 append)

---

## §A. spec 문서 조사 (레포: mediness-mediness)

조사 범위: spec-152(1869줄, B축 SoT)·spec-150·spec-153·spec-119·work-074·action-runtime-engine.md·work-076~078·inbox 원형·log.md·git 이력.

좌표 정정: `task_round` 조각은 spec-150 **§5.5**(조각 라이브러리, :208). spec-152 개정 노트는 6건이지만 **실제 계약 개정은 8회**(07-18 triage, 07-21 T-071 두 건이 무기록).

### A-1. 렌즈 1 — 슬랙 연동

**계약 요약**: outbound 3콜(declare 승인 실행: 채널 생성→초대→`[완료]` control 게시) + inbound 1건(`[완료]` 클릭→thread read→회고 초안)이 전부. **알림(push) 계약은 존재하지 않는다.** 채널명 `incident-{label}-{yyyymmdd-HHmm}` KST. 출처: spec-152:1152-1185(§T-1/T-2)·:143-148·:315·:1595-1597·:1704.

낡음/공백:
1. **메시지 형식 전면 미정의** — spec-152:1161 은 `"control 문안"` 한 단어. 실제 값(`action_id=incident_complete`, Block Kit)은 **work-074:166 완료 증거에만 존재** — 구현 로그가 유일한 SoT
2. **`POST /{run_id}/slack/complete` 는 죽은 경로** — API 표(:315)에 등재됐으나 미신설, 실경로는 `/slack/interact` block_actions 분기(work-074:438 ④)
3. "채널 또는 스레드" 미결정 서술 잔존(:769·:141) — 채널 생성으로 확정됐는데 §A-1/§U-1 미갱신
4. 와이어프레임 채널명 `#inc-api-5xx`(:109) 규칙 위반 잔재
5. declare proposal 의 "Slack 채널 계획" 소유 서술(:68) vs "채널명은 preview 에 안 담김"(:696) 정면 모순
6. **알림 부재 = 최대 실질 구멍** — Task 배정·거부·게이트 방치 전부 무알림. 거부 DM "v1 제외"(:1334), 게이트 방치 에스컬레이션 OQ-2 미정(:1861) → **결재 카드가 인박스에 무기한 무알림 대기 가능**

**spec-119 와의 관계**: sources 에 형식 인용만, 본문 참조 0건. 도메인도 다름(decision 원장). 단 재사용 자산 有 — `users.slack_id` SoT, 메시지 최소 계약(트리거 한 줄+제목+딥링크), 본인 억제·멱등 가드레일, 실패 1회 로그. 봇 scope 에 **`im:write` 없음**(spec-119:170). spec-119 §8 AC 는 "합의 진행 중" 미고정.

### A-2. 렌즈 2 — 슬랙으로 작업 생성

**결론: 계약 부재.** 진입점은 `POST /incidents/raise` 1개(:308-312, source = dev_button/error_webhook — Slack 축 없음). Task 생성은 승인 실행 fanout 2개뿐.

관련 자산:
- 채팅 진입 표면(공용층, spec-150:278) — incident 는 composition 없음(7파일, :245). **붙이는 비용 = 등록 1줄 + composition 1파일**(계약상)
- 슬래시 커맨드 선례: spec-051 `/gm` → `POST /api/v1/slack/commands` 라우터·서명검증 인프라 기존재
- 봇 멘션 선례: spec-111 `app_mention` → 폼 → 등록
- **inbox 원형에는 있었으나 승격 때 탈락한 축 2개**: Trigger 로서의 Slack mention(Canonical Model.md:33,98) · Review Surface projection 으로서의 Slack block(:89,124 — 승인 카드를 Slack 에 띄우는 축). 탈락 근거 문서 없음
- `source` 확장은 OQ-10 이 이미 열어둠 → `source=slack_command` 추가는 계약 파괴 없이 가능
- §Placement(:90) "구성원의 이슈라이징 발화" — raw-error-trigger 전환 후 미갱신. **문서 제목 "이슈라이징 기반" 자체가 구모델**

### A-3. 렌즈 3 — 후속 테스크 생성

**계약 요약**: 생성 주체 = 서버(승인 실행), AI 는 후보만.
| 경로 | 게이트 | 산출 | round |
|---|---|---|---|
| 1차 예방 | `review.finalize` [승인] — action_items **전량** | TK-2 `prevention.task.execute` | 1 |
| 후속 | `feedback.approve` [재발행] — follow_up_candidates **전량** | TK-3 `prevention.task.follow_up` | 원장 최대+1 |
| 추적 | `declare` [승인] | TK-1 `incident.response_tracking` | 0 |

`checked` 선별 폐지(제외하려면 [피드백] 재생성만). 담당자 resolver 4단(원본→is_lead→commander→approve actor). 초기 `accept_pending`(TK-1 만 즉시 in_progress). 출처: spec-152:1278-1389·:784-870·:1187-1233·:1054-1118·:1391-1413.

낡음/모순:
1. **`checked` 가 SVC-2 에만 생존**(:1036 예시·:1060 필드표) — SVC-3 은 폐지 단정(:1118). T-079 "완전 동형" 선언과 모순
2. payload 의 `task_type` 유령 키(:1037·:1094) — AI 가 정하나 서버가 정하나 미정의
3. TK-3 계보 이중 정의 — spec-152 "지름길 FK 없음"(:1389) vs work-074:106 `parent_task_id·feedback_action_id` 연결(구모델)
4. **`is_required` 잔재** — SPEC 은 제거, work-074 C1 landed 컬럼에 존재, C15(제거 마이그레이션) TODO → **DB 에는 아직 있음**
5. "열린 예방 Task 0" 단순화(:1708) vs `canceled` 조건부 terminal(:1325·:1524) — 판정 규칙 2벌
6. `scope_slug` PATCH 교정 미배선(:460 명시)

### A-4. 렌즈 4 — 후속 테스크 피드백

**계약 요약**: round 종결 → provider agentic 후속안(실패 시 최소 리뷰 fallback, Action 필수 생성) → `feedback.review` v1 + `feedback.approve` 카드 → CTA [재발행]/[피드백]/[완료]. [피드백] = `/feedback/regenerate` → 카드 `revision_requested` → 백그라운드 델타 재생성 → 같은 Subject version+1 + Action 재상정. 동시성 = 카드 상태 + 409. finalize 와 완전 동형(T-079). 출처: :172-185·:275-292·:821-870·:1066-1118·:1209-1243·:1391-1432.

T-079 상태: SPEC 확정·BE(C17)/FE(C18) DONE(라이브 E2E run 완주) — 단 **work-074 체크박스 미체크·죽은 에러코드(`FEEDBACK_REGENERATING` 422) 인용 잔존**.

낡음/모순:
1. **§Action.status 절(:1480-1511)이 현행 모델과 정면 충돌** — `revision_requested`=보완요청·`needs_revision` FSM 잔존. [보완 요청]은 T-079 가 폐지, 세 게이트 read-only 라 `needs_revision` 도달 불가 (죽은 FSM 이 SPEC 본문에)
2. feedback Subject 개수 모델 애매 — round 별 새 Subject v1 vs "항상 같은 Subject"(:78·:870) 스코프 구분 문구 없음
3. `feedback_requested` TaskEvent 의 귀속 Task 미정의(run 축 사건을 Task 에 매닮)
4. **TaskEvent 목록 2벌** — 계약 12종(:1419-1432) vs 제안 18종(:1812-1831), 어느 쪽이 계약인지 무답
5. spec-153 Timeline 은 3종만 인용 — 콘솔 렌더 미정의

### A-5. 렌즈 5 — 루프 구조

**계약 요약**: Subject 3종(declare.proposal/review.document/feedback.review) + gate 3종. 2층 상태(Action FSM 고정 / WorkflowRun 스테이지 선언, spec-150:163-170). 조각 분해: `ai_draft`×3 + `regen_gate`×3 + `task_round`×1 + `execution`(대기)×1. task_round 는 **판정만** — fanout 은 승인 실행 소유. 라운드: [재발행]→`tasks_in_progress`, round=원장 최대+1 / 전부 terminal→feedback 생성 / [완료]+열린 Task·Action 0→done.

불일치 전수:
- **A. 스테이지 수 3벌**: 5(spec-150:177·spec-152 OQ-7·work-074/078) vs **8**(spec-150:50 — 같은 문서 내 자기모순) vs 7파일(:245). 코드 실측 = 5 stages+11 edges(work-078:158)
- **B. `finalize_pending → done` 전이 누락(심각)**: R6 가 `complete_without_tasks` 를 착지 경로로 승격했는데 전이표(:1445)·done 진입조건(:1448)·전이규칙(:1465)·자동전이표(:1543)·Lifecycle(:1657)·**done 4조건(:1681 — ③④를 원리적으로 만족 불가)** 6곳 전부 미반영
- C. FE "완료 v2 비활성" 구서술 잔존(work-074:47·:290·:355)
- D. Subject 생성 시점 3벌 서술(:68 "직후" vs :221 등 "조사 완료 후"=확정)
- E. `review_draft` 유령 상태 — 같은 실행 안에서 즉시 통과, WP-078 실측 "미사용"
- F. 어휘 완전성 OQ 종결이 두 문서에서 다름 + 전이 수 불일치(16 vs 7+2+2+5)
- G. `stages` 저장 위치 — 코드 상수(INCIDENT_GRAPH)로 확정(work-078:121)됐으나 spec-152 미환류
- H. `failed` 복귀 전이 비대칭 — `finalize_pending`/`feedback_pending` 복귀 불가(:1450) vs 실패표 "유지"(:1555)

### A-6. 렌즈 6 — 완료처리

**정본 경로**: 마지막 round 전부 terminal → 후속안 → [완료](`no_follow_up`) → 열린 Task/Action 0 확인 → `done` + TaskEvent `workflow_closed`. 부수: finalize [완료](`complete_without_tasks`). 거절: declare reject → `rejected`.

T-063(회고 직접 발행 폐기→inbox 결재 부활) 상태: SPEC 확정 정본. **BE C13·FE C14 는 WP 상 TODO(미착수)** — 07-27 코드 대조로 착지 개연성 높으나 **문서로는 판정 불가. 재정비 착수 시 최우선 확인 항목.**

낡음/공백:
1. done 조건 ③④ vs `complete_without_tasks` 모순(위 B)
2. `workflow_closed` 가 TaskEvent — 귀속 Task 미정의 + Task 0 개 경로에선 남길 곳 없음
3. `workflow_closure_requested` 는 제안 목록에만 존재
4. `FEEDBACK_REQUIRED`(409) vs `TASK_ROUND_NOT_COMPLETE`(422) 발화 지점·역할 중복 미정의
5. `rejected` 이후 정리·재발 시 재개 계약 없음
6. `failed` run 을 사람이 닫는 경로 없음(콘솔은 retry/reconcile 만, 강제 종결 금지)
7. 회고 확정본 영속화(파일 export) 미결(:1705)

### A-7. 죽은 경로 전수 (D-1~D-27)

| # | 죽은 계약 | 폐기 근거 | 잔존 위치 |
|---|---|---|---|
| D-1 | `POST /review/revise` | T-063 | work-074 다수 |
| D-2 | `POST /review/publish` | T-063 | work-074 |
| D-3 | `POST /feedback/{sid}/revise` ([보완 요청]) | T-079 | work-074 |
| D-4 | `follow_up_candidates[].checked` | T-079 | work-074 |
| D-5 | `action_items[].checked` | T-063 | **spec-152:1036·:1060 본문 잔존** |
| D-6 | `REVIEW_/FEEDBACK_REGENERATING` 422 잠금 | R6 ① | work-074 8곳 |
| D-7 | `REVIEW_DOCUMENT_NOT_EDITABLE` | T-063 | work-074 |
| D-8 | `INCIDENT_TRIAGE_IN_PROGRESS`(A안) | B안 채택 | work-074 |
| D-9 | `INCIDENT_NOT_FOUND` 통합코드 | RUN/TASK 분리 | work-074 |
| D-10 | `TOOL_APPROVAL_REQUIRED` 403 | 감사 이벤트 강등 | work-074 |
| D-11 | `ADMIN_WORKFLOW_FORBIDDEN` 계열 | canonical collapse | spec-153·work-074 |
| D-12 | 구 finalize Action 경로(`/review/finalize-request`) | T-053/T-063 | work-074 (코드 잔존 별건) |
| D-13 | `POST /slack/complete` | 미신설 | **spec-152:315 API 표** |
| D-14 | `trigger_type=manual_incident` | source 축 통일 | **spec-153:258·:573**·work-074 |
| D-15 | Trigger 입력 title/severity 등 | raw event 모델 | work-074 |
| D-16 | tasks 조상 지름길 FK 4종 | 07-27 원장 원칙 | work-074 C1 landed 컬럼 |
| D-17 | `tasks.is_required` | T-071 | work-074 (DB 에 잔존, C15 TODO) |
| D-18 | `tasks.department`(loose) | T-071→scope_slug | work-074 |
| D-19 | 보완요청 FSM(`needs_revision`) | read-only 3게이트 | **spec-152:1487-1509 본문** |
| D-20 | declare [질문]/[수정] 두 갈래 | 단일 재조사 통합 | work-074 |
| D-21 | `/declare/revise` | 직접 편집 소멸 | work-074 |
| D-22 | 등록 폼 IncidentRaiseModal | dev 원클릭 | work-074 |
| D-23 | 채널 vs 스레드 택일 | 채널 확정 | spec-152:141·:769 |
| D-24 | `#inc-api-5xx` 채널명 | 규칙 확정 | spec-152:109 |
| D-25 | Subject 표 "Slack 채널 계획·risks" | SVC-1 부재 | spec-152:68 |
| D-26 | `result_note`/`evidence_url` | comment 통합 | work-074(제거 TODO) |
| D-27 | position 기반 gatekeeper | is_lead 이관 | work-074 |

### A-8. 미착수 설계 부채(주요)

- **§U-7 태스크 상세 2컬럼**(C12 TODO) · `comment` TaskEvent+상세 API(C11 TODO — 단 SPEC 은 landed 처럼 서술) · T-063 정합 C13/C14 TODO · `scope_slug`/`is_required` drop 마이그레이션 C15 TODO · 칸반 뱃지 C16 TODO
- 게이트 방치 에스컬레이션(OQ-2 미정 — 만료 없음만 확정) · **실전 error event 스키마(OQ-10 — incident 실전화 최대 미결)** · 회고 확정본 export 미결 · 전역 Runtime Registry endpoint 부재 · GitHub/Jira mirror(OQ-1/5 후속)

### A-9. 개정 이력 감사 (R1~R6 + 무기록 2회)

- R1(07-15 DRAFT) 모델 전환 — "Subject 2개" 서술이 현행 3종과 불일치, "이슈라이징" 제목·§Placement 잔존
- 무기록(07-18): AI 이슈조사단 + raw event 모델 — 헤더 이력 없음
- R2(07-20, T-051~056): provider 능동 탐색·[피드백] 루프·§U-7 신설
- R3(07-20, T-063): inbox 결재 부활 — [완료] v2 비활성 서술은 R6 가 뒤집었는데 상태머신 미반영
- 무기록(07-21, T-071): scope_slug·is_required 폐기 — **계약 파괴 변경인데 개정 노트 없음**
- R4(07-21, T-079): 피드백 finalize 동형화
- R5(07-23, WP-077): Definition-Driven Dispatch(표현 정합)
- R6(07-27, 코드 대조): **반영 누락 다수** — Action.status 절·complete_without_tasks 6곳·/slack/complete·:68 Subject 표·SVC-2 checked
- version 0.0.2 무변경(5회 계약 개정에도) · work-074 frontmatter 07-23 정지 · 재번호(150→152)로 git 이력 갈림

### A-10. 재정비 시 문서 관점 주의

1. **SoT 재선언이 선행** — spec-152/work-074/spec-153/spec-150 넷이 계약을 나눠 갖고 셋이 stale
2. spec-152 내부 화석 3절(§Action.status·§Task DB 제안·§TaskEvent 제안)이 초안 잔재 — 재정비 1순위 삭제/정리 대상
3. "개정 = 추가 + 구 서술 grep 삭제" 절차 강제 — 같은 계약이 3~4곳 다른 버전으로 존재하는 패턴 6회 반복됨
4. 개정 이력 = 실제 커밋 1:1 강제 (무기록 개정 2회)
5. **Slack 이 계약 사각지대** — incident Slack 계약을 spec-152 내부 절로 세울지, spec-119 를 워크플로 공통 알림 계약으로 승격할지 결정 필요
6. **work-074 는 사실상 폐기 — 신규 WP 로 갈아엎을 것** (죽은 계약 인용 20건+, DONE/TODO 표기 뒤엉킴)
7. 조각 관점 재서술 권고 — §A-1/A-2/A-3 등 게이트 3벌 중복 서술을 "조각 계약 1벌 + 파라미터 표"로 접으면 문서 절반 + 동형성 위반 구조적 차단
8. inbox 원형의 탈락 축 2개(Slack mention 트리거·Slack block 결재 카드) — 렌즈 1·2 재정비 전에 탈락 사유 확인(문서에 없음)

---

## §B. app 코드 조사 (레포: mediness-app) — 2026-08-31 완료

incident 도메인 = 7파일 패키지 `back/app/services/action_runtime/workflow/incident/`(const 220 · declaration 216 · definitions 358 · workflow 1132 · provider 410 · surface 442 · __init__ 54). 엔진·조각·태스크 기계는 공용층, incident 는 선언+콜러블 주입만.

### B-1. 렌즈 1 — 슬랙 실제 연결

**실물**: 클라이언트 1종 `SlackBotClient`(httpx + xoxb bot token, `slack_bot_client.py:35-81`, 429/5xx 3회 재시도). 설정 키 2개 — `slack_decision_bot_token` / `slack_decision_signing_secret`(config.py:375-376, **decision 이름을 incident 가 빌려 씀**). `slack_notifications_enabled` 는 WBS 스케줄러 전용 — incident 슬랙 kill switch 없음. 필요 scope: `channels:manage`·`channels:history`·`chat:write`·`conversations.invite`.

호출 지점 전수: ① declare 승인 execute → 채널 생성→초대→control 게시(definitions.py:164-262, 멱등 스텝 실행기 tools/steps.py) ② 회고 transcript 읽기(workflow.py:736-762, 실패 시 degrade+audit) ③ `[완료]` 인바운드(routers/slack.py:402-436, 서명검증 有) ④ **별도 HTTP 완료 수신구**(`POST /incidents/slack/complete`, action_runtime_v2.py:797-829).

**메시지 형식 조립은 `tools/slack.py:92-107` `_control_blocks()` 한 곳** — section+button(`action_id="incident_complete"`), 문안 `INCIDENT_CONTROL_MESSAGE`(const.py:150). 채널명 `incident-{slug|service}-{yyyymmdd-HHmm KST}`(definitions.py:191-199).

🔴 냄새:
1. **토큰 미설정 = 조용한 no-op** — `definitions.py:167-170`: 바인딩 None 이면 채널 생성 skip, audit 0, execution 은 DONE 으로 성공 처리 → run 은 `responding` 전진
2. **그리고 그 run 은 영원히 못 나온다** — `response` 출구는 `EV_SLACK_COMPLETE` 단 하나(declaration.py:73), 채널→run 역주행이 유일 발화 경로, `ExecutionStage` 에 on_timeout 없어 sweeper 사각. 웹 완료 버튼 없음(front 호출 0건). **슬랙 미연결이면 incident 100% responding 에서 사망**
3. 완료 수신구 2벌 — `/slack/interact`(서명검증) vs `/incidents/slack/complete`(**인증·서명 둘 다 없음**, 방어는 assignee 검사 하나)
4. `slack_id` 없는 초대 대상 조용히 드롭(감사 없음)
5. tool 설명 "제안서 요약 게시"는 코드 없음(control 1통뿐)

### B-2. 렌즈 2 — 슬랙으로 작업 생성

인바운드 3종(`/slack/events`·`/interact`·`/commands`)은 **전부 decision 도메인 착지**. incident 인바운드는 `[완료]` 분기 1개(생성 아님, 전진). **incident 생성 경로는 코드상 FE dev 버튼 1개**(task-kanban.tsx:205 → `/api/ax/incidents/raise`). 모니터링 웹훅 배선 없음. `DomainSpec`(incident/__init__.py:51-54)은 capability_leaves·chat_starter 등 미선언 → 채팅·MCP 시작 불가. MCP incident 툴 9종 전부 read-only.

### B-3. 렌즈 3 — 후속 테스크 생성

fanout 2곳 + 추적 1곳, 전부 승인 execute 소유:
| 라운드 | 트리거 | 위치 | type | 초기 상태 |
|---|---|---|---|---|
| 0 | declare 승인 | definitions.py:115-173 | `incident.response_tracking` | **IN_PROGRESS** |
| 1 | finalize 승인 | definitions.py:82-107 | `prevention.task.execute` | **ACCEPT_PENDING** |
| 2+ | feedback [재발행] | definitions.py:289-312 | `prevention.task.follow_up` | **ACCEPT_PENDING** |

후보: round1 = 회고 `action_items` 전량 / round2+ = `follow_up_candidates`(선별은 LLM 프롬프트 소유, provider.py:369-380). round 산식 = 원장 최대+1(definitions.py:303). 담당자 사다리 = AI→제품 대표→대응 총괄(workflow.py:479-492·:967-986). 공용 fanout `tasks/factory.py:202-245`.

🔴 `follow_up_task_created` 이벤트 **부존재**(grep 0) — 관측은 일반 `task_created` payload 뿐. 종결 판정 동개념 3벌 구현(렌즈 5).

### B-4. 렌즈 4 — 후속 테스크 피드백

**`feedback_requested` 이벤트 부존재**(grep 0). 구현된 "피드백"은 전부 **카드(안)에 대한 AI 재생성 루프** — 이벤트 리터럴 `"feedback"` 하나를 3게이트 공유: `accept_regen_feedback`(runs_surface.py:97-121, 중복 409) → `RegenGate.on_event`(카드 REVISION_REQUESTED + 백그라운드 재생성 발주) → 성공 시 SubjectVersion v+1 + 카드 재상정 / 실패 시 복원. 델타 재생성 예산 12→6턴. `triage/retry` 는 빈 피드백으로 같은 기계 재사용.

🔴 ① **태스크에 대한 피드백은 없음** — 태스크에 남길 수 있는 건 `comment` TaskEvent 뿐(다음 라운드 근거로 harvest) ② **`RegenGate.on_event` 가 이벤트 이름을 안 읽음**(regen_gate.py:88-105) — 어떤 이벤트든 재생성 접수 처리 ③ 폐지 이벤트 상수 12종 잔재(const.py:57-77)

### B-5. 렌즈 5 — 루프 구조

**실물 = 8 스테이지 · 11 엣지**(declaration.py:68-177): triage→declare→response→draft→finalize→prevention→fb_draft→feedback. 루프는 feedback `[재발행]`→prevention 하나. round 카운터는 원장 파생(loop() 미사용). gate 3종 전부 `gate_policy="incident_commander"` + **`ExpiryPolicy(kind="none")` 무기한**. 무한루프 방지 = Signal 연쇄 상한 16.

🔴 최심각 구간:
1. **라운드 종결 판정 3벌, 모수 다름** — `round_piece.py:52-60`(최대 round만) / `tasks_surface.py:340-347`(전 라운드) / `factory.py:180-191`(전 라운드). 엄격한 쪽이 이벤트 발사를 게이팅하고 느슨한 쪽이 판정하는 역전 2단 — 이전 라운드에 비terminal 1건 남으면 **루프 영구 정지**
2. **거절 태스크 1건이 run 전체를 영구 정지** — 거절해도 `accept_pending` 유지 = 비terminal, 취소 버튼은 UI 미노출. → **수락/거절 폐기 결정이 이 버그를 자동 해소 (재설계 최대 수혜)**
3. **태스크 완료 표면 4개 중 1개만 워크플로 전진** — `PATCH /incidents/{run}/tasks/{id}` 만 runner 전달. canonical transition·`/task-completions`·MCP `task_done` 은 round 평가 없음 → 채팅/MCP 완료는 워크플로를 못 깨움
4. `notify_event` 가 스테이지·이름 안 가림 — feedback 대기 중 `task_done` 도착 시 카드 재생성 발주 가능(우연히 게이팅에 막힘)
5. `response`·`prevention` on_timeout 없음 — sweeper 사각 2곳
6. 게이트 무기한 → 만료 sweep 0건 + 알림 0 (인박스 무기한 무알림 방치 가능)

### B-6. 렌즈 6 — 완료처리

종결 경로 3개: declare [거절]→`rejected` / finalize [완료](`complete_without_tasks`)→`done` / feedback [완료](`no_follow_up`)→`done`. feedback [완료] 사전조건 = decision 필수 + 열린 예방 task 0(422) + 열린 Action 0(409). 종결 = `Runner._land` → `set_run_status`(**run 상태 유일 쓰기 경로**, runtime.py:220-225).

🔴 ① **`workflow_closed` 부존재** — run-레벨 감사 이벤트 0(주석으로 유보 명시) ② 태스크 일괄 정리 없음 — `complete_without_tasks` 는 열린 task 검사조차 안 함, **round 0 tracking task 는 어느 경로에서도 정리 안 됨** ③ 종결 후 재개 불가(amendments 빈, notify_event→409), incident run 삭제 endpoint 도 없음 ④ `STATUS_FAILED` 도달 불가(엣지 없음)

### B-7. 죽은 코드 전수

- **도달 불가 BFF 3건**(호출자 0, BE 404 어서션 테스트 有): `front/app/api/ax/incidents/[run_id]/review/{revise,publish,finalize-request}/route.ts`
- 미사용 상수: `STATUS_FAILED` · `ERR/EV_ASSIGNEE_RESOLUTION_FAILED` · 도메인 이벤트 상수 12종(실제 audit 은 regen_gate 4종 하드코딩) · `ERR_ACTION_STALE_PLAN_VERSION` · `META_DECLARE_SUBJECT_ID` · ON_TIMEOUT 엣지 0 · `loop()` 미사용 · reconcile 미구현 · 고아 pyc(`actions/__pycache__/slack_channel...pyc`)
- **스펙에 있고 코드에 없는 이벤트 3종**: `workflow_closed` · `follow_up_task_created` · `feedback_requested` (레포 전체 grep 0)

### B-8. TaskEvent 실발생 (정의는 11종 — 스펙 "12종"과 불일치)

발생 ✅: task_created/started/accepted/completed/declined/assigned/comment. ⚠ 기계만 지원·표면 도달 불가: task_blocked(incident UI 버튼 없음)·task_canceled(발화 지점 0). ❌: task_edited(체크리스트·수동 전용)·task_deleted(incident 전용 삭제 없음).

### B-9. task 재설계 결정과의 충돌 (C1~C15)

`accept_pending 제거·수락/거절 폐기·전부 todo 생성·명시 시작` 결정 기준:
- C1/C2/C15: fanout·수동 생성 `ACCEPT_PENDING` → `TODO` (definitions.py:105·:310, tasks_surface.py:437·457)
- C3/C4: 생성 이벤트 분기 통일 + tracking 즉시 IN_PROGRESS 폐기 — 단 Slack [완료]가 `todo→done` 을 요구하게 되는데 **전이표에 TODO→DONE 없음** → 전이표 확장 or 합성 전이 필요
- C5/C9/C13: decline 기계·incident decline endpoint·MCP task_decline 제거 (의존 표면 3곳)
- C6/C7: reassign 리셋 → TODO, 전이표 accept_pending 행 삭제 + `_STATUS_EVENT`/`_STAMP` 재정의
- **C8: 거절 영구 정지 버그 자동 해소 — 최대 수혜**
- C10/C11: FE accept_pending 렌더·수락 버튼·거절 모달·declined 파생 삭제
- C12: WBS 축(`version_wbs_status.py` 등)과 enum 동시 변경 조율
- C14: decision `notify_task_declined` DM 폐기

### B-10. 테스트 자산

engine_v2 단위: test_incident_declaration(1195)·test_incident_surface(1791, Slack 3단 멱등 포함)·test_incident_background·test_task_round·fanout/Slack 골든 스냅샷 2종 등. API: wp102 gate e2e·assignable_users·**finalize_restore(폐지 3라우트 404 어서션)**. MCP: incident read-only 9종.
**미커버**: 실 Slack 왕복 · `/incidents/slack/complete` 인증 부재 · 다중 라운드 시나리오 · 완료 표면별 round 전진 · responding 무한 대기.

### B-11. 재정비 시 코드 관점 주의 (요지)

1. **웹 대응 완료 버튼 결정이 첫 결정** — 슬랙 미연결 시 전 run 사망. 엣지 1개 + surface 1개면 열림
2. 라운드 종결 판정 3벌 → 1벌 수렴(정본 선언 선행)
3. round 평가를 전이 seam(`lifecycle.apply_user_transition`) 안쪽으로 — 완료 표면 4개 모두 워크플로를 깨우게
4. `RegenGate.on_event` 이벤트 이름 가드
5. run-레벨 감사 도입 시 `set_run_status` 한 자리만 고치면 전 도메인 적용
6. 게이트 무기한 → 만료 or 알림 결정 필요
7. **incident 는 결재 후처리 훅 미등록**(`_POST_APPROVE_BY_TYPE` 에 decision 만) — 슬랙 DM 은 decision `notify.py` 규율 승계 + 훅 1줄이 최단 경로
8. `/incidents/slack/complete` 인증 구멍 — `/slack/interact` 만 남기고 닫기
9. round 0 tracking task 종결 정리 설계 필요("전부 todo 생성" 적용 시 영원히 todo 잔존 위험)
10. 폐지 BFF 3건·참조 0 상수 12종 안전 삭제 가능

---

## §C. 문서 ↔ 코드 대조 + 재정비 쟁점 (코디 종합)

| # | 항목 | 문서 | 코드 | 판정 |
|---|---|---|---|---|
| 1 | 스테이지 수 | 5(§5.2·OQ-7) vs 8(spec-150:50) 자기모순 | **8 스테이지·11 엣지** | 코드가 정본, 문서 양쪽 다 정정 |
| 2 | 이벤트 3종(workflow_closed·follow_up_task_created·feedback_requested) | 계약에 존재 | **구현체 0** | 스펙 유령 — 도입할지 삭제할지 결정 |
| 3 | TaskEvent 개수 | 계약 12종 + 제안 18종 2벌 | 정의 11종 | 3벌 → 1벌 확정 필요 |
| 4 | Slack 형식 | 미정의("control 문안") | `_control_blocks()` 실물 | 코드 실물을 계약으로 승격 |
| 5 | `/slack/complete` | API 표 등재 | 미신설(+무인증 변형 존재) | 죽은 계약 삭제 + 인증 구멍 폐쇄 |
| 6 | T-063/C13·C14 | WP 상 TODO | 폐지 3라우트 404 어서션 테스트 존재 = **착지됨** | WP-074 기록 불신 확정 |
| 7 | 수락 게이트 | B축 철학의 축 | 거절 영구 정지 버그의 원인 | 폐기 결정이 양쪽 다 해소 |

### 재정비 쟁점 (사용자와 확정할 것)

1. **웹 대응 완료 버튼** — Slack 미연결 대비 `response` 탈출구를 웹에도 낼 것인가 (권고: 낸다)
2. **Slack 실전 연결 범위** — 토큰 미설정 no-op 을 fail-loud 로 바꿀 것인가 / incident 전용 설정 키·kill switch 분리 / `im:write` scope 추가(알림용)
3. **알림 설계** — incident 결재 후처리 훅 등록 + 게이트 방치 에스컬레이션(만료 vs 알림) — 현재 무기한·무알림
4. **슬랙 인바운드 생성** — `source=slack_command` 확장(계약상 열려 있음) 이번 범위에 넣을지
5. **라운드 판정 정본** — 3벌 중 어느 정의로 수렴할지 (활성 라운드만 vs 전 라운드)
6. **round 평가 위치** — 전이 seam 안쪽으로 내려 완료 표면 4개 전부 전진 가능하게
7. **run-레벨 감사(`workflow_closed`) 도입 여부** + 종결 시 태스크(특히 round 0 tracking) 정리 정책
8. **스펙 재작성 방식** — spec-152 대수술 vs 조각 계약 1벌+파라미터 표로 재서술(문서 관점 권고안), WP-074 는 신규 WP 로 교체

