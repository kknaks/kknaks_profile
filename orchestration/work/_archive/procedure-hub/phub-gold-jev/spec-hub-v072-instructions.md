# SPEC-001 0.7.2 + WORK-013 고침 — 부위 거름 규칙 한 줄 바꿈

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-write-brief.md`(같은 폴더)의 역할 · 제약 · §9 완료 보고 그대로(핸들은 preamble 값). **이번 allowed_paths = `$W/SPEC-001-hub-gold-mcp.md`(0.7.1 → 0.7.2) · `$W/WORK-013-hub-v07.md`(0.1 → 0.2) 두 파일.** Procedure Hub 데이터 공개. 외부 호출 금지.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · `SM=$W/../_archive/procedure-hub/phub-ledger-redesign/silver-model`

## 결정(사용자 11-17 · `_RESUME` §2 맨 위 행)

「고민 + 부위」 요청: **물은 부위가 그 고민의 부위(자기 + 하위 고민 — CS 의 `sites[]` 와 같은 집합) 안에 있을 때만 부위로 거른다(HG3).** 그 밖 — 고민에 부위가 없거나, 부위가 있어도 물은 부위가 그 안에 없으면 — **거르지 않고 우선 표시(SP)**. 0.7.1 SP 는 「고민에 부위가 없을 때만 prefer」 였다 — 이것을 넓힌다.

까닭: research-concern-site.md §0-5 — 하위 고민에 부위를 넣으면 윗고민이 HG3 로 뒤집혀 「흉터 + 볼」 113 → 0 행 등 · O-31(부위 있는 고민을 다른 부위로 물으면 0 · 8,444 짝)도 같은 뿌리.

## 할 것

1. SPEC-001: §5-11 SP · §4-5(`site_mode` auto 판정) · O-30 · O-31(닫힘) · T28 고침 · 재셈(지금 데이터: filter 가 되는 짝 수 · prefer 짝 수 · 「이마주름 + 볼」 꼴 0 → 행 · 회귀 — 물은 부위가 안에 있는 짝은 지금과 같은 행) · **보강 뒤 어림**(`research-concern-site.md` 추천 7고민 8행을 넣었다고 치면 흉터 + 볼 113 이 그대로인지) · 0.7.2 변경 기록.
2. WORK-013: WP-3(SP)의 판정 · 시험 파일 · 기존 시험 기대 바뀌는 자리(grep 다시) 고침 · 「시험은 그 WP 파일만 · 전체 금지」 그대로 · B-1~B-3 은 그대로 둠(코디가 답함).

## 검증

재셈 명령과 결과 · 두 문서 사이 칸 이름 일치 · 공개 grep.
