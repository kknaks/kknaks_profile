
# [mobile] 프로토타입 시술현황 탭 읽기 전용 조사

너는 **day `mobile` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/mobile/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck`
base 브랜치: `조사 전용 · 현 워크트리` → 최종 PR 대상 `없음 · 구현과 PR 금지` (PR 은 코디네이터가 올린다)

같은 워크트리에 다른 세션의 day-procedure-board-2 기록이 있다. 해당 파일은 절대 수정하지 마라. 너는 이전 대화 맥락이 없다. 아래 근거로만 조사한다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/para/projects/company/day/log/2026-11-09-day-data-architecture.md` ← 계약의 SoT. **여기 없는 건 발명하지 마라.**
- `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/app/README.md · /Users/kknaks/git/CENTURION_DAY/AGENTS.md · /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/reference/2026-11-03-cc-day/screen/procedure-board-decisions.md · /Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec/products/day/40-architecture/mobile-deployment.md`

**기대는 개념** — 이 작업이 따를 판단 기준. 안 주면 워커가 매번 처음부터 정하고,
같은 결정이 작업마다 달라진다. 없으면 "해당 없음".

- `해당 없음` — 코드에 구현된 사실과 DAY에 대한 제안·미결을 구분한다.

## 2. 배경 / 무엇을 바꾸나

사용자는 DAY 앱의 첫 기능으로 시술현황 탭을 정했다. 기존 cc-prototype은 프로토타입이므로 로그인 방식·컬러·브랜딩은 DAY 기준으로 가야 한다. 지금은 구현 전 조사다. 기존 앱의 시술현황 화면·룸 상세·연결 동작을 읽어 무엇이 있는지 보고하라. 기능 채택·제외는 사용자가 결정한다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

새 계약을 만들지 않는다. 프로토타입 API 경로는 참고용이며 DAY API와 같다고 가정하지 않는다. DAY backend/ 수정 금지. 방 이동·차트 등 새 API는 별도 day-procedure-board-2 세션 소유다. 시작 취소 버튼은 유지하고 KOS에 쓰지 않는 결정은 DAY 백엔드에서 처리한다.

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/app/lib/ 아래 screens/board_screen.dart · room_screen.dart · shell.dart · login_screen.dart, widgets/call_sheet.dart · accept.dart · undo_sheet.dart · interpret_bar.dart · interpret_drawer.dart, view/view.dart, api/api.dart, sse/board_stream.dart, theme/tokens.dart` — 화면과 실제 호출 경로를 대조한다. 관련 파일은 추가로 읽어도 된다.

## 5. allowed_paths — 이 밖은 건드리지 마라

- /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/research-prototype-board.md 한 파일만 작성 가능. 조사 대상 레포와 그 밖의 모든 파일은 읽기 전용.

## 6. 구현 단계

1. 프로토타입 시술현황 탭을 코드로 조사한다. 보고서에는 ①화면 진입·폰/태블릿 구성 ②목록 카드 정보·필터·정렬·타이머 ③룸 상세 정보와 모든 조작 ④의사 호출·수락·재호출·되돌리기 ⑤실시간 갱신·푸시·통역 등 연결 기능 ⑥로그인·컬러·브랜딩을 DAY로 바꿀 부분 ⑦방 이동·차트 등 조사 범위에서 발견되지 않은 기능 ⑧기능 범위 논의를 위한 목록을 담는다. 각 사실에 파일:줄 근거를 붙인다. 화면에서 노출되는 기능과 모델/API만 있는 기능을 구분한다. 실제 실행 검증 여부를 명시한다.

## 7. 범위 제약 — 하지 말 것

- 앱 구현·의존성 설치·서버 실행·서명·배포·외부 API 호출 금지.
- 조사 대상 레포 수정, 기능 범위 확정, 화면 문구 창작 금지.
- 보고서 외 파일 수정·커밋·push·PR 금지.

## 8. 검증

```
읽은 코드의 화면 → 위젯 → API 연결을 대조한다. flutter 실행·서버 실행·기기 조작·외부 API 호출 없이 정적 조사만. 보고서의 핵심 사실마다 파일:줄 근거를 남긴다.
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
  --to term_781a6b8f-68da-447e-acb9-c2261321c190 --from term_0de3d2e6-b0f7-40f9-8295-7c24c42b0c5c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "mobile 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
