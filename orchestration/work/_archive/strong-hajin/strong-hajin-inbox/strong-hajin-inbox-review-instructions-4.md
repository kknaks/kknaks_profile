# [reviewer] 코드 검수 — WORK-011 BE-1 (커밋 78f014f)

이 워크트리(`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-inbox`)의 커밋 **78f014f** 를 SPEC-008 v0.5.1 · WORK-011 「Phase BE-1」 · 4차 검수 BE-1 항목 기준으로 검수한다. **지금 같은 워크트리에서 BE-2·BE-3 워커가 작업 중이다 — 작업 트리가 아니라 `git show 78f014f` / `git diff 78f014f~1 78f014f` 로 본다.** 아무것도 고치지 마라.
볼 것: 스키마(소프트 딜리트 · 사람마다 복제 · 카톡 중복 키 연동 범위) · 소유 검사(남의 연동·방·메시지 404) · 토큰 암호화(Fernet · 키 없으면?) · OAuth state(일회용·만료·회원 묶기·CSRF) · 기기 토큰(Bearer 전용 · 해시만 · 범위 = 카톡 수집 라우트만 · 웹 라우트 거절 · 철회) · 비밀값이 로그·repr·시험에 새지 않나 · NOTIFY 계약 · 모듈 분할이 BE-2∥BE-3 을 가능하게 하나 · manual SQL 과 schema_sync 일치 · 시험이 계약을 실제로 덮나
결과 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/review-be1.md`(항목·판정·근거 파일:줄·고칠 것 + 총평 PASS/WARN/FAIL). 끝나면 §9.
