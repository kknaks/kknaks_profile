# validation — pre-procedure-checklist.json 1차

## 상태

- **1차 범위 종료: 예** · **원장 전체 완료 아님**
- 전수 읽기: 6/6 구획(S00–S05) 직접 읽기 완료 — coverage.json `direct_reading=read`
- 구조·값 수집: 노드 503 · 말단 331(전부 문자열) · 객체 153 · 배열 19 · 빈 컨테이너 0 · 빈 문자열 0 · null 0 · 중복 키 0 · 이스케이프 0
- 형태소·표현 수집: kiwi 적용 165 · 제외 166(코드값: id·type·version·updated) · 필드명 10종 별도 기록 · 자동 후보 425(정규식 일치분만) · 수동 표현 188
- 기계 검증: verify.py 14,697 검사 · 실패 0 · EXIT 0
- 읽기 검토: 아래 §3 — 실제 추출 누락 1건 발견·수정(A-S04-6)
- 알려진 분석 오류: 형태소 오분절 44출현(구조화 기록) + issues K 8건(전역 G-4~G-7 · 구획 S02-4·S03-7·S05-5·S05-6 — 자동 패턴 오탐 2·kiwi 부정/금기 영향 2)
- 열린 미결: B 15 · P 3 · I 2(원문 내 불일치 후보, 원본 변경 선택 대기 아님) · F 10(deferred) · C 0
- 후속 의미 조사: type 의미, universal↔category 관계, 반복 주제 동일성, 카테고리 연결 — issues.md F

## 1. 재현 명령 (레포 루트)

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --python 3.12 --with kiwipiepy==0.24.1 python \
  orchestration/work/phub-ledger-redesign/first-pass/pre-procedure-checklist/build.py
# → ok sha=0de87bff…4086 nodes=503 leaves=331 morph=165 excl=166 auto=425 manual=188

python3 orchestration/work/phub-ledger-redesign/first-pass/pre-procedure-checklist/verify.py
# → checks=14697 failures=0, EXIT=0
```

build.py 는 이 폴더 안에만 쓴다. verify.py 는 표준 라이브러리만 쓰고 어떤 파일도 쓰지 않는다(원본은 시작·끝 해시만 읽음). 실패 시 exit 1.

## 2. 기계 검증 항목 (verify.py)

| 항목 | 방법 | 결과 |
|---|---|---|
| 원본 해시 시작/끝 불변 | sha256 시작·끝 비교 + source-map/coverage 기록과 대조 | `0de87bff91f721fe685884025d31749017d44da250492b2db9d49109a61e4086` 일치 |
| 중복 키 | `object_pairs_hook` 로 독립 감지 | 0 (기록과 일치) |
| 구조·값 양방향 대응 | 원본을 독립 순회한 Pointer 집합 ↔ source-map 노드 집합, 문서 순서, 자료형, 값, child_count | 503/503 일치 · 누락 0 · 불필요 0 |
| 리터럴 구간 재현 | `literal_cp` 를 원문에서 잘라 json.loads → 원본 값, `literal_byte` 를 바이트에서 디코딩 = cp 구간, 키 구간 | 전부 재현 |
| 구획 소유 | 구획별 owned_pointers 합집합 ↔ 전체 Pointer 양방향, 중복 소유 0, source-map segment 표시 일치, 말단 목록 일치 | 일치 |
| 구획 상태·파일 | 6구획 모두 `read`, review-part 파일 실재·집합 일치, 모든 소유 Pointer 의 값 표 행(컬럼명·자료형·원문 값) 존재, 관찰 반영 | 통과 |
| review.md | 구획 목차 6개, 컬럼 구성 표에 모든 경로 패턴 행 | 통과 |
| 형태소 적용/제외 | 문자열 말단 331 = 적용 165 ⊔ 제외 166, 중복 0, 제외 사유 존재 | 통과 |
| 토큰 구간 | surface = 값[start:end], file_cp 재현, 공백 외 모든 문자가 토큰에 덮임, 겹침은 축약 음절 표시(`span_shared_with_prev`)가 있을 때만 | 통과 |
| 필드명 | 10종 키·출현 Pointer 가 원본과 일치 | 통과 |
| 알려진 오분절 | 44건 모두 표면형이 원문에 있고 raw_tokens 가 실제 kiwi 결과 안에 있음 | 통과 |
| 표현 구간 | 자동 425·수동 188 구간을 값/원문에서 재현, 자동 후보를 기록된 패턴으로 재계산해 집합 일치, 수동 중복 생성 0, 수동 기록 수 = expressions 수 | 통과 |
| issues | 모든 미결 ID 가 issues.md 에 있고 Pointer 가 유효 | 통과 |

### verify 자체 시험 (스크래치 복사본에 변조 후 실행)

| 변조 | 결과 |
|---|---|
| 무변경 | exit 0 |
| 구획 소유 Pointer 1개 제거 | exit 1 |
| 구획 중복 소유 | exit 1 |
| 수동 표현 start +1 | exit 1 |
| 문자열 말단 값 변조 | exit 1 |
| 형태소 기록 1개 삭제 | exit 1 |
| 구획 상태 planned 로 | exit 1 |
| review-part 값 칸 변조 | exit 1 (처음엔 통과 → 행 단위 대조로 고친 뒤 실패 확인) |
| 토큰 start 변조 | exit 1 |
| 오분절 raw_tokens 변조 | exit 1 |
| issues.md 삭제 | exit 1 |

처음 verify 실행에서 15건 실패: kiwi 가 한 음절을 둘 이상 형태소로 나눌 때(인→이+ᆫ, 져→지+어, 필러→피+ᆯ러) 토큰 구간이 겹친다. 도구의 실제 출력이라 값은 그대로 두고 build.py 에서 `span_shared_with_prev` 로 표시했다. verify 는 그 표시가 있고 앞 토큰 구간 안에서 시작할 때만 겹침을 허용한다.

## 3. 별도 읽기 검토

1. **자동 후보 ↔ 수동 표현 대조**: 수동 표현이 덮지 않는 자동 후보 32건을 하나씩 읽었다.
   - 실제 누락 1건 → **A-S04-6 fixed**: `/category_specific/11/checks/2/label`(M12 이소트레티노인)의 괄호 앞 구절 두 개가 수동 기록에 없었다. 추가하고 재검증했다.
   - 나머지는 줄표(—)·괄호 전체 단위 후보로, 수동에서는 그 안의 하위 구절로 나눠 이미 보존돼 있다(예: «— 이물반응, 합병증 위험 대폭 증가» ↔ 수동 «이물반응, 합병증 위험 대폭 증가»). 원문 전체 값은 모든 기록의 `context_value` 에 있다.
   - 같은 대조에서 '켈로이드 체질 확인'(M11·M12·M13), '헤르페스 병력 확인'·'금속 임플란트 확인'(M8)을 추가했다.
2. **패턴 밖 표현**: 직접 읽기에서 형용사(현실적인·얕은·충분한·과도한·점진적·역설적·화학적·발작성·활동성), 부사(크게·특히·더·대폭·반드시), 회피·권고(상의 필수·연기 판단·고려 가능·제한 안내), 깊이·두께(니들 깊이별·지방층 두께·피하지방 두께), 근사·범위(1-3개월·30-70%·0.005-0.39%·I-VI), 「후/시/전/이내」 조건을 구획별 수동 표현으로 모았다. 그래도 전수 의미 해석은 아니다.
3. **수동 표현이 없는 분석 대상 19개**(verify info): 알레르기 병력·자가면역질환·수유 여부·기저질환·임신 여부·시술 부위 피부 상태 같은 universal label 6개와 카테고리 name 10개('PRP/자가혈'·'HIFES/EMS' 등 슬래시가 있는 이름은 수동 표현에 있음), '자가면역질환 여부'·'항응고제 복용 여부' 3개. 직접 읽었고 수식·조건이 없는 명사구라 따로 모으지 않았다. 원문·토큰은 source-map·morphology 에 있다.
4. **형태소 의심 태그 전수 대조**: MM·NR·NP·VV·VA·EC·EF·XPN 등 의심 태그 토큰을 원문 앞뒤 문맥과 함께 전부 출력해 오분절 기록과 비교했다. 오분절이 아닌 경우(정상 활용·접미사·의존명사)는 기록하지 않았다. 품사가 NNP/NNG 로 갈리는 것은 G-7 로 묶었다.
5. **금기 일괄 확정 방지**: type 값을 관계로 바꾸지 않았다. 확인·설명·준비·시술 후 지시가 섞여 있다는 점(G-2)과 type·문구가 다른 축으로 보이는 예(S05-4, S04-4, S01-5)를 기록했다.

## 4. 한계 (1차 종료를 막지 않음)

- 영문 약어·영단어는 kiwi SL 토큰으로만 보존했고 영어 형태 분석은 하지 않았다(G-4). 다른 언어는 없다.
- 하이픈 범위는 W_SERIAL 단일 토큰이다(G-5). 동음이의어·의미 sense 는 분석하지 않았다.
- 자동 후보는 정규식 일치분뿐이다(G-6). 슬래시 범위는 공백에서 끊긴다.
- 사용자 사전을 쓰지 않았다. 기본 결과를 보존하고 오분절은 출현별로 적었다.

## 5. batch-04 기록 보완 — 오분절 출현 구간(span) (2026-11-09)

독립 검토 [batch-04-review.md](../../batch-04-review.md) §2.4 R1 반영. 재조사·형태소 재분석은 하지 않았다.

- 무엇: `manual/segment-notes.json` 의 `morph_known_errors` 44출현에 `span` = 해당 Pointer 의 **디코딩된 값 문자열 안 Unicode 코드포인트 [start,end)** 를 추가했다. 기존 pointer·surface·raw_tokens·impact 는 그대로다.
- 생성부: build.py 가 이 수동 기록을 읽어 `morphology.json` 의 전역 `known_errors` 와 레코드별 `known_errors` 에 그대로 넣는다. build.py 는 각 span 이 원본 값에서 표면형을 재현하고 표면형이 그 값에서 1회인지 확인하고, 아니면 멈춘다. issues.md 「K-형태소 오분절 출현 목록」 각 줄에 `[start,end)` 를 찍는다.
- verify.py 추가 검사: span 형식(정수 2개), 범위(0 ≤ start < end ≤ 값 길이), `text[start:end]` = 표면형, 독립 순회한 원본 값에서도 재현, 표면형 1회, 레코드별 known_errors ↔ 전역 known_errors 동등(집합·포인터별 순서).
- 실제 결과:
  - span 재현 **44/44**, 표면형 정확히 1회 **44/44**, 전역 44 = 레코드별 합 44.
  - `python3 pre-procedure-checklist/verify.py` → `checks=15083 failures=0`, EXIT 0 (보완 전 14,697).
  - 스크래치 복사본에서 build.py 재실행: 보완 전 상태로는 기존 산출물 14개 전부 바이트 동일. 보완 후에는 `morphology.json`·`issues.md` 만 다르고, `morphology.json` 은 span 키를 빼면 기존과 동일, `issues.md` 는 K 목록 44줄에 구간 표기 + 설명 2줄만 다르다.
  - 변이 시험(스크래치): 전역 span start+1 → exit 1 · span 범위 밖 → exit 1 · span 삭제 → exit 1 · 레코드별 span 만 변조 → exit 1 · 수동 기록 span 변조 후 build → 「known_error span 재현 실패」로 멈춤.
