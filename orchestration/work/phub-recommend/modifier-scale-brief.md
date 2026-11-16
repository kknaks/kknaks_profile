# 부작용 수식어 수집 · 표준 점수 초안 발주 (2026-11-06 · 사용자 「형용사들 모아서 표준점수화」 · 읽기 전용 조사)

## 목적
시술→부작용 엣지(R15)의 빈도·정도·시점 값이 지금은 원장 글자 그대로(「드물게」「극히 드묾」「경미한」「심한」…)라 비교·정렬이 안 된다. 원장 수식어를 전부 모아, **원장이 이미 가진 눈금**에 맞춘 닫힌 값 + 서열 점수 **초안**을 만든다. 적용 아님 — 사용자가 표를 보고 고친 뒤 ERD v3.3 구조(H)와 결정 레코드로 9차에 들어간다.

## 입력(읽기만)
- 8차 산출 `silver-v3/out/`: `dictionaries.json` 의 phrase_dictionary(문구마다 parsed.degree/incidence/timing/courses/condition/misc/side/qualifiers) · `relations/R15.jsonl`(frequency_class · incidence_text · degree_text · timing_text · course) · `entities/adverse_effect.jsonl`.
- 게이트 6 R1 후보 20: `silver-v3/out/gate/batch6.json` 의 r1-candidates · `batch6-page-slots.json` 의 R1 자리.
- 원장 3판 `bronze/phub-ledger/`: complications.json(severity_levels 4단 mild/moderate/severe/critical 정의 · 항목별 severity · incidence 수치 문구) · taxonomy.json safety 칸 이름(common/uncommon/serious/…) · pih-risk.json 등 수치가 있는 파일.
- ERD v3.3 `erd-v3.3.md` §1.3(R1 수식어 · 분석기) · adverse_stopwords 138(class degree 25 · timing 29 · incidence 9 · condition 18 · connector 7 · misc 50) · course 사전(일시·지연·영구·재발·미상·지속).

## 할 일
1. **수집**: 부작용 문구(2,285 자리)에서 사건에 붙은 수식 말을 전부 모은다 — parsed 의 degree·incidence·timing·courses·misc·side·qualifiers 와 분석기 N2 가 뗀 관형어(misc by=analyzer_n2), R1 후보 20. 말마다 원장 자리 수 · 원문 예 3 · 붙은 사건 상위 3 · 지금 들어간 칸(어느 parsed 키 / R15 어느 속성).
2. **분류**: 말을 축으로 나눈다 — 빈도(얼마나 자주) · 정도(얼마나 심한지) · 시점(언제 생기나) · 경과(얼마나 가나 = course 사전) · 조건(어떤 경우) · 양상(점상·확산 등 모양) · 기타(분류 불가). 한 말이 두 축이면(「일시적」= 경과 · 「드물게 심한」) 둘 다 적는다.
3. **눈금 초안** — 원장 근거로만:
   - 정도: complications severity_levels 4단(경미 1 · 중등도 2 · 중증 3 · 위급 4)에 말을 맞춘다(경미한·가벼운·약간의·미세 → 경미 · 심한·과도한·강한·광범위 → ? 등). 원장 severity_levels 정의 문장을 근거로 붙인다.
   - 빈도: 원장 칸(common / uncommon / serious)과 원장 incidence 수치 문구(「0.5-2%」「<1%」「매우 흔함(~87%)」…)를 모아, 흔함 · 가끔 · 드묾 · 매우 드묾 같은 단계를 **원장 수치가 가르는 경계**로 제안(경계값을 원장이 안 주면 「경계 미정 — 사용자」).
   - 시점: 시술 중 · 직후 · 수시간 · 수일 · 지연 등 원장 말 그대로 단계화(점수는 시간 순서).
   - 경과: course 사전 그대로(새 값 만들지 않음 · 매핑만).
   - 각 말 → (축, 단계, 점수, 근거) · 매핑이 애매하면 「애매 — 사용자」로 비워 둔다. **지어낸 눈금·수치 금지.**
4. **R1 후보 20** 은 표 안에서 따로 표시(게이트 6 에서 넘어온 것).
5. 지금 R15 엣지가 이 초안대로 매핑되면 몇 개 엣지가 빈도/정도 값을 갖게 되는지 센다(결정 전 참고 · 적용 아님).

## 산출(쓰기 허용 위치 · 그 밖 수정 금지)
- `modifier-scale/modifier-inventory.json`(말 전수)
- `modifier-scale/modifier-scale-draft.md`(사용자 검토용 · 축별 표 · 눈금 표 · 애매 목록 · R1 20 · 엣지 영향 수)
- 생성 스크립트 `modifier-scale/collect.py`
커밋·게시 금지. silver-v3/ · bronze/ · erd-* 수정 금지.

## 보고(30줄 안)
축별 말 수 · 눈금 초안 요약(정도 4단 · 빈도 단계와 경계 근거) · 애매 수 · R1 20 처리 · 엣지 영향 수 · 파일 경로.
