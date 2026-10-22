---
type: work
id: WORK-004
title: "명동 PoC v2 구현 — 시술실 앱(Flutter · iOS) · 계정 · 권한 · 통역 · 원장 호출 푸시 · 최종 배포"
status: in-progress
product: cc-prototype
feature: procedure
work_type: new-feature
owner: kknaks
progress: 90
created_at: 2026-10-21
updated_at: 2026-10-22
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/work
  - status/in-progress
links:
  baselines:
    - "[[baseline-008-procedure-board|BASE-008]]"
  decisions:
    - "[[decision-005-procedure-board|DEC-005]]"
  specs:
    - "[[spec-004-procedure-app|SPEC-004]]"
    - "[[spec-003-procedure-board|SPEC-003]]"
  works:
    - "[[work-003-procedure-board|WORK-003]]"
  releases: []
  related: []
---

# 명동 PoC v2 구현 — 시술실 앱 · 계정 · 권한 · 통역

SPEC-004 를 **아이폰 · 아이패드 실기기 E2E(맥 IP back)** 까지 넣고, 그 뒤 **마지막 WP 로 back · front 를 `ccc.medisolveai.xyz` 에 배포**한다
(SPEC-004 A-11 · A-12 — 배포는 기기 E2E 앞이 아니라 맨 뒤 · 별도).

> **2026-10-22 상태(머지 전 동기화 · SPEC-004 0.3.0)**: 실제 순서는 「배포 먼저」(SPEC-004 A-20)로 바뀌었다 — WP1 ~ WP5 · WP11 · WP12 → 사용자 로컬 앱 E2E(A1 ~ A7 수정) → **WP10 배포(2026-10-21)** → TestFlight 빌드 1 ~ 2 → 실기기 피드백(T1 ~ T8) · 정상 로그인(OQ-601 닫힘) 수정 → main `329b543`(#4) · infra #24. 리뷰(WP6)는 하지 않았다. 남은 것 = WP9 의 기기 확인 일부 · 「열린 것」.
>
> 2026-10-21 SPEC-004 0.2.0 — 원장 호출 푸시(A-14) WP11(backend) · WP12(mobile) 추가 · 관리자도 모든 호출 푸시 · 앱 관리자 수락 = 원장 고르기(A-15) · WP9 에 D6 · WP10 에 푸시 1회. WP 번호는 순서가 아니다 — 순서는 「병렬」 그림.
>
> 1 파일 = 1 work = **빌드 계획**. 계약은 SPEC-004(+ SPEC-003)를 참조만 한다.

## Meta

- Covers spec: SPEC-004 (현황판 규칙 · 스냅샷 · SSE 는 SPEC-003)
- 코드 레포: `kknaksss/cc-prototype` — 범위 `procedure/back` · `procedure/front` · **`procedure/app`(새)** · 배포 WP 는 `.github/workflows/` · `cc/` 이동 · infra 레포(`charts/cc-prototype` 등)
- slug: `myeongdong-poc-v2`(같은 작업 단위 · 같은 코드 워크트리) · 워커: backend · frontend · **mobile(새 — Flutter)** · reviewer · infra
- 순서 원칙: back 계정 · 권한(WP1)이 **로그인 응답 · 토큰 모양을 먼저 고정** → 앱은 그 모양으로 · 통역(WP2)과 앱 화면(WP4)은 병렬 → 앱 통역(WP5) → 리뷰 → 수정 → 로컬 E2E → TestFlight · 기기 E2E → **배포(마지막)**
- 검증은 WP 마다 그 범위만. 전체 검증(`pytest -q` 전체 · `flutter test` 전체 · 웹 build)은 WP8 에서 한 번
- 실기기 E2E · 마이크 · 통역 재생 · 권한 403 1회가 앱 완료 조건(SPEC-004 §8.4) — 시뮬레이터 · 웹 확인으로 대신하지 않는다

## Work Packages

| WP | 내용 | 계약 | 담당 | 범위(경로) | 완료 조건 | 검증 명령(부분) | 상태 |
|---|---|---|---|---|---|---|---|
| WP1 | **back 계정 · 권한** — `account` 테이블 · 서버 시작 upsert(어드민 · 간호사 env) · 직원 조회 뒤 원장마다 doctor 행 · 의사 카드(`CCC_DOCTOR_KOS_ACCOUNT_ID`) · 토큰 claims(`role` · `staffId`) · 검증은 DB 값 · `/api/auth/{accounts,login,me}` 새 모양 · **조작 service 입구 역할 검사**(§3.4 표 · 검사 순서) · `AcceptRequest.doctorId` 선택 · 의사 = 자기 원장 · 403 3종 · `actor` = `login_id` · 수락 payload `byRole` · `.env.example` 이름 추가 | SPEC-004 §2.3 · §3 | backend | `procedure/back/app/{repository,domain,service,api,schemas}/**` · `procedure/back/tests/test_auth_roles.py`(새) · `procedure/.env.example` | §8.1 「역할 행렬」(역할 3 × 조작 8) · 「수락」 7줄 · 「토큰」 · 「계정」 · 「actor」 시험 통과 · 기존 시험이 새 로그인 모양으로 고쳐져 통과 · `.env.example` 값 0 | `cd procedure/back && uv run ruff check . && uv run pytest -q tests/test_auth_roles.py tests/test_actions.py tests/test_stream.py` | 완료 — be4 보고(pytest 106) · 정상 로그인(bcrypt · 계정 목록 API 제거 · 5회/1분 잠금 · env 비밀번호)은 #4 에서 더함(SPEC-004 §3.3 0.3.0) |
| WP2 | **back 통역** — `cc/back`(`origin/main`) 통역 4파일 · api · 시험 **복사**(import 금지) · 의존성 · container 주입 · **WS 토큰 인증**(헤더 · 쿼리 · accept 전 검증 · Origin 규칙) · `SONIOX_API_KEY` · 오류 문구 경로 | SPEC-004 §4 | backend | `procedure/back/app/service/interpret/**` · `app/api/interpret.py` · `app/container.py` · `app/main.py`(router 등록) · `pyproject.toml` · `uv.lock` · `tests/test_interpret.py` | 복사한 시험 + §8.1 「통역」 인증 6건 통과 · 실 Soniox 1회(맥 · 브라우저 없이 시험 스크립트로 PCM 파일 1개 → `caption` · `audio_start` 수신) · 로그에 토큰 · 키 0 | `uv run pytest -q tests/test_interpret.py` · 실 Soniox 1회 | 완료 — 실 Soniox 1회(caption + 24kHz 음성) · WS 로그 token 0 |
| WP3 | **웹 로그인 계정 체계** — 로그인 카드 `role=admin` 만 · 세션에 `role` · `name` · 헤더 계정 이름 · 의국 수락은 `doctorId` 그대로 | SPEC-004 §3.6 | frontend | `procedure/front/{app/login,lib/session.ts,lib/api.ts,lib/types.ts,components/common}/**` | 웹 로그인 → 현황판 → 의국 수락이 WP1 back 으로 동작 · 카드 1개 | `cd procedure/front && npx tsc --noEmit && npm run lint && npm run build` | 완료 — 처음엔 관리자 카드 · #4 에서 **아이디 · 비밀번호 폼**으로 바뀜(SPEC-004 §3.6 0.3.0) |
| WP4 | **Flutter 앱 뼈대 · 화면** — `procedure/app` 생성(iOS 만) · Info.plist(마이크 · 로컬 네트워크 · ATS `NSAllowsLocalNetworking` · 수출 규정) · 서명 xcconfig(gitignore) · 테마 · 서버 주소 입력칸 · 로그인 · SSE 클라이언트(§7.1) · 모델(코드 `schemas/board.py` 필드) · 표시 매핑(웹 `view.ts` 옮김) · 목록 · 룸 상세 · 호출 시트 · 모바일 / 태블릿 배치 · 조작 8종 호출 · 토스트. 통역 바는 자리 + 빠른 말하기 칩(§5 · 기기 TTS)까지 | SPEC-004 §2.1 · §2.2 · §2.4 · §5 · §6.0 ~ §6.4 · §6.6 · §6.7 · §7 | mobile | `procedure/app/**` | `flutter analyze` 0 · §8.2 단위 시험 통과 · 시뮬레이터(아이폰 · 아이패드)에서 **실 back(로컬 compose)** 로 로그인 3역할 · 목록 · 룸 상세 · 호출 · 수락(의사) · 시작 · 종료 · 귀가 대기 동작 · 스크린샷(모바일 · 태블릿 × 화면 5) · 레포에 맥 IP · 팀 id 0 | `cd procedure/app && flutter analyze && flutter test && flutter build ios --simulator --dart-define=API_BASE=http://localhost:8700` | 완료 — analyze 0 · test 39 · 시뮬레이터 실 back · 로그인 폼 · 서버 주소 칸 debug 만(T8)은 #4 |
| WP5 | **앱 통역** — 통역 드로어(§6.5) · WS(헤더 토큰 · start · pause/resume · stop) · 마이크 PCM16 16kHz mono 40ms 조각 · 24kHz PCM 재생 · 재생 중 마이크 안 보냄 · 언어 8 · 국적 자동 · 번체 · 오류 · 백그라운드 닫기 · iOS 오디오 세션(녹음 + 스피커) | SPEC-004 §4.3 · §4.4 · §6.5 | mobile | `procedure/app/lib/interpret/**` · 드로어 위젯 · `ios/Runner/Info.plist` | `flutter test`(ws/wss 주소 · 메시지 처리 가짜 서버) · **시뮬레이터 + 맥 마이크로 WP2 back 에 실발화 1회** — 자막 양쪽 · 번역 음성 재생 | `flutter analyze && flutter test test/interpret_*` · 시뮬레이터 실발화 1회 | 구현 완료(드로어 · WS · 마이크 · 24kHz 재생) — **기기 실음성 결과 기록 없음**(SPEC-004 OQ-617) |
| WP11 | **back 원장 호출 푸시**(0.2.0) — `device` 테이블 · `POST /api/devices` · `DELETE /api/devices/{token}` · 호출 생성(`call_create` · `call_reassign_all`) 커밋 뒤 비동기 발송 · 받는 사람(SPEC-004 §5-1.2 규칙 표 — 의사: 지정 = 그 원장 계정 · 전체 = 전원 · 호출한 의사 자신 제외 / **관리자: 전체 · 지정 모두 · 자기가 누른 것도** / 간호사: 없음) · 내용(고객 이름 없음) · APNs HTTP/2 + ES256 JWT(40분) · `APNS_ENV` 호스트 · 실패 로그만 · 재시도 1회 · 410 삭제 · `APNS_*` 비면 끔 · `.env.example` 이름 5개 | SPEC-004 §2.3 · §5-1.1 · §5-1.2 | backend | `procedure/back/app/{repository,service,api,schemas}/**` · `app/push/`(새 · APNs 클라이언트) · `pyproject.toml` · `uv.lock` · `tests/test_push.py`(새) · `procedure/.env.example` | §8.1 「푸시」 ① ~ ⑥ 가짜 APNs 시험 통과 · 로그에 토큰 전체 · JWT · 키 0 · `.env.example` 값 0. (실 APNs 는 키가 생기면 WP9 에서) | `uv run pytest -q tests/test_push.py tests/test_actions.py` | 완료 — 113 passed · 그 뒤 `push_log` · `CALL` 카테고리(의사만) · 죽은 토큰 400 3종 삭제 · `X-Accept-Source` 더함 |
| WP12 | **앱 푸시**(0.2.0) — Xcode Push Notifications capability · 로그인 직후 알림 권한 요청 · APNs 기기 토큰(Firebase 의존 0 · 플랫폼 채널 또는 비 Firebase 패키지) → `POST /api/devices` · 토큰 바뀜 · 앱 시작 · 서버 주소 바뀜 때 재등록 · 로그아웃 때 `DELETE` 먼저 · 알림 누르면 `visitId` 룸 상세(꺼진 상태 · 로그인 전 포함) · 앞에 있을 때 배너 + 소리 · 「알림 꺼짐」 한 줄 · **관리자 계정 [수락] = 원장 고르기**(웹 호출 탭과 같은 규칙 · SPEC-004 §6.2 · §6.3 #2 — 0.2.0 A-15) | SPEC-004 §2.4 · §5-1.1 · §5-1.3 · §6.1 · §6.2 · §6.3 #2 | mobile | `procedure/app/lib/**`(push · 로그인 · 로그아웃 · 라우팅) · `ios/Runner/{AppDelegate.swift,Runner.entitlements,Info.plist}` · Xcode 프로젝트 capability | `flutter analyze` 0 · `flutter test`(알림 payload → 룸 상세 경로 · 로그아웃 순서 · 관리자 수락이 `doctorId` 를 보냄) · `pubspec.lock` 에 firebase 패키지 0 · 시뮬레이터에서 `.apns` 파일 끌어놓기(`xcrun simctl push`)로 누르기 → 룸 상세 1회 | `flutter analyze && flutter test test/push_*` · `grep -i firebase procedure/app/pubspec.lock` 0 · `xcrun simctl push <시뮬레이터> <번들 id> <payload.apns>` | 완료 — test 54 · **알림 [수락]**(CALL · 네이티브 백그라운드 요청 · 결과 로컬 알림) · 실 back 200 · 실 APNs. 워치 실기기는 열림(OQ-616) |
| WP6 | **리뷰** — WP1 ~ WP5 · WP11 · WP12 를 SPEC-004 대조(§3.4 행렬 · 수락 규칙 · WS 인증 · 푸시 받는 사람 · 내용(고객 이름 없음) · 410 삭제 · 앱이 규칙을 다시 계산하지 않는가(§6.0) · 시안 차이 §6.7 · 비밀값 · public 값) | SPEC-004 전부 | reviewer | read-only | FAIL / WARN 목록 · 처분은 코디가 사용자와 | — | **하지 않음** — SPEC-004 범위 리뷰 없이 사용자 E2E 로 갔다(리뷰 r1 · r2 는 SPEC-003 WP1 ~ 5 만) |
| WP7 | **수정** — WP6 처분 반영 | WP6 처분 | backend · frontend · mobile | 처분이 정한 경로 | 처분 항목마다 해당 시험 통과 | 처분이 정한 부분 시험 | 완료(사용자 피드백 수정으로 대신) — 앱 A1 ~ A7(`e2e-app-feedback-batch-1.md`) · 실기기 T1 ~ T8(`e2e-device-feedback-batch-1.md`) · 정상 로그인 — main 329b543 |
| WP8 | **로컬 E2E** — compose back + 웹 + 시뮬레이터 앱 2개 · SPEC-004 §8.3 1 ~ 11 · 코디가 먼저 한 번 → 사용자. **전체 검증은 여기서 한 번** | SPEC-004 §8.3 | 코디(진행) · 수정은 해당 워커 | `procedure/**` | 사용자 로컬 E2E 통과 · 피드백은 모아서 한 번에 수정 발주 | `cd procedure/back && uv run pytest -q` · `cd procedure/front && npm run build` · `cd procedure/app && flutter analyze && flutter test` · `docker compose up --build` | 완료 — 사용자 로컬 앱 E2E batch 1(시뮬레이터 · A1 ~ A7 처리) |
| WP9 | **TestFlight · 실기기 E2E** — 맥 쪽(방화벽 8700 · 잠자기 막기 · 맥 IP 고정) · README TestFlight 절차대로 사용자 맥에서 `flutter build ipa`(`API_BASE` = 맥 IP) → 업로드 → 내부 테스터 → 아이폰 · 아이패드 설치 → SPEC-004 §8.4 D1 ~ D6(D6 = 원장 호출 푸시 — 맥 back 에 `APNS_*` · `APNS_ENV=production` · SPEC-004 OQ-613 사용자 키 준비가 먼저) | SPEC-004 §2.2 · §2.4 · §5-1 · §8.4 | 사용자(서명 · 업로드 · 기기) · mobile(빌드 준비 · README) · 코디(진행) | `procedure/app/README.md` · `ios/` 설정 | §8.4 표 전부 — **마이크 · 통역 재생 · 수락 403 각 1회 이상 · 아이폰 · 아이패드 각각** · **푸시 D6(아이폰 · 전체 · 지정 · 로그아웃 뒤 안 옴)** | 사용자 기기 확인(표에 결과 기록) | **진행 중** — TestFlight 빌드 1 ~ 2(배포 주소 · A-20) 아이폰 · 아이패드 설치 · 화면 피드백 T1 ~ T8 반영. 빌드 3(정상 로그인 반영) **업로드됨**(코드 PR #5). 남음: 빌드 3 기기 확인(OQ-618) · D3 통역 실음성(OQ-617) · D6 푸시 · D7 알림 [수락] 워치(OQ-616) 결과 기록 |
| WP10 | **최종 배포**(맨 뒤 · 별도) — `cc/` → `_archive/cc/` · Actions 이미지 `procedure-back` · `procedure-front`(`cc-*-image.yml` 대체) · Dockerfile 포트/이름 · infra 차트(`charts/cc-prototype`)를 procedure 로 · 기존 주소 `ccc.medisolveai.xyz` 교체 · **SSE · 통역 WS 가 ingress(cloudflared · nginx)에서 버퍼링 안 되고 유휴로 안 끊김**(`/api/board/stream` 버퍼링 off · 읽기 시간 늘림 · `/api/interpret` WebSocket 업그레이드 · `wss`) · k8s Secret(`SONIOX_API_KEY` · KOS 키 · 시스템 계정 · `CCC_*` 계정 · 세션 키 · **`APNS_*` + `.p8` 파일(Secret 을 파일로 마운트)** — 값은 Secret 에만 · 레포엔 `.env.example` 이름만) · 배포 뒤 앱 서버 주소를 https 로 바꿔 축약 확인. **들어가기 전에 SPEC-004 OQ-601(로그인 접근 제한) 사용자 결정** | SPEC-004 A-12 · §8.5 · SPEC-003 D-03 | infra · backend · frontend(이미지) · 코디 | `.github/workflows/**` · `procedure/*/Dockerfile` · `_archive/cc/` · infra 레포 `charts/cc-prototype` · `argocd/applications/cc-prototype*.yaml` · `provisioning/secrets/cc-prototype*.env.example` | Actions 빌드 성공 · 배포 주소에서 SPEC-004 §8.5 전부(웹 로그인 · SSE · 의국 수락 / 앱 https 로그인 · SSE · **wss 통역 실발화** · 403 1회 · **푸시 1회** · 유휴 2분 안 끊김) · 레포 · 차트에 비밀값 0 | Actions 로그 · `curl -N https://ccc.medisolveai.xyz/api/board/stream?token=…` 첫 바이트 즉시 · 기기 확인 | 완료(2026-10-21 · **기기 E2E 앞으로 당김** — A-20) — 아래 「배포 기록」 |

## 병렬

```text
WP1(back 계정 · 권한) ──┬─ WP3(웹 로그인)
                        ├─ WP11(back 푸시) ─────────────┐
WP2(back 통역) ─────────┼──────────────┐                │
                        │              │                │
WP4(앱 뼈대 · 화면) ────┴──── WP5(앱 통역) ── WP12(앱 푸시) ── WP6 리뷰 ── WP7 수정 ── WP8 로컬 E2E ── WP9 TestFlight · 기기 E2E ── WP10 배포(마지막)
```

- back 순서(한 워커): WP1 → WP2 → WP11. mobile 순서: WP4 → WP5 → WP12 (0.2.0)
- WP1 · WP2 는 같은 back 이라 한 워커가 차례로(WP1 먼저 — 로그인 모양을 고정해야 WP3 · WP4 가 붙는다). WP4 는 WP1 을 기다리는 동안 `PROC_FAKE_BOARD`(조작은 403)로 화면부터
- 로그인 응답 · 토큰 · 스냅샷 모양을 바꿔야 하면 SPEC-004(§3 · §7)를 먼저 고친다(코디 → planner) → 양쪽 다시 맞춤
- mobile 워커는 새 워커다 — `orchestration/config/projects/cc-prototype.json` · `orchestration/roles/cc-prototype/mobile/` 준비는 코디(발주 전)

## 주의

- public 레포(코드 · 문서 모두) — KOS 키 · Soniox 키 · 토큰 · 비밀번호 · 계정 이메일 · 실명 · KOS id 값 · **맥 IP · Apple 팀 id · 번들 서명 값**을 코드 · 시험 데이터 · 커밋에 넣지 않는다. 시험의 KOS · Soniox 응답은 모양만 맞춘 가짜 값
- APNs `.p8` 키 · Key ID · 팀 id · 번들 id 는 레포 밖(로컬 파일 · env / 배포 Secret). 키 준비는 사용자(SPEC-004 OQ-613) — 없으면 WP11 · WP12 는 가짜 APNs · 시뮬레이터까지만 하고 D6 은 키가 생긴 뒤 (0.2.0)
- PoC 의사 계정 = KOS 데모 지점 **실제 원장**(시스템 계정 X) — 값은 env 에만(SPEC-004 §2.3)
- 운영 명동점 키 금지(D-06). 실 쓰기는 데모 지점 · 데모 일정에만
- 워커는 사용자 포트(3600 · 8600 · 3700 · 8700)에 떠 있는 사용자 프로세스를 죽이지 않는다 · 사용자 기기 · 시뮬레이터 세션을 건드리지 않는다
- 백엔드 커밋 뒤 compose 를 다시 올리고 E2E(옛 코드가 떠 있는 채로 확인 금지)
- 앱 완료 = 사용자가 **기기에서** 본 것(WP9). 배포(WP10)는 그 뒤에만

## 배포 기록 (WP10 · 2026-10-21)

| 무엇 | 사실 | 근거 |
|---|---|---|
| TestFlight | 빌드 1(1.0.0 · 10-21 업로드 · 배포 주소) · 빌드 2(실기기 피드백 T1 ~ T8 을 받은 빌드) · 빌드 3(`1.0.0+3` · 정상 로그인 · T1 ~ T8 반영 · 업로드됨 — 코드 PR #5) | `_RESUME` 10-21 · `e2e-device-feedback-batch-1.md` · PR #5 |
| 코드 | `kknaksss/cc-prototype` #3 머지(`0f4634a`) → #4(`329b543` — 정상 로그인 · T1 ~ T8) → #5(OPEN — 데모 환자 스킬 · 빌드 3 번호) · `cc/` → `_archive/cc/` · Actions `procedure-back-image.yml` · `procedure-front-image.yml`(main push · arm64 · GHCR · 태그 = 커밋 sha) | 코드 main · `_RESUME` 10-21 |
| infra #22 | `ccc.medisolveai.xyz` 를 procedure 로 교체 — 이미지 `procedure-{back,front}:0f4634a` · back 8700 · PVC `procedure-db` · Ingress `/api` → back(SSE `/api/board/stream` · WS `/api/interpret` · 버퍼링 끔 · timeout 3600s) · `/` → front · Secret `cc-prototype-secret` · `cc-prototype-apns`(값은 클러스터에만) · `APNS_ENV=production` | `MediSolveAIDev/k8s_infra_mac#22` |
| infra #23 | back CrashLoop 수정 — APNs Secret 을 `/run/secrets` 로 통째 ro 마운트해 서비스계정 토큰 마운트가 막힘 → **`/etc/apns`**(`APNS_KEY_PATH=/etc/apns/apns.p8`) · `automountServiceAccountToken: false` | `#23` |
| infra #24 | 이미지 태그 → `329b543` · Secret 예시에 `CCC_DOCTOR_PASSWORD` · `CCC_NURSE_PASSWORD` 이름 | `#24` |
| 동기화 | ArgoCD **수동** sync(`cc-prototype-prod`) — Synced · Healthy | `_RESUME` 10-21 배포 완료 줄 · #23 본문 |
| 확인 | SPEC-004 §8.5 코디 확인 기록(카드 · SSE 10초 · 통역 wss 토큰 403 · APNs JWT production) | SPEC-004 §8.5 |
| 남은 정리 | **옛 `cc-db` PVC · scenario/staff Secret 은 keep**(#22) — 지울지 정하지 않음 | `#22` 본문 |

## 열린 것 (2026-10-22)

| 무엇 | 지금 | 근거 |
|---|---|---|
| 실기기 Apple Watch 알림 [수락] | 기록 없음 | SPEC-004 OQ-616 · §8.4 D7 |
| 통역 실음성(기기 마이크 · 스피커) | 기록 없음 | SPEC-004 OQ-617 · §8.4 D3 |
| 빌드 3 기기 확인 · `pubspec` `+3` main 반영 | 업로드됨 · 코드 PR #5 OPEN | SPEC-004 OQ-618 |
| 옛 `cc-db` PVC · scenario/staff Secret 정리 | keep | infra #22 |
| 웹 로그인 역할 제한 | 결정 필요 | SPEC-003 OQ-518 |
| SPEC-004 범위 코드 리뷰(WP6) | 하지 않음 — 할지 결정 | 이 문서 WP6 |
| `.env.example` 에 `PROC_SESSION_HOURS` · `PROC_BCRYPT_ROUNDS` 없음 | 코드 기본값으로 돈다 | SPEC-003 §2.3 |
