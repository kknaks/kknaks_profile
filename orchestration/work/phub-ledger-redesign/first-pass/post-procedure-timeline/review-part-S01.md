# S01 — /timelines/0 botox (보톡스)

> build.py 생성. 원문 값과 잠정 관찰은 서로 다른 절·칸에 둔다.

- 소유 범위: prefix ['/timelines/0'] · exact []
- 공유 문맥(소유 아님): ['', '/timelines', '/consensus_method', '/reaction_levels', '/reaction_levels/normal', '/reaction_levels/abnormal', '/reaction_levels/caution', '/reaction_levels/emergency']
- 직접 읽기: done (manual/S01.txt) · 마지막 읽은 Pointer `/timelines/0/phases/4/emergency/0`

## 1. 원문 — 모든 노드 (문서 순서)

| # | Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 원문 구간(cp) |
|---|---|---|---|---|---|
| 1 | `/timelines/0` | `[0]` | object | {id, category, name, phases} | 293–1590 |
| 2 | `/timelines/0/id` | `id` | string | botox | 299–306 |
| 3 | `/timelines/0/category` | `category` | string | M1 | 318–322 |
| 4 | `/timelines/0/name` | `name` | string | 보톡스 | 330–335 |
| 5 | `/timelines/0/phases` | `phases` | array | [길이 5] | 345–1589 |
| 6 | `/timelines/0/phases/0` | `[0]` | object | {period, label, normal, abnormal, caution, emergency} | 346–575 |
| 7 | `/timelines/0/phases/0/period` | `period` | string | Day 0 | 356–363 |
| 8 | `/timelines/0/phases/0/label` | `label` | string | 시술 당일 | 372–379 |
| 9 | `/timelines/0/phases/0/normal` | `normal` | array | [길이 3] | 389–450 |
| 10 | `/timelines/0/phases/0/normal/0` | `[0]` | string | 주사 부위 작은 돌기/발적 (15-60분 내 소실) | 390–420 |
| 11 | `/timelines/0/phases/0/normal/1` | `[1]` | string | 약간의 따끔함/화끈감 | 421–434 |
| 12 | `/timelines/0/phases/0/normal/2` | `[2]` | string | 주사 부위 경미한 압통 | 435–449 |
| 13 | `/timelines/0/phases/0/abnormal` | `abnormal` | array | [길이 1] | 462–481 |
| 14 | `/timelines/0/phases/0/abnormal/0` | `[0]` | string | 경미한 멍 (혈관 천자 시) | 463–480 |
| 15 | `/timelines/0/phases/0/caution` | `caution` | array | [길이 1] | 492–513 |
| 16 | `/timelines/0/phases/0/caution/0` | `[0]` | string | 1시간 이상 지속되는 발적/부종 | 493–512 |
| 17 | `/timelines/0/phases/0/emergency` | `emergency` | array | [길이 2] | 526–574 |
| 18 | `/timelines/0/phases/0/emergency/0` | `[0]` | string | 심한 두드러기/호흡곤란 (아나필락시스, 극히 드묾) | 527–557 |
| 19 | `/timelines/0/phases/0/emergency/1` | `[1]` | string | 심한 전신 발진/혈관부종 | 558–573 |
| 20 | `/timelines/0/phases/1` | `[1]` | object | {period, label, normal, abnormal, caution, emergency} | 576–861 |
| 21 | `/timelines/0/phases/1/period` | `period` | string | Day 1-3 | 586–595 |
| 22 | `/timelines/0/phases/1/label` | `label` | string | 초기 경과 | 604–611 |
| 23 | `/timelines/0/phases/1/normal` | `normal` | array | [길이 3] | 621–695 |
| 24 | `/timelines/0/phases/1/normal/0` | `[0]` | string | 미세한 근육 무거움/당김감 시작 (Day 2-3) | 622–651 |
| 25 | `/timelines/0/phases/1/normal/1` | `[1]` | string | 효과 아직 안 보임 (정상) | 652–669 |
| 26 | `/timelines/0/phases/1/normal/2` | `[2]` | string | 주사 부위 약간의 붓기 (1-2일 소실) | 670–694 |
| 27 | `/timelines/0/phases/1/abnormal` | `abnormal` | array | [길이 2] | 707–753 |
| 28 | `/timelines/0/phases/1/abnormal/0` | `[0]` | string | 멍 (수일 내 소실, 보라색→황색 변화) | 708–732 |
| 29 | `/timelines/0/phases/1/abnormal/1` | `[1]` | string | 경미한 두통 (수시간 내 소실) | 733–752 |
| 30 | `/timelines/0/phases/1/caution` | `caution` | array | [길이 2] | 764–808 |
| 31 | `/timelines/0/phases/1/caution/0` | `[0]` | string | 지속되는 심한 두통 (24시간 이상) | 765–787 |
| 32 | `/timelines/0/phases/1/caution/1` | `[1]` | string | 비대칭 느낌 (근육 반응 차이) | 788–807 |
| 33 | `/timelines/0/phases/1/emergency` | `emergency` | array | [길이 3] | 821–860 |
| 34 | `/timelines/0/phases/1/emergency/0` | `[0]` | string | 시야 변화/복시 | 822–832 |
| 35 | `/timelines/0/phases/1/emergency/1` | `[1]` | string | 심한 안검하수 | 833–842 |
| 36 | `/timelines/0/phases/1/emergency/2` | `[2]` | string | 연하곤란 (삼키기 어려움) | 843–859 |
| 37 | `/timelines/0/phases/2` | `[2]` | object | {period, label, normal, abnormal, caution, emergency} | 862–1100 |
| 38 | `/timelines/0/phases/2/period` | `period` | string | Day 3-7 | 872–881 |
| 39 | `/timelines/0/phases/2/label` | `label` | string | 효과 발현기 | 890–898 |
| 40 | `/timelines/0/phases/2/normal` | `normal` | array | [길이 3] | 908–958 |
| 41 | `/timelines/0/phases/2/normal/0` | `[0]` | string | 주사 부위 근육 움직임 감소 시작 | 909–929 |
| 42 | `/timelines/0/phases/2/normal/1` | `[1]` | string | 표정 변화 시작 (미세) | 930–945 |
| 43 | `/timelines/0/phases/2/normal/2` | `[2]` | string | 이마/눈가 당김감 | 946–957 |
| 44 | `/timelines/0/phases/2/abnormal` | `abnormal` | array | [길이 2] | 970–1007 |
| 45 | `/timelines/0/phases/2/abnormal/0` | `[0]` | string | 경미한 비대칭 (좌우 효과 속도 차이) | 971–994 |
| 46 | `/timelines/0/phases/2/abnormal/1` | `[1]` | string | 가벼운 눈 무거움 | 995–1006 |
| 47 | `/timelines/0/phases/2/caution` | `caution` | array | [길이 2] | 1018–1058 |
| 48 | `/timelines/0/phases/2/caution/0` | `[0]` | string | 뚜렷한 비대칭 (한쪽만 효과) | 1019–1037 |
| 49 | `/timelines/0/phases/2/caution/1` | `[1]` | string | 눈꺼풀 처짐 (경미한 안검하수) | 1038–1057 |
| 50 | `/timelines/0/phases/2/emergency` | `emergency` | array | [길이 2] | 1071–1099 |
| 51 | `/timelines/0/phases/2/emergency/0` | `[0]` | string | 시야 장애/복시 악화 | 1072–1085 |
| 52 | `/timelines/0/phases/2/emergency/1` | `[1]` | string | 연하곤란/호흡 불편 | 1086–1098 |
| 53 | `/timelines/0/phases/3` | `[3]` | object | {period, label, normal, abnormal, caution, emergency} | 1101–1356 |
| 54 | `/timelines/0/phases/3/period` | `period` | string | Day 7-14 | 1111–1121 |
| 55 | `/timelines/0/phases/3/label` | `label` | string | 효과 안정기 | 1130–1138 |
| 56 | `/timelines/0/phases/3/normal` | `normal` | array | [길이 3] | 1148–1216 |
| 57 | `/timelines/0/phases/3/normal/0` | `[0]` | string | 효과 본격적으로 나타남 (Day 7-10) | 1149–1174 |
| 58 | `/timelines/0/phases/3/normal/1` | `[1]` | string | Day 14 최대 효과 도달 | 1175–1192 |
| 59 | `/timelines/0/phases/3/normal/2` | `[2]` | string | 자연스러운 표정 유지되면서 주름 감소 | 1193–1215 |
| 60 | `/timelines/0/phases/3/abnormal` | `abnormal` | array | [길이 2] | 1228–1261 |
| 61 | `/timelines/0/phases/3/abnormal/0` | `[0]` | string | 효과 미흡 (용량 부족 가능성) | 1229–1248 |
| 62 | `/timelines/0/phases/3/abnormal/1` | `[1]` | string | 경미한 좌우 차이 | 1249–1260 |
| 63 | `/timelines/0/phases/3/caution` | `caution` | array | [길이 2] | 1272–1300 |
| 64 | `/timelines/0/phases/3/caution/0` | `[0]` | string | 눈꺼풀 처짐 지속 | 1273–1284 |
| 65 | `/timelines/0/phases/3/caution/1` | `[1]` | string | 표정 부자연스러움 심화 | 1285–1299 |
| 66 | `/timelines/0/phases/3/emergency` | `emergency` | array | [길이 2] | 1313–1355 |
| 67 | `/timelines/0/phases/3/emergency/0` | `[0]` | string | 시야 장애 지속 | 1314–1324 |
| 68 | `/timelines/0/phases/3/emergency/1` | `[1]` | string | 연하곤란/호흡곤란 (독소 원격 확산, 극히 드묾) | 1325–1354 |
| 69 | `/timelines/0/phases/4` | `[4]` | object | {period, label, normal, abnormal, caution, emergency} | 1357–1588 |
| 70 | `/timelines/0/phases/4/period` | `period` | string | Day 14-30 | 1367–1378 |
| 71 | `/timelines/0/phases/4/label` | `label` | string | 최종 평가기 | 1387–1395 |
| 72 | `/timelines/0/phases/4/normal` | `normal` | array | [길이 3] | 1405–1455 |
| 73 | `/timelines/0/phases/4/normal/0` | `[0]` | string | 최대 효과 유지 상태 | 1406–1419 |
| 74 | `/timelines/0/phases/4/normal/1` | `[1]` | string | 자연스러운 결과 완성 | 1420–1433 |
| 75 | `/timelines/0/phases/4/normal/2` | `[2]` | string | 재시술 필요 여부 판단 가능 시점 | 1434–1454 |
| 76 | `/timelines/0/phases/4/abnormal` | `abnormal` | array | [길이 2] | 1467–1507 |
| 77 | `/timelines/0/phases/4/abnormal/0` | `[0]` | string | Day 14에도 효과 부족 (터치업 고려) | 1468–1493 |
| 78 | `/timelines/0/phases/4/abnormal/1` | `[1]` | string | 경미한 비대칭 잔존 | 1494–1506 |
| 79 | `/timelines/0/phases/4/caution` | `caution` | array | [길이 2] | 1518–1544 |
| 80 | `/timelines/0/phases/4/caution/0` | `[0]` | string | 예상 부위 외 근육 약화 | 1519–1534 |
| 81 | `/timelines/0/phases/4/caution/1` | `[1]` | string | 지속적 두통 | 1535–1543 |
| 82 | `/timelines/0/phases/4/emergency` | `emergency` | array | [길이 1] | 1557–1587 |
| 83 | `/timelines/0/phases/4/emergency/0` | `[0]` | string | 전신 근육 약화 (독소 전신 확산, 극히 드묾) | 1558–1586 |

## 2. 원문 — 기간별 보기 (같은 값, 원본 컬럼명 그대로)

`id` = botox · `category` = M1 · `name` = 보톡스

### phases/0 — `period` = Day 0 · `label` = 시술 당일

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 주사 부위 작은 돌기/발적 (15-60분 내 소실) | `/timelines/0/phases/0/normal/0` |
| `normal` | 1 | 약간의 따끔함/화끈감 | `/timelines/0/phases/0/normal/1` |
| `normal` | 2 | 주사 부위 경미한 압통 | `/timelines/0/phases/0/normal/2` |
| `abnormal` | 0 | 경미한 멍 (혈관 천자 시) | `/timelines/0/phases/0/abnormal/0` |
| `caution` | 0 | 1시간 이상 지속되는 발적/부종 | `/timelines/0/phases/0/caution/0` |
| `emergency` | 0 | 심한 두드러기/호흡곤란 (아나필락시스, 극히 드묾) | `/timelines/0/phases/0/emergency/0` |
| `emergency` | 1 | 심한 전신 발진/혈관부종 | `/timelines/0/phases/0/emergency/1` |

### phases/1 — `period` = Day 1-3 · `label` = 초기 경과

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 미세한 근육 무거움/당김감 시작 (Day 2-3) | `/timelines/0/phases/1/normal/0` |
| `normal` | 1 | 효과 아직 안 보임 (정상) | `/timelines/0/phases/1/normal/1` |
| `normal` | 2 | 주사 부위 약간의 붓기 (1-2일 소실) | `/timelines/0/phases/1/normal/2` |
| `abnormal` | 0 | 멍 (수일 내 소실, 보라색→황색 변화) | `/timelines/0/phases/1/abnormal/0` |
| `abnormal` | 1 | 경미한 두통 (수시간 내 소실) | `/timelines/0/phases/1/abnormal/1` |
| `caution` | 0 | 지속되는 심한 두통 (24시간 이상) | `/timelines/0/phases/1/caution/0` |
| `caution` | 1 | 비대칭 느낌 (근육 반응 차이) | `/timelines/0/phases/1/caution/1` |
| `emergency` | 0 | 시야 변화/복시 | `/timelines/0/phases/1/emergency/0` |
| `emergency` | 1 | 심한 안검하수 | `/timelines/0/phases/1/emergency/1` |
| `emergency` | 2 | 연하곤란 (삼키기 어려움) | `/timelines/0/phases/1/emergency/2` |

### phases/2 — `period` = Day 3-7 · `label` = 효과 발현기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 주사 부위 근육 움직임 감소 시작 | `/timelines/0/phases/2/normal/0` |
| `normal` | 1 | 표정 변화 시작 (미세) | `/timelines/0/phases/2/normal/1` |
| `normal` | 2 | 이마/눈가 당김감 | `/timelines/0/phases/2/normal/2` |
| `abnormal` | 0 | 경미한 비대칭 (좌우 효과 속도 차이) | `/timelines/0/phases/2/abnormal/0` |
| `abnormal` | 1 | 가벼운 눈 무거움 | `/timelines/0/phases/2/abnormal/1` |
| `caution` | 0 | 뚜렷한 비대칭 (한쪽만 효과) | `/timelines/0/phases/2/caution/0` |
| `caution` | 1 | 눈꺼풀 처짐 (경미한 안검하수) | `/timelines/0/phases/2/caution/1` |
| `emergency` | 0 | 시야 장애/복시 악화 | `/timelines/0/phases/2/emergency/0` |
| `emergency` | 1 | 연하곤란/호흡 불편 | `/timelines/0/phases/2/emergency/1` |

### phases/3 — `period` = Day 7-14 · `label` = 효과 안정기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 효과 본격적으로 나타남 (Day 7-10) | `/timelines/0/phases/3/normal/0` |
| `normal` | 1 | Day 14 최대 효과 도달 | `/timelines/0/phases/3/normal/1` |
| `normal` | 2 | 자연스러운 표정 유지되면서 주름 감소 | `/timelines/0/phases/3/normal/2` |
| `abnormal` | 0 | 효과 미흡 (용량 부족 가능성) | `/timelines/0/phases/3/abnormal/0` |
| `abnormal` | 1 | 경미한 좌우 차이 | `/timelines/0/phases/3/abnormal/1` |
| `caution` | 0 | 눈꺼풀 처짐 지속 | `/timelines/0/phases/3/caution/0` |
| `caution` | 1 | 표정 부자연스러움 심화 | `/timelines/0/phases/3/caution/1` |
| `emergency` | 0 | 시야 장애 지속 | `/timelines/0/phases/3/emergency/0` |
| `emergency` | 1 | 연하곤란/호흡곤란 (독소 원격 확산, 극히 드묾) | `/timelines/0/phases/3/emergency/1` |

### phases/4 — `period` = Day 14-30 · `label` = 최종 평가기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 최대 효과 유지 상태 | `/timelines/0/phases/4/normal/0` |
| `normal` | 1 | 자연스러운 결과 완성 | `/timelines/0/phases/4/normal/1` |
| `normal` | 2 | 재시술 필요 여부 판단 가능 시점 | `/timelines/0/phases/4/normal/2` |
| `abnormal` | 0 | Day 14에도 효과 부족 (터치업 고려) | `/timelines/0/phases/4/abnormal/0` |
| `abnormal` | 1 | 경미한 비대칭 잔존 | `/timelines/0/phases/4/abnormal/1` |
| `caution` | 0 | 예상 부위 외 근육 약화 | `/timelines/0/phases/4/caution/0` |
| `caution` | 1 | 지속적 두통 | `/timelines/0/phases/4/caution/1` |
| `emergency` | 0 | 전신 근육 약화 (독소 전신 확산, 극히 드묾) | `/timelines/0/phases/4/emergency/0` |

## 3. 수동 표현 (직접 읽기) — 원문 구절과 관찰 칸 분리

| Pointer | 구간 | 원문 구절 | 탐색 관점(잠정) | 잠정 메모 |
|---|---|---|---|---|
| `/timelines/0/id` | [0,5) | botox | id_code | 영문 ID. 형태소 제외 |
| `/timelines/0/category` | [0,2) | M1 | id_code | 분류 코드. 다른 원장과의 연결은 후속(F) |
| `/timelines/0/name` | [0,3) | 보톡스 | procedure_name | 시술명 표면형 |
| `/timelines/0/phases/0/period` | [0,5) | Day 0 | period | 기간 표기. 단위 Day·영문 |
| `/timelines/0/phases/0/label` | [0,5) | 시술 당일 | reference_point | 「Day 0」 = 시술 당일이라는 원문 대응(기준 시점 = 시술) |
| `/timelines/0/phases/0/normal/0` | [0,5) | 주사 부위 | site | 반응 위치 = 주사 부위(구체 부위 없음) |
| `/timelines/0/phases/0/normal/0` | [6,14) | 작은 돌기/발적 | size, alt | 「작은」 크기 수식이 돌기만인지 발적까지인지 원문으로 불분명 |
| `/timelines/0/phases/0/normal/0` | [15,28) | (15-60분 내 소실) | resolution, time_range | 분 단위 소실 시간. 기준이 발현 시점인지 시술 시점인지 원문 없음 |
| `/timelines/0/phases/0/normal/1` | [0,11) | 약간의 따끔함/화끈감 | degree, alt | 정도 「약간의」 |
| `/timelines/0/phases/0/normal/2` | [0,12) | 주사 부위 경미한 압통 | site, severity | |  |
| `/timelines/0/phases/0/abnormal/0` | [0,5) | 경미한 멍 | severity | |  |
| `/timelines/0/phases/0/abnormal/0` | [6,15) | (혈관 천자 시) | condition, cause | 「시」 조건 — 혈관 천자가 있었을 때 |
| `/timelines/0/phases/0/caution/0` | [0,17) | 1시간 이상 지속되는 발적/부종 | duration_threshold, persistence, alt | 「이상」 비교 연산. 1시간 미만은 normal/0 쪽 15-60분과 맞물림(잠정) |
| `/timelines/0/phases/0/emergency/0` | [0,12) | 심한 두드러기/호흡곤란 | severity, alt | 「심한」 이 호흡곤란까지 걸리는지 불분명 |
| `/timelines/0/phases/0/emergency/0` | [13,28) | (아나필락시스, 극히 드묾) | label, frequency | 진단명 병기 + 빈도 「극히 드묾」. 백분율 없음 |
| `/timelines/0/phases/0/emergency/1` | [0,13) | 심한 전신 발진/혈관부종 | severity, extent, alt | 「전신」 범위. 수식이 혈관부종까지 걸리는지 불분명 |
| `/timelines/0/phases/1/period` | [0,7) | Day 1-3 | period, time_range | |  |
| `/timelines/0/phases/1/label` | [0,5) | 초기 경과 | phase_label | |  |
| `/timelines/0/phases/1/normal/0` | [0,17) | 미세한 근육 무거움/당김감 시작 | degree, onset, alt | 「시작」 = 발현 |
| `/timelines/0/phases/1/normal/0` | [18,27) | (Day 2-3) | onset_time, time_range | 기간(Day 1-3) 안의 세부 발현 시점 |
| `/timelines/0/phases/1/normal/1` | [0,15) | 효과 아직 안 보임 (정상) | negation, temporal, judgment | 「아직 안」 부정+시간. 「(정상)」 판정 병기 |
| `/timelines/0/phases/1/normal/2` | [0,12) | 주사 부위 약간의 붓기 | site, degree | |  |
| `/timelines/0/phases/1/normal/2` | [13,22) | (1-2일 소실) | resolution, time_range | 소실까지 1-2일. 기준 시점 원문 없음 |
| `/timelines/0/phases/1/abnormal/0` | [2,22) | (수일 내 소실, 보라색→황색 변화) | resolution, approx_time, color_change | 「수일」 근사. 화살표 = 색 변화 순서 |
| `/timelines/0/phases/1/abnormal/1` | [0,17) | 경미한 두통 (수시간 내 소실) | severity, resolution, approx_time | |  |
| `/timelines/0/phases/1/caution/0` | [0,20) | 지속되는 심한 두통 (24시간 이상) | persistence, severity, duration_threshold | 24시간 이상이 두통 지속 시간이라는 것은 잠정(괄호 위치) |
| `/timelines/0/phases/1/caution/1` | [0,17) | 비대칭 느낌 (근육 반응 차이) | subjective, cause_gloss | 「느낌」 주관 표현. 괄호 = 설명/원인 |
| `/timelines/0/phases/1/emergency/0` | [0,8) | 시야 변화/복시 | alt | |  |
| `/timelines/0/phases/1/emergency/1` | [0,7) | 심한 안검하수 | severity | |  |
| `/timelines/0/phases/1/emergency/2` | [0,14) | 연하곤란 (삼키기 어려움) | gloss | 괄호 = 쉬운 말 풀이 |
| `/timelines/0/phases/2/period` | [0,7) | Day 3-7 | period, time_range | |  |
| `/timelines/0/phases/2/label` | [0,6) | 효과 발현기 | phase_label, onset | 기간 이름이 효과 발현을 가리킴 |
| `/timelines/0/phases/2/normal/0` | [0,18) | 주사 부위 근육 움직임 감소 시작 | site, change, onset | |  |
| `/timelines/0/phases/2/normal/1` | [0,13) | 표정 변화 시작 (미세) | onset, degree | 「(미세)」 정도가 괄호로 뒤에 붙음 |
| `/timelines/0/phases/2/normal/2` | [0,9) | 이마/눈가 당김감 | site, alt | 구체 부위 이마·눈가. 시술 부위를 한정하는지 원문 불분명 |
| `/timelines/0/phases/2/abnormal/0` | [0,21) | 경미한 비대칭 (좌우 효과 속도 차이) | severity, speed, cause_gloss | 속도 차이 = 원인 설명(잠정) |
| `/timelines/0/phases/2/abnormal/1` | [0,9) | 가벼운 눈 무거움 | degree, site | |  |
| `/timelines/0/phases/2/caution/0` | [0,16) | 뚜렷한 비대칭 (한쪽만 효과) | degree, restriction | 「만」 한정 |
| `/timelines/0/phases/2/caution/1` | [0,17) | 눈꺼풀 처짐 (경미한 안검하수) | site, severity, gloss | 같은 시술 phases/1/emergency/1 은 「심한 안검하수」 → 정도에 따라 등급이 갈림(잠정) |
| `/timelines/0/phases/2/emergency/0` | [0,11) | 시야 장애/복시 악화 | alt, worsening | 「악화」 가 복시만인지 둘 다인지 불분명 |
| `/timelines/0/phases/2/emergency/1` | [0,10) | 연하곤란/호흡 불편 | alt | |  |
| `/timelines/0/phases/3/period` | [0,8) | Day 7-14 | period, time_range | |  |
| `/timelines/0/phases/3/label` | [0,6) | 효과 안정기 | phase_label | |  |
| `/timelines/0/phases/3/normal/0` | [0,23) | 효과 본격적으로 나타남 (Day 7-10) | onset, degree, onset_time | 「본격적으로」 부사 |
| `/timelines/0/phases/3/normal/1` | [0,15) | Day 14 최대 효과 도달 | peak_time | 최대 효과 시점. Day 14 는 phases/3(7-14) 끝과 phases/4(14-30) 시작에 동시에 걸림 |
| `/timelines/0/phases/3/normal/2` | [0,20) | 자연스러운 표정 유지되면서 주름 감소 | quality, concurrent, change | 「-면서」 동시 |
| `/timelines/0/phases/3/abnormal/0` | [0,17) | 효과 미흡 (용량 부족 가능성) | insufficiency, possibility, cause | 「가능성」 원인 추정 |
| `/timelines/0/phases/3/abnormal/1` | [0,9) | 경미한 좌우 차이 | severity | |  |
| `/timelines/0/phases/3/caution/0` | [0,9) | 눈꺼풀 처짐 지속 | persistence | |  |
| `/timelines/0/phases/3/caution/1` | [0,12) | 표정 부자연스러움 심화 | worsening | |  |
| `/timelines/0/phases/3/emergency/0` | [0,8) | 시야 장애 지속 | persistence | |  |
| `/timelines/0/phases/3/emergency/1` | [0,27) | 연하곤란/호흡곤란 (독소 원격 확산, 극히 드묾) | alt, cause, frequency | 원인 「독소 원격 확산」 + 빈도 |
| `/timelines/0/phases/4/period` | [0,9) | Day 14-30 | period, time_range | |  |
| `/timelines/0/phases/4/label` | [0,6) | 최종 평가기 | phase_label | |  |
| `/timelines/0/phases/4/normal/0` | [0,11) | 최대 효과 유지 상태 | maintenance | |  |
| `/timelines/0/phases/4/normal/1` | [0,11) | 자연스러운 결과 완성 | quality | |  |
| `/timelines/0/phases/4/normal/2` | [0,18) | 재시술 필요 여부 판단 가능 시점 | retreatment_decision, possibility | 재시술 「간격」이 아니라 판단 시점 |
| `/timelines/0/phases/4/abnormal/0` | [0,14) | Day 14에도 효과 부족 | time_anchor, concessive, insufficiency | 「에도」 양보 |
| `/timelines/0/phases/4/abnormal/0` | [15,23) | (터치업 고려) | recommendation, retreatment | 「고려」 권고 강도 약함 |
| `/timelines/0/phases/4/abnormal/1` | [0,10) | 경미한 비대칭 잔존 | severity, persistence | |  |
| `/timelines/0/phases/4/caution/0` | [0,13) | 예상 부위 외 근육 약화 | site, exclusion | 「외」 = 예상 부위 밖 |
| `/timelines/0/phases/4/caution/1` | [0,6) | 지속적 두통 | persistence | |  |
| `/timelines/0/phases/4/emergency/0` | [0,26) | 전신 근육 약화 (독소 전신 확산, 극히 드묾) | extent, cause, frequency | |  |

## 4. 자동 후보 요약 (정규식 일치분만 — 전수 의미 수집 아님)

P-ADVICE 2, P-ALT 11, P-APPROX 2, P-APPROXTIME 2, P-COMPARE 2, P-COND-SI 1, P-COURSE 18, P-DAY 9, P-DEGREE 20, P-DURING 1, P-FREQ 3, P-LATIN 9, P-NEG 3, P-NUMUNIT 4, P-PAREN 20, P-POSSIB 3, P-SITE 12, P-SYMBOL 1, P-TEMPORAL 2

전체 목록은 expressions.json (segment 필터).

## 5. 잠정 관찰

- **S01-O1** 5개 기간이 Day 0 / 1-3 / 3-7 / 7-14 / 14-30 이다. 경계일(3·7·14)이 앞뒤 기간에 모두 나온다. 경계 포함 여부는 원문에 없다.
- **S01-O2** 같은 증상이 기간마다 다른 등급에 나온다: 안검하수(phases/1 emergency 「심한」, phases/2 caution 「경미한」, phases/3 caution 「지속」), 시야 장애/복시(phases/1·2·3 emergency), 비대칭(phases/1 caution, phases/2 abnormal 「경미한」·caution 「뚜렷한」, phases/3 abnormal, phases/4 abnormal 「잔존」), 두통(phases/1 abnormal·caution, phases/4 caution). 등급을 가르는 단서는 정도·지속·기간이다(잠정).
- **S01-O3** 값 안의 시간 단위가 분·시간·일·Day 로 섞여 있다. 기간(period)은 Day, 괄호 속 소실·발현 시간은 분·시간·일·Day.
- **S01-O4** 재시술 관련 표현은 「재시술 필요 여부 판단 가능 시점」(phases/4)과 「터치업 고려」뿐이다. 재시술 간격 수치는 이 구획에 없다.

## 6. 미결 (이 구획)

| ID | 분류 | 위치 | 내용 |
|---|---|---|---|
| S01-Q1 | B | `/timelines/0/phases/0/normal/0` `/timelines/0/phases/1/normal/2` `/timelines/0/phases/1/abnormal/0` `/timelines/0/phases/1/abnormal/1` | 괄호 속 소실 시간의 기준 시점(시술 후·발현 후)이 원문에 없다. |
| S01-Q2 | B | `/timelines/0/phases/*/period` | 기간 경계일의 포함·제외가 원문에 없다(Day 14 가 두 기간에 걸림). |
| S01-Q3 | P | `/timelines/0/phases/0/emergency/1` `/timelines/0/phases/0/emergency/0` `/timelines/0/phases/2/emergency/0` | 「/」 앞 수식어(심한·전신·악화)가 뒤 항목까지 걸리는지 잠정. README 의 「/」 규칙은 시술 이름 규칙이라 증상 나열에 그대로 적용하지 않는다. |

## 7. 형태소 — 알려진 오분절 (교정 안 함)

| Pointer | 구간 | 원시 토큰 | 판정/설명 | 영향 |
|---|---|---|---|---|
| `/timelines/0/phases/0/normal/0` | [23,24) | 나/NP + 의/JKG | K-NAE 「내」(이내, 의존명사)가 나/NP+의/JKG 로 분석 | 기간 한정(이내) 의미가 대명사+조사로 바뀜 — 시간 범위 손실 |
| `/timelines/0/phases/0/caution/0` | [12,14) | 발/NNG + 적/XSN | K-BALJEOK 「발적」 이 발/NNG+적/XSN 으로 분할 | 사건 명사 손실(「-적」 접미 오인) |
| `/timelines/0/phases/2/caution/1` | [12,16) | 안검/NNG + 하수/NNG | K-ANGEOMHASU 「안검하수」 분할(다른 출현은 NNP 한 토큰) | 「하수」 오의미 |
| `/timelines/0/phases/4/abnormal/0` | [16,19) | 터치/NNG + 업/NNG | K-LOANSPLIT 외래어 「터치업」 분할 | 재시술 표현 분할 |

