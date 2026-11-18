# WORK 검수 지시서 — WORK-013 0.2(허브 · SPEC-001 0.7.2)

**너는 앞 판의 맥락이 없다.** `work-review-instructions.md`(같은 폴더)의 역할 · 볼 것 · 제약 · 완료 보고 꼴 그대로(핸들은 preamble 값). Procedure Hub 데이터 · medikit 공개. 외부 호출 금지. 같은 폴더에서 다른 검수 워커가 다른 WORK 를 본다 — 네 리포트 외에는 손대지 마라.

읽을 것: `WORK-013-hub-v07.md` · 계약 `SPEC-001-hub-gold-mcp.md 0.7.2 · SPEC-003-hub-gold-db.md` · 앞 검수 `review-spec-001-v07.md · review-spec-001-v071.md` · `_RESUME.md` §2 11-17 맨 위 행들(**시험은 그 WP 파일만 · 전체 pytest 금지** · 규칙 0.7.2 · U7 (a) · SPEC-006 코디 값 · W-9 (a) · W-10 「○○ 계열 시술」 · U6-1~3 · U6-4 보류 · 0.7.2 코디 확인) · 코드(/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev HEAD daa54e3 읽기만).

볼 것: ① SPEC ↔ WP 대응(미대응 0) · 지어낸 동작 0 · 결정 반영 ② 실행 가능성(경로 · 기존 시험 기대 바뀌는 자리 전수 · 함께 쓰는 코드 범위) ③ **WP 마다 돌릴 시험 파일이 정해졌고 전체 pytest 가 없는가** ④ 실물 확인이 실물을 요구 ⑤ CSV 판 = DB 판 응답 같음(DT10 표본 prefer · filter 짝) · B-1~B-3 에 코디 답이 필요한지 · 0.7.2 판정이 WP-3 에 맞게 들었나 ⑥ 공개 grep.

산출: `review-work-013.md` 1개 · PASS/WARN/FAIL · FAIL 없으면 「구현 진행 가능」.
