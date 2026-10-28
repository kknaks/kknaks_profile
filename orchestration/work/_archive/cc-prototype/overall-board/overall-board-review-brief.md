# [reviewer] WORK-005 코드 검수 — 전체현황판 시술 현황(BE1 · BE2 · FE1 · FE2)

너는 **cc-prototype `reviewer` 워커**다. **앞 판의 맥락이 없다.** 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` (**read-only** — 커밋 안 된 변경이 검수 대상: `git -C /Users/kknaks/orca/workspaces/cc-prototype/overall-board diff` · `git status`)

## 1. SSOT — 대조 기준

- 계약 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md` **0.4.2** (부록 E · F · G 포함) · `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md` 0.3.1 §3.4
- 빌드 계획 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/30-work/work-005-overall-board-procedure.md` (WP 별 완료 조건)
- 시안(정본) `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/design/Ceramique 전체현황판.dc.html` — 헤더 `M:63-92` · 제목 줄 `M:781-800` · 카드 `M:808-905` · 패널 `M:914-1086` · 드래그 `M:1464-1475`
- 워커 보고 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/backend-r1-report.md` · `frontend-r1-report.md` · 스크린샷 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/fe-shots/`(11장)
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/_RESUME.md` §2 2026-10-23 줄

## 2. 검수 대상

backend(16파일 + `tests/test_order.py` · CORS `PUT` 추가 · 기존 시험 2개 수정) · frontend(7파일).

## 3. 계약

해당 없음 (검수).

## 4. 먼저 볼 곳

`procedure/back/app/domain/rules.py` (`is_room_task`) · `service/` 순서 저장 · `api/` PUT · `board_service` 정렬 · `procedure/front/components/procedures/{OrderCard.tsx,view.ts,Aside.tsx}` · `app/(main)/procedures/live/page.tsx` 드래그 · 경합

## 5. allowed_paths

- 산출물 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/review-code-r1.md`. 코드 수정 금지. 시험 · 빌드 실행은 해도 된다(사용자 포트 금지 · 띄운 것은 내려라).

## 6. 할 일 — 각 지적에 `파일:줄` + 근거(SPEC 절 · 결정 줄) + 판정

1. SPEC-003 0.4.2 부록 E 의 절 전부 · §6.7 #11 ~ #22 가 코드에 맞게 들어갔나. OQ 기본값(OQ-520 ~ 525 · 514)이 코드에 그대로인가.
2. **사용자 핵심 결정 확인**: 「방 배정」만 빠지고 **방 없는 기타 작업(마취 · 시트팩 · 관리 마무리)은 남는다** — back 판정 · 시험 · 가짜 보드 · front 표시. 귀가 대기 취소 · 방 계산 · 앱 부작용 0.
3. 드래그 계약: 저장 · 거르기 · StrictInt · 마지막 쓰기 · SSE · KST 날짜 경계 · 방향 따라 놓기(시작 순서 기준) · 경합 ① ~ ④ · 귀가 대기 제외 · 필터로 숨긴 카드 포함 전체 순서.
4. 시안 대조: 스크린샷 11장과 시안 같은 장면. 다른 곳은 §6.7 표에 있는 차이인지.
5. 기능 독립(`procedure/` 밖 import 0) · public(실명 · KOS id · 키 0 — 시안 공지 실명이 들어가지 않았나) · CORS `PUT` 범위.
6. **조용히 통과하는 자리** — 시험은 초록인데 실물에서 어긋날 곳. 그리고 **「사용자가 실물에서 만날 자리」**를 따로 모아라(코디 E2E 체크리스트로 쓴다).

## 7. 범위 제약

- 수정 금지. 결정을 대신 내리지 마라 — 「사용자 결정 필요」로 따로.
- 예약 · 원내 현황 · 앱은 범위 밖.
- `npm run build` 첫 실행 실패는 기존 flaky(`flaky-baseline-evidence.md`) — 인용만.

## 8. 검증

```
각 지적에 파일:줄 + 근거(SPEC 절 · DEC D-번호). 판정 FAIL · WARN · PASS. 기능 독립 위반은 FAIL. 「조용히 통과하는 자리」를 따로 본다
```

- 리포트 맨 위 종합 판정과 FAIL · WARN 개수. FAIL 은 BE / FE 어느 워커 몫인지 표시.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 --from term_d5bb55fc-68e8-422a-86aa-a8710c7285ba \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
