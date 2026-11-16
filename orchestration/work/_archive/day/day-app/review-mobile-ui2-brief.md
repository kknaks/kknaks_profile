# UI 1차 리뷰 보완 재검수

대상: /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app app/ 미커밋 UI. 역할 reviewer, 코드·SPEC·서버 수정 금지. 하위 워커/내부 agent 금지. 기존 review-mobile-ui-report.md의 PASS(WARN4) 후속 재검수만 한다.
원천: /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/mobile-ui-fix1-report.md, 기존 review-mobile-ui-report.md, mobile-ui-fix1-brief.md, SPEC worktree cdde456a의 SPEC003. 기존 사용자 13항목 계약과 로컬 API 소비 6항목 유지. user 2차 수정 지시가 들어왔지만 아직 새 항목 미제공이며 여기서는 기존 WARN 해소만 검수한다.

확인할 것:
1. WARN1 calls[] fixture와 cards 정합, 호출 건수 실제 캡처 및 호출 탭.
2. WARN2 폰 호출창 방·고객명, 320 긴 이름의 읽힘.
3. WARN3 320 목록/상세 긴 고객/발음/시술, 599/600 경계 PNG 직접 열람. overflow/겹침/버튼 누락 0.
4. WARN4 canStart=true DAY 버튼, 호출/완료 인박스 폰+iPad PNG 직접 열람.
5. 후속 제품 수정의 범위·보안·13UI/6API 회귀(특히 폰/iPad 구분은 shortestSide600 기준), app/ 밖 변경 0. 필요한 최소 테스트만 실행; 이미 전체184 재실행 근거가 있으면 중복 전체 실행 불필요.
6. iOS 앱 프로세스 public /health/ready GET 결과 로그 검토. 자격증명/로그인/업무쓰기 없음, 제품 probe/demo 경로 없음, ATS 완화 없음, 표준 main 앱 복구 확인. health200을 인증 통합 PASS라 주장하지 않음.

산출물: profile 동일폴더 review-mobile-ui2-report.md. PASS/FAIL/WARN·직접 본 PNG명·수정 범위·실행 검사·통합 미실행 경계. 코드/커밋/push/merge 금지. 보고 뒤 preamble 정확한 ID로 worker_done 1회(outcome/report-path 포함), idle. 원본 브리프 mobile-ui-code-brief.md의 안전 경계 유지. 다른 작업을 시작하지 않는다.
