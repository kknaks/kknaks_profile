# [frontend] WP2 — 폰 현황판 = 1차 Aside 폭 전체 (탭 · 데스크톱은 1차 그대로)

너는 **cc-prototype `frontend` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/orchestration/roles/cc-prototype/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/cc-nav-resv`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ 같은 워크트리에서 backend 워커가 `cc/back/` 에서 WP4 를 하고 있다 — `cc/back/` 은 건드리지 마라. WP1 변경(공통 헤더 · `(main)` route group)은 미커밋으로 워크트리에 있다 — 너의 앞 작업이다, 되돌리지 마라.

## 1. SSOT

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/20-spec/spec-002-cc-nav-reservation.md` (0.2.0) ← 계약의 SoT. **여기 없는 건 발명하지 마라.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/10-decision/decision-004-cc-nav-reservation.md` — 특히 **D-21 기존 디자인 무변경**
- **§2 만** 이번 범위

## 2. 배경

사용자가 폰 현황판은 새 목록 시안 대신 **지금 현황판 오른쪽 패널(Aside — 예약 · 현황 · 직원 · 고객 탭) 그대로**를 보여 달라고 했다(D-19). 탭 · 데스크톱은 1차 도면 화면을 **그대로** 둔다 — 기존 디자인을 고치지 않는다(D-21). 왼쪽 메뉴 사이드바도 ≥760px 에서는 그대로 둔다.

## 3. 계약

SPEC-002 §2 그대로. 새 API 없음.

## 4. 먼저 읽을 핵심 파일

- `cc/front/app/(main)/desk/page.tsx` — `vw` · `narrow = vw < 1280` · `drawer` · `<Menu>` 사이드바 · `<FloorGrid>` · `<Aside narrow=… onClose=…>` 와 Aside 가 여는 모달 · 패널(`CheckInModal` · `ResvDetail` · `RoomPanel` · `DischargeModal`)
- `cc/front/components/desk/Aside.tsx` — 탭 · 서랍 닫기 버튼(`onClose`) · `narrow` 처리
- `cc/front/components/common/AppHeader.tsx` — 760 판정 방식(같은 기준을 쓴다)

## 5. allowed_paths

- `cc/front/`

## 6. 구현 단계

1. `/desk` 에서 폭 < 760px 일 때: 도면 · 왼쪽 메뉴 사이드바 · 서랍 열기 버튼을 감추고 Aside 를 폭 전체 · 헤더 아래 높이 전체로. Aside 의 서랍 닫기 버튼처럼 폰에서 의미 없는 것만 숨긴다
2. Aside 에서 여는 모달 · 패널(접수 · 예약 상세 · 방 패널(현황 탭) · 귀가 등)이 폰 폭에서 화면 밖으로 넘치지 않는지 확인. 넘치면 폭만 맞춘다 — 내용 · 동작은 그대로
3. 직원 · 고객 탭에서 선택하면 도면 위 동선을 그리던 동작 — 폰엔 도면이 없으니 선택 표시만 남는 게 정상. 에러 · 빈 화면 없게
4. ≥ 760px 은 **diff 0** 이 목표 — 바뀌었다면 이유를 보고

## 7. 하지 말 것

- 시안 「Ceramique 현황판 폰 v1」 구현(안 쓴다)
- ≥760px 레이아웃 · Aside 내용 · 1차 컴포넌트 모양 변경
- `cc/back/` · 예약관리(WP4)
- 사용자 포트 · 프로세스. 코디가 3610/8610 에 띄워 둔 서버도 건드리지 마라

## 8. 검증

```
cc/front 에서 npx tsc --noEmit · npm run lint · npm run build — 각 1회. 기능 폴더 밖 import 가 없는지 확인. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending 으로 보고
```

- 보고에: 폰 폭에서 감춘 것 목록 · 모달/패널 폭 조정한 곳 · ≥760px diff 유무

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_adf432d6-a97d-4457-a02d-041df0075fb7 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend(WP2) 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_adf432d6-a97d-4457-a02d-041df0075fb7 \
  --text "[worker_done] frontend(WP2) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_adf432d6-a97d-4457-a02d-041df0075fb7 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
