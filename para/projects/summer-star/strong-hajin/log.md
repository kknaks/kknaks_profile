# Product Log

> 제품 단위 통합 변경 로그. baseline, decision, spec, work 변경 이력을 한 곳에 모은다.

| Date | Entry | Links |
|---|---|---|
| 2026-09-15 | 업무 페이지 BASE·DEC·SPEC 2건 초안 및 단계 index 생성. 계약·출처·미결 검수 시작 | [입력](00-baseline/README.md) · [결정](10-decision/README.md) · [스펙](20-spec/README.md) |
| 2026-09-15 | 검수 FAIL에 따른 4문서 1차 수정 완료. 문서 ID 정렬, 스펙 v0.2.0 재검수 시작 | [결정](10-decision/README.md) · [스펙](20-spec/README.md) |
| 2026-09-15 | 스펙 0.2.1 문서 정정, WORK-001 초안 및 작업 index 생성. 코드 미착수, WP 검수 시작 | [구현 계획](30-work/work-001-task-creation.md) |
| 2026-09-15 | SPEC 0.2.2·WORK-001 수정 수령. 필수 생성 키·출처/승인 연속성·격리 DB 계획 반영, MCP 재시도 키 추가 정정 중 | [구현 계획](30-work/work-001-task-creation.md) |
| 2026-09-15 | SPEC-001 0.2.3: assigned 출처 상태·MCP 명시 키 확정. WORK-001 수정본 재검수 | [구현 계획](30-work/work-001-task-creation.md) |
| 2026-09-15 | SPEC-001 0.2.4: REST 키 헤더 일원화, WORK-001 잔여 RF-1/RW 정정. 최소 diff 재검수 | [구현 계획](30-work/work-001-task-creation.md) |
| 2026-09-15 | WORK-001 재검수 2차 PASS: RF-1·RW-1~4 해소. 사용자 계획 리뷰 대기, 코드 미착수. 헤더 필수화와 FE 키 전송의 동시 활성화는 구현 발주에 반영 | [구현 계획](30-work/work-001-task-creation.md) |
| 2026-09-16 | 사용자 W1 전체 구현 승인. BE/FE 발주, 코드 리뷰·자동 검증은 코디 담당. E2E는 사용자 수행 | [구현 계획](30-work/work-001-task-creation.md) |
| 2026-09-16 | W1 구현·코드 최종 리뷰 PASS. 코디 BE1297/scale13/release1/PG65, Node20.20에서 FE645·자산·빌드 통과. E2E는 사용자 수행 대기, 미커밋·미배포 | [구현 및 검증 상태](30-work/work-001-task-creation.md) |
| 2026-09-17 | v2 원문·예시·프론트 승인 반영: BASE-002·DEC-002·SPEC-003 v0.3.1. 스펙 검수 WARN 정정 후 BE·FE 통합 WORK-002 초안 작성 및 계획 검수 발주. 코드 미착수, OQ-203·206 답 대기. 단계 index 갱신 | [스펙](20-spec/spec-003-task-lifecycle-v2.md) · [계획](30-work/work-002-task-lifecycle-v2.md) |
| 2026-09-17 | WORK-002 BE·FE 구현 중. FE 검수 F-1 수정 발주, Phase7-A의 Composer를 기존 본문 계약에 따른 표시 눈금으로 명시하고 첨부 범위 유지·실패 재시도 검증 지시. 전체 자동 검증 및 사용자 E2E 미완료 | [계획](30-work/work-002-task-lifecycle-v2.md) |
| 2026-09-17 | Phase7-A 첨부 경계 실물 확인: 기존 자료 쓰기는 활성 담당자만 가능. 본인 생성의 두 단계 첨부를 구현하고 배정·발송·회의는 담당자 상세 첨부로 안내, 자료 권한 확대 및 근거 원장 대체 없음 | [계획](30-work/work-002-task-lifecycle-v2.md) |
| 2026-09-17 | SPEC 확정 계약의 직접취소 사유 입력·검증·이력 누락을 WORK-002 Phase5·7 통합 수정으로 명시. 권한과 미결 정책은 유지하고 BE·FE 동시 인수 | [계획](30-work/work-002-task-lifecycle-v2.md) |
| 2026-09-17 | WORK-002 자동검증 완료: Node20 `make verify` exit0, 격리 PostgreSQL 77 passed, FE 713 passed·tsc·build exit0. 브라우저 E2E는 사용자 수행으로 이관하고 OQ-203·206은 답 대기 유지 | [검증 인계](../../orchestration/work/strong-hajin-work/v2-verification-and-e2e.md) · [계획](30-work/work-002-task-lifecycle-v2.md) |
| 2026-09-19 | DEC-001 D-19·D-20 추가(참조 CC 수신함 읽음·프로젝트 선행업무)와 SPEC-001 0.3.0: 읽음 영수증·수신함 reference 필터·`preceding_task_ids`/`task_predecessors`·finish-to-start 시작 게이트(`WORK_PREDECESSORS_UNFINISHED` 409) 계약화. 코드 미착수 | [결정](10-decision/decision-001-work-page.md) · [스펙](20-spec/spec-001-work-management.md) |
| 2026-09-19 | DEC-001 D-21(업무 만들기 창 최종 프레임) 확정 반영: SPEC-001 §2 U-6 전면 개정(갈래 토글·왼쪽 탭 넷·갈래별 기본 정보·`업무 연결` 탭·참고 업무 UI 내림)과 WORK-003 신규 작성(BE 3·FE 3·공통 1 phase). D-16 의 「창에 없다」는 표로 정정하고 계약·데이터는 보존 | [결정](10-decision/decision-001-work-page.md) · [스펙](20-spec/spec-001-work-management.md) · [계획](30-work/work-003-inbox-predecessor-and-create-frame.md) |
| 2026-09-19 | SPEC/WP 검수 FAIL 수정 완료: S-1·S-2·Flow 의 폐기된 「생성 창 담당 칸」 서술을 D-21 프레임으로 정정(F-1), SPEC 의 WORK 역참조 제거·`works: []` 복귀(F-2), 본문 관계 wikilink 6곳을 ID 서술로 강등(F-3). WARN W-2~W-5·W-7 도 함께 닫고 단계 index·log 갱신(W-1). 계약 변경 0건, 코드 발주 대기 | [리뷰](../../orchestration/work/strong-hajin-work/review-spec-wp-report.md) · [계획](30-work/work-003-inbox-predecessor-and-create-frame.md) |
