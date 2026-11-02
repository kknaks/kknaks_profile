# [backend] Phase BE-2 — D1 세 자리 · `schedule_release` · 운영 대장

너는 **strong-hajin `backend` 워커**다. **BE-1 을 네가 방금 했다** — 맥락이 이어진다.
역할 문서와 `AGENTS.md` 는 다시 읽지 않아도 된다.

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar`

> ⚠ **BE-1 은 커밋됐다** (`1c15d02`). 네 새 변경만 uncommitted 로 남아야 한다.
> ⚠ 커밋·push 금지. FE 는 손대지 마라.

## 1. 작업 지시서

`…/30-work/work-004-calendar-scheduling.md` 의 **`Phase BE-2`** — 작업 1~7 과 완료 판정.
**그대로 따라라.** 여기서 다시 쓰지 않는다.

한 줄로: **배정이 사라지는 두 경로를 실제로 걸고, 닫힌 건수를 응답에 싣고, 표면 등록을 마친다.**

## 2. BE-1 검수가 남긴 것 — **K16. 반드시 받아라**

검수는 **PASS** 였고 지적은 하나다. 코디가 **더하기로 정했다**(DEC-003 증보 6 K16).

> `calendar_tasks`(`application.py:664`)가 `tasks_for` 를 직접 불러 **`_require(principal, TASK_READ)`
> 를 안 지난다.** 쓰기 쪽 `_assignable_task` 도 **`TASK_SELF_MANAGE` 를 안 지난다.**
> 같은 파일에 `TASK_READ` 를 요구하는 자리가 **열둘**이다.

**읽기에 `TASK_READ`, 쓰기에 `TASK_SELF_MANAGE` 를 건다.**

**왜** — 역량 문과 관계 검사는 **대체재가 아니라 겹겹**이다. K5 의 「판정은 담당 관계이고 봉투가
아니다」는 **봉투로 판정하지 말라**는 뜻이지 **봉투를 걷으라**는 뜻이 아니었다. 지금은 두 역량이
구성원·팀장 기본에 다 있어 못 지나는 역할이 없지만, **역량 없는 역할이 생기는 순간 새 표면만 샌다.**
같은 파일 열두 자리와 어긋나는 것 자체도 위험하다 — 다음 사람이 「여긴 안 걸어도 되는구나」로 읽는다.

**기존 동작이 바뀌지 않는 것**을 테스트로 남겨라 (구성원·팀장 둘 다 여전히 통과한다).

## 3. 틀리기 쉬운 자리 — BE-2 것

- **D1 은 세 자리다.** `application.py:518-520`(`update`) · `:1443`(`transition`) ·
  `:1679`(`_apply_proposal`). **공통 조상이 없다.** `touch()` 에 걸지 마라 — 날짜와 무관한 변경에도
  아홉 번 불린다.
- **검증과 저장이 한 transaction 이다.** 나뉘면 「배정은 닫혔는데 업무 날짜는 안 바뀐」 상태가
  **복구 경로 없이** 남는다(D3).
- **사유는 둘뿐이다.** 정규화 구간 밖 → `out_of_range` · 날짜 전부 지움 → `task_dates_cleared`.
  **셋째를 만들지 마라** (K1·K11 이 그래서 그렇게 정해졌다).
- **시작 전이 자리는 「닫을 것이 없음」을 증명한다.** K11 이후 그 자리에서 닫히는 배정은
  **구조적으로 나올 수 없다.** 그래도 **검증 훅과 `schedule_release` 묶음은 있어야 한다** —
  K3 이 세 자리 전부에 건수를 요구한다. **0 을 내는 것도 계약이다.**
- **문구는 서버가 만들지 않는다.** `released_count` 와 `reason` 만 낸다.
- **업무 종료는 쓰기가 아니다** — 상태 아홉 경로에 **아무것도 더하지 마라**. 읽기 필터로 끝났다.

## 4. 운영 대장 — **전체 재작성 금지**

`docs/unified-operations-inventory.json` (2.1MB).

- **행 3 추가** · `http_count` **156 → 159** · `tool_count` **129 불변**
- 각 행: `status: excluded` · `policy: E2` · `exclusion.reason` ·`reconsider_when`
  (문구는 WORK-004 작업 5 에 그대로 있다)
- `GET /api/meetings` 행의 **`http_signature` 갱신**(인자가 늘었다), 합본 조회 행의 응답 필드 증가도
- **`AGENTS.md:15` 가 절차다 — 테스트 실패 diff 를 보고 그 항목만 패치한다.** 통째로 다시 뽑으면
  `acceptance_evidence` 같은 **사람이 적은 판단**이 날아간다
- **BE-1 이 남긴 시그니처 주의** — `POST .../schedules` 에 `response: Response` 인자가 있다
  (영수증을 `200` 으로 내려고 상태를 동적으로 정한다). `http_signature` 에 그 인자가 함께 든다
- `Makefile:170` 과 `tests/architecture/test_local_stack_targets.py:28-40` 은 **동시에** 고친다

## 5. allowed_paths

- `backend/` · `docker-compose.yml` · `Makefile`
- **추가** — `docs/unified-operations-inventory.json` · `docs/domain-model.md`
  (BE-2 는 이 둘을 고쳐야 한다. **그 둘 말고 `docs/` 의 다른 파일은 건드리지 마라.**)

`para/`·`orchestration/`·`frontend/` 는 여전히 금지다.

## 6. 검증 — WORK-004 `Phase BE-2` 완료 판정 그대로

```
make test-unit        ← test_operation_inventory 가 이제 통과해야 한다
make test-contract
make test-postgres POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@127.0.0.1:54329/ax_test_calendar
```

- **`test_operation_inventory` 통과가 이 Phase 의 관문이다.** BE-1 이 의도적으로 깨 둔 것을 닫는다
- 대장 diff 가 **행 3 + count 1줄 + `http_signature` 2줄 이내**인지 확인하고 보고하라.
  `acceptance_evidence` 보존 확인
- 세 자리 각각의 테스트. **시작 전이는 `released_count = 0` 을 증명한다**
- 기간을 줄였다 되돌리면 **빈 채로 돌아오고**, 그 날에 **다시 배정할 수 있다**
- 기준선: BE-1 직후 `test-contract` 의 `material_worker_recovery` 2건은 **기존 flaky** 다. 무관으로 분리

## 7. 완료 보고에 **반드시** 넣을 것 — FE 가 이것을 쓴다

**실제 API 계약을 응답 예시로 적어라.** 추정이 아니라 **네가 돌려 본 실물**이다.

- `GET /api/calendar?from=&to=` 의 **실제 응답 한 벌** — `kind:'task'` 행과 `kind:'meeting'` 행 각각,
  필드 이름과 타입 그대로 (`span_from`·`span_to`·`schedules[]` 원소·`created_by_display_name`)
- `POST .../schedules` 201 / 영수증 200 / `409` 의 실제 본문
- `PATCH /api/task-schedules/{id}` 200 의 실제 본문
- 업무 날짜 수정 응답의 `schedule_release{released_count, reason}` 실물
- 에러 10종의 실제 `code` 문자열

**이것이 FE-1·FE-2 브리프에 그대로 박힌다. 틀리면 FE 가 통째로 틀어진다.**

## 8. 범위 제약

- **계약을 다시 정하지 마라.** 모순은 고치지 말고 **코디에게 물어라**
- FE 를 당겨 하지 마라
- 상태 아홉 경로에 아무것도 더하지 마라
- 커밋·push 금지

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_a9d49810-1ce8-4885-8c5f-b93200c501ac --from term_8d3cb041-0ed1-492c-ace7-2ea1fc902b77 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_a9d49810-1ce8-4885-8c5f-b93200c501ac \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_a9d49810-1ce8-4885-8c5f-b93200c501ac --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
