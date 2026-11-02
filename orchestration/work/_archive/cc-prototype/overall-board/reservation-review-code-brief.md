# [reviewer] 예약 현황 코드 리뷰 r1 — SPEC-005 0.2.0 ↔ 코드 (WP-E2E 의 리뷰 몫)

너는 **cc-prototype `reviewer` 워커**다. **앞 판의 맥락이 없다.** 먼저 역할 문서를 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리(코드 · **read-only**): `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` (branch `kknaksss/overall-board`) — 리뷰 대상 = **커밋 안 된 작업 트리 전체**(`git status` · `git diff` · 새 파일). 앞 커밋(`d05cd88` 되돌리기까지)은 대상 아님.

## 1. 기준

- 계약 = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-005-reservation-board.md`(0.2.0) · 작업 = `30-work/work-007-reservation-board.md`(WP-E2E 행 「reviewer:」 칸 그대로) · 결정 `10-decision/decision-006-reservation-board.md`
- **SPEC 보다 우선하는 추가 지시** = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-impl-addendum-1.md`(W1~W5) · 코디 허가: backend 가 `procedure/.env.example` · `procedure/README.md` 에 env 이름 줄 추가(허용) · W3 파일 5개 허용
- KOS 본문 기준 = `orchestration/work/overall-board/reservation-kos-probe-report.md`(K1~K10)
- 회귀 기준 = `20-spec/spec-003-procedure-board.md` 0.5.1 · `spec-004-procedure-app.md`
- 워커 보고: backend(인박스 요약 — 「SPEC 과 다르게/해석한 곳」 5개) · frontend(「SPEC 과 다르게 한 곳」 5개 · 스크린샷 `orchestration/work/overall-board/fe-shots-reservation/`)

## 2. 할 일 — 각 지적 `파일:줄` + 근거 + 판정(FAIL · WARN · PASS)

1. SPEC §1 ~ §8 ↔ 코드(부록 A 의 절 전부) — 특히 접수 묶음(§5.6 · 0단계 갈래 · 건너뛰기 · 다시 읽기 · 멈춤 · `step`) · 신분 조건(U2) · 두 구역(U1) · 수납 필요(카드 · [귀가 완료] 막기) · 2계층 상태 · 정원 미리 막기 · 이동 길이 · 고객 저장(다시 읽은 묶음 + 바꾼 칸) · 특이사항 묶음 · 오류 코드 매핑 · `can.*`
2. 기본값(§10 「planner 기본값」 줄 · addendum)이 코드에 그대로인지 · 워커가 「다르게 한 곳」 10개가 SPEC 문장 안의 해석인지, 계약 위반인지
3. KOS 호출 본문 = WP-KOS 판정 모양(경로 · 키). 운영 키 · 실제 테넌트 하드코딩 0
4. **시술 현황 회귀**: 헤더 · 계정(코디 추가) · 수락(`service/actions.py`) · 동기화 루프 · 기존 시험. `uv run pytest -q` · `npx tsc --noEmit` 는 돌려도 된다(읽기 · 포트 안 씀)
5. 계층 규약(router → service → repository · ORM 은 repository 밖으로 안 나감 · 아래층은 HTTP 모름 · 도메인 예외) · 기능 폴더 밖 import 0 · allowed_paths 이탈
6. public 누출: 실명 · KOS id · 키 · 토큰 · 이메일(grep)

## 3. allowed_paths

- 산출물 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-review-code-r1.md`. 코드 수정 금지 · 사용자 포트(3600 · 8600 · 3700 · 8700) · 프로세스 금지 · KOS 호출 금지

## 4. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

```bash
orca orchestration send \
  --to term_fa2737b7-e69a-40e1-9fac-019199b9dad3 --from <네 handle> \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "reviewer 완료: 예약 현황 코드 r1 <판정>" \
  --body "리포트 경로 / FAIL n · WARN n / FAIL 목록(파일:줄 · 고칠 것 · backend|frontend) / 사용자 결정 필요"

orca terminal send --terminal term_fa2737b7-e69a-40e1-9fac-019199b9dad3 \
  --text "[worker_done] reviewer 예약 현황 코드 r1 — <판정>. 상세는 reservation-review-code-r1.md" --enter
```
