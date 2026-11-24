# O-14 · O-15 반영 리포트 (app 워커 · 2026-11-22)

발주 `task_3ec8360de79e` · `ctx_787b6add7ce3` · 사용자 결정 11-22 「추천으로 가」. 커밋 0 · 서브에이전트 0 · 18222 손 안 댐 · 실물 실행 0(발주 범위 = 시험 줄).

## O-14 — 같은 값 앞 주제가 깊게보다 먼저

`clinic_chat/consult/topics.py`:
- 새 함수 `holds(turn, conds)` — 이번 턴 부딪힘 칸(부위 · 고민 · 시술 · 이름 일치 값 빼고) 값이 하나 이상이고, 그 값이 모두 그 주제 칸에 **같은 값**(표 · 코드 같음 또는 원문 이름 같음)으로 있는가.
- 판단 순서에 **1b** 를 넣었다(칸 0 · 정보 질문 · 첫 주제 다음, 「깊게」 앞).

| 판단 | 결과 |
|---|---|
| 지금 주제가 그 값을 다 가짐 | 1b 건너뜀(지금 주제에 머무름 → 깊게) |
| 그 값을 그대로 가진 앞 주제 하나 | **되돌림**(`to_from: rule` · 장부 `topic.same_values: true`) — 지금 주제의 빈 칸 채움보다 앞섬 |
| 둘 이상 | 이해 호출 `to` 가 그 가운데면 그 주제(`to_from: llm`) · 없거나 무효면 **물음**(`ask` · 조건 안 바꿈) |
| 없음 | 옛 순서 그대로(부딪힘 없음 → 깊게 / 부딪힘 → 맞는 앞 주제 · 새 주제) |

## O-15 — 앱 제안 셋 확정

| 확정 | 코드 |
|---|---|
| 뺌 칸(「~ 말고」 → 제외) | 그대로(주제 튜플 판) |
| 정보 질문 → 주제 그대로 | `topics.info_question(kinds, out, 말)` 로 한곳에 모음. 이해 `kinds`(원리 · 효과 · 부작용 …) · `out` 에 **가격 낱말 「가격」 · 「얼마」 · 「비용」** 을 더했다. 이해 종류 코드에 가격이 없어서, 「볼뉴머 가격은?」 이 볼뉴머로 좁혀지던 구멍을 막는다(앱 표지 · 낱말 목록은 사용자 확인 대상). 조건은 옛 판과 같다: 부위 · 고민 없음 + 그 값의 진료항목이 지금 목록과 겹침 |
| 같은 값 = 원문 이름 같음 | 그대로(`_same_value`) · O-14 `holds` 도 같은 판정을 쓴다 |

## 시험(`tests/test_v05_topic_tuple.py` · 줄 추가)

| 시험 | 무엇 |
|---|---|
| `test_o14_same_values_prev_topic_wins_over_deepen` | ① {볼 · 볼륨 손실 · 필러} → ② {기미} → 「아까 볼 필러 다시」(부위 볼 · 시술 필러) → **① 되돌림**(rule · `same_values`) · ② 칸에 볼 · 필러 안 섞임 · ① 저장 목록 그대로 |
| `test_o14_no_prev_with_value_deepens_current` | ① 팔자주름 → ② 미간 → 「보톡스로」(앞 주제에 보톡스 없음) → **미간 깊게** · 지금 주제가 이미 값을 가지면 머무름 |
| `test_o14_two_prev_with_value_llm_or_ask` | ① 팔자주름 · 보톡스 · ② 미간주름 · 보톡스 · ③ 턱(지금) → 「보톡스」 → 물음(t1 · t2) · LLM `to` t1 이면 t1 |
| `test_o15_info_question_includes_price_words` | kinds · 가격 낱말 · 「보톡스로 맞고 싶어서」 는 정보 질문 아님 · 목록 안 것의 가격 = 주제 그대로 |

| 명령 | 결과 |
|---|---|
| `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_v05_topic_tuple.py` | **15 passed**(a7d7e253 10 턴 시나리오 시험 포함 — O-14 뒤에도 같은 기대) |
| v05 전부 + 0.4 관련(T17 포함) | **297 passed · 1 skipped** |
| `ruff check clinic_chat/consult/` + 손댄 시험 | 통과 |

## 남은 것

- 실물 대화는 이번에 돌리지 않았다(발주 = 시험 줄). 실물 a7d7e253 10 턴은 O-14 뒤에도 규칙상 같은 길이다(시나리오 시험이 그대로 통과). 9 턴 「아까 미간 보톡스는 제오민이 나아?」 는 이제 1b 로 ② 에 돌아간다(같은 값 미간 · 보톡스).
- 가격 낱말 목록과 프롬프트 pick 규칙 18(정보 질문)은 초안이다.

---

## 덧붙임(코디 11-22 · O-14 에 같이) — 스펙 0.3.1 확정 둘 + 화면 둘

### 스펙 0.3.1 확정 둘 — 코드는 이미 그 꼴(시험 줄만 더함)

| 확정 | 코드 | 시험 |
|---|---|---|
| (1) 지금 주제에도 같은 값이 있으면 되돌리지 않고 지금 주제를 깊게 | 1b 는 `not holds(turn, 지금 주제)` 일 때만 탄다 | `test_o14_spec031_current_holds_same_value_stays` — ① 팔자주름 · 보톡스 / ② 미간주름 · 보톡스(지금) → 「보톡스 + 제오민」 → ② 깊게 |
| (2) 이번 턴이 좁힘 칸(제품 · 효과 · 국가 · 회차)만이면 같은 값 되돌림 안 씀 | `holds` 는 부위 · 고민 · 시술 값이 하나 이상 있어야 참 | `test_o14_spec031_narrow_only_turn_never_returns` — ① 미간주름 · 보톡스 · 제오민 / ② 팔자주름(지금) → 「제오민」 → ② 깊게 · `holds` 거짓 |

### 화면 ① 점 클릭 표시 = 시안 `cs-dot__ring` 웨이브

- `marks.html`: 누른 점(`iv.site`)의 자리마다 그 점 뒤에 `<circle class="cs-dot__ring" data-ring-for r=16>` 를 그린다. pair 면 둘 다 그린다. 시안 줄 365 ~ 367 의 `cs-ring` 애니메이션은 앱 CSS 에 이미 있다(움직임 줄임 설정이면 멈춤).
- `consult.css`: `.cs-dot[aria-pressed="true"]` 의 까만 채움을 없앴다. 지금은 primary 채움 + 흰 테두리 3(시안 `cs-dot--pick` 꼴)이다. 몸 이름 칩(`.cs-label`)은 그대로다.
- 다른 점은 그대로다(링 0). 같은 점을 다시 누르면 링도 사라진다(서버 조각).
- 시험: `test_click_filters_and_other_dots_stay` 에 링 단언 셋을 더했다(누른 점만 · 좌표 · 거름 없는 목록은 링 0).
- 실물(18294 · `fixAreal00000002` · 턱 누름): 링 = `SITE-072` 하나 · 점 둘 그대로 · 누른 점 채움 `rgb(32,200,214)`(primary).
- 스크린숏 `e2e-shots/o14-dot-ring.png`: 링은 퍼지며 사라지는 애니메이션이라, 찍힌 순간에 거의 투명할 수 있다. DOM 에는 있다.

### 화면 ② 진행 단계 = 스피너 + 한 줄(gui-feedback F5)

- `steps.html`: 목록(`ol` 4 줄 · 체크)을 **`p.cs-steps.cs-steps--one` 한 줄**(스피너 하나 + 지금 단계 글)로 바꿨다.
  - 지금 단계 = 진행 중 단계, 없으면 마지막 단계(목록 뒤 · 답 전 틈에도 줄이 남음).
  - 문구는 `prompts/consult.json` `steps` 그대로다(새 문구 0).
  - 턴이 끝나면 숨은 표지 하나(`span.cs-step-end` — 빈 SSE 자료는 브라우저가 버리므로 `live.py` 가 막음).
- `steps.py`: `finish()` 가 `ended` 를 켠다. `view()` 의 마지막 칸 `end`.
- `consult.css`:
  - 답 글이 오기 시작하면(답 자리 스피너가 사라지면) 단계 줄을 숨긴다(`.cs-step:has(~ .cs-answer:not(:has([data-cs-spinner])))`).
  - **스피너 둘 → 하나**: 원인은 답 자리 자리표시 스피너(`turn.html` `data-cs-spinner`)와 단계 줄 스피너가 함께 보이던 것이다. 단계 줄이 있는 동안 답 자리 스피너를 숨긴다.
- 실물(같은 대화 · 「가격은 얼마예요?」 · 0.5 초마다 관찰):
  - 줄이 「질문을 이해하고 있어요」 → 「관련 시술을 찾고 있어요」 → 「답변을 작성하고 있어요」 로 바뀐다. 보이는 스피너는 늘 1 이다.
  - 답이 오면 줄이 사라진다(스피너 0).
  - 스크린숏 `e2e-shots/o14-steps-1.png` · `-2` · `-3`.
- 시험: `test_step_labels_from_prompt_file_and_render`(한 줄 · 스피너 하나 · 끝난 단계 글 0 · 목록 뒤 틈 · 턴 끝 줄 0) · `test_fake_stream_has_steps_spinner_and_cumulative_markdown`(네 단계 글이 차례로 지나감 · 끝 = 숨은 표지).

### 시험 · 손댄 파일(덧붙임)

- 관련 **299 passed · 1 skipped** · ruff 통과 · T17(템플릿 · 코드 한글 0).
- 파일: `topics.py`(앞 판) · `steps.py` · `templates/partials/steps.html` · `templates/partials/marks.html` · `static/consult.css` · `tests/test_v05_topic_tuple.py` · `tests/test_v05_fix_a.py` · `tests/test_consult_chat_ui.py`.
- 서버: 18294 실물 확인 뒤 끔 · 18105 · 18222 손 안 댐.
