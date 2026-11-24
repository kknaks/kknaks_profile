# [reviewer_doc] SPEC-002 U-14 개정(명시적 저장 · 시술전후사진) 문서 검수

너는 **day `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec` — **read-only**. planner 가 남긴 미커밋 변경(`git -C /Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec diff` · `git status`)을 검수한다.

**너는 앞 맥락이 없다.** 이 브리프와 아래 파일이 전부다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md` ← 사용자 결정 C1 ~ C16 · KOS 사진 흐름 · 아직 안 정한 것. **검수의 기준.**
- planner 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/day-chart-photo-spec-brief.md` — 무엇을 시켰고 무엇을 금지했나(§6 · §7)
- planner 완료 보고 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/planner-1-report.md`(있으면)

**기대는 개념**: 해당 없음

## 2. 배경 / 무엇을 바꾸나

DAY-SPEC-002 차트 모달(U-14 · 규칙 31)을 자동 저장 → 탭별 명시적 저장으로 바꾸고, 시술전후사진 탭(KOS 사진 올리기 · 삭제)과 웹 헤더 로그인 표시를 더한 SPEC 개정을 검수한다. 이 판이 통과하면 커밋 · PR 뒤 Delivery Issue 가 이 SPEC 을 baseline 으로 발행된다 — **코드 워커가 이 문서만 보고 구현할 수 있는지**가 기준이다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음.

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec/products/day/20-spec/spec-002-procedure-board.md`(+ 바뀌었으면 `spec-001-login-session.md`) · `20-spec.md` · `10-decision.md` · `log.md` — `git diff origin/main` 로 바뀐 곳 전부
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec/products/day/00-baseline/planning/` 시술 현황 기획안 §4-2(차트)
- 코드 사실 대조(read-only): `git -C /Users/kknaks/git/CENTURION_DAY show origin/dev:<path>` — `backend/day/services/board_charts.py` · `templates/base.html` · `emr/kos/staff_client.py` · `.agents/skills/verify-day-web/features/clinical-chart.md`
- KOS 사진 실물: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/*.har`(모양만) · cc 기록 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/_archive/cc-prototype/overall-board/app-backend-report.md` 「WP-BE5」 · 「여권 사진 분류」

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정·생성 금지. 산출물은 브리프가 지정한 리뷰 리포트 파일 1개뿐)`

## 6. 구현 단계

1. 결정 C1 ~ C16 이 하나씩 SPEC 에 반영됐는지 표(결정 → SPEC 절:줄 → 반영/누락/어긋남)
2. **자동 저장 잔재 전수** — SPEC-002 전체에서 「자동 저장」 · 「2초」 · 「커서가 나갈 때」 · 「저장 버튼은 없다」 류 문장을 grep 으로 전부 세고, 살아 있는 문장(취소선 아님)이 남았는지
3. 발명 검사 — 결정 · 기획안 · HAR · 코드에 근거 없는 정책 · 화면 글자가 계약으로 들어갔는지(OQ · 「기본값(코디 제안)」 표시가 있으면 허용)
4. 금지 검사 — 사진 DB/Blob 저장 · 코드 테이블 · 권한 변경 · 앱 범위 · HAR 값(토큰 · URL · 고객 이름 · id) 유입 · 기획안 수정 · WORK 작성
5. 구현 가능성 — 저장 요청 단위 · transaction · 줄별 충돌 처리 · outbox · 사진 KOS 호출 순서 · 토큰 · 실패 경우가 코드 워커가 되묻지 않을 만큼 닫혔는지. 착수를 막는 OQ 에 기본값이 있는지
6. 케이스 매트릭스 · API 이름 제안 · KOS 쓰기 표 · §4 차이 표 · 지도/결정/log 가 서로 맞는지
7. lint

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/review-doc-1-report.md` — 판정(PASS/WARN/FAIL) · 지적마다 파일:줄 + 근거 + 고칠 방향.

## 7. 범위 제약 — 하지 말 것

- 레포 파일을 고치지 않는다(리포트 1개만) · 커밋 · push 금지
- 결정 C1 ~ C16 자체를 다시 열지 않는다 — 결정이 이상해 보이면 「사용자 확인 필요」로 따로 적는다

## 8. 검증

```
SPEC·WORK 를 DEC·baseline 에 대조. lint-pipeline --strict 로 products/day/ ERROR 0. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
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
  --to term_fae12a17-bcf2-4cd6-8e83-5f06c52bfc17 --from term_1c95f60f-45d5-4c05-96af-5157798267d2 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_fae12a17-bcf2-4cd6-8e83-5f06c52bfc17 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_fae12a17-bcf2-4cd6-8e83-5f06c52bfc17 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
