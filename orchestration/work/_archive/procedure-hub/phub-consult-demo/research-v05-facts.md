# research-v05-facts — SPEC-010 0.2.2 WP-0 실측 (app 워커 · 2026-11-20)

발주 `task_52860720a63e` · `ctx_aa28d030b303`. 코드 0 · 커밋 0 · 18222 손 안 댐 · 허브 18105 GET 만.
기준: 매핑 JSON v3 `94b88022…`(앱 `data/kos/` · 메인 로컬 두 경로 sha 같음) · 허브 gold `57b420ad…`(aux `51e3760a…` · `/health` `build.gold_hash` = `$J` `meta.hub_gold_hash` → JS4 불일치 0) · 앱 HEAD `97d964e`.
셈 스크립트는 워커 scratchpad 의 일회용(`hub.py` 쪽 넘김 · `jidx.py` 색인 · `cc.py` 고민 길 · `ax.py` 축)이고 레포에 넣지 않았다.

## 0. 한눈에

- 실측 항목 **13**(WP-0 목록 9: 1 · 2(닫힘 — 다시 안 셈) · 2b · 2c · 3 · 4 · 5 · 6 · 7 + AX7 기대값 고정 1 + 검수 r5 P2 3).
- 스펙과 다른 점 **19**(§2 표). 그중 착수 전에 코디 판단이 필요한 것 **4**: **N1**(이해 호출이 효과 · 케이스 · 국가를 못 냄) · **N2**(효과 길 폭 · 물려받음 없음 · package) · **N3**(경과 줄 · 빈 효과 코드) · **N12**(빈 slot 을 JSON 에 못 둠).
- 0.4 관련 시험 17 파일 기준선 **123 passed**(손대기 전 · 8.9 초).

## 1. 실측 표

| # | 무엇을 | 어떻게(호출 · 셈) | 결과(값 · 수) | 스펙과 다른 점 |
|---|---|---|---|---|
| 1 | 허브 `facets` profile · outcome · adverse 를 `procedure_case` 노드로 부를 때 칸 · role(케이스 셋) | `GET /facets?node=procedure_case:<CAS>&facet=<f>` read_all · 표본 CAS-064(케이스 1) · CAS-060(여럿 진료항목 BBL 1 모드) · CAS-001(보톡스 이마) | **profile** 3 행 = 자기(케이스 행) 1 + 물려받음 2(시술 행 · 계열 행) · 칸 29(`overview` · `mechanism_code` · `mechanism_name` · `mechanism_text` · `methods` · `procedure_code` … · `layer{role, path, holder{holder_table, holder_code}}`) · 케이스 행의 `overview` · `mechanism_text` 는 비고, **물려받은 시술 행에 `overview` · `mechanism_code` · `mechanism_text` 가 들어 있다**. **outcome** CAS-064 8(계열 물려받음 8) · CAS-060 12(시술 4 + 계열 8) · CAS-001 17(시술 8 + 계열 9) · 칸 = `effect_code` · `effect_name` · `note` · `site_name` · onset/peak/duration 15 · `target_*` · `layer`. **adverse** 28 · 39 · 67(CAS-001 만 자기 1) · 칸 = `adverse_code` · `adverse_name` · `severity_text` · `polarity` · freq 10 · `note` · `layer`. 쪽 넘김 = 전부 1 쪽. 명동점 케이스 137 전수: outcome 1750 행 = 계열 1054 · 시술 655 · 케이스 자기 41 · **`effect_code` 빈 행 455(26 %)** | N3 · N4 · N5 · N6 |
| 2 | 방법 코드 · 방법 글이 허브에 있나 | — | 닫힘(D-12 · WP-H). 덤: `facets?node=product:<PRD>&facet=profile` 제품 행에 `country` 칸 없음(WH7 아직) | 0 |
| 2b | 효과 칸 길(O-8) | `facets?node=effect:EFF-010` · `EFF-049` `facet=outcome` read_all(limit 100 · 20 둘 다) · 표마다 `$J` 색인 · 계열은 `scope?node=modality:` 의 `holder_table = procedure` → `by_proc` | **리프팅 EFF-010 = 70 행**(limit 20 이면 4 쪽 · 합 70) · 표 = product 46 · procedure 15 · modality 5(M1 · M7 · M10 · M11) · procedure_case 2 · **package 2**(PKG-0116 올타이트 · PKG-0069). **미백 EFF-049 = 14 행** = procedure 7 · modality 3(M11 · M16 · M17) · product 2 · procedure_case 1 · **package 1**. **행에 `layer` 가 없다(자기 · 물려받음 구분 0) · `roles=물려받음` 으로 불러도 같은 70 행** — 효과 속성 행 자체만 돌려주고, 물려받음 펼치기는 앱 몫. 진료항목: 리프팅 = 케이스 10 · 시술 130 · 제품 44 · 계열(scope) 110 → **합 141**(CZ1 뒤 141 · 324 의 44 %) · 미백 = 시술 4 · 계열 14 → **14** | N2 |
| 2c | `pair` 응답 꼴 | `pair?a=procedure:<PRC>&b=procedure:<PRC>` · 명동점 시술 위 14 개 쌍 91 개 전수 | `a=PRC-001`(맨 코드) = 422 `a 는 표:코드 꼴이어야 한다` 재확인. 응답 머리 = `total` · `next_cursor` · `counts{by_class, same_day, conflict}` · `same_day_packages[]` · `ledger_check[]` · 행 칸 = `from_*` · `to_*` · `kind` · `question_class` · `level_text` · `interval_*` · `order` · `same_day` · `same_day_text` · `text` · `goal_effects` · `conflict_id` · `a_side` · `a_layer` · `b_layer`. 표본 ① **같은 날 가능** PRC-001 보톡스 × PRC-007 근적외선 = 7 행(간격 3 · 보완 3 · 순서 1 · same_day 가능 2 · 조건부 4) ② **정보 없음** PRC-001 × PRC-123(세라핏 지방분해) = 0 행. 91 쌍 최대 22 행 → 전부 1 쪽. `question_class` 값 9 종(간격 · 보완 · 순서 · 회피 · 대안 · 재시술 간격 · 이전 시술 확인 · 관련 기법 · 비교) · `same_day` 값 4(가능 · 조건부 · 불가 · 빈칸). **같은 시술 쌍**(PRC-001 × PRC-001)도 16 행(재시술 간격 14 · 이전 시술 확인 2) | N10 |
| 3 | `scope` 로 계열 → 시술 · 제품 → 하위 제품 · 쪽 넘김 | `scope?node=modality:M8` · `M2` · `M18` · `product:PRD-416` · `PRD-417` · `PRD-001` read_all(목록 칸 이름 = `holders`) | M8 = **146**(2 쪽 · 자기 1 · 하위 시술 7 · 하위 제품 60 · 하위 케이스 78) · M2 필러 64 · M18 지방분해 36(1 쪽). 제품: PRD-416 써마지 → role **「하위 제품」** PRD-417 써마지FLX(+ 물려받음 3 = 케이스 · 시술 · 계열) · PRD-417 → role **「상위 제품」** PRD-416 · PRD-001 보톡스 = 물려받음 23 · 하위 0. 「보톡스」 계열 M1 의 시술 = PRC-001 하나 → 진료항목 106(시술 길과 같은 수) | N9(AX3 role 이름) |
| 4 | `concern-candidates` reach 분포 · 「케이스 직접」 행 · `unreached[]` 꼴 | `concern-candidates?concern_code=<CON>&upper=auto&to_procedure=none` read_all(목록 = `groups`) · 행 `reach == 「케이스 직접」` 의 `candidate_code` → `by_case` − CZ1. `to_procedure=auto` 도 같이 셈 | **팔자주름 CON-009**: groups 88 = 케이스 직접 포함 **25** · 제품 경유만 **63**(스펙과 같음) · 행 264 = 제품 경유 239 · 케이스 직접 25 · 진료항목 직접 **23** · 전부 받으면 **168** · `unreached` 2(행 꼴 = `reach` 「제품 — 케이스 없음」 · `candidate_table = product` · PRD-251 테스리프트 등). 23 안에 다한증 · 승모근 · 종아리 · 침샘보톡스 0 · 써마지 FLX 3 · 슈링크 유니버스 4 든다(E1 그대로). **턱살 CON-168** = 3 묶음 · 진료항목 **5**. **기미 CON-068** = 84 묶음(직접 36) · 진료항목 **27**(전부 55). **다한증 CON-252** = 30 묶음(직접 5) · 진료항목 **15**. **CON-001 주름** = **173 묶음 · 2 쪽**(> 100) · 직접 134 · 진료항목 144. 묶음 `candidate_table` 은 전부 procedure_case · `inherited_from` 은 다섯 다 null. `to_procedure` none / auto 결과 같음(auto 만 `counts.descended` 칸이 참) | 0 |
| 5 | 그림 시드 폴더 · IM1 · silver `concept_image` 대조 · 명동점 빠짐 | 폴더 나열 · 정규식 `^MEC-\d{3}\.svg$` · `^MET-\d{3}\.svg$` · silver `concept_image.csv` 121 행 `svg_path` · `sha256` 대조 · 명동점 시술 43 의 profile `mechanism_code` · 케이스 137 의 silver `case_method` | 폴더 전체 원리 97 · 방법 107 · **정규식 맞는 파일 55 · 66**(나머지 = `MEC-001__botulinum-toxin.svg` 꼴 사본 · 표와 접두어 섞임 0 · 심볼릭 링크 0). silver 121 행 `svg_path` 전부 `images/<표>/<코드>.svg` 꼴 · 파일 있음 121 · **sha256 전부 같음** · 폴더에만 있는 정규식 파일 0. 명동점: 원리 코드 27 종 빠짐 0 · 방법 코드 26 종 빠짐 0 · 케이스 137 전부 방법 있음(1 개 132 · 2 개 5). **시술 PRC-020(태반주사 `26-SJS-TBJS` 하나)은 `mechanism_code` 빈칸** → IM9(원리 figure 숨김). silver `method.csv` 66 · 설명에 「·」 28 · 줄바꿈 0(WH2 근거 그대로) | 0(PRC-020 은 IM9 대로) |
| 6 | 시안 CSS ↔ 0.4 `consult.css` 클래스 겹침 | 시안 `<style>` 전부(줄 1 = 한 줄 기본 덩이 · 3 ~ 161 · 162 ~ 446)와 `static/consult.css` 의 `.cs-*` · `.ms-*` 클래스 · 선택자 · 선언 비교 | 시안 클래스 229(cs 159 · ms 70) · 0.4 consult.css 90 · **겹침 90(0.4 클래스 전부가 시안에 있음) · 시안에만 139 · 0.4 에만 0**. 시안 ms 70 개는 전부 0.4 `medikit.css` 에 있다. 선택자 겹침 134(0.4 전부) · 선언이 다른 것 5 = `:root` · `body` · `@font-face`(시안이 medikit 바탕 · 글꼴을 인라인) · `.cs-chat`(시안이 `position: relative` 더함) · `@keyframes … to`. 시안에만 있는 cs 클래스 = `cs-cart*` 18 · `cs-kind*` 6 · `cs-kinds*` 2 · `cs-pcard*` 7 · `cs-pm*` 13 · `cs-rec*` 4 · `cs-sk*` 5 · `cs-top*` 7 · `cs-fig*` 3 · `cs-right` · `cs-dot--pick` · `cs-dot__ring`(§4-1 목록과 같음 · `cs-right` 하나 더) | 0 |
| 7 | 매핑 JSON v3 꼴 ↔ §3-1 · JS2 | `$J` 전수 | `meta.version = v3` · items **324**(코드 유일) · status 295 / 13 / 8 / 6 / 2 · 케이스 1 개 이상 305(여럿 37) · 0 개 19(허브 대상 아님 13 · 시술 확인 필요 6) · 서로 다른 케이스 137 · 시술 43 · `kos_status` 324 PUBLISHED · 약물 「해당 없음」 127 · 기기 216 · note = 매핑됨 아닌 29 전부. products **150** · 이벤트 상품 64 · 옵션 **493** = single 456 · group 37 · `event_price` 있는 옵션 67 · 키 유일. `option_refs` 551 = `covers` 551(양쪽 같은 집합 · 어긋남 0) · 깨진 ref 0 · 깨진 covers 0 · option_refs 0 개 24 · 1 개 174 · **2 개 이상 126(2 ~ 5 = 118 · 6 ~ 8 = 8 · 최대 8)**. single 0 진료항목 36 = 옵션 0 **24** + group 만 **12**. 판매 종료 = **상품 P131 「크라이오 (copy)」 하나뿐**(옵션 `closed` 는 493 전부 null) → 26-KEUR 의 single 4 가 2 로 준다. group 37 전부 `count = null` · `compositions` 95 줄(count 1 = 89 · 5 = 4 · 10 = 2 · `covers` = 구성 진료항목 집합 37/37) · **`comp_event_price_is_option_total` 은 구성 줄 칸**(true 29 · false 66) · 구성 `unit` UnitType_UNKNOWN **44 / 95**. 「[11월 이벤트] 온다50kj+티타늄30kj」(P015-1) 정가 1,100,000 · 이벤트가 590,000 · 구성 둘 이벤트가 590000 반복 · 표지 true(D-17 그대로). sites 71 = 얼굴 32(point 15 · pair 17 · 빈 points 0) · 몸 39 list · 뿌리 SITE-001 전신 · SITE-007 얼굴 · SITE-147 몸(부모 SITE-001) · 목 SITE-079 부모 SITE-147 · `site_codes` 가 sites 에 없는 것 0. groups 131(진료항목 324 를 한 번씩) · 이름 중복 23 이름 66 항목 · KOS 시술 이름 = 진료항목 이름 25 · `site_scope` 7 종(특정 부위 154 · 얼굴 전체 109 · 몸 16 · 부위 개념 없음 16 · 어디든 11 · 얼굴 · 몸 가능 9 · 얼굴 일부 9). RT1 코드 여섯 전부 `$J` 에 있음. C9 표본 26-Avalanche-1(아발란체 제모 겨드랑이) single 4 = 남성 1 회 70,000 · 5 회 200,000 · 여성 1 회 50,000 · 5 회 150,000. C9c 26-THM3-600SHOT single 4(가입비 0 · 블랙 490,000 · 플래티넘 890,000 · 정가 2,200,000) + group 4 | N7 · N8 |
| AX7 | 다음 질문 축 표본 셋 기대값(시험이 이 값으로 판정) | AX3 대로 축 값: 부위 = `site_codes` 를 SITE-007 / SITE-147 바로 아래로 올림(SITE-007 · 001 · 147 자체는 그대로) · 고민 = 케이스 `facets indication` 의 `layer.role = 자기` ∧ `reach = 케이스 직접` 의 `concern_code` · 효과 = 케이스 `facets outcome` 의 `effect_code`(**빈 코드 뺌**) · 제품 = `hub.products` 를 scope role 「상위 제품」 으로 끝까지 올림. 점수 = 가장 큰 묶음 수 · 값 있는 묶음 < 2 또는 「없음」 > L/2 빼기 · 이미 값 있는 칸 빼기(AX2) | **① 팔자주름(고민 칸 참) L = 23** → 부위 23(SITE-007 23 · SITE-001 7) · 효과 23 · 제품 **5** → **축 = 제품 · 가장 큰 묶음 5**(PRD-435 소프웨이브 5 · PRD-402 5 · PRD-400 5 · PRD-150 4 · PRD-416 써마지 3 — 묶음 6) · 허브 호출 = 케이스 6 × 2 = 12. **② 「보톡스」(시술 칸 참 · M1 = PRC-001) L = 106** → 부위 **21**(SITE-072 턱 21 · SITE-007 16 · SITE-057 입 12 · … 묶음 16) · 고민 71 · 효과 106 · 제품 33(하이톡스 33 · 제오민 26 · 코어톡스 24 · 보톡스 23) → **축 = 부위 · 가장 큰 묶음 21**. 케이스 24 × 2 = **48 호출 > 40(AX6)** → 첫 턴(캐시 없음)엔 고민 · 효과 축이 빠지지만 답은 같다(부위 21). **③ 4 개 이하** 표본 = 「LDM」 KOS 시술 묶음 3 → 축 0 | N11 · N13 · N14 |
| r5-1 | e2e C3 옛 글(§9-2 줄 645) | C3 쌍 다시 셈 | 다한증 CON-252 직접 진료항목 **15**(다한증보톡스 겨드랑이 · 발 · 손 × 4 브랜드 · 하이톡스 · 바디보톡스 둘) ∩ 써마지 PRD-416 + 하위 PRD-417 진료항목 **5**(써마지 FLX 3 · 아이 써마지 2) = **0**. C4 도 같은 쌍으로 성립 | §9-2 「C3 『주름』 + 『종아리』」 → 「C3 『다한증』 → 『써마지로』」 |
| r5-2 | WP-5 시험 줄 옛 덮개 0 경우(§9-1 줄 623 ② ③) | v3 셈 | single 0 진료항목 = 옵션 0 **24** + group 만 **12**(OP5 단추 없음 · RC6 가격 없음). 판매 종료는 상품 단위 하나(P131 — 26-KEUR 의 single 1 회 · 5 회 사본 둘)뿐이라, RC10 「고른 옵션이 판매 종료가 되면 옵션 안 고름」 시험은 **작은 `$J` 고정본에서 `closed` 를 바꿔** 만든다(실물엔 「고른 뒤 종료」 경우 0). ① 「group count null」 은 37/37 이라 예외가 아니라 늘 그렇다 | ② → 「group 만 12 → OP5 단추 없음 · RC6 가격 없음」 · ③ → 「고른 옵션이 종료(고정본) → 옵션 안 고름(RC10)」 · ① → 「group 옵션 `count` 는 늘 null — 구성 `compositions[].count` 로 덮음(RC2 ③)」 |
| r5-3 | CO 겹침 | RC4 쓰인 가격 · 상품 제목 · 카테고리 C16 「10월 첫방문 이벤트」 | **CO1 13 · CO2 22 · CO3 23** · CO1 ∩ CO2 **10**(전부 `[DB 블랙 1년권] 가입비` P024 의 0 원 혜택 옵션 — 수액 무제한 7 · 써마지 600샷 · 울쎄라 600샷 · 혈액 줄기세포 2 회) · **합집합 25** · CO1 만 3(머미팩 · LED 재생레이저 · 시트팩) · CO3 은 CO1 · CO2 와 겹침 0 · 걸린 옵션 전부 single. P024 의 11 번째 옵션(가입비 본체 5,000,000)은 0 원이 아니라 CO2 만 | CO1 줄 「11 은 가입비 혜택」 → **10** · WP-5 완료 조건에 「규칙마다 따로 센다(겹침 10 · 합집합 25)」 |

## 2. 스펙과 다른 점(고칠 방향 — 스펙 고침은 코디)

| # | 스펙 절 | 실측 | 고칠 방향 | 급 |
|---|---|---|---|---|
| N1 | §5-1 ① · §5-0 CD1 · CD6 · E15 · E18 · C5 | 0.4 이해 호출의 목록 = `entry_list.TABLES` 다섯(concern · site · modality · procedure · product)이고 `verify.py:103` 이 그 밖 표를 떨군다 → **effect · procedure_case 는 targets 로 나오지 않는다**(SLOT_OF 아홉은 객체 칸 표일 뿐). pick 출력 꼴에 `country` 칸도 없다. 허브 `resolve` 는 `tables=effect` 136 행(EFF-010 = 「리프팅 · 처짐 개선 · 처짐 교정」) · `procedure_case` 55 행 / 44 코드(명동점 케이스 137 가운데 대부분은 이름 행이 없음) | WP-3 에 넣는다: `TABLES` 에 `effect`(필수 · E15) · `procedure_case`(선택 · E18 은 44 코드만 가능하다고 적기) · pick 규칙 · 출력 꼴에 `country`(CD6) — pick 판 `0.5.0-draft` · 목록 sha 바뀜. 회귀: `test_v04_prompt`(pick 판) · `test_v04_ledger`(pick_version) · `test_v04_verify` · `test_v04_understand` · `test_answer_key` · `test_v04_list` | **높음** |
| N2 | §5-1 ④ 효과 줄 · O-8 | 효과 응답에는 `layer` 가 없고 `roles` 인자가 결과를 안 바꾼다(속성 행만 70) — 「role 기본 자기 · 물려받음」 문구는 이 길에 해당하지 않는다. 표에 **package**(리프팅 2 · 미백 1)가 섞이는데 `$J` 에 package 길이 없다. 리프팅 = **141 진료항목**(계열 M1 보톡스 「눈썹 올리기」 한 행이 보톡스 106 을 통째로 끌어옴 · 행 `site_name` 「눈썹」 은 안 봄) | O-8 에 「물려받음 펼치기는 앱(계열 → scope 시술 · 시술 → by_proc 가 케이스 전부 포함)」 · 「package 행은 버리고 장부 `items.dropped_reach.package`」 를 적는다. 141 의 넓음(계열 행이 부위 한정 효과를 계열 전체로 퍼뜨림)을 받을지 · 계열 행을 빼거나 `site_name` 으로 거를지는 **코디 · 사용자 판단**(지금 규칙대로면 E15 「리프팅」 의 목록이 324 의 44 %) | **높음** |
| N3 | §4-5 `effect` 목록 · AX3 효과 축 | 케이스 outcome 행의 26 %(455 / 1750)가 **`effect_code` · `effect_name` 빈칸 · onset / peak / duration 만 있는 경과 줄**(예 PRC-001 「2-3일부터 효과 시작 · 약 1개월 완전 · 3-4개월 지속」) | 모달 효과 목록: 빈 `effect_name` 행을 어떻게 보일지 규칙(빼기 / 시안에 없는 「경과」 칸 → slot) · AX3: 빈 코드 행은 축 값에서 뺀다(위 AX7 은 뺀 값) | 중 |
| N4 | §4-5 `side` 목록 | adverse 행 `polarity` 에 「발생함」 밖 값이 있다(CAS-001 67 행 중 「보고 없음」 1 · 「해당 없음」 3) | 부작용 목록에 `polarity = 발생함` 만 둘지 원본 그대로 둘지 한 줄 | 중 |
| N5 | §4-5 `lead` · `mecText` · MD3 캐시 | 케이스 `facets profile` 응답이 물려받은 **시술 행**(`overview` · `mechanism_code` · `mechanism_text`)을 이미 준다 | 시술 profile 따로 부르기(`node=procedure:`) 대신 케이스 응답의 `layer.holder_table = procedure` 행을 써도 된다(호출 수 반) — 선택 | 낮음 |
| N6 | O-6 | CAS-060 outcome 12 = **시술 PRC-006 에서 4 + 계열에서 8**(「전부 PRC-006」 아님) | O-6 문구 고침 | 낮음 |
| N7 | §3-1 `items[].option_refs` | 「2 ~ 5 개 126」 → 실측 2 ~ 8 개 126(2 ~ 5 = 118 · 6 ~ 8 = 8 · 최대 8) | 「2 개 이상 126(최대 8)」 | 낮음 |
| N8 | §6-3 `.cs-sk--short` | 「구성 `unit` 221 중 148 UnitType_UNKNOWN」 → v3 구성 줄 **95 · UNKNOWN 44**(221 / 148 은 삭제 포함 원본 셈으로 보임) | 「95 중 44」 | 낮음 |
| N9 | AX3 제품 축 | 상위 제품은 scope role **「상위 제품」**(물려받음 아님 · PRD-417 → PRD-416) | AX3 에 role 이름을 적는다 | 낮음 |
| N10 | LC9 · R10 | `question_class` 9 종 · `same_day` 4 값 · `conflict` 수가 있다(스펙 「같은 날 · 간격 · 순서 · 피함」 넷보다 많음) · **같은 시술 쌍**(장바구니에 보톡스 진료항목 둘)도 행이 나온다(PRC-001 × PRC-001 = 16) | LC9 에 「행 원본 전부 싣기(분류 거름 0)」 · 같은 시술 쌍(`a = b`)을 부를지 한 줄 | 낮음 |
| N11 | AX6 | 「보톡스」 L 106 = 케이스 24 → indication + outcome 48 호출 > 40 → 첫 턴은 고민 · 효과 축 빠짐(고른 축은 부위로 같음) | 한도 40 을 그대로 두면 WP-3b 리포트 · 시험에 「첫 턴 축 빠짐 표지」 기대를 넣는다 · 또는 시작 때 137 케이스 캐시 미리 채움(274 호출 1 번) | 낮음 |
| N12 | §7-3 · §12 · ST5 | `prompt.py:204 ~ 208` 은 `slots` 값이 비면 `PromptError`(「빈 값 0」) — **빈 slot 을 `prompts/consult.json` 에 둘 수 없다**. 0.4 의 빈 자리 7 도 JSON 이 아니라 템플릿 `data-slot` 속성으로만 있다(JSON `slots` 는 `mark-modality-level` 하나) | 「새 slot 18 은 템플릿 `data-slot` 빈 자리 · 값은 사용자가 채우면 `slots` 키를 더함(없는 키 = 빈칸)」 으로 고침 | 중 |
| N13 | AX5 | 선택지 「묶음 크기 순 앞 5」 의 동점 순서가 없다(팔자주름 제품 5 · 5 · 5) | 동점 = `groups` 순서에서 처음 나온 진료항목 순(또는 코드 순) 한 줄 | 낮음 |
| N14 | AX4 | 값 묶음이 L 전체와 같은 축(팔자주름 부위 23 · 효과 23 · 보톡스 효과 106)은 「가르지 못함」 인데 지금 규칙은 점수로만 밀어낸다 | 「가장 큰 묶음 = L 이면 축 뺌」 한 줄(결과는 같고 장부가 깔끔) — 선택 | 낮음 |
| N15 | NM6 | 「한글 3 글자 이하 26」 → 실측 3 글자 이하 이름 26 = **한글 24 + ASCII 2(PRP · LDM)** | 수 고침 | 낮음 |
| N16 | §9-1 「함께 돌릴 0.4 시험」 | 표에 빠진 회귀 위험 파일: `test_v04_prompt.py`(pick `0.4.0-draft` 단언) · `test_v04_ledger.py`(`pick_version` · `CONSULT_REV == 4`) · `test_v04_verify.py` · `test_v04_understand.py`(TABLES) · `test_v04_turn.py`(`list` · `sites` 이벤트 · `sites.dots`) · `test_answer_key.py` · `test_v04_list.py`(TABLES) | WP-3 · WP-6 줄에 더한다(§3 표) | 중 |
| r5-P2-R1 | §9-2 | 위 r5-1 | 「C3 『다한증』 → 『써마지로』」 | P2 |
| r5-P2-R2 | §9-1 WP-5 줄 | 위 r5-2 | ② ③ 바꿈 · ① 문구 | P2 |
| r5-P2-R3 | CO1 · WP-5 완료 조건 | 위 r5-3 | 11 → 10 · 「규칙마다 따로(겹침 10 · 합집합 25)」 | P2 |

스펙과 **같음**을 확인한 것(고칠 것 0): 팔자주름 23 · 25 / 63 · 168 · 턱살 5 · 기미 27 · CON-001 173 > 100(2 쪽) · M8 146(2 쪽) · 효과 리프팅 70 행 · `pair` 422 · C3 / C4 0 · C9 · C9b(성별 낱말 single 70 전부 상품 제목) · C9c · CO 13 / 22 / 23 · v3 꼴 JS2 전 항목 · §3-1 items / status / 케이스 / 상품 / 옵션 수 · OP5 24 · 12 · 그림 55 · 66 · 빠짐 0 · IM13 · WH2 「·」 28 · 줄바꿈 0 · SF3 SITE-001 · SITE-147 · RT1 코드 여섯 · JS4 해시 같음.

## 3. 0.4 코드 — 재사용 · 손댈 파일 · 회귀 위험

### 3-1. 재사용할 함수(그대로 부름)

| 자리 | 함수 · 상수 | 0.5 에서 |
|---|---|---|
| `clients/hub_rest.py` | `HubRest.read_all(tool, request)` · `call` · `PAGE_LIST`(scope → `holders` · concern_candidates → `groups`) · 도구 이름은 밑줄 꼴(`concern_candidates`) | §5-1 ④ 쪽 넘김 · AX6 · LC9 |
| `consult/plan.py` | `Plan.get` 메모(같은 (도구, 인자) 한 번) · `scope_call` · `indication_call` · `ALLOWED` | §5-2 「0.4 조회가 부른 concern_candidates 다시 씀」 — `ALLOWED` 에 `facets outcome` · `facets profile` 더해야 함 |
| `consult/carry.py` | `candidates` · `with_options` · `alive_in_object` | CD3 이어받기 |
| `consult/state.py` | `SLOT_OF` · `update`(withdraw) · `observe_accepted` · `find` · `snapshot` | CD2 · CD4(거둠 → 칸 지움) |
| `consult/site_filter.py` | `decide` · `prev_ok` | SF1 부위 칸 |
| `consult/blanks.py` | `pick` · `record` · `ledger_view`(0.2 `ask` 꼴) | AX5 질문 하나 |
| `consult/listing.py` | `build_list` · `state_list` · `view_list` | ST2 — 장부 `list` 칸에 계속(지우지 않음) |
| `consult/material.py` | `TurnMaterial` · `renumber` · `message` | LC4 줄 번호 이어감 · LC5 덧붙이기 |
| `consult/prompt.py` | `parse` · `ConsultPrompt.slots` · `keep` / `kept` | §7-3 `kos` 절(키 검사 더함) |
| `consult/ledger.py` | `Ledger.end(conv, row)` · `Conv` · `state_at_start` | 장부 `items` · `conditions` · `cart` · `rec` · `viewed` 줄 |
| `consult/sites.py` · `face_coords.py` | `place` · `all_dots` · `FACE_COORDS` | FS6 `/face-check` 비교용만 |
| `consult/render.py` | `Render(slots=…)` · `_t` · `md` | 새 조각(items · modal · cart · rec) |
| `consult/fake_turn.py` | 가짜 턴 | WP-2 `items` 이벤트 |
| `config.py` | `Settings`(pydantic) | env 여섯(§2-3) 더함 |

### 3-2. 손댈 파일(WP 별)

| WP | 새로 | 고침 |
|---|---|---|
| WP-1 | `consult/kos_map.py` · `tests/test_v05_kos_map.py` | `config.py`(CHAT_KOS_MAP · _SHA · IMAGE_DIR · LLM_ITEMS_MAX · REC_MAX · ASK_LIST_MIN) · `server.py`(시작 때 적재 · JS4) · `ledger.py`(시작 줄 `kos_map`) |
| WP-2 | `templates/partials/{items,pcard,cart,rec,modal}.html` · `tests/test_v05_page.py` | `templates/page.html` · `ui.html` · `partials/main.html` · `static/consult.css`(시안 cs 139 더함 · `.cs-chat` `position: relative`) · `consult.js` · `render.py` · `fake_turn.py` · `server.py`(RT1 라우트 틀) |
| WP-3 | `consult/conditions.py` · `detect.py` · `tests/test_v05_detect.py` | **`entry_list.py` TABLES · `verify.py:103` · `prompts/consult.json` `pick`(effect · country — N1)** · `turn.py`(`Consult._apply` 뒤 조건 칸 · `screen` 의 `list` / `sites` → `items` 이벤트) · `state.py`(필요하면 `conditions` 칸) · `plan.py` `ALLOWED` · `ledger.py` |
| WP-3b | `consult/ask_axis.py` · `tests/test_v05_ask_axis.py` | `blanks.py`(축 · 선택지 연결) · `turn.py` |
| WP-4 | `consult/modal.py` · `images.py` · `tests/test_v05_modal.py` · `test_v05_images.py` | `server.py`(`/c/<id>/item` · `/img/…`) · `render.py` |
| WP-5 | `consult/cart.py` · `price.py` · `tests/test_v05_price.py` · `test_v05_cart.py` | `server.py`(`/c/<id>/cart` · `/cart/save`) · `ledger.py`(`cart` · `cart_saved` · `rec` — 가격 숫자 0) · `consult.js` |
| WP-6 | `tests/test_v05_llm_block.py` | `turn.py`(`Consult.message` 블록) · `material.py` · `prompt.py`(`kos` 절 키) · `prompts/consult.json`(`0.5.0-draft` · `kos`) |
| WP-7 | — | `README.md` 「상담 0.5」 절 |

### 3-3. 0.4 시험 회귀 위험

| 시험 파일 | 걸리는 것 | 언제 |
|---|---|---|
| `test_v04_prompt.py` | `p.pick["version"] == "0.4.0-draft"`(줄 29) · 최상위 `draft` | WP-3(pick 고침) · WP-6(최상위 판 0.5.0-draft) |
| `test_v04_ledger.py` | `pick_version == "0.4.0-draft"`(줄 27) · `CONSULT_REV == 4`(줄 41) · UNDERSTAND_KEYS 집합 | WP-3 · rev 올리면 |
| `test_v04_verify.py` · `test_v04_understand.py` · `test_answer_key.py` · `test_v04_list.py` | `entry_list.TABLES` 다섯 · 목록 sha · 거른 표 | WP-3(N1) |
| `test_v04_turn.py` · `test_consult_turn.py` · `test_v03_sites.py` | SSE `list` · `sites` 이벤트 · `row["sites"]["dots"]` | WP-2 · WP-3(`items` 이벤트가 그 자리에 듦 — 0.4 `list` · `sites` 이벤트를 지우면 깨짐 → 장부 칸은 남기고 이벤트만 바꿀지 정해야 함) |
| `test_consult_page.py` · `test_consult_chat_ui.py` | 페이지 마크업 · `data-slot` 4 곳 · 클래스 집합(`== set(`) | WP-2 |
| `test_consult_material.py` | 재료 줄 번호 · WH6 ④ | WP-6 · WP-H |
| `test_state_blanks.py` | `blanks.pick` 순서 | WP-3b |
| `test_consult_ledger.py` | 턴 줄 칸 | WP-1 · WP-5 |

- 기준선: 위 17 파일(`test_consult_{page,chat_ui,sites,turn,listing,carry,ledger,prompt,material}` · `test_v03_{sites,prompt}` · `test_v04_{list,ledger,verify,understand}` · `test_state_{carry,blanks}`) = **123 passed / 8.9 초**(WP-0 시점 · 손대기 전).
- WP 마다 §9-1 표 + 위 N16 파일을 같이 돌린다.
