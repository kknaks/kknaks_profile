# [reviewer_code] 코드 검수 1 — WP-001(backend) + WP-006 Phase 1·2(frontend)

너는 **sc-ax `reviewer_code` 워커**다. 역할 문서(절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/roles/sc-ax/reviewer/role.md` (+ `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting` (branch `kknaksss/sc-meeting`, base `origin/main` a0bcee8) — **읽기만.** 범위 = `git diff origin/main...HEAD` + untracked.

## 1. 판정 기준 (SSOT)

| 우선 | 무엇 | 어디 |
|---|---|---|
| 1 | **계약** — BE·FE 가 같은 계약을 봤는가 | `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/sc-meeting-be-brief.md` §3 · `sc-meeting-fe-brief.md` §3 (+ 코디 보강: PATCH agendas `lines?: string[]`) |
| 2 | **SPEC 0.4.1** | `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec/products/sc-ax/20-spec/spec-004-meeting-note.md` §3·§4·§5.1·§8.1·§10 |
| 3 | **WP** | 같은 리포 `30-work/work-001-meeting-agenda-domain-api.md` · `work-006-meeting-screens.md`(Phase 1·2) |
| 4 | **시안(화면 정본)** | `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/design/회의록.dc.html` · `회의실.dc.html` · 두 REPORT |
| 5 | 역할 규칙·경계 | `roles/sc-ax/backend/rules.md` · `roles/sc-ax/frontend/rules.md` · `backend/tests/architecture/` |
| 6 | 워커 완료 보고(자기보고 — 믿지 말고 확인) | 코디가 아래 §2 에 요약 |

## 2. 워커 자기보고 요약

- **backend**: 20파일. domain/application/persistence/meetings/http 재작성, note version·adopt·realtime 3라우트 제거, recordings/start·stop 은 잔존(코디 결정 A). 226 passed, reset-demo 성공, §3 대비 필드 diff 공집합. 주의점: 자동 취소는 조회 시점 판정 · 열람 축을 조직→참석으로(`meetings_visible_to`) · 생성 body 에서 organization_id·visibility 제거(visibility 컬럼 삭제) · 안건 POST 201 · **can_edit_note 가 cancelled 에서도 true**(SPEC §5.1 근거, 브리프는 done|failed) · failed→summarizing 허용 · MeetingAccessDenied 403→404.
- **frontend**: `frontend/src/meetings/` 8파일 + api/viewModels/labels/App/CalendarPage/styles. tsc 0, vitest 65/65(+D18 후 26). 시안 SCR-105 20/21 · MOD-102 18/18 · SCR-106 34/39. 안건 PATCH `lines` 덮어쓰기 소비. 스크립트 탭 빈 문구 워커 창작. MeetingDrawer·캘린더 회의 탭 미노출(파일 잔존).

## 3. 판정 축 — PASS / WARN / FAIL + 근거(파일:줄)

1. **범위·경계** — BE 는 `backend/`·Makefile·compose 만, FE 는 `frontend/` 만 건드렸는가. `tests/architecture` 규칙(domain/application 이 fastapi·sqlalchemy import 금지, entrypoints 가 platform 직접 import 금지)을 새 코드가 지키는가. FE: `api.ts` 밖 fetch 0 · hex 리터럴 0 · envelope/viewer_relation·can_edit_* 로 가시성 판단(kind 추론 0).
2. **BE↔FE 계약 일치(핵심)** — 경로·메서드·상태코드·필드명·enum 을 **양쪽 코드에서** 대조. 특히 (a) `GET /api/meetings` upcoming/past.items/next_cursor (b) MeetingDetail.meeting 의 can_edit_info/can_edit_note/viewer_relation (c) 안건 POST 201 을 FE `request<>` 가 받는가 (d) PATCH agendas `lines` (e) DELETE `?scope=` (f) quick-start (g) 오류 404/409/422 를 FE 가 어떻게 그리는가. 어긋남은 FAIL.
3. **SPEC·WP 정합** — WP-001 Phase 1~3 검증 항목이 테스트로 덮였는가(허용 안 된 전이·안건 21번째·안건 삭제→줄 삭제·비참석자 404·목록 격리·진행 중 편집 409·비소유 참석자 편집 허용·note 삭제 시 회의 유지·quick-start·자동 취소/해제). BE 주의점 6개 각각이 SPEC 과 맞는지 판정(맞으면 브리프 쪽을 고칠 항목으로 WARN, 틀리면 FAIL). WP-006 Phase 1·2 검증 11항목이 FE 테스트로 덮였는가.
4. **시안 정합** — FE 화면이 시안 요소·문구·가시성 표와 맞는가. 시안에 없는 요소·문구가 생겼으면 FAIL(스크립트 탭 빈 문구는 알려진 창작 — WARN 으로 문구 위치만).
5. **품질·위험** — 열람 축 변경(`meetings_visible_to`)이 다른 소비자(캘린더·MCP·graph·material_search)를 깨뜨리지 않는가(테스트 변경 근거 확인). 자동 취소를 조회 시 commit 하는 것이 읽기 경로에 쓰기를 넣는 문제 — 위험도 판정. reset_demo 밖 스키마 변경 없는가. 폐기 코드가 라우터에서만 떼졌고 import 가 깨지지 않는가. MeetingDrawer·liveTranscription 잔존이 빌드를 깨지 않는가.
6. **검증 재현** — `cd backend && uv run pytest -q tests/architecture` 와 워커가 고친 테스트 파일들 `-m 'not integration'` 을 **1회** 실행(전체 스위트 금지) · `cd frontend && npx tsc --noEmit` · `npx vitest run src/meetings/ src/labels.test.ts` 1회. 수치 보고. 서버·DB reset·포트 사용 금지(코디가 5176/8001 을 쓰고 있다).

## 4. 산출물 — 하나

`/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting/orchestration/work/sc-meeting/review-code-01-wp001-wp006-report.md`

```
# 코드 검수 1 — WP-001 + WP-006 P1·2
## 0. 총평 — 「FAIL — 재발주 필요(BE|FE)」 / 「PASS(WARN n)」 + 6축 표
## 1~6. 축별 상세 — 위반: 파일:줄 · 무엇이 · 어느 기준과 · 권장 수정 · 담당(BE/FE/코디)
## 7. 계약 대조표 — 엔드포인트별 BE 구현 / FE 소비 / 일치 여부
## 8. 코디가 정해야 할 것 (최소로)
## 9. 검증 재현 수치 · git status
```

## 5. 하지 말 것

- 코드·문서 수정 금지. 테스트 실행은 §3-6 범위만. `make reset-demo`·`make local-stack`·dev 서버 금지.
- 시안·SPEC 의 옳고 그름을 평하지 않는다. 코드가 그것과 맞는지만.

## 6. 완료 보고 — **문구 변경 금지**

> ⚠ 핸들은 dispatch preamble 값 우선.

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_9efe51f3-aec0-44b1-94ea-f86134b6ddea \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer_code 완료: 코드 검수 1 WP-001+WP-006" \
  --body "총평 / 축별 / FAIL 목록(담당) / 계약 대조 불일치 수 / 코디 결정 / 검증 수치 / git status"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] reviewer_code 완료 — 코드 검수 1: <PASS/FAIL 한 줄>. 상세는 인박스." --enter
```
