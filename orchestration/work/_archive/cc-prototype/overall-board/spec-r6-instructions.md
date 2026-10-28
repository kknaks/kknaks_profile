# planner r6 — review-doc-r4 반영 + WP-KOS 결과

1. `review-doc-r4.md` F1 · W1 ~ W6 **전부** 반영(리뷰 「고칠 것」 그대로). W3 = **게이트는 OQ-529 · OQ-530 만** 본다 — OQ-528(ETCETERA 호출 · 완료)은 게이트에서 빼고 WP-E2E 전까지 따로 확인(K5 는 사용자가 KOS 에 시트팩을 붙이면 진행).
2. **WP-KOS 중간 결과**(`kos-undo-probe-report.md`): OQ-529 받음 — `complete:false` 200 · `DONE → READY` · 22초 뒤에도 `READY` / OQ-530 받음 — `change-flow-step PROCEDURE → PROCEDURE_WAITING` 200. → OQ-529 · OQ-530 **닫음**(받음), §5.13 [종료] 되돌리기 직후 즉시 값 `READY` 확정(근거 = 리포트). WORK-006 게이트 행 「통과(10-26)」 · WP-KOS 「K1 ~ K4 완료 · K5 대기」.
3. SPEC-003 0.5.0 → 0.5.1 (`(r6)`) · 부록에 「r4 처분」. 끝나면 §9 두 채널.
