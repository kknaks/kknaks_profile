# WORK-002 v2 frontend — 재검수 N-1 최소 정정

- 작성: `@sc-ax-fe` (task `task_e503bfc50829` · dispatch `ctx_9b4a05af97e3`)
- 범위: **N-1 하나.** 다른 지적·보고서 재작성 없음. 커밋·push·PR 없음. BE·SPEC·WORK 미접촉.

## 무엇이 틀렸나

fix1 이 제안 게이트를 서버의 `_is_request_owner`(`requester_id` **또는** `promoted_by_member_id`)로
맞추면서, **재개도 같은 값을 쓰게** 했다. 그런데 서버는 그 둘을 **다른 함수로** 판정한다.

| 명령 | 서버 판정 | 받는 값 |
|---|---|---|
| 취소·조건 변경 제안 | `_is_request_owner` | `requester_id` **또는** `promoted_by_member_id` |
| **재개** | `_require_may_reopen` → `_requester_of` | **`requester_id` 하나뿐** |

회의 승격 요청은 `requester_id` 가 `system:meeting` 이라 **사람 id 와 같아지는 일이 없다** —
누른 사람에게도 재개는 언제나 거부된다. 한 값으로 묶어 그리면 그 사람에게 **누를 때마다 403 인 단추**가 섰다.

## 고친 게이트 (정확히 두 자리)

1. `workRows.ts` — `isRequestRecordRequester(request, personaId)` 추가:
   `request.requester_id === personaId` **하나만** 본다. 기존 `isRequestOwner`(두 항)는 **그대로 둔다**.
2. `WorkModals.tsx` — 재개 조건의 요청자 항만 좁은 값으로 바꿨다:
   `reviewed ? viewerIsRequester : viewerDrives` → `reviewed ? viewerIsRecordRequester : viewerDrives`.
   새 prop `viewerIsRecordRequester`(기본 `false`)를 `MyWorkPage` 가 같은 요청 행에서 채운다.

**제안 게이트는 fix1 정정 그대로다.** 본인 업무·기존 배정의 재개(`viewerDrives`)와
오늘·캘린더 경로(`personaId` 를 넘기지 않는 화면)도 손대지 않았다.
**서버 입력도 역량도 바꾸지 않았다** — 화면 노출만 좁혔다.

## 미결 보존

- 이 정정은 **OQ-206(승격 요청의 완료 확인자·재개자)의 결정이 아니다.** 지금 서버가 여는 만큼으로
  노출을 맞춘 것뿐이고, **그 미결을 닫지 않는다.** 서버가 그 자리를 열면 이 판정도 함께 넓힌다.
  코드 주석에도 같은 말을 적어 두었다.
- 목적은 「과거 데이터가 있어도 **항상 실패하는 단추를 내지 않는 것**」이다.

## 검증

| 명령 | exit | 결과 |
|---|---|---|
| `make frontend-test` | **0** | **53 파일 · 706 테스트 전부 통과** |
| `cd frontend && npx tsc --noEmit` | **0** | 오류 0 |

직전 판이 704 였으므로 **+2 가 이번 회귀**다. 삭제·skip·단언 약화 0. **한 번에 통과해 재실행 없음.**
로그: scratchpad 의 `fix2-frontend-test.log` · `fix2-tsc.log` 와 각 `.exit`.
`make frontend-build` · 전체 `make verify` 는 코디 몫이라 돌리지 않았다. 브라우저 E2E 미실행.

### 더한 회귀 둘

- **승격 요청**(`requester_id = system:meeting`)의 누른 사람: **제안은 서고 재개는 서지 않는다.**
- **일반 요청**의 요청자: **재개가 그대로 선다** — 좁힌 것은 승격 갈래뿐이다.

기존 회귀(요청자/담당자/제3자/본인·배정/수락 전 요청/`personaId` 없는 화면)는 그대로 통과한다.

## 변경 파일

- `frontend/src/features/work/workRows.ts`
- `frontend/src/features/work/WorkModals.tsx`
- `frontend/src/features/work/MyWorkPage.tsx`
- `frontend/src/features/work/TaskLifecycleV2.test.tsx`
