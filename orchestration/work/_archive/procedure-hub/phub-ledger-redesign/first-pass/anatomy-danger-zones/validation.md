# anatomy-danger-zones.json — 검증 기록

**1차 범위 종료: 예. 원장 전체 완료: 아님** (열린 I 4 · B 5 · F 3, P 11 · K 5 묶음 기록 — issues.md).

| 상태 | 결과 |
|---|---|
| 전수 읽기 | 12/12 구획 직접 읽기 done (S00 → S11, 남은 구획 없음 — coverage.json `reading_log`) |
| 구조·값 수집 | 노드 615 · 말단 483 (문자열 376 · 숫자 107) · 빈 값 0 · 중복 키 0 · 이스케이프 0 |
| 형태소·표현 수집 | 텍스트 값 331 · 필드명 74 · 제외 152(숫자 107 + 코드/ID 문자열 45) · 토큰 4273 / 수동 표현 352 · 정규식 후보 568 · 절 구간 410 |
| 기계 검증 | verify.py 34135 검사 · 실패 0 · 종료 코드 0. 변조 시험 4종 모두 실패 감지(종료 코드 1) |
| 읽기 검토 | 아래 §읽기 검토 — 누락 9건 보강 후 재검증 |
| 알려진 분석 오류 | K01~K05 (issues.md) |
| 열린 미결 | I 4 · B 5 · C 0 · A 0 |
| 후속 의미 조사 | F 3 + I 4 의 후속 확인 |

## 실행 환경과 명령

- 원본: `orchestration/work/phub-recommend/bronze/phub-ledger/anatomy-danger-zones.json` · 29555 바이트 · 19567 코드 포인트 · 한 줄 · 끝 줄바꿈 없음 · BOM 없음
- 형태소: Kiwi(kiwipiepy 0.24.1) `model_type="cong"`, `num_workers=1`, `OMP_NUM_THREADS=1`, 기본 내장 사전, 사용자 사전 없음, 오타 교정 없음, 입력 정규화 없음
- 캐시·임시 파일: 결과 폴더 밖에 쓰지 않음(uv 공유 패키지 캐시만 사용). 변조 시험은 세션 스크래치패드 사본에서 실행

```sh
# 레포 루트에서
OMP_NUM_THREADS=1 uv run --python 3.12 --with kiwipiepy==0.24.1 \
  python orchestration/work/phub-ledger-redesign/first-pass/anatomy-danger-zones/build.py
python3 orchestration/work/phub-ledger-redesign/first-pass/anatomy-danger-zones/verify.py
```

build.py 출력(최종):

```text
source sha256 start=end 34b2a2de737a2770828ce52e49c3f4f17dc54c21ad9754362c24ebf4fced69a4
nodes 615 leaves 483 string_leaves 376
morph text_values 331 fields 74 excluded 152 tokens 4273
manual_expr 352 auto 568 clauses 410
seg_review 249 split 117 cut_through 4
form_mismatch 3 serial 36
cue_review 51 not_retained 0
```

verify.py 출력(최종):

```text
source sha256 start=34b2a2de737a2770828ce52e49c3f4f17dc54c21ad9754362c24ebf4fced69a4 end=34b2a2de737a2770828ce52e49c3f4f17dc54c21ad9754362c24ebf4fced69a4
nodes=615 leaves=483 string_leaves=376 number_leaves=107
sections=12 owned_union=615 text_values=331 excluded=152 field_names=74
manual_expressions=352 regex_candidates=568 clause_segments=410
checks=34135 fails=0
exit=0
```

## verify.py 가 확인하는 것

verify.py 는 표준 라이브러리만 쓰고, 원본과 결과 파일을 읽기만 한다(쓰기 없음). 실패가 하나라도 있으면 종료 코드 1.

1. **원본 해시**: 시작·끝 sha256 = 기대값 `34b2a2de…69a4` = source-map·coverage 기록값.
2. **중복 키**: `object_pairs_hook` 로 독립 감지 → 0.
3. **구조·값 양방향 대응**: 원문을 독립 재귀 열거한 경로 집합 = source-map 노드 집합(누락·불필요 양쪽), 문서 순서 일치, 노드별 자료형·값(타입까지)·컨테이너 크기 일치.
4. **구간 재현**: 모든 노드의 리터럴 코드 포인트 구간을 다시 파싱하면 해당 값, 바이트 구간 디코딩 = 같은 리터럴, 바이트 오프셋 = 코드 포인트→바이트 환산, 문자열 내용 구간 = 디코딩 값, 숫자 리터럴 원문 보존, 키 리터럴 구간 = 키.
5. **구획 소유**: 12 구획 소유 합집합 = 전체 615 경로(누락·중복 0), 말단 합집합 = 전체 483 말단, 구획 배정 규칙 독립 재계산, 공유 문맥(루트·`/zones`)은 S00 만 소유, 모든 구획 `direct_read=done`·결과 파일 실재.
6. **분할 review 대조**: 각 구획 파일에 소유 노드 전부의 행이 있고, 행의 원본 컬럼명·원문 값(문자열 전문·숫자 리터럴)이 원문과 일치. review.md 에 구획 링크 12개, 컬럼 구성 표에 모든 경로 패턴.
7. **형태소 적용·제외 대응**: 적용 ∪ 제외 = 전체 말단, 교집합 0, 숫자 전부 제외, 제외마다 사유. 모든 토큰 `value[span] = surface`, 파일 구간 원문 재현. 필드명 분석 집합 = 전체 키 74, 출현 Pointer 일치. 분절·수치·단서 관찰 구간 재현. 분석기 설정 기록.
8. **표현**: 수동 표현 = manual-review.json 기록 순서·내용 그대로, 각 구간·파일 코드 포인트·바이트 구간 재현, 중복 생성 0. 정규식 후보는 같은 패턴으로 독립 재계산해 구간 집합 일치. 절 구간 재현.
9. **미결 참조**: 관찰 상태 문자가 A/B/C/I/P/F/K 중 하나, 근거 Pointer 가 원문에 실재, 참조한 미결 ID 가 issues.md 에 있음, issues.md 의 Pointer 표기가 원문에 실재.

### 변조 시험 (verify 가 실패를 잡는지)

결과 폴더 사본을 스크래치패드에 두고 하나씩 망가뜨린 뒤 실행했다. 원본·결과 폴더는 건드리지 않았다.

| 변조 | 감지 메시지 | 종료 코드 |
|---|---|---|
| review-part-S05 의 원문 값 한 칸을 줄임 | `review 원문 값 불일치 /zones/4/vessels/0/course` | 1 |
| coverage 에서 소유 경로 하나 삭제 | `소유 합집합 ≠ 원문 경로: 누락 ['/zones/2/danger_color']` 외 1 | 1 |
| morphology 토큰 구간 +1, 제외 기록 하나 삭제 | `적용∪제외 ≠ 전체 말단`, `토큰 표면 불일치 …` 외 1 | 1 |
| expressions 수동 구간 +1, 정규식 후보 하나 삭제 | `수동 표현 구간 MX-S00-021`, `정규식 후보 재계산 불일치 (568 vs 567)` | 1 |

## 읽기 검토

기계 검증과 따로, 결과를 원문과 다시 읽어 대조했다.

1. **수동 표현이 없는 텍스트 값 전수 확인**: 첫 빌드 뒤 수동 표현이 하나도 없는 텍스트 값 76개를 전부 다시 읽었다. 대부분 이름·라벨(`name_ko`, `name_en`, 혈관·신경 `name`, 짧은 감각 부위)이었다. 수식·통계·조건이 있는데 빠진 9개 값을 추가했다: `/zones/0/clinical_pearls/0`, `/zones/0/botox_specific/diffusion_range_cm`, `/zones/1/nerves/0/significance`, `/zones/2/clinical_pearls/1`, `/zones/2/botox_specific/safe_zone`, `/zones/5/clinical_pearls/0`, `/zones/7/clinical_pearls/0`, `/zones/8/clinical_pearls/0`, `/zones/8/botox_specific/safe_zone`. 이름·라벨 값은 값 전체를 보존하고 표기 차이를 ADZ-F13 에 모았다(manual-review.json `name_label_policy`).
2. **수식·조건·부정·가능성 보존**: 「드물게」「대부분」「대개」「거의」「상대적으로」「사실상」「수 있음」「가능」「금지」「금기」「불가」「않음」「없음」「아님」「불충분」과 「~ 시」 조건, 「이상·이하·이내·미만·까지·≥·±」 한계가 수동 표현 구간 안에 대상과 함께 들어 있는지 구획마다 확인했다. Kiwi 토큰에서 단서 표면이 사라진 곳은 0(cue_review 51). 단서가 걸리는 범위는 분석기가 주지 않으므로 수동 표현·절 구간으로만 보존된다(K05).
3. **수치 변환 금지**: 「드물게」「약」「평균」「가장 얕은 경우」「동물모델 상한값」 같은 한정을 숫자로 바꾸거나 떼어낸 기록이 없음을 확인했다. 숫자 필드의 단위는 필드명 접미사 그대로 두었고 단위·백분율을 새로 붙이지 않았다.
4. **오분절 영향**: 분절 관찰 249 출현 중 117 이 여러 형태소로 나뉜다. 뜻이 바뀌는 사례(관자궁→자궁, 천측두동맥→천/NR, 대이개신경→이/NR+개/NNB, 저·고·중점도→도/JX, 하안검→form 하안거)를 issues.md K01·K02 에 영향과 함께 적었다. 교정·사용자 사전은 쓰지 않았다(이번 지시: 기본 결과 보존).
5. **추출 오류 수정(A)**: 분절 관찰에서 부분 문자열 오검출 4건(골막상⊂골막상층·연골막상, 각동맥⊂내안각동맥)의 상태 분류를 고쳤고, 읽기 문서 숫자를 원문 리터럴로 싣도록 고쳤고, 절 구간이 소수점(「0.04mL」)·「et al.,」에서 잘리던 것을 고쳤다(494 → 410 구간). 재빌드·재검증 통과.
6. **원문 주장 대조**: issues.md 와 관찰에 쓴 원문 사실(「~」는 nose·neck 에만, 「–」「≥」는 glabella emergency_protocol 에만, 「±」 두 곳, danger_level = risk_level 11/11, 반복 문자열 목록)을 스크립트로 다시 확인했다.
7. **미검토로 남긴 것**: 부위·혈관·근육·시술의 공통 개념, 표기 간 동일성, 「→」「/」「-」의 관계 종류, 수치의 임상적 타당성, 다른 원장과의 연결. 1차에서 판단하지 않았다. 기계 통과는 의미가 맞다는 뜻이 아니다.

## 한계

- Kiwi 결과는 교정하지 않은 원시 결과다. 형태소 form·lemma 는 도메인 표준명이 아니다.
- 정규식 후보는 보조 수집이며 전수 의미 해석이 아니다. 패턴은 expressions.json `regex_patterns` 에 있다.
- 절 구간은 「.」「;」「—」 기준 기계 분할이다(소수점·「et al.,」 약어 점·「2017;37」 같은 숫자 사이 「;」에서는 자르지 않음). 괄호 안 「;」(예: 「0.0368mL; Yi et al.」)에서는 잘린다. 문맥 보존용 보조 기록이고 문장 경계 정답이 아니다.
