# [planner] ② 시술 현황 다음 판 — SPEC-003 0.5.1 → 0.6.0 · WORK-008 · workflow-v2 시술 차트 초안

너는 **cc-prototype `planner` 워커**다. **앞 판 맥락이 없다.** 먼저 역할 문서를 읽어라:
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/planner/role.md` (+ 같은 폴더 rules · skills · tools · workflow) — 「배포된 웹 화면은 구현본이 정본」(10-27) 줄 확인

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc` (코디 워크트리 — 공유. allowed_paths 밖 금지)

## 1. SSOT
- 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/_RESUME.md` §2 **2026-10-26 · 10-27 줄 중 시술 현황에 닿는 것**: 「시술 현황판 상태값 2계층」(§1 메모) · 「부상태 색 규칙」(10-27) · 「시술 카드 드래그 놓기 W2」 · 「시술 현황 상태 2계층 기본값」 · 「시술 현황 카드 한글 발음」 · 「② 시술 현황 시작 = 문서부터」 · 「웹은 구현본이 정본」 · SPEC-003 OQ-519 닫힘(D-59)
- 지금 계약: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md`(0.5.1) · `10-decision/decision-005-procedure-board.md`(개정하지 않음 — SPEC-003 머리말 우선순위 규칙대로 _RESUME 줄 > DEC-005)
- 예약 현황 쪽 같은 규칙(따라 맞출 원본): `20-spec/spec-005-reservation-board.md` 0.4.0 §5.1(주 상태 · 부상태 · 색 — 구현 값) · 구현 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/front/components/reservations/view.tsx`
- 흐름: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-12-cc-prototype/workflow-v2.md` — 「보류 · 시술 차트」(180행 근처) · 시술 구간
- 코드(읽기만): `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/`(branch `kknaksss/overall-board-2`) — 시술 현황 front `app/(main)/procedures/live/page.tsx` · `components/procedures/**` · back `schemas/board.py`(`phoneticName` 이미 있음) · `kos/sync.py`
- 리뷰 근거(W2): `orchestration/work/overall-board/review-code-r1.md` W2 절

## 2. 이번 판에 넣을 것(계약 — SPEC-003 0.6.0)
1. **상태 2계층**: 카드 = 주 상태 시술(대기 · 진행) / 귀가(대기) · 시술 줄 = 대기 · 진행 · 완료. 이름 · 색 = SPEC-005 §5.1 과 같은 규칙(대기 연한 배경 + 그 색 글자 · 진행 진한 채움 + 흰 글자 · 완료 회색). 지금 SPEC-003 의 `flowStep` · 작업 status 표시 규칙과 대조표(바뀌는 곳 전부 — 카드 · 필터 · 범례 · 시술 줄 · 앱 영향은 §10.1 앱 후속으로)
2. **W2 드래그 놓기**: 판 안 어디에 놓든(카드 사이 틈 · 빈 칸) 끄는 동안 보인 자리로 확정 · 판 밖 · 취소 = 원래 순서(§6.3 · §5.12)
3. **카드 한글 발음**: 이름 오른쪽에 `phoneticName`(KOS 값 그대로 · 없으면 안 그림 · 말줄임 규칙) — 예약 현황 카드와 같은 꼴
4. WORK-008(새): WP 나눔 · 대상 파일 · 완료 조건 · 검증 명령 · E2E 시나리오(사용자 실물 자리)

## 3. 이번 판은 초안만(계약 아님)
- **시술 차트**: workflow-v2 「보류 · 시술 차트」를 흐름 초안으로 — KOS 세 칸(간호관리차트 = `tasks[].assigneeMemo` · 의사차트 = `doctorMemo` · 시술 메모 = `memo`)이 무엇이고 어디서 읽히나(사본에 있나 · 코드 근거) · 쓰기는 공개 API 없음(HAR 필요) · **「정할 것」 목록**: 누가 쓰나 · 어느 화면(카드 · 시술 줄 · 모달 · 앱) · 언제(시술 중 · 완료 뒤 · 귀가 뒤 고치기) · 읽기만 먼저 할지 · 필요한 HAR 목록. **결정하지 마라**
- KOS 소켓 · OQ-528(K5)은 손대지 않는다

## 4. allowed_paths
- `para/projects/summer-star/cc-prototype/{20-spec/spec-003-procedure-board.md, 30-work/work-008-procedure-board-v2.md(새), 20-spec/README.md, 30-work/README.md, log.md}` · SPEC-004 는 frontmatter links 한 줄만
- `reference/2026-10-12-cc-prototype/workflow-v2.md`
- 보고 `orchestration/work/overall-board/procedure-spec-r7-report.md`

## 5. 금지 · 검증
- 코드 수정 금지 · 실명 · KOS id · 키 · 토큰 금지(public) · 열린 것은 OQ 로
- 검증: 위 결정 줄 → 절 대조(빠짐 0) · 2계층 대조표가 코드의 지금 표시 전부를 덮는지 · grep 0

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

- 커밋·push·PR 금지.

```bash
orca orchestration send \
  --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_7c6831e8-ba7a-4731-8eee-50a8bdc3063e \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 / 요약 / 검증 수치 / 정할 것(차트) / 미결"

orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
- 막히면: `orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[질문] planner: <질문>" --enter`
