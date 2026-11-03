# WP-10 F1~F3 코드 재검수

- 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 현 미커밋 코드, `wp10-code-review.md` F1~F3와 `wp10-review-defects-fix-report.md`를 대조한다. `tests/phase8/test_wp10_review_defects.py` 22개는 코디 직접 PASS, 워커 전체 390 tests PASS 보고.
- 읽기 전용으로 의미 반전·인용 절 부재/무공백 문장 경계, 공유 role/family의 `(node,id,owner)` 수신/검증/전달 provenance, 다른 anchor/순서와 부위 불일치, 팔자 하드코딩 제거를 재현하고 PASS/WARN/FAIL한다. 기존 공개 안전/지원 갈래 부분 답/동적 page 회귀를 보호하는지 확인한다.
- F1은 독립 의미 모델 대신 원문 전체만 승인하는 보수적 경로다. 이를 자연스러운 임상 의역 검증으로 과장하지 말고, 실제 사용자 답이 단순 원문 덤프로 퇴행하는 제한을 별도로 적는다. 안전 차단 결함과 표현 품질 제한을 구분한다. 새 범위를 확장하지 말고 중대한 잔여 재현만 지적한다.
- 코드·DB·서비스·새 provider/judge/batch 수정/호출 금지. `reference/2026-10-30-hub-evals/build-out/wp10-code-rereview.md`에 판정·재현을 쓰고 Orca worker_done 보고.
