# WP-10 잔여 F1 최종 코드 검수

- 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 읽기 전용. `wp10-code-rereview.md` 잔여 F1과 `wp10-heading-bypass-fix-report.md`를 대조한다. 고정 UI allowlist 변경과 신규 66개 직접/보정/fake 전체 경로 회귀가 대상이며 코디도 66개 PASS 확인했다. F2/F3와 공개 안전·공유 provenance·동적 page의 PASS 범위를 보존했는지 확인한다.
- 제목/도입/질문에 붙인 근거 없는 효과·위험 부정·임신 조건·수치·부재 주장이 직접 검사와 보정 후 최종 답에서 우회하는 잔여 경로가 있는지 재현한다. 신규 기능/범위를 넓히지 말고 P1/P2 실재 결함만 구체적으로 보고한다. 원문 전체만 승인하는 표현 품질 한계는 별도 WARN으로 명시한다.
- 코드·DB·서비스·provider/judge/실물 batch 수정/호출 금지. `reference/2026-10-30-hub-evals/build-out/wp10-final-code-review.md`에 PASS/WARN/FAIL와 실행 증거를 쓰고 Orca worker_done 보고.
