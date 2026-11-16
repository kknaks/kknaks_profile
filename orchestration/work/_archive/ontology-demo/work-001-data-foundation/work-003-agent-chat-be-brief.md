
# [backend] WORK-003 에이전트 루프 + 채팅 API (P1~P4, 게이트 4·5)

너는 **ontology-demo `backend` 워커**다. WORK-002 에 이어 같은 워크트리. FE 는 `app/front/` — 너는 `app/ontology-agent/`(+로컬 검증용 compose 실행)만. git 조작 금지.

## 1. SSOT (read-only 절대경로)

- `/Users/kknaks/orca/workspaces/kknaks_profile/docs-baseline/para/projects/summer-star/ontology-demo/30-work/work-003-agent-loop-and-chat.md` ← P1~P4 SoT
- 같은 폴더 `../20-spec/spec-005-agent-loop-and-gates.md`(v0.0.4 — 루프 3단계·답변 객체(used_edges·excluded_edges·citations·drilldown·followups·premise_correction·unknowns)·정량 추정 금지·게이트 4·5·회귀 3본 실측 단언) · `spec-003-api-and-chat-contract.md`(v0.0.8 — 채팅 5 엔드포인트·2초 폴딩·error_code(AI_TIMEOUT/AI_FAILED)·180초·1,000자·CONVERSATION_BUSY)
- **조사 리포트**: `/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/orchestration/work/docs-baseline/research-codex-mcp-report.md` — §2(open-kknaks 결선)·§3(MCP 연동)·§4(소비·폴딩)·§5.4(가져올 패턴)·§5.5(달라질 것 8건)·§5.6(착수 전 5건). 모범 코드 `app/back/service/chat/`(read-only)

## 2. 계약 — 코디 확정값

- **함정 2건 필수 반영**: 툴 허용은 per-tool `approval_mode=approve`(`approval_policy=never` 는 실패 처리) · `features.apps=false` 명시.
- 큐/키: queue=`ontology`(제출·워커·compose 3곳 일치), mcp_server_key 2곳 일치 — env(`ONTOLOGY_` prefix)로 SoT 단일화. 모델·effort 조합은 조사 리포트 §5.6 의 mediness 실측 조합을 따르고, 리포트에 없으면 gpt-5.6-terra + 기본 effort 로 두고 보고.
- **S-001**: 시스템 프롬프트에 관계·도메인 지식 금지 — 도구 사용 지침·응답 스키마 지시만. mediness 프롬프트 조립기 이식 금지.
- **구조화 답변**: LLM 출력 → SPEC-005 답변 객체 파싱·검증 단계(스키마 위반 시 SPEC-005 의 처리 — 재시도/실패). `used_edges ⊆ 확정(채택·자동 확정·선언)` 을 서버가 검증(위반 시 실패 처리 — 게이트 5).
- steps 기록 주체 = 백엔드(스트림 tool_use/tool_result 폴딩). 세션은 WORK-002 서명쿠키 그대로. error_code 필수.
- 로컬 검증 인프라: `app/back` compose 의 redis 재사용 + open-kknaks codex 워커(queue=ontology 분리 기동 — Dockerfile.worker 파라미터화 재사용). 비번 등 env 는 임시값.

## 3. 게이트 (완료 증거)

- **게이트 4 — 회귀 3본**: R-1(노쇼율 현황 — 5.3/4.8/5.2/5.0% 횡보) · R-2(8월 매출 전제 교정 — 3.69억 +27%, 내원 5,428→4,196·예약 9,057→6,852) · R-3(드릴다운 — 8월 취소 원본 20건 마스킹 행). pytest 자동화(LLM 호출 포함 — 스키마·수치·전제 교정 존재를 단언, 문구 완전일치 아님).
- **게이트 5 — 근거 무결성**: 답변 수치 = DB 재조회 일치 · used_edges ⊆ 확정 · citations 역추적 가능. 검증 코드로.

## 4. 하지 말 것 — 화면(FE)·배포 구성(WORK-005) 금지 · LLM SDK 직접 import 금지(ADR-04) · PII·git 조작 금지 · spec 어긋나면 질문.

## 5. 검증 — `uv run pytest -q <네 테스트만>` + 실기동 1회(redis+codex 워커+API 로 R-1 라이브 1회 — 통과하면 반복 금지).

## 6. 완료 보고 — 2채널 (preamble 값, 코디 term_45e793be-0adb-44c7-9d9a-eb35c4f48320), subject "backend 완료: WORK-003", body: phase·게이트 4/5 수치·모델 조합·미결. phase 마다 [진행] 1줄.
