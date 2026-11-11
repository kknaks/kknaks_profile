# day-app planner — SPEC 리뷰 수정(fix1) 결과 보고

## 상태: done (draft · 재리뷰 대기)

- task `task_f7c7e0a73677` · dispatch `ctx_ef6ebe409507` · 원천 `review-spec-report.md`(FAIL 1 · WARN 9)
- 워크트리 `mediness-mediness/day-app-spec` · 커밋 · push · PR 없음 · 원 보고서 `planner-spec-report.md` · 리뷰 보고서 보존

## 수정 확인표

| 지적 | 고친 곳 | 내용 |
|---|---|---|
| **F-1** | SPEC-003 U-4 호출 상자 · A-22 | [재호출] = DAY 웹 E22 와 같은 조건만 — `need.why = "call"` · `state = called` 줄 있음 · `board` edit(근거 `board_parts.html` `inbox_card`). 대상 호출 = 첫 `called` 줄의 `call.id`(웹과 같음). 자리만 룸 상세(모바일 적응), 노출 조건 · 동작은 같음 · 프로토의 넓은 조건 배제 |
| **W-1** | SPEC-001 §3 흐름 · 규칙 3 · 매트릭스 2줄 / SPEC-003 U-1 · Flow · A-23 | 넘김 전체 **60초**(dev KOS 3 × 15초 ≈ 45초보다 김) · 앱 로그인 대기 **75초** · prod · 앱 모두 자동 재시도 · 중복 인증 없음 · 넘김 시간 초과 뒤 dev 늦은 성공 = 토큰은 앱에 안 가고 기존 만료로 끝남(매트릭스 행) |
| **W-2** | SPEC-003 §3 새 「연결 대상 검증」 · A-19 · Frontend Implementation / SPEC-001 낱말 「주소 정규화」 · 규칙 3 · 「아직 열린 것」 닫음 / mobile-deployment §9-1 | 정식 빌드 `--dart-define` 허용 origin 목록(prod · dev — 값은 배포 설정 · 소스 하드코딩 아님) · 정규화(https · userinfo 없음 · host 소문자 · port 없음/443 · path 비었거나 `/` · query · fragment 없음 → `https://<host>`) · 서버 넘김 대상 = `DAY_DEMO_API_BASE` 하나 · 기동 때 정규화 실패면 넘김 끔 · 3xx 따라가지 않음 · dev 응답 대상이 설정과 다르면 `environment_unavailable` |
| **W-3** | SPEC-003 U-1 성공 · §3 「세션 보관」 쓰는 때 · Flow · A-21 | 로그인 응답 ~ `/me` 동안 토큰 · 대상은 메모리만 → `/me` 200 + `environment` 일치 뒤 `staff_id` 포함 묶음을 원자적으로 저장 · 실패 · 불일치면 저장 없음. 자동 로그인 · 네이티브 수락은 늘 `staff_id` 있는 묶음만 봄 |
| **W-4** | SPEC-003 U-1 병원 여럿 · 「연결 대상 검증」 비교 · A-20 / SPEC-001 규칙 4 | 로그인 때 받은 대상을 세션 동안 유지 · hospital 응답은 정규화 origin + `environment` 일치 때만 수용 · 다르면 로그인 실패(다른 주소로 이동 · 토큰 전달 금지) · 끝 `/` 차이는 같은 것 |
| **W-5 · W-9** | SPEC-003 U-2 · §5 OQ-A2 → 「UI · 구현 선택」 표로 이동 | 칩 = 서버 `inbox.section` 거르기만 · 칩 안 순서 = `cards[]` 서버 순서 · 웹 인박스 칸별 정렬과 다를 수 있음 명시 · 새 우선순위 계산 · 새 순서 API 요구 없음 |
| **W-6** | SPEC-003 U-5 | 호출 `{taskIds, target: "all" \| "one", doctorStaffId?}` · 재호출 `{target, doctorStaffId?}` · `one` 이면 `doctorStaffId` 필수(없으면 400) |
| **W-7** | SPEC-003 §3 「푸시」 칸 · 경우 표 · A-24 | `install_id` uuid · `push_token` 필수 · 길이 고정 가정 안 함 · `platform` = `ios` · `app_id` 필수 + 서버 허용 번들 목록(env 이름 제안 `DAY_APNS_ALLOWED_APP_IDS` · 값은 사용자) · `push_env` · `kind` enum · 모르는 칸 400 · 401 `unauthorized` / `session_expired`. 서버 미구현(D-2) 그대로 |
| **W-8** | SPEC-003 U-14 · OQ-A8 | DAY 웹 사실만 바로잡음: 호출 창 「모든 의사」 · 카드 원장 줄 「전체 의사」 · 응답 없음 줄 「전체 호출 응답 없음」. 새 문구 없음 · 결정은 열림 |
| 참고 ① 수락 대기 조건 | SPEC-003 U-4 | 호출 상자 [수락] = 그 호출에 `state = called` 줄 + `board.accept` edit |
| 참고 ② 실물 확인 담당 | SPEC-003 A-4 | prod 행 0 확인 = 사용자 prod DB 읽기 조회 |
| 참고 ③ SPEC-002 코드 차이 | SPEC-003 OQ-A12 | ①~⑥으로 정리 — `kos_failed` 웹 토스트에 실패 동작 없음 · 인박스 칸별 정렬이 앱 JSON 에 없음 추가 |

## 변경 파일 (이번 수정분)

- `products/day/20-spec/spec-003-mobile-app.md` — 위 표
- `products/day/20-spec/spec-001-login-session.md` — 낱말 · 응답 칸 · 흐름 · 규칙 3 · 4 · 매트릭스 · 「아직 열린 것」
- `products/day/40-architecture/mobile-deployment.md` — §9-1 한 줄(허용 목록 · 리다이렉트)
- `products/day/30-work.md` — 변경 없음(기존 승인 한 줄 그대로) · `20-spec.md` 변경 없음 · `10-decision.md` · `log.md` · `30-work/` · SPEC-000/002 손대지 않음

## 검증

- `python3 scripts/lint-pipeline.py --strict` → **exit 0** · `0 error, 263 warning` — products/day ERROR 0 · WARN 0. 263건은 전부 다른 제품(selly `doc_no` 누락 등) — **무관**.
- diff 검사: `git status` = 기존 5파일만 · `30-work.md` diff = `+| DAY-SPEC-003 | — (WP · Delivery Issue 미발주) | proposed |` 한 줄.
- SPEC-001 · 003 에 남은 「15초 넘김(넘김)」 · 「https 만 확인」 문장 0.

## 미결 · 주의점

- **정책 OQ 는 닫지 않았다** — OQ-A15 통역 권한 · OQ-A17 푸시 대상 · 알림 수락 조건(코디가 사용자에게 질문 중) · OQ-A1 · OQ-A9 · OQ-A11.
- 시간 값 60초 · 75초는 기술 기본값(리뷰 지시 범위) — 제품 정책 아님.
- env 이름 넷(`DAY_DEMO_LOGIN_EMAILS` · `DAY_DEMO_API_BASE` · `DAY_PUBLIC_API_BASE` · `DAY_APNS_ALLOWED_APP_IDS`)은 제안 · 값은 사용자 · dev `DAY_PUBLIC_API_BASE` 와 prod `DAY_DEMO_API_BASE` 가 같은 origin 이어야 함(배포 설정 확인 항목).
- 코드 PR 때 CENTURION_DAY `AGENTS.md` 「앱」 「서버 주소 · 환경값은 `--dart-define`」 문장을 「고정 진입점 · 허용 목록만 빌드, 연결 대상은 로그인 응답」 뜻으로 맞출 것(SPEC-003 Frontend Implementation 에 적음).
- 옆 세션 PR #920 과 SPEC-001 머리 개정 줄 · mobile-deployment M-18/M-19 인접 줄 충돌 주의는 원 보고서와 같음.
