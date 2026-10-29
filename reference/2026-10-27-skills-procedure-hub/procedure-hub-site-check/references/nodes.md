# 부위 노드 53 — 일반인 용어 · 전문의 용어 · 상위 · 위험 부위

정본 `orchestration/work/phub-recommend/step3-sites.json` `nodes[]`(revision v5 + 한 줄 수정 · open 0 · 2026-10-28)를 옮긴 것이다.
**판정할 때는 이 표가 아니라 정본을 연다** — 정본이 바뀌면 정본이 이긴다. 노드 속성 원본은 `step3-decisions.json` `nodes{}`.

- 상태: 트리 = DEC-002 37 · OQ-206 = 10-27 추가 6 · 3단계 = 10-28 추가 10(U1 등 · 옆구리 · 콧망울 / U2 팔 · 가슴 · 수염 · 구레나룻 · 인중 · 눈썹 · 마리오네트)
- 일반인 용어 = 노드 이름(상담 용어). 전문의 용어 = `anatomical_name{en, ko}` = **겉자리(체표) 이름만** — 근육 · 뼈 · 혈관은 `handoff_note`(4단계)
- 수준: 강 = 레포 파일에 그 이름이 있음(위험 부위 파일은 AI 합의본 — 의학 확정 아님) · 중 = 레포 일부 · 약 = 레포 밖 표준 용어집(FIPAT TA2 · KMA 의학용어 6.1판)만. 지금 강 20 · 중 4 · 약 29 — 약은 노드마다 의료진 질문 1줄(OQ-202)
- 이름 칸 근거 = 그 노드로 가는 문자열 수 · 등장 수(이름 칸 17종 기준). 0 이면 `name_field_exception` 이 있어야 한다(지금 입가 하나 — 묶음 자리)
- 묶음 노드(「(묶음)」 · 입가 · 얼굴 · 바디)는 경계 규칙대로만 문자열을 받는다(SKILL.md §3-5)

| id | 일반인 용어(노드) | 상위 | 상태 | 전문의 용어 en · ko | 수준 | 위험 부위 zone | 이름 칸 근거(문자열 · 등장) | 동의어 · 부위+다른 축(이름 칸 문자열) |
|---|---|---|---|---|---|---|---|---|
| `site.face` | 얼굴 | — | 트리 | Face (facies) · 얼굴 | 강 | — | 7 · 22 | 안면 · 얼굴 · 페이스 · 표정근 · 안면홍조(홍조 → 7단계 고민) · Facial Contouring(윤곽 → 7단계 고민) · 얼굴윤곽(윤곽 → 7단계 고민) |
| `site.forehead-group` | 이마(묶음) | 얼굴 | 트리 | Frontal region (regio frontalis) · 이마부위 | 약 | `forehead` 하위 이마가 소유 | 1 · 3 | 이마/관자놀이 |
| `site.forehead` | 이마 | 이마(묶음) | 트리 | Forehead (frons) · 이마 | 강 | `forehead` 같음 | 6 · 14 | forehead · 이마 · 이마 볼륨(볼륨 → 7단계 고민) · 이마 주름(주름 → 7단계 고민) · 이마지방이식(지방이식 → 2단계 계열) · 이마필러(필러 → 2단계 계열) |
| `site.glabella` | 미간 | 이마(묶음) | 트리 | Glabella · 미간 | 강 | `glabella` 같음 | 3 · 8 | glabella · 미간 · 미간 주름(주름 → 7단계 고민) |
| `site.temple` | 관자놀이 | 얼굴 | 트리 | Temple / temporal region (regio temporalis) · 관자부위 | 강 | `temple` 같음 | 5 · 13 | 관자놀이 · 볼/관자놀이 · 이마/관자놀이 · temple · 관자놀이충전(충전 → 6단계 목적) |
| `site.periorbital-group` | 눈가(묶음) | 얼굴 | 트리 | Periorbital region (regio orbitalis) · 눈확부위 | 강 | `periorbital` 묶음(하위 셋 다 덮음) 추천 | 3 · 5 | periorbital · 눈 주변 · 눈가 쳐짐(쳐짐 → 7단계 고민) |
| `site.lateral-canthus` | 눈가 | 눈가(묶음) | 트리 | Lateral canthal area (crow's feet) · 가쪽눈구석 주변 | 약 | `periorbital` 상위 묶음 zone | 4 · 16 | 눈가 · 까마귀발 주름(주름 → 7단계 고민) · 눈가보톡스(보톡스 → 2단계 계열) · 눈가 주름(주름 → 7단계 고민) |
| `site.infraorbital` | 눈밑 | 눈가(묶음) | 트리 | Infraorbital region · tear trough · 눈확아래부위 · 눈물고랑 | 강 | `periorbital` 상위 묶음 zone | 5 · 10 | 눈밑 · 눈밑꺼짐(꺼짐 · 주름 · 볼륨 → 7단계 고민) · 눈밑 볼륨(꺼짐 · 주름 · 볼륨 → 7단계 고민) · 다크서클필러(다크서클 → 7단계 고민 / 필러 → 2단계 계열) · 애교필러(필러 → 2단계 계열) |
| `site.eyelid` | 눈꺼풀 | 눈가(묶음) | 트리 | Eyelid (palpebra) · 눈꺼풀 | 강 | `periorbital` 상위 묶음 zone | 3 · 5 | 눈꺼풀 처짐(처짐 → 7단계 고민) · 눈꺼풀쳐짐(처짐 → 7단계 고민) · 아이라인반영구(반영구 → 2단계 계열) |
| `site.nose-group` | 코(묶음) | 얼굴 | 트리 | Nose (nasus) · 코 | 강 | `nose` 묶음(코끝 · 콧등 · 콧망울 포함) 추천 | 1 · 2 | nose |
| `site.nose` | 코 | 코(묶음) | 트리 | External nose · 바깥코 | 약 | `nose` 상위 묶음 zone | 5 · 12 | 코 · 코 라인(라인 → 7단계 고민) · 코실리프팅(실리프팅 → 2단계 계열) · 코조각주사(조각주사 → 2단계 계열(지방분해 주사)) · 코필러(필러 → 2단계 계열) |
| `site.nasal-tip` | 코끝 | 코(묶음) | 트리 | Tip of nose (apex nasi) · columella · 코끝 | 강 | `nose` 상위 묶음 zone | 1 · 5 | 코끝 |
| `site.nasal-dorsum` | 콧등 | 코(묶음) | OQ-206 | Dorsum of nose (dorsum nasi) · 콧등 | 강 | `nose` 상위 묶음 zone | 2 · 3 | 콧대 · 콧등 |
| `site.cheek-group` | 볼(묶음) | 얼굴 | 트리 | Cheek (Malar/Buccal) · 볼 | 강 | `cheek` 묶음 추천(Malar=광대 · Buccal=볼 둘 다) | 4 · 8 | cheek · Cheek (Malar/Buccal) · 볼/관자놀이 · 볼/광대 |
| `site.cheek` | 볼 | 볼(묶음) | 트리 | Buccal region (regio buccalis) · 볼부위 | 강 | `cheek` 상위 묶음 zone | 7 · 12 | 볼 · 볼 볼륨 (볼륨 · 충전 → 7단계 고민) · 볼볼륨충전(볼륨 · 충전 → 7단계 고민) · 볼살(살(지방) → 7단계 고민) · 볼지방이식(지방이식 → 2단계 계열) · 볼쳐짐(처짐 → 7단계 고민) · 볼필러(필러 → 2단계 계열) |
| `site.zygoma` | 광대 | 볼(묶음) | 트리 | Zygomatic (malar) region (regio zygomatica) · 광대부위 | 강 | `cheek` 상위 묶음 zone | 2 · 5 | 광대 · 광대축소주사(축소 → 6단계 목적 / 주사 → 2단계 계열) |
| `site.perioral` | 입가 | 얼굴 | 트리 | Perioral region (regio oralis) · 입부위 | 강 | `lips` 관련(입가 주름은 lips zone 이 다룸) | 0 · 0 — 예외: 묶음 자리 — 이름 칸 근거 0. DEC-002 「원천 근거 없음」은 이름 칸 기준으로 맞다. 하위(팔자 · 입술 · 입꼬리 · 잇몸 · 마리오네트 · 인중)가 이름 칸 근거를 가진다(브리프 예외) | — |
| `site.nasolabial` | 팔자 | 입가 | 트리 | Nasolabial fold (sulcus nasolabialis) · 코입술고랑 | 강 | `nasolabial` 같음(고민 「주름」 뗌 — D-07) | 3 · 6 | nasolabial · Nasolabial Fold · 팔자주름(주름 → 7단계 고민) |
| `site.lips` | 입술 | 입가 | 트리 | Lips (labia oris) · 입술 | 강 | `lips` 같음 | 5 · 10 | lips · 입술 · 입술 볼륨(볼륨 · 확대 · 라인 → 7단계 고민) · 입술반영구(반영구 → 2단계 계열) · 입술필러(필러 → 2단계 계열) |
| `site.mouth-corner` | 입꼬리 | 입가 | 트리 | Angle of mouth / oral commissure (angulus oris) · 입꼬리 | 강 | `lips` 관련(구각 · 상순동맥 유입) | 1 · 1 | 입꼬리 |
| `site.gingiva` | 잇몸 | 입가 | 트리 | Gingiva (gummy smile 부위) · 잇몸 | 약 | 위험 부위 원장 없음 | 1 · 1 | 잇몸미소(잇몸 노출 미소 → 7단계 고민) |
| `site.chin-group` | 턱(묶음) | 얼굴 | 트리 | Mandibular region (lower jaw) · 아래턱부위 | 약 | 하위 턱끝 · 턱선이 각 zone 소유 | 5 · 10 | 턱 · 턱/턱선 · ⚠하관 · 턱보톡스(보톡스 → 2단계 계열) · 턱필러(필러 → 2단계 계열) |
| `site.chin` | 턱끝 | 턱(묶음) | 트리 | Chin (mentum) · mental region (regio mentalis) · 턱끝부위 | 강 | `chin` 턱끝 추천 | 6 · 7 | chin · Chin (Mentum) · 자갈턱(자갈턱 → 7단계 고민) · 턱 끝 볼륨(볼륨 · 연장 → 7단계 고민) · 턱끝 연장(볼륨 · 연장 → 7단계 고민) · 턱 끝 지방이식(필러 · 지방이식 → 2단계 계열) |
| `site.jawline` | 턱선 | 턱(묶음) | 트리 | Jawline · (표준 체표 이름 없음 — 상담 용어 「턱선」) | 중 | `jawline` 같음 | 10 · 17 | 턱라인 · jawline · Jawline (Mandibular border) · 턱선 · 네페르티티(네페르티티 리프트 → 4단계 기법) · 네페르티티 리프트(네페르티티 리프트 → 4단계 기법) · ⚠불독살(처짐 · 살 → 7단계 고민) · 턱선무너짐(처짐 → 7단계 고민) · 턱선보톡스(보톡스 → 2단계 계열) · 턱선실리프팅(실리프팅 → 2단계 계열) |
| `site.masseter` | 사각턱 | 턱(묶음) | 트리 | Parotideomasseteric region (regio parotideomasseterica) · (KMA 표제어 없음 — TA2 이름만) | 약 | `jawline` 관련(교근 보톡스 경고가 cheek · jawline 두 zone 에) | 3 · 12 | 사각턱 · 교근축소(축소 → 6단계 목적) · 사각턱보톡스(보톡스 → 2단계 계열) |
| `site.submental` | 턱밑 | 턱(묶음) | 트리 | Submental region (regio submentalis) · 턱끝밑부위 | 약 | 위험 부위 원장 없음 | 3 · 21 | 턱밑지방 · 턱밑 · 이중턱(이중턱(지방) → 7단계 고민) |
| `site.full-face` | 얼굴 전체 | 얼굴 | 트리 | Whole face · 얼굴 전체 | 약 | 하위 zone 11곳 전부 해당 | 5 · 33 | 얼굴 전체 · 전체얼굴 · 풀페이스 · 페이스앤넥큐레이션(큐레이션 → 6단계 패키지) · 풀페이스큐레이션(큐레이션 → 6단계 패키지) |
| `site.neck-group` | 목(묶음) | — | 트리 | Neck (collum) · 목 | 강 | `neck` 묶음 추천 | 1 · 2 | neck |
| `site.neck` | 목 | 목(묶음) | 트리 | Anterior region of neck (regio cervicalis anterior) · 목 앞부위(앞목) — 경부 | 약 | `neck` 상위 묶음 zone | 8 · 14 | 목 · 네페르티티(네페르티티 리프트 → 4단계 기법) · 네페르티티 리프트(네페르티티 리프트 → 4단계 기법) · 넥큐레이션(큐레이션 → 6단계 패키지) · 초음파목(초음파 → 2단계 계열) · 목 실리프팅(리프팅 → 6단계 목적) · 목주름(주름 · 밴드 → 7단계 고민) · 페이스앤넥큐레이션(큐레이션 → 6단계 패키지) |
| `site.trapezius` | 승모근 | 목(묶음) | 트리 | Posterior region of neck (regio cervicalis posterior · nucha) · shoulder (omos) · 목덜미부위 · 어깨 | 약 | `neck` 관련(부신경) | 3 · 10 | 승모근 · 어깨라인 · 승모근보톡스(보톡스 → 2단계 계열) |
| `site.scalp` | 두피 | — | 트리 | Scalp · 머리덮개 | 중 | 위험 부위 원장 없음 | 11 · 31 | Scalp · 두피 · MTS두피(시술 이름 → 2단계 계열) · 두피PRP(시술 이름 → 2단계 계열) · 두피메조(시술 이름 → 2단계 계열) · 두피스케일링(시술 이름 → 2단계 계열) · 두피엑소좀(시술 이름 → 2단계 계열) · 두피주사(시술 이름 → 2단계 계열) · 두피치료(시술 이름 → 2단계 계열) · SMP(반영구 → 2단계 계열) · 헤어라인반영구(반영구 → 2단계 계열) |
| `site.body` | 바디 | — | 트리 | Body (trunk · limbs) · 몸통 · 팔다리 | 약 | 위험 부위 원장 없음 | 8 · 23 | Body · 바디 · EMS 바디(EMS → 2단계 계열) · 바디리프팅(라인 · 리프팅 · 탄력 → 7단계 고민) · 바디 쳐짐(라인 · 리프팅 · 탄력 → 7단계 고민) · 바디탄력(라인 · 리프팅 · 탄력 → 7단계 고민) · 바디(여성)(여성 → 대상 속성(성별 · 6단계)) · 바디큐레이션(큐레이션 → 6단계 패키지) |
| `site.axilla` | 겨드랑이 | 바디 | 트리 | Axilla (regio axillaris) · 겨드랑부위 | 약 | 위험 부위 원장 없음 | 1 · 6 | 겨드랑이 |
| `site.upper-arm` | 팔뚝 | 바디 | 트리 | Posterior upper arm (regio brachii posterior) · 위팔 뒤부위 | 약 | 위험 부위 원장 없음 | 1 · 4 | ⚠팔뚝 |
| `site.abdomen` | 복부 | 바디 | 트리 | Abdomen (regio abdominalis) · 배부위 | 중 | 위험 부위 원장 없음 | 2 · 9 | 복부 · ⚠임신선(튼살(임신선) → 7단계 고민) |
| `site.thigh` | 허벅지 | 바디 | 트리 | Thigh (regio femoris) · 넙다리부위 | 약 | 위험 부위 원장 없음 | 2 · 4 | 허벅지 · 허벅지 안쪽(안쪽(위치 수식) → 1단계 규격 · 단위) |
| `site.calf` | 종아리 | 바디 | 트리 | Calf (sura) · sural region (regio surae) · 장딴지(종아리) | 약 | 위험 부위 원장 없음 | 1 · 2 | 종아리 |
| `site.whole-body` | 전신 | 바디 | 트리 | Whole body surface · 온몸 피부 | 약 | 위험 부위 원장 없음 | 1 · 1 | 전신 |
| `site.hand` | 손 | 바디 | OQ-206 | Hand (manus) · 손 | 약 | 위험 부위 원장 없음 | 1 · 3 | 손 |
| `site.foot` | 발 | 바디 | OQ-206 | Foot (pes) · 발 | 약 | 위험 부위 원장 없음 | 1 · 3 | 발 |
| `site.leg` | 다리 | 바디 | OQ-206 | Lower limb (membrum inferius) · 다리 · 하지 | 중 | 위험 부위 원장 없음 | 2 · 3 | 다리 · 하지정맥류(정맥류 → 7단계 고민) |
| `site.bikini` | 비키니 | 바디 | OQ-206 | Inguinal · pubic region (regio inguinalis · regio pubica) · 샅굴부위 · 두덩부위 | 약 | 위험 부위 원장 없음 | 1 · 2 | 비키니 |
| `site.buttock` | 힙 | 바디 | OQ-206 | Gluteal region (regio glutealis) · 볼기부위 | 약 | 위험 부위 원장 없음 | 1 · 2 | 힙 |
| `site.back` | 등 | 바디 | 3단계 | Back (dorsum · regiones dorsi) · 등부위 | 약 | 위험 부위 원장 없음 | 3 · 5 | 등 · 브라라인 · 등살주사(살(지방) → 7단계 고민) |
| `site.flank` | 옆구리 | 바디 | 3단계 | Flank (regio lateralis abdominis) · 옆구리 | 약 | 위험 부위 원장 없음 | 2 · 3 | 러브핸들 · 옆구리 |
| `site.nasal-ala` | 콧망울 | 코(묶음) | 3단계 | Ala of nose (ala nasi) · 콧방울 | 강 | `nose` 상위 묶음 zone(비익 괴사 · 함몰 별도 경고) | 1 · 1 | 콧망울 |
| `site.arm` | 팔 | 바디 | 3단계 | Upper limb (membrum superius) · 팔 | 약 | 위험 부위 원장 없음 | 1 · 2 | 팔 |
| `site.chest` | 가슴 | 바디 | 3단계 | Chest (regio pectoralis) · breast (mamma) · 가슴부위 | 약 | 위험 부위 원장 없음 | 1 · 2 | 가슴 |
| `site.beard` | 수염 | 얼굴 | 3단계 | Beard area · 수염 자리 | 약 | 위험 부위 원장 없음 | 1 · 2 | 수염 |
| `site.sideburn` | 구레나룻 | 얼굴 | 3단계 | Sideburn (preauricular) area · 귀앞 털 자리 | 약 | 위험 부위 원장 없음 | 1 · 2 | 구레나룻 |
| `site.philtrum` | 인중 | 입가 | 3단계 | Philtrum · 인중 | 약 | `lips` 관련(상순 · 상구순) | 1 · 2 | 인중 |
| `site.eyebrow` | 눈썹 | 눈가(묶음) | 3단계 | Eyebrow (supercilium) · 눈썹 | 약 | `glabella` 관련(forehead · glabella 의 「눈썹 처짐」 경고) | 1 · 2 | 눈썹반영구(반영구 → 2단계 계열) |
| `site.marionette` | 마리오네트 | 입가 | 3단계 | Marionette line (labiomandibular fold) · 입꼬리-턱 주름 자리 | 약 | `lips` 관련(구각 · DAO) | 1 · 2 | 마리오네트라인(라인(주름) → 7단계 고민) |

⚠ = 근거 약(값 + 의료진 질문). 괄호 = 떼어 넘긴 다른 축 → 단계.

## 근육 · 뼈 이름을 뺀 5 노드 → 4단계 넘김 메모

| 노드 | v5 전 전문의 용어(수준) | 지금(겉자리 · 수준) | handoff_note |
|---|---|---|---|
| 턱선 | 아래턱뼈 아래모서리 · Mandibular border (margo inferior mandibulae) (강) | (표준 체표 이름 없음 — 상담 용어 「턱선」) · Jawline (중) | 뼈 지표 아래턱뼈 아래모서리(mandibular border) → 4단계 기법(깊이 · 지표) |
| 사각턱 | 아래턱뼈각 · 깨물근 · Mandibular angle · masseter (angulus mandibulae · m. masseter) (강) | (KMA 표제어 없음 — TA2 이름만) · Parotideomasseteric region (regio parotideomasseterica) (약) | 대상 근육 깨물근(masseter) · 뼈 지표 아래턱뼈각(angulus mandibulae) → 4단계 기법(대상 근육) |
| 목 | 앞목부위 · 넓은목근 · Anterior cervical region · platysma (강) | 목 앞부위(앞목) — 경부 · Anterior region of neck (regio cervicalis anterior) (약) | 대상 근육 넓은목근(platysma) → 4단계 기법(대상 근육) |
| 승모근 | 등세모근 · Trapezius (m. trapezius) (강) | 목덜미부위 · 어깨 · Posterior region of neck (regio cervicalis posterior · nucha) · shoulder (omos) (약) | 대상 근육 등세모근(trapezius) → 4단계 기법(대상 근육) |
| 종아리 | 종아리부위 · 장딴지근 · Calf (regio surae) · gastrocnemius (중) | 장딴지(종아리) · Calf (sura) · sural region (regio surae) (약) | 대상 근육 장딴지근(gastrocnemius) → 4단계 기법(대상 근육) |

나머지 48 노드는 겉자리 이름(TA2 regiones · 부분 이름 · 겉 고랑/주름 — 코입술고랑 · 눈물고랑 · 인중)이라 그대로. 턱(묶음) 「아래턱부위 · Mandibular region」은 아래턱(턱 · 하악, KMA jaw)을 몸 부분으로 쓴 것이라 그대로 둠

## 위험 부위 zone 11 대응(B9 — 최종 의료진 OQ-202)

| zone | 노드 | 판정 | 근거 |
|---|---|---|---|
| `forehead` | 이마 | 같음 | name_ko · name_en |
| `glabella` | 미간 | 같음 | name_ko · name_en |
| `temple` | 관자놀이 | 같음 | name_ko · name_en |
| `periorbital` | 눈가(묶음) | 묶음 추천(확인 필요 → 근거 있음) | target_muscle 「안륜근 — 까마귀발, 눈밑 주름」 · tissue_data.tear_trough_anatomy · clinical_pearls 「하안검 보톡스」 · vessels 「내안각동맥 — 상하 안검 내측 주행」 — 눈가 · 눈밑 · 눈꺼풀 셋 다 |
| `nose` | 코(묶음) | 묶음 추천(확인 필요 → 근거 있음) | safe_injection_depth 「골막상 (코뼈 부위) 또는 연골막상 (비첨부)」 · vessels 주상동맥(비주) · 외비동맥(비익) · 배비동맥(코등) — 코끝 · 콧등 · 콧망울(새) 모두 |
| `nasolabial` | 팔자 | 같음 | 고민 「주름」 뗌(D-07) |
| `cheek` | 볼(묶음) | 묶음 추천(확인 필요 → 근거 있음) | safe_injection_depth 「골막상 (관골부) 또는 피하 (협부)」 · filler_specific 「관골부(malar) … 협부: 피하 캐뉼러」 — 광대 · 볼을 따로 지시 |
| `lips` | 입술 | 같음 + 입꼬리 · 입가 · 인중(새) 관련 | clinical_pearls 「구각(oral commissure)」 · target_muscle 「입가 주름」 · 「상순」 |
| `chin` | 턱끝 | 턱끝 추천(확인 필요 → 근거 있음) | name_en 「Chin (Mentum)」 · safe_injection_depth 「이부 정중앙」 · target_muscle 「이근 (Mentalis)」 · vessels 「턱끝 상방」 — name_ko 「턱」만 넓음 |
| `jawline` | 턱선 | 같음 + 사각턱 관련 | name_en 「Mandibular border」 · target_muscle 「교근 (Masseter) — 사각턱」 |
| `neck` | 목(묶음) | 묶음 추천(확인 필요 → 근거 있음) | target_muscle 「광경근 (Platysma)」(목) + nerves 「부신경 — 승모근, 흉쇄유돌근 운동 — 손상 시 어깨 처짐」(승모근 쪽) |

## 경계 규칙(`step3-decisions.json` boundary_rules)

| 경계 | 원천 문자열이 가는 곳 | 근거 |
|---|---|---|
| 이름이 같은 묶음 · 좁은 노드(이마 · 눈가 · 코 · 볼 · 목 + 턱(묶음)) | 원천 문자열 「이마 · 눈가 · 코 · 볼 · 목」은 좁은 노드로. 묶음 노드는 동의어를 갖지 않고 (가) 고민 라벨처럼 하위 이름을 나란히 묶은 칸(「이마/관자놀이」 · 「볼/광대」 · 「턱/턱선」 · 「눈가 쳐짐」) (나) 위험 부위 zone 이름(periorbital · nose · cheek · neck) (다) 그 부위 해부 묶음 이름(Periorbital · Nose · Cheek · Neck · 경부 · 하악 · 하관)만 받는다 | DEC-002 「상위 = 묶음 · 하위 = 그 이름이 가리키는 좁은 부위」 |
| 「턱」 | 턱 단독 · 턱필러 · 턱보톡스 → 턱(묶음). 원천 detail 이 「턱끝 연장」 · 「사각턱 축소」로 하위를 정해 주면 단위 시술(5단계)에서 하위로 내린다 | taxonomy problem P1-3 items detail |
| 얼굴 ↔ 얼굴 전체 | 얼굴 · 안면 · face · 페이스 → 얼굴(최상위 묶음). 전체얼굴 · 얼굴 전체 · 안면 전체 · 전안면 · 풀페이스 → 얼굴 전체. 시장가 「(전체얼굴)」 · 「(풀페이스)」는 모두 얼굴 전체 | DEC-002 D-07 「얼굴 전체」는 부위 노드 · DEC-003 D-05 필링 기본값 |
| 바디 ↔ 전신 | 바디 · 탄탄한 몸 · 몸매 · 신체 처짐 → 바디(묶음). 전신은 「레이저 제모 (전신)」 · 「팔뚝, 복부 등 전신 처짐」 2곳만 노드 「전신」(몸 표면). 그 밖 「전신」 28회 + 전신항노화 · 전신재생 · 전신발진 등은 계통 → 부위 아님(수액은 「해당 없음」) | DEC-003 OQ-306 처리 · _RESUME 10-27 「「전신」 두 뜻 분리」 |
| 「(묶음)」 이름 | v3 트리 이름 그대로(이마(묶음) · 눈가(묶음) · 코(묶음) · 볼(묶음) · 턱(묶음) · 목(묶음)). 입가는 v3 이름 「입가」 그대로 — 좁은 「입가」 노드가 없어 원천 「입가 · 입 주변 · perioral · 구주위」가 바로 이 노드로 간다 | procedure-master-v3.json site_tree |
| 「‹부위›라인」(W7) | ‹부위›라인 = 부위 + 고민 「라인」(7단계). 예외: 턱라인(= 턱선 · 하악연 해부명) · 어깨라인(승모근 동의어 — DEC-002 D-03). 허리라인은 옆구리 + 라인(근거 약) | 검수 W7 · DEC-002 D-03 |

## 트리 밖 이름 판정(`out_of_tree` · D-05)

| 이름 | 묶음 | 결정 | 행선지 | D-05 ① 원천이 따로 부른다 | D-05 ② 시술 · 안전이 달라진다 |
|---|---|---|---|---|---|
| 등 | U1 | 새 노드 | 등 | 용도 「등살주사」(name) · 「등 브라라인」(detail) · 고민 P10-3 「수염/가슴/등」 | 지방분해 주사 · 제모 — 바디 다른 하위와 시술 대상이 다름(위험 부위 원장은 없음) |
| 브라라인 | U1 | 등 동의어 | 등 | 용도 detail 「등 브라라인」 안에서만 — 따로 부르는 이름 칸 없음 | 등과 같은 시술(등살주사) |
| 엉덩이 | U1 | 힙 동의어 | 힙 | 이름 칸에 없음(본문 12회) — 힙은 시장가 「이모드 (힙)」으로 이미 노드(OQ-206) | 같은 자리 · 같은 시술(「엉덩이 리프팅 (힙업)」 — 원천이 두 말을 같은 뜻으로 씀) |
| 옆구리 | U1 | 새 노드 | 옆구리 | 시장가 「쿨스컬프팅 (러브핸들 양쪽)」 · 용도 「러브핸들주사 (옆구리 지방분해 주사)」 | 쿨스컬프팅 어플리케이터 · 지방분해 주사 부위로 복부와 따로 값이 매겨짐 |
| 콧망울 | U1 | 새 노드 | 콧망울 | 용도 detail 「콧망울 지방분해 · 코 라인 날렵하게」 · 위험 부위 nose 본문 「비익」 | 안전이 다름 — nose zone 「비익 괴사 위험」(외비동맥) · 「비익 함몰(alar collapse) … 코 호흡 장애」(비근근 보톡스) |
| 페이스 | U1 | 얼굴 동의어 | 얼굴 | 용도 detail 「페이스/바디/두피」 — 바디 · 두피(최상위)와 나란히 쓴 최상위 뜻 | 얼굴과 다른 시술 · 안전 없음 |
| 하관 | U1 | 턱(묶음) 동의어 | 턱(묶음) | 용도 detail 「턱선+하관 라인 정리 전용」 1곳 — 기존 묶음과 같은 범위를 가리키는 말 | 새 시술 · 안전 없음. 문헌 「Botulinum toxin type A contours the lower face」(PMID 33714246)는 교근 보톡스 = 턱 묶음 안 |
| 팔 | U2 | 새 노드 | 팔 | 고민 P10-2 · CC 「겨드랑이/팔/다리」(제모) | 제모는 팔 전체, 팔뚝은 지방 · 탄력(쿨스컬프팅 · EMS) — 범위가 다름. 같은 고민 항목의 「다리」는 OQ-206 에서 노드로 추가됨(선례) |
| 가슴 | U2 | 새 노드 | 가슴 | 고민 P10-3 · CC 「수염/가슴/등」(제모) | 제모 · 지방이식(indications 「가슴 확대」) |
| 수염 | U2 | 새 노드 | 수염 | 고민 P10-3 · CC 「수염/가슴/등」(남성 제모) | 제모 전용 자리 |
| 구레나룻 | U2 | 새 노드 | 구레나룻 | 고민 P10-1 · CC 「인중/구레나룻」(얼굴 제모) | 제모 전용 자리 |
| 인중 | U2 | 새 노드 | 인중 | 고민 P10-1 · CC 「인중/구레나룻」(제모) | 제모 + 보톡스(「짧은 인중 늘리기」) · 필러(「입술라인 및 인중선 확대」) — 입술과 시술이 다름 |
| 눈썹 | U2 | 새 노드 | 눈썹 | 고민 P1-7 · CC 「눈썹반영구」 | 반영구 · 실 「눈썹 리프팅」 · 보톡스 「눈썹 올리기」. 안전 경고 「눈썹 처짐(Mephisto sign)」(glabella) · 「손상 시 … 눈썹 처짐」(forehead) |
| 마리오네트 | U2 | 새 노드 | 마리오네트 | 고민 P2-2 · CC 「마리오네트라인」 | 필러 · 실리프팅 대상(원천 정의 「입꼬리에서 턱으로 내려가는 주름」). 「팔자주름」 → 노드 팔자와 같은 꼴(D-07) |
| 무릎 | B5 | 다리 동의어 | 다리 | 이름 칸 없음 — indications 「무릎 위 지방」 · 「팔뚝/무릎 등 신체 처짐」 | 근거 없음 |
| 불독살 | B5 | 턱선 동의어 + 고민 처짐 | 턱선 | 고민 P3-1 · CC 「볼쳐짐/불독살」 — 처진 살(고민)이 붙은 말 | jowl 은 하악연 위 처짐 — jawline zone(Mandibular border) |
| 골반저근 | B6 | 부위 아님(비미용 적응증) | 계열 밖(비미용) — 부위 노드 없음 | 이름 칸 없음 — EMS indications 「골반저근 강화 (요실금 개선)」 | 미용 상담 부위 아님 |
| 관절치료 | B6 | 부위 아님(비미용 · 계열 밖) | 계열 밖(비미용) — 부위 노드 없음 | 시장가 「줄기세포 관절치료」 — v3 market_rows_skipped 에 이미 빠짐 | 미용 시술 아님 |
