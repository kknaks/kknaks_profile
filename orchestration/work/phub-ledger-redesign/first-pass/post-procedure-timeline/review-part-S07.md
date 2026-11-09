# S07 — /timelines/6 needle-rf (니들RF (미세침 고주파))

> build.py 생성. 원문 값과 잠정 관찰은 서로 다른 절·칸에 둔다.

- 소유 범위: prefix ['/timelines/6'] · exact []
- 공유 문맥(소유 아님): ['', '/timelines', '/consensus_method', '/reaction_levels', '/reaction_levels/normal', '/reaction_levels/abnormal', '/reaction_levels/caution', '/reaction_levels/emergency']
- 직접 읽기: done (manual/S07.txt) · 마지막 읽은 Pointer `/timelines/6/phases/2/emergency/1`

## 1. 원문 — 모든 노드 (문서 순서)

| # | Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 원문 구간(cp) |
|---|---|---|---|---|---|
| 1 | `/timelines/6` | `[6]` | object | {id, category, name, phases} | 8100–8843 |
| 2 | `/timelines/6/id` | `id` | string | needle-rf | 8106–8117 |
| 3 | `/timelines/6/category` | `category` | string | M11 | 8129–8134 |
| 4 | `/timelines/6/name` | `name` | string | 니들RF (미세침 고주파) | 8142–8158 |
| 5 | `/timelines/6/phases` | `phases` | array | [길이 3] | 8168–8842 |
| 6 | `/timelines/6/phases/0` | `[0]` | object | {period, label, normal, abnormal, caution, emergency} | 8169–8381 |
| 7 | `/timelines/6/phases/0/period` | `period` | string | Day 0 | 8179–8186 |
| 8 | `/timelines/6/phases/0/label` | `label` | string | 시술 당일 | 8195–8202 |
| 9 | `/timelines/6/phases/0/normal` | `normal` | array | [길이 4] | 8212–8266 |
| 10 | `/timelines/6/phases/0/normal/0` | `[0]` | string | 홍반/발적 (수시간 지속) | 8213–8229 |
| 11 | `/timelines/6/phases/0/normal/1` | `[1]` | string | 침자국 (미세한 점상 출혈) | 8230–8247 |
| 12 | `/timelines/6/phases/0/normal/2` | `[2]` | string | 경미한 부종 | 8248–8256 |
| 13 | `/timelines/6/phases/0/normal/3` | `[3]` | string | 화끈감/열감 | 8257–8265 |
| 14 | `/timelines/6/phases/0/abnormal` | `abnormal` | array | [길이 2] | 8278–8302 |
| 15 | `/timelines/6/phases/0/abnormal/0` | `[0]` | string | 예상보다 심한 출혈점 | 8279–8292 |
| 16 | `/timelines/6/phases/0/abnormal/1` | `[1]` | string | 뚜렷한 부종 | 8293–8301 |
| 17 | `/timelines/6/phases/0/caution` | `caution` | array | [길이 2] | 8313–8335 |
| 18 | `/timelines/6/phases/0/caution/0` | `[0]` | string | 수포 형성 | 8314–8321 |
| 19 | `/timelines/6/phases/0/caution/1` | `[1]` | string | 비정상적 심한 통증 | 8322–8334 |
| 20 | `/timelines/6/phases/0/emergency` | `emergency` | array | [길이 2] | 8348–8380 |
| 21 | `/timelines/6/phases/0/emergency/0` | `[0]` | string | 광범위 화상/수포 | 8349–8360 |
| 22 | `/timelines/6/phases/0/emergency/1` | `[1]` | string | 아나필락시스 (마취크림 관련) | 8361–8379 |
| 23 | `/timelines/6/phases/1` | `[1]` | object | {period, label, normal, abnormal, caution, emergency} | 8382–8626 |
| 24 | `/timelines/6/phases/1/period` | `period` | string | Day 1-3 | 8392–8401 |
| 25 | `/timelines/6/phases/1/label` | `label` | string | 회복기 | 8410–8415 |
| 26 | `/timelines/6/phases/1/normal` | `normal` | array | [길이 4] | 8425–8480 |
| 27 | `/timelines/6/phases/1/normal/0` | `[0]` | string | 홍반 점차 감소 (Day 1-2 소실) | 8426–8449 |
| 28 | `/timelines/6/phases/1/normal/1` | `[1]` | string | 침자국 소실 | 8450–8458 |
| 29 | `/timelines/6/phases/1/normal/2` | `[2]` | string | 부종 감소 | 8459–8466 |
| 30 | `/timelines/6/phases/1/normal/3` | `[3]` | string | 약간의 건조함/각질 | 8467–8479 |
| 31 | `/timelines/6/phases/1/abnormal` | `abnormal` | array | [길이 2] | 8492–8518 |
| 32 | `/timelines/6/phases/1/abnormal/0` | `[0]` | string | 홍반 3일 이상 지속 | 8493–8506 |
| 33 | `/timelines/6/phases/1/abnormal/1` | `[1]` | string | 미세 가피 형성 | 8507–8517 |
| 34 | `/timelines/6/phases/1/caution` | `caution` | array | [길이 2] | 8529–8571 |
| 35 | `/timelines/6/phases/1/caution/0` | `[0]` | string | 감염 징후 (농성 분비물 + 발적 확대) | 8530–8554 |
| 36 | `/timelines/6/phases/1/caution/1` | `[1]` | string | 화상 진행 (수포/가피) | 8555–8570 |
| 37 | `/timelines/6/phases/1/emergency` | `emergency` | array | [길이 2] | 8584–8625 |
| 38 | `/timelines/6/phases/1/emergency/0` | `[0]` | string | 감염 (고열 + 농 + 봉와직염) | 8585–8605 |
| 39 | `/timelines/6/phases/1/emergency/1` | `[1]` | string | 반흔 형성 (비후성/켈로이드) | 8606–8624 |
| 40 | `/timelines/6/phases/2` | `[2]` | object | {period, label, normal, abnormal, caution, emergency} | 8627–8841 |
| 41 | `/timelines/6/phases/2/period` | `period` | string | Day 3-7 | 8637–8646 |
| 42 | `/timelines/6/phases/2/label` | `label` | string | 안정/효과 시작기 | 8655–8666 |
| 43 | `/timelines/6/phases/2/normal` | `normal` | array | [길이 4] | 8676–8731 |
| 44 | `/timelines/6/phases/2/normal/0` | `[0]` | string | 피부 완전 정상화 | 8677–8688 |
| 45 | `/timelines/6/phases/2/normal/1` | `[1]` | string | 피부결 개선 느낌 시작 | 8689–8703 |
| 46 | `/timelines/6/phases/2/normal/2` | `[2]` | string | 메이크업 가능 | 8704–8713 |
| 47 | `/timelines/6/phases/2/normal/3` | `[3]` | string | 콜라겐 리모델링 진행 시작 | 8714–8730 |
| 48 | `/timelines/6/phases/2/abnormal` | `abnormal` | array | [길이 2] | 8743–8769 |
| 49 | `/timelines/6/phases/2/abnormal/0` | `[0]` | string | 지속적 홍반 | 8744–8752 |
| 50 | `/timelines/6/phases/2/abnormal/1` | `[1]` | string | PIH (색소침착) 시작 | 8753–8768 |
| 51 | `/timelines/6/phases/2/caution` | `caution` | array | [길이 2] | 8780–8801 |
| 52 | `/timelines/6/phases/2/caution/0` | `[0]` | string | PIH 진행 | 8781–8789 |
| 53 | `/timelines/6/phases/2/caution/1` | `[1]` | string | 반흔 초기 징후 | 8790–8800 |
| 54 | `/timelines/6/phases/2/emergency` | `emergency` | array | [길이 2] | 8814–8840 |
| 55 | `/timelines/6/phases/2/emergency/0` | `[0]` | string | 감염 (지연성) | 8815–8825 |
| 56 | `/timelines/6/phases/2/emergency/1` | `[1]` | string | 비후성 반흔/켈로이드 | 8826–8839 |

## 2. 원문 — 기간별 보기 (같은 값, 원본 컬럼명 그대로)

`id` = needle-rf · `category` = M11 · `name` = 니들RF (미세침 고주파)

### phases/0 — `period` = Day 0 · `label` = 시술 당일

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 홍반/발적 (수시간 지속) | `/timelines/6/phases/0/normal/0` |
| `normal` | 1 | 침자국 (미세한 점상 출혈) | `/timelines/6/phases/0/normal/1` |
| `normal` | 2 | 경미한 부종 | `/timelines/6/phases/0/normal/2` |
| `normal` | 3 | 화끈감/열감 | `/timelines/6/phases/0/normal/3` |
| `abnormal` | 0 | 예상보다 심한 출혈점 | `/timelines/6/phases/0/abnormal/0` |
| `abnormal` | 1 | 뚜렷한 부종 | `/timelines/6/phases/0/abnormal/1` |
| `caution` | 0 | 수포 형성 | `/timelines/6/phases/0/caution/0` |
| `caution` | 1 | 비정상적 심한 통증 | `/timelines/6/phases/0/caution/1` |
| `emergency` | 0 | 광범위 화상/수포 | `/timelines/6/phases/0/emergency/0` |
| `emergency` | 1 | 아나필락시스 (마취크림 관련) | `/timelines/6/phases/0/emergency/1` |

### phases/1 — `period` = Day 1-3 · `label` = 회복기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 홍반 점차 감소 (Day 1-2 소실) | `/timelines/6/phases/1/normal/0` |
| `normal` | 1 | 침자국 소실 | `/timelines/6/phases/1/normal/1` |
| `normal` | 2 | 부종 감소 | `/timelines/6/phases/1/normal/2` |
| `normal` | 3 | 약간의 건조함/각질 | `/timelines/6/phases/1/normal/3` |
| `abnormal` | 0 | 홍반 3일 이상 지속 | `/timelines/6/phases/1/abnormal/0` |
| `abnormal` | 1 | 미세 가피 형성 | `/timelines/6/phases/1/abnormal/1` |
| `caution` | 0 | 감염 징후 (농성 분비물 + 발적 확대) | `/timelines/6/phases/1/caution/0` |
| `caution` | 1 | 화상 진행 (수포/가피) | `/timelines/6/phases/1/caution/1` |
| `emergency` | 0 | 감염 (고열 + 농 + 봉와직염) | `/timelines/6/phases/1/emergency/0` |
| `emergency` | 1 | 반흔 형성 (비후성/켈로이드) | `/timelines/6/phases/1/emergency/1` |

### phases/2 — `period` = Day 3-7 · `label` = 안정/효과 시작기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 피부 완전 정상화 | `/timelines/6/phases/2/normal/0` |
| `normal` | 1 | 피부결 개선 느낌 시작 | `/timelines/6/phases/2/normal/1` |
| `normal` | 2 | 메이크업 가능 | `/timelines/6/phases/2/normal/2` |
| `normal` | 3 | 콜라겐 리모델링 진행 시작 | `/timelines/6/phases/2/normal/3` |
| `abnormal` | 0 | 지속적 홍반 | `/timelines/6/phases/2/abnormal/0` |
| `abnormal` | 1 | PIH (색소침착) 시작 | `/timelines/6/phases/2/abnormal/1` |
| `caution` | 0 | PIH 진행 | `/timelines/6/phases/2/caution/0` |
| `caution` | 1 | 반흔 초기 징후 | `/timelines/6/phases/2/caution/1` |
| `emergency` | 0 | 감염 (지연성) | `/timelines/6/phases/2/emergency/0` |
| `emergency` | 1 | 비후성 반흔/켈로이드 | `/timelines/6/phases/2/emergency/1` |

## 3. 수동 표현 (직접 읽기) — 원문 구절과 관찰 칸 분리

| Pointer | 구간 | 원문 구절 | 탐색 관점(잠정) | 잠정 메모 |
|---|---|---|---|---|
| `/timelines/6/id` | [0,9) | needle-rf | id_code | |  |
| `/timelines/6/category` | [0,3) | M11 | id_code | |  |
| `/timelines/6/name` | [0,14) | 니들RF (미세침 고주파) | procedure_name, mixed_script, gloss | 괄호 = 풀이 |
| `/timelines/6/phases/0/period` | [0,5) | Day 0 | period | |  |
| `/timelines/6/phases/0/label` | [0,5) | 시술 당일 | reference_point | |  |
| `/timelines/6/phases/0/normal/0` | [0,14) | 홍반/발적 (수시간 지속) | alt, duration, approx_time | |  |
| `/timelines/6/phases/0/normal/1` | [0,15) | 침자국 (미세한 점상 출혈) | gloss, size, pattern | |  |
| `/timelines/6/phases/0/normal/2` | [0,6) | 경미한 부종 | severity | |  |
| `/timelines/6/phases/0/normal/3` | [0,6) | 화끈감/열감 | alt | |  |
| `/timelines/6/phases/0/abnormal/0` | [0,11) | 예상보다 심한 출혈점 | comparison, severity | |  |
| `/timelines/6/phases/0/abnormal/1` | [0,6) | 뚜렷한 부종 | degree | |  |
| `/timelines/6/phases/0/caution/0` | [0,5) | 수포 형성 | formation | |  |
| `/timelines/6/phases/0/caution/1` | [0,10) | 비정상적 심한 통증 | degree, severity | |  |
| `/timelines/6/phases/0/emergency/0` | [0,9) | 광범위 화상/수포 | extent, alt | |  |
| `/timelines/6/phases/0/emergency/1` | [0,16) | 아나필락시스 (마취크림 관련) | label, cause_ref | |  |
| `/timelines/6/phases/1/period` | [0,7) | Day 1-3 | period, time_range | |  |
| `/timelines/6/phases/1/label` | [0,3) | 회복기 | phase_label | |  |
| `/timelines/6/phases/1/normal/0` | [0,21) | 홍반 점차 감소 (Day 1-2 소실) | speed, change, resolution, time_range | |  |
| `/timelines/6/phases/1/normal/1` | [0,6) | 침자국 소실 | resolution | |  |
| `/timelines/6/phases/1/normal/2` | [0,5) | 부종 감소 | change | |  |
| `/timelines/6/phases/1/normal/3` | [0,10) | 약간의 건조함/각질 | degree, alt | |  |
| `/timelines/6/phases/1/abnormal/0` | [0,11) | 홍반 3일 이상 지속 | duration_threshold, persistence | |  |
| `/timelines/6/phases/1/abnormal/1` | [0,8) | 미세 가피 형성 | size, formation | |  |
| `/timelines/6/phases/1/caution/0` | [0,22) | 감염 징후 (농성 분비물 + 발적 확대) | early_sign, co_occurrence, extent | |  |
| `/timelines/6/phases/1/caution/1` | [0,13) | 화상 진행 (수포/가피) | progress, alt | |  |
| `/timelines/6/phases/1/emergency/0` | [0,18) | 감염 (고열 + 농 + 봉와직염) | co_occurrence | |  |
| `/timelines/6/phases/1/emergency/1` | [0,16) | 반흔 형성 (비후성/켈로이드) | formation, alt | |  |
| `/timelines/6/phases/2/period` | [0,7) | Day 3-7 | period, time_range | |  |
| `/timelines/6/phases/2/label` | [0,9) | 안정/효과 시작기 | phase_label, alt, onset | |  |
| `/timelines/6/phases/2/normal/0` | [0,9) | 피부 완전 정상화 | degree, recovery | |  |
| `/timelines/6/phases/2/normal/1` | [0,12) | 피부결 개선 느낌 시작 | subjective, onset | |  |
| `/timelines/6/phases/2/normal/2` | [0,7) | 메이크업 가능 | activity, possibility | 조건 없음(CO2 는 「재상피화 후」) |
| `/timelines/6/phases/2/normal/3` | [0,14) | 콜라겐 리모델링 진행 시작 | mechanism, onset | |  |
| `/timelines/6/phases/2/abnormal/0` | [0,6) | 지속적 홍반 | persistence | |  |
| `/timelines/6/phases/2/abnormal/1` | [0,13) | PIH (색소침착) 시작 | abbreviation, gloss, onset | |  |
| `/timelines/6/phases/2/caution/0` | [0,6) | PIH 진행 | abbreviation, progress | |  |
| `/timelines/6/phases/2/caution/1` | [0,8) | 반흔 초기 징후 | early_sign | |  |
| `/timelines/6/phases/2/emergency/0` | [0,8) | 감염 (지연성) | delayed_onset | |  |
| `/timelines/6/phases/2/emergency/1` | [0,11) | 비후성 반흔/켈로이드 | alt | |  |

## 4. 자동 후보 요약 (정규식 일치분만 — 전수 의미 수집 아님)

P-AFTER 2, P-ALT 8, P-APPROXTIME 1, P-COMPARE 2, P-COURSE 21, P-DAY 4, P-DEGREE 11, P-DURING 1, P-LATIN 7, P-NUMUNIT 1, P-PAREN 11, P-POSSIB 1, P-SPEED 1, P-SYMBOL 3

전체 목록은 expressions.json (segment 필터).

## 5. 잠정 관찰

- **S07-O1** 기간 3개뿐(Day 0 / 1-3 / 3-7). Day 7 이후 기간이 없다. 효과 발현·재시술 판단 시점 값이 없다.
- **S07-O2** 「반흔 형성 (비후성/켈로이드)」 이 Day 1-3 emergency 에 있다. 다른 시술에서는 같은 계열 사건이 더 뒤 기간에 나온다(잠정 비교, 구획 간).

## 6. 미결 (이 구획)

| ID | 분류 | 위치 | 내용 |
|---|---|---|---|
| S07-Q1 | B | `/timelines/6/phases` | Day 7 이후 경과(효과 발현·재시술)가 원문에 없다. |

## 7. 형태소 — 알려진 오분절 (교정 안 함)

| Pointer | 구간 | 원시 토큰 | 판정/설명 | 영향 |
|---|---|---|---|---|
| `/timelines/6/name` | [6,9) | 미/NNP + 세침/NNG | K-MISECHIM 「미세침」 이 미/NNP+세침 으로 분할 | 「미세」 정도 단서 손실 |
| `/timelines/6/phases/0/normal/0` | [3,5) | 발/NNG + 적/XSN | K-BALJEOK 「발적」 이 발/NNG+적/XSN 으로 분할 | 사건 명사 손실(「-적」 접미 오인) |
| `/timelines/6/phases/1/abnormal/1` | [3,5) | 가/NNG + 피/NNG | K-GAPI 「가피」 가 가+피 로 분할 | 사건 명사 손실 |
| `/timelines/6/phases/1/caution/0` | [16,18) | 발/NNG + 적/XSN | K-BALJEOK 「발적」 이 발/NNG+적/XSN 으로 분할 | 사건 명사 손실(「-적」 접미 오인) |

