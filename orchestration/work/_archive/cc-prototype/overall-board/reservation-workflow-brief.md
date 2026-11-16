# [planner] 예약 구간 워크플로 — workflow-v3.md 작성

너는 **cc-prototype `planner` 워커**다. **앞 판의 맥락이 없다** — 이 브리프와 아래 파일만 믿어라. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc` (코디 워크트리 — 코디 · 다른 워커와 공유. allowed_paths 밖은 건드리지 마라)

## 1. SSOT — 먼저 읽을 것

- **결정 정본 = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/_RESUME.md` §2 결정 표의 2026-10-26 「예약 …」 줄 전부** + §1 의 2026-10-26 메모 2줄(시술 현황판 2계층 · 상담사 알림). 취소선 줄은 뒤집힌 것 — 지금 것만. 「사용자 지시」와 「코디 기본값」을 구분해 옮긴다
  - 같은 표의 2026-10-23 · 10-25 줄은 **시술 현황** 결정이다. 예약 구간과 닿는 것(「방 배정」 작업 · 카드 방 판정)만 참고
- **형식 원본 = `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-12-cc-prototype/workflow-v2.md`** — 같은 절 구성 · 같은 말투로 쓴다
  - 원칙 · 화면 · 큰 흐름 · 단계별(번호 절) · **KOS 반영 표** · 인증 · 계정(바뀐 것만) · 보류 · 다음 버전 · 정할 것
- 처음 구상 `workflow-v1.md`(같은 폴더) 1 ~ 5절 · 원 아이디어 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/00-baseline/baseline-004-reservation-idea.md`
- **시안(정본)** 분석: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/design-analysis-report.md` §3(예약 현황 전체) · §6 예약 행 · §7.2 · §11
- **KOS 조사 리포트 12개**(같은 `work/overall-board/` 폴더 — KOS 반영 표의 근거). 순서대로:
  1. `reservation-read-report.md` — 조회(스케줄 표 · 상태 · 권역 = 예약 그룹 · 공지 · 이전 방문)
  2. `reservation-questionnaire-report.md` — 문진(링크 · 제출 · 모달 필드)
  3. `reservation-visitor-update-report.md` — 기존 고객 수정 · 중복 확인
  4. `reservation-create-report.md` — 예약 등록(기존 · 신규) · 슬롯 · 정원
  5. `reservation-room-report.md` — KOS 접수 · 방 배정 우회 순서
  6. `reservation-reception-test-report.md` — ccc 접수 묶음 데모 실호출(성공)
  7. `reservation-memo-test-report.md` — 특이사항 = `visitor.memo` 실호출
  8. `reservation-move-cancel-report.md` — 이동 · 취소 · 부도 · 되돌리기 실호출
  9. `reservation-consultation-report.md` — 상담 구간
  10. `reservation-payment-discharge-report.md` — 수납 딥링크 · 수납 정보 · 귀가
  11. `reservation-postpay-report.md` — 후납 = 작업 `paymentRequired`
  12. `reservation-postpay-check-report.md` — 후납 수납 뒤 꺼짐 · KOS 소켓
- 시술 현황 계약(겹치는 데이터 · 규칙 확인용, 읽기만): `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/10-decision/decision-005-procedure-board.md`(D-08 · D-09 · D-12 ~ D-15) · `20-spec/spec-003-procedure-board.md` · `20-spec/spec-004-procedure-app.md` §3(계정 · 역할)

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 쓰나

workflow-v2 는 **시술 구간**(수납 뒤 ~ 귀가 대기)이다. 이번 v3 는 그 **앞 구간 — 예약 → 접수 → 상담 → (수납 · 시술 대기는 KOS) → 시술 구간 넘김**과 **귀가 대기 정산 · 귀가 완료**다. 「Ceramique 전체현황판」 시안의 「현황 › 예약 현황」 화면(스케줄 표 · 예약 등록 모달 · 예약 상세 모달 · 오른쪽 패널)을 기준으로 2026-10-26 사용자와 닫은 흐름을 문서로 옮긴다. **새로 정하지 마라 — `_RESUME` 결정과 리포트에 있는 것만.**

v2 와의 관계: v3 머리에 「뒤 구간 = workflow-v2」 링크 · v2 의 원칙(KOS 동기화 · KOS 기준 · ccc DB 가 KOS 를 품음 · 현장은 KOS 를 직접 조작하지 않는다 등)은 **다시 쓰지 말고 참조**하되, 예약 구간에서 달라진 것은 적는다 — 특히 **상담사가 상담 · 수납 · 시술 추가 · 시술 대기 전환을 KOS 에서 직접 한다**(v2 의 「현장은 KOS 를 직접 조작하지 않는다」와 범위가 다르다 — 그 차이를 원칙 절에 명시).

## 3. 계약 — 반드시 담을 것

1. **원칙**: KOS 와 ccc 는 항상 같은 데이터(사본 + KOS 기준) · KOS 에 없으면 안 쓴다 / KOS 에 있으면 칸을 만든다(예외: 「희망 시술」 선택) · 시안이 정본, 시안과 KOS 가 다르면 KOS 칸에 맞춰 시안을 고친다(문진 · 예약 모달) · 상태 2계층 · 웹이 정본
2. **화면 표**: 예약 현황(스케줄 표 · 오른쪽 패널 「예약 요청」(자리만) · 「원내 현황」) · 예약 등록 모달 · 예약 상세 모달(접수 전 / 접수 뒤) · 앱(QR · 스캐너 · 상담사 알림) — 이번 범위 ✅ / 자리만 / ❌
3. **큰 흐름** 그림(v2 처럼 text 블록) — ccc 가 하는 일과 KOS 에서 사람이 하는 일을 구분해 보이게
4. **단계별 절** — 최소: 예약 현황(스케줄 표 · 상태) / 예약 등록 / 예약 이동 · 취소 · 부도 / 접수 — 고객 정보(신분증 스캔 + 문진) · 특이사항 · 이전 방문 / 접수 완료 = 방 배정 / 상담(실장 호출) / 수납 · 시술 대기(KOS) / 귀가 대기 정산 · 귀가 완료. 각 절에 **AS-IS(KOS 현장)** 가 리포트에 있으면 짧게(예: 방 배정 우회)
5. **KOS 반영 표**(v2 와 같은 열: ccc 조작 · 어디서 · KOS 호출 · 종류(공개/내부)) — **이번엔 「조사 필요」로 비우지 않는다.** 리포트 12개에서 확인된 호출을 채우고, 데모 실호출로 확인한 것은 「(2026-10-26 데모 확인)」을 붙인다. 확인 안 된 것은 「미확인」 + 리포트 Q 번호
6. **ccc DB 에만 있는 것** 목록(신분 확인 상태 · 문진 방문별 이력 · 조작 로그 · 취소 되돌리기 로그 등) — `_RESUME` 결정 그대로
7. **계정 · 역할**: 코디 역할 추가 · 상담사(실장) 계정 필요(알림) · 동시 로그인 — 구상 단계면 그렇게 표시
8. **보류 · 다음 버전**: 본사 예약 요청(자리만) · 취소 되돌리기 버튼 · KOS 소켓 실시간 · 시술 현황판 2계층 맞추기 등
9. **정할 것 표**(v2 형식: 항목 · 기본값(안 정하면)): 리포트 Q-1 ~ Q-122 중 `_RESUME` 결정으로 **닫히지 않은 것만** 모아, 비슷한 것은 묶는다. 닫힌 Q 는 「(2026-10-26 정해짐)」 취소선 줄로 두지 말고 아예 빼도 된다(v3 는 새 문서). 각 줄에 근거 리포트 · Q 번호
10. 출처 머리말: 날짜 · 「사용자와 정리」 · `_RESUME` · 리포트 목록 · HAR 은 gitignore(파일 이름만)

## 4. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-26-cc-reservation/workflow-v3.md` — 새 파일 1개(폴더도 새로)
- workflow-v2.md · para/ · _RESUME · 리포트 · 코드 수정 금지(v2 와 어긋나는 걸 찾으면 고치지 말고 보고에 적는다)

## 5. 범위 제약 — 하지 말 것

- **새 결정 금지.** `_RESUME` · 리포트에 없는 동작을 지어내지 마라. 빈 곳은 「정할 것」으로
- **public 레포**: 실명(시안 공지 예시 · 리포트의 직원 이름 포함) · KOS id(테넌트 · 고객 · 일정 · 계정) · 키 · 토큰 · 딥링크의 실제 id · 금액 실제 값 금지. 경로는 `{tenantId}` 꼴로
- HAR 내용을 붙이지 마라 — 리포트 요약 + 리포트 절 번호
- 커밋 · push · PR 금지

## 6. 검증

```
_RESUME §2 의 2026-10-26 예약 결정 줄마다 v3 의 어느 절에 들어갔는지 대조표를 보고에 붙인다(빠진 줄 0). KOS 반영 표의 호출마다 근거 리포트 절. 정할 것의 Q 번호가 닫힌 결정과 겹치지 않는지
```

- 실명 · id grep 0건(테넌트 id 24자리 hex · `eyJ` · 시안 공지의 원장 이름 등)

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 과 preamble 이 다르면 preamble 쪽으로만 보낸다. 같은 워크트리에 다른 코디 세션(시술 현황 되돌리기)이 있다 — 그쪽으로 보내지 마라.

- 커밋 · push · PR 하지 마라. 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_fa2737b7-e69a-40e1-9fac-019199b9dad3 --from <네 handle> \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "planner 완료: workflow-v3 <한 줄>" \
  --body "파일 경로 / 절 구성 / 결정 대조(빠진 줄 수) / KOS 반영 표 행 수 / 정할 것 개수 / v2 와 어긋난 곳"

orca terminal send --terminal term_fa2737b7-e69a-40e1-9fac-019199b9dad3 \
  --text "[worker_done] planner workflow-v3 완료 — <한 줄>. 상세는 인박스." --enter
```

- 막히면 30분 이상 헤매지 말고: `orca terminal send --terminal term_fa2737b7-e69a-40e1-9fac-019199b9dad3 --text "[질문] planner: <질문>" --enter`
