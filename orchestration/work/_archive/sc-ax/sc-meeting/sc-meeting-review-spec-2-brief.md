# [reviewer_spec] 검수 2 — SPEC-004 0.4.0 · WP-001~006 · 10-decision · system.md §4

너는 **sc-ax `reviewer_spec` 워커**다. 검수 1(0.3.0)을 했던 세션이면 그 맥락을 써도 되나 **판정은 새로** 한다. 역할 문서:

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/roles/sc-ax/reviewer/role.md` (+ `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec` — **읽기만.**
코디 워크트리(read-only): `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting`

## 1. 판정 기준 (SSOT) — 이번엔 **디자인이 정본**이다

| 우선 | 무엇 | 어디 |
|---|---|---|
| 1 | **시안** — 화면의 SoT | `orchestration/work/sc-meeting/design/회의록.dc.html` · `회의실.dc.html` + `design/REPORT-회의록-v2.md` · `REPORT-회의실-v2.md` |
| 2 | **사용자 결정** D1~D15 | `orchestration/work/sc-meeting/sc-meeting-spec-brief.md` §2(D1~D9) · `sc-meeting-spec-fix-brief.md` §2(F-1·D12·D13·D14·W·R-12) · D10 알림 제외 · D11 AI 채팅 제외 · **D15 디자인이 정본**(기획서와의 차이는 §12 한 줄 목록만) |
| 3 | **백엔드 원형** = task-management | `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/20-spec/spec-007-meeting-live.md` §4 · `spec-008-meeting-close.md` · 코드 `/Users/kknaks/git/toy_pr2/task_management/app/back/api/meeting_stream_router.py` · `service/meeting_stream_service.py` · `meeting_batch_service.py` · `meeting_finalize_service.py`(읽기만) |
| 4 | 검수 1 리포트(F-1·WARN 11 이 해소됐는지의 기준) | `orchestration/work/sc-meeting/review-01-spec-004-report.md` |
| 5 | 현행 코드 사실 | `orchestration/work/sc-meeting/survey-01-ai-provider-report.md` |
| 6 | 기획 정본(참고 — §12 목록의 대조용일 뿐, 본문 판정 기준 아님) | `reference/2026-09-10-sc-meeting/*.md` |

## 2. 검수 대상 — `git status` 그대로

- M `products/sc-ax/20-spec/spec-004-meeting-note.md` (0.4.0, 518줄)
- M `products/sc-ax/10-decision.md` · `30-work.md` · `40-architecture/system.md`
- ?? `products/sc-ax/30-work/work-001~006-*.md` (6건, 149~183줄)

planner 자기보고(믿지 말고 확인): F-1 해소(§2.2 신설·§5.2-7·§5.3 pause/resume 제거), D12 §4.2·§6-5·§7.1·§8-5·§10-7, D13 §5.1 전체, D14 §3.1·§4.1·§8-5·§10-18, WARN 11 전부 처리, §12 R-1~R-30, §13 OQ-303·306·006 종결 + OQ-311~314 신설, SCAX-ESC-006 신설, WP-001~006 각각 Covers SPEC·BE/FE 계약·폐기/계승 파일·Phase 검증.

## 3. 판정 축 — PASS / WARN / FAIL + 근거(파일:줄)

1. **범위** — 변경이 위 목록뿐인가. `00-planning/` 무변경.
2. **검수 1 해소** — F-1 이 완전히 걷혔는가(「일시정지·재개·마이크·다른 창에서」 본문 grep 0, §2.2 데모 범위 밖 행 존재). WARN 11 각각의 처리 여부 표.
3. **디자인 정합(핵심)** — SPEC 본문이 시안과 맞는가. 최소 확인: 상태 6(예정·진행 중·정리 중·**완료**·실패·취소됨)과 시안 `screenState` 값 · 안건 줄 목록/다음 할 일/「연관 업무 ›」 · 진행 중 탭 둘(메모/AI 요약)·완료 후 합쳐진 회의록 · 머리 편집(제목·일시·참석자·장소 글자, 예정·완료) · 자료 행 클릭 → 드로어(PDF·MD) · 삭제 확인 모달(×·[회의록만 삭제]·[회의 취소]) · 공유 모달(조직도 2단) · 자료 첨부 모달 · 바로 시작(AI 즉시 안건·제목 후보·참석자 직접). **시안에 없는 화면 조작·문구를 SPEC 이 만들었으면 FAIL.** 시안과 SPEC 이 다르면 FAIL(시안이 이긴다).
4. **결정 반영** — D12~D15 가 자기보고한 절에 실제로 있는가. D13 이름 「정리됨」이 본문에 남았으면(§12 인용 제외) FAIL.
5. **WP 완결성** — 6건 각각: (a) Covers SPEC 절이 실재하고 그 절과 내용이 맞는가 (b) BE/FE 계약(엔드포인트·WS 프레임·필드)이 SPEC §5.3 등과 모순 없는가, WP 간에 같은 계약을 다르게 쓰지 않았는가 (c) task-management 원형 인용(문서 절·코드 경로)이 **실재**하는가 — 경로 하나하나 `ls`/`grep` 으로 확인 (d) 폐기/계승 파일이 survey-01 §11 과 맞는가 (e) 검증 기준이 실행 가능한가(구체 명령·조건) (f) `30-work.md` Status Board·WP List·Spec Coverage 가 6건과 동기됐는가. 빠진 범위가 있으면(예: 목록 삭제/취소, 자동 취소 X-185, 내보내기) WARN 으로 열거.
6. **문서 규약** — frontmatter 최소셋(WP 6건 포함), `templates/30-work.md` 형식 준수, `document_version` 0.4.0, `sources:` 경로 실재. `python3 scripts/lint-pipeline.py --strict` sc-ax 범위 ERROR/WARN 수.

## 4. allowed_paths

- 리포 파일 수정·생성 금지. 산출물 **하나**: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/review-02-spec-004-report.md`
- lint 실행만 허용. 서버·테스트 금지.

## 5. 리포트 형식

```
# 검수 2 — SPEC-004 0.4.0 + WP 리포트
## 0. 총평 — 「FAIL — 재발주 필요」 또는 「PASS(WARN n)」 + 6축 표
## 1~6. 축별 상세 — 위반: 파일:줄 · 무엇이 · 어느 기준(시안/결정/원형)과 어긋나나 · 권장 수정
## 7. 사용자가 정해야 할 것 (검수로 못 가르는 것만 — 최소로)
## 8. lint 원문 요약 + git status
```

## 6. 하지 말 것

- 문서를 고치지 않는다. 기획서의 옳고 그름을 평하지 않는다. **시안의 옳고 그름도 평하지 않는다** — 시안은 정본이다.
- ax-workspace 코드를 읽으러 가지 않는다(survey-01 로 충분). task_management 코드는 경로 실재·계약 대조에만.

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 다르면 preamble 이 맞다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_a551cbf0-0d02-43f1-a84b-4e00ed5fb398 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context> \
  --subject "reviewer_spec 완료: 검수 2 SPEC-004 0.4.0 + WP" \
  --body "총평 / 축별 판정 / FAIL 목록 / WP 6건 판정 / 사용자 결정 필요 / lint / git status"

# (2) 직접 주입
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] reviewer_spec 완료 — 검수 2: <PASS/FAIL 한 줄>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라.
