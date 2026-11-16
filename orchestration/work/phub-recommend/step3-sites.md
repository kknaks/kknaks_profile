---
type: silver
id: step3-sites
title: "실버 3단계 — 부위 원장"
product: procedure-hub
feature: phub-recommend
decision: "_RESUME.md §2 2026-10-28 「3단계 부위 조사(step3-research) 반영 — 전부 추천대로(사용자)」 · 사용자 「추천으로 가자」"
revision: "v5 — 범위 바로잡기(부위 = 「어디에 맞냐」 · 원천은 이름 칸만 · _RESUME §2 10-28)"
generated_by: step3-apply.py
data: step3-sites.json
---

# 실버 3단계 — 부위 원장

> **기준(v5)**: 부위 = 「어디에 맞냐」 — 시술 받는 사람이 말하는 자리, 사람 몸 겉(체표)에서 가리킬 수 있는 자리. 뼈 · 근육 · 혈관 · 조직층은 부위가 아니다. **원천은 이름 칸 17개만**(`step3-decisions.json` name_fields) — 설명 문장 칸의 해부 낱말은 세지 않는다. 노드 이름 2벌: 일반인 용어 = 노드 이름 · 전문의 용어 = 겉자리 이름(근육 · 뼈 이름은 4단계 넘김 메모).

## 셈

- 원천: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26` JSON 21개 · 문자열 칸 22,749 중 **이름 칸 17종의 1,953칸만** 셈
- **범위 바로잡기 전 → 후**: 문자열 525 → 176 · 등장 3,627 → 440회 · 노드로 333 → 153 · 넘김 192 → 23 · 근거 약 28 → 4 · 의료진 질문 55 → 35. 설명 문장 칸에만 나오던 결정 350행은 `strings_out_of_scope`(셈 밖 · 기록만)
- **노드 53** = DEC-002 트리 37 · OQ-206 추가 6 · 3단계 추가 10
- **원천 부위 문자열 176 · 등장 440회** — 노드로 153(393회 · 동의어 칸 76 · 부위+다른 축 칸 82) · 단계로 넘김 23(47회)
  - 넘김 단계별: 1단계 제품 8 · 7단계 고민 6 · 4단계 기법 3 · 5단계 단위 시술 경로 2 · 계열 밖(비미용) — 부위 노드 없음 1 · 2단계 계열 1 · 사후관리 문구 1 · 4단계 대상 근육 1
- **open 0** — 결정 없는 문자열 0 · 사전 밖 부위 형태소 잔여 0(허용 목록 대조) · 행선지 오류 0 · 위험 부위 대응 11 일치 · 조사 판 근거 약 누락 0
- **근거 약 4문자열** · 해부학 이름 수준 강 20 · 약 29 · 중 4
- **의료진 질문 35** = 근거 약 문자열(B4) 4 + 해부학 이름 — 근거 약(W5) 29 + 위험 부위 대응(B9) 1 + 해부학 이름(B10) 1
- 이번 판에서 바뀐 것 73건(아래 「바뀐 행」) · 원천에 없는 결정 문자열 0

> 결정 `step3-decisions.json`(행선지 · 노드 속성) · 사전 `step3-lexicon.json` · 재현 `python3 step3-apply.py`. 새 원천이 들어오면 사전에 잡혔는데 결정에 없는 문자열 · 사전 밖 부위 형태소가 open 으로 나온다 — 결정 · 사전 · 허용 목록에 더하면 닫힌다.

## 바뀐 행(검수 반영)

| 판 | 문자열(키) | 바뀐 것 |
|---|---|---|
| v2 | 볼/관자놀이 · 볼/관자놀이 | W6 kind |
| v2 | 무릎 · 무릎 | F2 근거 약 추가 |
| v2 | 꺼진눈 · 눈 주변 | F3(b) D-07 분리 |
| v2 | 손등회춘술 · 손등 | F3(b) D-07 분리 |
| v2 | 임신선 · 복부 | F3(b) D-07 분리 |
| v2 | lowerface · 하안면 | F2 근거 약 추가 |
| v2 | 하안면 · 하안면 | F2 근거 약 추가 |
| v2 | ems바디 · 바디 | F3(b) D-07 분리 |
| v2 | 이마/관자놀이 · 이마/관자놀이 | W6 kind |
| v2 | 턱/턱선 · 턱/턱선 | W6 kind |
| v2 | 볼/광대 · 볼/광대 | W6 kind |
| v2 | 불독살 · 불독살 | F2 근거 약 추가 |
| v2 | 탄탄한몸 · 바디 | F3(b) D-07 분리 |
| v2 | 신체처짐 · 바디 | F3(b) D-07 분리 |
| v2 | 전신처짐 · 전신 | F3(b) D-07 분리 |
| v2 | 초음파목 · 목 | F3(b) D-07 분리 |
| v2 | 하안면부 · 하안면 | F2 근거 약 추가 |
| v2 | 하관 · 하관 | F2 근거 약 추가 |
| v2 | 허리라인 · 옆구리 | F2 근거 약 추가; W7 ‹부위›라인 = 부위 + 고민 라인 |
| v2 | 토끼주름 · 토끼주름 | F3(b) D-07 분리 · 사전 항목 분리 |
| v2 | bunnylines · 토끼주름 | F1 대소문자 · F3(b) D-07 분리 |
| v2 | 상악골 · 상악골 | F4 턱(묶음) → 볼(묶음) · 질문 문구 |
| v2 | 위턱뼈 · 상악골 | F4 턱(묶음) → 볼(묶음) · 질문 문구 |
| v2 | deeptemporalfascia · 해부 지표(뼈 · 선 · 구조) | F1 원천 전수 누락 |
| v2 | superiortemporalline · 해부 지표(뼈 · 선 · 구조) | F1 원천 전수 누락 |
| v2 | orbitalseptum · 해부 지표(뼈 · 선 · 구조) | F1 원천 전수 누락 |
| v2 | 이개 · 해부 지표(뼈 · 선 · 구조) | F1 원천 전수 누락 |
| v2 | 구강 · 구강 · 구순 질환 | F1 원천 전수 누락 |
| v2 | 구순포진 · 구강 · 구순 질환 | F1 원천 전수 누락 |
| v2 | 구순염 · 구강 · 구순 질환 | F1 원천 전수 누락 |
| v2 | dryeye · 눈(기관 · 동작) | F1 원천 전수 누락 |
| v2 | dryeyes · 눈(기관 · 동작) | F1 원천 전수 누락 |
| v2 | aroundthemouth · 입가 | F1 원천 전수 누락 |
| v2 | 뱃살 · 뱃살 | F1 원천 전수 누락 |
| v2 | facialcontouring · 얼굴윤곽 | F1 원천 전수 누락 |
| v2 | bodycontouring · body contouring | F1 원천 전수 누락(검수 표 밖 1 — Body 패턴이 함께 잡음) |
| v2 | body · Body(대분류 영문) | F1 원천 전수 누락 |
| v2 | node · 두피 | F5 해부학 이름 근거 키 |
| v2 | node · 사각턱 | F5 해부학 이름 근거 키 |
| v2 | node · 팔자 | F5 해부학 이름 근거 키 |
| v2 | node · 얼굴 | F5 해부학 이름 근거 키 |
| v2 | dorsum · 콧등 | 잔여 검사(W2)로 찾은 사전 밖 문자열 |
| v2 | 입냄새 · 입냄새 | 잔여 검사(W2)로 찾은 사전 밖 문자열 |
| v2 | hair · hair | 잔여 검사(W2)로 찾은 사전 밖 문자열 |
| v2 | 손으로 · 손(위생 · 증상) | 잔여 검사(W2)로 찾은 사전 밖 문자열 |
| v2 | 머리높여 · 상체 거상 | 잔여 검사(W2)로 찾은 사전 밖 문자열 |
| v2 | 측두 · 측두부 | 잔여 검사 — 「측두의」를 사전 패턴에 넣음(같은 행, 등장 +1) |
| v2 | 입 · 입(동작) | 잔여 검사 — 「입을 크게 벌리」 · 「입과 입술 움직임」을 사전 패턴에 넣음(같은 행) |
| v3 | 쇄골 · 해부 지표(뼈 · 선 · 구조) | N2 결정 note — 같은 표면 다른 뜻(쇄골 라인 필러) |
| v3 | 헤어라인반영구 · 헤어라인반영구 | W-b kind 동의어 → 부위+다른 축(D-07)(handoff 「반영구 → 2단계 계열」 있음) |
| v3 | smp · 헤어라인반영구 | W-b kind 동의어 → 부위+다른 축(D-07)(handoff 「반영구 → 2단계 계열」 있음) |
| v3 | 입술 · 입술 | N1 「지방흡입술」 오매칭 뺌(사전 (?<!흡)) — 등장 25 → 24 |
| v3 | 등 · 등 | N2 패턴형 허용으로 드러난 부위 「등」 — 「등 지방」(indications 2) · 「등 마사지」(등살주사 aftercare 1)를 사전에 넣음(등장 8 → 11). 「목 마사지」가 목으로 가는 것과 같은 규칙 |
| v3 | lexicon · 볼 계열 | N2 볼 계열 패턴 앞 글자 막기 (?<![귓귀]) |
| v3 | lexicon · 목 라인 | N2 「목 라인」 앞 글자 막기(발목 라인) |
| v3 | lexicon · 질 | N2 「질」 문맥 패턴(타이트닝 · 레이저 · 건조 · 이완) — 지금 원천 0 |
| v3 | lexicon · residual | N2 잔여 형태소 한글 14 · 영문 10 추가 · 등 · 배 허용을 패턴형으로 |
| v3 | lexicon · fixture | N2-4 고정 시험 38건(step3-fixtures/cases.json · step3-fixture-test.py) — 첫 판 35/38: 저자 이름 「Shin」 허용이 대소문자 무시라 소문자 shin 을 막음 · 「지방흡입술」(조사 없는 꼴) 허용 누락 → 패턴형 허용으로 고침 · 치은은 사전 잇몸 항목에 이미 있어 기대값을 「결정 없는 문자열」로 바로잡음 |
| v4 | lexicon · 볼 | F-A 볼 뒤 막기 — 리포트 값(`기` 추가)으로 전수 시험하니 볼+한 글자 11,172 중 11,152 가 볼로 감(볼펜 · 볼트 …) → 코 · 목 꼴 앞보기 목록(끝 · 공백 · 기호 · 조사)으로 바꿈. 볼기는 볼로 안 감. 원천 셈 그대로 |
| v4 | lexicon · 힙 | F-A 힙 항목에 `볼기(?:부위)?`(KMA gluteal region = 볼기부위) — 지금 원천 0 |
| v4 | lexicon · residual | F-B 형태소 한글 100→171 · 영문 어간 86→165 를 표준 목록(TA2 Part 1 · KMA 의학용어 6.1판)과 상담 구어에서 채움 · 유두는 패턴 `(?<!모)유두(?!진피)` · 영문 어간 단어 안 매칭 · 악센트 접기(NFKD). 새로 드러난 소음 28낱말 허용(무리 1개) |
| v4 | supraorbital · 혈관 · 신경 이름 | F-B 단어 안 매칭으로 드러남(artery 생략 축약 4회) → supraorbitalartery 와 같은 행선지(deferred 위험 부위 속성). 사전 혈관 항목에 `\b[Ss]upra(?:orbital|trochlear)\b` |
| v4 | supratrochlear · 혈관 · 신경 이름 | 위와 같음(5회) |
| v4 | tragus · 해부 지표(뼈 · 선 · 구조) | F-B 표준 목록(TA2 111)으로 드러남 — 「이주(tragus)」 2회 → 이주와 같은 행선지 |
| v4 | submandibularsalivarygland · 해부 지표(뼈 · 선 · 구조) | F-B — 「submandibular salivary gland」 1회 → 침샘과 같은 행선지. v3 까지 「mandibular」 조각이 하악(노드)으로 잘못 갔다(하악 항목 `[Mm]andib…` 에 단어 앞 막기 없음) — 결정 [mandibular, 하악] 지움 |
| v4 | 복부라인 · ‹부위›라인 | W-C ‹부위›라인 일반 패턴으로 드러남(2회) — v3 까지 「라인」이 떨어진 채 복부 행에 섞임 → W7 규칙대로 복부 + 라인(D-07) |
| v4 | 이마라인 · ‹부위›라인 | 위와 같음(1회) — 이마 + 라인(D-07) |
| v4 | 콧등라인 · ‹부위›라인 | 위와 같음(1회) — 콧등 + 라인(D-07) |
| v4 | lexicon · 등 허용 | W-C 나열 「등」 허용에 앞 조건 — 앞 낱말이 노드 이름 · 노드로 가는 결정 문자열(+과/와)이고 나열 끝(앞에 , · / 、 ( )이 아니면 허용 안 함. 지금 원천 43회 중 42회는 나열 끝, 1회(「입술 등 점막 인접 부위」)는 residual_reviewed 한 줄로 닫음 |
| v4 | lexicon · fixture | 고정 시험 38→88: v3 §1 문장 26 · F-A 5 + 전수 1(11낱말 × 11,172자, step3-boundary-test.py) · F-B 13 · W-C 5. 첫 판 87/88 — FB-gluteal 기대값을 잘못 적음(결정 없는 문자열이 맞음) |
| v5 | scope · name_fields | 범위 바로잡기 — 부위 원천을 이름 칸 17(name_fields)로. 설명 문장 칸에만 나오던 문자열 350행은 strings_out_of_scope 로(셈 밖 · 기록만). 입가 = 묶음 자리 예외. B11 입가 줄 철회(withdrawn_v5) |
| v5 | nodes · anatomical_name | 추가 지시 7 — 전문의 용어를 겉자리 이름만으로: 사각턱(깨물근 · 아래턱뼈각 → TA2 214 · 약) · 목(넓은목근 → 앞목 · 약) · 승모근(등세모근 → 목덜미부위 · 어깨 · 약) · 종아리(장딴지근 → 장딴지 · 약) · 턱선(아래턱뼈 아래모서리 → Jawline · 표준 체표 이름 없음 · 중). 근육 · 뼈 이름은 handoff_note(4단계). 이전 값은 anatomical_before_v5 |
| v5 | 코조각주사 · 코조각주사 | v5 검수 F-1 — 허용 목록(성분 · 제품 이름)에서 빼고 사전 코조각주사 · 결정 코 + 조각주사(D-07 → 2단계 계열) |

## 노드

| id | 일반인 용어(노드 이름) | 상위 | 상태 | 동의어(등장) | 부위+다른 축 → 넘김 | 전문의 용어 — 겉자리 이름(수준) | 위험 부위 | 이름 칸 근거(문자열 · 등장) |
|---|---|---|---|---|---|---|---|---|
| `site.face` | 얼굴 | — | DEC-002 트리 | 안면(2) · 얼굴(9) · 페이스(1) | 안면홍조(4) → 홍조 → 7단계 고민 · Facial Contouring(1) → 윤곽 → 7단계 고민 · 얼굴윤곽(4) → 윤곽 → 7단계 고민 | Face (facies) · 얼굴 (**강**) | — | 6 · 21 |
| `site.forehead-group` | 이마(묶음) | 얼굴 | DEC-002 트리 | 이마/관자놀이(3) | — | Frontal region (regio frontalis) · 이마부위 (**약**) | `forehead` 하위 이마가 소유 | 1 · 3 |
| `site.forehead` | 이마 | 이마(묶음) | DEC-002 트리 | forehead(2) · 이마(2) | 이마 볼륨(1) → 볼륨 → 7단계 고민 · 이마 주름(4) → 주름 → 7단계 고민 · 이마지방이식(3) → 지방이식 → 2단계 계열 · 이마필러(2) → 필러 → 2단계 계열 | Forehead (frons) · 이마 (**강**) | `forehead` 같음 | 6 · 14 |
| `site.glabella` | 미간 | 이마(묶음) | DEC-002 트리 | glabella(2) · 미간(2) | 미간 주름(4) → 주름 → 7단계 고민 | Glabella · 미간 (**강**) | `glabella` 같음 | 3 · 8 |
| `site.temple` | 관자놀이 | 얼굴 | DEC-002 트리 | 관자놀이(3) · 볼/관자놀이(3) · 이마/관자놀이(3) · temple(2) | 관자놀이충전(2) → 충전 → 6단계 목적 | Temple / temporal region (regio temporalis) · 관자부위 (**강**) | `temple` 같음 | 5 · 13 |
| `site.periorbital-group` | 눈가(묶음) | 얼굴 | DEC-002 트리 | periorbital(2) · 눈 주변(1) | 눈가 쳐짐(2) → 쳐짐 → 7단계 고민 | Periorbital region (regio orbitalis) · 눈확부위 (**강**) | `periorbital` 묶음(하위 셋 다 덮음) 추천 | 3 · 5 |
| `site.lateral-canthus` | 눈가 | 눈가(묶음) | DEC-002 트리 | 눈가(7) | 까마귀발 주름(2) → 주름 → 7단계 고민 · 눈가보톡스(2) → 보톡스 → 2단계 계열 · 눈가 주름(5) → 주름 → 7단계 고민 | Lateral canthal area (crow's feet) · 가쪽눈구석 주변 (**약**) | `periorbital` 상위 묶음 zone | 4 · 16 |
| `site.infraorbital` | 눈밑 | 눈가(묶음) | DEC-002 트리 | 눈밑(1) | 눈밑꺼짐(3) → 꺼짐 · 주름 · 볼륨 → 7단계 고민 · 눈밑 볼륨(2) → 꺼짐 · 주름 · 볼륨 → 7단계 고민 · 다크서클필러(2) → 다크서클 → 7단계 고민 / 필러 → 2단계 계열 · 애교필러(2) → 필러 → 2단계 계열 | Infraorbital region · tear trough · 눈확아래부위 · 눈물고랑 (**강**) | `periorbital` 상위 묶음 zone | 5 · 10 |
| `site.eyelid` | 눈꺼풀 | 눈가(묶음) | DEC-002 트리 | — | 눈꺼풀 처짐(1) → 처짐 → 7단계 고민 · 눈꺼풀쳐짐(2) → 처짐 → 7단계 고민 · 아이라인반영구(2) → 반영구 → 2단계 계열 | Eyelid (palpebra) · 눈꺼풀 (**강**) | `periorbital` 상위 묶음 zone | 3 · 5 |
| `site.nose-group` | 코(묶음) | 얼굴 | DEC-002 트리 | nose(2) | — | Nose (nasus) · 코 (**강**) | `nose` 묶음(코끝 · 콧등 · 콧망울 포함) 추천 | 1 · 2 |
| `site.nose` | 코 | 코(묶음) | DEC-002 트리 | 코(4) | 코 라인(1) → 라인 → 7단계 고민 · 코실리프팅(3) → 실리프팅 → 2단계 계열 · 코조각주사(1) → 조각주사 → 2단계 계열(지방분해 주사) · 코필러(3) → 필러 → 2단계 계열 | External nose · 바깥코 (**약**) | `nose` 상위 묶음 zone | 5 · 12 |
| `site.nasal-tip` | 코끝 | 코(묶음) | DEC-002 트리 | 코끝(5) | — | Tip of nose (apex nasi) · columella · 코끝 (**강**) | `nose` 상위 묶음 zone | 1 · 5 |
| `site.nasal-dorsum` | 콧등 | 코(묶음) | OQ-206 추가 | 콧대(2) · 콧등(1) | — | Dorsum of nose (dorsum nasi) · 콧등 (**강**) | `nose` 상위 묶음 zone | 2 · 3 |
| `site.cheek-group` | 볼(묶음) | 얼굴 | DEC-002 트리 | cheek(1) · Cheek (Malar/Buccal)(1) · 볼/관자놀이(3) · 볼/광대(3) | — | Cheek (Malar/Buccal) · 볼 (**강**) | `cheek` 묶음 추천(Malar=광대 · Buccal=볼 둘 다) | 4 · 8 |
| `site.cheek` | 볼 | 볼(묶음) | DEC-002 트리 | 볼(1) | 볼 볼륨 (1) → 볼륨 · 충전 → 7단계 고민 · 볼볼륨충전(2) → 볼륨 · 충전 → 7단계 고민 · 볼살(1) → 살(지방) → 7단계 고민 · 볼지방이식(3) → 지방이식 → 2단계 계열 · 볼쳐짐(2) → 처짐 → 7단계 고민 · 볼필러(2) → 필러 → 2단계 계열 | Buccal region (regio buccalis) · 볼부위 (**강**) | `cheek` 상위 묶음 zone | 7 · 12 |
| `site.zygoma` | 광대 | 볼(묶음) | DEC-002 트리 | 광대(3) | 광대축소주사(2) → 축소 → 6단계 목적 / 주사 → 2단계 계열 | Zygomatic (malar) region (regio zygomatica) · 광대부위 (**강**) | `cheek` 상위 묶음 zone | 2 · 5 |
| `site.perioral` | 입가 | 얼굴 | DEC-002 트리 | — | — | Perioral region (regio oralis) · 입부위 (**강**) | `lips` 관련(입가 주름은 lips zone 이 다룸) | 0 · 0 — 예외: 묶음 자리 — 이름 칸 근거 0. DEC-002 「원천 근거 없음」은 이름 칸 기준으로 맞다. 하위(팔자 · 입술 · 입꼬리 · 잇몸 · 마리오네트 · 인중)가 이름 칸 근거를 가진다(브리프 예외) |
| `site.nasolabial` | 팔자 | 입가 | DEC-002 트리 | nasolabial(1) · Nasolabial Fold(1) | 팔자주름(4) → 주름 → 7단계 고민 | Nasolabial fold (sulcus nasolabialis) · 코입술고랑 (**강**) | `nasolabial` 같음(고민 「주름」 뗌 — D-07) | 3 · 6 |
| `site.lips` | 입술 | 입가 | DEC-002 트리 | lips(2) · 입술(3) | 입술 볼륨(1) → 볼륨 · 확대 · 라인 → 7단계 고민 · 입술반영구(2) → 반영구 → 2단계 계열 · 입술필러(2) → 필러 → 2단계 계열 | Lips (labia oris) · 입술 (**강**) | `lips` 같음 | 5 · 10 |
| `site.mouth-corner` | 입꼬리 | 입가 | DEC-002 트리 | 입꼬리(1) | — | Angle of mouth / oral commissure (angulus oris) · 입꼬리 (**강**) | `lips` 관련(구각 · 상순동맥 유입) | 1 · 1 |
| `site.gingiva` | 잇몸 | 입가 | DEC-002 트리 | — | 잇몸미소(1) → 잇몸 노출 미소 → 7단계 고민 | Gingiva (gummy smile 부위) · 잇몸 (**약**) | 위험 부위 원장 없음 | 1 · 1 |
| `site.chin-group` | 턱(묶음) | 얼굴 | DEC-002 트리 | 턱(1) · 턱/턱선(4) · ⚠하관(1) | 턱보톡스(2) → 보톡스 → 2단계 계열 · 턱필러(2) → 필러 → 2단계 계열 | Mandibular region (lower jaw) · 아래턱부위 (**약**) | 하위 턱끝 · 턱선이 각 zone 소유 | 5 · 10 |
| `site.chin` | 턱끝 | 턱(묶음) | DEC-002 트리 | chin(1) · Chin (Mentum)(1) | 자갈턱(1) → 자갈턱 → 7단계 고민 · 턱 끝 볼륨(1) → 볼륨 · 연장 → 7단계 고민 · 턱끝 연장(2) → 볼륨 · 연장 → 7단계 고민 · 턱 끝 지방이식(1) → 필러 · 지방이식 → 2단계 계열 | Chin (mentum) · mental region (regio mentalis) · 턱끝부위 (**강**) | `chin` 턱끝 추천 | 6 · 7 |
| `site.jawline` | 턱선 | 턱(묶음) | DEC-002 트리 | 턱라인(2) · jawline(1) · Jawline (Mandibular border)(1) · 턱선(4) | 네페르티티(1) → 네페르티티 리프트 → 4단계 기법 · 네페르티티 리프트(1) → 네페르티티 리프트 → 4단계 기법 · ⚠불독살(2) → 처짐 · 살 → 7단계 고민 · 턱선무너짐(2) → 처짐 → 7단계 고민 · 턱선보톡스(1) → 보톡스 → 2단계 계열 · 턱선실리프팅(2) → 실리프팅 → 2단계 계열 | Jawline · (표준 체표 이름 없음 — 상담 용어 「턱선」) (**중**) | `jawline` 같음 | 10 · 17 |
| `site.masseter` | 사각턱 | 턱(묶음) | DEC-002 트리 | 사각턱(7) | 교근축소(3) → 축소 → 6단계 목적 · 사각턱보톡스(2) → 보톡스 → 2단계 계열 | Parotideomasseteric region (regio parotideomasseterica) · (KMA 표제어 없음 — TA2 이름만) (**약**) | `jawline` 관련(교근 보톡스 경고가 cheek · jawline 두 zone 에) | 3 · 12 |
| `site.submental` | 턱밑 | 턱(묶음) | DEC-002 트리 | 턱밑지방(1) · 턱밑(7) | 이중턱(13) → 이중턱(지방) → 7단계 고민 | Submental region (regio submentalis) · 턱끝밑부위 (**약**) | 위험 부위 원장 없음 | 3 · 21 |
| `site.full-face` | 얼굴 전체 | 얼굴 | DEC-002 트리 | 얼굴 전체(1) · 전체얼굴(23) · 풀페이스(7) | 페이스앤넥큐레이션(1) → 큐레이션 → 6단계 패키지 · 풀페이스큐레이션(1) → 큐레이션 → 6단계 패키지 | Whole face · 얼굴 전체 (**약**) | 하위 zone 11곳 전부 해당 | 5 · 33 |
| `site.neck-group` | 목(묶음) | — | DEC-002 트리 | neck(2) | — | Neck (collum) · 목 (**강**) | `neck` 묶음 추천 | 1 · 2 |
| `site.neck` | 목 | 목(묶음) | DEC-002 트리 | 목(2) | 네페르티티(1) → 네페르티티 리프트 → 4단계 기법 · 네페르티티 리프트(1) → 네페르티티 리프트 → 4단계 기법 · 넥큐레이션(1) → 큐레이션 → 6단계 패키지 · 초음파목(1) → 초음파 → 2단계 계열 · 목 실리프팅(1) → 리프팅 → 6단계 목적 · 목주름(6) → 주름 · 밴드 → 7단계 고민 · 페이스앤넥큐레이션(1) → 큐레이션 → 6단계 패키지 | Anterior region of neck (regio cervicalis anterior) · 목 앞부위(앞목) — 경부 (**약**) | `neck` 상위 묶음 zone | 8 · 14 |
| `site.trapezius` | 승모근 | 목(묶음) | DEC-002 트리 | 승모근(5) · 어깨라인(3) | 승모근보톡스(2) → 보톡스 → 2단계 계열 | Posterior region of neck (regio cervicalis posterior · nucha) · shoulder (omos) · 목덜미부위 · 어깨 (**약**) | `neck` 관련(부신경) | 3 · 10 |
| `site.scalp` | 두피 | — | DEC-002 트리 | Scalp(1) · 두피(13) | MTS두피(2) → 시술 이름 → 2단계 계열 · 두피PRP(2) → 시술 이름 → 2단계 계열 · 두피메조(2) → 시술 이름 → 2단계 계열 · 두피스케일링(3) → 시술 이름 → 2단계 계열 · 두피엑소좀(2) → 시술 이름 → 2단계 계열 · 두피주사(1) → 시술 이름 → 2단계 계열 · 두피치료(1) → 시술 이름 → 2단계 계열 · SMP(2) → 반영구 → 2단계 계열 · 헤어라인반영구(2) → 반영구 → 2단계 계열 | Scalp · 머리덮개 (**중**) | 위험 부위 원장 없음 | 11 · 31 |
| `site.body` | 바디 | — | DEC-002 트리 | Body(1) · 바디(9) | EMS 바디(2) → EMS → 2단계 계열 · 바디리프팅(2) → 라인 · 리프팅 · 탄력 → 7단계 고민 · 바디 쳐짐(2) → 라인 · 리프팅 · 탄력 → 7단계 고민 · 바디탄력(3) → 라인 · 리프팅 · 탄력 → 7단계 고민 · 바디(여성)(3) → 여성 → 대상 속성(성별 · 6단계) · 바디큐레이션(1) → 큐레이션 → 6단계 패키지 | Body (trunk · limbs) · 몸통 · 팔다리 (**약**) | 위험 부위 원장 없음 | 8 · 23 |
| `site.axilla` | 겨드랑이 | 바디 | DEC-002 트리 | 겨드랑이(6) | — | Axilla (regio axillaris) · 겨드랑부위 (**약**) | 위험 부위 원장 없음 | 1 · 6 |
| `site.upper-arm` | 팔뚝 | 바디 | DEC-002 트리 | ⚠팔뚝(4) | — | Posterior upper arm (regio brachii posterior) · 위팔 뒤부위 (**약**) | 위험 부위 원장 없음 | 1 · 4 |
| `site.abdomen` | 복부 | 바디 | DEC-002 트리 | 복부(7) | ⚠임신선(2) → 튼살(임신선) → 7단계 고민 | Abdomen (regio abdominalis) · 배부위 (**중**) | 위험 부위 원장 없음 | 2 · 9 |
| `site.thigh` | 허벅지 | 바디 | DEC-002 트리 | 허벅지(3) | 허벅지 안쪽(1) → 안쪽(위치 수식) → 1단계 규격 · 단위 | Thigh (regio femoris) · 넙다리부위 (**약**) | 위험 부위 원장 없음 | 2 · 4 |
| `site.calf` | 종아리 | 바디 | DEC-002 트리 | 종아리(2) | — | Calf (sura) · sural region (regio surae) · 장딴지(종아리) (**약**) | 위험 부위 원장 없음 | 1 · 2 |
| `site.whole-body` | 전신 | 바디 | DEC-002 트리 | 전신(1) | — | Whole body surface · 온몸 피부 (**약**) | 위험 부위 원장 없음 | 1 · 1 |
| `site.hand` | 손 | 바디 | OQ-206 추가 | 손(3) | — | Hand (manus) · 손 (**약**) | 위험 부위 원장 없음 | 1 · 3 |
| `site.foot` | 발 | 바디 | OQ-206 추가 | 발(3) | — | Foot (pes) · 발 (**약**) | 위험 부위 원장 없음 | 1 · 3 |
| `site.leg` | 다리 | 바디 | OQ-206 추가 | 다리(2) | 하지정맥류(1) → 정맥류 → 7단계 고민 | Lower limb (membrum inferius) · 다리 · 하지 (**중**) | 위험 부위 원장 없음 | 2 · 3 |
| `site.bikini` | 비키니 | 바디 | OQ-206 추가 | 비키니(2) | — | Inguinal · pubic region (regio inguinalis · regio pubica) · 샅굴부위 · 두덩부위 (**약**) | 위험 부위 원장 없음 | 1 · 2 |
| `site.buttock` | 힙 | 바디 | OQ-206 추가 | 힙(2) | — | Gluteal region (regio glutealis) · 볼기부위 (**약**) | 위험 부위 원장 없음 | 1 · 2 |
| `site.back` | 등 | 바디 | 3단계 추가 | 등(3) · 브라라인(1) | 등살주사(1) → 살(지방) → 7단계 고민 | Back (dorsum · regiones dorsi) · 등부위 (**약**) | 위험 부위 원장 없음 | 3 · 5 |
| `site.flank` | 옆구리 | 바디 | 3단계 추가 | 러브핸들(2) · 옆구리(1) | — | Flank (regio lateralis abdominis) · 옆구리 (**약**) | 위험 부위 원장 없음 | 2 · 3 |
| `site.nasal-ala` | 콧망울 | 코(묶음) | 3단계 추가 | 콧망울(1) | — | Ala of nose (ala nasi) · 콧방울 (**강**) | `nose` 상위 묶음 zone(비익 괴사 · 함몰 별도 경고) | 1 · 1 |
| `site.arm` | 팔 | 바디 | 3단계 추가 | 팔(2) | — | Upper limb (membrum superius) · 팔 (**약**) | 위험 부위 원장 없음 | 1 · 2 |
| `site.chest` | 가슴 | 바디 | 3단계 추가 | 가슴(2) | — | Chest (regio pectoralis) · breast (mamma) · 가슴부위 (**약**) | 위험 부위 원장 없음 | 1 · 2 |
| `site.beard` | 수염 | 얼굴 | 3단계 추가 | 수염(2) | — | Beard area · 수염 자리 (**약**) | 위험 부위 원장 없음 | 1 · 2 |
| `site.sideburn` | 구레나룻 | 얼굴 | 3단계 추가 | 구레나룻(2) | — | Sideburn (preauricular) area · 귀앞 털 자리 (**약**) | 위험 부위 원장 없음 | 1 · 2 |
| `site.philtrum` | 인중 | 입가 | 3단계 추가 | 인중(2) | — | Philtrum · 인중 (**약**) | `lips` 관련(상순 · 상구순) | 1 · 2 |
| `site.eyebrow` | 눈썹 | 눈가(묶음) | 3단계 추가 | — | 눈썹반영구(2) → 반영구 → 2단계 계열 | Eyebrow (supercilium) · 눈썹 (**약**) | `glabella` 관련(forehead · glabella 의 「눈썹 처짐」 경고) | 1 · 2 |
| `site.marionette` | 마리오네트 | 입가 | 3단계 추가 | — | 마리오네트라인(2) → 라인(주름) → 7단계 고민 | Marionette line (labiomandibular fold) · 입꼬리-턱 주름 자리 (**약**) | `lips` 관련(구각 · DAO) | 1 · 2 |

⚠ = 근거 약(B4). 해부학 이름 근거 원문은 json `nodes[].anatomical_name.basis`. 수준 강 = 레포 파일에 그 이름이 있음(위험 부위 파일은 AI 합의본 — 의학 확정 아님) · 중 = 레포 일부 · 약 = 레포 밖 표준 용어집만. 확정은 의료진(OQ-202).

## 전문의 용어에서 뺀 근육 · 뼈 이름 → 4단계 넘김 메모(추가 지시 7)

| 노드 | 이전 전문의 용어 | 지금(겉자리) | 넘김 메모 |
|---|---|---|---|
| 턱선 | 아래턱뼈 아래모서리 · Mandibular border (margo inferior mandibulae) (강) | (표준 체표 이름 없음 — 상담 용어 「턱선」) · Jawline (**중**) | 뼈 지표 아래턱뼈 아래모서리(mandibular border) → 4단계 기법(깊이 · 지표) |
| 사각턱 | 아래턱뼈각 · 깨물근 · Mandibular angle · masseter (angulus mandibulae · m. masseter) (강) | (KMA 표제어 없음 — TA2 이름만) · Parotideomasseteric region (regio parotideomasseterica) (**약**) | 대상 근육 깨물근(masseter) · 뼈 지표 아래턱뼈각(angulus mandibulae) → 4단계 기법(대상 근육) |
| 목 | 앞목부위 · 넓은목근 · Anterior cervical region · platysma (강) | 목 앞부위(앞목) — 경부 · Anterior region of neck (regio cervicalis anterior) (**약**) | 대상 근육 넓은목근(platysma) → 4단계 기법(대상 근육) |
| 승모근 | 등세모근 · Trapezius (m. trapezius) (강) | 목덜미부위 · 어깨 · Posterior region of neck (regio cervicalis posterior · nucha) · shoulder (omos) (**약**) | 대상 근육 등세모근(trapezius) → 4단계 기법(대상 근육) |
| 종아리 | 종아리부위 · 장딴지근 · Calf (regio surae) · gastrocnemius (중) | 장딴지(종아리) · Calf (sura) · sural region (regio surae) (**약**) | 대상 근육 장딴지근(gastrocnemius) → 4단계 기법(대상 근육) |

나머지 48 노드는 겉자리 이름(TA2 regiones · 부분 이름 · 겉 고랑/주름 — 코입술고랑 · 눈물고랑 · 인중)이라 그대로. 턱(묶음) 「아래턱부위 · Mandibular region」은 아래턱(턱 · 하악, KMA jaw)을 몸 부분으로 쓴 것이라 그대로 둠

## 트리 밖 결정이 보낸 문자열

| 이름 | 결정 | 행선지 | 문자열(등장) |
|---|---|---|---|
| 등 | U1 새 노드 | 등 | 등(3) · 등살주사(1) |
| 브라라인 | U1 등 동의어 | 등 | 브라라인(1) |
| 엉덩이 | U1 힙 동의어 | 힙 |  |
| 옆구리 | U1 새 노드 | 옆구리 | 러브핸들(2) · 옆구리(1) |
| 콧망울 | U1 새 노드 | 콧망울 | 콧망울(1) |
| 페이스 | U1 얼굴 동의어 | 얼굴 | 페이스(1) |
| 하관 | U1 턱(묶음) 동의어 | 턱(묶음) | 하관(1) |
| 팔 | U2 새 노드 | 팔 | 팔(2) |
| 가슴 | U2 새 노드 | 가슴 | 가슴(2) |
| 수염 | U2 새 노드 | 수염 | 수염(2) |
| 구레나룻 | U2 새 노드 | 구레나룻 | 구레나룻(2) |
| 인중 | U2 새 노드 | 인중 | 인중(2) |
| 눈썹 | U2 새 노드 | 눈썹 | 눈썹반영구(2) |
| 마리오네트 | U2 새 노드 | 마리오네트 | 마리오네트라인(2) |
| 무릎 | B5 다리 동의어 | 다리 |  |
| 불독살 | B5 턱선 동의어 + 고민 처짐 | 턱선 | 불독살(2) |
| 골반저근 | B6 부위 아님(비미용 적응증) | 계열 밖(비미용) — 부위 노드 없음 |  |
| 관절치료 | B6 부위 아님(비미용 · 계열 밖) | 계열 밖(비미용) — 부위 노드 없음 | 관절치료(1) |

## 단계로 넘김(deferred)

| 단계 | 문자열(등장) |
|---|---|
| 1단계 제품 (8) | 리쥬란 아이(2) · 바디HIFU(2) · 바디써마지(2) · 바디인모드(2) · 엠페이스(2) · 인모드바디(1) · 코안면전문(1) · 튠페이스(1) |
| 7단계 고민 (6) | V라인(5) · 전신항노화(3) · 전체미백(3) · Hair(2) · 모발(1) · 전신재생(1) |
| 4단계 기법 (3) | 진피(6) · 표피(1) · 피하(1) |
| 5단계 단위 시술 경로 (2) | IV(3) · 정맥(2) |
| 계열 밖(비미용) — 부위 노드 없음 (1) | 관절치료(1) |
| 2단계 계열 (1) | 모발이식(3) |
| 사후관리 문구 (1) | 손톱(1) |
| 4단계 대상 근육 (1) | 표정근(1) |

## 경계 규칙(B8 · W7)

| 경계 | 원천 문자열이 가는 곳 |
|---|---|
| 이름이 같은 묶음 · 좁은 노드(이마 · 눈가 · 코 · 볼 · 목 + 턱(묶음)) | 원천 문자열 「이마 · 눈가 · 코 · 볼 · 목」은 좁은 노드로. 묶음 노드는 동의어를 갖지 않고 (가) 고민 라벨처럼 하위 이름을 나란히 묶은 칸(「이마/관자놀이」 · 「볼/광대」 · 「턱/턱선」 · 「눈가 쳐짐」) (나) 위험 부위 zone 이름(periorbital · nose · cheek · neck) (다) 그 부위 해부 묶음 이름(Periorbital · Nose · Cheek · Neck · 경부 · 하악 · 하관)만 받는다 |
| 「턱」 | 턱 단독 · 턱필러 · 턱보톡스 → 턱(묶음). 원천 detail 이 「턱끝 연장」 · 「사각턱 축소」로 하위를 정해 주면 단위 시술(5단계)에서 하위로 내린다 |
| 얼굴 ↔ 얼굴 전체 | 얼굴 · 안면 · face · 페이스 → 얼굴(최상위 묶음). 전체얼굴 · 얼굴 전체 · 안면 전체 · 전안면 · 풀페이스 → 얼굴 전체. 시장가 「(전체얼굴)」 · 「(풀페이스)」는 모두 얼굴 전체 |
| 바디 ↔ 전신 | 바디 · 탄탄한 몸 · 몸매 · 신체 처짐 → 바디(묶음). 전신은 「레이저 제모 (전신)」 · 「팔뚝, 복부 등 전신 처짐」 2곳만 노드 「전신」(몸 표면). 그 밖 「전신」 28회 + 전신항노화 · 전신재생 · 전신발진 등은 계통 → 부위 아님(수액은 「해당 없음」) |
| 「(묶음)」 이름 | v3 트리 이름 그대로(이마(묶음) · 눈가(묶음) · 코(묶음) · 볼(묶음) · 턱(묶음) · 목(묶음)). 입가는 v3 이름 「입가」 그대로 — 좁은 「입가」 노드가 없어 원천 「입가 · 입 주변 · perioral · 구주위」가 바로 이 노드로 간다 |
| 「‹부위›라인」(W7) | ‹부위›라인 = 부위 + 고민 「라인」(7단계). 예외: 턱라인(= 턱선 · 하악연 해부명) · 어깨라인(승모근 동의어 — DEC-002 D-03). 허리라인은 옆구리 + 라인(근거 약) |

## 위험 부위 대응(B9 — 최종 의료진)

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

## 의료진 질문 35

| 종류 | 문자열 · 노드 | 둔 값 | 질문 |
|---|---|---|---|
| 근거 약 문자열(B4) | 임신선 | 복부 | 「임신선」 를 복부 에 둔다 — 맞나 |
| 근거 약 문자열(B4) | 불독살 | 턱선 | 「불독살」 를 턱선 에 둔다 — 맞나 |
| 근거 약 문자열(B4) | 팔뚝 | 팔뚝 | 「팔뚝」 를 팔뚝 에 둔다 — 맞나 |
| 근거 약 문자열(B4) | 하관 | 턱(묶음) | 「하관」 를 턱(묶음) 에 둔다 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 이마(묶음) | Frontal region (regio frontalis) · 이마부위 | 「이마(묶음)」 의 해부학 이름을 Frontal region (regio frontalis) · 이마부위 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 눈가 | Lateral canthal area (crow's feet) · 가쪽눈구석 주변 | 「눈가」 의 해부학 이름을 Lateral canthal area (crow's feet) · 가쪽눈구석 주변 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 코 | External nose · 바깥코 | 「코」 의 해부학 이름을 External nose · 바깥코 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 잇몸 | Gingiva (gummy smile 부위) · 잇몸 | 「잇몸」 의 해부학 이름을 Gingiva (gummy smile 부위) · 잇몸 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 턱(묶음) | Mandibular region (lower jaw) · 아래턱부위 | 「턱(묶음)」 의 해부학 이름을 Mandibular region (lower jaw) · 아래턱부위 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 사각턱 | Parotideomasseteric region (regio parotideomasseterica) · (KMA 표제어 없음 — TA2 이름만) | 「사각턱」 의 해부학 이름을 Parotideomasseteric region (regio parotideomasseterica) · (KMA 표제어 없음 — TA2 이름만) 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 턱밑 | Submental region (regio submentalis) · 턱끝밑부위 | 「턱밑」 의 해부학 이름을 Submental region (regio submentalis) · 턱끝밑부위 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 얼굴 전체 | Whole face · 얼굴 전체 | 「얼굴 전체」 의 해부학 이름을 Whole face · 얼굴 전체 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 목 | Anterior region of neck (regio cervicalis anterior) · 목 앞부위(앞목) — 경부 | 「목」 의 해부학 이름을 Anterior region of neck (regio cervicalis anterior) · 목 앞부위(앞목) — 경부 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 승모근 | Posterior region of neck (regio cervicalis posterior · nucha) · shoulder (omos) · 목덜미부위 · 어깨 | 「승모근」 의 해부학 이름을 Posterior region of neck (regio cervicalis posterior · nucha) · shoulder (omos) · 목덜미부위 · 어깨 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 바디 | Body (trunk · limbs) · 몸통 · 팔다리 | 「바디」 의 해부학 이름을 Body (trunk · limbs) · 몸통 · 팔다리 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 겨드랑이 | Axilla (regio axillaris) · 겨드랑부위 | 「겨드랑이」 의 해부학 이름을 Axilla (regio axillaris) · 겨드랑부위 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 팔뚝 | Posterior upper arm (regio brachii posterior) · 위팔 뒤부위 | 「팔뚝」 의 해부학 이름을 Posterior upper arm (regio brachii posterior) · 위팔 뒤부위 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 허벅지 | Thigh (regio femoris) · 넙다리부위 | 「허벅지」 의 해부학 이름을 Thigh (regio femoris) · 넙다리부위 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 종아리 | Calf (sura) · sural region (regio surae) · 장딴지(종아리) | 「종아리」 의 해부학 이름을 Calf (sura) · sural region (regio surae) · 장딴지(종아리) 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 전신 | Whole body surface · 온몸 피부 | 「전신」 의 해부학 이름을 Whole body surface · 온몸 피부 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 손 | Hand (manus) · 손 | 「손」 의 해부학 이름을 Hand (manus) · 손 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 발 | Foot (pes) · 발 | 「발」 의 해부학 이름을 Foot (pes) · 발 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 비키니 | Inguinal · pubic region (regio inguinalis · regio pubica) · 샅굴부위 · 두덩부위 | 「비키니」 의 해부학 이름을 Inguinal · pubic region (regio inguinalis · regio pubica) · 샅굴부위 · 두덩부위 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 힙 | Gluteal region (regio glutealis) · 볼기부위 | 「힙」 의 해부학 이름을 Gluteal region (regio glutealis) · 볼기부위 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 등 | Back (dorsum · regiones dorsi) · 등부위 | 「등」 의 해부학 이름을 Back (dorsum · regiones dorsi) · 등부위 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 옆구리 | Flank (regio lateralis abdominis) · 옆구리 | 「옆구리」 의 해부학 이름을 Flank (regio lateralis abdominis) · 옆구리 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 팔 | Upper limb (membrum superius) · 팔 | 「팔」 의 해부학 이름을 Upper limb (membrum superius) · 팔 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 가슴 | Chest (regio pectoralis) · breast (mamma) · 가슴부위 | 「가슴」 의 해부학 이름을 Chest (regio pectoralis) · breast (mamma) · 가슴부위 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 수염 | Beard area · 수염 자리 | 「수염」 의 해부학 이름을 Beard area · 수염 자리 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 구레나룻 | Sideburn (preauricular) area · 귀앞 털 자리 | 「구레나룻」 의 해부학 이름을 Sideburn (preauricular) area · 귀앞 털 자리 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 인중 | Philtrum · 인중 | 「인중」 의 해부학 이름을 Philtrum · 인중 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 눈썹 | Eyebrow (supercilium) · 눈썹 | 「눈썹」 의 해부학 이름을 Eyebrow (supercilium) · 눈썹 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 해부학 이름 — 근거 약(W5) | 마리오네트 | Marionette line (labiomandibular fold) · 입꼬리-턱 주름 자리 | 「마리오네트」 의 해부학 이름을 Marionette line (labiomandibular fold) · 입꼬리-턱 주름 자리 로 둔다 — 근거는 표준 용어집만 — 맞나 |
| 위험 부위 대응(B9) | 위험 부위 대응 5줄 | 위험 부위 표 | periorbital · nose · cheek · neck 를 묶음에, chin 을 턱끝에 대는 게 맞나(OQ-202) |
| 해부학 이름(B10) | 해부학 이름 후보 강 · 중 | 노드 표 | 수준 강 · 중 후보 영문 · 한글을 확정(OQ-202) |

## 고정 시험(fixture) — 6/6 통과

`python3 step3-fixture-test.py` — 원천 사본에 문장 파일 하나씩 붙이거나 결정 한 줄을 빼고 돌려 open 이 기대와 같은지 본다. 사례 `step3-fixtures/cases.json`.

| 사례 | 종류 | 넣은 것 | 기대 open | 실제 open | 결과 |
|---|---|---|---|---|---|
| BASE | baseline | 원천 그대로 | 없음 | 없음 | PASS |
| T2 | remove_decision | 결정에서 ['하관', '하관'] 뺌 | 결정없음:하관|하관 · 트리밖행선지없음:하관 | 결정없음:하관|하관 · 트리밖행선지없음:하관 | PASS |
| N-이마 | remove_decision | 결정에서 ['이마', '이마'] 뺌 | 결정없음:이마|이마 | 결정없음:이마|이마 | PASS |
| N-forehead | remove_decision | 결정에서 ['forehead', 'forehead'] 뺌 | 결정없음:forehead|forehead | 결정없음:forehead|forehead | PASS |
| N-코필러 | remove_decision | 결정에서 ['코필러', '코필러'] 뺌 | 결정없음:코필러|코필러 | 결정없음:코필러|코필러 | PASS |
| N-사각턱 | remove_decision | 결정에서 ['사각턱', '사각턱'] 뺌 | 결정없음:사각턱|사각턱 | 결정없음:사각턱|사각턱 | PASS |

## 알려진 한계 — 사람이 찾는 몫

이 원장이 기계로 보장하는 것은 **이름 칸 · 사전 · 잔여 형태소 · 허용 목록 안**에서다. 아래는 open 으로 나오지 않을 수 있어 새 원천 때 사람이 본다.

- **이름 칸 밖의 부위 표현** — 설명 문장 칸(작용기전 · 적응증 설명 · 부작용 · 문헌 · 안전 본문 · 사후관리)은 세지 않는다(기준). 새 원천에서 이름 칸이 늘거나(새 파일 · 새 키) 부위가 설명 칸에만 적힌 시술이 생기면 `step3-decisions.json` name_fields 에 칸을 더해야 잡힌다.
- **사전 · 잔여 형태소 밖 신조어 · 구어** — 이름 칸 안이라도 사전 패턴 · 잔여 형태소와 글자가 겹치지 않으면 조용히 빠진다.
- **같은 표면 다른 뜻** — 행선지는 키(정규형 · 사전 무리) 단위라 같은 글자는 같은 곳으로 간다.

## open 0

없음.

## 잔여 검사 허용 목록

사전 밖 부위 형태소 171(한글) · 패턴 1 · 165(영문 어간)로 **이름 칸만** 다시 훑는다. 아래는 글자만 겹치는 낱말(허용 · 421개) — 무리별 이유는 `step3-lexicon.json` residual.allowed.

- **「입」 글자 겹침 — 주입 · 삽입 · 흡입 · 입자 · 수입 · 「…입니다」 · 입문 · 입체 · 입모근(모낭 근육)** (150)
- **「…하지」 동사 어미** (32)
- **「발」 글자 겹침 — 발현 · 발열 · 유발 · 재발 · 발한 · 개발 · 성분 이름** (66)
- **나열 「…등」 · 중등도 · 균등 — 부위 「등」은 사전 문맥 패턴이 잡음(8회)** (9)
- **사마귀 · 복귀 · 희귀** (6)
- **성분 · 제품 이름(알코올 · 코직산 · 코엔자임 · 피코 · 코팅 …)** (28)
- **배양 · 배출 · 배치 · 「N배」(배수)** (44)
- **손실 · 결손 · 손잡이** (11)
- **성분 · 제품 · 일반어 겹침(아목시실린 · 아다팔렌 · 세팔렉신 · 팔로마 · 트라넥삼산 · 라이넥 · 바넥스 · 협진 · 위협 · 주경부터 · 볼록함 · 에볼루션 · 토브라마이신 · 브라이트닝 · 헤어맥스 · 헤어셀 · 「헤어 제품」 · 「몸에 부담」)** (32)
- **영문 겹침 — 근육 몸통 「body 내」 · temporary · Legacy · Lipko · lipids · lipoic · LIPO · brace · breastfeeding** (13)
- **v3 새 형태소의 겹침 — 후두근(인두 · 후두 근육, 합병증 문맥) · 쥐젖(병변) · 젖산(성분)** (3)
- **영문 어간이 단어 안에서 겹침(v4 F-B 단어 안 매칭) — 일반 영단어 · 학술지 · URL · 저자 이름 · 제품 이름(research · appearance · surface · balance · Digital · onlinelibrary · Valanciene · HArmonyCa · EMFACE · Cryolipolysis …)** (27)
- **v4 표준 목록 한글 형태소의 겹침 — 제품 이름** (1)

사람이 문맥을 보고 닫은 잔여(`step3-decisions.json` residual_reviewed) 0: 없음
