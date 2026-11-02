# [frontend] 바퀴 7 — AX 채팅 드로어·액션 센터를 새 DS 로

너는 **sc-ax `frontend` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/roles/sc-ax/frontend/role.md` (+ `rules.md`·`skills.md`·`tools.md`·`workflow.md`)

작업 워크트리: **`/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-redesign-ax`** (branch `kknaksss/sc-meeting-redesign-ax`, base 커밋 `3f9c3dc`)

## 1. 이 바퀴가 무엇인가

**남은 바퀴 중 가장 크다.** 구 `styles.css` 1545줄 중 **544줄(35%)** 이 네 범위고, 테스트 CSS 결합 153건 중 **109건**이 여기 몰려 있다.

- **AX 채팅 드로어** — `src/chat/ChatDrawer.tsx` · `MessageList.tsx` · `AssistantMarkdown` 등. 오른쪽 아래 오브를 눌러 여는 AI 어시스턴트 패널
- **액션 센터** — `src/ActionCenter.tsx` + `ActionTaskCard` · `ActionMeetingCard` · `ActionProgressBatchCard` · `ActionPreview`

**시안이 없다.** 새 DS 에 대응하는 건 `AgentBubble`(말풍선) 하나뿐이고 `AiChatSidebar` 는 Figma 정적 렌더러라 못 쓴다.
그러니 **사다리 ③** 이다 — **레이아웃은 그대로 두고 토큰·부품만 새 DS 로 갈아끼운다.** 채팅 UX 를 새로 설계하지 마라.

구 `.ax-*` 클래스가 **87종**이다. 새 DS 의 `.ax-*` 13종(타이포·스크롤)과 **이름은 안 겹치지만 접두사를 공유**한다 — 네가 새로 만드는 것은 전부 `.scax-` 로 써라.

## 2. SSOT (read-only)

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/work/sc-meeting-redesign/design/handoff/shell/js/scax-ui.jsx` 의 **`AgentBubble`**(233줄) — 우하단 말풍선 정본
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/work/sc-meeting-redesign/design/handoff/my-work/css/components.css` · `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/work/sc-meeting-redesign/design/components/work/AiChatSidebar.jsx`(참고만 — 정적이라 못 씀)
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/work/sc-meeting-redesign/design/guidelines/*.card.html` — 색·타입·간격 규약
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/work/sc-meeting-redesign/design/ds-token-report.md` §10 의 O1·O2 행

## 3. 할 일

1. **AX 드로어**를 `.scax-drawer` 골격 위로 옮긴다(바퀴 3b 가 폭 두 단 `--sm` 520 / `--lg` 840 을 이미 만들었다). 지금 폭을 유지하는 쪽을 골라라
2. 메시지 목록·마크다운·근거 레일·승인 카드·실행 레일의 **색·타입·간격·라운드·그림자를 새 DS 토큰(`--scax-*`)으로** 바꾼다. **구조는 그대로**
3. **`AgentBubble`** — 우하단 런처를 시안 모양으로(말풍선 + orb). `AssistantLauncher` 가 지금 자리다. **orb 이미지는 `assets/ai-agent-orb.png` 가 다운로드에 실패했다**(256KiB 캡). 우리 `assistantCharacterAssets.ts` 에 이미 캐릭터 에셋이 있으니 **그걸 쓰고**, 시안 orb 가 꼭 필요하면 보고해라
4. **액션 센터** 카드 4종을 새 DS 부품(`Button`·`Badge`·`Chip`·`Empty`·`Skeleton`)으로. `overrides-transitional.css` 에 「→ 바퀴 7」로 달린 규칙(ax-rail-evidence 등)이 죽으면 **보고만** 해라(P-2)
5. `--ai-*` 팔레트 8종은 **`DS-gaps` G-17 미결**이다. 구 토큰을 그대로 쓰고 손대지 마라

## 4. allowed_paths

- `frontend/src/chat/` · `frontend/src/ActionCenter.tsx` · `frontend/src/Action*.tsx` · `frontend/src/AssistantCharacter*.tsx` · `frontend/src/assistant*.ts` · 네가 새로 만드는 `frontend/src/styles/*.css`

**`backend/` 는 한 줄도 안 건드린다.** 위 목록 밖 파일은 P-1~P-5 를 따른다.

## 5. 보고

- 처리한 것 / 못 한 것
- **죽은 구 `styles.css` 구획**(줄 범위 + 근거) — 지우지 말고 보고만
- **`DS-gaps` 후보 전수** — 여기서 제일 많이 나올 것이다. 형식 지켜라
- `tsc` · vitest passed/failed · 고친 테스트 · 접근성 질의로 깨진 것과 처리
- **빈 검사가 된 곳을 찾았는지**
- P-3 으로 넓혀야 했던 공용 부품 prop (바꿨으면 전건)
## 공통 규칙 — 병렬 워커 전원 (이 절은 세 브리프가 똑같이 갖는다)

지금 **네 워커가 각자 다른 워크트리에서 동시에** 돈다. 서로를 밟지 않는 것이 최우선이다.

| # | 규칙 |
|---|---|
| **P-1** | **`frontend/src/styles.css`(구 DS, 1545줄)를 한 줄도 건드리지 마라.** 지우지도, 고치지도 마라. 네 화면을 다 옮겨서 어떤 구획이 죽었으면 **보고서에 「죽은 구획: 줄 범위 + 근거」로만** 적어라. 실제 삭제는 바퀴 9 에서 코디가 한 번에 한다. **이게 병렬의 유일한 충돌원이라 막는 것이다** |
| **P-2** | **`src/styles/overrides-transitional.css` 도 건드리지 마라.** 같은 이유다. 네 바퀴에서 죽은 규칙이 있으면 보고만 |
| **P-3** | **공용 부품(`Button`·`Badge`·`Chip`·`Icon`·`Modal`·`Select`·`Empty`·`Skeleton`·`Popover`·`AppShell`…)의 시그니처를 바꾸지 마라.** 넓혀야 하면 **바꾸지 말고 보고**해라 — 다른 워커가 같은 파일을 만지고 있다. 정말 못 넘어가면 **가장 작게** 넓히고 전건 보고 |
| **P-4** | **`App.tsx` 를 건드리지 마라.** 셸 배선은 바퀴 2·5a·6a 에서 끝났다. 꼭 필요하면 보고하고 이유를 대라 |
| **P-5** | **네 화면 파일과 새 CSS(`src/styles/*.css` 중 네가 새로 만드는 것)만** 만져라 |
| **P-6** | 커밋·push 하지 마라. 코디가 브랜치별로 검증하고 커밋한다 |

## 공통 원칙 — 앞바퀴에서 굳은 것

- **레이아웃·시각은 시안이 정본, 로직·구조는 우리 것.** 상태 관리·`api.ts` 호출·권한 판단·`viewModels`·책임 분리는 안 바꾼다
- **시안이 없는 화면은 레이아웃을 그대로 두고 토큰·부품만 새 DS 로 갈아끼운다.** 새로 디자인하지 마라
- **없으면 발명하지 마라.** 새 DS 에 대응이 없으면 구 것을 남기고 **`DS-gaps` 후보로 보고**해라(현재 30건). 형식: `없는 것 / 어디서 몇 곳 / 구 DS 에선 무엇 / 새 DS 에서 가장 가까운 것 / 제안`. **결정은 사용자가 한다 — 네가 정하지 마라**
- **BE 계약이 없어도 그려라.** 「계약이 없으면 안 그린다」는 폐기됐다. 그리되 **무엇이 비었는지 보고**해라. 예외는 **눌러도 저장될 데가 없어 사용자를 속이는 것** 하나뿐
- **가짜 데이터 금지.** 사람 이름·파일·수치를 지어내지 마라. 핸드오프 예제의 값을 우리 화면에 옮기지 마라
- **아이콘이 모자라면 새로 그리지 말고** 뜻이 가까운 것으로 쓰고 보고

## 검증 (전원 공통)

```
cd frontend && npx tsc --noEmit          → 0 에러
cd frontend && npx vitest run             → 전체 1회
```

> 기준선: 커밋 `3f9c3dc` 시점 **`43 files · 474 tests` 전부 통과.** 시작 전에 한 번 돌려 확인해라.
> 새 워크트리라 `frontend/node_modules` 가 없다 — `npm ci` 부터 해라.

**깨진 테스트의 종류로 네 작업을 판정한다** (앞바퀴에서 값을 한 규칙이다):
- 클래스 선택자가 깨졌다 → 고친다
- **접근성·텍스트 질의가 깨졌다 → 멈추고 기능이 살아 있는지 먼저 확인.** 없앴으면 되살려라
- **「없음」 단언(`queryBy…` 가 null)이 통과로 바뀌었다 → 조용한 구멍이다.** 이번 세션에서만 네 번 나왔다. 반드시 확인
