
# [reviewer] 업무 스펙 초안 4건 검수 — 근거·범위·미결 재개방 확인

너는 **strong-hajin `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

이번은 planner 리뷰다. 코드 워크트리에서 실행하되 실제 검수 대상은 아래 코디 문서 4건이다. 모두 read-only, 보고서 1개만 작성한다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/strong-hajin-work-write-brief.md` — 원 발주와 allowed_paths.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/source-issue-7.md` — 원문 계약. 우선순위·D4 제외·미결 유지·기존 요구 임의 후순위 금지 확인.
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/project.md`와 `templates/projects/` 해당 양식.
- 기대는 개념: 해당 없음. 명시된 계약과 실제 근거로 판정.

## 2. 배경 / 무엇을 바꾸나

writer가 BASE/DEC/SPEC 2건을 냈다. #7 추적 누락 0이라는 주장과 OQ-1~7 사용자 결정 필요라는 주장을 검증한다. 코디는 아직 문서를 승인하지 않았다.

## 3. 계약

확정 사항 재질문 금지, 미결 임의 기본값/후순위 금지. 구현 방식 제안을 사용자 확정이라고 쓰지 않는다. 개발주체 1인과 제품 축소 구분은 코디 해석이며 사용자 직접 명시 여부를 구분한다.

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/00-baseline/baseline-001-work-page.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-001-work-page.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-002-action-item-review.md`
- 위 문서가 인용하는 코드 및 #7 고정 revision 원문은 read-only 확인.

## 5. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/review-spec-report.md` 한 파일만 쓴다.

## 6. 구현 단계

1. 네 신규 문서를 실제로 읽고 계약과 대조한다. 코디의 index/log 작성은 별도 소유이며 원 writer에게 allowed_paths 위반으로 돌리지 않는다. `reference/2026-09-10-sc-meeting/task.md`는 사용자/다른 작업 변경이므로 제외한다.
2. 특히 다음 의심점의 사실 여부를 판정한다: OQ-6 회사 원문을 읽을 수 없다는 주장(gh 접근 가능했음), D4 제외된 과거 pending 처리를 OQ-1 게이트로 재도입, D2 미결을 이유로 문의 기능 전체 후순위 확정, PA-03/04/06 차수 임의 확정, W1의 회의 후속업무/REST/MCP/AX 동일 경로 누락, D-3의 기존 멱등성만으로 새 인자 중복 안전성이 성립한다는 주장.
3. OQ별 원문으로 해소 가능 / 기술조사 필요 / 실제 사용자 제품 결정으로 분류하고 근거 절을 적는다. 기한/승인자/판정권한은 PLAN-001 X-178~180 등 원문을 실제로 대조한다.
4. frontmatter ID·관계 중복·양식 및 spec 간 API/권한/상태 일관성 확인. FAIL이면 수정할 파일:줄과 근거를 명시한다.

## 7. 범위 제약

문서/코드 수정·커밋·push·PR·DB 작업 금지. 범위 밖 기존 부채로 FAIL 주지 않는다. 새 제품 결정을 만들지 않는다.

## 8. 검증

planner 리뷰. 역할문서의 scripts/lint-pipeline.py는 이 레포에 없으므로 실행 불가를 명시하고 현재 project.md 및 양식 대조로 검증한다. 코드 테스트는 실행하지 않는다. 최종 PASS/WARN/FAIL과 OQ 분류, 못 확인한 것은 그대로 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9de388d5-58b1-4bbe-8864-5e930def648b --from term_22586d00-1fe8-4a69-9b8f-83f5b9d8dfb1 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
