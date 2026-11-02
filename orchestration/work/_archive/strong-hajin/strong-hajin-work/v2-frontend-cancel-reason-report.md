# WORK-002 v2 frontend — 직접 취소 사유 입력 보완

- 작성: `@sc-ax-fe` (task `task_cc5a74c9b4de` · dispatch `ctx_91d1e89288bf`)
- 근거: SPEC-003 §4 API(직접 취소) · §4 Validation(`reason` 필수) · SPEC-001(취소 사유 필수 · `WORK_REASON_REQUIRED`)
- **확정된 계약의 누락 보완이다.** 새 정책도, 미정(OQ-203·OQ-206) 결정도 아니다.
- 커밋·push·PR 없음. `backend/` · SPEC · WORK 미접촉.

## 1. 수정 경로 전수

직접 취소를 부르는 FE 경로를 전수 검색했다(`"cancel"` · `transitionDirectTask` · `onTransition`).

| 자리 | 전 | 후 |
|---|---|---|
| **업무 상세 드로어의 「업무 취소」** (`WorkModals.tsx`) | `ConfirmModal` — **누르면 곧바로 취소**, 사유 없음 | `ReasonPrompt` — 사유 입력 → 공백 거부 → `{expected_version, reason}` |
| 내 업무 relay (`MyWorkPage.transitionTask`) | `reason` 을 이미 그대로 넘김 | 같음 + **성공 여부를 돌려준다** |
| 오늘 relay (`TodayPage.transitionTask`) | 같음 | 같음 |
| 캘린더 relay (`CalendarPage.transition`) | 같음 | 같음 |

**UI 진입점은 드로어 하나뿐이다** — 행 액션·칸반에는 취소 전이가 없고(`transitionFor` 에 없다),
오늘·캘린더는 같은 드로어를 연다. 그래서 한 자리를 고치면 세 화면이 함께 닫힌다.

**`window.prompt` 를 쓰지 않았다.** 막힘 사유·요청 거절·제안이 이미 쓰는 부품(`ReasonPrompt`)을
그대로 재사용해 입력·돌아가기·오류가 한 모양으로 읽힌다. **사유 문자열을 지어내거나 고정 문구로
채우지 않는다** — 사람이 쓴 값만 간다.

## 2. 실제 BE 입력과 대조

BE 소유 워커가 같은 통합 단위에서 확정·반영한 계약을 받아 **그대로** 맞췄다.

```
POST /api/tasks/{task_id}/cancel
  { "expected_version": number, "reason": string }   ← reason 필수
  누락·빈 문자열·공백뿐 → 422 · 앞뒤/중복 공백은 서버가 다듬어 저장 · max 4000자
  성공 200 → state='cancelled', cancel_reason='direct'
```

- FE 가 보내는 본문은 `transitionDirectTask` 의 `{ expected_version, reason }` 그대로다.
  **화면이 공백을 먼저 막으므로** 서버의 422 자리에 닿기 전에 멈춘다(이중 방어이고, 서버 판정이 정본이다).
- **`cancel_reason` 은 사유 텍스트가 아니라 취소의 «종류»** (`direct` 등)다. 사람이 쓴 문장은
  **진행 기록(활동·이력)** 에 실리고, 상세의 `TaskHistorySection` 이 그 줄을 이미
  `사유: {reason}` 으로 그린다 — **새로 만든 표시가 아니라 있던 자리에 값이 도착한 것**이다.
- 착수 시점에는 `cancel_task` 가 `TaskVersionInput`(`extra='forbid'`, 회차만)이라 FE 가 `reason` 을
  실으면 422 였다. 그 상태를 코디에 먼저 올렸고, BE 가 REST 모델·`TaskTransitionInput` 의
  `cancelled` 사유 보존·MCP/AX·이력까지 함께 고쳤다는 회신을 받은 뒤 맞췄다.
- `block` 은 그대로 `{expected_version, reason}`, `start`·`complete`·`resume` 은 사유를 받지 않는다 —
  FE 도 그 셋에는 사유를 싣지 않는다(기존 그대로).

## 3. 인수 조건 대조

| 인수 | 어떻게 |
|---|---|
| 누르면 바로 취소하지 않고 입력 자리가 열린다 | 확인 모달 → `ReasonPrompt`. 열린 시점에 **명령 0건**(회귀로 단언) |
| 공백 사유는 전송하지 않는다 | 보내기 단추가 비활성이고 제출 경로도 막힌다. `"   "` 입력에도 전송 없음 |
| 사용자가 쓴 사유와 **원 회차**를 보낸다 | `onTransition(current, "cancel", reason)` — `current.version` 그대로. 회귀가 인자를 열어 단언 |
| 서버 실패 시 입력 보존 · 오류 | relay 가 **성공 여부를 돌려주고**, `false` 면 자리를 닫지 않는다. 쓴 문장이 그대로 남는다 |
| 성공 시 기존 갱신과 취소 표시 | 기존 `reload()`·알림 경로 그대로. 취소 표시(`cancel_reason`)도 기존 투영 그대로 |
| 다중 클릭으로 중복 명령 없음 | `ReasonPrompt` 에 `pending` 잠금 — 세 번 눌러도 **명령 1회**(회귀로 단언) |
| 합의취소·재개·완료·생성첨부 회귀 유지 | 전량에서 그대로 통과 |

**권한 게이트는 한 줄도 바꾸지 않았다.** 수락된 요청 Task 에는 직접 취소 자리가 애초에 없고
(N-1 에서 닫은 자리) 「취소 제안」이 그 자리다 — 회귀로 다시 못박았다. 수락 전 권한도 새로 열지 않았다.
서버가 409 로 막는 경우에도 FE 는 **서버 메시지를 그대로** 배너에 낸다.

## 4. 변경 파일

| 파일 | 무엇 |
|---|---|
| `frontend/src/features/work/WorkModals.tsx` | 취소 확인 모달 → 사유 입력 · `ReasonPrompt` 가 결과를 기다리고 `pending` 으로 연타를 막는다 · `onTransition` 타입 확장 |
| `frontend/src/features/work/MyWorkPage.tsx` | `transitionTask` 가 성공 여부를 돌려준다 |
| `frontend/src/features/today/TodayPage.tsx` | 같음 |
| `frontend/src/features/calendar/CalendarPage.tsx` | `transition` 이 같음 |
| `frontend/src/features/work/WorkViews.tsx` | prop 타입만 넓힘(동작 변화 없음) |
| `frontend/src/features/work/TaskLifecycleV2.test.tsx` | 회귀 7건 |

## 5. 검증 (실제 exit · 로그 `/tmp/v2-fe-cancel/`)

| 명령 | exit | 결과 | 로그 |
|---|---|---|---|
| `make frontend-test` (1회차) | 2 | `3 failed \| 710 passed (713)` | `frontend-test.log` |
| `make frontend-test` (2회차) | **0** | **53 파일 · 713 테스트 전부 통과** | `frontend-test-2.log` |
| `npx tsc --noEmit` | **0** | 오류 0 | `tsc.log`(0바이트) |
| `make frontend-build` | **0** | `tsc -b` + vite build 성공 | `frontend-build.log` |

- 직전 판이 706 이었으므로 **+7 이 이번 회귀**다. 삭제·skip·단언 약화 0.
- **1회차의 3건은 내 변경과 무관하다.** `Checklist`(「자료 모으기 위로」) · `MyWorkPage`(「받은 요청 0」이
  아직 1 이 아니다) · `MeetingList`(「회의 생성」) — 셋 다 **값이 도착하기 전에 조회한** 것이고,
  같은 코드로 돌린 2회차에서 전부 통과했다. 검수가 이미 적어 둔 **시간 민감 테스트 부채**와 같은 성격이다
  (내 파일이 아니고 이번 allowed_paths 밖이라 손대지 않았다). **그 부채가 사라졌다고 주장하지 않는다.**
- 전량 반복은 **원인 판별이라는 근거가 있을 때 한 번만** 했다(1회차 3건이 내 탓인지 가르기 위해).
- 그 밖에 한 번 고친 것: 내가 새로 쓴 「수락된 요청 업무…」 회귀가 **앞선 테스트가 남긴 mock 구현**에
  기대고 있었다(`vi.clearAllMocks()` 는 호출 기록만 지우고 구현은 남긴다). 전제를 명시로 바꿨다.
- 브라우저 E2E **미실행**(사용자 몫). 전체 `make verify` 는 코디 몫이라 돌리지 않았다.

### 회귀 이름

`TaskLifecycleV2.test.tsx` → `직접 취소 — 사유를 받아 보낸다`

1. 취소를 누르면 곧바로 취소하지 않고 사유 입력 자리가 열린다
2. 공백뿐인 사유는 보내지 않는다 — 서버가 422 로 막는 것을 화면이 먼저 막는다
3. 사람이 쓴 사유와 «원» 회차를 그대로 보낸다 — 문구를 지어내지 않는다
4. 성공하면 입력 자리가 닫힌다
5. 서버가 거절하면 자리를 닫지 않고 쓴 사유를 그대로 둔다
6. 여러 번 눌러도 명령은 한 번만 나간다
7. 수락된 요청 업무에는 직접 취소 자리가 없고 취소 제안이 그 자리다

## 6. 남은 것

- **BE 최종 실물과의 대조는 «계약 문서» 수준까지다.** BE 워커가 확정 회신한 입력·검증·저장 위치를
  그대로 맞췄고 FE 회귀로 본문 모양을 고정했지만, **실제 REST 왕복은 통합 검증에서 닫힌다** —
  FE 단위 테스트는 `onTransition` 인자까지만 본다.
- 사유 텍스트의 **표시**는 상세의 활동·이력 줄이다. 그 줄이 실제 취소 사유를 담는지는
  **서버 응답이 있는 통합/E2E** 에서 눈으로 확인할 자리다.
- **OQ-203 · OQ-206 은 그대로 미결**이다. 이 수정은 그 둘과 무관하고 닫지 않는다.
- 위 시간 민감 테스트 부채(내 파일 아님)는 그대로 남아 있다.
