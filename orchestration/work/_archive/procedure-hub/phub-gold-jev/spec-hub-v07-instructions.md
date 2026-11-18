# SPEC-001 0.7 — 허브: 시술로 내려가기 · 고민 부위 · 이름 맞춤

**너는 앞 판의 맥락이 없다.** 먼저 `phub-gold-jev-write-brief.md`(같은 폴더) 전체를 읽어라 — 역할 · 제약 · §8 검증 · §9 완료 보고 그대로(핸들은 preamble 값). **이번 allowed_paths = `$W/SPEC-001-hub-gold-mcp.md` 한 파일(0.6.0 → 0.7.0 · 고친 절 · 변경 기록 · 열린 것).** Procedure Hub 데이터는 공개(비밀값 · 키 · 내부 URL 금지 그대로). 외부 API 호출 금지.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 허브 `H=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(읽기만 · HEAD daa54e3 · 로컬 DB 판) · `SM=$W/../_archive/procedure-hub/phub-ledger-redesign/silver-model`

## 읽을 것

1. `$W/_RESUME.md` §1 「수정 2 목록」 00 · 6 · §2 11-17 맨 위 행들(「얼굴 점 = 대화 고민 부위 · 점 누르면 그 고민 시술」 · 「V라인주사 등 메뉴는 시술 아님」 · 「시술로 내려가기 규칙」) ← 정본
2. `$W/SPEC-001-hub-gold-mcp.md` 0.6.0 · `$W/SPEC-003-hub-gold-db.md`(DB 판 — repository · 계약 상수 · 응답 동일)
3. silver 용어집 `$SM/notes/glossary.md`(계열 M > 시술 PRC > 케이스 CAS · 제품 PRD · 패키지 PKG 기준) · `$SM/gold/semantic-map.md`(§5 물려받기 · reach) · `g_indication`(reach 갈래 8) · silver `package_item` · `procedure` · `product_procedure` · `case_product` · `concern_site` · `concern`(parent)
4. 허브 코드 `$H/backend/app/modules/gold/{core,service,concern,closure,resolve,repository}.py`

## 정해진 것(다시 묻지 마라)

- **H1 시술로 내려가기**: 고민에 닿은 대상이 시술이 아니면(패키지 · 메뉴 · 계열 · 제품) 연결을 끝까지 따라가 **시술(PRC)** 로 내린다 + 어디를 거쳐 내려왔는지 층 표시(경로). 하위 일반화 금지는 「계열 단위 표지」 로 지킨다(내린 시술 하나하나에 그 적응을 자기 것으로 적지 않음). **메뉴 · 패키지 이름(V라인주사 등)은 시술이 아니다** — 경로로만 남기고 시술 후보로 내지 않는다. 코디 셈: 적응 있는 고민 243 중 직접 시술 0 = 43 → 규칙으로 41(패키지 항목 8 · 계열 36). **문항 맞춤 금지 — 일반 규칙**.
- **H2 고민 부위**: `concern_candidates` 응답에 그 고민의 부위 코드 목록(silver `concern_site` · 하위 고민 포함 여부 정함) — 앱이 얼굴 점에 쓴다.
- **H3 이름 맞춤 보강**: 줄여 말한 이름(「지방 주사」 → 지방분해 주사 M18 등)을 잡는 일반 규칙(별칭 · 부분 일치 · 띄어쓰기) — 지금 resolve 규칙(SPEC-001 §5-1) 위에. 오매칭(「채우지」 → 제품 「채움」 같은 꼴)을 늘리지 않는 조건 함께.
- CSV · DB 두 판 응답 같음 유지(SPEC-003) · 응답 필드 추가는 기존 필드를 바꾸지 않음.

## 할 것

H1 · H2 · H3 각각: 규칙 · 도구 계약(입력 · 출력 칸) · gold 재셈 근거(고민 수 · 내려간 시술 수 · 메뉴/패키지가 시술로 새는 것 0) · 시험 T(번호 이어서) · 열린 것 · **WORK 전 사용자 결정**(최소 · 추천 붙임). 0.7.0 변경 기록.

## 검증

재셈 명령과 결과 · 결정 행 → 문서:줄 · 공개 grep.
