# [reviewer] WORK-015 검수 — 중간 배치는 AI 혼자(MF-71): 옵션 빌더 phase · 프롬프트 · 미러 갈래 삭제

너는 **task-management `reviewer` 워커**다. **read-only** — 코드를 고치지 않고 테스트도 돌리지 않는다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/reviewer/role.md`

## 0. 범위

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`, HEAD `aa375ed`). **아직 커밋 전** — 범위는 미커밋 변경 전부(백엔드 7 파일).
```bash
git status --short                      # tauri.conf.json 은 범위 밖
git diff HEAD -- app/back
```
**산출물** — `orchestration/work/docs-v1/work015-review-report.md` **1개**.
문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`(읽기 전용)

## 1. 네 층
```
정책       decision-003 §2(단계별 도구 · 잠금은 enabled_tools) · §4(AI 트랙 안건 축 — 발화만 보고 가른다 · 미러 없음 · 배치 입력) · §8 「단계별 도구」 행
아키텍처    backend/README.md §5-2(배치 입력 · 옵션 빌더 phase) · §10 · §12 테스트 6 · 7 · 7-b
           database/domains/meeting.md M-6 · M-7(ai 는 source_agenda_id 항상 NULL)
SPEC       spec-007 v0.0.3 §4 도구 표 「단계」 열 · allow list 두 벌 · 배치 입력 3행 · 출력 humanAgendaId null · 검증 2(무시 · 폐기 아님) · 3(업무만) · 5(source_agenda_id NULL) · §5 · §6 AC(「부른 흔적이 없다」 + 신설 2)
WP         work-015-meeting-batch-solo.md Phase 1 · 2 · §Internal Interface · Open Issues(웜스타트 final 가정 · get_meeting/get_account 도 닫힘)
결정 원본   Meeting flow.md §0 MF-71 · §2-3 본문
```

## ⛔ 2. 반드시 볼 축
```
2-1 옵션 빌더   build_codex_options(phase) — batch 셋(list_tasks · get_task · list_work_types) / final 일곱 · approval_mode 도 그 셋/일곱만 · batch 문자열에 list_agendas|get_agenda|get_meeting|get_account 0 · final 14줄이 WORK-009 목록과 문자열·순서 동일(회귀) · phase 기본값 없음(빠뜨리면 실패) · get_gateway().run( 호출 전부 phase 명시(배치 batch · ② final · 웜스타트 final — WP 가정)
2-2 프롬프트    build_batch_prompt 에 조회 순서 절 0 · 「안건이 늘어나면 잘못」 0 · 미러 지시(humanAgendaId 에 사람 안건 id) 0 · 「발화만 보고 네가 가른다 · 사람 것 안 본다」 · 업무 셋 안내 · 「처음부터 다시(전량 교체)」 유지 · 웜스타트 프롬프트 diff 0
2-3 파서·저장   _parse_output(fill_final=False) humanAgendaId 읽고 버림(None · 폐기 아님 — 사람 안건 id 든 없는 id 든) · fill_final=True 경로 diff 0 · _persist 미러 전체(사람 안건 조회 · source_agenda_id · 제목 · state 복사)가 플래그 안 · 회의 중 False · merged True · _run_once 의 사람 안건 조회 삭제(브리프 밖 최소 변경 — 타당한가)
2-4 불변        스키마 파일 diff 0 · 전량 교체 · 검증 0~5 자리 · MCP 서버 diff 0 · WORK-012 최종 테스트 무수정 통과 · 프론트 0
2-5 테스트      BE §12 6 확장 · 7 · 7-b · 단계별 옵션 4 · 정적 2 · 대역 게이트웨이가 phase 기록 — WP Phase 1·2 체크리스트 ↔ 테스트 대응표 · 없는 항목
```

## 3. 판정
- **PASS / WARN / FAIL** · 항목마다 파일:줄 + 문서 절.
- **FAIL** = batch 옵션에 안건 도구 · 회의 중 미러 잔재(source_agenda_id 채움) · humanAgendaId 로 폐기 · 최종 경로 변경 · 스키마/MCP 변경.
- **문서 공백** = 별도 절(웜스타트 phase 는 이미 §1 사용자 항목 — 다시 세지 마라).

## 4. 하지 마라
코드·문서 수정 금지 · 테스트 실행 금지(코디가 돌린다 — 워커 652) · 새 결정 금지.

## 5. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_be2a2f22-5ec1-4354-ab88-7ccb824100d3 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: WORK-015 검수" \
  --body "FAIL n · WARN n · 문서 공백 n / 축별 판정 한 줄씩 / 리포트 경로"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] reviewer 완료 — WORK-015 검수 FAIL n · WARN n. 상세는 인박스." --enter
```
- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] reviewer: <질문>" --enter`
