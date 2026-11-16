---
type: fix-list
id: step4-source-fix
title: "4단계 — 문서 · 3단계 정본 · 원천 수정 후보"
generated_by: step4-apply.py
---

# 4단계 — 문서 · 3단계 정본 · 원천 수정 후보

> 결정: _RESUME §2 2026-10-28 「4단계 기법 조사(step4-research) 반영 — 전부 추천대로(사용자 「추천으로 가자」)」 · J1 안 1 · J2 · + 3단계 「표정근」 · 10-29 J7 G5 · G6 · G7 · G8(K14 흡입 마사지 · N4 also K08 · N8 · N9 · N10 기본 기법). 이 목록만 낸다 — DEC-002.md · step1~3 산출 · 원천은 고치지 않았다.

## DEC 문구 1

| # | 대상 | 지금 | 고칠 것 | 이유 | 누가 |
|---|---|---|---|---|---|
| 1 | DEC-002.md D-02 예시 | 「HA 필러 · 코 · 피하 주입」 | 「HA 필러 · 코 · 주입」(층 속성: 콧등 골막상 · 코끝 연골막상) | J2 — 원천 anatomy nose safe_injection_depth 「골막상 (코뼈 부위) 또는 연골막상 (비첨부)」 · 예시 문구만(결정 내용 그대로) | 코디 → writer |

## 3단계 정본 1

| # | 대상 | 고칠 것 | 이유 | 누가 |
|---|---|---|---|---|
| 1 | step3-decisions.json strings 「표정근」(얼굴 노드 · kind 해부학 이름(속성)) | step3 얼굴 노드 해부학 이름 속성에서 빼기 — 4단계 대상 근육 값(H15)으로 넘김 | 10-28 해부학 결정(대상 근육 → 4단계) · 부위 노드에는 같은 겉자리 의학 이름만 | 코디(3단계 정본 갱신 때) · **반영됨** 2026-10-29 |

## 원천 수정 후보 3

| # | 파일 | 키 | 지금 | 고칠 것 | 충돌 |
|---|---|---|---|---|---|
| 1 | `anatomy-danger-zones.json` | zones[glabella].botox_specific.target_muscle | 비근근 (Procerus) | 눈살근 (Procerus) | X1 |
| 2 | `taxonomy.json` | modality[M8].products[M8-P-3] 설명 | Q-switched Nd:YAG | (허가 모델 CLARITY II LPA — 롱펄스) | X2 |
| 3 | `treatment-sequence.json` | sequence_order[11].categories | M15-LED | M8-LED | X5 |
