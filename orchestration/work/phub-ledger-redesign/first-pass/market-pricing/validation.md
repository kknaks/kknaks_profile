# market-pricing.json — 검증 기록

**1차 범위 종료: 예 · 원장 전체 완료 아님** (열린 B 30 · I 4 · P 12 · F 7 · K 4 · C 0 — [issues.md](issues.md))

## 재현 명령 (레포 루트)

```bash
uv run --python 3.12 --with kiwipiepy==0.24.1 python orchestration/work/phub-ledger-redesign/first-pass/market-pricing/build.py
python3 orchestration/work/phub-ledger-redesign/first-pass/market-pricing/verify.py
```

`verify.py` 는 표준 라이브러리만 쓰고 어떤 파일도 쓰지 않는다. 실패가 하나라도 있으면 exit 1.

## 기계 검증 결과 (2026-11-09 최종 실행)

```
{"checks": 11930, "failures": 0, "source_sha256_start": "601d7e7b…e477", "source_sha256_end": "601d7e7b…e477",
 "nodes": 806, "leaves_and_empty_containers": 648, "containers": 158, "segments": 18, "string_values": 282,
 "morph_applied": 262, "morph_excluded": 20, "tokens": 988, "auto_candidates": 348, "manual_expressions": 250, "issues": 57}
EXIT=0
```

| 검사 | 방법 | 결과 |
|---|---|---|
| 원본 해시 불변 | 시작·끝 sha256 을 기대값 `601d7e7b4db29731bf15304ff3ec9489ba38838e9f5ba2144c2c181cfd15e477` 과 대조, 모든 산출물의 `source_sha256` 대조 | 통과 |
| 중복 키 | `object_pairs_hook` 독립 감지 + build 파서 출현별 기록 | 0 |
| 구조·값 양방향 | 표준 `json` 파서로 독립 Pointer 집합(806)을 만들어 source-map 노드와 양방향 대조, 자료형·값·컨테이너 길이·원문 순서 | 누락 0 · 불필요 0 |
| 구간 재현 | 모든 노드의 코드포인트 구간 = 바이트 구간 디코딩 = 리터럴, 리터럴 재파싱 = 값. 키 666 출현 구간 재파싱 | 통과 |
| 구획 소유 | coverage 말단 집합(648) ↔ 원문, 구획 소유 합집합 ↔ 원문(양방향), 구획 간 중복, 컨테이너 소유, 구획별 direct_read·manual·review 파일·절 실재, 마지막 읽은 Pointer = 구획 끝 말단 | 통과 |
| 변이 시험 | 메모리 안에서 소유 1개 삭제 / 다른 구획 소유 1개 중복 추가 → 검출되는지 | 둘 다 검출 |
| 형태소 적용/제외 | 문자열 말단 282 = 적용 262 ∪ 제외 20 (교집합 0), 숫자 말단 366 목록 일치, 토큰 slice = 원문 구간, 공백 외 모든 문자가 토큰에 덮임, 분석기 설정 기록 | 통과 |
| 알려진 오분절 | 21출현 각각 구간 원문 재현 + 원시 토큰 일치, issues.md 에 출현별 기재 | 통과 |
| 표현 | 자동 후보 348·수동 250 의 구간 원문 재현, 자동 후보를 기록된 패턴으로 독립 재생성해 집합 일치, 수동 표현 ↔ manual/S*.json 1:1 | 통과 |
| 읽기용 문서 | review-part-S00~S17 각각: 루트 4값 행, 카테고리 id·name 행, 항목 122개 전부 `name·unit·low·mid·high` 원문 값 행(정확 문자열), 문자열 값 282개 형태소 행, 관찰·미결 ID. review.md 목차 18구획, issues.md 미결 57 ID | 통과 |

기계 통과는 원문 대응·보존의 검증이다. 의미 해석의 정답·정규화 완료를 뜻하지 않는다.

## 형태소 분석 설정

- kiwipiepy 0.24.1 · `Kiwi(num_workers=1, model_type='cong')` · 기본 사전 · 사용자 사전 없음 · `tokenize()` 기본 옵션 · python 3.12(uv)
- 적용: `/note`, `/categories/*/name`, `/categories/*/items/*/name`, `/categories/*/items/*/unit` (262값)
- 제외(사유는 morphology.json `excluded_strings`): `/version`(버전), `/updated`(날짜), `/currency`(통화 코드), `/categories/*/id`(17 식별자) — 20값
- 숫자 말단 366(low·mid·high) — 분석 대상 아님, 원문 값은 source-map 보존
- 필드명 12종은 `field_names` 에 따로(영문 식별자 → 전부 SL). 언어 텍스트 분석과 역할 구분
- 언어: 한국어 + 영문 약어·영숫자 혼합(HA·PRP·MTS·CO2·FLX·cm2·B1 등). 영문 부분은 Kiwi 가 SL/SN 으로만 표시하며 영어 형태소 분석은 하지 않음(K). 다른 언어 문장 없음
- 기본형은 Kiwi `Token.lemma` 그대로(`lemma_tool`). 도구가 주지 않은 기본형은 만들지 않음. 축약 활용 8토큰은 `form_equals_slice=false` 로 표시

## 자동 후보의 범위 (중요)

`expressions.json` 의 `auto_candidates` 348 은 **기록된 정규식 5종(괄호·숫자+단위·'+'·'/'·키워드)에 실제로 일치한 구간뿐**이다. 패턴 밖 표현은 자동 후보에 없다. 348 전부를 원문과 대조해 읽었고 부분 오탐 1건(`/note` '/' 패턴이 조사 '에'까지 포함)을 `review` 칸에 표시했다.

패턴 밖 표현은 직접 읽기로 따로 모았다 — 수동 250 중 123 은 어떤 자동 후보 구간 안에도 들지 않는다(부위·제품·장비명 후보, '턱 끝'·'허벅지 안쪽'의 위치 수식, '나노'·'고농도'·'소부위'·'프리미엄' 등).

## 읽기 검토 (작성자, 기계 검증과 별개)

1. 18구획을 S00 → S17 순서로 원문 값을 Pointer 와 함께 출력해 읽고, 구획마다 바로 manual/S*.json 에 관찰·표현·미결·마지막 읽은 Pointer 를 저장한 뒤 다음 구획으로 갔다(progress.md).
2. 패턴 밖 수식·조건 재훑기: 원문 전체에서 `약 ~ 최대 최소 부터 까지 정도 깊 얇 두께 빠 서서히 권장 주의 필요 가능 없 않 미만 이하 초과 전 후 회당 별도 포함 추가 % ± × 시` 를 검색 — `후` 1건(`/categories/14/items/5/name` '시술 후', 수집됨), `시)` 1건('동시)', 시간 조건 아님·'동시'로 수집됨) 외 0. 이 원장에는 깊이·두께·속도·근사 표현이 없다(원문 부재 확인이지 미수집이 아님).
3. 수집한 수식·조건·부정: '참고'(회피), '에 따라 상이'(조건), '정가 아닌'(부정), '이상'(하한 범위), '기준'·'부위당'·'1개당'(가격 기준·분모), '시술 후'(시간 조건·참조), '동시'(동시 시행), '비수술'(부정 접두), '고농도'(농도), '소부위'(크기), '나노'(기법 수식), '프리미엄'(등급), '집중'(강도/범위), '강화'·'축소'(효과 방향), '안쪽'·'끝'(위치), '양쪽'(양측성), '전체얼굴'·'풀페이스'·'전신'·'풀코스'(범위), '종합'(구성), '수입'·'국산'(원산지).
4. 수치 주장 재확인: 122항목 low<mid<high, mid=(low+high)/2 는 3항목, 볼·눈밑 지방이식 세 값 동일, 쥬베룩 볼륨 4cc low 가 2cc low 의 2배보다 낮음, 이모드 복부+힙 동시 가격 < 단독 합 — 모두 원문 값으로 확인. 환산·외부 가격 조회 없음.
5. 형태소 원시 결과 262값 전체를 원문과 나란히 읽고 오분절 서명 13종(21출현)을 기록했다. 서명 밖 토큰의 정답성은 보장하지 않는다.

미검토: 시술·부위·고민·제품의 의미 분해와 관계, 원장 간 연결(후속 F).

## 작업 중 고친 것

- verify.py 의 항목 행 계수 조건이 다른 6열 표까지 셌다(검증기 버그, 추출 오류 아님) → 항목 Pointer 정확 일치 정규식으로 고침. 고친 뒤 실패 0.
- 추출 오류(A)로 고친 것은 없다.

## 산출물

review.md(상태·컬럼 구성·목차) · review-part-S00~S17.md · source-map.json · morphology.json · expressions.json · coverage.json · issues.md · validation.md · progress.md · segments.json · manual/(S00~S17·auto-review·cross-issues) · build.py · verify.py · build-output.txt · read_segment.py(구획 읽기 출력 보조, 해석 없음)
