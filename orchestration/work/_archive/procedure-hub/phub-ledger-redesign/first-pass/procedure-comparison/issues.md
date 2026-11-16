# procedure-comparison.json — 미결 기록

분류
- **A** 추출·분석 한계(에이전트가 기록으로 남긴 알려진 오류·미판정). 실제 추출 오류(누락·잘못된 Pointer·구간·원문 변형)는 0건이다(verify.py).
- **B** 원문 정보 부족: 무엇이 없고 무엇이 제한되는지. 사용자 추측으로 채우지 않는다.
- **C** 사용자 결정 필요: **0건**. 근거는 아래 「C 가 0인 이유」.
- **F** 후속 의미 조사: 1차 범위 밖. 해결된 것으로 세지 않는다.

상태 표기: `열림`(처리 안 됨) · `기록됨`(1차에서 위치·영향을 남김, 해결 아님).

## A. 추출·분석 한계

| # | 내용 | 위치 | 영향 | 상태 |
|---|---|---|---|---|
| A1 | 원문 대조로 확인한 Kiwi 오분절·오태깅 39서명 52출현. 교정하지 않고 원시 토큰을 유지한 채 출현별 표시 | [segmentation-review.json](./segmentation-review.json) · review.md §5 | 의미 위험 큰 것: S01 RCT는→늘다, S06·S07 즉각·즉시 분절, S09 겔→것이ㄹ, S12 반영구→반영, S16 `>`→닫는 괄호, S17 피코→코, S20 타겟→타다, S23 과다→이다, S24 재발→발, S26 항노화→항+노화. 형태소 결과만 쓰면 시점·정도·부정·순서·부위가 사라지거나 가짜로 생긴다 | 기록됨(교정 아님) |
| A2 | NNP 태그 110건을 출현마다 판정하지 않았다. 보통명사(콜라겐·필러·다운타임·영구·멜라닌·니들 등)가 고유명사로 태깅된 것이 다수로 보인다 | morphology.json `auto_flags`(reason 「고유명사 추정(NNP)」) | 명사 범주는 유지되므로 1차 수집의 구간·원문 대응에는 영향이 없다. 고유명/보통명 구분에 품사를 쓰면 틀린다 | 기록됨(미판정) |
| A3 | 범위·수량 표기 「N-M」 이 W_SERIAL 한 토큰이고, 「Fitz III-V」 는 SL+SO+SL 로 나뉜다. 길이 0 토큰 2개(서술격 조사 복원) | morphology.json 토큰 · review.md §5 | 범위의 하한·상한이 형태소로는 분리되지 않는다. quantity_range_unit 후보(regex)로 원문 구간을 따로 보존했다 | 기록됨 |
| A4 | regex·keyword 후보는 직접 판정한 48건 외에는 미판정 후보다. 오탐 32·부분일치 3·구성요소 일치 13 은 표시만 하고 지우지 않았다 | [expression-review.json](./expression-review.json) | 후보 수를 의미 조사 결과로 세면 안 된다 | 기록됨 |

## B. 원문 정보 부족

| # | 무엇이 없나 | 원문 위치 | 제한되는 활용 | 상태 |
|---|---|---|---|---|
| B1 | `pain` ★ 척도의 정의(만점·측정 주체·마취 여부 조건) | `/comparisons/*/procedures/*/pain` 39 | 통증을 수치로 비교·정렬하는 질문 | 열림 |
| B2 | `pih_risk` 코드의 정의·순서·근거. `none` 이 「없음」인지 「해당 없음」인지 | `/comparisons/*/procedures/*/pih_risk` 39 | PIH 위험 비교, 「위험 없음」 응답 | 열림 |
| B3 | `cost_range` 의 가격 기준(21개는 기준 표기 없음)·시점·지역·통화 외 단위 | `/comparisons/*/procedures/*/cost_range` | 가격 비교·합산 | 열림 |
| B4 | 약어·코드 풀이(HIFU·RF·SMAS·PIH·PAH·LIOB·PLLA·PCL·CMC·PDLLA·BHA·TCA·PDT·IPL·MTS·PRP·HA·RCT·RR·Fitz 등). PN 만 원장 안에 병기 | `abbreviation_or_code_in_text` 후보 65출현 | 약어를 개념·부작용 노드로 연결하는 것. 외부 자료로 채우지 않았다 | 열림 |
| B5 | 근거 표현의 기준: 「근거수준 III」 등급 체계, 「RR 4.44」 의 비교 대상·대상 집단·출처, 「후향적 관찰연구」의 출처 | `/comparisons/0/evidence_notes/0`·`/3`, `/comparisons/3/evidence_notes/1`, `/comparisons/3/procedures/1/limitations` | 근거 수준 표시, 위험 크기 비교. 보고 수치를 발생률로 바꾸지 않는다 | 열림 |
| B6 | 비교·조건의 기준 생략: 「가장」의 비교 범위, 「레이저 대비」의 레이저, 「더 많은 회차」의 비교 대상, 「(반복 시)」의 횟수, 「(과다 시)」의 무엇이 과다한지, 「연간 비용 최저」의 계산, 「고급 재생」의 기준, 「저밀도/저에너지 세팅」의 수치 | `/comparisons/0/evidence_notes/2`, `/comparisons/0/procedures/1/limitations`, `/comparisons/5/procedures/2/limitations`, `/comparisons/5/procedures/3/limitations`, `/comparisons/4/procedures/3/limitations`, `/comparisons/2/evidence_notes/0`, `/comparisons/8/procedures/2/best_for`, `/comparisons/3/procedures/1/asian_skin_note` | 비교·조건을 수치나 다른 시술에 연결하는 것. 수식 대상을 채우지 않는다 | 열림 |
| B7 | 원장 내부 불일치 후보: 지방이식 「흡수율 변동(30-70%)」 ↔ 자가지방이식 「생착률 변동 (30-70%)」 — 같은 수치가 두 지표에 붙어 있다 | `/comparisons/2/evidence_notes/2` [18,32) · `/comparisons/2/procedures/3/limitations` [0,15) | 생착·흡수 수치의 사용. 어느 쪽이 맞는지 원장만으로 정할 수 없다 | 열림 |
| B8 | 값의 대상 정의 없음: 엘란쎄 「(타입별)」 의 타입 목록, 제모 duration 백분율(80-90% 등)이 무엇의 비율인지 | `/comparisons/2/procedures/2/duration`, `/comparisons/5/procedures/0..3/duration` | 지속기간·효과율 질문 | 열림 |
| B9 | 「실리콘피부관리 (아쿠아필/하이드라)」 의 「실리콘」 이 의도된 이름인지 오기인지 | `/comparisons/3/procedures/4/name` | 시술명 표준화·다른 원장 대조. 고치지 않았다 | 열림 |

## F. 후속 의미 조사 (1차 범위 밖)

| # | 과제 | 근거 위치 | 상태 |
|---|---|---|---|
| F1 | `category` Mxx 의 뜻(다른 원장과 대조). 한 코드에 서로 다른 기전 항목이 있음 | `/comparisons/*/procedures/*/category` | 열림 |
| F2 | 필드와 값 종류의 불일치 분해: `onset`(시간·회차·간격), `duration`(기간·영구 한정·백분율·관리 지시·서술), 괄호 한정(생착 후·사멸 지방·파괴된 피지선·생착분·타입별) | review.md §4.1·§4.2 | 열림 |
| F3 | 기호 `/`·`+` 의 역할 분해(대안·함께·나열·단위 기준·단계·하한). README 의 `/`=대안, `+`=함께 시술 규칙과 맞지 않는 쓰임 다수 | `symbol_relation` 후보 246 | 열림 |
| F4 | 같은·비슷한 이름의 대상 관계: 히알루론산 필러 2곳(값 다름), 리쥬란·쥬베룩·인모드·IPL·Nd:YAG 계열, 히알루로니다제/히알루로니다아제 철자, 한 항목 안 두 제품(스킨부스터) | review.md §4.1 | 열림 |
| F5 | evidence_notes 의 머리말(실리프팅·HIFU·RF·니들RF·CO2 프랙셔널·케미컬 필·바이오스티뮬레이터·HA 필러·지방이식)이 어느 procedures 항목·계열을 가리키는지. 「케미컬 필」 은 같은 비교군에 대응 항목 없음. HIFU 2-3개월 ↔ 울쎄라 3개월 차이 | `/comparisons/0/evidence_notes/*`, `/comparisons/2/evidence_notes/*`, `/comparisons/3/evidence_notes/*` | 열림 |
| F6 | 관계·수식 대상: 조합(실+RF/HIFU)의 보완 관계와 동시 시행 여부 구분, 「드물지만」의 수식 대상, `>` 순서 관계 방향, 근거 상태(아직 제한적)·변동 요인(혈소판 농도 의존)의 대상 | `/comparisons/0/evidence_notes/0`·`/3`, `/comparisons/1/procedures/1/limitations`, `/comparisons/2/procedures/0/limitations`, `/comparisons/3/evidence_notes/3`, `/comparisons/8/procedures/1..2/limitations` | 열림 |
| F7 | 부위·대상 집단 표현의 역할: best_for 괄호 부위(이마, 미간, 눈가 / 복부, 러브핸들)가 예시인지 한정인지, 피부·모발 유형(밝은/어두운, Fitz)이 적응 대상인지 위험 대상인지 | `/comparisons/1/procedures/0/best_for`, `/comparisons/6/procedures/0/best_for`, `/comparisons/5/procedures/*` | 열림 |

## C 가 0인 이유

- B1~B9 는 원장에 없는 사실이다. 사용자에게 사실을 추측해 정하게 하지 않는다(재개 노트 미결 2 규칙). 원장 수정 여부(예: B9 오기 확인)는 원장 관리자 확인 과제이지 1차 수집 범위의 선택지가 아니다.
- F1~F7 은 여러 원장을 모은 뒤 공통 의미 모델 단계에서 정할 일이다. 지금 선택지를 만들면 한 원장만 보고 의미를 확정하게 된다.
- 형태소 분석기 설정·사용자 사전 여부는 에이전트 판단이며, 브리프대로 기본 결과를 보존했다.
- 따라서 지금 사용자에게 올릴 선택 대기는 없다. 이는 미결이 없다는 뜻이 아니다 — B 9묶음과 F 7묶음이 열려 있다.
