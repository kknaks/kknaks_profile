# S08 — /timelines/7 skin-booster (스킨부스터)

> build.py 생성. 원문 값과 잠정 관찰은 서로 다른 절·칸에 둔다.

- 소유 범위: prefix ['/timelines/7'] · exact []
- 공유 문맥(소유 아님): ['', '/timelines', '/consensus_method', '/reaction_levels', '/reaction_levels/normal', '/reaction_levels/abnormal', '/reaction_levels/caution', '/reaction_levels/emergency']
- 직접 읽기: done (manual/S08.txt) · 마지막 읽은 Pointer `/timelines/7/phases/2/emergency/1`

## 1. 원문 — 모든 노드 (문서 순서)

| # | Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 원문 구간(cp) |
|---|---|---|---|---|---|
| 1 | `/timelines/7` | `[7]` | object | {id, category, name, phases} | 8844–9596 |
| 2 | `/timelines/7/id` | `id` | string | skin-booster | 8850–8864 |
| 3 | `/timelines/7/category` | `category` | string | M4 | 8876–8880 |
| 4 | `/timelines/7/name` | `name` | string | 스킨부스터 | 8888–8895 |
| 5 | `/timelines/7/phases` | `phases` | array | [길이 3] | 8905–9595 |
| 6 | `/timelines/7/phases/0` | `[0]` | object | {period, label, normal, abnormal, caution, emergency} | 8906–9145 |
| 7 | `/timelines/7/phases/0/period` | `period` | string | Day 0 | 8916–8923 |
| 8 | `/timelines/7/phases/0/label` | `label` | string | 시술 당일 | 8932–8939 |
| 9 | `/timelines/7/phases/0/normal` | `normal` | array | [길이 4] | 8949–9006 |
| 10 | `/timelines/7/phases/0/normal/0` | `[0]` | string | 주사 부위 돌기/울퉁불퉁 (papule, 정상) | 8950–8978 |
| 11 | `/timelines/7/phases/0/normal/1` | `[1]` | string | 발적/홍반 | 8979–8986 |
| 12 | `/timelines/7/phases/0/normal/2` | `[2]` | string | 경미한 부종 | 8987–8995 |
| 13 | `/timelines/7/phases/0/normal/3` | `[3]` | string | 따끔함/화끈감 | 8996–9005 |
| 14 | `/timelines/7/phases/0/abnormal` | `abnormal` | array | [길이 2] | 9018–9045 |
| 15 | `/timelines/7/phases/0/abnormal/0` | `[0]` | string | 멍 (혈관 천자 시) | 9019–9032 |
| 16 | `/timelines/7/phases/0/abnormal/1` | `[1]` | string | 예상보다 큰 돌기 | 9033–9044 |
| 17 | `/timelines/7/phases/0/caution` | `caution` | array | [길이 2] | 9056–9086 |
| 18 | `/timelines/7/phases/0/caution/0` | `[0]` | string | 심한 부종 (안면 전체) | 9057–9072 |
| 19 | `/timelines/7/phases/0/caution/1` | `[1]` | string | 비정상적 통증 지속 | 9073–9085 |
| 20 | `/timelines/7/phases/0/emergency` | `emergency` | array | [길이 2] | 9099–9144 |
| 21 | `/timelines/7/phases/0/emergency/0` | `[0]` | string | 아나필락시스 (HA 알레르기) | 9100–9118 |
| 22 | `/timelines/7/phases/0/emergency/1` | `[1]` | string | 혈관폐색 (blanching -- 드묾) | 9119–9143 |
| 23 | `/timelines/7/phases/1` | `[1]` | object | {period, label, normal, abnormal, caution, emergency} | 9146–9385 |
| 24 | `/timelines/7/phases/1/period` | `period` | string | Day 1-3 | 9156–9165 |
| 25 | `/timelines/7/phases/1/label` | `label` | string | 돌기 소실기 | 9174–9182 |
| 26 | `/timelines/7/phases/1/normal` | `normal` | array | [길이 4] | 9192–9245 |
| 27 | `/timelines/7/phases/1/normal/0` | `[0]` | string | 돌기 24-48시간 내 소실 | 9193–9210 |
| 28 | `/timelines/7/phases/1/normal/1` | `[1]` | string | 멍 있으면 변색 진행 | 9211–9224 |
| 29 | `/timelines/7/phases/1/normal/2` | `[2]` | string | 부종 감소 | 9225–9232 |
| 30 | `/timelines/7/phases/1/normal/3` | `[3]` | string | 촉촉함 느낌 시작 | 9233–9244 |
| 31 | `/timelines/7/phases/1/abnormal` | `abnormal` | array | [길이 2] | 9257–9284 |
| 32 | `/timelines/7/phases/1/abnormal/0` | `[0]` | string | 돌기 48시간 이상 지속 | 9258–9273 |
| 33 | `/timelines/7/phases/1/abnormal/1` | `[1]` | string | 경미한 가려움 | 9274–9283 |
| 34 | `/timelines/7/phases/1/caution` | `caution` | array | [길이 2] | 9295–9344 |
| 35 | `/timelines/7/phases/1/caution/0` | `[0]` | string | 돌기 72시간 이상 지속 (결절 가능성) | 9296–9320 |
| 36 | `/timelines/7/phases/1/caution/1` | `[1]` | string | 감염 징후 (발적 + 열감 + 통증) | 9321–9343 |
| 37 | `/timelines/7/phases/1/emergency` | `emergency` | array | [길이 2] | 9357–9384 |
| 38 | `/timelines/7/phases/1/emergency/0` | `[0]` | string | 감염 (농/발열) | 9358–9369 |
| 39 | `/timelines/7/phases/1/emergency/1` | `[1]` | string | 광범위 알레르기 반응 | 9370–9383 |
| 40 | `/timelines/7/phases/2` | `[2]` | object | {period, label, normal, abnormal, caution, emergency} | 9386–9594 |
| 41 | `/timelines/7/phases/2/period` | `period` | string | Day 3-7 | 9396–9405 |
| 42 | `/timelines/7/phases/2/label` | `label` | string | 효과 발현기 | 9414–9422 |
| 43 | `/timelines/7/phases/2/normal` | `normal` | array | [길이 4] | 9432–9480 |
| 44 | `/timelines/7/phases/2/normal/0` | `[0]` | string | 피부 수분감 개선 | 9433–9444 |
| 45 | `/timelines/7/phases/2/normal/1` | `[1]` | string | 피부 톤 개선 | 9445–9454 |
| 46 | `/timelines/7/phases/2/normal/2` | `[2]` | string | 모든 시술 흔적 소실 | 9455–9468 |
| 47 | `/timelines/7/phases/2/normal/3` | `[3]` | string | 자연스러운 윤기 | 9469–9479 |
| 48 | `/timelines/7/phases/2/abnormal` | `abnormal` | array | [길이 2] | 9492–9523 |
| 49 | `/timelines/7/phases/2/abnormal/0` | `[0]` | string | 잔여 결절 촉지 | 9493–9503 |
| 50 | `/timelines/7/phases/2/abnormal/1` | `[1]` | string | PIH (주사 자국 색소침착) | 9504–9522 |
| 51 | `/timelines/7/phases/2/caution` | `caution` | array | [길이 2] | 9534–9558 |
| 52 | `/timelines/7/phases/2/caution/0` | `[0]` | string | 결절 지속/커짐 | 9535–9545 |
| 53 | `/timelines/7/phases/2/caution/1` | `[1]` | string | 지연성 과민 반응 | 9546–9557 |
| 54 | `/timelines/7/phases/2/emergency` | `emergency` | array | [길이 2] | 9571–9593 |
| 55 | `/timelines/7/phases/2/emergency/0` | `[0]` | string | 지연성 감염 | 9572–9580 |
| 56 | `/timelines/7/phases/2/emergency/1` | `[1]` | string | 이물 반응/육아종 | 9581–9592 |

## 2. 원문 — 기간별 보기 (같은 값, 원본 컬럼명 그대로)

`id` = skin-booster · `category` = M4 · `name` = 스킨부스터

### phases/0 — `period` = Day 0 · `label` = 시술 당일

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 주사 부위 돌기/울퉁불퉁 (papule, 정상) | `/timelines/7/phases/0/normal/0` |
| `normal` | 1 | 발적/홍반 | `/timelines/7/phases/0/normal/1` |
| `normal` | 2 | 경미한 부종 | `/timelines/7/phases/0/normal/2` |
| `normal` | 3 | 따끔함/화끈감 | `/timelines/7/phases/0/normal/3` |
| `abnormal` | 0 | 멍 (혈관 천자 시) | `/timelines/7/phases/0/abnormal/0` |
| `abnormal` | 1 | 예상보다 큰 돌기 | `/timelines/7/phases/0/abnormal/1` |
| `caution` | 0 | 심한 부종 (안면 전체) | `/timelines/7/phases/0/caution/0` |
| `caution` | 1 | 비정상적 통증 지속 | `/timelines/7/phases/0/caution/1` |
| `emergency` | 0 | 아나필락시스 (HA 알레르기) | `/timelines/7/phases/0/emergency/0` |
| `emergency` | 1 | 혈관폐색 (blanching -- 드묾) | `/timelines/7/phases/0/emergency/1` |

### phases/1 — `period` = Day 1-3 · `label` = 돌기 소실기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 돌기 24-48시간 내 소실 | `/timelines/7/phases/1/normal/0` |
| `normal` | 1 | 멍 있으면 변색 진행 | `/timelines/7/phases/1/normal/1` |
| `normal` | 2 | 부종 감소 | `/timelines/7/phases/1/normal/2` |
| `normal` | 3 | 촉촉함 느낌 시작 | `/timelines/7/phases/1/normal/3` |
| `abnormal` | 0 | 돌기 48시간 이상 지속 | `/timelines/7/phases/1/abnormal/0` |
| `abnormal` | 1 | 경미한 가려움 | `/timelines/7/phases/1/abnormal/1` |
| `caution` | 0 | 돌기 72시간 이상 지속 (결절 가능성) | `/timelines/7/phases/1/caution/0` |
| `caution` | 1 | 감염 징후 (발적 + 열감 + 통증) | `/timelines/7/phases/1/caution/1` |
| `emergency` | 0 | 감염 (농/발열) | `/timelines/7/phases/1/emergency/0` |
| `emergency` | 1 | 광범위 알레르기 반응 | `/timelines/7/phases/1/emergency/1` |

### phases/2 — `period` = Day 3-7 · `label` = 효과 발현기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 피부 수분감 개선 | `/timelines/7/phases/2/normal/0` |
| `normal` | 1 | 피부 톤 개선 | `/timelines/7/phases/2/normal/1` |
| `normal` | 2 | 모든 시술 흔적 소실 | `/timelines/7/phases/2/normal/2` |
| `normal` | 3 | 자연스러운 윤기 | `/timelines/7/phases/2/normal/3` |
| `abnormal` | 0 | 잔여 결절 촉지 | `/timelines/7/phases/2/abnormal/0` |
| `abnormal` | 1 | PIH (주사 자국 색소침착) | `/timelines/7/phases/2/abnormal/1` |
| `caution` | 0 | 결절 지속/커짐 | `/timelines/7/phases/2/caution/0` |
| `caution` | 1 | 지연성 과민 반응 | `/timelines/7/phases/2/caution/1` |
| `emergency` | 0 | 지연성 감염 | `/timelines/7/phases/2/emergency/0` |
| `emergency` | 1 | 이물 반응/육아종 | `/timelines/7/phases/2/emergency/1` |

## 3. 수동 표현 (직접 읽기) — 원문 구절과 관찰 칸 분리

| Pointer | 구간 | 원문 구절 | 탐색 관점(잠정) | 잠정 메모 |
|---|---|---|---|---|
| `/timelines/7/id` | [0,12) | skin-booster | id_code | |  |
| `/timelines/7/category` | [0,2) | M4 | id_code | |  |
| `/timelines/7/name` | [0,5) | 스킨부스터 | procedure_name, loanword | |  |
| `/timelines/7/phases/0/period` | [0,5) | Day 0 | period | |  |
| `/timelines/7/phases/0/label` | [0,5) | 시술 당일 | reference_point | |  |
| `/timelines/7/phases/0/normal/0` | [0,26) | 주사 부위 돌기/울퉁불퉁 (papule, 정상) | site, alt, mixed_script, judgment | |  |
| `/timelines/7/phases/0/normal/1` | [0,5) | 발적/홍반 | alt, synonym_pair | |  |
| `/timelines/7/phases/0/normal/2` | [0,6) | 경미한 부종 | severity | |  |
| `/timelines/7/phases/0/normal/3` | [0,7) | 따끔함/화끈감 | alt | |  |
| `/timelines/7/phases/0/abnormal/0` | [0,11) | 멍 (혈관 천자 시) | condition, cause | |  |
| `/timelines/7/phases/0/abnormal/1` | [0,9) | 예상보다 큰 돌기 | comparison, size | |  |
| `/timelines/7/phases/0/caution/0` | [0,13) | 심한 부종 (안면 전체) | severity, extent, site | |  |
| `/timelines/7/phases/0/caution/1` | [0,10) | 비정상적 통증 지속 | degree, persistence | |  |
| `/timelines/7/phases/0/emergency/0` | [0,16) | 아나필락시스 (HA 알레르기) | label, cause_ref, mixed_script | 성분 HA 언급 — 제품 성분 단정 아님 |
| `/timelines/7/phases/0/emergency/1` | [0,22) | 혈관폐색 (blanching -- 드묾) | mixed_script, frequency | 「--」 뒤 빈도 |
| `/timelines/7/phases/1/period` | [0,7) | Day 1-3 | period, time_range | |  |
| `/timelines/7/phases/1/label` | [0,6) | 돌기 소실기 | phase_label, resolution | |  |
| `/timelines/7/phases/1/normal/0` | [0,15) | 돌기 24-48시간 내 소실 | resolution, time_range | |  |
| `/timelines/7/phases/1/normal/1` | [0,11) | 멍 있으면 변색 진행 | condition, color_change, progress | 「있으면」 조건(패턴 「시」 밖) |
| `/timelines/7/phases/1/normal/2` | [0,5) | 부종 감소 | change | |  |
| `/timelines/7/phases/1/normal/3` | [0,9) | 촉촉함 느낌 시작 | subjective, onset | |  |
| `/timelines/7/phases/1/abnormal/0` | [0,13) | 돌기 48시간 이상 지속 | duration_threshold, persistence | |  |
| `/timelines/7/phases/1/abnormal/1` | [0,7) | 경미한 가려움 | severity | |  |
| `/timelines/7/phases/1/caution/0` | [0,22) | 돌기 72시간 이상 지속 (결절 가능성) | duration_threshold, persistence, possibility | normal 24-48 / abnormal 48+ / caution 72+ 로 같은 사건의 시간 단계가 등급을 가른다(잠정) |
| `/timelines/7/phases/1/caution/1` | [0,20) | 감염 징후 (발적 + 열감 + 통증) | early_sign, co_occurrence | |  |
| `/timelines/7/phases/1/emergency/0` | [0,9) | 감염 (농/발열) | gloss, alt | |  |
| `/timelines/7/phases/1/emergency/1` | [0,11) | 광범위 알레르기 반응 | extent | |  |
| `/timelines/7/phases/2/period` | [0,7) | Day 3-7 | period, time_range | |  |
| `/timelines/7/phases/2/label` | [0,6) | 효과 발현기 | phase_label, onset | |  |
| `/timelines/7/phases/2/normal/0` | [0,9) | 피부 수분감 개선 | change | |  |
| `/timelines/7/phases/2/normal/1` | [0,7) | 피부 톤 개선 | change | |  |
| `/timelines/7/phases/2/normal/2` | [0,11) | 모든 시술 흔적 소실 | quantifier_all, resolution | 「모든」 |
| `/timelines/7/phases/2/normal/3` | [0,8) | 자연스러운 윤기 | quality | |  |
| `/timelines/7/phases/2/abnormal/0` | [0,8) | 잔여 결절 촉지 | persistence, detection | |  |
| `/timelines/7/phases/2/abnormal/1` | [0,16) | PIH (주사 자국 색소침착) | abbreviation, gloss, site | |  |
| `/timelines/7/phases/2/caution/0` | [0,8) | 결절 지속/커짐 | persistence, alt, worsening | |  |
| `/timelines/7/phases/2/caution/1` | [0,9) | 지연성 과민 반응 | delayed_onset | |  |
| `/timelines/7/phases/2/emergency/0` | [0,6) | 지연성 감염 | delayed_onset | |  |
| `/timelines/7/phases/2/emergency/1` | [0,9) | 이물 반응/육아종 | alt | |  |

## 4. 자동 후보 요약 (정규식 일치분만 — 전수 의미 수집 아님)

P-AFTER 1, P-ALT 6, P-APPROX 1, P-APPROXTIME 1, P-COMPARE 3, P-COND-SI 1, P-COURSE 15, P-DAY 3, P-DEGREE 6, P-DURING 1, P-FREQ 1, P-IF 2, P-LATIN 7, P-NUMUNIT 3, P-PAREN 9, P-POSSIB 1, P-SITE 2, P-SYMBOL 3

전체 목록은 expressions.json (segment 필터).

## 5. 잠정 관찰

- **S08-O1** 「돌기」 가 Day 1-3 의 normal(24-48시간 내 소실)·abnormal(48시간 이상)·caution(72시간 이상) 에 시간 단계로 나뉘어 나온다. 같은 사건의 지속 시간이 등급을 가르는 원장 내 가장 명시적인 사례다(잠정).
- **S08-O2** 기간 3개(Day 0 / 1-3 / 3-7). Day 7 이후 기간·재시술 값이 없다.

## 6. 미결 (이 구획)

| ID | 분류 | 위치 | 내용 |
|---|---|---|---|
| S08-Q1 | B | `/timelines/7/phases` | Day 7 이후 경과·재시술 시점이 원문에 없다. |

## 7. 형태소 — 알려진 오분절 (교정 안 함)

| Pointer | 구간 | 원시 토큰 | 판정/설명 | 영향 |
|---|---|---|---|---|
| `/timelines/7/phases/0/normal/0` | [6,8) | 돌/VV + 기/ETN | K-DOLGI 명사 「돌기」 가 돌/VV+기/ETN(동사 명사형) | 사건 명사 손실 |
| `/timelines/7/phases/1/normal/1` | [0,1) | 멍/MAG | K-MAG-NOUN 명사 「멍」 이 MAG(부사) | 사건 명사를 부사로 오태깅 — 명사 기준 탐색에서 누락 |
| `/timelines/7/phases/1/abnormal/0` | [0,2) | 돌/VV + 기/ETN | K-DOLGI 명사 「돌기」 가 돌/VV+기/ETN(동사 명사형) | 사건 명사 손실 |
| `/timelines/7/phases/1/caution/0` | [0,2) | 돌/VV + 기/ETN | K-DOLGI 명사 「돌기」 가 돌/VV+기/ETN(동사 명사형) | 사건 명사 손실 |

