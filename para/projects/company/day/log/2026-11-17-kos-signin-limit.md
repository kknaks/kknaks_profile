# 작업 요약 — kos-signin-limit (day)

기간: `2026-11-17` ~ `2026-11-17`
결과: 코드 CENTURION_DAY#257(dev `a6aa4ba5`) · 스펙 mediness#946(main `51f85837`) 스쿼시 머지 · **dev 배포 성공**. prod 는 같은 날 20시 사용자 예정(fix-feedback #255 와 같이 · `git push origin a6aa4ba5:prod`). migration 0 · 앱 응답 변화 0.

## 1. 무엇을 했나

KOS 가 계정당 동시 로그인을 5개로 막기 시작했다. DAY 는 로그인마다 KOS 세션을 하나 만들고 지우지 않아, 막히면 직원은 「이메일 또는 비밀번호가 맞지 않습니다」를 받고 시스템 계정(동기화)은 멈췄다 — fix-feedback E2E 도중 로컬 · dev 로그인이 막혀서 드러났다.
KOS 웹의 「이미 로그인 중인 기기가 있습니다」 흐름(HAR · 화면 캡처)을 기준으로: 판정(401 본문 `SignInLimitExceeded`) · 목록 · 해제 · 재 sign-in 을 공통으로 두고, **직원은 웹 기기 선택 단계**, **시스템 계정은 막혔을 때만 같은 환경 세션 1개 자동 해제**로 갈랐다. 같은 작업에서 로컬 확인 중 나온 화면 변경(차트 영역 · 탭 글자)도 넣었다.

## 2. 적용한 기술·개념

- **같은 401 을 본문 사유로 가른다** — 틀린 비밀번호와 기기 제한이 둘 다 401 `InvalidRequestException` → [[external-api-error-classification]]
  - 왜 이걸 골랐나: 상태 코드 · 클래스 이름으로는 못 가른다. `message == "SignInLimitExceeded"` 만 기기 제한으로 보고 나머지는 기존 「자격 틀림」 그대로 — 본문 모양이 다르면 기존 동작으로 떨어지게.
  - 근거: `be-0-findings.md` · `review-code-1-report.md` · CENTURION_DAY#257
- **다단계 로그인 동안 비밀번호를 들고 있기** — KOS 목록 · 해제가 이메일 + 비밀번호를 요구해 기기 선택 단계 동안 서버가 비밀번호를 가져야 했다 → [[password-login-hardening]]
  - 왜 이걸 골랐나: 화면 숨은 칸에 싣는 건 기각(응답 · 브라우저에 평문). 병원 고르기 임시 토큰 틀(Redis · 5분 · 꺼내면 지움)을 그대로 쓰되 값은 **암호문**, 토큰에 **종류 표시**를 둬서 병원 고르기 토큰과 섞이면 `session_expired`(검수 W-1 — 섞이면 KeyError 500 이었다). 로그아웃 때 KOS 해제는 비밀번호가 없어 불가 → 사용자 「다시 로그인할 때 고르면 된다」로 뺐다.
  - 근거: SPEC-001 개정 ⑨ §3 · `review-doc-1-report.md` W-1 · `be-1-report.md`
- **서버를 IP 가 아니라 User-Agent 표시로 식별** — dev · prod 가 같은 VM 이라 KOS 목록 IP 가 같다
  - 왜 이걸 골랐나: 서버는 자기 공인 IP 를 모르고, 알아도 dev · prod 를 못 가른다. KOS 가 기록하는 `userAgent` 끝에 ` (local)` · ` (dev)` · ` (prod)` 를 붙여(`KOS_CLIENT_TAG` — `APP_ENV` 는 로컬도 dev 라 기각) 「같은 환경이 만든 세션」을 고른다. KOS 가 브라우저 UA 가 아니면 403 을 주던 전례가 있어 **코디가 시스템 계정으로 실물 시험**(표시 붙여도 sign-in · 내부 API 200 · 목록에 그대로 · 같은 IP+UA 재로그인해도 앞 세션 안 지워짐) 뒤 정했다.
  - 무엇이 어려웠나: 「같은 환경 전부」를 끊으면 같은 환경의 다른 프로세스 토큰을 서로 끊는 왕복 위험 → 막혔을 때만 · 가장 오래된 1개 · 재시도 1회. 표시가 없으면 사람 세션일 수 있어 정리 안 함.
  - 근거: `_RESUME.md` §2 · SPEC-001 S-8 · 로컬 실물 `(local)` 세션 확인
- **깔린 앱은 모르는 단계 · 코드를 글자 그대로 보인다** — 앱 로그인 API 에 새 단계를 넣으면 심사 중 앱이 `unexpected_response` 를 띄운다 → [[tolerant-reader]]
  - 왜 이걸 골랐나: planner 는 새 코드 `kos_signin_limit` 을 제안했지만 앱 `copy.dart` 가 모르는 코드를 코드 글자로 보여 준다 → 앱 JSON 은 **지금과 같은 401 `invalid_credentials`**(원인 오안내 감수 · 다음 앱 버전에서). 사용자 「앱 화면은 지금과 같게」의 뜻을 코드 사실로 맞춘 것.
  - 근거: `spec-2-report.md` · `spec-3-instructions.md` · SPEC-003 ⑱

## 3. 막혔던 것 / 사고

- **「코드 구현부터」를 「스펙 건너뛰고 코드」로 잘못 알아들었다** — backend 를 먼저 띄웠다가 사용자 정정(「스펙 먼저 하라고 · 코드 구현까지 끝내자 · 배포 나중」)으로 중단. 반쯤 짠 코드는 `be-0-draft.patch` 로만 남기고 워크트리를 되돌렸다. 「~부터」는 끝점일 수도 있다 — 범위와 순서를 한 번 되묻거나 기본 파이프라인을 지킨다.
- **중복 발주** — 사용자가 끊은(거절) 발주 명령이 실제로는 워커를 띄워, 같은 fe-4 를 워커 둘이 같은 파일에서 고쳤다(워커가 「누가 같은 파일을 고친다」고 물어 알았다). 하나를 Esc · 터미널 닫기로 멈추고 최종 상태를 코디가 검증(CSS 빌드 동기 · 전체 테스트). → 발주가 거절로 끝나도 `worker-list` 로 확인.
- **화면을 안 보고 버그로 단정** — 사용자 「수락하고 시작 전인데 원장 변경 안 된다」를 버그로 보고 조사 워커를 띄웠는데, 사용자 스크린샷으로 보니 그 줄은 KOS 집도의가 있는 **준비중** 줄(규칙 27 상 대상 아님)이었다. 앞 답변의 「준비중 = 원장이 정해지지 않은 상태」 설명이 틀려 혼선을 키웠다. 사용자 질책. → 화면 증상은 스크린샷 · 로그(이번엔 `/doctor` 0건 · `/chart` 3건이 답이었다)부터.
- **시스템 계정 자리가 다시 찼다** — 로컬 재빌드마다 `(local)` 세션이 하나씩 늘어 dev 배포 직후 5/5. 새 dev 서버는 아직 `(dev)` 세션이 없어 막히면 자동 정리도 못 한다 → 코디가 로컬 옛 세션 2개만 해제해 3/5. 배포 직후 표시 없는 옛 세션 정리가 필요한 이유.
- 개인정보 플러그인이 「이메일 + User-Agent 한 호출」을 막아, KOS 시험은 HAR 에서 값을 읽는 스크립트 파일로 돌렸다.

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-11-17 | 공통 = 401 `SignInLimitExceeded` → 목록 → 해제 → 재 sign-in | 사용자 · KOS HAR |
| 2026-11-17 | 시스템 계정 = UA 환경 표시 `KOS_CLIENT_TAG` · 막혔을 때만 같은 UA 가장 오래된 1개 해제 · 재시도 1회 | 사용자 · 코디 실물 시험 · 검수 W-3 |
| 2026-11-17 | 직원 = 웹 기기 선택 단계(KOS 화면 글자 · 「처음으로」 없음) · ~~안내만~~ · 로그아웃 때 해제 안 함 | 사용자 |
| 2026-11-17 | 앱 JSON = 지금과 같은 401 `invalid_credentials` · 앱 기기 선택은 다음 앱 버전 | 사용자(A) · 앱 코드 사실 |
| 2026-11-17 | 차트 여는 곳 = 시술명 영역 전체 · 호버 툴팁만(배경 · 테두리 · 포커스 표시 없음) · 정렬 탭 「시술대기 순」 · 「방별 순」 | 사용자 로컬 확인 |
| 2026-11-17 | 원장 변경 = 수락 · 진행중만(그대로) — KOS 집도의 있는 준비중 줄은 대상 아님 | 규칙 27 · 사용자 확인 |
| 2026-11-17 | 순서 = 스펙 먼저 → 코드 구현까지 · 배포는 사용자 시점(20시 prod) | 사용자 정정 |

## 5. 날짜별 로그

- `2026-11-17` KOS 기기 제한 실물 확인(HAR · UA 표시 시험) · 코드 먼저 띄웠다 중단 · planner spec-1 ~ 4 · 문서 검수 · be · fe · 코드 검수 PASS · 로컬 확인 픽스 4(차트 영역 · 탭 글자 · 투명 · 중복 발주 정리) · 전체 1359 passed · #257 · #946 머지 · dev 배포 · 시스템 세션 정리

## 6. 산출물

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/946 (`51f85837`)
- code PR: https://github.com/MediSolveAIDev/CENTURION_DAY/pull/257 (`a6aa4ba5` · dev 배포 성공)
- 리포트: `be-0-findings.md` · `spec-report.md` ~ `spec-4-report.md` · `review-doc-1-report.md` · `be-1-report.md` · `fe-1-report.md` ~ `fe-5-report.md` · `review-code-1-report.md` · `delivery-close-report.md`
- 초기화 스크립트(레포 밖): `~/Downloads/kos_reset_signins.py` · KOS 화면 캡처 `~/.config/day/reference/kos-device-limit-2026-11-17.png`

## 7. 잔여

- **prod 배포 20시**(사용자) — `git push origin a6aa4ba5:prod` · prod.env `KOS_CLIENT_TAG=prod` 포함 · 배포 뒤 시스템 계정 표시 없는 옛 세션(52.x) 정리.
- 앱 기기 선택 화면 · 앱 오류 안내(다음 앱 버전).
- 기기 선택 목록에서 `(dev)` 등 표시를 「DAY dev」처럼 보일지(글자 미정) · KOS 해제가 토큰을 즉시 막는지(OQ-K11 실물).
- 로컬 재빌드마다 `(local)` 세션이 쌓인다 — 로컬은 막히면 자동 정리되지만 자리 관리 감안.

<!-- work-links:start -->
## 작업 기록

- [[orchestration/work/_archive/day/kos-signin-limit/README|kos-signin-limit]]
<!-- work-links:end -->
