# [frontend] 3루프 — e2e 2회차 F1 · F2 · 검수 4 W2 · W4 · W7

## 읽을 것
이 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/` 의 아래 파일:
- `e2e-2-feedback.md`
- `review-code-4-report.md`
- SPEC 고침 `planner-fix-11-report.md`

## 할 것

### F2 · W2 — 10초 확인이 올리기를 깨뜨림
- 10초 확인은 **사진 목록만** 다시 그린다. 올리기 form · 파일 칸은 갈아 끼우지 않는다.
- 파일 고르기 중이거나 요청 중이면 그 회차를 건너뛴다.
- 시험: 파일 칸을 누른 뒤 10초 넘게 기다렸다 고르면 올라간다.

### F1 — 토스트가 모달 dim 뒤에 깔림
- 모달(`<dialog>` showModal)이 열려 있으면 토스트를 같은 top layer 에 띄운다.
- 방법은 둘 중 하나: dialog 안 토스트 자리 / popover.
- 대상: 차트 · 사진 모달의 모든 토스트.

### W4 — 숨겨진 탭
- `document.hidden` 이면 10초 확인을 멈춘다.
- 다시 보이면 바로 1회 확인한다.

### W7 — 삭제와 확인 응답이 엇갈림
- 삭제 요청 중이거나 직후에 온 확인 응답이 지운 사진을 다시 그리지 않게 한다.

### C33 — 본문 상한 초과
- 413(앞단 본문 상한) 응답에 오류 토스트를 띄운다.
- 글자가 SPEC 에 없으면 [질문].

## 하지 마라
- backend 파일
- 커밋

## 검증
- `scripts/test.sh -q backend/tests/architecture backend/tests/day/web`
- `npm run -s check`

## 보고
- `fe-loop3-report.md`
- preamble worker_done 두 채널
