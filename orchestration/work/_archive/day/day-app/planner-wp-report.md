# day-app planner — Delivery request(WP) 작성 보고

## 상태: done — **GitHub 이슈는 아직 만들지 않았다**

- task `task_818208d68503` · dispatch `ctx_043f04754b26`
- 산출물: `orchestration/work/day-app/delivery-request.json`(start-delivery CLI 입력 — 원장 아님 · 원장은 생성될 CENTURION_DAY Delivery Issue)
- CLI `--plan` / `--apply` · Issue · PR · 커밋 · push · MCP Task draft · 승인 receipt 생성 없음. SPEC · 코드 · 30-work 수정 없음.

## request 요약

| 칸 | 값 |
|---|---|
| idempotency_key · product · root · version | `day/day-app` · `day` · `products/day` · 1 |
| risk_level | **L3** — 앱 신규 + 로그인 공개 계약 변경 + 환경 간 인증 전달. 첫 apply = `delivery-plan:review` · 사람 승인 gate 그대로 |
| target_specs | `DAY-SPEC-003` · `DAY-SPEC-001` |
| spec_baseline_revision | `b4cd1a004cd99c8e57761ad8cccd434d5e237b38`(= 로컬 `origin/main`) — main 에 SPEC-003 · SPEC-001 「앱 환경 연결」 절이 없으므로 **spec-baseline:pending** 이어야 한다(우회 없음 · review_surface 첫 줄에 명시) |
| target_delta | 8줄 — 앱 골격 · 시술 현황 · SSE · 세션 보관/연결 검증 · 푸시 앱 쪽 · 통역 앱 쪽 · D-1 백엔드 · AGENTS.md 「앱」 정합 |
| acceptance | A1 ~ A13 — SPEC-003 인수조건 26개(A-1 ~ A-24 · A-14b · A-16b) 전부 대응(기계 대조 누락 0) · 각 줄에 더블 / 실물 구분 · D-2 · D-3 실물은 「이 Delivery 완료 조건 아님」 명시 · 검증 명령(A12) · 경로 검사(A13) |
| non_goals | 8줄 — D-2 · D-3 서버 전체 · 사용자 설정 · 옆 세션 기능 · D-1 밖 backend · 상담사 호출 등 미래/보류 OQ · 다른 탭 · Android · 배포 |
| review_surface | 5줄 — Stable SPEC 부재 · 공개 계약 변경 · 인증 전달 안전 · 완료 정의 분리 · 옆 세션 겹침 |
| execution | code_surface 5 · dependencies 6 · phases 7 · verification 5 · predeploy 2 · rollback 2 · open_questions 1 — L3 필수 4칸(code_surface · phases · verification · rollback) 비어 있지 않음 |

## 범위 · 의존성

- 코드 범위: CENTURION_DAY `app/`(origin/dev 91728737 에 없음 — 새로) · D-1 로그인(`routers/api/auth.py` · `schemas/auth.py` · `services/auth.py` · `common/config.py`) · `tests/day/auth/` · env 이름 placeholder · AGENTS.md 「앱」 문장. 코드 PR 하나 → dev · 머지는 사용자 지시 때.
- 순서 근거: D-1(앱이 기댈 로그인 계약) → 앱 골격 · 세션 → 로그인 → 시술 현황 → 푸시 · 통역(더블) → 검증.
- 서버 미구현 · 담당 미배정: D-2(기기 등록 · APNs 발송) · D-3(통역 WS · 사전). 사용자 몫: Apple 등록 · 서명 · TestFlight · APNs · Soniox 키 · 서버 env 값 — 코드 착수 조건 아님 · 실물 검증 조건.
- 정책: 통역 = board view · 푸시 = 호출 대상 그대로 · 대리 수락과 수신 별개 · 상담사 호출 범위 밖 — SPEC-003 확정 그대로. 남은 OQ-A1 · A9 · A11 · 문구 OQ 는 SPEC 보류대로(새 질문 없음).

## 검증

- JSON 파싱 OK · `delivery-request.schema.json`(+ `delivery-issue.schema.json` execution) Draft 2020-12 검증 **오류 0**(`uv run --with jsonschema`).
- baseline SHA = 로컬 `origin/main` 일치 · target ID 2개 모두 실재(SPEC-001 은 main 에 있음 · SPEC-003 은 로컬 초안 — pending 으로 다룸).
- Acceptance ↔ Non-Goals 대조: D-2 · D-3 · 사용자 설정은 acceptance 에서 「더블 / 실물은 완료 조건 아님」으로만 나오고 non_goals 와 충돌 없음 · D-1 은 둘 다에서 범위 안(관련 테스트 포함)으로 일치.

## 주의

- baseline 재결속: SPEC PR 머지 뒤 같은 key · version 2 · 새 main SHA 로 재실행해야 ready.
- 옆 세션 PR #920 과 SPEC-001 · mobile-deployment 충돌 · 머지 순서는 SPEC PR 단계에서 처리.
