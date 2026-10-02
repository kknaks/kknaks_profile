# 리뷰 리포트 — strong-hajin-polish / frontend Phase 3b (2026-10-01)

## 판정: FAIL

**FAIL 1 · WARN 5.**
- 와이어프레임과 SPEC-002 §2.9의 항목은 대부분 코드로 맞게 섰다.
  - 4칸 바 · 호버 화살표 · 스와이프 · 키보드 · 빈 페이지 · 등록/거절/수정 · 접힘
  - 갈래 고정 · 모달 제출 = confirm+draft · 닫으면 버림
  - 칩 0건 · 칩 자리 · 켰을 때만 초안 줄 · 수신함 미혼입 · 홈 카드
- 다만 **「수정」 창이 초안의 참고 업무(`reference_task_ids`)를 조용히 잃을 수 있다.** P-1(필드를 잃지 않는다)에 걸린다.

## 검수 범위

- `frontend/` 미커밋 변경(HEAD `4a89650` 위). 수정 13개 + 신규 2개(`features/action/AxDraftCard.tsx` · `.test.tsx`). `backend/` · `src-tauri/` 변경은 0이다.
- 기준: WP Phase 3b · P-1 · P-2 · P-3 / SPEC-002 §2.4 · §2.9 · S-7 · §6 / SPEC-001 U-2 · S-9 · §6 / `strong-hajin-polish-fe-p3b-brief.md` / `review-be-p3a-report.md`
- 실행한 검사
  - diff 정독
  - grep: `SC AX` · `CreateWorkModal` · `axDraft` · `ownerName` · 토큰 정의
  - 직렬 vitest: `AxDraftCard` · `ActionTaskCard` · `TodayPage` · `MyWorkPage` · `CreateWork` · `ChatDrawer` · `App` → 215 중 211 통과
    - 실패 4는 `CreateWork.test.tsx` 시작일 4건이다. 기준선 날짜 의존과 같다(`flaky-baseline-evidence.md`).
  - tsc · build는 다시 돌리지 않았다(워커 보고).

## 1. 계약 대조 (SPEC-002 §2.9 · WP 3b)

| 항목 | 결과 | 근거 |
|---|---|---|
| 배지 「AX」 · 「초안 · N회차」 · 종류 · 제목 | PASS | `AxDraftCard.tsx:295-301` · 라벨 `labels.ts` `axDraftCard`. 「SC AX」 노출 0(`ActionTaskCard.tsx:467` · `:934` placeholder까지 고침. grep 0) |
| 4칸 바(현재 칸 검정, 누르면 이동) · 현재 페이지 이름 | PASS | `:302-315` · `ax.css` `__step--on{background:--scax-color-ink}` |
| 본문 = 탭 넷 읽기 전용 요약, 1:1, 빈 페이지 「없음」 | PASS(모양은 WARN-2) | `PageBody` `:127-192`. 기본 정보 · 체크리스트 「N개 · 첫 항목」 · 업무 연결 「상위 · 프로젝트 · 참고 N · 선행 N」 · 자료 「파일 N · 링크 N」 |
| 호버 때만 ‹ ›, 첫/끝에서 숨김, 본문 위 겹침 | PASS | `:325-335`(첫/끝 조건부 렌더) · `ax.css` `__nav{opacity:0}` + `__body:hover/:focus-within` |
| 트랙패드 스와이프 · ← → | PASS | `onWheel` `:254-264`(가로 우세 · 40px 누적) · `onKeyDown` `:243-251`. 테스트 `:82` |
| 높이 고정 | PASS(내용 잘림은 WARN-2) | `ax.css` `__body{height:96px;overflow:hidden}` |
| [등록] = 초안 그대로 확인 · [거절] = 기존 거절 | PASS | `:365-368` `confirmPayload()`(draft 없음, 자료 초안 id 동봉) · `:341-350` |
| [수정] = 「새 업무 추가」 창 그대로 | PASS | `:372-413` `CreateWorkModal`에 `axDraft` + `initial`. 새 폼 없음 |
| 갈래 고정 | PASS | `WorkModals.tsx` `useState(axDraft ? axDraft.kind : …)` · 토글 `!axDraft` 조건 · `canCreateTask/Request`를 kind 하나만 참으로 |
| 모달 제출 = confirm + draft, 새 업무를 따로 만들지 않음 | PASS | `WorkModals.tsx` `if (axDraft) { … await axDraft.onSubmit(draft); return; }`. 생성 API 호출 전에 반환한다. 테스트 `AxDraftCard.test.tsx:186` |
| 닫으면 버림 | PASS | `onClose={() => setEditing(false)}`. 다시 열면 `initial`이 초안 값으로 새로 선다. 테스트 `:214` |
| 등록 뒤 한 줄 요약 + [업무 열기] | PASS | `:266-285` |
| 「만든 지 며칠」 | 홈 · 칩 PASS / **채팅 WARN-3** | 봉투 `created_at`(`axDraftFromEnvelope`) · 채팅은 `createdAt: null`(`:78`) |
| 홈 판단 대기 카드 클릭 → 같은 카드 | PASS | `TodayPage.tsx` `AxDraftModal`(편집 계약이 없는 옛 봉투는 기존 드로어) |
| 「AX 제안 N」 칩: 하나만 켜짐 · `받은 요청` 바로 뒤 · `기한 지남` 맨 끝 · 0건 표시 | PASS | `labels.ts` `myWorkChips = [all, awaiting_acceptance, ax_drafts, open, in_progress, overdue]` · 라벨 `{label} {count ?? 0}`(`MyWorkPage.tsx:1137`) · `mineCounts.ax_drafts = axDrafts.length` |
| 켰을 때만 초안 줄, 전체 · 다른 칩 · 수신함 미혼입 | PASS | `workRows.ts` `matchesChip(ax_drafts) → false` · `activeChip === "ax_drafts"`일 때만 `AxDraftTable` · 수신함 경로는 그대로(기존 단언 유지) |
| 초안 줄 = 업무 행 열 틀(요청자 「AX」 · 상태 「초안」 · 만든 지 며칠 · 액션 비움) | PASS | `WorkTables.tsx` `AxDraftTable` |
| 자동 만료 없음 | PASS | 만료 처리 코드 없음 |
| Phase 2 규칙(기억한 봉투로 명령 안 엶) | PASS | `locked={!todayFresh}` · `locked={!workFresh}` · `axDrafts`는 `useRemembered("work.axDrafts")`. 단, Phase 2 재검수 WARN-A(진입 갱신이 실패하면 계속 잠김)가 이 두 자리에도 이어진다 |
| envelope · `api.ts` 밖 fetch 0 | PASS | 명령은 `runActionCommand`(api.ts)와 기존 채팅 `onDecide`. 단추는 `allowed_commands`(`confirm` · `reject`)에서, [수정]은 편집 계약(`editable`)에서 선다 |
| 다른 AX 카드 불변 | PASS | `MessageList.tsx`: `axDraftFromAction`이 참일 때만 새 카드. 나머지는 기존 `ActionTaskCard` 등 그대로 |

## 위반 (FAIL)

### FAIL-1 「수정」 창의 등록이 초안의 참고 업무를 지울 수 있다 (P-1)

- 창이 보내는 draft는 `reference_task_ids: reference_task_ids ?? []`다(`WorkModals.tsx` axDraft 분기). 그 값은 **`linkedTasks` 상태**에서 나온다.
- `linkedTasks`는 처음에 비어 있고, 마운트 effect가 `getTasks(true)`를 받은 **뒤에야** 초안 id로 채운다(`WorkModals.tsx:4575-4592`, `preset.includes(row.task_id)`).
- 그래서 아래 셋에서 AX가 고른 참고 업무가 **빈 배열로 덮인다.** 초안 값(`baseValues`)을 펼친 뒤 이 키를 다시 쓰기 때문에, 초안 값은 살아남지 않는다.
  1. **목록이 오기 전에 등록**: 창을 열자마자 [등록]. 내 업무 · 홈 진입이 여러 콜이고 서버 N+1이 남아 있어 수백 ms 창은 실제로 있다.
  2. **`getTasks` 실패**: `catch`가 `setReferenceChoices([])`만 하고 `linkedTasks`를 채우지 않는다.
  3. **초안이 고른 업무가 `getTasks(true)` 결과에 없을 때**: 걸러져 빠진다.
- 사람은 창에서 참고 업무를 건드리지 않았는데 결과 업무에는 참고 연결이 없다. 서버는 이것을 「사람이 고친 값」으로 받아 회차 2와 diff로 남긴다.
- 테스트는 이 경로를 보지 않는다. `AxDraftCard.test.tsx:186`의 초안은 `reference_task_ids: []`다(`:26`).
- **권장**
  - 참고 업무 목록이 오기 전에는 `baseValues.reference_task_ids`를 그대로 보낸다.
  - 목록에 없는 초안 id는 버리지 않고 남긴다(표에는 「읽을 수 없는 업무」로 세우거나, draft에만 싣는다).
  - 테스트: `getTasks`를 보류하거나 실패시킨 채 [등록] → draft의 `reference_task_ids`가 초안과 같다.
- 같은 모양의 위험을 다른 칸에서도 찾아봤다. 상위 · 프로젝트 · 선행 · 참조자 · 결재자 · 담당은 `initial`에서 상태로 **바로** 서서 비동기 의존이 없다. 참고 업무만 해당한다.

## 경미 (WARN)

- **WARN-1 (워커 미결 ①) 채팅에서 AX 초안에 자료를 붙이던 입구가 사라졌다 — 기존 기능 회귀**
  - 예전 두 kind 카드는 `ActionTaskCard`의 첨부 피커(`stageActionMaterialFile` · `stageActionMaterialLink`)로 확인 **전에** 자료를 붙일 수 있었다.
  - 이제 카드는 요약만 하고, 수정 창 자료 탭은 읽기 전용이다(`WorkModals.tsx` axDraft 자료 fieldset). 두 kind는 확인 전 자료 첨부 길이 없다. AX가 붙인 자료는 그대로 간다(`attachment_draft_ids`).
  - SPEC과는 맞는다. SPEC-001 S-9 6 「자료는 생성 명령의 필드가 아니다 … 자료 첨부는 지금처럼 생성 뒤 단계다(U-6-b)」 · 발주서 §3-2 「못 쓰면 읽기 전용으로 두고 보고」. 그래서 FAIL이 아니다.
  - 그래도 사용자가 쓰던 기능이 줄었다. 등록 뒤 업무 상세의 「자료」에서는 붙일 수 있다. **사용자 E2E에서 확인받을 자리**다.
- **WARN-2 기본 정보 페이지가 96px에 들어가지 않으면 참조자 · 결재자가 보이지 않게 잘린다**
  - `ax.css` `.ax-draft-card__body{height:96px;overflow:hidden}`
  - 요청 초안에 기간 · 담당 후보 · 내용 2줄 · 참조자 · 결재자를 다 채우면 6줄(caption 약 18px × 6 + 간격 + 위아래 패딩)이라 약 130px가 넘는다. 끝의 **결재자(때로 참조자)가 표시 없이 잘린다.**
  - 1:1 요약 계약(§2.9 「기본 정보: … 참조자 · 결재자」)이 화면에서 깨지는 자리다. 줄 수 상한이나 「…」 표시 같은 모양 결정이 필요하다(DS-gaps).
- **WARN-3 (워커 미결 ②) 채팅 카드에 「만든 지 며칠」이 없다**
  - 채팅의 `ActionItem`에는 만든 시각 필드가 없다(`lib/viewModels.ts` `ActionItem`에 `created_at` 없음). 3a는 봉투(`GET /api/action-items`)에만 `created_at`을 실었다(`review-be-p3a-report.md` §4).
  - §2.9 표 「만든 지 며칠 | 만든 시각에서 센다」를 채팅 카드에서는 지키지 못한다. 대화 안이라 메시지 시각이 대신하지만 계약 문면과는 다르다.
  - 코디가 정할 일이다: (a) 채팅 뷰에도 `created_at`을 싣는 BE 한 줄, (b) 채팅은 예외로 SPEC에 적기.
- **WARN-4 (워커 미결 ③) 결재자 선택값이 창에서 이름 없이 보일 수 있다**
  - 창의 결재자 후보는 `ccCandidates`(+ 요청이면 `assigneeCandidates`)에서 만든다. 편집 계약의 `approver_id.options`를 쓰지 않는다(`AxDraftCard.tsx:377` · `:391`).
  - 초안의 결재자가 참조자 후보 밖이면 Select가 값은 들고 있지만 **라벨 없이** 서고, 사람이 그 값을 알아보지 못한다. 등록하면 값은 그대로 간다.
    - 업무 갈래: 결재자 ≠ 본인이고 참조자 후보는 본인 제외 전원이다. 그래서 거의 없다.
    - 요청 갈래: 결재자가 요청자 본인이거나 참조 후보 밖의 사람일 때 생긴다. SPEC-001 OQ-M(요청 결재자)이 열려 있는 자리라 실제 빈도는 낮다.
  - 권장: 결재자 후보에 `approver_id.options`를 합친다.
- **WARN-5 Phase 2 잠금 잔여(이어진 것)**
  - `AxDraftModal locked={!todayFresh}` · `locked={!workFresh}`는 진입 갱신이 실패하면 셸 새로 고침이 성공해도 풀리지 않는다(Phase 2 재검수 WARN-A).
  - 이번 diff가 만든 문제는 아니지만 AX 카드가 그 영향을 받는다.

## 2. 워커 미결 ①~④ 의견

| # | 미결 | 의견 |
|---|---|---|
| ① | 수정 창 자료 탭 읽기 전용 → 채팅 카드의 자료 첨부 입구 소실 | **SPEC · 발주서와는 맞고, 기존 기능 대비로는 회귀**(WARN-1). 사용자 결정이 필요하다: 등록 뒤 업무 상세에서 붙이는 것으로 충분한가, 아니면 카드나 창에 AX 자료 초안 추가(stage) 입구를 되살리는가. 되살린다면 창의 자료 탭에서 `stageActionMaterialFile/Link`를 부르는 게 가장 작다(API는 있다) |
| ② | 채팅 카드엔 만든 지 며칠 없음 | **계약 문면과 다르다**(WARN-3). BE에서 채팅 뷰에 `created_at`을 싣는 것이 가장 작다 |
| ③ | 결재자 후보가 편집 계약 options를 안 씀 | **실제로 생길 수 있다.** 다만 드물다(WARN-4). options를 합치는 한 줄로 닫힌다 |
| ④ | 채팅 거절은 옛 경로 | **문제없다.** 채팅 `onDecide`는 기존 `POST /api/actions/{id}/decide` 호환 경로다. 서버가 DecisionItem이 있으면 원장 경로로 보낸다(be-survey §1-1). 같은 항목이 바뀐다. 홈 · 칩은 원장 입구(`runActionCommand`)다. 두 표면 일치를 지킨다 |

## 3. 회귀 — 일반 「새 업무 추가」 5곳

- `CreateWorkModal`의 바뀐 자리
  - `axDraft` 분기
  - `initial`의 새 키 여섯(`startDate` · `projectId` · `ccIds` · `approverId` · `precedingTaskIds` · `referenceTaskIds`)
  - 상위 Select의 `&& !axDraft`
  - 제출 단추 라벨
  - 자료 탭 분기
- 일반 여는 자리 5곳(`CalendarPage:645` · `TodayPage:442` · `WorkModals:2997` · `MyWorkPage:1327` · `MeetingDetailPage:1289`)은 새 키를 넘기지 않는다. 모든 분기가 `axDraft`나 새 키가 있을 때만 갈린다. 그래서 **동작 불변**이다.
- Phase 1 B-02(담당 빈칸 시작 · 참조자 동적 제외)도 그대로다. `CreateWork.test.tsx`의 B-02 묶음이 통과했다.

## 4. 조용히 통과하는 자리 · P-2

- 참고 업무 비동기 손실(FAIL-1)은 테스트 초안이 빈 배열이라 통과한다.
- 96px 잘림(WARN-2)은 jsdom이 레이아웃을 재지 않아 테스트가 볼 수 없다.
- P-2: 새 토큰 0. 쓴 토큰(`--scax-radius-xs` · `--scax-focus-ring` · `--scax-space-100/150/200/600` · `--scax-color-line/ink/ink-assistive` · `--scax-text-caption1-size`)은 모두 정의돼 있다. 4칸 바 · 호버 화살표는 시안이 없는 자리라 DS-gaps에 적혀 있다(`ax.css` 주석).
- 화살표는 `opacity:0`으로만 숨긴다. 보이지 않는 동안에도 그 자리를 누르면 넘어간다. 의도와 같은 결과라 해는 없다.

## 5. 화면 확인 · 사용자 E2E 후보

1. **채팅 → 카드**: 「KPI 설정 업무 만들어 줘」 → 높이 고정 카드. 4칸 바 클릭 · 호버 ‹ › · 트랙패드 좌우 · ← →(본문 클릭 뒤)로 네 페이지를 넘긴다. 첫/끝에서 화살표가 사라지는지 본다.
2. **기본 정보 잘림**(WARN-2): 참조자 · 결재자 · 내용 2줄을 다 채운 **요청** 초안에서 결재자 줄이 보이는지 본다.
3. **[수정]**: 「새 업무 추가」 창이 초안 값으로 열리고 갈래 토글이 없는지 본다. 값을 하나 고쳐 [등록] → 업무가 생기고 카드가 한 줄 요약 + [업무 열기]로 접히는지 본다. 창을 닫으면 카드가 초안 그대로인지 본다.
4. **참고 업무**(FAIL-1): AX에게 참고 업무를 걸어 달라고 한 초안을 [수정] → 곧바로 [등록]. 만들어진 업무에 참고 연결이 남는지 본다(현재 코드로는 빠를수록 빠진다).
5. **기한 없는 초안 [등록]** 성공(P-1).
6. **홈 판단 대기**: 두 kind 카드를 누르면 같은 요약 카드(작은 모달)가 뜨는지, 등록 · 거절 뒤 목록에서 사라지는지 본다.
7. **업무 › 「AX 제안 N」**: 0건이면 「AX 제안 0」. 켜면 초안 줄만 서고, 「전체」 · 다른 칩 · 받은 요청 수신함에는 없는지 본다. 줄 → 카드 → 등록 → 칩 숫자가 줄어드는지 본다.
8. **자료**(WARN-1, 사용자 결정): 초안에 자료를 붙일 길이 없어진 것을 사용자가 받아들이는지 본다.
9. **「SC AX」 문자열**이 화면 어디에도 없는지 본다.
10. **다른 AX 카드**(회의실 예약 · 업무 상태 변경 등)가 예전 모양 그대로인지 본다.
11. **채팅 카드 「만든 지 며칠」 없음**(WARN-3)을 사용자가 괜찮다고 하는지 본다.

## 확인한 것

- 전수(P-3): `SC AX` 노출 0 · `CreateWorkModal` 여는 곳 5 + AX 1 · 칩 정의 `labels.ts` 1곳 · action item을 그리는 곳(홈 `ActionItemCard` → `AxDraftModal`, 채팅 `MessageList`, 업무 칩 `AxDraftTable`) ✔
- `api.ts` 밖 fetch 0 · 새 의존성 0 ✔
- 직렬 vitest 211/215(실패 4 = 기준선) ✔ · tsc · build **재실행 안 함**
