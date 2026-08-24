---
type: decision
id: AXKG-DEC-006
title: "역할(admin/staff) 권한 모델과 접근 경계"
status: accepted
product: ax-knowledge-graph
created_at: 2026-07-10
updated_at: 2026-07-14
tags:
  - product/ax-knowledge-graph
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-001-ax-knowledge-graph-from-curated-sources|AXKG-BL-001]]"
  decisions:
    - "[[decision-001-para-pipeline-and-approval-gates|AXKG-DEC-001]]"
    - "[[decision-004-mvp-defaults-and-scope|AXKG-DEC-004]]"
  specs:
    - "[[spec-003-source-inbox|AXKG-SPEC-003]]"
    - "[[spec-006-graph-chat|AXKG-SPEC-006]]"
    - "[[spec-008-simple-token-auth|AXKG-SPEC-008]]"
    - "[[spec-013-document-library|AXKG-SPEC-013]]"
  works:
    - "[[work-009-chat-push-to-inbox|AXKG-WORK-009]]"
  releases: []
  related: []
up:
  - role-based-entity
  - jwt
---

# 역할(admin/staff) 권한 모델과 접근 경계

MVP는 단일 seed 계정으로 로그인 여부만 가드했다(AXKG-DEC-004: auth token은 `localStorage`, role/permission은 범위 밖). 제품이 prod에서 role 개념 없이 라이브 중이라, 다중 사용자 운영을 위해 role·유저 관리·접근 경계를 확정한다. 이 결정은 정책 확정이며 구현(라우트/마이그레이션/화면)은 후속 BE/FE work가 담당한다.

## Decision

사용자 승인 2026-07-10. 아래 항목만 확정 — 추가 정책(이메일 인증, 비밀번호 복잡도 규칙, 세션 정책 변경 등)은 발명하지 않는다.

1. **role 2값 `admin`/`staff`** — 그 이상 세분화하지 않는다. `users`에 `role`과 `is_active`를 둔다. `is_active=false`는 로그인 차단이며 admin이 토글한다.
2. **접근 경계** (계약 매트릭스 SSOT는 AXKG-SPEC-008이 소유한다):
   - `staff` = `/graph`(그래프 시각화 + 채팅④) + 본인 계정(me / 비밀번호 변경) + 문서 라이브러리(`/documents`, 읽기 전용 열람 — **2026-07-11 추가**, 매트릭스 세부는 AXKG-SPEC-008 §4·페이지 계약은 AXKG-SPEC-013).
   - `admin` = 전부 (소스 inbox/수집, 분류②·문서화③ 승인 게이트, 설정, 유저 관리).
   - 승인 게이트의 승인 권한은 admin만 가진다. staff는 게이트 API·화면 표면 자체에 접근할 수 없다.
   - FE 내비/가드 + BE 라우트 authz 양쪽에서 이중으로 강제한다.
3. **유저 생성 = admin 전용** (공개 가입 없음). 생성 시 기본 비밀번호는 `1234`다.
4. **비밀번호 변경 = 본인 자율**. **최초 로그인 강제 변경은 채택하지 않는다** — 사용자 명시 선택(2026-07-10 박제).
5. **역할 변경 = admin 전용**.
6. **시드 정책**: 활성 22명 로스터(admin 3: 이건학·전창원·김수연 + staff 19)로 시드한다. email 기준 멱등이며, 기존 seed 계정(`kknaks@medisolveai.com`)은 admin으로 로스터에 흡수된다. 레퍼런스(mediness 유저)의 `department`/`position`/`source_user_id` 등은 저장하지 않는다 — role 매핑 소스일 뿐이다. 로스터 전문은 AXKG-SPEC-008이 수록한다.

## Rationale

- prod에 seed 계정 `1234`가 role 개념 없이 노출된 채 라이브 중이라, 승인 게이트/설정/수집 같은 운영 권한과 열람 권한을 분리해야 한다.
- staff 다수는 완성된 지식을 그래프로 열람·질의하는 소비자이고, 큐레이션(수집·분류·문서화 승인)·설정·유저 관리는 소수 운영자(admin)의 일이므로 2값 role로 충분하다. 더 세분화하면 MVP 대비 비용만 커진다.
- 강제 비밀번호 변경은 초기 소규모 신뢰 사용자 집단에서 UX 마찰만 키우므로 채택하지 않는다. 대신 본인 자율 변경을 제공한다.
- 접근 경계 매트릭스는 한 곳(SPEC-008)에만 두고, 게이트/설정 스펙은 참조만 한다 — 같은 사실을 여러 스펙에 복사하지 않는다.

## 개정: 채팅→인박스 push 단일 쓰기 액션 = 전 유저 허용 (2026-07-14 개정, PLAN-013-T-002)

채팅 고도화 라운드(PLAN-013 ② 채팅 활용방안)에서 접근 경계에 **비대칭 쓰기 액션 하나**를 추가한다. 위 Decision 2(접근 경계)를 아래로 보강한다 — role 2값·이중 강제·게이트 admin 전용 등 나머지 경계는 불변이다. 기존 경계의 refinement이므로 신규 DEC로 쪼개지 않고 in-place 개정한다(DEC-005 amendment 선례 준수).

- **채팅→Source Inbox push = 전 유저(staff 포함) 허용, 단일 쓰기 액션**: 채팅④에서 AI가 제시한 방안을 사용자가 Source Inbox로 push하는 동작(AXKG-SPEC-006 `Source Inbox에 추가` CTA의 실체화)은 staff도 수행할 수 있다. push는 `source_channel=chat` source 1건을 `received`로 생성하는 **쓰기 단일 액션**이며, 사용자 명시 CTA를 통해서만 일어난다(자동 push 없음). push되는 payload는 방안만이 아니라 **push 시점까지의 대화 내용 전부(방안 포함)**다 — 경계 결정은 무관하며 payload 계약 SSOT는 AXKG-SPEC-006/003이다(2026-07-14 PLAN-013-T-003).
- **인박스 표면(목록·조회·관리·삭제/무시)은 admin 전용 유지**: staff는 자신이 push한 것을 포함해 Source Inbox 화면/목록/관리 표면에 접근할 수 없다(현행 그대로). 즉 staff는 인박스에 **쓰기(push)만** 가능하고 **읽기·관리 표면은 없다**(비대칭 권한).
- **분류 승인은 admin 유지**: push된 chat source도 기존 요약→분류→문서화 게이트를 그대로 타며, 게이트 승인 권한은 admin만 갖는다(AXKG-SPEC-001/002 무변경).
- 채팅 접근 자체(staff·admin 모두 `/graph`)는 무변경.

**근거**: staff가 그래프를 탐색하다 떠오른 방안을 잃지 않고 큐레이션 큐로 흘려보내려면 push 쓰기는 열어야 하지만, 인박스 운영(무엇을 채택/폐기)은 여전히 admin의 일이므로 읽기·관리는 닫는다. 자동 침투 없이 사용자 명시 CTA 기반 push만 허용한다.

**정합 대상**: AXKG-SPEC-008 §4 접근 경계 매트릭스(이 액션 행 추가 — 경계 SSOT), AXKG-SPEC-006(방안 제시→push flow·push API 계약), AXKG-SPEC-003(`source_channel=chat` intake 데이터 계약). 인박스 열람 권한 확대·staff 본인 제출분 열람·자동 push·프로젝트 전용 별도 인박스 신설은 하지 않는다.

## 근거 개념

이 결정이 기대는 개념. 상세는 concept 노트가 갖는다.

- [[role-based-entity]] — `admin`/`staff` 두 값을 **별도 테이블이 아니라 `users.role` 로** 두고 권한을 가른 선택. 역할이 늘면 어떻게 되는지의 경계도 여기 있다
- [[jwt]] — 토큰 로그인 위에 역할을 얹는 구조. 토큰이 신원을 나르고 **권한 판정은 서버 라우트가** 한다는 이중 강제가 이 결정의 2항이다

## Open Questions

- admin의 타 유저 비밀번호 리셋(`1234` 재초기화) 제공 여부 — 미논의. AXKG-SPEC-008 §7 Open Questions로 추적한다.
