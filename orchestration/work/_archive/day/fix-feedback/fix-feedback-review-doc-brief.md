
# [reviewer_doc] fix-feedback 스펙 개정(SPEC-002 ㉑ · SPEC-005 · SPEC-003 ⑰) 검수 (read-only)

너는 **day `reviewer_doc` 워커**다. 너는 앞 맥락이 없다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-feedback-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

planner 는 끝났다(해제됨). 이 워크트리 파일을 고치지 마라 — 리포트 1개만.

## 1. SSOT — 먼저 읽을 것

- **사용자 결정 정본**: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/fix-feedback-spec-brief.md` §1 결정 표(F-1 · F-2 · F-3 · F-4 · F-6 · F-7 · 범위 밖) — 스펙이 이 표를 빠짐 · 넘침 없이 담았는지가 검수 기준.
- 원천: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/e2e-feedback.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/_RESUME.md` §2 · 조사 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/research-1-report.md`.
- 리뷰 대상: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-feedback-spec` 미커밋 5파일(`git -C /Users/kknaks/orca/workspaces/mediness-mediness/fix-feedback-spec diff`) — `products/day/20-spec/spec-002-procedure-board.md`(개정 ㉑) · `spec-005-notifications.md`(2026-11-17) · `spec-003-mobile-app.md`(⑰) · `20-spec.md` · `log.md`.
- planner 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/spec-report.md` · Delivery Issue #254(`gh issue view 254 -R MediSolveAIDev/CENTURION_DAY`).
- 코드(읽기만 · 계약 사실 대조): `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-feedback` (dev `4f8316a7`).

기대는 개념: 해당 없음.

## 2. 배경

사용자 2026-11-17 DAY 현장 피드백을 planner 가 스펙에 반영했다. 다음은 코드(be · fe) 발주다 — 코드 워커가 이 스펙만 보고 짓는다. 빠짐 · 넘침 · 모순 · 코드 사실과 어긋남을 잡는다.

## 3. 계약

해당 없음(검수).

## 4. 먼저 읽을 핵심 파일

위 §1.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정·생성 금지. 산출물은 브리프가 지정한 리뷰 리포트 파일 1개뿐)`

## 6. 검토 항목

1. 결정 표 F-1 · F-2 · F-3 · F-4 · F-6 · F-7 하나하나가 스펙에 있는가(절 · 줄) — **빠짐**.
2. 결정 표에 없는 정책 · 화면 문구가 들어갔는가 — **넘침**. 허용 글자는 사용자 말(「귀가 대기 취소」 · 「시술순」 · 「방별순」(임시) · 「바로 시작 · N건」 · 「의사 호출 · N건」 · 「수락」)과 기존 스펙 글자뿐.
3. F-3: 11-09 「원장 없이 시작 없음」 계열 문장(U-7 · 규칙 10 · 20 · S-4 · S-6 · 케이스 매트릭스 · KOS 쓰기 표)을 products/day/ 전체에서 grep — 취소선 · 기록 문맥이 아닌 **살아 있는 옛 문장**이 남았는지, 새 규칙(집도의 없으면 시스템 계정 `change-tasks-doctors` → 기존 시작 쓰기)과 서로 모순되는 곳이 없는지. 새 엔드포인트 계약(경로 · 본문 · 응답 · 409 코드)이 코드 워커가 지을 수 있을 만큼 닫혔는지.
4. F-1 되돌리기 · F-4 SSE/알림 · F-7 분기 · F-6 매크로 서술이 코드 사실(`/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-feedback`)과 맞는지 — 파일:줄 대조.
5. F-4 「원장 계정 웹에서만 뜬다」 서술이 SPEC-005 받는 계정 규칙과 맞는지.
6. OQ-58 ~ 66 · OQ-N8 ~ N13 이 열린 것으로 정직하게 적혔는지, 그리고 **코드 착수를 막는 OQ**(기본값 없이는 못 짓는 것)를 따로 표로 — 각 OQ 에 planner 가 적은 기본값이 있는지.
7. `python3 scripts/lint-pipeline.py --strict` — products/day/ ERROR 0.

## 7. 범위 제약 — 하지 말 것

- 파일 수정 금지(리포트 1개만). 커밋 · push · Issue 수정 · 승인 금지.
- 고객 값 · 키 · 토큰 · 계정 이메일 출력 금지.

## 8. 검증

```
SPEC·WORK 를 DEC·baseline 에 대조. lint-pipeline --strict 로 products/day/ ERROR 0. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
```

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/review-doc-1-report.md` — 판정(PASS/WARN/FAIL) · 지적마다 파일:줄 + 근거 + 고칠 방향 · 착수 막는 OQ 표.

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
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
