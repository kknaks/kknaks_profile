# [reviewer_code] 허브 코드 검수 — WORK-016 resolve 0.8.1

**앞 판 맥락 없음.** `phub-gold-jev-review-code-hub-brief.md`(같은 폴더)의 역할 · 제약 · §9 완료 보고 꼴만 써라(그 브리프의 WORK-001 · 0.4.1 · 「볼 것」 은 옛 판 — 아래가 앞선다 · 핸들은 preamble 값). 검수 워크트리 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(HEAD d97a9ad 위 미커밋 변경 — 15 수정 · 1 삭제). **파일 고치지 마라 · stash · checkout 금지.**

## 읽을 것

계약 `SPEC-001-hub-gold-mcp.md` 0.8.1 · `WORK-016-hub-resolve-v081.md` · 지시서 `impl-hub-v081-instructions.md` · 검수 `review-work-016-017.md`(R-1 · R-6) · `_RESUME.md` §2 맨 위 11-18 행. 구현 보고 요지: 정확 norm 일치(기존 `entries_by_norm`) · `matched={span}` · 줄임 색인 · `abbr_keys`/`entries_by_abbr` · headers 상수 지움 · `abbr` 주면 resolve.py 한 곳에서 422(서명 · REST · MCP 스키마엔 남김) · 시험 지움 20 · 고침 13 · ★7 · Q21 = `SECOND_END` 상수.

## 볼 것

1. `git diff` 범위 — `backend/` 밖 0 · 다른 도구(scope · facets · concern_candidates …) 코드 diff 0 · service.py diff 0 주장 확인.
2. SPEC-001 0.8.1 대조 — §4-1 · §5-1 R1~R9 · 부록 A 필드 · 오류 · 목록 꼴 불변 · REST = MCP.
3. 남은 줄임 · 부분 일치 흔적 grep(`abbr` · `줄임` · `covered_by` · `HOW_` · `MATCHED_` · `NM_`) — 허용 줄 밖 0.
4. 시험 — 지운 시험이 계약 변경 몫만인지(계약과 무관한 시험을 지우지 않았나) · 고친 기대값이 계약에서 오나 · `SECOND_END` 가 gold 근거와 맞나. **직접 돌려라**: WORK-016 의 그 시험 파일들만(전체 pytest 금지) · 데이터 env 판 1회(접속 값은 `~/.config/phub/medallion-pg.env` 를 `set -a; . 파일; set +a` 로만 · 찍지 마라).
5. 실물: 서버를 띄우지 마라(18105 는 아직 0.7.2 — 비교 기준으로 GET 만).
6. 비밀값 grep.

## 산출

`review-code-hub-v081.md` 1개(같은 폴더). 판정 PASS/WARN/FAIL + 지적 표(파일:줄 · 심각도 · SPEC 절 · 고칠 방향).
