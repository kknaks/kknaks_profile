# [architect] SPEC-008 · WORK-008 재개 — 정합 맞추고 마무리

너는 **task-management `architect` 워커**다. **처음부터 다시 쓰지 마라. 지금까지 한 것 위에서 정합만 맞춘다.**

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app`
**산출물 2개** — `20-spec/spec-008-meeting-close.md` · `30-work/work-008-meeting-close.md`

## 0. 왜 멈췄나

병렬 발주가 원인이다. SPEC-006 이 닫히기 전에 007·008 을 동시에 띄워 이름이 갈렸다.
**직렬로 바꿨다** — SPEC-006 · 007 정정이 끝났고, 이제 네가 마지막이다.

**네가 멈추기 직전에 `tracks.*` 로 바꾸려 했는데, 그 근거였던 SPEC-007 §7-D D-4 문장은 코디의 오류였고 이미 삭제됐다.**

## ⛔ 1. 확정된 정본 — 006·007 이 이미 이대로다

| 항목 | 정본 |
|---|---|
| `MeetingDetail` 트랙 필드 | **`agendas.{human, ai, merged}`** — 각각 AgendaItem 배열, 줄은 안건 안 `lines[]` (`tracks.*` 아님) |
| 배치 회차 필드 | **`latestBatchSeq`** (`aiBatchSeq` 아님) |
| 상태 가드 에러코드 | **`invalid_meeting_status`** 하나 (`meeting_not_recording` 폐기됨) |
| 자식 쓰기 응답 | **`MeetingDetail` 전체** · 삭제만 `204` · 없는 자식 `404` |
| 안건 표면 | `PATCH …/agendas/{id}` 하나. **보낸 필드만** 바꾼다 — `title` 은 `scheduled`(006) · `ended`(너), `state` 는 `recording`(007) |
| **안건 `next` 배지 문구** | **회의 중 「대기」 / 종료 후 「다음 논의로」**(DEC-003 §1 표). **네 담당은 종료 후이므로 「다음 논의로」다** |
| `/end` 사전 조건 | **`paused/stream` 에서도 받는다.** BE §8-2 의 409 는 **오디오 요청**뿐이다. 「WS 연결 있음」 조건을 두지 마라 |
| `MeetingDetail` 정본 소유 | **SPEC-006**. 네가 더한 `durationMinutes`·`activeJobId`·`finalBatchState`·`mergedSummary`·`headline` 은 006 §4 필드 소유 표에 이미 반영돼 있다 |

**`recordingStartedAt` 은 SPEC-006 에 이미 있다**(6건). 「추가 필요」로 적지 마라.

## 2. 할 일

### 2-1. 먼저 보고할 것 — **손대기 전에**

`spec-008` · `work-008` 의 **현재 상태를 확인하고 코디에 한 줄로 보고**해라. 중단 지시를 받고 되돌리는 중에 멈춰서 절반만 정정된 상태다.

```
grep -c 'tracks\.'  ·  'aiBatchSeq'  ·  'agendas\.'  ·  'latestBatchSeq'  ·  '다음으로'  ·  '다음 논의로'
```

보고는 `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "..." --enter` 로 하고, **답을 기다리지 말고 이어서 진행**해라.

### 2-2. 정합 맞추기

- `tracks.*` → `agendas.{human, ai, merged}` · `aiBatchSeq` → `latestBatchSeq` — **0건이 될 때까지**
- 안건 `next` 배지 → **「다음 논의로」**(네 담당은 종료 후다). 「대기」로 적힌 자리를 고쳐라.
  **단 「다음으로 가지 않는다」 같은 다른 뜻은 건드리지 마라**
- `/end` 사전 조건에서 **「WS 연결 있음」·「비활성」을 걷어내라**. `paused/stream` 에서도 종료가 활성이다
- `invalid_meeting_status` 하나만 쓴다
- 자식 쓰기 응답은 `MeetingDetail` 전체
- **SPEC-006·007 을 「고쳐야 한다」고 적은 정합 항목 중 이미 해소된 것을 지워라** — 006·007 정정이 끝났다.
  네 정합 표를 다시 읽고 **살아 있는 것만 남겨라**

### 2-3. 2차 브리프의 미완분 — 이미 했으면 넘어가라

- **결정 ① AI 한 줄 요약 바**: U-1 생성중 단계 문구 · U-3 상단 `top 150 · 1640×56` 바([09] L727~733) · U-4 드로어 배치 판단 · §4 `POST /integrate` 응답에 **`headline`**(별도 호출 금지) · 우측 카운트 「안건 n · 결정 n · 액션 n」 출처 · 통합 실패 시 `headline` 처리 · §6 Acceptance · §7 에서 「한 줄 요약」과 「문단 요약」 구분(문단은 계속 제외)
- **결정 ② 줄 삭제 · 안건 이름 수정**: §7 제외 목록에서 **「편집 중 안건 제목 입력 상자 L1894·L1924·L1959」를 빼내 계약으로** · U-7 에 줄 「제거」 + 안건 제목 인라인 · §4 `DELETE …/lines/{id}` · `PATCH …/agendas/{id} { title }` · **경계 셋**(삭제는 `merged` 만 / `source_*_line_id` 원본 보존 / 업무는 안 지움) · **「되돌리기」는 계속 제외** · **줄 순서 변경 없음** · §6 Acceptance
- **WORK-008 작성** — 템플릿(`work-004`·`work-005`) 섹션 전부. Phase 마다 `be`/`fe` 담당 + 검증 방법. Done Criteria 수 = SPEC §6 Acceptance 수
  - Depends on: **WORK-006**(도메인·`MeetingDetail`) · **WORK-007**(AI 배치·`AgendaLineTree`·근거 칩·트랜스크립트) · **WORK-005**(`PATCH /api/tasks/{id}/status`·완료 게이트) · **WORK-004**(`task_service`·`task_memo`)
  - **선행 WP 가 못박은 것을 지켜라** — `work-005` L137 「회의록의 업무 갱신은 `PATCH /api/tasks/{id}/status` 하나만 지난다. 회의록 쪽에 판정 코드를 두지 않는다」 · L147 「`task.status` 대입은 `change_status()` 안에만」 · `work-004` L156
  - **`AgendaLineTree` 는 WORK-007 것이다.** 통합본 탭도 같은 컴포넌트다 — 두 번째 구현 금지

## 3. 하지 마라

1. **SPEC-006 · SPEC-007 · WORK-006 · WORK-007 을 건드리지 마라.** 정정이 끝났고 006 은 코드가 돌고 있다
2. **기획·정책·아키텍처·시안을 고치지 마라**
3. **처음부터 다시 쓰지 마라.** 지금 파일 위에서 고친다
4. **커밋·push 하지 마라**
5. **기획·정책에 없는 기능을 만들지 마라.** 시안에 있어도 — §7 에 「시안 L### 에 있으나 기획·정책에 없어 제외」로
6. **OQ 를 쓸 거면 「어디를 찾았나(파일·섹션·grep 문자열·건수)」를 함께 적어라.** 없으면 반려한다.
   **SPEC·WP 가 정하면 되는 것**(API 경로·에러코드·검증·수치·Phase 분할)은 묻지 말고 정해라

## 4. Done Criteria

- [ ] `grep -c 'tracks\.'` = 0 · `grep -c 'aiBatchSeq'` = 0 (두 파일)
- [ ] 안건 `next` 배지가 **「다음 논의로」**
- [ ] `/end` 에 「WS 연결 있음」·「비활성」이 없다
- [ ] 정합 표에서 **해소된 항목이 지워졌다**
- [ ] 결정 ①·② 가 U-n · §4 · §6 **세 곳 전부**에 있다
- [ ] §7 제외 목록에서 **안건 제목 입력 상자가 계약으로 옮겨졌다**
- [ ] WORK-008 이 템플릿 섹션 전부 · Phase 마다 검증 방법
- [ ] WORK-008 Done Criteria 수 = SPEC-008 §6 Acceptance 수
- [ ] **네 파일 2개 외 변경 0건**

## 5. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from term_e9fc284a-afbb-442b-aa52-8c3e2cd070fe \
  --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "SPEC-008 · WORK-008 정합 + 마무리 완료" \
  --body "재개 시점의 파일 상태 / 치환 건수(tracks·aiBatchSeq·배지) / /end 사전 조건 변경 / 정합 표에서 지운 항목 / 결정 ①·② 를 넣은 자리(U-n·§4·§6) / 제외에서 계약으로 옮긴 것 / WORK-008 Phase 구성과 Done Criteria 수 / OQ 건수와 각각의 「어디를 찾았나」 / 손대지 않은 것"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] SPEC-008 · WORK-008 완료. 상세는 인박스." --enter
```
