# [frontend] Phase FE-2 — 상호작용 넷 · 금지 문구. **마지막 Phase 다**

너는 **strong-hajin `frontend` 워커**다. **FE-1 을 네가 방금 했다** — 맥락이 이어진다.
역할 문서와 `AGENTS.md` 는 다시 읽지 않아도 된다.

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar`

> ⚠ **FE-1 은 커밋됐다** (`c5b109d`). BE 는 `1c15d02`·`2a85176`. 네 새 변경만 uncommitted 로 남는다.
> ⚠ **이번엔 쓰기를 붙인다.** 실제 API 를 부른다 — 목데이터가 아니다.
> ⚠ 커밋·push 금지.

## 1. 작업 지시서

`…/30-work/work-004-calendar-scheduling.md` 의 **`Phase FE-2`** — 작업 1~9 · 완료 판정.
**그대로 따라라.** 특히 **작업 9(WARN-A)가 이미 한 줄로 정해져 있다** — 네가 다시 정하지 마라.

실제 API 계약은 `orchestration/work/strong-hajin-calendar/be2-report.md` §5. **FE-1 때 읽은 그것이다.**

## 2. 쓰기에서 틀리기 쉬운 자리 — **여섯. 전부 검수가 닫은 것들이다**

1. **같은 날 재배정은 `POST` 가 아니라 `PATCH`** 다 (K10·K1).
   `POST` 는 **생성 전용**이고 그 날이 차 있으면 **`409`** 다. `schedules[]` 가 `schedule_id`·`version`
   을 이미 주므로 **그 날에 배정이 있으면 곧바로 `PATCH`** 를 부른다.
   **정상 흐름에서 `409` 를 보면 안 된다.**
2. **연타는 같은 멱등 키로** 보낸다 (K12). 그래야 `409` 가 아니라 **`200` 영수증**이다.
   키를 매번 새로 만들면 두 번째 클릭이 `409` 를 맞는다.
   **`201` 과 영수증 `200` 은 본문이 같다 — 상태 코드로 가른다.**
3. **`PATCH` 의 `expected_version` 은 무조건 필수**이고 **그 배정 자신의 회차**다 (K8).
   업무 회차가 아니다.
4. **가드는 `span_from`·`span_to`** 로 판정한다 (K14). `start_date`/`due_date` 로 판정하면
   뒤집힌 업무에서 **서버가 받는 날을 화면이 막는다.**
5. **세로 손잡이는 놓을 때 한 번만** 부른다. 끄는 동안 부르면 회차가 매번 어긋난다.
   **회의 블록에는 손잡이를 붙이지 않는다** (§F — 회의는 캘린더에서 읽기 전용).
6. **에러 본문에 `code` 가 없다** — `{"detail":"…"}` 뿐이다.
   **상태 코드 + 어떤 명령을 불렀는지**로 갈라라. `WORK_SCHEDULE_START_AFTER_DUE` 의 서버 문구는
   **영문**이다 — 그대로 내보내지 마라.

## 3. K3 알림 — **조건이 둘 있다**

`schedule_release.released_count` 로 「N건의 시간 배정이 기간 밖이라 해제되었습니다.」
**0건이면 아무 말도 하지 않는다.**

**BE 검수가 남긴 것 둘을 받아라.**

- **제안 재전송 영수증은 `{0, null}` 을 낸다.** 화면이 영수증으로 알림을 만들면 「N건 해제」를 **놓친다**.
  **알림은 첫 응답으로만 만든다.**
- **`schedule_release` 는 `/block`·`/resume`·`/complete`·`/cancel` 응답에 없다** — 읽으면 `undefined` 다.
  싣는 표면은 셋뿐: `PATCH /api/tasks/{id}` · `POST /api/tasks/{id}/start` ·
  `POST .../proposals/{pid}/respond`.

## 4. 금지는 말로 한다 (§I) — **조용한 거절 0개가 완료 조건이다**

시안은 조용히 거절한다(`canDrop` 이 거짓이면 `preventDefault` 를 안 불러 브라우저가 막는다).
**우리는 그렇게 하지 않는다.** 저장소 선례는 칸반의 `onInvalidMove` 다.

거절마다 문구 — **기간 밖 · 기한 없음 · 역전 · 담당 아님** 전부.
**기간 밖 문구에는 그 업무의 실제 기간을 넣는다** — `span_from`~`span_to` 다(정규화 구간).

## 5. allowed_paths

- `frontend/`

`backend/`·`docs/`·`para/`·`orchestration/` 금지. 백엔드가 모자라 보이면 **고치지 말고 코디에게 물어라.**

## 6. 검증 — **이 Phase 는 최종 검증까지 간다**

```
make frontend-test
cd frontend && npx tsc --noEmit
make verify                    ← 최종. FE-2 의 완료 판정이다
make test-postgres POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@127.0.0.1:54329/ax_test_calendar
```

- 기준선: FE-1 직후 **67파일 857통과 · tsc 0** · BE 는 test-unit 356p/0f · test-postgres 89p/0f
- `test-contract` 의 `material_worker_recovery` 2건은 **기존 flaky** 다. 무관으로 분리
- **상호작용 넷이 실제 API 를 부르는지**를 테스트로 박아라 — 목으로 넘기지 마라
- **브라우저 E2E 는 사용자 담당**이다. 네가 스택을 띄우지 마라

## 7. 범위 제약

- **계약을 다시 정하지 마라.** 작업 9(WARN-A)는 **이미 정해졌다** — 그대로 구현한다
- 백엔드를 건드리지 마라
- 시안은 **레이아웃 정본**이다. 기능·모달은 우리 것 — 「업무 만들기」는 **기존 모달**을 연다(K17)
- 커밋·push 금지

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_a9d49810-1ce8-4885-8c5f-b93200c501ac --from term_49972e50-eed3-461b-8174-fc4f61de218d \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_a9d49810-1ce8-4885-8c5f-b93200c501ac \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_a9d49810-1ce8-4885-8c5f-b93200c501ac --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
