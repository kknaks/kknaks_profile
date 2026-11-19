# planner — 삭제 로그 되돌림 (사용자 2026-11-19)

사용자: 「로그는 다른 데서 남긴다 — 삭제 로그를 남길 필요 없다.」 `spec-2-delete-log.md` 의 **로그 부분을 되돌린다.**

- 남긴다: 「삭제는 소프트 딜리트(`deleted_at`)만 — 동기화 · 환불 등 어떤 경로든 물리 삭제 금지」. 사라짐은 기존대로 `deleted_at` + `external_ref` 원천 표시.
- 뺀다: `event_log` `record.delete` · `record.restore` · payload 표 · 관련 OQ-76 · 77(번호를 비우지 말고 다음 OQ 번호를 당기거나 「없앰」 표시 — 이 SPEC 관례대로) · SPEC-000 `event_log` 설명에 더한 값이 있으면 그것도.
- lint 다시 · `spec-sync-report.md` 에 「삭제 로그 되돌림」 한 줄.
- 끝나면: orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --text "[worker_done] planner 삭제 로그 되돌림 완료 — <한 줄>" --enter
