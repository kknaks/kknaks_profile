# [frontend] photo fix-1 — 결정 C26 · C27

## 읽을 것
- 결정 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md` 의 C26 · C27
- `review-code-3-report.md` 의 P6 · P3

## 할 것
- **C26 삭제 확인 창**
  - 글자 「사진을 삭제할까요?」 · 버튼 [취소] [삭제]
  - 차트 미저장 확인 창(E59)과 같은 모양 · 같은 방식으로 만든다
  - [취소]를 누르면 요청 0
- **C27 토스트**
  - 서버가 `message` 를 넘기면 토스트를 그린다(지금 방식 그대로)
  - 글자는 서버가 준다

## 하지 마라
- backend 파일
- 커밋

## 검증
- 화면 pytest
- `npm run -s check`

## 보고
- `fe-photo-fix-1-report.md`
- preamble 의 worker_done 두 채널
