# [reviewer] 시술 현황 코드 리뷰 — WORK-008(2계층 · 드래그 놓기 W2 · 한글 발음)

너는 **cc-prototype `reviewer` 워커**다. **앞 판 맥락이 없다.** 먼저 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/reviewer/role.md`(+ 같은 폴더 rules · skills · tools · workflow)를 읽어라.

- **대상** = `/Users/kknaks/orca/workspaces/cc-prototype/overall-board`(branch `kknaksss/overall-board-2`)의 **커밋 안 된 변경 전체**(`901267f` 이후 · `git diff`) — **read-only**
- **기준** = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md` **0.6.0(r7 · r8)** §5.12 · §5.14(대조표 ● 바꿈 / ○ 그대로) · §6.3 · §9 #27~#32 · 부록 K · `30-work/work-008-procedure-board-v2.md` · 처분표 `orchestration/work/overall-board/procedure-review-doc-r5-dispositions.md`
- **워커 보고** = `orchestration/work/overall-board/procedure-fe-v2-report.md` · 스크린샷 `fe-shots/v2-*.png`
- 화면 정본 = 배포된 웹 구현(D-60) — 시안 대조로 FAIL 하지 마라

## 볼 것
1. §5.14 ● 줄이 전부 바뀌고 ○ 줄이 그대로인가(grep 전수) · 색 = 예약 현황 `phaseStyle` 재사용 · **예약 현황 화면 값 무변경**(`components/reservations/**` diff 0 확인)
2. W2: 판(흰 판 전체) 안 어디든 마지막 미리보기로 저장 · 판 밖 · Esc · 미리보기 없음 = 저장 없음 · 귀가 대기 카드 · 필터 중 · 경합(다른 화면 순서 SSE) 회귀
3. 발음: 빈 값 · 말줄임 · `title` · 오른쪽 칸 한 줄(W5)
4. `fake_board.py` = 예시 값만 · 카드 수 5 · back 다른 파일 diff 0
5. 시술 현황 회귀(되돌리기 · 호출 · 체크 · 시작/종료) · DS 컴포넌트만 · public 누출 0

직접 `cd procedure/back && uv run pytest -q` · `cd procedure/front && npx tsc --noEmit && npm run lint` 수치를 적어라(사용자 포트 3700 · 8700 금지 · 파일 수정 금지). **짧게 — FAIL 은 사용자 E2E 를 막는 것만.**

산출물: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/procedure-review-code-r3.md` 1개

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_3432bee9-d298-4960-b87f-bbf87ab7a0ae --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "reviewer 완료: 시술 현황 코드 <판정 한 줄>" --body "리포트 경로 / FAIL n · WARN n / FAIL 목록 / 고칠 사람"
orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[worker_done] reviewer 시술 현황 코드 — <판정>. 상세는 procedure-review-code-r3.md" --enter
```
