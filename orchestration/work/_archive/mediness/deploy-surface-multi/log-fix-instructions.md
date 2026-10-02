# [planner · micro] log.md 5차 행에 `wp-add` 결합

**WP-131 통과다.** 코디가 직접 검증했다 — `lint --strict` 0 error/263, `doc_no 254` 전역 유일(1건), AC 16건 ↔ Phase 대응 구멍 0, Spec Coverage·Status Board·WP List 3표 등재 확인.

**네가 보고한 「lint 264 → 263」도 네 해석이 맞다.** WARN 은 「늘어난 계약을 받을 원장이 없다」는 **대리 신호**였고, WP-131 이 covering 에 들어가면서 그 신호가 요구하던 원장이 실제로 생겼다. 대리물이 본체로 바뀐 것이라 **옳은 소멸**이다. 되돌리지 않는다 — 네 권고대로다.

**§Rollback 이 이 WP 에서 제일 잘 쓴 절이다.** 「같은 (제품,환경)에 2행이 생긴 뒤 = point of no return」을 표로 가르고, down 첫머리에 중복 그룹 검사를 넣어 **조용히 실패하지 않게** 한 것, 부분 revert 두 조합을 ⛔ 로 금지한 것 — 되돌릴 수 없는 지점을 아는 게 그 절의 일이라는 걸 정확히 했다.

## 이번 판 — 딱 한 줄

네가 미결로 넘긴 `log.md` **wp-add entry** 를 닫는다. **안 넣은 건 네 판단이 옳았다** — 내가 WP 지시서에서 「`log.md` 를 고치지 마라」라고 못 박았다. 범위를 지킨 것이고, 규약 확인은 코디 몫이었다.

확인 결과 **넣는 게 맞다**:

- `rules/document-pipeline.md:330` — `종류` enum 에 **`wp-add`** 가 있다.
- `:331` — 「복합 변경 시 `종류` 콤마 결합 가능 (예: `wp-add, spec-change`)」.
- 선례 — `log.md` `2026-08-31 | wp-add, spec-change | MEDINESS-WP-128, …` (WP 신설을 이 방식으로 기록했다).

### 할 것

`products/mediness/log.md` 의 **2026-09-22 행 하나만** 고친다:

1. `종류` → **`spec-change, open-resolve, wp-add`**
2. `문서` 칸에 **`MEDINESS-WP-131`** 추가 (기존 `MEDINESS-SPEC-051` 뒤에)
3. `요약` 본문 끝에 **한 문장만** 덧붙여라 — 실행 원장이 WP-131 이라는 것 + Harness v1 예외라는 것. 예: 「실행 원장은 [WP-131](30-work/work-131-deploy-surface-axis.md)(7 Phase·BE+FE) — Harness v1 상 신규 실행은 Delivery Issue 이나 SPEC 과 동시 리뷰를 위해 사용자 판단으로 WP 로 만든 예외다.」 **기존 요약 본문은 한 글자도 고치지 마라.**

### 하지 말 것

- **다른 행·다른 파일을 건드리지 마라.** `spec-051`·`21-html`·`30-work.md`·`work-131` 전부 확정됐다.
- 요약 본문 재작성 금지 — **덧붙이기만.**
- 커밋·push·PR 금지.

### 검증

- `python3 scripts/lint-pipeline.py --strict` → **0 error / 263 warning 유지**(늘면 그게 문제다).
- 선례 행(`2026-08-31` WP-128)과 **표기 형태가 같은지** 눈으로 대조해라.

### 리포트

`planner-report.md` 에 「7차 — log wp-add」 절로 두세 줄. 끝나면 §9 완료 보고 두 채널. **코디handle 은 preamble 값을 믿어라 — 이 세션에서 세 번 바뀌었다.**
