# [reviewer] Phase FE-3 코드 검수

너는 **strong-hajin `reviewer` 워커**다. **앞 검수 워커는 죽었다 — 너는 맥락이 없다.**
먼저 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `rules.md`·`skills.md`·`tools.md`·`workflow.md`)
- `orchestration/work/strong-hajin-calendar/review-fe1-report.md` · `review-fe2-report.md`
  — **1루프 FE 검수가 무엇을 보았는지.** 그 규율이 회귀했는지가 이번 §6 이다

작업 워크트리(읽기 전용 검증용): `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar`


대상: 코드 워크트리의 **uncommitted diff** (수정 12, 전부 `frontend/`).
BE-4 는 커밋됐다(`434003c`). 리포트: **새 파일** `review-fe3-report.md`.
read-only. **테스트 돌리지 마라 — 내가 돌렸다.**

기준: SPEC-004 **v0.3.1** (`bfe299a`) · DEC-003 **증보 8~10** · WORK `Phase FE-3`.

## 코디가 확인한 것

- `frontend/` 밖 **0건**
- `make frontend-test` **929 passed / 0 failed** (기준선 914 → +15)
- `npx tsc --noEmit` **exit 0**

## 이 Phase 가 고친 것 셋 — **사용자가 실물에서 찾은 것들이다**

| | 증상 | 결정 |
|---|---|---|
| **K20** | 월 뷰에서 **같은 업무가 두 번** 뜬다(종일 띠 + 시간 배정) · 셀 안이 정렬 안 됨 | 월 뷰는 **종일 띠만**. 회의는 계속. **시간순 정렬** |
| **K21** | 겹치는 시간 블록이 **밑에 깔려 안 보인다**(09:30–12:30 안의 10:00–11:00 회의) | **나란히 그린다** |
| **K19** | 카드에 상태 배지가 없다 | **상태 배지 + 승인 배지 둘.** BE-4 가 `approval` 을 실어 준다 |

## 볼 것 여덟

1. **K20 이 실제로 닫혔나** — 월 뷰에 업무의 시간 배정이 **안 그려지나**. **회의는 그려지나**
   (회의는 그 자체가 일정이다 — 같이 빼면 과잉이다). 셀 안이 **시간순**인가.
   **주 뷰는 안 건드렸나** — 거기는 종일 칸과 시간 격자가 이미 나뉘어 있다.
2. **K21 이 그리기만 고쳤나** — **이미 겹쳐 있는 것은 여전히 그려져야 한다.**
   나란히 배치가 **막는 것**으로 번지면 FAIL(그건 서버 몫이고 이미 BE-3·BE-4 가 한다).
   종일 띠의 `packLanes` 를 깨지 않았나.
3. **K19 가 기존 어휘를 재사용하나** — `derivedApprovalLabel` 과 업무 화면
   (`features/work/WorkTables.tsx:197`)의 방식을 쓰나. **새 라벨·새 톤을 만들었으면 지적하라** —
   업무 화면과 캘린더가 같은 상태를 다르게 말하게 된다.
4. **`approval` 네 값을 다 다루나** — `null`·`awaiting_review`·`awaiting_revision`·`approved`.
   빠진 값에서 `undefined` 가 화면에 새지 않나.
5. **격자는 여전히 상태를 안 말하나** — 배지는 **좌측 카드**만. 격자는 유형 둘(업무/회의)로만.
6. **1루프 규율이 회귀하지 않았나** — 이게 중요하다. 전부 검수를 지난 것들이다:
   - **`span_from`·`span_to` 로만 그린다**(K14). `start_date`/`due_date` 로 그리는 자리가 생겼나
   - **한 화면 = 한 요청** — 탭 전환에 재조회가 없나
   - **레일과 격자가 같은 범위**(K18) — 월 뷰면 그 달
   - `api.ts` 밖 `fetch` 0건
7. **FE-4 를 당겨 하지 않았나** — 겹침 **거절 문구** · 업무 탭 레일에 회의 ·
   「업무 만들기」 단추는 **다음 Phase** 다. 들어와 있으면 Phase 경계 위반.
8. **조용히 통과하는 자리** — 테스트가 **+15** 건 늘었다. 그중 **공회전하는 것**이 있나
   (픽스처에 겹치는 블록이 없는데 「나란히 그린다」를 단언한다든지). 기존 테스트 약화 0건인가.

## 판정

FAIL 은 계약과 다른 것이 도는 자리·Phase 경계 위반·회귀에만.
WARN 은 **FE-4 브리프에 실을지**를 적어라.

## 보고

```bash
orca terminal send --terminal term_a9d49810-1ce8-4885-8c5f-b93200c501ac \
  --text "[worker_done] reviewer FE-3 검수 완료 — <판정과 한 줄>" --enter
```
