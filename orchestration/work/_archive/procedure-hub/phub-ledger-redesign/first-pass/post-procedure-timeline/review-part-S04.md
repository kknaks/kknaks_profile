# S04 — /timelines/3 fractional-co2 (프락셔널 CO2 레이저)

> build.py 생성. 원문 값과 잠정 관찰은 서로 다른 절·칸에 둔다.

- 소유 범위: prefix ['/timelines/3'] · exact []
- 공유 문맥(소유 아님): ['', '/timelines', '/consensus_method', '/reaction_levels', '/reaction_levels/normal', '/reaction_levels/abnormal', '/reaction_levels/caution', '/reaction_levels/emergency']
- 직접 읽기: done (manual/S04.txt) · 마지막 읽은 Pointer `/timelines/3/phases/4/emergency/1`

## 1. 원문 — 모든 노드 (문서 순서)

| # | Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 원문 구간(cp) |
|---|---|---|---|---|---|
| 1 | `/timelines/3` | `[3]` | object | {id, category, name, phases} | 4037–5393 |
| 2 | `/timelines/3/id` | `id` | string | fractional-co2 | 4043–4059 |
| 3 | `/timelines/3/category` | `category` | string | M8 | 4071–4075 |
| 4 | `/timelines/3/name` | `name` | string | 프락셔널 CO2 레이저 | 4083–4097 |
| 5 | `/timelines/3/phases` | `phases` | array | [길이 5] | 4107–5392 |
| 6 | `/timelines/3/phases/0` | `[0]` | object | {period, label, normal, abnormal, caution, emergency} | 4108–4336 |
| 7 | `/timelines/3/phases/0/period` | `period` | string | Day 0 | 4118–4125 |
| 8 | `/timelines/3/phases/0/label` | `label` | string | 시술 당일 | 4134–4141 |
| 9 | `/timelines/3/phases/0/normal` | `normal` | array | [길이 4] | 4151–4208 |
| 10 | `/timelines/3/phases/0/normal/0` | `[0]` | string | 강한 홍반/화끈감 (선번 유사) | 4152–4171 |
| 11 | `/timelines/3/phases/0/normal/1` | `[1]` | string | 부종 (특히 눈 주위) | 4172–4186 |
| 12 | `/timelines/3/phases/0/normal/2` | `[2]` | string | 미세한 점상 출혈 | 4187–4198 |
| 13 | `/timelines/3/phases/0/normal/3` | `[3]` | string | 삼출액 분비 | 4199–4207 |
| 14 | `/timelines/3/phases/0/abnormal` | `abnormal` | array | [길이 2] | 4220–4243 |
| 15 | `/timelines/3/phases/0/abnormal/0` | `[0]` | string | 예상보다 심한 부종 | 4221–4233 |
| 16 | `/timelines/3/phases/0/abnormal/1` | `[1]` | string | 지속적 출혈 | 4234–4242 |
| 17 | `/timelines/3/phases/0/caution` | `caution` | array | [길이 2] | 4254–4290 |
| 18 | `/timelines/3/phases/0/caution/0` | `[0]` | string | 심한 수포 형성 | 4255–4265 |
| 19 | `/timelines/3/phases/0/caution/1` | `[1]` | string | 비정상적 통증 (통증 스케일 8 이상) | 4266–4289 |
| 20 | `/timelines/3/phases/0/emergency` | `emergency` | array | [길이 2] | 4303–4335 |
| 21 | `/timelines/3/phases/0/emergency/0` | `[0]` | string | 아나필락시스 (마취크림 관련) | 4304–4322 |
| 22 | `/timelines/3/phases/0/emergency/1` | `[1]` | string | 광범위 수포/화상 | 4323–4334 |
| 23 | `/timelines/3/phases/1` | `[1]` | object | {period, label, normal, abnormal, caution, emergency} | 4337–4637 |
| 24 | `/timelines/3/phases/1/period` | `period` | string | Day 1-3 | 4347–4356 |
| 25 | `/timelines/3/phases/1/label` | `label` | string | 삼출/가피 형성기 | 4365–4376 |
| 26 | `/timelines/3/phases/1/normal` | `normal` | array | [길이 4] | 4386–4472 |
| 27 | `/timelines/3/phases/1/normal/0` | `[0]` | string | Day 1: 삼출액 지속, 홍반 심함 | 4387–4409 |
| 28 | `/timelines/3/phases/1/normal/1` | `[1]` | string | Day 2-3: 가피(딱지) 형성 시작 | 4410–4433 |
| 29 | `/timelines/3/phases/1/normal/2` | `[2]` | string | 부종 피크 (Day 1-2) 후 점차 감소 | 4434–4459 |
| 30 | `/timelines/3/phases/1/normal/3` | `[3]` | string | 피부 조임감/당김 | 4460–4471 |
| 31 | `/timelines/3/phases/1/abnormal` | `abnormal` | array | [길이 2] | 4484–4512 |
| 32 | `/timelines/3/phases/1/abnormal/0` | `[0]` | string | Day 3에도 삼출 지속 | 4485–4500 |
| 33 | `/timelines/3/phases/1/abnormal/1` | `[1]` | string | 가피 형성 불량 | 4501–4511 |
| 34 | `/timelines/3/phases/1/caution` | `caution` | array | [길이 3] | 4523–4580 |
| 35 | `/timelines/3/phases/1/caution/0` | `[0]` | string | 농성 삼출 (노란/초록 분비물) | 4524–4543 |
| 36 | `/timelines/3/phases/1/caution/1` | `[1]` | string | 발열 (37.5도 이상) | 4544–4559 |
| 37 | `/timelines/3/phases/1/caution/2` | `[2]` | string | 통증 악화 (감소가 아닌 증가) | 4560–4579 |
| 38 | `/timelines/3/phases/1/emergency` | `emergency` | array | [길이 2] | 4593–4636 |
| 39 | `/timelines/3/phases/1/emergency/0` | `[0]` | string | 감염 (고열 + 농 + 발적 확대) | 4594–4615 |
| 40 | `/timelines/3/phases/1/emergency/1` | `[1]` | string | 헤르페스 재활성화 (수포 군집) | 4616–4635 |
| 41 | `/timelines/3/phases/2` | `[2]` | object | {period, label, normal, abnormal, caution, emergency} | 4638–4903 |
| 42 | `/timelines/3/phases/2/period` | `period` | string | Day 3-5 | 4648–4657 |
| 43 | `/timelines/3/phases/2/label` | `label` | string | 필링기 | 4666–4671 |
| 44 | `/timelines/3/phases/2/normal` | `normal` | array | [길이 4] | 4681–4743 |
| 45 | `/timelines/3/phases/2/normal/0` | `[0]` | string | 가피 건조/갈색 변화 | 4682–4695 |
| 46 | `/timelines/3/phases/2/normal/1` | `[1]` | string | 가피 가장자리부터 벗겨짐 시작 | 4696–4714 |
| 47 | `/timelines/3/phases/2/normal/2` | `[2]` | string | 홍반 점차 감소 | 4715–4725 |
| 48 | `/timelines/3/phases/2/normal/3` | `[3]` | string | 가려움 (정상 치유 반응) | 4726–4742 |
| 49 | `/timelines/3/phases/2/abnormal` | `abnormal` | array | [길이 2] | 4755–4790 |
| 50 | `/timelines/3/phases/2/abnormal/0` | `[0]` | string | 가피 아래 농 | 4756–4765 |
| 51 | `/timelines/3/phases/2/abnormal/1` | `[1]` | string | 가피 조기 탈락 (자연 탈락 전 뜯음) | 4766–4789 |
| 52 | `/timelines/3/phases/2/caution` | `caution` | array | [길이 2] | 4801–4843 |
| 53 | `/timelines/3/phases/2/caution/0` | `[0]` | string | 감염 징후 (발적 확대 + 열감 + 통증) | 4802–4827 |
| 54 | `/timelines/3/phases/2/caution/1` | `[1]` | string | 가피 아래 이상 분비물 | 4828–4842 |
| 55 | `/timelines/3/phases/2/emergency` | `emergency` | array | [길이 2] | 4856–4902 |
| 56 | `/timelines/3/phases/2/emergency/0` | `[0]` | string | 봉와직염 (광범위 발적 + 고열) | 4857–4877 |
| 57 | `/timelines/3/phases/2/emergency/1` | `[1]` | string | 반흔 초기 징후 (비정상적 조직 증식) | 4878–4901 |
| 58 | `/timelines/3/phases/3` | `[3]` | object | {period, label, normal, abnormal, caution, emergency} | 4904–5144 |
| 59 | `/timelines/3/phases/3/period` | `period` | string | Day 5-7 | 4914–4923 |
| 60 | `/timelines/3/phases/3/label` | `label` | string | 재상피화기 | 4932–4939 |
| 61 | `/timelines/3/phases/3/normal` | `normal` | array | [길이 4] | 4949–5020 |
| 62 | `/timelines/3/phases/3/normal/0` | `[0]` | string | 대부분의 가피 자연 탈락 | 4950–4965 |
| 63 | `/timelines/3/phases/3/normal/1` | `[1]` | string | Day 7-10: 재상피화 완료 | 4966–4985 |
| 64 | `/timelines/3/phases/3/normal/2` | `[2]` | string | 분홍빛 새 피부 노출 | 4986–4999 |
| 65 | `/timelines/3/phases/3/normal/3` | `[3]` | string | 홍반 지속 (정상, 수주 소요) | 5000–5019 |
| 66 | `/timelines/3/phases/3/abnormal` | `abnormal` | array | [길이 2] | 5032–5061 |
| 67 | `/timelines/3/phases/3/abnormal/0` | `[0]` | string | Day 7에도 가피 잔존 | 5033–5048 |
| 68 | `/timelines/3/phases/3/abnormal/1` | `[1]` | string | 불균일한 재상피화 | 5049–5060 |
| 69 | `/timelines/3/phases/3/caution` | `caution` | array | [길이 2] | 5072–5107 |
| 70 | `/timelines/3/phases/3/caution/0` | `[0]` | string | 재상피화 지연 (10일 이상) | 5073–5091 |
| 71 | `/timelines/3/phases/3/caution/1` | `[1]` | string | 비후성 반흔 초기 징후 | 5092–5106 |
| 72 | `/timelines/3/phases/3/emergency` | `emergency` | array | [길이 2] | 5120–5143 |
| 73 | `/timelines/3/phases/3/emergency/0` | `[0]` | string | 감염 (지연성) | 5121–5131 |
| 74 | `/timelines/3/phases/3/emergency/1` | `[1]` | string | 반흔 형성 진행 | 5132–5142 |
| 75 | `/timelines/3/phases/4` | `[4]` | object | {period, label, normal, abnormal, caution, emergency} | 5145–5391 |
| 76 | `/timelines/3/phases/4/period` | `period` | string | Day 7-14 | 5155–5165 |
| 77 | `/timelines/3/phases/4/label` | `label` | string | 회복 완성기 | 5174–5182 |
| 78 | `/timelines/3/phases/4/normal` | `normal` | array | [길이 4] | 5192–5263 |
| 79 | `/timelines/3/phases/4/normal/0` | `[0]` | string | 재상피화 완료 | 5193–5202 |
| 80 | `/timelines/3/phases/4/normal/1` | `[1]` | string | 분홍빛 홍반 지속 (정상, 1-3개월 소요) | 5203–5229 |
| 81 | `/timelines/3/phases/4/normal/2` | `[2]` | string | 피부 질감 개선 시작 | 5230–5243 |
| 82 | `/timelines/3/phases/4/normal/3` | `[3]` | string | 메이크업 가능 (재상피화 후) | 5244–5262 |
| 83 | `/timelines/3/phases/4/abnormal` | `abnormal` | array | [길이 2] | 5275–5311 |
| 84 | `/timelines/3/phases/4/abnormal/0` | `[0]` | string | 지속적 홍반 (예상보다 진함) | 5276–5294 |
| 85 | `/timelines/3/phases/4/abnormal/1` | `[1]` | string | 색소침착 시작 (PIH) | 5295–5310 |
| 86 | `/timelines/3/phases/4/caution` | `caution` | array | [길이 2] | 5322–5357 |
| 87 | `/timelines/3/phases/4/caution/0` | `[0]` | string | PIH (염증 후 과색소침착) 진행 | 5323–5344 |
| 88 | `/timelines/3/phases/4/caution/1` | `[1]` | string | 비후성 반흔 형성 | 5345–5356 |
| 89 | `/timelines/3/phases/4/emergency` | `emergency` | array | [길이 2] | 5370–5390 |
| 90 | `/timelines/3/phases/4/emergency/0` | `[0]` | string | 켈로이드 형성 | 5371–5380 |
| 91 | `/timelines/3/phases/4/emergency/1` | `[1]` | string | 지연성 감염 | 5381–5389 |

## 2. 원문 — 기간별 보기 (같은 값, 원본 컬럼명 그대로)

`id` = fractional-co2 · `category` = M8 · `name` = 프락셔널 CO2 레이저

### phases/0 — `period` = Day 0 · `label` = 시술 당일

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 강한 홍반/화끈감 (선번 유사) | `/timelines/3/phases/0/normal/0` |
| `normal` | 1 | 부종 (특히 눈 주위) | `/timelines/3/phases/0/normal/1` |
| `normal` | 2 | 미세한 점상 출혈 | `/timelines/3/phases/0/normal/2` |
| `normal` | 3 | 삼출액 분비 | `/timelines/3/phases/0/normal/3` |
| `abnormal` | 0 | 예상보다 심한 부종 | `/timelines/3/phases/0/abnormal/0` |
| `abnormal` | 1 | 지속적 출혈 | `/timelines/3/phases/0/abnormal/1` |
| `caution` | 0 | 심한 수포 형성 | `/timelines/3/phases/0/caution/0` |
| `caution` | 1 | 비정상적 통증 (통증 스케일 8 이상) | `/timelines/3/phases/0/caution/1` |
| `emergency` | 0 | 아나필락시스 (마취크림 관련) | `/timelines/3/phases/0/emergency/0` |
| `emergency` | 1 | 광범위 수포/화상 | `/timelines/3/phases/0/emergency/1` |

### phases/1 — `period` = Day 1-3 · `label` = 삼출/가피 형성기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | Day 1: 삼출액 지속, 홍반 심함 | `/timelines/3/phases/1/normal/0` |
| `normal` | 1 | Day 2-3: 가피(딱지) 형성 시작 | `/timelines/3/phases/1/normal/1` |
| `normal` | 2 | 부종 피크 (Day 1-2) 후 점차 감소 | `/timelines/3/phases/1/normal/2` |
| `normal` | 3 | 피부 조임감/당김 | `/timelines/3/phases/1/normal/3` |
| `abnormal` | 0 | Day 3에도 삼출 지속 | `/timelines/3/phases/1/abnormal/0` |
| `abnormal` | 1 | 가피 형성 불량 | `/timelines/3/phases/1/abnormal/1` |
| `caution` | 0 | 농성 삼출 (노란/초록 분비물) | `/timelines/3/phases/1/caution/0` |
| `caution` | 1 | 발열 (37.5도 이상) | `/timelines/3/phases/1/caution/1` |
| `caution` | 2 | 통증 악화 (감소가 아닌 증가) | `/timelines/3/phases/1/caution/2` |
| `emergency` | 0 | 감염 (고열 + 농 + 발적 확대) | `/timelines/3/phases/1/emergency/0` |
| `emergency` | 1 | 헤르페스 재활성화 (수포 군집) | `/timelines/3/phases/1/emergency/1` |

### phases/2 — `period` = Day 3-5 · `label` = 필링기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 가피 건조/갈색 변화 | `/timelines/3/phases/2/normal/0` |
| `normal` | 1 | 가피 가장자리부터 벗겨짐 시작 | `/timelines/3/phases/2/normal/1` |
| `normal` | 2 | 홍반 점차 감소 | `/timelines/3/phases/2/normal/2` |
| `normal` | 3 | 가려움 (정상 치유 반응) | `/timelines/3/phases/2/normal/3` |
| `abnormal` | 0 | 가피 아래 농 | `/timelines/3/phases/2/abnormal/0` |
| `abnormal` | 1 | 가피 조기 탈락 (자연 탈락 전 뜯음) | `/timelines/3/phases/2/abnormal/1` |
| `caution` | 0 | 감염 징후 (발적 확대 + 열감 + 통증) | `/timelines/3/phases/2/caution/0` |
| `caution` | 1 | 가피 아래 이상 분비물 | `/timelines/3/phases/2/caution/1` |
| `emergency` | 0 | 봉와직염 (광범위 발적 + 고열) | `/timelines/3/phases/2/emergency/0` |
| `emergency` | 1 | 반흔 초기 징후 (비정상적 조직 증식) | `/timelines/3/phases/2/emergency/1` |

### phases/3 — `period` = Day 5-7 · `label` = 재상피화기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 대부분의 가피 자연 탈락 | `/timelines/3/phases/3/normal/0` |
| `normal` | 1 | Day 7-10: 재상피화 완료 | `/timelines/3/phases/3/normal/1` |
| `normal` | 2 | 분홍빛 새 피부 노출 | `/timelines/3/phases/3/normal/2` |
| `normal` | 3 | 홍반 지속 (정상, 수주 소요) | `/timelines/3/phases/3/normal/3` |
| `abnormal` | 0 | Day 7에도 가피 잔존 | `/timelines/3/phases/3/abnormal/0` |
| `abnormal` | 1 | 불균일한 재상피화 | `/timelines/3/phases/3/abnormal/1` |
| `caution` | 0 | 재상피화 지연 (10일 이상) | `/timelines/3/phases/3/caution/0` |
| `caution` | 1 | 비후성 반흔 초기 징후 | `/timelines/3/phases/3/caution/1` |
| `emergency` | 0 | 감염 (지연성) | `/timelines/3/phases/3/emergency/0` |
| `emergency` | 1 | 반흔 형성 진행 | `/timelines/3/phases/3/emergency/1` |

### phases/4 — `period` = Day 7-14 · `label` = 회복 완성기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 재상피화 완료 | `/timelines/3/phases/4/normal/0` |
| `normal` | 1 | 분홍빛 홍반 지속 (정상, 1-3개월 소요) | `/timelines/3/phases/4/normal/1` |
| `normal` | 2 | 피부 질감 개선 시작 | `/timelines/3/phases/4/normal/2` |
| `normal` | 3 | 메이크업 가능 (재상피화 후) | `/timelines/3/phases/4/normal/3` |
| `abnormal` | 0 | 지속적 홍반 (예상보다 진함) | `/timelines/3/phases/4/abnormal/0` |
| `abnormal` | 1 | 색소침착 시작 (PIH) | `/timelines/3/phases/4/abnormal/1` |
| `caution` | 0 | PIH (염증 후 과색소침착) 진행 | `/timelines/3/phases/4/caution/0` |
| `caution` | 1 | 비후성 반흔 형성 | `/timelines/3/phases/4/caution/1` |
| `emergency` | 0 | 켈로이드 형성 | `/timelines/3/phases/4/emergency/0` |
| `emergency` | 1 | 지연성 감염 | `/timelines/3/phases/4/emergency/1` |

## 3. 수동 표현 (직접 읽기) — 원문 구절과 관찰 칸 분리

| Pointer | 구간 | 원문 구절 | 탐색 관점(잠정) | 잠정 메모 |
|---|---|---|---|---|
| `/timelines/3/id` | [0,14) | fractional-co2 | id_code | |  |
| `/timelines/3/category` | [0,2) | M8 | id_code | |  |
| `/timelines/3/name` | [0,12) | 프락셔널 CO2 레이저 | procedure_name, mixed_script | CO2 는 영문+숫자. 형태소 분절 주의 |
| `/timelines/3/phases/0/period` | [0,5) | Day 0 | period | |  |
| `/timelines/3/phases/0/label` | [0,5) | 시술 당일 | reference_point | |  |
| `/timelines/3/phases/0/normal/0` | [0,17) | 강한 홍반/화끈감 (선번 유사) | degree, alt, similarity, loanword | 「선번」 = sunburn 외래어(잠정). 「강한」 |
| `/timelines/3/phases/0/normal/1` | [0,12) | 부종 (특히 눈 주위) | site, emphasis | 「특히」 |
| `/timelines/3/phases/0/normal/2` | [0,9) | 미세한 점상 출혈 | size, pattern | |  |
| `/timelines/3/phases/0/normal/3` | [0,6) | 삼출액 분비 | event | |  |
| `/timelines/3/phases/0/abnormal/0` | [0,10) | 예상보다 심한 부종 | comparison, severity | |  |
| `/timelines/3/phases/0/abnormal/1` | [0,6) | 지속적 출혈 | persistence | |  |
| `/timelines/3/phases/0/caution/0` | [0,8) | 심한 수포 형성 | severity, formation | |  |
| `/timelines/3/phases/0/caution/1` | [0,21) | 비정상적 통증 (통증 스케일 8 이상) | degree, scale_threshold | ha-filler 는 7 이상. 척도 정의 없음 |
| `/timelines/3/phases/0/emergency/0` | [0,16) | 아나필락시스 (마취크림 관련) | label, cause_ref | 「관련」 원인 연결 약함. 마취크림 = 시술 전 처치(잠정) |
| `/timelines/3/phases/0/emergency/1` | [0,9) | 광범위 수포/화상 | extent, alt | |  |
| `/timelines/3/phases/1/period` | [0,7) | Day 1-3 | period, time_range | |  |
| `/timelines/3/phases/1/label` | [0,9) | 삼출/가피 형성기 | phase_label, alt | |  |
| `/timelines/3/phases/1/normal/0` | [0,20) | Day 1: 삼출액 지속, 홍반 심함 | time_anchor, persistence, severity | 값 안 「Day 1:」 머리표 |
| `/timelines/3/phases/1/normal/1` | [0,21) | Day 2-3: 가피(딱지) 형성 시작 | time_anchor, time_range, gloss, onset | |  |
| `/timelines/3/phases/1/normal/2` | [0,23) | 부종 피크 (Day 1-2) 후 점차 감소 | peak, peak_time, sequence, speed | 「후」 선후. 「점차」 |
| `/timelines/3/phases/1/normal/3` | [0,9) | 피부 조임감/당김 | alt, subjective | |  |
| `/timelines/3/phases/1/abnormal/0` | [0,13) | Day 3에도 삼출 지속 | time_anchor, concessive, persistence | |  |
| `/timelines/3/phases/1/abnormal/1` | [0,8) | 가피 형성 불량 | quality_negative | |  |
| `/timelines/3/phases/1/caution/0` | [0,17) | 농성 삼출 (노란/초록 분비물) | color, alt, gloss | |  |
| `/timelines/3/phases/1/caution/1` | [0,13) | 발열 (37.5도 이상) | numeric_threshold, unit | |  |
| `/timelines/3/phases/1/caution/2` | [0,17) | 통증 악화 (감소가 아닌 증가) | worsening, negation, contrast | 「아닌」 |
| `/timelines/3/phases/1/emergency/0` | [0,19) | 감염 (고열 + 농 + 발적 확대) | cause_label, co_occurrence, extent | 「+」 세 증상 동반 |
| `/timelines/3/phases/1/emergency/1` | [0,17) | 헤르페스 재활성화 (수포 군집) | recurrence, pattern | |  |
| `/timelines/3/phases/2/period` | [0,7) | Day 3-5 | period, time_range | |  |
| `/timelines/3/phases/2/label` | [0,3) | 필링기 | phase_label, loanword | |  |
| `/timelines/3/phases/2/normal/0` | [0,11) | 가피 건조/갈색 변화 | alt, color_change | |  |
| `/timelines/3/phases/2/normal/1` | [0,16) | 가피 가장자리부터 벗겨짐 시작 | site_within, onset, sequence | 「가장자리부터」 시작 위치 |
| `/timelines/3/phases/2/normal/2` | [0,8) | 홍반 점차 감소 | speed, change | |  |
| `/timelines/3/phases/2/normal/3` | [0,14) | 가려움 (정상 치유 반응) | judgment | |  |
| `/timelines/3/phases/2/abnormal/0` | [0,7) | 가피 아래 농 | location | |  |
| `/timelines/3/phases/2/abnormal/1` | [0,21) | 가피 조기 탈락 (자연 탈락 전 뜯음) | timing, cause, behavior, sequence | 「전」 선후. 환자 행동이 원인(잠정) |
| `/timelines/3/phases/2/caution/0` | [0,23) | 감염 징후 (발적 확대 + 열감 + 통증) | early_sign, co_occurrence | |  |
| `/timelines/3/phases/2/caution/1` | [0,12) | 가피 아래 이상 분비물 | location, abnormality | |  |
| `/timelines/3/phases/2/emergency/0` | [0,18) | 봉와직염 (광범위 발적 + 고열) | label, extent, co_occurrence | |  |
| `/timelines/3/phases/2/emergency/1` | [0,21) | 반흔 초기 징후 (비정상적 조직 증식) | early_sign, gloss | |  |
| `/timelines/3/phases/3/period` | [0,7) | Day 5-7 | period, time_range | |  |
| `/timelines/3/phases/3/label` | [0,5) | 재상피화기 | phase_label | |  |
| `/timelines/3/phases/3/normal/0` | [0,13) | 대부분의 가피 자연 탈락 | proportion_approx | |  |
| `/timelines/3/phases/3/normal/1` | [0,17) | Day 7-10: 재상피화 완료 | time_anchor, time_range, completion | 기간(Day 5-7) 밖 Day 8-10 까지 걸치는 값 |
| `/timelines/3/phases/3/normal/2` | [0,11) | 분홍빛 새 피부 노출 | color | |  |
| `/timelines/3/phases/3/normal/3` | [0,17) | 홍반 지속 (정상, 수주 소요) | persistence, judgment, approx_time, duration | 「수주 소요」 지속 기간 근사 |
| `/timelines/3/phases/3/abnormal/0` | [0,13) | Day 7에도 가피 잔존 | time_anchor, concessive, persistence | |  |
| `/timelines/3/phases/3/abnormal/1` | [0,9) | 불균일한 재상피화 | quality_negative | |  |
| `/timelines/3/phases/3/caution/0` | [0,16) | 재상피화 지연 (10일 이상) | delay, duration_threshold | 「10일 이상」 이 시술 후 10일인지 지연 기간인지 불분명 |
| `/timelines/3/phases/3/caution/1` | [0,12) | 비후성 반흔 초기 징후 | early_sign | |  |
| `/timelines/3/phases/3/emergency/0` | [0,8) | 감염 (지연성) | delayed_onset | |  |
| `/timelines/3/phases/3/emergency/1` | [0,8) | 반흔 형성 진행 | formation, progress | |  |
| `/timelines/3/phases/4/period` | [0,8) | Day 7-14 | period, time_range | |  |
| `/timelines/3/phases/4/label` | [0,6) | 회복 완성기 | phase_label | |  |
| `/timelines/3/phases/4/normal/0` | [0,7) | 재상피화 완료 | completion | phases/3/normal/1 과 같은 사건이 두 기간에 나옴 |
| `/timelines/3/phases/4/normal/1` | [0,24) | 분홍빛 홍반 지속 (정상, 1-3개월 소요) | color, persistence, judgment, duration, time_range | 「개월」 단위. phases/3/normal/3 「수주 소요」 와 기간 표현이 다름 |
| `/timelines/3/phases/4/normal/2` | [0,11) | 피부 질감 개선 시작 | onset, change | |  |
| `/timelines/3/phases/4/normal/3` | [0,16) | 메이크업 가능 (재상피화 후) | activity, possibility, condition, sequence | 「후」 조건 — 관리·활동 재개 |
| `/timelines/3/phases/4/abnormal/0` | [0,16) | 지속적 홍반 (예상보다 진함) | persistence, comparison, color_degree | |  |
| `/timelines/3/phases/4/abnormal/1` | [0,13) | 색소침착 시작 (PIH) | onset, abbreviation | |  |
| `/timelines/3/phases/4/caution/0` | [0,19) | PIH (염증 후 과색소침착) 진행 | abbreviation, gloss, progress, sequence | 괄호 풀이 안의 「후」 는 용어 일부(조건 아님) |
| `/timelines/3/phases/4/caution/1` | [0,9) | 비후성 반흔 형성 | formation | |  |
| `/timelines/3/phases/4/emergency/0` | [0,7) | 켈로이드 형성 | formation | |  |
| `/timelines/3/phases/4/emergency/1` | [0,6) | 지연성 감염 | delayed_onset | |  |

## 4. 자동 후보 요약 (정규식 일치분만 — 전수 의미 수집 아님)

P-AFTER 6, P-ALT 6, P-APPROX 2, P-APPROXTIME 1, P-BEFORE 1, P-COMPARE 6, P-COURSE 35, P-DAY 11, P-DEGREE 9, P-DURING 1, P-LATIN 14, P-NEG 3, P-NUMUNIT 3, P-PAREN 24, P-POSSIB 1, P-SCALE 1, P-SITE 4, P-SPEED 3, P-SYMBOL 5, P-TEMPORAL 1

전체 목록은 expressions.json (segment 필터).

## 5. 잠정 관찰

- **S04-O1** 기간 Day 0 / 1-3 / 3-5 / 5-7 / 7-14. 값 안에 「Day 1:」「Day 2-3:」「Day 7-10:」 같은 세부 시점 머리표가 있다. phases/3 의 「Day 7-10」 은 그 기간(Day 5-7) 밖까지 간다.
- **S04-O2** 「재상피화 완료」 가 phases/3(Day 7-10 머리표)와 phases/4 에 두 번 나온다. 홍반 지속 기간이 phases/3 「수주 소요」, phases/4 「1-3개월 소요」 로 다르게 적혔다.
- **S04-O3** 관리·활동 표현: 「메이크업 가능 (재상피화 후)」 — 시간 대신 사건(재상피화) 을 기준으로 한 조건.
- **S04-O4** 「자연 탈락 전 뜯음」 은 환자 행동을 원인으로 적은 유일한 값이다(이 구획 안).

## 6. 미결 (이 구획)

| ID | 분류 | 위치 | 내용 |
|---|---|---|---|
| S04-Q1 | I | `/timelines/3/phases/3/normal/3` `/timelines/3/phases/4/normal/1` | 홍반 지속 기간 표현이 두 기간에서 다르다(수주 / 1-3개월). 원문 내 불일치 후보(I-DUR). |
| S04-Q2 | B | `/timelines/3/phases/3/caution/0` | 「10일 이상」 의 기준(시술 후 경과일인지 지연 기간인지)이 원문에 없다. |
| S04-Q3 | B | `/timelines/3/phases/0/caution/1` | 통증 스케일 정의 없음(S02 와 같은 원인). |

## 7. 형태소 — 알려진 오분절 (교정 안 함)

| Pointer | 구간 | 원시 토큰 | 판정/설명 | 영향 |
|---|---|---|---|---|
| `/timelines/3/phases/0/normal/0` | [11,13) | 선/NNG + 번/NNB | K-SEONBEON 외래어 「선번」 이 선+번(의존명사) 로 분할 | 외래어 사건명 손실 |
| `/timelines/3/phases/0/normal/0` | [14,16) | 유/NNG + 사/NNG | K-YUSA 「유사」 가 유+사 로 분할 | 비유·유사 단서 손실 |
| `/timelines/3/phases/0/caution/0` | [3,5) | 수/NNB + 포/NNG | K-SUPO 「수포」 가 수+포 로 분할 | 「수」(가능·수량) 오탐 위험, 사건명 손실 |
| `/timelines/3/phases/0/emergency/1` | [4,6) | 수/NNG + 포/NNG | K-SUPO 「수포」 가 수+포 로 분할 | 「수」(가능·수량) 오탐 위험, 사건명 손실 |
| `/timelines/3/phases/1/label` | [3,5) | 가/NNG + 피/NNG | K-GAPI 「가피」 가 가+피 로 분할 | 사건 명사 손실 |
| `/timelines/3/phases/1/normal/0` | [7,9) | 삼/NR + 출/NNG | K-SAMCHUL 「삼출」 이 삼/NR(수사)+출 로 분할 | 수량 오탐(삼=3) 위험 |
| `/timelines/3/phases/1/normal/1` | [9,11) | 가/NNG + 피/NNG | K-GAPI 「가피」 가 가+피 로 분할 | 사건 명사 손실 |
| `/timelines/3/phases/1/emergency/0` | [13,15) | 발/NNG + 적/XSN | K-BALJEOK 「발적」 이 발/NNG+적/XSN 으로 분할 | 사건 명사 손실(「-적」 접미 오인) |
| `/timelines/3/phases/1/emergency/1` | [11,13) | 수/NNB + 포/NNG | K-SUPO 「수포」 가 수+포 로 분할 | 「수」(가능·수량) 오탐 위험, 사건명 손실 |
| `/timelines/3/phases/2/caution/0` | [7,9) | 발/NNG + 적/XSN | K-BALJEOK 「발적」 이 발/NNG+적/XSN 으로 분할 | 사건 명사 손실(「-적」 접미 오인) |
| `/timelines/3/phases/2/emergency/0` | [10,12) | 발/NNG + 적/XSN | K-BALJEOK 「발적」 이 발/NNG+적/XSN 으로 분할 | 사건 명사 손실(「-적」 접미 오인) |
| `/timelines/3/phases/3/normal/0` | [5,7) | 가/NNG + 피/XPN | K-GAPI 「가피」 가 가+피 로 분할 | 사건 명사 손실 |
| `/timelines/3/phases/4/caution/0` | [10,13) | 과/NNG + 색소/NNG | K-GWA-NNG 접두 「과」 가 NNG 로 분석 | 과도 단서 품사 불일치 |

