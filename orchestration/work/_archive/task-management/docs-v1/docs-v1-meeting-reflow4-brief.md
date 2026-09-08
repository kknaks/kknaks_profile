# [architect] 회의록 계약 정정 4차 — MF-71 「중간 배치는 AI 혼자 쓴다」 전파 + WORK-015

너는 **task-management `architect` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/architect/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app`

**`docs-v1-meeting-reflow3-brief.md` 의 후속이다.** WORK-009~014 가 전부 코드로 들어갔고(코드 워크트리 `kknaksss/docs-v1` HEAD `5c72c25`), 오늘 아침 실물 회의 두 번(id 8 · 9)에서 결정 하나가 새로 닫혔다.
정본은 `reference/2026-09-06-task-management-app/Meeting flow.md` — **§0 표의 MF-71 과 §2-3 본문**(MF-50 · 51 행의 괄호 정정 포함)이다. 브리프 문장이 아니라 **그 본문을 읽고** 옮겨라.

---

## ⛔ 옮길 것 — MF-71 하나 · 닿는 문서 넷 · WP 하나

### 1. 무엇이 바뀌나
```
전    중간 배치가 list_agendas · get_agenda 로 사람 안건·줄을 읽고 미러 안건(source_agenda_id)을 만든다 (MF-50 · 51 · WORK-011)
후    중간 배치는 발화만 보고 AI 혼자 안건·줄을 만든다. 사람 것을 보지 않는다
      - 도구: 중간 = list_tasks · get_task · list_work_types 셋 (enabled_tools 자체가 셋 — 프롬프트 지시가 아니라 설정)
             최종 = 일곱 그대로
      - humanAgendaId 는 중간에 항상 null(서버가 무시) · 미러 없음 · AI 안건 전부 신설(source_agenda_id NULL)
      - 전량 교체(MF-53) · 스키마 한 벌(MF-52) · 검증 순서 0~5 · 최종(MF-56) · 프론트는 그대로
```

### 2. 닿는 문서 — 하나씩 열어 낡은 문장을 네가 찾아라(grep `list_agendas` · `get_agenda` · `미러` · `source_agenda_id` · `humanAgendaId` · `조회 순서` · 「안건이 늘어나면」)
```
10-decision/decision-003-meeting-notes.md   §4(배치 입력 · AI 트랙 안건 축) · §2/§8 도구 표(중간/최종 도구 수) · OQ 가 있으면 닫기
20-spec/spec-007-meeting-live.md             §4 「배치 입력」 · 「AI 도구 7개」 불릿(중간 셋/최종 일곱) · 「배치 출력」(humanAgendaId 중간 null) · 검증 순서 표 3행(참조 검사는 업무만) · U-4(AI 탭 — 미러 표시가 있으면 삭제) · §6 AC(「워커가 list_agendas 를 부른 흔적」 → 「부르지 않은 흔적」) · §7 변경 이력
40-architecture/backend/README.md            §5-2(배치 입력 · 조회) · §8-1 옵션 빌더(enabled_tools 가 phase 별로 다르다 — build_codex_options 에 인자 하나) · §12 테스트 6·7
40-architecture/database/domains/meeting.md  M-6/M-6-a(AI 안건 source_agenda_id — 중간엔 항상 NULL · 최종에서만 값) · M-7
reference/2026-09-06-task-management-app/ai-prompt-draft.md §B   조회 순서 절에 폐기 표시(코디가 §B 에 이미 정정 블록 하나 넣어 둠 — 그 아래에 MF-71 한 줄)
```
`spec-008` · `frontend/README.md` 는 닿지 않을 것이다 — 확인만 하고 손대지 마라.

### 3. WORK-015 (신규) — `30-work/work-015-meeting-batch-solo.md`
WORK-011 의 후속. **백엔드만**(프론트 0). 형식은 `work-011-meeting-live.md` 와 같게(frontmatter · Code Surface · Internal Interface · Phase · 검증 · Done Criteria · Open Issues · Related).
```
Phase 1  integrations/agent.py build_codex_options(…, phase: "batch"|"final") — enabled_tools 셋/일곱 · 옵션 문자열 테스트(WORK-009 의 14줄 표 갱신)
Phase 2  meeting_batch_service — build_batch_prompt 에서 「조회 순서」 절 · 「안건이 발화 구간마다 늘어나면 잘못」 삭제 · 「발화만 보고 네가 가른다」 · _parse_output(fill_final=False) 가 humanAgendaId 를 무시(null 강제 · 값이 와도 폐기 아님) · _persist 미러(source_agenda_id 복사) 갈래 삭제(중간) · 최종 경로(fill_final=True)는 불변
         BE §12 6·7 테스트 갱신 · 정적: 배치 프롬프트에 list_agendas|get_agenda 0 · 중간 옵션 문자열에 그 둘 0
Depends  WORK-011 · 012(둘 다 done)
```
`30-work/README.md` 표에 WORK-015 행(todo) + 발주 순서 문장.

---

## 하지 마라
- 새 결정 만들지 마라. MF-71 본문에 없는 것은 「아직 안 정한 것」으로 WP Open Issues 에.
- 코드 워크트리 금지. `orchestration/` 금지(코디 것).
- `decisions-pending.md` · `walkthrough-fixes.md` 근거로 쓰지 마라.

## 산출물
- 고친 문서 넷 + `ai-prompt-draft.md` 한 줄 + `work-015-meeting-batch-solo.md` + `30-work/README.md`
- 보고: `orchestration/work/docs-v1/docs-v1-meeting-reflow4-report.md` — 문서별 「어느 절 · 전/후 한 줄」 표 · 새로 드러난 결정 필요 항목(있으면)

---

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_58393ecb-2acf-44c6-840a-d0ec4310db1c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "architect 완료: 회의록 계약 정정 4차(MF-71) + WORK-015" \
  --body "문서별 변경 요약 / WORK-015 Phase 요약 / 결정 필요 항목 / 보고 경로"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] architect 완료 — MF-71 전파 + WORK-015. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] architect: <질문>" --enter`
