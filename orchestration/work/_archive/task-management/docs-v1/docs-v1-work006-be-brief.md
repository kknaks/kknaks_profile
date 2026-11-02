# [backend] WORK-006 Phase 1~3 — 회의 도메인 · 본체 API · 안건 · 첨부

너는 **task-management `backend` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

## 0. 어디서 무엇을 보나

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`).
레포는 `github.com/kknaks/task_management`. **코드 워커는 한 번에 하나만 돈다** — 이 트리에서 직접 작업한다.
**문서는 코디 워크트리 절대경로로 읽는다(읽기 전용).**

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/
  30-work/work-006-meeting-setup.md      ← 네 빌드 계획. Phase 1~3 만
  20-spec/spec-006-meeting-setup.md      ← 외부 계약(§4)·Acceptance(§6)
  10-decision/decision-003-meeting-notes.md   ← 정책
  00-baseline/baseline-003-meeting-notes.md   ← 기획
  40-architecture/backend/README.md · database/README.md · database/domains/meeting.md
```

## 1. 범위 — Phase 1 · 2 · 3 만

```
Phase 1  회의 도메인 마이그레이션 · schedule_service 연결
Phase 2  회의 본체 API · /start · MeetingDetail 빌더
Phase 3  안건 · 첨부 API
```

**Phase 4~6 은 프론트다. 건드리지 마라.**

## ⛔ 2. 코디가 정한 것 — SPEC 문서보다 이게 우선이다

SPEC 3개가 병렬로 쓰여 이름이 갈린 자리가 있다. **아래대로 쓴다.**

| 항목 | 결정 |
|---|---|
| **`MeetingDetail` 트랙 필드** | **`agendas.{human, ai, merged}`** — 안건 배열이고 줄은 안건 안 `lines[]` 에 중첩된다 |
| **배치 회차 필드** | **`latestBatchSeq`** (`aiBatchSeq` 아니다) |
| **상태 가드 에러코드** | **`invalid_meeting_status`** 하나. **`meeting_not_recording` 을 만들지 마라** — 같은 상황이다 |
| **`/end` 사전 조건** | 이 work 범위 밖(WORK-008). 다만 **끊긴 상태에서도 `/end` 는 받는다**가 확정이다 — `paused/stream` 에서 409 로 막는 것은 **오디오뿐**이다 |

**`build_detail()` 은 하나뿐이다**(WP L165 · SPEC-006 §5 · WORK-004 F-4 교훈).
상세·생성·`PATCH`·`/start`·안건·첨부 응답을 **전부 이 함수 하나**가 만든다. 삭제만 `204`.
**WORK-007·008 이 이 함수에 필드를 더한다** — 네가 만드는 것은 뼈대다:

```
채운다     agendas.human 트리 · attachments · durationMinutes · 메타
비워둔다   agendas.ai = []      agendas.merged = []
           headline = null      mergedSummary = null
           latestBatchSeq = 0   finalBatchState = null   activeJobId = null
```

**표면마다 다른 조립을 두지 마라.** WORK-004 에서 그걸 하다 반려가 났다.

## 3. 지킬 것 — 아키텍처

`backend/README.md` 가 판정 기준이다. 리뷰어가 이걸로 본다.

```
계층        router → service → repository 한 방향. 건너뛰지 않는다
ORM 경계    모델은 repository 를 넘지 않는다. service 는 dto 만 본다
schema/dto  service 는 schemas/ 를 import 하지 않는다
            router 가 schema → dto 로 바꿔 넘긴다. dict 를 계층 계약으로 쓰지 마라
PATCH       T | Unset + model_dump(exclude_unset=True)
            「안 보냄」과 「null 로 지움」을 구분한다
쿼리 파라미터  Query(alias="camelCase") 를 손으로 적는다
            — alias_generator 는 본문에만 걸린다. 빠뜨리면 조용히 무시되고 200 이 난다
            (WORK-004 에서 실제로 밟았다 — backend/README §3-7)
트랜잭션     요청 하나가 경계. service·repository 에서 commit() 하지 않는다
예외        도메인 예외만 던진다. except Exception 금지
            열거되지 않은 실패는 fallback 하지 말고 그대로 전파한다
            (BASE-003 L43 · DEC-003 §7)
```

## 4. 다시 만들지 마라 — 이미 있는 것을 쓴다

| 무엇 | 어디 | 근거 |
|---|---|---|
| **겹침 검사 · `schedule` 파생** | `service/schedule_service.py` | **`work-004` L155 「두 번째 구현을 만들지 않는다」.** 회의 일시도 이 서비스를 그대로 부른다 |
| 유형(`kind='meeting'`) · 프로젝트 | `service/work_type_service.py` · `project_service.py` | WORK-003 |
| 소프트 딜리트 규약 · 자식 컬렉션 표면 | `task_service` · `task_router` | WORK-004 형태를 따른다 |

## 5. 검증

```bash
cd app/back && uv run pytest -q <네가 만들거나 고친 테스트만>
```

**전체 스위트 금지. 검증은 1회만.**

자기점검 — ORM 이 repository 를 넘지 않는가 · schema/dto 를 섞지 않았는가 ·
`except Exception` 을 쓰지 않았는가 · `Query(alias=...)` 를 빠뜨리지 않았는가.

**WP 의 Phase 1~3 검증 항목을 그대로 확인해라.** SPEC-006 §6 Acceptance 중
Phase 1~3 에 해당하는 것도 함께 본다.

## 6. 지킬 것 — 일반

1. **`app/back/` 밖을 건드리지 마라**(`docker-compose*.yml` · `.env.example` 은 필요하면 허용)
2. **프론트를 만들지 마라.** Phase 4~6 은 다른 워커다
3. **문서를 고치지 마라.** SPEC·WP·정책·아키텍처 전부 읽기 전용이다
4. **커밋·push 하지 마라**
5. **WP 범위 밖을 하지 마라.** 필요해 보여도 하지 말고 보고에 적어라
6. 막히면 물어라 — `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "..." --enter`

## 7. Done Criteria

- [ ] Phase 1~3 의 WP 검증 항목이 전부 통과
- [ ] `build_detail()` **하나**가 상세·생성·PATCH·`/start`·안건·첨부 응답을 만든다
- [ ] `agendas.{human,ai,merged}` · `latestBatchSeq` 이름을 썼다
- [ ] `meeting_not_recording` 을 만들지 않았다
- [ ] `schedule_service` 를 소비만 했다 — 겹침·파생의 두 번째 구현이 없다
- [ ] 계층·ORM 경계·schema/dto·PATCH Unset·`Query(alias)` 자기점검 통과
- [ ] `except Exception` 0건
- [ ] `app/back/` 밖 변경 0건 · 커밋 없음

## 8. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from term_53af7066-d01d-4ce3-928f-5c85e7935570 \
  --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "WORK-006 Phase 1~3 완료" \
  --body "리비전 번호와 테이블·컬럼 / 만든 표면 목록 / build_detail 위치와 채운 필드·비워둔 필드 / schedule_service 소비 지점 / pytest 결과 / WP 검증 항목 통과 여부 / 범위 밖이라 안 한 것 / SPEC·WP 와 어긋나 못 한 것"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] WORK-006 Phase 1~3 완료. 상세는 인박스." --enter
```
