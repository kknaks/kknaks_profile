# complications.json — 1차 조사 검증 기록

> 기계 검증을 통과했다고 의미 해석이 맞다거나 정규화가 끝났다는 뜻이 아니다. 검증 대상은 **원문 대응**(누락·중복·Pointer·구간·해시·적용/제외)이다.

## 1. 원본 해시 (시작 · 끝)

| 시점 | sha256 | 근거 |
|---|---|---|
| 작업 시작(첫 열람 전) | `7bf0573efa955225f63cc33d96b68a20693ddaac647ee2a0c679c1de32d3d932` | `shasum -a 256 …/complications.json` |
| build.py 시작·끝 | 같음 | [build-output.txt](./build-output.txt) `source sha256=… / end=… unchanged=True` |
| verify.py 시작·끝 | 같음 | verify `recorded_sha256_*` · `source_hash_unchanged_during_verify` |
| 작업 끝(보고 직전) | `7bf0573efa955225f63cc33d96b68a20693ddaac647ee2a0c679c1de32d3d932` | `shasum -a 256` 재실행 |

크기 58,333 bytes, 33,470 code points. BOM 없음, 개행 없음, 백슬래시 이스케이프 0, BMP 밖 문자 0. 원본에 쓰기 작업을 하지 않았다.

## 2. 실행 명령과 결과

레포 루트 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` 에서:

```text
$ uv run --python 3.12 --with kiwipiepy==0.24.1 python orchestration/work/phub-ledger-redesign/first-pass/complications/build.py
source sha256=7bf0573e…d932 bytes=58333 code_points=33470 nodes=781 keys=613 duplicate_keys=0 escapes=0
morphology: analyzed=531 excluded=97 tokens=9697 field_names=18 segmentation_review=107
expressions: total=5061 manual=189 …
observations: 68 (evidence quotes all found)
source sha256 end=7bf0573e…d932 unchanged=True

$ python3 orchestration/work/phub-ledger-redesign/first-pass/complications/verify.py ; echo exit=$?
{ "nodes": 781, "keys": 613, "strings": 628, "analyzed": 531, "excluded": 97, "tokens": 9697,
  "segmentation_flags": 107, "expressions": 5061, "observations": 68,
  "check_kinds": 73, "check_runs": 89629, "failure_count": 0 }
exit=0
```

verify.py 는 build.py 의 스캐너를 쓰지 않는다. 표준 `json` 파서(중복 키는 `object_pairs_hook` 로 감지)로 원본을 다시 읽어 결과 파일과 맞춰 본다. 어떤 파일도 쓰지 않는다. verify 실행 전후로 결과 폴더 전 파일의 해시가 같음을 확인했다.

## 3. 검사 항목 (verify.py)

| 묶음 | 검사 | 결과 |
|---|---|---|
| 원본 식별 | 세 JSON 의 `sha256_start`·`sha256_end`·크기·경로 = 실제 원본 | 통과 |
| 노드 양방향 | 파서가 연 노드 집합 = source-map 노드 집합(누락·초과 0, Pointer 중복 0), 개수 781 = 781 | 통과 |
| 노드 값 | 노드마다 자료형 · `text[span]` 을 `json.loads` 한 값 = Pointer 로 찾은 값 · `byte_span` 디코딩 = 같은 리터럴 · 스칼라 `value`·`literal` · 문자열 `value_span` = 따옴표 안쪽 · 객체 `children` 순서 · 컨테이너 길이 · 문서 순서 | 통과 |
| 키 | 키 출현 613(객체·키·순서) 양방향 일치 · `span` 재현 · `byte_span` · `value_pointer` · 중복 키 0 · `field_name_occurrences` 전수 | 통과 |
| 형태소 적용/제외 | 문자열 628 = 분석 531 ⊔ 제외 97(겹침 0, 누락 0) · 제외 사유 존재와 규칙 일치(id·severity 코드·기호 단독·URL 만) · 코드값이 분석에 없음 · 분석 값 = 원문 · `file_span_of_text` 재현 | 통과 |
| 토큰 | 9,697 토큰 전부 `value[span] = surface` · 구간이 값 안 · 순서 · `form_equals_surface` 정합 · tag·lemma 있음 · 필드명 18 토큰 surface | 통과 |
| 분석기 기록 | kiwipiepy 0.24.1 · model_type cong · num_workers 1 | 통과 |
| 오분절 표시 | 107출현 각각: Pointer 분석됨 · `phrase_span` 재현 · `token_indexes` 의 실제 토큰 = 기록된 원시 토큰 · 규칙과 일치 · 상태 「교정 아님」 · 규칙별 출현 수 = 기록 | 통과 |
| 표현 | 5,061 각각: Pointer 가 문자열 · `value[span] = text` · keyword_span ⊂ span · span ⊂ clause_span · 완전 중복 0 · ID 연번 · 모든 문자열에 `segment.value` · 수동 189 전부 배치 · URL 구간과 겹치는 비분할 후보 0 | 통과 |
| 관찰 | 68건 근거 Pointer 유효 · 인용이 그 값 안에 실제로 있음 · review.md 에 실림 | 통과 |
| review.md 전수 | 카테고리 id·name 을 뺀 문자열 608개가 `\| \`원본 컬럼명\` \| \`Pointer\` \| 원문 값 \|` 한 행으로 그대로 있음 · 카테고리 20값은 제목줄 · 항목 65 제목 · 빈 배열 46행 · 「(키 없음)」 행 수 = 실제 빠진 키 수(73) | 통과 |

## 4. 변이 시험 (검사가 실제로 잡는지)

결과 폴더를 스크래치에 복사하고 한 곳씩 망가뜨린 뒤 `verify.py --source … --dir …` 로 돌렸다(원본·결과 폴더는 건드리지 않음).

| # | 망가뜨린 것 | 결과 |
|---|---|---|
| M1 | 원본 사본 한 글자(「일시적」→「일시작」) | exit 1 · failure 16 — 기록 해시 6 · node_value 1 · node_literal 1 · analyzed_text_matches 1 · token_surface 1 · expr_span_text 4 · expr_keyword_span 1 · review_row_exact 1 |
| M2 | 토큰 하나의 span 끝 +1 | exit 1 · `token_surface` |
| M3 | source-map 에서 노드 하나 삭제 | exit 1 · `node_set_equal`(누락 Pointer 이름까지) · `node_count` |
| M4 | review.md 원문 값 한 칸 줄임 | exit 1 · `review_row_exact` |
| M5 | 제외 기록 하나 삭제 | exit 1 · `morph_cover_all_strings` |
| M6 | 표현 하나의 span 시작 +1 | exit 1 · `expr_span_text` |
| — | 변이 없음(기준) | exit 0 · failure 0 |

## 5. 재현성

build.py 를 두 번 돌렸을 때 source-map · morphology · expressions · review.md 의 해시 묶음이 같았다(`71557fcd0c3409c0` 두 번). Kiwi 는 스레드 1개로 돌렸다.

## 6. 별도 읽기 검토 (작성자 3회차 · 독립 아님)

| 확인한 것 | 방법 | 결과 |
|---|---|---|
| 문맥 보존 | 모든 값이 `segment.value` 로 통째 보존되고, 문장·쉼표 절·괄호 구간이 따로 있음. 표현 후보마다 `clause_span` 이 있음 | 이상 없음 |
| 수식·조건·부정·가능성 탈락 | 표현 후보가 하나도 걸리지 않은 어절 2,331개를 값마다 읽음 | 빠진 표지 보강: 필요시·으로만·가는·얕은·얇은·높은·어려워·달리·우선·기존·최근·병력 등 → keyword 규칙 추가, 범주 comparison_contrast·obligation_recommendation 신설. 남은 어절은 사건·행위·재료·부위 같은 내용어 |
| 오분절 영향 | 의심 품사·시간·부정·가능성·용어 낱말의 출현 249곳 이상을 원문과 나란히 대조 | 57규칙 107출현 표시(issues A1). 표현 추출은 품사를 쓰지 않으므로 오분절이 표현 후보로 번지지 않음 |
| 추출 오류 | regex 결과 열람 | X1~X3 고침(issues 「해결한 추출 오류」), 재실행·재검증 |
| 미검토 | 의미 관계(수식 대상·관계 방향·인과·선후)의 정답 | **검토 안 함** — 후속 F 과제 |

## 7. 한계

- 기계 검증은 원문 대응만 본다. 관찰 문장의 해석, 범주 후보의 정답, 오분절 규칙 밖 토큰의 정확성은 보장하지 않는다.
- 표현 후보 keyword 오탐은 출현별로 판정하지 않았다(issues A2).
- 읽기 검토는 작성자가 직접 했다(issues A4).
