# 최종 검수 v5 — 실버 3단계(부위) 범위 바로잡기

**판정: FAIL** · **open = 1** · FAIL 1 · WARN 0

지금 원천 기준으로만 봤다(가상 문장 시험 · 목록 확장 · 미래 원천 대비는 보지 않음 — `_RESUME` §2 10-28). 이름 칸 17 · 노드 53 · 질문 35 · 결정론 · 수정 금지는 모두 맞다. 다만 이름 칸 안의 부위 문자열 **1건(「코조각주사」)이 허용 목록에 「성분 · 제품 이름」으로 잘못 들어가 행 없이 빠져 있다.** 결정 한 줄로 닫힌다.

- 검수자: reviewer(read-only) · 2026-10-28
- 기준: `_RESUME.md` §2 10-28 3단계 행 전부(부위 = 「어디에 맞냐」 · 원천은 이름 칸만 · 노드 이름 2벌 · 해부학 용어는 기법 · 안전 쪽 · 끝 조건 = 지금 원천 기준) · DEC-002 D-05 ①
- 방법: 모든 실행은 scratchpad 사본에서 했다. 레포 안에서 고친 파일은 이 리포트 하나다

## 1. 이름 칸 17 — PASS

- **D-05 ① 대조**: 「원천이 따로 부르는 칸」은 넷이고, 17칸이 넷을 다 덮는다.
  - 시장가 — market-pricing `items.name`
  - 고민 분류 — taxonomy `problem` 대분류 · 영문 · 중분류 · 항목 이름 · 꼬리표 / problem-packages `problem` · `cc_group` · `cc` · `cc_detail` / problem-combos `problem`
  - 용도별 — taxonomy `modality` 중분류 · 항목 이름 · 꼬리표
  - 위험 부위 — anatomy-danger-zones `zones` id · name_ko · name_en
- **원천 키 대조**: 21파일을 다시 훑어 키 1,215개를 뽑았다. 17칸은 모두 원천에 있고, 칸 수를 더하면 **1,953** 으로 md 셈과 같다.
- **빠진 이름 칸 없음**: 17칸 밖의 이름꼴 칸 18개를 사전으로 훑었다. 사전 무리 가운데 17칸에 없는 것은 synergy `links.target` 「코성형」 1회뿐인데, 코 노드는 이미 17칸이 근거를 갖고 있다. 훑은 18칸은 다음과 같다.
  - patient-education `patient_name` · pih-risk `name` · `subcategory`
  - problem-combos `packages.name` · procedure-comparison `procedures.name` · `title` · `subtitle`
  - combo-recipes `name` · `subtitle` · treatment-sequence `common_combos.name`
  - problem-packages `combos.name` · `procedures.name`
  - taxonomy `modality.products.name` · `modality.category_en`
  - post-procedure-timeline `name` · market-pricing `categories.name` · synergy `target` · treatment-optimization `plan_name`

## 2. 이름 칸 부위 문자열 175 · 439회 — FAIL 1

- **결정대로**: 행 175 의 destination · nodes · deferred_stage · kind 를 `step3-decisions.json strings[]` 와 하나씩 대조했다. 어긋남 0 이다. 결정 쪽에도 행이 없는 것이 0 이라 stale 도 0 이다.
- **독립 재추출**: 이름 칸 1,953칸을 직접 걷고, 검수자가 따로 만든 부위 형태소(한글 약 90 · 영문 약 50)로 사전이 덮지 못한 낱말을 찾았다. 남은 56종은 모두 글자 겹침이다(주입 · 수입 · 사마귀 · 트라넥삼산 · 배양액 · 「… 등」 나열 · 셀룰라이트(고민) …). **하나만 실제 부위다.**

### F-1 (FAIL) 「코조각주사」 — 이름 칸의 부위 문자열이 허용 목록에 묻힘

- 원천: taxonomy `modality[수액치료].subcategories[지방분해주사 (마케팅명)].items[auto-M16-1775403061033].name` 「코조각주사」이다. 단위 시술 이름 칸이다.
- 지금 상태: `step3-lexicon.json residual.allowed` 「성분 · 제품 이름(알코올 · 코직산 · 코엔자임 · 피코 · 코팅 …)」 무리에 토큰 「코조각주사」가 들어 있다. 그래서 행 없이 셈 밖이고, open 0 이다.
- 왜 틀렸나: 성분이나 제품 이름이 아니다. 「코(부위) + 조각주사(지방분해 주사 마케팅 이름)」인 단위 시술 이름이다. 꼬리표 「콧망울 지방분해 · 코 라인 날렵하게」가 그 뜻을 받쳐 준다. 이 항목의 부위는 꼬리표 쪽 행(콧망울 · 코 라인)으로 잡히긴 하지만, 이름 칸 문자열 자체는 행이 없다. 같은 꼴인 「코필러」 · 「코실리프팅」은 D-07 행이다.
- 고칠 값:
  - 허용 목록에서 「코조각주사」를 뺀다.
  - 사전 `코` 계열에 `코조각주사` 항목을 둔다.
  - 결정 한 줄을 더한다: node 코(꼬리표대로면 콧망울 — 사람 판단) · kind 부위+다른 축(D-07) · handoff 「조각주사 → 2단계 계열(지방분해 주사)」.
- 셈 영향: 문자열 175 → 176 · 등장 439 → 440 · 노드로 153 → 154 가 될 것이다.

허용 목록 422 가운데 이름 칸에 나오는 토큰 64종을 전부 다시 봤다. 실제 부위는 이것 하나다.

## 3. 노드 53 — PASS

- **상위**:
  - 트리 37 · OQ-206 6 · 3단계 추가 10 이 `_RESUME` 10-28 결정(콧망울 → 코(묶음) · 팔 · 가슴 · 등 · 옆구리 → 바디 · 수염 · 구레나룻 → 얼굴 · 인중 · 마리오네트 → 입가 · 눈썹 → 눈가(묶음))과 같다.
  - 가드 `node_ids · nodes 와 트리 + 추가` 도 통과한다.
- **이름 칸 근거**:
  - 52노드가 이름 칸 문자열을 1개 이상 갖는다.
  - 입가만 0 이다. 하위 6노드(팔자 · 입술 · 입꼬리 · 잇몸 · 마리오네트 · 인중)가 이름 칸 근거를 가진 묶음 자리라서 `name_field_exception` 에 이유가 적혀 있다. DEC-002 트리 노드이니 맞다.
- **전문의 용어 = 겉자리 이름만**: 53노드의 `anatomical_name.en/ko` 를 다 읽었다. 근육 · 뼈 · 혈관 이름이 값으로 들어간 노드는 0 이다(근거 칸에 원천 인용으로 나오는 근육 이름은 값이 아니다).
- **근육 4행 교체**:

| 노드 | 지금 값 | 넘김 메모 |
|---|---|---|
| 사각턱 | Parotideomasseteric region(TA2 214) | 깨물근 · 아래턱뼈각 → 4단계 |
| 목 | Anterior region of neck(TA2 229) | 넓은목근 → 4단계 |
| 승모근 | Posterior region of neck · shoulder(TA2 243 · 139) | 등세모근 → 4단계 |
| 종아리 | Calf · sural region(TA2 164 · 328) | 장딴지근 → 4단계 |

  턱선도 뼈 이름(아래턱뼈 아래모서리)을 빼고 「Jawline」(중)으로 바꿨다. 뼈 지표는 4단계 넘김이다.

## 4. 질문 · open · 결정론 · 수정 금지 — PASS

- **의료진 질문 35** = 근거 약 문자열 4 + 해부학 이름 약 29(수준 「약」 노드 29 와 같음) + 위험 부위 대응 1 + 해부학 이름 1. `doctor_questions` 35 개다.
- **open 0(원장)** · stale 0 이다. 검수 판정은 F-1 때문에 open 1 이다.
- **결정론**: 사본에서 `step3-apply.py` 를 돌리니 `step3-sites.json` · `.md` · `step3-source-fix.md` 가 원본과 바이트가 같다. 사본 `step3-fixture-test.py` 는 **6/6** 이고 `result.json` 이 같다.
- **수정 금지 PASS**: 모두 mtime 이 그대로다.
  - DEC-001 · 002(10-27 09:53) · DEC-003(10-27 13:42)
  - step1-products(10-28 10:37) · step2-families(14:16) · procedure-master-v3(10-27 17:00) · step3-research(14:59)
  - 원천 21개(10-26 22:11)

참고(지적 아님): 넘김 행 「손톱」(taxonomy 꼬리표 「비타민H · 모발/피부/손톱」)의 단계 이름이 「사후관리 문구」로 남아 있다. 옛 문맥(「손톱으로 긁지」) 이름이다. 결정 note 는 「부위 해당 없음」으로 맞고 셈에도 영향이 없다. 마감 때 단계 이름만 바꾸면 된다.

## 5. 닫으려면

1. F-1: 「코조각주사」를 허용 목록에서 빼고, 사전 항목과 결정 한 줄(코 · D-07 · 조각주사 → 2단계)을 더한다. 셈은 176 · 440 · 노드로 154 가 된다. 이렇게 닫으면 open 0 이고, 나머지는 이번 검수에서 PASS 다.
