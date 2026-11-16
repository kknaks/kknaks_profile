# products.json — 상태·검증 기록 (1차)

**1차 범위 종료: 충족(작성자 판정, 코디 확인 전)** · **원장 전체 완료 아님** — B 7 · P 2 · F 7 · K 32출현이 열려 있다. 의미 조사·정규화는 시작하지 않았다.

| 단계 | 상태 |
|---|---|
| 전수 읽기 | 원본 전체(한 줄 8,322바이트)를 위에서 아래로 직접 읽음: 메타 3키 → 묶음 8개 순서대로 59항목 전 필드. 이어 review.md §3 전 행과 형태소 출력 전 토큰을 다시 읽음. 별도 검토자 없음 |
| 구조·값 수집 | 노드 415(object 68·array 9·string 297·boolean 41·number 0·null 0) · 키 352 · 중복 키 0 · 빈 값 0 · 이스케이프 0 |
| 형태소·표현 수집 | Kiwi 0.24.1 `cong` 1스레드 · 적용 225값 558토큰(길이 0 토큰 5) · 제외 72값(사유 기록) · 필드명 352출현 제외(사유 기록) · 알려진 오분절·오태깅 32출현 표시(교정 아님) · 표현 701(값 297·문장 8·정규식 248·수동 148) |
| 기계 검증 | verify.py failure_count 0 · 변이 시험 4종 모두 검출 · 재현성 바이트 동일 |
| 읽기 검토 | 작성자 2차 읽기(아래 §4). 수식·조건·부정 탈락 없음 확인, 오분절 영향 기록 |
| 알려진 분석 오류 | K 32출현 (issues.md K) |
| 열린 미결 | B 원문 부족 7 · P 잠정 2 · C 사용자 결정 0(근거 issues.md C) |
| 후속 의미 조사 | F 7 — 시작 안 함 |

기계 검증 통과는 **원문 대응(누락·중복·위치·구간·해시)** 이 맞다는 뜻이다. 의미 해석의 정답이나 정규화 완료가 아니다.

## 1. 실행한 명령 (레포 루트)

```sh
shasum -a 256 orchestration/work/phub-recommend/bronze/phub-ledger/products.json
#  → 090955cccd35468ace2882024f0e0f216d3ebdb58b38d77693c0cf402338b854 (시작)
wc -c …/products.json                   # → 8322
grep -c '\\' …/products.json            # → 0 (이스케이프 없음)
head -c 3 …/products.json | xxd         # → 7b2276 '{"v' (BOM 없음)

# 수집 + 빌드 내 검사 (요약은 build-output.txt)
uv run --python 3.12 --with kiwipiepy==0.24.1 python \
  orchestration/work/phub-ledger-redesign/first-pass/products/build.py      # build_checks_failed 0

# 독립 재검증 (build.py 코드 미사용, 표준 라이브러리, 파일 쓰지 않음, 실패 시 exit 1)
python3 orchestration/work/phub-ledger-redesign/first-pass/products/verify.py  # failure_count 0, exit 0

# 재현성: 산출 JSON·review.md 해시 → build 재실행 → 해시 비교            # → IDENTICAL

# 끝 해시
shasum -a 256 …/products.json            # → 090955cc…b854 (동일)
git status --short -- orchestration/work/phub-recommend   # 변경 없음
```

도구: Python 3.12(uv), kiwipiepy 0.24.1, `Kiwi(model_type="cong", num_workers=1)`, 사용자 사전 없음, `tokenize` 기본 옵션, 오타 교정 미사용. lemma 는 `Token.lemma` 제공값 그대로(작업자 생성 없음). 실제 설정값은 morphology.json `analyzer`.

## 2. 기계 검증 결과 (verify.py)

| 검사 | 방법 | 결과 |
|---|---|---|
| 원본 해시 | source-map 시작/끝·morphology·expressions 기록값 == verify 시작·끝 sha256 | 통과 |
| 크기 | 바이트 8322·코드 포인트 6666 | 통과 |
| 중복 키 | 자체 파서 + `object_pairs_hook` | 0 — 통과 |
| 정방향 | 노드 415 각각 Pointer 해소 → 자료형·값 일치, span 재파싱 값 일치, byte_span 재계산 일치, value_span slice == 값, literal == 원문, 객체 키 순서·배열 길이 일치 | 통과 |
| 역방향 | `json.loads` 전 경로 415 == 노드 집합, 개수 일치, Pointer 유일 | 통과 |
| 키 | 352 = 객체 멤버 수 합, 키 span slice == JSON 키 리터럴, field_name_occurrences 합집합 == 키 위치 | 통과 |
| 형태소 분할 | 문자열 297 = 적용 225 ∪ 제외 72, 서로소, 제외마다 rule·reason, 제외는 버전·날짜·M코드·국가 2자·'-' 만 | 통과 |
| 필드명 | 352출현 모두 제외 기록(사유 FIELDNAME) | 통과 |
| 토큰 구간 | 558토큰: 값 기준 slice == surface, 파일 기준 slice == surface, byte_span 일치, lemma 칸 존재 | 통과(길이 0 토큰 5 — 리쥬란 3·울쎄라·아이닉의 이/VCP) |
| 토큰 커버리지 | 적용 값의 공백 아닌 모든 문자가 토큰 구간에 덮임 | 통과 |
| 오분절 표시 | 32출현 id 유일·status '표시됨(교정 아님)'·영향 기재, 각 토큰 (pointer, span, form, tag) 가 실제 토큰에 존재, morphology.json 내장본 == segmentation-review.json | 통과 |
| 표현 | 701건 slice == text(값·파일 기준), id 유일, (pointer, span, 범주, 방법) 완전 중복 0, 모든 문자열 값에 segment.value | 통과 |
| 수동 표현 | 148 전부 반영, viewpoint 정의 존재 | 통과 |
| 관찰 포인터 | O01~O28 의 모든 Pointer 해소 | 통과 |
| review.md 값 | 말단 값 338개 모두 §1·§3 에 `| 리터럴 | \`Pointer\` |` 행으로 존재 | 통과 |

변이 시험(scratchpad 사본에서, 원 결과는 건드리지 않음): ① source-map 노드 1개 삭제 → `bidirectional nodes` 등 4 FAIL ② 토큰 span 1 늘림 → `tok` 3 FAIL ③ 수동 표현 1건 삭제 → `manual coverage` FAIL ④ 원본에 1바이트 추가 → JSON 파싱 예외로 nonzero 종료. 모두 검출.

빌드 중 발견·수정한 추출 오류 A1~A3 은 issues.md A. A2 는 verify 의 말단 값 대조가 잡았다.

## 3. 수치 재확인

observations 의 개수 서술(공통 키 4, mfds 41·type 25·ingredient 9·note 5·material 5·legal_warning 2·regulatory_status 2, 제조사 문자열 반복 수)은 원본을 `python3` 로 다시 집계해 맞췄다(A3).

## 4. 별도 읽기 검토 (작성자 2차 읽기 — 독립 검토자 아님)

- **문맥 보존**: 모든 문자열 값은 segment.value 로, 2문장 값(legal_warning 2)은 문장 구획으로 보존. source-map 의 각 노드 context 에 묶음·항목 Pointer·항목 name·형제 필드 Pointer 가 있다.
- **수식·조건·부정**: 원본에서 해당 말이 있는 값은 description·note 5·legal_warning 2·regulatory_status 2·manufacturer 일부뿐이다. 다시 읽어 확인한 것 — 부정(유통사 아닌·별도 제품 아님·'주입'이 아닌·허가 없음), 금지(사용 금지), 한정(허가만·로만), 가능성(위반 소지가 있으며), 반복(반복 경고·단속), 조건(시술 표기·광고 시), 선후(MTS·니들RF 후), 의무(표현해야 합니다), 예정(출시 예정), 시간(2026 하반기·2026-07-26), 열린 나열(미국·중국·유럽 등). 모두 manual 표현으로 구간 보존, 형태소에서도 탈락 없음(issues.md K 마지막 문단). 빈도·깊이·정도 같은 수량 수식어(드문·깊게·심한 등)는 이 원장에 **나오지 않는다**.
- **수치·단위**: 숫자는 버전 1.2, 날짜 2026-07-26, 2026(하반기), 이름 속 2(클라리티2), 코드 숫자뿐. 단위·백분율은 원문에 없고 채우지 않았다.
- **오분절 영향**: 수식어 오탐 1(더채움 '더'/MAG), 전문어 오분절 2출현(경피), 원문에 없는 형태소 복원(제테마 저+의, 길이 0 이/VCP 5) 은 영향과 함께 표시. 나머지는 고유명 분절·품사 차이.
- **미검토**: 각 수식이 무엇에 걸리는지(예: '반복' 이 경고·단속 둘 다인지), 항목 간 관계, 개체 동일성은 확정하지 않았다(F2·F3·F7).

## 5. 수정 범위

쓰기는 `orchestration/work/phub-ledger-redesign/first-pass/products/` 안에서만 했다: build.py · verify.py · manual-expressions.json · segmentation-review.json · observations.json(수동 기록) · source-map.json · morphology.json · expressions.json · review.md · build-output.txt(생성) · issues.md · validation.md. 원본·공통 스킬·_RESUME·다른 워커 폴더는 건드리지 않았다. 변이 시험·해시 비교 임시 파일은 세션 scratchpad 에만 두고 지웠다. 커밋·push 없음.
