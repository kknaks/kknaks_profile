---
type: work
id: STL-WORK-002
title: "Mobile Apple Sign-In integration"
status: todo
product: study-timelapse
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 0
created_at: 2026-06-21
updated_at: 2026-06-21
tags:
  - product/study-timelapse
  - doc/work
  - status/todo
links:
  baselines: []
  decisions: []
  specs:
    - "[[spec-009-auth-onboarding|STL-SPEC-009]]"
    - "[[spec-008-mobile-revenuecat-integration|STL-SPEC-008]]"
  works: []
  releases: []
  related: []
---

# Mobile Apple Sign-In integration

iOS 앱 로그인 화면에 Sign in with Apple을 추가하고, 기존 backend `POST /auth/apple` 계약에 연결해 Google 단독 로그인 gap을 닫는다. 결제/구독 상태머신 변경은 이 work 범위가 아니다.

> 1 파일 = 1 work = 빌드 계획. 이 문서는 구현 전에 범위와 검증 조건만 고정한다.
> SPEC의 외부 계약 본문은 복제하지 않고 frontmatter `links.specs`와 index에서 연결한다.

## Meta

- Baseline: 없음
- Covers spec: STL-SPEC-009, STL-SPEC-008
- Depends on work: STL-WORK-001 완료됨
- Parallel work: STL-SPEC-006 RevenueCat `INITIAL_PURCHASE period_type` 분기와 병렬 가능
- Follow-up work: TestFlight submission / release work
- External dependency: Apple Developer capability, bundle identifier, EAS credentials, code repo `/Users/kknaks/git/toy_pr2/study_timelapse`

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | todo |
| Progress | 0% |
| Branch/PR | TBD |
| Blocker | Apple Developer Sign in with Apple capability 설정 확인 필요 |
| Next | Apple capability / bundle id / Expo dependency 확인 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | TestFlight/App Review 요구사항 범위 확정 | todo |
| Design | kknaks | 로그인 화면 내 Apple/Google 버튼 배치와 copy | todo |
| FE | kknaks | AppleAuthentication SDK 연동, login flow 구현 | todo |
| BE | kknaks | 기존 `/auth/apple` aud/client_id 설정 확인 | todo |
| QA | kknaks | 실제 iOS Apple Sign-In E2E 검증 | todo |
| Ops | kknaks | Apple capability, EAS/App Store Connect 설정 확인 | todo |

## Scope

포함:

- `expo-apple-authentication` 추가 및 iOS에서만 Apple 로그인 버튼 노출
- `frontend/mobile/app/login.tsx`에 Apple 버튼과 loading/error 상태 추가
- mobile API client에 `loginWithApple` 함수 추가 또는 기존 auth API 확장
- Apple identity token + name + timezone + terms/privacy flags를 backend `POST /auth/apple`로 전송
- 로그인 성공 후 token 저장, RevenueCat `logIn(user.id)`, query invalidation, 신규/기존 사용자 라우팅을 Google flow와 동일하게 처리
- backend `APPLE_CLIENT_ID` / `apple_client_id`가 iOS bundle id와 맞는지 확인
- Apple Developer / App Store Connect / EAS capability 설정 확인

제외:

- Backend Apple JWT 검증 로직 재작성
- Apple 계정 탈퇴/연동 해제 정책
- RevenueCat subscription event state machine 변경
- Android Google Play 로그인 정책 변경

## Code Surface

- Repo / module: `study_timelapse/frontend/mobile/`, `study_timelapse/backend/`
- 만질 파일 후보:

| 경로 후보 | 설명 |
|---|---|
| `frontend/mobile/package.json` | `expo-apple-authentication` dependency 추가 |
| `frontend/mobile/app/login.tsx` | Apple 로그인 버튼, 상태, error handling |
| `frontend/mobile/src/api/auth.ts` | `loginWithApple` API 함수 추가 |
| `frontend/mobile/app.json` 또는 EAS config | iOS capability/config 필요 여부 확인 |
| `backend/app/config.py` / deploy env | `apple_client_id`가 bundle id와 일치하는지 확인 |
| `backend/app/api/v1/auth.py` / `schemas/auth.py` | 기존 계약 확인. 변경은 최소화 |

- Domain / schema note: DB/migration 없음. provider는 기존 `google|apple` 모델 재사용.

## Domain / Schema

해당 없음.

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| TestFlight/App Review | Sign in with Apple | Google 로그인 제공 앱의 iOS 심사 리스크 제거 |
| RevenueCat mobile SDK | `loginRevenueCat(user.id)` | Apple 로그인 후에도 Google 로그인과 동일한 app_user_id 매핑 |
| Auth onboarding | `is_new` 분기 | 신규 Apple 사용자는 terms → trial-intro로 이동 |

## Internal Interface Contract

- Apple 로그인은 iOS에서만 노출한다. Web/Android에서는 숨긴다.
- Google 로그인 flow와 동일하게 access/refresh token 저장, `setLoggedIn(true)`, `queryClient.invalidateQueries()`, 신규/기존 라우팅을 수행한다.
- Apple `fullName`은 첫 로그인에서만 올 수 있으므로 없으면 `name: null`로 전송한다.
- 사용자가 Apple 로그인 sheet를 취소하면 alert 없이 조용히 종료한다.
- backend `audience`는 실제 iOS bundle identifier와 일치해야 한다.

## Execution

각 Phase의 상태는 `TODO / IN_PROGRESS / DONE / BLOCKED / SUPERSEDED` 중 하나로 갱신한다.

### Phase 1 — Capability and contract check

- **Status**: TODO
- **설명**: 구현 전에 Apple Developer/EAS/backend 설정과 기존 API 계약이 맞는지 확인한다.
- **작업**:
  - [ ] iOS bundle id 확인
  - [ ] Apple Developer Sign in with Apple capability 확인
  - [ ] EAS/App Store Connect capability 또는 entitlements 필요 여부 확인
  - [ ] backend `apple_client_id`가 bundle id와 일치하는지 확인
  - [ ] `POST /auth/apple` request/response 계약 재확인
- **검증**:
  - [ ] 설정 mismatch 여부가 문서화됐다.
  - [ ] 구현 착수 전 blocker가 없다.
- **완료 증거**: 미작성

### Phase 2 — Mobile implementation

- **Status**: TODO
- **설명**: 로그인 화면에 Apple Sign-In을 추가하고 backend auth flow에 연결한다.
- **작업**:
  - [ ] `expo-apple-authentication` dependency 추가
  - [ ] `loginWithApple` API 함수 추가
  - [ ] `login.tsx`에 Apple button 추가
  - [ ] identity token/name/timezone을 `/auth/apple`로 전송
  - [ ] token 저장, RevenueCat logIn, 신규/기존 route 분기 연결
  - [ ] 취소/실패 error handling 정리
- **검증**:
  - [ ] TypeScript 검증 통과
  - [ ] Google 로그인 기존 flow 회귀 없음
- **완료 증거**: 미작성

### Phase 3 — iOS E2E QA

- **Status**: TODO
- **설명**: 실제 iOS simulator/device에서 Apple 로그인과 온보딩 분기를 검증한다.
- **작업**:
  - [ ] Apple 로그인 sheet 표시 확인
  - [ ] 신규 사용자 약관 → trial-intro 분기 확인
  - [ ] 기존 사용자 홈 진입 확인
  - [ ] RevenueCat logIn 호출 이후 구독 상태 조회 확인
  - [ ] Apple 로그인 취소 시 화면 유지 확인
- **검증**:
  - [ ] Apple 로그인 E2E 성공
  - [ ] Google 로그인 기존 flow 성공
  - [ ] TestFlight 심사 전 auth blocker 없음
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] Apple Developer capability가 켜져 있다.
- [ ] Bundle ID와 backend `apple_client_id`가 일치한다.
- [ ] Apple 로그인 버튼이 iOS에서 보이고, non-iOS에서는 노출되지 않는다.
- [ ] Google 로그인과 Apple 로그인 모두 token 저장/온보딩 분기가 동작한다.
- [ ] 신규 env/credential이 배포 환경에 반영됐다.

## Rollback

- mobile Apple button/API call/dependency PR revert.
- Apple capability는 켜져 있어도 Google flow에는 영향 없어야 한다.
- backend env 변경이 있었다면 이전 `apple_client_id`로 복구.

## Done Criteria

- [ ] 모든 Phase가 `DONE` 또는 `SUPERSEDED`다.
- [ ] 모바일 Apple Sign-In이 end-to-end 동작한다.
- [ ] SPEC-009의 Apple Sign-In gap이 닫혔다.
- [ ] product `log.md`와 `30-work/README.md`가 갱신됐다.

## Open Issues

- Apple Developer capability / EAS entitlements 설정 상태 확인 필요.
- backend `apple_client_id` 기본값(`com.focustimelapse.app`)과 실제 bundle id(`com.kknaks.studytimelapse`) 일치 여부 확인 필요.

## Related

- SPEC: STL-SPEC-009, STL-SPEC-008
