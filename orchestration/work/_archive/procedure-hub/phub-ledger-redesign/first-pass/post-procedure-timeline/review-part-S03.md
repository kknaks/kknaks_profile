# S03 — /timelines/2 hifu-rf (HIFU/RF 리프팅)

> build.py 생성. 원문 값과 잠정 관찰은 서로 다른 절·칸에 둔다.

- 소유 범위: prefix ['/timelines/2'] · exact []
- 공유 문맥(소유 아님): ['', '/timelines', '/consensus_method', '/reaction_levels', '/reaction_levels/normal', '/reaction_levels/abnormal', '/reaction_levels/caution', '/reaction_levels/emergency']
- 직접 읽기: done (manual/S03.txt) · 마지막 읽은 Pointer `/timelines/2/phases/3/emergency/1`

## 1. 원문 — 모든 노드 (문서 순서)

| # | Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 원문 구간(cp) |
|---|---|---|---|---|---|
| 1 | `/timelines/2` | `[2]` | object | {id, category, name, phases} | 3005–4036 |
| 2 | `/timelines/2/id` | `id` | string | hifu-rf | 3011–3020 |
| 3 | `/timelines/2/category` | `category` | string | M9 | 3032–3036 |
| 4 | `/timelines/2/name` | `name` | string | HIFU/RF 리프팅 | 3044–3057 |
| 5 | `/timelines/2/phases` | `phases` | array | [길이 4] | 3067–4035 |
| 6 | `/timelines/2/phases/0` | `[0]` | object | {period, label, normal, abnormal, caution, emergency} | 3068–3322 |
| 7 | `/timelines/2/phases/0/period` | `period` | string | Day 0 | 3078–3085 |
| 8 | `/timelines/2/phases/0/label` | `label` | string | 시술 당일 | 3094–3101 |
| 9 | `/timelines/2/phases/0/normal` | `normal` | array | [길이 4] | 3111–3170 |
| 10 | `/timelines/2/phases/0/normal/0` | `[0]` | string | 홍반/온감 (수시간 내 소실) | 3112–3130 |
| 11 | `/timelines/2/phases/0/normal/1` | `[1]` | string | 시술 부위 따끔거림/화끈감 | 3131–3147 |
| 12 | `/timelines/2/phases/0/normal/2` | `[2]` | string | 경미한 부종 | 3148–3156 |
| 13 | `/timelines/2/phases/0/normal/3` | `[3]` | string | 근육통 유사 불편감 | 3157–3169 |
| 14 | `/timelines/2/phases/0/abnormal` | `abnormal` | array | [길이 2] | 3182–3219 |
| 15 | `/timelines/2/phases/0/abnormal/0` | `[0]` | string | 뚜렷한 부종 (24시간 이상) | 3183–3201 |
| 16 | `/timelines/2/phases/0/abnormal/1` | `[1]` | string | 시술 라인 따라 선형 발적 | 3202–3218 |
| 17 | `/timelines/2/phases/0/caution` | `caution` | array | [길이 2] | 3230–3265 |
| 18 | `/timelines/2/phases/0/caution/0` | `[0]` | string | 수포/물집 형성 | 3231–3241 |
| 19 | `/timelines/2/phases/0/caution/1` | `[1]` | string | 비정상적 심한 통증 (진통제 미반응) | 3242–3264 |
| 20 | `/timelines/2/phases/0/emergency` | `emergency` | array | [길이 2] | 3278–3321 |
| 21 | `/timelines/2/phases/0/emergency/0` | `[0]` | string | 화상/물집 (2도 이상) | 3279–3294 |
| 22 | `/timelines/2/phases/0/emergency/1` | `[1]` | string | 안면 신경 손상 증상 (안면 비대칭/마비) | 3295–3320 |
| 23 | `/timelines/2/phases/1` | `[1]` | object | {period, label, normal, abnormal, caution, emergency} | 3323–3549 |
| 24 | `/timelines/2/phases/1/period` | `period` | string | Day 1-3 | 3333–3342 |
| 25 | `/timelines/2/phases/1/label` | `label` | string | 초기 회복기 | 3351–3359 |
| 26 | `/timelines/2/phases/1/normal` | `normal` | array | [길이 4] | 3369–3420 |
| 27 | `/timelines/2/phases/1/normal/0` | `[0]` | string | 홍반 소실 | 3370–3377 |
| 28 | `/timelines/2/phases/1/normal/1` | `[1]` | string | 시술 부위 압통/뻐근함 | 3378–3392 |
| 29 | `/timelines/2/phases/1/normal/2` | `[2]` | string | 미세한 타이트닝 느낌 시작 | 3393–3409 |
| 30 | `/timelines/2/phases/1/normal/3` | `[3]` | string | 일상생활 가능 | 3410–3419 |
| 31 | `/timelines/2/phases/1/abnormal` | `abnormal` | array | [길이 2] | 3432–3464 |
| 32 | `/timelines/2/phases/1/abnormal/0` | `[0]` | string | 지속 홍반 (3일 이상) | 3433–3448 |
| 33 | `/timelines/2/phases/1/abnormal/1` | `[1]` | string | 경미한 저림/감각 둔화 | 3449–3463 |
| 34 | `/timelines/2/phases/1/caution` | `caution` | array | [길이 2] | 3475–3498 |
| 35 | `/timelines/2/phases/1/caution/0` | `[0]` | string | 물집/수포 악화 | 3476–3486 |
| 36 | `/timelines/2/phases/1/caution/1` | `[1]` | string | 심한 부종 지속 | 3487–3497 |
| 37 | `/timelines/2/phases/1/emergency` | `emergency` | array | [길이 2] | 3511–3548 |
| 38 | `/timelines/2/phases/1/emergency/0` | `[0]` | string | 안면 함몰 징후 (지방위축 시작) | 3512–3532 |
| 39 | `/timelines/2/phases/1/emergency/1` | `[1]` | string | 안면 비대칭/신경 마비 | 3533–3547 |
| 40 | `/timelines/2/phases/2` | `[2]` | object | {period, label, normal, abnormal, caution, emergency} | 3550–3756 |
| 41 | `/timelines/2/phases/2/period` | `period` | string | Day 3-7 | 3560–3569 |
| 42 | `/timelines/2/phases/2/label` | `label` | string | 회복기 | 3578–3583 |
| 43 | `/timelines/2/phases/2/normal` | `normal` | array | [길이 3] | 3593–3633 |
| 44 | `/timelines/2/phases/2/normal/0` | `[0]` | string | 압통 감소 | 3594–3601 |
| 45 | `/timelines/2/phases/2/normal/1` | `[1]` | string | 피부 질감 개선 시작 | 3602–3615 |
| 46 | `/timelines/2/phases/2/normal/2` | `[2]` | string | 저림/감각변화 점차 정상화 | 3616–3632 |
| 47 | `/timelines/2/phases/2/abnormal` | `abnormal` | array | [길이 2] | 3645–3673 |
| 48 | `/timelines/2/phases/2/abnormal/0` | `[0]` | string | 지속적 감각 둔화 | 3646–3657 |
| 49 | `/timelines/2/phases/2/abnormal/1` | `[1]` | string | 불편감 1주 이상 지속 | 3658–3672 |
| 50 | `/timelines/2/phases/2/caution` | `caution` | array | [길이 2] | 3684–3709 |
| 51 | `/timelines/2/phases/2/caution/0` | `[0]` | string | 감각 소실 지속 | 3685–3695 |
| 52 | `/timelines/2/phases/2/caution/1` | `[1]` | string | 비대칭적 부종/경결 | 3696–3708 |
| 53 | `/timelines/2/phases/2/emergency` | `emergency` | array | [길이 2] | 3722–3755 |
| 54 | `/timelines/2/phases/2/emergency/0` | `[0]` | string | 안면 함몰 진행 (지방위축) | 3723–3740 |
| 55 | `/timelines/2/phases/2/emergency/1` | `[1]` | string | 화상 반흔 형성 시작 | 3741–3754 |
| 56 | `/timelines/2/phases/3` | `[3]` | object | {period, label, normal, abnormal, caution, emergency} | 3757–4034 |
| 57 | `/timelines/2/phases/3/period` | `period` | string | Day 7-30 | 3767–3777 |
| 58 | `/timelines/2/phases/3/label` | `label` | string | 콜라겐 리모델링기 | 3786–3797 |
| 59 | `/timelines/2/phases/3/normal` | `normal` | array | [길이 4] | 3807–3882 |
| 60 | `/timelines/2/phases/3/normal/0` | `[0]` | string | 점진적 리프팅 효과 발현 (2-4주) | 3808–3830 |
| 61 | `/timelines/2/phases/3/normal/1` | `[1]` | string | 피부 탄력 개선 체감 | 3831–3844 |
| 62 | `/timelines/2/phases/3/normal/2` | `[2]` | string | 저림/감각변화 완전 소실 (2-4주) | 3845–3867 |
| 63 | `/timelines/2/phases/3/normal/3` | `[3]` | string | 콜라겐 생성 진행 중 | 3868–3881 |
| 64 | `/timelines/2/phases/3/abnormal` | `abnormal` | array | [길이 2] | 3894–3931 |
| 65 | `/timelines/2/phases/3/abnormal/0` | `[0]` | string | 효과 미미 (추가 시술 고려 시점) | 3895–3916 |
| 66 | `/timelines/2/phases/3/abnormal/1` | `[1]` | string | 일부 감각 변화 잔존 | 3917–3930 |
| 67 | `/timelines/2/phases/3/caution` | `caution` | array | [길이 2] | 3942–3968 |
| 68 | `/timelines/2/phases/3/caution/0` | `[0]` | string | 안면 비대칭 지속 | 3943–3954 |
| 69 | `/timelines/2/phases/3/caution/1` | `[1]` | string | 불규칙한 피부 표면 | 3955–3967 |
| 70 | `/timelines/2/phases/3/emergency` | `emergency` | array | [길이 2] | 3981–4033 |
| 71 | `/timelines/2/phases/3/emergency/0` | `[0]` | string | 진행성 안면 함몰 (지방위축 -- HIFU 심부 에너지 과다 시) | 3982–4020 |
| 72 | `/timelines/2/phases/3/emergency/1` | `[1]` | string | 지연성 신경 손상 | 4021–4032 |

## 2. 원문 — 기간별 보기 (같은 값, 원본 컬럼명 그대로)

`id` = hifu-rf · `category` = M9 · `name` = HIFU/RF 리프팅

### phases/0 — `period` = Day 0 · `label` = 시술 당일

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 홍반/온감 (수시간 내 소실) | `/timelines/2/phases/0/normal/0` |
| `normal` | 1 | 시술 부위 따끔거림/화끈감 | `/timelines/2/phases/0/normal/1` |
| `normal` | 2 | 경미한 부종 | `/timelines/2/phases/0/normal/2` |
| `normal` | 3 | 근육통 유사 불편감 | `/timelines/2/phases/0/normal/3` |
| `abnormal` | 0 | 뚜렷한 부종 (24시간 이상) | `/timelines/2/phases/0/abnormal/0` |
| `abnormal` | 1 | 시술 라인 따라 선형 발적 | `/timelines/2/phases/0/abnormal/1` |
| `caution` | 0 | 수포/물집 형성 | `/timelines/2/phases/0/caution/0` |
| `caution` | 1 | 비정상적 심한 통증 (진통제 미반응) | `/timelines/2/phases/0/caution/1` |
| `emergency` | 0 | 화상/물집 (2도 이상) | `/timelines/2/phases/0/emergency/0` |
| `emergency` | 1 | 안면 신경 손상 증상 (안면 비대칭/마비) | `/timelines/2/phases/0/emergency/1` |

### phases/1 — `period` = Day 1-3 · `label` = 초기 회복기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 홍반 소실 | `/timelines/2/phases/1/normal/0` |
| `normal` | 1 | 시술 부위 압통/뻐근함 | `/timelines/2/phases/1/normal/1` |
| `normal` | 2 | 미세한 타이트닝 느낌 시작 | `/timelines/2/phases/1/normal/2` |
| `normal` | 3 | 일상생활 가능 | `/timelines/2/phases/1/normal/3` |
| `abnormal` | 0 | 지속 홍반 (3일 이상) | `/timelines/2/phases/1/abnormal/0` |
| `abnormal` | 1 | 경미한 저림/감각 둔화 | `/timelines/2/phases/1/abnormal/1` |
| `caution` | 0 | 물집/수포 악화 | `/timelines/2/phases/1/caution/0` |
| `caution` | 1 | 심한 부종 지속 | `/timelines/2/phases/1/caution/1` |
| `emergency` | 0 | 안면 함몰 징후 (지방위축 시작) | `/timelines/2/phases/1/emergency/0` |
| `emergency` | 1 | 안면 비대칭/신경 마비 | `/timelines/2/phases/1/emergency/1` |

### phases/2 — `period` = Day 3-7 · `label` = 회복기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 압통 감소 | `/timelines/2/phases/2/normal/0` |
| `normal` | 1 | 피부 질감 개선 시작 | `/timelines/2/phases/2/normal/1` |
| `normal` | 2 | 저림/감각변화 점차 정상화 | `/timelines/2/phases/2/normal/2` |
| `abnormal` | 0 | 지속적 감각 둔화 | `/timelines/2/phases/2/abnormal/0` |
| `abnormal` | 1 | 불편감 1주 이상 지속 | `/timelines/2/phases/2/abnormal/1` |
| `caution` | 0 | 감각 소실 지속 | `/timelines/2/phases/2/caution/0` |
| `caution` | 1 | 비대칭적 부종/경결 | `/timelines/2/phases/2/caution/1` |
| `emergency` | 0 | 안면 함몰 진행 (지방위축) | `/timelines/2/phases/2/emergency/0` |
| `emergency` | 1 | 화상 반흔 형성 시작 | `/timelines/2/phases/2/emergency/1` |

### phases/3 — `period` = Day 7-30 · `label` = 콜라겐 리모델링기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 점진적 리프팅 효과 발현 (2-4주) | `/timelines/2/phases/3/normal/0` |
| `normal` | 1 | 피부 탄력 개선 체감 | `/timelines/2/phases/3/normal/1` |
| `normal` | 2 | 저림/감각변화 완전 소실 (2-4주) | `/timelines/2/phases/3/normal/2` |
| `normal` | 3 | 콜라겐 생성 진행 중 | `/timelines/2/phases/3/normal/3` |
| `abnormal` | 0 | 효과 미미 (추가 시술 고려 시점) | `/timelines/2/phases/3/abnormal/0` |
| `abnormal` | 1 | 일부 감각 변화 잔존 | `/timelines/2/phases/3/abnormal/1` |
| `caution` | 0 | 안면 비대칭 지속 | `/timelines/2/phases/3/caution/0` |
| `caution` | 1 | 불규칙한 피부 표면 | `/timelines/2/phases/3/caution/1` |
| `emergency` | 0 | 진행성 안면 함몰 (지방위축 -- HIFU 심부 에너지 과다 시) | `/timelines/2/phases/3/emergency/0` |
| `emergency` | 1 | 지연성 신경 손상 | `/timelines/2/phases/3/emergency/1` |

## 3. 수동 표현 (직접 읽기) — 원문 구절과 관찰 칸 분리

| Pointer | 구간 | 원문 구절 | 탐색 관점(잠정) | 잠정 메모 |
|---|---|---|---|---|
| `/timelines/2/id` | [0,7) | hifu-rf | id_code | |  |
| `/timelines/2/category` | [0,2) | M9 | id_code | |  |
| `/timelines/2/name` | [0,11) | HIFU/RF 리프팅 | procedure_name, alt, mixed_script | 「/」 대안(README 규칙상 둘 중 하나). 한 타임라인이 두 계열을 함께 다룸 |
| `/timelines/2/phases/0/period` | [0,5) | Day 0 | period | |  |
| `/timelines/2/phases/0/label` | [0,5) | 시술 당일 | reference_point | |  |
| `/timelines/2/phases/0/normal/0` | [0,16) | 홍반/온감 (수시간 내 소실) | alt, resolution, approx_time | |  |
| `/timelines/2/phases/0/normal/1` | [0,14) | 시술 부위 따끔거림/화끈감 | site, alt | |  |
| `/timelines/2/phases/0/normal/2` | [0,6) | 경미한 부종 | severity | |  |
| `/timelines/2/phases/0/normal/3` | [0,10) | 근육통 유사 불편감 | similarity | 「유사」 비유 |
| `/timelines/2/phases/0/abnormal/0` | [0,16) | 뚜렷한 부종 (24시간 이상) | degree, duration_threshold | 24시간 이상이 지속 시간이라는 것은 잠정. 「지속」 말이 없음 |
| `/timelines/2/phases/0/abnormal/1` | [0,14) | 시술 라인 따라 선형 발적 | site, pattern | 「시술 라인」 = 시술 경로(잠정) |
| `/timelines/2/phases/0/caution/0` | [0,8) | 수포/물집 형성 | alt, synonym_pair | 수포와 물집은 같은 뜻 병기로 보임(잠정) |
| `/timelines/2/phases/0/caution/1` | [0,20) | 비정상적 심한 통증 (진통제 미반응) | degree, severity, negation | |  |
| `/timelines/2/phases/0/emergency/0` | [0,13) | 화상/물집 (2도 이상) | alt, grade_threshold | 「2도」 = 화상 등급(잠정). 체온 「도」 와 다름 |
| `/timelines/2/phases/0/emergency/1` | [0,23) | 안면 신경 손상 증상 (안면 비대칭/마비) | site, gloss, alt | |  |
| `/timelines/2/phases/1/period` | [0,7) | Day 1-3 | period, time_range | |  |
| `/timelines/2/phases/1/label` | [0,6) | 초기 회복기 | phase_label | |  |
| `/timelines/2/phases/1/normal/0` | [0,5) | 홍반 소실 | resolution | |  |
| `/timelines/2/phases/1/normal/1` | [0,12) | 시술 부위 압통/뻐근함 | site, alt | |  |
| `/timelines/2/phases/1/normal/2` | [0,14) | 미세한 타이트닝 느낌 시작 | degree, subjective, onset, loanword | |  |
| `/timelines/2/phases/1/normal/3` | [0,7) | 일상생활 가능 | possibility, activity | 활동 재개 가능 |
| `/timelines/2/phases/1/abnormal/0` | [0,13) | 지속 홍반 (3일 이상) | persistence, duration_threshold | |  |
| `/timelines/2/phases/1/abnormal/1` | [0,12) | 경미한 저림/감각 둔화 | severity, alt | |  |
| `/timelines/2/phases/1/caution/0` | [0,8) | 물집/수포 악화 | alt, worsening | |  |
| `/timelines/2/phases/1/caution/1` | [0,8) | 심한 부종 지속 | severity, persistence | |  |
| `/timelines/2/phases/1/emergency/0` | [0,18) | 안면 함몰 징후 (지방위축 시작) | site, early_sign, onset | |  |
| `/timelines/2/phases/1/emergency/1` | [0,12) | 안면 비대칭/신경 마비 | site, alt | |  |
| `/timelines/2/phases/2/period` | [0,7) | Day 3-7 | period, time_range | |  |
| `/timelines/2/phases/2/label` | [0,3) | 회복기 | phase_label | |  |
| `/timelines/2/phases/2/normal/0` | [0,5) | 압통 감소 | change | |  |
| `/timelines/2/phases/2/normal/1` | [0,11) | 피부 질감 개선 시작 | onset, change | |  |
| `/timelines/2/phases/2/normal/2` | [0,14) | 저림/감각변화 점차 정상화 | alt, speed, recovery | |  |
| `/timelines/2/phases/2/abnormal/0` | [0,9) | 지속적 감각 둔화 | persistence | |  |
| `/timelines/2/phases/2/abnormal/1` | [0,12) | 불편감 1주 이상 지속 | duration_threshold, persistence | 「1주」 단위. 기간 Day 3-7 안의 값이 1주 이상 지속을 말함 |
| `/timelines/2/phases/2/caution/0` | [0,8) | 감각 소실 지속 | persistence | |  |
| `/timelines/2/phases/2/caution/1` | [0,10) | 비대칭적 부종/경결 | asymmetry, alt | |  |
| `/timelines/2/phases/2/emergency/0` | [0,15) | 안면 함몰 진행 (지방위축) | site, progress, cause_label | |  |
| `/timelines/2/phases/2/emergency/1` | [0,11) | 화상 반흔 형성 시작 | onset, formation | |  |
| `/timelines/2/phases/3/period` | [0,8) | Day 7-30 | period, time_range | |  |
| `/timelines/2/phases/3/label` | [0,9) | 콜라겐 리모델링기 | phase_label, mechanism | |  |
| `/timelines/2/phases/3/normal/0` | [0,20) | 점진적 리프팅 효과 발현 (2-4주) | speed, onset, time_range | 「2-4주」 는 효과 발현 시기. 기간(Day 7-30)과 단위가 다름 |
| `/timelines/2/phases/3/normal/1` | [0,11) | 피부 탄력 개선 체감 | subjective, change | |  |
| `/timelines/2/phases/3/normal/2` | [0,20) | 저림/감각변화 완전 소실 (2-4주) | alt, degree, resolution, time_range | 「완전」. 같은 「2-4주」 가 소실 시점으로 쓰임 |
| `/timelines/2/phases/3/normal/3` | [0,11) | 콜라겐 생성 진행 중 | mechanism, progress | |  |
| `/timelines/2/phases/3/abnormal/0` | [0,19) | 효과 미미 (추가 시술 고려 시점) | insufficiency, recommendation, retreatment_decision | |  |
| `/timelines/2/phases/3/abnormal/1` | [0,11) | 일부 감각 변화 잔존 | proportion_approx, persistence | 「일부」 |
| `/timelines/2/phases/3/caution/0` | [0,9) | 안면 비대칭 지속 | site, persistence | |  |
| `/timelines/2/phases/3/caution/1` | [0,10) | 불규칙한 피부 표면 | texture | |  |
| `/timelines/2/phases/3/emergency/0` | [0,36) | 진행성 안면 함몰 (지방위축 -- HIFU 심부 에너지 과다 시) | progress, cause, condition, depth, procedure_ref | 「HIFU」 만 지목 — 이름의 HIFU/RF 중 하나에만 해당(잠정). 「심부」 깊이, 「과다 시」 조건 |
| `/timelines/2/phases/3/emergency/1` | [0,9) | 지연성 신경 손상 | delayed_onset | |  |

## 4. 자동 후보 요약 (정규식 일치분만 — 전수 의미 수집 아님)

P-AFTER 1, P-ALT 13, P-APPROX 1, P-APPROXTIME 1, P-COMPARE 4, P-COND-SI 1, P-COURSE 26, P-DAY 4, P-DEGREE 9, P-DEPTH 1, P-DURING 2, P-IF 7, P-LATIN 7, P-NEG 2, P-NUMUNIT 6, P-PAREN 12, P-POSSIB 2, P-SITE 9, P-SPEED 2, P-SYMBOL 1

전체 목록은 expressions.json (segment 필터).

## 5. 잠정 관찰

- **S03-O1** 타임라인 이름이 「HIFU/RF 리프팅」 으로 두 계열을 한 줄에 묶었다. phases/3/emergency/0 만 「HIFU 심부 에너지 과다 시」 로 한쪽을 지목한다. 나머지 값이 둘 다에 해당하는지는 원문에 없다.
- **S03-O2** 기간 4개(Day 0 / 1-3 / 3-7 / 7-30). 마지막 기간 안의 값은 주 단위(2-4주, 1주 이상)를 쓴다.
- **S03-O3** 「도」 가 화상 등급(2도)으로 쓰였다. ha-filler 의 체온(37.5도)과 같은 글자이며 다른 대상이다(잠정).

## 6. 미결 (이 구획)

| ID | 분류 | 위치 | 내용 |
|---|---|---|---|
| S03-Q1 | B | `/timelines/2/name` `/timelines/2/phases/*/*` | HIFU 와 RF 중 어느 쪽에 해당하는 반응인지 phases/3/emergency/0 외에는 원문에 없다. |
| S03-Q2 | P | `/timelines/2/phases/0/abnormal/0` | 「(24시간 이상)」 이 부종 지속 시간인지 원문 표현이 생략돼 있다. |

## 7. 형태소 — 알려진 오분절 (교정 안 함)

| Pointer | 구간 | 원시 토큰 | 판정/설명 | 영향 |
|---|---|---|---|---|
| `/timelines/2/phases/0/abnormal/1` | [12,14) | 발/NNG + 적/XSN | K-BALJEOK 「발적」 이 발/NNG+적/XSN 으로 분할 | 사건 명사 손실(「-적」 접미 오인) |
| `/timelines/2/phases/1/normal/1` | [6,8) | 압/NNG + 통/NNG | K-APTONG 「압통」 이 압+통 으로 분할 | 사건 명사 손실 |
| `/timelines/2/phases/1/abnormal/0` | [0,2) | 지/NP + 속/NNG | K-JISOK 「지속」 이 지/NP+속/NNG 로 분할 | 지속(경과) 단서 손실 |

