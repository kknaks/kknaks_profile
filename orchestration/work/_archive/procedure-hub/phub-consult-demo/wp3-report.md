# WP-3 리포트 — 조건 누적 · 주제 → 진료항목 (app 워커 · 2026-11-20)

발주 `task_55ea70c3f1d3` · `ctx_51d6946db7e1` · SPEC-010 0.2.7(§5-0 · §5-0b · §5-1 ~ §5-3 · §13 WP-3). 기준은 `$J` `1af2216c` · 허브 18105 `caa03560`(GET 만)이다. 커밋 0 · push 0 · 18222 손 안 댐(pid 64439 그대로) · 실물 서버 18297(끝에 내림). 코디 덧붙임(앞 주제 머리 = 조건 이름)도 반영했다.

## 1. 바뀐 파일

| 파일 | 무엇 |
|---|---|
| `clinic_chat/consult/detect.py`(새) | **이름 일치** `name_hits`(NM2 공백 지움 · NM3 긴 것 · NM4 같은 이름 전부 · NM5 진료항목 이름 먼저 · NM6 ASCII 3 글자 이하 낱말 경계 · 일반 낱말 표지). **`Detector.items(conds)`**: 칸 안 = 합집합, 칸끼리 = 교집합, 순서 = 이름 일치 → groups. 칸별 길: 고민 = `concern_candidates`(upper auto · to_procedure none · read_all)에서 reach 「케이스 직접」 만(나머지 reach 는 `dropped_reach` 로 셈 · 물려받은 고민은 `upper`) · 시술 = by_proc · 계열 = scope 의 procedure 행 · 케이스 = by_case · 제품 = by_product + scope 「하위 제품」 · 효과 = `facets outcome node=effect:` 의 procedure_case · procedure 행만(N2 · modality · product · package 는 셈만) · 부위 = SF2 · SF3 · 국가 = 제품 profile `country`(CD6 · 프로세스 캐시 · 빈칸으로 뺀 수 = 다른 칸 만족분 기준). **CZ1**: 이름 일치 밖 모든 값에서 케이스 0 을 뺀다. 같은 (도구, 인자) 는 턴에 한 번 · 허브 오류는 그 값만 빼고 `errors[]` |
| `clinic_chat/consult/topics.py`(새) | 조건 칸(`procedure · site · concern · effect · product · country`) · `turn_conditions`(follow 로 채운 대상 뺌 · method / material 칸 아님 · 이름 일치는 시술 칸 · 바뀐 칸 차례) · `merge`(CD2) · `withdraw`(CD4) · `subset` / `same` · 표지 `new_marker`(TP4 · 「또」 낱말 경계 · `도(고민|…)`) · `back_marker`(TP5) · **`decide`**: TP2 A · B → TP3 2 ~ 7 → TP11 후처리 → TP14 ① ~ ⑤ → TP6(`cond_dropped` · `add_zero`) → LS1 ~ LS3(LS2 = 바뀐 칸 역순 · 다 빼도 0 이면 all). 장부 칸 = TP10 한 정의 `{change, by, marker, A, B, llm_move, llm_to, rule_move, used, to_from, cond_dropped}` |
| `clinic_chat/consult/turn.py` | `Consult` 가 앞 맺는 줄의 주제를 들고(`last_topics` + `topic_switch`) 이해 호출 턴 메시지에 **주제 블록**(지금 주제 id + 앞 주제 · 머리 = IL11 조건 이름 · 수)을 넣는다. 검증에 앞 주제 id 를 넘긴다. `_after` 맨 앞 `_detect`(이름 일치 · 이번 턴 조건 · decide · 지금 주제 진료항목 · 장부 · 화면 값) · 감지 오류는 기록만(`detect_error`). 턴 줄기 **`items` 이벤트**(LLM 답보다 먼저) · 장부 `items{codes, by, conditions, turn_conditions, blocked, ls, name_hits, dropped_reach, upper, errors, country_dropped, ms, hub_calls}` · `consult{topics, active_topic, topic, conditions}` |
| `clinic_chat/consult/entry_list.py` | N1 — `TABLES` 에 `effect` · `procedure_case` · 머리 「효과」 · 「케이스」 |
| `clinic_chat/consult/verify.py` | `Accepted.country`(「KR」 · 「수입」 만) · `Accepted.topic`(`topic_of` — move 셋 밖 = 없음 · `to` 가 앞 주제 id 아니면 null) · `parsed_view` · `Accepted.view` 에 둘 |
| `clinic_chat/consult/understand.py` | `topic_lines` · `turn_message(…, topics=)`(객체 블록 뒤 · 이번 말 앞) |
| `clinic_chat/consult/prompt.py` | `PICK_HEADER_OPTIONAL`(주제 머리 · 필수 검사 밖 · r7 P2-B) |
| `prompts/consult.json` | `pick` 판 **`0.5.0-draft`** · 출력 꼴에 `country` · `topic` · 규칙 13(효과 · 케이스 표) · 14(country) · 15(topic) · 머리 「# 주제」 · 「지금 주제:」 · 「앞 주제:」 — **문구 초안(사용자 확인 대상)** |
| `tests/test_v05_detect.py`(새) | 31 시험(아래) |
| `tests/test_v04_list.py` · `test_v04_prompt.py` · `test_v04_ledger.py`(0.4 · 고침) | N1 표 일곱 · resolve `tables` 인자 · pick 판 `0.5.0-draft` · **「주제 머리 키 없음 → pick None 아님」 한 줄**(TP13) |

## 2. 시험

| 명령 | 결과 |
|---|---|
| `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_v05_detect.py` | **31 passed** — NM(고정본 셋 · 실물 E7 · E7b · E7c · E7d · E8b) · 고민 「케이스 직접」 만 + 쪽 넘김 2 쪽 + `dropped_reach` + 물려받은 고민(E1 · E3 · E3b) · E2 · 효과 케이스 · 시술 행만(E15 · N2) · 계열(E6) · 제품 하위(E8) · 시술(E5) · 케이스(E18) · 부위 SF2 · SF3 · CZ1(E4 · E4b · 몸 부위) · 이름 일치만 CZ1 밖 · 순서 · 교집합(E9) · 같은 호출 한 번 · 국가(C5 · R7 셈) · 허브 오류 · **주제** TP1 · T1(표지 · 자동) · T2 · T9(저장 상태 그대로) · T4 · C1 · T7 · C2 · C6 · T5 · T6(LS1 · 막은 칸 all) · C4(LS3 · 막은 칸 = 제품) · T8 · T10 · T11(LLM 대상 · cond_dropped) · T12 · T13(+ 검증 `topic_of`) · T14 · T15 · T16 · T17 · T18 · T19 · CD4(E14) · **한 턴 끝까지**(가짜 CLI · 가짜 허브: `items` 이벤트가 done 앞 · 장부 `items` · `consult.topics/active_topic/topic/conditions` · LLM `topic` 칸 · 두째 턴 새 주제 · **앞 주제 머리 = 조건 이름**(코디 덧붙임) · 재시작 뒤 주제 복원) · 이해 호출 턴 메시지의 주제 블록 |
| 위 + v05_page · v05_kos_map + **§13 WP-3 회귀 목록**(`test_consult_turn` · `test_v04_list` · `test_consult_listing` · `test_consult_carry` · `test_state_carry` · `test_v04_prompt` · `test_v04_ledger` · `test_v04_verify` · `test_v04_understand` · `test_v04_turn` · `test_answer_key`) + WP-2 때 0.4 화면 · 장부 묶음 | **262 passed · 1 skipped** |
| `ruff check` 손댄 py 11 · `ruff format` 새 py 3 | 통과 |

## 3. 실물 표본 대조(빈 포트 18297 · 실제 이해 호출(소넷) · 허브 caa03560 · `$J` 1af2216c)

| 말 | 이해 호출이 고른 대상 | 진료항목 수 | 스펙 기대 | 엉뚱함 · 비고 |
|---|---|---|---|---|
| 팔자주름이 고민이에요 | concern CON-009 + site SITE-046 | **23** | 23 | 다한증 · 승모근 · 종아리 · 침샘 **0** · 「제품 경유」 239 행 버림 |
| 턱살이 고민이에요 | concern CON-168 | **5** | 5 | — |
| 기미가 고민이에요 | concern CON-068 | **27** | 27 | 「제품 경유」 90 행 버림 · 몸(바디) 2 는 정상(케이스 직접) |
| 리프팅 받고 싶어요 | effect EFF-010 | **130** | 130 | modality 5 · product 46 · package 2 행 버림 · 보톡스 PRC-001 시술 행이 106 을 품어 다한증 · 승모근 · 침샘 보톡스가 든다(**O-8 코디 · 사용자 판단 그대로**) |
| 미백 하고 싶어요 | effect EFF-049 | **4** | 4 | — |
| 써마지 받고 싶어요 | product PRD-416 | **5** | 5 | — |
| 보톡스 국산으로 하고 싶어요 | modality M1 · country KR | **57** | (C5) | 보톡스 106 가운데 KR 제품 57 · 국가 빈칸으로 뺀 것 0(나머지는 수입 제품) |
| BBL HERO (1가지 모드) 궁금해요 | product PRD-321 + 이름 일치 | **1** | E7 | 이름 일치 진료항목 |
| 셀코어 궁금해요 | product PRD-181 + 이름 일치 「셀코어」 | **1** | E8b | 제품 길은 CZ1 로 0 · 이름 일치로 나옴 |

허브 없이 같은 셈을 직접 돌린 값도 같다: 다한증 15 · E6 필러 M2 23 · 지방분해 M18 18 · E4 턱 142 · E4b 얼굴 220 · E9 주름 ∩ 턱 80 · C3 다한증 ∩ 써마지 0 · T6 B(종아리 ∩ 쥬비덤) 0 · T19 써마지 ∩ 턱 3.

## 4. 주제 시나리오(실물 · 장부 발췌 · `wp3real000000002`)

| 턴 | 말 | 이해 호출 `topic` | 장부 `consult.topic` | 주제 목록(머리 = 조건 이름 · 수) · 지금 |
|---|---|---|---|---|
| 1 | 볼에 필러 맞고 싶어요 | continue | by first · A 6 · used continue | **t1 [필러 · 볼] 6** · 지금 t1 |
| 2 | 쥬비덤으로 할래요 | continue | A 1 · B 6 · rule continue · used continue | **t1 [필러 · 볼 · 쥬비덤] 1** · 지금 t1(좁힘) |
| 3 | 그리고 기미도 고민이에요 | new | marker 「그리고」 · A 0 · B 27 · rule new · llm new · used new | t1 [필러 · 볼 · 쥬비덤] 1 · **t2 [기미] 27** · 지금 t2 |
| 4 | 아까 볼 필러 다시 보여줘요 | return · to t1 | marker 「아까」 · rule return · llm return(to t1 = 규칙 대상) · used return · to_from llm · cond_dropped false | **t1 1 그대로(저장 상태 · 앞 값 6 으로 안 돌아감)** · t2 27 접힘 · 지금 t1 |

- 화면 머리(`wp3-shots/topics-real.png`): 지금 「필러 · 볼 · 쥬비덤 1」(펼침) · 앞 「기미 27」(접힘). 코디 덧붙임대로 조건 이름이다.
- 허브 호출: 턴마다 1 ~ 3 · 감지 6 ~ 13 ms.

## 5. 스펙과 다른 점 · 남은 것

| # | 무엇 | 실측 · 내용 | 제안 |
|---|---|---|---|
| D1 | **LS3 「막은 칸 값은 칸에 남는다」 → 그 주제의 A 가 늘 0** | 실물 `wp3real000000001`: 1 턴 「볼 꺼짐 때문에 필러」 에서 이해 호출이 고민 「볼 꺼짐」(CON-057 — 「제품 경유」 행만 · 진료항목 0)을 골랐다 → A = B = 0 → LS3(막은 칸 = 고민 · 목록 6). 2 턴 「쥬비덤으로」 는 막은 고민이 칸에 남아 A = 0 · B = 6 → **TP3 4 자동 새 주제**가 되었다(좁히기가 안 됨). 같은 대화 4 턴 되돌림도 `add_zero` | 코디 판단: (가) LS 로 막은 칸 값은 주제 칸에서 빼고 장부 `blocked` 에만 둔다 (나) A 셈에서 막은 칸을 빼고 센다 (다) 그대로. 코드는 지금 스펙 문구대로 (다)다 |
| D2 | SF3 몸 조상 | 「조상 몸(SITE-147)」 만 적혀 있으나 r4 · r6 실측(써마지 FLX 가 종아리에 맞음)은 SITE-001 전신까지 몸 조상으로 본 값이다. 코드는 부위의 조상 전부(몸 · 전신)를 몸 규칙으로 본다 · 얼굴 부위면 맨 위 조상(얼굴)만 | SF3 에 「SITE-001 전신 포함」 한 줄 |
| D3 | CZ1 범위 | 스펙 본문은 「부위 · 제품 · 효과 · 고민 칸」 이지만 「19 는 이름 일치로만」 과 맞추려고 시술 칸의 허브 값(시술 · 계열 · 케이스)에서도 케이스 0 을 뺐다 | CZ1 에 「이름 일치 밖 모든 값」 |
| D4 | SF1 부위 칸 출처 | 0.4 부위 거르개(`site_filter`)가 아니라 이번 턴 이해 결과의 site 대상(follow 로 채운 것 뺌)을 쓴다. OU7 이어받기는 CD2(칸 그대로)로 같은 결과 | 그대로 두거나 SF1 문구를 맞춤 |
| D5 | 이름 일치 범위 | NM2 대로 말 안의 덩이를 다 맞추므로 「가짜보톡스시술」 안의 KOS 시술 「가짜 보톡스」 처럼 긴 낱말 안 이름도 맞는다(시험에서 확인). 실물 KOS 이름은 대부분 길어 문제는 아직 못 봤다 | 지켜봄 |
| D6 | TP12 「데이터 판이 바뀐 재시작이면 다시 셈 · 장부 표지」 | 안 함 — 저장 상태를 그대로 쓴다 | WP-7 또는 다음 판 |
| D7 | TP7 · R11 · LC7(주제 바뀜을 봇이 한 줄 말함 · 조건 줄 · 막은 조건 말함) | 장부에는 있으나 LLM 블록은 **WP-6** | WP-6 |
| D8 | 주제 id 꼴 | `t1` · `t2` …(스펙에 꼴 없음) | — |
| D9 | pick 규칙 13 ~ 15 · 머리 글 | 초안(사용자 확인 대상) | 사용자 |
| D10 | 0.4 `list` · `sites` 이벤트 | 아직 보낸다(받는 자리 없음 · 장부 0.4 칸 유지 ST2) | O-5(0.6) |
| D11 | 가짜 턴 주제 | WP-2 가짜 턴은 여전히 KOS 시술 이름을 시술 칸 값으로 쓴다(가짜 감지). 실제 턴은 이해 호출 조건 이름이다 | — |

- 18222 재기동: 이제 실제 턴이 `items` 를 보내 왼쪽 목록 · 점이 바뀐다(WP-2 검수 P2-3 의 막힘은 풀림). `.env` 에 `CHAT_KOS_MAP` 이 있어야 뜨는 것은 그대로다.
