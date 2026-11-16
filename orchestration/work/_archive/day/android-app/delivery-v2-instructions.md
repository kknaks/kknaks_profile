# [planner] Delivery #251 v2 재결속 + 승인 receipt 적용

같은 역할. 맥락이 없으면 이 폴더(`/Users/kknaks/orca/workspaces/kknaks_profile/안드로이드-배포/orchestration/work/android-app/`)의 `spec-report.md`(v1) · `spec-2-report.md` §4 · `spec-3-report.md` §6(v2 목록 정본) · `review-doc-2-report.md` R-1~R-4 · `review-doc-3-report.md` R-3 · R-4 · W-3 · `_RESUME.md` §2 결정 표를 읽어라.

## 상태

- 스펙 PR mediness#940 **머지됨** — squash `855bab4f861ef97257621b45b296061c511e1223`(origin/main).
- 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/android-app-spec` 의 브랜치는 머지됐다. `git fetch origin && git checkout --detach origin/main` 으로 맞춘 뒤 진행(스펙 파일 수정 없음 · 커밋 · push 금지).
- 코드 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/android-app` (base dev `0106654e` · 읽기만).

## 할 것

1. **v2 재결속** — 같은 key `day/android-dev-app-local-run` · baseline = `855bab4f`. `mediness start-delivery --mediness-repo <스펙 워크트리> --code-repo /Users/kknaks/orca/workspaces/CENTURION_DAY/android-app --github-repo MediSolveAIDev/CENTURION_DAY` `--plan` → `--apply`. Issue #251 을 갱신한다.
   - 내용 = spec-3-report §6 그대로 + 아래 반영:
   - **risk L3**(외부 쓰기 = Play 업로드).
   - **phase 순서**(리뷰 3 R-3): AND-1 스캐폴드 · id · 이름 → AND-2 session 구현 · push/video 스텁 → AND-3 통역 Android → AND-4 로컬 에뮬레이터 A1~A5 → **코드 PR 먼저 머지 가능 지점**(사용자 11-13: Play 단계가 막혀도 로컬 끝나면 먼저 머지 — R-4) → AND-5 업로드 키 생성(**코드 워커가 keytool 로 `~/.config/day/android/` 600 에 · 값 출력 금지 · 백업은 사용자** — 사용자 11-13) · release AAB 서명 · targetSdk 36 → AND-6 사용자 손 단계(앱 만들기 · 첫 AAB 손 업로드 · 콘텐츠 선언 · 테스터 · 서비스 계정) → AND-7 API 업로드 스크립트 · 둘째 빌드(versionCode 증가) · A6.
   - **A6 확인 기기 = 실제 Android 폰**(사용자 11-13) · 같은 기기의 로컬 빌드는 먼저 지움(W-3). 참여 링크는 게시 뒤 몇 시간 걸릴 수 있음.
   - A5 TTS = 칩 언어(`en` · `ja` · `zh` · `zh-Hant` · `th`) 중 하나 이상 소리 · 음성 없는 언어는 U-15 토스트(정상) · 에뮬레이터 호스트 마이크 켜기(R-1 · R-2).
   - dependencies 에 dev 서버 통역(D-3)(R-4) · 사용자 손 단계 · 서비스 계정 키.
   - Review Surface[4] 「통역 범위 밖」 삭제 · 「Dart 변경 0」은 Non-Goal 이 아니라 「기본 · 바꾸면 코디 확인」(R-3).
2. **승인 receipt 적용** — 사용자가 2026-11-13 이 세션에서 「그냥 승인하고 해」라고 v2 승인을 미리 위임했다(코디 기록 `_RESUME.md` §2). 직전 관례대로 receipt `{"decision":"approved","reviewer_type":"human","reviewer":"kknaksss","plan_digest":"<v2 plan_digest>"}` 를 만들어 `--plan`(receipt 포함 · digest 같음 확인) → `--apply` 로 `plan-approved` 까지. **digest 가 달라지면 멈추고 보고**한다.

## 하지 말 것

- 스펙 파일 수정 · 커밋 · push · PR · 코드 워크트리 수정.
- 키 · 계정 · 서비스 계정 · 개발자 id 값.

## 산출물

- 리포트 `delivery-v2-report.md`(같은 폴더) — Issue · 라벨 · risk · contract/plan digest · baseline · receipt 경로 · status(`plan-approved`) · Target Delta · A · phases 요약 · request/plan/apply JSON 을 `delivery/` 폴더로 복사.
- 완료 보고는 1회차 브리프 §9 두 명령(새 preamble 의 taskId · dispatchId).
