# [frontend] 조직 화면 1단계 — v3 레이아웃 읽기 전용 구현 (기존 API 4개 + access/members 위)

너는 **sc-ax `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/roles/sc-ax/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system` (HEAD `ceecbe9` — 디자인 v2 1~3차 + 부품 Drawer·ConfirmModal·Toast·DatePicker 커밋됨)
base 브랜치: `origin/main` → 최종 PR 대상 `main`

코디가 API 8001(`AX_DEMO_EMAIL_DOMAIN=companysc.com`)·프론트 5176 을 띄워 둔다. 로컬 DB 는 SC 조직도 165명 단독. 로그인은 `<사번>@companysc.com` / `scax-demo-1234` — 대표 `1001`(조직 관리 권한 있음), 부서장 `1106`, 팀장 `1141`, 팀원 `1107`. `backend/`·`.design-sync/`·`frontend/ds-entry.tsx` 는 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- **디자인 핸드오프(화면 스펙)**: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/reference/2026-09-09-sc-ax-design/org-chart-template/HANDOFF.md` ← 레이아웃·패널·행 규격·상태·상호작용·토큰이 전부 여기. **이 문서가 이번 작업의 계약이다.**
- **디자인 마크업**: 같은 폴더 `OrgChart.dc.html` — 인라인 스타일 값과 클래스가 그대로 쓸 수 있는 형태(더미 데이터 주의).
- **조사 리포트**: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/work/sc-design-system/org-screen-survey-report.md` §대조표·§BE 필요 — 무엇이 현재 API 로 되고 무엇이 안 되는지.
- 스펙: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/work/sc-design-system/ref-spec-main/spec-005-organization-people-access.md` §5 「UI 가 제공하지 않는 기능을 사용 가능한 관리 기능처럼 표시하지 않는다」.
- 기존 부품: `frontend/src/{Icon,Skeleton,Empty,Modal(Drawer·ConfirmModal·Toast),FormControls(Checkbox·FieldMessage),Popover,DateField,DatePicker}.tsx` · `styles.css` 클래스 — **새 CSS 는 원칙적으로 쓰지 않는다**(핸드오프 원문). 꼭 필요하면 `styles.css` 에 최소로, hex 금지.

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

`OrgPage.tsx`(트리 + 구성원 + 권한 폼)를 핸드오프의 v3 로 바꾼다: 관리자/직원 배지 → 3분할(조직 tree 392 · 구성원 목록 1fr · 6축 상세 600) → 관리자만 하단 변경 기록. **이번 1단계는 읽기 전용**이다. BE 에 아직 없는 것(축별 이력 API·변경 기록 API·소속/직책 변경 command·행 메뉴 envelope)은 만들지도, 있는 척 그리지도 않는다.

## 3. 계약 (코디 결정 2026-09-07 — BE 가 없는 자리의 처리)

- **데이터는 기존 API 만**: `GET /api/organization/tree`(member_count·leaders 포함) · `units/{id}/members` · `me` · 관리자일 때 `GET /api/access/members/{id}` · `GET /api/access/roles`. `api.ts` 에 **새 엔드포인트 추가 금지** — 응답에 이미 있는 필드의 타입 보강만 허용.
- 관리자 판정 = `me` 의 capability 에 `organization.manage` 가 있는가(현재 `administers` 로직 유지).
- **「이력」 버튼**: 그리되 `disabled` + `title="이력 조회는 준비 중"`. 클릭 동작 없음.
- **「변경」 버튼(소속·직책)**: command 가 없으므로 **그리지 않는다**(SPEC-005 §5). 권한 축의 「변경」만 살린다 — 기존 부여/회수 폼을 `Drawer`(label 「권한 변경」)로 옮긴다. 회수는 `ConfirmModal`(destructive, 사유 필수)로 확인하되 **Drawer 를 닫은 뒤** 띄운다(DS 규칙). 결과는 `Toast`.
- **행 메뉴 `⋯`**: envelope 없음 → 그리지 않는다.
- **사번 자리** = `member.id`(임시 사번 key). **「로그인 계정 있음」 배지**: 응답에 계정 유무가 없으니 그리지 않고 「재직」만.
- **직무 축**: SC 데이터 0 → `EmptyValue`. **회수된 권한**: `access/members` 응답에 회수분이 있으면 그리고 없으면 절 자체를 생략(보고에 어느 쪽이었는지).
- **권한 축(직원 관점)**: 자기 자신이면 `me.grants` 로 채우고, 남이면 값 자리에 `EmptyValue` + 보조설명 「관리 권한이 있는 사람에게만 보입니다」. 403 을 스켈레톤으로 남기는 기존 버그를 고친다 — 실패는 `Empty variant="error"`.
- **변경 기록**(관리자만): API 없음 → 헤더 + `Empty variant="filter" title="이 세션에서 만든 변경이 없습니다"` 만. 테이블 마크업은 만들지 않는다.
- 조직 유형 라벨은 API 의 unit type 이름 그대로(「본부」로 나와도 고치지 않는다 — 카탈로그 소유).
- 사람 표기 유지. `viewModels.ts`·`idempotency.ts`·`backend/` 불변.

## 4. 먼저 읽을 핵심 파일

- `frontend/src/OrgPage.tsx`(현재 414줄 — 상태·fetch 흐름 재사용) · `frontend/src/api.ts` 의 organization/access 타입 · `frontend/src/Modal.tsx`(Drawer·ConfirmModal·Toast 시그니처) · `frontend/src/Empty.tsx` · `frontend/src/styles.css` 의 `.page-head`·`.surface-card`·`.plain-table`·`.avatar`·`.badge`·`.btn`·`.search-input-box`·`.segmented`·`.field`
- `frontend/src/OrgPage.test.tsx`(있으면) · `App.test.tsx` 의 조직 화면 케이스

## 5. allowed_paths — 이 밖은 건드리지 마라

- `frontend/src/OrgPage.tsx` 와 그 하위 컴포넌트 신규 파일(`frontend/src/org/*.tsx` 권장) · 옆자리 테스트 · `frontend/src/labels.ts`(문구) · `frontend/src/styles.css`(최소 추가, hex 금지) · `frontend/src/api.ts`(**타입 보강만**)
- **금지**: 새 fetch 엔드포인트 · `viewModels.ts` · `idempotency.ts` · `App.tsx` 레이아웃 · `ds-entry.tsx` · `.design-sync/` · `backend/` · `package.json` · 커밋·push

## 6. 구현 단계

1. HANDOFF.md 를 끝까지 읽고 「이번에 그리는 것 / 안 그리는 것(§3)」 표를 먼저 써서 보고 초안에 둔다.
2. 페이지 골격: `.page-head` + 배지, 3분할 grid(핸드오프 값 그대로: `minmax(300px,392px) minmax(380px,1fr) minmax(440px,600px)`, gap 24, `calc(100vh - 300px)`/min 560), 패널 3개(외곽 `--border-strong`, r `--radius-panel`, 내부 스크롤·헤더 고정).
3. 패널 ① tree: 펼침(chevron)과 선택을 분리(`expandedOrgIds` Set), 직접/전체 카운트, 리더 `avatar xs`, 이름 검색(구성원 이름으로 트리 필터 — 클라이언트).
4. 패널 ② 목록: 행 68, 사번(`member.id`)·`avatar sm`·이름·소속 요약 「(주) · (겸직)」·직급. 선택 행 `--surface-selected-row`. 로딩은 실제 행 수만큼 `Skeleton`, 실패 `Empty error`.
5. 패널 ③ 상세: 헤더(`avatar lg`·이름 20·사번·「재직」 배지), 축 5행(계층·소속·직책·직급·직무) + 권한 박스. §3 규칙대로 버튼 처리. 관리자 권한 변경은 Drawer 로.
6. 하단 변경 기록(관리자만): 헤더 + Empty.
7. 직원 관점(팀원 1107 로그인)에서 「변경」·행 메뉴·변경 기록이 없는지, 관리자(1001)에서 있는지 확인.
8. 테스트: 관리자/직원 두 관점 렌더, tree 펼침≠선택, 403 → Empty error, 권한 변경 Drawer 열림/회수 ConfirmModal 순서.
9. 5176 에서 **1920 · 1440 · 1280** 세 폭으로 확인(가로 오버플로 0, 패널 내부 스크롤).

## 7. 범위 제약 — 하지 말 것

- BE 가 없는 기능을 그리지 않는다(소속·직책 변경, 행 메뉴, 이력 조회, 변경 기록 테이블). 목업 데이터 금지.
- 새 API·새 의존성·`App.tsx` 셸 변경 금지. Drawer 위에 모달 겹치기 금지.
- 핸드오프의 「프로토타입 전용 좁은 창 CSS」는 옮기지 않는다.
- 핸드오프에 없는 요소를 「보통 이렇다」로 더하지 않는다.

## 8. 검증

```
cd frontend && npx tsc --noEmit (0 에러) + npx vitest run <만진/새 테스트만>. 게이트: grep -o -E '#[0-9a-fA-F]{3,6}\b' src/OrgPage.tsx src/org/*.tsx → 0 · grep -n 'fetch(' src/OrgPage.tsx src/org/*.tsx → 0 · api.ts diff 에 새 request 호출 0 · 세 폭 × 두 관점 화면표(가로 오버플로 0).
전체 빌드·acceptance-e2e 금지 — 사용자 방침. 검증은 1회만
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 보고에 「그린 것 / 안 그린 것과 이유(§3 항목별)」 표 · 회수된 권한 처리 결과 · 변경 파일 · 화면표를 붙인다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_64a88609-f01f-4c9c-942e-e2f3a883dc4d --from term_072aa511-0dd8-4318-8318-769bb9d30ac3 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_64a88609-f01f-4c9c-942e-e2f3a883dc4d \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_64a88609-f01f-4c9c-942e-e2f3a883dc4d --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
