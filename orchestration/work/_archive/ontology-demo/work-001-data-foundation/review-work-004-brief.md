
# [reviewer_code] WORK-004 프론트 3페이지 검수

너는 **reviewer 워커**다 (read-only). 대상: 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/work-001-data-foundation` 의 **`app/front/` 미추적 신규 + middleware.ts 만** (app/ontology-agent 는 WORK-002 진행 중 — 범위 제외).

## 기준 (위반 = FAIL, 파일:줄 근거)

1. 역할 규칙: `orchestration/roles/ontology-demo/frontend/rules.md` — globals.css·기존 파일 수정 0(diff 로 실증) · 파생 카운트 하드코딩 금지(시안 숫자 리터럴 grep) · PII(원값·언마스킹 UI·폐기 표기 19**) · 미니그래프 금지 · 스트리밍 금지(2초 폴링) · 토큰 컨테이너 스코프(--ont-* 밖 전역 오염)
2. spec 준수: SPEC-004 v0.1.0 U-1~U-15·AC 23·파생 표 / SPEC-003 shape(mock 픽스처가 계약과 일치하는지 — lib/ontology 픽스처 vs spec JSON 예시 대조) / SPEC-001 마스킹 표기·enum
3. mock/실API 스위치가 lib/ontology/client.ts 한 곳인지 · middleware matcher 가 /ontology 한정인지
4. 코디 승인된 예외 4건(TopNav CSS 가림·woff2 커밋·has_prev_period 후속·빈 컬럼 사유)은 위반 아님

코디 재검증 참고: tsc 0 · build 성공(라우트 5) · matcher 확인됨.

## 산출물 — `/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/orchestration/work/work-001-data-foundation/review-work-004-report.md` 1개. 판정 PASS/WARN/FAIL.

## 완료 보고 — 2채널 (preamble 값, 코디 term_45e793be-0adb-44c7-9d9a-eb35c4f48320), subject "review 완료: WORK-004".
