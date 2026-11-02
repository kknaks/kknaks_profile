# 리뷰 리포트 — strong-hajin-polish2 / backend · WORK-009 Phase 1 재검수 fix1 (2026-10-02)

## 판정: WARN

앞 판의 F1·W1~W4 가 **전부 닫혔다**. 새로 생긴 FAIL 은 없다. 경미 1건이 남는다. 서버가 첨부 자료 ID 목록을 **순서까지 같은지** 비교한다는 점이다. 지금 FE 는 저장·등록 둘 다 정렬한 같은 목록을 실어서 문제가 드러나지 않는다. 그 밖의 호출자에게만 해당한다 — 다음 단계(커밋·verify)로 넘어가도 된다.

## 검수 범위

- 대상: `backend/` + `docs/unified-operations-inventory.json` 미커밋 변경 전체(fix1 반영 후). 수정 21파일 + 새 `tests/contract/test_task_due_date_fill.py`. +800 / −97. `frontend/`(`4789647` 커밋)는 FE 페이로드 확인용으로 읽기만 했다
- 기준: 앞 리포트 `review-be-p1-report.md` · 지시서 `strong-hajin-polish2-be-p1-fix1-brief.md` · 앞 판 기준(WP Phase 1 · SPEC · add1)
- 실행한 검사
  - 백엔드 소스 「기한」 grep(주석 제외)
  - **`COMMAND_CONTRACTS` 모든 모델의 JSON 스키마를 재귀로 돌며 `title` 에 「기한」이 든 곳을 실제로 출력 → 0**
  - inventory 의 「기한」 grep → 0
  - inventory diff 줄 집계
  - `payloads.attachment_draft_ids` · FE `AxDraftCard.tsx` confirmPayload 대조
  - 새 테스트 읽기(W1·W2·W4)
  - `make test-unit` → **403 passed** · `make test-contract` → 병렬 **1159 passed** · 직렬 **128 passed, 실패 0**

## 앞 지적 해소

| 앞 지적 | 결과 | 근거 |
|---|---|---|
| **F1** 화면에 닿는 스키마 title 「기한」 | **닫힘** | 스키마 전수 출력 0 · 백엔드 소스의 「기한」은 주석 아닌 줄 기준으로 넷만 남았다. 오류 문구 2(`payloads.py:127` · `requests.py:296` — add1 §3 FE 정규식 대상으로 유지) · AI 프롬프트 예시 1(`codex_cli.py:512`) · 회의 쪽 docstring(`meetings.py:787` · `finalize.py:204` · `export.py:219` — 회의 할 일 기한, 업무 `due_date` 아님)이다. inventory 는 `"title": "기한"` → `"마감일"` **한 줄만** 바뀌었다 |
| **W1** 자료 붙은 초안 저장 → 등록 회차 | **닫힘** | 코드는 원래 저장이 `attachment_draft_ids` 를 스냅샷에 남기는 구조였다(`action_center.py:603-611` 정규화 → `decide_ax_confirmation` 최종 스냅샷). fix1 은 그것을 계약 테스트로 고정했다. `test_a_saved_draft_keeps_its_staged_materials_so_confirming_opens_no_third_round`(`test_action_center.py:1850`)이 링크 자료 staged → 저장(회차 2, 스냅샷에 ID) → draft 없이 같은 ID 로 confirm → 회차 `[1, 2]` · 결정이 2회차에 붙고 · 만든 업무에 `external_link` 자료가 붙는 것까지 본다. FE 는 저장·등록 둘 다 `[...new Set(ids)].sort()`(`AxDraftCard.tsx:286-287`)로 같은 목록을 싣는다 |
| **W2** 남이 저장 | **닫힘** | `test_only_the_owner_of_the_draft_may_save_it`(`:1886`) — 다른 persona → **404**, 회차 `[1]` · `awaiting_review` · 값 그대로. 응답은 지금 코드 그대로(소유자 잠금 `ActionNotFound`) |
| **W3** `TaskScheduleReleaseView` docstring | **닫힘** | `task_results.py:53-54` 「네 자리 … 완료의 마감일 채움(완료 · 완료 보고 제출)」. inventory 의 그 `description` 도 같은 문장으로 패치됐다. `test_task_schedule_release.py` 의 「세 자리」 docstring 도 「막힘·취소」로 고쳤다 |
| **W4** 넷째 자리 훅 증명 | **닫힘** | `test_task_due_date_fill.py:160-234`. 실제 경로를 본다 — 스파이가 `TaskApplication._release_schedules_outside` 를 **클래스 수준**에서 감싸고 원래 함수를 그대로 부른다. 그래서 `transition_task`·`submit_completion` → `_schedule_release_for` → 그 메서드로 가는 운영 경로에서 잡힌다. 시작 예정일 하루(09-08)에 살아 있는 배정을 둔 업무로 세 경우를 본다. ① 직접 완료 — 훅 1회 · `released_count 0` · 배정 생존 ② 요청 Task 완료 보고 — 같음 ③ 마감일이 이미 있음 — 훅 0회. 「안 돌아서 0」과 「돌았고 닫을 것이 없어 0」이 갈린다 |
| 직렬 흔들림 | **재현 안 됨** | 이번 직렬 패스 128 passed · 실패 0 → 이름을 잡을 일이 없었다 |

## 위반 (FAIL 사유)

- 없음

## 경미 (WARN)

- **W5 `backend/src/ax_workspace/modules/actions/payloads.py:84` · `backend/src/ax_workspace/platform/action_center.py:603-611`** — 첨부 ID 정규화가 중복만 걷고 **순서는 받은 그대로**다(`list(dict.fromkeys(...))`). 저장·확인의 「바뀌었나」 비교(`confirmation.py:226-228`)와 저장 영수증 해시(`action_center.py:1061-1063`)는 그 순서까지 같아야 같다고 본다. 그래서 다음 둘이 생긴다.
  - (a) 같은 자료 집합을 **다른 순서**로 보내면 새 회차가 열리고 diff 에 `attachment_draft_ids` 가 바뀐 것으로 남는다
  - (b) draft 없는 confirm 이 `attachment_draft_ids` 키를 **빼면** `[]` 로 비교된다. 그러면 저장 회차와 달라 새 회차가 열리고, 자료는 claim 되지 않은 채 업무가 생긴다

  지금 FE 는 저장·등록 둘 다 정렬한 같은 목록을 싣는다. 그래서 2a-1 화면에서는 일어나지 않는다. 다른 호출자(범용 렌더러로 떨어진 경우 · MCP 등)에게만 열린 자리다
  - 근거: WP 1-1 「저장 뒤 등록 … 회차가 또 늘지 않는다」 · SPEC-002 §4(코디가 고칠 「자료」 줄)
  - 권장: 서버가 `attachment_draft_ids` 를 정렬해 정규화한다. (b)는 「draft 없는 confirm 은 키가 없으면 최신 스냅샷의 첨부를 쓴다」로 맞춘다 — draft 를 생략하면 최신 스냅샷을 쓰는 지금 규칙과 같은 결이다. 이번 판에서 할지, 이월할지는 코디 판단

## 확인한 것 (PASS 근거) — 새 문제 점검

- **F1 교체가 다른 것을 바꾸지 않았나**
  - 바뀐 것은 pydantic `title` 문자열뿐이다. 필드 id·API 키(`due_date`·`clear_due_date`)는 그대로다
  - FE 정규식(`/마감일|기한|due_date|schedule/`)은 오류 문장을 보는데, 오류 문구 2곳은 그대로라 매칭이 유지된다. 이제 라벨까지 「마감일」이 되어 정규식의 「마감일」 갈래로도 잡힌다
  - inventory 에서 title 이 바뀐 줄은 하나다. `task.update`·`work_request.amend`·`project.plan_work` 스키마가 inventory 에 실린 것은 그 한 자리뿐이다 — drift 테스트(architecture) 통과
- **inventory 「그 항목만」** — 이번 diff 의 비반복 줄은 다음뿐이다. 재배열 흔적 없음
  - `save_command` 반복 블록(앞 판과 같은 63)
  - `TaskScheduleReleaseView`(완료 결과 타입 · 고친 docstring)
  - `complete` http_signature
  - 두 도구 description
  - `title 기한→마감일` 1
- **W1 이 confirm+draft(다른 카드) 경로를 바꾸지 않았나** — 소스 변경이 아니라 테스트 추가이고, 기존 계약 테스트 전부 통과한다
- **W4 테스트가 오늘에 의존하지 않나** — 고정 시계(`_INSTANT = 2026-09-09T16:30Z`, 서울 09-10)이고 배정일 09-08 → 채움 뒤 기간 `[09-08, 09-10]`. 배정이 시작 예정일 끝점이라 정규화 구간 안이다(SPEC-004 K11 논증과 같다)
- **테스트**: `make test-unit` 403 · `make test-contract` 1159 + 직렬 128, 실패 0

## 남은 코디 몫 (앞 판에서 이월)

- `make test-postgres`(격리 DB) · `make verify`
- 실물: 로컬 스택 「…업무 만들어 줘」 1회(체크리스트·내용 채움) · 채팅 확인 폼 라벨 「마감일」(`task.update`·`work_request.amend`·`project.plan_work`) · 자료 붙인 초안 저장 → 등록 회차 그대로
- SPEC-002 고치기 — 낡음 오류(422 + 문장)와 「자료」 줄(저장도 붙인 자료 ID 를 남긴다)
