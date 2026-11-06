# ERD v2 발주서 — 구조 개정 2건 (사용자 승인 2026-11-04 「진행하자」)

v1.1(`erd-v1.1.*` · 생성기 `erd_spec_v11.py`·`erd_colmap_v11.py`·`erd_build_v11.py` · `erd-v1.1-resolve.py` · `erd-v1.1-check.py`)을 **구조만** 개정한다.
v1 발주서(`erd-v1-brief.md`) · v1.1 발주서(`erd-v1.1-brief.md`)의 입력·금지·기준·질문 기본값·처분은 그대로다.
ERD 는 설계다. 데이터는 안 고친다. 사전 값·동의어 추가는 이번 범위가 아니다(실버 빌드의 결정 묶음).
**범위는 아래 두 구조 변경뿐이다. 그 밖의 개체·관계·속성은 v1.1 그대로 둔다.** 바꾸고 싶은 게 보이면 §「v2 밖 관찰」에 적고 손대지 않는다.

## 구조 변경 1 — 시술 축: 분류 항목과 단위 시술 분리
배경: v1.1 의 `procedure` 는 taxonomy 항목 521 그대로다. taxonomy 는 제품·마케팅명·부위 붙은 메뉴·기법이 섞인 분류 트리(10-27 결정)라 「단위 시술 = 무엇을 × 어디에 × 어떻게」가 아니고, 부위 관계가 없다.
- `catalog_item`(분류 항목, 접두 CAT) 신설: taxonomy modality 항목 521 을 **있는 그대로** 담는다. v1.1 `procedure` 의 속성·alias·출처를 전부 여기로 옮긴다. 계층(계열→하위분류→항목)도 그대로.
- `procedure`(단위 시술, 접두 PRC) 재정의: **튜플 (what, site, technique)**.
  - what = modality | modality_subcategory | product 중 하나(필수). 분류 항목이 제품명이면 product, 아니면 가장 구체적인 계열 층.
  - site = 부위 사전 값 | `none`(부위 미상). 「전체얼굴」같은 조각이 사전에 없으면 none 이 아니라 **미등록 조각 기록 + none** 으로 두고 표시.
  - technique = 기법 사전 값 | 계열 기본값 상속(v1.1 R5 의 계열→기법에서) | `none`.
  - 식별자 = PRC-sha256(what_id|site_id|technique_id)[:10]. 같은 튜플 = 같은 시술.
  - 원천: ① 분류 항목 521 을 분해 규칙(v1.1 §1.3 확장: 이름 → what/site/technique 조각)으로 튜플화 ② 자유 텍스트 참조(v1.1 §9.2 자리 전부)의 분해 결과 ③ market-pricing 메뉴 122. 하나의 분류 항목이 하나의 튜플로 내려가고, 여러 분류 항목이 같은 튜플이면 같은 시술에 R `derived_from`(procedure → catalog_item, 1:N) 으로 매단다.
  - 분해에서 조합 기호(+·/)로 멤버가 둘 이상이면 시술이 아니라 `package`(kind=combo_ref) 로 보내고 멤버 각각을 튜플화.
- v1.1 에서 시술 축(proc_axis)을 끝으로 쓰던 엣지(R3·R9·R12·R15·R16·R17·R18)의 target_depth 에 `catalog_item` 을 추가하고, 튜플이 확정된 경우 procedure 로 승격되는 규칙을 적는다. 규칙만 적고 값은 안 만든다.
- 부위 사전: v1.1 의 21 을 유지. 공유 사전이다(구조 변경 2 와 공용).

## 구조 변경 2 — 부작용: 단위 부작용 튜플 + 사건 사전 + 표현 분리
배경: v1.1 `adverse_effect` 는 정규화 문자열이 식별자라 「멍」 4표기가 4개체, 문헌 문장 32 가 32개체다. 분류 축이 없다.
- `adverse_event_type`(사건, 사전 ADV-EVT) 신설 — **값 사전**이다. 뼈대 = complications.json 65 이름을 분해해 얻는 사건 조각(멍·부종·홍반·통증·감염·혈관 폐색·괴사·감각 이상·색소침착(PIH)·결절·육아종·이물반응·실 노출·실 이동·비대칭·반흔·아나필락시스·PAH …). 각 사건에 속성 `category` ∈ {국소 일시 반응, 염증/감염, 혈관, 신경, 색소, 구조/이물, 전신}. 표기 변형은 동의어. **사전 값 하나하나에 출처(파일·키) 필수**. 사전에 없는 조각은 미등록.
- `course`(경과, 사전) 신설: 일시 · 지연 · 영구 · 재발 · 미상. 원장 이름의 「일시적」「지연성」「가역적」「영구」같은 수식어에서 분해.
- `adverse_effect`(단위 부작용, 접두 ADV) 재정의: **튜플 (event, site, course)**. site 는 공유 부위 사전 + 상대 부위 값(`주사 부위`·`시술 부위`) + none. 식별자 = ADV-sha256(event|site|course)[:10]. 같은 튜플 = 같은 단위 부작용. 「혈관 폐색」→「피부 괴사」같은 인과는 R `leads_to`(adverse_effect → adverse_effect) 로.
- R15 `may_cause`(시술 축 → adverse_effect) 유지. **등급·빈도·발생 시기·지속·대처·예방·위험 요인·예상/이상/주의/응급 표시는 전부 엣지 속성**(v1.1 과 같음). 원인 시술은 튜플에 넣지 않는다.
- `adverse_expression`(표현, 접두 AEX) 신설: 문헌 부작용 문장 · 타임라인 문구 · consent/extracted 응급 징후 · 환자 설명(4개 언어)을 담는 원문 레코드. 속성 kind ∈ {evidence_statement, symptom_phrase, emergency_sign, patient_text}, text, lang, 출처, citation(있으면). R `expresses`(adverse_expression → adverse_effect, N:1 | null). 튜플에 닿으면 연결, 아니면 null + 미등록 조각 기록. v1.1 `evidence_statement` 중 adverse_effects 섹션 분은 여기로 옮기고, moa/effects 섹션은 v1.1 그대로.
- 타임라인 `normal` 문구는 부작용 사전에 넣지 않는다. 표현(kind=symptom_phrase)으로 두고 R15 엣지 속성 reaction_level=normal 로 표시.

## 검산 (둘 다 스크립트, 독립 실행)
1. **행선지 전수** — `erd-v2-check.py`: 잎 키 1,072 전부 행선지, 미정 0, 중복 0, v1.1 검산 항목 전부 유지. 옮긴 키(procedure→catalog_item, adverse_effect→adverse_expression 등)는 이동 표로.
2. **튜플 분해 실측** — `erd-v2-tuples.py`: 실제로 돌려서 센다.
   - 시술: 분류 항목 521 + 참조 자리 전부 + market-pricing 122 → 튜플 수 · 분류 항목이 접힌 비율(521 → N 튜플) · what/site/technique 각 축의 미등록 조각 상위 30 · none 비율
   - 부작용: complications 65 + extracted/taxonomy safety 전 문구 + 응급 징후 + 문헌 adverse_effects 32 + 타임라인 abnormal/caution/emergency → 튜플 수 · 65 가 접힌 결과(어떤 이름들이 같은 튜플로 갔는지 전부 표) · 사건 사전 최종 값 수 · 미등록 조각 전부
   - 두 결과를 `erd-v2.md` §9 에 표로. **숫자는 목표가 아니다.** 접힌 결과 표가 사용자가 「같은 게 맞다」고 볼 수 있게 전부 보여야 한다.

## 산출물
`erd-v2.md` · `erd-v2.json` · `erd-v2-column-map.md` · `erd-v2-dictionaries.json`(사건·경과 사전 추가) · `erd-v2-check.py` · `erd-v2-tuples.py` · `erd-v2-tuples.json` · 생성기 `*_v2.py`. v1·v1.1 파일은 지우지 않는다. `erd-v2.md` 끝에 「v1.1 → v2 변경 목록」과 「v2 밖 관찰」절.

## 보고
개체·관계·사전 수 변화 · 행선지 분포 · 시술 튜플 실측(521→N, none 비율, 미등록 상위) · 부작용 튜플 실측(65→N, 사건 사전 수, 미등록 수) · 검산 결과 · v2 밖 관찰 수. 본문 재붙임 금지.
