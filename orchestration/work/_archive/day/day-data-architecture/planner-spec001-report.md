# DAY-SPEC-001 로그인 · 세션 — 결과 보고

## 상태: done

## 작성 내용

워크트리 `mediness-mediness/day-data-architecture-spec`(PR #909 브랜치) · `products/day/` 만. 커밋 · push 안 함.

| 파일 | 내용 |
|---|---|
| `products/day/20-spec/spec-001-login-session.md` (신규 · DAY-SPEC-001 · doc_no DAY-DOC-5 · draft · owner TBD) | spec 템플릿 구조 — §1 개요(왜) · §2 사용자 경험(U-1 로그인 폼 · U-2 병원 고르기 · U-3 로그아웃 / S-1 처음 로그인 · S-2 다시 로그인 · S-3 병원 여럿 · S-4 만료 · S-5 로그아웃 · S-6 실패) · §3 계약(동작 단위 표 — 경로는 OQ · Validation · 케이스 매트릭스 11행 · Flow sequence · login_session 상태) · §4 Functional Rule 11개(원천에서 정한 것만) · DB(SPEC-000 테이블 이름 참조만) · §5 OQ-1~11 |
| `products/day/20-spec.md` | In Scope · SPEC Bundle · SPEC List · 영역별 읽는 순서(계정 · 인증) · OQ 링크에 SPEC-001 |
| `products/day/30-work.md` | Spec Coverage `DAY-SPEC-001 \| — (WP · Delivery Issue 미발주) \| proposed` (lint 미러) |
| `products/day/log.md` | 2026-11-05 `spec-add` · DAY-SPEC-001 · #909 |

데이터 칸은 SPEC-000 §3 04 를 이름으로만 참조(복제 0). 원천에 없는 계약 값(API 경로 · 세션 전달 · 쿠키 이름 · 세션 길이 · 오류 코드 · 재로그인 · 2단계 인증 · 시간 제한)은 본문에 「→ OQ-n」만 두고 정하지 않았다.

## 검증

```
python3 scripts/lint-pipeline.py --strict → 0 error, 263 warning
products/day/ 범위: ERROR 0 · WARN 0 (263 은 타 제품 기존 — 무관)
```

## 원천 근거 표 (SPEC 의 정한 것 → 어디서)

| SPEC-001 규칙 | 원천 |
|---|---|
| 로그인 = 우리 화면 → KOS sign-in → 반환값 저장 · 비밀번호 저장 안 함 | `erd/04-staff.md` 「정한 것」 1 |
| 로그인하면 자동으로 채움 · 관리자가 미리 만들지 않음 | 04 「정한 것」 2 |
| 역할 = KOS 직무 · 권한 = job_role_permission · featureList 안 씀 | 04 「정한 것」 3 |
| 본사 · 시스템 관리자는 KOS 직무 없음 | 04 「정한 것」 4 |
| 업무 판단은 job_role.tags(고정 7) | 04 「정한 것」 5 |
| KOS id → external_ref · 토큰 → external_session(KOS 떼면 테이블째) | 04 「정한 것」 6 |
| 직원 본인 KOS 토큰으로 KOS 에 씀 | 04 「정한 것」 7 |
| ① sign-in → ② get-user-tenants(연결된 병원만 · 하나면 자동) → ③ get-user-account → login_session + external_session | 04 「로그인 흐름」 표 |
| account 없으면 만들고 있으면 갱신 · staff 있으면 연결 없으면 만듦 | 04 「로그인 흐름」 표 ① · ③ |
| KOS 토큰 만료 → 다시 로그인 | 04 `external_session.token_expires_at` 설명 |
| account.is_active = 로그인 허용 · staff.is_active = 재직 | 04 `account` · `staff` 표 |
| login_session.hospital_id · staff_id 필수 · expires_at · last_used_at · revoked_at | 04 `login_session` 표 |
| 로그인은 api 가 KOS 를 바로 부르는 예외 | `system/README.md` 결정 1 |
| KOS 내부 API 브라우저 헤더(UA · Origin · kos-client-uri) 필수 · 403 `Unsupported client.` | `system/README.md` 「위험 — KOS 내부 API 차단」 |
| 연결된 병원 = crm_connection.config.tenant_id · APP_ENV=dev 는 is_demo 연결만 동기화 | `erd/01-hospital.md` |
| 연동 기간엔 외부가 원장 | `erd/README.md` 공통 규칙 「원장」 |
| `mfaMethods` 는 ③ get-user-account 응답 칸 | KOS HAR `로그인.har` — 필드 이름만 확인(값 옮기지 않음) |

참고(권한 아님 — OQ 의 권장 근거로만): cc-prototype `POST /api/auth/login` · `GET /api/auth/me` · Bearer · 세션 12시간(`proc_session_hours`) · 401 이면 토큰 다시 받기 1회(시스템 계정이라 가능) · 오류 순서 401 → 403 / centurion 세션 쿠키 `ms_sso_session` httpOnly · SameSite=Lax · Secure · 8시간(관리자 1시간) · CSRF / CENTURION_DAY `AGENTS.md` 「웹 화면」 CSRF `X-CSRF-Token` · 「작업 규칙」 API 경로 · 인증 · 쿠키 · 오류 = 외부 계약.

## 사용자에게 받을 OQ (옵션 + 권장)

| # | 질문 | 옵션 | 권장 · 근거 |
|---|---|---|---|
| OQ-1 | API 경로 | (a) JSON `/api/auth/login` · `/me` · 로그아웃 · 병원 고르기 하나를 웹 · 앱이 같이 (b) 웹 폼 `/login` + 앱 JSON 따로 | **(a)** — cc 선례 · 계약 하나 |
| OQ-2 | 세션 전달 · 쿠키 이름 | (a) 웹 쿠키(httpOnly · Lax · Secure · CSRF) + 앱 Bearer, 같은 login_session (b) 둘 다 Bearer. 이름 `day_session` / centurion `ms_sso_session` 재사용 | **(a) + `day_session`** — centurion · cc 선례, DAY 는 독립 |
| OQ-3 | 세션 길이 · 이전 세션 | (a) DAY 세션 만료 = KOS 토큰 만료 (b) 고정 12시간(cc). 이전 세션 (가) 둔다(여러 기기) (나) 끝낸다 | **(a) + (가)** — 원천 「토큰 지나면 다시 로그인」과 일치, 폰 · 아이패드 · 웹 |
| OQ-4 | 오류 코드 · HTTP · 시간 제한 | 후보: 401 `invalid_credentials` · 503 `kos_unavailable` · 403 `no_connected_hospital` · 403 `no_staff_account` · 403 `mfa_not_supported` · 403 `account_inactive` · 401 `session_expired` + KOS 호출 시간 제한 값 | **후보대로** — cc 오류 순서 · 코드로 문구 선택 |
| OQ-5 | 재로그인 · 토큰 처리 | (가) KOS 가 만료 전 401 → 세션 끝 · 다시 로그인(DAY 는 비밀번호 없음) (나) 토큰 만료 직원의 쓰기 큐: (a) 다시 로그인까지 「반영 중」 (b) 실패 처리 (c) 다른 직원 토큰(비권장) (다) 로그아웃 때 KOS 에 알리기 | **(가) · (나)-(a) · (다) 알리지 않음** — 원천 「KOS 기록에 실제 직원」 |
| OQ-6 | 2단계 인증 계정 | (a) 1차는 막고 안내 (b) KOS 2단계 흐름 지원(KOS 흐름 미확인) | **(a)** |
| OQ-7 | 본사 · 시스템 관리자 로그인 | (a) 1차는 병원 직원만 — 나중에 SPEC-000 개정 (b) KOS sign-in + 어느 병원 직원 계정 필요 (c) login_session 병원 · 직원 nullable 로 SPEC-000 개정 | **(a)** — login_session.hospital_id · staff_id 필수(데이터 모델과 충돌), 1차 범위 = 시술실 · 의국 |
| OQ-8 | 로그인 뒤 병원 바꾸기 | (a) 다시 로그인 (b) 세션 안에서 바꾸기 | **(a)** — 세션 = 병원 하나(external_session 테넌트 하나) |
| OQ-9 | 비활성 직원(staff.is_active=false) | (a) 로그인 막기 (b) 권한 없이 들어옴 | **(a)** — ③ 응답에 활성 칸이 안 보여 기준 정보 동기화로만 알 수 있을 수 있음(확인) |
| OQ-10 | dev 서버 로그인 후보 | (a) is_demo 연결만 (b) 제한 없음 | **(a)** — dev 가 실제 병원 데이터를 건드리지 않게 하는 원천 장치와 같은 뜻 |
| OQ-11 | 권한 행이 없는 직무의 기본 | (a) 아무것도 못 함 (b) 보기만 | **(a)** — 권한은 DAY 관리자가 직무별로 정한다(04) · permission_key 목록은 SPEC-000 OQ-04-2 |

## 미결 · 주의점

1. **Delivery #227(로그인)의 target SPEC 은 지금 DAY-SPEC-000 하나다.** SPEC-001 을 대상으로 넣으려면 같은 key(`day/v2-login`) · contract_version 2 · `scope_delta`("target SPEC 에 DAY-SPEC-001 추가") 로 재실행 → plan_digest 가 바뀌어 L3 승인을 다시 받아야 한다. #227 의 Review Surface 「로그인 API 계약을 담을 SPEC」 항목이 이걸로 풀린다. 코디가 처리(이번 작업 범위 밖 — Issue 는 손대지 않았다).
2. OQ-7 은 데이터 모델(SPEC-000 `login_session` 필수 칸)과 원천 「본사 · 시스템 관리자」가 1차 로그인에서 맞물리지 않는 원천 쪽 빈칸이다 — (a)를 고르면 SPEC-000 변경 없음, (b)(c)는 SPEC-000 개정이 따른다.
3. 화면(로그인 폼 · 병원 고르기) 문구 · 디자인은 두지 않았다 — 디자인이 바뀔 수 있어 백엔드만(2026-11-05 사용자 결정).
