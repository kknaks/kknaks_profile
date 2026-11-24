# 리뷰 리포트 — day-chart-photo / code 재검수 2 (WP① · ③ 고침 · review-code-1 W1 ~ W7) (2026-11-24)

- 대상: 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-chart-photo` 미커밋 변경(be-fix-1 · fe-fix-2 반영 뒤)
- 근거: 결정 C18 · C19 · C20 · C21-기본값(매핑 뒤 DAY 직원 수) · SPEC-002 규칙 31(mediness `b2005927`) · review-code-1
- read-only. 파일 수정 없음.

## 판정: PASS (WARN 2 · 낮음)

W1 ~ W7 은 모두 결정대로 닫혔다. 브리프가 든 네 가지 틈(동기화 뒤 다시 저장 · 응답 유실 · CRLF · 보내는 중 잠금)은 각각 그 틈을 직접 재현하는 테스트가 덮는다.
새로 생긴 어긋남은 둘이고 둘 다 낮음이다. 하나는 의사차트에서만 C18 이 빗나갈 수 있는 경우(N1), 다른 하나는 README 의 테스트 파일 이름(N2)이다.

## 관문 명령(1회씩)

| 명령 | 결과 |
|---|---|
| `scripts/test.sh -q backend/tests/day/board backend/tests/day/web` | **421 passed** (61.58s · exit 0) |
| `cd backend && uv run ruff check day tests` | All checks passed |
| `cd scripts/frontend && npm run -s check` | 118 pass · 0 fail |

## W1 ~ W7 닫힘 확인

| 앞 지적 | 결정 | 고친 곳 | 덮는 테스트 | 판정 |
|---|---|---|---|---|
| W1 동기화 뒤 다시 저장이 또 걸려 글 두 번 | C18 | `backend/day/policies/board_chart_tabs.py:46-61` `day_differs` — `baseLogId` 뒤가 전부 `source=kos` 이고 마지막 글(+집도의) = 요청 `base` 면 안 걸림 · 모르는 `baseLogId` = 걸림 · `baseLogId` 없음 = 이력 전부가 뒤 이력 · 입력 = `services/board_charts.py` `_history`(잠금 안 · `revision` 순) | `tests/day/board/test_board_chart_conflicts.py:127` `test_C18_충돌_뒤_동기화_KOS_이력이_쌓여도_다시_저장은_200_글_한_번` — 409 → 실제 DB 에 `source=kos` 이력 + 사본 넣음 → 걸린 응답 값 그대로 다시 저장 → 200 · 이력 = `[KOS 글, KOS 글\n내 글]`(글 한 번) · 순수 `test_board_chart_tabs_policy.py:136` | PASS |
| W2 응답 유실 뒤 다시 저장 = 자기 글과 409 | C19 | `board_chart_tabs.py:33-43` `already_saved`(세션 직원 · `source=day` · 같은 글(C20) · 같은 담당자) · `:85` 첫 단계(DAY · KOS 판정 안 함) → `board_charts.py` `changed` 에서 그대로라 저장 0 | `test_board_chart_conflicts.py:165` `test_C19_커밋_뒤_응답_유실_같은_요청_다시_보내면_200_이력_1개` — 두 줄 200 → 옛 `baseLogId` 로 같은 요청 → 200 · 이력 각 1 · `visit.chart_save` 1 · outbox 그대로 · 같은 직원이라도 다른 글이면 409 · 순수 `:153` | PASS |
| W3 보내는 중 친 글이 말없이 사라짐 | C21-기본값 | `backend/day/static/day.js:1442-1448` `chartLock`(글 칸 `readOnly` · 담당자 트리거 `disabled` · `aria-busy`) · `:1460` 요청 **전에** 잠금 · `:1499` 응답 뒤 form 이 남았으면(실패 · 넘김 · 오류 토스트) 풀기 — 기준값은 다시 잡지 않아 바뀐 줄 유지 · 200 · 409 는 새 form(잠금 없음) | `scripts/frontend/tests/chart-save.test.mjs:162` 「while a save is in flight the tab's text and staff fields are locked; the response handler unlocks a kept form」 · `:94` 잠금 → trigger 순서 · `backend/tests/day/web/test_board_page_chart_controller.py` | PASS |
| W4 CRLF 줄이 끝없이 409 | C20 | `board_chart_tabs.py:11-13` `chart_text` — `\r\n` · `\r` → `\n` 뒤 strip. 기준값(`chart_base`) · KOS 지금 값(`_kos_values`) · 요청 · 이력 비교 · 저장 글이 모두 이 함수를 쓴다 | 순수 `test_board_chart_tabs_policy.py:88` `test_글_정규화_줄바꿈_앞뒤_빈칸` · `:103` `test_C20_KOS_글이_CRLF_여도_같은_글이면_안_걸림` | PASS — hidden 칸이 `\n` 으로 바꿔 돌려보내도 서버 양쪽이 LF 라 같다. HTML 을 거치는 e2e 테스트는 없다 → 실물 ⑨ |
| W5 집도의 「한 명」 기준 차이 | C21-기본값(매핑 뒤 DAY 직원 수) | `services/board_charts.py` `_kos_values` — 매핑 먼저 → 매핑된 직원이 한 명일 때만 · `chart_base` = `t.doctor_ids`(매핑된 집도의만) 그대로 → 두 쪽 같은 단계 | 기존 `test_A2_의사차트_KOS_집도의가_바뀌었으면_409_담당자는_KOS_값`(`test_board_chart_conflicts.py:109`) — 「둘 중 하나 매핑 안 됨」 전용 테스트는 없음 | PASS(결정대로) · 아래 N1 |
| W6 문서의 자동 저장 문장 | — | `.agents/skills/verify-day-web/SKILL.md:130` 「입력·[저장]·닫기」 · `README.md:197-200` 응답 유실은 남고 C19 로 200 | — | PASS · 아래 N2 |
| W7 `"staff_not_listed"` 문자열 | — | `backend/common/error_codes.py:50` `STAFF_NOT_LISTED` · `board_charts.py` 가 씀 | — | PASS |

규칙 31 ⓑ 새 순서(SPEC `b2005927`: 이미 저장됨(C19) → DAY 쪽(C18 단서) → KOS 쪽(C20) → 걸리면 409 → 담당자)는 `judge_row` `:84-90` 와 `save_chart_tab` 의 순서가 그대로 따른다. **같음.**

## WARN (새 어긋남)

### N1 (낮음) 의사차트 C18 — 동기화 이력의 집도의는 「한 명일 때만」 규칙을 따르지 않아, 집도의가 둘이거나 매핑되지 않으면 다시 저장이 또 걸린다
- 위치: `backend/day/emr/sync_tasks.py:354` · `:361-365`(의사 `source=kos` 이력 `staff_id` = 매핑된 **첫** 집도의, 없으면 앞 이력 담당자 `last_staff`) vs `policies/board_chart_tabs.py:61`(`newest.staff_id` 를 요청 `base.doctorStaffId` 와 비교) · `base.doctorStaffId` = `_kos_values` 의 「매핑 뒤 한 명일 때만 · 아니면 None」(C21).
- 순서: 의사차트 줄에서 KOS 집도의가 둘(둘 다 매핑) 또는 매핑 안 된 사람 → KOS 충돌 409(응답 `base.doctorStaffId = None`) → 동기화가 `source=kos` 이력을 더함(`staff_id` = 첫 집도의, 또는 앞 담당자) → 다시 [저장] → `kos_differs` 가 None ≠ 직원 → 또 409 · 글 = `KOS 글\nKOS 글\n내 글`. 세 번째 저장은 통과한다(`baseLogId` 가 동기화 이력으로 옮겨감).
- 근거: C18 「마지막 글(+집도의)이 요청 `base` 와 같으면」 · C21-기본값 「두 쪽 같은 단계」 — 셋째 쪽(동기화 이력 담당자)이 다른 규칙을 쓴다. 간호관리차트는 집도의를 비교하지 않아 해당이 없다. 동기화 코드는 이번 WP 범위 밖(diff 없음)이므로 기존 규칙과의 맞물림 문제다.
- 고칠 방향(제안): C18 의 의사 비교에서 동기화 이력 담당자 대신 그때 DAY 사본(`chart_base`)을 쓴다. 아니면 C18 비교를 글만으로 한정한다(집도의 차이는 KOS 쪽 판정이 이미 본다). 결정 필요 — 드문 경우라 다음 고침에 넘겨도 된다.

### N2 (낮음) README 가 C18 · C19 테스트 파일 이름을 틀리게 적었다
- `README.md:200` 「`test_board_chart_api.py` 의 C19 · 동기화 뒤 다시 저장(C18) 테스트」 — 실제로는 `backend/tests/day/board/test_board_chart_conflicts.py:127` · `:165`(700줄 제한 때문에 나눈 파일).

## 고침이 만든 다른 영향(확인 · 지적 아님)
- C20 은 비교뿐 아니라 **저장 글**도 LF 로 만든다(`_save_row` → `chart_text`). KOS 로 나가는 메모도 LF 다. KOS 가 받은 글을 CRLF 로 바꿔 돌려주는 경우 동기화가 `source=kos` 이력을 한 번 더한다. 그다음 저장은 C18 · C20 이 처리한다. be-fix-1 보고의 「코디가 확인할 것」과 같다.
- C19 는 KOS 판정도 건너뛴다(SPEC 그대로). 같은 직원이 같은 글을 다시 보낼 때, 그사이 KOS 가 바뀌었는데 아직 동기화 전이면 저장 0 · 200 이다. KOS 값은 다음 조회가 DAY 로 가져온다(규칙 32 ②). 결정 문장 그대로다.
- `chartLock` 은 `htmx:afterRequest` 로만 풀린다. 요청이 아예 나가지 않으면(htmx 가 요청을 취소하는 경우) 잠긴 채로 남는다. 지금 그 form 에는 `hx-confirm` 이나 validation 이 없어 이 길이 없다. 확인만 한다.
- 정형 결속(`verification_binding.py` · `source-map.json` · `day_differs` 극성)은 be-fix-1 보고대로다. TLC · 브라우저 검증은 실행하지 않았다(pending — 범위 밖).

## 직원이 실물에서 만날 자리 — 로컬 e2e 에서 더 볼 것(review-code-1 체크리스트에 더함)
1. ⓑ-(ii) KOS 수정 직후(10초 안) DAY [저장] → 409 → 15초 뒤 다시 [저장] → **200 · KOS 글 한 번**(C18)
2. [저장] 직후 오프라인 → 다시 연결 → 같은 [저장] → **200 · 이력 1**(C19)
3. KOS 에서 여러 줄 메모 → 동기화 뒤 그 줄 [저장] → **409 아님**(C20)
4. [저장]을 누르고 응답 전에 글 칸에 입력 → **입력 안 됨** · 응답 뒤 풀림 · 오프라인 실패면 풀리고 [저장] 켜짐(C21-기본값)
5. (N1) 집도의가 둘인 의사차트 줄 — KOS 충돌 뒤 동기화가 지나고 다시 [저장] → 또 409 가 나는지

## 범위 밖
- 사진 서버(WP②) — 사진 탭 404 토스트는 예상된 동작이다.
