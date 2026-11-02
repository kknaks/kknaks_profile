# [reviewer_spec] planner 리뷰 — MCP 도서관 발행 SPEC-013·060 개정 초안 검수

너는 **mediness `reviewer_spec` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/orchestration/roles/mediness/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/mcp-library-publish-spec`
base 브랜치: `origin/mediness` → 최종 PR 대상 `mediness`

**리뷰 모드: planner 리뷰 (문서 리포 diff).** read-only — 리포 파일을 수정·생성하지 않는다.
산출물은 리뷰 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/orchestration/work/mcp-library-publish/review-spec-report.md`

## 1. 검수 대상과 SSOT

- diff: `git diff origin/mediness...HEAD` + untracked — 예상 범위는 5파일: `spec-013-baseline-publish.md` · `spec-060-mcp-surface.md` · `spec-003-capability-rbac.md` · `20-spec.md` · `log.md`
- 원 워커 브리프(allowed_paths 포함): `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/orchestration/work/mcp-library-publish/mcp-library-publish-spec-brief.md`
- 사용자 확정 요구 (개정이 이걸 지켰는지가 1순위 검수 항목):
  1. MCP 도서관 발행 도구 신설 — 기존 REST 의 thin wrapper, 새 정책 발명 없음
  2. MCP 경유 발행은 **시스템 관리자 capability 전용** — 툴 선언층 + back 재판정층 **두 층 모두**. 웹 발행(`baseline.publish.basic`)은 좁히지 않는다

## 2. 특별 검수 항목 (일반 체크리스트에 추가)

- 전용 라우트(`agent-publishes`) + 신규 leaf(`baseline.publish.agent`) 설계가 SPEC-060 §4 원칙(툴 전용 leaf 금지 · 툴은 게이트 아님)과 **실제로 정합**한가 — 초안의 논거를 원문과 대조
- 「웹 발행 불변」 주장이 diff 로 성립하는가 — 기존 3 endpoint·basic leaf 관련 서술에 변경이 없는지
- 즉시형 예외(§ '호출자 밖 쓰기는 즉시형 불가' 규율과의 긴장) 처리가 SPEC-060 원문을 왜곡 없이 인용했는가, OQ 로 남긴 것이 규약(§6 머리)대로인가
- SPEC-003 leaf index 2행 수정이 최소인가 (그 이상 손댔으면 위반)
- frontmatter status 를 stable 로 유지하고 ⏳ 라벨로 초안성을 표현한 처리가 lint 게이트 규칙상 타당한가

## 3. 검증 명령

```
python3 scripts/lint-pipeline.py --strict → products/mediness/ 범위 ERROR 0 확인 (타 제품 기존 WARN/ERROR 는 '무관' 분리 보고)
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. subject 에 판정(PASS/WARN/FAIL)을 박는다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_915b3ecb-68dd-4d26-98f7-ef3f645318fb --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_spec 완료: <판정 — 한 줄>" \
  --body "판정 / 위반 목록(파일:줄+근거) / 확인한 것 / 리포트 경로"

# (2) 직접 주입
orca terminal send --terminal term_915b3ecb-68dd-4d26-98f7-ef3f645318fb \
  --text "[worker_done] reviewer_spec 완료 — <판정> <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라.
