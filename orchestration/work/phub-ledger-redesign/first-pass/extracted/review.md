# extracted.json — 1차 조사 (읽기용)

> **1차 범위: 종료 기준 충족(작성자 자체 판정 · 독립 검토 전 · 코디 확인 전).** **원장 전체 완료 아님** — 열린 미결은 [issues.md](./issues.md)에 있다(원문 부족 B 10 · 원문 내 불일치 I 13 · 잠정 P 4 · 후속 의미 조사 F 11 · 알려진 분석 한계 K 5 · 에이전트 오류 A 3(해결) · 사용자 결정 필요 C 0).
>
> 이 문서는 상태·전체 컬럼 구성·구획 목차를 갖는다. **모든 값은 구획별 `review-part-*.md`** 에 원본 컬럼명·JSON Pointer·자료형·원문 값으로 실려 있고, 잠정 관찰은 각 파일의 별도 절에 있다. 원문 칸과 관찰 칸을 섞지 않는다. 원문의 임상·법적 주장은 **원장에 그렇게 적혀 있다**는 사실로만 기록했다. 사실 여부는 검증하지 않았고 외부 자료로 보충하지 않았다. 공통 개념 ID·동의어·부위 체계·관계 방향은 정하지 않았다(1차 범위 밖).

## 상태

| 구분 | 상태 |
|---|---|
| 1차 범위 종료 | **충족(자체 판정)** — 전 구획 직접 읽기·구조/값 대응·형태소·표현 수집·기계 검증 통과. 독립 읽기 검토는 받지 않았다 |
| 원장 전체 완료 | **아님** — B·I·P·F 미결과 의미 분해·정규화가 남아 있다 |
| 전수 읽기 | 구획 18개(S00 루트 + 항목 17) 전부 직접 읽음. 항목마다 3회(통독 · 값별 표지 기록 · 형태소 대조). [coverage.json](./coverage.json) · [reading-log.json](./reading-log.json) |
| 구조·값 수집 | 노드 958 전부 · 키 출현 445 (서로 다른 키 44) · object 86 · array 153 · string 717 · number 0 · boolean 0 · null 2 · 말단 719 · 빈 값 2(null) · 중복 키 0 · 이스케이프 0 |
| 형태소·표현 수집 | Kiwi 0.24.1(cong, 스레드 1, 사용자 사전 없음) — 분석 648값 9,940토큰 · 제외 71 말단(사유별) · 필드명 44 · 알려진 오분절·오태깅 표시 34출현(**교정 아님**) · 표현 후보 3,907(수동 190 포함) |
| 기계 검증 | [validation.md](./validation.md) — verify.py 실패 0 · 원본 해시 시작·끝 동일 · 변이 시험 검출 |
| 읽기 검토 | 작성자 3회차까지. 독립 검토자 아님 |
| 알려진 분석 오류 | issues K1~K5 (형태소 표시 34출현 · NNP 과다 태깅 미표시 · 규칙 후보 오탐 미판정 등) |
| 열린 미결 | B 10 · I 13 · P 4 · F 11 · C 0 — [issues.md](./issues.md) |
| 후속 의미 조사 | 시작 안 함 |
| 마지막 읽은 위치 | {"section": "S17", "pointer": "/M9/related_techniques/3", "pass": "3회차", "note": "전 구획 3회차까지 완료. 남은 구획 없음."} |

## 0. 원본과 기록 위치

| 항목 | 값 |
|---|---|
| 원본 | `orchestration/work/phub-recommend/bronze/phub-ledger/extracted.json` (읽기 전용) |
| 크기 | 56,589 bytes · 29,178 code points · UTF-8 · BOM 없음 · 개행 없는 한 줄 · 이스케이프 0 · BMP 밖 문자 0 · `\|` 0 |
| sha256 | `b829d499e3e3fd7f6119f2dc23092cf50f7c13e57ee18e9d3131a14c7e350f2c` (작업 시작·끝 동일) |
| 구조·값 | [source-map.json](./source-map.json) — 모든 노드(Pointer·자료형·값·리터럴·코드 포인트/바이트 구간·키 구간·문맥 참조·구획) · 필드명 출현 위치 |
| 구획 대응 | [coverage.json](./coverage.json) — 구획별 소유 Pointer 집합·말단·문맥 참조·읽기 상태·review 파일 |
| 형태소 | [morphology.json](./morphology.json) — 분석·제외·필드명·알려진 오분절 표시(원본 [segmentation-review.json](./segmentation-review.json)) |
| 복합 표현 | [expressions.json](./expressions.json) — 규칙 후보 + 수동 구절(원본 [manual-expressions.json](./manual-expressions.json)) |
| 잠정 관찰 | 각 `review-part-*.md` §2 (원본 [manual-observations.json](./manual-observations.json), 76건) |
| 미결 · 검증 | [issues.md](./issues.md) · [validation.md](./validation.md) |
| 재현 | [build.py](./build.py)(`uv run --python 3.12 --with kiwipiepy==0.24.1 python …/build.py`) · [verify.py](./verify.py)(`python3 …/verify.py`) |

구간 기준: 디코딩된 원문 문자열의 Unicode 코드 포인트 `[start,end)`. source-map 의 `span` 은 파일 전체 텍스트 기준(따옴표 포함 리터럴), `value_span` 은 따옴표 안쪽, `byte_span` 은 UTF-8 바이트다. morphology·expressions 의 `span` 은 그 값 문자열 기준이다(파일 위치 = `value_span[0] + start`). 이스케이프가 없어 디코딩 문자열과 리터럴 안쪽이 글자 단위로 같다(`decoded_equals_literal_inner`).

## 1. 읽기 범위와 구획

**구획 분할:** 원장은 최상위 객체 하나에 시술 항목 17개다. 항목 하나가 1,256~2,165자로 한 번에 전부 읽을 수 있어 **항목 하나 = 구획 하나**로 정했다(문장 중간 자르기 없음). S00 은 루트 객체 노드만 소유하고, 항목 구획은 루트를 문맥으로 참조만 한다. 각 항목의 `name`·`procedure_id` 는 그 구획이 소유하면서 구획 안 모든 값의 문맥으로 참조한다.

| 회차 | 범위 | 방식 |
|---|---|---|
| 1 | 전 구획 | 항목 객체를 키 순서대로 출력해 2~3개 항목씩 순차로 위에서 아래로 읽음(묶음 6회) |
| 2 | 전 구획 | 값마다 다시 열어 조건·부정·가능성·범위·시간·부위 역할·참조·하위 유형·근거 표지를 원문 인용으로 기록(수동 표현 190 · 관찰 76) |
| 3 | 분석 대상 전부 | 의심 품사(NNP·NR·MM·NP·MAJ·XR·SW·W_SERIAL·불규칙 활용 태그 등) 전 출현과 전문어·부위어·부작용어·부정/가능성 표지 약 170개 낱말의 모든 출현을 원문 어절과 대조 → 오분절 규칙 20 · 출현 34 |

- **자동 처리:** 구조 열거 · Pointer · 구간 · 해시 · 형태소 분석 · regex/keyword 후보 · 수동 인용 위치 찾기 · coverage 생성.
- **직접 읽기:** 위 세 회차. 3회차 범위 밖 토큰의 정확성은 보장하지 않는다.
- **한계:** 「별도 읽기 검토」는 같은 작성자가 관점을 바꿔 다시 읽은 것이다.

### 구획 목차

| 구획 | 항목 | 소유 Pointer | 노드 수 | 직접 읽기 | 값·관찰 위치 |
|---|---|---|---|---|---|
| S00 | (루트) | `""` | 1 | 직접 읽음 | 이 문서 §S00 |
| S01 | `M10` HIFES/EMS | `/M10` … | 50 (말단 37) | 직접 읽음 | [review-part-01-M10.md](./review-part-01-M10.md) |
| S02 | `M11` 니들RF | `/M11` … | 53 (말단 39) | 직접 읽음 | [review-part-02-M11.md](./review-part-02-M11.md) |
| S03 | `M12` MTS (마이크로니들 치료) | `/M12` … | 54 (말단 40) | 직접 읽음 | [review-part-03-M12.md](./review-part-03-M12.md) |
| S04 | `M13` 플라즈마 | `/M13` … | 44 (말단 31) | 직접 읽음 | [review-part-04-M13.md](./review-part-04-M13.md) |
| S05 | `M14` 크라이오리포라이시스 | `/M14` … | 52 (말단 38) | 직접 읽음 | [review-part-05-M14.md](./review-part-05-M14.md) |
| S06 | `M15` 메디컬스킨케어 | `/M15` … | 64 (말단 50) | 직접 읽음 | [review-part-06-M15.md](./review-part-06-M15.md) |
| S07 | `M16` 수액치료 | `/M16` … | 53 (말단 39) | 직접 읽음 | [review-part-07-M16.md](./review-part-07-M16.md) |
| S08 | `M17` 줄기세포치료 | `/M17` … | 47 (말단 33) | 직접 읽음 | [review-part-08-M17.md](./review-part-08-M17.md) |
| S09 | `M1` 보톡스 | `/M1` … | 72 (말단 58) | 직접 읽음 | [review-part-09-M1.md](./review-part-09-M1.md) |
| S10 | `M2` 필러 | `/M2` … | 64 (말단 49) | 직접 읽음 | [review-part-10-M2.md](./review-part-10-M2.md) |
| S11 | `M3` 바이오스티뮬레이터 | `/M3` … | 57 (말단 43) | 직접 읽음 | [review-part-11-M3.md](./review-part-11-M3.md) |
| S12 | `M4` 스킨부스터 | `/M4` … | 58 (말단 44) | 직접 읽음 | [review-part-12-M4.md](./review-part-12-M4.md) |
| S13 | `M5` PRP 피부재생술 | `/M5` … | 50 (말단 36) | 직접 읽음 | [review-part-13-M5.md](./review-part-13-M5.md) |
| S14 | `M6` 지방이식 | `/M6` … | 53 (말단 39) | 직접 읽음 | [review-part-14-M6.md](./review-part-14-M6.md) |
| S15 | `M7` 실리프팅 | `/M7` … | 65 (말단 51) | 직접 읽음 | [review-part-15-M7.md](./review-part-15-M7.md) |
| S16 | `M8` 레이저 | `/M8` … | 64 (말단 49) | 직접 읽음 | [review-part-16-M8.md](./review-part-16-M8.md) |
| S17 | `M9` 기기리프팅 | `/M9` … | 57 (말단 43) | 직접 읽음 | [review-part-17-M9.md](./review-part-17-M9.md) |

### S00 루트

| # | 원본 컬럼명 | JSON Pointer | 자료형 | 원문 값 |
|---|---|---|---|---|
| 1 | (루트) | `""` | object | (object · 17) — 키: M10, M11, M12, M13, M14, M15, M16, M17, M1, M2, M3, M4, M5, M6, M7, M8, M9 |

## 2. 구조 — 원문 대응

### 2.1 컬럼 구성 표

`<항목 키>` 는 최상위 키(M1~M17)다. 「출현」은 노드 수, 「항목」은 그 경로가 있는 항목이다. 원문 예시가 길면 80자에서 끊었고 전체 값은 구획 파일에 있다.

| 원본 컬럼명(경로 패턴) | JSON Pointer 패턴 | 자료형 | 중첩 구조 | 출현 | 항목 | 원문 예시 | 예시 위치 |
|---|---|---|---|---|---|---|---|
| `(루트)` | `""` | object | 키: M10, M11, M12, M13, M14, M15, M16, M17, M1, M2, M3, M4, M5, M6, M7, M8, M9 · 길이 17~17 | 1 | (루트) | (object · 17) | `""` |
| `<항목 키>` | `/M\d+` | object | 키 구성 변형 2종(§2.2) · 길이 15~16 | 17 | 전 항목(17) | (object · 15) | `/M10` |
| `<항목 키>.name` | `/M\d+/name` | string | 스칼라 | 17 | 전 항목(17) | HIFES/EMS | `/M10/name` |
| `<항목 키>.safety` | `/M\d+/safety` | object | 키 구성 변형 2종(§2.2) · 길이 3~4 | 17 | 전 항목(17) | (object · 3) | `/M10/safety` |
| `<항목 키>.safety.common` | `/M\d+/safety/common` | array | 문자열 배열 · 길이 2~7 | 17 | 전 항목(17) | (array · 3) | `/M10/safety/common` |
| `<항목 키>.safety.common[]` | `/M\d+/safety/common/\d+` | string | 스칼라 | 59 | 전 항목(17) | 시술 부위 근육통 (운동 후와 비슷한 느낌) | `/M10/safety/common/0` |
| `<항목 키>.safety.serious` | `/M\d+/safety/serious` | null | 스칼라 | 2 | 항목 M10, M13 | null | `/M10/safety/serious` |
| `<항목 키>.safety.uncommon` | `/M\d+/safety/uncommon` | array | 문자열 배열 · 길이 1~5 | 17 | 전 항목(17) | (array · 2) | `/M10/safety/uncommon` |
| `<항목 키>.safety.uncommon[]` | `/M\d+/safety/uncommon/\d+` | string | 스칼라 | 45 | 전 항목(17) | 시술 부위 피부 발적 (빨개짐) | `/M10/safety/uncommon/0` |
| `<항목 키>.source` | `/M\d+/source` | string | 스칼라 | 17 | 전 항목(17) | 일반 의학 지식 | `/M10/source` |
| `<항목 키>.name_en` | `/M\d+/name_en` | string | 스칼라 | 17 | 전 항목(17) | High-Intensity Focused Electromagnetic Stimulation / EMS | `/M10/name_en` |
| `<항목 키>.overview` | `/M\d+/overview` | string | 스칼라 | 17 | 전 항목(17) | HIFES(고강도 집속 전자기 자극)와 EMS(전기근육자극)는 전자기 에너지를 이용해 근육을 강제로 수축시키는 시술이다. 한국에서는 '엠스컬프' …(전체는 해당 구획 표) | `/M10/overview` |
| `<항목 키>.aftercare` | `/M\d+/aftercare` | array | 문자열 배열 · 길이 2~5 | 17 | 전 항목(17) | (array · 3) | `/M10/aftercare` |
| `<항목 키>.aftercare[]` | `/M\d+/aftercare/\d+` | string | 스칼라 | 53 | 전 항목(17) | 특별한 다운타임 없이 일상생활 바로 가능 | `/M10/aftercare/0` |
| `<항목 키>.mechanism` | `/M\d+/mechanism` | string | 스칼라 | 17 | 전 항목(17) | 고강도 집속 전자기장(HIFEM)이 운동신경을 자극하여 단시간에 수만 회의 근육 초극대 수축(supramaximal contraction)을 유 …(전체는 해당 구획 표) | `/M10/mechanism` |
| `<항목 키>.indications` | `/M\d+/indications` | object | 키: primary, extended · 길이 2~2 | 17 | 전 항목(17) | (object · 2) | `/M10/indications` |
| `<항목 키>.indications.primary` | `/M\d+/indications/primary` | array | 문자열 배열 · 길이 2~5 | 17 | 전 항목(17) | (array · 3) | `/M10/indications/primary` |
| `<항목 키>.indications.primary[]` | `/M\d+/indications/primary/\d+` | string | 스칼라 | 56 | 전 항목(17) | 복부 근육 강화 및 지방 감소 | `/M10/indications/primary/0` |
| `<항목 키>.indications.extended` | `/M\d+/indications/extended` | array | 문자열 배열 · 길이 3~19 | 17 | 전 항목(17) | (array · 4) | `/M10/indications/extended` |
| `<항목 키>.indications.extended[]` | `/M\d+/indications/extended/\d+` | string | 스칼라 | 101 | 전 항목(17) | 팔뚝 근육 토닝 | `/M10/indications/extended/0` |
| `<항목 키>.source_type` | `/M\d+/source_type` | string | 스칼라 | 17 | 전 항목(17) | general | `/M10/source_type` |
| `<항목 키>.extracted_at` | `/M\d+/extracted_at` | string | 스칼라 | 17 | 전 항목(17) | 2026-03-28 | `/M10/extracted_at` |
| `<항목 키>.procedure_id` | `/M\d+/procedure_id` | string | 스칼라 | 17 | 전 항목(17) | M10-HIFES | `/M10/procedure_id` |
| `<항목 키>.onset_duration` | `/M\d+/onset_duration` | object | 키: peak, onset, duration · 길이 3~3 | 17 | 전 항목(17) | (object · 3) | `/M10/onset_duration` |
| `<항목 키>.onset_duration.peak` | `/M\d+/onset_duration/peak` | string | 스칼라 | 17 | 전 항목(17) | 마지막 시술 후 2~4주 뒤 | `/M10/onset_duration/peak` |
| `<항목 키>.onset_duration.onset` | `/M\d+/onset_duration/onset` | string | 스칼라 | 17 | 전 항목(17) | 시술 직후 근육 피로감, 2~4주 후 근육 강화 체감 | `/M10/onset_duration/onset` |
| `<항목 키>.onset_duration.duration` | `/M\d+/onset_duration/duration` | string | 스칼라 | 17 | 전 항목(17) | 6~12개월 유지 (운동 병행 시 더 오래 유지) | `/M10/onset_duration/duration` |
| `<항목 키>.contraindications` | `/M\d+/contraindications` | object | 키: absolute, relative · 길이 2~2 | 17 | 전 항목(17) | (object · 2) | `/M10/contraindications` |
| `<항목 키>.contraindications.absolute` | `/M\d+/contraindications/absolute` | array | 문자열 배열 · 길이 2~4 | 17 | 전 항목(17) | (array · 3) | `/M10/contraindications/absolute` |
| `<항목 키>.contraindications.absolute[]` | `/M\d+/contraindications/absolute/\d+` | string | 스칼라 | 53 | 전 항목(17) | 체내 금속 임플란트가 시술 부위에 있는 경우 | `/M10/contraindications/absolute/0` |
| `<항목 키>.contraindications.relative` | `/M\d+/contraindications/relative` | array | 문자열 배열 · 길이 2~6 | 17 | 전 항목(17) | (array · 3) | `/M10/contraindications/relative` |
| `<항목 키>.contraindications.relative[]` | `/M\d+/contraindications/relative/\d+` | string | 스칼라 | 55 | 전 항목(17) | 간질(뇌전증) 환자 | `/M10/contraindications/relative/0` |
| `<항목 키>.guardrail_version` | `/M\d+/guardrail_version` | string | 스칼라 | 17 | 전 항목(17) | 1.0 | `/M10/guardrail_version` |
| `<항목 키>.related_techniques` | `/M\d+/related_techniques` | array | 문자열 배열 · 길이 2~4 | 17 | 전 항목(17) | (array · 3) | `/M10/related_techniques` |
| `<항목 키>.related_techniques[]` | `/M\d+/related_techniques/\d+` | string | 스칼라 | 51 | 전 항목(17) | 크라이오리포라이시스 (냉동지방분해) -- 지방 감소에 병합 | `/M10/related_techniques/0` |
| `<항목 키>.safety.serious` | `/M\d+/safety/serious` | array | 문자열 배열 · 길이 1~5 | 15 | 항목 M1, M2, M3, M4, M5, M6, M7, M8, M9, M11, M12, M14, M15, M16, M17 | (array · 2) | `/M11/safety/serious` |
| `<항목 키>.safety.serious[]` | `/M\d+/safety/serious/\d+` | string | 스칼라 | 37 | 항목 M1, M2, M3, M4, M5, M6, M7, M8, M9, M11, M12, M14, M15, M16, M17 | 감염 (1회용 팁 사용으로 위생 관리) | `/M11/safety/serious/0` |
| `<항목 키>.safety.emergency` | `/M\d+/safety/emergency` | array | 문자열 배열 · 길이 1~1 | 2 | 항목 M2, M8 | (array · 1) | `/M2/safety/emergency` |
| `<항목 키>.safety.emergency[]` | `/M\d+/safety/emergency/\d+` | string | 스칼라 | 2 | 항목 M2, M8 | 주사 직후 피부가 하얗게 변하면 혈관이 막혔을 가능성 — 즉시 히알루로니다아제(분해효소) 투여 필요 | `/M2/safety/emergency/0` |
| `<항목 키>.updated` | `/M\d+/updated` | string | 스칼라 | 1 | 항목 M3 | 2026-07-11 | `/M3/updated` |

### 2.2 객체 키 구성 변형

| 경로 패턴 | 키 수 | 키(원문 순서) | 객체 수 | Pointer |
|---|---|---|---|---|
| `(루트)` | 17 | `M10, M11, M12, M13, M14, M15, M16, M17, M1, M2, M3, M4, M5, M6, M7, M8, M9` | 1 | `""` |
| `<항목 키>` | 15 | `name, safety, source, name_en, overview, aftercare, mechanism, indications, source_type, extracted_at, procedure_id, onset_duration, contraindications, guardrail_version, related_techniques` | 16 | `/M10`, `/M11`, `/M12`, `/M13`, `/M14`, `/M15`, `/M16`, `/M17`, `/M1`, `/M2`, `/M4`, `/M5`, `/M6`, `/M7`, `/M8`, `/M9` |
| `<항목 키>.safety` | 3 | `common, serious, uncommon` | 15 | `/M10/safety`, `/M11/safety`, `/M12/safety`, `/M13/safety`, `/M14/safety`, `/M15/safety`, `/M16/safety`, `/M17/safety`, `/M1/safety`, `/M3/safety`, `/M4/safety`, `/M5/safety`, `/M6/safety`, `/M7/safety`, `/M9/safety` |
| `<항목 키>.indications` | 2 | `primary, extended` | 17 | `/M10/indications`, `/M11/indications`, `/M12/indications`, `/M13/indications`, `/M14/indications`, `/M15/indications`, `/M16/indications`, `/M17/indications`, `/M1/indications`, `/M2/indications`, `/M3/indications`, `/M4/indications`, `/M5/indications`, `/M6/indications`, `/M7/indications`, `/M8/indications`, `/M9/indications` |
| `<항목 키>.onset_duration` | 3 | `peak, onset, duration` | 17 | `/M10/onset_duration`, `/M11/onset_duration`, `/M12/onset_duration`, `/M13/onset_duration`, `/M14/onset_duration`, `/M15/onset_duration`, `/M16/onset_duration`, `/M17/onset_duration`, `/M1/onset_duration`, `/M2/onset_duration`, `/M3/onset_duration`, `/M4/onset_duration`, `/M5/onset_duration`, `/M6/onset_duration`, `/M7/onset_duration`, `/M8/onset_duration`, `/M9/onset_duration` |
| `<항목 키>.contraindications` | 2 | `absolute, relative` | 17 | `/M10/contraindications`, `/M11/contraindications`, `/M12/contraindications`, `/M13/contraindications`, `/M14/contraindications`, `/M15/contraindications`, `/M16/contraindications`, `/M17/contraindications`, `/M1/contraindications`, `/M2/contraindications`, `/M3/contraindications`, `/M4/contraindications`, `/M5/contraindications`, `/M6/contraindications`, `/M7/contraindications`, `/M8/contraindications`, `/M9/contraindications` |
| `<항목 키>.safety` | 4 | `common, serious, uncommon, emergency` | 2 | `/M2/safety`, `/M8/safety` |
| `<항목 키>` | 16 | `name, safety, source, name_en, updated, overview, aftercare, mechanism, indications, source_type, extracted_at, procedure_id, onset_duration, contraindications, guardrail_version, related_techniques` | 1 | `/M3` |

### 2.3 형태소 분석 적용·제외

| 대상 | 처리 | 사유 |
|---|---|---|
| name · overview · mechanism · source · safety/* · aftercare/* · indications/* · onset_duration/* · contraindications/* · related_techniques/* | 분석 | 언어 텍스트 |
| name_en 17 | 분석(원시 결과만) | 영문 시술명. Kiwi 는 SL 토큰을 준다 — 영어 형태 분석이 아니다(K4) |
| procedure_id 17 | 제외 | 코드값(Mxx-영문 대문자) |
| extracted_at 17 · updated 1 | 제외 | 날짜값 |
| guardrail_version 17 | 제외 | 버전 문자열 |
| source_type 17 | 제외 | 열거 코드값(kr/general/us) |
| safety/serious = null 2 | 제외 | 문자열 아님(값 보존) |
| 필드명 | 분석(별도) | 영문 식별자·항목 키. Kiwi 결과와 `_` 분할을 함께 남기며 뜻은 정하지 않음 |

표현 후보 범주별 수: causal_marker 28 · comparison_contrast 52 · condition_scope 186 · course_duration_marker 62 · cross_reference_name 137 · degree_adverb_extra 46 · endpoint_addition_marker 10 · evidence_marker 10 · frequency_degree 182 · latin_term 170 · manual.alternative 1 · manual.alternative_with_frequency 1 · manual.causal 1 · manual.combination_purpose 1 · manual.comparison_condition 1 · manual.comparison_contrast 3 · manual.comparison_degree 1 · manual.comparison_limit_site 1 · manual.comparison_possibility 1 · manual.condition 1 · manual.condition_alternative 1 · manual.condition_combination 2 · manual.condition_combination_recommendation 1 · manual.condition_duration 1 · manual.condition_effect 4 · manual.condition_possibility_causal 1 · manual.condition_threshold_time_window 2 · manual.condition_time 1 · manual.condition_with_remedy 1 · manual.count_anchor 1 · manual.count_time 1 · manual.course_frequency 1 · manual.course_frequency_time 1 · manual.degree_condition 1 · manual.degree_effect_shortfall 1 · manual.degree_scope 1 · manual.degree_site_condition 1 · manual.depth_condition 1 · manual.duration_modifier_scoped 2 · manual.efficacy_in_contraindication 1 · manual.event_with_gloss_comparison 1 · manual.evidence_gap_statement 2 · manual.exception_qualifier 1 · manual.field_content_without_time 2 · manual.frequency_course_scoped 1 · manual.frequency_degree_scoped 6 · manual.frequency_degree_scoped_condition 2 · manual.frequency_duration_scoped 1 · manual.frequency_severity_contrast 1 · manual.frequency_severity_scoped 1 · manual.historical_claim 6 · manual.history_condition_obligation 1 · manual.ingredient_condition 1 · manual.ingredient_condition_risk 1 · manual.interval 1 · manual.management_in_safety 1 · manual.medication_condition 1 · manual.medication_condition_risk 1 · manual.medication_possibility 1 · manual.medication_possibility_obligation 2 · manual.medication_time_window 1 · manual.named_variant_with_ingredient 1 · manual.negated_causal 2 · manual.negated_comparison 1 · manual.negated_condition 5 · manual.negated_evidence_statement 3 · manual.negated_prefix_gloss 1 · manual.negated_safety_claim 1 · manual.negated_statement 6 · manual.negated_threshold_condition 2 · manual.obligation 1 · manual.optional_instruction 1 · manual.permission_vs_avoidance 1 · manual.population_frequency 1 · manual.population_recommendation 2 · manual.population_subgroup 1 · manual.population_subtype_risk 1 · manual.possibility_condition 2 · manual.possibility_obligation 1 · manual.possibility_statement 3 · manual.possibility_variability 1 · manual.possibility_with_time 2 · manual.prevention_in_safety_paren 1 · manual.quantity_approx 1 · manual.quantity_comparison 1 · manual.quantity_threshold 1 · manual.quantity_threshold_interval 1 · manual.quantity_with_target 6 · manual.quantity_word_scoped 2 · manual.regulatory_claim_scoped 1 · manual.scope_inclusion 1 · manual.selectivity_negated_prefix 1 · manual.sequence_after 2 · manual.sequence_hyphen 1 · manual.sign_condition_possibility 1 · manual.sign_condition_urgent_action 1 · manual.site_condition 1 · manual.site_condition_frequency 1 · manual.site_list_purpose 1 · manual.site_mention 1 · manual.site_restriction 1 · manual.site_role 3 · manual.site_role_condition 1 · manual.speed_modifier_scoped 1 · manual.subtype_condition 5 · manual.subtype_depth_range 3 · manual.subtype_test_condition 1 · manual.subtype_time 6 · manual.symbol_combination 1 · manual.symbol_conjunction_time 1 · manual.thickness_site_caution 1 · manual.threshold_unspecified 1 · manual.time_and_degree_scoped 1 · manual.time_degree_avoidance 1 · manual.time_degree_negated_instruction 1 · manual.time_order_mismatch 1 · manual.time_range 2 · manual.time_range_word 2 · manual.time_site_degree 1 · manual.time_subtype_condition 1 · manual.time_vague_condition_risk 1 · manual.time_vague_site_condition 1 · manual.time_window_avoidance 3 · manual.time_window_with_anchor 9 · manual.time_with_condition 2 · manual.time_with_variability 1 · manual.urgent_action 1 · negation 69 · obligation_recommendation 84 · population_subgroup 77 · possibility_uncertainty 61 · quantity_unit_time 97 · quantity_word 12 · quoted_name 24 · range 71 · scope_restriction 27 · segment.clause 441 · segment.parenthetical 353 · segment.sentence 107 · segment.value 717 · site_or_layer_keyword 239 · state_marker 18 · symbol_relation 200 · time_relative 229 · year_date 8. 범주는 탐색용 후보이며 분류가 확정된 것이 아니다. 같은 구간이 여러 범주에 겹치는 것은 의도했고, 같은 (Pointer, 구간, 범주) 중복 생성은 0 이다. 규칙은 원문 문자열에 직접 적용했고 형태소 품사를 쓰지 않았다(형태소 오분절이 표현 후보로 옮겨 가지 않는다). `cross_reference_name` 은 이 원장 `/Mx/name` 값·약칭과 같은 문자열일 뿐 관계 확정이 아니다.

## 3. 전역 잠정 관찰 (원문과 분리)

분류 문자: 구조 = 원장 구조 사실 · P 잠정 · B 원문 정보 부족 · F 후속 의미 조사 · I 원문 내 불일치 · K 분석 한계. 항목별 관찰은 각 구획 파일 §2 에 있다.

- **OB-S00-01** (구조) 최상위는 객체 하나이고 키 17개(M10, M11, …, M17, M1, …, M9 — 숫자 순이 아니라 문자열 정렬 순)다. 각 키 값은 시술 항목 객체다. 키 이름과 항목 안 procedure_id 의 접두(Mxx-)가 같다.  
  근거: `/M10/procedure_id` 「M10-HIFES」; `/M1/procedure_id` 「M1-BOTOX」
- **OB-S00-02** (구조) 16개 항목은 키 15개가 같은 순서(name, safety, source, name_en, overview, aftercare, mechanism, indications, source_type, extracted_at, procedure_id, onset_duration, contraindications, guardrail_version, related_techniques)다. M3 만 name_en 뒤에 updated 가 하나 더 있다. → B9  
  근거: `/M3/updated` 「2026-07-11」
- **OB-S00-03** (구조) safety 는 common·serious·uncommon 3키가 기본이고 M2·M8 에만 emergency 가 추가된다. serious 는 M10·M13 에서 null 이고 나머지는 문자열 배열이다. 빈 배열·빈 문자열·숫자·불리언은 없다. → B1  
  근거: `/M10/safety/serious`; `/M13/safety/serious`; `/M2/safety/emergency/0` 「즉시 히알루로니다아제」
- **OB-S00-04** (B) safety 의 common/uncommon/serious 구분 기준(빈도·중증도 중 무엇인지)과 indications 의 primary/extended, contraindications 의 absolute/relative 기준이 원장에 정의돼 있지 않다. 그룹 이름은 영문 키뿐이다. → B1, B8  
  근거: `/M10/safety`; `/M10/indications`; `/M10/contraindications`
- **OB-S00-05** (구조) extracted_at 은 17개 모두 "2026-03-28", guardrail_version 은 17개 모두 "1.0" 이다. source_type 은 kr 11 · general 5 · us 1 이다. 각 코드의 뜻은 원장에 없다. → B9  
  근거: `/M7/source_type` 「us」; `/M10/source_type` 「general」
- **OB-S00-06** (P) related_techniques 값은 대부분 「기법명 + 구분자 + 관계 설명」 꼴이다. 구분자는 「 -- 」 와 「 — 」 두 가지가 항목에 따라 섞인다. 구분자 앞을 기법명 후보, 뒤를 관계 설명 후보로 읽을 수 있으나 관계 종류(병합·시너지·대안·비교·설명)는 자유 서술이다. → F6, F7  
  근거: `/M10/related_techniques/0` 「 -- 」; `/M12/related_techniques/0` 「 — 」
- **OB-S00-07** (P) safety·contraindications·indications 항목 안의 괄호는 역할이 여러 가지다 — 쉬운 말 풀이(빨개짐), 조건(부적절한 에너지 설정 시), 빈도(극히 드묾), 예방 메모(1회용 팁 사용으로 위생 관리), 하위 유형(모노실), 성분(글루타치온, 비타민C). 괄호 = 한 가지 역할로 다루면 뜻이 섞인다. → F4  
  근거: `/M11/safety/common/0` 「(빨개짐)」; `/M11/safety/serious/1` 「(부적절한 에너지 설정 시)」; `/M11/safety/serious/0` 「(1회용 팁 사용으로 위생 관리)」
- **OB-S00-08** (P) README 의 「+ = 함께 시술 / / = 둘 중 하나」 규칙이 이 원장 값에 그대로 맞지 않는 출현이 있다 — 「+」가 효과 두 가지 병렬(M3 onset), 「/」가 나열·병기(리프팅/타이트닝, 손끝/발끝, 진정/살균). 기호만으로 의미 관계를 정하지 않았다. → F7  
  근거: `/M3/onset_duration/onset` 「즉각적 볼륨 효과 + 콜라겐 재생은」; `/M11/indications/primary/1` 「리프팅/타이트닝」; `/M14/contraindications/relative/0` 「손끝/발끝」
- **OB-S00-09** (F) 같은 조건이 항목마다 다른 금기 등급에 있다 — 켈로이드 체질(M11 relative 단서 포함 · M12·M2·M3·M7 absolute · M15 relative · M8 absolute(박피형 레이저 시)), 당뇨병(M4 absolute · M12 absolute「조절이 안 되는」 · M16·M6 relative), 비현실적·과도한 기대(M1 absolute · M15 relative). 시술이 달라 불일치로 단정하지 않는다. → F9  
  근거: `/M11/contraindications/relative/0` 「켈로이드 체질」; `/M12/contraindications/absolute/3` 「켈로이드 체질」; `/M4/contraindications/absolute/1` 「당뇨병 환자」; `/M16/contraindications/relative/1` 「당뇨병 환자」; `/M1/contraindications/absolute/3` 「비현실적인 기대」; `/M15/contraindications/relative/3` 「과도한 기대」
- **OB-S00-10** (F) 표기 변형이 항목 사이에 있다 — 래디에스/래디어스, 레이저 토닝/레이저토닝, 손등회춘술/손등 회춘술, 자외선 차단제/자외선차단제/썬크림, SVF(기질혈관분획)/SVF(기질혈관분획) 치료법, 자가지방이식/지방이식, MTS(마이크로니들링)/MTS (마이크로니들 치료). → F7, I2  
  근거: `/M2/mechanism` 「래디에스」; `/M3/overview` 「래디어스」; `/M13/related_techniques/1` 「레이저 토닝」; `/M15/related_techniques/1` 「레이저토닝」; `/M9/aftercare/2` 「썬크림」; `/M6/related_techniques/1` 「SVF(기질혈관분획)」; `/M17/related_techniques/1` 「SVF(기질혈관분획) 치료법」
