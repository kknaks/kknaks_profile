# day-mobile-v2 Delivery #262 · #263 v2 재결속 — 결과 보고 (머지된 스펙 기준)

## 상태: done — 두 Issue 를 v2 로 재결속했다 · plan 승인 대기(receipt 는 적용하지 않음)

문서 수정 · 커밋은 없다. 워크트리는 `kknaksss/day-mobile-v2-spec`(`246ccaf0`)로 되돌렸다.

## baseline 확인

| 항목 | 값 |
|---|---|
| origin/main | `3ae2317ed00f737944e4ae77657b054daf9e7970`(#955 스쿼시 머지) |
| 브랜치 HEAD 와 트리 비교 | `git diff 246ccaf0 origin/main` = **차이 없음**(트리 같음) |
| 결속에 쓴 곳 | `git checkout --detach origin/main` 위에서 `uv run mediness start-delivery … --plan` → `--apply`(`tools/harness`) |

## 결과

| | #262 (main · `day/day-mobile-v2-0.2.0-2026-11-20`) | #263 (FCM · `day/day-mobile-v2-fcm-2026-11-20`) |
|---|---|---|
| contract_version | 2 | 2 |
| spec_baseline_revision | `3ae2317e…` · state `ready` | `3ae2317e…` · state `ready` |
| contract digest | `sha256:48b52015c199094ceff0a78fcb542ed00cdd8709a79d41643d970941b5298abd` | `sha256:d87c889b482158995aea996502df5a4aa0dc5d1471c5bacd38cc4b06fc01d2d4` |
| **plan digest** | **`sha256:ad01aa59e0ec47b2f4e8b6bed9612a9eb01bb4d5dcdcfa6e003e8b1da341105b`** | **`sha256:e5e252ae480085c9c5232ad3674cd7257e03aeb1a2e7e572e9ac29c22c85cb2a`** |
| apply status | `scope-delta-recorded` · plan_review `review-required` · next = `review-delivery-plan`(human gate) | 같음 |
| task_projection | `blocked`(승인 전 — 정상) | 같음 |

`--plan` · `--apply` 는 둘 다 rc=0 이었다. 옛 v1 plan digest(#262 `2f5930b3…` · #263 `85b22374…`)는 이제 무효이니 승인에 쓰지 마라.

요청 · 출력 파일은 `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-day-mobile-v2-spec/55c97167-02b2-4ce4-8179-785d92dc4074/scratchpad/delivery/` 에 있다.
- 요청: `main.v2m.request.json` · `fcm.v2m.request.json`
- 출력: `{main,fcm}.v2m.{plan,apply}.json`

## 반영 항목 체크

| 항목 | #262 | #263 |
|---|---|---|
| baseline = `3ae2317e` · review_surface 첫 줄 = 머지된 스펙(개정 ⑲ ⑳ · ⑩ ⑪ · ㉕ ㉖) | ✓ | ✓ |
| spec-5 목록: `can*` = 서비스 거절 규칙 정본 · 호출 취소 확인 창 없음 · 「{방} · 호출 취소」 · 완전히 닫힐 때만 · 원래 알림 닫기 · 웹 = OS 알림만 · TokenGate · 빈 final · `audio_stop` / `playback_stopped` · prod 서버 먼저 · 되돌리기 통역 되울림 | ✓ Target Delta · A2 ~ A5 · rollback | ✓ prod 먼저 |
| Firebase 준비됨 · 한 벌 · 채널 「원장 호출」 · 「채팅」 | — | ✓ |
| 바로 시작 = [의사 호출] 옆 → 의사 호출 드로어 · 원장 고르기 없음 · `canQuickStart` · 토스트 한 장씩 | ✓ M-4/5 · A3 · P6 | — |
| 시안 없음(P4 = 하지 않음 · OQ-A52 · A54 닫음) · 「복귀하기」 · 「원장 변경」 · 시술 칸 없음 · `canChangeDoctor` = `doctor_change_block` | ✓ | — |
| 통역 동시 상한 설정 3 · I-1 닫음 · 재생 중 안내 줄 없음 | ✓ M-8 · A5 · P1 · P5 | — |
| 푸시 묶음 iOS `apns-collapse-id` = callId / Android tag `call:{callId}` | ✓ M-6 · P3 | ✓ M-7 · F2 |
| `/api/auth/device` client=web = 400 | ✓ M-3 · P2 | — |
| migration `0013_doctor_call_cancel_kind` · `0014_device_platform_android`(dev `0012_kos_keys` 다음) · prod = `5ece25ea` 로 셋 함께 | ✓ M-6 · predeploy · review_surface | ✓ M-7 · predeploy |
| release Android 빌드는 Firebase 없으면 멈춤(`-PDAY_ALLOW_NO_PUSH=true`) · OQ-A50 · A51 · A60 닫음 | — | ✓ M-7 · A4 · review_surface |
| 롤백: 0013 앞 이미지로 되돌리면 알림 목록 500 → migration 판단을 같이 | ✓ rollback | — |
| 닫힌 OQ 정리(K18 · 77 · 78 · A50 ~ A54 · A58 · A60 · N20 · I-1) · 열린 것 K19 · K20 · N18 · A56 · A57 · A62 · I-6 | ✓ open_questions · review_surface | ✓ open_questions = 없음 |
| **상태 기록**: 구현 = CENTURION_DAY#266 → dev `5ece25ea` · dev 배포 성공(alembic 0014 head) · DAY Dev 0.2.0 TestFlight (4) · Play internal vc4 | ✓ Target Delta 끝 줄 · review_surface · P1 ~ P3 · P5 · P6 「구현됨」 | ✓ Target Delta 끝 줄 · F1 · F2 「구현됨」 · dev FCM 키 실림 |
| **남은 것 = 완료로 쓰지 않음**: 실기기 확인(A-50 · I-6 / F3) · prod 서버 배포 · 정식 0.2.0 앱 | ✓ P7 「남음」 · A6 「남음」 · verification 「남음」 | ✓ F3 「남음」 · A4 「남음」 · verification 「남음」 |

비밀값 grep(키 · 이메일 · IP · Firebase 값 · Key Vault 이름)은 요청 두 파일 모두 0건이다.

## 승인 명령 (적용하지 않음 — 코디가 검수 뒤)

1. receipt 파일 두 개를 만든다(스키마 `tools/harness/src/mediness_harness/schemas/delivery-plan-approval-receipt.schema.json`).

   `main.approval.json`:
   ```json
   {"decision": "approved", "reviewer_type": "human", "reviewer": "<승인자 handle>", "plan_digest": "sha256:ad01aa59e0ec47b2f4e8b6bed9612a9eb01bb4d5dcdcfa6e003e8b1da341105b"}
   ```

   `fcm.approval.json`:
   ```json
   {"decision": "approved", "reviewer_type": "human", "reviewer": "<승인자 handle>", "plan_digest": "sha256:e5e252ae480085c9c5232ad3674cd7257e03aeb1a2e7e572e9ac29c22c85cb2a"}
   ```

2. **origin/main 이 아직 `3ae2317e` 일 때** 같은 요청으로 apply 한다. main 이 움직였으면 baseline 검사에서 다시 막힐 수 있다.
   ```sh
   cd <mediness 워크트리>/tools/harness
   uv run mediness start-delivery --request <D>/main.v2m.request.json --mediness-repo <워크트리> \
     --code-repo /Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2 --github-repo MediSolveAIDev/CENTURION_DAY \
     --apply --plan-approval-receipt main.approval.json --json
   # #263 도 같은 꼴: --request <D>/fcm.v2m.request.json --plan-approval-receipt fcm.approval.json
   ```
   `<D>` = `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-day-mobile-v2-spec/55c97167-02b2-4ce4-8179-785d92dc4074/scratchpad/delivery`. 워크트리는 `origin/main` 에 detach 하고 실행한다(이번과 같은 방법).
