# S10 — /timelines/9 chemical-peel-mid (케미컬 필링 (중간 깊이))

> build.py 생성. 원문 값과 잠정 관찰은 서로 다른 절·칸에 둔다.

- 소유 범위: prefix ['/timelines/9'] · exact []
- 공유 문맥(소유 아님): ['', '/timelines', '/consensus_method', '/reaction_levels', '/reaction_levels/normal', '/reaction_levels/abnormal', '/reaction_levels/caution', '/reaction_levels/emergency']
- 직접 읽기: done (manual/S10.txt) · 마지막 읽은 Pointer `/timelines/9/phases/3/emergency/2`

## 1. 원문 — 모든 노드 (문서 순서)

| # | Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 원문 구간(cp) |
|---|---|---|---|---|---|
| 1 | `/timelines/9` | `[9]` | object | {id, category, name, phases} | 10670–11821 |
| 2 | `/timelines/9/id` | `id` | string | chemical-peel-mid | 10676–10695 |
| 3 | `/timelines/9/category` | `category` | string | M15 | 10707–10712 |
| 4 | `/timelines/9/name` | `name` | string | 케미컬 필링 (중간 깊이) | 10720–10736 |
| 5 | `/timelines/9/phases` | `phases` | array | [길이 4] | 10746–11820 |
| 6 | `/timelines/9/phases/0` | `[0]` | object | {period, label, normal, abnormal, caution, emergency} | 10747–11003 |
| 7 | `/timelines/9/phases/0/period` | `period` | string | Day 0 | 10757–10764 |
| 8 | `/timelines/9/phases/0/label` | `label` | string | 시술 당일 | 10773–10780 |
| 9 | `/timelines/9/phases/0/normal` | `normal` | array | [길이 4] | 10790–10870 |
| 10 | `/timelines/9/phases/0/normal/0` | `[0]` | string | 시술 중 작열감/따끔 (TCA 도포 시) | 10791–10815 |
| 11 | `/timelines/9/phases/0/normal/1` | `[1]` | string | 즉각적 홍반/발적 | 10816–10827 |
| 12 | `/timelines/9/phases/0/normal/2` | `[2]` | string | 피부 하얗게 변함 (frost, TCA 반응) | 10828–10855 |
| 13 | `/timelines/9/phases/0/normal/3` | `[3]` | string | 시술 후 열감/조임감 | 10856–10869 |
| 14 | `/timelines/9/phases/0/abnormal` | `abnormal` | array | [길이 2] | 10882–10916 |
| 15 | `/timelines/9/phases/0/abnormal/0` | `[0]` | string | 예상보다 깊은 frost (과도한 침투) | 10883–10907 |
| 16 | `/timelines/9/phases/0/abnormal/1` | `[1]` | string | 심한 부종 | 10908–10915 |
| 17 | `/timelines/9/phases/0/caution` | `caution` | array | [길이 2] | 10927–10967 |
| 18 | `/timelines/9/phases/0/caution/0` | `[0]` | string | 수포 형성 (깊은 침투 시사) | 10928–10946 |
| 19 | `/timelines/9/phases/0/caution/1` | `[1]` | string | 비정상적 통증 (진통제 미반응) | 10947–10966 |
| 20 | `/timelines/9/phases/0/emergency` | `emergency` | array | [길이 2] | 10980–11002 |
| 21 | `/timelines/9/phases/0/emergency/0` | `[0]` | string | 광범위 화학 화상 | 10981–10992 |
| 22 | `/timelines/9/phases/0/emergency/1` | `[1]` | string | 아나필락시스 | 10993–11001 |
| 23 | `/timelines/9/phases/1` | `[1]` | object | {period, label, normal, abnormal, caution, emergency} | 11004–11257 |
| 24 | `/timelines/9/phases/1/period` | `period` | string | Day 1-3 | 11014–11023 |
| 25 | `/timelines/9/phases/1/label` | `label` | string | 염증/가피기 | 11032–11040 |
| 26 | `/timelines/9/phases/1/normal` | `normal` | array | [길이 4] | 11050–11111 |
| 27 | `/timelines/9/phases/1/normal/0` | `[0]` | string | 강한 홍반/부종 지속 | 11051–11064 |
| 28 | `/timelines/9/phases/1/normal/1` | `[1]` | string | 피부 갈색 변화 시작 (가피 형성) | 11065–11086 |
| 29 | `/timelines/9/phases/1/normal/2` | `[2]` | string | 조임감/건조감 | 11087–11096 |
| 30 | `/timelines/9/phases/1/normal/3` | `[3]` | string | 세안/보습 주의 기간 | 11097–11110 |
| 31 | `/timelines/9/phases/1/abnormal` | `abnormal` | array | [길이 2] | 11123–11155 |
| 32 | `/timelines/9/phases/1/abnormal/0` | `[0]` | string | 예상보다 심한 부종 (특히 눈 주위) | 11124–11146 |
| 33 | `/timelines/9/phases/1/abnormal/1` | `[1]` | string | 통증 증가 | 11147–11154 |
| 34 | `/timelines/9/phases/1/caution` | `caution` | array | [길이 3] | 11166–11200 |
| 35 | `/timelines/9/phases/1/caution/0` | `[0]` | string | 농성 분비물 | 11167–11175 |
| 36 | `/timelines/9/phases/1/caution/1` | `[1]` | string | 발열 (37.5도 이상) | 11176–11191 |
| 37 | `/timelines/9/phases/1/caution/2` | `[2]` | string | 수포 확대 | 11192–11199 |
| 38 | `/timelines/9/phases/1/emergency` | `emergency` | array | [길이 2] | 11213–11256 |
| 39 | `/timelines/9/phases/1/emergency/0` | `[0]` | string | 감염 (고열 + 농 + 발적 확대) | 11214–11235 |
| 40 | `/timelines/9/phases/1/emergency/1` | `[1]` | string | 헤르페스 재활성화 (수포 군집) | 11236–11255 |
| 41 | `/timelines/9/phases/2` | `[2]` | object | {period, label, normal, abnormal, caution, emergency} | 11258–11507 |
| 42 | `/timelines/9/phases/2/period` | `period` | string | Day 3-7 | 11268–11277 |
| 43 | `/timelines/9/phases/2/label` | `label` | string | 필링기 | 11286–11291 |
| 44 | `/timelines/9/phases/2/normal` | `normal` | array | [길이 4] | 11301–11382 |
| 45 | `/timelines/9/phases/2/normal/0` | `[0]` | string | Day 3-4: 각질/가피 벗겨짐 시작 | 11302–11325 |
| 46 | `/timelines/9/phases/2/normal/1` | `[1]` | string | 가려움 (정상 치유 반응) | 11326–11342 |
| 47 | `/timelines/9/phases/2/normal/2` | `[2]` | string | 분홍빛 새 피부 노출 | 11343–11356 |
| 48 | `/timelines/9/phases/2/normal/3` | `[3]` | string | 자연스러운 각질 탈락 (강제 제거 금지) | 11357–11381 |
| 49 | `/timelines/9/phases/2/abnormal` | `abnormal` | array | [길이 2] | 11394–11415 |
| 50 | `/timelines/9/phases/2/abnormal/0` | `[0]` | string | 필링 불균일 | 11395–11403 |
| 51 | `/timelines/9/phases/2/abnormal/1` | `[1]` | string | 가피 조기 탈락 | 11404–11414 |
| 52 | `/timelines/9/phases/2/caution` | `caution` | array | [길이 2] | 11426–11466 |
| 53 | `/timelines/9/phases/2/caution/0` | `[0]` | string | 감염 (필링 중 감염 취약) | 11427–11444 |
| 54 | `/timelines/9/phases/2/caution/1` | `[1]` | string | 화상 깊이 과도 (재상피화 지연) | 11445–11465 |
| 55 | `/timelines/9/phases/2/emergency` | `emergency` | array | [길이 2] | 11479–11506 |
| 56 | `/timelines/9/phases/2/emergency/0` | `[0]` | string | 감염 확산 (봉와직염) | 11480–11494 |
| 57 | `/timelines/9/phases/2/emergency/1` | `[1]` | string | 반흔 형성 시작 | 11495–11505 |
| 58 | `/timelines/9/phases/3` | `[3]` | object | {period, label, normal, abnormal, caution, emergency} | 11508–11819 |
| 59 | `/timelines/9/phases/3/period` | `period` | string | Day 7-14 | 11518–11528 |
| 60 | `/timelines/9/phases/3/label` | `label` | string | 재상피화/회복기 | 11537–11547 |
| 61 | `/timelines/9/phases/3/normal` | `normal` | array | [길이 4] | 11557–11643 |
| 62 | `/timelines/9/phases/3/normal/0` | `[0]` | string | Day 7-10: 새 피부 형성 완료 | 11558–11580 |
| 63 | `/timelines/9/phases/3/normal/1` | `[1]` | string | 분홍빛 홍반 지속 (정상, 수주-수개월 소요) | 11581–11608 |
| 64 | `/timelines/9/phases/3/normal/2` | `[2]` | string | 메이크업 가능 (재상피화 후) | 11609–11627 |
| 65 | `/timelines/9/phases/3/normal/3` | `[3]` | string | 자외선 차단 필수 기간 | 11628–11642 |
| 66 | `/timelines/9/phases/3/abnormal` | `abnormal` | array | [길이 2] | 11655–11690 |
| 67 | `/timelines/9/phases/3/abnormal/0` | `[0]` | string | 지속적 깊은 홍반 | 11656–11667 |
| 68 | `/timelines/9/phases/3/abnormal/1` | `[1]` | string | PIH (염증 후 과색소침착) 시작 | 11668–11689 |
| 69 | `/timelines/9/phases/3/caution` | `caution` | array | [길이 3] | 11701–11759 |
| 70 | `/timelines/9/phases/3/caution/0` | `[0]` | string | PIH 진행 (특히 피부 타입 III-V) | 11702–11727 |
| 71 | `/timelines/9/phases/3/caution/1` | `[1]` | string | 재상피화 지연 (10일 이상) | 11728–11746 |
| 72 | `/timelines/9/phases/3/caution/2` | `[2]` | string | 비후성 반흔 초기 | 11747–11758 |
| 73 | `/timelines/9/phases/3/emergency` | `emergency` | array | [길이 3] | 11772–11818 |
| 74 | `/timelines/9/phases/3/emergency/0` | `[0]` | string | 켈로이드/비후성 반흔 | 11773–11786 |
| 75 | `/timelines/9/phases/3/emergency/1` | `[1]` | string | 지연성 감염 | 11787–11795 |
| 76 | `/timelines/9/phases/3/emergency/2` | `[2]` | string | 화상 확장 (화학물질 잔류에 의한) | 11796–11817 |

## 2. 원문 — 기간별 보기 (같은 값, 원본 컬럼명 그대로)

`id` = chemical-peel-mid · `category` = M15 · `name` = 케미컬 필링 (중간 깊이)

### phases/0 — `period` = Day 0 · `label` = 시술 당일

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 시술 중 작열감/따끔 (TCA 도포 시) | `/timelines/9/phases/0/normal/0` |
| `normal` | 1 | 즉각적 홍반/발적 | `/timelines/9/phases/0/normal/1` |
| `normal` | 2 | 피부 하얗게 변함 (frost, TCA 반응) | `/timelines/9/phases/0/normal/2` |
| `normal` | 3 | 시술 후 열감/조임감 | `/timelines/9/phases/0/normal/3` |
| `abnormal` | 0 | 예상보다 깊은 frost (과도한 침투) | `/timelines/9/phases/0/abnormal/0` |
| `abnormal` | 1 | 심한 부종 | `/timelines/9/phases/0/abnormal/1` |
| `caution` | 0 | 수포 형성 (깊은 침투 시사) | `/timelines/9/phases/0/caution/0` |
| `caution` | 1 | 비정상적 통증 (진통제 미반응) | `/timelines/9/phases/0/caution/1` |
| `emergency` | 0 | 광범위 화학 화상 | `/timelines/9/phases/0/emergency/0` |
| `emergency` | 1 | 아나필락시스 | `/timelines/9/phases/0/emergency/1` |

### phases/1 — `period` = Day 1-3 · `label` = 염증/가피기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 강한 홍반/부종 지속 | `/timelines/9/phases/1/normal/0` |
| `normal` | 1 | 피부 갈색 변화 시작 (가피 형성) | `/timelines/9/phases/1/normal/1` |
| `normal` | 2 | 조임감/건조감 | `/timelines/9/phases/1/normal/2` |
| `normal` | 3 | 세안/보습 주의 기간 | `/timelines/9/phases/1/normal/3` |
| `abnormal` | 0 | 예상보다 심한 부종 (특히 눈 주위) | `/timelines/9/phases/1/abnormal/0` |
| `abnormal` | 1 | 통증 증가 | `/timelines/9/phases/1/abnormal/1` |
| `caution` | 0 | 농성 분비물 | `/timelines/9/phases/1/caution/0` |
| `caution` | 1 | 발열 (37.5도 이상) | `/timelines/9/phases/1/caution/1` |
| `caution` | 2 | 수포 확대 | `/timelines/9/phases/1/caution/2` |
| `emergency` | 0 | 감염 (고열 + 농 + 발적 확대) | `/timelines/9/phases/1/emergency/0` |
| `emergency` | 1 | 헤르페스 재활성화 (수포 군집) | `/timelines/9/phases/1/emergency/1` |

### phases/2 — `period` = Day 3-7 · `label` = 필링기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | Day 3-4: 각질/가피 벗겨짐 시작 | `/timelines/9/phases/2/normal/0` |
| `normal` | 1 | 가려움 (정상 치유 반응) | `/timelines/9/phases/2/normal/1` |
| `normal` | 2 | 분홍빛 새 피부 노출 | `/timelines/9/phases/2/normal/2` |
| `normal` | 3 | 자연스러운 각질 탈락 (강제 제거 금지) | `/timelines/9/phases/2/normal/3` |
| `abnormal` | 0 | 필링 불균일 | `/timelines/9/phases/2/abnormal/0` |
| `abnormal` | 1 | 가피 조기 탈락 | `/timelines/9/phases/2/abnormal/1` |
| `caution` | 0 | 감염 (필링 중 감염 취약) | `/timelines/9/phases/2/caution/0` |
| `caution` | 1 | 화상 깊이 과도 (재상피화 지연) | `/timelines/9/phases/2/caution/1` |
| `emergency` | 0 | 감염 확산 (봉와직염) | `/timelines/9/phases/2/emergency/0` |
| `emergency` | 1 | 반흔 형성 시작 | `/timelines/9/phases/2/emergency/1` |

### phases/3 — `period` = Day 7-14 · `label` = 재상피화/회복기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | Day 7-10: 새 피부 형성 완료 | `/timelines/9/phases/3/normal/0` |
| `normal` | 1 | 분홍빛 홍반 지속 (정상, 수주-수개월 소요) | `/timelines/9/phases/3/normal/1` |
| `normal` | 2 | 메이크업 가능 (재상피화 후) | `/timelines/9/phases/3/normal/2` |
| `normal` | 3 | 자외선 차단 필수 기간 | `/timelines/9/phases/3/normal/3` |
| `abnormal` | 0 | 지속적 깊은 홍반 | `/timelines/9/phases/3/abnormal/0` |
| `abnormal` | 1 | PIH (염증 후 과색소침착) 시작 | `/timelines/9/phases/3/abnormal/1` |
| `caution` | 0 | PIH 진행 (특히 피부 타입 III-V) | `/timelines/9/phases/3/caution/0` |
| `caution` | 1 | 재상피화 지연 (10일 이상) | `/timelines/9/phases/3/caution/1` |
| `caution` | 2 | 비후성 반흔 초기 | `/timelines/9/phases/3/caution/2` |
| `emergency` | 0 | 켈로이드/비후성 반흔 | `/timelines/9/phases/3/emergency/0` |
| `emergency` | 1 | 지연성 감염 | `/timelines/9/phases/3/emergency/1` |
| `emergency` | 2 | 화상 확장 (화학물질 잔류에 의한) | `/timelines/9/phases/3/emergency/2` |

## 3. 수동 표현 (직접 읽기) — 원문 구절과 관찰 칸 분리

| Pointer | 구간 | 원문 구절 | 탐색 관점(잠정) | 잠정 메모 |
|---|---|---|---|---|
| `/timelines/9/id` | [0,17) | chemical-peel-mid | id_code | |  |
| `/timelines/9/category` | [0,3) | M15 | id_code | |  |
| `/timelines/9/name` | [0,14) | 케미컬 필링 (중간 깊이) | procedure_name, depth, loanword | 「중간 깊이」 = 시술 강도/침투 깊이 구분(잠정). 수치 없음 |
| `/timelines/9/phases/0/period` | [0,5) | Day 0 | period | |  |
| `/timelines/9/phases/0/label` | [0,5) | 시술 당일 | reference_point | |  |
| `/timelines/9/phases/0/normal/0` | [0,11) | 시술 중 작열감/따끔 | reference_point, alt | 「시술 중」 |
| `/timelines/9/phases/0/normal/0` | [12,22) | (TCA 도포 시) | condition, ingredient_ref, mixed_script | 「시」 조건. 성분 약어 TCA |
| `/timelines/9/phases/0/normal/1` | [0,9) | 즉각적 홍반/발적 | onset_speed, alt | |  |
| `/timelines/9/phases/0/normal/2` | [0,25) | 피부 하얗게 변함 (frost, TCA 반응) | color_change, mixed_script, cause | |  |
| `/timelines/9/phases/0/normal/3` | [0,11) | 시술 후 열감/조임감 | reference_point, sequence, alt | 「시술 후」 |
| `/timelines/9/phases/0/abnormal/0` | [0,22) | 예상보다 깊은 frost (과도한 침투) | comparison, depth, degree, cause | 「깊은」 깊이 = frost 의 깊이(침투). 「과도한」 |
| `/timelines/9/phases/0/abnormal/1` | [0,5) | 심한 부종 | severity | |  |
| `/timelines/9/phases/0/caution/0` | [0,16) | 수포 형성 (깊은 침투 시사) | formation, depth, inference | 「시사」 추정 |
| `/timelines/9/phases/0/caution/1` | [0,17) | 비정상적 통증 (진통제 미반응) | degree, negation | |  |
| `/timelines/9/phases/0/emergency/0` | [0,9) | 광범위 화학 화상 | extent | |  |
| `/timelines/9/phases/0/emergency/1` | [0,6) | 아나필락시스 | label | |  |
| `/timelines/9/phases/1/period` | [0,7) | Day 1-3 | period, time_range | |  |
| `/timelines/9/phases/1/label` | [0,6) | 염증/가피기 | phase_label, alt | |  |
| `/timelines/9/phases/1/normal/0` | [0,11) | 강한 홍반/부종 지속 | degree, alt, persistence | |  |
| `/timelines/9/phases/1/normal/1` | [0,19) | 피부 갈색 변화 시작 (가피 형성) | color_change, onset, gloss | |  |
| `/timelines/9/phases/1/normal/2` | [0,7) | 조임감/건조감 | alt | |  |
| `/timelines/9/phases/1/normal/3` | [0,11) | 세안/보습 주의 기간 | management, caution_period, alt | 관리 시점 표현. 구체 방법 원문 없음 |
| `/timelines/9/phases/1/abnormal/0` | [0,20) | 예상보다 심한 부종 (특히 눈 주위) | comparison, severity, site, emphasis | |  |
| `/timelines/9/phases/1/abnormal/1` | [0,5) | 통증 증가 | worsening | |  |
| `/timelines/9/phases/1/caution/0` | [0,6) | 농성 분비물 | event | |  |
| `/timelines/9/phases/1/caution/1` | [0,13) | 발열 (37.5도 이상) | numeric_threshold, unit | |  |
| `/timelines/9/phases/1/caution/2` | [0,5) | 수포 확대 | extent | |  |
| `/timelines/9/phases/1/emergency/0` | [0,19) | 감염 (고열 + 농 + 발적 확대) | co_occurrence, extent | |  |
| `/timelines/9/phases/1/emergency/1` | [0,17) | 헤르페스 재활성화 (수포 군집) | recurrence, pattern | |  |
| `/timelines/9/phases/2/period` | [0,7) | Day 3-7 | period, time_range | |  |
| `/timelines/9/phases/2/label` | [0,3) | 필링기 | phase_label | |  |
| `/timelines/9/phases/2/normal/0` | [0,21) | Day 3-4: 각질/가피 벗겨짐 시작 | time_anchor, time_range, alt, onset | |  |
| `/timelines/9/phases/2/normal/1` | [0,14) | 가려움 (정상 치유 반응) | judgment | |  |
| `/timelines/9/phases/2/normal/2` | [0,11) | 분홍빛 새 피부 노출 | color | |  |
| `/timelines/9/phases/2/normal/3` | [0,11) | 자연스러운 각질 탈락 | quality | |  |
| `/timelines/9/phases/2/normal/3` | [12,22) | (강제 제거 금지) | avoidance, management | 「금지」 회피 지시 |
| `/timelines/9/phases/2/abnormal/0` | [0,6) | 필링 불균일 | quality_negative | |  |
| `/timelines/9/phases/2/abnormal/1` | [0,8) | 가피 조기 탈락 | timing | |  |
| `/timelines/9/phases/2/caution/0` | [0,15) | 감염 (필링 중 감염 취약) | vulnerability, reference_point | 「필링 중」 기간 조건 |
| `/timelines/9/phases/2/caution/1` | [0,18) | 화상 깊이 과도 (재상피화 지연) | depth, degree, consequence | |  |
| `/timelines/9/phases/2/emergency/0` | [0,12) | 감염 확산 (봉와직염) | extent, label | |  |
| `/timelines/9/phases/2/emergency/1` | [0,8) | 반흔 형성 시작 | onset, formation | |  |
| `/timelines/9/phases/3/period` | [0,8) | Day 7-14 | period, time_range | |  |
| `/timelines/9/phases/3/label` | [0,8) | 재상피화/회복기 | phase_label, alt | |  |
| `/timelines/9/phases/3/normal/0` | [0,20) | Day 7-10: 새 피부 형성 완료 | time_anchor, time_range, completion | |  |
| `/timelines/9/phases/3/normal/1` | [0,25) | 분홍빛 홍반 지속 (정상, 수주-수개월 소요) | color, persistence, judgment, approx_time, duration, time_range | 「수주-수개월」 근사 범위 |
| `/timelines/9/phases/3/normal/2` | [0,16) | 메이크업 가능 (재상피화 후) | activity, possibility, condition, sequence | |  |
| `/timelines/9/phases/3/normal/3` | [0,12) | 자외선 차단 필수 기간 | management, obligation | 「필수」 강한 권고. 기간 길이 원문 없음 |
| `/timelines/9/phases/3/abnormal/0` | [0,9) | 지속적 깊은 홍반 | persistence, color_degree | 「깊은」 은 여기서 색 정도(잠정) — 주입·침투 깊이와 다름 |
| `/timelines/9/phases/3/abnormal/1` | [0,19) | PIH (염증 후 과색소침착) 시작 | abbreviation, gloss, onset | |  |
| `/timelines/9/phases/3/caution/0` | [0,23) | PIH 진행 (특히 피부 타입 III-V) | abbreviation, progress, emphasis, population, range | 피부 타입 III-V 로마 숫자 범위. 분류 체계 이름 원문 없음 |
| `/timelines/9/phases/3/caution/1` | [0,16) | 재상피화 지연 (10일 이상) | delay, duration_threshold | |  |
| `/timelines/9/phases/3/caution/2` | [0,9) | 비후성 반흔 초기 | early_sign | |  |
| `/timelines/9/phases/3/emergency/0` | [0,11) | 켈로이드/비후성 반흔 | alt | |  |
| `/timelines/9/phases/3/emergency/1` | [0,6) | 지연성 감염 | delayed_onset | |  |
| `/timelines/9/phases/3/emergency/2` | [0,19) | 화상 확장 (화학물질 잔류에 의한) | extent, cause | |  |

## 4. 자동 후보 요약 (정규식 일치분만 — 전수 의미 수집 아님)

P-ADVICE 3, P-AFTER 3, P-ALT 10, P-APPROXTIME 1, P-COMPARE 4, P-COND-SI 1, P-COURSE 22, P-DAY 6, P-DEGREE 7, P-DEPTH 5, P-DURING 3, P-LATIN 13, P-NEG 2, P-NUMUNIT 2, P-PAREN 22, P-POSSIB 2, P-SCALE 1, P-SITE 1, P-SPEED 2, P-SYMBOL 2, P-TEMPORAL 2

전체 목록은 expressions.json (segment 필터).

## 5. 잠정 관찰

- **S10-O1** 「깊」 이 세 가지 대상에 쓰였다: 시술명 「중간 깊이」, frost/침투 「깊은」, 홍반 「깊은」(색 정도로 보임), 「화상 깊이」. 대상이 다르므로 하나로 묶지 않는다(잠정).
- **S10-O2** 관리 표현: 세안/보습 주의 기간, 강제 제거 금지, 메이크업 가능(재상피화 후), 자외선 차단 필수 기간. 기간 길이는 소속 period 로만 짐작되며 원문에 따로 없다.
- **S10-O3** 「피부 타입 III-V」 는 대상 집단 조건이다. 분류 체계(예: 어느 척도인지)는 원문에 없다.

## 6. 미결 (이 구획)

| ID | 분류 | 위치 | 내용 |
|---|---|---|---|
| S10-Q1 | B | `/timelines/9/phases/3/caution/0` | 「피부 타입 III-V」 의 분류 체계 이름이 원문에 없다. |
| S10-Q2 | B | `/timelines/9/phases/1/normal/3` `/timelines/9/phases/3/normal/3` | 「주의 기간」「필수 기간」 의 시작·끝이 소속 period 외에 원문에 없다. |

## 7. 형태소 — 알려진 오분절 (교정 안 함)

| Pointer | 구간 | 원시 토큰 | 판정/설명 | 영향 |
|---|---|---|---|---|
| `/timelines/9/phases/0/caution/0` | [13,15) | 시/NNB + 사/NNG | K-SISA 「시사」(추정) 가 시/NNB+사/NNG 로 분할 | 조건 「시」 오탐 위험, 추정 표현 손실 |
| `/timelines/9/phases/1/normal/1` | [13,15) | 가/NNG + 피/NNG | K-GAPI 「가피」 가 가+피 로 분할 | 사건 명사 손실 |
| `/timelines/9/phases/1/emergency/0` | [13,15) | 발/NNG + 적/XSN | K-BALJEOK 「발적」 이 발/NNG+적/XSN 으로 분할 | 사건 명사 손실(「-적」 접미 오인) |
| `/timelines/9/phases/1/emergency/1` | [11,13) | 수/NNB + 포/NNG | K-SUPO 「수포」 가 수+포 로 분할 | 「수」(가능·수량) 오탐 위험, 사건명 손실 |
| `/timelines/9/phases/2/caution/1` | [3,5) | 깊이/MAG | K-MAG-NOUN 명사 「깊이」 가 MAG(부사 「깊이」) | 깊이(대상 속성) 를 부사로 오태깅 |
| `/timelines/9/phases/3/abnormal/1` | [10,13) | 과/NNG + 색소/NNG | K-GWA-NNG 접두 「과」 가 NNG 로 분석 | 과도 단서 품사 불일치 |

