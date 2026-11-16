# combo-recipes.json — 검증 기록 (1차)

기계 검증 통과는 **원문 대응(누락·중복·위치·구간·해시·적용/제외)** 이 맞다는 뜻이다. 의미 해석의 정답이나 정규화 완료를 뜻하지 않는다.

## 0. 상태

| 항목 | 상태 |
|---|---|
| **1차 범위 종료** | **예** |
| **원장 전체 완료** | **아님** — B 10 · P 8 · F 7 · I 1 열림(issues.md). 사용자 결정 필요 C 0(issues.md §0 근거) |
| 전수 읽기 | 구획 8/8(S0 상위 + S1~S7 레시피) 직접 읽음 — coverage.json `direct_read=done`, 남은 구획 없음, 마지막 위치 `/recipes/6/followUp/3/action` |
| 구조·값 수집 | 노드 192(경로 전부) · 키 출현 137 · 말단 141(문자열 113 + 정수 28) · 빈 값 0 · 중복 키 0 |
| 형태소·표현 수집 | 형태소 적용 78값 · 제외 35값(사유별) · 토큰 961 · 필드명 17 · 표현 633(수동 181) |
| 기계 검증 | verify.py 92검사 failure_count=0 |
| 읽기 검토 | §3 — 같은 에이전트의 별도 관점 재독(독립 검토자 아님) |
| 알려진 분석 오류 | 오분절 14규칙 · 출현 29건 · 태그 비일관 5형 — 미교정, 출현별 기록 |
| 열린 미결 · 후속 의미 조사 | issues.md §2~5 |

## 1. 실행한 명령 (레포 루트)

```sh
# 원본 고정
shasum -a 256 orchestration/work/phub-recommend/bronze/phub-ledger/combo-recipes.json
#  → 1bb7c309e8ec72768ae9c5db94e1911188be240f4c7d770d54244008aeab0c94 (시작)
wc -c -l …/combo-recipes.json        # 6486 bytes, 개행 0
grep -c '\\' …/combo-recipes.json     # 0 (이스케이프 없음)
head -c 3 … | xxd                     # 7b2276 — BOM 없음

# 수집(재현) — 출력은 build-output.txt
uv run --python 3.12 --with kiwipiepy==0.24.1 python \
  orchestration/work/phub-ledger-redesign/first-pass/combo-recipes/build.py

# 독립 검증 — 표준 라이브러리만, build.py 를 import 하지 않음, 파일을 쓰지 않음, 실패 시 exit 1
python3 orchestration/work/phub-ledger-redesign/first-pass/combo-recipes/verify.py
#  → checks=92 failure_count=0 paths=192 leaves=141 strings=113, exit 0

# 재현성: 산출 JSON·review.md 해시 → build.py 재실행 → 비교
#  → IDENTICAL

# 원본·타 작업 불변
shasum -a 256 …/combo-recipes.json    # 1bb7c309…0c94 (끝, 동일)
git status --short -- orchestration/work/phub-recommend reference   # phub-recommend 변경 없음
```

도구: Python 3.12.11(uv), kiwipiepy 0.24.1 / kiwipiepy_model 0.24.0, `Kiwi(num_workers=1, model_type="cong")`, tokenize 기본 옵션, 사용자 사전 없음. verify 는 시스템 `python3`.

## 2. 기계 검증 결과 (verify.py)

| 검사 | 방법 | 결과 |
|---|---|---|
| 원본 해시 불변 | verify 시작·끝 sha256 == 기록값, 4개 산출 JSON 의 source.sha256 일치 | 통과 |
| 중복 키 | `object_pairs_hook` 로 객체마다 키 중복 감지(build 는 자체 파서로 별도 감지) | 0 — 통과 |
| 구조·값 양방향 | `json.loads` 로 독립 열거한 경로 192 ↔ source-map 노드 192: 양쪽 차집합 0, 자료형·값 일치 | 통과 |
| 리터럴 구간 | 노드 span slice 를 다시 `json.loads` → 값 일치, byte_span 디코딩 == 코드포인트 slice, 문자열 value_span slice == 디코딩 값 | 통과 |
| 키 구간 | 키 출현 137 == 문서의 객체 키 합, span slice 가 키 리터럴 재현 | 통과 |
| coverage 양방향 | 구획 소유 경로 합집합 == 전체 경로 192, 중복 소유 0, 말단 합집합 == 141, 구획 경계(S0=비-recipes 원소, Sk=/recipes/k-1) 위반 0 | 통과 |
| coverage 상태·파일 | 8구획 모두 machine_extraction·direct_read=done, review 파일·앵커 실재, 문맥 참조 Pointer 유효, 남은 구획 0 | 통과 |
| review 값 표 | 「### 원문 값」 표에서 **모든 경로가 정확히 한 행**, 원본 컬럼명(배열 원소는 `부모키[i]`)·자료형·원문 값(`\|` 복원 후) 일치 | 통과 |
| 형태소 적용/제외 | 문자열 113 = 적용 78 ∪ 제외 35, 서로소, 제외마다 사유, 제외 값 == 원문 | 통과 |
| 토큰 구간 | 961토큰 값 기준·파일 기준 slice == surface, form_equals_surface 일관, 적용 값의 공백 아닌 모든 문자가 토큰에 덮임 | 통과 |
| 필드명 | 고유 필드명 17/17 분석 기록 | 통과 |
| 분석 설정 | cong · num_workers 1 · kiwipiepy 0.24.1 기록 | 통과 |
| 오분절 출현 | 29출현 각각 surface·원시 토큰이 morphology 값과 일치, 14규칙 출현 수 == expected_count(0 출현 규칙 없음) | 통과 |
| 표현 | 633건 값 기준·파일 기준 slice == text, id 유일, (pointer·span·category·method) 완전 중복 0, 적용 78값 모두 segment.value 보유 | 통과 |
| 수동 표현 | manual 181항목 각각 정확히 1건 대응, 8구획 모두 수동 표현 보유 | 통과 |
| 오탐 표시 | 4건 각각 사유 | 통과 |
| 관찰 | 관찰 Pointer 전부 유효, 상태 문자 ∈ {P,F,B,I,K}, 모든 관찰 ID 가 review.md 에 실림 | 통과 |

**검증기 자체 시험(변조 시험)** — 원본·산출물을 스크래치 경로에 복제해 하나씩 변조 후 verify 실행:

| 변조 | 결과 |
|---|---|
| review.md 값 한 칸(`3~6개월 간격 반복` → `3~6개월 간격`) | FAIL(review value) — 감지 |
| coverage 에서 `/recipes/2/analogy` 소유 제거 | FAIL 2건(all paths owned · leaf union) — 감지 |
| morphology 토큰 start +1 | FAIL(tok_span·uncovered) — 감지 |
| 원본 끝에 공백 추가 | FAIL 5건(해시) — 감지 |

## 3. 별도 읽기 검토 (같은 에이전트, 다른 관점)

1회차: 원본 한 줄을 레시피 단위로 위에서 아래로 직접 읽으며 manual-expressions·manual-observations 작성. 2회차: Kiwi 출력 961토큰을 값마다 원문과 나란히 열람해 오분절 규칙 작성. 3회차(아래): 탈락 관점 재독.

- **수식·정도**: 형태소 기반 수식 후보(MAG·VA·XR·MM·XSA 어절) 전부를 수동 표현 구간과 대조. 수동 구간 밖은 3건(`팽팽하게,` ×2·`(HIFU 반복 or 실리프팅 업그레이드)` 괄호) — 모두 수동 비유 대응·대안 표현 안에 내용이 들어 있고 구두점·괄호만 밖이라 보강하지 않았다. 「오래」「스스로」「아주 작은」「확연한」「확실한」「자연스러운/자연스럽게」「바로」「잘게」「맑고」「단단하게」는 모두 수식 대상과 함께 수동 표현으로 보존.
- **조건**: 「효과 부족 부위」「효과 감소 시」「부족하면」(×2)「반복 시」(×3)「경과에 따라」「평가 후 결정」「필요시」 — 각각 조건이 한정하는 행위·효과와 함께 보존. 조건 범위가 불분명한 곳은 P-5·P-8 로 남김.
- **가능성**: 「가능」(×3)「검토」(×3)「결정」 — 확정 행위와 구분해 possibility 로 보존(F-5).
- **부정**: 직접 읽기와 정규식 모두에서 부정 표현 0. 정규식 「안 」 2건은 「동안(童顔)」 오탐으로 출현별 표시.
- **범위·수량·시간**: `~` 범위 16건·숫자+단위 39건 전부 regex 와 수동 양쪽에 있음. 「수천 개」「5살」「30분 내」 등 어림·체감 수치는 수치로 바꾸지 않음. week↔개월 환산 판정은 넣지 않음(A-4 에서 제거).
- **오분절의 의미 영향**: 시술(실·필러)·부위(이마) 소실, 관형 수식 변질(새), 조건 표지 은닉(필요시) — 출현별 기록. 수동 표현이 원문 구간으로 같은 내용을 보존하고 있음을 확인.
- **문맥 보존**: 문장 간·절 간 지시(「이 열이」「거기에」)와 문장 내 선후(「…고정한 뒤」)를 문장 전체 구간과 함께 보존.
- **미검토**: 시술 간 관계(보완·동시·순서·회피)의 의미, M 코드 대상, 기호 규칙 적용 여부는 1차 범위 밖 — 미검토로 둔다.

## 4. 한계

- 읽기 검토는 독립 검토자가 아니다.
- 오분절 규칙 밖 토큰의 형태소 정답을 전수 보장하지 않는다.
- 표현 범주는 탐색 라벨이며 분류 확정이 아니다.
