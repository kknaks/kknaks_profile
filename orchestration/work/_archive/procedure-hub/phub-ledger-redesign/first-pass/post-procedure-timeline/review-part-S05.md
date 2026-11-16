# S05 — /timelines/4 thread-lift (실리프팅)

> build.py 생성. 원문 값과 잠정 관찰은 서로 다른 절·칸에 둔다.

- 소유 범위: prefix ['/timelines/4'] · exact []
- 공유 문맥(소유 아님): ['', '/timelines', '/consensus_method', '/reaction_levels', '/reaction_levels/normal', '/reaction_levels/abnormal', '/reaction_levels/caution', '/reaction_levels/emergency']
- 직접 읽기: done (manual/S05.txt) · 마지막 읽은 Pointer `/timelines/4/phases/4/emergency/1`

## 1. 원문 — 모든 노드 (문서 순서)

| # | Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 원문 구간(cp) |
|---|---|---|---|---|---|
| 1 | `/timelines/4` | `[4]` | object | {id, category, name, phases} | 5394–6686 |
| 2 | `/timelines/4/id` | `id` | string | thread-lift | 5400–5413 |
| 3 | `/timelines/4/category` | `category` | string | M7 | 5425–5429 |
| 4 | `/timelines/4/name` | `name` | string | 실리프팅 | 5437–5443 |
| 5 | `/timelines/4/phases` | `phases` | array | [길이 5] | 5453–6685 |
| 6 | `/timelines/4/phases/0` | `[0]` | object | {period, label, normal, abnormal, caution, emergency} | 5454–5690 |
| 7 | `/timelines/4/phases/0/period` | `period` | string | Day 0 | 5464–5471 |
| 8 | `/timelines/4/phases/0/label` | `label` | string | 시술 당일 | 5480–5487 |
| 9 | `/timelines/4/phases/0/normal` | `normal` | array | [길이 4] | 5497–5556 |
| 10 | `/timelines/4/phases/0/normal/0` | `[0]` | string | 즉각적 리프팅 효과 (과교정 상태) | 5498–5519 |
| 11 | `/timelines/4/phases/0/normal/1` | `[1]` | string | 부종/당김감 | 5520–5528 |
| 12 | `/timelines/4/phases/0/normal/2` | `[2]` | string | 주사 부위 통증 | 5529–5539 |
| 13 | `/timelines/4/phases/0/normal/3` | `[3]` | string | 입 벌리기 불편 (정상) | 5540–5555 |
| 14 | `/timelines/4/phases/0/abnormal` | `abnormal` | array | [길이 2] | 5568–5600 |
| 15 | `/timelines/4/phases/0/abnormal/0` | `[0]` | string | 멍 (광범위할 수 있음) | 5569–5584 |
| 16 | `/timelines/4/phases/0/abnormal/1` | `[1]` | string | 한쪽이 더 당기는 느낌 | 5585–5599 |
| 17 | `/timelines/4/phases/0/caution` | `caution` | array | [길이 2] | 5611–5640 |
| 18 | `/timelines/4/phases/0/caution/0` | `[0]` | string | 비정상적 심한 통증 | 5612–5624 |
| 19 | `/timelines/4/phases/0/caution/1` | `[1]` | string | 피부 표면에 실 만져짐 | 5625–5639 |
| 20 | `/timelines/4/phases/0/emergency` | `emergency` | array | [길이 2] | 5653–5689 |
| 21 | `/timelines/4/phases/0/emergency/0` | `[0]` | string | 심한 출혈/혈종 | 5654–5664 |
| 22 | `/timelines/4/phases/0/emergency/1` | `[1]` | string | 안면 신경 손상 (입꼬리/눈꺼풀 마비) | 5665–5688 |
| 23 | `/timelines/4/phases/1` | `[1]` | object | {period, label, normal, abnormal, caution, emergency} | 5691–5967 |
| 24 | `/timelines/4/phases/1/period` | `period` | string | Day 1-3 | 5701–5710 |
| 25 | `/timelines/4/phases/1/label` | `label` | string | 급성 부종기 | 5719–5727 |
| 26 | `/timelines/4/phases/1/normal` | `normal` | array | [길이 4] | 5737–5805 |
| 27 | `/timelines/4/phases/1/normal/0` | `[0]` | string | 부종 피크 (Day 1-2) | 5738–5755 |
| 28 | `/timelines/4/phases/1/normal/1` | `[1]` | string | 멍 확대 (중력에 의해 아래로 이동) | 5756–5778 |
| 29 | `/timelines/4/phases/1/normal/2` | `[2]` | string | 입 벌리기/씹기 불편 지속 | 5779–5795 |
| 30 | `/timelines/4/phases/1/normal/3` | `[3]` | string | 당김감 강함 | 5796–5804 |
| 31 | `/timelines/4/phases/1/abnormal` | `abnormal` | array | [길이 2] | 5817–5848 |
| 32 | `/timelines/4/phases/1/abnormal/0` | `[0]` | string | 비대칭 부종 (좌우 차이 큼) | 5818–5836 |
| 33 | `/timelines/4/phases/1/abnormal/1` | `[1]` | string | 침자 부위 삼출 | 5837–5847 |
| 34 | `/timelines/4/phases/1/caution` | `caution` | array | [길이 3] | 5859–5911 |
| 35 | `/timelines/4/phases/1/caution/0` | `[0]` | string | 발열 (37.5도 이상) | 5860–5875 |
| 36 | `/timelines/4/phases/1/caution/1` | `[1]` | string | 통증 악화 (개선 아닌 악화) | 5876–5894 |
| 37 | `/timelines/4/phases/1/caution/2` | `[2]` | string | 실 삽입 부위 발적 확대 | 5895–5910 |
| 38 | `/timelines/4/phases/1/emergency` | `emergency` | array | [길이 2] | 5924–5966 |
| 39 | `/timelines/4/phases/1/emergency/0` | `[0]` | string | 감염 초기 (발열 + 발적 + 농) | 5925–5946 |
| 40 | `/timelines/4/phases/1/emergency/1` | `[1]` | string | 혈종 형성 (한쪽 급격 부종) | 5947–5965 |
| 41 | `/timelines/4/phases/2` | `[2]` | object | {period, label, normal, abnormal, caution, emergency} | 5968–6220 |
| 42 | `/timelines/4/phases/2/period` | `period` | string | Day 3-7 | 5978–5987 |
| 43 | `/timelines/4/phases/2/label` | `label` | string | 회복기 | 5996–6001 |
| 44 | `/timelines/4/phases/2/normal` | `normal` | array | [길이 4] | 6011–6061 |
| 45 | `/timelines/4/phases/2/normal/0` | `[0]` | string | 부종 점차 감소 | 6012–6022 |
| 46 | `/timelines/4/phases/2/normal/1` | `[1]` | string | 멍 황색 변화 (흡수 진행) | 6023–6040 |
| 47 | `/timelines/4/phases/2/normal/2` | `[2]` | string | 당김감 완화 | 6041–6049 |
| 48 | `/timelines/4/phases/2/normal/3` | `[3]` | string | 입 움직임 개선 | 6050–6060 |
| 49 | `/timelines/4/phases/2/abnormal` | `abnormal` | array | [길이 2] | 6073–6108 |
| 50 | `/timelines/4/phases/2/abnormal/0` | `[0]` | string | 부종 감소 느림 | 6074–6084 |
| 51 | `/timelines/4/phases/2/abnormal/1` | `[1]` | string | 피부 표면 불규칙 (dimpling) | 6085–6107 |
| 52 | `/timelines/4/phases/2/caution` | `caution` | array | [길이 3] | 6119–6160 |
| 53 | `/timelines/4/phases/2/caution/0` | `[0]` | string | 실 촉지/돌출 (피부 아래 만져짐) | 6120–6141 |
| 54 | `/timelines/4/phases/2/caution/1` | `[1]` | string | 지속적 발열 | 6142–6150 |
| 55 | `/timelines/4/phases/2/caution/2` | `[2]` | string | 심한 비대칭 | 6151–6159 |
| 56 | `/timelines/4/phases/2/emergency` | `emergency` | array | [길이 3] | 6173–6219 |
| 57 | `/timelines/4/phases/2/emergency/0` | `[0]` | string | 실 노출 (피부 밖으로) | 6174–6189 |
| 58 | `/timelines/4/phases/2/emergency/1` | `[1]` | string | 감염 (농/발열/발적) | 6190–6204 |
| 59 | `/timelines/4/phases/2/emergency/2` | `[2]` | string | 안면 신경 마비 지속 | 6205–6218 |
| 60 | `/timelines/4/phases/3` | `[3]` | object | {period, label, normal, abnormal, caution, emergency} | 6221–6461 |
| 61 | `/timelines/4/phases/3/period` | `period` | string | Day 7-14 | 6231–6241 |
| 62 | `/timelines/4/phases/3/label` | `label` | string | 안정기 | 6250–6255 |
| 63 | `/timelines/4/phases/3/normal` | `normal` | array | [길이 4] | 6265–6321 |
| 64 | `/timelines/4/phases/3/normal/0` | `[0]` | string | 부종/멍 대부분 소실 | 6266–6279 |
| 65 | `/timelines/4/phases/3/normal/1` | `[1]` | string | 리프팅 효과 자연스러워짐 | 6280–6295 |
| 66 | `/timelines/4/phases/3/normal/2` | `[2]` | string | 일상생활 완전 복귀 | 6296–6308 |
| 67 | `/timelines/4/phases/3/normal/3` | `[3]` | string | 콜라겐 생성 시작 | 6309–6320 |
| 68 | `/timelines/4/phases/3/abnormal` | `abnormal` | array | [길이 3] | 6333–6375 |
| 69 | `/timelines/4/phases/3/abnormal/0` | `[0]` | string | 경미한 비대칭 잔존 | 6334–6346 |
| 70 | `/timelines/4/phases/3/abnormal/1` | `[1]` | string | 미세한 dimpling 잔존 | 6347–6364 |
| 71 | `/timelines/4/phases/3/abnormal/2` | `[2]` | string | 간헐적 찌릿함 | 6365–6374 |
| 72 | `/timelines/4/phases/3/caution` | `caution` | array | [길이 3] | 6386–6418 |
| 73 | `/timelines/4/phases/3/caution/0` | `[0]` | string | 실 이동/돌출 징후 | 6387–6399 |
| 74 | `/timelines/4/phases/3/caution/1` | `[1]` | string | 지연성 감염 | 6400–6408 |
| 75 | `/timelines/4/phases/3/caution/2` | `[2]` | string | 비대칭 악화 | 6409–6417 |
| 76 | `/timelines/4/phases/3/emergency` | `emergency` | array | [길이 3] | 6431–6460 |
| 77 | `/timelines/4/phases/3/emergency/0` | `[0]` | string | 실 노출 | 6432–6438 |
| 78 | `/timelines/4/phases/3/emergency/1` | `[1]` | string | 농양 형성 | 6439–6446 |
| 79 | `/timelines/4/phases/3/emergency/2` | `[2]` | string | 진행성 안면 비대칭 | 6447–6459 |
| 80 | `/timelines/4/phases/4` | `[4]` | object | {period, label, normal, abnormal, caution, emergency} | 6462–6684 |
| 81 | `/timelines/4/phases/4/period` | `period` | string | Day 14-30 | 6472–6483 |
| 82 | `/timelines/4/phases/4/label` | `label` | string | 최종 안정기 | 6492–6500 |
| 83 | `/timelines/4/phases/4/normal` | `normal` | array | [길이 4] | 6510–6569 |
| 84 | `/timelines/4/phases/4/normal/0` | `[0]` | string | 최종 리프팅 결과 확인 | 6511–6525 |
| 85 | `/timelines/4/phases/4/normal/1` | `[1]` | string | 당김감 자연스러움 | 6526–6537 |
| 86 | `/timelines/4/phases/4/normal/2` | `[2]` | string | 콜라겐 리모델링 진행 중 | 6538–6553 |
| 87 | `/timelines/4/phases/4/normal/3` | `[3]` | string | 재시술 판단 가능 시점 | 6554–6568 |
| 88 | `/timelines/4/phases/4/abnormal` | `abnormal` | array | [길이 2] | 6581–6607 |
| 89 | `/timelines/4/phases/4/abnormal/0` | `[0]` | string | 리프팅 효과 조기 감소 | 6582–6596 |
| 90 | `/timelines/4/phases/4/abnormal/1` | `[1]` | string | 경미한 비대칭 | 6597–6606 |
| 91 | `/timelines/4/phases/4/caution` | `caution` | array | [길이 2] | 6618–6647 |
| 92 | `/timelines/4/phases/4/caution/0` | `[0]` | string | 실 이동 (리프팅 소실) | 6619–6634 |
| 93 | `/timelines/4/phases/4/caution/1` | `[1]` | string | 만성 통증/불편감 | 6635–6646 |
| 94 | `/timelines/4/phases/4/emergency` | `emergency` | array | [길이 2] | 6660–6683 |
| 95 | `/timelines/4/phases/4/emergency/0` | `[0]` | string | 지연성 감염/농양 | 6661–6672 |
| 96 | `/timelines/4/phases/4/emergency/1` | `[1]` | string | 실 노출/돌출 | 6673–6682 |

## 2. 원문 — 기간별 보기 (같은 값, 원본 컬럼명 그대로)

`id` = thread-lift · `category` = M7 · `name` = 실리프팅

### phases/0 — `period` = Day 0 · `label` = 시술 당일

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 즉각적 리프팅 효과 (과교정 상태) | `/timelines/4/phases/0/normal/0` |
| `normal` | 1 | 부종/당김감 | `/timelines/4/phases/0/normal/1` |
| `normal` | 2 | 주사 부위 통증 | `/timelines/4/phases/0/normal/2` |
| `normal` | 3 | 입 벌리기 불편 (정상) | `/timelines/4/phases/0/normal/3` |
| `abnormal` | 0 | 멍 (광범위할 수 있음) | `/timelines/4/phases/0/abnormal/0` |
| `abnormal` | 1 | 한쪽이 더 당기는 느낌 | `/timelines/4/phases/0/abnormal/1` |
| `caution` | 0 | 비정상적 심한 통증 | `/timelines/4/phases/0/caution/0` |
| `caution` | 1 | 피부 표면에 실 만져짐 | `/timelines/4/phases/0/caution/1` |
| `emergency` | 0 | 심한 출혈/혈종 | `/timelines/4/phases/0/emergency/0` |
| `emergency` | 1 | 안면 신경 손상 (입꼬리/눈꺼풀 마비) | `/timelines/4/phases/0/emergency/1` |

### phases/1 — `period` = Day 1-3 · `label` = 급성 부종기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 부종 피크 (Day 1-2) | `/timelines/4/phases/1/normal/0` |
| `normal` | 1 | 멍 확대 (중력에 의해 아래로 이동) | `/timelines/4/phases/1/normal/1` |
| `normal` | 2 | 입 벌리기/씹기 불편 지속 | `/timelines/4/phases/1/normal/2` |
| `normal` | 3 | 당김감 강함 | `/timelines/4/phases/1/normal/3` |
| `abnormal` | 0 | 비대칭 부종 (좌우 차이 큼) | `/timelines/4/phases/1/abnormal/0` |
| `abnormal` | 1 | 침자 부위 삼출 | `/timelines/4/phases/1/abnormal/1` |
| `caution` | 0 | 발열 (37.5도 이상) | `/timelines/4/phases/1/caution/0` |
| `caution` | 1 | 통증 악화 (개선 아닌 악화) | `/timelines/4/phases/1/caution/1` |
| `caution` | 2 | 실 삽입 부위 발적 확대 | `/timelines/4/phases/1/caution/2` |
| `emergency` | 0 | 감염 초기 (발열 + 발적 + 농) | `/timelines/4/phases/1/emergency/0` |
| `emergency` | 1 | 혈종 형성 (한쪽 급격 부종) | `/timelines/4/phases/1/emergency/1` |

### phases/2 — `period` = Day 3-7 · `label` = 회복기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 부종 점차 감소 | `/timelines/4/phases/2/normal/0` |
| `normal` | 1 | 멍 황색 변화 (흡수 진행) | `/timelines/4/phases/2/normal/1` |
| `normal` | 2 | 당김감 완화 | `/timelines/4/phases/2/normal/2` |
| `normal` | 3 | 입 움직임 개선 | `/timelines/4/phases/2/normal/3` |
| `abnormal` | 0 | 부종 감소 느림 | `/timelines/4/phases/2/abnormal/0` |
| `abnormal` | 1 | 피부 표면 불규칙 (dimpling) | `/timelines/4/phases/2/abnormal/1` |
| `caution` | 0 | 실 촉지/돌출 (피부 아래 만져짐) | `/timelines/4/phases/2/caution/0` |
| `caution` | 1 | 지속적 발열 | `/timelines/4/phases/2/caution/1` |
| `caution` | 2 | 심한 비대칭 | `/timelines/4/phases/2/caution/2` |
| `emergency` | 0 | 실 노출 (피부 밖으로) | `/timelines/4/phases/2/emergency/0` |
| `emergency` | 1 | 감염 (농/발열/발적) | `/timelines/4/phases/2/emergency/1` |
| `emergency` | 2 | 안면 신경 마비 지속 | `/timelines/4/phases/2/emergency/2` |

### phases/3 — `period` = Day 7-14 · `label` = 안정기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 부종/멍 대부분 소실 | `/timelines/4/phases/3/normal/0` |
| `normal` | 1 | 리프팅 효과 자연스러워짐 | `/timelines/4/phases/3/normal/1` |
| `normal` | 2 | 일상생활 완전 복귀 | `/timelines/4/phases/3/normal/2` |
| `normal` | 3 | 콜라겐 생성 시작 | `/timelines/4/phases/3/normal/3` |
| `abnormal` | 0 | 경미한 비대칭 잔존 | `/timelines/4/phases/3/abnormal/0` |
| `abnormal` | 1 | 미세한 dimpling 잔존 | `/timelines/4/phases/3/abnormal/1` |
| `abnormal` | 2 | 간헐적 찌릿함 | `/timelines/4/phases/3/abnormal/2` |
| `caution` | 0 | 실 이동/돌출 징후 | `/timelines/4/phases/3/caution/0` |
| `caution` | 1 | 지연성 감염 | `/timelines/4/phases/3/caution/1` |
| `caution` | 2 | 비대칭 악화 | `/timelines/4/phases/3/caution/2` |
| `emergency` | 0 | 실 노출 | `/timelines/4/phases/3/emergency/0` |
| `emergency` | 1 | 농양 형성 | `/timelines/4/phases/3/emergency/1` |
| `emergency` | 2 | 진행성 안면 비대칭 | `/timelines/4/phases/3/emergency/2` |

### phases/4 — `period` = Day 14-30 · `label` = 최종 안정기

| 원본 컬럼명 | 순서 | 원문 값 | Pointer |
|---|---|---|---|
| `normal` | 0 | 최종 리프팅 결과 확인 | `/timelines/4/phases/4/normal/0` |
| `normal` | 1 | 당김감 자연스러움 | `/timelines/4/phases/4/normal/1` |
| `normal` | 2 | 콜라겐 리모델링 진행 중 | `/timelines/4/phases/4/normal/2` |
| `normal` | 3 | 재시술 판단 가능 시점 | `/timelines/4/phases/4/normal/3` |
| `abnormal` | 0 | 리프팅 효과 조기 감소 | `/timelines/4/phases/4/abnormal/0` |
| `abnormal` | 1 | 경미한 비대칭 | `/timelines/4/phases/4/abnormal/1` |
| `caution` | 0 | 실 이동 (리프팅 소실) | `/timelines/4/phases/4/caution/0` |
| `caution` | 1 | 만성 통증/불편감 | `/timelines/4/phases/4/caution/1` |
| `emergency` | 0 | 지연성 감염/농양 | `/timelines/4/phases/4/emergency/0` |
| `emergency` | 1 | 실 노출/돌출 | `/timelines/4/phases/4/emergency/1` |

## 3. 수동 표현 (직접 읽기) — 원문 구절과 관찰 칸 분리

| Pointer | 구간 | 원문 구절 | 탐색 관점(잠정) | 잠정 메모 |
|---|---|---|---|---|
| `/timelines/4/id` | [0,11) | thread-lift | id_code | |  |
| `/timelines/4/category` | [0,2) | M7 | id_code | |  |
| `/timelines/4/name` | [0,4) | 실리프팅 | procedure_name | 형태소 분절 주의(실+리프팅) |
| `/timelines/4/phases/0/period` | [0,5) | Day 0 | period | |  |
| `/timelines/4/phases/0/label` | [0,5) | 시술 당일 | reference_point | |  |
| `/timelines/4/phases/0/normal/0` | [0,19) | 즉각적 리프팅 효과 (과교정 상태) | onset_speed, judgment | |  |
| `/timelines/4/phases/0/normal/1` | [0,6) | 부종/당김감 | alt | |  |
| `/timelines/4/phases/0/normal/2` | [0,8) | 주사 부위 통증 | site | 실리프팅인데 「주사 부위」 표현(원문 그대로) |
| `/timelines/4/phases/0/normal/3` | [0,13) | 입 벌리기 불편 (정상) | function, judgment | |  |
| `/timelines/4/phases/0/abnormal/0` | [0,13) | 멍 (광범위할 수 있음) | extent, possibility | |  |
| `/timelines/4/phases/0/abnormal/1` | [0,12) | 한쪽이 더 당기는 느낌 | asymmetry, comparison, subjective | 「더」 |
| `/timelines/4/phases/0/caution/0` | [0,10) | 비정상적 심한 통증 | degree, severity | |  |
| `/timelines/4/phases/0/caution/1` | [0,12) | 피부 표면에 실 만져짐 | location, detection | |  |
| `/timelines/4/phases/0/emergency/0` | [0,8) | 심한 출혈/혈종 | severity, alt | |  |
| `/timelines/4/phases/0/emergency/1` | [0,21) | 안면 신경 손상 (입꼬리/눈꺼풀 마비) | site, gloss, alt | |  |
| `/timelines/4/phases/1/period` | [0,7) | Day 1-3 | period, time_range | |  |
| `/timelines/4/phases/1/label` | [0,6) | 급성 부종기 | phase_label, speed | |  |
| `/timelines/4/phases/1/normal/0` | [0,15) | 부종 피크 (Day 1-2) | peak, peak_time | |  |
| `/timelines/4/phases/1/normal/1` | [0,20) | 멍 확대 (중력에 의해 아래로 이동) | extent, cause, direction | 「아래로」 방향 |
| `/timelines/4/phases/1/normal/2` | [0,14) | 입 벌리기/씹기 불편 지속 | function, alt, persistence | |  |
| `/timelines/4/phases/1/normal/3` | [0,6) | 당김감 강함 | degree | |  |
| `/timelines/4/phases/1/abnormal/0` | [0,16) | 비대칭 부종 (좌우 차이 큼) | asymmetry, degree | |  |
| `/timelines/4/phases/1/abnormal/1` | [0,8) | 침자 부위 삼출 | site | |  |
| `/timelines/4/phases/1/caution/0` | [0,13) | 발열 (37.5도 이상) | numeric_threshold, unit | |  |
| `/timelines/4/phases/1/caution/1` | [0,16) | 통증 악화 (개선 아닌 악화) | worsening, negation, contrast | |  |
| `/timelines/4/phases/1/caution/2` | [0,13) | 실 삽입 부위 발적 확대 | site, extent | |  |
| `/timelines/4/phases/1/emergency/0` | [0,19) | 감염 초기 (발열 + 발적 + 농) | early_sign, co_occurrence | |  |
| `/timelines/4/phases/1/emergency/1` | [0,16) | 혈종 형성 (한쪽 급격 부종) | formation, restriction, speed | |  |
| `/timelines/4/phases/2/period` | [0,7) | Day 3-7 | period, time_range | |  |
| `/timelines/4/phases/2/label` | [0,3) | 회복기 | phase_label | |  |
| `/timelines/4/phases/2/normal/0` | [0,8) | 부종 점차 감소 | speed, change | |  |
| `/timelines/4/phases/2/normal/1` | [0,15) | 멍 황색 변화 (흡수 진행) | color_change, progress | |  |
| `/timelines/4/phases/2/normal/2` | [0,6) | 당김감 완화 | change | |  |
| `/timelines/4/phases/2/normal/3` | [0,8) | 입 움직임 개선 | function, change | |  |
| `/timelines/4/phases/2/abnormal/0` | [0,8) | 부종 감소 느림 | speed | |  |
| `/timelines/4/phases/2/abnormal/1` | [0,20) | 피부 표면 불규칙 (dimpling) | texture, mixed_script | |  |
| `/timelines/4/phases/2/caution/0` | [0,19) | 실 촉지/돌출 (피부 아래 만져짐) | detection, alt, location | |  |
| `/timelines/4/phases/2/caution/1` | [0,6) | 지속적 발열 | persistence | |  |
| `/timelines/4/phases/2/caution/2` | [0,6) | 심한 비대칭 | severity | |  |
| `/timelines/4/phases/2/emergency/0` | [0,13) | 실 노출 (피부 밖으로) | exposure, location | |  |
| `/timelines/4/phases/2/emergency/1` | [0,12) | 감염 (농/발열/발적) | gloss, alt | |  |
| `/timelines/4/phases/2/emergency/2` | [0,11) | 안면 신경 마비 지속 | persistence | |  |
| `/timelines/4/phases/3/period` | [0,8) | Day 7-14 | period, time_range | |  |
| `/timelines/4/phases/3/label` | [0,3) | 안정기 | phase_label | |  |
| `/timelines/4/phases/3/normal/0` | [0,11) | 부종/멍 대부분 소실 | alt, proportion_approx, resolution | |  |
| `/timelines/4/phases/3/normal/1` | [0,13) | 리프팅 효과 자연스러워짐 | quality, change | |  |
| `/timelines/4/phases/3/normal/2` | [0,10) | 일상생활 완전 복귀 | activity, degree | 「완전」 |
| `/timelines/4/phases/3/normal/3` | [0,9) | 콜라겐 생성 시작 | mechanism, onset | |  |
| `/timelines/4/phases/3/abnormal/0` | [0,10) | 경미한 비대칭 잔존 | severity, persistence | |  |
| `/timelines/4/phases/3/abnormal/1` | [0,15) | 미세한 dimpling 잔존 | degree, mixed_script, persistence | |  |
| `/timelines/4/phases/3/abnormal/2` | [0,7) | 간헐적 찌릿함 | frequency_pattern | 「간헐적」 = 반복 양상(빈도와 다름, 잠정) |
| `/timelines/4/phases/3/caution/0` | [0,10) | 실 이동/돌출 징후 | alt, early_sign | |  |
| `/timelines/4/phases/3/caution/1` | [0,6) | 지연성 감염 | delayed_onset | |  |
| `/timelines/4/phases/3/caution/2` | [0,6) | 비대칭 악화 | worsening | |  |
| `/timelines/4/phases/3/emergency/0` | [0,4) | 실 노출 | exposure | |  |
| `/timelines/4/phases/3/emergency/1` | [0,5) | 농양 형성 | formation | |  |
| `/timelines/4/phases/3/emergency/2` | [0,10) | 진행성 안면 비대칭 | progress, site | |  |
| `/timelines/4/phases/4/period` | [0,9) | Day 14-30 | period, time_range | |  |
| `/timelines/4/phases/4/label` | [0,6) | 최종 안정기 | phase_label | |  |
| `/timelines/4/phases/4/normal/0` | [0,12) | 최종 리프팅 결과 확인 | evaluation | |  |
| `/timelines/4/phases/4/normal/1` | [0,9) | 당김감 자연스러움 | quality | |  |
| `/timelines/4/phases/4/normal/2` | [0,13) | 콜라겐 리모델링 진행 중 | mechanism, progress | |  |
| `/timelines/4/phases/4/normal/3` | [0,12) | 재시술 판단 가능 시점 | retreatment_decision, possibility | |  |
| `/timelines/4/phases/4/abnormal/0` | [0,12) | 리프팅 효과 조기 감소 | timing, change | 「조기」 — 기준 기간 원문 없음 |
| `/timelines/4/phases/4/abnormal/1` | [0,7) | 경미한 비대칭 | severity | |  |
| `/timelines/4/phases/4/caution/0` | [0,13) | 실 이동 (리프팅 소실) | consequence_gloss | |  |
| `/timelines/4/phases/4/caution/1` | [0,9) | 만성 통증/불편감 | chronicity, alt | 「만성」 기간 정의 없음 |
| `/timelines/4/phases/4/emergency/0` | [0,9) | 지연성 감염/농양 | delayed_onset, alt | |  |
| `/timelines/4/phases/4/emergency/1` | [0,7) | 실 노출/돌출 | alt, exposure | |  |

## 4. 자동 후보 요약 (정규식 일치분만 — 전수 의미 수집 아님)

P-ADVICE 2, P-AFTER 1, P-ALT 11, P-APPROX 1, P-COMPARE 2, P-COURSE 37, P-DAY 6, P-DEGREE 11, P-DURING 2, P-FREQ 1, P-IF 4, P-LATIN 8, P-NEG 1, P-NUMUNIT 1, P-PAREN 17, P-POSSIB 2, P-SITE 11, P-SPEED 4, P-SYMBOL 2

전체 목록은 expressions.json (segment 필터).

## 5. 잠정 관찰

- **S05-O1** 「실 노출」 이 phases/2·3·4 emergency 에, 「실 이동/돌출」 이 phases/2·3·4 caution 에 반복된다. 같은 증상이 caution(촉지/돌출)·emergency(노출/돌출)에 함께 걸친다(phases/4: caution 「실 이동」, emergency 「실 노출/돌출」).
- **S05-O2** 기간 Day 0 / 1-3 / 3-7 / 7-14 / 14-30.

## 6. 미결 (이 구획)

| ID | 분류 | 위치 | 내용 |
|---|---|---|---|
| S05-Q1 | B | `/timelines/4/phases/4/abnormal/0` `/timelines/4/phases/4/caution/1` | 「조기」「만성」 의 기간 기준이 원문에 없다. |
| S05-Q2 | P | `/timelines/4/phases/2/caution/0` `/timelines/4/phases/4/emergency/1` | 「돌출」 이 caution·emergency 양쪽에 있어 등급을 가르는 기준(촉지 vs 노출)은 잠정. |

## 7. 형태소 — 알려진 오분절 (교정 안 함)

| Pointer | 구간 | 원시 토큰 | 판정/설명 | 영향 |
|---|---|---|---|---|
| `/timelines/4/phases/0/normal/0` | [12,15) | 과/NNG + 교정/NNG | K-GWA-NNG 접두 「과」 가 NNG 로 분석(다른 출현은 XPN) | 과도 단서 품사 불일치 |
| `/timelines/4/phases/1/abnormal/1` | [0,2) | 침/NNG + 자/NNG | K-CHIMJA 「침자」 가 침+자 로 분할 | 부위 표현 분할 |
| `/timelines/4/phases/1/caution/2` | [8,10) | 발/NNG + 적/XSN | K-BALJEOK 「발적」 이 발/NNG+적/XSN 으로 분할 | 사건 명사 손실(「-적」 접미 오인) |
| `/timelines/4/phases/2/normal/1` | [0,1) | 멍/MAG | K-MAG-NOUN 명사 「멍」 이 MAG(부사) | 사건 명사를 부사로 오태깅 — 명사 기준 탐색에서 누락 |
| `/timelines/4/phases/2/normal/1` | [2,4) | 황/NNG + 색/NNG | K-HWANGSAEK 「황색」 이 황+색 으로 분할 | 색 표현 분할 |
| `/timelines/4/phases/2/caution/0` | [2,4) | 촉/NNG + 지/NNG | K-CHOKJI 「촉지」 가 촉+지 로 분할 | 감지 방식 단서 손실 |
| `/timelines/4/phases/2/emergency/1` | [9,11) | 발/NNG + 적/XSN | K-BALJEOK 「발적」 이 발/NNG+적/XSN 으로 분할 | 사건 명사 손실(「-적」 접미 오인) |
| `/timelines/4/phases/3/normal/0` | [5,8) | 대/XPN + 부분/NNG | K-DAEBUBUN 「대부분」 이 대/XPN+부분/NNG 로 분할 | 근사·비율 단서 「대부분」 손실 |
| `/timelines/4/phases/3/emergency/1` | [0,2) | 농/NNG + 양/NNG | K-NONGYANG 「농양」 이 농+양 으로 분할 | 사건 명사 손실 |

