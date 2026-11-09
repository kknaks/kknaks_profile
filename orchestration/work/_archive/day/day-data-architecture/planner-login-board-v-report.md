# planner-login-board-v 결과 보고 — done (미커밋 · 승인 안 함)

## 1. SPEC-001 「웹 화면」 절 닫기 (`products/day/20-spec/spec-001-login-session.md`)

원천 04 「웹 화면 문구 · 흐름」 줄(사용자 2026-11-06 「추천안으로 가자」).

- 머리말 개정 ⑤ 한 줄.
- 「웹 화면」 절 머리 — 「사용자 확인 전 추천안」 → 「사용자 2026-11-06 결정(추천안 그대로)」. 대응표 머리 「문구(추천 — 사용자 확인 전)」 → 「문구(사용자 2026-11-06)」.
- 흐름 그림의 「이메일 유지 · 비밀번호 비움」 · 로그인 뒤 갈 곳 · 임시 토큰 줄에서 「제안」을 걷고 「사용자 2026-11-06」 — **검수 N1 닫힘**.
- §5 「아직 열린 것」에서 문구 · 숨은 폼 칸 줄 삭제 · 새 표 「웹 화면에서 정한 것」(경로 · 문구 · 임시 토큰 · 실패 화면 · 갈 곳).
- `log.md` 한 줄 · lint `--strict` 0 error.
- (검수 N2 — 원천 04 「CSRF (웹)」 줄을 웹 `/login` · `/login/hospital` 까지로 맞출지는 코디 몫 · 그대로 둠 · #232 Review Surface 에 적음.)

## 2. #232 contract v2 — [CENTURION_DAY#232](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/232)

- **plan_digest v2 = `sha256:f9a3b870336a0f1a2c68a6037a9e8e7c88796cf2b30135b4bcd69cf96b79ba6d`**(v1 `8c8fadd9…` stale) · L2 · 같은 key `day/v2-login-page` · `scope-delta-recorded`.

| 검수 | 바뀐 것 |
|---|---|
| W1 | target 정본 = SPEC-001 「웹 화면」 절(닫힘) 인용 · phase 1(SPEC 쓰기) · A6(SPEC PR) · code_surface 의 mediness 줄 · open_questions 삭제 · Non-Goal 「SPEC 문서 작성」 |
| W2 | 「웹 = 화면 라우트」를 기본값이 아니라 사용자 결정(원천 04)으로 Review Surface 에 |
| W3 | 임시 토큰 = 숨은 폼 칸(TD8 · A7) |
| W4 | A2 = 매트릭스 13줄 + 로그아웃 렌더 테스트 · A3 = forbidden 권한 없음 화면 · csrf_failed 토스트 · 만료 ?reason |
| W5 | A5 = 쿠키 세션 쓰기(POST /logout)만 CSRF · 로그인 전 요청(웹 /login · /login/hospital · 앱 /api/auth/login · /hospital) 미적용 |
| 4절 ① | 웹 화면 라우트 새로(TD3) |
| 4절 ② | 쿠키 심기를 웹 라우트로 · JSON client 기본값 app 또는 칸 없앰(TD4 · A6 회귀 테스트) |
| 4절 ③ | 웹 로그아웃 — 쿠키 지움 · form csrf_token · /api/auth/logout 은 앱 전용(TD5) |
| 4절 ④ | CSRF 미적용 주석에 웹 둘(TD6) |
| 4절 ⑤ | 웹 오류 응답 의존성 · 핸들러 — 이동(303 · HX-Redirect · ?reason) · 권한 없음 화면 · CSRF 토스트 · JSON 과 HX-Request · 경로로 가름(TD7) |
| 문장 | 「백엔드는 라우트 · 리다이렉트만」 → #227 웹 쪽 손질(쿠키 자리 · client 기본값 · 웹 오류 응답)을 Target Delta 로 · Review Surface 에 JSON client 기본값 변경 = 외부 계약 |

제목도 「… (#229 매크로 · DAY-SPEC-001 웹 화면)」으로 계약 title 을 바꿨지만 CLI 는 GitHub 제목을 바꾸지 않는다(본문 목표 줄만).

## 3. #230 contract v3 — [CENTURION_DAY#230](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/230)

- **plan_digest v3 = `sha256:46842b5ac920b1edc8f1a38b3be4a9c10dec924845393bc345ec90b531b7c45a`**(v2 `99bd5c99…` stale) · L3 · `scope-delta-recorded`.
- **W6**(사용자 2026-11-06 · 원천 screen 결정 「#230 계약 검수」): TD 새 줄 — [귀가 대기] · 시작 취소 · 완료 취소 · 재호출은 DAY 동작은 하고 KOS op 만 안 만듦(지원 안 함으로 드러냄) · 다음 폴링이 되돌릴 수 있음(감수) · HAR 오면 확인 값만. A5 = 「DAY 동작 성공 · op 0 · 다음 조회가 KOS 값을 따름」 단위 테스트. Non-Goal · Review Surface 문구를 결정으로 · 검증 한 줄.
- **W8 열린 채**: A8 끝에 「수락 단계 원장 계정은 사용자가 준 뒤(local.env)」 · Review Surface 한 줄 · open_question 「데모 지점 원장 계정(W8)」.

라벨은 둘 다 `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:pending`.
