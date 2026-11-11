# day-app planner — WP 리뷰 W-1 ~ W-3 수정 보고

## 상태: done — **GitHub 이슈는 아직 만들지 않았다**

- task `task_fbcb7c64e913` · dispatch `ctx_d44c8bbc6f4c` · 원천 `review-wp-report.md` · 원 보고서(`planner-wp-report.md`) 보존
- 수정 파일: `delivery-request.json` 하나. CLI plan/apply · Issue · 커밋 · receipt 없음.
- 그대로: `contract_version` 1 · `risk_level` L3 · target `DAY-SPEC-003` · `DAY-SPEC-001` · baseline `b4cd1a004cd99c8e57761ad8cccd434d5e237b38`(pending) · target_delta · non_goals · 기능 범위.

## 변경 필드

| 지적 | 필드 | 변경 |
|---|---|---|
| W-1 | `acceptance[0]` 새 줄 | 「완료 정의」 — 구현 완료 = 머지 전 PR head 의 앱 단위 · 위젯 · 계약 더블 · D-1 로컬 단위 · infra 테스트 · analyze · unsigned build · diff · 비밀 검사. 기존 dev 서버 · day-local · 실기기 · prod 배포 뒤 확인 = 통합 검증(별도 기록 · 미실행 pending · 선행 조건 아님). D-2 · D-3 분리 그대로 |
| W-1 | `acceptance` A1 · A2 · A3 · A4 · A5 · A7 · A8 | 각 줄을 「완료 = 더블/로컬 테스트」 + 「통합 검증(완료 조건 아님 · 별도 기록 · pending)」으로 같은 형식. A3 = prod 배포 뒤 데모 넘김 · prod 행 0 은 범위 밖 통합 검증 · 구현 완료는 D-1 pytest(테스트 DB 로 prod 행 미생성) |
| W-1 | `review_surface[3]` · `execution.predeploy[0]` | 완료 정의와 같은 구분 · 머지 전 dev 서버 확인 문장을 PR head pytest 로 바꿈 |
| W-2 | `execution.code_surface` · `verification` · `acceptance` A12 | `deploy/local.env.example` · `backend/tests/architecture` · infra 테스트 = 로컬 compose PostgreSQL · Redis 필요(사용자 환경 · 포트 조작 금지 · 못 돌리면 pending) · `pytest -m "not infra"` 와 `scripts/test.sh` 구분 |
| W-2 | `acceptance` A8 · `verification[4]` | 시뮬레이터 검수 = 사용자 또는 명시 허용된 앱 워커 스크린샷 · read-only 리뷰어가 기기 조작 안 함 |
| W-3 | `execution.rollback` | 「데모 이메일 env 비우면 기존 동작」 삭제. ① 코드 revert = 새 정식 앱은 환경 칸 없어 로그인 거절(앱 fail-closed) — **서버가 prod 행을 만들지 않는다는 증거가 아님**을 명시 ② 데모 넘김 중지 = `DAY_DEMO_LOGIN_EMAILS` 유지 · `DAY_DEMO_API_BASE` 비워 503 `environment_unavailable`(SPEC-001 기존 fail-closed) · 목록 비우기는 롤백 수단 아님 · env 변경 · 배포 실행은 범위 밖 ③ migration 없음 |

## 검증

- JSON 파싱 OK · schema(Draft 2020-12 · execution ref) **오류 0**
- baseline · target · version · risk 변경 없음 확인 · SPEC-003 인수조건 26개 대응 누락 0
- 잔여 문장 검사: 접두 없는 `local.env.example` 0 · `tests/architecture` 0 · 「비우면 기존」 0
- Acceptance ↔ Non-Goals: prod 배포 · D-2 · D-3 · 사용자 설정은 acceptance 에서 「통합 검증 · 완료 조건 아님」으로만 나와 non_goals 와 충돌 없음

## 다음

- 코디 독립 재리뷰 → CLI `--plan` → `--apply`(첫 apply = `delivery-plan:review` · 구현 전 사람 승인). worker 는 승인 요구 · receipt 생성 안 함.
