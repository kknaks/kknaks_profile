# Product Log

> 제품 단위 통합 변경 로그. baseline, decision, spec, work 변경 이력을 한 곳에 모은다.

| Date | Entry | Links |
|---|---|---|
| 2026-09-24 | 로컬 웹·Tauri 재실행 절차와 Mac Studio 운영 배포의 현재 상태·차단 항목을 환경 문서와 RUNBOOK-001로 분리해 기록 | [환경 구성](40-architecture/deploy/environments.md) · [로컬 실행](70-runbook/runbook-001-local-tauri.md) |
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
| 2026-09-21 | 「프로젝트」 화면 착수. 시안 정독 후 read-only 조사 2건 발주(BE 726줄·FE 500줄) → D-1~D-9 중 **있다 6·다르다 2·없다 1**. 사용자와 결정 10건을 닫고 BASE-004·DEC-004 작성. 진행률은 저장하지 않고 체크리스트로 파생, 관리 기능은 모달로 분리. 미결 9건 답 대기, 코드 미착수 | [입력](00-baseline/baseline-004-projects.md) · [결정](10-decision/decision-004-projects.md) |
| 2026-09-21 | DEC-004 개정: 미결 9건을 사용자와 전부 닫고 결정 **27건**으로(D-11~D-27 신규). 간트는 깊이 제한 없는 **재귀 트리**(코디의 「2단계」 제안은 철회 — 선행에 깊이 제한이 없어 의존선이 조용히 사라진다), **손자도 프로젝트에 종속**(`children_of` 직속만 도는 것 수정), **배정·발송 시 프로젝트 자동 초대**와 **거절·철회 시 자동 해제**(조건 둘). BASE-004 어긋남 4건으로. 코드 미착수 | [입력](00-baseline/baseline-004-projects.md) · [결정](10-decision/decision-004-projects.md) |
| 2026-09-21 | SPEC-005 확정(1121줄·인수조건 75·열린 미결 0). 검수 FAIL 4·WARN 5 를 전부 닫음 — 상태 어휘를 「외부 계약은 넷 + `blocked` 는 M-6 통과값」으로 바로잡고, 프로젝트 이동 게이트를 `WORK_PROJECT_LOCKED_BY_PREDECESSORS` 로 정정, 떼는 자리에 직접 배정 철회를 추가, 근거 없는 결정 번호 3자리 강등. 요약 스트립 모수는 「취소를 뺀 업무」 하나로 통일(D-04 해석 확정). 새 라우트 0·새 오류 0 | [스펙](20-spec/spec-005-projects.md) · [검수](../../orchestration/work/strong-hajin-projects/review-spec-005-report.md) |
| 2026-09-21 | WORK-005 확정(1222줄·Phase 6·인수조건 75줄 전수 배정). 검수 FAIL 4·WARN 6 을 SPEC·WP 동시 수정으로 닫음 — **직접 배정 경로는 자동 초대가 원리적으로 불가**(`TaskAssignmentInput` 이 non-null `project_id` 를 거부)해 붙는 자리를 셋→**둘**로, 요청 발송도 배정 행을 만든다는 사실이 드러나 흔적 컬럼을 두 표→**`task_assignments` 한 칸**으로 좁힘. `-p no:randomly` 는 미설치라 무동작이어서 제거. 코드 미착수 | [스펙](20-spec/spec-005-projects.md) · [계획](30-work/work-005-projects.md) · [검수](../../orchestration/work/strong-hajin-projects/review-wp-005-report.md) |
| 2026-09-22 | **Phase 0 닫힘** — `material_*` 병렬 흔들림의 원인은 「테스트가 자식 프로세스를 띄우고 초 단위 실시간 창을 잰다 + `-n auto`(코어 11)의 스케줄 지터」. `@pytest.mark.serial` 마커로 가르고 `conftest` 걸개로 재발을 막았다(제품 코드 0줄). **`make verify` exit 0 · 실패 0건** — 캘린더 작업 전부터 있던 부채가 닫혔다. 그리고 **브라우저 E2E 1차** 후 수정 지시 11건을 받아 **DEC-004 결정 38건**(D-28~D-38 · **D-12 뒤집음**) · **SPEC-005 v0.2.0**(계약 변경은 체크리스트·업무내용 읽기 범위 하나) · **WORK-005 2루프 Phase BE-3→FE-4→FE-5 직렬**(인수조건 2루프 52줄) 로 개정. 검수 FAIL 6 을 닫으며 **조사가 틀렸던 사실 하나**(`external_key` 를 API 가 받는다)를 바로잡았다. 코드 미착수·커밋 0건 | [결정](10-decision/decision-004-projects.md) · [스펙](20-spec/spec-005-projects.md) · [계획](30-work/work-005-projects.md) |

| 2026-09-22 | DEC-005 accepted: Tauri 웹 래퍼 목적을 회의 녹음·후속 OS 알림으로 확정. 쿠키 로그인 유지, 녹음 중 자동 절전 방지, 참조 설치파일 빌드 구성 계승 및 지속 배포 문서화. 구현·배포 미착수 | [결정](10-decision/decision-005-tauri-wrapper.md) |
| 2026-09-22 | 루프2 구현 완주 — BE-3(게이트 제거·체크리스트 읽기 범위) · FE-4(간트 틀고정·오늘 기준·자동 스크롤) · FE-5(생성 모달·레일 머리·업무 정보·상태 드롭다운) 를 각각 **구현→검수→수정** 으로 돌렸다. 검수가 건진 것: 완료 보고 거절이 **화면에 안 뜨던 것**(`onError` 차단) · 우리가 더한 테스트의 **flaky**(9회 중 1회) · **자기참조 단언** 둘 · 조사가 틀린 사실(`external_key` 는 API 가 받는다). 사용자 확인 뒤 **~~D-31~~ 을 D-39 로 뒤집음**(「프로젝트 추가」는 누구에게나 선다 — 서버는 여전히 자격을 쥐고 거절은 모달이 말한다). 커밋 0건 | [결정](10-decision/decision-004-projects.md) · [스펙](20-spec/spec-005-projects.md) |

| 2026-09-22 | SPEC-006 draft 및 Tauri 적용 조사 작성. 별도 Claude 검수 착수. 운영 프로파일·녹음 포맷 실측·일시정지 범위 등 미결을 분리. 구현 미착수 | [스펙](20-spec/spec-006-tauri-wrapper.md) |

| 2026-09-22 | SPEC-006 독립 검수 FAIL 5·WARN 10 후 수정 발주. 비가시 상태 절전 방지·실제 세션 만료 동작·도달 가능한 녹음 상태·문서 탐색 경계 정정. WebKit 포맷 지원은 최신 공식 문서로 재확인 | [스펙](20-spec/spec-006-tauri-wrapper.md) |

| 2026-09-22 | SPEC-006 v0.2.0 재검수 착수. 절전 점유를 네이티브 소유로 변경하고 세션·화면 전환 사실 정정. 문서 draft 유지, 제품 구현·실측 미착수 | [스펙](20-spec/spec-006-tauri-wrapper.md) |

| 2026-09-22 | SPEC-006 v0.2.1 수정 수령·R2 수정 범위 재검수. 취소된 닫기·재무장·늦은 요청·호출 실패 계약 보완. 인수조건 43개, 실측 미수행·draft 유지 | [스펙](20-spec/spec-006-tauri-wrapper.md) |

| 2026-09-22 | SPEC-006 문서 검수 종료: Claude R3 FAIL 0·WARN 5 후 코디 문구 정리(v0.2.2). AC 43건·실측 15건. 사용자 미결·실측 미완으로 draft 유지, WP·제품 코드 미착수 | [스펙](20-spec/spec-006-tauri-wrapper.md) |

| 2026-09-22 | DEC-005 D-07~09·SPEC-006 v0.2.3: macOS·Windows 지원, Mac Studio 운영 FE·BE, 코드 GitHub Releases 설치파일·프로필 60-release 문서 관리 확정. 도메인·최소 OS·아키텍처·서명 등 세부 및 실측은 남음. 구현·배포 미착수 | [결정](10-decision/decision-005-tauri-wrapper.md) · [스펙](20-spec/spec-006-tauri-wrapper.md) |

| 2026-09-22 | WORK-006 계획 검수 종료: R2 승인저지0·회귀0 후 WARN3·경미4 문구 정리 및 코디 확인. 10단계에 AC43·실측15 배정. 기존 코드 워크트리 계승, 운영 실행 포함, origin 설정→최종 빌드→검증→동일 설치파일 발행. 사용자 계획 리뷰 전·구현/실측/배포 미착수 | [계획](30-work/work-006-tauri-wrapper.md) |

| 2026-09-22 | 사용자 야간 구현 Goal 승인: Phase별 구현→검수→수정 직렬 루프. WORK-006 Phase 1 Claude 구현 발주, Rust 검증 설정 추가. 코드·자동검증 우선, 사용자 설치·최종 E2E는 다음 날. 실제 운영배포·Release 미수행 | [계획](30-work/work-006-tauri-wrapper.md) |
| 2026-09-24 | Tauri 로컬 앱 실행과 월간 날짜·주간 종일·주간 시간 드래그 앤 드롭을 사용자 실측으로 확인. WKWebView의 HTML5 드롭을 선점하던 Tauri 네이티브 파일 드롭 핸들러를 제품 창에서 비활성화해 웹과 같은 드래그 미리보기·저장 흐름을 복원했다. 날짜 선택기 정렬·여백과 월간 일정 막대 폭도 보정. 다음 세션은 디자인 정리와 배포 준비이며 운영 origin·로그인·서명/공증·Windows·Release는 미완료로 유지 | [계획](30-work/work-006-tauri-wrapper.md) · [구현 상태](../../../../orchestration/work/strong-hajin-projects/tauri-implementation-status.md) |
