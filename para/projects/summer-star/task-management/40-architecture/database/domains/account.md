---
type: architecture
id: DOMAIN-001
title: "account — 계정·세션·유형·프로젝트"
status: draft
product: "task-management"
created_at: 2026-09-04
updated_at: 2026-09-07
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
| `auth_session` | refresh 토큰 회전 기록 **+ 회의별 단명 토큰**(`kind ∈ {refresh, meeting}`, 2026-09-07 MF-69) | refresh 는 해시만. **회의 토큰(`kind='meeting'`)은 원문을 `meeting_token` 컬럼에 둔다**(A-13) |
| `work_type` | 동적 유형 | `kind ∈ {meeting, task}` + 이름 + 색 + **설명**(`description`, 2026-09-07 MF-21). 소프트 딜리트 |
| `project` | 프로젝트 | 이름 + 색. 소프트 딜리트 |

## Invariants

- **A-1** `account.login_id` 는 로그인 식별자다. `email` 은 **표시 전용**이고 인증·발송에 쓰지 않는다 — 로그인 폼의 「이메일」 라벨은 정정 대상이다(DEC-001 §3 · §A-9).
- **A-2** 비밀번호는 **8자 이상 + 문자·숫자·특수문자**. 해시만 저장한다(DEC-001 §3).
- **A-3** **프로필의 회사·소속·직무를 `account` 에 두지 않는다.** 「현재」 경력(`ended_on IS NULL`)에서 파생한다(DEC-001 §3 · G-7).
- **A-4** `work_type.is_default = true` 인 **시드 3종**(미팅·회의 = `meeting` / 개인 업무 = `task` / 문서·보고 = `task`)은 **삭제 불가·이름과 종류 고정, `color_token` 과 `description` 만 편집 가능**하다(DEC-001 §4 · MF-21).
- **A-12** **`work_type.description text NULL` — 「어떤 업무인지」**(2026-09-07 · MF-21). 업무 설정에서 유형을 등록할 때 적는다. 쓰는 곳은 회의록 AI 의 `list_work_types()`(이름 · 종류 · 설명) — AI 가 새 업무의 유형을 고르는 근거다(MF-59). 시드 문구: 개인 업무 「혼자 처리하는 실무. 개발·수정·확인 등」 · 문서·보고 「산출물이 문서인 것. 기획서·보고서·회의록 정리」 · **미팅·회의는 빈 값**(DEC-003 OQ-11 — 문구가 정해지지 않았다). 비어 있어도 유형은 유효하다(선택 입력).
- **A-5** `color_token` 은 **디자인 시스템 허용 팔레트의 토큰명**을 담는다. 자유 색상(임의 hex)을 저장하지 않는다(DEC-001 §3).
- **A-6** 유형·프로젝트를 소프트 딜리트해도 **참조 중인 업무·회의는 이름·색을 그대로 보여준다.** 빠지는 곳은 생성·변경의 선택 목록뿐이다(DEC-001 §4).
- **A-7** `auth_session` 의 refresh 는 **1회용**이다. 쓰면 `revoked_at` 을 찍고 새 행을 만든다. 이미 무효인 토큰이 다시 오면 그 계정의 유효 세션을 **전부** 끊는다. **이 규칙은 `kind='refresh'` 행에만 적용된다** — 회의 토큰(A-13)은 회전하지 않는다.
- **A-13** **`auth_session.kind varchar CHECK (refresh | meeting)` — 회의별 단명 토큰이 같은 테이블에 산다**(2026-09-07 · **MF-69** · DEC-003 OQ-9 닫힘). `kind='meeting'` 행은 **회의록 AI 가 MCP 도구로 우리 REST 를 부를 때 쓰는 토큰**이다(DEC-003 §2 · §8). 규칙 넷.
  - **발급** — 회의 `/start` 가 **본인 계정으로** 행 하나를 INSERT 하고 원문 토큰을 codex 실행 옵션의 MCP 헤더에 싣는다. **회의 하나에 하나**이고, **원문은 그 행의 `meeting_token` 컬럼에 둔다**(2026-09-07 저녁 사용자 확정 — refresh 처럼 해시만 두지 않는다. 매 배치 · 최종 제출이 그 원문을 다시 읽어 헤더에 실어야 하는데, 제출마다 새로 발급하는 것은 오버헤드다. 단명 · 회의 범위 · 폐기 = 행 삭제라 노출 위험이 refresh 와 다르다). `refresh_token_hash` 는 이 행에서 NULL 이다. **재시도(`POST /finalize`)도 같은 함수로 새로 발급한다**(2026-09-08 · WORK-012 — ② 종결이 행을 지우므로 재시도 ② 는 새 행이 필요하다. 남은 행이 있으면 지우고 낸다 — 회의당 하나는 어느 시점에도 유지).
  - **검증** — MCP 가 부르는 REST 가 그 행으로 **계정 · 회의 범위**를 본다. 권한 판정은 백엔드가 지고 MCP 는 두 번째 게이트가 아니다(DEC-003 §2).
  - **폐기 = 행 삭제** — 종료 파이프라인 ② 가 끝나면 그 행을 DELETE 한다(best-effort. 실패는 만료로 흡수 — MF-4). **`revoked_at` 을 찍지 않는다** — 회의 토큰은 회전하지 않아 「이미 쓴 토큰」을 탐지할 대상이 아니다(A-7 은 `refresh` 행의 규칙이다).
  - **왜 무상태 JWT 가 아닌가** — access 는 무상태 JWT(1시간)라 **폐기 표면이 없다.** MF-4 의 「마감 시 best-effort 폐기」가 성립하려면 지울 행이 있어야 한다. 그래서 이미 있는 `auth_session` 에 종류를 하나 더한다 — 새 테이블을 만들지 않는다.
- **A-8** 로그인 실패 횟수를 세지 않는다 — 잠김 정책이 없다(DEC-001 §4 「정책 없음(논외)」).
- **A-9** 감사 로그 테이블을 두지 않는다(DEC-001 §6). 「마지막 저장」 캡션은 `updated_at` 으로 그린다.
- **A-10** **v2 항목의 컬럼을 만들지 않는다** — 소셜 로그인·목소리 샘플·연동 관리·계정 삭제·「다른 기기 모두 로그아웃」은 프론트만 그린다(DEC-001 §v2).
- **A-11** **「업무 시간(시작–종료)」 필드를 두지 않는다**(2026-09-05 확정). 디자인 프로필 패널에 셀렉터가 있으나 v1 에서 쓰는 곳이 없다 — 캘린더 시간 그리드는 08–20 고정이다. **디자인 정정 대상**(§A-14, DEC-001 §3).

## Related Specs / Works

- SPEC-00x 인증·설정 (DEC-001 Resulting Spec)
- 소비처: `domains/task.md` · `domains/meeting.md` · `domains/calendar.md`
