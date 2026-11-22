# [mobile] M2 — 기기 선택(U-17) · 바로 시작(U-18) · 호출 취소(U-19) · 원장 바꾸기(U-22) + M1 정리

같은 워크트리 · 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/day-mobile-v2-app-brief.md` 의 역할 · 규칙 · 검증 · 금지 그대로. M1 `e7853088` · P5 `bb8412de` · 서버 P2 `e96b0718` 커밋됨. ⚠ backend 가 같은 워크트리 `backend/` 에서 P3 작업 중 — `backend/` 읽기만 · git 읽기만(커밋은 코디). 시안 없음(사용자) — 기존 앱 컴포넌트 + DAY 웹 배치 · 글자. 글자 짓기 금지(없으면 비우고 리포트).

## 정본
- 스펙 `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-003-mobile-app.md` U-17 · U-18 · U-19 · U-20(누름) · U-22 · §5 OQ
- 서버 계약 = 커밋 `e96b0718`(`backend/day/routers/api/auth.py` · `routers/api/board.py` · `schemas/`) · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/be-p2-report.md`(요청/응답 예시 · 오류 코드 표)
- 웹 원천: 기기 선택 `backend/day/templates/` 의 기기 선택 조각 · 바로 시작 액션바 `partials/board_parts.html:188-196` · 호출 취소 ⋮ `:117-126` · 원장 바꾸기

## 사용자 결정 (2026-11-20)
- **바로 시작 = 룸 상세 [의사 호출] 옆에 [바로 시작]** · 누르면 의사 호출처럼 드로어(`app/lib/ui/doctor_picker.dart` 시트 — 시술 체크 · [전체 선택] 그대로 · 원장 고르기 단계 없음) → [바로 시작 · N건](웹 글자) · 체크 가능 줄 = 서버 `canQuickStart`
- 호출 취소 = 호출 줄 ⋮ → 「호출 취소」 · **확인 창 없음**(웹과 같음) · `canCancelCall`
- 원장 바꾸기 = 진행중 줄 담당의 자리(이름 · 「간호관리」 · 「담당의 미정」) 누름 → 원장 고르기 드로어(U-6 대리 수락과 같은 배치) · `canChangeDoctor`
- 기기 선택 = 로그인 중간 단계(병원 고르기와 같은 틀) · 글자 = 웹(KOS 글자)

## M1 정리(같이)
- 검수 W-2: `unsetActionCodes` 웹 표 손 복제 → 출처 주석 · 가능하면 한 곳으로 · W-3: 거절 토스트 테스트 단언(:190 · :250) 강화

## 할 것 · 검증
- 테스트 · `flutter analyze` · `flutter test` · `flutter build ios --no-codesign` 각 1회
- 캡처 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/shots/m2-*.png`(폰 · 아이패드: 기기 선택 · 바로 시작 드로어 · 호출 취소 메뉴 · 원장 바꾸기)
- 알림 · 푸시(새 kind) · 통역 드로어 안내 문구는 이번 아님.
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/mobile-m2-report.md` — 글자 출처 · 비운 글자 · 판단한 배치

완료 보고는 dispatch preamble 의 worker_done 그대로. 커밋 · push · PR 금지.
