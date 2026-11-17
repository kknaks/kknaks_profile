
# [planner] 현장 피드백 F-1·F-2·F-3·F-4·F-6·F-7 — SPEC 개정 · Delivery Issue 발행

너는 **day `planner` 워커**다. 너는 앞 맥락이 없다 — 아래 파일이 전부다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-feedback-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

혼자 쓰는 워크트리다.

## 1. SSOT — 먼저 읽을 것

### 사용자 결정 — 이번 범위(2026-11-17 · 이 표가 정본)

원천: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/e2e-feedback.md`(F-1 ~ F-7 · 화면 위치) · `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/_RESUME.md` §2 결정 표 · 조사 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/research-1-report.md`(파일:줄 근거).

| # | 결정 |
|---|---|
| **F-1** 귀가 대기 취소 | 「귀가 대기」 상태(배지 `day-badge--going-wait` 자리)에도 세로 ⋮ 더보기 → 「귀가 대기 취소」. **단순 되돌리기 = 귀가 대기 직전 상태(완료)로 복귀** → 그 오더지(방문 카드)가 판에 다시 보인다. |
| **F-2** 시술 현황 정렬 탭 | `/board` 머리(`day-page-head`) 오른쪽 끝에 탭 둘. 이름은 **임시 「시술순」 · 「방별순」**(사용자: 이름은 나중에 — 확정 아님으로 적어라). 시술순 = 지금 그대로(오더지 순 · 드래그 앤 드롭 지원). 방별순 = 방(룸) 이름 오름차순 · 드래그 앤 드롭 없음 · **빈방은 이번에 안 보인다**(빈방 표시는 다음 스펙). |
| **F-3** 바로 시작 | 액션바(`day-actionbar`)의 「의사 호출 · N건」 옆에 「**바로 시작 · N건**」 버튼 — 버튼 둘. **선택한 준비중 줄을 원장 호출 없이 바로 시작.** 그 줄의 KOS 집도의(`doctors[]`)에 원장이 있으면 지금처럼 그대로 시작 · **없으면 병원 시스템 계정을 KOS 집도의로 쓰고(`change-tasks-doctors` · doctorIds=[시스템 계정]) 시작.** 이로써 SPEC-002 U-7 「원장 없이 시작하는 길 없음(사용자 2026-11-09)」을 **이 방식으로 뒤집는다**(뒤집은 날짜 · 사유를 남겨라). 호출 중(수락 전) 줄은 대상 아님(지금 스펙 그대로) · N = 선택 중 준비중 줄 수 · 일부만 시작되면 나머지는 토스트. 서버 = 선택한 줄을 한 번에 받는 엔드포인트 하나 · 이번엔 웹만(앱 버튼 없음). 근거: 사용자 HAR(호출 없이 `change-tasks-doctors`[시스템 계정] 200 → `change-tasks-complete` 200 · 사용자 관찰 「의사 배정하면 KOS 바로 진행중 · 시스템 계정은 관리자라 배정 가능」) · 시스템 계정이 KOS 집도의로 남는 것 사용자 OK. 원장 칸 · 원장 상태 · 의사차트 집도의 처음 값에서 시스템 계정을 어떻게 다룰지는 코드 사실(research-1 Q1 · Q2 · Q7)을 보고 정하되 **결정이 필요한 것은 「정할 것」**으로. |
| **F-4** 웹 알림 | DAY 웹 탭이 열려 있으면 **다른 화면 · 다른 브라우저 탭 · 다른 프로그램 위에도 OS(브라우저 Notification) 알림.** 대상 = **원장 호출 알림만**(이미 쌓는 원장 호출 알림 행 — SPEC-005 · `services/notifications.py` 의 받는 계정 · 설정 규칙 그대로). 지금 SSE 는 `/board` 에서만 붙는다(`templates/board.html:8`) — 모든 화면에서 받게. 탭을 닫아도 오는 웹 푸시(서비스워커)는 **다음 스펙**. 브라우저 알림 권한 묻는 시점 · 거절 시 동작은 「정할 것」. |
| **F-6** 차트 아이콘 | 판 카드 **완료 줄**과 **「시술 완료」 탭**에서 **작성된 차트만 파란(brand) 아이콘**, 미작성(disabled 회색)은 그리지 않는다. 미완료 줄은 지금처럼 아이콘 없음. 매크로 `ui.chart_icons`(`ui.html:258-260`) 한 곳. 예: 둘 다 없음 → 「쥬베룩」 / 간호만 → 「쥬베룩 [간호]」 / 의사만 → 「쥬베룩 [의사]」 / 둘 다 → 「쥬베룩 [간호][의사]」. 스펙 E30 「여는 곳 = … 차트 아이콘」 문장(SPEC-002 :165 · :170 · :318 · :337 · :341)도 맞춘다(줄 전체가 연다 — research-1 Q12). 개발용 키트 견본도 같은 규칙. |
| **F-7** 원장 계정 수락 | **웹도 앱(SPEC-003 U-6)처럼.** 로그인 계정이 원장(`snapshot.doctors` 에 있음)이면 팝오버 없이 **본인이 집도의로 바로 수락** · 간호 · 관리 · 기타 직원은 지금처럼 원장 골라 대리 수락. 다른 원장 지정 호출도 앱처럼 본인 수락. 버튼 글자 「수락」 그대로. 서버 · API · 앱 변경 없음. |

**범위 밖**: F-5(더보기 → 이전 단계 되돌리기 — 사용자가 뒤에 따로 줌) · 빈방 표시 · 웹 푸시 · 앱 변경 · 기획안(`00-baseline/planning/`) 수정.

- 스펙: `products/day/20-spec/spec-002-procedure-board.md`(주) · `spec-005-notifications.md`(F-4) · `spec-003-mobile-app.md`(F-7 앱과 같음 · F-3 앱 버튼 없음 사실) · `spec-000-data-model.md`(필요하면) · `products/day/20-spec.md`.
- 코드(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-feedback` (base dev `4f8316a7`) — 레포 루트 `AGENTS.md`.
- Delivery 절차: `start-delivery` 스킬 · `rules/delivery-workflow.md` · `tools/harness/references/requests.md`.
- 직전 같은 형식(참고): `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/_archive/day/fix-web/fix-web-spec-brief.md` · 같은 폴더 `spec-report.md`.

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 바꾸나

사용자 2026-11-17 DAY 현장 피드백을 코드 전에 스펙에 먼저 반영한다. 위 결정 표가 정본 — 스펙을 그대로 맞춘다. 기획안은 고치지 않고, 스펙 차이표(spec-002 기획안과의 차이 절)에 이번 변경을 「사용자 2026-11-17」로 남긴다. 특히 F-3 은 11-09 결정을 뒤집으므로 U-7 · 규칙 10 · 케이스 매트릭스 · S-4 · KOS 쓰기 표에서 옛 문장을 지우지 말고 뒤집은 날짜 · 사유를 남긴다.

## 3. 계약

- F-3: 새 「선택한 줄 바로 시작」 엔드포인트(웹) — 경로 · 본문(줄 id 목록) · 응답(시작된 줄 / 거절된 줄과 409 코드) · KOS 쓰기 순서(집도의 없으면 `change-tasks-doctors`[시스템 계정] → 기존 [시작] 쓰기) 를 스펙 KOS 쓰기 표에 적는다. 기존 단건 [시작]의 `no_doctor` 를 어떻게 할지(단건도 시스템 계정으로 풀지)는 「정할 것」.
- F-4: SSE 이벤트 이름 · 조각 · 붙는 위치(공통 틀) — 코드 사실대로, 새 이름이 필요하면 후보와 「정할 것」.
- 나머지(F-1 · F-2 · F-6 · F-7): 기존 엔드포인트 · API 를 쓰는지, 새로 필요한지 코드 사실로 적는다. F-1 되돌리기 엔드포인트가 없으면 계약을 적되 결정은 「정할 것」.

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/research-1-report.md` — F-3 Q1 ~ Q5 · F-7 Q6 ~ Q9 · F-6 Q10 ~ Q12 · 고칠 방향 후보 · 정할 것
- 코드: `backend/day/services/board_rules.py:280-292`(start_block) · `services/board.py`(call :581 · accept :694 · start :807 · home :948) · `emr/kos/writes.py` · `templates/partials/board_parts.html` · `board_regions.html:55-60` · `templates/ui.html:258-260` · `templates/board.html:8` · `templates/base.html:70` · `services/notifications.py`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/day/`

## 6. 구현 단계

1. 스펙 개정 — 위 결정 표 F-1 · F-2 · F-3 · F-4 · F-6 · F-7 을 spec-002 · spec-005 · spec-003(·필요하면 spec-000 · 20-spec.md) 에 반영. 버전 · 변경 이력 올림. **사용자 말에 없는 화면 문구를 지어 넣지 마라** — 사용자 말: 「귀가 대기 취소」 · 「시술순」 · 「방별순」(임시) · 「바로 시작 · N건」 · 「의사 호출 · N건」 · 「수락」. 토스트 · 알림 본문 등 그 밖 글자는 기존 스펙 글자를 쓰거나 비워 두고 「정할 것」.
2. 열린 것은 열린 것으로 — 「정할 것」 목록(OQ)으로 모아 리포트에 둔다. 추측으로 메우지 마라.
3. 리포트에 변경 요약(파일:줄)을 남긴 뒤 **Delivery Issue 를 발행**한다(`mediness start-delivery --mediness-repo <이 워크트리> --code-repo /Users/kknaks/orca/workspaces/CENTURION_DAY/fix-feedback --github-repo MediSolveAIDev/CENTURION_DAY` — `--plan` → `--apply`). baseline 은 스펙 PR 머지 전이라 pending 이어도 된다. Target Delta = 위 결정 표 · Non-Goals = 범위 밖 목록 + migration 없음이 맞으면 그것도.
4. **승인 receipt 는 적용하지 마라** — 승인은 사용자 몫. plan_digest 와 승인 대기 상태를 보고한다.

## 7. 범위 제약 — 하지 말 것

- 코드 워크트리 수정 금지 · 커밋 · push · PR 금지(코디 몫).
- 기획안(`00-baseline/planning/`) 수정 금지 · F-5 는 쓰지 마라.
- 고객 값 · 키 · 토큰 · 계정 이메일 금지. 화면 문구 발명 금지.

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/day/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 근거 없는 정책 0 · 열린 것은 열린 것으로
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/spec-report.md` (변경 파일:줄 · 결정 표 항목별 반영 위치 · Issue 번호 · URL · 라벨 · risk · digest · baseline · 정할 것)

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_94fbe396-828d-4fa4-8bd8-829294f10614 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
