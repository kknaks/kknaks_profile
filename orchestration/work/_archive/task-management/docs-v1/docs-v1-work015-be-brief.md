# [backend] WORK-015 Phase 1~2 — 중간 배치는 AI 혼자 쓴다(MF-71): 옵션 빌더 `phase` · 배치 프롬프트 조회 절 삭제 · 미러 갈래 삭제

너는 **task-management `backend` 워커**다. 오늘 아침 실물 회의(id 9)에서 AI 요약이 사람 노트의 톤을 그대로 따라간 것을 사용자가 보고 결정을 바꿨다 — **회의 중 AI 는 사람 것을 보지 않는다.**
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

## 0. 어디서 무엇을 보나

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`, HEAD = 스키마 수정 `dd9d861` + LineRow 커밋 위). 도커 스택이 떠 있고 api 는 `--reload` 다 — 지금은 회의가 없으니 고쳐도 된다.

문서는 전부 **코디 워크트리 절대경로 · 읽기 전용**이다.
```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/
  30-work/work-015-meeting-batch-solo.md       ← 네 빌드 계획 전부. Code Surface · Internal Interface · Phase 1·2 검증 · Open Issues(웜스타트 phase=final 가정 · get_meeting/get_account 도 중간엔 닫힘)
  20-spec/spec-007-meeting-live.md v0.0.3      ← §4 도구 표 「단계」 열(중간 셋/최종 일곱) · allow list 두 벌 · 배치 입력 3행 · 출력 humanAgendaId null · 검증 2(무시 · 폐기 아님) · 3(업무만) · 5(source_agenda_id 항상 NULL) · §5 · §6 AC
  10-decision/decision-003-meeting-notes.md    ← §2 · §4 · §8 「단계별 도구」
  40-architecture/backend/README.md            ← §5-2(배치 입력 · 옵션 빌더 phase) · §12 테스트 6 · 7 · 7-b
  40-architecture/database/domains/meeting.md  ← M-6 · M-7(ai 는 source_agenda_id 항상 NULL)
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/reference/2026-09-06-task-management-app/Meeting flow.md §0 MF-71 · §2-3 본문   ← 결정 원본
```

## 1. 범위 — Phase 1 · 2 (백엔드만 · 프론트 0)

```
Phase 1  integrations/agent.py build_codex_options(…, phase: Literal["batch","final"]) — enabled_tools batch = list_tasks · get_task · list_work_types 셋 / final = 일곱 · tools.<n>.approval_mode 도 그 셋/일곱만 · 옵션 문자열 테스트(batch 줄 수 · final 줄 수 · batch 문자열에 list_agendas|get_agenda|get_meeting|get_account 0)
         호출자 — meeting_batch_service 배치 제출 = "batch" · meeting_finalize_service ② = "final" · 웜스타트(WORK-010 launch_warm_start) = "final"(WP Open Issues 가정 · 사용자 확인 대기 — 바꾸기 쉽게 한 자리)
Phase 2  meeting_batch_service.build_batch_prompt — 「정리하기 전에 이 순서로 조회해라」 절 · 「안건이 발화 구간마다 늘어나면 잘못」 문구 삭제 → 「발화만 보고 네가 안건을 가른다 · 업무를 가리킬 때만 셋을 부른다 · 앞 배치 것도 포함해 처음부터 다시(전량 교체)」
         _parse_output(fill_final=False) — humanAgendaId 를 무시(값이 와도 폐기 아님 · null 저장) · 최종(fill_final=True)은 불변
         _persist(회의 중) — 미러 갈래(source_agenda_id 복사 · 제목 복사) 삭제 → source_agenda_id 항상 NULL · 제목은 출력 title 그대로 · 최종 경로(merged) 불변
         BE §12 6(humanAgendaId 실려 와도 폐기 아님) · 7 · 7-b 테스트 · 정적: 배치 프롬프트 문자열에 list_agendas|get_agenda 0 · 「조회」 0
```

## ⛔ 2. 하지 말 것 · 이미 있는 것

```
스키마 한 벌(meeting_notes.json)   건드리지 마라 — humanAgendaId 필드는 남는다(최종이 쓴다). 회의 중엔 서버가 무시
전량 교체 · 검증 순서 0~5          그대로. 검증 2가 「무시」로 바뀌는 것뿐
최종 경로(fill_final=True · merged) 불변 — list_agendas · get_agenda · 사람 안건 정확히 한 번 규칙 그대로
웜스타트 프롬프트 문구             건드리지 마라(WORK-010 소관 · WP Open Issues 관찰 항목)
MCP 서버(app/mcp/)                 일곱 그대로 노출 — 잠금은 워커 -c 뿐
프론트                             0. 미러 배지 죽은 갈래는 별건
except Exception · 임의 재시도 · 조용한 기본값 금지
```

## 3. 계약

- **`build_codex_options(*, session_id, output_schema, timeout_sec, meeting_token, phase)`** — `phase="batch"` 면 `enabled_tools` 셋 + 그 셋의 `approval_mode` · `"final"` 이면 일곱. 나머지 `-c` 줄은 같다. `-c` 는 resume 에도 산다(open-kknaks 2.1.2 adapter).
- **배치 프롬프트** — 발화 + 「AI 트랙 전체를 다시」 + 업무 참조 셋 안내. 안건·사람 줄 조회 지시 0.
- **회의 중 저장** — `humanAgendaId` 무시 · `source_agenda_id NULL` · `title` 출력 그대로 · `state` NULL.

## 4. allowed_paths
```
app/back/
```

## 5. 검증
WP §Execution Phase 1 · 2 검증 체크리스트 전부. 특히 — 옵션 문자열 batch 에 안건 도구 0 · final 일곱 · `humanAgendaId: 12` 가 실려 온 회의 중 출력이 폐기되지 않고 `source_agenda_id NULL` 로 저장 · 미러 테스트(있으면) 삭제·대체 · 최종 경로 테스트 불변(그대로 통과) · BE §12 7-b.
```bash
cd /Users/kknaks/orca/workspaces/task_management/docs-v1 && make test    # 전체 · Errors 0
```
**실물** — 코디가 스택을 띄워 뒀다. `make test` 뒤 워커 컨테이너 로그로 다음 회의에서 확인하는 것은 사용자 몫 — 네가 회의를 만들지 마라.

막히면 30분 넘기지 말고 §9 (2) 로 물어라.

---

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_fd9fc1ce-619d-4f87-b218-10dfaefaa275 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: WORK-015 Phase 1~2" \
  --body "변경 파일 목록 / Phase 별 구현 요약 / 검증 결과(수치 · 정적 grep) / 계약 준수 / 미결·주의점"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] backend 완료 — WORK-015 중간 배치 AI 혼자. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] backend: <질문>" --enter`
