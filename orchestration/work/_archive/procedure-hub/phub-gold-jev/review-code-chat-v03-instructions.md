# [reviewer_code] 상담 0.3 코드 검수(WORK-014)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-review-code-app-brief.md`(폴더 /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev)의 역할 · 제약(read-only · 실호출 금지 · .env 열지 마라 · 18105 · 18222 GET 만 · 질문 보내기 금지) · 완료 보고 그대로(핸들은 preamble 값). Procedure Hub 데이터 · medikit 공개.

검수 워크트리: /Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev (HEAD 68a31b1 위 미커밋). 얼굴 SVG · face_coords 는 대상 아님(바뀌었는지만).

읽을 것: /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/SPEC-006-consult-v03.md · /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/WORK-014-consult-v03.md · /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/review-spec-006.md · /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/review-work-014.md · /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/impl-chat-v03-instructions.md · 보고 /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/impl-chat-v03-report.md · SPEC-001 0.7.2(앱이 읽는 칸) · /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/_RESUME.md §2 11-17 맨 위 행들.

볼 것: ① A1~A8 계약(턴 종류 · talk 은 검색 재료 안 씀 · system_v3 금지 낱말 · close 하나 · empty(안전 종류는 「확인된 정보 없음」) · 리스트 계열→시술 · 메뉴 시술 아님 · 「○○ 계열 시술」 · 점 누적 · 누르기 · viewing 한 턴 · 드로어 · 객체 패널 env) ② 0.7.2 칸(descended · sites · site_applied · site_prefer)을 묶음마다 맞게 읽나 ③ 함께 쓰는 코드(front +18 · col_b +3)가 시험 앱 동작을 안 바꾸나 · 고친 기존 시험 5개가 결정된 예외인가 ④ **실측에서 본 것 판단**: 턴 종류 오판 2(「지방이 두꺼운 느낌이야」 → follow · 「볼이 처져서요」 → new) · **「지방 주사」 줄임 후보 Noul 0.58 이 문턱 아래라 입구 없음** — 사용자가 처음 지적한 꼴이 여전히 안 잡힌다 — 문턱 · 지시문 어디를 고치면 되는지 근거와 제안 ⑤ 시험은 바뀐 파일 관련만 · ruff ⑥ 커밋 후보 grep ⑦ 「사용자가 실물에서 만날 자리」(18222 GET).

산출: /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/review-code-chat-v03.md 1개 · PASS/WARN/FAIL.
