# extracted.json — 미결·한계 기록

> **1차 범위 종료(자체 판정) · 원장 전체 완료 아님.** 아래 B·I·P·F 는 열린 상태로 남는다. 사용자 결정 필요 C 는 0 이다 — 근거는 맨 아래 「C 0 의 근거」.
> 문자 뜻: **A** 에이전트 추출/해석 오류 · **B** 원문 정보 부족 · **C** 현재 사용자 결정 필요 · **I** 원문 내 불일치 · **P** 잠정 해석 · **F** 후속 의미 조사 · **K** 알려진 분석 한계. 원문 내 불일치는 C 가 아니다. 원본 변경 제안은 원본 보존 지시 아래 후속 확인 후보이며 지금 선택 대기로 올리지 않는다.

## 요약

| 구분 | 수 | 상태 |
|---|---|---|
| A 에이전트 오류 | 3 | 해결·재검증(아래) |
| B 원문 정보 부족 | 10 | 열림 — 부족한 정보와 제한되는 활용을 적었다. 사용자에게 사실을 정하라고 묻지 않는다 |
| I 원문 내 불일치 | 13 | 열림 — 원문 보존. 해석·정규화 단계에서 처리 규칙 필요 |
| P 잠정 해석 | 4 | 열림 — 확정 데이터로 쓰지 않음 |
| F 후속 의미 조사 | 11 | 열림 — 공통 의미 모델·실버 설계 단계 과제 |
| K 알려진 분석 한계 | 5 | 기록됨 — 1차 종료를 막지 않음 |
| C 사용자 결정 필요 | 0 | 영향 검토 후 0(근거 아래) |

## A — 에이전트 추출 오류 (해결)

- **A1** 수량 후보 규칙이 코드 속 숫자(`G6PD` 의 6, `5-5-5` 의 5-5)를 수량·범위로 잡았다(1차 빌드 전 점검). 숫자 앞뒤가 영문자·숫자·「영문-」 이면 제외하고 범위 구분자를 `~` 로만 한정해 고쳤다. verify.py 가 「수량 후보에 코드 속 숫자 0」을 검사한다. `/M16/contraindications/absolute/1` 「G6PD」, `/M3/aftercare/0` 「5-5-5」.
- **A2** 부위 키워드 규칙의 「등」이 나열 표지 「등(etc.)」과 겹쳐 오탐이 대부분이었다. 규칙에서 빼고 실제 부위 출현(`/M14/indications/extended/3` 「등 지방」)은 수동 표현 MX180 으로 기록했다.

- **A3** 별도 읽기 검토(규칙·수동 후보가 하나도 걸리지 않은 어절 전수 열람, [reading-review-uncovered.json](./reading-review-uncovered.json))에서 표현 규칙의 표지 누락을 찾았다 — 경과·지속(일시적·지속·호전·회복·누적·만성), 정도 부사(더·잘·가장·완전히·직접·스스로), 상태(활동성·진행 중·감염성), 범위 한정(「…만」: 부위에만·표적만·지방세포만), 인과(때문에·로 인한·에 의해), 종점(최종). 범주 6개를 추가해 재빌드했다(표현 후보 3,716 → 3,907). 보강 뒤 남은 미포착 어절 2,664(서로 다른 1,393)는 내용어이며, 표지 글자를 포함한 27출현도 내용어 일부(심장·흡수·반흔 등)임을 확인했다.

## B — 원문 정보 부족

- **B1** safety 그룹 기준이 없다. common/uncommon/serious(+emergency) 를 빈도로 나눴는지 중증도로 나눴는지 원장에 정의가 없고, serious 가 null 인 항목(M10·M13)이 「없음」인지 「미기재」인지도 없다. 일부 사건은 조건·빈도 없이 한 단어다(`/M6/safety/serious/0` 「감염」). → 부작용 빈도·중증도 속성으로 옮길 때 그룹 이름만으로 값을 채울 수 없다.
- **B2** 빈도어에 수치·분모·기준 집단이 없다 — 드물게·극히 드묾·드물지만·대부분·일부·흔함(`/M11/safety/serious/1` 「드물게」, `/M16/safety/serious/0` 「극히 드묾」, `/M15/safety/common/1` 「대부분 호전」). 수치는 `/M15/safety/serious/0` 「1% 이내」 하나뿐이며 분모가 없다. → 빈도를 수치로 바꿀 수 없다(바꾸지 않는다).
- **B3** 필드가 담아야 할 정보가 원문에 없다 — 기간 값이 없는 duration(`/M12/onset_duration/duration`, `/M13/onset_duration/duration`, `/M17/onset_duration/duration`), 하위 방법 일부만 있는 기전(`/M9/mechanism` 은 RF 만, HIFU 없음). → 지속 기간·기전 질의에 답할 값이 없다.
- **B4** 기간 없는 시간어 — 「최근 수술 이력」(`/M10/contraindications/relative/2`), 「최근 과도한 자외선 노출」(`/M8/contraindications/relative/0`). → 금기 적용 기간을 정할 수 없다.
- **B5** 하위 유형 일부만 값이 있다 — M3 PDLLA(쥬베룩) 기간 없음(`/M3/overview` vs `/M3/onset_duration/duration`), M2 PLLA 기간 없음(`/M2/overview` vs `/M2/onset_duration/duration`), M17 peak 은 아디포셀만(`/M17/onset_duration/peak`). → 제품·방법별 시간 질의가 일부만 가능하다.
- **B6** 수식·대상이 생략돼 있다 — 「운동 병행 시 효과 극대화」의 효과 대상(`/M10/aftercare/2`), 「드물게 메스꺼움, 피로감, 감기 비슷한 증상」에서 「드물게」의 적용 범위(`/M1/safety/serious/0`), 「미세한 바늘(0.2~2.0mm)」의 수치가 길이인지(`/M12/mechanism`). → 수식 대상을 연결할 때 원문만으로 확정할 수 없다. 임의로 채우지 않는다.
- **B7** 출처 상세가 없다 — 「일반 의학 지식」 5항목(M10·M13·M14·M16·M6), 「임상적 피부관리 N장」 11항목(판·저자·쪽 없음). 외부 서지가 완전한 것은 M7 하나다. → 근거 수준·출처 추적을 항목 단위로만 할 수 있다.
- **B8** indications 의 primary/extended, contraindications 의 absolute/relative 구분 기준이 원장에 없다. → 등급을 의미 속성으로 쓸 때 기준을 원문에서 가져올 수 없다.
- **B9** 메타데이터 코드의 뜻이 없다 — source_type(kr/general/us), guardrail_version(전부 1.0), extracted_at(전부 2026-03-28), updated(M3 만 2026-07-11). → 버전·갱신 이력 해석 불가. 값은 보존했다.
- **B10** 임계·정도 값이 없다 — 「부적절한 에너지 설정」「에너지가 과한 경우」「너무 높은 에너지」「과도한 열 작용」「일정 온도 이하」「심각한 심폐질환」「일반적인 니들RF」(`/M11/safety/serious/1`, `/M8/safety/serious/0`, `/M9/safety/uncommon/0`, `/M9/safety/serious/1`, `/M14/mechanism`, `/M10/contraindications/relative/1`, `/M11/contraindications/relative/0`). → 조건을 수치 조건으로 만들 수 없다.

## I — 원문 내 불일치 (C 아님)

- **I1** HIFES(name) / HIFEM(mechanism) 약칭 차이 — `/M10/name`, `/M10/mechanism`.
- **I2** 래디에스(`/M2/mechanism`) / 래디어스(`/M3/overview`·`/M3/mechanism`·`/M3/onset_duration/duration`) 표기 차이.
- **I3** M11 mechanism 「색소침착 등의 부작용이 없고」 vs safety/uncommon 「색소침착 (… 위험이 매우 작음)」.
- **I4** M2 aftercare 「시술 후 … 무균 상태에서 시술해야 하며」 — 시점 혼재(`/M2/aftercare/2`).
- **I5** M9 같은 금속 조건이 absolute·relative 두 등급에 있음(`/M9/contraindications/absolute/0`, `/M9/contraindications/relative/2`).
- **I6** safety 그룹에 사건이 아닌 진술 — 효과 감소/부족(`/M1/safety/serious/1`, `/M1/safety/uncommon/1`, `/M17/safety/uncommon/0`), 사건 부재 주장(`/M5/safety/serious/0`), 근거 상태(`/M17/safety/serious/0`), 결과 차이·평가(`/M5/safety/uncommon/0`, `/M7/safety/uncommon/4`), 교정 방법(`/M9/safety/serious/2`).
- **I7** onset_duration/duration 이 기간이 아닌 병합 효과 진술(`/M13/onset_duration/duration`).
- **I8** contraindications 에 환자 조건이 아닌 진술 — 위험 진술(`/M15/contraindications/absolute/0`), 효과 진술(`/M5/contraindications/relative/2`), 평가 미흡 권고(`/M17/contraindications/relative/2`), 시술 방식 권고(`/M9/contraindications/relative/3`).
- **I9** uncommon 그룹 값 안 「특히 아시안 피부에서 흔함」(`/M8/safety/uncommon/0`).
- **I10** 한 항목 안 같은 대상 중복 — 반흔/비후성 반흔(`/M15/safety/serious/0`·`/1`), 모공각화증/닭살 (모공각화증)(`/M15/indications/primary/2`, `/M15/indications/extended/7`).
- **I11** 바이오스티뮬레이터 serious 의 「필러가 혈관에 들어갈 위험」(`/M3/safety/serious/1`).
- **I12** M1 aftercare 두 값 내용 겹침(`/M1/aftercare/0`, `/M1/aftercare/1`).
- **I13** aftercare·indications 칸의 병합 권고 — `/M5/aftercare/2`, `/M5/indications/extended/3` 「다른 시술과 병행 — …」.

I 항목은 원문 보존 지시에 따라 고치지 않았다. 원본 수정 여부는 후속 확인 후보이고, 지금 사용자 선택 대기로 올리지 않는다.

## P — 잠정 해석

- **P1** related_techniques 「기법명 + ` -- `/` — ` + 관계 설명」 분할(OB-S00-06). 관계 종류 미확정.
- **P2** 괄호의 역할 다중성(풀이·조건·빈도·예방·하위 유형·성분, OB-S00-07).
- **P3** 기호 「+」「/」「-」의 값별 용법 차이 — README 규칙을 일괄 적용하지 않음(OB-S00-08, OB-S06-05).
- **P4** overview 따옴표 이름 = 브랜드명 후보. 원문이 「브랜드명」이라 명시한 항목(M10·M11·M14·M9)과 「이름」이라고만 한 항목(M13·M16)·「로 널리 알려져」(M4) 가 있다.

## F — 후속 의미 조사

- **F1** 부위 역할 구분 — 시술·채취·주입·이식·금기·위험 조건 부위(OB-S08-03, OB-S10-05, OB-S14-01, OB-S01-05).
- **F2** indications 값 분해 — 부위·고민·목적·기법이 한 값·한 목록에 섞임(OB-S09-04, OB-S10-04, OB-S03-03).
- **F3** 하위 유형(제품·재료·기법·성분) 조건부 값 — M2·M3·M7·M8·M15·M16·M17(OB-S06-02, OB-S07-01, OB-S15-02, OB-S16-02).
- **F4** 수식·빈도·정도·지속성 표현의 대상 연결(OB-S02-02, OB-S05-01, OB-S12-01, OB-S15-03, OB-S17-04 등).
- **F5** 시간 역할 구분 — 효과 시작·정점·지속, 부작용 지속, 관리 기간, 재시술 간격, 기준 시점(OB-S05-03, OB-S13-02, OB-S06-05, OB-S10-01).
- **F6** 다른 시술 언급과 관계 — related_techniques·overview·mechanism·aftercare 안의 시술명. 이 원장 name 과 같은 문자열은 `cross_reference_name` 후보로만 있다. 이 원장 밖 이름(IPL·PDT·메조테라피·SVF·지방흡입 등)은 다른 원장과 연결 과제(OB-S01-06, OB-S04-04, OB-S05-04, OB-S13-03).
- **F7** 표기 변형 정규화 — 띄어쓰기·구분자·풀이 차이(OB-S00-10, OB-S00-06, OB-S15-02).
- **F8** 역사·규제·근거 주장의 근거 수준(연도·FDA/식약처·RCT·「보고 없음」·「연구 부족」). 사실 검증 안 함(OB-S09-01, OB-S09-03, OB-S11-03, OB-S03-05).
- **F9** 같은 조건의 항목 간 금기 등급 차이(OB-S00-09).
- **F10** 수치의 대상·분모 — 면적 20%, 생체이용률 100%, 흡수율 10~30%, 생착률 30~70%, 1% 이내(OB-S02-03, OB-S07-02, OB-S14-02).
- **F11** 항목 범위·명칭 — name/name_en 의 「/」 병기, 총칭 vs 대표 시술, 레이저 vs Laser & Light(OB-S01-02, OB-S06-04, OB-S12-02, OB-S16-02, OB-S04-03).

## K — 알려진 분석 한계

- **K1** 형태소 오분절·오태깅 34출현(규칙 20)을 출현별로 표시했다(교정 아님) — [segmentation-review.json](./segmentation-review.json), 각 review-part §4. 주요 영향: 부위어 소실(이중턱→이/MM+중턱, 이마→이/MM+마), 질환명 소실(복직근이개→이/JKS), 층위 뒤바뀜(진피하→진+피하), 단위 오인(초회통과→초/NNB+회/NNB), 부정 표지 품사 소실(미착용→미/NNG), 사건 명사 부사화(멍/MAG 6출현).
- **K2** 형태는 맞고 품사만 고유명사(NNP)로 붙은 일반 명사(수유·붓기·보정·강화·농양·두피·제모·생착률 등)는 출현별로 표시하지 않았다. 의미 구간 손실이 없다고 판단했다.
- **K3** 규칙 기반 표현 후보(keyword·regex)의 오탐은 판정하지 않았다 — 예: condition_scope 「\S+ 시」가 「시술 시」 외 다른 「시」를 잡을 수 있고, time_relative 「중」「간」, site 「배」「목」「코」 단음절이 다른 뜻으로 걸릴 수 있다. 후보는 탐색용이다.
- **K4** name_en(영문) 17값은 Kiwi 로 분석해 SL 토큰만 남는다. 영어 형태 분석이 아니다.
- **K5** segment.clause 는 괄호 밖 「, 」·구분자 기준 휴리스틱이라 명사 나열도 「절」로 잘린다. segment.sentence 는 「.」+공백 기준이다.

3회차 대조 범위(의심 품사 전 출현 + 전문어·부위어·부작용어·부정/가능성 표지 약 170개 낱말) 밖 토큰의 정확성은 보장하지 않는다.

## C 0 의 근거

- 남은 B 는 원문에 정보가 없다는 기록이다. 사용자 추측으로 채울 대상이 아니다.
- I 는 원문 내 불일치로 보존했다. 원본 수정은 원본 보존 지시 아래 후속 확인 후보다.
- P·F 는 공통 의미 모델·실버 설계 단계에서 다른 원장과 함께 판단할 과제다. 지금 한 원장만 보고 사용자에게 고르게 하면 적용 범위가 정해지지 않는다.
- 도구 선택(Kiwi·cong·사용자 사전 없음)·구획 분할·규칙 설계는 에이전트 판단으로 기록했다. 사용자 결정으로 넘기지 않았다.
- 따라서 지금 사용자 선택을 요청할 항목은 없다. 이 판정은 위 처리 상태와 영향 검토에 근거하며, 승인·확정을 뜻하지 않는다.
