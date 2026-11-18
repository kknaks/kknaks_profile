---
type: spec
id: SPEC-008
title: "상담 채팅 0.4 — 상담 입구 소넷 전환: 켠 상태의 턴에서 Jev 와 resolve 맞춤 꼴을 걷어 내고 소넷 「이해」 호출 하나(대상 · 턴 종류 · 이번 턴 부위 · 거둠 · 정보 종류)로"
status: draft
product: procedure-hub
feature: phub-gold-jev
version: 0.2.1
created_at: 2026-11-18
updated_at: 2026-11-18
tags:
  - product/procedure-hub
  - feature/phub-gold-jev
  - doc/spec
  - status/draft
links:
  decisions:
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-18 0.2.1 근거 행 — 「앱 0.4 코드 검수 WARN 코디 답」(L-1 · L-2 · M-1 · L-8) · 「E8-0: CLI 로는 thinking 완전히 못 끔」 · 「상담 0.4 결과 = 이 정도면 받음 · thinking 은 SDK 에서 끈다」) · §5 「앱 fix1」 · review-code-app-v04.md · WORK-017 §B · 앱 `296cb2c` (구현 결과가 정본) · research-input-space/runs/v04c-score · v04d-score"
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-18 — 「SPEC-008 검수 WARN 16 코디 답」: F-1 ⓒ · F-5 · F-6 · U8-1 (가) · U8-2 90% · F-8 · F-9 · F-10 · 나머지 리포트대로) · review-spec-008.md (검수 F-1 ~ F-16) · spec-008-fix1-brief.md (0.2.0 발주서)"
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-18 — 「상담 입구 결정 표 D-1~D-15 확정(추천 그대로 · 코드 구현까지 진행)」)"
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-18 — 「상담 판단은 소넷으로만 — Jev 를 뺀다(대상 확정 · 턴 종류 · 입구 고르기 · 거둠 + 정보 종류 14 · 범위 밖 · 값 고르기 · 깊이 판단까지)」)"
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-18 — 「허브 resolve = 최소 목록 꼴(입구 목록 출력) · 규칙을 더하지 않는다 · 입력 정리는 채팅(앱) 단에서」 · 「resolve(글자 맞춤) 를 후보 관문에서 뺀다 → 소넷이 대화 맥락으로 gold 목록 안에서 후보를 뽑는다」)"
    - "orchestration/work/phub-gold-jev/spec-008-brief.md (발주서 — 절 구성 · 보조 근거)"
  sources:
    - "orchestration/work/phub-gold-jev/research-input-space.md (입력 전수 표 · 실패 층 · AR-1 ~ AR-12 · DA-1 ~ DA-6 · §3 소넷 시안)"
    - "orchestration/work/phub-gold-jev/research-input-space/pick-prompt.md (시안 프롬프트 · 호출 인자 · 목록 꼴) · conversations.jsonl · now-turns.jsonl"
    - "orchestration/work/phub-gold-jev/review-input-space.md (검수 WARN — R-1 ~ R-11 · 「빠진 정할 것」 7)"
    - "orchestration/work/phub-gold-jev/SPEC-006-consult-v03.md (0.1.0 — 고치지 않는다) · SPEC-005-consult-state.md · SPEC-004-consult-chat.md"
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md (0.8.0 — §4-1 목록 꼴 · §4-5 `sites[]` · `site_applied`)"
    - "orchestration/work/phub-gold-jev/SPEC-002-chat-eval.md (걷기 ① ~ ③ — 시험 앱 B 열 · 고치지 않는다)"
    - "clinic_chat 워크트리 phub-gold-jev (HEAD be1c622 · 읽기만) — clinic_chat/consult/ · clinic_chat/walk/ · clinic_chat/columns/col_b.py · clinic_chat/llm/chat_cli.py · prompts/consult.json"
  related:
    - "orchestration/work/phub-gold-jev/SPEC-006-consult-v03.md"
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md"
---

# SPEC-008 — 상담 채팅 0.4 · 상담 입구 소넷 전환

경로 접두어: `$W` = 이 폴더 · `$A` = clinic_chat 워크트리 `phub-gold-jev`(읽기만 · HEAD `be1c622` = 상담 0.3) · `$H` = PROCEDURE-HUB 워크트리 `phub-gold-jev`(읽기만 · HEAD `d97a9ad`).
「조사」 = `$W/research-input-space.md` · 「검수」 = `$W/review-input-space.md` · 「시안」 = `$W/research-input-space/pick-prompt.md` · 「표」 = 입력 전수 표 `$W/research-input-space/conversations.jsonl`(판마다 수가 바뀐다 — 이 문서는 고정 수를 끝 조건에 쓰지 않는다 · 0.2.0 을 쓸 때 78 대화 · 356 턴 · 애매 18 · 스크립트 = `$W/research-input-space/scripts/` · README) · 「조사 판」 = 조사가 잰 255 턴 판(§1-1 의 수) · 「0.3」 = SPEC-006 과 그 구현.
줄마다 상태를 적었다: **결정** = `_RESUME` §2 11-18 행(D-1 ~ D-15 · 「소넷으로만」)에 있다 · **사실** = 코드 · 조사로 확인한 것 · **제안** = 이 워커의 제안(코디 · 사용자가 정한다 — §9).
**SPEC-004 · 005 · 006 은 고치지 않는다.** 닿는 곳은 §5 · §6 에 모았다. 이 워커는 서버 · DB · LLM · Jev 를 부르지 않았다 — 수는 전부 조사 · 검수의 것이고, 표의 수는 `build.py` 가 낸 것이다.
프롬프트 문구(§7)는 **초안**이다(사용자 확인). 화면 문구는 새로 짓지 않았다 — 새 빈 자리는 **하나**(CP7 옛 끈 대화의 새 턴을 막는 자리 · 문구 = U8-3 · 비워 둔다).

## 0. 요약

| 무엇 | 이 스펙이 정하는 것 |
|---|---|
| 무엇을 빼나 | 켠 상태(`CHAT_STATE=on`)의 턴에서 **Jev 요청 전부**(맨 앞 판단 · 입구 고르기 · 거둠 · 턴 종류 · 값 고르기 · 깊이 · `answer_ready`)와 **허브 `resolve` 맞춤 꼴 호출 전부** |
| 무엇으로 | 턴마다 소넷 **「이해」 호출 하나** — 시스템 글 = 규칙 + gold 목록(820 항목 + 별칭) · 턴 메시지 = 대화 + 객체 + 이번 말 → JSON `{targets[{table, code, sure}], kind, sites[], withdraw[], kinds[], out}` |
| 앱이 하는 것 | 출력 검증(gold 에 없는 코드 버림) → 객체 갱신 → 조회(부위 거르개 = 이번 턴 부위만) → 화면(점 = 말한 고민 부위만) → 빈 칸 · 되묻기 → 답(소넷 · 지금 그대로) → 장부 |
| 답 재료 | 걷기 ②(폭 읽기 — 대상 × 정보 종류 → 허브 조회)의 **결정론 함수는 그대로 부른다**. 객체 기준 조회는 리스트 · 선택지 · 시너지만 덮는다(§3) |
| 값 고르기 · 깊이 | 소넷 호출을 **더하지 않는다** — 깊이는 「이번 턴 대상인 후보만 깊이 읽기」 로 이해 호출이 대신하고, 값 고르기 표지는 없앤다(§3 · **U8-1 (가) 확정** — 코디 11-18). 표에 재료 정답 키(`key.material`)를 22 턴 보탰다(§8-2 E8-6b) |
| 실패 | 이해 호출이 10초를 넘거나 오류 · JSON 깨짐 → 대상 없이 되묻기. 옛 resolve 길로 돌아가지 않는다(D-10) |
| 범위 밖 | 시험 앱 B 열 — 옛 판 그대로(D-2). **끈 상태 = 0.4 서버에서 새로 열지 않는다**(옛 끈 대화 = 읽기만 · CP1 · CP7 — 코디 F-1 ⓒ). `walk/` · `columns/` 의 기존 함수 동작 · 시험은 바뀌지 않는다(`walk/` 에 얇은 공개 감쌈을 더하는 것만 예외 — CP3 · §3-4) |
| 완료 | 표 재실행 — 앱 전체 8 검사 90%↑ · 입구 3 검사 95%↑(D-14) · 정보 종류 90%↑(U8-2) — 분모는 실행 때 `score.py` 가 낸 채점 턴 수 |

## 1. 목적 · 범위

### 1-1. 왜

| # | 본 것(조사 판 — 255 턴 · 채점 239 턴 · 그때의 수다 — 지금 표의 끝 조건 분모가 아니다) | 수 |
|---|---|---|
| P1 | 지금 시스템 통과 | 115 / 239(48%) · 실패 층 = 후보 39 · Jev 43 · 앱 규칙 39 · 데이터 3 |
| P2 | 후보 층 — resolve 글자 맞춤이 관문이라 정답이 후보에 없다(조사 끼임 · 어순 · 바꿔 말하기) | 39 턴(「고민+부위」 19 턴 가운데 16) |
| P3 | Jev 층 — 후보에 있는데 점수로 떨어짐 16 · 턴 종류 `new` 로 11 · 엉뚱한 것 yes 9 · 그 밖 7 | 43 턴 |
| P4 | 입구 고르기가 돈 턴의 지연 | 36 턴 중앙 7,378ms(Jev 35 요청) · 맞힌 것 9 / 29 |
| P5 | 소넷 + 별칭 시안(입구 3 검사) | 대상 정답 97.1%(엄격 채점 92.5 ~ 94.1% — 검수 R-3) · 턴 종류 97.5% · 부위 99.2% · 지어낸 코드 0 / 375 · 중앙 2,852ms |
| P6 | 앱 규칙 층 · 데이터 층은 입구를 바꿔도 남는다(검수 R-7) | 39 + 3 턴 — §5 의 AR 처분이 그 몫이다 |

### 1-2. 정해진 것(다시 묻지 않는다)

| # | 정해진 것(`_RESUME` §2 11-18) | 이 문서에서 |
|---|---|---|
| D-1 | 허브 resolve 는 목록 꼴 그대로 · 맞춤 꼴은 정확한 이름 → 코드만 | §2-1 · SPEC-001 0.8.0 |
| D-2 | 시험 앱 B 열은 허브 0.7.2 옛 판에 묶고 안 고침 — 이번 일 = 상담만 | §1-3 · CP1 ~ CP3 |
| D-3 | 목록에 별칭을 넣는다 | LD3 · LD4 |
| D-4 | thinking 끔 · CLI 그대로(배포 전 SDK) | UC2 · UC3 |
| D-5 | 말하지 않은 고민을 붙이지 않는다 | §7 규칙 3 · OU6 |
| D-6 | 고민만 답 → **바로 앞 턴이 부위만일 때만** 그 부위를 잇는다 — 「답」 = **앞 턴 되물음(ask)에 대한 답**(코디 11-18 F-5) | OU7 |
| D-7 | 같은 이름이 여러 표 = 가장 넓은 것 하나(계열) | VF4 · §7 규칙 4 |
| D-8 | 맥락에 앞 답 요약 · 보여 준 리스트 이름을 넣는다 | UC6 |
| D-9 | 소넷이 대상마다 확실 / 애매 표지 → 애매 = `guess` + 되묻기 | UC8 · OU2 |
| D-10 | 10초 넘음 · 오류 = 대상 없이 되묻기(옛 resolve 로 안 돌아감) | §4-1 |
| D-11 | 정보 종류는 소넷이 같은 호출에 · 값 고르기 · 깊이 판단은 SPEC 에서 소넷 꼴로 정하고 표에 정답 키를 보탠다 — 코디 11-18: U8-1 (가) · 정보 종류 = 있는 키로 · 문턱 90%(U8-2) · 값 · 깊이 정답 키 20 턴↑ 보탬 | UC8 · §3 · §8-2 |
| D-12 | `new` 에 앞 대상을 다시 든 것 = 군더더기 아님 · 객체가 안 바뀌면 재조회 없음 | OU5 · QS4 |
| D-13 | 데이터 DA-2(눈 ↔ 눈 주변) 먼저 · DA-1 은 조회 규칙 · DA-4 · DA-5 는 원장 확인 뒤 | QS6(DA-1) · 데이터는 이 문서 밖 |
| D-14 | 완료 = 앱 전체 8 검사 90%↑ + 입구 3 검사 95%↑ · 정답 키 꼴마다 표본 사람 검수 | §8-1 |
| D-15 | 애매 14 턴은 채점 밖(표본 검수 때 같이) · 턴당 값은 SDK 때 — 「14」 는 조사 판의 수다. 지금 표는 애매 18 → 채점 밖 = 표의 `ambiguous` 턴 전부(실행 때 수) | §8-1 |
| D-16 | 상담 판단은 소넷으로만 — Jev 를 뺀다 · 모델 소넷(하이쿠 비교 안 함) | §2 전부 |

| F 답 | SPEC-008 검수 WARN 16 코디 답(F-1 ⓒ · F-5 · F-6 · F-8 · F-9 · F-10 · 나머지 리포트대로) | CP1 · CP7 · OU7 · §8-2 · VF8 · OU9 · §3-4 · 변경 기록 0.2.0 |

(D-16 은 결정 표의 「소넷으로만 — Jev 뺌」 행에 이 문서가 붙인 번호다. 「F 답」 은 11-18 「SPEC-008 검수 WARN 16 코디 답」 행이다.)

### 1-3. 범위 · 범위 밖

| # | 규칙 | 상태 |
|---|---|---|
| CP1 | 이 스펙이 바꾸는 것은 **켠 상태 대화의 턴 흐름**(`$A/clinic_chat/consult/turn.py` 의 `Consult` 가지)이다. **끈 상태 대화(`consult_state` = `off`)는 0.4 서버에서 새로 열지 않는다** — `chat_state` 기본값 = `on`(지금 `config.py:82` 의 `"off"` 를 바꾼다) · 끈 상태로 시작하는 새 대화는 없다(`CHAT_STATE=off` 를 주어도 새 대화는 켠 상태로 연다 — CP7). 까닭: 끈 상태는 0.1 그대로 `walk()` → `front()` 로 맞춤 꼴에 손님 문장을 넣는데(`walk/front.py:225-226`) 상담 서버의 허브 주소는 하나다(`config.py:41`) — 허브 0.8.0 에서 끈 대화는 후보가 사실상 0 이 된다(검수 F-1 · SPEC-001 0.8.1 영향 표) | 결정(코디 F-1 ⓒ) |
| CP2 | **코드 경로를 나눈다.** 켠 가지는 `walk()`(`$A/clinic_chat/columns/col_b.py:161`) · `front()`(`walk/front.py:210`) · `cst.retract()`(`consult/state.py:261`) · `tk.judge()`(`consult/turn_kind.py:60`) · `value_pick.run()` · `walk_depth()` 를 **부르지 않는다**. 걷기의 결정론 함수(`plan_calls` · `read_calls` · `build` · `roster` · `check` · `_labels` · `same_day_marks` · `_end_check` · `es.decide` · `mat.renumber`)는 **고치지 않고 부르기만** 한다(0.2 의 `plan.Reader` 가 `read_calls` 를 부르는 것과 같은 꼴) | 결정(D-2) · 함수 목록은 사실(코드) |
| CP3 | `$A/clinic_chat/walk/` · `clinic_chat/columns/` · `prompts/jev/` 아래 **기존 함수의 동작 · 기존 시험은 바뀌지 않는다**(시험 S8-T18). 예외 하나: §3-4 의 함수 서명이 상담 쪽에서 맞지 않는 자리에 한해 **`walk/` 에 공개 함수(기존 함수를 부르기만 하는 얇은 감쌈 · 동작 변경 0)를 더하는 것은 된다**(코디 F-10). `columns/` · `prompts/jev/` 는 diff 0 그대로다. 걷기 코드를 상담 쪽에 베끼지 않는다(두 벌 금지). 0.3 이 `walk()` · `front()` 에 더한 선택 인자(`entry_pick` · `abbr_yes_only`)는 부르는 곳이 없어지지만 지우지 않는다 | 결정(D-2 · 코디 F-10) · 「지우지 않는다」 는 제안 |
| CP4 | 시험 앱 B 열 · C 열 · 답 키 명세 · 속도 탭은 범위 밖이다. B 열을 어느 허브 판에 묶는지는 SPEC-001 0.8.0 변경 기록의 영향 표 | 결정(D-2) |
| CP5 | 답 LLM(CLI · 소넷 · `--resume`) · 상담 프롬프트 `system_v3` · 끝맺음 · `empty` · 리스트 꼴 · 화면 네 칸 · 드로어 · 패널 틀은 0.3 그대로다 | 결정(발주서 ⑧ 「지금 그대로」) |
| CP6 | 데이터 보강(DA-2 · DA-4 · DA-5) · SDK 전환 · 턴당 값 · 실서버 지연은 이 문서 밖이다(D-13 · D-15 · 검수 R-10) | 결정 |
| CP7 | **옛 끈 대화**(0.4 이전에 `consult_state` = `off` 로 시작된 대화 — 장부 첫 줄의 `consult_state`): 열면 「옛 판 대화」 로 **읽기만** 한다 — 지난 턴 · 드로어는 0.1 꼴 그대로 보이고 **새 턴은 받지 않는다**(`POST …/turns` 를 막는다 — 켠 rev 3 대화의 `rev_changed` 와 같은 자리 · C8-4). 막는 화면 문구는 **빈칸**이다(새 `data-slot` 하나 — 문구는 U8-3). 끈 상태 코드(`turn.py:125` 의 `walk()` 가지)는 지우지 않는다 — 0.4 서버에서 부르는 곳이 없어질 뿐이다(CP3 과 같은 꼴) | 결정(코디 F-1 ⓒ) · 막는 자리를 `rev_changed` 꼴로 = 제안 |

## 2. 새 턴 흐름

```text
POST …/turns
  ① 목록 적재      허브 resolve 목록 꼴 → 입구 목록 글(gold_hash 마다 한 번)
  ② 이해 호출      소넷 1 회 → JSON
  ③ 앱 검증        없는 코드 버림 · 같은 이름 접기 · 값 고침
  ④ 객체 갱신      sure → said · 애매 → guess · 거둠 · 부위 잇기 · focus
  ⑤ 조회          객체 기준 조회(리스트 · 선택지 · 시너지) + 답 재료 조회(대상 × 정보 종류)
  ⑥ 화면          list · sites(LLM 을 기다리지 않음)
  ⑦ 빈 칸 · 되묻기  ask 하나 · close 하나
  ⑧ 답            CLI 소넷 --resume(0.3 그대로)
  ⑨ 장부
```

0.3 은 걷기(① resolve + Jev)와 가르기 · 거둠 요청을 **함께** 띄웠다(`turn.py:326-385`). 0.4 는 ② 가 끝나야 ④ ⑤ 가 설 수 있어 **차례로** 돈다 — 턴의 앞머리 값은 이해 호출 하나의 시간이다(조사: 중앙 2.9초 · 개발 Mac · CLI · thinking 15% 켜짐 조건 — 실서버 수가 아니다 · 검수 R-10).

### 2-1. ① 목록 적재

| # | 규칙 | 상태 |
|---|---|---|
| LD1 | 입구 목록 = 허브 `resolve` **목록 꼴** — `tables` = `concern` · `site` · `modality` · `procedure` · `product`(`text` 없음) 를 `next_cursor: null` 까지 넘긴 `g_entry` 행 전부. 허브 계약은 SPEC-001 §4-1 「목록 꼴」 그대로다(0.8.0 에서 안 바뀐다) | 결정(D-1 · D-3) |
| LD2 | 개념 하나 = (`entity_table`, `entity_code`) 하나. 이름 = `entity_name` · 별칭 = 그 개념의 다른 행 `text` 가운데 이름과 글자가 다른 것(행 순서 그대로 · 같은 글자는 한 번). 11-16 gold 에서 **820 항목**(고민 260 · 부위 89 · 계열 18 · 시술 138 · 제품 315 — 조사 §3) | 사실(조사) · 별칭 식은 제안(시안의 목록과 같은 꼴인지 E8-1 로 대조) |
| LD3 | 목록 글의 꼴 = 시안의 「# 목록」 그대로: 표마다 머리 `## <표 한국어 이름> (table = <entity_table>)` · 줄마다 `<코드> <이름> (= <별칭>, …)`(별칭이 없으면 괄호 없음). 표 순서 = 위 LD1 의 순서 · 표 안 순서 = **허브가 낸 순서 그대로**(앱이 다시 정렬하지 않는다) | 결정(D-3) · 꼴은 사실(시안) |
| LD4 | `CHAT_PICK_ALIASES` = `off` 면 괄호(별칭)만 뺀다(견줌용 — 조사: 별칭을 빼면 대상 정답 97.5 → 93.4%) | 제안 |
| LD5 | **캐시** = 프로세스 메모리 · 키 = 허브 응답 머리의 `gold_hash`. 대화의 `gold_hash`(`Conv.gold_hash`)와 캐시 키가 다르면 다시 받는다. 목록 글은 같은 `gold_hash` 에서 **글자가 같아야** 한다(결정론) — 시스템 글이 같아야 프롬프트 캐시가 맞는다(조사: 입력 14,842 토큰 가운데 캐시 읽음 14,012) | 결정(발주서 「gold_hash 단위 캐시」) · 까닭은 사실(조사) |
| LD6 | 목록 글의 sha256 을 장부 `consult.understand.list_sha` 에 남긴다(어느 목록으로 뽑았는지) | 제안 |
| LD7 | 목록 적재 실패(허브 오류 · 쪽 넘김이 안 끝남) → 그 턴은 §4-1 의 실패 길(`error.kind` = `list`)이다. 반쪽 목록으로 이해 호출을 띄우지 않는다 | 제안(D-10 과 같은 길) |
| LD8 | 목록은 다섯 표뿐이다 — 사건(`adverse`) · 조건(`condition`) · 효과(`effect`) · 재료 · 방법 · 해부 · 케이스 · 패키지 · 상품은 **이해 호출의 대상이 아니다**(조사의 채점도 「다섯 표만 센다」). 그 표가 앞 대상이던 0.1 CR1 의 길(SPEC-006 W-3)은 켠 상태에서 없어진다 | 사실(조사 §1) · 뒷절은 끌어낸 것 |

### 2-2. ② 이해 호출

| # | 규칙 | 상태 |
|---|---|---|
| UC1 | 켠 상태의 **모든 턴**(첫 턴 포함)에 이해 호출을 **한 번** 띄운다. 턴 종류를 따로 묻는 요청 · 거둠 요청 · 입구 고르기 · 두 번째 걷기는 없다 | 결정(D-16) |
| UC2 | 호출 = `claude -p` · 모델 = `CHAT_PICK_MODEL`(기본 `sonnet`) · **thinking 끔**(D-4) · `--effort low` · `--max-turns 1` · `--output-format json` · **세션을 남기지 않는다**(`--no-session-persistence` — 턴마다 새 호출 · 맥락은 턴 메시지의 글로) · 격리 인자는 답 실행기와 같은 것(`--setting-sources ""` · `--tools ""` · `--disallowedTools <DISALLOWED_TOOLS>` · `--disable-slash-commands` · `--strict-mcp-config` · `--permission-mode bypassPermissions` — `$A/clinic_chat/llm/chat_cli.py:51-59` `chat_args` · 시안 호출 줄) · 턴 메시지는 stdin · cwd = 답 실행기의 고정 cwd | 결정(D-4 · 발주서 「같은 격리 인자」) · 인자는 사실(시안) |
| UC3 | **thinking 을 끄는 방법은 구현 첫 걸음(E8-0)에서 실측으로 정한다** — 조사 호출은 `--effort low` 인데도 소넷 39 / 255 호출에서 thinking 토큰을 썼다(검수 R-2 — 그 호출의 API 시간 중앙 3,078ms vs 없는 호출 1,645ms). 끝 조건 = 이해 호출 20 회의 `usage` 에서 thinking 토큰이 전부 0. CLI 로 못 끄면 코디에게 올린다(D-4 는 「CLI 그대로」 다 — 이 워커는 CLI 의 끄는 인자를 확인하지 못했다) | 결정(D-4) · 방법은 열림(C8-5) |
| UC4 | `--fallback-model` 을 싣지 않는다 — 소넷이 안 되면 §4-1 의 실패 길이다(하이쿠로 넘어가지 않는다 — 결정 「하이쿠 비교 안 함」 · 조사: 하이쿠는 줄임 50.0% · 턴 종류 66.7%) | 제안 |
| UC5 | **시스템 글** = `prompts/consult.json` 의 `pick.rules[]`(§7) + 빈 줄 + 목록 글(LD3). 턴 · 대화와 무관하게 같은 글이다(LD5) | 결정(발주서 ②) |
| UC6 | **턴 메시지** = 세 블록(머리 글자는 `pick.headers` — 시안의 `# 대화 지금까지` · `# 지금 객체` · `# 이번 말`). ⓐ 대화: 이 대화의 **성공 턴 전부**를 차례로 — 턴마다 손님 말 · `→ 고른 대상: 이름(table:code), … · <턴 종류>`(③ 검증 뒤 값 — 대상이 없으면 「없음」) · 그 턴에 앱이 물은 선택지(`ask.options` — `n) 이름(table:code)`). 그리고 **가까운 `CHAT_PICK_CONTEXT_TURNS` 턴**(기본 2)에는 **앞 답 요약** 과 **보여 준 리스트 이름**(UC7)을 더 싣는다 ⓑ 객체: 대상(축 항목 — 이름(table:code)) · 애매(`guess`) · 거둔 것 ⓒ 이번 말 = 손님 글 그대로 | 결정(D-8 · 발주서 ②) · 「가까운 n 턴」 · 꼴은 제안 |
| UC7 | **앞 답 요약** = 그 턴의 답 본문(꼬리 뗀 것 — 장부 `answer`)의 앞 `CHAT_PICK_ANSWER_CHARS` 자(기본 200) — **LLM 으로 줄이지 않는다**(호출을 더하지 않는다 · 결정론). **보여 준 리스트 이름** = 그 턴 장부 `list` 의 줄을 화면에 그린 순서대로 `n) 이름(table:code)` — 묶음 ① 관심 대상 · ② 계열 → 시술 · ③ 시너지 순 · 앞에서 `CHAT_PICK_LIST_MAX` 개(기본 30). 리스트가 그 턴에 안 바뀌었으면 「앞과 같음」 한 줄 | 결정(D-8) · 요약 식 · 한도는 제안(C8-3) |
| UC8 | **출력** = JSON 객체 하나(설명 · 코드 울타리 없음): `{"targets":[{"table":…,"code":…,"sure":true\|false}], "kind":"new"\|"follow"\|"talk", "sites":["SITE-…"], "withdraw":["table:code"], "kinds":["<정보 종류 코드>"], "out":true\|false}` — 필드 뜻은 아래 표 | 결정(D-9 · D-11 · 발주서 ②) · `out` 은 결정 행 「범위 밖」 의 자리(이름 제안) |
| UC9 | 시간 한도 = `CHAT_PICK_TIMEOUT_SEC`(기본 **10**) — 넘으면 프로세스를 거두고 §4-1 | 결정(D-10) |
| UC10 | 단계 표시는 0.3 그대로다 — 이해 호출이 도는 동안 `understand` · ⑤ 가 `search` · ⑥ 이 `list` · ⑧ 이 `answer`. `talk` 턴은 `understand` → `answer`(TT5 그대로) | 결정(CP5) |

출력 필드:

| 필드 | 뜻 | 닫힌 값 |
|---|---|---|
| `targets[]` | 이번 말이 말하거나 가리키는 대상 — **부위도 늘 여기 넣는다**(`table` = `site` · 코디 F-8). **순서 = 말에 나온 차례**(코디 F-9 — `focus` 가 이 순서를 읽는다 · OU9). `follow` 면 이어 묻는 **앞 대상** · `talk` 면 `[]` | `table` ∈ 다섯 표 · `code` ∈ 목록 |
| `targets[].sure` | 확실(`true`) / 애매(`false` — 여러 가지로 읽히거나 목록에서 가장 가까운 것으로 읽었다) | bool |
| `kind` | 턴 종류 — 뜻은 SPEC-006 TK1 그대로(`new` · `follow` · `talk`) | 셋 |
| `sites[]` | **이번 턴 부위 거르개로 쓸 부위** — `targets` 의 부위 가운데 이번 말에 나온 것 + 고민 이름 안의 부위(예: 「눈밑 꺼짐」 의 눈밑). 앞 턴의 부위를 끌고 오지 않는다. `sites` 에만 있고 `targets` 에 없는 부위는 앱이 `targets` 에 더한다(VF8) | `site` 코드 |
| `withdraw[]` | 손님이 빼 달라고 한 대상 | `"table:code"` |
| `kinds[]` | 이번 말이 알고 싶어 하는 **정보 종류** — 묻지 않았으면 `[]` | 14 코드(`$A/clinic_chat/walk/kinds.py:22-37` — `overview` · `mechanism` · `indication` · `outcome` · `lineup` · `adverse` · `recovery` · `contraindication` · `avoid` · `combo` · `package` · `same_day` · `order_interval` · `offer`) |
| `out` | 이번 말이 14 종류 어느 것으로도 못 답하는 것을 묻는다(순위 · 비교 · 문헌 … — 지금 `jev_front.gap` 의 뜻) | bool |

### 2-3. ③ 앱 검증

| # | 규칙 | 상태 |
|---|---|---|
| VF1 | 출력 글에서 첫 `{` 부터 마지막 `}` 까지를 JSON 으로 읽는다. 못 읽거나 객체가 아니면 §4-1(`error.kind` = `json`) | 결정(D-10 「JSON 깨짐」) · 읽는 식은 제안 |
| VF2 | `targets[]` 의 (`table`, `code`) 가 **목록에 없으면 버린다** — 지어낸 코드 · 다섯 표 밖 · 꼴이 틀린 항목. 버린 것은 장부 `consult.understand.dropped[]` 에 `{table, code, why}` 로 남기고 **센다**(`why` = `not_in_gold` · `bad_shape` · `dup`). 버리고 남은 것으로 턴은 계속 돈다 | 결정(`_RESUME` §2 11-18 「앱이 gold 에 없는 코드는 버림」 · 발주서 ③) |
| VF3 | 같은 (`table`, `code`) 는 한 번(처음 것 · `sure` 가 갈리면 `false`) | 제안 |
| VF4 | **같은 이름 접기**(D-7): 남은 대상 가운데 계열 · 시술 · 제품 표의 항목끼리 **이름의 `norm` 이 같으면**(목록의 이름 = `entity_name` 기준 — 예: `M1` · `PRC-001` · `PRD-001` · `norm` = 허브 R1 과 같은 식 — 공백 연속 제거 + 소문자 · 다른 정규화를 더하지 않는다 · SPEC-001 §5-1 R1 · `gold-build.py:126-127`) 가장 넓은 것 하나만 남긴다(계열 > 시술 > 제품). 접힌 것은 `consult.understand.merged[]`. 소넷이 규칙 4 로 이미 하나만 냈으면 할 일이 없다 — 앱은 뒤를 받칠 뿐이다 | 결정(D-7) |
| VF5 | 고민과 부위가 **같은 이름**인 것(목록에서 `팔자주름` `CON-009` ↔ `SITE-046` · `사각턱` `CON-161` ↔ `SITE-076` · `마리오네트라인` `CON-010` ↔ `SITE-120`)은 접지 않는다 — 고민은 `targets` 로 · 부위는 `sites` 로 받는다(0.2 코디 결정 「고민 / 부위 같은 이름이면 둘 다 객체에」 그대로 · OU3) | 사실(0.2 결정) · 이름 셋은 시안 목록에서 본 것 |
| VF6 | `kind` 가 셋 밖이면 `new`. `talk` 인데 `targets` 가 있으면 대상을 **버린다**(`dropped.why` = `talk`) — 맞장구에 앞 대상을 다시 든 꼴(조사: 「응 맞아」 「네」)이 검색을 일으키지 않게. `follow` 인데 `targets` 가 `[]` 이면 **앞 대상**(SPEC-006 TW6 — 객체에서 가장 최근에 든 `subjects[]` · 없으면 `focus` 고민)을 싣는다(`consult.follow_target`) | 제안 |
| VF7 | 첫 턴의 `follow` 는 `new` 로 읽는다(이을 앞 대상이 없다). 첫 턴의 `talk` 는 그대로 받는다(SPEC-006 TK2 「첫 턴은 묻지 않고 `new`」 를 이렇게 달리 받는다 — 인사뿐인 첫 말이 검색으로 가지 않는다) | 제안(C8-6) |
| VF8 | **부위의 두 칸**(코디 F-8): 부위는 늘 `targets[]`(`table` = `site`)에도 있다 — 그래서 「부위만」 = 그 턴 `targets` 가 전부 `site` 인 턴 · 「대상 0」 = `targets` 가 `[]` 인 턴(QM3)으로 갈린다. `sites[]` = 그 가운데 **이번 턴 부위 거르개**로 쓸 것이다. 앱 받침: ⓐ `sites[]` 는 `site` 표 코드만 남긴다(없는 코드 버림) ⓑ `sites[]` 에 있고 `targets` 에 없는 부위는 `targets` 끝에 **더한다**(`sure` = `true` · `consult.understand.added_from_sites[]`) ⓒ `targets` 의 부위 가운데 `sites[]` 에 없는 것은 거르개가 아니다(앞 턴 부위를 다시 든 꼴 — 객체에는 든다). 이번 턴 부위(거르개) = 검증 뒤 `sites[]` + OU7 이음 → 장부 `consult.site_filter`(§6-1) | 결정(코디 F-8) · 받침 ⓑ ⓒ 는 제안 |
| VF9 | `withdraw[]` = `"table:code"` 꼴 · **객체에 살아 있는 항목**(`said` · `confirmed` · `guess`)일 때만 받는다. `targets` 와 겹치면 거둠이 앞선다(그 대상을 뺀다 — 시안 규칙 8) | 제안 |
| VF10 | `kinds[]` = 14 코드만 남긴다(순서 = **`walk/kinds.py:38` `KIND_CODES` 순**(… `package` · `same_day` · `order_interval` …) — `consult/state.py:30` `KIND_CODES_14` 는 순서가 다르다(… `same_day` · `order_interval` · `package` …) — 이 칸은 걷기 함수(`plan_calls`)에 넘기므로 걷기의 목록을 쓴다 · 중복 한 번). `sure` · `out` 이 bool 이 아니면 `sure` = `false` · `out` = `false` | 제안 |
| VF11 | `CHAT_TALK_MAX`(기본 3 · SPEC-006 TT6)는 그대로다 — `talk` 가 잇달아 그 수면 다음 턴의 `talk` 는 `new` 로 읽는다. **0.2.1 — 구현은 VF11 을 VF6 앞에 둔다**(턴 종류를 먼저 정한다 — VF6 뒤에 두면 대상을 버린 뒤 `new` 가 되어 「입구 없음」 으로 떨어진다 · §10-1) | 결정(CP5) |
| VF12 | 검증 뒤 값(`consult.understand.accepted`)이 그 턴의 **유일한 입구**다. ④ ~ ⑨ 는 이 값만 읽는다 — 글에서 낱말을 따로 뽑지 않는다(SPEC-005 UP1 의 뜻 그대로 · 재료만 걷기 trace → 이해 출력) | 결정(UP1) |

### 2-4. ④ 객체 갱신

객체의 꼴 · 칸 · `state` · diff · `axis_items()`(축 = `said` · `confirmed`)는 SPEC-005 그대로다. 바뀌는 것은 **관찰을 어디서 얻나** 하나다 — `cst.observe(w, prev_ask)`(`state.py:84-108` · 걷기 trace)의 자리에 검증 뒤 값이 온다.

| # | 규칙 | 상태 |
|---|---|---|
| OU1 | 관찰 하나 = 검증 뒤 대상 하나. 넣는 칸은 `SLOT_OF`(`state.py:24-25`) 그대로 — 고민 → `concerns[]` · 부위 → `sites[]` · 계열 · 시술 · 제품 → `subjects[]` | 사실 |
| OU2 | **급**(D-9): `sure` = `true` → `said` · `false` → **`guess`**. `guess` 는 조회 축 · `focus` · 거르개가 아니고(RV1 그대로) 빈 칸 BK5(추정 확인)로 되묻는다(§2-7). `guess` → `confirmed` 의 길은 SPEC-006 FX1 그대로다(다시 `sure` 로 나옴 · 걸린 선택지 답 · BK5 답) | 결정(D-9) |
| OU3 | `how`: 앞 턴 `ask.options` 에 있는 대상 → `option`(+ `from_ask`) · `follow` 턴의 대상 → `carried` · 그 밖 → `text`. 부위 대상(VF8 — `targets` 의 `site` · `sites[]` 에서 더한 것 포함) → 객체 `sites[]` 칸에 `said` · `how` = `text` · 이번 턴 대상인 고민과 **이름이 같은 부위**면 `source.pair_concern` = 그 고민 코드(0.2 W-2 그대로) | 제안 |
| OU4 | `follow` 턴의 대상이 **이미 객체에 있으면 급을 바꾸지 않는다**(`KEEP` — `state.py:28` · `history[]` 에 턴만 더한다). 객체에 없으면(한 턴보다 앞의 대상을 다시 가리킨 꼴 — AR-9) `said` 로 넣는다 | 제안 |
| OU5 | `new` 턴이 앞 대상을 다시 들어도(D-12) 그대로 받는다 — 객체에 이미 있으면 SPEC-005 UP6(`said` → `confirmed`)이 돈다. **축 항목 · `focus` · 이번 턴 부위가 앞 턴과 같으면 객체 기준 조회를 새로 부르지 않는다**(QS4) | 결정(D-12) |
| OU6 | **말하지 않은 고민을 붙이지 않는다**(D-5). 앱에는 부위 · 대상에서 고민을 지어 넣는 길이 없다(파생은 `procedures[]` · `concern_sites[]` 뿐 — `plan.derive`). 소넷 쪽은 §7 규칙 3 이 막는다(조사에서 틀린 7 턴 가운데 3 턴이 「보톡스 + 이마」 → 이마주름을 붙인 것) | 결정(D-5) |
| OU7 | **부위 잇기**(D-6 · 코디 F-5 — 「고민만 **답**」 = **앞 턴 되물음에 대한 답**) — 앱이 결정론으로 한다. **넷이 다 맞을 때만** 잇는다: ⓐ 이번 턴 대상이 **고민뿐**(`targets` 가 전부 `concern` — 부위 · 계열 · 시술 · 제품 0) ⓑ 이번 턴 부위(VF8 `sites[]`)가 `[]` ⓒ **바로 앞 성공 턴이 「부위만」**(그 턴의 검증 뒤 `targets` 가 전부 `site` — VF8) ⓓ **그 앞 턴에 앱이 고민 선택지를 물었다**(그 턴 장부 `consult.ask.slot` = `concern` 이고 `about` 이 그 부위 — QY7 의 되물음 · `blanks.py:45`). 이으면 그 앞 턴의 부위(`sites[]` 거르개 · 없으면 그 턴 `targets` 의 부위)를 **이번 턴 부위로 잇는다**(`consult.site_filter.carried[]` · `from` = 그 턴 번호). 소넷은 `sites[]` 에 앞 턴 부위를 넣지 않는다(§7 규칙 7) — 잇는 것은 앱뿐이다. ⓓ 가 없는 「부위만 → 고민만」(앞 턴에 `focus` 가 있어 QY7 이 서지 않은 꼴)은 잇지 않는다 — 그 고민은 앞 턴 부위의 답이 아니라 새 말이다 | 결정(D-6 · 코디 F-5) |
| OU8 | **거둠** = `withdraw[]`(VF9) → `withdrawn`(RV2 · RV3 그대로). 거둠용 `resolve` 한 번 · Jev `retract` 요청(`state.py:261-`)은 없어진다 | 결정(D-16) |
| OU9 | **`focus`** = 이번 턴에 `said` 급으로 든 고민 가운데 **`targets` 순서로 마지막** 것 — `targets` 순서 = **말에 나온 차례**(§7 규칙 1 · 코디 F-9). 0.3 은 걷기 trace 의 글자 자리 `start` 로 골랐다(`state.py:200-205`) — 그 재료가 없어진 자리를 출력 순서가 받고, 그 순서의 뜻을 프롬프트가 정한다. 이번 턴에 고민이 없으면 그대로. `viewing`(SPEC-006 FD6 · W-2)의 순서 규칙은 그대로다 | 결정(코디 F-9) |
| OU10 | `talk` 턴: 객체는 `withdraw[]` 로만 바뀐다(SPEC-006 TT1 의 ① — ② 걸린 선택지 답은 `new` 로 온다: §7 규칙 6 · 9). 안 바뀌면 조회 0 · `list` · `sites` 안 보냄(TT2 그대로) | 제안 |
| OU11 | 바람(`wishes[]`)의 정보 종류 = 검증 뒤 `kinds[]` 가운데 `recovery` · `outcome`(`WISH_KINDS` — `state.py:29` 그대로) | 사실 |
| OU12 | 객체 항목 `source` 에서 **없어지는 칸**: `noul` · `decision` · `matched` · `covered_by`. **새 칸**: `sure`(bool). `how` · `turn` · `from_ask` · `pair_concern` 은 그대로 | 제안 |

### 2-5. ⑤ 조회

조회는 둘이다. 둘 다 허브만 부른다(LLM · Jev 0).

**(가) 객체 기준 조회** — SPEC-005 QY1 ~ QY7 · `plan.run`(`$A/clinic_chat/consult/plan.py:193`) 그대로. 고치는 것은 아래 넷이다.

| # | 규칙 | 상태 |
|---|---|---|
| QS1 | **부위 거르개 = 이번 턴 부위만**(AR-4). QY1 · QY5 의 `site` 값 = 이번 턴 부위(장부 `consult.site_filter.sites` — VF8 의 `sites[]` + OU7 이음 · QS3 짝 고민 규칙까지 적용한 것)의 **이름**이다 — 객체 `sites[]` 에 쌓인 앞 턴 부위는 거르개가 아니다(`state.filter_sites` · `plan.qy1_calls` 가 읽는 재료를 객체 축 → 이번 턴 부위로). 부위가 여럿이면 부위마다 조회 하나(지금 꼴) · `[]` 면 거르개 없이 하나 | 결정(발주서 ⑤ 「조회 부위 거르개는 이번 턴만」 — 출처를 바로잡음 · 검수 F-15) |
| QS2 | 허브 `site` 입력은 부위 **이름** 글자다(조사 DA-3) — 앱은 코드를 목록의 `entity_name` 으로 바꿔 넘긴다(별칭 · 코드를 넘기지 않는다). 거름 / 우선 표시는 허브가 정한다(SPEC-001 SP1 — `site_applied`) | 사실(DA-3) |
| QS3 | 같은 이름의 부위(`pair_concern`)는 0.2 W-2 그대로 — 짝 고민이 `focus` 일 때만 거르개다. 이번 턴 부위에 그 부위가 들어 있어도 같다 | 결정(0.2 W-2) |
| QS4 | **리스트 ②(`focus` 고민의 시술)를 다시 조회하는 때** = `focus` 가 바뀐 턴 · 또는 이번 턴 부위가 `[]` 이 아닌 턴. `focus` 가 그대로이고 이번 턴 부위가 `[]` 이면 **앞 리스트를 그대로 둔다**(거르개 없는 조회로 덮어쓰지 않는다 · D-12 「객체 안 바뀌면 재조회 없음」). 대화 메모(`Conv.memo`)에 있는 조회는 지금처럼 허브를 다시 부르지 않는다 | 결정(D-12) · 「부위 없는 턴은 앞 리스트 유지」 는 제안 |
| QS5 | QY2(대상의 `scope`) · QY3(대상만 있고 고민 없음 → `facets(indication)` 선택지) · 시너지(SPEC-005 §7 — `pair` 보완)는 그대로다. 재료가 되는 축 항목만 OU1 ~ OU4 로 선다 | 사실 |
| QS6 | **QY7 — 부위만 → 고민 선택지**(AR-11 · DA-1 · D-13): 선택지 = ⓐ 그 부위에 **`concern_site` 로 묶인 고민**(먼저) ∪ ⓑ 지금의 `facets(site, indication)` 행의 고민(`plan.py:220-223`) — 같은 고민은 한 번. ⓐ 의 재료 = 고민 → 부위 묶임의 **거꾸로 색인**: `gold_hash` 마다 한 번(짓는 때 = **그 `gold_hash` 로 QY7 이 처음 서는 턴** — 서버 시작 때 미리 짓지 않는다 · 그 턴의 지연에 든다 · 장부 `consult.site_index{built, concerns, ms}` 로 잰다 — O8-1), 목록의 고민 260 마다 `concern_candidates(concern_code, limit=1)` 머리의 `sites[]` 가운데 `match` = `직접` 인 항목을 모아 `site_code → [concern_code]` 로 짓는다(허브 계약 변경 0 — `sites[]` 는 첫 쪽 머리에 늘 실린다 · SPEC-001 CS1). 조사: 고민이 묶인 부위 52 가운데 15 부위가 ⓑ 만으로는 0 행이다(예: 턱 `SITE-072` → `CON-163` · `168` · `170` · `171` · `172`) | 결정(D-13 「DA-1 은 조회 규칙」) · 색인을 얻는 길은 제안(C8-1) |

**(나) 답 재료 조회** — 0.3 까지 답 재료(「자료」 줄)는 걷기 ② 가 댔다. 객체 기준 조회의 닫힌 목록(`plan.ALLOWED` — `concern_candidates` · `scope` · `facets(indication)` · `pair`)에는 개요 · 원리 · 효과 · 부작용 · 회복 · 금기 · 상품 … 이 없다(§3). 그래서 재료 조회는 남는다.

| # | 규칙 | 상태 |
|---|---|---|
| QM1 | 재료 조회가 도는 턴 = `new` · `follow` 이고 검증 뒤 대상이 1 이상인 턴. 대상(입구) = 검증 뒤 `targets`(`sure` 무관 — 애매한 대상도 그 턴의 답 재료는 읽는다 · 지금 `uncertain_kept` 가 대상인 것과 같다) + 이번 턴 부위(부위는 지금처럼 거르개 입구 — BR1) | 제안 |
| QM2 | 읽을 정보 종류 = §3-1 의 표(KS1 ~ KS8)로 정한 `kinds` · `required` · `offered`. 조회 계획 = `plan_calls(entries, kinds)`(걷기와 같은 함수 · 같은 `Call`) → `read_calls`(쪽 넘김 끝까지) → `_labels` · `same_day_marks` → `build` · `roster` · `check`(관문) → `_end_check` → `es.decide`(종료 상태). **폭 원칙 · 관문 · 종료 상태 · 재료 줄 번호 · 근거 꼬리는 0.3 과 같은 코드 · 같은 값이다** | 사실(코드) · 「같은 함수」 는 결정(CP2) |
| QM3 | 대상이 0 인 `new` 턴(검증 뒤 `targets` 가 `[]` — 부위도 `targets` 에 들므로(VF8) 「부위만」 턴은 여기 오지 않는다 · §4 의 실패가 아닌데 소넷이 대상을 못 고른 것) = 종료 상태 「입구 없음」 — 0.3 의 말 그대로(SPEC-006 §5-2). `out` = `true` 이고 대상 0 · `kinds` 0 이면 「범위 밖」(지금 `front.py:306-313` 의 자리 — 점수 자리에 bool) | 제안 |
| QM4 | 깊이 읽기 · 값 고르기는 §3-2 · §3-3 | — |
| QM5 | 걷기와 객체 조회가 같은 조회를 두 번 부르지 않는 것은 0.2 그대로다 — `plan.Reader` 가 이번 턴 재료 조회의 `Read` 를 `key()` 로 먼저 본다(`plan.py:46`) | 사실 |

### 2-6. ⑥ 화면

| # | 규칙 | 상태 |
|---|---|---|
| DT1 | **점 = 말한 고민의 부위만**(AR-5): 객체 `concerns[]` 가운데 `said` · `confirmed` 인 고민마다 그 고민의 `concern_candidates.sites[]` 에서 **`match` = `직접`** 인 부위만 점이다. `match` = `하위`(하위 고민의 부위)는 점이 아니다 — **SPEC-006 FD1 「둘 다 점」 을 이렇게 바꾼다**. 조사: 「주름이 고민이에요」 → 말하지 않은 부위 10 곳 · 「처짐」 → 18 곳에 점(9 턴) | 결정(발주서 ⑥ 「점은 말한 고민만」 — 출처를 바로잡음 · 검수 F-15) |
| DT2 | 쌓임 · 보내는 때 · 누르기 · `viewing` · 부위 없는 고민의 칩(SPEC-006 FD2 ~ FD11)은 그대로다. 하위 고민의 점이 없어지므로 「하위 고민 부위 점을 눌러 그 하위 고민으로 `viewing`」(SPEC-006 W-1 · `sites.viewable_subs`)은 **닿는 점이 없어진다** — 코드는 남기되 부르는 자리가 비는지는 WORK 에서 본다 | 사실 · 뒷절은 끌어낸 것 |
| DT3 | 하위 고민의 부위는 **되묻기 선택지**(BK4 — `plan.sub_sites`)로는 그대로 쓴다. 점이 아닐 뿐이다 | 사실 |
| DT4 | `list` 조각의 꼴(고민 → 계열 → 시술 · 내려온 시술 · 안 그리는 것)은 SPEC-006 §6 그대로다 | 결정(CP5) |
| DT5 | `list` · `sites` 는 ⑤ 가 끝나면 답 LLM 을 기다리지 않고 보낸다(TF3 그대로). 0.3 과 달리 그 앞에 이해 호출 하나가 있다 — `timing.first_list_ms` 가 그만큼 는다(장부로 잰다) | 사실 |

### 2-7. ⑦ 빈 칸 · 되묻기

| # | 규칙 | 상태 |
|---|---|---|
| BQ1 | 빈 칸 세기 · 고르기(SPEC-005 §6 NQ1 ~ NQ9 · BK1 ~ BK5) · 끝맺음 `close`(SPEC-006 §4)는 그대로다. 재료가 되는 「이번 턴에 새로 든 항목」 · 「새 `guess`」 는 ④ 의 diff 에서 온다(지금과 같다 — `turn.py:444-452`) | 결정(CP5) |
| BQ2 | **애매한 대상**(`sure` = `false`) → `guess` → BK5(추정 확인) 빈 칸 → `ask` 로 한 번 확인한다(D-9). 문구는 0.3 의 BK5 자리 그대로다(새 문구 0) | 결정(D-9) |
| BQ3 | `kinds_read`(NQ6 — 안전 종류를 물은 턴은 `ask` null)의 재료 = §3-1 의 `kinds` | 사실 |
| BQ4 | **NQ5 를 한 곳에서 좁힌다**(AR-12): 이번 턴이 `new` 이고 QY7 이 선 턴(대상이 부위뿐 · `focus` 없음)이면 NQ5(「앞 턴 되물음에 답하지 않았으면 이번 턴은 안 묻는다」 — `blanks.py:99-100`)를 걸지 않는다 — 고민을 모르면 리스트가 설 수 없다. 그 밖의 턴은 NQ5 그대로다. **SPEC-005 검수 W-2 의 「새 항목 무관」 을 이 한 곳에서 달리 받는다** | 제안(C8-2) |
| BQ5 | §4-1 의 실패 턴 · 「입구 없음」 · 「범위 밖」 턴은 NQ7 그대로 `ask` 가 없다 — 되묻는 말은 종료 상태의 말이 한다 | 사실(`blanks.py:95-96`) |

### 2-8. ⑧ 답 · ⑨ 장부

| # | 규칙 | 상태 |
|---|---|---|
| AN1 | 답 = 0.3 그대로 — CLI 소넷 · `--resume` · `system_v3` · 「앱 판정」 · 재료 · 근거 꼬리 · `close` 줄. 「앱 판정」 의 `turn_kind` 는 검증 뒤 `kind` 다 | 결정(CP5) |
| AN2 | 답 LLM 에 이해 호출의 출력을 통째로 주지 않는다 — 「앱 판정」 · 「상담 상태」 의 0.3 칸으로만 간다(「LLM 에는 필요한 것만」) | 제안 |
| AN3 | 장부는 §6 | — |

## 3. 값 고르기 · 깊이 판단의 자리(D-11)

### 3-0. 걷기가 상담에서 하던 일(코드로 센 것)

`walk()`(`$A/clinic_chat/columns/col_b.py:161-227`)는 켠 상태 턴에서 아래를 했다. **답 LLM 에 가는 「자료」 줄은 전부 이 걷기의 `verified` 행에서 나온다**(`mat.renumber(w, …)` — `turn.py:143`).

| 단계 | 하는 일 | Jev | 답 재료에 보태던 것 | 0.4 |
|---|---|---|---|---|
| ① 맨 앞 판단 `front()` | resolve 맞춤 꼴 → 후보 · Jev 한 요청(후보 Noul + 정보 종류 14 Noul + 범위 밖) · 후보 0 이면 입구 고르기 | 요청 1 + 입구 고르기 30 안팎 | 대상(입구) · 읽을 정보 종류 · 범위 | **이해 호출이 대신**(§2-2 · §3-1) |
| ② 폭 읽기 `plan_calls` → `read_calls` | 대상 × 정보 종류 → 허브 조회 계획 · 쪽 넘김 끝까지 | 0 | **재료 행 전부**(개요 · 원리 · 적응 · 효과 · 하위 목록 · 부작용 · 회복 · 금기 · 회피 · 조합 · 패키지 · 같은 날 · 순서·간격 · 상품) | **그대로**(QM2) |
| ②-b 값 고르기 `value_pick.run`(`walk/value_pick.py:78`) | 물은 종류가 값 종류(부작용 · 금기 · 효과 · 적응)인데 그 값 표의 입구가 없을 때 — 읽은 행의 서로 다른 값마다 Noul | 요청 1+ | ⓐ yes 값의 행에 표지 `value_pick`(「질문이 가리킨 값」 — **행을 빼지 않는다**) ⓑ 미룬 부작용 상세를 yes 사건의 위험 id 로만 읽음(못 고르면 **미룬 조회 전부**) ⓒ 값 이름이 품은 거르개 조각을 걷고 다시 읽음(VP3) | §3-3 |
| ③ 깊이 `walk_depth`(`walk/depth.py:50`) | 읽은 행에서 깊이 후보(상대 끝 · 상품의 시술 · 값 쪽 시작의 대상)를 뽑아 후보마다 Noul → `deepen` / `listed_only` / `uncertain` · 이번 턴 대상인 후보는 Noul 과 무관하게 `gate_forced` | 걸음마다 요청 1+ | 깊이 본 후보의 조회 행(상대 끝 · 상품의 시술 = 개요 profile · 값 쪽 = 상세 · 회복 · 속성 시작 = 그 대상의 읽기로 한 종류 전부) — **목록 · 재료에서 빼는 길은 없다**(`depth.py:3-4`) | §3-2 |
| ③-4 `answer_ready` | 걸음 끝마다 Noul 하나 | 걸음마다 요청 1 | **0** — 값을 적기만 한다. 걸음을 잇는 조건은 남은 후보 · required 뿐이다(`depth.py:133-152` · 머리말 「그 값은 종료 제안일 뿐이다」) | **없앤다** |
| ④ 관문 · 종료 | `build` · `roster` · `check` · `_end_check` · `es.decide` | 0 | 종료 상태 · `empty` 의 근거 | **그대로**(QM2) |

- **객체 기준 조회는 걷기 ② 를 덮지 않는다.** `plan.ALLOWED` 는 `concern_candidates` · `scope` · `facets(indication)` · `pair` 넷뿐이고(`plan.py:27` — QY6 「안전 종류 0」) 그 응답은 리스트 · 선택지 · 시너지 · 점에 쓰인다. 「울쎄라 효과가 얼마나 가요」 의 답 재료(`g_outcome` 행)는 걷기 ② 에서만 나온다. 그래서 **②④ 는 남기고 Jev 가 끼던 네 자리(① · ②-b · ③ · ③-4)만 처분한다.**
- 이 표로는 「값 고르기 · 깊이가 몇 턴에 돌았나」 를 못 센다 — 조사의 턴 기록(`now-turns.jsonl`)에 그 칸이 없다(8 검사만). 결정 행도 「정보 종류 · 값 · 깊이는 이번 표로 안 쟀다」 고 적었다 → 재는 몫은 §8-2.

### 3-1. 정보 종류 — 이해 호출의 `kinds[]`

지금은 Jev 가 14 종류마다 점수를 내고 `_decide_kinds`(`walk/front.py:85-136`)가 규칙으로 읽을 종류를 정한다. 소넷은 점수를 내지 않는다 — **고른 것 = yes · 안 고른 것 = no** 로 읽고, 점수의 「사이 값」 에 기대던 규칙만 없앤다.

| # | 지금 규칙 | 0.4 | 상태 |
|---|---|---|---|
| KS1 | KD1 — 점수 yes 인 종류를 읽는다(`by` = `yes`) | `kinds[]` 에 든 종류 = `yes` | 결정(D-11) |
| KS2 | KD2 — yes 가 없어도 가장 높은 종류 하나(`top`) | **없어짐** — `kinds[]` 가 `[]` 면 KS6(기본 묶음)으로 간다 | 제안 |
| KS3 | KD5 — 입구가 이름 댄 정보(대상의 표가 정하는 종류 · `entry`) | 그대로(결정론 — 대상의 표만 본다) | 사실 |
| KS4 | KD10 — 사이 값 가운데 `jev_kind_read_at` 이상이면 읽는다 | **없어짐**(사이 값이 없다) | 제안 |
| KS5 | KD9 — 개요가 yes · 1위면 그 대상의 한 벌 | 그대로(`overview` 가 `kinds[]` 에 있을 때) | 사실 |
| KS6 | KD6 — 읽기로 한 종류가 대상의 표에 하나도 없으면 그 표의 기본 묶음 | 그대로(`kinds[]` 가 `[]` 인 턴 = 「시술 이름만 말한 턴」 이 여기로 온다) | 사실 |
| KS7 | KD3 · RG1 — 범위 = 읽기로 한 (대상의 표, 종류) 의 범위 합집합 + 그 범위의 기본 묶음 / KD11 — 그 범위에 강하게 선 종류가 있고 점수가 no 이하인 기본 묶음 종류는 안 읽고 `offered` | 범위 식은 그대로. KD11 = **그 범위에 `yes` · `entry` 종류가 있으면 `kinds[]` 에 없는 기본 묶음 종류는 읽지 않고 `offered`** 로(안 고름 = no) | 제안 |
| KS8 | `required` = `by` 가 `yes` · `top` · `entry` 인 종류 / `offered` = 사이 값이거나 KD11 인 종류 | `required` = `yes` · `entry` / `offered` = KS7 로 안 읽은 종류뿐 | 제안 |

- KD7(안전 종류는 묻지 않으면 기본 묶음에 없다) · KD4(대상의 표에 없는 종류는 건너뜀)는 결정론이라 그대로다.
- 범위 밖(RG5)의 자리 = 출력 `out`(QM3).
- 이 표는 걷기의 `_decide_kinds` 를 **고치지 않고** 상담 쪽에 같은 뜻의 함수를 따로 둔다는 계약이다(CP2 · CP3). 두 함수가 갈리는 곳은 KS2 · KS4 · KS7 · KS8 넷뿐이어야 한다(시험 S8-T9).

### 3-2. 깊이 판단 — 판정: **소넷 호출을 더하지 않는다 · 「이번 턴 대상인 후보만 깊이 읽기」 로 이해 호출이 대신한다**(U8-1 (가) — 코디 11-18 확정)

| # | 규칙 | 상태 |
|---|---|---|
| DP8-1 | 깊이 후보를 뽑는 식(`depth_candidates` — `walk/calls.py:462`)과 깊이 조회(`depth_calls` — `:499`)는 그대로 부른다 | 결정(CP2) |
| DP8-2 | **깊이 결정**(U8-1 (가)) = 후보가 **이번 턴 대상**(검증 뒤 `targets` 의 노드)이면 `gate_forced`(지금 `depth.py:96-97` 「G7 명시 대상」 그대로) → 깊이 읽기 · **그 밖의 후보는 전부 `listed_only`**. 후보마다 묻는 요청 · 사이 값(`uncertain`) · C2(required 미충족이면 점수 높은 순으로 하나씩 깊이)는 없어진다 | 결정(U8-1 (가)) |
| DP8-3 | `listed_only` 인 후보는 **목록에 그대로 있다** — 폭에서 읽은 행(관계 행 · 상품 행)은 재료에서 빠지지 않는다. 안 읽는 것은 그 후보 **자신의 깊이 조회 행**(상대 끝 · 상품의 시술의 개요 profile)뿐이다 | 사실(`depth.py:3-4`) |
| DP8-4 | 걸음은 한 번이다 — `gate_forced` 후보를 읽은 뒤 새 후보가 나와도 DP8-2 로만 가른다(이번 턴 대상이 아니면 `listed_only`). 걸음 상한(C3)에 닿을 길이 없어진다 | 끌어낸 것 |
| DP8-5 | required 가 폭 읽기 뒤에도 미충족이면 지금의 「후보 소진」 그대로다 → `empty` 로 말한다(SPEC-006 §5) | 사실(`depth.py:153-154`) |
| DP8-6 | 관문 `check(decisions=…, required=…)` 에는 DP8-2 의 결정 표와 `rq1` 값을 그대로 넘긴다(칸 꼴은 지금과 같다 — `decision` · `reason` · `range` · `closed_as` · `noul` 은 `null`) | 제안 |

근거 — 깊이 판단이 상담 답 재료에 보태던 것과 0.4 에서의 자리:

| 깊이 꼴(`depth_kind`) | 서는 때 | 깊이 조회가 보태던 행 | 0.4 에서 |
|---|---|---|---|
| `other_end` · `other_end_one_side`(조합 · 순서·간격 · 회피) | 관계 행의 상대 끝 | 상대 끝의 **개요 profile** | 손님이 상대를 말했으면 그것은 이번 턴 대상이다 → `gate_forced` 로 읽힌다. 말하지 않은 상대의 개요는 「묻지 않은 것」 이다 — 관계 행(무엇과 · 어떤 관계)은 재료에 남는다 |
| `offer_items`(상품) | 상품 행의 시술 | 그 시술의 개요 profile | 같음 |
| `adverse_value_side` · `condition_side`(값 쪽 시작) | 대상이 없고 사건 · 조건 입구만 있을 때 | 그 값을 가진 대상의 상세 · 회복 | **서지 않는다** — 사건 · 조건은 목록(다섯 표)에 없어 입구가 될 수 없다(LD8) |
| 속성 시작(`ATTR_DEPTH`) | 대상이 부위뿐일 때 | 그 부위 행에 나온 대상마다 읽기로 한 종류 전부 | 「부위만」 턴은 QY7 로 **고민을 되묻는 턴**이다(0.2 W-1 (가) — 리스트 · 답을 곧바로 넓히지 않는다). 부위 행의 대상은 `listed_only` 로 목록에만 남는다 |
| (깊이 칸 「없음」 — 시술 · 부위·고민 · 동시 가능) | — | 0(지금도 ③-1 ~ ③-3 을 건너뛴다 — `depth.py:9`) | 달라지는 것 0 |

- 즉 Jev 깊이 판단이 하던 「말하지 않은 후보 가운데 무엇을 더 읽을까」 는 0.4 에서 **「더 읽지 않는다」** 가 된다. 폭 원칙(「질문이 가리키는 대상 × 필요한 정보 안에서는 빠짐없이」)은 ② 가 지킨다 — 깊이는 그 밖의 것이다.
- 놓칠 수 있는 꼴(재는 몫 — §8-2 E8-6): 「보톡스랑 같이 받으면 좋은 게 뭐예요, 그건 어떤 시술이에요?」 처럼 **상대를 이름 없이** 더 물은 말 — 다음 턴에 `follow` · 이름으로 물으면 그때 대상이 된다.

### 3-3. 값 고르기 — 판정: **없앤다(표지 0 · 미룬 상세는 전부 읽는다) · 소넷 호출을 더하지 않는다**(U8-1 (가) — 코디 11-18 확정)

| # | 규칙 | 상태 |
|---|---|---|
| VP8-1 | 값 고르기 요청은 없다. 표지 `value_pick`(「질문이 가리킨 값」)은 0.4 재료에 없다 — `system_v3.material` 절의 그 표지 설명 줄은 남겨도 닿는 줄이 없다(문구 정리는 사용자 몫) | 결정(U8-1 (가)) |
| VP8-2 | 미루던 부작용 상세(`adverse_detail` — W-7 · BR5)는 **미루지 않고 폭 읽기에서 전부 읽는다**(지금 「아무 조회도 id 를 못 내면 미룬 조회 전부」 의 가지 — `value_pick.py:150-153` 와 같은 결과) | 제안 |
| VP8-3 | VP3(값 이름이 품은 거르개 조각을 걷고 다시 읽기)는 없다 — 그 구멍(「눈 주변 멍」 의 「눈」 이 부위 거르개로 걸리는 꼴)은 이해 호출이 `sites[]` 를 뜻으로 내는 것으로 받는다(§7 규칙 5 · 7) | 제안 |
| VP8-4 | 적응(`indication`)의 값 = 고민이다 — 고민은 목록에 있어 이해 호출이 대상으로 뽑는다(값 입구가 있으면 지금도 값 고르기는 돌지 않는다 — VP1 · `value_pick.py:28-33`) | 사실 |

근거 — 값 고르기가 상담 답 재료에 보태던 것과 0.4 에서의 자리:

| 보태던 것 | 근거(코드) | 0.4 에서 | 잃는 것 |
|---|---|---|---|
| yes 값의 행에 표지(행은 그대로) | `value_pick.py:104-109` | 표지 없음 — 답 소넷이 손님 말과 행을 보고 그 값을 답한다(재료 행은 같다) | 「어느 행이 물은 값인가」 의 앱 쪽 표시. 답의 정확도로 드러나는지는 E8-6 |
| 부작용 상세를 yes 사건의 것만 읽음 | `:131-149` | 전부 읽음 | **재료가 커진다** — 큰 계열 · 제품에서 메시지가 `answer_input_max_tokens`(150,000 · `config.py:56`)를 넘으면 지금처럼 「실행 중단」(FT5 · `turn.py:152-161`)이다. 몇 턴이 넘는지는 E8-6 이 센다 |
| 거르개 걷고 다시 읽기(VP3) | `:111-130` | 없음(VP8-3) | 부위 이름이 값 이름 안에 든 말에서 소넷이 부위를 `sites[]` 로 내면 거르개가 걸린다 — E8-6 표본에 그 꼴을 넣는다 |

- **값을 소넷으로 고르는 다른 길 둘**(이 판에서 고르지 않은 것 — U8-1): (나) 폭 읽기 뒤 두 번째 소넷 호출(값 종류를 물었고 값 입구가 없는 턴에만 — 그 턴이 한 호출만큼 느려진다) (다) 목록에 사건 · 조건 · 효과 표를 더한다(그러면 값이 대상으로 뽑혀 지금의 「값 입구」 가 된다 — 목록 820 · 토큰 · D-3 의 수가 바뀌고 표의 채점 표가 다섯에서 는다).

### 3-4. 부를 함수의 서명(코디 F-10 — WORK 전에 맞춘 것)

상담 쪽은 **걷기의 그릇(`Walk` · `FrontResult` · `DepthResult`)을 스스로 지어** 걷기 함수에 넘긴다. 셋 다 모든 칸에 기본값이 있는 dataclass 라 빈 그릇에서 지을 수 있다(`columns/col_b.py:47` `Walk` · `walk/front.py:50` `FrontResult` · `walk/depth.py:41` `DepthResult`). 상담이 채우는 `FrontResult` 칸 = `entries`(검증 뒤 대상 → `walk/calls.py:55` `Entry(table, code, name, by="target")`) · `kinds` · `required` · `offered` · `by`(§3-1 의 상담 함수) · `ranges` · `attr_start` · `coverage` · `groups` · `links` · `applicable_kinds`. `end` 는 QM3 의 「입구 없음」 · 「범위 밖」 만. `trace_front` · `trace_entry` · `jev_*` · `carried` 는 비워 둔다(장부에 안 실린다 — §6-1).
줄 번호 = 앱 `be1c622`.

| 함수 | 자리 | 서명 | 넘길 그릇 · 읽는 `Walk` 칸 | 상담에서 맞나 |
|---|---|---|---|---|
| `plan_calls` | `walk/calls.py:304` | `(entries: list[Entry], kinds, *, purpose="read", groups=None) -> list[Call]` | `FrontResult.entries` · `kinds` · `groups` | **맞음** — 그대로 |
| `read_calls` | `walk/breadth.py:61` | `async (hub, calls, verified, ledger, reads, *, depth="breadth", read_as_by_node=None, follow=True) -> list[Read]` | `Walk.verified` · `ledger` · `reads`(제자리에 쌓음) | **맞음** — `read_as_by_node` 는 `None`(TG2 · TG3 표지가 없다) |
| `scope_links` · `group_targets` | `walk/groups.py:23` · `:44` | `async (hub, nodes)` → `(links, visited)` · `(targets: list[Entry], links)` → `(groups, bys)` | 대상 둘 이상일 때 `FrontResult.links` · `groups`(PR1 — `front.py:423-428` 과 같은 꼴) | **맞음** — 공개 함수 |
| `_coverage` | `walk/front.py:168` | `async (hub, nodes) -> (cov, build)` | `FrontResult.coverage`(KS6 · `_end_check` 의 `coverage_zero` · `rq1`) | **밑줄** → `walk/front.py` 에 공개 감쌈 `coverage_of_nodes(hub, nodes)`(본문 = `_coverage` 를 부를 뿐 · F-10 예외) |
| `_ranges_for` | `walk/front.py:193` | `(pairs) -> list[str]` | `FrontResult.ranges`(KS7 범위 합집합) | **밑줄** → 같은 파일에 공개 감쌈 `ranges_for(pairs)`(F-10 예외) |
| `nonzero_rows` · `range_of` · `is_attr_start` | `walk/front.py:179` · `walk/kinds.py:111` · `walk/ranges.py:23` | 공개 | §3-1 상담 함수(KS1 ~ KS8)의 재료 · `offered` 의 행 수 | **맞음** — `_kind_rows`(`front.py:189` · 밑줄)를 쓰면 공개 감쌈을 더한다(F-10 예외) |
| `_labels` | `columns/col_b.py:74` | `async (d: Deps, w: Walk) -> None` | `w.verified` · `reads` · `ledger` · `labels`(채움) | **밑줄 · `columns/`** — `columns/` 는 diff 0 이라 감쌈을 그 자리에 못 더한다 → **그대로 import 해 부른다**(서명은 맞다 — 지은 `Walk` 를 넘긴다) · 감쌈이 필요하면 C8-9 |
| `same_day_marks` | `columns/col_b.py:121` | `(w: Walk) -> None` | `w.front.kinds` · `entries` · `links` · `w.verified` | **맞음**(공개) — `w.front` 에 상담이 지은 `FrontResult` |
| `rq1` | `walk/depth.py:35` | `(f: FrontResult, reads) -> dict` | `f.required` · `entries` · `coverage` · `applicable` | **맞음** — `DepthResult.required` 에 넣는다(DP8-5 · DP8-6) |
| `depth_candidates` · `depth_calls` | `walk/calls.py:462` · `:499` | `(range_code, rows, entries)` · `(range_code, cand, read_kinds)` | 폭 읽기 행 · `FrontResult.entries` · `kinds` | **맞음** — DP8-1 · DP8-2 |
| `build` | `walk/material.py:160` | `(verified, *, decisions=None, speak_names=None, inherited_kinds=None) -> Material` | `decisions` = DP8 결정 표 · `speak_names` = `w.labels` · `inherited_kinds` = `rq1` 의 `met_by` = `inherited`(`col_b.py:202` 와 같은 식) | **맞음** |
| `roster` | `walk/material.py:268` | `(reads, verified, entry_nodes) -> dict` | `{e.node for e in entries}` | **맞음** |
| `check` | `walk/gate.py:38` | `(*, reads, verified, entries, decisions, ranges, kinds, material, planned, required) -> dict` | 위 값 그대로 · `planned` = 재료 조회 계획 | **맞음** |
| `_end_check` | `columns/col_b.py:230` | `async (d: Deps, w: Walk) -> dict` | `w.front.entries` · `ranges` · `coverage` · `groups` · `w.reads` · `verified` · `ledger` | **밑줄 · `columns/`** — `_labels` 와 같이 그대로 부른다 |
| `es.decide` | `walk/end_state.py:79` | `(*, aborted, entry_end, unsettled, required_ok, gate_ok) -> (str, str \| None)` | `col_b.py:222-224` 와 같은 값 | **맞음** |
| `judgement` | `columns/col_b.py:254` | `(w: Walk) -> dict` | `w.front` · `w.depth`(`DepthResult` — `decisions` · `required` · `exhausted`) · `w.end_state` | **맞음** — `w.depth` 에 상담이 지은 `DepthResult`(`steps` · `jev_requests` · `answer_ready` 는 기본값) |
| `mat.renumber` | `consult/material.py:162` | `(w, sent, summaries_seen, next_n, v3=False)` | `w.material` · `w.reads` · `w.front` · `w.end_state`(`consult/` 자리 — 고칠 수 있다) | **맞음** — 지은 `Walk` 를 넘긴다 |

- `Deps`(`columns/base.py:21`)는 지금 상담이 쓰는 것을 그대로 넘긴다(`_labels` · `_end_check` 는 `d.hub` 만 읽는다 — `d.jev` 를 부르지 않는다).
- 공개 감쌈의 이름은 제안이다(WORK 가 정한다). 조건: 감싼 함수의 본문 · 기존 시험을 바꾸지 않는다 · 감쌈은 인자를 그대로 넘기는 한 줄(S8-T18).

## 4. 실패 길 · 설정값

### 4-1. 실패 길(D-10)

| # | 무엇 | 규칙 | 상태 |
|---|---|---|---|
| FL1 | 실패의 꼴 | ⓐ 시간 초과(`CHAT_PICK_TIMEOUT_SEC`) ⓑ CLI 오류(종료 코드 · 인증 · 프로세스) ⓒ JSON 깨짐(VF1) ⓓ 목록 적재 실패(LD7) → `consult.understand.error{kind: "timeout" \| "cli" \| "json" \| "list", detail}` | 결정(D-10) · ⓓ 는 제안 |
| FL2 | 그 턴 | **대상 없이 되묻는다**: 객체 갱신 0(diff `[]`) · 조회 0 · `list` · `sites` 안 보냄 · 종료 상태 = 「입구 없음」 · 답 LLM 은 0.3 의 「입구 없음」 말(SPEC-006 §5-2 — 손님 말로 한 번 묻는다)로 답한다. **새 문구 0** | 결정(D-10) · 「입구 없음」 의 자리를 쓰는 것은 제안 |
| FL3 | 안 하는 것 | 옛 길로 돌아가지 않는다 — `resolve` 맞춤 꼴 · `walk()` · Jev 를 부르지 않는다. 다른 모델로 넘어가지 않는다(UC4). **다시 부르지 않는다**(재시도 0 — 10초를 기다린 턴에 10초를 더 얹지 않는다) | 결정(D-10) · 재시도 0 은 제안 |
| FL4 | 대화 | 턴을 죽이지 않는다 — 대화는 이어지고 다음 턴이 다시 이해 호출을 띄운다. 실패 턴은 UC6 의 「성공 턴」 이 아니다(다음 턴의 대화 블록에 손님 말만 `(이해 실패)` 표지와 함께 싣는다 — 손님이 「아까 말했잖아요」 로 받을 수 있게) | 제안 |
| FL5 | 답 LLM 이 죽은 턴 | 0.3 그대로(`turn_error` · `broken`) — 이 스펙이 건드리지 않는다 | 사실 |
| FL6 | 검증으로 다 버려진 턴 | 출력은 읽혔는데 대상이 전부 버려졌다(VF2) = 실패가 아니다 — QM3(「입구 없음」)으로 가고 `dropped[]` 에 남는다 | 제안 |

### 4-2. 설정값(이름 · 기본값 전부 제안)

| env | 기본 | 뜻 |
|---|---|---|
| `CHAT_PICK_MODEL` | `sonnet` | 이해 호출 모델(UC2) |
| `CHAT_PICK_EFFORT` | `low` | 이해 호출 `--effort`(시안 값) |
| `CHAT_PICK_THINKING` | `off` | thinking — 끄는 방법은 E8-0 이 정한다(UC3) |
| `CHAT_PICK_TIMEOUT_SEC` | `10` | 시간 한도(UC9 · D-10) |
| `CHAT_PICK_ALIASES` | `on` | 목록에 별칭을 넣는다(LD4 · D-3) |
| `CHAT_PICK_LIST_CACHE` | `on` | 목록 글을 `gold_hash` 마다 한 번 짓는다(LD5) — `off` 는 턴마다 다시(시험용) |
| `CHAT_PICK_CONTEXT_TURNS` | `2` | 앞 답 요약 · 리스트 이름을 싣는 가까운 턴 수(UC6) |
| `CHAT_PICK_ANSWER_CHARS` | `200` | 앞 답 요약 글자 수(UC7) |
| `CHAT_PICK_LIST_MAX` | `30` | 턴마다 싣는 리스트 이름 수(UC7) |

켠 상태에서 **안 읽게 되는 설정**(값은 남는다 — 시험 앱 B 열이 읽는다 · 0.4 서버는 끈 상태 대화를 새로 열지 않는다 — CP1): `CHAT_CARRY_TURNS` · `CHAT_RETRACT` · `CHAT_TURN_KIND` · `JEV_NOUL_YES_AT` · `JEV_NOUL_NO_AT` · `JEV_KIND_READ_AT` · `JEV_BATCH_SIZE` · `WALK_MAX_STEPS`. 그대로 읽는 것: `CHAT_STATE`(**기본 `on` 으로 바뀐다** · `off` 는 새 대화에 쓰이지 않는다 — CP1 · CP7) · `CHAT_ASK_MAX` · `CHAT_SYNERGY` · `CHAT_TALK_MAX` · `CHAT_ALT_MAX` · `CHAT_VOICE_CHECK` · `CHAT_DEBUG_PANEL` · `CHAT_DRAWER_MAX` · `ANSWER_INPUT_MAX_TOKENS`.

## 5. 앱 규칙 — 고칠 곳(AR-1 ~ AR-12)

자리 = 조사 §5 의 것(검수 §6 이 표본 11 을 확인) · 「표에서」 = 조사가 센 턴 수.

| # | 무엇(지금) | 자리 | 표에서 | 처분 | 0.4 의 꼴 |
|---|---|---|---|---|---|
| AR-1 | 후보 관문 = resolve 글자 맞춤 · 입구 고르기는 후보 0 일 때만 | `walk/front.py:225-238` · `:298-326` · `consult/turn.py:380-383`(TW5) | 후보 층 39 · 입구 고르기 36 턴 중앙 7.4초 | **없어짐** | 켠 가지가 `front()` 를 부르지 않는다(CP2). 후보 = 이해 호출이 목록 820 에서 뜻으로 뽑는다 · 입구 고르기 · 두 번째 걷기 없음(UC1) |
| AR-2 | 같은 조각 겹침을 점수가 아니라 범위 규칙으로 고름(TG3 · `lost`) | `walk/front.py:335-356` · `:362-363` | 「사각턱인데 ?」 | **없어짐** | 겹침 묶음이 없다 — 고민은 `targets` · 같은 이름 부위는 `sites`(VF5) · 계열 · 시술 · 제품 같은 이름만 D-7 로 접는다(VF4) |
| AR-3 | 점수가 낮아도 이름이 글에 들면 대상(TG2 · TG3) | `walk/front.py:373-376` | 4 턴(「재발」 → 발 · 「온다 리프팅」 → 다리 …) | **없어짐** | 글자 일치로 대상이 되는 길이 없다 — §7 규칙 5 「글자만 같고 뜻이 다른 것은 고르지 않는다」 |
| AR-4 | 조회 부위 거르개 = 객체에 쌓인 축 부위 전부 | `consult/state.py:65-68` `filter_sites` · `consult/plan.py:87-95` `qy1_calls` | 20 턴 | **고침** | 이번 턴 부위만(QS1) · 앞 턴 고민 되물음에 고민만 답한 턴은 그 「부위만」 턴의 부위를 잇는다(OU7) · 부위 없는 턴은 앞 리스트 유지(QS4) |
| AR-5 | 점 = 고민의 하위 고민 부위까지 전부 | `consult/plan.py:228-266` `derive` · `consult/sites.py:88-92` · `consult/turn.py:621` | 9 턴 | **고침** | `match` = `직접` 인 부위만 점(DT1) · 하위 부위는 되묻기 선택지로만(DT3) |
| AR-6 | 입구 고르기로 확정한 대상이 객체에 안 듦 | `consult/state.py:84-108` `observe` | 3 턴 | **없어짐** | 입구 고르기가 없다. 관찰의 재료가 검증 뒤 값 하나다(VF12 · OU1) — 「대상인데 객체에 안 든다」 가 설 자리가 없다(시험 S8-T5) |
| AR-7 | 사이 값 대상은 `guess` → 조회 축 · `focus` 아님 | `consult/state.py:71-81` · `:55-57` | 3 턴(이름을 말했는데 `guess`) | **고침** | `guess` 는 소넷이 `sure` = `false` 라고 한 대상뿐이다(OU2). 축 규칙(RV1)은 그대로 — 애매하면 축이 아니고 BK5 로 되묻는다(BQ2). 단 그 턴의 답 재료는 읽는다(QM1) |
| AR-8 | 턴 종류 판정이 `new` 먼저 | `consult/turn_kind.py:60-66` | 2 턴 + Jev 판정 11 턴 | **없어짐** | 점수 셋 · 판정 순서가 없다 — `kind` 는 이해 호출의 값 하나(VF6 으로만 고친다) |
| AR-9 | 든 후보 = 바로 앞 한 턴의 대상만 | `consult/carry.py:15-31` · `chat_carry_turns` 1 · `consult/turn_kind.py:69-81` | 「둘 다」 「아까 그거」 「첫 번째 걸로」 | **없어짐** | 든 후보가 없다. 대화 블록이 성공 턴 전부의 대상 · 선택지 + 가까운 턴의 답 요약 · 리스트 이름을 싣는다(UC6 · UC7) — 한 턴보다 앞의 대상도 `follow` 의 대상이 된다(OU4) |
| AR-10 | `focus` = 글에서 뒤에 나온 고민 | `consult/state.py:200-205` | 2 턴(「여드름 흉터」 → 넓은 흉터) | **고침** | `targets` 순서(= 말에 나온 차례)로 마지막인 `said` 고민(OU9). 넓은 고민과 좁은 고민이 함께 대상이 되는 꼴은 §7 규칙 3 이 좁은 것 하나로 낸다 |
| AR-11 | 부위만 → 선택지 = `facets(site, indication)` 하나 | `consult/plan.py:220-223`(QY7) | 1 턴(「턱이요」 — DA-1) | **고침** | `concern_site` 로 묶인 고민 ∪ 지금 것(QS6) |
| AR-12 | 앞 턴 되물음에 답하지 않았으면 이번 턴은 안 물음(NQ5) | `consult/blanks.py:95-101` | 6 턴(앞 턴이 후보 층에서 틀린 뒤) | **고침(한 곳)** | QY7 이 선 `new` 턴에는 NQ5 를 걸지 않는다(BQ4). 그 밖은 그대로 — 6 턴의 큰 까닭은 앞 턴의 틀린 되물음이라 AR-1 이 없어지면 함께 준다(재실행으로 확인 — E8-4) |

처분 수: **없어짐 6**(AR-1 · 2 · 3 · 6 · 8 · 9) · **고침 6**(AR-4 · 5 · 7 · 10 · 11 · 12) · **그대로 0**.

SPEC-004 · 005 · 006 을 **달리 받는 곳**:

| 문서 · 규칙 | 0.3 | 0.4 |
|---|---|---|
| SPEC-006 TK2 ~ TK7(가르는 주체 = Jev Noul 셋) · TW1 ~ TW8(걷기와의 순서 · 줄임 후보) | Jev · 걷기 두 번 | 이해 호출의 `kind`(UC8 · VF6 · VF7) — TW 전부 없어짐. TW6(앞 대상)만 VF6 이 쓴다 |
| SPEC-006 TT1 ② (`talk` 턴의 걸린 선택지) | `target_option` Noul | 선택지 답은 `new` 로 온다(OU10) |
| SPEC-006 FD1(하위 고민 부위도 점) · W-1(하위 점 누르기) | 둘 다 점 | 직접만 점(DT1 · DT2) |
| SPEC-006 W-3(다섯 표 밖이 앞 대상이면 든 후보로) | CR1 | 없어짐(LD8) |
| SPEC-005 UP1 ~ UP3(재료 = 걷기 trace · 확실함 = 판정 값) | `target` · `uncertain_kept` · `named` · `carried` | 검증 뒤 값 · `sure`(OU1 ~ OU4) |
| SPEC-005 RV2 · RV3 의 거둠 요청 | resolve + Jev | `withdraw[]`(OU8) |
| SPEC-005 QY1 · QY5 의 거르개 · QY7 | 객체 축 부위 · facets 하나 | 이번 턴 부위(QS1) · `concern_site` 더함(QS6) |
| SPEC-005 NQ5(검수 W-2 「새 항목 무관」) | 늘 | QY7 턴만 뺌(BQ4) |
| SPEC-004 CR1 ~ CR6(든 후보) · ST3(선택 인자) | `carry` · `instr` · `entry_pick` · `abbr_yes_only` | 켠 가지에서 안 씀(CP2 · CP3) |
| SPEC-004 TF2(턴마다 걷기) | `walk()` | 이해 호출 + 걷기의 결정론 함수(QM2) |

## 6. 장부 · 패널 · SSE

### 6-1. 장부

| 칸 | 0.3 | 0.4 |
|---|---|---|
| 시작 줄 `consult_rev` | `3` | **`4`**. `consult_rev` 가 3 인 켠 대화는 0.4 서버에서 끝난 대화다(`conv_end` = `rev_changed` — SPEC-006 FX4 와 같은 꼴 · C8-4) |
| **`consult.understand`**(새) | — | `{model, thinking, pick_version, list_sha, aliases, input_bytes{system, message}, output_raw, parsed{targets, kind, sites, withdraw, kinds, out}, accepted{…같은 꼴}, dropped[{table, code, why}], merged[{kept, folded[]}], added_from_sites[], ms, api_ms, usage{input_tokens, cache_read_input_tokens, output_tokens, thinking_tokens}, error{kind, detail} \| null}` — `parsed` = 읽은 그대로 · `accepted` = 검증 뒤(VF12) |
| **`consult.site_filter`**(새 — 검수 F-4) | — | `{sites[], carried[], from, pair_kept[], pair_dropped[]}` — 이 턴 조회에 **실제로 건 부위 거르개**: `sites` = 걸린 부위 코드(VF8 `sites[]` + OU7 이음 · QS3 짝 고민 규칙 적용 뒤) · `carried` = OU7 로 이은 부위 · `from` = 이은 턴 번호(`null`) · `pair_kept` / `pair_dropped` = QS3 로 남긴 · 뺀 같은 이름 부위. 칸 이름은 WORK 가 바꿀 수 있다 — 채점(`score.py` 검사 3)이 이 칸을 읽는다(E8-pre) |
| `consult.turn_kind` | `{kind, nouls{new, talk, follow}, rule, requests, ms, error, walks[]}` | `{kind, from: "understand" \| "first_follow" \| "talk_max" \| "bad_value"}` — **`nouls` · `rule` · `requests` · `walks[]` 없어짐** |
| `consult.follow_target` | TW4 로 실은 앞 대상 | VF6 으로 실은 앞 대상(뜻 같음) |
| `consult.retract` | `{items[{noul …}], requests, resolve_ms, ms, error}` | **없어짐** → `consult.understand.accepted.withdraw` |
| `targets[]`(턴 줄) | `{table, code, name, by: "rule" \| "noul" \| "carried" …}` | `{table, code, name, sure, how}` — **`by` · `noul` 없어짐** |
| `kinds[]` · `trace.front.kinds[]` | 종류마다 `noul` · `decision` · `by`(`yes` · `top` · `kd10` · `kd9` · `kd11` · `entry` · `default`) | 종류마다 `by`(`yes` · `entry` · `kd9` · `default`) · `offered[]` — **`noul` · `top` · `kd10` 없어짐** |
| `trace.front.targets[]`(후보마다 `noul` · `decision` — `target` · `uncertain_kept` · `named` · `overlap` · `dropped` · `carried`) | 있음 | **없어짐** |
| `trace.entry{resolve_candidates[], picked[], overlaps[], unused[], value_pick}` · `trace.entry_pick{requests …}` | 있음 | **없어짐**(resolve 후보 · 입구 고르기 · 값 고르기) |
| `trace.depth{steps[{candidates[{noul, decision}], answer_ready}], jev_requests}` | 있음 | `trace.depth{decisions{id: gate_forced \| listed_only}, read[]}` — **`noul` · `answer_ready` · `jev_requests` 없어짐** |
| 객체 항목 `source` | `noul` · `decision` · `matched` · `covered_by` | **없어짐** + `sure`(OU12) |
| `timing.parts` | `jev_ms` · `hub_ms` · `llm_ms` · `walk_ms` | `understand_ms` · `hub_ms` · `llm_ms` · `material_ms` — **`jev_ms` · `walk_ms` 없어짐** |
| `consult.queries[]` | `rule` · `skipped: "walk"` | 그대로(`skipped` 값 이름은 `material` — 재료 조회가 이미 읽음) + QS6 의 색인 적재는 `consult.site_index{built, concerns, ms}`(지은 턴에만 — 짓는 데 든 허브 호출 수 `calls` 도 · O8-1) |
| `sites.dots[]` | 직접 + 하위 | 직접만(`data-match` 값은 `직접` 하나) |
| 그 밖(`consult.after` · `diff` · `blanks` · `ask` · `close` · `empty` · `voice` · `viewing` · `list` · `llm_user_message` · `answer_raw`) | — | 그대로 |

- 쓴 줄은 고치지 않는다(SPEC-004 LG) · 옛 줄(0.3)은 옛 꼴 그대로 읽힌다(드로어 · 되읽기는 `consult_rev` 로 가른다).
- `output_raw` 는 소넷이 낸 글 그대로다(코드 · JSON 뿐 — 비밀값 없음). 턴 메시지 전문은 싣지 않고 바이트 수만 남긴다(대화 블록은 장부의 앞 줄로 다시 지을 수 있다).

### 6-2. 객체 패널(SPEC-006 SV8 · SV9)

| 무엇 | 0.4 |
|---|---|
| 턴 묶음에 싣는 판정 | `consult.turn_kind{kind, from}`(점수 없음) · `consult.close` · `consult.ask` 그대로 + **`consult.understand` 의 `accepted` · `dropped` · `merged` · `ms` · `error` + `consult.site_filter`** — 「무엇으로 읽었나 · 무엇을 버렸나 · 얼마나 걸렸나」 를 화면에서 본다 |
| 문구 | 짓지 않는다 — 칸 이름 = 장부 키 그대로(SV10). 패널의 새 빈 자리(`data-slot`) 0(화면 전체의 새 빈 자리는 CP7 하나 — U8-3) |
| 없어지는 표시 | `nouls` · Jev 요청 수 |

### 6-3. SSE

| 이벤트 | 0.4 |
|---|---|
| `step` · `list` · `sites` · `delta` · `state` · `done` · `turn_error` · `close` | **이름 · 자리 · 조각 꼴 그대로**(새 이벤트 0 · 없어지는 이벤트 0) |
| `step` 의 단계 | 넷 그대로(`understand` · `search` · `list` · `answer` — 문구는 `prompts/consult.json` `steps` 의 지금 값). 걷기가 내던 속 단계(`①` · `②` · `③` · `④`)는 이해 · 재료 조회로 바뀌지만 화면 넷에 묶이는 자리는 같다 |
| 달라지는 것 | 때뿐이다 — `list` · `sites` 가 이해 호출 뒤에 온다(DT5). §4-1 의 실패 턴은 `list` · `sites` 없이 `delta` → `done` 이다(`turn_error` 가 아니다 — 답은 나간다) |

## 7. 프롬프트 — `prompts/consult.json` 의 새 절 `pick`(**초안 · 사용자 확인 대상**)

- 시안(`pick-prompt.md`)의 규칙 9 줄을 바탕으로 **D-5 · D-6 · D-7 · D-8 · D-9 · D-11** 과 조사가 본 틀린 꼴(맞장구를 `follow` 로 · 「첫 번째」 를 대화의 첫 대상으로 · 말하지 않은 고민을 붙임)을 넣어 고쳤다.
- **예문은 입력 전수 표의 턴과 겹치지 않게 새로 지었다**(검수 R-4 — 시안의 예문 8 개는 표의 턴과 글자가 같았다). 0.1.0 워커가 조사 판 255 턴과 · 0.2.0 워커가 지금 표 356 턴(공백 무시 부분 문자열)과 대조했다 — 따옴표 예문의 겹침 0(규칙 11 의 종류 풀이 낱말 「원리」 · 「부작용」 · 단계 이름 「이해」 만 턴 글에 든다 — 예문이 아니다). 0.2.0 에서 「팔뚝에 살」 을 바꿨다(C45-1 과 같은 대상 · 같은 꼴 — 검수 F-16). E8-2 가 기계로 다시 본다. 예문의 코드는 시안 목록에 있는 것이다.
- 꼴 = `pick{version, rules[], headers{history, object, utterance}, marks{failed, same_list, none}}` — `rules[]` 를 줄바꿈으로 이은 글이 시스템 글의 앞머리다(UC5). `version` = `0.4.0-draft`. 이 절을 바꾸면 `prompts/consult.json` 의 sha 가 바뀐다 → 새 대화부터 쓰인다(0.3 과 같다). 적재기 계약은 아래 「적재기 계약」 표(검수 F-7).
- 사람에게 보이는 글이 아니다(화면 문구 0). `headers` · `marks` 는 턴 메시지 안의 블록 머리 · 표지 글자다.

`rules[]`(초안):

```text
너는 피부 · 미용 상담 앱의 「이해」 단계다. 손님의 이번 말을 읽고 아래 목록에서 대상을 골라 JSON 객체 하나로만 답한다. 설명 · 코드 울타리 · 다른 글을 쓰지 않는다.

출력 꼴: {"targets":[{"table":"concern","code":"CON-000","sure":true}],"kind":"new","sites":["SITE-000"],"withdraw":[],"kinds":[],"out":false}

규칙
1. targets = 이번 말이 말하거나 가리키는 대상. 부위도 targets 에 넣는다(table = site). 말에 나온 차례대로 적는다. 목록에 있는 (table, code) 만 쓴다. 목록에 없으면 넣지 않는다 — 코드를 지어내지 않는다.
2. 글자가 아니라 뜻으로 읽는다. 조사가 끼거나(등에 여드름) 어순이 바뀌거나(배가 나왔어요) 줄이거나 오타가 있거나 자기 말로 바꿔 말해도(손에 땀이 많아요) 같은 대상이다. 괄호 안의 (= …) 는 같은 대상의 다른 이름이다.
3. 넓은 고민과 부위를 **둘 다 말했고** 그 부위의 더 좁은 고민이 목록에 있으면 좁은 고민 하나를 고른다. 손님이 고민을 말하지 않았으면 고민을 넣지 않는다 — 시술과 부위만 말했으면(「볼에 맞을 거예요」) 고민을 짐작해 붙이지 않고 그 부위만 targets · sites 에 넣는다.
4. 같은 이름이 계열 · 시술 · 제품 표에 함께 있으면 가장 넓은 것 하나만 고른다(계열 > 시술 > 제품). 손님이 제품 · 시술임을 분명히 말했으면 그것을 고른다.
5. 글자만 같고 뜻이 다른 것은 고르지 않는다(「점점 심해져요」 의 점은 고민 CON-247 이 아니다). 낱말의 한 부분이 우연히 부위 · 제품 이름과 같은 것도 고르지 않는다.
6. kind — new: 대상(고민 · 부위 · 시술 · 계열 · 제품)을 새로 말했거나, 자기 상태를 새 말로 설명했거나, 상담사의 물음에 대상으로 답했다. follow: 대상을 새로 말하지 않고 앞에서 나온 대상에 대해 더 묻거나 그것을 고른다(「통증은 어때요?」 「그럼 그쪽으로 정할게요」) — targets 에 그 대상을 넣는다. talk: 찾아볼 것이 없는 인사 · 맞장구 · 짧은 대답 · 불만 · 혼잣말(「좋네요」 「설명이 어려워요」) — targets 는 []. 「그렇죠」 「아하」 처럼 받기만 하는 말은 앞 대상을 다시 넣지 않고 talk 다.
7. sites = targets 의 부위 가운데 이번 말에 나온 것의 코드 + 고민 이름 안의 부위(이번 턴에 거를 부위). 앞 턴의 부위를 끌고 오지 않는다. 없으면 [].
8. withdraw = 손님이 빼 달라고 한 대상의 "table:code"(「스킨부스터는 빼 주세요」 「그건 됐고」). 그 대상은 targets 에 넣지 않는다. 없으면 [].
9. 앞 턴에 상담사가 선택지를 물었고 이번 말이 그 답이면(「1번이요」 · 선택지의 이름) 그 선택지를 targets 에 넣고 kind 는 new 다. 이번 말이 앞에서 **보여 준 리스트** 의 순서를 가리키면(「위에서 둘째 거」) 대화의 첫 대상이 아니라 그 리스트의 그 줄을 targets 에 넣는다.
10. sure — 그 대상이라고 분명하면 true. 여러 가지로 읽히거나, 목록에 그 이름이 없어 가장 가까운 것으로 읽었으면 false. 가까운 것조차 없으면 넣지 않는다.
11. kinds = 이번 말이 알고 싶어 하는 정보의 종류 코드(여럿 가능). 대상만 말하고 무엇을 알고 싶은지 말하지 않았으면 []. 코드: overview(무엇인지) · mechanism(원리) · indication(무엇에 쓰나 · 그 고민에 무엇을 하나) · outcome(효과 · 언제부터 · 얼마나 가나) · lineup(그 아래 제품 · 시술 · 종류) · adverse(부작용) · recovery(회복 · 붓기 · 일상 복귀) · contraindication(시술을 피해야 하는 사람) · avoid(함께 하면 안 되는 것) · combo(같이 받으면 좋은 것) · package(묶음 프로그램) · same_day(같은 날 가능 여부) · order_interval(순서 · 간격 · 다시 받는 간격) · offer(상품 · 가격).
12. out = 이번 말이 위 종류 어느 것으로도 답할 수 없는 것을 묻는다(무엇이 제일 좋은지 순위 · 인기 · 논문 · 번역 · 예약 · 위치 등). 그 밖은 false.
```

| 줄 | 시안에서 달라진 것 | 근거 |
|---|---|---|
| 머리 · 출력 꼴 | 「후보 뽑기」 → 「이해」 · 출력에 `sure` · `kinds` · `out` | D-9 · D-11 · 결정 행 「범위 밖」 |
| 1 | 「부위도 targets 에」 · 「말에 나온 차례대로」(0.2.0) | 코디 F-8 · F-9 |
| 2 | 별칭 괄호의 뜻 한 줄 · 예문 셋 교체(0.2.0 — 「팔뚝에 살」 → 「등에 여드름」: 표 C45-1 과 같은 대상 · 같은 꼴이었다) | D-3 · 검수 R-4 · F-16 |
| 3 | 「둘 다 말했고」 · 「말하지 않았으면 붙이지 않는다」 + 예문 | D-5 — 조사에서 틀린 7 턴 가운데 3 턴 |
| 4 | 「계열 · 시술 · 제품 표」 로 좁힘(고민 ↔ 부위 같은 이름은 규칙 7 이 받는다) · 뒷문장 | D-7 · VF5 |
| 5 | 예문 교체 · 「낱말의 한 부분」 | AR-3(「재발」 → 발) · 검수 R-4 |
| 6 | 자기 상태 묘사 = `new`(0.3 W-4) · 고르는 말 = `follow` · 받기만 하는 말 = `talk` | 조사 「소넷이 틀린 턴」(맞장구를 `follow` 로 3 턴 · 고르는 말을 `new` 로 2 턴) · 표의 정답 키(고르는 말 = `follow` 또는 `talk`) |
| 7 | 0.2.0 — 「targets 의 부위 가운데」 · 「이번 턴에 거를 부위」 | D-6 은 앱이 한다(OU7) · 코디 F-8 |
| 8 | 예문 교체 | 검수 R-4 |
| 9 | 뒷문장(리스트 순서) | D-8 · 검수 R-8(「첫 번째 걸로 할게요」) |
| 10 ~ 12 | 새로 | D-9 · D-11 · 「범위 밖」(지금 `jev_front.gap` 의 뜻) |

- 규칙 11 의 종류 설명은 `walk/kinds.py:22-37` 의 영어 이름을 한국어로 옮긴 초안이다(뜻을 넓히지 않았다). 규칙 12 의 예(「예약 · 위치」)는 검수 §4 「표 밖 꼴」 에서 온 것이고 지금 `gap` 지시문에는 없다 — 넣을지는 사용자(문구 확인 때).
적재기 계약(`consult/prompt.py` — 검수 F-7):

| 무엇 | 0.3 | 0.4 |
|---|---|---|
| 최상위 필수 키(`KEYS` — `prompt.py:27`) | `version` · `system` · `jev_front` · `turn_headers` · `tail_marker` | **그대로**(`jev_front` 절을 지우면 `parse` 가 `keys` 로 떨어진다 — 남긴다) |
| `pick` 절 | — | **새 필수 절**(켠 대화 문턱에만): `version`(빈 글 아님) · `rules[]`(1 줄 이상 · 빈 줄 아님) · `headers{history, object, utterance}` · `marks{failed, same_list, none}` — 하나라도 없거나 비면 `pick` 은 없는 것(`ConsultPrompt.pick` = `None`) |
| `state_ready`(켠 대화를 시작할 수 있나 — `prompt.py:66-72`) | `system_text_v3` · `jev_state.retract` · `jev_front.target_option` · `turn_headers.consult` · `turn_kind` 셋 · `kind_labels` 14 · `voice_check` · V3 머리 둘 | **`jev_state.retract` · `jev_front.target_option` · `turn_kind` 셋을 빼고 `pick` 을 더한다**: `system_text_v3` · `pick` · `turn_headers.consult` · `kind_labels` 14 · `voice_check` · V3 머리 둘 |
| 남기는 절 | — | `jev_front` · `jev_state`(`retract` · `turn_kind`) 는 **지우지 않는다** — 켠 대화가 읽지 않을 뿐이다(옛 끈 대화 · 옛 rev 3 대화는 읽기만이라 그 절로 턴을 돌리지 않는다 · CP7 · C8-4) |
| `draft`(`prompt.py:62-64`) | 최상위 `version` 이 `-draft` 로 끝나나 | **뜻 그대로 — 최상위 `version` 만 본다.** `pick.version` 의 `-draft` 는 `draft` 에 닿지 않는다(장부 `consult.understand.pick_version` 으로만 남는다). 초안 표시를 화면에 띄우려면 최상위 `version` 을 `-draft` 로 둔다(지금과 같은 길) |
| sha | `prompts/consult.json` 파일 sha | 그대로 — `pick` 을 바꾸면 sha 가 바뀌어 새 대화부터 |

- 턴 메시지 머리(`headers`)는 시안 글자 그대로(`# 대화 지금까지` · `# 지금 객체` · `# 이번 말`) — 답 요약 줄 · 리스트 줄의 머리 글자는 WORK 에서 정한다(사람에게 안 보인다).

## 8. 시험

### 8-1. 끝 조건 — 입력 전수 표 재실행(D-14)

표 = `$W/research-input-space/conversations.jsonl` · 스크립트 = `$W/research-input-space/scripts/`(README 「돌리는 법」). **분모 · 애매 수는 고정 수로 적지 않는다** — 실행 때 `build.py` · `score.py` 가 낸 수가 그 판의 수다(0.2.0 을 쓸 때: 78 대화 · 356 턴 · 애매 18 · 정보 종류 키 156 · 재료 키 22 — 참고일 뿐 끝 조건이 아니다).

| # | 무엇 | 끝 조건 |
|---|---|---|
| E8-0 | thinking 끔 실측(UC3) | 이해 호출 20 회의 thinking 토큰 전부 0 · 끄는 방법을 `CHAT_PICK_THINKING` 뜻으로 적는다. **0.2.1 결과 — 못 미침**: CLI 로는 완전히 못 끈다(후보 다섯 모두 20 호출 가운데 4 ~ 5 회 thinking) → ⓐ 꼴로 두고 진행 · SDK 몫(§10-1 · §10-3) |
| **E8-pre** | **채점기를 0.4 장부에 맞춘다**(검수 F-4 — E8-3 ~ E8-6 의 앞 단계) | `score.py` `now_turn` · `slim.py` 가 0.4 장부 칸을 읽는다: 대상 = `targets[]{table, code}`(`by` 를 읽지 않는다) · 거둠 = `consult.understand.accepted.withdraw` + `consult.after` 의 `withdrawn` · 부위 거르개(검사 3) = **`consult.site_filter.sites`**(옛 `filter_sites` 식 85 ~ 98 행을 바꾼다) · 턴 종류 = `consult.turn_kind.kind` · 정보 종류 = `consult.understand.accepted.kinds` · 재료 · 깊이 = `material.new_lines[].gid` · `material.seen_lines` · `trace.depth.decisions`(`slim.py` 에 더함 — E8-6b). 옛 층 가르기(`trace.front.targets` · `trace.entry` · `trace.entry_pick` · `consult.retract`)는 0.4 줄에서 비어 있어도 채점이 떨어지지 않는다(층은 `checks` 만 본다 — README). 끝 조건 = 0.3 장부(`runs/now-rows.jsonl`)로 돌린 수가 고치기 전과 같다(옛 칸 길을 남김) · 0.4 장부 표본 3 대화에서 검사 8 개가 `None` 아닌 값을 낸다 |
| E8-1 | 목록 글 대조 | 앱이 지은 목록 글의 항목 수 = 그 `gold_hash` 의 다섯 표 개념 수(조사 판 820 — 고민 260 · 부위 89 · 계열 18 · 시술 138 · 제품 315 · 데이터 판이 바뀌면 다시 센다) · 시안 목록과 줄 단위로 견줘 다른 줄을 보고한다(데이터 판이 바뀌어 다른 줄은 까닭과 함께) |
| E8-2 | 예문 겹침 | `pick.rules[]` 의 따옴표 안 예문이 **표 전체 턴**의 글과 부분 문자열(공백 무시)로 겹치는 것 0 |
| E8-3 | **입구 3 검사**(대상 · 턴 종류 · 부위 — `score.py` 의 `target_score` · `site_score` 그대로) | 실행 때 `score.py` 가 낸 **채점 턴**의 **세 검사를 모두 통과한 턴 95% 이상**(D-14 · `summary.json` `pass3_pct`) |
| E8-4 | **앱 전체 8 검사**(대상 · 턴 종류 · 부위 거르개 · 객체 반영 · 점 · 부위만 → 선택지 · 거르개가 실제로 걸림 · 리스트에 시술 — README 「8 검사」) | 실행 때 `score.py` 가 낸 채점 턴의 **해당 검사를 모두 통과한 턴 90% 이상**(D-14 · `pass8_pct`) |
| E8-5 | 정답 키 사람 검수 | 의도 꼴 · 말 꼴(표의 `tags` — 실행 때 `build.py` 가 찍는 꼴 수)마다 표본을 사람이 보고 고친 키로 E8-3 · E8-4 를 잰다(D-14 · 검수 R-3). 채점 밖 = 표의 `ambiguous` 턴 전부(D-15 — 지금 18) · 표본 검수 때 같이 본다. **이름으로 박은 표본**: 아래 「D-6 규칙과 표의 키」 의 네 턴(C05-2 · C15-3 · C28-3 · C38-4 — 검수 F-5) |

- 재는 방법은 조사와 같다 — 앱 코드를 부르기만 하고(`run_now.py` → `run_turn` · `CHAT_STATE=on`) 답 LLM 자리에는 빈 답을 내는 가짜를 둔다. 이해 호출은 실물 소넷이다(가짜 아님).
- **앞 답을 가리키는 턴**(`key.ref.to` = `answer` — 표에서 직접 센 수 **5**: C56-5 · C57-2 · C58-3 · C65-4 · C69-2)은 **표 실행에서 답 LLM 을 실제로 부른다** — 그 턴이 든 **대화 전부**(C56 · C57 · C58 · C65 · C69 — 25 턴)를 가짜 답 없이 돌린다(코디 기본값 · `_RESUME` 179 행 · 검수 F-3). 그 다섯 대화의 앞 답 요약(UC7)이 실물 답에서 나온다. 「7」 과 갈린 까닭: 7 은 의도 꼴 `답참조` 태그 수다 — 그 가운데 C57-5 는 애매(`ambiguous` — `ref` 없음 · 채점 밖)이고 C67-3(「덜 아픈 쪽으로요」)은 대상이 리스트 둘 가운데 어느 것이든이라 `ref` 를 달지 않았다(그 대화 C67 은 리스트 가리킴이라 빈 답 실행으로 잰다). 그 밖의 대화는 빈 답 실행이다 — 리스트 가리킴(`ref.to` = `list`)은 README 의 규칙대로(앱 리스트 앞머리 = `shown.list` 일 때만 채점).
- E8-7 은 **실물 화면 확인**만이다 — 앞 답 턴의 채점은 위 실행이 한다.
- 데이터 층(DA-2 · DA-5)은 데이터 보강 전이면 그대로 실패로 센다(D-13 — 90% 에 들어 있는 몫이다).

**D-6 규칙과 표의 키**(OU7 — 코디 F-5 로 좁힌 규칙 · 앞 턴이 부위만이고 이번 턴이 고민만인 턴 넷):

| 턴 | 앞 턴 | 이번 턴 | 앞 턴에 고민 되물음(QY7)? | OU7 | 키(`site_filter` · `site_required`) | 키와 맞나 |
|---|---|---|---|---|---|---|
| C05-2 | 「눈 밑이 고민이에요」(첫 턴 · 부위만 `SITE-024`) | 「다크서클이요」(`CON-066`) | **있음**(첫 턴 · `focus` 없음 → QY7) | 이음 `SITE-024` | `[SITE-024]` · 아님 | **맞음** |
| C15-3 | 「코 쪽이 특히요」(부위만 `SITE-035`) | 「블랙헤드도 많고」(`CON-103`) | **없음** — 턴 1 「모공이 넓어요」 로 `focus` 가 있어 QY7 이 서지 않는다(`blanks.py:45`) | 안 이음 | `[]` · 아님 | **맞음**(0.1.0 규칙으로는 이어 검사 3 에서 떨어졌다 — F-5) |
| C28-3 | 「턱 쪽에 주로 나요」(부위만 `SITE-072`) | 「빨갛게 자국도 남았어요」(`CON-111` \| `CON-110`) | **없음** — 턴 1 「여드름이 계속 올라와요」 로 `focus` 있음 | 안 이음 | `[]` · 아님 | **맞음**(F-5 와 같음) |
| C38-4 | 「이마도 봐주세요」(부위만 `SITE-014`) | 「주름이요」(`CON-005` \| `CON-001`) | **없음** — 턴 2 「첫 번째요」 가 턴 1 의 QY7 되물음에 답해 고민이 들어 `focus` 있음 | 안 이음 | `[SITE-014]` · **꼭** | **갈린다** — 소넷이 `CON-005`(이마주름 — `concern_site` 에 `SITE-014`)를 고르면 검사 3 통과(고른 고민의 부위로 걸림) · `CON-001`(주름)을 고르면 `site_required` 에서 떨어진다. 키를 고칠지(`site_required` = 아님 또는 `CON-005` 만) · 규칙을 넓힐지는 E8-5 표본 검수에서(코디 · 사용자) |

- 넷 모두 키 · 턴을 이 판에서 고치지 않았다(발주서 「기존 키 · 턴은 바꾸지 않는다」). 「되물음」 판정은 실행 때 앞 턴 장부의 `consult.ask` 로 정해지므로 표의 앞 턴이 실행에서 다르게 돌면(예: 첫 턴 대상이 틀림) 위 칸도 달라진다.

### 8-2. D-11 의 시험 몫 — 정보 종류 · 값 · 깊이

| # | 무엇 | 방법 | 끝 조건 |
|---|---|---|---|
| E8-6a | 정보 종류 | **표에 이미 있는 키로 잰다**(`key.kinds` · `kinds_ok` — 0.1.0 의 「워커가 gold 로 짓는다」 를 고침 · 검수 F-6). 대상 = `key.kinds` 가 있는 턴 전부(fix1 전 134 · fix1 이 보탠 22 턴에도 있어 지금 156 — 실행 때 `score.py` 가 낸 수). 검사 = `score.py` `kinds_score` — 검증 뒤 `consult.understand.accepted.kinds` 가 기대 종류를 전부 담고 그 밖은 `kinds_ok` 안(0.3 의 「읽은 종류」 가 아니라 이해 호출의 값이라 `kinds_has` 가 아닌 엄한 쪽으로 본다) · 애매 턴 · 채점 밖 턴은 뺀다 | **통과 90% 이상**(U8-2 (a) — 코디 11-18 채택) |
| E8-6b | 값 · 깊이 | **재료 정답 키**(`key.material` — 표 C74 ~ C78 의 22 턴 · fix1 이 보탬): 값을 이름으로 물은 턴 13(부작용 · 금기 · 효과 — 「멍」 「항응고제」 「임신」 「화상」 「당김」 「내성」 …) · 상대를 이름으로 물은 턴 4(깊이 = 상대) · 상대를 이름 없이 물은 턴 4 · 상품 1(깊이 0). **키의 꼴**: `rows[[gid, …], …]` = 그 턴 재료(답 LLM 에 가는 「자료」 줄 — `material.new_lines[].gid` ∪ `seen_lines` 가 가리키는 앞 줄)에 **꼭 있어야 하는 gold 행**(바깥 = 전부 · 안 = 어느 것이든 — 물은 값의 행 · 물은 관계의 `g_pair` 행 · 물은 상품의 `g_offer` 행) · `depth[]` = **깊이 읽기를 해야 하는 노드**(U8-1 (가) = 이번 턴 대상인 깊이 후보 — 상대를 이름으로 물었으면 두 대상 · 이름 없이 물었으면 `[]`). 근거 = 각 턴 `basis` 의 「재료 — <gid> …」 · 「깊이 — …」(`build.py` 가 gold 행에서 적는다). 검사 셋: ⓐ `rows` 묶음 전부가 재료에 있다 ⓑ `trace.depth.decisions` 의 `gate_forced` ⊆ `depth` ⓒ `depth` 가운데 그 턴 깊이 후보로 선 것은 전부 `gate_forced`. 같은 턴을 0.3(값 고르기 · 깊이 켬 — 0.3 앱 실행)에도 돌려 **재료 줄 집합**을 견준다 | ⓐ ~ ⓒ 의 통과율 · 0.3 에만 있는 줄 수(깊이 조회 행) · 0.4 에만 있는 줄 수(안 좁힌 부작용 상세) · 메시지가 `ANSWER_INPUT_MAX_TOKENS` 를 넘은 턴 수(FT5)를 보고한다. **문턱은 U8-4** |
| E8-7 | 실물 화면 확인(답 LLM 포함) | 18222 에서 대화 셋 — 앞 답의 글을 가리키는 말 · 거둠 · 애매한 말(`sure` = `false` → BK5 되묻기) · 실패 길(시간 한도를 1초로 낮춘 한 턴) + 옛 끈 대화 하나를 열어 새 턴이 막히는지(CP7) | 턴마다 장부 `consult.understand` · `consult.site_filter` · 객체 diff · 화면이 §2 대로 |

### 8-3. 단위 시험(외부 호출 0 — 가짜 CLI · 가짜 허브)

| # | 무엇 | 기대 |
|---|---|---|
| S8-T1 | 목록 글 | 가짜 `g_entry` 로 — 표 머리 · 줄 꼴 · 별칭 괄호 · 같은 글자 별칭 한 번 · `CHAT_PICK_ALIASES=off` 면 괄호 없음 · 같은 입력 두 번 = 같은 글자(sha 같음) · `gold_hash` 가 바뀌면 다시 받는다 |
| S8-T2 | 호출 인자 | `--no-session-persistence` 있음 · `--resume` · `--session-id` · `--fallback-model` 없음 · 격리 인자가 `chat_args` 와 같은 값 · 시스템 글 = `pick.rules` + 목록 |
| S8-T3 | 턴 메시지 | 성공 턴 전부의 손님 말 · 대상 · 선택지 · 가까운 `CHAT_PICK_CONTEXT_TURNS` 턴에만 답 요약(앞 `CHAT_PICK_ANSWER_CHARS` 자) · 리스트 이름(`n) 이름(table:code)` · `CHAT_PICK_LIST_MAX` 까지) · 실패 턴은 표지 · 객체 블록(대상 · 애매 · 거둔 것) |
| S8-T4 | 검증 — 버림 | 목록에 없는 코드 · 다섯 표 밖 · 꼴 틀림 → `dropped[]` 에 `why` 와 함께 · 남은 것으로 턴이 돈다 · 전부 버려지면 「입구 없음」(FL6) |
| S8-T5 | 검증 — 접기 · 값 | 같은 이름 계열 · 시술 · 제품 → 계열 하나(`merged`) · 고민 ↔ 부위 같은 이름은 안 접음 · `kind` 셋 밖 → `new` · `talk` + 대상 → 대상 버림 · `follow` + `[]` → 앞 대상 · 첫 턴 `follow` → `new` · `withdraw` 가 객체에 없으면 버림 · `targets` 와 겹치면 거둠 · `kinds` 14 밖 버림 · **검증 뒤 대상은 전부 객체 diff 에 든다**(AR-6) |
| S8-T6 | 객체 | `sure` true → `said` · false → `guess`(축 아님 · BK5 빈 칸) · 선택지 답 → `how` = `option` · `follow` 의 객체 안 대상 → 급 그대로 · 객체 밖 대상 → `said` · `focus` = `targets` 순서 마지막 `said` 고민 · **순서 시험**(F-9): 가짜 출력 `targets` = [고민 A, 고민 B] → `focus` = B · [B, A] → A(앱이 다시 정렬하지 않는다) · 프롬프트 규칙 1 에 「말에 나온 차례대로」 줄이 있다 · 거둠 → `withdrawn` · `talk` 은 거둠으로만 바뀜 |
| S8-T7 | 부위 잇기(D-6 · F-5) | 앞 턴 「부위만」(그 턴 `targets` 전부 `site`) + 그 턴 `consult.ask.slot` = `concern` · `about` = 그 부위 + 이번 턴 고민만 · 부위 없음 → 이음(`site_filter.carried` · `from`) / 앞 턴에 고민 되물음이 없었음(`ask` 없음 또는 다른 `slot` — `focus` 가 있던 꼴) → 안 이음 / 앞 턴에 고민이 있었음 → 안 이음 / 이번 턴에 부위가 있음 → 안 이음 / 이번 턴에 고민 말고 계열 · 시술 · 제품이 같이 있음 → 안 이음 / 두 턴 앞의 「부위만」 → 안 이음 / 앞 턴이 실패 턴 → 그 앞의 성공 턴 기준 / 앞 턴이 `sites=[]` 로만 부위를 낸 꼴(VF8 받침 뒤 `targets` 의 부위)도 「부위만」 |
| S8-T8 | 부위 거르개(AR-4 · F-8) | `targets` 에 부위 A · `sites` = [A] → 거르개 A · `targets` 에 부위 A(앞 턴 부위를 다시 든 꼴) · `sites` = [] → 거르개 없음(A 는 객체에 그대로) · `sites` 에만 B · `targets` 에 없음 → `targets` 에 B 를 더하고(`added_from_sites`) 거르개 B / 턴 1 고민 + 부위 A · 턴 2 같은 고민 + 부위 B → 턴 2 의 `concern_candidates` 조회의 `site` = B 의 이름 하나(A 없음) · 장부 `consult.site_filter.sites` = 조회에 건 값과 같다 · 부위 없는 `new` 턴 + `focus` 그대로 → 리스트 조회 0(앞 리스트 유지) · `focus` 가 바뀌고 부위 없음 → 거르개 없는 조회 하나 · 같은 이름 부위는 짝 고민이 `focus` 일 때만 |
| S8-T9 | 정보 종류 | KS1 ~ KS8 — `kinds` `[]` → 기본 묶음 · `overview` → 한 벌 · 고른 종류가 범위에 있으면 안 고른 기본 묶음 종류는 `offered` · 안전 종류는 고를 때만 · 걷기의 `_decide_kinds` 에 같은 입력(yes = 1.0 · 그 밖 = 0.0)을 준 결과와 KS2 · KS4 가 닿지 않는 경우에 같은 `kinds` · `required` |
| S8-T10 | 깊이(§3-2) | 이번 턴 대상인 후보만 깊이 조회 · 그 밖은 `listed_only` 이고 폭 행은 재료에 그대로 · Jev 가짜가 **한 번도 안 불린다** |
| S8-T11 | 값(§3-3) | 값 종류를 물은 턴 — 부작용 상세 조회가 미뤄지지 않고 전부 읽힌다 · 재료에 `value_pick` 표지 0 |
| S8-T12 | 점(AR-5) | 고민의 `sites[]` 가운데 `match` = `직접` 만 점 · 하위 부위는 점 아님(선택지에는 있음) · 고민 둘이면 직접 부위의 합집합 · 거두면 빠짐 |
| S8-T13 | QY7(AR-11) | 부위만 → 선택지 = `concern_site` 묶인 고민 먼저 ∪ facets 행의 고민 · 같은 고민 한 번 · facets 가 0 행이어도 묶인 고민이 나온다 · 색인은 `gold_hash` 마다 한 번 짓는다 |
| S8-T14 | NQ5(AR-12) | 앞 `ask` 에 답 안 함 + QY7 이 선 `new` 턴 → 묻는다 / 그 밖의 턴 → 0.3 그대로 안 묻는다 |
| S8-T15 | 실패 길 | 시간 초과 · CLI 오류 · JSON 깨짐 · 목록 실패 넷 — 객체 diff `[]` · 허브 조회 0 · `list` · `sites` 이벤트 없음 · 종료 상태 「입구 없음」 · 답 LLM 은 불린다 · `resolve` 맞춤 꼴 · Jev · 두 번째 이해 호출 0 · 다음 턴이 정상으로 돈다 |
| S8-T16 | 재조회 없음(D-12) | `new` 가 앞 대상만 다시 들고 부위 없음 → 객체 기준 조회의 허브 호출 0(메모) · `list` 이벤트 없음 |
| S8-T17 | 장부 | `consult.understand` 의 칸 전부(`pick_version` · `added_from_sites` 포함) · `consult.site_filter` 의 칸 전부(F-4) · `consult_rev` 4 · 없어진 칸(`nouls` · `retract` · `trace.entry_pick` · `source.noul`)이 줄에 없다 · rev 3 켠 대화는 턴을 받지 않는다 |
| S8-T18 | 경로 나눔(D-2 · F-10) | **기존 함수 동작 · 기존 시험 불변**: `clinic_chat/walk/` · `clinic_chat/columns/` 의 기존 시험(끈 상태 0.1 시험 S5-T15 등 · 걷기 시험)이 그대로 통과 · `columns/` · `prompts/jev/` 의 diff 0 · `walk/` 의 diff = §3-4 의 공개 감쌈 추가뿐(기존 줄의 바뀜 · 지움 0 — `git diff` 가 더한 줄만이고 각 감쌈 본문은 감싼 함수를 부르는 한 줄) · 켠 턴에서 Jev 가짜 · `hub.resolve(text=…)` 가 0 번 불린다 · 걷기 코드를 상담 쪽에 베낀 함수 없음(§3-4 표의 함수를 부른다) |
| S8-T19 | 끈 상태(F-1 ⓒ · CP1 · CP7) | 설정 기본값 `chat_state` = `on` · `CHAT_STATE=off` 를 주어도 새 대화의 장부 첫 줄 `consult_state` = `on` · 장부 첫 줄이 `off` 인 옛 대화 → 열기(드로어 · 지난 턴)는 되고 `POST …/turns` 는 막힌다(새 턴 줄 0 · Jev · 허브 0) · 막는 화면 자리는 빈 `data-slot` 하나(문구 없음 — U8-3) · `turn.py` 의 끈 가지 코드는 남아 있다 |
| S8-T20 | 프롬프트 적재기(F-7) | `pick` 절 없음 · 한 칸이라도 빔 → `pick` = `None` · `state_ready` = 거짓(켠 대화를 시작하지 않는다) · `jev_state.retract` · `jev_front.target_option` · `turn_kind` 가 없어도 `pick` 이 있으면 `state_ready` = 참 · `jev_front` 절을 지우면 `parse` 가 `keys` 로 떨어진다(지금 그대로) · `pick.version` 에 `-draft` 가 있어도 `draft` 는 최상위 `version` 으로만 정해진다 |

- 0.3 의 단위 시험 가운데 Jev 점수 · 걷기 trace 를 재료로 한 것(턴 종류 판정 순서 · 든 후보 · 줄임 후보 · `guess` 사이 값 · 거둠 요청)은 **켠 상태 기대가 없어진다** — 지울지 · 끈 상태 쪽으로 옮길지는 WORK 에서 시험 이름별로 적는다.

## 9. 정할 것

D-1 ~ D-15 · 「소넷으로만」 으로 닫힌 것은 다시 올리지 않았다.

### 9-1. 사용자(추천 붙임)

| # | 정할 것 | 선택지 | 추천 | 근거 |
|---|---|---|---|---|
| ~~U8-1~~ | 값 고르기 · 깊이 판단의 자리(§3-2 · §3-3) — **결정됨 (가)**(코디 11-18 — 소넷 호출 안 더함 · 깊이 = 이번 턴 대상만 · 값 표지 없앰) | (가) 호출을 더하지 않는다 — 깊이 = 이번 턴 대상인 후보만 · 값 표지 없음 · 상세 전부 읽음(본문) (나) 폭 읽기 뒤 두 번째 소넷 호출로 값 · 깊이를 고른다(그 턴만 한 호출 더) (다) 목록에 사건 · 조건 · 효과 표를 더해 값을 대상으로 뽑는다 | **(가)** — E8-6b 의 수(잃는 줄 · 느는 줄 · FT5 턴)를 보고 모자라면 (나) | 값 고르기 · 깊이는 재료 행을 **빼지 않던** 단계다(§3-0). (나)는 턴당 지연이 는다 · (다)는 D-3 의 목록과 표의 채점 표가 바뀐다. 결정 행도 「이번 표로 안 쟀다」 |
| ~~U8-2~~ | 정보 종류 검사(E8-6a)의 문턱 — **결정됨 (a) 90%**(코디 11-18) | (a) 90%(앱 전체와 같은 값) (b) 수만 보고하고 문턱 없음 (c) 입구 검사에 넣어 네 검사 95% | **(a)** | D-14 는 8 검사 · 3 검사만 정했다. 정보 종류가 틀리면 답 재료가 통째로 달라진다 — 문턱 없이 두기 어렵다. 키가 새로 지어지는 칸이라 (c)는 이르다 |
| U8-3 | 옛 끈 대화를 열었을 때 새 턴을 막는 화면 문구(CP7 — 빈 `data-slot` 하나) | (가) 문구 한 줄을 사용자가 준다 (나) 문구 없이 입력칸만 막는다(빈칸 그대로) | — **추천 없음**(화면 문구는 짓지 않는다 — 코디 F-1 ⓒ 「빈칸 + 정할 것」) | 0.4 이전에 끈 상태로 시작된 대화만 닿는다(그런 대화가 서버에 몇 개인지는 장부로 센다 — WORK) |
| U8-4 | 재료 정답 키 검사(E8-6b ⓐ ~ ⓒ)의 문턱 | (a) ⓐ 90% · ⓑ ⓒ 100%(깊이 결정은 결정론이라) (b) 수만 보고 — 문턱 없음(0.1.0 본문) (c) ⓐ 도 100% | **(a)** — 22 턴은 값 · 관계 행이 gold 에 바로 있는 턴만 골랐다(근거 `basis`). ⓑ ⓒ 는 DP8-2 의 결정론 규칙이 그대로 드러나는 자리라 빠지면 구현 오류다. 0.3 과의 줄 수 비교는 문턱 없이 보고 | 코디 F-6 은 「키 꼴을 적고 표본을 보탠다」 까지 — 문턱은 정해지지 않았다 |

### 9-2. 코디 기본값(바꿀 것만 말하면 된다)

| # | 무엇 | 본문 값 | 달리 갈 길 |
|---|---|---|---|
| C8-1 | 부위 → 고민 거꾸로 색인을 얻는 길(QS6) | 앱이 `gold_hash` 마다 한 번 고민 260 의 `concern_candidates(limit=1)` 머리로 짓는다(허브 변경 0) | 허브에 부위 쪽 입력 · 도구를 더한다(SPEC-001 다음 판 — 이번 발주는 「다른 도구 계약은 건드리지 않는다」) |
| C8-2 | NQ5 좁힘(BQ4) | QY7 이 선 `new` 턴만 NQ5 를 안 건다(SPEC-005 검수 W-2 를 한 곳에서 달리 받음) | 그대로 두고 E8-4 의 「부위만 → 선택지」 검사로 다시 본다 |
| C8-3 | 앞 답 요약(UC7) | 답 본문 앞 200 자 · 가까운 2 턴 · 리스트 이름 30 개 — LLM 요약 없음 | 답 꼬리에 요약 한 줄을 쓰게 한다(`system_v3.tail` 문구가 바뀐다 — 사용자 문구) |
| C8-4 | 0.3 으로 시작한 켠 대화 | 0.4 서버에서 끝난 대화(`rev_changed`) — 0.3 길을 코드에 남기지 않는다 | — |
| C8-5 | thinking 을 끄는 방법(UC3) | E8-0 에서 실측으로 정한다 · CLI 로 못 끄면 올린다 | SDK(D-4 「배포 전 SDK」)를 앞당긴다 |
| C8-6 | 첫 턴의 `kind`(VF7) | `talk` 는 받고 `follow` 는 `new` 로 | SPEC-006 TK2 그대로 첫 턴은 늘 `new` |
| C8-7 | 실패 턴의 말(FL2) | 종료 상태 「입구 없음」 의 0.3 말을 그대로 쓴다(새 문구 0) | 실패 전용 자리를 `system_v3.material` 에 더한다(사용자 문구) |
| C8-8 | 옛 끈 대화를 막는 자리(CP7) | 켠 rev 3 대화의 `rev_changed` 와 같은 자리 · 같은 꼴(끝난 대화로 읽기만) | 옛 끈 대화도 0.4 켠 상태로 이어 돌린다(대화 첫 값을 바꾼다 — 코디 F-1 ⓒ 의 「읽기만」 과 갈린다) |
| C8-9 | `columns/col_b.py` 의 밑줄 함수(`_labels` · `_end_check`)를 부르는 꼴(§3-4) | 그대로 import 해 부른다(`columns/` diff 0) | `columns/` 에도 얇은 공개 감쌈을 허용한다(F-10 예외를 넓힘 — 코디) |

### 9-3. 열린 것

| # | 무엇 | 언제 |
|---|---|---|
| O8-1 | 이해 호출의 실서버 지연 · 캐시가 식은 첫 호출(목록 14.8k 토큰 쓰기) — 조사 수는 개발 Mac · 캐시 따뜻 조건(검수 R-10 · §5) · **QS6 거꾸로 색인을 짓는 턴**(그 `gold_hash` 의 첫 QY7 턴 — `concern_candidates(limit=1)` 고민 수만큼 · 장부 `consult.site_index.ms` · `calls` — 검수 F-12) | 구현 뒤 서버에서 — 색인 턴이 느리면 서버 시작 때 짓기로 옮길지 코디 |
| O8-2 | 표 밖 꼴(검수 §4 — 여러 문장 · 30 자 넘는 말 · 「아니 턱이 아니라 볼이요」 같은 바로잡기 · 받아 본 시술 · 목록에 없는 시술을 가까운 것으로 끌어다 붙임)에서의 값 | E8-5 표본 검수 때 표에 보탤지 |
| O8-3 | 「받아 본 것」(「보톡스는 해봤는데 효과 없었어요」)을 대상으로 잡을지 거둘지 — 약속이 없다(검수 §4) | 표에 그 꼴이 들어올 때 |
| O8-4 | `viewable_subs`(하위 점 누르기) · `entry_pick` · `abbr_yes_only` · 켠 상태에서 안 읽는 설정의 정리 | 마감 뒤(B 열을 다시 볼 때) |
| O8-5 | 대화가 길어질 때 대화 블록의 길이(성공 턴 전부 — 턴 한도 `CHAT_MAX_TURNS` 20 안에서는 조사의 턴 메시지 중앙 343 자에 답 요약 · 리스트가 는다) | E8-3 재실행의 입력 바이트로 |

## 10. 구현 결과 되적기(0.2.1)

근거: `$W/_RESUME.md` §2 2026-11-18 「앱 0.4 코드 검수 WARN 코디 답」 · 「E8-0」 · 「상담 0.4 결과 = 이 정도면 받음」 · §5 「앱 fix1」 · `$W/review-code-app-v04.md` · `$W/WORK-017-consult-v04.md` §B · 앱 `296cb2c`(구현 결과가 정본) · `$W/research-input-space/runs/v04c-score` · `v04d-score`. **새로 정한 것 0** — 아래는 구현 · 검수 · 사용자 답이 이미 정한 것이다.

### 10-1. 구현에서 달리 받은 것

| # | 본문 | 구현(`296cb2c`) | 근거 |
|---|---|---|---|
| R8-1 | VF6 · VF11 차례(§2-3) | **VF11 을 VF6 앞에** — 턴 종류(VF6 셋 밖 · VF7 · VF11)를 먼저 정하고 대상을 거른다. VF11 이 `talk` → `new` 로 읽은 턴은 대상을 버리지 않는다 | `verify.py` 머리말 · 코드 검수 §2 「맞음 — VF11 의 뜻」 |
| R8-2 | `new` + `targets []` + `withdraw [x]`(거둠만) | **`talk` 갈래로 읽는다**(`turn_kind.from` = `withdraw_only`) — 객체가 바뀌면 조회 · 리스트를 다시 보낸다(TT2). 「입구 없음」 으로 가서 거둔 항목이 화면에 남던 것(코드 검수 L-1)을 막는다 · **사용자 확인 목록** | `verify.py` 끝 · `_RESUME` §2 「앱 0.4 코드 검수 WARN 코디 답」 L-1 |
| R8-3 | EN1 의 상품 이름 입구 | **`offer_name` 길 없음** — 상품 이름 입구는 resolve 맞춤 꼴의 몫이었다. 목록이 다섯 표(LD8)라 상품(`g_offer`)은 `offer` 종류 재료로만 온다. 계약과 부딪히지 않는다 | 코드 검수 §2 QM 줄 ⓐ |
| R8-4 | `site_index` 캐시(QS6 · C8-1) | 캐시 키 = (`gold_hash`, 목록 sha) — LD5 와 같은 뜻 · 더 엄하다. 고민 하나가 실패해도 **그 고민만 뺀 색인을 캐시**한다(실패 수는 지은 턴 `site_index.errors`) — 실패 뒤 260 호출 되풀이 0 | `site_index.py` · 코드 검수 L-4 · 「받은 것」 ⑤ |
| R8-5 | `pick.headers`(§7 「WORK 에서 정한다」 · WORK B-4) | 머리 글자 **9** = 코디가 정한 셋(「앞 답 요약:」 · 「보여 준 리스트:」 · 「(앞과 같음)」) + 구현이 지은 여섯(`picked` · `options` · `obj_targets` · `obj_guess` · `obj_withdrawn` · `user`). 손님에게 안 보인다. 하나라도 비면 `pick` = `None` → 켠 대화 시작 불가(적재기 필수 키 — `headers` 열하나 · `marks` 셋). `pick.version` = `0.4.0-draft` · **사용자 확인 목록** | `prompts/consult.json` · 코드 검수 L-2 · `_RESUME` §2 R-5 |
| R8-6 | KS7 「강한 판정」(§3-1) | `kinds_pick.STRONG_BY` = `yes` · `entry` · **`kd9`**(0.3 `STRONG_BY` 그대로) — 본문은 `yes` · `entry` 만 적었다 | `kinds_pick.py:18` · 코드 검수 §2 QM 줄 ⓑ |
| R8-7 | E8-0 · C8-5 thinking 끄기 | **CLI 로는 완전히 못 끈다** — ⓐ `--settings '{"alwaysThinkingEnabled": false}'` + env `MAX_THINKING_TOKENS=0` 으로 두었다(`CHAT_PICK_THINKING=off` 의 뜻). 20 호출 가운데 4 ~ 5 회 thinking 이 선다 → **SDK 의 몫**(D-4 「배포 전 SDK」) | `understand.py:5-6 · 22` · `_RESUME` §2 「E8-0」 |
| R8-8 | §8-1 앞 답을 가리키는 턴 | **`answer_ref` 턴은 D-14 분모 밖**에서 따로 센다 — 답 LLM 을 실물로 부른 다섯 대화(C56 · C57 · C58 · C65 · C69)의 둘째 턴부터. 표의 키가 가짜 앞 답 기준이라 실물 답과 어긋난다(코드 검수 M-1). 채점 턴 = 336 − 18 = **318** | `score.py` `answer_ref` · `_RESUME` §2 M-1 |

### 10-2. E8 결과(같은 코드 두 판 · 채점 318 턴)

| 판 | 3 검사(E8-3 · 문턱 95) | 8 검사(E8-4 · 문턱 90) | 지연 턴 중앙 · p90 |
|---|---|---|---|
| v04c | **94.3%**(300/318) | **88.7%**(282/318) | 3.0 · 5.6초 |
| v04d | **95.3%**(303/318) | **90.9%**(289/318) | 3.0 · 5.5초 |

- **비결정 폭**(코드 검수 L-8 — 같은 코드로 두 번): 8 검사에서 갈린 턴 19(v04c 만 실패 13 · v04d 만 실패 6) · 3 검사는 통과 수가 순 3 턴 차이다. 두 판 모두 문턱 경계에 걸쳐 있다.
- `answer_ref`(분모 밖) 18 턴: 두 판 모두 8 검사 · 3 검사 통과 8. 사람 검수 몫(§10-3).
- 이해 오류 9 턴(시간 초과 6 · JSON 덧붙임 3 — 두 판 같은 턴 · `_RESUME` §5 「앱 fix1」).
- **사용자 결정**: 「이 정도면 받음」(`_RESUME` §2 11-18 「상담 0.4 결과 … = 이 정도면 받음」) — 이번 판은 이 수로 닫는다. 문턱(D-14)을 고치지 않았다.

### 10-3. 남은 것(다음 작업)

| # | 무엇 | 근거 |
|---|---|---|
| N8-1 | **SDK 에서 thinking 끔** — 이해 호출을 SDK 길로 옮겨 시험(앱 `.env` 의 API 키가 비어 있어 키가 필요) | `_RESUME` §2 「thinking 은 SDK 에서 끈다」 · R8-7 |
| N8-2 | **`pick` 확정** — `0.4.0-draft` 의 규칙 · 머리 글자 9(R8-5) · 거둠만 = `talk`(R8-2)를 사용자 확인 | §7 · R8-2 · R8-5 |
| N8-3 | **막힘 · 새 대화 문구** — 옛 끈 대화를 막는 화면 문구(U8-3 · 빈 `data-slot`) | §9-1 U8-3 |
| N8-4 | **`answer_ref` 사람 검수** — 실물 앞 답으로 키를 다시 매기거나 채점을 가른다(R8-8 · E8-5) | 코드 검수 M-1 |
| N8-5 | **JSON 덧붙임** 처분 — 이해 출력 뒤에 글이 붙어 VF1 에서 떨어지는 턴(3) · SDK 결과로 다시 본다 | `_RESUME` §2 「SDK … JSON 덧붙임 처분도 SDK 결과로 다시 봄」 |
| N8-6 | **시간 한도** — `CHAT_PICK_TIMEOUT_SEC` 10초에서 시간 초과 6 턴 · SDK 결과로 다시 본다 | 같은 행 · UC9 |

## 부록 A. 결정 행 → 이 문서

| 결정(11-18) | 규칙 |
|---|---|
| D-1 | LD1 · SPEC-001 0.8.0 |
| D-2 | CP1 ~ CP4 · S8-T18 |
| D-3 | LD2 ~ LD4 |
| D-4 | UC2 · UC3 · E8-0 |
| D-5 | OU6 · §7 규칙 3 |
| D-6 | OU7 · S8-T7 · §8-1 「D-6 규칙과 표의 키」 |
| D-7 | VF4 · VF5 · §7 규칙 4 |
| D-8 | UC6 · UC7 · §7 규칙 9 |
| D-9 | UC8 · OU2 · BQ2 · §7 규칙 10 |
| D-10 | UC9 · §4-1 · S8-T15 |
| D-11 | UC8 `kinds` · §3 · §3-4 · §7 규칙 11 · E8-6a · E8-6b · U8-1 · U8-2 |
| D-12 | OU5 · QS4 · S8-T16 |
| D-13 | QS6(DA-1) — DA-2 · 4 · 5 는 데이터 작업(이 문서 밖) |
| D-14 · D-15 | §8-1 |
| 「소넷으로만 — Jev 뺌」 | UC1 · CP2 · §3 · §6-1 |
| 「resolve = 최소 목록 꼴 · 입력 정리는 채팅 단」 | LD1 · VF12 |
| 「SPEC-008 검수 WARN 16 코디 답」 | CP1 · CP3 · CP7 · VF8 · OU7 · OU9 · §3-4 · §7 · §8 · §9 · 변경 기록 0.2.0 |

## 변경 기록

### 0.2.1 — 2026-11-18 · 마감 되적기 — 구현에서 달리 받은 것 · E8 결과 · 남은 것

근거: `$W/_RESUME.md` §2 2026-11-18 「앱 0.4 코드 검수 WARN 코디 답」 · 「E8-0」 · 「상담 0.4 결과 = 이 정도면 받음」 · §5 「앱 fix1」 · `$W/review-code-app-v04.md` · WORK-017 §B · 앱 `296cb2c` · `runs/v04c-score` · `v04d-score`. 새로 정한 것 0.

- **§10 을 더했다**: 10-1 달리 받은 것 R8-1 ~ R8-8(VF11 을 VF6 앞 · 거둠만 = `talk`(`withdraw_only`) · `offer_name` 길 없음 · `site_index` 캐시 키 · `pick` 머리 글자 9 · KS7 `kd9` · CLI thinking 못 끔 → SDK 몫 · `answer_ref` 분모 밖) · 10-2 E8 결과(v04c/v04d 3 검사 94.3/95.3 · 8 검사 88.7/90.9 · 비결정 폭 · 「이 정도면 받음」 사용자 결정) · 10-3 남은 것 N8-1 ~ N8-6(SDK thinking 끔 · `pick` 확정 · 막힘/새 대화 문구 · `answer_ref` 사람 검수 · JSON 덧붙임 · 시간 한도).
- 본문에 한 줄씩: §2-3 VF11(차례) · §8-1 E8-0(결과).

### 0.2.0 — 2026-11-18 · 검수(`review-spec-008.md`) WARN 16 고침 — 코디 답 반영

근거: `$W/_RESUME.md` §2 2026-11-18 「SPEC-008 검수 WARN 16 코디 답」 행 · `$W/review-spec-008.md` · `$W/spec-008-fix1-brief.md`(발주서). 이 워커는 서버 · DB · LLM · Jev 를 부르지 않았다 · 앱 · 허브 코드를 고치지 않았다(읽기만 — 줄 번호 = 앱 `be1c622` · 허브 `d97a9ad`). 표는 `build.py` 로만 다시 냈다.

| F | 처분 | 고친 곳 |
|---|---|---|
| F-1 | 코디 ⓒ — 0.4 서버는 끈 상태 대화를 새로 열지 않는다(`chat_state` 기본 `on`) · 옛 끈 대화 = 「옛 판 대화」 읽기만 · 새 턴 막음(문구 빈칸 → U8-3) · SPEC-001 0.8.1 영향 표에 끈 상태 줄 + 「0.4 켠 상태는 0.7.2 허브로도 돈다 — 같이 올리는 것이 필수는 아니다」 | 머리말 · §0 · CP1 · **CP7(새)** · §4-2 · S8-T19 · E8-7 · U8-3 · C8-8 · SPEC-001 0.8.1 |
| F-2 | 끝 조건을 고정 수 대신 「실행 때 `score.py` 가 낸 수」 로 · 표 판(지금 78 대화 · 356 턴 · 애매 18)은 참고로만 · 「스크립트를 코디가 옮긴다」 줄 지움(이미 `research-input-space/scripts/`) · §1-1 의 수는 「조사 판」 으로 표지 · D-15 「애매 14」 는 조사 판 수로 밝힘 | 머리말 · §0 · §1-1 · §1-2 D-15 · §8-1 E8-1 ~ E8-5 |
| F-3 | `ref.to` = `answer` 턴 = 표에서 직접 센 **5**(C56-5 · C57-2 · C58-3 · C65-4 · C69-2) — 표 실행에서 답 LLM 실제 호출 · 그 턴이 든 대화 전부(C56 · C57 · C58 · C65 · C69) · 코디의 「7」 = 의도 꼴 `답참조` 태그 수(C57-5 애매 · C67-3 `ref` 없음이 더해짐) · E8-7 = 실물 화면 확인만 | §8-1 불릿 · E8-7 |
| F-4 | 장부 `consult.site_filter`(새 칸) · E8-pre = `score.py` / `slim.py` 를 0.4 장부 칸에 맞추는 단계(대상 = `targets[]` · 거둠 = `accepted.withdraw` · 거르개 = 새 칸 · 재료 · 깊이 칸을 `slim.py` 에) | §6-1 · QS1 · §8-1 E8-pre · S8-T17 |
| F-5 | D-6 의 「답」 = 앞 턴 되물음에 대한 답으로 좁힘(OU7 ⓓ = 앞 턴 `consult.ask.slot` = `concern` · `about` = 그 부위) · 네 턴 표(C05-2 맞음 · C15-3 맞음 · C28-3 맞음 · C38-4 갈림 → E8-5 이름 박은 표본) | §1-2 D-6 · OU7 · AR-4 · §8-1 「D-6 규칙과 표의 키」 · E8-5 · S8-T7 |
| F-6 | E8-6a = 있는 정보 종류 키로(지금 156 = 134 + fix1 22) · 문턱 90%(U8-2 (a) 결정) · U8-1 (가) 결정 · E8-6b 에 재료 정답 키의 꼴(`key.material{rows, depth}`) · **표에 22 턴 보탬**(C74 ~ C78 — 값 13 · 상대 이름 4 · 상대 이름 없음 4 · 상품 1 · gold 근거 `basis`) · 문턱은 U8-4 로 | §0 · §1-2 D-11 · §3-2 · §3-3 · §8-2 · §9-1 · 표 · `scripts/convs.py` · `convs2.py` · `build.py` · README |
| F-7 | 프롬프트 적재기 계약 표(필수 키 · `pick` 절 · `state_ready` 를 `pick` 기준으로 · `jev_front` · `jev_state` 남김 · `draft` 는 최상위 `version` 만) | §7 「적재기 계약」 · S8-T20 |
| F-8 | 부위는 늘 `targets[]` 에도(`table` = `site`) · `sites[]` = 그 가운데 이번 턴 거르개 · 「부위만」 / 「대상 0」 이 갈림 · `sites` 에만 온 부위는 앱이 `targets` 에 더함 | UC8 표 · VF8 · OU3 · OU7 · QM3 · §7 규칙 1 · 3 · 7 · S8-T8 |
| F-9 | `targets` 순서 = 말에 나온 차례 · `focus` = 마지막 고민 | UC8 표 · OU9 · AR-10 · §7 규칙 1 · S8-T6 |
| F-10 | 함수 서명 표 · `walk/` 에 얇은 공개 감쌈(동작 변경 0)은 diff 0 의 예외 · `columns/` 밑줄 함수는 그대로 부름(감쌈 넓힘은 C8-9) · S8-T18 = 「기존 함수 동작 · 시험 불변」 | §0 · CP3 · **§3-4(새)** · S8-T18 · C8-9 |
| F-11 | SPEC-001 0.8.1 — 고칠 · 지울 허브 시험 표 · T27 에서 T3 를 뺌 | SPEC-001 §9 T27 · 변경 기록 0.8.1 |
| F-12 | 거꾸로 색인을 짓는 때(그 `gold_hash` 의 첫 QY7 턴)와 장부 `consult.site_index{…, ms, calls}` · O8-1 에 더함 | QS6 · §6-1 · O8-1 |
| F-13 | VF4 의 `norm` = 허브 R1 식 · VF10 의 순서 = `walk/kinds.py:38` `KIND_CODES`(`state.py:30` `KIND_CODES_14` 와 다름을 밝힘) | VF4 · VF10 |
| F-14 | 줄 번호: `plan.py:27` ALLOWED · `:193` run · `:228-266` derive · `:46` Reader · `state.py:24-25` SLOT_OF · `:28` KEEP · `:29` WISH_KINDS · `turn.py:143` renumber | §2-4 · §2-5 · §3-0 · §5 |
| F-15 | 「조회 부위 거르개는 이번 턴만」 · 「점은 말한 고민만」 의 출처 = 발주서 ⑤ · ⑥(`_RESUME` 아님) · VF2 는 `_RESUME` 11-18 | QS1 · DT1 · VF2 |
| F-16 | 예문 「팔뚝에 살」 → 「등에 여드름」 · 356 턴과 다시 대조(겹침 0) | §7 규칙 2 · 예문 불릿 |

- **끌어낸 것**: ① 옛 끈 대화를 막는 자리를 켠 rev 3 대화의 `rev_changed` 와 같은 꼴로(C8-8) ② VF8 ⓑ ⓒ(앱 받침 — `sites` 에만 온 부위를 `targets` 에 더함 · `targets` 의 부위 가운데 `sites` 에 없는 것은 거르개 아님) ③ OU7 ⓓ 의 판정 재료 = 앞 턴 장부 `consult.ask`(slot · about) ④ E8-6a 를 `kinds_has` 가 아닌 엄한 `kinds_score` 로 ⑤ U8-4 를 새로 올림(코디 F-6 이 E8-6b 문턱을 정하지 않았다) ⑥ 앞 답 턴의 실물 실행 범위 = 그 다섯 대화 전부(25 턴).
- **확인하지 못한 것**: 공개 감쌈 이름(§3-4 — WORK) · 0.4 서버에 남은 옛 끈 대화 수 · C38-4 의 실행 결과(소넷이 어느 고민을 고르나).

### 0.1.0 — 2026-11-18 · 처음 씀

근거: `$W/_RESUME.md` §2 2026-11-18 행 넷 · 조사 · 검수 · 시안 · 앱 `be1c622` 코드. 이 워커는 서버 · DB · LLM · Jev 를 부르지 않았고 앱 · 허브 · 데이터를 고치지 않았다.

- **끌어낸 것**(다르게 읽을 수 있어 따로 밝힌다): ① 답 재료는 걷기 ② 의 결정론 함수를 그대로 부른다 — 발주서 ⑤ 는 「객체 기준 조회」 만 적었으나 그 조회의 닫힌 목록에 정보 종류 재료가 없다(§3-0) ② 값 고르기 · 깊이는 「소넷 꼴」 을 **이해 호출 하나가 대신하는 꼴**로 읽었다(호출을 더하지 않음 — U8-1) ③ 출력에 `out`(범위 밖)을 더했다 — 발주서 ② 의 필드 목록에는 없고 결정 행 「소넷으로만」 의 「범위 밖」 에서 왔다 ④ D-6 의 부위 잇기는 소넷이 아니라 앱이 한다 ⑤ D-7 의 접기는 계열 · 시술 · 제품 사이로 읽었다(고민 ↔ 부위 같은 이름은 0.2 결정대로 둘 다) ⑥ 사건 · 조건 · 효과 표는 목록에 없어 이해 호출의 대상이 아니다(LD8). ⑦ D-14 의 「8 검사 90%↑ · 3 검사 95%↑」 를 **검사마다의 통과율이 아니라 「해당 검사를 모두 통과한 턴의 비율」** 로 읽었다(E8-3 · E8-4 — 조사의 「지금 115 / 239」 · 검수 표 C 의 「소넷 229 / 239」 와 같은 자) — 검사마다로 읽으면 더 느슨하다.
- **확인하지 못한 것**: CLI 에서 thinking 을 끄는 인자(C8-5) · `mat.renumber` · `build` · `check` 가 `Walk` 객체 없이 불리는 꼴(상담 쪽이 같은 칸을 가진 그릇을 지어 넘겨야 한다 — WORK 에서 함수 서명으로 확인) · 시안 목록의 별칭 식이 LD2 와 글자까지 같은지(E8-1).
