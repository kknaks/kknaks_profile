# S016 — M7 실리프팅

- 읽기 상태: **read** · 마지막 읽은 Pointer `/modality/6/subcategories/2/items/2/extracted/aftercare/4`
- 단위: id, category, category_en, group, subcategories 컨테이너, M7-1 items/0, M7-1 items/1, M7-1 items/2, M7-1 items/3, M7-1 items/4, M7-1 items/5, M7-2 items/0, M7-2 items/1, M7-2 items/2, M7-3 items/0, M7-3 items/1, M7-3 items/2
- 상위 문맥(공동 참조·소유 아님): 없음
- 기계 기록: `source-map.json`(section=S016) · `morphology/S016.json` · `expressions.json`(section=S016) · 읽기 렌더 `reading/S016.txt`

## 원문 값 (원본 컬럼명 그대로, 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/modality/6` | modality[6] | object | {object, 키 8: id, category, category_en, group, subcategories, extracted, products, name} |
| `/modality/6/id` | id | string | M7 |
| `/modality/6/category` | category | string | 실리프팅 |
| `/modality/6/category_en` | category_en | string | Thread Lifting |
| `/modality/6/group` | group | string | 시술/기기 |
| `/modality/6/subcategories` | subcategories | array | [array, 원소 3] |
| `/modality/6/subcategories/0` | subcategories[0] | object | {object, 키 3: id, label, items} |
| `/modality/6/subcategories/0/id` | id | string | M7-1 |
| `/modality/6/subcategories/0/label` | label | string | 재질별 |
| `/modality/6/subcategories/0/items` | items | array | [array, 원소 6] |
| `/modality/6/subcategories/0/items/0` | items[0] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/6/subcategories/0/items/0/id` | id | string | M7-1-1 |
| `/modality/6/subcategories/0/items/0/name` | name | string | PDO |
| `/modality/6/subcategories/0/items/0/detail` | detail | string | `""` (빈 문자열) |
| `/modality/6/subcategories/0/items/0/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/6/subcategories/0/items/0/extracted/overview` | overview | string | 6-8개월에 녹는 생분해성 실 |
| `/modality/6/subcategories/0/items/0/extracted/mechanism` | mechanism | string | 체내에서 자연 분해되면서 주변 콜라겐 재생을 유도하고, 삽입 직후 물리적 지지로 즉각적인 리프팅 효과를 제공한다. |
| `/modality/6/subcategories/0/items/0/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/6/subcategories/0/items/0/extracted/indications/primary` | primary | array | [array, 원소 4] |
| `/modality/6/subcategories/0/items/0/extracted/indications/primary/0` | primary[0] | string | 초기 처짐 개선 |
| `/modality/6/subcategories/0/items/0/extracted/indications/primary/1` | primary[1] | string | 피부 탄력 증강 |
| `/modality/6/subcategories/0/items/0/extracted/indications/primary/2` | primary[2] | string | 미세주름 개선 |
| `/modality/6/subcategories/0/items/0/extracted/indications/primary/3` | primary[3] | string | 턱선 정의 |
| `/modality/6/subcategories/0/items/0/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/6/subcategories/0/items/0/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/6/subcategories/0/items/0/extracted/safety/common/0` | common[0] | string | 일시적 부종 |
| `/modality/6/subcategories/0/items/0/extracted/safety/common/1` | common[1] | string | 경미한 멍 |
| `/modality/6/subcategories/0/items/0/extracted/safety/common/2` | common[2] | string | 당김감 |
| `/modality/6/subcategories/0/items/0/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/6/subcategories/0/items/0/extracted/safety/serious/0` | serious[0] | string | 신경 손상 (드묾) |
| `/modality/6/subcategories/0/items/0/extracted/safety/serious/1` | serious[1] | string | 감염 |
| `/modality/6/subcategories/0/items/0/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/6/subcategories/0/items/0/extracted/onset_duration/onset` | onset | string | 즉시~1주일 |
| `/modality/6/subcategories/0/items/0/extracted/onset_duration/duration` | duration | string | 6-8개월 |
| `/modality/6/subcategories/0/items/0/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/6/subcategories/0/items/0/extracted/aftercare/0` | aftercare[0] | string | 48시간 음주 자제 및 금연 권장(일반 건강) |
| `/modality/6/subcategories/0/items/0/extracted/aftercare/1` | aftercare[1] | string | 일주일간 과도한 표정 피하기 |
| `/modality/6/subcategories/0/items/0/extracted/aftercare/2` | aftercare[2] | string | 처음 2주간 찜질방/사우나 자제 |
| `/modality/6/subcategories/0/items/0/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 실 흡수 후 재시술 고려 (PDO 6개월, PLLA 12-18개월, PCL 24-36개월). 재시술은 6개월 이상 간격 권장. 기존 실 흡수 및 콜라겐 잔존 상태 평가 후 판단 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/6/subcategories/0/items/1` | items[1] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/6/subcategories/0/items/1/id` | id | string | M7-1-2 |
| `/modality/6/subcategories/0/items/1/name` | name | string | PCL |
| `/modality/6/subcategories/0/items/1/detail` | detail | string | `""` (빈 문자열) |
| `/modality/6/subcategories/0/items/1/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/6/subcategories/0/items/1/extracted/overview` | overview | string | 12-15개월 지속되는 장기 생분해성 실 |
| `/modality/6/subcategories/0/items/1/extracted/mechanism` | mechanism | string | PDO보다 느린 분해 속도로 더 오래 물리적 지지를 제공하며, 지속적인 콜라겐 자극으로 장기간 피부 개선을 유도한다. |
| `/modality/6/subcategories/0/items/1/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/6/subcategories/0/items/1/extracted/indications/primary` | primary | array | [array, 원소 4] |
| `/modality/6/subcategories/0/items/1/extracted/indications/primary/0` | primary[0] | string | 중등도 처짐 |
| `/modality/6/subcategories/0/items/1/extracted/indications/primary/1` | primary[1] | string | 장기 리프팅 효과 원하는 경우 |
| `/modality/6/subcategories/0/items/1/extracted/indications/primary/2` | primary[2] | string | 볼 처짐 |
| `/modality/6/subcategories/0/items/1/extracted/indications/primary/3` | primary[3] | string | 팔자주름 |
| `/modality/6/subcategories/0/items/1/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/6/subcategories/0/items/1/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/6/subcategories/0/items/1/extracted/safety/common/0` | common[0] | string | 일시적 부종 |
| `/modality/6/subcategories/0/items/1/extracted/safety/common/1` | common[1] | string | 당김감 |
| `/modality/6/subcategories/0/items/1/extracted/safety/common/2` | common[2] | string | 경미한 멍 |
| `/modality/6/subcategories/0/items/1/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/6/subcategories/0/items/1/extracted/safety/serious/0` | serious[0] | string | 감염 |
| `/modality/6/subcategories/0/items/1/extracted/safety/serious/1` | serious[1] | string | 신경 손상 (드묾) |
| `/modality/6/subcategories/0/items/1/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/6/subcategories/0/items/1/extracted/onset_duration/onset` | onset | string | 즉시~2주일 |
| `/modality/6/subcategories/0/items/1/extracted/onset_duration/duration` | duration | string | 12-15개월 |
| `/modality/6/subcategories/0/items/1/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/6/subcategories/0/items/1/extracted/aftercare/0` | aftercare[0] | string | 48시간 음주 자제 및 금연 권장(일반 건강) |
| `/modality/6/subcategories/0/items/1/extracted/aftercare/1` | aftercare[1] | string | 2주간 심한 운동 피하기 |
| `/modality/6/subcategories/0/items/1/extracted/aftercare/2` | aftercare[2] | string | 한 달간 찜질방/고온 환경 제한 |
| `/modality/6/subcategories/0/items/1/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 실 흡수 후 재시술 고려 (PDO 6개월, PLLA 12-18개월, PCL 24-36개월). 재시술은 6개월 이상 간격 권장. 기존 실 흡수 및 콜라겐 잔존 상태 평가 후 판단 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/6/subcategories/0/items/2` | items[2] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/6/subcategories/0/items/2/id` | id | string | M7-1-3 |
| `/modality/6/subcategories/0/items/2/name` | name | string | PLCL |
| `/modality/6/subcategories/0/items/2/detail` | detail | string | `""` (빈 문자열) |
| `/modality/6/subcategories/0/items/2/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/6/subcategories/0/items/2/extracted/overview` | overview | string | 12-18개월 지속되는 혼합형 생분해성 실 |
| `/modality/6/subcategories/0/items/2/extracted/mechanism` | mechanism | string | PCL과 PLA의 장점을 결합하여 중간 정도의 분해 속도로 안정적인 리프팅과 강화된 콜라겐 유도를 동시에 제공한다. |
| `/modality/6/subcategories/0/items/2/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/6/subcategories/0/items/2/extracted/indications/primary` | primary | array | [array, 원소 4] |
| `/modality/6/subcategories/0/items/2/extracted/indications/primary/0` | primary[0] | string | 중등도 이상 처짐 |
| `/modality/6/subcategories/0/items/2/extracted/indications/primary/1` | primary[1] | string | 복합적 피부 개선 |
| `/modality/6/subcategories/0/items/2/extracted/indications/primary/2` | primary[2] | string | 턱선 및 볼 리프팅 |
| `/modality/6/subcategories/0/items/2/extracted/indications/primary/3` | primary[3] | string | 전체 얼굴 구조 개선 |
| `/modality/6/subcategories/0/items/2/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/6/subcategories/0/items/2/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/6/subcategories/0/items/2/extracted/safety/common/0` | common[0] | string | 일시적 부종 |
| `/modality/6/subcategories/0/items/2/extracted/safety/common/1` | common[1] | string | 당김감 |
| `/modality/6/subcategories/0/items/2/extracted/safety/common/2` | common[2] | string | 경미한 멍 |
| `/modality/6/subcategories/0/items/2/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/6/subcategories/0/items/2/extracted/safety/serious/0` | serious[0] | string | 감염 |
| `/modality/6/subcategories/0/items/2/extracted/safety/serious/1` | serious[1] | string | 신경 손상 (드묾) |
| `/modality/6/subcategories/0/items/2/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/6/subcategories/0/items/2/extracted/onset_duration/onset` | onset | string | 즉시~2주일 |
| `/modality/6/subcategories/0/items/2/extracted/onset_duration/duration` | duration | string | 24-36개월 |
| `/modality/6/subcategories/0/items/2/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/6/subcategories/0/items/2/extracted/aftercare/0` | aftercare[0] | string | 48시간 음주 자제 및 금연 권장(일반 건강) |
| `/modality/6/subcategories/0/items/2/extracted/aftercare/1` | aftercare[1] | string | 2주간 심한 운동 피하기 |
| `/modality/6/subcategories/0/items/2/extracted/aftercare/2` | aftercare[2] | string | [시술 주기 참고] 실 흡수 후 재시술 고려 (PDO 6개월, PLLA 12-18개월, PCL 24-36개월). 재시술은 6개월 이상 간격 권장. 기존 실 흡수 및 콜라겐 잔존 상태 평가 후 판단 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/6/subcategories/0/items/3` | items[3] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/6/subcategories/0/items/3/id` | id | string | auto-26-1774737181584 |
| `/modality/6/subcategories/0/items/3/name` | name | string | PLLA |
| `/modality/6/subcategories/0/items/3/detail` | detail | string | `""` (빈 문자열) |
| `/modality/6/subcategories/0/items/3/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/6/subcategories/0/items/3/extracted/overview` | overview | string | 12-18개월에 걸쳐 점진적으로 분해되며 신생콜라겐 생성을 유도하는 폴리-L-락트산 기반 실리프팅 제품 |
| `/modality/6/subcategories/0/items/3/extracted/mechanism` | mechanism | string | PLLA는 조직에 삽입된 후 대식세포에 의해 탐식되어 섬유아세포를 자극하고 신생콜라겐 및 섬유가교를 형성하도록 유도한다. 이 과정은 48주에 걸쳐 최대 24% 조직수축을 일으키며 장기간의 피부견인 및 볼륨 복원 효과를 제공한다. |
| `/modality/6/subcategories/0/items/3/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/6/subcategories/0/items/3/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/6/subcategories/0/items/3/extracted/indications/primary/0` | primary[0] | string | 중등도 이상의 얼굴 처짐 및 팔자주름 |
| `/modality/6/subcategories/0/items/3/extracted/indications/primary/1` | primary[1] | string | 광대뼈 부위 볼륨 감소 |
| `/modality/6/subcategories/0/items/3/extracted/indications/primary/2` | primary[2] | string | 턱선 및 목 처짐 |
| `/modality/6/subcategories/0/items/3/extracted/indications/primary/3` | primary[3] | string | 관자놀이 및 미간 주름 |
| `/modality/6/subcategories/0/items/3/extracted/indications/primary/4` | primary[4] | string | 팔·다리·복부의 피부 탄력 저하 |
| `/modality/6/subcategories/0/items/3/extracted/safety` | safety | object | {object, 키 3: common, serious, contraindications} |
| `/modality/6/subcategories/0/items/3/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/6/subcategories/0/items/3/extracted/safety/common/0` | common[0] | string | 주입부위 부종(3-5일) |
| `/modality/6/subcategories/0/items/3/extracted/safety/common/1` | common[1] | string | 경미한 멍 및 압통 |
| `/modality/6/subcategories/0/items/3/extracted/safety/common/2` | common[2] | string | 일시적 피부 불균일감 |
| `/modality/6/subcategories/0/items/3/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/6/subcategories/0/items/3/extracted/safety/serious/0` | serious[0] | string | 육아종 형성 |
| `/modality/6/subcategories/0/items/3/extracted/safety/serious/1` | serious[1] | string | 비가교HA와의 동시 사용 금기(24-72시간 분해 상충) |
| `/modality/6/subcategories/0/items/3/extracted/safety/contraindications` | contraindications | array | [array, 원소 3] |
| `/modality/6/subcategories/0/items/3/extracted/safety/contraindications/0` | contraindications[0] | string | 임신·수유 중 |
| `/modality/6/subcategories/0/items/3/extracted/safety/contraindications/1` | contraindications[1] | string | 활동성 감염 부위 |
| `/modality/6/subcategories/0/items/3/extracted/safety/contraindications/2` | contraindications[2] | string | 과도한 면역반응 병력 |
| `/modality/6/subcategories/0/items/3/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/6/subcategories/0/items/3/extracted/onset_duration/onset` | onset | string | 3-4주(초기 콜라겐 생성 시작) |
| `/modality/6/subcategories/0/items/3/extracted/onset_duration/duration` | duration | string | 12-18개월(점진적 분해 및 지속) |
| `/modality/6/subcategories/0/items/3/extracted/aftercare` | aftercare | array | [array, 원소 6] |
| `/modality/6/subcategories/0/items/3/extracted/aftercare/0` | aftercare[0] | string | 24시간 이내 고온 환경(사우나, 운동) 피하기 |
| `/modality/6/subcategories/0/items/3/extracted/aftercare/1` | aftercare[1] | string | 주입부위 과도한 압박 자제(72시간) |
| `/modality/6/subcategories/0/items/3/extracted/aftercare/2` | aftercare[2] | string | 48시간 내 비가교HA 제품 사용 자제 |
| `/modality/6/subcategories/0/items/3/extracted/aftercare/3` | aftercare[3] | string | 냉찜질로 부종 관리(필요시) |
| `/modality/6/subcategories/0/items/3/extracted/aftercare/4` | aftercare[4] | string | 4주 후 추적 검진으로 육아종 모니터링 |
| `/modality/6/subcategories/0/items/3/extracted/aftercare/5` | aftercare[5] | string | [시술 주기 참고] 실 흡수 후 재시술 고려 (PDO 6개월, PLLA 12-18개월, PCL 24-36개월). 재시술은 6개월 이상 간격 권장. 기존 실 흡수 및 콜라겐 잔존 상태 평가 후 판단 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/6/subcategories/0/items/4` | items[4] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/6/subcategories/0/items/4/id` | id | string | auto-M7-1775361902160 |
| `/modality/6/subcategories/0/items/4/name` | name | string | PCA실 |
| `/modality/6/subcategories/0/items/4/detail` | detail | string | 폴리카프로락톤아크릴레이트 · 잼버실 소재 |
| `/modality/6/subcategories/0/items/4/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/6/subcategories/0/items/4/extracted/overview` | overview | string | 폴리카프로락톤 기반의 생분해성 실을 이용한 리프팅 및 조직 재생 시술 |
| `/modality/6/subcategories/0/items/4/extracted/mechanism` | mechanism | string | 폴리카프로락톤아크릴레이트 실이 피하조직에 삽입되어 즉각적인 리프팅 효과를 제공합니다. 실이 서서히 분해되면서 콜라겐 생성을 촉진하여 장기간 조직 재생 및 탄력 개선 효과를 나타냅니다. |
| `/modality/6/subcategories/0/items/4/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/6/subcategories/0/items/4/extracted/indications/primary` | primary | array | [array, 원소 2] |
| `/modality/6/subcategories/0/items/4/extracted/indications/primary/0` | primary[0] | string | 안면 리프팅 및 윤곽 개선 |
| `/modality/6/subcategories/0/items/4/extracted/indications/primary/1` | primary[1] | string | 목과 목선 탄력 개선 |
| `/modality/6/subcategories/0/items/4/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/6/subcategories/0/items/4/extracted/safety/common` | common | array | [array, 원소 1] |
| `/modality/6/subcategories/0/items/4/extracted/safety/common/0` | common[0] | string | 시술 부위 일시적 부종 및 멍 |
| `/modality/6/subcategories/0/items/4/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/6/subcategories/0/items/4/extracted/onset_duration/onset` | onset | string | 즉시 |
| `/modality/6/subcategories/0/items/4/extracted/onset_duration/duration` | duration | string | 12-18개월 |
| `/modality/6/subcategories/0/items/4/extracted/aftercare` | aftercare | array | [array, 원소 6] |
| `/modality/6/subcategories/0/items/4/extracted/aftercare/0` | aftercare[0] | string | 시술 후 1-2주간 과도한 안면 움직임 및 강한 마사지 자제 |
| `/modality/6/subcategories/0/items/4/extracted/aftercare/1` | aftercare[1] | string | 며칠간 강한 안면 마사지 자제 (실 고정 안정화 목적) |
| `/modality/6/subcategories/0/items/4/extracted/aftercare/2` | aftercare[2] | string | 크게 입 벌리거나 강한 저작 며칠 자제 |
| `/modality/6/subcategories/0/items/4/extracted/aftercare/3` | aftercare[3] | string | 당김감/부종은 수일 내 자연 완화 |
| `/modality/6/subcategories/0/items/4/extracted/aftercare/4` | aftercare[4] | string | 이상 반응(감염 징후, 실 노출, 심한 통증) 시 즉시 내원 |
| `/modality/6/subcategories/0/items/4/extracted/aftercare/5` | aftercare[5] | string | [시술 주기 참고] 실 흡수 후 재시술 고려 (PDO 6개월, PLLA 12-18개월, PCL 24-36개월). 재시술은 6개월 이상 간격 권장. 기존 실 흡수 및 콜라겐 잔존 상태 평가 후 판단 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/6/subcategories/0/items/5` | items[5] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/6/subcategories/0/items/5/id` | id | string | auto-M7-1775364775160 |
| `/modality/6/subcategories/0/items/5/name` | name | string | PLLA+PCL복합실 |
| `/modality/6/subcategories/0/items/5/detail` | detail | string | 혼합장기유도 |
| `/modality/6/subcategories/0/items/5/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/6/subcategories/0/items/5/extracted/overview` | overview | string | 혼합 성분 장기간 유도 실리프팅 |
| `/modality/6/subcategories/0/items/5/extracted/mechanism` | mechanism | string | PLLA와 PCL 성분이 서로 다른 속도로 분해되면서 단계적 콜라겐 생성을 유도합니다. 즉각적인 리프팅과 장기간 지속되는 탄력 개선을 동시에 달성합니다. |
| `/modality/6/subcategories/0/items/5/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/6/subcategories/0/items/5/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/6/subcategories/0/items/5/extracted/indications/primary/0` | primary[0] | string | 강력한 리프팅 |
| `/modality/6/subcategories/0/items/5/extracted/indications/primary/1` | primary[1] | string | 장기간 지속 |
| `/modality/6/subcategories/0/items/5/extracted/indications/primary/2` | primary[2] | string | 깊은 주름 개선 |
| `/modality/6/subcategories/0/items/5/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/6/subcategories/0/items/5/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/6/subcategories/0/items/5/extracted/safety/common/0` | common[0] | string | 시술 부위 부종 |
| `/modality/6/subcategories/0/items/5/extracted/safety/common/1` | common[1] | string | 경미한 멍 |
| `/modality/6/subcategories/0/items/5/extracted/safety/common/2` | common[2] | string | 일시적 당김감 |
| `/modality/6/subcategories/0/items/5/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/6/subcategories/0/items/5/extracted/onset_duration/onset` | onset | string | 즉시 (최대 효과 4-6주) |
| `/modality/6/subcategories/0/items/5/extracted/onset_duration/duration` | duration | string | 12-18개월 |
| `/modality/6/subcategories/0/items/5/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/6/subcategories/0/items/5/extracted/aftercare/0` | aftercare[0] | string | 시술 후 1주일 강한 표정 자제 |
| `/modality/6/subcategories/0/items/5/extracted/aftercare/1` | aftercare[1] | string | 강한 마사지 자제 |
| `/modality/6/subcategories/0/items/5/extracted/aftercare/2` | aftercare[2] | string | 충분한 보습 |
| `/modality/6/subcategories/0/items/5/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 실 흡수 후 재시술 고려 (PDO 6개월, PLLA 12-18개월, PCL 24-36개월). 재시술은 6개월 이상 간격 권장. 기존 실 흡수 및 콜라겐 잔존 상태 평가 후 판단 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/6/subcategories/1` | subcategories[1] | object | {object, 키 3: id, label, items} |
| `/modality/6/subcategories/1/id` | id | string | M7-2 |
| `/modality/6/subcategories/1/label` | label | string | 형태별 |
| `/modality/6/subcategories/1/items` | items | array | [array, 원소 3] |
| `/modality/6/subcategories/1/items/0` | items[0] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/6/subcategories/1/items/0/id` | id | string | M7-2-1 |
| `/modality/6/subcategories/1/items/0/name` | name | string | 코그(Cog) |
| `/modality/6/subcategories/1/items/0/detail` | detail | string | 양방향/단방향 · 견인력 |
| `/modality/6/subcategories/1/items/0/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/6/subcategories/1/items/0/extracted/overview` | overview | string | PDO, PLLA, PCL 소재의 양방향/단방향 견인력 코그를 이용한 supraSMAS 층 배치 실리프팅으로 즉각적 거상과 장기 조직재구성을 동시에 제공하는 시술. |
| `/modality/6/subcategories/1/items/0/extracted/mechanism` | mechanism | string | 코그의 물리적 견인력으로 즉각적인 조직 거상을 유도하며, 동시에 이물반응을 통해 신생콜라겐 형성, 섬유가교, 혈관신생을 자극한다. 소재별 분해 기간(PDO 6개월/PLLA 12-18개월/PCL 24-36개월)에 따라 단계적 조직수축(48주 기준 24%)과 장기 구조적 재모델링을 달성한다. |
| `/modality/6/subcategories/1/items/0/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/6/subcategories/1/items/0/extracted/indications/primary` | primary | array | [array, 원소 4] |
| `/modality/6/subcategories/1/items/0/extracted/indications/primary/0` | primary[0] | string | 중등도 안면 처짐(미간, 눈썹, 광대) |
| `/modality/6/subcategories/1/items/0/extracted/indications/primary/1` | primary[1] | string | 목 주름 및 처짐 |
| `/modality/6/subcategories/1/items/0/extracted/indications/primary/2` | primary[2] | string | 팔뚝/허벅지 지방감소 및 거상 |
| `/modality/6/subcategories/1/items/0/extracted/indications/primary/3` | primary[3] | string | 조직 재생이 필요한 노화성 피부 |
| `/modality/6/subcategories/1/items/0/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/6/subcategories/1/items/0/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/6/subcategories/1/items/0/extracted/safety/common/0` | common[0] | string | 시술 후 부종(3-7일) |
| `/modality/6/subcategories/1/items/0/extracted/safety/common/1` | common[1] | string | 경미한 멍/출혈 |
| `/modality/6/subcategories/1/items/0/extracted/safety/common/2` | common[2] | string | 당김감(2-4주) |
| `/modality/6/subcategories/1/items/0/extracted/safety/serious` | serious | array | [array, 원소 4] |
| `/modality/6/subcategories/1/items/0/extracted/safety/serious/0` | serious[0] | string | 신경손상(안면신경) |
| `/modality/6/subcategories/1/items/0/extracted/safety/serious/1` | serious[1] | string | 감염 |
| `/modality/6/subcategories/1/items/0/extracted/safety/serious/2` | serious[2] | string | 부당한 거상(코그 이탈) |
| `/modality/6/subcategories/1/items/0/extracted/safety/serious/3` | serious[3] | string | PDO+비가교HA 병용 금기(24-72시간 급속분해 위험) (in vitro 연구 기반, 임상 증거 제한적) |
| `/modality/6/subcategories/1/items/0/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/6/subcategories/1/items/0/extracted/onset_duration/onset` | onset | string | 즉각(물리적 거상) / 점진적(콜라겐 형성 2-4주) |
| `/modality/6/subcategories/1/items/0/extracted/onset_duration/duration` | duration | string | 24-36개월 |
| `/modality/6/subcategories/1/items/0/extracted/aftercare` | aftercare | array | [array, 원소 7] |
| `/modality/6/subcategories/1/items/0/extracted/aftercare/0` | aftercare[0] | string | 24-48시간 항생제 연고 도포 |
| `/modality/6/subcategories/1/items/0/extracted/aftercare/1` | aftercare[1] | string | 72시간 음주 자제/과도한 안면표정 제한 |
| `/modality/6/subcategories/1/items/0/extracted/aftercare/2` | aftercare[2] | string | 1주일 사우나/찜질방 자제 |
| `/modality/6/subcategories/1/items/0/extracted/aftercare/3` | aftercare[3] | string | 2주일 격렬한 운동 자제 |
| `/modality/6/subcategories/1/items/0/extracted/aftercare/4` | aftercare[4] | string | 비가교HA 제품 72시간 금기 |
| `/modality/6/subcategories/1/items/0/extracted/aftercare/5` | aftercare[5] | string | 지속적 부종 시 냉찜질 시행 |
| `/modality/6/subcategories/1/items/0/extracted/aftercare/6` | aftercare[6] | string | [시술 주기 참고] 실 흡수 후 재시술 고려 (PDO 6개월, PLLA 12-18개월, PCL 24-36개월). 재시술은 6개월 이상 간격 권장. 기존 실 흡수 및 콜라겐 잔존 상태 평가 후 판단 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/6/subcategories/1/items/1` | items[1] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/6/subcategories/1/items/1/id` | id | string | M7-2-2 |
| `/modality/6/subcategories/1/items/1/name` | name | string | 모노 |
| `/modality/6/subcategories/1/items/1/detail` | detail | string | 콜라겐 유도 · 탄력 |
| `/modality/6/subcategories/1/items/1/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/6/subcategories/1/items/1/extracted/overview` | overview | string | 콜라겐 유도에 특화된 매끈한 구조 실 |
| `/modality/6/subcategories/1/items/1/extracted/mechanism` | mechanism | string | 톱니가 없어 통증이 적으면서도 실 삽입 부위 주변에 강한 콜라겐 자극과 재생을 유도하며, 점진적인 피부 탄력 개선을 제공한다. |
| `/modality/6/subcategories/1/items/1/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/6/subcategories/1/items/1/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/6/subcategories/1/items/1/extracted/indications/primary/0` | primary[0] | string | 경미한 처짐 |
| `/modality/6/subcategories/1/items/1/extracted/indications/primary/1` | primary[1] | string | 피부 탄력 증강 |
| `/modality/6/subcategories/1/items/1/extracted/indications/primary/2` | primary[2] | string | 미세주름 개선 |
| `/modality/6/subcategories/1/items/1/extracted/indications/primary/3` | primary[3] | string | 피부결 개선 |
| `/modality/6/subcategories/1/items/1/extracted/indications/primary/4` | primary[4] | string | 전체 얼굴 톤 업 |
| `/modality/6/subcategories/1/items/1/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/6/subcategories/1/items/1/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/6/subcategories/1/items/1/extracted/safety/common/0` | common[0] | string | 일시적 부종 |
| `/modality/6/subcategories/1/items/1/extracted/safety/common/1` | common[1] | string | 경미한 멍 |
| `/modality/6/subcategories/1/items/1/extracted/safety/common/2` | common[2] | string | 당김감 |
| `/modality/6/subcategories/1/items/1/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/6/subcategories/1/items/1/extracted/safety/serious/0` | serious[0] | string | 감염 |
| `/modality/6/subcategories/1/items/1/extracted/safety/serious/1` | serious[1] | string | 신경 손상 (드묾) |
| `/modality/6/subcategories/1/items/1/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/6/subcategories/1/items/1/extracted/onset_duration/onset` | onset | string | 1-2주일 |
| `/modality/6/subcategories/1/items/1/extracted/onset_duration/duration` | duration | string | 6-12개월 |
| `/modality/6/subcategories/1/items/1/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/6/subcategories/1/items/1/extracted/aftercare/0` | aftercare[0] | string | 24시간 음주 자제 및 금연 권장(일반 건강) |
| `/modality/6/subcategories/1/items/1/extracted/aftercare/1` | aftercare[1] | string | 일주일간 과도한 표정 피하기 |
| `/modality/6/subcategories/1/items/1/extracted/aftercare/2` | aftercare[2] | string | [시술 주기 참고] 실 흡수 후 재시술 고려 (PDO 6개월, PLLA 12-18개월, PCL 24-36개월). 재시술은 6개월 이상 간격 권장. 기존 실 흡수 및 콜라겐 잔존 상태 평가 후 판단 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/6/subcategories/1/items/2` | items[2] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/6/subcategories/1/items/2/id` | id | string | M7-2-3 |
| `/modality/6/subcategories/1/items/2/name` | name | string | 볼륨실 |
| `/modality/6/subcategories/1/items/2/detail` | detail | string | 볼륨+탄력 |
| `/modality/6/subcategories/1/items/2/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/6/subcategories/1/items/2/extracted/overview` | overview | string | 부피감+탄력을 동시에 제공하는 복합 실 |
| `/modality/6/subcategories/1/items/2/extracted/mechanism` | mechanism | string | 실 자체가 부피를 만들어 처진 부위를 물리적으로 채우면서 동시에 콜라겐 유도로 탄력을 개선하여, 볼륨 손실과 처짐을 함께 교정한다. |
| `/modality/6/subcategories/1/items/2/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/6/subcategories/1/items/2/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/6/subcategories/1/items/2/extracted/indications/primary/0` | primary[0] | string | 볼 꺼짐 + 처짐 |
| `/modality/6/subcategories/1/items/2/extracted/indications/primary/1` | primary[1] | string | 평탄한 얼굴 입체감 개선 |
| `/modality/6/subcategories/1/items/2/extracted/indications/primary/2` | primary[2] | string | 팔자주름 개선 |
| `/modality/6/subcategories/1/items/2/extracted/indications/primary/3` | primary[3] | string | 종합적 얼굴 리프팅 |
| `/modality/6/subcategories/1/items/2/extracted/indications/primary/4` | primary[4] | string | 노화로 인한 볼륨 손실 |
| `/modality/6/subcategories/1/items/2/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/6/subcategories/1/items/2/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/6/subcategories/1/items/2/extracted/safety/common/0` | common[0] | string | 부종 |
| `/modality/6/subcategories/1/items/2/extracted/safety/common/1` | common[1] | string | 당김감 |
| `/modality/6/subcategories/1/items/2/extracted/safety/common/2` | common[2] | string | 울퉁불퉁함 |
| `/modality/6/subcategories/1/items/2/extracted/safety/serious` | serious | array | [array, 원소 3] |
| `/modality/6/subcategories/1/items/2/extracted/safety/serious/0` | serious[0] | string | 감염 |
| `/modality/6/subcategories/1/items/2/extracted/safety/serious/1` | serious[1] | string | 신경 손상 |
| `/modality/6/subcategories/1/items/2/extracted/safety/serious/2` | serious[2] | string | 비대칭 결과 |
| `/modality/6/subcategories/1/items/2/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/6/subcategories/1/items/2/extracted/onset_duration/onset` | onset | string | 즉시~1주일 |
| `/modality/6/subcategories/1/items/2/extracted/onset_duration/duration` | duration | string | 12-18개월 |
| `/modality/6/subcategories/1/items/2/extracted/aftercare` | aftercare | array | [array, 원소 5] |
| `/modality/6/subcategories/1/items/2/extracted/aftercare/0` | aftercare[0] | string | 48시간 음주 자제 및 금연 권장(일반 건강) |
| `/modality/6/subcategories/1/items/2/extracted/aftercare/1` | aftercare[1] | string | 2주간 심한 운동 피하기 |
| `/modality/6/subcategories/1/items/2/extracted/aftercare/2` | aftercare[2] | string | 한 달간 찜질방/고온 환경 제한 |
| `/modality/6/subcategories/1/items/2/extracted/aftercare/3` | aftercare[3] | string | 정기적 경과 관찰 |
| `/modality/6/subcategories/1/items/2/extracted/aftercare/4` | aftercare[4] | string | [시술 주기 참고] 실 흡수 후 재시술 고려 (PDO 6개월, PLLA 12-18개월, PCL 24-36개월). 재시술은 6개월 이상 간격 권장. 기존 실 흡수 및 콜라겐 잔존 상태 평가 후 판단 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/6/subcategories/2` | subcategories[2] | object | {object, 키 3: id, label, items} |
| `/modality/6/subcategories/2/id` | id | string | M7-3 |
| `/modality/6/subcategories/2/label` | label | string | 브랜드 |
| `/modality/6/subcategories/2/items` | items | array | [array, 원소 24] |
| `/modality/6/subcategories/2/items/0` | items[0] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/6/subcategories/2/items/0/id` | id | string | M7-3-1 |
| `/modality/6/subcategories/2/items/0/name` | name | string | 민트리프트 |
| `/modality/6/subcategories/2/items/0/detail` | detail | string | Cog · 대표 브랜드 |
| `/modality/6/subcategories/2/items/0/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/6/subcategories/2/items/0/extracted/overview` | overview | string | 코그 톱니 구조로 강력한 리프팅 브랜드 |
| `/modality/6/subcategories/2/items/0/extracted/mechanism` | mechanism | string | 양방향 또는 단방향 코그 톱니를 이용해 처진 피부를 강력하게 들어올리며, PDO 또는 PLLA 재질로 장기간 효과를 유지하고 콜라겐 재생을 자극한다. |
| `/modality/6/subcategories/2/items/0/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/6/subcategories/2/items/0/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/6/subcategories/2/items/0/extracted/indications/primary/0` | primary[0] | string | 중등도 이상 처짐 |
| `/modality/6/subcategories/2/items/0/extracted/indications/primary/1` | primary[1] | string | 빠른 리프팅 효과 원하는 경우 |
| `/modality/6/subcategories/2/items/0/extracted/indications/primary/2` | primary[2] | string | 페이스라인 재정의 |
| `/modality/6/subcategories/2/items/0/extracted/indications/primary/3` | primary[3] | string | 턱선 강화 |
| `/modality/6/subcategories/2/items/0/extracted/indications/primary/4` | primary[4] | string | 애플 페이스 복원 |
| `/modality/6/subcategories/2/items/0/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/6/subcategories/2/items/0/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/6/subcategories/2/items/0/extracted/safety/common/0` | common[0] | string | 당김감 |
| `/modality/6/subcategories/2/items/0/extracted/safety/common/1` | common[1] | string | 부종 |
| `/modality/6/subcategories/2/items/0/extracted/safety/common/2` | common[2] | string | 피부 요철감 |
| `/modality/6/subcategories/2/items/0/extracted/safety/serious` | serious | array | [array, 원소 3] |
| `/modality/6/subcategories/2/items/0/extracted/safety/serious/0` | serious[0] | string | 신경 손상 |
| `/modality/6/subcategories/2/items/0/extracted/safety/serious/1` | serious[1] | string | 과도한 들어올림 |
| `/modality/6/subcategories/2/items/0/extracted/safety/serious/2` | serious[2] | string | 감염 |
| `/modality/6/subcategories/2/items/0/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/6/subcategories/2/items/0/extracted/onset_duration/onset` | onset | string | 즉시~3일 |
| `/modality/6/subcategories/2/items/0/extracted/onset_duration/duration` | duration | string | 12-18개월 |
| `/modality/6/subcategories/2/items/0/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/6/subcategories/2/items/0/extracted/aftercare/0` | aftercare[0] | string | 처음 당일 음주 자제 및 금연 권장(일반 건강) |
| `/modality/6/subcategories/2/items/0/extracted/aftercare/1` | aftercare[1] | string | 2주간 심한 운동 및 표정 제한 |
| `/modality/6/subcategories/2/items/0/extracted/aftercare/2` | aftercare[2] | string | 붓기가 안정화될 때까지 정기 추적 |
| `/modality/6/subcategories/2/items/0/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 실 흡수 후 재시술 고려 (PDO 6개월, PLLA 12-18개월, PCL 24-36개월). 재시술은 6개월 이상 간격 권장. 기존 실 흡수 및 콜라겐 잔존 상태 평가 후 판단 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/6/subcategories/2/items/1` | items[1] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/6/subcategories/2/items/1/id` | id | string | M7-3-3 |
| `/modality/6/subcategories/2/items/1/name` | name | string | 테스리프트 |
| `/modality/6/subcategories/2/items/1/detail` | detail | string | PDO+몰딩 메쉬 |
| `/modality/6/subcategories/2/items/1/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/6/subcategories/2/items/1/extracted/overview` | overview | string | PDO 실과 몰딩 메쉬 구조로 즉각적인 리프팅과 장기적인 콜라겐 재생을 동시에 제공하는 고급 시술 제품 |
| `/modality/6/subcategories/2/items/1/extracted/mechanism` | mechanism | string | PDO 실의 기계적 견인력으로 즉각적인 조직 거상을 유도하며, 몰딩 메쉬는 신생콜라겐 생성, 섬유가교 형성, 24%의 조직 수축(48주)을 촉진한다. Supra-SMAS 배치를 통해 혈관개선 및 지방감소 효과를 동반한 장기적 윤곽 개선을 실현한다. |
| `/modality/6/subcategories/2/items/1/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/6/subcategories/2/items/1/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/6/subcategories/2/items/1/extracted/indications/primary/0` | primary[0] | string | 중면부 하강 |
| `/modality/6/subcategories/2/items/1/extracted/indications/primary/1` | primary[1] | string | 팔자주름 |
| `/modality/6/subcategories/2/items/1/extracted/indications/primary/2` | primary[2] | string | 볼살 처짐 |
| `/modality/6/subcategories/2/items/1/extracted/indications/primary/3` | primary[3] | string | 턱선 이완 |
| `/modality/6/subcategories/2/items/1/extracted/indications/primary/4` | primary[4] | string | 목주름 |
| `/modality/6/subcategories/2/items/1/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/6/subcategories/2/items/1/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/6/subcategories/2/items/1/extracted/safety/common/0` | common[0] | string | 일시적 붓기 |
| `/modality/6/subcategories/2/items/1/extracted/safety/common/1` | common[1] | string | 경미한 통증 |
| `/modality/6/subcategories/2/items/1/extracted/safety/common/2` | common[2] | string | 피부 발적 |
| `/modality/6/subcategories/2/items/1/extracted/safety/serious` | serious | array | [array, 원소 3] |
| `/modality/6/subcategories/2/items/1/extracted/safety/serious/0` | serious[0] | string | 신경손상 |
| `/modality/6/subcategories/2/items/1/extracted/safety/serious/1` | serious[1] | string | 감염 |
| `/modality/6/subcategories/2/items/1/extracted/safety/serious/2` | serious[2] | string | 과도한 조직반응 |
| `/modality/6/subcategories/2/items/1/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/6/subcategories/2/items/1/extracted/onset_duration/onset` | onset | string | 3-7일 (즉각적 리프팅), 2-3주 (콜라겐 생성) |
| `/modality/6/subcategories/2/items/1/extracted/onset_duration/duration` | duration | string | 6-9개월 (PDO), 콜라겐 재생 효과 12-18개월 |
| `/modality/6/subcategories/2/items/1/extracted/aftercare` | aftercare | array | [array, 원소 8] |
| `/modality/6/subcategories/2/items/1/extracted/aftercare/0` | aftercare[0] | string | 시술 후 48시간 음주 자제 |
| `/modality/6/subcategories/2/items/1/extracted/aftercare/1` | aftercare[1] | string | 1주일 과도한 안면운동 제한 |
| `/modality/6/subcategories/2/items/1/extracted/aftercare/2` | aftercare[2] | string | 비가교HA 제품 24-72시간 사용자제 |
| `/modality/6/subcategories/2/items/1/extracted/aftercare/3` | aftercare[3] | string | 고강도 운동 3-5일 피하기 |
| `/modality/6/subcategories/2/items/1/extracted/aftercare/4` | aftercare[4] | string | 냉찜질로 부종 관리 |
| `/modality/6/subcategories/2/items/1/extracted/aftercare/5` | aftercare[5] | string | 항생제 연고 도포 |
| `/modality/6/subcategories/2/items/1/extracted/aftercare/6` | aftercare[6] | string | 과도한 얼굴 강한 마사지 자제 |
| `/modality/6/subcategories/2/items/1/extracted/aftercare/7` | aftercare[7] | string | [시술 주기 참고] 실 흡수 후 재시술 고려 (PDO 6개월, PLLA 12-18개월, PCL 24-36개월). 재시술은 6개월 이상 간격 권장. 기존 실 흡수 및 콜라겐 잔존 상태 평가 후 판단 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/6/subcategories/2/items/2` | items[2] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/6/subcategories/2/items/2/id` | id | string | M7-3-2 |
| `/modality/6/subcategories/2/items/2/name` | name | string | 실루엣소프트 |
| `/modality/6/subcategories/2/items/2/detail` | detail | string | PLLA 콘 |
| `/modality/6/subcategories/2/items/2/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/6/subcategories/2/items/2/extracted/overview` | overview | string | PLLA 콘 구조로 즉각적 기계적 지지와 12-18개월 생물학적 자극을 제공하는 차세대 실리프팅 제품 |
| `/modality/6/subcategories/2/items/2/extracted/mechanism` | mechanism | string | PLLA 콘은 조직에 즉시 물리적 지탱력을 부여하며, 12-18개월에 걸쳐 신생콜라겐 유도, 섬유가교 형성, 지방감소를 유발한다. 이를 통해 48주 기준 24% 수축효과와 혈관개선을 동시에 달성한다. |
| `/modality/6/subcategories/2/items/2/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/6/subcategories/2/items/2/extracted/indications/primary` | primary | array | [array, 원소 4] |
| `/modality/6/subcategories/2/items/2/extracted/indications/primary/0` | primary[0] | string | 중등도 이상의 안면 처짐 |
| `/modality/6/subcategories/2/items/2/extracted/indications/primary/1` | primary[1] | string | 팔자주름 및 마리오네트라인 |
| `/modality/6/subcategories/2/items/2/extracted/indications/primary/2` | primary[2] | string | 턱선 리프팅 |
| `/modality/6/subcategories/2/items/2/extracted/indications/primary/3` | primary[3] | string | 광대뼈 부위 볼륨 소실 |
| `/modality/6/subcategories/2/items/2/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/6/subcategories/2/items/2/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/6/subcategories/2/items/2/extracted/safety/common/0` | common[0] | string | 시술 부위 부종 |
| `/modality/6/subcategories/2/items/2/extracted/safety/common/1` | common[1] | string | 경미한 통증 |
| `/modality/6/subcategories/2/items/2/extracted/safety/common/2` | common[2] | string | 일시적 발적 |
| `/modality/6/subcategories/2/items/2/extracted/safety/serious` | serious | array | [array, 원소 3] |
| `/modality/6/subcategories/2/items/2/extracted/safety/serious/0` | serious[0] | string | 신경손상 |
| `/modality/6/subcategories/2/items/2/extracted/safety/serious/1` | serious[1] | string | 감염 |
| `/modality/6/subcategories/2/items/2/extracted/safety/serious/2` | serious[2] | string | 혈종 |
| `/modality/6/subcategories/2/items/2/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/6/subcategories/2/items/2/extracted/onset_duration/onset` | onset | string | 즉시(기계적 지지) / 4-6주(콜라겐 유도 시작) |
| `/modality/6/subcategories/2/items/2/extracted/onset_duration/duration` | duration | string | 12-18개월 |
| `/modality/6/subcategories/2/items/2/extracted/aftercare` | aftercare | array | [array, 원소 5] |
| `/modality/6/subcategories/2/items/2/extracted/aftercare/0` | aftercare[0] | string | 48-72시간 음주 자제, 금연 권장(일반 건강) |
| `/modality/6/subcategories/2/items/2/extracted/aftercare/1` | aftercare[1] | string | 과도한 안면 표정 및 마사지 피하기(최소 2주) |
| `/modality/6/subcategories/2/items/2/extracted/aftercare/2` | aftercare[2] | string | 항염증제 복용(필요시) |
| `/modality/6/subcategories/2/items/2/extracted/aftercare/3` | aftercare[3] | string | 냉찜질로 부종 관리 |
| `/modality/6/subcategories/2/items/2/extracted/aftercare/4` | aftercare[4] | string | [시술 주기 참고] 실 흡수 후 재시술 고려 (PDO 6개월, PLLA 12-18개월, PCL 24-36개월). 재시술은 6개월 이상 간격 권장. 기존 실 흡수 및 콜라겐 잔존 상태 평가 후 판단 (개인차 있으며, 의사와 상의하여 결정) |

## 잠정 관찰 (원문 아님 · 직접 읽기 기록)

| 상태 | 근거 Pointer | 관찰 |
|---|---|---|
| P | `/modality/6/group`, `/modality/6/subcategories/0/label`, `/modality/6/subcategories/1/label`, `/modality/6/subcategories/2/label` | M7 group '시술/기기'(M1~M6 은 '주사/주입'). 하위분류 축이 셋으로 다르다: '재질별'(PDO·PCL·PLCL·PLLA·PCA실·PLLA+PCL복합실), '형태별'(코그·모노·볼륨실), '브랜드'(민트리프트 …). 같은 깊이 items 가 재질·형태·브랜드라는 서로 다른 종류다. |
| P | `/modality/6/subcategories/0/items/0/name`, `/modality/2/subcategories/0/label` | 재질명(PDO, PCL, PLLA)이 M7 항목 name 으로, 같은 원장의 M3 하위분류 label 로도 쓰인다. 같은 문자열이 다른 계열·다른 층에 있다(연결 키 없음). |
| P | `/modality/6/subcategories/0/items/0/detail`, `/modality/6/subcategories/0/items/3/detail` | 재질별 앞 네 항목 detail 은 빈 문자열. |
| I | `/modality/6/subcategories/0/items/1/extracted/overview`, `/modality/6/subcategories/0/items/1/extracted/aftercare/3` | PCL 항목 overview '12-15개월 지속' / duration '12-15개월' 과 M7 상용구 'PCL 24-36개월' 이 다르다. |
| I | `/modality/6/subcategories/0/items/2/extracted/overview`, `/modality/6/subcategories/0/items/2/extracted/onset_duration/duration` | PLCL: overview '12-18개월 지속' vs duration '24-36개월' — 같은 항목 안 불일치. |
| P | `/modality/6/subcategories/0/items/0/extracted/aftercare/3` | M7 상용구 '[시술 주기 참고] 실 흡수 후 재시술 고려 (PDO 6개월, PLLA 12-18개월, PCL 24-36개월). 재시술은 6개월 이상 간격 권장 …' 가 모든 항목에 반복. PDO 항목 overview 는 '6-8개월에 녹는' — 상용구 'PDO 6개월' 과 범위 차이. |
| P | `/modality/6/subcategories/1/items/0/extracted/mechanism`, `/modality/6/subcategories/2/items/1/extracted/mechanism`, `/modality/6/subcategories/2/items/2/extracted/mechanism`, `/modality/6/subcategories/0/items/3/extracted/mechanism` | '48주 (기준) 24% 조직수축' 수치 문장이 여러 항목(PLLA, 코그, 테스리프트, 실루엣소프트) mechanism 에 반복된다. |
| P | `/modality/6/subcategories/0/items/3/extracted/safety/serious/1`, `/modality/6/subcategories/1/items/0/extracted/safety/serious/3` | '비가교HA와의 동시 사용 금기(24-72시간 분해 상충)' 가 safety/serious 에 있다 — 부작용 칸에 병용 금기. 코그에는 '(in vitro 연구 기반, 임상 증거 제한적)' 근거 수준이 덧붙어 있다. |
| P | `/modality/6/subcategories/1/items/0/extracted/indications/primary/2`, `/modality/6/subcategories/0/items/3/extracted/indications/primary/4` | 얼굴 외 부위(팔뚝/허벅지, 팔·다리·복부) 적응증. |
| I | `/modality/6/subcategories/0/items/4/detail`, `/modality/6/subcategories/0/items/4/extracted/overview` | PCA실 detail '폴리카프로락톤아크릴레이트', overview '폴리카프로락톤 기반' — 재질명 표기 차이. |

## 수동 복합 표현 (원문 구간)

| Pointer | 구간 | 원문 표현 | 관점 | 메모 |
|---|---|---|---|---|
| `/modality/6/subcategories/0/items/0/extracted/overview` | [0, 16] | 6-8개월에 녹는 생분해성 실 | 수량·단위·시간, 범위 |  |
| `/modality/6/subcategories/0/items/0/extracted/aftercare/0` | [0, 25] | 48시간 음주 자제 및 금연 권장(일반 건강) | 수량·단위·시간, 부정 | M7 반복. 괄호가 지시 근거 성격 표시 |
| `/modality/6/subcategories/0/items/0/extracted/aftercare/3` | [11, 61] | 실 흡수 후 재시술 고려 (PDO 6개월, PLLA 12-18개월, PCL 24-36개월) | 조건, 수량·단위·시간 | 상용구 |
| `/modality/6/subcategories/0/items/0/extracted/aftercare/3` | [82, 109] | 기존 실 흡수 및 콜라겐 잔존 상태 평가 후 판단 | 조건 |  |
| `/modality/6/subcategories/0/items/1/extracted/mechanism` | [0, 27] | PDO보다 느린 분해 속도로 더 오래 물리적 지지 | 비교, 참조 | 다른 항목(PDO) 참조 |
| `/modality/6/subcategories/0/items/1/extracted/indications/primary/1` | [0, 16] | 장기 리프팅 효과 원하는 경우 | 조건 | 적응증 칸의 환자 희망 조건 |
| `/modality/6/subcategories/0/items/2/extracted/mechanism` | [0, 31] | PCL과 PLA의 장점을 결합하여 중간 정도의 분해 속도 | 비교, 수식 | PLA(PLLA 아님) 표기 |
| `/modality/6/subcategories/0/items/3/extracted/mechanism` | [74, 93] | 48주에 걸쳐 최대 24% 조직수축 | 수량·단위·시간, 범위 |  |
| `/modality/6/subcategories/0/items/3/extracted/safety/serious/1` | [0, 31] | 비가교HA와의 동시 사용 금기(24-72시간 분해 상충) | 부정, 조건, 수량·단위·시간 |  |
| `/modality/6/subcategories/0/items/3/extracted/aftercare/2` | [0, 21] | 48시간 내 비가교HA 제품 사용 자제 | 수량·단위·시간, 부정 | serious 는 24-72시간, aftercare 는 48시간 |
| `/modality/6/subcategories/0/items/3/extracted/aftercare/3` | [0, 15] | 냉찜질로 부종 관리(필요시) | 조건 |  |
| `/modality/6/subcategories/0/items/4/extracted/aftercare/2` | [0, 21] | 크게 입 벌리거나 강한 저작 며칠 자제 | 수식, 수량·단위·시간, 부정 |  |
| `/modality/6/subcategories/0/items/4/extracted/aftercare/4` | [0, 33] | 이상 반응(감염 징후, 실 노출, 심한 통증) 시 즉시 내원 | 조건 |  |
| `/modality/6/subcategories/0/items/5/extracted/onset_duration/onset` | [0, 15] | 즉시 (최대 효과 4-6주) | 수량·단위·시간, 범위 |  |
| `/modality/6/subcategories/1/items/0/detail` | [0, 13] | 양방향/단방향 · 견인력 | 기호 | '/' 대안(형태 변형) |
| `/modality/6/subcategories/1/items/0/extracted/overview` | [39, 53] | supraSMAS 층 배치 | 부위 | 해부층 |
| `/modality/6/subcategories/1/items/0/extracted/mechanism` | [73, 116] | 소재별 분해 기간(PDO 6개월/PLLA 12-18개월/PCL 24-36개월) | 수량·단위·시간, 기호 | '/' 나열 |
| `/modality/6/subcategories/1/items/0/extracted/safety/serious/2` | [0, 13] | 부당한 거상(코그 이탈) | 수식 |  |
| `/modality/6/subcategories/1/items/0/extracted/safety/serious/3` | [0, 60] | PDO+비가교HA 병용 금기(24-72시간 급속분해 위험) (in vitro 연구 기반, 임상 증거 제한적) | 부정, 기호, 주장, 수량·단위·시간 | '+' = 병용 |
| `/modality/6/subcategories/1/items/0/extracted/onset_duration/onset` | [0, 29] | 즉각(물리적 거상) / 점진적(콜라겐 형성 2-4주) | 수량·단위·시간, 기호 | '/' 두 단계 병기 |
| `/modality/6/subcategories/1/items/0/extracted/aftercare/4` | [0, 16] | 비가교HA 제품 72시간 금기 | 수량·단위·시간, 부정 |  |
| `/modality/6/subcategories/1/items/1/extracted/mechanism` | [0, 16] | 톱니가 없어 통증이 적으면서도 | 부정, 비교 |  |
| `/modality/6/subcategories/1/items/2/extracted/indications/primary/0` | [0, 9] | 볼 꺼짐 + 처짐 | 부위, 기호 | '+' = 함께 |
| `/modality/6/subcategories/2/items/0/extracted/mechanism` | [41, 56] | PDO 또는 PLLA 재질로 | 조건 | 대안 |
| `/modality/6/subcategories/2/items/1/extracted/onset_duration/duration` | [0, 30] | 6-9개월 (PDO), 콜라겐 재생 효과 12-18개월 | 수량·단위·시간, 범위 |  |
| `/modality/6/subcategories/2/items/2/extracted/aftercare/1` | [0, 26] | 과도한 안면 표정 및 마사지 피하기(최소 2주) | 범위, 부정, 수량·단위·시간 |  |
| `/modality/6/subcategories/2/items/2/extracted/aftercare/2` | [0, 12] | 항염증제 복용(필요시) | 조건 |  |

## 형태소 분석 확인 (알려진 오분절 K)

| 범위 | 표면형 | 문제 | 영향 |
|---|---|---|---|
| all | 비가교HA | 비가교/NNP HA, 비/NNG 가교/NNG HA, 비가교/NNG HA 로 문맥별 상이 — 부정 접두 '비' 가 분리되기도 한다 | '비(非)' 부정 의미가 토큰 단위로 일관되지 않음 |
| all | 마리오네트라인 | 마리오네트/NNP 라인/NNG | 부위 표현 분해(복합 표현으로 보존) |

## 미결

| ID | 상태 | Pointer | 내용 | 영향·후속 |
|---|---|---|---|---|
| S016-I01 | I | `/modality/6/subcategories/0/items/2/extracted/overview`, `/modality/6/subcategories/0/items/2/extracted/onset_duration/duration` | PLCL overview 12-18개월 vs duration 24-36개월. | 기간 채택 시 확인 |
| S016-I02 | I | `/modality/6/subcategories/0/items/1/extracted/onset_duration/duration`, `/modality/6/subcategories/0/items/1/extracted/aftercare/3` | PCL 12-15개월 vs 상용구 24-36개월. | GLOBAL-I01 |
| S016-F01 | F | `/modality/6/subcategories/0`, `/modality/6/subcategories/1`, `/modality/6/subcategories/2` | 재질·형태·브랜드 세 축이 같은 깊이에 병렬. 브랜드 항목이 어느 재질·형태인지는 detail 문자열에만 있다. | 축 분해는 설계 단계 |

