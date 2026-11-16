# 레코드 스키마 — `step2-families.json`

`step2-apply.py` 가 쓰는 칸을 풀어 쓴 것과 실제 행 발췌다(재검수 v5 PASS 판). 칸을 새로 만들지 말고 이 칸에 넣는다.

## 파일 최상위

| 칸 | 무엇 |
|---|---|
| `version` · `generated_by` · `inputs[]` · `decision` · `rules[]` | 판 · 만든 스크립트 · 입력 고정본 · 근거 결정 · 규칙 요약 |
| `summary` | `families` · `rows` · `verdicts{맞음, 옮김, 여러, 계열 밖, 판단 필요}` · `by_family` · `changed_rows`(주 계열 ≠ 1단계 `step1_code`) · `open` · `pending_director` · `evidence_weak` · `conflicts` · `out_of_family` · `this_apply_changed_rows` — **반영 때마다 스크립트가 다시 센다** |
| `families[]` | 계열 18(아래) |
| `product_family[]` | 제품 행 → 계열(아래). 1단계 active 행과 1:1 |
| `out_of_family[]` | 계열 밖 행 `{ledger_id, display_name, kind, basis}` — `kind` = 의약품(D02) · 진단 장비(D12) · 단독 기기(D16) |
| `open[]` | 값이 안 정해진 칸 — **끝 조건 = 빈 목록** |
| `pending_director[]` | 원장님 문의 `{ledger_id, display_name, question, if_confirmed, researched_value, researched_basis, sources[], status}` |
| `research_errata{}` | 조사 파일 추천 칸을 메모대로 정정한 행 `{display_name, research_field, applied, research_note, tag}` |
| `source_fix_candidates[]` | 1단계 · 원천 값이 틀린 것(1단계는 고정이라 기록만) `{ledger_id, display_name, field, value, conflict, action}` |
| `v2_delta[]` · `v3_delta[]` · `v4_fix[]` | 판마다 바뀐 행 표 — 회귀 검사용. 새 반영도 같은 모양의 `*_delta` 를 하나 더 남긴다 |

## 계열 (`families[]`)

| 칸 | 무엇 | 비고 |
|---|---|---|
| `id` | M1~M17 · N1 | 문헌 카테고리 코드. 새 계열은 N2 … |
| `name` · `name_status` · `name_basis[]` | 계열 이름 · 상태(확정 · 국내 공식 출처 · 공식 출처 미확인 · 품목명 일부만 해당) · 출처 | 규칙 「이름」 |
| `literature_name` | 문헌 영문 이름 | `literature-evidence.json categories.<id>.name` |
| `definition` | 한 문장 정의 | 「무엇을 · 어떻게 넣어/쏘아 · 무엇을 일으키는 시술」 |
| `literature_evidence[]` | `{path, statement, pmid, doi, title, role}` · 새로 찾은 문헌 `{pmid, doi, title, journal, year, quote, verified}` · 반영 결정 `{decision}` | PMID 는 NCBI ESummary 로 실재 확인 |
| `synonyms[]` | 상담 용어 · 원천 이름 · 영문 | 제품 · 장비 이름은 「(장비 이름)」 꼬리 |
| `sub_families[]` | 하위 칸 — 「무엇으로」 한 축(재질 · 매질 · 에너지) | M8 은 실제로 쓴 매질만 남는다 |
| `sub_family_handling[]` | 원천 하위 → 행선지 `{source, handling, basis}` | 판마다 쌓인 기록 — 지금 규칙과 다른 줄이 있다(families.md M8 ⚠) |
| `deferred[]` | 3 · 4 · 5 · 6단계로 넘긴 것 `{source, deferred_to, handling, basis}` | 표시만 |
| `new_family` · `note` | 2단계에서 세운 계열인가 · 메모 | N1 만 true |

## 제품 행 (`product_family[]`)

| 칸 | 무엇 | 비고 |
|---|---|---|
| `ledger_id` · `display_name` | 1단계 행 id · 대표 이름 | 1단계와 같은 값. 바꾸지 않는다 |
| `family` · `family_name` | 주 계열 코드 · 이름 | `families[].id` · 「계열 밖」 · null(원장님 문의만) |
| `also_families[]` | 보조 계열 코드 | 주와 겹치지 않음 |
| `sub_family` · `sub_family_basis` | 주 하위 칸 · 근거 문장 + 「출처: …」 | 칸은 그 계열 `sub_families` 에 있어야 한다. 하위 칸 없는 계열은 null + 「이 계열은 하위 계열 없음(D18)」 |
| `also_sub_families[]` | 보조 하위 `{family, sub_family}` 객체 | 같은 계열 보조도 family 를 적는다. family 는 주 또는 보조 계열 |
| `technique_hint` | M8 방식 — 적힌 말 그대로 배열 | 4단계 재료. 판정에 쓰지 않는다 |
| `basis` · `note` | 계열 판정 근거 한 줄(「원천 › 하위 「설명」 · 허가 품목 「…」 ↔ 정의」) · 메모 | |
| `step1_family` · `step1_code` | 1단계 `family.name` · 그 이름의 M 코드(`step2-apply.py` `step1_code()` — `family.code` 가 아니라 이름에서 읽는다) | **지금 계열은 이 파일의 `family` 한 곳에서 읽는다.** 1단계 `family.code` 는 원천 위치일 뿐이다 — 코드 ↔ 이름이 다른 4행에서 조사가 틀렸다(기록 §5-4 · `check_families.py` `step1_code_name_split`) |
| `verdict` | 맞음 · 옮김 · 여러 · 계열 밖 · 판단 필요 | 여러 = 보조 계열 있음 |
| `bundles[]` | 결정 묶음 id(D01~D18) | 새 반영은 새 묶음 id |
| `auto` | 원천 자동 병합 행(`auto-…`) | 오배치 의심 1순위 |
| `conflict` | 허가 ↔ 원천(또는 출처끼리) 충돌 한 줄 | 지우지 않는다 · 원천 수정 근거 |
| `evidence_level` | null · 강 · 약 | 해결안에서 들어온 값만 강/약 |
| `confirm_question` | 근거 약 · 원장님 문의 행의 질문 | 약이면 필수 |
| `pending_director` | 정체 미확인 → 원장님 문의 | true 면 family null |
| `resolve_rule` | 해결안 적용 규칙 이름 | open 해결 행에만 |

## 입력 파일의 행 (갱신할 때 손대는 곳)

`step2-apply.py` 는 이 두 파일을 입력으로 고정하고 결정대로 결정론 적용한다.

`step2-research.json` `rows[]` — 계열 판정 1행:

```json
{"ledger_id": "M1-2-1", "display_name": "보톡스", "auto": false, "current_family": "M1 보톡스", "current_code": "M1",
 "verdict": "맞음", "recommended_family": "M1", "also_families": [],
 "basis": "원천 M1 › 수입 「오리지널 보톡스, 900kDa 복합체 제형」 · 허가 품목 「전문의약품」 ↔ M1 정의", "bundles": []}
```

`step2-open-resolve.json` `rows[]` — open 1행의 해결 값:

```json
{"ledger_id": "auto-17-1774737181584", "display_name": "리투오", "group": "칸이 없던 것", "open_type": "sub_family",
 "now": {"family": "M4", "sub_family": null, "reason": "D07 은 M4 편입만 결정 — M4 하위(HA · PN · 콜라겐 · 복합)에 hADM 하위 없음"},
 "resolve": {"family": "M4", "also_families": [], "sub_family": "무세포동종진피(hADM)", "also_sub_families": [],
             "new_sub_family": "M4 「무세포동종진피(hADM)」 — 원천 M3 하위 이름 그대로"},
 "basis": "원천 하위 「무세포동종진피(hADM)」(taxonomy M3-new-1774324237649) · …", "sources": ["taxonomy.json modality M3 subcategories 「무세포동종진피(hADM)」"],
 "level": "강", "why_weak": null, "ask": null, "conflict": null, "note": null, "rule": "브리프 「칸이 없던 것」 · D07"}
```

## 실제 행 발췌

**맞음 · 하위 주 + 보조(매질 둘)** — 젠틀맥스 프로

```json
{"ledger_id": "auto-M8-1775362612108", "display_name": "젠틀맥스 프로", "family": "M8", "also_families": [],
 "sub_family": "알렉산드라이트 레이저",
 "sub_family_basis": "허가 품목 「알렉산드라이트레이저수술기」 = 주 · 원천 설명 「알렉산드라이트(755nm)와 Nd:YAG(1064nm)」 = 보조 · 출처: …",
 "also_sub_families": [{"family": "M8", "sub_family": "엔디야그 레이저"}],
 "step1_family": "M8 레이저 · 제모", "step1_code": "M8", "verdict": "맞음", "evidence_level": "강",
 "resolve_rule": "_RESUME.md §2 2026-10-28 「하위 계열도 주 · 보조로」 — 주 = 허가 품목 매질 → 없으면 원천 설명 첫 매질"}
```

**여러 · 주 계열 + 보조 계열(복합 장비)** — 바넥스프로

```json
{"ledger_id": "auto-M10-1775361916636", "display_name": "바넥스프로", "family": "M10", "also_families": ["M9"], "sub_family": "EMS",
 "basis": "원천 「RF 고주파, EMS 근육자극, 석션」 — 근육 자극 있어 M10 주, RF 는 M9 · 지방 감소는 목적",
 "verdict": "여러", "bundles": ["D11"]}
```

**여러 · 보조 하위가 다른 계열** — 바이리즌(라인 허가 2건)

```json
{"display_name": "바이리즌", "family": "M4", "also_families": ["M2"], "sub_family": "폴리뉴클레오타이드(PN·PDRN)",
 "also_sub_families": [{"family": "M2", "sub_family": "히알루론산(HA)"}], "verdict": "여러", "bundles": ["D15"]}
```

**옮김 · 새 하위 칸(원천 이름 그대로)** — 리투오

```json
{"display_name": "리투오", "family": "M4", "sub_family": "무세포동종진피(hADM)", "step1_family": "M3 바이오스티뮬레이터/콜라겐부스터 · 무세포동종진피(hADM)",
 "basis": "원천 … 「콜라겐 생성을 ‘유도’하는 것이 아니라 구조 자체를 ‘직접 보충’」 ↔ M3 정의 collagen-stimulating 과 반대 · M4 문헌(39544509)은 … hADM 직접 언급은 없음(본문 검색 0)",
 "verdict": "옮김", "bundles": ["D07"], "evidence_level": "강"}
```

**옮김 · 새 계열** — 벨카이라 (`step1_code` null — 1단계 이름에 M 코드가 없던 행)

```json
{"display_name": "벨카이라", "family": "N1", "sub_family": null, "sub_family_basis": "이 계열은 하위 계열 없음(D18)",
 "basis": "원천 M16-DCA 「데옥시콜산(DCA)이 지방세포막을 … 파괴」 ↔ M16 문헌 정의는 정맥 미량영양소 — 투여 경로(피하)·작용(지방세포 용해)이 다름 · 27785706",
 "step1_family": "피하 지방분해주사 (원천 시술군 M16)", "step1_code": null, "verdict": "옮김", "bundles": ["D01", "D10"]}
```

**옮김 · 하위 없음(기기)** — 큐어젯

```json
{"display_name": "큐어젯", "family": "M4", "sub_family": null, "sub_family_basis": "D05 「M4 의 제품(기기) — 하위 계열 아님 · 「어떻게」는 4단계 기법」",
 "step1_family": "M15 메디컬스킨케어 · 주입장비 (원천 시술군 M15)", "verdict": "옮김", "bundles": ["D05"]}
```

**근거 약 + 충돌** — 실루엣소프트

```json
{"display_name": "실루엣소프트", "family": "M7", "sub_family": "PLLA",
 "conflict": "PLLA(유럽 자료) ↔ PLGA(미국 InstaLift 자료)", "evidence_level": "약",
 "confirm_question": "국내 실루엣소프트(수허 15-878) 실 재질이 PLLA 인가요, PLGA 인가요?"}
```

**충돌 · 허가가 이김** — 셀렉V

```json
{"display_name": "셀렉V", "family": "M8", "sub_family": "IPL", "also_sub_families": [{"family": "M8", "sub_family": "엔디야그 레이저"}],
 "technique_hint": ["Q-switched"], "conflict": "허가 IPL ↔ 원천 설명 Q-switched Nd:YAG — 원천 설명 확인 대상", "evidence_level": "강"}
```

**계열 밖** — 아큐탄

```json
{"display_name": "아큐탄", "family": "계열 밖", "family_name": "계열 밖", "sub_family": null,
 "basis": "원천 여드름 전용 「경구 이소트레티노인」 — 먹는 처방약(전신 약물치료), 시술 아님 · 37649956", "verdict": "계열 밖", "bundles": ["D02"]}
```

**원장님 문의(정체 미확인)** — 알렉스필 · 행과 최상위 `pending_director[]` 둘 다

```json
{"display_name": "알렉스필", "family": null, "sub_family": null, "verdict": "판단 필요", "bundles": ["D16"], "pending_director": true,
 "basis": "원천 케미컬필링이나 설명이 「알렉산드라이트 레이저의 755nm 파장이 멜라닌에 … 흡수」 — 필링 제품인지 레이저 시술 이름인지 원천 확인 필요(M15 ↔ M8)",
 "confirm_question": "「알렉스필」은 알렉산드라이트 레이저로 하는 시술 이름인가요(바르는 필링이 아닌)?"}
```

```json
{"display_name": "알렉스필", "question": "…", "if_confirmed": "바르는 필링이면 M15 「화학 박피」 · 알렉산드라이트 레이저 시술이면 레이저 시술 이름 → 5단계(시술 이름)",
 "researched_value": {"family": "M8", "sub_family": "알렉산드라이트 레이저"}, "status": "원장님 문의 · family null · 추천 제외(1단계 확인 불가 그대로)"}
```

조사 값(`researched_value`)이 있어도 원장님 답 전엔 행에 넣지 않는다.
