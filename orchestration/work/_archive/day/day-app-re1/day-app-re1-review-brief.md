
# [reviewer] 앱 차트 코드 검수 — #281 backend · #282 mobile (커밋 `43ba40a3`)

너는 **day `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

backend · mobile 은 끝났다. 코디가 같은 워크트리에서 로컬 스택(.run/ · 포트 11040)을 띄워 실물 확인 중이다 — 프로세스 · 포트 · `deploy/*.env` · `.run/` 건드리지 마라. 레포 파일 수정 금지.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/delivery-1-report.md` §「BE ↔ APP 계약 전문」 C0 ~ C3 ← 계약
- SPEC: `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec/products/day/20-spec/spec-002-procedure-board.md`(개정 ㉚) · `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec/products/day/20-spec/spec-003-mobile-app.md`(개정 ㉑ · U-23 · A-51 ~ A-60)
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/_RESUME.md` §2(D1 ~ D15 · D6′)
- 워커 보고 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/be-1-report.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/app-1-report.md`
- Issue MediSolveAIDev/CENTURION_DAY#281 · #282(읽기만)

**기대는 개념**: 해당 없음

## 2. 배경 / 무엇을 바꾸나

1루프 구현 검수. 대상 = `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1` 의 커밋 `43ba40a3`(= `git diff 55e60aa4..43ba40a3`). 다음은 사용자 시뮬레이터 E2E 다 — 그 전에 계약 위반 · 조용히 통과하는 자리를 잡는다. 픽셀 · 간격은 2루프 몫이니 FAIL 로 잡지 마라.

## 3. 계약

C0 ~ C3 그대로.

## 4. 먼저 읽을 핵심 파일

- `git -C /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1 diff 55e60aa4..43ba40a3 --stat` 부터 · 새 파일 `backend/day/routers/api/board_photos.py` · `backend/day/schemas/board_charts.py` · `photos.py` · `app/lib/model/chart.dart` · `app/lib/state/chart_controller.dart` · `app/lib/ui/chart_photos.dart` · `app/lib/ui/session_nav.dart` · `app/lib/ui/chart_sheet.dart` · `app/ios/Runner/Info.plist` · `deploy/` Caddy

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정 금지. 산출물은 브리프가 지정한 리포트 파일 1개뿐)`

## 6. 구현 단계

1. 계약 대조 — C2 · C3 경로 / 요청 / 응답 / 오류 코드 / 권한(view · edit · is_admin)이 백과 앱에서 **같은 이름 · 같은 모양**인지(앱이 기대하는 칸을 백이 실제로 내는지 줄 단위로)
2. 서비스 재사용 — 새 라우터가 웹과 같은 서비스를 부르나(복사 · 갈라진 규칙 없음) · 웹 경로 동작 · 쿠키 전용 GET 그대로인가
3. 앱 동작 — 닫기 표(D6′ · D12) 다섯 길 × 미저장 있음 / 없음 · 충돌 409 반영 · 저장 실패 시 쓴 글 유지 · 보기 권한이면 쓰기 UI 없음 · 10초 tick 이 탭 닫히면 멈추나 · 세션 Navigator 로 옮긴 시트들(D14)이 세션 끝날 때 같이 사라지나 · 사진 파일 GET 에 Bearer 머리
4. Info.plist 문구 = `_RESUME.md` D15 와 바이트 일치 · 까만 줄 테마
5. 테스트가 실제로 그 동작을 지키나(더블이 너무 넓어 아무것도 안 보는 테스트) · 「조용히 통과하는 자리」
6. 범위 밖 변경 · 새 화면 글자 발명 · 새 패키지
7. 마지막에 **「사용자가 시뮬레이터에서 만날 자리」** 목록 — 막히진 않는데 사람 눈에 이상해 보일 곳

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/review-code-1-report.md` — 판정 FAIL / WARN / PASS · 지적마다 파일:줄 + 근거(SPEC 절 · D 번호) + 고칠 방향.

## 7. 범위 제약 — 하지 말 것

- 레포 파일 수정 · 커밋 · push 금지(리포트 1개만)
- 로컬 스택 · 포트 · 프로세스 · `deploy/*.env` 건드리지 마라 · 시뮬레이터 실행 금지
- 결정 · SPEC 을 다시 열지 마라 — 이상하면 「사용자 확인 필요」로 따로

## 8. 검증

```
각 지적에 파일:줄 + 근거(SPEC 절 · DEC D-번호). 판정 FAIL · WARN · PASS. 「조용히 통과하는 자리」를 따로 본다
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **(코디 추가 · 2026-11-25)** 이번 발주는 orca Run(`worker-start`)으로 나간다. **dispatch preamble 에 적힌 `worker_done` 명령(Task · Dispatch ID · `--outcome` · `--report-path`)이 아래 (1)보다 우선**이다. (2) 직접 주입은 그대로 해도 된다.

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_414d6113-407d-486b-ab54-10a4a6b455cb --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_414d6113-407d-486b-ab54-10a4a6b455cb \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_414d6113-407d-486b-ab54-10a4a6b455cb --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
