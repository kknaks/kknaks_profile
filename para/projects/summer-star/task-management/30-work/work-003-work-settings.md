---
type: work
id: WORK-003
title: "업무 설정 — 유형·프로젝트 CRUD · 팔레트 8종 · 인라인 편집"
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
  specs: [SPEC-002]
  works: [WORK-001, WORK-002]
  releases: []
  related: []
---

# 업무 설정 — 유형·프로젝트 CRUD · 팔레트 8종 · 인라인 편집

**업무를 만들려면 유형이 먼저 있어야 한다.** 유형(종류 + 이름 + 색)과 프로젝트(이름 + 색)를 만들고 고치고 지운다. 기본 유형 3종은 색만 바뀐다. 업무·회의 화면은 만들지 않는다 — 이 work 는 **그들이 참조할 원천**을 세운다.

> 1 파일 = 1 work = **빌드 계획**. dev가 이 문서만 보고 PR 분리 / 일정 / 작업 시작이 가능해야 한다.
> SPEC의 외부 계약 본문은 복제하지 않고 frontmatter `links.specs`와 index에서 연결한다.

## Meta

- Baseline: BASE-001
- Covers spec: **SPEC-002**(업무 설정 — 유형 · 프로젝트)
- Depends on work: **WORK-001**(`work_type`·`project` 테이블 · 기본 3종 시드 · 토큰 CSS 자리) · **WORK-002**(세션 가드 · 설정 레이아웃 · `ConfirmModal`)
- Parallel work: 없음
- Follow-up work: 내 업무 그룹(유형·프로젝트를 소비한다) · 회의록 그룹(종류=미팅 유형) · 캘린더 그룹(유형 색·필터)
- **External dependency**: **코드 레포는 별도다** — `github.com/kknaks/task_management`. 이 워크트리에 코드를 만들지 않는다. 그 밖의 외부 의존은 없다

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner |  |
| Status | todo |
| Progress | 0% |
| Branch/PR |  |
| Blocker | WORK-002 미완 |
| Next | Phase 1 — 유형·프로젝트 API |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | 범위 확정 · SPEC-002 대조 | todo |
| Design |  | 팔레트 8종 적용 · 인라인 행/팝오버/삭제 모달 규격 확인 | todo |
| FE |  | 팔레트 CSS 변수 · 배지·dot 공용 컴포넌트 · 설정 화면 · 자동 저장 실패 표시 | todo |
| BE |  | 유형·프로젝트 CRUD · 잠금·중복·팔레트 검증 · 소프트 딜리트 | todo |
| QA |  | Phase 검증(앱 창 E2E) | todo |
| Ops |  | 해당 없음(신규 env 없음) | todo |

## Scope

포함:

- 유형 CRUD — 생성(**종류 + 이름 + 색**) · 이름/색 수정 · **소프트 딜리트**
- 프로젝트 CRUD — 생성(이름 + 색) · 이름/색 수정 · 소프트 딜리트
- 기본 유형 3종 잠금(이름·종류 고정, **색만 편집**, 삭제 불가)
- **허용 팔레트 8종** — CSS 변수 등록 + `data-color-token` 렌더 규약 + 배지/dot 공용 컴포넌트
- 업무 설정 화면 — 패널 2개 · **인라인 추가 행(종류 셀렉터·색 팝오버)** · 인라인 편집 자동 저장 · 삭제 확인 모달 · 빈 상태 · 반응형
- **자동 저장 실패 표시 공통 컴포넌트**(SPEC-002 U-7 — 전 영역이 재사용한다)

제외:

- 개인 설정(프로필·경력·목소리)·연동 관리 → 개인 설정 그룹(SPEC-010)
- 유형·프로젝트를 **고르는 쪽**(업무 생성 드로어·필터·배지 표시) → 각 소비 그룹
- 집계 카운트(「이번 달 8건」) → v1 에 넣지 않는다(SPEC-002 S002-OQ-3)
- 삭제 복원 UI → **v1 에 없다**

## Code Surface

- Repo / module: `github.com/kknaks/task_management` — `app/back`(BE) · `app/front`(FE)
- 만질 파일 후보

| 경로 후보 | 설명 |
|---|---|
| `app/back/api/setting_router.py` | `/api/work-types` · `/api/projects` — 라우터 단위 `require_account` |
| `app/back/service/work_type_service.py` | 기본 3종 잠금 · 이름 유일성 · 팔레트 검증 · 소프트 딜리트 |
| `app/back/service/project_service.py` | 이름 유일성 · 팔레트 검증 · 소프트 딜리트 |
| `app/back/repository/work_type_repository.py` · `project_repository.py` | 기본 조회는 **`deleted_at IS NULL`**. 삭제분 조회 메서드는 이름에 그 사실을 드러낸다 |
| `app/back/schemas/setting.py` · `dto/setting.py` | FE 계약(camelCase) / 내부 dto. **입력도 dto** 로 넘긴다 |
| `app/back/core/constants.py`(신규) | **허용 팔레트 토큰명 8종** — 서버 검증의 단일 출처 |
| `app/back/tests/test_work_type.py` · `test_project.py` | 잠금 · 중복 · 팔레트 밖 값 · 삭제 후 목록 제외 · 참조 표시 유지 |
| `app/front/src/styles/tokens.css` | **팔레트 8종** `--tm-palette-<name>-bg` / `-fg` 쌍 등록 |
| `app/front/src/components/shared/TypeBadge.tsx` · `ColorDot.tsx` | `data-color-token` 으로 색을 고른다. **인라인 hex 금지**(FE §5-3) |
| `app/front/src/components/shared/ColorPickerPopover.tsx` | 24px 스와치 4×2 · 선택 즉시 저장 |
| `app/front/src/components/shared/InlineAddRow.tsx` · `InlineEditText.tsx` | 56px 추가 행 · blur 자동 저장. **실패 상태 prop 공통** |
| `app/front/src/components/shared/AutoSaveError.tsx`(또는 위 두 컴포넌트의 공통 prop) | 「저장되지 않았습니다 · 다시 저장」 규격 |
| `app/front/src/features/settings/api.ts` · `hooks/useWorkTypes.ts` · `useProjects.ts` | 호출·쿼리·무효화 |
| `app/front/src/features/settings/components/WorkSettingsScreen.tsx` 외 | 패널 2개 · 목록 행 · 추가 행 · 삭제 모달 연결 |
| `app/front/src/app/(app)/settings/work/page.tsx` | 라우트 껍데기(`'use client'`, 화면 컴포넌트 하나를 렌더) |
| `app/front/src/lib/api/queryKeys.ts` | `['workTypes']` · `['projects']` 키 등록 |

- Domain / schema note: **마이그레이션 없음.** WORK-001 이 만든 `work_type`·`project` 를 쓴다. 팔레트 값은 **컬럼이 아니라 토큰명**이라 스키마 변경이 없다

## Domain / Schema

| Entity | 역할 |
|---|---|
| `work_type` | 동적 유형 — 종류(`meeting`\|`task`) · 이름 · 색 토큰 · 기본 여부 · `deleted_at` |
| `project` | 프로젝트 — 이름 · 색 토큰 · `deleted_at` |

- 상태 / invariant: `domains/account.md` **A-4**(기본 3종 잠금) · **A-5**(색은 팔레트 토큰명, 자유 hex 금지) · **A-6**(삭제해도 참조 중인 기록에는 이름·색이 그대로) · `database/README.md` **§0-1**(소프트 딜리트 · 복원 없음)
- Migration 필요 여부: **없음**
- SPEC 에 환류해야 하는 변경: 없음. 다만 **`duplicate_name`·`invalid_color_token`·`not_found` 코드**가 아키텍처 §8-2 표에 없다(SPEC-002 S002-OQ-2) — 구현은 SPEC-002 §4 Case Matrix 를 따르고 표 갱신은 코디 소관

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| 내 업무 그룹 | `GET /api/work-types`·`/api/projects` · `TypeBadge`/`ColorDot` · 팔레트 변수 | 업무는 유형이 **필수**다 — 이 work 없이는 업무를 만들 수 없다 |
| 회의록 그룹 | 같은 목록 중 **종류=미팅**만 | 회의 유형 셀렉터가 이 목록을 거른다 |
| 캘린더 그룹 | 유형 색·필터 | 유형 분포 카드가 이 목록과 색을 쓴다 |
| 전 영역 | **자동 저장 실패 표시 컴포넌트** | SPEC-002 U-7 이 전 영역 공통 규격이다 — 여기서 처음 만든다 |

## Internal Interface Contract

외부 계약(엔드포인트·검증·에러)은 **SPEC-002 §4** 가 정본이다. 후속 work 가 의존하는 내부 접점만 고정한다.

| 접점 | 계약 |
|---|---|
| **팔레트 토큰명 8종** | `indigo` · `violet` · `steel` · `mint` · `sky` · `amber` · `rose` · `graphite`(값은 SPEC-002 §4 Data Contract). **서버는 `core/constants.py` 한 곳**, **프론트는 `tokens.css` 한 곳**에서만 정의한다 |
| 색 렌더 | 컴포넌트는 `data-color-token="<name>"` 을 받고 CSS 가 변수 쌍을 고른다. **인라인 `style` 로 hex 를 넣지 않는다**(FE §5-3). 팔레트에 없는 토큰명이 오면 **중립 색으로 떨어뜨리고 항목을 숨기지 않는다** |
| 목록 응답 | `{ items: [...] }` 로 감싼다. `items` 를 꺼내는 것은 `features/settings/api.ts` 까지이고 훅 위로는 배열이 올라간다(FE §3-6) |
| 캐시 키·무효화 | `['workTypes']`·`['projects']`. 유형·프로젝트가 바뀌면 **`['tasks']`·`['meetings']` 도 무효화**한다(배지 이름·색이 딸려 있다 — FE §3-3). 이 work 시점에는 후자 키가 없으므로 **키 등록만 해 두고 소비 그룹에서 연결**한다 |
| 자동 저장 실패 표시 | `InlineEditText`·`Selector` 계열이 **실패 상태 prop 을 공통으로** 갖는다. 해제 조건은 「다시 저장 성공」 또는 「그 필드 재편집 후 저장 성공」 **둘뿐**이고 시간 경과로 사라지지 않는다 |
| 기본 유형 잠금 | 화면이 컨트롤을 감춰도 **서버 판정이 정본**이다(`work_type_locked`). 두 겹으로 막는다 |

## Execution

### Phase 1 — 유형·프로젝트 API (백엔드)

- **Status**: TODO
- **설명**: 화면 없이 **CRUD 와 규칙이 도는 상태**를 만든다. 잠금·중복·팔레트·소프트 딜리트가 서버에서 판정되는지를 이 Phase 에서 못박는다.
- **작업**:
  - [ ] `core/constants.py` — **허용 팔레트 토큰명 8종**(서버 검증 단일 출처)
  - [ ] `repository/work_type_repository.py` · `project_repository.py` — 기본 조회 `deleted_at IS NULL`, dto 반환
  - [ ] `service/work_type_service.py` — **기본 3종 잠금**(이름·종류 변경·삭제 거부) · **이름 유일성**(계정 안, 삭제분 제외, 공백·대소문자 정규화) · 팔레트 검증 · 소프트 딜리트 · **종류는 생성 시에만**
  - [ ] `service/project_service.py` — 이름 유일성 · 팔레트 검증 · 소프트 딜리트
  - [ ] `api/setting_router.py` — 목록·생성·부분 수정·삭제 8표면. 라우터 단위 인가
  - [ ] `schemas/setting.py`·`dto/setting.py` — PATCH 는 `T | Unset` 로 「보내지 않음」과 「지움」을 구분
  - [ ] 테스트 — 잠금 · 중복 · 팔레트 밖 값 · **삭제한 유형이 목록에서 빠지고 참조에는 이름·색이 남는다**(A-6) · 남의 것 404
- **검증**:
  - [ ] `curl` 로 유형을 만들고(`kind`+`name`+`colorToken`) 목록에 나온다
  - [ ] 기본 유형의 **이름·종류 변경과 삭제가 409 `work_type_locked`** 로 거부되고, **색 변경은 된다**
  - [ ] 같은 이름으로 또 만들면 **409 `duplicate_name`**
  - [ ] 팔레트 밖 토큰명은 **422 `invalid_color_token`**
  - [ ] 커스텀 유형을 삭제하면 목록에서 빠지고, **DB 에는 행이 남아 있다**(소프트 딜리트)
  - [ ] 생성 후 `kind` 를 PATCH 로 바꾸려 하면 **거부**된다
  - [ ] `pytest` 통과
- **완료 증거**: 미작성

### Phase 2 — 팔레트 토큰 · 배지/dot 공용 컴포넌트

- **Status**: TODO
- **설명**: 색을 **한 곳에서만** 정의한다. 이후 업무·회의·캘린더가 전부 이 컴포넌트로 색을 그리므로, 화면보다 먼저 세운다.
- **작업**:
  - [ ] `styles/tokens.css` — 8종 `--tm-palette-<name>-bg` / `-fg` 쌍 등록(값은 SPEC-002 §4)
  - [ ] `components/shared/TypeBadge.tsx` — h20 · r4 · 11/600, `data-color-token` 으로 색 선택
  - [ ] `components/shared/ColorDot.tsx` — 8px dot(프로젝트용)
  - [ ] `components/shared/ColorPickerPopover.tsx` — 240 폭 · 24px 스와치 4×2 · 현재 값 `#7181F8` 테두리 + 3px 글로우 · **선택 즉시 반영, 확인 버튼 없음** · **자유 색 입력 없음**
  - [ ] ESLint 규칙(또는 리뷰 체크) — **인라인 `style` 로 색 hex 지정 금지**(FE §금지 목록 4)
- **검증**:
  - [ ] 스토리 화면(또는 임시 페이지)에서 8종 배지·dot 가 **디자인 값 그대로** 보인다
  - [ ] 팔레트에 없는 토큰명을 주면 **중립 색으로 그려지고 항목이 사라지지 않는다**
  - [ ] 코드 검색 결과 **컴포넌트에 hex 리터럴이 없다**(완료 증거에 grep 결과 첨부)
  - [ ] 색 팝오버에서 고르면 **확인 버튼 없이** 값이 바뀐다
- **완료 증거**: 미작성

### Phase 3 — 업무 설정 화면 · 자동 저장 · 삭제 모달

- **Status**: TODO
- **설명**: 사용자가 **앱 창에서 유형과 프로젝트를 직접 만드는** 단계. 자동 저장 실패 표시가 여기서 처음 만들어져 이후 전 영역이 재사용한다.
- **작업**:
  - [ ] `features/settings` — 호출·훅(`['workTypes']`·`['projects']`)·무효화
  - [ ] 「업무 유형」 패널 — 헤더(캡션 「입력을 마치면 자동으로 저장됩니다」 · 「유형 추가」) + 목록 행 64px(배지 · 이름 · 종류 칩 · 색 트리거 · 삭제)
  - [ ] **인라인 추가 행 56px** — **종류 셀렉터(미팅/업무)** + 이름 + 색 트리거 + 취소/추가. `Enter` 와 버튼 **둘 다**
  - [ ] 기본 유형 3종 — 「기본」 칩 · 이름/종류 읽기 전용 · 삭제 버튼 없음 · **색만 활성**
  - [ ] 「프로젝트」 패널 — 같은 구조(종류 없음) + **빈 상태**(「아직 프로젝트가 없습니다」)
  - [ ] 인라인 편집 blur 자동 저장 · **자동 저장 실패 표시**(토스트 + 필드 실패 테두리 + 「다시 저장」, **자동 재시도 없음**)
  - [ ] 삭제 → `ConfirmModal`(WORK-002 산출물) 재사용, 문구·경고는 SPEC-002 U-6
  - [ ] 반응형 — 1280~1439 메뉴 카드 240 / ≥1440 260, **이름 열만 줄어든다**
- **검증**:
  - [ ] 설정 → 「업무 설정」에 **기본 3종이 「기본」 칩과 함께** 보인다
  - [ ] 「유형 추가」로 **종류·이름·색**을 넣어 유형을 만들고 배지가 고른 색으로 보인다. **종류를 고르기 전에는 「추가」가 비활성**이다
  - [ ] 이미 있는 이름으로 추가하면 인라인 안내가 뜨고 **입력이 사라지지 않는다**
  - [ ] 기본 유형은 **이름이 편집되지 않고 삭제 버튼이 없으며**, 색만 바뀐다
  - [ ] 이름을 고치고 바깥을 클릭하면 **저장 버튼 없이** 저장된다
  - [ ] 삭제하면 **확인 모달(600)** 을 지나 목록에서 사라진다
  - [ ] 프로젝트가 없으면 **빈 상태**가 보이고, 하나 만들면 사라진다
  - [ ] **서버를 내린 채** 이름을 고치면 **토스트 + 그 필드 「저장되지 않았습니다 · 다시 저장」** 이 뜨고 **가만히 두어도 재시도가 나가지 않는다**(네트워크 탭 확인). 서버를 올리고 「다시 저장」을 누르면 저장된다
  - [ ] 창을 1439 이하로 줄여도 행이 **두 줄로 접히지 않는다**
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] 신규 env 가 없다(이 work 는 설정 값을 추가하지 않는다)
- [ ] 목록 응답에 **다른 계정의 유형·프로젝트가 섞이지 않는다**(소유 검사)
- [ ] 삭제가 **소프트**이고 하드 삭제 경로가 없다(복원 화면이 없으므로 실수로 지운 데이터가 DB 에는 남는다)

## Rollback

- **스키마 변경이 없다** — 되돌릴 마이그레이션이 없다. 잘못 만든 행은 소프트 딜리트로 목록에서 빠진다
- **백엔드**: `setting_router` 미등록으로 표면을 걷어낼 수 있다. 그 순간 프론트 화면은 조회 실패 표시가 된다(빈 목록이 아니다)
- **프론트**: 브랜치 폐기. `tokens.css` 의 팔레트 변수는 다른 화면이 아직 쓰지 않으므로 함께 되돌려도 영향이 없다 — **단, 소비 그룹이 시작된 뒤에는 되돌리지 않는다**(배지 색이 전부 중립으로 떨어진다)

## Done Criteria

- [ ] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다.
- [ ] **SPEC-002 §6 Acceptance 14개 항목이 전부 확인**됐다.
- [ ] 팔레트 8종이 **서버 상수와 CSS 변수 두 곳에만** 정의돼 있다(중복 정의 없음).
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다.

## Open Issues

- **에러 코드 3종이 아키텍처 §8-2 표에 없다**(`duplicate_name` · `invalid_color_token` · `not_found` — SPEC-002 S002-OQ-2). 구현은 SPEC-002 §4 를 따르고 표 갱신은 코디 소관
- **이름 중복 금지는 spec 이 새로 정한 규칙이다**(SPEC-002 S002-OQ-1). DEC-001 에 유일성 규정이 없다 — 정책서 반영 필요
- **커스텀 유형의 종류 변경 불가도 spec 판단이다**(SPEC-002 S002-OQ-4). DEC-001 은 기본 3종의 고정만 말한다
- **팔레트 5종의 hex 가 디자인 원본에 없다**(SPEC-002 S002-OQ-5). 디자인 시스템에 등록되면 `tokens.css` 와 `core/constants.py` 를 함께 고친다 — **값이 바뀌어도 토큰명이 그대로면 코드 변경이 두 파일로 끝난다**
- **집계 카운트를 넣지 않았다**(SPEC-002 S002-OQ-3). 참고 시안의 「이번 달 8건」은 v1 범위 밖이다
- **`['tasks']`·`['meetings']` 무효화 연결은 소비 그룹에서** 한다 — 이 work 시점에는 그 키가 없다

## Related

- SPEC: SPEC-002 (frontmatter `links.specs`)
- Work: WORK-001 · WORK-002 (선행)
