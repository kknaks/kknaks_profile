# [reviewer_code] 0.6 app 코드 검수

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-review-code-app-brief.md`(폴더 /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev)의 역할 · 제약(read-only · 공개 레포 규칙 · 실호출 금지 · .env 열지 마라 · 18105 · 18220 은 코디 것 — GET 은 됨) · 완료 보고 그대로(핸들은 preamble 값). **디스크 여유 2~3GB.**

검수 워크트리: /Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev (미커밋 — 이번 판은 WORK-009 구현분 · 앞 판 /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/review-code-v052-app.md).

읽을 것: /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/WORK-009-v06.md · /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/SPEC-002-chat-eval.md(0.6.0 · §3-7) · /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/review-work-v06.md · /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/_RESUME.md §2 맨 위 네 행(코디 결정 W-1~W-7 · B-1~B-3 · 사용자 U-5~U-9) · 보고 /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/impl-v06-app-report.md.

볼 것: ① WP 마다 완료 조건 · 결정 반영(특히 W-1 B-3 · W-2 표지 자리 · W-4 lineup 안 가림 · W-7 VP 뒤 상세 · U-9 BR6) ② **일반 규칙인지** — 문항 번호 · 코드 · 이름으로 갈라지는 가지 0 ③ 원칙: 빠짐없이 · 묻지 않은 것 안 붙임(KD9 · KD10 · BR6 이 asked_only 를 키우는 꼴) · LLM 에는 필요한 칸만(이름 목록 FT8 이 입력을 얼마나 늘리나 — 수로) · **앱이 답 문장을 짓지 않음**(answer_check 는 기록만) ④ 동결 3 파일(answer_key.py · walk/calls.py · walk/keycodes.py)이 고칠 것을 남기면 **FAIL 로 적지 말고 「동결 파일 — 고치면 키 다시」** 로 표시 ⑤ B 와 키가 같은 함수(BR5 · 갈래) ⑥ ruff · pytest 1회 ⑦ 커밋 후보 grep ⑧ 「사용자가 실물에서 만날 자리」(Q03 B 가 비교 질문을 거절한 답 — 보고서 §4) — 원인이 프롬프트인지 재료인지.

산출: /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/review-code-v06-app.md 1개 · 판정 PASS/WARN/FAIL.
