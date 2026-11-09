# S035 — M12 마이크로니들링(MTS)

- 읽기 상태: **read** · 마지막 읽은 Pointer `/modality/11/name`
- 단위: id, category, category_en, group, subcategories 컨테이너, M12-1 items/0, M12-1 items/1, M12-1 items/2, M12-2 items/0, M12-2 items/1, M12-2 items/2, M12-2 items/3, extracted, products 컨테이너, name
- 상위 문맥(공동 참조·소유 아님): 없음
- 기계 기록: `source-map.json`(section=S035) · `morphology/S035.json` · `expressions.json`(section=S035) · 읽기 렌더 `reading/S035.txt`

## 원문 값 (원본 컬럼명 그대로, 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/modality/11` | modality[11] | object | {object, 키 8: id, category, category_en, group, subcategories, extracted, products, name} |
| `/modality/11/id` | id | string | M12 |
| `/modality/11/category` | category | string | 마이크로니들링(MTS) |
| `/modality/11/category_en` | category_en | string | Microneedling |
| `/modality/11/group` | group | string | 시술/기기 |
| `/modality/11/subcategories` | subcategories | array | [array, 원소 2] |
| `/modality/11/subcategories/0` | subcategories[0] | object | {object, 키 3: id, label, items} |
| `/modality/11/subcategories/0/id` | id | string | M12-1 |
| `/modality/11/subcategories/0/label` | label | string | 수동 MTS |
| `/modality/11/subcategories/0/items` | items | array | [array, 원소 3] |
| `/modality/11/subcategories/0/items/0` | items[0] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/11/subcategories/0/items/0/id` | id | string | M12-1-1 |
| `/modality/11/subcategories/0/items/0/name` | name | string | 더마롤러 |
| `/modality/11/subcategories/0/items/0/detail` | detail | string | 롤러형 |
| `/modality/11/subcategories/0/items/0/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/11/subcategories/0/items/0/extracted/overview` | overview | string | 롤러형 마이크로니들로 피부에 미세한 자극을 주는 시술 |
| `/modality/11/subcategories/0/items/0/extracted/mechanism` | mechanism | string | 손으로 조작하는 롤러형 기구의 바늘(0.2~2.0mm)이 피부 표면을 균일하게 자극하여 콜라겐 생성을 유도한다. 롤러의 크기와 방향에 따라 넓은 면적을 효율적으로 시술할 수 있다. |
| `/modality/11/subcategories/0/items/0/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/11/subcategories/0/items/0/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/11/subcategories/0/items/0/extracted/indications/primary/0` | primary[0] | string | 피부 노화 개선 (주름, 잔주름) |
| `/modality/11/subcategories/0/items/0/extracted/indications/primary/1` | primary[1] | string | 피부 탄력 개선 |
| `/modality/11/subcategories/0/items/0/extracted/indications/primary/2` | primary[2] | string | 흉터 개선 (위축성 흉터, 여드름 흉터) |
| `/modality/11/subcategories/0/items/0/extracted/indications/primary/3` | primary[3] | string | 모공 축소 |
| `/modality/11/subcategories/0/items/0/extracted/indications/primary/4` | primary[4] | string | 색소침착 개선 |
| `/modality/11/subcategories/0/items/0/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/11/subcategories/0/items/0/extracted/safety/common` | common | array | [array, 원소 4] |
| `/modality/11/subcategories/0/items/0/extracted/safety/common/0` | common[0] | string | 시술 직후 홍반 |
| `/modality/11/subcategories/0/items/0/extracted/safety/common/1` | common[1] | string | 미세한 출혈 |
| `/modality/11/subcategories/0/items/0/extracted/safety/common/2` | common[2] | string | 일시적 부종 |
| `/modality/11/subcategories/0/items/0/extracted/safety/common/3` | common[3] | string | 가려움증 |
| `/modality/11/subcategories/0/items/0/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/11/subcategories/0/items/0/extracted/safety/serious/0` | serious[0] | string | 심한 감염 (무균 처리 미흡 시) |
| `/modality/11/subcategories/0/items/0/extracted/safety/serious/1` | serious[1] | string | 색소 이상 (색소침착/감소) |
| `/modality/11/subcategories/0/items/0/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/11/subcategories/0/items/0/extracted/onset_duration/onset` | onset | string | 3~7일 후부터 콜라겐 재생 시작, 2~4주 후 시각적 개선 |
| `/modality/11/subcategories/0/items/0/extracted/onset_duration/duration` | duration | string | 시술 효과는 3~6개월 지속, 정기적 시술로 누적 효과 기대 |
| `/modality/11/subcategories/0/items/0/extracted/aftercare` | aftercare | array | [array, 원소 6] |
| `/modality/11/subcategories/0/items/0/extracted/aftercare/0` | aftercare[0] | string | 시술 24시간 후 세안 및 화장품 사용 재개 |
| `/modality/11/subcategories/0/items/0/extracted/aftercare/1` | aftercare[1] | string | 자외선 차단제 필수 사용 (SPF 30 이상) |
| `/modality/11/subcategories/0/items/0/extracted/aftercare/2` | aftercare[2] | string | 시술 후 5일간 자극적인 성분 (레티놀, 비타민C, AHA/BHA) 피하기 |
| `/modality/11/subcategories/0/items/0/extracted/aftercare/3` | aftercare[3] | string | 심한 홍반이나 부종 시 냉찜질 |
| `/modality/11/subcategories/0/items/0/extracted/aftercare/4` | aftercare[4] | string | 회복 기간 중 과도한 운동 및 발한 피하기 |
| `/modality/11/subcategories/0/items/0/extracted/aftercare/5` | aftercare[5] | string | [시술 주기 참고] 피부 회복 후 재시술 (보통 4-6주). 과도한 채널 생성 시 장벽 손상 주의 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/11/subcategories/0/items/1` | items[1] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/11/subcategories/0/items/1/id` | id | string | auto-45-1774737181584 |
| `/modality/11/subcategories/0/items/1/name` | name | string | 더마스탬프 |
| `/modality/11/subcategories/0/items/1/detail` | detail | string | 스탬프형 |
| `/modality/11/subcategories/0/items/1/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/11/subcategories/0/items/1/extracted/overview` | overview | string | 스탐프형 마이크로니들로 정확한 압력으로 시술하는 기구 |
| `/modality/11/subcategories/0/items/1/extracted/mechanism` | mechanism | string | 손잡이에 달린 스탬프 헤드의 바늘 묶음이 수직으로 피부를 자극하여 일정한 깊이와 강도로 상처를 유도한다. 롤러보다 정밀한 시술이 가능하고 압력 조절로 시술 강도를 더 세밀하게 조정할 수 있다. |
| `/modality/11/subcategories/0/items/1/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/11/subcategories/0/items/1/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/11/subcategories/0/items/1/extracted/indications/primary/0` | primary[0] | string | 피부 탄력 개선 |
| `/modality/11/subcategories/0/items/1/extracted/indications/primary/1` | primary[1] | string | 흉터 개선 (위축성 흉터, 여드름 흉터) |
| `/modality/11/subcategories/0/items/1/extracted/indications/primary/2` | primary[2] | string | 피부 톤 균일화 |
| `/modality/11/subcategories/0/items/1/extracted/indications/primary/3` | primary[3] | string | 모공 축소 |
| `/modality/11/subcategories/0/items/1/extracted/indications/primary/4` | primary[4] | string | 피부 재생 |
| `/modality/11/subcategories/0/items/1/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/11/subcategories/0/items/1/extracted/safety/common` | common | array | [array, 원소 4] |
| `/modality/11/subcategories/0/items/1/extracted/safety/common/0` | common[0] | string | 시술 직후 홍반 |
| `/modality/11/subcategories/0/items/1/extracted/safety/common/1` | common[1] | string | 점상 출혈 |
| `/modality/11/subcategories/0/items/1/extracted/safety/common/2` | common[2] | string | 부종 |
| `/modality/11/subcategories/0/items/1/extracted/safety/common/3` | common[3] | string | 작열감 |
| `/modality/11/subcategories/0/items/1/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/11/subcategories/0/items/1/extracted/safety/serious/0` | serious[0] | string | 감염 위험 (부적절한 소독 시) |
| `/modality/11/subcategories/0/items/1/extracted/safety/serious/1` | serious[1] | string | 과도한 손상으로 인한 색소 변화 |
| `/modality/11/subcategories/0/items/1/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/11/subcategories/0/items/1/extracted/onset_duration/onset` | onset | string | 1~2주 후 콜라겐 합성 증가, 3~4주 후 개선 효과 확인 |
| `/modality/11/subcategories/0/items/1/extracted/onset_duration/duration` | duration | string | 한 번의 시술 효과는 3~4개월 지속, 월 1회 정기 시술 권장 |
| `/modality/11/subcategories/0/items/1/extracted/aftercare` | aftercare | array | [array, 원소 6] |
| `/modality/11/subcategories/0/items/1/extracted/aftercare/0` | aftercare[0] | string | 시술 12시간 동안 물로만 세안 |
| `/modality/11/subcategories/0/items/1/extracted/aftercare/1` | aftercare[1] | string | 고자극성 스킨케어 3~5일 자제 |
| `/modality/11/subcategories/0/items/1/extracted/aftercare/2` | aftercare[2] | string | 자외선 차단제 매일 사용 (SPF 50+) |
| `/modality/11/subcategories/0/items/1/extracted/aftercare/3` | aftercare[3] | string | 항생제 연고 도포 권장 (의료진 지시 시) |
| `/modality/11/subcategories/0/items/1/extracted/aftercare/4` | aftercare[4] | string | 시술 후 1주일간 사우나, 찜질방 자제 |
| `/modality/11/subcategories/0/items/1/extracted/aftercare/5` | aftercare[5] | string | [시술 주기 참고] 피부 회복 후 재시술 (보통 4-6주). 과도한 채널 생성 시 장벽 손상 주의 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/11/subcategories/0/items/2` | items[2] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/11/subcategories/0/items/2/id` | id | string | auto-M12-1775364775166 |
| `/modality/11/subcategories/0/items/2/name` | name | string | MTS롤러 |
| `/modality/11/subcategories/0/items/2/detail` | detail | string | 192핀수동 |
| `/modality/11/subcategories/0/items/2/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/11/subcategories/0/items/2/extracted/overview` | overview | string | 192개의 미세 바늘이 장착된 수동 마이크로니들링 롤러 |
| `/modality/11/subcategories/0/items/2/extracted/mechanism` | mechanism | string | 192개의 미세 바늘이 피부에 균일한 미세 손상을 만들어 자연 치유 과정을 활성화합니다. 콜라겐과 엘라스틴 생성을 촉진하여 피부 재생과 유효성분 흡수를 개선합니다. |
| `/modality/11/subcategories/0/items/2/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/11/subcategories/0/items/2/extracted/indications/primary` | primary | array | [array, 원소 2] |
| `/modality/11/subcategories/0/items/2/extracted/indications/primary/0` | primary[0] | string | 피부 재생 |
| `/modality/11/subcategories/0/items/2/extracted/indications/primary/1` | primary[1] | string | 제품 흡수율 향상 |
| `/modality/11/subcategories/0/items/2/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/11/subcategories/0/items/2/extracted/safety/common` | common | array | [array, 원소 1] |
| `/modality/11/subcategories/0/items/2/extracted/safety/common/0` | common[0] | string | 시술 후 미세한 점상출혈 |
| `/modality/11/subcategories/0/items/2/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/11/subcategories/0/items/2/extracted/onset_duration/onset` | onset | string | 1-2주 |
| `/modality/11/subcategories/0/items/2/extracted/onset_duration/duration` | duration | string | 2-4개월 |
| `/modality/11/subcategories/0/items/2/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/11/subcategories/0/items/2/extracted/aftercare/0` | aftercare[0] | string | 소독 관리 |
| `/modality/11/subcategories/0/items/2/extracted/aftercare/1` | aftercare[1] | string | 재생 세럼 사용 |
| `/modality/11/subcategories/0/items/2/extracted/aftercare/2` | aftercare[2] | string | [시술 주기 참고] 피부 회복 후 재시술 (보통 4-6주). 과도한 채널 생성 시 장벽 손상 주의 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/11/subcategories/1` | subcategories[1] | object | {object, 키 3: id, label, items} |
| `/modality/11/subcategories/1/id` | id | string | M12-2 |
| `/modality/11/subcategories/1/label` | label | string | 전동 MTS |
| `/modality/11/subcategories/1/items` | items | array | [array, 원소 4] |
| `/modality/11/subcategories/1/items/0` | items[0] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/11/subcategories/1/items/0/id` | id | string | M12-2-2 |
| `/modality/11/subcategories/1/items/0/name` | name | string | 펜타입 |
| `/modality/11/subcategories/1/items/0/detail` | detail | string | 전자동 |
| `/modality/11/subcategories/1/items/0/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/11/subcategories/1/items/0/extracted/overview` | overview | string | 전자동 펜형 기구로 정밀하고 깊이 조절이 가능한 시술 |
| `/modality/11/subcategories/1/items/0/extracted/mechanism` | mechanism | string | 전자동 펜 형태의 기구가 분당 1,200~2,000회 진동하며 미세한 바늘이 피부에 수직으로 펌핑 운동을 한다. 깊이(0.5~2.5mm) 조절이 정확하고 시술 속도가 빨라 균일한 자극을 제공하며, 동시에 유효 성분의 흡수를 극대화할 수 있다. |
| `/modality/11/subcategories/1/items/0/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/11/subcategories/1/items/0/extracted/indications/primary` | primary | array | [array, 원소 6] |
| `/modality/11/subcategories/1/items/0/extracted/indications/primary/0` | primary[0] | string | 피부 주름 개선 (특히 깊은 주름) |
| `/modality/11/subcategories/1/items/0/extracted/indications/primary/1` | primary[1] | string | 피부 탄력 강화 |
| `/modality/11/subcategories/1/items/0/extracted/indications/primary/2` | primary[2] | string | 흉터 개선 (위축성 흉터) |
| `/modality/11/subcategories/1/items/0/extracted/indications/primary/3` | primary[3] | string | 색소침착 개선 |
| `/modality/11/subcategories/1/items/0/extracted/indications/primary/4` | primary[4] | string | 피부 톤 및 결 개선 |
| `/modality/11/subcategories/1/items/0/extracted/indications/primary/5` | primary[5] | string | 약물 침투 증대 (비타민, 성장인자 등) |
| `/modality/11/subcategories/1/items/0/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/11/subcategories/1/items/0/extracted/safety/common` | common | array | [array, 원소 4] |
| `/modality/11/subcategories/1/items/0/extracted/safety/common/0` | common[0] | string | 시술 직후 홍반 (24~48시간) |
| `/modality/11/subcategories/1/items/0/extracted/safety/common/1` | common[1] | string | 점상 출혈 |
| `/modality/11/subcategories/1/items/0/extracted/safety/common/2` | common[2] | string | 부종 |
| `/modality/11/subcategories/1/items/0/extracted/safety/common/3` | common[3] | string | 따끔거림 |
| `/modality/11/subcategories/1/items/0/extracted/safety/serious` | serious | array | [array, 원소 3] |
| `/modality/11/subcategories/1/items/0/extracted/safety/serious/0` | serious[0] | string | 감염 (멸균 불충분 시) |
| `/modality/11/subcategories/1/items/0/extracted/safety/serious/1` | serious[1] | string | 과도한 깊이 설정 시 진피 손상 |
| `/modality/11/subcategories/1/items/0/extracted/safety/serious/2` | serious[2] | string | 색소 변화 (특히 어두운 피부) |
| `/modality/11/subcategories/1/items/0/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/11/subcategories/1/items/0/extracted/onset_duration/onset` | onset | string | 3~5일 후 초기 개선, 2~3주 후 명백한 효과 |
| `/modality/11/subcategories/1/items/0/extracted/onset_duration/duration` | duration | string | 단일 시술 효과 4~6개월, 4주 간격 월 1회 시술로 누적 효과 |
| `/modality/11/subcategories/1/items/0/extracted/aftercare` | aftercare | array | [array, 원소 8] |
| `/modality/11/subcategories/1/items/0/extracted/aftercare/0` | aftercare[0] | string | 시술 첫 24시간 얼굴 접촉 최소화 |
| `/modality/11/subcategories/1/items/0/extracted/aftercare/1` | aftercare[1] | string | 순한 클렌징 제품만 사용 (24시간 후) |
| `/modality/11/subcategories/1/items/0/extracted/aftercare/2` | aftercare[2] | string | 보습 집중 관리 (히알루론산, 세라마이드) |
| `/modality/11/subcategories/1/items/0/extracted/aftercare/3` | aftercare[3] | string | 자외선 차단제 매 2시간마다 재도포 |
| `/modality/11/subcategories/1/items/0/extracted/aftercare/4` | aftercare[4] | string | 시술 후 1주일간 화학 필링, 레이저 시술 자제 |
| `/modality/11/subcategories/1/items/0/extracted/aftercare/5` | aftercare[5] | string | 항염증제 복용 (의료진 지시 시) |
| `/modality/11/subcategories/1/items/0/extracted/aftercare/6` | aftercare[6] | string | 림프 배수 마사지로 부종 완화 |
| `/modality/11/subcategories/1/items/0/extracted/aftercare/7` | aftercare[7] | string | [시술 주기 참고] 피부 회복 후 재시술 (보통 4-6주). 과도한 채널 생성 시 장벽 손상 주의 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/11/subcategories/1/items/1` | items[1] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/11/subcategories/1/items/1/id` | id | string | auto-M12-1775363026852 |
| `/modality/11/subcategories/1/items/1/name` | name | string | 더마펜4 |
| `/modality/11/subcategories/1/items/1/detail` | detail | string | 더마펜월드 · 전동 마이크로니들 · 16핀 |
| `/modality/11/subcategories/1/items/1/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/11/subcategories/1/items/1/extracted/overview` | overview | string | 16개 초미세 바늘이 장착된 전동 마이크로니들링 장비로 피부 재생과 콜라겐 합성을 촉진하는 미용의학 시술 도구 |
| `/modality/11/subcategories/1/items/1/extracted/mechanism` | mechanism | string | 16개의 미세 바늘이 진피층에 미세한 상처를 생성하여 자연 치유 과정을 활성화시킵니다. 이 과정에서 콜라겐과 엘라스틴 합성이 증가하며 피부 재생과 재구조화가 진행됩니다. |
| `/modality/11/subcategories/1/items/1/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/11/subcategories/1/items/1/extracted/indications/primary` | primary | array | [array, 원소 2] |
| `/modality/11/subcategories/1/items/1/extracted/indications/primary/0` | primary[0] | string | 여드름 흉터 및 모공 개선 |
| `/modality/11/subcategories/1/items/1/extracted/indications/primary/1` | primary[1] | string | 피부 탄력 증진 및 주름 완화 |
| `/modality/11/subcategories/1/items/1/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/11/subcategories/1/items/1/extracted/safety/common` | common | array | [array, 원소 1] |
| `/modality/11/subcategories/1/items/1/extracted/safety/common/0` | common[0] | string | 시술 후 일시적 홍조 및 부종 |
| `/modality/11/subcategories/1/items/1/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/11/subcategories/1/items/1/extracted/onset_duration/onset` | onset | string | 4-6주 |
| `/modality/11/subcategories/1/items/1/extracted/onset_duration/duration` | duration | string | 6-12개월 |
| `/modality/11/subcategories/1/items/1/extracted/aftercare` | aftercare | array | [array, 원소 5] |
| `/modality/11/subcategories/1/items/1/extracted/aftercare/0` | aftercare[0] | string | 시술 후 24시간 동안 화장품 및 자외선 노출 자제 |
| `/modality/11/subcategories/1/items/1/extracted/aftercare/1` | aftercare[1] | string | 자외선 차단 (마이크로채널 → PIH 예방) |
| `/modality/11/subcategories/1/items/1/extracted/aftercare/2` | aftercare[2] | string | 당일 자극적 제품 자제 |
| `/modality/11/subcategories/1/items/1/extracted/aftercare/3` | aftercare[3] | string | 홍반은 1-2일 내 자연 소실 |
| `/modality/11/subcategories/1/items/1/extracted/aftercare/4` | aftercare[4] | string | [시술 주기 참고] 피부 회복 후 재시술 (보통 4-6주). 과도한 채널 생성 시 장벽 손상 주의 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/11/subcategories/1/items/2` | items[2] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/11/subcategories/1/items/2/id` | id | string | auto-M12-1775363035813 |
| `/modality/11/subcategories/1/items/2/name` | name | string | 스킨스탬프 |
| `/modality/11/subcategories/1/items/2/detail` | detail | string | 전동 스탬프형 MTS |
| `/modality/11/subcategories/1/items/2/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/11/subcategories/1/items/2/extracted/overview` | overview | string | 미세바늘을 이용해 피부에 미세한 천공을 만들어 콜라겐 생성을 촉진하는 피부 재생 시술 |
| `/modality/11/subcategories/1/items/2/extracted/mechanism` | mechanism | string | 미세바늘이 진피층까지 침투하여 인위적인 미세손상을 유발한다. 이 과정에서 상처 치유 반응이 활성화되어 콜라겐과 엘라스틴 합성이 증가하고 피부 재생이 촉진된다. |
| `/modality/11/subcategories/1/items/2/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/11/subcategories/1/items/2/extracted/indications/primary` | primary | array | [array, 원소 4] |
| `/modality/11/subcategories/1/items/2/extracted/indications/primary/0` | primary[0] | string | 여드름 흉터 개선 |
| `/modality/11/subcategories/1/items/2/extracted/indications/primary/1` | primary[1] | string | 모공 축소 |
| `/modality/11/subcategories/1/items/2/extracted/indications/primary/2` | primary[2] | string | 피부 탄력 개선 |
| `/modality/11/subcategories/1/items/2/extracted/indications/primary/3` | primary[3] | string | 잔주름 완화 |
| `/modality/11/subcategories/1/items/2/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/11/subcategories/1/items/2/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/11/subcategories/1/items/2/extracted/safety/common/0` | common[0] | string | 일시적 홍반과 부종 |
| `/modality/11/subcategories/1/items/2/extracted/safety/common/1` | common[1] | string | 따끔거림과 가벼운 출혈 |
| `/modality/11/subcategories/1/items/2/extracted/safety/common/2` | common[2] | string | 가피 형성 |
| `/modality/11/subcategories/1/items/2/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/11/subcategories/1/items/2/extracted/onset_duration/onset` | onset | string | 2-4주 |
| `/modality/11/subcategories/1/items/2/extracted/onset_duration/duration` | duration | string | 3-6개월 |
| `/modality/11/subcategories/1/items/2/extracted/aftercare` | aftercare | array | [array, 원소 5] |
| `/modality/11/subcategories/1/items/2/extracted/aftercare/0` | aftercare[0] | string | 시술 후 24-48시간 세안 자제 |
| `/modality/11/subcategories/1/items/2/extracted/aftercare/1` | aftercare[1] | string | 자외선 차단제 필수 사용 |
| `/modality/11/subcategories/1/items/2/extracted/aftercare/2` | aftercare[2] | string | 보습제 충분한 도포 |
| `/modality/11/subcategories/1/items/2/extracted/aftercare/3` | aftercare[3] | string | 알코올 성분 화장품 사용 자제 |
| `/modality/11/subcategories/1/items/2/extracted/aftercare/4` | aftercare[4] | string | [시술 주기 참고] 피부 회복 후 재시술 (보통 4-6주). 과도한 채널 생성 시 장벽 손상 주의 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/11/subcategories/1/items/3` | items[3] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/11/subcategories/1/items/3/id` | id | string | auto-M12-1775364775165 |
| `/modality/11/subcategories/1/items/3/name` | name | string | 에이팩 |
| `/modality/11/subcategories/1/items/3/detail` | detail | string | 진동형 |
| `/modality/11/subcategories/1/items/3/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/11/subcategories/1/items/3/extracted/overview` | overview | string | 진동 기술을 활용한 마이크로니들링 시스템으로 피부 재생을 촉진하는 시술 |
| `/modality/11/subcategories/1/items/3/extracted/mechanism` | mechanism | string | 미세한 바늘이 진동하며 피부에 미세 채널을 생성합니다. 이를 통해 콜라겐 생성이 촉진되고 유효성분의 침투가 향상됩니다. |
| `/modality/11/subcategories/1/items/3/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/11/subcategories/1/items/3/extracted/indications/primary` | primary | array | [array, 원소 4] |
| `/modality/11/subcategories/1/items/3/extracted/indications/primary/0` | primary[0] | string | 흉터 개선 |
| `/modality/11/subcategories/1/items/3/extracted/indications/primary/1` | primary[1] | string | 모공 축소 |
| `/modality/11/subcategories/1/items/3/extracted/indications/primary/2` | primary[2] | string | 피부 탄력 증진 |
| `/modality/11/subcategories/1/items/3/extracted/indications/primary/3` | primary[3] | string | 색소침착 개선 |
| `/modality/11/subcategories/1/items/3/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/11/subcategories/1/items/3/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/11/subcategories/1/items/3/extracted/safety/common/0` | common[0] | string | 일시적 홍조 |
| `/modality/11/subcategories/1/items/3/extracted/safety/common/1` | common[1] | string | 경미한 부종 |
| `/modality/11/subcategories/1/items/3/extracted/safety/common/2` | common[2] | string | 따끔거림 |
| `/modality/11/subcategories/1/items/3/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/11/subcategories/1/items/3/extracted/onset_duration/onset` | onset | string | 2-4주 |
| `/modality/11/subcategories/1/items/3/extracted/onset_duration/duration` | duration | string | 6-12개월 |
| `/modality/11/subcategories/1/items/3/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/11/subcategories/1/items/3/extracted/aftercare/0` | aftercare[0] | string | 자외선 차단 |
| `/modality/11/subcategories/1/items/3/extracted/aftercare/1` | aftercare[1] | string | 충분한 보습 |
| `/modality/11/subcategories/1/items/3/extracted/aftercare/2` | aftercare[2] | string | 음주 자제 48시간 |
| `/modality/11/subcategories/1/items/3/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 피부 회복 후 재시술 (보통 4-6주). 과도한 채널 생성 시 장벽 손상 주의 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/11/extracted` | extracted | object | {object, 키 8: overview, mechanism, indications, contraindications, safety, onset_duration, aftercare, related_techniques} |
| `/modality/11/extracted/overview` | overview | string | MTS는 아주 가느다란 바늘이 많이 달린 롤러나 스탬프로 피부에 미세한 구멍을 내서, 피부가 스스로 상처를 치유하는 과정에서 콜라겐(피부 탄력 단백질)이 새로 만들어지게 유도하는 시술이다. 바늘 구멍을 통해 비타민, 히알루론산 등 유효 성분의 흡수를 높이는 효과도 있다. |
| `/modality/11/extracted/mechanism` | mechanism | string | MTS 롤러의 미세한 바늘(0.2~2.0mm)이 피부 표피층과 진피층을 자극하면, 피부에 작은 상처가 생긴다. 이 상처를 회복하기 위해 PDGF, TGF-α/β 등 다양한 성장인자(세포 성장을 돕는 단백질)가 분비되고, 이들이 섬유모세포(콜라겐을 만드는 세포)를 활성화시킨다. 그 결과 새로운 콜라겐과 엘라스틴(피부 탄력 성분)이 만들어져 피부 탄력이 좋아지고, 각질층도 두꺼워진다. 흉터 부위에 시술하면 흉터의 콜라겐 밴드를 물리적으로 끊어줘서 흉터가 부드러워진다. |
| `/modality/11/extracted/indications` | indications | object | {object, 키 2: primary, extended} |
| `/modality/11/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/11/extracted/indications/primary/0` | primary[0] | string | 피부 노화 개선 (주름, 잔주름, 피부 탄력 저하) |
| `/modality/11/extracted/indications/primary/1` | primary[1] | string | 여드름흉터 |
| `/modality/11/extracted/indications/primary/2` | primary[2] | string | 피부결 개선 |
| `/modality/11/extracted/indications/extended` | extended | array | [array, 원소 5] |
| `/modality/11/extracted/indications/extended/0` | extended[0] | string | 색소침착 개선 (약물 투입과 병행 시) |
| `/modality/11/extracted/indications/extended/1` | extended[1] | string | 탈모 치료 (두피 MTS + PRP 또는 성장인자) |
| `/modality/11/extracted/indications/extended/2` | extended[2] | string | 넓은 모공 개선 |
| `/modality/11/extracted/indications/extended/3` | extended[3] | string | 각종 유효 성분(비타민, 플라센타, 히알루론산 등) 흡수 촉진 |
| `/modality/11/extracted/indications/extended/4` | extended[4] | string | 수술 후 흉터 개선 |
| `/modality/11/extracted/contraindications` | contraindications | object | {object, 키 2: absolute, relative} |
| `/modality/11/extracted/contraindications/absolute` | absolute | array | [array, 원소 4] |
| `/modality/11/extracted/contraindications/absolute/0` | absolute[0] | string | 피부에 감염성 질환이 있는 경우 |
| `/modality/11/extracted/contraindications/absolute/1` | absolute[1] | string | 심한 여드름이 진행 중인 경우 |
| `/modality/11/extracted/contraindications/absolute/2` | absolute[2] | string | 조절이 안 되는 당뇨병 |
| `/modality/11/extracted/contraindications/absolute/3` | absolute[3] | string | 켈로이드 체질 (흉터가 비정상적으로 부풀어오르는 체질) |
| `/modality/11/extracted/contraindications/relative` | relative | array | [array, 원소 2] |
| `/modality/11/extracted/contraindications/relative/0` | relative[0] | string | 출혈성 질환이 있거나 아스피린 등 혈액 응고에 영향을 주는 약을 복용 중인 경우 주의 |
| `/modality/11/extracted/contraindications/relative/1` | relative[1] | string | 혈액으로 인한 감염성 질환이 있는 경우 주의 |
| `/modality/11/extracted/safety` | safety | object | {object, 키 3: common, uncommon, serious} |
| `/modality/11/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/11/extracted/safety/common/0` | common[0] | string | 시술 중 약간의 출혈과 진물 |
| `/modality/11/extracted/safety/common/1` | common[1] | string | 시술 후 피부가 빨개지고 약간 부을 수 있음 (1~2일 내 호전) |
| `/modality/11/extracted/safety/common/2` | common[2] | string | 출혈에 의해 일시적으로 멍이 들 수 있음 |
| `/modality/11/extracted/safety/uncommon` | uncommon | array | [array, 원소 3] |
| `/modality/11/extracted/safety/uncommon/0` | uncommon[0] | string | 감염 (무균 관리가 안 될 경우) |
| `/modality/11/extracted/safety/uncommon/1` | uncommon[1] | string | 색소침착 (특히 진피까지 깊이 치료한 경우) |
| `/modality/11/extracted/safety/uncommon/2` | uncommon[2] | string | 알레르기성 접촉피부염 (도포 약물에 의한 반응) |
| `/modality/11/extracted/safety/serious` | serious | array | [array, 원소 1] |
| `/modality/11/extracted/safety/serious/0` | serious[0] | string | 쾨브너현상 (건선 등 피부질환이 있는 환자에서 시술 부위에 병변이 새로 생기는 현상) |
| `/modality/11/extracted/onset_duration` | onset_duration | object | {object, 키 3: onset, peak, duration} |
| `/modality/11/extracted/onset_duration/onset` | onset | string | 시술 후 1~2주부터 피부결 개선 느껴짐 |
| `/modality/11/extracted/onset_duration/peak` | peak | string | 3~6회 반복시술 후 최대 효과 (콜라겐 리모델링에 수주~수개월 소요) |
| `/modality/11/extracted/onset_duration/duration` | duration | string | 반복시술 시 피부가 점점 두꺼워지고 효과가 누적됨 |
| `/modality/11/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/11/extracted/aftercare/0` | aftercare[0] | string | 시술 후 보습제와 자외선차단제 꼭 사용하기 |
| `/modality/11/extracted/aftercare/1` | aftercare[1] | string | 가벼운 세안과 샤워는 괜찮지만, 탕목욕이나 사우나는 피하기 |
| `/modality/11/extracted/aftercare/2` | aftercare[2] | string | 출혈이 생긴 정도로 진피까지 치료한 경우 2~4일 화장 피하기 |
| `/modality/11/extracted/aftercare/3` | aftercare[3] | string | 롤러는 반드시 멸균 상태에서 1회용으로 사용할 것 |
| `/modality/11/extracted/related_techniques` | related_techniques | array | [array, 원소 3] |
| `/modality/11/extracted/related_techniques/0` | related_techniques[0] | string | MTS + PRP — 미세 구멍 후 PRP 도포로 피부 재생 효과 극대화 |
| `/modality/11/extracted/related_techniques/1` | related_techniques[1] | string | MTS + 약물 투입 — 비타민C, 히알루론산 등 유효 성분 경피 흡수 촉진 |
| `/modality/11/extracted/related_techniques/2` | related_techniques[2] | string | 프랙셔널 레이저 — 비슷한 원리(미세 열손상 → 재생)이지만 레이저 에너지 사용 |
| `/modality/11/products` | products | array | `[]` (빈 배열) |
| `/modality/11/name` | name | string | 마이크로니들링(MTS) |

## 잠정 관찰 (원문 아님 · 직접 읽기 기록)

| 상태 | 근거 Pointer | 관찰 |
|---|---|---|
| P | `/modality/11/subcategories/0/label`, `/modality/11/subcategories/1/label`, `/modality/11/products` | M12 하위분류는 구동 방식 축('수동 MTS','전동 MTS'). 항목은 기구 형태(더마롤러·더마스탬프·펜타입)와 제품명(더마펜4·에이팩·MTS롤러)이 섞인다. products 빈 배열. |
| I | `/modality/11/subcategories/0/items/1/extracted/overview` | '스탐프형' 오기(detail 은 '스탬프형'). 원문 보존. |
| P | `/modality/11/subcategories/0/items/0/extracted/aftercare/5` | M12 상용구 '[시술 주기 참고] 피부 회복 후 재시술 (보통 4-6주). 과도한 채널 생성 시 장벽 손상 주의 …'. 더마스탬프 duration '월 1회 정기 시술 권장' 과 병존. |
| P | `/modality/11/subcategories/0/items/2/extracted/indications/primary/1`, `/modality/11/subcategories/1/items/0/extracted/indications/primary/5` | 적응증에 '제품 흡수율 향상','약물 침투 증대' — 다른 시술·성분의 전달 수단으로서의 용도. |
| P | `/modality/11/extracted/safety/serious/0` | M12 serious '쾨브너현상 (건선 등 피부질환이 있는 환자에서 …)' — 기저질환 조건부 부작용. |
| P | `/modality/11/extracted/contraindications/absolute/2` | 절대금기 '조절이 안 되는 당뇨병' — M4 의 '당뇨병 환자'(무조건)와 조건 표현 다름. |

## 수동 복합 표현 (원문 구간)

| Pointer | 구간 | 원문 표현 | 관점 | 메모 |
|---|---|---|---|---|
| `/modality/11/subcategories/0/items/0/extracted/mechanism` | [9, 30] | 롤러형 기구의 바늘(0.2~2.0mm) | 수량·단위·시간, 범위 |  |
| `/modality/11/subcategories/0/items/0/extracted/safety/serious/0` | [0, 18] | 심한 감염 (무균 처리 미흡 시) | 수식, 조건 |  |
| `/modality/11/subcategories/0/items/0/extracted/safety/serious/1` | [0, 15] | 색소 이상 (색소침착/감소) | 기호 | 반대 방향 '/' |
| `/modality/11/subcategories/0/items/0/extracted/aftercare/2` | [0, 41] | 시술 후 5일간 자극적인 성분 (레티놀, 비타민C, AHA/BHA) 피하기 | 수량·단위·시간, 부정 |  |
| `/modality/11/subcategories/0/items/0/extracted/aftercare/5` | [34, 54] | 과도한 채널 생성 시 장벽 손상 주의 | 조건, 가능성·빈도 | 상용구 |
| `/modality/11/subcategories/0/items/1/extracted/aftercare/0` | [0, 17] | 시술 12시간 동안 물로만 세안 | 수량·단위·시간, 조건 | '만' 한정 |
| `/modality/11/subcategories/0/items/1/extracted/aftercare/3` | [0, 23] | 항생제 연고 도포 권장 (의료진 지시 시) | 조건 |  |
| `/modality/11/subcategories/0/items/2/detail` | [0, 6] | 192핀수동 | 수량·단위·시간 |  |
| `/modality/11/subcategories/1/items/0/extracted/mechanism` | [14, 32] | 분당 1,200~2,000회 진동 | 수량·단위·시간, 범위 |  |
| `/modality/11/subcategories/1/items/0/extracted/mechanism` | [63, 85] | 깊이(0.5~2.5mm) 조절이 정확하고 | 수량·단위·시간, 범위 |  |
| `/modality/11/subcategories/1/items/0/extracted/safety/serious/1` | [0, 17] | 과도한 깊이 설정 시 진피 손상 | 조건, 수식 |  |
| `/modality/11/subcategories/1/items/0/extracted/safety/serious/2` | [0, 17] | 색소 변화 (특히 어두운 피부) | 조건 |  |
| `/modality/11/subcategories/1/items/0/extracted/aftercare/3` | [0, 19] | 자외선 차단제 매 2시간마다 재도포 | 수량·단위·시간 | 빈도 |
| `/modality/11/subcategories/1/items/0/extracted/aftercare/4` | [0, 26] | 시술 후 1주일간 화학 필링, 레이저 시술 자제 | 수량·단위·시간, 부정, 참조 | 다른 시술과의 간격 |
| `/modality/11/subcategories/1/items/1/detail` | [0, 23] | 더마펜월드 · 전동 마이크로니들 · 16핀 | 수량·단위·시간 |  |
| `/modality/11/extracted/mechanism` | [76, 100] | PDGF, TGF-α/β 등 다양한 성장인자 | 기호 |  |
| `/modality/11/extracted/mechanism` | [215, 249] | 흉터 부위에 시술하면 흉터의 콜라겐 밴드를 물리적으로 끊어줘서 | 조건 |  |
| `/modality/11/extracted/indications/extended/1` | [0, 28] | 탈모 치료 (두피 MTS + PRP 또는 성장인자) | 부위, 기호, 참조 | '+' 병행, '또는' 대안 |
| `/modality/11/extracted/contraindications/relative/0` | [0, 47] | 출혈성 질환이 있거나 아스피린 등 혈액 응고에 영향을 주는 약을 복용 중인 경우 주의 | 조건 |  |
| `/modality/11/extracted/safety/uncommon/1` | [0, 24] | 색소침착 (특히 진피까지 깊이 치료한 경우) | 조건 |  |
| `/modality/11/extracted/onset_duration/peak` | [0, 39] | 3~6회 반복시술 후 최대 효과 (콜라겐 리모델링에 수주~수개월 소요) | 수량·단위·시간, 범위 |  |
| `/modality/11/extracted/aftercare/2` | [0, 34] | 출혈이 생긴 정도로 진피까지 치료한 경우 2~4일 화장 피하기 | 조건, 수량·단위·시간, 범위 |  |
| `/modality/11/extracted/aftercare/3` | [0, 27] | 롤러는 반드시 멸균 상태에서 1회용으로 사용할 것 | 조건, 수식 | 시술자 지시 |
| `/modality/11/extracted/related_techniques/1` | [0, 42] | MTS + 약물 투입 — 비타민C, 히알루론산 등 유효 성분 경피 흡수 촉진 | 기호, 참조 |  |

## 형태소 분석 확인 (알려진 오분절 K)

| 범위 | 표면형 | 문제 | 영향 |
|---|---|---|---|
| all | 더마롤러 | 더/MAG 마/MAG 롤러/NNG — 'derma' 의 '더' 를 비교 부사로 | 기구명 분해·부사 오탐(더마스탬프·더마펜4·더마브이도 같은 패턴) |
| all | 더마스탬프 | 더/MAG 마/NNG 스탬프/NNG | 기구명 분해 |
| all | 더마펜4 | 더/MAG 마/NNG 펜/NNG 4/SN | 제품명 분해 |

## 미결

| ID | 상태 | Pointer | 내용 | 영향·후속 |
|---|---|---|---|---|
| S035-I01 | I | `/modality/11/subcategories/0/items/1/extracted/overview` | '스탐프형' 오기. | 표기 보존 |

