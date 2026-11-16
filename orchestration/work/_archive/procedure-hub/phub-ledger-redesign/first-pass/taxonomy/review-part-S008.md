# S008 — M3 바이오스티뮬레이터/콜라겐부스터

- 읽기 상태: **read** · 마지막 읽은 Pointer `/modality/2/subcategories/3/items/2/extracted/aftercare/2`
- 단위: id, category, category_en, group, subcategories 컨테이너, M3-1 items/0, M3-1 items/1, M3-1 items/2, M3-1 items/3, M3-2 items/0, M3-2 items/1, M3-2 items/2, M3-5 items/0, M3-5 items/1, M3-5 items/2, M3-5 items/3, M3-3 items/0, M3-3 items/1, M3-3 items/2
- 상위 문맥(공동 참조·소유 아님): 없음
- 기계 기록: `source-map.json`(section=S008) · `morphology/S008.json` · `expressions.json`(section=S008) · 읽기 렌더 `reading/S008.txt`

## 원문 값 (원본 컬럼명 그대로, 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/modality/2` | modality[2] | object | {object, 키 8: id, category, category_en, group, subcategories, extracted, products, name} |
| `/modality/2/id` | id | string | M3 |
| `/modality/2/category` | category | string | 바이오스티뮬레이터/콜라겐부스터 |
| `/modality/2/category_en` | category_en | string | Biostimulator / Collagen Stimulator |
| `/modality/2/group` | group | string | 주사/주입 |
| `/modality/2/subcategories` | subcategories | array | [array, 원소 7] |
| `/modality/2/subcategories/0` | subcategories[0] | object | {object, 키 3: id, label, items} |
| `/modality/2/subcategories/0/id` | id | string | M3-1 |
| `/modality/2/subcategories/0/label` | label | string | PLLA (폴리-L-락틱산) |
| `/modality/2/subcategories/0/items` | items | array | [array, 원소 4] |
| `/modality/2/subcategories/0/items/0` | items[0] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/2/subcategories/0/items/0/id` | id | string | M3-1-1 |
| `/modality/2/subcategories/0/items/0/name` | name | string | 스컬트라 |
| `/modality/2/subcategories/0/items/0/detail` | detail | string | 갈더마 · 대표 PLLA |
| `/modality/2/subcategories/0/items/0/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/2/subcategories/0/items/0/extracted/overview` | overview | string | PLLA 기반 콜라겐 부스터 |
| `/modality/2/subcategories/0/items/0/extracted/mechanism` | mechanism | string | poly-L-lactic acid(PLLA) 미세입자가 진피 내 이물반응을 유도하여 자체 콜라겐 생성을 촉진. 점진적 흡수되며 신생 콜라겐이 그 자리를 대체하여 장기 볼륨 회복. |
| `/modality/2/subcategories/0/items/0/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/2/subcategories/0/items/0/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/2/subcategories/0/items/0/extracted/indications/primary/0` | primary[0] | string | 팔자주름 |
| `/modality/2/subcategories/0/items/0/extracted/indications/primary/1` | primary[1] | string | 얼굴 전체 위축 |
| `/modality/2/subcategories/0/items/0/extracted/indications/primary/2` | primary[2] | string | 볼 함몰 |
| `/modality/2/subcategories/0/items/0/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/2/subcategories/0/items/0/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/2/subcategories/0/items/0/extracted/safety/common/0` | common[0] | string | 일시적 부종 |
| `/modality/2/subcategories/0/items/0/extracted/safety/common/1` | common[1] | string | 압통 |
| `/modality/2/subcategories/0/items/0/extracted/safety/common/2` | common[2] | string | 미세 결절 형성 |
| `/modality/2/subcategories/0/items/0/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/2/subcategories/0/items/0/extracted/safety/serious/0` | serious[0] | string | 지연성 육아종 반응 |
| `/modality/2/subcategories/0/items/0/extracted/safety/serious/1` | serious[1] | string | 이물반응 |
| `/modality/2/subcategories/0/items/0/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/2/subcategories/0/items/0/extracted/onset_duration/onset` | onset | string | 4-6주(점진적) |
| `/modality/2/subcategories/0/items/0/extracted/onset_duration/duration` | duration | string | 24-36개월 |
| `/modality/2/subcategories/0/items/0/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/2/subcategories/0/items/0/extracted/aftercare/0` | aftercare[0] | string | 5-5-5 마사지는 선택 (결절 예방효과 RCT 미입증; 결절 예방의 핵심은 희석·수화·주입 깊이) |
| `/modality/2/subcategories/0/items/0/extracted/aftercare/1` | aftercare[1] | string | 시술 후 부종은 수일 내 소실 |
| `/modality/2/subcategories/0/items/0/extracted/aftercare/2` | aftercare[2] | string | [시술 주기 참고] 반복 시술 권장. 1개월 간격, 3회 이상 코스. 콜라겐 생성 완료까지 2-6개월 소요. 소재별 지속: PLLA 24개월+, CaHA 12-24개월, PCL 36개월+ (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/2/subcategories/0/items/1` | items[1] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/2/subcategories/0/items/1/id` | id | string | auto-10-1774737181584 |
| `/modality/2/subcategories/0/items/1/name` | name | string | 올리디아 |
| `/modality/2/subcategories/0/items/1/detail` | detail | string | PRP사이언스 |
| `/modality/2/subcategories/0/items/1/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/2/subcategories/0/items/1/extracted/overview` | overview | string | PRP사이언스 PLLA 기반 바이오스티뮬레이터 |
| `/modality/2/subcategories/0/items/1/extracted/mechanism` | mechanism | string | PLLA 미세입자가 진피 내 이물반응을 유도하여 콜라겐 신생을 촉진한다. 주입 후 점진적으로 PLLA가 분해되면서 자가 콜라겐으로 대체된다. |
| `/modality/2/subcategories/0/items/1/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/2/subcategories/0/items/1/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/2/subcategories/0/items/1/extracted/indications/primary/0` | primary[0] | string | 피부 탄력 저하 |
| `/modality/2/subcategories/0/items/1/extracted/indications/primary/1` | primary[1] | string | 미세주름 |
| `/modality/2/subcategories/0/items/1/extracted/indications/primary/2` | primary[2] | string | 피부 톤 개선 |
| `/modality/2/subcategories/0/items/1/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/2/subcategories/0/items/1/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/2/subcategories/0/items/1/extracted/safety/common/0` | common[0] | string | 주사 부위 부종 |
| `/modality/2/subcategories/0/items/1/extracted/safety/common/1` | common[1] | string | 일시적 홍반 |
| `/modality/2/subcategories/0/items/1/extracted/safety/common/2` | common[2] | string | 가려움증 |
| `/modality/2/subcategories/0/items/1/extracted/safety/serious` | serious | array | [array, 원소 1] |
| `/modality/2/subcategories/0/items/1/extracted/safety/serious/0` | serious[0] | string | 감염(혈액유래 시술) |
| `/modality/2/subcategories/0/items/1/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/2/subcategories/0/items/1/extracted/onset_duration/onset` | onset | string | 2-4주 |
| `/modality/2/subcategories/0/items/1/extracted/onset_duration/duration` | duration | string | 6-12개월 |
| `/modality/2/subcategories/0/items/1/extracted/aftercare` | aftercare | array | [array, 원소 5] |
| `/modality/2/subcategories/0/items/1/extracted/aftercare/0` | aftercare[0] | string | 자극적 제품 사용 자제(3일) |
| `/modality/2/subcategories/0/items/1/extracted/aftercare/1` | aftercare[1] | string | 시술 후 가벼운 마사지로 균일한 분포 유도 (의사 지시에 따라) |
| `/modality/2/subcategories/0/items/1/extracted/aftercare/2` | aftercare[2] | string | 결절 발생 시 내원 상담 |
| `/modality/2/subcategories/0/items/1/extracted/aftercare/3` | aftercare[3] | string | 멍/부종은 수일 내 자연 소실 |
| `/modality/2/subcategories/0/items/1/extracted/aftercare/4` | aftercare[4] | string | [시술 주기 참고] 반복 시술 권장. 1개월 간격, 3회 이상 코스. 콜라겐 생성 완료까지 2-6개월 소요. 소재별 지속: PLLA 24개월+, CaHA 12-24개월, PCL 36개월+ (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/2/subcategories/0/items/2` | items[2] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/2/subcategories/0/items/2/id` | id | string | auto-11-1774737181584 |
| `/modality/2/subcategories/0/items/2/name` | name | string | 에스테필 |
| `/modality/2/subcategories/0/items/2/detail` | detail | string | 레지메드/휴메딕스 유통 · PDLLA 콜라겐 부스터 |
| `/modality/2/subcategories/0/items/2/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/2/subcategories/0/items/2/extracted/overview` | overview | string | PDLLA(폴리디엘락틱애시드) 미립자 기반의 생분해성 콜라겐 부스터 — HA 필러가 아니며 즉시 볼륨 효과는 제한적이고 수주에 걸친 신생 콜라겐 형성으로 서서히 볼륨이 나타남 |
| `/modality/2/subcategories/0/items/2/extracted/mechanism` | mechanism | string | PDLLA 미세입자가 진피 내 이물반응(foreign body reaction)을 통해 I형/III형 콜라겐 합성을 자극한다. 입자가 점진적으로 생분해되면서 신생 콜라겐으로 대체된다. |
| `/modality/2/subcategories/0/items/2/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/2/subcategories/0/items/2/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/2/subcategories/0/items/2/extracted/indications/primary/0` | primary[0] | string | 얕은 주름 |
| `/modality/2/subcategories/0/items/2/extracted/indications/primary/1` | primary[1] | string | 입술 확대 |
| `/modality/2/subcategories/0/items/2/extracted/indications/primary/2` | primary[2] | string | 광대뼈 보강 |
| `/modality/2/subcategories/0/items/2/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/2/subcategories/0/items/2/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/2/subcategories/0/items/2/extracted/safety/common/0` | common[0] | string | 부종 |
| `/modality/2/subcategories/0/items/2/extracted/safety/common/1` | common[1] | string | 멍 |
| `/modality/2/subcategories/0/items/2/extracted/safety/common/2` | common[2] | string | 압통 |
| `/modality/2/subcategories/0/items/2/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/2/subcategories/0/items/2/extracted/safety/serious/0` | serious[0] | string | 혈관 폐색 |
| `/modality/2/subcategories/0/items/2/extracted/safety/serious/1` | serious[1] | string | 과민반응 |
| `/modality/2/subcategories/0/items/2/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/2/subcategories/0/items/2/extracted/onset_duration/onset` | onset | string | 즉시-2일 |
| `/modality/2/subcategories/0/items/2/extracted/onset_duration/duration` | duration | string | 12-18개월 |
| `/modality/2/subcategories/0/items/2/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/2/subcategories/0/items/2/extracted/aftercare/0` | aftercare[0] | string | 48시간 냉찜질 |
| `/modality/2/subcategories/0/items/2/extracted/aftercare/1` | aftercare[1] | string | 과도한 안면 운동 피하기 |
| `/modality/2/subcategories/0/items/2/extracted/aftercare/2` | aftercare[2] | string | [시술 주기 참고] 반복 시술 권장. 1개월 간격, 3회 이상 코스. 콜라겐 생성 완료까지 2-6개월 소요. 소재별 지속: PLLA 24개월+, CaHA 12-24개월, PCL 36개월+ (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/2/subcategories/0/items/3` | items[3] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/2/subcategories/0/items/3/id` | id | string | auto-M3-1775364775145 |
| `/modality/2/subcategories/0/items/3/name` | name | string | PLLA-SCA |
| `/modality/2/subcategories/0/items/3/detail` | detail | string | 수용성콜라겐 |
| `/modality/2/subcategories/0/items/3/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/2/subcategories/0/items/3/extracted/overview` | overview | string | 수용성 콜라겐과 폴리락틱산의 콜라겐 부스터 |
| `/modality/2/subcategories/0/items/3/extracted/mechanism` | mechanism | string | 폴리락틱산이 서서히 분해되면서 섬유아세포를 자극합니다. 자체 콜라겐 생성을 촉진하여 점진적인 볼륨 개선 효과를 나타냅니다. |
| `/modality/2/subcategories/0/items/3/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/2/subcategories/0/items/3/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/2/subcategories/0/items/3/extracted/indications/primary/0` | primary[0] | string | 콜라겐 재생 |
| `/modality/2/subcategories/0/items/3/extracted/indications/primary/1` | primary[1] | string | 자연스러운 볼륨 증대 |
| `/modality/2/subcategories/0/items/3/extracted/indications/primary/2` | primary[2] | string | 피부 탄력 개선 |
| `/modality/2/subcategories/0/items/3/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/2/subcategories/0/items/3/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/2/subcategories/0/items/3/extracted/safety/common/0` | common[0] | string | 일시적 부종 |
| `/modality/2/subcategories/0/items/3/extracted/safety/common/1` | common[1] | string | 주사 부위 발적 |
| `/modality/2/subcategories/0/items/3/extracted/safety/common/2` | common[2] | string | 결절 형성 가능성 |
| `/modality/2/subcategories/0/items/3/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/2/subcategories/0/items/3/extracted/onset_duration/onset` | onset | string | 4-6주 |
| `/modality/2/subcategories/0/items/3/extracted/onset_duration/duration` | duration | string | 12-18개월 |
| `/modality/2/subcategories/0/items/3/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/2/subcategories/0/items/3/extracted/aftercare/0` | aftercare[0] | string | 충분한 수분 섭취 |
| `/modality/2/subcategories/0/items/3/extracted/aftercare/1` | aftercare[1] | string | 마사지 권장 |
| `/modality/2/subcategories/0/items/3/extracted/aftercare/2` | aftercare[2] | string | [시술 주기 참고] 반복 시술 권장. 1개월 간격, 3회 이상 코스. 콜라겐 생성 완료까지 2-6개월 소요. 소재별 지속: PLLA 24개월+, CaHA 12-24개월, PCL 36개월+ (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/2/subcategories/1` | subcategories[1] | object | {object, 키 3: id, label, items} |
| `/modality/2/subcategories/1/id` | id | string | M3-2 |
| `/modality/2/subcategories/1/label` | label | string | CaHA (칼슘하이드록시아파타이트) |
| `/modality/2/subcategories/1/items` | items | array | [array, 원소 3] |
| `/modality/2/subcategories/1/items/0` | items[0] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/2/subcategories/1/items/0/id` | id | string | M3-2-1 |
| `/modality/2/subcategories/1/items/0/name` | name | string | 래디어스 |
| `/modality/2/subcategories/1/items/0/detail` | detail | string | 멀츠 |
| `/modality/2/subcategories/1/items/0/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/2/subcategories/1/items/0/extracted/overview` | overview | string | CaHA 기반 장기 콜라겐 부스터 |
| `/modality/2/subcategories/1/items/0/extracted/mechanism` | mechanism | string | 칼슘하이드록시아파타이트(CaHA) 미세구와 카복시메틸셀룰로오스(CMC) 겔 복합체. 즉각적 볼륨 제공 후 CMC 흡수되면서 CaHA 입자가 이물반응을 통해 콜라겐 생성 지속. |
| `/modality/2/subcategories/1/items/0/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/2/subcategories/1/items/0/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/2/subcategories/1/items/0/extracted/indications/primary/0` | primary[0] | string | 심한 팔자주름 |
| `/modality/2/subcategories/1/items/0/extracted/indications/primary/1` | primary[1] | string | 턱 선 강화 |
| `/modality/2/subcategories/1/items/0/extracted/indications/primary/2` | primary[2] | string | 얼굴 윤곽 교정 |
| `/modality/2/subcategories/1/items/0/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/2/subcategories/1/items/0/extracted/safety/common` | common | array | [array, 원소 2] |
| `/modality/2/subcategories/1/items/0/extracted/safety/common/0` | common[0] | string | 경미한 부종 |
| `/modality/2/subcategories/1/items/0/extracted/safety/common/1` | common[1] | string | 일시적 압통 |
| `/modality/2/subcategories/1/items/0/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/2/subcategories/1/items/0/extracted/safety/serious/0` | serious[0] | string | 육아종 |
| `/modality/2/subcategories/1/items/0/extracted/safety/serious/1` | serious[1] | string | 이물반응 |
| `/modality/2/subcategories/1/items/0/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/2/subcategories/1/items/0/extracted/onset_duration/onset` | onset | string | 즉시-1주 |
| `/modality/2/subcategories/1/items/0/extracted/onset_duration/duration` | duration | string | 12-24개월 |
| `/modality/2/subcategories/1/items/0/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/2/subcategories/1/items/0/extracted/aftercare/0` | aftercare[0] | string | 시술 후 가벼운 마사지로 균일한 분포 유도 (의사 지시에 따라) |
| `/modality/2/subcategories/1/items/0/extracted/aftercare/1` | aftercare[1] | string | 결절 발생 시 내원 상담 |
| `/modality/2/subcategories/1/items/0/extracted/aftercare/2` | aftercare[2] | string | 멍/부종은 수일 내 자연 소실 |
| `/modality/2/subcategories/1/items/0/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 반복 시술 권장. 1개월 간격, 3회 이상 코스. 콜라겐 생성 완료까지 2-6개월 소요. 소재별 지속: PLLA 24개월+, CaHA 12-24개월, PCL 36개월+ (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/2/subcategories/1/items/1` | items[1] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/2/subcategories/1/items/1/id` | id | string | auto-12-1774737181584 |
| `/modality/2/subcategories/1/items/1/name` | name | string | 디클래씨 |
| `/modality/2/subcategories/1/items/1/detail` | detail | string | 대웅제약 |
| `/modality/2/subcategories/1/items/1/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/2/subcategories/1/items/1/extracted/overview` | overview | string | PDLLA/HA 복합 바이오스티뮬레이터 |
| `/modality/2/subcategories/1/items/1/extracted/mechanism` | mechanism | string | 칼슘하이드록시아파타이트(CaHA) 미세구와 카복시메틸셀룰로오스(CMC) 겔 캐리어로 구성. CaHA 미세구가 즉각적 구조 지지를 제공하고, 이물반응을 통해 콜라겐 합성을 자극한다. |
| `/modality/2/subcategories/1/items/1/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/2/subcategories/1/items/1/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/2/subcategories/1/items/1/extracted/indications/primary/0` | primary[0] | string | 피부 위축 |
| `/modality/2/subcategories/1/items/1/extracted/indications/primary/1` | primary[1] | string | 볼 함몰 |
| `/modality/2/subcategories/1/items/1/extracted/indications/primary/2` | primary[2] | string | 전체 얼굴 리프팅 |
| `/modality/2/subcategories/1/items/1/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/2/subcategories/1/items/1/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/2/subcategories/1/items/1/extracted/safety/common/0` | common[0] | string | 부종 |
| `/modality/2/subcategories/1/items/1/extracted/safety/common/1` | common[1] | string | 미세 결절 |
| `/modality/2/subcategories/1/items/1/extracted/safety/common/2` | common[2] | string | 일시적 홍반 |
| `/modality/2/subcategories/1/items/1/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/2/subcategories/1/items/1/extracted/safety/serious/0` | serious[0] | string | 감염 |
| `/modality/2/subcategories/1/items/1/extracted/safety/serious/1` | serious[1] | string | 지연성 이물반응 |
| `/modality/2/subcategories/1/items/1/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/2/subcategories/1/items/1/extracted/onset_duration/onset` | onset | string | 2-4주 |
| `/modality/2/subcategories/1/items/1/extracted/onset_duration/duration` | duration | string | 18-24개월 |
| `/modality/2/subcategories/1/items/1/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/2/subcategories/1/items/1/extracted/aftercare/0` | aftercare[0] | string | 시술 후 가벼운 마사지로 균일한 분포 유도 (의사 지시에 따라) |
| `/modality/2/subcategories/1/items/1/extracted/aftercare/1` | aftercare[1] | string | 고강도 운동 3주 피하기 |
| `/modality/2/subcategories/1/items/1/extracted/aftercare/2` | aftercare[2] | string | [시술 주기 참고] 반복 시술 권장. 1개월 간격, 3회 이상 코스. 콜라겐 생성 완료까지 2-6개월 소요. 소재별 지속: PLLA 24개월+, CaHA 12-24개월, PCL 36개월+ (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/2/subcategories/1/items/2` | items[2] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/2/subcategories/1/items/2/id` | id | string | auto-M3-1775364775147 |
| `/modality/2/subcategories/1/items/2/name` | name | string | HArmonyCa |
| `/modality/2/subcategories/1/items/2/detail` | detail | string | CaHA+HA |
| `/modality/2/subcategories/1/items/2/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/2/subcategories/1/items/2/extracted/overview` | overview | string | 칼슘하이드록시아파타이트와 히알루론산의 복합 바이오스티뮬레이터 |
| `/modality/2/subcategories/1/items/2/extracted/mechanism` | mechanism | string | CaHA 마이크로스피어가 콜라겐 생성을 자극하고 HA가 즉시 볼륨을 제공합니다. 이중 작용으로 즉각적이면서도 지속적인 개선 효과를 나타냅니다. |
| `/modality/2/subcategories/1/items/2/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/2/subcategories/1/items/2/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/2/subcategories/1/items/2/extracted/indications/primary/0` | primary[0] | string | 즉각적 볼륨 증대 |
| `/modality/2/subcategories/1/items/2/extracted/indications/primary/1` | primary[1] | string | 콜라겐 재생 |
| `/modality/2/subcategories/1/items/2/extracted/indications/primary/2` | primary[2] | string | 피부 질감 개선 |
| `/modality/2/subcategories/1/items/2/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/2/subcategories/1/items/2/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/2/subcategories/1/items/2/extracted/safety/common/0` | common[0] | string | 주사 부위 부종 |
| `/modality/2/subcategories/1/items/2/extracted/safety/common/1` | common[1] | string | 일시적 압통 |
| `/modality/2/subcategories/1/items/2/extracted/safety/common/2` | common[2] | string | 발적 |
| `/modality/2/subcategories/1/items/2/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/2/subcategories/1/items/2/extracted/onset_duration/onset` | onset | string | 즉시 |
| `/modality/2/subcategories/1/items/2/extracted/onset_duration/duration` | duration | string | 15-18개월 |
| `/modality/2/subcategories/1/items/2/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/2/subcategories/1/items/2/extracted/aftercare/0` | aftercare[0] | string | 24시간 메이크업 자제 |
| `/modality/2/subcategories/1/items/2/extracted/aftercare/1` | aftercare[1] | string | 일주일간 사우나 피하기 |
| `/modality/2/subcategories/1/items/2/extracted/aftercare/2` | aftercare[2] | string | 부드러운 마사지 |
| `/modality/2/subcategories/1/items/2/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 반복 시술 권장. 1개월 간격, 3회 이상 코스. 콜라겐 생성 완료까지 2-6개월 소요. 소재별 지속: PLLA 24개월+, CaHA 12-24개월, PCL 36개월+ (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/2/subcategories/2` | subcategories[2] | object | {object, 키 3: id, label, items} |
| `/modality/2/subcategories/2/id` | id | string | M3-5 |
| `/modality/2/subcategories/2/label` | label | string | 콜라겐 |
| `/modality/2/subcategories/2/items` | items | array | [array, 원소 4] |
| `/modality/2/subcategories/2/items/0` | items[0] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/2/subcategories/2/items/0/id` | id | string | auto-13-1774737181584 |
| `/modality/2/subcategories/2/items/0/name` | name | string | 콜라쥬 |
| `/modality/2/subcategories/2/items/0/detail` | detail | string | `""` (빈 문자열) |
| `/modality/2/subcategories/2/items/0/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/2/subcategories/2/items/0/extracted/overview` | overview | string | 콜라겐 기반 필러 |
| `/modality/2/subcategories/2/items/0/extracted/mechanism` | mechanism | string | 생체 유래 콜라겐 단백질이 직접 진피 내 볼륨 제공 및 구조 지지. 타입 I/III 콜라겐으로 천연 세포외기질 모방. |
| `/modality/2/subcategories/2/items/0/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/2/subcategories/2/items/0/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/2/subcategories/2/items/0/extracted/indications/primary/0` | primary[0] | string | 얕은 주름 |
| `/modality/2/subcategories/2/items/0/extracted/indications/primary/1` | primary[1] | string | 입술 풍만 |
| `/modality/2/subcategories/2/items/0/extracted/indications/primary/2` | primary[2] | string | 미세 흉터 |
| `/modality/2/subcategories/2/items/0/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/2/subcategories/2/items/0/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/2/subcategories/2/items/0/extracted/safety/common/0` | common[0] | string | 부종 |
| `/modality/2/subcategories/2/items/0/extracted/safety/common/1` | common[1] | string | 멍 |
| `/modality/2/subcategories/2/items/0/extracted/safety/common/2` | common[2] | string | 일시적 결절 |
| `/modality/2/subcategories/2/items/0/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/2/subcategories/2/items/0/extracted/safety/serious/0` | serious[0] | string | 알레르기 반응 |
| `/modality/2/subcategories/2/items/0/extracted/safety/serious/1` | serious[1] | string | 이물반응 |
| `/modality/2/subcategories/2/items/0/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/2/subcategories/2/items/0/extracted/onset_duration/onset` | onset | string | 즉시-3일 |
| `/modality/2/subcategories/2/items/0/extracted/onset_duration/duration` | duration | string | 3-6개월(상대적 단기) |
| `/modality/2/subcategories/2/items/0/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/2/subcategories/2/items/0/extracted/aftercare/0` | aftercare[0] | string | 사전 패치테스트 권장 |
| `/modality/2/subcategories/2/items/0/extracted/aftercare/1` | aftercare[1] | string | 48시간 냉찜질 |
| `/modality/2/subcategories/2/items/0/extracted/aftercare/2` | aftercare[2] | string | [시술 주기 참고] 반복 시술 권장. 1개월 간격, 3회 이상 코스. 콜라겐 생성 완료까지 2-6개월 소요. 소재별 지속: PLLA 24개월+, CaHA 12-24개월, PCL 36개월+ (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/2/subcategories/2/items/1` | items[1] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/2/subcategories/2/items/1/id` | id | string | auto-14-1774737181584 |
| `/modality/2/subcategories/2/items/1/name` | name | string | 레티젠 |
| `/modality/2/subcategories/2/items/1/detail` | detail | string | `""` (빈 문자열) |
| `/modality/2/subcategories/2/items/1/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/2/subcategories/2/items/1/extracted/overview` | overview | string | 정제 콜라겐 기반 조직충전제 |
| `/modality/2/subcategories/2/items/1/extracted/mechanism` | mechanism | string | 인체/동물 유래 정제 콜라겐을 진피에 주입하여 볼륨을 회복하고 조직 재건을 지원한다. 숙주 조직과 생체적합적으로 통합되어 자연스러운 볼륨을 제공한다. |
| `/modality/2/subcategories/2/items/1/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/2/subcategories/2/items/1/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/2/subcategories/2/items/1/extracted/indications/primary/0` | primary[0] | string | 전체 피부 탄력 저하 |
| `/modality/2/subcategories/2/items/1/extracted/indications/primary/1` | primary[1] | string | 주름 |
| `/modality/2/subcategories/2/items/1/extracted/indications/primary/2` | primary[2] | string | 피부 품질 개선 |
| `/modality/2/subcategories/2/items/1/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/2/subcategories/2/items/1/extracted/safety/common` | common | array | [array, 원소 2] |
| `/modality/2/subcategories/2/items/1/extracted/safety/common/0` | common[0] | string | 주사 부위 부종 |
| `/modality/2/subcategories/2/items/1/extracted/safety/common/1` | common[1] | string | 가려움증 |
| `/modality/2/subcategories/2/items/1/extracted/safety/serious` | serious | array | [array, 원소 1] |
| `/modality/2/subcategories/2/items/1/extracted/safety/serious/0` | serious[0] | string | 감염(배양 과정) |
| `/modality/2/subcategories/2/items/1/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/2/subcategories/2/items/1/extracted/onset_duration/onset` | onset | string | 2-4주 |
| `/modality/2/subcategories/2/items/1/extracted/onset_duration/duration` | duration | string | 12-18개월 |
| `/modality/2/subcategories/2/items/1/extracted/aftercare` | aftercare | array | [array, 원소 5] |
| `/modality/2/subcategories/2/items/1/extracted/aftercare/0` | aftercare[0] | string | 세포 배양 기간 필수(2-3주) |
| `/modality/2/subcategories/2/items/1/extracted/aftercare/1` | aftercare[1] | string | 시술 후 가벼운 마사지로 균일한 분포 유도 (의사 지시에 따라) |
| `/modality/2/subcategories/2/items/1/extracted/aftercare/2` | aftercare[2] | string | 결절 발생 시 내원 상담 |
| `/modality/2/subcategories/2/items/1/extracted/aftercare/3` | aftercare[3] | string | 멍/부종은 수일 내 자연 소실 |
| `/modality/2/subcategories/2/items/1/extracted/aftercare/4` | aftercare[4] | string | [시술 주기 참고] 반복 시술 권장. 1개월 간격, 3회 이상 코스. 콜라겐 생성 완료까지 2-6개월 소요. 소재별 지속: PLLA 24개월+, CaHA 12-24개월, PCL 36개월+ (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/2/subcategories/2/items/2` | items[2] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/2/subcategories/2/items/2/id` | id | string | auto-15-1774737181584 |
| `/modality/2/subcategories/2/items/2/name` | name | string | 미라콜 |
| `/modality/2/subcategories/2/items/2/detail` | detail | string | `""` (빈 문자열) |
| `/modality/2/subcategories/2/items/2/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/2/subcategories/2/items/2/extracted/overview` | overview | string | 콜라겐 기반 볼륨 충전제 |
| `/modality/2/subcategories/2/items/2/extracted/mechanism` | mechanism | string | 정제된 콜라겐 매트릭스를 진피에 주입하여 즉각적 볼륨을 제공한다. 생체적합성 콜라겐이 조직에 통합되면서 자가 세포의 침투와 리모델링을 촉진한다. |
| `/modality/2/subcategories/2/items/2/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/2/subcategories/2/items/2/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/2/subcategories/2/items/2/extracted/indications/primary/0` | primary[0] | string | 피부 위축 |
| `/modality/2/subcategories/2/items/2/extracted/indications/primary/1` | primary[1] | string | 넓은 주름 |
| `/modality/2/subcategories/2/items/2/extracted/indications/primary/2` | primary[2] | string | 볼 함몰 |
| `/modality/2/subcategories/2/items/2/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/2/subcategories/2/items/2/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/2/subcategories/2/items/2/extracted/safety/common/0` | common[0] | string | 부종 |
| `/modality/2/subcategories/2/items/2/extracted/safety/common/1` | common[1] | string | 결절 형성 |
| `/modality/2/subcategories/2/items/2/extracted/safety/common/2` | common[2] | string | 압통 |
| `/modality/2/subcategories/2/items/2/extracted/safety/serious` | serious | array | [array, 원소 1] |
| `/modality/2/subcategories/2/items/2/extracted/safety/serious/0` | serious[0] | string | 육아종 반응 |
| `/modality/2/subcategories/2/items/2/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/2/subcategories/2/items/2/extracted/onset_duration/onset` | onset | string | 3-6주 |
| `/modality/2/subcategories/2/items/2/extracted/onset_duration/duration` | duration | string | 18-24개월 |
| `/modality/2/subcategories/2/items/2/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/2/subcategories/2/items/2/extracted/aftercare/0` | aftercare[0] | string | 시술 후 가벼운 마사지로 균일한 분포 유도 (의사 지시에 따라) |
| `/modality/2/subcategories/2/items/2/extracted/aftercare/1` | aftercare[1] | string | 과도한 근육 운동 제한 |
| `/modality/2/subcategories/2/items/2/extracted/aftercare/2` | aftercare[2] | string | [시술 주기 참고] 반복 시술 권장. 1개월 간격, 3회 이상 코스. 콜라겐 생성 완료까지 2-6개월 소요. 소재별 지속: PLLA 24개월+, CaHA 12-24개월, PCL 36개월+ (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/2/subcategories/2/items/3` | items[3] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/2/subcategories/2/items/3/id` | id | string | auto-M3-1775364775146 |
| `/modality/2/subcategories/2/items/3/name` | name | string | 콜라겐핀 |
| `/modality/2/subcategories/2/items/3/detail` | detail | string | 인체유래주입 |
| `/modality/2/subcategories/2/items/3/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/2/subcategories/2/items/3/extracted/overview` | overview | string | 인체 유래 콜라겐을 이용한 자가 콜라겐 부스터 |
| `/modality/2/subcategories/2/items/3/extracted/mechanism` | mechanism | string | 인체에서 추출한 콜라겐을 직접 주입하여 조직을 보강합니다. 생체 적합성이 높아 자연스러운 콜라겐 재생을 유도합니다. |
| `/modality/2/subcategories/2/items/3/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/2/subcategories/2/items/3/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/2/subcategories/2/items/3/extracted/indications/primary/0` | primary[0] | string | 자연스러운 콜라겐 보충 |
| `/modality/2/subcategories/2/items/3/extracted/indications/primary/1` | primary[1] | string | 피부 재생 |
| `/modality/2/subcategories/2/items/3/extracted/indications/primary/2` | primary[2] | string | 잔주름 개선 |
| `/modality/2/subcategories/2/items/3/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/2/subcategories/2/items/3/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/2/subcategories/2/items/3/extracted/safety/common/0` | common[0] | string | 일시적 부종 |
| `/modality/2/subcategories/2/items/3/extracted/safety/common/1` | common[1] | string | 주사 부위 발적 |
| `/modality/2/subcategories/2/items/3/extracted/safety/common/2` | common[2] | string | 가벼운 압통 |
| `/modality/2/subcategories/2/items/3/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/2/subcategories/2/items/3/extracted/onset_duration/onset` | onset | string | 2-4주 |
| `/modality/2/subcategories/2/items/3/extracted/onset_duration/duration` | duration | string | 8-12개월 |
| `/modality/2/subcategories/2/items/3/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/2/subcategories/2/items/3/extracted/aftercare/0` | aftercare[0] | string | 감염 예방 관리 |
| `/modality/2/subcategories/2/items/3/extracted/aftercare/1` | aftercare[1] | string | 충분한 보습 |
| `/modality/2/subcategories/2/items/3/extracted/aftercare/2` | aftercare[2] | string | [시술 주기 참고] 반복 시술 권장. 1개월 간격, 3회 이상 코스. 콜라겐 생성 완료까지 2-6개월 소요. 소재별 지속: PLLA 24개월+, CaHA 12-24개월, PCL 36개월+ (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/2/subcategories/3` | subcategories[3] | object | {object, 키 3: id, label, items} |
| `/modality/2/subcategories/3/id` | id | string | M3-3 |
| `/modality/2/subcategories/3/label` | label | string | PCL (폴리카프로락톤) |
| `/modality/2/subcategories/3/items` | items | array | [array, 원소 4] |
| `/modality/2/subcategories/3/items/0` | items[0] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/2/subcategories/3/items/0/id` | id | string | M3-3-1 |
| `/modality/2/subcategories/3/items/0/name` | name | string | 엘란쎄 |
| `/modality/2/subcategories/3/items/0/detail` | detail | string | 싱클레어 |
| `/modality/2/subcategories/3/items/0/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/2/subcategories/3/items/0/extracted/overview` | overview | string | PCL 기반 장기 콜라겐 부스터 |
| `/modality/2/subcategories/3/items/0/extracted/mechanism` | mechanism | string | Polycaprolactone(PCL) 미세입자의 1:4 희석액을 진피 내 주사 시 이물반응으로 콜라겐 신생 촉진. 진피 두께 1년 내 26.7% 증가, 4년간 48% 증가. PCL 입자는 4년 이상 생분해 가능. |
| `/modality/2/subcategories/3/items/0/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/2/subcategories/3/items/0/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/2/subcategories/3/items/0/extracted/indications/primary/0` | primary[0] | string | 심한 주름 |
| `/modality/2/subcategories/3/items/0/extracted/indications/primary/1` | primary[1] | string | 얼굴 위축 |
| `/modality/2/subcategories/3/items/0/extracted/indications/primary/2` | primary[2] | string | 피부 탄력 재생 |
| `/modality/2/subcategories/3/items/0/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/2/subcategories/3/items/0/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/2/subcategories/3/items/0/extracted/safety/common/0` | common[0] | string | 부종 |
| `/modality/2/subcategories/3/items/0/extracted/safety/common/1` | common[1] | string | 미세 결절 |
| `/modality/2/subcategories/3/items/0/extracted/safety/common/2` | common[2] | string | 일시적 홍반 |
| `/modality/2/subcategories/3/items/0/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/2/subcategories/3/items/0/extracted/safety/serious/0` | serious[0] | string | 지연성 육아종 |
| `/modality/2/subcategories/3/items/0/extracted/safety/serious/1` | serious[1] | string | 이물반응 |
| `/modality/2/subcategories/3/items/0/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/2/subcategories/3/items/0/extracted/onset_duration/onset` | onset | string | 4-8주 |
| `/modality/2/subcategories/3/items/0/extracted/onset_duration/duration` | duration | string | 36-48개월(장기) |
| `/modality/2/subcategories/3/items/0/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/2/subcategories/3/items/0/extracted/aftercare/0` | aftercare[0] | string | 시술 후 가벼운 마사지로 균일한 분포 유도 (의사 지시에 따라) |
| `/modality/2/subcategories/3/items/0/extracted/aftercare/1` | aftercare[1] | string | 반복 시술 가능 |
| `/modality/2/subcategories/3/items/0/extracted/aftercare/2` | aftercare[2] | string | [시술 주기 참고] 반복 시술 권장. 1개월 간격, 3회 이상 코스. 콜라겐 생성 완료까지 2-6개월 소요. 소재별 지속: PLLA 24개월+, CaHA 12-24개월, PCL 36개월+ (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/2/subcategories/3/items/1` | items[1] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/2/subcategories/3/items/1/id` | id | string | M3-3-2 |
| `/modality/2/subcategories/3/items/1/name` | name | string | 고우리 |
| `/modality/2/subcategories/3/items/1/detail` | detail | string | 덱스레보 액상 PCL |
| `/modality/2/subcategories/3/items/1/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/2/subcategories/3/items/1/extracted/overview` | overview | string | 액상형 PCL 콜라겐 부스터 |
| `/modality/2/subcategories/3/items/1/extracted/mechanism` | mechanism | string | 액상 형태의 Polycaprolactone(PCL) 입자 현탁액으로 균등한 분배 가능. PCL의 이물반응 유도 콜라겐 생성 메커니즘과 시술 용이성 결합. |
| `/modality/2/subcategories/3/items/1/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/2/subcategories/3/items/1/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/2/subcategories/3/items/1/extracted/indications/primary/0` | primary[0] | string | 전면 주름 |
| `/modality/2/subcategories/3/items/1/extracted/indications/primary/1` | primary[1] | string | 피부 처짐 |
| `/modality/2/subcategories/3/items/1/extracted/indications/primary/2` | primary[2] | string | 넓은 영역 위축 |
| `/modality/2/subcategories/3/items/1/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/2/subcategories/3/items/1/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/2/subcategories/3/items/1/extracted/safety/common/0` | common[0] | string | 부종 |
| `/modality/2/subcategories/3/items/1/extracted/safety/common/1` | common[1] | string | 결절 |
| `/modality/2/subcategories/3/items/1/extracted/safety/common/2` | common[2] | string | 가벼운 멍 |
| `/modality/2/subcategories/3/items/1/extracted/safety/serious` | serious | array | [array, 원소 1] |
| `/modality/2/subcategories/3/items/1/extracted/safety/serious/0` | serious[0] | string | 과도한 이물반응 |
| `/modality/2/subcategories/3/items/1/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/2/subcategories/3/items/1/extracted/onset_duration/onset` | onset | string | 4-8주 |
| `/modality/2/subcategories/3/items/1/extracted/onset_duration/duration` | duration | string | 36-48개월 |
| `/modality/2/subcategories/3/items/1/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/2/subcategories/3/items/1/extracted/aftercare/0` | aftercare[0] | string | 시술 후 가벼운 마사지로 균일한 분포 유도 (의사 지시에 따라) |
| `/modality/2/subcategories/3/items/1/extracted/aftercare/1` | aftercare[1] | string | 규칙적 추적 관찰 |
| `/modality/2/subcategories/3/items/1/extracted/aftercare/2` | aftercare[2] | string | [시술 주기 참고] 반복 시술 권장. 1개월 간격, 3회 이상 코스. 콜라겐 생성 완료까지 2-6개월 소요. 소재별 지속: PLLA 24개월+, CaHA 12-24개월, PCL 36개월+ (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/2/subcategories/3/items/2` | items[2] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/2/subcategories/3/items/2/id` | id | string | auto-16-1774737181584 |
| `/modality/2/subcategories/3/items/2/name` | name | string | 라풀렌 |
| `/modality/2/subcategories/3/items/2/detail` | detail | string | 삼양홀딩스 |
| `/modality/2/subcategories/3/items/2/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/2/subcategories/3/items/2/extracted/overview` | overview | string | 바이오스티뮬레이터 기반 장기 리프팅 |
| `/modality/2/subcategories/3/items/2/extracted/mechanism` | mechanism | string | 고함량 생분해성 바이오폴리머 입자로 조직 내 이물반응을 유도하여 자체 콜라겐 생성 메커니즘 활성화. 장기간 진피 구조 강화 및 탄력성 회복. |
| `/modality/2/subcategories/3/items/2/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/2/subcategories/3/items/2/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/2/subcategories/3/items/2/extracted/indications/primary/0` | primary[0] | string | 중등도 이상 주름 |
| `/modality/2/subcategories/3/items/2/extracted/indications/primary/1` | primary[1] | string | 얼굴 전체 위축 |
| `/modality/2/subcategories/3/items/2/extracted/indications/primary/2` | primary[2] | string | 팔자주름 |
| `/modality/2/subcategories/3/items/2/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/2/subcategories/3/items/2/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/2/subcategories/3/items/2/extracted/safety/common/0` | common[0] | string | 부종 |
| `/modality/2/subcategories/3/items/2/extracted/safety/common/1` | common[1] | string | 경미한 결절 |
| `/modality/2/subcategories/3/items/2/extracted/safety/common/2` | common[2] | string | 압통 |
| `/modality/2/subcategories/3/items/2/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/2/subcategories/3/items/2/extracted/safety/serious/0` | serious[0] | string | 이물반응 |
| `/modality/2/subcategories/3/items/2/extracted/safety/serious/1` | serious[1] | string | 감염 |
| `/modality/2/subcategories/3/items/2/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/2/subcategories/3/items/2/extracted/onset_duration/onset` | onset | string | 3-6주 |
| `/modality/2/subcategories/3/items/2/extracted/onset_duration/duration` | duration | string | 24-36개월 |
| `/modality/2/subcategories/3/items/2/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/2/subcategories/3/items/2/extracted/aftercare/0` | aftercare[0] | string | 격렬한 운동 제한(초기) |
| `/modality/2/subcategories/3/items/2/extracted/aftercare/1` | aftercare[1] | string | 정기 추적 관찰 |
| `/modality/2/subcategories/3/items/2/extracted/aftercare/2` | aftercare[2] | string | [시술 주기 참고] 반복 시술 권장. 1개월 간격, 3회 이상 코스. 콜라겐 생성 완료까지 2-6개월 소요. 소재별 지속: PLLA 24개월+, CaHA 12-24개월, PCL 36개월+ (개인차 있으며, 의사와 상의하여 결정) |

## 잠정 관찰 (원문 아님 · 직접 읽기 기록)

| 상태 | 근거 Pointer | 관찰 |
|---|---|---|
| P | `/modality/2/subcategories` | M3 subcategories 배열 순서: M3-1(PLLA), M3-2(CaHA), M3-5(콜라겐), M3-3(PCL), M3-4, M3-new-…, M3-new-… — id 순서와 다르다. 하위분류 축이 재질(성분)이다. label 은 '약어 (한글 풀이)' 형식. |
| I | `/modality/2/subcategories/1/items/1/extracted/overview`, `/modality/2/subcategories/1/items/1/extracted/mechanism`, `/modality/2/subcategories/1` | 디클래씨: overview 'PDLLA/HA 복합 바이오스티뮬레이터', mechanism 'CaHA 미세구와 CMC 겔 캐리어', 소속 하위분류는 CaHA. 한 항목 안에서 재질 서술이 충돌. |
| I | `/modality/2/subcategories/2/items/1/extracted/aftercare/0`, `/modality/2/subcategories/2/items/1/extracted/safety/serious/0`, `/modality/2/subcategories/2/items/1/extracted/mechanism` | 레티젠: mechanism 은 '정제 콜라겐 주입' 인데 aftercare '세포 배양 기간 필수(2-3주)', serious '감염(배양 과정)' — 세포배양 시술 서술이 섞여 있다. |
| I | `/modality/2/subcategories/0/items/2/extracted/overview`, `/modality/2/subcategories/0/items/2/extracted/onset_duration/onset` | 에스테필 overview '즉시 볼륨 효과는 제한적 … 서서히 볼륨' vs onset '즉시-2일'. |
| P | `/modality/2/subcategories/0/items/1/detail`, `/modality/2/subcategories/0/items/1/extracted/safety/serious/0` | 올리디아 detail 'PRP사이언스'(회사명), serious '감염(혈액유래 시술)' — PLLA 제품에 혈액유래 시술 표현. 판단은 후속(F). |
| P | `/modality/2/subcategories/2/items/0/detail`, `/modality/2/subcategories/2/items/1/detail`, `/modality/2/subcategories/2/items/2/detail` | M3-5 콜라겐 하위분류의 앞 세 항목 detail 은 빈 문자열 "". 제조사 정보 없음. |
| P | `/modality/2/subcategories/0/items/0/extracted/aftercare/2` | M3 상용구 '[시술 주기 참고] 반복 시술 권장. 1개월 간격, 3회 이상 코스. … 소재별 지속: PLLA 24개월+, CaHA 12-24개월, PCL 36개월+' — 여기서 '+' 는 '이상'(하한) 표기로 쓰여 README 의 '+ = 함께' 와 다르다(GLOBAL-F01). 재질별 수치를 모든 재질 항목에 일괄 부착. |
| P | `/modality/2/subcategories/1/items/2/detail`, `/modality/2/subcategories/0/items/3/detail` | detail 이 성분 조합('CaHA+HA')이나 성분명('수용성콜라겐'), 시술 방식('인체유래주입')인 항목. detail 의 정보 종류가 항목마다 다르다. |
| P | `/modality/2/subcategories/3/items/0/extracted/mechanism` | 엘란쎄 mechanism 은 희석비(1:4)·진피 두께 증가율(1년 26.7%, 4년 48%)·생분해 기간(4년 이상) 수치를 담는다. 출처 미기재(B 아님 — 수치 자체는 원문). |

## 수동 복합 표현 (원문 구간)

| Pointer | 구간 | 원문 표현 | 관점 | 메모 |
|---|---|---|---|---|
| `/modality/2/subcategories/0/items/0/extracted/aftercare/0` | [0, 55] | 5-5-5 마사지는 선택 (결절 예방효과 RCT 미입증; 결절 예방의 핵심은 희석·수화·주입 깊이) | 시술·제품명, 부정, 주장, 조건 | '5-5-5' 는 기법명(분석기는 W_SERIAL) |
| `/modality/2/subcategories/0/items/0/extracted/onset_duration/onset` | [0, 9] | 4-6주(점진적) | 수량·단위·시간, 수식 |  |
| `/modality/2/subcategories/0/items/0/extracted/aftercare/2` | [21, 37] | 1개월 간격, 3회 이상 코스 | 수량·단위·시간, 범위 | 회차 하한 |
| `/modality/2/subcategories/0/items/0/extracted/aftercare/2` | [39, 59] | 콜라겐 생성 완료까지 2-6개월 소요 | 수량·단위·시간, 범위 |  |
| `/modality/2/subcategories/0/items/0/extracted/aftercare/2` | [61, 104] | 소재별 지속: PLLA 24개월+, CaHA 12-24개월, PCL 36개월+ | 수량·단위·시간, 범위, 기호 | '+' = 이상 |
| `/modality/2/subcategories/0/items/1/extracted/aftercare/0` | [0, 16] | 자극적 제품 사용 자제(3일) | 부정, 수량·단위·시간 |  |
| `/modality/2/subcategories/0/items/1/extracted/aftercare/1` | [0, 35] | 시술 후 가벼운 마사지로 균일한 분포 유도 (의사 지시에 따라) | 수식, 조건 | M3 반복 문장. M1·M2 의 '마사지 자제'와 방향 반대 |
| `/modality/2/subcategories/0/items/1/extracted/aftercare/2` | [0, 13] | 결절 발생 시 내원 상담 | 조건 |  |
| `/modality/2/subcategories/0/items/2/extracted/overview` | [40, 97] | HA 필러가 아니며 즉시 볼륨 효과는 제한적이고 수주에 걸친 신생 콜라겐 형성으로 서서히 볼륨이 나타남 | 부정, 수식, 수량·단위·시간 |  |
| `/modality/2/subcategories/0/items/2/detail` | [0, 12] | 레지메드/휴메딕스 유통 | 기호 | '/' 두 유통사 |
| `/modality/2/subcategories/0/items/2/extracted/mechanism` | [49, 69] | I형/III형 콜라겐 합성을 자극한다 | 기호 |  |
| `/modality/2/subcategories/0/items/3/extracted/safety/common/2` | [0, 9] | 결절 형성 가능성 | 가능성·빈도 |  |
| `/modality/2/subcategories/1/items/0/extracted/mechanism` | [47, 96] | 즉각적 볼륨 제공 후 CMC 흡수되면서 CaHA 입자가 이물반응을 통해 콜라겐 생성 지속 | 수량·단위·시간, 조건 | 두 단계 기전 |
| `/modality/2/subcategories/1/items/1/extracted/aftercare/1` | [0, 13] | 고강도 운동 3주 피하기 | 수식, 수량·단위·시간, 부정 |  |
| `/modality/2/subcategories/2/items/0/extracted/onset_duration/duration` | [0, 13] | 3-6개월(상대적 단기) | 수량·단위·시간, 비교 |  |
| `/modality/2/subcategories/2/items/0/extracted/aftercare/0` | [0, 11] | 사전 패치테스트 권장 | 수량·단위·시간 | 시술 전 지시 |
| `/modality/2/subcategories/2/items/1/extracted/mechanism` | [0, 15] | 인체/동물 유래 정제 콜라겐 | 기호 | '/' 대안/나열 |
| `/modality/2/subcategories/2/items/1/extracted/aftercare/0` | [0, 17] | 세포 배양 기간 필수(2-3주) | 수량·단위·시간 | S008-I02 |
| `/modality/2/subcategories/3/items/0/extracted/mechanism` | [28, 35] | 1:4 희석액 | 수량·단위·시간 | 비율 |
| `/modality/2/subcategories/3/items/0/extracted/mechanism` | [65, 96] | 진피 두께 1년 내 26.7% 증가, 4년간 48% 증가 | 수량·단위·시간 |  |
| `/modality/2/subcategories/3/items/0/extracted/mechanism` | [98, 118] | PCL 입자는 4년 이상 생분해 가능 | 범위, 가능성·빈도 |  |
| `/modality/2/subcategories/3/items/0/extracted/onset_duration/duration` | [0, 11] | 36-48개월(장기) | 수량·단위·시간 |  |
| `/modality/2/subcategories/3/items/2/extracted/aftercare/0` | [0, 13] | 격렬한 운동 제한(초기) | 부정, 수량·단위·시간 | 비수치 시점 |
| `/modality/2/subcategories/3/items/2/extracted/indications/primary/0` | [0, 9] | 중등도 이상 주름 | 범위, 수식 |  |

## 형태소 분석 확인 (알려진 오분절 K)

| 범위 | 표면형 | 문제 | 영향 |
|---|---|---|---|
| all | 콜라쥬 | 제품명을 콜라/NNG 이/VCP 쥬/EF 로 분석 | 제품명 소실 |
| all | 디클래씨 | 디클래/NNP 씨/NNB — 제품명 끝 '씨'를 의존명사로 | 제품명 절단 |
| all | 콜라겐핀 | 콜라겐/NNP 핀/NNG | 제품명 분해 |
| all | 5-5-5 | 기법명 '5-5-5'를 W_SERIAL 한 토큰으로 — 범위·일련번호와 구분 안 됨 | GLOBAL-K01 과 같은 태그지만 범위 아님 |

## 미결

| ID | 상태 | Pointer | 내용 | 영향·후속 |
|---|---|---|---|---|
| S008-I01 | I | `/modality/2/subcategories/1/items/1/extracted/overview`, `/modality/2/subcategories/1/items/1/extracted/mechanism` | 디클래씨 재질 서술 충돌(PDLLA/HA vs CaHA/CMC). | 재질 축 분류 시 확인 필요(원본 확인 후보) |
| S008-I02 | I | `/modality/2/subcategories/2/items/1/extracted/aftercare/0`, `/modality/2/subcategories/2/items/1/extracted/safety/serious/0` | 레티젠 콜라겐 주입 항목에 세포배양 서술. | 다른 항목 서술 혼입 가능성 — 후속 확인 |
| S008-I03 | I | `/modality/2/subcategories/0/items/2/extracted/overview`, `/modality/2/subcategories/0/items/2/extracted/onset_duration/onset` | 에스테필 즉시효과 서술 충돌. | 시점 정보 채택 시 확인 |
| S008-B01 | B | `/modality/2/subcategories/2/items/0/detail`, `/modality/2/subcategories/2/items/1/detail`, `/modality/2/subcategories/2/items/2/detail` | detail 빈 문자열 — 제조사·특징 정보 없음. | 제품 식별 정보 부족 |

