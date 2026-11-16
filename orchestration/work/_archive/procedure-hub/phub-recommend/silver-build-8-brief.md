# 실버 8차 발주 — ERD v3.3 반영 · 원장 3판 · 승인 결정 묶음 6-A (2026-11-06 · 사용자 「erd 발주 하고 빌드 까지 해서 최종 결과 보고해 · fable로」)

읽을 것(순서): `HANDOFF-2026-11-05.md`(원칙 · 11-06 추가 절 전부) → `erd-v3.3.md` §「v3.2 → v3.3 변경 목록」·§5·§9.20~9.24·§12~14 → `erd-v3.3.json`·`erd-v3.3-dictionaries.json`·`erd-v3.3-tuples.json` → `silver-v3/README.md` → `silver-v3/out-dryrun3/report.md` §0·§8(분석기 규칙을 코드로 옮긴 방식 · 빌더 반영 메모) → `silver-v3/dryrun3/`(dry3_au.py · kiwi_t0.py · common2.py — 3차 규칙 구현 · lib 로 옮길 원본) → `silver-v3/lib/v32.py`(AdverseUnits32._apply_cores · Tokenizer.strip · judge_phrase · duplicate_pairs) · `lib/decisions.py`(kind 20 · 적용 순서) · `lib/load.py`.

## 목표
7차(ERD v3.2 · 원장 2판) → **8차(ERD v3.3 · 원장 3판 · 결정 묶음 6-A)**. `python3 build.py --erd ../erd-v3.3.json --dict ../erd-v3.3-dictionaries.json --tuples ../erd-v3.3-tuples.json`(인자 이름은 build.py 실제 인자 확인) → `check.py` ①~⑨ 전부 PASS → `tests/run_tests.py` PASS(enumerate_cases 가 v3.3 json 에서 경우를 다시 뽑음 — 수 변동 보고) → `baseline/manifest-8차.json` 저장.

## 절대 규칙
- 원장 불변(3판 · HASHES 3판 검증). ERD v3.3 파일 수정 금지(틈이 있으면 「ERD 질문」표로). `bronze/phub-ledger-v2/`(2판 복원) 건드리지 않음. 커밋 금지.
- 결정은 **approved 만 빌드가 읽고**, approved 는 아래 6-A 목록만. 그 밖(⑦ 접기 36쌍 분류 · 애매 23 · 문장꼴 15 · 폐색/색전 3 · 묶음3 15 · Mxx- 접두 34 · 의미 동의어)은 **사용자 미결 — 결정 파일 만들지 않는다**(게이트 6 아티팩트에서 사용자가 고르는 중).
- 추정 매칭 0 · 임상 동치 0 · unreviewed 등급 0(새 노드는 정식 노드 · status 필드 자체를 없앤다). 수치는 센 값만.
- 기존 lib 를 고치되 7차 재현성을 깨지 않는다: `python3 build.py --erd ../erd-v3.2.json --bronze ../bronze/phub-ledger-v2 …` 로 돌리면 determinism key 가 `baseline/manifest-7차.json` 과 같아야 한다(분기: ERD json 의 erd_version 으로 v3.2 경로/v3.3 경로를 가른다). 끝에 이 7차 재현을 실제로 돌려 보인다.
- 분석기(kiwipiepy)는 `.venv-kiwi` 에만 있다. build.py 는 시스템 python3 로 돌아야 하므로 **분석기 호출은 `.venv-kiwi/bin/python` 서브프로세스**(입력 문구 전부 → 품사열 JSON 캐시 `out/kiwi-cache.json` · 캐시 키 = 판 + 사전 등록 해시 + 문구 정규화형)로 감싼다. 캐시가 있으면 venv 없이도 재현된다(④ 재실행 바이트 동일 유지). kiwipiepy 판 0.24.1 고정 확인.

## 반영 항목
1. **ERD v3.3 로드**(load.py · rule_data): R36 component_of · product.kind/component_of/component_kind(값 0 · 엣지 0 · 보고에 0 명시) · what_kind component 분기(실제 발생 0) · category 삭제(사전·adverse_effect 속성 event_category·dictionary_add/event_split new_value·report7/gate5 의 category 참조 10자리 전부 — grep 으로 전수 · 남으면 실패) · 사전 「폐색」(옛 「혈관 폐색」 id alias · decomposed_from) · site 동맥·정맥·안동맥 · 7차 산출 (혈관 폐색, none) 단위가 (폐색, 혈관) 로 바뀌는지 확인 · 폐색≠색전(⑦ 쌍 0 · 같은 단위 0 검증).
2. **토큰화 = 분석기(V3.3-B)**: dryrun3 의 T0(사전 값 사용자 단어 · phrase_dictionary 제외) · T1(명사 + N1 ㅁ/음 명사형 · ANOM 통째 명사 · 조사/연결어미 붙은 토막 불가) · T2(N2 절 판정 · 관형어 하나 = R1 수식어 · (a)/(b)) · T3(괄호 라틴·수치) · T4(--/—/: 뒤 서술) · R2 (구조·부위 말 → 부위 칸 · 붙은 꼴 포함 · N4 부위 값은 이제 사전) · R1(「이상」 제외 · dryrun3 §3.4 의 새 R1 후보 21 은 **적용하지 않음** — ERD 규칙 데이터가 아니므로 「R1 후보」 게이트로만) · R3 · R4 를 `lib/`(새 모듈 `lib/adverse33.py` + v32 의 분기) 로 옮긴다. 기존 Tokenizer.strip 목록은 analyzer_assist 로만. 문장꼴(b) 문구는 노드 없이 phrase_dictionary status=sentence 로 보존(게이트 6 에서 사용자가 행선지 고름).
3. **결정 묶음 6-A**(`decisions/batch6a/` · approved · decided_by 사용자 · reason 에 사용자 말 인용 · HANDOFF 11-06 절에서):
   - dictionary_add site 15(눈밑·눈꺼풀·코끝·목주름·얼굴 전체·바디 전체·복부·옆구리·팔뚝·허벅지·종아리·힙·가슴·겨드랑이·두피 · kind·parent 는 ERD v3.3 site 규칙 · locator 는 erd-v3.3 §9.21 표) — 「부위는 일단 추가 해야하는게 맞지」
   - dictionary_add ingredient_material 6(HA·히알루론산·TCA·글리콜산·살리실산·페놀 · HA↔히알루론산은 한 값+동의어인지 ERD 사전 규칙대로)
   - fold_approve 20(~감·증·형성 쌍 · erd-v3.3 §1.5 표 · keep = 현상 이름 · 자극감 은 ERD D 대로 canonical_rename 동반) — 「응 같다고 하자」
   - dictionary_add product_name 동의어 7: 더채움프리미어→더채움 · 엘라비에프라임→엘라비에 · LDM초음파관리→LDM · 더마펜→더마펜4 · 민트→민트리프트 · 인모드FX→인모드 · 알렉→알렉산드라이트
   - **만들지 않음**: 미라클필링/레스틸렌스킨부스터(짝 안 지음 — 노드/항목 그대로) · 울쎄라급·울트라·피코(미해결 유지 + 메모는 report 에만) · ⑦ 36쌍 · 접두 34.
4. **게이트 6 재계산**(`out/gate/batch6.json/.md`): 8차 뒤 남는 자리 — 새 사건 노드(종류 질문 없음 · 목록만) · ⑦ strong 쌍(접미사 20 닫힌 뒤) · 문장꼴(b) · 애매 · 폐색/색전 · 묶음3 15 · R1 후보 21 · Mxx- 34. **자리 수를 묶음별로 센 표**. 추천 칸은 원장이 말할 때만.
5. **보고**(`out/report.md` §16 8차 + 종료 메시지 60줄 안): 결정 적용 로그(6-A 48건 전부 적용·거부 0) · 개체·관계 7차→8차 표 · 부작용: 사건 노드 수(사전 + 새) · 단위 수 · 문구 2,285 분포(exact/new/sentence/memo · 사건 칸 비는 수 0) · (폐색, 부위) 단위 표 · category 참조 0 · 분석기 캐시 크기·판 · check ①~⑨ · tests 경우 수 · 7차 재현 key 일치 · 게이트 6 자리 표 · 「ERD 질문」표(v3.3 문장으로 구현이 안 갈리는 자리 · 코디가 ERD 로 돌려보낼 것).
