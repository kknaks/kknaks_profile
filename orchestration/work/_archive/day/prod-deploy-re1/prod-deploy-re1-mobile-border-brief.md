
# [mobile] 앱 카드 테두리(파란 띠) 없애기 — A1

너는 **day `mobile` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/roles/day/mobile/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1` (브랜치 `kknaksss/prod-deploy-re1` · PR #244)

⚠ 미추적 `app/store/` · `app/tool/store_capture/` 는 앱 세션 소유다 — 건드리지 마라. 같은 워크트리에서 다른 워커가 일할 수 있다 — 네 allowed_paths 밖 변경은 손대지 마라.

## 1. SSOT — 먼저 읽을 것

- 사용자 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/e2e-feedback.md` **A1**(사용자 말 그대로)
- 스펙(지금 문장 — planner 가 같은 결정으로 고치는 중): `/Users/kknaks/orca/workspaces/mediness-mediness/prod-deploy-re1-spec/products/day/20-spec/spec-003-mobile-app.md` :194 · :261 · :334 · :342 · :719

기대는 개념: 해당 없음.

## 2. 무엇을 바꾸나

사용자 2026-11-12: 「우리 앱에서 파란색 띠 다 빼자고 한 거 아니야?」 · 「띠는 다 없애자는 거였는데」.
지금 앱은 **시술 중(`doing`)** 일 때 카드 · 행을 DAY 주색(`Ms.primary`) 테두리로 두른다(시술현황 탭 카드 · 방 상세 시술 행 등). **이 색 테두리를 모두 없앤다** — 그 자리는 상태와 상관없이 평소 카드 · 행과 같은 테두리(지금 평소 값)로 둔다.

- 대상 = 상태에 따라 **카드 · 행 바깥 테두리 색**을 바꾸는 곳 전부. 아는 곳: `app/lib/ui/board_screen.dart:296` · `app/lib/ui/room_screen.dart:533`. **목록이 아니다 — `app/lib` 에서 `Border.all(` · `BorderSide(` · `border:` 를 전부 grep 해 상태(doing · alert · selected 등)로 색을 바꾸는 카드 · 행 테두리를 세고 리포트에 표로 적는다.**
- 그대로 둘 것: 카드 안 연한 배경(시술 중 연한 DAY 배경) · 「확인 필요」 상자의 옅은 빨강 바탕과 왼쪽 빨간 띠(3차 B안 · `board_screen.dart:347` — 사용자가 말하지 않음) · 필터 칩 · 버튼 · 입력칸 · 구분선. 판단이 애매한 곳은 고치지 말고 리포트에 「애매」로 적는다.

## 3. 계약

해당 없음 — 서버 · API · 데이터 변경 없음. 화면 문구 변경 없음(새 글자 넣지 마라).

## 4. allowed_paths

- `app/lib/ui/` 아래 테두리 줄만 · `app/test/` 아래 이 변경 시험(있으면 맞춤)

## 5. 범위 제약 — 하지 말 것

- 스펙 · backend · 웹 · `app/ios` · 버전 · 빌드 번호 변경 금지. 빌드 · TestFlight 업로드 금지(앱 세션 몫).
- 사용자 포트 · 프로세스(로컬 11040 · `day-local`) 건드리지 마라.

## 6. 검증

```
cd app && flutter analyze <만진 파일> · flutter test <관련 시험 파일만> — 각 1회. 실행 못 한 검증은 사유와 함께 pending
```

- 고친 화면의 전/후 캡처를 시뮬레이터로 남길 수 있으면 `orchestration/work/prod-deploy-re1/fe-captures/` 에(실명 · 이메일 보이면 남기지 마라). 못 하면 pending.
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/mobile-border-report.md` (grep 표 · 바꾼 파일:줄 · 그대로 둔 것과 이유 · 검증 수치)

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디 handle 이 preamble 과 다르면 preamble 이 맞다.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다.
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_e62e850f-aae8-4092-a945-6f9406c2af07 --from term_673fbaad-f2e5-4915-8835-e0035563e1ef \
  --type worker_done \
  --task-id <이 태스크의 taskId> \
  --dispatch-id <이 태스크의 dispatchId> \
  --subject "mobile 완료: <한 줄>" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 미결·주의점"

orca terminal send --terminal term_e62e850f-aae8-4092-a945-6f9406c2af07 \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_e62e850f-aae8-4092-a945-6f9406c2af07 --text "[질문] mobile: <질문>" --enter`
