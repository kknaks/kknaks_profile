# treatment-sequence.json — 미결 기록 (1차)

> 분류: **A** 추출 처리(에이전트가 해결·표시) · **B** 원문 정보 부족 · **C** 원문 내 불일치(후속 비교·판단 대상) · **D** 후속 의미 조사 · **E** 사용자 결정 필요.
> 원문 보존만으로 닫은 항목은 없다. B·C·D 는 모두 **열림**이다. 임상 사실 여부는 판단하지 않았다.

## 요약

| 분류 | 건수 | 상태 |
|---|---|---|
| A1 추출 오류(규칙) | 5 | 수정·재검증됨 |
| A2 알려진 형태소 오분절 | 69출현 | 표시됨(교정 아님) — 한계로 남김 |
| A3 알려진 표현 오탐 | 19출현 | 표시됨(삭제 안 함) |
| B 원문 정보 부족 | 10 | 열림 |
| C 원문 내 불일치 | 8 | 열림 — 관찰 유지. C1·C3·C5·C6 은 후속 의미 조사·원장 간 비교 과제(§E) |
| D 후속 의미 조사 | 8 | 열림, 시작 안 함 |
| E 사용자 선택 대기 | 0 | 근거는 §E |

## A. 추출 처리

### A1. 에이전트가 고친 추출 오류 (모두 반영 후 build·verify 재실행 통과)

| # | 무엇이 틀렸나 | 영향 | 처리 |
|---|---|---|---|
| A1-1 | 절 분할이 `)` 뒤 공백에서도 잘라 `/principles/5`(「채널 오픈(…)」/「후 도포는…」), `/incompatible_same_day/4/reason`·`/minimum_intervals/0/reason`(「고온(>55°C)」/「노출 시…」), `/principles/8`, `/sequence_order/5/reason`, `/minimum_intervals/3/to`, `/common_combos/6/note` 의 한 문장을 둘로 나눴다 | 조건과 결과가 다른 절로 갈라짐 | `.` 뒤 공백·` — `·`; ` 만 경계로 사용 |
| A1-2 | `; ` 분할이 괄호 안 인용(「Consensus 2016; Derm Surg」, `/sequence_order/5/reason`)을 잘랐다 | 근거 표기가 두 절로 갈라짐 | 괄호 안 구분자는 경계로 쓰지 않음 |
| A1-3 | condition_scope `중` 규칙이 「이중」「집중」 안의 `중` 을 잡았다(`/incompatible_same_day/1/reason`, `/common_combos/3·4·7/name`) | 조건 후보 오탐 4 | 앞이 공백인 독립 어절 `중` 만 |
| A1-4 | order_direction `전` 규칙이 「완전」의 `전` 을 잡았다(`/incompatible_same_day/6/reason`) | 순서 후보 오탐 | 앞이 한글이 아닌 경우만 |
| A1-5 | possibility_risk 에 「저하」, latin_term 이 「°C」의 `C` 를 잡았다 | 범주 오탐 | 규칙에서 제거 / `°` 뒤 제외 |

### A2. 알려진 형태소 오분절 — 69출현 (원시 Kiwi 토큰 유지, 교정 안 함)

전체 기록: [segmentation-review.json](./segmentation-review.json) (`id`·Pointer·`phrase_span`·원시 토큰·영향). build.py 가 매 실행 원문·원시 토큰과 대조한다.

| 종류 | 출현 | 대표(Pointer [구간] 원시 토큰) | 영향 |
|---|---|---|---|
| meaning-risk | 40 | `/principles/1` [13,16) 열/NR 시/NNB 술/NNG · `/minimum_intervals/3/reason` [21,23) 한/MM 해/NNB · `/minimum_intervals/3/reason` [0,3) 저/NP ᆫ/JX 안면/NNG · `/incompatible_same_day/4/reason` [12,13) >/SSC · `/common_combos/0/sequence/2` [3,5) 팔/VV 자/EC | 시술·부위·제품명 소실, 범위 조건(「에 한해」「전안면」)이 시간 수량·대명사로, 초과 비교(>)가 괄호로, 처치(진정)가 부사로 바뀜 |
| tag-only | 3 | `/principles/0` 진정/NNP · `/principles/11`·`/minimum_intervals/7/reason` 먼저/NNG | 품사 기반 수식 후보에서 빠짐(순서 keyword 로는 보존) |
| minor | 8 | CO2 → CO/SL 2/SN (3출현) · 전/MM 안면 (2) · 항/염 · 도/포 · 코스메슈티컬의 | 의미 영향 작음 |
| range-token | 6 | `30-60` `24-72` `60-90` 등 → 단일 W_SERIAL | 범위 하한·상한이 토큰으로 나뉘지 않음(원문 구간·quantity 후보로 보존) |
| code-split | 10 | `M15-클렌징` → M/SL 15/SN -/SO 클렌징 | 코드 번호가 수사로 나옴 — 코드 식별은 원문 값으로 |
| negation-prefix-fused | 1 | `/incompatible_same_day/2/pair/1` 비가교/NNP | 부정 접두 「비」가 드러나지 않음 |
| zero-length | 1 | `/sequence_order/5/reason` [193,193) 이/VCP | surface 빈 문자열 토큰 존재(Kiwi 복원형) |

한계: 1,429토큰을 모두 읽었으나 기록 밖 토큰이 모두 맞다는 보증은 아니다. NNG/NNP 혼용(보톡스·필러·스킨부스터가 출현마다 다름), 「재표면화」의 재/NNG, 「턱선」 턱/선 분리처럼 의미 영향이 작다고 본 차이는 기록하지 않았다. 사용자 사전은 쓰지 않았다(브리프: 기본 결과 보존).

### A3. 알려진 표현 오탐 — 19출현

[manual-expressions.json](./manual-expressions.json) `known_false_positives` (FP01~FP19). 부분일치 8(「웬만하면」의 `면` 2, 코드 접두 `M15-`/`M8-` 만 잡은 latin 6) · 범주 불일치 3(「검증 중」의 `중`, 「아직」을 부정으로, 이름 「동안 기본」의 `기본`) · 오태깅 유래 8(세·이·딩·진정×2·한·이마×2 — 각 A2 기록 id 연결). 표현 자체는 지우지 않았다.

## B. 원문 정보 부족 (열림)

무엇이 부족하고 어떤 판단이 제한되는지만 적는다. 사용자에게 사실을 정해 달라고 묻지 않는다.

| # | 원문 위치 | 부족한 것 | 제한되는 것 |
|---|---|---|---|
| B1 | `/minimum_intervals/2/min_months`(0) ↔ 같은 항목 reason 「중단 후 0~2개월 범위에서 의사 판단」 | 숫자 0 이 하한인지 「대기 없음」인지 원문이 명시하지 않음. **잠정 해석 병기(batch-01 검토 §3.4):** reason 의 「0~2개월 범위」 단서로 보아 0 은 범위의 하한 후보다(확정 아님 · 순수한 원문 부족만은 아님) | **숫자 칸 단독 사용 위험:** 간격 질의에 `min_months` 만 쓰면 0개월(=즉시)로 읽힐 수 있음. reason 과 함께 읽어야 하며, 상한 2개월·「의사 판단」은 숫자 칸에 없음 |
| B2 | `/principles/6` 「침습도 높은 시술」, `/principles/7` 「출혈 위험 시술」 | 침습도 값·척도, 출혈 위험 시술 목록 | 이 두 원칙을 특정 시술 쌍에 적용 불가 |
| B3 | `/incompatible_same_day/6/reason` 「충분한 회복 후에만」 | 회복 기간 값 | 심부 필링 뒤 다른 시술까지의 간격 답변 불가(`/minimum_intervals/4` 의 레이저 14일만 있음) |
| B4 | `/principles/2`·`/sequence_order/2/reason` 「2주 이내 효력 저하 가능성」 | 「효력」의 대상(어느 시술의 효력), `/sequence_order/2/reason` 의 귀결 행동 | 위험 대상 연결·순서 이유 서술 |
| B5 | `/common_combos/*/sequence` | 배열 순서가 시행 순서인지 | C4 판정 불가. note 있는 3건만 순서 서술 |
| B6 | `/incompatible_same_day/0`·`/1`·`/5` pair | 방향(어느 쪽이 먼저일 때 문제인지) | `/minimum_intervals` 의 방향 있는 규칙과 연결·비교 |
| B7 | `/sequence_order/*/categories` 의 `Mn`·`Mn-이름` | 코드가 가리키는 대상 정의(이 원장 밖), 마취 두 값의 코드 | 카테고리 연결은 다른 원장과 비교 단계에서만 가능 |
| B8 | `/minimum_intervals/1·4·7·8/source` 「임상 가이드」, `/minimum_intervals/5/source` 「피부 회복」, `/minimum_intervals/6/source` 「PRS 논문」; `incompatible_same_day` 는 source 칸 없이 reason 안 인용 | 특정 문헌 식별 | 근거 수준 표시·인용 연결 |
| B9 | `/` 와 `+` 기호: 「부종/열 상호작용」「분해/변형」「몰딩/마사지」「이론적/합의 수준」「클렌징/준비」「약물 도포/침투」「진정/마무리」, 「TCA 50%+」「리프팅 + 피부결」 | 기호의 뜻이 README(「/」=대안, 「+」=함께)와 다르게 쓰인 곳이 있음 | 기호만으로 대안/병렬/임계를 기계 분리 불가 |
| B10 | `/common_combos/*/total_time` | 시간에 포함되는 범위(마취 대기 등) | 소요 시간 질의 답변의 범위 |

## C. 원문 내 불일치 (열림 — 후속 비교 대상)

같은 원장 안에서 같은 대상이 다르게 적힌 곳. 어느 쪽이 맞는지 정하지 않았다. 아래 관찰은 그대로 유지한다. C1·C3·C5·C6 은 후속 의미 조사·원장 간 비교 과제로 두고, 비교 결과 **실제 원본 수정 제안이 필요해질 때만** 사용자에게 묻는다(§E).

| # | 위치 | 내용 |
|---|---|---|
| C1 | HA 필러 → RF/HIFU 14일: `/principles/10` 「필수」 · `/incompatible_same_day/4/reason` 「권장」 · `/minimum_intervals/0` 강도 표현 없음. HA 필러 → 레이저 5일: `/principles/12` 「권장」 · `/incompatible_same_day/5/reason` 「필요」 · `/minimum_intervals/1` 없음 | 같은 간격의 강도 표현이 셋으로 갈림 |
| C2 | `/incompatible_same_day/*` | 블록 이름(같은 날 불가)과 내용(간격 규칙·복용 상태·역순 같은 날 가능) 불일치. `/4` pair 원소 1개 |
| C3 | 필러·보톡스 같은 날 순서: `/principles/8` 「순서 유연」· `/sequence_order/5/reason` 「어느 순서든 허용」· `/common_combos/5/note` 「순서 준수」; `/sequence_order/7/reason` 「보톡스 마지막」인데 order 8/11 | 강도와 「마지막」 범위 |
| C4 | `/common_combos/0`·`/2`(보톡스가 필러 앞), `/common_combos/4`(레이저가 IPL 앞) ↔ `sequence_order` phase 순서 | B5 에 달림 — 배열이 시행 순서일 때만 불일치 |
| C5 | 이소트레티노인: `/incompatible_same_day/3`(프락셔널/필링) · `/7`(프락셔널 레이저) · `/8`(케미컬 필링) · `/minimum_intervals/2`(프락셔널/얕은 필링, 0개월) · `/minimum_intervals/3`(박리성(ablative) 레이저/심부 필링, 6개월) | 같은 주제가 다섯 항목에 겹치는 범위로 나뉨 |
| C6 | 명칭 표면형: 「심부 필링(페놀)」·「심부 필링(TCA 50%+/페놀)」·「심부 필링」 / 「CO2 프락셔널」·「프락셔널 CO2」 / 「울쎄라 HIFU」·「HIFU 울쎄라」 / 「레이저토닝」·「토닝」·「레이저 토닝」 / 「HA 필러」·「필러」 | 같은 대상인지 미정(동의어 병합 안 함) |
| C7 | `/description` 「동일 세션」 ↔ `/principles/9`·`/minimum_intervals/*` 별도 세션 | 원장 범위 설명과 내용 |
| C8 | 채널 도포 제한: `/principles/4`(채널 시술 MTS/니들RF) · `/principles/5`(+프락셔널, 금지 예시 목록) · `/sequence_order/9/reason`(+과민반응) | 같은 규칙의 범위·목록 차이 |

## D. 후속 의미 조사 (열림, 시작 안 함)

| # | 과제 | 근거 위치 |
|---|---|---|
| D1 | 관계 방향의 표기 통일 해석: `→`, `from`/`to`, 「역순」, 「먼저/나중에」, 「선행」 | principles 전반, `/minimum_intervals/*`, `/incompatible_same_day/4` |
| D2 | 시간 기준점 구분: 「주입 후」「중단 후」「시술 전」「복용 중」「즉시」「같은 날」「별도 세션」 | `/principles/2`, `/incompatible_same_day/3·7·8`, `/sequence_order/1/reason` 등 |
| D3 | 조건·범위 수식의 대상: 「같은 부위」「동일 부위」「전안면」「국소 부위」「비박리성」「얕은」「모든 시술」 | `/incompatible_same_day/2·6`, `/minimum_intervals/2·3·8` |
| D4 | 강도·가능성 표현 단계: 필수·필요·권장·준수·가능·웬만하면·보수적으로·유연·허용 | C1·C3 포함 |
| D5 | 근거 수준 표현: in vitro·in vivo·RCT 아님·전문가 합의/컨센서스·「임상 가이드」 | `/incompatible_same_day/2`, `/sequence_order/5/reason`, B8 |
| D6 | 시술·제품·브랜드·계열·부위가 한 문자열에 붙은 표현의 분리(「슈링크 HIFU」「스킨부스터 리쥬란」「보톡스 이마+미간」 등) | `/common_combos/*/sequence`, pair·from·to |
| D7 | `categories` 코드와 다른 원장 항목의 연결(다른 원장은 열지 않았다) | B7 |
| D8 | phase 이름의 참조 역할(「에너지 기기 다음, 주사 전」)과 「주사-」 접두 묶음의 구조 | `/sequence_order/3/reason`, `/sequence_order/5~8/phase` |

## E. 사용자 결정 필요 — 현재 선택 대기 0

- 이번 1차에서 사용자에게 고를 것을 묻지 않았다. 도구·규칙 선택(분석기 설정, 절 분할, 오탐 판정)은 에이전트 판단으로 처리하고 기록했다.
- B 는 원문 부족이라 사용자에게 사실을 정해 달라고 물을 항목이 아니다.
- C1·C3·C5·C6 은 **후속 의미 조사·원장 간 비교 과제**로 둔다(batch-01 검토 §3.4·§4 재분류 반영, 이전 표현은 「후속 비교 뒤 사용자 결정 후보」). 대응: C1·C3 = D4(강도·가능성 표현 단계), C5 = D2·D3(시간 기준점·범위 수식, 원장 간 비교), C6 = D6(표면형 분리)·원장 간 동의어 비교. 원문 내 불일치 관찰(§C 표)은 지우지 않고 유지한다.
- 비교 결과 **실제 원본 수정 제안**(원장 문구를 고치거나 정본 표현을 고르는 일)이 필요해질 때만 원문·이유·선택지와 함께 사용자에게 올린다. 지금 사용자 결정을 받은 것으로 취급하지 않으며, 이 재분류 자체도 사용자 결정이 아니다.
- 0 건은 「결정 불필요」가 아니라 「현재 단계에서 선택 대기로 올린 것 없음」이다.
