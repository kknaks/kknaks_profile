# kos-signin-limit-spec 결과 보고 — KOS 동시 로그인 5개 제한 · SPEC-001 개정 ⑨ · Delivery 발행

## 상태: done (plan 승인 대기 — 승인 receipt 는 적용 안 함 · 사용자 몫)

| 항목 | 값 |
|---|---|
| Delivery Issue | **CENTURION_DAY#256** — https://github.com/MediSolveAIDev/CENTURION_DAY/issues/256 |
| 라벨 | `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:ready` |
| risk | **L3** — KOS `revoke-active-sign-in`(외부 쓰기 · 세션 끊기) · 비밀번호 서버 임시 보관 · 새 외부 계약(API 경로 · 응답) |
| idempotency_key | `day/kos-signin-limit-2026-11-17` |
| contract_digest | `sha256:4decfb5b2ef12d652893011a4d806a99b10f009f9bb559c350a1e4f6c6ad19ec` |
| plan_digest (승인 대상) | `sha256:38a941dd3c2fe85899c47af4d603a816c08287f8250c7d0190e4b309c74b597a` |
| baseline | mediness `origin/main` `4443a99ac616cc29bf681cf47a84f719d532fb94` — **개정 ⑨ · ⑱ 은 이 워크트리에만(미커밋)**. Review Surface[0]: 스펙 PR 머지 → 같은 key 로 contract_version 2 재결속 → 그 뒤 사용자 승인 권장(v1 plan_digest 는 승인하지 않는 쪽 권장 · 앞 #254 와 같은 순서) |
| next_action | `review-delivery-plan` · human_gate true · task_projection blocked(`delivery-plan-review-required`) — 정상 |
| request / plan / apply | `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-kos-signin-limit-spec/40b80114-ef00-4681-a657-e248a0ad6222/scratchpad/delivery/ksl.v1.request.json` · `ksl.v1.plan.json` · `ksl.v1.apply.json` (같은 폴더) |

## 수행 내용 — 변경 파일 (워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/kos-signin-limit-spec` · 미커밋 · `products/day/` 만)

- `products/day/20-spec/spec-001-login-session.md` — 개정 ⑨(+175 −11) · `last_updated` 2026-11-17 · sources 에 `_RESUME.md`
- `products/day/20-spec/spec-003-mobile-app.md` — 개정 ⑱(:72) · U-1 「KOS 기기 제한」(:234) · 케이스 매트릭스 한 줄(:748)
- `products/day/20-spec/spec-000-data-model.md` — 2026-11-17 개정 줄(:39) · 「테이블에 두지 않는 것」 `KOS_CLIENT_TAG`(:220) · `last_updated`
- `products/day/20-spec.md` — In Scope 로그인 줄(:31) · Out Of Scope 앱 기기 선택 · 로그아웃 해제(:42)
- `products/day/log.md` — 2026-11-17 spec-change 행(:17)

`version` 은 0.0.1 그대로(문서 개정으로 올리지 않음 — 파이프라인 규칙).

## 결정 표 반영 위치 (spec-001 줄 = 수정 뒤)

| 결정 | 위치 |
|---|---|
| K-1 공통(401 `message` 로 가름 · 목록 → 해제 → 다시) | §3 「KOS 동시 로그인 제한」 :361 — KOS 사실 표 · 「공통 (K-1)」 :379 · 규칙 15 :529 · 케이스 매트릭스 :441~ |
| K-2 시스템 계정(`KOS_CLIENT_TAG` · 막혔을 때만 · 같은 UA · 표시 비면 안 함) | 「시스템 계정 (K-2)」 :386 · S-8 :240 · 매트릭스 끝 줄 · SPEC-000 :220 |
| K-3 직원 기기 선택(KOS 화면 구성 · 글자 · 계속하기 · 이후 기존 흐름 · DS 같은 틀) | U-4 :95 · 웹 라우트 `/login/device` :117 · 흐름 · 숨은 칸 :140 · 화면 글자 표 :153 · 웹 대응표 :180~ · S-7 :232 · API `/api/auth/device` :258 · 응답 `choose_device` :289 · 「직원 — 기기 선택 단계」 :399 · Validation :423 · Flow opt :469 |
| 비밀번호 임시 보관(같은 틀 · 기본값) | 「기기 선택 동안 비밀번호」 :409 · 규칙 1 :513 · OQ-K3 |
| K-4 로그아웃 KOS 해제 안 함 | U-3 :93 · 공통 4 |
| K-5 웹 · 앱 둘 다 · 앱 무수정 | 응답 표 :289(앱 칸) · 데모 넘김 규칙 9 :359 · SPEC-003 개정 ⑱ |
| K-6 스펙 → 검수 → 코드 · 배포 나중 | 개정 ⑨ 노트 :42 · OQ-K15 |

화면 글자 = 결정 표 글자만(제목 · 안내 2줄 · 「{OS} {브라우저} · {IP}」 · 「n분 전」 · 「방금 전」 · 「계속하기」). 「처음으로」 재사용은 OQ-K10 으로 올림(기본 둔다 · 사용자 확인).

## 앱 영향 (코드 사실 · CENTURION_DAY dev `0c401726` · 앱 무수정)

- 깔린 앱이 200 `choose_device` 를 받으면 `session_controller.dart:203` `status != 'signed_in'` → `unexpected_response` 실패 → 로그인 화면 · 이메일 유지 · 비밀번호 비움(`_fail` :347-353) · 오류 칸에 **코드 `unexpected_response` 문자열 그대로**(`copy.dart:51` codeOnly · `login_screen.dart:84` · :100). 자동 재시도 · KOS 해제 없음. (지금은 같은 경우 「이메일 또는 비밀번호가 맞지 않습니다 …」)
- 데모 계정: 지금 `services/environments.py` `read_success` 는 `signed_in` · `choose_hospital` 밖 200 을 `environment_unavailable` 503 으로 — 규칙 9(OQ-K7 기본)로 넘기게 하면 위와 같은 `unexpected_response`.
- 막힌 직원의 우회: 같은 계정 로그인을 DAY 웹 기기 선택 또는 KOS 웹에서 해제 뒤 앱 로그인(사실에서 따라옴 · 안내 글자는 안 정함).

## KOS 사실 중 새로 확인한 것 (HAR · 값은 옮기지 않음)

- 목록 · 해제 · 해제 뒤 다시 sign-in 의 `kos-client-uri` = `<web>/auth/active-sign-in-limit` · 막힌 첫 sign-in = `<web>/auth/sign-in` (be-0 「스펙에서 정할 것」 4번 해소). 응답 모양은 브리프 사실과 같음(`maxSignInCount` int · `data` 5건).

## 착수 막는 OQ (기본값 후보 — SPEC-001 §5 「기기 제한 — 정할 것」 :594)

| OQ | 질문 | 기본값 후보 |
|---|---|---|
| OQ-K1 | 시스템 계정 해제 개수 | 같은 UA 중 가장 오래된 하나(전부는 api · worker 왕복 위험) |
| OQ-K2 | 직원 요청도 표시 UA | 싣는다(서버 하나에 UA 하나) — 시스템 계정 이메일로 DAY 로그인한 사람 세션이 자동 해제 대상이 될 수 있음 |
| OQ-K3 | 비밀번호 보관 | 임시 토큰 값 통째 `encrypt_value` · Redis 5분 · 꺼내면 지움 · 잘못된 선택만 되돌림 · DB/로그/응답/화면/URL 없음 |
| OQ-K4 | 새 이름 | `choose_device` · `POST /api/auth/device {pending_token, device_id, client}` · `POST /login/device` · `devices[{id,label,ip_address,signed_in_at}]` |
| OQ-K5 | 60분 넘는 상대 시각 | 「n분 전」 그대로(글자 안 지음) |
| OQ-K6 | UA → OS · 브라우저 | 흔한 이름만 · 못 읽으면 userAgent 원문 |
| OQ-K7 | 데모 넘김 `choose_device` | 넘긴다(규칙 9) |
| OQ-K8 | 해제 4xx · 웹 잘못된 선택 | 그래도 sign-in 다시 · 웹 `/login?reason=session_expired` |
| OQ-K12 | 빈 목록 | 503 `kos_unavailable` |

그 밖(착수 안 막음): OQ-K9 목록 순서 · K10 「처음으로」 · K11 해제가 토큰을 바로 막는지(데모 실물) · K13 「최대 5개」 고정 · K14 앱 화면 · K15 배포 값 · deployment.md 표 · K16 로그인 쌓이는 원인.

## 검증

- `python3 scripts/lint-pipeline.py --strict` → rc 0 · **0 error · 263 warning** · `products/day/` 범위 ERROR 0 · WARN 0. 263 WARN 은 전부 타 제품(selly 등 — `doc_no` 누락 · frontmatter) — 무관.
- 개인정보: 문서에 비밀번호 · 이메일 · IP · 서버 IP 없음(HAR 파일 이름만 언급 · 화면 캡처는 글자만).

## 미결 · 주의점

- 스펙이 미커밋이라 #256 v1 baseline(4443a99a)은 옛 계약 — 스펙 PR 머지 뒤 v2 재결속 후 승인 권장.
- 「처음으로」를 기기 선택에 둘지(OQ-K10) — 결정 표 밖이라 기본값만 두었다. 검수가 「글자 지음」으로 보면 기본값을 「두지 않음」으로 바꾸면 된다.
- S-7 5 · OQ-K11: KOS 해제가 그 로그인의 토큰을 즉시 무효화하는지 미확인(추측으로 메우지 않음).
- 하네스 실행이 `tools/harness/.venv` 를 만들었다(gitignore 대상 — `git status` 에 안 보임).
