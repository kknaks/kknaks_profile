# R4a — 영문 `name` 을 그 나라 글자로 · 중국어권 3개(zh · zh-Hant · yue) (DEC D-61)

- 조사 날짜: **2026-11-15** · researcher(read-only) · **결정하지 않음** — 판정과 근거만
- 대상: `quality-r4-targets.json` 의 담당 언어 행 **136칸**(zh 42 · zh-Hant 29 · yue 65) — 시드 `.8` 에서 `name` 이 영문인 칸
- 기계 대조용 전체: `r4a-zh.json`(136행)
- 원칙(D-61): 그 나라 글자 표기가 **현지 클리닉 · 현지 플랫폼에 있으면** `name` 으로, 영문은 별칭으로. 지어낸 음역 · 별명은 쓰지 않는다

## 결론 먼저

1. **136칸 중 38칸에서 그 나라 글자 표기를 찾았다**(zh 4 · zh-Hant 10 · yue 24). 그중 출처 2곳 이상(reviewed true 제안)은 27칸
2. **나머지 98칸은 영문 그대로** — 현지 표기 없음 90 · 별명뿐 3 · 일반어인데 정해진 현지 이름이 없는 것 5
3. **홍콩(yue)이 가장 많이 바뀐다.** 홍콩 클리닉은 영문 상표 옆에 시장 이름을 붙여 판다(`鋼筋索` · `無雙電波` · `原美電波` · `黃金樁` · `鑽石超塑` · `海菲秀` · `膠原槍` · `素顏針` · `塑顏針` · `美肌針`). 앞 조사(R1)는 이 칸들을 「현지도 영문」 으로 셌다
4. **대륙(zh)은 거의 안 바뀐다.** 新氧 상품 검색에서 대상 브랜드 대부분이 제목 일치 0건이다 — 대륙에 팔리지 않는 한국 제품 · 기기라 현지 표기 자체가 없다. 바뀌는 것은 `热玛吉四代` · `纽拉美斯` · `帝医思黄金微针` · `多聚核苷酸` 넷
5. **한국 내수 브랜드**(신펄 · 채움 · 더채움 · 타임버스 · 에버라인 · 벨피엔 · 에스에프 · 큐어스킨 · 글로벨라 · 마이셀 · 셀피아 · 리젠ACR · ACT · MCT · 리투오)는 세 나라 모두 0건 — 영문 그대로. 시드 별칭에 든 한자 꼴(`新珍珠` · `彩韵` · `时光巴士` · `艾芙莱恩` · `贝尔菲恩` · `格洛贝拉` · `多普勒金` · `雅格尼斯` · `英特拉赛尔` · `玛伊赛尔` · `赛尔皮亚` · `瑞珍ACR`)은 어디에서도 못 찾았다
6. 바로 반영하기 전에 정해야 할 것이 있다 — **상자 색 표기**(`麗珠蘭白盒` 류)와 **「~針」 꼴 시장 이름**을 별명으로 볼지, **두 표기가 갈리는 칸**(Dysport · PDRN · INTRAcel)을 어느 쪽으로 할지(「정할 것」)

## 방법

1. **앞 조사 본문 재사용** — R1(2026-11-14)이 받아 둔 현지 클리닉 공식 사이트 본문(대륙 6 + 보조 1 · 대만 6 · 홍콩 6 + 보조 2 · 사이트당 최대 300쪽)에서, 칸마다 영문 상표 **앞뒤에 붙은 한자 낱말**을 사이트별로 세고 문맥을 눈으로 확인했다
2. **현지 플랫폼** — 대륙은 **新氧(soyoung.com) 상품 검색**: 칸마다 영문 상표 · 지금 별칭의 한자 꼴로 검색해 **상품 제목에 그 글자가 든 것만** 셌다(검색이 느슨해 무관한 상품이 섞인다). 대만은 **醫美圈圈(worthit.com.tw)** 1건
3. **웹 검색(Yahoo 홍콩 · 대만)** — 본문에 없는 칸은 「상표 + 香港 / 診所」 로 검색해 **결과의 제목 · 발췌 글자를 그대로** 읽었다. 한국 병원 외국어 페이지 · 한국 회사 플랫폼(강남언니 · creatrip 등)은 걸러 냈고, 홍콩 검색에 섞여 나온 대만 클리닉은 홍콩 근거로 치지 않았다. 핵심 출처 11쪽은 쪽 제목을 직접 받아 확인했다(표의 ✔)
4. **판정**
   - 「현지 글자로」: 현지 클리닉 · 플랫폼 1곳 이상이 그 글자를 **그 상표의 이름으로** 쓴다. 2곳 이상이면 reviewed true 제안
   - 클리닉이 지은 자기 상품명(DR REBORN 「羽點美肌療程」 류)과 기술 설명(「絶緣射頻」 · 「退紅激光」 · 「微波止汗」)은 이름으로 치지 않았다 → 「현지 표기 없음」 + 메모
   - 색 별명(`绿毒` · `粉毒` · 병 색)은 「별명뿐」
- ⚠ 한계
  - **검색으로만 본 출처는 제목 · 발췌까지만 확인했다**(쪽 본문 전체를 읽지 않음). 표 A 메모에 「검색」 이라 적은 곳이 그렇다
  - 新氧은 PC 웹 검색 결과(쪽당 10건)만 봤다. 앱 안의 표기 · 百科 항목은 못 봤다. 「제목 일치 0」 은 「그 검색 10건 안에 없다」 는 뜻이다
  - 대륙 클리닉 본문은 R1 과 같이 얇다(한국 브랜드 주사 · 기기를 거의 안 다룸)
  - 2 ~ 3자 영문 약어(ACT · MCT)는 글자 대조를 믿을 수 없어 「현지 표기 없음」 으로 뒀다

## 사이트 · 플랫폼

### 클리닉 공식 사이트 (R1 본문 재사용)

| # | 나라 | 이름 | URL |
|---|---|---|---|
| C1 | 대륙 | 上海美莱医疗美容医院 | http://www.shmylike.com/ |
| C2 | 대륙 | 上海艺星医疗美容医院 | http://www.shyestar.com/ |
| C3 | 대륙 | 中国医学科学院整形外科医院 | https://www.zhengxing.com.cn/ |
| C4 | 대륙 | 四川华美紫馨医学美容医院 | http://www.cdhuamei.com/ |
| C5 | 대륙 | 重庆当代整形外科医院 | https://www.cqddzx.com/ |
| C6 | 대륙 | 长沙雅美医疗美容医院 | https://www.csyamei.com/ |
| C7(보조) | 대륙 | 杭州艺星医疗美容医院 | https://www.hzyestar.com/ |
| T1 | 대만 | 粹究美學診所 | https://tresure-clinic.com/ |
| T2 | 대만 | 木木日安皮膚科診所 | https://www.muskin.com.tw/ |
| T3 | 대만 | 愛爾麗診所 | https://www.airlee.com.tw/ |
| T4 | 대만 | 映玥美型診所 | https://hikaruclinic.com/ |
| T5 | 대만 | 佳醫美人診所 | http://www.beautyclinic.com.tw/ |
| T6 | 대만 | 韓佳人診所 | https://www.koreabeautydream.com/ |
| H1 | 홍콩 | DR REBORN | https://www.drreborn.com/ |
| H2 | 홍콩 | Perfect Medical | https://www.psmedical.com.hk/ |
| H3 | 홍콩 | Go Young | https://goyoung.com.hk/ |
| H4 | 홍콩 | MÍOGGÍ | https://www.mioggi.com/ |
| H5 | 홍콩 | COSMED 映匯醫學集團 | https://cosmed.hk/ |
| H6 | 홍콩 | SurrFACE Medical | https://surrface.com.hk/ |
| H7(보조) | 홍콩 | CosMax | https://www.cosmax.com.hk/ |
| H8(보조) | 홍콩 | Pretty Medical | https://prettymedical.com.hk/ |

### 이번에 더 본 곳 (검색 결과 제목 · 발췌 — ✔ 는 쪽 제목 직접 확인)

| # | 나라 | 이름 | URL | 쓴 칸 |
|---|---|---|---|---|
| P1 | 대륙 | **新氧**(플랫폼 · 상품 검색) | https://www.soyoung.com/searchNew/product?keyword=… | zh 42칸 전부 |
| P2 | 대만 | **醫美圈圈**(플랫폼) ✔ | https://www.worthit.com.tw/therapy/info/232 | Doublo Gold |
| T7 | 대만 | 彭賢禮皮膚科診所 ✔ | https://www.pskin.tw/mc_services/revlite/ | RevLite |
| T8 | 대만 | 順風美醫診所 ✔ | https://www.sfclinic.com.tw/miraclethread/ | Miracle Thread |
| T9 | 대만 | 夏爾診所 ✔ | https://shirebeauty.com.tw/intracel/ | INTRAcel |
| T10 | 대만 | iSkin尚行美健康聯合診所 | https://www.iskin.com.tw/ | INTRAcel |
| T11 | 대만 | dunyenclinic.com(클리닉) | https://dunyenclinic.com/ | Doublo Gold |
| T12 | 대만 | 美麗爾診所 ✔ · sccare.com.tw · 健立診所 | https://www.merrier.com.tw/treatment-33.html · https://sccare.com.tw/ · https://regentaiwan.com/prp | PRP |
| T13 | 대만 | skin-cosda | https://www.skin-cosda.com/ | AGNES |
| H9 | 홍콩 | LM Skin Centre ✔ | https://lmskincentre.com/ | Xeomin · InMode · EXION |
| H10 | 홍콩 | BEAUSKIN Medical ✔ · Dear Beauty | https://beauskinmedical.hk/dysport · https://mydearbeauty.hk/pages/dysport | Dysport · Ultraformer |
| H11 | 홍콩 | Empathy ✔ · Hada Hana | https://www.empathy.com.hk/oligiox · https://hadahana.hk/ | Oligio |
| H12 | 홍콩 | AMOUR · Love Share Beauty | https://amour-group.com/volnewmer/ · https://lovesharebeauty.com/pages/volnewmer | Volnewmer |
| H13 | 홍콩 | PEKO ✔ | https://www.peko.com.hk/treatments/btl-exion/ | EXION |
| H14 | 홍콩 | MEDILASE ✔ · MIIO | https://www.medilase.com.hk/beauty-density.php · https://miio.hk/ | DENSITY |
| H15 | 홍콩 | REDEFINE · D-Skin · Trinity Medical | https://www.redefine.com.hk/ · https://www.d-skin.com.hk/ · https://trinitymedical.com.hk/ | Juvelook · Rejuran |
| H16 | 홍콩 | arum.hk · Initial Plus · Rootology · Kairos | (표 A 출처) | Rejuran 갈래 |
| H17 | 홍콩 | AG Beauty · MedSkin+ | https://www.agbeauty.com.hk/inmodeformai · https://medskinplus.com/ | InMode |
| H18 | 홍콩 | Beauty101 · YSO | https://www.beauty101hk.com/ · https://www.ysobeauty.com/ | Silhouette Soft |
| H19 | 홍콩 | iBeauty | https://ibeauty.com.hk/ | LDM |
| H20 | 홍콩 | All Beauty Medical | https://www.allbeautymedical.hk/ | PicoSure · Ultraformer(쪽 본문 차단 — 검색 결과만) |
| H21 | 홍콩 | 통증 · 정형 클리닉 2 · 仁恩 | (표 A 출처) | PRP — 미용 클리닉 아님 |

- 근거로 **치지 않은** 것: gangnamunni · creatrip · 한국 병원의 중문 쪽 · 판매상(lushfills 「傑特瑪毒素」) · 보도(「普菲洛」)


## 판정 집계

| 언어 | 현지 글자로 | 일반어 → 현지 글자 | 일반어 → 영문 그대로 | 현지 표기 없음 | 별명뿐 | 합 | name 이 바뀌는 칸 | 그중 reviewed true 제안 |
|---|---|---|---|---|---|---|---|---|
| zh | 3 | 1 | 2 | 33 | 3 | 42 | 4 | 2 |
| zh-Hant | 6 | 4 | 1 | 18 | 0 | 29 | 10 | 7 |
| yue | 21 | 3 | 2 | 39 | 0 | 65 | 24 | 18 |
| **합** | 30 | 8 | 5 | 90 | 3 | **136** | **38** | **27** |

- 「name 이 바뀌는 칸」 = 현지 글자로 + 일반어 → 현지 글자. 나머지 98칸은 영문 `name` 그대로

## 표 A — 「현지 글자로」 (일반어 포함 · 38칸)

| id | ko | 언어 | 지금 name | 제안 name | 별칭 | 판정 | 출처 | reviewed | 메모 |
|---|---|---|---|---|---|---|---|---|---|
| ph-081 | PN | zh | `PN` | **`多聚核苷酸`** | `PN` | 일반어 | [hzyestar.com](https://www.hzyestar.com/news/59611.html) | false | 杭州艺星(R1 보조 B1) 「PN多聚核苷酸在临床应用的分享」 1곳. 新氧 상품 제목은 영문 「PN」 · 「三文鱼PN水光」(별명) — 손님이 보는 표기는 영문 약어 쪽 |
| ph-137 | 인트라셀 | zh | `INTRAcel` | **`帝医思黄金微针`** | `再希思黄金微针` · `Intracel黄金微针` · `INTRAcel` · `INTRACELL` | 현지 글자로 | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=INTRAcel) · [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=%E5%B8%9D%E5%8C%BB%E6%80%9D) · [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=%E5%86%8D%E5%B8%8C%E6%80%9D) · [新氧 상품](https://www.soyoung.com/cp1337953) · [新氧 상품](https://www.soyoung.com/cp10666993) | true | 新氧 「韩国进口帝医思黄金微针（Intracel）」(广州丽合) · 「再希思Intracel黄金微针」(上海和德 · 武汉中翰) · 「Intracel黄金微针」(上海华美). ⚠ 한자 표기가 둘(帝医思 · 再希思 — 둘 다 제조사 Jeisys 의 표기) — 어느 쪽을 name 으로 할지 정할 것. 지금 별칭 「英特拉赛尔」 은 0건 |
| kr-001 | 써마지 CPT | zh | `Thermage CPT` | **`热玛吉四代`** | `热玛吉CPT` · `Thermage CPT` · `四代热玛吉` | 현지 글자로 | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=%E7%83%AD%E7%8E%9B%E5%90%89%E5%9B%9B%E4%BB%A3) · [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=%E7%83%AD%E7%8E%9B%E5%90%89CPT) · [cqddzx.com](https://www.cqddzx.com/tech/qingbao-thermage) | true | 新氧 상품 제목 · 항목 꼬리표가 「热玛吉四代」 · 「四代热玛吉」(厦门华美 · 杭州艺星 · 济南海峡 등 9건). 重庆当代 「Thermage 热玛吉正品仪器及探头（四代 / 五代）」. 글자 「热玛吉CPT」 는 新氧 제목 0건 — 지금 별칭 그대로 둠 |
| kr-008 | 뉴라미스 | zh | `Neuramis` | **`纽拉美斯`** | `Neuramis` | 현지 글자로 | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=%E7%BA%BD%E6%8B%89%E7%BE%8E%E6%96%AF) · [新氧 상품](https://www.soyoung.com/cp11217663) | false | 新氧 「纽拉美斯（黄盒）玻尿酸1mL」 — 常德德美整形美容 한 곳(상품 2건). 출처 1 |
| ph-008 | 엘라비에 | zh-Hant | `Elravie` | **`艾麗微`** | `Elravie` | 현지 글자로 | [tresure-clinic.com](https://tresure-clinic.com/collagen-skin-booster/) | false | 粹究 「Elravie（艾麗微）是韓國生技廠 Humedix 旗下的注射美學品牌」 · 표 「品牌 Elravie 艾麗微」. 출처 1(제품 소개 글 — 대만 미허가 제품) |
| ph-019 | 레블라이트 | zh-Hant | `RevLite` | **`淨化光雷射`** | `淨膚雷射` · `RevLite` | 현지 글자로 | [tresure-clinic.com](https://tresure-clinic.com/portfolio-item/%E6%B7%A8%E8%86%9A%E9%9B%B7%E5%B0%84/) · [pskin.tw](https://www.pskin.tw/mc_services/revlite/) | true | 粹究 「REVLITE淨化光雷射 … 也稱為V淨化光雷射」 · 彭賢禮皮膚科 쪽 제목 「REVLITE 淨化光雷射」. 지금 별칭 「淨膚雷射」 은 범주 이름(토닝 ph-012 의 name 과 같음) |
| ph-060 | 미라클 | zh-Hant | `Miracle Thread` | **`提美拉`** | `Miracle Thread` | 현지 글자로 | [tresure-clinic.com](https://tresure-clinic.com/portfolio-item/%e5%9f%8b%e7%b7%9a%e6%8b%89%e6%8f%90/) · [sfclinic.com.tw](https://www.sfclinic.com.tw/miraclethread/) · [koreabeautydream.com](https://www.koreabeautydream.com/treatments/plastic-surgery/mint-lifting-guide) | true | 粹究 선재 비교표 「提美拉 MIRACLE THREAD · 俗稱 提美拉」 · 順風美醫 쪽 제목 「提美拉」 · 韓佳人 「芭比線又稱為提美拉」(R1 S6) |
| ph-080 | PDRN | zh-Hant | `PDRN` | **`聚去氧核苷酸`** | `PDRN` · `多聚脫氧核苷酸` | 일반어 | [tresure-clinic.com](https://tresure-clinic.com/rejuran-news/) · [hikaruclinic.com](https://hikaruclinic.com/news/news01/) | false | ⚠ 풀이 표기가 곳마다 다르다 — 粹究 「PDRN（聚去氧核苷酸）」 · 映玥 「PDRN (多聚脫氧核苷酸)」. 지금 별칭 「聚脫氧核苷酸」 은 6곳 0건. 두 곳 모두 영문 PDRN 을 앞세우고 괄호로 풀이 — 어느 꼴을 name 으로 할지(또는 영문 그대로) 정할 것 |
| ph-081 | PN | zh-Hant | `PN` | **`多核苷酸`** | `PN` | 일반어 | [tresure-clinic.com](https://tresure-clinic.com/rejuran-news/) · [hikaruclinic.com](https://hikaruclinic.com/news/news01/) | true | 粹究 「PN（多核苷酸）」 · 映玥 「PN(多核苷酸)」 |
| ph-124 | 더블로골드 | zh-Hant | `Doublo Gold` | **`黃金倍提音波`** | `Doublo Gold` · `倍提音波` | 현지 글자로 | [dunyenclinic.com](https://dunyenclinic.com/doublo-gold-%E9%BB%83%E9%87%91%E5%80%8D%E6%8F%90%E9%9F%B3%E6%B3%A2%EF%BD%9C%E6%96%B0%E4%B8%80%E4%BB%A3%E9%9F%B3%E6%B3%A2%E6%8B%89%E6%8F%90%EF%BC%8C%E5%BF%AB%E9%80%9F%E9%87%8D%E6%8B%BE%E7%B7%8A/) · [worthit.com.tw](https://www.worthit.com.tw/therapy/info/232) · [tresure-clinic.com](https://tresure-clinic.com/hifu-price/) | true | 대만 클리닉 「Doublo Gold 黃金倍提音波」 · 醫美圈圈(대만 플랫폼) 「Doublo Gold 黃金倍提音波 … 是倍提音波的改良進階版，於2021年通過台灣衛福部核准上市」 · 粹究 「倍提音波(Doublo)」(앞 세대) |
| ph-136 | 아그네스 | zh-Hant | `AGNES` | **`精準電波`** | `AGNES` | 현지 글자로 | [skin-cosda.com](https://www.skin-cosda.com/edcontent_d.php?lang=tw&tb=3&id=957) | false | 대만 클리닉 글 제목 「AGNES精準電波 改善眼袋好輕鬆」 1곳 — 영문 브랜드에 붙인 말. 출처 1 |
| ph-137 | 인트라셀 | zh-Hant | `INTRAcel` | **`標靶電波`** | `INTRAcel` · `4D標靶電波` | 현지 글자로 | [shirebeauty.com.tw](https://shirebeauty.com.tw/intracel/) · [iskin.com.tw](https://www.iskin.com.tw/service/3/%E6%A8%99%E9%9D%B6%E9%9B%BB%E6%B3%A2%E2%88%95INTRAcel%E9%9B%BB%E6%B3%A2) | true | 夏爾診所 쪽 제목 「4D標靶電波」(주소 /intracel/) · iSkin尚行美 「標靶電波∕INTRAcel電波」. 粹究는 영문 「INTRAcel微針電波」 |
| ph-140 | HIFES/EMS | zh-Hant | `HIFES` | **`高強度電場`** | `HIFES` · `高強度電場技術` | 일반어 | [hikaruclinic.com](https://hikaruclinic.com/course/emface/) · [tresure-clinic.com](https://tresure-clinic.com/portfolio-item/emface/) · [airlee.com.tw](https://www.airlee.com.tw/news/390) | true | 映玥 「高強度電場技術 HIFES™」 · 粹究 「高強度電場技術（HIFES™）」 · 愛爾麗 「以高強度電場刺激肌肉收縮」. 기기 이름은 菲斯波(EMFACE) |
| ph-157 | PRP (혈소판풍부혈장) | zh-Hant | `PRP` | **`高濃度血小板血漿`** | `PRP` · `自體血小板血漿` | 일반어 | [sccare.com.tw](https://sccare.com.tw/what-is-platelet-rich-plasma/) · [merrier.com.tw](https://www.merrier.com.tw/treatment-33.html) · [regentaiwan.com](https://regentaiwan.com/prp) | true | 대만 클리닉 3곳 「PRP 高濃度血小板血漿」. 粹究는 「PRP 自體血小板血漿」(https://tresure-clinic.com/portfolio-item/code-x/). 지금 별칭 「自體血小板」 은 그 줄임 |
| ph-008 | 엘라비에 | yue | `Elravie` | **`艾莉薇`** | `Elravie` | 현지 글자로 | [goyoung.com.hk](https://goyoung.com.hk/news/20240103) | false | Go Young 「其他出名嘅透明質酸品牌，例如：…伊婉/YVOIRE、艾莉薇/ELRAVIE」 1곳(대륙 허가명과 같은 글자) |
| ph-009 | 이브아르 | yue | `Yvoire` | **`伊婉`** | `Yvoire` | 현지 글자로 | [goyoung.com.hk](https://goyoung.com.hk/news/20240103) | false | Go Young 「伊婉/YVOIRE」 1곳(대륙 허가명과 같은 글자) |
| ph-017 | 피코슈어 | yue | `PicoSure` | **`蜂巢皮秒激光`** | `PicoSure` | 현지 글자로 | [psmedical.com.hk](https://www.psmedical.com.hk/blog/pigmentation-removal-tips/picosure-laser/) · [allbeautymedical.hk](https://www.allbeautymedical.hk/picosurepro-%E8%9C%82%E5%B7%A2%E7%9A%AE%E7%A7%92%E6%BF%80%E5%85%89) | true | Perfect Medical 「蜂巢皮秒激光有效嗎？」(주소 picosure-laser · 「進行Picosure 蜂巢皮秒…」) · All Beauty Medical 주소 「picosurepro-蜂巢皮秒激光」(쪽 본문은 차단돼 검색 결과로만 확인). ⚠ 홍콩에서 「蜂巢皮秒」 는 다른 기기에도 쓴다(MÍOGGÍ 「PICO Laser 蜂巢皮秒激光」 · SurrFACE 「enLIGHTen黃金蜂巢皮秒」) |
| ph-021 | IPL | yue | `IPL` | **`彩光`** | `IPL` · `光子嫩膚` | 일반어 | [surrface.com.hk](https://surrface.com.hk/) · [psmedical.com.hk](https://www.psmedical.com.hk/blog/acne-health/rosacea-lasers/) · [prettymedical.com.hk](https://prettymedical.com.hk/) · [cosmed.hk](https://cosmed.hk/) | true | SurrFACE 「屬於彩光(IPL)技術」 · Perfect Medical 「激光治療和彩光治療怎麽選」 · Pretty Medical 「利用彩光為客人處理雀斑」 · COSMED 「激光彩光後使用」. 시술 메뉴 이름은 「光子嫩膚」 도 많다(Go Young 48쪽 · SurrFACE 메뉴) |
| ph-037 | 제오민 | yue | `Xeomin` | **`淨優明`** | `Xeomin` | 현지 글자로 | [lmskincentre.com](https://lmskincentre.com/tc/%E9%86%AB%E5%AD%B8%E7%BE%8E%E5%AE%B9/xeomin/) | false | LM Skin Centre(홍콩) 쪽 제목 「Xeomin - 淨優明肉毒桿菌素」 1곳(대만 허가명과 같은 글자). 홍콩 4곳(DR REBORN · Go Young · CosMax · COSMED)과 공식 xeominhk.com 은 영문 「XEOMIN」. Go Young 글 제목 「德國西馬」 1쪽 |
| ph-039 | 디스포트 | yue | `Dysport` | **`儷緻`** | `Dysport` · `麗舒妥` · `儷致` | 현지 글자로 | [beauskinmedical.hk](https://beauskinmedical.hk/dysport) · [mydearbeauty.hk](https://mydearbeauty.hk/pages/dysport) · [cosmax.com.hk](https://www.cosmax.com.hk/treatment/refinement/) · [cosmed.hk](https://cosmed.hk/botox-1/) | true | BEAUSKIN Medical 쪽 제목 「DYSPORT® 儷緻 肉毒桿菌素」 · Dear Beauty 「DYSPORT 的中文名稱為「儷緻」」. ⚠ 다른 표기: CosMax 「Dysport® 麗舒妥」 · COSMED 「Dysport（儷致）」 · Go Young 글 「吉適」(대륙 이름). 5곳은 영문 그대로 |
| ph-065 | 실루엣소프트 | yue | `Silhouette Soft` | **`鈴鐺線`** | `Silhouette Soft` · `鈴鐺埋線` | 현지 글자로 | [beauty101hk.com](https://www.beauty101hk.com/silhouette-soft-%E9%88%B4%E9%90%BA%E7%B7%9A/) · [drreborn.com](https://www.drreborn.com/treatment/lanluma/) · [ysobeauty.com](https://www.ysobeauty.com/%E6%96%B0%E4%B8%80%E4%BB%A3%E5%9F%8B%E7%B7%9A-%E5%B0%87%E4%B8%8B%E5%9E%82%E9%AC%86%E5%BC%9B%E7%9A%84%E7%B5%84%E7%B9%94%E5%BC%B7%E5%8A%9B%E6%8B%89%E6%8F%90-%E4%B8%A6%E6%BF%80%E6%B4%BB%E8%86%A0%E5%8E%9F/) | true | Beauty101 주소 · 제목 「Silhouette Soft 鈴鐺線」 · DR REBORN 「Ellanse、「鈴鐺線」英國廠商Sinclair出品」 · YSO 「Silhouette Soft鈴鐺埋線」 |
| ph-071 | 볼뉴머 | yue | `Volnewmer` | **`黃金樁`** | `Volnewmer` | 현지 글자로 | [drreborn.com](https://www.drreborn.com/treatment/volnewmer/) · [amour-group.com](https://amour-group.com/volnewmer/) · [lovesharebeauty.com](https://lovesharebeauty.com/pages/volnewmer) | true | DR REBORN 메뉴 「Volnewmer 黃金樁療程」 · AMOUR 「VOLNEWMER 黃金樁緊膚」 · Love Share Beauty 「Volnewmer 黃金椿」(椿 으로 적음) |
| ph-072 | 리쥬란아이 | yue | `Rejuran i` | **`麗珠蘭白盒`** | `Rejuran i` | 현지 글자로 | [goyoung.com.hk](https://goyoung.com.hk/news/20240816) · [arum.hk](https://www.arum.hk/products/rejuran-i-white-box-%E9%BA%97%E7%8F%A0%E8%98%AD%E7%99%BD%E7%9B%92) · [initial-plus.com](https://initial-plus.com/rejuran-i-%E9%BA%97%E7%8F%A0%E8%98%AD-%E7%99%BD%E7%9B%92/) · [redefine.com.hk](https://www.redefine.com.hk/rejuran-white) | true | Go Young 「最後系麗珠蘭白盒。佢專注於眼部護理」 · arum.hk 「Rejuran i white box 麗珠蘭白盒」 · Initial Plus 「Rejuran I 麗珠蘭 (白盒)」 · REDEFINE 「REJURAN 白盒麗珠蘭水光針 眼部專…」. ⚠ 상자 색으로 갈래를 가르는 표기 — 색 별명으로 볼지 정할 것(zh 는 처분 ④ 로 「丽驻兰白盒」 을 name 으로 씀) |
| ph-075 | 리쥬란 힐러 | yue | `Rejuran Healer` | **`麗珠蘭黑盒`** | `Rejuran Healer` | 현지 글자로 | [goyoung.com.hk](https://goyoung.com.hk/news/20240816) · [drreborn.com](https://www.drreborn.com/treatment/13treatments/) | true | Go Young 「首先嚟睇麗珠蘭黑盒 … 專為需要綜合抗衰老同保濕」 · DR REBORN 「黑盒: 20mg/ml 藍盒：10mg/ml 白盒：10mg/ml Rejuran麗珠蘭」. ⚠ 상자 색 표기(ph-072 와 같음) |
| ph-079 | 리쥬란 HB+ | yue | `Rejuran HB+` | **`麗珠蘭紅盒`** | `Rejuran HB+` · `Rejuran HB` | 현지 글자로 | [goyoung.com.hk](https://goyoung.com.hk/news/20240816) · [rootologyhk.com](https://rootologyhk.com/product/rejuran-hb/) · [redefine.com.hk](https://www.redefine.com.hk/rejuranred) · [kairosskin.com](https://www.kairosskin.com/b32/) | true | Go Young 「麗珠蘭紅盒 … 顯著降低痛感」 · Rootology 「REJURAN HB 麗珠蘭紅盒」 · REDEFINE 「REJURAN 紅盒麗珠蘭水光針」 · Kairos 「Rejuran HB 麗珠蘭紅盒水光針」. ⚠ 상자 색 표기(ph-072 와 같음) |
| ph-081 | PN | yue | `PN` | **`多核苷酸`** | `PN` | 일반어 | [drreborn.com](https://www.drreborn.com/) · [goyoung.com.hk](https://goyoung.com.hk/news/20240816) · [mioggi.com](https://www.mioggi.com/) · [cosmed.hk](https://cosmed.hk/) | true | 홍콩 4곳(DR REBORN · Go Young · MÍOGGÍ · COSMED) 본문에 「多核苷酸」 — 「PN 多核苷酸」 · 「核心成分系多核苷酸」 |
| ph-108 | 쥬베룩 | yue | `Juvelook` | **`素顏針`** | `Juvelook` | 현지 글자로 | [goyoung.com.hk](https://goyoung.com.hk/) · [mioggi.com](https://www.mioggi.com/zh-hant/product/detail/1217246) · [trinitymedical.com.hk](https://trinitymedical.com.hk/zh/product/juvelook/) | true | Go Young 「Juvelook 素顏針」 · MÍOGGÍ 메뉴 「JUVELOOK® 素顏針」 · Trinity Medical 「Juvelook 素顏針」. ⚠ 「~針」 꼴 시장 이름 — 별명으로 볼지 정할 것. Perfect Medical 은 「素顏針」 을 다른 제품에 쓴다(R1). DR REBORN 은 영문 + 자기 상품명 |
| ph-111 | 래디어스 | yue | `Radiesse` | **`美肌針`** | `Radiesse` · `微晶瓷` · `再生針` | 현지 글자로 | [cosmed.hk](https://cosmed.hk/) · [goyoung.com.hk](https://goyoung.com.hk/) · [radiesse.com.hk](https://www.radiesse.com.hk/radiesse-treatment/) · [lumino.com.hk](https://lumino.com.hk/radiesse/) | true | COSMED 메뉴 「RADIESSE 美肌針」(181쪽) · Go Young 「Radiesse 美肌針」. 다른 표기: 「微晶瓷」(Go Young · Perfect Medical) · 「再生針」(radiesse.com.hk) · 「芮得怡 / 瑞得喜」(Lumino). ⚠ 「~針」 꼴 시장 이름 |
| ph-113 | 쥬베룩볼륨 | yue | `Juvelook Volume` | **`塑顏針`** | `Juvelook Volume` | 현지 글자로 | [goyoung.com.hk](https://goyoung.com.hk/) · [redefine.com.hk](https://www.redefine.com.hk/juvelookvolume) · [d-skin.com.hk](https://www.d-skin.com.hk/juvelookvolume) · [mioggi.com](https://www.mioggi.com/) | true | Go Young 「JUVELOOK Volume 塑顏針」 · REDEFINE 「Juvelook Volume® 塑顏…」 · D-Skin 「Juvelook Volume 塑顏針」 · MÍOGGÍ. ⚠ 「~針」 꼴 시장 이름(ph-108 과 같음) |
| ph-122 | 인모드 | yue | `InMode` | **`鑽石超塑`** | `InMode` | 현지 글자로 | [agbeauty.com.hk](https://www.agbeauty.com.hk/inmodeformai) · [lmskincentre.com](https://lmskincentre.com/tc/%E6%B2%BB%E7%99%82%E8%88%87%E7%94%A2%E5%93%81/%E9%86%AB%E5%AD%B8%E7%BE%8E%E5%AE%B9/inmode-lift%E9%91%BD%E7%9F%B3%E8%B6%85%E5%A1%91-forma-%E5%8F%8A-minifx-%E7%9A%AE%E8%86%9A%E7%B7%8A%E7%B7%BB%E5%8F%8A%E8%84%82%E8%82%AA%E6%B8%9B%E5%B0%91%E7%9A%84%E5%B0%84%E9%A0%BB%E6%B2%BB%E7%99%82/) · [medskinplus.com](https://medskinplus.com/inmode-guide-information/) | true | AG Beauty 「鑽石超塑眼部逆齡棒 Inmode Forma-I」 · LM Skin Centre 「Inmode Lift鑽石超塑」 · MedSkin+ 「INMODE 鑽石超塑」. R1 의 홍콩 8곳 본문에는 InMode 0건 — 검색 결과 제목 · 발췌로 확인 |
| ph-123 | 올리지오 | yue | `Oligio` | **`原美電波`** | `Oligio` · `Oligio X` | 현지 글자로 | [psmedical.com.hk](https://www.psmedical.com.hk/) · [hadahana.hk](https://hadahana.hk/zh-hant/hada-hana-%E8%AD%B7%E7%90%86%E7%99%82%E7%A8%8B/oligio-x-%E5%8E%9F%E7%BE%8E%E9%9B%BB%E6%B3%A2%E5%8D%87%E7%B4%9A%E7%89%88/) · [empathy.com.hk](https://www.empathy.com.hk/oligiox) | true | Perfect Medical 메뉴 「Oligio X 原美電波」 · Hada Hana 「Oligio X 原美電波升級版」 · Empathy 「Oligio X 原美電波｜Oligio X 香港」. 세 곳 모두 신형 Oligio X 에 붙인 이름 |
| ph-126 | 슈링크유니버스 | yue | `Ultraformer MPT` | **`鋼筋索`** | `Ultraformer MPT` · `Shurink Universe` | 현지 글자로 | [drreborn.com](https://www.drreborn.com/) · [surrface.com.hk](https://surrface.com.hk/) · [mydearbeauty.hk](https://mydearbeauty.hk/pages/%E6%9C%80%E6%96%B0%E7%AC%AC4%E4%BB%A3ultraformer-mpt-%E9%8B%BC%E7%AD%8B%E7%B4%A2) · [allbeautymedical.hk](https://www.allbeautymedical.hk/ultraformer-mpt-%E9%8B%BC%E7%AD%8B%E7%B4%A2) · [psmedical.com.hk](https://www.psmedical.com.hk/) | true | DR REBORN 메뉴 「Ultraformer MPT 鋼筋索療程」 · SurrFACE 「第4代Ultraformer MPT 鋼筋索療程」 · Dear Beauty · All Beauty Medical 「鋼筋索 Ultraformer MPT」 · Perfect Medical 「鋼筋索採用第四代…」. 홍콩 시장 이름(지금 별칭) |
| ph-132 | LDM | yue | `LDM-MED` | **`LDM水滴提升`** | `LDM-MED` · `LDM` | 현지 글자로 | [ibeauty.com.hk](https://ibeauty.com.hk/zh-hk/article-inner/?article_id=22092) · [ibeauty.com.hk](https://ibeauty.com.hk/zh-hk/article-inner/?article_id=16779) | false | iBeauty(홍콩) 「LDM® Noblesse水滴提升療程」 1곳(글 2건). 영문 약어 + 한자 꼴(대만 시드 「LDM水滴拉提」 와 같은 짜임). 홍콩 8곳 본문 「LDM」 0건 |
| ph-157 | PRP (혈소판풍부혈장) | yue | `PRP` | **`富血小板血漿`** | `PRP` · `高濃度血小板血漿` | 일반어 | [kneepain.com.hk](https://www.kneepain.com.hk/zh-hk/platelet-rich-plasma-prp/) · [ortho.luxliving.hk](https://ortho.luxliving.hk/%E5%AF%8C%E8%A1%80%E5%B0%8F%E6%9D%BF%E8%A1%80%E6%BC%BF%E6%B2%BB%E7%99%82/) · [yansgroup.com.hk](https://yansgroup.com.hk/prp%E9%AB%98%E6%BF%83%E5%BA%A6%E8%A1%80%E5%B0%8F%E6%9D%BF%E8%A1%80%E6%BC%BF%E6%B2%BB%E7%99%82/) | false | 홍콩 통증 · 정형 클리닉 2곳 「富血小板血漿(PRP)」 · 仁恩 「PRP高濃度血小板血漿治療」 — ⚠ 미용 클리닉이 아니라 reviewed false. 미용 쪽(Perfect Medical 「PRP生髮針」 · Go Young)은 영문 약어 그대로 |
| kr-003 | 엑시온 | yue | `EXION` | **`膠原槍`** | `EXION` · `BTL Exion` | 현지 글자로 | [surrface.com.hk](https://surrface.com.hk/%e7%ac%ac5%e4%bb%a3btl-exion%e6%a5%b5%e7%b7%bb%e9%80%86%e9%bd%a1%e8%86%a0%e5%8e%9f%e7%b7%8a%e7%b7%bb/) · [lmskincentre.com](https://lmskincentre.com/tc/%E9%86%AB%E5%AD%B8%E7%BE%8E%E5%AE%B9/btl-exion-%E7%AC%AC%E4%BA%94%E4%BB%A3%E8%86%A0%E5%8E%9F%E6%A7%8D/) · [peko.com.hk](https://www.peko.com.hk/treatments/btl-exion/) | true | SurrFACE 쪽 제목 「BTL Exion 膠原槍」 · LM Skin Centre 「BTL Exion 第五代膠原槍」 · PEKO 「BTL Exion 膠原槍」. ⚠ 「膠原槍」 은 BTL 계열(앞 세대 Exilis 포함)에 두루 쓰는 이름 — Perfect Medical 은 「BTL Exilis Ultra 360 眼袋槍 / BTL Exion 眼袋槍」 으로 적는다. EXION 만 가리키려면 「第五代膠原槍」 |
| kr-004 | 덴서티 | yue | `DENSITY` | **`無雙電波`** | `DENSITY` | 현지 글자로 | [mioggi.com](https://www.mioggi.com/) · [miio.hk](https://miio.hk/density-%E7%84%A1%E9%9B%99%E9%9B%BB%E6%B3%A2/) · [medilase.com.hk](https://www.medilase.com.hk/beauty-density.php) | true | MÍOGGÍ 메뉴 「DENSITY 無雙電波」(48쪽) · MIIO 「無雙電波 DENSITY」 · MEDILASE 쪽 제목 「DENSITY 無雙電波香港」. 지금 별칭 |
| kr-009 | 벨로테로 리바이브 | yue | `Belotero Revive` | **`保柔緹Revive`** | `Belotero Revive` | 현지 글자로 | [goyoung.com.hk](https://goyoung.com.hk/news/20240904) | false | Go Young 「保柔緹 REVIVE 水光針」 1곳 — 브랜드만 한자(갈래 Revive 는 영문). 다른 곳은 영문 「Belotero® Revive水光針」(MÍOGGÍ · REDEFINE). COSMED 메뉴는 Belotero 를 「彩虹針」 이라 함(R1) — 갈래를 가르지 않음 |
| kr-011 | 하이드라페이셜 | yue | `HydraFacial` | **`海菲秀`** | `HydraFacial` | 현지 글자로 | [surrface.com.hk](https://surrface.com.hk/) · [cosmed.hk](https://cosmed.hk/) | true | SurrFACE 메뉴 「尊貴海菲秀水潤療程」(67쪽) · 「HydraFacial 海菲秀認可醫美中心證書」 · COSMED 「海菲秀 HydraFacial 係一種結合…」 |

## 표 B — 영문 그대로 (98칸)

### 별명뿐 (3)

| id | ko | 언어 | name(그대로) | 출처 · 확인한 곳 | 메모 |
|---|---|---|---|---|---|
| ph-027 | 나보타 | zh | `Nabota` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Nabota) · [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=%E7%BB%BF%E6%AF%92) | 「绿毒」 은 색 별명 — 이름 아님(新氧 제목 0건 · 대륙 6곳 0건). 대륙 허가 · 중문 상품명 근거 못 찾음. 영문 그대로 |
| ph-041 | 메디톡신 | zh | `Meditoxin` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Meditoxin) · [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=%E7%B2%89%E6%AF%92) | 「粉毒」 은 색 별명 — 이름 아님(新氧 제목 0건). 영문 그대로 |
| ph-113 | 쥬베룩볼륨 | zh | `Juvelook Volume` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Juvelook) · [新氧 상품](https://www.soyoung.com/cp11848375) | 新氧 「juvelook黑瓶200mg」(联成益美 1곳) — 영문 브랜드 + 병 색 별명. 지금 별칭 「乔雅露黑瓶丰盈」 0건. 영문 그대로 |

### 일반어 — 현지 이름 못 찾음 (5)

| id | ko | 언어 | name(그대로) | 출처 · 확인한 곳 | 메모 |
|---|---|---|---|---|---|
| ph-080 | PDRN | zh | `PDRN` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=PDRN) · [shmylike.com](http://www.shmylike.com/) | 新氧 상품 제목은 영문 「PDRN」 그대로(「海月兰PDRN水光」 · 「普丽兰PDRN修复水光」) + 별명 「三文鱼」. 성분 풀이 「聚脱氧核糖核苷酸」 은 上海美莱 글 1쪽뿐 — 이름으로 쓰인 근거 아님. 영문 그대로 |
| ph-140 | HIFES/EMS | zh | `HIFES` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=HIFES) | 대륙 6곳 · 新氧 제목 0건. 기술 약어 — 영문 그대로 |
| ph-088 | SVF (자가지방줄기세포) | zh-Hant | `SVF` | [ava-ps.com](https://ava-ps.com/tw/journal/svf-and-prp-autologous-regenerative-care-anatomy/) · [prsa.org.tw](https://www.prsa.org.tw/people/education/content.php?id=290) | 대만 6곳 본문 「SVF」 0건. 검색에서 본 풀이는 「自體脂肪 SVF（血管基質…）」 처럼 영문 약어를 앞세운다 — 정해진 한자 이름 근거 없음. 지금 별칭 「脂肪幹細胞」 은 6곳에서 다른 문맥(피부 세포 설명). 영문 그대로 |
| ph-080 | PDRN | yue | `PDRN` | [beauty101hk.com](https://www.beauty101hk.com/misfill-pdrn/) · [goyoung.com.hk](https://goyoung.com.hk/) | 홍콩 표기는 영문 「PDRN」 + 별명 「三文魚」(Beauty101 「PDRN三文魚水光療程」 · Go Young 「三文魚PDRN」). 한자 성분명은 못 찾음(「多核苷酸」 은 PN). 영문 그대로 |
| ph-140 | HIFES/EMS | yue | `HIFES` | [surrface.com.hk](https://surrface.com.hk/) · [psmedical.com.hk](https://www.psmedical.com.hk/) | 풀이가 곳마다 다르다 — SurrFACE 「HIFES 高能量聚焦磁場」 · Perfect Medical 「HIFES高強度聚焦電磁場技術」. 정해진 이름 없음 — 영문 그대로 |

### 현지 표기 없음 (90)

| id | ko | 언어 | name(그대로) | 출처 · 확인한 곳 | 메모 |
|---|---|---|---|---|---|
| ph-001 | 신펄 | zh | `Synpurl` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Synpurl) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. 별칭 「新珍珠」 제목 일치 0 |
| ph-002 | 채움 | zh | `Chaeum` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Chaeum) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. 별칭 「彩韵」 0 |
| ph-004 | 더채움 | zh | `The Chaeum` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Chaeum) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. 별칭 「彩韵Plus」 0 |
| ph-019 | 레블라이트 | zh | `RevLite` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=RevLite) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. |
| ph-020 | 클라리티2 | zh | `Clarity II` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Clarity) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. |
| ph-023 | 엑셀V | zh | `Excel V` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Excel%20V) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. |
| ph-028 | 뉴럭스 | zh | `NEWLUX` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=NEWLUX) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. 별칭 「纽乐适」 0 · Neurox 0 |
| ph-044 | 타임버스 | zh | `Tyemvers` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Tyemvers) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. 별칭 「时光巴士」 제목 일치 0 |
| ph-060 | 미라클 | zh | `Miracle Thread` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=%E5%A5%87%E8%BF%B9%E7%BA%BF) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. 별칭 「奇迹线」 0 |
| ph-062 | 에버라인 | zh | `Everline` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Everline) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. 별칭 「艾芙莱恩」 제목 일치 0 |
| ph-070 | 벨피엔 | zh | `BelPN` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=BelPN) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. 별칭 「贝尔菲恩」 0 |
| ph-083 | 에스에프 | zh | `SF Injection` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=SF%E6%B3%A8%E5%B0%84) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. 별칭 「SF注射」 제목 일치 0 |
| ph-084 | 큐어스킨 | zh | `CureSkin` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=CureSkin) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. |
| ph-108 | 쥬베룩 | zh | `Juvelook` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Juvelook) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. 新氧 상품 제목은 영문 「juvelook蓝瓶 / 黑瓶」(联成益美 · 深圳妍熙悦). 지금 별칭 「乔雅露」 은 新氧 검색 결과 6건 중 제목 일치 0 — 대륙 클리닉 · 플랫폼 근거 없음 |
| ph-110 | 글로벨라 | zh | `Glovella` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Glovella) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. 별칭 「格洛贝拉」 0 |
| ph-123 | 올리지오 | zh | `Oligio` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Oligio) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. 「欧立吉奥」 0 |
| ph-124 | 더블로골드 | zh | `Doublo Gold` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Doublo) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. 별칭 「多普勒金」 0 |
| ph-126 | 슈링크유니버스 | zh | `Shurink Universe` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Shurink) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. Ultraformer 도 제목 일치 0 |
| ph-132 | LDM | zh | `LDM` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=LDM) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. 「LDM水滴」 · 「水滴提升」 0 |
| ph-134 | 시크릿 | zh | `Secret RF` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Secret) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. 별칭 「Secret黄金微针」 제목 일치 0. 「黄金微针」 은 범주 이름(半岛 · 帝医思 등) |
| ph-135 | 포텐자 | zh | `Potenza` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Potenza) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. |
| ph-136 | 아그네스 | zh | `AGNES` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=AGNES) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. 별칭 「雅格尼斯」 0 |
| ph-149 | 마이셀 | zh | `Mycell` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Mycell) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. 별칭 「玛伊赛尔」 근거 없음 |
| ph-150 | 셀피아 | zh | `Cellpia` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Cellpia) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. 별칭 「赛尔皮亚」 근거 없음 |
| ph-151 | 리젠ACR | zh | `RegenACR` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=RegenACR) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. 별칭 「瑞珍ACR」 0 |
| ph-152 | ACT | zh | `ACT` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=ACT) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. |
| ph-155 | MCT (메타셀) | zh | `MCT` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=MCT) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. |
| kr-003 | 엑시온 | zh | `EXION` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=EXION) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. |
| kr-004 | 덴서티 | zh | `DENSITY` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=DENSITY) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. |
| kr-007 | 프로파일로 | zh | `Profhilo` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Profhilo) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. 新氧 「Profhilo」 · 「普菲洛」 제목 일치 0. 「逆时针」 은 新氧에서 다른 기기(「半岛逆时针（第五代半岛黄金微针）」) — 프로파일로 표기로 쓰면 안 됨. 「普菲洛」 는 海南 허가 보도에 나온 제품명일 뿐 클리닉 · 플랫폼 표기 0 |
| kr-009 | 벨로테로 리바이브 | zh | `Belotero Revive` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Belotero) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. 브랜드 표기 「保柔缇」 는 근거 있음(新氧 「保柔缇BELOTERO · 保柔缇Balance」 다수 · 长沙雅美). 그러나 갈래 Revive 는 新氧 「保柔缇Revive」 제목 일치 0 — 갈래 표기 없음 |
| kr-013 | 텐서(테슬라포머) | zh | `TeslaFormer` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=TeslaFormer) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. |
| kr-015 | 리투오 | zh | `Re2O` | [新氧 검색](https://www.soyoung.com/searchNew/product?keyword=Re2O) | 대륙 6곳 본문 0건 · 新氧 상품 검색 제목 일치 0. |
| ph-001 | 신펄 | zh-Hant | `Synpurl` | — | 대만 6곳 본문 0건 · 검색에서 현지 클리닉 표기 못 찾음. |
| ph-004 | 더채움 | zh-Hant | `The Chaeum` | — | 대만 6곳 본문 0건 · 검색에서 현지 클리닉 표기 못 찾음. |
| ph-030 | 더톡신 | zh-Hant | `Jetema The Toxin` | [tresure-clinic.com](https://tresure-clinic.com/) | 粹究에 영문 「Jetema」 만(「韓國 Jetema 研發」). 검색에서 본 「傑特瑪毒素」 는 판매상 쪽(클리닉 · 플랫폼 아님) — 근거로 치지 않음 |
| ph-040 | 리즈톡스 | zh-Hant | `Liztox` | — | 대만 6곳 본문 0건 · 검색에서 현지 클리닉 표기 못 찾음. 검색에서 본 대만 클리닉 쪽도 영문 「Liztox」 |
| ph-044 | 타임버스 | zh-Hant | `Tyemvers` | — | 대만 6곳 본문 0건 · 검색에서 현지 클리닉 표기 못 찾음. |
| ph-062 | 에버라인 | zh-Hant | `Everline` | — | 대만 6곳 본문 0건 · 검색에서 현지 클리닉 표기 못 찾음. |
| ph-069 | SVF지방이식 | zh-Hant | `SVF` | — | 대만 6곳 본문 「SVF」 0건. 약어를 그대로 쓰는 말 — 한자 이름 근거 없음 |
| ph-070 | 벨피엔 | zh-Hant | `BelPN` | — | 대만 6곳 본문 0건 · 검색에서 현지 클리닉 표기 못 찾음. |
| ph-083 | 에스에프 | zh-Hant | `SF Injection` | — | 대만 6곳 본문 0건 · 검색에서 현지 클리닉 표기 못 찾음. |
| ph-084 | 큐어스킨 | zh-Hant | `CureSkin` | — | 대만 6곳 본문 0건 · 검색에서 현지 클리닉 표기 못 찾음. |
| ph-110 | 글로벨라 | zh-Hant | `Glovella` | — | 대만 6곳 본문 0건 · 검색에서 현지 클리닉 표기 못 찾음. |
| ph-134 | 시크릿 | zh-Hant | `Secret RF` | [dr-shine.com.tw](https://dr-shine.com.tw/) | 대만 6곳 0건. 검색에서 본 표기는 「Secret RF 微針電波」 — 「微針電波」 는 범주 이름(INTRAcel · Potenza 에도 씀) |
| ph-149 | 마이셀 | zh-Hant | `Mycell` | — | 대만 6곳 본문 0건 · 검색에서 현지 클리닉 표기 못 찾음. |
| ph-150 | 셀피아 | zh-Hant | `Cellpia` | — | 대만 6곳 본문 0건 · 검색에서 현지 클리닉 표기 못 찾음. |
| ph-151 | 리젠ACR | zh-Hant | `RegenACR` | — | 대만 6곳 본문 0건 · 검색에서 현지 클리닉 표기 못 찾음. |
| ph-152 | ACT | zh-Hant | `ACT` | — | 대만 6곳 본문 0건 · 검색에서 현지 클리닉 표기 못 찾음. 2 ~ 3자 약어 — 글자 대조 불가(R1 과 같음) |
| ph-155 | MCT (메타셀) | zh-Hant | `MCT` | — | 대만 6곳 본문 0건 · 검색에서 현지 클리닉 표기 못 찾음. 2 ~ 3자 약어 — 글자 대조 불가(R1 과 같음) |
| kr-015 | 리투오 | zh-Hant | `Re2O` | [tresure-clinic.com](https://tresure-clinic.com/collagen-skin-booster/) | 粹究 「Re2O／CellREDM是什麼？… Re2O 不能進口台灣」 — 영문 표기뿐 |
| ph-001 | 신펄 | yue | `Synpurl` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |
| ph-002 | 채움 | yue | `Chaeum` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |
| ph-004 | 더채움 | yue | `The Chaeum` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |
| ph-015 | 프락셀 | yue | `Fraxel` | — | 영문 「Fraxel」 4곳(Pretty Medical 「Fraxel 分段激光」 · CosMax · DR REBORN · SurrFACE). 「飛梭」 는 COSMED · Perfect Medical 글에 범주 낱말로만(「飛梭點陣激光」) — Fraxel 상표 표기로 쓴 곳 못 찾음 |
| ph-019 | 레블라이트 | yue | `RevLite` | — | 홍콩 8곳 0건. 검색에서 본 표기는 영문 + 설명(「RevLite SI C10」 · 「Revlite C8納秒激光」) |
| ph-020 | 클라리티2 | yue | `Clarity II` | — | 홍콩 8곳 0건. 검색에서도 영문 「Clarity II」 |
| ph-023 | 엑셀V | yue | `Excel V` | — | 영문 + 설명 — COSMED 「CUTERA EXCEL V+ 退紅激光」 · Le Ciel 「Excel V 血管激光」 · Pretty Medical 「Xeo / Excel V」. 정해진 한자 이름 없음 |
| ph-027 | 나보타 | yue | `Nabota` | — | 홍콩 8곳 0건. 검색에 나온 「娜柏塔」 는 모두 대만 클리닉 |
| ph-028 | 뉴럭스 | yue | `Neurox` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |
| ph-030 | 더톡신 | yue | `The Toxin` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |
| ph-031 | 레티보 | yue | `Letibo` | — | 홍콩 8곳 0건. 검색에 나온 「保提拉」 는 모두 대만 클리닉 |
| ph-040 | 리즈톡스 | yue | `Liztox` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |
| ph-041 | 메디톡신 | yue | `Meditoxin` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |
| ph-042 | 보툴렉스 | yue | `Botulax` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |
| ph-044 | 타임버스 | yue | `Timbus` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |
| ph-060 | 미라클 | yue | `Miracle Thread` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |
| ph-062 | 에버라인 | yue | `Everline` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |
| ph-063 | 민트리프트 | yue | `MINT Lift` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. 검색에 나온 「秘特線」 은 대만 클리닉 |
| ph-064 | 테스리프트 | yue | `TESSLIFT` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |
| ph-070 | 벨피엔 | yue | `Belpien` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |
| ph-083 | 에스에프 | yue | `SF Injection` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |
| ph-084 | 큐어스킨 | yue | `CureSkin` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |
| ph-110 | 글로벨라 | yue | `Glovella` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |
| ph-124 | 더블로골드 | yue | `Doublo Gold` | — | COSMED 글에 영문 「Doublo」 1쪽. 검색에서 본 표기는 영문 + 설명(「DOUBLO 聚焦超聲波 HIFU」) |
| ph-134 | 시크릿 | yue | `Secret RF` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. 검색에서 본 표기는 영문 + 설명(「Secret RF 微針射頻」) |
| ph-135 | 포텐자 | yue | `Potenza` | — | SurrFACE 글에 영문 「Potenza」. 검색: MIIO 「POTENZA 黃金射頻微針」 · potenza.hk 영문 — 설명어뿐 |
| ph-136 | 아그네스 | yue | `AGNES` | — | Pretty Medical(R1 보조) 「AGNES 絶緣射頻」 — 영문 + 기술 설명 |
| ph-137 | 인트라셀 | yue | `INTRACELL` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |
| ph-149 | 마이셀 | yue | `Mycell` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |
| ph-150 | 셀피아 | yue | `Cellpia` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |
| ph-151 | 리젠ACR | yue | `RegenACR` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |
| ph-152 | ACT | yue | `ACT` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. 2 ~ 3자 약어 — 글자 대조 불가 |
| ph-153 | ASCEplus | yue | `ASCE+` | — | Go Young 「ASCE Plus HRLV 外泌體髮再生精華」 — 영문 브랜드 + 범주어(外泌體) |
| ph-154 | EXOSOME SKIN | yue | `ExoSCRT` | — | Go Young 글에 영문 「ExoSCRT」(기술 이름) 1쪽 |
| ph-155 | MCT (메타셀) | yue | `MCT` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. 2 ~ 3자 약어 — 글자 대조 불가 |
| kr-001 | 써마지 CPT | yue | `Thermage CPT` | — | Pretty Medical(보조) 메뉴 「Thermage CPT 電波拉皮」 · 공식 thermage.hk 「Thermage CPT」 — 갈래는 영문. 맨 이름 「熱瑪吉」 는 4곳(R1 정할 것 1) · 「熱瑪吉CPT」 글자는 0건 |
| kr-012 | 미라드라이 | yue | `miraDry` | — | 홍콩 8곳 0건. 검색에서 본 표기는 영문 + 설명(JOY MED 「miraDry微波止汗」 · 「miraDry 無創微波腋下止汗療程」). 대만 이름 「清新微波」 는 홍콩에서 못 찾음 |
| kr-013 | 텐서(테슬라포머) | yue | `TeslaFormer` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |
| kr-015 | 리투오 | yue | `Re2O` | — | 홍콩 8곳 본문 0건 · 검색에서 현지 표기 못 찾음. |

## 정할 것 (코디 · 사용자가 처분 — 결정하지 않음)

1. **상자 색으로 갈래를 가르는 표기** — yue `麗珠蘭白盒`(아이) · `麗珠蘭黑盒`(힐러) · `麗珠蘭紅盒`(HB+). 홍콩 클리닉 · 판매처가 상품 이름으로 쓰지만(4곳 · 2곳 · 4곳) 브리프는 「색 별명은 이름이 아니다」 라고 한다. zh 는 처분 ④ 로 이미 `丽驻兰白盒` 류를 name 으로 쓰고 있다 — yue 도 같은 처리로 할지, 색 별명으로 보고 영문(`Rejuran i` 류)에 둘지. 안 쓰면 yue 세 칸은 브랜드 표기 `麗珠蘭` 으로 겹친다(대만과 같은 문제)
2. **「~針」 꼴 시장 이름** — yue `素顏針`(쥬베룩) · `塑顏針`(쥬베룩볼륨) · `美肌針`(래디어스). 홍콩에서 메뉴 이름으로 굳은 말이지만 효능을 딴 통칭이다(R1 이 낸 `少女針` · `童顏針` 과 같은 갈래). `素顏針` 은 Perfect Medical 이 다른 제품에 쓴다. 이름으로 칠지 별명으로 볼지
3. **표기가 둘로 갈리는 칸**
   - yue Dysport: `儷緻`(2곳 · 「中文名稱為儷緻」) vs `麗舒妥`(CosMax) vs `儷致`(COSMED). 제안은 `儷緻`
   - zh-Hant PDRN: `聚去氧核苷酸`(粹究) vs `多聚脫氧核苷酸`(映玥) — 1곳씩. 두 곳 모두 영문 PDRN 을 앞세운다. 영문 그대로 두는 길도 있다
   - zh INTRAcel: `帝医思黄金微针` vs `再希思黄金微针` — 둘 다 新氧에 여러 기관. 제조사 표기가 둘이다
4. **한 낱말이 여러 기기를 가리키는 칸** — yue `蜂巢皮秒激光`(PicoSure 외 PICO Laser · enLIGHTen 에도) · yue `膠原槍`(BTL Exilis 계열에도 · EXION 만이면 `第五代膠原槍`) · yue `原美電波`(세 곳 모두 신형 Oligio X). name 으로 올릴지, 별칭으로만 둘지
5. **영문 + 한자 섞인 꼴** — yue `LDM水滴提升` · `保柔緹Revive`, zh `热玛吉四代` 는 통째 한자지만 zh-Hant `精準電波`(AGNES)는 클리닉이 영문 뒤에 붙인 말 1곳. 섞인 꼴을 「그 나라 글자」 로 칠지(대만 시드는 이미 `LDM水滴拉提` · `TESS線` 을 쓴다)
6. **영문 상표 + 기술 설명만 있는 칸** — 「현지 표기 없음」 으로 둔 칸 가운데 홍콩 · 대만 클리닉이 설명어를 붙여 쓰는 것: Fraxel(分段激光) · Excel V(退紅激光 / 血管激光) · Potenza(黃金射頻微針) · Secret RF(微針射頻 / 微針電波) · AGNES(絶緣射頻) · miraDry(微波止汗) · Doublo(聚焦超聲波 HIFU) · RevLite(納秒激光). 설명어는 다른 기기와 겹쳐 이름으로 쓰지 않았다 — 결과 페이지에 「현지 표기 없음」 으로 낼지, 설명어를 별칭으로라도 넣을지
7. **맨 이름 「써마지」** — yue · zh 의 kr-001 은 갈래(CPT)를 가르는 표기가 약하다. zh 는 `热玛吉四代` 가 있지만 yue 는 갈래 표기 0건이고 맨 이름 `熱瑪吉` 만 4곳이다(R1 정할 것 1 과 같은 문제 — 아직 열려 있음)
8. **한자 이름이 있는 일반어인데 손님이 영문 약어로 보는 것** — zh PN(`多聚核苷酸` 1곳 · 新氧 상품은 「PN」) · zh PDRN(新氧 상품은 「PDRN」 + 별명 `三文鱼`) · yue PRP(`富血小板血漿` 은 정형 · 통증 클리닉 표기 · 미용 쪽은 「PRP」). 통역 화면에 어느 쪽을 낼지
9. **시드 별칭의 근거 없는 한자 꼴** — 이번에 어디서도 못 찾은 별칭: zh `新珍珠` · `彩韵` · `彩韵Plus` · `纽乐适` · `时光巴士` · `奇迹线` · `艾芙莱恩` · `贝尔菲恩` · `SF注射` · `乔雅露` · `乔雅露黑瓶丰盈` · `格洛贝拉` · `多普勒金` · `Secret黄金微针` · `雅格尼斯` · `英特拉赛尔` · `玛伊赛尔` · `赛尔皮亚` · `瑞珍ACR`, zh-Hant `聚脫氧核苷酸`. D-53(쓰임 없는 별칭 빼기)을 zh 에도 적용할지 — 이 조사 범위(name) 밖이라 목록만 남긴다
10. **yue Xeomin `淨優明`** — 홍콩 1곳(LM Skin Centre)뿐이고 대만 허가명과 같은 글자다. 공식 xeominhk.com 과 4곳은 영문. 올릴지
11. **대륙 플랫폼을 더 볼지** — 新氧 PC 웹 검색만 봤다. 「현지 표기 없음」 33칸은 대륙에 안 팔리는 제품이라 더 봐도 바뀔 가능성은 낮다고 보지만, 앱 · 百科 는 확인하지 못했다

## 검증

- `r4a-zh.json` 행 수 **136** = 대상 목록의 담당 언어 행 수 136(zh 42 · zh-Hant 29 · yue 65) — (id · lang) 빠짐 0 · 남음 0
- 「현지 글자로」(일반어 포함) 38행 모두 출처 1개 이상 — 출처 0인 행 0
- 제안 name 이 같은 언어의 다른 term name · 별칭과 겹치는 것 0(시드 `.8` 대조)
- 사전 · 코드 · 문서 수정 없음. 만든 파일은 `r4a-zh-report.md` · `r4a-zh.json` 둘
