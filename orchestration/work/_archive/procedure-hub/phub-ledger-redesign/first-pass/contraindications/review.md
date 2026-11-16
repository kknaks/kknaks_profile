# contraindications.json — 1차 조사 (읽기용)

> **1차 범위 종료: 예(코디 확인 전)** · **원장 전체 완료 아님** — 의미 모델·정규화·관계 확정은 하지 않았다. 미결은 [issues.md](./issues.md).

- 원본: `orchestration/work/phub-recommend/bronze/phub-ledger/contraindications.json` · 6390 bytes · sha256 `964b729594b1756036c160823dc2e8d27ea38fe85d7aefb7559733522d7c53c2` · 1줄 압축 JSON · 끝 줄바꿈 없음 · BOM 없음
- 노드 221 · 말단 192 · 키 출현 193 · 중복 키 0 · 이스케이프 0 · 빈 값 0
- 구간 단위: span_cp = 디코딩된 원문 문자열의 Unicode 코드 포인트 [start,end) (시작 포함·끝 제외). file_span_cp = 원본 파일 텍스트(UTF-8 디코딩) 전체 기준 코드 포인트 [start,end). byte_span = 원본 파일 UTF-8 바이트 [start,end). literal_span = JSON 리터럴(따옴표 포함) 의 file 코드 포인트 구간. 이 파일은 이스케이프 0 · BMP 밖 문자 0 이라 문자열 내부 리터럴 = 디코딩 문자열이고 코드 포인트 = UTF-16 코드 단위(빌드가 검사).
- 기계 기록: [source-map.json](./source-map.json) · [morphology.json](./morphology.json) · [expressions.json](./expressions.json) · [coverage.json](./coverage.json) · 검증 [validation.md](./validation.md)

## 상태

- **1차 범위 종료**: 예 — 코디 확인 전. 원장 전체 완료 아님
- **전수 읽기**: S0·S1 두 구획 모두 직접 읽기 완료(27 rule × 7칸 + 메타 3)
- **구조·값 수집**: 노드 221 · 말단 192 · 키 출현 193 · 중복 키 0 · 이스케이프 0 — source-map.json
- **형태소·표현 수집**: 언어 텍스트 109값 Kiwi(cong) 분석 · 토큰 741 · 제외 83값(ID·코드·날짜·버전) 사유 기록 · 필드명 11개 별도 · 직접 표현 107 + regex 후보 185
- **기계 검증**: verify.py PASS — validation.md
- **읽기 검토**: 수식·조건·부정·가능성·범위·순서 표현을 rule 별로 대조. 결과 validation.md §5
- **알려진 분석 오류**: Kiwi 오분절/오태깅 known_issue 23출현 — issues.md K1 (원시 출력 미교정)
- **열린 미결**: A 0(해결 1) · B 6 · C 0 · I 3 · P 7 · F 6 · K 4 — issues.md. 현재 사용자 선택 대기 0(미결이 닫혔다는 뜻 아님)
- **후속 의미 조사**: level 체계·from/to 방향·분기 interval·레이저 종류 명칭·다른 원장 참조 — issues.md F

## 구획 목차

| 구획 | 원문 Pointer 범위 | 소유 말단 수 | 직접 읽기 | 절 |
|---|---|---|---|---|
| S0 | `/version · /updated · /description · /rules(컨테이너)` | 3 | direct_read_done | [S0 · 최상위 메타데이터](#s0--최상위-메타데이터) |
| S1 | `/rules/0 … /rules/26 (각 7키)` | 189 | direct_read_done | [S1 · rules 전체](#s1--rules-전체) |

## 컬럼 구성 표

| 원본 컬럼명 / JSON 경로 패턴 | 자료형 · 중첩 | 출현 | 값 형태 변형 | 원문 예시 | 예시 위치 |
|---|---|---|---|---|---|
| version | string · 최상위 객체 키 | 1 | — | 1.1 | `/version` |
| updated | string(날짜형) · 최상위 | 1 | — | 2026-07-11 | `/updated` |
| description | string · 최상위 | 1 | — | 시술 간 금기/주의사항/간격 매트릭스 | `/description` |
| rules | array · 최상위 · 원소 object 27개 | 1 | 빈 배열 아님 | (27 object) | `/rules` |
| rules/* | object · 7키 고정 순서 from, from_name, to, to_name, level, interval, note | 27 | 선택적 필드 없음 · 키 순서 27개 동일 | {from:M1,…} | `/rules/0` |
| rules/*/from | string · ID 코드 M+숫자 | 27 | M1·M2·M3·M4·M5·M6·M7·M8·M9 (from 에 M11·M12 없음) | M1 | `/rules/0/from` |
| rules/*/from_name | string · 시술명 | 27 | 한글 단독 / 한글+'/'+한글 / 한글+괄호 영문 / 공백 포함 | 바이오스티뮬레이터/콜라겐부스터 | `/rules/11/from_name` |
| rules/*/to | string · ID 코드 | 27 | M2·M4·M7·M8·M9·M11·M12 (to 에 M1·M3·M5·M6 없음) | M11 | `/rules/5/to` |
| rules/*/to_name | string · 시술명 | 27 | 한글 단독 / 한글+영문 혼합 / 괄호 영문 | 마이크로니들링(MTS) | `/rules/10/to_name` |
| rules/*/level | string · 영문 코드 | 27 | caution 14 · safe 8 · warning 5 (build 집계) | caution | `/rules/1/level` |
| rules/*/interval | string · 간격 구절 | 27 | '같은 날 가능' / 'N주 간격 권장' / 'N~M주 간격(권장)' / 'N주·N개월 이상(간격)' / 'N개월 간격' / 분기형 '조건: 값 / 조건: 값' | 2~4주 간격 권장 | `/rules/7/interval` |
| rules/*/interval (분기형) | string · 한 칸 안 ' / ' 로 분기 2개, 각 분기 '조건: 값' | 2 | rule 2(같은 날·괄호 순서 포함), rule 12 | 비침습/프락셔널 논어블레이티브: 2~4주 / 어블레이티브(프락셔널 CO2/Er:YAG 등): 3~4개월 | `/rules/12/interval` |
| rules/*/note | string · 1~4 문장, 마침표 구분 | 27 | 근거·순서(→)·조건·예외(괄호)·level 코드 언급 | 동일 부위는 보톡스 먼저 → 필러 순서 권장. 주입 부위가 다르면 순서 무관 | `/rules/0/note` |

빈 문자열·빈 배열·빈 객체·null·숫자·불리언: **없음**(빌드 집계 0). 선택적 필드: **없음** — 27개 rule 모두 같은 7개 키를 같은 순서로 가진다.

## S0 · 최상위 메타데이터

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| version | `/version` | string | 1.1 |
| updated | `/updated` | string | 2026-07-11 |
| description | `/description` | string | 시술 간 금기/주의사항/간격 매트릭스 |
| rules | `/rules` | array(object) 길이 27 | (S1) |

**잠정 관찰 (원문 아님)**

- description 은 '금기/주의사항/간격'을 말하지만 level 값은 safe/caution/warning 셋이며 '금기'로 표시된 값은 없다(I1·F1).
- updated 2026-07-11 · version 1.1 — 변경 이력은 원장 안에 없다(README 의 CHANGELOG 는 이번 범위 밖).

**직접 읽기 표현** (`/description`)

- `E0000` [0,20) 「시술 간 금기/주의사항/간격 매트릭스」 — whole_value, scope, separator_slash · 관찰: 원장 전체 범위 서술. '/' 3항 나열. level 값에는 금기에 해당하는 별도 값이 없다(I1·B1 참고).
- `E0001` [5,15) 「금기/주의사항/간격」 — separator_slash, enumeration · 관찰: '/'가 README 의 '둘 중 하나'인지 단순 나열인지 원문으로 확정 불가(P).
- `E0002` [0,4) 「시술 간」 — scope, relation_between_procedures

## S1 · rules 전체

구획 공통 문맥: `/description`(「시술 간 금기/주의사항/간격 매트릭스」). 각 rule 은 원본 배열 순서대로다.

### /rules/0

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/0/from` | string | M1 |
| from_name | `/rules/0/from_name` | string | 보톡스 |
| to | `/rules/0/to` | string | M2 |
| to_name | `/rules/0/to_name` | string | 필러 |
| level | `/rules/0/level` | string | safe |
| interval | `/rules/0/interval` | string | 같은 날 가능 |
| note | `/rules/0/note` | string | 동일 부위는 보톡스 먼저 → 필러 순서 권장. 주입 부위가 다르면 순서 무관 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0003 | `/rules/0/interval` | [0,7) | 같은 날 가능 | time, same_day, possibility |
| E0004 | `/rules/0/note` | [0,24) | 동일 부위는 보톡스 먼저 → 필러 순서 권장 | condition, body_area_like, order_sequence, recommendation, arrow |
| E0005 | `/rules/0/note` | [0,6) | 동일 부위는 | condition, body_area_like |
| E0006 | `/rules/0/note` | [26,42) | 주입 부위가 다르면 순서 무관 | condition, body_area_like, order_sequence, negation_like |
| E0007 | `/rules/0/note` | [26,36) | 주입 부위가 다르면 | condition |

**잠정 관찰 (원문 아님)**

- note 의 순서(보톡스 먼저)는 from→to 순서와 같다. 비교: rule 3·6·13 은 반대 순서(P2).
- `E0004`: 조건(동일 부위)이 붙은 순서 권장. 보톡스=from_name, 필러=to_name 과 같은 순서.
- `E0005`: 부위가 특정되지 않은 상대 조건.
- `E0006`: '무관' = 순서 제약 없음. 앞 문장과 대비되는 조건 분기.

### /rules/1

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/1/from` | string | M1 |
| from_name | `/rules/1/from_name` | string | 보톡스 |
| to | `/rules/1/to` | string | M7 |
| to_name | `/rules/1/to_name` | string | 실리프팅 |
| level | `/rules/1/level` | string | caution |
| interval | `/rules/1/interval` | string | 2주 간격 권장 |
| note | `/rules/1/note` | string | 보톡스가 안정화된 후 실리프팅. 동시 시술 시 보톡스 확산 위험 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0008 | `/rules/1/interval` | [0,8) | 2주 간격 권장 | quantity_time, recommendation |
| E0009 | `/rules/1/note` | [0,16) | 보톡스가 안정화된 후 실리프팅 | order_sequence, time_relative |
| E0010 | `/rules/1/note` | [18,35) | 동시 시술 시 보톡스 확산 위험 | condition, risk, same_day |
| E0011 | `/rules/1/note` | [18,25) | 동시 시술 시 | condition |

**잠정 관찰 (원문 아님)**

- `E0009`: 보톡스 먼저. '안정화' 시점은 원문에 기간 없음.

### /rules/2

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/2/from` | string | M1 |
| from_name | `/rules/2/from_name` | string | 보톡스 |
| to | `/rules/2/to` | string | M8 |
| to_name | `/rules/2/to_name` | string | 레이저 |
| level | `/rules/2/level` | string | safe |
| interval | `/rules/2/interval` | string | 비박리·비박리 프락셔널: 같은 날 가능(레이저 먼저 → 보톡스 순서 권장) / 박리 CO2·Er:YAG: 3일~1주 간격 권장 |
| note | `/rules/2/note` | string | 비박리·비박리 프락셔널 레이저와 보톡스의 같은 날 병행은 안전하며 레이저 후 냉각·부기를 고려해 레이저 먼저, 보톡스 다음 순서를 권장. 레이저 열에 의한 보톡스 확산 우려는 이론적이며 임상 근거가 부족. 박리 레이저(CO2/Er:YAG)는 부기·조직 부종 때문에 3일~1주 caution 유지 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0012 | `/rules/2/interval` | [0,41) | 비박리·비박리 프락셔널: 같은 날 가능(레이저 먼저 → 보톡스 순서 권장) | branch, subtype_like, same_day, order_sequence, parenthetical |
| E0013 | `/rules/2/interval` | [0,12) | 비박리·비박리 프락셔널 | subtype_like, enumeration |
| E0014 | `/rules/2/interval` | [22,40) | 레이저 먼저 → 보톡스 순서 권장 | order_sequence, recommendation, arrow |
| E0015 | `/rules/2/interval` | [41,44) |  /  | branch_separator, separator_slash |
| E0016 | `/rules/2/interval` | [44,70) | 박리 CO2·Er:YAG: 3일~1주 간격 권장 | branch, subtype_like, range, quantity_time, recommendation |
| E0017 | `/rules/2/interval` | [44,57) | 박리 CO2·Er:YAG | subtype_like, device_like, enumeration |
| E0018 | `/rules/2/interval` | [59,64) | 3일~1주 | range, quantity_time, mixed_unit |
| E0019 | `/rules/2/note` | [0,36) | 비박리·비박리 프락셔널 레이저와 보톡스의 같은 날 병행은 안전하며 | subtype_like, same_day, assessment |
| E0020 | `/rules/2/note` | [37,75) | 레이저 후 냉각·부기를 고려해 레이저 먼저, 보톡스 다음 순서를 권장 | order_sequence, reason, recommendation |
| E0021 | `/rules/2/note` | [77,113) | 레이저 열에 의한 보톡스 확산 우려는 이론적이며 임상 근거가 부족 | evidence_hedge, negation_like, mechanism |
| E0022 | `/rules/2/note` | [115,164) | 박리 레이저(CO2/Er:YAG)는 부기·조직 부종 때문에 3일~1주 caution 유지 | subtype_like, reason, range, level_code_in_text |
| E0023 | `/rules/2/note` | [122,132) | CO2/Er:YAG | device_like, separator_slash, parenthetical |
| E0024 | `/rules/2/note` | [154,164) | caution 유지 | level_code_in_text |

**잠정 관찰 (원문 아님)**

- level=safe 이나 interval 이 두 분기이고 둘째 분기(박리)는 '3일~1주 간격 권장', note 는 'caution 유지'라 적는다 — 한 rule 의 level 칸 하나가 두 분기를 다 담지 못한다(I2).
- interval 은 'CO2·Er:YAG', note 는 'CO2/Er:YAG' — 같은 대상에 구분자가 다르다(I3).
- '박리/비박리'(rule 2)와 '어블레이티브/논어블레이티브'(rule 12·21)가 같은 구분인지 원문은 말하지 않는다(F4).
- `E0012`: interval 칸 안 첫 분기. 순서는 레이저(to) 먼저.
- `E0013`: '비박리'와 '비박리 프락셔널' 두 항 나열로 읽힘(P). 같은 말 반복이 오기인지 원문으로 확정 불가.
- `E0015`: 공백 둘린 '/'가 분기 구분자로 쓰임. 같은 값 안 'CO2·Er:YAG'는 '·'.
- `E0016`: 둘째 분기.
- `E0017`: note 에서는 'CO2/Er:YAG'로 구분자가 다르다.
- `E0018`: 하한·상한 단위가 다르다(일·주).
- `E0021`: 근거 수준에 대한 원문 진술. 근거 출처는 원문에 없음.
- `E0022`: note 안에 level 코드 'caution'이 등장. 이 rule 의 level 칸은 'safe'(I1).

알려진 형태소 오분절 (원시 출력 · 미교정)

- `/rules/2/interval` [0,3) 「비박리」 → 비/XPN + 박/NNG + 리/XSN — 비/XPN+박/NNG+리/XSN — '박리'(ablative 의미로 쓰인 말)가 깨져 비박리·박리 대비가 토큰에서 사라진다
- `/rules/2/interval` [4,7) 「비박리」 → 비/XPN + 박/NNG + 리/XSN — 비/XPN+박/NNG+리/XSN — '박리'(ablative 의미로 쓰인 말)가 깨져 비박리·박리 대비가 토큰에서 사라진다
- `/rules/2/note` [0,3) 「비박리」 → 비/XPN + 박/NNG + 리/XSN — 비/XPN+박/NNG+리/XSN — '박리'(ablative 의미로 쓰인 말)가 깨져 비박리·박리 대비가 토큰에서 사라진다
- `/rules/2/note` [4,7) 「비박리」 → 비/XPN + 박/NNG + 리/XSN — 비/XPN+박/NNG+리/XSN — '박리'(ablative 의미로 쓰인 말)가 깨져 비박리·박리 대비가 토큰에서 사라진다
- `/rules/2/interval` [44,46) 「re:(?<!비)박리」 → 박/NNP + 리/NNG — 박/NNG|NNP+리 로 분절 — 레이저 종류 구분어가 토큰으로 남지 않는다
- `/rules/2/note` [115,117) 「re:(?<!비)박리」 → 박/NNG + 리/XSN — 박/NNG|NNP+리 로 분절 — 레이저 종류 구분어가 토큰으로 남지 않는다
- `/rules/2/interval` [47,50) 「CO2」 → CO/SL + 2/SN — CO/SL+2/SN — 장비명 안 숫자 2가 수량 후보로 오탐될 수 있다
- `/rules/2/note` [122,125) 「CO2」 → CO/SL + 2/SN — CO/SL+2/SN — 장비명 안 숫자 2가 수량 후보로 오탐될 수 있다
- `/rules/2/interval` [51,57) 「Er:YAG」 → Er/SL + :/SP + YAG/SL — Er/SL+:/SP+YAG/SL — 장비명이 기호로 쪼개지고 ':'가 분기 구분 ':'와 같은 태그가 된다
- `/rules/2/note` [126,132) 「Er:YAG」 → Er/SL + :/SP + YAG/SL — Er/SL+:/SP+YAG/SL — 장비명이 기호로 쪼개지고 ':'가 분기 구분 ':'와 같은 태그가 된다

### /rules/3

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/3/from` | string | M1 |
| from_name | `/rules/3/from_name` | string | 보톡스 |
| to | `/rules/3/to` | string | M9 |
| to_name | `/rules/3/to_name` | string | 기기 리프팅 |
| level | `/rules/3/level` | string | caution |
| interval | `/rules/3/interval` | string | 2주 간격 권장 |
| note | `/rules/3/note` | string | HIFU/RF의 열에너지가 보톡스 단백질에 영향. 리프팅 안정화 후 보톡스 시술 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0025 | `/rules/3/interval` | [0,8) | 2주 간격 권장 | quantity_time, recommendation |
| E0026 | `/rules/3/note` | [0,26) | HIFU/RF의 열에너지가 보톡스 단백질에 영향 | mechanism, device_like, separator_slash |
| E0027 | `/rules/3/note` | [0,7) | HIFU/RF | device_like, separator_slash |
| E0028 | `/rules/3/note` | [28,44) | 리프팅 안정화 후 보톡스 시술 | order_sequence, time_relative |

**잠정 관찰 (원문 아님)**

- 순서: 리프팅(to) 먼저 → 보톡스(from) — from/to 와 반대(P2).
- `E0026`: to_name '기기 리프팅'의 구체 표현으로 읽힘(P). 원문에 소속 관계 명시 없음.
- `E0028`: to(기기 리프팅) 먼저 → from(보톡스). from/to 순서와 반대(P2).

### /rules/4

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/4/from` | string | M1 |
| from_name | `/rules/4/from_name` | string | 보톡스 |
| to | `/rules/4/to` | string | M4 |
| to_name | `/rules/4/to_name` | string | 스킨부스터 |
| level | `/rules/4/level` | string | safe |
| interval | `/rules/4/interval` | string | 같은 날 가능 |
| note | `/rules/4/note` | string | 주입 깊이가 달라 상호 영향 적음 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0029 | `/rules/4/interval` | [0,7) | 같은 날 가능 | time, same_day, possibility |
| E0030 | `/rules/4/note` | [0,18) | 주입 깊이가 달라 상호 영향 적음 | reason, degree, negation_like |
| E0031 | `/rules/4/note` | [10,18) | 상호 영향 적음 | degree |

**잠정 관찰 (원문 아님)**

- `E0030`: '적음'은 없음이 아니라 정도 표현.

### /rules/5

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/5/from` | string | M1 |
| from_name | `/rules/5/from_name` | string | 보톡스 |
| to | `/rules/5/to` | string | M11 |
| to_name | `/rules/5/to_name` | string | 니들RF |
| level | `/rules/5/level` | string | caution |
| interval | `/rules/5/interval` | string | 2주 간격 권장 |
| note | `/rules/5/note` | string | 니들RF의 열과 침습이 보톡스 확산에 영향 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0032 | `/rules/5/interval` | [0,8) | 2주 간격 권장 | quantity_time, recommendation |
| E0033 | `/rules/5/note` | [0,23) | 니들RF의 열과 침습이 보톡스 확산에 영향 | mechanism |

**잠정 관찰 (원문 아님)**

- 순서·이유의 방향(무엇이 먼저인지) 진술 없음(B3).
- `E0033`: 순서 진술 없음.

알려진 형태소 오분절 (원시 출력 · 미교정)

- `/rules/5/note` [6,11) 「열과 침습」 → 열/NR + 과/JC + 침습/NNG — 열/NR(수사 10) — 열(heat)이 숫자로 오태깅. 수량 오탐 가능

### /rules/6

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/6/from` | string | M2 |
| from_name | `/rules/6/from_name` | string | 필러 |
| to | `/rules/6/to` | string | M7 |
| to_name | `/rules/6/to_name` | string | 실리프팅 |
| level | `/rules/6/level` | string | safe |
| interval | `/rules/6/interval` | string | 같은 날 가능 |
| note | `/rules/6/note` | string | 실로 올리고 필러로 채우는 보완적 조합. 실 먼저 → 필러 순서 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0034 | `/rules/6/interval` | [0,7) | 같은 날 가능 | time, same_day, possibility |
| E0035 | `/rules/6/note` | [0,21) | 실로 올리고 필러로 채우는 보완적 조합 | mechanism, combination |
| E0036 | `/rules/6/note` | [23,35) | 실 먼저 → 필러 순서 | order_sequence, arrow |

**잠정 관찰 (원문 아님)**

- 순서: 실(to) 먼저 → 필러(from) — from/to 와 반대(P2).
- `E0036`: to(실리프팅) 먼저. from/to 순서와 반대(P2). '권장' 등 서술어 없음.

알려진 형태소 오분절 (원시 출력 · 미교정)

- `/rules/6/note` [0,6) 「실로 올리고」 → 실로/MAG + 올리/VV + 고/EC — 실로/MAG(부사 '실로') — '실(thread)+로'가 사라져 수단 표현이 없어진다

### /rules/7

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/7/from` | string | M2 |
| from_name | `/rules/7/from_name` | string | 필러 |
| to | `/rules/7/to` | string | M8 |
| to_name | `/rules/7/to_name` | string | 레이저 |
| level | `/rules/7/level` | string | caution |
| interval | `/rules/7/interval` | string | 2~4주 간격 권장 |
| note | `/rules/7/note` | string | 레이저 열이 HA 필러를 분해할 수 있음. 특히 프락셔널, IPL은 4주 간격 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0037 | `/rules/7/interval` | [0,10) | 2~4주 간격 권장 | range, quantity_time, recommendation |
| E0038 | `/rules/7/note` | [0,22) | 레이저 열이 HA 필러를 분해할 수 있음 | possibility, mechanism, subtype_like |
| E0039 | `/rules/7/note` | [7,12) | HA 필러 | subtype_like |
| E0040 | `/rules/7/note` | [24,43) | 특히 프락셔널, IPL은 4주 간격 | condition, subtype_like, quantity_time, exception |
| E0041 | `/rules/7/note` | [27,36) | 프락셔널, IPL | subtype_like, enumeration |

**잠정 관찰 (원문 아님)**

- interval '2~4주' 와 note 의 '특히 프락셔널, IPL은 4주' — 범위 안 값 선택 조건이 note 에만 있다(P5).
- `E0038`: 'HA 필러'로 대상이 좁혀짐. 다른 필러 재질에 대한 진술 없음(B).
- `E0040`: interval 범위(2~4주)의 상한을 특정 종류에 적용하는 것으로 읽힘(P).
- `E0041`: IPL 이 '레이저' 범주에 포함되는지 원문은 나열만 한다(F).

### /rules/8

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/8/from` | string | M2 |
| from_name | `/rules/8/from_name` | string | 필러 |
| to | `/rules/8/to` | string | M9 |
| to_name | `/rules/8/to_name` | string | 기기 리프팅 |
| level | `/rules/8/level` | string | warning |
| interval | `/rules/8/interval` | string | 4주 이상 간격 |
| note | `/rules/8/note` | string | HIFU/RF의 강한 열이 HA 필러를 분해·변형시킬 위험. 필러 안정화 후 시술 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0042 | `/rules/8/interval` | [0,8) | 4주 이상 간격 | range, lower_bound, quantity_time |
| E0043 | `/rules/8/note` | [0,32) | HIFU/RF의 강한 열이 HA 필러를 분해·변형시킬 위험 | risk, mechanism, degree, device_like, subtype_like |
| E0044 | `/rules/8/note` | [22,27) | 분해·변형 | enumeration |
| E0045 | `/rules/8/note` | [34,45) | 필러 안정화 후 시술 | order_sequence, time_relative |

**잠정 관찰 (원문 아님)**

- `E0042`: '권장' 없음.
- `E0045`: 필러(from) 먼저.

### /rules/9

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/9/from` | string | M2 |
| from_name | `/rules/9/from_name` | string | 필러 |
| to | `/rules/9/to` | string | M11 |
| to_name | `/rules/9/to_name` | string | 니들RF |
| level | `/rules/9/level` | string | warning |
| interval | `/rules/9/interval` | string | 4주 이상 간격 |
| note | `/rules/9/note` | string | 니들이 필러 주입부를 관통할 위험 + RF 열이 필러에 영향 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0046 | `/rules/9/interval` | [0,8) | 4주 이상 간격 | range, lower_bound, quantity_time |
| E0047 | `/rules/9/note` | [0,33) | 니들이 필러 주입부를 관통할 위험 + RF 열이 필러에 영향 | risk, mechanism, separator_plus |
| E0048 | `/rules/9/note` | [4,10) | 필러 주입부 | body_area_like |

**잠정 관찰 (원문 아님)**

- note 의 '+'는 두 이유 연결. README '+ = 함께 시술'과 다른 쓰임(P3).
- `E0047`: '+'가 두 이유를 잇는다. README 의 '+ = 함께 시술'과 다른 쓰임(P3).

알려진 형태소 오분절 (원시 출력 · 미교정)

- `/rules/9/note` [0,3) 「니들이」 → 니/NP + 들/XSN + 이/JKS — 니/NP+들/XSN — '니들'(침)이 대명사+복수로 오분석. 주어 대상이 사라진다

### /rules/10

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/10/from` | string | M2 |
| from_name | `/rules/10/from_name` | string | 필러 |
| to | `/rules/10/to` | string | M12 |
| to_name | `/rules/10/to_name` | string | 마이크로니들링(MTS) |
| level | `/rules/10/level` | string | caution |
| interval | `/rules/10/interval` | string | 2주 간격 권장 |
| note | `/rules/10/note` | string | 미세침이 필러 주입 부위를 자극할 수 있음 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0049 | `/rules/10/interval` | [0,8) | 2주 간격 권장 | quantity_time, recommendation |
| E0050 | `/rules/10/note` | [0,23) | 미세침이 필러 주입 부위를 자극할 수 있음 | possibility, mechanism |
| E0051 | `/rules/10/note` | [5,13) | 필러 주입 부위 | body_area_like |

**잠정 관찰 (원문 아님)**

- (별도 관찰 없음)

### /rules/11

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/11/from` | string | M3 |
| from_name | `/rules/11/from_name` | string | 바이오스티뮬레이터/콜라겐부스터 |
| to | `/rules/11/to` | string | M9 |
| to_name | `/rules/11/to_name` | string | 기기 리프팅 |
| level | `/rules/11/level` | string | caution |
| interval | `/rules/11/interval` | string | 4주 간격 권장 |
| note | `/rules/11/note` | string | 콜라겐 생성 과정 중 과도한 열자극 방지 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0052 | `/rules/11/interval` | [0,8) | 4주 간격 권장 | quantity_time, recommendation |
| E0053 | `/rules/11/note` | [0,22) | 콜라겐 생성 과정 중 과도한 열자극 방지 | time_relative, degree, prevention |
| E0054 | `/rules/11/note` | [12,19) | 과도한 열자극 | degree |

**잠정 관찰 (원문 아님)**

- (별도 관찰 없음)

### /rules/12

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/12/from` | string | M3 |
| from_name | `/rules/12/from_name` | string | 바이오스티뮬레이터/콜라겐부스터 |
| to | `/rules/12/to` | string | M8 |
| to_name | `/rules/12/to_name` | string | 레이저 |
| level | `/rules/12/level` | string | caution |
| interval | `/rules/12/interval` | string | 비침습/프락셔널 논어블레이티브: 2~4주 / 어블레이티브(프락셔널 CO2/Er:YAG 등): 3~4개월 |
| note | `/rules/12/note` | string | 비침습·프락셔널 논어블레이티브 레이저는 2~4주 간격 유지. 어블레이티브 박피 레이저는 콜라겐 리모델링·미세구 안정화 고려 3~4개월 권장 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0055 | `/rules/12/interval` | [0,22) | 비침습/프락셔널 논어블레이티브: 2~4주 | branch, subtype_like, range, quantity_time, separator_slash |
| E0056 | `/rules/12/interval` | [0,16) | 비침습/프락셔널 논어블레이티브 | subtype_like, separator_slash, scope_ambiguity |
| E0057 | `/rules/12/interval` | [18,22) | 2~4주 | range, quantity_time |
| E0058 | `/rules/12/interval` | [22,25) |  /  | branch_separator, separator_slash |
| E0059 | `/rules/12/interval` | [25,57) | 어블레이티브(프락셔널 CO2/Er:YAG 등): 3~4개월 | branch, subtype_like, range, quantity_time, parenthetical, open_list |
| E0060 | `/rules/12/interval` | [32,49) | 프락셔널 CO2/Er:YAG 등 | device_like, open_list, parenthetical |
| E0061 | `/rules/12/interval` | [52,57) | 3~4개월 | range, quantity_time |
| E0062 | `/rules/12/note` | [0,32) | 비침습·프락셔널 논어블레이티브 레이저는 2~4주 간격 유지 | subtype_like, range, quantity_time |
| E0063 | `/rules/12/note` | [34,77) | 어블레이티브 박피 레이저는 콜라겐 리모델링·미세구 안정화 고려 3~4개월 권장 | subtype_like, reason, range, quantity_time, recommendation |
| E0064 | `/rules/12/note` | [49,65) | 콜라겐 리모델링·미세구 안정화 | enumeration, mechanism |
| E0065 | `/rules/12/note` | [58,61) | 미세구 | term_unclear |

**잠정 관찰 (원문 아님)**

- interval 분기 조건의 수식 범위 모호(F3). '미세구' 뜻 불명(B4).
- `E0055`: '비침습/프락셔널 논어블레이티브'의 수식 범위가 모호: (비침습)|(프락셔널 논어블레이티브) 또는 (비침습|프락셔널) 논어블레이티브(F3).
- `E0056`: note 에서는 '비침습·프락셔널 논어블레이티브'.
- `E0058`: 같은 값에서 '/'가 분기 구분(공백 있음)과 항목 대안(공백 없음) 두 가지로 쓰인다.
- `E0060`: '등' = 열린 목록.
- `E0065`: rule 14 의 '미세구멍'과 같은 뜻인지(잘림 여부) 원문으로 확정 불가(B4). 고치지 않는다.

알려진 형태소 오분절 (원시 출력 · 미교정)

- `/rules/12/interval` [37,40) 「CO2」 → CO/SL + 2/SN — CO/SL+2/SN — 장비명 안 숫자 2가 수량 후보로 오탐될 수 있다
- `/rules/12/interval` [41,47) 「Er:YAG」 → Er/SL + :/SP + YAG/SL — Er/SL+:/SP+YAG/SL — 장비명이 기호로 쪼개지고 ':'가 분기 구분 ':'와 같은 태그가 된다

### /rules/13

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/13/from` | string | M4 |
| from_name | `/rules/13/from_name` | string | 스킨부스터 |
| to | `/rules/13/to` | string | M8 |
| to_name | `/rules/13/to_name` | string | 레이저 |
| level | `/rules/13/level` | string | safe |
| interval | `/rules/13/interval` | string | 1주 간격 권장 |
| note | `/rules/13/note` | string | 스킨부스터 안정화 후 레이저. 순서: 레이저 → 스킨부스터도 가능 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0066 | `/rules/13/interval` | [0,8) | 1주 간격 권장 | quantity_time, recommendation |
| E0067 | `/rules/13/note` | [0,15) | 스킨부스터 안정화 후 레이저 | order_sequence, time_relative |
| E0068 | `/rules/13/note` | [17,36) | 순서: 레이저 → 스킨부스터도 가능 | order_sequence, arrow, possibility, alternative |

**잠정 관찰 (원문 아님)**

- level=safe 인데 interval 은 '1주 간격 권장' — safe 가 같은 날 가능을 뜻하지 않는 사례(P4). 순서 두 방향 모두 가능.
- `E0066`: level=safe 인데 같은 날이 아니라 1주 간격(P4).
- `E0068`: 두 순서 모두 허용으로 읽힘. 역순일 때 간격이 같은지는 원문에 없음(B).

### /rules/14

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/14/from` | string | M4 |
| from_name | `/rules/14/from_name` | string | 스킨부스터 |
| to | `/rules/14/to` | string | M12 |
| to_name | `/rules/14/to_name` | string | 마이크로니들링(MTS) |
| level | `/rules/14/level` | string | safe |
| interval | `/rules/14/interval` | string | 같은 날 가능 |
| note | `/rules/14/note` | string | MTS로 미세구멍 → 스킨부스터 흡수 극대화. 시너지 조합 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0069 | `/rules/14/interval` | [0,7) | 같은 날 가능 | time, same_day, possibility |
| E0070 | `/rules/14/note` | [0,24) | MTS로 미세구멍 → 스킨부스터 흡수 극대화 | mechanism, arrow, degree |
| E0071 | `/rules/14/note` | [26,32) | 시너지 조합 | reference_other_concept |

**잠정 관찰 (원문 아님)**

- '시너지 조합' — 다른 원장(synergy) 개념 언급. 이 원장엔 참조 키 없음(F5).
- `E0070`: '→'가 순서 권장이 아니라 인과/과정으로 쓰임(P3).
- `E0071`: 다른 원장(synergy)과의 연결은 후속(F5). 이 원장 안에 참조 키 없음.

### /rules/15

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/15/from` | string | M5 |
| from_name | `/rules/15/from_name` | string | PRP/자가혈 |
| to | `/rules/15/to` | string | M12 |
| to_name | `/rules/15/to_name` | string | 마이크로니들링(MTS) |
| level | `/rules/15/level` | string | safe |
| interval | `/rules/15/interval` | string | 같은 날 가능 |
| note | `/rules/15/note` | string | MTS + PRP는 대표적 시너지 조합. 재생 효과 극대화 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0072 | `/rules/15/interval` | [0,7) | 같은 날 가능 | time, same_day, possibility |
| E0073 | `/rules/15/note` | [0,21) | MTS + PRP는 대표적 시너지 조합 | separator_plus, combination, reference_other_concept |
| E0074 | `/rules/15/note` | [23,32) | 재생 효과 극대화 | degree, effect |

**잠정 관찰 (원문 아님)**

- 'MTS + PRP' 이름 순서가 from(M5 PRP)/to(M12 MTS)와 반대. '+'는 함께 시술 쓰임으로 읽힘.
- `E0073`: 이름 순서가 from/to 와 반대(M5=PRP, M12=MTS).

알려진 형태소 오분절 (원시 출력 · 미교정)

- `/rules/15/note` [6,10) 「PRP는」 → PRP/SL + 늘/VV + ᆫ/ETM — PRP/SL+늘/VV+ᆫ/ETM — 보조사 '는'이 동사 '늘다'로 오분석. 없는 동사가 생긴다

### /rules/16

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/16/from` | string | M5 |
| from_name | `/rules/16/from_name` | string | PRP/자가혈 |
| to | `/rules/16/to` | string | M8 |
| to_name | `/rules/16/to_name` | string | 레이저 |
| level | `/rules/16/level` | string | safe |
| interval | `/rules/16/interval` | string | 같은 날 가능 |
| note | `/rules/16/note` | string | 프락셔널 레이저 후 PRP 도포/주입으로 재생 촉진 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0075 | `/rules/16/interval` | [0,7) | 같은 날 가능 | time, same_day, possibility |
| E0076 | `/rules/16/note` | [0,28) | 프락셔널 레이저 후 PRP 도포/주입으로 재생 촉진 | order_sequence, subtype_like, separator_slash, effect |
| E0077 | `/rules/16/note` | [15,20) | 도포/주입 | separator_slash, alternative |

**잠정 관찰 (원문 아님)**

- '프락셔널 레이저'로 한정 — to_name '레이저' 전체에 대한 진술인지 불명(B2).
- `E0076`: '프락셔널' 레이저로 한정된 서술. 다른 레이저 종류는 원문에 없음(B).

### /rules/17

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/17/from` | string | M7 |
| from_name | `/rules/17/from_name` | string | 실리프팅 |
| to | `/rules/17/to` | string | M9 |
| to_name | `/rules/17/to_name` | string | 기기 리프팅 |
| level | `/rules/17/level` | string | caution |
| interval | `/rules/17/interval` | string | 2~3개월 간격 |
| note | `/rules/17/note` | string | 실이 완전히 자리잡은 후 에너지기기. 실 위치 변형 방지 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0078 | `/rules/17/interval` | [0,8) | 2~3개월 간격 | range, quantity_time |
| E0079 | `/rules/17/note` | [0,19) | 실이 완전히 자리잡은 후 에너지기기 | order_sequence, time_relative, degree |
| E0080 | `/rules/17/note` | [21,31) | 실 위치 변형 방지 | prevention |

**잠정 관찰 (원문 아님)**

- '에너지기기' — to_name '기기 리프팅'과 다른 말(P1).
- `E0078`: '권장' 없음.
- `E0079`: '에너지기기'가 to_name '기기 리프팅'을 가리키는지 원문으로 확정 불가(P).

### /rules/18

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/18/from` | string | M7 |
| from_name | `/rules/18/from_name` | string | 실리프팅 |
| to | `/rules/18/to` | string | M8 |
| to_name | `/rules/18/to_name` | string | 레이저 |
| level | `/rules/18/level` | string | caution |
| interval | `/rules/18/interval` | string | 4주 간격 권장 |
| note | `/rules/18/note` | string | 실 삽입부 회복 후 레이저 시술 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0081 | `/rules/18/interval` | [0,8) | 4주 간격 권장 | quantity_time, recommendation |
| E0082 | `/rules/18/note` | [0,17) | 실 삽입부 회복 후 레이저 시술 | order_sequence, body_area_like, time_relative |

**잠정 관찰 (원문 아님)**

- (별도 관찰 없음)

### /rules/19

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/19/from` | string | M7 |
| from_name | `/rules/19/from_name` | string | 실리프팅 |
| to | `/rules/19/to` | string | M11 |
| to_name | `/rules/19/to_name` | string | 니들RF |
| level | `/rules/19/level` | string | warning |
| interval | `/rules/19/interval` | string | 2~3개월 간격 |
| note | `/rules/19/note` | string | 니들이 실을 건드릴 위험. 실 완전 안착 후 시술 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0083 | `/rules/19/interval` | [0,8) | 2~3개월 간격 | range, quantity_time |
| E0084 | `/rules/19/note` | [0,13) | 니들이 실을 건드릴 위험 | risk, mechanism |
| E0085 | `/rules/19/note` | [15,27) | 실 완전 안착 후 시술 | order_sequence, time_relative, degree |

**잠정 관찰 (원문 아님)**

- (별도 관찰 없음)

알려진 형태소 오분절 (원시 출력 · 미교정)

- `/rules/19/note` [0,3) 「니들이」 → 니/NP + 들/XSN + 이/JKS — 니/NP+들/XSN — '니들'(침)이 대명사+복수로 오분석. 주어 대상이 사라진다

### /rules/20

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/20/from` | string | M8 |
| from_name | `/rules/20/from_name` | string | 레이저 |
| to | `/rules/20/to` | string | M9 |
| to_name | `/rules/20/to_name` | string | 기기 리프팅 |
| level | `/rules/20/level` | string | caution |
| interval | `/rules/20/interval` | string | 2~4주 간격 |
| note | `/rules/20/note` | string | 열 부하 축적 방지. 같은 날 레이저 + HIFU는 과자극 위험 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0086 | `/rules/20/interval` | [0,7) | 2~4주 간격 | range, quantity_time |
| E0087 | `/rules/20/note` | [0,10) | 열 부하 축적 방지 | prevention, mechanism |
| E0088 | `/rules/20/note` | [12,35) | 같은 날 레이저 + HIFU는 과자극 위험 | condition, same_day, separator_plus, risk, device_like |

**잠정 관찰 (원문 아님)**

- '레이저 + HIFU' — HIFU 가 to_name '기기 리프팅'의 예로 읽힘(P1).
- `E0088`: '+' = 함께(같은 날). HIFU 가 to_name '기기 리프팅'의 예로 읽힘(P).

알려진 형태소 오분절 (원시 출력 · 미교정)

- `/rules/20/note` [0,4) 「열 부하」 → 열/NR + 부하/NNG — 열/NR(수사 10) — 열(heat)이 숫자로 오태깅. 수량 오탐 가능

### /rules/21

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/21/from` | string | M8 |
| from_name | `/rules/21/from_name` | string | 레이저 |
| to | `/rules/21/to` | string | M11 |
| to_name | `/rules/21/to_name` | string | 니들RF |
| level | `/rules/21/level` | string | caution |
| interval | `/rules/21/interval` | string | 2주 간격 권장 |
| note | `/rules/21/note` | string | 피부 회복 후 시술. 레이저 종류에 따라 다름 (어블레이티브는 4주) |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0089 | `/rules/21/interval` | [0,8) | 2주 간격 권장 | quantity_time, recommendation |
| E0090 | `/rules/21/note` | [0,10) | 피부 회복 후 시술 | order_sequence, time_relative |
| E0091 | `/rules/21/note` | [12,38) | 레이저 종류에 따라 다름 (어블레이티브는 4주) | condition, subtype_like, exception, parenthetical, quantity_time |
| E0092 | `/rules/21/note` | [26,38) | (어블레이티브는 4주) | parenthetical, exception |

**잠정 관찰 (원문 아님)**

- interval 은 2주, note 괄호에 어블레이티브 4주 예외 — interval 칸만 쓰면 예외가 사라진다(P5).
- `E0089`: note 의 어블레이티브 4주 예외가 interval 칸에는 없다(P5).
- `E0090`: 어느 시술이 먼저인지 명시 없음(B).

### /rules/22

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/22/from` | string | M8 |
| from_name | `/rules/22/from_name` | string | 레이저 |
| to | `/rules/22/to` | string | M12 |
| to_name | `/rules/22/to_name` | string | 마이크로니들링(MTS) |
| level | `/rules/22/level` | string | caution |
| interval | `/rules/22/interval` | string | 2주 간격 권장 |
| note | `/rules/22/note` | string | 레이저로 손상된 피부 회복 후 MTS. 순서: 레이저 → (회복) → MTS |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0093 | `/rules/22/interval` | [0,8) | 2주 간격 권장 | quantity_time, recommendation |
| E0094 | `/rules/22/note` | [0,20) | 레이저로 손상된 피부 회복 후 MTS | order_sequence, time_relative |
| E0095 | `/rules/22/note` | [22,42) | 순서: 레이저 → (회복) → MTS | order_sequence, arrow, parenthetical |

**잠정 관찰 (원문 아님)**

- `E0095`: 괄호 안 '회복'은 시술이 아닌 단계.

알려진 형태소 오분절 (원시 출력 · 미교정)

- `/rules/22/note` [17,22) 「MTS. 」 → MTS./SL — 'MTS.'가 한 SL 토큰 — 문장 경계 마침표가 사라진다

### /rules/23

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/23/from` | string | M9 |
| from_name | `/rules/23/from_name` | string | 기기 리프팅 |
| to | `/rules/23/to` | string | M11 |
| to_name | `/rules/23/to_name` | string | 니들RF |
| level | `/rules/23/level` | string | caution |
| interval | `/rules/23/interval` | string | 2~4주 간격 |
| note | `/rules/23/note` | string | RF 에너지 중복. 열 부하 과축적 방지 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0096 | `/rules/23/interval` | [0,7) | 2~4주 간격 | range, quantity_time |
| E0097 | `/rules/23/note` | [0,9) | RF 에너지 중복 | mechanism, device_like |
| E0098 | `/rules/23/note` | [11,22) | 열 부하 과축적 방지 | prevention, degree |

**잠정 관찰 (원문 아님)**

- (별도 관찰 없음)

알려진 형태소 오분절 (원시 출력 · 미교정)

- `/rules/23/note` [11,15) 「열 부하」 → 열/NR + 부하/NNG — 열/NR(수사 10) — 열(heat)이 숫자로 오태깅. 수량 오탐 가능
- `/rules/23/note` [16,19) 「과축적」 → 과/NNG + 축적/NNG — 과/NNG+축적/NNG — 접두 '과-'가 명사로 태깅

### /rules/24

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/24/from` | string | M6 |
| from_name | `/rules/24/from_name` | string | 지방이식 |
| to | `/rules/24/to` | string | M9 |
| to_name | `/rules/24/to_name` | string | 기기 리프팅 |
| level | `/rules/24/level` | string | warning |
| interval | `/rules/24/interval` | string | 3개월 이상 |
| note | `/rules/24/note` | string | 이식된 지방의 생착률 보호. 열에너지가 이식 지방을 파괴할 수 있음 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0099 | `/rules/24/interval` | [0,6) | 3개월 이상 | range, lower_bound, quantity_time |
| E0100 | `/rules/24/note` | [0,14) | 이식된 지방의 생착률 보호 | prevention, effect |
| E0101 | `/rules/24/note` | [16,37) | 열에너지가 이식 지방을 파괴할 수 있음 | possibility, mechanism, risk |

**잠정 관찰 (원문 아님)**

- interval '3개월 이상' — '간격' 어휘 없음. 하한만 있음.
- `E0099`: '간격'·'권장' 없음.

### /rules/25

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/25/from` | string | M6 |
| from_name | `/rules/25/from_name` | string | 지방이식 |
| to | `/rules/25/to` | string | M8 |
| to_name | `/rules/25/to_name` | string | 레이저 |
| level | `/rules/25/level` | string | warning |
| interval | `/rules/25/interval` | string | 2~3개월 간격 |
| note | `/rules/25/note` | string | 지방 생착 완료 전 열자극 금지 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0102 | `/rules/25/interval` | [0,8) | 2~3개월 간격 | range, quantity_time |
| E0103 | `/rules/25/note` | [0,17) | 지방 생착 완료 전 열자극 금지 | prohibition, time_relative |

**잠정 관찰 (원문 아님)**

- note '금지' 와 level=warning, interval '2~3개월 간격' 공존(P6).
- `E0103`: '금지'가 있으나 level=warning, interval 은 기간 제시(P6).

### /rules/26

| 원본 컬럼명 | Pointer | 자료형 | 원문 값 |
|---|---|---|---|
| from | `/rules/26/from` | string | M6 |
| from_name | `/rules/26/from_name` | string | 지방이식 |
| to | `/rules/26/to` | string | M2 |
| to_name | `/rules/26/to_name` | string | 필러 |
| level | `/rules/26/level` | string | caution |
| interval | `/rules/26/interval` | string | 3개월 간격 |
| note | `/rules/26/note` | string | 지방 생착 결과 확인 후 필러로 보충. 동시 주입 시 과교정 위험 |

직접 읽기 표현 (원문 구간)

| ID | Pointer | span_cp | 원문 구간 | 탐색 관점 |
|---|---|---|---|---|
| E0104 | `/rules/26/interval` | [0,6) | 3개월 간격 | quantity_time |
| E0105 | `/rules/26/note` | [0,20) | 지방 생착 결과 확인 후 필러로 보충 | order_sequence, time_relative, condition |
| E0106 | `/rules/26/note` | [22,36) | 동시 주입 시 과교정 위험 | condition, same_day, risk |

**잠정 관찰 (원문 아님)**

- 배열 끝 3개(rule 24~26)가 from=M6 — from 순서가 M9(rule 23) 뒤에 M6 로 돌아간다(구조 사실).
- `E0105`: 지방이식(from) 먼저.

알려진 형태소 오분절 (원시 출력 · 미교정)

- `/rules/26/note` [30,33) 「과교정」 → 과/NNG + 교정/NNG — 과/NNG+교정/NNG — 접두 '과-'(지나침)가 명사로 태깅돼 정도 수식이 독립 명사처럼 보인다
- `/rules/26/note` [3,5) 「생착」 → 생/XPN + 착/NNG — 생/XPN+착/NNG — 같은 원장 다른 출현(/rules/25/note)과 분절이 다르다

## 구조 사실 (원문 그대로 · 의미 승인 아님)

- 등장 ID: M1, M2, M3, M4, M5, M6, M7, M8, M9, M11, M12 (M10 없음)
- ID ↔ 이름: M1=보톡스(6); M2=필러(7); M3=바이오스티뮬레이터/콜라겐부스터(2); M4=스킨부스터(3); M5=PRP/자가혈(2); M6=지방이식(3); M7=실리프팅(5); M8=레이저(10); M9=기기 리프팅(7); M11=니들RF(5); M12=마이크로니들링(MTS)(4)
- level 값별 수: {'caution': 14, 'safe': 8, 'warning': 5}
- 순서 무시한 쌍 중복: 없음 · 자기 쌍: 없음
- from 순서(배열 순): M1 M1 M1 M1 M1 M1 M2 M2 M2 M2 M2 M3 M3 M4 M4 M5 M5 M7 M7 M7 M8 M8 M8 M9 M6 M6 M6
