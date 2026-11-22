# [backend] F1 — Android 푸시 FCM 서버 + P2 검수 남은 것

같은 워크트리 · 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/day-mobile-v2-be-brief.md` 의 역할 · 규칙 · 검증 · 금지 그대로(allowed_paths 만 아래로). 커밋됨: P1 a7868dc6 · P2 e96b0718 · P3 9162ee18. ⚠ mobile 이 `app/` 작업 중 · reviewer 가 P3 를 읽는 중 — `app/` 금지 · git 읽기만(커밋은 코디). Delivery = CENTURION_DAY#263.

## A. FCM (F1)
정본(PR 브랜치 스펙):
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-003-mobile-app.md` §3 「Android 푸시 — FCM」(:694 근처 표 전부) · OQ-A50(env 이름 기본값 `DAY_FCM_SERVICE_ACCOUNT` 비밀 · `DAY_FCM_ALLOWED_APP_IDS`) · OQ-A51(`android` 은 `push_env` 안 보냄 · 토큰 = 빈 문자열 아님 · 4096자 이하) · OQ-A59(data 메시지 · 채널 「원장 호출」 · 「채팅」 · 호출 취소 = 원장 호출 채널)
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-000-data-model.md` device `platform` `android` migration · `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/40-architecture/mobile-deployment.md` §8-1
- 발송 범위 = 원장 호출 · 호출 취소 · 채팅 (iOS 와 같은 갈래) · 키 없음 = `skipped_no_key` · 죽은 토큰 = `token_removed` · 5xx/429/네트워크 1회 재시도(APNs 규칙과 같게)
- 코드: `backend/day/adapters/apns.py`(꼴 참고) · `services/notifications.py` · `services/notification_cancel.py` · `services/devices.py`(:113 잠금 키 `push_env.value` — android null 주의) · `schemas/devices.py` · `tasks/notifications.py` · 채팅 푸시 경로
- 키: 로컬 실물 1회만 `~/.config/day/android/fcm-service-account.dev.json` 을 env 로 읽어 FCM HTTP v1 에 **validate_only** 로 1회(실제 기기 토큰 없음 — 가짜 토큰이면 오류 갈래 확인으로 충분). 키 내용 · 토큰 출력 · 파일 복사 금지. Key Vault 는 코디가 넣는다 — 손대지 마라.

## B. P2 검수 남은 것(`/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-code-p2-report.md`)
- 앱 API 만료 · 로그 · 503 시험 · `canCancelCall` 수락된 호출 시험 추가
- `/api/auth/device` 의 `client=web` 허용 비대칭 — 스펙(SPEC-001 ⑩)대로 고치거나, 스펙이 말이 없으면 멈추고 질문

## allowed_paths
- A: `backend/day/adapters/`(새 `fcm.py`) · `services/notifications.py` · `services/notification_cancel.py` · `services/devices.py` · `services/` 채팅 푸시 부분 · `schemas/devices.py` · `enums/` · `models/` 필요 칸 · `tasks/notifications.py` · `common/config.py`(env 2개) · `backend/migrations/versions/`(새 파일 1 · 0013) · `deploy/config/dev.env` · `prod.env`(비밀 아닌 `DAY_FCM_ALLOWED_APP_IDS` 만 — 앱 id `day.medisolveai.dev` · `day.medisolveai`) · `pyproject.toml` · `uv.lock`(google-auth 등 필요 시만) · 관련 테스트
- B: `backend/day/routers/api/auth.py` · `services/auth.py` · 관련 테스트
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/be-f1-report.md`

## 검증
관련 테스트 + migration up/down · ruff 1회씩 · FCM validate_only 실물 1회. 리포트에 A · B 따로 · Key Vault 에 넣을 비밀 env 이름 목록(값 없이).

완료 보고는 dispatch preamble 의 worker_done 그대로. 커밋 · push · PR 금지.
