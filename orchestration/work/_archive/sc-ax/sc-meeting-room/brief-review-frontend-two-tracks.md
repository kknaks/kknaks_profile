# 발주 — 프론트 「세 벌 뼈대」 검수

## 0. 너는 누구인가

`sc-meeting-room` 의 reviewer 다. 너는 방금 **백엔드** 세 벌 뼈대를 검수했다 —
그 맥락을 그대로 쓴다. 이번엔 **화면**이 그 계약에 맞게 섰는지 본다.

**read-only 다. 코드도 문서도 한 글자 고치지 마라.** 지적만 낸다.

## 1. 정본과 재료

- 계약: `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-room-spec/products/sc-ax/20-spec/spec-004-meeting-note.md` **v0.5.1**
  ⚠ **`§4.0-2` 본문이 아직 `human` 이라 적혀 있는데 그것은 낡았다.** 사용자가 뒤집어
  벌 이름은 **`memo`·`ai`·`final`** 이다. 코드가 정본이다 (`domain.py:80`)
  ⚠ **`§8-11` 의 「원본을 여는 자리」도 낡았다.** 사용자 결정으로 **자리를 두지 않는다** —
  종료 화면은 최종 벌만 낸다. `OQ-319` 는 「만들지 않는다」로 닫혔다
- 발주서: `orchestration/work/sc-meeting-room/brief-frontend-two-tracks.md` (일곱 갈래)
  ⚠ 발주서가 `{human,ai,final}` 이라 적은 것은 **오기**다. `{memo,ai,final}` 이 맞다
- 워커 보고: `orchestration/work/sc-meeting-room/frontend-two-tracks-report.md`
- **네 백엔드 검수 리포트**: `orchestration/work/sc-meeting-room/review-backend-two-tracks-report.md`
  — §5「프론트가 고쳐야 할 것 전수」가 **이 검수의 대조표**다
- 백엔드 커밋 셋: `51ecceb`(세 벌) · `ec025f9`(FAIL 수정) · `addddbc`(schema_sync)
- 코드: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-room/frontend`
  **검수 대상은 커밋 `952f8f5` 하나다** — feat(meetings): 회의록 세 벌을 화면이 벌 축으로 가른다 (12파일).
  같이 선 `a4d1c93`(사이드바 머리 · 5파일)은 **앞 바퀴 잔여라 이번 검수 대상이 아니다** —
  다만 커밋이 갈렸는지(세 벌 작업이 그쪽에 섞이지 않았는지)는 확인해라.
  `backend/` 는 이번 검수 대상이 아니다.

  참고 — 코디가 고쳤던 둘(`shell.css` 의 `body` 글꼴 · `glyphs.tsx` 의 `tune`·`circle-exclamation`)은
  **이미 `5e7a41d` 에 들어가 있다.** 워커가 근거를 대고 셋째 커밋을 만들지 않았고 그 판단이 옳다.
  그 두 건은 이번 검수 대상이 아니다.

## 2. 무엇을 보나

### 2.1 일곱 갈래가 실제로 닫혔나

① 탭마다 자기 벌의 안건 목록 · ② `can_edit_agendas` 벌별 + `can_add_agenda` ·
③ 종료는 최종만(만들지 않는다) · ④ 결론 표시 최종 벌 한정 · ⑤ 자리표시 제목 ·
⑥ 저장이 줄 id 를 싣는다 · ⑦ 계보는 타입만.

**각각 코드에서 확인하고 파일:줄을 대라.** 보고서가 「했다」는 것을 믿지 마라.

### 2.2 조용히 통과하는 자리

- **`?? 'memo'` 류 폴백이 «없는지».** 워커가 「두지 않았다」고 했다 — 두면 AI 벌·최종 벌
  안건이 사람 벌로 끌려온다. 전수 grep 해라
- **SSE `ai_batch` 가 사람 벌을 지우지 않는가.** 백엔드가 이 이벤트를 「AI 벌만」으로 줄였다.
  화면이 `agendas` 를 통째로 갈아 끼우는 자리가 «어디에도» 없는지 확인해라.
  워커는 「`aiTab` 조건 안이고 `track==='ai'` 로 한 번 더 거른다」고 했다 — 직접 봐라
- **`can_add_agenda` 와 `can_edit_agendas` 를 혼동하지 않았나.** 사람 벌은 「진행 중」에
  **더할 수는 있지만 고칠 수는 없다.** 이 한 칸이 틀리면 회의 중 안건 추가가 막히거나
  반대로 원본이 열린다
- **줄 id 가 «모든» 저장 경로에서 실리는가.** 워커가 「409 충돌로 갈아 끼울 때도 id 를 들고 온다」
  고 했다 — 거기서 글자만 뽑으면 다음 저장이 계보를 통째로 버린다. **그 경로를 직접 읽어라**
- **결론 표시**가 회의 중 어느 탭에도 서지 않는지 (§4.0-5)

### 2.3 범위가 안 샜나

- **충돌 판정 UI 가 없는지** (`OQ-308` · D-3) — 나란히 보이기·판정 카드 전수 grep
- **원본 두 벌을 여는 자리를 만들지 않았는지** (`OQ-319`) — 탭·드로어·접힘·컨트롤
- **계보(`merged_from`·`from_lines`)를 «그리지» 않았는지** — 타입에만 있어야 한다
- **`backend/` 를 안 고쳤는지** — 커밋에 `backend/` 가 있으면 위반
- **커밋이 갈렸는지** — 세 벌 작업 / 앞 바퀴 잔여(사이드바) / 코디가 고친 둘
  (`shell.css` 글꼴 · `glyphs.tsx` 글리프)이 섞이지 않았는지

## 3. 테스트

```
cd frontend && npx tsc --noEmit && npx vitest run && npx vite build
```

- 새 검사 8건이 **갈림 자체를 거는지** 읽어라. 「탭이 있다」가 아니라 「두 탭의 안건 목록이
  다르다」를 걸어야 한다. 한 벌 시절에도 통과하는 단언이면 **빈 단언**이다
- 워커가 기존 테스트를 고쳤다 — 보고서 표에 「무엇을 왜」가 있다. **약하게 만든 자리가 없는지**
  `git diff` 로 직접 확인해라. 특히 `MeetingLive` 픽스처를 두 벌로 가른 것과
  「출처 다섯 → 넷 + null」로 바꾼 것
- `WorkViews.tsx:542` `dataTransfer` 의 Unhandled Error 1건은 **원래 있던 것**이다

## 4. 판정

각 지적에 **파일:줄 + 근거**. 근거 없는 지적은 쓰지 마라.
**FAIL**(계약과 다른 것이 돈다) · **WARN**(물어야 할 만큼 모호하다) · **PASS**

## 5. 산출물

`/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/work/sc-meeting-room/review-frontend-two-tracks-report.md`

구성: 판정 · 일곱 갈래 대조표(파일:줄 + PASS/WARN/FAIL) · 지적 목록 ·
**네 백엔드 검수 §5 목록과의 대조**(빠진 것이 있나) · 테스트 판정 · 범위 · 커밋 위생

## 6. 보고

- 판정과 지적 건수
- **가장 위험한 지적 하나**와 왜
- 저장이 계보를 살리는지에 대한 네 판정 (백엔드에서 살렸는데 프론트가 죽이면 헛일이다)
- 테스트 결과
