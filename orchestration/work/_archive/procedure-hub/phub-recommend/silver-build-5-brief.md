# 실버 빌드 5차 발주서 — 빌더 v3 보강 + 결정 묶음 3 (사용자 승인 2026-11-05 「v3 진행하자」 흐름)

## 목적
동결된 ERD **v3**(`ERD-FROZEN.md` v3 절 · `erd-v3.json` · `erd-v3-dictionaries.json` · `erd-v3-tuples.py/.json` · `erd-v3.md`) 대로 빌더 `silver-v3/` 를 보강하고, 결정 묶음 3 을 만들어 5차 빌드를 돌린다.

## A. 빌더 v3 보강 (코드)
ERD 입력을 `erd-v3.json`·`erd-v3-dictionaries.json` 로 바꾸고 V3-1~V3-10 을 전부 구현한다. 규칙 해석은 `erd-v3.md` 가 정본, 분해 결과는 `erd-v3-tuples.py` 참조 구현과 **같아야** 한다(결정 적용 전 수치 = `erd-v3-tuples.json` 요약, 차이 0 — 검산 ③).
- V3-1 부작용 qualifier 칸·사전 `adverse_qualifier` · V3-2 회사·제품 괄호 규칙 · V3-3 stopwords → 참조 `qualifier_text`·R12 `session_index` · V3-4 `+`/`/` 규칙 · multi_tuple(anchor `REF-…#s<i>`) · R12 `member_mode`·`alternatives` · V3-5 site.kind(layer 는 시술 site 금지) · V3-6 `canonical_rename` kind(코드 기반 id 유지 · 사전 id 재계산 · 옛 id alias) · V3-7 description·media_refs 속성(값은 새 원천 있을 때만) · V3-8 R5 하위분류 기법 · V3-9 tuple_assign/_multi/adverse_tuple_assign 을 미해결·조합·#s<i> anchor 에도 적용 · V3-10 fold_approve 가 ⑦ 를 닫음(status=resolved·decision_id).
- 기존 결정(batch1·2a·2b·_bootstrap)은 v3 에서도 그대로 적용돼야 한다. 4차에서 거부된 2건(SLS-02·09 outer_only)과 미적용 3건(per_site)은 v3 규칙으로 자동 해소되거나 적용되는지 확인해 report 에.
- `check.py` 는 v3 항목으로 갱신(①~⑨ 유지 + V3 각 항목 + ⑦ 닫힘 수 + layer 금지 + qualifier).

## B. 결정 묶음 3
`decisions/_batch3-candidates.md`(사용자 대화에서 쌓인 것)를 결정 파일로. 두 폴더로 나눈다.
- `decisions/batch3/`(**approved** · decided_by 사용자(이건학) · 2026-11-05): 표에 「확정」또는 사용자 말이 결정인 것 — M1 「보툴리눔 톡신」·M3 「바이오스티뮬레이터」 rename(canonical_rename · 콜라겐부스터 is_marketing_name) · 교근 → 사각턱 동의어 · 더모톡신·메조보톡스 → 스킨보톡스 동의어 · 시크릿 → 시크릿RF 동의어(시크릿맥스 제외) · 라라젯 제품 등록(출처 `sources/2026-11-05-lhalajet-blsclinic.md`) · 인과 엣지 R30 동상→괴사 · 혈관 폐색→괴사 · 섬유화→경결(영구) · 금기 엣지 R16 이소트레티노인→프락셔널·필링 각각 · 감각이상/홍반·부종 3건 → 시술 부위 adverse_tuple_assign · 지방괴사 → (괴사, 피하 지방층)·피부 괴사 → (괴사, 피부) · #58 → (경결, 일시)+(섬유화, 미상) · 엑소좀 통합 6단계(제품 3 dictionary_add · M5 제품 2 재분류 → M4 · M17 엑소좀 → M4 동의어 · M15 엑소좀필/두피주사 tuple_assign (엑소좀, 얼굴/두피, 도포/주사) · 임상 규칙 「화장품 허가·주사 불법」 → 엑소좀 제품 전부 · 시장가 PRP/엑소좀 M5 동의어 제외 + 메뉴 2 → M4) · 엘러간 회사 동의어(「엘러간」= 앨러간/애브비) · 부위 「팔자」(필러 팔자+볼) · 결정 묶음 1 에서 미제안이던 조각 중 v3 규칙으로 근거가 생긴 것.
  각 결정에 근거 locator(원장·sources·사용자 말 인용) 필수. 근거 없는 건 approved 로 만들지 말고 proposed 로.
- `decisions/batch3-proposed/`(**proposed** · 빌드가 읽지 않음): M5 「자가혈 유래 시술」 rename(추천·미확정) · M16 하위분류별 기법 지정(V3-8) · 해부 이름 → 부위 동의어 묶음(광경근→목·코끝→코 등 미등록 조각에서 추출) · HIFU·RF·필링·MTS·LED·토닝 등 묶음 1 동의어가 v3 에서 하위분류 라벨에 닿는지 확인해 안 닿으면 보강 제안 · 「공기색전」 qualifier 튜플 · 그 밖 `_batch3-candidates.md` 의 「추천」「미정」. `_INDEX.md` 로 표.

## C. 5차 빌드
`python3 build.py`(브론즈 2판 기본) → `check.py` 전부 PASS. report.md 「5차 빌드 · ERD v3 + 묶음 3」: 4차 대비 변화표(개체·관계·게이트 4종·충돌 kind·⑦ 닫힘) · 적용/거부 결정 수 · v3 규칙으로 자동 해소된 참조 수(`+` 4곳 · 괄호 대안 3 · stopwords 4 등) · 미해결 사유 상위 조각.

## 규칙
ERD v3 정본 · 원장 불변 · provenance 필수 · 재실행 바이트 동일 · 커밋 금지 · 금지 목록은 이전 발주서와 같음(silver-v3 외 silver-* · step2·3 · DATA-001 · _archive 금지).

## 보고
A 의 V3-1~10 구현 위치 한 줄씩 · B 의 approved/proposed 건수 · C 의 변화표 · check 결과. 본문 재붙임 금지.
