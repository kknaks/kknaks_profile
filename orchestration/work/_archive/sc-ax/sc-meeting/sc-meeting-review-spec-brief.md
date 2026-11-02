# [reviewer_spec] 검수 1 — SPEC-004 재작성(0.3.0) · 10-decision · system.md §4

너는 **sc-ax `reviewer_spec` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/roles/sc-ax/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec` (branch `kknaksss/sc-meeting-spec`, base `origin/main` 59cd71302) — **읽기만 한다.**
코디 워크트리(read-only 참조): `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting`

## 1. SSOT — 판정 기준

검수 대상이 따라야 했던 입력이다. 대상 문서가 이것과 어긋나면 FAIL 후보다.

- **기획 정본**: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/reference/2026-09-10-sc-meeting/plan-004-meeting-note.md`(PLAN-004 v1.0.0) · `screen-005-meeting-note.md`(SCREENDEF-005 v1.0.0). `X-###`·`D-###` 는 풀지 않는다(정본 없음 — 사용자 지시).
- **사용자 결정 D1~D11**: planner 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/sc-meeting-spec-brief.md` §2 표(D1~D9) + 추가 D10(데모에서 알림 제외) · D11(데모에서 상단 AI 채팅 입력 제외).
- **현행 코드 사실**: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/survey-01-ai-provider-report.md`
- **중계 원형**: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/20-spec/spec-007-meeting-live.md` §4 · `spec-008-meeting-close.md`
- 리포 규칙: `rules/document-pipeline.md` · `AGENTS.md`

## 2. 검수 대상 (planner 산출물 — `git diff origin/main` 이 전부)

- `products/sc-ax/20-spec/spec-004-meeting-note.md` (0.2.0 → 0.3.0, 87 → 426줄)
- `products/sc-ax/10-decision.md` (로그·현재 결론)
- `products/sc-ax/40-architecture/system.md` §4

planner 가 스스로 보고한 것: D1~D11 반영 위치, §11 현행 대조(폐기 7·계승 8·신설 4), §12 기획 개정 요청 12건(R-1~R-12), §13 Open Question 16건, lint --strict sc-ax 범위 0. **이 자기보고를 믿지 말고 네가 확인한다.**

## 3. 판정 축 — 각 축에 PASS / WARN / FAIL 과 근거(파일:줄 · 어긋난 SSOT 절)

1. **범위 준수** — 변경이 3파일뿐인가. `00-planning/` 에 변경이 없는가(기획자 소유). `30-work/`·ERD·타 spec 무변경인가.
2. **결정 반영** — D1~D11 각각이 SPEC 어느 절에 어떻게 박혔는지 표로. 빠졌거나 뜻이 바뀐 것은 FAIL. 특히 D1(두 트랙 + **자동** 합성, 채택 없음) · D3(재전사 **완전 삭제**) · D8(판 없음·덮어쓰기·수정은 만든 사람) · D10·D11(데모 범위 밖 처리).
3. **기획 정합** — SPEC 이 인용한 기획 ID(FTR-004-NN · SCR-105/106 요소 ID · MOD-1xx · OQ-###)가 reference 본에 실재하고 뜻이 같은가. 기획에 없는 값을 SPEC 이 **지어낸** 곳이 있는가(있으면 FAIL — Open Question 으로 갔어야 한다).
4. **§12 기획 개정 요청의 타당성** — 12건 각각이 정말 기획과 어긋나는지 reference 본에서 확인. 오독이면 WARN 으로 지적. 놓친 어긋남이 있으면 추가.
5. **계약의 완결성** — §5.3 WS 계약이 sc-ax 권한 모델(참석자·만든 사람·공유 열람)과 맞물리는가. 상태 6개 전이가 빠짐없는가. 실패·재시도 경로가 있는가. spec-007 원형을 **복사**했는지 **옮겼는지**(sc-ax 이름·ID 로).
6. **문서 규약** — frontmatter 최소셋·status draft·document_version 증가·관련 문서 경로 실재. `python3 scripts/lint-pipeline.py --strict` 재실행 결과(sc-ax 범위 ERROR/WARN 수, 타 제품은 「무관」으로 분리).

## 4. 먼저 읽을 것

- `git -C <워크트리> diff origin/main --stat` 로 범위 확정 → 3파일 diff 전문
- SPEC-004 §0(인용 규약)·§2.2·§5·§6·§7·§8·§11·§12·§13
- reference screen-005 §3 · SCR-105 · SCR-106 · MOD-102/104/105 · §7 / plan-004 §4·§7·§14·§16

## 5. allowed_paths

- **리포 파일 수정·생성 금지.** 스펙 워크트리·코디 워크트리 모두 읽기만.
- 산출물은 **단 하나**: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/review-01-spec-004-report.md`
- lint 스크립트 실행은 허용(읽기 전용 도구). 그 외 스크립트·서버·테스트 금지.

## 6. 리포트 형식

```
# 검수 1 — SPEC-004 0.3.0 리포트
- 작성: 날짜 / reviewer_spec / 대상 커밋·diff 범위
## 0. 총평 — 판정 6축 표 (축 · PASS/WARN/FAIL · 한 줄)
## 1~6. 축별 상세 — 위반 목록: 파일:줄 · 무엇이 · 어느 SSOT 절과 어긋나나 · 권장 수정
## 7. 사용자가 정해야 할 것 — 검수로 못 가르는 것만
## 8. lint 결과 원문(요약)
```

FAIL 이 하나라도 있으면 총평 첫 줄에 「FAIL — 재발주 필요」, 없으면 「PASS(WARN n)」.

## 7. 하지 말 것

- 문서를 고치지 않는다. 판정과 근거만.
- 기획 자체의 옳고 그름을 평하지 않는다 — 기획은 정본이다. SPEC 이 기획·결정과 맞는지만 본다.
- Claude Design·ax-workspace 코드·task_management 코드를 읽으러 가지 않는다.

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict 실행 → products/sc-ax/ 범위 ERROR 0 확인 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 리뷰는 read-only — 문서를 고치지 않는다. 리포트 저장 후 스펙 워크트리 `git status --porcelain` 이 planner 의 3파일(M) 그대로인지 확인해 보고에 붙인다
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 산출물은 리포트 1개뿐.
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_a53b7eb6-b86f-4486-850f-3f53f53d161c --from term_a551cbf0-0d02-43f1-a84b-4e00ed5fb398 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_spec 완료: 검수 1 SPEC-004" \
  --body "총평(PASS/FAIL·WARN 수) / 축별 판정 / FAIL 목록 / 사용자 결정 필요 항목 / lint 결과 / 워크트리 status"

# (2) 직접 주입
orca terminal send --terminal term_a53b7eb6-b86f-4486-850f-3f53f53d161c \
  --text "[worker_done] reviewer_spec 완료 — 검수 1 SPEC-004: <PASS/FAIL 한 줄>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_a53b7eb6-b86f-4486-850f-3f53f53d161c --text "[질문] reviewer_spec: <질문>" --enter`
