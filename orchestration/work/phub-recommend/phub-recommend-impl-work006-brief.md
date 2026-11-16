# 발주서 — WORK-006 구현(실험 앱 · SPEC-006 v2.1 0.3.1)

## 정본
`SPEC-006.md`(0.3.1 · §3-4 case3 Jev 재귀 탐색 · §3-4-2 peek 꼴 = SPEC-005 §5-16 · §3-5 전달 보장 (a) 설정 · §3-6 intent · §3-7 공정성 · §4 기록 칸 · §4-4 검증 스크립트 · §7-6 끝 조건) · `WORK-006.md`(WP-0~5 · Scope 29파일 · 순서 의존) · 보충 `phub-recommend-jev-walk-addendum.md` · 검수 `review-spec006-v2.1-report.md`(PASS 상당). 둘이 다르면 SPEC. 허브 쪽 계약 = `SPEC-005.md`(0.3.3) §5-0-2(meta · intent 문구) · §5-16(T10 peek · T11 expand).

## 순서(허브 WORK-007 이 병렬로 진행 중 — 의존 없는 WP 먼저)
1. **지금**: WP-2 intent(프롬프트 한 줄 + 의도 표 12 · intent_passed · intent_values 기록) · WP-4 verify_runs(결정론 검증 스크립트 · rerun-v3 기준선 = fail-triage2 숫자: 잘림 100/614 · intent 14/662 · C 18) · 기록 칸(delivered_bytes · truncated · stray · walk) · 모의 허브(fake_hub)에 peek/expand 를 SPEC-005 §5-16 꼴로 미리 넣어 WP-3 시험 준비
2. **허브가 peek/expand 를 발행하고 코디가 18005 를 재시작한 뒤**(코디가 「허브 준비」 보냄): WP-3 case3 Jev 걷기(걸음 ≤4 · peek → Choice 「펼칠 것」 + Noul 「충분」 ≥ 0.5 · expand · 멈춤 4종 · 되돌아가기 = 지금 경로 1회 · trace.walk · 단계 이름) · WP-0 확인 시험(실물 1회씩 · 한도 일부러 작게 → 마커 확정 → TRUNCATION_MARKERS 상수 · 문턱 실측값) · WP-1 전달 보장(자식 env · Codex 플래그 · 허브 meta 는 허브 몫)
3. 시험 · ruff · 18210 재시작 · worker_done(끝 조건 표: 잘림 0 · intent ≥95% · stray 0 · 결정론 · 기존 시험). WP-5 182 재실행은 코디가 따로 발주.

## 제약
공개 레포: 키 · 원장 · 골드 · runs · 사용자 홈 경로 커밋 금지 · 로컬 커밋 · push 금지 · 허브 18005 손대지 말 것 · 실물 CLI 호출은 WP-0 확인 시험(각 1회)만 · 사용자 포트 · procedure-* 컨테이너 손대지 않음 · 추측으로 메우지 않기(막히면 ask).
