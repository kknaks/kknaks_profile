# review — patient-education.json 1차 조사

> **1차 수집 범위: 종료** (아래 상태표 기준) · **원장 전체 완료 아님** — 원문 정보 부족 B·잠정 P·후속 F·원문 표기 이상 I·알려진 분석 한계 K 가 열려 있다. 의미 관계·정규화는 하지 않았다.

- 원본: `orchestration/work/phub-recommend/bronze/phub-ledger/patient-education.json` (읽기 전용)
- sha256 `6c96520c514b76ef7f93d7f685e53023afe91b05133a9b9ca5db0a95d42d91ac` · 26,551 bytes · 13,043 코드포인트 · 한 줄(minified) JSON · 줄바꿈 0 · 백슬래시 이스케이프 0 · 중복 키 0 · BMP 밖 문자 0
- 조사일 2026-11-09 · 이 원장 외 다른 원장은 열지 않았다

## 상태

| 단계 | 상태 |
|---|---|
| 전수 읽기 | 18/18 구획(S00 상위 메타 + S01~S17 카테고리 17개) 원문을 위에서 아래로 직접 읽음. 각 구획 기록은 `manual/S*.json`, 진행은 `progress.md` · `coverage.json` |
| 구조·값 수집 | 노드 327(객체 69·배열 18·문자열 240) · 말단 240 · 빈 컨테이너 0 · 빈 문자열 0 · 숫자/불리언/null 0 — `source-map.json` |
| 형태소 | Kiwi(kiwipiepy 0.24.1, cong, 스레드 1, 사용자 사전 없음) 적용 221값 4,989토큰 · 제외 19값(version·updated·id) · 필드명 14종 제외(영문 식별자) · 알려진 오분절/오태깅 25출현 기록(교정 안 함) — `morphology.json` |
| 표현 수집 | 직접 읽기 표현 806건(문장 231 포함, 겹침 의도) · 보조 정규식 후보 572건(패턴 일치분뿐) 중 수동 구절 밖 49건 전부 판정(문장 단위 보존 43 · 오탐 6) — `expressions.json` |
| 기계 검증 | `verify.py` 34,232검사 실패0(원본 해시 시작/끝 불변·양방향 대조·구간 재현·구획 소유·문서 대조·변이 시험) — `validation.md` |
| 읽기 검토 | 작성자 별도 읽기 검토 1회: 형태소 수식어(MAG·VA·XR·XPN·부정·조건 어미) 대조로 패턴 밖 구절 27건 보충·오태깅 1건 추가. 독립 검토자 검토는 아직 없음 |
| 열린 미결 | B 36 · P 42 · F 10 · I 1 · K 1관찰+25출현 · A 0(발견분 수정) · **C 0** — `issues.md` |
| 후속 의미 조사 | 시작 안 함 |

## 이 원장의 형태 (요약 — 상세 값은 구획 파일)

`{version, updated, categories[17]}`. 각 카테고리는 같은 9키(id·name·patient_name·simple_explanation·how_it_works·duration_simple·pain_level·downtime·common_concerns)를 갖고, `common_concerns` 는 언제나 `{q, a}` 3개다. 모든 말단이 문자열이다. 언어별 필드는 없고 한국어 문장에 라틴 약어(PRP·RF·SMAS·PIH·AHA 등)·제품명·수치가 섞여 있다.

같은 키 이름 아래 정보 종류가 다르다(잠정 관찰): `duration_simple` 은 지속 기간·발현 시점·반복 회차·생착률(%)·최대 효과 시점을 오가고, `downtime`·`pain_level` 은 종류별 세분(「토닝: … / 프락셔널: …」)이 들어간다. `common_concerns/*/a` 에는 행동 지시·금기 대상·근거 서술·규제 서술·위험 목록이 섞여 있다.

## 컬럼 구성 표 (원본 컬럼명/경로 패턴 · 자료형 · 중첩 · 원문 예시와 위치)

`*` 는 배열 인덱스. 출현 수는 원문 실측. 선택적 필드 여부는 상위 객체 수와 출현 수 비교로 판정.

| 경로 패턴 | 원본 컬럼명 | 자료형 | 중첩 구조 | 출현 | 선택적? | 빈 값 | 길이(코드포인트) 최소–최대 | 원문 예시 | 예시 위치 |
|---|---|---|---|---|---|---|---|---|---|
| `/` | (루트) | object | 자식 수 3(×1) | 1 | 아니오(모든 상위 객체에 있음) | 0 |  | (컨테이너) | `/` |
| `/version` | version | string | 말단 | 1 | 아니오(모든 상위 객체에 있음) | 0 | 3–3 | "1.3" | `/version` |
| `/updated` | updated | string | 말단 | 1 | 아니오(모든 상위 객체에 있음) | 0 | 10–10 | "2026-07-26" | `/updated` |
| `/categories` | categories | array | 자식 수 17(×1) | 1 | 아니오(모든 상위 객체에 있음) | 0 |  | (컨테이너) | `/categories` |
| `/categories/*` | * | object | 자식 수 9(×17) | 17 | 아니오(모든 상위 객체에 있음) | 0 |  | (컨테이너) | `/categories/0` |
| `/categories/*/id` | id | string | 말단 | 17 | 아니오(모든 상위 객체에 있음) | 0 | 2–3 | "M1" | `/categories/0/id` |
| `/categories/*/name` | name | string | 말단 | 17 | 아니오(모든 상위 객체에 있음) | 0 | 2–16 | "보톡스" | `/categories/0/name` |
| `/categories/*/patient_name` | patient_name | string | 말단 | 17 | 아니오(모든 상위 객체에 있음) | 0 | 5–21 | "주름 보톡스" | `/categories/0/patient_name` |
| `/categories/*/simple_explanation` | simple_explanation | string | 말단 | 17 | 아니오(모든 상위 객체에 있음) | 0 | 29–56 | "근육을 일시적으로 쉬게 해서 주름을 펴는 주사입니다." | `/categories/0/simple_explanation` |
| `/categories/*/how_it_works` | how_it_works | string | 말단 | 17 | 아니오(모든 상위 객체에 있음) | 0 | 54–151 | "주름을 만드는 근육에 약을 주사하면 근육이 쉬면서 주름이 펴집니다. 칼로 자르거나 꿰매지 않아요." | `/categories/0/how_it_works` |
| `/categories/*/duration_simple` | duration_simple | string | 말단 | 17 | 아니오(모든 상위 객체에 있음) | 0 | 14–141 | "약 3-6개월 지속됩니다." | `/categories/0/duration_simple` |
| `/categories/*/pain_level` | pain_level | string | 말단 | 17 | 아니오(모든 상위 객체에 있음) | 0 | 13–39 | "모기 물린 정도의 따끔함" | `/categories/0/pain_level` |
| `/categories/*/downtime` | downtime | string | 말단 | 17 | 아니오(모든 상위 객체에 있음) | 0 | 11–48 | "바로 일상 복귀 가능" | `/categories/0/downtime` |
| `/categories/*/common_concerns` | common_concerns | array | 자식 수 3(×17) | 17 | 아니오(모든 상위 객체에 있음) | 0 |  | (컨테이너) | `/categories/0/common_concerns` |
| `/categories/*/common_concerns/*` | * | object | 자식 수 2(×51) | 51 | 아니오(모든 상위 객체에 있음) | 0 |  | (컨테이너) | `/categories/0/common_concerns/0` |
| `/categories/*/common_concerns/*/q` | q | string | 말단 | 51 | 아니오(모든 상위 객체에 있음) | 0 | 10–27 | "보톡스 맞으면 표정이 굳나요?" | `/categories/0/common_concerns/0/q` |
| `/categories/*/common_concerns/*/a` | a | string | 말단 | 51 | 아니오(모든 상위 객체에 있음) | 0 | 35–319 | "적절한 양을 맞으면 자연스러운 표정을 유지할 수 있어요. 과도하게 맞는 경우에만 표정이 어색할 수 있습니다." | `/categories/0/common_concerns/0/a` |

## 구획 목차 (모든 값은 review-part-*.md 에 원본 컬럼명 그대로)

| 구획 | 범위 | 소유 노드 | 소유 말단 | 직접 읽기 | 표현 | 관찰 | 파일 |
|---|---|---|---|---|---|---|---|
| S00 | 상위 메타 — / · /version · /updated · /categories 컨테이너 | 4 | 2 | direct_read | 0 | 4 | [review-part-S00.md](./review-part-S00.md) |
| S01 | /categories/0 M1 보톡스 | 19 | 14 | direct_read | 55 | 7 | [review-part-S01.md](./review-part-S01.md) |
| S02 | /categories/1 M2 필러 | 19 | 14 | direct_read | 52 | 6 | [review-part-S02.md](./review-part-S02.md) |
| S03 | /categories/2 M3 바이오스티뮬레이터/콜라겐부스터 | 19 | 14 | direct_read | 55 | 6 | [review-part-S03.md](./review-part-S03.md) |
| S04 | /categories/3 M4 스킨부스터 | 19 | 14 | direct_read | 54 | 6 | [review-part-S04.md](./review-part-S04.md) |
| S05 | /categories/4 M5 PRP/자가혈 | 19 | 14 | direct_read | 42 | 4 | [review-part-S05.md](./review-part-S05.md) |
| S06 | /categories/5 M6 지방이식 | 19 | 14 | direct_read | 48 | 5 | [review-part-S06.md](./review-part-S06.md) |
| S07 | /categories/6 M7 실리프팅 | 19 | 14 | direct_read | 44 | 4 | [review-part-S07.md](./review-part-S07.md) |
| S08 | /categories/7 M8 레이저 | 19 | 14 | direct_read | 54 | 6 | [review-part-S08.md](./review-part-S08.md) |
| S09 | /categories/8 M9 기기 리프팅 | 19 | 14 | direct_read | 45 | 6 | [review-part-S09.md](./review-part-S09.md) |
| S10 | /categories/9 M10 HIFES/EMS | 19 | 14 | direct_read | 37 | 3 | [review-part-S10.md](./review-part-S10.md) |
| S11 | /categories/10 M11 니들RF | 19 | 14 | direct_read | 41 | 4 | [review-part-S11.md](./review-part-S11.md) |
| S12 | /categories/11 M12 마이크로니들링(MTS) | 19 | 14 | direct_read | 41 | 5 | [review-part-S12.md](./review-part-S12.md) |
| S13 | /categories/12 M13 플라즈마 | 19 | 14 | direct_read | 42 | 5 | [review-part-S13.md](./review-part-S13.md) |
| S14 | /categories/13 M14 크라이오리포라이시스 | 19 | 14 | direct_read | 51 | 5 | [review-part-S14.md](./review-part-S14.md) |
| S15 | /categories/14 M15 메디컬스킨케어 | 19 | 14 | direct_read | 45 | 5 | [review-part-S15.md](./review-part-S15.md) |
| S16 | /categories/15 M16 수액치료 | 19 | 14 | direct_read | 45 | 4 | [review-part-S16.md](./review-part-S16.md) |
| S17 | /categories/16 M17 줄기세포치료 | 19 | 14 | direct_read | 55 | 5 | [review-part-S17.md](./review-part-S17.md) |
