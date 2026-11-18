# WORK-013(허브) 작성 지시서 — SPEC-001 0.7.1 구현 계획(내려가기 DP · 고민 부위 CS · 줄임 NM · 부위 없는 고민 SP)

**너는 앞 판의 맥락이 없다.** `work-write-instructions.md`(같은 폴더)의 역할 · 제약 · 검증 · 완료 보고 꼴 그대로(핸들은 preamble 값). allowed_paths = **`WORK-013-hub-v07.md` 새 파일 하나만**. 다른 writer 가 같은 폴더에 `WORK-014-consult-v03.md` 를 동시에 쓴다 — 손대지 마라. Procedure Hub 데이터 공개.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 허브 `H=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(읽기만 · HEAD daa54e3)

읽을 것: `$W/SPEC-001-hub-gold-mcp.md` 0.7.1(§4-1 · §4-5 · §5-11 DP · CS · NM · SP · §9 T24~T28) · `$W/review-spec-001-v07.md` · `$W/review-spec-001-v071.md`(NOTE N-2 · N-3 은 WORK 에 한 줄씩) · `$W/SPEC-003-hub-gold-db.md`(CSV=DB · DT10) · `$W/_RESUME.md` §2 11-17 맨 위 행들(**시험은 구현한 것만 · 전체 안 돌림** · U7 (a) · 규칙 ① · O-30 · O-31) · 앞 WORK 꼴 `$W/WORK-010-hub-db.md` · 허브 코드.

쓸 것: SPEC 절 ↔ WP(미대응 0) · 시험 T24~T28 + DT10 표본(prefer 짝 · filter 짝 — N-3) · N-2(site_match 꼴 하나로) · CSV 판 · DB 판 응답 같음 · MCP 도구 설명 문장 · **WP 마다 「그 WP 시험 파일만 돌림 · 전체 pytest 금지 · 돌린 파일 목록 보고」**(사용자 11-17) · 실물 확인(허브 18107 띄웠다 내림 · 18105 는 코디 것) · 완료 조건.

검증: 대응표 · 경로 실재 · 공개 grep.
