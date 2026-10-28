# 대만 클리닉 사이트 3곳 전수 — 시술명 → 통키 사전(zh-Hant) 대조

**사이트 성격(첫 줄):** ① tresure-clinic.com = 粹究美學診所(대만 타이베이 의원) ② muskin.com.tw = 木木日安(대만 타이베이 피부과 의원, 忠孝復興站) ③ koreabeautydream.com = **韓佳人診所 한가인클리닉 — 한국 측 안내 사이트가 아니라 타이베이 의원**이다(`<html lang="zh-Hant-TW">`, 지점 忠孝店·光復館, 번체 본문 + 한국어 소제목만 장식으로 씀, 원장 陳芳蒂는 「韓籍醫師 · 台北醫學大學醫學系畢業」로 소개, 컨셉이 「韓式醫美」). **세 곳 모두 대만 클리닉 · 번체(台灣)** 이다 → 표의 「출처 성격」 칸은 셋 다 「대만 클리닉」이고, 「한국 측 중문 안내」 출처는 이번 조사에 없다.

- 조사일: 2026-10-27 · researcher(read-only) · 결정하지 않음
- 방법: 각 사이트 Yoast sitemap 으로 URL 전수 → curl 로 원문 HTML 받아 제목·h1~h3·본문에서 문자열 확인(요약 모델을 거치지 않음). tresure 168페이지(portfolio 140 + page 28) + 블로그 5편, muskin page 83, koreabeautydream 치료·소식 페이지 60(이 중 수술 6쪽은 404)
- 사전: `seed-current.json` version `2026-10-27.4`, 157 term
- 약어: **T** = tresure-clinic.com, **M** = muskin.com.tw, **K** = koreabeautydream.com. URL 은 `T:/portfolio-item/botox/` 처럼 줄여 쓴다(도메인 앞에 붙이면 원문)

## 0. 한 줄 결론

1. **사전 톡신 이름 4개가 대만 클리닉 표기와 다르다** — ph-031 레티보 `樂提保`·ph-042 보툴렉스 `白毒`(둘 다 대만에선 `保提拉`), ph-041 메디톡신 `粉毒`(대만 `優力柔`), ph-027 나보타 `綠毒`(대만 `娜柏塔`/`彩虹肉毒`). 별명이 name 자리에 앉아 있다.
2. **사전 표기 중 대륙식이 확인된 것** — ph-026 `下頜線`(T 는 `下顎線`), ph-130 alias `熱瑪吉`(T 가 「中國與港澳星馬」 표기라고 명시), ph-093 `超聲波`(세 곳 모두 `超音波`), ph-096 `離子匯入`(세 곳 모두 `導入`), ph-116 `無細胞同種真皮`(T·K 는 `異體真皮(粉)`), ph-059 `脂肪細胞破壞`(T·K 는 `去氧膽酸`/`倍克脂`).
3. **koreabeautydream 에서 한국 전용 브랜드(신펄·더채움·리쥬란 주사·리즈톡스·코어톡스·나보타)의 중문 표기는 찾지 못했다** — 이 사이트도 대만 허가 품목만 쓴다(톡신은 `Botox保妥適 / Letybo保提拉 / Dysport皇家` 셋뿐). 한국 브랜드 중 대만에 들어온 것만 대만식 이름이 있다(아래 §4).

---

## 1. tresure-clinic.com (粹究美學診所)

### 표 A-T — 사전 term 과 같은 것

| 사이트 표기 | 영문 | 사전 term (ko) | 지금 사전 zh-Hant | 제안 | 출처 성격 | URL |
|---|---|---|---|---|---|---|
| `Botox肉毒(保妥適)` · `經典肉毒` · `美國保妥適` | Botox | ph-033 보톡스 | 肉毒 / [肉毒素, 肉毒桿菌, 肉毒桿菌注射, 保妥適] | alias `經典肉毒` | 대만 클리닉 | T:/portfolio-item/botox/ |
| `Dysport皇家肉毒` · `儷緻注射劑`(허가명) · `舊名"麗舒妥"` | Dysport | ph-039 디스포트 | 儷緻 / [吉適, Dysport] | alias `皇家肉毒` `麗舒妥`. ⚠ `吉適` 은 3 사이트 어디에도 없음(확인 필요) | 대만 클리닉 | T:/portfolio-item/皇家肉毒/ |
| `Xeomin淨優明天使肉毒` | Xeomin | ph-037 제오민 | 淨優明 / [思奧美, Xeomin, 天使肉毒] | 없음(`思奧美` 는 3 사이트에 없음) | 대만 클리닉 | T:/portfolio-item/天使肉毒_xeomin/ |
| `Letybo保提拉肉毒` · `輕齡肉毒` | Letybo(=Botulax 수출명) | ph-031 레티보 · ph-042 보툴렉스 | 樂提保 / [Letibo] · 白毒 / [Botulax] | **name `保提拉`**(두 term 모두) · alias `輕齡肉毒` `白毒`. `樂提保` 는 3 사이트에 없음 | 대만 클리닉 | T:/portfolio-item/保提拉肉毒_letybo/ |
| `Neuronox優力柔 奇蹟肉毒/奇肌肉毒` · `韓國內銷名稱為Meditoxin` | Neuronox(=Meditoxin) | ph-041 메디톡신 | 粉毒 / [Meditoxin] | **name `優力柔`** · alias `Neuronox` `奇蹟肉毒` `奇肌肉毒` `粉毒` | 대만 클리닉 | T:/portfolio-item/neuronox/ · T:/portfolio-item/肉毒緊致/ |
| `NABOTA娜柏塔` · `彩虹肉毒` · `綠毒` (블로그) | Nabota | ph-027 나보타 | 綠毒 / [Nabota] | **name `娜柏塔`** · alias `彩虹肉毒` `綠毒` | 대만 클리닉 | T:/韓國肉毒比較/ (앞 리포트 C5) |
| `肉毒瘦小腿(俗稱瘦腿針)` · `蘿蔔腿` · `小腿肉毒` | Calf | ph-038 종아리 | 小腿 / [瘦小腿, 蘿蔔腿] | alias `瘦腿針` `小腿肉毒` | 대만 클리닉 | T:/portfolio-item/leg-slimming/ |
| `肉毒瘦肩` · `瘦肩針` · `輕盈天使肩` · `上斜方肌` | Trapezius | ph-035 승모근 | 斜方肌 / [瘦肩] | alias `瘦肩針` `肉毒瘦肩` | 대만 클리닉 | T:/portfolio-item/shoulder-slimming/ · T:/btx-facelift/ |
| `瘦小臉（國字臉改善）` · `咀嚼肌肥厚` · `咬肌` | Square Jaw | ph-034 사각턱 | 瘦臉針 / [咬肌, 國字臉, …] | 없음 | 대만 클리닉 | T:/portfolio-item/肉毒緊致/ |
| `抬頭紋、皺眉紋、魚尾紋等動態紋` · `皺眉紋（川字紋）` | Wrinkle | ph-024 주름 | 除皺 / [皺紋, 除皺針, 動態皺紋] | alias `抬頭紋` `皺眉紋` `魚尾紋` 후보 | 대만 클리닉 | T:/portfolio-item/肉毒緊致/ |
| `腋下多汗症` | Hyperhidrosis | ph-029 다한증 | 多汗症 | 없음(근거 확보 → reviewed 후보) | 대만 클리닉 | T:/portfolio-item/肉毒緊致/ · T:/portfolio-item/微波止汗/ |
| `頸紋、脖紋` | Neck Wrinkle | ph-032 목주름 | 頸紋 | alias `脖紋` | 대만 클리닉 | T:/neck-wrinkles/ |
| `嘴角/眉尾上揚` | Lip Corners | ph-036 입꼬리 | 嘴角 | 없음 | 대만 클리닉 | T:/portfolio-item/肉毒緊致/ |
| **`下顎線`**(x96) | Jawline | ph-026 턱선 | **下頜線** | **name `下顎線`**(`下頜` 은 `下頜韌帶` 해부 용어로만 2회) | 대만 클리닉 | T:/jawline/ |
| `玻尿酸` | Filler | ph-003 필러 | 玻尿酸 | 없음 | 대만 클리닉 | T:/portfolio-item/玻尿酸/ |
| `喬雅登玻尿酸` | Juvéderm | ph-005 | 喬雅登 | 없음 | 대만 클리닉 | T:/portfolio-item/喬雅登玻尿酸/ |
| `瑞絲朗／Restylane` | Restylane | ph-006 | 瑞絲朗 / [瑞藍, …] | 없음(`瑞藍` 은 3 사이트에 없음) | 대만 클리닉 | T:/portfolio-item/瑞絲朗/ |
| `Belotero保柔緹 仿生玻尿酸(水無痕玻尿酸)` | Belotero | ph-007 | 保柔緹 | alias `水無痕` `仿生玻尿酸` | 대만 클리닉 | T:/portfolio-item/水無痕玻尿酸/ |
| `洢蓮絲 Ellansé` · `少女針` · `PCL 聚己內酯微型晶球` | Ellansé · PCL | ph-107 · ph-117 | 洢蓮絲 · 聚己內酯 | 없음(ph-117 근거 확보) | 대만 클리닉 | T:/portfolio-item/洢蓮絲/ |
| `晶亮瓷(再生針)Radiesse 瑞得喜/微晶瓷` · `CaHA微晶球` | Radiesse · CaHA | ph-111 · ph-115 | 晶亮瓷 · 羥基磷灰石鈣 | ph-111 alias `微晶瓷` `再生針`. ph-115 중문 화학명은 사이트에 없음(`CaHA` 로만 씀) | 대만 클리닉 | T:/portfolio-item/晶亮瓷/ |
| `童顏針Sculptra` · `4D舒顏萃` · `童妍針` · `聚左旋乳酸（PLLA）` | Sculptra · PLLA | ph-112 · ph-120 | 舒顏萃 / [素顏萃童顏針, Sculptra] · 聚左旋乳酸 | ph-112 alias `童顏針` `童妍針` `4D舒顏萃`. `素顏萃` 은 3 사이트에 없음 | 대만 클리닉 | T:/portfolio-item/sculptra/ |
| `喬雅露 Juvelook` | Juvelook | ph-108 | 喬雅露 | 없음 | 대만 클리닉 | T:/portfolio-item/juvelook/ |
| `AestheFill艾麗斯精靈針 PDLLA聚雙旋乳酸` | PDLLA | ph-118 | 聚雙旋乳酸 | 없음(제품명은 표 B) | 대만 클리닉 | T:/portfolio-item/艾麗斯百變精靈針/ |
| `多核苷酸（PN）` | PN | ph-081 | PN / [聚合核苷酸] | alias `多核苷酸` | 대만 클리닉 | T:/portfolio-item/pinklla/ |
| `Rejuran PDRN Booster` | PDRN | ph-080 | PDRN | 없음 | 대만 클리닉 | T:/portfolio-item/rejuran/ |
| `麗珠蘭修復水光` · `麗珠蘭白瓷水光` — 「台灣目前合法上市的麗珠蘭，是原廠於 2024 年底引進的 Rejuran PDRN Booster 水光系列…兩款都屬於外用導入型產品」 | Rejuran | ph-072 · ph-075 · ph-079 | 麗珠蘭 / [麗珠蘭白盒/黑盒/紅盒, …] | name `麗珠蘭` 은 맞음. **`黑盒/紅盒/白盒` 은 3 사이트에 없음**, 대만 합법품은 외용 Booster 뿐이라 주사제(Healer·HB+·i)의 대만 클리닉 표기는 **없음** | 대만 클리닉 | T:/portfolio-item/rejuran/ |
| `膠原蛋白熊貓針`(双美膚力原) | Collagen | ph-109 | 膠原蛋白 | 없음 | 대만 클리닉 | T:/portfolio-item/膠原蛋白熊貓針/ |
| `外泌體`(ExoCake 訊聯外泌體) | Exosome | ph-082 | 外泌體 | 없음 | 대만 클리닉 | T:/portfolio-item/exocake/ |
| `異體真皮粉` · `MegaDerm異體真皮` · `脫細胞真皮基質（mADM）` · 공지: 「異體真皮粉已停止供應，全面升級為「再生真皮粉」(TISUAPP)」 | hADM | ph-116 무세포동종진피 | **無細胞同種真皮** | **name `異體真皮`** · alias `異體真皮粉` `脫細胞真皮基質`. (대만 공급 중단 공지 있음) | 대만 클리닉 | T:/portfolio-item/filler-megafill/ · T:/portfolio-item/megaderm/ |
| `自體脂肪移植` · `補脂` | Fat Graft | ph-066 | 自體脂肪移植 | 없음 | 대만 클리닉 | T:/portfolio-item/自體脂肪移植/ |
| `脂肪槍 MAFT-GUN（Micro-Autologous Fat Transplantation）` | Micro Fat Grafting | ph-068 마이크로지방이식 | 微脂肪填充 | alias `脂肪槍` `MAFT`. `微脂肪填充` 은 3 사이트에 없음 | 대만 클리닉 | T:/portfolio-item/maft-gun/ |
| `埋線拉提` · `秘特 MINT LIFT` · `鈴鐺線`(俗稱) · `Silhouette Instalift` · `PDO 螺旋倒鉤` | Thread Lift · MINT · Silhouette · PDO | ph-061 · ph-063 · ph-065 · ph-119 | 埋線拉提 · Mint薄荷線 / [秘特線, …] · 鈴鐺線 · PDO線 | ph-063 name `秘特線` 후보(`薄荷` 는 3 사이트에 없음) | 대만 클리닉 | T:/portfolio-item/埋線拉提/ |
| `鳳凰電波Thermage FLX` · 「中國與港澳星馬等地區，也有熱瑪吉等別稱」 | Thermage FLX | ph-130 | 鳳凰電波 / [美版熱瑪吉FLX, …, 熱瑪吉, 美版電波] | **alias `熱瑪吉` `美版熱瑪吉FLX` 는 대만 표기 아님**(사이트가 명시) | 대만 클리닉 | T:/portfolio-item/flx鳳凰電波/ |
| `海芙電波 Volnewmer` | Volnewmer | ph-071 | 海芙電波 / [黃金樁, Volnewmer] | `黃金樁` 은 3 사이트에 없음 | 대만 클리닉 | T:/portfolio-item/volnewmer/ |
| `海芙音波`(Ultraformer III) · 「韓國以「Shurink（슈링크）」名稱銷售」 · `海芙音波第四代「媚必提」`(Ultraformer MPT) · 「韓國同世代機型以「Shurink Universe（슈링크 유니버스，俗稱宇宙版）」名稱銷售」 | Ultraformer MPT = Shurink Universe | ph-126 슈링크유니버스 | 海芙音波 / [Shurink Universe, Shurink, 韓版音波] | **name `海芙音波媚必提`(또는 `媚必提`)** — 사이트 기준 `海芙音波` 는 3세대(Shurink)를 가리킴. alias `Ultraformer MPT` `海芙媚必提`. → 표 C-1 | 대만 클리닉 | T:/portfolio-item/ultraformer/ · T:/portfolio-item/ultraformer-mpt/ |
| `音波拉提` · `HIFU 聚焦原理` | HIFU | ph-131 | 音波拉提 | 없음 | 대만 클리닉 | T:/portfolio-item/ultraformer/ |
| `電波拉提` | RF | ph-133 | 電波拉提 | 없음 | 대만 클리닉 | T:/儀器療程/電波拉提/ |
| `微針電波`(Exion 時空E電波) | Needle RF | ph-141 | 微針電波 | 없음 | 대만 클리닉 | T:/portfolio-item/exion/ |
| 「韓國診所口中的黃金微針，多數指的是 POTENZA 這台儀器，**台灣的中文名稱為無限電波**」 | Potenza | ph-135 포텐자 | 黃金微針 / [無限電波, Potenza] | **name `無限電波`** · `黃金微針` 은 alias 로(한국식 표현이라는 사이트 설명) | 대만 클리닉 | T:/gold-microneedling/ |
| `CODE-X肌活筆（電動微針筆）` · `醫用無線自動微針設備（Automatic MTS）` | Electric MTS | ph-148 전동 MTS | 電動MTS | alias `電動微針筆` `微針筆` | 대만 클리닉 | T:/portfolio-item/code-x/ |
| `微針` · `微針滾輪` | MTS | ph-146 · ph-147 | 微針 / [MTS, 滾針] · 手動MTS | ph-147 alias `微針滾輪` 후보 | 대만 클리닉 | T:/portfolio-item/code-x/ |
| `超能電漿` · `氦氣電漿` · `電漿拉皮`(Renuvion) | Plasma | ph-143 플라즈마 | 電漿 / [等離子] | 없음(`等離子` 는 「等離子體」 물리 용어로 1회) | 대만 클리닉 | T:/portfolio-item/renuvion/ |
| `淨膚雷射 REVLITE V淨化光` | Toning · RevLite | ph-012 · ph-019 | 淨膚雷射 | ph-019 alias `淨化光` | 대만 클리닉 | T:/portfolio-item/淨膚雷射/ |
| `星皮秒雷射 StarWalker` · `皮秒` | Picosecond | ph-022 | 皮秒雷射 | 없음(기기명은 표 B) | 대만 클리닉 | T:/portfolio-item/星皮秒雷射/ |
| `聚焦飛梭雷射｜蜂巢皮秒空泡效應` | PicoSure(Focus) | ph-017 · ph-015 | 蜂巢皮秒 · 飛梭雷射 | → 표 C-8 | 대만 클리닉 | T:/portfolio-item/聚焦飛梭/ |
| `M22彩衝光`(OPT 脈衝光 + ResurFX 飛梭) · `IPL脈衝技術` | IPL | ph-021 | 脈衝光 | 없음 | 대만 클리닉 | T:/portfolio-item/m22彩衝光梭/ |
| `雷射除毛` · `亞歷山大除毛雷射` | Hair Removal | ph-011 | 除毛雷射 | 없음 | 대만 클리닉 | T:/portfolio-item/除毛雷射/ |
| `水光針`(療程統稱) · `水光槍`(以自動化儀器施打) · `水光注射` · `手打` | Skin Booster · Mesogun | ph-074 · ph-090 · ph-089 | 水光針 · 水光槍 / [機打] · 水光 | ph-074 alias `水光注射`. `機打` 는 3 사이트에 없음(사이트는 「手打」 대 「機器」) | 대만 클리닉 | T:/mesotherapy-fail/ · T:/portfolio-item/dermashine/ |
| `煥膚療程` · `杏仁酸` · `MSA胜肽酸` | Chemical Peeling | ph-094 | 果酸換膚 / [刷酸, 化學換膚, 杏仁酸換膚] | alias `煥膚` | 대만 클리닉 | T:/portfolio-item/煥膚療程/ |
| `深層清潔`(Venus Glow 水飛梭) | Deep Cleansing | ph-091 딥클렌징 | 深層清潔 | 없음(근거 확보 → reviewed 후보) | 대만 클리닉 | T:/portfolio-item/新一代水飛梭/ |
| `保濕導入` · `超音波導入` · 「醫美專業等級的保濕導入是以超音波震動與升溫輔助」 | Ultrasound Care · Iontophoresis | ph-093 · ph-096 | 超聲波護理 · **離子匯入** | ph-093 → `超音波導入` 후보 · ph-096 → `導入`(또는 `離子導入`). `匯入`·`超聲波` 는 3 사이트에 없음 | 대만 클리닉 | T:/portfolio-item/保濕/ |
| `輸液點滴` | IV Therapy | ph-055 | 點滴 / [輸液療法, 營養點滴, 靜脈注射] | alias `輸液點滴` | 대만 클리닉 | T:/portfolio-item/輸液點滴/ |
| `消脂針`(x127) · `溶脂針`(x4) | Fat Dissolving Injection | ph-058 | 溶脂針 | alias `消脂針` | 대만 클리닉 | T:/portfolio-item/消脂針/ |
| `倍克脂Belkyra (美國銷售名稱為Kybella)` · `去氧膽酸(deoxycholic acid)` · `DCA` | DCA | ph-059 | **脂肪細胞破壞** | **name `去氧膽酸`** · alias `DCA` `倍克脂`. `脂肪細胞破壞` 는 3 사이트에 없음 | 대만 클리닉 | T:/portfolio-item/belkyra/ |
| `菲斯波 EMFACE` · `高強度電場技術（HIFES™）` · `同步電波` | HIFES / Facial EMS | ph-140 · ph-138 | HIFES · 面部EMS | ph-140 alias `菲斯波` 후보. `EMS` 는 T 에 없음 | 대만 클리닉 | T:/portfolio-item/emface/ |
| `美肌動力光`(各種不同顏色、不同波長的光線) | LED | ph-104 | 光療 / [LED] | → 표 C-12 | 대만 클리닉 | T:/portfolio-item/美肌動力光/ |
| `清新微波 miraDry`(腋下多汗) | Microwave | ph-125 | 微波治療 | → 표 C-9 | 대만 클리닉 | T:/portfolio-item/微波止汗/ |

### 표 B-T — 사전에 없는 시술·제품(새 후보)

| 사이트 표기 | 영문 | 가까운 term | URL |
|---|---|---|---|
| `仙女玻尿酸` — 「正式名稱是 Neuramis，由韓國 Medytox 生產」, 허가 衛部醫器輸字第033914·037033號 | Neuramis(**한국 필러**) | ph-003 계열 | T:/portfolio-item/neuramis/ |
| `Profhilo 逆時針 (璞菲洛)` · `液態電波` | Profhilo | ph-074 | T:/portfolio-item/profhilo/ |
| `素妍針` — `Belotero Revive` 장기 보습 | Belotero Revive | ph-007 · ph-074 | T:/portfolio-item/revive/ |
| `索夫波 Sofwave` | Sofwave | ph-128 | T:/portfolio-item/sofwave/ |
| `CPT黃金電波`(Thermage CPT) | Thermage CPT | ph-130 → 표 C-2 | T:/portfolio-item/cpt黃金電波/ |
| `鳳凰光`(Clear+Brilliant Touch) | Clear+Brilliant | — → 표 C-2 | T:/portfolio-item/cbt/ |
| `時空E電波 Exion` | Exion | ph-141 | T:/portfolio-item/exion/ |
| `泡泡電波`(Tripollar) · `4D黃金馬甲電波` | — | ph-133 | T:/portfolio-item/泡泡電波/ · T:/portfolio-item/黃金馬甲/ |
| `音波水光`(海芙媚必提) · `疼就酷 Targetcool冰晶水光` · `德瑪莎肌膚之光 Dermashine` | — | ph-074 · ph-090 · ph-092 | T:/portfolio-item/ultra-booster/ · /targetcool/ · /dermashine/ |
| `熊貓光`(星皮秒＋M22) · `日式光纖` · `靜脈雷射/氦氖雷射 ILIB` · `G緊雷射` | — | ph-014 | T:/portfolio-item/eye-laser/ · /日式光纖/ · /靜脈雷射/ · /g緊雷射/ |
| `水飛梭 Venus Glow` · `海飛秀`(Hydrafacial) · `親氧水美肌` · `LPG臉部蜜提` | — | ph-091 | T:/portfolio-item/新一代水飛梭/ · /親氧水美肌/ · /lpg臉部蜜提/ |
| `白金熊貓針 膚漾美`(Deusaderm Ultra) | — | ph-109 | T:/portfolio-item/deusaderm-ultra/ |
| `PiNkLLA粉光瓶`(PLLA×PN) · `aesPlla艾莉雅 原生曙光瓶`(PLLA) | — | ph-120 · ph-081 | T:/portfolio-item/pinklla/ · /aesplla/ |
| `艾麗斯精靈針 AestheFill` | AestheFill | ph-118 | T:/portfolio-item/艾麗斯百變精靈針/ |
| `再生真皮粉 TISUAPP（鐵愛）` | TISUAPP | ph-116 | T:/portfolio-item/tisuapp/ |
| 필러 브랜드: `Vivacy維法熙魔V針` · `Teoxane緹奧希` · `ANiMERS愛霓密絲` · `海德密絲 Hya-Dermis` · `Princess公主玻尿酸` · `氧氣玻尿酸 MissStunnin 絲登齡` | — | ph-003 | T:/微整美學/各式玻尿酸/ |
| `美肌拉提斯 MagiLates`(Dysport 全臉肉毒拉提) · `英倫大提升` | — | ph-046 · ph-049 → 표 C-13 | T:/portfolio-item/magilates/ |
| `Ronkyla容脂溶脂針` · `消脂點滴(肝得健+卡尼丁)` | — | ph-058 | T:/portfolio-item/ronkyla/ · /消脂點滴/ |
| `標靶震波減脂 UltraShape` · `超音波聚焦減脂` · `TeslaFormer易力肌塑 磁雕` · `音浪脂雕 LSSA` · `黃金Z波溶脂` | — | ph-139(일부) | T:/portfolio-item/標靶震波減脂/ · /teslaformer/ · /lssa/ · /z波溶脂/ |
| 감량 약: `猛健樂 Mounjaro` · `善纖達 Saxenda` · `週纖達 Wegovy` · `康纖芙 Contrave` | — | — | T:/portfolio-item/mounjaro/ · /善纖達…/ · /wegovy/ · /contrave/ |
| 여성: `薇薇電波 Viveve` · `閨蜜電波 Emfemme` · `寵愛椅 TESLAChair` | — | — | T:/儀器療程/私密護理/ |
| 시술성 미용: `三明治眼袋微整術` · `槍托式下巴` · `貴族法令微整術` | — | — | T:/portfolio-item/三明治眼袋隱形術/ · /gunstock-jawline/ · /nasal-folds/ |
| 수술(사전에 수술 카테고리 없음): `隱痕眼袋手術` `韓式無痕雙眼皮` `開眼頭/開眼尾` `深層拉皮` `微創拉皮` `天鵝頸手術` `韓系小喵鼻` `腹部拉皮` `提乳手術` `男性女乳症` `頂漿腺(狐臭)手術`, 가슴 보형물 `Mentor曼陀` `Motiva魔滴` `Luna璐娜` `Sebbin柔滴` `珍珠波` `MESMO繆思女神波` | — | — | T:/整形外科/… |
| `VISIA肌膚檢測` | — | — | T:/portfolio-item/肌膚檢測儀/ |

---

## 2. muskin.com.tw (木木日安 · 피부과)

가격표(`M:/price/`)의 시술명: 皮秒雷射 · 皮秒真皮層透鏡 · 皮秒雙透鏡 · 皮秒單點 · 染料雷射 · 光纖雷射 · 清新光雷射 · 醫療級果酸 · 清痘 · 聲波導入 · 水飛梭渦流清潔 · MESOJET 導入 · 除毛雷射 · 鉺雅鉻雷射換膚 · 贅生物 · UP雷射換膚 · 皮下剝離手術 · FLX鳳凰電波 · 海芙音波媚必提 · `Botox 肉毒桿菌` · 玻尿酸 · `Sculptra 舒顏萃` · `Juvelook 喬雅露` · `Aesthefill 艾麗斯` · `Profhilo 逆時針` · 白皙微針

### 표 A-M — 사전 term 과 같은 것

| 사이트 표기 | 영문 | 사전 term | 지금 사전 zh-Hant | 제안 | 출처 성격 | URL |
|---|---|---|---|---|---|---|
| `保妥適BOTOX` · `肉毒桿菌` | Botox | ph-033 | 肉毒 | 없음 | 대만 클리닉 | M:/botox/ |
| `Letybo保提拉肉毒桿菌` | Letybo | ph-031 · ph-042 | 樂提保 · 白毒 | name `保提拉`(표 A-T 와 같음) | 대만 클리닉 | M:/letybo/ |
| `國字臉` · `咀嚼肌` · `瘦小臉` | Square Jaw | ph-034 | 瘦臉針 | 없음 | 대만 클리닉 | M:/botox/ |
| `模特兒平肩美型` · `上斜方肌` | Trapezius | ph-035 | 斜方肌 | 없음 | 대만 클리닉 | M:/botox/ |
| `瘦小腿，小腿肚肌肉拉展` | Calf | ph-038 | 小腿 | 없음 | 대만 클리닉 | M:/botox/ |
| `抬頭紋` · `魚尾紋` · `木偶紋` | Wrinkle | ph-024 | 除皺 | alias 후보(표 A-T 와 같음) | 대만 클리닉 | M:/botox/ |
| `Juvelook喬雅露（新童妍）` · `Lenisna`(大分子) | Juvelook · Juvelook Volume | ph-108 · ph-113 | 喬雅露 | ph-108 alias `新童妍` → 표 C-5 | 대만 클리닉 | M:/juvelook/ |
| `Sculptra 4D／聚左旋乳酸／舒顏萃` | Sculptra | ph-112 | 舒顏萃 | 없음 | 대만 클리닉 | M:/sculptra/ · M:/aesthefill/ |
| `ELLANSE／洢蓮絲／少女針` | Ellansé | ph-107 | 洢蓮絲 | 없음 | 대만 클리닉 | M:/aesthefill/ |
| `AestheFill／艾麗斯聚雙旋乳酸／精靈針` | PDLLA | ph-118 | 聚雙旋乳酸 | 없음 | 대만 클리닉 | M:/aesthefill/ |
| `目前市面上合法的膠原蛋白增生劑有` | Biostimulator | ph-114 | 膠原蛋白增生劑 | 없음(근거 확보) | 대만 클리닉 | M:/aesthefill/ |
| `Ulthera音波拉皮` · `音波拉提` · `極線音波拉皮` | Ulthera | ph-121 | 美國音波 / [美版超聲刀, …, 極線音波, 美版音波, 音波拉提] | alias `音波拉皮`. `超聲刀` 는 3 사이트에 없음 | 대만 클리닉 | M:/ulthera/ |
| `Ultraformer 海芙音波` · `海芙音波媚必提` | Ultraformer | ph-126 | 海芙音波 | 표 C-1 | 대만 클리닉 | M:/ultraformer/ |
| `鳳凰電波` · `電波拉皮` | Thermage FLX · RF | ph-130 · ph-133 | 鳳凰電波 · 電波拉提 / [射頻, RF, 電波, 電波拉皮] | 없음 | 대만 클리닉 | M:/thermage_flx/ |
| `黃金電波 Thermage CPT` | Thermage CPT | ph-130 | — | 표 C-2 | 대만 클리닉 | M:/thermage_cpt/ |
| `皮秒雷射` · `探索皮秒 Discovery Pico` | Picosecond | ph-022 | 皮秒雷射 | 없음 | 대만 클리닉 | M:/discoverypico/ |
| `Vbeam 染料雷射` | Vascular | ph-013 | 血管雷射 / [染料雷射] | 없음 | 대만 클리닉 | M:/vbeam-prima/ |
| `鉺雅鉻雷射飛梭`(汽化雷射) · `UP雷射`(UltraPulse, CO2 升級版) | Fractional | ph-016 · ph-015 | 飛梭雷射 | 기기명은 표 B | 대만 클리닉 | M:/eryag_laser/ · M:/ultrapulse/ |
| `亞歷山大光纖雷射除毛` · `日式光纖雷射：除毛/美白/淡斑` | Hair Removal | ph-011 | 除毛雷射 | 표 C-14 | 대만 클리닉 | M:/laser_hair_removal/ · M:/gentlelaser-light/ |
| `醫療級果酸` · `果酸換膚術` · `杏仁酸` | Chemical Peeling | ph-094 | 果酸換膚 | 없음 | 대만 클리닉 | M:/acid_peels/ · M:/price/ |
| `醫療級清痘` | Acne | ph-098 여드름 전용 | 痘痘專用 | alias `清痘` · `痘痘專用` 은 3 사이트에 없음 | 대만 클리닉 | M:/acnes/ |
| `痘疤特別門診` · `凹洞疤痕` | Scar | ph-100 흉터 전용 | 疤痕專用 | alias `痘疤` · `疤痕專用` 은 3 사이트에 없음 | 대만 클리닉 | M:/scar-sr/ |
| `聲波導入` · `MESOJET 導入` | Iontophoresis · Injection Equipment | ph-096 · ph-092 | 離子匯入 · 匯入裝置 | `導入` 계열(표 A-T 와 같음) | 대만 클리닉 | M:/price/ |
| `水飛梭渦流清潔` | Deep Cleansing | ph-091 | 深層清潔 | alias `水飛梭` 후보 | 대만 클리닉 | M:/price/ |
| `白皙微針注射`(傳明酸＋維他命C) | Whitening | ph-052 | 美白點滴 / […, 美白導入] | 표 C-15 | 대만 클리닉 | M:/vitamin/ |
| `皮膚管理`(青春痘酒糟肌專屬…皮膚管理) | Medical Skincare | ph-095 | 皮膚管理 | 없음(근거 확보) | 대만 클리닉 | M:/price/ |

### 표 B-M — 새 후보

| 사이트 표기 | 영문 | URL |
|---|---|---|
| `Profhilo 逆時針` | Profhilo | M:/profhilo/ |
| `Neobeam 清新光（全新光）` | Neobeam | M:/neobeam/ |
| `皮下剝離` (Subcision) | Subcision | M:/subcision/ |
| `鉺雅鉻雷射`(Er:YAG MCL31) · `UP雷射` | Er:YAG · UltraPulse | M:/eryag_laser/ · M:/ultrapulse/ |
| `皮秒真皮層透鏡` · `皮秒雙透鏡` · `皮秒單點` | — | M:/price/ |
| `輕齡蛋殼肌`(光纖雷射) | — | M:/gentlelaser-pico/ |
| `Volite 玻尿酸` | Volite | M:/hyaluronic_acid/ |
| `OBSERV膚質檢測` | — | M:/observ/ |
| `贅生物`(粟粒腫/瘜肉/皮脂腺增生/角化/痣/黃斑瘤) | — | M:/price/ |

---

## 3. koreabeautydream.com (韓佳人診所 한가인클리닉 · 타이베이)

**한국 전용 브랜드 확인(이번 범위 추가의 핵심 질문):** `Liztox` `麗茲` `Coretox` `Nabota` `娜柏塔` `Neuronox` `Meditoxin` `Botulax` `Rejuran` `麗珠蘭` `Chaeum` `彩韻` `Synpurl` `新珍珠` `Elravie` `Yvoire` `Neuramis` `Shurink` `Potenza` 를 사이트 전 페이지(60)에서 찾았다 → **하나도 없음**. 톡신은 `美國 Botox保妥適 / 韓國 Letybo保提拉 / 英國 Dysport皇家` 셋뿐(K:/treatments/micro-plastic/botox-treatment-guide). 이 사이트에 있는 한국 제품은 대만 허가를 받은 것(Juvelook·VIVABELLA·MINT·Oligio·Ultraformer·Curejet·Vital Injector2·Density)뿐이다.

### 표 A-K — 사전 term 과 같은 것

| 사이트 표기 | 영문 | 사전 term | 지금 사전 zh-Hant | 제안 | 출처 성격 | URL |
|---|---|---|---|---|---|---|
| `美國 Botox保妥適` · `肉毒桿菌素` | Botox | ph-033 | 肉毒 | 없음 | 대만 클리닉 | K:/treatments/micro-plastic/botox-treatment-guide |
| `韓國 Letybo保提拉` | Letybo | ph-031 · ph-042 | 樂提保 · 白毒 | name `保提拉` | 대만 클리닉 | 같음 |
| `英國 Dysport皇家` | Dysport | ph-039 | 儷緻 | alias `皇家肉毒` | 대만 클리닉 | 같음 |
| `咀嚼肌過大造成的國字臉` · `瘦小腿` · `肩頸瘦肩` · `多汗症` | — | ph-034 · ph-038 · ph-035 · ph-029 | — | 없음 | 대만 클리닉 | 같음 |
| `喬雅登玻尿酸` · `BELOTERO 保柔緹` | Juvéderm · Belotero | ph-005 · ph-007 | 喬雅登 · 保柔緹 | 없음 | 대만 클리닉 | K:/treatments/micro-plastic/hyaluronic-acid-filler |
| `JuveLook喬雅露 (素顏針)` · `Lenisna 200mg大分子` | Juvelook · Juvelook Volume | ph-108 · ph-113 | 喬雅露 | ph-108 alias `素顏針` → 표 C-5 | 대만 클리닉 | K:/treatments/micro-plastic/juvelook |
| `Sculptra 舒顏萃 (4D童妍針)` | Sculptra | ph-112 | 舒顏萃 | alias `童妍針` | 대만 클리닉 | K:/treatments/micro-plastic/sculptra-youth-4d-needle |
| `Sunmax 膚力原膠原蛋白` · `膠原蛋白熊貓針` | Collagen | ph-109 | 膠原蛋白 | 없음 | 대만 클리닉 | K:/treatments/micro-plastic/sunmax-skin-origin-collagen |
| `MegaFill 異體真皮粉` | hADM | ph-116 | 無細胞同種真皮 | name `異體真皮`(표 A-T 와 같음) | 대만 클리닉 | K:/treatments/micro-plastic/megafill-alloderm-powder |
| `MINT神力拉提2.0` · `韓國MINT神力拉提 민트실리프팅 TFDA認證合法臉部PDO拉提` · `秘特線` | MINT Lift | ph-063 | Mint薄荷線 / [秘特線, Mint Lift, 薄荷線, Mint] | alias `神力拉提` · 표 C-10 | 대만 클리닉 | K:/treatments/micro-plastic/mint-lifting-guide |
| `Stratafix 藍鑽魚骨線` | Thread | ph-061 | 埋線拉提 | 제품명은 표 B | 대만 클리닉 | K:/treatments/micro-plastic/stratafix |
| `Thermage®FLX 鳳凰電波` | Thermage FLX | ph-130 | 鳳凰電波 | 없음 | 대만 클리닉 | K:/treatments/medical-beauty/thermal-flx-phoenix-wave |
| `Ultherapy PRIME 美國音波2.0極透+` | Ulthera | ph-121 | 美國音波 | 없음 | 대만 클리닉 | K:/treatments/medical-beauty/ultherapy-prime |
| `Ultraformer III 海芙3音波` · `第三代海芙音波` | Ultraformer III | ph-126 | 海芙音波 | 표 C-1 | 대만 클리닉 | K:/treatments/medical-beauty/ultraformer-iii |
| `Oligio 玩美電波` | Oligio | ph-123 | 玩美電波 | 없음 | 대만 클리닉 | K:/treatments/medical-beauty/oligio-perfect-wave |
| `VirtueRF 神比微針電波` · 「加入黃金微針的物理性重建」 | Needle RF | ph-141 · ph-135 | 微針電波 · 黃金微針 | 표 C-3 | 대만 클리닉 | K:/treatments/medical-beauty/divine-microneedle-rf-asce |
| `魔泌ASCEplus` · `魔泌ASCE` | ASCE+ | ph-153 | ASCE+ 外泌體 / [艾思科+, ASCE+] | alias `魔泌` · `艾思科+` 는 3 사이트에 없음 | 대만 클리닉 | K:/news/latest-news/asce |
| `Exosome 外泌體` | Exosome | ph-082 | 外泌體 | 없음 | 대만 클리닉 | K:/treatments/regeneration/exosome-exosomes |
| `Vital Injector2 水光注射` · `水光槍` · `물광주사` · `水光針` | Mesogun · Skin Booster · Water Glow | ph-090 · ph-074 · ph-089 | 水光槍 · 水光針 · 水光 | ph-074/089 alias `水光注射` | 대만 클리닉 | K:/treatments/medical-beauty/vital-injector2-hydro-injection · K:/news/blog/korean-celeb-secret-aqua-injection |
| `HydraFacial 海菲秀` · `海菲秀深層清潔` · `水皮秒/水飛梭` | Deep Cleansing | ph-091 | 深層清潔 | 표 C-11 | 대만 클리닉 | K:/treatments/medical-beauty/hydrafacial-treatment |
| `MedioStar 德國光纖除毛` · `二極體粉餅雷射` | Hair Removal | ph-011 | 除毛雷射 | 표 C-14 | 대만 클리닉 | K:/treatments/medical-beauty/mediostar-laser-hair-removal |
| `探索皮秒 DiscoveryPico` | Picosecond | ph-022 | 皮秒雷射 | 없음 | 대만 클리닉 | K:/treatments/medical-beauty/picoskin-treatment-guide |
| `Belkyra 倍克脂` · `去氧膽酸`(消脂點滴 페이지) | DCA | ph-059 | 脂肪細胞破壞 | name `去氧膽酸`(표 A-T 와 같음) | 대만 클리닉 | K:/treatments/weight-loss/belkyra-double-chin-treatment · /custom-fat-reduction-drip |
| `客製化消脂點滴` · `肝得健消脂針` | — | ph-058 · ph-055 | 溶脂針 · 點滴 | 표 C-11 | 대만 클리닉 | K:/treatments/weight-loss/custom-fat-reduction-drip |
| `Onda Pro 昂達超微波` | Microwave | ph-125 | 微波治療 | 표 C-9 | 대만 클리닉 | K:/treatments/weight-loss/ondapro |
| `ZField 肌力塑` · `HEIT電磁科技` | Body EMS | ph-139 | 身體EMS | 표 C-12 | 대만 클리닉 | K:/treatments/weight-loss/german-muscle-sculpt |
| `PLT 血小板生長因子凍晶` · 「突破以往的PRP治療限制」 | PRP | ph-157 · ph-158 | PRP · PRP/自體血 | 표 C-15 | 대만 클리닉 | K:/treatments/regeneration/plt-platelet-growth-factor-cryogel |
| `韓式皮膚管理` | Medical Skincare | ph-095 | 皮膚管理 | 없음 | 대만 클리닉 | K:/doctors |

### 표 B-K — 새 후보

| 사이트 표기 | 영문 | 비고 | URL |
|---|---|---|---|
| `VIVABELLA 薇貝拉 (魔法針)` · `黑童`(200 大分子) · `白童針`(50 小分子) | VIVABELLA | 한국 PDLLA+HA | K:/treatments/micro-plastic/vivabella-magic-needle |
| `Profhilo 逆時真`(제목) · `Profhilo 逆時針`(본문) | Profhilo | 제목 표기 흔들림 | K:/treatments/micro-plastic/profhilo |
| `Sofwave 索夫波` · `Density 無雙電波` | — | | K:/treatments/medical-beauty/sofwave · /density |
| `Curejet 酷捷無針注射` · `CureJet 酷捷無針水光` | Curejet | 한국 무침 주입 | K:/treatments/medical-beauty/curejet |
| `DermaClear 黑鑽水飛梭` | — | | K:/treatments/medical-beauty/terms-clear-black-diamond-hydro-microdermabrasion |
| `ILIB 氦氖雷射(靜脈雷射)` · `MCS 血漿置換術` | — | | K:/treatments/regeneration/ilib-helium-neon-laser · /mcs-plasma-exchange |
| `RA 自體微移植育髪` | — | ph-102 근처 | K:/treatments/regeneration/ra-hair-restoration |
| `韓式線雕隆鼻`(不動刀三段式隆鼻) · `微笑唇` | — | | K:/treatments/micro-plastic/korean-thread-nose-lift · /news/latest-news/korean-classic-treatment-smile-lips |
| `薇薇電波` | Viveve | | K:/news/blog/vivi-radiofrequency-female-health |

---

## 4. 표 C — 모호한 말(여러 term 에 걸림 · 사이트마다 다르게 부름)

| # | 말 | 무엇이 걸리나 | 사이트별 근거 |
|---|---|---|---|
| C-1 | `海芙音波` | Ultraformer III(=한국 Shurink) 를 가리킬 때와 `海芙音波媚必提`(Ultraformer MPT = 한국 Shurink Universe) 를 줄여 부를 때가 섞임. 사전 ph-126 슈링크유니버스 name 은 `海芙音波` | T: 「海芙音波…同原理機型在韓國以「Shurink」名稱銷售」, 「媚必提…韓國同世代機型以「Shurink Universe」名稱銷售」 · M: 제목 `Ultraformer 海芙音波`, 본문 `海芙音波媚必提` · K: `Ultraformer III 海芙3音波` |
| C-2 | `鳳凰` 계열 | `鳳凰電波`(Thermage FLX) · `黃金電波`(Thermage CPT, 이전 세대) · `鳳凰光`(Clear+Brilliant **레이저**) · 사전 ph-123 Oligio alias `小鳳凰` | T:/flx鳳凰電波/ · T:/cpt黃金電波/ · T:/cbt/ · M:/thermage_cpt/ (「鳳凰電波比較」) |
| C-3 | `黃金微針` | 한국에선 Potenza, 대만 Potenza 는 `無限電波`(T 설명). K 는 VirtueRF 의 구성 요소로, T 는 Exion 의 「24K黃金微針」으로 씀 → 기기 하나가 아니라 바늘 종류 | T:/gold-microneedling/ · T:/portfolio-item/exion/ · K:/…/divine-microneedle-rf-asce |
| C-4 | `水光` 계열 | `水光針`(시술 통칭) · `水光槍`(기계) · `水光注射` · 그리고 **바늘 없는** `音波水光` `冰晶水光` `無針水光`(Curejet) — ph-074 · ph-089 · ph-090 · ph-092 에 걸림 | T:/mesotherapy-fail/ (「水光針是療程統稱…水光槍是以自動化儀器施打」) · K:/…/vital-injector2… · K:/…/curejet |
| C-5 | `童顏/素顏` 계열 | Juvelook = M `新童妍` · K `素顏針`. Sculptra = T `童顏針` `童妍針` · K `4D童妍針`. Belotero Revive = T `素妍針`. 사전 ph-112 alias `素顏萃童顏針`. **`素顏針`(K: Juvelook) 과 `素妍針`(T: Belotero Revive) 은 한 글자 차이로 다른 제품** | M:/juvelook/ · K:/…/juvelook · T:/portfolio-item/sculptra/ · T:/portfolio-item/revive/ |
| C-6 | `熊貓針` | `膠原蛋白熊貓針`(双美/Sunmax 콜라겐) · `白金熊貓針`(Deusaderm) · `熊貓光`(레이저) | T:/膠原蛋白熊貓針/ · T:/deusaderm-ultra/ · T:/eye-laser/ · K:/…/sunmax… |
| C-7 | `天使` · `皇家` | `天使肉毒`(Xeomin) 대 `輕盈天使肩`(어깨 보톡스 상품명). `皇家肉毒`(Dysport) · K `Dysport皇家` 대 `曼陀皇家Boost`(가슴 보형물) | T:/天使肉毒_xeomin/ · T:/shoulder-slimming/ · T:/皇家肉毒/ · T:/mentor-boost/ |
| C-8 | `聚焦飛梭` | 제목은 `聚焦飛梭雷射`, 부제가 `蜂巢皮秒空泡效應` → ph-015/016 飛梭雷射 · ph-017 蜂巢皮秒 둘 다에 걸림 | T:/portfolio-item/聚焦飛梭/ |
| C-9 | `微波` | `清新微波 miraDry`(땀샘, T) · `昂達超微波 Onda`(지방, K) · 사전 ph-125 마이크로웨이브(기기 리프팅) 微波治療. 덧붙여 M `清新光 Neobeam`(레이저)는 `清新微波` 와 이름이 비슷함 | T:/微波止汗/ · K:/…/ondapro · M:/neobeam/ |
| C-10 | MINT 실 | 사전 name `Mint薄荷線` · T `秘特 MINT LIFT` · K `MINT神力拉提` + `秘特線`. `薄荷線` 은 3 사이트에 없음 | T:/埋線拉提/ · K:/…/mint-lifting-guide |
| C-11 | `消脂/溶脂` · `水飛梭/海菲秀` | ① `消脂針`(T 주표기) · `溶脂針` · `倍克脂`(DCA) · `消脂點滴` · `肝得健消脂針`(K) → ph-058 · ph-059 · ph-055 ② `水飛梭`(T Venus Glow, M 渦流清潔) · `海菲秀`/`海飛秀`(Hydrafacial, T 는 두 표기 다 씀, K 는 `海菲秀`) · `水皮秒`(K) · `黑鑽水飛梭`(K) → ph-091 | T:/消脂針/ · T:/belkyra/ · K:/…/custom-fat-reduction-drip · T:/新一代水飛梭/ · K:/…/hydrafacial-treatment |
| C-12 | EMS · 光 | `菲斯波 EMFACE`(HIFES+RF, 얼굴) · `易力肌塑 TeslaFormer`(磁雕, 몸) · `肌力塑 ZField`(電磁, 몸) → ph-138/139/140. `美肌動力光`(여러 색 빛, T) → ph-104 LED 인지 불명 | T:/emface/ · T:/teslaformer/ · K:/…/german-muscle-sculpt · T:/美肌動力光/ |
| C-13 | 전안 보톡스 | `美肌拉提斯 MagiLates`(Dysport 全臉肉毒拉提) · `微滴`(T 비교 항목) → ph-046 스킨보톡스 · ph-049 풀페이스큐레이션 어느 쪽인지 불명 | T:/portfolio-item/magilates/ |
| C-14 | `光纖` | M `日式光纖雷射`(除毛/美白/淡斑) · M `亞歷山大光纖雷射除毛` · T `日式光纖` · K `德國光纖除毛`(二極體) — 같은 말로 다른 기기 | M:/gentlelaser-light/ · M:/laser_hair_removal/ · T:/日式光纖/ · K:/…/mediostar… |
| C-15 | 미백 · 혈소판 | M `白皙微針注射`(傳明酸＋維他命C, 바늘 주입) 대 ph-052 미백 = 수액 `美白點滴`. K `PLT 血小板生長因子凍晶` 대 ph-157 PRP | M:/vitamin/ · K:/…/plt… |

## 5. 사전 표기 중 이번 3 사이트에서 근거를 못 찾은 것(참고 · 틀렸다는 뜻은 아님)

`吉適`(ph-039) · `思奧美`(ph-037) · `瑞藍`(ph-006) · `樂提保`(ph-031) · `紐樂適`(ph-028) · `麗姿妥適`(ph-040) · `素顏萃童顏針`(ph-112) · `黃金樁`(ph-071) · `美版超聲刀`(ph-121) · `麗珠蘭黑盒/紅盒/白盒`(ph-072/075/079) · `薄荷線`(ph-063) · `機打`(ph-090) · `微脂肪填充`(ph-068) · `脂肪細胞破壞`(ph-059) · `艾思科+`(ph-153) · `痘痘專用`(ph-098) · `疤痕專用`(ph-100) · `冷凍減脂`/`酷塑`(ph-105/106 — 세 사이트 모두 냉동지방분해 시술 페이지가 없음)

## 6. 코디·사용자가 정할 것(결정하지 않음)

1. 톡신 4 term(ph-027·031·041·042)의 name 을 대만 허가명(`娜柏塔` `保提拉` `優力柔`)으로 바꾸고 색 별명(`綠毒` `白毒` `粉毒`)을 alias 로 내릴지
2. 대륙식 표기 6건(§0-2)을 name 에서 고칠지, alias 에서 지울지(`熱瑪吉` 처럼 사이트가 「대만 아님」이라고 한 것도 손님이 말할 수는 있음)
3. ph-126 슈링크유니버스 = `海芙音波媚必提` 로 둘지, `海芙音波` 를 유지할지(표 C-1)
4. ph-135 포텐자 name 을 `無限電波` 로 바꿀지(T 설명 1건이 근거)
5. 표 B 의 새 시술을 사전에 넣을지와 범위(제품 브랜드까지인가, 시술 일반명까지인가). 수술·감량 약은 사전 카테고리 밖
6. 한국 전용 브랜드(리즈톡스·코어톡스·신펄·더채움·리쥬란 주사)의 중문명은 대만 클리닉 사이트로는 **얻을 수 없다**는 점 — 다른 출처(한국 클리닉의 중문 페이지, 강남언니 TW 판 등)를 볼지
