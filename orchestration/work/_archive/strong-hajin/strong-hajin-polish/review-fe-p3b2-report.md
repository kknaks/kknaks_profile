# 리뷰 리포트 — strong-hajin-polish / Phase 3b 재검수 (fix1 + 채팅 created_at) (2026-10-01)

## 판정: WARN

**앞 검수의 FAIL 1 · WARN 5가 모두 닫혔다. 새 FAIL은 없다. 새 WARN 3(경미)과 참고 2를 남긴다.**
- FAIL-1(참고 업무 유실): 목록이 오기 전 · 조회 실패 · 목록에 없는 id, 세 경우 모두 초안 값을 그대로 싣는다. 테스트 3건이 직접 확인한다.
- 되살린 자료 첨부는 예전 `ActionTaskCard` 피커와 같은 API · 같은 규칙이다. 등록(창 · 카드 둘 다)이 그 초안 id를 싣는다. 예외 하나: 업로드 중 페이지 이탈 가드가 빠졌다(N-1).
- 채팅 `created_at`: BE는 tz가 붙은 ISO 8601이고, 봉투 값과 같다. FE는 서울 날짜로 센다. 형식이 맞는다.

## 검수 범위
- 대상: HEAD `4a89650` 위 미커밋 전체. frontend 수정 13 + 신규 2(`AxDraftCard.tsx` · `.test.tsx`), backend 4, `docs/unified-operations-inventory.json`.
- 기준: `review-fe-p3b-report.md` · `strong-hajin-polish-fe-p3b-fix1-brief.md` · `strong-hajin-polish-be-p3b-brief.md`(+ redo) · WP Phase 3b · SPEC-002 §2.4 · §2.9 · SPEC-001 U-2 · S-9
- 실행한 검사
  - diff 정독. 예전 `ActionTaskCard.tsx:300-440 · :700-745`와 한 줄씩 대조
  - 직렬 vitest(`--no-file-parallelism`)
    - `AxDraftCard` · `ActionTaskCard` · `TodayPage` · `MyWorkPage` · `CreateWork`: 133개 중 129개 통과
    - 실패 4건은 `CreateWork.test.tsx` 시작일 테스트다. 앞 검수와 같은 기준선 날짜 의존이다(`flaky-baseline-evidence.md`).
    - `features/chat` · `App`: 99/99 통과
  - `npx tsc --noEmit`: 0 오류
  - 실행하지 않은 것
    - **백엔드 테스트.** `make test-unit` · `make test-contract`는 병렬이라 이번 발주의 「직렬만」 조건에 맞지 않는다. BE 워커 보고에 맡긴다.
    - `make frontend-build`

## 1. 닫힘표

| 앞 지적 | 결과 | 근거 |
|---|---|---|
| **FAIL-1** 참고 업무 유실 | **닫힘** | `WorkModals.tsx:4570` `presetReferenceIds`, `:4601` `unplacedReferenceIds`(목록이 null이거나 목록에 없는 프리셋 id). `:4838` 제출 값 = 표에 선 것 ∪ 표에 못 선 프리셋. `:4660` 목록이 오면 표에 세운다(사람이 이미 고른 게 있으면 덮지 않는다). 사람이 표에서 체크를 풀면 그 id는 `unplaced`에도 없다. 그래서 「빼기」가 지켜진다. 테스트 `AxDraftCard.test.tsx:304`(보류) · `:311`(실패) · `:318`(목록 밖) |
| FAIL-1 「비동기로 채워지는 칸」 전수 | **다른 칸 없음(재확인)** | 상위 · 프로젝트 · 참조자 · 결재자 · 선행 · 담당 · 시작일 · 기한 · 체크리스트는 모두 `initial`에서 `useState`로 바로 선다. `CreateWorkModal` 안의 effect 두 개(`getTasks` · `listProjects`)는 위 상태를 쓰지 않는다. `listProjects`는 `availableProjects`만 바꾼다. 그래서 프로젝트 값은 남고, 이름만 늦게 붙는다 |
| **WARN-1** 자료 첨부 입구 | **닫힘**(N-1 하나 남음) | 아래 §2 대조표 |
| **WARN-2** 96px 잘림 | **닫힘** | `ax.css:632` `height:calc(6 줄 × caption1 크기 × 줄높이 + 5 × space-100 + 2 × space-200)`. `--t-caption1-lh:1.334`(`typography.css:15`)는 단위 없는 값이라 calc가 성립한다. 기본 정보의 행은 다섯 개다(내용은 2줄 clamp라 실제 6줄). 틈은 4개면 되지만 5개를 넣어 4px 여유가 있다. `dd`는 한 줄 말줄임(`:637`), 내용은 2줄 clamp(`:638`). 모든 페이지가 같은 높이다. **화면 확인은 E2E로 남긴다**(jsdom은 레이아웃을 재지 않는다) |
| **WARN-3** 채팅 「만든 지 며칠」 | **닫힘** | §3 |
| **WARN-4** 결재자 이름 없음 | **닫힘** | `WorkModals.tsx:5171` 후보에 `approverOptions`를 id 중복 없이 합친다. `AxDraftCard.tsx:390` `people(contract, "approver_id")`. 테스트 `:401` |
| **WARN-5** Phase 2 잠금 잔여 | **닫힘(이미)** | `TodayPage.tsx:124` · `MyWorkPage.tsx:376`. 진입 · 셸 refresh · 쓰기 뒤의 어떤 `reload` 든 성공하면 `setTodayFresh/WorkFresh(true)`(커밋 `1ef8db0`). `AxDraftModal locked={!todayFresh}`(`TodayPage.tsx:437`) · `{!workFresh}`(`MyWorkPage.tsx:1346`)가 그 플래그를 쓴다 |

## 2. 되살린 자료 첨부 ↔ 예전 `ActionTaskCard` 규칙

| 규칙 | 예전 `ActionTaskCard` | fix1(`WorkModals.tsx` axDraft 분기) | 결과 |
|---|---|---|---|
| 파일 → 판단 항목 자료 초안 | `stageActionMaterialFile`(`:415`) | `stageAxFile` → `stageActionMaterialFile(axDraft.actionId, file)` | 같음 |
| 링크 → 자료 초안 | `stageActionMaterialLink`(`:400`). URL · 이름이 비면 막음(`:934`) | `stageAxLink`. 단추가 `url.trim() && label.trim()`일 때만 열림 | 같음 |
| 빼기 = 서버에서 버림 | `discardActionMaterialDraft`(`:429`) | `discardAxMaterial` | 같음 |
| 업로드 중 · 실패가 남아 있으면 확인 막기 | 업로드 중이면 단추 비활성(`:511` · `:573`). 실패 행은 `incompleteMaterial` | `:5241` `axUploadPending`(업로드 중 + 실패 모두)이면 [등록] 비활성. 실패 행은 X로 뺀다 | 같음(더 엄격) |
| 확인이 싣는 id | `state === "staged"`만(`:561-562`) | 창 `:4867` · 카드 `AxDraftCard.tsx:225` 둘 다 `state === "staged"`만 | 같음 |
| 붙인 즉시 서버에 남음 → 카드에 반영 | 카드 자체 상태 | `onMaterialsChange` → 카드 `setMaterials`(`AxDraftCard.tsx:218-220 · :389`). 자료 페이지 숫자가 따라간다. 테스트 `:333` · `:355` | 같음 |
| **업로드 중 페이지 이탈 가드** | `useBrowserOperationGuard(uploadingMaterial)`(`:327`) | **없음** | **다름 → N-1** |
| 빼기 X의 조건 | `state === "staged"`일 때만(`:725`) | 모든 행(`:5727`) | 차이는 있지만 무해. pending 초안의 자료는 늘 staged다. claimed는 확인 뒤에야 생기고, 그때 카드는 이미 접혀 있다 |

**등록에 실리는가**: 실린다.
- 창의 [등록]: `axDraft.onSubmit(draft, staged ids)` → `confirmPayload(draft, attachmentIds)` → `attachment_draft_ids`(`AxDraftCard.tsx:243-247 · :393-395`)
- 카드의 [등록]: `confirmPayload()` 기본값이 카드 `materials`의 staged다. 창에서 붙인 것도 여기에 들어 있다(테스트 `:355`).

## 3. 채팅 `created_at` — BE ↔ FE

- **BE**
  - `platform/actions.py:557-558`: 채팅 뷰에 `created_at`을 싣는다. tz가 없으면 UTC로 보고 `isoformat()`
  - `platform/action_center.py:759`: 봉투도 같은 보정을 한다(3a는 tz 없는 값을 낼 수 있었다 — 이번에 함께 고침)
  - `result_contracts.py:92-93`: `ActionProposalResult.created_at: str`. 이 TypedDict를 만드는 곳은 `actions.py:519` `view()` 하나뿐이다(grep). 빠진 생산자는 없다
  - 테스트 `tests/contract/test_action_center.py:843-857`
    - 대화 조회 action의 `created_at`이 tz 포함 ISO인지 본다
    - 그 값이 봉투 값과 같고, 제안 응답 값과도 같은지 본다
  - inventory diff는 `created_at` 항목만이다. 61곳 × 같은 5줄(속성 + required)이고, 다른 줄은 0
- **FE**
  - `viewModels.ts` `ActionItem.created_at?: string | null`(선택)
  - `axDraftFromAction`(`AxDraftCard.tsx:79`)이 받아 `axDraftAgeDays` → `isoDateInSeoul`(`new Date(iso)` → `Asia/Seoul` 날짜)로 센다. tz가 붙어 있어서 브라우저 현지 시간대와 상관없다
  - 값이 없으면 줄을 세우지 않는다(`:346`). 테스트 `:386`
- **형식이 맞는다.**

## 4. 새 지적 (fix1이 만든 것 · 조용히 통과하는 자리)

### N-1 (WARN) 창의 자료 업로드 중 페이지 이탈 가드가 없다
- 예전 피커는 업로드 중일 때 `useBrowserOperationGuard(uploadingMaterial)`로 새로 고침 · 이탈을 막았다(`ActionTaskCard.tsx:327`).
- 새 창(`WorkModals.tsx:4493-4538`)에는 그 가드가 없다. 큰 파일을 올리는 중에 새로 고치면 업로드가 조용히 끊긴다.
- 발주 「예전 `ActionTaskCard` 첨부 피커와 같은 규칙」(fix1 brief 2)과 어긋나는 한 자리다. `axUploads.some(!failed)`로 같은 훅을 부르는 한 줄이면 닫힌다.

### N-2 (WARN) 자료 초안 갱신을 state updater 안에서 부모에게 알린다
- `changeAxMaterials`(`WorkModals.tsx:4497-4503`)는 `setAxMaterials`의 updater 함수 안에서 `axDraft.onMaterialsChange(updated)`(= 카드의 `setMaterials`)를 부른다.
- React 규칙상 updater는 순수해야 한다. 앱은 `StrictMode`다(`main.tsx:7`). 그래서 dev에서는 updater가 두 번 돈다. 다만 값이 같아 결과는 같다.
- 같은 fiber에 앞선 업데이트가 쌓여 있으면 updater는 렌더 중에 돈다. `stageAxFile`은 바로 앞에서 `setAxUploads`를 부른다. 이때 「다른 컴포넌트를 렌더하는 중 업데이트」 경고가 날 수 있다.
- 이번 직렬 테스트 로그에서 그 경고는 **0건**이었다. 동작은 맞는다. 고친다면 새 배열을 먼저 계산하고, 두 setter를 따로 부르면 된다.

### N-3 (WARN · 경미) 표에 못 선 참고 업무는 창에서 뺄 수 없다. 조회 실패 때 문구도 어긋난다
- `unplacedReferenceIds`는 「읽을 수 없는 업무 N건 — 초안 그대로 함께 등록됩니다」 한 줄로만 선다(`:5638`). 뺄 단추가 없다.
- 그 id를 정말 읽을 수 없다면 서버가 거절한다. `_readable_tasks`의 「Anything else is refused rather than quietly dropped」(`modules/work/application.py:517-525`)다.
  - 그러면 창 [등록]과 카드 [등록]이 모두 실패하고, 사람이 고칠 길은 없다. 남는 길은 [거절]뿐이다.
- 그런데 AX 도구 계약이 「readable reference_task_ids」를 요구한다(`tool_catalog.py:546 · :648`). 그래서 실제로는 드물다. 흔한 경우는 「`getTasks(true)` 목록 밖이지만 읽을 수 있는 업무」이고, 이때는 그대로 성공한다.
- `getTasks`가 **실패**했을 때도 모든 프리셋을 「읽을 수 없는 업무」로 부른다. 사실과 다른 문구다(P-1 문면 위반은 아니다).
- 권장: 실패와 목록 밖을 문구로 가르고, 표에 못 선 id에도 「빼기」를 둔다. 코디 판단으로 넘긴다.

### 참고 (판정 밖)
- **R-1 창을 닫아도 자료는 남는다**
  - 「닫으면 버림」(§2.9)은 칸 값에만 걸린다. 자료는 고르는 즉시 서버의 자료 초안이 되어 남는다.
  - 예전 피커와 같은 규칙이고, 코드 주석과 테스트(`AxDraftCard.test.tsx:355`)가 의도로 못 박았다. 사용자 E2E에서 받아들여지는지 본다.
- **R-2 `projectCandidates`가 렌더마다 새 배열이다**(3b 원본 · `AxDraftCard.tsx:419`)
  - `CreateWorkModal`의 `listProjects` effect(`[projectCandidates]`)가 카드가 다시 그려질 때마다 돈다.
  - fix1부터는 자료를 붙일 때마다 카드가 다시 그려진다.
  - 계약의 `project_id.options`가 비어 있으면 그때마다 `listProjects`를 다시 부른다. 값은 잃지 않는다. 효율 문제다.

### 조용히 통과하는 자리
- N-1(이탈 가드)과 N-2(updater 부작용)는 테스트가 볼 수 없다.
- WARN-2의 실제 높이는 jsdom이 레이아웃을 재지 않아 테스트로 검증되지 않는다. E2E에 남긴다.
- 백엔드 contract 테스트는 이번 검수에서 직접 돌리지 않았다(위 「실행하지 않은 것」).

## 5. 사용자 E2E 목록 (갱신)

1. **채팅 → 카드**: 4칸 바 · 호버 ‹ › · 트랙패드 좌우 · ← →로 네 페이지를 넘긴다. 첫/끝에서 화살표가 사라지는지 본다.
2. **기본 정보 높이**(WARN-2 닫힘 확인): 기간 · 담당 · 내용 2줄 · 참조자 · 결재자를 다 채운 **요청** 초안에서 결재자 줄까지 보이는지 본다. 참조자가 길면 「…」로 줄여 보이는지 본다. 다른 페이지로 넘겨도 카드 높이가 그대로인지 본다.
3. **채팅 카드 「만든 지 며칠」**(WARN-3): 채팅 카드 아래에 「N일 전」류가 서는지 본다. 같은 초안을 홈 판단 대기에서 열었을 때와 같은 숫자인지 본다.
4. **[수정]**: 창이 초안 값으로 열리는지, 갈래 토글이 없는지 본다. 값을 하나 고쳐 [등록] → 업무가 서고 카드가 한 줄 + [업무 열기]로 접히는지 본다. 창을 닫으면 칸 값이 초안 그대로인지 본다.
5. **참고 업무**(FAIL-1 닫힘 확인): AX에게 참고 업무를 걸어 달라고 한다 → [수정] → 곧바로 [등록]. 만들어진 업무에 참고 연결이 남는지 본다. 연관 업무 탭에서 체크를 풀고 등록하면 빠지는지도 본다.
6. **결재자 이름**(WARN-4): 초안 결재자가 창의 결재자 칸에 이름으로 서는지 본다.
7. **자료 첨부**(WARN-1 되살림)
   - [수정] 창의 자료 탭에서 파일 하나 · 링크 하나를 붙인다. 카드의 자료 페이지 숫자가 바로 바뀌는지 본다.
   - 하나를 빼고 [등록] → 업무 상세에 남은 것만 붙었는지 본다.
   - 업로드 중에는 [등록]이 막히는지 본다.
8. **창을 닫아도 자료는 남음**(R-1): 자료를 붙이고 창을 닫는다 → 카드 자료 숫자는 그대로 남는다. 카드 [등록]이 그것을 함께 붙인다. 사용자가 이 동작을 받아들이는지 본다.
9. **업로드 중 새로 고침**(N-1): 큰 파일을 올리는 중에 새로 고치면 경고 없이 끊긴다. 받아들일지 본다.
10. **기한 없는 초안 [등록]**이 성공하는지 본다(P-1).
11. **홈 판단 대기**: 두 kind를 누르면 같은 요약 카드(작은 모달)가 뜨는지 본다. 등록 · 거절 뒤 목록에서 사라지는지 본다. 화면 진입 직후 잠금이 갱신 뒤 풀리는지 본다(WARN-5).
12. **업무 › 「AX 제안 N」**: 0건이면 「AX 제안 0」인지 본다. 켰을 때만 초안 줄이 서는지 본다. 줄 → 카드 → 등록 → 숫자가 줄어드는지 본다. 「전체」 · 다른 칩 · 수신함에는 없는지 본다.
13. **「SC AX」 문자열**이 화면 어디에도 없는지 본다. 다른 AX 카드(회의실 · 상태 변경 등)가 예전 모양 그대로인지 본다.

## 확인한 것
- FAIL-1 · WARN 1~5 닫힘 ✔(표 §1)
- 자료 규칙 대조 ✔(§2, 차이 1 = N-1)
- BE `created_at` tz · 단일 생산자 · inventory가 `created_at`만인 것 ✔
- `api.ts` 밖 fetch 0 · 새 의존성 0 ✔(새 호출은 모두 `lib/api`의 기존 함수)
- 직렬 vitest 228/232(실패 4 = 기준선) ✔ · tsc 0 ✔ · build · 백엔드 테스트 **재실행 안 함**
