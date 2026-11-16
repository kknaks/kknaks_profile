# S06 — /timelines/5 dca-injection (DCA 지방분해 주사)

> build.py 생성. 원문 값과 잠정 관찰은 서로 다른 절·칸에 둔다.

- 소유 범위: prefix ['/timelines/5'] · exact []
- 공유 문맥(소유 아님): ['', '/timelines', '/consensus_method', '/reaction_levels', '/reaction_levels/normal', '/reaction_levels/abnormal', '/reaction_levels/caution', '/reaction_levels/emergency']
- 직접 읽기: done (manual/S06.txt) · 마지막 읽은 Pointer `/timelines/5/phases/4/emergency/0`

## 1. 원문 — 모든 노드 (문서 순서)

| # | Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 원문 구간(cp) |
|---|---|---|---|---|---|
| 1 | `/timelines/5` | `[5]` | object | {id, category, name, phases} | 6687–8099 |
| 2 | `/timelines/5/id` | `id` | string | dca-injection | 6693–6708 |
| 3 | `/timelines/5/category` | `category` | string | M16-DCA | 6720–6729 |
| 4 | `/timelines/5/name` | `name` | string | DCA 지방분해 주사 | 6737–6750 |
| 5 | `/timelines/5/phases` | `phases` | array | [길이 5] | 6760–8098 |
| 6 | `/timelines/5/phases/0` | `[0]` | object | {period, label, normal, abnormal, caution, emergency} | 6761–7034 |
| 7 | `/timelines/5/phases/0/period` | `period` | string | Day 0 | 6771–6778 |
| 8 | `/timelines/5/phases/0/label` | `label` | string | 시술 당일 | 6787–6794 |
| 9 | `/timelines/5/phases/0/normal` | `normal` | array | [길이 4] | 6804–6876 |
| 10 | `/timelines/5/phases/0/normal/0` | `[0]` | string | 주사 부위 강한 작열감/통증 (시술 중~직후) | 6805–6832 |
| 11 | `/timelines/5/phases/0/normal/1` | `[1]` | string | 즉각적 부종 시작 | 6833–6844 |
| 12 | `/timelines/5/phases/0/normal/2` | `[2]` | string | 주사 부위 발적/열감 | 6845–6858 |
| 13 | `/timelines/5/phases/0/normal/3` | `[3]` | string | 감각 이상 (저림/무감각) | 6859–6875 |
| 14 | `/timelines/5/phases/0/abnormal` | `abnormal` | array | [길이 2] | 6888–6908 |
| 15 | `/timelines/5/phases/0/abnormal/0` | `[0]` | string | 예상보다 광범위한 부종 | 6889–6903 |
| 16 | `/timelines/5/phases/0/abnormal/1` | `[1]` | string | 멍 | 6904–6907 |
| 17 | `/timelines/5/phases/0/caution` | `caution` | array | [길이 2] | 6919–6960 |
| 18 | `/timelines/5/phases/0/caution/0` | `[0]` | string | 비정상적 심한 통증 (수시간 지속) | 6920–6941 |
| 19 | `/timelines/5/phases/0/caution/1` | `[1]` | string | 피부색 변화 (창백/검은색) | 6942–6959 |
| 20 | `/timelines/5/phases/0/emergency` | `emergency` | array | [길이 3] | 6973–7033 |
| 21 | `/timelines/5/phases/0/emergency/0` | `[0]` | string | 아나필락시스 | 6974–6982 |
| 22 | `/timelines/5/phases/0/emergency/1` | `[1]` | string | 피부 괴사 초기 징후 (검은 반점) | 6983–7004 |
| 23 | `/timelines/5/phases/0/emergency/2` | `[2]` | string | 하악변연신경 손상 (비대칭 미소/입꼬리 처짐) | 7005–7032 |
| 24 | `/timelines/5/phases/1` | `[1]` | object | {period, label, normal, abnormal, caution, emergency} | 7035–7336 |
| 25 | `/timelines/5/phases/1/period` | `period` | string | Day 1-3 | 7045–7054 |
| 26 | `/timelines/5/phases/1/label` | `label` | string | 부종 피크기 | 7063–7071 |
| 27 | `/timelines/5/phases/1/normal` | `normal` | array | [길이 4] | 7081–7168 |
| 28 | `/timelines/5/phases/1/normal/0` | `[0]` | string | 부종 심화 (거의 필발, 이중턱보다 부을 수 있음) | 7082–7112 |
| 29 | `/timelines/5/phases/1/normal/1` | `[1]` | string | 경결감 (딱딱한 느낌) | 7113–7127 |
| 30 | `/timelines/5/phases/1/normal/2` | `[2]` | string | 통증 지속 (진통제 복용 가능) | 7128–7147 |
| 31 | `/timelines/5/phases/1/normal/3` | `[3]` | string | 감각 이상 지속 (저림/무감각) | 7148–7167 |
| 32 | `/timelines/5/phases/1/abnormal` | `abnormal` | array | [길이 2] | 7180–7200 |
| 33 | `/timelines/5/phases/1/abnormal/0` | `[0]` | string | 광범위 멍 | 7181–7188 |
| 34 | `/timelines/5/phases/1/abnormal/1` | `[1]` | string | 연하 시 불편감 | 7189–7199 |
| 35 | `/timelines/5/phases/1/caution` | `caution` | array | [길이 3] | 7211–7255 |
| 36 | `/timelines/5/phases/1/caution/0` | `[0]` | string | 부종이 목/가슴으로 확대 | 7212–7227 |
| 37 | `/timelines/5/phases/1/caution/1` | `[1]` | string | 발열 (37.5도 이상) | 7228–7243 |
| 38 | `/timelines/5/phases/1/caution/2` | `[2]` | string | 피부 변색 악화 | 7244–7254 |
| 39 | `/timelines/5/phases/1/emergency` | `emergency` | array | [길이 3] | 7268–7335 |
| 40 | `/timelines/5/phases/1/emergency/0` | `[0]` | string | 피부 괴사 진행 (검은색 변색 확대) | 7269–7291 |
| 41 | `/timelines/5/phases/1/emergency/1` | `[1]` | string | 하악변연신경 손상 (비대칭 미소 지속) | 7292–7315 |
| 42 | `/timelines/5/phases/1/emergency/2` | `[2]` | string | 호흡 곤란 (기도 주변 부종) | 7316–7334 |
| 43 | `/timelines/5/phases/2` | `[2]` | object | {period, label, normal, abnormal, caution, emergency} | 7337–7560 |
| 44 | `/timelines/5/phases/2/period` | `period` | string | Day 3-7 | 7347–7356 |
| 45 | `/timelines/5/phases/2/label` | `label` | string | 회복 시작기 | 7365–7373 |
| 46 | `/timelines/5/phases/2/normal` | `normal` | array | [길이 4] | 7383–7447 |
| 47 | `/timelines/5/phases/2/normal/0` | `[0]` | string | 부종 서서히 감소 시작 | 7384–7398 |
| 48 | `/timelines/5/phases/2/normal/1` | `[1]` | string | 경결감 지속 (정상) | 7399–7412 |
| 49 | `/timelines/5/phases/2/normal/2` | `[2]` | string | 통증 완화 | 7413–7420 |
| 50 | `/timelines/5/phases/2/normal/3` | `[3]` | string | 감각 이상 지속 가능 (정상, 수주 소요) | 7421–7446 |
| 51 | `/timelines/5/phases/2/abnormal` | `abnormal` | array | [길이 2] | 7459–7482 |
| 52 | `/timelines/5/phases/2/abnormal/0` | `[0]` | string | 부종 감소 없음 | 7460–7470 |
| 53 | `/timelines/5/phases/2/abnormal/1` | `[1]` | string | 경결 부위 커짐 | 7471–7481 |
| 54 | `/timelines/5/phases/2/caution` | `caution` | array | [길이 2] | 7493–7529 |
| 55 | `/timelines/5/phases/2/caution/0` | `[0]` | string | 감염 징후 (발적 + 열감 + 농) | 7494–7515 |
| 56 | `/timelines/5/phases/2/caution/1` | `[1]` | string | 피부 울퉁불퉁 심화 | 7516–7528 |
| 57 | `/timelines/5/phases/2/emergency` | `emergency` | array | [길이 2] | 7542–7559 |
| 58 | `/timelines/5/phases/2/emergency/0` | `[0]` | string | 피부 괴사 | 7543–7550 |
| 59 | `/timelines/5/phases/2/emergency/1` | `[1]` | string | 농양 형성 | 7551–7558 |
| 60 | `/timelines/5/phases/3` | `[3]` | object | {period, label, normal, abnormal, caution, emergency} | 7561–7879 |
| 61 | `/timelines/5/phases/3/period` | `period` | string | Day 7-14 | 7571–7581 |
| 62 | `/timelines/5/phases/3/label` | `label` | string | 회복기 | 7590–7595 |
| 63 | `/timelines/5/phases/3/normal` | `normal` | array | [길이 4] | 7605–7666 |
| 64 | `/timelines/5/phases/3/normal/0` | `[0]` | string | 부종 상당 부분 소실 | 7606–7619 |
| 65 | `/timelines/5/phases/3/normal/1` | `[1]` | string | 경결감 점차 감소 | 7620–7631 |
| 66 | `/timelines/5/phases/3/normal/2` | `[2]` | string | 감각 정상화 시작 | 7632–7643 |
| 67 | `/timelines/5/phases/3/normal/3` | `[3]` | string | 지방 분해 효과 아직 미미 (정상) | 7644–7665 |
| 68 | `/timelines/5/phases/3/abnormal` | `abnormal` | array | [길이 2] | 7678–7786 |
| 69 | `/timelines/5/phases/3/abnormal/0` | `[0]` | string | 지속적 경결 (대개 정상 염증반응으로 수 주 내 자연 소실 — 데옥시콜산은 임의 마사지가 표적외 확산·신경손상·괴사 위험이 있어 금기. 지속·악화 시 시술 병원 문의) | 7679–7774 |
| 70 | `/timelines/5/phases/3/abnormal/1` | `[1]` | string | 감각 이상 지속 | 7775–7785 |
| 71 | `/timelines/5/phases/3/caution` | `caution` | array | [길이 2] | 7797–7819 |
| 72 | `/timelines/5/phases/3/caution/0` | `[0]` | string | 비대칭 경결/울퉁 | 7798–7809 |
| 73 | `/timelines/5/phases/3/caution/1` | `[1]` | string | 지연성 감염 | 7810–7818 |
| 74 | `/timelines/5/phases/3/emergency` | `emergency` | array | [길이 2] | 7832–7878 |
| 75 | `/timelines/5/phases/3/emergency/0` | `[0]` | string | 하악변연신경 손상 지속 (4주 이상 시 영구 손상 우려) | 7833–7866 |
| 76 | `/timelines/5/phases/3/emergency/1` | `[1]` | string | 피부 괴사/궤양 | 7867–7877 |
| 77 | `/timelines/5/phases/4` | `[4]` | object | {period, label, normal, abnormal, caution, emergency} | 7880–8097 |
| 78 | `/timelines/5/phases/4/period` | `period` | string | Day 14-30 | 7890–7901 |
| 79 | `/timelines/5/phases/4/label` | `label` | string | 효과 발현기 | 7910–7918 |
| 80 | `/timelines/5/phases/4/normal` | `normal` | array | [길이 4] | 7928–7982 |
| 81 | `/timelines/5/phases/4/normal/0` | `[0]` | string | 지방 분해 효과 서서히 발현 | 7929–7946 |
| 82 | `/timelines/5/phases/4/normal/1` | `[1]` | string | 턱선 개선 시작 | 7947–7957 |
| 83 | `/timelines/5/phases/4/normal/2` | `[2]` | string | 경결감 소실 | 7958–7966 |
| 84 | `/timelines/5/phases/4/normal/3` | `[3]` | string | 감각 정상화 (대부분) | 7967–7981 |
| 85 | `/timelines/5/phases/4/abnormal` | `abnormal` | array | [길이 2] | 7994–8025 |
| 86 | `/timelines/5/phases/4/abnormal/0` | `[0]` | string | 효과 미미 (추가 세션 필요 가능) | 7995–8016 |
| 87 | `/timelines/5/phases/4/abnormal/1` | `[1]` | string | 잔여 경결 | 8017–8024 |
| 88 | `/timelines/5/phases/4/caution` | `caution` | array | [길이 2] | 8036–8068 |
| 89 | `/timelines/5/phases/4/caution/0` | `[0]` | string | 비대칭 지방 분해 | 8037–8048 |
| 90 | `/timelines/5/phases/4/caution/1` | `[1]` | string | 만성 감각 이상 (6주 이상) | 8049–8067 |
| 91 | `/timelines/5/phases/4/emergency` | `emergency` | array | [길이 1] | 8081–8096 |
| 92 | `/timelines/5/phases/4/emergency/0` | `[0]` | string | 영구 신경 손상 징후 | 8082–8095 |

## 2. 원문 — 기간별 보기 (같은 값, 원본 컬럼명 그대로)

`id` = dca-injection · `category` = M16-DCA · `name` = DCA 지방분해 주사

### phases/0 — `period` = Day 0 · `label` = 시술 당일

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 주사 부위 강한 작열감/통증 (시술 중~직후) | `/timelines/5/phases/0/normal/0` |
| `normal` | 1 | 즉각적 부종 시작 | `/timelines/5/phases/0/normal/1` |
| `normal` | 2 | 주사 부위 발적/열감 | `/timelines/5/phases/0/normal/2` |
| `normal` | 3 | 감각 이상 (저림/무감각) | `/timelines/5/phases/0/normal/3` |
| `abnormal` | 0 | 예상보다 광범위한 부종 | `/timelines/5/phases/0/abnormal/0` |
| `abnormal` | 1 | 멍 | `/timelines/5/phases/0/abnormal/1` |
| `caution` | 0 | 비정상적 심한 통증 (수시간 지속) | `/timelines/5/phases/0/caution/0` |
| `caution` | 1 | 피부색 변화 (창백/검은색) | `/timelines/5/phases/0/caution/1` |
| `emergency` | 0 | 아나필락시스 | `/timelines/5/phases/0/emergency/0` |
| `emergency` | 1 | 피부 괴사 초기 징후 (검은 반점) | `/timelines/5/phases/0/emergency/1` |
| `emergency` | 2 | 하악변연신경 손상 (비대칭 미소/입꼬리 처짐) | `/timelines/5/phases/0/emergency/2` |

### phases/1 — `period` = Day 1-3 · `label` = 부종 피크기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 부종 심화 (거의 필발, 이중턱보다 부을 수 있음) | `/timelines/5/phases/1/normal/0` |
| `normal` | 1 | 경결감 (딱딱한 느낌) | `/timelines/5/phases/1/normal/1` |
| `normal` | 2 | 통증 지속 (진통제 복용 가능) | `/timelines/5/phases/1/normal/2` |
| `normal` | 3 | 감각 이상 지속 (저림/무감각) | `/timelines/5/phases/1/normal/3` |
| `abnormal` | 0 | 광범위 멍 | `/timelines/5/phases/1/abnormal/0` |
| `abnormal` | 1 | 연하 시 불편감 | `/timelines/5/phases/1/abnormal/1` |
| `caution` | 0 | 부종이 목/가슴으로 확대 | `/timelines/5/phases/1/caution/0` |
| `caution` | 1 | 발열 (37.5도 이상) | `/timelines/5/phases/1/caution/1` |
| `caution` | 2 | 피부 변색 악화 | `/timelines/5/phases/1/caution/2` |
| `emergency` | 0 | 피부 괴사 진행 (검은색 변색 확대) | `/timelines/5/phases/1/emergency/0` |
| `emergency` | 1 | 하악변연신경 손상 (비대칭 미소 지속) | `/timelines/5/phases/1/emergency/1` |
| `emergency` | 2 | 호흡 곤란 (기도 주변 부종) | `/timelines/5/phases/1/emergency/2` |

### phases/2 — `period` = Day 3-7 · `label` = 회복 시작기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 부종 서서히 감소 시작 | `/timelines/5/phases/2/normal/0` |
| `normal` | 1 | 경결감 지속 (정상) | `/timelines/5/phases/2/normal/1` |
| `normal` | 2 | 통증 완화 | `/timelines/5/phases/2/normal/2` |
| `normal` | 3 | 감각 이상 지속 가능 (정상, 수주 소요) | `/timelines/5/phases/2/normal/3` |
| `abnormal` | 0 | 부종 감소 없음 | `/timelines/5/phases/2/abnormal/0` |
| `abnormal` | 1 | 경결 부위 커짐 | `/timelines/5/phases/2/abnormal/1` |
| `caution` | 0 | 감염 징후 (발적 + 열감 + 농) | `/timelines/5/phases/2/caution/0` |
| `caution` | 1 | 피부 울퉁불퉁 심화 | `/timelines/5/phases/2/caution/1` |
| `emergency` | 0 | 피부 괴사 | `/timelines/5/phases/2/emergency/0` |
| `emergency` | 1 | 농양 형성 | `/timelines/5/phases/2/emergency/1` |

### phases/3 — `period` = Day 7-14 · `label` = 회복기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 부종 상당 부분 소실 | `/timelines/5/phases/3/normal/0` |
| `normal` | 1 | 경결감 점차 감소 | `/timelines/5/phases/3/normal/1` |
| `normal` | 2 | 감각 정상화 시작 | `/timelines/5/phases/3/normal/2` |
| `normal` | 3 | 지방 분해 효과 아직 미미 (정상) | `/timelines/5/phases/3/normal/3` |
| `abnormal` | 0 | 지속적 경결 (대개 정상 염증반응으로 수 주 내 자연 소실 — 데옥시콜산은 임의 마사지가 표적외 확산·신경손상·괴사 위험이 있어 금기. 지속·악화 시 시술 병원 문의) | `/timelines/5/phases/3/abnormal/0` |
| `abnormal` | 1 | 감각 이상 지속 | `/timelines/5/phases/3/abnormal/1` |
| `caution` | 0 | 비대칭 경결/울퉁 | `/timelines/5/phases/3/caution/0` |
| `caution` | 1 | 지연성 감염 | `/timelines/5/phases/3/caution/1` |
| `emergency` | 0 | 하악변연신경 손상 지속 (4주 이상 시 영구 손상 우려) | `/timelines/5/phases/3/emergency/0` |
| `emergency` | 1 | 피부 괴사/궤양 | `/timelines/5/phases/3/emergency/1` |

### phases/4 — `period` = Day 14-30 · `label` = 효과 발현기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 지방 분해 효과 서서히 발현 | `/timelines/5/phases/4/normal/0` |
| `normal` | 1 | 턱선 개선 시작 | `/timelines/5/phases/4/normal/1` |
| `normal` | 2 | 경결감 소실 | `/timelines/5/phases/4/normal/2` |
| `normal` | 3 | 감각 정상화 (대부분) | `/timelines/5/phases/4/normal/3` |
| `abnormal` | 0 | 효과 미미 (추가 세션 필요 가능) | `/timelines/5/phases/4/abnormal/0` |
| `abnormal` | 1 | 잔여 경결 | `/timelines/5/phases/4/abnormal/1` |
| `caution` | 0 | 비대칭 지방 분해 | `/timelines/5/phases/4/caution/0` |
| `caution` | 1 | 만성 감각 이상 (6주 이상) | `/timelines/5/phases/4/caution/1` |
| `emergency` | 0 | 영구 신경 손상 징후 | `/timelines/5/phases/4/emergency/0` |

## 3. 수동 표현 (직접 읽기) — 원문 구절과 관찰 칸 분리

| Pointer | 구간 | 원문 구절 | 탐색 관점(잠정) | 잠정 메모 |
|---|---|---|---|---|
| `/timelines/5/id` | [0,13) | dca-injection | id_code | |  |
| `/timelines/5/category` | [0,7) | M16-DCA | id_code | 다른 시술은 M+숫자, 이 값만 「-DCA」 접미 |
| `/timelines/5/name` | [0,11) | DCA 지방분해 주사 | procedure_name, mixed_script | |  |
| `/timelines/5/phases/0/period` | [0,5) | Day 0 | period | |  |
| `/timelines/5/phases/0/label` | [0,5) | 시술 당일 | reference_point | |  |
| `/timelines/5/phases/0/normal/0` | [0,15) | 주사 부위 강한 작열감/통증 | site, degree, alt | |  |
| `/timelines/5/phases/0/normal/0` | [16,25) | (시술 중~직후) | time_range, reference_point | 「~」 범위. 시술 중부터 직후까지 |
| `/timelines/5/phases/0/normal/1` | [0,9) | 즉각적 부종 시작 | onset_speed, onset | |  |
| `/timelines/5/phases/0/normal/2` | [0,11) | 주사 부위 발적/열감 | site, alt | |  |
| `/timelines/5/phases/0/normal/3` | [0,14) | 감각 이상 (저림/무감각) | gloss, alt, negation | 「무」 접두 부정 |
| `/timelines/5/phases/0/abnormal/0` | [0,12) | 예상보다 광범위한 부종 | comparison, extent | |  |
| `/timelines/5/phases/0/abnormal/1` | [0,1) | 멍 | event | 수식 없는 단독 값 |
| `/timelines/5/phases/0/caution/0` | [0,19) | 비정상적 심한 통증 (수시간 지속) | degree, severity, duration, approx_time | |  |
| `/timelines/5/phases/0/caution/1` | [0,15) | 피부색 변화 (창백/검은색) | color_change, alt | |  |
| `/timelines/5/phases/0/emergency/0` | [0,6) | 아나필락시스 | label | 수식 없는 단독 값 |
| `/timelines/5/phases/0/emergency/1` | [0,19) | 피부 괴사 초기 징후 (검은 반점) | early_sign, color | |  |
| `/timelines/5/phases/0/emergency/2` | [0,25) | 하악변연신경 손상 (비대칭 미소/입꼬리 처짐) | anatomy, gloss, alt | 전문어 「하악변연신경」 오분절 주의 |
| `/timelines/5/phases/1/period` | [0,7) | Day 1-3 | period, time_range | |  |
| `/timelines/5/phases/1/label` | [0,6) | 부종 피크기 | phase_label, peak | |  |
| `/timelines/5/phases/1/normal/0` | [0,28) | 부종 심화 (거의 필발, 이중턱보다 부을 수 있음) | worsening, approx, comparison, possibility | 「거의 필발」 의 뜻이 원문으로 불분명(오기 여부 미상, 해석하지 않음) |
| `/timelines/5/phases/1/normal/0` | [14,27) | 이중턱보다 부을 수 있음 | comparison, possibility | 비교 기준 = 시술 전 이중턱(잠정) |
| `/timelines/5/phases/1/normal/1` | [0,12) | 경결감 (딱딱한 느낌) | gloss, texture | |  |
| `/timelines/5/phases/1/normal/2` | [0,17) | 통증 지속 (진통제 복용 가능) | persistence, management, possibility | 관리: 진통제 복용. 약 이름·용량 없음 |
| `/timelines/5/phases/1/normal/3` | [0,17) | 감각 이상 지속 (저림/무감각) | persistence, gloss, alt | |  |
| `/timelines/5/phases/1/abnormal/0` | [0,5) | 광범위 멍 | extent | |  |
| `/timelines/5/phases/1/abnormal/1` | [0,8) | 연하 시 불편감 | condition | 「시」 = 삼킬 때 |
| `/timelines/5/phases/1/caution/0` | [0,13) | 부종이 목/가슴으로 확대 | extent, direction, site, alt | |  |
| `/timelines/5/phases/1/caution/1` | [0,13) | 발열 (37.5도 이상) | numeric_threshold, unit | |  |
| `/timelines/5/phases/1/caution/2` | [0,8) | 피부 변색 악화 | worsening | |  |
| `/timelines/5/phases/1/emergency/0` | [0,20) | 피부 괴사 진행 (검은색 변색 확대) | progress, color, extent | |  |
| `/timelines/5/phases/1/emergency/1` | [0,21) | 하악변연신경 손상 (비대칭 미소 지속) | anatomy, persistence | |  |
| `/timelines/5/phases/1/emergency/2` | [0,16) | 호흡 곤란 (기도 주변 부종) | cause_gloss, site | |  |
| `/timelines/5/phases/2/period` | [0,7) | Day 3-7 | period, time_range | |  |
| `/timelines/5/phases/2/label` | [0,6) | 회복 시작기 | phase_label, onset | |  |
| `/timelines/5/phases/2/normal/0` | [0,12) | 부종 서서히 감소 시작 | speed, change, onset | 「서서히」 |
| `/timelines/5/phases/2/normal/1` | [0,11) | 경결감 지속 (정상) | persistence, judgment | |  |
| `/timelines/5/phases/2/normal/2` | [0,5) | 통증 완화 | change | |  |
| `/timelines/5/phases/2/normal/3` | [0,23) | 감각 이상 지속 가능 (정상, 수주 소요) | persistence, possibility, judgment, approx_time, duration | |  |
| `/timelines/5/phases/2/abnormal/0` | [0,8) | 부종 감소 없음 | negation | |  |
| `/timelines/5/phases/2/abnormal/1` | [0,8) | 경결 부위 커짐 | size, worsening | |  |
| `/timelines/5/phases/2/caution/0` | [0,19) | 감염 징후 (발적 + 열감 + 농) | early_sign, co_occurrence | |  |
| `/timelines/5/phases/2/caution/1` | [0,10) | 피부 울퉁불퉁 심화 | texture, worsening | |  |
| `/timelines/5/phases/2/emergency/0` | [0,5) | 피부 괴사 | event | |  |
| `/timelines/5/phases/2/emergency/1` | [0,5) | 농양 형성 | formation | |  |
| `/timelines/5/phases/3/period` | [0,8) | Day 7-14 | period, time_range | |  |
| `/timelines/5/phases/3/label` | [0,3) | 회복기 | phase_label | |  |
| `/timelines/5/phases/3/normal/0` | [0,11) | 부종 상당 부분 소실 | proportion_approx, resolution | 「상당 부분」 |
| `/timelines/5/phases/3/normal/1` | [0,9) | 경결감 점차 감소 | speed, change | |  |
| `/timelines/5/phases/3/normal/2` | [0,9) | 감각 정상화 시작 | recovery, onset | |  |
| `/timelines/5/phases/3/normal/3` | [0,19) | 지방 분해 효과 아직 미미 (정상) | temporal, insufficiency, judgment | 「아직」 |
| `/timelines/5/phases/3/abnormal/0` | [0,6) | 지속적 경결 | persistence | |  |
| `/timelines/5/phases/3/abnormal/0` | [8,32) | 대개 정상 염증반응으로 수 주 내 자연 소실 | frequency_hedge, judgment, approx_time, resolution | 「대개」. 「수 주」(띄어씀) 표기 |
| `/timelines/5/phases/3/abnormal/0` | [35,74) | 데옥시콜산은 임의 마사지가 표적외 확산·신경손상·괴사 위험이 있어 금기 | avoidance, management, risk, cause | 회피/금기 대상 = 임의 마사지. 이유 = 세 위험(「·」 나열). 성분명 데옥시콜산 |
| `/timelines/5/phases/3/abnormal/0` | [42,48) | 임의 마사지 | management, qualifier | 「임의」 — 지시 없는 마사지만인지 원문 범위 미상 |
| `/timelines/5/phases/3/abnormal/0` | [76,92) | 지속·악화 시 시술 병원 문의 | condition, action, recommendation | 「시」 조건 + 대응 행동 |
| `/timelines/5/phases/3/abnormal/0` | [33,34) | — | punctuation | 값 안 EM DASH(U+2014). 다른 값의 「--」 와 다른 문자 |
| `/timelines/5/phases/3/abnormal/1` | [0,8) | 감각 이상 지속 | persistence | |  |
| `/timelines/5/phases/3/caution/0` | [0,9) | 비대칭 경결/울퉁 | asymmetry, alt, texture | |  |
| `/timelines/5/phases/3/caution/1` | [0,6) | 지연성 감염 | delayed_onset | |  |
| `/timelines/5/phases/3/emergency/0` | [0,31) | 하악변연신경 손상 지속 (4주 이상 시 영구 손상 우려) | anatomy, persistence, duration_threshold, condition, possibility | 「4주 이상 시」 조건 + 「우려」 가능성. 4주 기준 = 손상 지속 기간(잠정) |
| `/timelines/5/phases/3/emergency/1` | [0,8) | 피부 괴사/궤양 | alt | |  |
| `/timelines/5/phases/4/period` | [0,9) | Day 14-30 | period, time_range | |  |
| `/timelines/5/phases/4/label` | [0,6) | 효과 발현기 | phase_label, onset | botox 「효과 발현기」(Day 3-7)와 이름 같고 시기 다름 |
| `/timelines/5/phases/4/normal/0` | [0,15) | 지방 분해 효과 서서히 발현 | speed, onset | |  |
| `/timelines/5/phases/4/normal/1` | [0,8) | 턱선 개선 시작 | site, onset, change | 시술 부위 「턱선」 이 처음 나오는 값(이 구획). 적용 부위 확정 아님 |
| `/timelines/5/phases/4/normal/2` | [0,6) | 경결감 소실 | resolution | |  |
| `/timelines/5/phases/4/normal/3` | [0,12) | 감각 정상화 (대부분) | recovery, proportion_approx | |  |
| `/timelines/5/phases/4/abnormal/0` | [0,19) | 효과 미미 (추가 세션 필요 가능) | insufficiency, retreatment, possibility | 「추가 세션」 — 간격 없음 |
| `/timelines/5/phases/4/abnormal/1` | [0,5) | 잔여 경결 | persistence | |  |
| `/timelines/5/phases/4/caution/0` | [0,9) | 비대칭 지방 분해 | asymmetry | |  |
| `/timelines/5/phases/4/caution/1` | [0,16) | 만성 감각 이상 (6주 이상) | chronicity, duration_threshold | 「만성」 을 6주 이상으로 병기 |
| `/timelines/5/phases/4/emergency/0` | [0,11) | 영구 신경 손상 징후 | permanence, early_sign | |  |

## 4. 자동 후보 요약 (정규식 일치분만 — 전수 의미 수집 아님)

P-ADVICE 4, P-AFTER 4, P-ALT 9, P-APPROX 3, P-APPROXTIME 3, P-COMPARE 10, P-COND-SI 3, P-COURSE 37, P-DAY 5, P-DEGREE 7, P-DURING 3, P-FREQ 1, P-LATIN 6, P-NEG 5, P-NUMUNIT 3, P-PAREN 23, P-POSSIB 5, P-SITE 7, P-SPEED 4, P-SYMBOL 4, P-TEMPORAL 1

전체 목록은 expressions.json (segment 필터).

## 5. 잠정 관찰

- **S06-O1** phases/3/abnormal/0 은 이 원장에서 가장 긴 값이다. 한 값 안에 증상(지속적 경결)·경과 판정(대개 정상)·소실 시기(수 주 내)·금기(임의 마사지)·이유(세 위험)·조건부 대응(지속·악화 시 문의)이 함께 있다. 후속 분해 대상(F).
- **S06-O2** 시간 기준: 「시술 중~직후」(phases/0), 「수주 소요」, 「수 주 내」, 「4주 이상 시」, 「6주 이상」. 「수주」/「수 주」 표기가 섞여 있다.
- **S06-O3** 「만성」 의 기간이 이 구획에서만 「6주 이상」 으로 병기된다. thread-lift 「만성 통증」 에는 없다.

## 6. 미결 (이 구획)

| ID | 분류 | 위치 | 내용 |
|---|---|---|---|
| S06-Q1 | B | `/timelines/5/phases/1/normal/0` | 「거의 필발」 은 원문으로 뜻을 정할 수 없다. 오기 여부를 원본 정정 없이 후속 확인 후보로 둔다(현재 사용자 선택 아님). |
| S06-Q2 | P | `/timelines/5/phases/3/emergency/0` | 「4주 이상」 의 기준이 손상 지속 기간인지 시술 후 경과인지 잠정. |
| S06-Q3 | F | `/timelines/5/phases/3/abnormal/0` | 복합 값의 절 단위 분해(증상·판정·금기·이유·조건부 대응)는 후속 의미 조사. |

## 7. 형태소 — 알려진 오분절 (교정 안 함)

| Pointer | 구간 | 원시 토큰 | 판정/설명 | 영향 |
|---|---|---|---|---|
| `/timelines/5/phases/0/abnormal/1` | [0,1) | 멍/MAG | K-MAG-NOUN 명사 「멍」 이 MAG(부사) | 사건 명사를 부사로 오태깅 — 명사 기준 탐색에서 누락 |
| `/timelines/5/phases/1/normal/0` | [14,17) | 이/MM + 중턱/NNG | K-IJUNGTEOK 「이중턱」 이 이/MM+중턱 으로 분할 | 비교 기준 부위 손실 |
| `/timelines/5/phases/2/emergency/1` | [0,2) | 농/NNG + 양/NNG | K-NONGYANG 「농양」 이 농+양 으로 분할 | 사건 명사 손실 |
| `/timelines/5/phases/3/caution/0` | [4,6) | 경/NNG + 결/NNG | K-GYEONGGYEOL 「경결」 이 경+결 로 분할 | 사건 명사 손실 |
| `/timelines/5/phases/3/caution/0` | [7,9) | 울/NNG + 퉁/MAG | K-ULTUNG 「울퉁」 이 울/NNG+퉁/MAG 로 분할 | 질감 표현 분할 |
| `/timelines/5/phases/4/abnormal/1` | [3,5) | 경/NNG + 결/NNG | K-GYEONGGYEOL 「경결」 이 경+결 로 분할 | 사건 명사 손실 |

