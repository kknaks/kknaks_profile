# [planner] 예약 현황 — BASE-009 · DEC-006 · SPEC-005 · WORK-007 (+ workflow-v2 남은 4곳)

너는 **cc-prototype `planner` 워커**다. **앞 판의 맥락이 없다** — 이 브리프와 아래 파일만 믿어라. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc` (코디 워크트리 — 공유. allowed_paths 밖은 건드리지 마라)

## 0. 사용자 지시 (2026-10-26)

「**코드까지 다 작성해서 알려줘 — e2e 로컬 해보게**」. 이번 판은 그 첫 단계 — 구현 워커(BE · FE)가 그대로 짤 수 있는 계약을 쓴다. 문서 뒤에 reviewer_doc 검수 → BE ∥ FE → reviewer → 코디 검증 → 사용자 로컬 E2E 순서다.

## 1. SSOT — 먼저 읽을 것

- **흐름 정본 = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-26-cc-reservation/workflow-v3.md`**(418줄 · 사용자와 닫은 예약 구간). 그 머리말의 리포트 15개(`orchestration/work/overall-board/reservation-*-report.md`)가 KOS 근거
- **결정 정본 = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/_RESUME.md` §2 의 2026-10-26 줄 전부** + §1 메모. 취소선은 뒤집힌 것. 「사용자 지시」/「코디 기본값」 구분 유지
- **시안(정본)**: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/design/Ceramique 전체현황판.dc.html` 「예약 현황」 `M:93-715` · 분석 `orchestration/work/overall-board/design-analysis-report.md` §3 · §6 · §7.2 · §9 · §10 · §11
- **같은 앱의 지금 계약 · 형식 원본**(읽기만): `para/projects/summer-star/cc-prototype/` — `10-decision/decision-005-procedure-board.md` · `20-spec/spec-003-procedure-board.md`(0.5.1 — 절 구성 · 문체 · OQ 번호 방식의 원본) · `20-spec/spec-004-procedure-app.md`(계정 · 역할 §3) · `30-work/work-006-overall-board-undo.md`(WORK 형식) · `00-baseline/baseline-004-reservation-idea.md` · `baseline-008-procedure-board.md` · 각 폴더 `README.md`(번호 · frontmatter 규칙)
- **코드 현실**(읽기만 · 계약을 코드에 맞게): `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/`(back = FastAPI · front = Next.js · `README.md` · `docker-compose.yml`). KOS 클라이언트 · 동기화 · 계정 · 이벤트 로그 · 헤더 「현황」 드롭다운이 이미 있다 — **새 기능 폴더를 만들지 말고 `procedure/` 안에 예약 현황을 더한다**(같은 헤더 「현황 › 예약 현황」)

기대는 개념: 해당 없음.

## 2. 쓸 문서 (allowed_paths)

`/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/` 아래:

1. **`00-baseline/baseline-009-reservation-board.md`** — 원천 기록: 사용자 대화 2026-10-26 · workflow-v3 · 리포트 15개 · HAR 은 이름만(gitignore). 「이해한 것」 수준(새 결정 없음)
2. **`10-decision/decision-006-reservation-board.md`** — `_RESUME` 10-26 예약 결정을 D-01 ~ 로. 각 줄 근거(사용자 지시 / 코디 기본값 / 조사 결과 · 리포트). DEC-005 와 겹치거나 범위를 나누는 것(D-10 범위 · 2계층 상태 · 「같은 데이터」 원칙)은 DEC-005 번호로 잇는다
3. **`20-spec/spec-005-reservation-board.md`** — 구현 계약. SPEC-003 절 구성을 따른다: 범위 · 폴더 · 실행 · 데이터 모델(ccc 사본 + ccc 만의 것) · KOS 연동(조회 주기 · 인증 · 호출별 본문 모양 — 리포트 근거) · 상태 · 규칙(2계층 · 수납 필요 · 정원 · 접수 묶음 · 실패 · 반영 지연) · 화면(시안 기준 · 시안과 다른 곳 표) · back ↔ front API(경로 · 요청 · 응답 · 오류) · KOS 반영 표 · **검증 기준 — 로컬 E2E(데모 지점) 시나리오 표** · 열린 것(OQ-701 ~)
4. **`30-work/work-007-reservation-board.md`** — WP 쪼개기 · BE ↔ FE 계약 고정점 · 병렬 · 하지 않는 것 · 검증 명령
5. 각 폴더 `README.md` 목록 갱신(있다면) · DEC-005 / SPEC-003 / SPEC-004 frontmatter `links` 에 새 문서 한 줄(본문 수정 금지)
6. **`/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-12-cc-prototype/workflow-v2.md` 남은 4곳**(`orchestration/work/overall-board/reservation-workflow-v3-r2-report.md` §코디 확인 4): 정렬 [입실순 | 배치순] 버튼 · 헤더 메뉴 「현황」 하나 · KOS 반영 표에 [시작] · [종료] 되돌리기 행 · 카드 드래그 순서(ccc DB). v2 규칙(취소선 + 「(2026-10-2X 바뀜)」 + 지금 것)
- 보고서: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-spec-report.md`

## 3. 범위 — 코디 기본값(사용자 통보 예정 · SPEC §1 에 그대로 적는다)

**이번 판 = 웹(간호 스테이션 · 데스크 PC) + back.** 「웹이 정본, 앱은 나중에 웹에 맞춘다」(사용자 지시).

넣는다
- 헤더 「현황」 드롭다운에 **「예약 현황」** 하위 화면 추가(시술 현황은 그대로)
- **스케줄 표**: 날짜 이동 · [오늘] · 칸 = KOS 예약 그룹 전부(order 순) · 시간축(그룹 운영 시간 · 칸마다 자기 간격 · 1시간 높이 같음 · 운영 밖 회색 · 칸 머리 「{정원}명 / {간격}분」) · 카드(성별 · KOS 이름 · 발음 · 초진/재진 · 국기(ISO → 그림) · 주 상태 색 + 부상태 뱃지) · 범례 7(예약 · 접수 · 상담 · 시술 · 귀가 · 취소 · 부도) · 총 예약 N건(취소 · 부도 뺌) · 칸 [+] → 예약 등록 · **드래그 이동**(정원 꽉 찬 칸 미리 막기 · 거절이면 원위치 + 토스트 · 길이 유지)
- **오른쪽 패널**: 「예약 요청」 탭 = **공지(그 날짜 KOS 공지 · 읽기)** + 예약 요청 목록 **자리만**(빈 상태) · 「원내 현황」 탭(필터 · 카드 · 수납 필요)
- **예약 등록 모달**: 고객 검색(내부 `get-visitors`) · 결과 표 · 이름 같은 고객 경고 · 신규/기존 · KOS 예약 칸 그대로(상담 필요 · 수면마취 · 귀가 희망 · 예약 담당자 · 당일 지정 의사 · 희망 상담사 · 유입 KOS 코드 · 예약 메모) · 신규 구분 규칙(이름 + 다섯 중 하나) · 내부 `find-duplicated` → `create-visitor` → `reserve`
- **예약 상세 모달**: 고객 기본 정보(KOS 값 먼저 채움 → 고쳐 저장 = 내부 `update-visitor-personal-information` 읽은 묶음 전체) · 신분 확인(**ccc 상태 · 이번 판은 데스크가 웹에서 [확인 완료] 수동 표시** — 앱 스캐너는 나중) · 유입 · 예약 메모 · **건강 정보(KOS 문진 답 읽기 · 「확인 필요」 기준)** · **특이사항**(`visitor.memo` 읽기 · 쓰기 = 관리 묶음) · 이전 방문(오늘 빼고) · 진행 경로 = 상담 필요 체크(`updateReservationV2.consultationRequired`) · [시술실 선택] → **[접수 완료] 묶음**(recept → 방 배정 작업 → change-tasks-room → 상담 대기/시술 대기) · [예약 취소](취소 | 부도) · 접수 뒤 「내원 현황」(상담 카드: [상담사 선택](직원 사본 COUNSELOR · 지금 상태 계산) → [실장 호출] = `update-reservation{counselor}` · 단계 카드 2계층) · 「귀가 대기」 정산(전체 · 결제 금액 · **수납 필요 N건**(후납 금액 없음) · [수납하기 ›] 딥링크 `tab=purchase` · [처방전 출력] 딥링크 `tab=etceteraWork` · [귀가 완료] = `changeFlowStep(COMPLETED)` · 수납 필요면 꺼짐)
- **계정**: 역할 **코디** 추가(권한 제한 없음 — 직무별 제한은 마지막에)
- ccc DB: 신분 확인 상태 · 조작 이벤트 로그(취소 되돌리기는 로그만) · 문진 방문별 이력 테이블(이번 판은 쓰는 길이 없으면 스키마 + 읽기 때 쌓기 중 planner 가 정해 OQ 로)

빼는 것(SPEC §1 「하지 않는 것」)
- 앱 전부: 고객 QR 문진 입력 · 태블릿 띄우기 · 신분증 스캐너 · 상담사 푸시 알림 · 상담사(실장) 계정 연결
- 본사 예약 요청(Linky) 동작 · 승인/반려 모달 동작 — 자리만
- 취소 되돌리기 버튼 · KOS 소켓 실시간(10초 조회 유지) · 시술 현황판 2계층 맞추기(OQ 로) · 여정 리포트

## 4. 열린 것 처리

workflow-v3 「정할 것」 42행: **구현에 꼭 필요한 것은 기본값을 정해 SPEC 에 쓰고 OQ 에 「planner 기본값 — 사용자 확인 대기」로 표시**(예: 하루 일정 조회 길 = 내부 `get-schedules-for-reservation` 1번 + 10초 · 이동 = 공개 `updateReservationV2` · 접수 = 내부 `recept` · 공개/내부 선택 근거는 리포트). 구현에 필요 없는 것은 OQ 로만. **새 정책을 지어내지 말고 리포트 · 결정 · 시안 안에서 고른다.**

## 5. 하지 말 것

- 코드 수정 금지 · `_RESUME` · 리포트 · workflow-v3 수정 금지(어긋나면 보고)
- **public 레포**: 실명(시안 공지 · 직원) · KOS id · 키 · 토큰 · 실제 금액 · 실제 지점 처방 HAR 내용 금지. 시안 실명이 화면 예시로 필요하면 가짜 값으로(SPEC 에 「시안 실명 치환」 규칙 한 줄 — 디자인 Q-22)
- 커밋 · push · PR 금지

## 6. 검증

```
DEC-006 = _RESUME 10-26 예약 결정 줄 전부(대조표 · 빠진 줄 0) · SPEC-005 의 KOS 호출마다 근거 리포트 절 · SPEC §9 E2E 시나리오가 §3 「넣는다」 항목을 모두 덮는지(대조표) · WORK-007 WP 가 SPEC 절을 모두 덮는지
```
- 실명 · id grep 0(새 문서 4개 + v2)

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 같은 워크트리에 다른 코디 세션(시술 현황)이 있다 — 그쪽으로 보내지 마라.

- 커밋 · push · PR 하지 마라. 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_fa2737b7-e69a-40e1-9fac-019199b9dad3 --from <네 handle> \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "planner 완료: 예약 현황 문서 <한 줄>" \
  --body "파일 목록 / DEC 줄 수 · 대조 / SPEC 절 · API 수 · E2E 시나리오 수 / WP 수 / planner 기본값 OQ 목록 / v2 4곳"

orca terminal send --terminal term_fa2737b7-e69a-40e1-9fac-019199b9dad3 \
  --text "[worker_done] planner 예약 현황 문서 완료 — <한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_fa2737b7-e69a-40e1-9fac-019199b9dad3 --text "[질문] planner: <질문>" --enter`
