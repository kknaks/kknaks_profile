---
type: fix-list
id: step3-source-fix
title: "3단계 — DEC-002 근거 표 정정 · 원천 수정 후보"
generated_by: step3-apply.py
---

# 3단계 — DEC-002 근거 표 정정 · 원천 수정 후보

> 결정: _RESUME.md §2 2026-10-28 「3단계 부위 조사(step3-research) 반영 — 전부 추천대로(사용자)」 · 사용자 「추천으로 가자」 (B11 · B12). 이 목록만 낸다 — DEC-002.md · 원천은 고치지 않았다.

## B11 DEC-002 근거 표 정정 2

| # | 대상 | 지금 | 고칠 것 |
|---|---|---|---|
| 1 | DEC-002 얼굴 전체 줄 | 고민 「P5-4 전체미백」 | P5-4 항목은 백옥주사(글루타치온 IV) · 비타민C주사 둘 다 정맥 — 「전체」는 계통 뜻 → 수액 「해당 없음」(DEC-003). 근거에서 뺀다 |
| 2 | DEC-002 전신 줄 | 고민 「P4-3 전신항노화」 · CC 「P4 전신항노화/NAD+수액」 | 계통 뜻 — DEC-003 OQ-306 처리로 「해당 없음」. 몸 표면 「전신」 근거는 시장가 「레이저 제모 (전신)」 하나(v5 — indications 「팔뚝, 복부 등 전신 처짐」은 설명 칸이라 근거에서 뺌) |

## B12 원천 수정 후보 2

| # | 파일 | 키 | 지금 | 고칠 것 | 근거 수준 |
|---|---|---|---|---|---|
| 1 | `anatomy-danger-zones.json` | zones[glabella].botox_specific.target_muscle · zones[nose].botox_specific.target_muscle | 「비근근」이 glabella 에선 Procerus, nose 에선 Nasalis | 한글 근육 이름을 하나씩(Procerus · Nasalis 를 다른 이름으로) — 이름 값은 의료진 확인 | 강(원천 문자열 그대로) |
| 2 | `anatomy-danger-zones.json` | zones[temple].clinical_pearls | 「중측두정맥은 관자궁 상방 약 2cm」 | 「관골궁」 오기인지 확인 | 약(오기로 보임) |

> B12 는 이름 칸 밖(위험 부위 본문) — 부위 원장 셈과 무관, 원천 수정 후보로만 유지(B12 결정 그대로).

## 철회 1 (v5 범위 바로잡기)

| 대상 | 그때 고칠 것 | 철회 이유 |
|---|---|---|
| DEC-002 「노드별 원천 근거」 입가(묶음) 줄 | 본문에 있다 — taxonomy 제품 indications 「입가 주름」 · 「입가주름」 · 「팔자주름 및 입가 거상」 · 「눈가, 입가 등 민감 부위의 주름」 · zones[lips].botox_specific.target_muscle 「입가 주름」 · 「입 주변」 · 「구주위」 · perioral(PMID 33633459). 이름 칸(시장가 · 고민 · 용도 · CC)에는 여전히 0 | v5 범위 바로잡기 — 근거가 설명 문장 칸(indications · target_muscle · 문헌)이라 부위 원천이 아님. DEC-002 「원천에 입가라는 이름이 없다」는 이름 칸 기준으로 맞아 정정 대상이 아니다 |

참고(이미 목록에 있음): `taxonomy.json` auto-M1-1775360538524 (다복스) extracted.indications — 「눈�리 주름(까치발)」 깨진 글자 · 이미 _RESUME 원천 수정 목록 대상 — 다시 올리지 않음
