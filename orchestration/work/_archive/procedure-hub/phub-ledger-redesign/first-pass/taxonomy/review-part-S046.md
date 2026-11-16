# S046 — M16 수액치료

- 읽기 상태: **read** · 마지막 읽은 Pointer `/modality/15/subcategories/2/items/2/extracted/aftercare/2`
- 단위: id, category, category_en, group, subcategories 컨테이너, M16-1 items/0, M16-1 items/1, M16-1 items/2, M16-1 items/3, M16-1 items/4, M16-1 items/5, M16-1 items/6, M16-2 items/0, M16-2 items/1, M16-2 items/2, M16-2 items/3, M16-2 items/4, M16-2 items/5, M16-2 items/6, M16-2 items/7, M16-3 items/0, M16-3 items/1, M16-3 items/2
- 상위 문맥(공동 참조·소유 아님): 없음
- 기계 기록: `source-map.json`(section=S046) · `morphology/S046.json` · `expressions.json`(section=S046) · 읽기 렌더 `reading/S046.txt`

## 원문 값 (원본 컬럼명 그대로, 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/modality/15` | modality[15] | object | {object, 키 8: id, category, category_en, group, subcategories, extracted, products, name} |
| `/modality/15/id` | id | string | M16 |
| `/modality/15/category` | category | string | 수액치료 |
| `/modality/15/category_en` | category_en | string | IV Therapy |
| `/modality/15/group` | group | string | 관리 |
| `/modality/15/subcategories` | subcategories | array | [array, 원소 7] |
| `/modality/15/subcategories/0` | subcategories[0] | object | {object, 키 3: id, label, items} |
| `/modality/15/subcategories/0/id` | id | string | M16-1 |
| `/modality/15/subcategories/0/label` | label | string | 미백/항산화 |
| `/modality/15/subcategories/0/items` | items | array | [array, 원소 7] |
| `/modality/15/subcategories/0/items/0` | items[0] | object | {object, 키 8: id, name, detail, is_marketing_name, ingredient_basis, canonical_category, naming_caveat, extracted} |
| `/modality/15/subcategories/0/items/0/id` | id | string | M16-1-1 |
| `/modality/15/subcategories/0/items/0/name` | name | string | 백옥주사 |
| `/modality/15/subcategories/0/items/0/detail` | detail | string | 마케팅 명칭 — 실제 성분은 글루타치온 IV |
| `/modality/15/subcategories/0/items/0/is_marketing_name` | is_marketing_name | boolean | true |
| `/modality/15/subcategories/0/items/0/ingredient_basis` | ingredient_basis | string | 환원형 글루타치온(GSH). 용량은 클리닉별로 상이(600-2,000mg 범위) |
| `/modality/15/subcategories/0/items/0/canonical_category` | canonical_category | string | M16 수액치료 > 항산화·미백 IV |
| `/modality/15/subcategories/0/items/0/naming_caveat` | naming_caveat | string | '하얗게 된다'는 효과 기반 마케팅명. 고용량 글루타치온 IV의 미백 효과는 제한된 임상 근거이며 FDA·식약처의 미백 목적 공식 허가 적응증 아님. 의료광고 표현 주의 필요 |
| `/modality/15/subcategories/0/items/0/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/15/subcategories/0/items/0/extracted/overview` | overview | string | 글루타치온 정맥주사로 항산화·미백 |
| `/modality/15/subcategories/0/items/0/extracted/mechanism` | mechanism | string | 글루타치온의 강력한 항산화 작용으로 활성산소 제거 및 멜라닌 합성 억제. 정맥주사를 통해 높은 생체이용률로 직접 혈류 전달되어 전신 항산화 효과 제공. |
| `/modality/15/subcategories/0/items/0/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/15/subcategories/0/items/0/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/15/subcategories/0/items/0/extracted/indications/primary/0` | primary[0] | string | 피부미백 |
| `/modality/15/subcategories/0/items/0/extracted/indications/primary/1` | primary[1] | string | 항산화 |
| `/modality/15/subcategories/0/items/0/extracted/indications/primary/2` | primary[2] | string | 피로개선 |
| `/modality/15/subcategories/0/items/0/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/15/subcategories/0/items/0/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/15/subcategories/0/items/0/extracted/safety/common/0` | common[0] | string | 주사 부위 통증 |
| `/modality/15/subcategories/0/items/0/extracted/safety/common/1` | common[1] | string | 일시적 어지러움 |
| `/modality/15/subcategories/0/items/0/extracted/safety/common/2` | common[2] | string | 소화불편 |
| `/modality/15/subcategories/0/items/0/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/15/subcategories/0/items/0/extracted/safety/serious/0` | serious[0] | string | 알레르기 반응 |
| `/modality/15/subcategories/0/items/0/extracted/safety/serious/1` | serious[1] | string | 아나필락시스 |
| `/modality/15/subcategories/0/items/0/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/15/subcategories/0/items/0/extracted/onset_duration/onset` | onset | string | 1-3일 |
| `/modality/15/subcategories/0/items/0/extracted/onset_duration/duration` | duration | string | 1-2주 |
| `/modality/15/subcategories/0/items/0/extracted/aftercare` | aftercare | array | [array, 원소 2] |
| `/modality/15/subcategories/0/items/0/extracted/aftercare/0` | aftercare[0] | string | 주사 후 2시간 음주 자제 |
| `/modality/15/subcategories/0/items/0/extracted/aftercare/1` | aftercare[1] | string | 정기적 시술로 효과 유지 |
| `/modality/15/subcategories/0/items/1` | items[1] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/15/subcategories/0/items/1/id` | id | string | M16-1-2 |
| `/modality/15/subcategories/0/items/1/name` | name | string | 고농도C |
| `/modality/15/subcategories/0/items/1/detail` | detail | string | 비타민C 메가도스 |
| `/modality/15/subcategories/0/items/1/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/15/subcategories/0/items/1/extracted/overview` | overview | string | 비타민C 메가도스 정맥주사 |
| `/modality/15/subcategories/0/items/1/extracted/mechanism` | mechanism | string | 고용량 비타민C의 강력한 항산화 작용으로 콜라겐 합성 촉진 및 활성산소 제거. 정맥주사를 통해 경구 투여 불가능한 고농도 도달로 피부 항노화 효과. |
| `/modality/15/subcategories/0/items/1/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/15/subcategories/0/items/1/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/15/subcategories/0/items/1/extracted/indications/primary/0` | primary[0] | string | 피부탄력 개선 |
| `/modality/15/subcategories/0/items/1/extracted/indications/primary/1` | primary[1] | string | 항노화 |
| `/modality/15/subcategories/0/items/1/extracted/indications/primary/2` | primary[2] | string | 항산화 |
| `/modality/15/subcategories/0/items/1/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/15/subcategories/0/items/1/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/15/subcategories/0/items/1/extracted/safety/common/0` | common[0] | string | 주사 부위 불편감 |
| `/modality/15/subcategories/0/items/1/extracted/safety/common/1` | common[1] | string | 일시적 소화불편 |
| `/modality/15/subcategories/0/items/1/extracted/safety/common/2` | common[2] | string | 두통 |
| `/modality/15/subcategories/0/items/1/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/15/subcategories/0/items/1/extracted/safety/serious/0` | serious[0] | string | 신장 결석(과다 투여 시) |
| `/modality/15/subcategories/0/items/1/extracted/safety/serious/1` | serious[1] | string | 용혈성 빈혈(G6PD 결핍자) |
| `/modality/15/subcategories/0/items/1/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/15/subcategories/0/items/1/extracted/onset_duration/onset` | onset | string | 3-7일 |
| `/modality/15/subcategories/0/items/1/extracted/onset_duration/duration` | duration | string | 2-3주 |
| `/modality/15/subcategories/0/items/1/extracted/aftercare` | aftercare | array | [array, 원소 2] |
| `/modality/15/subcategories/0/items/1/extracted/aftercare/0` | aftercare[0] | string | 충분한 수분섭취 |
| `/modality/15/subcategories/0/items/1/extracted/aftercare/1` | aftercare[1] | string | 신기능 정상 확인 후 시술 |
| `/modality/15/subcategories/0/items/2` | items[2] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/15/subcategories/0/items/2/id` | id | string | auto-55-1774737181584 |
| `/modality/15/subcategories/0/items/2/name` | name | string | 셀디톡스수액 |
| `/modality/15/subcategories/0/items/2/detail` | detail | string | 해독·항산화 |
| `/modality/15/subcategories/0/items/2/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/15/subcategories/0/items/2/extracted/overview` | overview | string | 해독·항산화 성분 복합 수액 |
| `/modality/15/subcategories/0/items/2/extracted/mechanism` | mechanism | string | 항산화제 및 간 해독 성분의 복합작용으로 활성산소 제거 및 체내 독소 배출 촉진. 정맥주사를 통해 높은 생체이용률로 전신 해독·항산화 효과 제공. |
| `/modality/15/subcategories/0/items/2/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/15/subcategories/0/items/2/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/15/subcategories/0/items/2/extracted/indications/primary/0` | primary[0] | string | 피로회복 |
| `/modality/15/subcategories/0/items/2/extracted/indications/primary/1` | primary[1] | string | 면역력 강화 |
| `/modality/15/subcategories/0/items/2/extracted/indications/primary/2` | primary[2] | string | 피부개선 |
| `/modality/15/subcategories/0/items/2/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/15/subcategories/0/items/2/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/15/subcategories/0/items/2/extracted/safety/common/0` | common[0] | string | 주사 부위 통증 |
| `/modality/15/subcategories/0/items/2/extracted/safety/common/1` | common[1] | string | 일시적 어지러움 |
| `/modality/15/subcategories/0/items/2/extracted/safety/common/2` | common[2] | string | 메스꺼움 |
| `/modality/15/subcategories/0/items/2/extracted/safety/serious` | serious | array | [array, 원소 1] |
| `/modality/15/subcategories/0/items/2/extracted/safety/serious/0` | serious[0] | string | 알레르기 반응 |
| `/modality/15/subcategories/0/items/2/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/15/subcategories/0/items/2/extracted/onset_duration/onset` | onset | string | 즉시~1일 |
| `/modality/15/subcategories/0/items/2/extracted/onset_duration/duration` | duration | string | 3-7일 |
| `/modality/15/subcategories/0/items/2/extracted/aftercare` | aftercare | array | [array, 원소 2] |
| `/modality/15/subcategories/0/items/2/extracted/aftercare/0` | aftercare[0] | string | 충분한 수분섭취 |
| `/modality/15/subcategories/0/items/2/extracted/aftercare/1` | aftercare[1] | string | 알코올 섭취 제한 |
| `/modality/15/subcategories/0/items/3` | items[3] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/15/subcategories/0/items/3/id` | id | string | auto-M16-1775362661625 |
| `/modality/15/subcategories/0/items/3/name` | name | string | 알파리포산주사 |
| `/modality/15/subcategories/0/items/3/detail` | detail | string | 항산화 · 당대사 개선 · 신데렐라주사 성분 |
| `/modality/15/subcategories/0/items/3/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/15/subcategories/0/items/3/extracted/overview` | overview | string | 강력한 항산화 작용으로 세포 재생을 촉진하고 피부 개선 효과를 제공하는 미용 주사 |
| `/modality/15/subcategories/0/items/3/extracted/mechanism` | mechanism | string | 세포 내 미토콘드리아에서 에너지 대사를 활성화하고 활성산소를 제거합니다. 당대사 개선을 통해 피부 세포의 재생력을 높이고 콜라겐 합성을 촉진합니다. |
| `/modality/15/subcategories/0/items/3/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/15/subcategories/0/items/3/extracted/indications/primary` | primary | array | [array, 원소 2] |
| `/modality/15/subcategories/0/items/3/extracted/indications/primary/0` | primary[0] | string | 피부 톤 개선 및 미백 |
| `/modality/15/subcategories/0/items/3/extracted/indications/primary/1` | primary[1] | string | 피로 개선 및 항노화 |
| `/modality/15/subcategories/0/items/3/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/15/subcategories/0/items/3/extracted/safety/common` | common | array | [array, 원소 1] |
| `/modality/15/subcategories/0/items/3/extracted/safety/common/0` | common[0] | string | 주사 부위 일시적 통증 |
| `/modality/15/subcategories/0/items/3/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/15/subcategories/0/items/3/extracted/onset_duration/onset` | onset | string | 24-48시간 |
| `/modality/15/subcategories/0/items/3/extracted/onset_duration/duration` | duration | string | 2-4주 |
| `/modality/15/subcategories/0/items/3/extracted/aftercare` | aftercare | array | [array, 원소 2] |
| `/modality/15/subcategories/0/items/3/extracted/aftercare/0` | aftercare[0] | string | 충분한 수분 섭취 |
| `/modality/15/subcategories/0/items/3/extracted/aftercare/1` | aftercare[1] | string | 음주 자제 24시간 |
| `/modality/15/subcategories/0/items/4` | items[4] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/15/subcategories/0/items/4/id` | id | string | auto-M16-1775364775092 |
| `/modality/15/subcategories/0/items/4/name` | name | string | 멀티비타민수액 |
| `/modality/15/subcategories/0/items/4/detail` | detail | string | B1/B2/B6/B12/C |
| `/modality/15/subcategories/0/items/4/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/15/subcategories/0/items/4/extracted/overview` | overview | string | 필수 비타민 B군과 C를 조합한 정맥 수액 치료 |
| `/modality/15/subcategories/0/items/4/extracted/mechanism` | mechanism | string | 비타민 B군은 에너지 대사와 신경 기능을 지원합니다. 비타민 C는 콜라겐 합성과 항산화 작용을 통해 피부 건강을 개선합니다. |
| `/modality/15/subcategories/0/items/4/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/15/subcategories/0/items/4/extracted/indications/primary` | primary | array | [array, 원소 2] |
| `/modality/15/subcategories/0/items/4/extracted/indications/primary/0` | primary[0] | string | 피로 회복 |
| `/modality/15/subcategories/0/items/4/extracted/indications/primary/1` | primary[1] | string | 피부 톤 개선 |
| `/modality/15/subcategories/0/items/4/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/15/subcategories/0/items/4/extracted/safety/common` | common | array | [array, 원소 1] |
| `/modality/15/subcategories/0/items/4/extracted/safety/common/0` | common[0] | string | 주사 부위 경미한 통증 |
| `/modality/15/subcategories/0/items/4/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/15/subcategories/0/items/4/extracted/onset_duration/onset` | onset | string | 당일-3일 |
| `/modality/15/subcategories/0/items/4/extracted/onset_duration/duration` | duration | string | 1-2주 |
| `/modality/15/subcategories/0/items/4/extracted/aftercare` | aftercare | array | [array, 원소 2] |
| `/modality/15/subcategories/0/items/4/extracted/aftercare/0` | aftercare[0] | string | 충분한 수분 섭취 |
| `/modality/15/subcategories/0/items/4/extracted/aftercare/1` | aftercare[1] | string | 시술 부위 강한 압박 자제 |
| `/modality/15/subcategories/0/items/5` | items[5] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/15/subcategories/0/items/5/id` | id | string | auto-M16-1775364775093 |
| `/modality/15/subcategories/0/items/5/name` | name | string | 비타민D주사 |
| `/modality/15/subcategories/0/items/5/detail` | detail | string | 콜레칼시페롤 |
| `/modality/15/subcategories/0/items/5/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/15/subcategories/0/items/5/extracted/overview` | overview | string | 비타민D3 고용량 근육주사를 통한 결핍 교정 |
| `/modality/15/subcategories/0/items/5/extracted/mechanism` | mechanism | string | 콜레칼시페롤이 간과 신장에서 활성형 비타민D로 변환됩니다. 칼슘 흡수 촉진과 면역 기능 조절을 통해 전신 건강을 개선합니다. |
| `/modality/15/subcategories/0/items/5/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/15/subcategories/0/items/5/extracted/indications/primary` | primary | array | [array, 원소 2] |
| `/modality/15/subcategories/0/items/5/extracted/indications/primary/0` | primary[0] | string | 비타민D 결핍 |
| `/modality/15/subcategories/0/items/5/extracted/indications/primary/1` | primary[1] | string | 면역력 저하 |
| `/modality/15/subcategories/0/items/5/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/15/subcategories/0/items/5/extracted/safety/common` | common | array | [array, 원소 1] |
| `/modality/15/subcategories/0/items/5/extracted/safety/common/0` | common[0] | string | 주사 부위 근육통 |
| `/modality/15/subcategories/0/items/5/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/15/subcategories/0/items/5/extracted/onset_duration/onset` | onset | string | 1-2주 |
| `/modality/15/subcategories/0/items/5/extracted/onset_duration/duration` | duration | string | 2-3개월 |
| `/modality/15/subcategories/0/items/5/extracted/aftercare` | aftercare | array | [array, 원소 2] |
| `/modality/15/subcategories/0/items/5/extracted/aftercare/0` | aftercare[0] | string | 주사 후 충분한 휴식 |
| `/modality/15/subcategories/0/items/5/extracted/aftercare/1` | aftercare[1] | string | 혈중 농도 추적 검사 |
| `/modality/15/subcategories/0/items/6` | items[6] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/15/subcategories/0/items/6/id` | id | string | auto-M16-1775402736447 |
| `/modality/15/subcategories/0/items/6/name` | name | string | 스노우주사 |
| `/modality/15/subcategories/0/items/6/detail` | detail | string | 글루타치온+트라넥삼산 |
| `/modality/15/subcategories/0/items/6/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/15/subcategories/0/items/6/extracted/overview` | overview | string | 글루타치온과 트라넥삼산을 조합한 미백 수액으로 전신 미백과 항산화 효과를 제공 |
| `/modality/15/subcategories/0/items/6/extracted/mechanism` | mechanism | string | 글루타치온의 항산화와 멜라닌 합성 억제, 트라넥삼산의 미백 효과로 피부 톤 개선 |
| `/modality/15/subcategories/0/items/6/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/15/subcategories/0/items/6/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/15/subcategories/0/items/6/extracted/indications/primary/0` | primary[0] | string | 전신 미백 |
| `/modality/15/subcategories/0/items/6/extracted/indications/primary/1` | primary[1] | string | 색소침착 |
| `/modality/15/subcategories/0/items/6/extracted/indications/primary/2` | primary[2] | string | 간 해독 |
| `/modality/15/subcategories/0/items/6/extracted/indications/primary/3` | primary[3] | string | 피로 회복 |
| `/modality/15/subcategories/0/items/6/extracted/indications/primary/4` | primary[4] | string | 항산화 |
| `/modality/15/subcategories/0/items/6/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/15/subcategories/0/items/6/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/15/subcategories/0/items/6/extracted/safety/common/0` | common[0] | string | 주사 부위 통증 |
| `/modality/15/subcategories/0/items/6/extracted/safety/common/1` | common[1] | string | 일시적 어지러움 |
| `/modality/15/subcategories/0/items/6/extracted/safety/common/2` | common[2] | string | 알레르기 반응 가능 |
| `/modality/15/subcategories/0/items/6/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/15/subcategories/0/items/6/extracted/onset_duration/onset` | onset | string | 2-4주 |
| `/modality/15/subcategories/0/items/6/extracted/onset_duration/duration` | duration | string | 2-3개월 |
| `/modality/15/subcategories/0/items/6/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/15/subcategories/0/items/6/extracted/aftercare/0` | aftercare[0] | string | 충분한 수분 섭취 |
| `/modality/15/subcategories/0/items/6/extracted/aftercare/1` | aftercare[1] | string | 금주 24시간 |
| `/modality/15/subcategories/0/items/6/extracted/aftercare/2` | aftercare[2] | string | 운전 주의 |
| `/modality/15/subcategories/0/items/6/extracted/aftercare/3` | aftercare[3] | string | 알레르기 관찰 |
| `/modality/15/subcategories/1` | subcategories[1] | object | {object, 키 3: id, label, items} |
| `/modality/15/subcategories/1/id` | id | string | M16-2 |
| `/modality/15/subcategories/1/label` | label | string | 피로회복 |
| `/modality/15/subcategories/1/items` | items | array | [array, 원소 8] |
| `/modality/15/subcategories/1/items/0` | items[0] | object | {object, 키 8: id, name, detail, is_marketing_name, ingredient_basis, canonical_category, naming_caveat, extracted} |
| `/modality/15/subcategories/1/items/0/id` | id | string | M16-2-1 |
| `/modality/15/subcategories/1/items/0/name` | name | string | 마늘주사 |
| `/modality/15/subcategories/1/items/0/detail` | detail | string | 마케팅 명칭 — 실제 성분은 비타민 B1(푸르설티아민 등) |
| `/modality/15/subcategories/1/items/0/is_marketing_name` | is_marketing_name | boolean | true |
| `/modality/15/subcategories/1/items/0/ingredient_basis` | ingredient_basis | string | 푸르설티아민(fursultiamine) 등 지용성 B1 유도체. 주사 후 일시적 마늘향 체취가 이름의 유래 |
| `/modality/15/subcategories/1/items/0/canonical_category` | canonical_category | string | M16 수액치료 > 비타민 B 계열 |
| `/modality/15/subcategories/1/items/0/naming_caveat` | naming_caveat | string | '마늘'은 주사 후 특유의 체취에서 유래한 마케팅명이며 실제 마늘 추출물이 아님. 피로 개선 효능은 대체적이며 식약처 허가 적응증 확인 필요 |
| `/modality/15/subcategories/1/items/0/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/15/subcategories/1/items/0/extracted/overview` | overview | string | 비타민B1 복합 피로회복 주사 |
| `/modality/15/subcategories/1/items/0/extracted/mechanism` | mechanism | string | 비타민B1과 마늘 추출물의 협력작용으로 탄수화물 대사 촉진 및 에너지 생성 활성화. 정맥주사를 통해 빠른 흡수로 급성 피로 회복 및 신경 기능 개선. |
| `/modality/15/subcategories/1/items/0/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/15/subcategories/1/items/0/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/15/subcategories/1/items/0/extracted/indications/primary/0` | primary[0] | string | 피로회복 |
| `/modality/15/subcategories/1/items/0/extracted/indications/primary/1` | primary[1] | string | 신진대사 촉진 |
| `/modality/15/subcategories/1/items/0/extracted/indications/primary/2` | primary[2] | string | 에너지 부스트 |
| `/modality/15/subcategories/1/items/0/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/15/subcategories/1/items/0/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/15/subcategories/1/items/0/extracted/safety/common/0` | common[0] | string | 마늘 냄새 입냄새 |
| `/modality/15/subcategories/1/items/0/extracted/safety/common/1` | common[1] | string | 일시적 소화불편 |
| `/modality/15/subcategories/1/items/0/extracted/safety/common/2` | common[2] | string | 주사 부위 통증 |
| `/modality/15/subcategories/1/items/0/extracted/safety/serious` | serious | array | [array, 원소 1] |
| `/modality/15/subcategories/1/items/0/extracted/safety/serious/0` | serious[0] | string | 알레르기 반응 |
| `/modality/15/subcategories/1/items/0/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/15/subcategories/1/items/0/extracted/onset_duration/onset` | onset | string | 즉시~수 시간 |
| `/modality/15/subcategories/1/items/0/extracted/onset_duration/duration` | duration | string | 3-5일 |
| `/modality/15/subcategories/1/items/0/extracted/aftercare` | aftercare | array | [array, 원소 2] |
| `/modality/15/subcategories/1/items/0/extracted/aftercare/0` | aftercare[0] | string | 과도한 운동 제한(24시간) |
| `/modality/15/subcategories/1/items/0/extracted/aftercare/1` | aftercare[1] | string | 충분한 수면 |
| `/modality/15/subcategories/1/items/1` | items[1] | object | {object, 키 8: id, name, detail, is_marketing_name, ingredient_basis, canonical_category, naming_caveat, extracted} |
| `/modality/15/subcategories/1/items/1/id` | id | string | M16-2-2 |
| `/modality/15/subcategories/1/items/1/name` | name | string | 신데렐라주사 |
| `/modality/15/subcategories/1/items/1/detail` | detail | string | 마케팅 명칭 — 실제 성분은 알파리포산(ALA) |
| `/modality/15/subcategories/1/items/1/is_marketing_name` | is_marketing_name | boolean | true |
| `/modality/15/subcategories/1/items/1/ingredient_basis` | ingredient_basis | string | 알파리포산(alpha-lipoic acid). 용량은 클리닉별 상이 |
| `/modality/15/subcategories/1/items/1/canonical_category` | canonical_category | string | M16 수액치료 > 항산화 IV |
| `/modality/15/subcategories/1/items/1/naming_caveat` | naming_caveat | string | '신데렐라처럼 예뻐진다'는 효과 연상 마케팅명. 알파리포산의 미용·피부 효과는 제한적 근거이며 당뇨병성 신경병증 등 일부 적응증 외에는 공식 미용 허가 아님 |
| `/modality/15/subcategories/1/items/1/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/15/subcategories/1/items/1/extracted/overview` | overview | string | 알파리포산 항노화·대사촉진 주사 |
| `/modality/15/subcategories/1/items/1/extracted/mechanism` | mechanism | string | 알파리포산의 강력한 항산화 작용으로 활성산소 제거 및 미토콘드리아 에너지 생성 촉진. 정맥주사를 통해 세포 대사 활성화 및 피부 항노화 효과 동시 달성. |
| `/modality/15/subcategories/1/items/1/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/15/subcategories/1/items/1/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/15/subcategories/1/items/1/extracted/indications/primary/0` | primary[0] | string | 항노화 |
| `/modality/15/subcategories/1/items/1/extracted/indications/primary/1` | primary[1] | string | 피부탄력 개선 |
| `/modality/15/subcategories/1/items/1/extracted/indications/primary/2` | primary[2] | string | 체내 에너지 촉진 |
| `/modality/15/subcategories/1/items/1/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/15/subcategories/1/items/1/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/15/subcategories/1/items/1/extracted/safety/common/0` | common[0] | string | 주사 부위 통증 |
| `/modality/15/subcategories/1/items/1/extracted/safety/common/1` | common[1] | string | 일시적 저혈당 |
| `/modality/15/subcategories/1/items/1/extracted/safety/common/2` | common[2] | string | 두통 |
| `/modality/15/subcategories/1/items/1/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/15/subcategories/1/items/1/extracted/safety/serious/0` | serious[0] | string | 알레르기 반응 |
| `/modality/15/subcategories/1/items/1/extracted/safety/serious/1` | serious[1] | string | 심한 저혈당(당뇨약 병용 시) |
| `/modality/15/subcategories/1/items/1/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/15/subcategories/1/items/1/extracted/onset_duration/onset` | onset | string | 1-3일 |
| `/modality/15/subcategories/1/items/1/extracted/onset_duration/duration` | duration | string | 1-2주 |
| `/modality/15/subcategories/1/items/1/extracted/aftercare` | aftercare | array | [array, 원소 2] |
| `/modality/15/subcategories/1/items/1/extracted/aftercare/0` | aftercare[0] | string | 공복 피하기 |
| `/modality/15/subcategories/1/items/1/extracted/aftercare/1` | aftercare[1] | string | 당뇨약 복용자 의료진 상담 필수 |
| `/modality/15/subcategories/1/items/2` | items[2] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/15/subcategories/1/items/2/id` | id | string | auto-56-1774737181584 |
| `/modality/15/subcategories/1/items/2/name` | name | string | 에너지부스트수액 |
| `/modality/15/subcategories/1/items/2/detail` | detail | string | 피로회복 |
| `/modality/15/subcategories/1/items/2/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/15/subcategories/1/items/2/extracted/overview` | overview | string | 비타민·미네랄 복합 피로회복 수액 |
| `/modality/15/subcategories/1/items/2/extracted/mechanism` | mechanism | string | 비타민B군, 미네랄, 항산화제의 복합작용으로 세포 에너지 생성 촉진 및 피로물질 제거. 정맥주사를 통해 높은 생체이용률로 빠른 피로회복 및 신진대사 활성화. |
| `/modality/15/subcategories/1/items/2/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/15/subcategories/1/items/2/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/15/subcategories/1/items/2/extracted/indications/primary/0` | primary[0] | string | 피로회복 |
| `/modality/15/subcategories/1/items/2/extracted/indications/primary/1` | primary[1] | string | 신진대사 촉진 |
| `/modality/15/subcategories/1/items/2/extracted/indications/primary/2` | primary[2] | string | 스트레스 해소 |
| `/modality/15/subcategories/1/items/2/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/15/subcategories/1/items/2/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/15/subcategories/1/items/2/extracted/safety/common/0` | common[0] | string | 주사 부위 불편감 |
| `/modality/15/subcategories/1/items/2/extracted/safety/common/1` | common[1] | string | 일시적 어지러움 |
| `/modality/15/subcategories/1/items/2/extracted/safety/common/2` | common[2] | string | 메스꺼움 |
| `/modality/15/subcategories/1/items/2/extracted/safety/serious` | serious | array | [array, 원소 1] |
| `/modality/15/subcategories/1/items/2/extracted/safety/serious/0` | serious[0] | string | 알레르기 반응 |
| `/modality/15/subcategories/1/items/2/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/15/subcategories/1/items/2/extracted/onset_duration/onset` | onset | string | 즉시~수 시간 |
| `/modality/15/subcategories/1/items/2/extracted/onset_duration/duration` | duration | string | 3-7일 |
| `/modality/15/subcategories/1/items/2/extracted/aftercare` | aftercare | array | [array, 원소 2] |
| `/modality/15/subcategories/1/items/2/extracted/aftercare/0` | aftercare[0] | string | 충분한 수분섭취 |
| `/modality/15/subcategories/1/items/2/extracted/aftercare/1` | aftercare[1] | string | 과도한 운동 제한(24시간) |
| `/modality/15/subcategories/1/items/3` | items[3] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/15/subcategories/1/items/3/id` | id | string | auto-57-1774737181584 |
| `/modality/15/subcategories/1/items/3/name` | name | string | 아르기닌주사 |
| `/modality/15/subcategories/1/items/3/detail` | detail | string | 혈류개선·체력회복 |
| `/modality/15/subcategories/1/items/3/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/15/subcategories/1/items/3/extracted/overview` | overview | string | 아미노산 혈류개선·면역강화 주사 |
| `/modality/15/subcategories/1/items/3/extracted/mechanism` | mechanism | string | 아르기닌의 일산화질소(NO) 생성 촉진으로 혈관 이완 및 혈류 개선. 정맥주사를 통해 직접 혈류 전달로 빠른 혈류 개선, 조직 산소공급 증가 및 체력 회복 촉진. |
| `/modality/15/subcategories/1/items/3/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/15/subcategories/1/items/3/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/15/subcategories/1/items/3/extracted/indications/primary/0` | primary[0] | string | 혈류개선 |
| `/modality/15/subcategories/1/items/3/extracted/indications/primary/1` | primary[1] | string | 체력회복 |
| `/modality/15/subcategories/1/items/3/extracted/indications/primary/2` | primary[2] | string | 면역강화 |
| `/modality/15/subcategories/1/items/3/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/15/subcategories/1/items/3/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/15/subcategories/1/items/3/extracted/safety/common/0` | common[0] | string | 주사 부위 통증 |
| `/modality/15/subcategories/1/items/3/extracted/safety/common/1` | common[1] | string | 일시적 혈압저하 |
| `/modality/15/subcategories/1/items/3/extracted/safety/common/2` | common[2] | string | 메스꺼움 |
| `/modality/15/subcategories/1/items/3/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/15/subcategories/1/items/3/extracted/safety/serious/0` | serious[0] | string | 저혈압 |
| `/modality/15/subcategories/1/items/3/extracted/safety/serious/1` | serious[1] | string | 헤르페스 재활성화 |
| `/modality/15/subcategories/1/items/3/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/15/subcategories/1/items/3/extracted/onset_duration/onset` | onset | string | 1-2일 |
| `/modality/15/subcategories/1/items/3/extracted/onset_duration/duration` | duration | string | 1-2주 |
| `/modality/15/subcategories/1/items/3/extracted/aftercare` | aftercare | array | [array, 원소 2] |
| `/modality/15/subcategories/1/items/3/extracted/aftercare/0` | aftercare[0] | string | 혈압 저하자 의료진 상담 |
| `/modality/15/subcategories/1/items/3/extracted/aftercare/1` | aftercare[1] | string | 충분한 수면 |
| `/modality/15/subcategories/1/items/4` | items[4] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/15/subcategories/1/items/4/id` | id | string | auto-M16-1775362647500 |
| `/modality/15/subcategories/1/items/4/name` | name | string | 징크주사 |
| `/modality/15/subcategories/1/items/4/detail` | detail | string | 아연 · 면역/피부재생 |
| `/modality/15/subcategories/1/items/4/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/15/subcategories/1/items/4/extracted/overview` | overview | string | 아연을 정맥 또는 근육 주사로 투여하여 면역력 강화와 피부 재생을 촉진하는 미용의학 시술 |
| `/modality/15/subcategories/1/items/4/extracted/mechanism` | mechanism | string | 아연이 콜라겐 합성과 단백질 대사에 필수적인 보조인자로 작용하여 상처 치유와 피부 재생을 촉진합니다. 또한 항산화 효소의 활성을 높이고 면역세포 기능을 강화하여 전반적인 피부 건강을 개선합니다. |
| `/modality/15/subcategories/1/items/4/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/15/subcategories/1/items/4/extracted/indications/primary` | primary | array | [array, 원소 2] |
| `/modality/15/subcategories/1/items/4/extracted/indications/primary/0` | primary[0] | string | 상처 치유 지연 및 피부 재생 촉진 |
| `/modality/15/subcategories/1/items/4/extracted/indications/primary/1` | primary[1] | string | 면역력 저하로 인한 피부 트러블 개선 |
| `/modality/15/subcategories/1/items/4/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/15/subcategories/1/items/4/extracted/safety/common` | common | array | [array, 원소 1] |
| `/modality/15/subcategories/1/items/4/extracted/safety/common/0` | common[0] | string | 주사 부위 통증 및 부종 |
| `/modality/15/subcategories/1/items/4/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/15/subcategories/1/items/4/extracted/onset_duration/onset` | onset | string | 2-4주 |
| `/modality/15/subcategories/1/items/4/extracted/onset_duration/duration` | duration | string | 4-8주 |
| `/modality/15/subcategories/1/items/4/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/15/subcategories/1/items/4/extracted/aftercare/0` | aftercare[0] | string | 주사 부위 청결 유지 및 과도한 자극 피하기 |
| `/modality/15/subcategories/1/items/4/extracted/aftercare/1` | aftercare[1] | string | 주사 부위 압박 수분간 |
| `/modality/15/subcategories/1/items/4/extracted/aftercare/2` | aftercare[2] | string | 충분한 수분 섭취 |
| `/modality/15/subcategories/1/items/5` | items[5] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/15/subcategories/1/items/5/id` | id | string | auto-M16-1775362656075 |
| `/modality/15/subcategories/1/items/5/name` | name | string | 비오틴주사 |
| `/modality/15/subcategories/1/items/5/detail` | detail | string | 비타민H · 모발/피부/손톱 |
| `/modality/15/subcategories/1/items/5/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/15/subcategories/1/items/5/extracted/overview` | overview | string | 모발, 피부, 손톱 건강 개선을 위한 비타민H(비오틴) 정맥주사 요법 |
| `/modality/15/subcategories/1/items/5/extracted/mechanism` | mechanism | string | 케라틴 합성에 필수적인 조효소 역할을 하여 모발과 손톱의 구조적 강도를 향상시킵니다. 지방산 합성과 아미노산 대사를 촉진하여 피부 세포 재생과 보습 기능을 개선합니다. |
| `/modality/15/subcategories/1/items/5/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/15/subcategories/1/items/5/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/15/subcategories/1/items/5/extracted/indications/primary/0` | primary[0] | string | 모발 탈모 및 모발 가늘어짐 |
| `/modality/15/subcategories/1/items/5/extracted/indications/primary/1` | primary[1] | string | 손톱 약화 및 갈라짐 |
| `/modality/15/subcategories/1/items/5/extracted/indications/primary/2` | primary[2] | string | 피부 건조 및 거칠음 |
| `/modality/15/subcategories/1/items/5/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/15/subcategories/1/items/5/extracted/safety/common` | common | array | [array, 원소 2] |
| `/modality/15/subcategories/1/items/5/extracted/safety/common/0` | common[0] | string | 주사 부위 경미한 통증 |
| `/modality/15/subcategories/1/items/5/extracted/safety/common/1` | common[1] | string | 일시적 소화불량 |
| `/modality/15/subcategories/1/items/5/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/15/subcategories/1/items/5/extracted/onset_duration/onset` | onset | string | 4-6주 |
| `/modality/15/subcategories/1/items/5/extracted/onset_duration/duration` | duration | string | 2-3개월 |
| `/modality/15/subcategories/1/items/5/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/15/subcategories/1/items/5/extracted/aftercare/0` | aftercare[0] | string | 충분한 수분 섭취 |
| `/modality/15/subcategories/1/items/5/extracted/aftercare/1` | aftercare[1] | string | 균형잡힌 단백질 식단 유지 |
| `/modality/15/subcategories/1/items/5/extracted/aftercare/2` | aftercare[2] | string | 과도한 열 스타일링 피하기 |
| `/modality/15/subcategories/1/items/6` | items[6] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/15/subcategories/1/items/6/id` | id | string | auto-M16-1775364775090 |
| `/modality/15/subcategories/1/items/6/name` | name | string | 마이어스칵테일 |
| `/modality/15/subcategories/1/items/6/detail` | detail | string | Mg+Ca+B/C 복합수액 |
| `/modality/15/subcategories/1/items/6/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/15/subcategories/1/items/6/extracted/overview` | overview | string | 마그네슘, 칼슘, 비타민 B/C 복합 정맥 수액 치료 |
| `/modality/15/subcategories/1/items/6/extracted/mechanism` | mechanism | string | 마그네슘과 칼슘이 근육 이완과 신경 전달을 조절합니다. 비타민 B/C 복합체가 에너지 생성과 항산화 작용을 통해 전신 컨디션을 개선합니다. |
| `/modality/15/subcategories/1/items/6/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/15/subcategories/1/items/6/extracted/indications/primary` | primary | array | [array, 원소 2] |
| `/modality/15/subcategories/1/items/6/extracted/indications/primary/0` | primary[0] | string | 만성피로 |
| `/modality/15/subcategories/1/items/6/extracted/indications/primary/1` | primary[1] | string | 스트레스성 피부 트러블 |
| `/modality/15/subcategories/1/items/6/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/15/subcategories/1/items/6/extracted/safety/common` | common | array | [array, 원소 1] |
| `/modality/15/subcategories/1/items/6/extracted/safety/common/0` | common[0] | string | 수액 주입 중 혈관 따끔함 |
| `/modality/15/subcategories/1/items/6/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/15/subcategories/1/items/6/extracted/onset_duration/onset` | onset | string | 당일-1주 |
| `/modality/15/subcategories/1/items/6/extracted/onset_duration/duration` | duration | string | 2-4주 |
| `/modality/15/subcategories/1/items/6/extracted/aftercare` | aftercare | array | [array, 원소 2] |
| `/modality/15/subcategories/1/items/6/extracted/aftercare/0` | aftercare[0] | string | 수액 후 충분한 휴식 |
| `/modality/15/subcategories/1/items/6/extracted/aftercare/1` | aftercare[1] | string | 알코올 섭취 자제 |
| `/modality/15/subcategories/1/items/7` | items[7] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/15/subcategories/1/items/7/id` | id | string | auto-M16-1775364775091 |
| `/modality/15/subcategories/1/items/7/name` | name | string | 종합아미노산수액 |
| `/modality/15/subcategories/1/items/7/detail` | detail | string | 필수아미노산 20종 |
| `/modality/15/subcategories/1/items/7/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/15/subcategories/1/items/7/extracted/overview` | overview | string | 인체 필수 아미노산 20종을 포함한 종합 정맥 수액 |
| `/modality/15/subcategories/1/items/7/extracted/mechanism` | mechanism | string | 필수 아미노산들이 단백질 합성의 기본 재료로 사용됩니다. 콜라겐 생성 촉진과 세포 재생을 통해 피부 탄력과 회복력을 개선합니다. |
| `/modality/15/subcategories/1/items/7/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/15/subcategories/1/items/7/extracted/indications/primary` | primary | array | [array, 원소 2] |
| `/modality/15/subcategories/1/items/7/extracted/indications/primary/0` | primary[0] | string | 피부 탄력 저하 |
| `/modality/15/subcategories/1/items/7/extracted/indications/primary/1` | primary[1] | string | 회복 지연 |
| `/modality/15/subcategories/1/items/7/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/15/subcategories/1/items/7/extracted/safety/common` | common | array | [array, 원소 1] |
| `/modality/15/subcategories/1/items/7/extracted/safety/common/0` | common[0] | string | 수액 주입 중 팔 무거움 |
| `/modality/15/subcategories/1/items/7/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/15/subcategories/1/items/7/extracted/onset_duration/onset` | onset | string | 3-7일 |
| `/modality/15/subcategories/1/items/7/extracted/onset_duration/duration` | duration | string | 3-6주 |
| `/modality/15/subcategories/1/items/7/extracted/aftercare` | aftercare | array | [array, 원소 2] |
| `/modality/15/subcategories/1/items/7/extracted/aftercare/0` | aftercare[0] | string | 단백질 식품 함께 섭취 |
| `/modality/15/subcategories/1/items/7/extracted/aftercare/1` | aftercare[1] | string | 충분한 수면 |
| `/modality/15/subcategories/2` | subcategories[2] | object | {object, 키 3: id, label, items} |
| `/modality/15/subcategories/2/id` | id | string | M16-3 |
| `/modality/15/subcategories/2/label` | label | string | 재생/면역 |
| `/modality/15/subcategories/2/items` | items | array | [array, 원소 9] |
| `/modality/15/subcategories/2/items/0` | items[0] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/15/subcategories/2/items/0/id` | id | string | M16-3-1 |
| `/modality/15/subcategories/2/items/0/name` | name | string | 태반주사(라엔넥) |
| `/modality/15/subcategories/2/items/0/detail` | detail | string | 인태반 추출물 |
| `/modality/15/subcategories/2/items/0/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/15/subcategories/2/items/0/extracted/overview` | overview | string | 인태반 추출물 항노화·재생 주사 |
| `/modality/15/subcategories/2/items/0/extracted/mechanism` | mechanism | string | 라엔넥의 효소처리 인태반 추출물(저·중분자 단백질 포함)에 포함된 필수 아미노산, 펩타이드, 비타민, 미네랄, 핵산, 성장인자가 세포 재생 촉진 및 항노화 효과 제공. 근육/피하주사로 천천히 흡수되어 지속적 효과 유지. |
| `/modality/15/subcategories/2/items/0/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/15/subcategories/2/items/0/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/15/subcategories/2/items/0/extracted/indications/primary/0` | primary[0] | string | 피부재생 |
| `/modality/15/subcategories/2/items/0/extracted/indications/primary/1` | primary[1] | string | 항노화 |
| `/modality/15/subcategories/2/items/0/extracted/indications/primary/2` | primary[2] | string | 피로회복 |
| `/modality/15/subcategories/2/items/0/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/15/subcategories/2/items/0/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/15/subcategories/2/items/0/extracted/safety/common/0` | common[0] | string | 주사 부위 통증 |
| `/modality/15/subcategories/2/items/0/extracted/safety/common/1` | common[1] | string | 발적 |
| `/modality/15/subcategories/2/items/0/extracted/safety/common/2` | common[2] | string | 약간의 가려움 |
| `/modality/15/subcategories/2/items/0/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/15/subcategories/2/items/0/extracted/safety/serious/0` | serious[0] | string | 알레르기 반응 |
| `/modality/15/subcategories/2/items/0/extracted/safety/serious/1` | serious[1] | string | 감염 |
| `/modality/15/subcategories/2/items/0/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/15/subcategories/2/items/0/extracted/onset_duration/onset` | onset | string | 1주 |
| `/modality/15/subcategories/2/items/0/extracted/onset_duration/duration` | duration | string | 2-4주 |
| `/modality/15/subcategories/2/items/0/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/15/subcategories/2/items/0/extracted/aftercare/0` | aftercare[0] | string | 정맥주사 절대 금지(쇼크 위험) |
| `/modality/15/subcategories/2/items/0/extracted/aftercare/1` | aftercare[1] | string | 주사 부위 청결 유지 |
| `/modality/15/subcategories/2/items/0/extracted/aftercare/2` | aftercare[2] | string | 주 1-2회 정기적 시술 권장 |
| `/modality/15/subcategories/2/items/1` | items[1] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/15/subcategories/2/items/1/id` | id | string | M16-3-2 |
| `/modality/15/subcategories/2/items/1/name` | name | string | NAD+ |
| `/modality/15/subcategories/2/items/1/detail` | detail | string | 항노화 · 세포에너지 |
| `/modality/15/subcategories/2/items/1/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/15/subcategories/2/items/1/extracted/overview` | overview | string | 항노화·세포에너지 촉진 수액 |
| `/modality/15/subcategories/2/items/1/extracted/mechanism` | mechanism | string | NAD+(nicotinamide adenine dinucleotide)는 세포 에너지(ATP) 생성의 핵심 코엔자임으로, 정맥주사를 통해 직접 혈류 전달되어 미토콘드리아 기능 활성화, DNA 손상 복구 및 장수 유전자 활성화로 항노화 효과 제공. |
| `/modality/15/subcategories/2/items/1/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/15/subcategories/2/items/1/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/15/subcategories/2/items/1/extracted/indications/primary/0` | primary[0] | string | 항노화 |
| `/modality/15/subcategories/2/items/1/extracted/indications/primary/1` | primary[1] | string | 세포에너지 촉진 |
| `/modality/15/subcategories/2/items/1/extracted/indications/primary/2` | primary[2] | string | 인지기능 개선 |
| `/modality/15/subcategories/2/items/1/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/15/subcategories/2/items/1/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/15/subcategories/2/items/1/extracted/safety/common/0` | common[0] | string | 주사 부위 불편감 |
| `/modality/15/subcategories/2/items/1/extracted/safety/common/1` | common[1] | string | 일시적 피부 홍조 |
| `/modality/15/subcategories/2/items/1/extracted/safety/common/2` | common[2] | string | 가벼운 두통 |
| `/modality/15/subcategories/2/items/1/extracted/safety/serious` | serious | array | [array, 원소 1] |
| `/modality/15/subcategories/2/items/1/extracted/safety/serious/0` | serious[0] | string | 알레르기 반응 |
| `/modality/15/subcategories/2/items/1/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/15/subcategories/2/items/1/extracted/onset_duration/onset` | onset | string | 수 시간~1-2일 |
| `/modality/15/subcategories/2/items/1/extracted/onset_duration/duration` | duration | string | 1-2주 |
| `/modality/15/subcategories/2/items/1/extracted/aftercare` | aftercare | array | [array, 원소 2] |
| `/modality/15/subcategories/2/items/1/extracted/aftercare/0` | aftercare[0] | string | 충분한 수분섭취 |
| `/modality/15/subcategories/2/items/1/extracted/aftercare/1` | aftercare[1] | string | 정기적 시술로 효과 극대화 |
| `/modality/15/subcategories/2/items/2` | items[2] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/15/subcategories/2/items/2/id` | id | string | auto-58-1774737181584 |
| `/modality/15/subcategories/2/items/2/name` | name | string | 이뮨코어수액 |
| `/modality/15/subcategories/2/items/2/detail` | detail | string | 면역강화 |
| `/modality/15/subcategories/2/items/2/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/15/subcategories/2/items/2/extracted/overview` | overview | string | 면역강화 복합 수액 |
| `/modality/15/subcategories/2/items/2/extracted/mechanism` | mechanism | string | 비타민C, 아연, 셀레늄, 항산화제 등의 복합작용으로 면역세포 기능 촉진 및 자연살해세포 활성화. 정맥주사를 통해 높은 생체이용률로 빠른 면역력 강화 및 항바이러스·항감염 효과. |
| `/modality/15/subcategories/2/items/2/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/15/subcategories/2/items/2/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/15/subcategories/2/items/2/extracted/indications/primary/0` | primary[0] | string | 면역력 강화 |
| `/modality/15/subcategories/2/items/2/extracted/indications/primary/1` | primary[1] | string | 감염 예방 |
| `/modality/15/subcategories/2/items/2/extracted/indications/primary/2` | primary[2] | string | 회복력 촉진 |
| `/modality/15/subcategories/2/items/2/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/15/subcategories/2/items/2/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/15/subcategories/2/items/2/extracted/safety/common/0` | common[0] | string | 주사 부위 통증 |
| `/modality/15/subcategories/2/items/2/extracted/safety/common/1` | common[1] | string | 일시적 피로감 |
| `/modality/15/subcategories/2/items/2/extracted/safety/common/2` | common[2] | string | 메스꺼움 |
| `/modality/15/subcategories/2/items/2/extracted/safety/serious` | serious | array | [array, 원소 1] |
| `/modality/15/subcategories/2/items/2/extracted/safety/serious/0` | serious[0] | string | 알레르기 반응 |
| `/modality/15/subcategories/2/items/2/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/15/subcategories/2/items/2/extracted/onset_duration/onset` | onset | string | 즉시~1-2일 |
| `/modality/15/subcategories/2/items/2/extracted/onset_duration/duration` | duration | string | 1-2주 |
| `/modality/15/subcategories/2/items/2/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/15/subcategories/2/items/2/extracted/aftercare/0` | aftercare[0] | string | 충분한 수분섭취 |
| `/modality/15/subcategories/2/items/2/extracted/aftercare/1` | aftercare[1] | string | 균형 잡힌 식단 |
| `/modality/15/subcategories/2/items/2/extracted/aftercare/2` | aftercare[2] | string | 규칙적 운동 |

## 잠정 관찰 (원문 아님 · 직접 읽기 기록)

| 상태 | 근거 Pointer | 관찰 |
|---|---|---|
| P | `/modality/15/group`, `/modality/15/subcategories/0/label`, `/modality/15/subcategories/1/label` | M16 group '관리'. 하위분류가 효과·목적 축('미백/항산화','피로회복','재생/면역'). |
| P | `/modality/15/subcategories/0/items/0/is_marketing_name`, `/modality/15/subcategories/1/items/0/is_marketing_name`, `/modality/15/subcategories/1/items/1/is_marketing_name` | 백옥주사·마늘주사·신데렐라주사 — M4 와 같은 마케팅명 4필드(is_marketing_name, ingredient_basis, canonical_category, naming_caveat). canonical_category 'M16 수액치료 > 항산화·미백 IV' 등 '>' 경로, 하위 이름이 실제 label('미백/항산화')과 다르다. |
| I | `/modality/15/subcategories/1/items/0/naming_caveat`, `/modality/15/subcategories/1/items/0/extracted/mechanism` | 마늘주사: naming_caveat '실제 마늘 추출물이 아님' 인데 mechanism '비타민B1과 마늘 추출물의 협력작용'. 같은 레코드 안 모순. |
| P | `/modality/15/subcategories/0/items/3/detail`, `/modality/15/subcategories/1/items/1/ingredient_basis` | 알파리포산주사 detail '신데렐라주사 성분' — 같은 모달리티 다른 하위분류 항목(신데렐라주사, ingredient_basis 알파리포산)을 참조하는 표현. 같은 성분이 두 항목·두 하위분류(미백/항산화, 피로회복)에. |
| P | `/modality/15/subcategories/0/items/5/extracted/overview`, `/modality/15/subcategories/2/items/0/extracted/aftercare/0` | 수액치료 모달리티에 근육주사(비타민D '근육주사', 태반주사 '근육/피하주사', '정맥주사 절대 금지')가 포함 — '수액(IV)' 이름과 투여 경로가 다른 항목. |
| P | `/modality/15/subcategories/0/items/0/naming_caveat`, `/modality/15/subcategories/1/items/1/naming_caveat` | naming_caveat 이 허가 범위·근거 수준 주장('FDA·식약처의 미백 목적 공식 허가 적응증 아님', '공식 미용 허가 아님') — 규제 주장(승인하지 않음). |
| P | `/modality/15/subcategories/0/items/0/extracted/aftercare`, `/modality/15/subcategories/1/items/0/extracted/aftercare` | M16 항목 aftercare 에 '[시술 주기 참고]' 상용구 없음. |

## 수동 복합 표현 (원문 구간)

| Pointer | 구간 | 원문 표현 | 관점 | 메모 |
|---|---|---|---|---|
| `/modality/15/subcategories/0/items/0/ingredient_basis` | [16, 44] | 용량은 클리닉별로 상이(600-2,000mg 범위) | 조건, 수량·단위·시간, 범위 |  |
| `/modality/15/subcategories/0/items/0/naming_caveat` | [22, 54] | 고용량 글루타치온 IV의 미백 효과는 제한된 임상 근거이며 | 주장, 수식 | 근거 수준 |
| `/modality/15/subcategories/0/items/0/naming_caveat` | [55, 82] | FDA·식약처의 미백 목적 공식 허가 적응증 아님 | 부정, 주장 |  |
| `/modality/15/subcategories/0/items/0/naming_caveat` | [84, 97] | 의료광고 표현 주의 필요 | 조건 |  |
| `/modality/15/subcategories/0/items/0/extracted/aftercare/0` | [0, 14] | 주사 후 2시간 음주 자제 | 수량·단위·시간, 부정 |  |
| `/modality/15/subcategories/0/items/1/extracted/mechanism` | [53, 70] | 경구 투여 불가능한 고농도 도달 | 부정, 비교 |  |
| `/modality/15/subcategories/0/items/1/extracted/safety/serious/0` | [0, 14] | 신장 결석(과다 투여 시) | 조건 |  |
| `/modality/15/subcategories/0/items/1/extracted/safety/serious/1` | [0, 16] | 용혈성 빈혈(G6PD 결핍자) | 조건 |  |
| `/modality/15/subcategories/0/items/1/extracted/aftercare/1` | [0, 14] | 신기능 정상 확인 후 시술 | 조건 | 시술 전 조건 |
| `/modality/15/subcategories/0/items/4/detail` | [0, 14] | B1/B2/B6/B12/C | 기호 | '/' 성분 나열(함께) |
| `/modality/15/subcategories/0/items/6/detail` | [0, 11] | 글루타치온+트라넥삼산 | 기호 |  |
| `/modality/15/subcategories/0/items/6/extracted/aftercare/2` | [0, 5] | 운전 주의 | 조건 |  |
| `/modality/15/subcategories/1/items/0/ingredient_basis` | [36, 59] | 주사 후 일시적 마늘향 체취가 이름의 유래 | 수량·단위·시간 |  |
| `/modality/15/subcategories/1/items/0/naming_caveat` | [31, 44] | 실제 마늘 추출물이 아님 | 부정 | S046-I01 |
| `/modality/15/subcategories/1/items/0/extracted/onset_duration/onset` | [0, 7] | 즉시~수 시간 | 수량·단위·시간, 범위 |  |
| `/modality/15/subcategories/1/items/1/naming_caveat` | [53, 87] | 당뇨병성 신경병증 등 일부 적응증 외에는 공식 미용 허가 아님 | 부정, 조건, 주장 |  |
| `/modality/15/subcategories/1/items/1/extracted/safety/serious/1` | [0, 16] | 심한 저혈당(당뇨약 병용 시) | 조건, 수식 |  |
| `/modality/15/subcategories/1/items/1/extracted/aftercare/1` | [0, 17] | 당뇨약 복용자 의료진 상담 필수 | 조건 |  |
| `/modality/15/subcategories/1/items/3/extracted/safety/serious/1` | [0, 9] | 헤르페스 재활성화 |  |  |
| `/modality/15/subcategories/1/items/4/extracted/overview` | [0, 19] | 아연을 정맥 또는 근육 주사로 투여 | 조건 | 투여 경로 대안 |
| `/modality/15/subcategories/1/items/6/detail` | [0, 14] | Mg+Ca+B/C 복합수액 | 기호 | '+' 와 '/' 혼용 |
| `/modality/15/subcategories/2/items/0/extracted/aftercare/0` | [0, 17] | 정맥주사 절대 금지(쇼크 위험) | 부정, 조건, 수식 |  |
| `/modality/15/subcategories/2/items/0/extracted/aftercare/2` | [0, 16] | 주 1-2회 정기적 시술 권장 | 수량·단위·시간, 범위 |  |
| `/modality/15/subcategories/2/items/1/extracted/mechanism` | [115, 133] | 장수 유전자 활성화로 항노화 효과 | 주장 |  |
| `/modality/15/subcategories/2/items/1/extracted/onset_duration/onset` | [0, 9] | 수 시간~1-2일 | 수량·단위·시간, 범위 |  |

## 형태소 분석 확인 (알려진 오분절 K)

| 범위 | 표면형 | 문제 | 영향 |
|---|---|---|---|
| all | 비오틴주사 | 비오티/NNG ᆫ/JX 주사/NNG — 성분명 끝 받침을 조사로 | 성분명 소실 |
| all | 종합아미노산수액 | … 수/NNG 액/NNG — '수액' 분해 | 시술 유형어 분해 |
| all | 고농도C | 고/XPN 농도/NNG C/SL | 수식 접두 '고' 분리(정도 표현은 유지되나 토큰 단위) |

## 미결

| ID | 상태 | Pointer | 내용 | 영향·후속 |
|---|---|---|---|---|
| S046-I01 | I | `/modality/15/subcategories/1/items/0/naming_caveat`, `/modality/15/subcategories/1/items/0/extracted/mechanism` | 마늘주사 '마늘 추출물 아님' vs '마늘 추출물의 협력작용'. | 성분 서술 채택 시 확인 |
| S046-F01 | F | `/modality/15/subcategories/0/items/3`, `/modality/15/subcategories/1/items/1` | 같은 성분(알파리포산)이 두 항목·두 하위분류. | 성분-마케팅명 관계 설계 |
| S046-F02 | F | `/modality/15/subcategories/0/items/0/canonical_category`, `/modality/15/subcategories/1/items/0/canonical_category`, `/modality/15/subcategories/1/items/1/canonical_category` | canonical_category 경로 하위명이 실제 label 과 불일치(S012-F02 와 같은 성격). | 표준 분류 매핑 후속 |

