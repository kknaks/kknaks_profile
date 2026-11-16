# pih-risk.json — 검증 기록 (1차)

기계 검증 통과는 **원문 대응(누락·중복·Pointer·구간·해시·적용/제외·구획 소유)** 이 맞다는 뜻이다. 의미 해석의 정답이나 정규화 완료를 뜻하지 않는다.

## 1. 실제 실행한 명령 (레포 루트 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`)

```bash
# 빌드 (재현) — 원본은 읽기만, 시작/끝 해시 비교
uv run --python 3.12 --with kiwipiepy==0.24.1 python \
  orchestration/work/phub-ledger-redesign/first-pass/pih-risk/build.py \
  > orchestration/work/phub-ledger-redesign/first-pass/pih-risk/build-output.txt

# 독립 검증 — 표준 라이브러리만, 파일을 쓰지 않음, 실패 시 exit 1
python3 orchestration/work/phub-ledger-redesign/first-pass/pih-risk/verify.py
#   (validation-machine.json 은 위 명령의 stdout 을 저장한 것)
```

결과: `exit=0` · `failure_count 0` · 검사 77 종 11,410 회 · 원본 sha256 시작=끝 `cb6e9305113d0b47f447eb314ce3bb34d0278bbc8bdf26bc3303d323028575c8` (원장 폴더 HASHES.txt 의 접두 `cb6e9305113d0b47` 와 일치).

재현성: build.py 2회 실행 후 source-map·morphology·expressions·coverage·review.md 해시 동일(`REPRO_OK`).

## 2. verify.py 가 확인하는 것

| 묶음 | 내용 |
|---|---|
| 원본 | 시작/끝 sha256 = 기대값, bytes·이스케이프 수 일치 |
| 구조 양방향 | `object_pairs_hook` 독립 재파싱(중복 키 감지 · 빈 객체/배열 구분)으로 만든 Pointer 목록 ↔ source-map 노드 목록: 집합·**순서**·유일성·자료형·값 일치. 키 출현 249 순서 일치 |
| 구간 재현 | 모든 노드 `text[cp]` 재파싱 = Pointer 값, `byte` ↔ `cp` 환산·디코딩 일치, 문자열 `value_cp` = 디코딩 값, 키 리터럴 구간 = 키, child_count·leaf 플래그 |
| 구획 소유 | 9 구획 소유 노드 합집합 = 전체 노드 344 (누락·불필요 중복 0), 말단 288·키 출현 249 도 양방향, 계획(prefix/owns_exact)으로 소유 재판정, 구획별 direct_read=true·read_status=read·last_read_pointer 소유 여부·manual 기록·review-part 실재, **구획 파일에 소유 노드마다 행이 있고 원문 값 JSON 리터럴이 그대로 실림**, review.md 목차 링크 |
| 형태소 | 말단 288 ↔ value 레코드, 키 출현 249 ↔ field_name 레코드(순서), 적용/제외 정책을 Pointer 패턴으로 재판정, 제외 사유 존재, 토큰 `surface = text[start:end]`·단조·범위, **토큰이 덮지 않은 비공백 문자 0**, 분석기 기록(kiwipiepy 0.24.1 · cong · num_workers 1) |
| 오분절 기록 | 51 출현 각각 값 구간·파일 구간 원문 재현, 소유 구획 일치 |
| 표현 | 수동 310: 값 구간·파일 cp·파일 byte 원문 재현, 문장 구간 포함, facets 어휘 내, 상태 문자, 소유 구획, (Pointer, 구간) 중복 0. regex 107: 구간 재현, `covered_by_manual` 실제 포함 |
| 읽기 검토 보조 | ① 수식·조건·부정·가능성·비교 단서 131 개(키워드 목록 verify.py `CUES`)가 전부 수동 표현 구간 안 ② 언어 텍스트 값(subcategory 제외)의 내용 문자가 수동 표현 구간 밖에 남지 않음(구두점·공백·주제 조사 은/는만 허용) ③ subcategory 외 모든 분석 적용 값에 수동 표현 ≥1 |
| 미결 참조 | manual/S*.json `open` 이 가리키는 issues.md 항목(### ID) 실재 |

## 3. 변이 시험 (결과 폴더 복사본을 스크래치에서 변형 → `verify.py --results <복사본>`)

| 변이 | 결과 |
|---|---|
| M1 coverage 에서 `/procedures/10/prevention` 소유 삭제 | exit 1 · `cov_owned_nodes_union missing` |
| M2 표현 E0040 시작 구간 +1 | exit 1 · `expr_text` 등 2 |
| M3 review-part-S8 의 "제스너 필링" 값 변형 | exit 1 · `review_value_literal` |
| M4 '드물게' 포함 표현 삭제 | exit 1 · `modifier_cue_covered`·`regex_cover_ids`·`expr_char_coverage` 5 |
| M5 procedure_ref 를 분석 적용으로 뒤집기 | exit 1 · `morph_policy_value` 등 4 |
| M6 S5 를 미독으로 | exit 1 · `seg_direct_read` |
| M7 `/procedures/5/name` 을 S1 에 중복 소유 | exit 1 · `seg_owner_by_plan`·`no_dup` 등 3 |

M4 는 처음에 verify.py 가 예외로 종료(StopIteration)해 실패 메시지가 안 남았다 → 가드 추가 후 재실행해 실패 5 건으로 정상 보고(A 아님: 검증기 자체 보완).

## 4. 별도 읽기 검토 (기계 검사와 구분)

- 원문 전체 1회 통독 → 구획 S0~S8 순차 재독(각 구획에서 원문·Kiwi 원시 출력을 나란히 보고 관찰·표현·오분절을 `manual/S*.json` 에 즉시 기록, progress.md 갱신).
- 모든 risk_factors 68 값은 값 전체를 하나의 표현(`risk_factor_phrase`)으로 보존 — 생략된 결과·조건(15·17번)이 잘리지 않음.
- pih_risk ↔ pih_rate ↔ risk_levels 를 26 행 모두 직접 대조하고, 스크래치 계산으로 한 번 더 대조 → 범위 밖 2 행(5·12번 = I1·I2)만 확인. 표는 review.md 「대조」.
- 수식·조건·부정의 탈락 위험 지점은 형태소 층에서 확인: 부등호→괄호 태그, '고에너지' 길이 0 토큰, '비의존적' 의 비/NNG, '깊이'→MAG, '+'(이상) 분리, 범위 W_SERIAL. 표현 층에서는 해당 구절을 원문 구간으로 보존했다(K1).
- 같은 수치·기호의 다른 대상(% 비율/농도, 1.5mm 카트리지/니들, 빈도=시술 빈도, 부위=손상 자리)을 출현별로 따로 기록(F6).
- **미검토**: 의미 관계(비교 대상 행, 조건 적용 범위, 원인 사슬, 기호 의미, 코드 연결)는 1차에서 확정하지 않았다 — F1~F7.

## 5. 한계

- 형태소 원시 출력은 교정하지 않았다. 오분절 기록 51 출현은 원문 읽기에서 눈에 띈 전문어·수식·부정·비교·범위 관련 출현이며, 그 밖 토큰의 정확성은 보장하지 않는다.
- 단서 키워드 검사(§2 읽기 검토 보조)는 직접 읽기를 대신하지 않는다. 키워드 밖 수식이 있을 수 있어 내용 문자 포괄 검사(②)를 함께 둔다.
- facets 는 탐색 관점이며 분류 확정이 아니다.
