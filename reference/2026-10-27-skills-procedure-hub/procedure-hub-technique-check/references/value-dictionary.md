# 값 사전 — 속성 값은 여기 안에서만

출처: `step4-decisions.json` `dictionaries` · `pulse_by_medium` · `site_layer_split` · 산출 `step4-techniques.json` `unit_procedure_attrs`(판 v1). 속성은 단위 시술 키를 가르지 않는다(J1 안 1).
점검 스크립트는 표현 행 `layers` · `muscles` · `attach` · technique_hint `pulse_mode` · `modes` · `ablative` · `pulse_by_medium` 이 이 사전 안인지, 대상 근육 · 층 나눔 부위가 3단계 노드인지 본다. 새 값이 필요하면 **사전 한 줄 추가가 먼저**(최종 판단).

## 1. 단위 시술 속성(키 밖)

- **layer(층 · 깊이)** 13: 표피 · 진피 · 피하 · 피하-근막 경계(SMAS 상방) · Sub-SMAS · 근육 내 · 골막상 · 연골막상 · 심부측두근막 심층 · 점막하 · 정맥 내 · 병변 내 · 피하 지방층
- **tool_form(도구 형태)** 3: 롤러형 · 스탬프형 · 전동 — 더마롤러 · 더마스탬프 · MTS롤러(OQ-311)
- **peel_depth(박피 깊이)** 3: 얕은 · 중간 · 깊은
- 단위 시술 속성 칸: safe_layers(+ constraint_text) · target_muscles · landmarks · tool_form · peel_depth · application · evidence

### 대상 근육 17 — 키 = 영문 · 한글 = KMA · 원천 표기 = `source_label`

| 키 | KMA 한글 | 원천 표기 | 부위(3단계 노드) | 근거 |
|---|---|---|---|---|
| Frontalis | 이마근(전두근) | 전두근 (Frontalis) | 이마 | zones forehead target_muscle |
| Corrugator supercilii | 눈썹주름근(추미근) | 추미근 (Corrugator supercilii) | 미간 | zones glabella target_muscle |
| Procerus | 눈살근 | 비근근 (Procerus) | 미간 | zones glabella target_muscle — 원천 「비근근」 표기(코 Nasalis 와 같은 표기 · 충돌 X1) |
| Temporalis | 관자근(측두근) | 측두근 (Temporalis) | 관자놀이 | zones temple target_muscle 「이갈이/사각턱 보조」 |
| Orbicularis oculi | 눈둘레근(안륜근) | 안륜근 (Orbicularis oculi) | 눈가 · 눈밑 | zones periorbital target_muscle 「까마귀발, 눈밑 주름」 |
| Nasalis | 코근 | 비근근 (Nasalis) | 코 | zones nose target_muscle 「bunny lines」 — 원천 「비근근」 표기(충돌 X1) |
| Depressor septi nasi | 코중격내림근 | depressor septi nasi | 코끝 | zones nose target_muscle 「코끝 처짐(depressor septi nasi)」 |
| Levator labii superioris | 위입술올림근(상순거근) | 상순거근 (Levator labii superioris) | 팔자 | zones nasolabial target_muscle 「NLF 보조 치료」 |
| Masseter | 깨물근(교근) | 교근 (Masseter) | 사각턱 | zones cheek · jawline target_muscle 「사각턱」 · step3 handoff_note 사각턱 |
| Zygomaticus | 광대근 | 광대근 (Zygomaticus) | 잇몸 | zones cheek target_muscle 「gummy smile」 |
| Orbicularis oris | 입둘레근(구륜근) | 구륜근 (Orbicularis oris) | 입술 · 입가 | zones lips target_muscle 「lip flip, 입가 주름」 |
| Mentalis | 턱끝근(이근) | 이근 (Mentalis) | 턱끝 | zones chin target_muscle 「턱 딤플(peach pit chin)」 |
| Platysma | 넓은목근(광경근) | 광경근 (Platysma) | 턱선 · 목 | zones jawline · neck target_muscle 「턱선 리프트 · platysmal bands, 목 주름」 · step3 handoff_note 목 |
| Depressor anguli oris | 입꼬리내림근(구각하제근) | DAO(구각하제근) | 입꼬리 | zones chin tissue_data.dao_coverage · notes 「DAO 보톡스 시 이신경 손상 주의」 |
| Trapezius | 등세모근 | (원천 이름 칸 「승모근」) | 승모근 | step3 handoff_note 승모근(10-28 부위 이름 2벌 결정) |
| Gastrocnemius | 장딴지근 | (원천 이름 칸 「종아리」) | 종아리 | step3 handoff_note 종아리 |
| Musculi faciei (mimetic muscles) (묶음) | 표정근(얼굴근육) | 표정근 (원천 이름 칸 — 시장가 「안면 EMS (표정근 강화)」) | 얼굴 | step3 이름 칸 「표정근」(market-pricing 「안면 EMS (표정근 강화)」) — 낱 근육이 아니라 얼굴 표정근 묶음 · 10-28 해부학 결정(대상 근육 → 4단계) · 브리프 추가 |

대상 근육은 원천 행(`muscles`) · 근거 속성(`attach`) · 넘겨받은 것(`handoffs[].muscles`) 중 하나가 있어야 선다(없으면 「근거 없는 대상 근육」). 표정근은 낱 근육이 아니라 묶음(`group: true`) — 3단계 이름 칸 「표정근」(시장가 「안면 EMS (표정근 강화)」)을 4단계가 받았다(H15).

### 부위 × 층 — `safe_layers`(주입 K01)

원천 `anatomy-danger-zones.json zones[].safe_injection_depth` → 3단계 `danger_zone_mapping` 으로 부위 노드. 「근거만」 = 층 값 없이 근거 속성(`attach[{layer, site}]`)만 붙은 부위.

| 부위 | zone | 층 | 제약 · 지표(원문) | 근거 속성 수 |
|---|---|---|---|---|
| 이마 | forehead | 골막상 | — | 1 |
| 미간 | glabella | 골막상 | 피하 금지(원문 「절대 피하층 주사 금지」) | 0 |
| 관자놀이 | temple | 심부측두근막 심층 · 골막상 | — | 1 |
| 눈가(묶음) | periorbital | 골막상 | 안와연 외측(원문 지표) | 0 |
| 코(묶음) | nose | 골막상 · 연골막상 | 골막상 = 코뼈 부위(콧등) · 연골막상 = 비첨부(코끝)(원문) — 코(묶음)은 둘 다 | 0 |
| 팔자 | nasolabial | 피하 · 피하-근막 경계(SMAS 상방) | — | 0 |
| 볼(묶음) | cheek | 골막상 · 피하 | 골막상 = 관골부(광대) · 피하 = 협부(볼) · Sub-SMAS 주의(원문) | 0 |
| 입술 | lips | 진피 · 점막하 | vermillion border 진피 내 또는 점막하(원문) | 0 |
| 턱끝 | chin | 골막상 | 이신경공 외측 피할 것 → 8단계 신경 주의(site_caution) | 0 |
| 턱선 | jawline | 골막상 · 피하 | 하악연 위/아래 구분(원문 지표 → 주입 지표 속성) | 0 |
| 목(묶음) | neck | 근육 내 · 진피 | 광경근 내 또는 피내(진피층)(원문) | 0 |
| 콧등 (← 코(묶음) 나눔) | nose | 골막상 | 원문 「골막상 (코뼈 부위)」 — 코뼈 = 콧등 | 0 |
| 코끝 (← 코(묶음) 나눔) | nose | 연골막상 | 원문 「연골막상 (비첨부)」 — 비첨 = 코끝 | 1 |
| 눈밑 | — | 근거만 | — | 1 |
| 눈가 | — | 근거만 | — | 1 |
| 코 | — | 근거만 | — | 2 |
| 볼 | — | 근거만 | — | 4 |

**층 나눔(`site_layer_split`)** — 원천이 한 zone 안에서 자리를 나눠 층을 따로 적은 곳만:

```json
{
 "zone": "nose",
 "group_site": "코(묶음)",
 "group_layers": [
  "골막상",
  "연골막상"
 ],
 "splits": [
  {
   "site": "콧등",
   "layers": [
    "골막상"
   ],
   "basis": "원문 「골막상 (코뼈 부위)」 — 코뼈 = 콧등"
  },
  {
   "site": "코끝",
   "layers": [
    "연골막상"
   ],
   "basis": "원문 「연골막상 (비첨부)」 — 비첨 = 코끝"
  }
 ],
 "source": "anatomy-danger-zones.json zones[nose].safe_injection_depth 「골막상 (코뼈 부위) 또는 연골막상 (비첨부)」",
 "decided_by": "_RESUME §2 10-28 J2 · 브리프"
}
```

같은 부위에 층이 「또는」으로 둘인 곳 5(관자놀이 · 팔자 · 입술 · 턱선 · 목 — 기록 §3-3)은 층 둘을 그대로 둔다 — 층을 노드로 두면 한 부위 주입이 둘로 갈린다(J1 안 1 의 이유).

### 주입 지표 — `landmarks`(넘겨받은 것)

| 부위 | 지표(원문) | 넘김 |
|---|---|---|
| 사각턱 | 아래턱뼈각(angulus mandibulae) | H05 |
| 턱선 | 아래턱뼈 아래모서리(mandibular border) — zones jawline 「하악연 위/아래 구분」과 같은 지표 | H09 |

## 2. 장비(제품) 속성

- **pulse_mode(펄스 방식)** 3: 피코초 · Q스위치(나노초) · 롱펄스
- **ablative(박피 여부)** 2: 박피성 · 비박피성
- **modes(가능 방식)** 1: 프락셔널 → K04b(S6 — 가능 방식(장비) → K04b 프락셔널과 잇는 조건)
- 장비 속성 칸: pulse_mode · modes · ablative · electrode(모노폴라 · 바이폴라) · energy(RF · 캐비테이션) · injector(멀티니들) · delivery(이온도입 · 전기천공 · 초음파) · thread_design · suction · cooling

매질별 펄스 방식(`pulse_by_medium` — 매질은 2단계 하위 계열 정본):

| 매질 | 낼 수 있는 펄스 |
|---|---|
| 알렉산드라이트 레이저 | 롱펄스 · 피코초 |
| 엔디야그 레이저 | Q스위치(나노초) · 롱펄스 · 피코초 |
| PDL | 롱펄스 |

technique_hint 25행(step2 원문 hint → 장비 속성)은 `step4-techniques.md` 「technique_hint → 장비 속성」 표. 보조 매질에만 걸리는 펄스는 `pulse_scope`(지금 1행 — 셀렉V `auto-M8-1775364106103` Q스위치(나노초) = 「보조 하위 계열 엔디야그 레이저」).
