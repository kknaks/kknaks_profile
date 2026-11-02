# [frontend] WORK-014 Phase 1~3 — breadcrumb 링크 · 「←」 · 헤더 순서 세 화면 · 미리보기 CTA · 크기 · 밀도

너는 **task-management `frontend` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

## 0. 어디서 무엇을 보나

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`). **WORK-009 ~ 013 이 전부 들어와 있다** — `git log -5`(013 커밋이 최신). `AgendaLineTree` · `LineRow` · `MeetingClosedPage` 를 013 · 012 가 먼저 고쳤으니 **그 위에서** 고친다.

문서는 전부 **코디 워크트리 절대경로 · 읽기 전용**이다.

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/
  30-work/work-014-meeting-list-ui.md          ← 네 빌드 계획 전부. Code Surface · Internal Interface(Breadcrumb trail · DetailHeaderBar · 헤더 순서 · CTA · 패널 크기 · density) · Phase 1~3 검증
  20-spec/spec-006-meeting-setup.md            ← **U-1**(breadcrumb 「홈」 링크 · 목록엔 「←」 없음) · **U-4**(시작 전 — 「←」 + breadcrumb · 헤더 배지 줄 → 제목 → 메타) · **U-6**(반응형 · 패널 고정 · 패널 안 스크롤) · **U-8**(미리보기 CTA 4행 · compact 밀도) · §6 AC
  20-spec/spec-007-meeting-live.md U-1 Placement   ← 회의 중 헤더 순서 · 일시정지·회의 종료는 배지 줄 우측
  20-spec/spec-008-meeting-close.md U-3        ← 종료 후 헤더 순서 · 삭제 + 상태 칩 우측
  40-architecture/frontend/README.md           ← §2 규칙 7(밀도 prop) · **§6-3 상세 헤더 규약**(링크 · 「←」= 부모 라우트 · 순서 · 반려 조건) · §7-1 · 금지 목록
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/reference/2026-09-06-task-management-app/Meeting flow.md §1-1   ← MF-5 · 6 · 7 · 8 (그림 있음)
```

**시각 정본** — `para/projects/summer-star/task-management/00-design/회의록.dc.html` L47~68(목록 헤더) · L148~228(미리보기) · L565~585(시작 전 헤더) · L784~807(회의 중 헤더) · L1427~1443(종료 후 헤더 — **순서는 MF-8 로 정정: 배지 줄 → 제목 → 메타**) · **업무 상세 헤더**(`업무 화면 정의서.dc.html` — 순서의 정본). 새로 그리지 않는다 — 배치만 바꾼다.

## 1. 범위 — Phase 0(013 검수 이관) · 1 · 2 · 3

```
Phase 0  WORK-013 검수 WARN 2 — 파일 이름이 내용과 어긋난다. features/meetings/components/CreateTaskFromLineDrawer.tsx → ActionPayloadDrawer.tsx · LinkTaskDrawer.tsx → TaskPayloadDrawer.tsx 로 git mv(export 이름 openActionPayloadDrawer/openTaskPayloadDrawer 는 이미 맞다). import · 테스트 파일 이름 · static.test needle 을 따라 고친다. 동작 변경 0
Phase 1  components/shared/AppShell.tsx — Breadcrumb trail: readonly {label, href?}[] · 마지막만 <span> · 앞은 <a> · hover/focus 링 · TRAIL 상수 갱신
         DetailHeaderBar(같은 파일 신설 · PageHeader.tsx 만들지 않는다) — backTo 있으면 breadcrumb 왼쪽 「←」 <a href={backTo}> · router.back() 금지
         회의록 세 화면 + 업무 상세에 backTo 전달(업무 쪽은 그 한 줄뿐)
Phase 2  MeetingScheduledPage · MeetingLiveView · MeetingClosedPage 헤더 — ① breadcrumb(+「←」) → ② 배지 줄(유형 · 프로젝트 인라인 셀렉터 / 우측 액션 · 상태 칩 같은 높이) → ③ 제목 → ④ 메타 한 줄(일시 · 소요만)
         MeetingMetaInline — MeetingMetaLine 은 일시·소요만 · 유형/프로젝트 인라인은 variant="badge" 로 배지 줄에서(컴포넌트 그대로 · 배치만)
Phase 3  MeetingPreviewPanel — CTA 라벨 4행(scheduled·recording 「회의 입장」 / generating·ended 「상세보기」 · 가는 곳은 넷 다 /meetings/detail?id=) · 패널 높이 고정 + 본문 overflow-y-auto · MeetingsScreen min-w-0 · flex-1
         AgendaLineTree density?:"default"|"compact"(글자 · 여백 · 라벨 폭만) · AgendaHeader · LineRow 클래스 · 미리보기 트리에 compact
```

## ⛔ 2. 하지 말 것

```
업무 화면              backTo 한 줄 외 수정 0(git diff --stat features/tasks). 업무 헤더는 **정본 — 참고만**, 순서를 바꾸지 않는다
PageHeader.tsx 신설     하지 않는다 — AppShell 안 DetailHeaderBar
router.back()          0건. 「←」는 부모 라우트 <a>
미리보기 전용 트리       만들면 반려 — AgendaLineTree 하나에 density
position:absolute      0(패널 배치)
MeetingDetailDrawer 헤더  이미 배지 줄 → 제목 순서. 확인만, 수정 없음
줄 버튼 · 편집 · 드로어 · 카운트 값   WORK-012 · 013 것. 건드리지 마라
fetch 직접 · Sheet/Dialog 직접 import · hex 리터럴   금지
```

## 3. 계약

- `Breadcrumb` — 마지막 외 `<a>` 0건이면 반려(FE §6-3). 키보드 Tab 닿고 Enter 이동
- `DetailHeaderBar({trail, backTo})` — 회의록 상세 → `/meetings/` · 업무 상세 → `/tasks/`. 목록 화면은 `backTo` 없음
- 헤더 순서 — 제목이 배지 줄 위에 오면 반려. 우측 액션은 배지 줄과 같은 높이
- CTA 4행 · 패널 크기 = 빈 상태 기준 · 본문 스크롤 · 1280~1439 좌 400 고정 + 우 유동 · ≥1440 좌 500 + 우 유동 — 둘 다 화면 안
- `density` — 구조 · 배지 · 펼침 규칙 하나

## 4. allowed_paths

```
app/front/
```

## 5. 검증

WP §Execution Phase 1 · 2 · 3 검증 체크리스트 전부(DOM 순서 단언 · `<a>` 개수 · CTA 4행 · density · `router.back(` 0 · `position: absolute` 0 · 트리 컴포넌트 1)

```bash
cd /Users/kknaks/orca/workspaces/task_management/docs-v1/app/front && npx tsc --noEmit && npx vitest run 2>&1 | tail -8   # Errors 줄 0
```

**앱 창 실측** — 가능하면 `tauri dev` 로 1280 · 1439 · 1440 · 1920 네 폭에서 미리보기 패널이 화면 안에 있는지, 「←」와 breadcrumb 링크가 동작하는지 캡처. 못 띄우면 그 사실만.

막히면 30분 넘기지 말고 §9 (2) 로 물어라.

---

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_1c173ed7-8c1c-4b28-9b4c-f7817cc54ec8 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: WORK-014 Phase 1~3" \
  --body "변경 파일 목록 / Phase 별 구현 요약 / 검증 결과(tsc · vitest · 정적 · 앱 창 네 폭) / 계약 준수 / 미결·주의점"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] frontend 완료 — WORK-014 목록·상세 UI. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] frontend: <질문>" --enter`
