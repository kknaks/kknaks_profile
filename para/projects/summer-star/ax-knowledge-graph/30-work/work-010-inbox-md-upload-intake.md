---
type: work
id: AXKG-WORK-010
title: "WP9: 인박스 md 업로드 intake"
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
created_at: 2026-07-14
updated_at: 2026-07-14
tags:
  - product/ax-knowledge-graph
  - doc/work
  - status/done
links:
  baselines:
    - "[[baseline-001-ax-knowledge-graph-from-curated-sources|AXKG-BL-001]]"
  decisions:
    - "[[decision-001-para-pipeline-and-approval-gates|AXKG-DEC-001]]"
  specs:
    - "[[spec-003-source-inbox|AXKG-SPEC-003]]"
    - "[[spec-012-source-collection-adapter|AXKG-SPEC-012]]"
  works:
    - "[[work-002-source-intake|AXKG-WORK-002]]"
  releases: []
  related: []
---

# WP9: 인박스 md 업로드 intake

Source Inbox의 수동 입력 표면(U-3 Direct Inbox Modal)에 URL 외 **md 파일 업로드** intake를 추가한다. v1은 `.md`만 허용하고, URL 수집을 스킵한 채 **업로드된 md 본문 자체가 원문**이 되어 그대로 요약 입력이 된다(fallback이 아니라 원문 그 자체 — AXKG-SPEC-012 adapter 대상 아님). 기존 수동 입력 표면의 확장이라 admin 전용이며 접근 경계 변경은 없다. BE + FE.

## Meta

- Baseline: AXKG-BL-001
- Covers spec: AXKG-SPEC-003(`source_channel=upload` intake·S-5·U-3 업로드 UI·`UNSUPPORTED_UPLOAD_TYPE`·`original_filename`), AXKG-SPEC-012(업로드는 adapter 수집 대상 아님 — 경계)
- Covers decision: AXKG-DEC-001(PARA 파이프라인 — 업로드 source도 동일 요약→분류 흐름)
- Depends on work: AXKG-WORK-002(WP1 — Source Inbox·U-3 모달·요약 파이프라인)
- Parallel work: AXKG-WORK-008(WP7), AXKG-WORK-009(WP8)
- Follow-up work: pdf/docx 등 타 포맷 업로드(파싱 계층 필요, 이번 라운드 제외·parking)
- External dependency: 없음

## Scope

포함:

- BE 업로드 endpoint — `.md`만 허용, `original_filename` 보존, URL 수집 스킵→요약 직행, admin 전용
- `source_channel=upload` source 생성(`source_url=null`·`slack_message_ts=null`·`raw_text`=md 본문 필수)
- received→요약①→분류 파이프라인 합류(업로드 md 본문 자체가 원문)
- FE Direct Inbox Modal(U-3) 업로드 UI — `md 파일 업로드` CTA·선택 파일명·허용 형식(.md)·형식 오류 표면

제외:

- md 외 포맷(pdf/docx 등) — 파싱 계층 필요, 후속 확장(parking)
- URL 수집 adapter 경로 (업로드는 adapter 대상 아님, AXKG-SPEC-012)
- 분류/문서화 게이트 자체 (AXKG-SPEC-001/002/004 무변경)

## Progress Checklist

코드 발주 단위(C-item). 계약·스펙 참조 수준까지만 — 파일 크기 상한·md 본문 저장 위치·frontmatter 처리는 AXKG-SPEC-003 §7 OQ대로 구현 기본값으로 확정한다.

- [x] **C-1 업로드 endpoint** — `.md`만 허용하고 그 외 형식은 `UNSUPPORTED_UPLOAD_TYPE`으로 거부(source row 미생성 intake validation, 수집 실패와 무관), admin 전용. (AXKG-SPEC-003 §4 API·S-5) — PLAN-013-T-009(`POST /sources/upload`, multipart `file`, sources 라우터 `require_admin`).
- [x] **C-2 upload source 생성** — `source_channel=upload`·`source_url=null`·`slack_message_ts=null`, `raw_text`=업로드 md 본문(필수)·`original_filename` 보존, `received`. (AXKG-SPEC-003 Data Contract) — PLAN-013-T-009(`create_upload`, `original_filename` 컬럼 마이그 0021).
- [x] **C-3 요약 직행** — URL 수집을 스킵하고 업로드 md 본문 자체가 원문이 되어 곧 요약 입력(fallback 아님·원문 그 자체, AXKG-SPEC-012 adapter 대상 아님). 이후 요약→분류 흐름·분류 승인(admin)은 slack/manual/chat과 동일. (AXKG-SPEC-003 §5, AXKG-SPEC-012 경계) — PLAN-013-T-009(`start_summary` 배선, adapter 미경유).
- [x] **C-4 FE 업로드 UI** — Direct Inbox Modal(U-3)에 `md 파일 업로드` CTA·선택 파일명·허용 형식(.md)·형식 오류(`UNSUPPORTED_UPLOAD_TYPE`) 표면, admin 전용 표면(경계 변경 없음). 한국어 카피 시안 기준. (AXKG-SPEC-003 U-3)

## Verification

- [ ] AXKG-SPEC-003 S-5·U-3·`source_channel=upload` 데이터 계약·`UNSUPPORTED_UPLOAD_TYPE` 반영
- [ ] `.md`가 아닌 업로드는 거부되고 source가 생성되지 않는다
- [ ] upload source가 URL 수집 없이 md 본문(`raw_text`)으로 `summarized`에 도달한다(fallback 아님)
- [ ] 업로드 표면이 admin 전용이며 접근 경계 변경이 없다(AXKG-SPEC-008 소스 Inbox 표면 행에 포섭)

## Rollback

- 작업 레포 커밋 단위 revert. 업로드 endpoint·UI 제거 시 기존 URL intake는 무영향.

## Change Log

| Date | Change |
|---|---|
| 2026-07-14 | work-add. PLAN-013-T-005 WP 분해로 신규 작성(todo). AXKG-SPEC-003/012 T-004 산출분 기준. |
| 2026-07-14 | PLAN-013-T-010 FE: Direct Inbox Modal md 업로드 UI 구현(ax-graph apps/web). C-4 done. BE endpoint 경로·필드 정합은 T-009 리포트 대조 예정. |
| 2026-07-14 | PLAN-013-T-009 BE: C-1~C-3 done. `POST /sources/upload`(admin, multipart `file`)·`source_channel=upload` source·`original_filename` 마이그(0021)·요약 직행(adapter 미경유). FE(T-010) 계약 정합: 경로 `/sources/upload`·필드 `file`·`UNSUPPORTED_UPLOAD_TYPE`. OQ 확정 — 크기상한 1MiB·frontmatter 보존. pytest 425 pass(신규 11). 미커밋(admin 검수 대기). |
| 2026-07-14 | 라운드 마감: pytest 425 게이트·prod 배포(717c95e)·FE-BE 계약 정합 확인(/sources/upload·file 필드). 업로드 라이브 E2E는 미실시(pytest 검증). status done. |
| 2026-07-14 | PLAN-013-T-011 BE 버그픽스: upload 요약이 수집 어댑터를 타 `INVALID_URL`→`collection_failed`(prod 786d3a5d). C-3 계약 위반 수정 — `source_summary.py` 빌더가 `source_channel==upload`면 collect 미경유로 `build_upload_material`(raw_text=원문, adapter/format=upload/markdown) 합성. `queue_collection` 재시도는 upload면 note를 무시해 raw_text(원문) 미덮어씀. 회귀 테스트 실 collect 경로(`_collect_forbidden`)로 collect 미호출·raw_text 요약입력·재시도 검증. pytest 427 pass(신규 2). 미커밋(admin 검수 대기). |
