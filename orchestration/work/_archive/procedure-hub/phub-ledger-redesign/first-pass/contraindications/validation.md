# contraindications.json — 검증 기록

> **1차 범위 종료: 예(코디 확인 전)** · **원장 전체 완료 아님**. 기계 통과는 원문 대응의 검증이지 의미 정답이 아니다.

## 1. 원본 고정

| 항목 | 값 |
|---|---|
| 경로 | `orchestration/work/phub-recommend/bronze/phub-ledger/contraindications.json` |
| 크기 | 6390 bytes · 1줄 압축 JSON · 끝 줄바꿈 없음 · BOM 없음 |
| sha256 (시작 = 끝) | `964b729594b1756036c160823dc2e8d27ea38fe85d7aefb7559733522d7c53c2` — build 시작·끝, verify 시작·끝 모두 같음 |
| 구조 | 노드 221(object 28 · array 1 · string 192) · 말단 192 · 키 출현 193 · 중복 키 0 · 이스케이프 0 · 빈 값/숫자/불리언/null 0 · BMP 밖 문자 0 |

## 2. 실행한 명령

```sh
# 레포 루트에서
uv run --no-project --python 3.12 --with kiwipiepy==0.24.1 python \
  orchestration/work/phub-ledger-redesign/first-pass/contraindications/build.py   # exit 0
python3 orchestration/work/phub-ledger-redesign/first-pass/contraindications/verify.py  # exit 0, VERIFY PASS
```

- 재현성: build 를 두 번 돌려 `source-map.json`·`morphology.json`·`expressions.json`·`coverage.json`·`review.md` sha256 이 같음을 확인(diff 0).
- verify.py 는 표준 라이브러리만 쓰고 파일을 쓰지 않는다. build 의 스캐너 대신 `json.loads(object_pairs_hook)` 로 원본을 따로 열거해 대조한다.

## 3. verify.py 결과 (77 검사 · 실패 0)

| 묶음 | 검사 | 결과 |
|---|---|---|
| 해시 | source-map·coverage·review.md 의 sha256 = 원본, 크기, 끝 시점 불변 | PASS |
| 중복 키 | 독립 파서 감지 0 = 기록 0 | PASS |
| 구조·값 양방향 | 원본 전체 Pointer 집합 ↔ source-map 노드 집합(누락 0·초과 0), 자료형·길이·값 일치, 말단 플래그 | PASS |
| 구간 재현 | 모든 노드 literal_span(코드 포인트)·byte_span(UTF-8 바이트)·문자열 inner 구간이 원문을 그대로 재현, 키 구간 193 | PASS |
| coverage | 구획 소유 말단 합집합 = 원본 말단 192(양방향), 구획 간 중복 소유 0, 컨테이너 소유 양방향, 구획별 `direct_read_done`·review 파일·절 제목 실재, 공유 문맥은 소유하지 않음, 남은 구획 0 | PASS |
| 형태소 적용/제외 | 문자열 192 = 적용 109 + 제외 83(겹침 0), 적용 필드 규칙(description·from_name·to_name·interval·note), 제외 사유 전부 있음, 토큰 구간 `text[start:end] == surface`, 분석기 설정(kiwipiepy 0.24.1·cong·workers 1), 필드명 11개 = 원본 키 집합, 분절 검토 141행 원문 재현 | PASS |
| 표현 | ID 유일, 292개 전부 `value[span] == text` 및 file 구간 재현, 완전 중복 0, 수동 107 = 입력 107(순서·문자열 일치), 수동 표현 ID 가 review.md 에 전부 있음 | PASS |
| review.md | 말단 192 모두 `| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |` 행으로 원문 그대로 있음, rule 27 제목, 잠정 관찰 절 28(S0 + rule 27)로 원문과 분리, known_issue 23출현 표시 | PASS |
| issues.md | 인용한 「`Pointer` [a,b)」 구간이 원문 값 범위 안, 인용 Pointer 실재 | PASS |

출력 끝:

```text
source sha256 964b729594b1756036c160823dc2e8d27ea38fe85d7aefb7559733522d7c53c2
nodes 221 · leaves 192 · owned 192 · morph applied 109 excluded 83 · tokens 741 · expressions 292 (manual 107) · known_issue 23
checks 77 · failed 0
VERIFY PASS
```

## 4. 음성 시험 (verify 가 실제로 잡는지)

세션 scratchpad 에 같은 상대 경로로 원본·결과 사본을 만들어 하나씩 훼손했다(레포 파일은 건드리지 않음).

| 훼손 | 잡힌 검사 |
|---|---|
| review.md 에서 `/rules/13/interval` 행 삭제 | `review.every_leaf_row` FAIL |
| coverage 에서 `/rules/5/note` 소유 제거 + `/rules/6/note` 를 S0 에도 소유 | `coverage.source_leaves_owned`·`coverage.no_duplicate_owner` FAIL |
| expressions `E0005` 구간 시작 +1 | `expr.spans_reproduce` FAIL |
| 사본 원본의 `"safe"` 한 곳을 `"safx"` 로 | `hash.*`·`nodes.type_length_value`·`spans.*` FAIL, exit 1 |

## 5. 별도 읽기 검토

기계 검증과 별개로 원문을 rule 순서대로 다시 읽으며 확인했다.

- **문맥 보존**: 각 rule 은 7칸을 한 표로 묶었고(review.md S1), 원장 설명 `/description` 을 구획 공통 문맥으로 연결했다. source-map 의 각 노드 `context.read_with` 가 같은 rule 의 나머지 칸을 가리킨다.
- **수식·조건·부정·가능성·범위·순서 탈락 점검**: regex 후보 중 의미 표지(가능·수 있음·권장·금지·방지·위험·우려·먼저·순서·후·전·시·다르면·따라 다름·특히·무관·적음·부족·과도한·과-·극대화·강한·완전·이론적·임상 근거·등·→·+·이상·수량·범위·level 코드) 출현이 **전부** 직접 읽기 표현 구간 안에 들어 있음을 확인(미포함 0). 또 모든 interval·note 54값에서 공백·마침표·쉼표를 뺀 모든 글자가 하나 이상의 직접 읽기 표현에 덮인다(미포함 0).
- **형태소 영향**: 오분절이 의미 표지를 지우는 곳을 출현별로 기록했다 — 「PRP는」이 동사 늘다로(없는 서술어 생성), 「열」이 수사 NR(수량 오탐 위험), 「CO2」의 2(수량 오탐 위험), 「니들이」가 대명사(주어 상실), 「실로」 부사(수단 상실), 「MTS.」(문장 경계 상실), 「과-」 명사화(정도 수식 분리). 범위 하한 단위 생략(K3)은 표현 구간이 보존한다. issues.md K1~K4.
- **잠정 해석 근거**: P1~P7 모두 원문 Pointer 를 붙였고 확정 데이터로 쓰지 않았다. 「드물게」류 빈도 표현은 이 원장에 없다. 단위·백분율·부위를 채운 곳 없음.
- **미검토 의미 관계**: level 체계, from/to 방향, 레이저 종류 명칭 동일성, 장비 ↔ 시술 소속, 다른 원장 연결은 **미검토**(F1~F6).

## 6. 상태

| 항목 | 상태 |
|---|---|
| 1차 범위 종료 | **예 — 코디 확인 전** |
| 원장 전체 완료 | **아님** |
| 전수 읽기 | S0·S1 직접 읽기 완료 (coverage.json · reading-log.json) |
| 구조·값 수집 | 완료 — 말단 192 양방향 대응 |
| 형태소·표현 수집 | 적용 109 · 제외 83 · 토큰 741 · 표현 292(수동 107 · regex 185) |
| 기계 검증 | PASS 77/77 · 음성 시험 4건 검출 |
| 읽기 검토 | 완료(§5) |
| 알려진 분석 오류 | K1 23출현 외 K2~K4 — 미교정 |
| 열린 미결 | A 0(해결 1) · B 6 · C 0 · I 3 · P 7 · F 6 · K 4 — 현재 사용자 선택 대기 0 |
| 후속 의미 조사 | F1~F6 |
