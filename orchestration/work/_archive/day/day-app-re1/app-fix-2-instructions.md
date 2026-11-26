# [mobile] app-fix-2 — review-code-2 AW1 ~ AW7

너는 day `mobile` 워커다. 역할 · 워크트리 공유 · 검증 · 완료 보고는 `app-2-instructions.md`(같은 폴더)를 그대로 잇는다(먼저 읽어라 · allowed_paths · 금지 같음). 대상 코드 = 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1` HEAD `fb08fe4e`. backend 워커가 같은 때 `backend/` 를 고친다 — 너는 `app/` 만. 커밋 금지.

읽을 것: `review-code-2-report.md`(같은 폴더) AW1 ~ AW7 전부.

## 고칠 것

1. AW1 — Android 스캔 화면 FLAG_SECURE · 최근 앱 썸네일 막기(효과 없는 `excludeFromRecents` 정리) · 리포트에 실제 효과 사실대로
2. AW2 — 카메라 시작 실패 = 닫기와 구분 · [손으로 입력]으로 · 받은 요청을 조용히 canceled 하지 않음
3. AW3 — 손 입력 칸 형식 검사(성별 · 날짜 · 국가 코드 · 여권번호 — cc 원천 · SPEC U-27 규칙만 · 새 글자는 짓지 말고 칸 표시로) · 서버 400 의 `field` 를 그 칸에 보임
4. AW4 — 여권번호 「고치기」가 체크숫자만 맞는 다른 번호를 만들지 않게(cc 원천 확인 · 근거 적기)
5. AW5 — 받은 스캔 상세 읽기 실패 = 다시 시도 또는 닫기(상태가 오래 남지 않게)
6. AW6 — Android 분석 프레임 비트맵 크기 · 재사용
7. AW7 — 정보(의존성 · 고지) · 리포트에 목록만

## 검증 · 보고

`cd app && fvm flutter analyze · fvm flutter test · fvm flutter build apk --debug · fvm flutter build ios --no-codesign` 각 1회 + Kotlin 단위 시험. 리포트 `app-fix-2-report.md`(같은 폴더 · 처분표 · 바꾼 파일:줄 · 수치). 완료 보고 = dispatch preamble 의 `worker_done` + 브리프 §9 (2) 직접 주입(subject 「mobile 완료: app-fix-2」).
