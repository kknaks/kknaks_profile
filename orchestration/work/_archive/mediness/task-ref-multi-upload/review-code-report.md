# 리뷰 리포트 — task-ref-multi-upload / frontend (2026-09-03)

## 판정: WARN

계약 8개 항목 **전부 통과**. allowed_paths 이탈 없음, API·콜사이트·범위 제약 위반 없음,
§4.19.1 폼 한 벌 유지, 테스트 실효성 확인. 아래 WARN 4건은 **머지 가능하되 알아야 할 것**이며
재작업 사유는 아니다 — 수정 여부는 코디네이터 판단.

## 검수 범위

- diff: `origin/dev`..worktree, **수정 2개 + untracked 1개 = 3파일** (커밋 없음, working tree 기준)
  - `front/components/tasks/TaskReferenceList.tsx` (+149/−39)
  - `front/vitest.config.ts` (+4, include 1행 + 주석 3행)
  - `front/__tests__/task-reference-multi-upload.test.tsx` (신규 213줄, untracked)
- 실행한 검사 (전부 read-only):
  - `git diff origin/dev --stat` · `git status --short` — 범위 산정
  - `git -C .../mediness-mediness show origin/mediness:...spec-154-decision-workflow.md` — §4.19.1 원문 대조
  - `grep -rn "onAddFile" front --include="*.tsx"` — 콜사이트 전수
  - `front/lib/tasks/task-references.ts` · `ManualTaskCreateModal.tsx` · `TaskDetailRail.tsx` 대조 읽기
  - **테스트는 실행하지 않았다** (브리프 §3 지시 — 코디가 8/8 확인 완료)

## 위반 (FAIL 사유)

없음.

## 경미 (WARN)

### W1. 부분 실패 재시도 시 **제목 축이 뒤집힌다** — 계약 6(제목 축)의 경계 케이스

`TaskReferenceList.tsx:338,345,373`

`single = files.length === 1` 은 **매 submit 마다 현재 `files` 로 다시 계산**되고, `title` 상태는
`titleShown` 이 false 로 바뀌어도 **지워지지 않는다**. 그래서:

1. 파일 1개 선택 → 표시 이름 「산출물」 입력 (`title` 상태에 남는다)
2. 파일 2개 추가 선택 → `titleShown=false`, 입력칸은 사라지지만 `title` 은 `"산출물"` 그대로
3. 제출 → 3건 모두 `title=""` 로 나감 (여기까지는 계약대로)
4. 1건 실패 → `setFiles(failed)` 로 `files.length===1` → **입력칸이 「산출물」이 채워진 채 다시 나타나고**
5. 재시도 → 그 파일만 `title="산출물"` 로 올라간다

성공한 2건은 파일명, 재시도된 1건만 「산출물」 — 같은 배치가 두 축으로 갈린다.
근거: 브리프 §6-2 「2개 이상이면 파일명을 그대로 쓴다」의 의도. 신규 테스트 `:187-200` 은
다중 선택 시점만 덮고 이 전이는 덮지 않는다.

- 권장 수정: `titleShown` 이 false 로 넘어갈 때 `setTitle("")` 하거나, `single` 판정을
  제출 시점의 `files.length` 대신 **이번 배치의 원 개수**로 잡는다.

### W2. 에러 리스트 React key 중복 가능

`TaskReferenceList.tsx:534-535` — `key={message}`. `files` 는 `:461` 에서 **누적 append** 되므로
서로 다른 두 번의 선택에서 **같은 파일명**이 들어올 수 있고(다른 폴더의 동명 파일), 둘 다 같은
사유로 실패하면 `reasons` 에 **동일 문자열 2개** → duplicate key 경고 + 리컨실리에이션 이상.
근거: 리포 기존 패턴(`:485` 의 파일 목록은 `${name}-${size}-${i}` 로 인덱스를 섞어 이미 방어했다) —
같은 파일 안에서 두 리스트의 key 규율이 갈렸다.

- 권장 수정: `key={`${i}-${message}`}`.

### W3. 새 파일을 고르면 **직전 업로드 실패 사유가 사라진다**

`TaskReferenceList.tsx:460` — `setErrors(rejected)` 가 무조건 덮어쓴다. 부분 실패로
`files=[b.pdf] / errors=["b.pdf · …"]` 상태에서 사용자가 파일을 더 고르면 25MB 거절이 없는 한
`rejected=[]` 라 **실패 사유만 증발**하고 `b.pdf` 는 이유 없이 목록에 남는다(목록 행 자체에는
실패 표시가 없다 — `:483-507`).
근거: 계약 5 「실패 건만 목록에 남고 사유를 단다」의 사후 상태가 유지되지 않는다.

- 권장 수정: 25MB 거절과 업로드 실패를 다른 슬롯에 두거나, 실패 표시를 파일 행에 붙인다.

### W4. 같은 파일 중복 선택에 dedup 이 없다

`TaskReferenceList.tsx:461` — `setFiles((prev) => [...prev, ...accepted])`. 같은 파일을 두 번 고르면
두 건이 큐에 서고 서버에 **행 2개**가 생긴다. 건별 제거 버튼(`:495-505`)이 있어 복구는 되고
브리프가 dedup 을 계약하지도 않았으므로 위반은 아니다 — 인지 항목.

## 기존 부채 (이번 판정 제외)

없음. (`uploadPendingTaskReferences` `lib/tasks/task-references.ts:196-226` 은 이번 diff 밖이고
무변경 확인.)

## 참고 — 검증했으나 위반 아님

**세 번째 소비 표면의 blast radius.** 브리프가 명시한 두 표면(레일 다이얼로그·완료 모달) 외에
`ManualTaskCreateModal.tsx:454-462` 이 같은 폼을 `presentation="inline"` 으로 쓴다. 이제 `onAddFile`
이 **연속 N회** 불리므로 stale-closure 유실(컴포저 다중첨부 테스트가 지키는 바로 그 버그)이
의심됐으나, `queueReference`(`:183-189`)가 **함수형 setState + `refSeq` ref** 로 되어 있어 안전하다.
`title=""` 도 `pendingTaskReferenceLabel`(`lib/tasks/task-references.ts:177-182`)이 파일명으로 폴백한다.
→ **안전 확인. 다만 이 경로를 지키는 테스트는 없다**(브리프 §6-5 범위 밖이라 결함으로 세지 않는다).

## 확인한 것 (PASS 근거)

| # | 계약 항목 | 확인 방법 | 결과 |
|---|---|---|---|
| 1 | allowed_paths (`front/`) | `git diff --stat` + `git status --short` | ✅ 3파일 전부 `front/` 안. 이탈 0 |
| 2 | API 계약 무변경 | `lib/tasks/task-references.ts:147-157` 대조 — diff 에 없음 | ✅ `form.append("file", …)` 1개/요청 유지. `addTaskReferenceFile`·BFF·`back/` 무변경 |
| 2 | 순차(병렬 금지) | `:341-352` `for` + `await` 단일 루프. `Promise.all`/`map(async` 없음 | ✅ 동시 진행 1건 |
| 3 | 콜사이트 무변경 | `grep -rn "onAddFile"` → `TaskCompletionModal:215` · `ManualTaskCreateModal:460` · `TaskDetailRail:184` 전부 diff 밖 | ✅ 시그니처 `(file, title) => Promise<void>` 그대로(`:282`), 루프는 폼 내부(`:341`) |
| 4 | §4.19.1 폼 한 벌 | `presentation` 참조 지점 전수(`:568,588…`) — **껍데기 분기만**, 다중첨부 로직은 `formBody` 단일 | ✅ 표면별 복제·분기 0. spec 원문 「갈리는 것은 껍데기뿐」 준수 |
| 5 | 건별 25MB 가드 | `:449-461` — 초과분만 `rejected`, 통과분만 `accepted` 로 목록 유지. 기존 문구 「파일당 25MB 까지 올릴 수 있어요.」 톤 유지 | ✅ 배치 통째 폐기 없음 |
| 5 | 부분 실패·롤백 없음 | `:344-358` — 건별 try/catch, 루프 계속, `setFiles(failed)` 로 실패분만 잔류 | ✅ 성공분 롤백 없음, 재시도 시 성공분 재업로드 없음 |
| 6 | 제목 축 | `:338,345` `single ? title : ""` · `:373` `titleShown` | ⚠ 정상 경로 ✅ / 재시도 경계 **W1** |
| 6 | role 선택 컨트롤 없음 | `:396-414` 토글은 `link`/`file` 두 값뿐, `role` 은 여전히 prop | ✅ |
| 7 | 범위 제약 | diff 파일 목록 = 2개. `uploadPendingTaskReferences`·생성 모달 큐·랜딩챗(`Composer.tsx`) 전부 미변경 | ✅ 패턴만 차용(`Array.from` + `multiple`은 `Composer.tsx:201-212` 선례) |
| 8 | vitest include 등재 | `vitest.config.ts:139` 에 `"__tests__/task-reference-multi-upload.test.tsx"` 추가, 기존 주석 규율(왜 도는지) 동일 톤 | ✅ 실제로 돈다 |
| 8 | 테스트 실효성 | 신규 파일 8케이스 정독 | ✅ 순차성(`maxInFlight()===1`, resolve 5ms 지연으로 병렬 검출 가능 · `:44-59,105-112`) · 순서(`:98-102`) · 건별 거절(`:114-128`) · 부분 실패 + 재시도 중복 없음(`:139-171`) · 제목 분기 양방향(`:173-200`) · **두 `presentation` 값 모두**(`:202-212`) 커버 |
| FE 규율 | 컴포넌트·lib 재사용 | `formatReferenceSize`·`Icons.X`·`TASK_REFERENCE_MAX_BYTES` 전부 기존 것 사용. 신규 컴포넌트·유틸 0 | ✅ 재구현 없음 |
| FE 규율 | 중복·컨벤션 | diff 내 JSX 복붙 없음, Tailwind 토큰(`text-[12px]`·`mgray-*`·`mred-*`) 이웃 코드와 동일 | ✅ |
| FE 규율 | 접근성 | 제거 버튼 `aria-label={`${name} 제외`}`(`:498`), 사유 `role="alert"`(`:535`), 제목 `label htmlFor`(`:516`), input `aria-label="파일 선택"`(`:442`) | ✅ 회귀 없음 |

**확인 안 함 (이유 명시)**
- `npx tsc --noEmit` · `prettier --check` · 테스트 실행 — 브리프 §3 「테스트도 돌리지 마라(코디가 이미 8/8 확인)」 + `tools.md` 「상태를 바꾸는 명령 금지」. 구현 워커·코디 몫.
- 브리프 §4 가 든 콜사이트 4곳 중 `CanonicalTaskDetail.tsx` · `task-kanban.tsx` · `WbsGanttEmbed.tsx` 은 `onAddFile` prop 을 직접 넘기지 않는다(핸들러 정의 자리다). 전부 diff 밖 = 무변경이라 시그니처 검증은 실제 prop 소비자 3곳으로 갈음했다.
