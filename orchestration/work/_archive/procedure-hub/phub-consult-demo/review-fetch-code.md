# SPEC-011 구현 검수 (reviewer · 2026-11-23)

발주 `task_ad18d0780e5c` · `ctx_97a856861651`.
- 대상: 구현 발주 `fetch-plan-code-task.md` · 정본 `SPEC-011-fetch-plan.md` 0.1.2 · 리포트 `fetch-code-report.md` · `fetch-code/` · 앱 워크트리 `git diff`.
- 이번 변경 위주로 봤다. 13:12 이후 바뀐 파일은 `verify.py` · `understand.py` · `kinds_pick.py` · `material.py` · `material_read.py` · `ledger.py` · `turn.py` · 새 `fetch_read.py` · `config.py` · `prompts/consult.json` · 시험 7 이다.
- 규칙:
  - 코드 · 데이터는 고치지 않았다(시작 · 끝 `git status` · `git diff` 바이트 같음). 커밋 0 · 서브에이전트 0 · 키 출력 0 이다.
  - 18222(pid 22758) · 18105(pid 56191)는 그대로다.
  - 실물은 빈 포트 **18241** 에 같은 env + 따로 `CHAT_DIR`(스크래치)로 띄우고, 끝나고 껐다.
- 검수 사본 · 스크립트: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-PROCEDURE-HUB-phub-consult-demo/2a3fa575-be27-4afd-b79b-a4acb54de70e/scratchpad/rvfc/`
  - `cmp_live.py` · `tok_check.py` · `shot.cjs` · `head/`(HEAD archive)
  - 재생 장부(가격 포함)는 스크래치에만 있다.

## 판정: **PASS**(P0 0 · P1 0 · P2 4)

- WP-1 ~ WP-4 와 사용자 결정(UD1 ~ UD5 · DQ1 = 예 · 호출마다 토큰)대로 구현됐다.
- 실물 3 대화를 직접 다시 돌렸다. 「## 자료」 바이트가 코드 워커 판과 **턴마다 같았고**(2차가 결정론), 답 입력은 **−51.4%**(워커 −50.9%)로 재현됐다.
- 답 호출 토큰은 CLI 세션 기록과 **14/14 같다**.
- 옛 실패 1 은 **HEAD 에서도 같은 자리에서 실패**한다.
- 남은 것은 P2 넷이다(문장 · 방어 손질).

## 1. 볼 것 1 — 스펙 · 사용자 결정 · 스펙 밖 고침

| 항목 | 확인 | 판정 |
|---|---|---|
| UD1 1차 JSON → 2차 결정론 → 3차 | `verify.fetch_of`(`verify.py:124`) → `Consult.fetch_cut`(`turn.py:719`) → `fetch_read.decide`(`fetch_read.py:144`, 판단 0 · 순서 고정) → `renumber(cut=…)` | ✅ |
| UD2 Jev 거르기 없음 | 상담 경로에 `system_one` 호출 없음(Jev 는 끈 가지 `walk()` 만 · `turn.py:172`) | ✅ |
| UD3 `--resume` 둠 | 답 호출 `llm/chat_cli.py:159`(그대로) | ✅ |
| UD4 출력 안 줄임 | 출력 상한 · 줄임 코드 없음. 답 출력은 `tokens.calls[].output` 기록만 | ✅ |
| UD5 상한 고정 없음 · 안전 · 명시 늘 | `fetch_read.py:155-160` — 명시(코드 · 이름) → 안전(adverse · recovery · contraindication · avoid · caution)이 종류 · 주제 · 범위 판단보다 앞이다(밖 하위 안전 줄도 전체) | ✅ |
| DQ1 범위 기본 | `FETCH_DEFAULT.scope = branch`(`verify.py:27`) · 명동점 닿음 = 매핑 `by_case` · `by_proc` · `by_product`(`fetch_read.py:89`) · 밖 하위 · 후보는 이름만(`:177`) | ✅ |
| KD9 범위(스펙 §3-3) | 상담 경로 `kinds_pick.py` 만 끔 · `STRONG_BY = yes · entry · fetch`(`:20`). `walk/front.py` KD9 · `KD9_SET` · `report.py` 는 diff 0 | ✅ |
| G7 이름만 → 같은 번호로 다시 싣기 | `material.py:176-190` · `ledger.py:242-246`(이름만은 `sent_names` · 전체로 다시 실으면 `sent` 로 옮김) · `turn.py:197` 에서 넘김. 시험 `test_g7_names_then_named_again_same_number_full` 통과 | ✅ |
| (스펙 밖) `verify.parse` 맨 끝 객체 | `verify.py:83-112`. 첫 `{` ~ 마지막 `}` 가 JSON 이면 옛 길 그대로이고, 깨질 때만 맨 끝 **완결** 객체를 받는다. 앞 객체 안의 중첩 객체는 `raw_decode` 의 end 로 건너뛴다 | ✅. 다만 꼬리 조각 객체를 받을 수 있다(P2-1) |
| (스펙 밖) `layers` 칸 없앰 | 프롬프트 출력 꼴에서 뺌 · `fetch_of` 는 `layers` 가 없으면 고침으로 세지 않음 · `fetch_cut` 이 `plan.layers = "sub"` 고정(`turn.py:725`). 스펙 JC3 추천 · 측정 62/62 sub 와 맞다 | ✅ |
| (스펙 밖) `CHAT_FETCH_CUT` | `config.py:94` on 기본 · off 면 줄은 다 싣고 `new_lines[].fetch_would` 만 남긴다(`turn.py:198-202`). `.env.example` 값 없음 | ✅. 되돌림 손잡이로 안전하다 |
| (스펙 밖) renumber 를 감지 뒤로 | `turn.py:193-204`. 상담 경로만 옮겼고, 끈 가지는 앞 그대로(`:190`). talk 턴 · NO_B_ON 턴은 옛처럼 재료 0. `after_walk` 는 `tm` 을 쓰지 않는다. shrink(`material.py:371`)는 그 뒤에서 그대로 돈다 | ✅ |

## 2. 볼 것 2 — 호출마다 토큰

- **상담 경로 LLM 호출 = 둘.** grep(`run_cli(` · `und.call(` · `.turn(` · `system_one(` · `create_subprocess`)으로 확인했다.
  - 이해: `turn.py:428` → `understand.py:230`.
  - 답: `turn.py:259` → `chat_cli.py:159`.
  - 나머지(`e8.py:100` · `probe.py:72` 실측 스크립트 · `llm/cli.py:318` 시험 앱 열 · `jev_client.py:79` 끈 가지)는 상담 턴에서 불리지 않는다.
  - `modal` · `detect` · `ask_axis` · `kos_block` 은 LLM import 가 0 이다.
- **CLI 원 usage 대조**(`tok_check.py`): 코드 워커 재생 장부(`live_on`) 14 턴의 `tokens.calls[answer]` 를 CLI 세션 기록(`~/.claude/projects/-Users-kknaks-Library-Caches-clinic-chat-consult-cli/<session>.jsonl` · assistant 메시지 id 마다 usage)과 맞댔다.
  - 네 칸이 **14/14 같다**.
  - 옛 평평한 칸 = `calls[answer]` 14/14 이다.
  - `sum` = `calls` 합 14/14 이다.
  - `calls[understand]` = `consult.understand.usage` 14/14 이다.
  - 이해 호출은 `--no-session-persistence` 라 세션 기록이 없다. 앱이 CLI `result.usage` 를 그대로 옮기는 것만 코드로 확인했다(`understand.py:256-263`).
- **null 처리**: `_int_or_none`(`turn.py:113`)이다. 값이 없으면 null 이고 `sum` 도 값이 하나도 없으면 null 이다. 시험 `test_v06_fetch_contract`(null) 통과. 답 호출 `thinking` 은 CLI 답 경로가 내지 않아 늘 null 이다(지어 넣지 않음 — 발주 「있으면」 대로).
- **옛 칸 읽는 곳**: 평평한 `tokens.input_tokens` 등은 그대로 남았다.
  - `token-cause` · `fetch-plan` 스크립트는 사본으로 `replay54 --offline` 을 돌려 그대로 돈다.
  - `speed.py` · `columns/*` 는 시험 앱 `runs.jsonl` 꼴이라 무관하다.
  - `consult/e3.py` · `e5.py` 는 `tokens` 를 통째로 복사만 한다.
  - 깨진 곳 0 이다.

## 3. 볼 것 3 — 실물 직접(18241 · 잘라 내기 켬 · 발주서 말 그대로 13 턴 · 모두 `done`)

칸 = input / cache_creation / cache_read / output. 「전」 은 옛 장부다(03b8 · 73bd = `runs/consult/turns.jsonl` · ecc6 = 테스트 고침 E 재생 장부). 「워커」 는 `fetch-code` 의 `live_on`, 「검수」 는 이번 18241 이다.

| 턴 | 말 | 이해 전 | 이해 후(워커) | 이해 후(검수) | 답 전 | 답 후(워커) | 답 후(검수) | 답 입력 전 → 워커 → 검수 | 「## 자료」 B 전 → 워커 → 검수 | fetch(검수) | 정보없음(전/워커/검수) | 이름만 줄 인용(검수) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 03b8 T1 | 팔자주름에 대해서 고민이돼 | 2/None/19183/97 | 2/0/21063/139 | 2/0/21063/138 | 2/11688/5608/280 | 2/17691/0/772 | 2/0/17691/871 | 17,298 → 17,693 → 17,693 | 1,337 → 1,337 → 1,337 | targets/[]/branch/none | 0/0/0 | - |
| 03b8 T2 | 미간에 주름도 고민이야 | 2/None/19183/117 | 2/1341/20507/159 | 2/1383/20507/159 | 4/5517/16976/317 | 4/5046/17691/643 | 4/5145/17691/248 | 22,497 → 22,741 → 22,840 | 892 → 892 → 892 | targets/[]/branch/none | 0/0/0 | - |
| 03b8 T3 | 얼굴에 탄력이 좀 떨어지는거 같은 | 2/None/19183/117 | 2/1883/20507/159 | 2/1959/20507/159 | 4/7744/22493/447 | 4/8110/22737/367 | 4/7715/22836/471 | 30,241 → 30,851 → 30,555 | 2,566 → 2,566 → 2,566 | targets/[]/branch/none | 0/0/0 | - |
| 03b8 T4 | 그중에서 소프웨이브, 써마지, 울 | 2/None/19183/133 | 2/2396/20507/175 | 2/2471/20507/175 | 4/9480/30237/675 | 4/8827/30847/1825 | 4/8931/30551/1237 | 39,721 → 39,678 → 39,486 | 13,455 → 13,455 → 13,455 | targets/[]/branch/none | 0/0/0 | - |
| 03b8 T5 | 고주파 원리가 머야 ? | 2/None/19183/98 | 2/3168/20507/151 | 2/3210/20507/151 | 4/9039/39717/282 | 4/12183/39674/1348 | 4/11595/39482/895 | 48,760 → 51,861 → 51,081 | 15,520 → 20,062 → 20,062 | targets/overview,mechanism/branch/none | 0/0/0 | - |
| 03b8 T6 | 응 고주파에 대해서 전반적으로 설 | 2/None/19183/97 | 2/3242/20507/174 | 2/3239/20507/173 | 4/43255/48756/1395 | 4/31234/51857/2991 | 4/30783/51077/1701 | 92,015 → 83,095 → 81,864 | 90,211 → 60,856 → 60,856 | targets/overview,mechanism,indication,outcome,lineup/branch/names | 0/0/0 | [432, 433, 435, 440, 449, 466] |
| ecc6 T1 | 요즘 피부 탄력이 저하 되서 고민 | 2/None/19411/98 | 2/0/21069/133 | 2/0/21069/133 | 2/0/18358/258 | 2/0/18753/995 | 2/0/18753/215 | 18,360 → 18,755 → 18,755 | 2,548 → 2,548 → 2,548 | targets/[]/branch/none | 0/0/0 | - |
| ecc6 T2 | 얼굴에 | 2/None/19411/104 | 2/1659/20507/139 | 2/1670/20507/139 | 4/197324/18038/294 | 4/39255/18753/1064 | 4/38794/18433/333 | 215,366 → 58,012 → 57,231 | 433,360 → 79,429 → 79,429 | topic/[]/branch/none | 0/0/0 | - |
| ecc6 T3 | 얼굴에 | 2/None/19411/104 | 2/2656/20507/139 | 2/2777/20507/139 | 4/198808/215362/505 | 4/4038/58008/497 | 4/3305/57227/273 | 414,174 → 62,050 → 60,536 | 423,129 → 20 → 20 | topic/[]/branch/none | 0/0/**1** | - |
| 73bd T1 | 얼굴에 피부 탄력이 없어져서 걱정 | 2/None/19183/118 | 2/0/21071/160 | 2/0/21071/159 | 2/12827/5608/1066 | 2/12865/5965/986 | 2/0/18830/829 | 18,437 → 18,832 → 18,832 | 2,548 → 2,548 → 2,548 | targets/[]/branch/none | 0/0/0 | - |
| 73bd T2 | 아 주름이 눈가 입꼬리에 잇어 | 2/None/19183/533 | 2/1696/20507/557 | 2/1719/20507/505 | 4/7965/18435/788 | 4/7922/18830/633 | 4/7766/18830/704 | 26,404 → 26,756 → 26,600 | 1,379 → 1,379 → 1,379 | targets/[]/branch/none | 0/0/0 | - |
| 73bd T3 | 아 눈가는 볼뉴머 이ㅃ고리는 필러 | 2/None/19183/464 | 2/2174/20507/252 | 2/2228/20507/252 | 4/2147/26400/1900 | 4/3559/26752/1034 | 4/3630/26596/1238 | 28,551 → 30,315 → 30,230 | 881 → 881 → 881 | targets/[]/branch/none | 1/1/1 | - |
| 73bd T4 | 입꼬리에는 필러를 맞고 싶다니까 | 2/None/19183/116 | 2/1997/20507/158 | 2/2001/20507/158 | 4/4305/28547/1260 | 4/2144/30311/418 | 4/2348/30226/272 | 32,856 → 32,459 → 32,578 | 20 → 20 → 20 | targets/[]/branch/none | 1/1/1 | - |

**합(전이 있는 턴)**
- 답 입력: 전 1,004,680 → 워커 493,098(−50.9%) → **검수 488,281(−51.4%)**.
- 「## 자료」 바이트: 987,846 → 185,993(−81.2%) → **185,993(−81.2%)** — 워커 판과 턴마다 같다.
- 답 길이(출력)는 호출마다 다르다. 같은 앱인데 검수 출력이 워커보다 대체로 짧았다(03b8 T4 1,825 → 1,237 등). UD4 대로 기록만 한다.

**빠짐**
- 잘라 내기 켬에서는 뺀 줄이 답에 보이지 않아 셀 수 없다. 그래서 워커의 끔 장부(`live_off` · `fetch_would`)를 다시 셌다.
  - 인용 85 = 그 턴 줄 79 + **앞 턴 줄 6**.
  - 그 턴 줄 79 은 뺌 0 · 이름만 3(03b8 T6 lineup) · 전체 76 이다.
  - 앞 턴 줄 6 은 근원 턴에서 모두 `full`(read · explicit)이다.
  - **빠짐 0** 이 재현된다.
- 표본 43 · 지금 시대 밖 11 은 `replay54.py --offline`(사본)으로 다시 셌다. −62.6% · −17.6% · 빠짐 0/276 · 0/49 · 상세 잃음 7 · lineup 17 이 리포트와 같다.

**이름만 줄에 지어낸 상세: 0**
- 03b8 T6 이 인용한 이름만 줄 6 은 모두 `marks.names_only = lineup`, `holder_name` 만 있는 줄이다(써마지FLX · 올리지오 · 텐써마 · 볼뉴머 · 인모드 · 써마지).
- 답은 그 줄로 「고주파 장비로는 써마지, 볼뉴머 … 올리지오, 인모드, 텐써마 … 명동점에는 없어요」 처럼 **이름만** 말했다.
- 「명동점에는 써마지 FLX 가 있고」 는 옛 답과 같은 꼴이다.

## 4. 볼 것 4 — 답 품질(전 → 후 · 사람 눈)

| 턴 | 판정 |
|---|---|
| 03b8 T1 ~ T4 | 빠진 정보 0. 같은 계열 설명이고, 주제 바뀜 알림 · 목록 남음 안내가 새 판에서 더 또렷하다. T4 는 세 장비 깊이 · 제조사(써마지 = 솔타 모노폴라 RF · 울쎄라 = 멀츠 집속초음파 3mm/근막)를 자료 줄대로 말했다 |
| 03b8 T5 | 전 답은 「조직을 가열하는 원리예요」 + 그림 표지뿐이었다. 후 답은 overview 를 더 읽어 모노폴라 · 바이폴라 깊이까지 말한다. **나아짐**(FR6 규칙대로 자료 15.5 → 20.1 KB) |
| 03b8 T6 | 원리 · 적응증 · 효과 시점 · 유지 · 라인업을 다 말한다. 전 답의 「강력한 리프팅은 어려운 편」 한 줄은 후 답에 없다(그 줄은 실렸으나 답이 고르지 않은 것 — 답 변동). 명동점 밖을 잘못 말한 것 0 |
| ecc6 T1 | 같다 |
| ecc6 T2 | 전 답은 명동점 목록 62 개 · 옵션 가격 · 「목록 일부만 얼굴」 설명이었다. 후 답은 계열 설명 + 명동점 진료항목 이름이다. 빠진 정보 0. 가격은 명동점 블록 몫이라 이 변경과 무관하다 |
| ecc6 T3 | 후 답(검수)이 「**이번에는 새로 가져온 자료가 없어서 더 보태 드릴 내용은 없어요**」 라고 했다. 같은 말 되풀이라 새 줄 0(앞 줄은 `seen_lines`)인 턴이다. 앱 속사정을 손님에게 말한 문장이다(워커 판 답에는 없음 — 답 변동). **P2-2** |
| 73bd T1 · T2 | 같다(빠진 정보 0) |
| 73bd T3 · T4 | 후 답 둘째 줄이 「**필러 개요 정보는 없어요**」 다. 전 답에도 T3 · T4 모두 같은 류의 문장이 1 씩 있었다(EM `empty[]` — 개요를 읽었는데 허브 행 0). 이번 변경 탓은 아니지만 첫머리에 보인다. **P2-3**(리포트 §6-1 과 같음 · 코디 결정 몫) |

틀린 말 · 명동점 밖을 잘못 말함 · 안 가져온 종류로 인한 「정보 없어요」 는 0 이다.

## 5. 볼 것 5 — 화면(새 브라우저 프로필 · 페이지마다 새 chromium · 18241)

| 화면 | 결과 | 스크린숏 |
|---|---|---|
| 03b8 마지막 | 주제 3(머리 3) · 얼굴 점 4 · 목록 13(소프웨이브 · 써마지 · 울쎄라 묶음) · 답 6 · 「시술 원리 · 조직 가열」 그림 · 페이지 오류 0 | `e2e-shots/review-fetchplan-03b8-final.png` |
| ecc6 마지막 | 주제 1 「얼굴 피부 탄력 저하 62」 · 점 1 · 목록 62 · 페이지 오류 0 | `e2e-shots/review-fetchplan-ecc6-final.png` |
| 73bd 마지막 | 주제 3 · 점 5(눈가 · 입꼬리) · 목록 6(풀페이스필러) · 페이지 오류 0 | `e2e-shots/review-fetchplan-73bd-final.png` |
| 모달 | 「얼굴필러 레스틸렌」 — 탭(시술 개요 · 설명 · 효과 · 부작용) · 원리 그림 「채움」 · 담기 단추 | `e2e-shots/review-fetchplan-73bd-modal.png` |
| 스피너 | 새 대화 첫 턴 1.5 초에 「질문을 이해하고 있어요」 · 끝나면 스피너 0 · 답 1 | `e2e-shots/review-fetchplan-spinner.png` · `review-fetchplan-spinner-done.png` |

앞 고침(D · E) 꼴(주제 머리 · 점 · 목록 접기 · 모달 탭 · 이해 중 스피너)이 그대로다 ✅.

## 6. 볼 것 6 — 시험

- **관련**(스펙 목록 + 새 둘 + 고친 시험 + `test_v04_turn` · `test_v04_verify` · `test_state_object`): **174 passed · 1 skipped · 1 failed**.
  - 실패 1 은 `test_state_object.py::test_s5_t18_terminal_turn_updates_but_no_list_then_catches_up` 다.
- **옛 실패 확인**: `git archive HEAD` 를 스크래치 `head/` 에 풀고 그 코드로(`clinic_chat.consult.verify.__file__` 가 `head/` 임을 확인) 같은 시험을 돌렸다. **같은 자리 `tests/test_state_object.py:146` `assert (None == '범위 밖')` 로 실패**한다.
  - 시험 파일은 HEAD 와 diff 0 이다.
  - 원인 규칙(「검수 L-1 대상 없이 거둠만 = talk」)도 HEAD `verify.py:175` 에 있다.
  - 이번 변경 전부터의 실패다 ✅.
- 전체 pytest 는 발주(관련만)대로 돌리지 않았다.

## 7. 지적

### P2

| # | 지적 | 근거 | 고칠 방향 |
|---|---|---|---|
| P2-1 | `verify.parse` 대체 길이 **아무 꼬리 객체**나 받는다 | `verify.py:83-98 last_object` 는 맨 끝 완결 `dict` 면 칸을 보지 않는다. 이해 호출이 객체 뒤에 「Wait — scope 는 `{"scope":"all"}`」 같은 조각을 내면 그 조각이 parsed 가 된다. 그러면 targets 0 → 대상 없는 턴으로 간다. 실측 2 건은 둘 다 온전한 객체를 다시 낸 꼴이라 문제가 없었다 | 맨 끝 객체 가운데 `targets` 또는 `kind` 칸이 있는 것만 받는다. 시험에 「꼬리 조각 객체」 갈래를 하나 더한다 |
| P2-2 | 새 줄 0 턴에서 답이 앱 속사정을 말한다 | 검수 실물 ecc6 T3 「이번에는 새로 가져온 자료가 없어서 더 보태 드릴 내용은 없어요」(워커 판에는 없음 — 답 변동). 잘라 내기로 같은 말 되풀이 턴은 「## 자료」 가 20 B 가 되어 이 꼴이 더 자주 난다. R15(`prompts/consult.json:392`)는 「fetch 밖 종류를 정보 없음으로」 만 막는다 | R15 에 「새 자료 줄이 없거나 `seen_lines` 만 있는 턴은 앞 자료로 답하고, 자료를 새로 가져왔는지는 말하지 않는다」 한 줄을 더한다 |
| P2-3 | 「필러 개요 정보는 없어요」 가 답 첫머리에 온다 | 73bd T3 · T4(전 · 워커 · 검수 셋 다). EM `empty[]` 를 답이 그대로 말함 | 리포트 §6-1 대로 코디 결정(SPEC-010 검수 P2-2 몫). 이번 변경 탓은 아니다 |
| P2-4 | 리포트의 「전」 이해 열 꼴 | 리포트 §3 표의 이해 「전」 cache_creation 이 `null` 인 것은 옛 앱이 버린 칸이라 맞다. 다만 답 「전」 과 「후」 의 첫 턴 cache 가 다른 것(03b8 T1 워커 17,691 쓰기 · 검수 17,691 읽기)은 앞 실행이 데운 캐시 차이다. 토큰 비교에 「캐시 상태에 따라 creation ↔ read 가 옮겨 감 · 합으로 볼 것」 을 한 줄 적어 두면 오독이 준다 | 리포트 주석 한 줄 |

## 8. 다시 돌리기

```bash
A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo
W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo
R=/private/tmp/claude-501/-Users-kknaks-orca-workspaces-PROCEDURE-HUB-phub-consult-demo/2a3fa575-be27-4afd-b79b-a4acb54de70e/scratchpad/rvfc
cd $A && CHAT_DIR=$R/chat CHAT_STATE=on CHAT_KOS_MAP=data/kos/myeongdong-mapping-20261120-v3.json CHAT_KOS_MAP_SHA=d21903f5 \
  CHAT_IMAGE_DIR=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/assets/procedure-images/images uv run python -m clinic_chat.consult --port 18241 &
uv run --no-sync python $R/live/live3.py http://127.0.0.1:18241 rv        # 실물 13 턴
uv run --no-sync python $R/cmp_live.py $W $R                             # 전 · 워커 · 검수 표
python3 $R/tok_check.py <장부 turns.jsonl>                                # calls[answer] ↔ CLI 세션 기록
PW_PATH=<playwright> node $R/shot.cjs http://127.0.0.1:18241 $W/e2e-shots '<{"03b8":id,…}>'
cd $R/head && $A/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_state_object.py   # HEAD 옛 실패
```
