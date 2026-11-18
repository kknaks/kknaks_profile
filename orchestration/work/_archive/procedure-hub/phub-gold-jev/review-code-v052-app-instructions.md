# [reviewer_code] 0.5.2 app 코드 검수

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-review-code-app-brief.md`(폴더 /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev)의 역할 · 제약(read-only · 공개 레포 규칙 · 실호출 금지 · .env 열지 마라 · 18105 · 18106 · 18220 은 코디 것 — 띄우거나 내리지 마라 · GET 은 됨) · 완료 보고 그대로(핸들은 preamble 값). 문서는 전부 /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev 에 있다. **디스크 여유가 2.7GB 뿐이다 — 큰 파일을 만들지 마라.**

검수 워크트리: /Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev (미커밋 — 이번 판은 WORK-008-app-v052.md 구현분 + 앞 판 app-key-fix1 · 앞 판 v05 검수 /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/review-code-v05-app.md).

읽을 것: /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/WORK-008-app-v052.md · /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/SPEC-002-chat-eval.md(0.5.2) · /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/review-work-v052.md(A-1~A-4) · /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/impl-v052-app-instructions.md · 보고 /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/app-v052-report.md · /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/app-key-fix1-report.md · /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/_RESUME.md §2 맨 위 행들(B-1 · U-1 · U-2 · 답 키 검토).

볼 것: ① WP 마다 완료 조건 · A-1~A-4 ② 키: 키 전용 기준 대상을 B · C 에 안 줌 · expected_kinds_by_entry 를 따라야 하는 곳 전부 따름 · (나)/(다) 대조가 재현되나(바이트 같음) ③ end_state counted_rows 를 HG1 표지로 넓힌 것이 SPEC (가) 와 부딪치나 ④ 보고서 미결 F2(볼 주름 묶음 2 — Jev 가 주름 + 부위 볼 을 남겨 HG1·HG3 겹친 좁은 조회) · F3(Q12 B 후보 소진 — adverse 대상 required 0) 의 원인을 코드에서 짚고 고칠 방향 제안(고치지 마라) ⑤ 원칙(빠짐없이 · LLM 에는 필요한 칸만 · 행 안 뺌) · 안전 강제 첨부 0 ⑥ ruff · pytest 1회 ⑦ 커밋 후보 grep(키 · 회사 데이터 · 홈 경로).

산출: /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/review-code-v052-app.md 1개 · 판정 PASS/WARN/FAIL.
