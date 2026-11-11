# day-app planner — 직원 앱 SPEC 결과 보고

## 상태: done (SPEC 초안 · draft — 리뷰 전)

- 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec` · base `origin/main`(b4cd1a00) · 커밋 · push · PR 없음
- task `task_b51737e75121` · dispatch `ctx_f9d14e23b91f`

## 수행 내용 — 변경 파일

| 파일 | 변경 |
|---|---|
| `products/day/20-spec/spec-003-mobile-app.md` | **새로** — DAY-SPEC-003 직원 앱(iOS · 1차 시술 현황) · `doc_no: DAY-DOC-7` · draft |
| `products/day/20-spec/spec-001-login-session.md` | 개정(앱 환경 연결) 머리 줄 · 메타 OQ 줄 · §3 「지금 응답 모양」 표(현행 구현) · §3 「앱 환경 연결 (데모 계정) — 구현 전」(낱말 · 응답 칸 · 흐름 · 규칙 1~8) · 케이스 매트릭스 끝 두 줄(`environment_unavailable` 503 · dev 4xx 그대로) · 규칙 14 · 「아직 열린 것」 4줄 · last_updated |
| `products/day/20-spec.md` | In Scope 줄 · Out Of Scope(직원 앱 빼고 앱 범위 밖 줄) · Bundle · SPEC List · 읽는 순서 · OQ 링크 · 최종 수정 |
| `products/day/30-work.md` | Spec Coverage 에 `DAY-SPEC-003 \| — (WP · Delivery Issue 미발주) \| proposed` 한 줄만(코디 회신 A) |
| `products/day/40-architecture/mobile-deployment.md` | §1 API 주소 [확정](deployment.md 도메인) · 정식 앱 하나 + 데모 → dev [확정] · §6 심사 계정 [확정] · §9 API 주소 행 · 새 §9-1(환경 연결 · 푸시 topic/production 주의 · dev flavor 미결) · M-6 · M-14 닫음 · M-19 추가 · last_updated |

`10-decision.md` 는 바꾸지 않았다 — 결정권자 escalation 거리가 없다(사용자가 정한 방향 · 열린 것은 팀 몫). `log.md` 는 PR 번호가 없어 쓰지 않았다(아래 「log 제안」).

## API 변경표 (SPEC-001 · SPEC-003 — 전부 제안 · 서버 구현 전)

| 경로 | 바뀌는 것 | 지금 dev |
|---|---|---|
| `POST /api/auth/login`(client=app) | 응답에 `environment` · `api_base_url` 추가 · prod 서버가 `DAY_DEMO_LOGIN_EMAILS` 이면 dev 로 넘겨 인증 · 실패 503 `environment_unavailable` · dev 4xx 그대로 | 칸 없음 · 분기 없음 |
| `POST /api/auth/hospital` | 응답에 `environment` · `api_base_url` | 없음 |
| `GET /api/auth/me` | `environment` 추가 | 없음 |
| env(이름 제안) | prod: `DAY_DEMO_LOGIN_EMAILS` · `DAY_DEMO_API_BASE` / 모든 서버: `DAY_PUBLIC_API_BASE` — 값은 사용자 | 없음 |
| `PUT` · `DELETE /api/devices/{install_id}` | 새로 — 세션에 설치 잇기 · 끊기(`push_token` · `platform` · `app_id` · `push_env` · `kind`) · 세션 끝나면 발송 중지 · 푸시 본문 `environment` | 없음(`device` 테이블만) |
| `WS /api/interpret` | 새로 — interpret-pwa §5 계약 · Bearer · 시드 `2026-10-27.6` 서버 context | 없음 |
| 판 · 조작 JSON · SSE | 바꾸지 않음 — 현행 그대로 소비 | 있음 |

## 서버 의존 표

| # | 무엇 | 앱 구현(더블) | 통합 검증(실물) | 담당 |
|---|---|---|---|---|
| D-1 | 로그인 환경 연결 | 가능 — 정식 빌드는 칸 필수(없으면 실패) · 개발 빌드만 요청 주소 대신 | prod 배포 + 서버 구현 뒤 | 백엔드(사용자 승인 예외 범위) |
| D-2 | 기기 등록 API · APNs 발송(앱 id · 환경별 topic · `device` 칸 개정 SPEC-000 §3 07) | 가능 | 서버 + APNs 키(사용자) + TestFlight | 미배정 |
| D-3 | 통역 WS · 시드 가져오기 · Soniox | 가능(가짜 WS) | 서버 + Soniox 키(사용자) | 미배정 |
| D-4 | 방 이동 · 차트 · 시드 | 안 함 | 옆 세션 머지 뒤 | day-procedure-board-2 |

## 검증

- `python3 scripts/lint-pipeline.py --strict` → **exit 0** · products/day 범위 **ERROR 0 · WARN 0**.
- 전체 WARN 263건은 전부 다른 제품(예: selly `doc_no` 누락) — 무관.
- 처음 실행 때 DAY ERROR 2(20-spec.md SPEC List · 30-work.md Spec Coverage 에 SPEC-003 없음) → 20-spec.md 갱신 · 코디 회신 A 로 30-work.md 한 줄 → 해소.

## 계약 준수

- SPEC-002 스냅샷 · SSE · JSON 조작 경로는 dev 구현(`routers/api/board.py` · `services/board_rules.py`)과 줄 단위 대조 — 조사 리포트 「앱용 계약 없음」은 사실과 다름을 SPEC-003 §3 에 적음. UUID · 서버 계산 값(`can*` · `pickable` · `inbox.section`)만 씀.
- 수락 = DAY 권한 표(`board.accept`) · 간호사 대리 수락 · 원장 본인 수락 기본 선택 = 본인(SPEC-002 OQ-19) · 프로토 반대 규칙 배제.
- 통역 = interpret-pwa 7개 언어(대만 `zh-Hant` · 홍콩 `yue` 분리) · 사전은 서버 context(정 · 역방향 · `t2s` · 언어별 줄이기) · 값 번역 없음 · 사전 화면 없음.
- 환경 연결: 진입점 고정 · 서버 판별 · 요청 칸 · 헤더로 못 고름 · dev 장애 prod 우회 금지 · 토큰과 주소 함께 저장 · 복원 · 삭제 · SSE · HTTP · 통역 · 푸시 · 네이티브 수락 같은 환경 · 서버 분리 유지 · 심사 기능 숨김 금지.
- 문구: DAY SPEC · 웹 템플릿 글자 → 없으면 프로토 글자(파일 줄 근거) → 없으면 OQ. 새 문구 0.
- SPEC-000 · SPEC-002 · 30-work/ · 옆 워크트리 수정 없음.

## 미결 · 주의점

1. **정책 미결(사용자 결정 필요 · 기본값을 구현하지 말 것)** — OQ-A15 통역 권한 키 · OQ-A17 호출 푸시 받는 사람 · 알림 수락 액션 조건 · OQ-A1 앱 카드 순서 끌어 놓기 · OQ-A9 국적 → 통역 언어(국적 형식 W4 대기) · OQ-A11 `vi` · `yue` 빠른 말하기 문장 · OQ-A2 거르기 칩 = 인박스 칸 적응(리뷰 확인).
2. **문구 미결** — OQ-A16 `environment_unavailable` · OQ-A7 네트워크 실패 · OQ-A5 빈 판 · OQ-A6 오더 메모 없음 · OQ-A8 푸시 「전체 호출」 · OQ-A10 마이크 안내 앱 이름.
3. **나중 설정(OQ 아님 · 착수 조건 아님)** — Apple 등록 · 서명 · TestFlight · APNs 키 · 서버 env 값(데모 이메일 · 주소) · Soniox 키.
4. **SPEC-002 정정 필요(옆 세션 소유 · OQ-A12)** — JSON 오류 본문 `{detail, code, field}`(SPEC 은 `{error:{code,message}}`) · SSE `session_expired` 이벤트 · 연결 수명 1시간 · 구현 추가 칸 `firstKind` · `lateAt` · `overSec`.
5. **머지 충돌 주의** — 옆 워크트리(day-procedure-board-2-spec, 미커밋)가 SPEC-001(U-2 · S-1 · 매트릭스 행 · Flow · 규칙 5 · OQ-10 · 머리 개정 ⑥) · mobile-deployment(§1 서버 줄 · 그림 · §9 KOS 행 · M-18)를 고친다. 이쪽은 그 줄을 피했지만 SPEC-001 머리 개정 줄은 같은 자리(⑤ 바로 뒤)에 들어가 충돌이 난다 — 둘 다 남기면 된다(이쪽은 번호 없이 「2026-11-09 개정(앱 환경 연결)」). M-19 를 M-18 행 바로 뒤에 넣어 그 행과도 붙어 있다. 그쪽이 `is_demo` 를 지우므로 데모 계정이 prod 에 직접 붙으면 `no_connected_hospital` — 이 SPEC 의 dev 넘김이 그 빈자리를 메운다(정합).
6. **doc_no** — `DAY-DOC-7` 사용. 옆 세션이 새 문서를 만들면 같은 번호를 쓸 수 있다 — 병합 때 전수 확인.
7. `_RESUME.md` 「첫 업로드 = iOS 개발 버전」(11-09)과 「정식 앱 하나 · 데모 → dev」(브리프 최종)의 관계 — mobile-deployment 에 dev flavor 앱 유지 여부를 M-19 로 열어 둠.

## log 제안 (PR 번호 생기면 코디가 추가)

| 날짜 | 종류 | 영향 ID | PR | 요약 |
|---|---|---|---|---|
| 2026-11-09 | spec-add, spec-change, arch-change | DAY-SPEC-003, DAY-SPEC-001 | #<PR> | 직원 앱 SPEC-003 초안(draft — 시술 현황 탭 · 본인 / 대리 수락 · SSE · 푸시 · 통역 사전 · 서버 의존 D-1~D-4) · SPEC-001 앱 환경 연결(정식 앱 하나 · 데모 계정 → prod 판별 · dev 인증 · `environment` · `api_base_url` · `environment_unavailable` — 구현 전) · mobile-deployment 심사 계정 · API 주소 정합 |
