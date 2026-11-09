# procedure-comparison.json — 검증 기록

**1차 수집 범위 종료: 충족(작성자 판정, 코디 확인 전)** · **원장 전체 완료 아님** — 원문 부족 B 9묶음, 후속 의미 조사 F 7묶음, 알려진 형태소·표현 한계 A1~A4가 열려 있다. 사용자 선택 대기 0건. 의미 조사·정규화는 시작하지 않았다(batch-01 묶음 검토 §3.2 형식 비고 반영, 상세는 review.md §7).

기계 검증은 **원문 대응**(누락·중복·포인터·구간·해시·적용/제외)을 확인한다. 의미 해석이 맞다는 보장이 아니다.

## 1. 실행한 명령과 결과 (2026-11-09, 레포 루트)

```sh
# 원본 해시(시작)
shasum -a 256 orchestration/work/phub-recommend/bronze/phub-ledger/procedure-comparison.json
# → eba7ae5af919ef77ff52cb07b2f6117b458751319f530f38cf30c61e94989571  (HASHES.txt 앞 16자리 eba7ae5af919ef77 와 일치)

# 생성(재현)
uv run --python 3.12 --with kiwipiepy==0.24.1 python \
  orchestration/work/phub-ledger-redesign/first-pass/procedure-comparison/build.py
# → build-output.txt: nodes 533 · keys 473 · dups 0 · strings 471 · analyzed 343 · excluded 128 · tokens 2127
#   · auto_flags 442 · seg_review 52 · expressions 2181 · uncovered 81 · manual_nohit [] · seg_errors [] · rev_unused [] · failures []

# 독립 검증(표준 라이브러리만, 파일을 쓰지 않음, 실패 시 exit 1)
python3 orchestration/work/phub-ledger-redesign/first-pass/procedure-comparison/verify.py
# → failure_count 0, exit 0
#   counts: nodes 533 · tokens 2127 · zero_length_tokens 2 · segmentation_occurrences 52 · expressions 2181 · review_leaf_values 471

# 원본 해시(끝) — 위와 동일 eba7ae5a…89571
```

오분절 출현 기록 갱신 순서(서명을 바꿀 때만): `build.py` → `python3 …/make-segmentation-review.py` → `build.py`.

## 2. build.py 내부 검사 (validation-machine.json, failure_count 0)

| 검사 | 결과 |
|---|---|
| hash_unchanged — 시작·끝 sha256 동일 | 통과 |
| no_duplicate_keys — 자체 파서가 객체마다 키 중복 감지 | 통과(0) |
| node_span_reparse — 노드마다 `span` 리터럴을 다시 파싱하면 Pointer 로 찾은 값과 같다 | 통과 533/533 |
| bidirectional_pointer_set — 원본을 따로 걸어 얻은 경로 집합 = 노드 집합(개수도 동일) | 통과 |
| morph_partition — 문자열 값 = 형태소 적용 ∪ 제외(서로소) | 통과 343 + 128 = 471 |
| token_surface_reproduces — 토큰 span 으로 자른 원문 = surface | 통과 |
| segmentation_review_matches_tokens — 표시한 출현의 토큰·구절 구간이 실제 토큰·원문과 일치 | 통과 52 |
| manual_expressions_all_hit — 수동 표현 331개 모두 원문 출현 ≥1 | 통과 |
| expression_review_all_used — 판정 48건 모두 실제 후보에 대응 | 통과 |
| expr_span_reproduces — 표현 후보 span = text | 통과 2,181 |
| every_value_has_segment — 분석 값마다 값 전체 구간 후보 | 통과 343 |

## 3. verify.py 독립 검사 (build 코드 미사용)

| 범위 | 확인 내용 |
|---|---|
| 해시 | 현재 원본 sha256 = 상수 기대값 = 세 산출물의 start/end 기록. 크기·코드포인트·이스케이프 수 기록 일치 |
| 원본 중복 키 | `json.loads(object_pairs_hook=…)` 로 별도 감지 — 0 |
| 노드 → 원문 | Pointer 해소, 자료형, `span` 재파싱, `byte_span` = 코드포인트→바이트 재계산, 바이트 구간 디코드 = 리터럴, 값·리터럴·길이·객체 키 순서, 문자열 `value_span` 경계와 `decoded_equals_literal_interior` 값 |
| 원문 → 노드 | 원본을 따로 걸어 얻은 경로 전부가 노드에 있고 개수 동일, 노드 Pointer 중복 없음, 키 출현 수 = 객체 키 총수, 키 구간 재파싱 = 키 |
| 필드명 | 필드명 집합·출현 합계 = 원본 키 |
| 형태소 | 적용·제외 서로소·합집합 = 문자열 값, 분석기 버전 0.24.1·cong·num_workers 1 기록, 값 텍스트 = 원본, 파일 구간 재현, 토큰 경계·surface 재현(길이 0 토큰 2개 허용), **토큰이 덮지 않은 비공백 문자 0** |
| 오분절 표시 | morphology 의 표시 수 = segmentation-review 수, 구절 구간 재현, 표시 토큰이 그 값의 실제 토큰 |
| 기계 표시 | auto_flags 토큰이 실제 토큰 |
| 표현 | span 재현, id 유일, (pointer, span, 범주, 방법) 완전 중복 없음, source_token 실재, 분석 값마다 값 전체 후보, 판정 항목이 실제 후보에 있음, 수동 표현 전부 출현 |
| review.md | **말단 값 471개 모두** 그 Pointer 가 적힌 줄에 원문 값(Markdown `\|` 이스케이프만 적용)과 원본 컬럼명 `\| key \|` 이 함께 있다 |

## 4. 재현성·변이 시험

- 재현성: build.py 를 두 번 돌린 뒤 source-map.json·morphology.json·expressions.json·review.md·validation-machine.json 의 sha256 이 같았다(`REPRO_SAME`).
- 변이 시험: 결과 폴더를 scratchpad 로 복사해 하나씩 망가뜨린 뒤 복사본 verify.py 실행(원본 결과 폴더는 건드리지 않음). 모두 exit 1 로 잡혔다.

| 변이 | 검출 메시지(첫 항목) |
|---|---|
| M1 토큰 span 끝 +1 | `token surface /comparisons/0/evidence_notes/3` |
| M2 노드 하나 삭제 | `bidirectional nodes 533 vs 532` |
| M3 review.md 값 「3-7일 부종/멍」→「3-7일 부종」 | `review.md value missing /comparisons/0/procedures/2/downtime` |
| M4 표현 text 변형 | `expr span E00011` |
| M5 제외 기록 하나 삭제 | `morph partition` |
| M6 오분절 표시 토큰 구간 변형 | `seg token /comparisons/0/evidence_notes/3 RCT` |

## 5. 별도 읽기 검토 (같은 에이전트, 관점을 바꿔 다시 읽음 — 독립 검토 아님)

| 관점 | 한 일 | 결과 |
|---|---|---|
| 모든 구획 문맥 보존 | review.md §3 이 9개 비교군 × 모든 필드를 원본 컬럼명·Pointer 와 함께 보여주는지 확인. evidence_notes 없는 6개 비교군은 「키 자체가 없다」로 명시 | 누락 0(verify 의 review 검사와 일치) |
| 수식·조건·부정·가능성·범위·시간 | §4.3 표 8유형을 원문 구절 단위로 manual 후보에 넣었는지, 형태소만으로 사라지는 곳을 서명으로 표시했는지 대조 | 「드물지만」「(반복 시)」「(과다 시)」「아님」「안 됨」「부재」「가능」「경향」「기대되나」「>」「%+」「항노화」 모두 원문 구간 보존 |
| 오탐 | condition_scope 의 「즉시」9·「-지만」의 「만」7, CO2 의 「2」4, 「1차」의 「1」1, manual 의 「볼(볼륨)」9·「HA(BHA)」1 등 | 오탐 32 표시, 삭제 안 함 |
| 잠정 해석 근거 | §4 의 각 관찰에 Pointer 를 붙였는지, 원문에 없는 단위·백분율·뜻·부위를 채우지 않았는지 | 채운 것 없음. 불일치 후보(B7, F5)는 어느 쪽이 맞는지 정하지 않음 |
| 미검토 | 시술 간 관계·조합의 의미·부위 역할·카테고리 의미 | 1차에서 검토하지 않음 → F1~F7 |

## 6. 한계

- 기계 검증 통과는 원문 대응이 맞다는 뜻이다. 형태소 정답·의미 해석 정답·정규화 완료를 뜻하지 않는다.
- NNP 110건은 출현별로 판정하지 않았다(issues A2). 확인한 오분절 52출현 밖의 형태소 정확성은 보장하지 않는다.
- 독립 검토자는 없었다.
