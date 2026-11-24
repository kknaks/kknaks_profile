# SPEC-012 0.1.2 구현 리포트 — WP-1 → WP-2 → WP-3 (판 7 · 마감 · after6 측정 뒤)

2026-11-23 · 앱 코드 워커 · 발주 task_761e25b2aad0 · 정본 `SPEC-012-consult-quality.md` 0.1.2(검수 r3 PASS).

지킨 것:
- 앱 워크트리 `clinic_chat/phub-consult-demo` 에서만 고쳤다. 커밋 0 · 서브에이전트 0 · **LLM 호출 0**.
- 18222 · 18105 는 손대지 않았다(18105 는 HF2 자료 확인용 GET 만).
- 화면은 빈 포트 18245 에 띄워 찍고 껐다.
- 키 · 토큰 값 출력 0.
- 측정(WP-0 · WP-4)은 하지 않았다(코디가 따로 발주).


## ★ 판 7 — 마감: 검수 r4 P1-1 · P2 7 + 최종 전체 실측 after6(2026-11-24 · 발주 task_509da87bba98)

측정은 `quality/after6-report.md` 다(마감). 조건은 S01 ~ S13 × 3 한 번 · 최종 코드 · 최종 프롬프트 `7ff6a7c1…` · 새 gold `8f65957f…` · 채점 0.6 이다.
- 결과는 **1,400/1,410** 이고, **base2 대비 떨어진 기준 0** 이다.
- after5f 대비 11 −3 · 16 −1 은 코드 탓 0 이다(실패 턴 1차 출력 = 앞 실측 · 답 프롬프트 바뀐 칸 0 → 답 글 흔들림). 데이터 턴은 S01 T1 팔자주름 1 칸이다.
- 정답표는 새 gold 로 다시 만들었고, 바뀐 칸 0 이다.

| 지적 | 고친 자리 | 어떻게 |
|---|---|---|
| P1-1 | 측정 · `quality/run.py` meta `tree` · `after5-report.md` 바로잡음 줄 | 전체 한 번 실측 · 프롬프트 · diff 해시 기록 · 「프롬프트가 바뀐 판은 부분 실측 불가」 |
| P2-1 | `prompts/consult.json` pick 11 · 20-2 | 시나리오 말 예문 0 · 원칙 (가) 안전 · (나) 효과 · (다) 있음 · 선택지(두 규칙 같은 꼴). 시나리오 밖 6 문장 1차 kinds 6/6 맞음 |
| P2-2 · 3 · 4 | `quality/score.py` 0.6 · `QUALITY.md` | 기준 11 사정 바꿔 말한 꼴 · 기준 14 가장 가까운 앞 이름 짝 · 하위 칸 24 · `--answers` · `--cross-gold`. 바뀐 판정: base2 −4 · after2 −3 · after3 −6 · after4 +1 · after5f −3 + 1 |
| P2-5 | `consult/turn.py` `_said_product_names` | 모든 목록 이름에서 긴 이름이 이김 · 시술 · 계열과 같은 제품 이름(일반 이름)은 바꾸지 않음 · 시험 더함 |
| P2-6 | `SPEC-012-consult-quality.md` 0.1.5 | §3-E 계약 보탬 · HS1 같은 부위 우선 |
| P2-7 | `after5-report.md` | ④ 표에 after5f 2 칸 |

시험: 전체 **752 통과 · 1 실패(옛 `test_s5_t18`) · 2 건너뜀**.

남은 것(코디 판단):
- 기준 11 답 글 흔들림 7 칸 — 텍스트 값 충돌을 앱이 머리 한 줄로 묶는 구조가 후보다.
- 하위 23 4 칸.
- 하위 24(새) 16 칸 — 안 물은 턴에 시너지 요약 줄 `same_day` 칸을 빼고, 물은 턴에 다시 싣는 구조가 후보다.
- S03 T3 1차 표 틀림 바로잡기 후보.

## ★ 판 6 — 고침 5: 코디 결정 ① ~ ④(after4 남은 실패 · 2026-11-24 · 같은 발주 task_4a2965ba516f)

측정은 `quality/after5-report.md` 다. S03 · S04 · S09 · S10 만 다시 돌리고 나머지 9 는 after4 를 합쳤다(사용자 지시). 결과는 **1,405/1,410**(채점 0.5)이고 base2 · after3 대비 떨어진 기준은 0 이다.

| # | 구멍 | 고친 자리 | 어떻게 |
|---|---|---|---|
| ① | 1차 JSON 깨짐(S09 r1) | `consult/turn.py` `understand` · `_usage_sum` · 장부 `understand.retry` | 같은 입력으로 한 번 다시 부른다 · 그래도 깨지면 고침 2 동작(앞 상태 유지 · 첫 턴 FL2) · 토큰 합 |
| ② | 위 고민 → 하위 고민 둘(S03 T2 r1) | `turn.py` `_split_subs.concerns_for` | 고민 부위가 그 부위 하나뿐인 하위 고민이 있으면 그것만 둔다(좁은 쪽 · 데이터) |
| ③ | 말한 제품을 시술로(S04 T4 r2) | `turn.py` `_product_named_targets` · 장부 `topic.product_named` | 허브 목록 제품 이름이 말에 그대로 있고 1차가 그 제품의 매핑 시술을 냈으면 제품으로 바꾼다(시술 이름을 말했거나 · 진료항목 0 · 허브 오류면 그대로) |
| ④ | 채점 11 「확인이 필요」 가 손님 쪽 금기 안내를 침 | `quality/score.py` 0.5 · `QUALITY.md` | 같은 문장에 사정 말이 있을 때만 실패. 바뀐 판정: base2 · after2 · after3 0 · after4 4 |
| 덧 | 1차 원칙이 「받을 수 있어?」 를 안전으로 읽음(after5 S09 T3 r2) | `prompts/consult.json` pick 11 · 20-2 | 있음 · 선택지 확인 물음에는 안전 종류를 더하지 않는다(물은 종류는 그대로 넣음 · 비우지 않음) |

시험: `test_v07_spec012_fix4.py` 에 더함 · `test_v04_turn.py`(json 만 2 번) · `test_v04_ledger.py`(retry 키) 를 고침. 전체 **751 통과 · 1 실패(옛 `test_s5_t18`) · 2 건너뜀**.

남은 것: S03 T3 r2 1차가 제품 코드를 시술 표로 냄(검증이 버림 · 바로잡기 후보) · 답 모델 한 실행 흔들림 4 칸 · 하위 23 4 칸(after5-report §3).

## ★ 판 5 — 고침 4: after3 에서 떨어진 칸 · 남은 실패(2026-11-24 · 발주 task_4a2965ba516f)

근거: `quality/after3-report.md` §3 · §4. 사용자 결정은 그대로 지켰다 — 비용 안 줄임 · 새 고정 한도 0 · 낱말 · 문장 뜻 판정 0 · 판단은 소넷 · 시간 문턱 그대로.
- 측정은 `quality/after4-report.md` 다. 겨눈 네 칸은 닫혔다: S10 T1 12 · 8 3/3, S06 T4 10 3/3, S10 T2 29 · 29 · 29, S08 T3 14 2/3.
- 합계는 **1,377/1,410**(after3 1,390)이다. 떨어진 기준 6 · 7 · 11 · 20(+ after3 대비 1)이 남았다. 까닭은 1차 표본 흔들림 셋(S09 r1 JSON 깨짐 · S03 T2 r1 · S04 T4 r2)과 S10 T1 금기 문장의 채점 11 말 충돌이다.
- 새 diff `+` 줄의 `any(w in` · `_WORDS` · `re.compile` · `re.search` · `timeout` · `_MAX =` · `_LIMIT` · `[:숫자]` 는 0 이다.

| # | 구멍 | 고친 자리(작업 트리) | 어떻게(구조 · 데이터) |
|---|---|---|---|
| 1 | S10 T1 「맞아도돼 ?」 를 1차가 효과 확인으로 읽음 | `prompts/consult.json` pick 규칙 11 · 20-2 | 원칙만 넣었다: 받아도 · 맞아도 · 해도 되는지 = 안전 확인 → contraindication, adverse. 「~돼?」 는 효과가 나는지 확인하는 꼴로 좁혔다. R25 는 그대로 두었다(안전을 물으면 빠짐없이) |
| 2 | S06 T4 명동점 이름에 `out` 이 남음 | `consult/turn.py` `_clear_out_named` · `verify.py` `Accepted.out_cleared`(view 칸) | `out_names` 가 모두 명동점 진료항목 · KOS 시술 이름 전체와 같으면(NM · 일반 이름 뺌) `out` 을 거둔다. 장부는 `accepted.out_cleared` 다 |
| 3 | S10 T2 주제 시술 칸 = 계열 | `consult/turn.py` `_case_same_targets`(async · `det`) | 계열 아래 진료항목(`Detector.modality` · 허브 scope)이 케이스 진료항목을 품으면 케이스를 그 계열 값으로 바꾼다. 허브 오류면 바꾸지 않는다 |
| 4 | S08 T3 국산 줄 값 빠뜨림 | `consult/kos_block.py` `item_line` `products` | 매핑 제품 이름을 진료항목 줄에 싣는다(KOS 약 칸과 매핑 제품이 다른 줄 — 턱보톡스(국산) = 하이톡스) |
| 5 | 하위 23 4/177 | — | 까닭만 적었다: 장부에 `asked_kinds: []` 와 `safety_always` 표지가 다 있었고, 답 모델이 R25 를 그 턴만 안 따랐다(after4-report §4) |

시험:
- 새 `tests/test_v07_spec012_fix4.py` 6 개 — 원칙 문구 · R25 맞물림 · out 거둠 · 거두지 않음(섞임 · 일부 일치) · 계열 케이스 같은 말 · 계열 아래 아님 · 허브 오류 · 이름 그대로 · 진료항목 줄 products.
- `test_v07_spec012_fix3.py` 의 케이스 시험을 async 로 고쳤다.
- 전체 pytest **746 통과 · 1 실패(옛 `test_s5_t18` · 기준과 같음) · 2 건너뜀**.

남은 것(코디 판단):
- S09 r1 1차 JSON 깨짐: 고침 2 규칙대로 앞 상태를 유지했다. 첫 턴이라 0 목록이 됐고 r1 S09 전체가 따라 떨어졌다. 다시 부르기는 새 고정 횟수라 넣지 않았다.
- S03 T2 r1 · S04 T4 r2 1차 표본 흔들림: after3 는 3/3 같았다.
- S10 T1 기준 11: 「먼저 확인이 필요해요」(손님 쪽 금기 확인 문장)가 채점 금지말에 걸린다. 채점 규칙을 바꿀지는 코디 판단이다.

## ★ 판 4 — 고침 3: 재검수 r3 P2-1 ~ P2-7(2026-11-23 · 발주 task_6d33176c8747)

근거: `review-spec-012-code-r3.md`(PASS · P2 7). 사용자 결정은 그대로 지켰다 — 비용 안 줄임 · 새 고정 한도 0 · 낱말 · 문장 뜻 판정 0 · 판단은 소넷 · 시간 문턱 그대로.
- 측정은 `quality/after3-report.md` 다. **1,287 → 1,390/1,410**(채점 0.4 · base2 대비 떨어진 기준 0).
- 다만 after2 대비 하락 셋이 남았다(아래 「남은 것」).
- 새 diff `+` 줄의 `any(w in` · `_WORDS` · `re.compile` · `re.search` · `timeout` · `_MAX =` · `_LIMIT` · `[:숫자]` 는 0 이다.

| # | 지적 | 고친 자리(작업 트리) | 어떻게(구조 · 데이터) |
|---|---|---|---|
| P2-1 | S10 T2 1차가 케이스 · 시술 어느 쪽을 내느냐로 목록이 갈림 | `consult/turn.py:543-544`(HA1 뒤) · `:600-640` `_case_same_targets` · 장부 `topic.case_same` | 1차 케이스 대상이 네 조건을 다 맞으면 「같은 말」 로 보고 케이스를 주제 시술 값으로 바꾼다:<br>• 케이스 진료항목(매핑 `case_codes`) ⊆ 지금 목록<br>• 그 매핑 시술 ⊆ 주제 시술 칸<br>• 그 매핑 부위 ⊆ 주제 부위 칸<br>• 케이스 이름이 이번 말 안에 그대로 없음(pick 규칙 13 · NM2 꼴 이름 대조) |
| P2-2 | 밖 패키지(PKG-0069)가 상세로 실림 | `consult/fetch_read.py:32` `OWNER_TABLES` 에 package · `:91-98` `md_sets["package"]`(매핑 패키지 코드 = 지금 0) | 층 없는 줄의 대상이 패키지면 그 패키지가 주인이다. 명동점 밖이면 `scope = branch` 에서 이름만(HN1 · R17). 채점 쪽은 `score.py` `out_packages`(kind 「메뉴」) |
| P2-3 | 「이름 ⊂ 제품」 이 넓어짐(S12 T4) | `consult/detect.py:356-375` | 포함 관계를 양쪽으로 본다(좁은 쪽이 이김). 직접 · 이름 일치 집합 ⊊ 제품 집합이면 그 제품 집합은 합집합에서 뺀다(`per_slot.pick_narrowed`). 보톡스 ⊇ 하이톡스 규칙은 그대로다 |
| P2-4 | H10 표지가 참 · 거짓뿐 | `verify.py:43` · `:306-312` `out_names` · `turn.py:897-901` · `kos_block.py:140-142`(블록 맨 앞 줄) · 프롬프트 pick 출력 꼴 · 규칙 12 · kos R22 다시 씀 · 답 end_state 「범위 밖」 줄 · 라벨 `absent` | 1차(소넷)가 손님이 댄 목록 밖 이름을 `out_names` 로 낸다. 앱은 그 이름의 명동점 이름 일치(NM)가 0 일 때만 `명동점에 없음: [{name, branch_items: 0}]` 사실 줄을 싣는다. 장부는 `kos_block.absent` |
| P2-5 | 채점 엄함 | `quality/score.py` `answer_kind` `ask_site` · `site_names_in` · `KW.neg` | 기준 뜻대로 고쳤다. 바뀐 판정은 base2 0 · after2 7(엄함 4 풂 · 패키지 3 조임 — after3-report §1) |
| P2-6 | 묻지 않은 안전 먼저 | `turn.py:895-896` 조건 줄 `asked_kinds` · `material.py:215-216` · `:271-274` 머리 `marks.by = safety_always` · 프롬프트 R25 · `score.py` 하위 칸 23 | 1차 kinds 를 사실로 넘기고, 늘 읽은 안전 묶음에 표지를 단다. R25 가 둘을 읽는다 |
| P2-7 | 스펙 H15 자리 | `SPEC-012-consult-quality.md` 0.1.4 — H15 「구현 자리」 한 줄 · 판 기록 | — |

시험:
- 새 `tests/test_v07_spec012_fix3.py` 9 개 — 포함 관계 양쪽 · 합집합 그대로 · 케이스 같은 말 · 케이스 그대로 3 꼴 · 밖 패키지 이름만 · absent 줄 맨 앞 · `out_names` 받기 · 안전 표지 · R22 · R25 원칙만.
- `test_v05_llm_block.py` 규칙 수 26 → 27.
- 전체 pytest **740 통과 · 1 실패(옛 `test_s5_t18` · 기준과 같음) · 2 건너뜀**.

남은 것(after3 · 고침 4 후보 · 코디 판단):
- **S10 T1 기준 12 · 8 3/3 — 고침 3(P2-6)이 만듦.**
  - 1차 kinds 가 「맞아도돼?」 를 `[indication, outcome]` 로 읽었다(pick 20-2 「~돼?」 = 효과 확인).
  - 그래서 R25 가 늘 읽은 안전 묶음을 꺼내지 않게 했다.
  - 방향: pick 규칙 11 · 20-2 에 「받아도 · 맞아도 되는지 = contraindication · adverse 도」 원칙(1차 kinds 바로잡음).
  - 자리: `prompts/consult.json` pick 20-2 · R25 · `turn.py:895-896`.
- **S10 T2 기준 6(5 · 29 · 29) — 고침 3 규칙이 덜 덮음.**
  - T1 1차가 이번엔 계열 `M1` 을 내서 주제 시술 칸이 `modality` 다. `_case_same_targets` 는 `table = procedure` 만 본다(`turn.py:611`).
  - 방향: 계열 값도 받기(케이스 진료항목 ⊆ 목록이면 계열 아래).
- **S06 T4 기준 10 3/3 — 고침 3(P2-4)이 만듦.**
  - 1차가 명동점 이름인 티타늄리프팅을 `out = true · out_names` 로 냈다. absent 줄은 안 실렸지만 `out` 이 남아 답이 「안내해 드리기 어려워요」 가 됐다.
  - 방향: `out_names` 가 모두 명동점 이름 일치면 앱이 `out` 을 거둠(`turn.py:897-901` · `material_read` `scope_gap`).
- S08 T3 가격 빠뜨림 2/3 은 검수 r3 §5 그대로다(다음 판).

## ★ 판 3 — 고침 2: WP-4 측정에서 떨어진 기준 · 못 닫은 구멍(2026-11-23 · 발주 task_ea77a3581b93)

근거: `quality/after-report.md`(C3 · C4 못 함). 사용자 결정 그대로 — 비용 안 줄임 · 새 고정 한도 0 · 낱말 목록 0 · 판단은 소넷.
측정 결과는 `quality/after2-report.md`(1,287 → **1,382/1,410** · 떨어진 기준 0 · C3 · C4 통과).

| # | 구멍 | 고친 자리(작업 트리) | 어떻게(구조) |
|---|---|---|---|
| 1 | S06 T4 「티타늄리프팅이랑 포트라만」 — 칸 교집합으로 서로 지움 | `consult/detect.py:22` `PICK_SLOTS` · `:325-375` `items` | 시술 칸 · 제품 칸이 다 있으면 두 칸을 **한 집합(합집합)** 으로. 제품의 시술(`from: product`)은 넓히지 않음 · 직접 말한 시술이 제품 집합을 품으면(보톡스 ⊇ 하이톡스) 제품이 좁힘(옛 교집합 뜻 유지) |
| 2 | S10 T3 HA1 — 1차가 턱밑을 이미 내면 조상 턱이 남음 | `consult/turn.py:617-623` | 고민 부위가 이미 있어도 그 조상 1차 부위를 지움(`rec.replaced`) |
| 3 | H6 · HN1 둘째 줄 미구현 | `consult/material.py` `summaries` 줄에 `proc_codes` · `renumber(branch_procs=)` · `turn.py:202-205` | 계열 요약 줄의 시술 코드가 명동점 시술과 하나도 안 겹치면 **이름만** 묶음(머리 `marks.names_only = "branch"` · 줄 `{n, modality_name}`) · 2차 읽기 범위가 `branch` 일 때만 |
| 4a | HD7 가격 빠뜨림 | `turn.py:844-856` · `kos_block.py:143` `force_items` | 1차 kinds 에 `offer` 가 있으면 지금 목록 진료항목 줄(옵션 값)을 이 턴에 **다시 실음**(LC5 예외) · 조건 줄 `price_ask` · 장부 `kos_block.force_items` |
| 4b | H10 「모발이식도 해 ?」 | `turn.py:847-849` | 1차가 대상 0 · (`out` 또는 새 말)이면 조건 줄 `unmatched: true`(앱이 넘기는 사실) |
| 4c | H12 값 사정 | `material.py:163-190` `value_ranges` · `:262-266` | 같은 묶음의 `<칸>_min/_max/_unit` 값이 줄마다 다르면 머리 `marks.range` 에 범위 한 줄(같은 단위만 · 원문 값) |
| 4d | 프롬프트 | `prompts/consult.json` R22 · R23 · R24 | 위 세 칸을 읽는 원칙 문장만(채점 문구 0) |
| 5 | 1차 이해 시간 초과(S06 T4 r3) | `turn.py:524-533` | 까닭: 입력 크기 아님 — 시스템 38.6 KB + 메시지 0.1 KB 로 모든 턴이 같고(중앙값 40.8 KB), 같은 말이 다른 실행에서 6.1 · 6.9 초 → **모델 지연**. 동작: 1차 실패(시간 초과 · JSON 깨짐)면 앞 주제 · 조건 · 목록 그대로 · 장부 `topic.understand_error` · `items.understand_error`. 문턱 값은 그대로 |

시험: 새 `tests/test_v07_spec012_fix2.py` 7 개(합집합 · 제품 좁힘 · HA1 조상 · 값 범위 · 요약 이름만 · force_items · 1차 실패 상태 유지) ·
규칙 수 시험 2 곳 R24 까지. 전체 pytest **731 통과 · 실패 1(옛 `test_s5_t18` · 기준과 같음) · 건너뜀 2**.

남은 것(측정에서):
- **H10 여전히 0/9** — `unmatched` 는 3/3 실렸고 답도 「모발이식은 명동점에서 다루지 않아서…」(r2) 꼴까지 왔지만 「안내해 드리기 어려워요」 를 붙여 기준 10 · 8 · 13 채점에서 떨어짐. 프롬프트 원칙(R22)만으로는 표현이 고정되지 않음 — 다음은 구조(예: 앱이 「명동점 없음」 줄을 블록 맨 앞 사실로) 판단 필요.
- 턴 단위 새 실패 3(기준 수준 하락은 0): S08 T3 「나와 있지 않」 · S04 T6 「목록에는 없」 · S07 T2 울쎄라 빠짐.


## ★ 판 2 — 구현 검수 `review-spec-012-code.md`(FAIL · P1 1 · P2 5) 반영(2026-11-23 · 발주 task_fcaa28aab2fb)

지킨 것: 커밋 0 · LLM 0 · 18222 · 18105 손대지 않음 · 키 출력 0 · 시험은 관련만 + 끝에 전체 한 번.

| 지적 | 고친 것 | 바뀐 파일:줄 | 시험 |
|---|---|---|---|
| **P1-1** HD2 가 채점 금지 문구를 예문으로 박음 | 프롬프트에서 예문 따옴을 빼고 원칙만 남김:<br>• HD2 「값의 출처 · 자료 사정은 말하지 않는다」<br>• R16 뒷문장 = 병원 사실로만<br>• R18 「지금 화면 목록과 어긋나는 말을 하지 않는다」<br>• pick 규칙 12 의 「X 도 해?」 예문 → 원칙 문장 | `prompts/consult.json:169` · `:330` · `:396` · `:398` | `tests/test_v07_spec012_prompt.py::test_p1_1_no_scoring_phrases_in_prompt`:<br>• 채점 금지 정규식(값이 같이 · 둘 다 · 따로 · 적혀 있 · 설명도 있고 · 드리기 어려 · 모르겠 · 새로 가져온 · 나와 있지 않)이 프롬프트 전체에 0<br>• SPEC-012 가 쓴 줄에 예문 따옴 0(same_day 칸 값 「가능」 만 예외)<br>• 「확인이 필요」 0 |
| **P2-1** S10 T3 · T4 재생이 HA1 을 안 거침 | 시험만 — 1차 대상 → HA1(가짜 허브) → 이번 턴 조건 → 주제 판단을 이어 T1 → T4. 두 꼴(1차 부위 있음 r1 · r2 / 없음 r3) · 대조(HA1 없으면 깊게 = H14b) | — | `tests/test_v07_spec012_topics.py::test_s10_t3_t4_chain_through_ha1_both_forms` |
| **P2-2** `TOGETHER_KINDS` 시험이 상수만 봄 | 시험만 — `_kos_block` 길(가짜 CLI · 장바구니 둘)에서 같은 말 「같이 받아도 돼요?」 + kinds [] → 짝 줄 안 실음 · kinds `same_day` → 다시 실음 | — | `tests/test_v05_llm_block.py::test_turn_block_pairs_figure_ledger`(row4 · row5 더함) |
| **P2-3** HS1 하위 고민 가정 시험 없음 | 코드 — 일반 고민의 허브 행 고민 가운데 **고민 부위가 그 부위 자신 · 자손인 것만** 짝에 붙임(상위 고민 — 조상 부위만 가진 넓은 고민 — 이 섞여도 안 붙음) · 시험 — 하위 · 상위 섞인 가짜 det 로 「눈가 · 입꼬리 + 주름」 → 주제 둘(하위 고민 짝) · 하위 못 찾으면 안 찢음 | `clinic_chat/consult/turn.py:685-688` | `tests/test_v07_spec012_topics.py::test_hs1_general_concern_to_sub_concern_pairs`. WP-4 실측 S03 T2 r2 는 따로 볼 것 |
| **P2-4** HU1 보강이 스펙 글과 다름 | 스펙 0.1.3:<br>• HU1 에 보강 규칙 두 줄(새 값이 부위 · 고민이면 되돌린 뒤 적용 · 복원 뒤 같은 값이면 그대로)<br>• 검수 r3 P2-3(§3-D 표 머리 · 칸 0.1.2 · S11 T6 판정 칸 = 정답표 crit)<br>• 판 기록<br>그 밖 계약은 그대로 | `SPEC-012-consult-quality.md`(version 0.1.3 · §3-A H15 · §3-D 머리 · S11 T6 줄 · 부록 A) | — |
| **P2-5** HF2 케이스 부위를 허브 GET 으로 · 호출 수 장부에 없음 | 명동점 케이스는 매핑 `hub.case_codes` → 그 진료항목의 매핑 부위(`hub.site_codes` · 여럿이면 「|」 로 이음)로 먼저 정함(허브 GET 0). 매핑 밖 케이스만 허브 `facets profile` GET(gold 별 캐시). 장부 `consult.fetch.case_site{mapped, hub_get, known}` 에 수를 적음(C6). HF2 판정은 케이스 부위가 여럿이면 하나라도 주제 부위 가족이면 상세 | `clinic_chat/consult/turn.py:401-402` · `:850-863` · `:915-916` · `clinic_chat/consult/fetch_read.py:89` · `:167-168` | `tests/test_v07_spec012_fetch.py::test_hf2_case_site_from_mapping_first_and_hub_calls_counted`(매핑 케이스 GET 0 · 밖 케이스 GET 1 · 수 셈 · 판정) |

시험 수:
- 새 시험 3 파일 **23**(topics 12 · fetch 6 · prompt 5). 판 1 은 19 였다.
- `test_v05_llm_block.py` 한 시험에 row4 · row5 를 더했다.
- 관련 시험은 모두 통과다.
- **전체 pytest 한 번: 724 통과 · 1 실패 · 2 건너뜀.** 실패 1 은 옛 `test_state_object.py::test_s5_t18…` 로, 기준 `35b56e5` 에서도 같다.

판 1 의 아래 내용은 그대로 유효하다. 바뀐 줄 번호는 위 표가 정본이다.

## 0. 한눈에

| 항목 | 값 |
|---|---|
| 닫은 구멍(계약) | **H1 ~ H16 전부**(H14a · b 포함). WP-1 9 · WP-2 3 · WP-3 6(+ HD7 · HD8) |
| 검수 r3 P2 | P2-1 반영(`TOGETHER` → 1차 kinds) · P2-2 반영(`score.py`) · P2-3 스펙 문서 고침은 코디 몫이라 §6 에 적기만 · P2-4 반영(HQ1 뺌 · 고르기 = 답 재료) |
| 새 시험 | 3 파일 · 19 시험 — §3-D 연속 재생(S05 T1 → T4 · S06 T1 → T4 · S10 T3 · T4 · 「있어」 · 「잇어」 꼴) 포함 |
| 관련 시험 | WP 마다 통과(§4) |
| 전체 pytest | **720 통과 · 실패 1 · 건너뜀 2**. 실패 1 은 기준 `35b56e5` 에서도 똑같이 실패하는 옛 실패(`test_state_object.py::test_s5_t18…` — 기준 사본에서 같은 줄 확인). 기준 701 통과 + 이번 새 시험 19 = 720 |
| 화면 | `e2e-shots/spec012-home.png` · `spec012-face-check.png`(LLM 없이 열리는 화면 · 콘솔 오류 0 · 앱 로그 오류 0) |
| 스펙과 다르게 한 곳 | 3 곳 — HU1 보강 · HF1 을 상담 경로만 · HK1 을 상담 경로만(§5) |

## 1. WP 별 바뀐 파일:줄(작업 트리 기준)

### WP-1 입구 · 주제 상태

| 계약 | 바뀐 자리 | 내용 |
|---|---|---|
| HP1 쉼 | `consult/topics.py:94-117`(`active_conds` · `suspend_aware` · `turn_values` · `snap_values`) · `:180`(merge — 새 효과면 쉼 풂) · `:499-514`(깊게 — 이름별 0 검사 → `suspended=["effect"]`) · `consult/turn.py:536` · `:562`(셈에서 쉬는 칸 뺌) | 효과는 칸에 남기고 셈에서만 쉼 · 장부 `topic.suspended{slots, names}` |
| HW1 넓히기 | `topics.py:347-363` | 시술 · 제품 · 국가 · 뺌만 비움 · 효과 남김 · `suspended` · `list_held` 풂 |
| HU1 되돌림 | `topics.py:316-325`(새 값 견줌) · `:331-337`(복원에 `list_held`) · `:339-343`(복원 뒤 같은 값이면 그대로) | 사진에 없는 새 값이 고르기 칸에만 → 교체 · 부위 · 고민 새 값 → 되돌림(§5 보강) |
| HL1 앞 목록 표지 | `topics.py:486-487`(`snap` 에 `list_held`) · `:524`(셈 성공 시 지움) · `:558-561`(LS1 → `list_held`) · `consult/kos_block.py:256-258` | 조건 = kept · 표지만 |
| HQ0 · HQ1 · HQ2 | `topics.py:274`(`question` 인자) · `:300-305`(장부 칸) · `:379-401` · `turn.py:548` · `:579-582` `_is_question` | 물음 = 끝 「?」 + 1차 kinds · HQ2 = 고르기의 명동점 진료항목 0(데이터) · HQ1 = 물음 + 부위 · 고민 같음 → 그대로 · 고르기 · 뺌은 `asked_pick` |
| HA1 고민 부위 | `turn.py:525-531`(1차 대상 단계 — `turn_conditions` · `_split_subs` 앞) · `:584-621` `_concern_site_targets` | 결정론(없음 → 고민 부위 · 자손 → 바꿈 · 조상 → 그대로 · 다른 가지 → 더함 · 고민 부위 여럿 + 1차 부위 없음 → 안 넣음) · 장부 `topic.ha1` |
| HS1 짝 고민 · 일반 고민 → 하위 고민 | `turn.py:623-717` `_split_subs`(다시 씀 — 부위 짝마다 고민 · 일반 고민은 허브 하위 고민 가운데 그 부위에 닿는 것) | 시술 없고 고민만 있는 부위 짝도 찢기 판단에 듦 |
| HS2 0 짝 | `topics.py:646` · `:663-665` · `:687-689` · `:694-696` · `:719-727`(`blocked{slot: split}` · `cond_names_of`) | 0 짝은 주제 안 만듦 |
| HX1 부위 축 | `consult/ask_axis.py:83-104` `site_first` · `turn.py:759-767`(AX1 과 같은 문턱 · `multi`) | 부위 칸 없는 주제 + 얼굴 · 몸 두 갈래(또는 고민 부위 여럿) → 축 = 부위 |

### WP-2 가져오기 · 안전

| 계약 | 바뀐 자리 | 내용 |
|---|---|---|
| HF1 부위 거르개 끔 | `walk/calls.py:20`(contextvars) · `:139-146`(`SITE_NAME_OFF`) · `consult/material_read.py:96-103`(`build_walk` 감쌈 — 상담 걷기 전체) | 상담 경로만 허브 `site_name` 거르개 없음(§5) |
| HF2 holder 부위 가족 | `consult/fetch_read.py:87-88`(Ctx 칸) · `:161-172`(코드 명시 → HF2 → 이름 명시) · `turn.py:88`(`_CASE_SITE` 캐시) · `:199`(`prep_case_sites` 호출) · `:831-874`(케이스 부위 = 허브 `facets profile` `site_name` → 매핑 부위 이름) · `:879-891`(주제 부위 가족) · `:929-934`(장부 `by_fetch.holder` 갈래 — 크기 기록만) | 다른 부위 케이스 = 이름만(`names:site_other`) · 부위 없는 holder = 그대로 |
| HK1 안전 늘 | `consult/material_read.py:31-46` `safety_always` · `:121` · `turn.py:987-989`(늘 읽은 안전은 NQ6 「안전 물음」 으로 안 침) | 대상에 시술 · 계열 · 케이스 · 제품 → adverse · contraindication · recovery(`by: safety_always` · 필수 아님) |
| HN1 주인 · 재생 꼴 | `fetch_read.py:136-139`(층 없는 줄 = 행 대상 칸) · `consult/material.py:163-170` `_target_of` · `:247`(장부 `new_lines[].target`) | 밖 대상 = 이름만 · 장부에 대상 칸(3차 글은 그대로) |

### WP-3 답 글(`prompts/consult.json`)

| 계약 | 줄 | 내용 |
|---|---|---|
| HD1 | `:96` · `:195` | 같은 날은 물었을 때만 · 블록 · 자료 값 · 고정 문장 없음 |
| HD2 · HD4 | `:169` · `:170` | 값 갈림 = 손님 말로 범위 · 자료 · 출처 사정 안 말함 / 이미 한 설명 되풀이 안 함 |
| HD6 | `:173` · `:205` · `:221` | 물은 종류는 아는 것 먼저 · 빈 부분만 돌려 말함 · 돌려 막는 한 줄로 끝내지 않음 · 묻지 않은 안전 먼저 안 꺼냄 |
| HD5 | `:330`(pick 규칙 12) | 목록 어디에도 없는 시술 이름 물음 = out · kind new · 되묻지 않음 |
| HD3 · HN2 · 표지 · HD7 · HD8 | `:396-401`(R16 보강 · R17 ~ R21) | 목록 사정 말 안 함 · 이름만 줄 먼저 안 꺼냄 · `list_held` · `out_pick` · `asked_pick` · `suspended` 읽는 법 · 가격 빠짐없이 · 축 = 부위면 부위 물음 |
| r3 P2-1 | `consult/kos_block.py:25-26` · `turn.py:810-812` | 같이 받기 짝 줄 다시 싣기 = 1차 kinds(`combo` · `same_day`) — 낱말 `TOGETHER` 는 판정에 안 씀 |

시험 고침(새 계약에 맞춤):
- `tests/test_v05_topic_tuple.py` — 교체 0 시험은 명동점에 있는 고르기로 바꾸고, 명동점 0 고르기는 HQ2 로 확인. 67bb 되돌림 기록 칸 `restored`.
- `tests/test_v05_llm_block.py` — kos 규칙 수 18 → 23. 같이 받기 턴 가짜 이해에 kinds `combo`.
- `tests/test_v04_material.py` — 상담 걷기는 안전 종류를 더 읽음(그 밖은 시험 앱 걷기와 같음).

## 2. 구멍 → 고친 자리

| 구멍 | 계약 | 자리(§1) | 시험 |
|---|---|---|---|
| H1 부위 거르개로 안전 · 효과 0 | HF1 · HF2 | `walk/calls.py` · `material_read.py` · `fetch_read.py` · `turn.py` | `test_v07_spec012_fetch.py::test_hf1…` · `::test_hf2…` |
| H2 막힌 칸 뒤 앞 목록 | HL1 | `topics.py` · `kos_block.py` | `test_v07_spec012_topics.py::test_s05_t1_to_t4…` |
| H3 묻는 말이 목록을 바꿈 | HQ0 ~ 2 | `topics.py` · `turn.py` | `::test_hq1…` · `::test_hq2…` · `::test_spelling_and_typo…` · `test_v05_topic_tuple.py::test_1123_pick_replace_zero_follows` |
| H4 부위 둘 + 고민만 | HS1 · HS2 | `turn.py` `_split_subs` · `topics.py` `split_decide` | `::test_hs2…`(HS1 은 허브 하위 고민이 드는 길 — 가짜 허브 시험 없음 · §6) |
| H5 · H14b 이해 흔들림 · 빈 칸 채움 | HA1 | `turn.py` | `::test_ha1…` · `::test_s10_t3_t4…` |
| H6 밖 이름 상세 | HN1 · HN2 | `fetch_read.py` · `material.py` · 프롬프트 R17 | `test_v07_spec012_fetch.py::test_hn1…` |
| H7 「그중에서」 앞 목록 밖 | HP1 | `topics.py` | `::test_s06_t1_to_t3…` |
| H8 넓히기 범위 | HW1 | `topics.py` | `::test_s06_t1_to_t3…` · `test_v05_topic_tuple.py::test_1123_widen…`(그대로 통과) |
| H9 되풀이 | HD4 | 프롬프트 `:170` | `test_v07_spec012_prompt.py` |
| H10 없는 시술 · 돌려 막기 | HD5 · HD6 | 프롬프트 | `test_v07_spec012_prompt.py` |
| H11 같은 날 대본 | HD1 | 프롬프트 `:96` · `:195` | `::test_hd1…` |
| H12 값 사정 | HD2 | 프롬프트 `:169` | `::test_hd2_hd4_hd6…` |
| H13 목록 사정 | HD3 | 프롬프트 R16 | `::test_hd3_hd7_hd8…` |
| H14a 안전 종류 빠짐 | HK1 | `material_read.py` · `turn.py`(NQ6) | `test_v07_spec012_fetch.py::test_hk1…` |
| H15 「아니 X 말고 Y」 | HU1 | `topics.py` | `::test_s05_t1_to_t4…` · `::test_hu1_site_correction_still_undoes` |
| H16 부위 물음 | HX1 · HD8 | `ask_axis.py` · `turn.py` · 프롬프트 R21 | `::test_hx1_site_axis_first` |
| 가격 빠뜨림 | HD7 | 프롬프트 R20 | `::test_hd3_hd7_hd8…` |

## 3. 기존 낱말 판정 자리 — 전수(grep `any(w in` · `_WORDS` · 표지 튜플)

| 자리 | 낱말 | 무엇을 판정 | 이번 |
|---|---|---|---|
| `consult/topics.py:38-43` `UNDO_WORDS` · `:44` `MALGO` · `:58-68` `undo_marker` | 아니 · 그거 말고 · 그게 아니라 · 잘못 · ~ 말고 | 되돌림 표지(1차 `topic.move = undo` 와 함께) | 그대로(사용자 11-23 결정 표지). HU1 이 「되돌릴지 · 교체할지」 를 사진 값(데이터)으로 정함 |
| `topics.py:45-52` `WIDEN_WORDS` · `:71-73` | 다른 시술 · 다른 것 · 전체로 · 전부 · 상관없이 | 넓히기 표지(1차 `widen` 과 함께) | 그대로(사용자 11-23 결정 표지) |
| `topics.py:55` `PRICE_WORDS` · `:76-79` `info_question` | 가격 · 얼마 · 비용 | 옛 정보 질문(O-15) | 그대로 · HQ0(물음 판정)은 안 씀 |
| `consult/kos_block.py:21-25` `TOGETHER` | 같이 · 함께 · 동시에 | 장바구니 짝 줄 다시 싣기 | **판정에서 뺌** → 1차 kinds `combo` · `same_day`(`TOGETHER_KINDS`) · 튜플은 기록용으로 남김(r3 P2-1) |
| `consult/detect.py:47` `GENERIC_NAMES` | 스킨케어 등 일반 이름 | 이름 일치(NM6) 「일반 낱말 이름」 표지 | 그대로(이름 일치 표지 · 뜻 판정 아님) |
| `consult/price.py:18` `CO2_WORDS` · `:21` `GENDER` | 1년권 · 가입비 / 남성 · 여성 | 최저가 후보 거르기(상품 제목) | 그대로(상품 데이터 칸 · 손님 말 판정 아님) |
| `consult/verify.py:21` `COUNTRIES` | KR · 수입 | 1차 출력 값 검사 | 그대로(출력 enum) |

이번에 더한 낱말 판정은 **0** 이다. 물음은 「?」 부호 + 1차 kinds, 밖 · 없는 시술은 매핑 데이터, 같이 받기는 1차 kinds 로 판정한다.

## 4. 시험 결과

| 단계 | 돌린 것 | 결과 |
|---|---|---|
| 시작(기준) | 관련 12 파일 | 142 통과 · 2 건너뜀 |
| WP-1 | `test_v07_spec012_topics.py`(10) · `test_v05_topic_tuple.py` · `test_v05_fix_e.py` · `test_v05_detect.py` · `test_v05_ask_axis.py` · `test_v05_llm_block.py` · `test_v05_fix_a.py` · `test_consult_turn.py` | 108 + 10 통과 |
| WP-2 | `test_v07_spec012_fetch.py`(5) · `test_walk_ranges.py` · `test_v06_filters.py` · `test_v06_fetch_read.py` · `test_v06_fetch_contract.py` · `test_consult_material.py`(sha 지킴 그대로) · `test_v06_material.py` · `test_walk_front.py` · `test_v04_turn.py` · `test_v06_groups.py` · `test_walk_core.py` · `test_walk_entry.py` · `test_v04_material.py` · `test_v04_plan.py` | 148 + 5 통과 |
| WP-3 | `test_v07_spec012_prompt.py`(4) · `test_v05_llm_block.py` · `test_v04_prompt.py` · `test_consult_prompt.py` · `test_v04_understand.py` | 39 통과 · 1 건너뜀 |
| **전체 한 번** | `uv run pytest -q` | **720 통과 · 1 실패(옛 · 기준과 같음) · 2 건너뜀** |

전체에서 처음 잡힌 것 둘을 고쳤다.
- **HK1 + NQ6**: 늘 읽는 안전 종류가 「안전을 물으면 되묻지 않음」(NQ6)을 늘 켜서 0.2 빈 칸 질문 6 시험이 깨졌다 → 늘 읽은 안전은 NQ6 에서 뺌(`turn.py:987-989`).
- **HX1 문턱**: 목록이 작을 때도 축을 정해 버렸다 → AX1 과 같은 문턱(`chat_ask_list_min`)일 때만 걸림.

## 5. 스펙과 다르게 한 곳(검수에서 볼 것)

1. **HU1 보강**:
   - 스펙은 「사진에 없는 새 값이면 교체」 다.
   - 그대로 짜면 실물 67bb T4 「아니 이마에 써마지를 받고 싶다고」(새 값 = 부위 이마)가 미간 주제에 붙은 써마지를 그대로 두고 새 주제를 만든다. 기존 시험 `test_1123_conv67bb9faf_seven_turns` 가 깨진다.
   - 그래서 「새 값이 **고르기 칸(시술 · 제품)에만** 있으면 교체 · 부위 · 고민 칸에도 새 값이 있으면 되돌린 뒤 적용(직전 변화가 다른 주제로 간 것)」 으로 했다.
   - §3-D 결정 칸은 그대로다(S05 T3 교체 · T4 복원 · S11 T4 교체).
2. **HF1 은 상담 경로만**:
   - `walk/ranges.py` `SITE_NAME_FACETS` 를 비우면 시험 앱 열 걷기(`col_b.walk`)와 걷기 시험 6 개(`test_walk_core` · `test_v06_filters` · `test_v06_material`)의 계약이 바뀐다.
   - 그래서 `walk/calls.py` 에 `SITE_NAME_OFF`(contextvar)를 두고, 상담 `build_walk` 안에서만 끈다. 시험 앱 경로는 그대로다.
3. **HK1 은 상담 경로만**:
   - `kinds_pick.decide` 에 넣으면 걷기 `_decide_kinds` 와 같아야 한다는 시험(S8-T9)이 깨진다.
   - 그래서 `material_read.safety_always` 로 `kp.decide` 뒤에 덧붙였다(스펙 자리 `material_read.py:95` 그대로).
4. **HF2 순서**: 「보톡스(종아리)」 가 괄호를 떼면 「보톡스」 라 말 속 이름과 맞아 G3 이름 명시로 비껴간다. 그래서 코드 명시 → HF2 → 이름 명시 차례로 두었다(시험이 잡음).

## 6. 남은 것

- **측정**: WP-0 · WP-4 는 코디가 따로 발주한다. WP-0 은 다른 워커가 `35b56e5` 사본(18243)으로 돌리는 중이다. 이 작업 트리와 섞이지 않는다.
- **HS1 일반 고민 → 하위 고민**: 허브 `concern_candidates` 하위 고민 행(`r.upper`)에 기대는 길이다. 가짜 허브 시험을 짓지 않았으니 WP-4 실측(S03 T2 r2 꼴)에서 볼 것.
- **HF2 케이스 부위 조회**: 케이스 holder 마다 허브 `facets profile` 1 회(gold 별 프로세스 캐시)다. 호출 수는 장부 `consult` 에 따로 남기지 않았다(`self.case_site_calls` 는 있음). 크기는 `material_size.by_fetch.holder` 로 기록한다.
- **검수 r3 P2-3(스펙 문서)**: 코디 몫이라 고치지 않았다.
  - §3-D 표 머리 「0.1.1 계약 기준」 · 칸 「0.1.1 동작」 → 0.1.2 로.
  - S11 T6 판정 칸 「18 items_same ✓」 는 정답표 S11 T6 `crit = [8, 9, 10, 11, 15]` 와 다르다(18 은 그 턴에 안 봄).
- **`score.py`(r3 P2-2)**: 측정 meta 에 gold 가 있는데 정답표 gold 가 비면 멈추게 했다.
- **부수 영향 하나**: P2-2 확인을 위해 `score.py out/base-20261123-1714` 를 다시 돌렸다. 그때 정답표(`answers.json`)는 이미 코디가 새 gold `e8f02287…` 로 다시 만든 것이었다. 그래서 `out/base-20261123-1714/score.{json,md}` · `human.md` 가 새 정답표 기준으로 다시 쓰였다(1,024/1,137). `base-report.md` v0.3 의 수치(1,009/1,116)는 옛 정답표 기준이다.
- **커밋 0**: 바뀐 앱 파일 9 · 시험 고침 3 · 새 시험 3 은 작업 트리에만 있다.
