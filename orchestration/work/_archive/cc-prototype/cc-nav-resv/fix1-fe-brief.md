# [frontend] fix1 — E2E 피드백 batch-1 세 건(수정 미리보기 부제 · 토스트 색 · 폰 햄버거 가림)

너는 WP1 · WP2 · WP4-FE 를 한 그 frontend 워커다. 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/cc-nav-resv` — 앞 변경 전부 미커밋, 되돌리지 마라. `cc/back/` 은 건드리지 마라.

## 1. SSOT

- 피드백 원문 · 원인 · 방향: `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/orchestration/work/cc-nav-resv/e2e-feedback-batch-1.md` #1 ~ #3 ← 이 표가 범위다
- D-21(기존 디자인 무변경): `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/10-decision/decision-004-cc-nav-reservation.md`

## 2. 고칠 것

1. **#1 수정 미리보기 부제** — 같은 묶음에 KOS 등록 이력(snapshot 있는 줄)이 없으면 「이미 등록된 예약을…」 대신 등록 전임을 말하는 문구. 시안 톤(짧은 해요체)으로, 문구는 보고에 적어라. 버튼 · 제목(「KOS 수정 미리보기」 · [KOS 수정하기])은 시안 그대로 둔다
2. **#2 토스트** — 1차 토스트(`app/(main)/desk/page.tsx:270` 근처)와 같은 클래스 · 모양. 그리고 **새로 만든 파일 전부(`components/reservations/*` · `app/(main)/reservations/page.tsx` · `components/common/AppHeader.tsx` · `app/globals.css` 추가분)에서 쓴 `ms-*` · `text-typo-*` · `primary` 류 클래스를 grep 으로 다 뽑아 1차 코드나 medikit 에 실제로 있는지 대조**하라. 없는 것은 1차에 있는 것으로 바꾼다. 대조 표를 보고에
3. **#3 폰 햄버거 가림** — 폭 < 760 에서 헤더 · 메뉴 패널 · 막이 본문(Aside 포함) 위로. ≥ 760 의 1차 서랍(Aside 41 · 막 40) 동작은 그대로. 모든 `zIndex` 를 grep 해서 층 순서 표(본문 < 헤더/메뉴 < 모달 · 토스트 · 팝오버)를 보고에 — 모달이 헤더 아래로 깔리는 곳이 없어야 한다. `/staff` · `/reservations` 에서도 메뉴를 펼쳐 가리는 것이 없는지 코드로 확인

## 3. 하지 말 것

- batch-1 밖 수정 · 1차 화면 모양 변경 · `cc/back/` · 사용자 포트/프로세스(코디의 3610/8610 포함)

## 8. 검증

```
cc/front 에서 npx tsc --noEmit · npm run lint · npm run build — 각 1회. 기능 폴더 밖 import 가 없는지 확인. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending 으로 보고
```

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
  --subject "frontend(fix1) 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_adf432d6-a97d-4457-a02d-041df0075fb7 \
  --text "[worker_done] frontend(fix1) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_adf432d6-a97d-4457-a02d-041df0075fb7 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
