# 검수 — 앱 상담 0.4 코드(WORK-017 · SPEC-008 0.2.0 · 소넷 입구)

**판정: WARN** — 계약 줄(LD · UC · VF · OU · QS · QM · DT · BQ · FL · 장부 · SSE · 적재기)은 코드와 맞는다. 켠 경로에서 Jev · `resolve(text)` · `walk()` · `front()` 를 부르는 곳은 0 이다. `walk/` 는 더한 줄만 있고 `columns/` 는 diff 0 이다. 실물 두 대화도 §2 대로 돈다. 다만 아래 셋은 **마감 전에 고칠 코드 · 시험**이다.

- **C-1** 답 LLM 「앱 판정」 에서 `synergy_lines` 가 빠졌다. 주석이 키를 삼켰다 — 0.3 회귀.
- **C-2** 대상이 아닌 고민의 점이 빠진다. 메모와 걷기 읽기가 어긋나서다. E8 실패 2 턴이 이 몫이다.
- **C-3** WORK 가 「안 고침」 으로 적은 시험 파일 셋에서 9 개가 떨어진다. 시너지 · 끝맺음 · 리스트를 켠 경로로 보는 시험이 0.4 에서 하나도 없어졌다.

문턱 미달(3 검사 93.8 · 8 검사 86.9)의 실패 44 턴은 장부로 다시 갈랐다. 코드로 고칠 몫은 2 ~ 3 턴이다. **측정 몫이 9 턴**이다 — 답 LLM 을 실제로 부른 다섯 대화의 키가 표의 가짜 앞 답 기준이다. 나머지는 프롬프트 몫이다.

검수 범위: 앱 워크트리 `clinic_chat/phub-gold-jev`(HEAD `be1c622` + 미커밋 변경 32 파일 · 새 파일 20) · SPEC-008 0.2.0 · WORK-017 · `impl-chat-v04-instructions.md` · `review-work-016-017.md` R-2 ~ R-5 · `_RESUME` §2 11-18 · `research-input-space/scripts/README.md` · `runs/v04-score` · `runs/v04b-score` · `runs/v04b-rows.jsonl` · `runs/v04b/turns.jsonl`. 아무 파일도 고치지 않았다. stash · checkout 을 하지 않았다. 18222 · 18105 를 띄우거나 내리지 않았다.

## 지적 표

| # | 파일:줄 | 심각도 | SPEC 절 | 무엇 | 고칠 방향 |
|---|---|---|---|---|---|
| C-1 | `clinic_chat/consult/turn.py:556` | **Medium** | AN1 · CP5(답 = 0.3 그대로) · SPEC-005 §7 SY4 | `extra = {"turn_kind": …, "ask": self.ask_view,  # AN1 — 검증 뒤 \`kind\` "synergy_lines": self.syn_lines,` — 덧붙인 주석이 `"synergy_lines"` 키를 삼켰다(`git diff` 에서 그 줄 하나만 바뀜). `new` · `follow` 턴의 「앱 판정」 JSON 에 `synergy_lines` 가 없다. 시너지 요약 줄은 자료에 그대로 실리지만, 답 LLM 이 그 줄 번호를 「앱 판정」 으로 받지 못한다. `talk` 갈래(`:553`)는 멀쩡하다. 이 자리를 보는 시험(`test_state_synergy.py:48` `j["synergy_lines"] == …`)은 C-3 때문에 돌지 않아 못 잡았다 | 주석을 줄 끝으로 옮기고 키를 되살린다. `test_v04_*` 에 켠 턴 「앱 판정」 의 `synergy_lines` 단언 하나(C-3 과 같이) |
| C-2 | `clinic_chat/consult/plan.py:223` ↔ `:277`(`derive` 의 `else`) | **Medium** | DT1 · SPEC-006 FD1(점 = 말한 고민 전부 · 누적) · E8 검사 5 | `run` 은 대상이 아닌 축 고민의 `concern_candidates` 가 **걷기 읽기**(`reader.walk`)에 있으면 `qy1_plain` 을 건너뛴다(`:223` — `extra` 로 `reader.walk.values()` 를 넘김). 그런데 `derive` 는 `cc_reads_of(code, memo)` 를 **메모만**으로 본다(`:275` · `:277` — `extra` 없음). `Reader.get` 을 거치지 않은 걷기 읽기는 메모에 없다. 그래서 그 고민의 직접 부위 점이 빠진다. 0.4 에서는 `targets` 의 부위가 늘 재료 입구라(QM1) 걷기가 「고민 × 부위」 꼴 `concern_candidates` 를 자주 읽는다. 그래서 더 자주 걸린다. **장부 확인**: C59-1(focus `CON-024` · `CON-005` 이마주름은 걷기 QY5 읽기만 있고 QY1 0 → 점 `SITE-014` 빠짐) · C61-1(`CON-164` 이중턱 → `SITE-077` 빠짐). 두 턴 다 이해 출력은 맞았다. 0.3 HEAD 에도 같은 꼴이 있다(`HEAD:plan.py:208` ↔ `:259`) — 0.4 가 새로 낸 결함은 아니지만 0.4 에서 E8 실패로 드러났다 | `derive` 가 걷기 읽기도 본다(`run` 이 `reader.walk.values()` 를 `derive` 에 넘겨 `cc_reads_of(…, extra=…)`). 아니면 `:223` 에서 걷기 읽기를 메모에 옮겨 담는다. 시험 = 고민 둘 + 부위 둘 첫 턴에서 대상이 아닌 고민의 직접 부위가 점에 있다 |
| C-3 | `tests/test_state_synergy.py`(4 실패) · `tests/test_v03_close.py`(3) · `tests/test_v03_list.py`(2) | **Medium** | WORK §15-4 「안 고침」 줄(「깨지면 고치지 말고 보고」) · S8-T18 · QS5 · CP5 | WORK §15-4 는 이 세 파일을 「고치지 않은 채 통과」 쪽에 두었다. 그런데 셋 다 `Run(…, noul=jev(…))` 로 **가짜 Jev 를 입구로** 켠 턴을 돈다. 0.4 에서는 이해 가짜 출력이 없어 대상이 0 이 되고 기대가 깨진다(`KeyError: '가짜계열'` · `row["list"]` = `None` · 끝맺음 단언). 구현 보고에 이 9 개가 없다 — 세 파일이 어느 WP 의 「돌릴 파일」 에도 없어 아무도 돌리지 않았다. 결과로 **시너지(SPEC-005 §7) · 끝맺음 블록(S6-T10 · T11) · 턴 리스트 조각(S6-T15 · SP)을 켠 0.4 경로로 보는 시험이 0** 이다(`test_v04_*` 57 개 가운데 시너지 단언 0). C-1 이 그 빈 곳으로 빠져나갔다 | 세 파일의 픽스처를 가짜 이해 출력(`understand.json`)으로 바꾼다(기대값은 그대로 — 뜻이 0.4 에도 있다 · QS5 · CP5). 바꾼 수 · 이름을 보고한다. §15-4 「안 고침」 줄의 셈을 되적는다 |
| M-1 | `research-input-space/conversations.jsonl`(C57 · C58 · C65 · C69 의 키) · WP-12 채점 | **Medium(측정)** | §8-1 「앞 답을 가리키는 턴」 · E8-5 | **답 LLM 을 실제로 부른 다섯 대화의 키가 표의 가짜 앞 답(`shown.answer_summary`) 기준이다.** 실물 답은 다른 것을 말했고, 소넷은 실물 답을 맞게 따랐다. 예: C57-1 실물 답 = 「레이저 계열 … 메디컬스킨케어 계열」 → C57-2 「뒤에 거요」 = `M15` 메디컬스킨케어(소넷)인데, 키 = `PRC-006` IPL. C65-2 실물 답 = 「PLLA 와 무세포동종진피」 → C65-4 「뒤에 거」 = `PRC-108`(소넷)인데, 키 = PN주사. C69-1 실물 답의 기계 쪽 = 기기 리프팅 → `M9`(소넷 · 키 `extras_ok` 에만 있음)인데, 키 = HIFU. C58-2 실물 답 = 「가격은 안내할 내용 없어요」 → C58-3 「그 중에 제일 싼 거요」 는 가리킬 것이 없다. 이 판의 실패 44 가운데 **9 턴**(C57-2 · 3 · C58-3 · 4 · 5 · C65-3 · 4 · C69-2 · 3 — 앞 여섯은 분명하다 · C58 셋은 「답에 값 없음」 의 이어짐이다)이 이 꼴이다 | 앞 답을 실제로 부르는 대화는 ⓐ 실행 뒤 그 판의 실물 답으로 키를 다시 매기거나(E8-5 사람 검수 몫) ⓑ `ref.to=answer` 턴의 채점을 「실물 답이 그 대상을 말했을 때만」 으로 가른다(`list` 의 「앞머리 같을 때만」 과 같은 꼴). 코디 · 사용자가 고른다 |
| L-1 | `clinic_chat/consult/turn.py:157` · `material_read.py:89-90` | Low | OU8 · QM3 · TT2 | 「WORK 와 달리 받은 것 — 거둠만 있는 `new` 턴은 화면 안 갱신」. 소넷이 「스킨부스터는 빼 주세요」 를 `new` + `targets []` + `withdraw [x]` 로 내면 QM3 「입구 없음」(NO_B_ON)으로 간다. 그래서 `list` · `sites` 를 다시 보내지 않고, 거둔 항목이 다음 턴까지 화면에 남는다. 계약(W-6 「다음 턴이 따라잡는다」)과 부딪히지는 않는다. 손님 눈에는 「뺐는데 그대로」 다 | 검증에서 `targets == [] and withdraw` 인 `new` 를 `talk` 갈래(객체가 바뀌면 조회 · 리스트 — TT2)로 읽는다(`kind_from = "withdraw_only"`). 사용자 확인 대상으로 되적기 |
| L-2 | `prompts/consult.json` `pick.headers` · `consult/prompt.py:39` `PICK_HEADER_EXTRA` | Low | §7 · R-5(코디 답) · WORK B-4 | 코디가 정한 글자는 「앞 답 요약:」 · 「보여 준 리스트:」 · 「(앞과 같음)」 셋이다. 구현은 머리 글자 **여섯을 더 지었다**: `picked` 「→ 고른 대상:」(UC6 글자) · `options` 「상담사가 물은 선택지:」 · `obj_targets` 「대상:」 · `obj_guess` 「애매:」 · `obj_withdrawn` 「거둔 것:」 · `user` 「손님:」. 셋 다 손님에게 안 보이는 글이다. 다만 `pick` 은 사용자 확인 대상이고, 이 여섯이 **없으면 `pick` = `None` → 켠 대화 시작 불가**(적재기 필수 키)다 | 사용자 확인 목록에 여섯을 더한다(`pick.version` `-draft` 그대로). SPEC §7 적재기 계약 표에 `headers` 의 필수 키 전부를 되적는다 |
| L-3 | `clinic_chat/consult/entry_list.py:86-91` | Low | LD5 | 대화의 첫 턴(`Conv.gold_hash` 비어 있음)은 프로세스가 **마지막으로 받은 목록**(`_LAST`)을 그대로 쓴다. 허브 gold 가 바뀐 뒤(같은 서버 프로세스)의 새 대화는 첫 턴을 옛 목록으로 뽑는다. 둘째 턴부터는 대화 `gold_hash` 가 새 값이라 다시 받는다. 독스트링은 「`build_changed` 로 닫힌다」 고 하지만, 첫 턴 조회의 `build` 로 `Conv.gold_hash` 가 정해지므로 닫히지 않을 수 있다 | 첫 턴에는 허브 머리(`health` 또는 목록 첫 쪽의 `build.gold_hash`)로 판을 확인한다. 아니면 첫 턴 `build` 와 목록 `gold_hash` 가 다르면 그 턴을 `build_changed` 로 닫는다 |
| L-4 | `clinic_chat/consult/site_index.py:57-58` | Low | QS6 · O8-1 | 고민 하나라도 조회가 실패하면(`errors`) 색인을 캐시하지 않는다. 그 뒤 **QY7 이 서는 턴마다 `concern_candidates` 260 번**을 다시 부른다(지연 · 허브 부하). 장부 `site_index` 는 지은 턴에만 실려 되풀이가 드러나지 않는다 | 실패 고민만 빼고 캐시하고 `errors` 를 남긴다. 아니면 실패 뒤 한 번만 다시 짓는다 |
| L-5 | `clinic_chat/consult/turn.py:419-420`(`qy7_new`) | Low | BQ4 · E8 검사 6 | `qy7_new` 는 「`acc.targets` 가 전부 `site`」 일 때만 참이다. 소넷이 부위 + **애매한 고민**(`sure=false` → `guess` — 축이 아님 · `focus` 없음 · QY7 은 섬)을 내면 BQ4 가 빠져 NQ5 로 되묻지 않는다. C46-2 「다리에도 있어요」(`SITE-102` + `CON-126` guess) → 조회 39 행 · `ask` 없음 · 검사 6 실패 | 「대상이 부위뿐」 을 **축 항목 기준**으로 센다(`guess` 는 빼고 — RV1). 1 턴 |
| L-6 | 실물 18222 대화 B · `blanks` 우선순위(0.3 그대로) | Low(관찰) | BQ2 · D-9 | 「얼굴이 자꾸 빨개져요」 → 소넷 `CON-125` 안면홍조 `sure=false` + `SITE-007` 얼굴. 객체 = 고민 `guess` · 부위 `said`. 그래서 `ask` = QY7(「얼굴」 의 고민 선택지 — 얼굴 처짐 · 얼굴 위축 · **안면홍조(셋째)** …)이고 BK5(추정 확인)가 아니다. 답은 「붉어짐이 맞을까요, 아니면 얼굴 처짐 …」 으로 섞어 묻는다. 계약 위반은 아니다(NQ2 순위는 SPEC-005 그대로). 다만 D-9 「애매 = 한 번 확인」 의 뜻과는 갈린다 | 프롬프트 몫(규칙 10 의 `sure` 기준)과 함께 본다. 코드로는 QY7 선택지에 이번 턴 `guess` 고민을 맨 앞에 두는 길이 있다(사용자 확인) |
| L-7 | 프로필 레포 `research-input-space/`(통째로 미추적) · `scripts/README.md:25` | Low | 공개 레포 | ⓐ README 25 행에 `A=/Users/…/clinic_chat/phub-gold-jev` — 홈 절대 경로 ⓑ `runs/v04/turns.jsonl` 36MB · `runs/v04b/turns.jsonl` 35MB 원 장부가 gitignore 밖이다(README 「커밋 전에 slim 으로 줄이고 원본은 지운다」). 원 장부 안 `/Users/` 0 · 키 꼴 0(이 검수 grep) | 커밋 때(코디): README 경로를 `$A`(설명만)로 · 원 장부 둘은 빼거나 지운다 |
| L-8 | `_RESUME` · 구현 보고 「소넷 비결정 ±3.5%」 | Low(근거) | E8-3 · E8-4 | v04 ↔ v04b 의 같은 턴을 견주니 갈린 턴 24(v04 만 실패 12 · v04b 만 실패 12 · 순 0)다. 한쪽 12/336 = 3.6% 라 수는 맞다. 다만 두 판 사이에 **리스트 번호 고침이 끼어 있다**(`understand._list_text`). v04 만 실패 12 가운데 C56-2 ~ 5(4 턴)는 그 고침의 몫일 수 있다. 같은 코드로 두 번 잰 비결정 수가 아니다 | 같은 코드로 한 번 더 돌린 판(v04c)과 v04b 를 견줘 비결정 폭을 따로 잰다. 문턱 판정 차이(3 검사 = 4 턴 · 8 검사 = 11 턴)보다 큰지 보고한다 |

## 볼 것별 결과

### 1. 범위 · 경로 나눔(S8-T18)

- `git diff --stat -- clinic_chat/columns prompts/jev clinic_chat/llm clinic_chat/web clinic_chat/clients` = **비어 있음**.
- `git diff -- clinic_chat/walk | grep -c '^-[^-]'` = **0**. `walk/front.py` 에 감쌈 셋(`coverage_of_nodes` · `ranges_for` · `kind_rows`)이 있고, 본문은 다 감싼 함수를 부르는 한 줄이다. `kind_rows` 는 SPEC §3-4 「`_kind_rows` 를 쓰면 공개 감쌈」 대로다.
- 켠 경로 grep(WORK §4 명령 + `value_pick|walk_depth|front\(`): 남는 줄 = 끈 가지(`turn.py:118-119`) · 머리 독스트링(`turn.py:3`) · `d.jev` 시간 읽기(`turn.py:94` · `:210` — 끈 가지 `timing` 몫) · `prompt.py` 적재 · `e6.py`(B-8) · `carry.py` 주석. `rg filter_sites clinic_chat/` = 0.
- 켠 턴의 Jev 0 · `resolve(text)` 0 은 시험이 기계로 본다(`test_v04_turn.py:25` · `:61` — `r.fj.requests == []` · `hub.requests` 에 `text` 있는 `resolve` 0).
- 시험 앱 B 열 동작 불변: `columns/` · `walk/` 기존 줄 diff 0 이다. `test_columns.py` · `test_walk_*.py` 다섯이 통과한다(아래 4).
- 새 파일 = `consult/` 8(`e8` · `entry_list` · `kinds_pick` · `material_read` · `site_filter` · `site_index` · `understand` · `verify`) · 시험 12(`test_v04_*` 11 + `v04_fixture`) — B-1 이름 그대로.

### 2. SPEC-008 0.2.0 대조

| 절 | 코드 | 판정 |
|---|---|---|
| LD1 ~ LD8 | `entry_list.py` — 목록 꼴 `read_all("resolve", {"tables": 다섯})` · `complete` 아니면 `EntryListError`(LD7) · 개념 = (표, 코드) · 별칭 = 다른 행 `text`(같은 글자 한 번 · 행 순) · 머리 `## 고민 (table = concern)` · 허브 순서 · `aliases=False` 면 괄호 없음 · sha256 · 다섯 표 밖 버림 | 맞음. 첫 턴 캐시 = L-3 |
| UC1 ~ UC10 | `understand.py` — `-p` · `--model` · `--effort` · `--max-turns 1` · `--output-format json` · `--no-session-persistence` · `--resume`/`--session-id`/`--fallback-model` 없음 · 격리 인자 = `llm/cli.py` `DISALLOWED_TOOLS` · `OFF_SETTINGS` import(두 벌 아님) · stdin · 답 실행기 cwd · 시간 한도 · 재시도 0 | 맞음. thinking 은 E8-0 대로 완전히 못 끈다(실물 대화 A 두 턴 `thinking_tokens` 238 · 236 — D-4 「배포 전 SDK」 로 받음) |
| UC6 · UC7 · FL4 | `turn_message` — 성공 턴 전부 · 가까운 `context_turns` 에만 답 앞 200 자 · 리스트 이름(번호 = 손님이 세는 항목만 · 계열은 번호 없는 머리) · 안 바뀌면 `(앞과 같음)` · 실패 턴 `(이해 실패)` · 객체 세 줄 | 맞음. 계열 머리에 번호를 달지 않는 것은 E8 고침이다 — 규칙 9 「리스트의 그 줄」 의 뜻 안. 머리 글자 = L-2 |
| VF1 ~ VF12 | `verify.py` | 맞음. **VF11 을 VF6 앞에**(「받은 것」) 둔 것은 계약과 부딪히지 않는다. VF11 은 `talk` → `new` 를 고칠 뿐이고, VF6 뒤에 두면 대상을 버린 뒤 `new` 가 되어 「입구 없음」 으로 떨어진다. 앞에 두는 것이 VF11 의 뜻이다. `dup` · `bad_shape` · `not_in_gold` · `talk` · `withdraw` 의 `why` · `added_from_sites` · `merged` 가 장부에 있다 |
| OU1 ~ OU12 | `state.observe_accepted` · `update` · `_pair` · `_focus` · `turn._apply` · `_viewing` | 맞음. `focus` = `targets` 순서 마지막 `said`(`guess` 뺌 · 다시 정렬 없음). `pair_concern` = 이름 같은 부위. R-4 `viewing` `source{how: view, sure: null}`(`turn.py:451`) |
| OU7 · VF8 ⓒ · QS3 | `site_filter.decide` — 넷 조건 · 앞 **성공** 턴(`prev_ok` — 실패 턴 건너뜀) · `about` ∈ 그 부위 · `pair_kept`/`pair_dropped` | 맞음(S8-T7 · T8 시험 있음) |
| QS1 ~ QS6 | `plan.list_calls` · `qy1_calls(site_names)` · `run(site_options)` · `site_index` | 맞음. QS4 의 「앞 리스트」 = `Conv.list_calls`(메모리만) — 서버를 다시 띄우면 첫 턴은 새로 조회한다(뜻 안). 색인 실패 = L-4 |
| QM1 ~ QM5 · KS · DP8 · VP8 · §3-4 | `material_read.build_walk` — `col_b.walk()` 와 같은 차례에서 `front()` · `value_pick` · `walk_depth` · `offer_picks` 를 뺐다. DP8 = 이번 턴 대상이면 `gate_forced` · 걸음 한 번 · 새 후보는 결정만. `kinds_pick` 은 `_decide_kinds` 와 KS2 · KS4 · KS7(kv 문턱 없음) · KS8 만 갈린다 | 맞음. ⓐ 「`offer_name` 길 없음」(「받은 것」): EN1 의 상품 이름 입구는 resolve 맞춤 꼴의 몫이었다. LD8(목록 = 다섯 표)이라 계약과 부딪히지 않는다. 상품(`g_offer`)은 `offer` 종류 재료로만 온다 ⓑ `kinds_pick.STRONG_BY` 에 `kd9` 가 있다 — SPEC KS7 본문은 「`yes` · `entry`」 만 적었다. 0.3 `STRONG_BY`(kd9 포함)에 더 가깝다 → SPEC 되적기 후보 |
| DT1 ~ DT5 | `sites.site_pairs` `match ∈ (None, 직접)` · `plan.derive` 고민마다 `match` | 맞음. 비축 고민 점 빠짐 = **C-2** |
| BQ1 ~ BQ5 | `blanks.pick(qy7_new)` | 맞음. `qy7_new` 범위 = L-5 |
| FL1 ~ FL6 | 목록 · CLI · 시간 · JSON 실패 → 빈 `Walk`(입구 없음) · `_apply` 안 함(diff `[]`) · 조회 0(terminal → `derive` 만) · `list` · `sites` 안 보냄(NO_B_ON) · 답은 나감 · 재시도 0 | 맞음(S8-T15 시험) |
| 장부 §6-1 | `understand_view` · `site_filter` · `site_index`(지은 턴만) · `turn_kind{kind, from}` · 턴 줄 `targets{table, code, name, sure, how}` · `trace` 에서 `entry` · `entry_pick` · `steps` · `depth_decisions` 지움 + `trace.depth{decisions, read}` · `timing.parts{understand_ms, hub_ms, llm_ms, material_ms}` · `CONSULT_REV = 4` | 맞음. 실물 장부에 `nouls` · `retract` · `entry_pick` 0 |
| SSE §6-3 · 패널 §6-2 | 이벤트 이름 그대로 · 실물 SSE = `step` · `list` · `sites` · `delta` · `state` · `done` · `close` · 패널 조각에 `understand` · `site_filter` · `accepted` · `dropped` · `merged` · `turn_kind` 있음 · `nouls` · `jev_requests` 0 | 맞음 |
| CP1 · CP7 · 설정 | `config.chat_state = "on"` · `state_at_start` 새 대화 = 늘 `on` · `blocked` 옛 끈 대화 = `rev_changed` · `conv-off-closed` 빈 `data-slot`(`main.html`) · 설정 아홉 | 맞음 |
| 적재기 §7 | `_pick` — 하나라도 비면 `None` · `state_ready` = `pick` 기준(`retract` · `target_option` · `turn_kind` 안 봄) · `draft` = 최상위 `version` · `KEYS` 그대로 | 맞음. `rules[]` 에 SPEC 초안의 빈 줄 셋이 없다(적재기가 빈 줄을 막으므로 맞다 — 글자는 같다). 필수 머리 열하나 = L-2 |
| 「받은 것」 ① 가짜 CLI 이해 길 조건 | `tests/fake_cli/fake_cli.py` | 시험 도구 몫 — 계약 밖 |
| 「받은 것」 ⑤ `site_index` 캐시 키 (`gold_hash`, 목록 sha) | `site_index.py:53` | LD5 와 같은 뜻 · 더 엄하다 — 맞음 |

### 3. 실패 44 턴 — 장부로 직접(표본 22 · v04b)

`runs/v04b-score/now-turns.jsonl` 의 첫 실패 검사 = 대상 18 · 객체 13 · 점 5 · 거르개 효과 3 · 턴 종류 2 · 리스트 1 · 부위 1 · 선택지 1. `runs/v04b-rows.jsonl` 의 `consult.understand.parsed` · `accepted` · `site_filter` · `ask` · `queries` 와 키를 턴마다 견줬다.

| 무리 | 턴(본 것) | 장부가 보인 것 | 층 |
|---|---|---|---|
| 객체 13 | C16-1 · C19-1 · C44-1 · C46-1 · C52-1 · C55-2 · C11-2 · C09-3 · C31-1 · C32-2 · C51-3 · C61-3(+ C32-3) | 맞는 코드를 골랐는데 `sure=false` → `guess`(축 아님). 「광대 쪽이 처졌어요」 → `CON-041` 광대뼈 처짐 · 「쥬비덤 볼류마요」 → `PRD-050` 도 `false` 다. 코드는 D-9 · OU2 대로 했다. 「구현 보고 = `sure=false` → `guess`」 는 맞다 | **프롬프트**(규칙 10 의 `sure` 기준) · 채점(D-9 는 `guess` + 확인이 뜻 — 검사 4 는 축만 센다) |
| 점 5 | C59-1 · C61-1 | 이해 출력은 맞았다. 대상이 아닌 고민의 점이 빠졌다 | **코드(C-2)** |
| | C19-2 · C44-2 · C44-3 | 앞 턴 고민이 `guess` 라 점 재료가 없다(위 객체 무리의 이어짐) | 프롬프트(이어짐) |
| 대상 18 | C57-2 · 3 · C58-3 · 4 · 5 · C65-3 · 4 · C69-2 · 3 | 소넷이 **실물 앞 답**을 따라 맞게 골랐다. 키는 표의 가짜 앞 답 기준이다 | **측정(M-1)** |
| | C23-5 · C50-1 · C50-3 · C57-4 · C67-4 · C77-4 · C41-2 · C41-3 · C75-3 | C50-1 「턱 필러」 → `PRC-100` 히알루론산 필러(키 = 계열 `M2`) · C77-4 「써마지FLX」 → `PRD-416` 써마지(`sure=false` · 키 `PRD-417`) · C41-2 「세 번째요」 → `CON-038` 지어 붙임(키 `[]`) · C23-5 「세 군데」 → 고민 셋(키 = 보톡스) | 프롬프트 |
| 턴 종류 2 | C03-2 · C06-4 | 「지방분해 주사는 어때요?」 를 `follow` 로(키 `new`) | 프롬프트 |
| 부위 1 | C38-4 | `CON-001` 주름을 고름 → `site_required` 에서 떨어짐(SPEC §8-1 이 이름 박아 둔 갈리는 턴) | 측정(E8-5 키) |
| 선택지 1 | C46-2 | 부위 + `guess` 고민 → BQ4 빠짐 | **코드(L-5)** · 프롬프트(guess) |
| 데이터 4 | C08-2 · C15-2 · C28-2 · C44-5 | 고민 행 0 · 거르개 0 행 → 우선 표시로 풀림 | 데이터(D-13 — 90 안의 몫) |

- **코드 결함이 섞였나**: 섞였다 — C-2 두 턴(C59-1 · C61-1) · L-5 한 턴(C46-2). 나머지 41 턴은 코드가 계약대로 했다. 「이해 21 · 객체 13 · 조회 6 · 데이터 4」 의 「조회 6」 에는 코드 결함 2 · `guess` 이어짐 3 · BQ4 1 이 섞여 있다.
- **「소넷 비결정 ±3.5%」**: v04 ↔ v04b 같은 턴 견줌 = 갈린 턴 24(v04 만 실패 12 · v04b 만 실패 12). v04b 만 실패 12 는 C03-2 · C06-4 · C09-3 · C19-1 · C19-2 · C23-5 · C32-3 · C41-3 · C46-2 · C52-1 · C55-2 · C77-4 다. 다 소넷 출력이 갈린 턴이고(`sure` · `kind` · 대상), 코드가 같은 입력에 달리 한 턴은 없다. v04 만 실패 12 는 C02-2 · C08-3 · C18-2 · C29-2 · C29-5 · C40-2 · C54-2 · C56-2 ~ 5 · C61-2 다. 이 가운데 C56 넷은 그 사이 고친 리스트 번호의 몫일 수 있다 → 수는 맞지만 근거가 깨끗하지 않다(L-8).

### 4. 시험

돌린 파일(외부 호출 0 — 가짜 CLI · 가짜 허브 · 전체 pytest 아님):

| 묶음 | 파일 | 결과 |
|---|---|---|
| WP 「돌릴 파일」 전부(32) | `test_v04_*` 11 · `test_columns` · `test_walk_core` · `test_walk_front` · `test_walk_material` · `test_consult_{carry,ledger,page,prompt,sites,turn}` · `test_state_{blanks,carry,examples,list,object,plan}` · `test_v03_{fixes,frame,prompt,sites,start,turn_kind}` | **248 passed · 1 skipped** |
| §15-4 「안 고침」 줄 | `test_walk_entry` · `test_walk_ranges` · `test_v03_shared` · `test_v03_e6` · `test_consult_listing` · `test_consult_material` · `test_consult_chat_ui` · `test_consult_cli` | 통과 |
| | `test_state_synergy` | **4 failed**(s5_t11 · focus_change · s5_t21 · synergy_off) |
| | `test_v03_close` | **3 failed**(s6_t11 둘 · s6_t10) |
| | `test_v03_list` | **2 failed**(s6_t15 · sp_turn_site_view) |

- 지운 시험 = `git diff tests/` 의 `-def test_` **20** — §15-4 예상(turn_kind 13 · carry 5 · consult_turn 1 · examples 1)과 같은 수다. 넷 다 Jev 판정 · 든 후보 · 입구 고르기 · 거둠 요청 · 끈 대화 0.1 동작을 보던 것이다(X-8 ~ X-12 · X-23 · CP1) → 계약 변경 몫이다.
- R-2 끈 대화 시험 넷은 「옛 끈 대화 = 열기만 · 턴 막힘」 으로 고쳐 통과한다(`test_v03_prompt` · `test_v03_frame` · `test_state_blanks`).
- S8-T1 ~ T20 은 모두 시험 이름 · 주석으로 찾아진다. 기대값은 계약 글에서 온다(예: `focus` 순서 시험 = [A, B] → B · [B, A] → A · 적재기 = `pick` 한 칸 비면 `None`).
- 빠진 것 = C-3(시너지 · 끝맺음 · 리스트의 켠 0.4 경로).

### 5. 실물(18222 · CHAT_STATE=on · DEBUG_PANEL=on · 허브 18105)

| 대화 | 턴 | 이해 출력(검증 뒤) | 객체 · 거르개 | 조회 · 화면 | 판정 |
|---|---|---|---|---|---|
| A | 「턱에 살이 너무 많아보여」 | `SITE-072` 턱 · `CON-168` 턱살(둘 다 `sure`) · `new` · `sites [SITE-072]` · 4,255ms · thinking 238 | 턱살 `said` · focus `CON-168` · `site_filter.sites [SITE-072]` | QY5 `concern_candidates(CON-168, site=턱)` · `list` = 턱살 → 내려온 지방분해 주사 계열 시술 · 점 `SITE-072`(직접) | 맞음(조사 끼임 고민이 첫 후보로) |
| A | 「사각턱인데?」 | `CON-161` 사각턱 · `SITE-076` 사각턱 · `new` | 사각턱 `said` · focus `CON-161` · 같은 이름 부위 `pair_kept [SITE-076]` · 거르개 `[SITE-076]`(턱 `SITE-072` 끌고 오지 않음 — QS1) | QY5 `(CON-161, site=사각턱)` 10 행 · `list` = 보톡스 계열 · 점 = `SITE-072`(턱살) + `SITE-076`(사각턱 · focus) — 직접만 · 누적 | 맞음(0.3 의 「사각턱인데?」 겹침 실패 AR-2 가 없어짐) |
| B | 「얼굴이 자꾸 빨개져요」 | `CON-125` 안면홍조 `sure=false` · `SITE-007` 얼굴 · 2,585ms · thinking 0 | 안면홍조 `guess` · 얼굴 `said` · focus 없음 | QY7 facets 18 · `ask` = 얼굴의 고민 선택지(안면홍조 셋째) · `list` · `sites` 안 보냄 | 계약대로 · BK5 아님(L-6) |

- 패널 조각(`state` SSE)에 `understand` · `site_filter` · `accepted` · `dropped` · `merged` · `turn_kind{kind, from}` 가 있다. `nouls` · `jev_requests` 는 0 이다. 장부 `timing.parts` = `understand_ms` · `hub_ms` · `llm_ms` · `material_ms`.
- 네 턴에 걸쳐 이해 호출이 2.6 ~ 4.3 초다(thinking 이 선 턴이 느리다 — E8-0).

### 6. 공개 레포

- 앱(공개): 바뀐 · 새 파일 52 에서 `/Users/` · 홈 이름 · 키 꼴(`sk-ant` · `api_key=`) · 내부 도메인 · 사설 IP grep = **0**. `.env` · `runs/` · `data/` 는 ignored 다. `.env.example` 은 이름만 더했다.
- 프로필(공개): L-7.

## 문턱 미달 원인 — 셋으로 가름(v04b · 채점 336 · 실패 44)

| 코드로 고칠 것 | 프롬프트 몫 | 측정 몫 |
|---|---|---|
| **C-2** 비축 고민 점 빠짐 — C59-1 · C61-1(**2 턴**) | 규칙 10 `sure` — 맞는 코드에 `false`(객체 13 + 이어진 점 3 = **16 턴** · C16-1 · C19-1 · C44-1 · C32-2 · C31-1 …) | **M-1** 실물 앞 답 대화의 키가 가짜 앞 답 기준 — C57-2 · 3 · C58-3 · 4 · 5 · C65-3 · 4 · C69-2 · 3(**9 턴**) |
| **L-5** BQ4 가 `guess` 고민을 대상으로 셈 — C46-2(**1 턴**) | 대상 고르기 — 계열 ↔ 시술 급(C50-1 · C50-3) · 제품 이름 차이(C77-4) · 말 안 한 고민 붙임(C41-2 · C41-3 · C75-3 · C09-3) · 리스트 가리킴(C57-4 · C67-4) · 「세 군데」(C23-5)(**약 10 턴**) | C38-4 — SPEC §8-1 이 「갈림」 으로 박아 둔 키(E8-5)(**1 턴**) |
| (C-1 · C-3 은 E8 수에 안 닿는다 — 답 · 시험 몫) | 턴 종류 `follow` ↔ `new`(C03-2 · C06-4)(**2 턴**) | 데이터 DA(C08-2 · C15-2 · C28-2 · C44-5)(**4 턴** — D-13 · 90 안의 몫) |
| | | 비결정 폭 — 같은 코드 재측정 없음(L-8 · 한쪽 약 12 턴) |

- 셈(이 검수의 판정 — 사람 검수 전): 코드 3 · 프롬프트 약 28 · 측정 13(M-1 9 + C38-4 1 + 데이터 4 — 데이터는 「실패로 센다」 가 D-13).
- **어림**(문턱 판정이 아니다): C-2 · L-5 를 고치고(+3) M-1 의 9 턴을 채점 밖으로 두면, 분모 = 336 − 9 = 327 이다. 8 검사 실패는 44 − 9 − 3 = 32 → 295/327 = **90.2%**, 3 검사 실패는 21 − 9 = 12 → 315/327 = **96.3%** 다(C-2 · L-5 는 3 검사 밖). 둘 다 문턱을 넘는 쪽이다. 다만 비결정 폭(L-8)이 이 차이와 같은 크기라, 같은 코드로 두 번 재야 판정할 수 있다.

## 고칠 차례(제안)

1. C-1(한 줄) · C-2 · L-5 — 코드. C-3 — 시험 세 파일 픽스처를 이해 가짜로(기대값 그대로) · 그 파일만 돌림.
2. M-1 — 코디 · 사용자가 ⓐ(실물 답으로 키 다시 매김) · ⓑ(채점 가름) 가운데 고른다.
3. 같은 코드로 E8 두 번(v04c · v04d) → 비결정 폭 · 문턱 판정.
4. L-2 머리 글자 여섯 · L-6 은 `pick` 문구 확인 때 사용자에게 같이 올린다. L-7 은 커밋 때.
