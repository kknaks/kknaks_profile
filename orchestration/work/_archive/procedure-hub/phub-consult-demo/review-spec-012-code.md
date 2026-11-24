# 검수 — SPEC-012 0.1.2 구현(WP-1 ~ WP-3) · 2026-11-23

검수 워커(읽기만). 대상은 다음과 같다.
- 앱 작업 트리 `clinic_chat/phub-consult-demo`(기준 `35b56e5` · 커밋 안 된 변경 · `git diff 35b56e5`)
  - 앱 9 파일 · 시험 고침 3 · 새 시험 3
- `spec-012-code-report.md`
- 기준: `SPEC-012-consult-quality.md` 0.1.2 · `review-spec-012-r3.md` · `spec-012-code-task.md` · `_RESUME.md` §2 · `quality/answers.json`

지킨 것:
- 앱 · 허브 · 데이터 · 프롬프트 수정 0 · 커밋 0 · 서브에이전트 0 · LLM 0.
- 18222 · 18105 손대지 않음 · 서버 띄우지 않음.
- pytest 는 `-p no:cacheprovider` · `PYTHONDONTWRITEBYTECODE=1` 로 돌렸다. 작업 트리 `git status` 는 전 · 뒤 같다(15 줄).

## 판정: **FAIL** — P0 0 · P1 1 · P2 5

- 계약 H1 ~ H16 은 모두 코드에 있다.
- 결정 칸 연속 재생도 정답표와 같게 짜였다: S05 T1 → T4 · S06 T1 → T3 · S10 T3 · 「있어」 · 「잇어」.
- 새 낱말 판정 0 · 새 고정 한도 0 · 비용 쪽 변경 0 이다.
- 전체 pytest **720 통과 · 1 실패(옛 · 기준과 같음) · 2 건너뜀**은 그대로 재현된다.
- FAIL 까닭은 프롬프트 한 줄이다(P1-1). HD2 가 「값이 둘이다」 · 「~라고 적혀 있다」 · 「~라는 설명도 있다」 를 금지 예문으로 박았다. 스펙 §3-C 「금지 낱말 목록을 프롬프트에 넣지 않는다」 에 어긋나고, 품질 채점 기준 11 의 금지 정규식(`score.py` RX_BAN11 「값이 둘 다」 · 「적혀 있」 · 「설명도 있고 … 설명도 있」)과 같은 말이라 WP-4 측정을 흐린다.

## 1. 시험 재현

| 단계 | 리포트 | 다시 돎 | 같음 |
|---|---|---|---|
| 전체 `uv run pytest -q` | 720 통과 · 1 실패(옛) · 2 건너뜀 | **720 passed · 1 failed · 2 skipped**(33.6 초) · 실패 = `test_state_object.py::test_s5_t18_terminal_turn_updates_but_no_list_then_catches_up`(기준에서도 실패하는 옛 실패) | ✓ |
| 새 시험 3 파일 | 19 | topics 10 · fetch 5 · prompt 4 = 19(전체 안에서 통과) | ✓ |

## 2. 구멍 × 구현 대조

| 구멍 | 계약 | 구현(파일:줄 — 작업 트리) | 맞나 |
|---|---|---|---|
| H3 | HQ0 물음 = 끝 「?」 + 1차 kinds | `turn.py:579-582` `_is_question`(「?」 · 「？」 + `acc.kinds`) | ✓ 낱말 0 |
| | HQ1 물음 + 부위 · 고민 같음 → 그대로 · 고르기 · 뺌 = 답 재료(r3 P2-4) | `topics.py:390-402`(`asked_pick{pick, exclude}` · `info` · `same`) | ✓ |
| | HQ2 고르기의 명동점 0 → 고르기 안 함 · `out_pick` | `topics.py:379-389`(고르기 칸만 셈 → 0 이면 고르기 비움) | ✓ 데이터 판정 · 말 꼴 무관 |
| H4 | HS1 부위 짝 고민 · 일반 → 하위 · HS2 0 짝 | `turn.py:623-717` `_split_subs`(`concerns_for` · `det.concern` 의 `r.upper`) · `topics.py:663-665` · `:687-696` · `:719-727` | ✓(HS1 은 시험 없음 — P2-3) |
| H5 · H14b | HA1 1차 대상 단계 · 결정론 · 여러 부위 고민 = 넣지 않음 | `turn.py:525-531` · `:584-621` | ✓ |
| H7 | HP1 `suspended` | `topics.py:94-110` · `:499-514` · `:180` · `turn.py:536` · `:562` | ✓ |
| H8 | HW1 효과 남김 · 쉼 풂 | `topics.py:347-363` | ✓ |
| H2 | HL1 `list_held` · 사진에 담음 | `topics.py:486-487` · `:524` · `:558-561` · `kos_block.py:256-258` | ✓ |
| H15 | HU1 사진 견줌 | `topics.py:316-343` | ✓ + **보강**: 새 값이 부위 · 고민 칸에도 있으면 되돌림(67bb T4) — 스펙 글과 다르다(리포트 §5-1 · P2-4) |
| H16 | HX1 축 = 부위 | `ask_axis.py:83-104` `site_first` · `turn.py:759-767`(AX1 과 같은 문턱 `chat_ask_list_min` — 기존 설정 · 새 한도 아님) | ✓ |
| H1 | HF1 부위 거르개 끔 | `walk/calls.py:139-146`(contextvar `SITE_NAME_OFF`) · `material_read.py:96-103`(상담 `build_walk` 만) | ✓(상담 경로만 — 리포트 §5-2) |
| | HF2 holder 부위 가족 | `fetch_read.py:161-170`(코드 명시 → HF2 → 이름 명시) · `turn.py:831-864` `prep_case_sites`(케이스 부위 = 허브 `facets profile` site_name → 매핑 부위 이름이 하나인 코드) · `:879-891` · `:928-933` | ✓ · 케이스 부위를 매핑 `case_codes` 가 아니라 허브 GET 으로 얻음(P2-5) |
| H14a | HK1 안전 늘 | `material_read.py:31-46` `safety_always` · `:121` · `turn.py:987-989`(NQ6 에서 뺌) | ✓(상담 경로만 — §5-3) |
| H6 | HN1 층 없는 줄 = 행 대상 칸 · 재생 꼴 | `fetch_read.py:136-139` · `material.py:163-170` `_target_of` · `:247`(장부 `new_lines[].target`) | ✓ |
| H9 ~ H13 · 돌려 막기 · 가격 | HD1 ~ HD8 | `prompts/consult.json:96` · `:169-173` · `:195` · `:205` · `:221` · `:330` · `:396-401` | ✓ 원칙 문구 — **HD2 줄은 P1-1** |
| r3 P2-1 | `TOGETHER` → 1차 kinds | `kos_block.py:25-26` `TOGETHER_KINDS = {combo, same_day}`(1차 kinds 코드에 있음 — `prompts/consult.json:271-272`) · `turn.py:810-812` | ✓(시험이 상수만 봄 — P2-2) |
| r3 P2-2 | `score.py` 정답표 gold 비면 멈춤 | 리포트에 적힘(이번 검수 범위 밖 · 측정 파일) | — |

**더 한 것 · 빠진 것**:
- 스펙 밖 변경은 없다.
- 비용 쪽 변경(자료 줄이기 · 한도 · 가격 빼기) 0 · 새 숫자 한도 0(diff 숫자 grep — 기존 `OPTIONS_MAX` · `chat_ask_list_min` 만 씀).
- 화면 템플릿 · `items_view.py` · `ledger.py` · `llm/` 은 diff 0 이다.
- 장부는 칸이 더해지기만 한다:
  - `topic.question` · `asked_pick` · `out_pick` · `list_held` · `suspended` · `ha1` · `split_blocked`
  - `material_size.by_fetch.holder`
  - `new_lines[].target`
  - `tokens.calls[]` · `fetch` 칸의 기존 꼴은 그대로다.

## 3. 낱말 판정

- diff 의 `+` 줄에 새 낱말 튜플 · `any(w in question)` · 정규식이 없다. `nm in ctx.question` 한 줄은 기존 이름 명시 줄을 HF2 뒤로 옮긴 것이다.
- 물음은 부호 「?」, 같이 받기는 1차 kinds, 밖 · 없는 시술은 매핑 데이터로 판정한다.
- 리포트 §3 기존 자리 목록을 내 grep(짧은 한글 낱말 튜플 · `any(w in` · `_WORDS`)과 맞대 보았다. 상담 모듈 기준으로 `UNDO_WORDS` · `WIDEN_WORDS` · `PRICE_WORDS` · `TOGETHER` · `GENERIC_NAMES` 가 다 있고, 그 밖(`price.py` · `verify.py`)도 적혀 있다. `TOGETHER` 는 판정에서 빠졌다.

## 4. 결정 칸 연속 재생 시험(`tests/test_v07_spec012_topics.py`) — 정답표와 맞댐

| 시험 | 덮는 턴 | 기대값 | 정답표(`answers.json`) | 같음 |
|---|---|---|---|---|
| `test_s05_t1_to_t4…` | S05 T1 → T4 | T2 = LS1 · 목록 = T1 · 조건 볼 + 써마지 · `list_held` / T3 교체 · 볼 유지 / T4 복원 = T2 목록 · 표지 돌아옴 | T2 `same_as 1`(#10) · T3 `cond_keep [SITE-051]`(#11) · T4 `same_as 2` | ✓ |
| `test_s06_t1_to_t3…` | S06 T1 → T4 | T2 효과 칸 남김 + 쉼 · 셋 다 / T3 = T1 목록 · 효과 남김 / T4 둘 | T2 only 셋(#13) · T3 `same_as 1`(#14) · T4 only 둘 | ✓ |
| `test_spelling_and_typo…` | 「있어」 · 「잇어」 | 물음 아님 → 고르기 교체 · `_is_question` 넷 꼴 | #13 | ✓ |
| `test_hq1…` · `test_hq2…` | S10 T6 · S11 T6 · S09 T2 · T3 | 목록 그대로 · `asked_pick` · `out_pick` | `same_as` | ✓ |
| `test_s10_t3_t4_new_topic_after_ha1_site` | **S10 T3 만** | 새 주제 · 턱 주제 그대로 | #17 | ✓ — 다만 T4 없음 · HA1 을 거치지 않고 턱밑을 손으로 넣음(P2-1) |

시험이 구현을 베껴 너그러운가(표본 5):
- (1) S05 · S06 연속 시험은 장난감 셈 위에서 목록 · 칸 · 표지를 차례로 본다. 구현 상수를 다시 읽지 않는다 → 좋음.
- (2) `test_ha1_deterministic_sites` 는 다섯 꼴(자손 · 없음 · 같음 · 일반 · 여럿)을 따로 본다 → 좋음.
- (3) `test_hf2_case_holder_site_family` 는 턱 가족 · 종아리 · 계열 · 모름 · 명시 · 주제 부위 없음을 본다 → 좋음.
- (4) `test_kos_block_together_uses_understand_kinds_not_words` 는 상수 `TOGETHER_KINDS` 가 집합과 같은지만 본다. `turn.py:810` 의 판정 길은 안 탄다 → 너그러움(P2-2).
- (5) `test_v07_spec012_prompt.py` 는 구현이 넣은 문구가 있는지만 본다(스펙이 정한 방식). 금지 예문이 들어간 것을 잡지 못한다(P1-1 이 통과함).

## 5. 지적

### P1-1 HD2 프롬프트 줄이 채점 금지 문구를 예문으로 박음

- **근거**:
  - `prompts/consult.json:169`(system_v3)는 「…「값이 둘이다」 · 「~라고 적혀 있다」 · 「~라는 설명도 있다」 처럼 자료 · 출처 사정은 말하지 않는다」 이다.
  - 스펙 §3-C 머리는 「대본 문장 · 금지 낱말 목록을 프롬프트에 넣지 않는다(P2-8)」 이다.
  - 셋은 `quality/score.py` 기준 11 금지 정규식 「값이\s?(같이|둘\s?다|따로)」 · 「적혀\s?있」 · 「설명도\s?있고 … 설명도\s?있」 과 같은 말이다. 측정 말을 프롬프트에 그대로 넣으면 기준 11(C4 가 「오름」 을 요구하는 기준)이 원칙이 아니라 낱말 피하기로 오른다(다른 말투 「두 값이 나와요」 · 「자료마다 달라요」 는 그대로 나올 수 있음).
- **고칠 방향**:
  - 예문을 빼고 원칙만 둔다(「같은 대상 값이 줄마다 다르면 범위로 말하고, 값의 출처 · 자료 사정은 말하지 않는다」).
  - `test_v07_spec012_prompt.py` 에 「채점 금지 문구가 프롬프트에 없음」 시험을 더한다.

### P2

| # | 지적 | 근거 | 고칠 방향 |
|---|---|---|---|
| P2-1 | §3-D S10 T3 · T4 재생 시험이 T3 만 · HA1 을 거치지 않는다 | `test_s10_t3_t4_new_topic_after_ha1_site` 는 턱밑 부위를 손으로 넣고 `decide` 만 본다. HA1(`_concern_site_targets`)은 다른 시험이 따로 본다. T4(볼살만 → 볼 → 새 주제)는 없다. 스펙 C7 · WP-1 완료 조건은 「S10 T3 · T4 연속」 이다 | 가짜 kos · det 로 HA1 → `turn_conditions` → `decide` 를 이어 T3(턱 + 이중턱 / 이중턱만) · T4(볼 + 볼살 / 볼살만) 두 꼴씩 연속으로 돈다 |
| P2-2 | `TOGETHER_KINDS` 시험이 상수만 본다 | `test_kos_block_together…` 는 `TOGETHER_KINDS == {combo, same_day}` 만 본다. `turn.py:810-812`(장바구니 둘 이상 + kinds ∩ → 짝 줄 다시 싣기)와 옛 낱말 말 + kinds 빔 → 안 실음 은 시험이 없다 | `_kos_block` 길에서 「같이 받아도 돼」 + kinds [] → 안 실음 · kinds [combo] → 실음 둘을 본다 |
| P2-3 | HS1(일반 고민 → 하위 고민)이 시험 없음 | `_split_subs.concerns_for` 는 `det.concern` 의 `Result.upper`(`detect.py:131` 「물려받은 고민 행으로 온 고민」 · `:208`)를 하위 고민으로 쓴다. `upper` 에는 상위 고민 행도 들 수 있다. 부위가 있는 것만 남기므로 대개 하위로 걸러지지만, 이 가정을 보는 시험이 없다(리포트 §6 도 인정). S03 T2 r2 꼴이 이 길이다 | 가짜 det 에 하위 · 상위 고민 행을 섞어 「눈가 · 입꼬리 + 주름」 → 주제 둘(하위 고민 짝)을 본다. WP-4 실측 S03 T2 r2 를 따로 본다 |
| P2-4 | HU1 보강이 스펙 글과 다르다 | 스펙 HU1 은 「사진에 없는 값이 있으면 교체」 이고, 구현(`topics.py:316-325`)은 「새 값이 고르기 칸에만 → 교체 · 부위 · 고민에도 → 되돌린 뒤 적용」 이다. 결정 #11 · §3-D 칸은 그대로다(S05 T3 · T4 · S11 T4 · T5 를 코드로 따라감 — 깨짐 0). 다만 스펙과 코드가 다르다 | 스펙 0.1.3 에 보강 규칙을 옮겨 적는다(코디). 「아니 이마에 써마지」 꼴 시험은 `test_hu1_site_correction_still_undoes` 에 있다 |
| P2-5 | HF2 케이스 부위를 허브 GET 으로 얻는다 · 호출 수가 장부에 없다 | 스펙은 「명동점이면 매핑 `hub.case_codes` → 케이스 부위」 이다. 구현(`turn.py:831-864`)은 케이스 holder 마다 허브 `facets profile` 1 회다(gold 별 프로세스 캐시 · 부위 이름이 매핑에서 하나일 때만). 기준 S08 T1 같은 턴은 케이스 holder 81 개다(부작용 · GET 셈) → 첫 턴에 GET 수십 번이 늘 수 있다. `case_site_calls` 를 세지만 장부에 안 남긴다. C6 「비용 · 크기는 기록만」 에 허브 호출 수도 드는 게 맞다 | 명동점 케이스는 매핑 `case_codes` · 매핑 부위로 먼저 정하고, 매핑 밖 케이스만 GET 한다. `case_site_calls` 를 장부 `consult.fetch` 에 적는다 |

## 6. 깨질 자리

- **화면**:
  - 템플릿 · 정적 파일 · `items_view.py` diff 0 · `items` 꼴 그대로다.
  - 표지 칸(`list_held` · `out_pick` · `asked_pick` · `suspended`)은 `kos_block.cond_view` 의 3차 조건 줄에만 더해진다(화면 문구 0).
  - 스크린숏 `e2e-shots/spec012-home.png` · `spec012-face-check.png` 를 열어 보았다(얼굴 점 확인 화면이 그려짐). 대화 화면(주제 · 목록 · 모달 · 장바구니)은 LLM 이 있어야 열리므로 WP-4 실측에서 볼 몫이다.
- **장부**: 칸은 더해지기만 한다. `tokens.calls[]` · `fetch` 칸의 기존 키는 그대로다(diff 에 그 코드 없음).
- **HK1**: 모든 상담 턴에 안전 종류 셋이 붙어 자료가 커진다(스펙 D3 「기록만」 · `kinds_by` 에 `safety_always` 로 남음). NQ6 오작동은 `turn.py:987-989` 로 막았다.

## 7. 프롬프트(볼 것 6)

- HD1 · HD4 · HD6 · R16 ~ R21 은 원칙 문구다. 「물은 종류에서만」 범위는 HD6 에 「손님이 물은 종류는 … 묻지 않은 안전 줄은 먼저 꺼내지 않는다」 로 들어가 있다.
- HD1 「같은 날 받기는 원장님이 상태를 보고 정한다는 뜻으로」 는 뜻 지정이라 대본은 아니다. 다만 고정 문장으로 굳지 않는지 WP-4 에서 기준 16 으로 본다.
- 문제는 HD2 의 금지 예문(P1-1) 하나다.
