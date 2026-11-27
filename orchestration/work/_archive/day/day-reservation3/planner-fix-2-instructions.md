# [planner] SPEC-008 고침 2 — 검수 2차 FAIL 1 · WARN 3

맥락: `review-doc-2-report.md`(이 폴더 · N1 ~ N4 파일:줄). 같은 워크트리 · allowed_paths 그대로. 아래 = **코디 기본값 11-26** — 「코디 결정 11-26」으로 적는다.

- **N1 → ⓐ** 「확인 대기」(`pending_version_id`)는 묶음이 **확인될 때까지 유지**(실패해도). 풀리는 길 = 확인 · 또는 병원이 실패를 **접음**(웹 동작 하나 — 문구 비움 · OQ-Q04). 대기 중(실패 포함)에는 1차 W1 · W2 규칙 그대로(E3 · 자동 닫힘 · 생성 · 수정 · 취소 409 / 링키 `cancel` = 예약 있음으로 봄). spec-000:677 · 다시 시도 경로(407) 409 조건 · Rule 에 같은 말.
- **N2** U-5 표에 줄 더함: ① 실패 묶음 있음 → [다시 시도] · [접음]만 ② 접은 뒤 예약 없음 ∧ 답할 버전 `change` → `new` 로 보고 [예약 생성](F1 과 같게) ③ 접은 뒤 예약 없음 ∧ 답할 버전 `cancel` → 버튼 없음 · 스레드 「닫힘」 ④ W3 확인 · W18 실패 → ①.
- **N3** 기준 하나: `visit_id` 있음(지금 그 예약이 취소돼도) → `request_finished` · 없음 → `request_not_applied`. 상태 표 · E2 · Rule 3 · 케이스 표 모두 이 말로.
- **N4** [예약 수정] = **W4 한 본문에 최상위 `reservationMemo`(합친 글) · `funnel` 같이**(items 있으니 지금 `write_open` 갈래 그대로 · 비교 없이 늘 보냄). SPEC-007 고침 6 과 같은 말. OQ-Q02 실물 확인 대상 = 이 모양.

lint `--strict` products/day ERROR 0. 완료 보고 = 1판 브리프 §9 두 명령 · subject `planner 완료: SPEC-008 고침 2`.
