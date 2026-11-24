
# [reviewer] DAY 차트 탭 저장(WP①) · 모달 화면(WP③) 코드 검수

너는 **day `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-chart-photo`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

**read-only.** backend · frontend 의 미커밋 변경(`git diff origin/dev` · `git status`)을 검수한다. 파일 수정 · stash · checkout 금지.

## 1. SSOT — 먼저 읽을 것

**너는 앞 맥락이 없다.**
- WP · 계약 K1 ~ K5 · 공통 e2e: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/delivery-1-report.md` · 결과 계약 · Acceptance: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/delivery/request-be-chart.json` · `request-fe.json`
- 계약 보충: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/contract-k3-header-note-1.md`(헤더 header_staff · K3 값 이름 · 검사 담당 나눔)
- SPEC: `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec/products/day/20-spec/spec-002-procedure-board.md` 개정 ㉘(U-14 · 규칙 31 · API · 매트릭스) · `spec-001-login-session.md` 개정 ⑫ — 커밋 `a896cda0`
- 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md`(C1 ~ C17)
- 워커 보고: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/be-1-report.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/fe-1-report.md` · 레포 `AGENTS.md`

**기대는 개념**: 해당 없음

## 2. 배경 / 무엇을 바꾸나

차트 자동 저장 → 탭별 명시적 저장 + C17(저장 전 KOS 확인 · 하나라도 다르면 저장 0 · KOS 글 + 줄바꿈 + 내 글) · 옛 줄 저장 경로 삭제 · 모달 탭 3(사진 탭은 구조만 — 사진 서버 WP② 는 아직 없음 · 범위 밖) · 헤더 「이름 직군」. 1루프 구현을 계약대로 세웠는지 본다.

## 3. 계약

K1 ~ K5 + 보충 1 · 2 그대로.

## 4. 먼저 읽을 핵심 파일

- `backend/day/services/board_charts.py`(save_chart_tab · _kos_now · _save_row) · `policies/board_chart_tabs.py` · `routers/board.py` · `web.py` · `session.py` · `templates/partials/board_chart_tab.html` · `board_chart*.html` · `base.html` · `static/day.js`
- 지운 것: 옛 `/board/tasks/{id}/chart` · `/api/tasks/{id}/chart` · `verification_chart_races.py` · `verification_faults.py` · `chart-recovery.test.mjs` — 지운 이유가 맞는지(지킬 성질을 같이 지우지 않았는지)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정 금지. 산출물은 브리프가 지정한 리포트 파일 1개뿐)`

## 6. 구현 단계

1. C17 판정 — 검사 순서 · KOS 읽기가 transaction 밖 1회 · 걸리면 이력 · outbox · event 0(rollback) · 이어 붙인 글 · 안 보낸 줄 KOS 판정 안 함 · KOS 실패 = DAY 만 · 시술 전 의사차트 · 반영 대기 줄
2. 저장 — 방문 잠금 · transaction 1 · `visit.chart_save` 1행 + outbox 묶음 · 규칙 27 줄마다 · 그대로인 줄 건너뜀 · 담당자 거절 탭 전체
3. 화면 — 자동 저장 경로 0(grep: blur · input 타이머 · 2초) · [저장] 노출 조건 · 바뀐 줄만 전송 · 409 조각 교체 · 확인 창(✕ · Esc · 바깥) · 「최근 저장」 탭마다 · 헤더 · 인라인 script/style 0 · 지어 넣은 글자 0
4. 지운 테스트 · 검증 스크립트가 지키던 성질 중 명시적 저장에서도 남아야 하는 것(동시 저장 · 응답 유실 · 닫기 중 실패)이 새 테스트로 옮겨졌는지
5. 「조용히 통과하는 자리」 · 사용자가 실물에서 만날 자리(로컬 e2e 에서 볼 것 목록)
6. 관문 명령 1회씩: `scripts/test.sh -q backend/tests/day/board backend/tests/day/web` · `cd backend && uv run ruff check day tests` · `cd scripts/frontend && npm run -s check`

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/review-code-1-report.md` — 판정 · 지적 파일:줄 · 근거 · 실물 e2e 체크리스트.

## 7. 범위 제약 — 하지 말 것

- 파일 수정 · 커밋 · 사진 서버(WP②) 요구 · SPEC 재논의(결정 문제는 「사용자 확인 필요」로 따로)

## 8. 검증

```
각 지적에 파일:줄 + 근거(SPEC 절 · DEC D-번호). 판정 FAIL · WARN · PASS. 「조용히 통과하는 자리」를 따로 본다
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_fae12a17-bcf2-4cd6-8e83-5f06c52bfc17 --from term_1b967637-b488-40a4-8a36-00c3ebec0496 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_fae12a17-bcf2-4cd6-8e83-5f06c52bfc17 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_fae12a17-bcf2-4cd6-8e83-5f06c52bfc17 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
