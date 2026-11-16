# 제조사 · 제품/장비 원장 초안 v4 — 허가 미확인 148 · 신규 현장 기기 끝까지(웹 → 식약처)

- 2026-10-27 · researcher · 데이터 `product-master-draft.json`(v4) · v3 본문은 아래 「v3 본문」에 그대로
- 대상: 게이트 「허가 미확인」 **148**(웹 미조사 22 포함) + 신규 현장 기기 **24**(식약처 후보 없음 17 + 웹 미확인 7) = 172 — 전부 웹 조사함
- 웹으로 정체를 찾은 것 **117/172** · 식약처 재조회 337회(질의 527) · 웹 검색 약 WebSearch 205 · WebFetch 97 · 네이버 검색 결과 조회(curl) 다수 — 7개 병렬 조사 합계(대략)
- 허가 미확인 148 → **20건 이동**(자동 7 · 라인 8 · 이름 맞고 업체 다름 3 · 웹 허가번호 일치 1) · 그대로 허가 미확인 128
- 신규 현장 기기 24: 허가 미확인 16 · **이름+업체 일치**(신규라 확인 필요) 4 · 라인(이름 든 제품 여럿) 3 · 직접 확인(이름 맞고 업체 다름) 1
- 판정 규칙(3차와 같음): 공식명에 이름이 들고 업체가 같으면 자동(근거가 웹이어도) · 이름 든 제품 여럿 = 라인 · 이름 맞고 업체 다름 = 직접 확인. 업체 비교는 원장 표기 또는 웹에서 찾은 제조사 · 수입사

## ① 4차에서 새로 찾은 것 — 원장 제품

| 원장 | 무엇(웹) | 웹 정식명 · 업체 | 식약처 허가 (모델 · 품목 · 업체 · 상태) | 판정 | 출처 |
|---|---|---|---|---|---|
| 더마브이 | 루트로닉 롱펄스 532nm KTP+1064nm Nd:YAG 혈관·색소 레이저(냉매 냉각) | DermaV · (주)루트로닉 (현 Cynosure Lutronic) · 수입 (주)루트로닉(제조) | DermaV (엔디야그 레이저 수술기) · 주식회사 사이노슈어루트로닉테크놀로지 · 정상 | **자동**(이름+업체 일치) | [1](https://www.massdevice.com/?p=28885) |
| 듀오타이트 | 비올메디컬의 HIFU(집속초음파) 리프팅 장비 | DUOTITE · (주)비올메디컬 | DUOTITE™ (집속형 초음파 자극 시스템) · (주)비올메디컬 · 정상 | **자동**(이름+업체 일치) | [1](https://www.medigatenews.com/news/1070182010) [2](https://medicaltimes.com/Main/News/NewsView.html?ID=1170014) |
| 볼뉴머RF | 클래시스의 6.78MHz 모노폴라 고주파 리프팅 장비 | VOLNEWMER · (주)클래시스 | VOLNEWMER(VM1-M100)외 1건 (범용전기수술기) · (주)클래시스 · 정상 | **자동**(이름+업체 일치) | [1](https://classys.co.kr/product/volnewmer/) |
| 셀리뉴 | 비올메디컬의 마이크로니들 고주파(RF) 장비 | CELLINEW · (주)비올메디컬 | CELLINEW™ (범용 전기 수술기) · (주)비올메디컬 · 정상 | **자동**(이름+업체 일치) | [1](https://www.fnnews.com/news/202401281830171747) |
| 스플렌더X | 루메니스 755+1064nm 동시조사(BLEND X) 제모 레이저 | SPLENDOR X · Lumenis Be Ltd. | SPLENDOR X Alexandrite+Nd:YAG (알렉산드라이트레이저수술기) · 루메니스비코리아 유한회사 · 정상 | **자동**(이름+업체 일치) | [1](https://lumenis.com/aesthetics/products/splendorx/) [2](https://www.bioworld.com/articles/461561) |
| 에이비오톡신 | abobotulinumtoxinA(아보보툴리눔톡신A)의 음차로 보이며, 이 성분의 제품은 … | Dysport · Ipsen · 수입 입센코리아(주) (미용 적응증 유통·판촉: 갈더마코리아) | 디스포트주(클로스트리디움보툴리눔A형독소-혈구응집소복합체) · 입센코리아(주) · 정상 | **자동**(이름+업체 일치) | [1](https://nedrug.mfds.go.kr/searchDrug?itemName=디스포트) [2](https://medigatenews.com/news/1834898375) |
| 울트라포머MPT | 클래시스의 집속초음파(HIFU) 리프팅 장비, 국내명 슈링크 유니버스의 해외명 | ULTRAFORMER MPT · (주)클래시스 | ULTRAFORMER MPT PLUS (집속형 초음파 자극 시스템) · (주)클래시스 · 정상 | **자동**(이름+업체 일치) | [1](https://classys.co.kr/product/shurink-universe/) [2](https://www.smarttoday.co.kr/ko-kr/articles/76343) |
| 레블라이트SI | 사이노슈어의 Q스위치 Nd:YAG 다파장(1064/532nm 등) 색소·토닝 레이저 | RevLite SI · Cynosure (현 Cynosure Lutronic) · 수입 사이노슈어코리아 (Cynosure Korea) — 정확한… | RevLite SI (엔디야그레이저수술기) · (주)루트로닉 · 정상 | 라인(이름 든 제품 여럿) | [1](https://drdamoa.com/) [2](https://medicalaesthetic.co.kr/) |
| 리프테라 | 아스테라시스 HIFU(고강도집속초음파) 리프팅 기기, 펜타입 카트리지 | Liftera · (주)아스테라시스 (Asterasys) · 수입 (주)아스테라시스(제조) | Liftera Cool외 1건 (집속형 초음파 자극 시스템) · (주)아스테라시스 · 정상 | 라인(이름 든 제품 여럿) | [1](https://www.segye.com/newsView/20210716509338) [2](https://www.imcas.com/en/imcas-world-congress-2023/program/session/54421/s157-asterasys-symposium-new-possibilities-of-facial-skin-tightening-with-the-exclusive-patented-liftera-pen-type-cartridge) |
| 모자이크 | 루트로닉 비박피 프랙셔널 레이저(1550nm), 후속 Mosaic 3D | MOSAIC · (주)루트로닉 (현 Cynosure Lutronic) · 수입 (주)루트로닉(제조) | MOSAIC 3D (기타 레이저 수술기) · 주식회사 사이노슈어루트로닉테크놀로지 · 정상 | 라인(이름 든 제품 여럿) | [1](https://www.massdevice.com/?p=28885) |
| 벨피엔 프로 | 휴메딕스 PN(연어 정소 DNA) + 고순도 HA + 리도카인 복합 필러(눈가 주름 적응증… | Valpien(데일리팜 영문요약 표기, 미검증) · 휴메딕스(Humedix, 휴온스그룹) | 밸피엔(BelPN)외 1건 (조직 수복용 생체 재료) · (주)휴메딕스 · 정상 | 라인(이름 든 제품 여럿) | [1](https://dailypharm.com/user/news/339507) [2](https://medigatenews.com/news/1103940830) |
| 스텔라M22 | 루메니스 IPL+ResurFX(1565nm)+Nd:YAG 모듈형 플랫폼(M22 후속) | Stellar M22 · Lumenis Be Ltd. | Stellar M22 White외 3건 (펄스광선조사기) · 루메니스비코리아 유한회사 · 정상 | 라인(이름 든 제품 여럿) | [1](https://practicaldermatology.com/news/new-from-lumenis-meet-the-stellar-m22-platform/2460300) [2](https://www.biospace.com/lumenis-introduces-an-advanced-intelligent-skincare-innovation-stellar-m22) |
| 에코2 | 루트로닉 프랙셔널 CO2 레이저 | eCO2 · (주)루트로닉 (현 Cynosure Lutronic) · 수입 (주)루트로닉(제조) | eCO2 3D (탄산가스 레이저 수술기) · 주식회사 사이노슈어루트로닉테크놀로지 · 정상 | 라인(이름 든 제품 여럿) | [1](https://www.massdevice.com/?p=28885) |
| 에코2에볼루션 | 루트로닉 eCO2 프랙셔널 CO2 레이저 계열(모델명 Evolution 미확인) | eCO2 · (주)루트로닉 (현 Cynosure Lutronic) · 수입 (주)루트로닉(제조) | eCO2 3D (탄산가스 레이저 수술기) · 주식회사 사이노슈어루트로닉테크놀로지 · 정상 | 라인(이름 든 제품 여럿) | [1](https://www.massdevice.com/?p=28885) |
| 에피티크 | 제테마의 가교 히알루론산(HA) 필러 브랜드(4등급 의료기기) | e.p.t.q. · (주)제테마 | e.p.t.q.S500 1.0mL외 26건 (조직수복용생체재료) · (주)제테마용인공장 · 정상 | 라인(이름 든 제품 여럿) | [1](https://www.hankyung.com/article/202605072345i) [2](https://www.medipharmhealth.co.kr/mobile/article.html?no=119082) |
| 더마샤인 | 자동 음압 멀티니들 스킨부스터 주입기(전동식 의약품 주입 펌프) '더마샤인' — 물광주사 … | Derma Shine · ㈜파나시 → 휴온스메디텍 | Panace-DS-54외 5건 (전동식 의약품 주입 펌프) · (주)휴온스메디텍 · 정상 | 직접 확인(웹 허가번호와 같은 허가 · 이름 미포함) | [1](https://search.naver.com/search.naver?query=더마샤인+의료기기+허가) [2](https://search.naver.com/search.naver?query=더마샤인+휴온스+제조) |
| E-MAX | 시네론 elos(광+양극성RF) 복합 플랫폼 eMax(후속 elos Plus, 현 캔델라) | eMax · Syneron Medical Ltd. (현 Candela) | elos Plus (범용전기수술기) · 시너론켄델라코리아 유한회사 · 정상 | 직접 확인(이름 맞고 업체 다름) | [1](https://www.biospace.com/syneron-inc-receives-fda-clearance-for-elos-plus-next-generation-multi-platform-device) [2](https://remma.fr/en/model/medical-aesthetic-device-elos-plus) |
| 벡터스 | 사이노슈어(구 팔로마) 810nm 다이오드 제모 레이저 | Vectus · Cynosure (구 Palomar Medical Technologies) | Vectus (반도체레이저수술기) · (주)루트로닉 · 취소 | 직접 확인(이름 맞고 업체 다름) | — |
| 스타워커 | 포토나(슬로베니아) Q스위치/피코초 Nd:YAG·KTP 색소·문신 레이저 | StarWalker · Fotona d.o.o. | M031-3A/2 PICO Pro (엔디야그 레이저 수술기) · (주)신한씨스텍 · 정상 | 직접 확인(이름 맞고 업체 다름) | [1](https://www.praiston.pl/en/catalog/view/12916/fotona-starwalker-m031-3a2-maqx-laser) [2](https://www.gangnamunni.com/events/93208) |
| 라이트쉬어듀엣 | 루메니스 800nm 다이오드 제모 레이저 | LightSheer DUET · Lumenis Ltd. | LightSheer Desire (반도체 레이저 수술기) · 루메니스비코리아 유한회사 · 정상 | 직접 확인(계열 이름만 맞음) | — |

## ② 신규 현장 기기 24 — 웹 · 식약처

| 사진 | 현장 이름 | 무엇(웹) · 구분 | 웹 정식명 · 업체 | 식약처 허가 | 판정 | 출처 |
|---|---|---|---|---|---|---|
| DEV-005 | 아포지플러스 | 사이노슈어의 755nm 알렉산드라이트(+1064nm Nd:YAG 듀얼) 제모 레이저 '아포… · 의료기기 | Apogee+ · Cynosure, LLC(사이노슈어) · 수입 사이노슈어 한국법인(사이노슈어코리아, 루트로닉과 합병) — 수입사 법인명 미확인 | **못 찾음** | 허가 미확인 | [1](https://search.naver.com/search.naver?query=Apogee%2B+알렉산드라이트+허가) [2](https://search.naver.com/search.naver?query=사이노슈어코리아+아포지+엘리트+수입) |
| DEV-015 | 이브타이탄 | (주)위로(WEERO)·라이트스톤 공동개발 RF(1MHz 바이폴라)+EMS+미세전류 트리플… · 의료기기 | EVE TITAN · (주)위로(WEERO) | 이름 든 허가 없음 | 허가 미확인 | [1](https://search.naver.com/search.naver?query=이브타이탄+제조사) [2](https://search.naver.com/search.naver?query=이브타이탄+의료기기+허가+위로+제조) |
| DEV-018 | 이래비티 | 1064nm 롱펄스 Nd:YAG 레이저 리프팅 장비(수직 열 스태킹 방식), 이노메드 자체… · 의료기기 | ERAVITY · 이노메드 (INNOMED) | 이름 든 허가 없음 | 허가 미확인 | [1](https://drdamoa.com/product/eravity-%EC%9D%B4%EB%9E%98%EB%B9%84%ED%8B%B0/794/) [2](https://www.aestheticnews.co.kr/news/articleView.html?idxno=10020) |
| DEV-020 | 엔진리프팅 | EMS(근육 전기자극)+RF(고주파) 동시 조사 패치형 얼굴 리프팅 장비 (엔파인더스 N-… · 의료기기 | N-Gine · 엔파인더스(주) (N-Finders Co., Ltd.) | 이름 든 허가 없음 | 허가 미확인 | [1](https://nfinders.com/) [2](https://nfinders.com/eng/product_n-gine/) |
| DEV-034 | 벨르업 | 집속형 초음파(10Hz) 펜 카트리지 방식 미용기기(KC 인증) — 벨루미에 브랜드 탄력·… · 미용기기(비의료) | Belle Up · (주)벨레브 (판매사·브랜드 벨루미에 BELLELUMIE) — 제조사 별도 여부 미확인 | **못 찾음** | 허가 미확인 | [1](https://bellelumiemall.co.kr/product/%EB%B2%A8%EB%A5%B4%EC%97%85-%EB%B3%B8%EC%B2%B4/37/) [2](http://www.signaturemg.co.kr/shop/detail.php?idx=1698) |
| DEV-041 | 수소토닝 | 고농도 수소수·살균수(오존수)·아쿠아필(A/B/C 솔루션) 3모드 물 기반 피부관리 장비 … · 미용기기(비의료) | DUO HYDROGEN · Umbrella Inc. (엄브렐라, tradeKorea 판매자 — 제조/무역 구분 미확정) | **못 찾음** | 허가 미확인 | [1](https://www.tradekorea.com/product/detail/P791762/DUO-Hydrogen--aqua-peeling,-hydrogen-therapy,-skin-care-.html) [2](https://sevenu.co.kr/bbs/board.php?bo_table=notice&wr_id=34) |
| DEV-042 | 더마큐어 | 'DERMACURE' 표기 장비 — 후보: 더마큐어 플라즈마(DERMACURE PLASMA… · 미상 | 못 찾음 | **못 찾음** | 허가 미확인 | [1](https://www.mediallfor.com/74/?idx=75) |
| DEV-044 | 힐퓨전프로 | 3D 회전팁 워터젯 하이드로더마브레이전+흡입+솔루션 주입+하이드로 나노롤링 K-필링 피부관… · 미용기기(비의료) | HealFusion Pro · 힐룩스 (Healux Co., Ltd., 대표 김도연 — 쥬베룩·아이쓰레드 운영사) | **못 찾음** | 허가 미확인 | [1](https://www.rapportian.com/news/articleView.html?idxno=223110) [2](https://www.rapportian.com/news/articleView.html?idxno=222899) |
| DEV-045 | 크라이오 멀티마스터 | 크라이오 냉·온열+초음파+이온토+전기천공+스킨스크러버 6-in-1 프리/애프터 피부관리 장… · 미용기기(비의료) | CRYO MULTI MASTER · MORE3 (모어쓰리 추정 표기, 브랜드 PUREYOUNG 퓨리영) | **못 찾음** | 허가 미확인 | [1](https://www.gobizkorea.com/mobile/mobileGoodsDetail.do?goods_no=GS20180317186413) [2](https://www.tradekorea.com/product/detail/P779214/Cryo-multi-Master.html) |
| DEV-047 | 울킨 | 1/3/10MHz HIFU+고밀도 듀얼 초음파(HDU) 피부미용 기기 — 제조사 사이트에 … · 미용기기(비의료) | ULKIN · (주)메딕콘 (MEDICON) | **못 찾음** | 허가 미확인 | [1](https://www.ulkin.net/) [2](http://www.medicon.co.kr/en/21_en/18) |
| DEV-049 | 오투덤 | PSA 방식 90% 산소+음이온 약 300만개를 돔 마스크로 전달하는 산소테라피 피부관리기… · 미용기기(비의료) | O2toDerm · 주식회사 트리시스 | **못 찾음** | 허가 미확인 | [1](https://www.sportsseoul.com/news/read/804413) [2](https://blog.yeoshin.co.kr/blog/o2toderm-oxygen-therapy-skin-revitalization/) |
| DEV-052 | 트리필 프로 | CO2 가스 박리(서브시전)+약물(스킨부스터·PLLA 등) 3단계 순차 주입 의료기기 — … · 의료기기 | TriFill PRO · 엠큐어 (MCURE Co., Ltd.) | 이름 든 허가 없음 | 허가 미확인 | [1](https://mcure.co.kr/en/trifill-pro/) [2](https://www.tradekorea.com/product/detail/P837728/Trifill-Pro-Medical-Aesthetic-CO%E2%82%82-Subcision-Device-for-Skin-Care.html) |
| DEV-053 | AUTO MTS | 동방메디컬 국산 자동 MTS(마이크로니들) 디지털 머신 — 왕복 선형운동식, 니들 길이 조… · 의료기기 | DB FNS · 동방메디컬 (주식회사 동방메디컬, dbmedi.com) | DB FNS MICRO NEEDLE C-2.0U외 3건 (의약품 흡수 유도 피부 자극기) · (주)동방메디컬분당지점 · 정상 | **이름+업체 일치**(신규라 확인 필요) | [1](https://jongromedi.com/product/%EB%8F%99%EB%B0%A9%EB%A9%94%EB%94%94%EC%BB%AC-%EA%B5%AD%EC%82%B0-db-fns-%EC%98%A4%ED%86%A0mts-%EB%8B%88%EB%93%A4%EC%A1%B0%EC%A0%88-mts%EB%A8%B8%EC%8B%A0/1588/) [2](https://m.beautynanda.co.kr/product/db-fns-%EB%94%94%EC%A7%80%ED%84%B8-%EB%A8%B8%EC%8B%A0/2172/) |
| DEV-056 | 소노케어 | 다중주파(1/3MHz, 3/10MHz) 교차 고밀도 초음파 자극기 — 통증 완화·피부관리(… · 의료기기 | SONOCARE · 뉴퐁 (NEWPONG) | 이름 든 허가 없음 | 허가 미확인 | [1](https://www.newpong.com/kr/sonocare/) [2](https://www.medifonews.com/news/article.html?no=175168) |
| DEV-060 | 피코라이트블랙 | 수도그룹 피코세컨드 Nd:YAG 레이저(1064/532nm, 200~300ps) 색소·토닝… · 의료기기 | PICOLITE Black · 수도그룹 (SooDo Group, 1993 설립, 부산) | PICOLITE Black외 3건 (엔디야그레이저수술기) · (주)수도그룹 · 정상 | 라인(이름 든 제품 여럿) | [1](https://soodogroup.com/en/product/picolite/) [2](https://kr.aving.net/news/articleView.html?idxno=1797877) |
| DEV-061 | 피코 라이트 | 수도그룹 피코세컨드 Nd:YAG 레이저 PICOLITE(1064/532nm) — DEV-0… · 의료기기 | PICOLITE · 수도그룹 (SooDo Group) | PICOLITE Black외 3건 (엔디야그레이저수술기) · (주)수도그룹 · 정상 | 라인(이름 든 제품 여럿) | [1](https://soodogroup.com/en/product/picolite/) [2](https://kr.aving.net/news/articleView.html?idxno=1788052) |
| DEV-063 | 큐라스토닝 | 이루다 Q-switched Nd:YAG 레이저(1064/532nm) 색소·토닝 장비 CuR… · 의료기기 | CuRAS · 이루다 (Ilooda Co., Ltd.) — 큐라스 하이브리드는 클래시스 사이트에도 게재(이루다가 클래시스 계열) | 이름 든 허가 없음 | 허가 미확인 | [1](https://classys.co.kr/product/curas-hybrid/) [2](https://laserpro.or.kr/bbs/?t=9rl) |
| DEV-069 | 아톰레이저 | 405nm+635nm 듀얼 비열성 저출력 레이저(Class 3B) 손발톱 무좀(조갑진균증)… · 의료기기 | ATOM · 에버코스텍 (Evercosteq) — 검색 요약 기준, 미검증 · 수입 (주)메디뷰랩 (판매/브랜드 페이지), 바디코스 (공급사) | ATOM (범용전기수술기) · (주)바이오넷 · 취소 | 직접 확인(이름 맞고 업체 다름) | [1](http://medi-beau.com/page/product/atom.html) [2](https://www.biotimes.co.kr/news/articleView.html?idxno=34708) |
| DEV-071 | 미라쥬 | 3D 얼굴 스캐너 기반 얼굴 지능 진단·미용 디자인(시술 시뮬레이션) 상담 시스템 — 중국… · 미상 | Mirage 3D · Shanghai Yingzi Intelligent Technology Co., Ltd. (上海影子智能科技有限公司) | **못 찾음** | 허가 미확인 | [1](http://myreal3d.com/) [2](https://www.tmtpost.com/trendmakers/419421) |
| DEV-072 | 3D 메타뷰 | 4광원(일반/광택/편광/UV) 3D 얼굴 피부 분석기 — 카메라 3대 회전 촬영, 피부·성… · 미상 | 3D Meta-Vu · 피에스아이플러스㈜ (PSI PLUS Co., Ltd.) | 3D Meta-Vu R외 1건 (체외형 의료용 카메라) · 피에스아이플러스 주식회사 · 정상 | **이름+업체 일치**(신규라 확인 필요) | [1](http://www.psiplus.co.kr/home/sub02_01.php) [2](https://drdamoa.com/product/3d-meta-vu-3d%EB%A9%94%ED%83%80%EB%B7%B0/790/) |
| DEV-073 | 마크뷰 | 4광원 2D 피부 분석기 — 14종 피부 문제 정량 분석(세계 최초 전 광원 LED 분석기… · 미상 | Mark-Vu · 피에스아이플러스㈜ (PSI PLUS Co., Ltd.) | Mark-Vu WR외 3건 (체외형 의료용 카메라) · 피에스아이플러스 주식회사 · 정상 | **이름+업체 일치**(신규라 확인 필요) | [1](http://www.psiplus.co.kr/home/sub02_02.php) [2](https://www.psiplus.co.kr/en/sub02_02.php) |
| DEV-074 | 스캐나 | 비침습 피부 측정 AI 스캔 시스템(DERMA AI SCAN SYSTEM) — 피부 상태 … · 미상 | SKENA · 브이앤코 주식회사 (V&CO Co., Ltd.) | **못 찾음** | 허가 미확인 | [1](https://skena.co.kr/) |
| DEV-075 | 카프리레이저 | 1450nm 다이오드 레이저+약 400~415nm 블루 레이저 듀얼 파장 여드름·피지조절 … · 의료기기 | CAPRI · (주)오로 (ORO Co., Ltd. / ORO Tech Co., Ltd., 2016 설립) — 미국 M사와 공동개발 | CAPRI (반도체레이저수술기) · (주)오로 · 정상 | 라인(이름 든 제품 여럿) | [1](https://orolaser.com/?page_id=13) [2](https://us.kompass.com/p/oro-co-ltd/kr001399/capri-laser/98b1b9b6-e577-4ab6-80d9-d29752dc7301/) |
| DEV-076 | 아큐토닝 | 1450nm 고출력 다이오드 레이저 피지선 타깃 여드름·모공·흉터 치료기(K.L Globa… · 단종 | Accu TONING · K.L Global (케이엘글로벌) | ACCUTONING (반도체 레이저 수술기) · 주식회사 케이엘글로벌 · 정상 | **이름+업체 일치**(신규라 확인 필요) | [1](https://drdamoa.com/product/accu-toning-%EC%95%84%ED%81%90%ED%86%A0%EB%8B%9D-%EB%8B%A8%EC%A2%85/667/) [2](https://drdamoa.com/category/kl-global/799/) |

## ③ 끝까지 못 찾은 것과 이유 — 원장 제품(허가 미확인 유지)

| 원장 | 시술군 | 무엇인지 한 줄 | 구분 · 이유 | 출처 |
|---|---|---|---|---|
| 다복스 | M1 | 갈더마 취급 보툴리눔톡신으로 추정되나 '다복스'라는 제품명은 확인 불가 | 미상 — 의약품안전나라 '다복스' 검색 0건, 보툴리눔 허가 60건 중에도 없음. 갈더마가 국내에서 취급하는 톡신은 디스포트주(입센코리아 수입, 갈더마코리아 미용 유통)뿐이므로 디스포트의 병원 내 오기/별칭… | [1](https://nedrug.mfds.go.kr/searchDrug?itemName=다복스) [2](https://nedrug.mfds.go.kr/searchDrug?itemName=보툴리눔) |
| 보리톡스 | M1 | 보령제약 보툴리눔톡신으로 기재됐으나 해당 제품 확인 불가 | 미상 — 의약품안전나라 '보리톡스' 0건, 국내 보툴리눔 허가 60건 중 보령 제품 없음. 웹 검색에서도 보령 톡신 판권 기사 미확인. 병원 자체 표기/오기 추정 | [1](https://nedrug.mfds.go.kr/searchDrug?itemName=보리톡스) [2](https://nedrug.mfds.go.kr/searchDrug?itemName=보툴리눔) |
| 퓨어녹스 | M1 | 대화제약 보툴리눔톡신으로 기재됐으나 해당 제품 확인 불가 | 미상 — 국내 보툴리눔 허가 60건 중 '퓨어녹스'·대화제약 제품 없음(대화제약 주사제 8건에도 톡신 없음). 웹 검색 결과 없음. 순수톡신(코어톡스·제오민·보타루마 등)을 가리키는 병원 메뉴명이거나 오기 … | [1](https://nedrug.mfds.go.kr/searchDrug?itemName=보툴리눔) |
| 이볼브 | M10 | 인모드의 핸즈프리 RF+전자기(EMS) 바디 컨투어링 플랫폼 | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 국내 허가·수입사 페이지 확인 못함. RF와 근자극 결합이라 품목이 둘로 나뉠 수 있음 | [1](https://aestheticsjournal.com/tag/inmode/page/2/) |
| 쿨톤 | M10 | 앨러간(애브비)의 자기장 근육자극(MMS) 바디 톤업 장비 | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — FDA 2019 승인. 국내 허가·수입 정보 미확인 | [1](https://plasticsurgerypractice.com/treatment-solutions/products/allergan-receives-fda-clearance-cooltone-device/) [2](https://www.dermatologytimes.com/view/allergans-cooltone-device-receives-fda-clearance) |
| 트윈픽셀 | M11 | 은성글로벌의 고주파 마이크로니들링(니들RF) 장비, 이온도입·부스터 핸드피스 포함 | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 2025년 11월 식약처 제조품목허가 획득(기사). 허가번호 미기재 | [1](https://m.news.nate.com/view/20260203n28214) [2](https://www.businesskorea.co.kr/news/articleView.html?idxno=268380) |
| 프라임RF | M11 | 니들RF 그룹 항목이나 '프라임RF' 장비 확인 안 됨 | 미상 — 검색 결과 없음. '악센트 프라임'(Alma, 비니들 RF)·'울쎄라피 프라임' 등과 혼동되거나 병원 자체 메뉴명 추정 | — |
| 스킨스탬프 | M12 | 도장(스탬프)형 니들로 피부에 미세 구멍을 내는 MTS 시술의 일반 명칭 | 일반 시술명 — 특정 제품이 아닌 시술/도구 일반명(더마스탬프류). 이전 패스 판단과 동일 | — |
| 뉴라클플라즈마 | M13 | 플라즈마 피부 장비로 기재되었으나 '뉴라클' 제품 확인 안 됨 | 미상 — 한/영(NEURACLE) 검색 결과 없음. 병원 자체 메뉴명 또는 소규모 장비 추정 | — |
| 플라스젠 | M13 | 플라즈마 피부 장비로 기재되었으나 해당 제품 확인 안 됨 | 미상 — 동음 '플라스젠(PLAZEN)'은 치과 근관치료용 수중방전 플라즈마로 피부 장비 아님. 피부 플라즈마 '플라스젠'은 미확인 | [1](https://dentalnews.or.kr/news/article.html?no=48503) |
| 크라이오듀얼 | M14 | 후보: 벨기에 Medibeauty의 'Cryo-Dual' 흡입+냉각 지방감소 장비 | 미상 — 국내 '크라이오듀얼' 도입·허가 정보 없음. 동명 해외 장비만 확인되어 동일 여부 미확정. 듀얼 핸드피스 냉동지방분해 장비의 병원 메뉴명일 수도 있음 | [1](https://www.medibeauty.be/en/catalogue/catalogue-12/catalogue-12/mb-cryo360) |
| 노보젯 | M15 | 바즈바이오메딕의 피부·미용용 솔레노이드 자동반복분사 무바늘 약물(앰플)전달기기 '노보젯' — 큐어젯의 전신/… | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 회사 IR 자료: '의료기기 큐어젯(CUREJET)과 미용기기 노보젯(NOVOJET)' — 노보젯은 의료기기가 아닌 미용기기(앰플 화장품 도포용)로 소… | [1](https://search.naver.com/search.naver?query=노보젯+NOVOJET+바즈바이오메딕) [2](https://search.naver.com/search.naver?query=노보젯+피부) |
| 데마루치 | M15 | 불명 | 미상 — '데마루치'·'더마루치' 피부관리 맥락 검색 결과 0건(일본 성곽 용어만 나옴). 병원 자체 메뉴명 또는 오기 추정 | [1](https://search.naver.com/search.naver?query=데마루치+관리) |
| 라라젯 | M15 | 에이치투메디의 올인원 페이셜 장비 '라라젯' — 라쿠아 필링(수분 필링)+저온 플라즈마+트리플 제트 분사, … | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 기사에서 '미용기기'와 '의료기기' 표현 혼재 — 의료기기 허가 여부·번호 미확인. MFDS 조회 시 제조사 메타바이오메드로 검색 권장 | [1](https://search.naver.com/search.naver?query=라라젯+LHALA+JET+제조사) [2](https://search.naver.com/search.naver?query=라라젯+피부과) |
| 라라젯 (클렌징) | M15 | 음압+고압 미세 물줄기로 모공을 세정하는 병의원용 하이드로필(아쿠아필) 장비 | 미상 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 제품은 확인됐으나 의료기기 허가 여부 미확인. 판매 페이지는 '피부미용기기'로 분류 — 비의료기기(미용기기)일 가능성 있어 category unknow… | [1](https://www.lhalala.co.kr/jet) [2](https://medinbeauty.kr/product/%EB%9D%BC%EB%9D%BC%EC%A0%AF-lalajet-%EB%B3%91%EC%9D%98%EC%9B%90-%EC%A0%84%EC%9A%A9-%EC%8B%A0%EA%B0%9C%EB%85%90%EC%9D%98-%ED%95%98%EC%9D%B4%EB%93%9C%EB%A1%9C%ED%95%84/633/) |
| 메소건 | M15 | 메조테라피건(메조건) — 스킨부스터·약물을 진피에 일정 깊이·용량으로 자동 주입하는 인젝터류 장비의 일반 명… | 일반 시술명 — 특정 브랜드가 아닌 장비 유형 명칭. 오픈닥터 등에서 하이쿡스 등 제품이 '메조건' 분류로 쓰임 | [1](https://search.naver.com/search.naver?query=메소건+피부과) [2](https://search.naver.com/search.naver?query=메소건+의료기기+허가) |
| 바이오프로톤 | M15 | '바이오포톤'의 오기 추정 — (주)바이오포톤의 PDP(Platina Diamond Photon) 생육광선 … | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — '바이오프로톤' 그대로는 0건. 바이오포톤은 에스테틱 바디·온열관리용으로 쓰임. 의료기기 허가 여부·번호 미확인(업종은 '기타 가정용 전기기기 제조'로… | [1](https://search.naver.com/search.naver?query=주식회사+바이오포톤+의료기기+허가) [2](https://search.naver.com/search.naver?query=바이오포톤+피부관리+기기) |
| 벨라소닉 | M15 | 위드윈네트웍(위드윈피부과 공동개발)의 듀얼 초음파 피부치료기 — 고주파 초음파 벨라소노(3/10MHz)+저주… | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 기사에 '초음파자극기 벨라소닉 식약처 판매허가'로 기재. 허가번호 미확인. 2X PLUS는 LTRA Global 출시로 블로그 언급 | [1](https://search.naver.com/search.naver?query=벨라소닉+허가번호) [2](https://search.naver.com/search.naver?query=벨라소닉+피부) |
| 비타인젝터 | M15 | '바이탈 인젝터(Vital Injector 2)'의 통칭 추정 — 은성글로벌의 다중바늘 진공(음압) 스킨부스… | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — '비타인젝터'는 피부과 블로그에서 더마샤인과 나란히 스킨부스터 주입 장비로만 언급됨. Vital Injector 대응은 추정(미검증). 허가번호 미확인 | [1](https://search.naver.com/search.naver?query=Vital+Injector+2+manufacturer+korea) [2](https://search.naver.com/search.naver?query=비타인젝터+리쥬란) |
| 셀라이트 | M15 | 불명 — 웹상 '셀라이트'는 홈케어 LED마스크(CL-1546, 서울샵 판매)와 동물용 구충제(셀라이트 60… | 미상 — 피부과용 '셀라이트' 장비 확인 안 됨. 홈케어 LED마스크 브랜드 '셀라이트'(CL-1546)가 있으나 병원 장비인지 불명, 병원 자체 메뉴명(셀+라이트=LED관리)일 가능성 | [1](https://search.naver.com/search.naver?query=셀라이트+LED) |
| 소노퀸 | M15 | 바이슨메디칼이 개발한 HIFU(집속형 초음파) 리프팅 장비 '소노퀸'(퀸테라피 시술에 사용) | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 원장부 그룹은 메디컬스킨케어지만 실제는 HIFU 리프팅(기기 리프팅). 허가번호·품목명 미확인(집속초음파자극시스템 류 추정, 미검증) | [1](https://search.naver.com/search.naver?query=소노퀸+리프팅+장비) |
| 아스트로더 | M15 | '아스트로돔(AstrodomeFacial)'의 오기 추정 — 돔 마스크로 순수산소·음이온·LED(Red/Bl… | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — '아스트로더'로는 검색 결과 0건, '아스트로돔'이 피부관리 맥락에서 유일하게 일치. 허가번호·품목명(LED 의료기기 여부) 미확인. 국내 수입/판매사… | [1](https://search.naver.com/search.naver?query=아스트로돔페이셜+공식+수입) [2](https://search.naver.com/search.naver?query=아스트로돔+의료기기) |
| 아쿠아젯 | M15 | 불명 — 피부과에서 시술 전 딥클렌징/수분 분사 관리 메뉴명으로 쓰이는 정황(강남의원·로렌의원 '아쿠아젯')… | 미상 — '아쿠아젯' 검색은 산업용 고압세척기(성보하이드로)·산후조리원 수압마사지기 위주. 특정 피부과 장비 제조사 확인 안 됨 — 병원 자체 메뉴명(아쿠아필/제트필 계열 관리) 추정 | [1](https://search.naver.com/search.naver?query=아쿠아젯+강남의원) [2](https://search.naver.com/search.naver?query=아쿠아젯+관리+장비) |
| 옥시덤 | M15 | 아나시스(ANACIS)의 비타민K1옥사이드 함유 시술 후 멍·홍조 진정 크림 '케이-옥시덤(K-Oxiderm… | 화장품 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 원장부 kind=device 이지만 웹상 '옥시덤'은 멍크림(화장품)만 확인됨. 블로그에 '팩과 옥시덤을 후관리'로 등장 — 후관리 도포 크림으로 추정… | [1](https://search.naver.com/search.naver?query=옥시덤+피부과) [2](https://www.hwahae.co.kr) |
| 올타이트 | M15 | 이노서스의 40.68MHz 초단파 고주파(집중유전가열 DEH) 국산 리프팅 장비 '올타이트' | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 원장부 그룹은 메디컬스킨케어지만 실제는 RF 리프팅(기기 리프팅). 영문 표기는 추정(미검증). 허가번호 미확인 | [1](https://search.naver.com/search.naver?query=올타이트+장비+제조사+출시) [2](https://search.naver.com/search.naver?query=올타이트+피부과) |
| 제네오X | M15 | 폴로젠(루메니스)의 옥시제네오 기반 복합 스킨케어 플랫폼 '제네오X' — 각질제거+산소(OxyGeneo)+R… | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 루메니스코리아가 국내 출시(론치 나이트) 기사 확인. 허가번호 미확인. 블로그 기준 2024년 출시 | [1](https://search.naver.com/search.naver?query=제네오X+수입+루메니스) |
| 큐어젯 | M15 | 바즈바이오메딕의 솔레노이드 무바늘(needle-free) 분사식 약물주입기기 '큐어젯' — 흉터·스킨부스터 … | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 오픈닥터 분류: '솔레노이드 무바늘 분사식 주사기'. 허가번호 미확인(품목명은 무바늘주사기 계열 추정, 미검증) | [1](https://search.naver.com/search.naver?query=큐어젯+피부과) [2](https://search.naver.com/search.naver?query=큐어젯+CUREJET+바즈바이오메딕) |
| 크라이오셀 | M15 | (주)에스제이(에스제이글로벌)의 냉각+이온토포레시스(크라이오 전기영동) 진정·비타민 도입 관리 장비 '크라이… | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 중고의료기 사이트(메드나라) 기재: 모델명 Cryocell, 제조사 (주)에스제이. 허가번호 미확인. '포텐셀' 복합기의 한 기능명으로도 쓰임 | [1](https://search.naver.com/search.naver?query=크라이오셀+장비+제조사+냉각) [2](https://search.naver.com/search.naver?query=크라이오셀+피부과) |
| 하이쿡스 | M15 | (주)노바메디가 제조한 스킨부스터용 석션 멀티 니들 인젝터(메조건) '하이쿡스' | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 기사: 'KFDA 허가'. 허가번호 미확인. 한 의원은 '마이크로니들 RF'로 소개하나 제조/유통 정보는 니들 인젝터 | [1](https://search.naver.com/search.naver?query=하이쿡스) [2](https://search.naver.com/search.naver?query=하이쿡스+노바메디+허가) |
| 헤어셀 | M15 | 미세 자기장으로 모낭을 자극하는 탈모 치료용 의료기기 '헤어셀 S2' — 원개발 캐나다 CTC, 현재 ㈜트리… | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 기사: '국내 처음 식약청 인증 탈모치료용 의료기기'. 허가번호 미확인. 수입 품목(CTC)과 트리비스 제조 품목이 별도일 수 있음 | [1](https://search.naver.com/search.naver?query=헤어셀+S2+수입+국내) [2](https://search.naver.com/search.naver?query=트리비스+헤어셀+S2+제조) |
| 리포린 | M16 | 삼익제약의 데옥시콜산(DCA) 이중턱(턱밑지방) 개선 주사제 '리포린주' — 펜믹스 위탁생산 위임형 제네릭 | 의약품 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 기사로 식약처 품목허가 확인(2025년 출시 목록에 '삼익제약 리포린'). 단, nedrug 공개검색(itemName=리포린, 데옥시콜산 성분 전체)에… | [1](https://search.naver.com/search.naver?query=리포린+삼익제약) [2](https://nedrug.mfds.go.kr/searchDrug?itemName=리포린) |
| 아큐주사 | M16 | 병원들이 쓰는 지방분해·윤곽 주사 메뉴명(프리미엄 아큐주사·바디아큐주사 등) — 스테로이드 무함유 칵테일로 … | 병원 자체 메뉴명 — 여러 병원 메뉴명으로만 확인. 이름 유래(Aqualyx/아큐렉스 등) 근거 불충분 — 단일 제품 특정 불가 | [1](https://search.naver.com/search.naver?query=아큐주사+성분) |
| 카이벨라 | M16 | 애브비(엘러간) 데옥시콜산 이중턱 주사 Kybella — 국내명 '벨카이라주', 2017년 식약처 허가·20… | 단종 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — nedrug 현행 데옥시콜산 주사 9품목(브이올렛주·벨라콜린주·올리핏주·펜카이라주·바이블주·밀리핏주사·원더브이주·브이렛주·브이벨라주)에 벨카이라 없음.… | [1](https://search.naver.com/search.naver?query=벨카이라주+데옥시콜산+허가) [2](https://nedrug.mfds.go.kr/searchDrug?ingrName1=데옥시콜산) |
| 팻킬주사 | M16 | 병원(아이디의원 등) 자체 명칭의 지방분해주사 메뉴 — 스테로이드 무함유 지방분해 칵테일, 특정 허가 품목 … | 병원 자체 메뉴명 — 아이디의원 슬리밍센터 등 개별 병원 메뉴명으로만 등장. 단일 제품/허가 품목 근거 없음. 구성 성분 미공개 | [1](https://search.naver.com/search.naver?query=팻킬주사) [2](https://search.naver.com/search.naver?query=팻킬주사+성분) |
| 메테로 | M2 | 한국비엔씨 필러로 기재됐으나 동명 제품 확인 불가 | 미상 — 구글·네이버 '메테로 필러'/'한국비엔씨 메테로' 결과 없음(커피 필터만). 한국비엔씨 필러 브랜드는 큐젤 확인. 오기 추정 | [1](https://thevc.kr/bnckorea) |
| 셀레스텔라 | M2 | (주)더에쓰씨가 공급하는 국산 HA 필러 브랜드(제품군에 깊은 주름용 'Deepte' 등) | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 출처: 네이버 검색 결과의 한청메디컬 KIMES2026 게시물·더에쓰씨 보도(시선뉴스 2026-05-21, 스포츠월드 2025-07-03). 제조사-공… | [1](https://hanchungmedical.com) [2](https://www.sportsworldi.com) |
| 아띠에르 | M2 | 메디톡스의 리도카인 함유 가교 히알루론산 필러(클래식·인텐시브·볼륨 3종) | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 국내 허가번호 웹 미확인 | [1](https://doctornow.co.kr/content/magazine/652f0fd9b95a4718b93d5f16757a10de) [2](https://theguru.co.kr/news/article.html?no=106579) |
| 앨리필 | M2 | 필러로 기재됐으나 동명 제품 확인 불가 | 미상 — 구글·네이버 검색에서 '앨리필/엘리필' 필러 결과 없음(애플필·윙크필 등 질필러만 노출). 오기 또는 병원 내부 명칭 추정 | — |
| 에피로크 | M2 | 필러로 기재됐으나 동명 제품 확인 불가 | 미상 — 구글·네이버 검색에서 필러 관련 결과 0건. 오기(예: 에피티크 계열) 또는 병원 내부 명칭 추정 | — |
| 유스필 | M2 | 알에프바이오의 가교 히알루론산 필러 브랜드 | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 2021-04 '유스필 쉐입 위드 리도카인' CE 획득 기사 확인. 국내 허가번호 미확인. 알에프바이오는 엑세스바이오가 인수 | [1](https://core.asiae.co.kr/article/2021041314524851619) [2](https://www.etoday.co.kr/news/view/1901593) |
| 큐젤 | M2 | 한국비엔씨의 가교 히알루론산 필러 브랜드(2011년 출시) | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 국내 유통은 대한뉴팜과 독점판매 계약 기사 있음. 허가번호 미확인 | [1](https://thevc.kr/bnckorea) [2](https://www.etoday.co.kr/news/view/1485238) |
| 큐젤MAX | M2 | 한국비엔씨 큐젤 HA 필러의 대입자(볼륨) 라인 | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 모델명 세부는 이전 패스 결과 기반, 이번 패스에서 추가 확인 못함 | [1](https://thevc.kr/bnckorea) |
| 하모니카 | M2 | 엘러간(애브비)의 HA+칼슘하이드록시아파타이트(CaHA) 하이브리드 주입제(콜라겐 스티뮬레이터) | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 국내 기사(뉴스더보이스 2026-04-22, 메디컬투데이 2026-02-12, 유진투자증권 2026-09-01 리포트)에서 엘러간 '하모니카'를 래디어… | [1](https://www.newsthevoice.com) [2](https://www.mdtoday.co.kr) |
| HArmonyCa | M3 | 하모니카와 동일 — 엘러간(애브비) HA+CaHA 하이브리드 주입제 | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — id auto-M2-1775360655397(하모니카)와 같은 제품 | [1](https://www.newsthevoice.com) [2](https://www.mdtoday.co.kr) |
| 고우리 | M3 | 덱스레보의 완전 액상화 PCL(폴리카프로락톤) 콜라겐 스티뮬레이터 주사(4등급 의료기기) | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 서울신문 2026-09-22: CE·호주·싱가포르·대만 허가에 이어 국내 식약처 허가 받아 유통 중. 더벨 2024-11-01: 2024-07 식약처 … | [1](https://www.seoul.co.kr) [2](https://www.thebell.co.kr) |
| 도프ECM | M3 | 도프(DOF Inc.)의 인체조직(무세포동종진피) 기반 ECM 스킨부스터 — 인체조직 가공품 | 미상 — 도프는 초임계 공정 기반 이식용 인체조직·조직유래 제품 회사. ECM 스킨부스터는 인체조직으로 분류돼 의료기기 품목허가 비대상 → MFDS 의료기기 DB 매칭 어려움. 'ECM'은 병원 표기, 정식… | [1](https://www.imcas.com/zh/sponsor/imcas-asia-2025/view/17375) [2](https://m.dailypharm.com/user/news/338957) |
| 라풀렌 | M3 | 삼양홀딩스 바이오팜이 개발한 PCL 마이크로스피어 필러(2022년 출시) | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 인사이트코리아 2026-05-06 태국 론칭 기사. 바이오팜 사업은 삼양홀딩스에서 분할(삼양바이오팜)됐을 수 있어 현재 허가 명의 확인 필요. 허가번호… | [1](https://www.insightkorea.co.kr) [2](https://www.etoday.co.kr) |
| 레티젠 | M3 | 한국파비스제약의 순도 99.9% 제1형 아텔로콜라겐 콜라겐 사용 조직보충재(4등급) | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 영문 철자는 'Retigen'이 아니라 'LAETIGEN'(데일리팜 2026-06-01·07-07, 메디칼타임즈 2026-01-14). 2026-02 … | [1](https://www.dailypharm.com) [2](https://www.donga.com) |
| 리투오파인 | M3 | 엘앤씨바이오의 무세포동종진피(hADM) 기반 ECM 스킨부스터 '리투오'의 소입자 버전 | 미상 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — hADM 제품은 '인체조직안전 및 관리 등에 관한 법률'의 인체조직으로 관리될 가능성이 높아 식약처 의료기기 DB에 없을 수 있음(추정). 라인업: 리… | [1](https://biz.chosun.com) [2](https://www.hitnews.co.kr) |
| 린피니 | M3 | 콜라겐부스터로 기재됐으나 동명 제품 확인 불가 | 미상 — 네이버 '린피니 콜라겐/주사' 결과는 문구(델리 린피니 파일)만. 오기(예: 리투오파인 등) 또는 병원 메뉴명 추정 | — |
| 미라콜 | M3 | 대화제약의 고순도 아텔로콜라겐 콜라겐 사용 조직보충재(4등급, 2024-11 출시) | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 메디소비자뉴스·히트뉴스 2024-11-04 출시 기사. 광고심의필 52025-I10-04-0377 표기(허가번호 아님). 퓨어녹스의 maker_hint… | [1](https://www.medisobizanews.com) [2](https://www.richdoc.co.kr) |
| 셀르디엠 | M3 | 한스바이오메드의 무세포동종진피(hADM) 기반 ECM 스킨부스터(2025-09 출시) | 미상 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — maker_hint '한스바이오파마'는 한스바이오메드. 디지털타임스 2026-08-31 'CellREDM™' 표기. hADM은 인체조직으로 관리될 가능… | [1](https://www.dt.co.kr) [2](https://www.medipana.com) |
| 아디떼 | M3 | ECM 동종진피(무세포동종진피) 주사형 스킨부스터 — 인체조직 가공품 | 미상 — 병원 이벤트 페이지에 'ECM동종진피 아디떼 5CC'로만 노출. 인체조직 계열은 의료기기 품목허가 대상 아님 → MFDS 의료기기 DB에 없을 가능성 높음 | [1](https://www.gangnamunni.com/events/157779) [2](https://news.bizwatch.co.kr/article/healthcare/2026/10/16/0017) |
| 쥬베룩볼륨 | M3 | 바임의 PDLLA+HA 콜라겐 스티뮬레이터 '쥬베룩'의 볼륨(꺼짐·팔자주름)용 라인 | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 딜사이트 2025-10-22: 쥬베룩 볼륨 '이칭 레니스나' — 허가 모델명으로 Lenisna가 쓰였을 가능성. 2026-09 '쥬베룩 볼륨 100' … | [1](https://dealsite.co.kr) [2](https://www.medicaltimes.com) |
| 쥬브아셀 | M3 | 무세포동종진피(hADM) 기반 ECM 스킨부스터(인체조직 가공품) — 의료기기 품목허가 대상이 아닌 인체조직… | 미상 — ECM 스킨부스터는 인체조직(조직은행 관리)으로 분류되어 식약처 의료기기 품목허가 심사를 거치지 않음(비즈워치 2026-10-16). MFDS 의료기기 DB에 없을 가능성 높음 → 인체조직안전관리 … | [1](https://www.gangnamunni.com/events/149150) [2](https://dailypharm.com/user/news/341769) |
| 콜라겐핀 | M3 | 콜라겐부스터로 기재됐으나 동명 제품 확인 불가 | 미상 — 네이버 '콜라겐핀 주사' 결과 0건, '콜라겐핀'은 식품 광고만. 병원 자체 메뉴명 또는 오기 추정 | — |
| 콜라쥬 | M3 | 레겐보겐의 아텔로콜라겐(리얼 콜라겐) 주사 — 콜라겐 사용 조직보충재 | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 메디파나뉴스·라포르시안·데일리팜(2024-04-17), IT조선(2024-04-22) 총판 기사. 'CE 인증 획득' 언급. 영문 표기·허가번호 미확인 | [1](https://www.newsthevoice.com) [2](https://www.dailypharm.com) |
| ASCE+엑소좀 | M4 | 엑소코바이오의 인체지방줄기세포 배양액 추출물 + 장미줄기세포 엑소좀 함유 병의원용 스킨부스터 화장품(코스메슈… | 화장품 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 검색 요약 기준 '스킨부스터 화장품'. 모발용은 ASCE+ HRLV. MFDS 의료기기/의약품 DB 대상 아님 | [1](https://www.medicaltimes.com/Main/News/NewsView.html?ID=1149524) [2](https://medigatenews.com/news/3183086000) |
| NCTF 필로르가 | M4 | 비가교 HA + 비타민·아미노산 등 칵테일 메조테라피 스킨부스터(프랑스 Fillmed, 구 필로르가 메디컬) | 미상 — 국내 분류(의료기기/화장품) 원문 확인 못 함. 해외에선 CE 의료기기(Class III) | [1](https://medigatenews.com/news/2391991345) [2](https://www.ddgroup.com/facial-aesthetics/mesotherapy/600706--fillmed-nctf-135ha--ce) |
| SNP솔루션 | M4 | 실체 미확인 — 'SNP'는 국내 화장품 브랜드(에스앤피)로만 검색됨 | 미상 — 주사형 'SNP솔루션' 제품 없음. SNP 화장품 브랜드와 관련된 관리 프로그램이거나 병원 자체 메뉴명 추정 | [1](https://www.stylekorean.com/brands/95/snp/1010) |
| 드원셀 | M4 | 스킨부스터 메뉴명으로 보이나 실체 미확인 | 미상 — '드원셀' 검색 결과 없음. 병원 자체 메뉴명/화장품 추정 | — |
| 레나토S | M4 | 스킨부스터 제품/메뉴명으로 보이나 실체 미확인 | 미상 — 한·영('RENATO S') 검색에서 해당 제품 결과 없음. 병원 자체 메뉴명 또는 표기 오류 추정 | — |
| 리듐 | M4 | 스킨부스터 제품/메뉴명으로 보이나 실체 미확인 | 미상 — '리듐 스킨부스터' 검색에서 해당 제품 없음(리투오·리쥬란 등 유사명만). 표기 오류 또는 병원 메뉴명 추정 | — |
| 리쥬란HB+ | M4 | PN + 히알루론산 + 리도카인 복합 주사제(눈가 주름 개선 허가), 2021년 국내 허가 | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 데일리팜: 'PN과 HA를 피하에 주입해 성인 눈가 주름 개선' 목적으로 국내 허가, 2021 하반기 판매. 허가번호는 웹에서 원문 확인 못 함 | [1](https://m.dailypharm.com/user/news/49009) [2](https://m.dailypharm.com/newsView.html?ID=278928) |
| 리쥬란아이 | M4 | 연어 유래 PN(폴리뉴클레오티드) 주사제 중 눈가용 저점도 제품(리쥬란 라인) | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 허가번호 페이지 확인 못 함. 검색 요약에 리쥬란 힐러 '제허 14-825호'가 나왔으나 원문 페이지로 확인하지 못해 미기재. MFDS DB에서 파마리… | [1](https://www.beautetrade.com/products/rejuran-i/67461/) [2](https://reberryclinic.com/%EB%A6%AC%EC%A5%AC%EB%9E%80-%EC%B6%94%EC%B2%9C-%EC%84%9C%EC%9A%B8/) |
| 릴리이드M | M4 | 한국비엠아이 릴리이드 스킨부스터 라인 중 히알루론산나트륨(닭벼슬 유래) 주성분 제품 — 나머지 C/W/A/H… | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 분류(의료기기/화장품) 원문 확인 못 함 — category는 주사형 HA 스킨부스터라 의료기기 추정. 릴리이드 W는 알부틴 함유라고 해 라인 일부가 … | [1](https://doctornow.co.kr/content/magazine/a753410ddebe4e9995cae9510005149c) [2](https://m.dailypharm.com/user/news/48133) |
| 바이리즌 | M4 | 휴젤의 프리미엄 필러 브랜드 바이리즌의 첫 제품 — 고농도 가교 HA 스킨부스터(2022-01 출시) | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 영문 브랜드 'BYRYZN' 확인. maker_hint의 'PCL'은 근거 없음(HA). 허가번호 웹 미확인 — 휴젤 HA 필러(더채움 계열) 허가의 … | [1](https://dailypharm.com/user/news/43407) [2](https://dailypharm.com/user/news/6345) |
| 사이토케어 | M4 | 프랑스 Revitacare의 비가교 HA + 비타민·아미노산·미네랄 칵테일 메조테라피 스킨부스터(해외 Cla… | 미상 — 국내 수입사·허가 웹 확인 못 함 | [1](https://lindtest.quickbutik.com/mesoterapi/cytocare-532-10x5ml-vials) [2](https://www.prnewswire.co.uk/news-releases/groupe-sebbin-announces-agreement-with-revitacare-to-distribute-their-products-in-european-countries-650596233.html) |
| 셀엑소좀 | M4 | 프로스테믹스 줄기세포배양액(AAPE) + 식물유래 엑소좀 스킨부스터(바르는 병의원용 화장품 계열 추정) | 화장품 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 기사에 화장품/의료기기 분류 명시 없음 — AAPE·엑소좀 원료 특성상 화장품 추정(단정 아님) | [1](https://kormedi.com/1311313/) [2](https://www.hankyung.com/article/202606257940P) |
| 소노PDRN | M4 | PDRN(연어 DNA 유래) 스킨부스터 — '소노'가 붙은 특정 제품 미확인 | 미상 — '소노 PDRN' 제품 검색 결과 없음. PDRN 일반 시술명에 병원/브랜드 접두어를 붙인 메뉴명 추정(generic PDRN 주사) | — |
| 스네일샷 | M4 | 달팽이 점액 계열로 보이는 스킨부스터 메뉴명 — 실체 미확인 | 미상 — 주사형 '스네일샷' 의료기기 검색 결과 없음. 유사명은 VT코스메틱 '스네일 리들샷 100B'(화장품 앰플)뿐 → 화장품 또는 병원 자체 메뉴명 추정 | [1](https://www.stylekorean.com/product/snail-reedle-shot-100b-50ml/1739410815) |
| 엑소힐러 | M4 | 엑소좀 계열 스킨부스터 시술(병원 이벤트명) — 제조사·제품 실체 미확인 | 미상 — 병원 이벤트 페이지에만 '엑소힐러' 시술로 노출, 제조사·성분 미기재. 엑소좀 화장품 계열 또는 병원 메뉴명 추정 | [1](https://www.gangnamunni.com/events/152170) [2](https://www.gangnamunni.com/events/55455) |
| 인에이블 | M4 | 동국제약의 섬유아세포 엑소좀·FGF·콜라겐 함유 2제형(분말+액상 1바이알) 스킨부스터 — 주름개선 기능성 … | 화장품 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 2023-07 동국제약 출시. maker_hint의 'LG화학'은 웹 근거 없음(LG화학 스킨부스터는 비알팜 PN '비타란'). 화장품이라 MFDS 의… | [1](https://news.bizwatch.co.kr/article/mobile/2023/10/04/0034) [2](https://medigatenews.com/news/865623860) |
| 카탈리스트 | M4 | 스킨부스터 메뉴명으로 보이나 실체 미확인 | 미상 — '카탈리스트 스킨부스터' 한국어 검색에서 해당 제품 결과 없음. 병원 자체 메뉴명 또는 화장품 추정 | — |
| 투 (TU) | M4 | 스킨부스터 메뉴명으로 보이나 실체 미확인 | 미상 — '투(TU)' 스킨부스터 한·영 검색 결과 없음. 이름이 너무 짧아 식별 불가 — 병원 자체 메뉴명/약칭 추정 | — |
| 프로파일로 | M4 | IBSA의 고농도 하이브리드(고·저분자 HA 열안정화 복합체) 스킨부스터, 유럽 CE | 미상 — 국내 수입사·식약처 허가 웹에서 확인 못 함. IBSA 라이선싱 페이지가 한국을 파트너 물색 대상 시장으로 언급 → 국내 정식 허가 없을 가능성(병행/미허가) 있음, 단정 불가 | [1](https://businessdevelopment.ibsagroup.com/?p=42894) [2](https://aestheticsjournal.com/news/ibsa-derma-expands-into-australia-and-new-zealand/) |
| 필로르가135HA | M4 | NCTF 135HA(필메드/구 필로르가 메디컬) — 'NCTF 필로르가'와 동일 제품 | 미상 — 국내 분류·허가번호 원문 확인 못 함 | [1](https://medigatenews.com/news/2391991345) |
| 힐로웨이브 | M4 | 프랑스산 이중분자량 히알루론산 기반 바이오스티뮬레이터 스킨부스터, 식약처 4등급 의료기기 | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 허가번호 웹 미확인. MFDS 조회 시 업체명 '하이어코퍼레이션'으로 | [1](https://www.smarttoday.co.kr/ko-kr/articles/79173) [2](https://macaubusiness.com/scie-study-shows-hilo-wave-promotes-regenerative-skin-remodeling-without-inflammatory-response/) |
| N코그 | M7 | 3세대 몰딩형 멀티 PDO 코그실 '엔코그(N-Cog)' | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 엔파인더스(주)는 PDO 봉합사 제조사로 '2013년 식약처 허가 취득'·특허 가시 패턴 보유를 자사 페이지에 기재하나, 'N-COG' 제품명을 그 페… | [1](https://nfinders.com/product_pdo-thread/) [2](https://www.kaas.ne.kr/comm/comm_04_view2.html?c_idx=3&idx=75) |
| V리프트 | M7 | 울트라브이의 PDO 흡수성 리프팅 실 '울트라 V리프트'로 추정(일반 V라인 실리프팅 메뉴명일 수도 있음) | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 울트라브이(2011/2012 설립, 권한진 대표)가 '울트라 브이리프트' 상표로 4등급 PDO 허가를 받았다고 기업소개에 기재. 원장부 'V리프트'가 … | [1](https://app.rndcircle.io/company/b325ecb4-0386-52a5-9538-ba057f3086bb) [2](https://www.jobkorea.co.kr/company/16153907) |
| 레보실 | M7 | 확인 불가 — 실리프팅 제품으로 검색되지 않음 | 미상 — 네이버 검색 시 '레보실정'(의약품 정제)만 나오고 리프팅 실 결과 없음. 병원 자체 메뉴명 또는 오기 추정 | — |
| 로즈실 | M7 | 휴젤 흡수성 리프팅 실 '블루로즈'의 약칭으로 추정 | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — '로즈실'로 검색 시 블루로즈 실리프팅(휴젤사 흡수성 리프팅 실)만 나옴. 원장부 약칭으로 판단하나 병원 확인 필요 | [1](https://artis1.co.kr/blueroselift) |
| 리드파인 | M7 | 확인 불가 — 실리프팅 제품·시술명으로 검색되는 자료 없음 | 미상 — 네이버 통합/블로그 검색에서 '리드파인' 실/리프팅 제품 결과 없음. '리드(LEAD) 풀페이스' 같은 병원 메뉴 접두어와 '파인'의 조합인 병원 자체 메뉴명이거나 오기일 가능성 | — |
| 면사리프트 | M7 | 확인 불가 — 병원 자체 실리프팅 메뉴명으로 추정 | 병원 자체 메뉴명 — 네이버 검색 시 뜨개질용 '면사' 상품만 나옴. 리프팅 실 제품 근거 없음 | — |
| 몰드리프트 | M7 | 몰딩(Mold) 방식으로 돌기를 성형한 코그실을 쓰는 실리프팅의 일반 명칭으로 추정 | 일반 시술명 — '몰드리프트' 이름의 실 제품은 검색되지 않음(속옷 상품만 나옴). PDO 실 구조 분류(모노·스크류·코그·몰드·멀티) 중 '몰드'를 붙인 병원 메뉴명으로 판단. 민트리프트·업투유 3D 몰드 메쉬 … | — |
| 미스코 | M7 | 코 실리프팅(코에 돌기 있는 PDO/PCL 실 삽입) 시술의 통칭 중 하나 | 병원 자체 메뉴명 — 하이코·바비코·엣지코·미스코 등은 병원/제조사가 붙인 코 실리프팅 시술 명칭(지식iN 의사 답변). 특정 제품·제조사 연결 근거 못 찾음 | [1](https://search.naver.com/search.naver?query=%EB%AF%B8%EC%8A%A4%EC%BD%94+%EC%8B%A4%EB%A6%AC%ED%94%84%ED%8C%85) [2](https://www.kaas.ne.kr/comm/comm_04_view2.html?c_idx=3&idx=75) |
| 블루로즈클레어 | M7 | 휴젤 미용 흡수성 봉합사 '블루로즈' 라인의 PCL(폴리카프로락톤) 타입 리프팅 실 | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 나무위키·휴젤 보도: PDO 타입 '블루로즈 포르테·멀티·더블암'에 이어 PCL 타입 '블루로즈 클레어' 출시. 휴젤 종속회사 '제이월드'가 실 제조사… | [1](https://www.hugel-inc.com/) [2](https://namu.wiki/w/%ED%9C%B4%EC%A0%A4) |
| 실루엣소프트 | M7 | PLLA/PLGA 콘(Cone)이 달린 흡수성 양방향 리프팅 실(Sinclair 제조, 수입품) | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 싱클레어 코리아가 '실루엣소프트 SILK 세미나'(2023) 개최 — 국내 공급 주체로 판단. MFDS 수입허가는 싱클레어코리아 명의일 가능성 높으나 … | [1](https://sinclairkorea.co.kr/news/) |
| 앵커리프트 | M7 | 실을 고정점(앵커)에 걸어 당기는 방식의 실리프팅을 부르는 병원 메뉴명으로 추정 | 병원 자체 메뉴명 — 네이버 검색에서 '앵커리프트' 이름의 실 제품·제조사 결과 없음. 일반 시술명/병원 메뉴명으로 판단 | — |
| 엘리실 | M7 | 확인 불가 — 실리프팅 제품으로 검색되지 않음 | 미상 — 네이버 검색 시 시세이도 화장품 '엘리실(ELIXIR)'만 나오고 리프팅 실 결과 없음. 병원 메뉴명 또는 '엘라스티(동방메디컬)' 등의 오기 가능성 | — |
| 오메가리프트 | M7 | 오메가(Ω) 형태 구조의 PDO 녹는 실 '오메가 브이' 계열로 추정 — 병원 메뉴명 '오메가 실리프팅' | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 메디칼바이 쇼핑몰에 '[리프팅실 PDO녹는실] 오메가 브이 리틀, 제조사 (주)오브이월드'. 여러 병원이 '오메가 리프트/오메가 코그 실리프팅'을 메뉴… | [1](https://mielclinic.com/33) [2](https://www.beauty-eye.com/) |
| 울트라V | M7 | 울트라브이의 PDO/PCL 흡수성 리프팅 실 브랜드 '울트라 V(리프트)' | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 기업소개: 2012년 국내 최초 PDO 리프팅 식약처 허가(4등급) 획득, PDO·PCL 봉합사, Ultra V 브랜드. 허가번호는 페이지에서 확인 못… | [1](https://www.jobkorea.co.kr/company/16153907) [2](https://app.rndcircle.io/company/b325ecb4-0386-52a5-9538-ba057f3086bb) |
| 잼버실 | M7 | 스프링(코일) 형태의 PDO 봉합사 — 볼륨·리프팅용 실(잼버 시리즈) | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 이전 패스의 '일반 시술명' 판정은 틀림. 네오닥터(2002 설립)가 세계 최초 스프링형 PDO 봉합사 '잼버(JAMBER)' 시리즈를 개발·제조. '… | [1](https://app.rndcircle.io/company/1b0a0278-8d19-5f95-8ff9-9ffbad48eee1) [2](https://abijouonline.com/%EC%A0%AC%EB%B2%84%EB%A6%AC%ED%94%84%ED%8C%85-%EC%B2%AD%EB%9F%89%EB%A6%AC-%EA%B0%80%EA%B2%A9) |
| 캐번실 | M7 | 빈틈없이 감은 스프링 형태의 PDO 녹는 실(볼륨·리프팅용) '캐번' — 잼버의 전신 제품 | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 의학신문(2023.03.24) '실 리프팅계 패러다임 바꾼 잼버' 기사: 네오닥터가 '캐번의 업그레이드 버전'으로 잼버(JAMBER)를 출시. 이전 패… | [1](https://www.bosa.co.kr/) [2](https://www.thewalts.co.kr/) |
| 코그실루프 | M7 | 코그실을 루프(고리) 형태로 거는 실리프팅 방식을 부르는 병원 메뉴명으로 추정 | 병원 자체 메뉴명 — 네이버 검색에서 '코그실루프' 제품/제조사 결과 없음. '코그실 + 루프' 조합의 병원 자체 명칭으로 판단 | — |
| 테스리프트 | M7 | PDO 코그실에 3차원 메쉬 구조를 결합한 하이브리드 리프팅 실(캐뉼라 장착형) | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — (주)테스리프트는 2008년 설립, 강원 원주 생산. KMDF 인체이식형 의료기기 업체목록에 '주식회사 테스리프트' 제조업으로 등재. maker_hin… | [1](https://app.rndcircle.io/company/bfd2c137-66e3-5b34-864d-97736b23fab9) [2](https://www.onreyoung.com/products/24063) |
| 텐선실 | M7 | 확인 불가 — '텐션(tension)실' 류 병원 자체 메뉴명으로 추정 | 병원 자체 메뉴명 — 네이버 '텐선실 리프팅' 검색결과 없음 | — |
| 투와이실 | M7 | 확인 불가 — 병원 자체 실리프팅 메뉴명으로 추정 | 병원 자체 메뉴명 — 네이버 '투와이실 리프팅' 검색결과 없음. 제품명 근거 없음 | — |
| 프린스리프트 | M7 | 확인 불가 — 병원(예: 프린스성형외과) 자체 리프팅 메뉴명으로 추정 | 병원 자체 메뉴명 — 네이버 검색에서 '프린스리프트' 실 제품 결과 없음. '프린스 성형외과' 등 병원명만 나옴 | — |
| 해피리프트 | M7 | 러시아 Sulamanidze 박사가 개발한 아프토스(APTOS) 실 리프팅의 국내 통칭(러시안 리프트) | 병원 자체 메뉴명 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 병원 페이지: '해피리프트(러시안 리프트, 아프토스)는 러시아 슐라마니쯔 박사가 개발한 실 리프팅', '해피리프팅은 특수 실(Aptos threads)… | [1](https://www.gpmedi.com/) [2](http://cleoder.co.kr/Module/CMS/CMS.asp?Srno=34470&ContentsSrno=9439) |
| 허니콤실 | M7 | 확인 불가 — 벌집(honeycomb) 형태로 실을 교차 삽입하는 시술의 병원 메뉴명으로 추정 | 병원 자체 메뉴명 — 네이버 '허니콤실 리프팅' 검색결과 없음 | — |
| 로제라이트 | M8 | 미확인 — 홍조(로제이시아)용 광치료 메뉴명으로 추정 | 미상 — '로제라이트/RoseLight' 의료기기 웹 미검출. 병원 자체 메뉴명 추정 | — |
| 리레이저 | M8 | 미확인 레이저 명칭 | 미상 — '리레이저/ReLaser' 미용 의료기기 웹 미검출(산업용 Relaser만 나옴). 병원 자체 메뉴명 또는 오기 추정 | — |
| 리팟 | M8 | 클래시스 532nm Q스위치 Nd:YAG 색소 레이저(VSLS 냉각·압박 기술) | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 원 개발사는 이루다(ILOODA)로 알려짐, 합병 후 클래시스 | [1](https://classys.com/product_category/pigmentation) [2](https://www.venturesquare.net/897786/embed) |
| 바이탈라이즈 | M8 | 미확인 — 레이저 장비명 아님 가능성(SkinMedica 'Vitalize Peel' 필링 등) | 미상 — '바이탈라이즈/Vitalize' 레이저 의료기기 웹 미검출. 병원 자체 메뉴명 또는 필링제 명칭 추정 | — |
| 셀렉V | M8 | 제이시스메디칼 IPL(500~900nm) 필터교체형 광치료기 | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 이번 패스 추가 확인 없음, prev_web 기준 | — |
| 슬렌더엑스 | M8 | 사이노슈어/루트로닉 계열 바디(지방) 기기로 추정, 제품명 미확인 | 미상 — '슬렌더엑스/SlenderX' 의료기기 웹 미검출. Cynosure 바디 레이저는 SculpSure(스컬프슈어, 국내 승인 보도 있음). 병원 자체 메뉴명 또는 다른 제품 추정 | [1](https://www.biospace.com/cynosure-receives-approval-to-market-sculpsure-in-south-korea) |
| 아발란체 | M8 | 포토나 알렉산드라이트755+Nd:YAG1064 제모 레이저 플랫폼 | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — FDA K223540(2023-01). 국내 수입사·루트로닉 관계 미확인 | [1](https://510k.innolitics.com/device/K223540) [2](https://simplebooklet.com/fotonaavalanchelase?textonly=1) |
| 클리어앤브릴리언트 | M8 | 솔타메디칼 1440/1927nm 저출력 비박피 프랙셔널 다이오드 레이저 | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 국내 수입사 미확인 | [1](https://www.barchart.com/story/news/361623/bausch-health-s-aesthetics-business-solta-medical-announces-the-launch-of-clear-brilliant-touch-laser-in-canada) |
| 트루피코 | M8 | 피코초 레이저 계열 명칭으로 추정, 실제 제품 미확인 | 미상 — '트루피코/TruPico' 의료기기 웹 미검출. 병원 자체 메뉴명(피코토닝 브랜딩) 가능성 | — |
| 트리니티 | M8 | 블루코어컴퍼니 3파장(755/808/1064nm) 다이오드 레이저(제모) — 동명 제품 Syneron eTw… | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — maker_hint 없음 → 동명 다른 장비(Syneron Trinity: elos+Matrix IR 조합 플랫폼, 과거 국내 리프팅 '트리니티') 가… | [1](http://www.bluecorecompany.com) [2](https://www.businesswire.com/news/home/20260605526149/en/Laser-Treatments-Have-Long-Excluded-Patients-with-Darker-Skin-New-Korean-Technology-Is-Changing-the-Industry) |
| 포토나스타발브 | M8 | 포토나 '스타워커(StarWalker)' 오기로 추정 | 미상 — 포토나 제품군에 '스타발브' 없음(StarWalker/TimeWalker/SP Dynamis 등). 같은 배치 '스타워커'와 중복 항목일 가능성 | [1](https://www.praiston.pl/en/catalog/view/12916/fotona-starwalker-m031-3a2-maqx-laser) |
| 피코케어 | M8 | 원텍의 피코초 Nd:YAG(1064/532nm) 색소·문신 제거 레이저 '피코케어(450)' | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 이헬스통신·코넥스협회(2016.10.31): 원텍 'PICOCARE 450' 식약처 허가 취득(국내 최초 450 picosecond). 보건신문(202… | [1](https://www.e-healthnews.com/) [2](https://www.konex.or.kr/) |
| 피코코어 | M8 | 피코초 레이저로 추정되나 '피코코어'라는 제품명은 확인 못 함 | 미상 — 웹에서 '피코코어/PicoCore' 의료기기 미검출. 후보: 블루코어컴퍼니 PICORE(피코어, 450ps Nd:YAG) 오기, 또는 루트로닉 PicoPlus(피코플러스)/원텍 PicoCare(피코… | [1](http://www.bluecorecompany.com) [2](https://www.hankyung.com/amp/2017051620496) |
| 리니어펌 | M9 | 제이시스메디칼 HIFU 리프팅 기기(2017 출시, 해외명 ULTRAcel Q+) | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 후속 리니어지(LinearZ). 식약처 모델명은 ULTRAcel Q+ 계열일 가능성 | [1](https://www.smarttoday.co.kr/ko-kr/articles/38567) [2](https://dailypharm.com/user/news/16525) |
| 리저브 | M9 | 리프팅 그룹 항목이나 '리저브'라는 장비/제품 확인 안 됨 | 미상 — 한/영(Reserve) 검색에서 리프팅 장비 결과 없음. 병원 자체 메뉴명 또는 표기 오류 추정 | — |
| 바이캐빈 | M9 | 리프팅 그룹 항목이나 '바이캐빈' 장비 확인 안 됨 | 미상 — 한국어 검색 결과 없음. '바이(Bi-)'+'캐빈/캐비테이션' 계열 바디 장비 또는 병원 자체 메뉴명 추정 | — |
| 시크릿맥스 | M9 | 이루다(현 클래시스 계열)의 마이크로니들 고주파(RF) 장비, 시크릿 RF 상위 모델 | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 2024-05-21 식약처 허가 취득 기사. 허가번호 미기재. 참고: 시크릿 RF 제허 11-1071 호(클래시스 페이지) | [1](https://www.bosa.co.kr/news/articleView.html?idxno=2223124) [2](https://www.pharmnews.com/news/articleView.html?idxno=244396) |
| 아큐어 | M9 | 후보: Accure(아큐어) 1726nm 여드름(피지선) 레이저 — 단 리프팅 그룹과 불일치 | 미상 — 리프팅 장비 '아큐어' 검색 결과 없음. 동명 해외 여드름 레이저만 확인되고 국내 도입·허가 정보 없음 | [1](https://schweigerderm.com/cosmetic-dermatology/laser-treatments/accure-laser) [2](https://pubmed.ncbi.nlm.nih.gov/37328000/) |
| 아폴로 | M9 | 후보: 폴로젠(Pollogen, 루메니스 계열) TriPollar Apollo 멀티폴라 RF 장비 | 미상 — 국내 '아폴로' 리프팅 장비 도입·허가 페이지 미확인. 동명 해외 RF 장비만 확인되어 동일 여부 미확정 | [1](https://healthmanagement.org/products/view/aesthetic-medicine-radiofrequency-generator-apollo-pollogen) [2](https://www.theaestheticguide.com/energy-based-devices-treatments/apollo-duet-offers-physicians-versatility-with-noticeable-results) |
| 에브넥 | M9 | 리프팅 그룹 항목이나 '에브넥' 장비 확인 안 됨 | 미상 — 검색 결과 없음. 목(neck) 리프팅 병원 메뉴명 또는 표기 오류 추정 | — |
| 에이전 | M9 | 제이시스메디칼 관련 리프팅 장비로 기재되었으나 해당 제품명 확인 안 됨 | 미상 — 제이시스 공식 사이트 제품군(DENSITY, POTENZA, LinearZ, D'Liv, Cellec V, TRI-BEAM, Edge ONE)에 '에이전/AGEN' 없음. 검색 결과 없음. 아그네스… | [1](https://www.jeisys.com/) |
| 울트라셀Q+ | M9 | 제이시스메디칼의 선형샷 HIFU(집속초음파) 리프팅·지방감소 장비 | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 식약처 품목허가 획득 언급은 있으나 허가번호 미확인. 품목명은 추정 | [1](https://dotmed.com/listing/cosmetic-general/jeisys/ultracel-q/ultrasound-stimulator-hifu-q/4891085) [2](https://www.jeisys.com/uploaded/board/ir_data/_fab08d2fbc2ec29f570f1dc9da7e617c1.pdf) |
| 쿨소닉 | M9 | 아스테라시스 냉각(ACC) 일체형 HIFU 리프팅 기기, 2025-02 식약처 승인 | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 허가번호는 출처에서 확인 못 함 | [1](https://file.alphasquare.co.kr/media/pdfs/company-ir/20250210아스테라시스_차세대_HIFU_‘쿨소닉’_식약처_승인_획득…연내_FDA_목표.pdf) [2](https://view.asiae.co.kr/en/article/2026082008111739927) |
| 클래리파이 | M9 | 리프팅 그룹 항목이나 '클래리파이' 장비 확인 안 됨 | 미상 — 검색 시 미국 Clarify Medical 가정용 UVB 광선치료기만 나옴(리프팅 아님). 병원 자체 메뉴명 추정 | — |
| 트릴리프트 | M9 | 루메니스의 얼굴·바디 근육자극(DMSt)+RF 리프팅 장비 triLift | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 국내 허가·수입사 페이지 미확인. 품목명은 개인용저주파자극기/저주파자극기류 가능성 | [1](https://business.shapescale.com/content/posts/lumenis-trilift-guide) [2](https://www.americanspa.com/technology/lumenis-unveils-next-gen-dmst-powered-device-trilift-20) |
| 포커스듀얼 | M9 | 은성글로벌의 마이크로니들 고주파(RF)+HIFU 결합 리프팅 장비 | 의료기기 — 웹으로 찾음, 식약처에 이름 든 허가 없음 — 기사에 국내 KFDA 허가 획득 언급, 허가번호 미기재. RF+HIFU 복합이라 품목명이 두 개(집속형초음파자극시스템/범용전기수술기)일 수 있음 | [1](https://www.venturesquare.net/932516/) [2](https://lynton.co.uk/wp-content/uploads/2020/12/Focus-Dual-Brochure.pdf) |
| 하이푸니 | M9 | HIFU(하이푸) 리프팅을 지칭하는 병원 자체 메뉴명 추정 | 병원 자체 메뉴명 — '하이푸니'라는 제품명 웹 검색 결과 없음(한/영 'HIFUNI' 포함). '하이푸'(HIFU, 집속초음파)의 애칭형 병원 메뉴명으로 추정 | — |

## ④ 바뀐 것 (v3 → v4)

| 게이트 분류 v3 → v4 | 건수 |
|---|---|
| auto→auto | 45 |
| line→line | 60 |
| name_diff_co→name_diff_co | 42 |
| no_service→no_service | 45 |
| unconfirmed→auto | 7 |
| unconfirmed→license_match | 1 |
| unconfirmed→line | 8 |
| unconfirmed→name_diff_co | 3 |
| unconfirmed→name_family_only | 1 |
| unconfirmed→unconfirmed | 128 |

웹 조사 구분(172): not_found 42 · 의약품 2 · 의료기기 86 · 미상 14 · 화장품 4 · 병원 자체 메뉴명 12 · 일반 시술명 3 · 단종 3 · 미용기기(비의료) 6

## ⑤ 미결 · 원장 표기 수정 후보(사람 확인)

- 같은 허가가 원장 두 제품에 걸림: 에이비오톡신(4차 자동 → 디스포트주 · 입센코리아) = 원장 디스포트. 「에이비오」는 실제 업체가 아니고 abobotulinumtoxinA(디스포트 성분) 음역으로 본 것은 웹 추정 — 두 제품을 하나로 합칠지 게이트에서
- 같은 제품 중복(원장 정리 후보): NCTF 필로르가 = 필로르가135HA · 하모니카 = HArmonyCa · 울트라V ≈ V리프트(울트라브이 Ultra V Lift) · 잼버실 ↔ 캐번실(캐번 후속이 잼버, 네오닥터) · 스타워커 ↔ 포토나스타발브(포토나에 스타발브 없음) · 피코라이트블랙 ↔ 피코 라이트(DEV-060/061 같은 수도그룹 PICOLITE 로 판단, 중간 확신)
- 원장 업체 표기가 웹과 다름: 인에이블 = 동국제약 화장품(LG화학 아님) · 바이리즌 = HA(BYRYZN, PCL 아님) · 테스리프트 = (주)테스리프트(리젠바이오텍 관계 미확인) · 셀르디엠 = 한스바이오메드(한스바이오파마 아님) · 퓨어녹스의 「대화제약」은 미라콜(대화제약 콜라겐)에서 섞인 것으로 보임 · 벨피엔 프로 = 정식 표기 밸피엔(휴메딕스), 「프로」 라인 미확인 · 리투오파인 = 엘앤씨바이오(휴메딕스 아님)
- 시술군이 틀린 원장 제품: 소노퀸(HIFU) · 올타이트(RF) — 메디컬스킨케어가 아니라 기기 리프팅
- 일반 시술명 → 제품으로 바뀐 것: 잼버실 · 캐번실(네오닥터 JAMBER · CAVERN) — 3차 「일반 시술명」 판정 정정
- 인체조직(의료기기 아님 추정): 리투오파인 · 셀르디엠 · 쥬브아셀 · 아디떼 · 도프ECM — hADM/ECM 은 인체조직법 관리 가능성. 식약처 의료기기 DB 대신 인체조직 허가로 확인해야(이 MCP 범위 밖)
- 화장품 · 미용기기(허가 대상 아님 후보, 게이트에서 「허가 대상 아님」으로 옮길지): 인에이블 · ASCE+엑소좀 · 셀엑소좀(추정) · 옥시덤(멍크림) · 노보젯(제조사 IR 이 미용기기라고 함) · 신규 현장 기기 벨르업 · 수소토닝 · 힐퓨전프로 · 크라이오 멀티마스터 · 울킨(제조사가 의료기기 아님 명시) · 오투덤
- 단종 · 철수: 카이벨라(국내 판매명 벨카이라주, 앨러간 철수로 허가 취하 — 웹) · E-MAX(시네론 구모델) · 아큐토닝(판매 단종, 케이엘글로벌 ACCUTONING 허가는 정상으로 남아 있음)
- 웹 허가번호 일치 1: 더마샤인 — 중고 판매 블로그의 「제인 16-4944호」가 식약처 Panace-DS 허가(휴온스메디텍)와 같다. 이름(더마샤인)은 공식명에 없어 자동 아님
- 이름만 계열 일치라 자동에서 뺀 것: 라이트쉬어듀엣 → 식약처 LightSheer Desire 만 있음(DUET 없음) · 피코케어 → PICOCARE MAJESTY 만 이름에 걸림(PICOCARE 450 허가는 이름으로 안 잡힘)
- 신규 현장 기기 피부 분석기 4(3D 메타뷰 · 마크뷰 · 스캐나(정식 스케나) · 미라쥬): 메타뷰 · 마크뷰는 식약처 「체외형 의료용 카메라」 허가가 있다(피에스아이플러스) — 원장에 넣을지(시술 아님) 정할 것
- 웹 출처 중 일부는 네이버 검색 결과 URL(원 페이지 아님) — 게이트에서 출처를 열면 검색 결과가 뜬다
- 허가번호를 페이지에서 직접 본 것은 4건뿐(디스포트 품목기준코드 · 슈링크 유니버스 제인 21-831 · 볼뉴머 제허 22-512 · 더마샤인 제인 16-4944). 필러 · 스킨부스터 · 실은 식약처 모델명이 코드(M16-002 등)라 이름으로는 안 걸리고, 허가번호도 웹에 거의 없어 「허가 미확인」으로 남은 것이 많다

## ⑥ 기술 메모(v4)

- 각 대상 product · new_ledger_candidate 에 `web4`(category · what_is_it · official_ko/en · model_names · manufacturer · importer_kr · license_nos · sources · reason_if_not_found) · `match.r4`(gate_v3 · gate_v4 · license_no_match_keys) · 후보마다 `round: 4` · `via: web` · `name_contains_r4` · `license_no_match_web`
- 웹 자동 확정은 `match.auto_rule = web4(…)` · `match.auto_keys`. 업체 목록(ENTRPS · entp_name) 근거만 있는 후보는 이름 판정에 쓰지 않는다
- 웹 검색은 7개 병렬 조사로 나눠 했다. 일반 WebSearch 가 한국어 결과를 거의 못 줘서 일부는 네이버 검색 결과 URL 이 출처다(원 페이지 아님) — 그 행은 출처 확인이 필요하다
- 허가번호는 페이지에서 실제로 본 것만 적었다(검색 요약만 있는 것은 뺐다)

---

# v3 본문(그대로)

## ① 현장에서 쓰는 기기 76대 — 사진 판독 · 원장 · 식약처

사진 폴더 `1_더데이랩스_사용중`. 「사진에서 읽은 글자」는 사진에 실제로 보이는 로고 · 모델명만 적었다(파일명 아님).

| 사진 | 현장 이름 | 사진에서 읽은 글자 | 원장 제품 | 식약처 허가 (모델 · 업체 · 상태) | 어떻게 · 근거 |
|---|---|---|---|---|---|
| DEV-001 | 젠틀맥스프로플러스 | GentleMax Pro Plus / Candela | 젠틀맥스프로+ | GentleMaxi Pro Plus (알렉산드라이트 레이저 수술기) · 주식회사 밴스로컬 · 정상 | 검색어 든 허가 · 추측 |
| DEV-002 | 젠틀맥스프로 | GentleMax Pro / Candela | 젠틀맥스프로 | GentleMax Pro (엔디야그레이저수술기) · (주)신한씨스텍 · 취소 | 사진 모델명 든 허가 · 사진 · 추측 |
| DEV-003 | 아발란체 | Avalanche LXP | 아발란체 | PICOPLUS (엔디야그 레이저 수술기) · 주식회사 사이노슈어루트로닉테크놀로지 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 |
| DEV-004 | 클라리티2 | CLARITY II / Lutronic | 클라리티2 · 클라리티2 (혈관) | CLARITY II (엔디야그레이저수술기) · (주)루트로닉 · 정상 | **자동**(이름+업체 완전 일치) · Hub 영문명 · 사진 · 업체 목록 |
| DEV-005 | 아포지플러스 | Apogee / Cynosure | — 원장에 없음(②) | **못 찾음** | — |
| DEV-006 | 노블린 | Nobleen | 노블린 | Nobleen (알렉산드라이트레이저수술기) · 화인엠이씨(주) · 정상 | 사진 모델명 든 허가 · 사진 |
| DEV-007 | 아포지엘리트플러스 | Elite+ / Cynosure | 아포지엘리트플러스 | Elite iQ (알렉산드라이트레이저수술기) · (주)루트로닉 · 취소 | 사진 모델명 든 허가 · 사진 · 웹 · 업체 목록 |
| DEV-008 | 인모드 | InMode RF / InMode | 인모드 | InMode (반도체 레이저 수술기) · (주)신한네트웍스 · 정상 | 이름 든 허가 · 원천 이름 · Hub 영문명 · 사진 |
| DEV-009 | 써마지 | Thermage | 써마지FLX (써마지 ↔ 써마지FLX) | Thermage Deep Skin외 4건 (범용전기수술기) · (주)피에이치 · 정상 | 사진 모델명 든 허가 · 사진 |
| DEV-010 | 올리지오X | Oligio X | 올리지오X | Oligio X (범용전기수술기) · 원텍(주) · 정상 | 사진 모델명 든 허가 · 사진 |
| DEV-011 | 리니어펌 | LinearFirm / Jeisys | 리니어펌 | COTENZA (범용 전기 수술기) · (주)제이시스메디칼 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 |
| DEV-012 | 소프웨이브 | Sofwave | 소프웨이브 | Sofwave System (집속형 초음파 자극 시스템) · (주)신한씨스텍 · 정상 | 사진 모델명 든 허가 · 사진 · 추측 |
| DEV-013 | 덴서티하이 | DENSITY HIGH | — 원장에 없음(②) | DENSITY Noir (범용 전기 수술기) · (주)제이시스메디칼 · 정상 | 후보 · 사진 · 웹 |
| DEV-014 | BBL히어로 | mjoule | BBL히어로 | Joule BBL SkinTyte II (펄스광선조사기) · (주)아이맥 · 취소 | 검색어 든 허가 · 추측 |
| DEV-015 | 이브타이탄 | eve Titan | — 원장에 없음(②) | **못 찾음** | — |
| DEV-016 | 텐쎄라 | 10 THERA | 텐쎄라 | 10THERA (집속형초음파자극시스템) · (주)아스테라시스 · 정상 | 사진 모델명 든 허가 · 사진 |
| DEV-017 | 올타이트 | Innoxus (파일명과 다름) | 올타이트 (사진에 올타이트 표기 없음(Innoxus 만)) | **못 찾음** | — |
| DEV-018 | 이래비티 | ERAVITY | — 원장에 없음(②) | **못 찾음** | — |
| DEV-019 | 버츄RF | VIRTUE RF / SHENB | 버츄RF | VirtueRF (범용 전기 수술기) · (주)쉬엔비 · 정상 | 사진 모델명 든 허가 · 웹 |
| DEV-020 | 엔진리프팅 | N-gine | — 원장에 없음(②) | **못 찾음** | — |
| DEV-021 | 세르프 | XERF / Cynosure Lutronic | — 원장에 없음(②) | XERF (범용 전기 수술기) · 주식회사 사이노슈어루트로닉테크놀로지 · 정상 | 후보 · 사진 · 웹 |
| DEV-022 | 포텐자 | POTENZA / Jeisys | 포텐자 | POTENZA™ (범용전기수술기) · (주)제이시스메디칼 · 정상 | 사진 모델명 든 허가 · 사진 · 웹 |
| DEV-023 | 슈링크유니버스 | **사진 판독 불가** | 슈링크유니버스 (사진 판독 불가 — 이름(파일명)으로만 이음) | ULTRAFORMER MPT PLUS (집속형 초음파 자극 시스템) · (주)클래시스 · 정상 | 검색어 든 허가 · 웹 · 업체 목록 |
| DEV-024 | 덴서티 | DENSITY | — 원장에 없음(②) | DENSITY Noir (범용 전기 수술기) · (주)제이시스메디칼 · 정상 | 후보 · 웹 |
| DEV-025 | 온다 | onda / DEKA | 온다 | SSONDAR-SHARK (전기 수술 장치) · 쏜다(주) · 정상 | 검색어 든 허가 · 추측 |
| DEV-026 | 엠페이스 | EMFACE | 엠페이스 · 엠페이스(EMFACE) | EMFACE (범용전기수술기) · 비티엘메디컬테크놀로지코리아(유) · 정상 | 사진 모델명 든 허가 · 사진 · 추측 · 업체 목록 |
| DEV-027 | 리니어지 | Linear Z / Jeisys | — 원장에 없음(②) | LinearZ (집속형초음파자극시스템) · (주)제이시스메디칼 · 정상 | 후보 · 사진 · 웹 |
| DEV-028 | 티타늄 | Soprano Titanium / Alma | 소프라노 티타늄 (티타늄 ↔ 소프라노 티타늄) | Soprano Titanium (반도체레이저수술기) · 알마코리아 유한회사 · 정상 | 검색어 든 허가 · 사진 · 웹 · 업체 목록 |
| DEV-029 | 울쎄라피프라임 | Ultherapy / Merz Aesthetics | 울쎄라피프라임 | Ultherapy Prime (집속형초음파자극시스템) · 멀츠아시아퍼시픽피티이엘티디 · 정상 | 사진 모델명 든 허가 · 사진 · 웹 · 업체 목록 |
| DEV-030 | 올리지오 | Oligio / Wontech | 올리지오 | Oligio X (범용전기수술기) · 원텍(주) · 정상 | **자동**(규칙 A) · 원천 이름 · Hub 영문명 · 사진 · 업체 목록 |
| DEV-031 | 울핏 | Ulfit / Classys | — 원장에 없음(②) | Ulfit(UF1-M200)외 1건 (집속형초음파자극시스템) · (주)클래시스 · 정상 | 후보 · 사진 · 웹 |
| DEV-032 | 튠페이스 | Accent Prime / Alma | 튠페이스 (사진은 Alma Accent Prime(Tune 표기)…) | Accent Prime (범용전기수술기) · 알마코리아 유한회사 · 정상 | 사진 모델명 든 허가 · 사진 · 웹 |
| DEV-033 | 볼뉴머 | Classys | 볼뉴머 (사진에 CLASSYS 로고만) | VOLNEWMER(VM1-M100)외 1건 (범용전기수술기) · (주)클래시스 · 정상 | **자동**(규칙 A) · Hub 영문명 · 업체 목록 |
| DEV-034 | 벨르업 | Belle Up | — 원장에 없음(②) | **못 찾음** | — |
| DEV-035 | 써니 | Sunny | SUNNY | Sunny™ PLUS (범용 전기 수술기) · (주)쉬엔비 · 정상 | 사진 모델명 든 허가 · 사진 |
| DEV-036 | 쿨소닉 | CoolSoniq / Asterasys | 쿨소닉 | Liftera Cool외 1건 (집속형 초음파 자극 시스템) · (주)아스테라시스 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 |
| DEV-037 | 텐써마 | 10 THERMA | 텐써마 | 10 THERMA (범용전기수술기) · 텐텍(주) · 정상 | 사진 모델명 든 허가 · 사진 · 업체 목록 |
| DEV-038 | 울쎄라 | Ulthera / Ulthera | 울쎄라 | Ultherapy Prime (집속형초음파자극시스템) · 멀츠아시아퍼시픽피티이엘티디 · 정상 | 이름 든 허가 · 원천 이름 · Hub 영문명 · 사진 · 업체 목록 |
| DEV-039 | 스텔라듀오 | **사진 판독 불가** | — 원장에 없음(②) | RAYONE PLUS (집속형 초음파 자극 시스템) · (주)엘림텍 · 정상 | 후보 · 웹 · 업체 목록 |
| DEV-040 | 아쿠아필 | AQUA PEEL | 아쿠아필 | 아쿠아필(Aqua Peel) (전동식의료용흡인기) · 엠아이테크 · 정상 | 이름 든 허가 · 원천 이름 |
| DEV-041 | 수소토닝 | DUO HYDROGEN | — 원장에 없음(②) | **못 찾음** | — |
| DEV-042 | 더마큐어 | DERMACURE | — 원장에 없음(②) | **못 찾음** | — |
| DEV-043 | 오메가라이트 | OMEGA light | — 원장에 없음(②) | OMEGA HYDRO PEEL2-1 (전동식의료용흡인기) · (주)모어쓰리 · 정상 | 후보 · 웹 |
| DEV-044 | 힐퓨전프로 | HealFusion Pro / Healux | — 원장에 없음(②) | **못 찾음** | — |
| DEV-045 | 크라이오 멀티마스터 | CRYO MULTI MASTER / puRE young | — 원장에 없음(②) | **못 찾음** | — |
| DEV-046 | 아스트로돔(우주인토닝) | AstrodomeFacial | 아스트로더 (아스트로돔 ↔ 원장 아스트로더 — 같은 기기인지 확인 …) | **못 찾음** | — |
| DEV-047 | 울킨 | ulkin | — 원장에 없음(②) | **못 찾음** | — |
| DEV-048 | LDM-DCM | LDM MED Tri / wellcomet | LDM (LDM-DCM ↔ LDM) | LDM-Smart Tri외 1건 (초음파 자극기) · (주)웰코멧아시아 · 정상 | 이름 든 허가 · 원천 이름 · Hub 영문명 |
| DEV-049 | 오투덤 | OtoDerm | — 원장에 없음(②) | **못 찾음** | — |
| DEV-050 | 더마샤인 | Derma Shine PRO | 더마샤인 | **못 찾음** | — |
| DEV-051 | 큐어젯 | CURE jet | 큐어젯 | **못 찾음** | — |
| DEV-052 | 트리필 프로 | TriFill PRO | — 원장에 없음(②) | **못 찾음** | — |
| DEV-053 | AUTO MTS | DB FNS / dbmedi (uncertain) | — 원장에 없음(②) | DB FNS MICRO NEEDLE C-2.0U외 3건 (의약품 흡수 유도 피부 자극기) · (주)동방메디컬분당지점 · 정상 | 후보 · 사진 |
| DEV-054 | 미라젯 | mirajet | 미라젯 | mirajet Plus+2940외 1건 (기타레이저수술기) · (주)레이저옵텍 · 정상 | 사진 모델명 든 허가 · 사진 |
| DEV-055 | 하이쿡스 | HYCOOX | 하이쿡스 | **못 찾음** | — |
| DEV-056 | 소노케어 | sonocare | — 원장에 없음(②) | **못 찾음** | — |
| DEV-057 | 피코슈어 | Cynosure | 피코슈어 | PicoSure (알렉산드라이트 레이저 수술기) · (주)루트로닉 · 정상 | **자동**(이름+업체 완전 일치) · 원천 이름 · Hub 영문명 · 사진 · 업체 목록 |
| DEV-058 | 브라이톤 미인 | BRIGHTONE | — 원장에 없음(②) | BRIGHTONE M (엔디야그 레이저 수술기) · (주)엘트라글로벌 · 정상 | 후보 · 사진 · 웹 |
| DEV-059 | 할리우드 스펙트라 | HOLLYWOOD SPECTRA | 할리우드스펙트라 | HOLLYWOOD SPECTRA (엔디야그 레이저 수술기) · 주식회사 사이노슈어루트로닉테크놀로지 · 정상 | 사진 모델명 든 허가 · 사진 · 웹 · 업체 목록 |
| DEV-060 | 피코라이트블랙 | PICOLITE | — 원장에 없음(②) | PICOLITE Black외 3건 (엔디야그레이저수술기) · (주)수도그룹 · 정상 | 후보 · 사진 |
| DEV-061 | 피코 라이트 | PICO Lite | — 원장에 없음(②) | **못 찾음** | — |
| DEV-062 | 엑셀브이-제네시스 | **사진 판독 불가** | 엑셀브이 (엑셀브이-제네시스 ↔ 엑셀브이 · 사진 판독 불가) | Excel V Laser (엔디야그레이저수술기) · (주)큐텍코리아 · 정상 | 검색어 든 허가 · 추측 |
| DEV-063 | 큐라스토닝 | CURAS | — 원장에 없음(②) | **못 찾음** | — |
| DEV-064 | 더마브이 | DERMA V / Lutronic | 더마브이 | DermaV (엔디야그 레이저 수술기) · 주식회사 사이노슈어루트로닉테크놀로지 · 정상 | 사진 모델명 든 허가 · 웹 · 업체 목록 |
| DEV-065 | 헬리오스3 | HELIOS III / Laseroptek | — 원장에 없음(②) | HELIOS 785 Pico (엔디야그 레이저 수술기) · (주)레이저옵텍 · 정상 | 후보 · 사진 |
| DEV-066 | 포토나스타워커 | Fotona | 스타워커 (포토나스타워커 ↔ 스타워커) | **못 찾음** | — |
| DEV-067 | 피코케이 | PICO-K / Korea Laser | — 원장에 없음(②) | PICO-K (엔디야그레이저수술기) · 스페클립스(주) · 정상 | 후보 · 사진 · 웹 |
| DEV-068 | 피콜로 프리미엄 | PicoLO PREMIUM / Laseroptek | — 원장에 없음(②) | PICOLO (엔디야그레이저수술기) · (주)레이저옵텍 · 취소 | 후보 · 사진 · 웹 |
| DEV-069 | 아톰레이저 | ATOM / LCI | — 원장에 없음(②) | ATOM (범용전기수술기) · (주)바이오넷 · 취소 | 후보 · 사진 |
| DEV-070 | 브이빔 퍼펙타 | Candela | 브이빔퍼펙타 | Candela Family of Pulse Dye Laser System… (색소레이저수술기) · (주)신한씨스텍 · 취소 | 검색어 든 허가 · 사진 · 추측 |
| DEV-071 | 미라쥬 | Mirage 3D P2 | — 원장에 없음(②) | **못 찾음** | — |
| DEV-072 | 3D 메타뷰 | 3D Meta-Vu | — 원장에 없음(②) | 3D Meta-Vu R외 1건 (체외형 의료용 카메라) · 피에스아이플러스 주식회사 · 정상 | 후보 · 사진 |
| DEV-073 | 마크뷰 | Mark-Vu | — 원장에 없음(②) | Mark-Vu WR외 3건 (체외형 의료용 카메라) · 피에스아이플러스 주식회사 · 정상 | 후보 · 사진 |
| DEV-074 | 스캐나 | SKENA | — 원장에 없음(②) | **못 찾음** | — |
| DEV-075 | 카프리레이저 | CAPRI | — 원장에 없음(②) | CAPRI (반도체레이저수술기) · (주)오로 · 정상 | 후보 · 사진 |
| DEV-076 | 아큐토닝 | Accu TONING / K.L Global | — 원장에 없음(②) | ACCUTONING (반도체 레이저 수술기) · 주식회사 케이엘글로벌 · 정상 | 후보 · 사진 |

## ② 원장 신규 후보 35 — 현장에서 쓰는데 원장에 없는 기기

| 사진 | 현장 이름 | 사진 판독 | 제조사 · 국내 수입사 (웹) | 식약처 후보 | 출처 |
|---|---|---|---|---|---|
| DEV-005 | 아포지플러스 | Apogee / Cynosure | Cynosure (사이노슈어)(USA) · 수입 사이노슈어 한국법인(현 사이노슈어 루트… | **못 찾음** | [1](https://www.massdevice.com/?p=28885) [2](https://brunch.co.kr/@wclinic/39) |
| DEV-013 | 덴서티하이 | DENSITY HIGH | Jeisys Medical (제이시스메디칼)(South Korea) | DENSITY Noir (범용 전기 수술기) · (주)제이시스메디칼 · 정상 외 2 | [1](https://jeisys.com/product/density) [2](https://fda.innolitics.com/device/K250065) |
| DEV-015 | 이브타이탄 | eve Titan | WEERO Co., Ltd. (위로) 추정 — EVE 라인 제조사(South Korea… | **못 찾음** | [1](https://www.gangnamunni.com/events/163728) [2](https://www.theaestheticguide.com/energy-based-devices-treatments/unique-facial-rejuvenation-system-combines-three-technologies-into-one-device) |
| DEV-018 | 이래비티 | ERAVITY | 웹 못 찾음 | **못 찾음** | — |
| DEV-020 | 엔진리프팅 | N-gine | 웹 못 찾음 | **못 찾음** | — |
| DEV-021 | 세르프 | XERF / Cynosure Lutronic | Cynosure Lutronic (사이노슈어 루트로닉)(South Korea) | XERF (범용 전기 수술기) · 주식회사 사이노슈어루트로닉테크놀로지 · 정상 외 3 | [1](https://sports.khan.co.kr/article/202604202354003) [2](https://medigatenews.com/news/3653587790) |
| DEV-024 | 덴서티 | DENSITY | Jeisys Medical (제이시스메디칼)(South Korea) | DENSITY Noir (범용 전기 수술기) · (주)제이시스메디칼 · 정상 외 2 | [1](https://jeisys.com/product/density) [2](https://fda.innolitics.com/device/K250065) |
| DEV-027 | 리니어지 | Linear Z / Jeisys | Jeisys Medical (제이시스메디칼)(South Korea) | LinearZ (집속형초음파자극시스템) · (주)제이시스메디칼 · 정상 외 1 | [1](https://www.jeisys.com/product/linearz) |
| DEV-031 | 울핏 | Ulfit / Classys | Classys (클래시스) / Cluederm(South Korea) | Ulfit(UF1-M200)외 1건 (집속형초음파자극시스템) · (주)클래시스 · 정상 | [1](https://bioskin.it/en/classys-ulfit-ultrasound-device-mfu-mfcu/) |
| DEV-034 | 벨르업 | Belle Up | 웹 못 찾음 | **못 찾음** | — |
| DEV-039 | 스텔라듀오 | **사진 판독 불가** | ㈜엘림텍 (Elimtek)(South Korea) | RAYONE PLUS (집속형 초음파 자극 시스템) · (주)엘림텍 · 정상 외 20 | [1](https://www.kyeonggi.com/article/202011231146531) |
| DEV-041 | 수소토닝 | DUO HYDROGEN | 웹 못 찾음 | **못 찾음** | — |
| DEV-042 | 더마큐어 | DERMACURE | 웹 못 찾음 | **못 찾음** | — |
| DEV-043 | 오메가라이트 | OMEGA light | MORE3 Co., Ltd. (모어쓰리) — Omega PDT 기준(South Kore… | OMEGA HYDRO PEEL2-1 (전동식의료용흡인기) · (주)모어쓰리 · 정상 외 2 | [1](https://www.beautetrade.com/products/omega-pdt/84499/) [2](https://www.skroutz.mt/s/23746497/Omega-Light-O-Melon-Anti-ageing-Light-Therapy-Device-Face-LED-GPY-002.html) |
| DEV-044 | 힐퓨전프로 | HealFusion Pro / Healux | Healux Co., Ltd. (힐럭스)(South Korea) | **못 찾음** | [1](https://gleanmark.com/owner/healuxcoltd) |
| DEV-045 | 크라이오 멀티마스터 | CRYO MULTI MASTER / puRE young | 웹 못 찾음 | **못 찾음** | — |
| DEV-047 | 울킨 | ulkin | 웹 못 찾음 | **못 찾음** | — |
| DEV-049 | 오투덤 | OtoDerm | 웹 못 찾음 | **못 찾음** | [1](https://glownar.com/products/o2toderm-oxygen-led-dome) |
| DEV-052 | 트리필 프로 | TriFill PRO | MCURE (엠큐어)(South Korea) | **못 찾음** | [1](https://biancaclinic.jp/en/blog/54141/) |
| DEV-053 | AUTO MTS | DB FNS / dbmedi (uncertain) | 디비메디 (dbmedi) — 사진 URL 기준, 미검증(South Korea (추정)) | DB FNS MICRO NEEDLE C-2.0U외 3건 (의약품 흡수 유도 피부 자극기) · (주)동방메디컬분당지점 · 정상 | — |
| DEV-056 | 소노케어 | sonocare | NEWPONG (뉴퐁)(South Korea) | **못 찾음** | [1](https://www.praiston.pl/en/catalog/view/14375/new-pong-sonocare-ultrasound-therapy-device) [2](https://www.komachine.com/companies/newpong/products/126867-sonocare) |
| DEV-058 | 브라이톤 미인 | BRIGHTONE | LTRA GLOBAL Co., Ltd.(South Korea (GUDID 회사 접두 8… | BRIGHTONE M (엔디야그 레이저 수술기) · (주)엘트라글로벌 · 정상 | [1](https://accessgudid.nlm.nih.gov/devices/08800088300007) |
| DEV-060 | 피코라이트블랙 | PICOLITE | 웹 못 찾음 | PICOLITE Black외 3건 (엔디야그레이저수술기) · (주)수도그룹 · 정상 외 1 | — |
| DEV-061 | 피코 라이트 | PICO Lite | 웹 못 찾음 | **못 찾음** | — |
| DEV-063 | 큐라스토닝 | CURAS | Ilooda Co., Ltd. (일루다)(South Korea) | **못 찾음** | [1](https://fda.innolitics.com/device/K173038) [2](https://www.regdatalab.com/510k/K173038) |
| DEV-065 | 헬리오스3 | HELIOS III / Laseroptek | Laseroptek Co., Ltd. (라셉텍)(South Korea) | HELIOS 785 Pico (엔디야그 레이저 수술기) · (주)레이저옵텍 · 정상 외 4 | [1](https://accessgudid.nlm.nih.gov/devices/08800035501129) |
| DEV-067 | 피코케이 | PICO-K / Korea Laser | Speclipse, Inc. (스페클립스)(South Korea) | PICO-K (엔디야그레이저수술기) · 스페클립스(주) · 정상 외 1 | [1](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K253342) [2](https://www.imdad.com/Products/Pico-K) |
| DEV-068 | 피콜로 프리미엄 | PicoLO PREMIUM / Laseroptek | Laseroptek Co., Ltd. (라셉텍)(South Korea) | PICOLO (엔디야그레이저수술기) · (주)레이저옵텍 · 취소 | [1](https://www.janeyoomd.com/k-beauty/picolo-premium/) |
| DEV-069 | 아톰레이저 | ATOM / LCI | LCI (사진 표기) | ATOM (범용전기수술기) · (주)바이오넷 · 취소 | — |
| DEV-071 | 미라쥬 | Mirage 3D P2 | Mirage3D (myreal3d.com)(China) | **못 찾음** | [1](https://www.tmtpost.com/trendmakers/419421) |
| DEV-072 | 3D 메타뷰 | 3D Meta-Vu | PSI PLUS (피에스아이플러스) 추정(South Korea) | 3D Meta-Vu R외 1건 (체외형 의료용 카메라) · 피에스아이플러스 주식회사 · 정상 | [1](https://kidd.co.kr/news/246188) |
| DEV-073 | 마크뷰 | Mark-Vu | PSI PLUS (피에스아이플러스) 추정(South Korea) | Mark-Vu WR외 3건 (체외형 의료용 카메라) · 피에스아이플러스 주식회사 · 정상 | [1](https://kidd.co.kr/news/246188) [2](https://hdmall.co.th/beauty/program-mark-vu-analyze-facial-skin-condition-panglyst-clinic) |
| DEV-074 | 스캐나 | SKENA | 웹 못 찾음 | **못 찾음** | — |
| DEV-075 | 카프리레이저 | CAPRI | 웹 못 찾음 | CAPRI (반도체레이저수술기) · (주)오로 · 정상 외 1 | — |
| DEV-076 | 아큐토닝 | Accu TONING / K.L Global | K.L Global (사진 표기) | ACCUTONING (반도체 레이저 수술기) · 주식회사 케이엘글로벌 · 정상 | — |

## ③ 시술군별 — 원장 이름 → 식약처 품목

「현장」 ● = 더데이랩스에서 지금 쓰는 기기(사진 번호).

### M1 보톡스 (18)

| 원장 이름 | 현장 | 찾은 식약처 품목 (공식명 · 업체 · 상태) | 어떻게 · 근거 | 후보 |
|---|---|---|---|---|
| 나보타 |  | 나보타주150단위(클로스트리디움보툴리눔독소A형) · (주)대웅제약 · 정상 | **자동**(규칙 A) · 원천 이름 · Hub 영문명 | 4 |
| 더톡신 |  | 제테마더톡신주100단위(클로스트리디움보툴리눔독소A형) · (주)제테마 · 정상 | **자동**(규칙 A) · 원천 이름 · Hub 영문명 · 업체 목록 | 3 |
| 디스포트 |  | 디스포트주(클로스트리디움보툴리눔A형독소-혈구응집소복합체) · 입센코리아(주) · 정상 | **자동**(규칙 A) · 원천 이름 · Hub 영문명 · 업체 목록 | 15 |
| 메디톡신 |  | 메디톡신주150단위(클로스트리디움보툴리눔독소A형)[수출명:뉴로녹스주 15… · (주)메디톡스 · 정상 | **자동**(규칙 A) · 원천 이름 · Hub 영문명 · 업체 목록 | 10 |
| 보톡스(엘러간) |  | 보톡스주 50단위(클로스트리디움보툴리눔독소A형) · 한국애브비(주) · 정상 | **자동**(규칙 A) · 원천 이름 · Hub 영문명 · 업체 목록 | 40 |
| 보툴렉스 |  | 보툴렉스주300단위(클로스트리디움보툴리눔독소A형) · 휴젤주식회사 · 정상 | **자동**(규칙 A) · 원천 이름 · Hub 영문명 · 업체 목록 | 5 |
| 비비톡신 |  | 비비톡신주100단위(클로스트리디움보툴리눔독소A형) · (주)휴메딕스 · 정상 | **자동**(규칙 A) · 원천 이름 · 업체 목록 | 79 |
| 원더톡스 |  | 원더톡스주200단위(클로스트리디움보툴리눔독소A형) · (주)종근당 · 정상 | **자동**(규칙 A) · 원천 이름 | 3 |
| 이노톡스 |  | 이노톡스주(클로스트리디움보툴리눔독소A형)(수출명 : INNOTOX Inj… · (주)메디톡스 · 정상 | **자동**(규칙 A) · 원천 이름 · 업체 목록 | 10 |
| 제오민 |  | 제오민주50단위(클로스트리디움보툴리눔독소A형(150kDa)) · 멀츠아시아퍼시픽피티이엘티디 · 정상 | **자동**(규칙 A) · 원천 이름 · Hub 영문명 · 업체 목록 | 2 |
| 코어톡스 |  | 코어톡스주(클로스트리디움보툴리눔독소A형(150kDa))(수출명 : Cor… · (주)메디톡스 · 정상 | **자동**(규칙 A) · 원천 이름 · 업체 목록 | 10 |
| 다복스 |  | 넴루비오프리필드펜(네몰리주맙) · 갈더마코리아(주) · 정상 | 잡음 — 다른 제품일 수 있음 · 업체 목록 | 15 |
| 리즈톡신 |  | 리즈톡스주200단위(클로스트리디움보툴리눔독소A형)(수출명:휴톡스주200단… · (주)휴온스바이오파마 · 정상 | 이름 든 허가 · 원천 이름 · 웹 · 업체 목록 | 3 |
| 센독스 |  | 톡스나인주100단위(클로스트리디움보툴리눔독소A형)(수출용) · (주)메디카코리아 · 정상 | 검색어 든 허가 · 업체 목록 | 7 |
| 에이비오톡신 |  | 디스포트주(클로스트리디움보툴리눔A형독소-혈구응집소복합체) · 입센코리아(주) · 정상 | 이름 든 허가 · 원천 이름 | 1 |
| 톡스온 |  | 보타루마주(클로스트리디움보툴리눔독소A형(150kDa)) · (주)에이티지씨 · 정상 | 이름 든 허가 · 원천 이름 · 업체 목록 | 2 |
| 퓨어녹스 |  | 팜파스플라스타 · 대화제약(주) · 정상 | 잡음 — 다른 제품일 수 있음 · 업체 목록 | 284 |
| 보리톡스 |  | **못 찾음** | — | 0 |

### M2 필러 (29)

| 원장 이름 | 현장 | 찾은 식약처 품목 (공식명 · 업체 · 상태) | 어떻게 · 근거 | 후보 |
|---|---|---|---|---|
| 뉴라미스 |  | 뉴라미스 (조직수복용생체재료) · (주)메디톡스 · 정상 | **자동**(이름+업체 완전 일치) · 원천 이름 · 업체 목록 | 11 |
| 벨라스트 |  | 벨라스트 울트라 소프트 L(Bellast Ultra Soft L) 1.0… (조직수복용생체재료) · 동국제약(주) · 정상 | **자동**(규칙 A) · 원천 이름 · 업체 목록 | 46 |
| 엘라비에 |  | 엘라비에 터치 (조직 수복용 생체 재료) · (주)휴메딕스 · 정상 | **자동**(규칙 A) · 원천 이름 · 업체 목록 | 32 |
| 큐티필 |  | 큐티필 시그니처 파인(QT FILL Signature Fine)외 14건 (조직 수복용 생체 재료) · (주)에스테팜 · 정상 | **자동**(규칙 A) · 원천 이름 · 업체 목록 | 7 |
| 더채움 |  | 더채움 시그니처 4 (THE CHAEUM SIGNATURE 4)외 28건 (조직수복용생체재료) · (주)아크로스 · 정상 | 이름 든 허가 · 원천 이름 · Hub 영문명 | 13 |
| 더채움프리미어 |  | 더채움 시그니처 4 (THE CHAEUM SIGNATURE 4)외 28건 (조직수복용생체재료) · (주)아크로스 · 정상 | 검색어 든 허가 · 웹 · 3차 | 13 |
| 레스틸렌 |  | Restylane Kysse (조직 수복용 생체 재료) · 갈더마코리아(주) · 정상 | 이름 든 허가 · 원천 이름 · Hub 영문명 · 업체 목록 | 22 |
| 리쥬비엘 |  | REJUVIEL W WITH LIDOCAINE외 6건 (조직수복용생체재료) · (주)파마리서치 · 정상 | 검색어 든 허가 · 웹 · 업체 목록 | 43 |
| 메테로 |  | imijion FINE외 1건 (조직 수복용 생체 재료) · 주식회사 한국비엔씨 세종공장 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 47 |
| 벨로테로 |  | Belotero Revive 1.0ml (조직수복용생체재료) · 멀츠아시아퍼시픽피티이엘티디 · 정상 | 이름 든 허가 · 원천 이름 · Hub 영문명 · 업체 목록 | 14 |
| 스타일에이지 |  | Stylage XL Lidocaine_Bisoft외 3건 (조직수복용생체재료) · (주)에코라 · 정상 | 검색어 든 허가 · 추측 | 7 |
| 아띠에르 |  | PTF-NOM(수출명: Potenfill) (조직수복용생체재료) · (주)메디톡스 · 정상 | 계열만 맞음 — 확인 필요 · 웹 · 업체 목록 | 11 |
| 아말리안 |  | AMALIAN SF 24 advanced 2ml외 1건 (조직 수복용 생체 재료) · 대화제약(주) · 정상 | 검색어 든 허가 · 추측 | 5 |
| 아쿠아미드 |  | Aquamid Reconstruction외 1건 (조직수복용재료) · (주)유메코그룹 · 취소 | 검색어 든 허가 · 추측 | 3 |
| 아테콜 |  | Bellafill Treatment Kit (조직수복용생체재료) · (주)메디팁 · 정상 | 검색어 든 허가 · 웹 · 3차 | 1 |
| 에피티크 |  | JTM124(3.0/3.0)외 2건 (조직 수복용 재료) · (주)제테마용인공장 · 정상 | 계열만 맞음 — 확인 필요 · 웹 · 업체 목록 | 75 |
| 엘라비에프라임 |  | D42223(수출명: Elravie Premier Soft D42223)… (조직수복용생체재료) · (주)휴메딕스 · 정상 | 검색어 든 허가 · 웹 · 업체 목록 | 32 |
| 유스필 |  | RBMD-433-02X외 1건 (조직 수복용 생체 재료) · (주)알에프바이오 · 정상 | 계열만 맞음 — 확인 필요 · 웹 · 업체 목록 | 25 |
| 이브아르 |  | YVOIRE contour s 1.0외 6건 (조직 수복용 생체 재료) · (주)엘지화학익산공장 · 정상 | 이름 든 허가 · Hub 영문명 · 추측 · 업체 목록 | 10 |
| 쥬비덤 |  | Juvederm VOLUX (조직수복용생체재료) · 한국애브비(주) · 정상 | 이름 든 허가 · 업체 목록 | 29 |
| 큐젤 |  | imijion FINE외 1건 (조직 수복용 생체 재료) · 주식회사 한국비엔씨 세종공장 · 정상 | 계열만 맞음 — 확인 필요 · 웹 · 업체 목록 · 3차 | 34 |
| 큐젤MAX |  | imijion FINE외 1건 (조직 수복용 생체 재료) · 주식회사 한국비엔씨 세종공장 · 정상 | 계열만 맞음 — 확인 필요 · 웹 · 업체 목록 | 47 |
| 테오시알 |  | Teosyal® PureSense Global Action 1mL TS3… (조직 수복용 생체 재료) · 이머고코리아(유) · 정상 | 검색어 든 허가 · 추측 | 5 |
| 퍼펙타 |  | Perfectha Subskin 1ml (조직수복용생체재료) · 한국싱클레어 유한회사 · 정상 | 검색어 든 허가 · 추측 | 3 |
| 프린세스 |  | Princess Filler (조직수복용생체재료) · 엠엔엘 · 정상 | 검색어 든 허가 · 웹 · 3차 | 7 |
| 하모니카 |  | Juvederm VOLUX (조직수복용생체재료) · 한국애브비(주) · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 11 |
| 셀레스텔라 |  | **못 찾음** | — | 0 |
| 앨리필 |  | **못 찾음** | — | 0 |
| 에피로크 |  | **못 찾음** | — | 0 |

### M3 바이오스티뮬레이터/콜라겐부스터 (24)

| 원장 이름 | 현장 | 찾은 식약처 품목 (공식명 · 업체 · 상태) | 어떻게 · 근거 | 후보 |
|---|---|---|---|---|
| 스컬트라 |  | SCULPTRA (조직수복용재료) · 갈더마코리아(주) · 정상 | **자동**(규칙 A) · Hub 영문명 · 업체 목록 | 22 |
| 쥬베룩 |  | 쥬베룩스킨(Juvelook Skin)외 10건 (조직수복용재료) · (주)바임 · 정상 | **자동**(규칙 A) · 원천 이름 · Hub 영문명 · 업체 목록 | 3 |
| HArmonyCa |  | Juvederm VOLUX (조직수복용생체재료) · 한국애브비(주) · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 11 |
| PLLA-SCA |  | SCULPTRA (조직수복용재료) · 갈더마코리아(주) · 정상 | 검색어 든 허가 · 추측 | 1 |
| 고우리 |  | DAH01 (조직 수복용 재료) · (주)덱스레보 · 정상 | 계열만 맞음 — 확인 필요 · 웹 · 업체 목록 | 6 |
| 도프ECM |  | PD12152025외 61건 (콜라겐 사용 조직 보충재) · 주식회사 도프 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 5 |
| 디클래씨 |  | Facetem S BACF15P외 3건 (조직수복용재료) · (주)디엔컴퍼니 · 취소 | 검색어 든 허가 · 웹 · 3차 | 3 |
| 라풀렌 |  | DMFI250외 2건 (조직수복용재료) · (주)삼양바이오팜 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 2 |
| 래디어스 |  | RADIESSE + Lidocaine Injectable Implant … (조직수복용재료) · 멀츠아시아퍼시픽피티이엘티디 · 정상 | 이름 든 허가 · Hub 영문명 · 업체 목록 | 15 |
| 리투오 |  | RE2O I-Ject외 11건 (마취액 주입 도구 한 벌) · 메디허브(주) · 정상 | 검색어 든 허가 · 웹 · 3차 | 33 |
| 리투오파인 |  | 밸피엔(BelPN)외 1건 (조직 수복용 생체 재료) · (주)휴메딕스 · 정상 | 계열만 맞음 — 확인 필요 · 웹 · 업체 목록 | 32 |
| 셀르디엠 |  | PD B7007M외 419건 (콜라겐사용조직보충재) · 한스바이오메드(주) · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 · 3차 | 43 |
| 에스테필 |  | AestheFill-V50-WF외 12건 (조직수복용재료) · (주)리젠바이오텍 · 정상 | 검색어 든 허가 · 웹 · 3차 | 79 |
| 엘란쎄 |  | Ellanse S without needles (조직수복용재료) · 한국싱클레어 유한회사 · 정상 | 이름 든 허가 · Hub 영문명 · 업체 목록 | 13 |
| 올리디아 |  | 올리디아(Olidia) MYO 240외 44건 (조직 수복용 재료) · (주)피알피사이언스 · 정상 | 이름 든 허가 · 원천 이름 | 1 |
| 울트라콜 |  | ULTRACOL VIVID 200외 1건 (조직 수복용 재료) · 주식회사 울트라브이 · 정상 | 검색어 든 허가 · 웹 · 업체 목록 | 54 |
| 쥬베룩볼륨 |  | Vivabella-V50외 1건 (조직수복용재료) · (주)바임 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 3 |
| 쥬브아셀 |  | Vivabella-V50외 1건 (조직수복용재료) · (주)바임 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 3 |
| 레티젠 |  | **못 찾음** | — | 0 |
| 린피니 |  | **못 찾음** | — | 0 |
| 미라콜 |  | **못 찾음** | — | 0 |
| 아디떼 |  | **못 찾음** | — | 0 |
| 콜라겐핀 |  | **못 찾음** | — | 0 |
| 콜라쥬 |  | **못 찾음** | — | 0 |

### M4 스킨부스터 (31)

| 원장 이름 | 현장 | 찾은 식약처 품목 (공식명 · 업체 · 상태) | 어떻게 · 근거 | 후보 |
|---|---|---|---|---|
| NCTF 필로르가 |  | AS4011 (멸균주사침) · (주)아이더마바이오 · 정상 | 계열만 맞음 — 확인 필요 · 웹 · 업체 목록 · 3차 | 1 |
| 레스틸렌스킨부스터 |  | Restylane Skinboosters Vital Light Lidoc… (조직수복용생체재료) · 갈더마코리아(주) · 정상 | 검색어 든 허가 · 웹 · 업체 목록 | 22 |
| 리바이브 |  | Belotero Revive 1.0ml (조직수복용생체재료) · 멀츠아시아퍼시픽피티이엘티디 · 정상 | 검색어 든 허가 · 웹 · 업체 목록 | 14 |
| 리바이브 글리세롤 |  | Belotero Revive 1.0ml (조직수복용생체재료) · 멀츠아시아퍼시픽피티이엘티디 · 정상 | 검색어 든 허가 · 웹 · 3차 | 1 |
| 리쥬란HB+ |  | M16-002외 1건 (조직 수복용 생체 재료) · (주)파마리서치 · 정상 | 계열만 맞음 — 확인 필요 · 웹 · 업체 목록 | 43 |
| 리쥬란아이 |  | M16-002외 1건 (조직 수복용 생체 재료) · (주)파마리서치 · 정상 | 계열만 맞음 — 확인 필요 · 웹 · 업체 목록 | 43 |
| 리쥬란힐러 |  | 리쥬란(Rejuran)외 9건 (조직수복용생체재료) · (주)파마리서치 · 정상 | 검색어 든 허가 · 웹 · 업체 목록 | 43 |
| 릴리이드M |  | BMI-PNCol-3.0외 2건 (콜라겐 사용 조직 보충재) · (주)한국비엠아이 · 정상 | 계열만 맞음 — 확인 필요 · 웹 · 업체 목록 | 12 |
| 매쿰7 |  | 매쿰7 (McCoom7) (조직 수복용 재료) · 주식회사 사치바이오 · 정상 | 이름 든 허가 · 원천 이름 | 1 |
| 바이리즌 |  | HyalSense Deep (조직수복용생체재료) · 휴젤(주) · 취소 | 계열만 맞음 — 확인 필요 · 웹 · 업체 목록 | 11 |
| 벨피엔 프로 |  | 밸피엔(BelPN)외 1건 (조직 수복용 생체 재료) · (주)휴메딕스 · 정상 | 계열만 맞음 — 확인 필요 · 웹 · 업체 목록 | 32 |
| 볼뉴머 |  | VOLNEWMER(VM1-M100)외 1건 (범용전기수술기) · (주)클래시스 · 정상 | 이름 든 허가 · Hub 영문명 · 웹 · 업체 목록 | 121 |
| 비타란 |  | HP Cell VITARAN J외 2건 (조직수복용생체재료) · (주)비알팜 · 정상 | 검색어 든 허가 · 웹 · 업체 목록 | 26 |
| 셀엑소좀 |  | 밸피엔(BelPN)외 1건 (조직 수복용 생체 재료) · (주)휴메딕스 · 정상 | 계열만 맞음 — 확인 필요 · 웹 · 업체 목록 | 32 |
| 스킨바이브 |  | SKINVIVE by Juvederm (조직수복용생체재료) · 한국애브비(주) · 정상 | 검색어 든 허가 · 추측 · 업체 목록 | 12 |
| 인에이블 |  | YVOIRE contour s 1.0외 6건 (조직 수복용 생체 재료) · (주)엘지화학익산공장 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 6 |
| 테오시알레디세스 |  | Teosyal® PureSense Global Action 1mL TS3… (조직 수복용 생체 재료) · 이머고코리아(유) · 정상 | 검색어 든 허가 · 추측 | 5 |
| 필로르가135HA |  | AS4011 (멸균주사침) · (주)아이더마바이오 · 정상 | 계열만 맞음 — 확인 필요 · 웹 · 업체 목록 · 3차 | 1 |
| 힐로웨이브 |  | Dbit13S (치과 임플란트 시술용 드릴) · 주식회사 하이어코퍼레이션 · 정상 | 잡음 — 다른 제품일 수 있음 · 업체 목록 | 1 |
| ASCE+엑소좀 |  | **못 찾음** | — | 0 |
| SNP솔루션 |  | **못 찾음** | — | 0 |
| 드원셀 |  | **못 찾음** | — | 0 |
| 레나토S |  | **못 찾음** | — | 0 |
| 리듐 |  | **못 찾음** | — | 0 |
| 사이토케어 |  | **못 찾음** | — | 0 |
| 소노PDRN |  | **못 찾음** | — | 0 |
| 스네일샷 |  | **못 찾음** | — | 0 |
| 엑소힐러 |  | **못 찾음** | — | 0 |
| 카탈리스트 |  | **못 찾음** | — | 0 |
| 투 (TU) |  | **못 찾음** | — | 0 |
| 프로파일로 |  | **못 찾음** | — | 0 |

### M7 실리프팅 (24)

| 원장 이름 | 현장 | 찾은 식약처 품목 (공식명 · 업체 · 상태) | 어떻게 · 근거 | 후보 |
|---|---|---|---|---|
| 민트리프트 |  | MINT TB40외 7건 (안면조직고정용실) · 한스바이오메드(주) · 정상 | 검색어 든 허가 · 웹 · 업체 목록 | 149 |
| 블루로즈클레어 |  | AI25 (풍선확장기) · 휴젤(주)(서울지점) · 취소 | 잡음 — 다른 제품일 수 있음 · 업체 목록 | 11 |
| 실루엣소프트 |  | SMS 26-PL-3.0.1-NA외 5건 (안면조직고정용실) · 한국싱클레어 유한회사 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 13 |
| 울트라V |  | UVTS2590W-C70150외 256건 (안면조직고정용실) · 주식회사 울트라브이 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 8 |
| 테스리프트 |  | PowerFill-V500외 3건 (조직수복용재료) · (주)리젠바이오텍 · 정상 | 잡음 — 다른 제품일 수 있음 · 업체 목록 | 5 |
| N코그 |  | **못 찾음** | — | 0 |
| V리프트 |  | **못 찾음** | — | 0 |
| 레보실 |  | **못 찾음** | — | 0 |
| 로즈실 |  | **못 찾음** | — | 0 |
| 리드파인 |  | **못 찾음** | — | 0 |
| 면사리프트 |  | **못 찾음** | — | 0 |
| 몰드리프트 |  | **못 찾음** | — | 0 |
| 미스코 |  | **못 찾음** | — | 0 |
| 앵커리프트 |  | **못 찾음** | — | 0 |
| 엘리실 |  | **못 찾음** | — | 0 |
| 오메가리프트 |  | **못 찾음** | — | 0 |
| 잼버실 |  | **못 찾음** | — | 0 |
| 캐번실 |  | **못 찾음** | — | 0 |
| 코그실루프 |  | **못 찾음** | — | 0 |
| 텐선실 |  | **못 찾음** | — | 0 |
| 투와이실 |  | **못 찾음** | — | 0 |
| 프린스리프트 |  | **못 찾음** | — | 0 |
| 해피리프트 |  | **못 찾음** | — | 0 |
| 허니콤실 |  | **못 찾음** | — | 0 |

### M8 레이저 (50)

| 원장 이름 | 현장 | 찾은 식약처 품목 (공식명 · 업체 · 상태) | 어떻게 · 근거 | 후보 |
|---|---|---|---|---|
| 클라리티2 | ● DEV-004 | CLARITY II (엔디야그레이저수술기) · (주)루트로닉 · 정상 | **자동**(이름+업체 완전 일치) · Hub 영문명 · 사진 · 업체 목록 | 187 |
| 피코슈어 | ● DEV-057 | PicoSure (알렉산드라이트 레이저 수술기) · (주)루트로닉 · 정상 | **자동**(이름+업체 완전 일치) · 원천 이름 · Hub 영문명 · 사진 · 업체 목록 | 187 |
| BBL |  | Joule BBL SkinTyte II (펄스광선조사기) · (주)아이맥 · 취소 | 이름 든 허가 · 원천 이름 | 12 |
| BBL스킨타이트 |  | Joule BBL SkinTyte II (펄스광선조사기) · (주)아이맥 · 취소 | 검색어 든 허가 · 추측 | 2 |
| BBL히어로 | ● DEV-014 | Joule BBL SkinTyte II (펄스광선조사기) · (주)아이맥 · 취소 | 검색어 든 허가 · 추측 | 2 |
| E-MAX |  | 1.74 ASP USH UV-STAR DRIVE-MAX외 11건 (안경렌즈) · (주)데코비젼 · 정상 | 잡음 — 다른 제품일 수 있음 · 원천 이름 | 1 |
| 노블린 | ● DEV-006 | Nobleen (알렉산드라이트레이저수술기) · 화인엠이씨(주) · 정상 | 사진 모델명 든 허가 · 사진 · 3차 | 1 |
| 더마브이 | ● DEV-064 | DermaV (엔디야그 레이저 수술기) · 주식회사 사이노슈어루트로닉테크놀로지 · 정상 | 사진 모델명 든 허가 · 웹 · 업체 목록 | 187 |
| 디스커버리피코 |  | Discovery Pico Plus (루비레이저수술기) · (주)에코라 · 정상 | 검색어 든 허가 · 추측 | 2 |
| 라이트쉬어듀엣 |  | UltraPulse Alpha Office Silver 외 3건 (탄산가스 레이저 수술기) · 루메니스비코리아 유한회사 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 34 |
| 레블라이트SI |  | PICOPLUS (엔디야그 레이저 수술기) · 주식회사 사이노슈어루트로닉테크놀로지 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 187 |
| 리팟 |  | PENTO 9900 (엔디야그 레이저 수술기) · (주)클래시스 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 121 |
| 메디오스타넥스트프로 |  | MeDioStar (레이저수술기) · (주)네오아시아 · 취소 | 검색어 든 허가 · 추측 | 1 |
| 모자이크 |  | 로호 모자이크 (MOSAIC®) MOS1717HD-LTC외 2건 (의료용 압력분산 매트리스) · 퍼모빌엘엘씨 유한회사 · 정상 | 잡음 — 다른 제품일 수 있음 · 원천 이름 | 1 |
| 벡터스 |  | 9SYS7751-CNDL (반도체 레이저 수술기) · 시너론켄델라코리아 유한회사 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 30 |
| 브이빔 |  | Candela Family of Pulse Dye Laser System… (색소레이저수술기) · (주)신한씨스텍 · 취소 | 검색어 든 허가 · 추측 | 2 |
| 브이빔퍼펙타 | ● DEV-070 | Candela Family of Pulse Dye Laser System… (색소레이저수술기) · (주)신한씨스텍 · 취소 | 검색어 든 허가 · 사진 · 추측 | 2 |
| 사이노슈어아이콘 |  | Icon (기타 레이저 수술기) · (주)루트로닉 · 정상 | 검색어 든 허가 · 사진 · 추측 | 4 |
| 셀렉V |  | AQUA CEL (펄스광선조사기) · (주)제이시스메디칼 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 103 |
| 스마트사이드 |  | SmartXide UltraSpeed2 (탄산가스 레이저 수술기) · (주)에코라 · 정상 | 검색어 든 허가 · 추측 | 2 |
| 스텔라M22 |  | UltraPulse Alpha Office Silver 외 3건 (탄산가스 레이저 수술기) · 루메니스비코리아 유한회사 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 34 |
| 스플렌더X |  | UltraPulse Alpha Office Silver 외 3건 (탄산가스 레이저 수술기) · 루메니스비코리아 유한회사 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 34 |
| 슬렌더엑스 |  | PICOPLUS (엔디야그 레이저 수술기) · 주식회사 사이노슈어루트로닉테크놀로지 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 187 |
| 시너론 아이플러스 |  | WaveLight EX500 (기타안과용레이저수술기) · 한국알콘(주) · 정상 | 검색어 든 허가 · 추측 | 20 |
| 아발란체 | ● DEV-003 | PICOPLUS (엔디야그 레이저 수술기) · 주식회사 사이노슈어루트로닉테크놀로지 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 187 |
| 아포지엘리트플러스 | ● DEV-007 | Elite iQ (알렉산드라이트레이저수술기) · (주)루트로닉 · 취소 | 사진 모델명 든 허가 · 사진 · 웹 · 업체 목록 · 3차 | 190 |
| 에코2 |  | PICOPLUS (엔디야그 레이저 수술기) · 주식회사 사이노슈어루트로닉테크놀로지 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 187 |
| 에코2에볼루션 |  | PICOPLUS (엔디야그 레이저 수술기) · 주식회사 사이노슈어루트로닉테크놀로지 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 187 |
| 엑셀V+ |  | Excel V Laser (엔디야그레이저수술기) · (주)큐텍코리아 · 정상 | 이름 든 허가 · 원천 이름 · Hub 영문명 | 4 |
| 엑셀브이 | ● DEV-062 | Excel V Laser (엔디야그레이저수술기) · (주)큐텍코리아 · 정상 | 검색어 든 허가 · 추측 | 4 |
| 엔라이튼 |  | enlighten SR (엔디야그레이저수술기) · (주)큐텍코리아 · 정상 | 검색어 든 허가 · 추측 | 3 |
| 울트라펄스 |  | UltraPulse Alpha Office Silver 외 3건 (탄산가스 레이저 수술기) · 루메니스비코리아 유한회사 · 정상 | 검색어 든 허가 · 추측 | 3 |
| 젠틀레이즈 |  | GentleLase Pro-U (알렉산드라이트레이저수술기) · (주)신한씨스텍 · 취소 | 검색어 든 허가 · 추측 | 17 |
| 젠틀맥스프로 | ● DEV-002 | GentleMax Pro (엔디야그레이저수술기) · (주)신한씨스텍 · 취소 | 사진 모델명 든 허가 · 사진 · 추측 | 19 |
| 젠틀맥스프로+ | ● DEV-001 | GentleMaxi Pro Plus (알렉산드라이트 레이저 수술기) · 주식회사 밴스로컬 · 정상 | 검색어 든 허가 · 추측 | 19 |
| 클라리티2 (혈관) | ● DEV-004 | CLARITY II LPA (ICD Type)외 1건 (알렉산드라이트 레이저 수술기) · 주식회사 사이노슈어루트로닉테크놀로지 · 정상 | 사진 모델명 든 허가 · 사진 · 웹 · 업체 목록 | 187 |
| 클리어앤브릴리언트 |  | CBT-CONSOLE (반도체 레이저 수술기) · 솔타메디칼코리아 유한회사 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 20 |
| 트리니티 |  | 트리니티쿠션02(4040)외 6건 (의료용 압력분산 매트리스) · (주)포에버헬스케어 · 정상 | 잡음 — 다른 제품일 수 있음 · 원천 이름 | 2 |
| 포토나SP다이나미스 |  | XS Dynamis M002-2A (기타 레이저 수술기) · (주)신한씨스텍 · 정상 | 사진 모델명 든 허가 · 사진 · 3차 | 189 |
| 프락셀듀얼 |  | Fraxel(R) DUAL 1550/1927외 1건 (기타 레이저 수술기) · 솔타메디칼코리아 유한회사 · 정상 | 검색어 든 허가 · 추측 | 5 |
| 피코케어 |  | GU Laser (엔디야그 레이저 수술기) · 원텍(주) · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 136 |
| 피코코어 |  | PICOPLUS (엔디야그 레이저 수술기) · 주식회사 사이노슈어루트로닉테크놀로지 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 187 |
| 피코플러스 |  | PICOPLUS (엔디야그 레이저 수술기) · 주식회사 사이노슈어루트로닉테크놀로지 · 정상 | 사진 모델명 든 허가 · 사진 · 업체 목록 | 187 |
| 할리우드스펙트라 | ● DEV-059 | HOLLYWOOD SPECTRA (엔디야그 레이저 수술기) · 주식회사 사이노슈어루트로닉테크놀로지 · 정상 | 사진 모델명 든 허가 · 사진 · 웹 · 업체 목록 · 3차 | 212 |
| 로제라이트 |  | **못 찾음** | — | 0 |
| 리레이저 |  | **못 찾음** | — | 0 |
| 바이탈라이즈 |  | **못 찾음** | — | 0 |
| 스타워커 | ● DEV-066 | **못 찾음** | — | 0 |
| 트루피코 |  | **못 찾음** | — | 0 |
| 포토나스타발브 |  | **못 찾음** | — | 0 |

### M9 기기 리프팅 (42)

| 원장 이름 | 현장 | 찾은 식약처 품목 (공식명 · 업체 · 상태) | 어떻게 · 근거 | 후보 |
|---|---|---|---|---|
| 더블로골드 |  | DOUBLO-GOLD™ (집속형초음파자극시스템) · (주)하이로닉 · 정상 | **자동**(이름+업체 완전 일치) · Hub 영문명 · 업체 목록 | 61 |
| 볼뉴머 | ● DEV-033 | VOLNEWMER(VM1-M100)외 1건 (범용전기수술기) · (주)클래시스 · 정상 | **자동**(규칙 A) · Hub 영문명 · 업체 목록 | 121 |
| 올리지오 | ● DEV-030 | Oligio X (범용전기수술기) · 원텍(주) · 정상 | **자동**(규칙 A) · 원천 이름 · Hub 영문명 · 사진 · 업체 목록 | 136 |
| SUNNY | ● DEV-035 | Sunny™ PLUS (범용 전기 수술기) · (주)쉬엔비 · 정상 | 사진 모델명 든 허가 · 사진 · 3차 | 19 |
| 더블로 |  | DOUBLO-GOLD™ (집속형초음파자극시스템) · (주)하이로닉 · 정상 | 검색어 든 허가 · 웹 · 업체 목록 | 61 |
| 더블로골드S |  | DOUBLO-GOLD™ (집속형초음파자극시스템) · (주)하이로닉 · 정상 | 검색어 든 허가 · 추측 | 3 |
| 듀오타이트 |  | SCARLET PRO™ (범용 전기 수술기) · (주)비올메디컬 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 31 |
| 리니어펌 | ● DEV-011 | COTENZA (범용 전기 수술기) · (주)제이시스메디칼 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 103 |
| 리프세라 |  | Liftera Cool외 1건 (집속형 초음파 자극 시스템) · (주)아스테라시스 · 정상 | 검색어 든 허가 · 추측 | 7 |
| 리프테라 |  | Liftera Cool외 1건 (집속형 초음파 자극 시스템) · (주)아스테라시스 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 20 |
| 버츄RF | ● DEV-019 | VirtueRF (범용 전기 수술기) · (주)쉬엔비 · 정상 | 사진 모델명 든 허가 · 웹 · 3차 | 33 |
| 볼뉴머RF |  | ULTRAFORMER MPT PLUS (집속형 초음파 자극 시스템) · (주)클래시스 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 121 |
| 소프라노 티타늄 | ● DEV-028 | Soprano Titanium (반도체레이저수술기) · 알마코리아 유한회사 · 정상 | 검색어 든 허가 · 사진 · 웹 · 업체 목록 | 24 |
| 소프웨이브 | ● DEV-012 | Sofwave System (집속형 초음파 자극 시스템) · (주)신한씨스텍 · 정상 | 사진 모델명 든 허가 · 사진 · 추측 | 1 |
| 슈링크 |  | UF3-C300 (집속형초음파자극시스템) · (주)클래시스 · 정상 | 검색어 든 허가 · 웹 · 업체 목록 | 121 |
| 슈링크유니버스 | ● DEV-023 | ULTRAFORMER MPT PLUS (집속형 초음파 자극 시스템) · (주)클래시스 · 정상 | 검색어 든 허가 · 웹 · 업체 목록 | 121 |
| 시크릿맥스 |  | ULTRAFORMER MPT PLUS (집속형 초음파 자극 시스템) · (주)클래시스 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 121 |
| 써마지FLX | ● DEV-009 | Thermage Deep Skin외 4건 (범용전기수술기) · (주)피에이치 · 정상 | 사진 모델명 든 허가 · 사진 · 3차 | 22 |
| 아큐어 |  | 아큐어프러스 (반도체레이저수술기) · 현성메디텍 · 취소 | 잡음 — 다른 제품일 수 있음 · 원천 이름 | 1 |
| 에이전 |  | COTENZA (범용 전기 수술기) · (주)제이시스메디칼 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 105 |
| 온다 | ● DEV-025 | SSONDAR-SHARK (전기 수술 장치) · 쏜다(주) · 정상 | 검색어 든 허가 · 추측 | 1 |
| 올리지오X | ● DEV-010 | Oligio X (범용전기수술기) · 원텍(주) · 정상 | 사진 모델명 든 허가 · 사진 · 3차 | 122 |
| 울쎄라 | ● DEV-038 | Ultherapy Prime (집속형초음파자극시스템) · 멀츠아시아퍼시픽피티이엘티디 · 정상 | 이름 든 허가 · 원천 이름 · Hub 영문명 · 사진 · 업체 목록 | 14 |
| 울쎄라피프라임 | ● DEV-029 | Ultherapy Prime (집속형초음파자극시스템) · 멀츠아시아퍼시픽피티이엘티디 · 정상 | 사진 모델명 든 허가 · 사진 · 웹 · 업체 목록 | 14 |
| 울트라셀 |  | ULTRAcel [zi:]외 1건 (집속형초음파자극시스템) · (주)제이시스메디칼 · 정상 | 사진 모델명 든 허가 · 사진 · 업체 목록 | 103 |
| 울트라셀Q+ |  | COTENZA (범용 전기 수술기) · (주)제이시스메디칼 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 103 |
| 울트라포머MPT |  | ULTRAFORMER MPT PLUS (집속형 초음파 자극 시스템) · (주)클래시스 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 121 |
| 인모드 | ● DEV-008 | InMode (반도체 레이저 수술기) · (주)신한네트웍스 · 정상 | 이름 든 허가 · 원천 이름 · Hub 영문명 · 사진 | 2 |
| 쿨소닉 | ● DEV-036 | Liftera Cool외 1건 (집속형 초음파 자극 시스템) · (주)아스테라시스 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 20 |
| 쿨페이즈 |  | Coolfase-B외 3건 (범용 전기 수술기) · (주)아스테라시스 · 정상 | 검색어 든 허가 · 웹 · 업체 목록 | 20 |
| 텐써마 | ● DEV-037 | 10 THERMA (범용전기수술기) · 텐텍(주) · 정상 | 사진 모델명 든 허가 · 사진 · 업체 목록 | 18 |
| 텐쎄라 | ● DEV-016 | 10THERA (집속형초음파자극시스템) · (주)아스테라시스 · 정상 | 사진 모델명 든 허가 · 사진 · 3차 | 138 |
| 튠페이스 | ● DEV-032 | Accent Prime (범용전기수술기) · 알마코리아 유한회사 · 정상 | 사진 모델명 든 허가 · 사진 · 웹 · 3차 | 126 |
| 펠레베 |  | Pelleve S5-IEC (범용전기수술기) · 오큐텍 · 취소 | 검색어 든 허가 · 추측 | 2 |
| 포커스듀얼 |  | ELLISE (의료용 레이저 조사기) · 원텍(주) · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 27 |
| 리저브 |  | **못 찾음** | — | 0 |
| 바이캐빈 |  | **못 찾음** | — | 0 |
| 아폴로 |  | **못 찾음** | — | 0 |
| 에브넥 |  | **못 찾음** | — | 0 |
| 클래리파이 |  | **못 찾음** | — | 0 |
| 트릴리프트 |  | **못 찾음** | — | 0 |
| 하이푸니 |  | **못 찾음** | — | 0 |

### M10 HIFES/EMS (10)

| 원장 이름 | 현장 | 찾은 식약처 품목 (공식명 · 업체 · 상태) | 어떻게 · 근거 | 후보 |
|---|---|---|---|---|
| 엠페이스(EMFACE) | ● DEV-026 | EMFACE (범용전기수술기) · 비티엘메디컬테크놀로지코리아(유) · 정상 | **자동**(규칙 A) · 원천 이름 · 사진 | 1 |
| 바넥스프로 |  | Vanquish Me (초단파자극기) · 비티엘메디컬테크놀로지코리아(유) · 정상 | 검색어 든 허가 · 추측 | 1 |
| 스팀슈어 |  | StimSure (의료용전자기발생기) · (주)루트로닉 · 취소 | 검색어 든 허가 · 웹 · 3차 | 1 |
| 엠스컬프트 |  | EMSCULPT NEO (초단파 자극기) · 비티엘메디컬테크놀로지코리아(유) · 정상 | 검색어 든 허가 · 추측 · 업체 목록 | 21 |
| 엠스컬프트NEO |  | EMSCULPT NEO (초단파 자극기) · 비티엘메디컬테크놀로지코리아(유) · 정상 | 검색어 든 허가 · 추측 · 업체 목록 | 21 |
| 엠스컬프트네오 |  | EMSCULPT NEO (초단파 자극기) · 비티엘메디컬테크놀로지코리아(유) · 정상 | 검색어 든 허가 · 추측 · 업체 목록 | 21 |
| 엠페이스 | ● DEV-026 | EMFACE (범용전기수술기) · 비티엘메디컬테크놀로지코리아(유) · 정상 | 사진 모델명 든 허가 · 사진 · 추측 · 업체 목록 | 21 |
| 쿨톤 |  | CoolSculpting Elite System (의료용저온기) · 한국애브비(주) · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 3 |
| 트루스컬프트 |  | truSculpt flex (간섭전류형저주파자극기) · (주)큐텍코리아 · 취소 | 검색어 든 허가 · 추측 | 2 |
| 이볼브 |  | **못 찾음** | — | 0 |

### M11 니들RF (12)

| 원장 이름 | 현장 | 찾은 식약처 품목 (공식명 · 업체 · 상태) | 어떻게 · 근거 | 후보 |
|---|---|---|---|---|
| 모르페우스8 |  | Morpheus-A외 1건 (3등급의료용조합자극기) · (주)이노진 · 취소 | 검색어 든 허가 · 추측 | 2 |
| 비바체 |  | 비바체 (전동식 모유 착유기) · 유니맘 · 정상 | 이름 든 허가 · 원천 이름 | 75 |
| 셀리뉴 |  | SCARLET PRO™ (범용 전기 수술기) · (주)비올메디컬 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 31 |
| 스칼렛프로 |  | SCARLET PRO™ (범용 전기 수술기) · (주)비올메디컬 · 정상 | 검색어 든 허가 · 웹 · 업체 목록 | 31 |
| 시크릿RF |  | Secret DUO (반도체레이저수술기) · (주)클래시스 · 정상 | 검색어 든 허가 · 추측 | 4 |
| 실펌X |  | SYLFIRM H™ (범용 전기 수술기) · (주)비올메디컬 · 정상 | 검색어 든 허가 · 웹 · 업체 목록 | 32 |
| 아그네스 |  | AGNES Ultra (범용 전기 수술기) · (주)아그네스메디컬 · 정상 | 이름 든 허가 · Hub 영문명 · 사진 · 추측 | 5 |
| 인피니 |  | V1 INFINITY (집속형 초음파 자극 시스템) · (주)이끌레오 · 정상 | 검색어 든 허가 · 웹 · 3차 | 190 |
| 쿼드세이 |  | QUADESSY외 1건 (범용 전기 수술기) · (주)클래시스 · 정상 | 검색어 든 허가 · 웹 · 업체 목록 | 121 |
| 트윈픽셀 |  | ESK-3277PS (고주파 자극기) · (주)은성글로벌 · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 141 |
| 포텐자 | ● DEV-022 | POTENZA™ (범용전기수술기) · (주)제이시스메디칼 · 정상 | 사진 모델명 든 허가 · 사진 · 웹 · 3차 | 36 |
| 프라임RF |  | **못 찾음** | — | 0 |

### M12 마이크로니들링(MTS) (2)

| 원장 이름 | 현장 | 찾은 식약처 품목 (공식명 · 업체 · 상태) | 어떻게 · 근거 | 후보 |
|---|---|---|---|---|
| 더마펜4 |  | Dermapen③ (의약품흡수유도피부자극기) · (주)우리메카 · 정상 | 검색어 든 허가 · 추측 | 2 |
| 스킨스탬프 |  | **못 찾음** | — | 0 |

### M13 플라즈마 (3)

| 원장 이름 | 현장 | 찾은 식약처 품목 (공식명 · 업체 · 상태) | 어떻게 · 근거 | 후보 |
|---|---|---|---|---|
| 플라듀오 |  | PLADUO (전기 수술 장치) · (주)쉬엔비 · 정상 | 검색어 든 허가 · 웹 · 3차 | 1 |
| 뉴라클플라즈마 |  | **못 찾음** | — | 0 |
| 플라스젠 |  | **못 찾음** | — | 0 |

### M14 크라이오리포라이시스 (4)

| 원장 이름 | 현장 | 찾은 식약처 품목 (공식명 · 업체 · 상태) | 어떻게 · 근거 | 후보 |
|---|---|---|---|---|
| 바넥스 |  | Vanquish Me (초단파자극기) · 비티엘메디컬테크놀로지코리아(유) · 정상 | 검색어 든 허가 · 추측 | 1 |
| 쿨미니 |  | CoolSculpting Elite System (의료용저온기) · 한국애브비(주) · 정상 | 검색어 든 허가 · 추측 · 업체 목록 | 3 |
| 쿨스컬프팅 |  | CoolSculpting Elite System (의료용저온기) · 한국애브비(주) · 정상 | 검색어 든 허가 · 추측 · 업체 목록 | 3 |
| 크라이오듀얼 |  | **못 찾음** | — | 0 |

### M15 메디컬스킨케어 (73)

| 원장 이름 | 현장 | 찾은 식약처 품목 (공식명 · 업체 · 상태) | 어떻게 · 근거 | 후보 |
|---|---|---|---|---|
| LDM | ● DEV-048 | LDM-Smart Tri외 1건 (초음파 자극기) · (주)웰코멧아시아 · 정상 | 이름 든 허가 · 원천 이름 · Hub 영문명 | 7 |
| 미라젯 | ● DEV-054 | mirajet Plus+2940외 1건 (기타레이저수술기) · (주)레이저옵텍 · 정상 | 사진 모델명 든 허가 · 사진 · 3차 | 1 |
| 실크필 |  | SilkPeel (의료용삭피장치) · (주)한라인터내쇼날 · 취소 | 검색어 든 허가 · 추측 | 2 |
| 아쿠아퓨어 |  | AQUAPURE II(AQ2-M200)외 2건 (전동식 의료용 흡인기) · (주)클래시스 · 정상 | 검색어 든 허가 · 웹 · 3차 | 2 |
| 아쿠아필 | ● DEV-040 | 아쿠아필(Aqua Peel) (전동식의료용흡인기) · 엠아이테크 · 정상 | 이름 든 허가 · 원천 이름 · 3차 | 4 |
| 에어젯 |  | AIRJETII (전동식의약품주입펌프) · (주)유니온메디칼 · 정상 | 검색어 든 허가 · 추측 | 3 |
| 옴니럭스 |  | Omnilux revive (광선조사기) · (주)신한씨스텍 · 취소 | 검색어 든 허가 · 추측 | 2 |
| 옴니룩스 |  | Omnilux revive (광선조사기) · (주)신한씨스텍 · 취소 | 검색어 든 허가 · 추측 | 2 |
| 제트필 |  | JetPeel 3V (공압분사연삭기) · (주)스킨엠디코리아 · 취소 | 검색어 든 허가 · 추측 | 4 |
| 하이드라페이셜 |  | HydraFacialTM System & Accessories (의료용삭피장치) · 신한이앤아이 · 취소 | 검색어 든 허가 · 추측 | 1 |
| 힐라이트 |  | HEALITE II (2등급 의료용 조합 자극기) · 주식회사 사이노슈어루트로닉테크놀로지 · 정상 | 검색어 든 허가 · 추측 | 6 |
| 노보젯 |  | **못 찾음** | — | 0 |
| 더마샤인 | ● DEV-050 | **못 찾음** | — | 0 |
| 데마루치 |  | **못 찾음** | — | 0 |
| 라라젯 |  | **못 찾음** | — | 0 |
| 라라젯 (클렌징) |  | **못 찾음** | — | 0 |
| 메소건 |  | **못 찾음** | — | 0 |
| 바이오프로톤 |  | **못 찾음** | — | 0 |
| 벨라소닉 |  | **못 찾음** | — | 0 |
| 비타인젝터 |  | **못 찾음** | — | 0 |
| 셀라이트 |  | **못 찾음** | — | 0 |
| 소노퀸 |  | **못 찾음** | — | 0 |
| 아스트로더 | ● DEV-046 | **못 찾음** | — | 0 |
| 아쿠아젯 |  | **못 찾음** | — | 0 |
| 옥시덤 |  | **못 찾음** | — | 0 |
| 올타이트 | ● DEV-017 | **못 찾음** | — | 0 |
| 제네오X |  | **못 찾음** | — | 0 |
| 큐어젯 | ● DEV-051 | **못 찾음** | — | 0 |
| 크라이오셀 |  | **못 찾음** | — | 0 |
| 하이쿡스 | ● DEV-055 | **못 찾음** | — | 0 |
| 헤어셀 |  | **못 찾음** | — | 0 |
| ASA필 |  | 조회 안 함 — Algae Soft Abrasion · 해초 미세침 · 재생 · 해조류 추출물과 미세침을 이용한 순한 각질제… | 의약품·의료기기 밖 | — |
| CO2필 |  | 조회 안 함 — 탄산팩 · CO2+O2 교환 · 노폐물 배출+피부결 · 탄산가스를 이용해 피부의 산소공급을 촉진하고 노폐물 … | 의약품·의료기기 밖 | — |
| FCR필 |  | 조회 안 함 — Fermented Complex Regeneration · 발효 복합 재생 필링 · 발효 복합 성분을 활용한… | 의약품·의료기기 밖 | — |
| PHA필 |  | 조회 안 함 — 물톡스 · PHA 기반 · 수분보호막+보습+항산화 · 저자극 · PHA(폴리히드록시산) 기반의 저자극 수분 … | 의약품·의료기기 밖 | — |
| PRX필 |  | 조회 안 함 — PRX-T33 · TCA+H2O2+코직산 · 비박리성 바이오리버탈라이저 · TCA, 과산화수소, 코직산을 결… | 의약품·의료기기 밖 | — |
| 골드필 |  | 조회 안 함 — 금(Gold) 나노입자 · 항산화+항노화+피부 활성화 · 금 나노입자를 활용한 프리미엄 안티에이징 케미컬 필… | 의약품·의료기기 밖 | — |
| 그린필 |  | 조회 안 함 — 오리지널 GREEN PEEL · 허벌 필링 · 독일 · 피부재생 · 독일산 천연 허브 성분을 이용한 기계적 … | 의약품·의료기기 밖 | — |
| 닥토필 |  | 조회 안 함 — 5세대 내추럴필링+엑소좀 · 페이스/바디/두피 · 5세대 내추럴필링과 엑소좀을 결합한 페이스/바디/두피 종합… | 의약품·의료기기 밖 | — |
| 디멜라필 |  | 조회 안 함 — 산소+비타민C · 미백+주름개선+콜라겐 · 산소와 비타민C를 결합한 미백 및 항노화 전문 화학적 필링 시술 | 의약품·의료기기 밖 | — |
| 라라닥터 |  | 조회 안 함 — 5세대 LHA · 라라필 의료용 업그레이드 · PLLA+H2Sol+인큐브501 · 5세대 LHA와 PLLA … | 의약품·의료기기 밖 | — |
| 라라필 |  | 조회 안 함 — 효소 기반 온순한 필링 | 의약품·의료기기 밖 | — |
| 마꾸필 |  | 조회 안 함 — 마그네슘+구리 복합 · 미네랄 공급+재생 · 마그네슘과 구리 복합체를 이용한 미네랄 공급 피부 재생 필링 | 의약품·의료기기 밖 | — |
| 물톡스 |  | 조회 안 함 — PHA 기반 물광 필링 · 수분보호막+보습 · PHA(폴리하이드록시산) 기반의 순한 각질제거와 동시에 수분공… | 의약품·의료기기 밖 | — |
| 미라클필링 |  | 조회 안 함 — 담수해면체 · 천연 필링 · 재생+모공+블랙헤드 · 담수해면체 스피큘을 이용한 물리적 각질제거와 천연 성분의… | 의약품·의료기기 밖 | — |
| 미라필링 |  | 조회 안 함 — 산호칼슘미세침 · 산호 칼슘 미세침을 이용한 물리적 각질 제거 및 재생 시술 | 의약품·의료기기 밖 | — |
| 밀크필 |  | 조회 안 함 — 워터제트 기반 물리적 클렌징 | 의약품·의료기기 밖 | — |
| 베이비필 |  | 조회 안 함 — 초저자극 · 민감피부/아토피 가능 · 보습+진정 · 초저자극 성분으로 민감피부와 아토피 피부에도 적용 가능한… | 의약품·의료기기 밖 | — |
| 블랙필 |  | 조회 안 함 — 글리콜산 기반 표재성 필링 | 의약품·의료기기 밖 | — |
| 블랙필링 |  | 조회 안 함 — TCA+살리실 · TCA와 살리실산이 복합된 중강도 화학 박피 | 의약품·의료기기 밖 | — |
| 산소필 |  | 조회 안 함 — 비타민+산소 공급 · 혈액순환 · 미백+탄력+항노화 · 비타민과 산소를 공급하여 혈액순환을 개선하고 미백, … | 의약품·의료기기 밖 | — |
| 살몬필 |  | 조회 안 함 — 연어 PDRN 성분 · 재생+보습+항염 · 연어 유래 PDRN 성분으로 피부 재생과 보습, 항염 효과를 제공… | 의약품·의료기기 밖 | — |
| 생크림필 |  | 조회 안 함 — 생크림 텍스처 · 저자극 각질 녹임 · 보습+톤업 · 생크림 같은 부드러운 텍스처로 각질을 온화하게 녹이면서… | 의약품·의료기기 밖 | — |
| 솔코세릴필링 |  | 조회 안 함 — 천연성분 · 천연 성분을 이용한 순한 화학적 박피술 | 의약품·의료기기 밖 | — |
| 아미노필 |  | 조회 안 함 — 아미노산 기반 · 영양+각질제거 · 아미노산 기반의 순한 영양 공급형 각질제거 필링으로 민감한 피부에도 적용… | 의약품·의료기기 밖 | — |
| 알라딘필링 |  | 조회 안 함 — 위축성 흉터 전문 포인트 필링 | 의약품·의료기기 밖 | — |
| 알렉스필 |  | 조회 안 함 — 알렉산드라이트 원리 · 멜라닌 타겟 · 미백+솜털제모 · 알렉산드라이트 레이저 원리를 응용한 멜라닌 타겟 미… | 의약품·의료기기 밖 | — |
| 여우필 |  | 조회 안 함 — FOxC Peel · 수분+각질+여드름/미백/탄력 관리 · 여드름, 미백, 탄력을 동시에 개선하는 복합 화학… | 의약품·의료기기 밖 | — |
| 예스필 |  | 조회 안 함 — 민감/예민 피부 전용 · 피부장벽 개선 · 저자극 · 민감성 피부를 위한 저자극 화학 필링으로 피부장벽 강화… | 의약품·의료기기 밖 | — |
| 옐로우필링 |  | 조회 안 함 — 레티놀복합 · 레티놀 복합성분을 이용한 화학적 박피술 | 의약품·의료기기 밖 | — |
| 우유필 |  | 조회 안 함 — 우유단백 유래 락틱산 · 보습+각질제거 · 건성피부 · 우유단백 유래 락틱산을 이용한 순한 화학적 필링으로 … | 의약품·의료기기 밖 | — |
| 이지피틱필 |  | 조회 안 함 — Easy Phytic Peel · 피틱산 · 항산화+미백+저자극 · 피틱산 기반의 항산화, 미백, 저자극 화… | 의약품·의료기기 밖 | — |
| 진주필 |  | 조회 안 함 — 진주 분말 · 미백+영양+광채 · 진주 분말을 활용한 미백과 영양 공급을 통해 피부 광채를 개선하는 순한 필… | 의약품·의료기기 밖 | — |
| 체리필 |  | 조회 안 함 — 체리 추출 과일산 · 비타민+각질 · 체리 추출 과일산과 비타민을 활용한 순한 화학적 각질제거 필링 | 의약품·의료기기 밖 | — |
| 콜라겐필 |  | 조회 안 함 — 콜라겐 유효성분 침투 · 탄력+재생 · 콜라겐 성분을 피부 깊숙이 침투시켜 탄력 개선과 재생을 돕는 피부과 … | 의약품·의료기기 밖 | — |
| 쿰스필 |  | 조회 안 함 — 제스너 솔루션 변형 · AHA+BHA 혼합 · 여드름 · 제스너 솔루션을 변형한 AHA+BHA 혼합 화학 필… | 의약품·의료기기 밖 | — |
| 퀸즈필 |  | 조회 안 함 — PHA+히알루론산+펩타이드+아미노산 22종 · 필링+영양 동시 · PHA 기반의 순한 각질 제거와 동시에 히… | 의약품·의료기기 밖 | — |
| 크랜베리필 |  | 조회 안 함 — 크랜베리 추출 과일산 · 항산화+각질 · 크랜베리 추출 과일산을 이용한 항산화 성분이 함유된 순한 각질 제거… | 의약품·의료기기 밖 | — |
| 탄앤막필링 |  | 조회 안 함 — 알칼리 촉매 · TAN(표피재생)+MAHK(보호막) 2단계 · 알칼리 촉매를 이용한 표피재생과 보호막 형성의… | 의약품·의료기기 밖 | — |
| 플라필 |  | 조회 안 함 — 플래티넘필 · PHA+LHA+백금 · 초저자극 · 항산화+속건조 개선 · PHA와 LHA, 백금 성분을 결합… | 의약품·의료기기 밖 | — |
| 핑크필 |  | 조회 안 함 — 복합산 마이크로필링 | 의약품·의료기기 밖 | — |
| 해초필 |  | 조회 안 함 — 담수해면체 미세침 · 물리적 각질제거+재생 유도 · 소프트필 · 담수해면체 미세침을 이용한 물리적 각질제거 … | 의약품·의료기기 밖 | — |
| 호박필 |  | 조회 안 함 — 유산 기반 온순 필링 | 의약품·의료기기 밖 | — |

### M16 수액치료 (15)

| 원장 이름 | 현장 | 찾은 식약처 품목 (공식명 · 업체 · 상태) | 어떻게 · 근거 | 후보 |
|---|---|---|---|---|
| 뉴비쥬 |  | 뉴비쥬주(콜산) · (주)메디톡스 · 정상 | **자동**(규칙 A) · 원천 이름 · 업체 목록 | 10 |
| 밀리핏주사 |  | 밀리핏주사(데옥시콜산) · 동국제약(주) · 정상 | **자동**(규칙 A) · 원천 이름 | 1 |
| 바이블주 |  | 바이블주(데옥시콜산) · (주)한국비엠아이 · 정상 | **자동**(규칙 A) · 원천 이름 · 업체 목록 | 54 |
| 올리핏주 |  | 올리핏주(데옥시콜산) · (주)휴메딕스 · 정상 | **자동**(규칙 A) · 원천 이름 · 업체 목록 | 79 |
| 원더브이 |  | 원더브이주(데옥시콜산) · (주)종근당 · 정상 | **자동**(규칙 A) · 원천 이름 | 1 |
| 펜카이라주 |  | 펜카이라주(데옥시콜산) · (주)펜믹스 · 정상 | **자동**(규칙 A) · 원천 이름 · 업체 목록 | 39 |
| LDM초음파관리 |  | LDM-Smart Tri외 1건 (초음파 자극기) · (주)웰코멧아시아 · 정상 | 검색어 든 허가 · 웹 · 3차 | 105 |
| 리포린 |  | 크레지정2.5밀리그램(로수바스타틴칼슘) · 삼익제약(주) · 정상 | 잡음 — 다른 제품일 수 있음 · 업체 목록 | 192 |
| 벨라콜린 |  | 벨라콜린주(데옥시콜산) · (주)엘지화학 · 정상 | 이름 든 허가 · 원천 이름 | 1 |
| 벨카이라 |  | 브이벨라주(데옥시콜산) · 대한뉴팜(주) · 정상 | 검색어 든 허가 · 추측 | 9 |
| 브이올렛 |  | 브이올렛주(데옥시콜산) · (주)대웅제약 · 정상 | 이름 든 허가 · 원천 이름 | 1 |
| 카이벨라 |  | 엘라히어주(미르베툭시맙소라브탄신) · 한국애브비(주) · 정상 | 계열만 맞음 — 확인 필요 · 업체 목록 | 40 |
| 태반주사멜스몬 |  | 멜스몬주(자하거추출물) · (주)한국멜스몬 · 정상 | 이름 든 허가 · 원천 이름 | 1 |
| 아큐주사 |  | **못 찾음** | — | 0 |
| 팻킬주사 |  | **못 찾음** | — | 0 |

### M17 줄기세포치료 (3)

| 원장 이름 | 현장 | 찾은 식약처 품목 (공식명 · 업체 · 상태) | 어떻게 · 근거 | 후보 |
|---|---|---|---|---|
| AAPE |  | 조회 안 함 — ADSC추출단백질 · 지방줄기세포 추출단백질을 이용한 고농도 재생치료 | 의약품·의료기기 밖 | — |
| 노바스템 |  | 조회 안 함 — 줄기세포 유래 재생인자 제품 | 의약품·의료기기 밖 | — |
| 미라셀 |  | 조회 안 함 — 줄기세포 유래 성장인자 제제 | 의약품·의료기기 밖 | — |

---

## 4. 바뀐 것 (v2 → v3)

| v2 → v3 | 건수 |
|---|---|
| candidate→candidate | 174 |
| none→none | 82 |
| no_service→no_service | 45 |
| auto→auto | 29 |
| none→candidate | 10 |

- 못 찾음 → 찾음(근거별, 한 제품에 근거 여럿이면 각각 셈): 웹 8, 사진 2
- 후보 맨 위가 「계열만 · 잡음」 → 「이름 든 허가」로 바뀐 것(근거별): 웹 31, Hub 영문명 1, 사진 15
- 규칙 A(Hub 영문명)로 새로 자동: 0
- 후보 전체의 근거 분포: 업체 목록 8394, 웹 495, 추측 156, 원천 이름 151, Hub 영문명 112, 사진 75
- 맨 위 후보의 근거 분포: 업체 목록 126, 웹 53, 추측 51, 원천 이름 47, 사진 29, Hub 영문명 26
- Hub 영문명: terminology/matrix(제품 59 · 항목 13) + glossary/matrix(158행)에서 원장 38개에 41쌍. 대부분 v1 이 products.json `name_en` 으로 이미 조회한 이름과 같아 **새 질의는 거의 없고**, v2 의 추측 검색어(YVOIRE 등)를 원천 근거로 바꿔 준 효과가 크다
- 식약처 호출: 이번 3차 **300회**(상한 300 · 질의 350 · 상태 {'ok': 350}). 모델명 검색은 대소문자 구분 부분 일치라 읽은 그대로 → 0건이면 대문자로 한 번 더. 이름이 안 든 응답(ATOM → ATOMIZER 같은 부분 일치)과 치과 · 마스크 · CPAP 같은 남의 계열은 후보에서 뺐다

## 5. 미결

- **사진 판독 불가 8**: DEV-023 슈링크유니버스, DEV-039 스텔라듀오, DEV-062 엑셀브이-제네시스, DEV-078 01_보톡스·필러 시술 이미지, DEV-080 22_광선치료기, DEV-090 25_He-Ne, DEV-091 12_레블라이트, DEV-101 09_UP3000
- **이름 차이로 이어 준 것 · 사진과 원장이 어긋난 것 11** — 게이트에서 확인: DEV-005 아포지플러스 → 원장 아포지엘리트플러스와 다른 모델(Apogee+); DEV-009 써마지 → 써마지 ↔ 써마지FLX; DEV-017 올타이트 → 사진에 올타이트 표기 없음(Innoxus 만); DEV-023 슈링크유니버스 → 사진 판독 불가 — 이름(파일명)으로만 이음; DEV-028 티타늄 → 티타늄 ↔ 소프라노 티타늄; DEV-032 튠페이스 → 사진은 Alma Accent Prime(Tune 표기) — 원장 업체 클래시스와 다름; DEV-033 볼뉴머 → 사진에 CLASSYS 로고만; DEV-046 아스트로돔(우주인토닝) → 아스트로돔 ↔ 원장 아스트로더 — 같은 기기인지 확인 필요; DEV-048 LDM-DCM → LDM-DCM ↔ LDM; DEV-062 엑셀브이-제네시스 → 엑셀브이-제네시스 ↔ 엑셀브이 · 사진 판독 불가; DEV-066 포토나스타워커 → 포토나스타워커 ↔ 스타워커
- 신규 후보 중 웹에서 못 찾은 것 17: DEV-015 이브타이탄, DEV-018 이래비티, DEV-020 엔진리프팅, DEV-034 벨르업, DEV-041 수소토닝, DEV-042 더마큐어, DEV-045 크라이오 멀티마스터, DEV-047 울킨, DEV-053 AUTO MTS, DEV-060 피코라이트블랙, DEV-061 피코 라이트, DEV-069 아톰레이저, DEV-072 3D 메타뷰, DEV-073 마크뷰, DEV-074 스캐나, DEV-075 카프리레이저, DEV-076 아큐토닝
- **웹 미조사 22** — 세션 WebSearch 한도(200회) 소진: 크라이오듀얼, 라라젯 (클렌징), 옥시덤, 아스트로더, 셀라이트, 데마루치, 바이오프로톤, 소노퀸, 큐어젯, 미라젯, 벨라소닉, 하이쿡스, 더마샤인, 라라젯, 노보젯, 아쿠아젯, 크라이오셀, 메소건, 비타인젝터, 헤어셀, 올타이트, 리포린
- 웹에서 「일반 시술명(특정 제품 아님)」으로 본 것 13: 잼버실, V리프트, 앵커리프트, 캐번실, 코그실루프, 투와이실, 로즈실, 면사리프트, 텐선실, 허니콤실, 스킨스탬프, 팻킬주사, 아큐주사
- 웹이 원장 업체 표기와 다르다고 한 것(원천 수정 목록 후보 · 사람 확인): 리즈톡신: 정식명 리즈톡스(주). 의약품이라 의료기기 TYPE_NAME 아님; 아테콜: HA 아님 — PMMA+콜라겐 영구 필러. 국내 수입사·현재 허가 여부 미확인; 디클래씨: CaHA 기반 콜라겐 부스터(PDLLA 아님). 해외 브랜드 Facetem. 제조사 원천은 미확인, 영문 철자 Diclace는…; 라풀렌: PLLA 아님 — 다공성 PCL 마이크로스피어 필러; ASCE+엑소좀: 엑소좀 화장품이라 MFDS 의료기기 DB 대상 아님; 바이리즌: 정식명 바이리즌 스킨부스터 HA(HA 기반, PCL 아님). 화장품/의료기기 구분 및 영문 공식명 미확인; 소프라노 티타늄: 다이오드 제모 레이저(755/810/1064nm)를 '티타늄 리프팅'으로 사용. 국내 수입사 확인 못함(고주파 아님); 버츄RF: maker_hint 비올은 오류 — 쉬엔비 제조, 미국은 Cartessa 유통. 실제는 RF 마이크로니들; 올리지오X: maker_hint 클래시스는 오류 — 원텍 모노폴라 RF; 튠페이스: maker_hint 클래시스는 오류 — 튠페이스는 알마 Accent Prime(40.68MHz RF+초음파) 시술명. 국내 수…; 카이벨라: 데옥시콜산 주사제(의약품, 의료기기 아님 — MFDS 의약품 DB 대상). 국내 허가·수입사 미조사
- **같은 허가가 원장 여러 제품의 맨 위에 걸린 것 5** — 원장 제품이 실제로 다른 모델인지(예: 올리지오 ↔ 올리지오X) 게이트에서 확인: 디스포트 = 에이비오톡신; 볼뉴머 = 볼뉴머; 울쎄라 = 울쎄라피프라임; 올리지오 = 올리지오X; 엠페이스(EMFACE) = 엠페이스
- 웹 검색은 세션 한도로 신규 후보 DEV-074 스캐나 · DEV-075 카프리레이저 · DEV-076 아큐토닝도 미조사(사진 모델명으로만 식약처 조회)
- 식약처 오늘 누적 938/1000 — 남은 62회로는 위 미조사분을 다 못 돈다. 다음 판은 KST 내일

## 6. 기술 메모

- 각 product: `in_use_at_clinic`(사용 중 사진 번호) · `sample_photos` · `photo_evidence`(사진 경로 · 읽은 글자) · `hub_en` · `web`(출처 URL) · `match.v2_status` · `match.auto_rule`(exact · A · A(hub_en)) · `match.auto_keys` · 후보마다 `via`(source · hub_en · photo · web · guess · company_list) · `evidence`(사진 경로 / URL) · `photo_confirms`(사진에서 읽은 모델명이 허가 모델명에 듦)
- 최상위 `new_ledger_candidates`(신규 후보) · `photos`(109장 판독 결과와 원장 연결). 사진 파일 · 키 · 응답 원문은 넣지 않았다(경로만)
- auto: v2 자동 4 + 규칙 A 25 는 그대로(게이트 페이지 판정 그대로 옮김). 사진 · 웹 · 추측 · 업체 목록 근거는 auto 로 가지 않는다
- 같은 성분 · 함량만 다른 허가는 한 제품(+ 규격) — 게이트 화면에서 한 줄로 묶는 규칙은 v2 와 같다(정렬 · 묶음 키: 의약품 = 품목명에서 괄호 · 용량 뗀 이름 + 업체, 의료기기 = 모델명에서 「외 N건」 뗀 이름 + 업체)
