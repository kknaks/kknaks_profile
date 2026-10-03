# 리뷰 리포트 — strong-hajin-polish2 / frontend · WORK-009 Phase 2a-2 (2026-10-02)

## 판정: WARN

명시도를 다시 계산했다. 채팅 서랍 안의 DS 단추 네 종류(solid-primary · solid-danger · outlined-neutral · text-neutral)가 **진행 중·비활성 상태에서 포인터가 위에 있어도 파랑이 되는 경로는 0**이다. 덮어쓰기는 전부 `.scax-drawer--chat` 스코프라 서랍 밖으로 새지 않는다. 활성 상태 규칙은 건드리지 않았다. 남은 것은 경미 2건이다 — 서랍 안 사람 행동인데 파랑으로 남은 자리 하나(`ActionPreview` 의 펼치기 `summary`), 그리고 워커 보고 중 사실과 다른 한 줄.

## 검수 범위

- 대상: `frontend/` 미커밋 — `frontend/src/styles/ax.css`(+14/−1) · 새 `frontend/src/features/chat/ChatButtonStates.test.tsx`. Phase 2b(`c64cddf`)·`backend/` 는 보지 않았다
- allowed_paths: 이탈 0
- 기준: WP `work-009-polish2.md` 2a-2 · SPEC-002 v0.4.0 §2.9 「채팅 서랍 안의 색」·§6 · 발주서 `strong-hajin-polish2-fe-p2a-brief.md` · `fe-survey-report.md` §3 · 코디 판단(`.scax-md__ref` · 추천 칩 opacity · 명령 폼 네이티브 button 은 그대로)
- 실행한 검사
  - `components.css:6-27`·`:273-274`·`:408-416` 와 `ax.css:540-546`·`:665-685` 의 규칙을 명시도·순서로 대조
  - 채팅 서랍이 그리는 컴포넌트(ChatDrawer → MessageList · Composer · AxDraftCard · ActionTaskCard · ActionMeetingCard · ActionProgressBatchCard · CommandConfirmationForm · ActionPreview)의 `<Button>` variant·tone 을 전수로 셌다
  - `ax.css` 의 `accent` 사용처 전수 · 포털(`createPortal`) 대상 · `.scax-sources__more` 사용처
  - 테스트 `npx vitest run --no-file-parallelism src/features/chat/ChatButtonStates.test.tsx src/ds/HoverContrast.test.tsx` → **17/17 통과**

## 위반 (FAIL 사유)

- 없음

## 경미 (WARN)

- **W1 `frontend/src/styles/ax.css:297` · `frontend/src/features/action/ActionPreview.tsx:29`** — `.scax-preview>summary`(`<details>` 의 펼치기 머리)가 **`accent` 파랑 글자**다. 채팅 서랍 안에서 그려진다(`MessageList.tsx:299`·`:649` 가 `ActionPreviewDetails` 를 낸다). 사람이 눌러 펼치고 접는 행동이라 SPEC-002 §2.9 「범위 — 채팅 서랍 안의 사람 행동 단추 전부」에 든다. 조사표(`fe-survey §3-2`)에도, 워커 보고에도, 코디 판단 목록(`.scax-md__ref` · 추천 칩 · 명령 폼 네이티브 button)에도 없다 — **전수에서 빠진 자리**다
  - 근거: SPEC-002 §2.9 「원칙 — 파랑은 AI 가 진행 중이라는 표시에만」 · WP P-4
  - 권장: `.scax-drawer--chat .scax-preview>summary{color:var(--scax-color-ink-neutral)}` 처럼 서랍 스코프로 잉크 계열을 준다. AI 내용의 일부(근거 링크와 같은 결)로 본다면 코디 판단 목록에 올린다
- **W2 워커 보고 「ds/Modal 이 포털이 아니라 카드에서 띄운 창(거절 사유·**첨부 고르기**)에도 서랍 규칙이 닿음」** — 「첨부 고르기」는 사실과 다르다. `ActionTaskCard.tsx:754-784` 가 `AttachmentPickerModal` 을 `createPortal(…, document.body)` 로 띄운다. 그래서 서랍 규칙이 **닿지 않고** 앱 DS 로 선다. 결과 자체는 SPEC(「서랍 밖의 창은 앱 DS」)과 맞아 동작 결함은 아니다. 다만 그 창의 「업로드」 글자(`ax.css:526`, `accent`)·선택된 탭(`:494`)이 파랑인 것을 서랍 안 문제로 착각하지 않도록 보고를 바로잡는다. 「새 업무 추가」 수정 창도 같은 body 포털(`AxDraftCard.tsx:411-452`)이다 — 보고 그대로 맞다
  - 근거: 코드 `ActionTaskCard.tsx:784` `document.body` · SPEC-002 §2.9 「범위 밖」
  - 권장: 코디 기록에서 「서랍 규칙이 닿는 창」을 ds/Modal 로 띄우는 것만으로 좁힌다

## 참고 (판정 제외)

- **DS-gaps 기록** — WP 2a-2 「DS 의 hover 에 `:not(:disabled)` 가 없는 것은 DS-gaps 에 적는다」는 CSS 주석(`ax.css:676-682`)에만 있다. DS-gaps 문서(`.design-sync/report/02-DS-gaps.md`)는 바뀌지 않았다. 그 파일은 FE 발주서의 allowed_paths(`frontend/src/`) 밖이라 워커가 쓸 수 없는 자리다 — 코디가 옮겨 적을 몫이다
- **서랍 안 다른 파랑** — 코디가 이미 판단한 것과 사람 행동이 아닌 것들이다. 판정에 넣지 않았다
  - `.scax-md a`·`.scax-md__ref`(`:273-286`, AI 내용 링크 — 코디 판단)
  - `.scax-msg__caret`·`.scax-rail__*`·`.scax-agent__dot`(AI 진행 표시 — 원칙상 파랑이 맞다)
  - `.scax-actioncard>small`(`:256`, 카드 상태 글자 — 행동 아님)
  - `.scax-character-picker__option[aria-checked="true"]`(`:88`, 선택 **상태** 표시 — 단추의 색이 아니라 고른 것의 표시)
- **포커스 링** — 전부 DS 파랑 링 그대로다. SPEC-002 §2.9 「범위 밖」(fix1)대로다

## 확인한 것 (PASS 근거)

**1. 상태별로 이기는 규칙 (서랍 안)**

| 단추 | 상태 | 경쟁 규칙 (명시도) | 이기는 것 | 색 |
|---|---|---|---|---|
| solid-primary(카드 밖 — AxDraftCard 「등록 중…」 · ActionProgressBatchCard 「반영 중…/저장 중…」 · CommandConfirmationForm 주 단추 · ActionPreview primary · Composer 보내기 · MessageList 다시 시도) | 비활성+hover | `.scax-button:disabled` 0,2,0 · `.scax-button--solid-primary:hover` 0,2,0 · **`.scax-drawer--chat .scax-button--solid-primary:disabled` 0,3,0**(`ax.css:681`) | 새 규칙 | line / surface-alt / ink-disabled — **파랑 0** |
| solid-primary(`.action-task-card` 안 — ActionTaskCard·ActionMeetingCard) | 비활성(+hover) | `.action-task-card>….scax-button:disabled` **0,4,0**(`:546`) > 새 규칙 0,3,0 | `:546` | 새 규칙과 **같은 값**이라 두 구조가 한 모양이다 |
| solid-danger(ActionPreview danger) | 비활성+hover | `.scax-button--solid-danger:hover` 0,2,0(`components.css:274`) · 새 규칙 0,3,0(`:682`) | 새 규칙 | 회색 — 빨강도 남지 않는다 |
| outlined-neutral(AxDraftCard 거절·수정 · ActionPreview neutral · 대화 목록 다시 시도 등) | 비활성+hover | `:hover` 0,2,0(`components.css:18`) · 새 규칙 0,3,0(`:684`) | 새 규칙 | transparent / fill-weak / ink-disabled = DS 비활성 값 |
| text-neutral(진행 묶음 수정·취소 · 명령 폼 취소 · 카드 수정·취소·초기화) | 비활성+hover | `:hover` 0,2,0(`components.css:25`) · 새 규칙 0,3,0(`:685`) | 새 규칙(카드 안은 `:546` 0,4,0) | DS 비활성 값 |
| 위 넷 | 활성 · 활성+hover | 새 규칙은 `:disabled` 에만 걸린다 | 기존 WORK-008 규칙(`ax.css:670-673`, `:not(:disabled)`) 그대로 | 검정 / ink-alt — **회귀 없음** |

- 서랍 안에서 쓰는 variant·tone 은 이 넷뿐이다(전수 — solid-primary · solid-danger · outlined-neutral(기본값) · text-neutral). `outlined-primary`·`text-primary`·`inline`·`ai` 는 서랍 컴포넌트에 0곳이다. `inline` 은 `ActionCenter.tsx:573` 한 곳이고 ActionCenter 는 채팅에 그려지지 않는다. `inline`·`ai` 는 원래 hover 에 `:not(:disabled)` 가 있다
- DS 원본(`components.css`)은 바뀌지 않았다 — WP 「DS 원본 규칙은 고치지 않는다」 ✔
- 활성 모양이 바뀐 곳은 「근거 N개 더 보기」 하나다(의도된 변경 — accent → ink-neutral, hover ink). 비활성 모양은 카드 밖 solid 단추가 DS 회색면(fill-weak)에서 카드와 같은 surface-alt+line 테두리로 바뀐다 — WP 「`.action-task-card` 의 기존 처리와 같은 모양으로 통일」 그대로다

**2. 스코프** — 새 규칙 넷은 전부 `.scax-drawer--chat` 로 시작한다. `.scax-sources__more` 는 스코프가 없지만 쓰는 곳이 `MessageList.tsx:737` 하나이고, MessageList 는 ChatDrawer 안에서만 그려진다(`App.tsx` 는 ChatDrawer 만 쓴다). 서랍 밖으로 번지는 자리는 0이다. body 포털 창(수정 창 · 첨부 고르기)은 서랍 규칙 밖이고, SPEC 「범위 밖 — 서랍 밖 창은 앱 DS」와 맞다.

**3. 테스트가 jsdom 한계를 다루는 방식** — 빈 단언은 없다. 네 갈래다.
- (a) CSS 원문을 읽어 규칙의 **정확한 선택자+선언 블록**이 있는지(공백을 걷어 낸 문자열로)
- (b) 새 규칙의 명시도가 DS hover 넷보다 **크다**는 것을 계산 함수로 단언
- (c) 새 블록에 `accent` 토큰이 없다
- (d) 실제 렌더에서 「등록 중…」이 `disabled` + `scax-button--solid-primary` 이고 `.scax-drawer--chat` 조상 아래이며, 같은 순간 「거절」이 disabled outlined-neutral 이다

(d)가 「규칙이 겨누는 클래스로 실제 단추가 선다」를 이어 준다. 한계 — cascade 를 계산하지 않는다. 그래서 `.action-task-card` 0,4,0 이 이기는 경우와 순서 동률은 (b)의 「더 크다」로만 덮인다. 그 자리는 위 표에서 손으로 계산해 확인했다. 문자열 정확 일치라 서식만 바꿔도 깨지는 취약성은 있다(기존 `ds/HoverContrast.test.tsx` 와 같은 방식).

## 사용자가 실물에서 만날 자리 (코디 화면 확인 목록)

1. **AX 초안 카드 「등록」을 누르고 포인터를 단추 위에 둔다** — 「등록 중…」이 회색(surface-alt + 옅은 테두리)이고 파랑으로 번지지 않는다. `transition` 때문에 색이 서서히 바뀌므로 0.2초쯤 지켜본다
2. **같은 순간 「거절」·「수정」에 포인터** — 회색 그대로이고 활성처럼 칠해지지 않는다
3. **진행 묶음 카드 「반영 중…/저장 중…」 · 명령 확인 폼 주 단추** — 1과 같다
4. **비활성 주 단추의 모양 변화** — 카드 밖 solid 단추의 비활성이 「테두리 없는 회색면」에서 「옅은 테두리 + surface-alt」로 바뀌었다. 같은 카드 안에 비활성 outlined/text 단추(테두리 없는 fill-weak)가 나란히 서면 두 회색이 달라 보일 수 있다
5. **「근거 N개 더 보기」** — 회색 밑줄 글자, hover 때 검정. 같은 답변의 본문 근거 링크(`.scax-md__ref`)는 여전히 파랑이다 — 코디 판단대로지만, 한 답변 안에서 두 링크 색이 갈린다
6. **결과 카드의 「미리보기」 펼치기 머리**(`.scax-preview>summary`) — 아직 파랑이다(W1)
7. **카드에서 띄운 첨부 고르기 창** — body 포털이라 앱 DS(파랑 탭·업로드 글자)다. SPEC 상 정상이다(W2)
