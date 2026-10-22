# [frontend] procedure/front — WP5 (시술 현황판 화면 · SSE)

너는 **cc-prototype `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/roles/cc-prototype/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/myeongdong-poc-v2` (브랜치 `kknaksss/myeongdong-poc-v2`)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ **backend 워커가 같은 워크트리 `procedure/back/` 에서 WP2 ~ WP4 진행 중 — `procedure/back/` · `procedure/docker-compose.yml` 은 건드리지 마라.** `cc/` 는 읽기만(테마 복사 원천).

## 1. SSOT — 먼저 읽을 것

- **계약**: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md` — 특히 §2.4(테마 복사표) · §5(상태 · 규칙 · **버튼 활성표**) · §6(화면 · 시안≠DEC 표) · §7(API · §7.5 SSE). 여기 없는 건 발명하지 마라
- **WP5 완료 조건**: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/para/projects/summer-star/cc-prototype/30-work/work-003-procedure-board.md` WP5
- **화면 정본(시안)**: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/design-user-r4/Ceramique 시술현황판 v2.dc.html` + 읽기 리포트 `design-r3-read-report.md` · `design-r4-read-report.md`. **SPEC §6 의 「시안≠DEC」 표가 이긴다**(마취 버튼은 진행 중에도 · 수락은 그 호출 시술만 · 되돌리기 없음)
- 코드 대조표(디자인 값의 코드 원천): `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/design-r2-report.md` §1
- 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/para/projects/summer-star/cc-prototype/10-decision/decision-005-procedure-board.md`
- **backend 가 고정한 계약 코드**: `procedure/back/` 의 `schemas/`(스냅샷 · 요청/응답 · SSE 이벤트) · 가짜 스냅샷을 주는 `GET /api/board` · `GET /api/board/stream` — 이걸로 먼저 그린다

**기대는 개념** — 해당 없음.

## 2. 배경

새 기능 `procedure/`(시술 현황판). 기존 `cc/` 화면을 쓰지 않고 새로 만든다. **테마 · medikit · 디자인 시스템은 `cc/front` 에서 복사해 그대로**(기능끼리 import 금지). 목표 = 사용자가 로컬에서 E2E.

## 3. 계약

SPEC-003 §7 그대로 소비. 모양이 맞지 않으면 고치지 말고 코디에게 [질문].

## 4. 먼저 읽을 핵심 파일

- `cc/front` 의 `package.json` · `next.config` · 테마/토큰 · `medikit-patches.css` · `components/common/AppHeader.tsx` · `components/desk/Aside.tsx` · `FloorGrid.tsx` · `RoomPanel.tsx` · `lib/memo.tsx`(MemoCard) — **복사 원천**(SPEC §2.4 표)
- 시안의 `[Button-3]` · `[Badge-1]` patches 블록 — `procedure/front` 의 patches 에 추가

## 5. allowed_paths — 이 밖은 건드리지 마라

- `procedure/front/**`

## 6. 구현 단계

1. 테마 복사 · Next.js 앱 · 로그인(관리자 1개) · 헤더(「시술 현황」 하나) · 사이드바
2. 카드(§6.3) · 오른쪽 패널 3탭(§6.4) · 의사 호출 팝오버(§6.5) — **버튼 활성은 SPEC §5 활성표 그대로**(서버 스냅샷 값을 쓰고, front 에서 규칙을 다시 만들지 마라 — 스냅샷에 없으면 [질문])
3. SSE 연결(§7.5 — 첫 스냅샷 · 재연결 · version 순서) · 조작 API 호출 · 토스트(되돌리기 없음)
4. 가짜 스냅샷으로 시안 장면 8개가 화면에 나오는지 확인 → back WP2 이후 실제 back 으로 붙여 확인
5. `procedure/front/Dockerfile` 이 필요하면 SPEC §2 대로(compose 는 backend 몫 — front 서비스 항목이 필요하면 [질문])

## 7. 범위 제약 — 하지 말 것

- `procedure/front` 밖 import · 수정, `cc/` 수정
- 시안에 없는 화면 요소 발명 · 규칙을 front 에서 따로 계산
- 키 · 실명 · 연락처 값(public)
- 사용자 포트(3600 · 8600 · 3700 · 8700)에 떠 있는 사용자 프로세스를 죽이지 마라 — 네가 띄운 것만 정리
- 커밋 · push · PR 금지

## 8. 검증

```
단계마다 방금 만든 부분만 확인(tsc · 해당 화면). 통합 검증(npx tsc --noEmit · npm run lint · npm run build · 브라우저 전체 확인)은 **마지막에 한 번만**. procedure 밖 import 없음 확인. 브라우저로 로그인 → 카드 · 패널 · 팝오버 · SSE 갱신을 눈으로(스크린샷 경로를 보고에). 실행 못 한 검증은 사유와 함께 pending
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
