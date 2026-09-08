# [frontend] WORK-011 Phase 3~4 — 슬래시 명령어 5 · 좁혀지는 팝오버 · AI 탭 통째 교체 · 줄 시각 제거

너는 **task-management `frontend` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

## 0. 어디서 무엇을 보나

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`). **WORK-011 백엔드(Phase 1 · 2)가 방금 들어왔다** — `git log -1`. WS `ai.batch` 프레임이 **AI 트랙 전체(안건 안에 줄 중첩)** 로 바뀌었다. 그 모양이 네 입력이다.

문서는 전부 **코디 워크트리 절대경로 · 읽기 전용**이다.

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/
  30-work/work-011-meeting-live.md             ← 네 빌드 계획. **Phase 3 · 4 만.** Code Surface 프론트 행 · Internal Interface(슬래시 · mergeAiBatch) · Phase 검증
  20-spec/spec-007-meeting-live.md             ← U-2(줄 시각 없음 · 안건 시각 유지) · **U-3(프롬프트 바 · 슬래시 5 · 좁혀지는 팝오버 · 그 밖은 텍스트)** · U-4(트리 통째 교체 · 미확인 점) · §4 WS ai.batch · §6 AC
  40-architecture/frontend/README.md           ← §3-3 무효화 · §8 실시간(AI 증분 = 전체 교체 · 줄 시각 없음) · §11 테스트 · 금지 목록
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/reference/2026-09-06-task-management-app/Meeting flow.md §2-3 · §2-4   ← MF-9 · 10 · 53
```

**시각 정본** — `para/projects/summer-star/task-management/00-design/회의록.dc.html` L918~972(프롬프트 바 · 팝오버) · L833~913(줄). 이 work 는 **동작**을 바꾸는 것이고 시각은 지금 화면 그대로다. 새로 그리지 마라.

## 1. 범위 — Phase 3 · 4

```
Phase 3  PromptBar.tsx — 슬래시 명령어 5개(/논의 /결정 /업무 /액션 /새안건). 스페이스가 들어오는 순간 명령어가 사라지고 칩. 백스페이스로 칩 앞에서 지우면 텍스트 복귀
         LineKindPopover.tsx — "/" 뒤 글자로 좁혀진다(앞글자 일치). 항목·구조는 그대로
         그 밖의 "/…" 는 그대로 본문 — 이스케이프·갈래 없음. "안건 이동" 은 슬래시로 하지 않는다(팝오버만)
Phase 4  aiBatch.ts mergeAiBatch — 병합 → agendas.ai 를 프레임 트리로 통째 교체(orphaned 폐기)
         useMeetingStream.ts case "ai.batch" — 교체 결과 setQueryData · orphaned 재조회 갈래 삭제
         types.ts AiBatchFrame 중첩 트리
         LineRow.tsx — formatClock(line.createdAt) 삭제(MF-9). AgendaHeader 의 안건 시각은 남긴다
         테스트 — PromptBar.test · aiBatch.test · MeetingLiveView.test
```

## ⛔ 2. 하지 말 것 · 이미 있는 것

```
PromptBar · LineKindPopover · LineRow · AgendaLineTree · useMeetingStream   전부 있다. **동작만** 고친다. 새 컴포넌트 · 새 트리 금지
서버는 kind · content 만 받는다   명령어 문자열을 서버로 보내지 마라. "/결정" 이 content 에 실리면 반려
AI 탭 트리 = 회의록 탭과 같은 AgendaLineTree   두 번째 트리 금지. 배치가 오면 트리를 통째로 바꾸고 펼쳐 둔 줄은 접힌다(id 가 새로 생긴다)
안건 우측 시각 · 안내 바 「배치 n회 반영 · HH:MM」 · 「자동 저장 · HH:MM」 · 프롬프트 바 현재 시각   그대로. 지우는 건 **줄** 시각뿐
fetch 직접 호출 · Sheet/Dialog 직접 import · hex 리터럴 · localStorage   금지(FE 금지 목록)
편집 모드 · payload 드로어 · breadcrumb · 헤더 순서   WORK-013 · 014. 건드리지 마라
```

## 3. 계약

- **슬래시 5개뿐.** 스페이스가 들어올 때 앞 토큰이 5개 중 하나면 칩, 아니면 그대로 텍스트. `/api 경로를 바꾸자` → 본문 그대로 · `/논의 /api` → [논의] + 본문 `/api`. 팝오버로 고른 것과 **완전히 같은 상태**
- **안건 없음** 상태에서는 `/새안건` 만 칩이 되고 나머지 넷은 텍스트(SPEC-007 U-3)
- **`mergeAiBatch(detail, frame)`** — 이름 유지 · 동작은 `detail.agendas.ai = frame.agendas` 교체. 반환은 새 `MeetingDetail`. 고아 판정 없음
- 미확인 점(6px `#338BF6`)은 그대로 — 배치가 오면 켜지고 AI 탭 열면 꺼진다
- 줄에 시각 0. 안건 헤더 시각 유지

## 4. allowed_paths

```
app/front/
```
`app/back/` · `app/mcp/` · 문서 · compose 금지.

## 5. 검증

WP §Execution Phase 3 · 4 의 검증 체크리스트 전부. 특히

- `/결` 까지 → 팝오버가 「결정」으로 좁혀짐 · `/결정 `(스페이스) → 텍스트 사라지고 [결정] 칩 · 백스페이스 → `/결정` 텍스트 복귀 · 전송 시 `kind:"decision"` · `content` 에 `/결정` 없음(MSW 요청 단언)
- `/api 경로를 바꾸자` → `kind:"discussion"` · `content` 그대로 · `/논의 /api` → `kind:"discussion"` · `content:"/api"`
- `/새안건 제목` Enter → `POST agendas` → `PATCH state:active` 두 요청 순서
- 안건 0개에서 `/논의 ` 는 칩이 안 된다 · `/새안건 ` 만 칩
- `ai.batch` 두 번 → 첫 프레임의 AI 안건 id 가 캐시에 남지 않는다 · 펼친 줄이 접힌다 · 미확인 점 켜짐
- 줄 행에 `HH:MM` 텍스트 0 · 안건 헤더에는 있다(RTL 단언)
- **정적 검사**: `LineRow.tsx` 에 `formatClock` 0 · `aiBatch.ts` 에 `orphaned` 0 · `features/meetings` 에 두 번째 트리 컴포넌트 0 · `fetch(` 직접 호출 0

```bash
cd /Users/kknaks/orca/workspaces/task_management/docs-v1/app/front && npx tsc --noEmit && npx vitest run 2>&1 | tail -8   # Errors 줄 0
```

**앱 창 실측** — `tauri dev` 로 회의 중 화면에서 슬래시 · 팝오버 · 배치 교체를 눈으로 확인하고 결과를 보고에 적어라(캡처 경로).

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
  --subject "frontend 완료: WORK-011 Phase 3~4" \
  --body "변경 파일 목록 / Phase 별 구현 요약 / 검증 결과(tsc · vitest 수치 · 정적 검사 · 앱 창 실측) / 계약 준수 / 미결·주의점"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] frontend 완료 — WORK-011 회의 중 프론트. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] frontend: <질문>" --enter`
