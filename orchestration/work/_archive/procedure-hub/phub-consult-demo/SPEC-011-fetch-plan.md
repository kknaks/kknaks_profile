---
type: spec
id: SPEC-011
title: "상담 가져오기 계획 — 1차 이해 JSON 계약(fetch) + 질문 꼴 × 허브 가져오기 규칙표 + 2차 결정론 읽기"
status: draft
product: procedure-hub
feature: phub-consult-demo
version: 0.1.2
created_at: 2026-11-23
updated_at: 2026-11-23
tags:
  - product/procedure-hub
  - feature/phub-consult-demo
  - doc/spec
  - status/draft
links:
  decisions:
    - "코디 발주 task_5c73e0d2395d(사용자 승인 11-23 「응」) — 1차 소넷 JSON → 2차 결정론 읽기 → 3차 소넷 답 · `--resume` 유지 · 출력 안 줄임 · 턴당 상한 고정 금지 · 안전 · 명시 대상 늘"
    - "token-cause-report.md §3 · §5 — Jev 거르기 넣지 않음(인용 후보 중앙 0.74 vs 인용 없는 후보 0.78 · 못 가름)"
    - "review-spec-011.md(FAIL · P1 4 · P2 9) → spec-011-fix1-task.md — 0.1.1"
    - "review-spec-011-r2.md(FAIL · P1 1 · P2 4) → spec-011-fix2-task.md(코디 결정: P1-5 = (가) G2b 뺌 · 셈은 시대로 나눔) — 0.1.2"
  sources:
    - "orchestration/work/phub-consult-demo/fetch-plan-report.md(이 스펙의 측정 · 수치 정본 · 0.1.1 다시 셈 §3-5) · fetch-plan/out/*"
    - "orchestration/work/phub-consult-demo/token-cause-report.md · token-cause/out/*(원인 · 코드 자리)"
    - "clinic_chat 워크트리 phub-consult-demo(읽기만) — clinic_chat/consult/{understand,verify,kinds_pick,material,material_read,kos_block,turn,ledger}.py · walk/{ranges,calls,front,material,fold}.py · prompts/consult.json(pick 0.5.0-draft)"
    - "SPEC-010-consult-myeongdong.md(0.3.1 — LC1 ~ LC9 · TT · 장바구니 R5 자리)"
---

# SPEC-011 상담 가져오기 계획 0.1.2

## 0. 목적

상담 답 입력이 커지는 까닭 가운데 「## 자료」 는 「허브에서 무엇을 · 어디까지 가져오나」 를 앱이 정하지 못해 생긴다(token-cause-report §2-4). 예를 들면 이렇다.
- KD9 가 개요에 네 종류를 덧붙인다.
- 부위만 말한 턴이 기본 묶음으로 부위 전체의 고민 행을 읽는다(ecc6 「얼굴에」 194k).
- 명동점에 없는 하위 케이스 · 제품을 전부 읽는다.

이 스펙은 그 판단을 **1차 이해 호출(소넷)의 JSON 칸**으로 옮긴다. 2차는 판단 없이 그 칸대로만 읽고, 3차 소넷은 그 자료로 답한다.

**측정**(0.1.2 · 초안 프롬프트 r4 · 2차 규칙 **5판** · fetch-plan-report §3-6)은 시대로 나눈다. **머리 수는 지금 시대다.**
- 시대는 장부 줄의 `trace.front.kinds_by` 로 가른다.
  - `jev` = 11-18 Jev 종류 고르기 판 · 이해 호출 기록 없음.
  - `understand` · `default` = 지금 앱(이해 호출 판)이다.

| 모음 | 시대 | 턴 | 「## 자료」 | 빠짐 | 상세 잃음 | lineup 이름만 |
|---|---|---:|---|---:|---:|---:|
| **표본**(대화 10) | 지금(understand 33 · default 10) | 43 | 697,892 → 260,196 (**−62.7%**) | **0** / 276 | **7** | 17 |
| 표본에서 ecc6 「얼굴에」 두 턴(T2 · T3) 뺌 | 지금 | 41 | 306,525 → 234,486 (**−23.5%**) | 0 | 7 | 17 |
| **표본 밖**(지금 시대 장부 · 자료 · 인용 있는 턴 전부) | 지금(understand 9 · default 2) | 11 | 28,432 → 23,438 (**−17.6%**) | **0** / 49 | 0 | 0 |
| (참고) 표본 밖 Jev 시대 | jev | 8 | 34,969 → 31,134 (−11.0%) | 1 / 24 | 0 | 0 |

- **빠짐**은 답이 인용한 줄이 아예 안 실린 것이다.
- **상세 잃음**은 인용 줄이 「이름만」 으로 실린 것이다(lineup 빼고). **lineup 이름만**은 목록 이름이 답의 전부인 줄이다.
- **Jev 시대 빠짐 1** 은 44b2 T2 「사각턱인데 ?」 n1 이다. 후보 「사각턱보톡스」 의 overview 로, 그 줄은 Jev 점수 1위(`by: top`)로 읽혔다.
  - 지금 앱의 고민 턴에는 overview 줄이 실리지 않는다(표본 고민 턴 20/20 이 0).
  - 그러니 이 빠짐은 지금 앱에서 생기지 않는 **시대 차이**다. 0.1.1 의 G2b(고민 입구 + overview)는 뺐다.
- 앞 턴 줄을 인용한 31 개는 이렇다.
  - 근원 턴에서 전체로 실림 28.
  - 이름만 3: 이 가운데 1 은 다음 턴에 G7 로 상세가 다시 실리고, 2 는 이름만 그대로다.
- **맞추는 데 안 쓴 턴은 아직 없다.** 표본 43 과 지금 시대 밖 11 은 모두 규칙을 고치는 데 쓰였다. 11-23 이후 새 장부 턴은 WP 완료 조건에서 코드 워커가 만든다(§8).

## 1. 사용자 결정(다시 묻지 않음)

| # | 결정 |
|---|---|
| UD1 | 구조 = 1차 소넷이 질문 의도를 JSON 으로 → 2차가 그 JSON 대로만 허브에서 가져옴 → 3차 소넷이 그 자료로 답 |
| UD2 | 2차는 판단 없는 결정론이다. Jev 거르기는 넣지 않는다 |
| UD3 | `--resume` 는 둔다(앞 대화는 대부분 캐시 읽기). 끊는 안은 이 스펙에 없다 |
| UD4 | 출력은 줄이지 않는다. 출력 토큰은 재서 기록만 한다 |
| UD5 | 턴당 상한을 고정하지 않는다. 안전(부작용 · 금기 · 회복 · 회피)과 손님이 직접 말한 대상은 늘 가져온다. 명동점 밖 하위의 안전 줄도 전체로 싣는다(r3_rules4 「밖 안전 줄 이름만」 −64.4% 는 UD5 로 채택 안 함) |

## 2. 비용 몫(기록 · fetch-plan-report §1)

**무게 가정**은 API 표준 단가 비이고, 입력 1 을 기준으로 잡았다: input 1 · cache_creation 1.25 · cache_read 0.1 · output 5. 지금 시대 답 79 턴 · 이해 70 호출로 셌다.

| 몫 | 답 | 이해 |
|---|---:|---:|
| cache_creation | **59.2%** | 기록 없음 |
| cache_read | 11.3% | 9.0% |
| output | 16.2% | 4.3% |

- 이해 호출 캐시는 된다(67/70 캐시 읽기 · 같은 대화 안 시스템 글 바뀜 0).
- 이해 호출의 캐시 쓰기 토큰은 앱이 남기지 않는다(LG4 로 더함 · WP-1).
- 이 스펙을 따르면 이해 출력이 턴 중앙 97 → 158 토큰(+61 · r4 64 호출)이 된다. 시스템 글은 38,854 바이트(+3.3 KB)다(실측).

## 3. 1차 이해 JSON 계약

### 3-1. 칸

지금 출력(`prompts/consult.json` pick 출력 꼴 · `verify.parse` · `verify.verify`)에 `fetch` 객체 하나를 더한다. 나머지 칸은 그대로다.

```json
{"targets":[...],"kind":"new","sites":["SITE-000"],"withdraw":[],"exclude":[],"pairs":[],"kinds":[],"out":false,
 "country":null,"topic":{"move":"continue","to":null},
 "fetch":{"about":"targets","kinds":[],"layers":"sub","scope":"branch","lineup":"none"}}
```

| ID | 칸 | 값 | 뜻 | 빈 값 · 깨진 값일 때 | 상태 |
|---|---|---|---|---|---|
| JC1 | `fetch.about` | `targets` · `topic` | **대상**. `targets` = 이번 말의 대상(targets). `topic` = 부위만 말하거나, 짧게 이어 좁히거나, 이름 없이 앞 답 목록을 좁히는 턴(「그중에서 뭐가 좋아」). 지금 주제(SPEC-010 TT)의 고민 · 진료항목에 대해, 이번 턴 `sites` 로 거른다 | `targets` | 제안(측정 표본 43/43 · 밖 19/19 맞음) |
| JC2 | `fetch.kinds` | 종류 코드(지금 `kinds` 와 같은 14 개) | **종류**. 가져올 정보. 지금 `kinds`(말이 묻는 것)에 꼴 규칙(FR 표)으로 더한 것이다. 예: 「전반 설명」 = overview · mechanism · indication · outcome · lineup | `kinds` 그대로. 둘 다 [] 면 G2 | 제안 |
| JC3 | `fetch.layers` | `self` · `inherit` · `sub` | **층**. `self` = 그 대상 자체, `inherit` = + 위 계열에서 물려받음, `sub` = + 하위 시술 · 케이스 · 제품. **명동점 진료항목에 닿는 하위는 이 값과 무관하게 늘 읽는다**(G4). 이 칸이 가르는 것은 물려받음 줄과 명동점 밖 하위 줄(빼기 ↔ 이름만)이다. **측정(r4 · 62 턴 · `layers_check.py`)**: 1차가 고른 값은 61 턴 `sub` · 1 턴 fetch 빠짐(기본 `sub`)으로, 62/62 가 결국 `sub` 다. 같은 JSON 에서 이 값만 바꾸면 17 턴의 토큰이 달라지고 빠짐이 생긴다(`self` 25 · `inherit` 7). 그러니 고른 값이 늘 `sub` 인 한 이 칸은 결과를 바꾸지 않고, 다른 값을 고르면 빠짐만 낸다 | `sub` | 제안 — **2차는 `sub` 로 고정하고 칸을 없애는 쪽을 추천**(이해 출력 줄임). WP-1 에서 없앤 프롬프트로 다시 재 확인 |
| JC4 | `fetch.scope` | `branch` · `all` | **범위**. `branch` = 명동점 진료항목에 닿는 것은 다 읽고 밖은 **이름만**. `all` = 밖도 다 읽는다 | `branch` | **사용자 결정 필요 DQ1** |
| JC5 | `fetch.lineup` | `none` · `names` · `detail` | **라인업**. `names` = 하위 목록 줄의 이름 칸만, `detail` = 줄 전체 | `none`(lineup 종류가 있으면 `names`) | 제안 |
| JC6 | 부위 필터 | (새 칸 없음) | 이번 턴 `sites`(규칙 7)를 그대로 쓴다. 초안 r3 의 `fetch.site_filter` 는 43/43 턴에서 `sites` 와 같아 r4 에서 없앴다 | — | 제안 |

검증(`verify.verify` · VF 꼴)은 이렇다.
- 값이 enum 밖이면 기본값으로 바꾸고, 장부 `consult.fetch.fixed[]` 에 칸 이름을 남긴다.
- `fetch.kinds` 의 모르는 코드는 버린다.
- `fetch` 가 없으면 전부 기본값이고 `consult.fetch.from = "default"` 다. r4 64 호출 가운데 1 이 그랬다(a578 T5). 결과 빠짐은 0 이었다.

### 3-2. 프롬프트 규칙(초안 · `fetch-plan/out/draft_pick_r4.json` — 측정에 쓴 글 그대로)

- 출력 꼴 줄을 위 꼴로 바꾼다(`site_filter` 없음).
- 규칙 20 ~ 20-6 을 더한다.
  - 20 은 fetch 의 뜻이다.
  - 20-1 about · 20-2 kinds(꼴 규칙) · 20-3 layers · 20-4 scope · 20-5 lineup 이다.
  - 20-6 은 「layers 는 scope = all 일 때만 · 부위는 sites」 다. 앞 절(「scope = all 일 때만」)은 검수 지적을 옮긴 것인데, 실측(JC3)과 맞지 않는다. WP-1 은 이 줄과 `layers` 칸을 함께 없애는 쪽으로 재 본다.
- 회차별로 고친 것(fetch-plan-report §3-2 · §3-5):
  - r2:
    - 「몇 샷 · 몇 회 · 용량 · 가격」 → offer.
    - layers 기본은 `sub` 다.
    - 앞 답에서 명동점에 없다며 보인 것을 이어 물으면 `all` 이다.
  - r4:
    - 꼴이 겹치면 kinds 합집합 · lineup 은 가장 넓은 값 · scope 는 `all` 이 이긴다.
    - 「그중에서 + 이름 없음」 → `topic`.
    - 「명동점에 뭐 있어」 → `branch`.
- **남은 오답 2 건**(FR13b 02af T3 · FR14 dc78 T4)은 r3 · r4 에서 모두 `branch` 였다(0/2).
  - 까닭: 1차는 어떤 시술 · 제품이 명동점에 없는지 모른다. 입구 목록에 명동점 표지가 없고, dc78 T3 앞 답에도 「명동점에 없다」 는 말이 없었다.
  - 영향: 02af T3 은 빠짐 0 · 상세 잃음 0, dc78 T4 는 상세 잃음 2 다.
  - 막을 길은 WP-1 에서 잰다: 입구 목록에 「명동점 없음」 표지를 다는 것이다.
  - 2차 쪽 대안(같은 대상 follow 면 앞 턴 이름만 주인을 상세로 · 규칙 7 · 8판)도 재 봤다. 상세 잃음은 7 → 5 로 줄지만 감소가 62.1% → 58.5% 로 줄어(03b8 T6 +15k) 채택하지 않았다(리포트 §3-5).

### 3-3. 지금 칸과의 대응 · 사라지는 것

| 지금 | 자리 | 이 스펙 뒤 |
|---|---|---|
| KS1 `kinds` = yes | `kinds_pick.py:35` | 그대로. JC2 의 바탕 |
| KS3 입구가 이름 댄 종류(`entry`) | `kinds_pick.py:36-39` | 그대로(고민 → indication · 효과 → outcome 등). G2 가 이 값을 쓴다 |
| **KS5 · KD9**(개요가 yes 면 mechanism · indication · outcome · lineup 덧붙임) | **상담 경로 `kinds_pick.py:40-42` 만** | **상담 경로에서만 끈다.** 「전반 설명」 꼴은 1차가 JC2 로 그 다섯을 직접 고른다. **`walk/front.py:46 KD9_SET` · `:101-104` KD9 · 그것을 쓰는 상담 밖 걷기 경로(`report.py:356 · :406` 등)는 그대로 둔다**(상수를 지우지 않음) |
| KS6 기본 묶음(입구가 종류를 말하지 않음) | `kinds_pick.py:45-51` | `about = targets` 일 때 그대로. `about = topic` 이면 G6 |
| **KS7 범위 「강함」**(`STRONG_BY = yes · entry · kd9`) · KD11 `offered` | `kinds_pick.py:18` · `:52-66` | KS5 를 끄면 `STRONG_BY` 에서 kd9 몫이 사라진다. 개요 턴에서 KD11 갈래가 달라질 수 있다: 「강한 범위의 안 고른 기본 종류 → `offered`(안 읽음)」 가 늘고 `default`(읽음)가 준다. **표본 측정은 이미 실린 줄에서 빼기만 해서 이 변화를 보지 못했다** → WP-2 완료 조건 「offered 목록 전후 비교」 |
| `ROLES_TARGET`(자기 · 물려받음 · 하위 셋 늘) | `walk/ranges.py:16` · `walk/calls.py:162 _facets` | JC3 · JC4 로 바뀐다. 명동점 닿는 하위 = 늘. 밖 = `scope` 대로 |
| `_site_filters`(부위 입구 필터) | `walk/calls.py:137` | `about = topic` 일 때 지금 주제 대상에도 건다 |
| LC5 덧붙이기(명동점 블록 진료항목 다시 안 보냄) | `kos_block.py:47` | 그대로(명동점 블록은 이 스펙 밖) |
| 자료 덧붙이기 `seen_lines` · `sent` | `consult/material.py:173-179 renumber` · `consult/ledger.py:237-242`(`c.sent` 갱신) | **바뀐다(G7)**: 이름만 실은 gid 는 `sent` 에 넣지 않는다 |

## 4. 질문 꼴 × 가져오기 규칙표

꼴은 장부 실제 말 92 턴을 전수로 나눈 것이다(fetch-plan-report §2). 「장부 0」 꼴은 측정 근거 없이 규칙만 둔다.

**범위 기본은 「명동점 닿는 것은 다 · 밖은 이름만」** 이다(DQ1).
- 11-16 「폭은 빠짐없이」 원칙과는 이렇게 맞춘다. **폭(어떤 것이 있나 · 이름)은 밖까지 빠짐없이** 싣고, **깊이(상세 행)는 명동점에 닿는 것만** 싣는다.
- 측정에서 밖을 빼면 빠짐이 14 였고, 이름만으로 두면 0 이었다.

**꼴이 여럿이면**(예: 「턱에 보톡스 맞고 싶은데 효과랑 부작용좀 알려줘」 = 고르기 + 효과 + 부작용) 이렇게 합친다.
- kinds 는 합집합이다.
- lineup 은 가장 넓은 값이다(detail > names > none).
- scope 는 `all` 이 이긴다.
- about 은 이름 있는 대상이 있으면 `targets` 다.

| ID | 꼴(장부 턴) | 예 | about | kinds(JC2) | layers | scope | lineup | 측정(r4 · 5판) |
|---|---|---|---|---|---|---|---|---|
| FR1 | 고민(+부위) (26) | 「얼굴이 자꾸 빨개져요」 | targets | [] → G2(KS3 indication) | sub | branch | none | 지금 시대 빠짐 0. 장부 꼴 F20 「이해 실패 · 대상 없음」 6 턴(「사각턱인데 ?」 · 「턱살이 너무 많아」 등 · 44b2 · 9c9a)은 **Jev 시대 장부라 대상 칸이 없다.** 지금 시대에서는 FR1 고민이다(r4 1차는 고민 · 부위로 잡음) |
| FR2 | 부위만 · 첫 턴 (0) | 「턱이요」(주제 없음) | targets | [] → G2(속성 시작 = overview · indication) | sub | branch | none | 장부 0 |
| FR3 | **부위만 · 주제 있음** (5) | 「얼굴에」 | **topic** | [] | sub | branch | none | ecc6 T2 −94% · T3 −93% · 빠짐 0 |
| FR4 | 시술 · 제품 이름만 (2) · 고르기 (15 가운데 이름 있음) | 「써마지 받아보고 싶어」 · 「그중에서 소프웨이브, 써마지, 울쎄라만」 | targets | [] → G2(KS6 시술 = overview) | sub | branch | none | 빠짐 0 |
| FR4b | **그중에서 + 이름 없음** (장부 0) | 「그중에서 뭐가 제일 좋아」 | **topic**(앞 답 목록 = 지금 주제 진료항목) | [] | sub | branch | none | 장부 0 — 규칙만 |
| FR5 | 정체 묻기 (1) · 전반 설명 (5) | 「볼뉴머가 머야」 · 「전반적으로 설명해줘」 | targets | overview · mechanism · indication · outcome · lineup | sub | branch | names | 03b8 T6 −38% · 빠짐 0 |
| FR6 | 원리 (3) | 「고주파 원리가 머야」 | targets | overview · mechanism | sub | branch | none | 03b8 T5 −35% |
| FR7 | 효과 확인 (4) | 「슈링크로 턱라인 타이트닝이 돼?」 | targets | outcome · indication | sub | branch | none | 빠짐 0 |
| FR8 | 부작용 · 회복 · 금기 (2) | 「부작용은 ?」 | targets | adverse · recovery(+ 금기 말이면 contraindication) | sub | branch | none | 안전 강제 — 3016 T3 그대로 79,884 |
| FR9 | 가격 · 샷 · 회차 (1) | 「써마지 몇샷 맞아야해?」 | targets | offer(+ outcome) | sub | branch | none | 빠짐 0 · **장바구니 R5 와 겹침(§8)** |
| FR10 | 종류 · 뭐가 있어 · 추천 (12) | 「지방 분해주사 뭐뭐 잇어?」 | targets | lineup · indication | sub | branch | **names** | dc78 T3 −53% · lineup 이름만 8(목록 이름이 답의 전부) |
| FR11 | 같이 받기 · 순서 (2) | 「같이 하면 안돼?」 | targets | combo · avoid · same_day · order_interval 가운데 말이 묻는 것 | sub | branch | none | 표본 밖 9c9a T3 −71% · 빠짐 0 |
| FR12 | 비교 (0) | 「A 랑 B 차이가 뭐야」 | targets(둘) | overview · outcome | sub | branch | **detail** | 장부 0 |
| FR13a | **명동점 목록 물음** (1) | 「응 명동점 시술 뭐뭐 잇냐고」 | targets(또는 topic) | lineup · indication | sub | **branch** | names | 장부의 그 턴은 자료 없음 — 측정 없음 |
| FR13b | **명동점에 X 있나(X 가 명동점 밖)** (1) | 「실 리프팅은 없어 명동점에?」 | targets | lineup | sub | **all** | names | 02af T3: JSON 은 branch(오답 · §3-2) · 빠짐 0 |
| FR14 | 앞 답의 명동점 밖 것을 이어 물음 | 「어떤 원리인지 궁금해」(앞 답 = 밖 지방분해주사들) | targets | 묻는 종류 | sub | **all** | — | dc78 T4: JSON 은 branch(오답) · 상세 잃음 2 |
| FR15 | 효과 바람 (0) | 「리프팅 하고 싶어」 | targets(effect) | [] → G2(KS3 outcome) | sub | branch | none | 장부 0 |
| FR16 | 바로잡기 (2) · 넓히기 · 뺌 (2) | 「아니 미간 얘기」 · 「보톡스 말고 다른 시술」 | targets(바로잡은 대상) | 앞 턴 fetch 꼴 그대로 | sub | branch | none | 빠짐 0 |
| FR17 | 목록에 없는 것 (0) | (지어낸 이름 · 허브에 없는 시술) | targets [] | [] | — | — | — | 장부 0 — 2차 읽기 0 · 3차는 「안내할 자료 없음」 문장 규칙 그대로 |
| FR18 | talk (2) | 「아하 고마워」 | — | — | — | — | — | 2차 읽기 0(지금과 같음). 장부 F20 은 FR1 로 본다 |

## 5. 2차 읽기 규칙(결정론 · 판단 0)

| ID | 규칙 | 측정 근거 |
|---|---|---|
| G1 | 대상: `about = targets` 면 이번 턴 targets 의 입구 그대로다. `about = topic` 이면 지금 주제 칸(고민 · 시술 · 제품) + 이번 턴 `sites` 다 | — |
| G2 | 종류 = `fetch.kinds` ∪ `kinds` ∪ KS3 입구 종류(고민 → indication · 효과 → outcome · 금기 · 부작용 · 상품 · 묶음 표의 이름 댄 종류)다. 그 종류가 입구 어느 것에도 안 맞으면 KS6 기본 묶음(시술 → overview · 고민 → indication · 속성 시작 → overview · indication)이다. **KD9 덧붙임은 없다**(상담 경로) | 5판: 표본 43 · 지금 시대 밖 11 빠짐 0. Jev 시대 밖 8 은 빠짐 1(시대 차이 · §0) |
| G3 | **강제 포함**(UD5): 명시 대상(대상 코드 또는 이름이 말에 있음)의 줄 · 읽은 주인의 안전 종류(adverse · recovery · contraindication · avoid) 줄은 G2 · G4 · G6 과 무관하게 전체로 싣는다 | 3016 T3 안전 79,884 그대로 |
| G4 | 층 · 범위: 자기 · 물려받음은 `layers` 대로 싣는다. **하위 중 명동점 진료항목(매핑 `case_codes` · `procedure_codes` · `products`)에 닿는 것은 늘 싣는다.** 닿지 않는 하위 · 후보 줄은 `scope = all` 이면 전체, `branch` 면 **이름만**(줄 · 묶음 머리의 `*name*` 칸) | r1 빠짐 14(밖 뺌) · 6(inherit) → 0 |
| G5 | `lineup = names` 면 lineup 줄은 이름만(머리도), `detail` 이면 전체다 | dc78 T3 −53% |
| G6 | `about = topic`(부위만 턴 · 「그중에서 + 이름 없음」): 고민 이름 칸이 있는 줄은 지금 주제 고민과 같은 것만 싣는다. 고민 칸이 없는 대상 줄(케이스 · 제품 · 시술 profile)은 지금 주제 진료항목의 허브 코드에 닿는 것만 싣는다 | ecc6 T2 198,080 → 11,782(5판) |
| G7 | 같은 줄을 다시 보내지 않는 것(`seen_lines`) · 요약 줄(AP4 · QY*)은 지금 그대로다. **다만 「이름만」 으로 실은 gid 는 `sent` 에 넣지 않는다.** `new_lines` 에 `names_only: true` 를 달고, `ledger.py:237-242` 는 그 줄을 `c.sent` 에서 뺀다(번호는 `c.sent_names` 에 둔다). 뒤 턴에 같은 gid 를 G3 · G4 로 전체로 읽게 되면 **같은 번호로 상세를 다시 싣는다**(`material.py:173-179`) | 앞 턴 인용 31 가운데 근원에서 이름만 3. 0.1.0 G7 이면 3 모두 이름만 그대로. G7 을 바꾸면 a578 T7 「슈링크로 턱라인 타이트닝이 돼 ?」 가 T5 n136(슈링크 indication · 명시 대상)을 상세로 다시 싣는다. a578 T6 의 2(n136 · n195)는 그 턴 JSON 이 branch · 명시 아님이라 이름만 그대로다(상세 잃음 · 앞 턴 2) |

- 「이름만」 줄의 꼴: 줄 번호는 그대로 둔다(인용 가능). 칸은 `*name*` 칸만 남기고, 묶음 머리 `same` 도 이름 칸만 남긴다. 머리 `marks` 에 `names_only: true` 를 단다(3차 규칙 AR1).
- **2차는 「읽고 잘라 내기」(허브 호출은 지금 그대로 · 토큰만 줄임)로 시작한다.** 「안 읽기」(허브 호출 줄임)는 다음 판이다.
  - 이것은 구현 순서라 코디 몫이다(0.1.0 DQ3 를 내림).
  - 「안 읽기」 로 가면 `w.reads` 에서 짓는 상담 밖 목록(`turn.py:198-203` `build_list`)이 줄 수 있다. 그 판에서 확인한다.

## 6. 3차 답 규칙 변화

| ID | 규칙 | 상태 |
|---|---|---|
| AR1 | `names_only` 줄은 「명동점에는 없다 · 이런 것이 있다」 까지만 말한다. 상세(효과 · 원리 · 부작용)를 지어 말하지 않는다. 손님이 그것을 이름으로 다시 물으면 다음 턴 2차가 G3(명시)로 상세를 싣는다(G7). 이름 없이 이어 물으면 1차가 `scope = all` 을 골라야 실린다(FR14 · 측정 0/2) | 제안 |
| AR2 | 「## 앱 판정」 에 가져온 것 한 줄을 싣는다: `{"fetch":{"about","kinds","scope","lineup"}}`. 실리지 않은 종류를 「정보 없음」 으로 말하지 않게 한다(SPEC-010 검수 P2-2 「개요 정보 없어요」 문장과 같은 자리) | 제안 |
| AR3 | 나머지(R1 ~ R11 · 인용 꼬리 · 문장 규칙)는 그대로다 | — |

## 7. 장부 기록 칸(기록만 · 판단에 쓰지 않음)

| ID | 칸 | 내용 | WP |
|---|---|---|---|
| LG1 | `consult.understand.parsed.fetch` | 1차가 낸 그대로. **`verify.py:91-96 parsed_view` 의 칸 목록에 `fetch` 를 더해야 남는다**(지금 열 칸 고정) | WP-1 |
| LG2 | `consult.fetch` | `{about, kinds, layers, scope, lineup, from: understand\|default, fixed[]}` — 2차가 실제로 쓴 값 | WP-1(값) · WP-4(기록) |
| LG3 | `material_size.by_fetch` | 종류별 · 층별 · 범위별(`branch` · `names_only` · `all`) · 강제(명시 · 안전) 바이트와 추정 토큰. 테스트 고침 E 의 `material_size` 옆에 둔다 | WP-4 |
| LG4 | `consult.understand.usage.cache_creation_input_tokens` | 지금 버리는 칸을 남긴다(`understand.py:257-262`) | **WP-1 만** |
| LG5 | `tokens.output_tokens`(답) · `consult.understand.usage.output_tokens`(이해) | 지금 있음 — 출력은 기록만(UD4) | — |
| LG6 | `material.new_lines[].names_only` · `c.sent_names` | G7 — 이름만 실은 gid 와 그 번호 | WP-2 |

## 8. WP(코드 워커)

| WP | 바꿀 자리 | 할 일 | 완료 조건 | 관련 시험만 |
|---|---|---|---|---|
| WP-1 이해 계약 | `prompts/consult.json` pick(출력 꼴 줄 · 규칙 20 ~ 20-6 · `pick.version`) · `consult/verify.py:55-62`(Accepted dict 에 `fetch`) · `:77 parse` · `:91-96 parsed_view`(`fetch` 칸 더함 — LG1) · `:114 verify`(`fetch` 기본 · enum · `fixed[]`) · `consult/understand.py:257-262`(LG4) | JC1 ~ JC6 · 프롬프트 초안 r4 반영 — **단 r4 의 20-6 앞 절 「layers 는 scope 가 all 일 때만 쓰인다」 는 빼고 넣는다**(실측과 맞지 않음 · JC3) · (잼) 입구 목록에 「명동점 없음」 표지를 달아 FR13b · FR14 오답이 주는지 · `layers` 칸을 없앨지(JC3) | `fetch-plan/run4.py --rules 5` 를 앱 프롬프트로 바꿔 표본 43 + 지금 시대 밖 11 재생: JSON 깨짐 0 · `fetch` 빠짐 기록 · 장부 `consult.understand.parsed` 에 `fetch` 있음 · `usage.cache_creation_input_tokens` 있음 · FR13b · FR14 두 턴 결과 기록 · **11-23 이후 새 장부 턴(맞추는 데 안 쓴 것 · 코드 워커가 실물 3 대화 03b8 · ecc6 · 73bd 를 다시 돌려 만든다)에서 JSON 깨짐 0 · 빠짐 0** | `test_v04_understand.py` · `test_v04_prompt.py` · `test_v03_prompt.py` + 새 `test_v06_fetch_contract.py` |
| WP-2 2차 읽기 | `consult/kinds_pick.py:40-42`(상담 경로 KS5 끔 — `walk/front.py` KD9 · `KD9_SET` 는 둠) · `:18 STRONG_BY`(kd9 몫 정리) · `:45-51`(KS6 · about 갈래) · `consult/material_read.py:95`(`fetch` 를 `decide` · 걷기에 넘김) · `walk/calls.py:137 _site_filters` · `:162 _facets` · `walk/ranges.py:16 ROLES_TARGET`(명동점 닿음 갈래) · `consult/material.py:162 · 173-179 renumber`(이름만 · lineup names · 머리 `names_only` · G7 다시 싣기 — 입력에 `sent_names` 를 더함) · `consult/turn.py:159`(`renumber` 호출부 — `conv.sent_names` 를 넘김) · `consult/ledger.py:48-49`(대화 상태 `Conv` 에 `sent_names: dict[str, int]` 칸) · `:237-242`(이름만 gid 를 `sent` 대신 `sent_names` 에 · LG6) · `walk/material.py:253 to_lines` | G1 ~ G7 · 「읽고 잘라 내기」 | ① 표본 43 재생 「## 자료」 −55% 이상 · **지금 시대 밖 11 재생 −10% 이상**(측정 −62.7% · −17.6%) ② **빠짐 0 — 표본 · 지금 시대 밖 11 · 11-23 이후 새 장부 턴(맞추는 데 안 쓴 것 · 실물 3 대화 03b8 · ecc6 · 73bd 재생으로 만든다) 셋 다** ③ **상세 잃음 ≤ 7**(lineup 이름만은 따로 기록 · 측정 17) ④ **offered(KD11) 목록 전후 비교표**(KS7 변화) ⑤ 시험 「이름만 → 다음 턴 이름으로 다시 물음 → 같은 번호로 상세가 실림」(a578 T5 → T7 꼴) ⑥ 실물 3 대화(03b8 · ecc6 · 73bd) 답 확인 | `test_v04_material.py` · `test_v06_material.py` · `test_consult_material.py` · `test_walk_front.py` · `test_walk_core.py` · `test_v06_groups.py` · `test_v04_ledger.py` + 새 `test_v06_fetch_read.py`(FR 표 줄마다) |
| WP-3 3차 규칙 | `prompts/consult.json` kos rules · `system_v3` · `consult/material.py:248 judgement_v3`(AR2 줄) | AR1 · AR2 | 실물: 「명동점 밖」 이름만 줄에 상세를 지어내지 않음 · 「정보 없어요」 문장 0(03b8 · 73bd 재생) | `test_v05_llm_block.py` · `test_v04_prompt.py` |
| WP-4 장부 | `consult/turn.py:259-282`(trace · `material_size`) · `consult/ledger.py` | LG2(기록) · LG3 | 재생 장부에 칸이 다 있음 · `fetch-plan/cost.py` 가 이해 캐시 쓰기를 셈(LG4 는 WP-1) | `test_v04_ledger.py` |

**장바구니(SPEC-010 · token-cause R5)와 겹치는 자리**
- **FR9 「가격 · 샷 · 회차」 의 `offer`** 와 장바구니 R5 「옵션 가격을 가격 · 장바구니 · 모달 턴에만」 은 같은 신호다. R5 를 하는 워커는 이해 호출이 있는 턴에서 `fetch.kinds ∋ offer` 를 「가격 턴」 표지로 쓴다(두 벌 판정 금지).
- **이해 호출이 없는 턴**(모달 열기 · 장바구니 누름 — 이해 호출 0)은 지금 신호(장바구니 · 모달 본 것 — `kos_block.py:118 build` 의 입력) 그대로 쓴다.
- 자리는 `consult/kos_block.py:63 item_line` · `:18 OPTIONS_MAX` · `:118 build` 다. 이 스펙은 명동점 블록을 바꾸지 않는다.
- WP-1 이 먼저 끝나야 R5 가 `fetch` 를 읽을 수 있다.

**관련 · 별 WP 후보**(이 스펙 밖): token-cause R7 `walk/fold.py:16-18 est_tokens`. 지금 코드는 `바이트 // 3 + 1` 이다. 실측 k 는 바이트 × 0.458 이라 지금은 27% 적게 센다. `material_size` 의 한도 판단이 이것에 기댄다.

## 9. 사용자 결정 필요(추천 하나씩)

| # | 물음 | 추천 |
|---|---|---|
| DQ1 | 범위 기본을 「명동점 닿는 것은 다 · 밖은 이름만」(JC4 `branch`)으로 하나? | **예**(코디 추천). 손님이 명동점 밖을 말하거나 물을 때만 `all`. 폭은 빠짐없이(11-16) 지키고 깊이만 명동점. 측정: 밖을 빼면 빠짐 14, 이름만이면 0. 그 대가는 표본 상세 잃음 7 · 앞 턴 2 |

- 0.1.0 의 DQ2(밖 하위 안전 줄 이름만)는 UD5 로 이미 정해진 것이라 지웠다(§1 UD5).
- DQ3(읽고 잘라 내기 먼저)은 구현 순서라 §5 로 내렸다.

## 10. 시안에 없음

새 화면 문구 0. 이 스펙은 화면을 바꾸지 않는다(장부 · 프롬프트 · 읽기만).

## 부록 A. 바뀐 내역

| 판 | 날짜 | 내용 |
|---|---|---|
| 0.1.0 | 2026-11-23 | 처음. 비용 몫 · JC1 ~ JC6 · FR1 ~ FR18 · G1 ~ G7 · AR1 ~ AR3 · LG1 ~ LG5 · WP-1 ~ WP-4 · DQ1 ~ DQ3. 측정 = 호출 3 회 · 2차 규칙 4 판 · 채택 r3_rules3 |
| 0.1.1 | 2026-11-23 | 검수(review-spec-011.md) P1 4 · P2 9 반영. 다시 셈 = 초안 r4 · 2차 6판 · 표본 43 + 표본 밖 19 + 앞 턴 인용 확인 2(실제 호출 64) |
| 0.1.2 | 2026-11-23 | 재검수(review-spec-011-r2.md) P1 1 · P2 4 반영 · 코디 결정 P1-5 (가). G2b 뺌(2차 5판) · 셈을 시대로 나눔(지금 시대 = 머리 수) · WP 완료 조건에 11-23 이후 새 장부 턴 · G7 호출부 · 20-6 빼기. 다시 셈 = 같은 r4 JSON(호출 0) |

## 부록 B. 바뀐 것(검수 지적 → 절)

| 지적 | 무엇 | 고친 자리 |
|---|---|---|
| P1-1 이름만 gid 가 `seen_lines` 에 걸림 | G7: 이름만 gid 는 `sent` 에 넣지 않고 뒤 턴에 같은 번호로 상세를 다시 싣는다. 측정 = 앞 턴 인용 31 의 근원 상태 · a578 T7 다시 실림 1 · T6 이름만 2 | §0 표 아래 · §3-3 마지막 줄 · §5 G7 · §6 AR1 · §7 LG6 · §8 WP-2 자리(`material.py:173-179` · `ledger.py:237-242`) · 완료 ⑤ |
| P1-2 KD9 범위 · KS7 · 시험 | 상담 경로 `kinds_pick.py:40-42` 만 끈다 · `KD9_SET` · `walk/front.py:101-104` · `report.py` 경로는 둔다 · `STRONG_BY` 효과 · offered 전후 비교 · `test_v06_material.py` 더함 | §3-3 KS5 · KS7 줄 · §8 WP-2 자리 · 완료 ④ · 시험 목록 |
| P1-3 F20 오분류 · KD9 빠짐 | F20 을 FR1 로 옮김 · G2 를 새 JSON 으로 다시 셈(KS3 입구 · KS6) · 표본 밖 19 턴 전부 다시 셈. (0.1.1 에 넣은 G2b 는 0.1.2 에서 뺐다 — P1-5) | §0 표 · §4 FR1 · FR18 · §5 G2 · §8 WP-2 완료 ①② · 리포트 §3-5 · §3-6 |
| P1-4 LG1 자리 | WP-1 에 `verify.py:55-62 · :91-96` · 완료 「장부 parsed 에 fetch 있음」 | §7 LG1 · §8 WP-1 |
| P2-1 −22.5% 셈 글 | ecc6 「얼굴에」 두 턴(T2 · T3)만 뺀 41 턴으로 고침: 0.1.0 셈은 −22.4%, 0.1.1 셈은 −23.5% | §0 표 · 리포트 §0 · §3-5 · §4 |
| P2-2 「빠짐 0」 이 상세 잃음을 숨김 | 머리 수에 상세 잃음 7 · lineup 이름만 17 을 나눠 적음 · 완료 조건을 둘로 | §0 표 · §8 WP-2 완료 ③ · DQ1 추천 |
| P2-3 DQ2 = UD5 다시 묻기 | DQ2 지움 · r3_rules4 는 「UD5 로 채택 안 함」 기록 | §1 UD5 · §9 |
| P2-4 DQ3 은 기계 몫 | WP-2 / §5 결정으로 내림 · DQ 는 DQ1 하나 | §5 끝 · §9 |
| P2-5 완료 조건이 표본 맞춤 | 표본 밖 19 턴 빠짐 0 · 밖 감소 −10% 이상(측정 −13.5%)을 따로. (0.1.2 에서 「지금 시대 밖 11 · −17.6%」 와 11-23 이후 새 턴으로 바꿈 — P2-10 · P2-11) | §8 WP-1 · WP-2 완료 |
| P2-6 `layers` 측정 효과 0 | 다시 재 보니(`layers_check.py`) 1차가 고른 값이 62/62 `sub` 라 효과 0 이었다. 값을 바꾸면 17 턴이 달라지고 빠짐이 생긴다(self 25 · inherit 7). 그래서 「scope = all 일 때만」 이 아니라 「늘 sub · 다른 값은 빠짐만」 으로 적음 · 2차 `sub` 고정 · 칸 없앰 추천(WP-1 에서 잼) | §3-1 JC3 · §3-2 · §8 WP-1 |
| P2-7 꼴 겹침 · 「그중에서 + 이름 없음」 | 겹침 합치기 한 줄 · FR4b(about = topic) · 프롬프트 r4 20-1 · 20-2 · 20-4 · 20-5 | §4 머리 · FR4b · §3-1 JC1 · §3-2 |
| P2-8 FR13 섞임 | FR13a(명동점 목록 물음 = branch) · FR13b(명동점에 밖 X 있나 = all) · 프롬프트 r4 20-4 | §4 FR13a · FR13b · §3-2 |
| P2-9 자리 · 기록 | ① `est_tokens` = `바이트 // 3 + 1`(fold.py:16-18) · 0.458 은 측정 k ② LG4 는 WP-1 만 ③ 이해 없는 턴은 지금 신호 그대로 | §8 「관련 · 별 WP」 · §7 LG4 · §8 WP-4 · §8 장바구니 둘째 줄 |
| **P1-5**(재검수) G2b 근거가 Jev 시대 | 코디 결정 (가): G2b 를 뺐다(2차 5판). 44b2 T2 빠짐 1 은 Jev 시대 장부 줄의 시대 차이로 적음. F20 은 「Jev 시대 장부라 대상 칸 없음 — 지금 시대에서는 FR1 고민」 | §0 표 아래 · §3-3 KS6 줄 · §4 FR1 · FR18 · §5 G2(G2b 줄 지움) · 리포트 §3-6 |
| P2-10 표본 밖이 두 시대를 섞음 | 모든 셈을 시대로 나눔 — 지금 시대 밖 11: −17.6% · 빠짐 0/49 · Jev 시대 8: −11.0% · 빠짐 1(참고) · 표본 43 은 모두 지금 시대 | §0 표 · §5 G2 · §8 WP-1 · WP-2 완료 ① ② · 리포트 §3-6 |
| P2-11 맞추지 않은 밖 턴 없음 | WP-1 · WP-2 완료 조건에 「11-23 이후 새 장부 턴(맞추는 데 안 쓴 것) 빠짐 0 — 코드 워커가 실물 3 대화(03b8 · ecc6 · 73bd) 재생으로 만든다」 | §0 끝 줄 · §8 WP-1 · WP-2 완료 |
| P2-12 G7 호출부 · 상태 칸 | WP-2 자리에 `turn.py:159`(`renumber` 호출부 · `conv.sent_names` 넘김) · `ledger.py:48-49`(`Conv.sent_names` 칸) · `renumber` 입력에 `sent_names` | §8 WP-2 자리 |
| P2-13 측정 프롬프트 r4 의 틀린 20-6 | WP-1 할 일에 「r4 20-6 앞 절은 빼고 넣는다」 | §8 WP-1 할 일 |
