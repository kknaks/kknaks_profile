# 리뷰 리포트 — day-data-architecture / doc · DAY-SPEC-001 로그인 · 세션 (2026-11-05)

대상: `mediness-mediness/day-data-architecture-spec` 의 미커밋 변경. HEAD 는 `60fae27b`(PR #909 브랜치)다.
- 새 파일: `products/day/20-spec/spec-001-login-session.md`
- 수정: `20-spec.md` · `30-work.md` · `log.md`

SPEC-000 · architecture 는 이미 PASS 했다. 이번에는 SPEC-001 과 어긋나는지만 봤다.

정답지:
- 원천: `erd/04-staff.md` · `erd/01-hospital.md` · `erd/README.md` · `system/README.md`(2026-11-05 판)
- 사용자 결정: `planner-spec001-report.md` 「사용자에게 받을 OQ」 권장안 11개 전부 + OQ-6 근거

## 판정: WARN

- 결정 11개는 빠짐없이, 바뀌지 않고 들어갔다. 원천의 정한 것 · 로그인 흐름도 모두 옮겨졌다.
- SPEC-000 필수 칸(`login_session.hospital_id` · `staff_id` 등)과 정면으로 모순되는 곳은 없다.
- 결정 · 원천에 근거가 없는 이름 · 값이 몇 개 있다(W1 · W2). 사용자가 고를 거리다.
- SPEC-000 쪽에 닫히지 않은 OQ 하나와 워커가 추측해야 할 빈칸 두 개가 있다(W3 · W4).

## FAIL

없음.

## WARN

### W1. 권장안 밖에서 붙인 이름 — 사용자가 고를 것

결정이 동작은 정했지만 이름은 주지 않은 자리들이다. 동작은 결정과 맞으므로 「발명된 정책」은 아니다. **이름 · 매핑은 근거 없는 발명**이라 사용자 확인이 필요하다.

| # | 위치 (`spec-001-login-session.md`) | 붙인 것 | 결정 근거 | 판정 |
|---|---|---|---|---|
| a | `:129` | `POST /api/auth/hospital` | OQ-1 (a) 「`/api/auth/login` · `/me` · 로그아웃 · 병원 고르기 하나를」 — 병원 고르기 경로가 **있다**는 것만 정함 | 경로 이름과 메서드(POST)는 발명 |
| b | `:131` | `POST /api/auth/logout` | 같음 — 로그아웃 경로가 있다는 것만 정함 | 경로 이름과 메서드는 발명. cc 관례에 가깝지만 cc 에 logout 이 있는지는 원천 · 결정에 없음 |
| c | `:163` | 403 `staff_inactive` | OQ-9 (a) 「로그인 막기」 — 코드 없음 | 이름 · HTTP 발명. 형식은 OQ-4 후보와 같음 |
| d | `:165` | 401 `unauthorized` (세션 없음) | OQ-4 후보 7개에 없음. 「cc 선례 이름」이라 하지만 cc 코드는 결정 · 원천에 적혀 있지 않음 | 발명 |
| e | `:166` | 403 `forbidden` (권한 없음) | OQ-11 (a) 「아무것도 못 함」 — 코드 없음 | 이름 · HTTP 발명 |
| f | `:158` | KOS 내부 API 차단(403 `Unsupported client.`) → 503 `kos_unavailable` | OQ-4 후보에 `kos_unavailable` 이름만 있고 적용 범위는 정하지 않음. 원천 `system/README.md:29-33` 은 차단 위험만 적음 | 매핑은 planner 해석 |
| g | `:164` | 로그아웃된 세션 → 401 `session_expired` | OQ-4 후보 `session_expired` 는 만료용. 로그아웃된 세션에도 같은 코드를 쓰는 것은 정하지 않음(`unauthorized` 와도 겹칠 수 있음) | 매핑은 planner 해석 |

planner 가 스스로 적은 것은 a~e 다(`planner-spec001-fix-report.md` 미결 1 · 2). f · g 는 리뷰어가 더 찾은 것이다.

### W2. 결정 · 원천에 없는 작은 정책 · 문구

- `spec-001:148` Validation 「형식 · 길이 검사는 KOS 가 한다 — DAY 가 따로 정하지 않는다」 — 원천 · 결정 어디에도 없다. 원천 `04-staff.md` 로그인 흐름 ①은 요청 모양 `{email, password}` 만 적는다.
- `spec-001:162` 안내 문구 「2단계 인증 계정은 아직 DAY 로그인을 지원하지 않습니다」 — 결정 OQ-6 은 「막고 안내」까지만 정했다. SPEC 자신도 `:54, :58` 에서 「문구 · 컴포넌트는 화면 SPEC 에서 정한다 · 디자인은 범위 밖」이라고 한다. 같은 문서 안에서 어긋나니 문구를 빼거나 「예시」로 표시한다.

### W3. SPEC-000 OQ-04-1 이 아직 「열림」으로 남아 SPEC-001 OQ-6 「정함」과 어긋난다

- 위치: `spec-000-data-model.md:1288` 「OQ-04-1 KOS 계정에 2단계 인증(`mfaMethods`)이 켜진 경우의 로그인 흐름」 — 원천 `erd/04-staff.md` 「정할 것」 1 그대로다.
- 대조: `spec-001:46, :162, :248` 은 같은 질문을 「1차는 다루지 않는다 — 막고 안내」로 정했다(사용자 2026-11-05).
- 방향: SPEC-000 OQ-04-1 에 「→ 1차는 DAY-SPEC-001 OQ-6 으로 정함(막기)」 같은 표시를 한 줄 단다. 이것은 SPEC-000 수정이라 이번 범위 밖이다. 원천 04 「정할 것」 1 도 같이 갱신할지는 코디 판단.

### W4. 워커가 추측으로 메워야 하는 빈칸 2개

1. **세션 토큰이 무엇인가.**
   - SPEC-000 `login_session.id` 는 「쿠키가 가리킨다」(`spec-000-data-model.md:594`)인데, SPEC-001 은 앱 `Authorization: Bearer <세션 토큰>`(`:140`)이라고만 한다.
   - 쿠키 · Bearer 값이 `login_session.id`(uuid) 그대로인지, 따로 만든 값인지가 비어 있다. 따로 만든 값이라면 SPEC-000 에는 그 값을 둘 칸(해시 등)이 없다.
   - 둘 다 「같은 `login_session` 한 행」(`:142`)이라는 것까지만 정해졌다. 「아직 열린 것」에 넣거나 SPEC-000 과 맞춰 정한다.
2. **처음 로그인으로 만든 `account` 의 `is_active` 값.**
   - S-1 3단계(`:83`)는 「`account` 를 만들고 … `account.is_active = false` 면 `account_inactive`」라고 한다.
   - 그런데 새로 만들 때의 기본값(true 로 둘지)은 정하지 않았다. `is_active` 는 SPEC-000 에서 필수 bool 이다.
   - 원천 · 결정에 없으므로 「아직 열린 것」에 올리거나 사용자 확인이 필요하다.

---

## 결정 11개 반영 확인

| OQ | 권장안(사용자 결정) | SPEC-001 위치 | 결과 |
|---|---|---|---|
| 1 | (a) JSON `/api/auth/login` · `/me` · 로그아웃 · 병원 고르기 — 웹 · 앱 같이 | `:122-133` · `:54` | 반영. 로그아웃 · 병원 고르기 경로 이름은 W1 a · b |
| 2 | (a) 웹 쿠키(httpOnly · Lax · Secure · CSRF) + 앱 Bearer · 같은 login_session · 이름 `day_session` | `:135-142` · `:244` | 반영 |
| 3 | (a) 세션 만료 = KOS 토큰 만료 + (가) 이전 세션 둔다 | `:94` · `:104` · `:142` · `:210` · `:224` | 반영 |
| 4 | 후보 7개(401 invalid_credentials · 503 kos_unavailable · 403 no_connected_hospital · 403 no_staff_account · 403 mfa_not_supported · 403 account_inactive · 401 session_expired) + 시간 제한 값 | `:155-166` · 시간 제한 값은 `:257` 열림 | 7개 코드 · HTTP 모두 그대로. 추가분은 W1 c~g |
| 5 | (가) 조기 401 → 세션 끝 · (나)-(a) 「반영 중」 유지 · (다) KOS 에 알리지 않음 | `:105-106` · `:111` · `:221` · `:224` | 반영 |
| 6 | (a) 1차는 막고 안내 + 근거(cc 처리 없음 · 명동점 90계정 중 0개) | `:46` · `:162` · `:248` | 반영. 근거 문장 그대로. 안내 문구는 W2 |
| 7 | (a) 1차는 병원 직원만 — 나중에 SPEC-000 개정 | `:45` · `:77` · `:249` | 반영 |
| 8 | (a) 다시 로그인 | `:69` · `:223` · `:250` | 반영 |
| 9 | (a) 로그인 막기 (+ 활성 칸 확인) | `:85` · `:163` · `:228` · 확인 사항 `:258` 열림 | 반영. 코드 이름은 W1 c |
| 10 | (a) is_demo 연결만 | `:67` · `:84` · `:222` · `:252` | 반영 |
| 11 | (a) 아무것도 못 함 | `:87` · `:166` · `:225` · `:253` | 반영. 코드 이름은 W1 e |

빠진 결정 0, 바뀐 결정 0. 본문에 남은 「→ OQ-n」 미결 표지도 0이다.

## 원천 대조

| 원천 | SPEC-001 | 결과 |
|---|---|---|
| `erd/04-staff.md` 「정한 것」 7개(KOS sign-in · 비밀번호 저장 안 함 · 자동 채움 · 역할 = 직무 · featureList 안 씀 · 본사 / 관리자는 직무 없음 · tags 고정 7 · external_ref / external_session · 직원 본인 토큰) | `:38-41` · `:45` · Rule 1-4 · 8 | 모두 있음. 「KOS 를 떼도 job_role 남는다」는 로그인과 무관해 생략(SPEC-000 에 있음) |
| `erd/04-staff.md` 로그인 흐름 ①②③ + 마지막 행 | S-1 2-6 · Flow `:172-195` | 순서 · 호출 이름 · 채우는 테이블 같음 |
| `erd/04-staff.md` `external_session` 칸(토큰 암호화 · 만료 · 테넌트 id) | `:86` · Rule 3 | 같음 |
| `erd/01-hospital.md` `crm_connection.config.tenant_id` · `APP_ENV=dev` 는 `is_demo` 만 | `:67` · Rule 5 | 같음. dev 로그인 후보에 적용한 것은 OQ-10 결정 |
| `erd/README.md` 공통 「원장」 — 연동 기간엔 외부가 이긴다 | `:93` · Rule 12 | 같음 |
| `system/README.md:17` 결정 1 — api 는 KOS 를 부르지 않음(로그인 · 바로 조회만 예외) | `:133` · Rule 10 | 같음 |
| `system/README.md:29-33` KOS 내부 API 차단 — 2026-11-03 18:23 KST · 403 `Unsupported client.` · UA · Origin · kos-client-uri | Rule 9 `:226` · `:158` | 시각 · 코드 · 헤더 세 가지 그대로. 매핑은 W1 f |

참고: `mfaMethods` 가 ③ get-user-account 응답에 있다는 것(`:85` · `:191`)은 원천에 응답 위치가 적혀 있지 않다. 원천 04 「정할 것」 1 은 이름만 있다. planner 는 HAR 로 확인했다고 하지만 리뷰어 환경에서는 HAR(`reference/2026-10-12-cc-prototype/로그인.har`)를 찾지 못해 **검증하지 못했다**. 구현 때 KOS 응답으로 확인하라.

## SPEC-000 과의 정합

- `login_session.hospital_id` · `staff_id` 필수: 1차 = 병원 직원만(OQ-7)으로 맞췄다. 병원 고르기 전 상태를 login_session 에 두지 않는다는 것도 「아직 열린 것」 3(`:259`)이 정직하게 열어 두었다. **모순 없음**.
- `external_session`(session_id PK · vendor · access_token 암호화 · token_expires_at · external_tenant_id): `:86` · Rule 3 과 맞는다. `vendor` 는 언급하지 않았지만 SPEC-000 에 맡기는 것이라 문제없다.
- `account`(`is_system_admin` · `is_active` · `last_login_at`), `staff`(`is_active` ← KOS `activate`), `job_role`(name · tags · is_default), `job_role_permission`(`level` view · edit): SPEC-001 이 쓴 칸 이름이 모두 SPEC-000 에 실재한다.
- 어긋나는 곳: W3(OQ-04-1), W4-1(세션 토큰 ↔ `login_session.id`).

## 「아직 열린 것」 점검 (`:255-260`)

| 항목 | 정말 열렸나 |
|---|---|
| KOS 호출 시간 제한 값 | 예 — OQ-4 권장안에 값이 없다 |
| 비활성 직원을 아는 방법 | 예 — 권장안 OQ-9 가 「(확인)」을 달았고 원천 ③ 응답 칸에 활성 여부가 없다 |
| 로그인 1단계 → 병원 고르기를 잇는 방법 | 예 — 결정 · 원천에 없다. login_session 필수 칸 때문에 실제 빈칸이다 |
| `permission_key` 목록 | 예 — SPEC-000 OQ-04-2 그대로다 |

결정된 것을 다시 연 곳은 없다. 다만 열어야 할 것 2개(W4)가 빠져 있다.

## 인덱스 · log · 규칙 · 보안

- `20-spec.md`: In Scope · Bundle · SPEC List(draft) · 읽는 순서 · OQ 링크가 SPEC 파일과 맞는다. `30-work.md` Spec Coverage 한 행이 lint 미러 규칙에 맞는다.
- `log.md`: `spec-add` · `spec-change` 두 행 · DAY-SPEC-001 · #909. 형식에 맞는다.
- frontmatter: `id` · `doc_no DAY-DOC-5`(유일) · type · title · status draft · owner TBD · last_updated · version 0.0.1 · sources 4개. 규칙에 맞는다.
- SPEC 에 두지 말 것: 작업 일정 · PR · schema 전문이 없다. 칸은 이름으로만 참조한다.
- lint `python3 scripts/lint-pipeline.py --strict` 1회 → **exit 0 · 0 error · 263 warning**. `products/day/` 범위는 ERROR 0 · WARN 0이다. 263 WARN 은 타 제품의 기존 경고라 **무관**하다.
- 보안 grep(이메일 · JWT · 32자 이상 토큰 · URL · 테넌트 id 값): **0건**. 「명동점 90계정 중 0개」는 집계 수치라 개인정보가 아니다.

## 직원이 실물에서 만날 자리

- W1 d · g: 세션 없음(`unauthorized`)과 로그아웃된 세션(`session_expired`)의 안내가 다르다. 화면이 두 코드를 다른 문구로 보여 주면 직원은 「로그아웃했는데 만료됐다고 나온다」를 볼 수 있다. 사용자가 고를 때 함께 보라.
- W1 f: KOS 가 DAY 를 막으면 직원 화면에는 「DAY 쪽 문제」로 나온다(`:158`). 원천 `system/README.md:33` 의 「KOS 가 더 막으면 멈출 수 있다」와 맞는 안내인지 확인하라.

## 참고

- `mfaMethods` 응답 위치는 검증하지 못했다(위 원천 대조 아래 참고).
- `planner-spec001-fix-report.md` 미결 4(Delivery #227 target SPEC 에 SPEC-001 추가 · L3 재승인)는 문서 검수 범위 밖이다 — 코디 처리.
