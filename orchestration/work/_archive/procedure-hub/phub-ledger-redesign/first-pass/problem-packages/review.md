# problem-packages.json — 1차 조사 읽기용 결과

**1차 범위 종료: 예 · 원장 전체 완료: 아님** (열린 미결은 [issues.md](issues.md), 검증은 [validation.md](validation.md)).

원본 `orchestration/work/phub-recommend/bronze/phub-ledger/problem-packages.json` · 73526 바이트 · 48965 코드 포인트 · sha256 `e44fa7216e0eceefde4be368fcdfa623df0834de6989b826f66ba4e408fcb3dc` · 한 줄(줄바꿈 0) · BOM 없음 · 중복 키 0 · 문자열 이스케이프 0.

노드 3656 · 말단 2366(전부 string) · 빈 값 48(빈 배열: products 47 · combos 1).

기계 기록: [source-map.json](source-map.json) · [morphology.json](morphology.json) · [expressions.json](expressions.json) · [coverage.json](coverage.json) · [cue-review.json](cue-review.json). 직접 읽기 기록: `manual/Sxx.json`. 진행: [progress.md](progress.md).

## 상태

| 항목 | 상태 |
|---|---|
| 전수 읽기 | 15/15 구획 직접 읽기 done |
| 구조·값 수집 | 노드 3656 · 말단 2366 · 필드명 20종 |
| 형태소 | 텍스트 값 2096 · 필드명 20 · 제외 270 · 토큰 6708 |
| 표현 | 수동 871 · 정규식 후보 1031 · 절 구간 27 |
| 단서 대조 | 단서 375 · 수동 표현으로 덮임 360 · 판단 기록 15 · 미처리 0 |

## 컬럼 구성

원본 키 이름 그대로. `*` = 배열 순번. 모든 객체는 같은 위치에서 같은 키 집합·같은 순서를 가진다(선택적 필드 없음).

| 경로 패턴 | 원본 컬럼명 | 자료형·중첩 | 출현 수 | 원문 예시(위치) | 빈 값 |
|---|---|---|---|---|---|
| `(루트)` | `(루트)` | object 길이 4~4 | 1 | `` (object[4]) | — |
| `/version` | `version` | string | 1 | `/version` = 6.2 | — |
| `/updated` | `updated` | string | 1 | `/updated` = 2026-07-26 | — |
| `/description` | `description` | string | 1 | `/description` = taxonomy P1~P14 하위구조 기반 CC 자동 생성 | — |
| `/problems` | `problems` | array 길이 14~14 | 1 | `/problems` (array[14]) | — |
| `/problems/*` | `(problems 원소)` | object 길이 3~3 | 14 | `/problems/0` (object[3])<br>`/problems/1` (object[3]) | — |
| `/problems/*/problem_id` | `problem_id` | string | 14 | `/problems/0/problem_id` = P1<br>`/problems/1/problem_id` = P2 | — |
| `/problems/*/problem` | `problem` | string | 14 | `/problems/0/problem` = 쁘띠시술<br>`/problems/1/problem` = 주름 | — |
| `/problems/*/complaints` | `complaints` | array 길이 4~17 | 14 | `/problems/0/complaints` (array[17])<br>`/problems/1/complaints` (array[7]) | — |
| `/problems/*/complaints/*` | `(complaints 원소)` | object 길이 6~6 | 115 | `/problems/0/complaints/0` (object[6])<br>`/problems/0/complaints/1` (object[6]) | — |
| `/problems/*/complaints/*/cc` | `cc` | string | 115 | `/problems/0/complaints/0/cc` = 코필러<br>`/problems/0/complaints/1/cc` = 코실리프팅 | — |
| `/problems/*/complaints/*/cc_detail` | `cc_detail` | string | 115 | `/problems/0/complaints/0/cc_detail` = 콧대/코끝<br>`/problems/0/complaints/1/cc_detail` = 코끝 거상 | — |
| `/problems/*/complaints/*/cc_group` | `cc_group` | string | 115 | `/problems/0/complaints/0/cc_group` = 코<br>`/problems/0/complaints/1/cc_group` = 코 | — |
| `/problems/*/complaints/*/procedures` | `procedures` | array 길이 1~6 | 115 | `/problems/0/complaints/0/procedures` (array[2])<br>`/problems/0/complaints/1/procedures` (array[2]) | — |
| `/problems/*/complaints/*/procedures/*` | `(procedures 원소)` | object 길이 4~4 | 254 | `/problems/0/complaints/0/procedures/0` (object[4])<br>`/problems/0/complaints/0/procedures/1` (object[4]) | — |
| `/problems/*/complaints/*/procedures/*/name` | `name` | string | 254 | `/problems/0/complaints/0/procedures/0/name` = 필러<br>`/problems/0/complaints/0/procedures/1/name` = 보톡스 | — |
| `/problems/*/complaints/*/procedures/*/category` | `category` | string | 254 | `/problems/0/complaints/0/procedures/0/category` = M2<br>`/problems/0/complaints/0/procedures/1/category` = M1 | — |
| `/problems/*/complaints/*/procedures/*/role` | `role` | string | 254 | `/problems/0/complaints/0/procedures/0/role` = 볼륨 충전<br>`/problems/0/complaints/0/procedures/1/role` = 근이완 보조 | — |
| `/problems/*/complaints/*/procedures/*/products` | `products` | array 길이 0~3 | 254 | `/problems/0/complaints/0/procedures/0/products` (array[2])<br>`/problems/0/complaints/0/procedures/1/products` (array[2]) | 47개 (예: `/problems/0/complaints/3/procedures/0/products`) |
| `/problems/*/complaints/*/procedures/*/products/*` | `(products 원소)` | string | 388 | `/problems/0/complaints/0/procedures/0/products/0` = 쥬비덤<br>`/problems/0/complaints/0/procedures/0/products/1` = 이브아르 | — |
| `/problems/*/complaints/*/combos` | `combos` | array 길이 0~3 | 115 | `/problems/0/complaints/0/combos` (array[1])<br>`/problems/0/complaints/1/combos` (array[1]) | 1개 (예: `/problems/13/complaints/3/combos`) |
| `/problems/*/complaints/*/combos/*` | `(combos 원소)` | object 길이 4~4 | 146 | `/problems/0/complaints/0/combos/0` (object[4])<br>`/problems/0/complaints/1/combos/0` (object[4]) | — |
| `/problems/*/complaints/*/combos/*/name` | `name` | string | 146 | `/problems/0/complaints/0/combos/0/name` = 필러 + 보톡스<br>`/problems/0/complaints/1/combos/0/name` = 실리프팅 + 필러 | — |
| `/problems/*/complaints/*/combos/*/combo` | `combo` | array 길이 1~3 | 146 | `/problems/0/complaints/0/combos/0/combo` (array[2])<br>`/problems/0/complaints/1/combos/0/combo` (array[2]) | — |
| `/problems/*/complaints/*/combos/*/combo/*` | `(combo 원소)` | string | 277 | `/problems/0/complaints/0/combos/0/combo/0` = 필러<br>`/problems/0/complaints/0/combos/0/combo/1` = 보톡스 | — |
| `/problems/*/complaints/*/combos/*/reason` | `reason` | string | 146 | `/problems/0/complaints/0/combos/0/reason` = 볼륨 + 근이완 = 시너지<br>`/problems/0/complaints/1/combos/0/reason` = 거상 + 볼륨 = 입체적 리프팅 | — |
| `/problems/*/complaints/*/combos/*/evidence` | `evidence` | string | 146 | `/problems/0/complaints/0/combos/0/evidence` = 보톡스가 근육 움직임 줄여 필러 유지력 향상<br>`/problems/0/complaints/1/combos/0/evidence` = 실이 당기고 필러가 채움 | — |
| `/problems/*/complaints/*/alternatives` | `alternatives` | array 길이 1~2 | 115 | `/problems/0/complaints/0/alternatives` (array[1])<br>`/problems/0/complaints/1/alternatives` (array[1]) | — |
| `/problems/*/complaints/*/alternatives/*` | `(alternatives 원소)` | string | 125 | `/problems/0/complaints/0/alternatives/0` = 바이오스티뮬레이터로 장기 관리<br>`/problems/0/complaints/1/alternatives/0` = 실 시술 후 2개월간 HIFU/RF 피할 것 | — |

변형 행:

| 변형 | 위치 | 원문 |
|---|---|---|
| combos 빈 배열(유일) | `/problems/13/complaints/3/combos` | `[]` |
| products 빈 배열 47곳 | source-map.json `empty_values` | `[]` (예: `/problems/0/complaints/3/procedures/0/products`) |
| combo 원소 1개(단독 묶음) 21곳 | 예: `/problems/0/complaints/13/combos/0/combo` | ["반영구화장"] |
| combo 원소 3개 6곳 | 예: `/problems/8/complaints/0/combos/1/combo` | ["서브시전", "프락셔널", "PRP"] |
| alternatives 2개 10곳 | 예: `/problems/3/complaints/3/alternatives` | ["바이오스티뮬레이터로 장기 관리", "단계별 접근 추천"] |

## 구획 목차

| 구획 | 범위 | 노드 | 말단 | 직접 읽기 | 관찰 | 수동 표현 | 파일 |
|---|---|---|---|---|---|---|---|
| S00 | 루트·메타데이터·problems 컨테이너 | 5 | 3 | done | 7 | 4 | [review-part-S00.md](review-part-S00.md) |
| S01 | /problems/0 P1 쁘띠시술 | 456 | 292 | done | 14 | 126 | [review-part-S01.md](review-part-S01.md) |
| S02 | /problems/1 P2 주름 | 330 | 226 | done | 9 | 74 | [review-part-S02.md](review-part-S02.md) |
| S03 | /problems/2 P3 쳐짐 | 236 | 160 | done | 7 | 46 | [review-part-S03.md](review-part-S03.md) |
| S04 | /problems/3 P4 항노화 | 222 | 144 | done | 12 | 48 | [review-part-S04.md](review-part-S04.md) |
| S05 | /problems/4 P5 색소/미백 | 262 | 172 | done | 12 | 83 | [review-part-S05.md](review-part-S05.md) |
| S06 | /problems/5 P6 여드름 | 253 | 165 | done | 11 | 53 | [review-part-S06.md](review-part-S06.md) |
| S07 | /problems/6 P7 모공 | 223 | 147 | done | 7 | 41 | [review-part-S07.md](review-part-S07.md) |
| S08 | /problems/7 P8 홍조/혈관 | 144 | 92 | done | 6 | 35 | [review-part-S08.md](review-part-S08.md) |
| S09 | /problems/8 P9 흉터 | 493 | 325 | done | 15 | 105 | [review-part-S09.md](review-part-S09.md) |
| S10 | /problems/9 P10 제모 | 98 | 60 | done | 7 | 34 | [review-part-S10.md](review-part-S10.md) |
| S11 | /problems/10 P11 얼굴윤곽 | 231 | 151 | done | 9 | 51 | [review-part-S11.md](review-part-S11.md) |
| S12 | /problems/11 P12 바디 | 271 | 165 | done | 8 | 68 | [review-part-S12.md](review-part-S12.md) |
| S13 | /problems/12 P13 두피/탈모 | 293 | 181 | done | 11 | 63 | [review-part-S13.md](review-part-S13.md) |
| S14 | /problems/13 P14 기타 | 139 | 83 | done | 9 | 40 | [review-part-S14.md](review-part-S14.md) |

## 전 원장 관찰 요약(잠정 — 원문 칸과 분리)

- 같은 combo 블록·alternatives 문장이 부위·세부가 다른 complaint 에 글자 그대로 반복된다(B-02). description 이 스스로 '자동 생성' 이라고 한다(F-01).
- cc·cc_detail·cc_group·alternatives·evidence 는 칸마다 정보 종류가 섞여 있다(F-03·F-04·F-05·F-06).
- procedures.name ↔ combos.combo ↔ combo name ↔ cc_detail 표기가 일치하지 않는 곳이 여럿이다(I-01·I-02·I-03·I-06·I-10).
- 같은 combo 의 근거 진술이 complaint 마다 서로 맞지 않는 곳이 있다(I-05·I-09), 한 값 안의 정도 불일치(I-08).
- 기호 '+','/','·','=' 는 필드마다 쓰임이 다르다(F-02). 이름 안의 '+'(리쥬란 HB+·NAD+·ASCE+)는 기호 규칙과 겹친다(K-03).
