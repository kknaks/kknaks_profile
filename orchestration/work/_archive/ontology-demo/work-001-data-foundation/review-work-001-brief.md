
# [reviewer_code] WORK-001 코드 검수 — 데이터 기반 (P1~P5)

너는 **reviewer 워커**다 (read-only). 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/orchestration/roles/kknaks-dev/reviewer/role.md`
리뷰는 read-only — 코드를 고치지 않고 테스트도 돌리지 않는다(코디가 이미 실데이터 81 passed 확인).

## 대상

워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/work-001-data-foundation`
범위 산정: `git diff origin/ontology-demo...HEAD` + untracked (`app/ontology-agent/` 23파일).

## 기준 (위반 = FAIL, 근거는 파일:줄)

1. **역할 규칙**: `roles/ontology-demo/backend/rules.md` — S-001(관계 지식을 코드 상수·프롬프트에 넣지 않음) · S-002(파라미터화 조회만·DB read-only 소비) · PII(로그·픽스처·리포트에 원값 0) · **이식 원칙**(변환 규칙 재해석 없음 — reference/ontology_demo/scripts/ 원본과 대조, read-only)
2. **spec 준수**: `/Users/kknaks/orca/workspaces/kknaks_profile/docs-baseline/para/projects/summer-star/ontology-demo/20-spec/spec-001-data-layer-contract.md` (v0.0.4) — 테이블·뷰 이름, enum, 마스킹 표기, 게이트 코드
3. allowed_paths(`app/ontology-agent/`) 밖 변경 0 · DB·원천 미커밋 · 하드코딩 경로/값 없음(config env 경유)
4. 코드 품질: 기존 컨벤션(app/back 패턴) 준수 · 게이트가 실제로 막는 구조인지(우회 가능 경로)

## 산출물 — 이 파일 1개만

`/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/orchestration/work/work-001-data-foundation/review-work-001-report.md`
형식: 판정 PASS/WARN/FAIL + 위반 목록(파일:줄+근거 규칙) + 워커 보고 미결 3건(AC-8 이월·promo v2 id 참조·부분 월 플래그)에 대한 의견.

## 완료 보고 — 2채널 (preamble 값, 코디 term_45e793be-0adb-44c7-9d9a-eb35c4f48320)

subject "review 완료: WORK-001", body 판정+위반 수.
