# WORK-010 검수 지시서 (짧게)

**너는 앞 판의 맥락이 없다.** `work-review-instructions.md`(같은 폴더)의 역할 · 볼 것 · 제약 · 완료 보고 꼴 그대로(핸들은 preamble 값). 11-17 사용자 결정: Procedure Hub 데이터는 공개 정보 — 「회사 데이터 본문 0」 은 이 데이터에 걸지 않는다(비밀값 · 접속 문자열 금지는 그대로).

허브 `H=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(읽기만 · HEAD 85c28af).

읽을 것: `WORK-010-hub-db.md` · 계약 `SPEC-003-hub-gold-db.md` · `review-spec-003.md`(WARN 4 · NOTE 8) · `_RESUME.md` §2 11-17 행(U-1 · U-2 · 검수 뒤 코디 W-1~W-4) · 코디 답 B-1~B-3(아래).

코디 답(§11 B):
- B-1: 접속 값 파일은 `KEY=VALUE` 줄(`DATABASE_URL` 을 asyncpg 꼴 그대로 낸다) — 워커는 `set -a; . <코디가 발주서에 줄 경로>; set +a` 로만 올리고 찍지 않는다 · DB 이름은 발주서에.
- B-2: 37 답 키 명세 = 앱 워크트리 `data/eval-set/answer-key/` · `calls/`(gitignore 로컬 · 읽기만).
- B-3: 18107 은 WP-4 끝에 워커가 자기 프로세스를 스스로 내린다.

볼 것: ① SPEC-003 ↔ WP 대응(미대응 0) · 지어낸 동작 0 ② W-1~W-4 · NOTE 8 반영 · A-1(GoldSettings.DATABASE_URL 하나 — 기존 시험 test_app_main_untouched · test_entrypoint_imports_no_db 와 맞나 · alembic 은 어느 설정을 읽나 · 엉뚱한 DB 로 갈 길 0) ③ 실행 가능성(경로 · 명령 · 포트 18107 · 18432 · 18105/18220 은 코디 것) ④ WP-0 이 「확인 안 됨」 을 실물로 닫나 · 안 될 때 대안 ⑤ 완료 조건이 실물(로컬 PG 적재 · DB 판 응답 = CSV 판)을 요구 ⑥ 비밀값 grep.

산출: `review-work-010.md` 1개 · 판정 PASS/WARN/FAIL. FAIL 이 없으면 「구현 진행 가능」 명시.
