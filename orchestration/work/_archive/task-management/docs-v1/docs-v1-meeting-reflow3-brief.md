# [architect] 회의록 계약 정정 3차 — payload 드로어를 회의록 것으로 · MCP 배치 · 토큰 · 웜스타트 닫기

너는 **task-management `architect` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/architect/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app`

**`docs-v1-meeting-reflow2-brief.md` 의 후속이다.** 2차 계약을 사용자가 검수했고 결정 다섯이 새로 닫혔다.
정본은 `reference/2026-09-06-task-management-app/Meeting flow.md` — **§0 표의 MF-64(정정) · MF-67 · MF-68 · MF-69 · MF-70 과 각 본문**이다. 브리프 문장이 아니라 **그 본문을 읽고** 옮겨라.

**2차 정정 중 폐기되는 것이 있다.** 「업무 탭 드로어에 슬롯을 얹어 재사용」(MF-13 · 14 옛 문장 · SPEC-003 회의록 문단 · frontend 규칙 8)은 **MF-67 로 뒤집혔다.** 네가 2차에서 쓴 문장을 네가 지운다.

---

## ⛔ 옮길 것 다섯

### 1. MF-67 — payload 드로어는 회의록 것이다 (MF-13 · 14 정정)

```
전    업무 탭의 새 업무 드로어 · 업무 상세 드로어에 agendaSlot / taskSelectorSlot · prefill · submitMode 를 얹어 재사용
후    회의록 payload 드로어를 따로 만든다. 업무 드로어는 손대지 않는다

액션 payload 드로어   안건(고정) · 제목 · 유형 · 프로젝트 · 계획 시작 ~ 종료 · 설명 · 할일  = payload 키
업무 payload 드로어   헤더 업무 셀렉터(RelationPopover 단일 선택 · 0건이면 「전체」)
                     기한 · 상태(todo|in_progress) · 진행 메모 · 할일 추가 · 연관 · 프로젝트 · 완료 결과  = 변경분 일곱
둘 다               AI 줄/사람 줄 구분 없음(MF-65) · 편집 「취소 · 저장」 / 보기 「취소 · 넣기」(MF-66) · 인라인 자동 저장 없음
```

**RelationPopover 는 그대로 쓴다** — 업무 화면 부품이고 드로어가 아니다. 단일 선택 prop 하나는 남는다.

### 2. MF-64 정정 — 칩은 둘로 갈린다 (「칩 넷이 같다」 폐기)

```
+ 논의 · + 결정        줄 추가 드로어(U-8) → 「추가」에 줄. 닫으면 줄 없음
+ 연관 업무 · + 액션   payload 드로어가 바로 뜬다 → 「저장」에 줄 + payload 한 요청. 닫으면 줄 없음

서버   POST …/lines 가 액션·업무 줄에 한해 payload(업무 줄은 taskId 도)를 받는다
       2차에서 뺀 「422」 를 이 모양으로 되돌린다. 업무는 여전히 안 생긴다 — task_service 를 안 부른다
       논의·결정 줄에 payload 가 오면 422 그대로
```

「드로어를 닫아도 줄은 남는다」는 논의·결정에만 성립한다. U-8 은 논의·결정 전용이 된다(종류 고정 갈래 삭제).

### 3. MF-66 전파 — 푸터 모드별

SPEC-008 · SPEC-003 · frontend README 에는 이미 있다. **DEC-003 §5 업무 연동 · ERD `meeting.md` M-14 · M-14-a** 에 없다. 「둘 다 「넣기」」 류 문장을 「편집 「저장」 / 보기 「넣기」」로.

### 4. MF-68 · MF-69 — MCP 별도 컨테이너 · 단명 토큰 = auth_session 행 (DEC-003 OQ-9 · SYS-OQ-4 닫힘)

```
MCP    app/mcp/ 별도 서비스. compose 에 back · worker · mcp 셋. FastAPI 안에 두지 않는다
토큰   auth_session 에 kind='meeting' 행 — /start 때 INSERT · MCP 헤더 · ② 종결 시 행 삭제(best-effort)
       무상태 JWT 안 쓴다(폐기 표면 없음)
```

### 5. MF-70 — 웜스타트 실패 처리 없음 (DEC-003 OQ-8 닫힘)

```
별도 기록 · 재시도 · 재웜스타트 갈래를 만들지 않는다. 예외 전파 로그뿐
회의 중 = 배치 미제출(SPEC-007 검증 0) · 종료 후 = ② final_failed(SPEC-008) — 이미 있는 경로
```

---

## 산출물 — 어느 문서 어느 절

```
20-spec/spec-008-meeting-close.md
  U-6(여는 드로어 설명) · U-7(칩 넷 문단) · U-8(논의·결정 전용으로 — 종류 고정 갈래 삭제) ·
  U-9 · U-10(payload 드로어 규격으로 재작성 — 「SPEC-003 U-1/U-3 + 슬롯」 문장 전부) ·
  §4 API 표 · POST lines 본문·Validation(payload 갈래 복원) · Case Matrix validation_error 행 ·
  Flow · 구현 규칙(submitMode 문장 · 「AI/사람 분기 반려」는 유지) · S-6~S-9 · AC · §7 닫은 것 · 정합 #1(삭제) · §8 근거 표
  OQ 처리 표(OQ-8 · OQ-9 행)

20-spec/spec-003-tasks-crud.md
  U-1 · U-3 의 「회의록에서 열 때」 문단 **삭제** · U-8 의 「회의록도 이 팝오버를 그대로 쓴다(단일 선택)」는 **유지**

10-decision/decision-003-meeting-notes.md
  §2 AI 데이터 접근(토큰) · §5 업무 연동(드로어 · 푸터 · 칩) · §7 웜스타트 행 · §8 AI 도구 연결(MCP 배치 · 토큰) ·
  OQ-8 · OQ-9 닫기 · 머리말 「결정 31건 → 34건 · MF-1 ~ MF-70」 · Resulting Spec

40-architecture/database/domains/meeting.md   M-14 · M-14-a(푸터 · payload 드로어) · 머리말
40-architecture/database/domains/account.md   auth_session 에 kind 컬럼(meeting) — A-7 계열 불변식에 한 줄
40-architecture/database/README.md            §1 ERD auth_session 컬럼 · §2 표
40-architecture/backend/README.md             §4 디렉토리(app/mcp 별도 · ai_schemas 각주) · §5-2(토큰 발급·폐기 자리 확정 · OQ-8 문장) · §8-3 웜스타트 행 · §10 MCP 행 · §11 env(MCP_* 필요하면) · 머리말
40-architecture/system/README.md              Components MCP 행 · §codex(토큰 문장) · 흐름 ③(토큰 INSERT/삭제) · SYS-OQ-4 닫기 · 머리말
40-architecture/frontend/README.md            §2 규칙 8 재작성(회의록 payload 드로어 둘 · 업무 드로어 미수정) · FE-18 · 머리말
```

**`docs-v1-meeting-reflow3-report.md` 에 보고한다.** 다섯마다 「어느 문서 어느 절을 어떻게」 표. 끝에 grep 셋 —
`agendaSlot|taskSelectorSlot` 0건 · `submitMode` 는 SPEC-008 U-9/U-10 과 frontend 규칙 8 에만 · 「31건」 0건.

---

## 지킬 것

```
□ 다섯만 옮긴다. 다른 MF 를 건드리지 마라
□ 새 결정을 만들지 마라 — 본문에 없으면 멈추고 물어라
□ payload 드로어의 시각 참조는 **이미 만들어진 새 업무 드로어 · 업무 상세 드로어**(SPEC-003 U-1 · U-3 · 코드 `TaskCreateDrawer` · `TaskDetailDrawer`)다.
  입력 · 셀렉터 · 일정 · 할일 · 메모 · 완료 결과 블록을 그 규격으로 가리켜라. 새 시안은 없다. 옛 회의록 드로어 시안(L2306~2882)은 payload 가 없어 참고하지 않는다
□ RelationPopover 재사용 · MF-65(AI/사람 분기 없음) · MF-66(모드별 푸터) · MF-59(done 안 보냄) 는 그대로
□ POST lines 의 payload 복원은 액션·업무 줄에만. 논의·결정은 422 유지. task_service 호출 없음
□ 끝나고 grep — agendaSlot · taskSelectorSlot 0건 · 「업무 탭 드로어」「슬롯만 더한다」 가 회의록 드로어 설명에 남아 있으면 안 된다
```

---

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_09af09a4-5e04-4d80-ae68-1db18f7128a6 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "architect 완료: 회의록 계약 정정 3차" \
  --body "변경 파일 목록 / 다섯 항목별 어느 절 / grep 셋 결과 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] architect 완료 — 회의록 계약 정정 3차. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] architect: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
