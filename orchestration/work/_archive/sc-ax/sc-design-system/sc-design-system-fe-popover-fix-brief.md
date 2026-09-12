# [frontend] 버그 — 팝오버 내용이 스크롤되지 않는다

너는 **sc-ax `frontend` 워커**다(같은 세션). 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system` (HEAD `9b437bc`). 코디가 API 8001·프론트 5176 을 띄워 둔다. `backend/`·`.design-sync/`·`ds-entry.tsx` 불변.

## 1. SSOT
- `frontend/src/Popover.tsx` · `styles.css` 의 `.popover*` 규칙 · Popover 소비처 전부(`grep -rn "Popover" src --include=*.tsx`: 내 업무 「업무 유형 ▾」 필터 칩, 조직 화면, 그 외)
- 디자인 v2 `docs/design/design-system-v2.dc.html` `14 — OVERLAY` Popover 절(폭 200–400 · r12 · shadow-lg · 스크림 없음 · 트리거에서 8px). 높이 규정이 있는지 확인해 따르고, 없으면 「뷰포트 안에서 잘리지 않게 max-height + 내부 스크롤」로 하고 보고에 명시.

## 2. 배경 / 사용자 보고 (2026-09-08)
「팝오버들 다 스크롤이 안 되는 것 같다」 — 내용이 길면 팝오버 안에서 스크롤이 안 되고 잘리거나 화면 밖으로 나간다. 원인을 소비처 전수로 확인하고 **Popover 컴포넌트 한 곳**에서 고친다.

## 3. 계약
- 수정은 `Popover.tsx` + `styles.css` 의 popover 규칙에 한정. 소비처 코드는 원인이 소비처에 있을 때만(예: 내용 래퍼가 overflow hidden).
- 규칙: 팝오버 본문 `max-height` 는 뷰포트 기준(트리거 아래 남은 공간 또는 상한값), `overflow: auto`, 헤더가 있으면 헤더 고정. 휠·트랙패드·키보드 스크롤 동작. 바깥 클릭·Esc 닫힘·포커스 링은 그대로.
- hex 금지, 새 의존성 금지, `api.ts`·`viewModels.ts` 불변.

## 6. 단계 / 8. 검증
1. 소비처 전수 + 각각 긴 내용일 때 증상 재현(브라우저, 1440 폭). 2. 원인 확정 → 수정. 3. `Popover.test.tsx` 에 「내용이 max-height 를 넘으면 스크롤 컨테이너가 된다」 케이스 추가. 4. `npx tsc --noEmit` 0 · `npx vitest run src/Popover.test.tsx` + 만진 소비처 테스트. 5. 5176 에서 소비처마다 스크롤 확인 표(소비처 · 증상 · 수정 후). 커밋·push 금지.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_4fcd67c5-63d2-409e-ae57-ef22b8fa5fb1 --from term_072aa511-0dd8-4318-8318-769bb9d30ac3 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_4fcd67c5-63d2-409e-ae57-ef22b8fa5fb1 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_4fcd67c5-63d2-409e-ae57-ef22b8fa5fb1 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
