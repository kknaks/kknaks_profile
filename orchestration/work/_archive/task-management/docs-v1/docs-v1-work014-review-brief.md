# [reviewer] WORK-014 검수 — breadcrumb 링크 · 「←」 · 헤더 순서 세 화면 · 미리보기 CTA · 패널 크기 · 밀도 (+ 013 파일 이름 이관)

너는 **task-management `reviewer` 워커**다. **read-only** — 코드를 고치지 않고 테스트도 돌리지 않는다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/reviewer/role.md`

## 0. 범위

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`, HEAD `bfde960` = WORK-013). **아직 커밋 전** — 범위는 미커밋 변경 전부(프론트만 · `git mv` 둘 포함).

```bash
git status --short                      # tauri.conf.json 은 범위 밖
git diff HEAD --stat -M
git diff HEAD -M -- app/front
```

**워커 보고** — `orchestration/work/docs-v1/work014-fe-report.md`.
**산출물** — `orchestration/work/docs-v1/work014-review-report.md` **1개**.

문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`(읽기 전용)

## 1. 네 층

```
아키텍처    frontend/README.md §2 규칙 7(밀도 prop) · **§6-3 상세 헤더 규약**(링크 · 「←」= 부모 라우트 · 순서 · 반려 조건) · §7-1 · 금지 목록(position:absolute 5 · router.back)
SPEC       spec-006 U-1(breadcrumb 「홈」 링크 · 목록엔 「←」 없음) · U-4(시작 전 — 「←」 + breadcrumb · 배지 줄 → 제목 → 메타) · U-6(반응형 · 패널 고정 · 패널 안 스크롤 · 1280~1439 좌 400 / ≥1440 좌 500) · U-8(미리보기 CTA 4행 · compact 밀도) · §6 AC
           spec-007 U-1 Placement(회의 중 헤더 · 일시정지·회의 종료 배지 줄 우측) / spec-008 U-3(종료 후 헤더 · 삭제 + 상태 칩 우측)
WP         work-014-meeting-list-ui.md Phase 1~3 · §Internal Interface(Breadcrumb trail · DetailHeaderBar · 헤더 순서 · CTA · 패널 크기 · density)
결정 원본   Meeting flow.md §1-1 — MF-5 · 6 · 7 · 8
업무 화면    업무 상세 헤더가 순서의 정본(SPEC-003) — 참고만 · 순서 불변
```

## ⛔ 2. 이번에 반드시 볼 축

### 2-1. breadcrumb · 「←」 (FE §6-3 · MF-7)
```
Breadcrumb trail: {label, href?}[] — 마지막만 <span> · 앞은 전부 <a>(마지막 외 <a> 0건이면 반려) · hover/focus 링 · Tab 닿고 Enter 이동
DetailHeaderBar 는 AppShell 안(PageHeader.tsx 신설 0) · backTo 있으면 「←」 <a href={backTo}> · router.back( 0(정적)
회의록 상세 → /meetings/ · 업무 상세 → /tasks/ · 목록 화면 backTo 없음
업무 화면 diff = TaskDetailPage 의 nav 교체(+3/−9)뿐 — 업무 헤더 순서 불변 · 손으로 그린 breadcrumb nav 0
```

### 2-2. 헤더 순서 세 화면 (MF-8 · SPEC-006 U-4 · 007 U-1 · 008 U-3)
```
① breadcrumb(+「←」) → ② 배지 줄(MeetingBadgeRow — 좌 유형·프로젝트 인라인 셀렉터 / 우 액션·상태 칩 같은 높이) → ③ 제목 → ④ 메타 한 줄(일시 · 소요만)
제목이 배지 줄 위에 오면 반려 · DOM 순서 단언(compareDocumentPosition) 세 화면 전부
회의 중: 일시정지·회의 종료가 배지 줄 우측 / 종료 후: 삭제 + 상태 칩 우측 / 시작 전: 「←」 + breadcrumb
MeetingMetaInline — 일시·소요만 · 유형/프로젝트는 variant="badge" 로 배지 줄(컴포넌트 그대로 · 배치만)
MeetingDetailDrawer 헤더 이미 배지 줄 → 제목 — 수정 0
```

### 2-3. 미리보기 CTA · 패널 크기 · 밀도 (MF-5 · 6 · SPEC-006 U-6 · U-8)
```
CTA 4행 한 표(PREVIEW_CTA_LABEL) — scheduled·recording 「회의 입장」 / generating·ended 「상세보기」 · 가는 곳 넷 다 /meetings/detail?id=
패널 높이 = MeetingsScreen 이 고정 · 본문만 overflow-y-auto · 빈 상태와 바깥 클래스 동일 · position:absolute 0 · MeetingsScreen min-w-0 · flex-1
1280~1439 좌 400 고정 + 우 유동 · ≥1440 좌 500 + 우 유동 — 둘 다 화면 안 · 폭 규칙 한 자리
AgendaLineTree density?:"default"|"compact" — 글자·여백·라벨 폭만 · 구조·배지·펼침 규칙 하나 · 미리보기 전용 트리 0(트리 컴포넌트 1)
```

### 2-4. 013 이관 — 파일 이름 둘 (동작 0)
```
git mv CreateTaskFromLineDrawer.tsx → ActionPayloadDrawer.tsx · LinkTaskDrawer.tsx → TaskPayloadDrawer.tsx · import · 테스트 파일 · static needle 만 · 동작 변경 0(diff -M 으로 본다)
```

### 2-5. 금지 · 범위
```
fetch 직접 0 · Sheet/Dialog 직접 0 · hex 0 · localStorage 0 · 줄 버튼·편집·드로어·카운트 값(012·013 것) 수정 0
```

### 2-6. 테스트가 WP 검증 항목을 덮나
Phase 1~3 체크리스트 ↔ 테스트 대응표(DOM 순서 · <a> 개수 · CTA 4행 · density · 패널 클래스 · static ㉔ 6건). 없는 항목을 표로. **앱 창 네 폭 캡처는 없다**(워커가 `tauri dev` 흰 화면 — 네 번째 · 아침 사용자 항목) — 정적·클래스 단언으로 대체된 것이 무엇인지만 적어라.

## 3. 판정
- **PASS / WARN / FAIL**. 항목마다 **파일:줄 + 문서 절 번호**.
- **FAIL** = 마지막 외 <a> 0 · router.back · 제목이 배지 줄 위 · 미리보기 전용 트리 · position:absolute 패널 · 업무 헤더 순서 변경 · PageHeader.tsx 신설 · 012/013 범위 수정.
- **WARN** = 잔재 · 테스트 공백 · 문구.
- **문서 공백** = 별도 절.

## 4. 하지 마라
- 코드 · 문서 수정 금지. 테스트 실행 금지(코디가 돌렸다 — tsc 0 · vitest 360).
- 새 결정을 만들지 마라.

## 5. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_be2a2f22-5ec1-4354-ab88-7ccb824100d3 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: WORK-014 검수" \
  --body "FAIL n · WARN n · 문서 공백 n / 축별 판정 한 줄씩 / 리포트 경로"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] reviewer 완료 — WORK-014 검수 FAIL n · WARN n. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] reviewer: <질문>" --enter`
