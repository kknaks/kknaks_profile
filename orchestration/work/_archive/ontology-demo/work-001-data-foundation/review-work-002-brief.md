
# [reviewer_code] WORK-002 도구·API 검수

너는 **reviewer 워커**다 (read-only). 대상: 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/work-001-data-foundation` 의 `app/ontology-agent/` **미커밋 변경분**(WORK-002 — service/·tools/·api/ 신설 + 기존 수정. app/front 는 커밋됨·범위 제외).

## 기준 (위반 = FAIL, 파일:줄 근거)

1. 역할 규칙(roles/ontology-demo/backend/rules.md): S-001(관계 지식 상수 0) · S-002(파라미터화 조회만·자유 SQL 0·상한 초과 거부) · PII(응답·로그 원값 0, 마스킹 뷰 경유만) · ADR-04(LLM SDK import 0 — 이 WP 에 LLM 없음 확인)
2. spec 준수: SPEC-002 v0.0.4(도구 4종 시그니처·에러·빈 status 계약·reason/note 분리) · SPEC-003 v0.0.8(엔드포인트·게이트 401/INVALID_PASSWORD·has_prev_period·source_group·columns_note·edge_id·lag_days·sign U+2212)
3. **AC-8 정적 게이트의 실효성** — 워커가 두 번 조인 검사(lookahead 되감기·\b)가 실제로 우회를 막는지. 파일 whitelist 로 덮은 곳이 없는지.
4. 구조 결정 1건 평가: 연구 권고(B: MCP→내부 API 래퍼) 대신 공용 service/ 계층 — AC-5 구조 성립 주장 타당성.
5. build_meta(503)·서명쿠키 세션(비번 파생 키) 설계의 구멍.

코디 재검증: 실데이터 222 passed.

## 산출물 — `/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/orchestration/work/work-001-data-foundation/review-work-002-report.md` 1개. 판정 PASS/WARN/FAIL.

## 완료 보고 — 2채널 (preamble 값, 코디 term_45e793be-0adb-44c7-9d9a-eb35c4f48320), subject "review 완료: WORK-002".
