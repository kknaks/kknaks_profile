# [reviewer_code] 앱 재검수 1 (짧게)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-review-code-app-brief.md`(같은 폴더)의 역할 · 제약(read-only · 공개 레포 · 실호출 금지 · 허브 18105 띄우거나 내리지 마라) · 완료 보고 그대로. 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`.

읽을 것: `review-code-app.md`(1차 · FAIL 1 · WARN 8) · `app-fix1-instructions.md` · `_RESUME.md` §2 맨 위 「앱 검수 뒤」 행.

할 것(좁게): ① F-1 · W-1 ~ W-8 · Q10 · Q25 닫힘 표(파일:줄) ② 원칙 grep — 폭이 줄어드는 자리 0 · 묻지 않은 안전 붙이는 자리 0 ③ 새로 생긴 구멍만 ④ `uv run ruff check .` · `uv run pytest -q` 1회 ⑤ 커밋 후보 grep(키 · 홈 경로 · 회사 데이터) ⑥ README e2e 절이 따라 할 수 있는지(명령만 읽기 — 실행 금지).

산출: `review-code-app-r2.md` 1개 · 판정 PASS/WARN/FAIL.
