# treatment-optimization.json — 미결 기록

> build.py 가 manual/seg-XX.json 의 issues·F 관찰과 manual/global-issues.json 에서 생성한다. 손으로 고치지 말고 manual 을 고친 뒤 재생성한다.
> 기호: A=에이전트 추출/해석 오류 · B=원문 정보 부족 · C=현재 사용자 결정 필요 · I=원문 내 불일치(후보) · K=알려진 분석 한계 · P=잠정 · F=후속 의미 조사. 원문 내 불일치를 C 로 부르지 않는다. 원본 변경 제안은 현재 원본 보존 지시 아래 후속 확인 후보이며 선택 대기로 올리지 않는다.

## 요약

| 기호 | 뜻 | 건수 | 처리 상태 |
|---|---|---|---|
| A | 에이전트 추출/해석 오류 | 4 | 발견 즉시 수정·재검증(아래 목록은 수정 이력) |
| B | 원문 정보 부족 | 26 | 열림 — 원문에 정보가 없어 1차에서 닫을 수 없음. 사용자 추측으로 메우지 않음 |
| C | 현재 사용자 결정 필요 | 0 | 0 — 아래 「사용자 결정 0의 근거」 참조 |
| I | 원문 내 불일치 후보 | 12 | 열림 — 판정하지 않고 위치만 기록. 원본 수정 제안은 후속 확인 후보 |
| K | 알려진 분석 한계 | 6 | 기록됨 — 한계로 남김(교정 안 함) |
| P | 잠정 | 108 | review-part 의 잠정 관찰 절에 있음 |
| F | 후속 의미 조사 | 14 | 열림 — 전체 21개 비교 뒤 의미 조사 단계 |

## A — 에이전트 추출/해석 오류 (4)

- **A-01** (전역) 자동 후보 R19(계절·시기)가 「개월」 안의 「월」 24곳을 잡던 추출 오류.
  - 영향: 수정 전 R19 후보 24건이 노이즈였다. 수정 후 원문 구간 재현 확인.
  - 처리: 정규식을 어절 단독 「월·분기·연」 으로 고치고 재생성·재검증(build·verify 통과).
- **A-02** (전역) expression-review 의 「화장품 광고 내」 오탐 기록이 같은 값의 첫 「내」(국내외)를 가리킨 출현 인덱스 오기.
  - 처리: 출현 인덱스를 1로 고침. build 가 오탐 기록과 자동 후보의 정확 구간 일치를 단언해 검출했다.
- **A-03** (전역) seg-10 수동 구절 1건을 원문과 다른 문자열(「HA 주입 후 …」)로 적은 기록 오류.
  - 처리: 원문 「HA 필러 주입 후 14일 이내 RF/HIFU 시」 로 고침. build 는 수동 구절이 원문 부분 문자열이 아니면 실패한다.
- **A-04** (전역) 미덮임 어절 판정이 구두점 붙은 어절(「금지.」 등)을 미덮임으로 세던 판정 오류. 검토 중 수동 구절 누락 2건(「엑소좀 근거는」「HA 필러는」) 발견.
  - 처리: 앞뒤 구두점을 뗀 뒤 판정하도록 고치고 누락 2건을 manual 에 추가, 재생성·재검증. 남은 미덮임 어절은 전수 검토(validation.md §3).

## K — 알려진 분석 한계 (6)

- **K-01** (전역) Kiwi 0.24.1(cong·기본 사전·사용자 사전 없음) 원시 출력의 알려진 오분절·오태깅 77출현을 manual/segmentation-review.json 에 출현별(Pointer·구간·원시 토큰·영향)로 기록했다. 교정하지 않았다. 이 목록 밖 원시 토큰의 정확성은 보장하지 않는다. 같은 시술명이 NNP/NNG 로 흔들리는 태그 차이는 출현별로 기록하지 않았다.
  - 영향: 거짓 수량(열시술→열/NR 시/NNB, CO2→2/SN, 미백→백/NR), 부정 소실(비수술→비수, 비가교·비마사지군), 거짓 부사(엑소좀→좀/MAG, 아이스픽→픽/MAG, 슬림→슬/MAG), 시술명 분해(필러·필링·스킨부스터·서브시전·지방이식). 토큰만으로 수량·부정·정도를 뽑으면 오탐·누락이 난다 — 수동 구절과 원문 구간을 함께 써야 한다.
- **K-02** (전역) 다국어 범위: 영어(concern_en 8, level 괄호 영어 3, consensus_method, combination_rules evidence 의 문헌명·in vitro·RCT·split-face·test spot·Do No Harm 등)와 한자 약칭(美·韓)은 Kiwi 가 SL/SH 토큰으로만 자른다. 영어 형태소·기본형·품사는 제공되지 않으며 만들어 채우지 않았다.
  - 영향: 영어 구간의 수식·부정(No Harm, deep, fine 등)은 형태소로 잡히지 않고 수동 구절(kinds=language_en)·R20 라틴 연속 후보로만 수집됐다. 영어 전용 분석기는 1차 범위에서 쓰지 않았다.
- **K-03** (전역) 자동 정규식 후보(R01~R20)는 실제 일치분뿐이다. 키워드·부정·정도 목록은 불완전 목록이고, R04(`/`)·R05(`+`) 는 기호 양옆 한 어절만 잡아 항목 경계와 다를 수 있다(예: 「토닝 5-10회 + 스킨부스터 3회」에서 「5-10회 + 스킨부스터」).
  - 영향: 자동 후보 목록을 전수 표현 목록으로 쓰면 안 된다. 경계 오류 중 의미를 바꾸는 4건은 오탐으로 표시했고 나머지 경계 잘림은 이 한계로 남긴다.
- **K-04** (전역) auto_clause(C01) 는 `. ` `; ` `→` `, ` `: ` ` — ` 기준 기계 분할이라 괄호 안 쉼표에서도 자른다. 의미 단위가 아니다.
  - 영향: 절 단위는 문맥 탐색 보조로만 쓴다.
- **K-05** (전역) 필드명 41종은 Kiwi 에 그대로 넣어 영어 SL·`_`(SW) 토큰으로만 나뉜다. 필드명은 원문 텍스트와 역할을 구분해 morphology.json field_names 에 따로 두었다.
  - 영향: 필드명 뜻은 형태소로 얻지 않는다.
- **K-06** (전역) 「별도 읽기 검토」 는 같은 에이전트가 관점을 바꿔(토큰 대조·자동 후보 대조·미덮임 어절 대조·블록 간 대조) 다시 읽은 것이며 독립 검토자가 아니다.
  - 영향: 독립 검토는 코디 단계에서 필요하면 따로 한다.

## B — 원문 정보 부족 (26)

- **B-00-1** (SEG-00) 원칙 배열 순서의 의미(우선순위 여부)와 적용 대상 연결이 원문에 없다. 원칙별 가중·충돌 시 처리 규칙을 원장만으로 정할 수 없다.
  - 위치: `/optimization_principles`
- **B-01-1** (SEG-01) 「2주 후 필러」의 기준 시점과 스킨부스터의 간격이 원문에 없다.
  - 위치: `/by_concern/0/severity_levels/2/sequence`
- **B-01-2** (SEG-01) optimal_combo 「필러」가 금지 문구의 「HA 필러」와 같은지 원문에 없다.
  - 위치: `/by_concern/0/severity_levels/2/optimal_combo/2`, `/by_concern/0/severity_levels/2/contraindicated_combos/0`
- **B-02-1** (SEG-02) 간격(4주 후·2-4주 후)의 기준 시점과 뒤 단계(필러·바이오스티뮬레이터) 간격이 원문에 없다.
  - 위치: `/by_concern/1/severity_levels/1/sequence`, `/by_concern/1/severity_levels/2/sequence`
- **B-02-2** (SEG-02) 「동시」의 범위(같은 날·같은 회차·같은 부위)가 원문에 없다.
  - 위치: `/by_concern/1/severity_levels/2/contraindicated_combos/0`
- **B-03-1** (SEG-03) 「4주 간격」이 반복 간격인지 앞 시술과의 간격인지 원문에 없다.
  - 위치: `/by_concern/2/severity_levels/0/sequence`
- **B-04-1** (SEG-04) caveats 가 한 단계에만 있다. 다른 단계·고민에 주의사항이 없는 것인지 기록하지 않은 것인지 원문에 없다.
  - 위치: `/by_concern/3/severity_levels/2/caveats`
- **B-04-2** (SEG-04) 근거 서술(파일럿·RCT 1건)에 문헌 식별자가 없다. 근거 연결은 원장만으로 할 수 없다.
  - 위치: `/by_concern/3/severity_levels/2/caveats/1`
- **B-05-1** (SEG-05) 저출력·고출력·고에너지의 수치 기준이 원문에 없다. 추천(저출력 IPL)과 금지(고출력 IPL)의 경계를 원장만으로 정할 수 없다.
  - 위치: `/by_concern/4/severity_levels/1/contraindicated_combos/0`, `/by_concern/4/severity_levels/1/contraindicated_combos/1`, `/by_concern/4/severity_levels/2/contraindicated_combos/0`, `/by_concern/4/severity_levels/1/optimal_combo/3`
- **B-05-2** (SEG-05) 중증 단계에서 저출력·병용 IPL 이 허용되는지 원문에 없다.
  - 위치: `/by_concern/4/severity_levels/2/contraindicated_combos/1`
- **B-06-1** (SEG-06) 「침습 시술」 의 범위가 원문에 없다.
  - 위치: `/by_concern/5/severity_levels/2/contraindicated_combos/1`
- **B-06-2** (SEG-06) 「매회」 가 어느 시술의 회차를 가리키는지, 「2주 간격」 이 반복인지 원문에 없다.
  - 위치: `/by_concern/5/severity_levels/0/sequence`
- **B-07-1** (SEG-07) 피부톤(밝은/어두운) 구분 기준과 「필요시」 조건이 원문에 없다.
  - 위치: `/by_concern/6/severity_levels/1/rationale`, `/by_concern/6/severity_levels/1/sequence`
- **B-08-1** (SEG-08) `or` 와 `+` 의 결합 범위가 원문 표기만으로 정해지지 않는다(괄호 없음).
  - 위치: `/by_concern/7/severity_levels/1/sequence`, `/by_concern/7/severity_levels/1/expected_sessions`
- **B-08-2** (SEG-08) 「바디 HIFU/RF」 의 `/` 가 대안인지 병용인지 원문에 없다(sessions 는 따로 셈).
  - 위치: `/by_concern/7/severity_levels/2/sequence`, `/by_concern/7/severity_levels/2/expected_sessions`
- **B-09-1** (SEG-09) avoid 의 정도 기준(과도한·불필요한·과잉·회복력 초과)이 원문에 없다. 회피 조건을 판정 규칙으로 쓸 수 없다.
  - 위치: `/by_age_group/0/avoid/0`, `/by_age_group/0/avoid/1`, `/by_age_group/1/avoid/0`, `/by_age_group/2/avoid/0`, `/by_age_group/3/avoid/0`, `/by_age_group/3/avoid/1`
- **B-09-2** (SEG-09) 「연 1사이클」 의 사이클 정의(회차)가 원문에 없다.
  - 위치: `/by_age_group/2/maintenance`, `/by_age_group/3/maintenance`
- **B-09-3** (SEG-09) 20대에 upgrade 가 없는 것이 없음인지 미기록인지, 50대+ 외에 note 가 없는 것의 뜻이 원문에 없다.
  - 위치: `/by_age_group/0`
- **B-10-1** (SEG-10) priority 네 값의 척도·순서가 원문에 없다.
  - 위치: `/combination_rules/0/priority`, `/combination_rules/1/priority`, `/combination_rules/2/priority`, `/combination_rules/3/priority`, `/combination_rules/4/priority`, `/combination_rules/5/priority`, `/combination_rules/6/priority`, `/combination_rules/7/priority`
- **B-10-2** (SEG-10) evidence 가 범주·연도만 있어 문헌을 특정할 수 없는 값이 있다.
  - 위치: `/combination_rules/1/evidence`, `/combination_rules/3/evidence`, `/combination_rules/4/evidence`, `/combination_rules/5/evidence`, `/combination_rules/6/evidence`, `/combination_rules/7/evidence`
- **B-10-3** (SEG-10) 「5-5-5 마사지」 의 정의가 원문에 없다.
  - 위치: `/combination_rules/2/detail`
- **B-11-1** (SEG-11) 월 안의 날짜·순서·같은 날 여부와 procedures 배열 순서의 뜻이 원문에 없다. 같은 달 항목에 동일일·간격 규칙을 적용할 수 없다.
  - 위치: `/annual_plans/0/schedule`
- **B-11-2** (SEG-11) 예산 범위가 무엇을 포함하는지 원문에 없다.
  - 위치: `/annual_plans/0/annual_budget_range`
- **B-12-1** (SEG-12) 「터치업」 의 범위(부위·용량)와 회차 셈 포함 여부가 원문에 없다.
  - 위치: `/annual_plans/1/schedule/2/procedures/0`
- **B-13-1** (SEG-13) 「40대+」 가 by_age_group 의 40대·50대+ 중 무엇을 덮는지 원문에 없다.
  - 위치: `/annual_plans/2/age_group`
- **B-13-2** (SEG-13) 같은 달 여러 시술의 날짜·순서가 원문에 없어 동일일·간격 규칙 적용 여부를 판단할 수 없다.
  - 위치: `/annual_plans/2/schedule`

## I — 원문 내 불일치 후보 (12)

- **I-03-1** (SEG-03) CaHA 가 optimal_combo·sequence·rationale 에 있으나 expected_sessions 에 회차가 없다(원문 내 불일치 후보). 원본 수정 제안은 후속 확인 후보로만 둔다.
  - 위치: `/by_concern/2/severity_levels/2/optimal_combo/1`, `/by_concern/2/severity_levels/2/expected_sessions`
- **I-04-1** (SEG-04) optimal_combo 「MTS/니들RF」 와 sequence·sessions 「프락셔널 …/니들RF」: MTS 가 뒤 필드에서 사라진다(원문 내 불일치 후보).
  - 위치: `/by_concern/3/severity_levels/1/optimal_combo/1`, `/by_concern/3/severity_levels/1/sequence`, `/by_concern/3/severity_levels/1/expected_sessions`
- **I-04-2** (SEG-04) caveats/0 의 효능 단정 금지 지침과 rationale 의 「회복·재생 보조」 문구 사이의 긴장 후보. 판정하지 않음.
  - 위치: `/by_concern/3/severity_levels/2/caveats/0`, `/by_concern/3/severity_levels/2/rationale`
- **I-05-1** (SEG-05) 중증 트라넥삼산 경로: optimal_combo 「경구+주사」 vs sequence 「경구+국소」(원문 내 불일치 후보).
  - 위치: `/by_concern/4/severity_levels/2/optimal_combo/1`, `/by_concern/4/severity_levels/2/sequence`
- **I-06-1** (SEG-06) 중등도: optimal_combo 「MTS/니들RF」, sequence 「프락셔널/니들RF」, sessions 는 프락셔널·니들RF 를 따로 셈(원문 내 불일치 후보).
  - 위치: `/by_concern/5/severity_levels/1/optimal_combo/2`, `/by_concern/5/severity_levels/1/sequence`, `/by_concern/5/severity_levels/1/expected_sessions`
- **I-07-1** (SEG-07) 중등도 rationale 의 Nd:YAG 가 optimal_combo 에 없다(원문 내 불일치 후보).
  - 위치: `/by_concern/6/severity_levels/1/rationale`, `/by_concern/6/severity_levels/1/optimal_combo`
- **I-10-1** (SEG-10) HA 필러 → HIFU 간격: 4주 이상 권장 vs 14일 이내 위험/금지(원문 내 불일치 후보).
  - 위치: `/combination_rules/0/detail`, `/combination_rules/1/detail`, `/by_concern/0/severity_levels/2/contraindicated_combos/0`
  - 비고: 양립 가능; 모순으로 확정하지 않음. 「14일 이내 RF/HIFU 시 필러 용해 위험」(`/combination_rules/1/detail`)·「14일 이내 RF/HIFU 금지」(`/by_concern/0/severity_levels/2/contraindicated_combos/0`)는 금지·위험 하한이고, 「필러 후 HIFU를 4주 이상 간격 권장」(`/combination_rules/0/detail`)은 권장 간격이다 — 강도가 다른 별개 진술이라 함께 성립한다. 후속 검토로 남는 것: 14일~4주 구간을 어떻게 다룰지, 간격의 기준 시점, RF 포함 범위(4주 문장은 HIFU 만, 14일 문장은 RF/HIFU 를 적었다). I 분류·ID·집계는 그대로 둔다. 원문 모순 확정 목록에 넣지 않는다. 원문을 고치거나 새 관계를 적용하지 않았고, 원문 밖 임상 판단으로 채우지 않는다(batch-04 독립 검토 §2.5 R2 반영).
- **I-10-2** (SEG-10) 프락셔널 후 필러: 제목 「당일 금지」 vs detail 「최소 4주 간격」(원문 내 불일치 후보).
  - 위치: `/combination_rules/3/rule`, `/combination_rules/3/detail`
  - 비고: 양립 가능; 모순으로 확정하지 않음. detail 「최소 4주 간격」(`/combination_rules/3/detail`)은 rule 「프락셔널 후 당일 필러 금지」(`/combination_rules/3/rule`)를 포함한다 — 제목이 더 좁은 범위를 적은 포함 관계다. 후속 검토로 남는 것: 금지 범위가 당일인지 4주인지(제목과 상세의 범위 차이), 간격의 기준 시점. I 분류·ID·집계는 그대로 둔다. 원문 모순 확정 목록에 넣지 않는다. 원문을 고치거나 새 관계를 적용하지 않았고, 원문 밖 임상 판단으로 채우지 않는다(batch-04 독립 검토 §2.5 R2 반영).
- **I-10-3** (SEG-10) 기미: 「저출력 토닝만 권장」 vs 중등도 추천 「저출력 IPL(병용 보조)」(원문 내 불일치 후보).
  - 위치: `/combination_rules/4/detail`, `/by_concern/4/severity_levels/1/optimal_combo/3`
- **I-10-4** (SEG-10) 제모 부위 필링/프락셔널: 「2주 내」 vs 「동시」(원문 내 불일치 후보).
  - 위치: `/combination_rules/6/detail`, `/by_concern/6/severity_levels/2/contraindicated_combos/0`
  - 비고: 양립 가능; 모순으로 확정하지 않음. 「제모 부위 필링/프락셔널 동시 금지」(`/by_concern/6/severity_levels/2/contraindicated_combos/0`)는 「레이저 제모 후 2주 내 동일 부위 필링/프락셔널 금지」(`/combination_rules/6/detail`)에 포함된다 — 포함 관계다. 후속 검토로 남는 것: 「동시」의 범위, 2주 이후의 처리, 두 문장의 부위 표현(「제모 부위」·「동일 부위」)이 같은 범위인지. I 분류·ID·집계는 그대로 둔다. 원문 모순 확정 목록에 넣지 않는다. 원문을 고치거나 새 관계를 적용하지 않았고, 원문 밖 임상 판단으로 채우지 않는다(batch-04 독립 검토 §2.5 R2 반영).
- **I-11-1** (SEG-11) 20대 토닝·필링 빈도: plan(토닝 매월 4회·필링 연 4회) vs maintenance(토닝 월 1-2회·필링 월 1회)(원문 내 불일치 후보).
  - 위치: `/annual_plans/0/schedule`, `/by_age_group/0/maintenance`
- **I-12-1** (SEG-12) 30대 토닝 빈도: plan 월 4회 vs maintenance 월 1-2회(원문 내 불일치 후보).
  - 위치: `/annual_plans/1/schedule`, `/by_age_group/1/maintenance`

## F — 후속 의미 조사 (14)

- **F-O01-2** (SEG-01) optimal_combo 는 「레이저토닝」, sequence·expected_sessions·rationale 은 「토닝」으로 줄여 부른다. 같은 대상을 가리키는지는 문맥상 그럴듯하나 원문 표기만으로 연결하지 않았다.
  - 위치: `/by_concern/0/severity_levels/0/optimal_combo/0`, `/by_concern/0/severity_levels/0/sequence`, `/by_concern/0/severity_levels/0/expected_sessions`
- **F-O02-2** (SEG-02) 「써마지/RF」는 장비명과 계열명을 `/` 로 잇는다. README `/`(둘 중 하나)로 읽을지 동격(써마지=RF 장비)으로 읽을지 원문만으로 정하지 않았다. sequence 는 「RF 시술」로만 부른다.
  - 위치: `/by_concern/1/severity_levels/0/optimal_combo/0`, `/by_concern/1/severity_levels/0/sequence`
- **F-O02-5** (SEG-02) optimal_combo 의 「바이오스티뮬레이터」를 rationale·expected_sessions 는 「바이오스티뮬」로 줄여 쓴다. 표기 차이만 기록했다.
  - 위치: `/by_concern/1/severity_levels/1/rationale`, `/by_concern/1/severity_levels/1/expected_sessions`, `/by_concern/1/severity_levels/2/rationale`, `/by_concern/1/severity_levels/2/expected_sessions`
- **F-O03-5** (SEG-03) 같은 대상이 「HA 필러(딥)」「딥필러」「딥 필러」 세 표기로 나온다. 괄호 「(딥)」은 깊이 수식이다.
  - 위치: `/by_concern/2/severity_levels/2/optimal_combo/0`, `/by_concern/2/severity_levels/2/sequence`, `/by_concern/2/severity_levels/2/rationale`, `/by_concern/2/severity_levels/2/expected_sessions`
- **F-O05-10** (SEG-05) 「마이크로니들링+미백약물」(optimal_combo) / 「마이크로니들+미백약」(sequence) / 「마이크로니들 5회」(sessions): 표기 축약 차이. 여기 `+` 는 시술+약물 결합.
  - 위치: `/by_concern/4/severity_levels/2/optimal_combo/2`, `/by_concern/4/severity_levels/2/sequence`, `/by_concern/4/severity_levels/2/expected_sessions`
- **F-O06-4** (SEG-06) 「ALA-PDT」 를 rationale·sessions 는 「PDT」 로 줄여 쓴다.
  - 위치: `/by_concern/5/severity_levels/0/optimal_combo/0`, `/by_concern/5/severity_levels/0/rationale`, `/by_concern/5/severity_levels/0/expected_sessions`
- **F-O08-10** (SEG-08) RF 계열 이름이 단계마다 다르다: 「고주파 바디 RF」·「바디 RF」·「RF 타이트닝」.
  - 위치: `/by_concern/7/severity_levels/2/optimal_combo/2`, `/by_concern/7/severity_levels/1/optimal_combo/2`, `/by_concern/7/severity_levels/0/optimal_combo/1`
- **F-O08-11** (SEG-08) 「카복시테라피」 를 sequence·rationale·sessions 는 「카복시」 로 줄여 쓴다.
  - 위치: `/by_concern/7/severity_levels/1/optimal_combo/3`, `/by_concern/7/severity_levels/1/sequence`
- **F-O09-2** (SEG-09) primary_concerns 표기가 by_concern 의 concern 과 일부만 같다: 「여드름/흉터」「색소/기미」 는 같은 문자열, 「모공」「피부결」 은 by_concern 「피부결/모공」 을 둘로 나눈 꼴, 「초기 주름」「주름 심화」「깊은 주름」 은 정도 수식이 붙은 꼴, 「눈가 노화」「피부 노화」「목주름」 은 by_concern 에 대응 고민이 없다. 연결은 하지 않았다.
  - 위치: `/by_age_group/0/primary_concerns`, `/by_age_group/1/primary_concerns`, `/by_age_group/2/primary_concerns`, `/by_age_group/3/primary_concerns`
- **F-G1** (전역) 같은 대상으로 보이는 다른 표기의 연결: 필러/HA 필러/HA 필러(딥)/딥필러/딥 필러, 바이오스티뮬레이터/바이오스티뮬, 레이저토닝/토닝, 카복시테라피/카복시, 알렉산드라이트/알렉, ALA-PDT/PDT, HIFU(슈링크/울쎄라)/HIFU(울쎄라/슈링크)/울쎄라 HIFU/HIFU(울쎄라급), 실리프팅(PDO/PCL)/(PCL/PDO), CO2 프락셔널/프락셔널 CO2, 고주파 바디 RF/바디 RF/RF 타이트닝, 비가교HA/비가교 HA. 1차에서는 병합하지 않았다.
  - 영향: 병합 전에는 시술 단위 집계·관계 추출이 표기별로 갈린다.
- **F-G2** (전역) 기호 쓰임 정리: `+` (함께 시술·회차 나열·효과 나열·부위 나열·금지 조합·연령 이상·출처 나열·분수 아님), `/` (대안·대상 나열·부위·회당 빈도·분수·연도), `or`·「또는」(대안), 괄호(제품 예시·부위·목적·대상·계절·평가·영어 원어·사유·조건), `→`(순서), `:`(라벨·같은날 표지·장비명 내부). README 규칙과 다른 쓰임이 많다(review-part 잠정 관찰).
  - 영향: 기호만으로 관계를 확정하면 오류가 난다(README 도 기호만으로 의미 관계를 확정하지 말라고 함).
- **F-G3** (전역) 블록 간 연결: by_age_group.primary_concerns ↔ by_concern.concern, annual_plans.age_group ↔ by_age_group.age(「40대+」 불일치), combination_rules ↔ by_concern.contraindicated_combos, maintenance ↔ annual_plans.schedule. 원장 안에 참조 키가 없고 문자열만 겹친다.
  - 영향: 연결 규칙은 의미 조사 단계 과제다. 원장 내 불일치 후보(I)는 이 연결을 전제로 드러난 것이다.
- **F-G4** (전역) 시간·간격 표현의 의미 구분과 기준 시점: 후 / 후부터 / 간격(반복·앞 시술과의 간격) / 이내 / 내 / 이상 / 최소 / 동시 / 당일 / 같은날 / 직후 / 즉시 / 매회 / 사이사이 / 교차 / 회복(기간) / 터치업. 효과 보완·동일일 가능·순서·간격·회피·대상/부위별 조건을 구분해 관찰만 했다.
  - 영향: 간격 규칙을 구조화하려면 기준 시점(앞 단계 전체인지 직전 시술인지)이 필요하나 원문에 없는 곳이 많다(B 항목).
- **F-G5** (전역) 추천·금지의 조건 구조: 출력(저/고), 단독/병용, 피부톤(밝은/어두운, Fitzpatrick IV~VI), 상태(활성 여드름 시·기미에·진피 기미), 부위(제모 부위·동일 부위), 생활 사건(선탠 후), 선행 조건(시험 조사·광차단). 최적화 추천 문구는 확정 관계·임상 사실로 승인하지 않았다.
  - 영향: 조건을 떼면 추천과 금지가 충돌하는 것처럼 읽힌다(예: 저출력 IPL 병용 보조 추천 vs 기미 IPL 단독·고출력 금지).

## C — 현재 사용자 결정 필요 (0)

- 현재 사용자 선택 대기 C 는 0건이다. 이 표시는 아래 잔여 항목의 처리 상태와 영향을 검토한 뒤의 판단이다.
- B(원문 정보 부족): 원문에 없는 기준·정의·기준 시점이다. 사용자 추측으로 채우지 않는다 — 열린 채 둔다.
- I(원문 내 불일치 후보): 판정하지 않고 위치만 기록했다. 원본 수정 제안은 현재 원본 보존 지시 아래 후속 확인 후보이며 지금 선택 대기로 올리지 않는다.
- F(후속 의미 조사): 전체 21개 원장 비교 뒤 의미 조사·설계 단계에서 묶어 제시한다.
- K(분석 한계): 도구 설정·사용자 사전 여부는 에이전트 판단 범위다. 이번에는 기본 결과를 보존하고 알려진 오분절을 출현별로 기록했다.
- A(에이전트 오류): 발견한 4건은 수정·재검증했다. 사용자 결정으로 넘기지 않았다.

