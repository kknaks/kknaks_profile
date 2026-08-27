---
type: work
id: STL-WORK-001
title: "English app copy audit"
status: done
product: study-timelapse
work_type: polish
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: ""
  qa: kknaks
  ops: ""
progress: 100
created_at: 2026-06-20
updated_at: 2026-06-20
tags:
  - product/study-timelapse
  - doc/work
  - status/done
links:
  baselines: []
  decisions: []
  specs:
    - "[[spec-001-recording-state-machine|STL-SPEC-001]]"
    - "[[spec-002-capture-pipeline|STL-SPEC-002]]"
    - "[[spec-008-mobile-revenuecat-integration|STL-SPEC-008]]"
    - "[[spec-009-auth-onboarding|STL-SPEC-009]]"
    - "[[spec-010-session-domain|STL-SPEC-010]]"
    - "[[spec-012-stats-domain|STL-SPEC-012]]"
  works: []
  releases: []
  related: []
---

# English app copy audit

Study Timelapse iOS app에 노출되는 한글 알림, 모달, 토스트, 권한 안내, 버튼 문구를 전부 영어로 통일한다. API 계약, 결제 정책, Apple Sign-In 미연동 같은 기능 변경은 이 work 범위가 아니다.

> 1 파일 = 1 work = 빌드 계획. 이 문서는 코드 수정 전 audit와 실행 범위를 고정한다.
> SPEC의 외부 계약 본문은 복제하지 않고 frontmatter `links.specs`와 index에서 연결한다.

## Meta

- Baseline: 없음
- Covers spec: STL-SPEC-001, STL-SPEC-002, STL-SPEC-008, STL-SPEC-009, STL-SPEC-010, STL-SPEC-012
- Depends on work: 없음
- Parallel work: STL-SPEC-006 RevenueCat trial 분기, STL-SPEC-009 Apple Sign-In과 병렬 가능
- Follow-up work: 실제 코드 수정 PR
- External dependency: code repo `github.com/kknaks/study_timelapse`; local clone `/Users/kknaks/git/toy_pr2/study_timelapse`

## Work Summary

| Field | Value |
|---|---|
| Type | polish |
| Owner | kknaks |
| Status | done |
| Progress | 100% |
| Branch/PR | TBD |
| Blocker | 없음 |
| Next | 후속 work 선정 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 앱 언어 정책: 사용자 노출 문구는 영어로 통일 | done |
| Design | kknaks | 모달/알림 문구 tone 검수 | done |
| FE | kknaks | React Native 화면, Alert, Modal, Toast, i18n 리소스 수정 | done |
| BE |  | API 변경 없음 | n/a |
| QA | kknaks | 주요 플로우에서 한글 노출 잔존 여부 확인 | done |
| Ops |  | 배포/운영 변경 없음 | n/a |

## Scope

포함:

- 모바일 앱 사용자 노출 문구 중 한글을 영어로 변경
- `Alert.alert`, modal title/body/button, toast/snackbar, permission 안내, loading/error message, paywall/onboarding 안내 문구 점검
- 앱 주요 플로우 smoke QA: login/onboarding, session setup, focus, stop confirmation, generating, result, saving, stats, paywall
- i18n 리소스가 있다면 기본 locale과 fallback 정책 확인

제외:

- Apple Sign-In 신규 연동
- RevenueCat trial period_type backend 분기
- API schema, DB migration, 서버 에러 코드 구조 변경
- 디자인 레이아웃 리디자인

## Code Surface

- Repo / module: `study_timelapse/frontend/mobile/`
- 만질 파일 후보:

| 경로 후보 | 설명 |
|---|---|
| `frontend/mobile/app/**/*.tsx` | expo-router 화면, 모달, 알림, 버튼 문구 |
| `frontend/mobile/src/**/*.ts(x)` | hooks, api error mapper, i18n/util 문구 |
| `frontend/mobile/modules/timelapse-creator/**` | native module error message가 사용자에게 전달되는 경우만 |
| `frontend/mobile/package.json` | i18n 관련 dependency 확인만. 신규 dependency는 원칙적으로 추가하지 않음 |

- Domain / schema note: DB/migration 없음. 외부 API 계약 변경 없음.

## Domain / Schema

해당 없음.

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| 출시 QA | 사용자 노출 copy | 영어 문구 통일 여부를 심사/QA 전 확인 |
| App Store review | 앱 UI copy | iOS 앱 전반이 영어로 보이는지 확인 |

## Internal Interface Contract

- 사용자에게 직접 보이는 문자열은 기본 영어 문장으로 유지한다.
- 한국어 개발 주석, 내부 로그, 문서 문자열은 이 work의 차단 대상이 아니다.
- API에서 내려오는 서버 에러가 그대로 노출된다면 mobile에서 영어 사용자 메시지로 매핑한다.
- 버튼 문구는 짧은 명령형 영어를 우선한다. 예: `Cancel`, `Continue`, `Save`, `Try Again`, `Start Focus Session`.

## Execution

각 Phase의 상태는 `TODO / IN_PROGRESS / DONE / BLOCKED / SUPERSEDED` 중 하나로 갱신한다.

### Phase 1 — Copy audit

- **Status**: DONE
- **설명**: 모바일 코드 전체에서 사용자 노출 가능성이 있는 한글 문자열을 찾고, 내부 로그/주석과 실제 UI copy를 분리한다.
- **작업**:
  - [x] local code repo 위치 확인
  - [x] `frontend/mobile`에서 한글 문자열 grep
  - [x] Alert/Modal/Toast/permission/loading/error 문구 목록화
  - [x] 내부 로그/주석/테스트 문자열은 제외 표시
- **검증**:
  - [x] 한글 문자열 목록에 화면/파일/사용자 노출 여부가 표시됐다.
  - [x] 수정 대상과 제외 대상이 분리됐다.
- **완료 증거**: local clone `/Users/kknaks/git/toy_pr2/study_timelapse`. `rg -n "[가-힣]" frontend/mobile/app frontend/mobile/src -g '*.{ts,tsx}' -g '!**/__tests__/**'` 기준 사용자 노출 수정 대상은 `app/focus.tsx` stop alert/modal/indicator, `app/paywall.tsx` feature labels/login/alerts/legal note, `app/generating.tsx` loading text, `app/session-setup.tsx` quota fallback, `app/legal/{terms,privacy,refund}.tsx` meta labels, `src/legal/contents.ts` legal document body/title/version/date/draft warning, `src/constants/strings.ts` trial legal note. 주석, tests, native comments, color comments는 제외.

### Phase 2 — English copy replacement

- **Status**: DONE
- **설명**: Phase 1에서 사용자 노출로 분류된 문구를 영어로 교체한다.
- **작업**:
  - [x] 알림/모달 title/body/button 영문화
  - [x] 권한/오류/빈 상태/로딩 문구 영문화
  - [x] paywall/onboarding/stats/focus flow 문구 tone 통일
  - [x] 서버 에러 원문 노출 지점이 있으면 mobile 영어 메시지로 매핑
- **검증**:
  - [x] `frontend/mobile` 사용자 노출 경로에 한국어 문자열이 남지 않았다.
  - [x] TypeScript/lint/build 또는 가능한 모바일 검증 명령이 통과했다.
- **완료 증거**: `/Users/kknaks/git/toy_pr2/study_timelapse/frontend/mobile`에서 `npx tsc --noEmit` 통과. 사용자 노출 패턴 grep `rg -n "Alert\\.alert\\([^\\n]*[가-힣]|<Text[^>]*>[^\\n]*[가-힣]|label: '[^']*[가-힣]|title: '[^']*[가-힣]|subtitle: '[^']*[가-힣]|draftWarning: '[^']*[가-힣]|effectiveDate: '[^']*[가-힣]|version: '[^']*[가-힣]" frontend/mobile/app frontend/mobile/src -g '*.{ts,tsx}'` 0건. 변경 파일: `app/focus.tsx`, `app/paywall.tsx`, `app/generating.tsx`, `app/session-setup.tsx`, `app/legal/{terms,privacy,refund}.tsx`, `src/constants/strings.ts`, `src/legal/contents.ts`.

### Phase 3 — Flow QA

- **Status**: DONE
- **설명**: 주요 사용자 플로우에서 실제 화면, 모달, 알림에 한글이 남지 않았는지 확인하고 저장 후 navigation stack이 preview로 되돌아가지 않는지 확인한다.
- **작업**:
  - [x] login/onboarding/paywall 확인
  - [x] session setup/focus/stop confirmation 확인
  - [x] generating/result/saving 확인
  - [x] stats/settings/subscription sync 관련 알림 확인
  - [x] saving 완료 후 Android hardware back 또는 native back 동작 확인
- **검증**:
  - [x] QA 메모 또는 스크린샷으로 한글 잔존 없음 확인
  - [x] 저장 완료 후 back 시 preview가 아니라 home으로 이동한다.
  - [x] 발견된 잔존 문구는 Phase 2로 되돌려 수정
- **완료 증거**: 2026-06-20 사용자 E2E 확인 — 앱 전반 사용자 노출 한글 없음. `frontend/mobile/app/saving.tsx`에서 `BackHandler`를 등록해 saving 화면의 hardware back을 `navigateHome()`으로 처리하고, permission/save error alert의 OK도 home으로 이동하도록 변경. `navigateHome()`은 가능한 경우 `dismissAll()` 후 `/`로 replace한다.

## Pre-deploy Check

- [x] 앱스토어 제출 전 주요 화면에서 한국어 copy가 노출되지 않는다.
- [x] 결제/약관/개인정보 문구 의미가 기존 정책과 달라지지 않았다.
- [x] 신규 credential/env/서버 설정이 없다.

## Rollback

- copy-only 변경이므로 해당 PR revert.
- i18n 리소스를 수정한 경우 fallback locale만 이전 commit으로 되돌린다.

## Done Criteria

- [x] 모든 Phase가 `DONE` 또는 `SUPERSEDED`다.
- [x] 모바일 사용자 노출 문구가 영어로 통일됐다.
- [x] 가능한 테스트/검증이 끝났다.
- [x] product `log.md`와 `30-work/README.md`가 갱신됐다.

## Open Issues

- 없음.

## Related

- SPEC: STL-SPEC-001, STL-SPEC-002, STL-SPEC-008, STL-SPEC-009, STL-SPEC-010, STL-SPEC-012
