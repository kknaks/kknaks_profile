# 수출 전용 7행 — 국내 내수 허가 재조사 (2026-10-28)

원장 수정 없음. 근거 상세·질의는 `step1-domestic7.json`.

| 행 | 결과 | 내수 허가 · 근거 |
|---|---|---|
| `M11-P-1` 인트라셀 | 내수 허가 찾음 — 단 유효기간 만료(현재 유효한 내수 허가 없음) | 제허 09-682 호 (INTRAcel · 만료(유효기간) 2026-09-01) |
| `M3-3-2` 고우리 | 내수 허가 찾음 | 제허 25-634 호 (G.O.U.R.I., Elemoi, ELLINIQUE, BELLUXI-P · 정상) |
| `M9-1-6` 더블로 골드 | 내수 허가 찾음 | 제허 11-946 호 (DOUBLO Lifting · 정상) |
| `auto-M7-1775361076707` 잼버실 | 내수 허가 찾음 | 제허 13-1507 호 (NEO LINE Normal, Nubelline, NOVACUTAN No · 정상) |
| `auto-M7-1775362571755` N코그 | 국내 유통 확인 · 허가 특정 못 함(→ 허가번호 미확인 규칙) | — |
| `auto-M8-1775364775119` 에코2 에볼루션 | 국내 유통 근거 없음(→ 확인 불가) | — |
| `new-DEV-039` 스텔라듀오 | 국내 유통 근거 없음(→ 확인 불가) | — |

## 인트라셀 (`M11-P-1`) — 내수 허가 찾음 — 단 유효기간 만료(현재 유효한 내수 허가 없음)

- 내수 허가 **제허 09-682 호** · 범용전기수술기 · INTRAcel · 모델 IEZ, INTRAcel · 허가 2009-08-28 · xprtppYn 아니오 · 유효 2020-10-08 ~ 2026-08-31 · 만료(유효기간) 2026-09-01 — emedi 품목 상세 POST https://emedi.mfds.go.kr/search/data/item meddevItemSeq=2009004014 · 목록 query2=INTRAcel
- 같은 업체 내수 범용전기수술기 정상 허가 13-985(AcGen) · 19-78(POTENZA) · 23-472(DENSITY) — INTRAcel 이름·모델 없음
- INTRAcel 이름 허가 중 정상인 것(17-689 · 13-1858 · 13-1651 · 12-1085 · 09-747 · 09-831)은 전부 xprtppYn=예(수출용)
- 제인 09-1033 INTRAcel Tip(전극)은 내수지만 소모품 — 본체 허가 아님(기존 판정 유지)
- 모두케어 제허12-1387 INTRAcel K TM 취하 2015-04-09 · 풍림파마텍 Intracell-P/F 는 다른 제품(PRP 기구)
- 국내 유통: 근거 못 찾음 — data-anyang 「인트라셀/INTRAcel」 0건 · 웹 검색 결과 없음
- 메모: 원장 history 에 이미 09-682 「만료(유효기간)」로 있음 — 이번 조사로 이 허가가 내수(xprtppYn=아니오)임을 확인. 상태를 「만료」로 볼지 「확인 불가」로 둘지는 정할 것
- 질의: 식약처 의료기기 품목허가 API MdlpPrdlstPrmisnInfoService06/getMdlpPrdlstPrmisnList05 entrps=제이시스메디칼 (103건) / https://emedi.mfds.go.kr/search/data/list query2=INTRAcel · INTRACELL · 인트라셀(0) / emedi 품목 상세 POST https://emedi.mfds.go.kr/search/data/item meddevItemSeq=(제이시스 범용전기수술기·전극 정상 31건 상세) / WebSearch 「인트라셀 고주파 피부과 시술 제이시스메디칼」「"인트라셀" 여드름흉터 의원 가격」

## 고우리 (`M3-3-2`) — 내수 허가 찾음

- 내수 허가 **제허 25-634 호** · 조직 수복용 재료 · G.O.U.R.I., Elemoi, ELLINIQUE, BELLUXI-PCL · 모델 DLMR02, DLMR01 · 허가 2025-09-11 · xprtppYn 아니오 · 유효 2025-09-11 ~ 2030-09-10 · 정상 — emedi 품목 상세 POST https://emedi.mfds.go.kr/search/data/item meddevItemSeq=2025005234 · 목록 entpName=덱스레보
- 놓친 이유: 제품명 표기가 「G.O.U.R.I.」(점 포함)라 query2=GOURI 에 안 걸렸다
- 덱스레보 조직수복용재료 6건 중 내수는 25-634 하나 — 19-187(GOURI) · 26-447(GOURI HA) · 21-310 · 23-849 · 15-223 은 수출용
- 국내 유통: 확인 — 데이뷰의원 안양범계점 「[런칭] 세계최초 액상형 PCL, 고우리 1시린지」 2026-09 이벤트(https://daybeauclinic06.com/branch/event.php?uid=1327) · 라마르프리미어의원 범계역 「고우리 스킨부스터 런칭 이벤트」 팝업(https://www.pclamar.co.kr/STATIC/img/popup/popup_20260831135815_dd23ed01.jpg) — data-anyang prices/ours_데이뷰의원-안양범계점.json · prices_img/c14_라마르프리미어의원-범계역.json
- 메모: 허가 모델 DLMR01 · 제품명 G.O.U.R.I. — 「고우리」 와 같은 이름의 표기 차이(점)만 있음. 연결 여부는 검수 판단
- 질의: 식약처 의료기기 품목허가 API MdlpPrdlstPrmisnInfoService06/getMdlpPrdlstPrmisnList05 entrps=덱스레보 (6건) / https://emedi.mfds.go.kr/search/data/list entpName=덱스레보 (18행) / emedi 품목 상세 POST https://emedi.mfds.go.kr/search/data/item meddevItemSeq=(6건 상세)

## 더블로 골드 (`M9-1-6`) — 내수 허가 찾음

- 내수 허가 **제허 11-946 호** · 집속형초음파자극시스템 · DOUBLO Lifting · 모델 DOUBLO-GOLD, DOUBLO-S, DOUBLO, ULTRA VERA · 허가 2011-08-29 · xprtppYn 아니오 · 유효 2020-10-08 ~ 2027-03-31 · 정상 — emedi 품목 상세 POST https://emedi.mfds.go.kr/search/data/item meddevItemSeq=2011004326 · 목록 entpName=하이로닉(모델 행 DOUBLO-GOLD)
- 18-195(DOUBLO-GOLD™)는 수출용 — 같은 모델 이름 「DOUBLO-GOLD」가 내수 11-946 모델 목록에 있음
- 더블로골드S(auto-M9-1775364775134)는 이미 11-946 · 21-690 에 연결됨(원장) — 같은 허가
- 국내 유통: 이번 조사에서 별도 확인 안 함(허가 모델 일치로 충분) — data-anyang 「더블로」 0건
- 메모: export-recheck 가 M9-1-6 을 후보 대상에 안 넣어 놓쳤던 것으로 보임(candidates 키에 M9-1-6 없음)
- 질의: 식약처 의료기기 품목허가 API MdlpPrdlstPrmisnInfoService06/getMdlpPrdlstPrmisnList05 entrps=하이로닉 (61건) / https://emedi.mfds.go.kr/search/data/list entpName=하이로닉 (91행) / emedi 품목 상세 POST https://emedi.mfds.go.kr/search/data/item meddevItemSeq=(초음파 13건 상세)

## 잼버실 (`auto-M7-1775361076707`) — 내수 허가 찾음

- 내수 허가 **제허 13-1507 호** · 폴리디옥사논봉합사 · NEO LINE Normal, Nubelline, NOVACUTAN Normal, VIFINY Normal, BEAULIGNE Normal, JAMBER, JAMBER I, JAMBER F, JAMBER TANXING, Dr. perfect V-line, epiticon JAMBER, Double Fix Pyramid Jamber, LIPOLIF-T, FILLUP, Piezosilk, N-JAMBER, THE S#VRP JAMBER, ETENNA, Astella JAMBER, Medistream Standard, JAMBER Classic, JAMBER Harmonia, JAMBER AI, Reborn · 모델 CB2106030JF-30, YCB2106030JF-30 · 허가 2013-09-02 · xprtppYn 아니오 · 유효 2020-10-08 ~ 2027-12-31 · 정상 — emedi 품목 상세 POST https://emedi.mfds.go.kr/search/data/item meddevItemSeq=2013006205 · 목록 query2=CB2106030JF-30
- 놓친 이유: 이 허가 제품명은 emedi 목록 행(모델별)에 길게 붙어 있어 query2=JAMBER 첫 1,000행 안에서 잡히지 않은 것으로 보임(네오닥터 전체 7,358행)
- 네오닥터 봉합사 11건 중 내수는 13-1507 · 14-156(Cog 계열 · JAMBER 이름 없음) 둘
- 24-743(JAMBER L) · 24-273(JAMBER V/N) · 24-142(Jamber Rhanchor)는 수출용 — 원장 검색 이름 JAMBER L/V/N 은 수출용 허가 이름이다
- 국내 유통: 확인 — 데이뷰의원 안양범계점 「콜라겐생성 볼륨 잼버실 2줄」 · 유앤아이의원 안양점 「잼버실 4줄」(https://www.ayuni114.co.kr/) · 라마르프리미어의원 범계역 「팔자주름 잼버실 4줄」 — data-anyang prices/*.json
- 메모: 내수 허가 제품명은 「JAMBER」 · 「JAMBER Classic」 등 — 원장 「잼버실」이 이 중 어느 것인지는 출처 없음(허가 단위로는 13-1507 하나)
- 질의: 식약처 의료기기 품목허가 API MdlpPrdlstPrmisnInfoService06/getMdlpPrdlstPrmisnList05 entrps=네오닥터 (18건) / emedi 품목 상세 POST https://emedi.mfds.go.kr/search/data/item meddevItemSeq=(봉합사 11건 상세) / https://emedi.mfds.go.kr/search/data/list query2=CB2106030JF-30

## N코그 (`auto-M7-1775362571755`) — 국내 유통 확인 · 허가 특정 못 함(→ 허가번호 미확인 규칙)

- 연결 안 한 내수 후보 제허 13-2038 호 · 제품명 (없음) · 모델 NFCW26096G 외 2,834건 — emedi 품목 상세 POST https://emedi.mfds.go.kr/search/data/item meddevItemSeq=2013009297
- 연결 안 한 내수 후보 제허 14-152 호 · 제품명 (없음) · 모델 NFL-M05234055E 외 1,379건 — emedi 품목 상세 POST https://emedi.mfds.go.kr/search/data/item meddevItemSeq=2014001111
- N-Cog 이름은 수출용 17-914 제품명에만 있음 · 내수 13-2038 · 14-152 는 제품명 칸이 비어 있다
- 모델 코드 NFC19040G 가 17-914(수출) 와 13-2038(내수) 양쪽에 있음(query2=NFC19040G) — 그러나 제품명은 허가 단위라 이 모델이 N-Cog 인지 근거 없음 · NFC19032B · NFC19042E 는 17-914 에만
- 국내 유통: 확인 — 평촌고운세상피부과의원 비급여 고지표 「주름/탄력/리프팅 > N-COG」 550,000~880,000원(https://pcgowoonss.com/data/editor/2603/78448188b39c1e09e49755ce5e148c59_1773644563_533.png · data-anyang prices_img/c11_평촌고운세상피부과의원.json) · 메디게이트뉴스 2015-10-27 「엔파인더스의 '엔코그'」(https://medigatenews.com/news/3272101004 — 17-914 허가 이전 기사)
- 메모: 2015 기사 시점에 국내 유통 → 그때 유효한 내수 허가(13-2038 · 14-152 중) 아래였을 수 있으나 추정 — 연결하지 않음
- 질의: 식약처 의료기기 품목허가 API MdlpPrdlstPrmisnInfoService06/getMdlpPrdlstPrmisnList05 entrps=엔파인더스 (6건) / 식약처 API getMdlpPrdlstPrmisnItem05 ENTRPS=엔파인더스 (TYPE_NAME) / emedi 품목 상세 POST https://emedi.mfds.go.kr/search/data/item meddevItemSeq=(봉합사 3건 상세) / https://emedi.mfds.go.kr/search/data/list query2=NFC19032B · NFC19040G · NFC19042E / WebSearch 「N코그 엔파인더스 코실 피부과」「"엔코그" 코 실리프팅 의원」

## 에코2 에볼루션 (`auto-M8-1775364775119`) — 국내 유통 근거 없음(→ 확인 불가)

- 「eCO2 EVOLUTION」 모델은 수출용 19-716 하나뿐(query2=eCO2 EVOLUTION 1건)
- 같은 업체 내수 탄산가스레이저 정상 허가: 제허 12-1396(eCO2 · eCO2 Plus · 2012-11-01) · 제허 24-674(The eCO2 3D · eCO2 3D · 2024-10-07) · 제허 26-360(eCO2 3D · 2026-05-13 · 사이노슈어루트로닉테크놀로지) — 모델명이 다르다(라인 「에코2」 품목)
- 국내 유통: 근거 못 찾음 — data-anyang 「에코2/eCO2/에볼루션」 0건 · 웹 검색은 해외 eCO2 / eCO2 Plus 자료만
- 메모: 원장 「에코2에볼루션」이 실제로 eCO2 Plus 등 내수 모델을 부르는 현장 이름인지는 출처 없음
- 질의: 식약처 의료기기 품목허가 API MdlpPrdlstPrmisnInfoService06/getMdlpPrdlstPrmisnList05 entrps=루트로닉 (187건 · 탄산가스 7건 상세) / https://emedi.mfds.go.kr/search/data/list query2=eCO2 · eCO2 EVOLUTION · EVOLUTION / emedi 품목 상세 POST https://emedi.mfds.go.kr/search/data/item meddevItemSeq=2012006442 · 2019007006 · 2024005294 · 2025000940 · 2025002299 · 2026002907 · 2026004087 / WebSearch 「에코2 에볼루션 eCO2 Evolution 피부과」「"에코2" 레이저 흉터 의원 루트로닉」

## 스텔라듀오 (`new-DEV-039`) — 국내 유통 근거 없음(→ 확인 불가)

- StellarDuo 이름 허가는 수출용 23-602 하나(query2=StellarDuo 1건 · 스텔라듀오 0건)
- 엘림텍 집속형초음파 9건 중 내수는 제허 18-49(ELFU · 모델 FU1) 하나 — 이름·모델 다름
- 국내 유통: 근거 못 찾음 — 경기일보 2020-11-23 기사는 제품 소개만(「스킨케어와 스킨리프팅을 하나의 제품으로 … 스텔라듀오」 · 국내 판매 여부 기재 없음, https://www.kyeonggi.com/article/202011231146531) · data-anyang 「스텔라」 히트는 셀레스텔라(필러)뿐 · 현장 사진 DEV-039 는 있음(원장 7_site_use)
- 메모: 현장(우리 지점) 사진에 기기가 있음 — 그 자체를 「국내 유통」 근거로 볼지는 정할 것
- 질의: 식약처 의료기기 품목허가 API MdlpPrdlstPrmisnInfoService06/getMdlpPrdlstPrmisnList05 entrps=엘림텍 (21건) / https://emedi.mfds.go.kr/search/data/list entpName=엘림텍 (24행) · query2=StellarDuo · Stellar · 스텔라듀오 / emedi 품목 상세 POST https://emedi.mfds.go.kr/search/data/item meddevItemSeq=(초음파 9건 상세) / WebSearch 「스텔라듀오 엘림텍 리프팅 피부과」「"스텔라듀오" 리프팅 의원」

## 정할 것

- 인트라셀: 내수 09-682 는 2026-08-31 만료 — 상태 「만료」 vs 「확인 불가」
- 고우리: 25-634 「G.O.U.R.I.」 연결 여부
- 더블로 골드: 11-946 연결 여부(더블로골드S 와 같은 허가 · 라인)
- 잼버실: 13-1507 연결 여부 · 수출용 JAMBER L/V/N 검색 이름 유지 여부
- N코그: 허가번호 미확인 규칙 적용 여부
- 에코2 에볼루션 · 스텔라듀오: 확인 불가 유지 · 스텔라듀오 현장 사진을 유통 근거로 볼지
