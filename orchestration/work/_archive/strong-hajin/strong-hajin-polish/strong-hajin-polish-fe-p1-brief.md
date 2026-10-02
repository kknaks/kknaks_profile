# [frontend] WORK-008 Phase 1 — 화면 손질 다섯 (B-02 · F-01 · F-02 · F-03 · D-01)

너는 **strong-hajin `frontend` 워커**다. 앞서 이 워크트리를 조사한 그 워커다(`fe-survey-report.md`). 역할 문서를 다시 확인해라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish`
base: `origin/main`(015bed2) → PR `main`(코디가 올린다)

⚠ 같은 워크트리의 backend 워커는 **대기 중**이다(이번 페이지에 백엔드 변경 없음). `backend/` 를 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- **WP**: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-008-polish.md` — 「이 판의 원칙」 + **Phase 1(1-1 ~ 1-5)** 이 계약이다
- **SPEC (정본 — WP 와 다르면 SPEC 이 맞다. 다르면 코디에게 알려라)**: 같은 레포 `…/strong-hajin/20-spec/`
  - B-02 → SPEC-001 **U-6-a** · §6 만들기 창 AC
  - F-01 → SPEC-007 **§2.9** · §6 (사유 선택 — OQ-710 닫힘)
  - F-03 → SPEC-005 **§2.4**(범위 규칙 정본) · §6 L-53~L-56
  - D-01 → SPEC-001 **U-16** · §6
  - F-02 → SPEC 없음(DS 적용). WP 1-3 이 계약
- 너의 조사 리포트 `…/orchestration/work/strong-hajin-polish/fe-survey-report.md` §1·§2·§3·§4·§8
- 디자인 시스템: 코드 레포 `docs/design/design-system-v2.dc.html` · `docs/design/README.md`

**기대는 개념**: 해당 없음.

## 2. 원칙 — 이 판에서 어기면 FAIL

- **P-2 디자인 시스템 안에서만.** 기존 DS 부품(`Modal` 등)·토큰(`--scax-*`)만 쓴다. 혼자 새 모양을 만들지 않는다. 시안이 없는 자리는 DS-gaps 에 적는다(사용자 지시: 「우리 디자인시스템에 좀 맞춰 혼자 이상하게 만들지 말고」)
- **P-3 쓰는 곳 전부.** WP·리포트의 파일:줄은 **출발점**이다. 바꾸는 심볼·패턴을 쓰는 곳을 **grep 으로 전부 세고** 시작한다. 보고에 「센 것 / 바꾼 것 / 안 바꾼 것과 이유」를 적는다. 특히:
  - B-02: `assigneeId` 를 읽는 곳 전부 · `CreateWorkModal` 을 여는 곳 전부(`initial` 있는/없는)
  - F-02: `type="search"` · 검색칸 클래스(`search-input-box` 등) · 전역 input 규칙
  - F-03·D-01: 날짜 범위 계산(`ganttAxis` · `TaskTimeline` 의 창 계산) · 둘이 쓰는 날짜 유틸
- WP 의 「범위 밖」은 건드리지 않는다(결재자 필터 · 「자료 링크 추가」 인라인 폼)

## 3. 순서

1. **기준선 먼저** — 아무것도 고치기 전에 `make frontend-test` · `npx tsc --noEmit` 를 돌려 **기존 실패**를 적어 둔다(이번 변경과 분리하기 위해)
2. 1-1 B-02 → 1-2 F-01 → 1-3 F-02 → 1-4 F-03 → 1-5 D-01. 각 항목의 WP 체크박스를 하나씩 맞춘다
3. 바뀐 동작마다 테스트를 더한다: B-02(두 갈래 × 담당자 선택 전후의 참조자 목록 · 참조자 체크 해제) · F-01(작은 모달 열기/ESC/성공 후 상세 재조회) · F-03/D-01(월요일 경계 · 범위 밖 업무로 넓힘 · 첫 화면만 넓힘 · 1주 밀기)
4. F-02 는 Tauri 에서 보이는 모양이 계약이다. **너는 앱을 띄우지 않는다** — 코디가 확인한다. 대신 WebKit 기본 꾸밈을 걷는 CSS 를 빠짐없이 넣고 무엇을 넣었는지 보고한다

## 4. allowed_paths

- `frontend/src/` (테스트 포함)
- **금지**: `frontend/src-tauri/` · `backend/` · 문서 레포

## 5. 하지 말 것

- 커밋·push·PR 금지 — 워크트리에 변경만 남긴다
- **서버·프론트를 띄우지 마라. 사용자 포트·프로세스를 건드리지 마라**(8001 · 5176 · 54329). 브라우저·Tauri 를 열지 마라 — 화면 확인은 코디가 한다
- `~/strong-hajin-deploy-data/` 접근 금지
- 결정되지 않은 것을 메우지 마라 — 막히면 아래 [질문]

## 6. 검증

```
코드 레포 AGENTS.md 준수: make frontend-test 및 frontend에서 npx tsc --noEmit, 최종 빌드는 make frontend-build. 같은 검증 중복 실행 금지. envelope으로 권한 판단, api.ts 밖 fetch 금지, 기존 부품/viewModels 재사용, 시안 부재는 DS-gaps 기록. 실제 실행하지 못한 검증은 사유와 함께 pending으로 보고.
```

- 기준선 대비 **새 실패 0**. 기존 실패는 「무관」으로 분리 보고

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 작성 시점 값이다.

```bash
orca orchestration send \
  --to term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 완료: WORK-008 Phase 1" \
  --body "변경 파일 / 항목별(1-1~1-5) 계약 체크 / 전수조사(센 것·바꾼 것·안 바꾼 것) / 기준선 vs 결과(테스트 수·tsc·build) / DS-gaps / 미결·주의"

orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 \
  --text "[worker_done] frontend 완료 — WORK-008 Phase 1. 상세는 인박스." --enter
```

막히면 30분 넘게 헤매지 말고: `orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --text "[질문] frontend: <질문>" --enter`
