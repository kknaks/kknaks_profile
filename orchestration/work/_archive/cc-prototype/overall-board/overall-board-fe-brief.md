# [frontend] WORK-005 WP-FE1 · WP-FE2 — 헤더 · 틀 · 패널 · 카드 · 드래그

너는 **cc-prototype `frontend` 워커**다. **앞 판의 맥락이 없다** — 이 브리프와 아래 파일만 믿어라. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 레포 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/README.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` (branch `kknaksss/overall-board`, base `origin/main`)

⚠ 같은 워크트리에서 **backend 워커가 `procedure/back/` 를 병렬로** 고친다 — `procedure/back/` 는 건드리지 마라. back 을 기다리지 말고 가짜 보드(`PROC_FAKE_BOARD`)로 그린다 — 가짜 보드에서 `PUT` 은 403 이 맞는 동작이다(WORK-005).

## 1. SSOT — 먼저 읽을 것

- **빌드 계획** `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/30-work/work-005-overall-board-procedure.md` — 네 WP 행 · 「계약 고정점」 · 「주의」 · 「하지 않는 것」 전부
- **계약** `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md` **0.4.2** — WORK 의 「Covers spec」 절. 여기 없는 건 발명하지 마라
- 역할 검사표 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md` §3.4
- 시안(정본) `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/design/Ceramique 전체현황판.dc.html` · 분석 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/design-analysis-report.md` · 현재 코드 인벤토리 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/current-board-report.md`
- 문서는 **코디 워크트리 절대경로를 read-only 로** 읽는다(네 워크트리 base 엔 새 문서가 없다)

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 바꾸나

배포된 시술 현황판을 「Ceramique 전체현황판」 시안의 「현황 › 시술 현황」으로 바꾼다. **시안이 정본**이고, 사용자 결정(헤더 「현황」 하나 · 「방 배정」 줄만 제거(마취 · 시트팩 등 다른 기타 작업은 남김) · 입실순/배치순 제거 · KOS 반영 표시 제거 · 드래그 순서 back DB 저장)이 SPEC-003 0.4.2 에 들어가 있다. 너의 몫 = **WORK-005 WP-FE1 · WP-FE2**.

## 3. 계약

WORK-005 「계약 고정점」 표 그대로(`PUT /api/board/order` · 스냅샷 `cards[]` 배열 순서 · 「방 배정」 없는 `procedures[]` · SSE). 모양을 바꿔야 하면 **고치지 말고** §9 질문 채널로 물어라.

## 4. 먼저 읽을 핵심 파일

WORK-005 WP-FE1 · WP-FE2 행의 「대상 파일」 열.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `procedure/front/` (WORK-005 WP-FE1 · WP-FE2 대상 파일)

## 6. 구현 단계

1. WP-FE1 헤더 · 틀 · 제목 줄 · 패널 → 그 WP 검증 명령 + grep 기대값
2. WP-FE2 카드 · 드래그(방향 따라 놓기 · §5.12 「놓은 뒤 화면」 경합 규칙) → 그 WP 검증 명령
3. 스크린샷: WORK-005 FE1 · FE2 완료 조건의 장면들을 가짜 보드로 찍어 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/fe-shots/` 에 저장하고 리포트에 경로를 적는다. 가짜 보드 back 을 띄워야 하면 **사용자 포트를 피한 임시 포트**로 띄우고 끝나면 반드시 내린다

## 6.1 문서 검수 r3 참고(구현 때 반영)

- 고객 탭 줄 순서 = 카드 순서(경합 중엔 로컬 순서) — 로컬 순서를 `live/page.tsx` 에서 `Aside` 로 넘겨야 한다
- WP-FE1 grep `\bMenu\b` = 0 을 위해 `live/page.tsx:3` 주석의 「Menu」도 지운다
- WORK-005 머리 문단(W:38)의 「0.4.0」은 낡은 표기 — 계약은 **0.4.2**

## 7. 범위 제약 — 하지 말 것

- WORK-005 「하지 않는 것」 전부(예약 · 원내 현황 · 앱 · KOS 쓰기 · 경로 변경 · 열린 OQ).
- public 레포: 실명 · KOS id · 키 · 토큰 0. **시안 공지 예시의 실명을 코드 · 가짜 보드 · 시험에 옮기지 마라.**
- 사용자 포트(3600 · 8600 · 3700 · 8700)와 사용자 프로세스를 건드리지 마라. 커밋 · push 금지.

## 8. 검증

```
<기능>/front 에서 npx tsc --noEmit · npm run lint · npm run build — 각 1회. 기능 폴더 밖 import 가 없는지 확인. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending 으로 보고
```

- WP 마다 WORK-005 「검증 명령(부분)」을 1회씩. 통과하면 반복하지 마라.
- 완료 보고 본문에 WP 별 완료 조건 ①②… 각각의 결과(통과 · 수치)를 적는다. 실행 못 한 것은 사유와 함께 pending.
- 결과 리포트를 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/frontend-r1-report.md` 에 남긴다(이 파일은 코디 워크트리 — 리포트 1개만 예외로 허용).

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 --from term_295e88c1-2bea-440e-af22-21c4f28d47b9 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
