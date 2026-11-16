# [planner] 4회차 — review-doc-3 WARN 3 반영 (짧음)

같은 역할 · 같은 워크트리(미커밋 위에 이어서) · allowed_paths `products/day/` · 커밋 · Delivery 금지 그대로.
리뷰: `/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/review-doc-3-report.md` 의 W-1~W-3 · R-1.

1. **W-1** mobile-deployment :107 「Google 쪽 등록 없음」 → 「로컬 실행 · Play 내부 테스트(2026-11-13) — Play 에 이 패키지로 올리면 바꿀 수 없음(:103)」. 전수조사에서 같은 류 낡은 줄을 한 번 더 grep(「등록 없음」 「로컬 실행만」 「Google 쪽」).
2. **W-2** §7-3-2 손 단계 2와 3 사이에 「(코드 작업) 업로드 키로 서명한 release AAB 를 만들어 넘긴다 — §7-0 · Delivery」 · 5 끝에 「참여 링크는 게시 뒤 몇 시간 걸릴 수 있다(answer/9845334)」.
3. **W-3** spec-003 :575 근처에 「로컬 빌드와 Play 빌드는 서명이 달라 한 기기에 함께 깔 수 없다 — 바꿀 때 지우고 깐다(세션도 지워짐)」 · A-49 확인 칸에 「에뮬레이터면 Google Play 시스템 이미지 + 테스터 목록 Google 계정으로 Play 로그인」. 실기기/에뮬레이터 중 무엇으로 볼지는 정하지 마라(사용자 판단 대기).
4. **R-1** :245 · §14 의 Play 앱 서명 기본 등록 표현을 문서 현행 이름(「Google 생성 키로 자동 등록」)에 맞춤 — 뜻은 그대로.
5. lint `--strict` products/day ERROR 0.

리포트 `spec-4-report.md`(같은 폴더 · 짧게 — 변경 파일:줄 · lint). 완료 보고는 1회차 브리프 §9 두 명령(새 preamble 의 taskId · dispatchId).
