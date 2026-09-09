# [frontend] 조직 화면 2단계 — 읽기 API 소비: 6축 통합 응답 · 축별 이력 · 변경 기록 테이블 · 회수된 권한 · 계정 배지

너는 **sc-ax `frontend` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/roles/sc-ax/frontend/` (처음이면 읽어라).
워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system` (HEAD `5f8b608` — 1단계 화면 `9b437bc` + 팝오버 수정 + BE 읽기 API). API 8001(새 코드, `AX_DEMO_EMAIL_DOMAIN=companysc.com`)·프론트 5176 떠 있음. 로그인 `1001@companysc.com`(대표) / `1141@companysc.com`(팀장) / 비밀번호 `scax-demo-1234`. 부서장 1106·팀원 1107 은 실제 주소라 로그인 화면 목록에서 클릭(도메인 companysc.com). `backend/`·`.design-sync/`·`ds-entry.tsx` 불변.

## 1. SSOT
- 핸드오프: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/reference/2026-09-09-sc-ax-design/org-chart-template/HANDOFF.md` §③ 6축 상세(이력 버튼·회수된 권한·「로그인 계정 있음」 배지) · §하단 변경 기록(테이블 컬럼·빈 상태) · §Interactions.
- 마크업: 같은 폴더 `OrgChart.dc.html`(변경 기록 `.plain-table` 컬럼 폭·축 배지 색·회수된 권한 행).
- 새 API 계약(방금 들어옴): `backend/src/ax_workspace/entrypoints/http.py` 의 `/api/organization/members/{id}` · `/members/{id}/history?axis=` · `/api/organization/activity` 와 `MemberResponse.has_account`; 응답 shape 는 `backend/tests/contract/test_organization_member_axes.py` 가 정본. `docs/domain-model.md` Projection 4줄.
- 1단계 코드: `frontend/src/OrgPage.tsx` · `frontend/src/org/{OrgTreePanel,MemberListPanel,MemberAxesPanel,AccessDrawer}.tsx` · `OrgPage.test.tsx`.

## 2. 배경
1단계는 기존 API 로 현재값만 그렸다(이력 disabled, 변경 기록 빈 상태, 회수된 권한·계정 배지 생략). 이제 읽기 API 가 있으니 그 자리를 채운다. 소속·직책 **변경** command 와 행 메뉴 envelope 는 여전히 없다 — 그대로 그리지 않는다.

## 3. 계약 (코디 결정 2026-09-08)
- **상세 데이터 소스 교체**: 패널 ③ 는 `GET /api/organization/members/{id}` 한 번으로 6축·재직·계정·권한·회수분을 받는다(1단계의 목록 응답 + access/members 조합을 걷어낸다). `api.ts` 에 이 세 엔드포인트의 **request 함수와 타입만** 추가(응답 shape 는 계약 테스트 그대로). 권한 변경 Drawer 의 부여/회수는 기존 `/api/access/*` 유지.
- **「이력」 버튼 활성**: 클릭 → 그 축의 `history?axis=` 를 불러 `Popover`(폭 400, 헤더 「소속 이력」 등 고정, 행: 값 · 기간 tabular · 사유 · 처리자, 최신순, 빈 이력은 `Empty`) 로 보여준다. 403 이면 버튼을 그리지 않는다(응답의 민감 필드가 null 이면 자격 없음으로 간주 — 미리 판단, 호출 후 403 이면 Toast error). 직무 축은 SC 데이터가 0 이라 빈 상태가 정상.
- **회수된 권한** 절: `revoked_grants` 가 1건 이상일 때만 핸드오프 규격으로(11px Bold 헤더 · 12px 행 · 우측 기간 tabular · `--ai-border` 구분선). 3건 초과면 「n건 더 보기」 토글.
- **배지**: `has_account` 로 「로그인 계정 있음」/「계정 없음」(`badge neutral`).
- **변경 기록 테이블**(관리자만): `GET /api/organization/activity?unit_id=<선택 조직>&limit=50` → 핸드오프 `.plain-table`(시각 120 tabular · 변경 280 title-cell · 축 80 배지 · 사유 · 기록자 120). 축 배지: 권한 = `badge ai`, 조직·소속·직책 = `badge neutral`. 0건이면 지금의 `Empty variant="filter"`. cursor 가 오면 「더 보기」 버튼. 선택 조직이 바뀌면 다시 조회.
- 이름 표기: `actor_name`·`display_name` 은 응답 그대로. 사람 표기 유지.
- 안 그리는 것 유지: 소속·직책 「변경」, 행 메뉴 `⋯`. 「변경 기록」 은 관리자만.
- hex 금지 · 새 의존성 금지 · `viewModels.ts`·`idempotency.ts`·`App.tsx` 불변.

## 4. 핵심 파일
- `frontend/src/org/MemberAxesPanel.tsx`(축 행·권한 박스) · `OrgPage.tsx`(fetch 흐름·선택 상태) · `api.ts`(request 패턴) · `Popover.tsx`(방금 max-height 규칙 들어감 — 이력 팝오버가 그 규칙을 받는지 확인) · `Empty.tsx` · `styles.css` 의 `.plain-table`·`.badge`

## 5. allowed_paths
- `frontend/src/OrgPage.tsx` · `frontend/src/org/*` · 옆자리 테스트 · `frontend/src/api.ts`(세 엔드포인트 request+타입 추가만) · `labels.ts` · `styles.css`(최소, hex 0)
- **금지**: `viewModels.ts` · `idempotency.ts` · `App.tsx` · `ds-entry.tsx` · `.design-sync/` · `backend/` · `package.json` · 커밋·push

## 6. 단계 / 8. 검증
1. 계약 테스트에서 응답 shape 를 옮겨 타입 작성 → `api.ts` request 3개. 2. 패널 ③ 데이터 소스 교체(1단계 조합 제거) + 배지 + 회수된 권한. 3. 이력 Popover. 4. 변경 기록 테이블 + 더 보기 + 조직 연동. 5. 테스트: 이력 팝오버 열림·빈 이력·403 처리, 회수된 권한 0/1/4건, 변경 기록 0건/n건/축 배지, 배지 두 값. 6. `npx tsc --noEmit` 0 · `npx vitest run <만진 테스트>` · hex 0 · `fetch(` 0(api.ts 외) · 5176 에서 대표(1001)·팀장(1141) 두 관점 × 1920·1440 확인표(이력 팝오버가 화면 밖으로 안 나가는지 포함). 검증 1회.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_4fcd67c5-63d2-409e-ae57-ef22b8fa5fb1 --from term_072aa511-0dd8-4318-8318-769bb9d30ac3 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_4fcd67c5-63d2-409e-ae57-ef22b8fa5fb1 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_4fcd67c5-63d2-409e-ae57-ef22b8fa5fb1 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
