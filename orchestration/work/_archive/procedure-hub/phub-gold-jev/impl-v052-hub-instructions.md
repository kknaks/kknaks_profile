# [backend] 허브 구현 — WORK-007(SPEC-001 0.5.2)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-be-brief.md`(같은 폴더) 전체를 읽어라 — 역할 · SSOT · allowed_paths(`backend/`) · 제약 · §8 검증 · §9 완료 보고 그대로(핸들은 preamble 값). 워크트리 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(앞 판 미커밋 위에 이어서).

**이번 일 = `WORK-007-hub-v052.md`(같은 폴더) WP-1 ~ WP-5 전부.** 계약 = `SPEC-001-hub-gold-mcp.md` 0.5.2. `_RESUME.md` §2 맨 위 행들(U-3 · U-4 = 추천) 반영.

검수 `review-work-v052.md` 의 허브 WARN 둘을 이렇게 닫아라:
- **H-1**: 완료 조건 3 에 한 줄 더 — 「제품의 하위 제품을 거치는 길 한 건에서 `layer.depth` ≥ 2 · `layer.via[]` 의 마지막이 그 제품」 을 실물에서 확인해 보고.
- **H-2**: 「가장 긴 길 4 단」 은 `g_scope` 하위 행을 직접 이은 **그래프 셈**(= 4)으로만 단언하고, 응답의 `layer.depth` 최댓값은 **세어 보고만**(HG2-3 가장 얕은 길 — 2 로 예상 · 시험에 박지 마라).

- 확인 서버는 **18106** — WP-5 끝에 띄워 **둔다**(앱 워커가 그걸로 답 키를 다시 뽑는다). 18105 는 코디 것(건드리지 마라).
- **WP-5 에서 18106 을 띄우면 완료 보고 전에 코디에게 한 줄**: `[진행] backend: 0.5.2 허브 18106 준비`(§9 의 (2) 방식).
- 기준선: 데이터 env 전체 pytest 598 passed · 2 skipped 를 깨지 마라(응답이 넓어져 기대값이 바뀌는 시험은 SPEC 근거와 함께 고치고 목록 보고).
