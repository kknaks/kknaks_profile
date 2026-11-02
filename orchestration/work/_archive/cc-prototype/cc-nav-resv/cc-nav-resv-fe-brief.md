# [frontend] WP1 — 공통 헤더 `현황판 | 예약관리 | 내 스케쥴` + 예약관리 빈 페이지 + 직군 가드 해제

너는 **cc-prototype `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/orchestration/roles/cc-prototype/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/cc-nav-resv`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

이 워크트리는 지금 너 혼자 쓴다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/20-spec/spec-002-cc-nav-reservation.md` **§1 만** ← 계약의 SoT. **여기 없는 건 발명하지 마라.** §2(기기별 현황판) · §3(예약관리)은 이번 범위가 아니다
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/10-decision/decision-004-cc-nav-reservation.md` D-01 ~ D-06 · D-09 — 왜 이렇게 정했나
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/20-spec/spec-001-cc-poc.md` — 1차 계약(바뀌지 않는 부분)

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

지금 cc 는 직군으로 화면이 갈린다 — 데스크 계정은 `/desk`(현황판)만, 직원 계정은 `/staff`(직원 페이지)만 연다.
서로 상대 경로를 열면 가드가 되돌려 보낸다. 헤더도 화면마다 따로다(`/desk` 는 medikit `Header`+`Menu`, `/staff` 는 `StaffShell` 안의 자체 머리).

2차에서는 로그인 뒤 모든 화면이 **같은 헤더** 하나를 쓰고, 그 헤더로 `현황판(/desk) | 예약관리(/reservations) | 내 스케쥴(/staff)` 를 오간다.
예약관리는 시안을 다시 그릴 예정이라 **이번에는 빈 페이지**로 헤더에 연결만 한다.

## 3. 계약

BE 계약 변경 없음 — 새 API 없음. 화면 계약은 SPEC-002 §1 표 그대로:

- 헤더 갈래: 직원 계정(frame ≠ `desk`) = 세 갈래 / 데스크 계정(frame = `desk`) = `현황판 | 예약관리`
- 가드: `/desk` 의 「데스크 아니면 `/staff`」 삭제 · `StaffShell` 의 「데스크면 `/desk`」는 **유지**(데스크 계정은 직원 홈이 없다)
- `/login` 은 헤더 없음 · 로그인 뒤 첫 화면은 1차 `homePath` 그대로
- 폭 < 760px = 햄버거 메뉴로 접힘 · ≥ 760px = 갈래가 헤더에 나란히
- 로그아웃 · 계정 표시는 공통 헤더로 옮긴다(같은 기능이 두 번 보이지 않게)

## 4. 먼저 읽을 핵심 파일

- `cc/front/app/desk/page.tsx:24` — `MENUS`(현황판 메뉴) · `:79` 직군 가드 · `:101` `narrow = vw < 1280` 서랍(현황판 오른쪽 패널 — 이번에 건드리지 않는다) · `:119~135` medikit `Header` · `Menu` · 로그아웃
- `cc/front/components/staff/StaffShell.tsx:50` — 데스크 가드(유지) · `:139~143` 로그아웃 버튼 · `wide = w >= 760` 판정
- `cc/front/app/staff/layout.tsx` — `/staff` 두 경로가 `StaffShell` 을 공유하는 방식
- `cc/front/app/layout.tsx` · `cc/front/app/page.tsx` · `cc/front/lib/session.ts` — 세션 · `homePath`
- 헤더를 그리는 자리는 너가 고른다(예: `/desk` · `/reservations` · `/staff` 를 묶는 route group layout). 고른 이유를 보고에 한 줄

## 5. allowed_paths — 이 밖은 건드리지 마라

- `cc/front/`

## 6. 구현 단계

1. **헤더를 쓰는 곳을 전부 grep 으로 센다** — `Header` · `Menu` · `MENUS` · `clearSession` · `router.replace('/staff'` · `router.replace('/desk'` · `homePath` 가 나오는 파일 전부. 목록을 보고에 붙인다(이 브리프의 줄 번호 목록은 출발점일 뿐이다)
2. 공통 헤더 컴포넌트 — 갈래 · 선택 표시 · 계정 표시 · 로그아웃 · 760px 미만 햄버거
3. `/desk` · `/reservations` · `/staff` · `/staff/patient/[scheduleId]` 에 붙이고, 기존 화면별 머리에서 헤더와 겹치는 것을 걷어낸다. 화면 본문(도면 · 목록 · 상세) 레이아웃은 1차와 같게 — 헤더 높이 때문에 잘리거나 이중 스크롤이 생기지 않게
4. `/reservations` 빈 페이지 — 제목 「예약관리」 + 「준비 중」 한 줄. 데모 버튼 · 테이블 등 내용은 만들지 마라
5. 가드 정리(§3)

## 7. 범위 제약 — 하지 말 것

- 폰 현황판 목록 · 탭 도면 맞춤(SPEC-002 §2 — 다음 WP)
- 예약관리 내용 · 시안(DesignSync) — 다음 WP
- `cc/back/` · 새 API · 1차 화면 본문의 동작 변경
- 사용자 포트 · 프로세스(떠 있는 dev 서버)를 건드리지 마라

## 8. 검증

```
cc/front 에서 npx tsc --noEmit · npm run lint · npm run build — 각 1회. 기능 폴더 밖 import 가 없는지 확인. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending 으로 보고
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.
- 보고에 넣을 것: 헤더가 붙은 경로 목록 · 지운 가드 · 남긴 가드 · 걷어낸 기존 머리 요소 · 760px 전후 동작

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
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_adf432d6-a97d-4457-a02d-041df0075fb7 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_adf432d6-a97d-4457-a02d-041df0075fb7 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
