# 재개 노트 — phub-ledger-redesign (Procedure Hub)

**지금(11-15)**: ① 사전(22표 · 보강 1차) · **② 시술/케이스**(procedure 136 · procedure_material · procedure_case 265 · case_method · case_product · 계열 M18 추가) · **③ 관계**(silver 20표 — indication · outcome · adverse_risk(+frequency · factor · guidance · rating) · contraindication · procedure_relation(+effect) · package(+item · condition · schedule) · recovery · citation(+link · translation) — 표 구조 정본 silver-model/drafts/relation-pilot/relation-notes.md §9-2, 합치기 notes/relation-notes.md) 가 silver 에 들어갔다. 관계 보완 · 사전 보강 2차 완료(11-15).
**다음**: 원장 확인 목록 한 장(안 닿는 고민 18 · 계열만 50 · 보류 5 · 원장≠사전 제품 · ② 코드 없는 시술 종류 · 인터넷 조사 여부) → silver 통합 검사 + ERD 문서 → 상품(market-pricing) → gold → 마감(커밋 · PR). 미룬 작은 것: 골수 · method 별칭 띄어쓰기 8 · modality_alias 용도 · 멀티비타민/미네랄 성분 펼치기.

## 워크트리

- 현재 작업 레포: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`
- 새 작업 디렉토리: `orchestration/work/phub-ledger-redesign/`
- 별도 워크트리·브랜치 생성, 발주 스크립트 실행은 하지 않았다.

## 1. 지금

- [x] batch-03 5개 1차 범위 종료·누적16/21. 표현 후보 공백·원문 부족·후속 의미 과제는 열린 채 유지한다.
- [x] batch-04 마지막5개 1차 수집 범위 종료. 누적21/21. 알려진 분석 한계·원문 부족·후속 의미 과제는 열린 상태. 원장 전체 완료 아님.
- [!] 원장 전체 미완료: 원문 부족 B 10묶음·잠정 2·보류 2·후속 의미 조사 9가 남아 있다. [미결 기록](./first-pass/procedure-profiles/issues.md)을 참조한다.
- [!] 형태소 출력은 교정하지 않았다. 알려진 오류는 표시 또는 위치 기록으로 남겼다. 지정 품사·서명 밖 형태소 정확성 및 모든 의미 관계를 검증했다고 주장하지 않는다.
- [!] 현재 사용자 선택 대기는 0건이다. 전 C1은 도구 설정 판단으로, C2는 후속 의미 조사 전 재검토로 보류했다. 사용자 결정을 받은 것으로 취급하지 않는다.
- [!] 실제 조사·작성은 반드시 워커 발주로 수행한다. 원본·기존 작업 수정·삭제 금지, 복구 미요청 상태를 유지한다.

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-11 | 제품 v5 를 silver 확정: product 308 · organization 192 · product_organization 558(브랜드·제조원·수입사·유통사·허가권자 / 원장·외부 조사·식약처) · 회사 없음 50 · 영어 빈 117. 메모 속 회사 26 · 확인 목록 59 · 시술 이름 후보 4 는 notes/ 에 남김. 시술 중점으론 충분 — 제품은 나중에 따로 갱신 | 사용자 「이정보만 해도 충분한거 아니야 시술 중점으로 보면」「나중에 제품 쪽만 업데이트 해도 되지」 |
| 2026-11-11 | 사용자 웹 조사(research-todo/*-filled.csv) 반영: 회사 7 · 영어 이름 112 → source/name_en_source 「외부 조사」. PLLA-SCA 는 스컬트라와 합치지 않음(식약처 기록과 어긋남 → 확인 목록) · 하모니카 = HArmonyCa 합침 · 미스코·엑소힐러·크라이오셀 → 시술 이름 후보 · 캐번실 → 실 모양 후보 · 오기 의심은 고치지 않고 원장 작성자 확인 목록. 공개 자료로는 여기가 한계(사용자) | 사용자 「추천대로 가자」 |
| 2026-11-11 | 제품의 회사는 한 칸(manufacturer)이 아니라 제품-회사 역할 표(product_organization: 브랜드 · 제조원 · 수입사 · 유통사 · 허가권자 + 출처 원장/외부 조사/식약처). 원장 값 = 대개 브랜드, 식약처(step1) = 제조원·수입사·유통사. 원 제조사는 조직 연혁(current_org_code). | 사용자 「제조사 유통사 수입사 다 다를걸」 |
| 2026-11-11 | 제품 v2 판단: 아큐탄(성분 이소트레티노인 · 사람 조건으로)·콘투락투벡스겔(=컨트라투벡스)·헤어맥스 → 시술 아님, archive/not-procedure-products.csv · 벨카이라=카이벨라 한 행(국내 철수, 브이올렛 등 같은 성분 다른 제품은 합치지 않음) · 노바스템 = 자가혈 키트 · 미라셀 = 장비+키트 세트(자가혈·골수) · 잼버실 PDO · 인모드FX 비침습 RF(M9) · 울트라V 재질 빈칸(회사명) · 리바이브 글리세롤 → 리바이브에 합침 · name_check(확인/웹 미확인/웹·식약처 미확인 — 식약처 실제 조회 시만) · 오기 의심은 안 고침 | 사용자 11-11 붙여넣은 검토·조사 |
| 2026-11-11 | 제품 manufacturer = 현재 회사, 원 제조사는 조직 행(current_org_code·description 연혁) + 제품 description. 아그네스 = AGNES = 아그네스메디컬(원장 「제니스·고우리엔티」 오류, 제니스 존재 미확인) · 캔델라 = 시너론캔델라·시너론(한 조직) · 사이노슈어 루트로닉 = 사이노슈어+루트로닉(2024 합병) · 벡터스(원 팔로마)·펠레베(원 엘먼) → 사이노슈어 루트로닉 · 아발란체 → 포토나 · 에스테필 → 리젠바이오텍(휴메딕스 유통, 「레지메드」 오류, 주사제). 영어 이름 빈칸 유지 · 원장(브론즈) 수정 안 함. | 사용자 11-11 붙여넣은 조사 |
| 2026-11-11 | 시크릿(시크릿RF) 제조사 = 클래시스(현재) · 원 제조사 이루다(Ilooda, 원장 표기 「일루다」) — 2024-10-01 클래시스 흡수합병. 원장 「아이닉」은 오류. 시크릿맥스(M9)는 별개 제품 유지. | 사용자 11-11 붙여넣은 조사(FDA 510(k)·기사·클래시스 사이트) |
| 2026-11-11 | 올리지오·올리지오X 제조사 = 원텍(원장 taxonomy 「원텍 · 모노폴라」 + 사용자 외부 확인 기사 4건). products.json·taxonomy 제품목록·올리지오X detail 의 「클래시스」는 원장 오류로 notes 기록. 원장(브론즈) 자체 수정은 사용자 결정 대기. | 사용자 11-11 붙여넣은 조사 |
| 2026-11-11 | 제네시스는 제품 아님 → 시술(케이스) 이름: 1064nm + 롱펄스. 원장 3곳(taxonomy 「제네시스토닝」 detail 롱펄스 1064nm · 비교표 「제네시스 (Nd:YAG 롱펄스)」 · 가격표 「제네시스 (전체얼굴)」). 「제네시스토닝」은 같은 케이스의 다른 이름. 케이스 설계 때 주의: 피코제네시스(피코초 레이저)는 다른 케이스(원장엔 없음) · Q-스위치와 함께 적힌 「제네시스 토닝」은 시술 2개(원장엔 없음). (코디가 브리프에 「제네시스 = 장비」를 외부 지식으로 넣은 것은 오류) | 사용자 11-11 붙여넣은 설명 |
| 2026-11-10 | 방법 사전 = 투여 경로·주입 방식·도구·에너지 조사 방식·흡수 촉진(+재료 처리). 니들은 둘 다 둠: 재료 MAT-300(바늘 자체가 자극·절단) ≠ 방법 MET-040 니들 주입(약을 넣는 통로, 캐뉼러와 선택지). 케이스 이름(레이저토닝)·시술 이름(수액)을 방법의 aliases 에 넣지 않는다. | 사용자 「둘다 다른 니들 아니야」「그렇게 해서 실버로 가자」 |
| 2026-11-10 | 재료·기전·조직 확정본(silver/): 이름 = name_ko·name_en·abbr(+aliases), 괄호 없음, 파장 wavelength_nm. 전달 방식·RF 극성·비박피 미세 열손상 → method-candidates. 원장에 없는 영어 이름은 남기되 name_en_source(원장/보충)로 구분. 파장 등 수치는 material_spec(재료·항목[파장/농도/온도/주파수/깊이/분자량/입자 크기]·값·단위·근거) 테이블로(wavelength_nm 칸 폐지). | 사용자 「영어 한국어 약어」「추천으로」 |
| 2026-11-10 | 상품 = 제품·시술 + 수량(샷·cc·줄·회) + 가격(병원 무관, 예: 써마지 300샷). 원장 market-pricing 122행이 상품 — 시술·케이스를 다 만든 뒤에 다룬다(지금 설계에서 제외, 브론즈 보존). 패키지는 상품 아님 = 시너지. (앞 행의 「상품 = 병원 + …」「원장에 상품 없음」은 이 행으로 대체) | 사용자 11-10 「써마지 300샷이 상품이야?」「나중에 우리 시술 다 만들고 해도 되는거 아니야」 |
| 2026-11-10 | 상품 = 병원 + 제품·시술 + 수량(샷·cc·회) + 가격(예: 데이뷰 써마지 300샷) — 원장에 없음, 범위 밖. 원장 패키지(쁘띠·보톡스+필러·레시피·연간 플랜)는 상품이 아니라 시술 조합(시너지) 데이터 → 시술 간 관계(보완·같은 날·순서·간격·회차). 백옥주사 등 마케팅 이름 = 널리 쓰는 시술 이름(입구). 수액은 성분이 다르면 다른 시술(같은 계열 안). | 사용자 11-10 「데이뷰 써마지 300샷」「패키지도 시너지」「백옥주사는 많이 쓰는 시술」「같은 계열에 다른 시술」 |
| 2026-11-10 | 프로시져 허브 = 시술 원장. 상품(메뉴)은 각 피부과가 붙인 판매 이름이라 범위 밖(피부과 상품 → 케이스 연결은 나중). 울쎄라·보툴렉스는 제품(장비·약) → 시술. 입구 = 고민·시술 이름·제품. 부작용 위험(케이스 × 부작용)에 생기는 자리 칸(시술 자리와 다를 때만, 예: 이마 보톡스 → 눈꺼풀 안검하수). 논의 자리 = Claude Docs 「Procedure Hub 실버 데이터 구조」. | 사용자 11-10 「상품에 대한 영역이 없다고 봐야」「울쎄라가 상품이 아니라 제품에 연결된 시술」「그렇게 하는게 좋을거 같은데」 |
| 2026-11-10 | 시술 구조 = 계열(modality) → 시술 종류(재료 종류 + 작용 원리) → 케이스(작용 대상·부위·방법·제품·세부 재료, 원장이 말한 조합만). 작용 대상은 시술 정체 아님(보톡스 1개 · 스킨보톡스·다한증은 케이스). 기기 리프팅은 에너지 종류별 시술 종류 여럿. 레이저는 표적·파장·프락셔널을 케이스로. 계열=시술 1:1이면 설명은 시술 종류에. | 사용자 「다 같은 보톡스 아니야」「계열 - 시술종류 - 케이스」「발주 해주세요」 |
| 2026-11-10 | material·tissue 단독 CSV 는 정규화 안 됨(상·하위 나란히·콜라겐 두 테이블·조직 아닌 것·단위 제각각) → 후보 목록으로만. 시술·material·tissue 를 한 세트로, M1·M8·M16 시범부터. material 은 시술이 쓰는 것만·parent_code · tissue 는 층·구조(+표적)만 · 레이저 재료=파장, 펄스=원리. | 사용자 「정규화 한거야?」「시술하고 3개 세트로」「해보자」 |
| 2026-11-10 | 시술 정의 = 재료·에너지(material) + 작용 대상 조직(tissue) + 작용 원리가 같으면 같은 시술. 부위는 시술 정체 아님(부위 테이블 따로·나중 연결). 스킨보톡스 = 메조보톡스(= 더모톡신) 한 시술, 보톡스와는 다른 시술(대상 근육 vs 피지샘·모공). procedure 칸 = code·name_ko·name_en·modality_code·material_code·target_code·principle·overview·mechanism·method + procedure_name(확인된 같은 시술 이름만). material·tissue 값 목록 먼저. | 사용자 11-10 「tissue 개념이구나 진행해」 · 붙여넣은 스킨보톡스 비교 |
| 2026-11-10 | `modality_alias.csv` 는 유지(삭제 안 함). 용도 = 원장 표기 → modality 코드 매핑(나중에 데이터 모을 때 대비용) — 의미상 동의어 아님. 알려진 한계: 표기 형태로만 분류 · 원장별 중복 행 · 시술 이름(환자용)·범위 다른 이름(PRP/엑소좀) 섞임 · 타입 오류(synergy M5-PRP). 쓰임은 나중에 다시 판단. CSV 는 UTF-8 BOM. | 사용자 「일단 냅둬보자 나중에 어떻게 쓰일지 다시 판단」 |
| 2026-11-10 | 「계열」= taxonomy `modality[]` 17개(M1~M17). 용어는 modality 로. modality 는 유지(RF·HIFU 모두 기기 리프팅). 잘못된 것은 정보가 놓인 층(원장이 RF 기전을 modality 자리에 적음)과 소속(M16 의 DCA·지방분해주사 등). modality 테이블 = code·name_ko·name_en·overview·mechanism(하위 전부에 맞는 공통 수준, 원장 문장 근거) + modality_alias. group·basis·출처 메타는 넣지 않음. 실버 = 질문에 필요한 정보만 정규화(브론즈 전수 보존과 구분). | 사용자 11-10 대화 |
| 2026-11-10 | 계열 설계는 연결 관계 없이 계열 테이블 자체만(하위분류·겹침·상속·다른 원장 연결 제외). 연결 관계부터 생각하다 꼬였다는 판단 — 개체 먼저, 관계는 나중. | 사용자 「연결 관계 생각하지 말고 … 계속 연결 관계만 생각하다가 꼬인거 아니야」 · [지시서](./family-design-instructions.md) |
| 2026-11-10 | 부작용 틀 = 개념(명칭·별칭·현상) / 적용 케이스(시술+좁힘) / 케이스×부작용 값 하나 + 출처 여럿. 시범1 판정: D2 등급·수치 병기 · D6 taxonomy 항목·제품 common/serious 키는 빈도 근거 아님(계열 값 상속) · D1·D3·D4·D5·D7 원장 수치 충돌은 complications 채택(나머지 출처) · D8 케이스 부적합 의심 표시. 다음 시범 필러. | 사용자 「응」(추천대로) · 「필러 해보자」 |
| 2026-11-09 | 이슈 그루핑 결과·발주 기록·브리프·검토 보고서 삭제 및 관련 발주 이력 제거. 새 지시 전 재발주·추가 파일 작업 금지. 원본과 first-pass 보존. | 사용자 삭제 지시 |
| 2026-11-09 | 마지막5개를 Opus 원장별 워커로 발주. 전체 파악 후 미결을 원인별로 묶고 실제 설계 선택만 제시한다. 조사 오류/누락은 에이전트가 해결하며 자료부족을 추측 선택으로 바꾸지 않는다. | 사용자 「응 그렇게 가자 … 마지막 배치도 보내자」 |
| 2026-11-09 | batch-03의 pih-risk는 기존 실행 유지. 다른4개는 해당 출력 폴더 삭제 후 원본부터 새 Opus 워커로 조사한다. 원본·앞선11개 결과는 유지한다. | 사용자 「pih-risk는 돌고 있으니까 빼고 다른4개 다시 삭제하고 처음부터」 |
| 2026-11-09 | 다음 batch-03 진행 승인. Opus5명·1워커1원장, 큰 원장 구획 분할·읽기 기록·전체 누락 검증·추가 서브에이전트 금지 유지. | 사용자 「응 다음 가자」 및 이전 합의 |
| 2026-11-09 | 다음 배치 진행 승인. 분량이 많으면 상위 문맥을 유지해 나누고 구획별 읽기 상태와 전체 범위를 추적한다. 구획 일부 완료를 원장 1차 종료로 세지 않는다. | 사용자 「다음 배치 가자 너무 많으면 쪼개는거는 안 까먹었지」 |
| 2026-11-09 | 출력은 원본 컬럼명·자료형·원문 값·잠정 관찰로 분리한다. 1차 기준 충족 시 다음 원장으로 넘어가고, 알려진 분석 한계와 의미 과제는 기록해 후속으로 남긴다. Opus 5명이 5개 원장을 병렬 조사한다. | 사용자 「응 반영하고 발주해」 및 직전 합의 |
| 2026-11-09 | 코디 검토 결과 1차 수집 범위 종료 조건을 충족했다. W1 두 출현은 미교정 상태의 알려진 사례로 기록했고 W2 검증 한계도 명시했다. 원장 전체·의미 조사·정규화 완료 판정과 구분한다. | 재검토 리포트·최종 메모 실물 확인 및 코디 verify.py 재실행 failure_count=0 |
| 2026-11-09 | 실제 조사·산출물 작성은 반드시 별도 워커에게 발주한다. 메인은 범위 합의·발주·검토만 담당한다. 첫 원장은 procedure-profiles.json 전체로 승인됐다. | 사용자 진행 지시와 워커 발주 지시 |
| 2026-11-09 | 이전 세션을 이어 고치지 않고 원본과 현재 목표를 기준으로 새로 시작한다. | 이번 대화 사용자 지시 |
| 2026-11-09 | 새 작업 디렉토리는 `orchestration/work/phub-ledger-redesign/`이다. | 사용자 디렉토리 생성 요청 및 생성 결과 |
| 2026-11-09 | 목표 참고 문서를 바탕으로 이 재개 노트를 만든다. 원본 README는 유지한다. | 사용자 재개 노트 작성 요청 |
| 2026-11-09 | 원본·기존 작업 폴더는 수정·삭제하지 않는다. 삭제·덮어쓰기가 필요하면 정확한 경로와 영향을 제시하고 확인받는다. | 이번 대화 사용자 지시 |
| 2026-11-09 | 복구는 조사 선행 조건이 아니며, 별도 요청 없이 시작하지 않는다. | 이번 대화 사용자 지시 |
| 2026-11-09 | 참고 문서의 용어·목표는 참고하되, 이전 완료 상태·삭제 범위·진행 이력은 신뢰하지 않는다. | 이번 대화 사용자 지시 |
| 2026-11-09 | 1차 조사는 구조·전체 값·문맥·형태소·복합 표현 수집으로 수행하고, 개념 식별·의미 관계 확정은 후속 단계로 구분한다. 작업 스킬을 작성해 재개 시 참고한다. | 이번 대화의 방법 논의 및 사용자 스킬 작성 요청 |

### 원본과 기존 작업의 취급

- 원장 3판: [phub-ledger/](../phub-recommend/bronze/phub-ledger/)
- 목표 참고: [2026-11-09/README.md](../../../reference/2026-11-09/README.md)
- 사용자는 이전 삭제 사고 후 Git 추적 파일 2,642개를 복구했으나 미커밋 수정·미추적 파일은 복구되지 않았다고 설명했다. 원장 24개 파일 보존·당시 해시 불변 역시 사용자 제공 배경이며, 이번 세션에서 새로 검증한 결과가 아니다.
- 목표 참고 문서의 §6 삭제·초기화 기록은 이번 작업의 실행 지시 또는 현재 상태 근거로 사용하지 않는다.

### 목표·용어·설계 기준

아래는 목표 참고 문서 §1~5를 옮긴 것이다. 아래의 진행 단계는 목표이며 실행 완료를 뜻하지 않는다. 현재 사용자 지시가 우선한다.

### 1. 최종 목표

**원장 전체의 실제 정보를 조사하고, 의미와 관계를 보존해 정규화한 실버 데이터·ERD·공통 의미 모델을 만든다. 이를 바탕으로 질문 응답·추천·조회에 사용할 골드를 구성한다.**

지원하려는 질문은 다음과 같다. 아래는 기능 범위를 설명하기 위한 예이며, 특정 시술의 효과나 안전성을 승인한 문장이 아니다.

| 질문 범위 | 예시 | 필요한 정보 |
|---|---|---|
| 시술 | 이 시술은 무엇이고 어디에 쓰는가? | 시술·제품·기법·성분·적용 부위·목적·효과 |
| 부위·고민 | 이 부위의 이 고민에는 어떤 시술이 있는가? | 부위와 고민의 구분, 시술과의 적용 관계·조건 |
| 부작용 | 어떤 부작용이 있고 얼마나 자주, 언제, 얼마나 오래 나타나는가? | 사건·부위·빈도·정도·발현·지속·경과·조건·근거 |
| 시술 조합 | 함께 받으면 좋은 시술은 무엇인가? | 보완 관계·기대 효과·적용 조건·근거 |
| 동시 가능 여부 | 같은 날 받아도 되는가? | 동시 시행 가능 여부·제한·예외 |
| 순서·간격 | 어떤 순서로 받고 얼마나 간격을 두는가? | 방향 있는 선후 관계·최소/권장 간격·기준 시점·조건·이유 |
| 회피 관계 | 함께 피해야 하는 시술은 무엇인가? | 충돌·회피 관계와 적용 범위·조건 |

조사 문서나 형태소 분석 결과를 많이 만드는 것이 최종 목표는 아니다. 조사 결과가 개념·관계 정의와 ERD, 실제 데이터 변환·검증으로 이어져야 한다.

### 2. 각 층의 정의

**브론즈·실버·골드는 데이터 가공 단계이고, 시맨틱 레이어는 데이터의 의미와 사용 규칙을 실제 데이터 구조에 연결하는 논리적 계층이다.**

| 구분 | 정의 | 우리 작업의 내용 |
|---|---|---|
| 브론즈 | 들어온 자료를 원문·출처·버전 그대로 보존하는 층 | 원장 JSON과 원본 위치·버전·해시. 복합 문구·불일치·누락도 보존한다. 원장 수정은 별도 이력으로 구분한다. |
| 실버 | 정보를 분리·정규화하고 개체·관계·조건·근거를 일관된 구조로 연결한 데이터 층 | 시술·제품·성분·부위·고민·사건 등을 구분하고, 수식과 조건을 해당 대상에 연결한다. 원문 근거·불확실성·미결도 보존한다. |
| 골드 | 특정 서비스 목적에 맞춰 실버를 조합·집계·가공한 데이터 층 | 시술 상세, 부위·고민별 후보, 조합·순서·간격 등 조회·검색·추천 목적의 데이터. 원문에 없는 사실을 임의로 추가하는 단계가 아니다. |
| 시맨틱 레이어 | 공통 개념·관계·규칙을 실제 데이터에 연결해 일관되게 사용할 수 있도록 제공하는 논리적 계층 | 보완 관계와 동시 가능의 차이, 빈도·시간의 적용 대상, 관계의 방향·조건 등을 정의하고 실제 저장 위치·조회 경로에 매핑한다. |

시맨틱 레이어는 골드 다음에 오는 네 번째 데이터 등급이 아니다. 질문을 해석하는 기능만을 뜻하지도 않는다. 질의 처리와 서비스는 시맨틱 레이어가 제공하는 공통 정의·규칙·데이터 매핑을 사용한다.

공통 의미 정의는 실버 설계 시점부터 함께 만든다. 실버와 골드, 질의 처리에서 같은 개념의 뜻을 서로 다르게 정의하지 않는다.

### 3. 온톨로지·ERD·노드·엣지의 구분

| 용어 | 역할 |
|---|---|
| 온톨로지·공통 의미 모델 | 어떤 개념이 있고, 각각 무엇을 뜻하며, 어떤 관계·속성·제약을 갖는지 정의한다. |
| ERD | 개체·속성·관계를 데이터 구조로 표현한다. 의미 모델을 저장 구조로 구체화할 때 사용한다. |
| 노드 | 시술·제품·부위·고민·사건 등 구분해서 다룰 개체를 표현한다. |
| 엣지 | 적용·구성·보완·선후·회피 등 개체 사이의 관계를 표현한다. |
| 속성·메타데이터 | 명칭·설명·수치·단위·시간·상태·출처 등을 담는다. 대상과 역할을 정의해야 한다. |

**노드·엣지는 골드 전용 표현이 아니다. 실버부터 개체와 관계를 명시적으로 표현한다.** 골드는 이를 활용 목적에 맞게 조합·가공한다.

속성은 노드뿐 아니라 관계에도 필요하다. 예를 들어 시술 간 관계에는 적용 부위·조건·순서·간격·근거가 붙을 수 있다. 여러 대상과 조건이 함께 연결되는 적용 정보·위험 정보 등은 별도 개체로 표현할지 검토한다.

모든 정보를 자유로운 JSON 메타데이터 한 칸에 넣는 방식으로 문제를 넘기지 않는다. 질문에 필요한 정보는 명시적인 개념·관계·속성으로 정의한다.

실제 저장소를 관계형 DB로 할지 그래프 DB로 할지는 아직 정하지 않았다. 관계형 테이블과 연결 테이블로도 노드·엣지 구조를 표현할 수 있다. 노드·엣지 모델의 사용과 특정 DB 제품의 선택은 다른 결정이다.

### 4. 반드시 구분할 의미와 관계

- **시술과 부위:** 서로 분리하고 다대다로 연결한다. 보톡스는 이마·미간에 한정되지 않으며, `보톡스 이마`와 `보톡스 미간`을 서로 다른 시술의 정체로 만들지 않는다. 모든 시술×부위 조합이 유효하다고 가정하지 않는다.
- **부위의 역할:** 시술 대상 부위·부작용 발생 부위·회피해야 할 부위를 구분한다.
- **시술·제품·분류·판매 구성:** taxonomy의 같은 깊이에 있다는 이유로 같은 종류의 개체로 만들지 않는다. 제품·기법·성분/재질·형태·용량·회차·가격 옵션을 실제 값에 따라 구분한다.
- **조합의 의미:** 보완 효과가 있다는 것과 같은 날 시행할 수 있다는 것은 다르다. 선후 관계·간격·회피 조건도 따로 표현한다.
- **시간의 역할:** 효과 시작·부작용 발현·지속·소실·회복·재시술 간격·관리 시점을 구분한다.
- **수치의 대상:** 수치·단위·비교 연산·분모·대상 집단·기준 시점을 함께 보존한다. 보고 사건 구성비를 환자의 실제 발생률로 바꾸지 않는다.
- **원문과 판단:** 원장에 적혀 있다는 것, 정규화된 구조로 표현했다는 것, 사실 검증이 끝났다는 것은 다른 상태다.

#### 수식 표현도 조사·정규화 대상이다

형용사·부사 같은 수식 표현은 삭제하거나 명사 목록에 흡수하지 않는다. **무엇을 수식하는지와 적용 범위를 연결한다.**

| 표현 | 조사할 의미 | 주의점 |
|---|---|---|
| 드문·매우 드문 | 빈도 | 어떤 사건의 빈도인지 연결한다. 임의 백분율로 환산하지 않는다. |
| 깊게·얕은 | 깊이 | 주입·삽입 등 무엇의 깊이인지 연결한다. 임의 mm로 바꾸지 않는다. |
| 얇은 | 두께 | 피부 두께인지 다른 대상인지 확인한다. 주입 깊이와 구별한다. |
| 심한·경미한 | 정도·심각도 | 통증·부종 등 수식 대상을 구분한다. |
| 일시적·지속되는 | 경과·지속 특성 | 빈도와 구별하고, 시간 기준이 없는 경우 그대로 미상으로 둔다. |
| 빠르게·서서히 | 변화 속도 | 효과 발현·회복 등 무엇의 변화인지 확인한다. |

부정·가능성·비교·범위·조건도 포함한다. `발생하지 않음`, `발생할 수 있음`, `3일 이상`, `동일 부위인 경우` 등을 빠뜨리면 뜻이 달라진다. 생략된 수식 대상은 임의로 채우지 않고 미결로 남긴다.

### 5. 진행 단계와 확인 기준

단계는 다음 순서로 진행한다. 실제 데이터를 넣어 본 결과가 정의와 맞지 않으면 앞 단계의 정의·규칙·ERD를 수정한다.

| 단계 | 할 일 | 산출물과 확인 기준 |
|---|---|---|
| 1. 원장 전체 조사 | 원장21개 각각을 내부 값까지 최소 한 번 전수 조사한다. 이름·설명뿐 아니라 기전·적응증·안전·시간·관리·조합·순서·출처·메타데이터를 읽는다. | 원장별로 원문 위치 → 정보 종류 → 분해 후보 → 연결 대상·관계 → 수식·조건 → 미결을 기록한다. 모든 값이 조사 기록에 포함됐는지 확인한다. |
| 2. 공통 의미와 실버 ERD 설계 | 전체 조사 결과를 모아 같은 개념과 다른 개념, 개체·속성·관계·조건·단위·제약을 정의하고 저장 구조를 설계한다. | 공통 의미 모델과 실버 ERD. 실제 값의 행선지를 설명할 수 있어야 한다. 기존 ERD는 참고·대조 자료이며 유지해야 할 전제가 아니다. |
| 3. 실버 변환·검증 | 정의와 정규화 규칙으로 원장 전체를 실제 변환한다. | 실버 데이터·변환 규칙·원문 대응표·미결 목록. 누락·뜻의 변형·잘못된 대상 연결·조건 손실을 확인하고 모델과 ERD를 수정한다. |
| 4. 시맨틱 레이어 연결 | 공통 의미·관계·규칙을 실제 실버·골드 데이터 위치와 조회 경로에 연결한다. | 개념별 데이터 매핑·관계별 사용 규칙. 질문 처리와 서비스가 같은 정의를 사용할 수 있어야 한다. 공통 의미 정의 자체는 2단계부터 함께 만든다. |
| 5. 골드 구성·활용 | 실버를 질문 응답·조회·검색·추천 목적에 맞게 가공하고 시맨틱 정의에 연결한다. | 목적별 데이터와 조회 방식. 예상 질문으로 필요한 정보·조건·근거를 꺼낼 수 있는지 확인한다. |

골드와 연결해야 하는 시맨틱 매핑은 골드 구성과 함께 보완한다. 위 순서는 의미 정의를 마지막까지 미루거나 모든 단계를 되돌릴 수 없게 고정한다는 뜻이 아니다.

#### 조사와 검증에서 지킬 기준

- 조사 대상은 우선 원장에 이미 들어 있는 자료다. 외부 자료 추가 수집과 구분한다. 사실 확인이 필요한 부분은 별도 미결로 기록한다.
- 같은 문자열도 연결 대상·조건·문맥이 다르면 하나로 합치지 않는다.
- 임상 동의어·상하 관계·적용 범위를 문자열 유사성이나 형태소 분석만으로 확정하지 않는다.
- 형태소 분석은 후보를 찾는 도구다. 토큰·품사 목록을 전수 의미 조사 완료로 취급하지 않는다.
- 원문 조각과 포인터가 모두 보존됐다는 검증은 의미 해석의 정답을 보장하지 않는다.
- 담을 곳이 없는 말을 새 이름이나 불투명한 노드로 만들어 미해결을 닫지 않는다.
- 조사 기록의 잔여가 없더라도 정규화 완료로 세지 않는다. 식별 명칭의 역할·관계·조건 등이 미결일 수 있다.


### 이번 사용자 지시로 보완한 조사·미결·검증 계약

- 모든 원장을 각각 내부 값까지 최소 한 번 전수 조사한다. taxonomy의 모든 계층·항목·products·problem과 extracted의 기전·적응증·안전·시간·관리 문구까지 포함한다. 표본·필드 목록·값의 횟수·형태소 분석으로 대체하지 않는다.
- 값마다 원문과 정확한 위치, 정보 종류, 분리 대상, 무엇에 관한 정보인지, 연결 대상과 관계, 수식·조건·부정·가능성·범위, 원문만으로 확정 불가능한 부분을 기록한다.
- 흐름은 조사 → 검증 → 미연결·미결 탐색과 분류 → 필요한 사용자 선택을 아티팩트로 제시 → 선택 반영 → 재검증이다.
- 미결 1: 조사·해석·연결 오류는 에이전트가 먼저 해결한다.
- 미결 2: 원문 정보 부족은 부족한 정보와 제한되는 활용을 명시한다. 사용자에게 사실을 추측해 정하도록 묻지 않는다.
- 미결 3: 사용자 결정 필요는 원문·이유·추천·선택지·영향을 제시하고 확인받는다.
- 같은 원인의 항목은 묶고, 선택의 적용 범위와 예외를 기록해 재사용한다. 수천 개를 마지막에 넘기지 않는다. 선택 대기 중인 해석은 확정 데이터로 적용하지 않는다.
- 원문 보존만으로 미결을 닫지 않는다. 선택 대상 0건 표시는 잔여 항목의 처리 상태와 영향 검토가 뒷받침돼야 한다. 미결이 남은 원장은 완료라고 하지 않는다.
- 원장별 읽기용 Markdown과 필요한 구조화 기록을 만들고, 원문 대응과 의미 판단을 분리한다.
- 기계 검증: 원문 누락·중복·포인터·문자구간·해시. 의미 검토: 정보 종류·수식 대상·조건 범위·부정·관계 방향·인과·선후.
- 기계 검증 통과를 의미 해석 정답 또는 정규화 완료로 표현하지 않는다. 정규식·키워드·부분문자열 분류를 원문 전체의 의미 조사로 제시하지 않는다.
- 선택 화면은 작은 예제로 실제 표시·선택·응답 전달을 먼저 확인한다. 로컬 HTML 생성만으로 화면 제공을 주장하지 않는다. 승인 이력을 다시 묻거나 선택만으로 자동 반영됐다고 표시하지 않는다.
- 사용자가 질문하면 먼저 답한다. 중단 지시 시 본인과 서브에이전트 작업을 즉시 멈추고 실제 상태를 확인해 보고한다.

## 3. 발주 (살아 있는 것만)

이슈 그루핑 활성 발주 없음. 관련 작업은 폐기했다. 과거 retained/user_takeover 터미널의 프로세스까지 종료했다고 주장하지 않는다.

- 2026-11-10 기본 단위 재료·기전·조직(17계열) — task `task_840ce47b75a9` · dispatch `ctx_df323dbf97dd` · 워커 `term_dbf8189a-a5c4-48dd-b646-b41fe050e502` · 브리프 [atoms-material-mechanism-tissue-brief.md](./atoms-material-mechanism-tissue-brief.md) · 산출 `silver-model/drafts/atoms/`
- 2026-11-10 3층 시범(M1·M9·M8) — task `task_f92728163b6c` · dispatch `ctx_3ee5b6a912a5` · 워커 `term_e4be7950-c673-4bec-8d05-4512d660cdca` · 브리프 [procedure-3level-pilot-brief.md](./procedure-3level-pilot-brief.md) · 산출 `silver-model/archive/pilot-3level/`
- 2026-11-10 시술 세트 시범(M1·M8·M16) — task `task_b8d5c43f8b34` · dispatch `ctx_e7b00fe3ecee` · 워커 `term_5361efa1-bb77-49e6-ba92-1ac1537056f1` · 브리프 [procedure-set-pilot-brief.md](./procedure-set-pilot-brief.md) · 산출 `silver-model/archive/pilot-set/`
- 2026-11-10 modality 데이터 CSV — task `task_fe27646483c9` · dispatch `ctx_2653ebe0bac6` · 워커 `term_be929c0a-1d9c-4543-80cb-4e1436560387` · 브리프 [modality-data-brief.md](./modality-data-brief.md) · 산출 `silver-model/data/modality.csv`·`modality_alias.csv`·`modality-notes.md`
- 2026-11-10 계열 설계 — run `run_5e41335924e7` · task `task_d20b970b03fb` · dispatch `ctx_1a2225a724a7` · 워커 `term_81580fcd-3c6f-4bd9-95bc-0c9aa26601e6`(claude-opus-5-5) · 브리프 [family-design-brief.md](./family-design-brief.md) · 산출 `silver-model/family-design.md` · (필러 워커 ctx_22e5ecf5fab1 완료·release)
- 2026-11-10 시범2 필러×부작용 — run `run_5e41335924e7` · task `task_f061d73ef66b` · dispatch `ctx_22e5ecf5fab1` · 워커 `term_b56823ce-ef54-45be-ab4c-5f125301551f`(claude-opus-5-5) · 브리프 [pilot-filler-adverse-brief.md](./pilot-filler-adverse-brief.md) · 산출 `silver-model/pilot-filler-adverse.md`
- 2026-11-10 시범 보톡스×부작용 — run `run_5e41335924e7` · task `task_73fee96a8075` · dispatch `ctx_d5c25e523290` · 워커 `term_e0a80056-f3e9-4cac-bbe0-58ead8819c9b`(claude-opus-5-5) · 브리프 [pilot-botox-adverse-brief.md](./pilot-botox-adverse-brief.md) · 산출 `silver-model/pilot-botox-adverse.md` · 코디 handle `term_107c16b1-6066-4654-9272-359649efd67f`(11-10 변경)
- 2026-11-09 실버 테이블 목록 v0 — run `run_5e41335924e7` · task `task_a0c3ccbedd5c` · dispatch `ctx_8b2cc692336b` · 워커 `term_bd512976-dc29-4104-8a91-199a2a6658f8`(claude-opus-5-5, 코디 워크트리 탑승) · 브리프 [silver-model-v0-brief.md](./silver-model-v0-brief.md) · 산출 `silver-model/archive/tables-v0.md` · 코디 handle `term_107c16b1-6066-4654-9272-359649efd67f`

## 4. 산출물

- 2026-11-10 재료·기전·조직 확정본 발주 — 브리프 [atoms-finalize-brief.md](./atoms-finalize-brief.md) · 산출 `silver-model/silver/` (material·mechanism·tissue + method-candidates) · 이름 3칸(name_ko·name_en·abbr) · 괄호 제거 · wavelength_nm · 전달 방식·RF 극성·펄스·프락셔널 → 방법 후보

- 2026-11-11 제품 v5(사용자 조사 반영) 발주 — 브리프 [product-v5-user-research-brief.md](./product-v5-user-research-brief.md) · 산출 `silver-model/drafts/product-v5/` · v4 결과: product_organization 547 · 조직 189 · 회사 없는 제품 60
- 2026-11-11 제품-회사 역할 표 발주 — 브리프 [product-org-roles-brief.md](./product-org-roles-brief.md) · 산출 `silver-model/drafts/product-v4/`
- 2026-11-11 제품 v3 결과(drafts/product-v3/) — 빈칸 74 → 채움 11 · 이력만 3 · 못 채움 60(원장 작성자 확인 목록 notes §4) · 새 조직 12 · 겹침 34(원장=브랜드·판매사 vs 식약처=허가 제조원) → 제조사 정의 결정 필요(제품-회사 역할 표 제안) · 워커 `term_1c3c2cc3-dd50-4cbd-891c-3aa0dbeda256`
- 2026-11-11 제품 제조사 빈칸 식약처 반영 발주 — 브리프 [product-mfds-fill-brief.md](./product-mfds-fill-brief.md) · 산출 `silver-model/drafts/product-v3/` · 근거 = 10-28 식약처 조사 `phub-recommend/step1-products.json`(395) + 남은 9개 식약처 재조회 · manufacturer_source 「식약처」 추가 · KPIC 은 의약품 DB 라 이번엔 미사용
- **제품 v2 확정(11-11)** — `silver/` product 313 · organization 105 · product_material 388 · product_method 59 · product-research.csv(외부 조사 출처) · product-notes.md · name_check(확인 56 · 웹 미확인 42 · 웹·식약처 미확인 16 · 조사 대상 아님 199) · 시술 아님 3 → archive/not-procedure-products.csv · v1 은 archive/product-v1-silver
- 2026-11-11 제품 보완 결과(drafts/product-v2/) — 제조사 외부 조사 확인 52 채움(빈칸 74: 못 찾음 54 · 추정 20 미반영) · 새 조직 24(조직 107) · kind 필링제 2 · 줄기세포·엑소좀 제제 11 · 원장 오류 13건(notes §4.1) · 아큐탄(처방 경구약)·컨트라투벡스(일반의약품 겔) 시술 아님 · 사용자 판단 대기 · 워커 `term_8cfe6e00-2458-44be-909c-c41a862a8ac9`
- 2026-11-11 제품 보완 발주 — 브리프 [product-fill-brief.md](./product-fill-brief.md) · 산출 `silver-model/drafts/product-v2/` · 정규화 3(aliases 띄어쓰기 · kind 필링제/줄기세포·엑소좀 제제 · AAPE 재료) + 빈 제조사 116 · 빈 재료 6 웹 조사(출처·manufacturer_source) + 아큐탄·컨트라투벡스 조사(빼기는 사용자 판단)
- **제품 확정(11-11)** — `silver/` product 318 · organization 83(current_org_code·연혁) · product_material 390 · product_method 59 · product-notes.md(원장 오류 표: 올리지오·시크릿·아그네스·시너론 표기·벡터스·펠레베·에스테필, 출처 포함). 초안은 archive/product-draft
- 2026-11-11 제품 확정 발주 — dispatch `ctx_53855197080c` · 워커 `term_e22bb796-5900-4a41-9165-5cf045bbe09a` · 지시 [product-finalize-instructions.md](./product-finalize-instructions.md) (리젠바이오텍 합침 · 아그네스 절연 니들 · 브이빔 캔델라 → silver/)
- 2026-11-11 제품 4~7번 수정 — dispatch `ctx_71021eeefae2` · 워커 `term_1ef49bcf-cbca-454d-a6e4-66ac8227d333` · 지시 [product-orgs-fix-instructions.md](./product-orgs-fix-instructions.md)
- 2026-11-11 시크릿 수정 — dispatch `ctx_b5d107cda8a4` · 워커 `term_0c62088f-543d-4990-99b8-92edc4249ac5` · 지시 [product-secret-instructions.md](./product-secret-instructions.md)
- 2026-11-11 올리지오 수정 — dispatch `ctx_ad7d62815edf` · 워커 `term_7e70adf0-8375-49d3-b3e6-6f84fa36ee12` · 지시 [product-oligio-instructions.md](./product-oligio-instructions.md) (이전 제품 워커 터미널 쓰기 불가로 새로 띄움)
- 2026-11-11 제품 사전 결과(drafts/product/) — product 318(장비 157·약제 36·스킨부스터 36·필러 34·실 23·콜라겐 자극 20·기타 9·키트 3) · 제조사 85 · 제품-재료 390 · 제품-방법 59 · 확인 8사례 표현 · 판단 7건(추천 있음) 사용자 확인 대기 · 워커 `term_46a56daf-b69d-4836-85c6-c2f05d08542e` 유지
- 2026-11-10 제품 사전 발주 — 브리프 [atoms-product-brief.md](./atoms-product-brief.md) · 산출 `silver-model/drafts/product/`(product · organization · product_material · product_method)
- **방법 확정(11-10)** — `silver/method.csv` 43(투여 경로 7·주입 방식 10·도구 9·에너지 조사 11·흡수 촉진 5·재료 처리 1) · method-notes.md. method-candidates·atoms 초안은 archive 로
- 2026-11-10 방법 사전 발주 — 브리프 [atoms-method-brief.md](./atoms-method-brief.md) · 산출 `silver-model/drafts/method/` · 출발 method-candidates 13
- **재료·기전·조직 확정(11-10)** — `silver-model/silver/` material 135 · material_spec 27(파장 21·농도 5·온도 1) · mechanism 43 · tissue 24 · atoms-notes.md. 방법 후보 13행은 `drafts/method-candidates.csv`(방법 사전 출발점)

**폴더 규칙(11-10 · 11-11 보완)**: `silver-model/silver/` = 확정 CSV 데이터만 · `notes/` = 판단·조사 기록(*-notes.md, product-research.csv — 실버 아님) · `drafts/` = 작업 중(atoms 재료·기전·조직 초안, modality_alias 보류) · `archive/` = 지난 시도(material-tissue-v1 실패작, pilot-set, pilot-3level, tables-v0, family-design, 부작용 시범 2). 워커는 drafts 에 쓰고, 사용자 확인 후 silver 로 옮긴다.

- [기본 단위 재료·기전·조직](./silver-model/drafts/atoms/) — material 137(물질 88·에너지 40·기계 9, parent 계층) · mechanism 54 · tissue 24(층 11·구조 7·표적 6) · 대표 5사례 표현됨 · taxonomy 523 중 쌍 연결 421·못 찾음 65·제외 24·조합 15 · 11-10 검토: 기전에 전달 방식(진피 주입·경피 흡수 등) 섞임 → 방법 단위로? · 사용자 판단 2

- **구조 논의 문서(정본 논의 자리)**: [Procedure Hub 실버 데이터 구조](https://claude.ai/artifact/6GbVpucRZmnPdQq6TsJMKq) — 목표(고민·이름·상품 → 시술) · 3층(기본 단위 → 조합 → 관계) · 기본 단위 11 · 만드는 규칙 · 열린 질문 5 · 다음 순서. 11-10 작성, 여기서 사용자와 논의

- [3층 시범](./silver-model/archive/pilot-3level/) — 항목 479 판정 · 시술 종류 11(보톡스 1 · 레이저 6+IPL 1+근적외선 1 · HIFU · RF · 마이크로웨이브) · 케이스 96 · material 20 · tissue 12 · 11-10 검토: 케이스가 제품·가격표 조합으로 늘어남(제품을 케이스 축에서 뺄지) · 같은 케이스 중복(전체얼굴) · notes §5 7건

- [시술 세트 시범](./silver-model/archive/pilot-set/) — 항목 437 판정(제품 117·분류 칸 87·케이스 79·시술 62·메뉴 47·재분류 44) · 시술 53(M1 3·M8 29·M16 21) · material 41 · tissue 11 · 11-10 검토: 재료 세밀도 문제(파장·개별 성분 = 재료 → M8·M16 시술 폭증) 사용자 판단 대기 · notes §5 7건

- [material·tissue 데이터 v1(실패작)](./silver-model/archive/material-tissue-v1/) — material.csv 120행(물질 89·에너지 28·기계 3) · tissue.csv 38행(층 14·전신 1·구조 14·표적 물질 7·미생물 2) · notes §4 판단 10건(추천 있음) · 11-10 사용자 확인 대기. 짚을 것: 바르는·먹는 약 성분 다수(시술인지 시술 단계에서 판정)

- [modality 데이터](./silver-model/silver/) — modality.csv 17행(code·이름·공통 수준 overview/mechanism·근거) · modality_alias.csv 103행(원장 표기 매핑, 보류) · modality-notes.md · **확정(11-10)** · M8 기전 공통 수준 수정 완료(열 → 선택적 파괴·분해) · 남은 것: M3 콜라겐/hADM 소속 재검토(시술 설계 때)

- [계열 설계](./silver-model/archive/family-design.md) — 연결 관계 제외 · family(17)·family_profile(계열×TX/EX 34)·family_name · 16 시술 / M15 묶음 · 판단 대기: TX↔EX 설명 정본(9계열 차이)

- [시범2 필러×부작용](./silver-model/archive/pilot-filler-adverse.md) — 값 2231 대조(차집합 0) · 부작용 값 584 · 개념 71(공유 21) · 틀 통함 + 추가(기전 사건·의심 사건·대응 시한·분모 종류·측정 판·정점·병행 순서·상속) · 테이블 16→13 · 판정3 F1~F8(F2~F4 는 시술 간 간격) · 보톡스 소급 5건

- [시범 보톡스×부작용](./silver-model/archive/pilot-botox-adverse.md) — 값 1807 대조(차집합 0) · 부작용 값 502 · 개념 68 · 케이스 K0~K19 · 판정3 8건(D1~D8) · 테이블 초안 16 · 담을 칸 없는 값 0 · 11-10 코디 검토 후 사용자 판단 대기

- [실버 테이블 목록 v0](./silver-model/archive/tables-v0.md) — 68 테이블(개체19·관계34·상하위7·근거8) · 워커 완료 11-09 · 코디 검토 후 사용자 확인 대기(§5 판단 3 + 코디 지적 2: 회피 테이블 없음 · 「원장 근거 없는 상하위 안 만듦」은 브리프 오류)





- [batch-04 최종 메모](./batch-04-final-note.md) — span44/44·양립가능 비고3건·생성부/검증 정합. 코디 verify5/5 EXIT0 추가 확인은 발주 기록에 있음.

- [batch-04 독립검토](./batch-04-review.md) — 기계 전수 대응, 의미 재독은 공개된 표본. PASS3/WARN2·차단0.

- [batch-04 발주 기록](./batch-04-dispatches.json) · 결과 위치 `first-pass/<원장명>/`

- [batch-03 최종 메모](./batch-03-final-note.md) · [taxonomy 검토](./batch-03-review-taxonomy.md) · [나머지4개 검토](./batch-03-review-others.md) · [발주 기록](./batch-03-dispatches.json)

- [batch-02 묶음 검토](./batch-02-review.md)
- [batch-02 발주·후속 기록](./batch-02-dispatches.json)

- [batch-01 묶음 검토](./batch-01-review.md)
- [batch-01 기록 보완](./batch-01-final-note.md)

- [스킬 수정 보고](./skill-update-report.md)
- [batch-01 발주 기록](./batch-01-dispatches.json)
- [batch-01 묶음 검토](./batch-01-review.md) · [batch-01 최종 메모](./batch-01-final-note.md)(기록·분류 보완 반영·검증·남은 한계)
- batch-01 1차 조사 — [first-pass/](./first-pass/) products · procedure-comparison · complications · treatment-sequence · synergy

- [_RESUME.md](./_RESUME.md)
- [1차 조사 스킬](./ledger-first-pass/SKILL.md)
- procedure-profiles 1차 조사 — [first-pass/procedure-profiles/](./first-pass/procedure-profiles/): review.md · source-map.json · morphology.json · expressions.json · issues.md · validation.md (+ 재현 build.py·verify.py·manual-expressions.json·segmentation-review-rules.json·segmentation-occurrence-review.json·expression-review.json·validation-machine.json·build-output.txt)
- [procedure-profiles 보정 리포트](./procedure-profiles-correction-report.md) (F1~F7 처리·검증·남은 문제)
- [procedure-profiles 최종 메모](./procedure-profiles-final-note.md) (재검토 W1(b)·W2 처리·검증)

### procedure-profiles 단계별 상태 (2026-11-09 재검토 WARN 후 W1·W2 기록, 코디 확인 전)

| 단계 | 상태 |
|---|---|
| 전수 읽기 | 17/17 항목 + 상위 4키, 작성자 3회 통독. 보정 전 독립 검토 1회, 보정 후 독립 재검토 1회(WARN 경미) |
| 구조·값 수집 | 노드 583/583 · 키 412 · 중복 키 0 |
| 형태소·표현 수집 | Kiwi 0.24.1(cong) 197값 2,341토큰 · 제외 95 · 오태깅 **표시됨(교정 아님)** 70건 · 출현 판정 89건(MAG·MM·NR·NP·MAJ + 의미위험 서명 16종) · 범위 밖 알려진 오분절 2출현 기록(발적·수화, 미표시, issues A1-W1). 원시 형태소 출력의 범위 밖 정확성은 보장하지 않음 · 표현 후보 1,505(오탐 24 = regex 15 + 오태깅 유래 9, 부분일치 3) |
| 기계 검증 | 해시 불변·양방향 대조·Pointer·구간·적용/제외·출현 판정↔표시·오태깅 유래 표시 대응·재현성 통과, 변이 시험 2종 검출 |
| 읽기 검토 | 보정 반영. 행위·대상 구절 분해는 후속 F-1 |
| 1차 수집 범위 | 재검토의 조건부 종료 요건(W1 기록)을 기록으로 충족 — **코디 확인 전** |
| 열린 미결 | B 원문 정보 부족 10묶음 · 잠정 2 · C 0(전 C1·C2 보류, 사용자 결정 아님) · 후속 9 |
| 후속 의미 조사 | 시작 안 함 |


## 5. 이력 (최신이 위)

- 2026-11-09 사용자 삭제 지시 실행: `issue-grouping-brief.md · issue-grouping-dispatch.json · issue-grouping-fix-brief.md · issue-grouping-rereview-brief.md · issue-grouping-rereview.md · issue-grouping-review-brief.md · issue-grouping-review.md · issue-grouping-w4-w7-brief.md` 삭제. 이슈 그루핑 관련 상세 발주 이력도 이 재개 노트에서 제거하고 이 폐기 기록으로 대체했다. 원본·first-pass는 삭제 전후 전체 파일 해시 비교로 불변 확인. 실패 원인: 공통 어휘·의미 분류라는 목적에서 벗어나 관찰·후속 과제·도구 오류를 대량 미결로 혼합하고, 항목별 내용 파악 대신 자동 분류·관리 문서 보완을 반복했다. 해당 결과·잔여 작업 수·완료 주장은 다음 작업의 근거로 사용하지 않는다. 기존 조사 결과의 의미 판단도 완벽하다고 간주하지 않으며, 실제 원문 문맥으로 판단한다.

- 2026-11-09 batch-04 R1/R2 보완 실물확인·코디 verify5개 재실행 EXIT0/실패0·원본해시 baseline 일치. checklist span44건과 optimization 양립가능 비고3건 및 생성원천 반영 확인. 마지막5개1차 범위 종료, 누적21/21. 원장전체/의미조사/정규화 완료 아님. 비교단계는 미발주, 알려진 표현누락/다국어한계/분류권고는 다음조사 입력으로 유지. 보완워커 release 실제receipt 저장.

- 2026-11-09 batch-04 독립검토 PASS3/WARN2 수신(기계 전수·의미 표본 구분, 차단0·선택0). checklist44 known_errors span 부재는 각값내 유일함을 확인했고 보완발주. optimization I-10-1/2/4는 금지하한·권장간격/포함관계라 양립가능 비고 추가 발주. 기존ID/집계 유지·생성부 정합·5개검증/해시대조를 계약으로 Opus1명 발주. 리뷰워커 release closed_agent_terminal 확인.

- 2026-11-09 treatment-optimization 14/14구획 보고 수신, 코디 verify140/140·원본해시 baseline 일치 확인. batch-04 보고5/5 후 Opus 독립검토1명 발주. 단순 수치차와 실제 모순 구분·수식/조건 구절 수집범위·기계/표본/전수 검토범위·운영위반 비고 분리를 계약에 명시. 조사5명 release closed_agent_terminal 확인.

- 2026-11-09 patient-education 보고 수신(18/18구획), 코디 verify34,232검사 실패0·원본해시 baseline 일치. B36/P42/F10/I1/K25출현/C0 열림. batch-04 보고4/5·독립검토 전. release 실제 반환 receipt 저장.

- 2026-11-09 pre-procedure-checklist·post-procedure-timeline 보고 수신. 코디 verify14,697/27,804검사 모두 실패0·원본해시 baseline 일치. 보고3/5·독립검토 전. timeline의 허용경로밖 scratch_dummy 생성/삭제 보고를 운영 위반으로 기록(현재 존재 여부는 발주JSON, 과거 내용·소유권은 별도 증명하지 않음). 두 워커 release 실제 receipt 저장.

- 2026-11-09 market-pricing 보고 수신(18구획 직접읽기), 코디 verify11,930검사 실패0·원본해시 baseline 일치 확인. B30/I4/P12/F7/K4/C0 열림, 독립검토 전. batch-04 보고1/5. release 실제 반환은 batch-04-dispatches.json에 기록.

- 2026-11-09 사용자 승인으로 batch-04 마지막5개(market-pricing·patient-education·post-procedure-timeline·pre-procedure-checklist·treatment-optimization)를 Opus5명에게 발주. 5/5 ready/input_accepted·effective opus 확인. 결과 기존폴더 없음 확인 후 브리프/해시 baseline 저장. 이전배치의 후보 공백·다국어 과장·전역프로세스종료 재발 방지를 계약에 명시. 전체21개 파악 후 원장간 비교 및 실제 설계선택 묶음 제시 순서 합의.

- 2026-11-09 batch-03 기록 보완6개Markdown·최종 메모 실물 확인, 코디 verify5개 재실행 EXIT0/실패0·원본5개 해시 baseline 일치. batch-03 5개1차 범위 종료, 누적16/21. taxonomy 후보 공백·literature zh/ja 표현 미수집/한국어조건7건은 열린 한계이며 JSON에는 미반영. rebuild 시 보완문구 소실 주의. 마지막5개 미발주. 원장 전체 완료 아님.

- 2026-11-09 others 독립검토 PASS3/WARN1·차단0 수신. literature zh/ja 실제 수집범위 정정·한국어 조건7구절 기록 권고를 taxonomy 후보 공백 기록과 묶어 Opus writer1명에 발주했다. 원문/추출JSON 불변·Markdown6파일 이내 최소 보완 및 최종 메모만 허용. 선택적 분류 권고는 실제 분류 변경 없이 후속 유지. 검토2명 release의 closed_agent_terminal 확인.

- 2026-11-09 taxonomy 독립검토 WARN·추출 차단0 수신. 기계 독립 전수 대조 실패0, 원문 재독은 약380노드(2%) 표본. 자제·깊이·얇·서서히/점진·권장/주의/필요·단위 등의 표현 후보 미덮임과 validation의 전수 보존 주장 정정을 기록 보완 대상으로 유지한다. 아직 실제 조사 문서에 보완 적용하지 않았다. 검토 워커 release는 released/closed_agent_terminal 확인.

- 2026-11-09 taxonomy53/53 구획 보고 수신, 코디 verify오류0·17,593노드/11,931말단·빈컨테이너 대응 확인. batch-03 5/5 보고 후 독립검토를 taxonomy와 나머지4개로 나눠 Opus2명 발주했다. 이전 삭제된 taxonomy103구획 계획과 혼동하지 않도록 명시했다.

- 2026-11-09 literature-evidence 새시도 보고 수신。 코디 verify오류0·원본 해시불변·18구획/이스케이프9문자열 대응 확인. 언어별 내용은 수집했으나 형태소는 한국어만, en/zh/ja/서지 제외를 한계로 기록했다. batch-03 보고4/5, taxonomy 보고 전. 독립 묶음 검토 전.

- 2026-11-09 problem-packages 새시도 보고 수신. 코디 verify91,851검사 오류0·원본 해시불변·15구획/2366말단/빈배열48 대응 확인. batch-03 보고3/5, taxonomy·literature-evidence 보고 전. 독립 묶음 검토 전.

- 2026-11-09 problem-combos 새시도 보고 수신. 코디 verify132검사 오류0·원본 해시 불변·9구획370말단 대응 확인. batch-03 보고2/5, 독립 묶음 검토 전.

- 2026-11-09 pih-risk 보고 수신, 코디 verify오류0·원본 해시불변·9구획288말단 대응 확인. batch-03 보고1/5, 독립검토 전. 워커가 pkill -f cat -u 사용자 실행을 보고해 운영 사고로 기록했다. 다른4개 agent live는 확인했으나 다른cat/파일 영향은 미확인이다. 각4명에게 전역패턴종료 금지·정확PID만 제어·부분출력점검을 전달했다. pih release는 retained/user_takeover/processAction none.

- 2026-11-09 재연결 코디 Run generation2 바인딩 후, 종료된 네 원 태스크 상태를 failed로 정합화하고 --retry-of로 새Opus4명 발주. 모두 ready/input_accepted/effective opus 확인. pih-risk는 원dispatch 그대로이며 관련 프로세스·파일에 변경 명령을 실행하지 않았다.

- 2026-11-09 사용자 승인: pih-risk 제외, 다른4개 기존 출력 삭제 후 원본부터 새로 조사. 네 기존 dispatch failed/exited를 확인한 뒤 first-pass/taxonomy·literature-evidence·problem-packages·problem-combos 폴더만 삭제했다. pih-risk와 원본·기존11개 결과는 유지했다.

- 2026-11-09 사용자 시스템 다운 보고. 원본5개 해시 일치·중간 파일 존재 확인. taxonomy manual S000~S008 9개, literature manual17개, packages manual15개, combos 관찰파일2개, pih 중간산출물 보존. progress 일부는 실제 manual보다 오래돼 재개 시 대조 필요. 새 실행·stop·삭제·덮어쓰기 없음.

- 2026-11-09 batch-03 taxonomy·literature-evidence·problem-packages·problem-combos·pih-risk 발주5/5 state=ready·input_accepted·effective model=opus 확인. taxonomy 모든 계층/products/problem 및 큰 원장 구획분할·진행기록·전체누락검증을 브리프에 명시했다.

- 2026-11-09 batch-02 독립 검토 확인(PASS3/WARN2·추출/coverage 차단 오류0), 5개1차 범위 종료로 판정해 누적11/21. 독립 원문 읽기는 combo·contra 전수, anatomy·consent·extracted 표본이었다. WARN 권고는 보고서/발주기록에 남기고 재조사·임의 분류 변경은 하지 않았다. 현재 사용자 선택 대기0, 원장 전체 미완료. 검토 워커 release 반환 retained/user_takeover/processAction none 확인(프로세스 종료 주장 안 함).

- 2026-11-09 extracted 보고 수신·코디 verify182검사 실패0·18개 구획과17개 분할문서 대응 확인. batch-02 5/5 수신 후 Opus 독립 검토 ctx_68a17c6bda51 발주. 구획 소유 합집합·공유문맥·분할문서 접근성도 검토하도록 했다.

- 2026-11-09 anatomy-danger-zones 보고 수신, 코디 verify34,135검사 오류0·원본 해시 불변·12개 구획/분할 문서 대응 확인. batch-02 보고4/5, extracted 보고 전. 묶음 검토 전.

- 2026-11-09 batch-02 combo-recipes·consent-checklist 보고 수신, 코디 verify2개 재실행 오류0·원본 해시 불변·구획 coverage 확인. 보고3/5, 나머지 anatomy-danger-zones·extracted 보고 전. 독립 묶음 검토 전.

- 2026-11-09 batch-02 contraindications 보고 수신(1/5). 코디 verify77검사 통과·원본 해시 불변·coverage192말단의 소유 누락/중복0을 확인했다. 묶음 검토 전이며 다른4개 완료 보고는 아직 없다.

- 2026-11-09 batch-02 5개 모두 state=ready·input_accepted·effective model=opus 확인. 구획별 읽기 상태·전체 경로 집합 대응 및 분할 Markdown을 브리프에 명시했다. 결과는 first-pass/<원장명>/, actual receipt는 batch-02-dispatches.json.

- 2026-11-09 기록·분류 보완 실물 확인 및 코디 verify 5/5 재실행 exit0·원본 해시 불변 확인. batch-01 5개 1차 범위 종료로 판정, 샘플 포함 6/21. 원문 부족·잠정·후속·알려진 오류는 열린 채 유지. 현재 사용자 선택 대기0(원본 수정 승인 아님). 다음 묶음 미발주.

- 2026-11-09 writer 가 batch-01 기록·분류 보완 반영: products B5·B6 병기, procedure-comparison 상태 줄 맨 위, complications 카테고리 id·name Pointer 행(build.py 생성부)·A 보충(미표시 오분절 2·「삽입 깊이」·같은 구간 57쌍), treatment-sequence B1 병기·C1/C3/C5/C6 후속 과제화, synergy U1→F1·U2→실버 변환 규칙 재분류·「전층」 한계. 5개 verify 오류 0, 원본 24파일·JSON 불변, scratchpad 재빌드 바이트 동일. 코디 확인 전.
- 2026-11-09 묶음 검토 결과 5개 모두 1차 종료 가능(PASS3/WARN2), 종료 차단 추출 오류0. 기록·분류 보완만 Opus writer에 발주했다. 원본·JSON은 유지, 재조사·최종 의미 판정은 하지 않는다.

- 2026-11-09 complications 보고 수신·코디 verify.py 오류 0. batch-01 5/5 보고 수신 후 Opus 독립 묶음 검토 `ctx_15e5d7fecd82` 시작. 의미 과제·알려진 분석 한계를 반복 수정의 게이트로 만들지 않고 실제 수집 계약을 검토하도록 지시했다.

- 2026-11-09 synergy worker_done 수신. 코디 verify.py 재실행 오류 0·원본 해시 불변. 보고 수신 4/5. U1·U2는 원본 변경 제안으로, 사용자 원본 보존 지시에 따라 지금 선택을 요청하지 않는다. 관찰 자체는 후속 의미/변환 검토로 유지하며 묶음 검토에서 분류 표기 정리가 필요하다.

- 2026-11-09 treatment-sequence worker_done 수신。 코디 verify.py 재실행 32검사 통과. 묶음 검토 전. 보고 수신 3/5, 미수신 2/5. 해당 결과의 C는 사용자 결정이 아닌 원문 내 불일치이며 사용자 선택은 0건이다.

- 2026-11-09 procedure-comparison worker_done 수신. 코디 verify.py 재실행 오류 0·원본 해시 불변. 묶음 검토 전. batch-01 완료 보고 수신 2/5, 미수신 3/5.

- 2026-11-09 products worker_done 수신. 코디 verify.py 재실행 failure_count=0·원본 해시 불변. 1차 수집 종료 보고 수령, 묶음 읽기 검토 전. 나머지 원장 완료 보고 미수령. 상세 상태는 batch-01-dispatches.json.

- 2026-11-09 batch-01 원장 5개(products·procedure-comparison·complications·treatment-sequence·synergy) 발주 완료. 5개 receipt 모두 state=ready, input_accepted, effective model=opus를 확인했다. 실제 IDs·원본 해시·스킬 해시·receipt는 batch-01-dispatches.json에 저장했다.

- 2026-11-09 Opus 스킬 편집 워커 결과를 확인하고 quick_validate를 재실행해 통과했다. 첫 병렬 묶음 5개 원장 브리프를 준비했다. 편집 워커 release 반환은 retained/user_takeover/processAction none이므로 종료 프로세스를 주장하지 않는다.

- 2026-11-09 최종 보완 worker_done 수신. 코디가 W1(b)·W2 기록을 확인하고 verify.py를 재실행해 오류 0·원본 해시 불변을 확인했다. 1차 수집 범위 종료, 원장 전체 미완료로 판정했다. 다음 원장은 시작하지 않았다.

- 2026-11-09 researcher 워커가 재검토(WARN 경미) W1·W2 를 기록으로 보완했다. 발적 `/profiles/13/aftercare/0` [6,8)과 수화 `/profiles/2/practicalNotes/2` [66,68)을 범위 밖 알려진 오분절로 issues A1-W1 에 적었고(JSON 재생성 없음), 미판정 근거 토큰 46건의 correct 간주 구현과 재검토자 대조 결과를 구분해 기록했다. verify failure 0, 원본 해시 불변. 1차 수집 범위의 조건부 종료 요건을 기록으로 충족했으나 코디 확인 전이다. 원장 전체는 미완료다.

- 2026-11-09 F1~F7 보정 보고 수신. 코디 verify.py 재실행 failure_count=0. B 열린 10·현재 사용자 선택 0이라는 재분류 및 보정 내용을 독립 재검토 `ctx_880d1fe87c20`로 발주했다. 최종 판정 전이다.

- 2026-11-09 researcher 워커가 F1~F7 보정을 완료했다. 출현 재훑기로 미표시 4건(열/NR 3·수화/NNP 1)을 추가했고, 오태깅 유래 후보 9건을 출현별로 표시했다. B 를 재분류해 열린 묶음은 10이 됐고, C 는 0(보류 2)이다. 원본 해시 불변, build·verify 통과. 보정 후 독립 재검토는 아직 없다. 커밋·PR 없음.

- 2026-11-09 독립 검토 WARN 수신(F1~F7). 원문 대응 PASS와 구분하고 원 작성 워커에 보정 `ctx_482ce6e7cf27` 발주. 사용자 선택 제안은 재분류 중이며 승인 처리하지 않았다. B10 잔여 1건과 집계 불일치도 확인하도록 지시했다.

- 2026-11-09 조사 worker_done 수신. 코디 verify.py 재실행 failure_count=0. 원장 전체 완료로 승인하지 않고 독립 검토 워커 `ctx_cc054348815f`를 발주했다. 사용자 선택 2건은 검토 전 제안 상태다.

- 2026-11-09 researcher 워커가 procedure-profiles.json 1차 조사를 수행했다. 원본 해시 `a1fe389d…3f3e` 불변, 기계 검증 통과, 미결 B 13묶음·C 2건 기록. 원장 완료·정규화 완료가 아니다. 다른 원장은 열지 않았다.

- 2026-11-09 researcher 워커 발주: `task_3c622fd2e4c0` / `ctx_75bc57e3b6d3`. Orca input_accepted·turn_started 확인. 원본·기존 작업 폴더는 유지했다.

- 2026-11-09 사용자 지시로 실제 작업을 워커 전담으로 변경하고 첫 원장 전체 조사 브리프를 작성했다. new-work.sh는 기존 phub-recommend 감지로 변경 전 중단됐으며 기존 작업은 정리하지 않았다.

- 2026-11-09 사용자 요청으로 1차 조사 스킬을 작성하고 재개 노트에 연결했다. 원문 대응과 공통 개념 연결을 구분하고 전체 텍스트 형태소 분석·복합 표현 수집을 포함했다. 조사 실행은 시작하지 않았다.

- 2026-11-09 사용자 요청으로 목표 참고 문서 §1~5와 이번 대화의 제약·실제 진행 상태를 반영한 재개 노트를 작성했다. 참고 원본의 §6 과거 삭제·완료 기록은 계승하지 않았다.
- 2026-11-09 사용자 요청으로 `orchestration/work/phub-ledger-redesign/` 빈 디렉토리를 생성했다.
- 2026-11-09 AGENTS.md·관련 규칙·원장 README·목표 참고 문서를 읽고 전략을 제안했다. 원장 JSON 내부 조사는 시작하지 않았다.

- 2026-11-11 발주: 부위 사전 `atoms-site-brief.md` → 워커 term_08e928f1 (Opus 5.5). 산출 `silver-model/drafts/site/`. kind 부위 / 해부 구조(tissue_code + parent 부위) — 사용자 「응 발주혀」.
- 2026-11-12 발주: 실버 CSV `;` 여러 값 전부 풀기 `silver-split-brief.md` → ctx_969a3f6aa81e (Opus 5.5). 산출 `silver-model/drafts/silver-split/`. 공통 alias · source_ref 표 · product_modality · site_location(해부 구조 → 부위) · material_spec 값 분리 · 관계 표 id. 사용자 「까먹으면 어떡해 — 지금 다 푼다」. 부위 결정 2~5(턱 · 동의어 · 영문 지점 · 비근근)는 이 작업 뒤에 논의.
- 2026-11-12 silver 교체: `;` 다 푼 판(drafts/silver-split, 검증 PASS)을 silver/ 로 — 16표(사전 8 + 관계 5 + alias · source_ref + site_location). 이전 판 archive/silver-before-split/. method.from_code 칸 삭제(이력 11행 → notes/method-notes.md). **site · site_location 은 아직 미확정** — 부위 결정 2~5 대기(2번 「턱」 Chin/jaw 논의 중). 사용자 「그거는 옮겨야지」.
- 2026-11-12 부위 결정(사용자): ② 턱 = 큰 개념(jaw 보충) · 위험 구역 Chin → 턱끝 ③ 같은 자리는 한 행 — 일반 용어 이름 + alias kind 「의학 용어」 · 뉘앙스 차이는 고민·부작용에서 ④ Pitanguy line · Rhinion 영문 그대로 ⑤ 코 구역 비근근(Nasalis) → 비근(영어 기준 정정 · 원장 표기 별칭 · 확인 목록) · 해부 구조는 anatomy 표로 분리(tissue = 종류 · anatomy = 이름 붙은 개체 · site = 자리, 뼈는 시술 대상 아님). silver 직접 수정 발주 `site-finalize-brief.md`.
- 2026-11-12 부위 확정(silver: site 89 · anatomy 106 · anatomy_site 89, 검증 PASS) · 마무리 6건 추천대로(측두선←상측두융합선 · 다리←하지 · 체부→체간 · 안검/두부/하안면부 의학 용어 · anatomy 사전 행에 이름 칸 근거 · 관자궁 확인 목록) 발주 `site-finalize-2-instructions.md`. 다음 = 고민 사전(부위 노트 「고민 후보」 출발).
- 2026-11-12 부위 마무리 6건 완료(site 88 · anatomy 105 · anatomy_site 89, 검증 PASS · 이름 칸 없는 anatomy 24행은 근거가 anatomy_site 에만). 발주: 고민 사전 `atoms-concern-brief.md` → drafts/concern/ (concern · concern_site · alias · source_ref, 고민 아님 목록). 사용자 「고민 진행해」.
- 2026-11-12 고민 초안(271행 · 검증 PASS) · 결정 10건 추천대로(제모 → 「원치 않는 체모」 행 · 피부 타입은 사람 조건 · 같은 말 묶음 합침 · 나머지 지금대로) → silver 합치기 발주 `concern-finalize-instructions.md`. 사용자 「그렇게 하자」.
- 2026-11-12 고민 확정 → silver: concern 252 · concern_site 95(+ alias · source_ref 공통 표에 덧붙임), 검증 PASS. 같은 말 20행 합침(간반→기미 의학 용어 · 장미증→주사 등) · 「원치 않는 체모」 kind 체모 · 피부 타입 → 사람 조건 후보 · 흑자/검은 점/잡티 확인 목록. 다음 = 효과 사전.
- 2026-11-12 고민 v2 결정(사용자): 대·중·소 3단(대분류 = kind 16종을 행으로 · 모든 고민은 대분류 아래 · 중분류는 원장 subcategory) · 이름 명사형(「대상 + 상태 명사」, 원장 형용사형은 별칭 — 「이름 = 원장 표현」 규칙의 표기 정리 예외) · 자세한 것은 description(원장 근거만). 발주 `concern-v2-instructions.md`. 효과 사전 방식(a 따로+고민 연결 / b 관계만)은 그 뒤 논의.
- 2026-11-12 고민 v2 확정(silver: concern 260 = 대 17 · 중 36 · 소 207 · concern_site 95, 검증 PASS · 설명은 원장 인용 703 검증). 사용자: 자식 없는 중분류 = 그 자체가 끝 단계(복제 행 안 만듦) · 부위 별칭 든 이름 그대로(매핑은 코드로 연결 확인) · 이중턱 윤곽(처짐 연결은 관계 단계) · 혈관 병변 아래를 대분류 바로 아래로. 다음 = 효과 사전 방식 결정(a 따로 + 효과→고민 / b 관계만).
- 2026-11-12 효과 사전 방식(사용자): 효과 사전 따로 + 효과 → 고민(말뜻 연결)만. 케이스→효과 · 시점/지속 · 기전→효과 · 문헌 근거는 관계 단계(원문 위치만 notes). 고민과 같은 3단 · 명사형 · 자세한 설명. 발주 `atoms-effect-brief.md` → drafts/effect/.
- 2026-11-12 효과 결정(사용자): 효과는 시술 · 케이스 쪽에서 본다 — 이번엔 효과 사전 정규화만. effect_concern 은 silver 에 안 올리고 notes/effect-concern-reference.csv(54 짝 + 말뜻 후보)로 케이스 단계 참고. 「모든 고민이 닿는가」 확인은 케이스 단계로. §6 판단 추천대로 · 피부질환 등 빠진 효과 원장에서 다시 찾기. 발주 `effect-finalize-instructions.md`.
- 2026-11-12 효과 확정 → silver/effect.csv 70(대 21 · 중 39 · 소 10, 검증 PASS). 원장에서 다시 찾아 8행 추가(점 제거 · 혈관종 치료 · 다모증 치료 · 건선/백반증/아토피/피부암 전구 병변 치료 · 모공 막힘 해소). 사마귀 · 쥐젖 · 비듬 · 주사 등은 원장에 효과 표현 없음(notes). effect_concern 은 notes/effect-concern-reference.csv(원장 짝 63 · 말뜻 후보 11). 다음 = 부작용 개념 사전.
- 2026-11-12 발주: 부작용 개념 사전 `atoms-adverse-brief.md` → drafts/adverse/. 개념만(빈도 · 등급 · 시점 · 기간 · 위험 요인 · 대처 · 생기는 자리는 관계 단계) · 붙은 이름은 원자 개념으로 쪼갬(수식어는 관계 단계 목록) · 고민과 같은 말도 별개 행 · 3단 · 명사형 · 원장 인용 설명. 사용자 「그렇게 발주해줘」.
- 2026-11-12 부작용 초안 182행(대 15, 검증 PASS) · 결정 12건 추천대로 + 「미소 비대칭」 행 신설(원장이 분리 명시) → silver 합치기 발주 `adverse-finalize-instructions.md`. 결과류(효과 미흡 · 항체 내성 · ~악화)는 원장대로 부작용 행 · 고민과의 연결은 관계 단계. 다음 = 사람 조건 사전.
- 2026-11-12 부작용 확정 → silver/adverse.csv 183(대 15 · 중 141 · 소 27, 검증 PASS) · 미소 비대칭 ADV-183(근거 15 옮김). 다음 = 사람 조건 사전.
- 2026-11-12 발주: 사람 조건 사전 `atoms-condition-brief.md` → drafts/condition/. 개념만(금기/주의 · 위험도 · 중단 기간은 관계) · 약 · 성분은 material_code · 시술 간 간격 rules 는 시술 간 관계(넣지 않음) · 시술 이력은 판단 목록 · 3단 · 명사형 · 원장 인용 설명. 사용자 「발주해」.
- 2026-11-12 사람 조건 초안 152행(대 15, 검증 PASS) · 사용자 「정규화 중복 없게 추천으로」: 같은 뜻 한 행 · 포함은 부모 · 범위 겹침은 설명 · 측정값 이름은 상태 이름 · 152행 전수 점검 + 결정 12건(아큐탄 → 이소트레티노인 복용 별칭만 추가) → silver 합치기 발주 `condition-finalize-instructions.md`. 이게 끝나면 ① 사전 층 완료.
- 2026-11-12 **① 사전 층 완료.** 사람 조건 확정 → silver/condition.csv 151(대 15 · 중 80 · 소 56, 검증 PASS) · 피부염 → 피부 염증 합침 · 부모 4(개방성 상처 · 인공 태닝 · 마취제/히알루로니다아제 알레르기) · 범위 겹침 15쌍은 설명에 · 아큐탄 별칭. silver 22표. 다음 = ② 시술 · 케이스 조합 설계 논의(발주 전 사용자 합의).
- 2026-11-14 ② 조합 설계(사용자 「응!」): 표 = procedure(계열 · 재료 종류 · 주된 원리) · procedure_case(시술 + tissue/anatomy · site 하나 · 세부 재료, 이름은 원장이 붙인 것만) · case_method · case_product + 공통 alias/source_ref. 원장이 말한 조합만 · 부위만 달라도 별개 케이스 · 제품은 케이스를 가르지 않음(연결만) · 가격표로 케이스 안 만듦 · 약물은 성분이 다르면 다른 시술 · 사전 밖 값은 dict-candidates 로. 시범 M1 · M8 · M16 → 검수 뒤 14계열.
- 2026-11-14 ② 조합 시범 발주 — run `run_5e41335924e7` · task `task_513ea8e63f40` · dispatch `ctx_a9d48a54d279` · 워커 `term_3ff5dc93-6f21-4c02-bd11-bf9548db0957`(claude-opus-5-5) · 브리프 [combo-pilot-brief.md](./combo-pilot-brief.md) · 산출 `silver-model/drafts/combo/`
- 2026-11-14 ② 시범 결과(검증 PASS 재실행) — 시술 29 · 케이스 91 · 판정 462 · 가격표 케이스 0. 사용자 결정(「추천대로」): 제네시스 = 선택적 광열 · 대상 빈칸 · **재료는 연결 표 procedure_material**(복합 성분) · 열린 성분 수액 = 메뉴 · 원장에 정보 없는 항목 = 보류(판정만, 나중에 원장 보강 — 말로 준 정보는 근거 「사용자 제공」으로 구분) · 시술 이름 「선택적 광열 레이저」 「비박리성 레이저」 유지 · **새 계열 M18 지방분해 주사**(M16 의 DCA · PPC 등 이동, silver 반영은 확인 뒤). 제품이 케이스에 못 닿으면 시술까지(보톡스 제품 17 등).
- 2026-11-14 발주 4(run `run_5e41335924e7`, 발주 순서대로 task): 시범 확정 [combo-pilot-finalize-instructions.md](./combo-pilot-finalize-instructions.md) `task_1c4611ac5896` · A 주입(M2 M3 M4 M5 M6 M17 + M18) [combo-a-brief.md](./combo-a-brief.md) `task_f24c05056f26` → drafts/combo-a · B 기기·실(M7 M9 M10 M11 M14) [combo-b-brief.md](./combo-b-brief.md) `task_78f14b7c70be` → drafts/combo-b · C 피부 관리(M12 M13 M15) [combo-c-brief.md](./combo-c-brief.md) `task_eff0702d8a46` → drafts/combo-c. 코드 범위 A PRC-100/CAS-1000 · B PRC-300/CAS-3000 · C PRC-500/CAS-5000. 끝나면 코디 검증 → 합치기 → silver.
- 2026-11-14 ② 본작업 A·B·C 완료(각 check PASS 재실행): 시범 포함 시술 134 · 케이스 259. 사용자 「추천대로」: 각 notes §6 전부 추천 — 실 = 재질 × 원리(코그 = 견인 · 모노 = 콜라겐) · 인모드FX = 고주파까지(원장 「RF 니들」 ↔ 제품 사전 비침습, 확인 목록) · 잼버실 = 제품만(원장 PCA ↔ 사전 PDO, 확인 목록) · 모발이식 보류 · problem-packages 「지방분해」(M14) 분류 칸 · 열린 성분 필링 16 = 메뉴. 아직 안 닿은 것(보류 · 원리 빈칸 · 제품→케이스 못 닿음 · 사전 후보)은 합치기 notes 의 매핑 현황 집계로.
- 2026-11-14 ② 합치기 발주 — task `task_9152b378ae8f` · dispatch `ctx_f192f86f7391` · 워커 `term_9a5c0671-20e0-4cfa-a898-8436578051c0` · 지시서 [combo-merge-instructions.md](./combo-merge-instructions.md) · 산출 silver 5표 + M18 · product_modality 11 · notes/combo-*.
- 2026-11-14 안 이어진 것 처리 순서(사용자 「추천 순서대로」): 합치기 → ① 사전 보강(combo-dict-candidates 승인 후 사전 행 추가 + 다시 잇기, 워커 1회) → ② 원장 확인 목록 한 장(보류 · 인모드FX · 잼버실 · 제품→케이스 못 닿음 — 원장 4판 또는 「사용자 제공」 근거로 채움, 외부 보충 안 함) → ③ 관계(②와 병행 가능).
- 2026-11-14 **② 합치기 완료 → silver**(merge-check PASS 재실행): procedure 134 · procedure_material 167 · procedure_case 259 · case_method 98 · case_product 328 · modality 18(M18) · product_modality 10 바꿈 1 삭제 · alias 988 · source_ref 22345 · notes/combo-*(판정 합본 1696 · 사전 후보 54 · id 대응). 매핑: 원리 빈 시술 20 · 대상 빈 케이스 114 · 제품 케이스까지 210 / 시술까지만 81 / 안 닿음 16 · 보류 8. 백업 archive/silver-before-combo.
- 2026-11-14 사전 보강 발주(사용자 「추천대로」: 후보 54 전부 · 다시 잇기 · 합치기 판단 — 두피 메조 그대로 · 엑소좀 두피주사/두피 PRP 케이스로 · 병합 언급 그대로 · PRC-004 name_en 보충) — task `task_dd14f235fea1` · dispatch `ctx_8a706b5ef015` · 워커 `term_2f84d402-e38f-4e2b-8508-30183857fbe3` · 지시서 [dict-fill-instructions.md](./dict-fill-instructions.md) · 산출 silver + drafts/dict-fill/.
- 2026-11-14 사전 보강 완료(dict-fill-check PASS 재실행): 후보 54 → 새 행 34 · alias 7 · 넣지 않음 13 · 원리 빈 시술 20 → 2 · 보류 8 → 5 · 시술 136 · 케이스 261 · 제품 케이스까지 216. 판단 9 = 추천(a) 전부 → 데이터 변경은 2(product_method 4) · 8(코그실 3 설명) — 발주 `task_2417e7f90130` · `ctx_0435c6dbfc01` · 워커 `term_2f6cebab-4ece-4d4f-99ca-0b54332aeb7f` · [dict-fill-finalize-instructions.md](./dict-fill-finalize-instructions.md). merge-check 는 이제 FAIL(합치기 시점 고정) — 기준 검사는 dict-fill-check.
- 2026-11-14 사용자: 인터넷 조사 · 원장 확인 목록보다 **③ 관계 설계안 먼저**. (추천 안: 제품 사실만 웹 후보 「외부 확인」 칸 · 임상 사실은 ③ 뒤 별도 외부 검증 — 미정)
- 2026-11-14 사전 보강 확정(PASS 재실행): product_method +4(PMET-0060~63) · 코그실 3 설명 · 바뀐 silver 3표뿐. **② 단계 끝.**
- 2026-11-14 ③ 관계 설계(사용자 「응」 — 5건 추천): 관계는 계열 · 시술 · 케이스 어디든(target_table + target_code, 아래로 복사 안 함 · 조회 때 물려받기) · 시점/기간/빈도/간격 = 원문 + 숫자는 원문에 있을 때만 · 빈도 수치와 서술 등급 병기 · 원장 충돌 = 주제 전용 원장 채택(부작용 complications · 금기 contraindications) · 패키지 = package/package_item(상품 제외) · 표: indication · outcome · adverse_risk(+frequency · factor · guidance) · contraindication · procedure_relation · package(+item) · citation(+link). 시범 M1 · M2 → 검수 → 나머지.
- 2026-11-14 ③ 관계 시범 발주 — task `task_1496864f1d07` · dispatch `ctx_160b955b1ad6` · 워커 `term_0cc27dcf-c6f5-477b-8071-889b22f61ca9` · 브리프 [relation-pilot-brief.md](./relation-pilot-brief.md) · 산출 `silver-model/drafts/relation-pilot/`
- 2026-11-15 ③ 관계 시범 결과(PASS 재실행): 판정 4982 잎 · indication 123 · outcome 131 · adverse_risk 286(+빈도 45 · 요인 170 · 대처 490) · 금기 62 · 시술 간 135 · 패키지 32 · 문헌 22 · 담을 칸 없음 227. 사용자 결정: **칸 추가는 정규화해서**(번역 → statement_translation · 위험 등급 → rating_scale + adverse_rating · 부정 진술 → polarity 3값 · 다운타임 → recovery · 시너지 목표 → procedure_relation_effect · 사람 조건 → indication_condition/package_condition · 후속 일정 → package_schedule · 패키지 1:1 값 · pmc 는 칸) · **붙는 자리에 product 추가** · 케이스 4(관자놀이 · 팔자 · 입술 보톡스, 미간 필러) silver ② 에 · 충돌 5 = 보수적 · 전용 원장 쪽 · 쁘띠시술 적응 안 만듦.
- 2026-11-15 ③ 관계 시범 확정 발주 — task `task_a1c1dae3dc5c` · dispatch `ctx_c7dae1268969` · 워커 `term_51f5095e-c45a-43ee-9a0d-5cc3116e3d22` · [relation-pilot-finalize-instructions.md](./relation-pilot-finalize-instructions.md). 끝나면 §9 표 구조로 나머지 16계열 묶음 발주(순차).
- 2026-11-15 ③ 관계 시범 확정(PASS 재실행): 담을 칸 없음 227 → 0 · 새 표 8(rating_scale · adverse_rating · statement_translation · recovery · procedure_relation_effect · indication_condition · package_condition · package_schedule) · 제품 층 관계 842행(제품 50) · silver 에 케이스 4(CAS-092 · 093 · 094 · 1044) + 근거 28. 표 구조 정본 = drafts/relation-pilot/relation-notes.md §9-2. §9-4 남은 판단(시너지 이유의 고민 · 연령대 문맥 · ADV-145 · 척도 범위)은 지금대로로 진행.
- 2026-11-15 ③ 관계 본작업 4묶음 발주(사용자 「끝나고 순차적으로」, 발주 순서 a→d): A 주입(M3 M4 M5 M6 M16 M17 M18) · B 기기·실(M7 M9 M10 M11 M14) · C 빛·플라즈마(M8 M13) · D 피부 관리(M12 M15) — 브리프 relation-[abcd]-brief.md · 산출 drafts/relation-[abcd]/ · 겹침 규칙: 시술 간 관계는 M1·M2 끝 제외 · 다른 묶음 끝이면 작은 계열 번호 묶음 · 패키지는 M1·M2 포함 제외 · 최소 계열 묶음 · silver 안 고침(케이스 후보는 dict-candidates). task(목록 순): task_7b2e8ba51e1f · task_796dee5cb44e · task_d77da7a75ac5 · task_c516c92dc6c1.
- 2026-11-15 ③ 관계 A·B·C·D 완료(각 check PASS 재실행 · silver 불변): 판정 잎 계 26,923 · 적응 1,734 · 효과 1,588 · 부작용 위험 2,814 · 금기 349 · 시술 간 867. 사용자 「추천대로」: 칸 추가(adverse_guidance.evidence_text · contraindication.site_code · contraindication.polarity) · target_table 에 package · ② 코드 없는 메뉴 → package 로 · 시술 아님/성분 진술은 관계에서 뺌 · 코드 없는 시술 종류는 계열 층 + note · 묶음 경계 넘긴 ~60잎 합칠 때 확인 · 이소트레티노인 = consent 깊이별 행 · 충돌 14 각 decision 그대로 · 사파이어레이저 제품 추가 · 사전 후보 54 는 다음 사전 보강.
- 2026-11-15 ③ 관계 합치기 발주 — task `task_6acaa3e6564e` · dispatch `ctx_36fd893051c8` · 워커 `term_daf7072b-9549-4988-b754-027b045fd492` · [relation-merge-instructions.md](./relation-merge-instructions.md) · 산출 silver 관계 20표 + notes/relation-*. 다음: 사전 보강(후보 54) → 원장 확인 목록.
- 2026-11-15 **③ 관계 합치기 완료 → silver**(merge-check PASS 재실행): 관계 20표 · 적응 1,683 · 효과 1,592 · 부작용 위험 2,815 · 금기 350 · 시술 간 898 · 패키지 119 · 문헌 63 · 사파이어레이저 PRD-785 · 백업 archive/silver-before-relation. 입구: 시술 136 모두 관계 있음 · 고민 260 → 시술/케이스 192 · 계열 층만 50 · 안 닿음 18. 사용자 「그렇게 하자」: §5-1 빠진 잎 ~160 채우기 + §5-3 조합 메뉴 진술 → package (후속 발주) · §5-2/5-4/5-5 그대로. 다음: 사전 보강(relation-dict-candidates 53) → 원장 확인 목록(안 닿는 고민 18 · 보류 · 원장≠사전 제품).
- 2026-11-15 관계 보완 발주 — task `task_10b8709a5da8` · dispatch `ctx_fa7cda03eb38` · 워커 `term_b74b4d01-0107-4823-b5a1-eeb50be8b823` · [relation-gapfill-instructions.md](./relation-gapfill-instructions.md) · 산출 silver + drafts/relation-gapfill/.
- 2026-11-15 **관계 보완 완료**(gapfill-check PASS 재실행 · 바뀐 silver = 관계 7표 + source_ref): A 빠진 잎 198 중 143 관계 행(55 안 담음 — 이유) · B 조합 메뉴 4개 진술 45행 → package · 새 충돌 RCF-022~027 · 입구 변화 없음(고민 192/50/18) · 관계 있는 제품 296 → 298. **사용자 판단 대기 3**(gapfill-notes §6): 6-1 하모니카 M2 칸 HA 문장(추천 그대로 + 충돌 표시) · 6-2 효과 시점 충돌 3(추천 둘 다 유지) · 6-3 코드 없는 미녹시딜 두피 메조 · 프로락틴 · 알렉스필(추천 사전 보강 2차에 케이스 후보로). 다음 = 압축 → 3건 확인 → 사전 보강 2차 발주.
- 2026-11-15 보완 판단 3 결정(사용자 「발주해」): 하모니카 = HArmonyCa 합침(11-11 외부 조사) 유지 · 원장 M2 칸 HA 문장은 PRD-114 에서 뗌 → 원장 확인 목록 · 효과 시점 「충돌」은 동명이물/원장 오기(M4 제품 「스킨보톡스」 = 아르기닌 성장인자 복합체 · M9 제품 「LDM」 = RF 리프팅 기기 설명) → 진술 뗌 · 원장 확인 목록 · 미녹시딜 두피 메조 · 프로락틴 · 알렉스필 = 사전 보강 2차에서 케이스 후보. 새 파일 notes/ledger-check-list.csv(원장 작성자 확인 목록).
- 2026-11-15 사전 보강 2차 발주 — task `task_43c439074598` · dispatch `ctx_e00922007077` · 워커 `term_4dadf540-83e0-45c1-be13-26188a7d541f` · [dict-fill-2-instructions.md](./dict-fill-2-instructions.md) · 산출 silver + drafts/dict-fill-2/. 끝나면 코디 검증(check 재실행 + silver cmp) → 원장 확인 목록 한 장.
- 2026-11-15 **사전 보강 2차 완료**(dict-fill-2-check PASS 재실행 · 바뀐 silver 12표): 후보 53 → 새 부작용 5(ADV-184~188) · alias 2 · 넣지 않음 46(11-12 결정 「피부 개선류 · ~경우 · 기전 분류」에 걸림) · C 반영: 하모니카 M2 · 스킨보톡스(M4 제품) · LDM(M9 제품) 진술 42행 뗌 · 새 시술 2(PRC-559 미녹시딜 두피 메조 · PRC-560 프로락틴주사) · 케이스 3(CAS-5080 · 5081 · CAS-095 알렉스필) · notes/ledger-check-list.csv 3행(LCK-001~003). 입구 그대로(고민 192/50/18) · 시술 138 · 케이스 268. 판단 6(notes §5)은 모두 추천 (a) — 4 프로락틴/프로작 엇갈림 · 5 뜻 불명 3 은 원장 확인 목록으로. 다음 = 원장 확인 목록 한 장.
- 2026-11-15 사전 보강 2차 판단 6 = 추천 (a) 전부(사용자 「다음 단계 진행해」). 원장 확인 목록 한 장 발주 — task `task_e05ad1e036cb` · [ledger-check-instructions.md](./ledger-check-instructions.md) · 산출 notes/ledger-check-list.csv(덧붙임) · notes/ledger-check-sheet.md · drafts/ledger-check/ · silver 불변 · 외부 조사 안 함(check_by 칸으로 「외부 확인 후보」만 표시).
- 2026-11-15 **원장 확인 목록 완료**(ledger-check-check PASS 재실행 · silver 불변 · LCK-001~003 값 그대로 · 기존 확인 목록 3개 불변): notes/ledger-check-list.csv 303행 · notes/ledger-check-sheet.md 37묶음(원장 작성자 29 · 외부 확인 후보 4 · 원장 확인 아님 4). 판단 4(ledger-check-notes §4) 모두 추천 (a). 다음 = silver 통합 검사 + ERD 문서.
- 2026-11-15 원장 확인 목록 판단 4 = 추천 (a) 전부(사용자 「응」). silver 통합 검사 + ERD 발주 — task `task_9f98a827b58f` · [silver-check-instructions.md](./silver-check-instructions.md) · 산출 drafts/silver-check/ · notes/silver-erd.md · notes/silver-tables.md · silver 불변.
- 2026-11-15 **silver 통합 검사 완료**(silver-check 재실행 = FAIL 8 · WARN 401 — notes 표와 같음 · silver 불변): 참조 R1~R7 · id · 형식 · ② · ③ 원문/숫자 대조 전부 통과. FAIL 8 = M12 이름 괄호 · 새 부작용 ADV-184~188 근거 칸(5+1) · ADV-188 설명 코드 숫자. WARN = product_modality 근거 300 · 별칭 정리(괄호 38 · 같은 이름 13 · 띄어쓰기 23 · 근거 글자 13) · 설명 인용 8 등. 알려진 빈칸: 대상 빈 케이스 115 · 부위 빈 197 · 원리 빈 2 · 보류 5. 「(정의 없음)」 칸 29. 산출 drafts/silver-check/ · notes/silver-erd.md · notes/silver-tables.md.
- 2026-11-15 통합 검사 걸린 것 = 추천대로(사용자 「응」). silver 고치기 발주 — task `task_e4711050f40d` · [silver-fix-instructions.md](./silver-fix-instructions.md) · FAIL 8 · WARN 고침 ~75 · 나머지 알려진 예외 · 정의 없는 칸 29 뜻 초안 · 백업 archive/silver-before-fix. 원장 확인 목록 아티팩트 https://claude.ai/artifact/Bhfjdjf1Mtu2gWsxrexZPU — 사용자가 fable 로 외부 조사 예정(결과 CSV 받으면 「확인」만 외부 근거로 채움 · 「추정」은 따로 확인).
- 2026-11-15 **silver 고치기 완료**(silver-check 재실행 PASS · FAIL 0 · WARN 0 · 알려진 예외 355 고정 · 바뀐 7표 = adverse · alias 1007→972 · method · modality · organization · product · source_ref 46359→46365 · 백업 archive/silver-before-fix). 칸 29 뜻 초안 → notes/silver-tables.md 「(초안)」. 판단 7(silver-fix-notes §5) 사용자 확인 대기.
- 2026-11-15 사용자 외부 조사(fable) 결과 drafts/external-research/external-research.csv(448줄 · id 210 · 확인 164 · 추정 163). 결정(사용자 「그렇게 해」): 제품 사실 「확인」(대조 일치 + 식약처 재조회 일치)만 silver 에 외부 근거로 · 원장 ≠ 외부면 외부 값 + 원장 오류 의심 기록 · 추정 · 임상 · 의미 · 관계 행은 넣지 않고 원장 확인 목록 ext 칸 · 떼어 둔 42행 그대로 · 멜스몬 · 울트라V 정정 · silver 고치기 판단 7 추천대로. 발주 task `task_31ee3522c74c` · [external-fill-instructions.md](./external-fill-instructions.md).
- 2026-11-15 **외부 조사 반영 완료**(silver-check PASS · external-fill-check PASS 재실행 · 바뀐 silver 6표 = alias +5 · organization +10 · product 칸 · product_material +4 · product_organization +18 · source_ref +174 · ③ · 시술 · 케이스 불변 · 백업 archive/silver-before-external-fill). 넣은 줄 84 · 식약처 재조회 35 전부 맞음 · 회사 없는 제품 57→52 · 원장 확인 목록 ext 칸 210 id · LCK-304(PRD-684) · 칸 29 뜻 확정. 판단 2(external-fill-notes §7) 대기: 원장 오류 값 연결 6 · 아발란체 755nm.
- 2026-11-16 판단 2 결정(사용자 「추천으로 · 아발란체는 조사」): 원장 오류 값 연결 5 뗌(해피리프트 그대로) · 아발란체 정체 조사 → 근거 있으면 silver 를 그 장비 사실로. **사용자 원칙: 「원장이 틀릴 수 있다. silver 만 제대로 들어가면 된다」** — 제품 사실은 공식 출처 확인 값이 silver, 틀린 원장 값은 notes 「원장 오류 의심」. 발주 [external-fill-2-instructions.md](./external-fill-2-instructions.md).
- 2026-11-16 **원장 오류 연결 · 아발란체 완료**(silver-check PASS · external-fill-2-check PASS 재실행 · product_material −4 · product_organization −1 · product PRD-332 칸 2 · source_ref +7 · ③ · 시술 · 케이스 불변): 아발란체 = Fotona AvalancheLase(식약처 수허25-7호 · 신한씨스텍 · LXP 755+1064nm · 제모). 판단 3 대기: 아발란체 색소 적응 · 효과 관계 행 · 큐어젯 설명 · 클라리티2 · 아포지엘리트플러스 같은 꼴.
- 2026-11-16 판단 3 = 추천(사용자 「추천으로 가자」): 아발란체 색소 관계 행 뗌 · 혈관 병변 남김 · 큐어젯 설명 = 식약처 사실 · 클라리티2 · 아포지엘리트플러스 같은 방식 조사 반영. 발주 [external-fill-3-instructions.md](./external-fill-3-instructions.md).
- 2026-11-16 아발란체 FDA 용도에 양성 색소 · 혈관 병변 있음(AV-4 인용 누락) → 사용자 「추천」: 글자 기준 — 문신 · 색소 제거 효과 · 532nm 케이스 연결만 뗌, 기미 · 주근깨 · 검버섯 남김 + 확인 목록, 혈관 남김.
- 2026-11-16 **아발란체 관계 · 큐어젯 · 클라리티2 · 아포지 완료**(silver-check PASS · external-fill-3-check PASS 재실행 · case_product −4 · outcome −2 · product_material −1 · source_ref +9 · 시술 · 케이스 불변 · 입구 192/50/18 그대로): 클라리티2 = Lutronic CLARITY II · 아포지엘리트플러스 = Cynosure Elite+/Apogee Elite · 둘 다 755+1064nm(532 원장 오류 의심). LCK-305~307. 판단 3 대기(아포지 문신 · 클라리티2 적색 note · 큐어젯 gas-powered).
- 2026-11-16 판단 3 = 추천(사용자 「응」): 아포지 문신 남김 · 클라리티2 적색 note 그대로 · 큐어젯 고압 공기 되살림. 상품 설계안 + 시범 발주(큐어젯 되살림 A 포함 · 상품은 drafts/offer 만) — [product-offer-design-brief.md](./product-offer-design-brief.md).
- 2026-11-16 **상품 설계안 · 시범 완료**(offer-check PASS · silver-check PASS 재실행 · silver 변경 = 큐어젯 PMAT 되살림 1 + 근거 2): drafts/offer/ 8표(price_list · offer 122 · offer_item 163 · offer_quantity 129 · offer_site · offer_concern · offer_effect · offer_material) · 상품 122 → 케이스 58 · 시술까지 42 · 제품만 4 · 못 닿음 18(실 재질 · 플라즈마 핫/콜드 · 성분 미표기 · 줄기세포 종류). 판단 11(offer-notes §6) 대기.
- 2026-11-16 상품 판단 11 = 추천 (a) 전부(사용자 「응!」). 상품 8표 silver 반영 · 못 닿은 상품 18 → 원장 확인 목록 발주 — [offer-finalize-instructions.md](./offer-finalize-instructions.md).
- 2026-11-16 **상품 silver 반영 완료**(silver-check PASS(WARN 6) · offer-check PASS 재실행 · silver 55표 = 새 상품 8표(offer 122 · offer_item 163 · offer_quantity 129 …) · alias +8 · source_ref +1315 · product PRD-670 설명 · 그 밖 불변 · 백업 archive/silver-before-offer). 못 닿은 상품 18 → 원장 확인 목록. 판단 3 대기(alias 괄호 2 · 띄어쓰기 4 · sheet G39 행).
- 2026-11-16 상품 판단 3 = 코디 추천(사용자 「응!」): 계열 alias 괄호 풂 · 제품 띄어쓰기 alias 4 뺌 · sheet G39 행. gold 설계안 + 시맨틱 매핑 + 질문 시범 발주(A 별칭 정리 포함 · gold 는 drafts/gold 만) — [gold-design-brief.md](./gold-design-brief.md).
- 2026-11-16 **gold 설계안 · 시범 완료**(gold-check PASS · 구조 문제 0 · silver-check PASS(WARN 0) 재실행 · silver A = alias −5 · source_ref −5): drafts/gold/ 15표(g_entry · g_scope 물려받기 · g_profile · g_indication · g_outcome · g_adverse(+detail) · g_contraindication · g_pair · g_package · g_recovery · g_offer · g_node/g_edge · g_evidence) · semantic-map.md(개념 18 · 관계 16 · 규칙 6) · 질문 35 중 답함 32 · silver 빈칸 1 · 원장 확인 2. 판단 6(gold-notes §6) 대기.
- 2026-11-16 gold 판단 6 결정(사용자 「응!!」): 같은 날 칸 silver 추가(코디 추천) · 상위 제품 물려받지 않음 · product_procedure 표 추가 · 저장소 = 관계형 먼저 + 그래프 내보내기 · 문헌 gold 나중 · 근거 표 참조로. silver 보강 + gold 확정(silver-model/gold/) 발주 — [gold-finalize-instructions.md](./gold-finalize-instructions.md).
- 2026-11-16 **silver 보강 2 · gold 확정 완료**(silver-check PASS(WARN 0) · gold/gold-check.py PASS · 구조 문제 0 재실행 · silver = procedure_relation 칸 2(same_day · same_day_text: 가능 77 · 조건부 13 · 불가 22) · 새 product_procedure 81 · source_ref +224 · 백업 archive/silver-before-gold-final). gold 확정 = silver-model/gold/(15표 · README · semantic-map · questions 37 — 답함 34 · 원장 확인 2 · silver 빈칸 1 · g_evidence 13MB → 1.5MB 참조). 판단 3(gold-final-notes §5) 대기. 다음 = 마감.
- 2026-11-16 같은 날 판정 3 = 추천(5 · 4 불가 그대로 · 3행 불가로 채움) · 용어집(notes/glossary.md) · 값 목록(notes/vocabulary.csv + silver-check 검사) · 외부 코드 연결 표 external_code 설계만(빈 표) — 사용자 「응 추천이랑 … 반영해서 작업 하자」. 발주 [glossary-instructions.md](./glossary-instructions.md). 다음 = 마감(커밋 · PR · 회고 · archive-work.sh).
- 2026-11-16 정정: PRL-0884~0886 「같은 날 불가」 kind 는 원장 갈래가 아니라 11-15 합본에서 붙인 것(코디가 잘못 말함). 사용자 「추천」: 불가 · same_day_text 「PDO+비가교HA 병용 금기」(병용 금기 ⊃ 같은 날 불가) · E7 예외 3행.
- 2026-11-16 **용어집 · 같은 날 3 완료**(silver-check PASS(WARN 0) · gold-check PASS 재실행 · notes/glossary.md 용어 73 · notes/vocabulary.csv 값 357 · silver-check V3 · 빈 표 external_code). 판단 2 = 추천(넓음/좁음 = 외부 코드 기준 · 표준 값 뜻 빈칸). **데이터 보관 결정(사용자 11-16 「깃 이그노어하고 로컬에만」)**: kknaks_profile 은 PUBLIC → silver-model/(195MB · silver · gold · notes · drafts · archive)은 .gitignore(`orchestration/work/**/phub-ledger-redesign/silver-model/`) + .git/info/exclude · 로컬 사본 = /Users/kknaks/git/toy_pr2/kknaks_profile/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model/(diff 같음 확인). 커밋 대상 = 지시서 · _RESUME · .gitignore · 회고.
- 2026-11-16 사용자: 회고 + PR 까지만 · **실험용이라 회사 레포(프로시져 허브)에 머지 안 함** · 이 작업으로 다음 작업에서 gold 데이터 + jev + LLM 연결 시험 계속 → archive-work.sh 는 지금 안 돌림. 회고 발주(fable) — [retro-brief.md](./retro-brief.md) → para/projects/company/procedure-hub/log/2026-11-16-phub-ledger-redesign.md.
