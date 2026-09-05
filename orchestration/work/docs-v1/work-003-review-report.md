# WORK-003 검수 리포트

- 검수 대상: `ffc544d`(BE Phase 1) · `8e17d0b`(FE Phase 2·3) — `git diff 533843e...HEAD` 기준 39파일 / +3770 −10
- 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1` · 작업 트리 clean(`git status --porcelain` 무출력, untracked 0)
- 판정 기준: DEC-001 · SPEC-002 · `40-architecture/{backend,frontend,database/domains/account}` · WORK-003
- 검수자는 **코드·문서를 하나도 고치지 않았고 테스트·빌드를 돌리지 않았다.**

---

## 판정 요약

| 층 | 판정 | 근거 |
|---|---|---|
| **정책**(DEC-001) | **PASS** | §3 필드(유형 = 종류·이름·색 / 프로젝트 = 이름·색) · **slug·영문명 필드 0건** · §4 기본 3종 잠금(이름·종류 고정, 색만) · 소프트 딜리트 + **복원 API·UI 0건** · v1 제외인 **집계 카운트 0건**. 정책이 금지한 것이 하나도 들어오지 않았다 |
| **아키텍처 — 백** | **PASS** | 계층·ORM 경계·schema/dto 분리·`commit()` 위치·`except Exception` 0건·`persist_changes` 여전히 `RefreshTokenReuseError` 하나·env 단일 `Settings`(신규 env 없음)·CORS 무변경. 소유 검사가 **repository 의 모든 쿼리 첫 줄**에 있다 |
| **아키텍처 — 프론트** | **FAIL** | 정적빌드·상태관리·`retry:false`·hex 0건·`data-color-token` 렌더·중립 폴백·`items` 경계·무효화 키 전부 성립. 그러나 **자동 저장 실패 표시가 `InlineEditText` 안에 갇혀 색 컨트롤에 없다**(FAIL-1) — FE §3-5 가 「실패 상태 prop 을 공통으로 갖는다」로 못박은 자리다 |
| **SPEC**(SPEC-002) | **FAIL** | API 8표면·Validation·Case Matrix 5코드·상태 전이·팔레트 8종 hex 가 **표 그대로**다. 그러나 **U-7 의 절반(색 트리거의 실패 표시)이 구현되지 않았다**(FAIL-1 = §4 Case Matrix 마지막 행 「그 필드 + 하단 토스트」 위반). 그 밖 U-1~U-3 의 규격값 이탈 WARN 4건 |
| **WP**(WORK-003) | **WARN** | Phase 1~3 체크리스트 실질 완료, **범위 밖 침범 0건**(백 커밋은 `app/back` 만·프론트 커밋은 `app/front` 만), WORK-004 기능 선구현 0건. **Done Criteria 「팔레트가 두 곳에만」이 문자 그대로는 미충족**(WARN-1)이고, Internal Interface Contract 의 `core/constants.py` 기술이 실제와 다르다(문서공백 G-8) |

**단일 정의 축 총평 — 조건부 PASS.** 팔레트 **hex 값**은 `tokens.css` **한 곳뿐**이고 서버·프론트 어디에도 hex 중복이 없다(grep 0건). 다만 **토큰명 나열**은 5곳이라 Done Criteria 문구와 어긋난다(WARN-1). 렌더는 전부 `data-color-token` 이고 인라인 `style`·hex 리터럴이 컴포넌트에 **하나도 없다.**

---

## FAIL — 반드시 고쳐야 하는 것

| # | 파일:줄 | 무엇이 어긋났나 | 어긋난 문서 절 | 어떻게 고치나 |
|---|---|---|---|---|
| **F-1** | `ColorPickerPopover.tsx`(실패 상태 prop 자체가 없다) · `WorkTypePanel.tsx:107-114` · `ProjectPanel.tsx:96-103` · `InlineEditText.tsx:52` | **색 자동 저장이 실패하면 4초 토스트 하나로 끝난다.** 색 트리거는 U-3 이 「고르면 **즉시 저장**」으로 못박은 **자동 저장 컨트롤**인데, `saveColor` 는 실패를 잡아 `toast.error(autoSaveErrorToast("유형 색"))` 만 띄우고 **재전파하지 않으며**(같은 자리의 `saveName` 은 `throw error` 로 재전파한다), `ColorPickerPopover` 에는 실패 표시를 받을 자리가 없다. 결과: **서버를 내린 채 색을 바꾸면 토스트가 4초 뒤 사라지고 화면에 아무 흔적이 남지 않는다** — 사용자는 색이 저장된 줄 안다. 「다시 저장」도 없다. 뿌리는 그 위다 — 실패 상태가 `InlineEditText` 의 **내부 state**(`saveFailed`)라서 **prop 으로 공유될 수 없고**, 그래서 두 번째 자동 저장 컨트롤이 생기자마자 규격이 새어 나갔다 | **SPEC-002 U-7** 「*유지 조건*: 표시는 **화면에 남는다**」·「*해제 조건*: ①「다시 저장」 성공 ② 재편집 후 저장 성공 — **둘 중 하나뿐**」 · **§4 Case Matrix 마지막 행** 「(자동 저장 실패 — 위 어느 코드든, 또는 5xx·네트워크) → U-7 규격 … 표시 위치 = **그 필드** + 하단 토스트」 · **U-3 CTA** 「색 트리거 — 고르면 **즉시 저장**」 · **`frontend/README.md` §3-5** 「`InlineEditText`(S-20)·**`Selector`(S-06) 등 자동 저장 컴포넌트가 실패 상태 prop 을 공통으로 갖는다.** 화면마다 다르게 만들지 않는다」 · **WORK-003 §Internal Interface Contract** 자동 저장 실패 표시 행 | 실패 상태를 **컴포넌트 밖으로 끌어낸다.** ① `InlineEditText` 의 `saveFailed` 를 `saveFailed?: boolean` + `onRetry?: () => void` **prop** 으로 바꾸고(내부 state 는 없앤다), ② 같은 두 prop 을 `ColorPickerPopover` 가 받아 트리거 아래 「저장되지 않았습니다 · 다시 저장」을 그리며, ③ 실패 상태의 소유자는 **패널**(이미 `rowErrors` 를 들고 있다)로 옮겨 `rowFailures[id][field]` 로 필드 단위로 관리한다. 그러면 `saveColor` 의 재전파 유무가 규격을 좌우하지 않는다. **표시 규격 자체가 팝오버형 컨트롤에 대해 문서에 없으므로**(문서공백 G-12) 그 한 줄을 먼저 확정하고 고치는 편이 낫다. **이 컴포넌트를 업무·회의·캘린더가 전부 복제하므로 여기서 닫아야 한다** |

---

## WARN — 규약에서 벗어났으나 동작하는 것

| # | 파일:줄 | 무엇이 어긋났나 | 어긋난 문서 절 | 어떻게 고치나 |
|---|---|---|---|---|
| **W-1** | `app/front/src/types/api.ts:47-55` ↔ `app/front/src/lib/palette.ts:14-23` (그 밖: `app/back/dto/enums.py:19-32` · `app/back/alembic/versions/0001_account_domain_initial.py:25` · `tokens.css` 의 8개 `[data-color-token="…"]` 규칙) | **팔레트 토큰명이 5곳에 나열돼 있다** — Done Criteria 는 「**두 곳에만**」이다. hex 값은 `tokens.css` 한 곳뿐이라 실질 위험은 낮지만, **줄일 수 있는 중복이 하나 남아 있다**: `types/api.ts` 의 `ColorToken` 유니온과 `lib/palette.ts` 의 `PALETTE_TOKENS` 배열이 **같은 8개를 손으로 두 번** 적었다. 토큰을 하나 더할 때 배열에만 넣으면 타입이 잡아 주지만 **유니온에만 넣으면 팝오버에서 조용히 빠진다.** 덧붙여 `core/constants.py:4-5` 는 「DB CHECK 제약도 그 enum 에서 생성된다」라고 적었는데, 그건 `models/account.py:29` 만 사실이고 **마이그레이션은 문자열을 손으로 박았다**(WORK-001 산출물이라 이번 커밋 소관은 아니다) | **WORK-003 §Done Criteria** 「팔레트 8종이 서버 상수와 CSS 변수 **두 곳에만** 정의돼 있다(중복 정의 없음)」 · **§Internal Interface Contract** 팔레트 행 · **SPEC-002 §4 규칙 4** | `PALETTE_TOKENS` 를 정본으로 두고 유니온을 **파생**시킨다 — `export type ColorToken = (typeof PALETTE_TOKENS)[number]`. 그러면 프론트의 손으로 적은 목록이 하나 준다(남는 셋: 배열 1 · CSS 선택자 1 · 서버 enum 1 + 마이그레이션 스냅숏). 나머지 셋은 **구조상 줄일 수 없다**(CSS 는 파생 불가, 마이그레이션은 동결이 정석) — 그러니 Done Criteria 문구 쪽도 손봐야 한다(문서공백 G-8) |
| **W-2** | `WorkTypePanel.tsx:163-199` · `ProjectPanel.tsx:136-164` (+`ColorPickerPopover.tsx:53`) | **인라인 추가 행의 규격값 둘이 근사값으로 대체됐다.** ① SPEC 은 「컨트롤 **36px**」인데 실제는 셋으로 갈렸다 — 셀렉터·이름 입력 `h-9`(36 ✓) / 색 트리거 `h-control`(**34**) / 취소·추가 `size="sm"`(**32**). 같은 줄 안에서 높이가 세 가지다. ② 행 배경은 SPEC 이 `#FBFCFF` 로 못박았는데 `bg-row-hover`(`--tm-row-hover` = `#FAFBFC`, 행 hover 값)를 재사용했다 — 추가 행과 hover 행이 같은 색이 된다 | **SPEC-002 U-2 상태** 「*열림*: 56px 한 줄, 배경 `#FBFCFF`, **컨트롤 36px**」 | ① 세 컨트롤을 36 하나로 맞춘다(`h-9`). 색 트리거는 **목록 행에서도 쓰이므로** 높이를 prop 으로 받거나 추가 행에서만 `className` 으로 덮는다. ② `#FBFCFF` 에 토큰이 없다 — `--tm-row-add-bg` 를 `tokens.css` 에 신설해 쓴다(컴포넌트에 hex 를 넣으면 §11 금지 4 위반이다). 토큰 신설은 문서공백 G-11 과 함께 처리 |
| **W-3** | `WorkTypePanel.tsx:52-56` · `ProjectPanel.tsx:39-42` | `openAddRow` 가 `setAddOpen(true)` 와 에러 초기화만 한다. **이미 열려 있을 때 「유형 추가」를 다시 눌러도 아무 일도 일어나지 않는다** — `autoFocus` 는 마운트 때만 걸리므로 포커스가 이동하지 않는다. 바로 위 주석(`WorkTypePanel.tsx:53`)은 「그 행으로 포커스만 옮긴다」라고 **구현했다고 적혀 있다** | **SPEC-002 U-1 CTA** 「추가 행이 이미 열려 있으면 **그 행으로 포커스만 옮긴다**(두 줄이 동시에 열리지 않는다)」 | 이름 입력에 `ref` 를 걸고 `openAddRow` 에서 `inputRef.current?.focus()` 를 부른다. 두 패널이 같은 코드라 **추가 행을 컴포넌트로 뽑으면**(W-6) 한 번만 고치면 된다 |
| **W-4** | `InlineEditText.tsx:113`(`disabled={saving}` 뿐) · `ColorPickerPopover.tsx`(표시 없음) | **저장 중 진행 표시가 없다.** 입력은 `disabled` + `opacity-60` 으로 흐려지기만 하고, 색 트리거는 저장 중임을 전혀 드러내지 않는다. 느린 회선에서 「눌렀는데 반응이 없다」로 보인다 | **SPEC-002 U-3 상태** 「*저장 중*: **편집한 컨트롤 옆에 진행 표시.** 다른 행은 잠기지 않는다」 | 두 컨트롤에 스피너 자리를 둔다. WORK-002 의 `ConfirmModal`·`LoginScreen` 이 이미 `Loader2` 를 쓰므로 같은 표시를 재사용한다. 「다른 행은 잠기지 않는다」는 이미 성립한다(행별 state) |
| **W-5** | `SettingsPanel.tsx:30` `rounded-card` → `tokens.css` `--tm-radius-card: 12px` | **패널·카드 radius 가 12px 인데 SPEC 은 16 이다.** WORK-002 검수 W-2(설정 메뉴 카드)와 **같은 뿌리이고 이번에 패널 둘로 번졌다** — 고치지 않으면 이후 모든 카드가 12로 굳는다 | **SPEC-002 §2 Placement** 「카드는 1px `#D9D9D9` · **radius 16**」 · SPEC-001 U-4 같은 문구. `09-design-tokens.md` §형태는 「카드 **12~16**」 **범위**라 SPEC 쪽이 좁은 계약이다 | 토큰 하나를 정한다. 12→16 으로 올리거나 「패널·설정 카드만 16」인 두 번째 토큰을 둔다. **값 결정은 디자인 소관**이라 문서공백 G-10 에 함께 올렸다 |
| **W-6** | `WorkTypePanel.tsx:162-203` ↔ `ProjectPanel.tsx:135-169` | **인라인 추가 행이 두 패널에 통째로 복제됐다**(배경·높이·`Enter`/`Esc` 처리·취소/추가 버튼·인라인 에러 문단까지 거의 같은 40여 줄). 그래서 W-2·W-3 을 고치려면 **두 곳을 같이** 고쳐야 하고, 다음 영역(업무 생성 인라인 추가)이 **세 번째 사본**을 만들 자리다. FE §2 는 `InlineAddRow.tsx`(S-16)를 공용 목록에 이미 올려 두었다 | **`frontend/README.md` §2** `components/shared/` 목록에 `InlineAddRow.tsx` 가 있다 · **WORK-003 §Code Surface** 「`components/shared/InlineAddRow.tsx` — 56px 추가 행」 | 추가 행을 컴포넌트 하나로 뽑는다. 지금 소비자가 같은 영역 둘뿐이니 `features/settings/components/` 도 되고(FE §2 규칙 3 — shared 는 **두 영역 이상**), 업무 영역이 쓰기 시작할 때 `components/shared/` 로 올린다. **지금 뽑아 두면 F-1·W-2·W-3 을 한 자리에서 닫는다** |
| **W-7** | `app/front/src/components/shared/InlineEditText.test.tsx:1-8` | **필수 테스트 ③의 절반이 검증되지 않았다.** FE §11-3 은 「실패 응답에 **토스트 + 그 필드의 실패 표시**가 **함께** 뜨고 재시도가 나가지 않는다」인데, 테스트는 컴포넌트 몫(필드 표시·자동 재시도 없음·해제 조건 2가지)만 보고 **토스트 쪽은 호출자 몫이라며 비워 두었다.** 검증되지 않은 그 절반이 정확히 **F-1 이 숨어 있던 자리**다 — 색 저장 실패에는 토스트만 있고 필드 표시가 없다 | **`frontend/README.md` §11 「반드시 있어야 하는 테스트」 3** · 같은 절 「네트워크 = **MSW** 로 `client.ts` 아래에서 가로챈다」 | MSW 가 이미 설치돼 있으므로(`msw@^2.15.0`) **패널 레벨 테스트**를 하나 더한다 — `WorkTypePanel` 을 띄우고 PATCH 를 500 으로 막은 뒤 ① 이름 저장 실패에 토스트 + 필드 표시가 **함께** 뜨는가 ② **색 저장 실패에도 같은 둘이 뜨는가**(지금은 실패한다 = F-1 을 잡는 테스트) ③ 그 뒤 추가 요청이 나가지 않는가 |

---

## 문서 공백 — 코드가 아니라 문서를 고쳐야 하는 것

> G-1~G-7 은 코드 워커가 올린 것이고 판정을 붙였다. G-8 이후는 이번 검수에서 새로 찾은 것이다.

| # | 무엇이 비었나 | 어느 문서 어느 절 | 무엇을 적어야 하나 |
|---|---|---|---|
| **G-1** | **에러 코드 3종이 §8-2 표에 없다** — `duplicate_name`·`invalid_color_token`·`not_found`. 워커는 발명하지 않고 SPEC-002 §4 Case Matrix 의 문구·상태코드를 그대로 썼다(`work_type_service.py:19-21` · `constants.py:27` · `exceptions.py:52-54`) | **`backend/README.md` §8-2** 코드 표(SPEC-002 S002-OQ-2) | **판정: 코드가 맞다. 표에 3행을 더한다.** `duplicate_name` \| 409 \| 같은 계정에서 삭제되지 않은 것끼리 이름 중복 \| SPEC-002 §4 / `invalid_color_token` \| 422 \| 허용 팔레트 8종 밖의 토큰명·임의 hex \| A-5 / `not_found` \| 404 \| 없는 항목·**남의 항목**(존재를 흘리지 않는다) \| SPEC-002 §5. 셋 다 이미 §8-2 의 AppError 5종에 자연스럽게 얹힌다(Conflict·Validation·NotFound) — **새 가지를 만들 필요가 없다** |
| **G-2** | **`extra="forbid"` 를 이번 요청 스키마에만 걸었다**(`schemas/setting.py:52`). 기존 `schemas/auth.py` 는 그대로라, 같은 레포에 「모르는 필드를 거부하는 계약」과 「조용히 무시하는 계약」이 공존한다 | **`backend/README.md` §3**(schema/dto 규칙 여섯) | **판정: 코드가 맞고 규칙이 비었다.** 규칙 일곱 번째로 「**요청 schema 는 `extra="forbid"` 다** — 계약에 없는 필드를 조용히 무시하면 「바뀐 줄 알았는데 안 바뀐」 상태가 성립한다(SPEC-002 §4 「`kind` 는 PATCH 로 받지 않는다」가 이 설정으로 강제된다)」를 적고, **전 영역 적용 여부**를 못박아라. 전 영역으로 정하면 `schemas/auth.py` 에 소급 적용하는 작은 후속 작업이 하나 생긴다(로그인 요청에 여분 필드를 보내는 클라이언트가 없으므로 위험은 없다) |
| **G-3** | **빈 `PATCH {}` 의 계약이 없다.** 코드는 200 + 현재 값을 돌려준다(`work_type_service.py:102-104` · `project_service.py:79-80`). Case Matrix 에 「바꿀 것 없음」 실패가 없어 워커가 에러를 발명하지 않았다 | **SPEC-002 §4 Request / Response** PATCH 절 | **판정: 발명하지 않은 것이 옳다.** 한 줄만 적으면 닫힌다 — 「**보낸 필드가 하나도 없으면 200 + 현재 값**이다. 「바꿀 것 없음」은 실패가 아니다 — 인라인 자동 저장이 값이 그대로일 때 요청을 만들지 않으므로 정상 경로에서 도달하지 않는다」 |
| **G-4** | **이미 삭제된 항목의 PATCH·DELETE 가 404 인 근거가 간접적이다.** §4 State 에 「`삭제됨` 에서 나가는 전이가 없다」만 있고, **삭제된 항목을 지시했을 때**의 응답이 명시돼 있지 않다. 코드는 `_require_active` 로 404 를 낸다 | **SPEC-002 §4 Case Matrix** `not_found` 행 · **§4 State / Lifecycle** | **판정: 해석이 옳다.** Case Matrix 의 `not_found` 행 설명을 「(없는 항목 · 남의 항목)」 → 「(없는 항목 · **이미 삭제된 항목** · 남의 항목)」으로 넓힌다. 셋이 같은 응답이라는 것이 곧 「존재를 흘리지 않는다」의 내용이다 |
| **G-5** | **`tests/setting_fixtures.py` 가 `conftest.py` 가 아니라 자동 수집되지 않는다** — 쓰는 쪽이 `from tests.setting_fixtures import Owner, owner, stranger  # noqa: F401` 로 이름을 끌어온다(`test_work_type.py:19`). WORK-001 의 `conftest.py` 를 건드리지 않으려는 선택이었다 | **`backend/README.md` §12** 테스트 규약 표 | **판정: 동작하고(=import 로 수집된다) 의도도 옳다. 다만 규약이 없어 다음 work 가 또 고민한다.** §12 에 한 행 — 「**픽스처 배치**: 전 영역 공통은 `tests/conftest.py`, **work 하나에만 쓰이는 픽스처는 `tests/<영역>_fixtures.py`** 에 두고 쓰는 쪽이 import 한다(`# noqa: F401`). 선행 work 의 `conftest.py` 를 넓히지 않는다 — 그 파일이 커지면 모든 테스트가 서로의 픽스처에 묶인다」 |
| **G-6** | **A-6「참조 중인 곳에 이름·색 그대로」를 소비 경로로만 검증했다** — `task`·`meeting` 테이블이 아직 없어 `find_including_deleted` 로 확인했다(`test_work_type.py:411-438`). 화면 확인은 WORK-004 몫이다 | **WORK-003 §Done Criteria**(SPEC-002 §6 Acceptance 마지막 항목) · **WORK-004 이후 work 의 검증 절** | **판정: 지금 할 수 있는 최선이고 검증이 정확하다**(삭제분 조회는 이름·색을 그대로 돌려주고 활성 조회에는 안 잡힌다는 두 쪽을 다 본다). SPEC-002 §6 의 마지막 항목이 이미 「(다음 배치와 함께 확인)」이라고 적혀 있으니, **WORK-003 Done Criteria 에서 그 한 항목을 명시적으로 이월**로 표시하고(「14개 중 13개 확인 · 1개는 WORK-004 로 이월」), **WORK-004 의 검증 절에 그 항목을 복사해 넣어라.** 안 옮기면 아무도 안 본 채로 닫힌다 |
| **G-7** | **`['tasks']`·`['meetings']` 무효화가 읽는 화면이 없어 지금은 no-op** (`useWorkSettings.ts:33-47`) | **WORK-003 §Internal Interface Contract** 캐시 키 행 — **이미 적혀 있다** | **판정: 설계대로다. 지적 아님.** WP 가 「이 work 시점에는 후자 키가 없으므로 키 등록만 해 두고 소비 그룹에서 연결」이라고 미리 적어 두었고 코드가 그대로다. 다만 **다음 검수가 「죽은 코드」로 오판하지 않도록** WORK-004 의 Dependency 절에 「`['tasks']` 무효화는 **WORK-003 이 이미 걸어 두었다** — 화면만 만들면 붙는다」를 적어 두면 좋다 |
| **G-8** | **WP 가 지정한 서버 정의처가 실제와 다르다.** Internal Interface Contract 는 「**서버는 `core/constants.py` 한 곳**」이라 적었는데, 실제 값은 WORK-001 이 만든 `dto/enums.py` 의 `ColorToken` 에 있고 `constants.py` 는 **검증 함수만** 갖는다. 워커는 「여기서 8종을 다시 나열하면 정의가 둘이 된다」는 이유를 파일 머리에 남겼다(`constants.py:3-9`) — **판단이 옳다**(그렇게 안 했으면 서버에만 정의가 셋이 됐다) | **WORK-003 §Internal Interface Contract** 팔레트 행 · **§Done Criteria** 「두 곳에만」 | 두 문장을 고친다. ① 「서버는 **`dto/enums.py` 의 `ColorToken`** 한 곳(WORK-001 산출물)이 값의 정본이고, `core/constants.py` 는 **검증만** 갖는다」. ② Done Criteria 를 실측에 맞춘다 — 「**hex 값**은 `tokens.css` 한 곳, **토큰명**은 서버 enum 1 · CSS 선택자 1 · 프론트 배열 1 로 끝난다. 마이그레이션의 CHECK 문자열(`0001_account_domain_initial.py:25`)은 **의도적으로 동결된 스냅숏**이라 이 셈에 넣지 않는다」. 지금 문구 그대로면 앞으로 모든 검수가 같은 WARN 을 반복한다 |
| **G-9** | **「유형 추가」 버튼 높이가 문서끼리 어긋난다** — SPEC-002 U-1·U-5 는 「**32px**」, `09-design-tokens.md` §형태는 「버튼·필터 **34**」다. 코드는 34(`SettingsPanel.tsx:36` `h-control`)를 골랐다 | **`00-design/09-design-tokens.md` §형태** ↔ **SPEC-002 U-1 CTA·U-5** | 어느 쪽이 정본인지 한 줄로 못박아라. 토큰 문서가 컨트롤 높이의 정본이면 SPEC 의 32 를 34 로 정정하고, 「패널 헤더 CTA 만 32」라면 토큰 문서에 그 예외를 등록한다. **코드는 어느 쪽으로 정하든 한 글자만 바뀐다** — 지금 지적하지 않은 이유가 이것이다 |
| **G-10** | **카드 radius 가 문서끼리 어긋난다** — SPEC-001 U-4·SPEC-002 §2 는 「**16**」으로 못박았고 `09-design-tokens.md` §형태는 「카드 **12~16**」 **범위**다. 토큰은 12 로 굳어 있다(`tokens.css:63`). WORK-002 검수 W-2 로 이미 올렸고 **이번에 패널 둘로 번졌다** | **`00-design/09-design-tokens.md` §형태** ↔ SPEC-001 U-4 · SPEC-002 §2 Placement | **범위를 값 하나로 좁혀라.** 「카드 radius = 16(작은 칩·컨트롤은 8·4)」처럼 단일 값으로 적고, 두 값이 필요하면 `--tm-radius-card` / `--tm-radius-card-sm` 두 토큰으로 나눠 **어디에 무엇을 쓰는지**까지 적는다. 지금은 「범위」라 리뷰가 판정할 수 없고, 그래서 12 가 두 work 를 지나 굳었다 |
| **G-11** | **인라인 추가 행 배경 `#FBFCFF` 에 토큰이 없다.** SPEC-002 U-2 가 값을 직접 적었는데 `09-design-tokens.md` §색에는 그 자리가 없어(가장 가까운 것이 「행 hover `#FAFBFC`」) 워커가 `--tm-row-hover` 로 대체했다(W-2) | **`00-design/09-design-tokens.md` §색** — 「면·선」 항목 | 「**행 추가/편집 중 배경** `#FBFCFF`」를 §색에 등록한다. 그래야 `tokens.css` 에 `--tm-row-add-bg` 를 만들 근거가 생기고, 컴포넌트에 hex 를 넣지 않고도 U-2 를 만족시킬 수 있다. 값이 필요 없다고 판단되면 **SPEC-002 U-2 에서 `#FBFCFF` 를 지우고 「행 hover 와 같은 면」으로 고쳐라** — 지금처럼 두면 매 검수마다 같은 이탈이 잡힌다 |
| **G-12** | **U-7 이 「필드」만 상정하고 있어 팝오버형 컨트롤의 실패 표시 규격이 없다.** U-7 은 「*실패 필드*: **테두리** 실패색 + 값 유지 + 그 **아래** 12px 캡션」이라 **입력 상자**를 전제한다. 그런데 색 트리거는 56px 버튼 + 팝오버이고, 목록 행은 64px 고정이라 **캡션 한 줄을 넣을 세로 공간이 없다.** 규격이 없어서 구현이 통째로 빠졌다(FAIL-1) | **SPEC-002 U-7 상태** — 새 항목 | **F-1 을 고치기 전에 이것부터 정해야 한다.** 세 갈래 중 하나를 고르고 적어라 — ① 실패한 컨트롤에 **테두리 실패색만** 얹고 캡션·「다시 저장」은 **행 아래로 밀어낸다**(행이 64→84 로 늘어난다) ② 캡션 없이 **컨트롤 옆 아이콘 + 클릭 시 재시도**로 압축한다 ③ 행 아래 인라인 자리를 **필드 무관하게 하나** 두고 「〈필드 이름〉이 저장되지 않았습니다 · 다시 저장」으로 적는다. **어느 쪽이든 「화면에 남는다 · 해제 조건 둘뿐 · 자동 재시도 없음」은 그대로 지킨다.** 전 영역이 이 규격을 복제하므로 여기서 확정해야 한다(③이 행 높이를 안 건드려 U-8 「두 줄로 접히지 않는다」와도 안 부딪힌다) |

---

## 확인한 것 (PASS 근거)

**범위 산정** — `git diff 533843e...HEAD --stat`(39파일) + `git log 533843e..HEAD`(2커밋) + `git status --porcelain`(무출력). 커밋별 `--name-only`: `ffc544d` 는 `app/back/**` 14파일만, `8e17d0b` 는 `app/front/**` 25파일만. **백↔프론트 교차 0건**이고 `.env.example`·인프라 파일에 손대지 않았다.

**정책(DEC-001)**
- **slug·영문명 필드 0건** — `grep -rni "slug"` 가 `models/base.py:16` 의 「slug·영문명 필드를 두지 않는다」 주석 하나만 잡는다(§3 「(공통) 키」).
- **집계 카운트 0건** — 응답 schema(`WorkTypeItem`·`ProjectItem`)에 사용 건수 필드가 없고 service·repository 어디에도 집계 쿼리가 없다(§5 「집계를 계산하지 않는다」 · S002-OQ-3).
- **복원 경로 0건** — `restore`/`undelete` 가 API·서비스·화면 어디에도 없고, 그 사실을 백엔드 테스트 2개(`test_there_is_no_restore_endpoint`)가 못박는다(DEC-004 §4).
- 유형은 **종류+이름+색**, 프로젝트는 **이름+색** — dto·schema·화면이 모두 같은 필드 집합이다(§3).

**아키텍처 — 백엔드**(정적 검사)
- `grep -rn "except Exception\|except:"` → **0건**(§8-1). 포착은 전부 구체 타입이고 삼키는 자리가 없다.
- `grep -rn "\.commit()"` → `api/deps.py:40,42`(요청 경계)와 `seed/seed.py:132` 뿐. **service·repository 에 `commit()` 없음**, repository 는 전부 `flush()` 까지다(§2·§7).
- `grep -rn "^from fastapi\|from schemas" app/back/service app/back/repository` → **0건**(§2·§3 규칙 1).
- `from models` 가 `repository/`·`models/`·`alembic/`·`seed/`·`tests/` 밖에 **0건**. 두 repository 모두 `_to_dto()` 를 지나 `WorkTypeDTO`·`ProjectDTO` 만 반환 — **ORM 모델이 repository 를 넘지 않는다**(§2·§3 규칙 2). `AsyncSession` 전달은 규약에 금지 근거가 없어 지적하지 않았다.
- **`persist_changes` 는 그대로 하나** — `exceptions.py:44` 의 `RefreshTokenReuseError` 뿐이고 이번 커밋이 새로 켠 예외가 없다. `ConflictError`·`NotFoundError`·`ValidationError` 는 전부 기본 False(=롤백)다(§7, 2026-09-05 신설).
- **신규 env 0건**(WP Pre-deploy Check) — `config.py` 무변경, `main.py` 는 라우터 한 줄만 추가. CORS 는 `allow_origins=settings.cors_origin_list` + **`allow_credentials=False`** 그대로다.
- **입력도 dto** — `body.to_dto()` 로 8표면 전부가 명시 dto 를 만들어 넘긴다. PATCH 는 `T | Unset`(`dto/unset.py`)로 「보내지 않음」과 「null 로 지움」을 가르고, `_PartialUpdate._reject_explicit_null`(`schemas/setting.py:62-67`)이 명시적 `null` 을 거부한다(§3 규칙 3·4).
- **라우터 단위 인가** — `setting_router.py:25-29` 가 `dependencies=[Depends(require_account)]` 로 8표면 전부를 덮는다. **게이트 밖 표면이 하나도 없다**(§9). 테스트 2개(`test_every_surface_requires_a_session`)가 8표면 전수를 확인한다.
- **소유 검사가 쿼리의 첫 줄** — `_active(account_id)` 가 `account_id` + `deleted_at IS NULL` 을 함께 건다. 삭제분을 보는 메서드만 `find_including_deleted` 로 **이름에 그 사실이 드러난다**(DB §0-1).

**단일 정의 · 색 렌더**
- 팔레트 8종의 **hex 가 서버에 0건**(`grep -rniE "#(EEF1FE|F1F2FE|F4F7FF|EAF7F0|E9F3FD|FBF2DC|FCEEEC|F1F2F5)" app/back` → 무출력). 서버는 **토큰명만** 안다.
- `tokens.css` 의 16개 값이 **SPEC-002 §4 표와 8/8 전부 일치**(indigo `#EEF1FE`/`#4A55B8` · violet `#F1F2FE`/`#4B52A8` · steel `#F4F7FF`/`#3F5F94` · mint `#EAF7F0`/`#2F7F5B` · sky `#E9F3FD`/`#2E6FA8` · amber `#FBF2DC`/`#8A6714` · rose `#FCEEEC`/`#A34A3F` · graphite `#F1F2F5`/`#4A4E58`).
- **컴포넌트 hex 리터럴 0건** — `grep -rnE "#[0-9A-Fa-f]{3,8}" src --include='*.ts(x)'`(styles 제외) → **무출력**. 인라인 `style={{}}` **0건**. 신규 shadcn 생성물(`ui/select.tsx`·`ui/popover.tsx`)에도 hex 가 없다(§5-3 · §11 금지 4).
- **중립 폴백이 실제로 성립한다** — `tokens.css` 가 `[data-color-token]`(중립)을 **먼저** 선언하고 8개 `[data-color-token="…"]` 를 **뒤에** 둔다. 특이도가 같으므로 나중 규칙이 이기고, **매칭되는 것이 없으면 중립이 남는다.** 항목을 숨기는 코드가 없다(`TypeBadge.tsx:24-27` 은 검증조차 하지 않는다 — 걸러 내면 「항목이 사라진다」가 되기 때문). 테스트 `TypeBadge.test.tsx:44-51` 이 없는 토큰명으로 확인한다.

**아키텍처 — 프론트**(정적 검사)
- 동적 세그먼트 **0개** · `app/api/**` 없음 · `middleware.ts` 없음 · Server Action 없음. 신규 `settings/work/page.tsx` 에 `'use client'` ✓, 라우트 파일은 화면 컴포넌트 하나만 렌더한다(§1-3·§2 규칙 1).
- 전역 상태 라이브러리 **0건**(redux/zustand/jotai/recoil/mobx). 서버 상태는 TanStack Query, `retry:false` 는 `providers.tsx` 전역 그대로.
- **`items` 를 꺼내는 것이 `api.ts` 까지** — `features/settings/api.ts:13-18,47-50` 만 `response.items` 를 읽고, 훅·컴포넌트는 배열을 받는다(§3-6).
- **무효화 표대로다** — `useWorkSettings.ts:33-47` 이 `['workTypes']`(또는 `['projects']`) + `['tasks']` + `['meetings']` 셋만 무효화한다. 표에 없는 무효화가 없다(§3-3).
- **낙관적 갱신 0건** — 모든 mutation 이 `onSuccess` 에서만 무효화하고, 화면 값은 서버 응답이 온 뒤 바뀐다(§3-4 · SPEC-002 §4).
- **자동 재시도 0건** — `retry:false` 전역 + `InlineEditText` 가 실패 후 스스로 재요청하지 않는다. 테스트가 60ms 대기 후 `onSave` 호출 1회를 단언한다(`InlineEditText.test.tsx:35-37`).
- **토큰 저장소 격리 유지** — `localStorage`/`sessionStorage`/`@tauri-apps` 호출이 `tokenStore.ts` 와 그 테스트 목(`src/test/tauriMock.ts`) 밖에 **0건**. 직접 `fetch` **0건**. `ui/dialog` 직접 import 는 `ConfirmModal.tsx` 하나 그대로(§11 금지 1·2·3).
- **gutter W-2 정정 유지** — `tokens.css:104` 기본 48 + `@media (min-width:1440px)` 의 `clamp(80px, calc(80px + (100vw-1440px)/3), 240px)`. 1440→80 · 1920→240 이 그대로다.

**SPEC-002 대조**
- **API 8표면**의 경로·메서드·상태코드가 §4 표 그대로다(POST 201 · PATCH 200 · DELETE 204 · GET `{items:[…]}`). **복원 엔드포인트 없음**, **「삭제된 것도 달라」 파라미터 없음**.
- **Validation 5행 전부**: `kind` 는 `Literal["meeting","task"]` 생성 전용 · `name` 은 `strip_whitespace` + 1~30자 + **줄바꿈 거부**(`_reject_newlines`) · **이름 유일성**은 계정 안 · 삭제분 제외 · **종류 무관 전체 유일** · 대소문자·공백 정규화(`name_match.py` 가 파이썬과 SQL 규칙을 **한 파일**에 묶어 갈리지 않게 했다) · `colorToken` 은 팔레트 8종 · 기본 3종 잠금.
- **Case Matrix 5코드가 코드에 실재**: `validation_error`(422, `main.py` 핸들러) · `duplicate_name`(409) · `work_type_locked`(409) · `invalid_color_token`(422) · `not_found`(404). 프론트 `errors.ts:32-44` 가 **`code` 로만 분기**하고 문구를 Case Matrix 대로 갈랐다(「유형이」/「프로젝트가」 조사를 템플릿으로 묶지 않은 것까지). **Matrix 에 없는데 코드에 있는 에러는 없다** — 빈 PATCH 도 200 이고(G-3), 삭제된 항목도 `not_found` 로 합류한다(G-4).
- **`kind` 는 PATCH 로 받지 않는다** — `WorkTypeUpdateDTO` 에 필드 자체가 없고 `extra="forbid"` 가 422 `validation_error` 로 거부한다. **잠금(409)이 아니라 검증(422)** 이라는 WP 검증 항목까지 테스트가 못박는다(`test_patch_cannot_change_the_kind`).
- **기본 3종 잠금이 두 겹** — 서버 `work_type_service.py:91-92,125-126`(이름 변경·삭제 모두 `work_type_locked`, **색은 통과**) + 화면 `WorkTypePanel.tsx:230,247-248`(`readOnly` 이름 · 삭제 버튼 자리를 빈 칸으로 두어 열 정렬 유지 · 색 트리거만 활성). 테스트 3개가 「개명 409 · 삭제 409 · 색 변경 200」을 확인한다.
- **소프트 딜리트** — `soft_delete` 가 `deleted_at` 만 찍고 행을 지우지 않는다. 하드 삭제 경로 **0건**. `test_delete_is_soft_and_the_row_survives` 가 DB 행 잔존을, `test_a_deleted_type_keeps_its_name_and_color_for_references` 가 **A-6 양쪽**(삭제분 조회에는 이름·색 그대로 / 활성 조회에는 안 잡힘)을 확인한다.
- **남의 것은 404**(403 아님) — `find_active` 가 남의 것과 없는 것을 똑같이 `None` 으로 돌려 service 가 같은 `NotFoundError` 를 던진다. `test_another_accounts_type_is_404_not_403`·`test_list_never_mixes_in_another_account` 가 각 리소스마다 있다.
- **정렬** — 유형은 `is_default DESC, id ASC`(기본 3종 먼저 · 그 뒤 생성 순), 프로젝트는 `id ASC`(생성 순). §4 Data Contract 그대로이고 테스트가 확인한다.
- **U-4 색 팝오버** — 폭 240(`w-60`) · 24px 스와치(`h-6 w-6`) **4×2**(`grid-cols-4` × 8개) · 현재 값 `border-primary shadow-swatch-current`(1px + 3px 글로우) · **확인 버튼 없음**(고르면 `onSelect` + 닫힘) · **자유 색 입력 없음**(팔레트 배열만 순회) · `Esc`·바깥 클릭은 Radix 기본이라 값이 바뀌지 않는다.
- **U-6 삭제 모달** — 제목·요약·경고 3문구가 SPEC 과 **글자까지 일치**하고, WORK-002 의 `ConfirmModal`(600)을 `openConfirm` 으로 재사용하며 `destructive: true` 로 확인 버튼이 `#E2685B` 다. 실패해도 취소 경로 없이 토스트만 띄우고 행을 남긴다.
- **U-8 반응형** — `SettingsMenuCard.tsx:70` 이 `w-[240px] … wide:w-[260px]`(브레이크포인트 `wide: 1440px`)로 SPEC 의 240/260 을 정확히 재현하고 `self-start` 로 「내용 높이만큼만 · 상단 고정」을 만든다. 목록 행은 배지·칩·색·삭제가 전부 `shrink-0` 이고 이름 열만 `min-w-0 flex-1` 이라 **두 줄로 접히지 않는다.**
- **치수** — 패널 헤더 `h-[60px]` · 목록 행 `h-16`(64) · 추가 행 `py-2.5 + h-9`(=56) · 배지 `h-5 rounded-chip text-badge`(11px/600) · 패널 간격 `gap-5`(20) · 색 트리거 폭 `w-14`(56). 전부 SPEC 값이다(예외는 W-2·W-5).
- **빈 상태** — `ProjectPanel.tsx:180-190` 이 프로젝트 0건일 때만 뜨고 문구 두 줄 + 「프로젝트 등록」 진입점을 갖는다(U-5). **유형 패널에는 빈 상태가 없다** — 시드 3종이 항상 있어 도달하지 않는다.
- **조회 실패를 빈 목록으로 가리지 않는다** — 두 패널 모두 `isError` 에 「불러오지 못했습니다」 + 「다시 시도」를 그린다(§3-5 · DEC-003 §7 승계).

**WP**
- Phase 1 작업 7항목·Phase 2 작업 5항목·Phase 3 작업 8항목이 전부 실재한다(예외: `InlineAddRow` 를 뽑지 않고 인라인화 — W-6).
- 백엔드 테스트 **48개**(`test_work_type.py` 30 · `test_project.py` 18)가 WP Phase 1 검증 8항목을 덮는다.
- **범위 밖 선구현 0건** — 업무·회의 화면, 유형/프로젝트를 **고르는 쪽**(생성 드로어·필터), 집계 카운트가 하나도 없다. 개인 설정·연동 관리 페이지는 WORK-002 가 만든 제목 한 줄 그대로다.

---

## 코디 실행 요청

리뷰는 read-only 라 아래는 **실행하지 않았다.**

1. **`cd app/back && uv run pytest`** — 48개 신규 테스트 통과 확인(WP Phase 1 검증 마지막 항목). 특히 `setting_fixtures.py` 가 **`conftest.py` 가 아니라 import 로 수집되는** 구조라(G-5), 픽스처 해석이 실제로 도는지는 실행으로만 확인된다.
2. **`cd app/front && npm run test && npm run typecheck && npm run lint && npm run build`** — 신규 테스트 2파일 통과 · 타입 · ESLint 금지 규칙 · 정적 산출물 확인.
3. **F-1 재현**(권장, 5분): 앱 창에서 API 를 내린 뒤 ① 유형 **이름**을 고치고 포커스를 뺀다 → 토스트 + 필드에 「저장되지 않았습니다 · 다시 저장」이 **남는다**(정상). ② 같은 상태에서 유형 **색**을 바꾼다 → 토스트만 뜨고 **4초 뒤 아무 흔적도 남지 않는다**(F-1). 두 화면을 나란히 보면 규격이 반쪽인 것이 바로 보인다.
4. **문서 수정 착수 우선순위**: **G-12**(U-7 의 팝오버 규격 — F-1 수정의 선행조건) → **G-8**(Done Criteria·정의처 문구를 실측에 맞춤, 안 고치면 매 검수가 같은 WARN 반복) → **G-10**(카드 radius, WORK-002 부터 두 번째 재발) → G-1·G-2 → 나머지.
5. **F-1 재발주 범위**: 프론트 워커 한 명, `InlineEditText`·`ColorPickerPopover`·두 패널 4파일. **G-12 결정을 받은 뒤** 착수하는 편이 낫다 — 규격 없이 고치면 다음 영역이 또 다르게 만든다. W-2·W-3·W-6 을 같은 발주에 묶으면 추가 행을 뽑으면서 한 번에 닫힌다.

---

## 자기 점검

- [x] **네 층 전부에 판정을 냈다** — 정책 PASS / 아키텍처-백 PASS / 아키텍처-프론트 FAIL / SPEC FAIL / WP WARN (+ 단일 정의 축 별도 총평).
- [x] **모든 FAIL·WARN 에 파일:줄 + 어긋난 문서 절을 붙였다** — FAIL 1건, WARN 7건 전부.
- [x] **문서 공백을 지적과 분리했다** — 별도 절 12건. 워커가 올린 7건에 전부 판정을 붙였고(G-1~G-7, 그중 G-7 은 「지적 아님·설계대로」) 5건을 새로 찾았다(G-8 WP 기술 오류 · G-9·G-10 문서 간 충돌 2건 · G-11 토큰 부재 · G-12 U-7 규격 공백).
- [x] **코드·문서를 하나도 고치지 않았다** — `git status --porcelain` 무출력. 리포트는 문서 레포의 `orchestration/work/docs-v1/` 에만 썼다. 테스트·빌드를 돌리지 않았다.
- [x] **근거 없는 추측·취향 지적을 싣지 않았다** — 규약에 조문이 없는 것(추가 행 코드 중복의 미학, `ui/popover.tsx` 의 `"use client"` 누락, U-8 「이름 열 최소 200」이 실제 폭에서 한 번도 구속하지 않는 점)은 제외했다. WORK-004 이후의 미구현(업무 화면·집계 카운트·A-6 화면 확인)을 FAIL 로 잡지 않았고, A-6 이월은 G-6 에 기록만 했다. WORK-001·002 커밋은 다시 보지 않았다 — 다만 `alembic/0001` 의 팔레트 문자열과 `--tm-radius-card` 는 **이번 판정에 직접 걸려** WARN-1·W-5 에서 출처를 밝혀 언급했다.
