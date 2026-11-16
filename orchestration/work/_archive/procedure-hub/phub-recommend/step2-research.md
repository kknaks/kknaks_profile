# 실버 2단계(계열) 조사 — step2-research

> 2026-10-28 · researcher · 입력: `step1-products.json` active 352행(고정) · `literature-evidence.json` M1~M17 · `taxonomy.json` · v3 families · PubMed(ESummary 확인). 원장·결정·원천 파일은 고치지 않았다. 데이터: `step2-research.json`

## 1. 결정 묶음 목록

| # | 묶음 | 추천 | 근거 | 영향 | 최종 판단 |
|---|---|---|---|---|---|
| D01 | 지방분해주사 10행(데옥시콜산 9 · 콜산 1) | M16 에서 빼 새 계열 N1 로 세운다 | M16 문헌은 정맥 영양 — 피하 지방세포 용해는 정의 밖 + 독립 리뷰(27785706 · 38297988) → 새 계열 조건 둘 다 충족 | 10행 | **사용자** |
| D02 | 시술이 아닌 의약품 3행(아큐탄 · 라이넥 · 멜스몬) | 계열을 주지 않고 「의약품(시술 계열 밖)」으로 둔다 — 제품 원장 행은 그대로(1단계 D32) | 먹는 약 · 간보호제/자하거추출물 — 17 정의 밖, 미용 독립 문헌 확인 안 됨 | 3행 | **사용자** |
| D03 | M15 「외용 관리」 범위 — 화학 박피 38 · 기계적 박리·클렌징(하이드라더마브레이전 등) · 외용제 | 화학 박피와 하이드라더마브레이전을 새 계열로 떼지 않고 M15 하위 계열(「화학 박피」 「기계적 박리·클렌징」 「외용제」)로 둔다 | M15 「Topical」 — 박피·하이드라더마브레이전도 피부 표면 적용이라 17 안에 듦(분리 조건 미충족) | 53행 | **사용자** |
| D04 | LED 광치료 6행 + 현장 오메가라이트 1행 | M15 → M8 로 옮기고 M8 정의를 「레이저·IPL·LED(광)」로 넓힌다 | LED 는 광원(외용 아님) — IPL 같은 비간섭광(40751922), 원천 M8 「Laser & Light」 | 7행 | **사용자** |
| D05 | 주입 기기 7행(큐어젯 · 미라젯 · 에어젯 · 노보젯 · 하이쿡스 · 더마샤인 · 비타인젝터) | M15 → M4(스킨부스터)의 제품(기기)으로. 「어떻게」(무바늘 제트 · 멀티니들)는 4단계 기법 | M4 근거 문헌(39544509)이 무바늘 제트·자동 주입기를 스킨부스터 전달 방법으로 다룸(큐어젯 예시) | 7행 | 추천대로(승인) |
| D06 | 콜라겐 주입제 4행(콜라쥬 · 레티젠 · 미라콜 · 콜라겐핀) | M3 → M4 하위 「콜라겐」(M4 원천 콜라겐/신규 3행과 합침) | 콜라겐은 미립자 이물반응(M3) 아님 · 39544509 Collagen 절이 레티젠 예시 | 4행 | 추천대로(승인) |
| D07 | 무세포동종진피(hADM) 6행 | M3 → M4(스킨부스터) | 원천 설명 「유도가 아니라 직접 보충」 = M3 정의 반대 · hADM 직접 문헌은 확인 안 됨 | 6행 | **사용자** |
| D08 | 엑소좀 5행(ASCE+ · 셀엑소좀 · 카탈리스트 · 드원셀 · EXOSOME SKIN) | 엑소좀은 M5 하위 「엑소좀」 — M4 의 4행 옮김, EXOSOME SKIN 은 이미 M5. 줄기세포 배양액·추출물은 M17 유지 | 문헌 M5 이름에 exosome 명시 · M4 문헌은 exosome 0건 | 5행 | 추천대로(승인) |
| D09 | 초음파·이온 흡수 보조 기기(LDM · 벨라소닉 · 소노케어 · 크라이오 멀티마스터 + 트윈픽셀 보조) | M15 「외용 관리」 안에 둔다(외용제 흡수를 돕는 기기) | 허가 「초음파자극기」(비집속) · 외용 흡수 보조(26608060) — 독립 미용 문헌 확인 안 됨 | 5행 | **사용자** |
| D10 | procedure-master-v3 X1~X6(워커 초안 · 확정 아님) | X1 → N1(D01) · X2 카복시 → 새 계열 후보 N2 · X3 미녹시딜 두피 메조 → M4 · X4 성장호르몬 → 계열 밖 · X5 태반제제 → 계열 밖(D02) · X6 RF 지방감소 → M9(D11) | X1·X2 만 새 계열 조건 충족(27785706 · 35124882), X3 은 M4, X4·X5 는 17 밖+독립 문헌 없음, X6 은 M9 | 14행 | **사용자** |
| D11 | 비침습 지방 감소 기기 5행(트루스컬프트 · 바넥스 · 바넥스프로 · 바이캐빈 · 슬렌더엑스) | 새 계열 「비침습 지방 감소」를 세우지 않고 에너지대로 둔다 — RF → M9, 레이저 → M8, 근육 자극 겸용 → M10. 지방 감소는 6단계 목적 엣지. v3 X6 폐지 | 비침습 체형 기기는 에너지별(31168833) — 각 에너지가 이미 M8·M9·M10·M14 에 있음 | 5행 | **사용자** |
| D12 | 진단 장비 4행(미라쥬 · 3D 메타뷰 · 마크뷰 · 스케나) | 시술 계열을 주지 않고 1단계대로 「진단 장비」 노드 | 측정·촬영 기기 — 시술의 「무엇을」 아님 | 4행 | 추천대로(승인) |
| D13 | 다른 계열끼리 합친 4건(하모니카 · 볼뉴머 · LDM · 아포지 엘리트 플러스) | 하모니카 = 여러 계열(주 M2 · 보조 M3) · 볼뉴머 = M9 · LDM = M15(D09) · 아포지 엘리트 플러스 = M8 | 합쳐진 원천 행 설명 · 허가 품목 대조 | 4행 | 추천대로(승인) |
| D14 | 계열 없는 현장 기기 29행 | 허가 품목명으로 부여 — 엔디야그·반도체·레이저 조사기 11 → M8 · 범용전기수술기 3 + 집속형초음파 3 + HIFU 미용기기 1 → M9 · 의약품 흡수 유도 피부 자극기 1 → M12 · 하이드로더마브레이전 · 산소 · 흡수 보조 4 → M15 · LED 1 → M8(D04) · EMS+RF 1 → 여러(M10) · 판단 필요 3(이브타이탄 · 벨르업 · 더마큐어) · 카복시 장비 1(트리필 프로, D10) | 1단계 허가 품목명 · web4 출처로 부여 | 29행 | 추천대로(승인) |
| D15 | 복합 장비 15행(두 계열 에너지·재료) | 주 계열 1 + 보조 계열 — 주 = 허가 품목 · 원천 위치 · 설명 첫 원리 순으로 | 주 = 허가 품목 · 원천 위치 · 설명 첫 원리 | 15행 | 추천대로(승인) |
| D16 | 개별 옮김·판단 4행(신펄 · 올타이트 · 헤어셀 · 알렉스필) | 신펄 → M3(PLLA) · 올타이트 → M9 · 헤어셀 · 알렉스필은 판단 필요로 두고 원천 확인 | 원천 설명 · 허가 품목 대조 | 4행 | 추천대로(승인) |
| D17 | 계열 이름 한글 추천 16(M1 확정 제외) + N1 | 문헌 영문 이름을 기준으로 한 한글 이름(A 표) — 한글 공식 출처를 찾은 것은 M2 「성형용 필러」(동의어) · M7 「안면조직고정용실」(식약처 품목) 정도, 나머지는 「확인 안 됨」 | 「공식 일반명」 규칙 — 국내 출처 확인된 계열이 적음 | 16계열 + N1(이름만, 행 이동 없음) | **사용자** |
| D18 | 하위 계열 처리 규칙(17계열 공통) | 수입/국산 · 브랜드 → 제품 속성/제품 · 재질(M2·M3·M4·M7) · 광원/방식(M8) · 에너지(M9·M10) → 하위 계열 · 형태(M7) · 기구 형태(M12) → 제품 속성 · 용도별(M1-3)·부위(M10 페이셜/바디)·목적(M8 색소·혈관·제모 · M16 미백·피로) → 5·3·6단계 · 시그니처 프로그램 → 6단계 패키지 · 「기타」「추가」 → 해체 | 계열 = 무엇을 / 부위 · 목적 · 패키지는 다른 단계 | 17계열(하위 계열 · 행 이동 없음) | 추천대로(승인) |

「영향」은 그 묶음에 걸린 **행 수**(한 행이 두 묶음에 걸리면 양쪽에 셈 — 합이 352 가 아니다). 행 이동의 실제 셈은 §3.

## 2. 사용자가 최종 판단해야 하는 것만

1. **D01 지방분해주사 10행(데옥시콜산 9 · 콜산 1)** — 추천: M16 에서 빼 새 계열 N1 로 세운다. 이유: 계열 수를 17 → 18 로 늘리는 유일한 추천 — 「늘리는 것은 사용자 확정 기준을 둘 다 충족할 때만」이라 최종 판단은 사용자
2. **D02 시술이 아닌 의약품 3행(아큐탄 · 라이넥 · 멜스몬)** — 추천: 계열을 주지 않고 「의약품(시술 계열 밖)」으로 둔다 — 제품 원장 행은 그대로(1단계 D32). 이유: 원천은 M15 · M16 에 두고 병원은 「태반주사」로 팔고 있음 — 추천에서 빠지는 결과라 사용자 확인
3. **D03 M15 「외용 관리」 범위 — 화학 박피 38 · 기계적 박리·클렌징(하이드라더마브레이전 등) · 외용제** — 추천: 화학 박피와 하이드라더마브레이전을 새 계열로 떼지 않고 M15 하위 계열(「화학 박피」 「기계적 박리·클렌징」 「외용제」)로 둔다. 이유: 원천 개발 당시 문헌 카테고리에 「Chemical peeling」이 따로 있었던 흔적(clinical-review.md 「M13 Chemical peeling」 오매칭 처리)이 있어 분리 여부가 경계선
4. **D04 LED 광치료 6행 + 현장 오메가라이트 1행** — 추천: M15 → M8 로 옮기고 M8 정의를 「레이저·IPL·LED(광)」로 넓힌다. 이유: M8 정의를 문헌 이름보다 넓히는 판단(대안: 새 계열 「광생물조절(LED)」 — 17 밖 + 독립 문헌 둘 다 성립)
5. **D07 무세포동종진피(hADM) 6행** — 추천: M3 → M4(스킨부스터). 이유: 문헌 근거가 정의 일반론뿐이고 원천은 M3 에 둠 — 인체조직 제품이라 다른 주입제와 성격도 다름
6. **D09 초음파·이온 흡수 보조 기기(LDM · 벨라소닉 · 소노케어 · 크라이오 멀티마스터 + 트윈픽셀 보조)** — 추천: M15 「외용 관리」 안에 둔다(외용제 흡수를 돕는 기기). 이유: M15 를 「바르는 약제」에서 「바르는 약제 + 흡수 보조 기기」로 넓히는 판단(대안: 계열 밖)
7. **D10 procedure-master-v3 X1~X6(워커 초안 · 확정 아님)** — 추천: X1 → N1(D01) · X2 카복시 → 새 계열 후보 N2 · X3 미녹시딜 두피 메조 → M4 · X4 성장호르몬 → 계열 밖 · X5 태반제제 → 계열 밖(D02) · X6 RF 지방감소 → M9(D11). 이유: X2 는 새 계열 추천 두 번째 — 제품 행은 트리필 프로 1행(판단 필요)뿐이고 나머지는 5단계 단위 시술(카복시테라피)
8. **D11 비침습 지방 감소 기기 5행(트루스컬프트 · 바넥스 · 바넥스프로 · 바이캐빈 · 슬렌더엑스)** — 추천: 새 계열 「비침습 지방 감소」를 세우지 않고 에너지대로 둔다 — RF → M9, 레이저 → M8, 근육 자극 겸용 → M10. 지방 감소는 6단계 목적 엣지. v3 X6 폐지. 이유: M9 정의가 문헌상 「타이트닝」이라 RF 지방 감소를 넣으면 이름(리프팅)과 용도가 어긋남 · v3 X6 은 1차 답 ③ 에서 나온 것
9. **D17 계열 이름 한글 추천 16(M1 확정 제외) + N1** — 추천: 문헌 영문 이름을 기준으로 한 한글 이름(A 표) — 한글 공식 출처를 찾은 것은 M2 「성형용 필러」(동의어) · M7 「안면조직고정용실」(식약처 품목) 정도, 나머지는 「확인 안 됨」. 이유: 공식 일반명 규칙을 그대로 지키면 이름을 못 정하는 계열이 생김 — 문헌 직역으로 둘지 사용자 판단

나머지 9묶음은 근거가 문헌·허가 품목으로 닫혀 있어 추천대로 반영해도 된다(승인). 행 단위 「판단 필요」 6행은 정보가 없어 추천을 못 한 것 — §6 끝 목록.

## 3. 셈

| 판정 | 행 |
|---|---|
| 맞음 | 256 |
| 옮김 | 72 |
| 여러 계열 | 18 |
| 판단 필요 | 6 |
| **합** | **352** |

- 옮김 72행 = 17계열 사이 이동 31 · 계열 없던 현장 기기에 부여 24 · 새 계열 N1(D01) 10 · 계열 밖(D02 · D12) 7
- 자동 추가(auto-) 219행 중: 맞음 165 · 옮김 37 · 여러 계열 15 · 판단 필요 2
- 추천 계열별 행(여러 계열은 주 계열로 셈): M1 보툴리눔 톡신 19 · M2 필러 29 · M3 바이오스티뮬레이터 14 · M4 스킨부스터 40 · M5 PRP·엑소좀 8 · M7 실리프팅 12 · M8 레이저·IPL 68 · M9 HIFU·고주파 리프팅 49 · M10 HIFEM·EMS 근육 자극 8 · M11 고주파 마이크로니들(니들RF) 13 · M12 마이크로니들링(MTS) 3 · M13 플라즈마 3 · M14 냉동지방분해 3 · M15 외용 관리 55 · M17 줄기세포·줄기세포 유래 제제 5 · N1 지방분해 주사 10 · 계열 밖 7 · 판단 필요  6
- 새 계열 추천은 N1(지방분해 주사) 1개 + 후보 N2(카복시, 제품 행 0 — D10). 계열 수 17 → 18(D01 승인 시)

## 4. 계열 정의 (A)

### M1 보툴리눔 톡신 — 확정(10-27)

- 문헌 이름: Botulinum toxin type A (aesthetic)
- 정의: 보툴리눔 독소 A형을 근육·피부에 주사해 신경근 접합부의 아세틸콜린 분비를 막아 근육을 이완시키는 시술
- 근거:
  - `literature-evidence.json#categories.M1.name` = Botulinum toxin type A (aesthetic)
  - `literature-evidence.json#categories.M1.moa[0]` “Botulinum toxin type A inhibits the secretion of acetylcholine at the presynaptic neuromuscular junction.” (PMID 33714246)
  - `literature-evidence.json#categories.M1.moa[1]` “Botulinum toxin type A weakens skeletal muscles by presynaptic blockade of the exocytosis of acetylcholine-containing vesicles in the neuromuscular junction.” (PMID 33714246)
- 추천 이름: **보툴리눔 톡신** (확정(10-27)) — _RESUME.md §2 2026-10-27 「계열 이름 = 공식 일반명(M1 → 「보툴리눔 톡신」)」 · ATC M03AX01 「BOTULINUM TOXIN|보툴리눔 독소」(step1-products.json 보톡스 4_license.licenses[].kpic.atc)
- 동의어: 보톡스(상담 용어 · 엘러간 제품 이름과 겹침) · 톡신 · 보툴리눔 독소(ATC 한글) · Botulinum toxin

| 원천 하위 | 처리 | 근거 |
|---|---|---|
| M1-2 수입 · M1-1 국산 | 제품 속성 | 수입/국산은 제조국·수입사 — 1단계 6_companies(importer·manufacturer) 칸이 이미 가짐. 문헌 M1 정의는 A형 하나로 하위 구분 없음(literature M1.moa) |
| M1-3 용도별(13: 주름 · 사각턱 · 턱선보톡스 · 다한증 …) | 5단계로 넘김(표시만) | _RESUME §2 OQ-317 「턱선보톡스 = 단위 시술(보톡스 × 턱선)」 · 부위 이름 = 단위 시술, 목적 이름 = 목적 엣지 |

### M2 필러 — 추천

- 문헌 이름: Hyaluronic acid dermal fillers
- 정의: 진피·피하에 겔 상태의 충전 물질(주로 가교 히알루론산)을 주입해 부피·윤곽을 채우는 시술
- 근거:
  - `literature-evidence.json#categories.M2.name` = Hyaluronic acid dermal fillers
  - `literature-evidence.json#categories.M2.moa[0]` “Crosslinking of hyaluronic acid with agents such as BDDE modifies viscoelastic properties and prolongs tissue residence time.” (PMID 30960626)
  - `literature-evidence.json#categories.M2.moa[1]` “Hyaluronic acid fillers restore facial volume and contour lost due to ageing-related changes in skin, fat pads, bones, and muscles.” (PMID 33633459)
- 추천 이름: **필러** (추천) — 원천 이름 「필러」 = 상담 용어와 같음 · 식약처 안전정보 페이지 제목 「성형용 필러」(medical-codes.md §1 출처 「MFDS 성형용 필러 안전성정보」 링크 — 원문은 이번에 다시 열지 않음) · 식약처 품목명 「조직수복용생체재료」(step1 M2 행 허가 item)는 PN·콜라겐도 포함해 계열 이름으로 쓰기엔 넓음
- 동의어: 성형용 필러 · 히알루론산 필러 · HA 필러 · Dermal filler

| 원천 하위 | 처리 | 근거 |
|---|---|---|
| M2-1 국산 HA · M2-2 수입 HA | 하위 계열 「히알루론산(HA)」 1개 + 국산/수입은 제품 속성 | 문헌 M2 정의가 HA 필러(literature M2.name) · 국산/수입은 6_companies |
| M2-3 비HA 필러(아테콜 PMMA · 아쿠아미드 폴리아크릴아마이드) | 하위 계열 「비HA(영구·반영구)」 | 문헌 M2 는 HA 만 다룸 — 비HA 를 M2 에 두는 근거는 원천 하위(M2-3)와 허가 품목 「조직 수복용 생체 재료」(아테콜 ARTESENSE). 비HA 필러 독립 문헌은 이번에 찾지 않음(확인 안 됨) |

### M3 바이오스티뮬레이터 — 추천(한글 공식명 확인 안 됨)

- 문헌 이름: Collagen-stimulating biostimulators (PLLA/CaHA/PDLLA/PCL)
- 정의: 생분해성 고분자 미립자(PLLA · CaHA · PDLLA · PCL · PDO)를 주입해 이물 반응으로 자가 콜라겐 생성을 유도하는 시술
- 근거:
  - `literature-evidence.json#categories.M3.name` = Collagen-stimulating biostimulators (PLLA/CaHA/PDLLA/PCL)
  - `literature-evidence.json#categories.M3.moa[0]` “PLLA induces neocollagenesis through immune-mediated mechanisms involving macrophage activation and M2 polarization, distinct from mechanotransductive pathways” (PMID 38853456)
- 추천 이름: **바이오스티뮬레이터** (추천(한글 공식명 확인 안 됨)) — 문헌 M3 영문 「biostimulators」 음역 — 한국 공식 일반명 출처 확인 안 됨 / 「콜라겐부스터」는 상담 용어(원천 이름 일부)
- 동의어: 콜라겐부스터 · 콜라겐 자극제 · Collagen stimulator

| 원천 하위 | 처리 | 근거 |
|---|---|---|
| M3-1 PLLA · M3-2 CaHA · M3-3 PCL · M3-4 PDLLA · PDO | 하위 계열(재질) | 문헌 M3 이름이 재질로 나눔 「(PLLA/CaHA/PDLLA/PCL)」 · PDO 미립자(울트라콜)는 원천 설명 「이물반응을 유도, 콜라겐 신생」이 M3 정의와 같음 |
| M3-5 콜라겐 | 다른 계열로(M4) | 묶음 D06 — 39544509 Collagen 절 「intradermal collagen injections … skin regeneration」 · LAETIGEN(레티젠) 예시 |
| 무세포동종진피(hADM) | 다른 계열로(M4) — 사용자 판단 | 묶음 D07 — 원천 설명 「콜라겐 생성을 ‘유도’하는 것이 아니라 … ‘직접 보충’」 = M3 정의(collagen-stimulating)와 반대 |

### M4 스킨부스터 — 추천

- 문헌 이름: Skinboosters and mesotherapy (non-crosslinked HA, polynucleotides, amino-acid/vitamin cocktails)
- 정의: 비가교·저가교 히알루론산 · 폴리뉴클레오타이드 · 콜라겐 · 아미노산/비타민 칵테일 같은 재료를 진피에 소량씩 여러 점 주입(또는 무바늘 제트 주입)해 피부 질을 개선하는 시술
- 근거:
  - `literature-evidence.json#categories.M4.name` = Skinboosters and mesotherapy (non-crosslinked HA, polynucleotides, amino-acid/vitamin cocktails)
  - `literature-evidence.json#categories.M4.moa[0]` “Hyaluronic acid inhibits collagenase enzymes slowing collagen breakdown.” (PMID 39544509)
  - PMID 39544509 「Injectable "Skin Boosters" in Aging Skin Rejuvenation: A Current Overview.」 Arch Plast Surg 2024 — “목차: Hyaluronic Acid · Polynucleotide · Collagen · Polycomponent Products · Delivery Methods(Intradermal Injection Technique · Needle-free Jet Injectors) — 본문 「An example of this technology is the Curejet (Baz Biomedic, Seoul, Korea)」” (ESummary 확인)
- 추천 이름: **스킨부스터** (추천) — 원천 이름 = 상담 용어 · 문헌 M4 근거 논문 제목 「Injectable "Skin Boosters"」(39544509, 한국 저자)
- 동의어: 물광주사 · 메조테라피 · Skin booster · Mesotherapy

| 원천 하위 | 처리 | 근거 |
|---|---|---|
| M4-2 HA(물광) | 하위 계열 「히알루론산」 | 39544509 절 Hyaluronic Acid · literature M4.effects 비가교 HA |
| M4-1 PN/PDRN | 하위 계열 「폴리뉴클레오타이드(PN·PDRN)」 | 문헌 M4 이름 「polynucleotides」 · 39544509 절 Polynucleotide |
| auto-new-M4 콜라겐/신규 + M3-5 콜라겐 | 하위 계열 「콜라겐」 | 39544509 절 Collagen |
| (복합 성분: NCTF · 매쿰7 · 사이토케어 · 릴리이드M …) | 하위 계열 「복합 성분(칵테일)」 | 문헌 M4 이름 「amino-acid/vitamin cocktails」 · 39544509 절 Polycomponent Products |
| M4-3 엑소좀/성장인자 | 다른 계열로(M5) | 묶음 D08 — 문헌 M5 이름 「PRP and exosome therapies」. 39544509 는 exosome 을 다루지 않음(본문 검색 0건) |
| 주입 기기(원천 M15-6 주입장비 · 물광/메조건) | M4 의 제품(기기) — 하위 계열 아님 · 「어떻게」는 4단계 기법 | 묶음 D05 — 39544509 Delivery Methods 절 |

### M5 PRP·엑소좀 — 추천(한글 공식명 확인 안 됨)

- 문헌 이름: Platelet-rich plasma (PRP) and exosome therapies
- 정의: 자가혈에서 농축한 혈소판 성장인자(PRP·PRF 등) 또는 세포외소포(엑소좀)를 주입·도포해 재생을 유도하는 시술
- 근거:
  - `literature-evidence.json#categories.M5.name` = Platelet-rich plasma (PRP) and exosome therapies
  - `literature-evidence.json#categories.M5.moa[0]` “PRP delivers concentrated platelet-derived growth factors (PDGF, TGF-β, VEGF, EGF) that stimulate fibroblast proliferation and collagen synthesis.” (PMID 29457008)
  - `literature-evidence.json#categories.M5.moa[1]` “Extracellular vesicles (exosomes) carry proteins, lipids, and microRNAs that modulate recipient cell signaling and extracellular matrix remodeling.” (PMID 27035812)
- 추천 이름: **PRP·엑소좀** (추천(한글 공식명 확인 안 됨)) — 문헌 M5 이름 「Platelet-rich plasma (PRP) and exosome therapies」 그대로 — 「혈소판풍부혈장」 한글 공식 출처는 이번에 확인 안 됨
- 동의어: PRP · 자가혈 · 혈소판풍부혈장 · 엑소좀 · PRP / Autologous Blood

| 원천 하위 | 처리 | 근거 |
|---|---|---|
| M5-1 PRP · M5-2 PRF(PRF·CGF) | 하위 계열 「혈소판 농축물(PRP·PRF)」 | literature M5.moa[0] PRP 성장인자 |
| 엑소좀(원천 M4-3 · M17-3 · M5-P-4) | 하위 계열 「엑소좀」 | literature M5.moa[1]·[2] exosome |
| M5-3 MCT(메타셀) · ACT | 확인 안 됨 — 5단계 | 원천 항목명만 있고 문헌 근거 없음 |

### M6 자가지방이식 — 추천

- 문헌 이름: Autologous fat grafting / lipotransfer for facial rejuvenation
- 정의: 자기 몸에서 채취한 지방을 가공해 얼굴 등 부피가 꺼진 곳에 주입하는 시술
- 근거:
  - `literature-evidence.json#categories.M6.name` = Autologous fat grafting / lipotransfer for facial rejuvenation
  - PMID 37159906 「Technical Precision with Autologous Fat Grafting for Facial Rejuvenation: A Review of the Evolving Science.」 Plast Reconstr Surg 2024 — “Autologous fat grafting is … the preferred soft-tissue filler in the correction of facial atrophy … fat grafts to be divided based on parcel size and cell type into three major subtypes: macrofat, microfat, and nanofat.” (ESummary 확인)
- 추천 이름: **자가지방이식** (추천) — 문헌 M6 이름 「Autologous fat grafting」 직역 · 원천 이름 「지방이식」은 상담 용어
- 동의어: 지방이식 · Fat grafting · Lipotransfer
- 메모: 제품 행 0(시술 계열 — 제품이 아니라 자가 조직)

| 원천 하위 | 처리 | 근거 |
|---|---|---|
| M6-1 마이크로지방이식 · M6-2 나노지방이식 | 하위 계열(지방 입자 크기) | 37159906 「macrofat, microfat, and nanofat」 |
| M6-3 SVF지방이식 | 확인 안 됨 — 5단계 | 37159906 초록의 세 아형에 SVF 없음 · M17-2 SVF 와 겹침 |

### M7 실리프팅 — 추천

- 문헌 이름: Absorbable suspension threads (PDO/PLLA/PCL) for facial lifting
- 정의: 체내에서 녹는 실(PDO · PLLA · PCL · PLCL)을 피하에 넣어 처진 조직을 기계적으로 당기고 실 주변 콜라겐 생성을 유도하는 시술
- 근거:
  - `literature-evidence.json#categories.M7.name` = Absorbable suspension threads (PDO/PLLA/PCL) for facial lifting
  - `literature-evidence.json#categories.M7.moa[1]` “Absorbable barbed threads maintain mechanical lifting action for repositioning of sagging facial tissue.” (PMID 33469333)
  - `literature-evidence.json#categories.M7.moa[2]` “Thread insertion stimulates fibroblasts and synthesis of collagen, hyaluronic acid and elastin around the thread.” (PMID 33469333)
- 추천 이름: **실리프팅** (추천) — 원천 이름 = 상담 용어 · 식약처 품목명 「안면조직고정용실」(민트리프트 · 실루엣소프트 허가 item) · 「폴리디옥사논봉합사」(테스리프트 · 오메가리프트)
- 동의어: 안면조직고정용실(식약처 품목) · 실 리프팅 · Thread lift

| 원천 하위 | 처리 | 근거 |
|---|---|---|
| M7-1 재질별(PDO · PCL · PLCL · PLLA · PCA · 복합) | 하위 계열(재질) | 문헌 M7 이름 「(PDO/PLLA/PCL)」 |
| M7-2 형태별(코그 · 모노 · 볼륨) | 제품 속성(형태) | 문헌 M7 은 형태로 나누지 않음(barbed 는 moa 서술 안의 성질) |
| M7-3 브랜드(24) | 제품(1단계 원장 행) | 브랜드 = 제품 |

### M8 레이저·IPL — 추천(묶음 D04 를 받으면 「레이저·광치료」)

- 문헌 이름: Aesthetic lasers and IPL
- 정의: 특정 파장의 레이저 또는 광대역 펄스광(IPL)을 피부에 조사해 색소·혈관·모낭·진피를 선택적으로 가열·파괴하는 시술
- 근거:
  - `literature-evidence.json#categories.M8.name` = Aesthetic lasers and IPL
  - `literature-evidence.json#categories.M8.moa[0]` “Fractional ablative lasers vaporize the epidermis and heat the dermis to prompt collagen remodeling.” (PMID 32273965)
  - `literature-evidence.json#categories.M8.moa[2]` “Picosecond Nd:YAG laser reduces pigmentation in hyperpigmented scars.” (PMID 38525494)
- 추천 이름: **레이저·IPL** (추천(묶음 D04 를 받으면 「레이저·광치료」)) — 문헌 M8 이름 「Aesthetic lasers and IPL」 · 원천 영문 「Laser & Light」 · 식약처 품목명은 광원별(엔디야그레이저수술기 · 알렉산드라이트 레이저 수술기 · 펄스광선조사기 …)
- 동의어: 레이저 · IPL · Laser & Light

| 원천 하위 | 처리 | 근거 |
|---|---|---|
| M8-2 프락셔널 | 하위 계열 「프락셔널(박피/비박피)」 | literature M8.moa[0]·[3] fractional ablative / non-ablative |
| 피코초(auto-new-M8) · M8-1 색소/토닝 중 피코 | 하위 계열 「피코초」 | literature M8.moa[2]·[5] picosecond |
| M8-3 IPL | 하위 계열 「IPL」 | 문헌 M8 이름 「and IPL」 |
| M8-1 색소/토닝 · M8-4 혈관 · M8-5 제모 | 6단계 목적으로(하위 계열 아님) | 색소·혈관·제모는 「무엇을」이 아니라 목적 — _RESUME §2 10-27 「목적은 고민→시술 엣지」 |
| M8-6 기타 | 해체 — 행마다 광원 하위로 | 「기타」는 분류 기준 없음 |

### M9 HIFU·고주파 리프팅 — 추천(한글 공식명 확인 안 됨)

- 문헌 이름: Non-invasive skin tightening: HIFU and radiofrequency
- 정의: 피부를 뚫지 않고 집속 초음파(HIFU) 또는 고주파(RF)로 진피·SMAS 를 가열해 콜라겐 수축·신생을 유도하는 기기 시술
- 근거:
  - `literature-evidence.json#categories.M9.name` = Non-invasive skin tightening: HIFU and radiofrequency
  - `literature-evidence.json#categories.M9.moa[0]` “HIFU delivers focused ultrasound energy to generate thermal zones at specific depths in the dermis and SMAS layer, triggering collagen and elastin neogenesis” (PMID 37753689)
  - `literature-evidence.json#categories.M9.moa[1]` “HIFU induces dermal collagen thickening and straightening of elastic fibers in the mid-to-deep dermis and SMAS, while RF causes neocollagenesis and neoelastogenesis more diffusely in the upper papillary dermis” (PMID 37753689)
- 추천 이름: **HIFU·고주파 리프팅** (추천(한글 공식명 확인 안 됨)) — 문헌 M9 이름 「Non-invasive skin tightening: HIFU and radiofrequency」 — 원천 이름 「기기 리프팅」·상담 「리프팅」은 동의어(사용자 10-28 「리프팅도 문헌 카테고리」) · 식약처 품목명 「집속형초음파자극시스템」 · 「범용전기수술기」(울쎄라 계열 · 볼뉴머 허가 item)
- 동의어: 기기 리프팅 · 리프팅 · 울쎄라·써마지(장비 이름 — 10-27 결정대로 시술 동의어) · Energy Based Device Lifting

| 원천 하위 | 처리 | 근거 |
|---|---|---|
| M9-1 HIFU · M9-2 RF | 하위 계열 「HIFU」 「RF」 | 문헌 M9 이름 |
| M9-3 마이크로웨이브 | 하위 계열(원천 유지) — 문헌 확인 안 됨 | 문헌 M9 는 HIFU·RF 만 이름에 둠 |
| M9-4 복합 에너지 | 해체 — 행마다 주 에너지 하위 + 「여러 계열」 표시 | 복합은 분류 기준이 아니라 장비 성질 |
| M9-SIG 시그니처 프로그램 | 6단계(패키지)로 | _RESUME §2 10-27 「패키지는 단위 시술 묶음」 |

### M10 HIFEM·EMS 근육 자극 — 추천(한글 공식명 확인 안 됨)

- 문헌 이름: HIFEM/HIFES and EMS
- 정의: 고강도 집속 전자기장(HIFEM) 또는 전기 자극(EMS)으로 근육을 강제로 수축시키는 기기 시술
- 근거:
  - `literature-evidence.json#categories.M10.name` = HIFEM/HIFES and EMS
  - PMID 33960109 「The role and clinical benefits of high-intensity focused electromagnetic devices for non-invasive lipolysis and beyond: A narrative review and position paper.」 J Cosmet Dermatol 2021 — “In 2018, the first device to use high-intensity focused electromagnetic (HIFEM) technology to non-invasively build muscle was brought to market.” (ESummary 확인)
  - PMID 37957393 「High-Intensity Focused Electromagnetic (HIFEM) Energy With and Without Radiofrequency for Noninvasive Body Contouring: A Systematic Review.」 Aesthetic Plast Surg 2024 (ESummary 확인)
- 추천 이름: **HIFEM·EMS 근육 자극** (추천(한글 공식명 확인 안 됨)) — 문헌 M10 이름 「HIFEM/HIFES and EMS」 — 한글 공식 일반명 출처 확인 안 됨
- 동의어: HIFES/EMS · EMS · 엠스컬프트(장비 이름)

| 원천 하위 | 처리 | 근거 |
|---|---|---|
| M10-1 페이셜 EMS · M10-2 바디 EMS | 3단계 부위로(하위 계열 아님) | 얼굴/바디는 「어디에」 — _RESUME §2 시술 = 무엇을 × 어디에 × 어떻게 |
| (HIFEM · EMS) | 하위 계열 「HIFEM」 「EMS」 | 문헌 M10 이름 |

### M11 고주파 마이크로니들(니들RF) — 추천(한글 공식명 확인 안 됨)

- 문헌 이름: Fractional radiofrequency microneedling (RF microneedling)
- 정의: 절연·비절연 미세침을 진피에 찌른 뒤 침 끝으로 고주파를 흘려 분획 열손상을 만드는 시술
- 근거:
  - `literature-evidence.json#categories.M11.name` = Fractional radiofrequency microneedling (RF microneedling)
  - PMID 33577211 「Radiofrequency Microneedling: A Comprehensive and Critical Review.」 Dermatol Surg 2021 — “검색어 「"radiofrequency microneedling" OR "fractional radiofrequency" OR "radiofrequency needling" OR "radiofrequency percutaneous collagen induction"」 — RFMN 을 다른 에너지 기기와 나란히 독립 범주로 검토” (ESummary 확인)
- 추천 이름: **고주파 마이크로니들(니들RF)** (추천(한글 공식명 확인 안 됨)) — 문헌 M11 이름 「Fractional radiofrequency microneedling」 · 원천·상담 「니들RF」
- 동의어: 니들RF · 프락셔널 고주파 · Microneedle RF

| 원천 하위 | 처리 | 근거 |
|---|---|---|
| M11-1 니들RF 장비 | 하위 계열 없음(단일) | 원천 하위 1개 = 장비 목록 |

### M12 마이크로니들링(MTS) — 추천

- 문헌 이름: Microneedling / percutaneous collagen induction (non-RF)
- 정의: 고주파 없이 미세침(롤러·스탬프·전동 펜)으로 피부에 미세 천공을 내 상처 치유 과정의 콜라겐 생성을 유도하는 시술
- 근거:
  - `literature-evidence.json#categories.M12.name` = Microneedling / percutaneous collagen induction (non-RF)
  - `literature-evidence.json#categories.M12.moa[0]` “Microneedling creates micro-punctures in the skin that stimulate collagen production through percutaneous collagen induction.” (PMID 27559496)
- 추천 이름: **마이크로니들링(MTS)** (추천) — 문헌 M12 이름 「Microneedling / percutaneous collagen induction」 · 상담 「MTS」 · 식약처 품목명 「의약품 흡수 유도 피부 자극기」(AUTO MTS 허가 제인 10-343)
- 동의어: MTS · 더마펜(장비 이름) · Microneedling

| 원천 하위 | 처리 | 근거 |
|---|---|---|
| M12-1 수동 · M12-2 전동 | 제품 속성(기구 형태) | 문헌 M12 는 기구 형태로 나누지 않음 |

### M13 플라즈마 — 추천

- 문헌 이름: Plasma skin treatment
- 정의: 이온화된 기체(플라즈마)의 에너지를 피부 표면에 직접 전달해 색소단(chromophore)과 무관하게 열손상·재생을 일으키는 시술
- 근거:
  - `literature-evidence.json#categories.M13.name` = Plasma skin treatment
  - PMID 18038498 「Plasma skin regeneration technology.」 J Drugs Dermatol 2007 — “Unlike lasers which rely on the principle of selective photothermolysis … plasma technology delivers heat energy directly to tissue upon contact without reliance on skin chromophores.” (ESummary 확인)
- 추천 이름: **플라즈마** (추천) — 문헌 M13 이름 「Plasma skin treatment」 · 원천·상담 이름 같음
- 동의어: 플라즈마 피부 재생(plasma skin regeneration) · Plasma

| 원천 하위 | 처리 | 근거 |
|---|---|---|
| M13-1 핫 · M13-2 콜드 | 하위 계열(원천 유지) — 콜드 플라즈마 문헌 확인 안 됨 | 18038498 은 열(핫) 플라즈마만 다룸 |

### M14 냉동지방분해 — 추천(한글 공식명 확인 안 됨)

- 문헌 이름: Cryolipolysis
- 정의: 피부 밖에서 지방층을 냉각해 지방세포만 선택적으로 손상시키는 비수술 지방 감소 시술
- 근거:
  - `literature-evidence.json#categories.M14.name` = Cryolipolysis
  - PMID 26017594 「Cryolipolysis for fat reduction and body contouring: safety and efficacy of current treatment paradigms.」 Plast Reconstr Surg 2015 — “Cryolipolysis is a nonsurgical technique for localized fat reduction.” (ESummary 확인)
- 추천 이름: **냉동지방분해** (추천(한글 공식명 확인 안 됨)) — 문헌 M14 「Cryolipolysis」 · 원천 상담 「냉각지방분해」 · 한글 공식 일반명 출처 확인 안 됨
- 동의어: 크라이오리포라이시스 · 냉각지방분해 · 쿨스컬프팅(장비 이름) · Cryolipolysis

| 원천 하위 | 처리 | 근거 |
|---|---|---|
| M14-1 냉각지방분해 | 하위 계열 없음(단일) | 원천 하위 1개 |

### M15 외용 관리 — 추천(한글 공식명 확인 안 됨 · 사용자 판단 D03 와 묶임)

- 문헌 이름: Topical cosmeceuticals
- 정의: 피부 표면에 바르거나 흡수시키는 외용 관리 — 코스메슈티컬·외용 의약품, 화학 박피, 이를 적용하는 클렌징·박리 기기(묶음 D03 를 받으면)
- 근거:
  - `literature-evidence.json#categories.M15.name` = Topical cosmeceuticals
  - `literature-evidence.json#categories.M15.moa[0]` “L-ascorbic acid acts as a cofactor for prolyl and lysyl hydroxylases in collagen synthesis and as a skin antioxidant.” (PMID 28805671)
  - `literature-evidence.json#categories.M15.moa[1]` “Topical retinoids bind to retinoic acid receptors in the skin, promoting cell turnover and increasing collagen production.” (PMID 34292058)
  - PMID 30550830 「Basic chemical peeling: Superficial and medium-depth peels.」 J Am Acad Dermatol 2019 — “Chemical peeling, or chemexfoliation …” (ESummary 확인)
  - PMID 19146604 「Hydradermabrasion: an innovative modality for nonablative facial rejuvenation.」 J Cosmet Dermatol 2008 — “Hydradermabrasion … combines crystal-free microdermabrasion with the pneumatic application of an antioxidant-based serum.” (ESummary 확인)
- 추천 이름: **외용 관리** (추천(한글 공식명 확인 안 됨 · 사용자 판단 D03 와 묶임)) — 문헌 M15 「Topical cosmeceuticals」 의 「topical(외용)」 · 원천 「메디컬스킨케어」·상담 「스킨케어」·「필링」은 동의어
- 동의어: 메디컬스킨케어 · 스킨케어 · 필링 · 코스메슈티컬 · Medical Skincare

| 원천 하위 | 처리 | 근거 |
|---|---|---|
| M15-1 케미컬필링 | 하위 계열 「화학 박피」 | 30550830(국제필링학회) 「Chemical peeling, or chemexfoliation」 · literature M15.moa 의 레티노이드·비타민C 외용 |
| M15-2 딥클렌징 · 물리필링(해면체 미세침) · 허벌 필링 | 하위 계열 「기계적 박리·클렌징」 | 19146604 hydradermabrasion · 15034813 microdermabrasion |
| 약물/토피컬(auto-1775361777) · 흉터 전용 중 실리콘·연고 | 하위 계열 「외용제」 | literature M15.moa[0]~[4] |
| M15-3 광치료(LED) | 다른 계열로(M8) — 사용자 판단 | 묶음 D04 |
| M15-6 주입장비 · 물광/메조건 | 다른 계열로(M4) | 묶음 D05 |
| M15-4 초음파관리 · M15-5 이온토포레시스 | M15 유지(흡수 보조 기기) — 사용자 판단 | 묶음 D09 · 26608060 transdermal sonophoresis |
| 탈모(비수술) · 여드름 전용 · 흉터 전용 | 해체 — 항목마다 해당 계열/5단계로(LLLT·LED→M8 · 두피 메조·엑소좀→M4/M5 · PRP→M5 · 아큐탄·스피로노락톤→계열 밖 · 서브시전·스테로이드 주사·면포압출·펀치→5단계 시술) | 탈모·여드름·흉터는 고민(7단계) — 「무엇을」이 아님 |
| 시그니처프로그램 · M15-7/M15-8 「추가」 · 도포/팩(빈 하위) | 6단계(패키지) / 해체 | 패키지 = 단위 시술 묶음 · 「추가」는 분류 기준 없음 |

### M16 정맥 영양 수액 — 추천(한글 공식명 확인 안 됨)

- 문헌 이름: Intravenous micronutrient / antioxidant therapy (aesthetic)
- 정의: 비타민·글루타치온·아미노산 같은 미량영양소·항산화제를 정맥으로 투여하는 시술
- 근거:
  - `literature-evidence.json#categories.M16.name` = Intravenous micronutrient / antioxidant therapy (aesthetic)
  - `literature-evidence.json#categories.M16.moa[0]` “Glutathione inhibits tyrosinase activity and shifts melanogenesis from eumelanin toward pheomelanin in cultured melanocytes.” (PMID 27088927)
  - `literature-evidence.json#categories.M16.effects[0]` “Intravenous glutathione for skin lightening is not supported by the US FDA or multiple national regulatory agencies and has insufficient high-quality efficacy evidence.” (PMID 27088927)
- 추천 이름: **정맥 영양 수액** (추천(한글 공식명 확인 안 됨)) — 문헌 M16 「Intravenous micronutrient / antioxidant therapy」 · 원천 「수액치료」·상담 「수액」·「백옥주사」 등은 동의어
- 동의어: 수액치료 · 수액 · 영양주사 · IV Therapy
- 메모: M16 정의에 맞는 제품 행은 1단계 원장에 0(정맥 수액 제품이 원장에 없음)

| 원천 하위 | 처리 | 근거 |
|---|---|---|
| M16-1~4 미백/항산화 · 피로회복 · 재생/면역 · 영양보충 | 6단계 목적으로(하위 계열 아님) | 목적 이름 |
| M16-DCA · M16-LIPO · 기타 지방분해주사(PPC) | 다른 계열로(새 계열 N1) — 사용자 판단 | 묶음 D01 |
| M16-new 기타(카복시 · 미녹시딜 두피 메조 · LDM · 성장호르몬 …) | 해체 — X2 · M4 · M15 · 계열 밖 / 마케팅명은 5단계 | 묶음 D10 · D02 |
| 태반주사(라엔넥 · 멜스몬) | 계열 밖 — 사용자 판단 | 묶음 D02 |

### M17 줄기세포·줄기세포 유래 제제 — 추천(한글 공식명 확인 안 됨)

- 문헌 이름: Stem cells and stem cell-derived products
- 정의: 줄기세포 또는 줄기세포에서 얻은 산물(배양액·추출 단백질)을 주입·도포하는 시술
- 근거:
  - `literature-evidence.json#categories.M17.name` = Stem cells and stem cell-derived products
  - `literature-evidence.json#categories.M17.adverse_effects[0]` “Unregulated stem cell products have caused serious adverse events including blindness after intra-ocular injection and tumor formation at ectopic sites.” (PMID 28296617)
- 추천 이름: **줄기세포·줄기세포 유래 제제** (추천(한글 공식명 확인 안 됨)) — 문헌 M17 「Stem cells and stem cell-derived products」 직역
- 동의어: 줄기세포치료 · 줄기세포 · 줄기세포 배양액 · Stem Cell Therapy

| 원천 하위 | 처리 | 근거 |
|---|---|---|
| M17-1 줄기세포배양액 · 자가혈유래 줄기세포 | 하위 계열 「배양액·추출물」 | 원천 설명(노바스템 · 미라셀 · AAPE)이 모두 「ADSC 배양액/추출 단백질」 — 「자가혈유래」 하위 이름과 설명이 충돌(원천 확인) |
| M17-2 SVF | 하위 계열 「세포(SVF)」 | 문헌 M17 「stem cells」 |
| M17-3 엑소좀 | 다른 계열로(M5) | 묶음 D08 |

### N1 지방분해 주사 — 새 계열 후보 — 사용자 판단(D01)

- 문헌 이름: Injection lipolysis (deoxycholic acid · cholic acid)
- 정의: 피하 지방층에 지방세포를 녹이는 약물(데옥시콜산 · 콜산)을 직접 주사해 국소 지방을 줄이는 시술
- 근거:
  - PMID 27785706 「Deoxycholic Acid: A Review in Submental Fat Contouring.」 Am J Clin Dermatol 2016 — “Deoxycholic acid is a secondary bile acid … that causes adipocyte lysis when injected into subcutaneous fat tissue.” (ESummary 확인)
  - PMID 38297988 「Lipolytic agents for submental fat reduction: Review.」 Skin Res Technol 2024 (ESummary 확인)
  - `step1-products.json 브이올렛 4_license.licenses[0].kpic.kpic_class` = Deoxycholic Acid : 피부/피하조직질환 > 기타 약물 > 기타
- 추천 이름: **지방분해 주사** (추천(한글 공식명 확인 안 됨)) — 상담 용어 · 원천 하위 「지방분해주사」 · 문헌 「injection lipolysis」·「lipolytic agents」 직역
- 동의어: DCA · 데옥시콜산 주사 · 윤곽주사 · 이중턱 주사 · 국소 지방분해주사 · 피하 지방분해주사 · 콜산(CA) 국소 지방분해제
- 초안: procedure-master-v3 X1 「지방분해주사」 = 이 후보

| 원천 하위 | 처리 | 근거 |
|---|---|---|
| 데옥시콜산 9 · 콜산 1(뉴비쥬) | 제품 속성(성분) | 허가 성분명(브이올렛주(데옥시콜산) · 뉴비쥬주(콜산)) |
| M16-LIPO 마케팅명(V라인주사 · 팻킬주사 …) · PPC | 5단계(시술 이름 · 성분 확인 후) | 제품이 아니라 메뉴명 — 1단계 D21·D24 규칙 |

## 5. 경계 판정 (B)

### D01 지방분해주사 10행(데옥시콜산 9 · 콜산 1) — 분리(새 계열 N1 「지방분해 주사」)

- 추천: M16 에서 빼 새 계열 N1 로 세운다
- 근거: ① 17 정의 어디에도 안 듦: M16 문헌은 「Intravenous micronutrient / antioxidant therapy」(정맥 · 영양소) — 지방분해주사는 피하 주사 · 지방세포 용해(27785706) ② 문헌에서 독립 분야: 27785706 「Deoxycholic Acid: A Review in Submental Fat Contouring」 · 38297988 「Lipolytic agents for submental fat reduction: Review」 — 두 조건 모두 충족(사용자 10-28 기준)
- 사용자 판단 이유: 계열 수를 17 → 18 로 늘리는 유일한 추천 — 「늘리는 것은 사용자 확정 기준을 둘 다 충족할 때만」이라 최종 판단은 사용자
- 대상: 브이올렛(`auto-M16-1775403016892`) · 벨카이라(`auto-M16-1775403024925`) · 벨라콜린(`auto-M16-1775403142279`) · 올리핏(`auto-M16-DCA-1775404043062`) · 펜카이라(`auto-M16-DCA-1775404043063`) · 바이블(`auto-M16-DCA-1775404043064`) · 밀리핏(`auto-M16-DCA-1775404043065`) · 원더브이(`auto-M16-DCA-1775404043066`) · 리포린(`auto-M16-DCA-1775404043067`) · 뉴비쥬(`auto-M16-DCA-1775404043068`)

### D02 시술이 아닌 의약품 3행(아큐탄 · 라이넥 · 멜스몬) — 계열 밖

- 추천: 계열을 주지 않고 「의약품(시술 계열 밖)」으로 둔다 — 제품 원장 행은 그대로(1단계 D32)
- 근거: 아큐탄 = 먹는 이소트레티노인(37649956) — 시술 아님 · 라이넥 KPIC 「간보호제」 · 멜스몬 「자하거추출물」 — M16 정의(미량영양소)에 안 들고 미용 독립 분야 문헌 확인 안 됨 → 새 계열 조건 미충족
- 사용자 판단 이유: 원천은 M15 · M16 에 두고 병원은 「태반주사」로 팔고 있음 — 추천에서 빠지는 결과라 사용자 확인
- 대상: 멜스몬(`auto-M16-1775364775098`) · 라이넥(`M16-3-1`) · 아큐탄(`auto-M15-1775361951923`)

### D03 M15 「외용 관리」 범위 — 화학 박피 38 · 기계적 박리·클렌징(하이드라더마브레이전 등) · 외용제 — 17 안(M15)

- 추천: 화학 박피와 하이드라더마브레이전을 새 계열로 떼지 않고 M15 하위 계열(「화학 박피」 「기계적 박리·클렌징」 「외용제」)로 둔다
- 근거: M15 문헌 정의 「Topical cosmeceuticals」 — 근거 진술이 레티노이드 · 비타민C 외용(literature M15.moa) · 화학 박피(30550830)와 하이드라더마브레이전(19146604 「pneumatic application of … serum」)도 피부 표면에 약제를 적용 → 「17 어디에도 안 듦」 조건이 성립 안 함. 다만 화학 박피는 별도 학회(International Peeling Society, 30550830 저자) 문헌이 있어 독립 분야 조건은 충족 — 한쪽만 충족이라 분리 추천 안 함
- 사용자 판단 이유: 원천 개발 당시 문헌 카테고리에 「Chemical peeling」이 따로 있었던 흔적(clinical-review.md 「M13 Chemical peeling」 오매칭 처리)이 있어 분리 여부가 경계선
- 대상: 알라딘필링(`M15-1-3`) · 블랙필(`M15-1-4`) · 핑크필(`M15-1-6`) · 라라필(`M15-1-7`) · 호박필(`auto-46-1774737181584`) · 밀크필(`auto-47-1774737181584`) · 닥토필(`auto-M15-1775361455669`) · 미라필링(`auto-M15-1775364775115`) · 블랙필링(`auto-M15-1775364775116`) · 옐로우필링(`auto-M15-1775364775117`) · 솔코세릴필링(`auto-M15-1775364775118`) · 여우필(`auto-M15-1775401624105`) · 플라필(`auto-M15-1775401631147`) · 산소필(`auto-M15-1775401638316`) · PRX필(`auto-M15-1775401645338`) · CO2필(`auto-M15-1775401653479`) · 예스필(`auto-M15-1775401662170`) · 해초필(`auto-M15-1775401677251`) · 그린필(`auto-M15-1775401685107`) · 퀸즈필(`auto-M15-1775401692083`) · 살몬필(`auto-M15-1775401700008`) · 미라클필링(`auto-M15-1775401716456`) · FCR필(`auto-M15-1775401722628`) · 디멜라필(`auto-M15-1775401738092`) · 생크림필(`auto-M15-1775401745461`) · 우유필(`auto-M15-1775401753203`) · 베이비필(`auto-M15-1775401760736`) · 골드필(`auto-M15-1775401767756`) · 마꾸필(`auto-M15-1775401773800`) · 라라닥터(`auto-M15-1775401788467`) · 크랜베리필(`auto-M15-1775402057372`) · 체리필(`auto-M15-1775402064126`) · ASA필(`auto-M15-1775402078232`) · 탄앤막필링(`auto-M15-1775402083474`) · 이지피틱필(`auto-M15-1775402093377`) · 아미노필(`auto-M15-1775402100474`) · 쿰스필(`auto-M15-1775402107402`) · 진주필(`auto-M15-1775402113508`) · 콜라겐필(`auto-M15-1775402120118`) · 아쿠아필(`M15-2-1`) · 하이드라페이셜(`M15-2-2`) · 옥시덤(`auto-M15-1775362958625`) · 제트필(`auto-M15-1775362965286`) · 아쿠아퓨어(`auto-M15-1775362971889`) · 실크필(`auto-M15-1775362978512`) · 소노퀸(`auto-M15-1775364775167`) · 벨라소닉(`M15-6-4`) · 제네오X(`auto-M15-1775402654237`) · 힐퓨전 프로(`new-DEV-044`) · 크라이오 멀티마스터(`new-DEV-045`) · 오투덤(`new-DEV-049`) · 소노케어(`new-DEV-056`) · 콘투락투벡스(`auto-M15-1775364775171`)

### D04 LED 광치료 6행 + 현장 오메가라이트 1행 — 17 안(M8 로 옮김)

- 추천: M15 → M8 로 옮기고 M8 정의를 「레이저·IPL·LED(광)」로 넓힌다
- 근거: LED 는 바르는 관리가 아니라 광원(M15 정의 밖) · 40751922 「LED therapy employs narrow-spectrum, incoherent light」 — IPL 처럼 비간섭광 · 원천 M8 영문 「Laser & Light」. 문헌 M8 이름은 「lasers and IPL」로 LED 를 명시하지 않음 · LED 독립 문헌(33471046 · 40751922)이 있어 분리도 가능
- 사용자 판단 이유: M8 정의를 문헌 이름보다 넓히는 판단(대안: 새 계열 「광생물조절(LED)」 — 17 밖 + 독립 문헌 둘 다 성립)
- 대상: 옴니룩스(`M15-3-1`) · 힐라이트(`M15-3-2`) · 아스트로돔(`auto-49-1774737181584`) · 셀라이트(`auto-M15-1775362992228`) · 데마루치(`auto-M15-1775362998455`) · 바이오프로톤(`auto-M15-1775364775179`) · 오메가라이트(`new-DEV-043`)

### D05 주입 기기 7행(큐어젯 · 미라젯 · 에어젯 · 노보젯 · 하이쿡스 · 더마샤인 · 비타인젝터) — 17 안(M4 로 옮김)

- 추천: M15 → M4(스킨부스터)의 제품(기기)으로. 「어떻게」(무바늘 제트 · 멀티니들)는 4단계 기법
- 근거: M4 근거 문헌 39544509 의 Delivery Methods 절이 「Needle-free Jet Injectors」와 「automatic injector」를 스킨부스터 전달 방법으로 다루고 큐어젯을 직접 예로 듦 · 하이쿡스 · 더마샤인 허가 「전동식 의약품 주입 펌프」
- 대상: 큐어젯(`M15-6-2`) · 미라젯(`M15-6-3`) · 하이쿡스(`auto-50-1774737181584`) · 더마샤인(`auto-51-1774737181584`) · 에어젯(`auto-M15-1775360527416`) · 노보젯(`auto-M15-1775360904089`) · 비타인젝터(`auto-M15-1775361179297`)

### D06 콜라겐 주입제 4행(콜라쥬 · 레티젠 · 미라콜 · 콜라겐핀) — 17 안(M3 → M4)

- 추천: M3 → M4 하위 「콜라겐」(M4 원천 콜라겐/신규 3행과 합침)
- 근거: M3 문헌 정의는 미립자 이물반응형(PLLA/CaHA/PDLLA/PCL) · 콜라겐은 「직접 볼륨·구조」(원천 설명) · 39544509 Collagen 절이 레티젠(LAETIGEN)을 피부 질 개선용 진피 주입제로 예시
- 대상: 콜라쥬(`auto-13-1774737181584`) · 레티젠(`auto-14-1774737181584`) · 미라콜(`auto-15-1774737181584`) · 콜라겐핀(`auto-M3-1775364775146`)

### D07 무세포동종진피(hADM) 6행 — 17 안(M3 → M4)

- 추천: M3 → M4(스킨부스터)
- 근거: 원천 설명 「hADM ECM 스킨부스터」 「콜라겐 생성을 ‘유도’하는 것이 아니라 … ‘직접 보충’」 — M3 정의(collagen-stimulating)와 반대 · M4 정의 「various biological materials」에는 들지만 hADM 을 직접 다룬 문헌은 이번에 확인 안 됨
- 사용자 판단 이유: 문헌 근거가 정의 일반론뿐이고 원천은 M3 에 둠 — 인체조직 제품이라 다른 주입제와 성격도 다름
- 대상: 리투오(`auto-17-1774737181584`) · 리투오 파인(`auto-18-1774737181584`) · 셀르디엠(`auto-19-1774737181584`) · 쥬브아셀(`auto-20-1774737181584`) · 아디떼(`auto-21-1774737181584`) · 도프ECM(`auto-M3-hADM-1775404146754`)

### D08 엑소좀 5행(ASCE+ · 셀엑소좀 · 카탈리스트 · 드원셀 · EXOSOME SKIN) — 17 안(M5)

- 추천: 엑소좀은 M5 하위 「엑소좀」 — M4 의 4행 옮김, EXOSOME SKIN 은 이미 M5. 줄기세포 배양액·추출물은 M17 유지
- 근거: 문헌 M5 이름 「Platelet-rich plasma (PRP) and exosome therapies」 + exosome moa 2건 · M4 문헌(39544509)은 exosome 0건 · M17 「stem cell-derived products」와 겹치지만 이름에 exosome 을 명시한 쪽이 M5
- 대상: ASCE+엑소좀(`M4-3-1`) · 셀엑소좀(`auto-M4-1775361371619`) · 카탈리스트(`auto-M4-1775364775151`) · 드원셀(`auto-M4-1775364775155`) · EXOSOME SKIN(`M5-P-4`)

### D09 초음파·이온 흡수 보조 기기(LDM · 벨라소닉 · 소노케어 · 크라이오 멀티마스터 + 트윈픽셀 보조) — 17 안(M15)

- 추천: M15 「외용 관리」 안에 둔다(외용제 흡수를 돕는 기기)
- 근거: 허가 「초음파자극기」(비집속 — HIFU 인 「집속형초음파자극시스템」과 품목이 다름) · 원천 LDM 「각질층의 수분 흡수율 증가」 · 26608060 「transdermal sonophoresis」 — 외용 전달 보조. 독립 미용 분야 문헌은 확인 안 됨
- 사용자 판단 이유: M15 를 「바르는 약제」에서 「바르는 약제 + 흡수 보조 기기」로 넓히는 판단(대안: 계열 밖)
- 대상: 트윈픽셀(`auto-M11-1775360510687`) · LDM(`M15-4-1`) · 벨라소닉(`M15-6-4`) · 크라이오 멀티마스터(`new-DEV-045`) · 소노케어(`new-DEV-056`)

### D10 procedure-master-v3 X1~X6(워커 초안 · 확정 아님) — X1 분리 / X2 분리 후보 / X3 17 안(M4) / X4 계열 밖 / X5 계열 밖 / X6 17 안(M9)

- 추천: X1 → N1(D01) · X2 카복시 → 새 계열 후보 N2 · X3 미녹시딜 두피 메조 → M4 · X4 성장호르몬 → 계열 밖 · X5 태반제제 → 계열 밖(D02) · X6 RF 지방감소 → M9(D11)
- 근거: X2: 35124882 「Carboxytherapy, defined as the administration of carbon dioxide」 체계적 문헌고찰 — 17 정의 어디에도 안 들고 독립 문헌 있음(두 조건 충족) · X3: M4 문헌 이름 「mesotherapy」 · X4: 전신 호르몬 주사 — 17 밖, 미용 독립 문헌 확인 안 됨 · X5: D02 · X6: D11
- 사용자 판단 이유: X2 는 새 계열 추천 두 번째 — 제품 행은 트리필 프로 1행(판단 필요)뿐이고 나머지는 5단계 단위 시술(카복시테라피)
- 대상: 트루스컬프트(`auto-M10-1775363013079`) · 멜스몬(`auto-M16-1775364775098`) · 브이올렛(`auto-M16-1775403016892`) · 벨카이라(`auto-M16-1775403024925`) · 벨라콜린(`auto-M16-1775403142279`) · 올리핏(`auto-M16-DCA-1775404043062`) · 펜카이라(`auto-M16-DCA-1775404043063`) · 바이블(`auto-M16-DCA-1775404043064`) · 밀리핏(`auto-M16-DCA-1775404043065`) · 원더브이(`auto-M16-DCA-1775404043066`) · 리포린(`auto-M16-DCA-1775404043067`) · 뉴비쥬(`auto-M16-DCA-1775404043068`) · 트리필 프로(`new-DEV-052`) · 라이넥(`M16-3-1`)

### D11 비침습 지방 감소 기기 5행(트루스컬프트 · 바넥스 · 바넥스프로 · 바이캐빈 · 슬렌더엑스) — 17 안(에너지 계열)

- 추천: 새 계열 「비침습 지방 감소」를 세우지 않고 에너지대로 둔다 — RF → M9, 레이저 → M8, 근육 자극 겸용 → M10. 지방 감소는 6단계 목적 엣지. v3 X6 폐지
- 근거: 계열 = 「무엇을(약제·장비)」(_RESUME §2 10-27) · 31168833 비침습 체형 기기를 cryolipolysis · laser · HIFEM · RF · HIFU 로 나눔 — 각 에너지가 이미 M14 · M8 · M10 · M9 에 있음 → 「17 어디에도 안 듦」 불성립. 바넥스(원천 M14)는 설명이 RF+석션이라 M9
- 사용자 판단 이유: M9 정의가 문헌상 「타이트닝」이라 RF 지방 감소를 넣으면 이름(리프팅)과 용도가 어긋남 · v3 X6 은 1차 답 ③ 에서 나온 것
- 대상: 슬렌더엑스(`auto-M8-1775362619619`) · 바이캐빈(`auto-M9-1775364775136`) · 바넥스프로(`auto-M10-1775361916636`) · 트루스컬프트(`auto-M10-1775363013079`) · 바넥스(`auto-M14-1775361047443`)

### D12 진단 장비 4행(미라쥬 · 3D 메타뷰 · 마크뷰 · 스케나) — 계열 밖

- 추천: 시술 계열을 주지 않고 1단계대로 「진단 장비」 노드
- 근거: 치료가 아니라 측정·촬영(허가 「체외형 의료용 카메라」 · web4) — 시술 = 무엇을 × 어디에 × 어떻게의 「무엇을」이 아님
- 대상: 미라쥬(`new-DEV-071`) · 3D 메타뷰(`new-DEV-072`) · 마크뷰(`new-DEV-073`) · 스케나(`new-DEV-074`)

### D13 다른 계열끼리 합친 4건(하모니카 · 볼뉴머 · LDM · 아포지 엘리트 플러스) — 대표 행 계열 확정

- 추천: 하모니카 = 여러 계열(주 M2 · 보조 M3) · 볼뉴머 = M9 · LDM = M15(D09) · 아포지 엘리트 플러스 = M8
- 근거: 합쳐진 원천 행의 설명 · 허가 품목 대조(행 상세)
- 대상: 하모니카(`auto-M2-1775360655397`) · 아포지 엘리트 플러스(`auto-36-1774737181584`) · 볼뉴머(`M9-2-3`) · LDM(`M15-4-1`)

### D14 계열 없는 현장 기기 29행 — 계열 부여

- 추천: 허가 품목명으로 부여 — 엔디야그·반도체·레이저 조사기 11 → M8 · 범용전기수술기 3 + 집속형초음파 3 + HIFU 미용기기 1 → M9 · 의약품 흡수 유도 피부 자극기 1 → M12 · 하이드로더마브레이전 · 산소 · 흡수 보조 4 → M15 · LED 1 → M8(D04) · EMS+RF 1 → 여러(M10) · 판단 필요 3(이브타이탄 · 벨르업 · 더마큐어) · 카복시 장비 1(트리필 프로, D10)
- 근거: 1단계 허가 품목(4_license.licenses[].item) · web4 출처(1_identity.basis)
- 대상: 덴서티 하이(`new-DEV-013`) · 이브타이탄(`new-DEV-015`) · 이래비티(`new-DEV-018`) · 엔진(`new-DEV-020`) · 세르프(`new-DEV-021`) · 덴서티(`new-DEV-024`) · 리니어지(`new-DEV-027`) · 울핏(`new-DEV-031`) · 벨르업(`new-DEV-034`) · 스텔라듀오(`new-DEV-039`) · 더마큐어(`new-DEV-042`) · 오메가라이트(`new-DEV-043`) · 힐퓨전 프로(`new-DEV-044`) · 크라이오 멀티마스터(`new-DEV-045`) · 울킨(`new-DEV-047`) · 오투덤(`new-DEV-049`) · 트리필 프로(`new-DEV-052`) · 오토 MTS(`new-DEV-053`) · 소노케어(`new-DEV-056`) · 브라이톤(`new-DEV-058`) · 피코라이트 블랙(`new-DEV-060`) · 피코라이트(`new-DEV-061`) · 큐라스(`new-DEV-063`) · 헬리오스 3(`new-DEV-065`) · 피코케이(`new-DEV-067`) · 피콜로 프리미엄(`new-DEV-068`) · 아톰(`new-DEV-069`) · 카프리(`new-DEV-075`) · 아큐토닝(`new-DEV-076`)

### D15 복합 장비 15행(두 계열 에너지·재료) — 여러 계열

- 추천: 주 계열 1 + 보조 계열 — 주 = 허가 품목 · 원천 위치 · 설명 첫 원리 순으로
- 근거: 행 상세 — 시너론 아이플러스 · 로제라이트 · 이맥스 · 스마트자이드(M8+M9) · 시크릿맥스 · 포커스듀얼(M9+M11) · 트라이리프트(M9+M10) · 엠페이스 · 엠스컬프트 네오 · 이볼브 · 스팀슈어(M10+M9) · 비바체(M11+M8) · 트윈픽셀(M11+M15) · 라라젯(M15+M4) · 바이리즌(M4+M2) — 하모니카 · 바넥스프로 · 엔진은 D13 · D11 · D14
- 대상: 바이리즌(`auto-M4-1775361378128`) · 시너론 아이플러스(`auto-M8-1775362594611`) · 이맥스(`auto-M8-1775361417735`) · 스마트자이드(`auto-M8-1775364775123`) · 로제라이트(`auto-M8-1775364797146`) · 시크릿맥스(`auto-M9-1775363058909`) · 트라이리프트(`auto-M9-1775364775131`) · 포커스듀얼(`auto-M9-1775360610416`) · 엠페이스(`M10-1-1`) · 엠스컬프트 네오(`M10-2-2`) · 이볼브(`auto-M10-1775363005172`) · 스팀슈어(`auto-M10-1775364775185`) · 트윈픽셀(`auto-M11-1775360510687`) · 비바체(`auto-M11-1775361447933`) · 라라젯(`auto-48-1774737181584`)

### D16 개별 옮김·판단 4행(신펄 · 올타이트 · 헤어셀 · 알렉스필) — 신펄 M2→M3 · 올타이트 M15→M9 · 헤어셀 계열 밖(추천) · 알렉스필 원천 확인

- 추천: 신펄 → M3(PLLA) · 올타이트 → M9 · 헤어셀 · 알렉스필은 판단 필요로 두고 원천 확인
- 근거: 행 상세
- 대상: 알렉스필(`auto-M15-1775401780659`) · 헤어셀(`auto-M15-1775364775178`) · 올타이트(`auto-M15-1775402736453`) · 신펄(`M2-P-7`)

### D17 계열 이름 한글 추천 16(M1 확정 제외) + N1 — 이름 추천

- 추천: 문헌 영문 이름을 기준으로 한 한글 이름(A 표) — 한글 공식 출처를 찾은 것은 M2 「성형용 필러」(동의어) · M7 「안면조직고정용실」(식약처 품목) 정도, 나머지는 「확인 안 됨」
- 근거: _RESUME §2 10-27 「계열 이름 = 공식 일반명」 — 공식 일반명이 국내 출처로 확인 안 된 계열이 다수
- 사용자 판단 이유: 공식 일반명 규칙을 그대로 지키면 이름을 못 정하는 계열이 생김 — 문헌 직역으로 둘지 사용자 판단

### D18 하위 계열 처리 규칙(17계열 공통) — 규칙

- 추천: 수입/국산 · 브랜드 → 제품 속성/제품 · 재질(M2·M3·M4·M7) · 광원/방식(M8) · 에너지(M9·M10) → 하위 계열 · 형태(M7) · 기구 형태(M12) → 제품 속성 · 용도별(M1-3)·부위(M10 페이셜/바디)·목적(M8 색소·혈관·제모 · M16 미백·피로) → 5·3·6단계 · 시그니처 프로그램 → 6단계 패키지 · 「기타」「추가」 → 해체
- 근거: A 표 계열별 sub_families · _RESUME §2 10-27 시술 = 무엇을 × 어디에 × 어떻게

## 6. 행별 상세 (C)

추천 계열(주) 순. 「현재」 = step1 `family.name`. 「auto」 = 자동 추가 행.

### M1 보툴리눔 톡신 — 19행

| ledger_id | 이름 | auto | 현재 | 판정 | 보조 계열 | 근거 | 메모 |
|---|---|---|---|---|---|---|---|
| `M1-2-1` | 보톡스 |  | M1 보톡스 | 맞음 |  | 원천 M1 › 수입 「오리지널 보톡스, 900kDa 복합체 제형」 · 허가 품목 「전문의약품」 ↔ M1 정의 |  |
| `M1-2-3` | 디스포트 |  | M1 보톡스 | 맞음 |  | 원천 M1 › 수입 「클로스트리디움 보툴리눔 A형 독소 기반의 신경독소 제품으로, 광범위한 확산을 특징으로 하는 보톡스 시술용 제제입니다.」 · 허가 품목 「전문의약품」 ↔ M1 정의 |  |
| `M1-2-2` | 제오민 |  | M1 보톡스 | 맞음 |  | 원천 M1 › 수입 「150kDa 순수 보툴리눔 톡신 A로 안면 주름 개선 및 근육 이완 치료제」 · 허가 품목 「전문의약품」 ↔ M1 정의 |  |
| `auto-M1-1775360538524` | 다복스 | ○ | M1 보톡스 | 맞음 |  | 원천 M1 › 수입 「장기 지속형 보툴리눔 독소로 기존 제품 대비 효과 지속 기간이 연장된 신제제이다.」 ↔ M1 정의 |  |
| `M1-1-1` | 보툴렉스 |  | M1 보톡스 | 맞음 |  | 원천 M1 › 국산 「Clostridium botulinum Type A 독소를 기반으로 한 신경근 차단제로, 표정근 주름 개선 및 얼굴 윤곽 시술」 · 허가 품목 「전문의약품」 ↔ M1 정의 |  |
| `M1-1-2` | 나보타 |  | M1 보톡스 | 맞음 |  | 원천 M1 › 국산 「Clostridium botulinum Type A 독소를 정제한 신경독소로, 근육의 수축을 일시적으로 억제하여 주름 개선 및」 · 허가 품목 「전문의약품」 ↔ M1 정의 |  |
| `M1-1-4` | 메디톡신 |  | M1 보톡스 | 맞음 |  | 원천 M1 › 국산 「클로스트리디움 보툴리눔 A형 독소의 900kDa 복합체로 구성된 신경독소로, 근육 수축을 억제하여 주름 개선 효과를 제공하는 」 · 허가 품목 「전문의약품」 ↔ M1 정의 |  |
| `M1-1-3` | 코어톡스 |  | M1 보톡스 | 맞음 |  | 원천 M1 › 국산 「순수 보툴리눔 톡신 150kDa 단일 성분으로 제작된 프리미엄 보톡스 제품」 · 허가 품목 「전문의약품」 ↔ M1 정의 |  |
| `M1-1-5` | 이노톡스 |  | M1 보톡스 | 맞음 |  | 원천 M1 › 국산 「Clostridium botulinum Type A 독소를 정제한 근육이완제로, 표정주름 개선 및 얼굴 윤곽 시술에 사용되는 」 · 허가 품목 「전문의약품」 ↔ M1 정의 |  |
| `auto-1-1774737181584` | 더톡신 | ○ | M1 보톡스 | 맞음 |  | 원천 M1 › 국산 「클로스트리디움 보툴리눔 A형 독소를 기반으로 한 신경독소 미용시술 제품으로, 근육의 수축을 억제하여 주름 개선 효과를 제공합니」 · 허가 품목 「전문의약품」 ↔ M1 정의 |  |
| `M1-1-6` | 원더톡스 |  | M1 보톡스 | 맞음 |  | 원천 M1 › 국산 「Clostridium botulinum Type A 독소 기반의 신경독소로, 근육의 과도한 수축을 완화하여 주름 개선 및 얼굴」 · 허가 품목 「전문의약품」 ↔ M1 정의 |  |
| `M1-1-7` | 리즈톡스 |  | M1 보톡스 | 맞음 |  | 원천 M1 › 국산 「Clostridium botulinum Type A 독소를 유효성분으로 하는 근육이완제로, 표정주름 개선 및 미용 목적의 주사」 · 허가 품목 「전문의약품」 ↔ M1 정의 |  |
| `auto-M1-1775362455497` | 비비톡신 | ○ | M1 보톡스 | 맞음 |  | 원천 M1 › 국산 「휴메딕스의 보툴리눔 독소 A 제제로 근육 이완을 통한 주름 개선 및 과다 발한 치료용 미용의학 제품」 · 허가 품목 「전문의약품」 ↔ M1 정의 |  |
| `auto-M1-1775362462896` | 톡스온 | ○ | M1 보톡스 | 맞음 |  | 원천 M1 › 국산 「보툴리눔 톡신 후보 제품으로 기재됨(자동 수집 데이터). 허가 상태·임상 데이터는 별도 검증 필요」 · 허가 품목 「전문의약품」 ↔ M1 정의 |  |
| `auto-M1-1775364775101` | 센독스 | ○ | M1 보톡스 | 맞음 |  | 원천 M1 › 국산 「메디콕스에서 개발한 A형 보툴리눔 독소로 주름 개선 및 근육 이완 효과 제공」 ↔ M1 정의 |  |
| `auto-M1-1775364775102` | 보리톡스 | ○ | M1 보톡스 | 맞음 |  | 원천 M1 › 국산 「보령제약에서 제조한 국산 보툴리눔 독소로 안전성과 효과가 검증된 주름 개선 제품」 ↔ M1 정의 |  |
| `auto-M1-1775364775103` | 퓨어녹스 | ○ | M1 보톡스 | 맞음 |  | 원천 M1 › 국산 「대화제약에서 개발한 순수 보툴리눔 독소로 높은 순도와 안정성을 자랑하는 제품」 ↔ M1 정의 |  |
| `M1-P-8` | 티엠버스 |  | M1 보톡스 | 맞음 |  | 원천 M1 › products 「Clostridium botulinum Type A 독소 기반의 신경독소 주입제로, 표정근의 수축을 억제하여 주름 개선 효과를」 · 허가 품목 「전문의약품」 ↔ M1 정의 |  |
| `M1-P-9` | 뉴럭스 |  | M1 보톡스 | 맞음 |  | 원천 M1 › products 「Clostridium botulinum Type A 독소를 주성분으로 하는 신경근 차단제로, 근육 수축을 억제하여 주름 개선 」 ↔ M1 정의 |  |

### M2 필러 — 29행

| ledger_id | 이름 | auto | 현재 | 판정 | 보조 계열 | 근거 | 메모 |
|---|---|---|---|---|---|---|---|
| `M2-1-5` | 이브아르 |  | M2 필러 · 국산 HA | 맞음 |  | 원천 M2 › 국산 HA 「LG화학 HA 필러, 중간 탄성」 · 허가 품목 「조직 수복용 생체 재료 · 조직수복용생체재료」 ↔ M2 정의 |  |
| `M2-1-8` | 엘라비에 |  | M2 필러 · 국산 HA | 맞음 |  | 원천 M2 › 국산 HA 「휴메딕스 HA 필러, 가벼운 질감」 · 허가 품목 「조직 수복용 생체 재료 · 조직수복용생체재료」 ↔ M2 정의 |  |
| `M2-1-2` | 더채움 |  | M2 필러 · 국산 HA | 맞음 |  | 원천 M2 › 국산 HA 「휴젤 HA 필러, 높은 응집력」 · 허가 품목 「조직수복용생체재료」 ↔ M2 정의 |  |
| `M2-1-1` | 뉴라미스 |  | M2 필러 · 국산 HA | 맞음 |  | 원천 M2 › 국산 HA 「메디톡스 HA 필러, 다층 라인업」 · 허가 품목 「조직수복용생체재료」 ↔ M2 정의 |  |
| `M2-1-3` | 벨라스트 |  | M2 필러 · 국산 HA | 맞음 |  | 원천 M2 › 국산 HA 「동국제약 HA 필러, 중간 입자」 · 허가 품목 「조직수복용생체재료」 ↔ M2 정의 |  |
| `M2-1-4` | 에피티크 |  | M2 필러 · 국산 HA | 맞음 |  | 원천 M2 › 국산 HA 「제테마 HA 필러, 높은 순도」 · 허가 품목 「조직수복용생체재료」 ↔ M2 정의 |  |
| `M2-1-6` | 아띠에르 |  | M2 필러 · 국산 HA | 맞음 |  | 원천 M2 › 국산 HA 「메디톡스 HA 필러, 안정화 기술」 · 허가 품목 「조직수복용생체재료」 ↔ M2 정의 |  |
| `M2-1-7` | 리쥬비엘 |  | M2 필러 · 국산 HA | 맞음 |  | 원천 M2 › 국산 HA 「파마리서치 HA 필러, 부드러운 질감」 · 허가 품목 「조직수복용생체재료」 ↔ M2 정의 |  |
| `auto-8-1774737181584` | 셀레스텔라 | ○ | M2 필러 · 국산 HA | 맞음 |  | 원천 M2 › 국산 HA 「더에쓰씨 HA 필러, 프리미엄 라인」 · 허가 품목 「조직수복용생체재료」 ↔ M2 정의 |  |
| `auto-9-1774737181584` | 유스필 | ○ | M2 필러 · 국산 HA | 맞음 |  | 원천 M2 › 국산 HA 「알에프바이오 HA 필러, 톤 밝히기」 · 허가 품목 「조직 수복용 생체 재료 · 조직수복용생체재료」 ↔ M2 정의 |  |
| `auto-M2-1775361463441` | 큐젤 | ○ | M2 필러 · 국산 HA | 맞음 |  | 원천 M2 › 국산 HA 「국산 히알루론산 기반 진피 필러로 주름 개선 및 볼륨 증강에 사용되는 미용시술용 제품」 · 허가 품목 「조직수복용생체재료」 ↔ M2 정의 |  |
| `auto-M2-1775361728731` | 큐젤 맥스 | ○ | M2 필러 · 국산 HA | 맞음 |  | 원천 M2 › 국산 HA 「히알루론산 기반 하이드로리프팅 필러로 수분공급과 동시에 자연스러운 볼륨감을 제공하는 물광주사용 제품」 · 허가 품목 「조직수복용생체재료」 ↔ M2 정의 | 원천 「물광주사용」 설명이나 허가는 큐젤 필러 라인 품목(CUTEGEL Max 1400 Lidocaine) — 허가 기준 M2 |
| `auto-M2-1775361736267` | 큐티필 | ○ | M2 필러 · 국산 HA | 맞음 |  | 원천 M2 › 국산 HA 「에스테팜에서 개발한 국산 히알루론산 필러로 주름 개선과 볼륨 증대에 사용되는 미용의학 제품」 · 허가 품목 「조직 수복용 생체 재료」 ↔ M2 정의 |  |
| `auto-M2-1775364775104` | 에피로크 | ○ | M2 필러 · 국산 HA | 맞음 |  | 원천 M2 › 국산 HA 「국산 히알루론산 필러로 자연스러운 볼륨 증가와 주름 개선 효과 제공」 ↔ M2 정의 |  |
| `auto-M2-1775364775105` | 앨리필 | ○ | M2 필러 · 국산 HA | 맞음 |  | 원천 M2 › 국산 HA 「국산 히알루론산 기반 필러로 자연스러운 볼륨감과 우수한 지속력 제공」 ↔ M2 정의 |  |
| `auto-M2-1775364775106` | 메테로 | ○ | M2 필러 · 국산 HA | 맞음 |  | 원천 M2 › 국산 HA 「한국비엔씨에서 개발한 히알루론산 필러로 안정적인 볼륨 보정과 자연스러운 결과 제공」 ↔ M2 정의 |  |
| `auto-M2-1775364775107` | 엘라비에 프리미어 | ○ | M2 필러 · 국산 HA | 맞음 |  | 원천 M2 › 국산 HA 「휴메딕스프리미엄에서 제조한 고급 히알루론산 필러로 프리미엄 볼륨 개선 효과 제공」 · 허가 품목 「조직 수복용 생체 재료 · 조직수복용생체재료」 ↔ M2 정의 |  |
| `auto-M2-1775364775108` | 더채움 프리미엄 | ○ | M2 필러 · 국산 HA | 맞음 |  | 원천 M2 › 국산 HA 「휴젤프리미엄에서 개발한 최고급 히알루론산 필러로 뛰어난 지속성과 자연스러운 결과 보장」 · 허가 품목 「조직수복용생체재료」 ↔ M2 정의 |  |
| `M2-2-1` | 쥬비덤 |  | M2 필러 · 수입 HA | 맞음 |  | 원천 M2 › 수입 HA 「앨러간 HA 필러, 글로벌 스탠다드」 · 허가 품목 「조직 수복용 생체 재료 · 조직수복용생체재료」 ↔ M2 정의 |  |
| `M2-2-2` | 레스틸렌 |  | M2 필러 · 수입 HA | 맞음 |  | 원천 M2 › 수입 HA 「갈더마 HA 필러, 브래드마크 제품」 · 허가 품목 「조직 수복용 생체 재료 · 조직수복용생체재료」 ↔ M2 정의 |  |
| `M2-2-3` | 벨로테로 |  | M2 필러 · 수입 HA | 맞음 |  | 원천 M2 › 수입 HA 「동적 교차결합 HA 필러」 · 허가 품목 「조직수복용생체재료」 ↔ M2 정의 |  |
| `M2-2-4` | 테오시알 |  | M2 필러 · 수입 HA | 맞음 |  | 원천 M2 › 수입 HA 「테옥산 교차결합 HA 필러」 · 허가 품목 「조직 수복용 생체 재료」 ↔ M2 정의 |  |
| `M2-2-5` | 퍼펙타 |  | M2 필러 · 수입 HA | 맞음 |  | 원천 M2 › 수입 HA 「프랑스산 HA 필러」 · 허가 품목 「조직수복용생체재료」 ↔ M2 정의 |  |
| `M2-2-6` | 아말리안 |  | M2 필러 · 수입 HA | 맞음 |  | 원천 M2 › 수입 HA 「독일산 고강도 HA 필러」 · 허가 품목 「조직 수복용 생체 재료」 ↔ M2 정의 |  |
| `auto-M2-1775360655397` | 하모니카 | ○ | M2 필러 · 수입 HA | 여러 계열 | M3 | 원천 M2-2 「Vycross HA」 + 합쳐진 원천 M3-2 HArmonyCa(auto-M3-1775364775147 · CaHA) — HA 겔 + CaHA 복합. 주 = 필러(대표 행이 M2) · 보조 = M3 CaHA |  |
| `auto-M2-1775362470502` | 프린세스 | ○ | M2 필러 · 수입 HA | 맞음 |  | 원천 M2 › 수입 HA 「오스트리아 크로마비전사의 순수 비가교 히알루론산 필러로 자연스러운 볼륨감과 수분 공급에 특화된 제품」 · 허가 품목 「조직수복용생체재료」 ↔ M2 정의 | 원천 설명 「순수 비가교 HA」는 허가 품목명(Princess Filler · Princess Volume)과 충돌 — 원천 설명 확인 대상 |
| `auto-M2-1775362477273` | 스타일에이지 | ○ | M2 필러 · 수입 HA | 맞음 |  | 원천 M2 › 수입 HA 「프랑스 비비안비社의 모노페이직 히알루론산 필러로 자연스러운 볼륨 개선과 주름 완화에 사용」 · 허가 품목 「조직 수복용 생체 재료 · 조직수복용생체재료」 ↔ M2 정의 |  |
| `auto-M2-1775364775109` | 아테콜 | ○ | M2 필러 · 비HA 필러 | 맞음 |  | 원천 M2 › 비HA 필러 「PMMA 기반 영구 필러로 반영구적인 볼륨 증가와 윤곽 개선 효과 제공」 · 허가 품목 「조직 수복용 생체 재료」 ↔ M2 정의 |  |
| `auto-M2-1775364775110` | 아쿠아미드 | ○ | M2 필러 · 비HA 필러 | 맞음 |  | 원천 M2 › 비HA 필러 「폴리아크릴아미드겔 기반의 반영구 볼륨 필러」 ↔ M2 정의 |  |

### M3 바이오스티뮬레이터 — 14행

| ledger_id | 이름 | auto | 현재 | 판정 | 보조 계열 | 근거 | 메모 |
|---|---|---|---|---|---|---|---|
| `M3-1-1` | 스컬트라 |  | M3 바이오스티뮬레이터/콜라겐부스터 · PLLA (폴리-L-락틱산) | 맞음 |  | 원천 M3 › PLLA (폴리-L-락틱산) 「PLLA 기반 콜라겐 부스터」 · 허가 품목 「조직수복용재료」 ↔ M3 정의 |  |
| `auto-10-1774737181584` | 올리디아 | ○ | M3 바이오스티뮬레이터/콜라겐부스터 · PLLA (폴리-L-락틱산) | 맞음 |  | 원천 M3 › PLLA (폴리-L-락틱산) 「PRP사이언스 PLLA 기반 바이오스티뮬레이터」 · 허가 품목 「조직 수복용 재료」 ↔ M3 정의 |  |
| `auto-11-1774737181584` | 에스테필 | ○ | M3 바이오스티뮬레이터/콜라겐부스터 · PDLLA (폴리-D,L-락틱산) | 맞음 |  | 원천 M3 › PLLA (폴리-L-락틱산) 「PDLLA(폴리디엘락틱애시드) 미립자 기반의 생분해성 콜라겐 부스터 — HA 필러가 아니며 즉시 볼륨 효과는 제한적이고 수주에」 · 허가 품목 「조직수복용재료」 ↔ M3 정의 |  |
| `M3-2-1` | 래디어스 |  | M3 바이오스티뮬레이터/콜라겐부스터 · CaHA (칼슘하이드록시아파타이트) | 맞음 |  | 원천 M3 › CaHA (칼슘하이드록시아파타이트) 「CaHA 기반 장기 콜라겐 부스터」 · 허가 품목 「조직 수복용 재료 · 조직수복용재료」 ↔ M3 정의 |  |
| `auto-12-1774737181584` | 디클래씨 | ○ | M3 바이오스티뮬레이터/콜라겐부스터 · CaHA (칼슘하이드록시아파타이트) | 맞음 |  | 원천 M3 › CaHA (칼슘하이드록시아파타이트) 「PDLLA/HA 복합 바이오스티뮬레이터」 · 허가 품목 「조직수복용재료」 ↔ M3 정의 |  |
| `M3-3-1` | 엘란쎄 |  | M3 바이오스티뮬레이터/콜라겐부스터 · PCL (폴리카프로락톤) | 맞음 |  | 원천 M3 › PCL (폴리카프로락톤) 「PCL 기반 장기 콜라겐 부스터」 · 허가 품목 「조직수복용재료」 ↔ M3 정의 |  |
| `M3-3-2` | 고우리 |  | M3 바이오스티뮬레이터/콜라겐부스터 · PCL (폴리카프로락톤) | 맞음 |  | 원천 M3 › PCL (폴리카프로락톤) 「액상형 PCL 콜라겐 부스터」 · 허가 품목 「조직 수복용 재료」 ↔ M3 정의 |  |
| `auto-16-1774737181584` | 라풀렌 | ○ | M3 바이오스티뮬레이터/콜라겐부스터 · PCL (폴리카프로락톤) | 맞음 |  | 원천 M3 › PCL (폴리카프로락톤) 「바이오스티뮬레이터 기반 장기 리프팅」 · 허가 품목 「조직 수복용 재료」 ↔ M3 정의 |  |
| `auto-M3-1775364775148` | 린피니 | ○ | M3 바이오스티뮬레이터/콜라겐부스터 · PCL (폴리카프로락톤) | 맞음 |  | 원천 M3 › PCL (폴리카프로락톤) 「신규 PCL 기반의 차세대 바이오스티뮬레이터」 ↔ M3 정의 |  |
| `M3-4-2` | 쥬베룩볼륨 |  | M3 바이오스티뮬레이터/콜라겐부스터 · PDLLA (폴리-D,L-락틱산) | 맞음 |  | 원천 M3 › PDLLA (폴리-D,L-락틱산) 「고함량 PDLLA/HA 콜라겐 부스터」 · 허가 품목 「조직수복용재료」 ↔ M3 정의 |  |
| `M3-4-1` | 쥬베룩 |  | M3 바이오스티뮬레이터/콜라겐부스터 · PDLLA (폴리-D,L-락틱산) | 맞음 |  | 원천 M3 › PDLLA (폴리-D,L-락틱산) 「PDLLA+HA 복합 바이오스티뮬레이터」 · 허가 품목 「조직수복용재료」 ↔ M3 정의 |  |
| `auto-22-1774737181584` | 울트라콜 | ○ | M3 바이오스티뮬레이터/콜라겐부스터 · PDO (폴리디옥사논) | 맞음 |  | 원천 M3 › PDO (폴리디옥사논) 「울트라브이 PDO 미세입자 콜라겐부스터」 · 허가 품목 「조직수복용재료」 ↔ M3 정의 |  |
| `M2-P-7` | 신펄 |  | M2 필러 | 옮김 |  | 원천 products M2-P-7 「제테마의 PLLA(폴리락틱산) 콜라겐 자극형 필러 … 콜라겐 생성을 활성화」 ↔ M3 정의(PLLA) |  |
| `M3-P-5` | 글로벨라 |  | M3 바이오스티뮬레이터/콜라겐부스터 | 맞음 |  | 원천 M3 › products 「PLLA 기반 콜라겐부스터 필러」 ↔ M3 정의 |  |

### M4 스킨부스터 — 40행

| ledger_id | 이름 | auto | 현재 | 판정 | 보조 계열 | 근거 | 메모 |
|---|---|---|---|---|---|---|---|
| `auto-13-1774737181584` | 콜라쥬 | ○ | M3 바이오스티뮬레이터/콜라겐부스터 · 콜라겐 | 옮김 |  | 원천 M3-5 콜라겐 「콜라겐 … 진피 내 볼륨 제공·구조 지지」 — 미립자 이물반응(M3 정의) 아님 · 39544509 Collagen 절 「LAETIGEN … designed specifically for intradermal application to enhance aging skin quality」 |  |
| `auto-14-1774737181584` | 레티젠 | ○ | M3 바이오스티뮬레이터/콜라겐부스터 · 콜라겐 | 옮김 |  | 원천 M3-5 콜라겐 「콜라겐 … 진피 내 볼륨 제공·구조 지지」 — 미립자 이물반응(M3 정의) 아님 · 39544509 Collagen 절 「LAETIGEN … designed specifically for intradermal application to enhance aging skin quality」 |  |
| `auto-15-1774737181584` | 미라콜 | ○ | M3 바이오스티뮬레이터/콜라겐부스터 · 콜라겐 | 옮김 |  | 원천 M3-5 콜라겐 「콜라겐 … 진피 내 볼륨 제공·구조 지지」 — 미립자 이물반응(M3 정의) 아님 · 39544509 Collagen 절 「LAETIGEN … designed specifically for intradermal application to enhance aging skin quality」 |  |
| `auto-M3-1775364775146` | 콜라겐핀 | ○ | M3 바이오스티뮬레이터/콜라겐부스터 · 콜라겐 | 옮김 |  | 원천 M3-5 콜라겐 「콜라겐 … 진피 내 볼륨 제공·구조 지지」 — 미립자 이물반응(M3 정의) 아님 · 39544509 Collagen 절 「LAETIGEN … designed specifically for intradermal application to enhance aging skin quality」 |  |
| `auto-17-1774737181584` | 리투오 | ○ | M3 바이오스티뮬레이터/콜라겐부스터 · 무세포동종진피(hADM) | 옮김 |  | 원천 무세포동종진피 「hADM ECM 스킨부스터」 「콜라겐 생성을 ‘유도’하는 것이 아니라 구조 자체를 ‘직접 보충’」 ↔ M3 정의 collagen-stimulating 과 반대 · M4 문헌(39544509)은 「various biological materials」 — hADM 직접 언급은 없음(본문 검색 0) |  |
| `auto-18-1774737181584` | 리투오 파인 | ○ | M3 바이오스티뮬레이터/콜라겐부스터 · 무세포동종진피(hADM) | 옮김 |  | 원천 무세포동종진피 「hADM ECM 스킨부스터」 「콜라겐 생성을 ‘유도’하는 것이 아니라 구조 자체를 ‘직접 보충’」 ↔ M3 정의 collagen-stimulating 과 반대 · M4 문헌(39544509)은 「various biological materials」 — hADM 직접 언급은 없음(본문 검색 0) |  |
| `auto-19-1774737181584` | 셀르디엠 | ○ | M3 바이오스티뮬레이터/콜라겐부스터 · 무세포동종진피(hADM) | 옮김 |  | 원천 무세포동종진피 「hADM ECM 스킨부스터」 「콜라겐 생성을 ‘유도’하는 것이 아니라 구조 자체를 ‘직접 보충’」 ↔ M3 정의 collagen-stimulating 과 반대 · M4 문헌(39544509)은 「various biological materials」 — hADM 직접 언급은 없음(본문 검색 0) |  |
| `auto-20-1774737181584` | 쥬브아셀 | ○ | M3 바이오스티뮬레이터/콜라겐부스터 · 무세포동종진피(hADM) | 옮김 |  | 원천 무세포동종진피 「hADM ECM 스킨부스터」 「콜라겐 생성을 ‘유도’하는 것이 아니라 구조 자체를 ‘직접 보충’」 ↔ M3 정의 collagen-stimulating 과 반대 · M4 문헌(39544509)은 「various biological materials」 — hADM 직접 언급은 없음(본문 검색 0) |  |
| `auto-21-1774737181584` | 아디떼 | ○ | M3 바이오스티뮬레이터/콜라겐부스터 · 무세포동종진피(hADM) | 옮김 |  | 원천 무세포동종진피 「hADM ECM 스킨부스터」 「콜라겐 생성을 ‘유도’하는 것이 아니라 구조 자체를 ‘직접 보충’」 ↔ M3 정의 collagen-stimulating 과 반대 · M4 문헌(39544509)은 「various biological materials」 — hADM 직접 언급은 없음(본문 검색 0) |  |
| `auto-M3-hADM-1775404146754` | 도프ECM | ○ | M3 바이오스티뮬레이터/콜라겐부스터 · 무세포동종진피(hADM) | 옮김 |  | 원천 무세포동종진피 「hADM ECM 스킨부스터」 「콜라겐 생성을 ‘유도’하는 것이 아니라 구조 자체를 ‘직접 보충’」 ↔ M3 정의 collagen-stimulating 과 반대 · M4 문헌(39544509)은 「various biological materials」 — hADM 직접 언급은 없음(본문 검색 0) |  |
| `M4-1-1` | 리쥬란 |  | M4 스킨부스터 · PN/PDRN | 맞음 |  | 원천 M4 › PN/PDRN 「연어 DNA 유래 PN 스킨부스터」 · 허가 품목 「조직수복용생체재료」 ↔ M4 정의 |  |
| `M4-1-2` | 리쥬란 아이 |  | M4 스킨부스터 · PN/PDRN | 맞음 |  | 원천 M4 › PN/PDRN 「눈가 전용 PN 스킨부스터」 · 허가 품목 「조직수복용생체재료」 ↔ M4 정의 |  |
| `M4-1-3` | 리쥬란HB plus |  | M4 스킨부스터 · PN/PDRN | 맞음 |  | 원천 M4 › PN/PDRN 「HA+PN 복합 스킨부스터」 · 허가 품목 「조직수복용생체재료」 ↔ M4 정의 |  |
| `M4-1-7` | 비타란 |  | M4 스킨부스터 · PN/PDRN | 맞음 |  | 원천 M4 › PN/PDRN 「PN(폴리뉴클레오타이드) 기반 재생형 스킨부스터 — 제품명에 '비타'가 들어가지만 비타민 제제가 아님」 · 허가 품목 「조직수복용생체재료」 ↔ M4 정의 |  |
| `auto-M4-1775361749536` | 인에이블 | ○ | M4 스킨부스터 · PN/PDRN | 맞음 |  | 원천 M4 › PN/PDRN 「LG화학의 PN(폴리뉴클레오타이드) 기반 재생형 스킨부스터 — 리도카인·프로카인 마취제가 아님(이전 'PN = 프로카인/리도카」 ↔ M4 정의 |  |
| `auto-M4-1775362498539` | 스네일샷 | ○ | M4 스킨부스터 · PN/PDRN | 맞음 |  | 원천 M4 › PN/PDRN 「달팽이 분비물 추출물 기반의 스킨부스터로 피부 재생과 보습 개선을 위한 미용 시술」 ↔ M4 정의 | 하위 「PN/PDRN」 틀림 — 원천 설명 「달팽이 분비물 추출물」(복합 성분 하위) |
| `auto-M4-1775364775153` | 레나토S | ○ | M4 스킨부스터 · PN/PDRN | 맞음 |  | 원천 M4 › PN/PDRN 「차세대 폴리뉴클레오타이드 기반 스킨부스터」 ↔ M4 정의 |  |
| `auto-M4-1775364775154` | 소노PDRN | ○ | M4 스킨부스터 · PN/PDRN | 맞음 |  | 원천 M4 › PN/PDRN 「PDRN과 초음파를 결합한 혁신적 스킨부스터」 ↔ M4 정의 |  |
| `M4-2-1` | 스킨바이브 |  | M4 스킨부스터 · HA (물광) | 맞음 |  | 원천 M4 › HA (물광) 「앨러간 하이알루론산 스킨부스터」 · 허가 품목 「조직수복용생체재료」 ↔ M4 정의 |  |
| `M4-2-2` | 리바이브 |  | M4 스킨부스터 · HA (물광) | 맞음 |  | 원천 M4 › HA (물광) 「멀츠 하이알루론산 스킨부스터」 · 허가 품목 「조직수복용생체재료」 ↔ M4 정의 |  |
| `M4-2-3` | 릴리이드M |  | M4 스킨부스터 · HA (물광) | 맞음 |  | 원천 M4 › HA (물광) 「한국BMI 멀티펩타이드 스킨부스터」 ↔ M4 정의 |  |
| `auto-23-1774737181584` | 힐로웨이브 | ○ | M4 스킨부스터 · HA (물광) | 맞음 |  | 원천 M4 › HA (물광) 「하이어코퍼레이션 파동형 하이알루론산」 · 허가 품목 「조직수복용생체재료」 ↔ M4 정의 |  |
| `auto-M4-1775361364993` | NCTF 필로르가 | ○ | M4 스킨부스터 · HA (물광) | 맞음 |  | 원천 M4 › HA (물광) 「프랑스 필로르가의 53가지 활성성분과 히알루론산이 함유된 메조테라피 솔루션으로 피부 재생과 수분 공급을 동시에 제공하는 시술」 ↔ M4 정의 |  |
| `auto-M4-1775361743324` | 매쿰7 | ○ | M4 스킨부스터 · HA (물광) | 맞음 |  | 원천 M4 › HA (물광) 「7가지 성분의 복합 스킨부스터로 피부 재생과 수분 공급을 통한 고급 안티에이징 치료」 · 허가 품목 「조직 수복용 재료」 ↔ M4 정의 |  |
| `auto-M4-1775362484436` | 프로파일로 | ○ | M4 스킨부스터 · HA (물광) | 맞음 |  | 원천 M4 › HA (물광) 「고농도 히알루론산을 이용한 바이오리모델링 주사제로 피부 재생과 탄력 개선을 위한 미용의학 시술용 제품」 ↔ M4 정의 |  |
| `auto-M4-1775364775149` | 사이토케어 | ○ | M4 스킨부스터 · HA (물광) | 맞음 |  | 원천 M4 › HA (물광) 「메조테라피용 HA와 비타민 복합 스킨부스터」 ↔ M4 정의 |  |
| `auto-M4-1775364797153` | 테오시알레디세스 | ○ | M4 스킨부스터 · HA (물광) | 맞음 |  | 원천 M4 › HA (물광) 「테옥산 물광 효과의 특수 HA 스킨부스터」 ↔ M4 정의 |  |
| `auto-M4-1775364797154` | 레스틸렌스킨부스터 | ○ | M4 스킨부스터 · HA (물광) | 맞음 |  | 원천 M4 › HA (물광) 「갈더마의 프리미엄 물광 스킨부스터」 · 허가 품목 「조직수복용생체재료」 ↔ M4 정의 |  |
| `auto-M4-1775360452766` | 리듐 | ○ | M4 스킨부스터 · 콜라겐/신규 | 맞음 |  | 원천 M4 › 콜라겐/신규 「콜라겐 유래 성분으로 진피층에 직접 주입하여 피부탄력과 수분함량을 개선하는 미용시술 제품」 ↔ M4 정의 |  |
| `auto-M4-1775360463217` | 밸피엔 | ○ | M4 스킨부스터 · 콜라겐/신규 | 맞음 |  | 원천 M4 › 콜라겐/신규 「고농도 플라센타 추출물과 다중 성장인자를 함유한 차세대 스킨부스터로 피부 재생 및 탄력 개선을 유도하는 제품」 · 허가 품목 「조직 수복용 생체 재료」 ↔ M4 정의 | 허가 「밸피엔(BelPN)」(PN) — 원천 설명 「플라센타 추출물」은 허가와 충돌, 원천 확인 대상 |
| `auto-M4-1775360574999` | 투 (TU) | ○ | M4 스킨부스터 · 콜라겐/신규 | 맞음 |  | 원천 M4 › 콜라겐/신규 「인체 유래 I형 콜라겐을 직접 주입하여 피부 탄력과 볼륨을 개선하는 2025년 신규 미용시술」 ↔ M4 정의 |  |
| `auto-M4-1775361378128` | 바이리즌 | ○ | M4 스킨부스터 · 콜라겐/신규 | 여러 계열 | M2 | 허가 2건 「the 채움 프리미엄 No. 2」(HA 필러 라인) · 「PN SKINBOOSTER」 — 원천 M4 · 주 M4 · 필러 품목 = M2 |  |
| `auto-M4-1775364775152` | SNP솔루션 | ○ | M4 스킨부스터 · 콜라겐/신규 | 맞음 |  | 원천 M4 › 콜라겐/신규 「국산 콜라겐 기반 스킨부스터」 ↔ M4 정의 |  |
| `M15-6-2` | 큐어젯 |  | M15 메디컬스킨케어 · 주입장비 (원천 시술군 M15) | 옮김 |  | 원천 M15-6 주입장비 「약물 무침 주입」 — 바르는 관리 아님, 진피에 약제를 넣는 기기 · 39544509 Needle-free Jet Injectors 절(큐어젯 직접 예시) · 33682249 |  |
| `M15-6-3` | 미라젯 |  | M15 메디컬스킨케어 · 주입장비 (원천 시술군 M15) | 옮김 |  | 원천 M15-6 주입장비 「약물 무침 주입」 — 바르는 관리 아님, 진피에 약제를 넣는 기기 · 39544509 Needle-free Jet Injectors 절(큐어젯 직접 예시) · 33682249 |  |
| `auto-50-1774737181584` | 하이쿡스 | ○ | M15 메디컬스킨케어 · 주입장비 (원천 시술군 M15) | 옮김 |  | 허가 품목 「전동식 의약품 주입 펌프」 · 원천 「다중 미세바늘로 약물 정밀 주입」 · 39544509 「applied intradermally … using an automatic injector」 |  |
| `auto-51-1774737181584` | 더마샤인 | ○ | M15 메디컬스킨케어 · 주입장비 (원천 시술군 M15) | 옮김 |  | 허가 품목 「전동식 의약품 주입 펌프」 · 원천 「다중 미세바늘로 약물 정밀 주입」 · 39544509 「applied intradermally … using an automatic injector」 |  |
| `auto-M15-1775360527416` | 에어젯 | ○ | M15 메디컬스킨케어 · 주입장비 (원천 시술군 M15) | 옮김 |  | 원천 M15-6 주입장비 「약물 무침 주입」 — 바르는 관리 아님, 진피에 약제를 넣는 기기 · 39544509 Needle-free Jet Injectors 절(큐어젯 직접 예시) · 33682249 |  |
| `auto-M15-1775360904089` | 노보젯 | ○ | M15 메디컬스킨케어 · 주입장비 (원천 시술군 M15) | 옮김 |  | 원천 M15-6 주입장비 「약물 무침 주입」 — 바르는 관리 아님, 진피에 약제를 넣는 기기 · 39544509 Needle-free Jet Injectors 절(큐어젯 직접 예시) · 33682249 |  |
| `auto-M15-1775361179297` | 비타인젝터 | ○ | M15 메디컬스킨케어 · 물광/메조건 (원천 시술군 M15) | 옮김 |  | 원천 물광/메조건 「자동화 멀티니들 약물 주입 인젝터 … 진피에 균일하게 주입」 · 39544509 automatic injector |  |

### M5 PRP·엑소좀 — 8행

| ledger_id | 이름 | auto | 현재 | 판정 | 보조 계열 | 근거 | 메모 |
|---|---|---|---|---|---|---|---|
| `M4-3-1` | ASCE+엑소좀 |  | M4 스킨부스터 · 엑소좀/성장인자 | 옮김 |  | 원천 M4-3 엑소좀/성장인자 ↔ 문헌 M5 이름 「PRP and exosome therapies」(literature M5.moa[1]·[2]) · M4 문헌 39544509 은 exosome 0건 |  |
| `auto-M4-1775361371619` | 셀엑소좀 | ○ | M4 스킨부스터 · 엑소좀/성장인자 | 옮김 |  | 원천 M4-3 엑소좀/성장인자 ↔ 문헌 M5 이름 「PRP and exosome therapies」(literature M5.moa[1]·[2]) · M4 문헌 39544509 은 exosome 0건 |  |
| `auto-M4-1775364775151` | 카탈리스트 | ○ | M4 스킨부스터 · 엑소좀/성장인자 | 옮김 |  | 원천 M4-3 엑소좀/성장인자 ↔ 문헌 M5 이름 「PRP and exosome therapies」(literature M5.moa[1]·[2]) · M4 문헌 39544509 은 exosome 0건 |  |
| `auto-M4-1775364775155` | 드원셀 | ○ | M4 스킨부스터 · 엑소좀/성장인자 | 옮김 |  | 원천 M4-3 엑소좀/성장인자 ↔ 문헌 M5 이름 「PRP and exosome therapies」(literature M5.moa[1]·[2]) · M4 문헌 39544509 은 exosome 0건 |  |
| `M5-P-0` | 셀피아 |  | M5 PRP/자가혈 | 맞음 |  | 원천 M5 › products 「자가혈 기반 세포 활성 성장인자 제제」 ↔ M5 정의 |  |
| `M5-P-1` | 리젠ACR |  | M5 PRP/자가혈 | 맞음 |  | 원천 M5 › products 「자동화 혈소판 농축 성장인자 시스템」 ↔ M5 정의 |  |
| `M5-P-2` | 마이셀 |  | M5 PRP/자가혈 | 맞음 |  | 원천 M5 › products 「자가혈 기반 다층 성장인자 분리 제제」 ↔ M5 정의 |  |
| `M5-P-4` | EXOSOME SKIN |  | M5 PRP/자가혈 | 맞음 |  | 원천 M5 › products 「엑소솜 기반 성장인자 전달 시스템」 ↔ M5 정의 |  |

### M7 실리프팅 — 12행

| ledger_id | 이름 | auto | 현재 | 판정 | 보조 계열 | 근거 | 메모 |
|---|---|---|---|---|---|---|---|
| `M7-3-1` | 민트리프트 |  | M7 실리프팅 | 맞음 |  | 원천 M7 › 브랜드 「코그 톱니 구조로 강력한 리프팅 브랜드」 · 허가 품목 「안면조직고정용실」 ↔ M7 정의 |  |
| `M7-3-3` | 테스리프트 |  | M7 실리프팅 | 맞음 |  | 원천 M7 › 브랜드 「PDO 실과 몰딩 메쉬 구조로 즉각적인 리프팅과 장기적인 콜라겐 재생을 동시에 제공하는 고급 시술 제품」 · 허가 품목 「폴리디옥사논봉합사」 ↔ M7 정의 |  |
| `M7-3-2` | 실루엣소프트 |  | M7 실리프팅 | 맞음 |  | 원천 M7 › 브랜드 「PLLA 콘 구조로 즉각적 기계적 지지와 12-18개월 생물학적 자극을 제공하는 차세대 실리프팅 제품」 · 허가 품목 「안면조직고정용실」 ↔ M7 정의 |  |
| `auto-M7-1775361076707` | 잼버실 | ○ | M7 실리프팅 | 맞음 |  | 원천 M7 › 브랜드 「PCA(Polycaprolactone) 소재의 생분해성 실을 이용해 콜라겐 생성을 장기간 유도하는 리프팅 시술」 · 허가 품목 「폴리디옥사논봉합사」 ↔ M7 정의 |  |
| `auto-M7-1775362555891` | 블루로즈클레어 | ○ | M7 실리프팅 | 맞음 |  | 원천 M7 › 브랜드 「PCL(폴리카프로락톤) 소재의 흡수성 코그실로 리프팅과 콜라겐 재생을 동시에 제공하는 실리프팅 시술용 의료기기」 · 허가 품목 「기타흡수성봉합사」 ↔ M7 정의 |  |
| `auto-M7-1775362571755` | N코그 | ○ | M7 실리프팅 | 맞음 |  | 원천 M7 › 브랜드 「PDO 실을 이용하여 코 모양을 교정하고 높이를 개선하는 비수술적 성형술」 ↔ M7 정의 |  |
| `auto-M7-1775362579841` | 오메가리프트 | ○ | M7 실리프팅 | 맞음 |  | 원천 M7 › 브랜드 「오메가 형태의 PDO 코그 실을 이용한 리프팅 시술로 강력한 당김력과 볼륨 효과를 제공하는 미용 시술」 · 허가 품목 「폴리디옥사논봉합사」 ↔ M7 정의 |  |
| `auto-M7-1775362729861` | 캐번실 | ○ | M7 실리프팅 | 맞음 |  | 원천 M7 › 브랜드 「PDO 코그실 캐번디시 라인」 ↔ M7 정의 |  |
| `auto-M7-1775364775158` | 울트라V | ○ | M7 실리프팅 | 맞음 |  | 원천 M7 › 브랜드 「PDO 전문 리프팅 실」 ↔ M7 정의 |  |
| `M7-P-1` | 에버라인 |  | M7 실리프팅 | 맞음 |  | 원천 M7 › products 「PDO, PLLA, PCL 3가지 재질의 복합 스레드로 즉각적 리프팅과 장기간 콜라겐 재생을 동시에 제공하는 프리미엄 리프팅 」 ↔ M7 정의 |  |
| `M7-P-2` | 미라클 |  | M7 실리프팅 | 맞음 |  | 원천 M7 › products 「PDO 단일 성분의 6개월 분해 실리프팅으로 즉각적인 거상과 자연스러운 콜라겐 재생을 제공하는 시술 제품」 ↔ M7 정의 |  |
| `step1-new-APTOS` | 압토스 |  | M7 실리프팅 | 맞음 |  | 허가 품목 「안면조직 고정용 실」 ↔ M7 정의 |  |

### M8 레이저·IPL — 68행

| ledger_id | 이름 | auto | 현재 | 판정 | 보조 계열 | 근거 | 메모 |
|---|---|---|---|---|---|---|---|
| `M8-1-3` | 피코슈어 |  | M8 레이저 · 색소/토닝 | 맞음 |  | 원천 M8 › 색소/토닝 「755nm 알렉산드라이트 레이저를 이용한 초단펄스 피코초 기술로 표피 손상을 최소화하면서 멜라닌 색소와 문신 제거에 특화된 시」 · 허가 품목 「알렉산드라이트 레이저 수술기」 ↔ M8 정의 |  |
| `auto-M8-1775361386532` | 레블라이트 SI | ○ | M8 레이저 · 색소/토닝 | 맞음 |  | 원천 M8 › 색소/토닝 「큐스위치 Nd:YAG 레이저를 이용한 색소성 병변 및 흉터 개선 시술」 · 허가 품목 「엔디야그레이저수술기」 ↔ M8 정의 |  |
| `auto-M8-1775361394023` | 피코케어 | ○ | M8 레이저 · 색소/토닝 | 맞음 |  | 원천 M8 › 색소/토닝 「1064/532nm 파장의 피코초 레이저를 이용하여 색소질환과 피부재생을 동시에 개선하는 미용시술」 · 허가 품목 「엔디야그 레이저 수술기 · 엔디야그레이저수술기」 ↔ M8 정의 |  |
| `auto-M8-1775362587235` | 피코코어 | ○ | M8 레이저 · 색소/토닝 | 맞음 |  | 원천 M8 › 색소/토닝 「1064nm 파장의 피코초 레이저를 이용한 경제형 색소 치료 장비」 ↔ M8 정의 |  |
| `auto-M8-1775362943490` | 트루피코 | ○ | M8 레이저 · 색소/토닝 | 맞음 |  | 원천 M8 › 색소/토닝 「4파장 레이저 시스템을 이용한 컬러 문신 제거 전용 의료기기」 ↔ M8 정의 |  |
| `auto-M8-1775362951135` | 리레이저 | ○ | M8 레이저 · 색소/토닝 | 맞음 |  | 원천 M8 › 색소/토닝 「Q-switched Nd:YAG 레이저를 이용한 색소성 병변 및 문신 제거용 의료기기」 ↔ M8 정의 |  |
| `auto-M8-1775364775120` | 스타워커 | ○ | M8 레이저 · 색소/토닝 | 맞음 |  | 원천 M8 › 색소/토닝 「포토나 피코나노 기술의 프리미엄 레이저 시술」 · 허가 품목 「엔디야그 레이저 수술기 · 엔디야그레이저수술기」 ↔ M8 정의 |  |
| `M8-2-4` | 프락셀 듀얼 |  | M8 레이저 · 프락셔널 | 맞음 |  | 원천 M8 › 프락셔널 「1550nm와 1927nm 이중 파장을 이용한 비박피/얕은 박피 프락셀 레이저로 표피-진피 손상을 최소화하면서 콜라겐 재생을 」 · 허가 품목 「기타 레이저 수술기」 ↔ M8 정의 |  |
| `auto-M8-1775361850481` | 모자이크 | ○ | M8 레이저 · 프락셔널 | 맞음 |  | 원천 M8 › 프락셔널 「Er:Glass 1550nm 레이저를 이용한 비박리성 프락셔널 치료로 피부 재생과 질감 개선을 도모하는 미용시술」 · 허가 품목 「기타 레이저 수술기 · 기타레이저수술기」 ↔ M8 정의 |  |
| `auto-M8-1775362603297` | 에코2 | ○ | M8 레이저 · 프락셔널 | 맞음 |  | 원천 M8 › 프락셔널 「루트로닉의 CO2 프랙셔널 레이저로 프로스캔 기술을 통해 피부 재생과 리모델링을 유도하는 미용 레이저 장비」 · 허가 품목 「탄산가스 레이저 수술기 · 탄산가스레이저수술기」 ↔ M8 정의 |  |
| `auto-M8-1775364106103` | 셀렉V | ○ | M8 레이저 · IPL | 맞음 |  | 원천 M8 › 프락셔널 「Q-switched Nd:YAG 레이저를 이용한 색소성 병변 치료 장비」 · 허가 품목 「펄스광선조사기」 ↔ M8 정의 | 허가 「펄스광선조사기」(IPL) ↔ 원천 설명 「Q-switched Nd:YAG」 — 하위 계열은 허가 기준 IPL |
| `auto-M8-1775364775119` | 에코2 에볼루션 | ○ | M8 레이저 · 프락셔널 | 맞음 |  | 원천 M8 › 프락셔널 「루트로닉 CO2 레이저의 진화된 피부재생 시술」 ↔ M8 정의 |  |
| `auto-M8-1775364775129` | 울트라펄스 | ○ | M8 레이저 · 프락셔널 | 맞음 |  | 원천 M8 › 프락셔널 「루미너스 CO2 레이저를 이용한 피부 재생 시술」 · 허가 품목 「탄산가스 레이저 수술기」 ↔ M8 정의 |  |
| `auto-29-1774737181584` | BBL | ○ | M8 레이저 · IPL | 맞음 |  | 원천 M8 › IPL 「광범위 파장(515-1200nm)의 강렬한 펄스광을 이용한 비침습적 광열용해 시술」 ↔ M8 정의 |  |
| `auto-31-1774737181584` | BBL 히어로 | ○ | M8 레이저 · IPL | 맞음 |  | 원천 M8 › IPL 「Sciton 광대역 IPL 기기 (PDL 아님)」 · 허가 품목 「반도체 레이저 수술기」 ↔ M8 정의 |  |
| `auto-32-1774737181584` | BBL 스킨타이트 | ○ | M8 레이저 · IPL | 맞음 |  | 원천 M8 › IPL 「근적외선 광에너지를 이용하여 진피층의 콜라겐을 수축시키고 재생을 유도하는 비침습적 피부 타이트닝 시술」 ↔ M8 정의 | 원천 「810nm 근적외선 … 타이트닝」 — 광원 기기(M8), 목적이 타이트닝 |
| `M8-4-1` | 브이빔 |  | M8 레이저 · 혈관 | 맞음 |  | 원천 M8 › 혈관 「혈관 병변과 색소 질환 치료를 위한 선택적 광열용해 기반의 롱펄스 PDL 레이저」 ↔ M8 정의 |  |
| `M8-4-2` | 엑셀 V |  | M8 레이저 · 혈관 | 맞음 |  | 원천 M8 › 혈관 「멜라닌과 혈관 타겟팅이 가능한 이중 파장 롱펄스 Nd:YAG 레이저로 색소성 병변과 혈관병변을 동시에 치료하는 다목적 미용 레」 · 허가 품목 「엔디야그레이저수술기」 ↔ M8 정의 |  |
| `M8-4-3` | 더마V |  | M8 레이저 · 혈관 | 맞음 |  | 원천 M8 › 혈관 「멜라닌과 옥시헤모글로빈에 선택적으로 흡수되는 이중파장 레이저로 색소성 병변과 혈관성 병변을 동시에 치료하는 비절제 레이저」 · 허가 품목 「엔디야그 레이저 수술기」 ↔ M8 정의 |  |
| `auto-34-1774737181584` | 노블린 | ○ | M8 레이저 · 혈관 | 맞음 |  | 원천 M8 › 혈관 「멜라닌에 선택적으로 반응하는 이중파장 롱펄스 Nd:YAG 레이저로 색소질환과 혈관질환을 동시에 치료」 · 허가 품목 「알렉산드라이트레이저수술기」 ↔ M8 정의 |  |
| `auto-M8-1775361179259` | 엑셀 V+ | ○ | M8 레이저 · 혈관 | 맞음 |  | 원천 M8 › 혈관 「큐테라 KTP+Nd:YAG 듀얼 파장 혈관/색소 레이저」 · 허가 품목 「엔디야그레이저수술기」 ↔ M8 정의 |  |
| `auto-M8-1775362594611` | 시너론 아이플러스 | ○ | M8 레이저 · 혈관 | 여러 계열 | M9 | 원천 「IPL과 RF 에너지를 결합한 eLight」 — 주 IPL(원천 M8-4) · RF 보조 |  |
| `auto-M8-1775364775121` | 브이빔 퍼펙타 | ○ | M8 레이저 · 혈관 | 맞음 |  | 원천 M8 › 혈관 「시너론 595nm 레이저를 이용한 혈관 병변 치료」 ↔ M8 정의 |  |
| `auto-M8-1775364775122` | 아이콘 | ○ | M8 레이저 · 혈관 | 맞음 |  | 원천 M8 › 혈관 「IPL과 1540nm 레이저를 결합한 복합 피부 치료」 · 허가 품목 「기타 레이저 수술기」 ↔ M8 정의 |  |
| `M8-5-4` | 클라리티2 |  | M8 레이저 · 제모 | 맞음 |  | 원천 M8 › 제모 「멜라닌과 혈관 병변의 선택적 광열용해를 위한 듀얼 파장 롱펄스 Nd:YAG 레이저」 · 허가 품목 「알렉산드라이트 레이저 수술기 · 알렉산드라이트레이저수술기 · 엔디야그 레이저 수술기 · 엔디야그레이저수술기」 ↔ M8 정의 |  |
| `M8-5-3` | 젠틀맥스 프로 플러스 |  | M8 레이저 · 제모 | 맞음 |  | 원천 M8 › 제모 「멜라닌과 옥시헤모글로빈에 선택적으로 작용하는 듀얼 파장 레이저로 제모, 혈관병변, 색소병변 치료에 탁월한 효과를 발휘합니다.」 · 허가 품목 「알렉산드라이트레이저수술기」 ↔ M8 정의 |  |
| `M8-5-5` | 아발란체 |  | M8 레이저 · 제모 | 맞음 |  | 원천 M8 › 제모 「선택적 광열용해 원리로 멜라닌과 혈관 병변을 선택적으로 제거하는 이중 파장 롱펄스 레이저」 · 허가 품목 「엔디야그 레이저 수술기」 ↔ M8 정의 |  |
| `auto-36-1774737181584` | 아포지 엘리트 플러스 | ○ | M8 레이저 · 제모 | 맞음 |  | 허가 「알렉산드라이트 레이저 수술기」 Elite+ — 합쳐진 현장 기기 아포지 플러스(new-DEV-005)도 같은 레이저 |  |
| `auto-M8-1775361401143` | 라이트쉬어 듀엣 | ○ | M8 레이저 · 제모 | 맞음 |  | 원천 M8 › 제모 「루메니스社의 다이오드 808nm 레이저를 사용한 대면적 영구제모 시술」 · 허가 품목 「반도체 레이저 수술기」 ↔ M8 정의 |  |
| `auto-M8-1775361486532` | 트리니티 | ○ | M8 레이저 · 제모 | 맞음 |  | 원천 M8 › 제모 「3파장 다이오드 복합 제모 레이저」 · 허가 품목 「반도체 레이저 수술기」 ↔ M8 정의 |  |
| `auto-M8-1775362612108` | 젠틀맥스 프로 | ○ | M8 레이저 · 제모 | 맞음 |  | 원천 M8 › 제모 「알렉산드라이트(755nm)와 Nd:YAG(1064nm) 레이저를 결합한 듀얼 파장 제모 시스템」 · 허가 품목 「알렉산드라이트레이저수술기」 ↔ M8 정의 |  |
| `auto-M8-1775362619619` | 슬렌더엑스 | ○ | M8 레이저 · 제모 | 맞음 |  | 원천 「1060nm 다이오드 레이저 … 지방세포 파괴」 — 레이저(M8) 맞음 · 하위 「제모」는 틀림(목적 = 지방 감소, 6단계) |  |
| `auto-M8-1775362912344` | 젠틀레이즈 | ○ | M8 레이저 · 제모 | 맞음 |  | 원천 M8 › 제모 「755nm 알렉산드라이트 레이저를 이용한 선택적 광열분해 원리 기반의 영구 제모 시술」 ↔ M8 정의 |  |
| `auto-M8-1775362921273` | 메디오스타넥스트프로 | ○ | M8 레이저 · 제모 | 맞음 |  | 원천 M8 › 제모 「아스클레피온사의 다이오드 레이저를 이용한 무통 영구제모 시스템」 · 허가 품목 「반도체레이저수술기」 ↔ M8 정의 |  |
| `auto-M8-1775362928187` | 벡터스 | ○ | M8 레이저 · 제모 | 맞음 |  | 원천 M8 › 제모 「810nm 다이오드 레이저를 이용한 대면적 제모 및 혈관 치료 장비」 ↔ M8 정의 |  |
| `auto-M8-1775362936434` | 리팟 | ○ | M8 레이저 · 색소/토닝 | 맞음 |  | 원천 M8 › 제모 「클래시스의 532nm Q-switched Nd:YAG 레이저 시스템 — 멜라닌·헤모글로빈 선택적 광열분해로 표재성 색소 및 혈」 · 허가 품목 「엔디야그레이저수술기」 ↔ M8 정의 |  |
| `auto-M8-1775364775126` | 스플렌더 X | ○ | M8 레이저 · 제모 | 맞음 |  | 원천 M8 › 제모 「루메니스 듀얼 파장 레이저 제모 시스템」 · 허가 품목 「알렉산드라이트레이저수술기」 ↔ M8 정의 |  |
| `auto-M8-1775360944918` | SP 다이나미스 | ○ | M8 레이저 | 맞음 |  | 원천 M8 › 기타 「Er:YAG와 Nd:YAG 듀얼 레이저를 이용한 4차원 복합 안티에이징 리프팅 시술」 · 허가 품목 「엔디야그레이저수술기」 ↔ M8 정의 |  |
| `auto-M8-1775361179272` | 스텔라 M22 | ○ | M8 레이저 | 맞음 |  | 원천 M8 › 기타 「루메니스 멀티 애플리케이션 IPL/레이저 플랫폼」 · 허가 품목 「펄스광선조사기」 ↔ M8 정의 |  |
| `auto-M8-1775361179284` | 할리우드 스펙트라 | ○ | M8 레이저 | 맞음 |  | 원천 M8 › 기타 「루트로닉 1064/660nm Nd:YAG 토닝+할리우드필」 · 허가 품목 「엔디야그 레이저 수술기 · 엔디야그레이저수술기」 ↔ M8 정의 |  |
| `auto-M8-1775361417735` | 이맥스 | ○ | M8 레이저 | 여러 계열 | M9 | 원천 「RF, 다이오드 레이저, 근적외선 결합」 — 주 광원(원천 M8-6) · RF 보조 |  |
| `auto-M8-1775364775123` | 스마트자이드 | ○ | M8 레이저 | 여러 계열 | M9 | 원천 「DEKA CO2와 RF를 결합」 · 허가 「탄산가스 레이저 수술기」 — 주 M8 |  |
| `auto-M8-1775364775124` | 클리어 앤 브릴리언트 | ○ | M8 레이저 | 맞음 |  | 원천 M8 › 기타 「솔타 1440nm 레이저를 이용한 마일드 피부 재생」 · 허가 품목 「반도체 레이저 수술기」 ↔ M8 정의 |  |
| `auto-M8-1775364775127` | 바이탈라이즈 | ○ | M8 레이저 | 맞음 |  | 원천 M8 › 기타 「IPL을 이용한 피부 재생 및 활력 개선 시술」 ↔ M8 정의 |  |
| `auto-M8-1775364775128` | 포토나스타발브 | ○ | M8 레이저 | 맞음 |  | 원천 M8 › 기타 「Er:YAG 레이저를 이용한 어븀야그 피부 재생 시술」 ↔ M8 정의 |  |
| `auto-M8-1775364797146` | 로제라이트 | ○ | M8 레이저 | 여러 계열 | M9 | 원천 「홍조 전용 RF와 IPL」 — 주 IPL(원천 M8-6) · RF 보조 |  |
| `auto-M8-1775360583893` | 피코플러스 | ○ | M8 레이저 · 피코초(Picosecond) | 맞음 |  | 원천 M8 › 피코초(Picosecond) 「4가지 파장을 이용한 피코초 레이저로 색소질환과 피부톤 개선을 위한 미용시술」 · 허가 품목 「엔디야그 레이저 수술기 · 엔디야그레이저수술기」 ↔ M8 정의 |  |
| `auto-M8-1775360593064` | 디스커버리 피코 | ○ | M8 레이저 · 피코초(Picosecond) | 맞음 |  | 원천 M8 › 피코초(Picosecond) 「피코초 레이저를 이용한 멜라닌 색소 제거 및 피부 재생 시술」 · 허가 품목 「루비레이저수술기 · 엔디야그레이저수술기」 ↔ M8 정의 |  |
| `auto-M8-1775360601666` | 엔라이튼 | ○ | M8 레이저 · 피코초(Picosecond) | 맞음 |  | 원천 M8 › 피코초(Picosecond) 「큐테라사의 3파장 레이저로 멜라닌 선택적 파괴를 통한 색소성 병변 및 문신 제거 시술」 · 허가 품목 「엔디야그레이저수술기」 ↔ M8 정의 |  |
| `M15-3-1` | 옴니룩스 |  | M15 메디컬스킨케어 · 광치료(LED) (원천 시술군 M15) | 옮김 |  | 원천 M15-3 「LED 파장(적색/근적외선)이 미토콘드리아 …」 — 광원 기기, 외용제 아님(M15 정의 밖) · 40751922 「LED therapy employs narrow-spectrum, incoherent light for photobiomodulation」 · 원천 M8 영문 「Laser & Light」 |  |
| `M15-3-2` | 힐라이트 |  | M15 메디컬스킨케어 · 광치료(LED) (원천 시술군 M15) | 옮김 |  | 원천 M15-3 「LED 파장(적색/근적외선)이 미토콘드리아 …」 — 광원 기기, 외용제 아님(M15 정의 밖) · 40751922 「LED therapy employs narrow-spectrum, incoherent light for photobiomodulation」 · 원천 M8 영문 「Laser & Light」 |  |
| `auto-49-1774737181584` | 아스트로돔 | ○ | M15 메디컬스킨케어 · 광치료(LED) (원천 시술군 M15) | 옮김 |  | 원천 M15-3 「LED 파장(적색/근적외선)이 미토콘드리아 …」 — 광원 기기, 외용제 아님(M15 정의 밖) · 40751922 「LED therapy employs narrow-spectrum, incoherent light for photobiomodulation」 · 원천 M8 영문 「Laser & Light」 |  |
| `auto-M15-1775362992228` | 셀라이트 | ○ | M15 메디컬스킨케어 · 광치료(LED) (원천 시술군 M15) | 옮김 |  | 원천 M15-3 「LED 파장(적색/근적외선)이 미토콘드리아 …」 — 광원 기기, 외용제 아님(M15 정의 밖) · 40751922 「LED therapy employs narrow-spectrum, incoherent light for photobiomodulation」 · 원천 M8 영문 「Laser & Light」 |  |
| `auto-M15-1775362998455` | 데마루치 | ○ | M15 메디컬스킨케어 · 광치료(LED) (원천 시술군 M15) | 옮김 |  | 원천 M15-3 「LED 파장(적색/근적외선)이 미토콘드리아 …」 — 광원 기기, 외용제 아님(M15 정의 밖) · 40751922 「LED therapy employs narrow-spectrum, incoherent light for photobiomodulation」 · 원천 M8 영문 「Laser & Light」 |  |
| `auto-M15-1775364775179` | 바이오프로톤 | ○ | M15 메디컬스킨케어 · 광치료(LED) (원천 시술군 M15) | 옮김 |  | 원천 M15-3 「LED 파장(적색/근적외선)이 미토콘드리아 …」 — 광원 기기, 외용제 아님(M15 정의 밖) · 40751922 「LED therapy employs narrow-spectrum, incoherent light for photobiomodulation」 · 원천 M8 영문 「Laser & Light」 |  |
| `new-DEV-018` | 이래비티 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 2_리프팅) | 옮김 |  | 허가 품목 「엔디야그레이저수술기」 |  |
| `new-DEV-043` | 오메가라이트 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 6_피부관리) | 옮김 |  | web4 「LED (PDT, 423/532/583/640nm + 830nm IR)」 — LED 광원(D04 와 같이 감) |  |
| `new-DEV-058` | 브라이톤 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 1_레이저) | 옮김 |  | 허가 품목 「엔디야그레이저수술기」 |  |
| `new-DEV-060` | 피코라이트 블랙 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 1_레이저) | 옮김 |  | 허가 품목 「엔디야그레이저수술기」 |  |
| `new-DEV-061` | 피코라이트 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 1_레이저) | 옮김 |  | 허가 품목 「엔디야그레이저수술기」 |  |
| `new-DEV-063` | 큐라스 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 1_레이저) | 옮김 |  | 허가 품목 「엔디야그레이저수술기」 |  |
| `new-DEV-065` | 헬리오스 3 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 1_레이저) | 옮김 |  | 허가 품목 「엔디야그레이저수술기」 |  |
| `new-DEV-067` | 피코케이 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 1_레이저) | 옮김 |  | 허가 품목 「엔디야그레이저수술기」 |  |
| `new-DEV-068` | 피콜로 프리미엄 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 1_레이저) | 옮김 |  | 허가 품목 「엔디야그레이저수술기」 |  |
| `new-DEV-069` | 아톰 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 1_레이저) | 옮김 |  | 허가 품목 「의료용 레이저 조사기」(TINEA) · web4 「405nm+635nm 저출력 레이저 … 조갑진균증 치료기」 — 레이저(M8), 용도는 미용 아님(6단계 목적에서 처리) |  |
| `new-DEV-075` | 카프리 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 4_여드름) | 옮김 |  | 허가 품목 「반도체 레이저 수술기」 |  |
| `new-DEV-076` | 아큐토닝 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 4_여드름) | 옮김 |  | 허가 품목 「반도체 레이저 수술기」 |  |
| `M8-P-1` | 피코웨이 |  | M8 레이저 | 맞음 |  | 원천 M8 › products 「Candela 1064/532/785nm Nd:YAG 피코초 레이저」 · 허가 품목 「엔디야그레이저수술기」 ↔ M8 정의 |  |

### M9 HIFU·고주파 리프팅 — 49행

| ledger_id | 이름 | auto | 현재 | 판정 | 보조 계열 | 근거 | 메모 |
|---|---|---|---|---|---|---|---|
| `M9-1-1` | 울쎄라 |  | M9 기기 리프팅 · HIFU (초음파) | 맞음 |  | 원천 M9 › HIFU (초음파) 「집속초음파 에너지를 정밀하게 SMAS층에 전달하여 즉각적인 리프팅 효과를 제공하는 비침습적 시술」 · 허가 품목 「집속형초음파자극시스템」 ↔ M9 정의 |  |
| `M9-1-2` | 울쎄라피 프라임 |  | M9 기기 리프팅 · HIFU (초음파) | 맞음 |  | 원천 M9 › HIFU (초음파) 「최신형 HIFU 기술로 SMAS층까지 집중 에너지를 전달하여 즉각적인 리프팅 효과를 제공하는 신세대 초음파 미용기기」 · 허가 품목 「집속형초음파자극시스템」 ↔ M9 정의 |  |
| `M9-1-3` | 슈링크 |  | M9 기기 리프팅 · HIFU (초음파) | 맞음 |  | 원천 M9 › HIFU (초음파) 「HIFU(고강도 집속 초음파) 리프팅 기기」 · 허가 품목 「집속형초음파자극시스템」 ↔ M9 정의 |  |
| `M9-1-4` | 슈링크 유니버스 |  | M9 기기 리프팅 · HIFU (초음파) | 맞음 |  | 원천 M9 › HIFU (초음파) 「HIFU 전용 리프팅 기기 (클래시스)」 · 허가 품목 「집속형 초음파 자극 시스템」 ↔ M9 정의 |  |
| `M9-1-5` | 더블로 |  | M9 기기 리프팅 · HIFU (초음파) | 맞음 |  | 원천 M9 › HIFU (초음파) 「집속초음파(HIFU) 기술을 이용한 비침습적 안면 리프팅 및 탄력 개선 치료기」 · 허가 품목 「집속형 초음파 자극 시스템 · 집속형초음파자극시스템」 ↔ M9 정의 |  |
| `M9-1-6` | 더블로 골드 |  | M9 기기 리프팅 · HIFU (초음파) | 맞음 |  | 원천 M9 › HIFU (초음파) 「HIFU(고강도 집속 초음파) 리프팅 기기」 · 허가 품목 「집속형초음파자극시스템」 ↔ M9 정의 |  |
| `M9-1-8` | 리프테라 |  | M9 기기 리프팅 · HIFU (초음파) | 맞음 |  | 원천 M9 › HIFU (초음파) 「HIFU(고강도 집속 초음파) 리프팅 기기」 · 허가 품목 「집속형 초음파 자극 시스템 · 집속형초음파자극시스템」 ↔ M9 정의 |  |
| `M9-1-9` | 리니어펌 |  | M9 기기 리프팅 · HIFU (초음파) | 맞음 |  | 원천 M9 › HIFU (초음파) 「HIFU(고강도 집속 초음파) 리프팅 기기」 · 허가 품목 「집속형초음파자극시스템」 ↔ M9 정의 |  |
| `M9-1-10` | 텐쎄라 |  | M9 기기 리프팅 · HIFU (초음파) | 맞음 |  | 원천 M9 › HIFU (초음파) 「HIFU(고강도 집속 초음파) 리프팅 기기」 · 허가 품목 「집속형초음파자극시스템」 ↔ M9 정의 |  |
| `auto-37-1774737181584` | 쿨소닉 | ○ | M9 기기 리프팅 · HIFU (초음파) | 맞음 |  | 원천 M9 › HIFU (초음파) 「HIFU(고강도 집속 초음파) 리프팅 기기」 · 허가 품목 「집속형 초음파 자극 시스템」 ↔ M9 정의 |  |
| `auto-M9-1775362627041` | 울트라셀 Q+ | ○ | M9 기기 리프팅 · HIFU (초음파) | 맞음 |  | 원천 M9 › HIFU (초음파) 「고강도 집속 초음파(HIFU)와 도트 기술을 결합한 비수술적 리프팅 및 피부재생 장비」 · 허가 품목 「집속형초음파자극시스템」 ↔ M9 정의 |  |
| `auto-M9-1775363043305` | 울트라셀 | ○ | M9 기기 리프팅 · HIFU (초음파) | 맞음 |  | 원천 M9 › HIFU (초음파) 「고강도 집속 초음파(HIFU) 기술을 이용한 비침습적 리프팅 및 타이트닝 시술」 · 허가 품목 「집속형초음파자극시스템」 ↔ M9 정의 |  |
| `auto-M9-1775364775133` | 하이푸니 | ○ | M9 기기 리프팅 · HIFU (초음파) | 맞음 |  | 원천 M9 › HIFU (초음파) 「소형 HIFU 기술을 이용한 비침습적 리프팅 시술」 ↔ M9 정의 |  |
| `auto-M9-1775364775134` | 더블로골드S | ○ | M9 기기 리프팅 · HIFU (초음파) | 맞음 |  | 원천 M9 › HIFU (초음파) 「히로닉 최신 기술을 적용한 프리미엄 HIFU 리프팅」 · 허가 품목 「집속형 초음파 자극 시스템 · 집속형초음파자극시스템」 ↔ M9 정의 |  |
| `M9-2-1` | 써마지 FLX |  | M9 기기 리프팅 · RF (고주파) | 맞음 |  | 원천 M9 › RF (고주파) 「고주파 에너지를 이용하여 피부 깊숙한 층의 콜라겐을 수축·재생시키는 비침습적 리프팅 시술」 · 허가 품목 「범용 전기 수술기」 ↔ M9 정의 |  |
| `M9-2-2` | 올리지오 |  | M9 기기 리프팅 · RF (고주파) | 맞음 |  | 원천 M9 › RF (고주파) 「모노폴라 RF 에너지를 이용하여 깊은 진피층과 피하지방까지 열을 전달해 즉각적인 콜라겐 수축과 장기간의 신생콜라겐 생성을 유도」 · 허가 품목 「범용전기수술기」 ↔ M9 정의 |  |
| `M9-2-5` | 인모드 |  | M9 기기 리프팅 · RF (고주파) | 맞음 |  | 원천 M9 › RF (고주파) 「InMode Bipolar RF + IR(적외선) 복합 리프팅 기기」 · 허가 품목 「반도체 레이저 수술기 · 범용전기수술기」 ↔ M9 정의 |  |
| `M9-2-3` | 볼뉴머 |  | M9 기기 리프팅 · RF (고주파) | 맞음 |  | 허가 「범용전기수술기」 VOLNEWMER · 원천 M9-2 모노폴라 RF — 합쳐진 M4 볼뉴머(auto-M4-1775362490962)는 원장 중복이었고 M4 정의와 무관 |  |
| `M9-2-4` | 소프라노 티타늄 |  | M8 레이저 | 맞음 |  | 원천 M9 › RF (고주파) 「알마 소프라노 티타늄 — 3파장(755/810/1064nm) 다이오드 레이저 플랫폼으로 제모와 보조적 피부 재생에 사용. 본 」 · 허가 품목 「반도체레이저수술기」 ↔ M9 정의 | 허가 「반도체레이저수술기」 · 원천 「M9-2(RF) 섹션에 잘못 등재」 — 1단계 반영된 M8 이 맞음 |
| `auto-38-1774737181584` | 쿨페이즈 | ○ | M9 기기 리프팅 · RF (고주파) | 맞음 |  | 원천 M9 › RF (고주파) 「모노폴라 RF 에너지를 깊은 진피층과 SMAS까지 전달하여 즉각적인 콜라겐 수축과 장기간의 신생콜라겐 생성을 유도하는 비침습적」 · 허가 품목 「범용 전기 수술기」 ↔ M9 정의 |  |
| `auto-39-1774737181584` | 텐써마 | ○ | M9 기기 리프팅 · RF (고주파) | 맞음 |  | 원천 M9 › RF (고주파) 「모노폴라 RF 에너지로 심부 조직을 가열하여 즉각적인 콜라겐 수축과 장기적 신생 콜라겐 생성을 유도하는 비침습적 리프팅 기기」 · 허가 품목 「범용전기수술기」 ↔ M9 정의 |  |
| `auto-M9-1775361433713` | 버츄RF | ○ | M11 니들RF · 니들RF 장비 | 맞음 |  | 원천 M9 › RF (고주파) 「고주파 에너지를 이용하여 피부 깊숙한 층까지 열을 전달해 콜라겐 재생을 촉진하는 리프팅 시술」 · 허가 품목 「범용 전기 수술기」 ↔ M9 정의 | 허가 「범용 전기 수술기」 VirtueRF · 원천 설명 「미세 바늘을 통해 … 고주파」 — 1단계 반영된 M11 이 맞음 |
| `auto-M9-1775361486532` | 올리지오 X | ○ | M9 기기 리프팅 · RF (고주파) | 맞음 |  | 원천 M9 › RF (고주파) 「클래시스 모노폴라 RF 업그레이드 (GX 입체가열)」 · 허가 품목 「범용전기수술기」 ↔ M9 정의 |  |
| `auto-M9-1775362633910` | 에이전 | ○ | M9 기기 리프팅 · RF (고주파) | 맞음 |  | 원천 M9 › RF (고주파) 「제이시스 모노폴라 RF는 단극 고주파를 이용한 비침습적 피부 리프팅 및 타이트닝 치료 장비입니다.」 ↔ M9 정의 |  |
| `auto-M9-1775362640896` | 써니 | ○ | M9 기기 리프팅 · RF (고주파) | 맞음 |  | 원천 M9 › RF (고주파) 「국산 모노폴라 RF 장비로 진피층 콜라겐 리모델링을 통한 피부 탄력 개선 시술」 · 허가 품목 「범용 전기 수술기」 ↔ M9 정의 |  |
| `auto-M9-1775363058909` | 시크릿맥스 | ○ | M9 기기 리프팅 · RF (고주파) | 여러 계열 | M11 | 원천 「침습+비침습 RF 복합」 — 주 비침습 RF(원천 M9-2) · 침습 RF = 니들RF |  |
| `auto-M9-1775364775130` | 펠레베 | ○ | M9 기기 리프팅 · RF (고주파) | 맞음 |  | 원천 M9 › RF (고주파) 「시너론 모노폴라 RF를 이용한 깊은층 타이트닝」 ↔ M9 정의 |  |
| `auto-M9-1775364775131` | 트라이리프트 | ○ | M9 기기 리프팅 · 복합 에너지 | 여러 계열 | M10 | 원천 「RF와 마이크로커런트 … 근육을 자극」 — 주 RF · 근육 자극 = M10 |  |
| `auto-M9-1775364775132` | 리저브 | ○ | M9 기기 리프팅 · RF (고주파) | 맞음 |  | 원천 M9 › RF (고주파) 「국산 모노폴라 RF를 이용한 경제적인 리프팅 솔루션」 ↔ M9 정의 |  |
| `auto-M9-1775364797157` | 아큐어 | ○ | M9 기기 리프팅 · RF (고주파) | 맞음 |  | 원천 M9 › RF (고주파) 「국산 양극성 RF를 이용한 안전한 리프팅 시술」 ↔ M9 정의 |  |
| `M9-3-1` | 온다 |  | M9 기기 리프팅 · 마이크로웨이브 | 맞음 |  | 원천 M9 › 마이크로웨이브 「극초단파 에너지로 진피층의 수분을 공명시켜 심부 열을 발생, 콜라겐 수축과 신생 콜라겐 생성을 동시에 유도하는 비침습적 리프팅」 · 허가 품목 「극초단파 자극기 · 범용 전기 수술기」 ↔ M9 정의 | 극초단파(마이크로웨이브) — 문헌 M9 이름은 HIFU·RF, 원천 하위 M9-3 유지 |
| `auto-M9-1775364775139` | 클래리파이 | ○ | M9 기기 리프팅 · 마이크로웨이브 | 맞음 |  | 원천 M9 › 마이크로웨이브 「여드름과 피지 관리에 특화된 복합 치료 시술」 ↔ M9 정의 | 원천 하위 「마이크로웨이브」 ↔ 설명 「RF 에너지가 피지선…」 — 어느 쪽이든 M9 에너지, 하위는 확인 필요 |
| `auto-40-1774737181584` | 소프웨이브 | ○ | M9 기기 리프팅 · SUPERB 초음파 | 맞음 |  | 원천 M9 › 복합 에너지 「초음파 에너지를 이용한 비침습적 피부 리프팅 시술로, 민감 부위에 안전하게 적용 가능한 기기」 · 허가 품목 「집속형 초음파 자극 시스템」 ↔ M9 정의 |  |
| `auto-M9-1775360610416` | 포커스듀얼 | ○ | M9 기기 리프팅 · 복합 에너지 | 여러 계열 | M11 | 원천 「HIFU와 니들RF를 결합」 — 주 HIFU(원천 M9-4) · 니들RF 보조 |  |
| `auto-M9-1775360619387` | 듀오타이트 | ○ | M9 기기 리프팅 · HIFU (초음파) | 맞음 |  | 원천 M9 › 복합 에너지 「비올메디컬의 HIFU 신기종 듀오타이트는 이중 초점 기술로 리프팅과 타이트닝을 동시에 제공하는 비침습적 미용시술」 · 허가 품목 「집속형초음파자극시스템」 ↔ M9 정의 |  |
| `auto-M9-1775360627229` | 어센트 프라임 | ○ | M9 기기 리프팅 · RF (고주파) | 맞음 |  | 원천 M9 › 복합 에너지 「클래시스와 RF를 결합한 복합 리프팅 시술로 피부 탄력 개선과 윤곽 정리를 동시에 수행하는 튠페이스 치료」 · 허가 품목 「범용전기수술기」 ↔ M9 정의 |  |
| `auto-M9-1775364775135` | 에브넥 | ○ | M9 기기 리프팅 · 복합 에너지 | 맞음 |  | 원천 M9 › 복합 에너지 「RF와 초음파를 결합한 목 부위 전용 리프팅 장비」 ↔ M9 정의 |  |
| `auto-M9-1775364775136` | 바이캐빈 | ○ | M9 기기 리프팅 · 복합 에너지 | 맞음 |  | 원천 M9-4 「RF와 캐비테이션 … 체형 관리」 — RF 기기(M9) · 지방 감소는 목적(6단계) |  |
| `auto-M9-1775364775137` | 아폴로 | ○ | M9 기기 리프팅 · 복합 에너지 | 맞음 |  | 원천 M9 › 복합 에너지 「다중 에너지를 활용한 종합 리프팅 시스템」 ↔ M9 정의 |  |
| `auto-M10-1775363013079` | 트루스컬프트 | ○ | RF 지방감소 | 옮김 |  | 원천 「1.8MHz RF 에너지가 피하지방층 … 45-50도」 — 근육 자극(M10) 없음, RF 기기 · 지방 감소는 목적(6단계) · 31168833 비침습 체형 기기를 에너지별(cryolipolysis · laser · HIFEM · RF · HIFU)로 나눔 · v3 X6 「RF 지방감소」 = 1차 답 ③ 「EMS 아니라 RF」 |  |
| `auto-M14-1775361047443` | 바넥스 | ○ | M14 크라이오리포라이시스 · 냉각지방분해 | 옮김 |  | 원천 「RF 에너지와 석션을 결합 … 지방 감소」 — 냉각(M14) 기전 없음(사후관리 냉각 문구는 원천 혼입, _RESUME 2단계 메모) · 31168833 |  |
| `auto-M15-1775402736453` | 올타이트 | ○ | M15 메디컬스킨케어 (원천 시술군 M15) | 옮김 |  | 허가 품목 「초단파 자극기」(제인24-927 · 23-5136) · 원천 「RF와 HIFU를 결합한 복합리프팅」 — 외용 관리(M15) 아님 |  |
| `new-DEV-013` | 덴서티 하이 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 2_리프팅) | 옮김 |  | 허가 품목 「범용전기수술기」(고주파 발생 장치) · 현장 사진 폴더 2_리프팅 — RF 리프팅 기기 |  |
| `new-DEV-021` | 세르프 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 2_리프팅) | 옮김 |  | 허가 품목 「범용전기수술기」(고주파 발생 장치) · 현장 사진 폴더 2_리프팅 — RF 리프팅 기기 |  |
| `new-DEV-024` | 덴서티 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 2_리프팅) | 옮김 |  | 허가 품목 「범용전기수술기」(고주파 발생 장치) · 현장 사진 폴더 2_리프팅 — RF 리프팅 기기 |  |
| `new-DEV-027` | 리니어지 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 2_리프팅) | 옮김 |  | 허가 품목 「집속형초음파자극시스템」(HIFU) · 사진 폴더 2_리프팅/6_피부관리 |  |
| `new-DEV-031` | 울핏 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 2_리프팅) | 옮김 |  | 허가 품목 「집속형초음파자극시스템」(HIFU) · 사진 폴더 2_리프팅/6_피부관리 |  |
| `new-DEV-039` | 스텔라듀오 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 6_피부관리) | 옮김 |  | 허가 품목 「집속형초음파자극시스템」(HIFU) · 사진 폴더 2_리프팅/6_피부관리 |  |
| `new-DEV-047` | 울킨 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 6_피부관리) | 옮김 |  | web4 「1/3/10MHz HIFU+고밀도 듀얼 초음파 피부미용 기기」 · 제조사 「의료 기기가 아니며」 — HIFU 기기(허가 대상 아님은 1단계 상태) |  |

### M10 HIFEM·EMS 근육 자극 — 8행

| ledger_id | 이름 | auto | 현재 | 판정 | 보조 계열 | 근거 | 메모 |
|---|---|---|---|---|---|---|---|
| `M10-1-1` | 엠페이스 |  | M10 HIFES/EMS · 페이셜 EMS | 여러 계열 | M9 | 허가 「범용전기수술기」 EMFACE · 원천 「RF와 HIFES를 결합」 — 주 HIFES(원천 M10-1) · RF 보조 |  |
| `M10-2-1` | 엠스컬프트 |  | M10 HIFES/EMS · 바디 EMS | 맞음 |  | 원천 M10 › 바디 EMS 「HIFEM 기술로 근육 강화와 지방 감소를 동시 달성」 · 허가 품목 「의료용전자기발생기 · 초단파 자극기」 ↔ M10 정의 |  |
| `M10-2-2` | 엠스컬프트 네오 |  | M10 HIFES/EMS · 바디 EMS | 여러 계열 | M9 | 원천 「HIFEM+RF 결합」 — 주 HIFEM · RF 보조 |  |
| `auto-M10-1775361916636` | 바넥스프로 | ○ | M10 HIFES/EMS · 바디 EMS | 여러 계열 | M9 | 원천 「RF 고주파, EMS 근육자극, 석션」 — 근육 자극 있어 M10 주, RF 는 M9 · 지방 감소는 목적 |  |
| `auto-M10-1775363005172` | 이볼브 | ○ | M10 HIFES/EMS · 바디 EMS | 여러 계열 | M9 | 원천 「RF와 EMS를 결합한 바디 컨투어링」 — 원천 M10 유지 · RF 보조 |  |
| `auto-M10-1775363019549` | 쿨톤 | ○ | M10 HIFES/EMS · 바디 EMS | 맞음 |  | 원천 M10 › 바디 EMS 「앨러간의 크라이오리폴리시스와 EMS 근육자극을 결합한 체형관리 시술」 ↔ M10 정의 | 원천 설명에 「크라이오리폴리시스」와 「EMS 근육자극」이 섞임 — 근육 자극 기준 M10, 원천 설명 확인 대상 |
| `auto-M10-1775364775185` | 스팀슈어 | ○ | M10 HIFES/EMS · 바디 EMS | 여러 계열 | M9 | 원천 「RF와 EMS를 결합」 — 원천 M10 유지 · RF 보조 |  |
| `new-DEV-020` | 엔진 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 2_리프팅) | 여러 계열 | M9 | web4 「EMS(근육 전기자극)+RF(고주파) 동시 조사 패치형 얼굴 리프팅」 — EMFACE(M10 페이셜) 와 같은 구성, 주 M10 · RF 는 M9 |  |

### M11 고주파 마이크로니들(니들RF) — 13행

| ledger_id | 이름 | auto | 현재 | 판정 | 보조 계열 | 근거 | 메모 |
|---|---|---|---|---|---|---|---|
| `M11-1-1` | 포텐자 |  | M11 니들RF · 니들RF 장비 | 맞음 |  | 원천 M11 › 니들RF 장비 「절연 마이크로니들 + 펄스 RF 복합 시술」 · 허가 품목 「범용전기수술기」 ↔ M11 정의 |  |
| `M11-1-2` | 시크릿 RF |  | M11 니들RF · 니들RF 장비 | 맞음 |  | 원천 M11 › 니들RF 장비 「절연 마이크로니들 기반 분획 RF 시술」 · 허가 품목 「범용전기수술기」 ↔ M11 정의 |  |
| `M11-1-3` | 실펌 X |  | M11 니들RF · 니들RF 장비 | 맞음 |  | 원천 M11 › 니들RF 장비 「Viol/Jeisys 모노폴라 RF 마이크로니들 기기」 · 허가 품목 「범용 전기 수술기 · 범용전기수술기」 ↔ M11 정의 |  |
| `M11-1-4` | 모르페우스8 |  | M11 니들RF · 니들RF 장비 | 맞음 |  | 원천 M11 › 니들RF 장비 「절연 마이크로니들 + 분획 RF 플랫폼」 ↔ M11 정의 |  |
| `auto-43-1774737181584` | 쿼드세이 | ○ | M11 니들RF · 니들RF 장비 | 맞음 |  | 원천 M11 › 니들RF 장비 「다층 분획 RF 에너지 시술」 · 허가 품목 「범용 전기 수술기」 ↔ M11 정의 |  |
| `auto-M11-1775360510687` | 트윈픽셀 | ○ | M11 니들RF · 니들RF 장비 | 여러 계열 | M15 | 원천 「RF마이크로니들과 이온도입」 — 주 니들RF · 이온 도입 = 외용 흡수 보조(M15, D09) |  |
| `auto-M11-1775360637715` | 스칼렛 프로 | ○ | M11 니들RF · 니들RF 장비 | 맞음 |  | 원천 M11 › 니들RF 장비 「마이크로 니들과 RF 에너지를 결합한 차세대 피부재생 및 리프팅 시술」 · 허가 품목 「범용 전기 수술기」 ↔ M11 정의 |  |
| `auto-M11-1775360645191` | 셀리뉴 | ○ | M9 기기 리프팅 · RF (고주파) | 맞음 |  | 원천 M11 › 니들RF 장비 「모노폴라 RF 기술을 이용한 비침습적 피부 리프팅 및 타이트닝 시술」 · 허가 품목 「범용 전기 수술기」 ↔ M11 정의 | 허가 「범용 전기 수술기」 · 원천 설명 「비침습적 … 모노폴라 RF」 — 1단계 반영된 M9 가 맞음 |
| `auto-M11-1775361447933` | 비바체 | ○ | M11 니들RF · 니들RF 장비 | 여러 계열 | M8 | 원천 「RF 마이크로니들과 LED를 결합」 — 주 니들RF · LED 보조(D04 이면 M8) |  |
| `auto-M11-1775364775142` | 아그네스 | ○ | M11 니들RF · 니들RF 장비 | 맞음 |  | 원천 M11 › 니들RF 장비 「여드름 피지선을 타겟으로 하는 니들 RF 전용 장비」 · 허가 품목 「범용전기수술기」 ↔ M11 정의 |  |
| `auto-M11-1775364775143` | 인피니 | ○ | M11 니들RF · 니들RF 장비 | 맞음 |  | 원천 M11 › 니들RF 장비 「루트로닉의 3차원 니들 RF 시스템」 · 허가 품목 「범용전기수술기」 ↔ M11 정의 |  |
| `auto-M11-1775364775144` | 프라임RF | ○ | M11 니들RF · 니들RF 장비 | 맞음 |  | 원천 M11 › 니들RF 장비 「국산 기술로 개발된 니들 RF 장비」 ↔ M11 정의 |  |
| `M11-P-1` | 인트라셀 |  | M11 니들RF | 맞음 |  | 원천 M11 › products 「절연 마이크로니들 분획 RF 시술」 ↔ M11 정의 |  |

### M12 마이크로니들링(MTS) — 3행

| ledger_id | 이름 | auto | 현재 | 판정 | 보조 계열 | 근거 | 메모 |
|---|---|---|---|---|---|---|---|
| `auto-M12-1775363026852` | 더마펜4 | ○ | M12 마이크로니들링(MTS) · 전동 MTS | 맞음 |  | 원천 M12 › 전동 MTS 「16개 초미세 바늘이 장착된 전동 마이크로니들링 장비로 피부 재생과 콜라겐 합성을 촉진하는 미용의학 시술 도구」 ↔ M12 정의 |  |
| `auto-M12-1775363035813` | 스킨스탬프 | ○ | M12 마이크로니들링(MTS) · 전동 MTS | 맞음 |  | 원천 M12 › 전동 MTS 「미세바늘을 이용해 피부에 미세한 천공을 만들어 콜라겐 생성을 촉진하는 피부 재생 시술」 ↔ M12 정의 |  |
| `new-DEV-053` | 오토 MTS |  | 원천 시술군 없음(현장 기기 · 사진 폴더 5_약물흡수) | 옮김 |  | 허가 품목 「의약품 흡수 유도 피부 자극기」(제인 10-343, 니들) · 본체 「약물흡수유도용피부자극기」 조합(제인 12-1425) — 전동 마이크로니들링 |  |

### M13 플라즈마 — 3행

| ledger_id | 이름 | auto | 현재 | 판정 | 보조 계열 | 근거 | 메모 |
|---|---|---|---|---|---|---|---|
| `auto-M13-1775361440978` | 플라듀오 | ○ | M13 플라즈마 · 핫플라즈마 | 맞음 |  | 원천 M13 › 핫플라즈마 「뜨거운 플라즈마와 차가운 플라즈마를 동시에 사용하여 피부 재생과 탄력 개선을 도모하는 듀얼 플라즈마 시술」 · 허가 품목 「전기 수술 장치」 ↔ M13 정의 |  |
| `auto-M13-1775364775141` | 뉴라클플라즈마 | ○ | M13 플라즈마 · 핫플라즈마 | 맞음 |  | 원천 M13 › 핫플라즈마 「플라즈마 에너지를 이용한 비수술적 눈꺼풀 리프팅 시술」 ↔ M13 정의 |  |
| `auto-M13-1775364775140` | 플라스젠 | ○ | M13 플라즈마 · 콜드플라즈마 | 맞음 |  | 원천 M13 › 콜드플라즈마 「플라즈마 기술로 약물 침투를 촉진하는 피부 전달 시스템」 ↔ M13 정의 |  |

### M14 냉동지방분해 — 3행

| ledger_id | 이름 | auto | 현재 | 판정 | 보조 계열 | 근거 | 메모 |
|---|---|---|---|---|---|---|---|
| `M14-1-1` | 쿨스컬프팅 |  | M14 크라이오리포라이시스 · 냉각지방분해 | 맞음 |  | 원천 M14 › 냉각지방분해 「엘러간의 냉동 지방분해 기술 기반 비수술적 지방감소 시술」 · 허가 품목 「의료용저온기」 ↔ M14 정의 |  |
| `auto-M14-1775363067062` | 쿨미니 | ○ | M14 크라이오리포라이시스 · 냉각지방분해 | 맞음 |  | 원천 M14 › 냉각지방분해 「이중턱 지방세포를 선택적으로 파괴하는 비침습적 냉각지방분해 장비」 · 허가 품목 「의료용저온기」 ↔ M14 정의 |  |
| `auto-M14-1775364775188` | 크라이오듀얼 | ○ | M14 크라이오리포라이시스 · 냉각지방분해 | 맞음 |  | 원천 M14 › 냉각지방분해 「양쪽을 동시에 시술하는 듀얼 냉각 지방 분해 시스템」 ↔ M14 정의 |  |

### M15 외용 관리 — 55행

| ledger_id | 이름 | auto | 현재 | 판정 | 보조 계열 | 근거 | 메모 |
|---|---|---|---|---|---|---|---|
| `M15-1-3` | 알라딘필링 |  | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「위축성 흉터 전문 포인트 필링」 ↔ M15 정의 |  |
| `M15-1-4` | 블랙필 |  | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「글리콜산 기반 표재성 필링」 ↔ M15 정의 |  |
| `M15-1-6` | 핑크필 |  | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「복합산 마이크로필링」 ↔ M15 정의 |  |
| `M15-1-7` | 라라필 |  | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「효소 기반 온순한 필링」 ↔ M15 정의 |  |
| `auto-46-1774737181584` | 호박필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「유산 기반 온순 필링」 ↔ M15 정의 |  |
| `auto-47-1774737181584` | 밀크필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「워터제트 기반 물리적 클렌징」 ↔ M15 정의 | 원천 설명 「워터제트 기반 물리적 클렌징」 — 하위는 화학 박피가 아니라 기계적 박리·클렌징 |
| `auto-M15-1775361455669` | 닥토필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「5세대 내추럴필링과 엑소좀을 결합한 페이스/바디/두피 종합 재생 시술」 ↔ M15 정의 |  |
| `auto-M15-1775364775115` | 미라필링 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「산호 칼슘 미세침을 이용한 물리적 각질 제거 및 재생 시술」 ↔ M15 정의 | 원천 설명 「산호 칼슘 미세침 … 물리적 각질 제거」 — 하위 기계적 박리 |
| `auto-M15-1775364775116` | 블랙필링 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「TCA와 살리실산이 복합된 중강도 화학 박피」 ↔ M15 정의 |  |
| `auto-M15-1775364775117` | 옐로우필링 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「레티놀 복합성분을 이용한 화학적 박피술」 ↔ M15 정의 |  |
| `auto-M15-1775364775118` | 솔코세릴필링 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「천연 성분을 이용한 순한 화학적 박피술」 ↔ M15 정의 |  |
| `auto-M15-1775401624105` | 여우필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「여드름, 미백, 탄력을 동시에 개선하는 복합 화학박피 시술」 ↔ M15 정의 |  |
| `auto-M15-1775401631147` | 플라필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「PHA와 LHA, 백금 성분을 결합한 초저자극 화학 필링으로 속건조 개선과 항산화 효과를 제공하는 피부과 시술」 ↔ M15 정의 |  |
| `auto-M15-1775401638316` | 산소필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「비타민과 산소를 공급하여 혈액순환을 개선하고 미백, 탄력, 항노화 효과를 제공하는 저자극 필링」 ↔ M15 정의 |  |
| `auto-M15-1775401645338` | PRX필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「TCA, 과산화수소, 코직산을 결합한 비박리성 화학필링으로 피부 재생과 미백을 동시에 제공하는 바이오리버탈라이징 시술」 ↔ M15 정의 |  |
| `auto-M15-1775401653479` | CO2필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「탄산가스를 이용해 피부의 산소공급을 촉진하고 노폐물 배출을 도와 피부결 개선을 목적으로 하는 비침습적 필링 시술」 ↔ M15 정의 | 원천 「탄산팩 · 탄산가스를 이용 … 비침습적 필링」 — 바르는 탄산팩(외용), 카복시 주입(X2)과 다름 |
| `auto-M15-1775401662170` | 예스필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「민감성 피부를 위한 저자극 화학 필링으로 피부장벽 강화와 순한 각질 제거를 동시에 제공하는 전용 필링 시술」 ↔ M15 정의 |  |
| `auto-M15-1775401677251` | 해초필 | ○ | M15 메디컬스킨케어 · 물리필링(해면체 미세침) (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「담수해면체 미세침을 이용한 물리적 각질제거 및 피부재생 유도 소프트 필링」 ↔ M15 정의 | 원천 「담수해면체 미세침 … 물리적 각질제거」 — 하위 기계적 박리 |
| `auto-M15-1775401685107` | 그린필 | ○ | M15 메디컬스킨케어 · 허벌 필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「독일산 천연 허브 성분을 이용한 기계적 박피술로 피부 재생과 개선을 도모하는 전문 필링 시술」 ↔ M15 정의 |  |
| `auto-M15-1775401692083` | 퀸즈필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「PHA 기반의 순한 각질 제거와 동시에 히알루론산, 펩타이드, 아미노산으로 피부 영양을 공급하는 복합 필링 시술」 ↔ M15 정의 |  |
| `auto-M15-1775401700008` | 살몬필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「연어 유래 PDRN 성분으로 피부 재생과 보습, 항염 효과를 제공하는 메조테라피 필링」 ↔ M15 정의 | 원천 「연어 PDRN … 메조테라피 필링」 — 바르는 필링이면 M15, 주입이면 M4(원천 확인 대상) |
| `auto-M15-1775401716456` | 미라클필링 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「담수해면체 스피큘을 이용한 물리적 각질제거와 천연 성분의 화학적 필링을 결합한 복합 재생 시술」 ↔ M15 정의 | 원천 「담수해면체 스피큘 … 물리적 각질제거와 … 화학적 필링」 — 하위 기계적 박리(복합) |
| `auto-M15-1775401722628` | FCR필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「발효 복합 성분을 활용한 재생 촉진형 화학 필링으로 피부 턴오버를 개선하는 시술」 ↔ M15 정의 |  |
| `auto-M15-1775401738092` | 디멜라필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「산소와 비타민C를 결합한 미백 및 항노화 전문 화학적 필링 시술」 ↔ M15 정의 |  |
| `auto-M15-1775401745461` | 생크림필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「생크림 같은 부드러운 텍스처로 각질을 온화하게 녹이면서 보습과 톤업 효과를 동시에 제공하는 저자극 필링」 ↔ M15 정의 |  |
| `auto-M15-1775401753203` | 우유필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「우유단백 유래 락틱산을 이용한 순한 화학적 필링으로 건성피부의 각질제거와 보습을 동시에 제공하는 시술」 ↔ M15 정의 |  |
| `auto-M15-1775401760736` | 베이비필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「초저자극 성분으로 민감피부와 아토피 피부에도 적용 가능한 순한 화학 필링」 ↔ M15 정의 |  |
| `auto-M15-1775401767756` | 골드필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「금 나노입자를 활용한 프리미엄 안티에이징 케미컬 필링 시술」 ↔ M15 정의 |  |
| `auto-M15-1775401773800` | 마꾸필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「마그네슘과 구리 복합체를 이용한 미네랄 공급 피부 재생 필링」 ↔ M15 정의 |  |
| `auto-M15-1775401788467` | 라라닥터 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「5세대 LHA와 PLLA 복합체를 활용한 콜라겐 재생 촉진 의료용 필링 시술」 ↔ M15 정의 |  |
| `auto-M15-1775402057372` | 크랜베리필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「크랜베리 추출 과일산을 이용한 항산화 성분이 함유된 순한 각질 제거 필링」 ↔ M15 정의 |  |
| `auto-M15-1775402064126` | 체리필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「체리 추출 과일산과 비타민을 활용한 순한 화학적 각질제거 필링」 ↔ M15 정의 |  |
| `auto-M15-1775402078232` | ASA필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「해조류 추출물과 미세침을 이용한 순한 각질제거 및 피부재생 필링」 ↔ M15 정의 | 원천 「해조류 추출물과 미세침」 — 하위 기계적 박리 |
| `auto-M15-1775402083474` | 탄앤막필링 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「알칼리 촉매를 이용한 표피재생과 보호막 형성의 2단계 필링 시술」 ↔ M15 정의 |  |
| `auto-M15-1775402093377` | 이지피틱필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「피틱산 기반의 항산화, 미백, 저자극 화학적 필링 시술」 ↔ M15 정의 |  |
| `auto-M15-1775402100474` | 아미노필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「아미노산 기반의 순한 영양 공급형 각질제거 필링으로 민감한 피부에도 적용 가능한 저자극 케어」 ↔ M15 정의 |  |
| `auto-M15-1775402107402` | 쿰스필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「제스너 솔루션을 변형한 AHA+BHA 혼합 화학 필링으로 여드름과 모공 개선에 효과적」 ↔ M15 정의 |  |
| `auto-M15-1775402113508` | 진주필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「진주 분말을 활용한 미백과 영양 공급을 통해 피부 광채를 개선하는 순한 필링 시술」 ↔ M15 정의 |  |
| `auto-M15-1775402120118` | 콜라겐필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 케미컬필링 「콜라겐 성분을 피부 깊숙이 침투시켜 탄력 개선과 재생을 돕는 피부과 전용 필링 시술」 ↔ M15 정의 |  |
| `M15-2-1` | 아쿠아필 |  | M15 메디컬스킨케어 · 딥클렌징 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 딥클렌징 「3단계 통합 클렌징+보습+영양」 · 허가 품목 「전동식의료용흡인기」 ↔ M15 정의 |  |
| `M15-2-2` | 하이드라페이셜 |  | M15 메디컬스킨케어 · 딥클렌징 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 딥클렌징 「마이크로젯 기반 심층 클렌징」 · 허가 품목 「의료용삭피장치」 ↔ M15 정의 |  |
| `auto-48-1774737181584` | 라라젯 | ○ | M15 메디컬스킨케어 · 딥클렌징 (원천 시술군 M15) | 여러 계열 | M4 | 원천 「공기압 딥클렌징 … 약물을 피부에 주입하는 기능도 겸한다」 + 합쳐진 주입장비 라라젯(auto-52) — 주 클렌징 · 주입 = M4 |  |
| `auto-M15-1775362958625` | 옥시덤 | ○ | M15 메디컬스킨케어 · 딥클렌징 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 딥클렌징 「산소를 고압으로 피부 깊숙이 주입하여 세포 재생과 콜라겐 생성을 촉진하는 비침습적 미용 시술」 ↔ M15 정의 |  |
| `auto-M15-1775362965286` | 제트필 | ○ | M15 메디컬스킨케어 · 딥클렌징 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 딥클렌징 「고압 물 분사를 이용하여 모공 깊숙한 각질과 노폐물을 제거하는 비침습적 딥클렌징 시술」 ↔ M15 정의 |  |
| `auto-M15-1775362971889` | 아쿠아퓨어 | ○ | M15 메디컬스킨케어 · 딥클렌징 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 딥클렌징 「미세한 물 흡인과 동시에 유효성분을 피부에 도포하는 하이드라 필링 시술」 · 허가 품목 「전동식 의료용 흡인기」 ↔ M15 정의 |  |
| `auto-M15-1775362978512` | 실크필 | ○ | M15 메디컬스킨케어 · 딥클렌징 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 딥클렌징 「실크 단백질을 이용한 피부 재생 및 약물 전달 시스템으로 자연스러운 피부 개선을 도모하는 시술」 ↔ M15 정의 |  |
| `M15-4-1` | LDM |  | M15 메디컬스킨케어 · 초음파관리 (원천 시술군 M15) | 맞음 |  | 허가 「초음파자극기」 LDM-Triple · 원천 M15-4 「저주파 초음파 … 각질층의 수분 흡수율 증가」 — 합쳐진 M16 「LDM초음파관리」는 수액이 아님. M15 유지는 D09 판단에 묶임 |  |
| `auto-M15-1775364775167` | 소노퀸 | ○ | M9 기기 리프팅 · HIFU (초음파) (원천 시술군 M15) | 맞음 |  | 원천 M15 › 초음파관리 「초음파와 석션을 결합한 복합 피부 관리 시술」 · 허가 품목 「집속형초음파자극시스템」 ↔ M15 정의 | 허가 「집속형초음파자극시스템」(NP-100) — 원천은 M15 초음파관리였으나 현재 계열 M9 가 허가와 맞음 |
| `M15-6-4` | 벨라소닉 |  | M15 메디컬스킨케어 · 주입장비 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 주입장비 「초음파 에너지로 약물 침투 촉진 및 재생」 · 허가 품목 「초음파자극기」 ↔ M15 정의 | 허가 「초음파자극기」 BELLA SONIC 2X — 원천은 주입장비지만 바늘·제트 없이 초음파 흡수 보조(D09) |
| `auto-M15-1775402654237` | 제네오X | ○ | M15 메디컬스킨케어 (원천 시술군 M15) | 맞음 |  | 원천 M15 › 시그니처프로그램 「산소공급, 초음파, 마사지를 결합한 3in1 복합 피부관리 시술」 ↔ M15 정의 | 원천 시그니처 「옥시제네오 · 초음파 · 마사지」 · 1단계 D17 국문 브로슈어 OxyGeneo · LUX · LIFT — 박리+영양 도입(M15 기계적 박리) |
| `new-DEV-044` | 힐퓨전 프로 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 6_피부관리) | 옮김 |  | web4 「워터젯 하이드로더마브레이전+흡입+솔루션 주입」 — 하이드로더마브레이전(M15 기계적 박리·클렌징) · 19146604 |  |
| `new-DEV-045` | 크라이오 멀티마스터 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 6_피부관리) | 옮김 |  | web4 「냉·온열+초음파+이온토+전기천공+스킨스크러버 6-in-1 프리/애프터 피부관리」 — 외용 흡수 보조 기기(D09) · 「크라이오」는 냉동지방분해(M14) 아님 |  |
| `new-DEV-049` | 오투덤 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 6_피부관리) | 옮김 |  | 기사 「산소이온발생기 … 미용기기」 — 피부 표면 산소 관리(원천 M15-2 옥시덤과 같은 종류) |  |
| `new-DEV-056` | 소노케어 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 5_약물흡수) | 옮김 |  | 허가 품목 「초음파자극기」(LDM · 벨라소닉과 같은 품목) — D09 |  |
| `auto-M15-1775364775171` | 콘투락투벡스 | ○ | M15 | 맞음 |  | 원천 M15 › 흉터 전용 「양파 추출물 기반 흉터 개선 전용 연고」 · 허가 품목 「일반의약품 · 기타의 조직세포의 기능용의약품」 ↔ M15 정의 | 허가 「콘투락투벡스겔」 일반의약품(알란토인 · 헤파린) — 외용 의약품(M15 외용제) |

### M17 줄기세포·줄기세포 유래 제제 — 5행

| ledger_id | 이름 | auto | 현재 | 판정 | 보조 계열 | 근거 | 메모 |
|---|---|---|---|---|---|---|---|
| `auto-M17-1775364775191` | AAPE | ○ | M17 줄기세포치료 · 줄기세포배양액 (원천 시술군 M17) | 맞음 |  | 원천 M17 › 엑소좀 「지방줄기세포 추출단백질을 이용한 고농도 재생치료」 ↔ M17 정의 | 원천 「지방유래 줄기세포에서 추출한 고농도 단백질」 — M17 배양액·추출물 |
| `auto-61-1774737181584` | 노바스템 | ○ | M17 줄기세포치료 · 자가혈유래 줄기세포 (원천 시술군 M17) | 맞음 |  | 원천 M17 › 자가혈유래 줄기세포 「줄기세포 유래 재생인자 제품」 ↔ M17 정의 | 원천 하위 「자가혈유래 줄기세포」 ↔ 설명 「ADSC 배양에서 추출한 성장인자」 — 원천 확인 대상 |
| `auto-62-1774737181584` | 미라셀 | ○ | M17 줄기세포치료 · 자가혈유래 줄기세포 (원천 시술군 M17) | 맞음 |  | 원천 M17 › 자가혈유래 줄기세포 「줄기세포 유래 성장인자 제제」 ↔ M17 정의 | 원천 하위 「자가혈유래 줄기세포」 ↔ 설명 「ADSC 배양액 유래 성장인자」 — 원천 확인 대상 |
| `M17-P-0` | 큐어스킨 |  | M17 줄기세포치료 | 맞음 |  | 원천 M17 › products 「줄기세포 유래 재생 바이오솔루션」 ↔ M17 정의 |  |
| `M17-P-1` | 에스에프 |  | M17 줄기세포치료 | 맞음 |  | 원천 M17 › products 「줄기세포 유래 주사용 재생제제」 ↔ M17 정의 |  |

### N1 지방분해 주사 — 10행

| ledger_id | 이름 | auto | 현재 | 판정 | 보조 계열 | 근거 | 메모 |
|---|---|---|---|---|---|---|---|
| `auto-M16-1775403016892` | 브이올렛 | ○ | 국소 지방분해주사 (원천 시술군 M16) | 옮김 |  | 원천 M16-DCA 「데옥시콜산(DCA)이 지방세포막을 … 파괴」 ↔ M16 문헌 정의는 정맥 미량영양소(literature M16.name) — 투여 경로(피하)·작용(지방세포 용해)이 다름 · 27785706 |  |
| `auto-M16-1775403024925` | 벨카이라 | ○ | 피하 지방분해주사 (원천 시술군 M16) | 옮김 |  | 원천 M16-DCA 「데옥시콜산(DCA)이 지방세포막을 … 파괴」 ↔ M16 문헌 정의는 정맥 미량영양소(literature M16.name) — 투여 경로(피하)·작용(지방세포 용해)이 다름 · 27785706 |  |
| `auto-M16-1775403142279` | 벨라콜린 | ○ | 국소 지방분해주사 (원천 시술군 M16) | 옮김 |  | 원천 M16-DCA 「데옥시콜산(DCA)이 지방세포막을 … 파괴」 ↔ M16 문헌 정의는 정맥 미량영양소(literature M16.name) — 투여 경로(피하)·작용(지방세포 용해)이 다름 · 27785706 |  |
| `auto-M16-DCA-1775404043062` | 올리핏 | ○ | 피하 지방분해주사 (원천 시술군 M16) | 옮김 |  | 원천 M16-DCA 「데옥시콜산(DCA)이 지방세포막을 … 파괴」 ↔ M16 문헌 정의는 정맥 미량영양소(literature M16.name) — 투여 경로(피하)·작용(지방세포 용해)이 다름 · 27785706 |  |
| `auto-M16-DCA-1775404043063` | 펜카이라 | ○ | M16 수액치료 · DCA (지방세포파괴) (원천 시술군 M16) | 옮김 |  | 원천 M16-DCA 「데옥시콜산(DCA)이 지방세포막을 … 파괴」 ↔ M16 문헌 정의는 정맥 미량영양소(literature M16.name) — 투여 경로(피하)·작용(지방세포 용해)이 다름 · 27785706 |  |
| `auto-M16-DCA-1775404043064` | 바이블 | ○ | M16 수액치료 · DCA (지방세포파괴) (원천 시술군 M16) | 옮김 |  | 원천 M16-DCA 「데옥시콜산(DCA)이 지방세포막을 … 파괴」 ↔ M16 문헌 정의는 정맥 미량영양소(literature M16.name) — 투여 경로(피하)·작용(지방세포 용해)이 다름 · 27785706 |  |
| `auto-M16-DCA-1775404043065` | 밀리핏 | ○ | 국소 지방분해주사 (원천 시술군 M16) | 옮김 |  | 원천 M16-DCA 「데옥시콜산(DCA)이 지방세포막을 … 파괴」 ↔ M16 문헌 정의는 정맥 미량영양소(literature M16.name) — 투여 경로(피하)·작용(지방세포 용해)이 다름 · 27785706 |  |
| `auto-M16-DCA-1775404043066` | 원더브이 | ○ | 국소 지방분해주사 (원천 시술군 M16) | 옮김 |  | 원천 M16-DCA 「데옥시콜산(DCA)이 지방세포막을 … 파괴」 ↔ M16 문헌 정의는 정맥 미량영양소(literature M16.name) — 투여 경로(피하)·작용(지방세포 용해)이 다름 · 27785706 |  |
| `auto-M16-DCA-1775404043067` | 리포린 | ○ | M16 수액치료 · DCA (지방세포파괴) (원천 시술군 M16) | 옮김 |  | 원천 M16-DCA 「데옥시콜산(DCA)이 지방세포막을 … 파괴」 ↔ M16 문헌 정의는 정맥 미량영양소(literature M16.name) — 투여 경로(피하)·작용(지방세포 용해)이 다름 · 27785706 |  |
| `auto-M16-DCA-1775404043068` | 뉴비쥬 | ○ | 콜산(CA) 국소 지방분해제 (원천 시술군 M16) | 옮김 |  | 원천 M16-DCA 뉴비쥬 「콜산(CA) 성분 … 지방분해 신약」 · 허가 「뉴비쥬주(콜산)」 ↔ M16 정의(정맥 영양) 밖 · 27785706 · 38297988 |  |

### 계열 밖 — 7행

| ledger_id | 이름 | auto | 현재 | 판정 | 보조 계열 | 근거 | 메모 |
|---|---|---|---|---|---|---|---|
| `auto-M16-1775364775098` | 멜스몬 | ○ | 피하주사용 태반제제 (원천 시술군 M16) | 옮김 |  | 허가 「멜스몬주(자하거추출물)」 — 미량영양소 아님(M16 정의 밖) · 미용 독립 분야 문헌 확인 안 됨 |  |
| `new-DEV-071` | 미라쥬 |  | 진단 장비 (원천 시술군 없음 · 사진 폴더 7_피부진단) | 옮김 |  | 진단 장비(1단계 10-27 「진단 장비 4 는 「진단 장비」」) — 허가 「체외형 의료용 카메라」(메타뷰·마크뷰) · web4 「3D 얼굴 스캐너 … 상담 시스템」(미라쥬) · 「피부 측정 AI 스캔」(스케나) — 시술 계열이 아니라 진단 노드 |  |
| `new-DEV-072` | 3D 메타뷰 |  | 진단 장비 (원천 시술군 없음 · 사진 폴더 7_피부진단) | 옮김 |  | 진단 장비(1단계 10-27 「진단 장비 4 는 「진단 장비」」) — 허가 「체외형 의료용 카메라」(메타뷰·마크뷰) · web4 「3D 얼굴 스캐너 … 상담 시스템」(미라쥬) · 「피부 측정 AI 스캔」(스케나) — 시술 계열이 아니라 진단 노드 |  |
| `new-DEV-073` | 마크뷰 |  | 진단 장비 (원천 시술군 없음 · 사진 폴더 7_피부진단) | 옮김 |  | 진단 장비(1단계 10-27 「진단 장비 4 는 「진단 장비」」) — 허가 「체외형 의료용 카메라」(메타뷰·마크뷰) · web4 「3D 얼굴 스캐너 … 상담 시스템」(미라쥬) · 「피부 측정 AI 스캔」(스케나) — 시술 계열이 아니라 진단 노드 |  |
| `new-DEV-074` | 스케나 |  | 진단 장비 (원천 시술군 없음 · 사진 폴더 7_피부진단) | 옮김 |  | 진단 장비(1단계 10-27 「진단 장비 4 는 「진단 장비」」) — 허가 「체외형 의료용 카메라」(메타뷰·마크뷰) · web4 「3D 얼굴 스캐너 … 상담 시스템」(미라쥬) · 「피부 측정 AI 스캔」(스케나) — 시술 계열이 아니라 진단 노드 |  |
| `M16-3-1` | 라이넥 |  | M16 | 옮김 |  | 허가 「라이넥주」 KPIC 분류 「Human Placenta Hydrolysate : 소화기계질환 > 간장ㆍ담낭ㆍ췌장질환 치료 > 간보호제」 — 미량영양소 아님(M16 정의 밖) · 미용 독립 분야 문헌 확인 안 됨(PubMed 「human placental extract injection」·「Laennec placenta」 검색에 미용 리뷰 0) |  |
| `auto-M15-1775361951923` | 아큐탄 | ○ | M15 | 옮김 |  | 원천 여드름 전용 「경구 이소트레티노인」 — 먹는 처방약(전신 약물치료), 시술 아님 · 37649956 「Oral Isotretinoin and Its Uses in Dermatology」 |  |

### 판단 필요 — 6행

| ledger_id | 이름 | auto | 현재 | 판정 | 보조 계열 | 근거 | 메모 |
|---|---|---|---|---|---|---|---|
| `auto-M15-1775401780659` | 알렉스필 | ○ | M15 메디컬스킨케어 · 케미컬필링 (원천 시술군 M15) | 판단 필요 |  | 원천 케미컬필링이나 설명이 「알렉산드라이트 레이저의 755nm 파장이 멜라닌에 … 흡수」 — 필링 제품인지 레이저 시술 이름인지 원천 확인 필요(M15 ↔ M8) |  |
| `auto-M15-1775364775178` | 헤어셀 | ○ | M15 메디컬스킨케어 · 탈모(비수술) (원천 시술군 M15) | 판단 필요 |  | 허가 품목 「의료용전자기발생기」 H-Cell ST(1단계 D18: 원장 LED→자기장 오류) — 17 정의 어디에도 안 듦 · 독립 분야 문헌 확인 안 됨 → 추천은 계열 밖 |  |
| `new-DEV-015` | 이브타이탄 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 2_리프팅) | 판단 필요 |  | 허가 품목 「3등급 의료용 조합 자극기」(제허24-481)만 — 어떤 에너지(전기 자극 · RF …)인지 출처 확인 안 됨 |  |
| `new-DEV-034` | 벨르업 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 2_리프팅) | 판단 필요 |  | 정체 확인 안 됨 — 판매처 페이지에 원리 · 구분 문구 없음(1단계 기록) · 사진 폴더 2_리프팅만 |  |
| `new-DEV-042` | 더마큐어 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 6_피부관리) | 판단 필요 |  | 정체 확인 안 됨 — 이름 든 허가(제허22-692 「이학 진료용 기구」)는 수출용이라 연결 안 됨(1단계) · 원리 출처 없음 |  |
| `new-DEV-052` | 트리필 프로 |  | 원천 시술군 없음(현장 기기 · 사진 폴더 5_약물흡수) | 판단 필요 |  | web4 「CO2 가스 박리(서브시전)+약물(스킨부스터·PLLA 등) 순차 주입」 — 카복시(X2) 를 계열로 세울지(D10)에 따라 X2 / M4(약물 주입 기기) 갈림 |  |

## 7. 원천 확인 대상(설명 ↔ 허가·하위 충돌 — 계열 판정에는 영향 없음)

- 큐젤 맥스(`auto-M2-1775361728731`): 원천 「물광주사용」 설명이나 허가는 큐젤 필러 라인 품목(CUTEGEL Max 1400 Lidocaine) — 허가 기준 M2
- 프린세스(`auto-M2-1775362470502`): 원천 설명 「순수 비가교 HA」는 허가 품목명(Princess Filler · Princess Volume)과 충돌 — 원천 설명 확인 대상
- 스네일샷(`auto-M4-1775362498539`): 하위 「PN/PDRN」 틀림 — 원천 설명 「달팽이 분비물 추출물」(복합 성분 하위)
- 밸피엔(`auto-M4-1775360463217`): 허가 「밸피엔(BelPN)」(PN) — 원천 설명 「플라센타 추출물」은 허가와 충돌, 원천 확인 대상
- 셀렉V(`auto-M8-1775364106103`): 허가 「펄스광선조사기」(IPL) ↔ 원천 설명 「Q-switched Nd:YAG」 — 하위 계열은 허가 기준 IPL
- BBL 스킨타이트(`auto-32-1774737181584`): 원천 「810nm 근적외선 … 타이트닝」 — 광원 기기(M8), 목적이 타이트닝
- 소프라노 티타늄(`M9-2-4`): 허가 「반도체레이저수술기」 · 원천 「M9-2(RF) 섹션에 잘못 등재」 — 1단계 반영된 M8 이 맞음
- 버츄RF(`auto-M9-1775361433713`): 허가 「범용 전기 수술기」 VirtueRF · 원천 설명 「미세 바늘을 통해 … 고주파」 — 1단계 반영된 M11 이 맞음
- 온다(`M9-3-1`): 극초단파(마이크로웨이브) — 문헌 M9 이름은 HIFU·RF, 원천 하위 M9-3 유지
- 클래리파이(`auto-M9-1775364775139`): 원천 하위 「마이크로웨이브」 ↔ 설명 「RF 에너지가 피지선…」 — 어느 쪽이든 M9 에너지, 하위는 확인 필요
- 쿨톤(`auto-M10-1775363019549`): 원천 설명에 「크라이오리폴리시스」와 「EMS 근육자극」이 섞임 — 근육 자극 기준 M10, 원천 설명 확인 대상
- 셀리뉴(`auto-M11-1775360645191`): 허가 「범용 전기 수술기」 · 원천 설명 「비침습적 … 모노폴라 RF」 — 1단계 반영된 M9 가 맞음
- 밀크필(`auto-47-1774737181584`): 원천 설명 「워터제트 기반 물리적 클렌징」 — 하위는 화학 박피가 아니라 기계적 박리·클렌징
- 미라필링(`auto-M15-1775364775115`): 원천 설명 「산호 칼슘 미세침 … 물리적 각질 제거」 — 하위 기계적 박리
- CO2필(`auto-M15-1775401653479`): 원천 「탄산팩 · 탄산가스를 이용 … 비침습적 필링」 — 바르는 탄산팩(외용), 카복시 주입(X2)과 다름
- 해초필(`auto-M15-1775401677251`): 원천 「담수해면체 미세침 … 물리적 각질제거」 — 하위 기계적 박리
- 살몬필(`auto-M15-1775401700008`): 원천 「연어 PDRN … 메조테라피 필링」 — 바르는 필링이면 M15, 주입이면 M4(원천 확인 대상)
- 미라클필링(`auto-M15-1775401716456`): 원천 「담수해면체 스피큘 … 물리적 각질제거와 … 화학적 필링」 — 하위 기계적 박리(복합)
- ASA필(`auto-M15-1775402078232`): 원천 「해조류 추출물과 미세침」 — 하위 기계적 박리
- 소노퀸(`auto-M15-1775364775167`): 허가 「집속형초음파자극시스템」(NP-100) — 원천은 M15 초음파관리였으나 현재 계열 M9 가 허가와 맞음
- 벨라소닉(`M15-6-4`): 허가 「초음파자극기」 BELLA SONIC 2X — 원천은 주입장비지만 바늘·제트 없이 초음파 흡수 보조(D09)
- 제네오X(`auto-M15-1775402654237`): 원천 시그니처 「옥시제네오 · 초음파 · 마사지」 · 1단계 D17 국문 브로슈어 OxyGeneo · LUX · LIFT — 박리+영양 도입(M15 기계적 박리)
- AAPE(`auto-M17-1775364775191`): 원천 「지방유래 줄기세포에서 추출한 고농도 단백질」 — M17 배양액·추출물
- 노바스템(`auto-61-1774737181584`): 원천 하위 「자가혈유래 줄기세포」 ↔ 설명 「ADSC 배양에서 추출한 성장인자」 — 원천 확인 대상
- 미라셀(`auto-62-1774737181584`): 원천 하위 「자가혈유래 줄기세포」 ↔ 설명 「ADSC 배양액 유래 성장인자」 — 원천 확인 대상
- 콘투락투벡스(`auto-M15-1775364775171`): 허가 「콘투락투벡스겔」 일반의약품(알란토인 · 헤파린) — 외용 의약품(M15 외용제)

## 8. 이번에 새로 찾은 문헌 (NCBI ESummary 로 실재 확인 · 임상 주장 검수 아님)

- PMID 15034813 · Shpall R, Beddingfield FC 3rd, Watson D · 「Microdermabrasion: a review.」 Facial Plast Surg 2004 · DOI 10.1055/s-2004-822958
- PMID 18038498 · Bogle MA, Arndt KA, Dover JS · 「Plasma skin regeneration technology.」 J Drugs Dermatol 2007 · DOI 없음
- PMID 19146604 · Freedman BM · 「Hydradermabrasion: an innovative modality for nonablative facial rejuvenation.」 J Cosmet Dermatol 2008 · DOI 10.1111/j.1473-2165.2008.00406.x
- PMID 26017594 · Ingargiola MJ, Motakef S, Chung MT · 「Cryolipolysis for fat reduction and body contouring: safety and efficacy of current treatment paradigms.」 Plast Reconstr Surg 2015 · DOI 10.1097/PRS.0000000000001236
- PMID 26608060 · Ita K · 「Recent progress in transdermal sonophoresis.」 Pharm Dev Technol 2017 · DOI 10.3109/10837450.2015.1116566
- PMID 27785706 · Deeks ED · 「Deoxycholic Acid: A Review in Submental Fat Contouring.」 Am J Clin Dermatol 2016 · DOI 10.1007/s40257-016-0231-3
- PMID 30550830 · Lee KC, Wambier CG, Soon SL · 「Basic chemical peeling: Superficial and medium-depth peels.」 J Am Acad Dermatol 2019 · DOI 10.1016/j.jaad.2018.10.079
- PMID 31168833 · Mazzoni D, Lin MJ, Dubin DP · 「Review of non-invasive body contouring devices for fat reduction, skin tightening and muscle definition.」 Australas J Dermatol 2019 · DOI 10.1111/ajd.13090
- PMID 33471046 · Glass GE · 「Photobiomodulation: The Clinical Applications of Low-Level Light Therapy.」 Aesthet Surg J 2021 · DOI 10.1093/asj/sjab025
- PMID 33577211 · Tan MG, Jo CE, Chapas A · 「Radiofrequency Microneedling: A Comprehensive and Critical Review.」 Dermatol Surg 2021 · DOI 10.1097/DSS.0000000000002972
- PMID 33682249 · Han HS, Hong JY, Kwon TR · 「Mechanism and clinical applications of needle-free injectors in dermatology: Literature review.」 J Cosmet Dermatol 2021 · DOI 10.1111/jocd.14047
- PMID 33960109 · Goldberg DJ, Enright KM, Goldfarb R · 「The role and clinical benefits of high-intensity focused electromagnetic devices for non-invasive lipolysis and beyond: A narrative review and position paper.」 J Cosmet Dermatol 2021 · DOI 10.1111/jocd.14203
- PMID 35124882 · Ahramiyanpour N, Shafie'ei M, Sarvipour N · 「Carboxytherapy in dermatology: A systematic review.」 J Cosmet Dermatol 2022 · DOI 10.1111/jocd.14834
- PMID 37159906 · Strong AL, Rohrich RJ, Tonnard PL · 「Technical Precision with Autologous Fat Grafting for Facial Rejuvenation: A Review of the Evolving Science.」 Plast Reconstr Surg 2024 · DOI 10.1097/PRS.0000000000010643
- PMID 37649956 · Paichitrojjana A, Paichitrojjana A · 「Oral Isotretinoin and Its Uses in Dermatology: A Review.」 Drug Des Devel Ther 2023 · DOI 10.2147/DDDT.S427530
- PMID 37749418 · Alizadeh Z, Halabchi F, Bodaghabadi Z · 「Non-invasive Body Contouring Technologies: An Updated Narrative Review.」 Aesthetic Plast Surg 2024 · DOI 10.1007/s00266-023-03647-x
- PMID 37957393 · Kohan J, Vyas K, Erotocritou M · 「High-Intensity Focused Electromagnetic (HIFEM) Energy With and Without Radiofrequency for Noninvasive Body Contouring: A Systematic Review.」 Aesthetic Plast Surg 2024 · DOI 10.1007/s00266-023-03730-3
- PMID 38297988 · Park SY, Kim SB, Wan J · 「Lipolytic agents for submental fat reduction: Review.」 Skin Res Technol 2024 · DOI 10.1111/srt.13601
- PMID 39544509 · Rho NK, Kim HS, Kim SY · 「Injectable "Skin Boosters" in Aging Skin Rejuvenation: A Current Overview.」 Arch Plast Surg 2024 · DOI 10.1055/a-2366-3436
- PMID 40751922 · Guo Z, Yuan K · 「The Application of Light Emitting Diode (LED) in Cosmetic Dermatology.」 Photodermatol Photoimmunol Photomed 2025 · DOI 10.1111/phpp.70041

검색으로 못 찾은 것(확인 안 됨): 비HA 필러 독립 문헌 · 콜드 플라즈마 · 마이크로웨이브 리프팅 · hADM 스킨부스터 · 태반 추출물 미용 리뷰 · 각 계열 한글 공식 일반명 대부분.
