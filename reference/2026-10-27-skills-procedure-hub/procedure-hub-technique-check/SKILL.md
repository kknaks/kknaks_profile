---
name: procedure-hub-technique-check
description: 새 원천 · 새 계열 · 새 장비가 들어와 기법 표현이 생기거나, 기법 노드 · 층 · 대상 근육 · 펄스 같은 속성을 바꿀 때 Procedure Hub 실버 기법 원장(step4-techniques)을 갱신한다. 지도(source-map)가 4단계로 정한 칸인가 → 큰 기법(계열 정의 동사 · mechanism 태그) → 세부 노드(부위 쪼개기 규칙 D-05) / 단위 시술 속성(층 · 대상 근육 · 도구 형태) / 장비 속성(펄스 · 박피 · 가능 방식) / 넘김(다른 단계) 순으로 판정하고, 4단계 규칙(노드 2층 · 층 · 근육은 키 밖 · 펄스는 장비가 낸다 · 원문의 「또는」을 줄이지 않는다 · 다음 단계가 읽을 값은 칸으로 · 끝 조건 = 지금 원천 기준)대로 결정 파일 한 줄만 고친 뒤 step4-apply.py 로 결정론 반영한다. 트리거 예 — 「새 장비 기법 붙여 줘」「step4-apply 가 open 을 냈어」「이건 기법이야 속성이야」「층 값 하나 추가」「대상 근육 바꿔」「펄스 방식 어디에 둬」「step4-techniques 갱신」「기법 원장 점검」.
---

# Procedure Hub 기법 판정 · 실버 기법 원장 갱신

실버 4단계(기법 노드 · 원천 기법 표현 → 노드 · 속성 · 넘김, 2026-10-28)에서 실제로 한 방법을 옮긴 것이다. 새로 지어낸 절차가 아니다.
3단계(부위 — `procedure-hub-site-check`) 다음 단계다. 시술 = 「무엇을(계열) × 어디에(부위) × **어떻게(기법)**」의 셋째 칸이다.

- 정본 원장: `orchestration/work/phub-recommend/step4-techniques.json` · `.md`(노드 24 · 표현 181행 · 계열 기본 18 · 넘겨받은 것 15 · open 0)
- 결정(사람이 고치는 곳): `step4-decisions.json` — 노드 · 값 사전 · 표현 행선지 · 부위 층 나눔 · 넘겨받은 것 · technique_hint · 매질별 펄스 · 계열 기본 · 초안 대응 · 충돌 · 수정 목록
- 결정론 반영: `step4-apply.py`(입력 = 결정 · `source-map.json` 4단계 칸 · 원천 · `step3-decisions.json` `danger_zone_mapping` · `step3-sites.json` · `step2-families.json` · `procedure-master-v3.json` `techniques` → 출력 `step4-techniques.json` · `.md` · `step4-source-fix.md`) · 가드 시험 `step4-fixture-test.py` + `step4-fixtures/cases.json`(10건 — 「결정 한 줄 빼면 open」만)
- 입력 목록: `source-map.json`(원천 21파일 × 칸 517 행선지 지도) 에서 `destinations[].stage = "4"` 인 **칸 27** — 이 밖의 칸은 4단계가 보지 않는다
- 결정 정본: `orchestration/work/phub-recommend/_RESUME.md` §2 2026-10-28 행들 — 「4단계 기법 조사 반영 — 전부 추천대로」(S1~S12 · J1 · J2) · 「4단계 시작 — 계획 승인」 · 「source-map 승인」 · 「해부학 용어 = 시술 방법 · 작용기전 · 안전 쪽」. 규칙이 바뀌면 거기가 이긴다. 쪼개기 규칙 D-05 · 예시 D-02 는 `DEC-002.md`
- 과정 기록: `para/projects/company/procedure-hub/log/2026-10-28-silver-step4-technique.md`(§3 규칙 · §5 틀린 것) · 검수 `review-step4-report.md`
- 원천: `step4-decisions.json` `source.path`(지금 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26`) — 경로는 프로필 레포 기준

**원장 · 결정 파일은 승인 없이 고치지 않는다.** 판정 → 결정 목록(사람) → 결정 한 줄(승인된 것만) → 반영(스크립트) → 점검 · 검수 고리를 그대로 돈다.

## 1. 언제

| 경우 | 시작점 |
|---|---|
| ① **원천 새 스냅샷**(위험 부위 층 · 근육 · 조직 수치 · related_techniques · mechanism · 세션 순서 꼬리가 늘거나 바뀜) | `scripts/check_techniques.py --source <새 스냅샷>` → `errors[]` 「지도 칸 0줄」(원천 키가 바뀜)부터, 그다음 `open[]` 「결정 없는 표현」만 §2 |
| ② **지도가 바뀜**(`source-map.json` 에 4단계 칸이 더해지거나 빠짐) | 지도 승인이 먼저(사용자). 그 뒤 ① 과 같다 — 새 칸의 줄이 전부 「결정 없는 표현」으로 나온다 |
| ③ **새 계열 · 새 장비**(2단계 계열이 늘거나 · step2 `technique_hint` 행이 늘거나 · 4단계 deferred 가 생김) | `open[]` 「결정 없는 계열 기본 기법」 · 「결정 없는 technique_hint」 · 「넘겨받은 것 행선지 없음」 → §2-3 · §2-4 |
| ④ **3단계가 4단계로 넘김**(조직층 deferred · D-07 기법 축 · 부위 `handoff_note` 근육 · 뼈) | `open[]` 「넘겨받은 것 행선지 없음」 → `handoffs[]` 한 줄(§4). 3단계 쪽을 고친 뒤라면 3단계 open 0 부터 확인 |
| ⑤ **노드 · 속성 바꾸기 요청**(세부 기법 추가 · 층 값 · 대상 근육 · 펄스 · 가능 방식) | 노드는 §2-2 쪼개기 조건부터 — 못 채우면 「안 세움 + 대안(속성 · 5단계 이름)」으로 올린다 |
| ⑥ 정기 점검 · 결정을 고친 뒤 | `scripts/check_techniques.py` 한 번 — errors · open · stale 0 · 원장 ↔ 재추출 일치 |

점검(읽기만 · 표준 라이브러리):

```bash
python3 <스킬>/scripts/check_techniques.py \
  --work orchestration/work/phub-recommend \
  --out <scratchpad>/technique-check.json      # 새 스냅샷은 --source <폴더>
```

`open[]` = 지도 4단계 칸에서 펼쳤는데 결정 없는 표현 · 결정 없는 technique_hint · 계열 기본 · 초안 기법 · 4단계로 넘겼는데 행선지 없는 것 ·
`stale_decisions[]` = 결정은 있는데 원천 · step2 · 초안에 없는 것(지우지 말고 결정 목록에) ·
`errors[]` = 지도 칸 0줄 · 노드 2층 넘음 · 근거 빈칸 · 값 사전 밖 · 행선지 오류 · pulse_scope 가 step2 보조 하위 계열에 없음 · 계열 이름 불일치 · 원장 낡음 · summary · md 셈 불일치.

## 2. 판정 순서

표현 한 줄마다 위에서부터. **앞에서 끝나면 뒤로 가지 않는다.**

### 2-1. 지도가 4단계로 정한 칸인가

- `source-map.json` `fields[]` 중 `destinations[].stage == "4"` 인 칸 27만(`references/record-schema.md` §3 — anatomy-danger-zones 22 · taxonomy 2 · extracted 1 · procedure-profiles 1 · treatment-sequence 1)
- **아니면 4단계가 보지 않는다** — 행도 만들지 않는다. 그 칸이 4단계여야 한다고 보이면 지도 변경을 결정 목록에(사용자 승인 — 지도는 사용자 「추천으로 가자」로 섰다)
- extracted.json `{code}.related_techniques` 줄이 taxonomy `modality[{code}].extracted.related_techniques` 줄과 글자 그대로 같으면 **중복** — taxonomy 행으로 센다(`dedupe`). 한 글자라도 다르면 제 행이다

### 2-2. 기법 노드인가 — 큰 기법 → 세부 기법

1. **큰 기법(K01~K12)** — 2단계 계열 정의(문헌 기준 · 정본)의 **전달 동사** + procedure-profiles `mechanism` 의 **전달 태그**. 새 체계를 짜지 않는다
   - 「주사」「주입」 → K01 주입 · 「실을 피하에 넣어」 → K02 삽입 · 「미세침 … 찔러」 → K03 · 「피부에 조사」 → K04 · 「뚫지 않고 가열」 → K05 · 「전자기 · 전기 자극」 → K06 · 플라즈마 → K07 · 「냉각」 → K08 · 「바르거나」 → K09 · 흡수 보조 → K10 · 기계적 박리 · 클렌징 → K11 · 절단 · 펀치 · 압출 → K12
   - taxonomy `group`(주사/주입 · 시술/기기 · 관리)은 기준이 아니다 — mechanism 과 어긋난다(충돌 X3). 계열 표시 속성(원문)으로만
   - `regenerative` · `ablative` 태그는 기법이 아니다(효과 · 장비 성질) → ablative 는 장비 속성 「박피성 · 비박피성」
2. **세부 기법** — 3단계 부위 쪼개기 규칙(DEC-002 D-05)을 축만 바꿔 그대로: ① **원천이 따로 부른다** ② **가능 시술 · 안전이 달라진다**. 둘 다 아니면 쪼개지 않는다(속성 또는 5단계 이름)
   - 예: treatment-sequence 가 「M8-토닝」「M8-프락셔널」을 레이저 단계 안에서 따로 부른다 → K04a · K04b / M4 정의 「(또는 무바늘 제트 주입)」 → K01c / 원천 항목 서브시전 · 펀치이식 · 면포압출 → K12a~c
   - **2층까지** — 세부 기법 아래 세부 없음(단위 시술 → 기법 하나 `uses_technique` · canonical technique `parent_id`). 상위는 큰 기법이어야 한다(스크립트 가드)
   - 노드마다 근거 칸(`basis`) — 원천 표현 · 계열 기본 · 초안 합침 · 세부 근거 중 하나도 없으면 「근거 없는 노드」
3. 판정 값: `verdict` 「기법 노드」(그 표현이 노드 이름 자체 — 「M8-토닝」) / 「기법 노드 근거」(노드를 받치는 문장 — 「메조보톡스 -- 보톡스를 진피층에 소량 주사」 → K01a) · `bucket` 「노드로」 · `node`

### 2-3. 노드가 아니면 — 단위 시술 속성 / 장비 속성

**키를 가르는가**로 나눈다. 노드는 단위 시술 키(계열 × 하위 계열 × 부위 × 기법)를 가르고, 속성은 가르지 않는다(J1 안 1).

| 무엇 | 어디로 | 칸 | 예 |
|---|---|---|---|
| 층 · 깊이 | **단위 시술 속성**(키 밖) — 부위 × 주입 | `layers` → `safe_layers` + `constraint_text`(원문 제약) | 「골막상층 (supraperiosteal) — 혈관은 표재성이므로…」 → 이마 = 골막상 |
| 대상 근육 | **단위 시술 속성** | `muscles[{muscle, sites}]` → `target_muscles` | 「교근 (Masseter)」 → Masseter @ 사각턱 |
| 두께 · 덮임 같은 수치 · 근거 원문 · 출처 | **근거 속성** | `attach[{muscle}]` 또는 `attach[{layer, site}]` → `evidence` | `frontalis_thickness.midpupil_mm` 「1.8」 → Frontalis 근거 수치 |
| 뼈 · 구조 지표 | **주입 지표** | `landmarks`(넘겨받은 것) | 아래턱뼈각 @ 사각턱 · 아래턱뼈 아래모서리 @ 턱선 |
| 도구 형태 · 박피 깊이 | 단위 시술 속성 | `tool_form` · `peel_depth` | 롤러형 · 스탬프형 · 전동 / 얕은 · 중간 · 깊은 |
| 펄스 방식 · 가능 방식 · 박피 여부 · 전극 · 에너지 · 주입기 · 침투 방식 · 실 디자인 | **장비(제품) 속성** | `technique_hints[]` `pulse_mode` · `modes` · `ablative` · `pulse_scope` | 피코초 · Q스위치(나노초) · 롱펄스 / 모노폴라 · 바이폴라 / 멀티니들 / 이온도입 · 전기천공 · 초음파 / 코그 2방향 |

- 값은 **값 사전 안에서만**(`references/value-dictionary.md`) — 층 13 · 펄스 3 · 박피 2 · 도구 형태 3 · 박피 깊이 3 · 가능 방식 1 · 대상 근육 17. 사전에 없는 값이 필요하면 사전 한 줄 추가가 먼저(결정 목록)
- 층 값이 있는 행은 키가 `zones[<id>]` 여야 하고 그 zone 이 3단계 `danger_zone_mapping` 으로 부위 노드에 닿아야 한다
- 원천이 한 부위를 나눠 층을 따로 적었으면 **나눈 대로** `site_layer_split` — 코(묶음) = 골막상 · 연골막상 / 콧등 = 골막상 · 코끝 = 연골막상(J2)
- 대상 근육 키 = **영문**, 한글은 KMA 표준(`ko_kma`), 원천 표기는 `source_label` 로 보관 — 원천 한 표기에 두 근육이 겹치기 때문(「비근근」 = Procerus · Nasalis, X1)
- 장비가 프락셔널을 낼 수 있으면(`modes` 프락셔널) 그 단위 시술이 K04b — 가능 방식은 노드와 잇는 조건이다
- 펄스가 보조 매질에만 걸리면 **범위를 칸으로**(`pulse_scope`) — 셀렉V: 주 하위 계열 IPL · Q스위치는 보조 하위 계열 엔디야그 쪽에만
- **장비 속성(펄스 · 가능 방식 · 박피)은 5단계 제품 → 단위 시술 상속 근거다** — `procedure-hub-unit-check` §3(`technique_compat.requires` — K04a 펄스 · K04b 프락셔널). 속성이 없거나 어긋나면 그 장비는 조건 있는 기법 키를 상속하지 않는다(젠틀맥스 · 노블린 사례)
- 매질 · 입자 크기(IPL · 알렉산드라이트 · 루비 · 마이크로웨이브 · 미세 지방)는 **2단계 하위 계열** — 이미 정본, 다시 열지 않는다

### 2-4. 넘김 — 다른 단계 몫

`bucket` 「넘김」 + `stage`(2단계 · 5단계 · 7단계 · 8단계 · 계열 밖 · 시맨틱 — 이 밖의 값은 행선지 오류):

- **혈관 · 신경 · 합병증 → 8단계 안전**(`site_caution`) — 「Pitanguy line 위에서 안면신경 측두분지가 표재성으로 주행」 · 「이신경공 외측 피할 것」
- related_techniques 의 **다른 계열 언급 → 8단계 시술↔시술 관계** · 다른 계열 이름 · 하위 계열 이름 → **2단계**(이미 정본)
- **상담 이름 · 장비 프로그램 이름 → 5단계 단위 시술 이름** — 스킨보톡스 · 메조보톡스 · 에어보톡스 · 네페르티티 리프트 · 피코토닝 · 알렉스토닝 · BBL Forever Young · 포토나 4D
- 고민 · 목적 → 7단계(「진피색소」「진피 타이트닝」) · 비미용 → 계열 밖 · 시맨틱 묶음 이름 → 시맨틱
- 세션 순서 꼬리 중 마취 · 클렌징 · 진정은 세션 단계(지도 「꼬리는 4단계 기법 / 2단계 하위 계열 사전으로 풀어 conditions.sub」)
- 한 줄에 속성과 넘김이 같이 있으면 판정 「근거 원문 + 넘김」 · 「속성 값 + 넘김」 — 속성 칸과 `stage` 를 둘 다 적는다

### 2-5. 앞 단계가 넘긴 것 · 계열 기본

- **넘겨받은 것**: step3 deferred 4단계(조직층 진피 · 표피 · 피하) · step3 D-07 기법 축(네페르티티) · step3 `handoff_note`(사각턱 · 목 · 승모근 · 종아리 · 턱선) · step3 문자열(표정근) · step2 deferred 4단계(M8 방식 · M4 주입 기기) · step2 hint · 지도 U5 도포 가드 → `handoffs[]` 한 줄씩(H01~H15). 4단계로 보낸 것 **전수**가 행선지를 가져야 한다(역검사)
- **계열 기본 기법**: 2단계 계열마다 기본 1(+ 보조) — `family_defaults[]`(`references/family-defaults.md`). 단위 시술이 원천에서 다른 기법을 부르면 **5단계에서 덮어쓴다**(스킨보톡스 · 다한증 = K01a · 정맥 아닌 성분 주사 = 허가 용법)
- **새 계열**이 2단계에 서면 기본 기법 한 줄이 없어서 open — 계열 정의 동사로 고른다(§2-2 ①)

판정마다 「파일 · 키 · 원문 · 판정(verdict) · 묶음(bucket) · 노드 / 속성 칸 / 단계 · 근거(지도 칸 · 결정 행 · 문헌)」를 남긴다. 형식은 `references/record-schema.md`.

## 3. 4단계 규칙 체크리스트

각 줄은 `_RESUME.md` §2 10-28 결정이거나 4단계에서 틀린 것을 바로잡은 규칙이다. 틀렸던 예는 `references/mistakes.md`.

### 3-1. 범위

- [ ] **입력 = 지도가 4단계로 정한 칸만**(지금 27 · 줄 215 · 표현 181행). 결정: 사용자 「지금 모든 json이 메달리언에 녹아야 하는데」 → 지도 먼저 · 이후 단계 입력 = source-map
- [ ] **중복은 글자 그대로 같을 때만** — extracted ↔ taxonomy 51줄 → 17행
- [ ] **초안 큰 기법 65 는 재료지 기준이 아니다** — 유지 4 · 합침 29 · 버림 32. 장비 전극(모노폴라) · 하위 계열(IPL) · 실 디자인(오메가) · 상담 이름(스킨보톡스) · 층(진피 주입)이 한 칸에 섞여 있었다

### 3-2. 노드

- [ ] **큰 기법 = 계열 정의 동사 + mechanism 전달 태그** · group 은 기준 아님(X3) · regenerative · ablative 는 기법 아님
- [ ] **세부 = D-05 ① 또는 ②, 둘 다 아니면 안 쪼갠다** · **2층까지** · 노드마다 근거
- [ ] **노드 이름 = 상담 용어 · 의학 용어는 `medical_name` 속성** — 3단계 이름 2벌과 같은 꼴

### 3-3. 속성

- [ ] **층 · 깊이 · 대상 근육 · 도구 형태 = 단위 시술 속성(키 밖)** — 같은 부위에 층이 「또는」으로 둘인 곳이 5곳(관자놀이 · 팔자 · 입술 · 턱선 · 목) · 층을 노드로 두면 한 부위 주입이 둘로 갈린다. 근육은 부위와 1:1 이라 노드로 두면 노드만 는다
- [ ] **펄스 · 박피 · 가능 방식 · 전극 · 주입기 · 침투 · 실 디자인 = 장비 속성** — 펄스는 장비가 낸다. 한 장비가 피코초와 나노초를 둘 다 낸다(스타워커). 노드로 두면 같은 토닝이 장비마다 갈라진다
- [ ] **원문의 「또는」 · 「및」을 줄이지 않는다** — 「골막상 (코뼈 부위) 또는 연골막상 (비첨부)」는 둘이다. 틀렸던 예: J2 를 「HA 필러 · 코 · 골막상 주입」 하나로 사용자에게 냄 → 사용자 「같은 거야?」 → 결정 문구는 「코 · 주입」, 층은 콧등 골막상 · 코끝 연골막상 속성
- [ ] **수치는 근거지 층이 아니다** — `rhinion_subcutaneous_mm` 2.02 = 콧등 피하 조직 두께 근거(`attach`) · 주입 층 아님
- [ ] **근육 묶음 이름도 대상 근육 값** — 표정근 = Musculi faciei(`group: true`) @ 얼굴(3단계 부위 속성에서 4단계로 옮김 · H15)
- [ ] **뼈 · 구조 = 주입 지표 · 혈관 · 신경 · 합병증 = 8단계** — 해부학 결정(사용자 「해부학적 용어는 시술 방법이나 작용기전 쪽 아니야」)

### 3-4. 칸 · 숫자

- [ ] **다음 단계 스크립트가 읽을 값은 칸으로** — 문장(note)은 사람만 읽는다. 틀렸던 예: 셀렉V `pulse_scope` 가 반영 v1 에서 note 로 내려앉음(검수 W1) → 칸 되살림
- [ ] **숫자는 결정 · 정본에서 세어 낸다** — md 셈 줄 · 스크립트 문자열에 숫자를 손으로 적지 않는다. 틀렸던 예: 「조사 16 + 3단계 넘김 1」 · 「조사 14 + 브리프 추가 1」(검수 W2). 고정 숫자 assert 도 없다
- [ ] **결정을 옮길 때 표시도 옮긴다** — 구조 칸 · 근거 수준 · 넘김(3단계 §5-6 과 같은 꼴)

### 3-5. 끝 조건

- [ ] **끝 = 지금 원천 기준** — `step4-apply.py` open 0 · stale 0 · 결정론(같은 입력 → 바이트 같은 출력) · `step4-fixture-test.py` 10/10 · `check_techniques.py` errors 0
- [ ] **가상 문장 시험은 하지 않는다** — 「새 원천이 오면?」은 구조(결정 한 줄 빼면 그 한 줄이 open — fixture R1~R10)로 본다. 3단계 v2 ~ v4 FAIL 루프 교훈 · 4단계는 브리프에 처음부터 못박아 검수 1판으로 끝났다
- [ ] **검수 기준 = 지금 원천 · 지도가 정한 칸만** — 설명 문장 · 미래 원천은 보지 않는다

## 4. 갱신 방법

1. **결정 목록 먼저** — 변경분만. 각 항목을 셋 중 하나로 나눈다(4단계는 12묶음 S1~S12 중 사용자 앞에 간 것 2 — J1 · J2)
   - **승인**: 규칙으로 답이 닫힌 것 — 새 표현의 속성 · 넘김 · 기존 노드 근거 · 사전 안 값 · 넘겨받은 것 행선지 · technique_hint 재확인. 「추천대로」 한 번에
   - **원천 질문**: 원천끼리 충돌(X1~X6 꼴) — 값은 원천 정본 쪽으로 두고 `conflicts[]` · 원천 수정 후보
   - **최종 판단**: 새 노드 · 노드 구조 · 값 사전 새 값 · 지도 변경 · DEC 문구 — 추천 + 기본값을 깔고 결정만 받는다
   - 질문에는 **원천 원문 그대로**(「또는」까지)와 파일 · 키를, 숫자에는 **단위(행 / 줄 / 칸 / 노드 / 값)와 판**을 붙인다
2. **반영 = 결정만 고치고 `step4-apply.py` 재실행(결정론)** — 원장 json · md 를 손으로 고치지 않는다
   - 재실행 **전에** 지금 정본을 판 사본으로 남긴다(`step4-techniques.v1.json` 식 — 회귀 비교용)
   - **새 표현 = `expressions[]` 한 줄** — `file` · `key` · `text` 는 open 에 찍힌 값 그대로 · `verdict` · `bucket` · `stage` · `destination` · `node` · `layers` · `constraint_text` · `muscles` · `attach` · `basis`(지도 칸 · 결정) · `decided_by`. 형식 `references/record-schema.md` §1-2
   - **새 넘김 = `handoffs[]` 한 줄**(`source_ref.type` = step3_deferred · step3_compound · step3_handoff_note · step3_string · step2_deferred · step2_ledger · step2_hints · source_map) — 3단계가 deferred 로 바꾼 것은 `step3_deferred` 로
   - **새 장비 hint = `technique_hints[]` 한 줄** — `hint` 는 step2 원문 그대로 · 보조 매질에만 걸리면 `pulse_scope`
   - **새 계열 = `family_defaults[]` 한 줄**(`family_name` = step2 이름)
   - **새 노드** = `nodes[]` 한 줄(`id` · `parent` · `medical_name` · `basis` · `decided_by`) + 그 노드로 가는 표현 · 초안 · 계열 행 — 최종 판단 뒤
   - **새 값** = `dictionaries` 의 그 사전 한 줄(대상 근육은 `key` 영문 · `ko_kma` · `source_label` · `sites` 3단계 노드 · `basis`) — 승인 뒤
   - 원천 · DEC · 3단계 정본이 틀려 보이면 고치지 않고 `source_fix`(`source_candidates` · `dec_text` · `step3`)에 — `step4-source-fix.md` 로 나온다
3. **점검** — 프로필 레포 루트에서

```bash
W=orchestration/work/phub-recommend
python3 $W/step4-apply.py                    # 정본 재생성(승인된 반영 때만). 시험은 --out <scratchpad> 로
python3 $W/step4-fixture-test.py             # 10/10 — 결정 한 줄 빼면 open 이 나오나
python3 <스킬>/scripts/check_techniques.py --work $W --out <scratchpad>/technique-check.json
```

   open 0 · stale 0 · errors 0 · fixture 10/10 · 같은 입력 재실행 바이트 동일(scratchpad `--out` 두 번 → `cmp`)
   - 3단계 정본을 고친 뒤면 3단계 먼저(`step3-apply.py` open 0) — 4단계는 `step3-sites.json` 을 읽는다
4. **검수** — 바뀐 행 전부를 결정 · 원천 원문과 대조(읽기 전용 검수자). 지도 칸을 **따로 짠 추출기로** 원천에서 다시 뽑아 산출 표현과 양쪽 차이 0 · 앞 판 사본과 행 단위 비교(지시한 행 밖 차이 = 회귀) · 구조 칸(`pulse_scope` · `site_layer_split`)이 note 로 내려앉지 않았나 · md 에 손 숫자 없나 · step1~3 · DEC · 지도 · 원천 md5 그대로
   - **검수 기준에 가상 문장 · 미래 원천 시험을 넣지 않는다**(§3-5)
5. **끝 조건 = 검수 PASS + open 0** — WARN 은 고친 뒤 코디 확인

## 5. 출력 형식 — 변경 보고

```markdown
## 기법 원장 변경 보고 (YYYY-MM-DD · 판 <전 → 후> · 원천 <스냅샷> · 대상 N행)

### 새 표현 (N행 · N줄)
- 「<원문>」 `<파일#키>` — <노드로 K.. / 속성 <layers · muscles · attach> / 장비 속성 / 넘김 → <단계>> · 판정 <verdict> — <지도 칸 · 결정 근거>

### 행선지 변경 (N행)
- 「<원문>」 — <전 묶음 · 노드 · 단계> → <후> · 이유 <규칙 · 바뀐 원천 · 사용자 판단>

### 노드 · 사전 변경
- 새 노드 <id 이름>(상위 <>) — D-05 ① <원천이 따로 부르는 곳> · ② <시술 · 안전 차이> · 근거 표현 N
- 안 세움 — <이름> → <속성 · 5단계 이름>(D-05 ① ② 둘 다 아님)
- 사전 <layer · pulse_mode · target_muscle …> + <값>(근거 <원천 · KMA>)
- site_layer_split <zone> — <부위 = 층>(원문 「…」)

### 넘겨받은 것 · 장비 · 계열
- H.. <출처> <항목> → <행선지>
- technique_hint <ledger_id 이름> — pulse_mode <> · modes <> · ablative <> · pulse_scope <>
- 계열 <M..> 기본 <K..>(+ <보조>) — 정의 「<동사>」

### 사람에게 물을 것 (승인 N · 원천 질문 N · 최종 판단 N)
- [승인] 「<원문>」 — <한 줄: 무엇이 · 왜 · 추천>
- [원천] <충돌 a ↔ b> — 둔 값 <> · 원천 수정 후보 <>
- [최종 판단] <새 노드 · 새 값 · 지도 · DEC 문구> — 추천 <> · 기본값 <> · 원문 「…」(「또는」 줄이지 않음)

### 점검
- step4-apply: 노드 N · 표현 N행(속성 N · 넘김 N · 노드로 N · 중복 N) · 계열 기본 N · 넘겨받은 것 N · hint N · open N · stale N
- fixture N/10 · check_techniques errors N · 결정론 <바이트 같음 예/아니오>
```

변경이 0 이면 「변경 0 — check_techniques open 0 · stale 0 · errors 0(결과 경로)」 한 줄로 끝낸다.
