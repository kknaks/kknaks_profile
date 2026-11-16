# 이름 칸 17 — 부위 문자열의 원천

정본 `orchestration/work/phub-recommend/step3-decisions.json` `name_fields.fields[]`. 칸 수는 원천 stg 2026-10-26(21파일)을 `scripts/check_sites.py` 로 다시 센 값이다(단위 = 칸 · 합 **1,953** / 원천 문자열 칸 전체 22,749).

결정: `_RESUME.md` §2 10-28 「부위 기준 = 「어디에 맞냐」」 — 부위 원장의 원천은 **이름 칸만**. DEC-002 D-05 ① 「원천이 따로 부른다」의 「원천」 = 시장가 · 고민 분류 · 용도별 · 위험 부위의 **이름**이다.

| # | 파일 | 키 | 무엇 | D-05 ① 갈래 | 칸 |
|---|---|---|---|---|---|
| 1 | `market-pricing.json` | `categories.[].items.[].name` | 시장가 메뉴 이름(「팔자주름 (HA 1cc)」 · 「쿨스컬프팅 (러브핸들 양쪽)」) | 시장가 | 122 |
| 2 | `taxonomy.json` | `problem.[].category` | 고민 메뉴 대분류 | 고민 분류 | 14 |
| 3 | `taxonomy.json` | `problem.[].category_en` | 고민 메뉴 대분류(영문 — 「Body」) | 고민 분류 | 14 |
| 4 | `taxonomy.json` | `problem.[].subcategories.[].label` | 고민 메뉴 중분류(부위 묶음 꼬리표 — 「볼/관자놀이」) | 고민 분류 | 53 |
| 5 | `taxonomy.json` | `problem.[].subcategories.[].items.[].name` | 고민 메뉴 항목 이름 | 고민 분류 | 117 |
| 6 | `taxonomy.json` | `problem.[].subcategories.[].items.[].detail` | 고민 메뉴 항목 꼬리표(「콧대/코끝」 — 평균 7자) | 고민 분류 | 117 |
| 7 | `problem-packages.json` | `problems.[].problem` | 고민 패키지 이름 | 고민 분류 | 14 |
| 8 | `problem-packages.json` | `problems.[].complaints.[].cc_group` | CC 묶음 이름 | 고민 분류 | 115 |
| 9 | `problem-packages.json` | `problems.[].complaints.[].cc` | CC 이름(「수염/가슴/등」) | 고민 분류 | 115 |
| 10 | `problem-packages.json` | `problems.[].complaints.[].cc_detail` | CC 꼬리표 | 고민 분류 | 115 |
| 11 | `problem-combos.json` | `combos.[].problem` | 고민 조합 이름 | 고민 분류 | 8 |
| 12 | `taxonomy.json` | `modality.[].subcategories.[].label` | 용도별(시술 방식) 중분류 | 용도별 | 74 |
| 13 | `taxonomy.json` | `modality.[].subcategories.[].items.[].name` | 용도별 항목 = 단위 시술 이름(「사각턱보톡스」 · 「코조각주사」) | 용도별 | 521 |
| 14 | `taxonomy.json` | `modality.[].subcategories.[].items.[].detail` | 용도별 항목 꼬리표(「등 브라라인」 — 평균 15자 · 문장 아님) | 용도별 | 521 |
| 15 | `anatomy-danger-zones.json` | `zones.[].id` | 위험 부위 zone id(「forehead」) | 위험 부위 | 11 |
| 16 | `anatomy-danger-zones.json` | `zones.[].name_ko` | 위험 부위 zone 이름(「팔자주름」) | 위험 부위 | 11 |
| 17 | `anatomy-danger-zones.json` | `zones.[].name_en` | 위험 부위 zone 이름(영문 「Nasolabial Fold」) | 위험 부위 | 11 |

## 세지 않는 칸

- **설명 문장** — taxonomy `extracted`(작용기전 · 적응증 설명 · 안전) · complications · contraindications · literature-evidence · 위험 부위 본문(근육 · 혈관 · 깊이 · clinical_pearls) · 사후관리. 그 안의 해부 낱말은 부위가 아니다 — 행선지는 SKILL.md §3-3
- **사전 제외 키** — `step3-lexicon.json` `excluded_keys` = `citations.[].title`(논문 제목 · 서지)
- **이름꼴이지만 17칸 밖** — v5 검수가 18칸을 훑어 빠진 부위가 없음을 확인했다(synergy `links.target` 「코성형」 1회 — 코 노드는 이미 근거 있음): patient-education `patient_name` · pih-risk `name` · `subcategory` · problem-combos `packages.name` · procedure-comparison `procedures.name` · `title` · `subtitle` · combo-recipes `name` · `subtitle` · treatment-sequence `common_combos.name` · problem-packages `combos.name` · `procedures.name` · taxonomy `modality.products.name` · `modality.category_en` · post-procedure-timeline `name` · market-pricing `categories.name` · synergy `target` · treatment-optimization `plan_name`

## 칸을 더하는 조건

새 원천 파일 · 새 키가 생겼을 때만 본다. **「원천이 그 자리를 이름으로 부르는 칸」**(메뉴 · 분류 · 시술 · zone 이름 · 짧은 꼬리표)이면 더한다. 문장이면 더하지 않는다.
꼬리표(detail) 칸은 이름 칸이다 — 평균 7 ~ 15자 꼬리표이지 문장이 아니다.
칸을 더하면 결정 파일 `name_fields.fields[]` 한 줄(`file` · `key` · `what`) — 사람 승인 항목이다(SKILL.md §4).
