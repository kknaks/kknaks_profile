# S032 — M10 HIFES/EMS

- 읽기 상태: **read** · 마지막 읽은 Pointer `/modality/9/name`
- 단위: id, category, category_en, group, subcategories 컨테이너, M10-1 items/0, M10-1 items/1, M10-2 items/0, M10-2 items/1, M10-2 items/2, M10-2 items/3, M10-2 items/4, M10-2 items/5, M10-2 items/6, M10-2 items/7, extracted, products 컨테이너, name
- 상위 문맥(공동 참조·소유 아님): 없음
- 기계 기록: `source-map.json`(section=S032) · `morphology/S032.json` · `expressions.json`(section=S032) · 읽기 렌더 `reading/S032.txt`

## 원문 값 (원본 컬럼명 그대로, 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/modality/9` | modality[9] | object | {object, 키 8: id, category, category_en, group, subcategories, extracted, products, name} |
| `/modality/9/id` | id | string | M10 |
| `/modality/9/category` | category | string | HIFES/EMS |
| `/modality/9/category_en` | category_en | string | HIFES/EMS |
| `/modality/9/group` | group | string | 시술/기기 |
| `/modality/9/subcategories` | subcategories | array | [array, 원소 2] |
| `/modality/9/subcategories/0` | subcategories[0] | object | {object, 키 3: id, label, items} |
| `/modality/9/subcategories/0/id` | id | string | M10-1 |
| `/modality/9/subcategories/0/label` | label | string | 페이셜 EMS |
| `/modality/9/subcategories/0/items` | items | array | [array, 원소 2] |
| `/modality/9/subcategories/0/items/0` | items[0] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/9/subcategories/0/items/0/id` | id | string | M10-1-1 |
| `/modality/9/subcategories/0/items/0/name` | name | string | 엠페이스(EMFACE) |
| `/modality/9/subcategories/0/items/0/detail` | detail | string | BTL · RF+HIFES · 근육+피부 동시 |
| `/modality/9/subcategories/0/items/0/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/9/subcategories/0/items/0/extracted/overview` | overview | string | RF와 HIFES를 결합한 얼굴 근육강화 및 피부 재생 시술 |
| `/modality/9/subcategories/0/items/0/extracted/mechanism` | mechanism | string | 방사주파(RF) 에너지가 진피층의 콜라겐을 가열하여 재생을 유도하면서, 동시에 HIFES가 얼굴 표정근을 강화하여 피부 탄력 개선과 근육량 증대를 동시에 달성한다. 이는 피부 표면의 리프팅 효과와 깊은 층의 근육 강화를 통합적으로 제공한다. |
| `/modality/9/subcategories/0/items/0/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/9/subcategories/0/items/0/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/9/subcategories/0/items/0/extracted/indications/primary/0` | primary[0] | string | 얼굴 처짐 개선 |
| `/modality/9/subcategories/0/items/0/extracted/indications/primary/1` | primary[1] | string | 표정근 강화 |
| `/modality/9/subcategories/0/items/0/extracted/indications/primary/2` | primary[2] | string | 피부 탄력도 증가 |
| `/modality/9/subcategories/0/items/0/extracted/indications/primary/3` | primary[3] | string | 주름 개선 |
| `/modality/9/subcategories/0/items/0/extracted/indications/primary/4` | primary[4] | string | 얼굴 윤곽 개선 |
| `/modality/9/subcategories/0/items/0/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/9/subcategories/0/items/0/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/9/subcategories/0/items/0/extracted/safety/common/0` | common[0] | string | 시술 후 일시적 홍반 |
| `/modality/9/subcategories/0/items/0/extracted/safety/common/1` | common[1] | string | 근육통 유사 감각 |
| `/modality/9/subcategories/0/items/0/extracted/safety/common/2` | common[2] | string | 가벼운 부종 |
| `/modality/9/subcategories/0/items/0/extracted/safety/serious` | serious | array | [array, 원소 1] |
| `/modality/9/subcategories/0/items/0/extracted/safety/serious/0` | serious[0] | string | 금속 임플란트 부위의 화상 위험 (사전 확인 필수) |
| `/modality/9/subcategories/0/items/0/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/9/subcategories/0/items/0/extracted/onset_duration/onset` | onset | string | 1-2주 후부터 단계적 개선, 4주 후 명확한 효과 |
| `/modality/9/subcategories/0/items/0/extracted/onset_duration/duration` | duration | string | 3-6개월 유지, 정기적 시술로 지속 효과 |
| `/modality/9/subcategories/0/items/0/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/9/subcategories/0/items/0/extracted/aftercare/0` | aftercare[0] | string | 시술 24시간 후 스킨케어 재개 |
| `/modality/9/subcategories/0/items/0/extracted/aftercare/1` | aftercare[1] | string | 고강도 운동 48시간 자제 |
| `/modality/9/subcategories/0/items/0/extracted/aftercare/2` | aftercare[2] | string | 충분한 수분 섭취 |
| `/modality/9/subcategories/0/items/0/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 3개월 간격 권장. 근육 적응 및 지방 대사 완료 후 재시술 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/9/subcategories/0/items/1` | items[1] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/9/subcategories/0/items/1/id` | id | string | auto-M10-1775364775186 |
| `/modality/9/subcategories/0/items/1/name` | name | string | 엠페이스 |
| `/modality/9/subcategories/0/items/1/detail` | detail | string | BTL안면HIFES |
| `/modality/9/subcategories/0/items/1/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/9/subcategories/0/items/1/extracted/overview` | overview | string | BTL사의 안면 전용 HIFES 근육 강화 장비 |
| `/modality/9/subcategories/0/items/1/extracted/mechanism` | mechanism | string | 고강도 집속 전자기장(HIFES)이 안면 근육에 강력한 수축을 유발합니다. 근육 강화를 통해 자연스러운 리프팅과 윤곽 개선을 달성합니다. |
| `/modality/9/subcategories/0/items/1/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/9/subcategories/0/items/1/extracted/indications/primary` | primary | array | [array, 원소 2] |
| `/modality/9/subcategories/0/items/1/extracted/indications/primary/0` | primary[0] | string | 안면 근육 강화 |
| `/modality/9/subcategories/0/items/1/extracted/indications/primary/1` | primary[1] | string | 자연스러운 리프팅 |
| `/modality/9/subcategories/0/items/1/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/9/subcategories/0/items/1/extracted/safety/common` | common | array | [array, 원소 1] |
| `/modality/9/subcategories/0/items/1/extracted/safety/common/0` | common[0] | string | 시술 후 근육 피로감 |
| `/modality/9/subcategories/0/items/1/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/9/subcategories/0/items/1/extracted/onset_duration/onset` | onset | string | 2-4주 |
| `/modality/9/subcategories/0/items/1/extracted/onset_duration/duration` | duration | string | 6-9개월 |
| `/modality/9/subcategories/0/items/1/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/9/subcategories/0/items/1/extracted/aftercare/0` | aftercare[0] | string | 충분한 휴식 |
| `/modality/9/subcategories/0/items/1/extracted/aftercare/1` | aftercare[1] | string | 근육 마사지 |
| `/modality/9/subcategories/0/items/1/extracted/aftercare/2` | aftercare[2] | string | [시술 주기 참고] 3개월 간격 권장. 근육 적응 및 지방 대사 완료 후 재시술 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/9/subcategories/1` | subcategories[1] | object | {object, 키 3: id, label, items} |
| `/modality/9/subcategories/1/id` | id | string | M10-2 |
| `/modality/9/subcategories/1/label` | label | string | 바디 EMS |
| `/modality/9/subcategories/1/items` | items | array | [array, 원소 8] |
| `/modality/9/subcategories/1/items/0` | items[0] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/9/subcategories/1/items/0/id` | id | string | M10-2-1 |
| `/modality/9/subcategories/1/items/0/name` | name | string | 엠스컬프트 |
| `/modality/9/subcategories/1/items/0/detail` | detail | string | BTL · HIFEM · 근육수축+지방감소 |
| `/modality/9/subcategories/1/items/0/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/9/subcategories/1/items/0/extracted/overview` | overview | string | HIFEM 기술로 근육 강화와 지방 감소를 동시 달성 |
| `/modality/9/subcategories/1/items/0/extracted/mechanism` | mechanism | string | 고강도 집속 전자기장(HIFEM)이 운동신경을 자극하여 근육의 초극대 수축(supramaximal contraction)을 유발한다. 30분 시술로 수만 회의 강력한 근육 수축을 통해 근비대와 신규 근섬유 생성을 유도하며, 근육 수축의 대사 산물이 인접 지방세포의 자연사(apoptosis)를 유발하여 지방 감소를 동시에 달성한다. |
| `/modality/9/subcategories/1/items/0/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/9/subcategories/1/items/0/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/9/subcategories/1/items/0/extracted/indications/primary/0` | primary[0] | string | 복부 근육 강화 및 복부 지방 감소 |
| `/modality/9/subcategories/1/items/0/extracted/indications/primary/1` | primary[1] | string | 엉덩이 리프팅 (힙업) |
| `/modality/9/subcategories/1/items/0/extracted/indications/primary/2` | primary[2] | string | 팔뚝 근육 강화 |
| `/modality/9/subcategories/1/items/0/extracted/indications/primary/3` | primary[3] | string | 허벅지 근육 강화 및 지방 감소 |
| `/modality/9/subcategories/1/items/0/extracted/indications/primary/4` | primary[4] | string | 종아리 근육 강화 |
| `/modality/9/subcategories/1/items/0/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/9/subcategories/1/items/0/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/9/subcategories/1/items/0/extracted/safety/common/0` | common[0] | string | 시술 중 강한 근육 수축감 |
| `/modality/9/subcategories/1/items/0/extracted/safety/common/1` | common[1] | string | 시술 후 근육통 (48-72시간) |
| `/modality/9/subcategories/1/items/0/extracted/safety/common/2` | common[2] | string | 가벼운 부종 |
| `/modality/9/subcategories/1/items/0/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/9/subcategories/1/items/0/extracted/safety/serious/0` | serious[0] | string | 심박동기, 금속 임플란트 보유자 금기 |
| `/modality/9/subcategories/1/items/0/extracted/safety/serious/1` | serious[1] | string | 임신 중 금지 |
| `/modality/9/subcategories/1/items/0/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/9/subcategories/1/items/0/extracted/onset_duration/onset` | onset | string | 2주 후부터 근육 증가 감지, 4주 후 지각 가능한 변화 |
| `/modality/9/subcategories/1/items/0/extracted/onset_duration/duration` | duration | string | 3-6개월 효과 유지, 월 1-2회 시술로 지속 |
| `/modality/9/subcategories/1/items/0/extracted/aftercare` | aftercare | array | [array, 원소 5] |
| `/modality/9/subcategories/1/items/0/extracted/aftercare/0` | aftercare[0] | string | 시술 후 충분한 수분 섭취 |
| `/modality/9/subcategories/1/items/0/extracted/aftercare/1` | aftercare[1] | string | 24시간 내 격한 운동 자제 |
| `/modality/9/subcategories/1/items/0/extracted/aftercare/2` | aftercare[2] | string | 근육통 완화를 위해 가벼운 스트레칭 권고 |
| `/modality/9/subcategories/1/items/0/extracted/aftercare/3` | aftercare[3] | string | 최소 48시간 후 정상 운동 재개 |
| `/modality/9/subcategories/1/items/0/extracted/aftercare/4` | aftercare[4] | string | [시술 주기 참고] 3개월 간격 권장. 근육 적응 및 지방 대사 완료 후 재시술 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/9/subcategories/1/items/1` | items[1] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/9/subcategories/1/items/1/id` | id | string | M10-2-2 |
| `/modality/9/subcategories/1/items/1/name` | name | string | 엠스컬프트네오 |
| `/modality/9/subcategories/1/items/1/detail` | detail | string | BTL · HIFEM+RF 동시 |
| `/modality/9/subcategories/1/items/1/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/9/subcategories/1/items/1/extracted/overview` | overview | string | HIFEM+RF 결합으로 근육 강화와 피부 개선 동시 달성 |
| `/modality/9/subcategories/1/items/1/extracted/mechanism` | mechanism | string | HIFEM이 근육의 초극대 수축을 유발하여 근비대와 지방 감소를 달성하면서, 동시에 적용된 RF(방사주파) 에너지가 진피층의 콜라겐을 열변성시켜 즉각적인 피부 수축과 장기적 콜라겐 재생을 유도한다. 이를 통해 근육 강화, 지방 감소, 피부 탄력 개선을 통합적으로 제공한다. |
| `/modality/9/subcategories/1/items/1/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/9/subcategories/1/items/1/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/9/subcategories/1/items/1/extracted/indications/primary/0` | primary[0] | string | 복부 근육 강화, 지방 감소, 피부 탄력도 개선 |
| `/modality/9/subcategories/1/items/1/extracted/indications/primary/1` | primary[1] | string | 엉덩이 리프팅 및 피부 개선 |
| `/modality/9/subcategories/1/items/1/extracted/indications/primary/2` | primary[2] | string | 팔뚝 근육강화 및 처짐 개선 |
| `/modality/9/subcategories/1/items/1/extracted/indications/primary/3` | primary[3] | string | 허벅지 근육강화 및 피부 탄력도 증가 |
| `/modality/9/subcategories/1/items/1/extracted/indications/primary/4` | primary[4] | string | 피부 질감 개선 |
| `/modality/9/subcategories/1/items/1/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/9/subcategories/1/items/1/extracted/safety/common` | common | array | [array, 원소 4] |
| `/modality/9/subcategories/1/items/1/extracted/safety/common/0` | common[0] | string | 강한 근육 수축감 |
| `/modality/9/subcategories/1/items/1/extracted/safety/common/1` | common[1] | string | 시술 후 근육통 (48-72시간) |
| `/modality/9/subcategories/1/items/1/extracted/safety/common/2` | common[2] | string | 일시적 홍반 |
| `/modality/9/subcategories/1/items/1/extracted/safety/common/3` | common[3] | string | 경미한 부종 |
| `/modality/9/subcategories/1/items/1/extracted/safety/serious` | serious | array | [array, 원소 3] |
| `/modality/9/subcategories/1/items/1/extracted/safety/serious/0` | serious[0] | string | 심박동기, 금속 임플란트 보유자 금기 |
| `/modality/9/subcategories/1/items/1/extracted/safety/serious/1` | serious[1] | string | 임신 중 금지 |
| `/modality/9/subcategories/1/items/1/extracted/safety/serious/2` | serious[2] | string | 활성 피부 감염 부위 시술 금지 |
| `/modality/9/subcategories/1/items/1/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/9/subcategories/1/items/1/extracted/onset_duration/onset` | onset | string | 즉각적인 피부 수축감, 2주 후 근육 증가 감지, 4-6주 후 현저한 변화 |
| `/modality/9/subcategories/1/items/1/extracted/onset_duration/duration` | duration | string | 3-6개월 효과 유지, 월 1-2회 정기 시술로 지속 |
| `/modality/9/subcategories/1/items/1/extracted/aftercare` | aftercare | array | [array, 원소 5] |
| `/modality/9/subcategories/1/items/1/extracted/aftercare/0` | aftercare[0] | string | 시술 후 24시간 집중 보습 및 진정 팩 권고 |
| `/modality/9/subcategories/1/items/1/extracted/aftercare/1` | aftercare[1] | string | 48시간 내 격한 운동 자제 |
| `/modality/9/subcategories/1/items/1/extracted/aftercare/2` | aftercare[2] | string | 충분한 수분 섭취 |
| `/modality/9/subcategories/1/items/1/extracted/aftercare/3` | aftercare[3] | string | 최소 48시간 후 일반 운동 재개 |
| `/modality/9/subcategories/1/items/1/extracted/aftercare/4` | aftercare[4] | string | [시술 주기 참고] 3개월 간격 권장. 근육 적응 및 지방 대사 완료 후 재시술 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/9/subcategories/1/items/2` | items[2] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/9/subcategories/1/items/2/id` | id | string | auto-M10-1775361916636 |
| `/modality/9/subcategories/1/items/2/name` | name | string | 바넥스프로 |
| `/modality/9/subcategories/1/items/2/detail` | detail | string | RF+EMS+석션 · 바디 컨투어링 |
| `/modality/9/subcategories/1/items/2/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/9/subcategories/1/items/2/extracted/overview` | overview | string | RF 고주파, EMS 근육자극, 석션 기술을 결합한 비침습적 바디 컨투어링 장비 |
| `/modality/9/subcategories/1/items/2/extracted/mechanism` | mechanism | string | RF 고주파 에너지로 진피층 가열하여 콜라겐 재생성과 지방세포 파괴를 유도합니다. EMS 전기자극으로 근육수축을 증가시키고 석션으로 혈액순환을 개선하여 바디라인 개선 효과를 제공합니다. |
| `/modality/9/subcategories/1/items/2/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/9/subcategories/1/items/2/extracted/indications/primary` | primary | array | [array, 원소 4] |
| `/modality/9/subcategories/1/items/2/extracted/indications/primary/0` | primary[0] | string | 국소 지방 감소 |
| `/modality/9/subcategories/1/items/2/extracted/indications/primary/1` | primary[1] | string | 바디라인 개선 |
| `/modality/9/subcategories/1/items/2/extracted/indications/primary/2` | primary[2] | string | 셀룰라이트 개선 |
| `/modality/9/subcategories/1/items/2/extracted/indications/primary/3` | primary[3] | string | 근육 토닝 |
| `/modality/9/subcategories/1/items/2/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/9/subcategories/1/items/2/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/9/subcategories/1/items/2/extracted/safety/common/0` | common[0] | string | 시술 부위 일시적 홍조 |
| `/modality/9/subcategories/1/items/2/extracted/safety/common/1` | common[1] | string | 가벼운 부종 |
| `/modality/9/subcategories/1/items/2/extracted/safety/common/2` | common[2] | string | 근육 피로감 |
| `/modality/9/subcategories/1/items/2/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/9/subcategories/1/items/2/extracted/onset_duration/onset` | onset | string | 2-4주 |
| `/modality/9/subcategories/1/items/2/extracted/onset_duration/duration` | duration | string | 6-12개월 |
| `/modality/9/subcategories/1/items/2/extracted/aftercare` | aftercare | array | [array, 원소 5] |
| `/modality/9/subcategories/1/items/2/extracted/aftercare/0` | aftercare[0] | string | 충분한 수분 섭취 |
| `/modality/9/subcategories/1/items/2/extracted/aftercare/1` | aftercare[1] | string | 가벼운 마사지 |
| `/modality/9/subcategories/1/items/2/extracted/aftercare/2` | aftercare[2] | string | 규칙적인 운동 병행 |
| `/modality/9/subcategories/1/items/2/extracted/aftercare/3` | aftercare[3] | string | 음주 자제 24시간 |
| `/modality/9/subcategories/1/items/2/extracted/aftercare/4` | aftercare[4] | string | [시술 주기 참고] 3개월 간격 권장. 근육 적응 및 지방 대사 완료 후 재시술 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/9/subcategories/1/items/3` | items[3] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/9/subcategories/1/items/3/id` | id | string | auto-M10-1775363005172 |
| `/modality/9/subcategories/1/items/3/name` | name | string | 이볼브 |
| `/modality/9/subcategories/1/items/3/detail` | detail | string | 인모드 · RF+EMS 바디 근육+피부 |
| `/modality/9/subcategories/1/items/3/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/9/subcategories/1/items/3/extracted/overview` | overview | string | 인모드 기반 RF와 EMS를 결합한 바디 컨투어링 및 근육 강화 복합 시술 |
| `/modality/9/subcategories/1/items/3/extracted/mechanism` | mechanism | string | RF 에너지가 피하지방층과 진피층을 가열하여 콜라겐 재생성과 지방세포 파괴를 유도합니다. EMS 전기자극이 근육 수축을 강제로 유발하여 근육량 증가와 기초대사율 향상을 동시에 달성합니다. |
| `/modality/9/subcategories/1/items/3/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/9/subcategories/1/items/3/extracted/indications/primary` | primary | array | [array, 원소 2] |
| `/modality/9/subcategories/1/items/3/extracted/indications/primary/0` | primary[0] | string | 복부, 팔, 허벅지 등 바디 컨투어링 |
| `/modality/9/subcategories/1/items/3/extracted/indications/primary/1` | primary[1] | string | 근육 톤업 및 체형 개선 |
| `/modality/9/subcategories/1/items/3/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/9/subcategories/1/items/3/extracted/safety/common` | common | array | [array, 원소 1] |
| `/modality/9/subcategories/1/items/3/extracted/safety/common/0` | common[0] | string | 시술 부위 일시적 발적과 부종 |
| `/modality/9/subcategories/1/items/3/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/9/subcategories/1/items/3/extracted/onset_duration/onset` | onset | string | 2-4주 |
| `/modality/9/subcategories/1/items/3/extracted/onset_duration/duration` | duration | string | 6-12개월 |
| `/modality/9/subcategories/1/items/3/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/9/subcategories/1/items/3/extracted/aftercare/0` | aftercare[0] | string | 충분한 수분 섭취 및 가벼운 운동 권장 |
| `/modality/9/subcategories/1/items/3/extracted/aftercare/1` | aftercare[1] | string | 시술 후 근육통은 정상 반응 (1-3일) |
| `/modality/9/subcategories/1/items/3/extracted/aftercare/2` | aftercare[2] | string | 충분한 수분 섭취 권장 |
| `/modality/9/subcategories/1/items/3/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 3개월 간격 권장. 근육 적응 및 지방 대사 완료 후 재시술 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/9/subcategories/1/items/4` | items[4] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/9/subcategories/1/items/4/id` | id | string | auto-M10-1775363013079 |
| `/modality/9/subcategories/1/items/4/name` | name | string | 트루스컬프트 |
| `/modality/9/subcategories/1/items/4/detail` | detail | string | 큐테라 · RF 바디 지방감소 |
| `/modality/9/subcategories/1/items/4/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/9/subcategories/1/items/4/extracted/overview` | overview | string | 큐테라사의 RF(고주파) 기술을 이용한 비침습적 바디 컨투어링 및 지방감소 시술 |
| `/modality/9/subcategories/1/items/4/extracted/mechanism` | mechanism | string | 1.8MHz RF 에너지가 피하지방층 깊숙이 침투하여 지방세포의 온도를 45-50도까지 상승시킵니다. 열손상을 받은 지방세포는 자연적으로 파괴되어 림프계를 통해 체외로 배출됩니다. |
| `/modality/9/subcategories/1/items/4/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/9/subcategories/1/items/4/extracted/indications/primary` | primary | array | [array, 원소 2] |
| `/modality/9/subcategories/1/items/4/extracted/indications/primary/0` | primary[0] | string | 복부, 허벅지, 팔뚝 등 국소 지방 감소 |
| `/modality/9/subcategories/1/items/4/extracted/indications/primary/1` | primary[1] | string | 바디 윤곽 개선 및 타이트닝 |
| `/modality/9/subcategories/1/items/4/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/9/subcategories/1/items/4/extracted/safety/common` | common | array | [array, 원소 1] |
| `/modality/9/subcategories/1/items/4/extracted/safety/common/0` | common[0] | string | 시술 부위 일시적 발적 및 부종 |
| `/modality/9/subcategories/1/items/4/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/9/subcategories/1/items/4/extracted/onset_duration/onset` | onset | string | 4-6주 |
| `/modality/9/subcategories/1/items/4/extracted/onset_duration/duration` | duration | string | 6-12개월 |
| `/modality/9/subcategories/1/items/4/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/9/subcategories/1/items/4/extracted/aftercare/0` | aftercare[0] | string | 시술 후 충분한 수분 섭취로 지방세포 배출 촉진 |
| `/modality/9/subcategories/1/items/4/extracted/aftercare/1` | aftercare[1] | string | 시술 후 근육통은 정상 반응 (1-3일) |
| `/modality/9/subcategories/1/items/4/extracted/aftercare/2` | aftercare[2] | string | 충분한 수분 섭취 권장 |
| `/modality/9/subcategories/1/items/4/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 3개월 간격 권장. 근육 적응 및 지방 대사 완료 후 재시술 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/9/subcategories/1/items/5` | items[5] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/9/subcategories/1/items/5/id` | id | string | auto-M10-1775363019549 |
| `/modality/9/subcategories/1/items/5/name` | name | string | 쿨톤 |
| `/modality/9/subcategories/1/items/5/detail` | detail | string | 앨러간 · 쿨스컬프팅+EMS 근육 |
| `/modality/9/subcategories/1/items/5/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/9/subcategories/1/items/5/extracted/overview` | overview | string | 앨러간의 크라이오리폴리시스와 EMS 근육자극을 결합한 체형관리 시술 |
| `/modality/9/subcategories/1/items/5/extracted/mechanism` | mechanism | string | 크라이오리폴리시스를 통해 지방세포를 선택적으로 냉동시켜 자연사멸을 유도합니다. 동시에 EMS로 근육수축을 자극하여 근육량 증가와 지방분해를 촉진합니다. |
| `/modality/9/subcategories/1/items/5/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/9/subcategories/1/items/5/extracted/indications/primary` | primary | array | [array, 원소 2] |
| `/modality/9/subcategories/1/items/5/extracted/indications/primary/0` | primary[0] | string | 국소 지방감소 |
| `/modality/9/subcategories/1/items/5/extracted/indications/primary/1` | primary[1] | string | 근육량 증가 및 체형교정 |
| `/modality/9/subcategories/1/items/5/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/9/subcategories/1/items/5/extracted/safety/common` | common | array | [array, 원소 1] |
| `/modality/9/subcategories/1/items/5/extracted/safety/common/0` | common[0] | string | 시술부위 일시적 부종 및 멍 |
| `/modality/9/subcategories/1/items/5/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/9/subcategories/1/items/5/extracted/onset_duration/onset` | onset | string | 2-4주 |
| `/modality/9/subcategories/1/items/5/extracted/onset_duration/duration` | duration | string | 6개월-1년 |
| `/modality/9/subcategories/1/items/5/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/9/subcategories/1/items/5/extracted/aftercare/0` | aftercare[0] | string | 시술 후 마사지 권장 |
| `/modality/9/subcategories/1/items/5/extracted/aftercare/1` | aftercare[1] | string | 충분한 수분섭취 |
| `/modality/9/subcategories/1/items/5/extracted/aftercare/2` | aftercare[2] | string | 규칙적인 운동 병행 |
| `/modality/9/subcategories/1/items/5/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 3개월 간격 권장. 근육 적응 및 지방 대사 완료 후 재시술 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/9/subcategories/1/items/6` | items[6] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/9/subcategories/1/items/6/id` | id | string | auto-M10-1775364775185 |
| `/modality/9/subcategories/1/items/6/name` | name | string | 스팀슈어 |
| `/modality/9/subcategories/1/items/6/detail` | detail | string | RF+EMS |
| `/modality/9/subcategories/1/items/6/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/9/subcategories/1/items/6/extracted/overview` | overview | string | RF와 EMS를 결합한 피부 탄력 및 근육 강화 복합 치료 |
| `/modality/9/subcategories/1/items/6/extracted/mechanism` | mechanism | string | 고주파(RF)로 피부 깊숙한 콜라겐 생성을 촉진하고 EMS로 근육을 강화합니다. 피부와 근육을 동시에 개선하여 종합적인 리프팅 효과를 제공합니다. |
| `/modality/9/subcategories/1/items/6/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/9/subcategories/1/items/6/extracted/indications/primary` | primary | array | [array, 원소 2] |
| `/modality/9/subcategories/1/items/6/extracted/indications/primary/0` | primary[0] | string | 피부 탄력 개선 |
| `/modality/9/subcategories/1/items/6/extracted/indications/primary/1` | primary[1] | string | 근육 토닝 |
| `/modality/9/subcategories/1/items/6/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/9/subcategories/1/items/6/extracted/safety/common` | common | array | [array, 원소 1] |
| `/modality/9/subcategories/1/items/6/extracted/safety/common/0` | common[0] | string | 시술 부위 일시적 발적 |
| `/modality/9/subcategories/1/items/6/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/9/subcategories/1/items/6/extracted/onset_duration/onset` | onset | string | 2-3주 |
| `/modality/9/subcategories/1/items/6/extracted/onset_duration/duration` | duration | string | 4-8개월 |
| `/modality/9/subcategories/1/items/6/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/9/subcategories/1/items/6/extracted/aftercare/0` | aftercare[0] | string | 보습 관리 |
| `/modality/9/subcategories/1/items/6/extracted/aftercare/1` | aftercare[1] | string | 가벼운 운동 |
| `/modality/9/subcategories/1/items/6/extracted/aftercare/2` | aftercare[2] | string | [시술 주기 참고] 3개월 간격 권장. 근육 적응 및 지방 대사 완료 후 재시술 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/9/subcategories/1/items/7` | items[7] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/9/subcategories/1/items/7/id` | id | string | auto-M10-1775364775187 |
| `/modality/9/subcategories/1/items/7/name` | name | string | 엠스컬프트NEO |
| `/modality/9/subcategories/1/items/7/detail` | detail | string | HIFEM+RF |
| `/modality/9/subcategories/1/items/7/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/9/subcategories/1/items/7/extracted/overview` | overview | string | HIFEM과 RF를 동시 적용하는 혁신적인 바디컨투어링 장비 |
| `/modality/9/subcategories/1/items/7/extracted/mechanism` | mechanism | string | 고강도 집속 전자기장(HIFEM)으로 근육을 강화하고 RF로 지방을 감소시킵니다. 근육 증가와 지방 감소를 동시에 달성하여 이상적인 바디라인을 조성합니다. |
| `/modality/9/subcategories/1/items/7/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/9/subcategories/1/items/7/extracted/indications/primary` | primary | array | [array, 원소 2] |
| `/modality/9/subcategories/1/items/7/extracted/indications/primary/0` | primary[0] | string | 근육량 증가 |
| `/modality/9/subcategories/1/items/7/extracted/indications/primary/1` | primary[1] | string | 지방 감소 |
| `/modality/9/subcategories/1/items/7/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/9/subcategories/1/items/7/extracted/safety/common` | common | array | [array, 원소 1] |
| `/modality/9/subcategories/1/items/7/extracted/safety/common/0` | common[0] | string | 시술 후 근육통 |
| `/modality/9/subcategories/1/items/7/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/9/subcategories/1/items/7/extracted/onset_duration/onset` | onset | string | 2-4주 |
| `/modality/9/subcategories/1/items/7/extracted/onset_duration/duration` | duration | string | 6-12개월 |
| `/modality/9/subcategories/1/items/7/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/9/subcategories/1/items/7/extracted/aftercare/0` | aftercare[0] | string | 충분한 수분 섭취 |
| `/modality/9/subcategories/1/items/7/extracted/aftercare/1` | aftercare[1] | string | 근육 회복 관리 |
| `/modality/9/subcategories/1/items/7/extracted/aftercare/2` | aftercare[2] | string | [시술 주기 참고] 3개월 간격 권장. 근육 적응 및 지방 대사 완료 후 재시술 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/9/extracted` | extracted | object | {object, 키 8: overview, mechanism, indications, contraindications, safety, onset_duration, aftercare, related_techniques} |
| `/modality/9/extracted/overview` | overview | string | HIFES(고강도 집속 전자기 자극)와 EMS(전기근육자극)는 전자기 에너지를 이용해 근육을 강제로 수축시키는 시술이다. 한국에서는 '엠스컬프', '테슬라포머' 등의 브랜드명으로 알려져 있으며, 복부, 엉덩이, 팔, 다리 등의 근육 강화와 지방 감소를 목적으로 사용된다. |
| `/modality/9/extracted/mechanism` | mechanism | string | 고강도 집속 전자기장(HIFEM)이 운동신경을 자극하여 단시간에 수만 회의 근육 초극대 수축(supramaximal contraction)을 유발한다. 이는 일반적인 운동으로는 달성할 수 없는 강도의 근육 수축으로, 근육 섬유의 재구성(근비대)과 새로운 근섬유 생성(근섬유 증가)을 유도한다. 동시에 근육 수축으로 인해 주변 지방세포에 대사 스트레스가 가해져, 지방세포의 자연사(세포자멸사, apoptosis)가 유도되어 지방 감소 효과도 나타난다. |
| `/modality/9/extracted/indications` | indications | object | {object, 키 2: primary, extended} |
| `/modality/9/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/9/extracted/indications/primary/0` | primary[0] | string | 복부 근육 강화 및 지방 감소 |
| `/modality/9/extracted/indications/primary/1` | primary[1] | string | 엉덩이 리프팅 (힙업) |
| `/modality/9/extracted/indications/primary/2` | primary[2] | string | 허벅지 근육 강화 |
| `/modality/9/extracted/indications/extended` | extended | array | [array, 원소 4] |
| `/modality/9/extracted/indications/extended/0` | extended[0] | string | 팔뚝 근육 토닝 |
| `/modality/9/extracted/indications/extended/1` | extended[1] | string | 종아리 근육 강화 |
| `/modality/9/extracted/indications/extended/2` | extended[2] | string | 산후 복직근이개 (배 근육 벌어짐) 개선 |
| `/modality/9/extracted/indications/extended/3` | extended[3] | string | 골반저근 강화 (요실금 개선) |
| `/modality/9/extracted/contraindications` | contraindications | object | {object, 키 2: absolute, relative} |
| `/modality/9/extracted/contraindications/absolute` | absolute | array | [array, 원소 3] |
| `/modality/9/extracted/contraindications/absolute/0` | absolute[0] | string | 체내 금속 임플란트가 시술 부위에 있는 경우 |
| `/modality/9/extracted/contraindications/absolute/1` | absolute[1] | string | 심장박동기(페이스메이커) 또는 이식형 제세동기 사용자 |
| `/modality/9/extracted/contraindications/absolute/2` | absolute[2] | string | 임신 중인 경우 |
| `/modality/9/extracted/contraindications/relative` | relative | array | [array, 원소 3] |
| `/modality/9/extracted/contraindications/relative/0` | relative[0] | string | 간질(뇌전증) 환자 |
| `/modality/9/extracted/contraindications/relative/1` | relative[1] | string | 심각한 심폐질환 환자 |
| `/modality/9/extracted/contraindications/relative/2` | relative[2] | string | 최근 수술 이력이 있는 부위 |
| `/modality/9/extracted/safety` | safety | object | {object, 키 2: common, uncommon} |
| `/modality/9/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/9/extracted/safety/common/0` | common[0] | string | 시술 부위 근육통 (운동 후와 비슷한 느낌) |
| `/modality/9/extracted/safety/common/1` | common[1] | string | 일시적 근육 경련 |
| `/modality/9/extracted/safety/common/2` | common[2] | string | 시술 중 약간의 불편감 |
| `/modality/9/extracted/safety/uncommon` | uncommon | array | [array, 원소 2] |
| `/modality/9/extracted/safety/uncommon/0` | uncommon[0] | string | 시술 부위 피부 발적 (빨개짐) |
| `/modality/9/extracted/safety/uncommon/1` | uncommon[1] | string | 일시적 관절/건 불편감 |
| `/modality/9/extracted/onset_duration` | onset_duration | object | {object, 키 3: onset, peak, duration} |
| `/modality/9/extracted/onset_duration/onset` | onset | string | 시술 직후 근육 피로감, 2~4주 후 근육 강화 체감 |
| `/modality/9/extracted/onset_duration/peak` | peak | string | 마지막 시술 후 2~4주 뒤 |
| `/modality/9/extracted/onset_duration/duration` | duration | string | 6~12개월 유지 (운동 병행 시 더 오래 유지) |
| `/modality/9/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/9/extracted/aftercare/0` | aftercare[0] | string | 특별한 다운타임 없이 일상생활 바로 가능 |
| `/modality/9/extracted/aftercare/1` | aftercare[1] | string | 충분한 수분 섭취 |
| `/modality/9/extracted/aftercare/2` | aftercare[2] | string | 운동 병행 시 효과 극대화 |
| `/modality/9/extracted/related_techniques` | related_techniques | array | [array, 원소 3] |
| `/modality/9/extracted/related_techniques/0` | related_techniques[0] | string | 크라이오리포라이시스 (냉동지방분해) -- 지방 감소에 병합 |
| `/modality/9/extracted/related_techniques/1` | related_techniques[1] | string | 고주파(RF) 바디 -- 피부 타이트닝과 시너지 |
| `/modality/9/extracted/related_techniques/2` | related_techniques[2] | string | 지방흡입 -- 더 적극적인 지방 제거가 필요한 경우 |
| `/modality/9/products` | products | array | `[]` (빈 배열) |
| `/modality/9/name` | name | string | HIFES/EMS |

## 잠정 관찰 (원문 아님 · 직접 읽기 기록)

| 상태 | 근거 Pointer | 관찰 |
|---|---|---|
| P | `/modality/9/category`, `/modality/9/category_en`, `/modality/9/subcategories/0/label`, `/modality/9/subcategories/1/label` | M10 category·category_en 모두 'HIFES/EMS'(영문 동일). 하위분류는 부위 축('페이셜 EMS','바디 EMS'). products 빈 배열. |
| P | `/modality/9/subcategories/0/items/0/name`, `/modality/9/subcategories/0/items/1/name`, `/modality/9/subcategories/1/items/1/name`, `/modality/9/subcategories/1/items/7/name` | 같은 장비로 보이는 항목 쌍: '엠페이스(EMFACE)'(M10-1-1)/'엠페이스'(auto), '엠스컬프트네오'(M10-2-2)/'엠스컬프트NEO'(auto). 내용 상세도가 다르다(연결 키 없음). |
| P | `/modality/9/extracted/mechanism`, `/modality/9/subcategories/1/items/0/detail`, `/modality/9/subcategories/0/items/0/detail` | 용어 혼용: HIFES(고강도 집속 전자기 자극) / HIFEM(고강도 집속 전자기장). 모달리티 이름은 HIFES 이고 mechanism·엠스컬프트는 HIFEM. |
| P | `/modality/9/subcategories/1/items/5/detail`, `/modality/9/subcategories/1/items/5/extracted/mechanism`, `/modality/9/subcategories/1/items/4/detail` | 쿨톤은 '쿨스컬프팅+EMS'(크라이오리폴리시스, M14 계열), 트루스컬프트는 'RF 바디 지방감소'(EMS 아님) — M10 바디 EMS 하위분류에 다른 에너지 장비가 있다. |
| I | `/modality/9/subcategories/1/items/4/extracted/aftercare/1`, `/modality/9/subcategories/1/items/4/extracted/aftercare/0` | 트루스컬프트(RF 지방감소) aftercare 에 '시술 후 근육통은 정상 반응 (1-3일)' — EMS 상용 문장 혼입으로 보임. 같은 배열에 '충분한 수분 섭취' 계열 문장이 두 번(이볼브도 같음). |
| P | `/modality/9/subcategories/1/items/0/extracted/safety/serious` | safety/serious 원소가 금기 문장('심박동기, 금속 임플란트 보유자 금기','임신 중 금지'). |
| P | `/modality/9/subcategories/0/items/0/extracted/aftercare/3` | M10 상용구 '[시술 주기 참고] 3개월 간격 권장. 근육 적응 및 지방 대사 완료 후 재시술 …' — 엠스컬프트 duration '월 1-2회 시술로 지속' 과 다르다. |
| P | `/modality/9/extracted/indications/extended/2`, `/modality/9/extracted/indications/extended/3` | 확장 적응증 '산후 복직근이개', '골반저근 강화 (요실금 개선)' — 미용 외 기능 개선. |

## 수동 복합 표현 (원문 구간)

| Pointer | 구간 | 원문 표현 | 관점 | 메모 |
|---|---|---|---|---|
| `/modality/9/subcategories/0/items/0/detail` | [0, 25] | BTL · RF+HIFES · 근육+피부 동시 | 기호 | '+' 에너지 결합 / 대상 결합 |
| `/modality/9/subcategories/0/items/0/extracted/safety/serious/0` | [0, 28] | 금속 임플란트 부위의 화상 위험 (사전 확인 필수) | 조건, 가능성·빈도 |  |
| `/modality/9/subcategories/0/items/0/extracted/aftercare/0` | [0, 17] | 시술 24시간 후 스킨케어 재개 | 수량·단위·시간 |  |
| `/modality/9/subcategories/0/items/0/extracted/aftercare/3` | [11, 44] | 3개월 간격 권장. 근육 적응 및 지방 대사 완료 후 재시술 | 수량·단위·시간, 조건 | 상용구 |
| `/modality/9/subcategories/1/items/0/extracted/mechanism` | [75, 98] | 30분 시술로 수만 회의 강력한 근육 수축 | 수량·단위·시간 | '수만 회' 비수치 |
| `/modality/9/subcategories/1/items/0/extracted/mechanism` | [125, 166] | 근육 수축의 대사 산물이 인접 지방세포의 자연사(apoptosis)를 유발 | 수식 |  |
| `/modality/9/subcategories/1/items/0/extracted/indications/primary/1` | [0, 12] | 엉덩이 리프팅 (힙업) | 부위 |  |
| `/modality/9/subcategories/1/items/0/extracted/safety/common/1` | [0, 18] | 시술 후 근육통 (48-72시간) | 수량·단위·시간, 범위 |  |
| `/modality/9/subcategories/1/items/0/extracted/onset_duration/duration` | [0, 26] | 3-6개월 효과 유지, 월 1-2회 시술로 지속 | 수량·단위·시간, 범위 |  |
| `/modality/9/subcategories/1/items/0/extracted/aftercare/3` | [0, 18] | 최소 48시간 후 정상 운동 재개 | 범위, 수량·단위·시간 |  |
| `/modality/9/subcategories/1/items/1/extracted/safety/serious/2` | [0, 17] | 활성 피부 감염 부위 시술 금지 | 조건, 부정 |  |
| `/modality/9/subcategories/1/items/2/detail` | [0, 19] | RF+EMS+석션 · 바디 컨투어링 | 기호 |  |
| `/modality/9/subcategories/1/items/3/extracted/aftercare/1` | [0, 22] | 시술 후 근육통은 정상 반응 (1-3일) | 수량·단위·시간, 범위 |  |
| `/modality/9/subcategories/1/items/4/extracted/mechanism` | [0, 51] | 1.8MHz RF 에너지가 피하지방층 깊숙이 침투하여 지방세포의 온도를 45-50도까지 상승 | 수량·단위·시간, 범위, 부위 |  |
| `/modality/9/subcategories/1/items/5/detail` | [0, 18] | 앨러간 · 쿨스컬프팅+EMS 근육 | 기호, 참조 |  |
| `/modality/9/extracted/overview` | [68, 107] | 한국에서는 '엠스컬프', '테슬라포머' 등의 브랜드명으로 알려져 있으며 | 시술·제품명, 참조 | 항목명(엠스컬프트)과 표기 다름 |
| `/modality/9/extracted/mechanism` | [88, 117] | 일반적인 운동으로는 달성할 수 없는 강도의 근육 수축 | 부정, 비교 |  |
| `/modality/9/extracted/indications/extended/3` | [0, 16] | 골반저근 강화 (요실금 개선) | 부위 |  |
| `/modality/9/extracted/contraindications/absolute/1` | [0, 29] | 심장박동기(페이스메이커) 또는 이식형 제세동기 사용자 | 조건 |  |
| `/modality/9/extracted/contraindications/relative/2` | [0, 15] | 최근 수술 이력이 있는 부위 | 조건, 수량·단위·시간 | '최근' 비수치 |
| `/modality/9/extracted/onset_duration/peak` | [0, 15] | 마지막 시술 후 2~4주 뒤 | 수량·단위·시간, 범위, 조건 | 기준 사건 '마지막 시술' |
| `/modality/9/extracted/onset_duration/duration` | [0, 27] | 6~12개월 유지 (운동 병행 시 더 오래 유지) | 조건, 비교 |  |
| `/modality/9/extracted/aftercare/0` | [0, 22] | 특별한 다운타임 없이 일상생활 바로 가능 | 부정, 가능성·빈도 |  |
| `/modality/9/extracted/related_techniques/2` | [0, 28] | 지방흡입 -- 더 적극적인 지방 제거가 필요한 경우 | 참조, 조건, 비교 | taxonomy 밖 시술 |

## 형태소 분석 확인 (알려진 오분절 K)

| 범위 | 표면형 | 문제 | 영향 |
|---|---|---|---|
| all | 엠스컬프트NEO | 엠스컬프/NNG 트/VV NEO/SL — 끝 '트' 를 동사로 | 장비명 소실 |
| all | 복직근이개 | 복직근/NNP 이/JKS 개/NNG — '이개(diastasis)'를 조사+명사로 | 질환명 소실·조사 오탐 |

## 미결

| ID | 상태 | Pointer | 내용 | 영향·후속 |
|---|---|---|---|---|
| S032-F01 | F | `/modality/9/subcategories/0/items/0`, `/modality/9/subcategories/0/items/1`, `/modality/9/subcategories/1/items/1`, `/modality/9/subcategories/1/items/7` | 같은 장비로 보이는 항목 쌍(엠페이스, 엠스컬프트네오/NEO). | 개체 병합 후속 |
| S032-I01 | I | `/modality/9/subcategories/1/items/4/extracted/aftercare/1` | RF 장비 aftercare 에 EMS 근육통 문장. | 관리 지시 채택 시 확인 |
| S032-F02 | F | `/modality/9/subcategories/1/items/5`, `/modality/9/subcategories/1/items/4` | M10 에 크라이오·RF 지방감소 장비. | 계열 경계 후속 |

