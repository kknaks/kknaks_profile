# 발주서 — WORK-005 구현(허브 · SPEC-005 v3.1 0.3.1)

## 정본
`orchestration/work/phub-recommend/SPEC-005.md`(0.3.1 · §4-3 F-A~F-E · §5-13 동봉 · §5-14 의도→섹션 · §5-15 slim 승격 · §5-6 checks 펼침 · §6-5 끝 조건) · `WORK-005.md`(WP-0 ~ WP-7 · 코드 표면 표 · Done Criteria). 둘이 다르면 SPEC. 검수 `review-spec005-v3.1-report.md`(PASS 조건 반영됨).
배경 숫자: `reference/2026-10-30-hub-evals/build-out/fail-triage.md`(B 239 · 분모 205 · 조항이 닿는 행 186 · 닫지 않는 행 19) · `fail-triage-scripts/`(triage.py · replay.py 읽기만 · import 금지).

## 할 일 = WORK-005 WP-0 → WP-7 순서 그대로
- WP-0 **먼저**: 기준선 — 지금 떠 있는 18005(e9d30ace) 에 읽기 호출로 `replay.json` 을 만들고 `recheck.py`(판정 식 = triage 와 같은 식 · 320행 재분류 동일성 시험) 를 완성한 뒤에야 코드 변경.
- WP-1 fact 재부착 · 새 fact(F-A~F-E) · WP-2 섹션 매핑 · WP-3 `intent` 입력 · 의도→섹션 기본 묶음 · WP-4 의도별 고정 동봉 · WP-5 쌍 · 비교 · WP-6 check_conditions family/product 펼침 · WP-7 빌드 발행 · 재인용 측정 · 크기 · 품질 · 전체 검증.
- WP 마다 그 WP 시험만 · 전체(`make verify` 급)는 WP-7 에서 한 번.
- MCP 도구 스키마에도 `intent`(선택 · 의도 코드 I-01~I-12) 노출 — REST · MCP 같은 코어.

## 끝 조건(= SPEC §6-5 · WORK Done Criteria)
B 재인용률 — 조항이 닿는 행 186 중 ≥ 90%(168+) · 전체 205 기준 비율도 보고 · 오류 15 → 0 · 응답 크기 도구별 중앙 ≤ 2× (recommend ≤ 14.4KB) · 품질 6/6 · 106/106 · 회귀 0 · 결정론(두 번 같음) · 시험 전부 · ruff. 산출 `reference/2026-10-30-hub-evals/build-out/recheck/recheck-report.md`(+json · 두 export 해시 머리에) · `build-out/work005-report.md`(WP 별 결과 · SPEC 과 달라진 점 · 닫지 못한 행과 이유).

## 서버
- 코드 다 되면 골드 재빌드 · **18005 는 코디가 재시작한다**(끝났다고 보고 → 코디 재시작 → 재인용 측정은 새 서버로). WP-7 측정 전 코디에게 ask 로 「재시작 요청」.
- DB 55434(phub-graph-postgres) 그대로 · 새 alembic 리비전은 됨.

## 제약
커밋은 로컬(push 금지) · 원장 · 실버 · 골드 데이터 · 키 커밋 금지 · 사용자 포트 · procedure-* 컨테이너 손대지 않음 · 실버 · 시맨틱 파일 수정 금지(골드 빌드 규칙만) · 앱(clinic_chat) 수정 금지 · 추측으로 메우지 않기(막히면 ask). 끝나면 worker_done(끝 조건 표 + 보고서 경로).
