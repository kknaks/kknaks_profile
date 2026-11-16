# procedure-profiles.json — 검증 기록 (1차)

> **2026-11-09 보정판**: 독립 검토 F1~F7을 반영했다. §2b·§2c 를 추가했다. 보정 뒤 독립 재검토는 아직 없다.

기계 검증이 통과했다는 것은 **원문 대응(누락·중복·위치·구간·해시)** 이 맞다는 뜻이다. 의미 해석의 정답, 정규화 완료를 뜻하지 않는다.

## 1. 실제 실행한 명령 (레포 루트 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`)

```sh
# 원본 고정
shasum -a 256 orchestration/work/phub-recommend/bronze/phub-ledger/procedure-profiles.json
#  → a1fe389d83430002f3d78e7c07ead4a7675d4afcfb68d28f9ac94042a5423f3e  (시작)
wc -c -l …/procedure-profiles.json            # → 19548 bytes, 개행 0
grep -c '\\' …/procedure-profiles.json         # → 0 (이스케이프 없음)
python3 -m json.tool --no-ensure-ascii …/procedure-profiles.json   # 전체 통독용 정렬 출력

# 수집 + 기계 검증 (출력은 build-output.txt, 상세는 validation-machine.json)
uv run --python 3.12 --with kiwipiepy==0.24.1 python \
  orchestration/work/phub-ledger-redesign/first-pass/procedure-profiles/build.py

# 독립 재검증 (build.py 코드를 쓰지 않음, 표준 라이브러리만)
python3 orchestration/work/phub-ledger-redesign/first-pass/procedure-profiles/verify.py   # exit 0

# 재현성: 산출 JSON 해시 → build.py 재실행 → 해시 비교
(cd …/procedure-profiles && shasum -a 256 *.json) > h1 ; build.py ; … > h2 ; diff h1 h2   # → IDENTICAL

# 끝 해시
shasum -a 256 …/procedure-profiles.json        # → a1fe389d…3f3e (동일)
git status --short -- orchestration/work/phub-recommend reference   # phub-recommend 변경 없음
```

도구: Python 3.12(uv), kiwipiepy 0.24.1 / kiwipiepy_model 0.24.0, 모델 `cong`(Kiwi 기본값으로 로드됨). `sbg` 모델은 쓰지 않았다(코디 인계: 패키지 파일 누락).

## 2. 기계 검증 결과

| 검사 | 방법 | 결과 |
|---|---|---|
| 원본 해시 불변 | 작업 시작·build 내부 시작/끝·verify·작업 끝 sha256 | 모두 `a1fe389d…3f3e` — **통과** |
| 중복 키 | 자체 재귀 하강 파서가 객체마다 키 집합 추적(`json.loads` 의 조용한 덮어쓰기 회피) | 0건 — **통과** |
| 구조·값 정방향 | 파서 노드 583개 각각: Pointer 로 `json.loads` 결과 해소 → 자료형·값 일치, 노드 span 재파싱 값 일치 | 불일치 0 — **통과** |
| 구조·값 역방향 | `json.loads` 결과 전 경로 583개가 노드에 존재, 개수 일치 | 누락 0 — **통과** |
| Pointer 유일·해소 | 583 포인터 유일, 전부 해소 | **통과** |
| 키 구간 | 키 412개(4 + 17×24) span slice == JSON 키 리터럴 | 불일치 0 — **통과** |
| 문자열 값 구간 | 문자열 노드 292개 value_span slice == 디코딩 값 | 불일치 0 — **통과** |
| 바이트 구간 | 모든 노드 byte_span 디코딩 == 코드 포인트 span slice | 불일치 0 — **통과** |
| 형태소 적용/제외 대응 | 문자열 292 = 적용 197 ∪ 제외 95, 서로소, 각 제외에 사유 | **통과** (제외: ID 17·버전 1·날짜 1·snake_case 코드 76) |
| 필드명 분석 | 고유 필드명 28/28 분석 기록 | **통과** (Kiwi 미지원 → 규칙 분할 보완, issues A4) |
| 토큰 구간 | 2,341토큰: 값 기준 slice == surface, 파일 기준 slice == surface, 빈 구간 0 | **통과** |
| 토큰 커버리지 | 적용 값의 공백 아닌 모든 문자가 어떤 토큰 구간에 덮임 | 미포함 0 — **통과** |
| 표현 구간 | 1,505건 slice == text, 빈 표현 0, id 유일, (pointer·span·범주·방법) 완전 중복 0 | **통과** |
| 표현 값 커버리지 | 형태소 적용 값 197개 모두 `segment.value` 표현 보유 | **통과** |
| 수동 목록 | 210항목 모두 원문에서 ≥1회 발견 | **통과** |
| 오분절 규칙 | 35규칙 모두 실제 출현 ≥1(구절 규칙 66건 — 규칙이 비어 있지 않다는 것만 보장. 출현 전수는 §2b) | **통과** |
| 오탐 표시(보정) | expression-review.json 15출현 각각 정확히 1개 후보에 대응·텍스트 일치. 단어 단위 일괄 규칙은 폐기 | **통과** |
| 재현성 | build.py 재실행 시 산출 JSON 바이트 동일 | **통과** |

## 2b. 보정 검증 — 출현 단위 오태깅 (F1)

| 검사 | 방법 | 결과 |
|---|---|---|
| 판정 범위 전수 | 품사 MAG·MM·NR·NP·MAJ 전부 + 의미위험 서명 16종에 해당하는 **모든 값의 모든 토큰**이 segmentation-occurrence-review.json 에 정확히 1회(누락·잔존·중복) | 89/89, 누락 0 · 잔존 0 · 중복 0 — **통과** |
| 판정 ↔ 표시 양방향 | 판정이 correct 가 아닌 출현 39건은 모두 `segmentation_review` 에 있음. 표시된 토큰 중 판정이 correct 인 것은 0 | **통과** (재훑기로 4건 추가: 열/NR 3 · 수화/NNP 1 → 70건) |
| 표시 토큰 실재 | `segmentation_review` 의 모든 토큰이 원시 Kiwi 토큰 목록에 존재. status 는 모두 「표시됨(교정 아님)」 | **통과** |
| 변이 시험 | 사본에서 `/profiles/9/practicalNotes/0` 「열」 표시 1건 삭제 → verify 실패 1(`occ<->segrev`) | 검사가 실제로 잡음 |

**범위 밖 알려진 오분절 (재검토 W1, 미표시)**: `/profiles/13/aftercare/0` [6,8) 발적은 발/NNG+적/XSN, `/profiles/2/practicalNotes/2` [66,68) 수화는 수/NNG+화/XSN 으로 분석됐다. 위치·위험은 [issues.md](./issues.md) A1-W1 에 적었다. 원시 형태소 출력에는 이런 알려진 오류가 남아 있고, 이 검증은 지정 품사(MAG·MM·NR·NP·MAJ)·서명 16종 **밖**의 형태소 정확성을 보장하지 않는다.

규칙 단위의 「출현 ≥1」 검사는 그대로 둔다. 다만 그 검사는 규칙이 비어 있지 않다는 것만 보장한다. 출현 전수는 위 검사가 맡는다. 범위 밖 품사(NNG·VV 일반 등)는 출현 전수 판정을 하지 않았다.

## 2c. 보정 검증 — 오태깅 유래 표현 후보 (F2)

| 검사 | 방법 | 결과 |
|---|---|---|
| 근거 토큰 연결 | modifier_phrase 96건 모두 `source_token`(형태·품사·구간) 보유, 범위 안 품사는 출현 판정 존재 | **통과** |
| 유래 표시 대응(범위 한정) | 근거 토큰 판정이 correct 가 아니면 `false_positive(오태깅 유래)` + `review_basis`, correct 면 표시 없음 — 양방향 | 9건 표시, 불일치 0 — **통과** |
| 일괄 처리 금지 | 같은 구간의 다른 범주 후보(예: negation_phrase 「세안 피하기」)와 같은 단어의 다른 출현(피하기 7건)은 표시 안 됨 | 확인 |
| 보존 | 표현 수 1,505 그대로(삭제 0) | **통과** |
| 오탐 합계 | false_positive 표시 = expression-review 15 + 오태깅 유래 9 = 24 | **통과** |
| 변이 시험 | 사본에서 오태깅 유래 표시 1건(E00591) 제거 → verify 실패 1(`derived fp`) | 검사가 실제로 잡음 |

**W2 — 미판정 근거 토큰 46건**: modifier_phrase 의 근거 토큰 96개 품사는 MAG 39 · MM 11 · VA 24 · VA-I 6 · XR 14 · VCN 2 다. 이 가운데 VA·VA-I·XR·VCN **46건은 출현 판정 범위 밖**이다. build·verify 는 판정 목록에 없는 근거 토큰을 **correct 로 간주**한다. 따라서 위 「양방향」 검사는 범위 안 근거 토큰 50건에만 성립하는 구현이다. 이와 별개로, 2026-11-09 재검토자가 이 46건을 문맥과 함께 읽었고 **현재 추가 오태깅은 없었다**고 보고했다. 이 결과는 사람 대조이며 verify 가 보장하는 것이 아니다.

보정 때 실행한 명령은 다음과 같다.

```sh
uv run --python 3.12 --with kiwipiepy==0.24.1 python …/build.py      # build-output.txt — 모든 목록형 검사 빈 값
python3 …/verify.py                                                  # exit 0, failure_count 0 (occurrences 89, occ_non_correct 39, mistag_derived_fp 9, expr_review_entries 15)
# 변이 시험: scratchpad 사본 2종에서 verify → 각각 failure_count 1
shasum -a 256 …/procedure-profiles.json                              # a1fe389d…3f3e (보정 전·후 동일)
```

「무관」 실패: 없음. 이전부터 깨져 있던 항목도 발견되지 않았다.

## 3. 읽기 검토 (기계 검증과 별도)

| 검토 | 범위 | 결과 |
|---|---|---|
| 전수 원문 읽기 | 상위 4키 + 17항목 × 24필드 전부, 정렬 출력 통독 | review.md §4 에 항목별 원문 인용·관찰 |
| 형태소 대조 | 197값 전 토큰 열(구두점·조사·어미 제외 표시)과 원문 나란히 | 오분절 35규칙 확정(issues A1). 토큰은 고치지 않음 |
| 표현 손실 검토 | 값마다 「비세그먼트 표현에 덮이지 않은 어절」 목록 열람 | 1차: 이유(이므로·하여)·비망라(등·외)·범위(모든·다른·양쪽·단독·-별)·대안(또는·or)·`=`·정도어(고강도·초극대·중대·점진적·불균형한) 누락 발견 → 규칙 추가. 2차: 부정의 피수식 동사(「문지르지 않기」「주사하지 않음」) 누락 → 부정 구절 규칙 추가. 3차 잔여 = 행위·대상 명사(issues A3) |
| 오탐 검토 | 시점·부정·가능·조건 keyword 결과 전체 열람 | 즉시·반드시·안면·표면·피하(皮下) 오탐 확인 → 표시(issues A2) |
| 수식·조건·부정 탈락 | 형용사·부사·조건·부정·가능성 구절 | 위 보강 뒤 잔여 탈락 없음을 열람으로 확인. 단, 수식어가 **무엇을** 수식하는지는 연결하지 않음(후속) |

한계:
- 읽기 검토는 같은 에이전트의 재독이다. 독립 검토자 검토는 하지 않았다.
- 표현 범주는 regex·keyword·품사·수동목록으로 만든 **후보**다. 원문 전체의 의미 조사로 제시하지 않는다.
- 의미 관계(정보 종류·수식 대상·관계 방향·인과·선후)는 **미검토**다.

## 4. 산출물 목록

| 파일 | 역할 |
|---|---|
| review.md | 읽기용 조사 |
| source-map.json | 원본 식별·해시, 노드 583·키 412의 Pointer·자료형·값·코드포인트/바이트 구간·문맥, 필드명 출현 위치 |
| morphology.json | 분석 설정, 적용 197값 토큰(form·tag·lemma·span·surface), 제외 95값 사유, 필드명 28, 기계 표시 `segmentation_flags`, 확인된 `segmentation_review` |
| expressions.json | 복합 표현 후보 1,505건(방법·범주 후보·review 표시·문맥) |
| issues.md | 미결 A/B/C·후속 |
| validation.md | 이 문서 |
| validation-machine.json · build-output.txt | build.py 기계 검사 원자료 |
| segmentation-occurrence-review.json | (보정) 지정 범위 토큰 89출현의 오태깅 판정 |
| expression-review.json | (보정) regex·keyword 오탐 15출현 목록 |
| build.py · verify.py | 재현·독립 재검증 스크립트 |
| manual-expressions.json · segmentation-review-rules.json | 직접 읽기로 만든 수동 목록·오분절 규칙(build 입력) |
