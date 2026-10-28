# 앱 실기기 E2E batch 1 수정 (코디 · 2026-10-28)

원천: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/app-e2e-feedback-batch1.md`(6건 · 사용자 「응 수정하자」). 코드 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` — **새 브랜치 `kknaksss/overall-board-3`**(origin/main `f8a3751` · 운영 배포본). 커밋 · push 금지 · 사용자 포트 금지 · 끝나면 보고서에 「E2E batch 1」 절 + 두 명령(코디 `term_678ac61d-2472-4a9b-ba73-61883337b957`).

## 운영 확인 결과(코디 · #3)
- 운영 DB: 띄우기 요청 #10(scan → **새 기기 행 9**)에는 **푸시가 없다**(앱이 앞이라 SSE 로 보냄 · `reach`) — 그런데 폰엔 안 떴다 → **앱이 SSE `display` 를 받고도 화면을 안 열었거나, 기기 9 의 SSE 가 그 기기 id 로 붙지 않았다**. 요청 #9 · #7 · #8 은 **옛 기기 행 8** 로 가서 푸시 `sent` 기록(옛 토큰)
- 기기 행: 같은 폰이 8 · 9 두 줄(둘 다 이름 「iPhone」)

## backend (`procedure/back/**`)
- **#1**: 기기 등록에 설치 단위 id(`installId` — 앱이 보냄)를 받아 **같은 installId 의 옛 행을 새 토큰으로 바꿔 끼운다**(행 하나 유지) · 없으면 지금처럼. 마이그레이션 · 시험. targets 는 계정 · installId 당 하나
- **#3**: SSE `display` 가 그 기기 스트림으로 실제로 나가는지 시험(기기 id 쿼리로 붙은 스트림) — 문제면 고친다
- **#4(코디 기본값)**: 휴대폰 = **표시할 때만** 국가번호가 82 면 맨 앞 0 을 붙여 `010-xxxx-xxxx` 꼴로(KOS 값 · 보내는 값은 그대로). back 응답에 `phoneDisplay` 를 더하든 front · app 에서 같은 함수로 하든 — 셋이 같은 규칙. 정한 방식을 보고에

## mobile (`procedure/app/**`) — 새 워커
- **#1**: `installId`(`identifierForVendor` · 키체인에 보관) 를 기기 등록에 보냄
- **#2(코디 기본값)**: **첫 로그인 때 「이 기기 이름」 입력 시트**(예: 데스크 태블릿 · 코디 폰) — 설정에서 바꿀 수 있음(있음). entitlement 신청은 하지 않음
- **#3**: SSE `display` 받음 → 화면 열기가 실제로 되는지(앞 · 뒤 · 다른 탭) 고치고 시험
- **#5**: `ccc` URL 스킴 등록(`CFBundleURLTypes`) + 딥링크 `ccc://display?t=…` 열기 → 로그인 돼 있으면 claim · 아니면 로그인 뒤 claim
- **#6**: 여권 스캔을 `AVCaptureSession`(자동 매크로 되는 가상 카메라 — `builtInTripleCamera` / `builtInDualWideCamera` 먼저) **영상 프레임에서 가이드 틀 영역만 Vision 으로 연속 인식** → MRZ 검사 숫자 맞으면 **자동 촬영** · 3번(또는 N초) 실패 → 손 입력 · 사진첩 저장 0 · 법적 검토 주석 유지. 실기기 확인은 코디 · 사용자
- 검증 `flutter analyze` · `flutter test`(fvm `/Users/kknaks/fvm/versions/3.44.8/bin/flutter`)

## frontend (`procedure/front/**`)
- **#4**: 휴대폰 표시 규칙(backend 와 같은 것) · **#1**: 기기 목록이 installId 당 하나로 보이는지 · 「iPhone」 대신 기기 이름
- 검증 `tsc` · `lint`
