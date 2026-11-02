# [reviewer] WORK-008 SPEC 반영 검수 — planner 리뷰 모드

너는 **strong-hajin `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `rules.md` 등)

이번 모드: **planner 리뷰**(문서). **read-only** — 문서·코드를 한 글자도 고치지 않는다. 산출물은 리포트 한 장.

## 1. 대상

문서 레포(코디 워크트리) `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화` 의 미커밋 diff:

```bash
git -C /Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화 diff -- para/projects/summer-star/strong-hajin/20-spec/
```

SPEC-001 v0.4.0 · SPEC-002 v0.3.0 · SPEC-005 v0.3.0 · SPEC-007 v0.3.0 · `20-spec/README.md`.
(`30-work/README.md` 의 diff 는 코디 것 — 대상 아님)

## 2. 기준 (SoT)

- `…/strong-hajin/30-work/work-008-polish.md` — 사용자와 닫은 결정. 「이 판의 원칙」과 각 Phase 「계약」
- `…/orchestration/work/strong-hajin-polish/_RESUME.md` §1·§2 — 사용자 원문
- writer 브리프 `…/orchestration/work/strong-hajin-polish/strong-hajin-polish-write-brief.md`

## 3. 볼 것

1. **충실도** — WORK-008 의 결정이 **빠짐없이, 더하지 않고** 반영됐나. 요청별(B-02·F-01·F-03·D-01·D-02·A-01)로 반영 위치와 일치 여부. WORK-008 에 없는 결정을 SPEC 이 새로 세웠으면 FAIL
2. **충돌** — 고친 문장과 **고치지 않은 다른 절**이 서로 다른 말을 하지 않나(같은 SPEC 안, SPEC 사이). grep 으로 같은 개념의 다른 서술을 전부 찾는다(예: 간트 축 기간, 참조자 후보, AX 확인 카드·수신함, 담당자 변경, 기한 필수)
3. **인수조건** — 바뀐 계약마다 §6 AC 줄이 있고, 검증 가능한 문장인가
4. **형식** — 버전·변경 이력·결정 근거 열·frontmatter. 실명·메일 0건
5. **writer 가 연 Open Questions**(OQ-710 · OQ-O · OQ-P · OQ-608) — 각각 정말 미결인지, 다른 문서·코드 조사 리포트(`fe-survey-report.md`·`be-survey-report.md`)로 답이 나오는지 의견만 적는다
6. **조용히 통과하는 자리** — 취소선으로 남긴 옛 문장이 여전히 유효한 것처럼 읽히는 곳, 참조 절 번호가 틀린 곳

## 4. 판정

FAIL(결정과 다른 것이 적혔다 · 충돌) · WARN(모호) · PASS. 각 지적에 `파일:줄` + 근거.

## 5. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/review-spec-report.md` ← 이 파일 하나만

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

```bash
orca orchestration send \
  --to term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: WORK-008 SPEC 검수 <PASS|WARN|FAIL>" \
  --body "판정 / FAIL·WARN 목록(파일:줄) / OQ 의견 / 리포트 경로"

orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 \
  --text "[worker_done] reviewer 완료 — SPEC 검수 <판정>. 리포트 review-spec-report.md" --enter
```
