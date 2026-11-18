# [backend] 허브 구현 — WORK-013 0.2(SPEC-001 0.7.2 · 내려가기 · 고민 부위 · 줄임 · 부위 규칙)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-be-brief.md`(같은 폴더)의 역할 · 제약 · §9 완료 보고 그대로(핸들은 preamble 값 · 그 브리프의 WORK-001 · 18105 문구는 옛 판 — 아래가 앞선다). 워크트리 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(HEAD daa54e3 위 · `backend/` 만 · 커밋 금지). Procedure Hub 데이터 공개. 비밀값 · 접속 문자열 찍지 마라.

**이번 일 = `WORK-013-hub-v07.md` 0.2 WP-1 ~ WP-4 + 18107 실물.** 계약 = `SPEC-001-hub-gold-mcp.md` 0.7.2 · `SPEC-003-hub-gold-db.md`. 검수 `review-spec-001-v07.md` · `review-spec-001-v071.md` · `review-work-013.md` 반영.

## ⚠ 시험 — 사용자 지시(11-17)

**WP 마다 그 WP 시험 파일만. 전체 pytest 금지.** 돌린 파일 · 통과 수를 WP 별로 보고.
- **B-1(코디 답)**: WP-4 의 T27(두 판 · 기존 필드 불변)은 gold 시험 묶음(`tests/test_gold_*.py` + `tests/test_medallion_repo.py`)으로 돌려도 된다 — 이게 이번 판의 최대 범위다.

## 검수 WARN · NOTE — 이대로

- **W-1**: 완료 조건 8 의 수는 기본 `upper=auto` 로 260 고민을 돌린 값(155)으로 적는다 — 142 는 자기 행 247 기준이라는 것을 함께.
- **W-2**: 기본 · holes fixture 에 줄임 열쇠가 0 이다 → DT9 · DT10 의 줄임 표본은 v07 판 fixture + `matched.how == "줄임"` 단언으로.
- NOTE N-1 ~ N-4 는 리포트 「고칠 방향」 대로.
- **B-2(접속 값)**: `~/.config/phub/medallion-pg.env` 를 `set -a; . 파일; set +a` 로만(찍지 마라) · DB 이름 `phub_medallion`.
- **B-3(일정)**: 앱 0.3 이 병행 구현 중이다. 너는 18107 에서 확인하고 내린다 — 18105 재시작은 코디가 네 완료 뒤 한다.

## 포트

18107 만(띄우기 전 `lsof` · 끝나면 내림 · `lsof` 0). 18105 · 18222 · 18223 · 18220 · 18210 · 18005 건드리지 마라 · PG 18432 는 읽기 · 적재는 WORK 가 정한 만큼만.

## 보고

WP 끝마다 `[진행] backend: WP-n …` 한 줄 · 완료 보고에 「코디: 18105 를 0.7.2 로 재시작(DB 판) 필요」.
