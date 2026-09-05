---
type: work
id: WORK-002
title: "로그인 · 세션 — Bearer 발급·갱신 · 키체인 저장소 · 세션 가드"
status: todo
product: "task-management"
work_type: new-feature
owner: ""
roles:
  pm: ""
  design: ""
  fe: ""
  be: ""
  qa: ""
  ops: ""
progress: 0
created_at: 2026-09-05
updated_at: 2026-09-05
tags:
  - product/task-management
  - doc/work
  - status/todo
links:
  baselines: [BASE-001]
  decisions: [DEC-001]
  specs: [SPEC-001]
  works: [WORK-001]
  releases: []
  related: []
---

# 로그인 · 세션 — Bearer 발급·갱신 · 키체인 저장소 · 세션 가드

시드 계정으로 **앱에 들어가고, 앱을 껐다 켜도 로그인이 유지된다**(「유지」 체크 시). 로그아웃은 확인 모달을 지난다. 프로필·경력 화면은 만들지 않는다 — 개인 설정 그룹이다.

> 1 파일 = 1 work = **빌드 계획**. dev가 이 문서만 보고 PR 분리 / 일정 / 작업 시작이 가능해야 한다.
> SPEC의 외부 계약 본문은 복제하지 않고 frontmatter `links.specs`와 index에서 연결한다.

## Meta

- Baseline: BASE-001
- Covers spec: **SPEC-001**(로그인 · 세션 · 로그아웃)
- Depends on work: **WORK-001**(계정 테이블 · 시드 계정 · `Settings` · 예외 핸들러 · 앱 셸 기동)
- Parallel work: 없음 — WORK-003 은 이 work 의 세션 가드 위에서 검증된다
- Follow-up work: WORK-003(업무 설정) · 개인 설정 그룹(프로필·경력·비밀번호 변경)
- **External dependency**
  - **코드 레포는 별도다** — `github.com/kknaks/task_management`. 이 워크트리에 코드를 만들지 않는다
  - **OS 키체인**(Tauri 플러그인) — WORK-001 Phase 4 에서 의존성만 추가돼 있다. **이 work 에서 처음 실제로 쓴다**
  - 시드 계정(`SEED_LOGIN_ID`·`SEED_PASSWORD`) — WORK-001 Phase 2 산출물

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner |  |
| Status | todo |
| Progress | 0% |
| Branch/PR |  |
| Blocker | WORK-001 미완 |
| Next | Phase 1 — 인증 API |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | 범위 확정 · SPEC-001 대조 | todo |
| Design |  | 로그인 화면 정정 반영(「아이디」·링크 제거) · 확인 모달 · v2 표시 | todo |
| FE |  | 토큰 저장소 · 요청 파이프라인 · 로그인 화면 · 세션 가드 · 앱 셸 | todo |
| BE |  | 인증 4표면 · 해시·JWT · refresh 회전 · 인가 의존성 | todo |
| QA |  | Phase 검증(앱 창 E2E) · 저장소 격리 정적 검사 | todo |
| Ops |  | JWT 시크릿 관리 · CORS 목록 | todo |

## Scope

포함:

- 인증 4표면(로그인 · 갱신 · 로그아웃 · 세션 조회) · bcrypt · JWT · **refresh 회전과 재사용 감지**
- 라우터 단위 인가 의존성(`require_account`) — **로그인·갱신·헬스만 예외**
- **토큰 저장소 추상화 한 파일** — 「유지」 체크 시 OS 키체인, 미체크 시 메모리
- 요청 파이프라인 — Bearer 부착 · **401 갱신 1회 + 원 요청 1회 재시도** · 동시 401 시 갱신 1회만
- **로그인 화면**(정정 반영) · **세션 가드 레이아웃** · 앱 셸(사이드바 8메뉴)
- **설정 좌측 메뉴 카드** · **로그아웃 확인 모달**(600) · **v2 표시 공통 컴포넌트**

제외:

- 프로필·경력·목소리·연동 관리·비밀번호 변경 → 개인 설정 그룹(SPEC-010)
- 유형·프로젝트 화면 → **WORK-003**
- 회원가입·비밀번호 찾기·소셜 로그인 실동작 → v1 에 없다/v2
- `/tasks` 본문 → 내 업무 그룹(이 work 는 **셸만** 세운다)

## Code Surface

- Repo / module: `github.com/kknaks/task_management` — `app/back`(BE) · `app/front`(FE)
- 만질 파일 후보

| 경로 후보 | 설명 |
|---|---|
| `app/back/core/security.py` | bcrypt 해시·검증 · JWT 발급/검증 · refresh 토큰 생성과 해시 |
| `app/back/api/auth_router.py` | `login` · `refresh` · `logout` · `session` |
| `app/back/api/deps.py` | `require_account` 구현(라우터 단위로 건다) |
| `app/back/service/auth_service.py` | 자격 증명 검증 · 세션 발급 · **회전과 재사용 감지** |
| `app/back/repository/account_repository.py` · `auth_session_repository.py` | ORM/SQL 만 |
| `app/back/schemas/auth.py` · `dto/auth.py` | FE 계약(camelCase alias) / 내부 dto(frozen dataclass) |
| `app/back/tests/test_auth.py` | 갱신·회전·재사용·잠김 없음 |
| `app/front/src/lib/auth/tokenStore.ts` | **★ 교체 지점** — `get()`·`set(token, persist)`·`clear()` 셋. **저장소 API 를 부르는 유일한 파일** |
| `app/front/src/lib/auth/session.ts` | 로그인·갱신·로그아웃 상태 |
| `app/front/src/lib/api/client.ts` | Bearer 부착 · 401 갱신 1회 · 진행 중 갱신 Promise 공유 |
| `app/front/src/features/auth/components/LoginScreen.tsx` · `api.ts` · `types.ts` | 로그인 화면과 호출 |
| `app/front/src/app/(auth)/layout.tsx` · `(auth)/login/page.tsx` | 셸 밖 브랜드 패널 + 폼 |
| `app/front/src/app/(app)/layout.tsx` | **세션 가드**(미들웨어를 못 쓴다 — FE §4-3) + AppShell |
| `app/front/src/components/shared/AppShell.tsx` · `Sidebar.tsx` | 8메뉴. 홈·채팅은 라우트 없이 안내 |
| `app/front/src/components/shared/ConfirmModal.tsx` | 모달 600 공통 프레임(로그아웃·이후 삭제 모달이 재사용) |
| `app/front/src/components/shared/V2Gate.tsx` | **아직 열리지 않은 기능 표시** — 문구 두 가지(v2 / 곧 제공) |
| `app/front/src/app/(app)/settings/layout.tsx` | 메뉴 카드 260 + 로그아웃·계정 삭제 · 버전 캡션 |
| `app/front/src/app/(app)/tasks/page.tsx` | **셸만** — 본문은 내 업무 그룹이 채운다 |
| `app/front/src-tauri/` | 키체인 플러그인 권한·설정 |

- Domain / schema note: **마이그레이션 없음.** WORK-001 이 만든 `account`·`auth_session` 을 그대로 쓴다

## Domain / Schema

| Entity | 역할 |
|---|---|
| `account` | 로그인 식별자·비밀번호 해시. **읽기만** 한다(계정 생성 경로 없음) |
| `auth_session` | refresh 해시 · 만료 · 무효화 시각. **회전마다 새 행** |

- 상태 / invariant: `domains/account.md` **A-7**(refresh 1회용 · 재사용 시 그 계정의 유효 세션 전부 차단) · **A-8**(로그인 실패 횟수를 세지 않는다) · **A-2**(해시만 저장)
- Migration 필요 여부: **없음**
- SPEC 에 환류해야 하는 변경: **`invalid_refresh_token` 코드**가 아키텍처 §8-2 표에 없다(SPEC-001 S001-OQ-2) — 코드 표 반영은 코디 소관, 구현은 SPEC-001 §4 Case Matrix 를 따른다

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| WORK-003 및 이후 전부 | `require_account` · `client.ts` 의 Bearer·401 재시도 · `(app)/layout.tsx` 가드 | 모든 화면이 세션 뒤에 있다 |
| 이후 전 화면 | `ConfirmModal` · `V2Gate` · `AppShell` | 삭제 모달·v2 표시가 여기서 나온 컴포넌트를 재사용한다 |
| 개인 설정 그룹 | 설정 레이아웃(메뉴 카드) | 「개인 설정」 항목 본문만 채우면 된다 |

## Internal Interface Contract

외부 계약(요청/응답·에러 코드)은 **SPEC-001 §4** 가 정본이다. 후속 work 가 의존하는 내부 접점만 고정한다.

| 접점 | 계약 |
|---|---|
| `tokenStore` | `get(): string \| null` · `set(token: string, persist: boolean)` · `clear()` **셋뿐**. `persist=true` → OS 키체인, `false` → 메모리 변수. **다른 파일에서 키체인·`localStorage`·`sessionStorage` 를 부르면 리뷰 반려**(FE §4-1) |
| access 토큰 | **저장소에 넣지 않는다.** 메모리에만 둔다. 앱을 껐다 켜면 refresh 로 다시 받는다 |
| `client.ts` | 모든 호출이 지난다. `401 token_expired` → 갱신 1회 → 원 요청 1회 재시도 → 그래도 401 이면 `clear()` + 로그인 화면. **동시 401 은 갱신 한 번만**(진행 중 Promise 공유) |
| `require_account` | 라우터 단위 `dependencies=[...]` 로 건다. 개별 함수에서 빠뜨릴 여지를 없앤다(BE §9). 반환은 `account_id` |
| `V2Gate` | children 을 **그대로** 그리고 이벤트만 가로챈다. 문구 두 가지 — v2 대상 「v2에서 제공됩니다」 / 홈·채팅 「곧 제공됩니다」(§C-9). **컴포넌트를 둘로 나누지 않는다** |
| `ConfirmModal` | 600 · 제목 → 요약 → 경고 슬롯 → 취소/확인. **드로어가 열린 상태에서 열면 개발 모드에서 throw**(FE §6-2) |

## Execution

### Phase 1 — 인증 API (백엔드)

- **Status**: TODO
- **설명**: 화면 없이 **토큰이 도는 상태**를 먼저 만든다. `curl` 로 로그인 → 갱신 → 로그아웃이 왕복하면 프론트를 붙일 수 있다.
- **작업**:
  - [ ] `core/security.py` — bcrypt 해시 검증 · access JWT(1시간) 발급/검증 · refresh 토큰 생성 + **해시 저장**
  - [ ] `service/auth_service.py` — 자격 증명 검증(**실패 횟수를 세지 않는다**) · 세션 발급 · **회전**(쓴 토큰 즉시 무효) · **재사용 감지 시 그 계정 세션 전부 무효화**
  - [ ] `repository/account_repository.py` · `auth_session_repository.py` — dto 만 반환
  - [ ] `api/auth_router.py` 4표면 + `schemas/auth.py`(camelCase alias) · `dto/auth.py`
  - [ ] `api/deps.py` `require_account` — 라우터 단위 게이트. **로그인·갱신·헬스만 예외**
  - [ ] `tests/test_auth.py` — 성공 · 자격 증명 실패 · 만료 → 갱신 · **회전 후 옛 토큰 거부** · **재사용 감지 시 전체 무효** · 남의 자원 404
- **검증**:
  - [ ] `curl` 로 시드 계정 로그인 → `accessToken`·`refreshToken`·`expiresIn` 을 받는다
  - [ ] 잘못된 비밀번호는 **401 `invalid_credentials`** 이고, 다섯 번 반복해도 **응답이 달라지지 않는다**(잠기지 않는다)
  - [ ] 갱신을 부르면 **새 refresh 가 오고 옛 refresh 는 즉시 거부**된다(`invalid_refresh_token`)
  - [ ] 무효화된 refresh 를 다시 쓰면 **그 계정의 다른 세션도 끊긴다**
  - [ ] 토큰 없이 `session` 을 부르면 401, 유효한 토큰이면 계정 요약이 온다
  - [ ] `pytest` 통과
- **완료 증거**: 미작성

### Phase 2 — 토큰 저장소 · 요청 파이프라인 · 로그인 화면

- **Status**: TODO
- **설명**: 앱 창에서 **실제로 로그인해 들어가는** 단계. 「유지」 체크가 키체인/메모리로 갈리는 것이 이 Phase 의 핵심이다.
- **작업**:
  - [ ] `lib/auth/tokenStore.ts` — 인터페이스 셋. `persist=true` → **OS 키체인**, `false` → 메모리
  - [ ] `lib/api/client.ts` — Bearer 부착 · 401 갱신 1회 + 재시도 1회 · **진행 중 갱신 Promise 공유** · 실패 시 `clear()` + 로그인 이동
  - [ ] `features/auth` — 로그인 호출·타입·화면. **라벨 「아이디」, 비밀번호 찾기·회원가입 링크 없음**(§A-9)
  - [ ] `(auth)/layout.tsx`·`login/page.tsx` — 브랜드 그라디언트 패널(유동) + 폼 400 고정. 반응형 3구간(SPEC-001 U-8)
  - [ ] `(app)/layout.tsx` — **세션 가드**(확인 중에는 로그인 화면을 깜빡 보이지 않는다) + `AppShell`·`Sidebar`
  - [ ] `tasks/page.tsx` — 셸만(빈 본문)
- **검증**:
  - [ ] 앱 창에서 시드 계정으로 로그인하면 **앱 셸이 뜨고 `/tasks` 로 간다**
  - [ ] 「로그인 상태 유지」를 **켜고** 로그인 → **앱을 완전히 껐다 켜면 로그인 화면 없이 들어간다**
  - [ ] **끄고** 로그인 → 껐다 켜면 **로그인 화면**이고 만료 토스트가 뜨지 않는다
  - [ ] 비밀번호를 틀리면 폼 안에 인라인 안내가 뜨고 **입력값이 남는다**
  - [ ] 서버에서 세션을 무효화한 뒤 조작하면 **로그인 화면으로 가고 갱신 루프가 돌지 않는다**(네트워크 탭에 refresh 가 1회)
  - [ ] **정적 검사**: `tokenStore.ts` **밖에서** 키체인·`localStorage`·`sessionStorage` 를 부르는 코드가 **하나도 없다**(grep 결과를 완료 증거에 붙인다)
  - [ ] 「유지」 미체크로 로그인한 뒤 **키체인에 아무것도 남지 않는다**
- **완료 증거**: 미작성

### Phase 3 — 설정 셸 · 로그아웃 모달 · v2 표시 컴포넌트

- **Status**: TODO
- **설명**: 로그아웃 왕복을 닫고, **이후 모든 화면이 재사용할 두 컴포넌트**(확인 모달·v2 표시)를 여기서 만든다.
- **작업**:
  - [ ] `components/shared/ConfirmModal.tsx` — 600 공통 프레임(경고 슬롯 포함)
  - [ ] `components/shared/V2Gate.tsx` — 불투명도 0.45 · 포인터/키보드 가로채기 · **토스트 문구 두 가지**
  - [ ] `settings/layout.tsx` — 메뉴 카드(개인/업무/연동) + 하단 로그아웃·계정 삭제 + 버전·마지막 저장 캡션
  - [ ] 로그아웃 흐름 — 확인 모달 → 로그아웃 호출 → **실패해도 토큰은 지운다** + 실패 토스트
  - [ ] v2 표시 적용 — 소셜 버튼 · 하단 3링크 · 「계정 삭제」 · 사이드바 홈·채팅
- **검증**:
  - [ ] 설정 → 「로그아웃」이 **확인 모달(600)** 을 열고, 「취소」하면 로그인 상태가 유지된다
  - [ ] 「유지」로 로그인했으면 모달에 「**저장된 로그인 정보도 함께 지워집니다**」가 보인다
  - [ ] 「로그아웃」 확인 후 **앱을 껐다 켜도 로그인 화면**이다(키체인이 비었다)
  - [ ] 「회사 계정으로 계속하기」·「계정 삭제」·홈·채팅을 누르면 **토스트만** 뜨고 **네트워크 요청이 나가지 않는다**(홈·채팅은 「곧 제공됩니다」)
  - [ ] 「계정 삭제」는 **모달이 열리지 않는다**
  - [ ] 창을 1280~1439 로 줄이면 로그인 화면의 **브랜드 패널이 사라지고 폼이 가운데**로 온다
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] `JWT_SECRET` 이 레포에 없고 환경에서만 온다(기본값 없음)
- [ ] 응답 어디에도 **비밀번호 해시·refresh 원문**이 실리지 않는다
- [ ] CORS 는 **명시 목록**이고 `allow_credentials=False` 다(쿠키를 쓰지 않는다)
- [ ] 로그인 실패 응답이 **아이디 존재 여부를 흘리지 않는다**(문구 하나로 통일)

## Rollback

- **스키마 변경이 없다** — 되돌릴 마이그레이션이 없다. 세션 행이 남으면 `auth_session` 을 비우면 그만이다
- **백엔드**: 라우터 미등록으로 인증 표면을 즉시 걷어낼 수 있다(`main.py` 조립 한 줄). 단 그 순간 프론트는 로그인 화면에서 멈춘다
- **프론트**: 브랜치 폐기. 키체인에 남은 값은 사용자가 로그아웃하거나 앱 데이터 삭제로 지운다 — **되돌림 절차에 「키체인 항목 삭제」를 포함**한다
- 부분 revert 시: WORK-001 의 연결 확인 화면이 루트에 남아 있어야 앱이 빈 창이 되지 않는다(Phase 2 에서 대체하므로 **함께 되돌린다**)

## Done Criteria

- [ ] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다.
- [ ] **SPEC-001 §6 Acceptance 13개 항목이 전부 확인**됐다.
- [ ] 토큰 저장소 격리 정적 검사 결과가 완료 증거에 붙어 있다.
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다.

## Open Issues

- **`invalid_refresh_token` 코드가 아키텍처 §8-2 표에 없다**(SPEC-001 S001-OQ-2). 구현은 SPEC-001 §4 를 따르되, 코드 표 갱신은 코디 소관
- **로그인 후 진입 지점**(SPEC-001 S001-OQ-3) — `/tasks` 로 보내는데 그 화면이 이 그룹에서는 **빈 본문**이다. 내 업무 그룹 전까지 임시로 설정 화면을 기본 진입으로 둘지는 코디 판단
- **하단 3링크(약관·개인정보·고객지원)** — 정책 근거가 없어 v2 표시로 처리했다(SPEC-001 S001-OQ-4). 빼는 것이 맞다면 DEC-001 갱신 필요
- **키체인 접근이 macOS·Windows 에서 갈릴 수 있다** — Phase 2 검증은 macOS 기준이다. Windows 확인 시점은 WORK-001 Open Issues 와 함께 잡는다
- **「마지막 저장」 캡션 범위**(SPEC-001 S001-OQ-1) — 지금 계약은 **화면 수명 동안만** 유지다. 개인 설정 그룹에서 다시 본다

## Related

- SPEC: SPEC-001 (frontmatter `links.specs`)
- Work: WORK-001 (선행) · WORK-003 (후속)
