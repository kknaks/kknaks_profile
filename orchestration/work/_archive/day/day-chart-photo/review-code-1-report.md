# 리뷰 리포트 — day-chart-photo / code (WP① 탭 저장 · WP③ 모달 화면) (2026-11-24)

- 대상: 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-chart-photo` 미커밋 변경(`git diff origin/dev` 55 파일 +1964/−2000 · 새 파일 7)
- 근거: SPEC-002 개정 ㉘ 규칙 31 · U-14 · API(커밋 `a896cda0`) · SPEC-001 개정 ⑫ · 결정 C1 ~ C17 · 계약 K1 ~ K5 + 보충 1 · 2 · 레포 `AGENTS.md`
- read-only. 파일 수정 없음.

## 판정: WARN

FAIL 은 없다. 계약 K1 ~ K5 · 보충 1 · 2 와 규칙 31 검사 순서는 코드가 글자 그대로 따른다. 관문 3개 모두 통과.
다만 **실물에서 「다시 [저장]」이 또 걸리면서 글이 두 번 붙는 길**이 둘 있다(W1 · W2). 테스트에서는 이 길이 보이지 않는다.
W1 은 SPEC 문장(「`baseLogId` 는 DAY 쪽 판정으로 그대로 둔다」)을 그대로 구현해서 생긴다. 그래서 **사용자 확인 필요**로 따로 올린다.

## 관문 명령(1회씩)

| 명령 | 결과 |
|---|---|
| `scripts/test.sh -q backend/tests/day/board backend/tests/day/web` | **419 passed** (52.97s · exit 0) |
| `cd backend && uv run ruff check day tests` | All checks passed |
| `cd scripts/frontend && npm run -s check` | node tests 117 pass · 0 fail (CSS 재현 · lint · format 포함) |

## FAIL

없음.

## WARN

### W1 (높음 · 사용자 확인 필요) KOS 충돌 뒤 동기화가 KOS 이력을 먼저 쌓으면, 다시 [저장]이 DAY 쪽에서 또 걸리고 KOS 글이 두 번 붙는다
- 위치: `backend/day/policies/board_chart_tabs.py:48` · `:52` · `:61` (`day_hit = row.base_log_id != last_log_id` · 걸린 줄 `base_log_id=last_log_id`) · `backend/day/emr/sync_tasks.py:352-369`(규칙 32 ② — KOS 글 ≠ DAY 사본이면 `source=kos` 이력 1줄)
- 순서: 창 열기 → KOS 웹에서 같은 줄 메모 수정 → 10초 조회 **전에** DAY [저장] → 409(KOS 쪽만 걸림 · 응답 `baseLogId` = 옛 이력 id · `base` = KOS 글) → 10초 조회가 `source=kos` 이력을 더함(마지막 이력 id 바뀜) → 사용자가 이어 붙인 글을 읽고 다시 [저장] → `day_hit` → 또 409 · 글 = `KOS 글\nKOS 글\n내 글`.
- 근거: C17 「그 상태로 다시 저장 → 같은 확인 후 저장」 · 규칙 31 ③ 「같은 줄이 계속 걸리지 않게」. 코드는 규칙 31 의 「`baseLogId` 는 DAY 쪽 판정으로 그대로 둔다」를 그대로 따른다. 문제는 SPEC 이 이 틈을 다루지 않는다는 데 있다.
- 조용히 통과하는 자리: `test_board_chart_api.py:414` `test_A2_KOS_지금_값이_연_때와_다르면_409_…_다시_저장` 은 두 저장 사이에 동기화가 없다(FakeKos). 그래서 초록이다.
- 실물 e2e ⓑ 는 KOS 수정과 DAY [저장] 사이 간격이 10초보다 짧은지 긴지에 따라 결과가 갈린다.
- 정할 것(사용자): 예를 들어 DAY 쪽 판정에서 「요청 `baseLogId` 뒤의 이력이 모두 `source=kos` 이고 마지막 글이 요청 `baseBody` 와 같으면 걸리지 않음」으로 볼지 정해야 한다. 아니면 지금대로 두고 이 동작을 받아들인다.

### W2 (중간) 응답 유실 · 타임아웃 뒤 다시 [저장] = 자기 글과 409 · 글이 두 번 붙음. 지운 검증이 지키던 성질이 옮겨지지 않았다
- 위치: `backend/day/static/day.js:1484-1494`(`htmx:afterRequest` — 실패 · 타임아웃이면 form 그대로 · 바뀐 줄 유지) · `partials/board_chart_parts.html:82`(`timeout 15000`) · `policies/board_chart_tabs.py:48`
- 순서: [저장] → 서버는 commit 했으나 응답을 잃음(15초 타임아웃 · 네트워크 끊김 · 커밋 뒤 500) → 화면은 옛 `baseLogId` 를 가진 채 「바뀐 줄」 → 다시 [저장] → DAY 쪽에서 걸려 409 → 글 = `내 글\n내 글`.
- 지운 것: `scripts/frontend/tests/chart-recovery.test.mjs`(「a lost ACK is reconciled…」 · 「HTTP 500 after a commit is reconciled…」 · 「an exact duplicate conflict acknowledges…」) · `verification_faults.py`(처리 중 타임아웃). 지운 이유는 「명시적 저장으로 그 경로가 없어짐」(`README.md:197-198` · be-1-report)이다. 그러나 **커밋 뒤 응답 유실 경로는 명시적 저장에도 남아 있다.** 지금 남은 테스트는 「저장 0 · 바뀐 줄 유지」까지만 본다. 「다시 저장하면 어떻게 되나」는 아무 테스트도 보지 않는다.
- 서버 쪽 동시성 성질(동시 저장 · 커밋 뒤 응답 순서 · 커밋 뒤 취소)은 `test_chart_acknowledgement.py:43` · `:76` · `test_chart_recovery.py:18` · `tests/verification/concurrency.py`(`visit.chart_save`)로 옮겨졌다. 이 부분은 PASS.
- 고칠 방향(제안 · 결정 필요): ⓐ 판정에서 요청 글 · 담당자가 마지막 이력(작성자 = 세션 직원 · `source=day`)과 같으면 걸리지 않음으로 본다(옛 「exact duplicate」 성질과 같음). ⓑ 아니면 실패 안내 문구로 처리한다. fe-1-report 미결(「실패 안내 WORK 결정」)과 같은 문제다.

### W3 (중간) 저장 요청이 나가 있는 동안 친 글은 200 응답이 form 을 통째로 바꾸면서 말없이 사라진다
- 위치: `partials/board_chart_parts.html:82`(`target='this' swap='outerHTML'` · `disabled='find button'` — 글 칸은 잠기지 않음) · `day.js:1484-1494`(새 form 의 기준값을 응답 값으로 다시 잡음 → 사라진 글은 「바뀐 줄」로도 안 남음 → 닫기 경고도 안 뜸)
- 보낸 줄에 덧붙인 글, 보내지 않은 줄에 새로 친 글 모두 사라진다. 지운 테스트 「a delayed save queues the next edit…」 · 「returning to the original text while a save is pending…」가 지키던 「보내는 중 새 입력」 성질이 명시적 저장에서는 아예 다뤄지지 않는다.
- 근거: C5(저장 안 한 글을 말없이 잃지 않음 — 닫기 경고의 취지) · U-14 E57 「보내는 동안 꺼짐」은 버튼만 다룬다.
- 제안: 보내는 동안 그 탭 글 · 담당자 칸을 잠근다(readonly). 아니면 응답 뒤에도 보낸 뒤 바뀐 줄을 남긴다.

### W4 (중간) KOS 메모에 CR(`\r\n`)이 있으면 그 줄은 늘 KOS 충돌에 걸린다
- 위치: `partials/board_chart_parts.html:67`(`<input type="hidden" name="baseBody" value="…">`) · `emr/kos/mapper_values.py:10`(`text` = strip 만 · CR 그대로 저장) · `policies/board_chart_tabs.py:25`
- HTML 파서는 속성 값의 `\r\n` 을 `\n` 으로 바꾼다. 그래서 돌아오는 `baseBody` 는 `a\nb` 이고, KOS 지금 값은 `a\r\nb` 다. 결과는 409 다. 걸린 응답도 같은 hidden 칸으로 그리므로 다시 [저장]해도 또 걸린다(끝나지 않는 409).
- 근거: 규칙 31 「글은 앞뒤 빈칸을 뺀 값」. 줄바꿈 정규화는 SPEC 에 없어 **결정 필요**다. 제안은 `chart_text` 에서 `\r\n`·`\r` → `\n`.
- 확인: KOS 웹 · KOS 데스크톱이 메모를 CRLF 로 저장하는지 실물에서 1회 본다(아래 e2e ⑨).

### W5 (낮음) 의사 집도의 기준값 — DAY 사본과 KOS 지금 값의 「한 명」 기준이 서로 다르다
- 위치: `policies/board_chart_rules.py`(`chart_base` — `t.doctor_ids` = 매핑된 직원만 · `queries/board.py:322`) vs `services/board_charts.py:149-162`(`_kos_values` — KOS 외부 id 개수로 「한 명」을 판단한 뒤 매핑)
- KOS 집도의가 둘이고 그중 하나가 DAY 직원으로 매핑되지 않으면 이렇게 된다. DAY 기준값은 매핑된 그 한 명이고, KOS 지금 값은 None 이다. 그래서 첫 [저장]이 한 번 걸리고 글이 붙는다(두 번째는 통과). 매핑되지 않은 시스템 계정이 KOS 집도의로 남은 줄(규칙 34 「바로 시작」)도 확인할 대상이다.
- 근거: 규칙 31 「한 명이 아니면 없음 — `mapper.single` 과 같은 규칙」. 두 쪽 모두 같은 단계(매핑 전 개수)를 써야 한다.

### W6 (낮음) 문서에 자동 저장 문장이 남아 있다
- `.agents/skills/verify-day-web/SKILL.md:130` 「입력·자동 저장·닫기·재열기·빈 값 저장을 담는다」 — 영상 증거 범위 문장이다(fe-1-report 미결에도 적혀 있음). `verification_video.py` 는 이미 [저장] 클릭으로 바뀌었다.
- `README.md:197-198` 「그 경로가 없어져 지웠다」 — W2 때문에 사실과 다르다. 응답 유실 경로는 남아 있다.

### W7 (낮음) 오류 코드 글자를 코드에 직접 썼다
- `services/board_charts.py:223` `"staff_not_listed"` — 같은 줄의 `ErrorCode.DOCTOR_NOT_LISTED` 처럼 `common/error_codes.py` 에 상수가 없다. 계약 글자는 맞다(K3). 다만 오타를 막는 장치가 없다.

## PASS — 항목별 대조

### 6-1 C17 판정
| 항목 | 위치 | 판정 |
|---|---|---|
| 검사 순서 400 → 404 → KOS 읽기 → 잠금 → 충돌 → 담당자 → 그대로 건너뜀 → 저장 | `routers/board.py:443-488`(400 칸 수 · chart) · `services/board_charts.py:184-229` | PASS(규칙 31) |
| KOS 읽기 = transaction 밖 · 요청당 1회 · `fetch_visit_tasks` · 시스템 계정 | `board_charts.py:89-118`(`session.rollback()` 뒤 호출) · 테스트 `test_board_chart_api.py:494` | PASS |
| 걸리면 이력 · outbox · event 0(rollback) | `board_charts.py:212-214` · 테스트 `:377` · `:414` | PASS |
| 이어 붙인 글 = 지금 글 + `\n` + 요청 글 · 지금 글 없으면 요청 글만 | `board_chart_tabs.py:13-20` | PASS(OQ-91 기본값) |
| 담당자 = 의사 KOS 값 · 간호관리 요청 그대로 | `board_chart_tabs.py:53-55` | PASS |
| 안 보낸 줄 KOS 판정 안 함 · 응답은 지금 DAY 값 | `_rows_of` 가 보낸 줄만 · `board_chart_reads.py` `chart_tab_view` | PASS |
| KOS 실패(연결 없음 · 일정 id 없음 · EmrError) = DAY 쪽만 | `board_charts.py:106-118` · 테스트 `:465` | PASS |
| 시술 전 의사차트 · 반영 대기 줄 KOS 판정 안 함 | `board_charts.py:198-201` · `_GUARD_FIELDS` | PASS |
| 길이 검사 없음 | — | PASS(OQ-90 ⓒ) |

### 6-2 저장
| 항목 | 위치 | 판정 |
|---|---|---|
| 방문 잠금 · transaction 1 | `board_charts.py:191`(`_world`) · `:252`(`_finish`) | PASS |
| `visit.chart_save` 1행(payload chart · taskIds) · outbox 전부 그 event 에 · 줄 순서 | `:230-247` · `_rows_of` 규칙 2 순서 · 테스트 `:179` | PASS(W1 — SPEC 검수 지적) |
| 규칙 27 `task.doctor_change` 줄마다(수락 · 진행중) · 완료 = 집도의만 | `:300-306` · 테스트 `:257` | PASS |
| 그대로인 줄 건너뜀 · 전부 그대로면 event 0 | `:225-228` · 테스트 `:234` | PASS |
| 담당자 없음 · 목록 밖 = 탭 전체 409 · 충돌이 먼저 | `:212-224` · 테스트 `:287` | PASS(OQ-83 ⓑ) |
| 시술 전 의사차트 결정 (가) 그대로 | `:298-299` · 테스트 `:521` · `:548` · `:569` | PASS |
| 잠금 안에서 응답 값 확정(커밋 뒤 다른 편집자 이력을 자기 응답으로 안 돌림) | `:250-251` · 테스트 `test_chart_acknowledgement.py:43` | PASS |

### 6-3 화면
| 항목 | 위치 | 판정 |
|---|---|---|
| 자동 저장 경로 0 (blur · input 타이머 · 2초) | `day.js` 검색: 차트에 `setTimeout` · `focusout` 저장 없음(`:1591` 2000 = 토스트 숨김) · 테스트 `controllers.test.mjs:255` · `chart-save.test.mjs:74` | PASS |
| [저장] 차트 탭만 · 바뀐 줄 있을 때만 · 보내는 동안 꺼짐 · 보기 권한 숨김 | `board_chart_parts.html:42-49` · `day.js:1428-1439` | PASS |
| 바뀐 줄만 전송(안 바뀐 줄 칸 disabled → 복원) | `day.js:1440-1458` · `chart-save.test.mjs:94` | PASS(K2) |
| 409 `chart_conflict` 조각 교체 · 보낸 줄 dirty 유지 | `day.js:1215-1220`(X-Day-Error 4xx 끼우기) · `:1466-1483` · `chart-save.test.mjs:149` | PASS(K3) |
| 그 밖 오류 = 토스트 · form 그대로 | `day.js:1480` | PASS |
| 확인 창 ✕ · Esc = 창 · 바깥 = 무동작 · 「계속 쓰기」 · 「버리고 닫기」 | `day.js:1496-1561` · `board_chart_parts.html:91-103` | PASS(글자 = 기획 4-2 · OQ-79). 확인 창 동작은 node 테스트가 없다 — 실물 e2e ⑤ 로 본다 |
| 「최근 저장」 탭마다 · OOB | `board_chart_parts.html:30-38` · `board_chart_tab.html:9` | PASS(W9) |
| 헤더 「이름 직군」 · `header_staff` · 둘 이상 = None | `session.py:124-133` · `web.py:224` · `base.html:55-60` · `test_header_staff.py` | PASS(보충 1). 전체 페이지(board · reservations · kit)가 모두 `required_web_view` 를 거친다 |
| 인라인 script · style 0 · 지어 넣은 글자 0 | 새 템플릿 3개 검색 결과 0 · 사진 탭 버튼 글자 · aria-label 없음(OQ-88 — 짓지 않음) | PASS |
| `board_chart_saved.html` 지움 · 옛 `/board/tasks/{id}/chart` · `/api/tasks/{id}/chart` 지움 | 테스트 `test_board_chart_api.py:627` · `architecture/test_api_contracts.py` | PASS(K5) |
| 계층: router 가 DB 를 안 만짐 · 정책은 순수 | `policies/board_chart_tabs.py`(값만) · 라우터 `_chart_rows` 파싱만 | PASS |

### 6-4 지운 테스트 · 검증 스크립트
| 지운 것 | 지키던 성질 | 남는가 | 판정 |
|---|---|---|---|
| `verification_chart_races.py` | 동시 저장 · 잠금 | `tests/verification/concurrency.py`(탭 경로 · `visit.chart_save`) · `test_chart_acknowledgement.py` | PASS |
| `verification_faults.py` | 늦은 요청 · 처리 중 타임아웃 | 서버 쪽 커밋 뒤 취소는 남음. **화면의 응답 유실 → 다시 저장** 성질은 없음 | **W2** |
| `chart-recovery.test.mjs` | 응답 유실 복구 · 보내는 중 재입력 · 실패 뒤 닫기 · 같은 글 중복 인정 | 「실패면 dirty 유지」만 남음. 재입력 · 중복 인정은 없음 | **W2 · W3** |
| `test_chart_text_contract.py` | day.js `chartConfirmed` 와 서버 trim 일치 | 이제 화면은 글을 비교하지 않는다(서버 `chart_text` 하나). 지운 이유가 맞다 | PASS(CR 정규화는 W4) |

## 조용히 통과하는 자리
1. **W1** — FakeKos 테스트에는 두 저장 사이의 동기화가 없다. 실물에서는 10초 조회가 이력 id 를 바꾼다.
2. **W2** — 「실패면 form 그대로」는 테스트가 있다. 「커밋된 뒤 실패 → 다시 저장」은 아무 테스트도 보지 않는다.
3. **W4** — 테스트 데이터에 CR 이 없다. hidden 칸의 HTML 정규화는 pytest(값 직접 전달)에서 드러나지 않는다.
4. **사진 탭** — `GET /board/visits/{id}/photos` 라우트가 아직 없다(WP② 범위 밖). 템플릿 테스트(`test_board_page_chart_photos.py`)는 가짜 값으로 조각만 그린다. 실물에서 사진 탭을 누르면 404 오류 토스트가 뜬다 — 지금 단계에서는 예상된 동작이다.
5. `be-1-report` 미결 ① — 브라우저 · TLC · Lean 이 필요한 검증(`verification_journeys` · `video` · `cases closed-dialog` · formal)은 돌리지 않았다. closed-dialog 대조군은 `day.js:1503` 줄 글자에 묶여 있다.

## 직원이 실물에서 만날 자리 — 로컬 e2e 체크리스트(KOS 데모 지점 · 시험 고객)
1. ⓐ 간호관리 여러 줄 → [저장] 1회 → 요청 1개 · 바뀐 줄만(DevTools 폼 칸) · 「최근 저장」 그 탭만 바뀜 · KOS 메모 = 쓴 글
2. 의사차트 탭 따로 [저장] → 간호관리 「최근 저장」 그대로
3. ⓑ 충돌 **두 갈래**: (i) KOS 수정 후 10초 넘게 기다렸다가 DAY [저장] → 409 → 다시 [저장] → 200 (ii) KOS 수정 직후(10초 안) DAY [저장] → 409 → 15초 기다린 뒤 다시 [저장] → **W1: 또 409 · KOS 글이 두 번 붙는지** 본다
4. 수락 · 진행중 줄 의사차트 집도의 변경 → [저장] → 판 카드 · 원장 상태 갱신 · KOS 집도의 → 메모 순서
5. ⓓ 미저장 ✕ · Esc → 확인 창 · 바깥 누르기 → 아무 일 없음 · 「계속 쓰기」 → 글 그대로 · 「버리고 닫기」 → 요청 0 · 미저장 없으면 ✕ 바로 닫힘
6. 탭 옮겨도 쓴 글 남음 · 다른 탭이 미저장이어도 닫기 경고가 뜸
7. **W3**: [저장] 직후(응답 전) 다른 줄에 글 입력 → 응답 뒤 그 글이 남는지
8. **W2**: [저장] 직후 네트워크 끊기(DevTools offline) → 다시 연결 → [저장] → 409 · 글 두 번 붙는지
9. **W4**: KOS 에서 여러 줄 메모(줄바꿈) 저장 → DAY 동기화 뒤 그 줄 [저장] → 409 가 끝없이 나는지
10. 담당자 비운 줄 → [저장] → 오류 토스트 · form 그대로 · 저장 0
11. 보기 권한 계정 → [저장] 없음 · 글 칸 읽기만
12. 헤더 「이름 직군」 — 간호 · 원장 · 직군 둘 이상(이름만) · 판 · 예약 · kit 화면
13. 사진 탭 누르기 → (WP② 전) 404 토스트 — 화면이 깨지지 않는지만 본다

## 사용자 확인 필요(결정 문제 — SPEC 재논의 아님 · 기록만)
- W1: KOS 충돌 뒤 동기화로 생긴 `source=kos` 이력을 DAY 쪽 판정에서 어떻게 볼지(SPEC 규칙 31 「`baseLogId` 그대로」의 틈)
- W2: 응답 유실 뒤 다시 저장 — 같은 글이면 걸리지 않음으로 볼지, 아니면 안내 문구로 처리할지
- W4: 줄바꿈 정규화(CRLF → LF)를 비교 · 저장 규칙에 넣을지

## 참고(기존 부채 · 무관)
- 저장 한 번에 판 전체 읽기 `load_world` 가 3번 돈다(잠금 전 404 확인 · 잠금 안 · 응답용). 집도의를 바꾸면 `board()` 1번이 더 돈다(`board_charts.py:188` · `:191` · `:250`). 성능 회귀 측정은 하지 않았다.
- `board_messages.py` 의 `chart_conflict` 옛 글자가 남아 있다(라우트는 `message=""` · OQ-90) — be-1-report 미결 ③.
