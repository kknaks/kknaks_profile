# [backend] WORK-005 Phase 1·2 — 상태 전이 · 완료 게이트 · 목록 조회

너는 **task-management `backend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**WORK-004 는 끝났다**(업무 도메인·본체 API·자식 컬렉션·후보 검색). 그 위에 상태를 얹는다.

## 1. 이 work 가 무엇인가

**완료 게이트가 이 제품의 규칙이다** — 「결과자료가 있거나 완료 결과를 적었거나, 둘 중 하나는 있어야 업무를
어떻게 끝냈는지 기록이 된다」(DEC-002). 그 판정이 **한 곳에만** 있어야 한다.

상태를 바꾸는 진입점이 넷이다 — **리스트 셀 · 상세 드롭다운 · 칸반 DnD · (나중에) 회의록의 「업무 갱신」**.
넷이 전부 `PATCH /api/tasks/{id}/status` **하나**로 들어오고, 그 뒤 `change_status()` **하나**가 판정한다.
**여기서 판정을 한 곳에 못 모으면 이후 세 화면과 회의록이 각자 규칙을 갖는다.**

## 2. SSOT — 먼저 읽을 것

경로 기준: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`

| 층 | 문서 |
|---|---|
| **WP(이번 범위)** | `30-work/work-005-tasks-status-views.md` — **§Internal Interface Contract** · **§Execution Phase 1·2** 의 작업·검증 체크리스트가 네 할 일 목록이다 |
| **SPEC** | `20-spec/spec-004-tasks-status-views.md` — §4 API·Case Matrix가 **외부 계약의 정본** |
| **정책** | `10-decision/decision-002-tasks.md` — 완료 게이트 · 취소는 상태 · 소프트 딜리트 |
| **아키텍처** | `40-architecture/backend/README.md`(**§3 규칙 7 쿼리 alias** · §7 `persist_changes` · §8 에러 코드 · §10 · §12 필수 테스트) · `database/README.md` + `domains/task.md` |

**계약은 SPEC 이 SoT 이고 구조는 아키텍처가 SoT 다.** WP 는 그 둘을 이번 범위로 자른 것이다.

## 3. 이번 범위 — Phase 1·2 (백엔드만)

**Phase 3·4(프론트)는 네 몫이 아니다.** WP 의 Phase 1·2 체크리스트를 그대로 따라라.

### 특히 못박을 것

- **`task.status` 에 값을 대입하는 코드가 `change_status()` 안에만 있다.** grep 으로 증명해라
- **`TaskCompletionBlockedError` 를 던지는 곳이 1곳**
- **일반 `PATCH` 에 상태를 섞지 않는다** — `TaskUpdateDTO` 에 `status` 가 **없어야** 하고, `PATCH /api/tasks/{id}`
  로 `status` 를 보내면 **422 `validation_error`** 다. **게이트 우회 경로를 스키마 층에서 막는 것**이 요점이다.
  **WORK-004 에 이미 뚫려 있으면 여기서 막아라**(검수 결과가 오면 코디가 따로 알린다)
- **`persist_changes` 를 켜지 마라** — 이번 예외들은 실패가 쓰기를 뜻하지 않는다(BE §7)
- **파생 「지연」을 저장하지 마라** — 조회 시 계산해 `isOverdue`·`overdueDays` 로 내려준다
- **`typeCounts` 는 유형 탭 자신을 반영하지 않는다**(탭 숫자가 탭을 누를 때마다 흔들리면 안 된다)
- **목록 쿼리가 `schedule` 을 조인하지 않는다** — `EXPLAIN` 출력으로 증명해라(BE §12 5-a)
- **쿼리 파라미터에 `Query(alias=...)`** — §3 규칙 7. 빠뜨리면 필터가 **조용히 무시되고 200** 이 난다.
  **네가 WORK-004 에서 밟은 바로 그 함정이고, 이번엔 필터가 6개다.** 각 파라미터가 실제로 먹는지
  **값을 바꿔 결과가 달라지는 것으로** 확인해라

## 4. allowed_paths — 이 밖은 건드리지 마라

- `app/back/` — 전부(마이그레이션 포함. 스키마 변경이 필요하면 **새 리비전**을 추가하고 기존 것을 고치지 마라)

**`app/front/` 을 건드리지 마라.** 문서 레포도 **읽기 전용**이다 — 틀렸으면 보고한다.
**커밋·push·PR 하지 마라.**

## 5. 검증

WP Phase 1·2 의 **검증 체크리스트가 곧 합격 기준**이다. 전부 돌리고 **수치로** 보고해라.
특히 아래는 **실물 curl** 로 확인해라(테스트만으로 갈음하지 마라):

1. 결과자료도 완료 결과도 없는 업무에 `{"status":"done"}` → **422 `task_completion_blocked`** 이고 **DB 상태가 그대로**
2. 결과자료 1건 붙이면 같은 요청이 **200**. 그걸 지우고 완료 결과만 적어도 **200**(둘 중 하나)
3. 완료에서 `{"status":"cancelled"}` → **409 `invalid_status_transition`**
4. 취소를 사유 없이 → **422**
5. 완료 직후 `undo` → **200 + 직전 상태 복원 + 그 전이 로그 사라짐**. **5초 뒤 `undo` → 409**
6. `DELETE` 후 목록에서 빠지지만 **DB 에 행과 자식이 남아 있다**
7. **`PATCH /api/tasks/{id}` 에 `{"status":"done"}` → 422 `validation_error`**
8. 유형 탭 필터를 걸어도 `typeCounts` 가 **안 바뀌고**, 상태 필터를 걸면 **바뀐다**
9. 기한 없는 업무가 `due_asc` 에서 **맨 아래**
10. **`EXPLAIN` 에 `schedule` 이 없다** — 출력을 그대로 보고에 붙여라

```
cd app/back && pytest
```

계층 자기점검도 붙여라 — `except Exception` 0 · service 의 fastapi/schemas/models import 0 ·
router 의 models/repository import 0 · repository 의 ORM 반환 0 · `commit()` 0 ·
**`status` 대입 위치 grep** · **`TaskCompletionBlockedError` 발생 위치 grep**.

**dev DB 에 검증용 데이터를 만들어도 된다. 기존 행은 지우지 마라**(FE 워커가 같은 DB 를 본다).

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
