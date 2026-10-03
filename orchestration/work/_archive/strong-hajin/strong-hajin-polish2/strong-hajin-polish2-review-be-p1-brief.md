# [reviewer] WORK-009 Phase 1 코드 검수 — backend 리뷰 모드

너는 **strong-hajin `reviewer` 워커**다. 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/roles/strong-hajin/reviewer/role.md` (+ `rules.md`). **read-only.** 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/review-be-p1-report.md` 하나.

## 1. 대상
`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish2` 의 **`backend/` 와 `docs/unified-operations-inventory.json` 미커밋 변경**(`git diff -- backend docs` · 새 `backend/tests/contract/test_task_due_date_fill.py`). `frontend/` 는 커밋됐거나 다른 판 — 대상 아님. ⚠ frontend 워커가 곧 같은 워크트리 `frontend/` 에서 2a-1 을 한다 — 건드리지 마라.

## 2. 기준
- WP `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/projects/summer-star/strong-hajin/30-work/work-009-polish2.md` **Phase 1(1-1 · 1-2 · 1-3)** · 원칙 P-1·P-2·P-4
- SPEC: SPEC-002 v0.4.0 §2.9·S-7·§4 「초안 저장」·§5·§6 · SPEC-001 v0.5.0 S-9 6·7·§5·§6·U-17 · SPEC-003 v0.4.0 「날짜 채움」 · SPEC-004 v0.3.2 §5 (`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/projects/summer-star/strong-hajin/20-spec/`)
- 발주서 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/strong-hajin-polish2-be-p1-brief.md` + 추가 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/strong-hajin-polish2-be-p1-add1.md`
- 워커 보고 원문 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/be-p1-worker-report.md` (저장 명령 FE 계약 · revise 미재사용 판단 · `_open_revised_round` 공유 · grep 개수표 · 기준선 vs 결과)

## 3. 볼 것
1. **계약 충실도** — WP 체크박스마다 코드(파일:줄). 특히 저장: pending 유지·회차 +1·diff·effect 없음·변경 없음=200 같은 회차·낡음 거부·재전송 영수증·저장 뒤 draft 없는 confirm 이 저장 값으로 업무 생성(회차 안 오름)·두 kind 에만
2. **confirm 회귀** — `_open_revised_round` 로 뺀 뒤 confirm+draft(다른 카드·MCP)가 이전과 **같은 기록**을 남기나. 트랜잭션 경계(저장이 업무를 만들지 않는 것 · 실패 시 반쯤 쓴 회차가 남지 않는 것)
3. **권한** — 저장을 누가 할 수 있나(봉투가 내린 사람만 — SPEC-002 §4 「누가」)
4. **AI 지시문** — 「ID·날짜만 지어내지 않는다」로 좁혔는데 다른 정책 절(회의 참석자·진행 묶음)의 「지어내지 말라」를 건드리지 않았나 · 답변 지침
5. **마감일 채움** — 찍는 2곳 모두 · 빈 칸만 · 서울 날짜 · 배정 검증 훅 · 스냅샷 diff · 되돌리지 않음 · 응답 타입 변경(complete 반환 `TaskDateMutationResult`)이 기존 FE 소비자를 깨지 않나(FE 가 complete 응답에서 읽는 필드를 grep)
6. **add1 라벨** — 바꾼 12 · 유지 목록(오류 문구 2 · pydantic title 7 · 프롬프트 예시)이 지시대로인가. FE 정규식 매칭이 깨지지 않나
7. **operation inventory drift** — 「도구 64개 output_schema」가 바뀌었다는 보고: 왜 64개가 바뀌었나(결과 계약 변경이 의도된 것인가 · 「실패 diff 항목만」 원칙을 지켰나) — diff 를 직접 본다
8. **SPEC 차이** — 낡음 오류가 SPEC 은 `ACTION_VERSION_STALE` 409, 코드는 기존 confirm 과 같은 422+문장. 코디 판단: **코드(기존 confirm 관례)가 맞고 SPEC 을 고친다** — 이 판단에 반하는 근거가 있으면 적는다
9. **조용히 통과하는 자리** — 빈 단언·고정 날짜로 경계를 안 보는 테스트·오늘 의존(서울 자정 경계)
10. `make test-postgres` 는 워커가 못 돌렸다 — 격리 DB 없이 돌릴 수 없으면 코디 몫으로 적는다

## 4. 판정
FAIL · WARN · PASS, 각 지적에 파일:줄 + 근거. 테스트는 Makefile 타깃만, 서버·DB(사용자 54329) 금지.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba --from term_f8b0a2d6-3e7b-41de-b8c1-2acef6635f48 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: WORK-009 Phase 1 코드 검수 <PASS|WARN|FAIL>" \
  --body "판정 / FAIL·WARN(파일:줄) / 재계수 / 화면 확인 목록 / 리포트 경로"
orca terminal send --terminal term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba \
  --text "[worker_done] reviewer 완료 — Phase 1 코드 검수 <판정>. 리포트 review-be-p1-report.md" --enter
```
