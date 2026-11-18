# KD8 — Jev 정보 종류 판단 확인 결과(2026-11-16)

- 스크립트: `clinic_chat/experiments/kd8_kind_check.py`(허브 · LLM 없이 Jev 만 · 앱 본 코드 그대로)
- 질문 셋: 워크트리 `data/experiments/kd8/questions.json`(gitignore — 문장은 여기 없음) · 결과 JSON 같은 폴더 `results-20261116-212332.json`(본판) · `results-alt-order_interval.json` · `results-alt-inline.json`(가설 확인)
- 모델: `jev-1.14.0`(전 요청) · 문턱 yes ≥ 0.7 · no ≤ 0.3(설정 기본)
- 요청 꼴: 문항마다 한 요청 = `kind_{k}` Noul 14 · state = `{question, (question_en), target{table, name}, kinds_catalog[14]{code, name}}` · 대상은 일반 시술 이름 하나를 고정
- instructions(본판): ``Is `kinds_catalog[{k}]` needed to answer `question` about `target`? Say yes only if the question asks for this kind of information; do not count information that would merely be nice to have.`` (+ ko_en 판에 `question_en` 은 영어 풀이라는 한 문장)
- 실물 요청: 본판 26(13 문항 × 2 판) + 가설 확인 6(3 문항 × 2) = **32**

## 1. 본판 결과(문항 × 판)

KD3 덮음 = 앱이 KD1 · KD2 · KD3 본문대로 고를 때(yes ∪ 1위 ∪ 끌어낸 범위의 기본 묶음 · KD5 · KD6 은 이 시험 밖) 기대 종류가 다 읽히나. 사이 상위 n = yes 가 아닌 기대 종류를 닿게 하려면 사이 값 가운데 몇 번째까지 읽어야 하나(0 = 필요 없음 · — = no 이하라 n 으로 못 닿음).

| id | 꼴 | 기대 종류 | 판 | 물은 종류 Noul(순위 · 1위 · yes) | 묻지 않은 yes | 묻지 않은 사이 | 1위 | KD3 덮음 | 사이 상위 n | ms |
|---|---|---|---|---|---:|---:|---|:-:|---:|---:|
| a1 | 원리만 | mechanism | ko | mechanism 0.98(#1 1위 yes) | 0 | 0 | mechanism | ✓ | 0 | 283 |
| a2 | 효과만 | outcome | ko | outcome 0.98(#1 1위 yes) | 0 | 0 | outcome | ✓ | 0 | 186 |
| a3 | 회복만 | recovery | ko | recovery 0.99(#1 1위 yes) | 0 | 0 | recovery | ✓ | 0 | 172 |
| a4 | 하위 목록만 | lineup | ko | lineup 0.89(#1 1위 yes) | 0 | 1 | lineup | ✓ | 0 | 177 |
| a5 | 상품만 | offer | ko | offer 0.97(#1 1위 yes) | 0 | 1 | offer | ✓ | 0 | 183 |
| b1 | 효과+부작용 | outcome, adverse | ko | outcome 0.89(#2 yes) · adverse 0.97(#1 1위 yes) | 0 | 0 | adverse | ✓ | 0 | 172 |
| b2 | 원리+회복 | mechanism, recovery | ko | mechanism 0.98(#1 1위 yes) · recovery 0.97(#2 yes) | 0 | 0 | mechanism | ✓ | 0 | 164 |
| b3 | 금기+회피 | contraindication, avoid | ko | contraindication 0.79(#2 yes) · avoid 0.95(#1 1위 yes) | 0 | 1 | avoid | ✓ | 0 | 165 |
| b4 | 같은 날+간격 | same_day, order_interval | ko | same_day 0.93(#1 1위 yes) · **order_interval 0.09(#5)** | 0 | 0 | same_day | **✗** | — | 168 |
| b5 | 상품+패키지 | offer, package | ko | offer 0.97(#1 1위 yes) · package 0.92(#2 yes) | **1**(order_interval 0.74) | 0 | offer | ✓ | 0 | 162 |
| c1 | 뭐야 | overview | ko | overview 0.94(#1 1위 yes) | 0 | 1 | overview | ✓ | 0 | 170 |
| c2 | 뭐 해 | overview, indication | ko | overview 0.75(#2 yes) · indication 0.82(#1 1위 yes) | 0 | 0 | indication | ✓ | 0 | 172 |
| c3 | 뭐야 | overview | ko | overview 0.94(#1 1위 yes) | 0 | 1 | overview | ✓ | 0 | 169 |
| a1 | 원리만 | mechanism | ko_en | mechanism 0.99(#1 1위 yes) | 0 | 0 | mechanism | ✓ | 0 | 167 |
| a2 | 효과만 | outcome | ko_en | outcome 0.98(#1 1위 yes) | 0 | 0 | outcome | ✓ | 0 | 186 |
| a3 | 회복만 | recovery | ko_en | recovery 0.99(#1 1위 yes) | 0 | 0 | recovery | ✓ | 0 | 181 |
| a4 | 하위 목록만 | lineup | ko_en | lineup 0.89(#1 1위 yes) | 0 | 1 | lineup | ✓ | 0 | 166 |
| a5 | 상품만 | offer | ko_en | offer 0.98(#1 1위 yes) | 0 | 1 | offer | ✓ | 0 | 226 |
| b1 | 효과+부작용 | outcome, adverse | ko_en | outcome 0.92(#2 yes) · adverse 0.98(#1 1위 yes) | 0 | 0 | adverse | ✓ | 0 | 165 |
| b2 | 원리+회복 | mechanism, recovery | ko_en | mechanism 0.99(#1 1위 yes) · recovery 0.98(#2 yes) | 0 | 0 | mechanism | ✓ | 0 | 162 |
| b3 | 금기+회피 | contraindication, avoid | ko_en | contraindication 0.78(#2 yes) · avoid 0.97(#1 1위 yes) | 0 | 2 | avoid | ✓ | 0 | 177 |
| b4 | 같은 날+간격 | same_day, order_interval | ko_en | same_day 0.92(#1 1위 yes) · **order_interval 0.17(#5)** | 0 | 1 | same_day | **✗** | — | 165 |
| b5 | 상품+패키지 | offer, package | ko_en | offer 0.97(#1 1위 yes) · package 0.91(#2 yes) | **1**(order_interval 0.70) | 0 | offer | ✓ | 0 | 170 |
| c1 | 뭐야 | overview | ko_en | overview 0.96(#1 1위 yes) | 0 | 2 | overview | ✓ | 0 | 173 |
| c2 | 뭐 해 | overview, indication | ko_en | overview 0.29(#2) · indication 0.95(#1 1위 yes) | 0 | 0 | indication | ✓ | — | 168 |
| c3 | 뭐야 | overview | ko_en | overview 0.93(#1 1위 yes) | 0 | 2 | overview | ✓ | 0 | 177 |

### 합

| | ko | ko_en |
|---|---|---|
| 「하나만」 5 — 물은 종류 1위 · yes | 5/5 · 5/5 | 5/5 · 5/5 |
| 「둘 함께」 5 — 물은 종류 10 개 중 yes | 9/10(빠진 것 b4 `order_interval`) | 9/10(같음) |
| 「짚지 않음」 3 — 기대 종류 yes | 4/4 | 3/4(c2 `overview` 0.29 — 시술 범위 기본 묶음으로 KD3 이 덮음) |
| KD3 본문으로 기대 종류 다 덮음 | 12/13 | 12/13 |
| 묻지 않은 yes(합) | 1(b5 `order_interval`) | 1(같음) |
| 묻지 않은 사이(합 · 문항당 최대) | 5 · 1 | 9 · 2 |
| ms(중앙 · 최소 ~ 최대) | 172 · 162 ~ 283 | 170 · 162 ~ 226 |

- **한국어는 원인이 아니다** — 영어 풀이를 붙여도 물은 종류의 값 · 순위가 거의 같다(차이 ±0.03 · 같은 곳에서 같은 실패). 풀이를 붙이면 사이 값이 조금 는다(5 → 9).
- 속도 탭의 「묶음 Noul 이 대부분 사이」(KD2 근거)는 **종류를 짚은 질문에서는 나오지 않는다** — 물은 종류는 0.75 ~ 0.99 로 섰고 사이는 문항당 0 ~ 2.

## 2. 하나 남은 실패 — `order_interval` 은 색인 참조가 밀린다(가설 확인 6 요청)

b4 는 순서·간격을 물었는데 `order_interval` 이 0.09 / 0.17 이고, 상품 · 패키지를 물은 b5 에서는 0.74 / 0.70 · 상품만 물은 a5 에서도 0.42 / 0.38 이 나왔다. `order_interval` = `kinds_catalog[12]` · `offer` = `[13]` — 바로 옆 종류의 값을 따라가는 꼴이다.

| 시도(ko 판 · a5 · b4 · b5) | a5 `order_interval` | b4 `order_interval` | b5 `order_interval` | 판정 |
|---|---:|---:|---:|---|
| 본판(§3-2a 이름 · 색인만) | 0.42 | 0.09 | 0.74 | 실패 |
| ① 영어 이름만 바꿈(「order」 가 「주문」 으로 읽히나 — "which procedure comes first, the waiting interval between procedures, and how often to repeat it") | 0.64 | 0.20 | 0.70 | **안 고쳐짐** — 이름 문구 탓 아님 |
| ② instructions 에 종류 이름을 직접 적음(``Is the information kind "<name>" (`kinds_catalog[k]`) needed …`` · 이름은 §3-2a 그대로) | ≤ 0.3 | **0.96(yes)** | ≤ 0.3 | **고쳐짐** — b4 KD3 덮음 ✓ · a5 · b5 묻지 않은 yes 0 · 사이 0 |

②에서 다른 종류의 값도 그대로 섰다(a5 `offer` 0.99 · b4 `same_day` 0.97 · b5 `offer` 0.98 · `package` 0.97). ms 179 ~ 294.

## 3. 결론

**KD2 · KD3 본문 그대로 간다**(「사이 값 상위 n」 으로 넓힐 필요 없음 — 본판 26 에서 n 이 필요한 경우가 0 이다. 못 닿은 둘은 사이가 아니라 no 이하라 n 으로는 안 닿았다). 단, **`kind_{k}` instructions 에 종류 이름을 직접 적어야 한다** — 색인(`kinds_catalog[k]`)만 쓰면 목록 끝에서 옆 종류로 밀려 물은 종류를 놓치고(b4) 묻지 않은 종류를 yes 로 올린다(b5). §3-3 은 instructions 의 최종 문구를 구현 때 정한다고 적었으므로(O-24) SPEC 고침은 필요 없고 구현 지시로 충분하다 — 다만 `target_{i}` · `entry_{i}` · `candidate_{i}` 도 색인만 쓰면 같은 밀림이 있을 수 있어 같은 꼴(이름을 instructions 에 함께)을 권한다(이번 시험 밖 · 미확인).

## 4. 한계

- 문항 13 · 대상은 일반 시술 이름 하나 고정(대상 판단 · 후보 · `gap` Noul 없음) · 실제 단계 ①-2 요청은 `target_{i}` · `gap` 이 함께 들어 state 가 길다 — 그때의 밀림은 이 시험이 보지 않았다.
- ② 의 고침은 3 문항 · ko 판만 확인했다. 구현 뒤 1회차 trace 로 다시 본다.
- 문항 문장은 이 워커 초안(사용자 확정 대상 아님 · 실험용).
