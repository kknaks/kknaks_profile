# [frontend] WORK-005 검수 수정 — 기간 경계 · 칸반 데이터 범위 · WARN 6건

너는 **task-management `frontend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**네 Phase 3·4 는 핵심 축을 통과했다** — 세 진입점 훅 단일화, 낙관적 갱신 방향, 게이트 우회 없음.
**FAIL 2건은 둘 다 「실사용에서만 터지고 테스트로는 안 잡히는」 종류다.**

## 1. SSOT — 먼저 읽을 것

**검수 리포트 — 이번 작업의 출발점**
- `orchestration/work/docs-v1/work-005-review-report.md` — **F-1·F-2 행과 W-1~W-7 행을 그대로 읽어라**

**계약(2026-09-06 갱신 — 갱신분이 이번 수정의 근거다)**
- `para/projects/summer-star/task-management/20-spec/spec-004-tasks-status-views.md`
  — **§2 U-2 「데이터 범위」**(신설) · **§4 `statusCounts`·`unfilteredTotal`**(신설) · **U-4 정정 2건**(고스트·가이드선) · **§4 Case Matrix 같은 상태 전이 한 줄**(신설) · U-9
- `.../20-spec/spec-003-tasks-crud.md` — §4 상세 응답의 `isOverdue`·`overdueDays`(신설)
- `.../40-architecture/frontend/README.md` — **§1-2**(쿼리·뒤로가기) · **§3-6**(KST 변환은 `lib/datetime.ts` 하나) · §5-1 · §11
- `.../00-design/09-design-tokens.md` — **「현재 값 배경」·「드롭 플레이스홀더」 등재됨**

## 2. FAIL — 반드시 고칠 것

### F-1 — 기간 경계가 서버 계약과 다르다 **(먼저 고쳐라)**

**말일이 기한인 업무가 그 달 목록·칸반·`total`·`typeCounts` 어디에도 없다.**

`useTasksViewParams.ts` 의 `monthRange()` 가 `to` 를 **이번 달 마지막 날**로 보내는데,
서버는 끝 경계를 **열어 둔다**(`due_date < to_date`). 서버 자신의 기본값과 백엔드 테스트 헬퍼는
`to` = **다음 달 1일**을 보낸다 — **그래서 백엔드 테스트가 이걸 못 잡는다.**

같은 함수에 둘이 더 있다:

- **타임존 없는 날짜 문자열**(`"2026-08-01"`)을 보내 서버가 naive `datetime` 으로 파싱하고
  `.astimezone()` 이 **시스템 로컬**을 가정한다 — 컨테이너 TZ 에 따라 경계가 흔들린다
- **KST 달 경계가 아니라 UTC 달 경계**를 만들어, 기한 없는 업무의 `created_at` 축이 **9시간 어긋난다**
  (그 달 1일 00:00~09:00 KST 에 만든 무기한 업무가 빠진다 — T-1-a)

**고치는 방향** — `monthRange` 를 **서버의 `current_month_bounds()` 와 같은 규칙**으로:
① 끝을 **다음 달 1일**(배타) ② **KST 달 경계** ③ **UTC ISO(오프셋 포함)** 문자열.
기준 구현이 `task_service.py:current_month_bounds()` 와 `test_task_list.py:_month_bounds()` 에 **이미 있다.**

**재발 방지를 함께 넣어라** — 프론트 테스트가 이 축에 하나도 없다.
MSW 로 **「보낸 `from`·`to` 가 서버 기본값과 같은 형태인가」**를 한 줄 잡아 둬라.
**말일 기한 업무가 그 달에 잡히는지**도 테스트로 고정해라.

### F-2 — 칸반이 그 달 앞 12건만 그린다

목록 쿼리가 언제나 `size=12`·`page=1` 인데 **페이지네이션 UI 가 리스트 전용**이라,
칸반에서는 **13번째 업무부터 화면에 나타날 길이 없다.** 사용자는 그 달 업무가 12건뿐이라고 읽는다.
같은 뿌리로 완료 컬럼 헤더 「8월 12」가 **월 기준이 아니라 현재 페이지 안의 완료 수**다.

**SPEC 에 규격이 없어서 생긴 일이고, 코디가 정했다**(U-2 「데이터 범위」):

- **칸반은 페이지를 쓰지 않는다** — 그 달 전체를 한 번에 그린다. **`size` 상한은 500**
- **`total > 500` 이면** 보드 하단에 「이 달 업무가 n건이라 500건까지만 그립니다 · 리스트에서 보기」.
  **조용히 자르지 마라**
- 완료 컬럼의 「8월 12」와 하단 「8월 완료 12건」은 **`statusCounts.done`** 에서 온다.
  **받아온 카드를 세지 마라** — 상한에 걸리면 두 수가 갈린다

**백엔드 워커가 `statusCounts`·`unfilteredTotal`·`size` 상한 500 을 지금 같은 워크트리에서 만드는 중이다.**
먼저 붙으면 실물로, 아직이면 MSW 로 만들고 붙는 대로 확인해라.

## 3. WARN — 함께 고칠 것

- **W-1 Tailwind 관용구를 덮었다** — `extend.colors.current` 를 정의하는 순간 `text-current`·`fill-current` 의
  의미가 「상속색」에서 **`#F4F5FF` 고정**으로 바뀐다. shadcn `checkbox.tsx` 가 이미 영향을 받고 있고,
  지금은 둘 다 흰색에 가까워 **안 보일 뿐**이다. **이름만 바꿔라**(예 `pick`) — 값·규격은 그대로. 쓰는 자리는 넷뿐이다
- **W-2 뒤로가기가 안 산다** — 전부 `router.replace` 라 리스트↔칸반을 오간 뒤 뒤로가기를 누르면
  **이전 뷰가 아니라 페이지를 떠난다.** **뷰 전환만 `router.push`** 로 바꿔라(필터·기간까지 push 하면 히스토리가 시끄럽다).
  쿼리로 조건을 남기기로 한 이유 중 하나가 뒤로가기였다
- **W-4 칸반 취소 카드에 취소일이 없다** — 서버가 `cancelledAt` 을 **이미 내려주는데**(리비전 `0003` 을
  추가한 근거 둘 중 하나다) 프론트에서 읽는 코드가 0건이다. `lib/datetime.ts` 의 포맷으로 한 줄 더해라
- **W-6 빈 상태 캡션이 규격 문구가 아니다** — 「더 많은 업무가」가 아니라 **「n건이」**다.
  `n` 은 **`unfilteredTotal`**(백엔드가 만드는 중)에서 온다
- **W-7 날짜 변환이 `lib/datetime.ts` 밖에 있다** — `currentMonth`·`monthRange`·`shiftMonth`·`formatMonth`
  넷을 옮기고 **KST 기준으로 통일**해라. `currentMonth()` 가 **디바이스 로컬**을 쓰는데 서버는 KST 다.
  **F-1 을 고치면서 같은 파일을 만지니 함께 해라**

### W-3·W-5 는 고치지 마라 — **SPEC 을 낮췄다**

검수가 「코디 판단일 수 있다」고 올린 둘을 **규격에서 뺐다**(SPEC-004 U-4, 커밋 `5a56b06`):

- **드래그 고스트는 브라우저 기본을 쓴다.** 그림자를 강제하려면 복제 노드를 `setDragImage` 로 넘겨야 하는데
  **macOS·Windows 에서 다르게 그려진다** — 둘 다 배포 대상이다. **회전 없음만 규격**이다
- **삽입 가이드선은 두지 않는다.** 카드 순서를 저장하지 않으므로 가이드선은 **저장되지 않는 위치를 약속하는 표시**가 된다 —
  놓고 나면 서버 정렬대로 다른 자리로 가서 사용자가 「안 먹었다」고 읽는다

**네 구현이 이미 그 상태다.** 확인만 하고 넘어가라.

## 4. allowed_paths

- `app/front/` — 전부

**`app/back/` 을 건드리지 마라**(BE 워커가 같은 워크트리에서 응답 필드를 만드는 중이다).
문서 레포도 **읽기 전용**이다. **커밋·push·PR 하지 마라.**

## 5. 검증

```
cd app/front && npx tsc --noEmit + npm test. 정적 빌드 제약 자기점검(지난번 8항목 그대로). 전체 빌드 금지, 검증은 1회만
```

**앱 창에서 실물로 확인하고 수치를 보고해라:**

1. **이번 달 마지막 날**을 기한으로 업무를 만들고 `/tasks` 를 연다 → **목록·칸반·하단 카운트에 잡히는가**
   (고치기 전엔 안 잡혔다 — 전/후를 수치로)
2. 한 달에 **업무 13건 이상**을 두고 `?view=board` → **전부 보이는가**
3. **완료 컬럼의 수**가 `statusCounts.done` 과 같은가 — `size` 를 작게 만들어도 **월 기준 수가 유지되는가**
4. 리스트↔칸반을 오간 뒤 **뒤로가기가 이전 뷰로 가는가**
5. 칸반 취소 카드에 **취소일**이 보이는가
6. 필터로 0건을 만들면 캡션이 **「… n건이 보입니다」**로 실제 수를 적는가

**칸반 DnD 드롭의 네트워크 캡처는 여전히 미완으로 둬라** — macOS 네이티브 드래그 세션 문제라 네 잘못이 아니다.
**갈음하지 마라.** 사람이 한 번 확인할 몫으로 남긴다.

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 6. 질문하는 법 — **`orca orchestration ask` 를 쓰지 마라**

```bash
orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[질문] frontend: <질문>" --enter
```

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

**커밋·push·PR 하지 마라.**
