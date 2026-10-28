---
type: work
id: WORK-010
title: "고객 문진 웹 — 공개 페이지 · 토큰 링크 · 공개 API(BE4 재사용) · 데스크 웹 QR · 직원 앱 QR 화면 · 앱 문진 화면 빼기 · 고객 폰 E2E"
status: draft
product: cc-prototype
feature: procedure
work_type: enhancement
owner: kknaks
progress: 0
created_at: 2026-10-28
updated_at: 2026-10-28
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/work
  - status/draft
links:
  baselines:
    - "[[baseline-009-reservation-board|BASE-009]]"
  decisions:
    - "[[decision-008-customer-questionnaire-web|DEC-008]]"
    - "[[decision-007-app-v2|DEC-007]]"
  specs:
    - "[[spec-006-customer-questionnaire-web|SPEC-006]]"
    - "[[spec-004-procedure-app|SPEC-004]]"
    - "[[spec-005-reservation-board|SPEC-005]]"
  works:
    - "[[work-009-app-v2|WORK-009]]"
  releases: []
  related: []
sources:
  - "orchestration/work/overall-board/_RESUME.md §2 (2026-10-27 「문진 = 고객이 웹에서」 · 2026-10-28 「문진 다시 하기 착수」) · §1 「문진 다시 하기」"
  - "cc-prototype procedure/ main affac41 (읽기만 — back service/questionnaire.py · service/display.py · api/questionnaire.py · app lib/screens/questionnaire_screen.dart · launchers.dart · front components/reservations/Display.tsx)"
---

# 고객 문진 웹 — 빌드 계획

계약은 **SPEC-006 0.1.0**(전부) + SPEC-004 0.4.2(§5-3 · §6.10 · §6.11 · §6.15 · §6.17 · §7.3 · §7.4 바뀐 줄) + SPEC-005 0.4.1(§6.6 · §6.8 #10 바뀐 줄) — 이 문서는 빌드 계획만 적고 계약을 다시 쓰지 않는다. 결정 = DEC-008.

## Meta

- Covers spec: SPEC-006 0.1.0 · SPEC-004 0.4.2(문진 줄) · SPEC-005 0.4.1(QR 상자 줄)
- 코드 레포: `kknaksss/cc-prototype` — 범위 **`procedure/back/**` · `procedure/front/**` · `procedure/app/**`**(문진 · 띄우기 몫만). infra 레포 `MediSolveAIDev/k8s_infra_mac` — env 한 줄(`PROC_QWEB_FILL_MIN` 은 기본값이라 운영 Secret · ConfigMap 변경 없음 — 바꾸지 않으면 infra PR 없음)
- base: 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` · 브랜치는 코디가 정한다(지금 main = 운영 `affac41`). **DEC-008 D-08**: ① 앱 판 뒤에 착수 — 앱 판(WORK-009)의 BE3 · BE4 · APP4 · APP5 코드가 이 판의 출발점
- 워커: backend · frontend · mobile · reviewer · 코디(E2E · 배포)
- 검증은 WP 마다 그 범위만. 전체 검증(pytest 전부 · front build · `flutter build ipa` · compose)은 WP-E2E 에서 한 번
- **완료 = 사용자가 배포 주소에서 자기 폰(고객 역할)으로 SPEC-006 §10.3 Q1 ~ Q7 을 본 것**(로컬 · 시뮬레이터 · 데스크 브라우저로 대신하지 않는다 — 고객 폰 카메라 · Safari 가 표면)
- 데모 지점에만 쓴다 · public — 실명 · KOS id · 키 · 토큰 · QR 이미지 · 주소창 금지

## 계약 고정점

| 고정점 | 값 | SPEC-006 |
|---|---|---|
| 주소 | `{PROC_FRONT_ORIGIN}/q#<token>` · front `app/q/page.tsx` · `(main)` 밖 · `lib/publicApi.ts`(직원 세션 안 읽음) | §2 |
| 토큰 | HMAC(`PROC_SESSION_SECRET`, `q|{id}|{nonce}`) · DB = `qr_nonce` · `qr_token_hash` · 문진 종류만(스캔 그대로) | §3.1 |
| 시한 | 여는 10분(`PROC_DISPLAY_TTL_MIN`) · 쓰는 60분(`PROC_QWEB_FILL_MIN` 새) · `opened` = 고객이 엶 | §3.2 |
| 공개 API | `GET` · `POST /api/public/questionnaire` · 헤더 `X-Questionnaire-Token` · 오류 `q_token_missing` · `q_not_found` · `q_expired` · `q_canceled` · `q_submitted` · `q_submitting` · `too_many_requests` | §6.1 · §5 |
| 없앰 | `GET` · `POST /api/questionnaires/{reservationId}` · `POST /api/auth/unlock`(OQ-802) · 앱 문진 화면 · 잠금 | §6.2 · §8.2 |
| 경로 | 지금 50 − 3 + 2 = **49**(`test_route_count_49`) | §6.7 |
| 이력 | `questionnaire_history.source = web_submit` · 같은 제출본 `read` 행 고침 | §6.4 |
| 링크 싣는 곳 | 로그인 응답만 — create · SSE `display` · pending · 상세 `displays[]` 의 `qrUrl` · 푸시 payload 엔 없음 | §6.6 |
| 법적 검토 주석 | 3곳(공개 API 머리 · 페이지 머리 · 이력 표) | §7.6 |

## Work Packages

| WP | 내용 | 계약 | 워커 | 대상 파일(범위) | 완료 조건 | 검증 명령(부분) | 상태 |
|---|---|---|---|---|---|---|---|
| **WP-BE** | **공개 문진 · 토큰** — `display_request.qr_nonce` 열 · 문진 종류 토큰 HMAC · `qrUrl`(create · SSE `display` · pending · 상세 `displays[]` + `openedAt`) · 문진 종류 pending 은 `opened` 로 안 바꿈 · claim 에 문진 토큰 404 · 새 요청이 `pending` · `opened` 둘 다 닫음 · 쓰는 시한 만료 · **공개 router `api/public_questionnaire.py`**(헤더 토큰 · `Authorization` 무시 · 가짜 판 403 · `no-store`) · `QuestionnaireService` 「누가」 바꾸기(`public_target` · `load_for` · `submit_for` · 양식 읽기 · 미리 채움 · 제출 세 함수 — §9 자리) · 겹친 제출 잠금 · 속도 제한(메모리 · IP 헤더는 운영 ingress 확인 후 한 곳) · `event_log` `qweb_open` · `qweb_denied` · actor `customer` · 이력 `web_submit` · 직원 문진 경로 2 · unlock 없앰 · CORS `allow_headers` · `.env.example` 한 줄 · **법적 검토 주석 ①③** · 로그에 토큰 0 · 경로 49 | SPEC-006 §3 · §6 · §7 · §11 | backend | `procedure/back/app/{api/public_questionnaire.py(새),api/questionnaire.py(지움),api/auth.py,api/display.py,service/questionnaire.py,service/display.py,service/auth.py,repository/db.py,repository/repo.py,schemas/*.py,main.py,config.py}` · `tests/` · `procedure/.env.example` | SPEC-006 §10.1 전부 통과 · `grep -rn "법적 검토 필요" procedure/back` ≥ 2(이 판 몫) · 데모 지점 공개 `POST` 1회(시험 고객 · 코디 허가 뒤) | `uv run ruff check . && uv run pytest -q -k "questionnaire or display or route_count or rate"` | 대기 |
| **WP-FE** | **고객 페이지 · 데스크 QR 상자** — `app/q/page.tsx`(단계 ①~⑦ · 언어 칩 6 · KOS 양식 렌더(`CHECK_BOX` · `SELECT_BOX` · `INPUT_BOX` · `subText`) · 미리 채움 · 동의(`ja · en · zh` 키) · 오류 화면 7 · 브라우저 언어) · `lib/publicApi.ts` · `lib/q/text.ts`(앱 문구 6언어 옮김) · 메타(noindex · no-referrer) · **법적 검토 주석 ②** · `components/reservations/Display.tsx` 문진 몫(QR = `qrUrl` · 단계 pending → opened 「고객이 입력 중」 → done · 만료 [다시 만들기] · 오늘 이미 제출 안내 · 새로고침 때 `displays[].qrUrl`) · `lib/types.ts` | SPEC-006 §2 · §4 · §5 · §8.1 · SPEC-005 0.4.1 §6.6 | frontend | `procedure/front/{app/q/page.tsx(새),lib/publicApi.ts(새),lib/q/*(새),components/q/*(새),components/reservations/Display.tsx,lib/types.ts,lib/api.ts}` | 로컬(가짜 back 응답 또는 WP-BE 뒤 compose)에서 모바일 폭 ①~⑦ · 오류 화면 · 데스크 상자 단계 스크린샷(토큰 · QR 가림) · 예약 현황 그 밖 화면 회귀 없음 | `cd procedure/front && npx tsc --noEmit && npm run lint && npm run build` | 대기 (WP-BE 계약 고정점만 보고 화면 먼저 · 붙이기는 WP-BE 뒤) |
| **WP-APP** | **QR 화면 · 문진 화면 빼기** — 띄우기 `kind:"questionnaire"` = QR 화면(새 · `qrUrl` · 남은 시간 · 5초 상세 폴링으로 `pending` 아니면 닫힘 · [닫기] = 화면만 · 꺼짐 막기) · `pending` 문진 항목은 `status = pending` 만 연다 · 예약 상세 [이 기기에서 열기] → **[이 기기에 QR 보이기]** · [QR 읽기] 는 `ccc://` 만(https = 토스트) · **지움**: `screens/questionnaire_screen.dart` · `l10n/questionnaire_text.dart` · `model/questionnaire.dart` · 잠금 · unlock · 문진 API 호출 · 그 시험 | SPEC-006 §8.2 · SPEC-004 0.4.2 §5-3 · §6.10 · §6.11 | mobile | `procedure/app/lib/{screens/launchers.dart,screens/qr_show_screen.dart(새),screens/reservation_detail_screen.dart,screens/reservations*.dart,api/api.dart,api/session_store.dart,model/display.dart,app_state.dart}` · `test/` · (지움 파일) | 시뮬레이터(폰 · 패드)에서 데모 back 으로 [태블릿에 띄우기] → QR 화면 · 데스크 브라우저에서 그 주소 열면 화면 닫힘 · 스크린샷(QR 가림) | `cd procedure/app && flutter analyze && flutter test` | 대기 (WP-BE 뒤) |
| **WP-REVIEW** | reviewer: SPEC-006 §1 ~ §11 ↔ 코드 · 부록 A · 경로 49 · 공개 응답 허용 키 · 토큰이 로그 · DB 원문 · 푸시에 0 · 직원 세션 분리 · 법적 검토 주석 3곳 · 실명 · id grep. FAIL 은 모아서 한 번에 수정 발주 | 전체 | reviewer | 코드 전체 | PASS | — | 대기 |
| **WP-E2E** | 코디: 전체 검증 · compose 재기동(로컬 = 데스크 브라우저 · 시뮬레이터로 Q4 · Q5 흐름만 미리) → **배포**(코드 PR 머지 · 이미지 · infra `image.tag` — `deploy.md` 순서 · 앱은 TestFlight 다음 빌드) → **사용자 고객 폰 E2E SPEC-006 §10.3 Q1 ~ Q7**(+ Q8 안드로이드 있으면) · 피드백은 모아서 한 번에 | SPEC-006 §10.3 | 코디 · 사용자 · (수정) 각 워커 | — | Q1 ~ Q7 사용자 확인 | `uv run pytest -q` · `npm run build` · `flutter analyze && flutter test && flutter build ipa --release --dart-define=API_BASE=https://ccc.medisolveai.xyz --build-number=<+1>` | 대기 |

## 병렬

```text
WP-BE ──┬── WP-APP ─────────┐
        └── WP-FE(붙이기) ──┼── WP-REVIEW ── WP-E2E(배포 → 고객 폰)
WP-FE(화면 먼저 · 가짜 응답) ┘
```

- back 은 한 워커(같은 `service/questionnaire.py` · `service/display.py` · `repo.py`)
- front 는 화면을 가짜 응답으로 먼저 그리고 WP-BE 뒤 붙인다 · 앱은 WP-BE 뒤(`qrUrl` 이 있어야 그림)
- WP-FE · WP-APP 은 서로 파일이 겹치지 않는다 — 동시에

## 주의

- 고객 폰은 운영 주소에만 닿는다 — **고객 폰 E2E 는 배포 뒤**(로컬 http · 맥 IP 로 대신하지 않는다)
- 백엔드 커밋 뒤 compose 재기동(옛 코드로 E2E 금지) · 워커는 사용자 포트 · 프로세스를 건드리지 않는다
- 공개 `POST` 는 KOS 시험 고객 값을 바꾼다 — 데모 지점 · `[ccc 시험]` 고객만 · 운영 명동점 금지(D7-12)
- 스크린샷 · 리포트에 QR · 주소창 · 토큰 · 실명 0(SPEC-006 §7.5)
- 옛 TestFlight 빌드의 문진 화면은 배포 뒤 404 — 새 빌드를 같이 올린다(SPEC-006 OQ-812)
