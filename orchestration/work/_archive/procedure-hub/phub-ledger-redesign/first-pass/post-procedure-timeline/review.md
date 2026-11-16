# post-procedure-timeline.json — 1차 조사 (읽기용 목차)

> 생성: build.py (재생성 시 이 파일도 다시 만들어진다). 수동 보완은 manual/ 에만 적는다.

## 상태

| 항목 | 상태 |
|---|---|
| **1차 범위 종료** | validation.md 참조(기계 검증 + 별도 읽기 검토 결과가 거기 있다) |
| **원장 전체 완료** | **아님** — 원문 부족 B·잠정 P·후속 F·원문 불일치 I 가 열려 있다(issues.md) |
| 전수 읽기 | 구획 11/11 직접 읽기(coverage.json direct_read=done) |
| 구조·값 수집 | 노드 796 · 말단 558 (문자열 558) · 중복 키 0 · 이스케이프 0 · 빈 컨테이너 0 |
| 형태소 | Kiwi 0.24.1 cong · 적용 536값 3078토큰 · 제외 22값(ID/코드) · 필드명 15종 제외(영문 식별자) · 알려진 오분절 서명 32개(규칙 ID 28종, 문맥 대조 후 등록) 76출현 · 출현별 추가 판정 0 · NNG/NNP 갈림 22출현 |
| 표현 | 값 전체 558 · 수동 586 · 자동 후보 1147(정규식 일치분만) |
| 원본 | `orchestration/work/phub-recommend/bronze/phub-ledger/post-procedure-timeline.json` · sha256 `d04c9fe494acd318d656f6dea6d19e33cb944a20440e312ca9bad41309c9742e` · 20081 bytes · 11823 codepoints · 줄바꿈 0 |

## 파일

| 파일 | 내용 |
|---|---|
| review-part-S00.md … S10.md | 구획별 모든 값(원본 컬럼명·자료형·원문 값·Pointer)과 분리된 잠정 관찰·수동 표현·미결 |
| source-map.json | 원본 식별·해시, 모든 노드(컨테이너 포함)의 Pointer·자료형·값·리터럴 구간(코드포인트/바이트)·키 리터럴 구간·소유 구획, 필드명 출현 |
| morphology.json | 분석기 설정, 적용 값별 토큰(표면형·품사·도구 lemma·구간·원문 대조), 제외 값과 사유, 필드명 제외, 알려진 오분절 |
| expressions.json | 값 전체 문맥 단위 + 수동 구절 + 정규식 후보(패턴 목록 포함), 잔여 토큰 점검표 |
| coverage.json | 구획 계획·소유 Pointer 집합·공유 문맥·읽기 상태·대응 문서 |
| issues.md | 미결(A·B·C·K·P·F·I) |
| validation.md | 검증 명령·결과·별도 읽기 검토 |
| progress.md | 재개 위치 |
| manual/ | 직접 읽기 기록(구획별 S*.txt, segmentation.txt, global-issues.txt) |
| build.py · verify.py · read_segment.py | 재생성 · 독립 검증 · 구획 원문 출력 |

## 컬럼 구성

원본 컬럼명(경로 패턴, 배열 인덱스 = `*`) 그대로. 예시는 첫 출현의 원문 값과 Pointer.

| 원본 컬럼명 / 경로 패턴 | 자료형 · 중첩 구조 | 출현 수 | 배열 길이 분포 | 빈 값 | 필수/선택 | 원문 예시 | 예시 위치 |
|---|---|---|---|---|---|---|---|
| `(root)` | object×1 · object{version, updated, consensus_method, reaction_levels, timelines} | 1 |  | 0 | 루트 | (컨테이너) | `(root)` |
| `/version` | string×1 · string | 1 |  | 0 | 모든 부모에 있음 | 1.1 | `/version` |
| `/updated` | string×1 · string | 1 |  | 0 | 모든 부모에 있음 | 2026-07-11 | `/updated` |
| `/consensus_method` | string×1 · string | 1 |  | 0 | 모든 부모에 있음 | Perplexity(리서치) + Gemini(분석) + Claude(교과서 종합) 3-AI 컨센서스 | `/consensus_method` |
| `/reaction_levels` | object×1 · object{normal, abnormal, caution, emergency} | 1 |  | 0 | 모든 부모에 있음 | (컨테이너) | `/reaction_levels` |
| `/reaction_levels/normal` | string×1 · string | 1 |  | 0 | 모든 부모에 있음 | 정상 반응 -- 예상 범위, 조치 불필요 | `/reaction_levels/normal` |
| `/reaction_levels/abnormal` | string×1 · string | 1 |  | 0 | 모든 부모에 있음 | 이상 반응 -- 모니터링 필요, 경과 관찰 | `/reaction_levels/abnormal` |
| `/reaction_levels/caution` | string×1 · string | 1 |  | 0 | 모든 부모에 있음 | 주의 반응 -- 24-48시간 내 클리닉 연락 | `/reaction_levels/caution` |
| `/reaction_levels/emergency` | string×1 · string | 1 |  | 0 | 모든 부모에 있음 | 응급 반응 -- 즉시 응급실/클리닉 | `/reaction_levels/emergency` |
| `/timelines` | array×1 · array | 1 | 10:1 | 0 | 모든 부모에 있음 | (컨테이너) | `/timelines` |
| `/timelines/*` | object×10 · object{id, category, name, phases} | 10 |  | 0 | 배열 원소 | (컨테이너) | `/timelines/0` |
| `/timelines/*/id` | string×10 · string | 10 |  | 0 | 모든 부모에 있음 | botox | `/timelines/0/id` |
| `/timelines/*/category` | string×10 · string | 10 |  | 0 | 모든 부모에 있음 | M1 | `/timelines/0/category` |
| `/timelines/*/name` | string×10 · string | 10 |  | 0 | 모든 부모에 있음 | 보톡스 | `/timelines/0/name` |
| `/timelines/*/phases` | array×10 · array | 10 | 3:2, 4:3, 5:5 | 0 | 모든 부모에 있음 | (컨테이너) | `/timelines/0/phases` |
| `/timelines/*/phases/*` | object×43 · object{period, label, normal, abnormal, caution, emergency} | 43 |  | 0 | 배열 원소 | (컨테이너) | `/timelines/0/phases/0` |
| `/timelines/*/phases/*/period` | string×43 · string | 43 |  | 0 | 모든 부모에 있음 | Day 0 | `/timelines/0/phases/0/period` |
| `/timelines/*/phases/*/label` | string×43 · string | 43 |  | 0 | 모든 부모에 있음 | 시술 당일 | `/timelines/0/phases/0/label` |
| `/timelines/*/phases/*/normal` | array×43 · array | 43 | 3:10, 4:33 | 0 | 모든 부모에 있음 | (컨테이너) | `/timelines/0/phases/0/normal` |
| `/timelines/*/phases/*/normal/*` | string×162 · string | 162 |  | 0 | 배열 원소 | 주사 부위 작은 돌기/발적 (15-60분 내 소실) | `/timelines/0/phases/0/normal/0` |
| `/timelines/*/phases/*/abnormal` | array×43 · array | 43 | 1:1, 2:41, 3:1 | 0 | 모든 부모에 있음 | (컨테이너) | `/timelines/0/phases/0/abnormal` |
| `/timelines/*/phases/*/abnormal/*` | string×86 · string | 86 |  | 0 | 배열 원소 | 경미한 멍 (혈관 천자 시) | `/timelines/0/phases/0/abnormal/0` |
| `/timelines/*/phases/*/caution` | array×43 · array | 43 | 1:1, 2:34, 3:8 | 0 | 모든 부모에 있음 | (컨테이너) | `/timelines/0/phases/0/caution` |
| `/timelines/*/phases/*/caution/*` | string×93 · string | 93 |  | 0 | 배열 원소 | 1시간 이상 지속되는 발적/부종 | `/timelines/0/phases/0/caution/0` |
| `/timelines/*/phases/*/emergency` | array×43 · array | 43 | 1:2, 2:33, 3:6, 4:2 | 0 | 모든 부모에 있음 | (컨테이너) | `/timelines/0/phases/0/emergency` |
| `/timelines/*/phases/*/emergency/*` | string×94 · string | 94 |  | 0 | 배열 원소 | 심한 두드러기/호흡곤란 (아나필락시스, 극히 드묾) | `/timelines/0/phases/0/emergency/0` |

## 구획 목차

| 구획 | 범위 | 소유 노드 / 말단 | 직접 읽기 | 문서 |
|---|---|---|---|---|
| S00 | 상위 메타데이터 (version·updated·consensus_method·reaction_levels) + 루트·timelines 배열 컨테이너 | 10 / 7 | done | [review-part-S00.md](./review-part-S00.md) |
| S01 | /timelines/0 botox (보톡스) | 83 / 56 | done | [review-part-S01.md](./review-part-S01.md) |
| S02 | /timelines/1 ha-filler (HA 필러) | 92 / 65 | done | [review-part-S02.md](./review-part-S02.md) |
| S03 | /timelines/2 hifu-rf (HIFU/RF 리프팅) | 72 / 50 | done | [review-part-S03.md](./review-part-S03.md) |
| S04 | /timelines/3 fractional-co2 (프락셔널 CO2 레이저) | 91 / 64 | done | [review-part-S04.md](./review-part-S04.md) |
| S05 | /timelines/4 thread-lift (실리프팅) | 96 / 69 | done | [review-part-S05.md](./review-part-S05.md) |
| S06 | /timelines/5 dca-injection (DCA 지방분해 주사) | 92 / 65 | done | [review-part-S06.md](./review-part-S06.md) |
| S07 | /timelines/6 needle-rf (니들RF (미세침 고주파)) | 56 / 39 | done | [review-part-S07.md](./review-part-S07.md) |
| S08 | /timelines/7 skin-booster (스킨부스터) | 56 / 39 | done | [review-part-S08.md](./review-part-S08.md) |
| S09 | /timelines/8 biostimulator (바이오스티뮬레이터/콜라겐부스터) | 72 / 50 | done | [review-part-S09.md](./review-part-S09.md) |
| S10 | /timelines/9 chemical-peel-mid (케미컬 필링 (중간 깊이)) | 76 / 54 | done | [review-part-S10.md](./review-part-S10.md) |

## 시간·경과·관리·대응·재시술 표현 색인 (직접 읽기 구절, 역할은 잠정)

기준 시점·발현·피크·지속·소실/회복·지연·관리·응급 대응 시한·재시술 관련 수동 구절 전부. 「소속 period」 는 원문 구조상 그 값이 들어 있는 기간이며, 값 속 시간의 기준 시점은 대부분 원문에 없다(issues G-B2). 역할 이름은 탐색 관점이지 확정 분류가 아니다.

| Pointer | 소속 period | 원본 컬럼명 | 원문 구절 | 잠정 역할 |
|---|---|---|---|---|
| `/reaction_levels/caution` | - | `caution` | 주의 반응 -- 24-48시간 내 클리닉 연락 | action_time, time_range |
| `/reaction_levels/emergency` | - | `emergency` | 응급 반응 -- 즉시 응급실/클리닉 | action_time |
| `/timelines/0/phases/0/period` | Day 0 | `period` | Day 0 | period |
| `/timelines/0/phases/0/label` | Day 0 | `label` | 시술 당일 | reference_point |
| `/timelines/0/phases/0/normal/0` | Day 0 | `normal` | (15-60분 내 소실) | resolution, time_range |
| `/timelines/0/phases/0/abnormal/0` | Day 0 | `abnormal` | (혈관 천자 시) | condition |
| `/timelines/0/phases/0/caution/0` | Day 0 | `caution` | 1시간 이상 지속되는 발적/부종 | duration_threshold, persistence |
| `/timelines/0/phases/1/period` | Day 1-3 | `period` | Day 1-3 | period |
| `/timelines/0/phases/1/normal/0` | Day 1-3 | `normal` | 미세한 근육 무거움/당김감 시작 | onset |
| `/timelines/0/phases/1/normal/0` | Day 1-3 | `normal` | (Day 2-3) | onset_time, time_range |
| `/timelines/0/phases/1/normal/1` | Day 1-3 | `normal` | 효과 아직 안 보임 (정상) | temporal |
| `/timelines/0/phases/1/normal/2` | Day 1-3 | `normal` | (1-2일 소실) | resolution, time_range |
| `/timelines/0/phases/1/abnormal/0` | Day 1-3 | `abnormal` | (수일 내 소실, 보라색→황색 변화) | approx_time, resolution |
| `/timelines/0/phases/1/abnormal/1` | Day 1-3 | `abnormal` | 경미한 두통 (수시간 내 소실) | resolution |
| `/timelines/0/phases/1/caution/0` | Day 1-3 | `caution` | 지속되는 심한 두통 (24시간 이상) | duration_threshold, persistence |
| `/timelines/0/phases/2/period` | Day 3-7 | `period` | Day 3-7 | period |
| `/timelines/0/phases/2/label` | Day 3-7 | `label` | 효과 발현기 | onset |
| `/timelines/0/phases/2/normal/1` | Day 3-7 | `normal` | 표정 변화 시작 (미세) | onset |
| `/timelines/0/phases/2/abnormal/0` | Day 3-7 | `abnormal` | 경미한 비대칭 (좌우 효과 속도 차이) | speed |
| `/timelines/0/phases/3/period` | Day 7-14 | `period` | Day 7-14 | period |
| `/timelines/0/phases/3/normal/0` | Day 7-14 | `normal` | 효과 본격적으로 나타남 (Day 7-10) | onset, onset_time |
| `/timelines/0/phases/3/normal/1` | Day 7-14 | `normal` | Day 14 최대 효과 도달 | peak_time |
| `/timelines/0/phases/4/period` | Day 14-30 | `period` | Day 14-30 | period |
| `/timelines/0/phases/4/normal/2` | Day 14-30 | `normal` | 재시술 필요 여부 판단 가능 시점 | retreatment_decision |
| `/timelines/0/phases/4/abnormal/0` | Day 14-30 | `abnormal` | Day 14에도 효과 부족 | time_anchor |
| `/timelines/0/phases/4/abnormal/0` | Day 14-30 | `abnormal` | (터치업 고려) | retreatment |
| `/timelines/1/phases/0/normal/0` | Day 0 | `normal` | 즉각적인 볼륨 증가 | onset_speed |
| `/timelines/1/phases/0/abnormal/0` | Day 0 | `abnormal` | (혈관 천자 시, 흔함) | condition |
| `/timelines/1/phases/0/emergency/0` | Day 0 | `emergency` | ** 혈관폐색 (blanching/하얗게 변함) -- 골든타임 Day 0-1 ** | action_window |
| `/timelines/1/phases/0/emergency/0` | Day 0 | `emergency` | 골든타임 Day 0-1 | action_window, time_range |
| `/timelines/1/phases/1/period` | Day 1-2 | `period` | Day 1-2 | period |
| `/timelines/1/phases/1/normal/0` | Day 1-2 | `normal` | 부종 피크 (Day 2가 가장 심함, 정상) | peak, peak_time |
| `/timelines/1/phases/1/caution/0` | Day 1-2 | `caution` | 지속적 심한 통증 (진통제 미반응) | persistence |
| `/timelines/1/phases/1/caution/1` | Day 1-2 | `caution` | 부종 범위 급격 확대 | speed |
| `/timelines/1/phases/1/emergency/0` | Day 1-2 | `emergency` | ** 지연성 혈관폐색 -- 여전히 골든타임 ** | action_window, delayed_onset |
| `/timelines/1/phases/1/emergency/3` | Day 1-2 | `emergency` | 고열 + 급격한 부종 (감염) | speed |
| `/timelines/1/phases/2/period` | Day 3-5 | `period` | Day 3-5 | period |
| `/timelines/1/phases/2/normal/0` | Day 3-5 | `normal` | 부종 점차 감소 | speed |
| `/timelines/1/phases/2/abnormal/0` | Day 3-5 | `abnormal` | 부종 소실 느린 편 | speed |
| `/timelines/1/phases/3/period` | Day 5-7 | `period` | Day 5-7 | period |
| `/timelines/1/phases/3/normal/0` | Day 5-7 | `normal` | 부종 대부분 소실 | resolution |
| `/timelines/1/phases/3/normal/1` | Day 5-7 | `normal` | 멍 거의 소실 | resolution |
| `/timelines/1/phases/3/abnormal/0` | Day 5-7 | `abnormal` | 미세 결절 촉지 (마사지로 개선 가능) | management |
| `/timelines/1/phases/3/caution/1` | Day 5-7 | `caution` | 지연성 부종 재발 | delayed_onset |
| `/timelines/1/phases/3/emergency/0` | Day 5-7 | `emergency` | 지연성 감염 (발열/농/발적) | delayed_onset |
| `/timelines/1/phases/4/period` | Day 8-14 | `period` | Day 8-14 | period, time_range |
| `/timelines/1/phases/4/caution/0` | Day 8-14 | `caution` | 지연성 과민반응 (부종/발적 재발) | delayed_onset, recurrence |
| `/timelines/1/phases/4/emergency/0` | Day 8-14 | `emergency` | 지연성 감염/농양 | delayed_onset |
| `/timelines/2/phases/0/normal/0` | Day 0 | `normal` | 홍반/온감 (수시간 내 소실) | resolution |
| `/timelines/2/phases/0/abnormal/0` | Day 0 | `abnormal` | 뚜렷한 부종 (24시간 이상) | duration_threshold |
| `/timelines/2/phases/1/period` | Day 1-3 | `period` | Day 1-3 | period |
| `/timelines/2/phases/1/normal/2` | Day 1-3 | `normal` | 미세한 타이트닝 느낌 시작 | onset |
| `/timelines/2/phases/1/normal/3` | Day 1-3 | `normal` | 일상생활 가능 | activity |
| `/timelines/2/phases/1/abnormal/0` | Day 1-3 | `abnormal` | 지속 홍반 (3일 이상) | persistence |
| `/timelines/2/phases/2/period` | Day 3-7 | `period` | Day 3-7 | period |
| `/timelines/2/phases/2/normal/1` | Day 3-7 | `normal` | 피부 질감 개선 시작 | onset |
| `/timelines/2/phases/2/normal/2` | Day 3-7 | `normal` | 저림/감각변화 점차 정상화 | speed |
| `/timelines/2/phases/2/abnormal/1` | Day 3-7 | `abnormal` | 불편감 1주 이상 지속 | duration_threshold, persistence |
| `/timelines/2/phases/2/emergency/1` | Day 3-7 | `emergency` | 화상 반흔 형성 시작 | onset |
| `/timelines/2/phases/3/period` | Day 7-30 | `period` | Day 7-30 | period |
| `/timelines/2/phases/3/normal/0` | Day 7-30 | `normal` | 점진적 리프팅 효과 발현 (2-4주) | onset, speed, time_range |
| `/timelines/2/phases/3/normal/2` | Day 7-30 | `normal` | 저림/감각변화 완전 소실 (2-4주) | resolution, time_range |
| `/timelines/2/phases/3/abnormal/1` | Day 7-30 | `abnormal` | 일부 감각 변화 잔존 | persistence |
| `/timelines/2/phases/3/emergency/0` | Day 7-30 | `emergency` | 진행성 안면 함몰 (지방위축 -- HIFU 심부 에너지 과다 시) | condition |
| `/timelines/3/phases/1/period` | Day 1-3 | `period` | Day 1-3 | period |
| `/timelines/3/phases/1/normal/0` | Day 1-3 | `normal` | Day 1: 삼출액 지속, 홍반 심함 | persistence, time_anchor |
| `/timelines/3/phases/1/normal/1` | Day 1-3 | `normal` | Day 2-3: 가피(딱지) 형성 시작 | time_anchor, time_range |
| `/timelines/3/phases/1/normal/2` | Day 1-3 | `normal` | 부종 피크 (Day 1-2) 후 점차 감소 | peak, peak_time, sequence, speed |
| `/timelines/3/phases/1/abnormal/0` | Day 1-3 | `abnormal` | Day 3에도 삼출 지속 | time_anchor |
| `/timelines/3/phases/1/emergency/1` | Day 1-3 | `emergency` | 헤르페스 재활성화 (수포 군집) | recurrence |
| `/timelines/3/phases/2/period` | Day 3-5 | `period` | Day 3-5 | period |
| `/timelines/3/phases/2/normal/1` | Day 3-5 | `normal` | 가피 가장자리부터 벗겨짐 시작 | onset, sequence |
| `/timelines/3/phases/2/normal/2` | Day 3-5 | `normal` | 홍반 점차 감소 | speed |
| `/timelines/3/phases/2/abnormal/1` | Day 3-5 | `abnormal` | 가피 조기 탈락 (자연 탈락 전 뜯음) | sequence |
| `/timelines/3/phases/3/period` | Day 5-7 | `period` | Day 5-7 | period |
| `/timelines/3/phases/3/normal/1` | Day 5-7 | `normal` | Day 7-10: 재상피화 완료 | completion, time_anchor, time_range |
| `/timelines/3/phases/3/normal/3` | Day 5-7 | `normal` | 홍반 지속 (정상, 수주 소요) | approx_time, duration, persistence |
| `/timelines/3/phases/3/abnormal/0` | Day 5-7 | `abnormal` | Day 7에도 가피 잔존 | time_anchor |
| `/timelines/3/phases/3/caution/0` | Day 5-7 | `caution` | 재상피화 지연 (10일 이상) | delay, duration_threshold |
| `/timelines/3/phases/4/period` | Day 7-14 | `period` | Day 7-14 | period |
| `/timelines/3/phases/4/normal/0` | Day 7-14 | `normal` | 재상피화 완료 | completion |
| `/timelines/3/phases/4/normal/1` | Day 7-14 | `normal` | 분홍빛 홍반 지속 (정상, 1-3개월 소요) | duration, persistence, time_range |
| `/timelines/3/phases/4/normal/2` | Day 7-14 | `normal` | 피부 질감 개선 시작 | onset |
| `/timelines/3/phases/4/normal/3` | Day 7-14 | `normal` | 메이크업 가능 (재상피화 후) | activity, condition, sequence |
| `/timelines/3/phases/4/abnormal/0` | Day 7-14 | `abnormal` | 지속적 홍반 (예상보다 진함) | persistence |
| `/timelines/3/phases/4/abnormal/1` | Day 7-14 | `abnormal` | 색소침착 시작 (PIH) | onset |
| `/timelines/3/phases/4/caution/0` | Day 7-14 | `caution` | PIH (염증 후 과색소침착) 진행 | sequence |
| `/timelines/4/phases/0/normal/0` | Day 0 | `normal` | 즉각적 리프팅 효과 (과교정 상태) | onset_speed |
| `/timelines/4/phases/1/period` | Day 1-3 | `period` | Day 1-3 | period |
| `/timelines/4/phases/1/normal/0` | Day 1-3 | `normal` | 부종 피크 (Day 1-2) | peak |
| `/timelines/4/phases/2/period` | Day 3-7 | `period` | Day 3-7 | period |
| `/timelines/4/phases/2/normal/0` | Day 3-7 | `normal` | 부종 점차 감소 | speed |
| `/timelines/4/phases/3/period` | Day 7-14 | `period` | Day 7-14 | period |
| `/timelines/4/phases/3/normal/2` | Day 7-14 | `normal` | 일상생활 완전 복귀 | activity |
| `/timelines/4/phases/4/period` | Day 14-30 | `period` | Day 14-30 | period |
| `/timelines/4/phases/4/normal/3` | Day 14-30 | `normal` | 재시술 판단 가능 시점 | retreatment_decision |
| `/timelines/4/phases/4/caution/1` | Day 14-30 | `caution` | 만성 통증/불편감 | chronicity |
| `/timelines/4/phases/4/emergency/0` | Day 14-30 | `emergency` | 지연성 감염/농양 | delayed_onset |
| `/timelines/5/phases/0/normal/0` | Day 0 | `normal` | (시술 중~직후) | reference_point, time_range |
| `/timelines/5/phases/0/normal/1` | Day 0 | `normal` | 즉각적 부종 시작 | onset_speed |
| `/timelines/5/phases/0/caution/0` | Day 0 | `caution` | 비정상적 심한 통증 (수시간 지속) | duration |
| `/timelines/5/phases/1/period` | Day 1-3 | `period` | Day 1-3 | period |
| `/timelines/5/phases/1/normal/2` | Day 1-3 | `normal` | 통증 지속 (진통제 복용 가능) | management, persistence |
| `/timelines/5/phases/1/normal/3` | Day 1-3 | `normal` | 감각 이상 지속 (저림/무감각) | persistence |
| `/timelines/5/phases/1/abnormal/1` | Day 1-3 | `abnormal` | 연하 시 불편감 | condition |
| `/timelines/5/phases/2/period` | Day 3-7 | `period` | Day 3-7 | period |
| `/timelines/5/phases/2/normal/0` | Day 3-7 | `normal` | 부종 서서히 감소 시작 | onset, speed |
| `/timelines/5/phases/2/normal/1` | Day 3-7 | `normal` | 경결감 지속 (정상) | persistence |
| `/timelines/5/phases/2/normal/3` | Day 3-7 | `normal` | 감각 이상 지속 가능 (정상, 수주 소요) | approx_time, persistence |
| `/timelines/5/phases/3/period` | Day 7-14 | `period` | Day 7-14 | period |
| `/timelines/5/phases/3/normal/0` | Day 7-14 | `normal` | 부종 상당 부분 소실 | resolution |
| `/timelines/5/phases/3/normal/1` | Day 7-14 | `normal` | 경결감 점차 감소 | speed |
| `/timelines/5/phases/3/normal/2` | Day 7-14 | `normal` | 감각 정상화 시작 | recovery |
| `/timelines/5/phases/3/normal/3` | Day 7-14 | `normal` | 지방 분해 효과 아직 미미 (정상) | temporal |
| `/timelines/5/phases/3/abnormal/0` | Day 7-14 | `abnormal` | 대개 정상 염증반응으로 수 주 내 자연 소실 | approx_time, resolution |
| `/timelines/5/phases/3/abnormal/0` | Day 7-14 | `abnormal` | 데옥시콜산은 임의 마사지가 표적외 확산·신경손상·괴사 위험이 있어 금기 | avoidance, management |
| `/timelines/5/phases/3/abnormal/0` | Day 7-14 | `abnormal` | 임의 마사지 | management |
| `/timelines/5/phases/3/abnormal/0` | Day 7-14 | `abnormal` | 지속·악화 시 시술 병원 문의 | condition |
| `/timelines/5/phases/3/emergency/0` | Day 7-14 | `emergency` | 하악변연신경 손상 지속 (4주 이상 시 영구 손상 우려) | condition, duration_threshold, persistence |
| `/timelines/5/phases/4/period` | Day 14-30 | `period` | Day 14-30 | period |
| `/timelines/5/phases/4/label` | Day 14-30 | `label` | 효과 발현기 | onset |
| `/timelines/5/phases/4/normal/0` | Day 14-30 | `normal` | 지방 분해 효과 서서히 발현 | speed |
| `/timelines/5/phases/4/normal/1` | Day 14-30 | `normal` | 턱선 개선 시작 | onset |
| `/timelines/5/phases/4/normal/3` | Day 14-30 | `normal` | 감각 정상화 (대부분) | recovery |
| `/timelines/5/phases/4/abnormal/0` | Day 14-30 | `abnormal` | 효과 미미 (추가 세션 필요 가능) | retreatment |
| `/timelines/5/phases/4/caution/1` | Day 14-30 | `caution` | 만성 감각 이상 (6주 이상) | chronicity, duration_threshold |
| `/timelines/5/phases/4/emergency/0` | Day 14-30 | `emergency` | 영구 신경 손상 징후 | permanence |
| `/timelines/6/phases/0/normal/0` | Day 0 | `normal` | 홍반/발적 (수시간 지속) | duration |
| `/timelines/6/phases/1/period` | Day 1-3 | `period` | Day 1-3 | period |
| `/timelines/6/phases/1/normal/0` | Day 1-3 | `normal` | 홍반 점차 감소 (Day 1-2 소실) | resolution, speed |
| `/timelines/6/phases/1/abnormal/0` | Day 1-3 | `abnormal` | 홍반 3일 이상 지속 | duration_threshold |
| `/timelines/6/phases/2/period` | Day 3-7 | `period` | Day 3-7 | period |
| `/timelines/6/phases/2/normal/2` | Day 3-7 | `normal` | 메이크업 가능 | activity |
| `/timelines/7/phases/0/abnormal/0` | Day 0 | `abnormal` | 멍 (혈관 천자 시) | condition |
| `/timelines/7/phases/1/period` | Day 1-3 | `period` | Day 1-3 | period |
| `/timelines/7/phases/1/normal/0` | Day 1-3 | `normal` | 돌기 24-48시간 내 소실 | resolution |
| `/timelines/7/phases/1/normal/1` | Day 1-3 | `normal` | 멍 있으면 변색 진행 | condition |
| `/timelines/7/phases/1/abnormal/0` | Day 1-3 | `abnormal` | 돌기 48시간 이상 지속 | duration_threshold |
| `/timelines/7/phases/1/caution/0` | Day 1-3 | `caution` | 돌기 72시간 이상 지속 (결절 가능성) | duration_threshold, persistence |
| `/timelines/7/phases/2/period` | Day 3-7 | `period` | Day 3-7 | period |
| `/timelines/7/phases/2/normal/2` | Day 3-7 | `normal` | 모든 시술 흔적 소실 | resolution |
| `/timelines/7/phases/2/abnormal/0` | Day 3-7 | `abnormal` | 잔여 결절 촉지 | persistence |
| `/timelines/7/phases/2/caution/0` | Day 3-7 | `caution` | 결절 지속/커짐 | persistence |
| `/timelines/8/phases/0/normal/0` | Day 0 | `normal` | 즉각적 볼륨 (희석액에 의한 것, 수일 내 흡수됨) | approx_time, onset_speed, resolution |
| `/timelines/8/phases/1/period` | Day 1-7 | `period` | Day 1-7 | period, time_range |
| `/timelines/8/phases/1/normal/0` | Day 1-7 | `normal` | Day 2-3: 볼륨 감소 (희석액 흡수, 정상) | time_anchor, time_range |
| `/timelines/8/phases/1/normal/3` | Day 1-7 | `normal` | 시술 부위 부드러운 스무딩 | management |
| `/timelines/8/phases/1/abnormal/0` | Day 1-7 | `abnormal` | 자가 마사지로 해결할 대상이 아님 | avoidance, management |
| `/timelines/8/phases/2/period` | Day 7-30 | `period` | Day 7-30 | period |
| `/timelines/8/phases/2/normal/0` | Day 7-30 | `normal` | 볼륨 최저점 (희석액 완전 흡수) | trough |
| `/timelines/8/phases/2/normal/1` | Day 7-30 | `normal` | 눈에 보이는 변화 아직 없음 (정상) | temporal |
| `/timelines/8/phases/2/normal/3` | Day 7-30 | `normal` | 점진적 개선 시작 (3-4주) | onset, speed |
| `/timelines/8/phases/3/period` | Day 30-90 | `period` | Day 30-90 | period, time_range |
| `/timelines/8/phases/3/normal/0` | Day 30-90 | `normal` | 콜라겐 볼륨 점진적 증가 | speed |
| `/timelines/8/phases/3/normal/3` | Day 30-90 | `normal` | 최종 효과 판단 시점 (8-12주) | evaluation_time |
| `/timelines/8/phases/3/abnormal/0` | Day 30-90 | `abnormal` | 효과 미미 (추가 세션 필요) | retreatment |
| `/timelines/8/phases/3/emergency/0` | Day 30-90 | `emergency` | 육아종 (수개월 후에도 발생 가능) | approx_time, onset_time, sequence |
| `/timelines/9/phases/0/normal/0` | Day 0 | `normal` | 시술 중 작열감/따끔 | reference_point |
| `/timelines/9/phases/0/normal/0` | Day 0 | `normal` | (TCA 도포 시) | condition |
| `/timelines/9/phases/0/normal/1` | Day 0 | `normal` | 즉각적 홍반/발적 | onset_speed |
| `/timelines/9/phases/0/normal/3` | Day 0 | `normal` | 시술 후 열감/조임감 | reference_point, sequence |
| `/timelines/9/phases/1/period` | Day 1-3 | `period` | Day 1-3 | period |
| `/timelines/9/phases/1/normal/1` | Day 1-3 | `normal` | 피부 갈색 변화 시작 (가피 형성) | onset |
| `/timelines/9/phases/1/normal/3` | Day 1-3 | `normal` | 세안/보습 주의 기간 | caution_period, management |
| `/timelines/9/phases/1/emergency/1` | Day 1-3 | `emergency` | 헤르페스 재활성화 (수포 군집) | recurrence |
| `/timelines/9/phases/2/period` | Day 3-7 | `period` | Day 3-7 | period |
| `/timelines/9/phases/2/normal/0` | Day 3-7 | `normal` | Day 3-4: 각질/가피 벗겨짐 시작 | time_anchor, time_range |
| `/timelines/9/phases/2/normal/3` | Day 3-7 | `normal` | (강제 제거 금지) | avoidance, management |
| `/timelines/9/phases/2/caution/0` | Day 3-7 | `caution` | 감염 (필링 중 감염 취약) | reference_point |
| `/timelines/9/phases/2/emergency/1` | Day 3-7 | `emergency` | 반흔 형성 시작 | onset |
| `/timelines/9/phases/3/period` | Day 7-14 | `period` | Day 7-14 | period |
| `/timelines/9/phases/3/normal/0` | Day 7-14 | `normal` | Day 7-10: 새 피부 형성 완료 | time_anchor, time_range |
| `/timelines/9/phases/3/normal/1` | Day 7-14 | `normal` | 분홍빛 홍반 지속 (정상, 수주-수개월 소요) | approx_time, duration, persistence, time_range |
| `/timelines/9/phases/3/normal/2` | Day 7-14 | `normal` | 메이크업 가능 (재상피화 후) | activity, condition |
| `/timelines/9/phases/3/normal/3` | Day 7-14 | `normal` | 자외선 차단 필수 기간 | management, obligation |
| `/timelines/9/phases/3/abnormal/0` | Day 7-14 | `abnormal` | 지속적 깊은 홍반 | persistence |
| `/timelines/9/phases/3/caution/1` | Day 7-14 | `caution` | 재상피화 지연 (10일 이상) | delay |

## 원장 전체에 걸친 관찰(잠정)

원문 값은 각 구획 문서에 있다. 아래는 근거 위치를 붙인 잠정 관찰이며 의미 확정이 아니다.

- **G-O1** 모든 타임라인이 Day 0(label 「시술 당일」)에서 시작한다. period 는 「Day N」 또는 「Day N-M」 형태이며 단위 Day 는 영문이다. 기간 수는 3~5개, 마지막 기간 끝은 Day 7(needle-rf·skin-booster)·14(ha-filler)·30·90(biostimulator)으로 다르다. — 근거: `/timelines/0/phases/0/period`, `/timelines/1/phases/4/period`, `/timelines/8/phases/3/period`
- **G-O2** 모든 phase 객체가 period·label·normal·abnormal·caution·emergency 6키를 같은 순서로 갖고, 네 등급 배열은 모두 길이 ≥1 이다(빈 배열 0). 등급 키 이름은 /reaction_levels 의 키와 같다. — 근거: `/reaction_levels`, `/timelines/0/phases/0`
- **G-O3** 「발열 (37.5도 이상)」 이 다섯 타임라인 caution 에 같은 문자열로 나온다. 같은 문자열이라도 소속 시술·기간이 다르므로 출현별로 보존한다. — 근거: `/timelines/1/phases/2/caution/1`, `/timelines/3/phases/1/caution/1`, `/timelines/4/phases/1/caution/0`, `/timelines/5/phases/1/caution/1`, `/timelines/9/phases/1/caution/1`
- **G-O4** 재시술 관련 원문은 「판단(가능) 시점」·「고려」·「추가 세션 필요(가능)」 뿐이다. 재시술 최소/권장 간격 수치는 원장 어디에도 없다. — 근거: `/timelines/0/phases/4/normal/2`, `/timelines/1/phases/4/normal/2`, `/timelines/2/phases/3/abnormal/0`, `/timelines/4/phases/4/normal/3`, `/timelines/5/phases/4/abnormal/0`, `/timelines/8/phases/3/abnormal/0`, `/timelines/8/phases/3/normal/3`
- **G-O5** 관리·활동 재개 표현(메이크업 가능, 일상생활 가능/복귀, 세안/보습 주의 기간, 자외선 차단 필수 기간)은 normal 배열 안에 증상과 섞여 있다. 별도 필드가 없다. — 근거: `/timelines/3/phases/4/normal/3`, `/timelines/6/phases/2/normal/2`, `/timelines/9/phases/3/normal/2`, `/timelines/9/phases/3/normal/3`, `/timelines/9/phases/1/normal/3`, `/timelines/2/phases/1/normal/3`, `/timelines/4/phases/3/normal/2`
- **G-O6** 회피·금기·비권고 표현: 임의 마사지 금기(dca), 자가 마사지로 해결할 대상이 아님·스무딩 선택(biostimulator), 강제 제거 금지(chemical-peel). 반대로 ha-filler 는 「마사지로 개선 가능」(/timelines/1/phases/3/abnormal/0). 마사지에 대한 원문 방향이 시술마다 다르다. — 근거: `/timelines/5/phases/3/abnormal/0`, `/timelines/8/phases/1/abnormal/0`, `/timelines/8/phases/1/normal/3`, `/timelines/9/phases/2/normal/3`
- **G-O7** 구분 기호가 섞여 있다: ASCII 「--」(reaction_levels·여러 값), EM DASH 「—」(dca·biostimulator 2값), 「**」 강조(ha-filler 2값), 「→」(색 변화), 「~」(시술 중~직후), 「+」(동반), 「/」(대안·병기), 「·」(나열). — 근거: `/timelines/1/phases/0/emergency/0`, `/timelines/5/phases/3/abnormal/0`, `/timelines/8/phases/1/normal/3`

