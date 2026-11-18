# SPEC-001 0.7.0 검수 지시서(허브 — 시술로 내려가기 · 고민 부위 · 줄임 일치)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-review-doc-brief.md`(같은 폴더)의 역할 · 제약 · §9 완료 보고 그대로(핸들은 preamble 값). Procedure Hub 데이터는 공개(비밀값 · 키 · 내부 URL 은 그대로 본다). 외부 API 호출 금지. 같은 폴더에서 다른 워커들이 다른 파일을 쓰는 중 — 네 리포트 외에는 손대지 마라.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 허브 `H=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(읽기만) · `SM=$W/../_archive/procedure-hub/phub-ledger-redesign/silver-model`

읽을 것: `$W/spec-hub-v07-instructions.md`(지시 · 「정해진 것」) · `$W/_RESUME.md` §1 수정 2 목록 00 · 6 · §2 11-17 맨 위 행들 · `$W/SPEC-001-hub-gold-mcp.md` 0.7.0(변경 기록 · §5-11 · §4-5 · §4-1 · §9 T24~T27 · §10 U7) · `$W/SPEC-003-hub-gold-db.md`(CSV=DB) · silver 용어집 · gold CSV.

할 것:
1. 지시 H1~H3 이 문서:줄로 닫혔나 · 「정해진 것」 위반 0 — 특히 **메뉴 · 패키지 · 제품 이름이 시술 후보로 새는 길 0** · 하위 일반화 금지(계열 단위 표지) · 문항 맞춤 0 · 기존 필드 · 해시 불변.
2. 재셈: 시술 코드 없는 행 722(539 · 128 · 55) · 못 내림 0 · 고민 243 / 43 / 41(제품 길 포함 43) · 내린 고민 143 · 최대 130 · 부위 있는 고민 85 / 하위 포함 100 · 줄임 열쇠 2,881 · 37 문항 새 후보 0 · 턱살 CON-168 ↔ SITE-072. 다르면 세는 식까지.
3. 줄임 일치(NM)가 오매칭을 늘리지 않나(「채우지」 → 「채움」 · 「주사」 같은 꼴 · 한 글자 · 조사) — 표본 셈.
4. 계약 구멍: `descended[]` 꼴 · 쪽 넘김 · 크기(고민당 최대 130) · `sites[]` match · CSV/DB 같은 응답 · MCP 도구 설명 · 앱이 읽을 자리.
5. U7-1 ~ U7-3 추천이 원칙과 맞나 · 숨은 사용자 결정 0.
6. **최종**: PASS 면 「U7-1 ~ U7-3 정해지면 WORK 진행 가능」 명시.

산출: `$W/review-spec-001-v07.md` 1개만.
