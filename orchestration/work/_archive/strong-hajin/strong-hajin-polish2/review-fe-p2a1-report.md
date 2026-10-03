# 리뷰 리포트 — strong-hajin-polish2 / frontend · WORK-009 Phase 2a-1 (2026-10-02)

## 판정: WARN

계약대로 돈다. 창 「저장」(파랑), save_draft 만 보냄, 저장 뒤 새 회차, 등록이 새 base, 실패는 창 안만(fix0), 범용 렌더러 제외 5자리, 다른 CreateWorkModal 자리 불변 — 모두 코드와 서버 계약으로 확인했다.
FAIL 은 없다. 다만 **낡음·중간 닫기 경로에 사용자가 실물에서 만날 수 있는 구멍 3개**가 있다(W-1~W-3). 그중 W-1 은 SPEC-002 §6 체크 문장과 어긋나므로, 코디가 이번 판에서 고칠지 정해야 한다.

## 검수 범위
- diff: `git diff -- frontend`(HEAD `d1bb87d` 기준, 미커밋) 13 파일 + untracked `frontend/src/features/action/AxDraftSave.test.tsx` 1개. `backend/` 미커밋(Phase 1)은 계약 대조용으로 읽기만 했다.
- allowed_paths: 변경이 전부 `frontend/src/` 안이다 → 이탈 없음.
- 실행한 검사(직렬):
  - `npx vitest run --no-file-parallelism src/features/action/AxDraftSave.test.tsx src/features/action/AxDraftCard.test.tsx` → 39/39 통과
  - `npx vitest run --no-file-parallelism src/App.test.tsx -t "AX 초안 저장 실패"` → 1/1 통과
  - `npx tsc --noEmit -p .` → 0
  - grep 재계수(아래 §재계수). 서버·브라우저는 띄우지 않았다.

## 위반 (FAIL 사유)
없음.

## 경미 (WARN)

### W-1 — 낡은 저장이 거부된 뒤 FE 가 최신 회차를 다시 읽지 않는다 (SPEC-002 §6 체크와 어긋남)
- 근거:
  - SPEC-002 §4 「초안 저장」 표의 「낡은 저장」 줄: 「거부되고 최신 회차를 다시 읽는다」
  - §6 체크 `spec-002…md:687`: 「지난 회차를 기준으로 한 저장이 **거부**되고 최신 회차를 다시 읽는다」
  - §5 Case Matrix `ACTION_VERSION_STALE`(`:529`): 「지금 값으로 다시 불러오되 내가 쓰던 입력은 남긴다」
- 코드:
  - 채팅 경로 `src/App.tsx:361-367` — 실패하면 `throw` 만 하고, `refreshProjections()`(`:369`)는 성공 때만 돈다.
  - 홈·칩 경로 `src/features/action/AxDraftCard.tsx:517` — 실패하면 `onDone` 없이 throw 한다.
  - 두 경로 모두 창은 옛 `base_submission_version` 을 쥔 채 남는다.
- 실물 시나리오: 같은 초안을 홈 「AX 제안」에서 저장(→2회차)한 뒤 채팅 카드 [수정]→[저장]을 누른다.
  - 422 「base submission version is stale」가 창 안에 선다.
  - 다시 저장해도 같은 오류다. 카드 [등록]도 같은 낡음으로 거절된다.
  - 채팅은 턴이 진행 중일 때만 폴링하므로, 대화를 다시 열기 전까지 빠져나갈 길이 없다.
- 참작:
  - WP 2a-1 체크박스는 「충돌이면 지금 confirm 충돌과 같은 문구」까지만 요구한다.
  - 기존 confirm 낡음도 다시 읽지 않는다(기존 부채). 워커는 WP·발주서대로 했다 → FAIL 이 아니라 WARN.
- 권장 수정: 저장 실패가 422 낡음 문장이면 채팅은 `refreshProjections()`, 창은 `onDone()` 을 부른다. 입력은 그대로 둔다.
  - 카드의 새 `contract` 로 창의 `onSubmit` 클로저가 새 base 를 집는다(`AxDraftCard.tsx:432`). 그러면 다시 「저장」이 통과한다.

### W-2 — 저장 진행 중 창을 ×·Esc·바깥 클릭으로 닫으면, 카드 「등록」이 옛 회차로 열려 있고 저장 실패는 어디에도 안 선다
- 코드:
  - 창 「닫기」 단추만 `disabled={isWorking}` 이다(`src/features/work/WorkModals.tsx:5262`).
  - DS `Modal` 의 × · Esc · 바깥 클릭(`src/ds/Modal.tsx:157,162,180`)은 막히지 않는다. 그러면 `onClose={() => setEditing(false)}`(`AxDraftCard.tsx:453`)가 창을 내린다.
  - 저장은 창 안의 `submit` 이 돌리고 카드의 `busy` 를 세우지 않는다. 그래서 카드 「등록」(`AxDraftCard.tsx:408-411`)이 그 사이 눌린다.
- 실물 시나리오: 저장 중 Esc → 바로 [등록]. 두 경우 중 하나다.
  - 저장이 먼저 커밋되면 confirm 이 base 2(옛) → 422 낡음이다.
  - confirm 이 먼저 락을 잡으면 **고치기 전 값으로 업무가 생기고**, 저장은 실패한다.
- 실패가 숨는 문제: 저장 실패는 `onError` → `setEditError`(카드 state)로만 간다. 창이 없으니 보이지 않는다.
  - fix0 로 전역 띠도 끊었다(`App.tsx:365`). 홈·칩 경로도 전역에 알리지 않는다(`AxDraftCard.tsx:517-519`). 결과적으로 **아무 데도 안 선다.**
- 참작: × · Esc 를 막지 않는 것은 CreateWorkModal 공통의 기존 동작이다. 다만 「생성」은 끝나는 동작이고, 「저장」은 카드가 계속 명령을 받는 동작이라 이번 판에서 새로 생긴 경합이다.
- 권장 수정(택1):
  - 저장 중에는 창 닫기를 막는다(`onClose` 를 `isWorking` 일 때 무시).
  - 또는 AxDraftCard 가 저장 중 `busy` 를 세운다(onSubmit 을 `send` 와 같은 busy 로 감싼다).

### W-3 — 저장 성공 뒤 갱신이 실패하면, 화면이 「저장 실패」처럼 또는 「옛 회차」로 남는다
- 홈 「AX 제안」 칩(MyWorkPage):
  - `onDone = reload()+onDecided()`(`src/features/work/MyWorkPage.tsx:1349-1352`). `reload` 는 `getMyWork()` 실패 시 throw 한다(`:312-313`).
  - 그러면 `AxDraftCard.tsx:522` 의 `await onDone()` 이 throw 한다. 저장은 됐는데 창 안에 오류가 서고 창이 남는다.
  - 다시 저장하면 새 base(3)·같은 값이라 서버가 「변경 없음 200」을 돌려준다. 회복은 되지만 문구가 틀린다.
- 채팅:
  - `refreshProjections` 가 실패해도 토스트는 「AX 초안을 저장했습니다.」다(`src/App.tsx:369-372`). `staleProjection` 띠는 함께 선다.
  - 카드는 옛 회차 그대로라 [등록]이 422 낡음이다. W-1 과 같은 막힘이다.
- 권장: W-1 을 고치면 채팅 쪽은 같이 풀린다. 칩 쪽은 저장 분기에서 `onDone` 실패를 저장 실패와 분리한다(`try { await onDone() } catch {}` 후 notice).

### W-4 — 테스트가 실제 배선을 지나지 않는 자리 (조용히 통과하는 자리)
- `AxDraftSave.test.tsx:148` 「채팅 카드: 다시 읽어 온 새 회차」:
  - `rerender` 로 새 source 를 손으로 건넨다. 실제 경로(MessageList → `decideConversationAction` → `refreshProjections` → `refreshActiveConversation` → 카드 갱신)를 지나지 않는다.
  - 「저장 뒤 대화 재조회」를 단언하는 App 수준 테스트는 실패 경로(App.test fix0) 하나뿐이고, 성공 경로는 없다.
  - 대화 재조회의 `next.version >= current.version` 병합(`useConversations.ts:172`)은 저장이 대화 version 을 올리지 않아도 `>=` 라 통과한다. 이건 읽어서만 확인했다.
- `AxDraftSave.test.tsx:161` AxDraftModal:
  - 「부모가 옛 item 을 다시 내려도 높은 회차를 유지 / 더 높은 item 이 오면 따른다」(`AxDraftCard.tsx:509`)를 rerender 로 단언하지 않는다. 규칙 자체는 코드로 맞다(§확인 2).
- 모킹 모양은 서버 계약과 맞다. 저장 응답 봉투가 `submission_version` 3, `edit_contract.base_submission_version` 3, `expected_version` 5(그대로)이고, 서버 계약 테스트 `backend/tests/contract/test_action_center.py:1730-1735` 와 같은 모양이다.
- 빈 단언은 없다. `decideAction` 테스트의 응답 `{}` 는 반환값을 쓰지 않는 경로라 무해하다.

## 기존 부채 (이번 판정 제외)
- confirm 낡음 422 뒤에도 FE 가 다시 읽지 않는다(`App.tsx:361-367`, `AxDraftCard.tsx send`). SPEC §5 Case Matrix 「다시 불러오되 입력은 남긴다」와 어긋난다. W-1 은 이 부채가 저장으로 번진 것이다.
- 낡음 오류가 영문 서버 문장 그대로 선다(fix0 ② 로 범위 밖 확정). SPEC Case Matrix 409 와 서버 422 의 차이는 Phase 1 보고에 남아 있다.
- CreateWorkModal 의 DS Modal × · Esc · 바깥 클릭이 `isWorking` 중에도 열려 있다(만들기 경로 공통).

## 확인한 것 (PASS 근거)

1. **계약 충실도**
   - 창 주 단추:
     - `WorkModals.tsx:5268` `axDraft ? (isWorking ? axDraftCard.saving : axDraftCard.save)`. 문구는 `labels.ts` 「저장」/「저장 중…」이다.
     - `variant="solid" tone="primary"` 그대로이고 body 포털이라 DS 파랑이다. 「닫기」(`:5262`)는 그대로다.
     - 테스트 `AxDraftSave.test.tsx` 첫 케이스가 `scax-button--solid-primary` 를 단언한다.
   - save_draft 만 보낸다:
     - `AxDraftCard.tsx:432` 가 `onCommand(save.id, …)` 를 부른다. confirm 호출이 없다(테스트가 confirm 미호출을 단언).
     - 채팅 `api.ts:738` `decideAction` 이 save_draft 를 `runActionCommand` → `POST /api/action-items/{id}/commands/save_draft` 로 보낸다(서버 `http.py:2278` 과 일치).
   - 입력 모양 `{expected_version, base_submission_version, draft, attachment_draft_ids?}`:
     - `confirmPayload`(`AxDraftCard.tsx:282-286`)와 `expected_version` 주입(채팅 `api.ts:739` = `action.version`, 창 `AxDraftCard.tsx:517` = `current.expected_version`)이 맞다.
     - 서버 `normalize`(`action_center.py:583-605`)가 같은 키를 읽는다.
   - 저장 뒤 새 회차:
     - 채팅: `decideConversationAction` 이 성공 뒤 `refreshProjections`(`App.tsx:369`) → 대화 재조회를 한다. 카드는 `key` 가 같아 같은 인스턴스이고 `source.contract` 새 값으로 다시 그린다. 회차는 `axDraftFromAction` 의 `round = edit_contract.base_submission_version`(`AxDraftCard.tsx:73`)이다.
     - 홈·칩: `setCurrent(answered)`(`:521`) + `onDone`(목록 재조회) + 「AX 초안을 저장했습니다.」를 낸다. 창(카드 창)은 남는다.
     - 서버 응답이 `edit_contract`·`material_drafts`·`created_at` 을 싣는다. `ActionEnvelopeResult` TypedDict(`results.py:21-46`)에 다 있고, `ActionEditContract.save_command` 도 선언돼 있다(`result_contracts.py:77`).
   - 실패는 창 안만:
     - `WorkModals.tsx:4894` `onError` → `axDraft.error` 가 창 안에 선다.
     - fix0 `App.tsx:365` 가 save_draft 실패일 때 `setError` 를 하지 않는다. confirm·reject 는 그대로다.
     - 홈·칩 경로도 전역 `onError` 를 부르지 않는다. App.test 신규 1건이 확인한다.
   - 입력 유지: 창이 throw 를 받아 열린 채 남는다(`AxDraftCard.tsx:432-433` — 실패 시 `setEditing(false)` 에 닿지 않는다). 테스트가 단언한다.
   - 등록이 새 base:
     - 카드 「등록」 = `confirmPayload()`(draft 없음)이다. `contract.base_submission_version` 은 렌더 때의 source 에서 읽으므로 저장 뒤 새 회차다.
     - 서버는 저장 뒤 draft 없는 confirm 을 받는다(Phase 1 계약).
   - expected_version: 서버 계약상 저장으로 오르지 않는다(`test_action_center.py:1733`). FE 는 채팅에서 재조회한 `action.version`, 창에서는 저장 응답의 `expected_version` 을 쓴다. 어느 쪽이든 같은 값이라 맞다.
   - 자료 `attachment_draft_ids`:
     - 창 `onSubmit(draft, staged)` → `confirmPayload(draft, attachmentIds)` 로 싣는다.
     - 서버 `_save_draft` 는 claim 검증만 하고 소비하지 않는다(`action_center.py:1031-1035`). 그래서 drafts 가 staged 로 남는다.
     - 카드 「등록」의 기본 인자 `staged` 가 다시 싣는다. 회차 갱신 때 `materials` 는 `useEffect([source.materials])` 로 재동기화된다.
   - [수정]은 save 명령이 있을 때만 선다: `editable = pending && Boolean(save) && 편집 칸`(`AxDraftCard.tsx:261`). save 탐색은 `contract.save_command ?? "save_draft"` 로 하고, 봉투 명령 목록에서 찾는다. 테스트가 단언한다.
2. **낡음 경합**
   - 채팅에서 재조회 전 등록:
     - 창은 `await onCommand` 가 `refreshProjections` 까지 기다린 뒤 닫힌다(`App.tsx:369` 가 `decideConversationAction` 안). 그래서 정상 경로에서는 창이 열린 동안 카드 「등록」을 누를 수 없다.
     - 예외는 W-2(× · Esc 로 중간 닫기)와 W-3(재조회 실패)다.
   - 홈·칩 「더 높은 회차를 따른다」(`AxDraftCard.tsx:509`):
     - `useEffect([item])` 이므로 부모가 **새 객체**를 내릴 때만 비교한다.
     - 두 부모(`TodayPage.tsx:434-441` `selectedActionItem`, `MyWorkPage.tsx:1343-1353` `openAxDraft`)는 연 순간의 봉투를 state 로 쥔다. 목록 재조회 뒤에도 같은 객체라 effect 가 돌지 않고 `current` = 저장 응답이 유지된다.
     - 옛 회차 객체가 새로 와도 `<` 라 무시하고, 같거나 높으면 따른다. 맞다.
     - `key={action_item_id}` 라 다른 항목으로 바뀌면 state 가 초기화된다.
   - expected_version 불변 계약과 FE 가 맞다(위 1).
3. **범용 렌더러 제외 — 재계수 5/5**
   - grep 대상: `allowed_commands|\.commands\b|map((command`. 단추로 map 하는 자리는 다섯이고, 다섯 다 `withoutEditorOnlyCommands` 를 거친다.
     - ① `ActionPreview.tsx:66-70` `ActionCommandButtons`(MessageList:659 결과 카드)
     - ② `ActionCenter.tsx:419,455` 상세 footer
     - ③ `CommandConfirmationForm.tsx:125`
     - ④ `ActionTaskCard.tsx:570`
     - ⑤ `ActionMeetingCard.tsx:346`
   - 나머지는 단추를 그리지 않는다:
     - `find` 만 쓰는 자리: AxDraftCard:254-258 · ActionProgressBatchCard:47-48 · ActionTaskCard:322 · ActionMeetingCard:130
     - `assistantPresentation.ts:40` 은 개수만 센다.
     - `WorkModals.tsx:1131` 은 `accept` 존재만 본다.
   - 빠진 자리 없음.
4. **다른 CreateWorkModal 자리 불변 — 재계수 6 호출**
   - CalendarPage:683 · TodayPage:468 · WorkModals:3019(하위 업무) · AxDraftCard:420 · MyWorkPage:1423(새 업무·재요청 두 모드 = 조사 §2-4 의 7자리) · MeetingDetailPage:1289
   - `axDraft=` 는 AxDraftCard:422 한 곳뿐이다. 나머지 단추 문구(업무 추가 / 업무 요청 보내기 / 만드는 중…)와 제출 갈래는 바뀌지 않았다(`WorkModals.tsx:5268` 삼항의 else 갈래 그대로).
   - 테스트 `AxDraftSave.test.tsx` 마지막 케이스가 새 업무·재요청 문구를 단언한다.
5. **frontend 규율**
   - `api.ts` 밖 fetch 없음.
   - kind·status 로 명령을 추론하지 않는다(save 는 `edit_contract.save_command` 와 봉투 명령으로 찾는다).
   - 새 한국어 문구는 `labels.ts` `axDraftCard.save/saving/saved/saveFailed` 에 있다.
   - hex 리터럴 추가 없음.
   - 옆자리 테스트: `AxDraftSave.test.tsx` 신규, `AxDraftCard.test.tsx` 갱신.
6. **확인 안 함**: 전체 직렬 스위트·`make frontend-build` 는 돌리지 않았다(워커 보고: 5 실패 기준선 / build 성공). 실물 화면도 보지 않았다(브라우저 금지).

## 사용자가 실물에서 만날 자리 (코디 화면 확인 목록)
1. 채팅 AX 초안 [수정] → 창 하단 「저장」(파랑)·「저장 중…」 → 창 닫힘 → 카드 머리 「초안 · 2회차」·고친 제목 → [거절][수정][등록] 그대로 → [등록] → 업무가 고친 값으로 생성
2. 홈 판단 대기 / 내 업무 「AX 제안 N」 칩 카드 창 → [수정] → 저장 → 카드 창은 남고 2회차 → 목록 줄도 새 제목 → [등록] → 창 닫힘
3. 수정 창에서 링크·파일을 붙이고 저장 → 카드 자료 요약에 남음 → [등록] 뒤 업무에 자료가 붙었는지
4. 아무것도 고치지 않고 저장 → 회차가 오르지 않음(1회차 그대로)
5. **(W-1)** 같은 초안을 칩에서 저장한 뒤 채팅 카드에서 [수정]→[저장] → 창 안 영문 「base submission version is stale」, 재시도해도 같음, [등록]도 낡음 → 채팅을 닫았다 열어야 풀림
6. **(W-2)** 「저장 중…」 동안 Esc 또는 × → 카드 [등록]이 눌림. 저장 실패가 났다면 어디에도 문구가 없음
7. 저장 실패 시 전역 빨간 띠가 서지 않고 창 안에만 문구가 서는지(fix0). confirm 실패는 여전히 띠에 서는지
8. 채팅 결과 카드·판단 상세(ActionItemDrawer)에 「저장」 단추가 따로 서지 않는지
