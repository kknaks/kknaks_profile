# Delivery #251 v2 재결속 + 승인 receipt 리포트 (2026-11-13)

스펙 워크트리 `android-app-spec` = detached `origin/main` `855bab4f`(스펙 파일 수정 0 · 커밋 · push 0). 코드 워크트리 `CENTURION_DAY/android-app` dev `0106654e` 읽기만.

## 결과

| 항목 | 값 |
|---|---|
| Issue | CENTURION_DAY#251 — https://github.com/MediSolveAIDev/CENTURION_DAY/issues/251 (OPEN) |
| key · version | `day/android-dev-app-local-run` · contract_version **2** |
| 라벨 | `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:ready` |
| risk | **L3**(Play 업로드 = 외부 쓰기 · 패키지명 고정) |
| baseline | `855bab4f861ef97257621b45b296061c511e1223` |
| target_specs | DAY-SPEC-003, DAY-SPEC-004 |
| contract_digest | `sha256:d63d70acc0d6c2dc9b435022d237e2b4ec8558cd56bb2ab08b5f8cd7c561ab3e` |
| plan_digest | `sha256:e9664196d73545012edd23174a9ce4cbc0dc6d546c0dc5f0d53f12e67bba9101` — v2 plan · apply · receipt plan · receipt apply 네 번 모두 같음 |
| receipt | `delivery/android.v2.approval-receipt.json` — `{"decision":"approved","reviewer_type":"human","reviewer":"kknaksss","plan_digest":<위>}` · 근거 = 사용자 2026-11-13 「그냥 승인하고 해」 위임(`_RESUME.md` :42) |
| status | `plan_review.status = approved` · 마지막 apply status = `execution-updated` · next_action = `implement-and-open-code-pr`(human_gate false) |

## 거친 단계

1. v2 request(`delivery/android.v2.request.json`) — v1 을 바탕으로 spec-3-report §6 + 지시서 반영.
2. 첫 `--apply` = `conflict`: 「idempotency key already exists with a different contract; record a Scope Delta」 → request 에 `scope_delta`(v1→v2 바뀐 것 한 문단) 추가. plan_digest 는 변하지 않음(scope_delta 는 digest 밖).
3. `--plan` → `--apply` = `scope-delta-recorded` · Issue #251 갱신 · `delivery-plan:review`.
4. receipt 와 함께 `--plan`(digest 같음 확인 · plan_review approved) → `--apply` = `delivery-plan:approved`.

## 내용 요약

- **Target Delta 10**: app/android 생성(id · 이름) · day/session 구현 · day/push 스텁(설정 탭 알림 안내 그대로) · day/video 스텁 · 통역 Android(마이크 · 4 플러그인) · 그 밖 플러그인 권한 · release AAB · targetSdk 36 · 업로드 키 서명(값 저장소 밖) · 업로드 키 생성(코드 워커 keytool · `~/.config/day/android/` 600 · 값 출력 금지 · 백업은 사용자) · Play API 업로드 스크립트(둘째 빌드부터 · versionCode 인자) · README Android 절.
- **A 조건 7**: A1 로그인 → 시술 현황 · 채팅 목록 / A2 자동 로그인 · 로그아웃 뒤 다시 켜면 로그인 화면 · 푸시 없이 오류 없음 / A3 iOS build · ios 변경 0 · flutter create 산물 따로 적음 / A4 Dart 변경 0 기본 · 바꿨으면 코디 확인 기록 / A5 통역(호스트 마이크 · TTS 칩 언어 en · ja · zh · zh-Hant · th 중 하나 이상 · 음성 없으면 U-15 토스트 정상) / A6 Play 내부 테스트 — **실제 Android 폰** · 같은 기기 로컬 빌드 먼저 지움 · 참여 링크 몇 시간 · 둘째 빌드 API 업로드 → 업데이트 / A7 저장소 · 로그 · PR 비밀 0.
- **phases 7**: AND-1 스캐폴드 · id · 이름 → AND-2 session · 스텁 → AND-3 통역 → AND-4 로컬 A1~A5 · iOS build · README — **여기서 코드 PR 먼저 머지 가능** → AND-5 업로드 키 · release AAB · targetSdk 36 → AND-6 사용자 손 단계 대기 → AND-7 API 스크립트 · 둘째 빌드 · A6.
- **dependencies**: baseline 855bab4f · 로컬 SDK/AVD/fvm · **dev 서버 통역(D-3)** · **사용자 Play Console 손 단계**(§7-3-2) · **서비스 계정 키 JSON 로컬** · 실제 Android 폰.
- **Non-Goals**: iOS · FCM/알림 [수락]/채팅 푸시 Android · day/video 실제 구현 · 정식 앱(M-4 · M-3) · CI(M-12) · 업로드 키 백업 정하기(M-11) · 서버. 「Dart 동작 변경」은 Non-Goal 에서 빼 Review Surface 「기본 규칙 · 바꾸면 코디 · 사용자 확인」으로(R-3 ②). v1 Review Surface[4] 「통역 확인 범위 밖」 삭제(R-3 ①).
- **predeploy · rollback**: Play 업로드 전 패키지 · 트랙 · 서명 · 비밀 0 확인 / PR revert · 내부 테스트 출시 중지 · versionCode · 패키지명은 못 되돌림 · 업로드 키 재설정 요청.

## 주의

- apply 결과 `partial: true` — `task_projection` 이 `pending`(MCP `mediness.task_draft_request` 미호출). 승인 · 라벨과는 별개이고 지시서 범위 밖이라 하지 않았다. Task 카드가 필요하면 코디가 MCP 로 이어서.
- 마지막 status 문자열은 `plan-approved` 가 아니라 `execution-updated` 다(approve apply 의 status 값). 승인 상태는 `plan_review.status = approved` · 라벨 `delivery-plan:approved` 로 확인.
- 값(키 · 계정 · 서비스 계정 · 개발자 id) 0 — request 에 경로만.

## 파일 (`delivery/`)

`android.v2.request.json` · `android.v2.plan.json` · `android.v2.apply.json` · `android.v2.approval-receipt.json` · `android.v2.approve.plan.json` · `android.v2.approve.apply.json`
