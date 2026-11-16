# S02 — /timelines/1 ha-filler (HA 필러)

> build.py 생성. 원문 값과 잠정 관찰은 서로 다른 절·칸에 둔다.

- 소유 범위: prefix ['/timelines/1'] · exact []
- 공유 문맥(소유 아님): ['', '/timelines', '/consensus_method', '/reaction_levels', '/reaction_levels/normal', '/reaction_levels/abnormal', '/reaction_levels/caution', '/reaction_levels/emergency']
- 직접 읽기: done (manual/S02.txt) · 마지막 읽은 Pointer `/timelines/1/phases/4/emergency/1`

## 1. 원문 — 모든 노드 (문서 순서)

| # | Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 원문 구간(cp) |
|---|---|---|---|---|---|
| 1 | `/timelines/1` | `[1]` | object | {id, category, name, phases} | 1591–3004 |
| 2 | `/timelines/1/id` | `id` | string | ha-filler | 1597–1608 |
| 3 | `/timelines/1/category` | `category` | string | M2 | 1620–1624 |
| 4 | `/timelines/1/name` | `name` | string | HA 필러 | 1632–1639 |
| 5 | `/timelines/1/phases` | `phases` | array | [길이 5] | 1649–3003 |
| 6 | `/timelines/1/phases/0` | `[0]` | object | {period, label, normal, abnormal, caution, emergency} | 1650–1998 |
| 7 | `/timelines/1/phases/0/period` | `period` | string | Day 0 | 1660–1667 |
| 8 | `/timelines/1/phases/0/label` | `label` | string | 시술 당일 | 1676–1683 |
| 9 | `/timelines/1/phases/0/normal` | `normal` | array | [길이 3] | 1693–1745 |
| 10 | `/timelines/1/phases/0/normal/0` | `[0]` | string | 즉각적인 볼륨 증가 (과교정 상태 정상) | 1694–1718 |
| 11 | `/timelines/1/phases/0/normal/1` | `[1]` | string | 주사 부위 발적/부종 | 1719–1732 |
| 12 | `/timelines/1/phases/0/normal/2` | `[2]` | string | 경미한 압통/통증 | 1733–1744 |
| 13 | `/timelines/1/phases/0/abnormal` | `abnormal` | array | [길이 2] | 1757–1792 |
| 14 | `/timelines/1/phases/0/abnormal/0` | `[0]` | string | 멍 (혈관 천자 시, 흔함) | 1758–1775 |
| 15 | `/timelines/1/phases/0/abnormal/1` | `[1]` | string | 딱딱한 느낌 (젤 뭉침) | 1776–1791 |
| 16 | `/timelines/1/phases/0/caution` | `caution` | array | [길이 2] | 1803–1869 |
| 17 | `/timelines/1/phases/0/caution/0` | `[0]` | string | 비정상적으로 심한 통증 (통증 스케일 7 이상) | 1804–1832 |
| 18 | `/timelines/1/phases/0/caution/1` | `[1]` | string | 피부색 변화 (창백/청색 -- blanching 초기 징후) | 1833–1868 |
| 19 | `/timelines/1/phases/0/emergency` | `emergency` | array | [길이 4] | 1882–1997 |
| 20 | `/timelines/1/phases/0/emergency/0` | `[0]` | string | ** 혈관폐색 (blanching/하얗게 변함) -- 골든타임 Day 0-1 ** | 1883–1930 |
| 21 | `/timelines/1/phases/0/emergency/1` | `[1]` | string | 심한 통증 + 피부 창백/청색 변화 | 1931–1952 |
| 22 | `/timelines/1/phases/0/emergency/2` | `[2]` | string | 시야 변화/시력 저하 (안동맥 폐색) | 1953–1975 |
| 23 | `/timelines/1/phases/0/emergency/3` | `[3]` | string | 아나필락시스 (두드러기/호흡곤란) | 1976–1996 |
| 24 | `/timelines/1/phases/1` | `[1]` | object | {period, label, normal, abnormal, caution, emergency} | 1999–2298 |
| 25 | `/timelines/1/phases/1/period` | `period` | string | Day 1-2 | 2009–2018 |
| 26 | `/timelines/1/phases/1/label` | `label` | string | 부종 피크기 | 2027–2035 |
| 27 | `/timelines/1/phases/1/normal` | `normal` | array | [길이 3] | 2045–2107 |
| 28 | `/timelines/1/phases/1/normal/0` | `[0]` | string | 부종 피크 (Day 2가 가장 심함, 정상) | 2046–2072 |
| 29 | `/timelines/1/phases/1/normal/1` | `[1]` | string | 멍 변색 (보라→노랑 진행) | 2073–2090 |
| 30 | `/timelines/1/phases/1/normal/2` | `[2]` | string | 주사 부위 약간의 경결감 | 2091–2106 |
| 31 | `/timelines/1/phases/1/abnormal` | `abnormal` | array | [길이 2] | 2119–2141 |
| 32 | `/timelines/1/phases/1/abnormal/0` | `[0]` | string | 예상보다 큰 부종 | 2120–2131 |
| 33 | `/timelines/1/phases/1/abnormal/1` | `[1]` | string | 비대칭 부종 | 2132–2140 |
| 34 | `/timelines/1/phases/1/caution` | `caution` | array | [길이 2] | 2152–2189 |
| 35 | `/timelines/1/phases/1/caution/0` | `[0]` | string | 지속적 심한 통증 (진통제 미반응) | 2153–2174 |
| 36 | `/timelines/1/phases/1/caution/1` | `[1]` | string | 부종 범위 급격 확대 | 2175–2188 |
| 37 | `/timelines/1/phases/1/emergency` | `emergency` | array | [길이 4] | 2202–2297 |
| 38 | `/timelines/1/phases/1/emergency/0` | `[0]` | string | ** 지연성 혈관폐색 -- 여전히 골든타임 ** | 2203–2231 |
| 39 | `/timelines/1/phases/1/emergency/1` | `[1]` | string | 피부 괴사 징후 (검은색/보라색 변색) | 2232–2255 |
| 40 | `/timelines/1/phases/1/emergency/2` | `[2]` | string | 시야 변화/두통 + 주사 부위 변색 | 2256–2277 |
| 41 | `/timelines/1/phases/1/emergency/3` | `[3]` | string | 고열 + 급격한 부종 (감염) | 2278–2296 |
| 42 | `/timelines/1/phases/2` | `[2]` | object | {period, label, normal, abnormal, caution, emergency} | 2299–2554 |
| 43 | `/timelines/1/phases/2/period` | `period` | string | Day 3-5 | 2309–2318 |
| 44 | `/timelines/1/phases/2/label` | `label` | string | 회복기 | 2327–2332 |
| 45 | `/timelines/1/phases/2/normal` | `normal` | array | [길이 4] | 2342–2401 |
| 46 | `/timelines/1/phases/2/normal/0` | `[0]` | string | 부종 점차 감소 | 2343–2353 |
| 47 | `/timelines/1/phases/2/normal/1` | `[1]` | string | 멍 황색으로 변화 (흡수 진행) | 2354–2373 |
| 48 | `/timelines/1/phases/2/normal/2` | `[2]` | string | 볼륨이 자연스러워짐 | 2374–2386 |
| 49 | `/timelines/1/phases/2/normal/3` | `[3]` | string | 주사 부위 압통 감소 | 2387–2400 |
| 50 | `/timelines/1/phases/2/abnormal` | `abnormal` | array | [길이 2] | 2413–2445 |
| 51 | `/timelines/1/phases/2/abnormal/0` | `[0]` | string | 부종 소실 느린 편 | 2414–2426 |
| 52 | `/timelines/1/phases/2/abnormal/1` | `[1]` | string | 주사 부위 딱딱한 결절 촉지 | 2427–2444 |
| 53 | `/timelines/1/phases/2/caution` | `caution` | array | [길이 3] | 2456–2505 |
| 54 | `/timelines/1/phases/2/caution/0` | `[0]` | string | 부종 감소 없이 오히려 증가 | 2457–2474 |
| 55 | `/timelines/1/phases/2/caution/1` | `[1]` | string | 발열 (37.5도 이상) | 2475–2490 |
| 56 | `/timelines/1/phases/2/caution/2` | `[2]` | string | 주사 부위 발적 확대 | 2491–2504 |
| 57 | `/timelines/1/phases/2/emergency` | `emergency` | array | [길이 2] | 2518–2553 |
| 58 | `/timelines/1/phases/2/emergency/0` | `[0]` | string | 피부 괴사 (피부 검게 변함) | 2519–2537 |
| 59 | `/timelines/1/phases/2/emergency/1` | `[1]` | string | 농 배출/고열 (감염) | 2538–2552 |
| 60 | `/timelines/1/phases/3` | `[3]` | object | {period, label, normal, abnormal, caution, emergency} | 2555–2776 |
| 61 | `/timelines/1/phases/3/period` | `period` | string | Day 5-7 | 2565–2574 |
| 62 | `/timelines/1/phases/3/label` | `label` | string | 안정기 | 2583–2588 |
| 63 | `/timelines/1/phases/3/normal` | `normal` | array | [길이 4] | 2598–2649 |
| 64 | `/timelines/1/phases/3/normal/0` | `[0]` | string | 부종 대부분 소실 | 2599–2610 |
| 65 | `/timelines/1/phases/3/normal/1` | `[1]` | string | 멍 거의 소실 | 2611–2620 |
| 66 | `/timelines/1/phases/3/normal/2` | `[2]` | string | 최종 결과에 가까운 상태 | 2621–2636 |
| 67 | `/timelines/1/phases/3/normal/3` | `[3]` | string | 촉감 자연스러워짐 | 2637–2648 |
| 68 | `/timelines/1/phases/3/abnormal` | `abnormal` | array | [길이 2] | 2661–2696 |
| 69 | `/timelines/1/phases/3/abnormal/0` | `[0]` | string | 미세 결절 촉지 (마사지로 개선 가능) | 2662–2685 |
| 70 | `/timelines/1/phases/3/abnormal/1` | `[1]` | string | 경미한 비대칭 | 2686–2695 |
| 71 | `/timelines/1/phases/3/caution` | `caution` | array | [길이 2] | 2707–2731 |
| 72 | `/timelines/1/phases/3/caution/0` | `[0]` | string | 결절 크기 증가 | 2708–2718 |
| 73 | `/timelines/1/phases/3/caution/1` | `[1]` | string | 지연성 부종 재발 | 2719–2730 |
| 74 | `/timelines/1/phases/3/emergency` | `emergency` | array | [길이 2] | 2744–2775 |
| 75 | `/timelines/1/phases/3/emergency/0` | `[0]` | string | 지연성 감염 (발열/농/발적) | 2745–2763 |
| 76 | `/timelines/1/phases/3/emergency/1` | `[1]` | string | 피부 변색 지속 | 2764–2774 |
| 77 | `/timelines/1/phases/4` | `[4]` | object | {period, label, normal, abnormal, caution, emergency} | 2777–3002 |
| 78 | `/timelines/1/phases/4/period` | `period` | string | Day 8-14 | 2787–2797 |
| 79 | `/timelines/1/phases/4/label` | `label` | string | 최종 평가기 | 2806–2814 |
| 80 | `/timelines/1/phases/4/normal` | `normal` | array | [길이 3] | 2824–2869 |
| 81 | `/timelines/1/phases/4/normal/0` | `[0]` | string | 최종 결과 확인 가능 | 2825–2838 |
| 82 | `/timelines/1/phases/4/normal/1` | `[1]` | string | 필러 안정화 완료 | 2839–2850 |
| 83 | `/timelines/1/phases/4/normal/2` | `[2]` | string | 터치업 필요 여부 판단 시점 | 2851–2868 |
| 84 | `/timelines/1/phases/4/abnormal` | `abnormal` | array | [길이 2] | 2881–2911 |
| 85 | `/timelines/1/phases/4/abnormal/0` | `[0]` | string | 볼륨 비대칭 (재시술 고려) | 2882–2899 |
| 86 | `/timelines/1/phases/4/abnormal/1` | `[1]` | string | 미세 결절 잔존 | 2900–2910 |
| 87 | `/timelines/1/phases/4/caution` | `caution` | array | [길이 2] | 2922–2966 |
| 88 | `/timelines/1/phases/4/caution/0` | `[0]` | string | 지연성 과민반응 (부종/발적 재발) | 2923–2944 |
| 89 | `/timelines/1/phases/4/caution/1` | `[1]` | string | 육아종 초기 징후 (단단한 결절) | 2945–2965 |
| 90 | `/timelines/1/phases/4/emergency` | `emergency` | array | [길이 2] | 2979–3001 |
| 91 | `/timelines/1/phases/4/emergency/0` | `[0]` | string | 지연성 감염/농양 | 2980–2991 |
| 92 | `/timelines/1/phases/4/emergency/1` | `[1]` | string | 육아종 형성 | 2992–3000 |

## 2. 원문 — 기간별 보기 (같은 값, 원본 컬럼명 그대로)

`id` = ha-filler · `category` = M2 · `name` = HA 필러

### phases/0 — `period` = Day 0 · `label` = 시술 당일

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 즉각적인 볼륨 증가 (과교정 상태 정상) | `/timelines/1/phases/0/normal/0` |
| `normal` | 1 | 주사 부위 발적/부종 | `/timelines/1/phases/0/normal/1` |
| `normal` | 2 | 경미한 압통/통증 | `/timelines/1/phases/0/normal/2` |
| `abnormal` | 0 | 멍 (혈관 천자 시, 흔함) | `/timelines/1/phases/0/abnormal/0` |
| `abnormal` | 1 | 딱딱한 느낌 (젤 뭉침) | `/timelines/1/phases/0/abnormal/1` |
| `caution` | 0 | 비정상적으로 심한 통증 (통증 스케일 7 이상) | `/timelines/1/phases/0/caution/0` |
| `caution` | 1 | 피부색 변화 (창백/청색 -- blanching 초기 징후) | `/timelines/1/phases/0/caution/1` |
| `emergency` | 0 | ** 혈관폐색 (blanching/하얗게 변함) -- 골든타임 Day 0-1 ** | `/timelines/1/phases/0/emergency/0` |
| `emergency` | 1 | 심한 통증 + 피부 창백/청색 변화 | `/timelines/1/phases/0/emergency/1` |
| `emergency` | 2 | 시야 변화/시력 저하 (안동맥 폐색) | `/timelines/1/phases/0/emergency/2` |
| `emergency` | 3 | 아나필락시스 (두드러기/호흡곤란) | `/timelines/1/phases/0/emergency/3` |

### phases/1 — `period` = Day 1-2 · `label` = 부종 피크기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 부종 피크 (Day 2가 가장 심함, 정상) | `/timelines/1/phases/1/normal/0` |
| `normal` | 1 | 멍 변색 (보라→노랑 진행) | `/timelines/1/phases/1/normal/1` |
| `normal` | 2 | 주사 부위 약간의 경결감 | `/timelines/1/phases/1/normal/2` |
| `abnormal` | 0 | 예상보다 큰 부종 | `/timelines/1/phases/1/abnormal/0` |
| `abnormal` | 1 | 비대칭 부종 | `/timelines/1/phases/1/abnormal/1` |
| `caution` | 0 | 지속적 심한 통증 (진통제 미반응) | `/timelines/1/phases/1/caution/0` |
| `caution` | 1 | 부종 범위 급격 확대 | `/timelines/1/phases/1/caution/1` |
| `emergency` | 0 | ** 지연성 혈관폐색 -- 여전히 골든타임 ** | `/timelines/1/phases/1/emergency/0` |
| `emergency` | 1 | 피부 괴사 징후 (검은색/보라색 변색) | `/timelines/1/phases/1/emergency/1` |
| `emergency` | 2 | 시야 변화/두통 + 주사 부위 변색 | `/timelines/1/phases/1/emergency/2` |
| `emergency` | 3 | 고열 + 급격한 부종 (감염) | `/timelines/1/phases/1/emergency/3` |

### phases/2 — `period` = Day 3-5 · `label` = 회복기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 부종 점차 감소 | `/timelines/1/phases/2/normal/0` |
| `normal` | 1 | 멍 황색으로 변화 (흡수 진행) | `/timelines/1/phases/2/normal/1` |
| `normal` | 2 | 볼륨이 자연스러워짐 | `/timelines/1/phases/2/normal/2` |
| `normal` | 3 | 주사 부위 압통 감소 | `/timelines/1/phases/2/normal/3` |
| `abnormal` | 0 | 부종 소실 느린 편 | `/timelines/1/phases/2/abnormal/0` |
| `abnormal` | 1 | 주사 부위 딱딱한 결절 촉지 | `/timelines/1/phases/2/abnormal/1` |
| `caution` | 0 | 부종 감소 없이 오히려 증가 | `/timelines/1/phases/2/caution/0` |
| `caution` | 1 | 발열 (37.5도 이상) | `/timelines/1/phases/2/caution/1` |
| `caution` | 2 | 주사 부위 발적 확대 | `/timelines/1/phases/2/caution/2` |
| `emergency` | 0 | 피부 괴사 (피부 검게 변함) | `/timelines/1/phases/2/emergency/0` |
| `emergency` | 1 | 농 배출/고열 (감염) | `/timelines/1/phases/2/emergency/1` |

### phases/3 — `period` = Day 5-7 · `label` = 안정기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 부종 대부분 소실 | `/timelines/1/phases/3/normal/0` |
| `normal` | 1 | 멍 거의 소실 | `/timelines/1/phases/3/normal/1` |
| `normal` | 2 | 최종 결과에 가까운 상태 | `/timelines/1/phases/3/normal/2` |
| `normal` | 3 | 촉감 자연스러워짐 | `/timelines/1/phases/3/normal/3` |
| `abnormal` | 0 | 미세 결절 촉지 (마사지로 개선 가능) | `/timelines/1/phases/3/abnormal/0` |
| `abnormal` | 1 | 경미한 비대칭 | `/timelines/1/phases/3/abnormal/1` |
| `caution` | 0 | 결절 크기 증가 | `/timelines/1/phases/3/caution/0` |
| `caution` | 1 | 지연성 부종 재발 | `/timelines/1/phases/3/caution/1` |
| `emergency` | 0 | 지연성 감염 (발열/농/발적) | `/timelines/1/phases/3/emergency/0` |
| `emergency` | 1 | 피부 변색 지속 | `/timelines/1/phases/3/emergency/1` |

### phases/4 — `period` = Day 8-14 · `label` = 최종 평가기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 최종 결과 확인 가능 | `/timelines/1/phases/4/normal/0` |
| `normal` | 1 | 필러 안정화 완료 | `/timelines/1/phases/4/normal/1` |
| `normal` | 2 | 터치업 필요 여부 판단 시점 | `/timelines/1/phases/4/normal/2` |
| `abnormal` | 0 | 볼륨 비대칭 (재시술 고려) | `/timelines/1/phases/4/abnormal/0` |
| `abnormal` | 1 | 미세 결절 잔존 | `/timelines/1/phases/4/abnormal/1` |
| `caution` | 0 | 지연성 과민반응 (부종/발적 재발) | `/timelines/1/phases/4/caution/0` |
| `caution` | 1 | 육아종 초기 징후 (단단한 결절) | `/timelines/1/phases/4/caution/1` |
| `emergency` | 0 | 지연성 감염/농양 | `/timelines/1/phases/4/emergency/0` |
| `emergency` | 1 | 육아종 형성 | `/timelines/1/phases/4/emergency/1` |

## 3. 수동 표현 (직접 읽기) — 원문 구절과 관찰 칸 분리

| Pointer | 구간 | 원문 구절 | 탐색 관점(잠정) | 잠정 메모 |
|---|---|---|---|---|
| `/timelines/1/id` | [0,9) | ha-filler | id_code | |  |
| `/timelines/1/category` | [0,2) | M2 | id_code | |  |
| `/timelines/1/name` | [0,5) | HA 필러 | procedure_name, mixed_script | 영문 약어 HA + 한글 |
| `/timelines/1/phases/0/period` | [0,5) | Day 0 | period | |  |
| `/timelines/1/phases/0/label` | [0,5) | 시술 당일 | reference_point | |  |
| `/timelines/1/phases/0/normal/0` | [0,10) | 즉각적인 볼륨 증가 | onset_speed, change | 「즉각적인」 발현 속도 |
| `/timelines/1/phases/0/normal/0` | [11,22) | (과교정 상태 정상) | judgment | 과교정 상태가 정상이라는 판정 |
| `/timelines/1/phases/0/normal/1` | [0,11) | 주사 부위 발적/부종 | site, alt | |  |
| `/timelines/1/phases/0/normal/2` | [0,9) | 경미한 압통/통증 | severity, alt | |  |
| `/timelines/1/phases/0/abnormal/0` | [2,15) | (혈관 천자 시, 흔함) | condition, frequency | 「시」 조건 + 빈도 「흔함」. 빈도가 조건부인지 전체인지 불분명 |
| `/timelines/1/phases/0/abnormal/1` | [0,13) | 딱딱한 느낌 (젤 뭉침) | texture, subjective, cause_gloss | |  |
| `/timelines/1/phases/0/caution/0` | [0,12) | 비정상적으로 심한 통증 | degree, severity | 「비정상적으로」 부사 |
| `/timelines/1/phases/0/caution/0` | [13,26) | (통증 스케일 7 이상) | scale_threshold | 「통증 스케일」 척도 이름·만점 원문 없음. 「이상」 비교 |
| `/timelines/1/phases/0/caution/1` | [0,33) | 피부색 변화 (창백/청색 -- blanching 초기 징후) | color_change, alt, mixed_script, early_sign | 영어 「blanching」 병기. 「초기 징후」 |
| `/timelines/1/phases/0/emergency/0` | [0,45) | ** 혈관폐색 (blanching/하얗게 변함) -- 골든타임 Day 0-1 ** | emphasis_markup, mixed_script, action_window | 앞뒤 「**」 강조 기호가 값 안에 있다(원문 그대로) |
| `/timelines/1/phases/0/emergency/0` | [30,42) | 골든타임 Day 0-1 | action_window, time_range | 대응 시한. 무엇의 골든타임인지(처치) 원문 생략 |
| `/timelines/1/phases/0/emergency/1` | [0,19) | 심한 통증 + 피부 창백/청색 변화 | severity, co_occurrence, alt | 「+」 = 동반. README 의 「+」 는 시술 규칙이므로 여기선 증상 동반(잠정) |
| `/timelines/1/phases/0/emergency/2` | [0,20) | 시야 변화/시력 저하 (안동맥 폐색) | alt, cause_label | |  |
| `/timelines/1/phases/0/emergency/3` | [0,18) | 아나필락시스 (두드러기/호흡곤란) | label, gloss, alt | botox 와 달리 빈도 표현 없음 |
| `/timelines/1/phases/1/period` | [0,7) | Day 1-2 | period, time_range | |  |
| `/timelines/1/phases/1/label` | [0,6) | 부종 피크기 | phase_label, peak | |  |
| `/timelines/1/phases/1/normal/0` | [0,24) | 부종 피크 (Day 2가 가장 심함, 정상) | peak, peak_time, superlative, judgment | 「가장」 최상급 |
| `/timelines/1/phases/1/normal/1` | [0,15) | 멍 변색 (보라→노랑 진행) | color_change, sequence_arrow | botox 「보라색→황색」 과 표기 다름 |
| `/timelines/1/phases/1/normal/2` | [0,13) | 주사 부위 약간의 경결감 | site, degree | |  |
| `/timelines/1/phases/1/abnormal/0` | [0,9) | 예상보다 큰 부종 | comparison, size | 「예상보다」 비교 기준 = 예상(미정의) |
| `/timelines/1/phases/1/abnormal/1` | [0,6) | 비대칭 부종 | asymmetry | |  |
| `/timelines/1/phases/1/caution/0` | [0,19) | 지속적 심한 통증 (진통제 미반응) | persistence, severity, negation | 「미반응」 부정 |
| `/timelines/1/phases/1/caution/1` | [0,11) | 부종 범위 급격 확대 | extent, speed, worsening | 「급격」 속도 |
| `/timelines/1/phases/1/emergency/0` | [0,26) | ** 지연성 혈관폐색 -- 여전히 골든타임 ** | emphasis_markup, delayed_onset, action_window | 「여전히」 = 앞 기간 골든타임과 연속(잠정). Day 범위 명시 없음 |
| `/timelines/1/phases/1/emergency/1` | [0,21) | 피부 괴사 징후 (검은색/보라색 변색) | early_sign, color_change, alt | |  |
| `/timelines/1/phases/1/emergency/2` | [0,19) | 시야 변화/두통 + 주사 부위 변색 | alt, co_occurrence, site | |  |
| `/timelines/1/phases/1/emergency/3` | [0,16) | 고열 + 급격한 부종 (감염) | co_occurrence, speed, cause_label | |  |
| `/timelines/1/phases/2/period` | [0,7) | Day 3-5 | period, time_range | |  |
| `/timelines/1/phases/2/label` | [0,3) | 회복기 | phase_label | |  |
| `/timelines/1/phases/2/normal/0` | [0,8) | 부종 점차 감소 | speed, change | 「점차」 속도 |
| `/timelines/1/phases/2/normal/1` | [0,17) | 멍 황색으로 변화 (흡수 진행) | color_change, progress | |  |
| `/timelines/1/phases/2/normal/2` | [0,10) | 볼륨이 자연스러워짐 | quality, change | |  |
| `/timelines/1/phases/2/normal/3` | [0,11) | 주사 부위 압통 감소 | site, change | |  |
| `/timelines/1/phases/2/abnormal/0` | [0,10) | 부종 소실 느린 편 | speed, hedge | 「느린 편」 완곡 |
| `/timelines/1/phases/2/abnormal/1` | [0,15) | 주사 부위 딱딱한 결절 촉지 | site, texture, detection | 「촉지」 = 만져짐 |
| `/timelines/1/phases/2/caution/0` | [0,15) | 부종 감소 없이 오히려 증가 | negation, contrast, worsening | 「없이 오히려」 |
| `/timelines/1/phases/2/caution/1` | [0,13) | 발열 (37.5도 이상) | numeric_threshold, unit | 도 = 체온 단위(원문 「도」) |
| `/timelines/1/phases/2/caution/2` | [0,11) | 주사 부위 발적 확대 | site, extent | |  |
| `/timelines/1/phases/2/emergency/0` | [0,16) | 피부 괴사 (피부 검게 변함) | gloss, color_change | |  |
| `/timelines/1/phases/2/emergency/1` | [0,12) | 농 배출/고열 (감염) | alt, cause_label | |  |
| `/timelines/1/phases/3/period` | [0,7) | Day 5-7 | period, time_range | |  |
| `/timelines/1/phases/3/label` | [0,3) | 안정기 | phase_label | |  |
| `/timelines/1/phases/3/normal/0` | [0,9) | 부종 대부분 소실 | proportion_approx, resolution | 「대부분」 근사 |
| `/timelines/1/phases/3/normal/1` | [0,7) | 멍 거의 소실 | approx, resolution | 「거의」 |
| `/timelines/1/phases/3/normal/2` | [0,13) | 최종 결과에 가까운 상태 | approx | |  |
| `/timelines/1/phases/3/normal/3` | [0,9) | 촉감 자연스러워짐 | quality, change | |  |
| `/timelines/1/phases/3/abnormal/0` | [0,21) | 미세 결절 촉지 (마사지로 개선 가능) | size, detection, management, possibility | 관리 방법 「마사지」. 누가·언제 하는지 원문 없음 |
| `/timelines/1/phases/3/abnormal/1` | [0,7) | 경미한 비대칭 | severity | |  |
| `/timelines/1/phases/3/caution/0` | [0,8) | 결절 크기 증가 | size, worsening | |  |
| `/timelines/1/phases/3/caution/1` | [0,9) | 지연성 부종 재발 | delayed_onset, recurrence | |  |
| `/timelines/1/phases/3/emergency/0` | [0,16) | 지연성 감염 (발열/농/발적) | delayed_onset, gloss, alt | |  |
| `/timelines/1/phases/3/emergency/1` | [0,8) | 피부 변색 지속 | persistence | |  |
| `/timelines/1/phases/4/period` | [0,8) | Day 8-14 | period, time_range | 앞 기간 Day 5-7 과 경계가 겹치지 않음(다른 시술은 겹침) |
| `/timelines/1/phases/4/label` | [0,6) | 최종 평가기 | phase_label | |  |
| `/timelines/1/phases/4/normal/0` | [0,11) | 최종 결과 확인 가능 | possibility, evaluation | |  |
| `/timelines/1/phases/4/normal/1` | [0,9) | 필러 안정화 완료 | completion | |  |
| `/timelines/1/phases/4/normal/2` | [0,15) | 터치업 필요 여부 판단 시점 | retreatment_decision | |  |
| `/timelines/1/phases/4/abnormal/0` | [0,15) | 볼륨 비대칭 (재시술 고려) | asymmetry, recommendation, retreatment | |  |
| `/timelines/1/phases/4/abnormal/1` | [0,8) | 미세 결절 잔존 | size, persistence | |  |
| `/timelines/1/phases/4/caution/0` | [0,19) | 지연성 과민반응 (부종/발적 재발) | delayed_onset, recurrence, alt | |  |
| `/timelines/1/phases/4/caution/1` | [0,18) | 육아종 초기 징후 (단단한 결절) | early_sign, texture | |  |
| `/timelines/1/phases/4/emergency/0` | [0,9) | 지연성 감염/농양 | delayed_onset, alt | |  |
| `/timelines/1/phases/4/emergency/1` | [0,6) | 육아종 형성 | formation | 같은 기간 caution/1 은 「초기 징후」, emergency/1 은 「형성」 |

## 4. 자동 후보 요약 (정규식 일치분만 — 전수 의미 수집 아님)

P-ADVICE 3, P-AFTER 3, P-ALT 13, P-APPROX 4, P-COMPARE 3, P-COND-SI 1, P-COURSE 26, P-DAY 7, P-DEGREE 13, P-DURING 1, P-FREQ 1, P-LATIN 10, P-NEG 2, P-NUMUNIT 1, P-PAREN 22, P-POSSIB 3, P-SCALE 1, P-SITE 6, P-SPEED 3, P-SYMBOL 11, P-TEMPORAL 2

전체 목록은 expressions.json (segment 필터).

## 5. 잠정 관찰

- **S02-O1** 기간이 Day 0 / 1-2 / 3-5 / 5-7 / 8-14 이다. 1-2 와 3-5 사이에 Day 2.x~3 공백이, 5-7 과 8-14 사이에 경계 비겹침이 있다. Day 5 는 두 기간에 걸린다. 다른 구획과 기간 분할이 다르다.
- **S02-O2** emergency 값 두 개(phases/0/emergency/0, phases/1/emergency/0)가 「** … **」 로 감싸여 있다. 강조 의도로 보이나(잠정) 원문 기호를 그대로 보존한다.
- **S02-O3** 「골든타임」 이 두 기간에 나온다. phases/0 은 「Day 0-1」 범위, phases/1 은 「여전히」 만 있고 범위가 없다.
- **S02-O4** 「+」 가 증상 동반 나열에 쓰였다(phases/0/emergency/1, phases/1/emergency/2·3). 시술 결합 규칙과 다른 용법이다(잠정).
- **S02-O5** 관리·대응 표현: 마사지로 개선 가능, 터치업 필요 여부 판단, 재시술 고려. 재시술 간격 수치는 없다.

## 6. 미결 (이 구획)

| ID | 분류 | 위치 | 내용 |
|---|---|---|---|
| S02-Q1 | B | `/timelines/1/phases/0/emergency/0` `/timelines/1/phases/1/emergency/0` | 「골든타임」 이 어떤 처치의 시한인지 원문에 없다. phases/1 은 범위도 없다. |
| S02-Q2 | B | `/timelines/1/phases/0/caution/0` | 「통증 스케일 7 이상」 의 척도 정의(0-10 등)가 원문에 없다. |
| S02-Q3 | I | `/timelines/1/phases/*/period` | 같은 원장 안에서 기간 경계 방식이 시술마다 다르다(겹침·공백). 원문 내 불일치로 기록(I-PERIOD). |
| S02-Q4 | P | `/timelines/1/phases/0/abnormal/0` | 「흔함」 이 혈관 천자 시 조건부 빈도인지 멍 전체 빈도인지 잠정. |

## 7. 형태소 — 알려진 오분절 (교정 안 함)

| Pointer | 구간 | 원시 토큰 | 판정/설명 | 영향 |
|---|---|---|---|---|
| `/timelines/1/phases/0/normal/1` | [6,8) | 발/NNG + 적/XSN | K-BALJEOK 「발적」 이 발/NNG+적/XSN 으로 분할 | 사건 명사 손실(「-적」 접미 오인) |
| `/timelines/1/phases/0/abnormal/1` | [8,9) | 젤/MAG | K-MAG-NOUN 명사 「젤」 이 MAG | 물질 명사 오태깅 |
| `/timelines/1/phases/0/emergency/2` | [13,16) | 안/NNG + 동맥/NNG | K-ANDONGMAEK 「안동맥」 이 안+동맥 으로 분할 | 「안」 부정 오탐 위험, 해부 명칭 손실 |
| `/timelines/1/phases/1/normal/1` | [0,1) | 멍/MAG | K-MAG-NOUN 명사 「멍」 이 MAG(부사) | 사건 명사를 부사로 오태깅 — 명사 기준 탐색에서 누락 |
| `/timelines/1/phases/1/emergency/0` | [19,23) | 골든/NNG + 타임/NNG | K-LOANSPLIT 외래어 복합어 분할(다른 출현은 NNP 한 토큰) | 대응 시한 표현이 두 토큰 |
| `/timelines/1/phases/2/normal/1` | [0,1) | 멍/MAG | K-MAG-NOUN 명사 「멍」 이 MAG(부사) | 사건 명사를 부사로 오태깅 — 명사 기준 탐색에서 누락 |
| `/timelines/1/phases/2/normal/3` | [6,8) | 압/NNG + 통/NNG | K-APTONG 「압통」 이 압+통 으로 분할 | 사건 명사 손실 |
| `/timelines/1/phases/2/abnormal/1` | [10,12) | 결/NNG + 절/NNG | K-GYEOLJEOL 「결절」 이 결+절 로 분할 | 사건 명사 손실 |
| `/timelines/1/phases/2/caution/2` | [6,8) | 발/NNG + 적/XSN | K-BALJEOK 「발적」 이 발/NNG+적/XSN 으로 분할 | 사건 명사 손실(「-적」 접미 오인) |
| `/timelines/1/phases/3/abnormal/0` | [3,5) | 결/NNG + 절/NNG | K-GYEOLJEOL 「결절」 이 결+절 로 분할 | 사건 명사 손실 |
| `/timelines/1/phases/3/abnormal/0` | [6,8) | 촉/NNG + 지/NNG | K-CHOKJI 「촉지」 가 촉+지 로 분할 | 감지 방식 단서 손실 |
| `/timelines/1/phases/3/emergency/0` | [13,15) | 발/NNG + 적/XSN | K-BALJEOK 「발적」 이 발/NNG+적/XSN 으로 분할 | 사건 명사 손실(「-적」 접미 오인) |
| `/timelines/1/phases/4/normal/2` | [0,3) | 터치/NNG + 업/NNG | K-LOANSPLIT 외래어 「터치업」 분할 | 재시술 표현 분할 |
| `/timelines/1/phases/4/abnormal/1` | [3,5) | 결/NNG + 절/NNG | K-GYEOLJEOL 「결절」 이 결+절 로 분할 | 사건 명사 손실 |
| `/timelines/1/phases/4/caution/0` | [13,15) | 발/NNG + 적/XSN | K-BALJEOK 「발적」 이 발/NNG+적/XSN 으로 분할 | 사건 명사 손실(「-적」 접미 오인) |
| `/timelines/1/phases/4/caution/1` | [15,17) | 결/NNG + 절/NNG | K-GYEOLJEOL 「결절」 이 결+절 로 분할 | 사건 명사 손실 |
| `/timelines/1/phases/4/emergency/1` | [0,3) | 육아/NNG + 종/NNG | K-YUKAJONG 「육아종」 이 육아+종 으로 분할 | 사건 명사 손실(「육아」 오의미) |

