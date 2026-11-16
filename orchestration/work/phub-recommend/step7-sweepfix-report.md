---
title: 7단계 전수 눈검 반영 보고(R23 ~ R27 · 판단 ① ~ ③)
date: 2026-10-30
author: researcher
brief: phub-recommend-step7-sweepfix-brief.md
review: review-step7-sweep.md · .json
---

# 7단계 전수 눈검 반영

## 결과
- 검수 항목 다시 셈(`review-step7-sweep-recount.py` — 항목마다 원인 조건을 지금 산출에 다시 대 봄 · 남은 원인의 등급으로 판정): **이상함 105 → 0 · 확인 필요 36 → 1**
- 남은 1 = `C:RC-RE-R7:1` 「레이저 토닝 + 재생」의 M5(얼굴 전체 엑소좀 · PRP · 엑소좀 도포). 두피 2(이상함 원인 C3)는 빠졌고, 검수가 「확인 필요」로 단 원인 C7 「재생」을 PRP 로 볼지만 남음 — 승인 규칙 밖(이름 조각에 PRP 없음)이라 손대지 않음
- 엣지 537 → 427(R27 합침 60 묶음 · CC 170행) · 좁혀진 엣지 72 · 바뀐 조합 구성 169(조합 63)
- open 5단계 0 · 7단계 0 · 8단계 0 · 결정론 cmp 5 · 7 · 8(5단계 md 는 고정 시험 절이 정본 폴더에서만 붙음 — 같은 폴더 두 번은 같음 · json 같음)
- 고정 시험 5단계 25/25 · 7단계 38/38(W1 ~ W9 새로 · G2 기대값에 판단 ① 결정 open 추가) · 8단계 49/49
- 스킬 concern-check · unit-check · relation-check errors 0 · `semantic-build.py` · `silver-graph-build.py` 재생성
- 8단계 끝점 바뀜 81(계열만 13) — 7단계 ③ 재사용분

## 규칙(결정 파일 rules · site_rules)
| 규칙 | 무엇 | 엣지 셈 |
|---|---|---|
| R24 | 이름 조각 · 레시피 subtitle · 제품 칸 괄호/「/」 안 낱말(고정 키 낱말 포함) — combo-recipes 도 problem-combos 처럼 | 「PDL(V빔)」 → U5-141 · 「니들RF + PRP」 → U5-020 · 「레이저 토닝」 → U5-023 |
| R23 | 다른 고민 용도(5단계 purposes)가 박힌 단위 시술이 섞인 여럿 → 고민 · 목적 이름 낱말에 든 용도만 · 없으면 계열만 | 18 |
| R22 + 판단 ① | 영역 없는 피부 고민 기본 영역 얼굴(P4 · P5 · P6 · P7 · P9 · J10) · 튼살 P9-4 바디 · P14 기타는 기본 없음 | md 셈 |
| R25 | 두피 단위 시술은 고민 영역에 두피가 있을 때만 | 5(나머지는 판단 ① 영역으로 먼저 빠짐) |
| R26 | 흉터 고민에 필러 단위 시술 없음 → 필러 계열만 + 원천 질문 | 3 · 원천 질문 1(4곳) |
| 판단 ② | 필러만 여럿 남은 「후보 전부」 = 그대로 + 「후보 여럿(필러 부위 못 정함 · 판단 ②)」 | 조합 |
| R27 | ③ (갈래 앵커 × 원천 시술 · 계열 · 단위 시술 · 앵커 부위) 하나 · CC 는 source_ids · evidence.ccs · 원천 수정 후보 60 | 110 엣지 줄어듦 |
| 판단 ③ | 5단계 결정 `device_synonym_extra` — 「엑셀 V」(M8-4-2) 동의어에 U5-138 | U5-138 이 P8-2 엣지 3에 |

대상 경로 = `site_rules.narrow_sources`(① ③ ④ ⑤) + 추천 조합 구성. ⑥ ⑦ ⑧ 은 단위 시술 직결이라 거르지 않음.

## 해석해 정한 것(보고)
- R23 「못 좁히면 계열만」 = 섞인 다른 용도가 있을 때 맞는 용도가 하나도 없으면 계열만. 「제품으로 좁힘」(브랜드 → 계열 전부)도 대상으로 넣음 — 켈로이드 보톡스(제품 보톡스/나보타)가 그대로 11개 남아서
- 판단 ① 「피부 고민」 = P4 · P5 · P6 · P7 · P9 · J10. P14 기타(다한증 · 점/사마귀 · 피부질환)는 넣지 않음 — 다한증은 겨드랑이 · 손 · 발(바디)이라 얼굴 기본값이면 틀림
- R23 으로만 비면 「→ 계열만」, 영역 · 두피 · 흉터로 비면 「→ 이 부위 단위 시술 없음 · 계열만」

## 바꾼 파일
- 5단계: `step5-apply.py`(device_synonym_extra) · `step5-decisions.json`(키 추가) · `step5-units.json` · `.md`
- 7단계: `step7-apply.py` · `step7-decisions.json`(rules R23 ~ R27 · 판단 ① ~ ③ · site_rules 키 추가) · `step7-fixture-test.py` · `step7-fixtures/cases.json` · `result.json` · `step7-concerns.json` · `.md` · `step7-source-fix.md` · `step7-origin-questions.md`
- 8단계: `step8-apply.py`(CC7 을 source_ids 마다 색인) · `step8-relations.json` · `.md`
- 스킬: concern-check `check_concerns.py`(③ 합친 CC 행 셈 · 판단 ① 기본 영역 · R25 · R26) · references 2곳
- 페이지: `semantic-*` · `silver-graph.html` 재생성 · 다시 셈 스크립트 `review-step7-sweep-recount.py`

## 추가(10-30) — R24 레시피 설명 문장 칸 · RC-RE-R7 「재생」 PRP
- 결정 `site_rules.recipe_text_fields` = analogy · patientExplanation · R24 문장 보강. 레시피는 이름 · subtitle 로 못 좁히면 analogy 「X = 비유」의 X 와 patientExplanation 괄호 안 · 영문 낱말로 좁힘
- 같은 성격 전수(레시피 7개): 좁혀진 조합 4 — R7 M5 → U5-020 얼굴 전체 PRP(「PRP」) · R1 · R2 M9 → 얼굴 전체 · 턱선 HIFU(「HIFU」) · R4 M9 → HIFU + 고주파(「HIFU/RF」). R3 · R5 · R6 은 이미 이름으로 좁혀졌거나 설명 낱말이 계열 전부(보톡스 · 필러 · 스킨부스터)
- 목적 연결: 레시피 anchor 에 `purposes`(이름 조각 → R12 · R14 · R16) 추가 — R7 「재생」 → 목적:재생 · R1 「리프팅 기본」 → 목적:리프팅. concern anchor 는 그대로(영역 셈 안 바뀜)
- 다시 셈: 이상함 0 · 확인 필요 0 · open 5 · 7 · 8 = 0 · cmp 같음 · 고정 시험 7단계 39/39(W10) · 5단계 25/25 · 8단계 49/49 · concern-check · relation-check errors 0 · 8단계 주장 바뀜 0 · semantic-build · silver-graph-build 재생성
