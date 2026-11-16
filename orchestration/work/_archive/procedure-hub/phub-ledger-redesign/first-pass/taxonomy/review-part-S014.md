# S014 — M5 PRP/자가혈

- 읽기 상태: **read** · 마지막 읽은 Pointer `/modality/4/name`
- 단위: id, category, category_en, group, subcategories 컨테이너, M5-1 items/0, M5-2 items/0, M5-2 items/1, M5-3 items/0, M5-new-1774324656750 items/0, extracted, products 컨테이너, M5-P-0, M5-P-1, M5-P-2, M5-P-3, M5-P-4, name
- 상위 문맥(공동 참조·소유 아님): 없음
- 기계 기록: `source-map.json`(section=S014) · `morphology/S014.json` · `expressions.json`(section=S014) · 읽기 렌더 `reading/S014.txt`

## 원문 값 (원본 컬럼명 그대로, 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/modality/4` | modality[4] | object | {object, 키 8: id, category, category_en, group, subcategories, extracted, products, name} |
| `/modality/4/id` | id | string | M5 |
| `/modality/4/category` | category | string | PRP/자가혈 |
| `/modality/4/category_en` | category_en | string | PRP / Autologous Blood |
| `/modality/4/group` | group | string | 주사/주입 |
| `/modality/4/subcategories` | subcategories | array | [array, 원소 4] |
| `/modality/4/subcategories/0` | subcategories[0] | object | {object, 키 3: id, label, items} |
| `/modality/4/subcategories/0/id` | id | string | M5-1 |
| `/modality/4/subcategories/0/label` | label | string | PRP (혈소판풍부혈장) |
| `/modality/4/subcategories/0/items` | items | array | [array, 원소 1] |
| `/modality/4/subcategories/0/items/0` | items[0] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/4/subcategories/0/items/0/id` | id | string | M5-1-1 |
| `/modality/4/subcategories/0/items/0/name` | name | string | PRP |
| `/modality/4/subcategories/0/items/0/detail` | detail | string | 원심분리 → 성장인자 농축 → 주입 |
| `/modality/4/subcategories/0/items/0/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/4/subcategories/0/items/0/extracted/overview` | overview | string | 자가혈액 혈소판 3-5배 농축 성장인자 치료 |
| `/modality/4/subcategories/0/items/0/extracted/mechanism` | mechanism | string | 원심분리로 혈소판을 3-5배 농축(≥1,000,000 plt/μL)하여 PDGF, TGF-β1, VEGF, EGF, FGF-2, IGF-1 등 4000+ 단백질을 함유. 활성화 1시간 내 95% 성장인자 방출 후 7-10일간 추가 합성되며, 진피 섬유모세포 증식 및 I형 콜라겐 생성을 촉진. |
| `/modality/4/subcategories/0/items/0/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/4/subcategories/0/items/0/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/4/subcategories/0/items/0/extracted/indications/primary/0` | primary[0] | string | 피부 노화 |
| `/modality/4/subcategories/0/items/0/extracted/indications/primary/1` | primary[1] | string | 주름 개선 |
| `/modality/4/subcategories/0/items/0/extracted/indications/primary/2` | primary[2] | string | 피부 탄력 저하 |
| `/modality/4/subcategories/0/items/0/extracted/indications/primary/3` | primary[3] | string | 탈모 |
| `/modality/4/subcategories/0/items/0/extracted/indications/primary/4` | primary[4] | string | 모발 재성장 |
| `/modality/4/subcategories/0/items/0/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/4/subcategories/0/items/0/extracted/safety/common` | common | array | [array, 원소 4] |
| `/modality/4/subcategories/0/items/0/extracted/safety/common/0` | common[0] | string | 주입 부위 통증 |
| `/modality/4/subcategories/0/items/0/extracted/safety/common/1` | common[1] | string | 부종 |
| `/modality/4/subcategories/0/items/0/extracted/safety/common/2` | common[2] | string | 발적 |
| `/modality/4/subcategories/0/items/0/extracted/safety/common/3` | common[3] | string | 일시적 멍 |
| `/modality/4/subcategories/0/items/0/extracted/safety/serious` | serious | array | [array, 원소 3] |
| `/modality/4/subcategories/0/items/0/extracted/safety/serious/0` | serious[0] | string | 감염 |
| `/modality/4/subcategories/0/items/0/extracted/safety/serious/1` | serious[1] | string | TGF-beta1에 의한 비후성 반흔 촉진 가능 |
| `/modality/4/subcategories/0/items/0/extracted/safety/serious/2` | serious[2] | string | 알레르기 반응(드묾) |
| `/modality/4/subcategories/0/items/0/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/4/subcategories/0/items/0/extracted/onset_duration/onset` | onset | string | 2-4주 |
| `/modality/4/subcategories/0/items/0/extracted/onset_duration/duration` | duration | string | 3-6개월 |
| `/modality/4/subcategories/0/items/0/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/4/subcategories/0/items/0/extracted/aftercare/0` | aftercare[0] | string | 주입 후 24시간 냉찜질 |
| `/modality/4/subcategories/0/items/0/extracted/aftercare/1` | aftercare[1] | string | NSAIDs 사용 자제 (혈소판 기능 억제) |
| `/modality/4/subcategories/0/items/0/extracted/aftercare/2` | aftercare[2] | string | 음주·운동 1주일 제한 |
| `/modality/4/subcategories/0/items/0/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 1-3개월 간격, 2-3회 코스 권장 (스킨부스터에 준함). 효과 발현 4-8주. NSAIDs 자제 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/4/subcategories/1` | subcategories[1] | object | {object, 키 3: id, label, items} |
| `/modality/4/subcategories/1/id` | id | string | M5-2 |
| `/modality/4/subcategories/1/label` | label | string | PRF (피브린풍부혈장) |
| `/modality/4/subcategories/1/items` | items | array | [array, 원소 2] |
| `/modality/4/subcategories/1/items/0` | items[0] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/4/subcategories/1/items/0/id` | id | string | M5-2-1 |
| `/modality/4/subcategories/1/items/0/name` | name | string | PRF |
| `/modality/4/subcategories/1/items/0/detail` | detail | string | 2세대 · 서방형 성장인자 |
| `/modality/4/subcategories/1/items/0/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/4/subcategories/1/items/0/extracted/overview` | overview | string | 2세대 자가혈 제품, 서방형 성장인자 방출 |
| `/modality/4/subcategories/1/items/0/extracted/mechanism` | mechanism | string | 혈소판과 백혈구를 포함한 섬유소 매트릭스 형성으로 성장인자(PDGF, TGF-β1, VEGF)를 14-28일에 걸쳐 지속 방출. PRP 대비 장시간 생체활성 유지로 진피 리모델링 및 신생혈관화 촉진. |
| `/modality/4/subcategories/1/items/0/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/4/subcategories/1/items/0/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/4/subcategories/1/items/0/extracted/indications/primary/0` | primary[0] | string | 피부 재생 |
| `/modality/4/subcategories/1/items/0/extracted/indications/primary/1` | primary[1] | string | 진피층 회복 |
| `/modality/4/subcategories/1/items/0/extracted/indications/primary/2` | primary[2] | string | 질 주름 개선 |
| `/modality/4/subcategories/1/items/0/extracted/indications/primary/3` | primary[3] | string | 흉터 |
| `/modality/4/subcategories/1/items/0/extracted/indications/primary/4` | primary[4] | string | 탈모 |
| `/modality/4/subcategories/1/items/0/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/4/subcategories/1/items/0/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/4/subcategories/1/items/0/extracted/safety/common/0` | common[0] | string | 주입 부위 통증 |
| `/modality/4/subcategories/1/items/0/extracted/safety/common/1` | common[1] | string | 부종 |
| `/modality/4/subcategories/1/items/0/extracted/safety/common/2` | common[2] | string | 발적 |
| `/modality/4/subcategories/1/items/0/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/4/subcategories/1/items/0/extracted/safety/serious/0` | serious[0] | string | 감염 |
| `/modality/4/subcategories/1/items/0/extracted/safety/serious/1` | serious[1] | string | 이물질 반응 |
| `/modality/4/subcategories/1/items/0/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/4/subcategories/1/items/0/extracted/onset_duration/onset` | onset | string | 3-4주 |
| `/modality/4/subcategories/1/items/0/extracted/onset_duration/duration` | duration | string | 4-8개월 |
| `/modality/4/subcategories/1/items/0/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/4/subcategories/1/items/0/extracted/aftercare/0` | aftercare[0] | string | 주입 후 48시간 냉찜질 |
| `/modality/4/subcategories/1/items/0/extracted/aftercare/1` | aftercare[1] | string | 음주·운동 2주 제한 |
| `/modality/4/subcategories/1/items/0/extracted/aftercare/2` | aftercare[2] | string | 정기적인 후속 시술 권장 |
| `/modality/4/subcategories/1/items/0/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 1-3개월 간격, 2-3회 코스 권장 (스킨부스터에 준함). 효과 발현 4-8주. NSAIDs 자제 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/4/subcategories/1/items/1` | items[1] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/4/subcategories/1/items/1/id` | id | string | auto-M5-1775364775189 |
| `/modality/4/subcategories/1/items/1/name` | name | string | CGF |
| `/modality/4/subcategories/1/items/1/detail` | detail | string | 성장인자농축 |
| `/modality/4/subcategories/1/items/1/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/4/subcategories/1/items/1/extracted/overview` | overview | string | 성장인자 농축 자가혈 치료 |
| `/modality/4/subcategories/1/items/1/extracted/mechanism` | mechanism | string | 자가혈액에서 추출한 농축 성장인자가 피부 재생을 촉진합니다. 혈소판과 성장인자가 콜라겐 생성과 혈관 신생을 유도하여 자연스러운 피부 개선을 유도합니다. |
| `/modality/4/subcategories/1/items/1/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/4/subcategories/1/items/1/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/4/subcategories/1/items/1/extracted/indications/primary/0` | primary[0] | string | 자연스러운 피부 재생 |
| `/modality/4/subcategories/1/items/1/extracted/indications/primary/1` | primary[1] | string | 흉터 개선 |
| `/modality/4/subcategories/1/items/1/extracted/indications/primary/2` | primary[2] | string | 모공 축소 |
| `/modality/4/subcategories/1/items/1/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/4/subcategories/1/items/1/extracted/safety/common` | common | array | [array, 원소 2] |
| `/modality/4/subcategories/1/items/1/extracted/safety/common/0` | common[0] | string | 채혈 부위 멍 |
| `/modality/4/subcategories/1/items/1/extracted/safety/common/1` | common[1] | string | 일시적 부종 |
| `/modality/4/subcategories/1/items/1/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/4/subcategories/1/items/1/extracted/onset_duration/onset` | onset | string | 2-4주 |
| `/modality/4/subcategories/1/items/1/extracted/onset_duration/duration` | duration | string | 6-12개월 |
| `/modality/4/subcategories/1/items/1/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/4/subcategories/1/items/1/extracted/aftercare/0` | aftercare[0] | string | 채혈 후 충분한 수분 섭취 |
| `/modality/4/subcategories/1/items/1/extracted/aftercare/1` | aftercare[1] | string | 시술 부위 냉찜질 |
| `/modality/4/subcategories/1/items/1/extracted/aftercare/2` | aftercare[2] | string | 음주 자제 3일 |
| `/modality/4/subcategories/1/items/1/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 1-3개월 간격, 2-3회 코스 권장 (스킨부스터에 준함). 효과 발현 4-8주. NSAIDs 자제 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/4/subcategories/2` | subcategories[2] | object | {object, 키 3: id, label, items} |
| `/modality/4/subcategories/2/id` | id | string | M5-3 |
| `/modality/4/subcategories/2/label` | label | string | MCT (메타셀) |
| `/modality/4/subcategories/2/items` | items | array | [array, 원소 1] |
| `/modality/4/subcategories/2/items/0` | items[0] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/4/subcategories/2/items/0/id` | id | string | M5-3-1 |
| `/modality/4/subcategories/2/items/0/name` | name | string | CPR |
| `/modality/4/subcategories/2/items/0/detail` | detail | string | 고농축 성장인자 |
| `/modality/4/subcategories/2/items/0/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/4/subcategories/2/items/0/extracted/overview` | overview | string | 고농축 혈소판 성장인자 제제 |
| `/modality/4/subcategories/2/items/0/extracted/mechanism` | mechanism | string | 혈소판을 고농축(5배 이상)하여 PDGF, TGF-β1, VEGF, EGF 등 성장인자 농도를 극대화. 진피 섬유모세포의 증식 및 I형 콜라겐 생성 능력을 4-6배 증강하고 MMP-1/3 발현 조절. |
| `/modality/4/subcategories/2/items/0/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/4/subcategories/2/items/0/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/4/subcategories/2/items/0/extracted/indications/primary/0` | primary[0] | string | 깊은 주름 |
| `/modality/4/subcategories/2/items/0/extracted/indications/primary/1` | primary[1] | string | 피부 탄력 저하 |
| `/modality/4/subcategories/2/items/0/extracted/indications/primary/2` | primary[2] | string | 광손상 피부 |
| `/modality/4/subcategories/2/items/0/extracted/indications/primary/3` | primary[3] | string | 난치성 탈모 |
| `/modality/4/subcategories/2/items/0/extracted/indications/primary/4` | primary[4] | string | 재생성 흉터 |
| `/modality/4/subcategories/2/items/0/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/4/subcategories/2/items/0/extracted/safety/common` | common | array | [array, 원소 4] |
| `/modality/4/subcategories/2/items/0/extracted/safety/common/0` | common[0] | string | 주입 부위 통증 |
| `/modality/4/subcategories/2/items/0/extracted/safety/common/1` | common[1] | string | 부종 |
| `/modality/4/subcategories/2/items/0/extracted/safety/common/2` | common[2] | string | 발적 |
| `/modality/4/subcategories/2/items/0/extracted/safety/common/3` | common[3] | string | 일시적 멍 |
| `/modality/4/subcategories/2/items/0/extracted/safety/serious` | serious | array | [array, 원소 3] |
| `/modality/4/subcategories/2/items/0/extracted/safety/serious/0` | serious[0] | string | 감염 |
| `/modality/4/subcategories/2/items/0/extracted/safety/serious/1` | serious[1] | string | 신경 손상 |
| `/modality/4/subcategories/2/items/0/extracted/safety/serious/2` | serious[2] | string | 과도한 염증반응 |
| `/modality/4/subcategories/2/items/0/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/4/subcategories/2/items/0/extracted/onset_duration/onset` | onset | string | 2-3주 |
| `/modality/4/subcategories/2/items/0/extracted/onset_duration/duration` | duration | string | 4-6개월 |
| `/modality/4/subcategories/2/items/0/extracted/aftercare` | aftercare | array | [array, 원소 5] |
| `/modality/4/subcategories/2/items/0/extracted/aftercare/0` | aftercare[0] | string | 주입 후 24시간 냉찜질 |
| `/modality/4/subcategories/2/items/0/extracted/aftercare/1` | aftercare[1] | string | 72시간 화장품 사용 자제 |
| `/modality/4/subcategories/2/items/0/extracted/aftercare/2` | aftercare[2] | string | 2주간 음주·사우나 자제 |
| `/modality/4/subcategories/2/items/0/extracted/aftercare/3` | aftercare[3] | string | 비후성 반흔 위험군은 의료진 상담 필수 |
| `/modality/4/subcategories/2/items/0/extracted/aftercare/4` | aftercare[4] | string | [시술 주기 참고] 1-3개월 간격, 2-3회 코스 권장 (스킨부스터에 준함). 효과 발현 4-8주. NSAIDs 자제 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/4/subcategories/3` | subcategories[3] | object | {object, 키 3: id, label, items} |
| `/modality/4/subcategories/3/id` | id | string | M5-new-1774324656750 |
| `/modality/4/subcategories/3/label` | label | string | ACT |
| `/modality/4/subcategories/3/items` | items | array | [array, 원소 1] |
| `/modality/4/subcategories/3/items/0` | items[0] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/4/subcategories/3/items/0/id` | id | string | auto-M5-1775364775190 |
| `/modality/4/subcategories/3/items/0/name` | name | string | ACR |
| `/modality/4/subcategories/3/items/0/detail` | detail | string | 자가세포재생 |
| `/modality/4/subcategories/3/items/0/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/4/subcategories/3/items/0/extracted/overview` | overview | string | 자가세포 재생 치료 |
| `/modality/4/subcategories/3/items/0/extracted/mechanism` | mechanism | string | 환자 자신의 혈액에서 추출한 재생인자가 손상된 피부를 복구합니다. 자가 치유력을 극대화하여 부작용을 최소화하면서 자연스러운 피부 개선을 달성합니다. |
| `/modality/4/subcategories/3/items/0/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/4/subcategories/3/items/0/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/4/subcategories/3/items/0/extracted/indications/primary/0` | primary[0] | string | 자연스러운 안티에이징 |
| `/modality/4/subcategories/3/items/0/extracted/indications/primary/1` | primary[1] | string | 피부 재생 |
| `/modality/4/subcategories/3/items/0/extracted/indications/primary/2` | primary[2] | string | 전체적인 피부 개선 |
| `/modality/4/subcategories/3/items/0/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/4/subcategories/3/items/0/extracted/safety/common` | common | array | [array, 원소 2] |
| `/modality/4/subcategories/3/items/0/extracted/safety/common/0` | common[0] | string | 채혈 부위 불편감 |
| `/modality/4/subcategories/3/items/0/extracted/safety/common/1` | common[1] | string | 경미한 홍조 |
| `/modality/4/subcategories/3/items/0/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/4/subcategories/3/items/0/extracted/onset_duration/onset` | onset | string | 3-4주 |
| `/modality/4/subcategories/3/items/0/extracted/onset_duration/duration` | duration | string | 8-12개월 |
| `/modality/4/subcategories/3/items/0/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/4/subcategories/3/items/0/extracted/aftercare/0` | aftercare[0] | string | 충분한 영양 섭취 |
| `/modality/4/subcategories/3/items/0/extracted/aftercare/1` | aftercare[1] | string | 규칙적인 생활 |
| `/modality/4/subcategories/3/items/0/extracted/aftercare/2` | aftercare[2] | string | 스트레스 관리 |
| `/modality/4/subcategories/3/items/0/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 1-3개월 간격, 2-3회 코스 권장 (스킨부스터에 준함). 효과 발현 4-8주. NSAIDs 자제 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/4/extracted` | extracted | object | {object, 키 8: overview, mechanism, indications, contraindications, safety, onset_duration, aftercare, related_techniques} |
| `/modality/4/extracted/overview` | overview | string | PRP는 자기 혈액에서 혈소판이 풍부한 혈장(피를 뽑아서 성장인자가 많은 부분만 모은 것)을 추출해 피부에 주사하거나 바르는 재생 시술이다. 1987년 심장수술에서 처음 사용된 후, 피부 노화 개선 효과가 알려지면서 미용 분야에서 단독 또는 다른 시술과 병행해 널리 쓰이고 있다. |
| `/modality/4/extracted/mechanism` | mechanism | string | 환자 본인의 혈액을 채취해 원심분리기(빠르게 회전시키는 기계)로 돌려 혈소판이 농축된 혈장을 추출한다. 이 PRP에는 PDGF, TGF-β, VEGF, EGF, IGF 등 다양한 성장인자(세포 성장을 촉진하는 단백질)가 풍부하게 들어있다. 이 성장인자들이 피부의 섬유모세포(콜라겐을 만드는 세포)를 자극해서 새로운 콜라겐과 엘라스틴(피부 탄력 성분)을 만들어내고, 히알루론산 생성도 촉진한다. |
| `/modality/4/extracted/indications` | indications | object | {object, 키 2: primary, extended} |
| `/modality/4/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/4/extracted/indications/primary/0` | primary[0] | string | 피부 노화 개선 (전반적인 피부결, 탄력, 피부톤 개선) |
| `/modality/4/extracted/indications/primary/1` | primary[1] | string | 잔주름 감소 |
| `/modality/4/extracted/indications/primary/2` | primary[2] | string | 꺼진 부위 볼륨 회복 (꺼진 볼, 꺼진 눈밑, 팔자주름 등) |
| `/modality/4/extracted/indications/extended` | extended | array | [array, 원소 4] |
| `/modality/4/extracted/indications/extended/0` | extended[0] | string | 여드름흉터 (진피절제주입법과 병행) |
| `/modality/4/extracted/indications/extended/1` | extended[1] | string | 탈모치료 (두피에 주입) |
| `/modality/4/extracted/indications/extended/2` | extended[2] | string | 처진 피부 탄력 개선 |
| `/modality/4/extracted/indications/extended/3` | extended[3] | string | 다른 시술과 병행 — MTS, 프랙셔널 레이저, 메조테라피 후 도포 |
| `/modality/4/extracted/contraindications` | contraindications | object | {object, 키 2: absolute, relative} |
| `/modality/4/extracted/contraindications/absolute` | absolute | array | [array, 원소 3] |
| `/modality/4/extracted/contraindications/absolute/0` | absolute[0] | string | 혈소판 기능 장애가 있는 경우 |
| `/modality/4/extracted/contraindications/absolute/1` | absolute[1] | string | 패혈증이나 전신 감염이 있는 경우 |
| `/modality/4/extracted/contraindications/absolute/2` | absolute[2] | string | 주사 부위에 활동성 감염이나 염증이 있는 경우 |
| `/modality/4/extracted/contraindications/relative` | relative | array | [array, 원소 3] |
| `/modality/4/extracted/contraindications/relative/0` | relative[0] | string | 혈액 응고에 영향을 주는 약물(아스피린 등) 복용 중이면 출혈 위험이 높아질 수 있음 |
| `/modality/4/extracted/contraindications/relative/1` | relative[1] | string | 혈액으로 인한 감염성 질환이 있는 경우 주의 |
| `/modality/4/extracted/contraindications/relative/2` | relative[2] | string | 색소성 질환에 대한 치료 효과는 적은 편 |
| `/modality/4/extracted/safety` | safety | object | {object, 키 3: common, uncommon, serious} |
| `/modality/4/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/4/extracted/safety/common/0` | common[0] | string | 주사 부위 통증 |
| `/modality/4/extracted/safety/common/1` | common[1] | string | 1~2일 정도 붓기 |
| `/modality/4/extracted/safety/common/2` | common[2] | string | 3~7일 정도 멍이 들 수 있음 |
| `/modality/4/extracted/safety/uncommon` | uncommon | array | [array, 원소 1] |
| `/modality/4/extracted/safety/uncommon/0` | uncommon[0] | string | 피부 재생 정도가 사람마다 달라 시술 결과에 차이가 있을 수 있음 |
| `/modality/4/extracted/safety/serious` | serious | array | [array, 원소 1] |
| `/modality/4/extracted/safety/serious/0` | serious[0] | string | 본인 혈액을 사용하므로 알레르기·거부반응이 거의 없음 (매우 안전한 시술) |
| `/modality/4/extracted/onset_duration` | onset_duration | object | {object, 키 3: onset, peak, duration} |
| `/modality/4/extracted/onset_duration/onset` | onset | string | 시술 후 3~6주경부터 효과가 나타나기 시작 |
| `/modality/4/extracted/onset_duration/peak` | peak | string | 2~3개월에 걸쳐 서서히 좋아짐 |
| `/modality/4/extracted/onset_duration/duration` | duration | string | 1회 시술로 6~12개월 유지 (반복시술은 4~6주 간격 가능) |
| `/modality/4/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/4/extracted/aftercare/0` | aftercare[0] | string | 시술 후 세안이나 화장 등 일상생활에 지장 없음 |
| `/modality/4/extracted/aftercare/1` | aftercare[1] | string | 시술 부위 청결 유지 |
| `/modality/4/extracted/aftercare/2` | aftercare[2] | string | 깊은 주름이나 심한 노화에는 고주파, IPL, 필러, 보톡스 등과 병행하는 것이 좋음 |
| `/modality/4/extracted/related_techniques` | related_techniques | array | [array, 원소 3] |
| `/modality/4/extracted/related_techniques/0` | related_techniques[0] | string | MTS + PRP — MTS로 미세 구멍을 낸 후 PRP를 도포해 흡수 촉진 |
| `/modality/4/extracted/related_techniques/1` | related_techniques[1] | string | 프랙셔널 레이저 + PRP — 레이저 시술 후 PRP를 도포해 재생 효과 증대 |
| `/modality/4/extracted/related_techniques/2` | related_techniques[2] | string | 진피절제주입법 + PRP — 여드름흉터에 서브시전 후 PRP 주입 |
| `/modality/4/products` | products | array | [array, 원소 5] |
| `/modality/4/products/0` | products[0] | object | {object, 키 8: id, name, name_en, manufacturer, country, mfds, type, extracted} |
| `/modality/4/products/0/id` | id | string | M5-P-0 |
| `/modality/4/products/0/name` | name | string | 셀피아 |
| `/modality/4/products/0/name_en` | name_en | string | Cellpia |
| `/modality/4/products/0/manufacturer` | manufacturer | string | CGBio |
| `/modality/4/products/0/country` | country | string | KR |
| `/modality/4/products/0/mfds` | mfds | boolean | true |
| `/modality/4/products/0/type` | type | string | PRP키트 |
| `/modality/4/products/0/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/4/products/0/extracted/overview` | overview | string | 자가혈 기반 세포 활성 성장인자 제제 |
| `/modality/4/products/0/extracted/mechanism` | mechanism | string | 자가혈액에서 혈소판 및 성장인자를 추출·농축하여 섬유모세포 증식, I형 콜라겐 생성, VEGF 매개 신생혈관화 유도. 개인 맞춤형 성장인자 농도 기반 피부 재생. |
| `/modality/4/products/0/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/4/products/0/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/4/products/0/extracted/indications/primary/0` | primary[0] | string | 피부 노화 |
| `/modality/4/products/0/extracted/indications/primary/1` | primary[1] | string | 주름 |
| `/modality/4/products/0/extracted/indications/primary/2` | primary[2] | string | 피부톤 개선 |
| `/modality/4/products/0/extracted/indications/primary/3` | primary[3] | string | 탈모 |
| `/modality/4/products/0/extracted/indications/primary/4` | primary[4] | string | 피부 재생 |
| `/modality/4/products/0/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/4/products/0/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/4/products/0/extracted/safety/common/0` | common[0] | string | 주입 부위 통증 |
| `/modality/4/products/0/extracted/safety/common/1` | common[1] | string | 부종 |
| `/modality/4/products/0/extracted/safety/common/2` | common[2] | string | 발적 |
| `/modality/4/products/0/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/4/products/0/extracted/safety/serious/0` | serious[0] | string | 감염 |
| `/modality/4/products/0/extracted/safety/serious/1` | serious[1] | string | 알레르기 반응 |
| `/modality/4/products/0/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/4/products/0/extracted/onset_duration/onset` | onset | string | 2-4주 |
| `/modality/4/products/0/extracted/onset_duration/duration` | duration | string | 3-6개월 |
| `/modality/4/products/0/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/4/products/0/extracted/aftercare/0` | aftercare[0] | string | 주입 후 냉찜질 |
| `/modality/4/products/0/extracted/aftercare/1` | aftercare[1] | string | 항염증제 사용 가능 |
| `/modality/4/products/0/extracted/aftercare/2` | aftercare[2] | string | 1주일 자외선 차단 |
| `/modality/4/products/0/extracted/aftercare/3` | aftercare[3] | string | 음주·운동 제한 |
| `/modality/4/products/1` | products[1] | object | {object, 키 8: id, name, name_en, manufacturer, country, mfds, type, extracted} |
| `/modality/4/products/1/id` | id | string | M5-P-1 |
| `/modality/4/products/1/name` | name | string | 리젠ACR |
| `/modality/4/products/1/name_en` | name_en | string | RegenACR |
| `/modality/4/products/1/manufacturer` | manufacturer | string | 리젠바이오텍 |
| `/modality/4/products/1/country` | country | string | KR |
| `/modality/4/products/1/mfds` | mfds | boolean | true |
| `/modality/4/products/1/type` | type | string | PRP키트 |
| `/modality/4/products/1/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/4/products/1/extracted/overview` | overview | string | 자동화 혈소판 농축 성장인자 시스템 |
| `/modality/4/products/1/extracted/mechanism` | mechanism | string | 자가혈액을 자동 원심분리하여 혈소판 3-5배 농축. PDGF, TGF-β1, VEGF, EGF, FGF 등 성장인자 최적화로 진피층 콜라겐 재생 및 세포 증식 촉진. |
| `/modality/4/products/1/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/4/products/1/extracted/indications/primary` | primary | array | [array, 원소 4] |
| `/modality/4/products/1/extracted/indications/primary/0` | primary[0] | string | 피부 주름 |
| `/modality/4/products/1/extracted/indications/primary/1` | primary[1] | string | 피부 탄력 저하 |
| `/modality/4/products/1/extracted/indications/primary/2` | primary[2] | string | 탈모 |
| `/modality/4/products/1/extracted/indications/primary/3` | primary[3] | string | 모발 재성장 |
| `/modality/4/products/1/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/4/products/1/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/4/products/1/extracted/safety/common/0` | common[0] | string | 주입 부위 통증 |
| `/modality/4/products/1/extracted/safety/common/1` | common[1] | string | 부종 |
| `/modality/4/products/1/extracted/safety/common/2` | common[2] | string | 멍 |
| `/modality/4/products/1/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/4/products/1/extracted/safety/serious/0` | serious[0] | string | 감염 |
| `/modality/4/products/1/extracted/safety/serious/1` | serious[1] | string | 신경 손상 |
| `/modality/4/products/1/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/4/products/1/extracted/onset_duration/onset` | onset | string | 3-4주 |
| `/modality/4/products/1/extracted/onset_duration/duration` | duration | string | 3-6개월 |
| `/modality/4/products/1/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/4/products/1/extracted/aftercare/0` | aftercare[0] | string | 주입 후 24시간 냉찜질 |
| `/modality/4/products/1/extracted/aftercare/1` | aftercare[1] | string | 1주일 자외선 차단 |
| `/modality/4/products/1/extracted/aftercare/2` | aftercare[2] | string | 음주·운동 1주일 제한 |
| `/modality/4/products/2` | products[2] | object | {object, 키 8: id, name, name_en, manufacturer, country, mfds, type, extracted} |
| `/modality/4/products/2/id` | id | string | M5-P-2 |
| `/modality/4/products/2/name` | name | string | 마이셀 |
| `/modality/4/products/2/name_en` | name_en | string | Mycell |
| `/modality/4/products/2/manufacturer` | manufacturer | string | 한스바이오메드 |
| `/modality/4/products/2/country` | country | string | KR |
| `/modality/4/products/2/mfds` | mfds | boolean | true |
| `/modality/4/products/2/type` | type | string | PRP키트 |
| `/modality/4/products/2/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/4/products/2/extracted/overview` | overview | string | 자가혈 기반 다층 성장인자 분리 제제 |
| `/modality/4/products/2/extracted/mechanism` | mechanism | string | 자가혈액에서 혈소판 및 백혈구 포함 성장인자층을 분리·농축하여 PDGF, TGF-β1, VEGF, HGF 등을 최대화. 섬유모세포 증식 및 I형 콜라겐 생성 능력 극대화. |
| `/modality/4/products/2/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/4/products/2/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/4/products/2/extracted/indications/primary/0` | primary[0] | string | 피부 노화 |
| `/modality/4/products/2/extracted/indications/primary/1` | primary[1] | string | 주름 개선 |
| `/modality/4/products/2/extracted/indications/primary/2` | primary[2] | string | 피부 재생 |
| `/modality/4/products/2/extracted/indications/primary/3` | primary[3] | string | 탈모 |
| `/modality/4/products/2/extracted/indications/primary/4` | primary[4] | string | 난치성 흉터 |
| `/modality/4/products/2/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/4/products/2/extracted/safety/common` | common | array | [array, 원소 4] |
| `/modality/4/products/2/extracted/safety/common/0` | common[0] | string | 주입 부위 통증 |
| `/modality/4/products/2/extracted/safety/common/1` | common[1] | string | 부종 |
| `/modality/4/products/2/extracted/safety/common/2` | common[2] | string | 발적 |
| `/modality/4/products/2/extracted/safety/common/3` | common[3] | string | 멍 |
| `/modality/4/products/2/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/4/products/2/extracted/safety/serious/0` | serious[0] | string | 감염 |
| `/modality/4/products/2/extracted/safety/serious/1` | serious[1] | string | 이물질 반응 |
| `/modality/4/products/2/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/4/products/2/extracted/onset_duration/onset` | onset | string | 2-4주 |
| `/modality/4/products/2/extracted/onset_duration/duration` | duration | string | 4-6개월 |
| `/modality/4/products/2/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/4/products/2/extracted/aftercare/0` | aftercare[0] | string | 주입 후 냉찜질 48시간 |
| `/modality/4/products/2/extracted/aftercare/1` | aftercare[1] | string | 72시간 화장품 최소화 |
| `/modality/4/products/2/extracted/aftercare/2` | aftercare[2] | string | 2주 음주·사우나 금지 |
| `/modality/4/products/2/extracted/aftercare/3` | aftercare[3] | string | 여성 환자는 높은 EGF/HGF 농도로 더 효과적 |
| `/modality/4/products/3` | products[3] | object | {object, 키 9: id, name, name_en, manufacturer, country, mfds, type, note, extracted} |
| `/modality/4/products/3/id` | id | string | M5-P-3 |
| `/modality/4/products/3/name` | name | string | ASCEplus |
| `/modality/4/products/3/name_en` | name_en | string | ASCE+ |
| `/modality/4/products/3/manufacturer` | manufacturer | string | 엑소코바이오 |
| `/modality/4/products/3/country` | country | string | KR |
| `/modality/4/products/3/mfds` | mfds | boolean | false |
| `/modality/4/products/3/type` | type | string | 엑소좀 |
| `/modality/4/products/3/note` | note | string | 화장품 허가 (주사 사용 불법) |
| `/modality/4/products/3/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/4/products/3/extracted/overview` | overview | string | 자가혈 유래 성장인자 복합 제제 |
| `/modality/4/products/3/extracted/mechanism` | mechanism | string | 자가혈액에서 혈소판 및 성장인자를 고농축하여 PDGF, TGF-β1, VEGF, EGF, IGF-1을 함유. 진피 섬유모세포의 증식 및 I형 콜라겐 생성과 세포외기질 재형성 촉진. |
| `/modality/4/products/3/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/4/products/3/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/4/products/3/extracted/indications/primary/0` | primary[0] | string | 피부 탄력 저하 |
| `/modality/4/products/3/extracted/indications/primary/1` | primary[1] | string | 주름 |
| `/modality/4/products/3/extracted/indications/primary/2` | primary[2] | string | 피부 광손상 |
| `/modality/4/products/3/extracted/indications/primary/3` | primary[3] | string | 탈모 |
| `/modality/4/products/3/extracted/indications/primary/4` | primary[4] | string | 피부 재생 |
| `/modality/4/products/3/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/4/products/3/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/4/products/3/extracted/safety/common/0` | common[0] | string | 주입 부위 통증 |
| `/modality/4/products/3/extracted/safety/common/1` | common[1] | string | 부종 |
| `/modality/4/products/3/extracted/safety/common/2` | common[2] | string | 발적 |
| `/modality/4/products/3/extracted/safety/serious` | serious | array | [array, 원소 3] |
| `/modality/4/products/3/extracted/safety/serious/0` | serious[0] | string | 감염 |
| `/modality/4/products/3/extracted/safety/serious/1` | serious[1] | string | 신경 손상 |
| `/modality/4/products/3/extracted/safety/serious/2` | serious[2] | string | 과도한 염증 |
| `/modality/4/products/3/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/4/products/3/extracted/onset_duration/onset` | onset | string | 2-3주 |
| `/modality/4/products/3/extracted/onset_duration/duration` | duration | string | 3-6개월 |
| `/modality/4/products/3/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/4/products/3/extracted/aftercare/0` | aftercare[0] | string | 주입 후 냉찜질 |
| `/modality/4/products/3/extracted/aftercare/1` | aftercare[1] | string | 1주일 자외선 차단 |
| `/modality/4/products/3/extracted/aftercare/2` | aftercare[2] | string | 음주·운동 제한 |
| `/modality/4/products/3/extracted/aftercare/3` | aftercare[3] | string | 비후성 반흔 위험군 주의 |
| `/modality/4/products/4` | products[4] | object | {object, 키 9: id, name, name_en, manufacturer, country, mfds, type, note, extracted} |
| `/modality/4/products/4/id` | id | string | M5-P-4 |
| `/modality/4/products/4/name` | name | string | EXOSOME SKIN |
| `/modality/4/products/4/name_en` | name_en | string | ExoSCRT |
| `/modality/4/products/4/manufacturer` | manufacturer | string | 엑소스템텍 |
| `/modality/4/products/4/country` | country | string | KR |
| `/modality/4/products/4/mfds` | mfds | boolean | false |
| `/modality/4/products/4/type` | type | string | 엑소좀 |
| `/modality/4/products/4/note` | note | string | 화장품 허가 |
| `/modality/4/products/4/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/4/products/4/extracted/overview` | overview | string | 엑소솜 기반 성장인자 전달 시스템 |
| `/modality/4/products/4/extracted/mechanism` | mechanism | string | 자가혈 유래 혹은 배양 성장인자를 엑소솜(세포외소포체)에 탑재하여 표적 세포로 전달. PDGF, TGF-β1, VEGF, EGF 등을 포함한 엑소솜이 진피층에 도달하여 섬유모세포 증식 및 콜라겐 생성 효율 극대화. |
| `/modality/4/products/4/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/4/products/4/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/4/products/4/extracted/indications/primary/0` | primary[0] | string | 피부 주름 |
| `/modality/4/products/4/extracted/indications/primary/1` | primary[1] | string | 피부 탄력 저하 |
| `/modality/4/products/4/extracted/indications/primary/2` | primary[2] | string | 광손상 |
| `/modality/4/products/4/extracted/indications/primary/3` | primary[3] | string | 탈모 |
| `/modality/4/products/4/extracted/indications/primary/4` | primary[4] | string | 피부 재생 |
| `/modality/4/products/4/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/4/products/4/extracted/safety/common` | common | array | [array, 원소 2] |
| `/modality/4/products/4/extracted/safety/common/0` | common[0] | string | 주입 부위 부종 |
| `/modality/4/products/4/extracted/safety/common/1` | common[1] | string | 발적 |
| `/modality/4/products/4/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/4/products/4/extracted/safety/serious/0` | serious[0] | string | 감염 |
| `/modality/4/products/4/extracted/safety/serious/1` | serious[1] | string | 이상 염증반응 |
| `/modality/4/products/4/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/4/products/4/extracted/onset_duration/onset` | onset | string | 3-4주 |
| `/modality/4/products/4/extracted/onset_duration/duration` | duration | string | 4-8개월 |
| `/modality/4/products/4/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/4/products/4/extracted/aftercare/0` | aftercare[0] | string | 주입 후 냉찜질 |
| `/modality/4/products/4/extracted/aftercare/1` | aftercare[1] | string | 1주일 자외선 차단 |
| `/modality/4/products/4/extracted/aftercare/2` | aftercare[2] | string | 음주·운동 제한 |
| `/modality/4/products/4/extracted/aftercare/3` | aftercare[3] | string | 정기적 후속 시술 권장 |
| `/modality/4/name` | name | string | PRP/자가혈 |

## 잠정 관찰 (원문 아님 · 직접 읽기 기록)

| 상태 | 근거 Pointer | 관찰 |
|---|---|---|
| P | `/modality/4/subcategories/2/label`, `/modality/4/subcategories/2/items/0/name`, `/modality/4/subcategories/3/label`, `/modality/4/subcategories/3/items/0/name` | 하위분류 label 과 항목 name 약어가 다르다: 'MCT (메타셀)' → 항목 'CPR', 'ACT' → 항목 'ACR'. 약어 풀이 없음(B). |
| P | `/modality/4/subcategories/0/items/0/detail` | PRP detail '원심분리 → 성장인자 농축 → 주입' — '→' 로 시술 절차 순서를 표기. |
| P | `/modality/4/subcategories/0/items/0/extracted/aftercare/3` | M5 상용구 '[시술 주기 참고] 1-3개월 간격, 2-3회 코스 권장 (스킨부스터에 준함). 효과 발현 4-8주. NSAIDs 자제 …' — 다른 모달리티(스킨부스터)를 참조하는 상용구. |
| I | `/modality/4/products/3/note`, `/modality/4/products/3/type`, `/modality/4/products/3/extracted/overview`, `/modality/4/products/3/extracted/aftercare/0` | ASCEplus: note '화장품 허가 (주사 사용 불법)', type '엑소좀' 인데 overview '자가혈 유래 성장인자 복합 제제', aftercare '주입 후 냉찜질', safety '주입 부위 통증'. 허가 상태 메모와 사용 서술이 충돌하고 성분 서술도 type 과 다르다. |
| I | `/modality/4/products/4/name`, `/modality/4/products/4/name_en`, `/modality/4/products/4/note` | EXOSOME SKIN name_en 'ExoSCRT' — name 과 영문명 불일치. note '화장품 허가' 인데 safety '주입 부위 부종'. |
| P | `/modality/4/products/0/type`, `/modality/4/products/3/type` | M5 products 에 type 필드(PRP키트, 엑소좀). M5 products 는 키트·화장품 허가 제제까지 포함. 엑소좀은 M4-3 하위분류에도 있다. |
| P | `/modality/4/extracted/safety/serious/0`, `/modality/4/extracted/safety/uncommon/0` | M5 모달리티 safety/serious 원소가 부작용이 아니라 안심 문구('알레르기·거부반응이 거의 없음 (매우 안전한 시술)'), uncommon 원소가 결과 편차 설명. 키 이름과 내용 종류 불일치. |
| P | `/modality/4/subcategories/1/items/0/extracted/indications/primary/2` | PRF indications 에 '질 주름 개선' — 안면 외 부위(여성 생식기) 적응증. 해석하지 않고 보존. |
| P | `/modality/4/products/2/extracted/aftercare/3` | 마이셀 aftercare '여성 환자는 높은 EGF/HGF 농도로 더 효과적' — 관리 지시가 아닌 효과 주장이 aftercare 에. |

## 수동 복합 표현 (원문 구간)

| Pointer | 구간 | 원문 표현 | 관점 | 메모 |
|---|---|---|---|---|
| `/modality/4/subcategories/0/items/0/extracted/overview` | [0, 24] | 자가혈액 혈소판 3-5배 농축 성장인자 치료 | 수량·단위·시간, 범위 | 배수 |
| `/modality/4/subcategories/0/items/0/extracted/mechanism` | [6, 37] | 혈소판을 3-5배 농축(≥1,000,000 plt/μL) | 수량·단위·시간, 범위, 기호 | ≥ 하한 |
| `/modality/4/subcategories/0/items/0/extracted/mechanism` | [80, 93] | 4000+ 단백질을 함유 | 수량·단위·시간, 기호 | '+' = 이상 |
| `/modality/4/subcategories/0/items/0/extracted/mechanism` | [95, 131] | 활성화 1시간 내 95% 성장인자 방출 후 7-10일간 추가 합성 | 수량·단위·시간, 범위 |  |
| `/modality/4/subcategories/0/items/0/extracted/safety/serious/1` | [0, 26] | TGF-beta1에 의한 비후성 반흔 촉진 가능 | 가능성·빈도, 조건 | β 대신 beta 표기 |
| `/modality/4/subcategories/0/items/0/extracted/safety/serious/2` | [0, 11] | 알레르기 반응(드묾) | 가능성·빈도 |  |
| `/modality/4/subcategories/0/items/0/extracted/aftercare/1` | [0, 24] | NSAIDs 사용 자제 (혈소판 기능 억제) | 부정, 조건 | 이유 괄호 |
| `/modality/4/subcategories/1/items/0/extracted/mechanism` | [54, 70] | 14-28일에 걸쳐 지속 방출 | 수량·단위·시간, 범위 |  |
| `/modality/4/subcategories/1/items/0/extracted/mechanism` | [72, 90] | PRP 대비 장시간 생체활성 유지 | 비교 |  |
| `/modality/4/subcategories/2/items/0/extracted/mechanism` | [73, 110] | I형 콜라겐 생성 능력을 4-6배 증강하고 MMP-1/3 발현 조절 | 수량·단위·시간, 범위, 기호 |  |
| `/modality/4/subcategories/2/items/0/extracted/aftercare/3` | [0, 21] | 비후성 반흔 위험군은 의료진 상담 필수 | 조건 |  |
| `/modality/4/subcategories/0/items/0/extracted/aftercare/3` | [32, 43] | (스킨부스터에 준함) | 참조, 비교 | 모달리티 간 참조 |
| `/modality/4/extracted/overview` | [79, 100] | 1987년 심장수술에서 처음 사용된 후 | 수량·단위·시간, 주장 |  |
| `/modality/4/extracted/overview` | [56, 75] | 피부에 주사하거나 바르는 재생 시술 | 조건 | 적용 방법 대안 |
| `/modality/4/extracted/indications/extended/3` | [0, 37] | 다른 시술과 병행 — MTS, 프랙셔널 레이저, 메조테라피 후 도포 | 참조, 시술·제품명 |  |
| `/modality/4/extracted/contraindications/relative/2` | [0, 22] | 색소성 질환에 대한 치료 효과는 적은 편 | 비교, 수식 | 금기 칸의 효과 진술 |
| `/modality/4/extracted/safety/common/1` | [0, 10] | 1~2일 정도 붓기 | 수량·단위·시간, 범위 |  |
| `/modality/4/extracted/safety/common/2` | [0, 17] | 3~7일 정도 멍이 들 수 있음 | 수량·단위·시간, 범위, 가능성·빈도 |  |
| `/modality/4/extracted/safety/serious/0` | [13, 41] | 알레르기·거부반응이 거의 없음 (매우 안전한 시술) | 부정, 주장 |  |
| `/modality/4/extracted/onset_duration/duration` | [0, 35] | 1회 시술로 6~12개월 유지 (반복시술은 4~6주 간격 가능) | 수량·단위·시간, 범위, 가능성·빈도 | 상용구 '1-3개월 간격' 과 다름 |
| `/modality/4/extracted/aftercare/2` | [0, 47] | 깊은 주름이나 심한 노화에는 고주파, IPL, 필러, 보톡스 등과 병행하는 것이 좋음 | 조건, 참조 |  |
| `/modality/4/extracted/related_techniques/0` | [0, 42] | MTS + PRP — MTS로 미세 구멍을 낸 후 PRP를 도포해 흡수 촉진 | 시술·제품명, 기호, 참조 | '+' = 함께(병행) |
| `/modality/4/products/3/note` | [0, 17] | 화장품 허가 (주사 사용 불법) | 주장, 부정 | 규제 주장 |
| `/modality/4/products/4/extracted/mechanism` | [0, 17] | 자가혈 유래 혹은 배양 성장인자 | 조건 | 대안 |
| `/modality/4/products/2/extracted/aftercare/3` | [0, 27] | 여성 환자는 높은 EGF/HGF 농도로 더 효과적 | 조건, 비교, 주장 |  |

## 형태소 분석 확인 (알려진 오분절 K)

| 범위 | 표면형 | 문제 | 영향 |
|---|---|---|---|
| all | 엑소솜 | '엑소솜'(다른 곳 '엑소좀') — 표기 변형. 분석 결과는 표기를 따른다 | 같은 성분명 두 표기 |

## 미결

| ID | 상태 | Pointer | 내용 | 영향·후속 |
|---|---|---|---|---|
| S014-I01 | I | `/modality/4/products/3/note`, `/modality/4/products/3/extracted/overview`, `/modality/4/products/3/type` | ASCEplus 허가 메모·type·서술 충돌. | 제품 정보 채택 시 확인 |
| S014-I02 | I | `/modality/4/products/4/name`, `/modality/4/products/4/name_en` | EXOSOME SKIN / ExoSCRT 이름 불일치. | 제품 식별 |
| S014-B01 | B | `/modality/4/subcategories/2/label`, `/modality/4/subcategories/3/label` | MCT·CPR·ACT·ACR 약어 정의 없음. | 하위분류·항목 의미 식별 제한 |

