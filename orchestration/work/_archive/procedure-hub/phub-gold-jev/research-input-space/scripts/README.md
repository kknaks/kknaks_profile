# 입력 전수 표 — 다시 돌리는 법

2026-11-18 · 조사 워커가 scratchpad 에서 쓰던 스크립트를 옮긴 것. 앱 · 허브 · gold 를 고치지 않는다(부르기만).

## 파일

| 파일 | 하는 일 | 무엇으로 돌리나 |
|---|---|---|
| `paths.py` | 경로 한 곳(레포 루트 · silver-model · `runs/`) — env `INPUT_SPACE_SILVER_MODEL` · `INPUT_SPACE_RUN_DIR` 로 바꿈 | — |
| `convs.py` · `convs2.py` | 대화 DSL(C01~C55 · 보강 C56~C73 · 값 · 깊이 키 C74~C78 + 기존 턴의 정보 종류 정답 `KMAP`) | — |
| `build.py` | DSL → `../conversations.jsonl`(코드 검사 · 근거 칸 · 꼴 수) | 아무 python3 |
| `run_now.py` | 앱 한 턴 흐름(`consult.turn.run_turn` · `CHAT_STATE=on`)을 대화마다 돌림 · 답 LLM 자리는 빈 답 | 앱 venv |
| `slim.py` | 앱 장부 → 채점이 읽는 칸만(`runs/<이름>-rows.jsonl`) | 아무 python3 |
| `score.py` | 채점(쓰는 자리 = env `INPUT_SPACE_OUT` · 기본 `..`) → `../now-turns.jsonl` · `../pick-*-turns.jsonl` · `../fan-*-turns.jsonl` · `../fail-by-tag.csv` · `../summary.json` | 아무 python3 |
| `fan_extra.py` | fan-out 문턱별 · 「윗층 받아 준」 채점(fan-out 에만 적용) → `summary.json` 에 더함 | 아무 python3 |
| `tables.py` | `summary.json` → 리포트 표(마크다운) | 아무 python3 |
| `pick.py` · `jev_pick.py` · `jev_fan.py` | **11-18 측정에 쓴 시안**(소넷 · 하이쿠 후보 뽑기 / 옛 `jev_front` 지시문으로 Jev 확정 / Jev fan-out) — 되풀이용 | 앱 venv |

`../runs/` = 11-18 실행의 원 기록(`now-rows.jsonl` 255 줄 · `pick-*.jsonl` · `fan-*.jsonl` · `tables.out`). 이것만으로 `score.py` 가 리포트의 수를 다시 낸다.

## 돌리는 법

```sh
cd orchestration/work/phub-gold-jev/research-input-space/scripts
A=/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev        # 앱 워크트리

python3 build.py                                                   # 표를 고쳤을 때만(DSL → conversations.jsonl)

# 앱 전체(8 검사) — 허브 18105 · 앱 .env 가 있어야 한다. 실행 이름은 아무 글자(장부 = runs/<이름>/turns.jsonl)
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$A $A/.venv/bin/python run_now.py v04            # 전부 · 끊기면 같은 명령으로 이어 돈다
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$A $A/.venv/bin/python run_now.py v04 C56,C57    # 대화 몇 개만
python3 slim.py ../runs/v04/turns.jsonl v04                        # → runs/v04-rows.jsonl
INPUT_SPACE_NOW=v04-rows.jsonl python3 score.py                    # 채점(now-turns.jsonl · summary.json 을 덮어쓴다)
python3 fan_extra.py && python3 tables.py > ../runs/tables.out     # 표

# 상담 0.4(SPEC-008 E8 · WORK-017 WP-12) — 앞 답 가리킴 5 대화는 답 LLM 실제 호출 · 채점 출력은 조사 산출물을 덮지 않는 자리로
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$A $A/.venv/bin/python run_now.py v04 --real-answer C56,C57,C58,C65,C69
python3 slim.py ../runs/v04/turns.jsonl v04 && INPUT_SPACE_NOW=v04-rows.jsonl INPUT_SPACE_OUT=../runs/v04-score python3 score.py

# 엄격 채점(검수 R-3)
INPUT_SPACE_STRICT=prior python3 score.py      # 앞 턴 정답을 다시 든 것을 군더더기로 센다
INPUT_SPACE_STRICT=extras python3 score.py     # extras_ok 를 끈다
```

- `run_now.py` 의 `runs/<이름>/turns.jsonl` 은 앱 장부 그대로라 크다(255 턴에 31MB) — 커밋 전에 `slim.py` 로 줄이고 원본은 지운다.
- `score.py` 는 `runs/` 에 있는 것만 채점한다. 실행 기록이 없는 대화(지금은 C56~C78)는 건너뛴다.
- 표 크기는 고정 수로 적지 않는다 — `build.py` 가 찍는 `convs … turns …` · `amb …` 가 그때의 수다(11-18 fix1 뒤 78 대화 · 356 턴 · 애매 18 · 정보 종류 키 156 · 재료 키 22). `key.ref.to` = `answer` 인 턴 = 5(C56-5 · C57-2 · C58-3 · C65-4 · C69-2) — 의도 꼴 「답참조」 7 턴과 다르다(C57-5 는 애매라 `ref` 없음 · C67-3 은 「덜 아픈 쪽」 이라 `ref` 없음).
- 시안 되풀이: `… $A/.venv/bin/python pick.py sonnet on [대화,…]` → `runs/pick-sonnet-on.jsonl` · `… jev_pick.py pick-sonnet-on.jsonl` · `… jev_fan.py on tables`. `pick.py` 의 규칙 글에는 표의 턴과 같은 예문이 8 개 있다(검수 R-4) — 새 프롬프트의 예문은 표 밖 말로 쓴다.

## 표(`conversations.jsonl`)의 칸

줄 = 대화 `{conv, title, turns[]}` · 턴 = `{n, text, tags{intent[], form, data[]}, key{…}, ambiguous, basis[], shown?}`

| 칸 | 뜻 |
|---|---|
| `key.targets[[…]]` | 기대 대상 — 바깥 = 묶음(전부 맞혀야) · 안 = 어느 것이든 |
| `key.extras_ok[]` | 함께 나와도 군더더기로 안 세는 것 |
| `key.kind[]` | 받는 턴 종류(new / follow / talk) |
| `key.site_filter[]` · `site_required` | 이번 턴 부위 · 꼭 걸려야 하나 |
| `key.withdraw[[…]]` | 거둬져야 하는 것 |
| `key.ask_option` | 앞 턴에 앱이 준 되물음의 n 번째 선택지 — 실행 기록의 `consult.ask.options` 로 푼다(안 물었으면 채점 밖) |
| `key.kinds[]` · `kinds_ok[]` | 기대 정보 종류 · 함께 나와도 받는 종류 — 앱 `clinic_chat/walk/kinds.py` `KIND_CODES` 14 그대로(없는 턴 = 정보 종류를 채점하지 않음) |
| `key.ref{to, how}` | 이번 말이 가리키는 것 — `to` = `list`(보여 준 리스트) · `answer`(앞 답) |
| `shown{answer_summary, list[]}` | **이 턴 뒤에** 상담사가 한 답의 요약 · 화면에 보여 준 리스트 — 표에 적어 둔 가짜 앞 답이다(리스트 = gold `g_indication` 에서 그 고민에 닿는 시술 gid 순 앞 넷 · 값 = `g_offer` 행). 다음 턴의 `key.ref` 정답은 이것 기준 |
| `ambiguous` | 정답을 못 박을 근거가 없는 턴의 까닭 — 채점 밖 |
| `key.material{rows[[…]], depth[]}` | **재료 정답 키**(11-18 SPEC-008 E8-6b · C74~C78 의 22 턴에만). `rows` = 그 턴 재료(답 LLM 에 가는 「자료」 줄 = 장부 `material.new_lines[].gid` ∪ `material.seen_lines` 번호가 가리키는 앞 턴 줄의 gid)에 꼭 있어야 하는 gold 행 gid — 바깥 = 묶음(전부) · 안 = 어느 것이든. `depth` = 깊이 읽기(`trace.depth.decisions` 의 `gate_forced`)를 해야 하는 노드 `table:code` — `[]` = 깊이 읽기 0 기대. 검사: ⓐ `rows` 묶음이 전부 재료에 있다 ⓑ 깊이 읽은 노드 ⊆ `depth` ⓒ `depth` 가운데 그 턴 깊이 후보로 선 것은 전부 깊이 읽음. 근거 = `basis` 의 「재료 — <gid> <gold 표> …」 · 「깊이 — …」 줄(`build.py` 가 gold 행에서 적는다 · 없는 gid 는 `bad`) |

가리키는 말(`key.ref`) 턴을 재는 두 길:
1. **입구만 잴 때**(후보 뽑기 호출을 따로 부를 때) — 앞 턴의 `shown` 을 대화 맥락에 그대로 실어 준다(`pick.py` 가 그렇게 한다).
2. **앱 전체로 잴 때**(`run_now.py`) — 답 LLM 이 빈 답이라 앞 답 요약이 없고, 리스트는 앱이 실제로 낸 것이다. `score.py` 는 `ref.to` = `list` 인 턴을 앱 리스트의 앞머리가 `shown.list` 와 같을 때만 채점하고 다르면 채점 밖으로 둔다. `ref.to` = `answer` 인 턴은 그대로 채점한다 — **앞 답이 빈 글이면 풀 수 없는 턴이므로**, 이 턴들을 재려면 `run_now.py` 의 가짜 답 자리에 `shown.answer_summary` 를 내도록 바꾸거나 답 LLM 을 실제로 불러야 한다(코디 몫 — 어느 쪽으로 할지는 정하지 않았다).

## 8 검사(앱 전체) · 3 검사(입구)

채점 대상 = 애매(`ambiguous`)도 아니고 채점 밖(되물음이 없었음 · 리스트가 다름)도 아닌 턴.

| # | 검사 | 통과 조건 | 3 검사 |
|---|---|---|---|
| 1 | 대상 `target` | 확정 대상이 묶음을 전부 맞히고 군더더기가 없다. 다섯 표(고민 · 부위 · 계열 · 시술 · 제품)만 센다 · 앞 턴에 정답이었던 대상을 다시 든 것(D-12) · 고른 고민의 `concern_site` 부위 · `extras_ok` 는 군더더기가 아니다 · 객체에서 거둔 것은 뺀다 | ✓ |
| 2 | 턴 종류 `kind` | 판정한 종류가 `key.kind` 안에 있다 | ✓ |
| 3 | 부위 거르개 `site` | 이번 턴에 고민 · 부위가 있는 턴만 본다. 거르개에 이번 턴 부위(+ 고른 고민의 부위) 밖의 것이 없고, `site_required` 면 이번 턴 부위가 걸려 있다 | ✓ |
| 4 | 객체 `obj` | 맞힌 대상이 객체 축(said · confirmed)에 들었고 · focus 가 이번 턴 고민이고 · 거둘 것이 거둬졌다 | |
| 5 | 점 `dots` | 화면의 점 · 라벨 부위 = 지금까지 말한 고민(고른 것)의 `concern_site` 직접 부위(더도 덜도 없음) — 그 대화에서 고민을 전부 맞혔을 때만 본다 | |
| 6 | 선택지 `options` | 부위만 말한 턴(고민 없음)에 그 부위에 묶인 고민이 gold 에 있으면 되물음 선택지가 1 개 이상 | |
| 7 | 거르개 효과 `site_effect` | `site_required` 턴에서 허브 응답이 「우선 표시 · 표지 0 행」 으로 풀리지 않았다 | |
| 8 | 리스트 `list` | 이번 턴 고민이 focus 이고 리스트를 보냈으면 시술이 1 개 이상(내려온 시술 포함) | |

- **8 검사 통과**(`summary.json` `now.counts.pass` · `pass8_pct`) = 여덟 가운데 해당하는 것을 전부 통과한 턴. 못 통과한 턴은 첫 실패(위 순서)로 층(후보 · Jev · 앱 규칙 · 데이터)을 붙인다 — 층 이름과 까닭 글은 옛 흐름(resolve · Jev)에 맞춰 있으므로 새 흐름에서는 `now-turns.jsonl` 의 `checks` 를 본다.
- **3 검사 통과**(`…all.pass3` · `pass3_pct`) = 1 · 2 · 3 을 전부 통과(3 은 해당 없으면 통과로 침). `conv_pass3` = 채점 턴이 전부 3 검사를 통과한 대화 수.
- **정보 종류**(8 검사 밖 · `kinds` / `kinds_has` / `kinds_n`) = `key.kinds` 가 있는 턴만. `kinds_has` = 기대 종류를 전부 냈다 · `kinds` = 거기에 더해 낸 것이 `kinds ∪ kinds_ok` 안. 지금 앱의 `kinds` 는 「읽은 종류」(기본 묶음이 섞임)라 `kinds_has` 로 본다.
- 완료 기준(D-14): 앱 전체 8 검사 90%↑ + 입구 3 검사 95%↑.

## 채점이 앱 장부에서 읽는 칸

`slim.py` 가 남기는 것 그대로다 — 새 흐름이 이 칸의 꼴을 바꾸면 `score.py` `now_turn` 을 맞춰야 한다.

| 검사 | 읽는 칸(맺는 줄) |
|---|---|
| 대상 | `targets[]{table, code, by}` · 거둔 것 = `consult.after.{concerns,sites,subjects}[].state == "withdrawn"` |
| 턴 종류 | `consult.turn_kind.kind` |
| 부위 거르개 | `consult.after.sites[]`(said · confirmed · `source.pair_concern` 이 없거나 focus) — 옛 `filter_sites` 와 같은 식. **「이번 턴 부위만」 으로 바뀌면 여기를 새 거르개 칸으로 바꾼다** |
| 객체 | `consult.after`(`concerns` · `sites` · `subjects` · `focus`) · `consult.retract[]` |
| 점 | `sites{dots[], labels[]}`(안 보낸 턴은 앞 값) |
| 선택지 | `consult.ask.options[]` · `consult.queries[]`(QY7 total) · `consult.ask_why` |
| 거르개 효과 · 리스트 | `list.concerns[]{site{applied, prefer_rows}, modalities[].procedures[], descended[].procedures[]}` |
| 정보 종류 | `kinds[]` |
| 재료 · 깊이(C74~C78 · 채점기 아직 없음) | 재료 줄의 gid(`material.new_lines[].gid` · `material.seen_lines` — `slim.py` 가 아직 안 남긴다) · `trace.depth.decisions` — 0.4 장부 칸에 맞출 때 같이 더한다(SPEC-008 E8-pre) |
| 층 가르기(옛 흐름) | `trace.front.targets[]{id, noul, decision}` · `trace.entry.resolve_candidates[]` · `trace.entry_pick` |
