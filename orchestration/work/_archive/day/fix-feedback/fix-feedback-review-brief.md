# [reviewer] fix-feedback 코드 검수 — F-1 · F-2 · F-3 · F-4 · F-6 · F-7 (read-only)
# [reviewer] <한 줄 제목>

너는 **day `reviewer` 워커**다. 너는 앞 맥락이 없다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-feedback`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

be · fe 는 끝났다(해제됨). 이 워크트리 파일을 고치지 마라 — 리포트 1개만.

## 1. SSOT — 먼저 읽을 것

- 스펙(계약 SoT · 미커밋): `/Users/kknaks/orca/workspaces/mediness-mediness/fix-feedback-spec/products/day/20-spec/spec-002-procedure-board.md` 개정 ㉑(+ 보충) · `spec-005-notifications.md` 2026-11-17 개정. 「기본값(코디 2026-11-17 · …)」 값이 계약이다.
- 코디가 스펙보다 우선으로 박은 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/fix-feedback-fe-brief.md` §3 아래 「재검수 review-doc-2 반영」(D1 undo-home = 판 전체 다시 받기 · sort 는 GET 쿼리만 · D2 · D5).
- 브리프: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/fix-feedback-be-brief.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/fix-feedback-fe-brief.md` · 결과: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/be-1-report.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/fe-1-report.md`.
- 결정 원천: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/e2e-feedback.md` · 조사 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/research-1-report.md`.
- 리뷰 대상: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-feedback` 미커밋 diff(`git -C /Users/kknaks/orca/workspaces/CENTURION_DAY/fix-feedback diff` + `??` 새 파일) · base dev `4f8316a7`. 레포 `AGENTS.md`.

기대는 개념: 해당 없음.

## 2. 배경

DAY 현장 피드백 구현 1루프. 다음 단계는 사용자 로컬 E2E 다. 계약 위반 · 회귀 · 조용히 통과하는 자리를 잡는다.

## 3. 계약

be ↔ fe: `services/board.py` `quick_start` · `undo_home` · `board(..., sort=)` (be 리포트 「계약 대조」 — `ActionResult` 하위 · 선택 인자 `now` 차이는 코디 수용).

## 4. 먼저 읽을 핵심 파일

위 §1 · diff 전체.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정 금지. 산출물은 브리프가 지정한 리포트 파일 1개뿐)`

## 6. 검토 항목

1. 결정 · 스펙 대조 — F-1 · F-2 · F-3 · F-4 · F-6 · F-7 각각 스펙 규칙 34 · 35 · 36 · 37 · SPEC-005 웹 OS 알림 · U-6 과 코드가 맞나(파일:줄).
2. **F-3** — 줄 판정 순서 · 수락 줄 `task_not_waiting` · 귀가 대기 묶음 409 · 시스템 계정 경로의 outbox 순서(`change-tasks-doctors` doctors_equal → `change-flow-step` → 의사차트 글) · 한 transaction · `event_log` 1행 · 시스템 계정 KOS id 없음 409 `conflict` · 단건 [시작] `no_doctor` 그대로 · 앱 API 회귀 없음.
3. **F-1** — 직전 단계 계산 · `visit_flow_log` · KOS `change-flow-step` · 화면 응답(HX-Trigger 판 다시 받기)이 실제로 카드를 다시 앉히는지(`day.js` 경로 추적) · 방별순에서도.
4. **F-2** — `sort` 가 GET 쿼리로만 · SSE `hx-get` · 판 다시 받기에서 유지 · 방별순에서 끌기 · 순서 저장 막힘 · 기본값이면 지금 순서와 같음.
5. **F-4** — 공통 틀 스트림이 로그인 화면 · 권한 없는 계정에서 오류 없이 · `document.hidden` · `tag` · 중복 · 권한 요청 시점 · 인라인 스크립트 0 · `/board` 기존 SSE 와 충돌.
6. **F-6 · F-7** — off 아이콘 0 · 원장 계정 판정(`me_listed`) · 간호 계정 팝오버 회귀(fe 리포트: 「보는 사람이 원장이면 본인」 기본 선택 갈래 사라짐 — 의도와 맞나).
7. 테스트 — 새 테스트가 위 계약을 실제로 단언하나 · `pytest -m "not infra"` 를 1회 직접 돌려 수치 확인(로컬 스택 · Docker 금지 · infra 는 코디가 따로). ruff 1회.
8. 「조용히 통과하는 자리」 · **사용자가 E2E 에서 만날 자리**를 따로 모아라.

## 7. 범위 제약 — 하지 말 것

- 파일 수정 금지(리포트 1개만) · 커밋 · push 금지 · 사용자 포트 · 프로세스 · Docker · 로컬 스택 금지 · KOS 실호출 금지.

## 8. 검증

```
각 지적에 파일:줄 + 근거(SPEC 절 · DEC D-번호). 판정 FAIL · WARN · PASS. 「조용히 통과하는 자리」를 따로 본다
```

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/review-code-1-report.md` — 판정 · 지적(FAIL/WARN · 파일:줄 · 근거 · 고칠 방향) · 테스트 수치 · E2E 에서 만날 자리.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_94fbe396-828d-4fa4-8bd8-829294f10614 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
