# [reviewer] 4회 — mobile 6판(review-code-3 WARN 반영) 재검수

같은 역할 · 같은 워크트리(미커밋). 읽기 · 시험만. 맥락: 이 폴더의 `review-code-3-report.md`(네가 낸 W-1~3) · `app-6-instructions.md` · `app-6-report.md` · `app-6-shots/`.

## 볼 것
1. W-1: 워커 전수 표(23개)를 직접 grep 으로 다시 세어 빠진 바닥 목록이 없는지 · `listEndInset` 이 iOS · 폰에서 0 인지 · `chart_sheet.dart` 추가 고침이 맞는지 · 새 테스트(TargetPlatformVariant)가 실제 배선을 지나는지 · 스크린샷 02 가 맞는지.
2. W-2/W-3: `play_upload.py` 짝 검사 · choices · commit 뒤 읽기 실패 exit 0. 실제 Play 쓰기 금지(`tracks` 읽기는 됨).
3. 루트 `.gitignore` 추가가 이미 추적 중인 파일을 숨기지 않는지(`git ls-files -ci --exclude-standard` 0).
4. 비밀 grep · analyze · test 수치.

## 산출물
`review-code-4-report.md` — PASS/WARN/FAIL · 근거. 완료 보고는 1판 리뷰 브리프의 두 명령(새 preamble 값).
