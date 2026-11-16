# S10 — `M2` (필러) · extracted.json 1차 조사

> 구획 S10 · 소유 Pointer `/M2` 와 그 아래 64개 노드(말단 49). 문맥 참조: 루트 `""`, `/M2/name`, `/M2/procedure_id`. 직접 읽기 상태: **직접 읽음** (1회차: 항목 객체 전체를 키 순서대로 출력해 위에서 아래로 읽음(읽기 묶음 4 — 2~3개 항목씩 순차); 2회차: 값마다 다시 열어 조건·부정·가능성·범위·시간·부위 역할·참조를 manual-expressions / manual-observations 에 원문 인용으로 기록(build 가 인용 실재 검사); 3회차: 이 구획 값의 형태소 토큰 중 의심 품사·전문어 출현을 원문 어절과 대조(segmentation-review.json)).
> 「원문 값」 칸은 원장 문자열 그대로다(`|` 없음). 잠정 관찰은 아래 별도 절에 있고 원문 칸에 섞지 않았다. [목차로](./review.md#구획-목차)

## 1. 모든 값 (원본 순서)

| # | 원본 컬럼명 | JSON Pointer | 자료형 | 원문 값 | 형태소 분석 |
|---|---|---|---|---|---|
| 1 | `(항목 M2)` | `/M2` | object | (object · 15) | —(컨테이너) |
| 2 | `name` | `/M2/name` | string | 필러 | 분석 |
| 3 | `safety` | `/M2/safety` | object | (object · 4) | —(컨테이너) |
| 4 | `safety.common` | `/M2/safety/common` | array | (array · 4) | —(컨테이너) |
| 5 | `safety.common[0]` | `/M2/safety/common/0` | string | 주사 부위 홍반 (빨개짐) | 분석 |
| 6 | `safety.common[1]` | `/M2/safety/common/1` | string | 멍 | 분석 |
| 7 | `safety.common[2]` | `/M2/safety/common/2` | string | 부종 (붓기) | 분석 |
| 8 | `safety.common[3]` | `/M2/safety/common/3` | string | 압통 (누르면 아픈 느낌) | 분석 |
| 9 | `safety.serious` | `/M2/safety/serious` | array | (array · 4) | —(컨테이너) |
| 10 | `safety.serious[0]` | `/M2/safety/serious/0` | string | 혈관 막힘 (필러가 혈관에 들어가 피부 괴사를 일으킬 수 있음 — 드물지만 위험) | 분석 |
| 11 | `safety.serious[1]` | `/M2/safety/serious/1` | string | 시술 부위 피부 괴사 (혈류 차단으로 피부 조직이 죽는 것) | 분석 |
| 12 | `safety.serious[2]` | `/M2/safety/serious/2` | string | 이물반응 (몸이 필러를 이물질로 인식해 염증을 일으키는 것) | 분석 |
| 13 | `safety.serious[3]` | `/M2/safety/serious/3` | string | 실명 위험 (코, 이마 등 혈관이 눈동맥과 연결된 부위 시술 시 극히 드물게 발생) | 분석 |
| 14 | `safety.uncommon` | `/M2/safety/uncommon` | array | (array · 4) | —(컨테이너) |
| 15 | `safety.uncommon[0]` | `/M2/safety/uncommon/0` | string | 필러가 만져지는 느낌 (덩어리감) | 분석 |
| 16 | `safety.uncommon[1]` | `/M2/safety/uncommon/1` | string | 필러가 원래 위치에서 옆으로 이동하는 현상 | 분석 |
| 17 | `safety.uncommon[2]` | `/M2/safety/uncommon/2` | string | 색소침착 (시술 부위가 어두워지는 현상) | 분석 |
| 18 | `safety.uncommon[3]` | `/M2/safety/uncommon/3` | string | 감염 (무균 관리가 안 될 경우) | 분석 |
| 19 | `safety.emergency` | `/M2/safety/emergency` | array | (array · 1) | —(컨테이너) |
| 20 | `safety.emergency[0]` | `/M2/safety/emergency/0` | string | 주사 직후 피부가 하얗게 변하면 혈관이 막혔을 가능성 — 즉시 히알루로니다아제(분해효소) 투여 필요 | 분석 |
| 21 | `source` | `/M2/source` | string | 임상적 피부관리 35장 | 분석 |
| 22 | `name_en` | `/M2/name_en` | string | Soft Tissue Augmentation (Filler) | 분석 |
| 23 | `overview` | `/M2/overview` | string | 필러는 피부 속 부피가 줄어든 부위에 채움 물질을 주입해서 주름을 펴거나 윤곽을 잡아주는 미용 시술이다. 1893년부터 시작된 오랜 역사를 가진 시술로, 히알루론산(HA) 필러가 현재 가장 많이 사용된다. 콜라겐 자극형 필러(칼슘 필러, PLLA 등)도 있어서 목적에 따라 다양한 종류를 선택할 수 있다. | 분석 |
| 24 | `aftercare` | `/M2/aftercare` | array | (array · 3) | —(컨테이너) |
| 25 | `aftercare[0]` | `/M2/aftercare/0` | string | 시술 후 강한 압력으로 시술 부위를 누르거나 마사지하지 않기 | 분석 |
| 26 | `aftercare[1]` | `/M2/aftercare/1` | string | 시술 당일 과도한 음주, 사우나, 격렬한 운동 피하기 | 분석 |
| 27 | `aftercare[2]` | `/M2/aftercare/2` | string | 시술 후 화장은 완전히 지우고 무균 상태에서 시술해야 하며, 감염 예방을 위해 청결 유지 | 분석 |
| 28 | `mechanism` | `/M2/mechanism` | string | 필러는 피부 연조직의 결손부위(꺼진 곳, 주름, 흉터)에 물질을 채워 넣어 즉각적으로 볼륨을 만들어준다. 히알루론산 필러의 경우, 주입된 히알루론산이 주변의 수분을 끌어당겨 부피가 커지면서 피부를 안쪽에서 밀어올린다. 칼슘 기반 필러(래디에스 등)는 주입 직후 볼륨 효과에 더해, 시간이 지나면서 우리 몸의 콜라겐(피부 탄력 단백질) 생성을 촉진해 더 오래 유지된다. 자가지방이식은 본인의 지방세포를 옮기는 방식이라 거부반응 없이 자연스러운 결과를 준다. | 분석 |
| 29 | `indications` | `/M2/indications` | object | (object · 2) | —(컨테이너) |
| 30 | `indications.primary` | `/M2/indications/primary` | array | (array · 3) | —(컨테이너) |
| 31 | `indications.primary[0]` | `/M2/indications/primary/0` | string | 주름치료 — 이마주름, 미간주름, 눈가주름, 팔자주름(코입술주름), 입꼬리주름, 목주름, 잔주름 | 분석 |
| 32 | `indications.primary[1]` | `/M2/indications/primary/1` | string | 윤곽성형 — 이마 키우기, 관자놀이 키우기, 볼 키우기, 턱 키우기, 코 보형, 입술확대 | 분석 |
| 33 | `indications.primary[2]` | `/M2/indications/primary/2` | string | 흉터치료 — 여드름흉터, 수두자국, 위축성 흉터 (살이 꺼진 흉터) | 분석 |
| 34 | `indications.extended` | `/M2/indications/extended` | array | (array · 8) | —(컨테이너) |
| 35 | `indications.extended[0]` | `/M2/indications/extended/0` | string | 꺼진 눈 교정 | 분석 |
| 36 | `indications.extended[1]` | `/M2/indications/extended/1` | string | 다크서클 교정 (눈밑 꺼짐) | 분석 |
| 37 | `indications.extended[2]` | `/M2/indications/extended/2` | string | 애교살 키우기 | 분석 |
| 38 | `indications.extended[3]` | `/M2/indications/extended/3` | string | 상악골 윤곽성형 (위턱뼈 주변) | 분석 |
| 39 | `indications.extended[4]` | `/M2/indications/extended/4` | string | 입술라인 및 인중선 확대 | 분석 |
| 40 | `indications.extended[5]` | `/M2/indications/extended/5` | string | 손등회춘술 (손등 볼륨 채움) | 분석 |
| 41 | `indications.extended[6]` | `/M2/indications/extended/6` | string | 가슴확대술 | 분석 |
| 42 | `indications.extended[7]` | `/M2/indications/extended/7` | string | 히알루론산 메조테라피 (물광주사) | 분석 |
| 43 | `source_type` | `/M2/source_type` | string | kr | 제외: 영문 소문자 열거 코드값(kr/general/us) |
| 44 | `extracted_at` | `/M2/extracted_at` | string | 2026-03-28 | 제외: 날짜값(YYYY-MM-DD) |
| 45 | `procedure_id` | `/M2/procedure_id` | string | M2-FILLER | 제외: 코드값(Mxx-영문 대문자 식별자) |
| 46 | `onset_duration` | `/M2/onset_duration` | object | (object · 3) | —(컨테이너) |
| 47 | `onset_duration.peak` | `/M2/onset_duration/peak` | string | 붓기가 빠진 후 1~2주 뒤 최종 결과 확인 | 분석 |
| 48 | `onset_duration.onset` | `/M2/onset_duration/onset` | string | 시술 직후 즉각적인 볼륨 효과 | 분석 |
| 49 | `onset_duration.duration` | `/M2/onset_duration/duration` | string | 히알루론산 필러 6~18개월, 칼슘 필러 12~24개월, 자가지방이식 6~12개월 (생착률에 따라 다름) | 분석 |
| 50 | `contraindications` | `/M2/contraindications` | object | (object · 2) | —(컨테이너) |
| 51 | `contraindications.absolute` | `/M2/contraindications/absolute` | array | (array · 4) | —(컨테이너) |
| 52 | `contraindications.absolute[0]` | `/M2/contraindications/absolute/0` | string | 필러 성분(히알루론산, 콜라겐 등)에 알레르기가 있는 경우 | 분석 |
| 53 | `contraindications.absolute[1]` | `/M2/contraindications/absolute/1` | string | 주사 맞을 부위에 염증이나 감염이 진행 중인 경우 | 분석 |
| 54 | `contraindications.absolute[2]` | `/M2/contraindications/absolute/2` | string | 소 콜라겐 필러 사용 시 피부반응검사에서 양성 반응이 나온 경우 | 분석 |
| 55 | `contraindications.absolute[3]` | `/M2/contraindications/absolute/3` | string | 켈로이드 체질 (흉터가 비정상적으로 부풀어오르는 체질) | 분석 |
| 56 | `contraindications.relative` | `/M2/contraindications/relative` | array | (array · 3) | —(컨테이너) |
| 57 | `contraindications.relative[0]` | `/M2/contraindications/relative/0` | string | 임신 중이거나 수유 중일 때는 미루는 게 좋음 | 분석 |
| 58 | `contraindications.relative[1]` | `/M2/contraindications/relative/1` | string | 혈액 응고에 영향을 주는 약물(아스피린 등) 복용 중이면 멍이 잘 들 수 있으니 의사에게 알릴 것 | 분석 |
| 59 | `contraindications.relative[2]` | `/M2/contraindications/relative/2` | string | 자가면역질환이 있는 경우 의사와 상의 필요 | 분석 |
| 60 | `guardrail_version` | `/M2/guardrail_version` | string | 1.0 | 제외: 버전 문자열(숫자 |
| 61 | `related_techniques` | `/M2/related_techniques` | array | (array · 3) | —(컨테이너) |
| 62 | `related_techniques[0]` | `/M2/related_techniques/0` | string | 히알루론산 메조테라피 (물광주사) — 피부 속 수분·탄력 개선 | 분석 |
| 63 | `related_techniques[1]` | `/M2/related_techniques/1` | string | 자가지방이식 — 본인 지방으로 볼륨 채움, 알레르기 위험 없음 | 분석 |
| 64 | `related_techniques[2]` | `/M2/related_techniques/2` | string | 진피절제주입법 (서브시전 + 필러) — 흉터 치료에 병합 활용 | 분석 |

## 2. 잠정 관찰 (원문과 분리)

각 줄의 「근거」는 Pointer 와 원문 인용이다. 분류 문자: 구조 = 원장 구조 사실, P = 잠정 해석, B = 원문 정보 부족, F = 후속 의미 조사, I = 원문 내 불일치, K = 알려진 분석 한계. 확정 의미·관계가 아니다.

- **OB-S10-01** (구조) safety 에 emergency 키가 있다(이 원장에서 M2·M8 둘뿐). 값은 징후 조건 → 가능성 → 즉시 조치의 한 문장이다. → F5  
  근거: `/M2/safety/emergency/0` 「주사 직후 피부가 하얗게 변하면」
- **OB-S10-02** (I) aftercare 셋째 값은 「시술 후」로 시작하지만 「무균 상태에서 시술해야 하며」는 시술 전·중 행위다. 시점이 한 값 안에서 섞인다. → I4  
  근거: `/M2/aftercare/2` 「시술 후 화장은 완전히 지우고 무균 상태에서 시술해야 하며」
- **OB-S10-03** (B) overview 는 콜라겐 자극형 필러로 칼슘 필러·PLLA 를 들지만 duration 은 히알루론산·칼슘·자가지방이식만 기간을 준다. PLLA 기간은 이 항목에 없다. → B5  
  근거: `/M2/overview` 「(칼슘 필러, PLLA 등)」; `/M2/onset_duration/duration` 「히알루론산 필러 6~18개월, 칼슘 필러 12~24개월, 자가지방이식 6~12개월」
- **OB-S10-04** (F) indications/primary 세 값은 「분류 — 하위 목록」 꼴(주름치료 — 이마주름, …)이고 부위·목적이 섞인다. extended 의 「히알루론산 메조테라피 (물광주사)」는 related_techniques 에도 있고, M4 overview 는 스킨부스터를 「물광주사」로 부른다. → F2, F6  
  근거: `/M2/indications/primary/1` 「윤곽성형 — 이마 키우기」; `/M2/indications/extended/7` 「히알루론산 메조테라피 (물광주사)」; `/M4/overview` 「'물광주사'로 널리 알려져」
- **OB-S10-05** (P) serious 「실명 위험」의 조건은 부위(코, 이마 등 혈관이 눈동맥과 연결된 부위)와 빈도(극히 드물게)를 함께 단다. 부위 역할은 위험 발생 조건이다. → F1  
  근거: `/M2/safety/serious/3` 「코, 이마 등 혈관이 눈동맥과 연결된 부위 시술 시」

## 3. 수동 표현 기록 (직접 읽기)

| ID | 범주 후보 | Pointer | 원문 구간 | 메모 |
|---|---|---|---|---|
| MX110 | frequency_severity_contrast | `/M2/safety/serious/0` | 드물지만 위험 |  |
| MX111 | site_condition_frequency | `/M2/safety/serious/3` | 코, 이마 등 혈관이 눈동맥과 연결된 부위 시술 시 극히 드물게 발생 |  |
| MX112 | sign_condition_possibility | `/M2/safety/emergency/0` | 주사 직후 피부가 하얗게 변하면 혈관이 막혔을 가능성 |  |
| MX113 | urgent_action | `/M2/safety/emergency/0` | 즉시 히알루로니다아제(분해효소) 투여 필요 |  |
| MX114 | time_order_mismatch | `/M2/aftercare/2` | 시술 후 화장은 완전히 지우고 무균 상태에서 시술해야 하며 | 「시술 후」 아래 시술 전 행위(I4) |
| MX115 | negated_causal | `/M2/mechanism` | 자가지방이식은 본인의 지방세포를 옮기는 방식이라 거부반응 없이 |  |
| MX116 | time_window_with_anchor | `/M2/onset_duration/peak` | 붓기가 빠진 후 1~2주 뒤 |  |
| MX117 | subtype_time | `/M2/onset_duration/duration` | 히알루론산 필러 6~18개월, 칼슘 필러 12~24개월, 자가지방이식 6~12개월 (생착률에 따라 다름) |  |
| MX118 | subtype_test_condition | `/M2/contraindications/absolute/2` | 소 콜라겐 필러 사용 시 피부반응검사에서 양성 반응이 나온 경우 |  |
| MX119 | medication_possibility_obligation | `/M2/contraindications/relative/1` | 복용 중이면 멍이 잘 들 수 있으니 의사에게 알릴 것 |  |
| MX183 | historical_claim | `/M2/overview` | 1893년부터 시작된 오랜 역사 |  |

## 4. 형태소 분석 — 이 구획에서 표시한 알려진 오분절·오태깅 (교정 아님)

| ID | Pointer | 구간 | 원문 | 원시 토큰 | 문제 | 영향 |
|---|---|---|---|---|---|---|
| R01-3 | `/M2/indications/primary/1` | [7,9) | 이마 | 이/MM + 마/NNG | 관형사 「이」 오분리 — 부위어가 MM+다른 명사로 쪼개짐 | 부위 표현 탐색 시 「이중턱」「이마」가 「중턱」「마」로 바뀜. 형태소 기반 부위 후보 추출에서 누락·오탐 |
| R07-1 | `/M2/mechanism` | [65,67) | 필러 | 필/NNG + 러/EC | 「필러」가 필 + 러/EC(연결어미)로 분절 | 시술명 「필러」 식별 실패(같은 원장 다른 출현은 NNP 로 정상). 시술명 교차 참조 탐색 누락 |
| R08-1 | `/M2/safety/serious/0` | [7,10) | 필러가 | 필러가/NNG | 「필러」+조사가 한 명사(NNG)로 묶임(필러가·필러와) | 조사 정보 소실 및 명사 형태가 「필러가」로 남아 시술명 집계·대조에서 누락 |
| R11-3 | `/M2/safety/common/1` | [0,1) | 멍 | 멍/MAG | 단독 값 「멍」(타박 멍)을 부사(MAG)로 태깅 | 부작용 사건 명사가 부사로 분류 — 품사로 사건 명사를 고르면 누락. 값 자체는 원문 보존 |

규칙 기반 표현 후보 304건(이 구획)은 [expressions.json](./expressions.json) 의 `section: "S10"` 에 있다. 후보이며 전수 의미 해석이 아니다.
