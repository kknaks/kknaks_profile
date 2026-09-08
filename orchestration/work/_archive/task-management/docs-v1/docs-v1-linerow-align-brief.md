# [frontend] 실물 버그 1 — 회의 중 화면 줄 행의 종류 라벨 · 본문 세로 가운데 정렬

너는 **task-management `frontend` 워커**다. 오늘 아침 사용자가 실제 회의(id 9)를 앱에서 돌리며 본 화면 버그다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

## 0. 어디서

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`, HEAD `5c72c25` = WORK-014). 백엔드 미커밋 변경(스키마 수정)이 있다 — 건드리지 마라.
**시각 정본** — `para/projects/summer-star/task-management/00-design/회의록.dc.html` L833~913(줄). 사용자 캡처: `/var/folders/_z/ldzs6w2525zbx_49m1zzsx_00000gn/T/orca-paste-1788827277530-6d64513b-138e-4211-9980-afff9e4f2329.png`(있으면 봐라 · 없으면 아래 설명으로).

## 1. 증상

회의 중 화면 `AgendaLineTree` 의 줄 행에서 **종류 라벨(「논의」)이 본문 텍스트보다 위로 붙는다.** 본문은 한 줄인데 라벨 baseline 이 본문 baseline 과 어긋나 라벨이 떠 보인다. 안건 헤더(「안건 1 · 오픈 ai · 논의 중」)는 정상.
- 예상 원인: `LineRow.tsx` 의 라벨 칸과 본문 칸이 `items-start` 이거나 라벨 폭 고정 + 줄 높이(leading)가 본문과 다름. WORK-014 가 `density` 클래스 스왑을 넣었으니 `default` · `compact` 둘 다 본다.

## 2. 고칠 것
```
LineRow.tsx   라벨 · 본문(· 있으면 시각/버튼 칸)이 첫 줄 기준으로 세로 가운데 — 본문이 여러 줄이면 라벨은 첫 줄에 맞춘다(items-start + 같은 line-height · padding-top 보정 중 시안과 맞는 쪽)
              default · compact 둘 다 · 회의 중 · 종료 후(편집 모드 포함) 화면 모두 같은 컴포넌트라 한 곳에서
테스트        RTL 로 클래스 단언(정렬 클래스가 라벨·본문 둘에 같은 규칙) · 기존 340+ 테스트 통과
```

## 3. 하지 마라
- 구조 · 배지 · 펼침 · 줄 버튼 · payload 드로어 수정 0. 클래스만.
- `app/back/` 금지. hex 리터럴 금지.

## 4. 검증
```bash
cd /Users/kknaks/orca/workspaces/task_management/docs-v1/app/front && npx tsc --noEmit && npx vitest run 2>&1 | tail -6   # Errors 0
```
앱 창(`tauri dev`)이 사용자 환경에서는 뜬다 — 네가 못 띄우면 그 사실만 적고, 사용자가 확인한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_1c173ed7-8c1c-4b28-9b4c-f7817cc54ec8 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: LineRow 세로 정렬" \
  --body "고친 파일 / 원인 한 줄 / tsc · vitest 수치"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] frontend 완료 — LineRow 세로 정렬. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] frontend: <질문>" --enter`
