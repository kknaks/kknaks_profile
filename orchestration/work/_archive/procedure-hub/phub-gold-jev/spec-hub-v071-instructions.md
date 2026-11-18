# SPEC-001 0.7.1 — 0.7.0 검수 고침 + 규칙 ①(부위 연결 없는 고민 + 부위 질문)

**너는 앞 판의 맥락이 없다.** 먼저 `phub-gold-jev-write-brief.md`(같은 폴더) 전체를 읽어라 — 역할 · 제약 · §8 검증 · §9 완료 보고 그대로(핸들은 preamble 값). **이번 allowed_paths = `$W/SPEC-001-hub-gold-mcp.md` 한 파일(0.7.0 → 0.7.1).** 필요하면 SPEC-002 에 닿는 줄은 「SPEC-002 §x 되적기 후보」 로 SPEC-001 변경 기록 끝에 목록만(SPEC-002 파일은 고치지 마라). 같은 폴더에서 다른 워커가 다른 파일을 검수 중 — 손대지 마라. Procedure Hub 데이터는 공개. 외부 API 호출 금지.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 허브 `H=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(읽기만) · `SM=$W/../_archive/procedure-hub/phub-ledger-redesign/silver-model`

## 읽을 것

`$W/_RESUME.md` §2 11-17 맨 위 행들(**U7-1~3 = (a)** · **SPEC-006 U6 · 규칙 ①** · 내려가기 · 메뉴는 시술 아님) · `$W/review-spec-001-v07.md`(WARN 6 · NOTE 8) · `$W/SPEC-001-hub-gold-mcp.md` 0.7.0(§5-9 HG3 · §5-11) · `$W/SPEC-002-chat-eval.md`(TG · 부위 거르개 쪽) · 허브 `concern.py` · `core.py`.

## 할 것

1. **검수 WARN 6 닫기**(리포트 고칠 방향대로): W-1 고민 수 242 · 247 · 142 · 138 · 최대 107(CON-226 · 계열 6) — 빈 고민 묶음 63행은 따로 표기 · W-2 `lands=procedure` 꼴(어느 묶음 · procedures[] 범위 · unit) · W-3 `concern_candidates` · `resolve` MCP 도구 설명 문장 하나씩(unit=계열 · how=줄임 뜻) · W-4 낡은 문장 · W-5 한 글자 앞 낱말 규칙 한 꼴로(2,881 이 나오는 꼴) · W-6 줄임 오매칭 근거에 리포트 §3 표본(52 / 3,254 · 1.6%) 사실 적고 규칙은 그대로. NOTE 8 은 리포트대로.
2. **규칙 ①(사용자 결정 11-17)**: 고민에 `concern_site` 가 **없을 때** 「고민 + 부위」 요청은 **부위로 거르지 않는다** — 그 고민의 시술 행 전부를 내고, 행 부위 글자가 요청 부위와 맞는 행에 「우선 표시」 표지(칸 이름 정함)를 단다 · 앱은 그 행을 앞에 둔다. `concern_site` 가 **있는** 고민(이마주름 등)은 HG3 그대로. 「행은 안 뺌 · 빠짐없이 · 묻지 않은 것 안 붙임」. 재셈: 부위 연결 없는 고민 수(160 · 하위 포함 기준 확인) · 「볼 + 탄력 저하」 꼴 지금 남는 행 수 → 규칙 뒤 행 수 · 표지 붙는 행 수 · 이마 꼴(HG3) 회귀 0. 시험 T(이어서). 앱 걷기 · 답 키 함수에 같은 규칙이 필요하다는 줄은 「SPEC-002 되적기 후보」 로.
3. 0.7.1 변경 기록 · 열린 것 · WORK 전 사용자 결정(새로 생기면만 · 추천 붙임).

## 검증

재셈 명령과 결과 · 결정 행 → 문서:줄 · 공개 grep.
