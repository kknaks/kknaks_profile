---
type: spec
id: SPEC-004
title: "명동 PoC v2 — 시술실 앱(Flutter · iOS) · 계정 · 권한 · 통역 · 원장 호출 푸시 계약"
version: 0.3.0
status: draft
product: cc-prototype
feature: procedure
created_at: 2026-10-21
updated_at: 2026-10-22
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/spec
  - status/draft
links:
  baselines:
    - "[[baseline-008-procedure-board|BASE-008]]"
  decisions:
    - "[[decision-005-procedure-board|DEC-005]]"
  specs:
    - "[[spec-003-procedure-board|SPEC-003]]"
    - "[[spec-001-cc-poc|SPEC-001]]"
  works:
    - "[[work-004-procedure-app|WORK-004]]"
  releases: []
  related: []
sources:
  - orchestration/work/myeongdong-poc-v2/_RESUME.md §2 (2026-10-21 「디자인 2단계」 이후 줄)
  - orchestration/work/myeongdong-poc-v2/design-mobile-read-report.md §2 · §5 · §7 · §9 · §9-1 · §9-2
  - orchestration/work/myeongdong-poc-v2/e2e-feedback-batch-1.md
  - orchestration/work/myeongdong-poc-v2/design-mobile/ (간호사 모바일 · 시술실 태블릿 시안)
  - cc-prototype procedure/back (구현 코드 — 로직 정본)
  - cc-prototype origin/main cc/back/app/service/interpret/ (통역 원천)
  - orchestration/work/myeongdong-poc-v2/_RESUME.md §2 2026-10-21 「원장 호출 푸시」 줄 · 코디 지시(0.2.0)
  - orchestration/work/myeongdong-poc-v2/e2e-app-feedback-batch-1.md(A1 ~ A7) · e2e-device-feedback-batch-1.md(T1 ~ T8) (0.3.0)
  - kknaksss/cc-prototype main 329b543(procedure/back · procedure/app · procedure/front) · infra PR #22 ~ #24 (0.3.0)
---

# 명동 PoC v2 — 시술실 앱 계약

> 0.3.0(2026-10-22): **머지 전 코드 동기화** — **정상 로그인**(A-16 · OQ-601 닫힘 — 아이디 + 비밀번호 · bcrypt · 계정 목록 API 제거 · 5회/1분 잠금) ·
> **알림 [수락]**(A-17 · `CALL` 카테고리) · **`push_log` · `X-Accept-Source`**(A-18) · 죽은 기기 토큰 삭제 · Apple 준비(A-19) · **배포 먼저 · 앱 = 배포 주소 고정**(A-20 — A-11 · A-12 를 고침) ·
> 앱 피드백 A1 ~ A7 · 실기기 T1 ~ T8 · iOS 15 · 배포 완료(infra #22 ~ #24). §0 · §1 · §2.2 ~ §2.4 · §3 · §5-1 · §6(화면 정본 칸) · §7.3 · §8 · §9 · 부록 A · 부록 B(새). 출처 줄 전수 대응표는 SPEC-003 부록 D. 바뀐 줄 끝에 `(0.3.0)`.
> 0.2.0(2026-10-21): **관리자도 호출 푸시를 받는다 · 앱 카드에 관리자 · 관리자는 앱에서도 원장을 골라 수락**(A-15) / **원장 호출 푸시**(A-14 — D-34 「원장 호출 휴대폰 알림 = 다음」을 뒤집음) — §5-1 새 절 · §1 · §2.3 · §2.4 · §6.1 · §7.3 · §8 · §9 OQ-613 · 부록 A. 바뀐 줄 끝에 `(0.2.0)`.

> `procedure/app`(Flutter · iOS) 과 `procedure/back` 의 **추가분**(계정 · 권한 · 통역)이 지킬 계약.
> 현황판 규칙 · 스냅샷 · 조작 API · SSE · KOS 연동은 **SPEC-003 그대로**이고, 이 문서는 그 위에 얹는 것만 적는다.
>
> SSOT 순서(이기는 순): ① 결정(아래 A-nn) ② 로직 = SPEC-003 + **구현 코드 `procedure/back`**(스냅샷 · 조작 API · SSE 의 실제 모양)
> + E2E 결정(`e2e-feedback-batch-1.md`) ③ 화면 모양 = 시안 `Ceramique 간호사 모바일.dc.html` · `Ceramique 시술실 태블릿.dc.html`
> (읽기 리포트 `design-mobile-read-report.md` — 이하 「리포트」) ④ 통역 = 이전 PoC `cc/back`(`origin/main`).
>
> 이 레포는 public — 키 · 토큰 · 비밀번호 · 실명 · 연락처 · 계정 이메일 · KOS id 값 · **Apple 팀 id · 서명 값**을 쓰지 않는다. env 는 이름만.

## 0. 근거 표기

| 표기 | 무엇 | 원천 |
|---|---|---|
| A-01 | 디자인 2단계 = Flutter PoC 앱 · 서버 = `procedure/back` 그대로 | `_RESUME` 10-21 · 리포트 §9 U1 |
| A-02 | 앱 로직 정본 = 구현 코드(back 스냅샷 값). 시안은 화면 모양만 — 시안 로직 X6 · X7 · M3 · M5 · M8 · M10 · M11 버림 | `_RESUME` 10-21 · U2 |
| A-03 | 계정 = 어드민 · 의사 · 간호사. PoC 로그인 카드 = 어드민 + 의사 1 + 간호사 1. DB 에는 사람마다 계정(원장 = KOS 원장 연결 · 간호사도 한 명씩) | `_RESUME` 10-21 · U3 |
| A-04 | 통역 = 이전 PoC `cc/back` `WS /api/interpret` · Soniox 로직 · 언어(zh 번체 포함 · en · ja · th · fr · es · tl · hi) → `procedure/back` 으로 복사(D-01) | `_RESUME` 10-21 · U4 |
| A-05 | 빠른 말하기 = 시안 문구 6개 하드코딩(위 언어 번역). 병원별 설정은 나중 | `_RESUME` 10-21 · U5 |
| A-06 | 앱 PoC 에서 뺌: 동의서 · 시술 메모 · [다시 알림] · 간호사 요청 · 빈 방/입실 예정 | `_RESUME` 10-21(코디 기본값) |
| A-07 | 의사 계정 [수락] = 자기 자신으로 수락(원장 고르기 없음) | `_RESUME` 10-21 · 리포트 §9 정정 |
| A-08 | 권한은 back 이 조작 API 마다 검사. 토큰에 역할 + 연결 원장 id. 수락: 의사 = 로그인 원장(다르면 403) · 지정 호출은 지정 원장만 · 간호사 403 · 어드민은 원장 골라 수락. 그 밖 조작 = 세 역할 모두(기본값). `actor` = 로그인 계정. PoC 의사 = KOS 데모 실제 원장. 역할별 허용 · 403 단위 시험 | `_RESUME` 10-21 · 리포트 §9-1 |
| A-09 | 앱 E2E = 로컬 + 아이폰 + 아이패드(iOS 만) · 사용자 맥북 로컬 빌드 → TestFlight · 기기는 초대 설치 | `_RESUME` 10-21 · 리포트 §9-2 |
| A-10 | 앱 코드 = `procedure/app/`(Flutter) | `_RESUME` 10-21(코디 기본값 앞 절반) |
| A-11 | ~~**기기가 닿는 back = 같은 공유기 Wi-Fi 의 맥 IP**(http :8700 · 통역 ws). ATS 로컬 네트워크 허용 · 로컬 네트워크 권한 문구 · back `0.0.0.0` · 맥 방화벽 8700 · 맥 IP 고정 또는 앱 안 서버 주소 입력칸. `_RESUME` 10-21 「기기 back = 배포 주소 · 기기 E2E 전에 WP7」은 **취소**~~ → **A-20 이 뒤집음**(배포 먼저 · 앱은 배포 주소). 로컬 맥 IP 는 debug 빌드 확인용으로만 남는다 (0.3.0) | 리포트 §9-2 사용자 결정 · 코디 정정(2026-10-21) · A-20 |
| A-12 | ~~앱 E2E 가 끝나면 **최종으로**~~ → **먼저**(A-20) back · front 를 `ccc.medisolveai.xyz` 에 배포 — **2026-10-21 완료**(infra #22 ~ #24) (0.3.0). ~~앱 서버 주소 기본값 = 맥 IP → 배포 뒤 https 주소로 바꿔 씀~~(→ A-20 · release 는 배포 주소 고정). 완료 조건: 통역 wss · SSE 가 ingress(cloudflared · nginx)에서 버퍼링 안 되고 유휴로 안 끊김 · `SONIOX_API_KEY` · KOS 키 · 시스템 계정 · ccc 계정 값은 k8s Secret 에만 · `cc/` → `_archive/cc` · Actions 이미지 `procedure-*` | 코디 추가 결정(2026-10-21 · 리포트 §9-2) |
| A-14 | **원장 호출 푸시를 이번 앱 PoC 에 넣는다**(D-34 뒤집음). iOS **APNs 직접**(Firebase 없음 · .p8 인증 키) · 지정 호출 = 그 원장 · 전체 호출 = 기기 토큰 등록한 의사 계정 전원 · 누르면 그 방 룸 상세 · 로그인 때 기기 토큰 등록 · 키 · 팀 id 는 레포 밖. 세부(env 이름 · `POST /api/devices` · 내용 · 실패 · 시험) = 코디 지시 0.2.0 | `_RESUME` 10-21 「원장 호출 푸시」 · 사용자 「푸시 알림 필요한데」 · 코디 지시 (0.2.0) |
| A-15 | **관리자도 호출 푸시를 받는다** — 앱 로그인 카드 = 관리자 · 의사 · 간호사. 관리자 계정으로 앱에 로그인해 기기 토큰을 등록하면 **모든 호출(전체 · 지정)** 푸시. 관리자는 앱에서도 수락할 때 원장을 고른다(웹 의국과 같음) | 사용자(코디 전달 2026-10-21) (0.2.0) |
| A-13 | (사실) 관리자 권한 시스템 계정으로 **다른 원장 계정 id 로 수락을 대신 넣기 됨**(KOS 200) — 의국 · 앱 어디서 수락해도 KOS 쪽은 같은 요청 | `_RESUME` 10-21 (사실) |
| A-16 | **OQ-601 닫음 — 정상 로그인(웹 · 앱 둘 다)**: 아이디 + 비밀번호 · 계정 카드 목록 API(`GET /api/auth/accounts`) 공개 제거 · 비밀번호는 해시로 DB(서버 시작 때 env/Secret 값으로 어드민 · PoC 의사 · 간호사 — 그 밖 원장 doctor 행은 비밀번호 없으면 로그인 불가) · 실패 반복 잠금(5회 · 1분) · 토큰은 키체인 (0.3.0) | `_RESUME` 10-21 「OQ-601 닫음」 줄 · 사용자 「이제 로그인 정보 막자 · 정상 로그인으로 · 웹 앱 다」 |
| A-17 | **알림에서 바로 [수락]**(Apple Watch 포함 — iPhone 알림 액션이 워치에 그대로 · 워치 앱 없음). 의사 수신자 알림에만 카테고리 `CALL` + 액션 「수락」 → 앱이 백그라운드에서 `POST /api/calls/{callId}/accept`(doctorId 없음). 관리자 알림은 액션 없음. 결과는 로컬 알림 한 줄 · 실패면 누르면 룸 상세 · 토큰은 키체인 (0.3.0) | `_RESUME` 10-21 「알림에서 바로 [수락]」 줄 · 사용자 「와치에도 · 수락 버튼까지 넣자」 |
| A-18 | **알림 내역을 DB 에** — `push_log`(호출 · 받는 사람 · 기기 토큰 끝 6자리 · 카테고리 · 상태 · APNs 결과 · 시각). 수락 출처(push · app · web) = `X-Accept-Source` 헤더 → `call_accept` 이벤트. 조회 API 는 나중 (0.3.0) | `_RESUME` 10-21 「알림 내역을 DB 에」 줄 · 사용자 「알림 내역도 DB 에 쌓을 거지?」 |
| A-19 | Apple 준비 — 번들 id 등록(개인 팀 · Explicit · Push) · App Store Connect 앱 레코드 · 사용자 액세스 = 전체 · APNs 키(Sandbox & Production · Team Scoped). 번들 id · 팀 id 값은 레포에 쓰지 않는다(`.env` · `Signing.xcconfig` 만) · `.p8` 은 레포 밖 (0.3.0) | `_RESUME` 10-21 Apple 두 줄 · 사용자 |
| A-20 | **배포 먼저** — 앱은 배포 주소(`https://ccc.medisolveai.xyz`)로 TestFlight. 로그인 접근 제한은 배포 뒤(→ A-16 으로 닫음). 앱 서버 주소 칸 · [연결 확인]은 **debug 빌드에서만** · release 는 `API_BASE` 고정 · 저장된 옛 주소 무시 (0.3.0) | `_RESUME` 10-21 「배포 먼저」 줄 · T8 |

그 밖: `D-nn` = DEC-005 · `SPEC-003 §n` · `E2E-n` = `e2e-feedback-batch-1.md` · `X/M/N/C-n` = 리포트 표 번호 · `기본값` = 결정에 없어
이 문서가 고른 구현값(§9 에 같이 올림) · `코드` = `procedure/back` 현재 구현 · `A1 ~ A7` = `e2e-app-feedback-batch-1.md` · `T1 ~ T8` = `e2e-device-feedback-batch-1.md` (0.3.0).

## 1. 범위

### 1.1 In

| 무엇 | 근거 |
|---|---|
| `procedure/app/` Flutter 앱 **iOS 만**(아이폰 · 아이패드) — 한 앱 · 화면 폭으로 모바일 / 태블릿 배치 | A-01 · A-09 · A-10 |
| 앱 화면: 로그인(아이디 + 비밀번호) · 시술실 현황(목록) · 룸 상세 · 의사 호출 시트 · 통역 바 · 통역 드로어 · 빠른 말하기 (0.3.0) | A-01 · A-16 · 리포트 §2 |
| 앱 조작 = 웹과 같은 조작 API(SPEC-003 §7.3) — 마취 시작/종료 · 의사 호출 · 다른 의사 호출 · [다른 원장에게] · 수락 · [시작] · [종료] · [귀가 대기] | A-02 · A-08 |
| back: **ccc 계정 체계**(어드민 · 의사 · 간호사) · **비밀번호 로그인(bcrypt · 잠금)** · 토큰에 역할 + 원장 id · **조작 API 마다 역할 검사** · `actor` = 로그인 계정 (0.3.0) | A-03 · A-07 · A-08 · A-16 |
| back: **통역** `WS /api/interpret` 복사 + **토큰 인증** | A-04 · 리포트 §9 ② |
| 웹 front 로그인 · 의국 화면을 새 계정 체계(어드민)로 | A-03 · A-08 |
| 로컬 E2E(맥 · 시뮬레이터) → ~~TestFlight → 아이폰 · 아이패드 실기기 E2E(맥 IP)~~ → **배포 → TestFlight(배포 주소) → 아이폰 · 아이패드 실기기 E2E** (0.3.0) | A-09 · A-20 |
| ~~마지막:~~ back · front 를 `ccc.medisolveai.xyz` 에 배포 — 2026-10-21 완료 (0.3.0) | A-12 · A-20 |
| **원장 호출 푸시**(APNs 직접) — 앱 기기 토큰 등록 · back 이 호출 생성 때 받을 원장에게 발송 · 누르면 그 방 룸 상세(§5-1) (0.2.0) · **알림에서 바로 [수락]**(워치 포함) · 발송 내역 `push_log` (0.3.0) | A-14 · A-17 · A-18 |

### 1.2 Out (뺀 것)

| 무엇 | 근거 |
|---|---|
| 동의서 서명 · [시작] 동의서 조건(X8 · N8) | A-06 |
| 시술 메모 쓰기 · 시술 줄 메모(X11 · N6 · N7) | A-06 · D-34 |
| [다시 알림](X9 · N3) | A-06 |
| 간호사 요청 시트(태블릿 · N15) | A-06 |
| 빈 방 카드 · 「입실 예정」(X3 · N12) | A-06 |
| 시안 로직 — 마취는 시술 시작 전에만(X6 · M8) · 동시 진행 막기(X7 · M5) · 방 단위 한 번에 수락(M3) · 「담당의 미정」 확인 필요(M10) · 필터 상태 하나씩(M11) | A-02 |
| 주의 상자 · 나이 · 성별 · 출국 시각 meta(N9 · N10) — 저장 안 함 | D-14 · 기본값(데이터 없음) |
| 마취 종류(크림 · 국소 · 수면 · N11) — 「마취 중」만 | A-02 · 기본값(데이터 없음) |
| 「누가 호출했나」 표시(N5 · X18) — 로그 `actor` 에만 남김 | 기본값(결정 없음) |
| [못 감] · 다음 동선 예측 · 준비물 · 보조 요청함 · 평면도 · 배정 이동 · 기록지 출력 · 스케줄(캔버스 TURN 1 · 2 나머지) | D-34 · A-06 · 리포트 Q-M15 — 원장 호출 푸시는 In(A-14 · 0.2.0) |
| Android · 웹 앱 빌드 | A-09 |
| 빠른 말하기 병원별 설정 · 문구 편집 | A-05 |
| 통역 대화 저장(서버 · 기기) | 이전 PoC 와 같음(A-04) · 시안 M16 |
| 되돌리기 | D-28 |
| 간호사 계정 전원 목록의 원천(KOS 역할 태그) — PoC 는 간호사 1명 | §9 OQ-603 |

## 2. 폴더 · 실행

### 2.1 폴더 (코드 레포 `kknaksss/cc-prototype`)

```text
procedure/
  app/                         # Flutter · iOS 만 (A-10)
    pubspec.yaml · analysis_options.yaml · README.md
    lib/
      main.dart
      config/        # 서버 주소 — release = dart-define API_BASE 고정 · debug 만 입력칸 · 저장 (0.3.0)
      api/           # REST(SPEC-003 §7 · 이 문서 §3.3) · 오류 {error:{code,message}}
      sse/           # SSE 클라이언트(§7.1)
      interpret/     # 통역 WS · 마이크 PCM16 · 24kHz 재생 · 빠른 말하기 TTS(§4 · §5)
      model/         # 스냅샷 모델 — 코드 schemas/board.py 와 같은 필드
      view/          # 표시 문구 · 순서(웹 view.ts 와 같은 매핑 · §6.1)
      push/          # 기기 토큰 등록 · 알림 누름 → 룸 상세 (0.3.0)
      screens/       # login · list(board) · room (모바일 / 태블릿 배치)
      widgets/       # 호출 시트 · 통역 바 · 드로어 · Badge · 버튼
      theme/         # Ceramique 토큰을 Dart 로(§6.6)
    ios/                       # Runner · Info.plist · AppDelegate.swift(푸시 · 알림 [수락]) · Signing.xcconfig(gitignore)(§2.4) (0.3.0)
    test/
  back/                        # 기존 + 계정 · 권한 · 통역(§3 · §4)
  front/                       # 기존 + 로그인 계정 체계(§3.6)
```

- 기능끼리 import 금지(D-02) — 앱은 back 을 HTTP · WS 로만 안다
- 계층 규약(router → service → repository · 도메인 예외)은 back 추가분도 같다(SPEC-003 §2.1)

### 2.2 로컬 실행

| 무엇 | 값 | 근거 |
|---|---|---|
| back | `cd procedure && docker compose up --build`(compose 는 이미 `8700:8700` 을 모든 인터페이스에 연다 · 컨테이너 uvicorn `--host 0.0.0.0` — 코드 Dockerfile) / 개별 실행은 `uv run uvicorn app.main:create_app --factory --host 0.0.0.0 --port 8700` | A-11 · 코드 |
| 맥 쪽 | macOS 방화벽에서 8700 들어오기 허용(docker · python) · E2E 동안 잠자기 막기(`caffeinate -dimsu` 등) · 공유기에서 맥 IP 고정(DHCP 예약) 권장 | A-11 |
| 앱 — 시뮬레이터 | `cd procedure/app && flutter run -d <iOS 시뮬레이터> --dart-define=API_BASE=http://localhost:8700` | 기본값 |
| 앱 — 실기기(개발) | `flutter run -d <기기> --dart-define=API_BASE=http://<맥 IP>:8700` | A-11 |
| 앱 서버 주소 | 빌드 값 = `API_BASE`(dart-define · 코드 기본 `http://localhost:8700`). **release(TestFlight) = `API_BASE` 고정** — 입력칸 · [연결 확인] 없음 · 기기에 저장된 옛 주소는 무시. **debug 빌드만** 로그인 화면 「서버 주소」 입력칸으로 바꾸고 저장(로컬 확인용). 통역 주소는 이것에서 만든다: `http → ws` · `https → wss` + `/api/interpret` (0.3.0) | A-20 · T8 · 코드 `lib/config/server.dart` |
| 배포 뒤 | TestFlight 빌드를 `--dart-define=API_BASE=https://ccc.medisolveai.xyz` 로 만든다 ~~입력칸에 https 로 바꿔 쓴다~~ (0.3.0) | A-20 |

- 코드의 `API_BASE` 기본값은 배포 주소로 두지 않는다(SPEC-003 §2.2 W14 와 같은 기준). ~~TestFlight 빌드의 기본값 = 맥 IP~~ → TestFlight 는 빌드 명령 인자로 배포 주소 (0.3.0) — A-20
- 맥 IP 값은 레포에 쓰지 않는다(빌드 명령 인자 · 입력칸에만)

### 2.3 env 추가 (`procedure/.env.example` — 이름만)

| 이름 | 뜻 | 근거 |
|---|---|---|
| `SONIOX_API_KEY` | 통역(Soniox STT · TTS) 키 | A-04 · 이전 PoC 와 같은 이름 |
| `CCC_ADMIN_ID` · `CCC_ADMIN_PASSWORD` | 어드민 로그인 아이디 · 비밀번호(기존 · SPEC-003 §2.3) (0.3.0) | A-03 · A-16 |
| `CCC_DOCTOR_ID` · `CCC_DOCTOR_PASSWORD` | PoC 의사 로그인 아이디 · 비밀번호 (0.3.0) | A-03 · A-16 |
| `CCC_DOCTOR_KOS_ACCOUNT_ID` | 그 의사 계정을 연결할 **KOS 데모 지점 실제 원장**의 계정 id(`getAccounts` id). 시스템 계정 id 는 안 됨(원장 목록에서 빠지므로) | A-08 · D-11 |
| `CCC_NURSE_ID` · `CCC_NURSE_PASSWORD` · `CCC_NURSE_NAME` | PoC 간호사 로그인 아이디 · 비밀번호 · 표시 이름 (0.3.0) | A-03 · A-16 |
| `PROC_SESSION_HOURS` · `PROC_BCRYPT_ROUNDS` | 토큰 만료(기본 12시간) · 해시 비용(기본 12) — `.env.example` 에 없음(코드 기본값) (0.3.0) | 코드 `config.py` |
| `APNS_KEY_PATH` | APNs 인증 키 `.p8` 파일 경로(파일은 레포 밖 · 배포는 Secret 을 파일로 마운트 — **`/etc/apns/apns.p8`**, infra #23) (0.2.0 · 0.3.0) | A-14 · infra #23 |
| `APNS_KEY_HOST_PATH` | compose 전용 — 호스트의 `.p8` 경로(레포 밖). compose 가 컨테이너 `/run/secrets/apns.p8` 로 읽기 전용 마운트 (0.3.0) | 코드 `.env.example` |
| `APNS_KEY_ID` · `APNS_TEAM_ID` | 그 키의 Key ID · Apple 팀 id(JWT `kid` · `iss`) (0.2.0) | A-14 |
| `APNS_BUNDLE_ID` | 앱 번들 id(`apns-topic`) (0.2.0) | A-14 |
| `APNS_ENV` | `sandbox` \| `production`(코드 기본 `production`) — **TestFlight = `production`** · Xcode 에서 기기로 직접 실행(debug)한 앱 = `sandbox` (0.2.0 · 0.3.0) | A-14 · 코드 `config.py` |
| `PROC_INTERPRET_ORIGIN` | (선택) 브라우저에서 WS 를 열 때 허용 출처 — 비우면 `PROC_FRONT_ORIGIN` | 기본값(§4.2) |

- ~~`CCC_ADMIN_PASSWORD` 등 비밀번호 칸은 로그인 방식이 바뀔 때(§9 OQ-601) 쓴다~~ → 비밀번호 3개는 **서버 시작 · 계정 동기화 때 bcrypt 해시로 `account.password_hash`**(값이 지금 해시와 맞으면 다시 만들지 않음). 비면 그 계정은 로그인 불가 (0.3.0) — A-16 · 코드 `service/accounts.py` `_passwords`
- 값 원천 = 사용자(ax-clinic-project · KOS 데모 화면). 배포는 k8s Secret 에만(A-12) — `cc-prototype-secret`(env) · `cc-prototype-apns`(`.p8` 파일) · 레포에는 이름만(infra Secret 예시에 `CCC_DOCTOR_PASSWORD` · `CCC_NURSE_PASSWORD` 이름 추가 — infra #24) (0.3.0)

### 2.4 iOS 설정 · TestFlight

| 항목 | 값 | 근거 |
|---|---|---|
| 플랫폼 | iOS 만 · 아이폰 + 아이패드(Universal) · 세로/가로는 기본값(폰 세로 · 패드 가로 우선, 둘 다 허용) | A-09 · 시안(폰 390 × 844 · 태블릿 가로) |
| 최소 iOS | **15.0**(`Podfile` · Runner `IPHONEOS_DEPLOYMENT_TARGET`) (0.3.0) | 코드 `ios/` · 커밋 329b543 「iOS 15 타깃」 |
| 번들 id | 사용자가 정해 등록함(A-19). 레포엔 자리만 — `PRODUCT_BUNDLE_IDENTIFIER = $(APP_BUNDLE_ID)` · 값은 `ios/Flutter/Signing.xcconfig`(gitignore) · back 은 `APNS_BUNDLE_ID` (0.3.0) | A-19 · 코드 `project.pbxproj` |
| 앱 표시 이름 · 아이콘 | 「시술 현황」(`CFBundleDisplayName`) · 아이콘 = Ceramique 로고 「C」(바탕 ceramique primary · 1024 알파 없음 · AppIcon 15개) (0.3.0) | A7 · 코드 `Info.plist` · `assets/icon/` |
| 서명 | Xcode **Automatic signing** · 팀은 사용자 맥에서만 고른다. 팀 id 는 커밋하지 않는다 — `ios/Flutter/Signing.xcconfig`(gitignore · `DEVELOPMENT_TEAM`)를 Runner 설정이 include, 없으면 서명 없이 시뮬레이터 빌드 | 브리프(팀 id 금지) · 기본값 |
| `NSMicrophoneUsageDescription` | 「통역할 때 의료진과 고객의 말을 듣기 위해 마이크를 사용합니다.」 — 없으면 통역 불가 | 리포트 §9-2 ③ |
| `NSLocalNetworkUsageDescription` | 「같은 Wi-Fi 의 시술 현황 서버에 연결하기 위해 로컬 네트워크를 사용합니다.」 | A-11 |
| `NSAppTransportSecurity` | `NSAllowsLocalNetworking = true`(맥 IP http · ws). `NSAllowsArbitraryLoads` 는 켜지 않는다. ※ Dart `dart:io` 소켓은 ATS 대상이 아닐 수 있다 — 넣어 두고 실기기에서 http · ws 가 붙는지로 확인 | A-11 |
| Push Notifications | Xcode **Push Notifications capability** 켬(`aps-environment` entitlement — 개발 빌드 development · TestFlight/App Store 내보내기 때 production 으로 바뀜). App ID 에도 Push 켜짐(사용자 · 서명 자동이면 Xcode 가 함). **Firebase 의존 0** (0.2.0) | A-14 |
| 알림 카테고리 | 앱 시작 때 `UNNotificationCategory` **`CALL`** + 액션 **`ACCEPT`(「수락」)** 등록 — 알림 [수락](§5-1.3) (0.3.0) | A-17 · 코드 `AppDelegate.swift` |
| Background Modes | Remote notifications 는 켜지 않는다(보이는 알림만 · 조용한 푸시 없음) (0.2.0) | 기본값 |
| 오디오 백그라운드 | 넣지 않는다(통역은 앱이 앞에 있을 때만) | 기본값 |
| `ITSAppUsesNonExemptEncryption` | `false`(표준 https 만) — 업로드 때 수출 규정 질문을 건너뛴다 | 기본값 |

TestFlight 절차(사용자 맥북 · README 에 그대로):

1. App Store Connect 에서 앱 레코드 생성(번들 id · 이름) — 사용자
2. `cd procedure/app && flutter build ipa --release --dart-define=API_BASE=https://ccc.medisolveai.xyz --build-number=<+1>` ~~(`API_BASE` = 맥 IP)~~ (0.3.0 — A-20)
3. 만든 `.ipa` 를 Xcode Organizer 또는 Transporter 로 업로드 — 사용자 Apple 계정
4. App Store Connect → TestFlight → **내부 테스터**(App Store Connect 사용자 · 심사 없음)에 빌드 배정 → 아이폰 · 아이패드에서 TestFlight 앱으로 설치
5. 첫 실행: (로그인 직후) 알림 허용 · (통역 처음 열 때) 마이크 허용 → 아이디 · 비밀번호로 로그인. ~~로그인 화면 「서버 주소」 확인~~ — release 엔 서버 주소 칸이 없다 (0.3.0)

- 외부 테스터는 베타 심사가 걸리므로 쓰지 않는다 — 리포트 §9-2 ④ · 기본값
- 빌드 번호는 업로드마다 올린다(같은 번호 거절). 기록: 빌드 1(1.0.0 · 2026-10-21 업로드) · 빌드 2(실기기 피드백 T1 ~ T8 을 받은 빌드 — `e2e-device-feedback-batch-1.md` 「빌드 1 ~ 2」) · **빌드 3 = 업로드됨**(정상 로그인 · T1 ~ T8 반영분 — `pubspec.yaml` `1.0.0+3` 은 코드 PR #5(OPEN · 2026-10-22)에 · main 329b543 은 아직 `+1`) (0.3.0) — `_RESUME` 10-21 배포 완료 줄 · 코드 PR #5

## 3. 계정 · 권한 (back 변경)

### 3.1 계정 테이블 `account` (ccc 원천)

| 필드 | 뜻 |
|---|---|
| `id` | ccc PK(정수) |
| `login_id` | 로그인 아이디(문자열 · 유일) — 토큰 `sub` · `event_log.actor` 에 쓰는 값 |
| `role` | `admin` \| `doctor` \| `nurse` |
| `name` | 표시 이름(의사 = 연결된 `staff.name`) |
| `staff_id` | 연결 `staff.id`(의사만 · KOS 원장) · 나머지 null |
| `active` | 쓰는 계정인가 |
| `card` | PoC 계정인가(어드민 · 의사 1 · 간호사 — 비밀번호를 받는 계정). ~~로그인 카드에 보이나~~ — 카드 화면은 없어졌다 (0.3.0) |
| `password_hash` | bcrypt 해시 · **없으면 로그인 불가**(그 밖 원장 doctor 행 등) (0.3.0) |
| `created_at` · `updated_at` | |

만드는 법(기본값 — 「DB 에는 사람마다」 A-03):

| 역할 | 행 | PoC 계정(`card` · 비밀번호) (0.3.0) |
|---|---|---|
| admin | 서버 시작 때 `CCC_ADMIN_ID` 로 1행 upsert · 비밀번호 `CCC_ADMIN_PASSWORD` | ○ |
| doctor | **직원 조회(1시간 · 서버 시작)마다 원장 목록(SPEC-003 §4.6) 한 명당 1행** upsert(`staff_id` 연결 · `name` = staff 이름). `login_id` = `CCC_DOCTOR_ID` 가 가리키는 한 명은 그 값, 나머지는 back 이 만든 내부 값(로그인 카드 없음). 원장 목록에서 빠진 원장의 계정은 `active=false`(행은 남김) | `CCC_DOCTOR_KOS_ACCOUNT_ID` 원장 1명만 ○ · 비밀번호 `CCC_DOCTOR_PASSWORD` |
| nurse | 서버 시작 때 `CCC_NURSE_ID` · `CCC_NURSE_NAME` 으로 1행 upsert · 비밀번호 `CCC_NURSE_PASSWORD`. 간호사 전원 목록의 원천은 §9 OQ-603 | ○ |

- env 값이 비면 그 계정은 만들지 않는다(이미 있던 같은 역할 고정 계정은 비활성 — 아무도 못 들어오는 쪽이 기본) (0.3.0) — 코드 `service/accounts.py`
- 비밀번호 = PoC 계정(`card` · `active` · 그 env 아이디와 같은 `login_id`)에만 env 값을 bcrypt(`PROC_BCRYPT_ROUNDS`) 해시로. env 값이 지금 해시와 맞으면 다시 만들지 않는다 · 그 밖 계정은 해시를 지운다 (0.3.0) — A-16 · 코드 `_passwords`
- `CCC_DOCTOR_KOS_ACCOUNT_ID` 의 원장이 원장 목록에 없으면(비활성 · 시스템 계정 등) 의사 카드를 만들지 않고 로그에 사유만(값 없이) 남긴다

### 3.2 토큰

- 지금 형식(코드 `service/auth.py` — `PROC_SESSION_SECRET` HMAC 서명 · `PROC_SESSION_HOURS` 기본 12시간 (0.3.0))을 그대로 쓰고 **본문(claims)에 `role` · `staffId` 를 더한다**: `{sub: login_id, role, staffId|null, exp}` — A-08
- 검증: 서명 · 만료 + **`account` 에 `login_id` 가 있고 `active`** 인가. 아니면 401 `unauthorized`. 역할 · `staffId` 는 **토큰이 아니라 DB 의 지금 값**으로 판단한다(토큰 값과 다르면 401 — 다시 로그인) — 기본값
- 앱은 토큰을 기기 안전 저장소(iOS Keychain · `first_unlock_this_device`)에 둔다. 알림 [수락]용으로 서버 주소 + 토큰을 네이티브 키체인에도 따로 둔다(백그라운드에서 읽힘 · §5-1.3) (0.3.0) — 기본값 · A-17 · 코드 `session_store.dart` · `AppDelegate.swift`

### 3.3 로그인 API (SPEC-003 §7.1 을 바꾼다)

| 메서드 · 경로 | 요청 | 응답 | 오류 |
|---|---|---|---|
| ~~`GET /api/auth/accounts`~~ | — | **없앴다**(계정 목록 공개 제거 — A-16) | 404 (0.3.0) |
| `POST /api/auth/login` | `{id, password}` — **둘 다 필수**(빠지거나 그 밖 필드 = 400 `invalid_request`) (0.3.0) | `{token, expiresAt, id, role, name, staffId}` | 401 `invalid_credentials` 「아이디 또는 비밀번호가 맞지 않아요」 · 429 `too_many_attempts` 「로그인 실패가 많아요. 1분 뒤 다시 시도해 주세요」 (0.3.0) |
| `GET /api/auth/me` | — | `{id, role, name, staffId}` | 401 |

- 로그인 = **아이디 + 비밀번호**(bcrypt 비교). ~~카드를 눌러 바로(비밀번호 검증 없음)~~ (0.3.0) — A-16 · 코드 `service/auth.py`
- 없는 아이디 · 비활성 · 비밀번호 없는 계정 · 틀린 비밀번호 = **같은 401 · 같은 문구**(없는 아이디도 가짜 해시로 한 번 비교 — 시간 차 없게) (0.3.0)
- **같은 아이디 5회 연속 실패 → 1분 잠금(429)** · 잠금이 풀리면 0부터 · 성공하면 실패 수를 지운다 · 실패 수는 back 메모리(재시작하면 사라짐) (0.3.0) — A-16
- bcrypt 가 받지 못하는 72바이트 넘는 비밀번호 = 틀린 비밀번호로 (0.3.0) — 코드

### 3.4 조작 API 역할 검사표

검사는 **router 가 아니라 service 의 조작 함수 입구**에서(웹 · 앱 · 시험 모두 같은 길) — 위반은 도메인 예외 → 403 `{error:{code,message}}`. 검사 순서: 401(로그인) → 403 `fake_board`(SPEC-003 §2.3) → **역할 403**(`role_forbidden` · `doctor_forbidden` — 요청만 보고) → 404 → **호출을 읽어야 아는 403**(`not_your_call`) → 409(SPEC-003 §7.3).

| API | admin | doctor | nurse | 403 코드 |
|---|---|---|---|---|
| `GET /api/board` · `GET /api/board/stream` | ○ | ○ | ○ | — |
| `POST /api/visits/{id}/anesthesia/start` · `/end` | ○ | ○ | ○ | — |
| `POST /api/visits/{id}/calls` | ○ | ○ | ○ | — |
| `POST /api/calls/{id}/reassign-all` | ○ | ○ | ○ | — (기본값 — 「호출」과 같은 묶음으로 봄 · §9 OQ-602) |
| `POST /api/calls/{id}/accept` | ○ 원장을 골라 `doctorId` 필수 | ○ **자기 자신으로만**(아래) | **✕** | `role_forbidden` |
| `POST /api/procedures/{id}/start` · `/finish` | ○ | ○ | ○ | — |
| `POST /api/visits/{id}/home` | ○ | ○ | ○ | — |
| `WS /api/interpret` | ○ | ○ | ○ | (연결 거절 · §4.2) |

수락 규칙(A-07 · A-08):

| 누가 | 요청 `doctorId` | back 이 쓰는 원장 | 결과 |
|---|---|---|---|
| doctor | 없음 | 로그인 계정의 `staff_id` | 진행(SPEC-003 §5.5 · 아래 지정 규칙) |
| doctor | 자기 `staff_id` 와 같음 | 같음 | 진행 |
| doctor | 자기와 다름 | — | **403 `doctor_forbidden`** |
| doctor | — · 지정 호출(`kind=one`)인데 지정 원장 ≠ 자기 | — | **403 `not_your_call`** |
| doctor | — · 자기 원장이 원장 목록에 없음(비활성 등) | — | 409 `doctor_not_listed`(코드 그대로) |
| admin | 필수(없으면 400 `invalid_request`) | 요청 값 | 코드 그대로 — 지정 호출에 다른 원장이면 409 `doctor_mismatch` |
| nurse | 무엇이든 | — | **403 `role_forbidden`** |

- 받는 시술 범위 = 코드 `receivable(call)`(그 호출이 유효 호출인 시술 중 미수락) — **호출 1건 단위**(A-02 · D-27). 시안 방 단위 한 번에(M3)는 버림
- 요청 모양: `AcceptRequest.doctorId` 를 **선택**으로 바꾼다(`doctorId?: int`) — 웹 의국 화면(admin)은 지금처럼 보낸다
- 403 메시지(기본값): `role_forbidden` 「이 계정은 수락할 수 없어요」 · `doctor_forbidden` 「본인 이름으로만 수락할 수 있어요」 · `not_your_call` 「다른 원장을 지정한 호출이에요」

### 3.5 `actor` · 로그

- `event_log.actor` = 로그인 계정 `login_id` — A-08. KOS 반영 실패(`kos_failed`)는 `system` (0.3.0)
- `call_accept` 이벤트 payload 에 `byRole` 을 더한다(누가 대신 눌렀는지 — admin 이 원장 골라 수락한 것과 원장 본인 수락 구분) — 기본값
- 같은 payload 에 **`source`**(`push` \| `app` \| `web`) — 선택 헤더 `X-Accept-Source` 값(그 셋 중 하나일 때). 없으면 Origin 헤더가 있으면 `web` · 그 밖 `app`. 앱 화면 수락은 `app` · 알림 [수락]은 `push` 를 싣는다 (0.3.0) — A-18 · 코드 `api/actions.py` `accept_source`
- 토큰 · 비밀번호 · 키는 로그에 싣지 않는다(SPEC-003 §4.1 그대로)

### 3.6 웹 front (SPEC-003 화면에 닿는 곳만)

- ~~로그인 카드 = `GET /api/auth/accounts` 중 **`role = admin` 만**~~ → **아이디 · 비밀번호 폼**(카드 없음). 웹은 관리자 계정으로 쓴다 — 단 폼은 역할을 거르지 않는다(SPEC-003 OQ-518) (0.3.0) — A-03 · A-16 · 코드 `front/app/login/page.tsx`
- 세션(localStorage)에 토큰 · `role` · `name` 을 함께 저장. 헤더 계정 표시 = `name`
- 의국 화면 수락은 지금처럼 원장을 골라 `doctorId` 를 보낸다(admin) — A-08
- 그 밖 화면 · 규칙 변경 없음

## 4. 통역 (back 변경)

### 4.1 복사 목록 (D-01 — `cc/` import 금지 · 복사)

| `cc/back`(`origin/main`) | `procedure/back` 으로 | 어떻게 |
|---|---|---|
| `app/service/interpret/{session,soniox,assembler,chinese}.py` · `__init__.py` | `app/service/interpret/` | 그대로 — 언어 집합 `LANGS = {zh, en, ja, th, fr, es, tl, hi}` · Soniox 모델 · 음색 · 샘플레이트 · keepalive · 정리 규칙 모두 |
| `app/api/interpret.py` | `app/api/interpret.py` | **인증만 바꾼다**(§4.2) · 오류 문구의 `cc/back/.env` → `procedure/.env` |
| `tests/test_interpret.py` | `tests/` | 그대로 + §4.2 인증 시험 |
| 의존성 `websockets` · `opencc-python-reimplemented` | `pyproject.toml` | 버전 그대로 |
| container 의 `open_stt` · `open_tts` 주입 | `container.py` | 같은 모양(시험에서 가짜 Soniox 주입) |

### 4.2 WS 인증 — Origin 만으로 안 된다

이전 코드는 `Origin` 이 **없으면 통과**한다(앱은 Origin 을 안 보낸다 → 누구나 연결 · 키 소모). 그래서:

| 항목 | 계약 |
|---|---|
| 경로 | `WS /api/interpret` |
| 토큰 | 핸드셰이크 헤더 **`Authorization: Bearer <ccc 토큰>`**(앱 — `dart:io` WebSocket 은 헤더를 실을 수 있다). 브라우저용으로 `?token=` 도 받는다(SPEC-003 §7.5 와 같은 이유 · 접근 로그 쿼리 지움 필터가 이미 있음 — 코드 `DropQueryString`) |
| 검증 | `accept()` **전에** §3.2 검증. 실패면 accept 하지 않고 닫는다(close 1008 → 클라이언트에는 핸드셰이크 거절 403) |
| Origin | 있으면 `PROC_INTERPRET_ORIGIN`(비면 `PROC_FRONT_ORIGIN`)과 같아야 — 다르면 1008. 없으면(앱) 토큰만으로 |
| 역할 | 세 역할 모두(§3.4) |
| 키 없음 | `SONIOX_API_KEY` 가 비면 `error no_api_key`(코드 그대로) |
| 동시 연결 | 제한 두지 않음(Soniox TTS 동시 한도 3 — 이전 코드 주석). 세션이 끝나면 Soniox 두 연결을 반드시 닫는다(코드 그대로) |

### 4.3 WS 메시지 (이전 PoC 계약 그대로 — `interpret-ws-contract.md` · 코드 `session.py`)

| 방향 | 프레임 | 내용 |
|---|---|---|
| 앱 → back | 첫 텍스트 | `{type:"start", lang, traditional}` — `lang ∈ LANGS` · `traditional` = 중국어 자막을 번체로(§4.4). 10초 안에 안 오면 `error bad_request` |
| 앱 → back | 바이너리 | **PCM s16le · 16 kHz · mono** 조각(이전 front = 640 샘플 = 40 ms) |
| 앱 → back | 텍스트 | `{type:"pause"}` · `{type:"resume"}` · `{type:"stop"}` |
| back → 앱 | 텍스트 | `{type:"ready"}` · `{type:"caption", id, side:"me"\|"them", original, translation, final}` · `{type:"audio_start", id, sampleRate:24000}` · `{type:"audio_end", id}` · `{type:"error", code, message}` |
| back → 앱 | 바이너리 | 번역 음성 **PCM s16le · 24 kHz · mono**(`audio_start` ~ `audio_end` 사이) |

- `side` = 원문이 한국어면 `me`(의료진) · 아니면 `them`(고객) — 말한 사람을 자동으로 가른다(Soniox `two_way`)
- 앱은 **번역 음성 재생 중에는 마이크 조각을 보내지 않는다**(이전 front `!speaking` — 스피커 소리가 다시 들어가 번역되는 것 막기) — A-04
- 닫기: 드로어 [종료] = `stop` 보내고 닫음. 앱이 백그라운드로 가면 닫는다(기본값)

### 4.4 언어

| `lang` | 화면 이름 | 고객 국적 → 자동(이전 front `NAT_LANG`) | 번체 |
|---|---|---|---|
| `zh` | 중국어 | TW · CN · HK | TW · HK 면 `traditional=true` |
| `en` | 영어 | US · PH · IN · **그 밖 전부(기본)** | — |
| `ja` | 일본어 | JP | — |
| `th` | 태국어 | TH | — |
| `fr` | 프랑스어 | FR | — |
| `es` | 스페인어 | — | — |
| `tl` | 타갈로그어 | — | — |
| `hi` | 힌디어 | — | — |

- 고객 국적 = 스냅샷 `cards[].customer.nationality`. 위 표는 ISO 두 글자 기준(이전 PoC). **KOS 데모 지점의 실제 값 형식은 미확인** → §9 OQ-604
- 드로어 언어 칩 = 위 8개. 자동 고른 언어에 「· 자동」(시안 모양). 시안의 4개(번체 · 광둥어 · 일본어 · 베트남어)는 쓰지 않는다 — A-04
- 국적이 `KR` 이거나 없으면 자동 = `en`(기본값 — 이전 front 와 같음)

## 5. 빠른 말하기 (A-05 — 하드코딩)

- 문구 6개 = 시안 `zh-TW` · `ja` · `vi` 세트의 한국어 6개(시안 광둥어 세트의 「의사 선생님이 곧 오세요」는 다른 세트에 없어 뺐다)
- 누르면 **기기 TTS(iOS 음성 · `flutter_tts`)로 고객 언어 문장을 읽는다** — 시안 주석 「Flutter 에선 flutter_tts」 · 기본값. back · Soniox 를 거치지 않는다(키 사용 없음 · 오프라인도 됨)
- 통역 드로어가 열려 있으면 대화에 의료진 말(오른쪽 · 원문 = 한국어 · 번역 = 그 문장)로 한 줄 더한다(시안 `say`) — 서버로는 안 보냄
- 언어 = 통역 드로어에서 고른 언어, 안 열었으면 자동 언어(§4.4) · `zh` 는 번체 여부를 따른다
- TTS 음성 로캘(기본값): zh 번체 `zh-TW` · zh 간체 `zh-CN` · en `en-US` · ja `ja-JP` · th `th-TH` · fr `fr-FR` · es `es-ES` · tl `fil-PH` · hi `hi-IN`. **기기에 그 음성이 없으면** 칩을 누를 때 토스트 「이 기기에 <언어> 음성이 없어요」(조용히 실패하지 않는다) — tl 음성 유무는 실기기에서 확인(§9 OQ-607)

| # | 한국어 | zh 번체 | zh 간체 | en | ja | th | fr | es | tl | hi |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 조금 뜨거울 수 있어요 | 會有一點熱 | 会有一点热 | It may feel a little hot. | 少し熱くなります | อาจจะรู้สึกร้อนเล็กน้อยนะคะ | Cela peut chauffer un peu. | Puede sentir un poco de calor. | Maaaring medyo mainit po ito. | थोड़ी गर्मी महसूस हो सकती है। |
| 2 | 아프면 손을 들어주세요 | 痛的話請舉手 | 痛的话请举手 | If it hurts, please raise your hand. | 痛かったら手を挙げてください | ถ้าเจ็บ กรุณายกมือขึ้นนะคะ | Si vous avez mal, levez la main, s'il vous plaît. | Si le duele, levante la mano, por favor. | Kung masakit po, pakitaas ang inyong kamay. | दर्द हो तो कृपया हाथ उठाइए। |
| 3 | 눈을 감아주세요 | 請閉上眼睛 | 请闭上眼睛 | Please close your eyes. | 目を閉じてください | กรุณาหลับตานะคะ | Fermez les yeux, s'il vous plaît. | Cierre los ojos, por favor. | Pakipikit po ang inyong mga mata. | कृपया आँखें बंद कीजिए। |
| 4 | 10분 정도 걸려요 | 大約需要十分鐘 | 大约需要十分钟 | It will take about 10 minutes. | 10分ほどかかります | ใช้เวลาประมาณ 10 นาทีค่ะ | Cela prendra environ 10 minutes. | Tardará unos 10 minutos. | Aabutin po ito ng mga 10 minuto. | इसमें लगभग 10 मिनट लगेंगे। |
| 5 | 움직이지 마세요 | 請不要動 | 请不要动 | Please don't move. | 動かないでください | กรุณาอย่าขยับนะคะ | Ne bougez pas, s'il vous plaît. | No se mueva, por favor. | Huwag po kayong gumalaw. | कृपया हिलें नहीं। |
| 6 | 다 끝났습니다 | 已經結束了 | 已经结束了 | We're all done. | 終わりました | เสร็จเรียบร้อยแล้วค่ะ | C'est terminé. | Ya hemos terminado. | Tapos na po. | सब पूरा हो गया है। |

- zh 번체 · ja 는 시안 문구 그대로. 나머지는 이 문서가 옮긴 **초안**(원어민 검수 전) — §9 OQ-606
- th 는 여성 화자 어미(นะคะ · ค่ะ) — 시술실 간호 인력 기준 기본값 · §9 OQ-606

## 5-1. 원장 호출 푸시 (0.2.0 — A-14)

### 5-1.1 기기 토큰 (back 변경 · 앱)

테이블 `device`(ccc 원천):

| 필드 | 뜻 |
|---|---|
| `id` | PK |
| `account_id` | 등록한 로그인 계정(`account.id`) |
| `token` | APNs 기기 토큰(16진 32 ~ 200자 · 소문자로 저장 · 유일) (0.3.0 — 코드 `schemas/actions.py` `DeviceRequest`) |
| `created_at` · `updated_at` | |

| 메서드 · 경로 | 요청 | 응답 | 역할 · 규칙 |
|---|---|---|---|
| `POST /api/devices` | `{token}` | `{ok:true}` | 세 역할 모두(기본값 — 발송 대상은 **의사 · 관리자** 계정 · §5-1.2 받는 사람 규칙 표). **같은 토큰이 다른 계정에 있으면 지금 계정으로 옮긴다**(한 기기 = 마지막 로그인 계정) · 같은 계정이면 `updated_at` 만 |
| `DELETE /api/devices/{token}` | — | `{ok:true}` | 자기 계정의 토큰만 지운다(남의 것 · 없는 것 = 그냥 `{ok:true}` — 기본값) |

앱:

1. 로그인 성공 직후 **알림 권한 요청**(alert · sound · badge 없음 — 기본값). 거부해도 앱은 그대로 쓴다(머리 계정 ▾ 아래 「알림 꺼짐 · 설정에서 켜기」 한 줄 — 기본값)
2. 허용되면 iOS `registerForRemoteNotifications` → 받은 기기 토큰(16진)을 `POST /api/devices`. 토큰이 바뀌어 다시 오면 다시 등록. 앱 시작 때 로그인 상태면 다시 등록(멱등)
3. **로그아웃 때 `DELETE /api/devices/{token}` 먼저** → 토큰 지움 → 로그인 화면
4. 토큰 받기는 Runner 의 작은 플랫폼 채널(Swift `AppDelegate`) 또는 Firebase 를 쓰지 않는 패키지 — **Firebase 의존 0** 이 조건 (기본값)
5. 서버 주소(§2.2)를 바꾸면 새 주소로 다시 등록

### 5-1.2 발송 (back)

| 항목 | 계약 |
|---|---|
| 언제 | 호출이 생길 때 — `POST /api/visits/{id}/calls`(`call_create`) · `POST /api/calls/{id}/reassign-all`(`call_reassign_all`, 새 전체 호출) — **트랜잭션 커밋 뒤** 비동기로(조작 응답 · SSE 를 기다리게 하지 않는다) |
| 받는 사람 | 아래 「받는 사람 규칙」 표의 계정들의 `device` 토큰 전부. 토큰 없으면 보내지 않음 |
| 내용 | 제목 「원장 호출」 · 본문 **「<방> · 시술 N건 · 전체 호출」 / 「<방> · 시술 N건 · 지정 호출」** — N = 그 호출에 든 시술 수. **고객 이름 · 국적 · 시술 이름 넣지 않음**(잠금 화면) · 소리 `default` |
| payload | `{aps:{alert:{title, body}, sound:"default"}, visitId, callId}` — **의사 수신자에게만 `aps.category = "CALL"`**(알림에서 바로 [수락] · §5-1.3). 의사 수신자는 늘 그 호출을 수락할 수 있는 원장(전체 = 전원 · 지정 = 그 원장). 관리자 알림은 category 없음(앱을 열어 원장을 고른다) (0.3.0) — A-17 · 코드 `service/push.py` |
| APNs 요청 | HTTP/2 `POST https://api.push.apple.com/3/device/<token>`(`APNS_ENV=production`) · `https://api.sandbox.push.apple.com/…`(`sandbox`). 헤더 `authorization: bearer <JWT>` · `apns-topic: <APNS_BUNDLE_ID>` · `apns-push-type: alert` · `apns-priority: 10` · `apns-expiration: 0`(늦게 닿을 호출은 의미 없음 — 기본값) |
| JWT | ES256 · `kid=APNS_KEY_ID` · `iss=APNS_TEAM_ID` · `iat` · `.p8` 로 서명. **40분마다 새로**(Apple: 20분 ~ 60분 사이 재사용) — 기본값 |
| 설정 없음 | `APNS_*` 하나라도 비면(또는 `APNS_ENV` 가 두 값이 아니면) 발송을 끈다(서버 시작 때 경고 1줄 · 조작은 그대로) · 받을 기기마다 `push_log` `skipped_no_key` 를 쌓는다 (0.3.0) |
| 키 확인 | 켜져 있으면 서버 시작 때 JWT 를 한 번 서명해 본다 — 실패면 오류 로그 1줄(값 없이) · 발송은 실패로 기록 (0.3.0) — 코드 `check_key` |
| 실패 | 로그(HTTP 상태 · `reason` · 토큰 끝 6자리만 — 토큰 전체 · JWT · 키 없음) + `push_log`. 네트워크 오류 · 5xx · 429 는 **재시도 1회**. **죽은 토큰 = 그 `device` 행 삭제 + `push_log` `token_removed`** — 410 은 늘 · 400 은 `reason` 이 `BadDeviceToken` · `DeviceTokenNotForTopic`(번들 id 바꾸기 전 옛 토큰 — 2026-10-21 실 APNs) · `Unregistered` 일 때. ~~400 `BadDeviceToken` 은 로그만 · 삭제 안 함~~(→ OQ-614). 그 밖 4xx 는 재시도 없음 · `failed` (0.3.0) — 코드 `service/push.py` `DEAD_400` |
| 이벤트 | `event_log` 에 남기지 않는다(조작이 아님). ~~발송 성공/실패는 앱 로그만~~ → **`push_log`(아래)** 에 받는 기기마다 1행 (0.3.0) — A-18 |
| 라이브러리 | `httpx[http2]`(h2) · `PyJWT[crypto]` 또는 `cryptography` — 기본값 |

`push_log`(쌓기만 · `event_log` 와 같은 원칙 · 조회 API 는 나중 — A-18) (0.3.0):

| 필드 | 뜻 |
|---|---|
| `id` · `call_id` · `visit_id` | 호출 · 카드 |
| `account_id` · `role` · `device_id` | 받는 계정 · 역할 · 기기 행 |
| `token_tail` | 기기 토큰 **끝 6자리만** |
| `category` | `CALL`(의사) \| null |
| `status` | `sent` · `failed` · `skipped_no_key` · `token_removed` |
| `apns_status` · `apns_reason` · `apns_id` · `attempts` | APNs 응답 상태 · 이유 · `apns-id` 헤더 · 보낸 횟수(1 · 재시도면 2) |
| `created_at` · `sent_at` | 발송 시작 · 200 받은 시각 |

받는 사람 규칙:

| 계정 역할 | 전체 호출(`kind=all`) | 지정 호출(`kind=one`) | 근거 |
|---|---|---|---|
| doctor | `active` 의사 계정 **전원** | **지정 원장**(`target_staff_id`)에 연결된 의사 계정만 | A-14 |
| admin | **받음** | **받음**(지정 원장과 상관없이 — 모든 호출) | A-15 |
| nurse | 안 받음 | 안 받음 | A-14(원장 호출) |

- 빼는 사람: 호출을 누른 계정이 **의사**면 그 의사 자신은 뺀다(기본값). **관리자는 빼지 않는다** — 관리자 계정은 간호 스테이션 · 의국이 같이 쓰므로(D-05 · A-15 「모든 호출」), 웹(관리자)에서 누른 호출도 관리자 폰으로 간다
- 한 토큰은 한 계정에만 있으므로(§5-1.1 옮기기) 같은 기기에 두 번 가지 않는다

### 5-1.3 앱에서 받기

- **알림 [수락]**(`CALL` 카테고리 · 의사 알림만 · A-17) (0.3.0) — 앱 화면을 열지 않고 네이티브(`AppDelegate.swift`)가 키체인의 서버 주소 · 토큰으로 `POST /api/calls/{callId}/accept`(본문 `{}` = 자기 자신 · 헤더 `X-Accept-Source: push`)를 백그라운드 작업으로 보낸다
  - 결과 = **로컬 알림 한 줄**: 성공 「수락했어요 · <방>」 / 실패 「수락 못 함 · <back message>」(연결 실패면 「서버에 연결할 수 없어요」 · 키체인에 로그인 없음이면 「수락 못 함 · 앱에서 다시 로그인해 주세요」). 실패 알림을 누르면 그 방 룸 상세
  - Apple Watch = iPhone 알림 액션이 워치에 그대로 보인다(워치 앱 없음). **실기기 워치에서 [수락] 확인은 기록 없음** → §9 OQ-616
- **알림을 누르면** 앱이 열리고(꺼져 있던 경우 포함) 로그인 상태면 **`visitId` 룸 상세**로. 그 방이 스냅샷에 없으면 토스트 「호출이 끝났거나 방이 비었어요」 → 목록 / 로그인 안 됐으면 로그인 뒤 그 방으로 — 기본값
- 앱이 앞에 있을 때도 배너 + 소리로 보인다(iOS 14+ `banner · list · sound`) — 기본값(원장이 목록을 보고 있어도 알게)
- 배지 숫자는 쓰지 않는다 — 기본값

## 6. 앱 화면

| 화면 정본 | 값 |
|---|---|
| 확정 시안(모양 기준) | `design-mobile/Ceramique 간호사 모바일.dc.html` · `Ceramique 시술실 태블릿.dc.html`(claude design `dda9a931`) |
| **구현 반영 시안 파일 이름**(main `329b543` 앱 화면 = A1 ~ A7 · T1 ~ T8 · 로그인 폼 반영을 다시 그린 시안) | claude design `dda9a931` 「Ceramique 간호사 모바일 (구현 v3)」 · 「Ceramique 시술실 태블릿 (구현 v3)」 · 「Ceramique 의료진 앱 (구현 v3)」(.dc.html) — 폰 · 태블릿 장면 14 + 캔버스 「구현 v3」 절 22 프레임 · 원본 3개는 그대로 · 대응표 `design-sync-mobile-report.md` (2026-10-22) |

### 6.0 공통 원칙 (A-02)

- **모든 버튼의 보임 · 켜짐 · 상태 이름 · 필터 수 · 「확인 필요」 = back 스냅샷 값**(SPEC-003 §7.2 · 코드 `schemas/board.py`). 앱은 규칙을 다시 계산하지 않는다
  - 시술: `state` · `pickable` · `canStart` · `canFinish` · `call` · `doctor` · `kind` · 고객: `state` · `canCall` · `canHome` · `need` · `anesthesia.{canStart, canEnd, long, runningSince, lastMinutes}` · 판: `counts` · `calls` · `doctors` · `limits`
- 앱이 하는 계산은 **표시용 매핑만** — 문구 · 순서 · 경과 시간(스냅샷 `now` 와 기기 시계 차 보정 · SPEC-003 §6.6) · 「나에게 온 호출」 고르기(의사 = `calls[]` 중 `kind=all` 또는 `targetDoctorId = 내 staffId` · 관리자 = `calls[]` 전부 — A-15). 이 매핑은 웹 `components/procedures/view.ts`(`STATE_NAME` · `STATE_BADGE` · `procLine` · `orderedProcs` · `firstOpenCall` · `needView` · `docName` · `visitCls`)와 같게 Dart 로 옮긴다(리포트 §7-1)
- `kind = "etc"`(방 배정 등) 줄은 **그리지 않는다** — E2E-10. 「n / m」 · 진행 막대도 `kind = procedure` 만 센다
- 조작 응답은 `{ok…}` 만 — 화면은 뒤따르는 SSE `board` 로 바뀐다(SPEC-003 §7.5). 409 · 403 은 토스트로 `message` 를 그대로 보인다
- 「KOS 반영 중 · 실패」(`kos.status`) · 「수납 필요」(`paymentRequired`) — 룸 상세 머리 아래 작은 글자 / 칩으로 보인다(웹 SPEC-003 §6.3 · §6.7 #7 · #8 과 같은 뜻) — 기본값(시안엔 자리 없음 · X13)
- 배치 고르기: 화면 짧은 변 **< 600 = 모바일 배치**, 이상 = 태블릿 배치(기본값 — 아이폰 / 아이패드)
- **반응형 글자 배율**(T4): 폰 = 1 · 태블릿 = 짧은 변 / 700(1.15 ~ 1.3 — 아이패드 11" ≈ 1.19 · 13" = 1.3 · mini = 1.15). 모든 글자(Typo · 숫자 타이머)에 `MediaQuery.textScaler` 로 걸고, 버튼 높이 · 카드 격자 최소 폭도 같은 배율. 모바일 글자는 그대로 (0.3.0) — T3 · T4 · 코드 `theme/tokens.dart`
- **토스트 = 화면 위**(safe area + 머리 아래) · Material 안에서 그린다(노란 이중 밑줄 없음) (0.3.0) — A3 · 코드 `widgets/ui.dart`

### 6.1 로그인 (모바일 · 태블릿 같음)

- 시안에 로그인 화면이 없다 — 웹 로그인의 모양을 앱 테마로(기본값)
- 위: 로고 · 「시술 현황」 / ~~계정 카드~~ → **아이디 · 비밀번호 입력 + [로그인]**(관리자 · 의사 · 간호사 모두 같은 폼) → 목록. 실패 401 · 잠금 429 = 폼 아래 빨간 한 줄(back `message`). **아이디만 기기에 기억**(키체인) · 비밀번호는 저장하지 않는다 (0.3.0) — A-16 · 코드 `screens/login_screen.dart`
- 「서버 주소」 입력칸 · [연결 확인](`GET /api/health`)은 **debug 빌드에만**(§2.2) (0.3.0) — T8
- 토큰이 있고 `GET /api/auth/me` 가 200 이면 로그인 화면을 건너뛴다 · 401 이면 로그인으로
- 로그인 직후 알림 권한 요청 · 기기 토큰 등록(§5-1.1) (0.2.0)
- 헤더 계정 칸 ▾ = [로그아웃](기기 토큰 해제 → 토큰 지움 → 로그인 · §5-1.1) (0.2.0). 시안의 「데모 계정 전환」은 로그아웃 → 다른 아이디로 대신한다 (0.3.0)

### 6.2 시술실 현황 (목록)

| 요소 | 모바일 | 태블릿 | 값 |
|---|---|---|---|
| 머리 | 56px: 「시술실 현황」 · `<계정 이름> ▾` / 오른쪽 「확인 N」 빨간 알약 · 시계 | 64px: 로고 · 「시술실 현황」 / 시계 · `<계정 이름> ▾` · 「확인 필요 N」 | 「확인」 수 = `counts.need` · 계정 = 로그인 `name` |
| 필터 칸(가로 스크롤 · 한 번에 하나) | 전체 · 확인 · 대기 · 마취 · 호출 · 진행(웹과 같은 6칸 · **겹쳐 셈**) + **「귀가」**(귀가 대기 카드 — 「전체」는 귀가 대기를 포함하므로 칩 합이 맞게) (0.3.0) + **의사 · 관리자 계정은 「수락 대기 N」**(관리자 = 모든 받을 호출 — 0.2.0) | 같음 | 수 = `counts.{all, need, waiting, anes, call, doing}` · 「귀가」 수 = 스냅샷 카드 중 `state = home` 수(`counts` 에 칸 없음 — 표시용 세기) (0.3.0). 칸의 카드 고르기 = 웹 `filterFn` 과 같은 정의(SPEC-003 §6.4). 「수락 대기」 = 나에게 온 호출이 있는 카드 · 수 = 그 호출 수 |
| 카드 배열 | 한 줄 1장 | 격자 `minmax(270px × 글자 배율,1fr)` · **필터로 카드가 적어도 왼쪽 위부터 채운다**(폭 전체) (0.3.0 — T5) | 순서 = 입실순(`inAt`) · 귀가 대기는 맨 뒤 흐림(SPEC-003 §6.3 · 앱은 [입실순 \| 배치순] 고르기 없음 — 기본값). 필터 = 맞는 카드만 남김(흐림은 쓰지 않음 — 웹과 같음 · T5 처분) |
| 카드 | 방 이름 · 고객 이름 / 상태 Badge(§6.0 · 마취 중 · 확인 필요 덮기는 웹 §5.2 와 같음) — **배지는 카드 오른쪽 끝**(좌우 여백 같게 · 짧은 배지도) · (태블릿) 국적 · 첫/재내원 칩 (0.3.0 — A1) | 같음 | `room.title` · `customer` · `state` · `anesthesia.runningSince` · `need` |
| 카드 「지금」 상자 | 진행 시술 있음 → 「<시술>」「<원장> · HH:MM 시작」 · mm:ss / 받을 호출 있음 → 「전체 호출 · 수락 대기」·「<원장> 지정 · 수락 대기」 · N분(≥ `limits.callMin` 빨강) / 마취 중 → 「마취 중」「HH:MM 시작 · 기준 N분」 · N분(`long` 빨강) / `canHome` → 「시술 모두 완료」 / 귀가 대기 → 「귀가 대기 · HH:MM」 / 그 밖 「시술 대기」 + 「담당 <원장>」 또는 「담당의 미정」 | 같음 | 우선순위는 표시만(상태는 바꾸지 않음): 귀가 대기 > 진행 > 모두 완료 > 호출 > 마취 > 대기 — 시안 M9 의 **보이는 순서**만 쓴다(빨강 · 확인 필요 판정은 `need` · `long`) |
| 진행 막대 | 시술 수만큼 칸(완료 회색 · 진행 파랑 · 대기 연회색) + 「n / m」 + 「다음 <시술> · <원장>」 | 같음 | `procedures[].state` · 순서 = `orderedProcs` |
| 카드 [수락] | **의사 계정 + 그 카드에 나에게 온 호출** → 카드 아래 「전체 호출 · N건」/「나를 지정 · N건」 + [수락] — **호출마다 한 줄**(한 카드에 둘이면 둘). **관리자 계정 + 그 카드의 받을 호출** → 같은 줄 + [수락] — 누르면 **원장 고르기**(§6.3 #2) (0.2.0) | 같음(태블릿도 의사 · 관리자 계정이면 보임 — §6.7) | `calls[]` · 의사 = `POST /api/calls/{callId}/accept`(본문 없음) · 관리자 = `{doctorId}` |
| 강조 | `need` 있음 = 빨간 2px 테두리 · `doing` = 파랑 1px · 귀가 대기 = 흐림 | 같음 | |
| 누르면 | → 룸 상세 | → 룸 상세 | |
| 빈 상태 | 「시술 중인 방이 없어요」 | 같음 | 기본값 |

### 6.3 룸 상세

모바일 = 한 열(위 → 아래) · 태블릿 = 두 열(왼쪽 `minmax(260px,380px)` = 오더 메모 · 마취 / 오른쪽 = 호출 · 완료 · 시술).

- **본문 순서 = 지금 할 일(호출 · 완료 상자) → 오더 메모 → 마취 → 시술(+ [의사 호출])** — 웹 카드 순서와 같게. 아래 표 번호는 요소 이름일 뿐 순서가 아니다 (0.3.0 — A5)
- **태블릿 두 열 = 남은 높이 전부**(통역 바 바로 위까지): 왼쪽 오더 메모 카드가 늘어나고(안에서 스크롤) 마취는 아래 · 오른쪽 시술 카드가 늘어나고(시술 목록 안에서 스크롤) [의사 호출] 줄은 열 바닥 고정. 가로 · 세로 둘 다 (0.3.0 — T1)
- **태블릿 머리 = 한 줄**: [← 현황 · 다른 룸 확인] │ 방(크게) │ 고객 · 국적 · 첫/재내원 · 입실 │ … 상태 배지 · 시각. 모바일은 두 줄 그대로. 배지 · 시각은 머리 오른쪽 끝(A4) · 배지 문구가 길어 잘리지 않게(A6) (0.3.0 — T2 · A4 · A6)
- 오더 메모 글자: 모바일 = 본문 한 단계 위 · 태블릿 = 시안 제목 크기 + 본문(배율 곱해 시술 이름과 비슷 · 줄 간격 1.6) (0.3.0 — T3)

| # | 요소 | 값 · 버튼 |
|---|---|---|
| 1 | 머리: [← 현황] + 「다른 룸 확인 N」(빨강 · `counts.need` 에서 이 카드 뺀 수) / 상태 Badge · 시계 / 방 · 고객 이름 / 국적 칩 · 첫/재내원 · 「입실 HH:MM」 / 「수납 필요」 · 「KOS 반영 중 · 실패」 | `room` · `customer` · `inAt` · `paymentRequired` · `kos` |
| 2 | **호출 상자** — 이 카드의 받을 호출(`calls[]` 중 `visitId` 같음)마다 하나: 「전체 호출 / <원장> 지정 호출 · 수락 대기」 · 큰 「N분」 · 「HH:MM 호출 · 시술 N건 · 기준 N분(넘음)」 | 의사(나에게 온 호출): **[수락 · N건]**(lg · 꽉 찬 폭) · **관리자(모든 받을 호출 · 0.2.0 · A-15)**: 웹 호출 탭과 같은 규칙 — 전체 호출 = 원장 고르기(`doctors[]` 비어 있는 원장 먼저 · 「<busyRoom> 시술 중」/「비어있음」 · 하나만) → [<원장> 수락 · N건] · 지정 호출 = [<지정 원장> 으로 수락 · N건](원장 고정) + [다른 원장에게] · 간호사 · 나에게 안 온 호출: [다른 의사 호출](→ 호출 시트 · 그 호출의 시술 미리 체크) · 지정 호출이면 [다른 원장에게](`reassign-all`) |
| 3 | **완료 상자**(`canHome`): 「시술 모두 완료」 · 「마지막 종료 HH:MM」 + **[귀가 대기]** | `POST /api/visits/{id}/home` — 세 역할 모두(A-08) |
| 4 | 시술 상자: 「시술 N · 완료 n」 · 줄마다 이름 · 둘째 줄(웹 `procLine` 문구) · 오른쪽 [시작](`canStart` 일 때 켜짐 · `wait` 일 때 보임) / [종료](`canFinish`) / 「완료」 Badge · 「호출함」 Badge. 아래 **[의사 호출]**(`canCall` 일 때 켜짐 — 꺼지면 「호출할 대기 시술 없음」) | `procedures[]` · 진행 줄 파랑 바탕 |
| 5 | 마취 상자: 「마취」 + 「안 함」 / 「완료 N분」 / 「마취 중」 「N분」(`long` 빨강) + [마취 시작](`canStart`) / [마취 종료](`canEnd`) | `anesthesia` — 시술 진행 중에도 켜질 수 있다(D-23 · 시안 X6 버림) |
| 6 | 오더 메모(전체 · 줄바꿈 그대로) | `orderMemo` — 없으면 「오더 메모 없음」 · 글자 크기는 위 T3 |
| 7 | 바닥 고정 **통역 바**: 「빠른 말하기 · <언어>」 + 문장 칩 6개(§5) + **[통역하기]**(lg → 드로어). 태블릿 = 「통역」 라벨 + 칩 + [통역하기] 한 줄 · 칩 줄 끝은 **페이드**(가로 태블릿에서 마지막 칩이 잘려 보이던 것 · 끝까지 밀면 마지막 칩이 페이드 밖) (0.3.0 — T7) | §4 · §5 |

- 이 방 카드가 스냅샷에서 사라지면(KOS 귀가 처리 등) 토스트 「<방> 고객이 판에서 빠졌어요」 → 목록으로(기본값)

### 6.4 의사 호출 시트 (바텀 시트 · 태블릿은 가운데 시트)

- 머리 「의사 호출 · <방>」(태블릿 「<방> · <고객>」)
- 「호출할 시술」 머리에 **[전체 선택]**(`pickable` 시술만 · 웹 카드 「전체 선택」과 같은 동작) (0.3.0 — A2)
- 「호출할 시술」 체크 줄 = **`pickable` 시술만 켜짐**(나머지 꺼짐 · 회색). 줄 메모 = 웹 `procLine`. 기본 체크: [의사 호출]로 열면 **없음** · [다른 의사 호출]로 열면 그 호출의 받을 시술(기본값 — 시안 M12 의 미리 체크 규칙은 버림 · A-02)
- 「누구에게」 = 「모든 의사 · 먼저 수락한 원장」 + `doctors[]`(**비어 있는 원장 먼저** — `busy=false` 먼저 · 「<busyRoom> 시술 중」/「비어있음」) · 하나만 · 다시 누르면 해제
- [취소] · [<원장> 호출 · N건 / 모든 의사 호출 · N건](대상 · 시술 둘 다 있어야 켜짐 · 아니면 「의사를 선택하세요」)
- 보내기 = `POST /api/visits/{visitId}/calls {procedureIds, target}` → 닫고 토스트(웹 문구)
- 시트는 시안(X10 — 취소 · 시트 안 체크)대로 — 웹 팝오버와 모양만 다르고 API · 규칙은 같다

### 6.5 통역 드로어 (높이 92%)

- 머리: 「통역 · <언어> ▾」(누르면 언어 칩 8개 · §4.4) · 「<방> · mm:ss」 · [종료]. 태블릿은 「<고객> 님 · <국적> · 국적으로 자동 선택 · 눌러서 변경」 · [통역 종료]
- 대화: 의료진(`side=me`) 오른쪽 파랑 · 고객(`them`) 왼쪽 흰색 · 원문 + 번역. `final=false` 는 「…」 흐림으로 덮어쓰기
- 문장 칩(§5) · 마이크 버튼: 연결 중(`ready` 전) → 듣는 중 → 멈춤(`pause`/`resume`). 「양쪽 말을 모두 들어요 · 누가 말했는지 자동으로 구분해요」
- 언어를 바꾸면 지금 WS 를 `stop` 하고 새 `start` 로 다시 연다(이전 front 와 같음)
- 닫으면 대화는 기기에서 지운다 — 통역 바 아래에 「마지막 통역 HH:MM · N문장」만(시안 M16 · 기본값)
- 오류(`error` · 연결 끊김 · 마이크 거부) = 드로어 안 빨간 줄 + [다시 연결]. 마이크 거부면 「설정 → 시술 현황 → 마이크」 안내

### 6.6 테마

- Ceramique 토큰(색 · 글꼴 Pretendard · 반경 · Badge · Button 크기 lg 48 · md 40 · sm)을 `theme/` 에 Dart 상수로 옮긴다 — 원천 = `procedure/front/app/styles/ceramique-theme.css` · `medikit-patches.css`(리포트 §7: 시안과 어긋남 0)
- medikit 은 React 라 쓰지 못한다 — 모양만 Flutter 위젯으로(기본값)
- Pretendard 는 `pubspec.yaml` 에 글꼴 파일로 넣는다(라이선스 OFL — 이미 웹이 씀)

### 6.7 시안과 다른 곳

| # | 시안 | 이 계약 | 근거 |
|---|---|---|---|
| 1 | 마취 버튼 = 어떤 시술도 시작 전에만(M8 · X6) | `anesthesia.canStart/canEnd` — 진행 중에도 | A-02 · D-23 |
| 2 | [시작] = 진행 중 시술 있으면 꺼짐 · 동의서(M5 · X7 · X8) | `canStart` 그대로(동시 진행 안 막음 · 동의서 없음) | A-02 · A-06 · D-30 |
| 3 | [수락] = 그 방의 나에게 온 호출 전부 한 번에(M3) | **호출 1건마다 [수락]** · 받는 범위 = back | A-02 · A-07 · D-27 |
| 4 | 확인 필요에 「담당의 미정 대기」(M10) | `need`(home · anes · call)만 | A-02 |
| 5 | 필터 = 상태 하나씩 · 「완료 · 귀가」 칸(M11 · X15) | 웹과 같은 6칸 겹쳐 셈(`counts`) + **「귀가」 칸**(T5) + 의사 · 관리자 「수락 대기」 (0.3.0) | A-02 · T5 |
| 6 | 태블릿 = 「김 간호사」 고정 · 수락 없음 | 로그인 계정 이름 · 의사 계정이면 태블릿에서도 [수락] · 관리자 계정이면 원장 골라 [수락](0.2.0) | A-03 · A-07 · A-15 |
| 7 | 계정 전환 드롭다운(데모) | 로그아웃 → 카드 다시 고르기 | A-03 |
| 8 | 언어 4개(번체 · 광둥어 · 일본어 · 베트남어) | 이전 PoC 8개 | A-04 |
| 9 | [다시 알림] · [시술 메모] · 동의서 줄 · 「데모: 서명 / 수락 처리」 · 간호사 요청 · 빈 방 카드 · 주의 상자 · meta(나이 · 성별 · 출국) · 마취 종류 「크림」 | 없음 | A-06 · §1.2 |
| 10 | 「명동점 A구역」 | 쓰지 않음(구역 이름 저장 안 함 · 조회 구역 = 4층) | D-08 · N13 |
| 11 | 「HH:MM 김 간호사 호출」 | 「HH:MM 호출」(누가는 로그만) | §1.2 |
| 12 | 귀가 대기 흐림 0.6 | 웹과 같은 0.55 | SPEC-003 §5.7 |
| 13 | 로그인 화면 없음 | §6.1 아이디 · 비밀번호 폼(서버 주소는 debug 만) (0.3.0) | A-03 · A-16 · A-20 |
| 14 | 방 배정(etc) 줄 없음 | 그리지 않음(같음) | E2E-10 |
| 15 | 「수납 필요」 · 「KOS 반영 중 · 실패」 자리 없음 | 룸 상세 머리 아래 작게 | §6.0 · SPEC-003 §6.7 #7 · #8 |

## 7. 데이터 — SSE · API

### 7.1 SSE 를 Flutter 에서 (리포트 §9 ④ — `EventSource` 없음)

| 항목 | 계약 |
|---|---|
| 연결 | `GET {API_BASE}/api/board/stream?token=<ccc 토큰>` 를 `http` 패키지 **스트림 요청**(`Client.send` → `StreamedResponse.stream`)으로. 헤더 `Accept: text/event-stream` · `Cache-Control: no-cache` |
| 파싱 | UTF-8 줄 단위 · 빈 줄 = 이벤트 끝. `event:` · `id:` · `data:`(여러 줄이면 `\n` 으로 이음) · `retry:`(ms · 재연결 간격) · `:` 로 시작 = 주석(ping) 무시. `event: board` 만 쓴다 |
| 첫 스냅샷 | 연결 직후 오는 `board` 하나로 첫 화면을 그린다(`GET /api/board` 따로 안 부름) — SPEC-003 §7.5 |
| version | 지금 가진 것보다 작거나 같으면 버린다. **새 연결의 첫 `board` 는 무조건 받는다**(back 재시작이면 version 이 0 부터 — 웹 `hooks.ts` 와 같음) |
| 재연결 | 끊기거나 오류면 `retry`(기본 3000ms) 뒤 다시. 연속 실패면 3s → 6s → 12s, 최대 30s(기본값). **45초 동안 아무 바이트도 안 오면 끊긴 것으로 보고 다시 연결**(back ping 15초 — 기본값) |
| 401 | 토큰 지우고 로그인 화면 |
| 앱 생명주기 | 백그라운드로 가면 스트림을 닫고, 앞으로 오면 다시 연결(첫 스냅샷으로 전부 바뀜) — 기본값 |
| 표시 | 연결 끊긴 동안 머리에 「연결 끊김 · 다시 연결 중」(값은 마지막 스냅샷 그대로) — 기본값 |

### 7.2 스냅샷 모양

SPEC-003 §7.2(0.3.0 부터 `procedures[].kind`(`procedure` \| `etc`) · `procedures[].kosStatus` 포함 — 코드가 정본) (0.3.0). 앱 `model/` 은 코드 `schemas/board.py` 의 필드 이름 · null 여부를 그대로 따른다. 모르는 필드는 무시(back 이 필드를 더해도 앱이 깨지지 않게).

### 7.3 API — 재사용 · 새것

| 구분 | API | 이 문서 |
|---|---|---|
| 재사용 | `GET /api/board/stream` · `GET /api/board`(디버그) · 조작 8종(SPEC-003 §7.3) · `GET /api/health` | 역할 검사만 더함(§3.4) |
| 바뀜 | `POST /api/auth/login`(`{id, password}` 필수 · +`role` · `name` · `staffId` · 429) · `GET /api/auth/me`(+`role` · `name` · `staffId`) · `POST /api/calls/{id}/accept`(`doctorId` 선택 · 선택 헤더 `X-Accept-Source`) (0.3.0) | §3.3 · §3.4 · §3.5 |
| 없앰 | ~~`GET /api/auth/accounts`~~ (0.3.0) | §3.3 · A-16 |
| 새것 | `WS /api/interpret` | §4 |
| 새것 | `POST /api/devices` · `DELETE /api/devices/{token}` (0.2.0) | §5-1.1 |
| 새 오류 코드 | 403 `role_forbidden` · `doctor_forbidden` · `not_your_call` · 429 `too_many_attempts` (0.3.0) | §3.3 · §3.4 |

- **back 경로 전부(코드 기준 16개 — router 15 + `GET /api/health`)**: `POST /api/auth/login` · `GET /api/auth/me` · `GET /api/board` · `GET /api/board/stream` · 조작 8(SPEC-003 §7.3) · `GET /api/health` · `WS /api/interpret` · `POST /api/devices` · `DELETE /api/devices/{token}` — 이 문서 · SPEC-003 표와 빠진 것 0 · 없는 것 0 (0.3.0)

- 앱은 Origin 을 보내지 않으므로 CORS 와 상관없다. 웹 CORS(`PROC_FRONT_ORIGIN`)는 그대로

## 8. 검증

### 8.1 back 단위 시험 (pytest · KOS · Soniox 가짜)

| 시험 | 내용 |
|---|---|
| 역할 행렬 | §3.4 표 전부 — **역할 3 × 조작 8**(마취 시작 · 종료 · 호출 · 다른 원장에게 · 수락 · 시작 · 종료 · 귀가 대기)의 허용 / 403 · 403 이 409 보다 먼저 · 403 때 DB · `event_log` · `kos_op` 변화 0 |
| 수락 | §3.4 수락 규칙 7줄 — doctor 본문 없음 · 같음 · 다름(403) · 남의 지정 호출(403) · 목록 밖(409) / admin `doctorId` 없음(400) · 지정 불일치(409) / nurse(403) |
| 토큰 | `role` · `staffId` claims · 비활성 · 없는 계정 · DB 역할과 다름 → 401 |
| 로그인 (0.3.0) | 맞는 비밀번호 200 · 틀림 · 없는 아이디 · 해시 없는 계정 · 비활성 = 같은 401 · 같은 아이디 5회 → 429 · 1분 뒤 풀림 · 성공하면 실패 수 지움 · 비밀번호 빠짐 400 · 해시는 env 가 그대로면 다시 안 만듦 · `GET /api/auth/accounts` 404 |
| 계정 | env 3개로 PoC 계정 3개(0.3.0) · env 비면 계정 없음 · 직원 조회 뒤 원장마다 doctor 행 · 목록에서 빠지면 `active=false` · `CCC_DOCTOR_KOS_ACCOUNT_ID` 가 목록 밖이면 카드 없음 |
| actor | 조작마다 `event_log.actor` = 로그인 `login_id` · 수락 payload `byRole` |
| 통역 | 복사한 `test_interpret.py` 전부 + 토큰 없음 · 틀림 → 핸드셰이크 거절 · 헤더 토큰 통과 · 쿼리 토큰 통과 · 다른 Origin 거절 · Origin 없음 + 토큰 = 통과 |
| SSE | 기존 시험 + 세 역할 토큰 모두 연결됨 |
| 푸시 (0.2.0) | (0.3.0 더함: 의사 수신자만 `category=CALL` · 관리자는 없음 · `push_log` 상태 4종 · 400 `BadDeviceToken` · `DeviceTokenNotForTopic` → 삭제 · `X-Accept-Source` → `call_accept.source`) **가짜 APNs**(요청을 받아 적는 가짜 · 응답 코드를 고를 수 있음)로 — ① 받는 사람: 지정 호출 = 그 원장 계정 토큰만 · 전체 호출 = 의사 계정 전원 토큰 · **관리자 토큰 = 전체 · 지정 모두 받음** · 간호사 토큰 0 · 호출한 의사 자신 제외 · **관리자가 누른 호출도 관리자 토큰에 감** · 비활성 의사 제외(0.2.0 · A-15) · `reassign-all` 도 발송 ② 내용: 본문 「<방> · 시술 N건 · 전체/지정 호출」 · 고객 이름 · 시술 이름 없음 · payload `visitId` · `callId` · 헤더 topic · push-type ③ 410 → `device` 행 삭제 · 5xx → 1회 재시도 뒤 멈춤 · ~~400 → 삭제 안 함~~ → 400 은 `reason` 이 죽은 토큰 3종일 때만 삭제(0.3.0) ④ `APNS_*` 비면 발송 0 · 조작 성공 ⑤ `POST/DELETE /api/devices` — 토큰 옮기기 · 남의 토큰 안 지움 ⑥ 로그에 토큰 전체 · JWT 0 |

### 8.2 앱 시험

- `flutter analyze` 0 · `flutter test` — SSE 파서(여러 줄 data · 주석 · retry · 끊긴 조각) · version 규칙 · 표시 매핑(`procLine` 등 웹과 같은 입력 → 같은 문구) · 「나에게 온 호출」 고르기 · 서버 주소 → ws/wss 변환 · release 에서 저장 주소 무시(0.3.0) · 로그인 401 · 429 문구(0.3.0)
- 화면 모양은 시뮬레이터 스크린샷(모바일 · 태블릿 × 목록 · 룸 상세 · 호출 시트 · 통역 드로어 · 로그인)

### 8.3 로컬 E2E (맥 · 시뮬레이터 + 웹)

준비 = SPEC-003 §9 와 같음(데모 KOS 4층 오늘 일정 · 시술 대기 · 방 배정). 웹(어드민) 브라우저 1 + 시뮬레이터 앱 2(간호사 · 의사)를 띄워 두고 매 단계 **세 화면이 새로고침 없이** 같이 바뀌는지 본다.

| # | 단계 | 확인 |
|---|---|---|
| 1 | 앱 로그인 — 아이디 · 비밀번호로 **관리자** · 의사 · 간호사 각각 · 틀린 비밀번호 401 · 웹 로그인 — 관리자 (0.3.0) | §3.3 · §3.6 · A-15 · A-16 |
| 2 | 간호사 앱: 방 카드 → 룸 상세 · [마취 시작] → 웹 카드 「마취 중」 | SSE |
| 3 | 간호사 앱: [의사 호출] → 시트 → 시술 2개 · 「모든 의사」 | 웹 · 의사 앱에 호출 · 의사 앱 「수락 대기 1」 |
| 4 | 간호사 앱에 [수락] 이 없다 · (시험 도구로) 간호사 토큰 수락 → 403 | A-08 |
| 5 | 의사 앱: 카드 [수락] → 두 시술 「<원장> 수락 · 시작 가능」 · 웹 호출 탭 0건 | A-07 · KOS 작업 `doctors` = 그 원장(A-13) |
| 6 | 웹(어드민)에서 다른 원장 지정 호출 → 의사 앱에 [수락] 안 보임 · 의사 토큰 수락 → 403 `not_your_call` · 웹에서 [다른 원장에게] → 의사 앱에 「전체 호출」로 [수락] 보임 | §3.4 |
| 7 | 의사 앱 [시작] → [종료] · 간호사 앱 나머지 [시작] → [종료] → 완료 상자 [귀가 대기] | 웹 카드 흐림 · KOS `PROCEDURE_DONE` |
| 8 | `event_log.actor` 가 단계마다 누른 계정 | §3.5 |
| 9 | 통역(시뮬레이터 · 맥 마이크): 드로어 열기 → 한국어 · 고객 언어 한 마디씩 → 자막 양쪽 · 번역 음성 재생 · 언어 바꾸기 · [종료] | §4 |
| 10 | 빠른 말하기 칩 6개 × 언어 2개 이상 읽기 | §5 |
| 11 | back 재시작 → 앱 · 웹 다시 붙고 같은 상태 | §7.1 |

### 8.4 아이폰 · 아이패드 실기기 E2E — **완료 조건**

TestFlight 로 설치한 앱 · ~~서버 주소 = 맥 IP(A-11) · 맥에서 back(compose)~~ → **배포 back `https://ccc.medisolveai.xyz`**(A-20) (0.3.0).

| # | 확인 | 완료 조건 |
|---|---|---|
| D1 | 첫 실행 → 아이디 · 비밀번호 로그인(서버 주소 칸 없음) (0.3.0) | 아이폰 · 아이패드 각 1회 |
| D2 | §8.3 의 2 ~ 7 을 **아이폰(간호사) · 아이패드(의사 또는 간호사) · 맥 웹(어드민)** 로 | 세 화면 실시간 · 권한(수락 403 1회 포함) |
| D3 | **마이크 권한** 허용 → 통역 실발화(한국어 ↔ 고객 언어 1쌍 이상) → **번역 음성이 기기 스피커로 재생** | 아이폰 · 아이패드 각 1회 |
| D4 | 빠른 말하기 — 기기 TTS 재생(언어 2개 이상 · tl 음성 유무 기록) | 각 1회 |
| D5 | 앱을 백그라운드 → 앞으로 → SSE 다시 붙음 | 1회 |
| D6 | **원장 호출 푸시**(0.2.0): TestFlight 아이폰을 의사 계정으로 로그인 · 알림 허용 → 잠금 · 다른 앱 상태에서 간호사(아이패드 또는 웹)가 ① 전체 호출 ② 그 원장 지정 호출 → 아이폰 잠금 화면에 「<방> · 시술 N건 · 전체/지정 호출」 · 소리 · 고객 이름 없음 → 알림을 누르면 그 방 룸 상세 → [수락]. 다른 원장 지정 호출은 안 옴. 로그아웃 뒤 호출 → 안 옴. **관리자 계정**(아이패드 또는 같은 아이폰 다시 로그인): 다른 원장 지정 호출 · 웹(관리자)에서 누른 호출도 옴 → 누르면 룸 상세 → 원장 골라 [수락](0.2.0 · A-15) | 아이폰 1회씩(①②③ 로그아웃) + 관리자 1회 — `APNS_ENV=production` |
| D7 | **알림 [수락]**(0.3.0 · A-17): 의사 계정 아이폰 잠금 화면 알림을 길게 눌러 [수락] → 로컬 알림 「수락했어요 · <방>」 · 웹 호출 탭에서 사라짐 · `call_accept.source = push` / 같은 알림을 **Apple Watch** 에서 [수락] | 아이폰 1회 · 워치 1회 |

- 이 표를 사용자가 기기에서 본 것이 완료다(시뮬레이터 · 웹 확인으로 대신하지 않는다)
- **기록된 결과**(2026-10-21 · 빌드 1 ~ 2): 아이폰 · 아이패드 설치 · 로그인 · 목록 · 룸 상세 화면을 사용자가 봄 → 피드백 T1 ~ T8(모두 코드 반영 · main 329b543). 알림 [수락] = mobile 워커가 실 back 200 · 실 APNs 로 확인(`_RESUME` §3 mobile 줄). **D3(통역 실음성 · 기기 스피커) · D7 워치는 결과 기록 없음** → §9 OQ-616 · OQ-617. 빌드 3(정상 로그인 반영 · 업로드됨 — PR #5)의 기기 설치 · 확인은 기록 없음 (0.3.0)

### 8.5 배포 뒤 축약 (A-12 · A-20)

**코디 확인 기록(2026-10-21 · 배포 이미지 0f4634a)**: back/front Running · ArgoCD Synced Healthy · 카드 7 · KOS 공개/내부 토큰 true · SSE 첫 접속 + 10초마다 · 통역 wss 토큰 있음 열림 / 없음 403 · APNs JWT OK(production). Cloudflare 가 Python 기본 UA 를 403(Dart UA 는 200). 정상 로그인 이미지 329b543 은 infra #24 로 올림 (0.3.0) — `_RESUME` 10-21 배포 완료 줄 · infra #22 ~ #24


- 웹 `https://ccc.medisolveai.xyz`: 어드민 로그인 · 카드 · SSE 갱신 · 의국 수락
- 앱: ~~서버 주소를 바꿔~~ TestFlight(배포 주소 빌드)로 로그인 · SSE (0.3.0) · **통역 `wss` 실발화 1회** · 수락 403 1회 · **푸시 1회**(배포 back 의 `APNS_*` = Secret · production) (0.2.0)
- SSE · 통역 WS 가 **유휴 2분 넘게 안 끊김**(SSE ping 15초 · 통역 keepalive) · SSE 가 버퍼링 없이 바로 옴

## 9. 열린 것

| ID | 질문 | 지금(기본값) | 상태 |
|---|---|---|---|
| ~~OQ-601~~ | 로그인 접근 제한 — 카드 선택만으로 배포 주소에 들어올 수 있다 | **닫힘(A-16)** — 정상 로그인(아이디 + 비밀번호 · bcrypt · 계정 목록 API 제거 · 5회/1분 잠금) · §3.3 | 닫힘 (0.3.0) |
| OQ-602 | [다른 원장에게](`reassign-all`) · [다른 의사 호출]의 역할 — 결정 줄은 「마취 · 호출 · 시작 · 종료 · 귀가 대기」만 적음 | 세 역할 모두(「호출」로 봄) | 새로 |
| OQ-603 | 간호사 계정 전원의 원천 — KOS `getAccounts` 의 간호사 역할 태그(번호 미확인) 또는 ccc 에서 직접 | PoC = env 간호사 1명 | 새로 |
| ~~OQ-604~~ | KOS `visitor.nationality` 값 형식(ISO 두 글자인지) — 자동 언어(§4.4) 가 맞나 | **닫힘** — 데모 지점에 ISO 두 글자(KR · CN · TW · JP · US 등)로 만든 데모 고객 190건을 KOS 재조회로 국적 불일치 0 확인 → 표 그대로 | 닫힘 (0.3.0 — `demo-patients-2026-10-22.md`) |
| ~~OQ-605~~ | 번들 id · 앱 이름 · 아이콘 | **닫힘** — 번들 id = 사용자 등록(A-19 · 값은 레포 밖) · 이름 「시술 현황」 · 아이콘 = Ceramique 로고 「C」(A7) | 닫힘 (0.3.0) |
| OQ-606 | 빠른 말하기 번역(zh 번체 · ja 외) 원어민 검수 · th 화자 어미 | 이 SPEC 초안 그대로 | 새로 |
| OQ-607 | iOS 기기에 tl(타갈로그) · hi TTS 음성이 있나 | 없으면 토스트 · 대체 없음 | 새로 · 기기 E2E 에서 기록 |
| OQ-608 | 의사 계정 로그인 카드를 둘 이상(원장 여럿 시연) | PoC 1명 | 새로 |
| ~~OQ-609~~ | 어드민이 앱에서 수락(원장 고르기) | **닫힘(A-15)** — 앱에서도 원장을 골라 수락(§6.2 · §6.3 #2) | 닫힘 (0.2.0) |
| OQ-610 | 시안의 「누가 호출했나」 표시(N5 · X18) — 계정이 생겼으니 스냅샷 `call` 에 `actorName` 을 싣나 | 싣지 않음(로그만) | 새로 |
| ~~OQ-611~~ | SPEC-003 §1.2(개인 계정 · 앱 수락 Out) · §7.1(관리자 1개) · §7.2(`kind` · `kosStatus` 없음) 이 이 문서 · 코드와 어긋남 | **닫힘** — SPEC-003 0.3.0 이 같이 고쳤다 | 닫힘 (0.3.0) |
| ~~OQ-613~~ | **APNs 인증 키 준비** — Apple Developer 에서 `.p8` 키 만들기(Key ID) · 팀 id · 번들 id · App ID Push 켜기 · 로컬은 레포 밖 파일 · 배포는 Secret | **닫힘(A-19)** — 키(Sandbox & Production · Team Scoped) · 로컬 back JWT 서명 OK · 배포 Secret `cc-prototype-apns` → `/etc/apns/apns.p8` · 배포 APNs JWT OK(production) | 닫힘 (0.3.0) |
| OQ-614 | sandbox · production 섞임 — Xcode 로 직접 설치한 앱(sandbox 토큰)과 TestFlight(production)가 한 back 에 섞이면 한쪽은 400 `BadDeviceToken` | `APNS_ENV` 하나 · 실기기 확인은 TestFlight(production)만. ~~400 은 로그만~~ → **코드는 400 `BadDeviceToken` · `DeviceTokenNotForTopic` · `Unregistered` 를 죽은 토큰으로 보고 `device` 행을 지운다**(§5-1.2) — 섞인 쪽 기기는 다음 로그인 · 앱 시작 때 다시 등록 | 코드 기준으로 바뀜 (0.3.0) |
| OQ-615 | 호출이 수락 · 재호출되면 이미 간 알림을 지우나(다른 원장 폰에 남은 전체 호출 알림) | 지우지 않음 — 누르면 그 방 상세에서 지금 상태(이미 수락이면 [수락] 없음) | 새로 (0.2.0) |
| OQ-612 | 통역 동시 세션 한도(Soniox TTS 동시 3) — 기기 여러 대가 동시에 열면 | 제한 없음 · 넘으면 `soniox_unavailable` 표시 | 새로 |
| OQ-616 | **실기기 Apple Watch 알림 [수락]**(A-17) 확인 | 아이폰 알림 액션이 워치에 그대로 보인다는 전제 · 결과 기록 없음 — §8.4 D7 | 열림 — 사용자 기기 (0.3.0) |
| OQ-617 | **통역 실음성 기기 확인**(§8.4 D3 — 실발화 · 번역 음성 기기 스피커) | 실 Soniox 는 back 시험 스크립트 1회(WORK-004 WP2) · 배포 wss 연결 확인만 · 기기 실음성 결과 기록 없음 | 열림 — 사용자 기기 (0.3.0) |
| OQ-618 | 빌드 3(정상 로그인 · T1 ~ T8) 기기 설치 · 확인 | 업로드됨(`1.0.0+3` · 코드 PR #5 OPEN) · 기기 확인 기록 없음 · PR #5 머지 전엔 main 이 `+1` | 열림 — 사용자 기기 · PR #5 머지 (0.3.0) |

## 부록 A. 결정 대응표

| 근거 | 내용(줄임) | SPEC-004 |
|---|---|---|
| A-01 | Flutter PoC 앱 · 서버 = `procedure/back` | §1.1 · §2.1 · §6 |
| A-02 | 로직 정본 = 구현 코드 · 시안 로직 버림 | §1.2 · §3.4 · §6.0 · §6.2 ~ §6.4 · §6.7 #1 ~ #5 · §7.2 |
| A-03 | 계정 3종 · 카드 3 · DB 사람마다 · 웹은 어드민 | §1.1 · §2.3 · §3.1 ~ §3.3 · §3.6 · §6.1 · §6.7 #6 · #7 · #13 |
| A-04 | 통역 복사 · 언어 8 | §1.1 · §2.3 · §4 · §6.5 · §6.7 #8 |
| A-05 | 빠른 말하기 6 하드코딩 | §1.2 · §5 · §6.3 #7 |
| A-06 | 동의서 · 시술 메모 · 다시 알림 · 간호사 요청 · 빈 방 뺌 | §1.2 · §6.7 #2 · #9 |
| A-07 | 의사 = 자기 자신으로 수락 | §3.4 · §6.2 · §6.3 #2 · §6.7 #3 · #6 |
| A-08 | 권한 back 검사 · 역할 + 원장 id · 403 · actor · 실제 원장 · 단위 시험 | §2.3 · §3.2 ~ §3.5 · §4.2 · §8.1 · §8.3 #4 · #6 · #8 |
| A-09 | 로컬 + 아이폰 + 아이패드 · TestFlight | §1.1 · §2.4 · §8.3 · §8.4 |
| A-10 | `procedure/app/` | §1.1 · §2.1 |
| A-11 | 기기 back = 맥 IP · ATS · 로컬 네트워크 · 0.0.0.0 · 방화벽 · 주소 입력칸 | §2.2 · §2.4 · §6.1 · §8.4 |
| A-12 | 최종 배포 · wss · SSE ingress · Secret · `_archive/cc` · `procedure-*` | §1.1 · §2.2 · §2.3 · §8.5 · WORK-004 마지막 WP |
| A-13 | (사실) 다른 원장 id 로 수락 KOS 200 | §3.4(admin 수락) · §8.3 #5 |
| A-15 | 관리자도 모든 호출 푸시 · 앱 카드에 관리자 · 앱에서도 원장 골라 수락 (0.2.0) | §5-1.1 · §5-1.2 받는 사람 규칙 · §6.0 · §6.1 · §6.2 · §6.3 #2 · §6.7 #6 · §8.1 푸시 ① · §8.3 #1 · §8.4 D6 · OQ-609 닫힘 |
| A-14 | 원장 호출 푸시 · APNs 직접 · 받을 원장 · 룸 상세로 · 로그인 때 토큰 · 키 레포 밖 (0.2.0) | §1.1 · §1.2 · §2.3 · §2.4 · §5-1 · §6.1 · §7.3 · §8.1 · §8.4 D6 · §8.5 · OQ-613 ~ 615 |
| A-16 | 정상 로그인 · 목록 API 제거 · bcrypt · 5회/1분 · env 비밀번호 (0.3.0) | §1.1 · §2.3 · §3.1 · §3.3 · §3.6 · §6.1 · §7.3 · §8.1 · §8.3 #1 · §8.4 D1 · OQ-601 닫힘 |
| A-17 | 알림 [수락] · `CALL` · 워치 · 로컬 알림 결과 (0.3.0) | §1.1 · §2.4 · §3.2 · §5-1.2 · §5-1.3 · §8.4 D7 · OQ-616 |
| A-18 | `push_log` · `X-Accept-Source` (0.3.0) | §3.5 · §5-1.2 · §7.3 · §8.1 |
| A-19 | Apple 번들 · 앱 레코드 · APNs 키 (0.3.0) | §2.4 · OQ-605 · OQ-613 닫힘 |
| A-20 | 배포 먼저 · 앱 = 배포 주소 · 서버 주소 칸 debug 만 (0.3.0) | §0(A-11 · A-12 고침) · §1.1 · §2.2 · §2.4 · §6.1 · §6.7 #13 · §8.4 · §8.5 |
| U1 ~ U5 · §9-1 · §9-2 | 리포트 §9 | 각각 A-01 ~ A-05 · A-08 · A-09 · A-11 |

누락 0.

## 부록 B. 앱 · 실기기 피드백 반영표 (0.3.0)

원천 `orchestration/work/myeongdong-poc-v2/e2e-app-feedback-batch-1.md`(A1 ~ A7 · 시뮬레이터) · `e2e-device-feedback-batch-1.md`(T1 ~ T8 · TestFlight 빌드 1 ~ 2). 코드 = main `329b543`.

| # | 처분 | SPEC-004 |
|---|---|---|
| A1 | 목록 카드 상태 배지 오른쪽 끝 · 좌우 여백 같게 | §6.2 카드 |
| A2 | 호출 시트 「호출할 시술」 [전체 선택](pickable 만) | §6.4 |
| A3 | 토스트 = 화면 위 · Material 안(노란 밑줄 없음) · 웹 · 앱 같은 규칙 | §6.0 |
| A4 | 룸 상세 머리 배지 · 시각 오른쪽 끝 | §6.3 |
| A5 | 룸 상세 = 오더 메모 → 마취 → 시술 · 지금 할 일 맨 위 · 태블릿도 | §6.3 |
| A6 | 머리 배지 문구 잘리지 않게 | §6.3 |
| A7 | 앱 아이콘 = Ceramique 로고 「C」(1024 · 알파 없음) | §2.4 · OQ-605 |
| T1 | 태블릿 두 열 = 화면 끝까지(오더 메모 · 시술 카드 늘어남 · 버튼 줄 바닥) | §6.3 |
| T2 | 태블릿 머리 한 줄 | §6.3 |
| T3 | 오더 메모 글자 키움(태블릿 시안 크기 · 모바일 한 단계) | §6.3 |
| T4 | 반응형 글자 배율(짧은 변 / 700 · 1.15 ~ 1.3) | §6.0 · §6.2 |
| T5 | 필터 = 맞는 카드만 · 왼쪽 위부터 · 「귀가」 칩 | §6.2 · §6.7 #5 |
| T6 | `canCall` = pickable 시술 ≥ 1(back) | SPEC-003 §5.11 |
| T7 | 통역 바 칩 줄 끝 페이드 | §6.3 #7 |
| T8 | 서버 주소 칸 · [연결 확인] debug 만 · release 는 `API_BASE` 고정 · 저장 주소 무시 | §2.2 · §6.1 · A-20 |

누락 0.
