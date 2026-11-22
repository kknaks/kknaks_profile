
# [reviewer] 코드 검수 — mobile M1(방 옮기기 · 복귀 · 점유 띠 · 간호관리 표시)

너는 **day `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

⚠ backend 워커가 같은 워크트리 `backend/` 에서 통역 작업 중 — **읽기만.** `backend/` 변경은 이번 검수 대상 아님. git 은 읽기만(stash · checkout 금지).

## 1. SSOT — 먼저 읽을 것

- 스펙(PR 브랜치 · 정본): `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-003-mobile-app.md` U-20 · U-21 · 규칙 「서버 계산 값만」 · `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-002-procedure-board.md` 방 옮기기 · 복귀 · 점유
- 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/day-mobile-v2-app-brief.md` · 워커 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/mobile-m1-report.md` · 캡처 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/shots/m1-*.png`
- 사용자 결정: 시안 없음 — 기존 앱 컴포넌트 + DAY 웹 배치 · 글자(`backend/day/templates/partials/board_parts.html`)
- 레포 `AGENTS.md` 「앱」

기대는 개념: 해당 없음.

## 2. 배경

DAY 직원 앱 0.2.0 의 첫 앱 조각. 대상 = 워크트리 `app/` 미커밋 변경 전부(`git status` · `git diff -- app/` · 새 파일 `app/lib/ui/room_move.dart` · `app/test/ui/room_move_test.dart` · `app/test/capture/room_move_capture_test.dart`).

## 3. 계약

해당 없음(검수).

## 4. 먼저 읽을 핵심 파일

위 §1 · 바뀐 app 파일.

## 5. allowed_paths

- 리포트 1개만: `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-code-m1-report.md`

## 6. 검토 항목

1. 스펙 U-20 · U-21 대로인가 — 서버 칸(`canMoveRoom` · `canHoldMove` · `canReturnRoom` · `holdRoom` · `rooms[]` · `systemDoctor`)만으로 그리나(앱이 판정을 새로 하지 않나) · 방 목록 재묶음 규칙 · API 경로 · 본문이 서버(`backend/day/routers/api/board.py` · `schemas`)와 맞나
2. 글자가 웹 원천에 있나(파일:줄) · 지은 글자 0
3. 관대한 읽기 — 칸이 없거나 모르는 값이면 깨지지 않나
4. 회귀 — 기존 동작(카드 누름 · 의사 호출 시트 · 리포트 이슈 4 `taskDoctorLabel` 범위 밖 변경)
5. 테스트가 실제 동작을 보나 · `flutter analyze` · `flutter test`(관련 파일만) 1회

## 7. 범위 제약

- 파일 수정 · 커밋 금지. 사용자 포트 · 기기 금지.

## 8. 검증

```
지적마다 파일:줄 + 근거 · 판정 FAIL/WARN/PASS
```

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
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_5e3720e2-a945-4350-86e9-f3f6bce65ac0 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_5e3720e2-a945-4350-86e9-f3f6bce65ac0 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
