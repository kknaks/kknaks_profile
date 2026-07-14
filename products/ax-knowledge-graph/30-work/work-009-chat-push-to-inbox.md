---
type: work
id: AXKG-WORK-009
title: "WP8: 채팅→인박스 push (생각→방안→push)"
status: todo
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
progress: 0
created_at: 2026-07-14
updated_at: 2026-07-14
tags:
  - product/ax-knowledge-graph
  - doc/work
  - status/todo
links:
  baselines:
    - "[[baseline-001-ax-knowledge-graph-from-curated-sources|AXKG-BL-001]]"
  decisions:
    - "[[decision-006-role-authz-and-access-boundary|AXKG-DEC-006]]"
  specs:
    - "[[spec-006-graph-chat|AXKG-SPEC-006]]"
    - "[[spec-003-source-inbox|AXKG-SPEC-003]]"
    - "[[spec-008-simple-token-auth|AXKG-SPEC-008]]"
  works:
    - "[[work-002-source-intake|AXKG-WORK-002]]"
    - "[[work-005-graph-chat|AXKG-WORK-005]]"
    - "[[work-007-auth-roles-and-user-management|AXKG-WORK-007]]"
  releases: []
  related: []
---

# WP8: 채팅→인박스 push (생각→방안→push)

채팅④에서 AI가 제시한 방안을 사용자가 `Source Inbox에 추가`로 push해, push 시점까지의 대화 내용 전부(방안 포함)를 `source_channel=chat` source로 흘려보낸다. push는 채팅 접근이 되는 모든 유저(staff·admin)가 쓸 수 있는 **단일 쓰기 액션**이고, 인박스 목록·조회·관리 표면은 admin 전용으로 유지한다(비대칭 권한). 생성된 source는 기존 요약→분류 파이프라인에 그대로 합류한다. BE + FE.

## Meta

- Baseline: AXKG-BL-001
- Covers spec: AXKG-SPEC-006(방안 제시→push flow S-4·`POST /graph/chats/{chat_id}/push-to-inbox` 계약·U-2 push CTA), AXKG-SPEC-003(`source_channel=chat` intake 데이터 계약·S-4 lifecycle), AXKG-SPEC-008(접근 경계 매트릭스 push 행)
- Covers decision: AXKG-DEC-006(2026-07-14 개정 — 채팅→인박스 push 단일 쓰기 액션 전 유저 허용, 인박스 표면 admin 전용 유지)
- Depends on work: AXKG-WORK-005(WP4 — chat④), AXKG-WORK-002(WP1 — Source Inbox·요약 파이프라인), AXKG-WORK-007(WP6 — role/authz)
- Parallel work: AXKG-WORK-008(WP7), AXKG-WORK-010(WP9)
- Follow-up work: 없음
- External dependency: 없음

## Scope

포함:

- BE `POST /graph/chats/{chat_id}/push-to-inbox` — 권한 staff·admin(비대칭 쓰기), 대화 전체 직렬화
- `source_channel=chat` source 생성(`source_url=null`·`slack_message_ts=null`·`raw_text` 필수) + push provenance(chat/run)
- received→요약①→분류 파이프라인 합류(User Note Fallback 경로 재사용)
- FE 방안 push CTA(`Source Inbox에 추가`)와 push 상태 표면(push 중·완료·실패). 인박스 목록/관리 표면은 이 화면에 미노출

제외:

- Source Inbox 목록·조회·관리 표면 (admin 전용, AXKG-SPEC-003 소관·경계 변경 없음)
- 분류/문서화 게이트 자체 (AXKG-SPEC-001/002/004 무변경, 승인 권한 admin)
- retriever·방안 생성 품질 (AXKG-WORK-008·chat 실행 소관)

## Progress Checklist

코드 발주 단위(C-item). 계약·스펙 참조 수준까지만 — 대화 직렬화 형식·조립 위치·endpoint 최종 형태는 AXKG-SPEC-006 §7 OQ대로 구현 확정한다.

- [x] **C-1 push endpoint** — `POST /graph/chats/{chat_id}/push-to-inbox`, 권한 staff·admin(비대칭 쓰기 — 인박스 읽기·관리 표면 접근 미부여). 접근 경계 매트릭스 SSOT는 AXKG-SPEC-008. (AXKG-SPEC-006 §4, AXKG-DEC-006) — PLAN-013-T-008(graph 라우터 `get_current_auth` = staff·admin, owner 스코프).
- [x] **C-2 대화 직렬화** — push 시점까지의 채팅 대화 내용 전부(user·assistant 메시지 이력, 제시된 방안 포함)를 `raw_text`로. 직렬화 형식(role 구분 표기 등)·조립 위치(클라이언트 vs 서버 `chat_id` 조립)는 AXKG-SPEC-006 §7 OQ대로 구현 확정, `EMPTY_PUSH_TEXT` 검증. (AXKG-SPEC-006 §4 Request) — **확정: 서버 조립** + `## {Role}` heading 직렬화, `run_id` 컷오프.
- [x] **C-3 chat source 생성** — `source_channel=chat`·`source_url=null`·`slack_message_ts=null`·`raw_text`(필수, trim 후 non-empty)로 `received` 생성, push한 chat/run을 provenance로 기록. (AXKG-SPEC-003 §5·S-4) — PLAN-013-T-008(`create_chat_push`, `metadata.chat_push`).
- [x] **C-4 파이프라인 합류** — `received`→자동 요약①(URL 없음 → `raw_text`가 곧 요약 입력, AXKG-SPEC-012 User Note Fallback 경로 재사용). 이후 분류→문서화 게이트·분류 승인(admin)은 slack/manual과 동일·무변경. (AXKG-SPEC-003 §5, AXKG-SPEC-012) — PLAN-013-T-008(`start_summary` 배선, manual과 동일).
- [x] **C-5 FE push CTA·상태 표면** — 방안 답변의 `Source Inbox에 추가` CTA(U-2)와 push 중·완료·`EMPTY_PUSH_TEXT` 상태 표면, 인박스 목록/관리 표면 미노출. 기준 `21-html/page-graph.html` — 레이아웃·한국어 카피 모두 시안을 따른다. (AXKG-SPEC-006 U-2)

## Verification

- [ ] AXKG-SPEC-006 S-4·U-2·push API 계약 반영, 자동 push 없음(CTA로만)
- [ ] AXKG-SPEC-003 `source_channel=chat` 데이터 계약·요약→분류 lifecycle 합류 반영
- [ ] AXKG-SPEC-008 접근 경계 — push는 staff·admin 모두 가능, push 후에도 인박스 목록/관리 표면은 staff에 미노출
- [ ] push된 chat source가 URL 없이 `raw_text`(대화 전부)로 `summarized`에 도달한다

## Rollback

- 작업 레포 커밋 단위 revert. push endpoint 제거 시 기존 채팅·인박스 흐름은 무영향.

## Change Log

| Date | Change |
|---|---|
| 2026-07-14 | work-add. PLAN-013-T-005 WP 분해로 신규 작성(todo). AXKG-DEC-006 개정·AXKG-SPEC-006/003/008 T-002·T-003 산출분 기준. |
| 2026-07-14 | PLAN-013-T-010 FE: 방안 push CTA + push 상태 표면 구현(ax-graph apps/web). C-5 done. BE endpoint 계약 정합은 T-008 리포트 대조 예정. |
| 2026-07-14 | PLAN-013-T-008 BE: C-1~C-4 done. `POST /graph/chats/{chat_id}/push-to-inbox`(staff·admin, owner), 서버 대화 조립(§7 OQ 확정)·`source_channel=chat` source·요약 파이프라인 합류. source_channel enum+URL nullable 마이그(0020, upload 채널 동반). pytest 414 pass(신규 11). 미커밋(admin 검수 대기). |
