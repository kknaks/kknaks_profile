
# [mobile] M1 — 방 옮기기 · 복귀 · 점유 띠(U-21) · 「간호관리」 표시(U-20) — 기존 API 만

너는 **day `mobile` 워커**다. 너는 앞 맥락이 없다 — 이 브리프가 전부다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/roles/day/mobile/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

⚠ **backend 워커가 같은 워크트리의 `backend/` 에서 통역 작업 중이다 — `backend/` · `deploy/` · `scripts/` 는 읽기만.** 너는 `app/` 만. git 명령은 읽기만(stash · checkout · reset 금지).

## 1. SSOT — 먼저 읽을 것

- **스펙(정본 · PR 브랜치 — 머지 전이다 · 이 경로가 정본)**: `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-003-mobile-app.md` — 개정 ⑲ · **U-20 · U-21**(:496 ~ :510 근처) · §1 범위 표 · 규칙 「서버 계산 값만」 · §5 OQ(A52 · A54 · A55 · A58)
- 같은 스펙 `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-002-procedure-board.md` — 방 옮기기 · 복귀 · 점유 규칙 · 개정 ㉕ · 방 목록 재묶음(W-2)
- **사용자 결정(2026-11-20)**: 앱 시안 없음 — **지금 앱 컴포넌트(기존 시트 · 버튼 · 칩)를 그대로 쓰고, 배치 · 글자는 DAY 웹을 따른다.** 웹에 없는 글자는 짓지 말고 비워 두고 리포트에 적어라.
- 웹 원천(읽기만): `backend/day/templates/partials/board_parts.html`(방 옮기기 :283-293 · 점유 띠 `holdRoom` :174-178 · 「간호관리」 :83 · :134) · `backend/day/presentation/board.py:70-79`(rooms[] · takenBy)
- 조사 · 검수 지도: `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/research-current-state.md` §C · `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-doc-1-report.md` W-2 · W-3
- 레포 규칙: 워크트리 루트 `AGENTS.md` 「앱」 절 먼저.

기대는 개념: `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/para/areas/concept/` 에서 `tolerant-reader` 를 찾아 읽어라(앱이 모르는 값 처리 기준).

## 2. 배경

DAY 직원 앱 0.2.0. 이번 M1 은 **서버를 안 바꿔도 되는 화면만**: 방 옮기기(이동 · 점유 이동) · 방 복귀 · 점유 띠 표시(U-21) · 원장 칸 「간호관리」 표시(U-20 — 표시만 · 누르면 원장 바꾸기는 다음 M 에서 `canChangeDoctor` 가 생긴 뒤). 서버 API · 스냅샷 칸(`canMoveRoom` · `canHoldMove` · `canReturnRoom` · `holdRoom` · `rooms[]` · `tasks[].systemDoctor`)은 dev 에 이미 있다.

## 3. 계약

기존 `/api/visits/{id}/room-move` · `/api/visits/{id}/room-return` · 스냅샷 칸 그대로(`backend/day/routers/api/board.py` · `backend/day/schemas/` 에서 확인). 앱은 서버 계산 값만 쓴다. 방 목록은 스펙 U-21 의 재묶음 규칙(지금 방 빼기 · 자기 자신을 `takenBy` 에서 빼기 · 빈 방 먼저)대로.

## 4. 먼저 읽을 핵심 파일

- `app/lib/ui/room_screen.dart`(룸 상세 · :483 담당의 자리) · `app/lib/ui/board_screen.dart`(카드) · `app/lib/model/board.dart` · `app/lib/state/board_controller.dart` · `app/lib/core/copy.dart` · `app/lib/ui/format.dart`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `app/lib/` · `app/test/`
- 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/mobile-m1-report.md` · 시뮬레이터 캡처 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/shots/m1-*.png`

## 6. 구현 단계

1. 모델에 필요한 칸 읽기(`canMoveRoom` · `canHoldMove` · `canReturnRoom` · `holdRoom` · `rooms[]` · `systemDoctor`) — 모르는 값은 관대하게.
2. U-21: 룸 상세에 방 옮기기 진입(웹 배치 · 글자) → 방 목록 시트(재묶음 규칙) → 이동 / 점유 이동 → 성공 · 오류 토스트(웹 글자 · 없으면 비움). 점유 띠(카드 · 룸 상세) + [복귀] → `room-return`.
3. U-20: 진행중 · 완료 줄과 카드 담당의 자리에 `systemDoctor` 면 「간호관리」(웹 글자). 누르는 동작은 넣지 마라.
4. 테스트(위젯 · 모델) 추가.
5. 시뮬레이터 캡처: 로컬 백엔드가 떠 있지 않으면 위젯 테스트 golden 또는 목 데이터 화면으로 캡처 — 사용자 포트 · 프로세스 · 기기를 건드리지 마라. 못 하면 pending.

## 7. 범위 제약 — 하지 말 것

- `backend/` 수정 금지(backend 워커 작업 중). 통역 · 로그인 · 알림 · 바로 시작 · 호출 취소 · 원장 바꾸기는 이번 아님.
- 화면 글자 짓기 금지. 커밋 · push · PR 금지. 버전 · 빌드 번호 바꾸지 마라.

## 8. 검증

```
cd app && flutter analyze · flutter test · flutter build ios --no-codesign — 각 1회(통합은 마지막). 사용자 포트·프로세스·기기를 건드리지 않는다. 서명·TestFlight 는 사용자 몫 — 실행 못 한 검증은 사유와 함께 pending
```
- 리포트 `mobile-m1-report.md`: 바꾼 파일 · 글자 출처(웹 파일:줄) · 비운 글자 · 테스트 수치 · 캡처 목록.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **완료 보고는 dispatch preamble 의 worker_done 명령을 그대로 따른다**(아래 옛 형식과 다르면 preamble 이 맞다).
- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_5e3720e2-a945-4350-86e9-f3f6bce65ac0 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "mobile 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_5e3720e2-a945-4350-86e9-f3f6bce65ac0 \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_5e3720e2-a945-4350-86e9-f3f6bce65ac0 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
