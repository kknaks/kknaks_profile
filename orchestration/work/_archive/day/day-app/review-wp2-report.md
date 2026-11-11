# 리뷰 리포트 — day-app / WP(Delivery request) 재검수 (2026-11-09)

- 대상: `delivery-request.json`(현재본)의 변경 필드 · `planner-wp-fix-report.md` · 원 지적 `review-wp-report.md`(W-1 ~ W-3)
- read-only · CLI · GitHub 쓰기 · receipt 없음

## 판정: PASS

W-1 ~ W-3이 해소됐고, 변경으로 생긴 새 모순은 없다. 고정돼야 할 결과 계약도 그대로다. **이 PASS는 코드 구현 승인도, 실연동 완료도 아니다.** CLI 공식 흐름대로 `--apply`가 첫 이슈를 `delivery-plan:review`(L3 사람 승인 대기)로 만들고, 사람 승인은 코드 구현 전에 받는다. 「승인 전 이슈 생성 금지」 같은 게이트를 새로 요구하지 않는다.

## 지적별 확인

| 지적 | 결과 | 근거(JSON 필드) |
|---|---|---|
| **W-1** 완료 기준 | **해소** | `acceptance[0]` 「완료 정의」 = 머지 전 PR head의 더블 · 로컬 단위 · infra · analyze · unsigned build · diff · 비밀 검사. 기존 dev · day-local · 실기기 · prod 배포 뒤 확인 = 통합 검증(별도 기록 · 미실행 pending · 선행 조건 아님). A1 · A2 · A3 · A4 · A5 · A7 · A8이 모두 「완료 = … / 통합 검증(Delivery 완료 조건 아님 · pending)」 같은 형식이다. A3의 prod 데모 넘김 · prod 행 0은 범위 밖 통합 검증으로 옮겼고, 구현 완료는 D-1 pytest(테스트 DB에 prod 행 미생성)다. `review_surface[3]` · `predeploy[0]`(dev 서버 확인 → PR head pytest)도 같은 뜻. A9 · A10(D-2 · D-3)은 그대로 |
| **W-2** 경로 · 담당 | **해소** | `code_surface[3]` `deploy/local.env.example` · `verification[2]` · A12 `backend/tests/architecture` — dev 91728737 실재. `-m "not infra"`는 실제 marker다(`pyproject.toml` `markers = ["infra: …"]` · `tests/day/auth/test_auth_api.py` · `test_web_login.py`). infra = 로컬 compose 필요 · 포트 조작 금지 · 못 돌리면 pending. 시뮬레이터 = 사용자 또는 명시 허용된 앱 워커 스크린샷(A8 · `verification[4]`) · 리뷰어는 기기를 조작하지 않음 |
| **W-3** 롤백 | **해소** | `rollback[1]` = `DAY_DEMO_LOGIN_EMAILS`는 두고 `DAY_DEMO_API_BASE`를 비워 503 `environment_unavailable`(SPEC-001의 기존 fail-closed). 목록 비우기는 롤백 수단에서 뺐다(「prod 일반 인증으로 보냄」을 명시). `rollback[0]` revert = 앱 쪽 fail-closed인데, 「서버가 prod 행을 만들지 않는다는 증거 아님」이라고 정확히 한정했다. env 변경 · 배포는 범위 밖(사용자) |

## 유지 확인

- schema(Draft 2020-12 · execution ref) **오류 0** · 필수 칸 모두 있음.
- `day/day-app` · `day` · `products/day` · v1 · **L3** · target `DAY-SPEC-003`, `DAY-SPEC-001` · baseline `b4cd1a004cd99c8e57761ad8cccd434d5e237b38` = 이번에 fetch한 `origin/main`과 같다(→ pending 유지).
- target_delta 8 · non_goals 8은 내용이 바뀌지 않았다(기능 범위 · D-2/D-3 미승인 · 사용자 설정 · 옆 세션 · 상담사 호출 범위 밖 그대로). acceptance는 13 → 14로 「완료 정의」 한 줄만 더했다. SPEC-003 AC 26개 대응 누락은 0.

## 참고(판정 밖 · 선택)

- `acceptance[0]`은 infra 테스트 통과를 구현 완료에 넣고, A12 · `verification[2]`는 「못 돌리면 pending」이다. 「infra pending이면 구현 완료도 pending」이라고 읽는 것이 자연스럽다. `review-delivery` 판정 때 그렇게 해석하면 된다. 문장으로 박고 싶으면 A12 끝에 「infra pending 동안 Delivery 구현 완료도 pending」을 덧붙인다.

## 남은 것

- 코디가 CLI `--plan`을 다시 확인한 뒤 `--apply`로 첫 이슈(`delivery-plan:review` · `spec-baseline:pending`)를 만든다. 코드 구현 전에 L3 사람 승인을 받는다. SPEC PR 머지 뒤 version 2 · 새 main SHA로 baseline ready에 재결속한다.
- 서버 D-2 · D-3은 미구현 · 미배정이다. Apple · 서명 · TestFlight · 키 · env는 사용자 몫이다. 통합 검증은 모두 pending으로 따로 기록한다.
