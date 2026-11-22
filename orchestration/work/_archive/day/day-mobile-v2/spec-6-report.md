# day-mobile-v2-spec 6차 결과 보고 — 새 main 위로 rebase · 구현 사실 동기화 · 남은 문장 3

## 상태: done (커밋함 · push 안 함 — 코디가 force push)

| 항목 | 값 |
|---|---|
| 브랜치 | `kknaksss/day-mobile-v2-spec`(PR mediness#955) |
| 새 base | `origin/main` `07aaa6d2`(#954 KOS 키 테이블 · #957 prod 반영 절차 포함) |
| 커밋 1(rebase 된 옛 커밋) | `5cf09d21` — 직원 앱 0.2.0 스펙(옛 `7d198317`) |
| **새 HEAD** | **`bc3f9669`** — `docs(day): 0.2.0 구현 사실 동기화 — 바로 시작 드로어 · 시안 없음 · 통역 상한 3 · 푸시 묶음 · 복귀하기 · canChangeDoctor` |
| 코드 근거 | CENTURION_DAY dev `5ece25ea`(PR #266 스쿼시). 아래 사실은 모두 이 커밋에서 `git grep` 으로 확인했다 |

## 1. rebase 충돌과 푼 방법

충돌은 두 파일에서만 났다. 나머지 6파일은 저절로 합쳐졌다. `20-spec.md` 와 `40-architecture/` 는 겹치지 않았다.

| 파일 | 충돌 | 푼 방법 |
|---|---|---|
| `products/day/20-spec/spec-000-data-model.md:40-42` | 머리말의 2026-11-20 개정 문단이 양쪽에 하나씩 있었다(main = §4A KOS 키 보충 · 우리 = enum `doctor_call_cancel` · `device.platform android`) | **둘 다 살림**. 우리 문단을 먼저, main 문단을 그 뒤에 두고 `>` 줄로 나눴다 |
| `products/day/log.md:17-20` | 변경 이력 맨 위 2026-11-20 행(main 1행 · 우리 3행) | **둘 다 살림**. 우리 3행 아래에 main 1행을 두었다 |

migration 번호는 우리 스펙 문장에 아예 없었다. 그래서 동기화 커밋에서 실제 이름을 넣었다(아래 2).

**참고(고치지 않음)**: `40-architecture/deployment.md:240`(#957 · 다른 세션 문서)에는 「#266 의 2026-11-20 dev 배포는 취소됨 · dev DB 는 0012」라고 적혀 있다. 그런데 `_RESUME.md` §4 는 「dev 배포 성공(run 44708143917 attempt 2) · alembic `0014_device_platform_android` (head)」라고 한다. 다른 세션의 prod 절차 문서라 손대지 않았다. 코디가 어느 쪽이 맞는지 확인해야 한다.

## 2. 구현 사실 동기화 — 바꾼 곳(줄 = 새 HEAD 기준)

표기: `S0` · `S1` · `S2` · `S3` · `S5` = spec-000 · 001 · 002 · 003 · 005, `MD` = `40-architecture/mobile-deployment.md`. 옛 문장은 취소선으로 남기고 「→ 개정 …」을 달았다. 새 정책과 새 글자는 없다.

| 사실(근거) | 바꾼 곳 |
|---|---|
| 개정 머리말 | S3:77 개정 ⑳ · S1:50 개정 ⑪ · S2:43 개정 ㉖ · S5:38 2026-11-22 개정 · MD:27 ⑥ |
| **바로 시작 = [의사 호출] 옆 [바로 시작] → 의사 호출 드로어 재사용 · 원장 고르기 없음 · 체크 가능 = `canQuickStart` · 거절 토스트는 코드마다 한 장씩 차례로**(사용자 · `room_screen.dart:513` `PickMode.quickStart` · mobile M2 · M2 고침 W-1 `toast.dart`) | S3:486(U-18 고르기 — 옛 「designer 시안 뒤」 취소선) · S3:488(결과 — 중복 없이 처음 나온 순서 · 한 장씩 · 200 = 닫힘 · 409 = 드로어 그대로) |
| **시안 없음 → 앱 = 기존 컴포넌트 + 웹 배치 · 글자**(사용자) | S3:476(U-17 로그인 카드 안 · OQ-A52) · S3:507(U-21 머리 방 이름 ▾ · 창 모양) · S3:510(점유 띠 자리 · 모양) · S3:516(U-22 「원장 변경」 `ui.html:400 · :459` · **시술 칸 「호출할 시술」 안 그림** — 검수 M2 F-1 · `room_screen.dart:528`) · OQ 표 S3:1169 A52 · S3:1170 A54 닫음 |
| **U-21 「복귀」 → 「복귀하기」**(검수 M1 W-1 · `copy.dart:96` · 웹 `board_parts.html:178 · :279`) | S3:509 |
| **통역 동시 상한 3**(`deploy/config/dev.env:43` · `prod.env:44` · 코드 기본값 6 그대로) | S3:776(동시 세션 절) · S3:796(설정 표) · S3:834(「바뀌지 않는 것」 줄) · S3:836(Soniox 한도 줄) · S3:1149(OQ-A46 표시) · S3:1155(**I-1 닫음**) |
| **푸시 묶음 = iOS `apns-collapse-id` = callId · Android tag `call:{callId}` · 새 칸 없음**(`adapters/apns.py:98-100` · `PushLogic.kt:61`) | S3:449(호출 취소 푸시 줄) · S3:706(FCM 메시지 모양 줄) · S5:38 · S5:277(「닫을 범위」 ②) |
| **`/api/auth/device` client=web → 400 `invalid_request`**(`routers/api/auth.py:154`) | S1:50 · S1:269(웹 API 표 — OQ-K18 닫음 표시) · S1:439(Validation 표) · S1:632(**OQ-K18 닫음**) |
| **migration `0013_doctor_call_cancel_kind` · `0014_device_platform_android`**(dev 0012 = `0012_kos_keys`) | S0:40(우리 2026-11-20 문단 ① ②) |
| **통역 드로어 재생 중 안내 「번역 음성이 나오는 동안은 듣지 않아요」 지움 · 「번역 읽는 중」 그대로 · 대리 수락 창 「호출할 시술 · N개」 그대로**(사용자 · `interpret_widgets.dart:407`) | S3:462(U-15 통역 드로어 줄) · S3:77 ⑦ |
| **release Android 빌드는 Firebase 설정이 없으면 멈춤 · `-PDAY_ALLOW_NO_PUSH=true` 예외**(`build.gradle.kts:114-118`) | S3:708(FCM 빌드 줄 — **OQ-A60 닫음**) · S3:1183(OQ-A60 행) · MD:27 · MD:294(§8-1 새 줄) |
| FCM 칸 이름 · `android` 기기 검사 = 기본값대로(`adapters/fcm.py` · `services/push.py` · `schemas/devices.py`) | S3:1167 **OQ-A50** · S3:1168 **OQ-A51** 닫음 · MD:396(M-9 행 끝) |
| 기기 선택 뒤로 가기 = 입력 화면(mobile M2) · 목록 카드 담당의 규칙(mobile M1 `format.dart` `taskDoctorLabel`) | S3:479 · S3:1179 **OQ-A53** · S3:1182 **OQ-A58** 닫음 |
| 앞에 있을 때도 호출 취소 배너(기본값대로) | S5:464 **OQ-N20** 닫음(실기기 확인 전) |
| 바로 시작 전부 거절 = 409 + 첫 코드 · 칸 이름 셋 = 기본값대로(`presentation/board.py:172-174`) | S2:1168 **OQ-77** · S2:1169 **OQ-78** 닫음 |
| 실기기 확인 못 한 것 | S3:1185 I-6 「**실기기 확인 전**」 · S3:77 · S5:38 에 「A-50 실기기 확인 전」 |
| log | `log.md:17` 2026-11-22 행(PR 칸 「PR 전 · 코디가 PR」 — #955 번호로 바꿀 것) |

frontmatter `last_updated` 는 커밋 때 hook 이 2026-11-22 로 바꿨다(S0 · S1 · S2 · S3 · S5 · MD 의 7 · 8줄).

## 3. 남은 문장 3

| # | 바꾼 곳 |
|---|---|
| U-21 「복귀」 → 「복귀하기」 | S3:509(위 표) |
| SPEC-002 `canChangeDoctor` 주석을 개정 ㉕ ③ 과 맞춤(검수 P2 WARN-3) | S2:674 — 「accepted · doing · 담당 원장 또는 systemDoctor」에 취소선을 긋고 「→ `doctor_change_block` 이 막지 않음(귀가 아님 · accepted · doing — 담당 원장 · systemDoctor 는 보지 않아 둘 다 없는 줄도 true · ③ ⓐ · OQ-78)」으로 바꿈. 같은 줄 「이름 제안 OQ-78」 → 「OQ-78 닫음」 |
| 바로 시작 드로어 결정 | S3:486 · :488(위 표) |

## 검증

- `python3 scripts/lint-pipeline.py --strict` → **0 error · 263 warning** · `products/day/` 줄은 **0**(ERROR · WARN 모두). 263 WARN 은 다른 제품 몫이다.
- diff `+` 줄의 비밀값 grep(키 · 이메일 · IP · Azure 이름 · Key Vault 이름 · Firebase 값) → **0건**.
- 커밋 2개 = rebase 된 `5cf09d21` + 새 커밋 `bc3f9669` 하나. push 는 하지 않았다.

## Delivery #262 · #263 v2 재결속 때 넣을 문구(spec-5-report 목록 + 이번 구현 사실)

준비된 요청 파일은 `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-day-mobile-v2-spec/55c97167-02b2-4ce4-8179-785d92dc4074/scratchpad/delivery/main.v2.request.json` · `fcm.v2.request.json` 이다. **#955 머지 뒤 `spec_baseline_revision` = 머지 SHA** 로 바꾸고, 아래를 더해 다시 만든다. 지금 요청에 든 baseline `7d198317` 은 rebase 로 사라진 커밋이라 쓸 수 없다. 이제 코드가 dev 에 있으므로, 재결속은 「구현할 일」이 아니라 「구현된 것을 검수 · 동기화할 계약」으로 읽혀야 한다. 단계(P1 ~ P7 · F1 ~ F3)를 완료로 표시할지는 harness 규칙(review-delivery)을 따른다.

**spec-5-report 목록 — 그대로 유지**
- `can*` = 서비스 거절 규칙이 정본이다.
- 호출 취소에는 확인 창이 없다 · 복귀 · 점유 띠 · 방 목록 재묶음 · 「담당의 미정」도 누른다.
- 호출 취소 알림: 본문 「{방} · 호출 취소」 · 그 호출이 완전히 닫힐 때만 · 원래 알림 닫기 · 웹은 OS 알림만.
- 단계 시작 조건 = 의존 표를 따른다.
- 출시 순서: prod 서버 먼저 → 정식 앱 · 되돌리기에 통역 되울림 · 새 경로 404.
- 통역: TokenGate · 빈 final · `audio_stop` · `playback_stopped`.
- Firebase 준비됨 · 한 벌 · 채널 「원장 호출」 · 「채팅」.

**#262(main)에 더할 것**
- Target Delta M-4 / A3:
  - 바로 시작 = 룸 상세 [의사 호출] 옆 [바로 시작] → 의사 호출 드로어 재사용 · 원장 고르기 없음 · 체크 가능 = `canQuickStart` · `rejected[]` 토스트는 코드마다 한 장씩 차례로.
  - 방 옮기기 = 머리 방 이름(▾) · 버튼 「복귀하기」 · 원장 바꾸기 창 「원장 변경」 · 시술 칸 없음.
- Review Surface:
  - 「designer 시안 게이트(A52 · A54)」 줄을 걷는다. **시안 없음(사용자)** — 앱 = 기존 컴포넌트 + 웹 배치 · 글자다.
  - 착수 막는 OQ 줄을 「없음 — K18 · 77 · 78 · A50 · A51 · A52 · A54 모두 닫음」으로 바꾼다.
- M-8 / A5 통역:
  - 동시 상한 = dev · prod 설정 3(`DAY_INTERPRET_MAX_SESSIONS=3` · I-1 닫음).
  - 재생 중 안내 줄은 없다 · 「번역 읽는 중」 그대로.
- A4 / M-6: 푸시 묶음 = iOS `apns-collapse-id` = callId · 새 칸 없음.
- M-3 / A1: `/api/auth/device` client=web = 400 `invalid_request`.
- migration: `0013_doctor_call_cancel_kind` · `0014_device_platform_android`(dev `0012_kos_keys` 다음). 롤백 메모 = 0013 앞 이미지로 되돌리면 알림 목록이 500 이 난다(P3 검수) → migration 도 같이 되돌린다.
- 실기기 확인(A-50 · I-6)은 **실기기 확인 전**이다(DAY Dev 0.2.0 — TestFlight (4) · Play internal vc4).

**#263(FCM)에 더할 것**
- 알림 tag = `call:{callId}`(원장 호출 · 호출 취소가 같은 자리를 덮음) · 채팅은 메시지마다.
- release Android 빌드는 Firebase 설정이 없으면 멈춘다(`-PDAY_ALLOW_NO_PUSH=true` 예외 · OQ-A60 닫음).
- 칸 이름 `DAY_FCM_SERVICE_ACCOUNT` · `DAY_FCM_ALLOWED_APP_IDS` · `android` 는 `push_env` 를 보내면 400 · 토큰 4096자 이하(OQ-A50 · A51 닫음).
- dev 서버에는 FCM 키가 실렸다(`_RESUME.md` §4). prod 는 prod 배포 때 넣는다.
- migration `0014_device_platform_android`.
