# treatment-sequence.json — 검증 기록 (1차)

기계 검증 통과는 **원문 대응(누락·중복·위치·구간·해시·적용/제외)** 이 맞다는 뜻이다. 의미 해석의 정답이나 정규화 완료를 뜻하지 않는다.

## 1. 실제 실행한 명령 (레포 루트 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`)

```sh
# 원본 고정 (시작)
shasum -a 256 orchestration/work/phub-recommend/bronze/phub-ledger/treatment-sequence.json
#  → e2f74d41d75a0b4b9d1f6216ccc17402af64bbd455b1c1627395a819ce76cfaf
wc -c …/treatment-sequence.json                 # → 8964
grep -c '\\' …/treatment-sequence.json          # → 0 (이스케이프 없음)
grep treatment-seq …/phub-ledger/HASHES.txt      # → e2f74d41d75a0b4b (접두 일치)
cat -n …/treatment-sequence.json                 # 한 줄 전체 직접 통독

# 수집 + 내장 기계 검증 (로그 build-output.txt, 상세 validation-machine.json) — exit 0
uv run --python 3.12 --with kiwipiepy==0.24.1 python \
  orchestration/work/phub-ledger-redesign/first-pass/treatment-sequence/build.py

# 수동 기록 생성기 (직접 읽은 결과를 JSON 으로; build 전에 실행)
python3 orchestration/work/phub-ledger-redesign/first-pass/treatment-sequence/manual-expressions-make.py      # 폴더 안에서
python3 orchestration/work/phub-ledger-redesign/first-pass/treatment-sequence/segmentation-review-make.py     # 폴더 안에서, build 1회차 morphology.json 기준

# 독립 검증 (표준 라이브러리만, build.py 코드 미사용, 파일 쓰기 없음) — exit 0
python3 orchestration/work/phub-ledger-redesign/first-pass/treatment-sequence/verify.py
#  → checks=32 failure_count=0

# 재현성: 산출 JSON·review.md 해시 → build.py 재실행 → 해시 비교 → 동일(REPRO_IDENTICAL)
# 변이 시험 6종: 결과 파일을 일부러 망가뜨림 → verify.py → 백업으로 원복 → 해시 동일 확인(RESTORED_IDENTICAL)

# 원본 고정 (끝)
shasum -a 256 …/treatment-sequence.json         # → e2f74d41…cfaf (동일)
git status --short -- orchestration/work/phub-recommend reference orchestration/work/phub-ledger-redesign
#  → phub-recommend 변경 없음 (?? 는 작업 시작 전부터 있던 미추적 폴더)
```

도구: Python 3.12.x(uv), kiwipiepy 0.24.1 / kiwipiepy_model 0.24.0, `Kiwi(num_workers=1, model_type='cong')`(로드 후 `model_type`='cong', `num_workers`=1 확인), 사용자 사전 없음, `tokenize` 기본 옵션. verify.py 는 시스템 `python3` 표준 라이브러리만 쓴다. 임시 백업은 이 세션 전용 스크래치 폴더에만 두었다.

## 2. 기계 검증 결과

### 2a. build.py 내장 (12검사, validation-machine.json)

노드 정방향(Pointer 해소·span 재파싱·byte_span 디코딩) · 노드 역방향(json.loads 위치 전부 존재) · 중복 키 0 · value_span == 값 · 문자열 = 분석 + 제외 · 형태소 surface == text[span] · 표현 text == 값[span] · 표현 생성 중복 0 · 수동 표현 원문 존재 · 오분절 기록 원문·원시 토큰 일치 · 알려진 오탐 기록 대응 · 원본 해시 불변(build 시작/끝) — 전부 OK.

### 2b. verify.py 독립 (32검사)

| 검사 | 방법 | 결과 |
|---|---|---|
| 원본 해시 | 시작·끝 sha256 = 기록값 = 세 JSON 의 `sha256_start`/`sha256_end` | 통과 |
| 중복 키 | `object_pairs_hook` 로 독립 감지 | 0 — 통과 |
| 구조 양방향 | json.loads 로 독립 열거한 255위치 ↔ source-map 노드 255 (집합·수) | 통과 |
| 노드별 값 | 자료형·값·JSON 리터럴·span 재파싱·byte_span(독립 계산)·value_span·배열 길이·객체 자식 순서 | 불일치 0 — 통과 |
| 키 출현 | 142 키 (객체·키·값 Pointer) 순서까지 일치, 키 span 원문 재현, field_name_occurrences 재계산 일치 | 통과 |
| 적용/제외 | 문자열 164 = 분석 155 ⊔ 제외 9 (겹침·중복 없음), 제외마다 사유·원문 값, 비문자열 말단 20 전부, 필드명 22 전부 | 통과 |
| 형태소 구간 | 토큰 1,429 surface == 값[span], 값 == 원문, form_equals_surface 정합 | 통과 |
| 형태소 덮임 | 분석 값의 비공백 문자 중 어떤 토큰에도 들지 않은 문자 | 0 — 통과 |
| 오분절 기록 | 69출현 phrase == 값[span], 원시 토큰 == 실제 토큰, morphology 내장본 == 파일 | 통과 |
| 표현 | 922건 Pointer 유효·값[span] 재현·(Pointer,구간,범주,방법) 중복 0·id 중복 0, 분석 값마다 segment.value 1건, 제외 값엔 표현 없음, 수동 142 전부 반영, 오탐 19 ↔ 표현 대응, 오태깅 유래 오탐 → 오분절 id 존재 | 통과 |
| 읽기용 결과 | review.md 에 184개 말단 Pointer 전부와 각 원문 값(문자열 그대로·정수는 리터럴), 원본 컬럼명 22개 전부 | 통과 |

### 2c. 변이 시험 (verify 가 실제로 잡는지)

| 변이 | verify 결과 |
|---|---|
| M1 morphology 토큰 하나의 surface 변경 | rc=1 「형태소 surface = 값[span]」 FAIL |
| M2 source-map 노드 하나 삭제 | rc=1 「노드 수」·「노드 집합 양방향」 FAIL |
| M3 review.md 원문 값 하나 변형 | rc=1 「review.md 에 모든 말단 Pointer·원문 값」 FAIL |
| M4 표현 하나 구간 1칸 이동 | rc=1 「표현 Pointer·구간 원문 재현」 FAIL |
| M5 source-map 정수 값 변경(min_days 5→7) | rc=1 「노드별 자료형·값…」 FAIL |
| M6 제외 기록 하나 삭제 | rc=1 「문자열 = 분석 ⊔ 제외」 FAIL |

원복 후 해시 동일, verify 재실행 failure_count=0.

## 3. 별도 읽기 검토 (같은 에이전트, 관점 바꿔 재독 — 독립 검토 아님)

| 관점 | 한 일 | 결과 |
|---|---|---|
| 문맥 보존 | 다섯 블록 전 항목을 review.md 표에서 원본과 다시 읽고, 같은 항목 형제 필드(`context.sibling_pointers`)가 기록됐는지 표본이 아니라 블록별로 확인 | 누락 없음 |
| 수식·조건·부정 | 규칙 후보에 덮이지 않은 어절을 값별로 전부 열람(남은 것은 단일 명칭 값뿐), 부정·제한 표현(않·아님·금지·미허가·부족·피함·만·한정·한해·비-)과 조건·시간(시·경우·하에·후·전·이내·이상·최소·같은 날·별도 세션·즉시) 출현을 원문과 대조 | 수동 구절 14건 보강(직접 읽기 총 142). 절 분할 오류 2종 발견·수정(issues A1-1·A1-2) |
| 오분절 영향 | 1,429토큰 전체 열람 → 의미가 사라지거나 바뀌는 출현 69 기록. 특히 범위 조건(「에 한해」→1년, 「전안면」→저는)·비교(>→괄호)·부정 접두(비박리성·비가교)·처치/부위명 | 교정 안 함, 위치·영향 기록(issues A2) |
| 규칙 후보 오탐 | 13규칙 전 범주 후보를 열람 | 규칙 수정 4(issues A1-3~5), 남은 오탐 19 출현별 기록(issues A3) |
| 잠정 해석 근거 | review.md 잠정 관찰마다 Pointer 를 달고 원문 칸과 분리 | 확정 표현 없음 |

미검토로 남긴 것: 의미 관계(방향·조건 적용 대상·인과·선후의 정답), 다른 원장과의 연결, 카테고리 코드의 대상. issues D 로 남김.

## 4. 한계

- 형태소 정확성은 기록한 69출현과 그 종류에 대해서만 말한다. 기록 밖 토큰의 정확성은 보장하지 않는다.
- 표현 범주는 탐색용 후보이며, 규칙·품사·수동 목록 결과를 전수 의미 해석으로 쓰지 않는다.
- 읽기 검토는 같은 에이전트가 했다. 독립 검토가 필요하면 코디 판단으로 별도 발주한다.
