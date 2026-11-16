# 미해결 참조(⑨ unresolved_reference) — 자리별

총 240 행 · 후보는 사전 일치(정규화 완전 일치)·§1.3 계열 밖 모호만 — 추정 없음 · 결정 kind: tuple_assign(_multi) · dictionary_add · conflict_close(needs_source)

## market-pricing.items[].name (122) (72)

| # | 참조 문자열 | 힌트 | 사유 | 미등록 조각 | 닿은 조각(partial) | 후보(≤3 · 근거) | 위치 수 |
|---|---|---|---|---|---|---|---|
| 1 | EMS 바디 (팔뚝/허벅지) | M10 | unregistered | EMS, 바디 | site:팔뚝, site:허벅지 | 바디→problem:바디(정준값 완전 일치), purpose_label:바디(정준값 완전 일치) | 1 |
| 2 | LED 광선치료 (전체얼굴) | M15 | unregistered | 광선치료 | modality_subcategory:광치료(LED), site:얼굴 전체 | 없음 | 1 |
| 3 | MTS (두피 탈모) | M12 | unregistered | 탈모 | modality:마이크로니들링(MTS), site:두피 | 탈모→purpose_label:탈모(정준값 완전 일치) | 1 |
| 4 | MTS (여드름 흉터 집중) | M12 | unregistered | 여드름, 흉터 | modality:마이크로니들링(MTS) | 여드름→problem:여드름(정준값 완전 일치), purpose_label:여드름(정준값 완전 일치), person_condition:여드름(정준값 완전 일치); 흉터→problem:흉터(정준값 완전 일치), purpose_label:흉터(정준값 완전 일치), adverse_event_type:흉터(정준값 완전 일치) | 1 |
| 5 | MTS + PRP (전체얼굴) | M12 | combo_outside_fragment | — | modality:마이크로니들링(MTS), procedure:PRP, site:얼굴 전체 | (조각 둘 이상)→:['site:얼굴 전체'](§1.4 combo_outside_fragment — 닿은 조각(둘 이상)) | 1 |
| 6 | PDO 실 (10줄 기준) | M7 | unregistered | 실 | procedure:PDO, spec:10줄 기준 | 실→adverse_event_type:실(정준값 완전 일치) | 1 |
| 7 | PDRN 주사 (부위당) | M5 | unregistered | PDRN, 주사, 부위당 | — | 없음 | 1 |
| 8 | 감초주사 (간해독) | M16 | unregistered | 감초주사, 간해독 | — | 없음 | 1 |
| 9 | 고농도 비타민C 수액 | M16 | unregistered | 고농도, 비타민C | modality:수액치료 | 없음 | 1 |
| 10 | 눈가 주름 (국산) | M1 | multi_primary | — | site:눈가, procedure:주름, modality_subcategory:국산 | (조각 둘 이상)→:['catalog_item:주름[M1]→catalog_item:주름', 'subcategory:M1-1 국산'](§1.4 multi_primary — 닿은 조각(둘 이상)) | 1 |
| 11 | 눈가 주름 (수입) | M1 | multi_primary | — | site:눈가, procedure:주름, modality_subcategory:수입 | (조각 둘 이상)→:['catalog_item:주름[M1]→catalog_item:주름', 'subcategory:M1-2 수입'](§1.4 multi_primary — 닿은 조각(둘 이상)) | 1 |
| 12 | 눈밑 꺼짐 (HA 1cc) | M2 | unregistered | 꺼짐 | site:눈밑, modality:필러, spec:1cc | 없음 | 1 |
| 13 | 니들RF (모공축소) | M11 | unregistered | 모공축소 | modality:니들RF | 없음 | 1 |
| 14 | 니들RF (여드름 흉터) | M11 | unregistered | 여드름, 흉터 | modality:니들RF | 여드름→problem:여드름(정준값 완전 일치), purpose_label:여드름(정준값 완전 일치), person_condition:여드름(정준값 완전 일치); 흉터→problem:흉터(정준값 완전 일치), purpose_label:흉터(정준값 완전 일치), adverse_event_type:흉터(정준값 완전 일치) | 1 |
| 15 | 다이어트 수액 | M16 | unregistered | 다이어트 | modality:수액치료 | 없음 | 1 |
| 16 | 래디에스 (1.5cc) | M3 | unregistered | 래디에스 | spec:1.5cc | 없음 | 1 |
| 17 | 레이저 제모 (전신) | M8 | unregistered | 전신 | modality:레이저, modality_subcategory:제모 | 없음 | 1 |
| 18 | 마늘주사 (비타민B1) | M16 | unregistered | 비타민B1 | procedure:마늘주사 | 없음 | 1 |
| 19 | 면역 수액 (종합 비타민) | M16 | unregistered | 면역, 종합, 비타민 | modality:수액치료 | 종합→package_tier:vip(동의어 「종합」 완전 일치) | 1 |
| 20 | 모피어스8 (전체얼굴) | M11 | unregistered | 모피어스8 | site:얼굴 전체 | 없음 | 1 |
| 21 | 목주름 (네페르티티) | M1 | unregistered | 네페르티티 | site:목주름 | 없음 | 1 |
| 22 | 몰딩 실 (V라인) | M7 | unregistered | 몰딩, 실, V라인 | — | 실→adverse_event_type:실(정준값 완전 일치) | 1 |
| 23 | 문신 제거 (10cm2) | M8 | unregistered | 문신, 제거 | spec:10cm2 | 없음 | 1 |
| 24 | 미간 주름 (국산) | M1 | multi_primary | — | site:미간, procedure:주름, modality_subcategory:국산 | (조각 둘 이상)→:['catalog_item:주름[M1]→catalog_item:주름', 'subcategory:M1-1 국산'](§1.4 multi_primary — 닿은 조각(둘 이상)) | 1 |
| 25 | 미간 주름 (수입) | M1 | multi_primary | — | site:미간, procedure:주름, modality_subcategory:수입 | (조각 둘 이상)→:['catalog_item:주름[M1]→catalog_item:주름', 'subcategory:M1-2 수입'](§1.4 multi_primary — 닿은 조각(둘 이상)) | 1 |
| 26 | 민트 리프팅 (양쪽) | M7 | unregistered | 리프팅 | product:민트리프트, spec:양쪽 | 리프팅→purpose_label:리프팅(정준값 완전 일치) | 1 |
| 27 | 백옥주사 (글루타치온) | M16 | unregistered | 글루타치온 | procedure:백옥주사 | 없음 | 1 |
| 28 | 볼 볼륨 (HA 1cc) | M2 | unregistered | 볼륨 | site:볼, modality:필러, spec:1cc | 없음 | 1 |
| 29 | 사각턱 (국산) | M1 | multi_primary | — | procedure:사각턱, modality_subcategory:국산 | (조각 둘 이상)→:['catalog_item:사각턱[M1]→catalog_item:사각턱', 'subcategory:M1-1 국산'](§1.4 multi_primary — 닿은 조각(둘 이상)) | 1 |
| 30 | 사각턱 (수입) | M1 | multi_primary | — | procedure:사각턱, modality_subcategory:수입 | (조각 둘 이상)→:['catalog_item:사각턱[M1]→catalog_item:사각턱', 'subcategory:M1-2 수입'](§1.4 multi_primary — 닿은 조각(둘 이상)) | 1 |
| 31 | 슈링크 유니버스 (턱라인) | M9 | unregistered | 턱라인 | procedure:슈링크유니버스 | 없음 | 1 |
| 32 | 스킨부스터 물광주사 (전체얼굴) | M4 | unregistered | 물광주사 | modality:스킨부스터, site:얼굴 전체 | 없음 | 1 |
| 33 | 신데렐라주사 (알파리포산) | M16 | unregistered | 알파리포산 | procedure:신데렐라주사 | 없음 | 1 |
| 34 | 안면 EMS (표정근 강화) | M10 | unregistered | 안면, EMS, 표정근, 강화 | — | 없음 | 1 |
| 35 | 엑셀V (혈관/홍조) | M8 | unregistered | 홍조 | product:엑셀V, modality_subcategory:혈관 | 홍조→adverse_event_type:홍조(정준값 완전 일치) | 1 |
| 36 | 엘란쎄 M (1cc) | M3 | unregistered | M | procedure:엘란쎄, spec:1cc | 없음 | 1 |
| 37 | 엘란쎄 S (1cc) | M3 | unregistered | S | procedure:엘란쎄, spec:1cc | 없음 | 1 |
| 38 | 울쎄라 (턱라인) | M9 | unregistered | 턱라인 | procedure:울쎄라 | 없음 | 1 |
| 39 | 이마 볼륨 (HA 2cc) | M2 | unregistered | 볼륨 | site:이마, modality:필러, spec:2cc | 없음 | 1 |
| 40 | 이마 주름 (국산) | M1 | multi_primary | — | site:이마, procedure:주름, modality_subcategory:국산 | (조각 둘 이상)→:['catalog_item:주름[M1]→catalog_item:주름', 'subcategory:M1-1 국산'](§1.4 multi_primary — 닿은 조각(둘 이상)) | 1 |
| 41 | 이마 주름 (수입) | M1 | multi_primary | — | site:이마, procedure:주름, modality_subcategory:수입 | (조각 둘 이상)→:['catalog_item:주름[M1]→catalog_item:주름', 'subcategory:M1-2 수입'](§1.4 multi_primary — 닿은 조각(둘 이상)) | 1 |
| 42 | 이모드 (4회 패키지) | M10 | unregistered | 이모드 | spec:4회 패키지 | 없음 | 1 |
| 43 | 이모드 (복부) | M10 | unregistered | 이모드 | site:복부 | 없음 | 1 |
| 44 | 이모드 (복부+힙 동시) | M10 | unregistered | 이모드 | site:복부, site:힙 | 없음 | 1 |
| 45 | 이모드 (힙) | M10 | unregistered | 이모드 | site:힙 | 없음 | 1 |
| 46 | 이온토포레시스 (비타민C) | M15 | unregistered | 비타민C | procedure:이온토포레시스 | 없음 | 1 |
| 47 | 입술 볼륨 (HA 1cc) | M2 | unregistered | 볼륨 | site:입술, modality:필러, spec:1cc | 없음 | 1 |
| 48 | 점 제거 (1개당) | M8 | unregistered | 점, 제거 | spec:1개당 | 없음 | 1 |
| 49 | 제네시스 (전체얼굴) | M8 | unregistered | 제네시스 | site:얼굴 전체 | 없음 | 1 |
| 50 | 줄기세포 + MTS (전체얼굴) | M17 | combo_outside_fragment | — | modality:줄기세포치료, modality:마이크로니들링(MTS), site:얼굴 전체 | (조각 둘 이상)→:['site:얼굴 전체'](§1.4 combo_outside_fragment — 닿은 조각(둘 이상)) | 1 |
| 51 | 줄기세포 관절치료 | M17 | unregistered | 관절치료 | modality:줄기세포치료 | 없음 | 1 |
| 52 | 줄기세포 두피치료 (탈모) | M17 | unregistered | 두피치료, 탈모 | modality:줄기세포치료 | 탈모→purpose_label:탈모(정준값 완전 일치) | 1 |
| 53 | 줄기세포 배양액 주입 (전체얼굴) | M17 | unregistered | 주입 | procedure:줄기세포배양액, site:얼굴 전체 | 없음 | 1 |
| 54 | 쥬베룩 울트라 (2cc) | M4 | unregistered | 울트라 | procedure:쥬베룩, spec:2cc | 없음 | 1 |
| 55 | 쥬베룩 파인 (2cc) | M4 | unregistered | 파인 | procedure:쥬베룩, spec:2cc | 없음 | 1 |
| 56 | 진정관리 (시술 후 재생팩) | M15 | unregistered | 진정관리, 시술, 후, 재생팩 | — | 없음 | 1 |
| 57 | 코그 실 리프팅 (양쪽 8줄) | M7 | unregistered | 코그 | modality:실리프팅, spec:양쪽, spec:8줄 | 없음 | 1 |
| 58 | 쿨미니 (소부위 1개) | M14 | unregistered | 소부위 | procedure:쿨미니, spec:1개 | 없음 | 1 |
| 59 | 쿨스컬프팅 (러브핸들 양쪽) | M14 | unregistered | 러브핸들 | procedure:쿨스컬프팅, spec:양쪽 | 없음 | 1 |
| 60 | 쿨스컬프팅 (턱밑 이중턱) | M14 | unregistered | 턱밑, 이중턱 | procedure:쿨스컬프팅 | 없음 | 1 |
| 61 | 쿨스컬프팅 (허벅지 안쪽 양쪽) | M14 | unregistered | 안쪽 | procedure:쿨스컬프팅, site:허벅지, spec:양쪽 | 없음 | 1 |
| 62 | 태반주사 (라이넥) | M16 | unregistered | 태반주사 | product:라이넥 | 없음 | 1 |
| 63 | 턱 끝 볼륨 (HA 1cc) | M2 | unregistered | 끝, 볼륨 | site:턱, modality:필러, spec:1cc | 없음 | 1 |
| 64 | 턱 끝 지방이식 | M6 | unregistered | 끝 | site:턱, modality:지방이식 | 없음 | 1 |
| 65 | 프리미엄 스킨케어 (풀코스) | M15 | unregistered | 프리미엄, 스킨케어, 풀코스 | — | 없음 | 1 |
| 66 | 플라즈마 (눈가 주름) | M13 | multi_primary | — | modality:플라즈마, site:눈가, procedure:주름 | (조각 둘 이상)→:['modality:플라즈마', 'catalog_item:주름[M1]→catalog_item:주름'](§1.4 multi_primary — 닿은 조각(둘 이상)) | 1 |
| 67 | 플라즈마 (눈꺼풀 처짐 비수술) | M13 | unregistered | 처짐, 비수술 | modality:플라즈마, site:눈꺼풀 | 처짐→adverse_event_type:처짐(정준값 완전 일치) | 1 |
| 68 | 플라즈마 (여드름 치료) | M13 | unregistered | 여드름, 치료 | modality:플라즈마 | 여드름→problem:여드름(정준값 완전 일치), purpose_label:여드름(정준값 완전 일치), person_condition:여드름(정준값 완전 일치) | 1 |
| 69 | 플라즈마 (쥐젖/사마귀 1개) | M13 | unregistered | 쥐젖, 사마귀 | modality:플라즈마, spec:1개 | 없음 | 1 |
| 70 | 플라즈마 리프팅 (전체얼굴) | M13 | unregistered | 리프팅 | modality:플라즈마, site:얼굴 전체 | 리프팅→purpose_label:리프팅(정준값 완전 일치) | 1 |
| 71 | 플라즈마 샤워 (진정/재생) | M13 | unregistered | 샤워, 진정, 재생 | modality:플라즈마 | 없음 | 1 |
| 72 | 화학 박피 (살리실산/글리콜산) | M15 | unregistered | 화학, 박피 | ingredient:살리실산, ingredient:글리콜산 | 박피→adverse_event_type:박피(정준값 완전 일치) | 1 |

## post-procedure-timeline.timelines[].name (10) (4)

| # | 참조 문자열 | 힌트 | 사유 | 미등록 조각 | 닿은 조각(partial) | 후보(≤3 · 근거) | 위치 수 |
|---|---|---|---|---|---|---|---|
| 1 | DCA 지방분해 주사 | M16 | unregistered | DCA, 지방분해, 주사 | — | 없음 | 1 |
| 2 | HIFU/RF 리프팅 | M9 | unregistered | 리프팅 | modality_subcategory:HIFU (초음파), modality_subcategory:RF (고주파) | 리프팅→purpose_label:리프팅(정준값 완전 일치) | 1 |
| 3 | 니들RF (미세침 고주파) | M11 | unregistered | 미세침, 고주파 | modality:니들RF | 없음 | 1 |
| 4 | 케미컬 필링 (중간 깊이) | M15 | unregistered | 중간, 깊이 | modality_subcategory:케미컬필링 | 없음 | 1 |

## problem-packages.combos[].combo[] (멤버 29) (10)

| # | 참조 문자열 | 힌트 | 사유 | 미등록 조각 | 닿은 조각(partial) | 후보(≤3 · 근거) | 위치 수 |
|---|---|---|---|---|---|---|---|
| 1 | 리프팅기기 | — | unregistered | 리프팅기기 | — | 없음 | 24 |
| 2 | 모발이식 | — | unregistered | 모발이식 | — | 모발이식→problem_subcategory_label:모발이식(정준값 완전 일치) | 2 |
| 3 | 미라드라이 | — | unregistered | 미라드라 | — | 없음 | 1 |
| 4 | 미백주사 | — | unregistered | 미백주사 | — | 없음 | 2 |
| 5 | 반영구화장 | — | unregistered | 반영구화장 | — | 반영구화장→problem_subcategory_label:반영구화장(정준값 완전 일치) | 4 |
| 6 | 병변내 스테로이드주사 | — | unregistered | 병변내, 스테로이드주사 | — | 없음 | 2 |
| 7 | 약물치료 | — | unregistered | 약물치료 | — | 약물치료→problem_subcategory_label:약물치료(정준값 완전 일치) | 3 |
| 8 | 제모레이저 | — | unregistered | 제모레이저 | — | 없음 | 5 |
| 9 | 지방분해 | — | unregistered | 지방분해 | — | 없음 | 3 |
| 10 | 피코레이저 | — | unregistered | 피코레이저 | — | 피코레이저→product_type:피코레이저(정준값 완전 일치) | 1 |

## problem-packages.procedures[].name (시술 종류 29) (10)

| # | 참조 문자열 | 힌트 | 사유 | 미등록 조각 | 닿은 조각(partial) | 후보(≤3 · 근거) | 위치 수 |
|---|---|---|---|---|---|---|---|
| 1 | 리프팅기기 | M9 | unregistered | 리프팅기기 | — | 없음 | 17 |
| 2 | 모발이식 | M15 | unregistered | 모발이식 | — | 모발이식→problem_subcategory_label:모발이식(정준값 완전 일치) | 2 |
| 3 | 미라드라이 | M9 | unregistered | 미라드라 | — | 없음 | 1 |
| 4 | 미백주사 | M16 | unregistered | 미백주사 | — | 없음 | 2 |
| 5 | 반영구화장 | M15 | unregistered | 반영구화장 | — | 반영구화장→problem_subcategory_label:반영구화장(정준값 완전 일치) | 4 |
| 6 | 병변내 스테로이드주사 | M15 | unregistered | 병변내, 스테로이드주사 | — | 없음 | 2 |
| 7 | 약물치료 | M15 | unregistered | 약물치료 | — | 약물치료→problem_subcategory_label:약물치료(정준값 완전 일치) | 3 |
| 8 | 제모레이저 | M8 | unregistered | 제모레이저 | — | 없음 | 4 |
| 9 | 지방분해 | M14 | unregistered | 지방분해 | — | 없음 | 3 |
| 10 | 피코레이저 | M8 | unregistered | 피코레이저 | — | 피코레이저→product_type:피코레이저(정준값 완전 일치) | 1 |

## problem-packages.procedures[].products[] (제품 34) (4)

| # | 참조 문자열 | 힌트 | 사유 | 미등록 조각 | 닿은 조각(partial) | 후보(≤3 · 근거) | 위치 수 |
|---|---|---|---|---|---|---|---|
| 1 | CO2레이저 | — | unregistered | CO2레이저 | — | 없음 | 2 |
| 2 | PDL(V빔) | — | unregistered | PDL, V빔 | — | 없음 | 2 |
| 3 | 트리암시놀론(±5-FU) | — | unregistered | 트리암시놀론, ±5-FU | — | 없음 | 2 |
| 4 | 헤어맥스(LLLT) | — | unregistered | 헤어맥스, LLLT | — | 없음 | 3 |

## procedure-comparison.json:comparisons[].id (7)

| # | 참조 문자열 | 힌트 | 사유 | 미등록 조각 | 닿은 조각(partial) | 후보(≤3 · 근거) | 위치 수 |
|---|---|---|---|---|---|---|---|
| 1 | body_contouring | — | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 2 | hair_removal | — | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 3 | lifting | — | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 4 | pigment | — | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 5 | rejuvenation | — | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 6 | skin_texture | — | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 7 | volume | — | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |

## procedure-comparison.procedures[].name (39) (33)

| # | 참조 문자열 | 힌트 | 사유 | 미등록 조각 | 닿은 조각(partial) | 후보(≤3 · 근거) | 위치 수 |
|---|---|---|---|---|---|---|---|
| 1 | CO2 프랙셔널 레이저 | M8 | unregistered | 프랙셔널 | modality:레이저, modality:레이저 | 없음 | 1 |
| 2 | IPL (광선치료) | M9 | unregistered | 광선치료 | procedure:IPL | 없음 | 1 |
| 3 | IPL 제모 | M9 | multi_primary | — | procedure:IPL, modality_subcategory:제모 | (조각 둘 이상)→:['catalog_item:IPL[M8]→modality_subcategory:M8-3 IPL', 'subcategory:M8-5 제모'](§1.4 multi_primary — 닿은 조각(둘 이상)) | 1 |
| 4 | Nd:YAG (1064nm) | M8 | unregistered | 1064nm | modality:레이저 | 없음 | 1 |
| 5 | PDT (광역동치료) | M8 | unregistered | PDT, 광역동치료 | — | 없음 | 1 |
| 6 | PRP (자가혈 재생) | M5 | unregistered | 자가혈, 재생 | procedure:PRP | 없음 | 1 |
| 7 | Q-스위치 Nd:YAG | M8 | unregistered | Q-스위치 | modality:레이저 | 없음 | 1 |
| 8 | 다이오드 (808nm/810nm) | M8 | unregistered | 808nm, 810nm | modality_subcategory:제모 | 없음 | 1 |
| 9 | 레이저토닝 (저출력 Nd:YAG) | M8 | unregistered | 저출력 | procedure:레이저토닝, modality:레이저 | 없음 | 1 |
| 10 | 리쥬란 (PN주사) | M4 | unregistered | 리쥬란, PN주사 | — | 없음 | 1 |
| 11 | 리포셀 (HIFU 지방) | M10 | unregistered | 리포셀, 지방 | modality_subcategory:HIFU (초음파) | 지방→adverse_qualifier:지방(정준값 완전 일치) | 1 |
| 12 | 마이크로니들RF (시크릿/인모드) | M11 | unregistered | 마이크로니들RF | product:시크릿, procedure:인모드 | 없음 | 1 |
| 13 | 물광주사 (메소테라피) | M4 | unregistered | 물광주사, 메소테라피 | — | 없음 | 1 |
| 14 | 바넬라 (고주파 바디) | M9 | unregistered | 바넬라, 고주파, 바디 | — | 바디→problem:바디(정준값 완전 일치), purpose_label:바디(정준값 완전 일치) | 1 |
| 15 | 살리실릭 필링 | M15 | unregistered | 살리실릭 | modality:메디컬스킨케어 | 없음 | 1 |
| 16 | 스컬트라 (PLLA) | M3 | multi_primary | — | procedure:스컬트라, procedure:PLLA | (조각 둘 이상)→:['catalog_item:스컬트라[M3]→product:스컬트라', 'catalog_item:PLLA[M7]→ingredient:PLLA'](§1.4 multi_primary — 닿은 조각(둘 이상)) | 1 |
| 17 | 스컬프슈어 (레이저 지방분해) | M8 | unregistered | 스컬프슈어, 지방분해 | modality:레이저 | 없음 | 1 |
| 18 | 스킨부스터 (쥬베룩/리쥬란) | M4 | unregistered | 리쥬란 | modality:스킨부스터, procedure:쥬베룩 | 없음 | 1 |
| 19 | 실리콘피부관리 (아쿠아필/하이드라) | M15 | unregistered | 실리콘피부관리, 하이드라 | procedure:아쿠아필 | 없음 | 1 |
| 20 | 실리프팅 (PDO코그) | M7 | unregistered | PDO코그 | modality:실리프팅 | 없음 | 1 |
| 21 | 써마지FLX (RF) | M9 | multi_primary | — | procedure:써마지FLX, modality_subcategory:RF (고주파) | (조각 둘 이상)→:['catalog_item:써마지FLX[M9]→product:써마지FLX', 'subcategory:M9-2 RF (고주파)'](§1.4 multi_primary — 닿은 조각(둘 이상)) | 1 |
| 22 | 아그네스 (RF 니들 피지선) | M11 | unregistered | 니들, 피지선 | procedure:아그네스, modality_subcategory:RF (고주파) | 없음 | 1 |
| 23 | 알렉산드라이트 (755nm) | M8 | unregistered | 755nm | procedure:알렉산드라이트 | 없음 | 1 |
| 24 | 압출+스킨스케일링 | M15 | unregistered | 압출, 스킨스케일링 | — | 없음 | 1 |
| 25 | 엑소좀 (줄기세포 유래) | M17 | unregistered | 유래 | modality_subcategory:엑소좀, modality:줄기세포치료 | 없음 | 1 |
| 26 | 엘란쎄 (PCL) | M3 | multi_primary | — | procedure:엘란쎄, procedure:PCL | (조각 둘 이상)→:['catalog_item:엘란쎄[M3]→product:엘란쎄', 'catalog_item:PCL[M7]→ingredient:PCL'](§1.4 multi_primary — 닿은 조각(둘 이상)) | 1 |
| 27 | 울쎄라 (HIFU) | M9 | multi_primary | — | procedure:울쎄라, modality_subcategory:HIFU (초음파) | (조각 둘 이상)→:['catalog_item:울쎄라[M9]→product:울쎄라', 'subcategory:M9-1 HIFU (초음파)'](§1.4 multi_primary — 닿은 조각(둘 이상)) | 1 |
| 28 | 인모드FX (RF마이크로니들) | M11 | unregistered | RF마이크로니들 | product:인모드 | 없음 | 1 |
| 29 | 자가지방이식 | M6 | unregistered | 자가지방이식 | — | 없음 | 1 |
| 30 | 제네시스 (Nd:YAG 롱펄스) | M8 | unregistered | 제네시스, 롱펄스 | modality:레이저 | 없음 | 1 |
| 31 | 쿨스컬프팅 (냉동지방분해) | M14 | unregistered | 냉동지방분해 | procedure:쿨스컬프팅 | 없음 | 1 |
| 32 | 프락셀 (프랙셔널 레이저) | M8 | unregistered | 프랙셔널 | product:프락셀, modality:레이저 | 없음 | 1 |
| 33 | 피코 프랙셔널 | M8 | unregistered | 피코, 프랙셔널 | — | 없음 | 1 |

## synergy.links[].from/to (노드 52) (4)

| # | 참조 문자열 | 힌트 | 사유 | 미등록 조각 | 닿은 조각(partial) | 후보(≤3 · 근거) | 위치 수 |
|---|---|---|---|---|---|---|---|
| 1 | HIFES/EMS 바디 | — | unregistered | EMS, 바디 | modality:HIFES/EMS | 바디→problem:바디(정준값 완전 일치), purpose_label:바디(정준값 완전 일치) | 1 |
| 2 | 마이크로니들링(MTS) 두피 | — | unregistered | 마이크로니들링 | site:두피, modality:마이크로니들링(MTS) | 없음 | 1 |
| 3 | 인모드(바디) | M9 | unregistered | 바디 | procedure:인모드 | 바디→problem:바디(정준값 완전 일치), purpose_label:바디(정준값 완전 일치) | 1 |
| 4 | 저출력레이저(LLLT) 두피 | — | unregistered | 저출력레이저, LLLT | site:두피 | 없음 | 1 |

## taxonomy.json:modality[].subcategories[].items[].canonical_category (6)

| # | 참조 문자열 | 힌트 | 사유 | 미등록 조각 | 닿은 조각(partial) | 후보(≤3 · 근거) | 위치 수 |
|---|---|---|---|---|---|---|---|
| 1 | 비가교 HA 메조테라피 | M4 | canonical_category 가 하위분류 사전에 없다(질문 23) | 비가교 HA 메조테라피 | — | 없음 | 1 |
| 2 | 비타민 B 계열 | M16 | canonical_category 가 하위분류 사전에 없다(질문 23) | 비타민 B 계열 | — | 없음 | 1 |
| 3 | 재생형 메조테라피 | M4 | canonical_category 가 하위분류 사전에 없다(질문 23) | 재생형 메조테라피 | — | 없음 | 1 |
| 4 | 콜라겐 혼합 메조테라피 | M4 | canonical_category 가 하위분류 사전에 없다(질문 23) | 콜라겐 혼합 메조테라피 | — | 없음 | 1 |
| 5 | 항산화 IV | M16 | canonical_category 가 하위분류 사전에 없다(질문 23) | 항산화 IV | — | 없음 | 1 |
| 6 | 항산화·미백 IV | M16 | canonical_category 가 하위분류 사전에 없다(질문 23) | 항산화·미백 IV | — | 없음 | 1 |

## treatment-optimization.annual_plans.schedule[].procedures[] (29) (5)

| # | 참조 문자열 | 힌트 | 사유 | 미등록 조각 | 닿은 조각(partial) | 후보(≤3 · 근거) | 위치 수 |
|---|---|---|---|---|---|---|---|
| 1 | IPL(가을 색소 관리) | — | unregistered | 색소 | procedure:IPL | 색소→purpose_label:색소(정준값 완전 일치) | 1 |
| 2 | IPL(가을 색소) | — | unregistered | 색소 | procedure:IPL | 색소→purpose_label:색소(정준값 완전 일치) | 1 |
| 3 | IPL(색소 관리) | — | unregistered | 색소 | procedure:IPL | 색소→purpose_label:색소(정준값 완전 일치) | 1 |
| 4 | 연말 리프팅 관리(RF/HIFU 터치) | — | unregistered | 리프팅 | modality_subcategory:RF (고주파), modality_subcategory:HIFU (초음파) | 리프팅→purpose_label:리프팅(정준값 완전 일치) | 1 |
| 5 | 프락셔널(피부결) | — | unregistered | 피부결 | modality_subcategory:프락셔널 | 피부결→purpose_label:피부결(정준값 완전 일치) | 1 |

## treatment-optimization.by_age_group recommended_base/avoid/upgrade (22) (10)

| # | 참조 문자열 | 힌트 | 사유 | 미등록 조각 | 닿은 조각(partial) | 후보(≤3 · 근거) | 위치 수 |
|---|---|---|---|---|---|---|---|
| 1 | HIFU(울쎄라급) | — | unregistered | 울쎄라급 | modality_subcategory:HIFU (초음파) | 없음 | 1 |
| 2 | 과도한 시술 빈도(피부 회복력 저하 고려) | — | unregistered | 시술, 회복력, 저하, 고려 | layer_site:피부 | 없음 | 1 |
| 3 | 과도한 필러 (자연스러운 노화 중요) | — | unregistered | 자연스러운, 노화, 중요 | modality:필러 | 없음 | 1 |
| 4 | 과도한 필러(부자연스러운 외관) | — | unregistered | 부자연스러운, 외관 | modality:필러 | 없음 | 1 |
| 5 | 과도한 필러량(자연스러움 유지) | — | unregistered | 필러량, 자연스러움 | — | 없음 | 1 |
| 6 | 목전용 HIFU/RF | — | unregistered | 목전용 | modality_subcategory:HIFU (초음파), modality_subcategory:RF (고주파) | 없음 | 1 |
| 7 | 바이오스티뮬레이터 (콜라겐 예방적 투자) | — | unregistered | 예방적, 투자 | modality:바이오스티뮬레이터, modality_subcategory:콜라겐 | 없음 | 1 |
| 8 | 불필요한 보톡스(예방 목적 과잉 금지) | — | unregistered | 불필요한, 예방, 목적, 과잉, 금지 | modality:보툴리눔 톡신 | 없음 | 1 |
| 9 | 프락셔널 CO2(피부결) | — | unregistered | 피부결 | modality_subcategory:프락셔널, modality:레이저 | 피부결→purpose_label:피부결(정준값 완전 일치) | 1 |
| 10 | 회복력 초과 시술 빈도 | — | unregistered | 회복력, 초과, 시술 | — | 없음 | 1 |

## treatment-optimization.json:by_age_group[].primary_concerns[] (16)

| # | 참조 문자열 | 힌트 | 사유 | 미등록 조각 | 닿은 조각(partial) | 후보(≤3 · 근거) | 위치 수 |
|---|---|---|---|---|---|---|---|
| 1 | 깊은 주름 | 50대+ | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 2 | 눈가 노화 | 30대 | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 3 | 목주름 | 50대+ | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 4 | 볼륨 손실 | 40대 | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 5 | 볼륨 손실 | 50대+ | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 6 | 색소 심화 | 40대 | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 7 | 색소(기미 초기) | 20대 | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 8 | 색소/기미 | 30대 | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 9 | 여드름/흉터 | 20대 | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 10 | 주름 심화 | 40대 | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 11 | 처짐 | 40대 | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 12 | 처짐 | 50대+ | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 13 | 초기 주름 | 30대 | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 14 | 탄력 저하 | 30대 | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 15 | 피부 노화 | 50대+ | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 16 | 피부결 | 20대 | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |

## treatment-optimization.json:by_concern[].concern (6)

| # | 참조 문자열 | 힌트 | 사유 | 미등록 조각 | 닿은 조각(partial) | 후보(≤3 · 근거) | 위치 수 |
|---|---|---|---|---|---|---|---|
| 1 | 바디컨투어링 | — | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 2 | 볼륨 손실 | — | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 3 | 색소/기미 | — | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 4 | 여드름/흉터 | — | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 5 | 주름 개선 | — | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |
| 6 | 피부결/모공 | — | 고민 사전 일치 없음(질문 12) | — | — | 없음 | 1 |

## treatment-optimization.optimal_combo[] (57) (28)

| # | 참조 문자열 | 힌트 | 사유 | 미등록 조각 | 닿은 조각(partial) | 후보(≤3 · 근거) | 위치 수 |
|---|---|---|---|---|---|---|---|
| 1 | CaHA(레디에스) | — | unregistered | 레디에스 | ingredient:CaHA | 없음 | 1 |
| 2 | HA 볼류마이징 스킨부스터 | — | unregistered | 볼류마이징 | ingredient:HA, modality:스킨부스터 | 없음 | 1 |
| 3 | HA 필러(딥) | — | unregistered | 딥 | ingredient:HA, modality:필러 | 없음 | 1 |
| 4 | LED(블루라이트) | — | unregistered | 블루라이트 | modality_subcategory:광치료(LED) | 없음 | 1 |
| 5 | PRP (엑소좀은 보조·근거 제한적) | — | unregistered | 보조·근거, 제한적 | procedure:PRP, modality_subcategory:엑소좀 | 없음 | 1 |
| 6 | RF 타이트닝 | — | unregistered | 타이트닝 | modality_subcategory:RF (고주파) | 없음 | 1 |
| 7 | TCA Cross | — | unregistered | Cross | ingredient:TCA | 없음 | 1 |
| 8 | 고주파 바디 RF | — | unregistered | 고주파, 바디 | modality_subcategory:RF (고주파) | 바디→problem:바디(정준값 완전 일치), purpose_label:바디(정준값 완전 일치) | 1 |
| 9 | 다이오드 레이저(810nm) | — | unregistered | 810nm | product:다이오드 레이저 | 없음 | 1 |
| 10 | 다이오드(810nm) | — | unregistered | 810nm | modality_subcategory:제모 | 없음 | 1 |
| 11 | 듀얼파장(알렉+다이오드 or 다이오드+Nd:YAG) | — | unregistered | 듀얼파장, or | product:알렉산드라이트, modality_subcategory:제모, modality_subcategory:제모, modality:레이저 | 없음 | 1 |
| 12 | 마이크로니들링+미백약물 | — | unregistered | 마이크로니들링, 미백약물 | — | 없음 | 1 |
| 13 | 바디 HIFU(리포셀) | — | unregistered | 바디, 리포셀 | modality_subcategory:HIFU (초음파) | 바디→problem:바디(정준값 완전 일치), purpose_label:바디(정준값 완전 일치) | 1 |
| 14 | 바디 RF | — | unregistered | 바디 | modality_subcategory:RF (고주파) | 바디→problem:바디(정준값 완전 일치), purpose_label:바디(정준값 완전 일치) | 1 |
| 15 | 비타민C 이온토포레시스 | — | unregistered | 비타민C | procedure:이온토포레시스 | 없음 | 1 |
| 16 | 스킨부스터(리쥬란) | — | unregistered | 리쥬란 | modality:스킨부스터 | 없음 | 1 |
| 17 | 스킨부스터(미백성분) | — | unregistered | 미백성분 | modality:스킨부스터 | 없음 | 1 |
| 18 | 써마지/RF | — | unregistered | 써마지 | modality_subcategory:RF (고주파) | 없음 | 1 |
| 19 | 알렉산드라이트(755nm) | — | unregistered | 755nm | procedure:알렉산드라이트 | 없음 | 1 |
| 20 | 울쎄라 HIFU | — | multi_primary | — | procedure:울쎄라, modality_subcategory:HIFU (초음파) | (조각 둘 이상)→:['catalog_item:울쎄라[M9]→product:울쎄라', 'subcategory:M9-1 HIFU (초음파)'](§1.4 multi_primary — 닿은 조각(둘 이상)) | 1 |
| 21 | 저출력 IPL(병용 보조) | — | unregistered | 저출력 | procedure:IPL | 없음 | 1 |
| 22 | 저출력 피코토닝 | — | unregistered | 저출력 | procedure:피코토닝 | 없음 | 1 |
| 23 | 지방분해주사(데옥시콜산) | — | unregistered | 지방분해주사, 데옥시콜산 | — | 없음 | 1 |
| 24 | 지방흡입(리포) | — | unregistered | 지방흡입, 리포 | — | 없음 | 1 |
| 25 | 크라이오(냉동지방분해) | — | unregistered | 냉동지방분해 | modality:크라이오리포라이시스 | 없음 | 1 |
| 26 | 트라넥삼산(경구+주사) | — | unregistered | 경구, 주사 | procedure:트라넥삼산 | 없음 | 1 |
| 27 | 트라넥삼산(경구/국소) | — | unregistered | 경구, 국소 | procedure:트라넥삼산 | 없음 | 1 |
| 28 | 필링(약한 산) | — | unregistered | 약한, 산 | modality:메디컬스킨케어 | 없음 | 1 |

## treatment-sequence.common_combos[].sequence[] (22 distinct) (10)

| # | 참조 문자열 | 힌트 | 사유 | 미등록 조각 | 닿은 조각(partial) | 후보(≤3 · 근거) | 위치 수 |
|---|---|---|---|---|---|---|---|
| 1 | ALA 도포·배양 | — | unregistered | ALA, 도포·배양 | — | 없음 | 1 |
| 2 | HIFU 울쎄라 | — | multi_primary | — | modality_subcategory:HIFU (초음파), procedure:울쎄라 | (조각 둘 이상)→:['subcategory:M9-1 HIFU (초음파)', 'catalog_item:울쎄라[M9]→product:울쎄라'](§1.4 multi_primary — 닿은 조각(둘 이상)) | 1 |
| 3 | MTS(미세채널 오픈) | — | unregistered | 미세채널, 오픈 | modality:마이크로니들링(MTS) | 없음 | 1 |
| 4 | PRP 도포 | — | unregistered | 도포 | procedure:PRP | 없음 | 1 |
| 5 | 광조사(PDT) | — | unregistered | 광조사, PDT | — | 없음 | 1 |
| 6 | 비타민C 이온토포레시스 | — | unregistered | 비타민C | procedure:이온토포레시스 | 없음 | 1 |
| 7 | 슈링크 HIFU | — | multi_primary | — | procedure:슈링크, modality_subcategory:HIFU (초음파) | (조각 둘 이상)→:['catalog_item:슈링크[M9]→product:슈링크', 'subcategory:M9-1 HIFU (초음파)'](§1.4 multi_primary — 닿은 조각(둘 이상)) | 1 |
| 8 | 스킨부스터 리쥬란 | — | unregistered | 리쥬란 | modality:스킨부스터 | 없음 | 1 |
| 9 | 울쎄라 HIFU | — | multi_primary | — | procedure:울쎄라, modality_subcategory:HIFU (초음파) | (조각 둘 이상)→:['catalog_item:울쎄라[M9]→product:울쎄라', 'subcategory:M9-1 HIFU (초음파)'](§1.4 multi_primary — 닿은 조각(둘 이상)) | 1 |
| 10 | 진정팩 | — | unregistered | 진정팩 | — | 없음 | 1 |

## treatment-sequence.incompatible_same_day[].pair[] (14 distinct) (7)

| # | 참조 문자열 | 힌트 | 사유 | 미등록 조각 | 닿은 조각(partial) | 후보(≤3 · 근거) | 위치 수 |
|---|---|---|---|---|---|---|---|
| 1 | HA 필러 주입 후 RF/HIFU | — | unregistered | 주입, 후 | ingredient:HA, modality:필러, modality_subcategory:RF (고주파), modality_subcategory:HIFU (초음파) | 없음 | 1 |
| 2 | PDO실 | — | unregistered | PDO실 | — | 없음 | 1 |
| 3 | 모든 시술 | — | unregistered | 모든, 시술 | — | 없음 | 1 |
| 4 | 비가교HA | — | unregistered | 비가교HA | — | 없음 | 1 |
| 5 | 심부 필링(TCA 50%+/페놀) | — | unregistered | 심부, 50% | modality:메디컬스킨케어, ingredient:TCA, ingredient:페놀 | 없음 | 1 |
| 6 | 심부 필링(페놀) | — | unregistered | 심부 | modality:메디컬스킨케어, ingredient:페놀 | 없음 | 1 |
| 7 | 이소트레티노인 복용 중 | — | unregistered | 복용, 중 | procedure:이소트레티노인 | 없음 | 3 |

## treatment-sequence.minimum_intervals from/to (14 distinct) (5)

| # | 참조 문자열 | 힌트 | 사유 | 미등록 조각 | 닿은 조각(partial) | 후보(≤3 · 근거) | 위치 수 |
|---|---|---|---|---|---|---|---|
| 1 | 박리성(ablative) 레이저/심부 필링 | — | unregistered | 박리성, 심부 | modality:레이저, modality:메디컬스킨케어, technique:ablative | 없음 | 1 |
| 2 | 심부 필링 | — | unregistered | 심부 | modality:메디컬스킨케어 | 없음 | 1 |
| 3 | 프락셔널/얕은 필링 | — | unregistered | 얕은 | modality_subcategory:프락셔널, modality:메디컬스킨케어 | 없음 | 1 |
| 4 | 필러 (동일 부위 재시술) | — | unregistered | 동일, 부위, 재시술 | modality:필러 | 없음 | 1 |
| 5 | 필러 (별도 세션) | — | unregistered | 별도, 세션 | modality:필러 | 없음 | 1 |

## treatment-sequence.sequence_order[].categories[] (19) (3)

| # | 참조 문자열 | 힌트 | 사유 | 미등록 조각 | 닿은 조각(partial) | 후보(≤3 · 근거) | 위치 수 |
|---|---|---|---|---|---|---|---|
| 1 | 국소마취 | — | unregistered | 국소마취 | — | 없음 | 1 |
| 2 | 연고마취 | — | unregistered | 연고마취 | — | 없음 | 1 |
| 3 | 클렌징 | M15 | unregistered | 클렌징 | — | 없음 | 1 |
