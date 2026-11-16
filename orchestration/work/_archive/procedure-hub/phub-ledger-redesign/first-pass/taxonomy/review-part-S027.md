# S027 — M9 기기 리프팅

- 읽기 상태: **read** · 마지막 읽은 Pointer `/modality/8/subcategories/0/items/11/extracted/aftercare/3`
- 단위: id, category, category_en, group, subcategories 컨테이너, M9-1 items/0, M9-1 items/1, M9-1 items/2, M9-1 items/3, M9-1 items/4, M9-1 items/5, M9-1 items/6, M9-1 items/7, M9-1 items/8, M9-1 items/9, M9-1 items/10, M9-1 items/11
- 상위 문맥(공동 참조·소유 아님): 없음
- 기계 기록: `source-map.json`(section=S027) · `morphology/S027.json` · `expressions.json`(section=S027) · 읽기 렌더 `reading/S027.txt`

## 원문 값 (원본 컬럼명 그대로, 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/modality/8` | modality[8] | object | {object, 키 8: id, category, category_en, group, subcategories, extracted, products, name} |
| `/modality/8/id` | id | string | M9 |
| `/modality/8/category` | category | string | 기기 리프팅 |
| `/modality/8/category_en` | category_en | string | Energy Based Device Lifting |
| `/modality/8/group` | group | string | 시술/기기 |
| `/modality/8/subcategories` | subcategories | array | [array, 원소 5] |
| `/modality/8/subcategories/0` | subcategories[0] | object | {object, 키 3: id, label, items} |
| `/modality/8/subcategories/0/id` | id | string | M9-1 |
| `/modality/8/subcategories/0/label` | label | string | HIFU (초음파) |
| `/modality/8/subcategories/0/items` | items | array | [array, 원소 16] |
| `/modality/8/subcategories/0/items/0` | items[0] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/8/subcategories/0/items/0/id` | id | string | M9-1-1 |
| `/modality/8/subcategories/0/items/0/name` | name | string | 울쎄라 |
| `/modality/8/subcategories/0/items/0/detail` | detail | string | 멀츠 · 오리지널 HIFU |
| `/modality/8/subcategories/0/items/0/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/8/subcategories/0/items/0/extracted/overview` | overview | string | 집속초음파 에너지를 정밀하게 SMAS층에 전달하여 즉각적인 리프팅 효과를 제공하는 비침습적 시술 |
| `/modality/8/subcategories/0/items/0/extracted/mechanism` | mechanism | string | HIFU(High Intensity Focused Ultrasound)가 60°C의 고열을 발생시켜 표적 조직을 응고괴사하고 콜라겐 수축을 유도합니다. 동시에 신생콜라겐 생성을 자극하여 장기적인 피부 탄력 개선을 실현합니다. 음향 캐비테이션(acoustic cavitation)으로 세포 구조를 추가 파괴하여 효과를 강화한다. 유일하게 US FDA 승인된 HIFU 기기로 실시간 초음파 영상화(visualization) 기능을 갖추고 있다. |
| `/modality/8/subcategories/0/items/0/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/8/subcategories/0/items/0/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/8/subcategories/0/items/0/extracted/indications/primary/0` | primary[0] | string | 안면 처짐 및 리프팅 |
| `/modality/8/subcategories/0/items/0/extracted/indications/primary/1` | primary[1] | string | 눈가 주름 개선 |
| `/modality/8/subcategories/0/items/0/extracted/indications/primary/2` | primary[2] | string | 목 처짐 |
| `/modality/8/subcategories/0/items/0/extracted/indications/primary/3` | primary[3] | string | 턱선 강화 |
| `/modality/8/subcategories/0/items/0/extracted/indications/primary/4` | primary[4] | string | 미간 주름 |
| `/modality/8/subcategories/0/items/0/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/8/subcategories/0/items/0/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/8/subcategories/0/items/0/extracted/safety/common/0` | common[0] | string | 일시적 홍반 |
| `/modality/8/subcategories/0/items/0/extracted/safety/common/1` | common[1] | string | 미열감 |
| `/modality/8/subcategories/0/items/0/extracted/safety/common/2` | common[2] | string | 부종 |
| `/modality/8/subcategories/0/items/0/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/8/subcategories/0/items/0/extracted/safety/serious/0` | serious[0] | string | 신경 손상 |
| `/modality/8/subcategories/0/items/0/extracted/safety/serious/1` | serious[1] | string | 화상 |
| `/modality/8/subcategories/0/items/0/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/8/subcategories/0/items/0/extracted/onset_duration/onset` | onset | string | 시술 직후 즉시 수축 효과, 3개월에 걸쳐 점진적 개선 |
| `/modality/8/subcategories/0/items/0/extracted/onset_duration/duration` | duration | string | 6-12개월 지속, 개인차 존재 |
| `/modality/8/subcategories/0/items/0/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/8/subcategories/0/items/0/extracted/aftercare/0` | aftercare[0] | string | 시술 후 24시간 고온 환경(사우나, 찜질방) 회피 |
| `/modality/8/subcategories/0/items/0/extracted/aftercare/1` | aftercare[1] | string | 강한 마사지 당일 자제 |
| `/modality/8/subcategories/0/items/0/extracted/aftercare/2` | aftercare[2] | string | 충분한 수분 섭취 |
| `/modality/8/subcategories/0/items/0/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 고출력 EBD — 최소 6개월 이상 간격 권장. 콜라겐 리모델링 완료(3-6개월)를 기다린 후 효과 평가. 리모델링 중 재시술은 과도한 열 누적/지방위축 위험. 아무리 빨라도 1개월 이상 간격 필수 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/8/subcategories/0/items/1` | items[1] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/8/subcategories/0/items/1/id` | id | string | M9-1-2 |
| `/modality/8/subcategories/0/items/1/name` | name | string | 울쎄라피프라임 |
| `/modality/8/subcategories/0/items/1/detail` | detail | string | 멀츠 · 신형 |
| `/modality/8/subcategories/0/items/1/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/8/subcategories/0/items/1/extracted/overview` | overview | string | 최신형 HIFU 기술로 SMAS층까지 집중 에너지를 전달하여 즉각적인 리프팅 효과를 제공하는 신세대 초음파 미용기기 |
| `/modality/8/subcategories/0/items/1/extracted/mechanism` | mechanism | string | 집속초음파(HIFU)가 피부 진피-피하층(3mm)과 SMAS층(4.5mm)에 정확히 도달하여 60°C의 열로 콜라겐을 응고괴사시킵니다. 손상된 콜라겐의 수축과 동시에 신생콜라겐 생성을 촉진하여 피부 탄력 강화 및 처짐 개선 효과를 제공합니다. |
| `/modality/8/subcategories/0/items/1/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/8/subcategories/0/items/1/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/8/subcategories/0/items/1/extracted/indications/primary/0` | primary[0] | string | 얼굴 처짐 및 탄력 저하 |
| `/modality/8/subcategories/0/items/1/extracted/indications/primary/1` | primary[1] | string | 목 주름 및 처짐 |
| `/modality/8/subcategories/0/items/1/extracted/indications/primary/2` | primary[2] | string | 광대뼈 처짐 |
| `/modality/8/subcategories/0/items/1/extracted/indications/primary/3` | primary[3] | string | 턱선 정의 |
| `/modality/8/subcategories/0/items/1/extracted/indications/primary/4` | primary[4] | string | 팔뚝/허벅지 처짐 |
| `/modality/8/subcategories/0/items/1/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/8/subcategories/0/items/1/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/8/subcategories/0/items/1/extracted/safety/common/0` | common[0] | string | 시술 직후 홍반 |
| `/modality/8/subcategories/0/items/1/extracted/safety/common/1` | common[1] | string | 경미한 부종 |
| `/modality/8/subcategories/0/items/1/extracted/safety/common/2` | common[2] | string | 따끔거림 감각 |
| `/modality/8/subcategories/0/items/1/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/8/subcategories/0/items/1/extracted/safety/serious/0` | serious[0] | string | 신경 손상(극히 드문) |
| `/modality/8/subcategories/0/items/1/extracted/safety/serious/1` | serious[1] | string | 피부화상(깊이 조절 오류시) |
| `/modality/8/subcategories/0/items/1/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/8/subcategories/0/items/1/extracted/onset_duration/onset` | onset | string | 즉시 효과 인지 가능, 최적 효과는 8주-3개월 |
| `/modality/8/subcategories/0/items/1/extracted/onset_duration/duration` | duration | string | 6-12개월 유지, 개인차에 따라 변동 |
| `/modality/8/subcategories/0/items/1/extracted/aftercare` | aftercare | array | [array, 원소 5] |
| `/modality/8/subcategories/0/items/1/extracted/aftercare/0` | aftercare[0] | string | 24시간 이내 뜨거운 물 접촉 자제 |
| `/modality/8/subcategories/0/items/1/extracted/aftercare/1` | aftercare[1] | string | 3일간 자극적 스킨케어 제품 사용 자제 |
| `/modality/8/subcategories/0/items/1/extracted/aftercare/2` | aftercare[2] | string | 부종 시 냉찜질 시행 |
| `/modality/8/subcategories/0/items/1/extracted/aftercare/3` | aftercare[3] | string | 필요시 진통제 복용 가능 |
| `/modality/8/subcategories/0/items/1/extracted/aftercare/4` | aftercare[4] | string | [시술 주기 참고] 고출력 EBD — 최소 6개월 이상 간격 권장. 콜라겐 리모델링 완료(3-6개월)를 기다린 후 효과 평가. 리모델링 중 재시술은 과도한 열 누적/지방위축 위험. 아무리 빨라도 1개월 이상 간격 필수 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/8/subcategories/0/items/2` | items[2] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/8/subcategories/0/items/2/id` | id | string | M9-1-3 |
| `/modality/8/subcategories/0/items/2/name` | name | string | 슈링크 |
| `/modality/8/subcategories/0/items/2/detail` | detail | string | 클래시스 |
| `/modality/8/subcategories/0/items/2/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/8/subcategories/0/items/2/extracted/overview` | overview | string | HIFU(고강도 집속 초음파) 리프팅 기기 |
| `/modality/8/subcategories/0/items/2/extracted/mechanism` | mechanism | string | 고강도 집속 초음파(HIFU)를 피부 특정 깊이(진피 1.5/3.0mm, SMAS 4.5mm)에 집중시켜 60°C 이상의 열응고점(TIZ)을 형성한다. 음향 캐비테이션과 열 응고로 콜라겐 수축 및 신생콜라겐 생성을 유도하여 리프팅 효과를 제공한다. |
| `/modality/8/subcategories/0/items/2/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/8/subcategories/0/items/2/extracted/indications/primary` | primary | array | [array, 원소 4] |
| `/modality/8/subcategories/0/items/2/extracted/indications/primary/0` | primary[0] | string | 얼굴 및 목 처짐 |
| `/modality/8/subcategories/0/items/2/extracted/indications/primary/1` | primary[1] | string | 팔뚝/허벅지 피부 탄력 감소 |
| `/modality/8/subcategories/0/items/2/extracted/indications/primary/2` | primary[2] | string | 복부 처짐 |
| `/modality/8/subcategories/0/items/2/extracted/indications/primary/3` | primary[3] | string | 이중턱 |
| `/modality/8/subcategories/0/items/2/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/8/subcategories/0/items/2/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/8/subcategories/0/items/2/extracted/safety/common/0` | common[0] | string | 일시적 홍반 |
| `/modality/8/subcategories/0/items/2/extracted/safety/common/1` | common[1] | string | 가벼운 부종 |
| `/modality/8/subcategories/0/items/2/extracted/safety/common/2` | common[2] | string | 시술 후 따끔거림 |
| `/modality/8/subcategories/0/items/2/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/8/subcategories/0/items/2/extracted/safety/serious/0` | serious[0] | string | 화상 |
| `/modality/8/subcategories/0/items/2/extracted/safety/serious/1` | serious[1] | string | 신경 손상 |
| `/modality/8/subcategories/0/items/2/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/8/subcategories/0/items/2/extracted/onset_duration/onset` | onset | string | 즉시 효과 시작, 4-6주 콜라겐 재생으로 최대 효과 |
| `/modality/8/subcategories/0/items/2/extracted/onset_duration/duration` | duration | string | 6-12개월 지속, 효과 소실 시 재시술 고려 |
| `/modality/8/subcategories/0/items/2/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/8/subcategories/0/items/2/extracted/aftercare/0` | aftercare[0] | string | 72시간 고온 노출 및 격렬한 운동 자제 |
| `/modality/8/subcategories/0/items/2/extracted/aftercare/1` | aftercare[1] | string | 가벼운 보습제 사용 |
| `/modality/8/subcategories/0/items/2/extracted/aftercare/2` | aftercare[2] | string | 홍반 시 진정 마스크팩 권장 |
| `/modality/8/subcategories/0/items/2/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 중출력 EBD — 3-6개월 간격 권장. 콜라겐 리모델링 진행 상황 평가 후 재시술 판단. 아무리 빨라도 1개월 이상 간격 필수 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/8/subcategories/0/items/3` | items[3] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/8/subcategories/0/items/3/id` | id | string | M9-1-4 |
| `/modality/8/subcategories/0/items/3/name` | name | string | 슈링크유니버스 |
| `/modality/8/subcategories/0/items/3/detail` | detail | string | 클래시스 · 신형 |
| `/modality/8/subcategories/0/items/3/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/8/subcategories/0/items/3/extracted/overview` | overview | string | HIFU 전용 리프팅 기기 (클래시스) |
| `/modality/8/subcategories/0/items/3/extracted/mechanism` | mechanism | string | 집속초음파(HIFU)가 정밀한 깊이(진피 1.5/3.0mm, SMAS 4.5mm)에 60°C 이상의 열응고점(TIZ)을 형성하여 콜라겐 수축 및 신생콜라겐 생성을 유도한다. Pre-focal zone에서도 추가 열손상이 발생하여 임상 효과에 기여한다. |
| `/modality/8/subcategories/0/items/3/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/8/subcategories/0/items/3/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/8/subcategories/0/items/3/extracted/indications/primary/0` | primary[0] | string | 얼굴 처짐 및 탄력 저하 |
| `/modality/8/subcategories/0/items/3/extracted/indications/primary/1` | primary[1] | string | 팔자주름 및 마리오네트라인 |
| `/modality/8/subcategories/0/items/3/extracted/indications/primary/2` | primary[2] | string | 목 주름 및 이중턱 |
| `/modality/8/subcategories/0/items/3/extracted/indications/primary/3` | primary[3] | string | 광대뼈 처짐 |
| `/modality/8/subcategories/0/items/3/extracted/indications/primary/4` | primary[4] | string | 전반적인 페이스리프팅 |
| `/modality/8/subcategories/0/items/3/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/8/subcategories/0/items/3/extracted/safety/common` | common | array | [array, 원소 4] |
| `/modality/8/subcategories/0/items/3/extracted/safety/common/0` | common[0] | string | 시술 직후 홍반 |
| `/modality/8/subcategories/0/items/3/extracted/safety/common/1` | common[1] | string | 부종 |
| `/modality/8/subcategories/0/items/3/extracted/safety/common/2` | common[2] | string | 경미한 열감 |
| `/modality/8/subcategories/0/items/3/extracted/safety/common/3` | common[3] | string | 건조함 |
| `/modality/8/subcategories/0/items/3/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/8/subcategories/0/items/3/extracted/safety/serious/0` | serious[0] | string | 신경 손상(희귀) |
| `/modality/8/subcategories/0/items/3/extracted/safety/serious/1` | serious[1] | string | 화상(부적절한 설정 시) |
| `/modality/8/subcategories/0/items/3/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/8/subcategories/0/items/3/extracted/onset_duration/onset` | onset | string | 2-4주 콜라겐 재생 시작, 즉각적 수축 효과 |
| `/modality/8/subcategories/0/items/3/extracted/onset_duration/duration` | duration | string | 6-12개월 지속(개인차 있음) |
| `/modality/8/subcategories/0/items/3/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/8/subcategories/0/items/3/extracted/aftercare/0` | aftercare[0] | string | 24시간 고온 환경(사우나, 찜질방) 회피 |
| `/modality/8/subcategories/0/items/3/extracted/aftercare/1` | aftercare[1] | string | 과도한 자극 피하기 |
| `/modality/8/subcategories/0/items/3/extracted/aftercare/2` | aftercare[2] | string | 충분한 수분섭취 |
| `/modality/8/subcategories/0/items/3/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 고출력 EBD — 최소 6개월 이상 간격 권장. 콜라겐 리모델링 완료(3-6개월)를 기다린 후 효과 평가. 리모델링 중 재시술은 과도한 열 누적/지방위축 위험. 아무리 빨라도 1개월 이상 간격 필수 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/8/subcategories/0/items/4` | items[4] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/8/subcategories/0/items/4/id` | id | string | M9-1-5 |
| `/modality/8/subcategories/0/items/4/name` | name | string | 더블로 |
| `/modality/8/subcategories/0/items/4/detail` | detail | string | 하이로닉 |
| `/modality/8/subcategories/0/items/4/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/8/subcategories/0/items/4/extracted/overview` | overview | string | 집속초음파(HIFU) 기술을 이용한 비침습적 안면 리프팅 및 탄력 개선 치료기 |
| `/modality/8/subcategories/0/items/4/extracted/mechanism` | mechanism | string | 고강도 집속초음파가 진피층과 SMAS층에 정밀하게 도달하여 60°C 이상의 열로 콜라겐 응고괴사를 유도합니다. 즉각적인 콜라겐 수축과 함께 신생콜라겐 생성을 촉진하여 장기적인 피부 탄력 개선을 실현합니다. |
| `/modality/8/subcategories/0/items/4/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/8/subcategories/0/items/4/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/8/subcategories/0/items/4/extracted/indications/primary/0` | primary[0] | string | 얼굴 처짐 및 탄력 저하 |
| `/modality/8/subcategories/0/items/4/extracted/indications/primary/1` | primary[1] | string | 눈가 주름 개선 |
| `/modality/8/subcategories/0/items/4/extracted/indications/primary/2` | primary[2] | string | 턱선 및 페이스라인 개선 |
| `/modality/8/subcategories/0/items/4/extracted/indications/primary/3` | primary[3] | string | 이마 주름 |
| `/modality/8/subcategories/0/items/4/extracted/indications/primary/4` | primary[4] | string | 목 처짐 |
| `/modality/8/subcategories/0/items/4/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/8/subcategories/0/items/4/extracted/safety/common` | common | array | [array, 원소 4] |
| `/modality/8/subcategories/0/items/4/extracted/safety/common/0` | common[0] | string | 일시적 발적 |
| `/modality/8/subcategories/0/items/4/extracted/safety/common/1` | common[1] | string | 부종 |
| `/modality/8/subcategories/0/items/4/extracted/safety/common/2` | common[2] | string | 따끔거림 |
| `/modality/8/subcategories/0/items/4/extracted/safety/common/3` | common[3] | string | 피부 건조증 |
| `/modality/8/subcategories/0/items/4/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/8/subcategories/0/items/4/extracted/safety/serious/0` | serious[0] | string | 신경 손상 (극히 드물음) |
| `/modality/8/subcategories/0/items/4/extracted/safety/serious/1` | serious[1] | string | 화상 |
| `/modality/8/subcategories/0/items/4/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/8/subcategories/0/items/4/extracted/onset_duration/onset` | onset | string | 즉각적 콜라겐 수축 후 2-3주부터 개선 체감 |
| `/modality/8/subcategories/0/items/4/extracted/onset_duration/duration` | duration | string | 3-6개월 지속, 개인차에 따라 최대 12개월 |
| `/modality/8/subcategories/0/items/4/extracted/aftercare` | aftercare | array | [array, 원소 5] |
| `/modality/8/subcategories/0/items/4/extracted/aftercare/0` | aftercare[0] | string | 시술 후 24시간 이상 강한 자극 피하기 |
| `/modality/8/subcategories/0/items/4/extracted/aftercare/1` | aftercare[1] | string | 과도한 운동 및 사우나 1주일 자제 |
| `/modality/8/subcategories/0/items/4/extracted/aftercare/2` | aftercare[2] | string | 충분한 보습 관리 |
| `/modality/8/subcategories/0/items/4/extracted/aftercare/3` | aftercare[3] | string | 필요시 진정 팩 사용 |
| `/modality/8/subcategories/0/items/4/extracted/aftercare/4` | aftercare[4] | string | [시술 주기 참고] 중출력 EBD — 3-6개월 간격 권장. 콜라겐 리모델링 진행 상황 평가 후 재시술 판단. 아무리 빨라도 1개월 이상 간격 필수 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/8/subcategories/0/items/5` | items[5] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/8/subcategories/0/items/5/id` | id | string | M9-1-6 |
| `/modality/8/subcategories/0/items/5/name` | name | string | 더블로골드 |
| `/modality/8/subcategories/0/items/5/detail` | detail | string | 하이로닉 · 신형 |
| `/modality/8/subcategories/0/items/5/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/8/subcategories/0/items/5/extracted/overview` | overview | string | HIFU(고강도 집속 초음파) 리프팅 기기 |
| `/modality/8/subcategories/0/items/5/extracted/mechanism` | mechanism | string | 고강도 집속 초음파(HIFU)를 피부 특정 깊이(진피 1.5/3.0mm, SMAS 4.5mm)에 집중시켜 60°C 이상의 열응고점(TIZ)을 형성한다. 음향 캐비테이션과 열 응고로 콜라겐 수축 및 신생콜라겐 생성을 유도하여 리프팅 효과를 제공한다. |
| `/modality/8/subcategories/0/items/5/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/8/subcategories/0/items/5/extracted/indications/primary` | primary | array | [array, 원소 5] |
| `/modality/8/subcategories/0/items/5/extracted/indications/primary/0` | primary[0] | string | 얼굴 및 목 처짐 |
| `/modality/8/subcategories/0/items/5/extracted/indications/primary/1` | primary[1] | string | 이마 주름 |
| `/modality/8/subcategories/0/items/5/extracted/indications/primary/2` | primary[2] | string | 팔자주름 |
| `/modality/8/subcategories/0/items/5/extracted/indications/primary/3` | primary[3] | string | 턱선 정의 |
| `/modality/8/subcategories/0/items/5/extracted/indications/primary/4` | primary[4] | string | 피부 탄력 저하 |
| `/modality/8/subcategories/0/items/5/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/8/subcategories/0/items/5/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/8/subcategories/0/items/5/extracted/safety/common/0` | common[0] | string | 시술 후 홍반 |
| `/modality/8/subcategories/0/items/5/extracted/safety/common/1` | common[1] | string | 부종 |
| `/modality/8/subcategories/0/items/5/extracted/safety/common/2` | common[2] | string | 일시적 감각 이상 |
| `/modality/8/subcategories/0/items/5/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/8/subcategories/0/items/5/extracted/safety/serious/0` | serious[0] | string | 신경손상(희귀) |
| `/modality/8/subcategories/0/items/5/extracted/safety/serious/1` | serious[1] | string | 화상(부적절한 설정시) |
| `/modality/8/subcategories/0/items/5/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/8/subcategories/0/items/5/extracted/onset_duration/onset` | onset | string | 즉각적 효과 1주, 최대 효과 12주 |
| `/modality/8/subcategories/0/items/5/extracted/onset_duration/duration` | duration | string | 6-12개월 |
| `/modality/8/subcategories/0/items/5/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/8/subcategories/0/items/5/extracted/aftercare/0` | aftercare[0] | string | 시술 후 48시간 고온 환경 회피 |
| `/modality/8/subcategories/0/items/5/extracted/aftercare/1` | aftercare[1] | string | 과도한 얼굴 강한 마사지 당일 자제 |
| `/modality/8/subcategories/0/items/5/extracted/aftercare/2` | aftercare[2] | string | 냉찜질로 부종 완화 |
| `/modality/8/subcategories/0/items/5/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 중출력 EBD — 3-6개월 간격 권장. 콜라겐 리모델링 진행 상황 평가 후 재시술 판단. 아무리 빨라도 1개월 이상 간격 필수 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/8/subcategories/0/items/6` | items[6] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/8/subcategories/0/items/6/id` | id | string | M9-1-8 |
| `/modality/8/subcategories/0/items/6/name` | name | string | 리프테라 |
| `/modality/8/subcategories/0/items/6/detail` | detail | string | 아스테라시스 |
| `/modality/8/subcategories/0/items/6/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/8/subcategories/0/items/6/extracted/overview` | overview | string | HIFU(고강도 집속 초음파) 리프팅 기기 |
| `/modality/8/subcategories/0/items/6/extracted/mechanism` | mechanism | string | 고강도 집속 초음파(HIFU)를 피부 특정 깊이(진피 1.5/3.0mm, SMAS 4.5mm)에 집중시켜 60°C 이상의 열응고점(TIZ)을 형성한다. 음향 캐비테이션과 열 응고로 콜라겐 수축 및 신생콜라겐 생성을 유도하여 리프팅 효과를 제공한다. |
| `/modality/8/subcategories/0/items/6/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/8/subcategories/0/items/6/extracted/indications/primary` | primary | array | [array, 원소 4] |
| `/modality/8/subcategories/0/items/6/extracted/indications/primary/0` | primary[0] | string | 안면 및 목 피부 처짐 |
| `/modality/8/subcategories/0/items/6/extracted/indications/primary/1` | primary[1] | string | 팔뚝 및 복부 탄력 저하 |
| `/modality/8/subcategories/0/items/6/extracted/indications/primary/2` | primary[2] | string | 피부 주름 개선 |
| `/modality/8/subcategories/0/items/6/extracted/indications/primary/3` | primary[3] | string | 전반적인 피부 탄력 강화 |
| `/modality/8/subcategories/0/items/6/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/8/subcategories/0/items/6/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/8/subcategories/0/items/6/extracted/safety/common/0` | common[0] | string | 시술 후 일시적 홍반 |
| `/modality/8/subcategories/0/items/6/extracted/safety/common/1` | common[1] | string | 부종 |
| `/modality/8/subcategories/0/items/6/extracted/safety/common/2` | common[2] | string | 따뜻함 또는 작열감 |
| `/modality/8/subcategories/0/items/6/extracted/safety/serious` | serious | array | [array, 원소 3] |
| `/modality/8/subcategories/0/items/6/extracted/safety/serious/0` | serious[0] | string | 화상 |
| `/modality/8/subcategories/0/items/6/extracted/safety/serious/1` | serious[1] | string | 색소침착 |
| `/modality/8/subcategories/0/items/6/extracted/safety/serious/2` | serious[2] | string | 신경 손상 |
| `/modality/8/subcategories/0/items/6/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/8/subcategories/0/items/6/extracted/onset_duration/onset` | onset | string | 1-2주 후부터 콜라겐 신생에 의한 개선 시작 |
| `/modality/8/subcategories/0/items/6/extracted/onset_duration/duration` | duration | string | 3-6개월 지속, 반복 시 누적 효과 가능 |
| `/modality/8/subcategories/0/items/6/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/8/subcategories/0/items/6/extracted/aftercare/0` | aftercare[0] | string | 시술 직후 냉찜질 권장 |
| `/modality/8/subcategories/0/items/6/extracted/aftercare/1` | aftercare[1] | string | 고온 환경 노출 48시간 회피 |
| `/modality/8/subcategories/0/items/6/extracted/aftercare/2` | aftercare[2] | string | 자극적 스킨케어 제품 1주일 자제 |
| `/modality/8/subcategories/0/items/6/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 중출력 EBD — 3-6개월 간격 권장. 콜라겐 리모델링 진행 상황 평가 후 재시술 판단. 아무리 빨라도 1개월 이상 간격 필수 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/8/subcategories/0/items/7` | items[7] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/8/subcategories/0/items/7/id` | id | string | M9-1-9 |
| `/modality/8/subcategories/0/items/7/name` | name | string | 리니어펌 |
| `/modality/8/subcategories/0/items/7/detail` | detail | string | 제이시스 |
| `/modality/8/subcategories/0/items/7/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/8/subcategories/0/items/7/extracted/overview` | overview | string | HIFU(고강도 집속 초음파) 리프팅 기기 |
| `/modality/8/subcategories/0/items/7/extracted/mechanism` | mechanism | string | 고강도 집속 초음파(HIFU)를 피부 특정 깊이(진피 1.5/3.0mm, SMAS 4.5mm)에 집중시켜 60°C 이상의 열응고점(TIZ)을 형성한다. 음향 캐비테이션과 열 응고로 콜라겐 수축 및 신생콜라겐 생성을 유도하여 리프팅 효과를 제공한다. |
| `/modality/8/subcategories/0/items/7/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/8/subcategories/0/items/7/extracted/indications/primary` | primary | array | [array, 원소 4] |
| `/modality/8/subcategories/0/items/7/extracted/indications/primary/0` | primary[0] | string | 얼굴 처짐 및 탄력 저하 |
| `/modality/8/subcategories/0/items/7/extracted/indications/primary/1` | primary[1] | string | 법령선 및 팔자주름 |
| `/modality/8/subcategories/0/items/7/extracted/indications/primary/2` | primary[2] | string | 턱선 강화 |
| `/modality/8/subcategories/0/items/7/extracted/indications/primary/3` | primary[3] | string | 얼굴 윤곽 개선 |
| `/modality/8/subcategories/0/items/7/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/8/subcategories/0/items/7/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/8/subcategories/0/items/7/extracted/safety/common/0` | common[0] | string | 시술 후 일시적 홍반 |
| `/modality/8/subcategories/0/items/7/extracted/safety/common/1` | common[1] | string | 따뜻함 또는 미온감 |
| `/modality/8/subcategories/0/items/7/extracted/safety/common/2` | common[2] | string | 부종 |
| `/modality/8/subcategories/0/items/7/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/8/subcategories/0/items/7/extracted/safety/serious/0` | serious[0] | string | 화상 |
| `/modality/8/subcategories/0/items/7/extracted/safety/serious/1` | serious[1] | string | 신경 손상 |
| `/modality/8/subcategories/0/items/7/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/8/subcategories/0/items/7/extracted/onset_duration/onset` | onset | string | 즉시 효과 시작, 3개월 최고 효과 |
| `/modality/8/subcategories/0/items/7/extracted/onset_duration/duration` | duration | string | 6-12개월 |
| `/modality/8/subcategories/0/items/7/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/8/subcategories/0/items/7/extracted/aftercare/0` | aftercare[0] | string | 시술 후 24시간 고온(사우나, 찜질방) 피하기 |
| `/modality/8/subcategories/0/items/7/extracted/aftercare/1` | aftercare[1] | string | 일주일 간 자극적 제품 사용 제한 |
| `/modality/8/subcategories/0/items/7/extracted/aftercare/2` | aftercare[2] | string | [시술 주기 참고] 중출력 EBD — 3-6개월 간격 권장. 콜라겐 리모델링 진행 상황 평가 후 재시술 판단. 아무리 빨라도 1개월 이상 간격 필수 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/8/subcategories/0/items/8` | items[8] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/8/subcategories/0/items/8/id` | id | string | M9-1-10 |
| `/modality/8/subcategories/0/items/8/name` | name | string | 텐쎄라 |
| `/modality/8/subcategories/0/items/8/detail` | detail | string | 원텍 |
| `/modality/8/subcategories/0/items/8/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/8/subcategories/0/items/8/extracted/overview` | overview | string | HIFU(고강도 집속 초음파) 리프팅 기기 |
| `/modality/8/subcategories/0/items/8/extracted/mechanism` | mechanism | string | 고강도 집속 초음파(HIFU)를 피부 특정 깊이(진피 1.5/3.0mm, SMAS 4.5mm)에 집중시켜 60°C 이상의 열응고점(TIZ)을 형성한다. 음향 캐비테이션과 열 응고로 콜라겐 수축 및 신생콜라겐 생성을 유도하여 리프팅 효과를 제공한다. |
| `/modality/8/subcategories/0/items/8/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/8/subcategories/0/items/8/extracted/indications/primary` | primary | array | [array, 원소 4] |
| `/modality/8/subcategories/0/items/8/extracted/indications/primary/0` | primary[0] | string | 안면 처짐 및 리프팅 |
| `/modality/8/subcategories/0/items/8/extracted/indications/primary/1` | primary[1] | string | 피부 탄력 저하 |
| `/modality/8/subcategories/0/items/8/extracted/indications/primary/2` | primary[2] | string | 주름 개선 |
| `/modality/8/subcategories/0/items/8/extracted/indications/primary/3` | primary[3] | string | 피부 결 정리 |
| `/modality/8/subcategories/0/items/8/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/8/subcategories/0/items/8/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/8/subcategories/0/items/8/extracted/safety/common/0` | common[0] | string | 시술 후 열감 |
| `/modality/8/subcategories/0/items/8/extracted/safety/common/1` | common[1] | string | 경미한 부종 |
| `/modality/8/subcategories/0/items/8/extracted/safety/common/2` | common[2] | string | 피부 발적 |
| `/modality/8/subcategories/0/items/8/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/8/subcategories/0/items/8/extracted/safety/serious/0` | serious[0] | string | 화상 |
| `/modality/8/subcategories/0/items/8/extracted/safety/serious/1` | serious[1] | string | 신경 손상 |
| `/modality/8/subcategories/0/items/8/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/8/subcategories/0/items/8/extracted/onset_duration/onset` | onset | string | 시술 직후부터 즉시 효과 체감, 1-3개월에 걸쳐 콜라겐 재생으로 최대 효과 |
| `/modality/8/subcategories/0/items/8/extracted/onset_duration/duration` | duration | string | 6-12개월 지속 (개인차 발생) |
| `/modality/8/subcategories/0/items/8/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/8/subcategories/0/items/8/extracted/aftercare/0` | aftercare[0] | string | 시술 후 24시간 고온 환경(사우나, 찜질방) 피하기 |
| `/modality/8/subcategories/0/items/8/extracted/aftercare/1` | aftercare[1] | string | 자극적인 스킨케어 제품 최소 1주일 피하기 |
| `/modality/8/subcategories/0/items/8/extracted/aftercare/2` | aftercare[2] | string | [시술 주기 참고] 중출력 EBD — 3-6개월 간격 권장. 콜라겐 리모델링 진행 상황 평가 후 재시술 판단. 아무리 빨라도 1개월 이상 간격 필수 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/8/subcategories/0/items/9` | items[9] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/8/subcategories/0/items/9/id` | id | string | auto-37-1774737181584 |
| `/modality/8/subcategories/0/items/9/name` | name | string | 쿨소닉 |
| `/modality/8/subcategories/0/items/9/detail` | detail | string | 아스테라시스 |
| `/modality/8/subcategories/0/items/9/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/8/subcategories/0/items/9/extracted/overview` | overview | string | HIFU(고강도 집속 초음파) 리프팅 기기 |
| `/modality/8/subcategories/0/items/9/extracted/mechanism` | mechanism | string | 고강도 집속 초음파(HIFU)를 피부 특정 깊이(진피 1.5/3.0mm, SMAS 4.5mm)에 집중시켜 60°C 이상의 열응고점(TIZ)을 형성한다. 음향 캐비테이션과 열 응고로 콜라겐 수축 및 신생콜라겐 생성을 유도하여 리프팅 효과를 제공한다. |
| `/modality/8/subcategories/0/items/9/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/8/subcategories/0/items/9/extracted/indications/primary` | primary | array | [array, 원소 4] |
| `/modality/8/subcategories/0/items/9/extracted/indications/primary/0` | primary[0] | string | 얼굴 및 목의 피부 탄력 감소 |
| `/modality/8/subcategories/0/items/9/extracted/indications/primary/1` | primary[1] | string | 법령선 및 팔자주름 |
| `/modality/8/subcategories/0/items/9/extracted/indications/primary/2` | primary[2] | string | 처진 피부(턱선, 볼 처짐) |
| `/modality/8/subcategories/0/items/9/extracted/indications/primary/3` | primary[3] | string | 전체적인 피부 리프팅 및 타이트닝 |
| `/modality/8/subcategories/0/items/9/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/8/subcategories/0/items/9/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/8/subcategories/0/items/9/extracted/safety/common/0` | common[0] | string | 시술 후 홍반 |
| `/modality/8/subcategories/0/items/9/extracted/safety/common/1` | common[1] | string | 경미한 부종 |
| `/modality/8/subcategories/0/items/9/extracted/safety/common/2` | common[2] | string | 일시적 건조감 |
| `/modality/8/subcategories/0/items/9/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/8/subcategories/0/items/9/extracted/safety/serious/0` | serious[0] | string | 화상 |
| `/modality/8/subcategories/0/items/9/extracted/safety/serious/1` | serious[1] | string | 신경 손상(드물게) |
| `/modality/8/subcategories/0/items/9/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/8/subcategories/0/items/9/extracted/onset_duration/onset` | onset | string | 2-4주 후 콜라겐 신생으로 점진적 개선 |
| `/modality/8/subcategories/0/items/9/extracted/onset_duration/duration` | duration | string | 3-6개월 지속, 시술 반복으로 효과 연장 |
| `/modality/8/subcategories/0/items/9/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/8/subcategories/0/items/9/extracted/aftercare/0` | aftercare[0] | string | 24시간 자극적 제품(비타민C, 산성 성분) 피하기 |
| `/modality/8/subcategories/0/items/9/extracted/aftercare/1` | aftercare[1] | string | 시술 후 3-7일 과도한 열 노출 제한 |
| `/modality/8/subcategories/0/items/9/extracted/aftercare/2` | aftercare[2] | string | 과도한 운동 및 사우나 1주일 피하기 |
| `/modality/8/subcategories/0/items/9/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 저출력 EBD — 최소 1개월 이상 간격, 보통 3개월 간격 권장. 과도한 열 누적 주의. 효과 평가 후 재시술 판단 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/8/subcategories/0/items/10` | items[10] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/8/subcategories/0/items/10/id` | id | string | auto-M9-1775361909628 |
| `/modality/8/subcategories/0/items/10/name` | name | string | 울트라포머MPT |
| `/modality/8/subcategories/0/items/10/detail` | detail | string | 클래시스 · MMFU 기술 · 미세점 HIFU |
| `/modality/8/subcategories/0/items/10/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/8/subcategories/0/items/10/extracted/overview` | overview | string | 미세점 HIFU 기술을 이용한 비침습적 리프팅 및 타이트닝 장비 |
| `/modality/8/subcategories/0/items/10/extracted/mechanism` | mechanism | string | MMFU(Micro and Macro Focused Ultrasound) 기술로 피부 진피층과 SMAS층에 집속초음파를 전달하여 열응고점을 생성합니다. 콜라겐 변성과 신생을 통해 피부 타이트닝과 리프팅 효과를 유도합니다. |
| `/modality/8/subcategories/0/items/10/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/8/subcategories/0/items/10/extracted/indications/primary` | primary | array | [array, 원소 2] |
| `/modality/8/subcategories/0/items/10/extracted/indications/primary/0` | primary[0] | string | 안면 및 목 주름 개선 |
| `/modality/8/subcategories/0/items/10/extracted/indications/primary/1` | primary[1] | string | 피부 탄력 증진 및 리프팅 |
| `/modality/8/subcategories/0/items/10/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/8/subcategories/0/items/10/extracted/safety/common` | common | array | [array, 원소 1] |
| `/modality/8/subcategories/0/items/10/extracted/safety/common/0` | common[0] | string | 시술 부위 일시적 홍반 및 부종 |
| `/modality/8/subcategories/0/items/10/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/8/subcategories/0/items/10/extracted/onset_duration/onset` | onset | string | 2-3개월 |
| `/modality/8/subcategories/0/items/10/extracted/onset_duration/duration` | duration | string | 12-18개월 |
| `/modality/8/subcategories/0/items/10/extracted/aftercare` | aftercare | array | [array, 원소 5] |
| `/modality/8/subcategories/0/items/10/extracted/aftercare/0` | aftercare[0] | string | 시술 후 2-3일간 과도한 열 노출 및 사우나 자제 |
| `/modality/8/subcategories/0/items/10/extracted/aftercare/1` | aftercare[1] | string | 홍반/부종은 수시간~수일 내 자연 소실 |
| `/modality/8/subcategories/0/items/10/extracted/aftercare/2` | aftercare[2] | string | 냉찜질로 통증/부종 완화 가능 |
| `/modality/8/subcategories/0/items/10/extracted/aftercare/3` | aftercare[3] | string | 당일 보습 관리 권장 |
| `/modality/8/subcategories/0/items/10/extracted/aftercare/4` | aftercare[4] | string | [시술 주기 참고] 중출력 EBD — 3-6개월 간격 권장. 콜라겐 리모델링 진행 상황 평가 후 재시술 판단. 아무리 빨라도 1개월 이상 간격 필수 (개인차 있으며, 의사와 상의하여 결정) |
| `/modality/8/subcategories/0/items/11` | items[11] | object | {object, 키 4: id, name, detail, extracted} |
| `/modality/8/subcategories/0/items/11/id` | id | string | auto-M9-1775362627041 |
| `/modality/8/subcategories/0/items/11/name` | name | string | 울트라셀Q+ |
| `/modality/8/subcategories/0/items/11/detail` | detail | string | 제이시스 · HIFU+DOT |
| `/modality/8/subcategories/0/items/11/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/8/subcategories/0/items/11/extracted/overview` | overview | string | 고강도 집속 초음파(HIFU)와 도트 기술을 결합한 비수술적 리프팅 및 피부재생 장비 |
| `/modality/8/subcategories/0/items/11/extracted/mechanism` | mechanism | string | 고강도 집속 초음파를 진피 깊숙이 전달하여 65-75℃의 열 응고점을 형성해 콜라겐 수축과 신생을 유도합니다. 도트 기술을 통해 미세한 열손상을 균등하게 분포시켜 피부 전체의 타이트닝과 재생을 촉진합니다. |
| `/modality/8/subcategories/0/items/11/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/8/subcategories/0/items/11/extracted/indications/primary` | primary | array | [array, 원소 2] |
| `/modality/8/subcategories/0/items/11/extracted/indications/primary/0` | primary[0] | string | 안면 및 목 부위 리프팅 |
| `/modality/8/subcategories/0/items/11/extracted/indications/primary/1` | primary[1] | string | 피부 타이트닝 및 주름 개선 |
| `/modality/8/subcategories/0/items/11/extracted/safety` | safety | object | {object, 키 1: common} |
| `/modality/8/subcategories/0/items/11/extracted/safety/common` | common | array | [array, 원소 1] |
| `/modality/8/subcategories/0/items/11/extracted/safety/common/0` | common[0] | string | 시술 부위 일시적 부종 및 홍조 |
| `/modality/8/subcategories/0/items/11/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/8/subcategories/0/items/11/extracted/onset_duration/onset` | onset | string | 2-3개월 |
| `/modality/8/subcategories/0/items/11/extracted/onset_duration/duration` | duration | string | 12-18개월 |
| `/modality/8/subcategories/0/items/11/extracted/aftercare` | aftercare | array | [array, 원소 4] |
| `/modality/8/subcategories/0/items/11/extracted/aftercare/0` | aftercare[0] | string | 홍반/부종은 수시간~수일 내 자연 소실 |
| `/modality/8/subcategories/0/items/11/extracted/aftercare/1` | aftercare[1] | string | 냉찜질로 통증/부종 완화 가능 |
| `/modality/8/subcategories/0/items/11/extracted/aftercare/2` | aftercare[2] | string | 당일 보습 관리 권장 |
| `/modality/8/subcategories/0/items/11/extracted/aftercare/3` | aftercare[3] | string | [시술 주기 참고] 중출력 EBD — 3-6개월 간격 권장. 콜라겐 리모델링 진행 상황 평가 후 재시술 판단. 아무리 빨라도 1개월 이상 간격 필수 (개인차 있으며, 의사와 상의하여 결정) |

## 잠정 관찰 (원문 아님 · 직접 읽기 기록)

| 상태 | 근거 Pointer | 관찰 |
|---|---|---|
| P | `/modality/8/subcategories/0/label`, `/modality/8/category_en` | M9 category '기기 리프팅'(category_en 'Energy Based Device Lifting'). 하위분류 label 'HIFU (초음파)' — 에너지원 축. |
| P | `/modality/8/subcategories/0/items/0/extracted/aftercare/3`, `/modality/8/subcategories/0/items/2/extracted/aftercare/3`, `/modality/8/subcategories/0/items/9/extracted/aftercare/3` | M9 상용구가 출력 등급별 3종이다: 고출력 EBD('최소 6개월 이상 간격 … 아무리 빨라도 1개월 이상 간격 필수'), 중출력 EBD('3-6개월 간격 권장'), 저출력 EBD('최소 1개월 이상 간격, 보통 3개월 간격'). 항목마다 어느 등급인지는 상용구로만 드러난다(울쎄라·울쎄라피프라임·슈링크유니버스=고출력, 슈링크·더블로·더블로골드·리프테라·리니어펌·텐쎄라·울트라포머MPT·울트라셀Q+=중출력, 쿨소닉=저출력). 등급 판정 근거는 원문에 없음(B). |
| P | `/modality/8/subcategories/0/items/2/extracted/mechanism`, `/modality/8/subcategories/0/items/6/extracted/mechanism`, `/modality/8/subcategories/0/items/7/extracted/mechanism` | HIFU 항목 다수가 같은 mechanism 문장('고강도 집속 초음파(HIFU)를 피부 특정 깊이(진피 1.5/3.0mm, SMAS 4.5mm)에 집중시켜 60°C 이상의 열응고점(TIZ)…')과 같은 overview('HIFU(고강도 집속 초음파) 리프팅 기기')를 공유한다. 장비별 차이는 indications·onset_duration·aftercare 일부에만. |
| P | `/modality/8/subcategories/0/items/0/extracted/mechanism` | 울쎄라 mechanism '유일하게 US FDA 승인된 HIFU 기기로 실시간 초음파 영상화' — 배타적 규제 주장(승인하지 않음). |
| P | `/modality/8/subcategories/0/items/1/extracted/indications/primary/4`, `/modality/8/subcategories/0/items/2/extracted/indications/primary/2` | 얼굴 외 부위(팔뚝/허벅지, 복부). |
| P | `/modality/8/subcategories/0/items/11/extracted/mechanism`, `/modality/8/subcategories/0/items/0/extracted/mechanism` | 온도 표기 '60°C', '60°C 이상', '65-75℃' — 기호(°C/℃) 혼용. |
| P | `/modality/8/subcategories/0/items/6/id`, `/modality/8/subcategories/0/items/5/id` | id 가 M9-1-6 다음 M9-1-8 (M9-1-7 없음). |

## 수동 복합 표현 (원문 구간)

| Pointer | 구간 | 원문 표현 | 관점 | 메모 |
|---|---|---|---|---|
| `/modality/8/subcategories/0/items/0/extracted/mechanism` | [41, 67] | 60°C의 고열을 발생시켜 표적 조직을 응고괴사 | 수량·단위·시간 |  |
| `/modality/8/subcategories/0/items/0/extracted/mechanism` | [183, 206] | 유일하게 US FDA 승인된 HIFU 기기 | 주장 |  |
| `/modality/8/subcategories/0/items/0/extracted/aftercare/3` | [11, 36] | 고출력 EBD — 최소 6개월 이상 간격 권장 | 범위, 수량·단위·시간, 조건 | 상용구 고출력판 |
| `/modality/8/subcategories/0/items/0/extracted/aftercare/3` | [71, 99] | 리모델링 중 재시술은 과도한 열 누적/지방위축 위험 | 조건, 가능성·빈도 |  |
| `/modality/8/subcategories/0/items/0/extracted/aftercare/3` | [101, 121] | 아무리 빨라도 1개월 이상 간격 필수 | 범위, 수량·단위·시간 | 양보 표현 + 하한 |
| `/modality/8/subcategories/0/items/1/extracted/mechanism` | [13, 41] | 피부 진피-피하층(3mm)과 SMAS층(4.5mm) | 부위, 수량·단위·시간 | 깊이 |
| `/modality/8/subcategories/0/items/1/extracted/safety/serious/1` | [0, 15] | 피부화상(깊이 조절 오류시) | 조건 |  |
| `/modality/8/subcategories/0/items/1/extracted/onset_duration/onset` | [0, 26] | 즉시 효과 인지 가능, 최적 효과는 8주-3개월 | 수량·단위·시간, 범위 | 단위 다른 양끝 |
| `/modality/8/subcategories/0/items/2/extracted/mechanism` | [27, 51] | 진피 1.5/3.0mm, SMAS 4.5mm | 부위, 수량·단위·시간, 기호 | '/' 두 깊이 |
| `/modality/8/subcategories/0/items/2/extracted/aftercare/3` | [11, 32] | 중출력 EBD — 3-6개월 간격 권장 | 수량·단위·시간, 범위, 조건 | 상용구 중출력판 |
| `/modality/8/subcategories/0/items/3/extracted/mechanism` | [97, 127] | Pre-focal zone에서도 추가 열손상이 발생하여 | 부위 |  |
| `/modality/8/subcategories/0/items/3/extracted/safety/serious/1` | [0, 13] | 화상(부적절한 설정 시) | 조건 |  |
| `/modality/8/subcategories/0/items/4/extracted/onset_duration/duration` | [0, 25] | 3-6개월 지속, 개인차에 따라 최대 12개월 | 조건, 범위 |  |
| `/modality/8/subcategories/0/items/6/extracted/onset_duration/duration` | [0, 23] | 3-6개월 지속, 반복 시 누적 효과 가능 | 조건, 가능성·빈도 |  |
| `/modality/8/subcategories/0/items/9/extracted/aftercare/3` | [11, 47] | 저출력 EBD — 최소 1개월 이상 간격, 보통 3개월 간격 권장 | 범위, 가능성·빈도, 수량·단위·시간 | 상용구 저출력판 |
| `/modality/8/subcategories/0/items/10/extracted/aftercare/1` | [0, 21] | 홍반/부종은 수시간~수일 내 자연 소실 | 수량·단위·시간, 범위 |  |
| `/modality/8/subcategories/0/items/11/extracted/mechanism` | [24, 37] | 65-75℃의 열 응고점 | 수량·단위·시간, 범위 |  |
| `/modality/8/subcategories/0/items/11/detail` | [0, 15] | 제이시스 · HIFU+DOT | 기호 |  |

## 형태소 분석 확인 (알려진 오분절 K)

| 범위 | 표면형 | 문제 | 영향 |
|---|---|---|---|
| all | 울쎄라 | 단독 '울쎄라' 를 울쎄/NNG 이/VCP 라/EC 로(텐쎄라도 같은 패턴) | 장비명 끝 '라' 를 서술격+어미로 — 장비명 소실 |
| all | 텐쎄라 | 텐쎄/NNG 이/VCP 라/EC | 장비명 소실 |
| all | 더블로 | 단독 '더블로' 를 더블/NNG 로/JKB | 장비명 절단 |
| all | 리니어펌 | 리니어/NNG 퍼/NNG ᆷ/EF | 장비명 소실 |

## 미결

| ID | 상태 | Pointer | 내용 | 영향·후속 |
|---|---|---|---|---|
| S027-B01 | B | `/modality/8/subcategories/0/items/0/extracted/aftercare/3`, `/modality/8/subcategories/0/items/2/extracted/aftercare/3`, `/modality/8/subcategories/0/items/9/extracted/aftercare/3` | 장비의 고/중/저출력 등급이 상용구로만 표시되고 판정 기준이 원문에 없다. | 출력 등급을 속성으로 쓸 때 근거 부족 |
| S027-F01 | F | `/modality/8/subcategories/0/items/2/extracted/mechanism`, `/modality/8/subcategories/0/items/6/extracted/mechanism` | 다수 항목이 같은 mechanism·overview 문장을 공유(템플릿 채움 흔적으로 보임). | 항목별 차이 판단 시 상용구 구분 필요 |

