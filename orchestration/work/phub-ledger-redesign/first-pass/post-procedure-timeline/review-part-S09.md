# S09 — /timelines/8 biostimulator (바이오스티뮬레이터/콜라겐부스터)

> build.py 생성. 원문 값과 잠정 관찰은 서로 다른 절·칸에 둔다.

- 소유 범위: prefix ['/timelines/8'] · exact []
- 공유 문맥(소유 아님): ['', '/timelines', '/consensus_method', '/reaction_levels', '/reaction_levels/normal', '/reaction_levels/abnormal', '/reaction_levels/caution', '/reaction_levels/emergency']
- 직접 읽기: done (manual/S09.txt) · 마지막 읽은 Pointer `/timelines/8/phases/3/emergency/1`

## 1. 원문 — 모든 노드 (문서 순서)

| # | Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 원문 구간(cp) |
|---|---|---|---|---|---|
| 1 | `/timelines/8` | `[8]` | object | {id, category, name, phases} | 9597–10669 |
| 2 | `/timelines/8/id` | `id` | string | biostimulator | 9603–9618 |
| 3 | `/timelines/8/category` | `category` | string | M3 | 9630–9634 |
| 4 | `/timelines/8/name` | `name` | string | 바이오스티뮬레이터/콜라겐부스터 | 9642–9660 |
| 5 | `/timelines/8/phases` | `phases` | array | [길이 4] | 9670–10668 |
| 6 | `/timelines/8/phases/0` | `[0]` | object | {period, label, normal, abnormal, caution, emergency} | 9671–9872 |
| 7 | `/timelines/8/phases/0/period` | `period` | string | Day 0 | 9681–9688 |
| 8 | `/timelines/8/phases/0/label` | `label` | string | 시술 당일 | 9697–9704 |
| 9 | `/timelines/8/phases/0/normal` | `normal` | array | [길이 3] | 9714–9772 |
| 10 | `/timelines/8/phases/0/normal/0` | `[0]` | string | 즉각적 볼륨 (희석액에 의한 것, 수일 내 흡수됨) | 9715–9745 |
| 11 | `/timelines/8/phases/0/normal/1` | `[1]` | string | 주사 부위 발적/부종 | 9746–9759 |
| 12 | `/timelines/8/phases/0/normal/2` | `[2]` | string | 경미한 통증/압통 | 9760–9771 |
| 13 | `/timelines/8/phases/0/abnormal` | `abnormal` | array | [길이 2] | 9784–9800 |
| 14 | `/timelines/8/phases/0/abnormal/0` | `[0]` | string | 멍 | 9785–9788 |
| 15 | `/timelines/8/phases/0/abnormal/1` | `[1]` | string | 주사 부위 경결 | 9789–9799 |
| 16 | `/timelines/8/phases/0/caution` | `caution` | array | [길이 2] | 9811–9833 |
| 17 | `/timelines/8/phases/0/caution/0` | `[0]` | string | 심한 통증 지속 | 9812–9822 |
| 18 | `/timelines/8/phases/0/caution/1` | `[1]` | string | 비정상적 부종 | 9823–9832 |
| 19 | `/timelines/8/phases/0/emergency` | `emergency` | array | [길이 2] | 9846–9871 |
| 20 | `/timelines/8/phases/0/emergency/0` | `[0]` | string | 아나필락시스 | 9847–9855 |
| 21 | `/timelines/8/phases/0/emergency/1` | `[1]` | string | 혈관폐색 (극히 드묾) | 9856–9870 |
| 22 | `/timelines/8/phases/1` | `[1]` | object | {period, label, normal, abnormal, caution, emergency} | 9873–10171 |
| 23 | `/timelines/8/phases/1/period` | `period` | string | Day 1-7 | 9883–9892 |
| 24 | `/timelines/8/phases/1/label` | `label` | string | 초기 흡수기 | 9901–9909 |
| 25 | `/timelines/8/phases/1/normal` | `normal` | array | [길이 4] | 9919–10020 |
| 26 | `/timelines/8/phases/1/normal/0` | `[0]` | string | Day 2-3: 볼륨 감소 (희석액 흡수, 정상) | 9920–9949 |
| 27 | `/timelines/8/phases/1/normal/1` | `[1]` | string | 부종/발적 소실 | 9950–9960 |
| 28 | `/timelines/8/phases/1/normal/2` | `[2]` | string | '원래대로 돌아간' 느낌 (정상) | 9961–9981 |
| 29 | `/timelines/8/phases/1/normal/3` | `[3]` | string | 시술 부위 부드러운 스무딩 (선택 — 결절 예방 효과는 미입증) | 9982–10019 |
| 30 | `/timelines/8/phases/1/abnormal` | `abnormal` | array | [길이 2] | 10032–10094 |
| 31 | `/timelines/8/phases/1/abnormal/0` | `[0]` | string | 결절 촉지 (자가 마사지로 해결할 대상이 아님 — 주입 깊이·농도 문제. 시술 병원에 문의) | 10033–10086 |
| 32 | `/timelines/8/phases/1/abnormal/1` | `[1]` | string | 멍 지속 | 10087–10093 |
| 33 | `/timelines/8/phases/1/caution` | `caution` | array | [길이 2] | 10105–10133 |
| 34 | `/timelines/8/phases/1/caution/0` | `[0]` | string | 비대칭 결절 | 10106–10114 |
| 35 | `/timelines/8/phases/1/caution/1` | `[1]` | string | 감염 징후 (발적 + 열감) | 10115–10132 |
| 36 | `/timelines/8/phases/1/emergency` | `emergency` | array | [길이 2] | 10146–10170 |
| 37 | `/timelines/8/phases/1/emergency/0` | `[0]` | string | 감염 (농/고열) | 10147–10158 |
| 38 | `/timelines/8/phases/1/emergency/1` | `[1]` | string | 이물 반응 초기 | 10159–10169 |
| 39 | `/timelines/8/phases/2` | `[2]` | object | {period, label, normal, abnormal, caution, emergency} | 10172–10422 |
| 40 | `/timelines/8/phases/2/period` | `period` | string | Day 7-30 | 10182–10192 |
| 41 | `/timelines/8/phases/2/label` | `label` | string | 콜라겐 유도기 | 10201–10210 |
| 42 | `/timelines/8/phases/2/normal` | `normal` | array | [길이 4] | 10220–10305 |
| 43 | `/timelines/8/phases/2/normal/0` | `[0]` | string | 볼륨 최저점 (희석액 완전 흡수) | 10221–10241 |
| 44 | `/timelines/8/phases/2/normal/1` | `[1]` | string | 눈에 보이는 변화 아직 없음 (정상) | 10242–10264 |
| 45 | `/timelines/8/phases/2/normal/2` | `[2]` | string | 콜라겐 생성 진행 중 (체내에서) | 10265–10285 |
| 46 | `/timelines/8/phases/2/normal/3` | `[3]` | string | 점진적 개선 시작 (3-4주) | 10286–10304 |
| 47 | `/timelines/8/phases/2/abnormal` | `abnormal` | array | [길이 2] | 10317–10332 |
| 48 | `/timelines/8/phases/2/abnormal/0` | `[0]` | string | 결절 지속 | 10318–10325 |
| 49 | `/timelines/8/phases/2/abnormal/1` | `[1]` | string | 비대칭 | 10326–10331 |
| 50 | `/timelines/8/phases/2/caution` | `caution` | array | [길이 2] | 10343–10367 |
| 51 | `/timelines/8/phases/2/caution/0` | `[0]` | string | 결절 크기 증가 | 10344–10354 |
| 52 | `/timelines/8/phases/2/caution/1` | `[1]` | string | 지연성 염증 반응 | 10355–10366 |
| 53 | `/timelines/8/phases/2/emergency` | `emergency` | array | [길이 2] | 10380–10421 |
| 54 | `/timelines/8/phases/2/emergency/0` | `[0]` | string | 육아종 형성 (단단한 결절 + 발적) | 10381–10403 |
| 55 | `/timelines/8/phases/2/emergency/1` | `[1]` | string | 이물 반응 (광범위 염증) | 10404–10420 |
| 56 | `/timelines/8/phases/3` | `[3]` | object | {period, label, normal, abnormal, caution, emergency} | 10423–10667 |
| 57 | `/timelines/8/phases/3/period` | `period` | string | Day 30-90 | 10433–10444 |
| 58 | `/timelines/8/phases/3/label` | `label` | string | 콜라겐 효과 발현기 | 10453–10465 |
| 59 | `/timelines/8/phases/3/normal` | `normal` | array | [길이 4] | 10475–10543 |
| 60 | `/timelines/8/phases/3/normal/0` | `[0]` | string | 콜라겐 볼륨 점진적 증가 | 10476–10491 |
| 61 | `/timelines/8/phases/3/normal/1` | `[1]` | string | 피부 탄력/질감 개선 | 10492–10505 |
| 62 | `/timelines/8/phases/3/normal/2` | `[2]` | string | 자연스러운 리프팅 효과 | 10506–10520 |
| 63 | `/timelines/8/phases/3/normal/3` | `[3]` | string | 최종 효과 판단 시점 (8-12주) | 10521–10542 |
| 64 | `/timelines/8/phases/3/abnormal` | `abnormal` | array | [길이 2] | 10555–10584 |
| 65 | `/timelines/8/phases/3/abnormal/0` | `[0]` | string | 효과 미미 (추가 세션 필요) | 10556–10574 |
| 66 | `/timelines/8/phases/3/abnormal/1` | `[1]` | string | 볼륨 비대칭 | 10575–10583 |
| 67 | `/timelines/8/phases/3/caution` | `caution` | array | [길이 2] | 10595–10619 |
| 68 | `/timelines/8/phases/3/caution/0` | `[0]` | string | 지연성 육아종 | 10596–10605 |
| 69 | `/timelines/8/phases/3/caution/1` | `[1]` | string | 비대칭 콜라겐 생성 | 10606–10618 |
| 70 | `/timelines/8/phases/3/emergency` | `emergency` | array | [길이 2] | 10632–10666 |
| 71 | `/timelines/8/phases/3/emergency/0` | `[0]` | string | 육아종 (수개월 후에도 발생 가능) | 10633–10654 |
| 72 | `/timelines/8/phases/3/emergency/1` | `[1]` | string | 만성 이물 반응 | 10655–10665 |

## 2. 원문 — 기간별 보기 (같은 값, 원본 컬럼명 그대로)

`id` = biostimulator · `category` = M3 · `name` = 바이오스티뮬레이터/콜라겐부스터

### phases/0 — `period` = Day 0 · `label` = 시술 당일

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 즉각적 볼륨 (희석액에 의한 것, 수일 내 흡수됨) | `/timelines/8/phases/0/normal/0` |
| `normal` | 1 | 주사 부위 발적/부종 | `/timelines/8/phases/0/normal/1` |
| `normal` | 2 | 경미한 통증/압통 | `/timelines/8/phases/0/normal/2` |
| `abnormal` | 0 | 멍 | `/timelines/8/phases/0/abnormal/0` |
| `abnormal` | 1 | 주사 부위 경결 | `/timelines/8/phases/0/abnormal/1` |
| `caution` | 0 | 심한 통증 지속 | `/timelines/8/phases/0/caution/0` |
| `caution` | 1 | 비정상적 부종 | `/timelines/8/phases/0/caution/1` |
| `emergency` | 0 | 아나필락시스 | `/timelines/8/phases/0/emergency/0` |
| `emergency` | 1 | 혈관폐색 (극히 드묾) | `/timelines/8/phases/0/emergency/1` |

### phases/1 — `period` = Day 1-7 · `label` = 초기 흡수기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | Day 2-3: 볼륨 감소 (희석액 흡수, 정상) | `/timelines/8/phases/1/normal/0` |
| `normal` | 1 | 부종/발적 소실 | `/timelines/8/phases/1/normal/1` |
| `normal` | 2 | '원래대로 돌아간' 느낌 (정상) | `/timelines/8/phases/1/normal/2` |
| `normal` | 3 | 시술 부위 부드러운 스무딩 (선택 — 결절 예방 효과는 미입증) | `/timelines/8/phases/1/normal/3` |
| `abnormal` | 0 | 결절 촉지 (자가 마사지로 해결할 대상이 아님 — 주입 깊이·농도 문제. 시술 병원에 문의) | `/timelines/8/phases/1/abnormal/0` |
| `abnormal` | 1 | 멍 지속 | `/timelines/8/phases/1/abnormal/1` |
| `caution` | 0 | 비대칭 결절 | `/timelines/8/phases/1/caution/0` |
| `caution` | 1 | 감염 징후 (발적 + 열감) | `/timelines/8/phases/1/caution/1` |
| `emergency` | 0 | 감염 (농/고열) | `/timelines/8/phases/1/emergency/0` |
| `emergency` | 1 | 이물 반응 초기 | `/timelines/8/phases/1/emergency/1` |

### phases/2 — `period` = Day 7-30 · `label` = 콜라겐 유도기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 볼륨 최저점 (희석액 완전 흡수) | `/timelines/8/phases/2/normal/0` |
| `normal` | 1 | 눈에 보이는 변화 아직 없음 (정상) | `/timelines/8/phases/2/normal/1` |
| `normal` | 2 | 콜라겐 생성 진행 중 (체내에서) | `/timelines/8/phases/2/normal/2` |
| `normal` | 3 | 점진적 개선 시작 (3-4주) | `/timelines/8/phases/2/normal/3` |
| `abnormal` | 0 | 결절 지속 | `/timelines/8/phases/2/abnormal/0` |
| `abnormal` | 1 | 비대칭 | `/timelines/8/phases/2/abnormal/1` |
| `caution` | 0 | 결절 크기 증가 | `/timelines/8/phases/2/caution/0` |
| `caution` | 1 | 지연성 염증 반응 | `/timelines/8/phases/2/caution/1` |
| `emergency` | 0 | 육아종 형성 (단단한 결절 + 발적) | `/timelines/8/phases/2/emergency/0` |
| `emergency` | 1 | 이물 반응 (광범위 염증) | `/timelines/8/phases/2/emergency/1` |

### phases/3 — `period` = Day 30-90 · `label` = 콜라겐 효과 발현기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 콜라겐 볼륨 점진적 증가 | `/timelines/8/phases/3/normal/0` |
| `normal` | 1 | 피부 탄력/질감 개선 | `/timelines/8/phases/3/normal/1` |
| `normal` | 2 | 자연스러운 리프팅 효과 | `/timelines/8/phases/3/normal/2` |
| `normal` | 3 | 최종 효과 판단 시점 (8-12주) | `/timelines/8/phases/3/normal/3` |
| `abnormal` | 0 | 효과 미미 (추가 세션 필요) | `/timelines/8/phases/3/abnormal/0` |
| `abnormal` | 1 | 볼륨 비대칭 | `/timelines/8/phases/3/abnormal/1` |
| `caution` | 0 | 지연성 육아종 | `/timelines/8/phases/3/caution/0` |
| `caution` | 1 | 비대칭 콜라겐 생성 | `/timelines/8/phases/3/caution/1` |
| `emergency` | 0 | 육아종 (수개월 후에도 발생 가능) | `/timelines/8/phases/3/emergency/0` |
| `emergency` | 1 | 만성 이물 반응 | `/timelines/8/phases/3/emergency/1` |

## 3. 수동 표현 (직접 읽기) — 원문 구절과 관찰 칸 분리

| Pointer | 구간 | 원문 구절 | 탐색 관점(잠정) | 잠정 메모 |
|---|---|---|---|---|
| `/timelines/8/id` | [0,13) | biostimulator | id_code | |  |
| `/timelines/8/category` | [0,2) | M3 | id_code | |  |
| `/timelines/8/name` | [0,16) | 바이오스티뮬레이터/콜라겐부스터 | procedure_name, alt, loanword | 「/」 두 이름 병기(동의어인지 대안인지 원문 불분명) |
| `/timelines/8/phases/0/period` | [0,5) | Day 0 | period | |  |
| `/timelines/8/phases/0/label` | [0,5) | 시술 당일 | reference_point | |  |
| `/timelines/8/phases/0/normal/0` | [0,28) | 즉각적 볼륨 (희석액에 의한 것, 수일 내 흡수됨) | onset_speed, cause, resolution, approx_time | 원인 = 희석액. 흡수 = 수일 내 |
| `/timelines/8/phases/0/normal/1` | [0,11) | 주사 부위 발적/부종 | site, alt | |  |
| `/timelines/8/phases/0/normal/2` | [0,9) | 경미한 통증/압통 | severity, alt | |  |
| `/timelines/8/phases/0/abnormal/0` | [0,1) | 멍 | event | |  |
| `/timelines/8/phases/0/abnormal/1` | [0,8) | 주사 부위 경결 | site | |  |
| `/timelines/8/phases/0/caution/0` | [0,8) | 심한 통증 지속 | severity, persistence | |  |
| `/timelines/8/phases/0/caution/1` | [0,7) | 비정상적 부종 | degree | |  |
| `/timelines/8/phases/0/emergency/0` | [0,6) | 아나필락시스 | label | |  |
| `/timelines/8/phases/0/emergency/1` | [0,12) | 혈관폐색 (극히 드묾) | frequency | |  |
| `/timelines/8/phases/1/period` | [0,7) | Day 1-7 | period, time_range | 다른 시술처럼 1-3/3-7 로 나누지 않음 |
| `/timelines/8/phases/1/label` | [0,6) | 초기 흡수기 | phase_label | |  |
| `/timelines/8/phases/1/normal/0` | [0,27) | Day 2-3: 볼륨 감소 (희석액 흡수, 정상) | time_anchor, time_range, change, cause, judgment | |  |
| `/timelines/8/phases/1/normal/1` | [0,8) | 부종/발적 소실 | alt, resolution | |  |
| `/timelines/8/phases/1/normal/2` | [0,18) | '원래대로 돌아간' 느낌 (정상) | quotation, subjective, judgment | ASCII 작은따옴표로 감싼 인용 표현 |
| `/timelines/8/phases/1/normal/3` | [0,14) | 시술 부위 부드러운 스무딩 | site, management, degree | 관리 행위(스무딩). 누가 하는지 원문 없음 |
| `/timelines/8/phases/1/normal/3` | [15,35) | (선택 — 결절 예방 효과는 미입증) | optional, evidence_negation | 「선택」 + 「미입증」 근거 부정. EM DASH |
| `/timelines/8/phases/1/abnormal/0` | [0,5) | 결절 촉지 | detection | |  |
| `/timelines/8/phases/1/abnormal/0` | [7,25) | 자가 마사지로 해결할 대상이 아님 | avoidance, negation, management | 「아님」 부정 — 자가 마사지 비권고 |
| `/timelines/8/phases/1/abnormal/0` | [28,39) | 주입 깊이·농도 문제 | depth, concentration, cause | 깊이·농도 = 원인. 수치 없음 |
| `/timelines/8/phases/1/abnormal/0` | [41,50) | 시술 병원에 문의 | action, recommendation | |  |
| `/timelines/8/phases/1/abnormal/0` | [26,27) | — | punctuation | 값 안 EM DASH(U+2014). 앞 절(아님)과 뒤 절(원인·대응)을 가름 |
| `/timelines/8/phases/1/normal/3` | [19,20) | — | punctuation | 값 안 EM DASH(U+2014) |
| `/timelines/8/phases/1/abnormal/1` | [0,4) | 멍 지속 | persistence | |  |
| `/timelines/8/phases/1/caution/0` | [0,6) | 비대칭 결절 | asymmetry | |  |
| `/timelines/8/phases/1/caution/1` | [0,15) | 감염 징후 (발적 + 열감) | early_sign, co_occurrence | |  |
| `/timelines/8/phases/1/emergency/0` | [0,9) | 감염 (농/고열) | gloss, alt | |  |
| `/timelines/8/phases/1/emergency/1` | [0,8) | 이물 반응 초기 | early_sign | |  |
| `/timelines/8/phases/2/period` | [0,8) | Day 7-30 | period, time_range | |  |
| `/timelines/8/phases/2/label` | [0,7) | 콜라겐 유도기 | phase_label, mechanism | |  |
| `/timelines/8/phases/2/normal/0` | [0,18) | 볼륨 최저점 (희석액 완전 흡수) | trough, degree, cause | 「최저점」 |
| `/timelines/8/phases/2/normal/1` | [0,20) | 눈에 보이는 변화 아직 없음 (정상) | negation, temporal, judgment | |  |
| `/timelines/8/phases/2/normal/2` | [0,18) | 콜라겐 생성 진행 중 (체내에서) | mechanism, progress, location | |  |
| `/timelines/8/phases/2/normal/3` | [0,16) | 점진적 개선 시작 (3-4주) | speed, onset, time_range | |  |
| `/timelines/8/phases/2/abnormal/0` | [0,5) | 결절 지속 | persistence | |  |
| `/timelines/8/phases/2/abnormal/1` | [0,3) | 비대칭 | asymmetry | 단독 값 |
| `/timelines/8/phases/2/caution/0` | [0,8) | 결절 크기 증가 | size, worsening | |  |
| `/timelines/8/phases/2/caution/1` | [0,9) | 지연성 염증 반응 | delayed_onset | |  |
| `/timelines/8/phases/2/emergency/0` | [0,20) | 육아종 형성 (단단한 결절 + 발적) | formation, texture, co_occurrence | |  |
| `/timelines/8/phases/2/emergency/1` | [0,14) | 이물 반응 (광범위 염증) | extent, gloss | |  |
| `/timelines/8/phases/3/period` | [0,9) | Day 30-90 | period, time_range | 원장에서 가장 긴 기간 |
| `/timelines/8/phases/3/label` | [0,10) | 콜라겐 효과 발현기 | phase_label, onset | |  |
| `/timelines/8/phases/3/normal/0` | [0,13) | 콜라겐 볼륨 점진적 증가 | speed, change | |  |
| `/timelines/8/phases/3/normal/1` | [0,11) | 피부 탄력/질감 개선 | alt, change | |  |
| `/timelines/8/phases/3/normal/2` | [0,12) | 자연스러운 리프팅 효과 | quality | |  |
| `/timelines/8/phases/3/normal/3` | [0,19) | 최종 효과 판단 시점 (8-12주) | evaluation_time, time_range | |  |
| `/timelines/8/phases/3/abnormal/0` | [0,16) | 효과 미미 (추가 세션 필요) | insufficiency, retreatment, recommendation | dca 는 「필요 가능」, 여기는 「필요」 |
| `/timelines/8/phases/3/abnormal/1` | [0,6) | 볼륨 비대칭 | asymmetry | |  |
| `/timelines/8/phases/3/caution/0` | [0,7) | 지연성 육아종 | delayed_onset | |  |
| `/timelines/8/phases/3/caution/1` | [0,10) | 비대칭 콜라겐 생성 | asymmetry, mechanism | |  |
| `/timelines/8/phases/3/emergency/0` | [0,19) | 육아종 (수개월 후에도 발생 가능) | onset_time, approx_time, sequence, concessive, possibility | 「후에도」 — 기간(Day 30-90) 밖 발생 언급 |
| `/timelines/8/phases/3/emergency/1` | [0,8) | 만성 이물 반응 | chronicity | |  |

## 4. 자동 후보 요약 (정규식 일치분만 — 전수 의미 수집 아님)

P-ADVICE 4, P-AFTER 2, P-ALT 6, P-APPROX 1, P-APPROXTIME 2, P-COURSE 19, P-DAY 5, P-DEGREE 5, P-DEPTH 1, P-DURING 2, P-FREQ 1, P-LATIN 5, P-NEG 4, P-NUMUNIT 2, P-PAREN 17, P-POSSIB 1, P-SITE 4, P-SPEED 3, P-SYMBOL 4, P-TEMPORAL 1

전체 목록은 expressions.json (segment 필터).

## 5. 잠정 관찰

- **S09-O1** 기간 Day 0 / 1-7 / 7-30 / 30-90. 값 안의 시간은 Day 2-3, 3-4주, 8-12주, 수일, 수개월 후.
- **S09-O2** 관리 표현: 스무딩(선택, 예방 효과 미입증), 자가 마사지 비권고, 시술 병원 문의. dca 의 「임의 마사지 금기」 와 표현·강도가 다르다(구획 간 비교, 잠정).
- **S09-O3** phases/3/emergency/0 「수개월 후에도 발생 가능」 은 해당 기간 끝(Day 90) 이후 발생을 말한다.

## 6. 미결 (이 구획)

| ID | 분류 | 위치 | 내용 |
|---|---|---|---|
| S09-Q1 | B | `/timelines/8/name` | 「바이오스티뮬레이터/콜라겐부스터」 의 「/」 가 동의어 병기인지 대안인지 원문에 없다. |
| S09-Q2 | B | `/timelines/8/phases/1/abnormal/0` | 「주입 깊이·농도 문제」 의 기준 깊이·농도가 원문에 없다. |

## 7. 형태소 — 알려진 오분절 (교정 안 함)

| Pointer | 구간 | 원시 토큰 | 판정/설명 | 영향 |
|---|---|---|---|---|
| `/timelines/8/phases/0/normal/1` | [6,8) | 발/NNG + 적/XSN | K-BALJEOK 「발적」 이 발/NNG+적/XSN 으로 분할 | 사건 명사 손실(「-적」 접미 오인) |
| `/timelines/8/phases/0/abnormal/0` | [0,1) | 멍/MAG | K-MAG-NOUN 명사 「멍」 이 MAG(부사) | 사건 명사를 부사로 오태깅 — 명사 기준 탐색에서 누락 |
| `/timelines/8/phases/0/abnormal/1` | [6,8) | 경/NNG + 결/NNG | K-GYEONGGYEOL 「경결」 이 경+결 로 분할 | 사건 명사 손실 |
| `/timelines/8/phases/1/normal/1` | [3,5) | 발/NNG + 적/XSN | K-BALJEOK 「발적」 이 발/NNG+적/XSN 으로 분할 | 사건 명사 손실(「-적」 접미 오인) |
| `/timelines/8/phases/1/normal/3` | [11,14) | 스무/MM + 딩/MAG | K-SMOOTHING 외래어 「스무딩」 이 스무/MM(수 관형사)+딩/MAG | 수량(스무=20) 오탐 위험, 관리 행위명 손실 |
| `/timelines/8/phases/1/abnormal/0` | [31,33) | 깊이/MAG | K-MAG-NOUN 명사 「깊이」 가 MAG(부사 「깊이」) | 깊이(대상 속성) 를 부사로 오태깅 |
| `/timelines/8/phases/1/abnormal/1` | [0,1) | 멍/MAG | K-MAG-NOUN 명사 「멍」 이 MAG(부사) | 사건 명사를 부사로 오태깅 — 명사 기준 탐색에서 누락 |
| `/timelines/8/phases/1/caution/1` | [7,9) | 발/NNG + 적/XSN | K-BALJEOK 「발적」 이 발/NNG+적/XSN 으로 분할 | 사건 명사 손실(「-적」 접미 오인) |
| `/timelines/8/phases/2/emergency/0` | [0,3) | 육아/NNG + 종/NNG | K-YUKAJONG 「육아종」 이 육아+종 으로 분할 | 사건 명사 손실(「육아」 오의미) |
| `/timelines/8/phases/2/emergency/0` | [17,19) | 발/NNG + 적/XSN | K-BALJEOK 「발적」 이 발/NNG+적/XSN 으로 분할 | 사건 명사 손실(「-적」 접미 오인) |

