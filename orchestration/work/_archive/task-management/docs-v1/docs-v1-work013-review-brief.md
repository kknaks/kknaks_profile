# [reviewer] WORK-013 검수 — payload 두 모양 · 「넣기」 두 표면 · payload 드로어 둘 · 편집 모드 칩 갈래 · 유형 설명

너는 **task-management `reviewer` 워커**다. **read-only** — 코드를 고치지 않고 테스트도 돌리지 않는다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/reviewer/role.md`

## 0. 범위

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`, HEAD `0415290` = WORK-012). **아직 커밋 전** — 범위는 미커밋 변경 전부(백 + 프론트 + 리비전 0009).

```bash
git status --short                      # tauri.conf.json 은 범위 밖
git diff HEAD --stat
git diff HEAD -- app/back app/front
```

**워커 보고** — `orchestration/work/docs-v1/work013-fe-report.md`(백엔드 보고는 인박스 본문뿐 — 아래 §2 에 요지).
**산출물** — `orchestration/work/docs-v1/work013-review-report.md` **1개**.

문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`(읽기 전용)

## 1. 네 층

```
정책       decision-003 §4(업무 갱신 허용 필드 일곱) · §5(편집 다섯 · 업무 연동) · §7(「업무 넣기 거부」) / decision-001 §3(유형.설명) · §4(기본 유형)
아키텍처    backend/README.md §8-3 「업무 넣기(payload) 거부」 · §10 회의록 행 · §12 테스트 8-b · 8-c
           frontend/README.md §2 규칙 8(payload 드로어는 회의록 것 · 업무 드로어 미수정 · 반려 조건) · §3-3 · §3-4 낙관적 · §6(모달 두 크기) · §6-1 · 금지 목록 · 영역 사이 import 예외(CROSS_AREA_ALLOWED)
           database/domains/meeting.md M-14 · M-14-a · M-20 / account.md A-12(description)
SPEC       spec-008 U-6(줄 버튼 세 상태 · dot · 툴팁 · 삭제된 업무) · U-7(편집 모드 · 칩 둘 갈래 · 「제거」 420) · U-8(논의·결정 전용) · U-9(업무 payload 드로어 — 헤더 셀렉터 · 변경분 일곱 · 모드별 푸터 · 「그대로 재사용」) · U-10(액션 payload 드로어 — 안건 고정 · 일곱) · §4 API(POST lines payload 갈래 · PATCH lines kind 없음 · DELETE 자리 유지 · POST/PATCH …/task 본문) · Validation 표 · §5 구현 규칙 · Case Matrix · §6 AC
           spec-003 U-1 · U-3(시각 부품 참조만) · U-8(RelationPopover 단일 · 0건 폴백) / spec-002 U-3 · U-4 · U-7(설명)
WP         work-013-meeting-edit.md Phase 1~5 · §Internal Interface(표면 둘 · done 뒷문 없음 · 원자성 · 줄 본문 출처 · 드로어 prop 둘 · 푸터 · 칩 진입 · ConfirmModal size · RelationPopover 단일 · 낙관적 · 무효화)
결정 원본   Meeting flow.md §3-4 · §3-5 — MF-13 · 14 · 21 · 36 · 59 · 60 · 61 · 62 · 63 · 64(정정) · 65 · 66 · 67
```

## ⛔ 2. 이번에 반드시 볼 축

### 2-1. 게이트 — task.status 대입 · done 뒷문 (BE §12 8-c · MF-59)
```
task.status 대입은 task_service.change_status() 안에서만 — 회의록 코드(meeting_edit_service · meeting_task_link_service · router · schemas)에 0
payload.status 와 TaskUpdateBody.status 가 같은 Literal/Enum(PayloadStatus{todo,in_progress}) — done · cancelled 는 세 표면(POST lines · PATCH lines · PATCH …/task) 모두 422 · task.status 불변 · task_log 0
백엔드 보고: 옛 PAYLOAD_STATUSES 가 「모든 상태 − cancelled」 라 done 이 지나고 있었다 → PayloadStatus 로 좁힘. finalize 의 중복 상수도 합쳤나 · 회의 중/최종 경로(WORK-011/012) 의 done 키 제거가 여전히 도나
회의록 코드에 판정 코드(전이 그래프 · 완료 게이트 · 결과자료 count) 0 · except 포착으로 게이트를 삼키는 곳 0
```

### 2-2. payload 저장 ≠ 업무 (M-14-a · MF-60)
```
POST/PATCH …/lines 가 task_service 를 import 하지 않는다(정적) · payload 저장 시 task 행·task_log·memo 0 변화
업무를 바꾸는 회의록 코드 = meeting_task_link_service.create_task_from_line · apply_task_update 둘뿐(AST 단위 정적 검사가 있나)
논의·결정 줄에 payload/taskId → 422 · LineCreate 에 newTask 0 · LineUpdate 에 kind 0 · content 네 종류 필수 · 서버가 업무 제목으로 content 를 덮지 않는다
변경분 키 null → 422(「보내지 않음 = 변경 없음」) · 업무 payload {} 유효 · 액션 payload title 필수
```

### 2-3. 「넣기」 두 표면 · 원자성 (SPEC-008 §4 · WP §Internal Interface)
```
POST …/lines/{id}/task — kind='action' · task_id 없음 조건 · 업무 생성 + 줄 kind='task' · task_id · payload=NULL 한 트랜잭션 · 줄 본문 유지(todos · startDate 받나)
PATCH …/lines/{id}/task — TaskUpdateBody(taskId 필수) ① status 다를 때만 change_status ②③⑦ update_task ④ add_memo ⑤ add_todo ⑥ link_relations(양방향) ⑧ 줄 task_id=본문 taskId · payload=NULL — 한 트랜잭션 · 어느 단계 거부 → 전부 롤백 · payload 그대로 · 변경분 0 → ⑧만 · 헤더 셀렉터 taskId 가 저장값을 이긴다
DELETE …/lines/{id} — 그 행만 · order_index 당김 0 · next_order_index max+1(8-b) · 편집 대상 트랙만 · ai 422
```

### 2-4. 리비전 0009 · 유형 설명 (A-12 · SPEC-002)
```
work_type.description text NULL · 시드 2건 UPDATE(description IS NULL 행만 · 미팅·회의 NULL) · 왕복 테스트 · 되감기 목표 리비전 id
0~200 · 줄바꿈 거부 · null 로 지움 · 기본 3종도 설명 편집 · GET /api/work-types 에 description(MCP list_work_types 통과)
work_type_repository.update None → UNSET 규약 변경 — 다른 호출자가 깨지지 않나
```

### 2-5. 프론트 — payload 드로어 둘 (FE §2 규칙 8 · MF-65 · 66 · 67 · U-9 · U-10)
```
① features/tasks/components/TaskCreateDrawer.tsx · TaskDetailDrawer.tsx diff 0 · RelationPopover 는 mode prop 하나 + 배럴 export(CROSS_AREA_ALLOWED 예외 하나 추가 — 이유 주석 · 예외 총수) · 업무 화면 다중 선택 불변
② 두 드로어 prop = prefill · submitMode 둘(모드를 가르는 것) — isAiLine · line.track === 로 가르는 코드 0
③ 액션 드로어 일곱(안건 고정 · 제목 · 유형 · 프로젝트 · 계획 시작~종료 · 설명 · 할일) · 업무 드로어 헤더 = 셀렉터(single) + 변경분 일곱(상태 둘) · 업무 미선택이면 본문 비활성 · 첨부·로그·참고자료 블록 0 · 업무 드로어에 제목·유형·설명·시작일 0
④ 푸터 save = 취소·저장 / insert = 취소·넣기 — 한 푸터에 셋 0 · 인라인 자동 저장 0 · SUBMIT_LABEL 한 자리
⑤ 본문에 채워진 키만(MSW) · 같은 상태 status 제외 · 저장 경로에 업무 API 0 · 넣기 = POST/PATCH …/task
⑥ 줄 버튼 세 상태(업무 생성 · 업무 갱신 · 갱신 완료 비활성) · dot · 툴팁 · generating 잠금 · 삭제된 업무 — 워커는 디스패치 「비활성」 대신 SPEC-008 U-6 「업무 갱신 그대로 + 캡션」을 따랐다: SPEC 문장이 그런지 확인
```

### 2-6. 프론트 — 편집 모드 · 모달 · 유형 설명 (U-7 · U-8 · FE §6 · SPEC-002)
```
① LineKindSelector 폐기 · onChangeKind 0 · AddLineDrawer 세그먼트 2값(논의|결정)
② 칩 둘 갈래 — + 논의·+ 결정 → 줄 추가 드로어 / + 연관 업무·+ 액션 아이템 → payload 드로어 바로(submitMode save · 「저장」= POST …/lines 한 요청 · 닫으면 줄 없음) — 드로어 연달아 둘 0(MF-64 정정)
③ ConfirmModal size light 420(제목 + 한 문장 + h32 · warning 없음) · 회의 삭제는 600 유지 · Dialog 직접 import = ConfirmModal 하나
④ 낙관적 — 인라인 본문 · 안건 이름 · U-8 추가 · payload 저장 O / 줄 삭제 · 넣기 X · 무효화 키(detail · tasks · schedules)
⑤ 에러 code 분기 — invalid_status_transition 409(드로어 유지 + 토스트) · validation_error 422(그 필드 인라인) · not_found 404
⑥ WorkTypePanel · InlineAddRow 설명(네 필드 · 인라인 편집 · 「설명 없음」 · 기본 3종 편집) · settings types/api
⑦ fetch 직접 0 · hex 0 · Sheet 직접 0 · localStorage 0 · retry:true 0 · WORK-014 범위(breadcrumb · 헤더 · 미리보기) 침범 0
```

### 2-7. 테스트가 WP 검증 항목을 덮나
Phase 1~5 체크리스트 ↔ 테스트 대응표. **BE §12 8-b · 8-c** 문장대로. static.test ㉓ 7건. 없는 항목을 표로.

## 3. 판정
- **PASS / WARN / FAIL**. 항목마다 **파일:줄 + 문서 절 번호**.
- **FAIL** = task.status 직접 대입 · done 뒷문 · payload 표면이 task_service 호출 · 업무 드로어 수정 · AI/사람 분기 prop · 드로어 연달아 둘 · 한 푸터 셋 · 원자성 깨짐 · 014 범위 침범.
- **WARN** = 잔재 · 테스트 공백 · 문구 · 규약 변경 파급.
- **문서 공백** = 별도 절. 워커가 올린 것 하나 — **업무 payload 드로어의 「현재 값」 둘(프로젝트 · 완료 결과)이 줄의 `task` 요약에 없다**(SPEC-008 U-9 「현재 값」 표시 규칙과 응답 형태를 대조해 공백인지 판정만 — 결정 만들지 마라).

## 4. 하지 마라
- 코드 · 문서 수정 금지. 테스트 실행 금지(코디가 돌렸다 — back 638 · front tsc 0 · vitest 340).
- 앱 창 실측은 이 검수에서 요구하지 않는다(아침 항목).
- 새 결정을 만들지 마라.

## 5. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_be2a2f22-5ec1-4354-ab88-7ccb824100d3 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: WORK-013 검수" \
  --body "FAIL n · WARN n · 문서 공백 n / 축별 판정 한 줄씩 / 리포트 경로"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] reviewer 완료 — WORK-013 검수 FAIL n · WARN n. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] reviewer: <질문>" --enter`
