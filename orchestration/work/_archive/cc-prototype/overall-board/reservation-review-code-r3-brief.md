# [reviewer] 예약 현황 코드 리뷰 r3 — WP-FIX3(예약 카드 드래그 · 공지 [수정하기])

너는 **cc-prototype `reviewer` 워커**다. **앞 판 맥락이 없다.** 먼저 역할 문서를 읽어라:
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/reviewer/role.md` (+ 같은 폴더 rules · skills · tools · workflow)

- **대상** = 코드 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board`(branch `kknaksss/overall-board-2`)의 **커밋 안 된 변경 전체**(`64e1989` 이후 · `git diff` + 새 파일 `procedure/back/tests/test_resv_notice.py`) — **read-only**
- **기준** = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-005-reservation-board.md` **0.4.0** — §3.2 `notice_save` · §5.4 이동 · §5.15 공지 · §6.4 · §7.2 · §7.5 · §7.6 · §9 #11 · #46 · 처분표 `orchestration/work/overall-board/reservation-review-doc-r3-dispositions.md` · `_RESUME.md` §2 2026-10-27 줄
- **워커 보고** = `reservation-fix3-backend-report.md`(추가 지시 1 절 포함) · `reservation-fix3-frontend-report.md` · 스크린샷 `fe-shots-reservation/fix3-*.png`
- **화면 정본 = 배포된 웹 구현**(D-60) — 시안 대조로 FAIL 하지 마라

## 볼 것
1. **드래그 원인 · 수정**: frontend 보고의 원인(끄는 원본 카드를 미리보기 칸으로 옮겨 그려 Chrome 이 끌기를 끝냄 → 원본 제자리 + 복제 미리보기)이 코드로 맞나 · 클릭(상세 열기)과 충돌 없나 · 끌 수 없는 카드(`draggable` false)는 그대로 막히나 · 정원 찬 칸 막기 · KOS 거절 원위치 · 길이 유지 회귀
2. **공지 back ↔ front 계약**: 요청 `{date, noticeId?, content}` · 응답 · 409 `notice_past_date` · 400 · `noticeEditable` · 저장 대상(요청 noticeId 우선 → KOS 첫 번째 → create) · 빈 값 = delete / 호출 없음 · trim 2000(back · front 같은 기준) · 캐시 비움 · 편집 중 날짜 이동 = 버림 + 토스트 · 실패 = 편집 유지
3. **`event_log(notice_save)` 키**: SPEC §3.2 = `{date, noticeId, op}` ↔ 구현(planner 보고: `action` · `length`?) — 다르면 어느 쪽인지 적고 FAIL/WARN 판정
4. 회귀: 시술 현황(SPEC-003) · 경로 수 35 · 가짜 모드 403 · 기존 시험
5. DS 컴포넌트만(native select · date · time · textarea 기본 위젯 0) · public 누출(실명 · KOS id · 키 · 토큰 0)

**짧게** — FAIL 은 사용자 E2E 를 막는 것만. 직접 `uv run ruff check . && uv run pytest -q` · `npx tsc --noEmit && npm run lint` 를 돌려 수치를 적어라(사용자 포트 3700 · 8700 금지 · 파일 수정 금지).

## 산출물
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-review-code-r3.md` 1개

## 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

```bash
orca orchestration send \
  --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_ea5c6e85-3bb1-4476-82db-32eac19f54ea \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "reviewer 완료: 예약 현황 코드 r3 <판정 한 줄>" \
  --body "리포트 경로 / FAIL n · WARN n / FAIL 목록 한 줄씩 / 고칠 사람(backend · frontend)"

orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 \
  --text "[worker_done] reviewer 예약 현황 코드 r3 — <판정>. 상세는 reservation-review-code-r3.md" --enter
```
