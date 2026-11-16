# issues — patient-education.json 1차 조사 미결·한계

**1차 수집 범위 종료 · 원장 전체 완료 아님.** 상태 문자: A=에이전트 추출/해석 오류 · B=원문 정보 부족 · C=현재 사용자 결정 필요 · K=알려진 분석 한계 · P=잠정 관찰 · F=후속 의미 조사 · I=원문 내 불일치·표기 이상. 원문 내 불일치는 C 가 아니다.

## 요약

- **A(에이전트 오류) 0 남음.** 작업 중 발견해 고친 것: ① 정규식 대조로 드러난 수치·빈도·근사 구절 누락(구절 단위 49건 보충) ② verify 문장 탈락 검사가 잡은 S01 `/categories/0/common_concerns/2/a` 문장 2개 미보존(문장 전체 기록 추가) ③ 별도 읽기 검토(형태소 수식어 대조)로 패턴 밖 구절 27건 보충. 각 보충은 manual 메모에 출처를 남겼다.
- **C(사용자 결정) 0.** 근거: 열린 항목은 모두 원문 부족(B — 사실을 사용자에게 추측시키지 않는다)·잠정(P)·후속 의미 조사(F — 21개 원장 비교 후 묶어서 제시)·표기 이상(I — 원본 보존 지시 아래 후속 확인 후보)·도구 한계(K — 에이전트 판단)로 분류되었다. 지금 선택을 받아야 진행되는 항목이 없다. 이 판정은 아래 전체 목록을 검토한 결과다.
- **B 원문 정보 부족 36** — 묶음: ① 지속·발현 시간의 주어/기준 시점 생략(「약 3-6개월 지속됩니다」 등) ② 「적절한 양·세기·간격」「과도하게」「고출력」「고용량」 기준값 없음 ③ 빈도 어휘(드물게·매우 낮음·많아요)에 수치·분모 없음, 수치(40~50%·20-25%·0.2~0.5%)에 분모·출처·대상 집단 없음 ④ 성분·약·재질·종류명 미기재(특수 성분·녹이는 약·녹는 실·바른 약물) ⑤ 「최근 연구」「보고」「임상연구」 출처 없음 ⑥ 반복 시술 간격 없음 ⑦ 응급 징후·대처 기술 없음(혈관 문제·아나필락시스).
- **응급 징후:** 원장 전체에서 응급 관련 표현은 「응급 대처가 가능한 병원」(M2)·「아나필락시스」(M16) 정도다. 증상별 응급 징후 서술은 없다(B). 설명 표현을 임상적으로 검증됐다고 승인하지 않는다.
- **I 1** — M9 「써마지은」 조사 표기(2출현). 원본은 고치지 않는다.

## K — 형태소 분석 한계 (출현별 표 밖)

- 출현별 표(아래)는 직접 확인한 오분절·오태깅만 담는다. 그 밖 토큰의 정확성은 검증하지 않았다(전수 정답 검증 아님).
- 품사 흔들림은 출현별로 기록하지 않았다: 같은 말이 NNG/NNP 를 오간다(토닝·프락셔널·필러·콜라겐 등). 「붓기」는 붓/NNG+기/XSN(2출현)과 붓/VV-I+기/ETN(6출현)으로 갈린다. 「붉은기」는 붉/VA+은/ETM+기/NNG 로 나뉜다. 「따끔함」 끝 ᆷ 이 EF/ETN 으로 갈린다. 「희석량」의 「량」이 NNG 로 남는다.
- 접두사 「비/미/무」(XPN)는 오분절이 아니다. 부정을 토큰으로 찾으려면 XPN 을 포함해야 한다. 「비수술」「미허가」는 부정으로 읽히지만 「무균적으로」는 요구 조건이다(부정 오탐 위험). 「고출력」의 「고」도 XPN 이다.
- 길이 0 토큰(「써마지은」의 이/VCP)은 surface 가 빈 문자열이다.
- 라틴 약어(PRP·RF·SMAS·PIH·PAH·SJS/TEN·AHA·BHA·TCA·MTS·HIFES·EMS·DNA·PN)는 SL 로 남는다. 영어 형태소 분석은 하지 않았다. 풀이 유무는 표현 기록 `paraphrase` 로만 표시했다.
- 「3-6」처럼 하이픈 범위는 W_SERIAL 한 토큰이고, 「0.2~2.0」「수시간~1일」은 SN/SO 로 쪼개진다. 범위 표기(「-」/「~」)가 섞여 토큰 기준 범위 추출 규칙이 하나로 안 된다.

## F — 후속 의미 조사 (21개 원장 비교 후 묶어서 다룸)

- 카테고리 id(M1~M17)·name 과 다른 원장 카테고리 체계의 대응 · 「/」 병기 호칭(바이오스티뮬레이터/콜라겐부스터, PRP/자가혈, HIFES/EMS)의 관계 · 제품명(리쥬란·울쎄라·써마지·엠페이스·포텐자·인모드·쿨스컬프팅)과 카테고리의 관계 · 카테고리 간 참조(필러↔콜라겐부스터·스킨부스터, 니들RF↔프락셔널 레이저, 줄기세포↔MTS·레이저) · 같은 문자열의 역할 차이(「눈꺼풀 처짐」 부작용 vs 고민) · 행동 지시와 근거 서술의 분리.
- 의미 관계·노드·정규화는 1차 범위 밖이다. 관찰이 없다고 의미가 없다는 뜻이 아니다.

## 상태별 집계 (manual 관찰 + 오분절 기록에서 생성)

| 상태 | 뜻 | 건수 |
|---|---|---|
| A | 에이전트 추출/해석 오류 | 0 |
| B | 원문 정보 부족 | 36 |
| C | 사용자 결정 필요 | 0 |
| I | 원문 내 불일치·표기 이상 | 1 |
| K | 알려진 분석 한계 | 26 (관찰 1 + 오분절 출현 25) |
| P | 잠정 관찰 | 42 |
| F | 후속 의미 조사 | 10 |

## 관찰·미결 전체 목록 (구획 순)

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| S00-O1 | P | `/version` | 버전 식별자 "1.3". 언어 텍스트 아님 — 형태소 제외 |
| S00-O2 | P | `/updated` | 날짜 "2026-07-26". 무엇의 갱신일인지(파일 전체/개별 항목) 원문에 범위 표기 없음 |
| S00-O3 | P | `/categories` | 배열 17개, 각 원소는 동일 9키(id·name·patient_name·simple_explanation·how_it_works·duration_simple·pain_level·downtime·common_concerns). common_concerns 는 모두 {q,a} 3개 |
| S00-O4 | F | `/categories` | id(M1~M17)·name 은 다른 원장의 카테고리 체계를 가리키는 것으로 보이나 이 원장 안에는 대응 정의가 없다. 연결은 후속 과제(다른 원장은 열지 않았다) |
| S01-O1 | B | `/categories/0/duration_simple` | 무엇이 3-6개월 지속되는지(효과) 문장에 주어가 생략됨 |
| S01-O2 | B | `/categories/0/how_it_works` | 주사하는 「약」의 이름·성분이 이 항목에 없다 |
| S01-O3 | B | `/categories/0/common_concerns/0/a` | 「적절한 양」「과도하게」의 기준값 미기재 |
| S01-O4 | B | `/categories/0/common_concerns/1/a` | 「의학적으로」의 근거 출처 미기재 |
| S01-O5 | P | `/categories/0/common_concerns/2/a` | 행동 지시(삼가·눕지 말고·문지르지 마세요)와 근거 설명(최근 연구…·이 주의사항은…)이 한 값에 섞여 있다. 시간 기준이 「당일(대략 24시간)」「시술 후 약 4시간」 두 개 |
| S01-O6 | F | `/categories/0/common_concerns/2/a` | 「톡신」과 name 「보톡스」의 관계(호칭 차이)는 의미 단계 과제. 「최근 연구」의 주장과 주의사항이 서로 다른 강도라 구조화 시 근거·지시 분리 필요 |
| S01-O7 | B | `/categories/0/common_concerns/2/a` | 「최근 연구」의 출처 미기재 |
| S02-O1 | P | `/categories/1/how_it_works` | 히알루론산은 「과 비슷한 젤」로 비교 대상이며, 필러 성분이 히알루론산이라고 단정하지 않는다. 같은 카테고리 a(/common_concerns/0/a)는 「히알루론산 필러는」으로 하위 종류를 한정해 필러에 다른 종류가 있음을 시사 |
| S02-O2 | P | `/categories/1/how_it_works` | 「팔자주름」은 고민 명칭이 부위 나열(입술·광대)에 함께 쓰였다. 부위/고민 구분은 후속 |
| S02-O3 | B | `/categories/1/duration_simple` | 제품별·부위별 지속 기간 값은 원문에 없다(「따라 다름」만) |
| S02-O4 | B | `/categories/1/common_concerns/0/a` | 「녹이는 약」 이름 미기재. 「매우 드뭅니다」 수치 없음 — 백분율로 바꾸지 않는다 |
| S02-O5 | B | `/categories/1/common_concerns/2/a` | 혈관 문제의 구체 사건·응급 징후·대처 방법이 기재되지 않음(「응급 대처가 가능한 병원」만) |
| S02-O6 | F | `/categories/1/common_concerns/2/q` | 「혈관에 문제」가 어떤 사건을 가리키는지는 다른 원장(합병증 등)과 연결해 판단할 후속 과제 |
| S03-O1 | F | `/categories/2/name` | 「/」 로 묶인 두 호칭의 관계(동의어/대안/상하) 미확정 — README 기호 규칙만으로 확정하지 않는다 |
| S03-O2 | B | `/categories/2/how_it_works` | 「특수 성분」 이름 미기재 |
| S03-O3 | P | `/categories/2/duration_simple` | 시간 역할이 발현(4-6주)과 지속(1-3년)으로 분리 기재된 사례 |
| S03-O4 | P | `/categories/2/common_concerns/0/a` | 「4-6주 후부터」 기준 시점 생략. duration_simple 「효과 발현까지 4-6주」와 같은 수치. 「보통 3회」 간격 미기재(B) |
| S03-O5 | P | `/categories/2/common_concerns/1/a` | 마사지 권고에 대한 부정(입증되지 않음)·조건부 허용(하시더라도…부드럽게)이 겹친 구조 |
| S03-O6 | F | `/categories/2/common_concerns/2/a` | 「필러」 참조는 S02(/categories/1)로 보이나 연결은 후속. 「지속 기간도 더 길어요」 비교는 원문 수치(1-3년 vs 6-18개월)로 정합 확인 가능 — 의미 단계에서 확인 |
| S04-O1 | P | `/categories/3/how_it_works` | 「여러 번 주사합니다」(한 회 안 다회 주사로 보임)와 duration_simple 「2-3회 반복 시술」(회차)은 다른 횟수 개념일 수 있다 — 잠정 |
| S04-O2 | P | `/categories/3/common_concerns/1/q` | 제품명 「리쥬란」이 카테고리 설명 안에 처음 등장. 「연어주사」는 통칭 |
| S04-O3 | P | `/categories/3/common_concerns/1/a` | 금기를 「해당할 수 있으므로」 가능성으로 표현 · 대상=「심한 해산물(생선) 알레르기가 있는 분」 · 시점=「시술 전」 행동 지시. 임상적으로 승인하지 않는다 |
| S04-O4 | B | `/categories/3/common_concerns/1/a` | 「반응」의 종류와 「드뭅니다」 빈도 수치 미기재 · 「대체 시술」 이름 미기재 |
| S04-O5 | B | `/categories/3/common_concerns/2/a` | 「흡수율이 … 훨씬 높습니다」 근거·수치 미기재 |
| S04-O6 | F | `/categories/3/common_concerns/1/a` | 리쥬란·PN 과 카테고리 스킨부스터의 관계(제품/성분/카테고리)는 다른 원장과 함께 후속 판단 |
| S05-O1 | P | `/categories/4/how_it_works` | 부위 역할이 둘: 채혈 부위(팔)와 주사 부위(피부). 시술 대상 부위 자체는 「피부」로만 기재 |
| S05-O2 | B | `/categories/4/common_concerns/0/a` | 「매우 낮습니다」 수치·근거 미기재 |
| S05-O3 | P | `/categories/4/common_concerns/1/a` | how_it_works 「소량」의 수치가 이 값(10-20ml 정도)에 있다 — 같은 카테고리 안 값 간 대응(잠정) |
| S05-O4 | B | `/categories/4/common_concerns/2/a` | 반복 시술 간격 미기재 |
| S06-O1 | P | `/categories/5/duration_simple` | 이 키는 다른 카테고리처럼 「N개월 지속」이 아니라 생착률(%)·부위별 비교·노화 경과를 담는다. 같은 키 이름 아래 정보 종류가 다르다 |
| S06-O2 | B | `/categories/5/duration_simple` | 「평균 약 40~50%」의 분모·대상 집단·측정 시점·보고 출처 미기재. 환자 실제 생착률로 바꾸지 않는다 |
| S06-O3 | P | `/categories/5/duration_simple` | 「~」가 이 값에서는 범위 기호로 쓰였다(다른 값은 「-」). 근사 표현 「약」「정도」가 함께 붙음 |
| S06-O4 | P | `/categories/5/how_it_works` | 부위 역할 두 개: 채취(복부·허벅지)와 주입(볼·이마·관자놀이). duration_simple 의 코·이마·볼·턱은 생착률 비교 대상 부위로 how_it_works 목록과 다르다(코·턱은 how_it_works 에 없음, 「등」으로 열림) |
| S06-O5 | P | `/categories/5/common_concerns/0/a` | 「보통 3개월 후 안정화」 기준 시점 생략(시술 후로 보임) |
| S07-O1 | B | `/categories/6/simple_explanation` | 「녹는 실」의 재질·종류 미기재(duration_simple 은 「실 종류에 따라」만) |
| S07-O2 | B | `/categories/6/duration_simple` | 실 종류별 지속 값 미기재 |
| S07-O3 | B | `/categories/6/common_concerns/0/a` | 「제대로」의 기준, 「간단히 조치」의 내용 미기재 |
| S07-O4 | P | `/categories/6/common_concerns/2/a` | 시간 역할: 당김감 소실(1-2주). downtime 의 붓기 3-5일·복귀 2-3일 후와 다른 역할 |
| S08-O1 | P | `/categories/7/downtime` | 「 / 」가 대안이 아니라 종류별 항목 구분자로 쓰였다(README 기호 규칙과 다른 쓰임 — 기호만으로 의미 확정 금지) |
| S08-O2 | P | `/categories/7/downtime` | 토닝·프락셔널·어블레이티브는 카테고리(레이저) 하위 종류명으로 보이나 이 원장 안에 정의 없음. duration_simple 은 토닝·색소 제거, pain_level 은 토닝·프락셔널로 세분 축이 값마다 다르다 |
| S08-O3 | B | `/categories/7/how_it_works` | 파장 수치·레이저 종류명 미기재 |
| S08-O4 | B | `/categories/7/common_concerns/0/a` | 「적절한 세기와 간격」「과도하게 자주」 기준 미기재 |
| S08-O5 | B | `/categories/7/common_concerns/1/a` | 자외선 차단 기간·수단 미기재 · 「수 주~수 개월」 불명확 수치 |
| S08-O6 | P | `/categories/7/common_concerns/0/q` | 두께 표현 「얇아지나요」 — 피부 두께 변화(부작용 우려)로 읽힘. 주입 깊이와 다른 정보 |
| S09-O1 | I | `/categories/8/common_concerns/0/q` | 「써마지은」 — patient_name 「써마지」 뒤 조사 「는」 대신 「은」(받침 없음). 같은 표기가 a 에도 「써마지은」. 원문 표기 그대로 보존 |
| S09-O2 | K | `/categories/8/common_concerns/0/q` | 「써마지은」 형태소 분절 이상 확인됨 — q 는 써마지/NNG 이/VCP(길이0) 은/EC, a 는 써마지은/NNG 로 출현마다 다르게 깨진다. 출현별 기록은 issues.md K 표(교정 안 함) |
| S09-O3 | B | `/categories/8/pain_level` | 마취 크림 사용 부위 미기재 |
| S09-O4 | B | `/categories/8/common_concerns/2/a` | 「일부 고출력 시술」 어느 시술인지·출력 기준 미기재 |
| S09-O5 | F | `/categories/8/patient_name` | 울쎄라·써마지(제품명)와 카테고리 「기기 리프팅」의 관계는 후속(다른 원장 연결) |
| S09-O6 | P | `/categories/8/how_it_works` | 효과 시간 역할 두 단계: 즉각적 당김 → 이후 콜라겐(duration_simple 「3개월에 걸쳐 점진적」) |
| S10-O1 | P | `/categories/9/common_concerns/0/a` | 질문(전기 자극 위험)에 금기 대상 목록으로 답한다. 대상 3종은 「시술 대상이 아닙니다」 단정, 금속 임플란트는 「알려주세요」 알림 지시로 강도가 다르다. 임상적으로 승인하지 않는다 |
| S10-O2 | B | `/categories/9/common_concerns/1/a` | 효과 체감 시점의 기준(첫 시술/코스) 미기재 · 「분이 많아요」 비율 없음 · 코스 간격 미기재 |
| S10-O3 | B | `/categories/9/name` | HIFES·EMS 약어 풀이 없음 |
| S11-O1 | P | `/categories/10/common_concerns/1/a` | 「흉터 깊이」는 고민(흉터)의 깊이로 시술 깊이(how_it_works 「정확한 깊이」)와 대상이 다르다 |
| S11-O2 | B | `/categories/10/how_it_works` | 전달 깊이 수치 미기재 |
| S11-O3 | F | `/categories/10/common_concerns/2/q` | 「프락셔널 레이저」는 S08(M8) downtime·pain_level 의 「프락셔널」과 연결될 수 있으나 후속 |
| S11-O4 | B | `/categories/10/common_concerns/0/a` | 반복 간격 미기재 |
| S12-O1 | P | `/categories/11/how_it_works` | 「0.2~2.0mm」가 바늘 길이인지 침투 깊이인지 원문은 괄호 수치로만 제시. 단위 대상 확정하지 않음 |
| S12-O2 | P | `/categories/11/common_concerns/0/a` | 홈케어 「0.25mm 이하」와 병원 「더 깊은 깊이」 비교. how_it_works 범위 하한 0.2mm 는 0.25mm 이하와 겹친다 — 원문 내 범위 겹침은 의미 단계 확인(I 로 확정하지 않음, P) |
| S12-O3 | P | `/categories/11/downtime` | 「24시간 후 세안 및 화장 가능」 기준 시점 생략. cc2 a 「세안 시기」 안내와 연결될 수 있음 |
| S12-O4 | B | `/categories/11/how_it_works` | 「바른 약물」 종류 미기재 |
| S12-O5 | B | `/categories/11/common_concerns/2/a` | 「자극 제품」 범위·자제 기간 미기재 |
| S13-O1 | P | `/categories/12/common_concerns/0/a` | 「피부색이 진한 편이면」 대상 조건 + 위험 증가 · 「적절한 평가」 내용 미기재(B). 임상적으로 승인하지 않는다 |
| S13-O2 | P | `/categories/12/common_concerns/1/a` | 질문(효과 있나)에 효과 단정 없이 「일부 클리닉에서 사용」과 위험만 답한다 — 효과 정보 부재(B) |
| S13-O3 | F | `/categories/12/common_concerns/1/q` | 「눈꺼풀 처짐」이 S01 a 에서는 부작용, 여기서는 고민으로 쓰인다 — 같은 문자열의 역할이 다르다. 병합하지 않는다 |
| S13-O4 | P | `/categories/12/downtime` | 가피(딱지) 소실 시간: downtime 은 「자연 탈락 대기」만, cc2 a 는 「보통 5-7일」 — 같은 카테고리 내 값 분산 |
| S13-O5 | B | `/categories/12/pain_level` | 마취 크림 사용 부위 미기재 |
| S14-O1 | P | `/categories/13/common_concerns/2/a` | 빈도 표현 3층: 「드물지만」(어휘)·「보고 발생률 약 0.2~0.5%」(보고 수치)·「과소보고 가능성 … 이보다 높을 수 있고」(수치 한정). 보고 수치를 환자 실제 발생률로 바꾸지 않는다 |
| S14-O2 | B | `/categories/13/common_concerns/2/a` | 보고 발생률의 분모·출처·기간 미기재 · 「남성에서 더 흔합니다」 비교 수치 없음 |
| S14-O3 | B | `/categories/13/common_concerns/1/a` | 「약 20-25%」 측정 방법·출처 미기재 |
| S14-O4 | P | `/categories/13/duration_simple` | 이 키는 지속 기간이 아니라 최대 효과 시점(3개월 후)과 「반영구적」 성질을 담는다 |
| S14-O5 | P | `/categories/13/downtime` | 값 안에 마침표로 두 문장 — 이 키에서 문장 종결형이 있는 값 |
| S15-O1 | P | `/categories/14/downtime` | 세분 축이 「가벼운/중간/깊은 필링」 — duration_simple·pain_level 은 「가벼운/깊은」 2단, downtime 은 3단(중간 추가). 「깊은 필링: 1-2주」는 무엇의 기간인지 생략(B) |
| S15-O2 | P | `/categories/14/common_concerns/1/a` | S08 cc0 a 와 거의 같은 문형(적절한 …와 간격으로 시술하면 오히려 … 과도하게 자주 받지 않는 것이 중요) — 다른 카테고리 간 반복 문형. 병합하지 않는다 |
| S15-O3 | B | `/categories/14/how_it_works` | AHA·BHA·TCA 풀이·농도 미기재 · 전문 기기 이름 미기재 |
| S15-O4 | B | `/categories/14/common_concerns/2/a` | 「효과와 안전성 모두 높아요」 근거 미기재 |
| S15-O5 | P | `/categories/14/duration_simple` | 「가벼운」은 정도, 「깊은」은 깊이 수식으로 필링 종류를 가른다 — 정도/깊이 축 혼재(잠정) |
| S16-O1 | P | `/categories/15/common_concerns/0/a` | 질문(미백)에 근거 부족·허가 외·위험 목록으로 답한다. 「드물게」는 중증 피부반응에, 「고용량 시」는 간·신장 부담에 붙은 것으로 읽힘(잠정) — 알레르기·아나필락시스에는 빈도 수식 없음. 임상적으로 승인하지 않는다 |
| S16-O2 | B | `/categories/15/common_concerns/0/a` | 「고용량」 기준 · 각 위험 빈도 수치 · 아나필락시스 응급 징후·대처 미기재 |
| S16-O3 | P | `/categories/15/how_it_works` | how_it_works 와 cc2 a 가 같은 근거 제한 문장(결핍이 없는 경우 경구 섭취보다 … 근거는 제한적)을 반복 |
| S16-O4 | B | `/categories/15/duration_simple` | 무엇이 1-2주 지속되는지(효과) 생략 · 「정기적」 간격은 cc1 a 에 「주 1-2회 또는 격주 1회」 |
| S17-O1 | P | `/categories/16/common_concerns/1/a` | 규제 서술(국내·허가·적응증)이 들어 있다. 시점·출처 미기재 — 현재 유효성은 외부 확인 대상이며 여기서 승인·보충하지 않는다(B) |
| S17-O2 | P | `/categories/16/common_concerns/2/a` | 조합 질문에 「함께 사용하는 경우가 있습니다」(현황) + 위험 + 「의사와 상담」으로 답한다. 동시 가능·보완 효과·순서를 단정하지 않는다. 선후 표현 「MTS(미세침)나 레이저 시술 후」는 조합의 시점 |
| S17-O3 | F | `/categories/16/common_concerns/2/a` | 「MTS(미세침)」「레이저」는 S12(M12)·S08(M8) 참조로 보이며 「앞서 안내드린 미허가 주사」는 같은 카테고리 cc1 a 참조. 연결은 후속 |
| S17-O4 | B | `/categories/16/common_concerns/2/a` | 「보고된 사례」 출처·빈도 미기재 · 「검증된 제품」 기준 미기재 |
| S17-O5 | P | `/categories/16/how_it_works` | how_it_works 는 「도포하거나 주사합니다」로 주사를 일반 방법으로 기술하나, cc1 a 는 주사 사용이 허가 적응증이 아니라고 기술 — 같은 카테고리 안 서술 긴장(I 후보). 임상·규제 판단은 하지 않는다 |

## K — 알려진 형태소 오분절 (출현별, 교정하지 않음)

| # | Pointer | 원문 표면 | 값 내 구간 | 원시 토큰 | 영향 |
|---|---|---|---|---|---|
| K1 | `/categories/3/common_concerns/1/q` | 리쥬란 | [0,3) | 리쥬/NNG 란/JX | 제품명이 「리쥬」+조사 「란」으로 분해 — 토큰 기준 제품명 검색 누락. 같은 카테고리 a 의 「리쥬란은」은 정상(출현별 불일치) |
| K2 | `/categories/8/common_concerns/0/q` | 써마지은 | [5,9) | 써마지/NNG 이/VCP 은/EC | 원문 조사 표기 이상(「써마지은」)으로 길이0 VCP와 연결어미 EC 생성 — 화제 조사 소실·가짜 서술격 |
| K3 | `/categories/8/common_concerns/0/a` | 써마지은 | [32,36) | 써마지은/NNG | 조사가 명사에 흡수된 미등록 명사 — 제품명 토큰 「써마지」 검색 누락 |
| K4 | `/categories/8/common_concerns/0/a` | 울쎄라는 | [0,4) | 울쎄/NNP 이/VCP 라는/ETM | 제품명이 「울쎄」로 잘리고 화제 조사 「는」이 인용형 「라는」으로 오인 — 제품명 손상·가짜 인용 구조 |
| K5 | `/categories/8/simple_explanation` | 초음파 | [0,3) | 초/XPN 음파/NNG | 「초음파」가 접두사+명사로 분해 — 에너지 종류 토큰 검색 시 「음파」로만 남음 |
| K6 | `/categories/8/how_it_works` | 초음파 | [13,16) | 초/XPN 음파/NNG | 「초음파」가 접두사+명사로 분해 — 에너지 종류 토큰 검색 시 「음파」로만 남음 |
| K7 | `/categories/8/common_concerns/0/a` | 초음파 | [5,8) | 초/XPN 음파/NNG | 「초음파」가 접두사+명사로 분해 — 에너지 종류 토큰 검색 시 「음파」로만 남음 |
| K8 | `/categories/8/simple_explanation` | 고주파 | [5,8) | 고/XPN 주파/NNG | 「고주파」가 접두사+명사로 분해 — 「고」가 정도(높음) 접두로 읽힐 위험·에너지 종류 토큰 누락 |
| K9 | `/categories/8/how_it_works` | 고주파 | [20,23) | 고/XPN 주파/NNG | 「고주파」가 접두사+명사로 분해 — 「고」가 정도(높음) 접두로 읽힐 위험·에너지 종류 토큰 누락 |
| K10 | `/categories/8/common_concerns/0/a` | 고주파 | [37,40) | 고/XPN 주파/NNG | 「고주파」가 접두사+명사로 분해 — 「고」가 정도(높음) 접두로 읽힐 위험·에너지 종류 토큰 누락 |
| K11 | `/categories/9/how_it_works` | 고주파 | [37,40) | 고/XPN 주파/NNG | 「고주파」가 접두사+명사로 분해 — 「고」가 정도(높음) 접두로 읽힐 위험·에너지 종류 토큰 누락 |
| K12 | `/categories/10/patient_name` | 고주파 | [5,8) | 고/XPN 주파/NNG | 「고주파」가 접두사+명사로 분해 — 「고」가 정도(높음) 접두로 읽힐 위험·에너지 종류 토큰 누락 |
| K13 | `/categories/10/simple_explanation` | 고주파 | [28,31) | 고/XPN 주파/NNG | 「고주파」가 접두사+명사로 분해 — 「고」가 정도(높음) 접두로 읽힐 위험·에너지 종류 토큰 누락 |
| K14 | `/categories/10/how_it_works` | 고주파 | [28,31) | 고/XPN 주파/NNG | 「고주파」가 접두사+명사로 분해 — 「고」가 정도(높음) 접두로 읽힐 위험·에너지 종류 토큰 누락 |
| K15 | `/categories/14/patient_name` | 필링 | [11,13) | 필/NNG 링/NNG | 「필링」이 「필」+「링」으로 분해(같은 카테고리 다른 출현은 「필링/NNG」) — 시술명 토큰 불일치 |
| K16 | `/categories/14/simple_explanation` | 필링 | [24,26) | 필/NNP 링/NNG | 「필링」이 「필」+「링」으로 분해(같은 카테고리 다른 출현은 「필링/NNG」) — 시술명 토큰 불일치 |
| K17 | `/categories/14/common_concerns/2/q` | 필링 | [7,9) | 필/NNP 링/NNG | 「필링」이 「필」+「링」으로 분해(같은 카테고리 다른 출현은 「필링/NNG」) — 시술명 토큰 불일치 |
| K18 | `/categories/15/how_it_works` | 혈중 | [70,72) | 혈/NNG 중/NNB | 「혈중」이 「혈」+의존명사 「중」으로 분해 — 「중」이 시간(~하는 중) 표현으로 오탐될 위험. 같은 카테고리 cc2 a 의 「혈중으로」는 정상 |
| K19 | `/categories/15/common_concerns/1/a` | 격주 | [26,28) | 격/NNG 주/NNG | 빈도 표현 「격주」가 「격」+「주」로 분해 — 주기 해석 시 「주」(week) 단독으로 오탐 위험 |
| K20 | `/categories/15/common_concerns/2/a` | 정맥염 | [66,69) | 정맥/NNG 염/NNG | 부작용명 「정맥염」이 「정맥」+「염」으로 분해 — 사건명 토큰 누락·부위 「정맥」 오탐 위험 |
| K21 | `/categories/11/common_concerns/0/q` | 더마롤러 | [4,8) | 더/MAG 마/MAG 롤러/NNG | 기구명 「더마롤러」에서 「더」가 비교 부사로 분석 — 비교 표현 오탐·기구명 누락 |
| K22 | `/categories/13/common_concerns/0/a` | 요요 | [51,53) | 요/MM 요/MM | 「요요」(체중 재증가)가 관형사 두 개로 분석 — 명사 소실 |
| K23 | `/categories/8/downtime` | 붉은기와 | [12,16) | 붉/VA 은/ETM 기와/NNG | 「붉은기와 붓기」의 「기」+조사 「와」가 명사 「기와」로 묶임 — 부작용 「붉은기」 소실·무관 명사 생성 |
| K24 | `/categories/9/common_concerns/0/a` | 박동기 | [3,6) | 박동/NNG 기/XSN | 기기명 「심장 박동기」의 「기」가 접미사 처리 — 경미(기기명 토큰 분해) |
| K25 | `/categories/11/how_it_works` | 바른 | [77,79) | 바르/VA ᆫ/ETM | 「바른 약물」의 바르다(도포·VV)가 형용사 VA(옳다)로 태깅 — lemma 「바르다」는 같으나 품사로 의미가 바뀜. 도포 행위 탐색 누락·「옳은 약물」 오해 위험 |

## 보조 정규식 후보 중 수동 구절로 덮이지 않은 것

정규식 후보 572건 중 문장 아닌 수동 구절에 포함되지 않은 것 49건(문장 기록까지 포함하면 미포함 0건). 판정은 manual/regex-review.json.

| ID | 종류 | Pointer | 일치 | 판정 | 메모 |
|---|---|---|---|---|---|
| R0001 | negation | `/categories/0/how_it_works` | 않 | covered_by_sentence_only | 문장 기록 칼로 자르거나 꿰매지 않아요. 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0009 | condition | `/categories/0/common_concerns/0/q` | 맞으면 | covered_by_sentence_only | 문장 기록 보톡스 맞으면 표정이 굳나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0010 | possibility | `/categories/0/common_concerns/0/a` | 수 있 | covered_by_sentence_only | 문장 기록 적절한 양을 맞으면 자연스러운 표정을 유지할 수 있어요. 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0051 | possibility | `/categories/1/common_concerns/0/q` | 수 있 | covered_by_sentence_only | 문장 기록 필러가 뭉치거나 울퉁불퉁해질 수 있나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0062 | possibility | `/categories/1/common_concerns/2/q` | 수 있 | covered_by_sentence_only | 문장 기록 필러 맞다가 혈관에 문제가 생길 수 있나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0068 | instruction | `/categories/1/common_concerns/2/a` | 중요합니다 | covered_by_sentence_only | 문장 기록 응급 대처가 가능한 병원에서 시술받는 것이 중요합니다. 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0072 | condition | `/categories/2/how_it_works` | 하면 | covered_by_sentence_only | 문장 기록 특수 성분을 피부 아래에 주사하면, 우리 몸이 그 주변에 새로운 콜라겐을 만들어냅니다. 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0086 | time_rel | `/categories/2/common_concerns/0/q` | 바로 | covered_by_sentence_only | 문장 기록 효과가 바로 보이나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0095 | possibility | `/categories/2/common_concerns/1/q` | 수 있 | covered_by_sentence_only | 문장 기록 결절(딱딱한 덩어리)이 생길 수 있나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0100 | condition | `/categories/2/common_concerns/1/a` | 더라도 | covered_by_sentence_only | 문장 기록 하시더라도 세게 하지 말고 부드럽게 하세요. 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0102 | instruction | `/categories/2/common_concerns/1/a` | 하세요 | covered_by_sentence_only | 문장 기록 하시더라도 세게 하지 말고 부드럽게 하세요. 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0106 | manner_speed | `/categories/2/common_concerns/1/a` | 부드럽게 | covered_by_sentence_only | 문장 기록 하시더라도 세게 하지 말고 부드럽게 하세요. 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0143 | condition | `/categories/4/how_it_works` | 하면 | covered_by_sentence_only | 문장 기록 이 농축액을 피부에 주사하면 성장인자가 피부 재생과 콜라겐 생성을 촉진합니다. 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0156 | negation | `/categories/4/common_concerns/0/q` | 없 | covered_by_sentence_only | 문장 기록 내 피를 쓰니까 부작용이 없나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0157 | possibility | `/categories/4/common_concerns/0/a` | 수 있 | covered_by_sentence_only | 문장 기록 다만 주사 부위에 일시적 붓기나 멍은 있을 수 있어요. 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0164 | time_rel | `/categories/4/common_concerns/2/q` | 바로 | covered_by_sentence_only | 문장 기록 효과가 바로 나타나나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0189 | negation | `/categories/5/common_concerns/0/q` | 않 | covered_by_sentence_only | 문장 기록 지방이 다 흡수되지는 않나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0194 | negation | `/categories/5/common_concerns/1/q` | 않 | covered_by_sentence_only | 문장 기록 지방 뽑는 부위가 움푹 꺼지지 않나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0196 | condition | `/categories/5/common_concerns/2/q` | 찌면 | covered_by_sentence_only | 문장 기록 살이 찌면 넣은 지방도 커지나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0215 | negation | `/categories/6/common_concerns/0/a` | 않 | covered_by_sentence_only | 문장 기록 제대로 시술하면 만져지지 않아요. 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0220 | condition | `/categories/6/common_concerns/1/q` | 녹으면 | covered_by_sentence_only | 문장 기록 실이 녹으면 다시 처지나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0221 | condition | `/categories/6/common_concerns/1/q` | 시  | false_positive | 「다시」의 일부 — 조건 아님 |
| R0227 | negation | `/categories/6/common_concerns/2/q` | 않 | covered_by_sentence_only | 문장 기록 실리프팅 후 표정이 어색하지 않나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0228 | time_rel | `/categories/6/common_concerns/2/q` | 후 | covered_by_sentence_only | 문장 기록 실리프팅 후 표정이 어색하지 않나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0231 | negation | `/categories/6/common_concerns/2/a` | 없 | covered_by_sentence_only | 문장 기록 일상 표정에는 영향이 없어요. 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0238 | condition | `/categories/7/duration_simple` | 따라 | covered_by_sentence_only | 문장 기록 시술 종류와 목적에 따라 다릅니다. 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0239 | instruction | `/categories/7/duration_simple` | 필요합니다 | covered_by_sentence_only | 문장 기록 토닝은 주 1회씩 여러 차례, 색소 제거는 수회 반복이 필요합니다. 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0248 | condition | `/categories/7/common_concerns/0/q` | 맞으면 | covered_by_sentence_only | 문장 기록 레이저 맞으면 피부가 얇아지나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0257 | possibility | `/categories/7/common_concerns/1/q` | 수 있 | covered_by_sentence_only | 문장 기록 레이저 후 색소침착이 생길 수 있나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0258 | time_rel | `/categories/7/common_concerns/1/q` | 후 | covered_by_sentence_only | 문장 기록 레이저 후 색소침착이 생길 수 있나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0262 | possibility | `/categories/7/common_concerns/1/a` | 수 있 | covered_by_sentence_only | 문장 기록 일시적으로 생길 수 있어요. 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0267 | possibility | `/categories/7/common_concerns/2/a` | 수 있 | covered_by_sentence_only | 문장 기록 레이저로 개선할 수 있지만 재발 관리가 중요해요. 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0273 | condition | `/categories/8/how_it_works` | 하면 | false_positive | 「수축하면서」 — 동시·연결 어미, 조건 아님 |
| R0290 | comparison | `/categories/8/common_concerns/1/q` | 만큼 | covered_by_sentence_only | 문장 기록 기기 리프팅이 수술만큼 효과 있나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0307 | negation | `/categories/9/common_concerns/0/q` | 않 | covered_by_sentence_only | 문장 기록 전기 자극이 위험하지 않나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0312 | time_rel | `/categories/9/common_concerns/1/q` | 바로 | covered_by_sentence_only | 문장 기록 효과가 바로 느껴지나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0348 | condition | `/categories/10/common_concerns/0/a` | 되면 | false_positive | 「재생되면서」 — 연결 어미, 조건 아님 |
| R0354 | time_rel | `/categories/10/common_concerns/2/q` | 중  | false_positive | 「레이저 중 뭐가」 — 선택 범위, 시간 아님 |
| R0355 | condition | `/categories/10/common_concerns/2/a` | 따라 | covered_by_sentence_only | 문장 기록 피부 상태와 목표에 따라 의사가 더 적합한 시술을 추천해드립니다. 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0380 | time_rel | `/categories/11/common_concerns/1/q` | 후 | covered_by_sentence_only | 문장 기록 시술 후 피가 나나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0388 | negation | `/categories/11/common_concerns/2/q` | 없 | covered_by_sentence_only | 문장 기록 감염 위험은 없나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0406 | negation | `/categories/12/common_concerns/0/q` | 않 | covered_by_sentence_only | 문장 기록 플라즈마가 뭔가요? 위험하지 않나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0412 | time_rel | `/categories/12/common_concerns/2/q` | 후 | covered_by_sentence_only | 문장 기록 시술 후 딱지가 생기나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0417 | possibility | `/categories/12/common_concerns/2/a` | 수 있 | covered_by_sentence_only | 문장 기록 미세한 점 형태의 가피가 생길 수 있어요. 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0422 | negation | `/categories/13/simple_explanation` | 없 | false_positive | 「없애는」 — 동사(제거), 부정 아님 |
| R0438 | condition | `/categories/13/common_concerns/0/a` | 따라 | false_positive | 「따라서」 — 접속 부사, 조건 아님 |
| R0467 | condition | `/categories/14/duration_simple` | 따라 | covered_by_sentence_only | 문장 기록 시술 종류에 따라 다릅니다. 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0481 | time_rel | `/categories/14/common_concerns/0/q` | 후 | covered_by_sentence_only | 문장 기록 필링 후 피부가 벗겨지는 게 정상인가요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
| R0521 | frequency | `/categories/15/common_concerns/1/q` | 자주 | covered_by_sentence_only | 문장 기록 얼마나 자주 맞아야 하나요? 안에 있음 — 짧은 단문으로 단서가 문장 전체에 걸려 있어 별도 구절로 분리하지 않음(직접 확인) |
