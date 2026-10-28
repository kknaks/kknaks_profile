# 통키 용어집 — 대만(zh-Hant) 현지 시술명 · 대륙(zh) 구어 별칭 조사

- 조사 날짜: **2026-10-27** · 조사자: interpret-pwa researcher (read-only)
- 대상: `interpret-pwa-poc/back/seed/glossary.json` 157 term (`zh-Hant` 전부 `source: draft-s2twp`, `reviewed: false`)
- 결과: **대만 현지명 77/157** (확신 높음 38 · 보통 39) · 찾지 못함 80
- 이 리포트는 결정하지 않는다. 시드에 어떻게 반영할지는 코디·사용자가 정한다(§5).

## 0. 출처 등급과 읽는 법

| 표시 | 뜻 |
|---|---|
| 공식 | 대만 지자체·병원 문서 (臺南市政府衛生局 收費標準 · 中國醫藥大學附設醫院 衛教 · 臺大/長庚 · 國軍醫院) |
| 매체 | 대만 언론·건강매체 (taiwannews · marieclaire.com.tw · commonhealth · tvbs · businesstoday · moneyweekly · thenewslens · heho · ettoday(광고성 기사)) |
| 비공식 | Dcard · vocus · uptogo · **creatrip · 강남언니(gangnamunni.com/tw)** — 뒤의 둘은 한국 회사가 만든 대만 손님용 번체 플랫폼이다. 「대만 손님이 한국에 와서 보는 이름」이라 통키에는 오히려 직접적이지만, 대만 현지 클리닉 출처는 아니다 |

- **확신**: 높음 = 서로 다른 도메인 2개 이상 / 보통 = 1개 / 없음 = 찾지 못함
- 본문을 직접 열어 확인한 것과 **검색 결과 스니펫으로만 본 것**을 구분했다. Dcard·uptogo·commonhealth 는 본문 접근이 막혀(403) 제목·스니펫까지만 봤다. 스니펫으로만 본 항목은 비고에 「스니펫 기준」이라고 적었다.
- 대만에서 수입되지 않는 한국 브랜드(Chaeum·Mint·TESS·LDM·InMode FX 등)는 대만판 플랫폼에서 **영문 브랜드 + 일반명**(예: 「Chaeum 玻尿酸」, 「TESS線」)으로 쓴다. 중문 음역명은 거의 나오지 않는다.

## 1. 핵심 발견 (시드 `zh-Hant` 가 체계적으로 틀린 자리)

1. **「鐳射」는 홍콩 표기다. 대만은 「雷射」다.** s2twp 가 대륙 「激光」를 「鐳射」로 바꿔서, 레이저 계열 zh-Hant 가 전부 홍콩식이 됐다(ph-013·014·015·016·019·020·022·023). 대만 공식 문서(臺南市 收費標準, 中國醫大 衛教)는 모두 「雷射」를 쓴다.
2. **리프팅 기기 넷이 전부 대륙식 이름이다.**
   | 시술 | 시드 zh-Hant | 대만 손님이 부르는 이름 |
   |---|---|---|
   | 울쎄라 | 美版超聲刀 | **美國音波** (別 極線音波·美版音波) |
   | 써마지FLX | 美版熱瑪吉FLX | **鳳凰電波** |
   | 올리지오 | 韓版熱瑪吉 | **玩美電波** (別 超玩美電波·韓版電波·小鳳凰) |
   | 슈링크유니버스 | 韓版超聲刀 | **海芙音波** (別 韓版音波) |
   | (볼뉴머) | 黃金樁 | **海芙電波** — 「黃金樁」은 홍콩·한국 클리닉 이름 |
3. **일반명도 대만어가 따로 있다.** 超聲波→**音波**, 射頻→**電波**(電波拉提·電波拉皮), 等離子→**電漿**, 脫毛→**除毛**, 刷酸→**果酸換膚**, 機打→**水光槍**, 冷凍溶脂→**冷凍減脂**(상표 酷塑), 脂肪填充→**自體脂肪(移植/注射)**, 提亮(토닝)→**淨膚雷射**, 色素→**(雷射)除斑**, IPL→**脈衝光**
4. **수입 브랜드는 대만 정식명이 따로 있다.** Restylane 瑞藍→**瑞絲朗**, Yvoire 伊婉→**伊芙瑞**, Xeomin 思奧美→**淨優明**, Dysport 吉適→**儷緻**, Radiesse 瑞得喜→**晶亮瓷**, Sculptra 素顏萃童顏針→**舒顏萃**, Ellansé 少女針→**洢蓮絲**. 그대로 맞는 것은 喬雅登(Juvéderm)·保柔緹(Belotero)·喬雅露(Juvelook)·蜂巢皮秒(PicoSure)·超皮秒(PicoWay)·鈴鐺線·麗珠蘭.
5. **분류 의심 1건**: ph-071 볼뉴머(Volnewmer)는 Classys 의 단극 RF 리프팅 기기인데([BT](https://www.businesstoday.com.tw/article/category/183030/post/202411050010/) · [VOV](https://vocus.cc/article/66f4cf0ffd89780001027553)), 시드는 「스킨부스터」로 분류했다. 처분은 코디가 정한다.

## 2. 대만 현지명 표 (157 term)

| term id | ko | 지금 시드 zh-Hant | 대만 현지명 | 대만 별칭[] | 출처 수(도메인) | 출처 URL | 확신 | 비고 |
|---|---|---|---|---|---|---|---|---|
| ph-001 | 신펄 | 新珍珠 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-002 | 채움 | 彩韻 | **Chaeum 玻尿酸** | — | 1 | https://www.gangnamunni.com/tw/events/125452 | 보통 | 영문 브랜드 + 玻尿酸 형태(강남언니 대만판). 彩韻 표기는 대만 출처 못 찾음 |
| ph-003 | 필러 | 填充劑 | **玻尿酸 (填充物)** | 玻尿酸注射 · 填充物注射 | 2 | https://health.tainan.gov.tw/warehouse/5655246A-3ADF-4F0F-BB63-DAA878C8EB30/20160224162451_臺南市醫療機構美容醫學診療項目收費標準表.pdf<br>https://tw.stock.yahoo.com/news/%E6%B3%B0%E5%90%88%E4%BB%A3%E7%90%86lg%E7%8E%BB%E5%B0%BF%E9%85%B8%E9%87%9D%E5%8A%91-%E7%8D%B2%E8%A1%9B%E7%A6%8F%E9%83%A8%E6%A0%B8%E5%87%86%E4%B8%8A%E5%B8%82-092924292.html | 높음 | 臺南市 收費標準 항목명 「玻尿酸及其它填充物注射」. 「填充劑」 단독 사용 근거 못 찾음 |
| ph-004 | 더채움 | 彩韻Plus | 찾지 못함 | — | 0 | — | 없음 | |
| ph-005 | 쥬비덤 | 喬雅登 | **喬雅登** | Juvederm | 2 | https://tw.stock.yahoo.com/news/%E6%B3%B0%E5%90%88%E4%BB%A3%E7%90%86lg%E7%8E%BB%E5%B0%BF%E9%85%B8%E9%87%9D%E5%8A%91-%E7%8D%B2%E8%A1%9B%E7%A6%8F%E9%83%A8%E6%A0%B8%E5%87%86%E4%B8%8A%E5%B8%82-092924292.html<br>https://www.gangnamunni.com/tw/events/146754 | 높음 | 시드와 같음 |
| ph-006 | 레스틸렌 | 瑞藍 | **瑞絲朗** | Restylane | 1 | https://tw.stock.yahoo.com/news/%E6%B3%B0%E5%90%88%E4%BB%A3%E7%90%86lg%E7%8E%BB%E5%B0%BF%E9%85%B8%E9%87%9D%E5%8A%91-%E7%8D%B2%E8%A1%9B%E7%A6%8F%E9%83%A8%E6%A0%B8%E5%87%86%E4%B8%8A%E5%B8%82-092924292.html | 보통 | 시드 「瑞藍」은 대륙명. 대만은 瑞絲朗 |
| ph-007 | 벨로테로 | 保柔緹 | **保柔緹** | Belotero | 1 | https://www.marieclaire.com.tw/beauty/skin-care/84561 | 보통 | 시드와 같음 |
| ph-008 | 엘라비에 | 艾拉薇 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-009 | 이브아르 | 伊婉 | **伊芙瑞** | Yvoire | 1 | https://tw.stock.yahoo.com/news/%E6%B3%B0%E5%90%88%E4%BB%A3%E7%90%86lg%E7%8E%BB%E5%B0%BF%E9%85%B8%E9%87%9D%E5%8A%91-%E7%8D%B2%E8%A1%9B%E7%A6%8F%E9%83%A8%E6%A0%B8%E5%87%86%E4%B8%8A%E5%B8%82-092924292.html | 보통 | 시드 「伊婉」은 대륙명. 대만 정식 수입명은 伊芙瑞(泰合生技 대리) |
| ph-010 | 색소 | 色素 | **除斑** | 雷射除斑 | 1 | https://health.tvbs.com.tw/review/364534 | 보통 | 「色素」 대신 「斑」으로 부름(雷射除斑) |
| ph-011 | 제모 | 脫毛 | **除毛雷射** | 雷射除毛 | 2 | https://health.tainan.gov.tw/warehouse/5655246A-3ADF-4F0F-BB63-DAA878C8EB30/20160224162451_臺南市醫療機構美容醫學診療項目收費標準表.pdf<br>https://health.tvbs.com.tw/medical/349135 | 높음 | 대만은 「除毛」(시드 「脫毛」는 대륙식) |
| ph-012 | 토닝 | 提亮 | **淨膚雷射** | 雷射淨膚 | 3 | https://health.tainan.gov.tw/warehouse/5655246A-3ADF-4F0F-BB63-DAA878C8EB30/20160224162451_臺南市醫療機構美容醫學診療項目收費標準表.pdf<br>https://health.tvbs.com.tw/review/364534<br>https://creatrip.com/zh-TW/blog/14908 | 높음 | 대만의 「토닝」은 Nd:YAG 1064 淨膚雷射. 시드 「提亮」은 근거 없음 |
| ph-013 | 혈관 | 血管鐳射 | **血管雷射** | 染料雷射 | 2 | https://health.tainan.gov.tw/warehouse/5655246A-3ADF-4F0F-BB63-DAA878C8EB30/20160224162451_臺南市醫療機構美容醫學診療項目收費標準表.pdf<br>https://epaper.ntuh.gov.tw/health/201204/pdf/%E8%84%88%E8%A1%9D%E5%BC%8F%E6%9F%93%E6%96%99%E9%9B%B7%E5%B0%84%E2%94%80%E5%92%8C%E4%BD%A0%E7%9A%84%E8%A8%8E%E5%8E%AD%E7%B4%85%E6%96%91%E8%AA%AA%E6%8E%B0%E6%8E%B0.pdf | 높음 | 시드 「鐳射」는 홍콩 표기. 대만은 雷射 |
| ph-014 | 레이저 | 鐳射 | **雷射** | — | 2 | https://health.tainan.gov.tw/warehouse/5655246A-3ADF-4F0F-BB63-DAA878C8EB30/20160224162451_臺南市醫療機構美容醫學診療項目收費標準表.pdf<br>https://cmuh.cmu.edu.tw/HealthEdus/Detail?no=6934<br>https://www.cmuh.cmu.edu.tw/HealthEdus/Detail?no=6921 | 높음 | 시드 「鐳射」는 홍콩 표기. 대만 병원·지자체 문서 전부 「雷射」 |
| ph-015 | 프락셀 | 飛梭鐳射 | **飛梭雷射** | Fraxel | 2 | https://health.tainan.gov.tw/warehouse/5655246A-3ADF-4F0F-BB63-DAA878C8EB30/20160224162451_臺南市醫療機構美容醫學診療項目收費標準表.pdf<br>https://www.cmuh.cmu.edu.tw/HealthEdus/Detail?no=6921 | 높음 | s2twp 결과 「飛梭鐳射」 → 대만은 「飛梭雷射」 |
| ph-016 | 프락셔널 | 點陣鐳射 | **飛梭雷射** | — | 2 | https://www.cmuh.cmu.edu.tw/HealthEdus/Detail?no=6921<br>https://health.tainan.gov.tw/warehouse/5655246A-3ADF-4F0F-BB63-DAA878C8EB30/20160224162451_臺南市醫療機構美容醫學診療項目收費標準表.pdf | 높음 | 대만에서 프락셔널 일반명도 飛梭雷射. 「點陣」은 대륙명 |
| ph-017 | 피코슈어 | 蜂巢皮秒 | **蜂巢皮秒** | PicoSure · 鉑金蜂巢皮秒 | 2 | https://cmuh.cmu.edu.tw/HealthEdus/Detail?no=6934<br>https://unni.app/tw/contents/37fd9338-d3d4-812e-9b7c-c231eef756ac | 높음 | 시드와 같음(蜂巢皮秒) |
| ph-018 | 피코웨이 | 超皮秒 | **超皮秒** | PicoWay | 1 | https://uptogo.com.tw/健康/醫學美容/蜂巢皮秒差別/ | 보통 | uptogo 본문은 403. 검색 스니펫으로만 확인 → 보통 |
| ph-019 | 레블라이트 | 鐳射 | **淨膚雷射** | RevLite淨膚雷射 · RevLite | 1 | https://www.gangnamunni.com/tw/events/149229 | 보통 | 시드 「鐳射」(일반명)는 오역. 대만판 플랫폼은 「RevLite淨膚雷射」 |
| ph-020 | 클라리티2 | 鐳射 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-021 | IPL | IPL | **脈衝光** | IPL | 2 | https://health.tainan.gov.tw/warehouse/5655246A-3ADF-4F0F-BB63-DAA878C8EB30/20160224162451_臺南市醫療機構美容醫學診療項目收費標準表.pdf<br>https://806.mnd.gov.tw/at-view/uploads/2022/PS-16.pdf | 높음 | 대만은 「脈衝光」. 홍콩은 「彩光」 |
| ph-022 | 피코초(Picosecond) | 皮秒鐳射 | **皮秒雷射** | 皮秒 | 3 | https://unni.app/tw/contents/37fd9338-d3d4-812e-9b7c-c231eef756ac<br>https://www.dcard.tw/f/makeup/p/231474959<br>https://cmuh.cmu.edu.tw/HealthEdus/Detail?no=6934 | 높음 | 鐳射→雷射 |
| ph-023 | 엑셀V | 鐳射 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-024 | 주름 | 皺紋 | **除皺** | 除皺針 · 動態皺紋 | 1 | https://www.gangnamunni.com/tw/events/147310<br>https://www.gangnamunni.com/tw/events/144503 | 보통 | 「除皺針」 = 주름 보톡스 |
| ph-025 | 코끝 | 鼻尖 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-026 | 턱선 | 下頜線 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-027 | 나보타 | 綠毒 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-028 | 뉴럭스 | 紐樂適 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-029 | 다한증 | 多汗症 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-030 | 더톡신 | 德妥欣 | **Jetema The Toxin** | The Toxin | 1 | https://www.gangnamunni.com/tw/events/147310 | 보통 | 강남언니 대만판 검색 스니펫에 「Jetema The Toxin」 영문 그대로. 중문명은 못 찾음 |
| ph-031 | 레티보 | 樂提保 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-032 | 목주름 | 頸紋 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-033 | 보톡스 | 肉毒素 | **肉毒** | 肉毒桿菌 · 肉毒桿菌注射 · 保妥適(Botox 상표) | 3 | https://health.tainan.gov.tw/warehouse/5655246A-3ADF-4F0F-BB63-DAA878C8EB30/20160224162451_臺南市醫療機構美容醫學診療項目收費標準表.pdf<br>https://www.commonhealth.com.tw/article/88833<br>https://www.gangnamunni.com/tw/events/147310 | 높음 | 시드 「肉毒素」 대신 대만 구어는 「肉毒」. 상표 Botox=保妥適 |
| ph-034 | 사각턱 | 咬肌 | **瘦臉針** | 國字臉 · 咀嚼肌肉毒 · 下顎角瘦臉針 · 瘦小臉 | 2 | https://www.gangnamunni.com/tw/events/147310<br>https://www.gangnamunni.com/tw/events/125289<br>https://www.commonhealth.com.tw/article/88833 | 높음 | 사각턱 보톡스. 咀嚼肌·國字臉·瘦小臉로 부름 |
| ph-035 | 승모근 | 斜方肌 | **斜方肌** | 瘦肩 | 1 | https://www.commonhealth.com.tw/article/88833 | 보통 | 시드와 같음(斜方肌). 「瘦肩」은 스니펫 근거 |
| ph-036 | 입꼬리 | 嘴角 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-037 | 제오민 | 思奧美 | **淨優明** | Xeomin · 天使肉毒 | 2 | https://www.gangnamunni.com/tw/events/144503<br>https://www.gangnamunni.com/tw/events/125289<br>https://www.worldjournal.com/wj/story/121208/9218319 | 높음 | 시드 「思奧美」는 대륙명. 대만은 淨優明. 天使肉毒 별칭은 WJ(미국 화문지)만 — 보조 |
| ph-038 | 종아리 | 小腿 | **小腿** | 瘦小腿 · 蘿蔔腿 | 2 | https://www.commonhealth.com.tw/article/88833<br>https://health.tainan.gov.tw/warehouse/5655246A-3ADF-4F0F-BB63-DAA878C8EB30/20160224162451_臺南市醫療機構美容醫學診療項目收費標準表.pdf | 높음 | 시드와 같음. 「瘦小腿」·「蘿蔔腿」은 스니펫 |
| ph-039 | 디스포트 | 吉適 | **儷緻** | Dysport | 1 | https://www.worldjournal.com/wj/story/121208/9218319 | 보통 | 시드 「吉適」는 대륙명. 대만 출처 1(WJ는 미국 화문지) — 보통 |
| ph-040 | 리즈톡스 | 麗姿妥適 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-041 | 메디톡신 | 粉毒 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-042 | 보툴렉스 | 白毒‌ | 찾지 못함 | — | 0 | — | 없음 | |
| ph-043 | 잇몸미소 | 牙齦笑 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-044 | 타임버스 | 時光巴士 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-045 | 넥큐레이션 | 頸部定製設計 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-046 | 스킨보톡스 | 緊緻肉毒 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-047 | 턱선보톡스 | 下頜線肉毒 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-048 | 바디큐레이션 | 身體定製設計 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-049 | 풀페이스큐레이션 | 全臉定製設計 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-050 | 페이스앤넥큐레이션 | 面頸部聯合定製設計 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-051 | 면역 | 免疫 | **免疫注射** | — | 1 | https://creatrip.com/zh-TW/blog/14808 | 보통 |  |
| ph-052 | 미백 | 美白 | **美白點滴** | 白玉注射 · 穀胱甘肽注射 · 美白導入 | 2 | https://creatrip.com/zh-TW/blog/14808<br>https://health.tainan.gov.tw/warehouse/5655246A-3ADF-4F0F-BB63-DAA878C8EB30/20160224162451_臺南市醫療機構美容醫學診療項目收費標準表.pdf | 높음 | 수액 문맥이면 白玉注射(글루타치온). TN103의 「美白、維它命C導入」은 피부 도포 시술 |
| ph-053 | 재생 | 再生 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-054 | 항산화 | 抗氧化 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-055 | 수액치료 | 輸液療法 | **點滴** | 營養點滴 · 靜脈注射 | 1 | https://creatrip.com/zh-TW/blog/14808 | 보통 | 시드 「輸液療法」 대만 근거 못 찾음 |
| ph-056 | 영양보충 | 營養補充 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-057 | 피로회복 | 疲勞恢復 | **維他命B/C/D注射** | 邁爾式雞尾酒點滴 | 1 | https://creatrip.com/zh-TW/blog/14808 | 보통 | 「疲勞恢復」이라는 이름 자체는 못 찾음 — 대표 시술명만 |
| ph-058 | 지방분해주사 (마케팅명) | 溶脂針 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-059 | DCA (지방세포파괴) | 脂肪細胞破壞 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-060 | 미라클 | 奇蹟線 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-061 | 실리프팅 | 線雕 | **埋線拉提** | 埋線 · 線雕 | 2 | https://www.thenewslens.com/article/133607<br>https://www.dcard.tw/f/facelift/p/261474483 | 높음 | 대만 기본은 「埋線(拉提)」. 「線雕」도 쓰임(TNL) |
| ph-062 | 에버라인 | 艾芙萊恩 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-063 | 민트리프트 | 秘特線 | **Mint薄荷線** | 薄荷線 · Mint | 1 | https://www.gangnamunni.com/tw/events/129974 | 보통 | 시드 「秘特線」 대만 근거 못 찾음 |
| ph-064 | 테스리프트 | 特斯線 | **TESS線** | TESS | 1 | https://www.gangnamunni.com/tw/events/129974 | 보통 | 시드 「特斯線」 대만 근거 못 찾음 |
| ph-065 | 실루엣소프트 | 鈴鐺線 | **鈴鐺線** | Silhouette Soft | 2 | https://www.dcard.tw/f/facelift/p/261474483<br>https://www.thenewslens.com/article/133607 | 높음 | 시드와 같음 |
| ph-066 | 지방이식 | 脂肪填充 | **自體脂肪移植** | 自體脂肪注射 · 補脂 | 2 | https://health.tainan.gov.tw/warehouse/5655246A-3ADF-4F0F-BB63-DAA878C8EB30/20160224162451_臺南市醫療機構美容醫學診療項目收費標準表.pdf<br>https://forum.heho.com.tw/post/5309 | 높음 | 시드 「脂肪填充」 대신 대만은 「自體脂肪(移植/注射)」. 「補脂」는 스니펫 |
| ph-067 | 나노지방이식 | 奈米脂肪填充 | **奈米脂肪** | — | 1 | https://forum.heho.com.tw/post/5309 | 보통 | 시드와 같음(奈米脂肪) |
| ph-068 | 마이크로지방이식 | 微脂肪填充 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-069 | SVF지방이식 | SVF 脂肪膠填充 | **SVF** | SVF gel | 1 | https://forum.heho.com.tw/post/5309 | 보통 | 영문 그대로 |
| ph-070 | 벨피엔 | 貝爾菲恩 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-071 | 볼뉴머 | 黃金樁 | **海芙電波** | Volnewmer · 黃金樁(港·韓) | 2 | https://www.businesstoday.com.tw/article/category/183030/post/202411050010/<br>https://vocus.cc/article/66f4cf0ffd89780001027553 | 높음 | ⚠ 볼뉴머는 단극 RF 기기(Classys). 시드는 「스킨부스터」로 분류. 「黃金樁」은 홍콩·한국 클리닉명(VOV 명시) |
| ph-072 | 리쥬란아이 | 麗珠蘭白盒 | **麗珠蘭** | Rejuran · 麗珠蘭眼周 | 1 | https://www.moneyweekly.com.tw/_Article?AID=229100 | 보통 | 麗珠蘭 브랜드명만 확인. 「白盒」 등 색상 별칭은 대만 출처 못 찾음. 대만 정식 판매는 외용 Booster 계열뿐(MW229100) |
| ph-074 | 스킨부스터 | 水光針 | **水光針** | 水光槍 | 2 | https://www.commonhealth.com.tw/article/90136<br>https://creatrip.com/zh-TW/blog/14908 | 높음 | 시드와 같음(水光針) |
| ph-075 | 리쥬란 힐러 | 麗珠蘭黑盒 | **麗珠蘭** | Rejuran Healer | 1 | https://www.moneyweekly.com.tw/_Article?AID=229100 | 보통 | 「黑盒」 별칭은 대만 출처 못 찾음 |
| ph-076 | 콜라겐/신규 | 膠原蛋白/新產品 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-077 | 엑소좀/성장인자 | 外泌體/生長因子 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-078 | HA (물광) | 水光針 | **水光針** | 玻尿酸水光 | 1 | https://www.commonhealth.com.tw/article/90136 | 보통 |  |
| ph-079 | 리쥬란 HB+ | 麗珠蘭紅盒 | **麗珠蘭** | Rejuran HB Plus | 1 | https://www.moneyweekly.com.tw/_Article?AID=229100 | 보통 | 「紅盒」 별칭은 대만 출처 못 찾음 |
| ph-080 | PDRN | PDRN | **PDRN** | 聚脫氧核苷酸 | 1 | https://www.moneyweekly.com.tw/_Article?AID=229100 | 보통 | 영문 그대로. 스니펫 기준 |
| ph-081 | PN | PN | **PN** | 聚合核苷酸 | 1 | https://www.moneyweekly.com.tw/_Article?AID=229100 | 보통 | 영문 그대로. 스니펫 기준 |
| ph-082 | 엑소좀 | 外泌體 | **外泌體** | Exosome | 2 | https://www.gangnamunni.com/tw/events/163504<br>https://www.ctee.com.tw/news/20251219701660-430201 | 높음 | 시드와 같음 |
| ph-083 | 에스에프 | SF注射 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-084 | 큐어스킨 | CureSkin | 찾지 못함 | — | 0 | — | 없음 | |
| ph-085 | 줄기세포치료 | 幹細胞/再生 | **幹細胞** | — | 1 | https://www.ctee.com.tw/news/20251219701660-430201 | 보통 |  |
| ph-086 | 줄기세포배양액 | 幹細胞培養液 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-087 | 자가혈유래 줄기세포 | 自體血來源幹細胞 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-088 | SVF (자가지방줄기세포) | 自體脂肪幹細胞 | **SVF** | 脂肪幹細胞 | 2 | https://forum.heho.com.tw/post/5309<br>https://www.ctee.com.tw/news/20251219701660-430201 | 높음 | 「脂肪幹細胞」은 CTEE(訊聯 脂肪幹細胞 서비스) 기준 |
| ph-089 | 물광 | 水光 | **水光** | 水光針 | 1 | https://www.commonhealth.com.tw/article/90136 | 보통 |  |
| ph-090 | 메조건 | 機打 | **水光槍** | — | 1 | https://www.commonhealth.com.tw/article/90136 | 보통 | 시드 「機打」는 대륙 구어. 대만은 「水光槍」 |
| ph-091 | 딥클렌징 | 深層清潔 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-092 | 주입장비 | 匯入裝置 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-093 | 초음파관리 | 超聲波護理 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-094 | 케미컬필링 | 刷酸 | **果酸換膚** | 化學換膚 · 杏仁酸換膚 | 3 | https://health.tainan.gov.tw/warehouse/5655246A-3ADF-4F0F-BB63-DAA878C8EB30/20160224162451_臺南市醫療機構美容醫學診療項目收費標準表.pdf<br>https://www.commonhealth.com.tw/article/87734<br>https://www.dcard.tw/f/facelift/p/233999726 | 높음 | 시드 「刷酸」은 대륙 구어 |
| ph-095 | 메디컬스킨케어 | 皮膚管理 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-096 | 이온토포레시스 | 離子匯入 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-097 | 시그니처프로그램 | 特色專案 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-098 | 여드름 전용 | 痘痘專用 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-099 | 진정팩 관리 | 鎮靜面膜管理 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-100 | 흉터 전용 | 疤痕專用 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-101 | 약물 도포 관리 | 藥物塗抹管理 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-102 | 탈모(비수술) | 脫髮 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-103 | 약물/토피컬 | 藥物/外用 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-104 | 광치료(LED) | 光療 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-105 | 냉각지방분해 | 冷凍溶脂 | **冷凍減脂** | 酷塑 · CoolSculpting | 2 | https://www.cmuh.cmu.edu.tw/HealthEdus/Detail?no=7407<br>https://www.marieclaire.com.tw/beauty/health-fitness/87796 | 높음 | 시드 「冷凍溶脂」 대신 대만은 「冷凍減脂」, 상표 酷塑 |
| ph-106 | 크라이오리포라이시스 | 冷凍溶脂 | **冷凍減脂** | 酷塑 | 2 | https://www.cmuh.cmu.edu.tw/HealthEdus/Detail?no=7407<br>https://www.marieclaire.com.tw/beauty/health-fitness/87796 | 높음 | 같은 항목 |
| ph-107 | 엘란쎄 | 少女針 | **洢蓮絲** | Ellansé | 2 | https://uptogo.com.tw/健康/醫學美容/如何豐頰/<br>https://news.everydayhealth.com.tw/?p=46202 | 높음 | 시드 「少女針」은 대륙 구어. 검색 스니펫 기준 — 본문 미확인 |
| ph-108 | 쥬베룩 | 喬雅露 | **喬雅露** | Juvelook | 1 | https://www.marieclaire.com.tw/beauty/skin-care/81106 | 보통 | 시드와 같음 |
| ph-109 | 콜라겐 | 膠原蛋白 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-110 | 글로벨라 | 格洛貝拉 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-111 | 래디어스 | 瑞得喜 | **晶亮瓷** | Radiesse | 2 | https://uptogo.com.tw/健康/醫學美容/如何豐頰/<br>https://news.everydayhealth.com.tw/?p=46202 | 높음 | 시드 「瑞得喜」는 대륙명. 스니펫 기준 |
| ph-112 | 스컬트라 | 素顏萃童顏針 | **舒顏萃** | Sculptra | 2 | https://uptogo.com.tw/健康/醫學美容/如何豐頰/<br>https://news.everydayhealth.com.tw/?p=46202 | 높음 | 시드 「素顏萃童顏針」은 대륙식. 스니펫 기준 |
| ph-113 | 쥬베룩볼륨 | 喬雅露黑瓶豐盈 | **喬雅露** | Lenisna | 1 | https://www.marieclaire.com.tw/beauty/skin-care/81106 | 보통 | 대만은 볼륨형을 「Lenisna 200mg(大分子)」로 소개 |
| ph-114 | 바이오스티뮬레이터/콜라겐부스터 | 膠原蛋白增生劑 / 再生針劑 | **膠原蛋白增生劑** | — | 2 | https://uptogo.com.tw/健康/醫學美容/如何豐頰/<br>https://news.everydayhealth.com.tw/?p=46202 | 높음 |  |
| ph-115 | CaHA (칼슘하이드록시아파타이트) | 羥基磷灰石鈣 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-116 | 무세포동종진피(hADM) | 無細胞同種真皮 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-117 | PCL (폴리카프로락톤) | 聚己內酯 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-118 | PDLLA (폴리-D,L-락틱산) | PDLLA / 聚雙旋乳酸 | **聚雙旋乳酸** | PDLLA | 1 | https://www.marieclaire.com.tw/beauty/skin-care/81106 | 보통 | 시드와 같음 |
| ph-119 | PDO (폴리디옥사논) | 聚對二氧環己酮 | **PDO線** | 聚對二氧環己酮線 | 1 | https://www.thenewslens.com/article/133607 | 보통 | 스니펫 기준 |
| ph-120 | PLLA (폴리-L-락틱산) | 聚左旋乳酸 | **聚左旋乳酸** | PLLA | 1 | https://uptogo.com.tw/健康/醫學美容/如何豐頰/ | 보통 | 시드와 같음 |
| ph-121 | 울쎄라 | 美版超聲刀 | **美國音波** | Ulthera · 極線音波 · 美版音波 · 音波拉提 | 4 | https://www.taiwannews.com.tw/zh/news/5054541<br>https://www.dcard.tw/@aive_dr_jun/post/260311453<br>https://vocus.cc/article/6985b8acfd8978000138b381<br>https://creatrip.com/blog/14916 | 높음 | ⚠ 시드 「美版超聲刀」 → 대만 손님은 「美國音波」. 극선音波는 creatrip 표기 |
| ph-122 | 인모드 | 英模 | **鑽石超塑** | InMode · INMODE FX | 1 | https://www.gangnamunni.com/tw/events/129937 | 보통 | 강남언니 대만판 검색 스니펫 기준(본문 옵션은 「INMODE FX」 영문). 대만 로컬 클리닉 출처 못 찾음 |
| ph-123 | 올리지오 | 韓版熱瑪吉 | **玩美電波** | Oligio · 超玩美電波 · 韓版電波 · 小鳳凰 | 3 | https://creatrip.com/zh-TW/blog/14911<br>https://www.ettoday.net/news/20260519/3168405.htm<br>https://www.dcard.tw/f/facelift/p/260723444 | 높음 | ⚠ 시드 「韓版熱瑪吉」 → 대만은 「玩美電波」. 韓版熱瑪吉는 대만에서 10Therma(十蓓電波) 별칭으로도 쓰임(대륙 표 참고) |
| ph-124 | 더블로골드 | 多普勒金 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-125 | 마이크로웨이브 | 微波治療 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-126 | 슈링크유니버스 | 韓版超聲刀 | **海芙音波** | Shurink · 韓版音波 | 4 | https://creatrip.com/blog/14916<br>https://www.businesstoday.com.tw/article/category/183030/post/202411050010/<br>https://vocus.cc/article/66f4cf0ffd89780001027553<br>https://www.gangnamunni.com/tw/events/153768 | 높음 | ⚠ 시드 「韓版超聲刀」 → 대만은 「海芙音波」(해외명 Ultraformer) |
| ph-127 | 시그니처 프로그램 | 特色專案 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-128 | 기기 리프팅 | 光電儀器拉提 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-129 | 복합 에너지 | 複合能量 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-130 | 써마지FLX | 美版熱瑪吉FLX | **鳳凰電波** | Thermage FLX · 熱瑪吉 · 美版電波 | 3 | https://creatrip.com/blog/14909<br>https://forum.heho.com.tw/post/6657<br>https://vocus.cc/article/66f4cf0ffd89780001027553 | 높음 | ⚠ 시드 「美版熱瑪吉FLX」 → 대만은 「鳳凰電波」. 熱瑪吉은 대륙·한국식(CR09) |
| ph-131 | HIFU (초음파) | 超聲波 | **音波拉提** | 音波 · HIFU | 2 | https://health.tvbs.com.tw/medical/354901<br>https://www.thenewslens.com/article/133607 | 높음 | 시드 「超聲波」 대신 대만은 「音波」 |
| ph-132 | LDM | LDM | **LDM水滴拉提** | LDM水滴 · LDM水滴超聲波 | 2 | https://www.gangnamunni.com/tw/events/145331<br>https://www.dcard.tw/f/facelift/p/262207230 | 높음 |  |
| ph-133 | RF (고주파) | 射頻 | **電波拉提** | 電波 · 電波拉皮 | 3 | https://health.tvbs.com.tw/medical/354901<br>https://health.tainan.gov.tw/warehouse/5655246A-3ADF-4F0F-BB63-DAA878C8EB30/20160224162451_臺南市醫療機構美容醫學診療項目收費標準表.pdf<br>https://www.thenewslens.com/article/133607 | 높음 | 시드 「射頻」 대신 대만 구어는 「電波」 |
| ph-134 | 시크릿 | Secret黃金微針 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-135 | 포텐자 | 黃金微針 | **黃金微針** | 無限電波 · Potenza | 1 | https://creatrip.com/zh-TW/blog/14908 | 보통 |  |
| ph-136 | 아그네스 | 雅格尼斯 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-137 | 인트라셀 | 英特拉賽爾 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-138 | 페이셜 EMS | 面部EMS | 찾지 못함 | — | 0 | — | 없음 | |
| ph-139 | 바디 EMS | 身體EMS | 찾지 못함 | — | 0 | — | 없음 | |
| ph-140 | HIFES/EMS | HIFES | 찾지 못함 | — | 0 | — | 없음 | |
| ph-141 | 니들RF | 微針射頻 | **微針電波** | — | 1 | https://creatrip.com/zh-TW/blog/14908 | 보통 | creatrip 14908 「微針RF探頭」. 「微針電波」라는 이름은 스니펫(痘疤 기사)뿐 — 보통 |
| ph-142 | 니들RF 장비 | 微針式RF裝置 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-143 | 플라즈마 | 等離子 | **電漿** | — | 1 | https://www.cgmh.org.tw/cgmn/cgmn_file/0903017.pdf | 보통 | 시드 「等離子」는 대륙어. 대만은 「電漿」 |
| ph-144 | 핫플라즈마 | 熱等離子 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-145 | 콜드플라즈마 | 冷等離子 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-146 | 마이크로니들링(MTS) | MTS | **微針** | MTS · 滾針 | 2 | https://www.dcard.tw/f/facelift/p/259745832<br>https://www.cgmh.org.tw/cgmn/cgmn_file/0903017.pdf | 높음 |  |
| ph-147 | 수동 MTS | 手動MTS | 찾지 못함 | — | 0 | — | 없음 | |
| ph-148 | 전동 MTS | 電動MTS | 찾지 못함 | — | 0 | — | 없음 | |
| ph-149 | 마이셀 | 瑪伊賽爾 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-150 | 셀피아 | 賽爾皮亞 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-151 | 리젠ACR | 瑞珍ACR | 찾지 못함 | — | 0 | — | 없음 | |
| ph-152 | ACT | ACT | 찾지 못함 | — | 0 | — | 없음 | |
| ph-153 | ASCEplus | 艾思科+ | **ASCE+ 外泌體** | ASCE+ | 1 | https://www.gangnamunni.com/tw/events/163504 | 보통 | 영문 브랜드 + 外泌體 |
| ph-154 | EXOSOME SKIN | 艾克索姆肌膚 | **ASCE+ 外泌體** | — | 1 | https://www.gangnamunni.com/tw/events/163504 | 보통 | ExoSCRT는 ASCE+의 기술명. 중문 고유명 못 찾음 |
| ph-155 | MCT (메타셀) | MCT | 찾지 못함 | — | 0 | — | 없음 | |
| ph-156 | PRF (피브린풍부혈장) | 富纖維蛋白血漿 | 찾지 못함 | — | 0 | — | 없음 | |
| ph-157 | PRP (혈소판풍부혈장) | 富血小板血漿 | **PRP** | 自體血小板 · 高濃度血小板血漿 | 1 | https://drug.tzuchi.com.tw/pain/images/files/0614-g.pdf | 보통 |  |
| ph-158 | PRP/자가혈 | PRP/自體血 | 찾지 못함 | — | 0 | — | 없음 | |
## 3. 대륙(zh) 구어 별칭 — 무엇을 가리키나

| 구어 | 가리키는 시술 | 출처 | 비고 |
|---|---|---|---|
| 超声刀 | **HIFU 일반명**. 맥락 없이 쓰면 대개 **울쎄라(Ultherapy)** 를 뜻한다 | [界面新闻](https://www.jiemian.com/article/9067548.html) — 「超声刀…通过聚焦超声加热」, [cn-healthcare](https://www.cn-healthcare.com/articlewm/20200706/content-1127954.html) — 超声刀를 SMAS 까지 닿는 집속 초음파로 설명 | ⚠ 모호. 미국판·한국판·중국산을 다 이 말로 부른다 |
| 美版超声刀 | **울쎄라(Ultherapy, Merz)** | [界面新闻](https://www.jiemian.com/article/9067548.html) 「美国Ulthera公司的超声刀Ultherapy…在国内被称为'美版超声刀'」, [新浪](https://k.sina.cn/article_6350340713_17a828269027005z3v.html) 「美国Ulthera超声刀」 | 높음 |
| 韩版超声刀 | **슈링크(Shurink = 해외명 Ultraformer, Classys)**. 중국명 「舒丽可」 | [新浪](https://k.sina.cn/article_6350340713_17a828269027005z3v.html) 「韩国的超声刀叫舒丽可」, [eastsidedermatology](https://eastsidedermatology.com.au/ultraformer-3-%E8%B6%85%E5%A3%B0%E5%88%80/) 「Ultraformer 3 超声刀」(호주 화문 클리닉 · 비공식) | 보통. 검색 스니펫에는 한국산 HIFU 제조사(Ultraformer·Doublo·UTIMS 등)를 통틀어 부른다는 서술도 있다(출처 [tuimy](https://www.tuimy.com/news/463.html), 본문 403) → **더블로 등 다른 한국 HIFU 일 수도 있다** |
| 超声炮 | **중국산 HIFU(深圳 半岛医疗)** — 울쎄라·슈링크 아님 | [界面新闻](https://www.jiemian.com/article/9067548.html) 「2021年6月，深圳半岛医疗的超声治疗仪获批，被称为'超声炮'」 | 높음은 아님(1). 손님이 「超声炮」라고 하면 우리 목록의 어느 기기와도 같지 않다 |
| 热玛吉 | **써마지(Thermage, Solta Medical)** — 상표 | [界面新闻](https://www.jiemian.com/article/9067548.html) 「Solta Medical（索塔医疗）公司的第一代热玛吉」, [Bausch Health IR](https://ir.bauschhealth.com/news-releases/2026/05-28-2026-211556273) (Thermage 중국 상표 인증), [cn-healthcare](https://www.cn-healthcare.com/articlewm/20200706/content-1127954.html) 「热玛吉也被称为电波拉皮，是一种单极射频」 | 높음. 대만 매체도 「熱瑪吉」를 「중국·한국식 명칭」으로 소개([CR09](https://creatrip.com/blog/14909)) |
| 韩版热玛吉 | **특정 기기 아님.** creatrip 은 **十蓓电波(10Therma, TENTECH)** 의 별칭으로 쓴다 | [creatrip zh-CN 14914](https://creatrip.com/zh-CN/blog/14914) 「十蓓电波…拥有『韩版热玛吉』、『韩版凤凰电波』的新称号」 | ⚠ 모호. 올리지오를 「韩版热玛吉」로 부르는 대륙 출처는 **찾지 못함**. 시드 ph-123 이 이 말을 올리지오에 붙였다 |
| 韩版电波 / 小凤凰 | **올리지오(Oligio)** (대만 표현) | [CR11](https://creatrip.com/zh-TW/blog/14911) 「玩美電波就是所謂的『韓版電波』…被稱作『小鳳凰電波』」 | 대만 구어. 대륙 구어 출처는 못 찾음 |
| 黄金桩 | **볼뉴머(Volnewmer)** (홍콩·한국 클리닉명) | [VOV](https://vocus.cc/article/66f4cf0ffd89780001027553) 「Volnewmer黃金樁(港·韓) / 海芙電波(台)」 | 대륙 출처는 못 찾음 |
| 海芙音波 / 海芙电波 | 슈링크 / 볼뉴머 (대만명) | §2 ph-126 · ph-071 | 대륙에서도 같은 이름을 쓰는지는 **찾지 못함** |

**정리**: 대륙 구어 중 한 기기로 딱 떨어지는 것은 「美版超声刀」=울쎄라, 「热玛吉」=써마지 둘뿐이다. 「超声刀」·「韩版超声刀」·「韩版热玛吉」는 여러 기기에 걸친다. 「超声炮」는 목록 밖 기기다.

## 4. 찾지 못한 목록 (80)

대만 출처에서 이름을 확인하지 못한 term. 시드 zh-Hant(s2twp 초안)를 대만명이라고 볼 근거가 **없다**.

- **한국 전용 브랜드** — 대만 판매가 없거나 대만판 플랫폼에서도 영문 그대로 쓰여 중문명이 안 나온 것: ph-001 신펄 · ph-004 더채움 · ph-008 엘라비에(대륙 「艾莉薇」 표기만 봄, 대만 아님) · ph-027 나보타(대만 TFDA 허가 사실만 확인, 중문명 못 찾음) · ph-028 뉴럭스 · ph-031 레티보 · ph-040 리즈톡스 · ph-041 메디톡신 · ph-042 보툴렉스 · ph-044 타임버스 · ph-060 미라클 · ph-062 에버라인 · ph-070 벨피엔 · ph-083 에스에프 · ph-084 큐어스킨 · ph-110 글로벨라 · ph-124 더블로골드 · ph-134 시크릿 · ph-136 아그네스 · ph-137 인트라셀 · ph-149 마이셀 · ph-150 셀피아 · ph-151 리젠ACR · ph-155 MCT
  - 강남언니 대만판의 톡신 옵션은 「Coretox」·「Xeomin（進口）」처럼 **영문 브랜드 + (韓國產/進口)** 로 쓴다([GU147310](https://www.gangnamunni.com/tw/events/147310)) → 한국 톡신은 대만 손님도 영문으로 말할 가능성이 크다(추정 아님 · 플랫폼 표기 사실만)
- **해외 기기·제품** — ph-020 클라리티2 · ph-023 엑셀V (대만 중문명 못 찾음)
- **부위·적응증 보톡스**: ph-025 코끝 · ph-026 턱선 · ph-029 다한증 · ph-032 목주름 · ph-036 입꼬리 · ph-043 잇몸미소 · ph-046 스킨보톡스 · ph-047 턱선보톡스
- **클리닉 자체 상품명(큐레이션·시그니처)**: ph-045 · ph-048 · ph-049 · ph-050 · ph-097 · ph-127 — 일반 용어가 아니라 대만명이 있을 수 없다
- **수액**: ph-053 재생 · ph-054 항산화 · ph-056 영양보충
- **지방**: ph-058 지방분해주사 · ph-059 DCA (대만 「溶脂針」 사용 여부·DCA 허가 여부 모두 못 찾음) · ph-068 마이크로지방이식
- **스킨부스터·재생**: ph-076 콜라겐/신규 · ph-077 엑소좀/성장인자 · ph-086 줄기세포배양액 · ph-087 자가혈유래 줄기세포 · ph-109 콜라겐 · ph-115 CaHA · ph-116 hADM · ph-117 PCL
- **메디컬스킨케어**: ph-091 딥클렌징 · ph-092 주입장비 · ph-093 초음파관리 · ph-095 메디컬스킨케어 · ph-096 이온토포레시스 · ph-098 여드름 전용 · ph-099 진정팩 관리 · ph-100 흉터 전용 · ph-101 약물 도포 관리 · ph-102 탈모(비수술) · ph-103 약물/토피컬 · ph-104 광치료(LED)
  - 참고: 臺南市 收費標準에 「美白、維它命C導入」 항목이 있다([TN103](https://health.tainan.gov.tw/warehouse/5655246A-3ADF-4F0F-BB63-DAA878C8EB30/20160224162451_臺南市醫療機構美容醫學診療項目收費標準表.pdf)) → 대만은 이온토포레시스류를 「導入」이라고 부른다는 근거 1건. ph-096 시드 「離子匯入」은 s2twp 가 「导入→匯入」로 **잘못** 바꾼 것(「匯入」은 IT 용어 import)일 가능성이 크다 — ph-092 「匯入裝置」, ph-097 「特色專案」(项目→專案)도 같은 s2twp 오변환 유형
- **기기 일반·EMS·MTS**: ph-125 마이크로웨이브 · ph-128 기기 리프팅 · ph-129 복합 에너지 · ph-138 페이셜 EMS · ph-139 바디 EMS · ph-140 HIFES/EMS · ph-142 니들RF 장비 · ph-144 핫플라즈마 · ph-145 콜드플라즈마 · ph-147 수동 MTS · ph-148 전동 MTS
- **PRP**: ph-152 ACT · ph-156 PRF · ph-158 PRP/자가혈

## 5. 코디·사용자가 정할 것 (결정하지 않음)

1. 대만명을 \`zh-Hant.name\` 으로 올리고 기존 s2twp 초안을 \`aliases\` 로 남길지, 버릴지 — 특히 「鐳射」(홍콩 표기)를 별칭에 남길지
2. 대륙 구어 중 **모호한 말**(超声刀 · 韩版超声刀 · 韩版热玛吉)을 한 term 의 alias 로 둘지, 「모호 — 되물어야 함」으로 따로 표시할지. 「超声炮」(목록 밖 중국산)를 어떻게 다룰지
3. ph-071 볼뉴머의 카테고리(스킨부스터 → 기기 리프팅?)
4. 한국 전용 브랜드(§4 첫 묶음)는 영문 브랜드명을 대만 \`name\` 으로 둘지
5. 「보통」(출처 1개·스니펫 기준) 항목을 \`reviewed: true\` 로 올릴 기준
6. s2twp 의 대만식 오변환(导入→匯入, 项目→專案, 设备→裝置)을 일괄 점검할지
