# 계열 18 정의 · 하위 칸

정본 `orchestration/work/phub-recommend/step2-families.json` `families[]`(재검수 v5 PASS · 2026-10-28)을 옮긴 것이다.
행 수는 그 판의 `product_family` 352행을 다시 센 값이다(단위 = 행). **판정할 때는 이 표가 아니라 정본을 연다** — 정본이 바뀌면 정본이 이긴다.

기준 문헌: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/literature-evidence.json` `categories.M1~M17`(영문 이름 · moa 진술 · PMID). N1 은 문헌 파일 밖 — 독립 리뷰 2건으로 세웠다.

## 한눈에

| 계열 | 이름 | 문헌 이름 | 하위 칸 | 주 행 | 보조로 걸린 행 | PMID |
|---|---|---|---|---|---|---|
| M1 | 보툴리눔 톡신 | Botulinum toxin type A (aesthetic) | 없음 | 19 | 0 | 33714246 |
| M2 | 성형용 필러 | Hyaluronic acid dermal fillers | 2 | 29 | 1 | 30960626 · 33633459 |
| M3 | 바이오스티뮬레이터 | Collagen-stimulating biostimulators (PLLA/CaHA/PDLLA/PCL) | 5 | 14 | 1 | 38853456 |
| M4 | 스킨부스터 | Skinboosters and mesotherapy (non-crosslinked HA, polynucleotides, amino-acid/vitamin cocktails) | 5 | 41 | 1 | 39544509 |
| M5 | PRP·엑소좀 | Platelet-rich plasma (PRP) and exosome therapies | 2 | 8 | 0 | 29457008 · 27035812 |
| M6 | 자가지방이식 | Autologous fat grafting / lipotransfer for facial rejuvenation | 1 | 0 | 0 | 37159906 |
| M7 | 실리프팅 | Absorbable suspension threads (PDO/PLLA/PCL) for facial lifting | 4 | 12 | 0 | 33469333 |
| M8 | 레이저·광치료 | Aesthetic lasers and IPL | 12 | 69 | 1 | 32273965 · 38525494 |
| M9 | HIFU·고주파 리프팅 | Non-invasive skin tightening: HIFU and radiofrequency | 4 | 50 | 10 | 37753689 |
| M10 | HIFEM·EMS 근육 자극 | HIFEM/HIFES and EMS | 2 | 8 | 2 | 33960109 · 37957393 |
| M11 | 고주파 마이크로니들(니들RF) | Fractional radiofrequency microneedling (RF microneedling) | 없음 | 13 | 2 | 33577211 |
| M12 | 마이크로니들링(MTS) | Microneedling / percutaneous collagen induction (non-RF) | 없음 | 3 | 0 | 27559496 |
| M13 | 플라즈마 | Plasma skin treatment | 2 | 3 | 0 | 18038498 |
| M14 | 냉동지방분해 | Cryolipolysis | 없음 | 3 | 0 | 26017594 |
| M15 | 외용 관리 | Topical cosmeceuticals | 4 | 54 | 1 | 28805671 · 34292058 · 30550830 · 19146604 |
| M16 | 정맥 영양 수액 | Intravenous micronutrient / antioxidant therapy (aesthetic) | 없음 | 0 | 0 | 27088927 |
| M17 | 줄기세포·줄기세포 유래 제제 | Stem cells and stem cell-derived products | 2 | 5 | 0 | 28296617 · 31247326 |
| N1 | 지방분해 주사 | Injection lipolysis (deoxycholic acid · cholic acid) | 없음 | 10 | 0 | 27785706 · 38297988 |
| 계열 밖 | — | — | — | 8 | — | — |
| family null(원장님 문의) | — | — | — | 3 | — | — |

제품 행 0 계열: M6 자가지방이식 · M16 정맥 영양 수액 — 시술 · 수액 계열이라 제품 원장에 해당 행이 없다(정의는 그대로 둔다).

## M1 보툴리눔 톡신

- **정의**: 보툴리눔 독소 A형을 근육·피부에 주사해 신경근 접합부의 아세틸콜린 분비를 막아 근육을 이완시키는 시술
- **이름 상태**: 확정(10-27) · 문헌 이름 「Botulinum toxin type A (aesthetic)」
- **동의어**: 보톡스(상담 용어 · 엘러간 제품 이름과 겹침) · 톡신 · 보툴리눔 독소(ATC 한글) · Botulinum toxin
- **문헌 근거**:
  - `literature-evidence.json#categories.M1.name` = 「Botulinum toxin type A (aesthetic)」
  - PMID 33714246 — Scientific review of the aesthetic uses of botulinum toxin type A. · 정의 근거 · 「Botulinum toxin type A inhibits the secretion of acetylcholine at the presynaptic neuromuscular junction.」
  - PMID 33714246 — Scientific review of the aesthetic uses of botulinum toxin type A. · 정의 근거 · 「Botulinum toxin type A weakens skeletal muscles by presynaptic blockade of the exocytosis of acetylcholine-containing vesicles in the neuromuscular junction.」
- **하위 칸**: 없음(D18)

원천 하위의 행선지:

- M1-2 수입 · M1-1 국산 → 제품 속성 — 수입/국산은 제조국·수입사 — 1단계 6_companies(importer·manufacturer) 칸이 이미 가짐. 문헌 M1 정의는 A형 하나로 하위 구분 없음(literature M1.moa)
- M1-3 용도별(13: 주름 · 사각턱 · 턱선보톡스 · 다한증 …) → 5단계로 넘김(표시만) — _RESUME §2 OQ-317 「턱선보톡스 = 단위 시술(보톡스 × 턱선)」 · 부위 이름 = 단위 시술, 목적 이름 = 목적 엣지

넘긴 것(표시만): M1-3 용도별(13: 주름 · 사각턱 · 턱선보톡스 · 다한증 …) → 5단계

## M2 성형용 필러

- **정의**: 진피·피하에 겔 상태의 충전 물질(주로 가교 히알루론산)을 주입해 부피·윤곽을 채우는 시술
- **이름 상태**: 국내 공식 출처 · 문헌 이름 「Hyaluronic acid dermal fillers」
- **동의어**: 필러 · 히알루론산 필러 · HA 필러 · Dermal filler
- **문헌 근거**:
  - `literature-evidence.json#categories.M2.name` = 「Hyaluronic acid dermal fillers」
  - PMID 30960626 — Hyaluronic Acid in the Third Millennium. · 정의 근거 · 「Crosslinking of hyaluronic acid with agents such as BDDE modifies viscoelastic properties and prolongs tissue residence time.」
  - PMID 33633459 — Whole-Face Approach with Hyaluronic Acid Fillers. · 정의 근거 · 「Hyaluronic acid fillers restore facial volume and contour lost due to ageing-related changes in skin, fat pads, bones, and muscles.」

| 하위 칸 | 주 행 | 보조 행 |
|---|---|---|
| 히알루론산(HA) | 27 | 1 |
| 비HA(영구·반영구) | 2 | 0 |

원천 하위의 행선지:

- M2-1 국산 HA · M2-2 수입 HA → 하위 계열 「히알루론산(HA)」 1개 + 국산/수입은 제품 속성 — 문헌 M2 정의가 HA 필러(literature M2.name) · 국산/수입은 6_companies
- M2-3 비HA 필러(아테콜 PMMA · 아쿠아미드 폴리아크릴아마이드) → 하위 계열 「비HA(영구·반영구)」 — 문헌 M2 는 HA 만 다룸 — 비HA 를 M2 에 두는 근거는 원천 하위(M2-3)와 허가 품목 「조직 수복용 생체 재료」(아테콜 ARTESENSE). 비HA 필러 독립 문헌은 이번에 찾지 않음(확인 안 됨)

## M3 바이오스티뮬레이터

- **정의**: 생분해성 고분자 미립자(PLLA · CaHA · PDLLA · PCL · PDO)를 주입해 이물 반응으로 자가 콜라겐 생성을 유도하는 시술
- **이름 상태**: 공식 출처 미확인 · 문헌 이름 「Collagen-stimulating biostimulators (PLLA/CaHA/PDLLA/PCL)」
- **동의어**: 콜라겐부스터 · 콜라겐 자극제 · Collagen stimulator
- **문헌 근거**:
  - `literature-evidence.json#categories.M3.name` = 「Collagen-stimulating biostimulators (PLLA/CaHA/PDLLA/PCL)」
  - PMID 38853456 — A morphological analysis of calcium hydroxylapatite and poly-l-lactic acid biostimulator particles. · 정의 근거 · 「PLLA induces neocollagenesis through immune-mediated mechanisms involving macrophage activation and M2 polarization, distinct from mechanotransductive pathways」

| 하위 칸 | 주 행 | 보조 행 |
|---|---|---|
| PLLA | 4 | 0 |
| CaHA | 2 | 0 |
| PCL | 4 | 0 |
| PDLLA | 3 | 0 |
| PDO | 1 | 0 |

원천 하위의 행선지:

- M3-1 PLLA · M3-2 CaHA · M3-3 PCL · M3-4 PDLLA · PDO → 하위 계열(재질) — 문헌 M3 이름이 재질로 나눔 「(PLLA/CaHA/PDLLA/PCL)」 · PDO 미립자(울트라콜)는 원천 설명 「이물반응을 유도, 콜라겐 신생」이 M3 정의와 같음
- M3-5 콜라겐 → 다른 계열로(M4) — 묶음 D06 — 39544509 Collagen 절 「intradermal collagen injections … skin regeneration」 · LAETIGEN(레티젠) 예시
- 무세포동종진피(hADM) → 다른 계열로(M4) — 사용자 판단 — 묶음 D07 — 원천 설명 「콜라겐 생성을 ‘유도’하는 것이 아니라 … ‘직접 보충’」 = M3 정의(collagen-stimulating)와 반대

## M4 스킨부스터

- **정의**: 비가교·저가교 히알루론산 · 폴리뉴클레오타이드 · 콜라겐 · 아미노산/비타민 칵테일 같은 재료를 진피에 소량씩 여러 점 주입(또는 무바늘 제트 주입)해 피부 질을 개선하는 시술
- **이름 상태**: 공식 출처 미확인 · 문헌 이름 「Skinboosters and mesotherapy (non-crosslinked HA, polynucleotides, amino-acid/vitamin cocktails)」
- **동의어**: 물광주사 · 메조테라피 · Skin booster · Mesotherapy
- **문헌 근거**:
  - `literature-evidence.json#categories.M4.name` = 「Skinboosters and mesotherapy (non-crosslinked HA, polynucleotides, amino-acid/vitamin cocktails)」
  - PMID 39544509 — Injectable "Skin Boosters" in Aging Skin Rejuvenation: A Current Overview. · 정의 근거 · 「Hyaluronic acid inhibits collagenase enzymes slowing collagen breakdown.」
  - PMID 39544509 — Injectable "Skin Boosters" in Aging Skin Rejuvenation: A Current Overview. · 정의 근거 · 「목차: Hyaluronic Acid · Polynucleotide · Collagen · Polycomponent Products · Delivery Methods(Intradermal Injection Technique · Needle-free Jet Injectors) — 본문 「An example of this technology is the Curejet (Baz Biomedic, S…」

| 하위 칸 | 주 행 | 보조 행 |
|---|---|---|
| 히알루론산 | 6 | 0 |
| 폴리뉴클레오타이드(PN·PDRN) | 9 | 0 |
| 콜라겐 | 7 | 0 |
| 복합 성분(칵테일) | 5 | 0 |
| 무세포동종진피(hADM) | 6 | 0 |
| (하위 없음) | 8 | — |

원천 하위의 행선지:

- M4-2 HA(물광) → 하위 계열 「히알루론산」 — 39544509 절 Hyaluronic Acid · literature M4.effects 비가교 HA
- M4-1 PN/PDRN → 하위 계열 「폴리뉴클레오타이드(PN·PDRN)」 — 문헌 M4 이름 「polynucleotides」 · 39544509 절 Polynucleotide
- auto-new-M4 콜라겐/신규 + M3-5 콜라겐 → 하위 계열 「콜라겐」 — 39544509 절 Collagen
- (복합 성분: NCTF · 매쿰7 · 사이토케어 · 릴리이드M …) → 하위 계열 「복합 성분(칵테일)」 — 문헌 M4 이름 「amino-acid/vitamin cocktails」 · 39544509 절 Polycomponent Products
- M4-3 엑소좀/성장인자 → 다른 계열로(M5) — 묶음 D08 — 문헌 M5 이름 「PRP and exosome therapies」. 39544509 는 exosome 을 다루지 않음(본문 검색 0건)
- 주입 기기(원천 M15-6 주입장비 · 물광/메조건) → M4 의 제품(기기) — 하위 계열 아님 · 「어떻게」는 4단계 기법 — 묶음 D05 — 39544509 Delivery Methods 절

넘긴 것(표시만): 주입 기기(원천 M15-6 주입장비 · 물광/메조건) → 4단계

## M5 PRP·엑소좀

- **정의**: 자가혈에서 농축한 혈소판 성장인자(PRP·PRF 등) 또는 세포외소포(엑소좀)를 주입·도포해 재생을 유도하는 시술
- **이름 상태**: 공식 출처 미확인 · 문헌 이름 「Platelet-rich plasma (PRP) and exosome therapies」
- **동의어**: PRP · 자가혈 · 혈소판풍부혈장 · 엑소좀 · PRP / Autologous Blood
- **문헌 근거**:
  - `literature-evidence.json#categories.M5.name` = 「Platelet-rich plasma (PRP) and exosome therapies」
  - PMID 29457008 — A Review of Platelet-Rich Plasma: History, Biology, Mechanism of Action, and Classification. · 정의 근거 · 「PRP delivers concentrated platelet-derived growth factors (PDGF, TGF-β, VEGF, EGF) that stimulate fibroblast proliferation and collagen synthesis.」
  - PMID 27035812 — The biology and function of exosomes in cancer. · 정의 근거 · 「Extracellular vesicles (exosomes) carry proteins, lipids, and microRNAs that modulate recipient cell signaling and extracellular matrix remodeling.」

| 하위 칸 | 주 행 | 보조 행 |
|---|---|---|
| 혈소판 농축물(PRP·PRF) | 3 | 0 |
| 엑소좀 | 5 | 0 |

원천 하위의 행선지:

- M5-1 PRP · M5-2 PRF(PRF·CGF) → 하위 계열 「혈소판 농축물(PRP·PRF)」 — literature M5.moa[0] PRP 성장인자
- 엑소좀(원천 M4-3 · M17-3 · M5-P-4) → 하위 계열 「엑소좀」 — literature M5.moa[1]·[2] exosome
- M5-3 MCT(메타셀) · ACT → 확인 안 됨 — 5단계 — 원천 항목명만 있고 문헌 근거 없음

넘긴 것(표시만): M5-3 MCT(메타셀) · ACT → 5단계

## M6 자가지방이식

- **정의**: 자기 몸에서 채취한 지방을 가공해 얼굴 등 부피가 꺼진 곳에 주입하는 시술
- **이름 상태**: 공식 출처 미확인 · 문헌 이름 「Autologous fat grafting / lipotransfer for facial rejuvenation」
- **동의어**: 지방이식 · Fat grafting · Lipotransfer
- **문헌 근거**:
  - `literature-evidence.json#categories.M6.name` = 「Autologous fat grafting / lipotransfer for facial rejuvenation」
  - PMID 37159906 — Technical Precision with Autologous Fat Grafting for Facial Rejuvenation: A Review of the Evolving Science. · 정의 근거 · 「Autologous fat grafting is … the preferred soft-tissue filler in the correction of facial atrophy … fat grafts to be divided based on parcel size and cell type into three major subtypes: macrofat, microfat, and nanofat.」

| 하위 칸 | 주 행 | 보조 행 |
|---|---|---|
| 지방 입자 크기(마이크로 · 나노) | 0 | 0 |

원천 하위의 행선지:

- M6-1 마이크로지방이식 · M6-2 나노지방이식 → 하위 계열(지방 입자 크기) — 37159906 「macrofat, microfat, and nanofat」
- M6-3 SVF지방이식 → 확인 안 됨 — 5단계 — 37159906 초록의 세 아형에 SVF 없음 · M17-2 SVF 와 겹침

넘긴 것(표시만): M6-3 SVF지방이식 → 5단계

메모: 제품 행 0(시술 계열 — 제품이 아니라 자가 조직)

## M7 실리프팅

- **정의**: 체내에서 녹는 실(PDO · PLLA · PCL · PLCL)을 피하에 넣어 처진 조직을 기계적으로 당기고 실 주변 콜라겐 생성을 유도하는 시술
- **이름 상태**: 국내 품목명 있음 · 계열 일부만 해당(3/12행) — 공식 일반명 아님 · 문헌 이름 「Absorbable suspension threads (PDO/PLLA/PCL) for facial lifting」
- **동의어**: 실 리프팅 · Thread lift
- **문헌 근거**:
  - `literature-evidence.json#categories.M7.name` = 「Absorbable suspension threads (PDO/PLLA/PCL) for facial lifting」
  - PMID 33469333 — The Science of Absorbable Poly(L-Lactide-Co-ε-Caprolactone) Threads for Soft Tissue Repositioning of the Face: An Evidence-Based Evaluation of Their Physical Properties and Clinical Application. · 정의 근거 · 「Absorbable barbed threads maintain mechanical lifting action for repositioning of sagging facial tissue.」
  - PMID 33469333 — The Science of Absorbable Poly(L-Lactide-Co-ε-Caprolactone) Threads for Soft Tissue Repositioning of the Face: An Evidence-Based Evaluation of Their Physical Properties and Clinical Application. · 정의 근거 · 「Thread insertion stimulates fibroblasts and synthesis of collagen, hyaluronic acid and elastin around the thread.」

| 하위 칸 | 주 행 | 보조 행 |
|---|---|---|
| PDO | 9 | 0 |
| PCL | 1 | 2 |
| PLCL | 0 | 0 |
| PLLA | 2 | 1 |

원천 하위의 행선지:

- M7-1 재질별(PDO · PCL · PLCL · PLLA · PCA · 복합) → 하위 계열(재질) — 문헌 M7 이름 「(PDO/PLLA/PCL)」
- M7-2 형태별(코그 · 모노 · 볼륨) → 제품 속성(형태) — 문헌 M7 은 형태로 나누지 않음(barbed 는 moa 서술 안의 성질)
- M7-3 브랜드(24) → 제품(1단계 원장 행) — 브랜드 = 제품

## M8 레이저·광치료

- **정의**: 특정 파장의 레이저, 광대역 펄스광(IPL), 협대역 비간섭광(LED)을 피부에 조사해 색소·혈관·모낭·진피를 선택적으로 가열·파괴하거나 광생물조절을 일으키는 시술
- **이름 상태**: 공식 출처 미확인 · 문헌 이름 「Aesthetic lasers and IPL」
- **동의어**: 레이저 · IPL · Laser & Light
- **문헌 근거**:
  - `literature-evidence.json#categories.M8.name` = 「Aesthetic lasers and IPL」
  - PMID 32273965 — Assessment of Laser Effects on Skin Rejuvenation. · 정의 근거 · 「Fractional ablative lasers vaporize the epidermis and heat the dermis to prompt collagen remodeling.」
  - PMID 38525494 — Picosecond Nd:YAG versus Fractional CO(2) Lasers in Management of Postburn Scars. · 정의 근거 · 「Picosecond Nd:YAG laser reduces pigmentation in hyperpigmented scars.」
  - 반영 결정: D04 반영: LED 편입 — PMID 40751922 「LED therapy employs narrow-spectrum, incoherent light for photobiomodulation」 · 원천 M8 영문 「Laser & Light」

| 하위 칸 | 주 행 | 보조 행 |
|---|---|---|
| IPL | 8 | 1 |
| LED | 7 | 0 |
| 엔디야그 레이저 | 26 | 6 |
| 알렉산드라이트 레이저 | 7 | 1 |
| 반도체 레이저 | 12 | 0 |
| 탄산가스 레이저 | 4 | 0 |
| 루비 레이저 | 0 | 1 |
| Er:YAG | 1 | 1 |
| Er:Glass | 2 | 1 |
| 톨륨 | 0 | 1 |
| KTP | 0 | 1 |
| PDL | 2 | 0 |

원천 하위의 행선지:

- M8-2 프락셔널 → 하위 계열 「프락셔널(박피/비박피)」 — literature M8.moa[0]·[3] fractional ablative / non-ablative
- 피코초(auto-new-M8) · M8-1 색소/토닝 중 피코 → 하위 계열 「피코초」 — literature M8.moa[2]·[5] picosecond
- M8-3 IPL → 하위 계열 「IPL」 — 문헌 M8 이름 「and IPL」
- M8-1 색소/토닝 · M8-4 혈관 · M8-5 제모 → 6단계 목적으로(하위 계열 아님) — 색소·혈관·제모는 「무엇을」이 아니라 목적 — _RESUME §2 10-27 「목적은 고민→시술 엣지」
- M8-6 기타 → 해체 — 행마다 광원 하위로 — 「기타」는 분류 기준 없음
- (재검수 v2 결정) → 하위 계열 = 광원 매질 한 축 — 프락셔널 · 피코초 칸 없앰 · 광원 2종은 null + open — _RESUME.md §2 2026-10-28 WARN 3 처리

> ⚠ 위 줄들은 판마다 쌓인 기록이다. 지금 규칙: 「프락셔널」 「피코초」 칸은 **없다**(방식 → 4단계) · 「광원 2종은 null + open」은 **철회** — 주 1 + 보조(`also_sub_families`)(_RESUME §2 10-28 「하위 계열도 주 · 보조로」)

넘긴 것(표시만): M8-1 색소/토닝 · M8-4 혈관 · M8-5 제모 → 6단계 / M8 방식(피코초 · 프락셔널 · 롱펄스 · Q스위치 등 — 원천 하위 M8-2 프락셔널 · 피코초 포함) → 4단계

## M9 HIFU·고주파 리프팅

- **정의**: 피부를 뚫지 않고 집속 초음파(HIFU) 또는 고주파(RF)로 진피·SMAS 를 가열해 콜라겐 수축·신생을 유도하는 기기 시술
- **이름 상태**: 공식 출처 미확인 · 문헌 이름 「Non-invasive skin tightening: HIFU and radiofrequency」
- **동의어**: 기기 리프팅 · 리프팅 · 울쎄라·써마지(장비 이름 — 10-27 결정대로 시술 동의어) · Energy Based Device Lifting
- **문헌 근거**:
  - `literature-evidence.json#categories.M9.name` = 「Non-invasive skin tightening: HIFU and radiofrequency」
  - PMID 37753689 — Efficacy of radiofrequency combined with single-dot ultrasound efficacy for skin rejuvenation: A non-randomized split-face trial with blinded response evaluation. · 정의 근거 · 「HIFU delivers focused ultrasound energy to generate thermal zones at specific depths in the dermis and SMAS layer, triggering collagen and elastin neogenesis」
  - PMID 37753689 — Efficacy of radiofrequency combined with single-dot ultrasound efficacy for skin rejuvenation: A non-randomized split-face trial with blinded response evaluation. · 정의 근거 · 「HIFU induces dermal collagen thickening and straightening of elastic fibers in the mid-to-deep dermis and SMAS, while RF causes neocollagenesis and neoelastogenesis more diffusely in the upper papillary dermis」

| 하위 칸 | 주 행 | 보조 행 |
|---|---|---|
| HIFU | 21 | 0 |
| RF | 26 | 0 |
| 마이크로웨이브 | 2 | 0 |
| SUPERB 초음파 | 1 | 0 |

원천 하위의 행선지:

- M9-1 HIFU · M9-2 RF → 하위 계열 「HIFU」 「RF」 — 문헌 M9 이름
- M9-3 마이크로웨이브 → 하위 계열(원천 유지) — 문헌 확인 안 됨 — 문헌 M9 는 HIFU·RF 만 이름에 둠
- M9-4 복합 에너지 → 해체 — 행마다 주 에너지 하위 + 「여러 계열」 표시 — 복합은 분류 기준이 아니라 장비 성질
- M9-SIG 시그니처 프로그램 → 6단계(패키지)로 — _RESUME §2 10-27 「패키지는 단위 시술 묶음」

넘긴 것(표시만): M9-SIG 시그니처 프로그램 → 6단계

## M10 HIFEM·EMS 근육 자극

- **정의**: 고강도 집속 전자기장(HIFEM) 또는 전기 자극(EMS)으로 근육을 강제로 수축시키는 기기 시술
- **이름 상태**: 공식 출처 미확인 · 문헌 이름 「HIFEM/HIFES and EMS」
- **동의어**: HIFES/EMS · EMS · 엠스컬프트(장비 이름)
- **문헌 근거**:
  - `literature-evidence.json#categories.M10.name` = 「HIFEM/HIFES and EMS」
  - PMID 33960109 — The role and clinical benefits of high-intensity focused electromagnetic devices for non-invasive lipolysis and beyond: A narrative review and position paper. · 정의 근거 · 「In 2018, the first device to use high-intensity focused electromagnetic (HIFEM) technology to non-invasively build muscle was brought to market.」
  - PMID 37957393 — High-Intensity Focused Electromagnetic (HIFEM) Energy With and Without Radiofrequency for Noninvasive Body Contouring: A Systematic Review. · 정의 근거

| 하위 칸 | 주 행 | 보조 행 |
|---|---|---|
| HIFEM | 3 | 0 |
| EMS | 5 | 1 |

원천 하위의 행선지:

- M10-1 페이셜 EMS · M10-2 바디 EMS → 3단계 부위로(하위 계열 아님) — 얼굴/바디는 「어디에」 — _RESUME §2 시술 = 무엇을 × 어디에 × 어떻게
- (HIFEM · EMS) → 하위 계열 「HIFEM」 「EMS」 — 문헌 M10 이름

넘긴 것(표시만): M10-1 페이셜 EMS · M10-2 바디 EMS → 3단계

## M11 고주파 마이크로니들(니들RF)

- **정의**: 절연·비절연 미세침을 진피에 찌른 뒤 침 끝으로 고주파를 흘려 분획 열손상을 만드는 시술
- **이름 상태**: 공식 출처 미확인 · 문헌 이름 「Fractional radiofrequency microneedling (RF microneedling)」
- **동의어**: 니들RF · 프락셔널 고주파 · Microneedle RF
- **문헌 근거**:
  - `literature-evidence.json#categories.M11.name` = 「Fractional radiofrequency microneedling (RF microneedling)」
  - PMID 33577211 — Radiofrequency Microneedling: A Comprehensive and Critical Review. · 정의 근거 · 「검색어 「"radiofrequency microneedling" OR "fractional radiofrequency" OR "radiofrequency needling" OR "radiofrequency percutaneous collagen induction"」 — RFMN 을 다른 에너지 기기와 나란히 독립 범주로 검토」
- **하위 칸**: 없음(D18)

원천 하위의 행선지:

- M11-1 니들RF 장비 → 하위 계열 없음(단일) — 원천 하위 1개 = 장비 목록

## M12 마이크로니들링(MTS)

- **정의**: 고주파 없이 미세침(롤러·스탬프·전동 펜)으로 피부에 미세 천공을 내 상처 치유 과정의 콜라겐 생성을 유도하는 시술
- **이름 상태**: 공식 출처 미확인 · 문헌 이름 「Microneedling / percutaneous collagen induction (non-RF)」
- **동의어**: MTS · 더마펜(장비 이름) · Microneedling
- **문헌 근거**:
  - `literature-evidence.json#categories.M12.name` = 「Microneedling / percutaneous collagen induction (non-RF)」
  - PMID 27559496 — Microneedling: Advances and widening horizons. · 정의 근거 · 「Microneedling creates micro-punctures in the skin that stimulate collagen production through percutaneous collagen induction.」
- **하위 칸**: 없음(D18)

원천 하위의 행선지:

- M12-1 수동 · M12-2 전동 → 제품 속성(기구 형태) — 문헌 M12 는 기구 형태로 나누지 않음

## M13 플라즈마

- **정의**: 이온화된 기체(플라즈마)의 에너지를 피부 표면에 직접 전달해 색소단(chromophore)과 무관하게 열손상·재생을 일으키는 시술
- **이름 상태**: 공식 출처 미확인 · 문헌 이름 「Plasma skin treatment」
- **동의어**: 플라즈마 피부 재생(plasma skin regeneration) · Plasma
- **문헌 근거**:
  - `literature-evidence.json#categories.M13.name` = 「Plasma skin treatment」
  - PMID 18038498 — Plasma skin regeneration technology. · 정의 근거 · 「Unlike lasers which rely on the principle of selective photothermolysis … plasma technology delivers heat energy directly to tissue upon contact without reliance on skin chromophores.」

| 하위 칸 | 주 행 | 보조 행 |
|---|---|---|
| 핫 플라즈마 | 2 | 0 |
| 콜드 플라즈마 | 1 | 0 |

원천 하위의 행선지:

- M13-1 핫 · M13-2 콜드 → 하위 계열(원천 유지) — 콜드 플라즈마 문헌 확인 안 됨 — 18038498 은 열(핫) 플라즈마만 다룸

## M14 냉동지방분해

- **정의**: 피부 밖에서 지방층을 냉각해 지방세포만 선택적으로 손상시키는 비수술 지방 감소 시술
- **이름 상태**: 공식 출처 미확인 · 문헌 이름 「Cryolipolysis」
- **동의어**: 크라이오리포라이시스 · 냉각지방분해 · 쿨스컬프팅(장비 이름) · Cryolipolysis
- **문헌 근거**:
  - `literature-evidence.json#categories.M14.name` = 「Cryolipolysis」
  - PMID 26017594 — Cryolipolysis for fat reduction and body contouring: safety and efficacy of current treatment paradigms. · 정의 근거 · 「Cryolipolysis is a nonsurgical technique for localized fat reduction.」
- **하위 칸**: 없음(D18)

원천 하위의 행선지:

- M14-1 냉각지방분해 → 하위 계열 없음(단일) — 원천 하위 1개

## M15 외용 관리

- **정의**: 피부 표면에 바르거나 흡수시키는 외용 관리 — 코스메슈티컬·외용 의약품, 화학 박피, 이를 적용하는 기계적 박리·클렌징 기기와 외용제 흡수 보조 기기
- **이름 상태**: 공식 출처 미확인 · 문헌 이름 「Topical cosmeceuticals」
- **동의어**: 메디컬스킨케어 · 스킨케어 · 필링 · 코스메슈티컬 · Medical Skincare
- **문헌 근거**:
  - `literature-evidence.json#categories.M15.name` = 「Topical cosmeceuticals」
  - PMID 28805671 — The Roles of Vitamin C in Skin Health. · 정의 근거 · 「L-ascorbic acid acts as a cofactor for prolyl and lysyl hydroxylases in collagen synthesis and as a skin antioxidant.」
  - PMID 34292058 — A Clinician's Guide to Topical Retinoids. · 정의 근거 · 「Topical retinoids bind to retinoic acid receptors in the skin, promoting cell turnover and increasing collagen production.」
  - PMID 30550830 — Basic chemical peeling: Superficial and medium-depth peels. · 정의 근거 · 「Chemical peeling, or chemexfoliation …」
  - PMID 19146604 — Hydradermabrasion: an innovative modality for nonablative facial rejuvenation. · 정의 근거 · 「Hydradermabrasion … combines crystal-free microdermabrasion with the pneumatic application of an antioxidant-based serum.」
  - 반영 결정: D03 · D09 반영: 화학 박피 · 기계적 박리·클렌징 · 흡수 보조 기기를 M15 하위로

| 하위 칸 | 주 행 | 보조 행 |
|---|---|---|
| 화학 박피 | 33 | 0 |
| 기계적 박리·클렌징 | 16 | 0 |
| 외용제 | 1 | 0 |
| 흡수 보조 기기 | 4 | 0 |

원천 하위의 행선지:

- M15-1 케미컬필링 → 하위 계열 「화학 박피」 — 30550830(국제필링학회) 「Chemical peeling, or chemexfoliation」 · literature M15.moa 의 레티노이드·비타민C 외용
- M15-2 딥클렌징 · 물리필링(해면체 미세침) · 허벌 필링 → 하위 계열 「기계적 박리·클렌징」 — 19146604 hydradermabrasion · 15034813 microdermabrasion
- 약물/토피컬(auto-1775361777) · 흉터 전용 중 실리콘·연고 → 하위 계열 「외용제」 — literature M15.moa[0]~[4]
- M15-3 광치료(LED) → 다른 계열로(M8) — 사용자 판단 — 묶음 D04
- M15-6 주입장비 · 물광/메조건 → 다른 계열로(M4) — 묶음 D05
- M15-4 초음파관리 · M15-5 이온토포레시스 → M15 유지(흡수 보조 기기) — 사용자 판단 — 묶음 D09 · 26608060 transdermal sonophoresis
- 탈모(비수술) · 여드름 전용 · 흉터 전용 → 해체 — 항목마다 해당 계열/5단계로(LLLT·LED→M8 · 두피 메조·엑소좀→M4/M5 · PRP→M5 · 아큐탄·스피로노락톤→계열 밖 · 서브시전·스테로이드 주사·면포압출·펀치→5단계 시술) — 탈모·여드름·흉터는 고민(7단계) — 「무엇을」이 아님
- 시그니처프로그램 · M15-7/M15-8 「추가」 · 도포/팩(빈 하위) → 6단계(패키지) / 해체 — 패키지 = 단위 시술 묶음 · 「추가」는 분류 기준 없음

넘긴 것(표시만): 탈모(비수술) · 여드름 전용 · 흉터 전용 → 5단계 / 시그니처프로그램 · M15-7/M15-8 「추가」 · 도포/팩(빈 하위) → 6단계

## M16 정맥 영양 수액

- **정의**: 비타민·글루타치온·아미노산 같은 미량영양소·항산화제를 정맥으로 투여하는 시술
- **이름 상태**: 공식 출처 미확인 · 문헌 이름 「Intravenous micronutrient / antioxidant therapy (aesthetic)」
- **동의어**: 수액치료 · 수액 · 영양주사 · IV Therapy
- **문헌 근거**:
  - `literature-evidence.json#categories.M16.name` = 「Intravenous micronutrient / antioxidant therapy (aesthetic)」
  - PMID 27088927 — Glutathione as a skin whitening agent: Facts, myths, evidence and controversies. · 정의 근거 · 「Glutathione inhibits tyrosinase activity and shifts melanogenesis from eumelanin toward pheomelanin in cultured melanocytes.」
  - PMID 27088927 — Glutathione as a skin whitening agent: Facts, myths, evidence and controversies. · 정의 근거 · 「Intravenous glutathione for skin lightening is not supported by the US FDA or multiple national regulatory agencies and has insufficient high-quality efficacy evidence.」
  - 반영 결정: D01 반영: 지방분해주사는 N1 로 나감 · D02: 태반 제제는 계열 밖
- **하위 칸**: 없음(D18)

원천 하위의 행선지:

- M16-1~4 미백/항산화 · 피로회복 · 재생/면역 · 영양보충 → 6단계 목적으로(하위 계열 아님) — 목적 이름
- M16-DCA · M16-LIPO · 기타 지방분해주사(PPC) → 다른 계열로(새 계열 N1) — 사용자 판단 — 묶음 D01
- M16-new 기타(카복시 · 미녹시딜 두피 메조 · LDM · 성장호르몬 …) → 해체 — X2 · M4 · M15 · 계열 밖 / 마케팅명은 5단계 — 묶음 D10 · D02
- 태반주사(라엔넥 · 멜스몬) → 계열 밖 — 사용자 판단 — 묶음 D02

넘긴 것(표시만): M16-1~4 미백/항산화 · 피로회복 · 재생/면역 · 영양보충 → 6단계 / M16-new 기타(카복시 · 미녹시딜 두피 메조 · LDM · 성장호르몬 …) → 5단계

메모: M16 정의에 맞는 제품 행은 1단계 원장에 0(정맥 수액 제품이 원장에 없음)

## M17 줄기세포·줄기세포 유래 제제

- **정의**: 줄기세포 또는 줄기세포에서 얻은 산물(배양액·추출 단백질)을 주입·도포하는 시술
- **이름 상태**: 공식 출처 미확인 · 문헌 이름 「Stem cells and stem cell-derived products」
- **동의어**: 줄기세포치료 · 줄기세포 · 줄기세포 배양액 · Stem Cell Therapy
- **문헌 근거**:
  - `literature-evidence.json#categories.M17.name` = 「Stem cells and stem cell-derived products」
  - PMID 28296617 — Vision Loss after Intravitreal Injection of Autologous "Stem Cells" for AMD. · 부작용 근거 · 「Unregulated stem cell products have caused serious adverse events including blindness after intra-ocular injection and tumor formation at ectopic sites.」
  - PMID 31247326 — Adipose-derived cellular and cell-derived regenerative therapies in dermatology and aesthetic rejuvenation. · 정의 근거 · 「Cellular and cell-derived components of adipose-derived tissue for the purposes of dermatologic and aesthetic rejuvenation … include micro-fragmented fat (nanofat), the stromal vascular fraction (SVF), adipose-derived me…」

| 하위 칸 | 주 행 | 보조 행 |
|---|---|---|
| 배양액·추출물 | 5 | 0 |
| 세포(SVF) | 0 | 0 |

원천 하위의 행선지:

- M17-1 줄기세포배양액 · 자가혈유래 줄기세포 → 하위 계열 「배양액·추출물」 — 원천 설명(노바스템 · 미라셀 · AAPE)이 모두 「ADSC 배양액/추출 단백질」 — 「자가혈유래」 하위 이름과 설명이 충돌(원천 확인)
- M17-2 SVF → 하위 계열 「세포(SVF)」 — 문헌 M17 「stem cells」
- M17-3 엑소좀 → 다른 계열로(M5) — 묶음 D08

## N1 지방분해 주사 — 새 계열(2단계에서 세움)

- **정의**: 피하 지방층에 지방세포를 녹이는 약물(데옥시콜산 · 콜산)을 직접 주사해 국소 지방을 줄이는 시술
- **이름 상태**: 공식 출처 미확인 · 문헌 이름 「Injection lipolysis (deoxycholic acid · cholic acid)」
- **동의어**: DCA · 데옥시콜산 주사 · 윤곽주사 · 이중턱 주사 · 국소 지방분해주사 · 피하 지방분해주사 · 콜산(CA) 국소 지방분해제
- **문헌 근거**:
  - PMID 27785706 — Deoxycholic Acid: A Review in Submental Fat Contouring. · 정의 근거 · 「Deoxycholic acid is a secondary bile acid … that causes adipocyte lysis when injected into subcutaneous fat tissue.」
  - PMID 38297988 — Lipolytic agents for submental fat reduction: Review. · 정의 근거
  - `step1-products.json 브이올렛 4_license.licenses[0].kpic.kpic_class` = 「Deoxycholic Acid : 피부/피하조직질환 > 기타 약물 > 기타」
- **하위 칸**: 없음(D18)

원천 하위의 행선지:

- 데옥시콜산 9 · 콜산 1(뉴비쥬) → 제품 속성(성분) — 허가 성분명(브이올렛주(데옥시콜산) · 뉴비쥬주(콜산))
- M16-LIPO 마케팅명(V라인주사 · 팻킬주사 …) · PPC → 5단계(시술 이름 · 성분 확인 후) — 제품이 아니라 메뉴명 — 1단계 D21·D24 규칙

넘긴 것(표시만): M16-LIPO 마케팅명(V라인주사 · 팻킬주사 …) · PPC → 5단계

## M8 하위 표기 대응 — 매질 이름은 식약처 품목명 표기로

`step2-apply.py` `M8_LIC` · `M8_TEXT` 를 옮긴 것(PDL · LED 두 줄은 그 밖 — 근거를 칸에 적었다). 새 이름을 짓지 않는다. 품목명 행이 없는 매질은 원문 그대로.

| 적힌 말(허가 품목 · 모델명 · 원천 설명) | 하위 칸 |
|---|---|
| 엔디야그 · Nd:YAG | 엔디야그 레이저 |
| 알렉산드라이트 · Alexandrite | 알렉산드라이트 레이저 |
| 반도체 · 다이오드 · diode | 반도체 레이저 |
| 탄산가스 · CO2 | 탄산가스 레이저 |
| 루비 · ruby | 루비 레이저 |
| Er:YAG · 어븀야그 | Er:YAG |
| Er:Glass · 에르븀 글래스 | Er:Glass |
| 톨륨 · thulium | 톨륨 |
| KTP | KTP |
| PDL — 브이빔 퍼펙타는 허가 품목 「색소레이저수술기」 · 사용목적 「매질로서 색소(DYE)」(emedi 상세 · 검수 v5 W1) | PDL |
| 펄스광선 · IPL | IPL |
| LED — 원천 LED 칸 · 광생물조절 기기(D04 · `SUB_BY_NAME` 이름별 지정) | LED |

방식(피코초 · 프락셔널 · 롱펄스 · Q-switched · 나노초 · 박리/비박리)은 하위 칸이 아니다 — 행의 `technique_hint` 에 적힌 말 그대로 두고 4단계(기법)로 넘긴다.
