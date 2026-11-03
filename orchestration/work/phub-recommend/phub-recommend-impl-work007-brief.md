# 발주서 — WORK-007 구현(허브 · SPEC-005 v3.2.1 0.3.3)

## 정본
`SPEC-005.md`(0.3.3 · §3-0 W5-D · §4-3 F-D′ F-F · §5-0-1 다이어트 A1-1~A1-9 · §5-0-2 meta · intent 문구 · §5-13 C′ · §5-14′ · §5-16 T10 peek · T11 expand · §6-5 끝 조건 (i)~(vii) · §6-6 걸음 도달 · §7 V · §8 B 186 표) · `WORK-007.md`(WP-0~5 · depends_on · 순서 의존 · Scope 표 — 79행 F-D′ 는 §4-3 consult_copy 7 이 맞음 · 패치 중) · 검수 `review-spec005-v3.2.1-report.md`(PASS 상당). 둘이 다르면 SPEC.
배경: `build-out/fail-triage2.md` · `recheck/` · 2차 replay2.json 676 · `backend/build-out/work005-report.md`.

## 할 일 = WORK-007 WP-0 → WP-5 순서
- WP-0 기준선 · recheck2(2차 replay 676 · 판정 식 같게 · not-closed-why 행 단위 재셈) 먼저
- 다이어트(A1-1~A1-9 · 도구별 상한 · claude_contract.priority/use_first · sections_index) → 동봉 C′ 규칙 → F-F 섹션 매핑 24(행마다 시험) · F-D′ 7 → **T10 peek · T11 expand**(새 도구 2 · intent? 받되 무시 · neighbors_by_kind · 설정 이름 7) → MCP 도구 14 meta `anthropic/maxResultSizeChars` + intent 설명 상수 → 빌드 발행
- WP 마다 그 WP 시험만 · 전체는 마지막
- REST · MCP 같은 코어 · 허브에 LLM 없음 · 결정론

## 끝 조건(= SPEC §6-5 (i)~(vii))
(i) 재실행 676 recheck2 — 조항 닿는 행 161 의 ≥90% (ii) 크기: case3 경로 중앙 ≤20KB · p95 ≤60KB · 도구별 상한 표 (iii) C3 5/5 + Q003 반대 조건 (iv) 품질 6/6 · 106/106 · 회귀 0 (v) peek ≤2KB 중앙 · expand 상한 (vi) 걸음 ≤4 BFS 도달 비율(§6-6) (vii) 결정론 · 시험 · ruff. 산출 `build-out/recheck2/` · `backend/build-out/work007-report.md`(WP 별 · SPEC 과 달라진 점 · 미닫힘 행 이유).
끝 조건 미달이면 멈추고 ask(수치 · 손잡이) — 추측으로 상한을 바꾸지 않음.

## 서버
새 빌드 발행 뒤 ask 「재시작 요청」 → 코디가 18005 재시작(현재 커밋 · 깨끗한 트리) → base-url 재측정 → worker_done. DB 55434 그대로 · alembic 리비전 됨.

## 제약
로컬 커밋(push 금지) · 원장 · 실버 · 골드 데이터 · 키 커밋 금지 · 실버 · 시맨틱 수정 금지 · 앱(clinic_chat) 수정 금지 · 사용자 포트 · procedure-* 컨테이너 손대지 않음 · 추측으로 메우지 않기(막히면 ask).
