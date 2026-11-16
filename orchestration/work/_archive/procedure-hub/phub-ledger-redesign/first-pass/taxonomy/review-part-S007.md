# S007 — M2 필러

- 읽기 상태: **read** · 마지막 읽은 Pointer `/modality/1/name`
- 단위: extracted, products 컨테이너, M2-P-0, M2-P-1, M2-P-2, M2-P-3, M2-P-4, M2-P-5, M2-P-6, M2-P-7, name
- 상위 문맥(공동 참조·소유 아님): `/modality/1` M2 / 필러 / 필러
- 기계 기록: `source-map.json`(section=S007) · `morphology/S007.json` · `expressions.json`(section=S007) · 읽기 렌더 `reading/S007.txt`

## 원문 값 (원본 컬럼명 그대로, 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/modality/1/extracted` | extracted | object | {object, 키 8: overview, mechanism, indications, contraindications, safety, onset_duration, aftercare, related_techniques} |
| `/modality/1/extracted/overview` | overview | string | 필러는 피부 속 부피가 줄어든 부위에 채움 물질을 주입해서 주름을 펴거나 윤곽을 잡아주는 미용 시술이다. 1893년부터 시작된 오랜 역사를 가진 시술로, 히알루론산(HA) 필러가 현재 가장 많이 사용된다. 콜라겐 자극형 필러(칼슘 필러, PLLA 등)도 있어서 목적에 따라 다양한 종류를 선택할 수 있다. |
| `/modality/1/extracted/mechanism` | mechanism | string | 필러는 피부 연조직의 결손부위(꺼진 곳, 주름, 흉터)에 물질을 채워 넣어 즉각적으로 볼륨을 만들어준다. 히알루론산 필러의 경우, 주입된 히알루론산이 주변의 수분을 끌어당겨 부피가 커지면서 피부를 안쪽에서 밀어올린다. 칼슘 기반 필러(래디에스 등)는 주입 직후 볼륨 효과에 더해, 시간이 지나면서 우리 몸의 콜라겐(피부 탄력 단백질) 생성을 촉진해 더 오래 유지된다. |
| `/modality/1/extracted/indications` | indications | object | {object, 키 2: primary, extended} |
| `/modality/1/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/1/extracted/indications/primary/0` | primary[0] | string | 주름치료 — 이마주름, 미간주름, 눈가주름, 팔자주름(코입술주름), 입꼬리주름, 목주름, 잔주름 |
| `/modality/1/extracted/indications/primary/1` | primary[1] | string | 윤곽성형 — 이마 키우기, 관자놀이 키우기, 볼 키우기, 턱 키우기, 코 보형, 입술확대 |
| `/modality/1/extracted/indications/primary/2` | primary[2] | string | 흉터치료 — 여드름흉터, 수두자국, 위축성 흉터 (살이 꺼진 흉터) |
| `/modality/1/extracted/indications/extended` | extended | array | [array, 원소 7] |
| `/modality/1/extracted/indications/extended/0` | extended[0] | string | 꺼진 눈 교정 |
| `/modality/1/extracted/indications/extended/1` | extended[1] | string | 다크서클 교정 (눈밑 꺼짐) |
| `/modality/1/extracted/indications/extended/2` | extended[2] | string | 애교살 키우기 |
| `/modality/1/extracted/indications/extended/3` | extended[3] | string | 상악골 윤곽성형 (위턱뼈 주변) |
| `/modality/1/extracted/indications/extended/4` | extended[4] | string | 입술라인 및 인중선 확대 |
| `/modality/1/extracted/indications/extended/5` | extended[5] | string | 손등회춘술 (손등 볼륨 채움) |
| `/modality/1/extracted/indications/extended/6` | extended[6] | string | 히알루론산 메조테라피 (물광주사) |
| `/modality/1/extracted/contraindications` | contraindications | object | {object, 키 2: absolute, relative} |
| `/modality/1/extracted/contraindications/absolute` | absolute | array | [array, 원소 4] |
| `/modality/1/extracted/contraindications/absolute/0` | absolute[0] | string | 필러 성분(히알루론산, 콜라겐 등)에 알레르기가 있는 경우 |
| `/modality/1/extracted/contraindications/absolute/1` | absolute[1] | string | 주사 맞을 부위에 염증이나 감염이 진행 중인 경우 |
| `/modality/1/extracted/contraindications/absolute/2` | absolute[2] | string | 소 콜라겐 필러 사용 시 피부반응검사에서 양성 반응이 나온 경우 |
| `/modality/1/extracted/contraindications/absolute/3` | absolute[3] | string | 켈로이드 체질 (흉터가 비정상적으로 부풀어오르는 체질) |
| `/modality/1/extracted/contraindications/relative` | relative | array | [array, 원소 3] |
| `/modality/1/extracted/contraindications/relative/0` | relative[0] | string | 임신 중이거나 수유 중일 때는 미루는 게 좋음 |
| `/modality/1/extracted/contraindications/relative/1` | relative[1] | string | 혈액 응고에 영향을 주는 약물(아스피린 등) 복용 중이면 멍이 잘 들 수 있으니 의사에게 알릴 것 |
| `/modality/1/extracted/contraindications/relative/2` | relative[2] | string | 자가면역질환이 있는 경우 의사와 상의 필요 |
| `/modality/1/extracted/safety` | safety | object | {object, 키 3: common, uncommon, serious} |
| `/modality/1/extracted/safety/common` | common | array | [array, 원소 4] |
| `/modality/1/extracted/safety/common/0` | common[0] | string | 주사 부위 홍반 (빨개짐) |
| `/modality/1/extracted/safety/common/1` | common[1] | string | 멍 |
| `/modality/1/extracted/safety/common/2` | common[2] | string | 부종 (붓기) |
| `/modality/1/extracted/safety/common/3` | common[3] | string | 압통 (누르면 아픈 느낌) |
| `/modality/1/extracted/safety/uncommon` | uncommon | array | [array, 원소 4] |
| `/modality/1/extracted/safety/uncommon/0` | uncommon[0] | string | 필러가 만져지는 느낌 (덩어리감) |
| `/modality/1/extracted/safety/uncommon/1` | uncommon[1] | string | 필러가 원래 위치에서 옆으로 이동하는 현상 |
| `/modality/1/extracted/safety/uncommon/2` | uncommon[2] | string | 색소침착 (시술 부위가 어두워지는 현상) |
| `/modality/1/extracted/safety/uncommon/3` | uncommon[3] | string | 감염 (무균 관리가 안 될 경우) |
| `/modality/1/extracted/safety/serious` | serious | array | [array, 원소 4] |
| `/modality/1/extracted/safety/serious/0` | serious[0] | string | 혈관 막힘 (필러가 혈관에 들어가 피부 괴사를 일으킬 수 있음 — 드물지만 위험) |
| `/modality/1/extracted/safety/serious/1` | serious[1] | string | 시술 부위 피부 괴사 (혈류 차단으로 피부 조직이 죽는 것) |
| `/modality/1/extracted/safety/serious/2` | serious[2] | string | 이물반응 (몸이 필러를 이물질로 인식해 염증을 일으키는 것) |
| `/modality/1/extracted/safety/serious/3` | serious[3] | string | 실명 위험 (코, 이마 등 혈관이 눈동맥과 연결된 부위 시술 시 극히 드물게 발생) |
| `/modality/1/extracted/onset_duration` | onset_duration | object | {object, 키 3: onset, peak, duration} |
| `/modality/1/extracted/onset_duration/onset` | onset | string | 시술 직후 즉각적인 볼륨 효과 |
| `/modality/1/extracted/onset_duration/peak` | peak | string | 붓기가 빠진 후 1~2주 뒤 최종 결과 확인 |
| `/modality/1/extracted/onset_duration/duration` | duration | string | 히알루론산 필러 6~18개월, 칼슘 필러 12~24개월, 자가지방이식 6~12개월 (생착률에 따라 다름) |
| `/modality/1/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/1/extracted/aftercare/0` | aftercare[0] | string | 시술 후 강한 압력으로 시술 부위를 누르거나 마사지하지 않기 |
| `/modality/1/extracted/aftercare/1` | aftercare[1] | string | 시술 당일 과도한 음주, 사우나, 격렬한 운동 피하기 |
| `/modality/1/extracted/aftercare/2` | aftercare[2] | string | 감염 예방을 위해 청결 유지 |
| `/modality/1/extracted/related_techniques` | related_techniques | array | [array, 원소 3] |
| `/modality/1/extracted/related_techniques/0` | related_techniques[0] | string | 히알루론산 메조테라피 (물광주사) — 피부 속 수분·탄력 개선 |
| `/modality/1/extracted/related_techniques/1` | related_techniques[1] | string | 자가지방이식 — 본인 지방으로 볼륨 채움, 알레르기 위험 없음 |
| `/modality/1/extracted/related_techniques/2` | related_techniques[2] | string | 진피절제주입법 (서브시전 + 필러) — 흉터 치료에 병합 활용 |
| `/modality/1/products` | products | array | [array, 원소 8] |
| `/modality/1/products/0` | products[0] | object | {object, 키 7: id, name, name_en, manufacturer, country, mfds, extracted} |
| `/modality/1/products/0/id` | id | string | M2-P-0 |
| `/modality/1/products/0/name` | name | string | 쥬비덤 |
| `/modality/1/products/0/name_en` | name_en | string | Juvéderm |
| `/modality/1/products/0/manufacturer` | manufacturer | string | 앨러간/애브비 |
| `/modality/1/products/0/country` | country | string | US |
| `/modality/1/products/0/mfds` | mfds | boolean | true |
| `/modality/1/products/0/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/1/products/0/extracted/overview` | overview | string | 앨러간(Allergan) Vycross 기술 HA 필러 |
| `/modality/1/products/0/extracted/mechanism` | mechanism | string | Vycross 기술(고분자량 HA + 저분자량 HA 혼합)로 G' 50-120 Pa 범위 조정 가능. 동적 교차결합으로 주입층별 맞춤 점도 제공. 안동맥 역행성 색전 위험(supratrochlear/supraorbital 분지)에 특히 주의 필요. |
| `/modality/1/products/0/extracted/indications` | indications | object | {object, 키 2: primary, secondary} |
| `/modality/1/products/0/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/1/products/0/extracted/indications/primary/0` | primary[0] | string | 주름 개선 |
| `/modality/1/products/0/extracted/indications/primary/1` | primary[1] | string | 볼륨 복원 |
| `/modality/1/products/0/extracted/indications/primary/2` | primary[2] | string | 입술 형성 |
| `/modality/1/products/0/extracted/indications/secondary` | secondary | array | [array, 원소 2] |
| `/modality/1/products/0/extracted/indications/secondary/0` | secondary[0] | string | 혼합층 주입 |
| `/modality/1/products/0/extracted/indications/secondary/1` | secondary[1] | string | 얕은/깊은 모든 층 |
| `/modality/1/products/0/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/1/products/0/extracted/safety/common` | common | array | [array, 원소 2] |
| `/modality/1/products/0/extracted/safety/common/0` | common[0] | string | 일시적 부종·멍 |
| `/modality/1/products/0/extracted/safety/common/1` | common[1] | string | 주입부위 발적 |
| `/modality/1/products/0/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/1/products/0/extracted/safety/serious/0` | serious[0] | string | 실명(미간 38.8%, 코 25.5%) |
| `/modality/1/products/0/extracted/safety/serious/1` | serious[1] | string | 혈관폐색 육아종 |
| `/modality/1/products/0/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/1/products/0/extracted/onset_duration/onset` | onset | string | 주입 직후~2주 |
| `/modality/1/products/0/extracted/onset_duration/duration` | duration | string | 9~12개월 |
| `/modality/1/products/0/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/1/products/0/extracted/aftercare/0` | aftercare[0] | string | 미간/코 주입 후 안구 증상 모니터링 |
| `/modality/1/products/0/extracted/aftercare/1` | aftercare[1] | string | 역행성 색전 증상(시야흐림·안통) 응급처치 준비 |
| `/modality/1/products/0/extracted/aftercare/2` | aftercare[2] | string | 72시간 음주 금지 |
| `/modality/1/products/1` | products[1] | object | {object, 키 7: id, name, name_en, manufacturer, country, mfds, extracted} |
| `/modality/1/products/1/id` | id | string | M2-P-1 |
| `/modality/1/products/1/name` | name | string | 레스틸렌 |
| `/modality/1/products/1/name_en` | name_en | string | Restylane |
| `/modality/1/products/1/manufacturer` | manufacturer | string | 갈더마 |
| `/modality/1/products/1/country` | country | string | SE |
| `/modality/1/products/1/mfds` | mfds | boolean | true |
| `/modality/1/products/1/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/1/products/1/extracted/overview` | overview | string | 갈더마 NASHA HA 필러 |
| `/modality/1/products/1/extracted/mechanism` | mechanism | string | NASHA(Non-Animal Stabilized HA) 기술로 동물 유래 성분 제거. G' 범위 60-150 Pa로 정교한 레올로지 조절. 최소 MoD(1-8%)에서 최대 겔 강도로 오래된 표준 필러. 안면동맥 분지 분포(미간·코) 고려 필수. |
| `/modality/1/products/1/extracted/indications` | indications | object | {object, 키 2: primary, secondary} |
| `/modality/1/products/1/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/1/products/1/extracted/indications/primary/0` | primary[0] | string | 중등도 주름 |
| `/modality/1/products/1/extracted/indications/primary/1` | primary[1] | string | 이마 |
| `/modality/1/products/1/extracted/indications/primary/2` | primary[2] | string | 광대뼈 |
| `/modality/1/products/1/extracted/indications/secondary` | secondary | array | [array, 원소 2] |
| `/modality/1/products/1/extracted/indications/secondary/0` | secondary[0] | string | 비순홈 |
| `/modality/1/products/1/extracted/indications/secondary/1` | secondary[1] | string | 턱선 보강 |
| `/modality/1/products/1/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/1/products/1/extracted/safety/common` | common | array | [array, 원소 3] |
| `/modality/1/products/1/extracted/safety/common/0` | common[0] | string | 부종(3~5일) |
| `/modality/1/products/1/extracted/safety/common/1` | common[1] | string | 멍 |
| `/modality/1/products/1/extracted/safety/common/2` | common[2] | string | 일시적 경결 |
| `/modality/1/products/1/extracted/safety/serious` | serious | array | [array, 원소 2] |
| `/modality/1/products/1/extracted/safety/serious/0` | serious[0] | string | 동맥 폐색(0.04mL) |
| `/modality/1/products/1/extracted/safety/serious/1` | serious[1] | string | 시력상실 위험 |
| `/modality/1/products/1/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/1/products/1/extracted/onset_duration/onset` | onset | string | 2~4주 |
| `/modality/1/products/1/extracted/onset_duration/duration` | duration | string | 12~18개월 |
| `/modality/1/products/1/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/1/products/1/extracted/aftercare/0` | aftercare[0] | string | 미간·코 주입 시 supratrochlear/supraorbital 분지 회피 |
| `/modality/1/products/1/extracted/aftercare/1` | aftercare[1] | string | 저용량 다중 주입 권장 |
| `/modality/1/products/1/extracted/aftercare/2` | aftercare[2] | string | 안압 모니터링 |
| `/modality/1/products/2` | products[2] | object | {object, 키 7: id, name, name_en, manufacturer, country, mfds, extracted} |
| `/modality/1/products/2/id` | id | string | M2-P-2 |
| `/modality/1/products/2/name` | name | string | 벨로테로 |
| `/modality/1/products/2/name_en` | name_en | string | Belotero |
| `/modality/1/products/2/manufacturer` | manufacturer | string | 멀츠 |
| `/modality/1/products/2/country` | country | string | DE |
| `/modality/1/products/2/mfds` | mfds | boolean | true |
| `/modality/1/products/2/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/1/products/2/extracted/overview` | overview | string | 멀츠(Merz, 독일) CPM 기술 HA 필러 |
| `/modality/1/products/2/extracted/mechanism` | mechanism | string | CPM(Cohesive Polydensified Matrix) 기술의 동적 교차결합으로 균일한 겔 밀도를 유지하면서 자연스러운 조직 통합. 얕은 층 주입에 최적화. |
| `/modality/1/products/2/extracted/indications` | indications | object | {object, 키 2: primary, secondary} |
| `/modality/1/products/2/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/1/products/2/extracted/indications/primary/0` | primary[0] | string | 주름 개선 |
| `/modality/1/products/2/extracted/indications/primary/1` | primary[1] | string | 입술 |
| `/modality/1/products/2/extracted/indications/primary/2` | primary[2] | string | 안면 윤곽 |
| `/modality/1/products/2/extracted/indications/secondary` | secondary | array | [array, 원소 2] |
| `/modality/1/products/2/extracted/indications/secondary/0` | secondary[0] | string | 콧등 보강 |
| `/modality/1/products/2/extracted/indications/secondary/1` | secondary[1] | string | 비순홈 |
| `/modality/1/products/2/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/1/products/2/extracted/safety/common` | common | array | [array, 원소 2] |
| `/modality/1/products/2/extracted/safety/common/0` | common[0] | string | 일시적 부종 |
| `/modality/1/products/2/extracted/safety/common/1` | common[1] | string | 주입부위 발적 |
| `/modality/1/products/2/extracted/safety/serious` | serious | array | [array, 원소 1] |
| `/modality/1/products/2/extracted/safety/serious/0` | serious[0] | string | 역행성 색전 |
| `/modality/1/products/2/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/1/products/2/extracted/onset_duration/onset` | onset | string | 주입 직후~2주 |
| `/modality/1/products/2/extracted/onset_duration/duration` | duration | string | 12~15개월 |
| `/modality/1/products/2/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/1/products/2/extracted/aftercare/0` | aftercare[0] | string | 고강도 운동 72시간 회피 |
| `/modality/1/products/2/extracted/aftercare/1` | aftercare[1] | string | 주입부위 마사지 금지 |
| `/modality/1/products/2/extracted/aftercare/2` | aftercare[2] | string | 극단적 온도 환경 제한(1주) |
| `/modality/1/products/3` | products[3] | object | {object, 키 7: id, name, name_en, manufacturer, country, mfds, extracted} |
| `/modality/1/products/3/id` | id | string | M2-P-3 |
| `/modality/1/products/3/name` | name | string | 이브아르 |
| `/modality/1/products/3/name_en` | name_en | string | Yvoire |
| `/modality/1/products/3/manufacturer` | manufacturer | string | LG화학 |
| `/modality/1/products/3/country` | country | string | KR |
| `/modality/1/products/3/mfds` | mfds | boolean | true |
| `/modality/1/products/3/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/1/products/3/extracted/overview` | overview | string | LG화학(LG Chem) 국산 HA 필러 |
| `/modality/1/products/3/extracted/mechanism` | mechanism | string | 동적 교차결합으로 G' 70-130 Pa의 유연한 레올로지. 얕은 진피층부터 깊은 치골궁까지 다층 주입 설계. 한국인 피부 특성 고려 개발로 섬세한 주름 개선. |
| `/modality/1/products/3/extracted/indications` | indications | object | {object, 키 2: primary, secondary} |
| `/modality/1/products/3/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/1/products/3/extracted/indications/primary/0` | primary[0] | string | 미세 주름 |
| `/modality/1/products/3/extracted/indications/primary/1` | primary[1] | string | 입술 볼륨 |
| `/modality/1/products/3/extracted/indications/primary/2` | primary[2] | string | 혼합층 주입 |
| `/modality/1/products/3/extracted/indications/secondary` | secondary | array | [array, 원소 2] |
| `/modality/1/products/3/extracted/indications/secondary/0` | secondary[0] | string | 이마 |
| `/modality/1/products/3/extracted/indications/secondary/1` | secondary[1] | string | 관자놀이 |
| `/modality/1/products/3/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/1/products/3/extracted/safety/common` | common | array | [array, 원소 2] |
| `/modality/1/products/3/extracted/safety/common/0` | common[0] | string | 경미한 부종 |
| `/modality/1/products/3/extracted/safety/common/1` | common[1] | string | 일시적 멍 |
| `/modality/1/products/3/extracted/safety/serious` | serious | array | [array, 원소 1] |
| `/modality/1/products/3/extracted/safety/serious/0` | serious[0] | string | 혈관폐색(드물음) |
| `/modality/1/products/3/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/1/products/3/extracted/onset_duration/onset` | onset | string | 1~2주 |
| `/modality/1/products/3/extracted/onset_duration/duration` | duration | string | 10~14개월 |
| `/modality/1/products/3/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/1/products/3/extracted/aftercare/0` | aftercare[0] | string | 주입 후 냉찜질(15분) |
| `/modality/1/products/3/extracted/aftercare/1` | aftercare[1] | string | 마사지 회피(48시간) |
| `/modality/1/products/3/extracted/aftercare/2` | aftercare[2] | string | 자외선 차단(2주) |
| `/modality/1/products/4` | products[4] | object | {object, 키 7: id, name, name_en, manufacturer, country, mfds, extracted} |
| `/modality/1/products/4/id` | id | string | M2-P-4 |
| `/modality/1/products/4/name` | name | string | 엘라비에 |
| `/modality/1/products/4/name_en` | name_en | string | Elravie |
| `/modality/1/products/4/manufacturer` | manufacturer | string | 휴메딕스 |
| `/modality/1/products/4/country` | country | string | KR |
| `/modality/1/products/4/mfds` | mfds | boolean | true |
| `/modality/1/products/4/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/1/products/4/extracted/overview` | overview | string | 휴메딕스(Humedix) 국산 HA 필러 |
| `/modality/1/products/4/extracted/mechanism` | mechanism | string | 낮은 교차결합도로 G' 40-70 Pa의 유동성 우수. 얕은 진피 주입에 최적화되어 자연스러운 라인 형성. 점도 낮아 미세 주름 충전에 적합. |
| `/modality/1/products/4/extracted/indications` | indications | object | {object, 키 2: primary, secondary} |
| `/modality/1/products/4/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/1/products/4/extracted/indications/primary/0` | primary[0] | string | 얕은 주름 |
| `/modality/1/products/4/extracted/indications/primary/1` | primary[1] | string | 피부 탄력 개선 |
| `/modality/1/products/4/extracted/indications/primary/2` | primary[2] | string | 광대뼈 윤곽 |
| `/modality/1/products/4/extracted/indications/secondary` | secondary | array | [array, 원소 2] |
| `/modality/1/products/4/extracted/indications/secondary/0` | secondary[0] | string | 이마 라인 |
| `/modality/1/products/4/extracted/indications/secondary/1` | secondary[1] | string | 눈가 주름 |
| `/modality/1/products/4/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/1/products/4/extracted/safety/common` | common | array | [array, 원소 2] |
| `/modality/1/products/4/extracted/safety/common/0` | common[0] | string | 최소 부종 |
| `/modality/1/products/4/extracted/safety/common/1` | common[1] | string | 일시적 발적 |
| `/modality/1/products/4/extracted/safety/serious` | serious | array | [array, 원소 1] |
| `/modality/1/products/4/extracted/safety/serious/0` | serious[0] | string | 드문 혈관 합병증 |
| `/modality/1/products/4/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/1/products/4/extracted/onset_duration/onset` | onset | string | 주입 직후~1주 |
| `/modality/1/products/4/extracted/onset_duration/duration` | duration | string | 8~12개월 |
| `/modality/1/products/4/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/1/products/4/extracted/aftercare/0` | aftercare[0] | string | 마사지 회피(72시간) |
| `/modality/1/products/4/extracted/aftercare/1` | aftercare[1] | string | 운동 제한(3일) |
| `/modality/1/products/4/extracted/aftercare/2` | aftercare[2] | string | 냉찜질 권장 |
| `/modality/1/products/5` | products[5] | object | {object, 키 7: id, name, name_en, manufacturer, country, mfds, extracted} |
| `/modality/1/products/5/id` | id | string | M2-P-5 |
| `/modality/1/products/5/name` | name | string | 채움 |
| `/modality/1/products/5/name_en` | name_en | string | Chaeum |
| `/modality/1/products/5/manufacturer` | manufacturer | string | 휴젤 |
| `/modality/1/products/5/country` | country | string | KR |
| `/modality/1/products/5/mfds` | mfds | boolean | true |
| `/modality/1/products/5/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/1/products/5/extracted/overview` | overview | string | 휴젤 고강도 HA 필러 |
| `/modality/1/products/5/extracted/mechanism` | mechanism | string | 강화된 교차결합으로 G' 150-200 Pa의 높은 탄성계수. 응집력 >0.5 N으로 리프팅 효과. 깊은 조직층 주입으로 구조적 볼륨 복원. |
| `/modality/1/products/5/extracted/indications` | indications | object | {object, 키 2: primary, secondary} |
| `/modality/1/products/5/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/1/products/5/extracted/indications/primary/0` | primary[0] | string | 깊은 주름 |
| `/modality/1/products/5/extracted/indications/primary/1` | primary[1] | string | 볼륨 손실 |
| `/modality/1/products/5/extracted/indications/primary/2` | primary[2] | string | 턱선 강화 |
| `/modality/1/products/5/extracted/indications/secondary` | secondary | array | [array, 원소 2] |
| `/modality/1/products/5/extracted/indications/secondary/0` | secondary[0] | string | 광대뼈 리프팅 |
| `/modality/1/products/5/extracted/indications/secondary/1` | secondary[1] | string | 안면 골격 정의 |
| `/modality/1/products/5/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/1/products/5/extracted/safety/common` | common | array | [array, 원소 2] |
| `/modality/1/products/5/extracted/safety/common/0` | common[0] | string | 부종(5~7일) |
| `/modality/1/products/5/extracted/safety/common/1` | common[1] | string | 제한된 가동범위 |
| `/modality/1/products/5/extracted/safety/serious` | serious | array | [array, 원소 1] |
| `/modality/1/products/5/extracted/safety/serious/0` | serious[0] | string | 혈관폐색(주의 필요) |
| `/modality/1/products/5/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/1/products/5/extracted/onset_duration/onset` | onset | string | 2~4주 |
| `/modality/1/products/5/extracted/onset_duration/duration` | duration | string | 15~18개월 |
| `/modality/1/products/5/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/1/products/5/extracted/aftercare/0` | aftercare[0] | string | 깊은 마사지 금지(1개월) |
| `/modality/1/products/5/extracted/aftercare/1` | aftercare[1] | string | 고강도 운동 회피(1주) |
| `/modality/1/products/5/extracted/aftercare/2` | aftercare[2] | string | 냉찜질 초기 단계 |
| `/modality/1/products/6` | products[6] | object | {object, 키 7: id, name, name_en, manufacturer, country, mfds, extracted} |
| `/modality/1/products/6/id` | id | string | M2-P-6 |
| `/modality/1/products/6/name` | name | string | 더채움 |
| `/modality/1/products/6/name_en` | name_en | string | The Chaeum |
| `/modality/1/products/6/manufacturer` | manufacturer | string | 휴젤 |
| `/modality/1/products/6/country` | country | string | KR |
| `/modality/1/products/6/mfds` | mfds | boolean | true |
| `/modality/1/products/6/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/1/products/6/extracted/overview` | overview | string | 휴젤(Hugel) 프리미엄 HA 필러 |
| `/modality/1/products/6/extracted/mechanism` | mechanism | string | 고순도 HA(><99.5%)로 입자 오염 최소화. G' 90-150 Pa의 균형잡힌 탄성. 정교한 분자 배치로 응집력·점도 최적화. 안동맥 분지(angular artery: 내안각 medial 9mm, 깊이 2.3mm) 고려 설계. |
| `/modality/1/products/6/extracted/indications` | indications | object | {object, 키 2: primary, secondary} |
| `/modality/1/products/6/extracted/indications/primary` | primary | array | [array, 원소 3] |
| `/modality/1/products/6/extracted/indications/primary/0` | primary[0] | string | 중등도~깊은 주름 |
| `/modality/1/products/6/extracted/indications/primary/1` | primary[1] | string | 입술 형성 |
| `/modality/1/products/6/extracted/indications/primary/2` | primary[2] | string | 혼합층 |
| `/modality/1/products/6/extracted/indications/secondary` | secondary | array | [array, 원소 2] |
| `/modality/1/products/6/extracted/indications/secondary/0` | secondary[0] | string | 비순홈 |
| `/modality/1/products/6/extracted/indications/secondary/1` | secondary[1] | string | 턱선 보강 |
| `/modality/1/products/6/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/1/products/6/extracted/safety/common` | common | array | [array, 원소 2] |
| `/modality/1/products/6/extracted/safety/common/0` | common[0] | string | 부종 |
| `/modality/1/products/6/extracted/safety/common/1` | common[1] | string | 일시적 결절 |
| `/modality/1/products/6/extracted/safety/serious` | serious | array | [array, 원소 1] |
| `/modality/1/products/6/extracted/safety/serious/0` | serious[0] | string | 역행성 색전(각동맥 분지 위험) |
| `/modality/1/products/6/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/1/products/6/extracted/onset_duration/onset` | onset | string | 2~3주 |
| `/modality/1/products/6/extracted/onset_duration/duration` | duration | string | 12~16개월 |
| `/modality/1/products/6/extracted/aftercare` | aftercare | array | [array, 원소 3] |
| `/modality/1/products/6/extracted/aftercare/0` | aftercare[0] | string | 내안각 주입 시 각동맥 분지 확인(9mm medial) |
| `/modality/1/products/6/extracted/aftercare/1` | aftercare[1] | string | 안와상부 얕은 주입 금지 |
| `/modality/1/products/6/extracted/aftercare/2` | aftercare[2] | string | 혈관폐색 증상 교육 |
| `/modality/1/products/7` | products[7] | object | {object, 키 7: id, name, name_en, manufacturer, country, mfds, extracted} |
| `/modality/1/products/7/id` | id | string | M2-P-7 |
| `/modality/1/products/7/name` | name | string | 신펄 |
| `/modality/1/products/7/name_en` | name_en | string | Synpurl |
| `/modality/1/products/7/manufacturer` | manufacturer | string | 제테마 |
| `/modality/1/products/7/country` | country | string | KR |
| `/modality/1/products/7/mfds` | mfds | boolean | true |
| `/modality/1/products/7/extracted` | extracted | object | {object, 키 6: overview, mechanism, indications, safety, onset_duration, aftercare} |
| `/modality/1/products/7/extracted/overview` | overview | string | 제테마의 PLLA(폴리락틱산) 콜라겐 자극형 필러 |
| `/modality/1/products/7/extracted/mechanism` | mechanism | string | PLLA 미립자가 진피층에 주입되어 생체적합성 물질로서 작용하며, 시간이 지나면서 대식세포가 인식해 염증 반응을 유발함으로써 피부 자체의 콜라겐 생성을 활성화시키고 부피를 점진적으로 증가시킨다. |
| `/modality/1/products/7/extracted/indications` | indications | object | {object, 키 1: primary} |
| `/modality/1/products/7/extracted/indications/primary` | primary | array | [array, 원소 6] |
| `/modality/1/products/7/extracted/indications/primary/0` | primary[0] | string | 광범위한 주름 치료 |
| `/modality/1/products/7/extracted/indications/primary/1` | primary[1] | string | 얼굴 전체 볼륨 손실 개선 |
| `/modality/1/products/7/extracted/indications/primary/2` | primary[2] | string | 피부 탄력도 저하 |
| `/modality/1/products/7/extracted/indications/primary/3` | primary[3] | string | 팔자주름 |
| `/modality/1/products/7/extracted/indications/primary/4` | primary[4] | string | 이마 및 미간주름 |
| `/modality/1/products/7/extracted/indications/primary/5` | primary[5] | string | 얼굴 하반부 처짐 |
| `/modality/1/products/7/extracted/safety` | safety | object | {object, 키 2: common, serious} |
| `/modality/1/products/7/extracted/safety/common` | common | array | [array, 원소 4] |
| `/modality/1/products/7/extracted/safety/common/0` | common[0] | string | 초기 부종 |
| `/modality/1/products/7/extracted/safety/common/1` | common[1] | string | 발적 |
| `/modality/1/products/7/extracted/safety/common/2` | common[2] | string | 압통 |
| `/modality/1/products/7/extracted/safety/common/3` | common[3] | string | 경미한 멍 |
| `/modality/1/products/7/extracted/safety/serious` | serious | array | [array, 원소 3] |
| `/modality/1/products/7/extracted/safety/serious/0` | serious[0] | string | 결절 형성 (드물음) |
| `/modality/1/products/7/extracted/safety/serious/1` | serious[1] | string | 육아종 (매우 드물음) |
| `/modality/1/products/7/extracted/safety/serious/2` | serious[2] | string | 지연성 알레르기 반응 |
| `/modality/1/products/7/extracted/onset_duration` | onset_duration | object | {object, 키 2: onset, duration} |
| `/modality/1/products/7/extracted/onset_duration/onset` | onset | string | 4-6주 (콜라겐 재형성 과정) |
| `/modality/1/products/7/extracted/onset_duration/duration` | duration | string | 24-36개월 (콜라겐 축적으로 장기 지속) |
| `/modality/1/products/7/extracted/aftercare` | aftercare | array | [array, 원소 5] |
| `/modality/1/products/7/extracted/aftercare/0` | aftercare[0] | string | 시술 후 24시간 동안 세안, 메이크업 피하기 |
| `/modality/1/products/7/extracted/aftercare/1` | aftercare[1] | string | 1주일간 마사지 및 강한 자극 금지 |
| `/modality/1/products/7/extracted/aftercare/2` | aftercare[2] | string | 2주일간 사우나, 찜질, 격렬한 운동 제한 |
| `/modality/1/products/7/extracted/aftercare/3` | aftercare[3] | string | 냉찜질로 초기 부종 완화 |
| `/modality/1/products/7/extracted/aftercare/4` | aftercare[4] | string | 최적의 결과 위해 4주 간격으로 2-3회 시술 권장 |
| `/modality/1/name` | name | string | 필러 |

## 잠정 관찰 (원문 아님 · 직접 읽기 기록)

| 상태 | 근거 Pointer | 관찰 |
|---|---|---|
| P | `/modality/1/extracted/indications/primary/0`, `/modality/1/extracted/indications/primary/1`, `/modality/1/extracted/indications/primary/2` | 모달리티 M2 indications/primary 원소는 '범주 — 하위 나열' 형식('주름치료 — 이마주름, …', '윤곽성형 — …', '흉터치료 — …'). 한 원소 안에 상위 범주와 하위 부위·고민 목록이 함께 있다. |
| P | `/modality/1/extracted/overview`, `/modality/1/extracted/mechanism`, `/modality/1/extracted/onset_duration/duration` | M2 모달리티 설명이 HA 외에 칼슘 필러(래디에스)·PLLA·자가지방이식까지 포함한다. 같은 원장에서 PLLA·CaHA 는 M3(바이오스티뮬레이터)에, 자가지방이식은 M6 에 따로 있다(이 구획에서는 참조만 보존). |
| P | `/modality/1/products/7`, `/modality/1/products/7/extracted/overview` | M2 products 의 신펄은 'PLLA(폴리락틱산) 콜라겐 자극형 필러' — 필러 계열 제품 목록에 콜라겐 자극형이 있다. M2 subcategories items 에는 신펄이 없다. |
| P | `/modality/1/products/5/name`, `/modality/1/products/6/name`, `/modality/1/subcategories/0/items/2/name` | 제품 '채움'(Chaeum)·'더채움'(The Chaeum) 이 같은 제조사(휴젤)로 별도 제품. 항목에는 '더채움'·'더채움프리미어'. 이름 포함 관계를 같은 개체로 보지 않는다. |
| I | `/modality/1/products/0/extracted/mechanism`, `/modality/1/subcategories/1/items/0/extracted/mechanism` | 쥬비덤 G' 범위가 제품 50-120 Pa, 항목 200-400 Pa 로 다르다. 레스틸렌도 제품 60-150 Pa, 항목 4-857 Pa. |
| I | `/modality/1/products/3/extracted/mechanism` | 이브아르 제품 mechanism '얕은 진피층부터 깊은 치골궁까지 다층 주입' — 안면 필러 설명에 '치골궁'. 원문 그대로(의미 판단 후속). |
| I | `/modality/1/products/6/extracted/mechanism` | '고순도 HA(><99.5%)' 부등호 두 개가 붙어 방향이 불명. |
| P | `/modality/1/products/0/extracted/aftercare`, `/modality/1/products/1/extracted/aftercare/0` | 제품 aftercare 일부는 환자 지시가 아니라 시술자 지시('supratrochlear/supraorbital 분지 회피', '저용량 다중 주입 권장', '혈관폐색 증상 교육'). aftercare 키가 행위 주체를 구분하지 않는다. |
| P | `/modality/1/products/1/country` | 레스틸렌 country 'SE'. 국가 코드 목록에 SE 추가. |

## 수동 복합 표현 (원문 구간)

| Pointer | 구간 | 원문 표현 | 관점 | 메모 |
|---|---|---|---|---|
| `/modality/1/extracted/overview` | [59, 83] | 1893년부터 시작된 오랜 역사를 가진 시술 | 주장, 수량·단위·시간 |  |
| `/modality/1/extracted/overview` | [115, 140] | 콜라겐 자극형 필러(칼슘 필러, PLLA 등) | 시술·제품명, 참조 |  |
| `/modality/1/extracted/indications/primary/0` | [25, 36] | 팔자주름(코입술주름) | 부위 | 동의 표현 괄호 |
| `/modality/1/extracted/indications/extended/1` | [0, 15] | 다크서클 교정 (눈밑 꺼짐) | 부위 |  |
| `/modality/1/extracted/indications/extended/5` | [0, 16] | 손등회춘술 (손등 볼륨 채움) | 시술·제품명, 부위 |  |
| `/modality/1/extracted/contraindications/absolute/2` | [0, 35] | 소 콜라겐 필러 사용 시 피부반응검사에서 양성 반응이 나온 경우 | 조건 | 조건부 절대금기 |
| `/modality/1/extracted/contraindications/relative/1` | [32, 54] | 멍이 잘 들 수 있으니 의사에게 알릴 것 | 가능성·빈도, 조건 |  |
| `/modality/1/extracted/safety/uncommon/3` | [0, 18] | 감염 (무균 관리가 안 될 경우) | 조건, 부정 |  |
| `/modality/1/extracted/safety/serious/0` | [37, 44] | 드물지만 위험 | 가능성·빈도 |  |
| `/modality/1/extracted/safety/serious/3` | [0, 46] | 실명 위험 (코, 이마 등 혈관이 눈동맥과 연결된 부위 시술 시 극히 드물게 발생) | 가능성·빈도, 조건, 부위 |  |
| `/modality/1/extracted/onset_duration/peak` | [0, 24] | 붓기가 빠진 후 1~2주 뒤 최종 결과 확인 | 조건, 수량·단위·시간, 범위 |  |
| `/modality/1/extracted/onset_duration/duration` | [0, 58] | 히알루론산 필러 6~18개월, 칼슘 필러 12~24개월, 자가지방이식 6~12개월 (생착률에 따라 다름) | 수량·단위·시간, 범위, 조건 | 재료별 기간 세 쌍 |
| `/modality/1/extracted/related_techniques/1` | [0, 34] | 자가지방이식 — 본인 지방으로 볼륨 채움, 알레르기 위험 없음 | 시술·제품명, 부정, 참조 | M6 와의 연결은 후속 |
| `/modality/1/extracted/related_techniques/2` | [0, 34] | 진피절제주입법 (서브시전 + 필러) — 흉터 치료에 병합 활용 | 시술·제품명, 기호, 참조 | '+' 병합 |
| `/modality/1/products/0/extracted/mechanism` | [0, 32] | Vycross 기술(고분자량 HA + 저분자량 HA 혼합) | 시술·제품명, 기호 | '+' 성분 혼합 |
| `/modality/1/products/0/extracted/indications/secondary/1` | [0, 10] | 얕은/깊은 모든 층 | 범위, 기호 |  |
| `/modality/1/products/0/extracted/aftercare/1` | [0, 26] | 역행성 색전 증상(시야흐림·안통) 응급처치 준비 | 조건 |  |
| `/modality/1/products/0/extracted/aftercare/2` | [0, 10] | 72시간 음주 금지 | 수량·단위·시간, 부정 |  |
| `/modality/1/products/1/extracted/mechanism` | [79, 112] | 최소 MoD(1-8%)에서 최대 겔 강도로 오래된 표준 필러 | 수량·단위·시간, 범위, 주장 |  |
| `/modality/1/products/1/extracted/aftercare/1` | [0, 12] | 저용량 다중 주입 권장 | 수식 | 시술자 지시 |
| `/modality/1/products/3/extracted/aftercare/2` | [0, 10] | 자외선 차단(2주) | 수량·단위·시간 |  |
| `/modality/1/products/3/extracted/safety/serious/0` | [0, 9] | 혈관폐색(드물음) | 가능성·빈도 |  |
| `/modality/1/products/4/extracted/safety/serious/0` | [0, 9] | 드문 혈관 합병증 | 가능성·빈도 |  |
| `/modality/1/products/6/extracted/mechanism` | [74, 128] | 안동맥 분지(angular artery: 내안각 medial 9mm, 깊이 2.3mm) 고려 설계 | 부위, 수량·단위·시간 | 항목 셀레스텔라는 9.0mm |
| `/modality/1/products/6/extracted/aftercare/1` | [0, 13] | 안와상부 얕은 주입 금지 | 부위, 부정, 수식 |  |
| `/modality/1/products/7/extracted/mechanism` | [46, 88] | 대식세포가 인식해 염증 반응을 유발함으로써 피부 자체의 콜라겐 생성을 활성화 | 수식 |  |
| `/modality/1/products/7/extracted/safety/serious/1` | [0, 12] | 육아종 (매우 드물음) | 가능성·빈도 |  |
| `/modality/1/products/7/extracted/onset_duration/onset` | [0, 17] | 4-6주 (콜라겐 재형성 과정) | 수량·단위·시간, 범위 |  |
| `/modality/1/products/7/extracted/aftercare/4` | [0, 28] | 최적의 결과 위해 4주 간격으로 2-3회 시술 권장 | 수량·단위·시간, 범위 | 회차·간격 |

## 형태소 분석 확인 (알려진 오분절 K)

| 범위 | 표면형 | 문제 | 영향 |
|---|---|---|---|
| all | 각동맥 | 각/MM 동맥/NNG — 해부명 '각동맥'의 '각'을 관형사로 | 부위명 분해·품사 오탐 |
| all | 드물음 | 문맥에 따라 드물음/NNP 또는 드물/VA 음/ETN | 빈도 수식어가 고유명사로 태깅되는 경우 있음(GLOBAL-K02) |
| all | 애교살 | 애교/NNG 살/NNG | 부위 생활어 분해 |
| all | >< | '><' 를 >/SSC </SSO 괄호류로 태깅 | 부등호 의미 소실 |

## 미결

| ID | 상태 | Pointer | 내용 | 영향·후속 |
|---|---|---|---|---|
| S007-I01 | I | `/modality/1/products/0/extracted/mechanism`, `/modality/1/subcategories/1/items/0/extracted/mechanism`, `/modality/1/products/1/extracted/mechanism`, `/modality/1/subcategories/1/items/1/extracted/mechanism` | 같은 이름 제품/항목 사이 G' 수치 불일치(쥬비덤 50-120 vs 200-400 Pa, 레스틸렌 60-150 vs 4-857 Pa). | 물성 수치 채택 시 후속 확인 |
| S007-B01 | B | `/modality/1/products/6/extracted/mechanism` | '(><99.5%)' 부등호 방향 불명. | 순도 수치 해석 불가 |
| S007-F01 | F | `/modality/1/extracted/overview`, `/modality/1/products/7` | M2 설명·제품에 PLLA·칼슘 필러·자가지방이식이 포함되어 M3·M6 와 범위가 겹친다. | 계열 경계는 후속 비교 과제 |

