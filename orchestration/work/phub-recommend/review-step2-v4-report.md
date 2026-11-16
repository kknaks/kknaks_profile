# 최종 검수 v4 — 실버 2단계 open 해결안 반영

**판정: FAIL** · **open = 0** · pending_director 3 · FAIL 2 · WARN 3 · 회귀 0

끝 조건(open[] = 0 · 남은 것은 원장님 문의 3행뿐)은 **충족한다**. FAIL 은 둘 다 해결안 값 하나씩이다. 「강」으로 매겼는데 인용한 출처가 그 값을 받쳐 주지 않는다. 반영(step2-apply)은 해결안을 그대로 옮겼으므로, 고칠 곳은 `step2-open-resolve.json` 두 행이다.

- 검수자: reviewer(read-only) · 2026-10-28
- 기준
  - 결정 `_RESUME.md` §2 10-28 「하위 계열도 주 · 보조로」(128행) · 「2단계 open 40 해결안 반영」(127행)
  - 해결안 `step2-open-resolve.json` · `.md`
  - 지시 `phub-recommend-step2-final-apply-brief.md`
- v3 기준본 `step2-families.v3.json` = 내가 v3 검수 때 다시 돌린 사본과 md5 `d4b2a45a…` 로 같다. 그래서 v3 시점과 직접 비교했다

---

## FAIL

### F1. 소프라노 티타늄 — 보조 「알렉산드라이트 · 엔디야그」의 인용 출처가 반대로 말함
- ledger `M9-2-4` · `step2-open-resolve.json` rows[소프라노 티타늄] → `step2-families.json` product_family `also_sub_families: ['알렉산드라이트 레이저', '엔디야그 레이저']` · level 강
- 해결안 근거: 「제조사 Alma 는 755 nm (Alexandrite) · 810 nm (Diode) · 1064 nm (Nd:YAG) 로 표기(FDA 510k K222064 정리 https://fda.innolitics.com/device/K222064)」
- 실제 그 페이지(2026-10-28 받음)
  - 「The indications for use for the **755nm Diode Laser Module** …」
  - 「**Soprano Trio diode laser** … Trio applicator emits 1064nm, 810nm, and 755nm wavelengths」
  - 「Alexandrite」 · 「Nd:YAG」 · 「YAG」는 **0회** 나온다
  - 즉 세 파장 모두 다이오드 모듈이다. 허가 품목도 「반도체레이저수술기」 하나다. 매질 2종 근거는 원천 설명의 파장 숫자뿐이다
- 고칠 값: `also_sub_families: []`(주 반도체 레이저 단독). `conflict` 는 「원천 설명이 파장을 매질 이름처럼 씀 — FDA 510k 는 전부 diode」로 고친다. 보조를 남기려면 level 「약」 + 확인 질문으로 내린다

### F2. 울트라V — 보조 「PCL」의 출처가 이 제품 허가가 아님
- ledger `auto-M7-1775364775158` · `also_sub_families: ['PCL']` · level 강
- 해결안 근거: 「같은 업체 수출 허가 20-682 「안면조직고정용실(PCL)」 = 보조」
- step1 `4_license.reference[]` 에서 이 허가는 **「수출용에 한함 — 연결 안 함」**이다(holder 주식회사 울트라브이 · 제조 메타바이오메드). 1단계가 이 제품의 허가로 묶지 않은 것을 「같은 업체」라는 이유로 재질 근거로 썼다 — 추정이다. 주 PDO 는 근거가 있다: 제품명이 든 허가 13-1398 「울트라V」 품목 「폴리디옥사논봉합사」 + 원천 「PDO 전문 리프팅 실」
- 고칠 값: `also_sub_families: []`. 남기려면 level 「약」 + 확인 질문(「쓰는 울트라V 에 PCL 실 라인도 있나요?」)

---

## 브리프 ①~⑦

### ① 37행 = 해결안 값 그대로 — PASS
- 37행 모두 `family` · `also_families` · `sub_family` · `also_sub_families` 가 해결안 `resolve` 와 같다(차이 0)
- 바뀐 행: 하위 바뀜 36 · 트리필 프로는 하위 null 그대로(D05 와 같은 기기 · 하위 없음)
- 새 하위 칸 2: M4 「무세포동종진피(hADM)」(원천 taxonomy M3 하위 `M3-new-1774324237649` label 그대로) · M9 「SUPERB 초음파」
- `conflict` 6행이 해결안과 같다: 실루엣소프트 · 셀렉V · BBL 히어로 · 노블린 · 아포지 엘리트 플러스 · 소프라노 티타늄
- 계열 주 · 보조
  - 이브타이탄 M9 + M10(판단 필요 → 여러)
  - 바이리즌 M4 + M2
  - 트리필 프로 M4(판단 필요 → 옮김)
  - 트리필 프로는 D10 「판단 필요 유지」 위에 결정 127행(해결 값대로)이 올라간 것이다

### ② 근거 약 9행 — PASS
- `evidence_level: "약"` + `confirm_question` 이 9행 모두에 있다: 실루엣소프트 · 압토스 · 에버라인 · 미라클 · 피코코어 · 트루피코 · 디스커버리 피코 · 아이콘 · 아톰
- 판정은 open 이 아니다
- 아이콘 · 디스커버리 피코는 해결안 `ask` 가 null 이라서, 반영 쪽(`ASK_FILL`)이 `why_weak` 를 질문으로 옮겨 적었다(W3)

### ③ pending_director 3 — PASS
- 알렉스필 · 벨르업 · 더마큐어 모두 `family: null` · verdict 「판단 필요」 · `pending_director: true` · open 에 없음
- `pending_director[]` 에 질문 + 「확인되면 갈 계열」 + 조사값(참고) + 「1단계 확인 불가 그대로」가 있다

### ④ open 0 · 칸 유효 — PASS
- `open[]` = 0
- 352행의 `sub_family` · `also_sub_families` 가 모두 families 정의 칸 안에 있다. 다른 계열 보조는 「M2 · 히알루론산(HA)」 · 「M10 · EMS」처럼 계열 코드를 붙여 적었고, 떼어 보면 M2 · M10 칸에 있다(W2)
- `also_families` 코드는 모두 18계열 안이다

### ⑤ 강 28행 출처 전수 대조

| 행 | 출처 | 결과 |
|---|---|---|
| hADM 6(리투오 · 리투오 파인 · 셀르디엠 · 쥬브아셀 · 아디떼 · 도프ECM) | taxonomy M3 하위 label 「무세포동종진피(hADM)」 · description 「주요 제조사: 엘앤씨바이오(리투오), 한스바이오메드(셀르디엠), 바임(쥬브아셀), 더에쓰씨(아디떼), 도프」 | ✓ |
| 바이리즌 | step1 허가 2건: 제허23-784 official_name 「PN SKINBOOSTER」 · 제허20-527 「the 채움 프리미엄 No. 2」(사용목적 「가교 히알루론산」) | ✓ |
| 민트리프트 | economist.co.kr 「Mint Lift는 PDO(폴리디옥사논)안면 조직 고정용 실」 · emedi 2014005735 사용목적 「흡수성 재질의 실」 | ✓ |
| 블루로즈클레어 | emedi 2021006818 brandName 「BLUE ROSE CLAIR」 포함 · 사용목적 「폴리카프로락톤봉합사와 범용카테터캐뉼러로 구성」 · 모델 PCL-18G | ✓ |
| N코그 | step1 reference 제허17-914 품목 「폴리디옥사논봉합사」(엔파인더스) · nfinders.com PDO Thread 페이지(제품명 N-COG 는 페이지에 없음, 업체 PDO 실은 맞음) | ✓ |
| 캐번실 | step1 reference 제허18-61 「폴리디옥사논봉합사」 | ✓ |
| 울트라V | 주 PDO ✓ · 보조 PCL ✗ | **F2** |
| 프락셀 듀얼 | 허가 모델 「Fraxel(R) DUAL 1550/1927」 · 원천 Er:Glass 1550 + 톨륨 1927 | ✓ |
| 셀렉V · BBL 히어로 · 노블린 · 아포지 엘리트 플러스 | 허가 item ↔ 원천 설명(각각 펄스광선/QS Nd:YAG · 반도체/IPL · 알렉산드라이트/Nd:YAG · 알렉산드라이트/Nd:YAG) — 둘 다 원문에 있다 · conflict 기록 | ✓ |
| 엑셀 V+ | 허가 엔디야그 · 원천 「KTP+Nd:YAG」 | ✓ |
| 브이빔 퍼펙타 | candelamedical.com/products/vbeam-perfecta — 「Vbeam 595 nm pulsed dye laser」 | ✓ (W1 — 인용문이 페이지에 그대로 있지는 않음) |
| 클라리티2 | 허가 알렉산드라이트 2건 + 엔디야그 2건 · 원천 Nd:YAG | ✓ |
| 젠틀맥스 프로 플러스 | Candela PDF 「dual wavelength platform of both the 755 nm Alexandrite as well as the 1064 nm Nd:YAG」 · gentle-pro-series 「both Alexandrite (755 nm) and Nd:YAG (1064 nm)」 | ✓ |
| 젠틀맥스 프로 | 허가 알렉산드라이트 · 원천 「알렉산드라이트(755nm)와 Nd:YAG(1064nm)」 | ✓ |
| 스플렌더 X | 허가 모델 「SPLENDOR X Alexandrite+Nd:YAG」 | ✓ |
| SP 다이나미스 | 허가 엔디야그 · 원천 「Er:YAG와 Nd:YAG 듀얼」 | ✓ |
| 소프라노 티타늄 | 주 반도체 ✓ · 보조 2 ✗(FDA 510k 는 전부 diode) | **F1** |
| 소프웨이브 | aafprs 「Synchronous Ultrasound Parallel Beam Technology SUPERB TM」 · biospectrumasia 「Korea approves … Synchronous Ultrasound Parallel Beam technology SUPERB™」 · sofwave.com 「SUPERB™」 | ✓ (W4) |
| 이브타이탄 | emedi 2024003814 brandName 「EVE Synergy, EVE Titan」 · 사용목적 「1. 고주파자극기: 고주파 에너지 … 2. 저주파자극기: … 저주파 전류」 | ✓ |
| 트리필 프로 | mcure.co.kr 「State-of-the-art CO2 gas and Drug delivery system」 · 「All drug injection available : PLLA, PDLA, HA, PDRN, FILLER」 | ✓ |

- 28행 중 26 ✓ · 2 ✗(F1 · F2)
- 외부 URL 10건은 모두 200 으로 받았다. emedi 3건은 품목 상세 POST(recheck_licenses.py 와 같은 방식)로 실제 조회했다

### ⑥ 셈 · 결정론 · 회귀 — PASS
- **판정 셈**: 맞음 256 · 옮김 66 · 여러 19 · 계열 밖 8 · 판단 필요 3 = 352. v3 대비 이브타이탄 판단 필요 → 여러, 트리필 프로 판단 필요 → 옮김뿐이다
- 계열별 행 수: M4 41 · M9 50(+1씩), 나머지는 v3 와 같다
- **결정론**: scratchpad 사본(입력 6파일)에서 두 번 다시 돌렸다. 3파일 모두 원본과 바이트 동일하다. step1-products.json md5 `cfa00e1a…` 그대로다
- **회귀**
  - 해결안 40행 밖 312행에서 바뀐 필드 **0**. 새 칸(also_sub_families · conflict · evidence_level · confirm_question · pending_director)도 312행에서는 모두 빈 값이다
  - families 차이는 M4 · M8 · M9 sub_families(새 칸 · 보조 매질 칸)뿐이다
  - research_errata · source_fix_candidates · out_of_family 는 v3 와 같다
  - v3 PASS 항목(M8 매질 한 축 · M7 동의어 · M2 이름 · M17 근거)도 그대로다

### ⑦ step2-origin-questions.md — PASS
- 두 절이 있다: 「원장님 문의 3」(질문 + 확인되면 갈 계열) · 「근거 약 확인 9」(질문 + 지금 값)
- 1단계 질문과 겹치는 2건(피코코어 · 트루피코)은 「(1단계 질문과 같음)」으로 표시돼 있다

---

## WARN

### W1. 브이빔 퍼펙타 — 인용문이 지금 페이지에 그대로 없음
- 해결안 근거 「Vbeam Perfecta … pulsed dye laser … wavelength of 595 nm」. 지금 그 URL 은 Vbeam Pro 소개 페이지다. Perfecta 는 「up to 2x the life of Vbeam Perfecta」 같은 비교로만 나온다
- 같은 페이지에 「Vbeam 595 nm pulsed dye laser」가 있어 값(PDL)은 맞다
- 고칠 값: 인용문을 실제 문구로 바꾸거나 Perfecta 제품 문서(IFU 등)로 출처를 바꾼다

### W2. also_sub_families 표기가 두 가지 섞임
- 같은 계열 보조는 「엔디야그 레이저」, 다른 계열 보조는 「M2 · 히알루론산(HA)」 · 「M10 · EMS」로 적혔다. 쓰는 쪽이 문자열을 쪼개야 한다
- 고칠 값(선택): `{family, sub_family}` 객체 배열로 통일한다

### W3. 아이콘 · 디스커버리 피코 확인 질문은 반영 쪽이 지었다
- 해결안 `ask` 가 null 이라 `step2-apply.py` 의 `ASK_FILL` 이 `why_weak` 를 질문 문장으로 바꿨다. 내용은 why_weak 와 맞는다. 다만 「해결안 그대로」가 아니므로 해결안 쪽 `ask` 를 채워 두는 편이 낫다
- 참고(W4): 소프웨이브 근거의 「원천 하위 「SUPERB 초음파」」는 step1 계열 이름의 하위 표기다. taxonomy 에서는 이 항목이 M9-4 「복합 에너지」 아래에 있다. 값에는 영향이 없다
