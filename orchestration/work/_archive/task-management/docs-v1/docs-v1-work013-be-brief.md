# [backend] WORK-013 Phase 1~2 — payload 두 모양 · kind/newTask 제거 · 「넣기」 두 표면 · 자리 유지 · 유형 설명

너는 **task-management `backend` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

## 0. 어디서 무엇을 보나

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`). **WORK-009 ~ 012 가 들어와 있다** — `git log -5`. WORK-012 가 `payload` 컬럼(리비전 0008)과 `merged` 트랙을 만들었다. 이 work 는 **사람이 `payload` 를 채우는 길**과 **업무로 넣는 길**을 연다.

문서는 전부 **코디 워크트리 절대경로 · 읽기 전용**이다.

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/
  30-work/work-013-meeting-edit.md             ← 네 빌드 계획. **Phase 1 · 2**(3 · 4 · 5 는 프론트 — 다른 발주). Code Surface 백 행 · Internal Interface(표면 둘 · done 뒷문 없음 · 원자성 · 줄 본문 출처) · Phase 검증
  20-spec/spec-008-meeting-close.md §4         ← API 표 · `POST lines`(payload 갈래 · 422 조건) · `PATCH lines` · `DELETE lines` · `POST/PATCH …/task` 본문 · Validation 표 · Case Matrix
  20-spec/spec-002-work-settings.md §4         ← `description` 0~200 · null 허용 · 기본 3종도 설명은 편집 가능 · 시드 문구
  10-decision/decision-003-meeting-notes.md    ← §4 업무 갱신 허용 필드 일곱 · §5 편집 다섯 · 업무 연동 · §7 「업무 넣기 거부」
  10-decision/decision-001-auth-settings.md    ← §3 유형.설명 · §4 기본 유형
  40-architecture/backend/README.md            ← §8-3 「업무 넣기(payload) 거부」 행 · §10 회의록 행 · §12 테스트 8-b · 8-c
  40-architecture/database/domains/meeting.md  ← M-14 · M-14-a · M-20 / account.md A-12(description)
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/reference/2026-09-06-task-management-app/Meeting flow.md §3-4 · §3-5   ← MF-13 · 14 · 21 · 36 · 59 · 60 · 62 · 64(정정) · 65 · 66 · 67
```

## 1. 범위 — Phase 1 · 2 (백엔드만)

```
Phase 1  schemas/meeting.py — ActionLinePayload · TaskLinePayload(status Literal["todo","in_progress"] · extra=forbid) · TaskUpdateBody(taskId 필수 + 변경분 일곱 · 같은 Literal) 신설 · PendingChange 폐기
         LineCreate: new_task 삭제 · payload/task_id 는 kind 로 가름(논의·결정에 오면 422) · LineUpdate: kind 삭제
         meeting_edit_service.add_line/update_line 재작성 — content 네 종류 필수 · 서버가 업무 제목으로 덮어쓰지 않음 · task_service 미호출 · kind 전환 분기 삭제
Phase 2  meeting_task_link_service — apply_pending_change → apply_task_update(body) ①~⑧ 한 트랜잭션 · add_task_line · _stored_change 폐기 · create_task_from_line 은 content 유지
         meeting_line_repository.delete_line 당김 제거(next_order_index = max+1 확인)
         리비전 0009 work_type.description + 시드 2건(미팅·회의는 NULL) · WorkType 모델 · seed · schemas/dto/setting · work_type_service(0~200 · 줄바꿈 불가 · null · 기본 3종도 편집)
         meeting_router PATCH …/lines/{id}/task 본문 수신
```

**Phase 3 · 4 · 5(프론트)는 다른 워커다. `app/front/` 금지.**

## ⛔ 2. 하지 말 것 · 이미 있는 것

```
task_service.py            **고치지 마라.** create · update · change_status · add_memo · 할일 · 연관 을 부르기만. 회의록 쪽에 판정 코드(전이 그래프 · 완료 게이트 · 결과자료) 0
task.status 대입            change_status() 안에서만. 회의록 코드에 0
done · cancelled           스키마 층 422. payload 와 TaskUpdateBody 가 **같은 Literal 을 공유**
payload 저장 ≠ 업무          POST/PATCH lines 는 task_service 를 import 하지 않는다(정적 검사). 업무를 바꾸는 회의록 코드는 meeting_task_link_service 의 두 함수뿐
같은 상태는 건너뛴다          ① 에서 status == task.status 면 전이를 부르지 않는다(로그 0)
원자성                     PATCH …/task ①~⑧ 한 트랜잭션. 어느 단계든 거부 → 전부 롤백 · payload 그대로
order_index 당기지 마라       delete_line 은 그 행만. next_order_index 는 max+1
줄 본문                    서버가 업무 제목으로 덮어쓰지 않는다. 액션 줄의 content 는 사람이 적은 것
except Exception · 임의 재시도 · 조용한 기본값 금지
```

## 3. 계약

- **`POST …/lines`** — `agendaId` · `kind` · `content`(필수) · `detail` + **action/task 줄에만** `payload`(업무 줄은 `taskId` 도). 논의·결정에 `payload`/`taskId` → 422. `newTask` 없음(422). 업무 안 생김
- **`PATCH …/lines/{id}`** — `content` · `payload` · `taskId`(task 줄만). `kind` → 422
- **`DELETE …/lines/{id}`** — 그 행만 하드 삭제 · 자리 유지 · 편집 대상 트랙만(`succeeded`→merged · `failed`→human) · `ai` 422 · 없으면 404
- **`POST …/lines/{id}/task`** — `LineNewTask`(SPEC-003 `POST /api/tasks` 규칙) → 업무 생성 + 줄 `kind='task'` · `task_id` · `payload=NULL` 한 트랜잭션. 조건: `kind='action'` · `task_id` 없음
- **`PATCH …/lines/{id}/task`** — `TaskUpdateBody`(`taskId` 필수 · 변경분 0~7) → ① status(다르면 `change_status`) ② dueDate ③ projectId ④ note(메모 새 항목) ⑤ todos(추가) ⑥ relatedTaskIds(양방향 추가) ⑦ completionResult(덮어씀) ⑧ 줄 `task_id=taskId` · `payload=NULL`. 조건: `kind='task'`
- **`work_type.description`** — 0~200 · 줄바꿈 불가 · `null` 허용 · 기본 3종도 편집 가능 · `GET /api/work-types` 응답에 실린다(MCP `list_work_types` 통과)

## 4. allowed_paths

```
app/back/
```

## 5. 검증

WP §Execution Phase 1 · 2 검증 체크리스트 전부. 특히 — `PATCH lines` `kind` 422 · `POST lines` `newTask` 422 · 논의·결정 `payload` 422 · 액션 `payload` 저장 시 업무 행 수 불변 · **BE §12 8-c**(`done`/`cancelled` 422 · `task.status` 불변) · `workTypeId=null` 저장 OK · **BE §12 8-b**(3 지우면 4 그대로 · 새 줄 max+1) · 줄 삭제 시 `task` · `ai` · transcript · `recording_path` 불변 · `PATCH …/task` 같은 상태 → `task_log` 0 · 거부 → 전부 롤백 · 변경분 0 → ⑧만 · 리비전 0009 왕복 · 시드 2건 · 미팅·회의 NULL · 정적: `meeting_edit_service` 가 `task_service` import 0 · `newTask|new_task|pendingChange|PendingChange` 0 · `task_service` 를 부르는 회의록 코드 = `create_task_from_line` · `apply_task_update` 둘

```bash
cd /Users/kknaks/orca/workspaces/task_management/docs-v1 && make test    # 전체 · Errors 0
```

막히면 30분 넘기지 말고 §9 (2) 로 물어라.

---

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_fd9fc1ce-619d-4f87-b218-10dfaefaa275 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: WORK-013 Phase 1~2" \
  --body "변경 파일 목록 / Phase 별 구현 요약 / 검증 결과(수치 · 정적 검사 grep) / 계약 준수 / 미결·주의점"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] backend 완료 — WORK-013 편집 백엔드. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] backend: <질문>" --enter`
