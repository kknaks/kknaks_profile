# [backend] 허브 구현 — WORK-016 resolve 0.8.1(SPEC-001 0.8.1)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-be-brief.md`(같은 폴더)의 역할 · 제약 · §9 완료 보고 꼴만 써라(핸들은 preamble 값 · 그 브리프의 WORK-001 · 18105 문구는 옛 판 — 아래가 앞선다). 워크트리 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(HEAD d97a9ad · `backend/` 만 · **커밋 금지**). Procedure Hub 데이터 공개. 비밀값 · 접속 문자열 찍지 마라.

**이번 일 = `WORK-016-hub-resolve-v081.md` WP-1 ~ WP-4.** 계약 = `SPEC-001-hub-gold-mcp.md` 0.8.1. 검수 `review-work-016-017.md` 의 허브 몫(R-1 · R-6 · R-7)을 아래대로 반영.

## 검수 반영(코디 답 · 이대로)

- **R-1**: H 표에 H-17 — `test_gold_contract.py` `V07_CALLS[1]` 은 `abbr` 를 뺀 이름 하나로 · `SYN_CALLS[0]` · `V07_CALLS[0]` 은 합성 **이름** 하나로(문장 금지 — 빈 검사 통과 막기) · `V07_LINES` 의 NM 줄 지움. WP-1 `headers.py` 에 `MATCHED_HOW` · `NM_ENTRY_COLUMNS` 지움 추가. 완료 조건 `rg` 꼴에 `MATCHED_HOW\|NM_ENTRY` 더함. 고침 · ★ 수를 다시 세어 보고.
- **R-6**: §0 파일 수는 §5(9) 로 · H-6 = `OLD_FRAGMENTS` 는 「있어야」 단언 — 「부분 문자열」 · 「조사를 떼지 않는다」 는 목록에서 빼고 「없음」 단언은 T29(H-10)로 · H-4 에 `TEXTS` · `MATCHED_06` · `RESOLVE_REQUEST_06` 지움.
- **A-3**(WORK): `abbr` 인자는 스키마에 남기고 주면 `invalid_argument`(REST = MCP) — 그대로.
- **R-7**: 18105 재시작 · 시험 앱 옛 허브 자리는 **코디 몫** — 너는 18105 를 건드리지 마라.

## ⚠ 시험 — 사용자 지시

**WP 마다 그 WP 시험 파일만 · 전체 pytest 금지.** 돌린 파일 · 통과 수를 WP 별로 보고. 바뀌는 기대값은 계약(SPEC-001 0.8.1)에서 정한다 — 시험이 낸 수를 그대로 옮기지 마라.

## 포트 · 실물

18107 만(띄우기 전 `lsof` · 끝나면 내림 · `lsof` 0) · DB 판(`GOLD_REPOSITORY=db` · 접속 값은 `~/.config/phub/medallion-pg.env` 를 `set -a; . 파일; set +a` 로만 · DB `phub_medallion` · 읽기만 — 적재 · alembic 금지). 실물 확인: 정확 이름 → 코드 · 문장 → 후보 0 · 목록 꼴 개수 그대로 · `abbr` 주면 거절 · REST = MCP. 18105 · 18222 · 18223 · 18224 · 18432 프로세스 건드리지 마라.

## 보고

WP 끝마다 `[진행] backend: WP-n …` 한 줄 · 완료 보고에 「코디: 커밋 · 18105 재시작(앱 0.4 와 같이 · 시험 앱 옛 허브 자리 먼저)」.
