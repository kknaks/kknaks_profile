---
type: work
id: AXKG-WORK-007
title: "WP6: 로그인·유저·역할 권한 — role/authz/유저 관리"
status: done
product: ax-knowledge-graph
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 100
created_at: 2026-07-10
updated_at: 2026-07-10
tags:
  - product/ax-knowledge-graph
  - doc/work
  - status/done
links:
  baselines:
    - "[[baseline-001-ax-knowledge-graph-from-curated-sources|AXKG-BL-001]]"
  decisions:
    - "[[decision-006-role-authz-and-access-boundary|AXKG-DEC-006]]"
  specs:
    - "[[spec-008-simple-token-auth|AXKG-SPEC-008]]"
  works:
    - "[[work-001-mvp-pipeline-scaffold|AXKG-WORK-001]]"
  releases: []
  related: []
---

# WP6: 로그인·유저·역할 권한 — role/authz/유저 관리

WP0이 깐 단일 seed 토큰 로그인 위에 **role(`admin`/`staff`) 모델·접근 경계·유저 관리**를 얹는다. 비목표: 새 인증 방식(OAuth/MFA/refresh)·비밀번호 복잡도·이메일 인증은 만들지 않는다(SPEC-008 Out of scope).

**완료(2026-07-10)**: BE-1~4 + FE-5~7 전부 done. BE pytest 356 passed(신규 25)·alembic 0019(로스터 시드 전담)·실 PG 라운드트립 검증, FE tsc/build 통과·BE 실물 계약 대조 완료. admin 라이브 검증(dev api 재빌드 + 0019 적용, 22명(admin 3) 시드, kknaks role=admin / staff 계정 role=staff 실측). 커밋은 미수행(사용자 일괄).

> 계약 SSOT는 AXKG-SPEC-008(접근 경계 매트릭스·Case Matrix·`role`/`is_active` 필드)과 AXKG-DEC-006이다. 이 문서는 **빌드 계획**이며 SPEC 본문을 복제하지 않는다. 수용 기준은 SPEC-008 §6 AC·§4 Case Matrix를 참조로 둔다.

## Meta

- Baseline: AXKG-BL-001
- Covers spec: AXKG-SPEC-008 (토큰 로그인·유저·역할 권한 경계)
- Depends on work: AXKG-WORK-001 (WP0 — auth 골격·`users`·seed·token)
- Parallel work: 없음 (BE·FE 트랙은 이 WP 내부에서 병렬)
- Follow-up work: 없음
- External dependency: 없음

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | done |
| Progress | 100% |
| Branch/PR | 미커밋(사용자 일괄) |
| Blocker | 없음 (21-html 시안 부재는 설정 화면 톤 차용으로 해소 — 사용자 결정) |
| Next | 커밋(사용자 일괄) |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위(SPEC-008/DEC-006)와 경계 | done |
| Design | kknaks | role 분기 UX·유저 관리/비밀번호 화면 | done (설정 톤 차용) |
| FE | kknaks | role 가드·유저 관리·비밀번호·에러 처리 | done |
| BE | kknaks | 마이그레이션·authz·유저 관리 API·시드 | done |
| QA | kknaks | SPEC-008 AC/Case Matrix 검증 | done (pytest 356·라이브) |
| Ops | kknaks | 배포·prod 시드 | todo (커밋·prod 배포 사용자 일괄) |

## Scope

포함 (SPEC-008 + DEC-006에서만 도출):

- `users`에 `role`(`admin`/`staff`)·`is_active` 추가 마이그레이션
- 활성 22명 로스터 시드 (email 기준 멱등, 기존 seed 계정 흡수, department/position 미저장)
- 라우트 authz: 게이트·소스·설정·유저 관리 = admin / 그래프·채팅 = 로그인만 / 본인 계정 = 본인
- FE 가드 + BE 라우트 authz 이중 강제
- 유저 관리 API·화면 (목록·생성·역할 변경·활성 토글, admin 전용, 생성 기본비번 `1234`)
- 본인 비밀번호 변경 (API·UI, 강제 아님)
- 로그인 후 role 분기 내비/가드 (staff = `/graph`만)
- `FORBIDDEN`·`INACTIVE_ACCOUNT` 에러 처리 (SPEC-008 Case Matrix)

제외:

- admin의 타 유저 비밀번호 리셋(`1234` 재초기화) — SPEC-008 §7 Open Question, WP 범위 밖
- 최초 로그인 강제 비밀번호 변경 (DEC-006 미채택)
- 3값 이상 role·OAuth·MFA·refresh token·이메일 인증·비밀번호 복잡도 규칙

## Code Surface

- Repo / module: ax-graph (WP0 auth 골격 확장)
- 산출물 경계 (구체 파일/클래스/시그니처는 워커 판단 — 여기선 계층·경계만):

| 계층 | 이 WP에서 만드는 것 |
|---|---|
| BE migration | `users.role`·`users.is_active` 컬럼 추가 + 시드 로스터 |
| BE authz | 라우트 권한 가드 (admin/로그인/본인 경계), `FORBIDDEN`·`INACTIVE_ACCOUNT` 응답 |
| BE routes/services | 유저 관리(목록·생성·역할 변경·활성 토글) + 본인 비밀번호 변경 |
| FE app shell/guard | role 분기 내비·클라이언트 가드 (staff=`/graph`만), `/auth/me`·login `role` 소비 |
| FE screens | admin 유저 관리 화면, 본인 비밀번호 변경 UI, 에러 표면 |

- Domain / schema note: `users` 테이블에 컬럼 2개 추가(migration 필요). 실제 컬럼 타입·제약은 코드/migration이 SoT.

## Domain / Schema

| Entity | 이 WP에서 |
|---|---|
| `users` | `role`(admin/staff)·`is_active` 추가, 시드 로스터 반영 |
| `auth_token` | 변경 없음 (WP0 그대로) |

- 상태 / invariant: `is_active=false`면 로그인 차단. role은 2값만. 시드는 email 멱등(재실행 시 중복 계정 없음).
- Migration 필요 여부: 있음 (`users` 컬럼 2개).
- SPEC에 환류해야 하는 외부 resource/status/enum 변경: 없음 예상 (SPEC-008이 이미 확정). 구현 중 계약 이탈 발견 시 SPEC-008로 환류.

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| FE 가드 | login response `user.role` / `GET /auth/me` `role` | role 분기 내비·가드 |
| 전 보호 라우트 | BE authz 가드 | 게이트·소스·설정·유저 관리 admin 강제 |

## Execution

각 Phase는 태스크=커밋 단위다. BE 트랙(1~4)과 FE 트랙(5~7)은 병렬 발주 가능하며, 계약은 SPEC-008(`role` 필드·Case Matrix)로 고정돼 FE는 BE 완료 전에도 계약 기준으로 착수할 수 있다. 상태는 `TODO / IN_PROGRESS / DONE / BLOCKED / SUPERSEDED`.

### Phase BE-1 — role/is_active 마이그레이션 + 시드 로스터

- **Status**: DONE
- **설명**: 권한 모델의 기반. `users`에 role·is_active를 추가하고 활성 22명 로스터를 email 멱등으로 시드한다.
- **작업**:
  - [ ] `users.role`(admin/staff)·`users.is_active` 마이그레이션
  - [ ] 활성 22명 로스터 시드 (email 멱등, 기존 seed 흡수, 기본비번 `1234`, department/position 미저장)
- **검증**:
  - [ ] 시드 2회 실행 시 중복 계정 없음 (SPEC-008 AC)
  - [x] admin 3 / staff 19 role 매핑 정확
- **완료 증거**: PLAN-010-T-003(profile-be). `models/user.py` role(Text, 기본 staff)·is_active(기본 true), alembic **0019**(down `0018`) 컬럼 backfill + CHECK `ck_users_role` + `seed_users` 22명 upsert. 기존 seed 계정은 role/is_active/display_name만 갱신(비번 보존) → `kknaks@medisolveai.com` admin 흡수. department/position/source_user_id 미저장. 실 PG 라운드트립 검증(upgrade head 클린·roster admin 3/staff 19·잘못된 role INSERT `violates check`·downgrade 클린·재upgrade 멱등 22명 중복 없음). 회귀: 0015는 role-free 경량 시드로 분리(role 도입 이전 마이그레이션 보호).

### Phase BE-2 — 라우트 authz 경계

- **Status**: DONE
- **설명**: SPEC-008 접근 경계 매트릭스를 BE 방어선으로 강제한다.
- **작업**:
  - [ ] authz 가드: 게이트·소스·설정·유저 관리 = admin / 그래프·채팅 = 로그인만 / 본인 계정 = 본인
  - [ ] `FORBIDDEN`(경계 밖)·`INACTIVE_ACCOUNT`(비활성 로그인) 응답
- **검증**:
  - [ ] staff가 게이트/소스/설정/유저 관리 API 직접 호출 시 `FORBIDDEN` (SPEC-008 AC)
  - [x] `is_active=false` 로그인 차단 (`INACTIVE_ACCOUNT`)
- **완료 증거**: PLAN-010-T-003(profile-be). `core/security.py` `require_admin`(role≠admin → 403 `FORBIDDEN`). `main.py` 라우터 이중화 — admin 전용: `/sources`·`/gates`·`/documentation-gates`·`/settings`·`/prompts`·`/templates`·`/users`, 로그인만(staff+admin): `/graph/*`·`/documents`, Slack intake는 signing secret 경로 유지. 로그인 시 `is_active=false` → 401 `INACTIVE_ACCOUNT`(`InactiveAccountError`). `/auth/login`·`/auth/me` 응답에 `user.role` 포함. SPEC-008 §4 매트릭스 그대로.

### Phase BE-3 — 유저 관리 API (admin 전용)

- **Status**: DONE
- **설명**: admin이 유저를 생성·관리하는 표면.
- **작업**:
  - [ ] 유저 목록·생성(기본비번 `1234`)·역할 변경·활성 토글 (admin 전용)
- **검증**:
  - [ ] 생성 계정이 `1234`로 로그인 가능 (SPEC-008 AC)
  - [x] 유저 생성·역할 변경·비활성화를 admin만 수행 (staff `FORBIDDEN`)
- **완료 증거**: PLAN-010-T-003(profile-be). `services/users.py`·`schemas/users.py`·`api/routes/users.py` 신설. `GET /users`(목록)·`POST /users`(생성, 기본비번 `1234`, 409 `EMAIL_EXISTS`·422 role)·`PATCH /users/{id}/role`(404 `USER_NOT_FOUND`·422)·`PATCH /users/{id}/active`. 전부 `require_admin`. pytest에서 생성 계정 `1234` 로그인·중복 email·잘못된 role·역할변경·활성토글·404 커버.

### Phase BE-4 — 본인 비밀번호 변경 API

- **Status**: DONE
- **설명**: 본인 자율 비밀번호 변경 (강제 아님).
- **작업**:
  - [ ] 본인 비밀번호 변경 엔드포인트 (본인 스코프)
- **검증**:
  - [x] 본인이 비밀번호 변경 가능, 최초 로그인 강제 없음 (SPEC-008 AC)
- **완료 증거**: PLAN-010-T-003(profile-be). `POST /auth/password`(본인 스코프) — 현재 비번 검증 → 새 비번 교체, 현재 비번 오류 시 401 `INVALID_CREDENTIALS`. 강제 변경 없음(DEC-006 미채택 준수).

### Phase FE-5 — role 분기 내비/가드

- **Status**: DONE
- **설명**: 로그인 후 role로 내비·가드를 분기한다.
- **작업**:
  - [ ] login response·`/auth/me`의 `role` 소비, 클라이언트 상태 배선
  - [ ] staff = `/graph`(그래프+채팅④)+본인 계정만 내비 노출·가드, admin = 전체
- **검증**:
  - [x] staff 내비에 소스/게이트/설정/유저 관리 미노출 (SPEC-008 AC)
- **완료 증거**: PLAN-010-T-004(profile-fe). `lib/access.ts` 신설 — `canAccessPath(role, pathname)`·`defaultLanding(role)`로 SPEC-008 §4 매트릭스를 FE 단일 원천화(staff 허용 prefix = `/graph`·`/account`). `app-shell.tsx` NAV_ITEMS `minRole` 필터(staff=그래프만, admin=소스/그래프/설정/유저 관리) + role 배지 + 비번 변경 링크. `auth-guard.tsx` staff의 admin 화면 접근 시 `/graph` 리다이렉트. login 성공 시 `defaultLanding(role)`(staff→`/graph`, admin→`/`). login·`/auth/me`의 `role` 소비. tsc/build 통과.

### Phase FE-6 — admin 유저 관리 화면

- **Status**: DONE
- **설명**: admin 전용 유저 관리 UI (SPEC-008 U-3).
- **작업**:
  - [ ] 유저 목록·생성·역할 변경·활성 토글 화면 (admin 전용)
- **검증**:
  - [x] admin만 접근, 생성 시 기본비번 `1234` 안내 (SPEC-008 U-3)
- **완료 증거**: PLAN-010-T-004(profile-fe). 실물 표면 = **`/users` 별도 내비**(설정 화면 톤 차용 — 사용자 결정으로 21-html 시안 부재 해소). `lib/api-client/users.ts`(list/create/updateRole/setActive) + `components/users/user-management.tsx` + `app/(app)/users/page.tsx`: 목록(이름·이메일·role·활성)·생성 모달(기본비번 `1234` 안내)·역할 Select 즉시 PATCH·활성 토글(비활성화는 ConfirmDialog). admin 전용 가드. BE 실물 계약(`UserAdminResponse{id,email,display_name,role,is_active}`)과 정확히 일치. `/users` 라우트 정적 생성.

### Phase FE-7 — 비밀번호 변경 UI + 에러 처리

- **Status**: DONE
- **설명**: 본인 비밀번호 변경 UI와 권한/비활성 에러 표면.
- **작업**:
  - [ ] 본인 비밀번호 변경 UI
  - [ ] `FORBIDDEN`·`INACTIVE_ACCOUNT` 에러 표면 (SPEC-008 Case Matrix)
- **검증**:
  - [x] 에러 문구·표시 위치가 SPEC-008 Case Matrix와 정합
- **완료 증거**: PLAN-010-T-004(profile-fe). 실물 표면 = **`/account` 신설**(본인 계정). `components/account/change-password.tsx` + `app/(app)/account/page.tsx`: 현재+새 비번(+확인)·일치/동일 검증·성공 표시, `INVALID_CREDENTIALS`(현재 비번 불일치) 맥락 문구. `changePassword`→`POST /auth/password`(착수 시 `/auth/change-password` 가정 → 실물 BE 경로로 교정). Case Matrix 정합: `INACTIVE_ACCOUNT`→로그인 화면, `FORBIDDEN`→화면 표면. `/account` 라우트 정적 생성.

## Progress Checklist

태스크=커밋 단위 SoT. 워커는 완료 시 체크하고 아래 Change Log에 커밋을 남긴다.

- [x] BE-1 role/is_active 마이그레이션 + 시드 로스터
- [x] BE-2 라우트 authz 경계 (FORBIDDEN/INACTIVE_ACCOUNT)
- [x] BE-3 유저 관리 API (admin 전용)
- [x] BE-4 본인 비밀번호 변경 API
- [x] FE-5 role 분기 내비/가드
- [x] FE-6 admin 유저 관리 화면
- [x] FE-7 비밀번호 변경 UI + 에러 처리

## Change Log

워커가 태스크 완료마다 한 줄씩 추가한다 (SoT).

| Date | Task | Change | Commit/PR |
|---|---|---|---|
| 2026-07-10 | — | WP6 신설 (SPEC-008 확장·DEC-006 기준, PLAN-010-T-002) | — |
| 2026-07-10 | BE-1 | role/is_active 마이그레이션(alembic 0019) + 활성 22명 시드(email 멱등) | 미커밋(사용자 일괄) |
| 2026-07-10 | BE-2 | 라우트 authz(`require_admin`)·`FORBIDDEN`·`INACTIVE_ACCOUNT`·응답 `role` | 미커밋(사용자 일괄) |
| 2026-07-10 | BE-3 | 유저 관리 API `/users`(목록·생성·역할 변경·활성 토글, admin 전용) | 미커밋(사용자 일괄) |
| 2026-07-10 | BE-4 | 본인 비밀번호 변경 `POST /auth/password` | 미커밋(사용자 일괄) |
| 2026-07-10 | FE-5 | role 분기 내비/가드(`lib/access.ts`·auth-guard·defaultLanding) | 미커밋(사용자 일괄) |
| 2026-07-10 | FE-6 | admin 유저 관리 화면 `/users`(설정 톤 차용) | 미커밋(사용자 일괄) |
| 2026-07-10 | FE-7 | 비밀번호 변경 UI `/account` + `FORBIDDEN`/`INACTIVE_ACCOUNT` 처리 | 미커밋(사용자 일괄) |
| 2026-07-10 | QA | BE pytest 356(신규 25)·FE tsc/build·admin 라이브 검증(22명 시드·role 실측) | — |

## Pre-deploy Check

- [x] prod 시드 시 기존 seed 계정(`kknaks@medisolveai.com`)이 admin으로 멱등 흡수됨 (dev 실측: 재upgrade 22명 중복 없음, 비번 보존)
- [x] authz 가드가 응답에 role/권한 관련 비공개 필드를 노출하지 않음 (응답 필드 = email/display_name/role/is_active만)
- [x] 기존 로그인/그래프/채팅 흐름 무영향 (BE 회귀 0 / FE build 통과)
- [ ] prod 배포(0019 적용) — 커밋·배포는 사용자 일괄

## Rollback

- 작업 레포 커밋 단위 revert. `users` 컬럼 마이그레이션은 down migration으로 되돌린다.
- 부분 revert 시 authz 가드만 off하면 WP0 단일-로그인 동작으로 복귀(단, role 컬럼은 유지).

## Done Criteria

- [x] 모든 Phase가 `DONE` 또는 `SUPERSEDED`다.
- [x] SPEC-008 §6 Acceptance Criteria·§4 Case Matrix가 검증 항목에 반영됐다 (test_authz_roles.py 25건).
- [x] 필요한 테스트/검증이 끝났다 (BE pytest 356·FE tsc/build·admin 라이브).
- [x] product `log.md`와 `30-work/README.md`가 갱신됐다 (PLAN-010-T-005).

## Open Issues

- ~~유저 관리·비밀번호 변경 화면의 `21-html/` 시안 부재~~ → **해소**(2026-07-10, 사용자 결정): 기존 설정 화면 톤을 차용해 `/users`·`/account`로 구현. 별도 21-html 시안 미생성.
- admin의 타 유저 비밀번호 리셋(`1234` 재초기화) 제공 여부는 SPEC-008 §7 OQ — **open 유지**. 결정되면 별도 Phase로 추가.

## Related

- SPEC: AXKG-SPEC-008 (frontmatter `links.specs`)
- Decision: AXKG-DEC-006
- Work: AXKG-WORK-001 (frontmatter `links.works`)
