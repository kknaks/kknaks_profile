# day-mobile-v2-spec 결과 보고 — 직원 앱 0.2.0 SPEC 개정 · WP 나누기 · Delivery 발행

## 상태: done (plan 승인 대기 — 승인 receipt 는 적용 안 함 · 사용자 몫)

| 항목 | 메인 0.2.0 | FCM |
|---|---|---|
| Delivery Issue | **CENTURION_DAY#262** https://github.com/MediSolveAIDev/CENTURION_DAY/issues/262 | **CENTURION_DAY#263** https://github.com/MediSolveAIDev/CENTURION_DAY/issues/263 |
| 라벨 | `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:ready` | 같음 |
| risk | L2(새 엔드포인트 · enum migration · 통역 프로토콜 변경 · 기존 결정 뒤집음) | L2(새 외부 발송 경로 · migration) |
| contract_digest | `sha256:e945e77fb1da263073fc2973d48b7d717b5c2b20c8b82f7b6f2c0b251f4cb24e` | `sha256:2277944658b58faecedb7f7a8b0b4cc2cddfd5bbff84f9360957e01aa4370153` |
| plan_digest (승인 대상) | `sha256:2f5930b335824c705552be7ab5ce23e936612792e8153ffb3f86603483c0066a` | `sha256:85b2237483ef9c34ba573af99c27369f8c9aab8c8d1b0cd8fa0f4c7750acb4e7` |
| baseline | mediness `origin/main` `ccede2866d006607509c5e34bdad33079fa9dffd`(옛 계약). **이번 개정은 워크트리에만 있음(미커밋)**. Review Surface[0]: 스펙 PR 머지 → 같은 key 로 contract_version 2 재결속 → 그 뒤 사용자 plan 승인 권장(v1 digest 는 승인하지 않는 쪽 권장) | 같음 |
| next_action | `review-delivery-plan` · human_gate true | 같음 |
| idempotency_key | `day/day-mobile-v2-0.2.0-2026-11-20` | `day/day-mobile-v2-fcm-2026-11-20` |
| request / plan / apply | `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-day-mobile-v2-spec/55c97167-02b2-4ce4-8179-785d92dc4074/scratchpad/delivery/main.v1.{request,plan,apply}.json` | 같은 폴더 `fcm.v1.*.json` |

FCM 을 따로 뗀 이유: 사용자 Firebase 준비에 걸려 있고, 「1 Delivery = 1 Code PR」이라 준비가 늦어도 메인 PR 을 막지 않게 했다.

## 수행 내용 — 변경 파일 (워크트리 `day-mobile-v2-spec` · 미커밋 · `products/day/` 만)

| 파일 | 무엇 |
|---|---|
| `20-spec/spec-003-mobile-app.md` | 개정 ⑲(:76) · 범위 「넣음」 0.2.0 줄 · 「뺌」 표(:108-125 근처 · 귀가 대기 취소 :123) · U-1 기기 제한 줄 · U-7 · U-14 · U-15 반이중 · **U-17 ~ U-22**(:471-516) · API 표(:589) · 「Android 푸시 — FCM」(:694) · 「통역 — 0.2.0」(:809) · 케이스 매트릭스 0.2.0 10줄 · A-50(:1038) · §5 「0.2.0 — 정할 것」(:1152) |
| `20-spec/spec-001-login-session.md` | 개정 ⑩(:48) · U-4 웹 · 앱 · API 표 `/api/auth/device`(:267) · 응답 모양 `choose_device` JSON · 앱 환경 연결 규칙 9 · K-3 규칙 1 · 3 · 7 · 비밀번호 예외 · Validation · 케이스 매트릭스 · 규칙 15 · OQ-K14 닫음 · K17 다시 닫음 · 새 OQ-K18 ~ K20(:626) |
| `20-spec/spec-002-procedure-board.md` | 개정 ㉕(:43) · API 표(호출 취소 `/api` 있음 · 바로 시작 `/api` 새로) · 바로 시작 JSON(:599) · 스냅샷 `canCancelCall` · `canQuickStart` · `canChangeDoctor`(:672) · OQ-77 · 78(:1166) |
| `20-spec/spec-005-notifications.md` | 2026-11-20 개정(:36) · 범위 표 · 「알림 행 만들기 — 호출 취소」(:265) · 발송 표 FCM 줄(:292) · OQ-N14 닫음 · 새 OQ-N15 ~ N20(:453) |
| `20-spec/spec-000-data-model.md` | 2026-11-20 개정(:37) · `notification.kind` · `push_log.kind` 에 `doctor_call_cancel` · `device.platform` 에 `android` · `push_env` · `push_token` · device 규칙 두 줄 |
| `40-architecture/mobile-deployment.md` | ⑤(:26) · §8-1 FCM 확정 · 칸 이름 · 위치(:290) · §10 0.2.0(:352) · M-9 닫음 · M-10 · M-13 |
| `20-spec.md` | 범위 문장(로그인 · 앱 · 알림) · 범위 밖 줄 · 최종 수정 |
| `log.md` | 2026-11-20 spec-change, arch-change 행 |

`version` 은 `0.0.1` 그대로다(규칙: 문서를 고쳤다고 올리지 않음). 앱 버전 0.2.0 은 제품 앱 빌드 번호라 SPEC `version` 과 다른 축이다.

## 결정 표 반영 위치

| # | 반영 |
|---|---|
| M-1 출시 | SPEC-003 개정 ⑲ ① · mobile-deployment ⑤ ① ~ ③ · §10 「[확정] 0.2.0」 · Delivery #262 P7 |
| M-2 호환 | SPEC-003 개정 ⑲ ②(「앱 코드 무수정」 문장들은 기록이 됨) · SPEC-001 개정 ⑩ ③(OQ-K14 닫음 — 가르기 없음) · SPEC-002 개정 ㉕ ④ · SPEC-005 개정 ②(배지 어긋남 고려 안 함) · 통역 0.2.0 머리 · 케이스 매트릭스 「깔린 0.1.0 이 choose_device」 줄 |
| M-3 기기 제한 | SPEC-001 개정 ⑩ 전부 · SPEC-003 U-17(웹 KOS 글자 그대로) · 로그아웃 KOS 해제 안 함 = SPEC-001 규칙 15 · U-17 마지막 줄 |
| M-4 시술 현황 | SPEC-003 U-18 ~ U-22 · 「뺌」 표(귀가 대기 취소 · 정렬 탭 · 순서 변경) · SPEC-002 개정 ㉕ ⑤ |
| M-5 API | SPEC-002 개정 ㉕ ① ~ ③(quick-start JSON · 기존 `/api` 3개 확인 · `can*` 3칸 · 방 옮기기는 기존 카드 칸으로 충분) · SPEC-003 API 표 |
| M-6 호출 취소 알림 | SPEC-005 「알림 행 만들기 — 호출 취소」 · SPEC-000 enum migration · SPEC-003 U-14 보강 |
| M-7 FCM | SPEC-003 「Android 푸시 — FCM」 · SPEC-005 FCM 줄 · SPEC-000 `platform android` · mobile-deployment §8-1(칸 이름 · 위치만 · 값 없음) · Delivery #263 |
| M-8 통역 | SPEC-003 「통역 — 0.2.0」(표마다 통키 DEC 번호 D-43 · 45 · 48 · 49 · 54 · 56 · 58 · 63 ~ 71) · U-15 반이중 걷음 · 기록(D-42) 없음 |
| M-9 글자 | U-17 = 웹 KOS 글자 · U-19 · U-20 · U-22 = 웹 글자 · 성공 토스트 · 글자 없는 오류 = 「미정」(OQ-A56 · A57) · FCM 채널 이름 미정(A59) |

## 착수를 막는 OQ (기본값 후보 — 결정 아님)

| OQ | 무엇 | 기본값 후보 | 막는 워커 |
|---|---|---|---|
| SPEC-001 OQ-K18 | 앱 기기 선택 경로 · JSON 칸 | `POST /api/auth/device {pending_token, device_id, client}` · 응답 = service 칸 + `environment` · `api_base_url` | backend · mobile |
| SPEC-002 OQ-77 | 바로 시작 전부 거절 응답 | 지금 service 그대로 409 + 첫 거절 코드 | backend · mobile |
| SPEC-002 OQ-78 | 새 `can*` 이름 · 판정 | `canCancelCall` · `canQuickStart` · `canChangeDoctor` = 서비스 거절 규칙 결과 | backend · mobile |
| SPEC-005 OQ-N15 | 새 알림 종류 이름(migration — 못 뺌) | `doctor_call_cancel` | backend |
| SPEC-005 OQ-N16 | 본문 {N} | 이번 취소로 빠진 시술 수 | backend |
| SPEC-005 OQ-N17 | 원래 원장 호출 알림 「닫기」 방법 · 때 | 서버 `read_at` 채움 + 앱이 OS 알림 센터의 원래 푸시 지움 · 그 호출이 닫힐 때만 | backend · mobile |
| SPEC-003 OQ-A50 | FCM env 이름 | `DAY_FCM_SERVICE_ACCOUNT` · `DAY_FCM_ALLOWED_APP_IDS` | backend(FCM) |
| SPEC-003 OQ-A51 | `android` 의 `push_env` · 토큰 검사 | `push_env` 안 보냄 · 토큰 = 비어 있지 않음 · 4096자 이하 | backend · mobile(FCM) |
| SPEC-003 OQ-A52 · A54 | 앱 화면 자리(기기 선택 · 바로 시작 다중 선택 · 방 옮기기 · 원장 바꾸기 · 간호관리) | designer 시안 · 새 글자 없음 | mobile |
| SPEC-003 OQ-A55 | **방 복귀를 앱에 넣나** — M-4 목록에 없지만 점유 이동만 넣으면 앱에서 돌아올 길이 없다 | 넣음(기존 API) — **사용자 확인 필요** | mobile · designer |
| SPEC-003 OQ-A59 | FCM 메시지 모양 · Android 알림 채널 | data 메시지 · 앱 로컬 알림 · 채널 2개(이름 글자 미정) | backend · mobile(FCM) |
| SPEC-003 OQ-A61 | `playback_stopped` 를 보내는 앱 조작 | 재생 중 [멈춤] · 드로어 닫기 · 언어 바꿈 · 다시 연결 | mobile |

막지 않는 것: OQ-K19 · K20 · N18 ~ N20(N19 = M-6 「웹 알림 목록 · 종 배지」 해석 — 웹에는 원장 호출 목록 · 종 화면도 없어 웹 OS 알림으로 읽음 · 다르면 사용자 확인) · A53 · A56 · A57 · A58 · A60 · A62 · I-6.

조사 §F 18개 중 결정 표로 안 닫힌 것: F-5(`(dev)` 표시 — 웹과 같음으로 흡수) · F-10(토스트 글자 → A56 · A57) · F-15(바로잡기 = 함수만 · M-8 로 닫힘) · F-17(Soniox 한도 → 기존 I-1 그대로) · F-18(옛 앱 + 새 통역 → M-2 로 고려 안 함). 확인 안 된 사실(KOS 해제 즉시성 OQ-K11 · Soniox 한도 · D-68 뒤 TTS 연결 수명)은 열린 채 뒀다.

## WP 나누기 (Delivery 실행 phase · 30-work.md 에는 새 WP 행을 넣지 않음 — 규칙상 신규 WP 금지 · 대시보드는 spec-sync 가 #262 · #263 을 넣음)

| 순 | 워커 | 일 | 의존 | Delivery |
|---|---|---|---|---|
| P1 | backend | 통역: STT v6 · D-67 · 시드 `.11` 로더 · context D-71 · 바로잡기(records 함수만) · turn D-68 ~ 70 · `audio_stop` / `playback_stopped` | 스펙 머지 · **마감 2026-12-15(v5 종료)** — 제일 먼저 | #262 |
| P2 | backend | 앱 `choose_device` · `/api/auth/device` · relay `read_success` · quick-start JSON · `can*` 3칸 | OQ-K18 · 77 · 78 | #262 |
| P3 | backend | `doctor_call_cancel` migration · 알림 행 · 원래 알림 닫기 · APNs · 웹 OS 알림 kind | OQ-N15 ~ N17 | #262 |
| P4 | designer | 앱 시안 5자리(아래 표) | 스펙 머지 · A55 답 | #262 |
| P5 | mobile | 통역 클라이언트(반이중 걷음 · `audio_stop` · `playback_stopped`) | P1 · A61 | #262 |
| P6 | mobile | 기기 선택 · 시술 현황 5동작 · 새 알림 kind · 푸시 탭 · 원래 푸시 지우기 | P2 · P3 · P4 | #262 |
| P7 | mobile(빌드) | DAY Dev 0.2.0(iOS 4 · Android 4) → 사용자 실기기 → 정식(iOS 3 · Android 4) | P5 · P6 (+ F2 가 늦으면 FCM 없이 먼저 낼지 사용자 판단) | #262 |
| F1 | backend | `platform android` migration · 등록 검사 · FCM 어댑터 · 발송 갈래(원장 호출 · 호출 취소 · 채팅) | 사용자 Firebase 키 · P3 의 kind · OQ-A50 · A51 · A59 | #263 |
| F2 | mobile | Android `day/push` 구현 · 알림 채널 · [수락] · google-services | F1 · `google-services.json` 두 벌 | #263 |
| F3 | 사용자 | Android 실기기 푸시(개발 → 정식) | F2 | #263 |

### 앱 화면 시안이 필요한 곳

| 자리 | SPEC | 시안이 정할 것 | 글자 원천 |
|---|---|---|---|
| 기기 선택 | SPEC-003 U-17 · OQ-A52 · A53 | 로그인 카드 자리 · 라디오 목록 · 폰 · 아이패드 · 뒤로 | 웹 U-4 KOS 글자 |
| 바로 시작 다중 선택 | U-18 · OQ-A54 | 룸 상세에서 준비중 줄 고르기(시트 / 줄 체크) · 「바로 시작 · N건」 버튼 자리 | 웹 액션바 글자 |
| 방 옮기기 | U-21 · OQ-A54 · A55 | 룸 상세 머리 메뉴 · 방 목록(비어 있음 / 배정됨) · 「이동」 / 「점유 이동」 · (복귀) | 웹 방 옮기기 글자 |
| 원장 바꾸기 | U-22 · OQ-A54 | 담당의 이름 누름 → 원장 고르기 드로어(U-6 대리 수락과 같은 배치) | 웹 원장 바꾸기 글자 |
| 간호관리 표시 | U-20 · OQ-A58 | 진행중 · 완료 줄 · 목록 카드 담당의 자리 · 누를 수 있다는 표시 | 웹 「간호관리」 |

## 검증

- `python3 scripts/lint-pipeline.py --strict` → **0 error, 263 warning** · `products/day/` 의 ERROR · WARN **0**. 263 WARN 은 모두 다른 제품(selly 등 `doc_no` 누락 · map frontmatter)이라 이번 작업과 무관하다.
- 근거 없는 정책: 결정 표에 없는 값은 모두 「제안 · 기본값」으로 OQ 에 올렸다(이름 · 응답 모양 · 닫는 방법 · env 이름 · 채널). 화면 · 토스트 글자는 웹 · 결정 표 글자만 썼고, 없는 곳은 「미정」으로 뒀다.
- 비밀값 · 이메일 · IP · Azure 이름 · Firebase 값: 문서에 넣지 않았다(env 이름 제안만).

## 미결 · 주의점

- **스펙이 미커밋이라 #262 · #263 v1 의 baseline(`ccede286`)은 옛 계약이다.** 스펙 PR 머지 뒤 같은 key 로 contract_version 2 재결속하고, 그 뒤 plan 승인을 권장한다.
- **OQ-A55(방 복귀)는 사용자에게 물어야 한다.** M-4 넣음 목록에 복귀가 없지만, 점유 이동만 넣으면 앱에서 원래 방으로 돌아올 길이 없다.
- **OQ-N15 의 kind 이름은 migration 이라 되돌리기 어렵다.** 착수 전에 확정이 필요하다.
- **M-6 「웹 알림 목록 · 종 배지」는 OQ-N19 로 해석했다.** 웹에는 원장 호출 목록 · 종 화면이 없어(`static/day.js:1826-1834` 은 OS 알림만) 웹 OS 알림으로 읽었다. 웹 목록 · 종 화면을 새로 만드는 뜻이면 범위 · 시안이 커진다.
- 통역 P1 은 STT v5 종료(2026-12-15)가 마감이라 맨 앞에 뒀다. Soniox TTS 한도(3)와 상한 6 의 관계, D-68 뒤 TTS 연결 수명은 확인되지 않았다(I-1).
- 데모 계정의 앱 기기 선택 제출은 최장 약 60초라 넘김 60초와 겹친다(OQ-K19 · 기본 = 그대로).
- `tools/harness/.venv` 가 CLI 실행 때 생겼다. gitignore 대상이라 `git status` 에는 안 나온다.
