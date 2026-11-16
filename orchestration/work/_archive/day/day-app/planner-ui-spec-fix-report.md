# planner-ui-spec-fix 결과 보고 — WARN 2건 최소 정정

## 상태: done (커밋 · push 없음 · 앞 교정 diff 위에 미커밋으로 추가)

## 수정 위치 (`products/day/20-spec/spec-003-mobile-app.md` 하나만 · `20-spec.md` 추가 변경 없음)

| 지적 | 위치 | 고친 것 |
|---|---|---|
| W1 | U-3 카드 3행(`:183`) | 「기타 제공 정보」 기본 표시 = 2026-11-09 판 카드가 싣던 `gender` 로 두되 **planner 해석 · 사용자 미정**이라고 적고 OQ-A27 로 연결. 「새 칸(예: `isNew`)」 사실오류 → 「2026-11-09 판 카드에 싣지 않던 서버 칸(예: `isNew` — 스냅샷에 이미 있음)」 |
| W1 | §5 UI 선택 표 OQ-A27(`:747`) 신규 | 3행에 실을 서버 값 — 기본 `gender` 만 · `isNew` 싣지 않음 · 사용자 확인 · 확정 4행 구조 그대로 |
| W2 | U-6(`:238-239`) | 「받아들일지는 서버가 정한다」 문장 삭제 → 사실 bullet: 원장 A 가 B 지정 호출을 본인 수락하면 **현 서버는 받아 A 의 수락으로 남긴다**(dev `board.py:603-605` 는 원장 목록 여부만 검사) · 11/09 판 기본 선택이 걸렀던 단계가 없어짐 · 기본 = 사용자 확정 즉시 본인 수락 유지 · 차단 정책 · API 추가 없음 · 버튼 노출은 OQ-A28 |
| W2 | 케이스 매트릭스(`:538`) 행 추가 | 「원장 A 가 원장 B 지정 호출을 본인 수락 → **성공** · 성공 토스트 「{방} 수락」 · 노출 여부 OQ-A28」 — 거절 전제 제거 |
| W2 | §5 UI 선택 표 OQ-A28(`:748`) 신규 | 다른 원장 지정 호출에서 원장 버튼을 그대로 보일지 — 기본 그대로 · 즉시 본인 수락 · 후속 확인점(승인 게이트 아님) |

새 카드 항목 · 문구 · 정책 · API · 승인 단계를 만들지 않았다. 사실 근거는 CENTURION_DAY day-app `backend/day/services/board.py:603-605`(read-only 재확인) · `board_rules.py:496` `isNew`.

## 검증

- `git diff --check` → 통과
- `python3 scripts/lint-pipeline.py --strict` 1회 → exit 0 · **0 error, 263 warning** · `products/day/` 해당 0건
- `git status --short` → `M products/day/20-spec.md` · `M products/day/20-spec/spec-003-mobile-app.md` 두 개(앞 교정 포함)

## 남은 확인점

- OQ-A27(카드 3행 기타 값) · OQ-A28(다른 원장 지정 호출 버튼 노출) — 사용자 확인 대상. 그 밖 OQ-A21 · OQ-A8 등은 앞 보고서 그대로.
- log.md · WP · 코드 후속은 앞 보고서(`planner-ui-spec-report.md`) 「미결 6」 그대로.
