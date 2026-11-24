# 검수 — SPEC-010 WP-3 · D1 고침 · WP-3b 코드 · 2026-11-20

reviewer 워커 · 읽기만(수정 0). 대상은 `clinic_chat/phub-consult-demo` 미커밋 변경 가운데 `detect.py` · `topics.py` · `ask_axis.py`(새)와 `turn.py` · `verify.py` · `understand.py` · `prompt.py` · `entry_list.py` · `ledger.py` · `server.py`(`/topic`) · `prompts/consult.json` 고친 곳이다. 기준은 SPEC-010 0.2.7 §5-0 · §5-0b · §5-1 ~ §5-4 · §13 WP-3 · WP-3b, 리포트 `wp3-report.md` · `wp3b-report.md`, 코디 판단 D1 (가)다. 18222 손대지 않음 · 실제 이해 호출 0(리포트 실물 표를 코드 · 허브 셈으로 대조).

## 판정 — **FAIL**(P0 0 · P1 1 · P2 5)

주제 판단 · 합치기 · 되돌림 · 저장 · 재기동 복원 · reach 「케이스 직접」 만 · 효과 길 · NM · SF · LS · D1 (가) · 축 고르기는 스펙과 같다. 시험 45 개가 그 계약을 막는다. FAIL 까닭은 하나다. 허브 오류 하나가 목록 전체를 0 으로 만들고, D1 (가)가 그 값을 주제에서 지운다. 스펙 §5-2(「그 근거만 빼고 나머지로」)와 반대인데, 시험이 그 반대 동작을 단언하고 있다. 몇 줄 고침이면 된다.

## 1. 다시 돌린 것

| 명령 | 결과 |
|---|---|
| `pytest -q tests/test_v05_detect.py tests/test_v05_ask_axis.py` | **45 passed**(33 + 12 — 리포트 13 · 셈 차이는 파라미터 없이 함수 수) |
| §13 WP-3 회귀 목록 + v05_page · kos_map + 0.4 화면 · 장부 · 프롬프트(`test_consult_{turn,listing,carry,page,ledger,prompt}` · `test_v04_{list,prompt,ledger,verify,understand,turn}` · `test_state_{carry,blanks}` · `test_answer_key`) | **162 passed · 1 skipped · 1 failed** — 실패는 `test_consult_page::test_t17`(코드 한글 0)이고 잡힌 파일은 **`modal.py`** 다. 이 파일은 WP-4 워커가 같은 워크트리에 17:48 에 새로 둔 것이다(`images.py` 도 같음). WP-3 · 3b 파일은 걸리지 않았다(P2-3) |
| `$J` 진료항목 제품 서로 다른 수 | 62(국가 첫 셈 때 허브 facets 호출 상한 — P2-4) |

## 2. 계약 대조

| 계약 | 코드 | 판정 |
|---|---|---|
| CD1 · CD2 칸 · 같은 칸 교체 · CD4 거둠 · CD5 method · material 밖 | `topics.py:44-96` · `detect.py:19-29` | 맞음 |
| 「이번 턴 조건」 = follow 로 채운 대상 뺌(r6 P2-4) | `topics.turn_conditions:52` | 맞음 |
| TP2 A · B · TP3 순서 2 ~ 7 · TP5 조건 ≥ 1 일 때만 · TP4 「또」 낱말 경계 | `topics.decide:202-237` · `TTO_RE:27` | 맞음(조건 0 이면 202 에서 먼저 나감) |
| TP11 같은 조건 주제 = new 뒤 후처리 · `rule_move = return` | `topics.py:240-250` | 맞음 |
| TP14 ① ~ ⑤ · TP6 `cond_dropped`(LLM 대상 ≠ 규칙 대상이면 조건 안 더함) · `add_zero` | `topics.py:204-206` · `252-279` | 맞음 |
| TP12 저장 상태 그대로 되살림 · TP10 장부 한 정의 · `topic_switch` 가 덮음(r6 P2-3) | `topics.py:265-279` · `ledger.py` `last_topics` · `topic_override` | 맞음 |
| TP13 이해 호출 `topic` 칸 · 검증(셋 밖 = 없음 · 앞 주제 아닌 `to` = null) · `parsed_view` · 턴 메시지 주제 블록 · 머리 키 선택(필수 밖) | `verify.py` `topic_of` · `understand.py` `topic_lines` · `prompt.py` `PICK_HEADER_OPTIONAL` | 맞음 |
| §5-1 ④ 고민 = reach 「케이스 직접」 · `candidate_table = procedure_case` 만 · 나머지는 `dropped_reach` 셈 | `detect.py:155-168` | 맞음 |
| 효과 = 케이스 · 시술 행만(N2) | `detect.py:186-197` | 맞음 |
| NM2 ~ NM6 | `detect.py:79-115` | 맞음(리포트 D5 — 긴 낱말 안 이름도 맞음, 지켜봄) |
| SF2 · SF3 | `detect.py:199-219` | 맞음 · 몸 조상 = 조상 전부(SITE-147 · 001 · 중간 단) — 리포트 D2, 스펙 한 줄 거리 |
| CZ1 | `detect.py:279-280` · 국가 292 | 이름 일치 밖 전부 — 리포트 D3, 스펙 한 줄 거리 |
| LS1 ~ LS3 · LS2 역순 · all · **D1 (가) 막은 값은 칸에서 빼고 `blocked` 에만** | `topics.py:290-320` · 시험 `test_d1_…` · C4 단언 | 맞음 |
| §5-4 AX1 ~ AX6 · N13 · N14 · AX7 표본 셋 | `ask_axis.py:24-189` · 시험 AX7 ① ② ③ | 맞음(X1 캐시 채움 · X2 `consult.ask_axis` 는 스펙 한 줄 거리) |
| 장부 가격 0 | `items_rec`(코드 · 칸 · 이름 일치 진료항목 코드) · `ask_axis`(값 · 이름 · 수)에 가격 칸 없음 | 맞음 |
| 실물 표본(리포트 §3) | 팔자주름 23 · 턱살 5 · 기미 27 · 리프팅 130 · 미백 4 · 써마지 5 · T6 B(종아리 ∩ 쥬비덤) 0 — 스펙 기대와 같고, 기미 · 다한증 · 써마지는 r6 때 내가 허브로 센 값과 같음 | 맞음 |

## 3. 지적

### P1-1 허브 오류 하나가 목록 전체를 0 으로 만들고, D1 이 그 조건을 지운다
- `detect.py:263-265`: 값이 오류면 `set()` 을 돌려준다. `detect.py:276-287` 은 그 칸의 빈 합집합을 `sets` 에 넣고, `302` 의 교집합이 **0** 이 된다. 스펙 §5-2 「허브 오류가 나면 그 근거만 빼고 나머지로 짓는다」 와 반대다. 시험 `tests/test_v05_detect.py:294-299` `test_hub_error_drops_that_basis_only` 는 이름과 달리 `r.codes == []` 를 단언해 이 동작을 굳히고 있다.
- 결과가 번진다. A = B = 0 이 되어 LS 를 탄다(`topics.py:290`). LS2 는 오류 난 칸을 「막은 칸」 으로 찾고, D1 (가)(`topics.py:314`)가 **손님이 말한 고민을 주제 칸에서 지운다**. 허브가 잠깐 느렸을 뿐인데 조건이 영구히 사라지고, 장부 `blocked` 는 「그 조건 때문에 0」 으로 남는다.
- 고칠 방향(셋 다 하는 게 좋다).
  - 오류 난 **값**은 그 칸 합집합에서만 빠진다. 칸의 모든 값이 오류면 그 칸을 교집합에서 뺀다(`sets` 에 넣지 않음).
  - `Result.errors` 가 있으면 `decide` 는 LS 칸 지우기(D1)와 자동 새 주제를 하지 않는다. 지금 주제 · 칸을 그대로 두고 장부에 `errors` 만 남긴다.
  - 시험을 「오류 난 고민은 빼고 시술 칸만으로 `ZZ-BTX-A`… 를 냄」 으로 바꾸고, 「오류 턴 뒤에도 주제 칸에 고민이 남음」 을 하나 더한다.

### P2-1 TP11 주제 수 한도가 화면에만 걸린다
- `chat_topic_max` 는 `topics_view`(화면)에서만 쓴다(`turn.py:456` · `server.py:128` · `fake_turn.py:153`). `decide` 의 주제 목록, 이해 호출 턴 메시지의 앞 주제 블록(`turn.py` `_topic_brief`), 장부 `consult.topics` 는 끝없이 는다. 그래서 화면에서 빠진 주제도 LLM `to` 로 되돌릴 수 있다.
- 고칠 방향: 스펙 TP11 「목록에서 뺀다(장부에는 남음)」 의 「목록」 이 화면만인지, LLM 블록 · 되돌림 대상까지인지 코디가 정한다. 후자면 `_topic_brief` · `prev_topic_ids` 도 한도 안 주제만 넘긴다.

### P2-2 첫 턴 LS「all」 이면 빈 주제 t1 이 생겨 남는다
- `topics.py:281-285` · `309-314` — 첫 턴(주제 없음)에 다 빼도 0(`blocked all`)이면 조건 · 진료항목이 빈 주제 t1 이 만들어진다. 다음 턴은 t1 안에서 이어지므로 셈은 맞다. 다만 그 뒤 새 주제가 생기면 t1 이 머리 글 없는 「0」 앞 주제로 화면 · LLM 주제 블록에 남는다.
- 고칠 방향: 조건이 빈 주제는 만들지 않거나(TP1 「첫 조건이 들어온 턴에 주제 1」 — 막혀서 칸에 남은 조건이 0 이면 아직 주제 없음), 새 주제가 생길 때 빈 주제를 걷는다.

### P2-3 같은 워크트리에서 WP-4 가 돌고 있어 0.4 T17 이 깨져 있다
- 지금 `test_consult_page::test_t17` 이 `modal.py`(WP-4 · 17:48 새 파일)의 한글로 실패한다. WP-3 · 3b 리포트 시점(17:39 · 17:46)에는 없던 파일이다.
- 고칠 방향: WP-4 워커가 `\u` 이스케이프나 `ui_text` 로 옮긴다. WP-3 쪽 할 일은 없다. 코디는 WP-4 검수 때 T17 을 회귀 목록에 넣는다.

### P2-4 국가 조건 첫 턴에 허브 호출이 상한 없이 최대 62 번 난다
- `detect.py:228-242` — `country()` 는 모든 진료항목의 모든 제품에 `facets profile` 을 부른다(서로 다른 제품 62 · 프로세스 캐시 뒤에는 0). 축 셈(AX6 40)과 달리 한도 · 표지가 없다. 리포트 C5 실물 턴의 호출 수도 적혀 있지 않다.
- 고칠 방향: 지금은 동작에 문제가 없다(캐시가 gold_hash 키). 국가 셈을 다른 칸 교집합 안의 진료항목 제품으로 좁히거나, 첫 호출 수를 장부 `hub_calls` 로 확인해 리포트에 적는다.

### P2-5 스펙으로 옮길 것(리포트가 올린 것 · 코드는 그대로 둔다)
- §5-1 ⑥ LS3 · C4 문구를 D1 (가)로 바꾼다(코디가 이미 「곧 고침」).
- SF3 몸 조상 = 조상 전부(SITE-147 · SITE-001 · 중간 단)(D2).
- CZ1 = 이름 일치 밖 모든 값(D3).
- SF1 부위 칸 출처 = 이해 결과 site 대상(D4).
- AX6 빠지는 턴에도 한도까지 캐시 채움(X1).
- 장부 `ask` → `consult.ask_axis`(X2).
- 주제 id 꼴 `t<n>`(D8).

## 4. 남은 것(지적 아님)
- TP12 「데이터 판이 바뀐 재시작이면 다시 셈」(리포트 D6) — 아직 안 했다. WP-7 · 다음 판으로 넘긴다.
- 봇이 주제 바뀜 · 막은 조건을 말하는 것(TP7 · R11 · LC7)은 WP-6 이다.
- pick 규칙 13 ~ 15 · 주제 머리 글은 초안이고 사용자 확인 대상이다.
- 회차 · 대상 축은 자리만 있다. 값은 WP-5 가 넣는다.
