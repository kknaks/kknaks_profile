# 검수 — 실버 3단계(부위) 반영 (step3-apply)

**판정: FAIL** · **open = 12** · FAIL 5 · WARN 7

끝 조건(open 0)을 채우지 못했다. 원장 안의 `open[]` 은 0 이다. 하지만 원천을 따로 다시 뽑아 보니 사전이 놓친 부위 문자열이 있었다(F1). 조사 판에서 「근거 약」 표시가 붙은 7행이 결정 파일로 넘어오면서 빠졌다(F2). D-07 분리가 노드 쪽에서 무너진 행도 16개 있다(F3).

- 검수자: reviewer(read-only) · 2026-10-28 · 브리프 `phub-recommend-review-step3-brief.md`
- 정본: `_RESUME.md` §2 10-28 「3단계 부위 조사(step3-research) 반영 — 전부 추천대로(사용자)」(127행) · 「3단계(부위) 시작」(128행) · `DEC-002.md` D-03 · D-05 · D-07 · 부위 트리 · `DEC-003.md`
- 대상: `step3-decisions.json` · `step3-apply.py` · `step3-sites.json` · `.md` · `step3-source-fix.md` / 근거 `step3-research.json` · `.md` / 원천 `PROCEDURE-HUB/phub-stg-2026-10-26/` 21개

## 0. 요약

| # | 볼 것 | 결과 |
|---|---|---|
| 1 | 결정 ↔ 반영(B1~B12 · U1 · U2) | U1 · U2 · B1 · B2 · B5 · B6 · B7 · B8 · B9 · B11 · B12 **PASS**. 트리 밖 18이름 · 37문자열을 행 단위로 모두 대조했다. 노드는 53(트리 37 · OQ-206 6 · 새 10)이고, 상위가 트리와 결정대로 맞으며 node_ids 53개는 겹치지 않는다. **B4 FAIL**(F2) · **B3 FAIL**(F3 · F4) |
| 2 | 문자열 500 전수 | 반영 셈 **PASS**: 노드로 325 + deferred 175 = 500 · open 0이고, 조사 판 290 + 트리 밖 35 = 325, 173 + B6 2 = 175 다. **원천 전수 FAIL**(F1): 사전 밖 낱말 하나하나를 원천에서 따로 다시 뽑았더니 노드로 갈 것 35회, 부위 아님 15회가 셈에 없다 |
| 3 | D-07 분리 · 트리 위반 | 트리 위반은 0 이다. **D-07 FAIL**(F3): 6행은 넘김 정보가 노드 표에서 빠졌고, 10행은 다른 축을 떼지 않은 채 동의어로 들어갔다 |
| 4 | 해부학 이름 후보 53 | 「강」 24 · 「중」 4 의 인용 28줄을 원천 키에서 전수 대조했다. 값은 모두 레포에 있다. 다만 **인용 키가 틀린 곳 3 · 다른 결정과 서로 어긋나는 곳 1**(F5)이 있다. 「약」 25 는 의료진 질문 1줄(AN)에만 묶여 있다(W5) |
| 5 | 위험 부위 11 · 의료진 질문 | 위험 부위 11 은 결정 대응과 노드의 `danger_zone` 이 11/11 일치해 **PASS**. 의료진 질문은 22 다. 근거 약 7행이 빠졌으니(F2) 29 여야 한다 |
| 6 | 범위 위반 · 수정 금지 | **PASS**: 시술↔부위 엣지 · 기법 목록을 만든 곳은 없고 `deferred` 표시만 했다. DEC-001~003 · step1 · step2 · procedure-master-v3 · 원천 21개 모두 3단계 발주(10-28 14:37) 앞의 mtime 그대로다. 원천은 10-26 22:11 이다 |
| 7 | 결정론 · 구조 | 결정론 **PASS**: scratchpad 사본에서 다시 돌린 결과 3파일 모두 바이트가 같다(`step3-sites.json` sha1 `09de8d4e…`). 고정 숫자 assert 는 없다(**PASS**). 구조는 **WARN**(W1~W4): 결정의 절반이 아직 조사 판(json)에 있다. 원천을 새로 넣으면 순서까지 맞아야 하는 가드에 걸려 멈추고, 결정 파일만 고쳐서는 흡수할 수 없다 |
| 8 | open 0 | 원장 `open[]` 은 0 이지만 검수 open 은 **12** 다 |

---

## FAIL

### F1. 원천 전수 누락 — 사전이 못 잡은 부위 문자열(노드로 갈 것 35회 · 부위 아님 15회)

- **방법**: 조사 사전과 별개로 부위 형태소 약 110개(한글)와 영문 어간 약 75개를 만들었다. 원천 21개의 문자열 칸 22,749개를 전부 훑었고, 조사 사전의 매치 범위(skip 포함)와 겹치지 않는 등장만 남겼다(597종 · 3,662회). 남은 것은 문맥을 하나씩 읽고 가려냈다. 「부위」 911 · 「…등」 나열 244 · 각질/질환(질) · 주입/입자(입) · 발현(발) · 배양(배) · 알코올(코) 같은 글자 겹침은 조사 §2-1 excluded 와 같은 기준으로 셈에서 뺐다. 「등」은 부위 뜻 8회가 모두 조사 패턴에 잡혀 있는 것을 확인했다.
- **근본 원인**: ① 영문 패턴이 대소문자를 가린다. method.normalize 는 「영문이면 소문자」로 정규화하는데 매칭(`re.compile(x['pattern'])`, `step3-apply.py:51`)은 대소문자를 구분한다. 그래서 `안면` 사전이 226회만 잡는다(대소문자 무시면 257). 콧등 사전은 20(21), 해부 지표 사전은 73(75)이다. ② 사전에 낱말 자체가 없다.
- 조사 §2-1 「residual_check … 남은 것 0」과 §9 「겹침 외 0 을 확인했다」는 **사실이 아니다**.

**노드로 가야 하는데 빠진 것(35회)**

| 문자열 | 등장 | 파일:키 | 고칠 값 |
|---|---|---|---|
| 뱃살 | 1 | taxonomy.json `modality[].subcategories[].items[].extracted.indications.primary[]` 「뱃살 제거」 | 복부 + 살(지방) → 7단계 고민(D-07). 「배」(S274)와 같은 근거 약 → 의료진 질문 |
| around the mouth | 1 | literature-evidence.json `categories.M2.moa[].patient_en` 「support to areas around the mouth」 | 입가 동의어(영문). perioral(S244)과 같은 자리 |
| Face · Facial(대문자) | 24 · 6 | literature-evidence.json `categories.M2.moa[].citations[].title`(「Whole-Face Approach…」 · 「…Facial Aesthetic Treatment…」) | 같은 citations.title 칸의 소문자 「face」 4회는 이미 셌다. 규칙을 하나로 정한다. (a) 영문 패턴을 대소문자 무시로 바꿔 face 10→34 · facial 21→27 로 세거나, (b) citations.title 을 학술지명 「craniofacial」처럼 셈 밖으로 빼서 face 10→6 으로 센다 |
| Facial Contouring | 1 | taxonomy.json `problem[].category_en`(P11 윤곽 대분류의 영문 이름) | 얼굴 + 윤곽 → 7단계 고민(D-07) |
| Body | 1 | taxonomy.json `problem[].category_en`(P12 바디 대분류의 영문 이름) | 바디. 근육 「body」(교근 body 등)와 「Foreign Body」는 지금처럼 셈 밖에 둔다 |
| Bunny lines | 1 | anatomy-danger-zones.json `zones[nose].botox_specific.dose_range` | S119 「bunny lines」 행에 합친다(대소문자). 분리는 F3 대로 |

`category_en` 두 칸은 대분류 이름이라 이름 칸 성격이다. `method.name_fields`(규칙 ①)에 넣을지 코디가 정한다. 지금 산출물은 둘 다 아예 세지 않았다.

**부위 아님으로 넘겨야 하는데 빠진 것(15회)**

| 문자열 | 등장 | 파일:키 | 고칠 값 |
|---|---|---|---|
| eye · eyes | 2 | literature-evidence.json `categories.M1.adverse_effects[].statement` 「Dry eye」 · `.patient_en` 「dry eyes」 | 「눈(기관 · 동작)」 행에 합치고 안전 원장(합병증)으로 |
| 구강 | 5 | anatomy-danger-zones.json `zones[lips].botox_specific.risk` 「구강 기능 장애」 · complications.json `mechanism` · `risk_factors[]` · `prevention` · pre-procedure-checklist.json `category_specific[].checks[].label` | 부위 아님 → 안전 원장(합병증 · 감염 경로) |
| 구순포진 · 구순염 | 2 | pre-procedure-checklist.json `universal_checks[].description` · taxonomy.json `…extracted.safety.common[]` | 부위 아님 → 안전 원장(금기 · 부작용) |
| 이개 | 1 | anatomy-danger-zones.json `zones[neck].nerves[].significance` 「이개, 이하부 감각」 | 위험 부위 속성(ANATOMY_HAZARD · 해부 지표) |
| deep temporal fascia · Superior temporal line · Mental foramen ×2 · orbital septum | 5 | anatomy-danger-zones.json `zones[temple].safe_injection_depth` · `.tissue_data.stl_entry_point` · `zones[chin].tissue_data.notes` · `.clinical_pearls[]` · `zones[periorbital].tissue_data.orbital_septum` | 위험 부위 속성. 한글 병기(심부측두근막 · 상측두융합선 · 이신경공 · 안와격막)는 이미 셌다. 영문 병기는 추미근/corrugator supercilii 처럼 따로 세는 게 방법이니 같은 규칙으로 맞춘다 |

- 사전에서 `\bala\b` 를 대소문자 무시로 바꾸면 성분 「ALA」 8회가 콧망울로 들어간다. 이때는 `#skip:ALA` 를 대소문자 구분 패턴으로 앞에 둔다(excluded 「ALA(성분)」).
- 고치면 조사 판의 rows · lexicon 과 반영 셈(500 · 3,582 · 노드로 · deferred)이 모두 바뀐다. 다시 돌린 뒤 이 표의 50회가 행으로 잡혔는지 다시 확인해야 한다.

### F2. B4 근거 약 — 트리 밖 7행의 「약」 표시와 의료진 질문이 빠졌다

- 위치: `step3-decisions.json` `weak_strings.strings`(20개) → `step3-apply.py:117` `weak = {…DEC['weak_strings']…}` → `step3-sites.json` strings[S280 · S328 · S329 · S390 · S486 · S492 · S493].weak = false · doctor_questions 22
- 근거:
  - `step3-research.json` rows 에서 이 7행은 `weak: true` 다(조사 판 weak 행은 27개).
  - 조사 B4 「영향」 칸에 「노드로 가는 것 중 20문자열 · 78회 **+ 트리 밖 무릎 · 불독살 · 하관 계열**」이라고 적혀 있다. 결정은 「추천대로」다.
  - 조사 §3 무릎 「근거 없음 … 근거 약 둘 다」 · 옆구리 행 「허리라인 = 근거 약」
  - 조사 판 §8 질문 목록도 이 7행을 빼먹었다. 결정 파일이 그것을 그대로 옮겼다.
- 고칠 값: `weak_strings.strings` 에 `["무릎","무릎"]` · `["lower face","하안면"]` · `["하안면","하안면"]` · `["하안면부","하안면"]` · `["하관","하안면"]`(행의 group 값 그대로) · `["불독살","불독살"]` · `["허리라인","옆구리"]` 7개를 더한다. 그러면 **근거 약 27 · 의료진 질문 29** 가 된다. 하관 계열 4행은 사용자가 U1 에서 고른 것이다. 그래도 근거 수준 표시와는 별개라 질문은 단다.

### F3. D-07 분리 — 다른 축이 붙은 문자열 16행이 노드 동의어로 들어감

**(a) 넘김 정보가 있는데 노드 표에서 동의어로 나온다(6행)**: 스크립트가 `kind` 로 나누기 때문이다(`step3-apply.py:174 · 176`). 트리 밖 행은 kind 가 「트리 밖」이라서, `handoff` 가 있어도 `synonyms[]` 로 간다. `synonyms[]` 칸에는 handoff 가 없어 노드 표와 json 노드에서 고민 · 계열 조각이 사라진다.

| 행 | 문자열 | 노드 | 사라진 넘김 |
|---|---|---|---|
| S319 · S423 · S465 | 마리오네트 라인 · 마리오넷 · 마리오네트선 | 마리오네트 | 라인(주름) → 7단계 고민 |
| S390 | 불독살 | 턱선 | 처짐 · 살 → 7단계 고민. 결정 B5 문구가 「턱선 동의어 **+ 고민 처짐**」이다 |
| S387 · S388 | 헤어라인반영구 · SMP | 두피 | 반영구 → 2단계 계열(눈썹반영구 · 입술반영구 · 아이라인반영구는 D-07 로 갔다) |

고칠 값: 174 · 176 행의 기준을 `s['kind']` 에서 `s['handoff']` 가 비었는지로 바꾼다. 비어 있지 않으면 `compound_strings` 다.

**(b) 다른 축이 붙어 있는데 넘김 없이 동의어나 노드 이름으로 갔다(10행)**: 조사 판 행 값의 문제다. B3 「부위+다른 축 분리(D-07)로 단다」에 어긋난다.

| 행 | 문자열 | 지금 | 같은 꼴인데 D-07 로 간 행 | 고칠 값 |
|---|---|---|---|---|
| S302 | 꺼진 눈 | 눈가(묶음) 동의어 | 눈밑 꺼짐(D-07) | 눈가(묶음) + 꺼짐 → 7단계 고민 |
| S293 · S119 | 토끼주름 · bunny lines | 콧등 노드 이름 | 까치발 주름 · crow's feet(D-07). 조사 note 도 「콧등+주름 구어」 | 콧등 + 주름 → 7단계 고민 |
| S472 | 신체 처짐 | 바디 노드 이름 | 바디 쳐짐(D-07) | 바디 + 처짐 → 7단계 고민 |
| S473 | 전신 처짐 | 전신 노드 이름 | 〃 | 전신 + 처짐 → 7단계 고민 |
| S411 | 탄탄한 몸 | 바디 노드 이름 | 바디탄력(D-07) | 바디 + 탄력 → 7단계 고민 |
| S353 | EMS 바디 | 바디 노드 이름 | 사각턱 보톡스 · 턱선보톡스(계열 → 2단계) | 바디 + EMS → 2단계 계열 |
| S476 | 초음파목 | 목 노드 이름(시장가 「RF+초음파목」) | 〃 | 목 + 초음파 → 2단계 계열 |
| S310 | 손등 회춘술 | 손 동의어 | 볼볼륨충전(D-07) | 손 + 회춘술(손등 볼륨 채움) → 6단계 목적. 근거 약은 유지 |
| S315 | 임신선 | 복부 노드 이름 | 「튼살」 고민. 이름 칸 「성장선/임신선」 | 복부(함축) + 튼살(임신선) → 7단계 고민. 근거 약은 유지 |

- 「어깨라인」(S406 · 승모근 동의어)은 DEC-002 D-03 표(86행)가 「구어(동의어 후보)」로 정했으므로 그대로 둔다. 같은 꼴인 「허리라인」(S493 · 옆구리)에는 그런 근거가 없다(W7).

### F4. 상악골 · 위턱뼈 → 턱(묶음) — 행의 근거 문구와 값이 어긋남

- 위치: `step3-research.json` lexicon `하악` 패턴 `하악(?![가-힣])|상악골|위턱뼈|[Mm]andib…` · site 턱(묶음) → rows S306 · S307 → `step3-sites.json` 턱(묶음) synonyms
- 근거: 그 행의 note가 스스로 「상악골 · 위턱뼈는 **위턱** — 「상악골 윤곽성형」 1곳(근거 약, **중안면**)」이라고 적는다. 원천 문맥은 taxonomy.json · extracted.json M2 `indications.extended[]` 「상악골 윤곽성형 (위턱뼈 주변)」이다. 트리의 턱(묶음) 하위는 턱끝 · 턱선 · 사각턱 · 턱밑으로 모두 아래턱이다. 「중안면 · 중안면부」는 같은 결정(B4)에서 볼(묶음)로 갔다.
- 고칠 값: lexicon 에서 `상악골|위턱뼈` 를 `하악` 에서 떼어 따로 항목으로 만들고 site 를 **볼(묶음)** 으로 한다(중안면과 같은 자리). 근거 약과 질문은 그대로 두되, 질문은 「상악골(위턱뼈) 윤곽성형을 볼(묶음)(중안면)에 둔다 — 맞나」로 바꾼다. 지금 질문 「「상악골」 를 턱(묶음) 에 둔다 — 맞나」는 아래턱/위턱이 어긋난다는 사실을 의료진에게 숨긴다.

### F5. 해부학 이름 근거 — 인용 키 틀림 3 · 자기모순 1

「강」 24 · 「중」 4 를 전수 대조했다. 인용된 원문 28줄 중 24줄은 적힌 키에 그 값이 그대로 있다. 눈꺼풀 · 코끝 · 콧등의 「이름 — course」 인용은 같은 vessels 원소의 name 과 course 를 「 — 」로 이어 붙인 것인데, 두 값 모두 그 원소에 있다. 아래 넷은 고쳐야 한다(`step3-research.json` nodes[].anatomical_basis → `step3-sites.json` 그대로 복사).

| 노드 | 지금 근거 | 원천 사실 | 고칠 값 |
|---|---|---|---|
| 두피(중) | 「레포 taxonomy(제품 extracted) 「scalp」 1곳」 | 원천 21개에 소문자 「scalp」는 없다. 유일한 등장은 taxonomy.json `problem[P13].category_en` 「Scalp & Hair Loss」(대분류 이름)다 | 키를 `taxonomy.json problem[P13].category_en 「Scalp & Hair Loss」` 로. 수준 중은 그대로 |
| 사각턱(강) | 「「하악각」(extracted)」 | extracted.json · taxonomy.json 에 「하악각」이 없다. anatomy-danger-zones.json `zones[jawline].vessels[0].course` 「하악각 전방에서…」 · `.tissue_data.notes` · `.clinical_pearls[0]` 에만 있다 | 키를 `zones[jawline].vessels[0].course · clinical_pearls[0]` 으로 |
| 팔자(강) | 「zones[nasolabial].name_en 「Nasolabial Fold」 · 「비순구」」 | 「비순구」는 nasolabial zone 에 없다. `zones[periorbital].vessels[0].course` 「…비순구를 따라 상행」에만 있다 | 「비순구」의 키를 `zones[periorbital].vessels[0].course` 로 |
| 얼굴(강) | literature M1 effects 「contours the lower face」 · M2 moa 「structure and framework to the face」 | 「lower face」는 하관 결정(U1)에서 **턱(묶음)** 으로 갔다(S328). 같은 문장을 얼굴의 근거로 쓰면 자기모순이다 | M1 인용을 빼고 M2 「structure and framework to the face」(PMID 32445044)만 남긴다. 수준 강은 그대로 |

---

## WARN

### W1. 결정이 데이터 파일로 절반만 빠졌다 — 새 문자열은 조사 판을 손으로 고쳐야 함

- 위치: `step3-apply.py:126`(노드로 행선지 = `r['site']`, 조사 판) · `:137`(deferred 단계 = `r['other_parts'][0]['stage']`, 조사 판) · `:174-180`(kind · synonym_type · handoff · 해부학 이름 · 위험 부위 = 조사 판 `rows` · `nodes`)
- 지금 `step3-decisions.json` 에 있는 것은 트리 밖 18 · 근거 약 · 노드 추가 · 질문 extra · 경계 규칙 · 원천 수정 목록이다. B3(290행 행선지) · B7(173행 단계) · D-07 넘김 · 노드 속성(B9 · B10)은 조사 산출물 `step3-research.json` 에 남아 있다.
- 결과: 새 부위 문자열 하나를 넣으려면 조사 판 `method.lexicon` 에 패턴을 넣고, `rows` 에 count · count_name_fields 가 정확한 행을 **원천 첫 등장 순서 자리에** 손으로 끼워야 한다(W2). 「결정 파일만 고치면 되는 구조」가 아니다. 2단계의 한계(이름별 dict)를 코드에서 조사 json 으로 옮긴 셈이다.
- 고칠 값: 행선지(`site` · `kind` · `other_parts` · stage) · 노드 속성 · lexicon 을 결정 파일(또는 결정 쪽 파일 `step3-lexicon.json`)로 옮긴다. 조사 판은 근거(표본 · note)로만 읽는다. rows 는 스크립트가 원천에서 만들어 낸다.

### W2. 재추출 가드 — 조사 판과 같은지만 보고, 새 원천은 막기만 하며, 전수성은 보지 못함

- 위치: `step3-apply.py:79-84`
- ① `list(found) != list(rkey)` 는 **순서까지** 비교한다. 원천 파일 하나나 문장 하나만 늘어도 첫 등장 순서가 밀려 「검사 실패」로 멈춘다. 집합 + 등장 수 비교로 충분하다.
- ② 새 원천(새 stg 스냅샷 · 새 파일)이 들어오면 등장 수가 하나만 달라도 멈춘다. 결정 파일에 행선지를 더해 흡수할 길이 없고 조사를 다시 돌려야 한다. 옳은 꼴은 「사전에 잡혔는데 결정에 없는 행 = `open[]`」으로 내보내고, 결정 파일에 행선지를 더하면 닫히는 구조다. 그러면 끝 조건 open 0 이 새 원천에도 그대로 통한다.
- ③ 가드는 같은 사전으로 다시 센 것이라 조사 판과의 **동일성**만 보장한다. 사전 밖 낱말(F1)은 가드가 보지 못한다. 전수성 검사(사전 밖 부위 형태소 잔여 = 0, 허용 목록 대조)를 스크립트에 넣는다. 조사 §2-1 residual_check 를 코드로 만드는 것이다.
- `SRC` 가 스냅샷 경로로 박혀 있다(`:21`). 원천 경로는 결정 파일의 `source` 키로 옮긴다.

### W3. 셈 검사 일부가 동어반복 · 위험 부위 결정을 강제하지 않음

- `:199` `len([s … if s['weak']]) != len(weak)` 의 양변은 같은 집합에서 나오므로 항상 통과한다. 쓸모 있는 검사는 「조사 판 weak 행 ⊆ 결정 weak」 같은 대조인데, 그랬다면 F2 를 잡았다.
- `:196` deferred 기대값도 같은 rows 로 계산한다.
- `:181-184` 는 「zone 을 가진 노드가 하나라도 있으면」 통과한다. `danger_zone_mapping[].node` 가 실제로 그 zone 을 `같음/묶음/추천` 으로 갖는지는 보지 않는다. 지금 값은 11/11 일치(검수 확인)하지만 강제하지는 않는다. 고칠 값: `노드[mapping.node].danger_zone.zone == mapping.zone` 를 검사한다.

### W4. md 셈 줄 · 질문 종류가 코드에 박혀 있음

- `:234` 「위험 부위 대응 **1** + 해부학 이름 **1**」은 리터럴이다. `:189` 질문 종류는 `q['id'] == 'DZ'` 분기다. extra 질문이 하나 늘면 셈 줄이 틀리고 종류도 잘못 붙는다. 고칠 값: `doctor_questions_extra[].kind` 를 결정 파일 필드로 두고, md 는 종류별로 Counter 를 센다.

### W5. 해부학 이름 「약」 25 — 개별 질문이 없음

- `doctor_questions` 의 AN 1줄 「후보 53 확정」에 「약」 25 가 묶여 있다. 레포 근거가 없는 25 노드(이마(묶음) · 눈가 · 코 · 잇몸 · 턱(묶음) · 턱밑 · 얼굴 전체 · 바디 하위 전부 · 새 노드 9 등)가 무엇인지 질문만 보고는 알 수 없다.
- 고칠 값: AN 의 value 에 「약」 노드 id 25개를 적는다. 또는 「약」 노드마다 질문 1줄(「X 의 해부학 이름을 ‹en› · ‹ko› 로 둔다 — 근거 표준 용어집만 — 맞나」)을 만든다.

### W6. kind 표기 — 부위 둘을 나열한 행이 「부위+다른 축(D-07)」

- S233 볼/관자놀이 · S371 이마/관자놀이 · S373 턱/턱선 · S383 볼/광대: `other_parts` 가 비어 있다(다른 축 없음). 노드 표 「부위+다른 축 → 넘김」 칸에 화살표 없이 나온다. 고칠 값: kind 를 「여러 부위(나열)」로 바꾼다. F3(a) 의 handoff 기준 수정 뒤에는 동의어 칸으로 간다. 그대로 둘지는 코디가 정한다.

### W7. 「…라인」 규칙이 한 줄로 정리되지 않음

- D-07 로 간 것: 페이스라인 · 바디라인 · 다리라인 · 코 라인 · 입술라인 · 마리오네트 라인(라인 → 고민). 동의어로 간 것: 어깨라인(DEC-002 D-03 근거 있음) · 허리라인(근거 없음 · 근거 약) · 턱라인(= 턱선, 해부 이름이라 맞음) · 네크라인.
- 고칠 값: `boundary_rules` 에 「‹부위›라인 = 부위 + 고민 「라인」. 예외는 턱라인(= 하악연 해부명) · 어깨라인(DEC-002 D-03)」 한 줄을 넣는다. 허리라인은 옆구리 + 라인 → 7단계로 둔다. F2 의 근거 약은 그대로 유지한다.

---

## 확인한 것 — PASS 근거

- **결정 ↔ 반영**: 트리 밖 37행을 하나씩 보면 `out_of_tree` 결정 18이름의 strings 에 정확히 한 번씩 걸리고, 남는 결정은 없다. U1 7 · U2 7 · B5 2 · B6 2 의 `resolution` · `node` · `parent` 가 `_RESUME` 127행과 조사 U1 · U2 표에 맞는다. 하관 결정은 lower face · 하안면 · 하안면부 · 하관 4행 12회로, 조사 U1 「하관 12회」와 같다.
- **노드 53**: `procedure-master-v3.json site_tree` 43개의 parent 를 바꾸지 않았다. 새 10개의 상위는 바디 4 · 얼굴 2 · 입가 2 · 코(묶음) 1 · 눈가(묶음) 1 로 U1 · U2 와 같다. node_ids 53개는 겹치지 않는다.
- **경계(B8)**: 「이마 · 눈가 · 코 · 볼 · 목」 단독은 좁은 노드로 갔다. zone 이름(periorbital · nose · cheek · neck)과 「하악 · 경부」는 묶음 노드로, 턱 단독 · 턱필러 · 턱보톡스는 턱(묶음)으로, 「전체얼굴 · 풀페이스 · 안면 전체 · 얼굴 전체 · 전안면」은 얼굴 전체로 갔다. 「전신」은 몸 표면 2행만 노드로 가고 계통 뜻은 lexicon_first 로 deferred 다. 규칙대로다.
- **B11 · B12 원천 대조**: P5-4 항목은 백옥주사(「글루타치온 IV」) · 비타민C주사(modality_ref M16 · problem-packages cc_detail 「고용량 정맥 투여」)라 B11 ② 가 맞다. P4-3 은 NAD+수액 · 줄기세포치료 · 항산화수액이라 ③ 이 맞다. 「비근근 (Procerus)」(glabella target_muscle) · 「비근근 (Nasalis)」(nose target_muscle)로 B12 ① 이 맞다. 「중측두정맥은 관자궁 상방 약 2cm」(temple clinical_pearls)로 B12 ② 가 맞다. DEC-002.md 는 고치지 않고 목록만 냈다.
- **위험 부위 11**: forehead 이마 · glabella 미간 · temple 관자놀이 · periorbital 눈가(묶음) · nose 코(묶음) · nasolabial 팔자 · cheek 볼(묶음) · lips 입술 · chin 턱끝 · jawline 턱선 · neck 목(묶음)이다. 결정 대응 노드가 sites 노드의 `danger_zone` 에서 같음 · 묶음 · 추천으로 붙어 있고, 하위 노드는 「상위 묶음 zone」으로 붙어 있다. 의료진 질문 DZ 1줄도 있다.
- **결정론**: `step3-apply.py` · `step3-decisions.json` · `step3-research.json` · `procedure-master-v3.json` 을 scratchpad 로 복사해 돌렸다. `step3-sites.json` · `.md` · `step3-source-fix.md` 가 원본과 바이트 동일하다(`cmp`). 스크립트에 고정 숫자 assert 는 없다.
- **범위**: `step3-sites.json` 에 시술↔부위 엣지 · 기법 목록 · 고민 노드가 없다. 다른 단계 일은 `deferred[].stage` · `handoff` 표시만 했다.

## 다시 돌릴 때 순서(제안)

1. F1 · F3(b) · F4 · F5 · W6: 조사 판의 lexicon · rows · nodes 를 고친다. W1 을 받으면 결정 쪽 파일로 옮겨서 고친다.
2. F2 · W4 · W5 · W7: `step3-decisions.json` 을 고친다.
3. F3(a) · W2 · W3: `step3-apply.py` 를 고친다(handoff 기준 · 순서 없는 비교 · 새 행 = open · 잔여 형태소 검사 · 위험 부위 강제).
4. 재검수에서는 F1 표의 50회가 행으로 잡혔는지, 근거 약 27 · 질문 29(+F1 로 늘어난 약 행), open 0 인지 본다.
