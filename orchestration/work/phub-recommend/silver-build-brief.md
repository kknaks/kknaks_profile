# 실버 빌드 1차 발주서 — WP-S1 (사용자 승인 2026-11-04 「동결 실버빌드 하자」)

## 목적
동결된 ERD v2.4(`ERD-FROZEN.md`)대로 브론즈 22개를 **실버 레코드**로 빌드하는 결정론 빌더를 만들고, 1차 빌드를 돌려 게이트에 올릴 목록(미해결 · 미등록 · 미연결 · 충돌)과 **결정 묶음 1 제안**을 낸다. 사용자가 결정을 승인하면 같은 빌더로 2차를 돌린다.

## 입력 (읽기 전용)
- 브론즈: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/*.json`(21) + `step1-products.json`(이 폴더 · 22번째 · 조사 산출물). SHA256 은 `erd-v2.4.json → source_files` 와 일치해야 하며 다르면 빌드 거부.
- ERD: `erd-v2.4.json`(규칙·개체·관계·결정 kind·적용 순서) · `erd-v2.4-dictionaries.json`(사전) · `erd-v2.4-tuples.py`(분해 규칙의 참조 구현 — 같은 입력에 같은 튜플이 나와야 함) · `erd-v2.4.md`(사람용 정본, 규칙 해석이 갈리면 md 가 이김).
- 결정: `erd-v2.4.json → review_dispositions`(또는 그 안의 decision 레코드 25). **status=approved 만 읽는다.**
- **금지**: step2·step3·source-map·DATA-001·DEC-*·silver-* 폴더·silver-batch1-candidate·silver-entity-graph-design·`_archive/`. 이전 실버 설계·값을 가져오지 않는다.

## 산출물 — 새 폴더 `silver-v3/`
```
silver-v3/
  build.py                 # 진입점. python3 build.py --bronze <dir> --erd erd-v2.4.json --dict ... --decisions decisions/ --out out/
  lib/                     # 모듈: load(브론즈·해시검증) · normalize · decompose(= erd-v2.4-tuples.py 와 같은 결과) · entities · relations · conflicts · decisions(적용 ①~⑦) · provenance · report
  decisions/               # 결정 레코드 저장소. 파일 하나 = 레코드 하나(JSON). 빌드는 approved 만 읽음
    _bootstrap/            # ERD 가 이미 approved 로 둔 19건을 파일로 옮긴 것
    proposed/              # 결정 묶음 1 제안(아래) — status=proposed, 빌드가 읽지 않음
  out/                     # 1차 빌드 결과 (재실행하면 바이트 동일)
    manifest.json          # 입력 해시 22 · ERD 해시 · 결정 적용 목록 · 빌드 시각 제외한 결정론 키
    entities/<type>.jsonl  # 개체 21종 각각. 레코드마다 id · 속성 · aliases · provenance[](file, path) · status
    relations/<R#>.jsonl   # 관계 31종. from · to · target_depth · 엣지 속성 · provenance[]
    dictionaries.json      # 적용된 사전(결정 ① 반영 후)
    conflicts.jsonl        # kind ⑥⑦⑧⑨ + ④ auto_resolved_by_trust. stable_key · values[] · status
    gate/                  # 사람이 볼 목록
      unresolved_references.md/.json   # 자리별 · 참조 문자열 · 조각 · 후보(사전 일치 후보 ≤3, 근거 명시 · 추정 금지)
      unregistered_fragments.md/.json  # 조각 · 횟수 · 등장 자리 · 축 후보
      unlinked_expressions.md/.json    # 표현 · kind · candidates
      catalog_partial.md/.json         # 항목 자신이 시술인 472 · candidate_name
      conflicts.md                     # open 충돌 · auto_resolved 요약
    report.md              # 수치 요약 + ERD 실측(erd-v2.4-tuples.json)과의 대조표
  check.py                 # 아래 검산
  README.md                # 실행법 · 결정 파일 형식 · 재빌드 절차
```
저장 형식은 JSON/JSONL 파일(기본값 · 사용자 미결정). DB 적재는 골드 설계에서.

## 규칙 (ERD 가 정본 · 여기 요약은 안내)
- **모든 값은 provenance 를 가진다.** 원장 locator(file:key path[index]) 없는 값은 빌드 FAIL. 파생 값(id·튜플·정규화)은 `derived_from` 으로 원 locator 를 가리킨다.
- 원장은 읽기만. 교정은 결정 레코드로만.
- 분해·접힘은 `erd-v2.4-tuples.py` 와 **같은 결과**(시술 521·튜플 수·부작용 57·exact 651 등 erd-v2.4-tuples.json 의 요약 수치와 1차 빌드 수치가 일치해야 함 — 결정 ①~⑦ 적용 전 기준). 다르면 FAIL 이고 어느 쪽이 틀렸는지 report 에.
- 충돌 ④ 자동 해결도 레코드. ⑥ open · ⑦ duplicate_candidate · ⑧ unregistered_value · ⑨ unresolved_reference.
- 결정 적용 순서 ①~⑦ · 같은 단계는 decided_at 순 · 파생 id(PRC-/ADV-/CFL-)를 target 으로 쓰는 결정은 거부.
- 빈값: 원장에 없음 = null · 명시적 빈 목록만 [].
- 재실행 = 바이트 동일(타임스탬프는 manifest 밖).

## 결정 묶음 1 제안 (`decisions/proposed/` · 빌드는 읽지 않음 · 사용자 승인용)
사람이 보고 approved 로 바꿀 파일을 **기계가 근거와 함께** 만든다. 추정 금지 — 각 제안에 원장·조사 근거 locator 필수.
1. `dictionary_add` — 제품 사전 확장: step1 395 중 `1_identity.kind` 가 제품·장비·제품(의료기기)·제품(의약품)이고 허가/웹 근거 locator 가 있는 것 → 제품 정준값 + search_names 동의어. 「확인 불가」「병원 메뉴명」「업체명」은 제외하고 별도 목록.
2. `dictionary_add` — 동의어: 미등록 조각 상위(전체얼굴·풀페이스 → 부위 「얼굴 전체」 · HIFU/RF/MTS/필링/LED/토닝/크라이오/HIFES/수액/줄기세포/CO2/Nd:YAG/혈관레이저/다이오드 → 해당 하위분류 라벨 · HA/CaHA/PLLA/PCL/PDO → 성분 사전) — **각 조각이 원장 어디에 어떤 라벨로 있는지 locator 를 붙인다.** 근거가 없는 조각(지방분해 등 둘 이상 후보)은 제안하지 않고 unregistered 목록에 둔다.
3. 수식어 제외 목록(회·차·터치업·유지·집중·연말·하반기·가을·관리·케어·과도한·빈도)은 사전이 아니라 `resolve_rules.stopwords` 제안으로 — ERD 규칙 데이터 변경이므로 **ERD 개정 후보**로 report 에만 적고 결정 파일로 만들지 않는다.
4. 기존 결정으로 넘긴 목록(`ERD-FROZEN.md` 마지막 절)은 각각 어떤 kind 로 적을지 **빈 템플릿**만 만든다(값은 사람이).

## 검산 `check.py`
① 입력 해시 22 일치 ② provenance 없는 값 0 ③ 1차 수치 = erd-v2.4-tuples.json 요약(차이 0) ④ 재실행 바이트 동일 ⑤ 결정 적용: _bootstrap 19 전부 적용 로그 · proposed 0 적용 ⑥ 파생 id target 결정 0 ⑦ 모든 엣지 끝이 존재하는 레코드를 가리킴(깨진 참조 0 · unresolved 는 conflict ⑨ 로) ⑧ 사전 값마다 출처 ⑨ gate 목록 합 = conflicts.jsonl 의 ⑦⑧⑨ 수.

## 작업 방식
- 코드는 Python 3 표준 라이브러리만(의존성 추가 금지). 이 레포 `app/back/` 규약과 무관한 독립 스크립트.
- 시작 전에 `erd-v2.4-tuples.py` 를 읽고 그 분해 로직을 lib/decompose 로 옮긴다(복붙이 아니라 모듈화 · 결과 동일 검산).
- 막히는 규칙 해석은 추측하지 말고 report 「해석 보류」절에 적고 그 값은 unresolved 로.
- 임시 파일은 `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile-----------/f4798840-05cc-4695-94d0-decfad37f126/scratchpad/`. 커밋하지 않는다.

## 보고
빌드 수치(개체별 레코드 수 · 관계별 엣지 수 · 충돌 kind 별 수 · gate 목록 4종 건수) · ERD 실측 대조 결과 · 결정 묶음 1 제안 건수(제품/동의어) · 해석 보류 수 · check.py 결과. 본문 재붙임 금지.
