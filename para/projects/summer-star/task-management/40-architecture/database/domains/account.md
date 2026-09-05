---
type: architecture
id: DOMAIN-001
title: "account — 계정·세션·유형·프로젝트"
status: draft
product: "task-management"
created_at: 2026-09-04
updated_at: 2026-09-04
tags:
  - product/task-management
  - doc/architecture
  - architecture/database
links:
  baselines: [BASE-001]
  decisions: [DEC-001]
  specs: []
  works: []
  related: []
---

# account

계정 하나와, 그 계정이 다른 모든 영역에 **공급**하는 것 — 세션·경력·유형·프로젝트. 이 도메인은 소비하지 않고 공급만 한다(DEC-001 §8).

## Purpose

DEC-001 이 정한 인증·설정을 담는다. 여기서 만든 `work_type`·`project` 를 업무·회의·캘린더가 참조한다.

## Entities / Tables

| Entity/Table | Purpose | Notes |
|---|---|---|
| `account` | 계정·프로필 | **앱에서 못 만든다 — 시드로만**(DEC-001 §2). `login_id` 는 이메일 형식이 아니다(§A-9 정정) |
| `career` | 경력 행 | **하드 삭제**(DEC-001 §5). `ended_on IS NULL` = 재직 중 |
| `auth_session` | refresh 토큰 회전 기록 | 해시만 저장. 원문은 서버에 남기지 않는다 |
| `work_type` | 동적 유형 | `kind ∈ {meeting, task}` + 이름 + 색. 소프트 딜리트 |
| `project` | 프로젝트 | 이름 + 색. 소프트 딜리트 |

## Invariants

- **A-1** `account.login_id` 는 로그인 식별자다. `email` 은 **표시 전용**이고 인증·발송에 쓰지 않는다 — 로그인 폼의 「이메일」 라벨은 정정 대상이다(DEC-001 §3 · §A-9).
- **A-2** 비밀번호는 **8자 이상 + 문자·숫자·특수문자**. 해시만 저장한다(DEC-001 §3).
- **A-3** **프로필의 회사·소속·직무를 `account` 에 두지 않는다.** 「현재」 경력(`ended_on IS NULL`)에서 파생한다(DEC-001 §3 · G-7).
- **A-4** `work_type.is_default = true` 인 **시드 3종**(미팅·회의 = `meeting` / 개인 업무 = `task` / 문서·보고 = `task`)은 **삭제 불가·이름과 종류 고정, `color_token` 만 편집 가능**하다(DEC-001 §4).
- **A-5** `color_token` 은 **디자인 시스템 허용 팔레트의 토큰명**을 담는다. 자유 색상(임의 hex)을 저장하지 않는다(DEC-001 §3).
- **A-6** 유형·프로젝트를 소프트 딜리트해도 **참조 중인 업무·회의는 이름·색을 그대로 보여준다.** 빠지는 곳은 생성·변경의 선택 목록뿐이다(DEC-001 §4).
- **A-7** `auth_session` 의 refresh 는 **1회용**이다. 쓰면 `revoked_at` 을 찍고 새 행을 만든다. 이미 무효인 토큰이 다시 오면 그 계정의 유효 세션을 **전부** 끊는다.
- **A-8** 로그인 실패 횟수를 세지 않는다 — 잠김 정책이 없다(DEC-001 §4 「정책 없음(논외)」).
- **A-9** 감사 로그 테이블을 두지 않는다(DEC-001 §6). 「마지막 저장」 캡션은 `updated_at` 으로 그린다.
- **A-10** **v2 항목의 컬럼을 만들지 않는다** — 소셜 로그인·목소리 샘플·연동 관리·계정 삭제·「다른 기기 모두 로그아웃」은 프론트만 그린다(DEC-001 §v2).
- **A-11** **「업무 시간(시작–종료)」 필드를 두지 않는다**(2026-09-05 확정). 디자인 프로필 패널에 셀렉터가 있으나 v1 에서 쓰는 곳이 없다 — 캘린더 시간 그리드는 08–20 고정이다. **디자인 정정 대상**(§A-14, DEC-001 §3).

## Related Specs / Works

- SPEC-00x 인증·설정 (DEC-001 Resulting Spec)
- 소비처: `domains/task.md` · `domains/meeting.md` · `domains/calendar.md`
