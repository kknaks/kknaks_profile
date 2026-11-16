# R1 — 대륙 중국어(zh) 검증 + 새 시술 zh

- 조사일: **2026-10-27** · researcher(read-only) · 결정하지 않음
- 사전: `seed-2026-10-27.5.json` (157 term)
- 방법: WebSearch 로 후보 URL → **curl 로 원문 HTML/PDF 를 받아 문자열을 직접 확인**(요약 모델 답만으로 적은 것은 없다. 원문 확인 못 한 것은 「요약만」이라고 표시). 중국 쪽 의료미용 업계 플랫폼 **医美部落 medbelove.com** 은 사이트 검색(`?s=`)이 열려 있어 브랜드별 기사를 전수 조회했다. 등록 여부는 **NMPA 등록증 번호를 적은 기사·상장사 공시**로 확인(NMPA DB 직접 조회는 못 함)
- 출처 성격 약어: **CN-P** = 중국 의료미용 플랫폼·업계 매체 · **CN-N** = 중국 경제지·공시 · **CN-C** = 중국 의원(보도자료 포함) · **KR-zh** = 한국 클리닉·한국행 플랫폼의 중문 안내 · **HK/TW** = 홍콩·대만(대륙 아님)
- ⚠ 한계: 新氧(soyoung) · 更美 등 대륙 소비자 플랫폼과 바이두·소고우는 원문을 못 읽었다(§5). 그래서 **「클리닉 메뉴판 표기」보다 「제조사·대리상 공식명 + 업계 매체」 근거가 많다**


## 0. 새 시술 최종 목록 (R1 확정 · R2 · R3 공용)

기준: 대만 대조 표 B(B-T · B-M · B-K) ∩ 브리프 후보 ∩ 사전 범위(피부과 기기 · 주사 · 시술). 사전에 이미 있는 것은 뺀다.

| # | ko | en | 카테고리(가까운 기존) | 대만 표 B 근거 |
|---|---|---|---|---|
| N01 | 써마지 CPT | Thermage CPT | 기기 리프팅 | B-T `CPT黃金電波` · A-M `黃金電波` |
| N02 | 소프웨이브 | Sofwave | 기기 리프팅 | B-T · B-K `索夫波` |
| N03 | 엑시온 | Exion | 기기 리프팅 / 니들RF | B-T `時空E電波` |
| N04 | 덴서티 | Density | 기기 리프팅 | B-K `無雙電波` |
| N05 | 엠페이스 | EMFACE | HIFES/EMS | A-T `菲斯波 EMFACE` |
| N06 | 클리어앤브릴리언트 | Clear + Brilliant | 레이저 | B-T `鳳凰光` |
| N07 | 프로파일로 | Profhilo | 스킨부스터 | B-T · B-M · B-K |
| N08 | 뉴라미스 | Neuramis | 필러 | B-T `仙女玻尿酸` |
| N09 | 벨로테로 리바이브 | Belotero Revive | 스킨부스터 | B-T `素妍針` |
| N10 | 에스테필 | AestheFill | 바이오스티뮬레이터 | B-T · A-M |
| N11 | 하이드라페이셜 | HydraFacial | 메디컬스킨케어 | B-T `海飛秀` · C-11 |
| N12 | 미라드라이 | miraDry | 기기(다한증) | A-T `清新微波 miraDry` |
| N13 | 울트라셰이프 | UltraShape | 바디 기기 | B-T `標靶震波減脂` |
| N14 | 텐서(테슬라포머) | TeslaFormer | HIFES/EMS 바디 | B-T `易力肌塑` |

빠진 후보: **쥬베룩(ph-108) · 스컬트라(ph-112) 는 사전에 이미 있다** → 새 시술 아님(기존 term 검증 대상). 감량 약 · 수술 · 가슴 보형물 · 여성 기기 제외.

## 1. 한 줄 결론

1. **사전 zh 에 대륙 공식명과 다른 이름이 6개 있다** — 리즈톡스 `丽姿妥适`(대륙 허가명 `解索橙`, 2026-01 허가) · 레티보 `乐提保`(대륙 `乐提葆`) · 엘라비에 `艾拉薇`(대륙 `艾莉薇`, 2015 허가) · 스컬트라 `素颜萃童颜针`(대륙 `塑妍萃`, 2024 허가) · 써마지FLX `美版热玛吉FLX`(대륙 공식 `超玛吉FLX`, 2024 허가) · 리쥬란 `丽珠兰…`(브랜드 공식 `丽驻兰`, `丽珠兰` 은 업계 통칭). 표 B
2. **나머지 한국 전용 제품(신펄 · 더채움 · 타임버스 · 에버라인 · 벨피엔 · 글로벨라 · 더블로골드 · 아그네스 · 인트라셀 · 마이셀 · 셀피아 · 리젠ACR 등)의 음역명은 대륙 출처에서 한 건도 찾지 못했다.** 한국 클리닉의 중문 메뉴(id艾蒂皮肤科 zh-cn)도 `AGNES` `Secret RF` `Density` `Sofwave` `Volnewmer` `Juvelook` 을 **영문 그대로** 쓴다
3. **대륙에서 허가된 톡신은 7개**(衡力 · 保妥适 · 吉适 · 乐提葆 · 思奥美 · 达希斐 · 解索橙 Hutox). 나보타 · 메디톡신 · 뉴럭스 · 보툴렉스(국내명)는 대륙 허가 목록에 없다 — 사전의 `绿毒` `粉毒` `白毒` `纽乐适` 은 대륙 허가명이 아니다
4. 새 시술 14개 중 **대륙 중문명이 출처로 확인된 것 7개**(素芙波 · 美菲斯 · 素颜光 · 艾塑菲 · 海菲秀 · 清新微波 · 热玛吉 4代 CPT), 대륙 미허가·중문명 없음 7개(Exion · Density · Profhilo · Neuramis · Belotero Revive · UltraShape · TeslaFormer)

## 2. 표 A — zh(대륙) × 새 시술

| # | en | zh name 후보 | aliases 후보 | 출처 수(사이트) | 근거 · URL | 확신 |
|---|---|---|---|---|---|---|
| N01 | Thermage CPT | `Thermage CPT` 또는 `热玛吉CPT` — 원문 문자열은 `Thermage CPT`(등록명 「射频治疗仪」) · `第四代(CPT)` · `第三代和第四代Thermage CPT` | `热玛吉第四代`(원문은 「第四代(CPT)」 「第四代…热玛吉」) | 2 | NMPA 国械注进20153092408(2019-12-26 갱신) — medbelove 2024-04-28 [M1] (CN-P) · china.com 2026-08-13 「第四代(CPT)与第五代(FLX)」 [Z1] (CN-N 광고성) | 중 — 「热玛吉CPT」 붙여 쓴 형태는 원문에서 못 봄 |
| N02 | Sofwave | `素芙波` | `Sofwave` · `素夫波` · `索夫波`(medbelove 2024 표기, 대만 표기와 같음) | 3 | 대리상 华瑭医疗(HTDK) 제품 페이지 「Sofwave™素芙波」 + 「成功取得NMPA第三类医疗器械注册证」 [H1] (CN 공식 대리상) · ymguancha 2026-10-22 [Y1] (CN-P) · china.com 2024-08-21 [Z2] · medbelove 2024-07-09 「素夫波」「索夫波」 [M2] | 상 |
| N03 | Exion | 현지에 없음 — 영문 `Exion` | — | 0 | 대륙 출처 못 찾음(BTL 영문 보도만) | — |
| N04 | Density | 현지에 없음 — 영문 `Density` | — | 1 | 爱美客가 Jeisys 의 Density · LinearZ 대륙 독점 판매권 취득(2023-11) [M3] — 허가·중문명은 못 찾음. 爱美客 2026 반기보고서의 「射频皮肤治疗仪」 는 자회사 上海维脉 자체 개발품이라 Density 아님 [I1]. 한국 클리닉 중문 메뉴도 `Density` [K1] | 중(부재) |
| N05 | EMFACE | `美菲斯` | `EMFACE` · `BTL EMFACE` | 3 | 聚美网 백과 「BTL Emface美菲斯」 2024 [J1] (CN-P) · 深圳联合丽格 「BTL EMface美菲斯」 ifeng 2023-08-23 [C1] (CN-C) · 深圳贝比蓝 「EMFACE美菲斯」 chinapp 2024-10-10 [C2] (CN-C). NMPA 허가 여부는 못 찾음. (대만은 `菲斯波`) | 중 |
| N06 | Clear + Brilliant | `素颜光` | `Clear+Brilliant` · `索塔素颜光` | 1(2편) | Solta(索塔) 대륙 브랜드 소개 「Clear+Brilliant®素颜光」 · NMPA 등록 「双波长点阵半导体激光治疗仪 Clear+Brilliant」 [M1] · 「索塔®素颜光」 新品上市 2026-09-14 [M4] — 둘 다 medbelove | 중 — 표 C-3 (대만 `鳳凰光` 과 다름) |
| N07 | Profhilo | 현지에 없음 — 영문 `Profhilo` | — | 2 | NMPA **受理**(심사 접수)만 — 复星/复锐 2023-12-11 [F1] · 2026-09 안면 적응증 접수 보도. 허가·중문명 없음 | 중 |
| N08 | Neuramis | 영문 `Neuramis` (중문명 못 찾음) | `Fillux`(대륙 판매 브랜드라는 한국 보도) | 1 | Medytox 「Neuramis Volume/Deep Lidocaine」 NMPA 허가, 대륙에선 「Fillux」 브랜드로 판매 — stockhub.kr [S1] (**한국 보도 · 대륙 원문 아님**) | 하 |
| N09 | Belotero Revive | 현지에 없음 — 영문 `Belotero Revive` | (`彩虹针` — 표 C-4) | 1 | 「Revive水光針仍未在國內上架」 — hk01 2025-01-23 [HK1] (**HK · 협찬 기사**). 대륙 Merz 보도(保柔缇)에 Revive 언급 없음 [Z3] | 중 |
| N10 | AestheFill | `艾塑菲` | `AestheFill` · (`童颜针` — 표 C-5) | 2(4편) | 「AestheFill艾塑菲聚乳酸面部填充剂…2024年1月获国家药监局(NMPA)批准…首款进口“童颜针”」 jiemian [N1] (CN-N) · medbelove 다수(「艾塑菲童颜针」) [M5] (CN-P) | 상 |
| N11 | HydraFacial | `海菲秀` | `Hydrafacial` | 2 | 「Hydrafacial海菲秀…全新一代海菲秀Syndeo」 2023-04 [T1] (CN-P, 企鹅号 医美视界) · medbelove 「海菲秀 | 中国独家代理「凯美俐」…」 등 5편 [M6] | 상 |
| N12 | miraDry | `清新微波` | `miraDry` · `miraDry清新微波` | 1 | 「miraDry清新微波中国十周年系列活动在上海举行」 2026-09-23 [M7] (CN-P). CFDA 2015/2016 허가 보도 [G1](영문) | 중 — 표 C-6 |
| N13 | UltraShape | 영문 `UltraShape` (브랜드 중문명 못 찾음) | (등록 품명 `聚焦超声减脂仪`) | 1 | CIRS 「已注册有源医美产品汇总」: 「已获批…聚焦超声产品为 赛诺龙…聚焦超声减脂仪 Contour I V3」 2023-07-31 [R1] — Contour I V3 = UltraShape 기기라는 대응은 **이 출처에 없음**(제품 계보상 추정이라 확정 아님) | 하 |
| N14 | TeslaFormer | 현지에 없음 — 영문 `TeslaFormer` | — | 0 | 대륙 출처 못 찾음 | — |

## 3. 표 B — 기존 사전 zh 중 대륙 표기와 다른 것 (D-40 검증)

### B-1 대륙 허가명·공식명이 확인된 것

| term | ko | 지금 zh | 대륙 표기(원문) | 근거 | 확신 |
|---|---|---|---|---|---|
| ph-040 | 리즈톡스 | `丽姿妥适` / [Liztox] | **`解索橙`** · 상품명 `Hutox` · 속칭 `橙毒` | 爱美客 IR 답변 「公司肉毒毒素产品解索橙Hutox于2026年8月3日正式上市销售」 [N2] · 「商品名：HUTOX，俗称“橙毒”」 medbelove 2026-01-19 [M8] · 「国内第七款…Huons BP」 nbd 2026-01-10 [N3] · cls 2026-01-08 [N4]. `丽姿妥适` 은 대륙 출처 0건 | 상 |
| ph-031 | 레티보 | `乐提保` / [Letibo] | **`乐提葆`**(葆) | nbd 2026-01-10 「韩国秀杰（Hugel）的乐提葆」 [N3] · jiemian 2026-03-20 「秀杰的乐提葆」 [N5] | 상 |
| ph-042 | 보툴렉스 | `白毒` / [Botulax] | 보툴렉스 = Letybo 수출명이므로 대륙 제품은 `乐提葆`(위). `白毒` 은 대륙 출처에서 못 찾음 | 위 + 대만 리포트(Letybo=Botulax) | 중 |
| ph-008 | 엘라비에 | `艾拉薇` / [Elravie] | **`艾莉薇`** (2015-01 CFDA, Humedix) | CIRS 승인 필러 목록 「艾莉薇 Elravie | 23 | 2015.01.26」 [R2] · 智研咨询 2019-12-30 「艾莉薇 2015年1月 Humedix」 [N6] · 智研咨询 2020-11-23 「艾莉薇 北京林特医药」 [N7] | 상 |
| ph-112 | 스컬트라 | `素颜萃童颜针` | **`塑妍萃`** (2024-09-30 NMPA, 国械注进20243130557) | medbelove 2024-10-10 · 2025-04-16 [M9]. `素颜萃` · `舒颜萃`(대만명) 대륙 원문 0건 | 상 |
| ph-130 | 써마지FLX | `美版热玛吉FLX` / [Thermage FLX, 热玛吉] | 공식 **`超玛吉FLX`**(2024-01 NMPA) · 「也叫“第五代”热玛吉」 · 브랜드 `Thermage®热玛吉` | medbelove 2024-04-28 [M1] · china.com 「第五代(FLX)」 [Z1]. `美版热玛吉` 은 대륙 원문에서 못 봄(검색 범위 한계) | 상(超玛吉) |
| ph-072 · 075 · 079 | 리쥬란 i · 힐러 · HB+ | `丽珠兰白盒` · `丽珠兰黑盒` · `丽珠兰红盒` | 브랜드 공식 **`丽驻兰`**(「丽驻兰 + REJURAN 双标识」), `丽珠兰` 은 「无商标布局时代…自发通用名称」 | medbelove 2026-07-06 [M10] (CN-P · 브랜드 측 입장 기사). 한국행 플랫폼은 여전히 `丽珠兰` [K2][K3]. `白盒/黑盒/红盒` 은 이번 조사에서 확인 못 함 | 중 — 표 C-7 |
| ph-108 | 쥬베룩 | `乔雅露` / [Juvelook] | 대륙은 2026-07-28 NMPA 허가(华熙生物 대리, 国械注进20263130274) — **중문명은 기사 3편 모두 `JUVELOOK` 영문만**. `乔雅露` 는 대만(muskin) 표기, 대륙 원문 0건 | medbelove 2026-07-31 · 2026-09-18 [M11] · 10jqka 요약 [N8](요약만) | 중 |

### B-2 대륙 허가 목록에 없는 톡신 (지금 zh 는 별명)

대륙 허가 7종 = 衡力 · 保妥适(Botox) · 吉适(Dysport) · 乐提葆(Letybo) · 思奥美(Xeomin) · 达希斐(Daxxify) · 解索橙(Hutox) [N3][N5]. 아래는 **이 목록에 없다**.

| term | ko | 지금 zh | 대륙 근거 |
|---|---|---|---|
| ph-027 | 나보타 | `绿毒` / [Nabota] | 허가 목록에 없음. `绿毒` 대륙 원문 못 찾음 |
| ph-041 | 메디톡신 | `粉毒` / [Meditoxin] | 허가 목록에 없음(华熙-Medytox 톡신 도입은 2023 해지 [M12]) |
| ph-028 | 뉴럭스 | `纽乐适` / [Neurox] | 허가 목록에 없음. `纽乐适` 대륙 원문 못 찾음 |
| ph-044 | 타임버스 | `时光巴士` / [Timbus] | 허가 목록에 없음. `时光巴士` 검색 0건(관련 없는 결과만) |

참고 — 일치 확인: ph-037 `思奥美` · ph-039 `吉适` · ph-005 `乔雅登`(medbelove 「乔雅登®质颜」 등) · ph-006 `瑞蓝`(「瑞蓝®丽瑅」 [M9]) · ph-007 `保柔缇` [Z3] · ph-009 `伊婉` [N6] 은 대륙 표기와 같다.

### B-3 한국 전용 제품 · 음역명 — 대륙 근거 없음

zh-Hant 를 영문으로 바꾼 25 term(ph-001 · 004 · 008 · 040 · 044 · 060 · 062 · 070 · 080 · 081 · 083 · 084 · 088 · 110 · 124 · 134 · 136 · 137 · 140 · 149 · 150 · 151 · 152 · 155 · 157) 중 고유 브랜드명:

| term | ko | 지금 zh | 결과 |
|---|---|---|---|
| ph-001 | 신펄 | `新珍珠` | 대륙 원문 0건 |
| ph-002 · 004 | 채움 · 더채움 | `彩韵` · `彩韵Plus` | 대륙 원문 0건. 강남언니 TW 판(한국 클리닉)에 `德彩` 이 있다는 검색 요약만(원문 미확인 · 대륙 아님) |
| ph-060 | 미라클 | `奇迹线` | 대륙 원문 0건 |
| ph-062 | 에버라인 | `艾芙莱恩` | 대륙 원문 0건(검색 결과는 게임 캐릭터 Evelynn) |
| ph-070 | 벨피엔 | `贝尔菲恩` | 0건 |
| ph-110 | 글로벨라 | `格洛贝拉` | 0건 |
| ph-124 | 더블로골드 | `多普勒金` | 0건 |
| ph-134 | 시크릿 | `Secret黄金微针` | 대륙 원문 0건. 한국행 중문 플랫폼은 `Secret微针电波` · `Secret激光` · `Secret RF` [K2][K1] — 「黄金微针」 은 표 C-1 |
| ph-136 | 아그네스 | `雅格尼斯` | 0건. 한국 클리닉 중문 메뉴 `AGNES` [K1] |
| ph-137 | 인트라셀 | `英特拉赛尔` | 0건 |
| ph-149 · 150 · 151 | 마이셀 · 셀피아 · 리젠ACR | `玛伊赛尔` · `赛尔皮亚` · `瑞珍ACR` | 0건 |
| ph-083 · 084 | 에스에프 · 큐어스킨 | `SF注射` · `CureSkin` | 0건 |

PDRN · PN · SVF · PRP · ACT · MCT · HIFES 는 일반 약어라 이번에 따로 보지 않았다.

## 4. 표 C — 모호한 말

| # | 말 | 걸리는 것 | 근거 |
|---|---|---|---|
| C-1 | `黄金微针` | 대륙에선 **장르 이름**(射频微针 일반) — 여러 제조사(美迪迈 · 金蔓佳 등)가 「黄金微针」 기기를 판다. 사전 ph-135 포텐자 name · ph-134 `Secret黄金微针` 에 걸림 | sina 2026-08-26 「黄金微针设备品牌盘点」 [Z4] · medbelove 「黄金微针领导品牌「美迪迈」」 등 [M13] · yeoti 「Secret激光…常被称为…黄金微针」 [K2] |
| C-2 | `热玛吉` | Thermage 브랜드 전체(CPT 4세대 · FLX 5세대). 「只写"热玛吉"…不注明代际」 가 문제라는 보도 | [Z1][M1] |
| C-3 | `素颜` 계열 | 대륙 `素颜光` = Clear+Brilliant, 사전 ph-112 `素颜萃` = 스컬트라(대륙 공식은 塑妍萃), 대만 `素顏針` = 쥬베룩 · `素妍針` = 벨로테로 리바이브 | [M4][M9] · 대만 리포트 C-5 |
| C-4 | `彩虹` | `彩虹针` = Belotero Revive(HK 기사) 대 대만 `彩虹肉毒` = 나보타 | [HK1] · 대만 리포트 |
| C-5 | `童颜针` | 장르 이름 — 艾塑菲(AestheFill) · 塑妍萃(Sculptra) · JUVELOOK · 艾维岚 · 濡白天使 모두 「童颜针」 | [N1][M5][M9][M11] |
| C-6 | `微波` · `清新` | `清新微波`(miraDry, 땀샘) 대 사전 ph-125 마이크로웨이브 `微波治疗`(기기 리프팅) | [M7] |
| C-7 | `丽珠兰` / `丽驻兰` | 같은 브랜드(REJURAN)의 통칭 · 공식명 — 손님은 `丽珠兰` 으로 말할 가능성 큼 | [M10][K2] |
| C-8 | `橙毒` | 解索橙(Hutox) 속칭. 대만 리포트의 onlineyimei 「Liztox 橙毒」 와 같은 계열 | [M8] |

## 5. 못 읽은 사이트

| 사이트 | 상태 |
|---|---|
| 新氧 soyoung.com | 홈은 200 이지만 Nuxt JS 렌더 · 항목 페이지(`/itemk/`)는 「登录中心」 로 리다이렉트 |
| 更美 gengmei.cn · y.soyoung.com | 연결 실패(000) |
| 바이두 · 소고우 · so.com · DuckDuckGo | 봇 차단(빈 페이지 · 캡차 · 302) — 소고우는 1회만 응답하고 이후 차단 |
| 知乎 zhuanlan.zhihu.com | 403 |
| 虎嗅 huxiu.com | 405 |
| businesswire zh-CN | 응답 없음 |
| 东方财富 wap / 财富号 | 본문이 JS(빈 본문) |

## 6. 출처

| id | 출처 | 성격 | 날짜 |
|---|---|---|---|
| M1 | medbelove 「索塔医疗：旗下「超玛吉FLX」焕新上市」 https://www.medbelove.com/index.php/2024/04/28/%e7%b4%a2%e5%a1%94%e5%8c%bb%e7%96%97%ef%bc%9a%e6%97%97%e4%b8%8b%e3%80%8c%e8%b6%85%e7%8e%9b%e5%90%89flx%e3%80%8d%e7%84%95%e6%96%b0%e4%b8%8a%e5%b8%82%ef%bc%8c%e6%a0%91%e7%ab%8b%e3%80%8c%e5%b0%84/ | CN-P | 2024-04-28 |
| M2 | medbelove 「素夫波：国内首款…SofWave」 https://www.medbelove.com/index.php/2024/07/09/%E7%B4%A2%E5%A4%AB%E6%B3%A2%EF%BC%9A%E5%9B%BD%E5%86%85%E9%A6%96%E6%AC%BE%E3%80%8C%E5%8E%BB%E7%9A%B1%E6%8F%90%E5%8D%87%E3%80%8D%E5%9B%BD%E9%99%85%E5%8F%8C%E8%AE%A4%E8%AF%81sofwave%E3%80%8C/ | CN-P | 2024-07-09 |
| M3 | medbelove 「爱美客：获得Jeisys公司旗下2款医美设备…独家经销权」 https://www.medbelove.com/index.php/2023/11/22/%e7%88%b1%e7%be%8e%e5%ae%a2%ef%bc%9a%e8%8e%b7%e5%be%97jeisys%e5%85%ac%e5%8f%b8%e6%97%97%e4%b8%8b2%e6%ac%be%e5%8c%bb%e7%be%8e%e8%ae%be%e5%a4%87%e5%9b%bd%e5%86%8510%e5%b9%b4%e7%8b%ac%e5%ae%b6/ | CN-P | 2023-11-22 |
| M4 | medbelove 「热光联合品项发布会暨「索塔®素颜光」新品上市会」 https://www.medbelove.com/index.php/2026/09/14/%e7%b4%a7%e8%87%b4%e7%84%95%e4%ba%ae%ef%bc%8c%e5%85%89%e8%80%80%e5%90%af%e7%a8%8b-%e7%83%ad%e5%85%89%e8%81%94%e5%90%88%e5%93%81%e9%a1%b9%e5%8f%91%e5%b8%83%e4%bc%9a%e6%9a%a8%e3%80%8c%e7%b4%a2/ | CN-P | 2026-09-14 |
| M5 | medbelove 사이트 검색 「艾塑菲」(기사 10편 — 「艾塑菲童颜针」 「江苏吴中：艾塑菲品牌上市峰会」 등) https://www.medbelove.com/?s=%E8%89%BE%E5%A1%91%E8%8F%B2 | CN-P | 2024~2026 |
| M6 | medbelove 사이트 검색 「海菲秀」(5편) https://www.medbelove.com/?s=%E6%B5%B7%E8%8F%B2%E7%A7%80 | CN-P | — |
| M7 | medbelove 「miraDry | 锚定腋下蓝海」 https://www.medbelove.com/index.php/2026/09/23/miradry-%e9%94%9a%e5%ae%9a%e8%85%8b%e4%b8%8b%e8%93%9d%e6%b5%b7%ef%bc%8c%e7%a7%91%e6%8a%80%e5%bc%95%e9%a2%86%e3%80%8c%e5%81%a5%e5%ba%b7%e7%be%8e%e5%ad%a6%e3%80%8d%e4%bb%b7%e5%80%bc%e5%88%9b%e6%96%b0/ | CN-P | 2026-09-23 |
| M8 | medbelove 「爱美客 | 苦等八年「橙毒」获批」 https://www.medbelove.com/index.php/2026/01/19/%E7%88%B1%E7%BE%8E%E5%AE%A2-%E8%8B%A6%E7%AD%89%E5%85%AB%E5%B9%B4%E3%80%8C%E6%A9%99%E6%AF%92%E3%80%8D%E8%8E%B7%E6%89%B9%EF%BC%8C%E3%80%8C%E8%82%89%E6%AF%92%E5%B8%82%E5%9C%BA%E3%80%8D%E5%86%8D/ | CN-P | 2026-01-19 |
| M9 | medbelove 「高德美 | 国内第四款「童颜针」Sculptra®「塑妍萃」正式获批」 https://www.medbelove.com/index.php/2024/10/10/%e9%ab%98%e5%be%b7%e7%be%8e-%e5%9b%bd%e5%86%85%e7%ac%ac%e5%9b%9b%e6%ac%be%e3%80%8c%e7%ab%a5%e9%a2%9c%e9%92%88%e3%80%8dsculptra%e3%80%8c%e5%a1%91%e5%a6%8d%e8%90%83%e3%80%8d%e6%ad%a3%e5%bc%8f/ (+ 2025-04-16 上市发布) | CN-P | 2024-10-10 |
| M10 | medbelove 「丽驻兰｜头皮水光全新上市，理清「REJURAN更名」背后的合规真相」 https://www.medbelove.com/index.php/2026/07/06/%e4%b8%bd%e9%a9%bb%e5%85%b0%ef%bd%9c%e5%a4%b4%e7%9a%ae%e6%b0%b4%e5%85%89%e5%85%a8%e6%96%b0%e4%b8%8a%e5%b8%82%ef%bc%8c%e7%90%86%e6%b8%85%e3%80%8crejuran%e6%9b%b4%e5%90%8d%e3%80%8d%e8%83%8c%e5%90%8e/ | CN-P(브랜드 측 입장) | 2026-07-06 |
| M11 | medbelove 「华熙生物 | 复合型「童颜针」JUVELOOK获批」 https://www.medbelove.com/index.php/2026/07/31/%e5%8d%8e%e7%86%99%e7%94%9f%e7%89%a9-%e5%a4%8d%e5%90%88%e5%9e%8b%e3%80%8c%e7%ab%a5%e9%a2%9c%e9%92%88%e3%80%8djuvelook%e8%8e%b7%e6%89%b9%ef%bc%8c%e6%89%a9%e5%85%85%e3%80%8cecm%e6%8a%97%e8%a1%b0/ · 2026-09-18 「JUVELOOK在韩国打输的官司」 | CN-P | 2026-07-31 · 09-18 |
| M12 | medbelove 「华熙生物：与韩国Medytox正式解约」 (사이트 검색 「Medytox」) | CN-P | 2023-09-08 |
| M13 | medbelove 사이트 검색 「黄金微针」(美迪迈 · 金蔓佳 · 金达威 기사) | CN-P | 2025 |
| N1 | 界面新闻 「首款进口童颜针上市半年卖了两个亿」 https://m.jiemian.com/article/11863896.html | CN-N | 2024-10 |
| N2 | 凤凰网(证券之星) 「爱美客：公司肉毒毒素产品解索橙Hutox于2026年8月3日正式上市销售」 https://i.ifeng.com/c/8vJkzhCPh7v | CN-N(IR 답변) | 2026-08-04 |
| N3 | 每经网 「爱美客肉毒素产品获批 国内“除皱神器”增至7款」 https://www.nbd.com.cn/articles/2026-01-10/4214916.html | CN-N | 2026-01-10 |
| N4 | 财联社 https://www.cls.cn/detail/2252324 | CN-N | 2026-01-08 |
| N5 | 界面新闻 「爱美客是如何从高增长走向首次“双跌”的？」 https://www.jiemian.com/article/14142991.html | CN-N | 2026-03-20 |
| N6 | 智研咨询 「2018年中国玻尿酸行业原料市场及市场格局分析」 https://www.chyxx.com/industry/201912/823487.html | CN-N(산업 리포트) | 2019-12-30 |
| N7 | 智研咨询 「2019年中国玻尿酸行业销售量…」 https://www.chyxx.com/industry/202011/911494.html | CN-N | 2020-11-23 |
| N8 | 同花顺 https://news.10jqka.com.cn/20260923/c680220393.shtml (요약만 · 원문 미확인) | CN-N | 2026-09-23 |
| I1 | 爱美客 2026 半年度报告 https://static.cninfo.com.cn/finalpage/2026-08-21/1225487535.PDF | CN 공시 | 2026-08-21 |
| H1 | 华瑭医疗 제품 페이지 「Sofwave™素芙波」 https://www.htdkgroup.com/products/sofwave | CN 대리상 공식 | 2026 |
| Y1 | 医美行业观察 「Sofwave素芙波国内首次亮相」 https://www.ymguancha.com/post/18878.html | CN-P | 2026-10-22 |
| Z1 | 中华网 「北京热玛吉价格…2026年选择指南」 https://m.tech.china.com/redian/2026/0813/082026_1940215.html | CN-N(광고성) | 2026-08-13 |
| Z2 | 中华网 「Sofwave素芙波开启超声新时代」 https://m.tech.china.com/tech/article/20240821/082024_1563937.html | CN-N | 2024-08-21 |
| Z3 | 中华网 「…保柔缇让每一次改变都“美得自然而然”」 https://m.tech.china.com/hea/articles/20260327/202603271834394.html | CN-N(광고성) | 2026-03-27 |
| Z4 | 新浪 「黄金微针设备品牌盘点」 https://news.sina.cn/sx/2026-08-26/detail-inippvuh9593847.d.html | CN-N(광고성) | 2026-08-25 |
| J1 | 聚美网 「面部肌肉抗老抗衰黑科技Emface怎么样」 https://www.it322.com/bk/ks_2225.html | CN-P | 2024-02-18 |
| C1 | 凤凰网 「深圳联合丽格：风靡欧美的BTLEMface美菲斯」 https://baby.ifeng.com/c/8SUJV1H87yd | CN-C(보도자료) | 2023-08-23 |
| C2 | 品牌网 「深圳贝比蓝：EMFACE美菲斯…」 https://m.chinapp.com/hangyedongtai/220086 | CN-C(보도자료) | 2024-10-10 |
| F1 | 复星医药 「复锐医疗科技宣布…Profhilo®正式获国家药监局受理」 https://www.fosunpharma.com/content/details38_11310.html | CN 공식 | 2023-12-11 |
| T1 | 腾讯云 개발자 커뮤니티(企鹅号 医美视界) 「海菲秀重磅新品发布」 https://cloud.tencent.com/developer/news/1051237 | CN-P | 2023-04-10 |
| R1 | CIRS 「【收藏】已注册有源医美产品汇总」 https://www.cirs-group.com/cn/md/shou-cang-yi-zhu-ce-you-yuan-yi-mei-chan-pin | CN 규제 컨설팅 | 2023-07-31 |
| R2 | CIRS 「CFDA 批准的注射填充美容产品汇总」 https://www.cirs-group.com/cn/md/cfdapzdzstctmzscphz%EF%BC%88fzccpxx%EF%BC%89 | CN 규제 컨설팅 | 2017-05-31 |
| S1 | StockHub 「Medytox Obtains Marketing Approval in China for Hyaluronic Acid Filler」 https://stockhub.kr/en/news/news_d0c337f519c3 | KR 보도 | 날짜 없음 |
| G1 | GlobeNewswire 「Meheco Named the Exclusive Partner for Miramar Labs miraDry Distribution in China」 https://www.globenewswire.com/news-release/2016/06/17/849426/0/en/ | 영문 보도 | 2016-06-17 |
| HK1 | 香港01 「水光針｜國內貴婦來香港都找它！大熱Revive…」 https://www.hk01.com/醫美Easy/1096759 | HK · 협찬 | 2025-01-23 |
| K1 | id艾蒂皮肤科 「项目 / 价格」 https://www.idclinic.co.kr/zh-cn/treatment-catalog | KR-zh | 날짜 없음 |
| K2 | YEOTI 「Secret微针电波全攻略」 https://yeoti.cn/secret-rf-microneedling-guide/ | KR-zh(한국행 플랫폼) | 2026-07-18 |
| K3 | 非常爱美 「2026韩国moonclinic皮肤科价格表」 https://www.verym.com/yiyuan/930/gl_76169.html | KR-zh | 2026 |

## 7. 코디 · 사용자가 정할 것 (결정하지 않음)

1. 표 B-1 의 6 term name 을 대륙 공식명으로 바꿀지(解索橙 · 乐提葆 · 艾莉薇 · 塑妍萃 · 超玛吉FLX · 丽驻兰) — 지금 표기는 alias 로 내릴지
2. 대륙 미허가 톡신(나보타 · 메디톡신 · 뉴럭스 · 타임버스)의 zh name — D-38 처럼 영문으로 둘지, 색 별명을 남길지. 보툴렉스(ph-042)를 레티보와 같은 `乐提葆` 로 둘지
3. 표 B-3 한국 전용 제품 음역명 — D-40 규칙대로 영문 name · 지금 음역은 alias 로 둘지(대륙 근거 0건)
4. 쥬베룩(ph-108) — 대륙 허가는 났지만 중문명이 `JUVELOOK` 영문뿐. `乔雅露`(대만명)를 유지할지
5. 표 A 의 「중문명 못 찾음」 7개는 영문 name 으로 둘지. N01 Thermage CPT 의 name 형태(`Thermage CPT` 대 `热玛吉CPT`)
6. 표 C 의 장르어(黄金微针 · 热玛吉 · 童颜针 · 素颜)를 alias 에서 뺄지
