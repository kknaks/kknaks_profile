
# [reviewer_code] WORK-003 에이전트·채팅 검수

너는 **reviewer 워커**다 (read-only). 대상: 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/work-001-data-foundation` 의 미커밋 변경분 — `app/ontology-agent/agent/`·`api/chat_router.py`·`config.py`·`main.py`·테스트 4파일 + **`app/back/docker-compose.yml`(+42/-0 — 코디 승인된 추가, 기존 서비스 무변경 검증만)**.

## 기준 (위반 = FAIL, 파일:줄 근거)

1. **S-001** — prompt.py 에 관계·도메인 지식 0건(도구·계층 사용 규칙만 허용 — 워커가 추가한 2규칙이 경계 안인지 판단). ADR-04(LLM SDK import 0, open-kknaks 경유만).
2. **게이트 5 검증기 구조** — answer.py 가 used_edges ⊆ 확정·citations 재조회 일치·정량 추정 차단을 정말 구조로 강제하는지(우회 경로: 검증기 스킵 분기·예외 삼킴·부분 검증).
3. **codex 제출 안전** — approval_mode per-tool 4줄(서버 기본 아님)·features.apps=false·shell/web_search off·sandbox read-only 가 테스트로 고정돼 있는지.
4. SPEC-003 채팅 계약(5 엔드포인트·폴딩·error_code·180초·BUSY·1000자) · SPEC-005 답변 객체 필드 전건.
5. 채팅 DB 분리(ontology_chat.db)가 온톨로지 DB read-only 를 깨지 않는지 · PII(args_summary 값 미포함 포함).
6. compose: 기존 worker·chat-worker diff 0 실증.

코디 검증: 364 passed/5 skipped 재현. 라이브 게이트 4·5 는 워커 실측 수치 인정(재실행 불요).

## 산출물 — `/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/orchestration/work/work-001-data-foundation/review-work-003-report.md` 1개. 판정 PASS/WARN/FAIL.

## 완료 보고 — 2채널 (preamble 값, 코디 term_45e793be-0adb-44c7-9d9a-eb35c4f48320), subject "review 완료: WORK-003".
