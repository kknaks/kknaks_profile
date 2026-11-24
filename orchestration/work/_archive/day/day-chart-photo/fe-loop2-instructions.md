# [frontend] 2루프 — e2e 1회차 피드백 (C28 · C29 · C30)

**읽을 것** (이 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/`)
- `e2e-1-feedback.md`
- 결정 파일 C28 ~ C30
- SPEC 고침 `planner-fix-10-report.md`(mediness #960 최신)

## 할 것

**C28 — 여러 장 올리기**
- 사진 파일 칸에 `multiple` 을 넣는다.
- 고른 파일 전부를 한 요청에 보낸다.

**C29 — 토스트**
- 차트 탭 저장이 거절되면(409 · 400) 서버 `message` 를 토스트로 띄운다.
- 지금 빈 값 처리가 막고 있지 않은지 확인한다.

**C30 — 사진 탭 다시 읽기 · 열려 있는 동안 동기화**
- 사진 탭을 고를 때마다 다시 읽는다.
  - 지금은 `day:photos-load` 를 처음 한 번만 부른다.
- 탭이 보이는 동안 10초마다 다시 읽는다.
  - 다른 탭으로 가거나 모달을 닫으면 멈춘다.
  - 올리기 · 삭제 요청 중에는 겹치지 않게 한다.

## 하지 마라
- backend 파일은 건드리지 않는다.
- 커밋하지 않는다.

## 검증
- 화면 pytest
- `npm run -s check`

## 보고
- `fe-loop2-report.md` 를 쓴다.
- preamble worker_done 두 채널로 알린다.
