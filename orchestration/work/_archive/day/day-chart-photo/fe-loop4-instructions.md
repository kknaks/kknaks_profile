# [frontend] 4루프 — C36 413 토스트 글자

## 넣을 글자
결정 파일 C36: 413 자리(`data-day-toast-on="413"`)에 「한 번에 올릴 수 있는 용량(100MB)을 넘었습니다」

## 빠진 장 토스트
- 「올리지 못한 사진이 있습니다 …」는 backend 가 `message` 로 준다
- 받은 글이 지금 경로로 그려지는지만 확인한다

## 검증
- `scripts/test.sh -q backend/tests/architecture backend/tests/day/web`
- `npm run -s check`

## 보고
- 커밋 금지
- 보고 파일 `fe-loop4-report.md`
- preamble worker_done 두 채널
