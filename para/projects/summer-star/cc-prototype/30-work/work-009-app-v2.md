---
type: work
id: WORK-009
title: "앱 다음 판 — 4탭 · 새 틀 · 웹 쓰기 · 상담사 호출 푸시 · 알림 둘 · QR 문진 · 여권 스캔 · 웹 따라잡기"
status: draft
product: cc-prototype
feature: procedure
work_type: enhancement
owner: kknaks
progress: 0
created_at: 2026-10-27
updated_at: 2026-10-27
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/work
  - status/draft
links:
  baselines:
    - "[[baseline-008-procedure-board|BASE-008]]"
    - "[[baseline-009-reservation-board|BASE-009]]"
  decisions:
    - "[[decision-007-app-v2|DEC-007]]"
  specs:
    - "[[spec-004-procedure-app|SPEC-004]]"
    - "[[spec-005-reservation-board|SPEC-005]]"
    - "[[spec-003-procedure-board|SPEC-003]]"
  works:
    - "[[work-004-procedure-app|WORK-004]]"
    - "[[work-007-reservation-board|WORK-007]]"
    - "[[work-008-procedure-board-v2|WORK-008]]"
  releases: []
  related: []
sources:
  - "orchestration/work/overall-board/_RESUME.md §2 (2026-10-26 · 10-27 앱 줄 · 「AP-1 ~ AP-45 기본값 전부 승인」)"
  - "reference/2026-10-27-cc-app/workflow-app.md"
  - "cc-prototype overall-board procedure/ (branch kknaksss/overall-board-2 — 읽기만 · app/lib · back/app)"
  - "orchestration/work/overall-board/app-review-doc-r1.md · app-wp-kos-report.md (r2)"
---

# 앱 다음 판 — 빌드 계획

계약은 **SPEC-004 0.4.0 → r2 0.4.1**(§1.1 · §3.4 · §3.7 · §5-2 ~ §5-4 · §6.0 ~ §6.3 · §6.8 ~ §6.17 · §7.1 · §7.3 · §7.4 · §8.0 · §8.6 ~ §8.8 · 부록 C · D) — 이 문서는 빌드 계획만 적고 계약을 다시 쓰지 않는다. 결정 = DEC-007.

> 1 파일 = 1 work = **빌드 계획**. 결정 원천 = `_RESUME` §2(DEC-007 부록 A). 앱 · 새 화면 = 시안 v4 정본 · 웹 규칙 = 배포된 웹 구현본.

## Meta

- Covers spec: SPEC-004 0.4.1(위 절 · r2) · 기대는 웹 계약 SPEC-005 0.4.0(예약 API · 2계층) · SPEC-003 0.6.0(§5.13 · §5.14 · §10.1)
- 코드 레포: `kknaksss/cc-prototype` — 범위 **`procedure/back/**` · `procedure/app/**` · `procedure/front/**`(SPEC-004 §6.17 자리만)**. infra 레포 `MediSolveAIDev/k8s_infra_mac` — WP-INFRA 만
- base: 같은 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` · branch `kknaksss/overall-board-2` — `_RESUME` 10-27 「다음 판 = 한 slug · 한 PR · ③ → ② → ①」 · **① 앱은 ③ 예약 잔여 · ② 시술 현황(WORK-008) 뒤**
- 워커: researcher(WP-KOS) · infra · backend · mobile(app) · frontend(§6.17) · reviewer · 코디(E2E)
- 검증은 WP 마다 그 범위만(`uv run pytest -q -k …` · `flutter analyze` · `flutter test` · `tsc` · lint). 전체 검증(pytest 전부 · `flutter build ipa` · front build · compose · 데모 지점)은 WP-E2E 에서 한 번
- **완료 = 사용자가 TestFlight 실기기(iOS)에서 SPEC-004 §8.8 E1 ~ E9 를 본 것**(시뮬레이터 · 웹 확인으로 대신하지 않는다 — 카메라 · 푸시는 실기기만)
- 데모 지점에만 쓴다 · 운영 명동점 쓰기 금지(D7-12) · public — 실명 · KOS id · 키 · 토큰 · 여권 값 금지

## 계약 고정점

| 고정점 | 값 | SPEC-004 |
|---|---|---|
| 역할 | admin · doctor · nurse · coordinator · **counselor** · 새 API 다섯 역할 ○ · 수락 분기 `admin \| coordinator \| counselor` | §3.4 · §3.7 |
| 상태 | 웹 `view.tsx` `MAIN_TONE` · `phaseStyle` · `stateText` 값 그대로 Dart 표 한 곳 | §6.9 |
| 쓰기 | SPEC-005 §7.5 API 그대로(새 back 로직 없음) · 수납 · 처방전 버튼 없음 | §6.11 |
| 알림 | 종류 둘(`doctor_call` · `counselor_call`) · `display` 는 목록 밖 | §5-2 ~ §5-4 |
| 경로 | ~~49~~ **50 = HTTP 49 + WS 1(새 HTTP 15 — unlock 더함)**(r2) | §7.3 |
| 기기 | `deviceId` = SSE 쿼리 · pending · claim · 문진 · 스캔 · unlock · 남의 계정 = 404 `device_not_found` · SSE 허브 계정 · 기기 단위(r2) | §5-3 · §7.1 |
| 사진 | `PROC_PHOTO_DIR`(PVC · 암호화 = 지원하면 켬 r2) · 무작위 파일 이름 · 원본 · 사진첩 저장 없음 · 주석 5곳 · 열람 = Bearer(웹 fetch → blob · r2) · KOS 이미지 = `get-codes` 이름 「태블릿」 실행 때 찾기 · `category` 없음(r2) | §2.3 · §6.16 · §6.17 · §7.4 |

## Work Packages

| WP | 내용 | 계약 | 워커 | 대상 파일(범위) | 완료 조건 | 검증 명령(부분) | 상태 |
|---|---|---|---|---|---|---|---|
| **WP-KOS** (게이트) | 데모 지점 1회씩: **K1** `update-reservation{counselor}` 를 상담 대기 · 상담 진행 일정에(웹 SPEC-005 §9 #25 결과가 있으면 그것으로 닫음) · **K2** `update-visitor-personal-information` 에 `passportExpiryDate`(`yyyy-MM-dd`) · **K3** 공개 `generateUploadingImageUrl` → PUT → `registerVisitorImages` + 분류 · 장비 코드(`get-codes`) 고르기 · **K4** ~~내부 `get-visitor-files`~~ 내부 `get-visitor-images`(r2) 로 K3 사진이 보이는지. 시험 고객 = `[ccc 시험]` · 시험 사진 = 지어낸 그림(실제 신분증 아님). **쓰기 허가는 사용자**(코디가 받는다) | §8.0 #8 · #21 ~ #23 · OQ-619 · OQ-622 | researcher | 코드 없음 · 리포트 ~~`app-kos-probe-report.md`~~ **`orchestration/work/overall-board/app-wp-kos-report.md`**(r2) | K1 ~ K4 각 확인 / 거절 + 응답 모양 · 데모 흔적 목록 · 값(id · 토큰) 없음 | 리포트 grep(24자 id · 토큰 0) | **완료**(2026-10-27 · r2) — K1 · K2 · K3 받음 · K4 = 사진은 `get-visitor-images` 에 보임 · 「못 넘으면」 분기 없음 · Q-154 ~ Q-157 코디 기본값(경로 = `get-visitor-images` · 분류 안 보냄 · `scheduleId` · `path` 안 보냄 · **데모 흔적 둠**) → SPEC-004 0.4.1 §6.16 ④-a · ④-c · §8.0 |
| **WP-INFRA** | 사진 볼륨 — back 파드에 PVC(작게 · 백업 없음) 마운트 · env `PROC_PHOTO_DIR` · compose 이름 있는 볼륨 · `.env.example` 이름 한 줄 · 상담사 env 3개 Secret 예시 이름(`CCC_COUNSELOR_*`) | §2.3 · D7-54 | infra | infra 레포 back Deployment · PVC · Secret 예시 / 코드 레포 `procedure/compose*.yml` · `.env.example` | 로컬 compose 에서 볼륨 마운트 · 컨테이너 재시작 뒤 파일 남음 · **볼륨 암호화 = 클러스터 저장소가 지원하는지 확인 · 보고(되면 켬 · 안 되면 없음 + PVC 정의에 법적 검토 주석 — SPEC-004 §2.3 · OQ-626 · D7-68)**(r2) · infra PR(머지는 코디 · 사용자) | `docker compose config` · `kubectl apply --dry-run=client` | 대기 |
| **WP-BE1** | **계정 · 기기 · 알림 바탕** — `counselor` 역할(모델 · schemas · `accept()` 분기 · 전수 grep) · 상담사 계정 동기화(§3.7 · 상담사 목록 함수 재사용) · `device.name · kind · last_seen_at` · `POST /api/devices` 응답 `deviceId` · stream `deviceId` 쿼리 · `notification` · `notification_setting` 표 · `GET/POST /api/notifications*` · `GET/PUT /api/me/notification-settings` · 원장 호출 발송에 `notification` 행 · `kind:"doctor_call"` · 설정 끔 반영 · SSE `notification` 이벤트 · **SSE 허브 계정 · 기기 단위**(연결마다 계정 · `deviceId` · `send_to_account` · `send_to_device` · `online` · 새 이벤트 `id:` 없음 · version 그대로 — r2) · ~~`push_log` 열~~ **`push_log` 표 다시 만들기**(옛 NOT NULL DB 에서 · 멱등 — r2) · `deviceId` 확인(`device_not_found` · r2) | §3.1 · §3.4 · §3.7 · §5-1.1 · §5-3 「기기 확인」 · §5-4 · §7.1 · §7.4 | backend | `procedure/back/app/{domain,schemas,service/accounts.py,service/push.py,service/notifications.py(새),service/stream.py,api/board.py,api/*,repository/db.py,repository/*}` · `tests/`(r2 — `service/stream.py` · `api/board.py` · `repository/db.py` 이름으로 더함) | §8.6 「역할 다섯」 · 「상담사 계정」 · 「원장 호출 회귀」 · 「알림」 · **「마이그레이션」 · 「SSE 허브」**(r2) 통과 · 기존 시험 그대로 | `cd procedure/back && uv run pytest -q -k "role or account or push or notification or migrat or stream"` | 대기 |
| **WP-BE2** | **상담사 호출 푸시** — `counselor-call` 성공(KOS 200 + 이벤트 커밋) 뒤 비동기 발송 · 받는 사람 = 그 상담사 계정 · 내용 · payload · `push_log.kind` · `notification` | §5-2 | backend | `service/push.py` · `service/reservations*.py`(counselor-call 끝) · `tests/` | §8.6 「상담사 호출 푸시」 통과 | `uv run pytest -q -k counselor` | 대기 (WP-BE1 뒤 · ~~K1 뒤~~ K1 통과 r2) |
| **WP-BE3** | **띄우기 요청** — `display_request` 표 · targets · 만들기 · pending · claim(해시 · 1회 · 10분) · close · SSE `display` · 띄우기 푸시(`display` · 목록 밖) · 상세 응답 `displays[]` · 만료 처리 | §5-3 · §7.3 · §7.4 | backend | `service/display.py`(새) · `api/display.py`(새) · `service/reservations*.py`(상세 응답) · `tests/` | §8.6 「띄우기」 통과(같은 계정 기기 둘 가르기 · `deviceId` 필수 · 보이는 알림 소리 없음 — r2) | `uv run pytest -q -k display` | 대기 (WP-BE1 뒤) |
| **WP-BE4** | **문진** — `GET/POST /api/questionnaires/{reservationId}`(`deviceId` · r2) · **`POST /api/auth/unlock`(기기별 5회 · 1분 · 로그인 실패 수와 따로 — D7-71 · r2)** · 같은 제출본 `read` 행 → `app_submit` 으로 고침(r2) · 언어 표 `domain/languages.py`(출처 주석) · KOS 공개 양식 · 약관 · 제출 · 제출 확인 · `questionnaire_history` 열(`source` · `language` · `device_id` · `display_request_id`) · 주민번호 · 발음 400 · 띄우기 done | §6.15 · §7.4 · §8.0 #16 ~ #20 | backend | `domain/languages.py`(새) · `service/questionnaire.py`(새) · `kos/client.py`(공개 메서드 더함) · `api/questionnaire.py`(새) · `service/auth.py` · `api/auth.py`(unlock · r2) · `repository/repo.py`(이력 고침 · r2) · `tests/` | §8.6 「문진」 통과 · 데모 1회 제출 200(시험 고객) | `uv run pytest -q -k "questionnaire or unlock"` | 대기 (WP-BE3 뒤) |
| **WP-BE5** | **여권 스캔 · 사진** — `passport-scan`(multipart · 5MB) · 고객 수정 함수 재사용(SPEC-005 §5.13 — 직전 다시 읽기 · ~~13키~~ 있는 키 전부 r2) · 만료일 보냄(K2 받음 r2) · 사진 `PROC_PHOTO_DIR` · `id_photo` 표 · KOS 이미지 올리기(K3 본문 — `category` · `scheduleId` · `path` 없음 · 장비 = `get-codes` 이름 「태블릿」 실행 때 · 못 찾으면 `failed` · `equipment_code_missing` r2) · kos-retry · 사진 열람(Bearer 헤더만 r2) · `identity_check` `app_scan` / `app_manual` · 이벤트 · **법적 검토 주석 ①②③** | §6.16 · §7.4 · §8.0 #21 ~ #23 | backend | `service/passport_scan.py`(새) · `service/id_photo.py`(새) · `kos/client.py` · `api/customers*.py` · `tests/` | §8.6 「스캔」 · 「경로 수」(~~`test_route_count_49`~~ **`test_route_count_50`** r2) 통과 · 주석 3곳 grep · 레포에 KOS 코드 id 0 | `uv run pytest -q -k "scan or photo or route_count"` · `grep -rn "법적 검토 필요" procedure/back` ≥ 3 | 대기 (WP-INFRA · WP-BE3 뒤 · WP-KOS 완료 r2) |
| **WP-APP1** | **새 틀** — 탭바 · 레일 · 공통 헤더(종 · 배지) · 탭별 스택 · 시술 현황 탭 = 지금 화면(헤더 · 계정 ▾ 정리) · 설정 탭(계정 · 알림 · 이 기기 이름(D7-70 · 기기 행 없으면 안내 r2) · 앱 정보 · 로그아웃) · 로그인 제목 · 앱 이름 「Céramique」 · 첫 화면 예약 현황 · 푸시 누름 → 탭 바꾸기 · `counselor` · `coordinator` 역할 값 · `deviceId` 받아 두기(로그아웃 때 지움 · SSE 쿼리 · r2) | §2.4 · §6.1 · §6.2 머리 · §6.8 · §6.14 · §5-1.3 | mobile | `procedure/app/lib/{main.dart,screens/shell*.dart(새),screens/settings*.dart(새),widgets/header.dart,model/account.dart,push/*,app_state.dart}` · `ios/Runner/Info.plist` | 시뮬레이터 스크린샷(폰 · 패드 × 4탭 · 설정) · 기존 시술 현황 동작 회귀 없음 | `cd procedure/app && flutter analyze && flutter test` | 대기 (WP-BE1 뒤 — 설정 API) |
| **WP-APP2** | **웹 따라잡기** — 카드 순서 = 배열 · `isRoomTask` 만 숨김(ETCETERA 줄) · 되돌리기(아이콘 · 확인 시트 · 토스트 [되돌리기]) · 2계층 표 `view/state.dart`(시술 현황 · 예약 공용) · 발음 · 「시술 완료」 배지 제거 · 필터 점 | §6.0 · §6.2 · §6.3 · §6.9 · 부록 D | mobile | `procedure/app/lib/{view/view.dart,view/state.dart(새),screens/board_screen.dart,screens/room_screen.dart,model/board.dart}` | §8.7 해당 시험 · 웹과 같은 판을 나란히 둔 스크린샷 | `flutter analyze && flutter test` | 대기 (WP-APP1 뒤 · 같은 파일 충돌 피함) |
| **WP-APP3** | **예약 현황 · 내원 현황 · 예약 상세**(앱엔 [스캔할 기기] 없음 — D7-72 r2) — 표(폰 시간대 목록 + 그룹 칩 · 패드 가로 스크롤 표) · 지금 시각 스크롤 · 상세(합집합 칸 · 쓰기 버튼 · 방 시트 · 상담사 시트 · 정산 글자만 · 5초 폴링 · 409 토스트) · 내원 현황 · [태블릿에 띄우기] · [여권 스캔] 진입 · [QR 읽기] | §6.10 ~ §6.12 · §5-3 | mobile | `procedure/app/lib/{screens/reservations*.dart,screens/reservation*.dart,screens/visits*.dart,api/*,model/reservation*.dart}`(새) | 데모 back 에 붙여 시뮬레이터로 쓰기 1회씩(웹 반영 확인) · 스크린샷 | `flutter analyze && flutter test` | 대기 (WP-APP2 뒤) |
| **WP-APP4** | **알림 목록 · 상담사 푸시 받기** — 알림 화면 · 배지 · 읽음 · `counselor_call` 누름 → 예약 상세 · `display` 누름 → 화면 열기 · SSE `notification` · `display`(`id:` 없음 · `board` 만 version r2) · pending 읽기(`?deviceId=` r2) | §5-2 ~ §5-4 · §6.13 · §7.1 | mobile | `procedure/app/lib/{screens/notifications*.dart(새),push/*,sse/*,ios/Runner/AppDelegate.swift}` | §8.7 · 시뮬레이터 목록 스크린샷(푸시 자체는 WP-E2E 실기기) | `flutter analyze && flutter test` | 대기 (WP-APP1 · WP-BE2 · WP-BE3 뒤) |
| **WP-APP5** | **문진 화면** — 잠금(탭 · 헤더 · 배너 · 뒤로 · 가장자리) · 언어 칩 6 · KOS 양식 4쪽 · 미리 채움 · 동의 · 제출 · 끝 · 대기 화면 · [직원] 길게 + 비밀번호 → `POST /api/auth/unlock`(기기별 5회 · 1분 문구 · 대기 화면도 잠금 — r2) · 실패 문구(6개 언어) · 문진 `GET` · `POST` 에 `deviceId`(r2) | §6.15 | mobile | `procedure/app/lib/screens/questionnaire*.dart`(새) · `lib/l10n/questionnaire_*.dart`(고정 문구 6언어) | 시뮬레이터 4쪽 · 언어 3가지 · 잠금 스크린샷 · 데모 제출 1회(시험 고객) | `flutter analyze && flutter test` | 대기 (WP-BE4 · WP-APP4 뒤) |
| **WP-APP6** | **여권 스캔 · 스캔 확인** — 카메라 · 가이드 틀 · Swift Vision 채널 · MRZ 파서 · 검사 숫자 · 세기 규칙(생년월일 · 만료일 r2) · alpha-3 → 2 · 3번 실패 → 손 입력 · 확인 화면(나란히 · 강조) · multipart 저장 · ccc / KOS 결과 따로 · 사진 다시 올리기 · 메모리만(사진첩 0) · **법적 검토 주석 ④⑤** · `NSCameraUsageDescription` | §6.16 · §2.1 · §2.4 | mobile | `procedure/app/lib/{scan/*(새),screens/scan*.dart(새)}` · `ios/Runner/TextScanner.swift`(새) · `Info.plist` | MRZ 단위 시험(견본값) · 시뮬레이터 = 손 입력 길 · 카메라는 WP-E2E 실기기 · `grep "법적 검토 필요"` 앱 ≥ 2 | `flutter analyze && flutter test` | 대기 (WP-BE5 · WP-APP3 뒤) |
| **WP-FE** | **웹 front 닿는 곳** — 상세 [QR로 고객 입력 요청] QR 상자 · [태블릿에 띄우기] 기기 목록 · 상태 · [스캔할 기기] 단계 · 썸네일(`fetch` + Bearer → blob URL · r2) · 「{기기}에서 수신」 · KOS 사진 실패 표시 · 역할 값 `counselor` | §6.17 · §3.4 | frontend | `procedure/front/components/reservations/**` · `lib/types.ts` · `lib/session.ts` | 로컬 웹에서 띄우기 만들기 · 닫기 · 상태 단계 · 썸네일(가짜 사진) 스크린샷 · 예약 현황 그 밖 화면 회귀 없음 | `cd procedure/front && npx tsc --noEmit && npm run lint` | 대기 (WP-BE3 · WP-BE5 뒤) |
| **WP-REVIEW** | reviewer: SPEC-004 부록 C(D-01 ~ D-66) · 부록 D · §3.4 · §7.3(경로 49) · §7.4 · §8.0 게이트 처리 ↔ 코드 · 법적 검토 주석 5곳 · 실명 · id grep · 웹 2계층 값이 웹 구현과 같은지. FAIL 은 모아서 한 번에 수정 발주 | 전체 | reviewer | 코드 전체 | PASS | — | 대기 |
| **WP-E2E** | 코디: 전체 검증 · compose 재기동 · 배포(코디 · 사용자 결정 — 앱 TestFlight 는 배포 주소) → **사용자 실기기 iOS E2E §8.8 E1 ~ E9**(아이폰 2 · 아이패드 1 · 맥 웹) · 피드백은 모아서 한 번에 | §8.8 | 코디 · 사용자 · (수정) 각 워커 | — | E1 ~ E9 사용자 확인 | `uv run pytest -q` · `flutter analyze && flutter test && flutter build ipa --release --dart-define=API_BASE=https://ccc.medisolveai.xyz --build-number=<+1>` · `npm run build` | 대기 |

## 병렬

```text
WP-KOS ──────────────┐
WP-INFRA ────────────┤
WP-BE1 ─┬─ WP-BE2 ───┼──────────────┐
        └─ WP-BE3 ─┬─ WP-BE4 ───────┤
                   └─ WP-BE5(K2·K3·INFRA) ─┐
WP-BE1 ── WP-APP1 ── WP-APP2 ── WP-APP3 ──┐│
                     WP-APP4(BE2·BE3) ── WP-APP5(BE4) ── WP-APP6(BE5·APP3) ──┬── WP-REVIEW ── WP-E2E
WP-BE3 ─┬───────────────────────────────────────────────────────────────────┤
WP-BE5 ─┴── WP-FE(BE3·BE5 뒤 · 앱과 따로) ─────────────────────────────────────┘
```

- (r2) WP-FE 는 **WP-BE3 · WP-BE5 뒤 바로**(표 의존 그대로) — 앱 WP 를 기다리지 않는다. WP-REVIEW 는 APP6 · FE 둘 다 끝난 뒤. WP-KOS = 완료(위 표)

- back 은 한 워커가 BE1 → BE2 ∥ BE3 → BE4 → BE5 순서(같은 `service/push.py` · `kos/client.py` 를 만진다 — 둘로 나누면 충돌)
- 앱은 한 mobile 워커가 APP1 → APP6 차례로(같은 `main.dart` · `app_state.dart`). back 이 늦으면 가짜 응답으로 화면부터 · API 붙이기는 그 BE 뒤
- WP-KOS · WP-INFRA 는 처음부터 따로 — K2 · K3 결과가 BE5 범위를 정한다(게이트를 못 넘으면 SPEC-004 §8.0 끝 줄대로 줄이고 사용자에게)

## 주의

- `_RESUME` 10-27 순서: ③ 예약 잔여 → ② 시술 현황(WORK-008) → **① 이 문서** · 같은 branch · PR 하나. WORK-008 의 웹 2계층 값이 이 판 앱 값의 원천이라 ② 가 먼저 머지 상태여야 한다
- 앱 실기기 확인 전에 「완료」라고 하지 않는다 · 워커는 사용자 포트 · 프로세스를 건드리지 않는다
- 백엔드 커밋 뒤 compose 재기동(옛 코드로 E2E 금지)
- 시험 사진 · 여권 값은 지어낸 것 · 견본만 — 레포 · 리포트에 실제 값 0
- archive 전 `git status --ignored` 확인(사진 볼륨 · `.env` · `.p8`)
