# [frontend] WORK-006 검수 수정 — FAIL 1 · WARN 5

너는 **task-management `frontend` 워커**다. **네가 방금 만든 WORK-006 Phase 4~6 의 지적을 닫는다.**

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`). 커밋 `2d6319e` 가 네 것이다.

**검수 리포트** — `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/work/docs-v1/work006-review-report.md` **먼저 통째로 읽어라.**

## ⛔ 1. 닫을 것 — 6건 전부

### F-1 (FAIL) — Case Matrix 의 에러 뒤 후속 동작 3곳

SPEC-006 §4 Case Matrix 가 요구하는 **후속 동작**이 빠졌다. 인라인 문구는 있는데 그 뒤가 없다.

```
invalid_work_type   인라인 ✔  +  **유형 목록 갱신** ✗
invalid_project     인라인 ✔  +  **프로젝트 목록 갱신** ✗
not_found (목록)     토스트 ✔  +  **목록 갱신** ✗
```

**왜 필요한가** — 삭제된 유형·프로젝트를 고른 것이라 목록을 다시 받아야 사용자가 고를 수 있다. 갱신이 없으면 같은 실패를 반복한다.

### W-1 — 영역 사이 import 8건

`frontend/README.md` §2 규칙 4 「영역 사이 import 금지. 공유가 필요하면 `components/shared/` 나 `lib/` 로 올린다」.
**예외는 「업무·회의 드로어를 캘린더가 재사용」 하나뿐이고 이건 해당하지 않는다.**

```
features/meetings/components/MeetingCreateDrawer.tsx:37-38   → features/settings
features/meetings/hooks/useAgendaAutoSave.tsx:26             → features/settings
features/tasks 5건                                          → features/settings
```

**`lib/` 로 올려라.** `inlineErrorMessage` · `useRowFailures` · 프로젝트/유형 쿼리 훅이 대상이다.
**meetings 것만 고치고 tasks 를 두면 안 된다** — 같은 규약 위반이 두 영역에 남는다. **여덟 건 다 정리해라.**
**WORK-007·008 이 같은 훅을 또 가져오면 세 영역이 된다. 지금이 제일 싸다.**

### W-2 — 공용 팝오버가 업무 전용 `role` 을 필수로 강제

`components/shared/AttachmentPopover.tsx:28-32`. 회의 쪽이 **가짜 값**을 채워 넣고 있다
(`MeetingCreateDrawer.tsx:333` · `MeetingAttachmentsTab.tsx:58·:92`).

**공용은 두 영역의 공통 부분만 갖는다.** `role` 을 팝오버에서 걷어내고 **호출부가 클로저로 넘겨라**(리뷰어 권고).

### W-3 — `validation_error` 가 무조건 제목 칸으로 간다

`features/meetings/errors.ts:35-36` 이 `field: "title"` 로 고정돼 있다.
SPEC-006 §4 는 **「해당 컨트롤」**에 붙이라고 한다 — 「회의는 5분 이상 300분 이하여야 합니다」·「종료 시각은 시작보다 뒤여야 합니다」는 **일시 칸**이다.

**서버 응답의 필드를 보고 해당 컨트롤에 붙여라.**

### W-4 — 임의 글꼴 크기 `text-[NNpx]` 10건

`frontend/README.md` §5-1 「타이포 계단은 Tailwind 유틸 프리셋으로 고정하고 컴포넌트가 임의 크기를 쓰지 않는다」.

```
MeetingCreateDrawer.tsx:85(18) · :262 · :288(11)
MeetingAgendaList.tsx:84 · :101(11) · :141 …  (리포트에 전체 목록)
```

**프리셋으로 바꿔라.** 프리셋에 없는 크기면 `tailwind.config.ts` 에 **계단을 더하고** 쓴다 — 컴포넌트에 리터럴을 남기지 마라.
**twMerge 프리셋 등록도 함께 확인해라**(`lib/utils.ts` — 등록 안 하면 색 클래스와 만날 때 조용히 버려진다. 이 프로젝트에서 실제로 밟았다).

### W-5 — `v2_not_available` 이 토스트 문구로 매핑 안 됨

`features/meetings/errors.ts:52-53` 의 `default: null` 때문에 생성 드로어에서 「회의록을 만들지 못했습니다」로 나온다.
SPEC-006 §4: **`501 v2_not_available` → 「v2에서 제공됩니다」 토스트.**

## 2. 지킬 것

1. **`app/front/` 밖을 건드리지 마라**
2. **문서를 고치지 마라**
3. **커밋·push 하지 마라**
4. **위 6건 밖을 고치지 마라.** 리팩터 욕심 금지 — 발견하면 보고에 적어라
5. **W-1 로 `lib/` 로 옮길 때 업무 화면이 깨지지 않는지 테스트로 확인해라**(`tasks` 기존 테스트 전부 통과)

## 3. 검증 — **앱 창 E2E 는 하지 마라**

```bash
cd app/front && npx tsc --noEmit
cd app/front && npx vitest run
```

**F-1·W-3·W-5 는 테스트로 고정해라** — 에러 응답을 목으로 주고 ① 목록 재요청이 나가는지 ② 인라인이 어느 칸에 붙는지 ③ 토스트 문구가 무엇인지.

**W-1 은 grep 으로 0 을 보여라** — `features/*` 사이 import 0건.

## 4. Done Criteria

- [ ] F-1 세 자리에 후속 동작이 붙었고 **테스트로 고정**됐다
- [ ] `features/*` 사이 import **0건**(meetings·tasks 둘 다) — grep 결과를 완료 증거에
- [ ] `AttachmentPopover` 가 `role` 을 요구하지 않는다. 회의 쪽 가짜 값 0
- [ ] `validation_error` 가 **해당 컨트롤**에 붙는다
- [ ] `text-[NNpx]` **0건**. 프리셋을 더했으면 twMerge 등록도 했다
- [ ] `v2_not_available` → 「v2에서 제공됩니다」
- [ ] `tsc` 0 에러 · `vitest` 전부 통과(업무 화면 회귀 없음)
- [ ] `app/front/` 밖 변경 0 · 커밋 없음

## 5. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from term_8b12b881-8c71-479c-9249-3b9707ef40d2 \
  --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "WORK-006 검수 수정 완료" \
  --body "6건 각각 어디를 어떻게 고쳤나(파일:줄) / lib/ 로 올린 것 목록과 업무 화면 회귀 확인 / 새로 고정한 테스트 / grep 0 증거(features 사이 import · text-[NNpx]) / tsc·vitest 결과 / 고치다 발견했지만 범위 밖이라 안 한 것"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] WORK-006 검수 수정 완료. 상세는 인박스." --enter
```
