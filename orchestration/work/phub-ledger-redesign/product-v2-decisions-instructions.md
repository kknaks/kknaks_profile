# 제품 사전 v2 — 사용자 판단 반영 (사용자 조사 2026-11-11)

대상: `silver-model/drafts/product-v2/` 의 product · organization · product_material · product_method · product-research · product-v2-notes (UTF-8 BOM 유지). `silver/` 와 원장은 고치지 않는다.

## 1. 시술 아님 → 제품 사전에서 뺀다
- 아큐탄(PRD-684) · 컨트라투벡스(PRD-683) · 헤어맥스(PRD-356)를 product 에서 지우고 이 제품들의 product_material · product_method 행도 지운다.
- 새 파일 `silver-model/archive/not-procedure-products.csv`(UTF-8 BOM)에 옮긴다. 칼럼: `former_code` · `name_ko` · `aliases` · `kind` · `ingredient` · `reason` · `basis` · `sources`.
  - 아큐탄: ingredient = 이소트레티노인 · reason = 처방 경구약(로슈 로아큐탄 2019-02 공급 중단 · 2019-04 품목허가 자진 취하, 이후 한미약품 이소티논연질캡슐이 대조약). 원장의 「아큐탄」은 이소트레티노인 복용 전체를 부르는 말로 쓰였을 가능성 — 사람 조건(복용력) 사전과 이을 것.
  - 컨트라투벡스: name_ko = **콘투락투벡스겔**(공식 제품명), aliases = 컨트라투벡스 · reason = 일반의약품 외용 겔(2001 허가), 집에서 바름.
  - 헤어맥스: reason = 가정용 LLLT 탈모 기기(FDA K180885).

## 2. 벨카이라 = 카이벨라 → 한 행
- 한 행으로 합치고(코드는 앞 번호), 다른 이름은 aliases. description 에 「국내 2017-08 허가 → 2020-12 품목허가 자진 취하(국내 철수)」.
- **같은 성분(데옥시콜산)의 다른 제품(브이올렛주 · 브이벨라주 등)은 합치지 않는다.**
- 원장에서 「벨카이라」「카이벨라」가 특정 제품으로 쓰였는지, 턱밑지방 주사 전체를 부르는 말로 쓰였는지 원장 자리를 보고 notes 에 판정(포인터와 원문).

## 3. 노바스템 · 미라셀
- **노바스템**: kind = 키트 · 재료 = **자가혈만**(골수 아님) · description 에 「자가혈(PRP) 분리·농축 키트. 원장 「ADSC 배양 성장인자」는 오류」.
- **미라셀**: 미라셀은 회사 이름이고 실제 제품은 추출 장비 SMART M-CELL + 전용 키트(BSC Blood Kit · BMSC Bone Marrow Kit) 세트(FDA 510(k)). 한 행 유지 · kind = 키트 · description 에 장비+키트 세트임을 명시 · aliases 에 SMART M-CELL · 재료 = 자가혈 + 골수(재료 사전에 골수가 없으면 잇지 말고 notes 「재료 추가 후보」). 조직(미라셀 회사)이 organization 에 필요하면 만든다.

## 4. 원장 오류 정정 (실버만, 원장 오류 표에 기록)
- **잼버실** → 재질 PDO(외부 조사, 출처 강남언니·식약처). 기존 PCA 연결을 PDO 로 바꾸고 product_material.source = 외부 조사.
- **인모드FX** → 비침습 RF. 니들RF(M11)가 아니다 — modality_code 를 기기 리프팅 쪽(M9)으로 맞추고, 니들 관련 방법 연결이 있으면 지운다. description 에 「비침습 RF(일부 병원은 마이크로핀 전달로 설명 — 바늘을 찔러 넣는 니들RF 아님)」.
- **울트라V** → **재질 빈칸**. 울트라V는 회사 이름(PDO · PCL · PLCL 실 · 필러 · 부스터를 모두 만듦)이라 원장 행이 특정 제품을 가리키지 않는 한 재질을 정할 수 없다. 기존 재질 연결 삭제, description 「회사명이라 재질 미정」.
- **리바이브 글리세롤** → 부모 「리바이브」(벨로테로 리바이브, 멀츠 · 글리세롤 + HA 복합)에 **합치고** 「리바이브 글리세롤」은 aliases. 부모 재료에 글리세롤이 없으면 잇는다(재료 사전 코드로).

## 5. 확인 안 된 제품 표시
- product 에 칼럼 `name_check` 추가: `확인`(웹 또는 식약처로 제품 실재 확인) / `웹 미확인` / `웹·식약처 미확인`.
- **`웹·식약처 미확인`은 식약처(의료기기·의약품 DB)를 실제로 조회했을 때만** 쓴다. 이번 조사에서 식약처를 실제로 조회했는지 notes 에 방법과 함께 정직하게 적는다(조회하지 않았으면 `웹 미확인`).
- 원장에 있고 이번에 조사하지 않은 제품(원장 제조사가 있던 것)은 `확인` 으로 두지 말고 빈칸(조사 대상 아님).
- 오기 의심(에피로크 → 에피티크 등)은 고치지 않는다.

## 6. 마무리
- notes: 이번 반영 절 추가 + 원장 오류 표 갱신(잼버실 · 인모드FX · 울트라V · 리바이브 글리세롤 · 벨카이라/카이벨라 · 노바스템/미라셀 · 아큐탄/컨트라투벡스 표기) + 출처(사용자 조사: 데일리팜 · 의약품안전나라 · 약학정보원 · 메디칼타임즈 · 강남언니 · Utusan/PR Newswire · 리베리의원 · Newsweek · 데일리팜(벨로테로 리바이브)).
- 검사: 코드 참조 전부 존재 · 이름 괄호 0 · basis 빈 행 0 · 지운 제품을 가리키는 연결 0.
- `git status` 확인 후 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "product-v2 판단 반영 완료" --enter`
(이 dispatch 의 worker_done 을 이미 보냈다면 다시 보내지 않는다. 새로 발주된 워커면 preamble 의 worker_done 을 한 번, --report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/product-v2/product-v2-notes.md)
