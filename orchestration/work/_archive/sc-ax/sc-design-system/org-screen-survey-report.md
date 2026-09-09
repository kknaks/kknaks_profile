# 조직 화면 v3 ↔ 현재 구현 대조 + SC 조직도 CSV → dataset 매핑 (조사)

- 조사일: 2026-09-07 · 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system` (HEAD `922ed65`)
- 화면 SoT: `reference/2026-09-09-sc-ax-design/조직 화면 v3 (standalone).html` — 396번째 줄의 JSON 문자열을 풀어 84KB HTML 을 얻었고, Playwright 로 아트보드 3개(각 1920×1080)를 캡처해 텍스트와 시각을 교차 확인했다. 캡처: `org-v3-shots/01_관리자.png` · `02_직원.png` · `03_소속_변경_모달.png`
- 데이터 SoT: `reference/2026-09-04-SC-org_data/…상세추가.csv` (169행 · 14열) — **구조와 개수만 인용한다**
- SPEC: 코디 정정에 따라 `orchestration/work/sc-design-system/ref-spec-main/` 사본(spec-005 v0.2.0 등)을 근거로 삼았다. canonical mediness 체크아웃은 쓰지 않았다.

---

## 요약 (5줄)

1. **v3 는 v2 와 거의 충돌하지 않는다.** 3분할이 정확히 **392 / 600 / 600 + 거터 24 = 1640** 으로 v2 `05` Dashboard 3열·`04` 콘텐츠 폭과 같고, v3 스타일시트는 v2 토큰 값을 그대로 쓴다. 브리프의 「v3 는 v2 와 안 맞는다」 전제는 **레이아웃·토큰 값 수준에서는 성립하지 않는다**(실제 충돌 3건은 §5).
2. **데이터 모델은 이미 v3 를 감당한다.** `memberships`·`appointments`·`grade_assignments`·`access_grants` 가 전부 `valid_from/valid_until` 을 갖고, `memberships.change_reason_ref`·`appointments.change_reason_ref`·`access_grants.revoked_at`·`ActivityEventRecord`(actor·reason·before/after) 가 있어 v3 의 이력·회수된 권한·변경 기록이 **저장 계층에서는 나온다**.
3. **막힌 곳은 command 와 API 다.** 조직 API 는 GET 4개뿐이고, 소속·직책을 바꾸는 command 가 **BE 에 아예 없다**(`administration.py` 는 grant/revoke/role 편집만). v3 의 「변경」 3개 중 **권한만 이미 있고 소속·직책은 BE 신규**다.
4. **CSV 는 6표 중 4표를 채우고 2표를 못 채운다.** `organization_units` 29 · `grades` 10 · `positions` 3 · `members` 165 · `memberships` 169 · `appointments` 22 는 나오지만, **`jobs`/`job_assignments` 는 0행**(CSV 에 직무 열이 없다) 이라 v3 의 직무 축은 비고, 입사일은 165명 중 **15명만** 있다.
5. **v3 의 4단 계층(회사›본부›실›팀)도 SC 데이터로는 3단까지만 채워진다** — CSV 는 부서·팀 2열뿐이라 「실」 단계가 없다.

---

## v3 해부 (아트보드별)

아래 요소 번호는 §3 대조표의 행과 1:1로 대응한다 (총 **50개**).

### 공통 셸 (아트보드 1·2·3 공통)

| # | 요소 | 요구 데이터 |
|---|---|---|
| A1 | 좌측 사이드바 200px · Ink pill active · 항목 8개(오늘·캘린더·내 업무·보고·자료·조직·설정 등) | 네비 목록 |
| A2 | 페이지 헤더: 타이틀 「조직」 + 원칙 문장(「여섯 축은 서로 독립입니다…」) | 정적 카피 |
| A3 | 우상단 배지 「조직 관리 권한 있음」 | 현재 principal 의 조직 관리 capability 보유 여부 |
| A4 | 하단 중앙 AX 바 720×52 · placeholder 「사람 이름이나 조직을 물어보세요」 | 없음(입력) |

### ② 조직 tree 패널 (폭 392)

| # | 요소 | 요구 데이터 |
|---|---|---|
| B1 | 패널 헤더 「조직 tree」 + 태그 「읽기 전용」 | — |
| B2 | 검색창 「사람 이름 검색」 | 사람 이름 인덱스(조직 트리 안에서) |
| B3 | 4단 계층 노드 (회사 › 본부 › 실 › 팀) | `unit.parent_id` 계층 |
| B4 | 노드별 종류 라벨 (회사/본부/실/팀) | `unit.unit_type` |
| B5 | 노드별 **「직접 N · 전체 M」** | 노드별 직접·전체 인원 수 |
| B6 | 노드별 **조직장 이름 + 아바타** (트리 우측 정렬) | 노드별 조직장(이름) |
| B7 | 펼침/접힘 캐럿 | — (화면 상태) |
| B8 | 선택 노드 하이라이트 | — (화면 상태) |

### ③ 구성원 목록 패널 (폭 600)

| # | 요소 | 요구 데이터 |
|---|---|---|
| C1 | 헤더 「{조직명} 구성원」 + 우측 「직접 소속 N명」 | 선택 노드의 직접 인원 수 |
| C2 | 행: **사번** (4자리) | 사번 |
| C3 | 행: 아바타 + 이름 | 이름 |
| C4 | 행: 소속 표시 「A (주) · B (겸직)」 복수 | 그 사람의 소속 전체 + 주/겸직 구분 |
| C5 | 행: 우측 직급 | 직급 |
| C6 | 행: **⋯ 메뉴** | 그 사람에게 가능한 행동 목록 |
| C7 | 선택 행 하이라이트 | — (화면 상태) |

### ④ 6축 상세 카드 (폭 600)

| # | 요소 | 요구 데이터 |
|---|---|---|
| D1 | 헤더: 아바타 + 이름 + 사번 | 이름·사번 |
| D2 | 헤더 배지 2개: 「재직」 · 「로그인 계정 있음」 + 문구 「재직과 계정은 다른 축입니다」 | `employment_state`, 계정 존재 여부 |
| D3 | **계층** 축: 「더에스씨 › 제품본부 › 제품기획팀」 + `이력` | 주소속의 조상 경로 + 그 경로의 이력 |
| D4 | **소속** 축: 「A (주) · B (겸직)」 + `이력` + **`변경`** | 소속 목록·기간 이력 |
| D5 | **직책** 축: 값 또는 `—` + `이력` + **`변경`** | 보직·기간 이력 |
| D6 | **직급** 축: 값 + `이력` (변경 버튼 **없음** — 「이 화면에서 바꾸지 않습니다」) | 직급·기간 이력 |
| D7 | **직무** 축: 「제품기획 (주) · UX리서치 (보조)」 + `이력` (변경 없음) | 직무 배정·주/보조·기간 이력 |
| D8 | **권한** 축: 「역할 · 범위」 목록 + `이력` + **`변경`**, 연보라 강조 박스 | 유효 grant 의 역할명·scope |
| D9 | **회수된 권한**: 「역할 · 범위」 + **기간(YYYY.MM.DD – YYYY.MM.DD)** + 「N건 더 보기」 | 회수된 grant 의 역할·scope·유효기간 |
| D10 | 축마다 원칙 문구 1줄 (6개) | 정적 카피 |

### ⑤ 변경 기록 (관리자 전용, 폭 1640)

| # | 요소 | 요구 데이터 |
|---|---|---|
| E1 | 패널 헤더 + 설명 「하나의 임명이 두 줄로 남습니다」 | — |
| E2 | 행: 시각 (「오늘 09:12」 / 「08.27 10:05」) | 발생 시각 |
| E3 | 행: 요약 「{사람} · {사건}」 | 요약문 |
| E4 | 행: **축 태그 칩** (조직 / 권한 / 소속) | 사건이 속한 축 |
| E5 | 행: 사유 | 변경 사유 |
| E6 | 행: 우측 처리자 이름 | actor |

### 아트보드 2 — 직원 관점 (읽기 전용)

| # | 요소 | 차이 |
|---|---|---|
| F1 | 6축 카드의 **「변경」 버튼 3개 미렌더** | D4·D5·D8 의 변경만 빠지고 `이력`은 남는다 |
| F2 | **⑤ 변경 기록 패널 자체를 렌더하지 않음** | — |
| F3 | 거부 박스 없음 (권한 없음 안내를 띄우지 않는다) | — |
| F4 | 권한 축의 **연보라 강조 박스도 없음** (평범한 축으로 렌더) | 캡처 `02_직원.png` 확인 |

### 아트보드 3 — M1 소속 변경 모달

필드 순서: **대상 → 값 → 적용일 → 미리보기 → 딸린 권한 체크 → 사유**

| # | 요소 | 요구 데이터 / 동작 |
|---|---|---|
| G1 | 헤더: 이름 · 「{사번} · {직급}」 + 「현재 소속」 표시 | 현재 소속 |
| G2 | **옮길 조직** 선택 | 선택 가능한 조직 목록 |
| G3 | **적용일** | 날짜 |
| G4 | **소속 종류**: 주소속 / 겸직 (택1) | `membership_kind` |
| G5 | 「겸직 해제」 | 기존 겸직 종료 |
| G6 | **미리보기** before/after + 문장(「…09월 06일로 종료됩니다. 계층 표시가 …로 바뀝니다」 / 「직급·직무·직책은 이 변경으로 바뀌지 않습니다」) | 서버가 계산한 변경 예상 |
| G7 | 체크 「새 조직의 표준 역할을 함께 부여」 (기본 켬) | `StandardGrantRule` |
| G8 | 체크 「이전 소속에서 받은 역할을 함께 회수」 (**주소속일 때만 활성**, 기본 끔) | 이전 소속 유래 grant |
| G9 | **사유** (필수 — 「사유를 적어야 저장할 수 있습니다」, 비면 저장 불가) | 사유 텍스트 |
| G10 | 확인 다이얼로그 「주소속을 교체할까요?」 / 「주소속 교체」 | — |
| G11 | 취소 / 저장 | — |

> 모달의 상태는 번들 안 `class Component extends DCLogic` 의 `state = { kind, grantStd, revokePrev, reason, confirmOpen }` 로 확정했다 — 추측이 아니다.

---

## 대조표 (50행)

분류: **FE** = 프론트만으로 가능 · **노출** = BE operation 은 있고 API/화면 노출만 필요 · **BE** = BE 신규 필요

| # | 요소 | 현재 | 근거 | 분류 |
|---|---|---|---|---|
| A1 | 사이드바 200 Ink pill | **부분** | `App.tsx:274` `.rail`, 네비 7개(`App.tsx:19-25`). v3 의 **자료·설정 2개가 없다** | FE(+별도 스펙) |
| A2 | 페이지 헤더 + 원칙 문장 | **부분** | `OrgPage.tsx:212` `page-surface` — 원칙 문장 없음 | FE |
| A3 | 「조직 관리 권한 있음」 배지 | **없음** | capability 는 `OrganizationProfile.capabilities`(`viewModels.ts:373`)에 있으나 배지 미구현 | FE |
| A4 | 하단 AX 바 720×52 | **부분** | 홈에만 있음(`TodayPage.tsx` `.ax-prompt`), 조직 화면엔 없음. 전역 AX 는 `ax-launcher`(`App.tsx`) | FE |
| B1 | tree 패널 헤더 + 읽기 전용 태그 | **부분** | `OrgPage.tsx:224` `.org-tree` — 태그 없음 | FE |
| B2 | 사람 이름 검색창 | **없음** | OrgPage 에 검색 입력 없음 | FE(클라 필터) 또는 BE(서버 검색) |
| B3 | 4단 계층 노드 | **있음** | `OrganizationUnitNode.parent_id`(`viewModels.ts:630`), `GET /api/organization/tree`(`http.py:897`) | FE |
| B4 | 노드별 종류 라벨 | **있음** | `OrganizationUnitNode.unit_type`(`viewModels.ts:631`) | FE |
| B5 | 「직접 N · 전체 M」 | **있음** | `member_count`·`direct_member_count`(`viewModels.ts:634-635`) — **이미 응답에 있다** | FE |
| B6 | 노드별 조직장 이름 | **있음** | `OrganizationUnitNode.leaders[]{display_name, position, kind}`(`viewModels.ts:636`) | FE |
| B7 | 펼침/접힘 캐럿 | **있음** | `OrgPage.tsx:183` `isCollapsed` + `Icon chevron` | FE |
| B8 | 선택 노드 하이라이트 | **있음** | `OrgPage.tsx:165` `.org-node.selected` | FE |
| C1 | 「{조직} 구성원」 + 직접 N명 | **부분** | `OrgPage.tsx:236` `.member-list`, `GET /units/{id}/members`(`http.py:901`). 헤더 카운트 문구는 미구현이나 B5 값으로 가능 | FE |
| C2 | 행: **사번** | **없음** | `OrganizationMember`(`viewModels.ts:639`)·`members` 테이블(`persistence.py:42`) 모두 사번 컬럼 없음 | **BE**(스키마 게이트) |
| C3 | 행: 아바타 + 이름 | **있음** | `OrganizationMember.display_name`, `.avatar`(v2 2차-a) | FE |
| C4 | 행: 소속 「(주)/(겸직)」 복수 | **있음** | `OrganizationMember.memberships[]{organization_name, kind}`(`viewModels.ts:642`) | FE |
| C5 | 행: 직급 | **있음** | `OrganizationMember.grade`(`viewModels.ts:645`) | FE |
| C6 | 행: ⋯ 메뉴 | **없음** | 행 단위 액션 메뉴 없음. 선택지는 서버가 줘야 한다(`rules.md` 권한 추론 금지) | **BE**(가능 행동 목록) + FE(Popover 재사용) |
| C7 | 선택 행 하이라이트 | **있음** | `OrgPage.tsx:240` `.member-row.selected`(v2 2차-a 에서 `--surface-selected-row` 로 분리) | FE |
| D1 | 헤더 이름 + 사번 | **부분** | 이름 `OrgPage.tsx:280`; 사번은 C2 와 동일 부재 | BE |
| D2 | 배지 「재직」·「로그인 계정 있음」 | **없음** | `members.employment_state`·`account_ref`(`persistence.py:47,50`)에 값은 있으나 **API 응답에 없다** | **BE**(응답 확장) |
| D3 | 계층 축 (경로) | **부분** | 트리로 계산 가능(FE). **경로 이력**은 저장은 되나(`memberships.valid_*`) API 없음 | FE(현재값) + BE(이력) |
| D4 | 소속 축 + 이력 + 변경 | **부분** | 현재값 있음(C4). **이력 API 없음**, **변경 command 자체가 BE 에 없음**(`administration.py` 에 membership 메서드 0개) | **BE**(이력 + command) |
| D5 | 직책 축 + 이력 + 변경 | **부분** | 현재값 `OrganizationMember.positions[]`(`viewModels.ts:643`). 이력·변경 없음(`appointments` 테이블만 존재) | **BE**(이력 + command) |
| D6 | 직급 축 + 이력 | **부분** | 현재값 있음(C5). 이력은 `grade_assignments.valid_*`(`persistence.py:113`)에 있으나 API 없음 | BE(이력만) |
| D7 | 직무 축 (주/보조) + 이력 | **부분** | `OrganizationMember.jobs: string[]`(`viewModels.ts:646`) — **주/보조 구분이 없다**(단순 문자열 배열). `job_assignments` 는 `kind` 를 가짐 | **BE**(응답에 kind 추가 + 이력) |
| D8 | 권한 축 + 이력 + 변경 | **있음(변경)** / 부분(이력) | `GET /api/access/members/{id}`(`http.py:849`), `POST /api/access/grants`(`856`), `POST …/revoke`(`873`). **변경은 이미 있다** — SPEC-005 §5 「현재 제공 범위」 | **노출** + BE(이력) |
| D9 | 회수된 권한 + 기간 | **부분** | `access_grants.revoked_at`·`valid_from`·`valid_until`(`persistence.py:209+`) 저장됨. `MemberAccess.grants`(`viewModels.ts:365`)가 **회수분을 포함하는지 확인 필요** | 노출 또는 BE |
| D10 | 축별 원칙 문구 6개 | **없음** | 정적 카피 — `labels.ts` 로 | FE |
| E1 | 변경 기록 패널 | **없음** | OrgPage 에 없음 | FE |
| E2 | 행: 시각 | **있음(저장)** | `ActivityEventRecord.occurred_at`(`platform/organization_access.py:340+`) | **BE**(조회 API) |
| E3 | 행: 요약 | **있음(저장)** | 같은 레코드 `safe_summary` | BE |
| E4 | 행: 축 태그 칩 | **부분** | `event_kind` 는 있으나 **축(조직/권한/소속) 분류가 정의되어 있는지 확인 필요** | BE |
| E5 | 행: 사유 | **있음(저장)** | 같은 레코드 `reason`; `revoke_grant(reason=…)`(`administration.py:138`) | BE |
| E6 | 행: 처리자 | **있음(저장)** | 같은 레코드 `actor_id` | BE |
| F1 | 직원: 변경 버튼 미렌더 | **부분** | OrgPage 는 `canAdministerAccess` 류로 권한 패널을 가림(`OrgPage.tsx:303`). v3 규칙에 맞춘 세분화 필요 | FE |
| F2 | 직원: 변경 기록 미렌더 | **없음** | E1 이 없으므로 해당 없음 | FE |
| F3 | 직원: 거부 박스 없음 | **확인 필요** | 현재 권한 없을 때 무엇을 그리는지 미확인 | FE |
| F4 | 직원: 권한 축 강조 없음 | **없음** | D8 강조 자체가 미구현 | FE |
| G1 | 모달 헤더 + 현재 소속 | **없음** | 소속 변경 모달 없음 | FE |
| G2 | 옮길 조직 선택 | **없음** | 트리 데이터로 목록화 가능 | FE |
| G3 | 적용일 | **없음** | `DateField` 재사용 가능 | FE |
| G4 | 소속 종류 주/겸직 | **없음** | v2 Radio 는 2차-a 에서 「대응 자리 없음」으로 안 만들었다 — **여기가 첫 소비처** | FE(Radio 신규) |
| G5 | 겸직 해제 | **없음** | — | BE(command) |
| G6 | 미리보기 before/after | **없음** | **서버가 계산해야 한다** — FE 가 계층 변화를 추론하면 `rules.md` 위반 | **BE**(preview) |
| G7 | 「표준 역할 함께 부여」 | **부분** | `standard_grant_rules` 테이블(`persistence.py:195`) 존재. command 노출 없음 | BE |
| G8 | 「이전 역할 함께 회수」(주소속만) | **부분** | `revoke_grant` 는 있음(`administration.py:138`). 「이전 소속 유래」 판별은 `access_grants.origin_rule_id` 로 가능 | BE |
| G9 | 사유 필수 | **부분** | `revoke_grant(reason)` 은 받음. 소속 변경 command 가 없어 미적용. FE 검증은 v2 2차-a `FieldMessage` 재사용 | FE + BE |
| G10 | 확인 다이얼로그 | **없음** | v2 `14` Modal(600) 재사용 | FE |
| G11 | 취소 / 저장 | **없음** | — | FE |

**집계**: 있음 12 · 부분 20 · 없음 18 = **50행** (§2 해부 목록 50개와 일치).
분류: FE 만 **23** · 노출 **2** · BE 신규 **15** · 혼합/확인 필요 **10**.

---

## BE 가 새로 필요한 것 (엔드포인트 제안)

SPEC-005 근거 절을 함께 적는다. **제안일 뿐 판정이 아니다.**

| # | 제안 | 응답/요청 shape (개략) | SPEC 근거 |
|---|---|---|---|
| BE-1 | `GET /api/organization/members/{id}` — 6축 한 번에 | `{member_id, employee_no?, display_name, employment_state, has_account, hierarchy_path[], memberships[]{unit,kind,valid_from,valid_until}, appointments[], grade, jobs[]{name,kind}, grants[], revoked_grants[]{role,scope,valid_from,valid_until}}` | §2 「재직·계정·소속·보직·직급·직무는 서로 다른 사실이며 **각각의 기간을 보존한다**」 |
| BE-2 | `GET /api/organization/members/{id}/history?axis=` | 축별 `[{value, valid_from, valid_until, reason, actor}]` | §2 같은 절(기간 보존) |
| BE-3 | `POST /api/organization/members/{id}/membership` — 소속 변경 | req `{unit_key, kind, effective_on, grant_standard_role, revoke_previous_roles, reason}` · res 변경 결과 | §5 「UI 가 제공하지 않는 기능을 사용 가능한 관리 기능처럼 표시하지 않는다」 — 역으로 **command 없이 변경 버튼을 그리면 안 된다** |
| BE-4 | `POST /api/organization/members/{id}/membership/preview` — G6 | req 동일 · res `{before[], after[], effects[]}` | §2·§3 (권한 축은 섞지 않는다 → 미리보기가 「직급·직무·직책은 안 바뀐다」를 서버 사실로 말해야) |
| BE-5 | `POST /api/organization/members/{id}/appointment` — 직책 임명/해제 | req `{unit_key, position_key, kind, effective_on, reason}` | §2 |
| BE-6 | `GET /api/organization/activity?unit=&limit=` — ⑤ 변경 기록 | `[{occurred_at, axis, summary, reason, actor_name, target}]` | §3 「grant 변경은 version 을 가지며」 + 기존 `ActivityEventRecord` |
| BE-7 | `MemberResponse` 확장 — 사번·재직·계정 유무·직무 kind | C2·D2·D7 | §2 「결과 field 는 현재 Principal 의 권한에 맞게 제한한다」 |
| BE-8 | 구성원 행 `⋯` 의 가능한 행동 목록 | `allowed_commands[]` 형태 (다른 화면의 envelope 와 같은 계약) | `rules.md` 「권한·가능한 행동은 envelope 로만 판단」 |

> **사번(BE-7)은 스키마 게이트다** — `members` 테이블에 컬럼이 없고 dataset `members` 표에도 없다. CSV 에도 사번 열이 없어 **SC 데이터로는 채울 수 없다**(§7).

---

## v2 ↔ v3 충돌 (판정 없이 목록만)

v3 스타일시트는 v2 토큰을 **그대로 정의해 쓴다**(`--content-w: 1640px`, `--control-h-md: 34px`, `--space-*`, `--radius-panel`). 그래서 충돌은 3건뿐이다.

| # | 항목 | v2 | v3 | 비고 |
|---|---|---|---|---|
| X1 | **토큰 이름 층위** | `01` 「화면에서는 **Semantic 이름만** 씁니다 — `gray-500` 이 아니라 Text Tertiary」 | v3 는 `--gray-500`·`--indigo-600`·`--space-16`·`--font-size-label-1` 등 **primitive 이름을 화면에서 직접 쓴다**(우리 `:root` 에 없는 이름 **54개**) | **값은 같다.** 이름 층위만 다름 |
| X2 | **막힘 상태 색** | `02` 상태 5종, 지연=red. 우리 구현은 `blocked`→danger(red) | v3 는 `--orange-500/700/050`(`#E1872D`/`#AF6419`/`#FBF4EC`)로 **`--status-blocked-*` 별도 축**을 만든다 | v2 에 없는 **6번째 상태 색** |
| X3 | **아키타입** | `05` List = 단일 8col 패널 / Dashboard = 3열 392·600·600 | 조직 화면이 **Dashboard 3열 + 하단 전폭 패널(⑤)** 형태 | 폭은 v2 와 동일(1640). 「조직 = 어느 아키타입인가」가 미정의 |
| X4 | (참고) `--surface-default` | 1차에서 **정의 없는 토큰**으로 판명돼 `--surface` 로 치환했다 | v3 가 이 이름을 쓴다 | 이름만 되살릴지 여부 |

---

## CSV → dataset 매핑표

CSV: **169행 · 14열**(부서·팀·이름·직급·고용형태·직책·비고·메모·입사일·생년월일·전화·지메일·위하고메일·담당 프로젝트).
미반입 열(§3): 전화·생년월일·지메일·위하고메일·메모.

### 표별 매핑과 예상 행수

| 표 | 예상 행수 | 열 매핑 | enum 대응 |
|---|---|---|---|
| `organization_units` | **29** | 회사 루트 1 + 부서 10 → `division` + 팀 18 → `team`. `key`=slug, `name`=원문, `parent_key`=부서(팀의 경우)/회사(부서의 경우) | `unit_type`: `company` 1 · `division` 10 · `team` 18. **`office`·`part` 미사용** |
| `grades` | **10** | 직급 10종 → `key`/`name`, `display_order` 는 직위 순서로 부여 | — |
| `positions` | **3** | 부서장→(`division`,`head`) · 팀장→(`team`,`head`) · 부팀장→(`team`,`deputy`) | `slot`: head 2 · deputy 1. `role_key` 는 `team-lead` 또는 비움 |
| `members` | **165** | `display_name`=이름, `primary_unit_key`=팀 있으면 팀·없으면 부서, `grade_key`=직급, `employment_type`=고용형태, `employed_from`=입사일 | `employment_state`: 전원 `active`(**확인 필요** — CSV 에 퇴사 표시 열 없음) · `employment_type`: `regular` 124 · `part_time` 39 · **빈값 2**(비워 둠) · `contract` 미사용 · `role_key`: `executive` **2** · `team-lead` **18** · `member` **145** |
| `memberships` | **169** | 주소속 165 + 겸임 4 | `kind`: `primary` 165 · `additional` 4 |
| `appointments` | **22** | 직책 있는 행마다 1행 (부서장 6 · 팀장 15 · 부팀장 1) | `kind`: `primary`/`concurrent` — 겸임자의 5건을 어떻게 볼지 **미결** |
| `jobs` / `job_assignments` | **0 / 0** | **CSV 에 직무 열이 없다** | — |
| `projects` / `project_assignments` | **12 / 12** (반입 여부 미결) | 담당 프로젝트 12행·12개 고유값 | `state` 미상(비움) · `kind`: 전원 `lead`? **미결** |
| `logins` | **0** | §3 「안 만듦」 | — |

### 특이 케이스

| # | 케이스 | 실제 | 제안 |
|---|---|---|---|
| S1 | **겸임 1명이 5행** | 한 사람이 글로벌사업부의 **팀 5곳 팀장**, 5행 모두 `비고=겸임`·동명 | 1 member + `memberships` 5(주 1 + 겸임 4) + `appointments` 5. **어느 팀이 주소속인지 CSV 가 말하지 않는다** → 미결 |
| S2 | **동명이인 2명** | 같은 이름 2행, 둘 다 국내사업부·팀 없음, **직급이 과장/사원으로 다름** | 별개 member 2개로 분리. `key` 를 이름만으로 만들면 충돌하므로 **직급·순번 등으로 구분자 필요** |
| S3 | **부서 단계의 팀장 1명** | 직책 `팀장`인데 팀 없이 **부서 소속** | `positions` 에 (`division`,`head`) 가 이미 부서장이라 **slot 충돌**. 부서장으로 볼지 팀장 정의를 division 에도 둘지 미결 |
| S4 | **입사일 154행 없음** | 165명 중 **15명만** 입사일 보유 | `employed_from` 비움 — 스키마 note 「원문에 없는 발령 효력일은 비워 둔다 — 만들어 내지 않는다」 그대로 |
| S5 | **고용형태 2행 없음** | 정규직 124 · 시간제 39 · 빈값 2 | 비워 둠(선택 열) |
| S6 | **「경영진」·「기타」** | 경영진 2명(둘 다 대표이사) · 기타 5명(이사 2·사원 3) | §3 대로 `division` 으로 유지 |
| S7 | **대표이사 2명** | 공동 대표. 둘 다 직책 열은 **비어 있다** | `role_key=executive`. `positions` 에 대표이사 정의를 둘지, `appointments` 를 만들지 미결 |
| S8 | 팀 이름 전역 유일 | 18개 팀명이 **부서를 넘어 겹치지 않음** | 팀 `key` 를 팀명 slug 단독으로 만들 수 있다 |

### `dataset-import --dry-run` 통과 조건

`modules/datasets/validation.py` 가 검사하는 것은 7가지다 — `missing_file`(표 파일 누락) · `duplicate`(key 중복, `unique` 조합 중복) · `missing_value`(required 열 빈값) · `unknown_value`(enum 밖 값) · `unknown_reference`(FK 가 없는 키를 가리킴) · `unknown_column`(표에 없는 열) · `cycles`(parent 순환).

따라서 통과 조건: **(1)** 11개 표 파일이 모두 있어야 한다(빈 표라도 헤더 필요 — `jobs`·`job_assignments`·`logins` 포함) **(2)** `members.key` 유일 → S2 해결 필수 **(3)** `memberships` 는 (member_key, unit_key) 유일 → S1 의 5행이 서로 다른 unit 이라 통과 **(4)** `appointments` 는 (member_key, unit_key, position_key) 유일 **(5)** enum 은 위 표의 값만 **(6)** `organization_units.parent_key` 에 순환이 없어야 한다.

> **본 조사에서 폴더 생성·import·`--dry-run` 실행은 하지 않았다**(§7).

---

## v3 가 SC 데이터로 채워지지 않는 영역

| 영역 | 채워지나 | 이유 |
|---|---|---|
| B3 4단 계층(회사›본부›실›팀) | **부분** | CSV 는 부서·팀 2열 → **3단까지만**. 「실」 단계 없음 |
| B5 직접/전체 인원 | ✅ | 소속에서 계산 |
| B6 노드별 조직장 | **부분** | 부서장·팀장이 있는 곳만. 부서 10 중 **6곳만 부서장**, 팀 18 중 **14곳만 팀장** |
| C2·D1 사번 | ❌ | **CSV 에 사번 열이 없다** |
| C5 직급 | ✅ | 10종 |
| D2 재직 배지 | **부분** | 전원 active 로 넣는 것이라 「재직」만 나온다 |
| D2 로그인 계정 배지 | ❌ | §3 `logins` 안 만듦 → 전원 「계정 없음」 |
| D4 소속(주/겸직) | ✅ | 겸임 1명이 실제 사례가 된다 |
| D5 직책 | ✅ | 22건 |
| D7 **직무** | ❌ | **CSV 에 직무 열이 없다** → 축 전체가 빈다 |
| D8 권한 | **부분** | `role_key` 3종에서 표준 grant 가 파생되지만, v3 가 보여 주는 「업무 열람 · 제품본부」 같은 **scope 별 grant 는 시드에 없다** |
| D9 회수된 권한 | ❌ | 과거 회수 이력이 CSV 에 없다 |
| D3~D8 **이력** | ❌ | CSV 는 **현재 시점 스냅샷 1장**이라 기간·과거값이 없다. 입사일도 15명뿐 |
| E ⑤ 변경 기록 | ❌ | 시드에는 변경 사건이 없다(임포트 자체를 사건으로 남길지는 미결) |
| G 소속 변경 모달 | — | 데이터가 아니라 command 문제 |

> 요약하면 **v3 의 「현재값」 축은 대부분 채워지고, 「이력·회수·변경 기록」 축은 시드로는 전부 빈다.** 이력은 제품을 쓰기 시작해야 쌓인다.

---

## 우선순위 제안 (근거 포함)

| 순 | 묶음 | 내용 | 근거 |
|---|---|---|---|
| 1 | **시드** | CSV → dataset 6표(+빈 표 5). S1~S3 를 먼저 결정해야 `--dry-run` 이 통과한다 | 다른 모든 작업이 「사람이 실제로 있는 화면」을 필요로 한다. FE·BE 와 독립 |
| 2 | **BE-7 응답 확장** | 사번(스키마 게이트)·재직·계정 유무·직무 kind | C2·D1·D2·D7 이 한 번에 풀린다. 화면 변경 없이 선행 가능 |
| 3 | **FE 읽기 전용 v3** | ②③④ 3열(392/600/600) + B5·B6 + 6축 카드의 **현재값과 이력 버튼(비활성)** | 대조표의 **FE 23건 중 대부분**이 여기. 이미 있는 데이터(B3~B8·C3~C7)로 화면의 뼈대가 선다. v2 3열은 3차에서 이미 구현돼 재사용 |
| 4 | **BE-1·BE-2** | 6축 통합 조회 + 축별 이력 | 3의 「이력」 버튼을 실제로 연다. SPEC-005 §2 의 기간 보존이 근거 |
| 5 | **BE-6 + FE ⑤** | 변경 기록 조회 API + 패널 | `ActivityEventRecord` 가 이미 쌓고 있어 **읽기만 열면 된다** — 비용 대비 효과가 크다 |
| 6 | **BE-3·4·5 + FE M1** | 소속·직책 변경 command + 미리보기 + 모달 | 가장 무겁고, SPEC-005 §5 상 **command 없이 버튼을 먼저 그리면 안 된다**. G4 는 v2 Radio 의 첫 소비처가 된다 |
| 7 | **BE-8 + C6** | 행 `⋯` 의 envelope | 6이 정해져야 「가능한 행동」이 정의된다 |

---

## 미결 · 확인 필요

1. **[중대] 사번** — v3 가 목록·상세에서 사번을 1급 식별자로 쓰는데 `members` 테이블·dataset 표·CSV **셋 다 없다**. 스키마 게이트이며, SC 데이터로는 채울 수도 없다. 대체 식별자(키)로 갈지 결정 필요.
2. **[중대] 겸임자의 주소속(S1)** — 5개 팀 중 어디가 주소속인지 CSV 가 말하지 않는다. `members.primary_unit_key` 가 required 라 **결정 없이는 import 가 안 된다**.
3. **[중대] 동명이인 key(S2)** — `members.key` 유일성 때문에 구분자 규칙이 필요하다.
4. **부서 단계 팀장(S3)** — `positions` 의 slot 충돌.
5. **대표이사 표현(S7)** — `role_key=executive` 는 정해졌으나 `positions`/`appointments` 를 둘지 미정. 직책 열이 비어 있다.
6. **`employment_state`** — CSV 에 퇴사 표시가 없어 전원 `active` 로 가정했다. 맞는지 확인 필요.
7. **`MemberAccess.grants` 가 회수분을 포함하는가**(D9) — 포함하면 「노출」, 아니면 BE 신규.
8. **`ActivityEventRecord.event_kind` 에 축 분류가 있는가**(E4) — v3 의 축 태그 칩이 여기서 나와야 한다.
9. **프로젝트 12건 반입 여부**(§3 미결) — `projects`·`project_assignments` 는 가능하나 `kind`(lead/member)를 CSV 가 말하지 않는다.
10. **v3 사이드바의 「자료」·「설정」** — 현재 앱에 없는 화면이다. 별도 스펙.
11. **X2 막힘 색** — v2 에 없는 orange 축을 v2 에 등록할지, v3 를 v2 에 맞출지.
12. **조직 화면의 아키타입**(X3) — v2 `05` 에 「조직」이 없다.
13. **F3 거부 박스** — 권한 없는 사용자에게 현재 무엇을 그리는지 확인하지 못했다.

---

## 자체 점검 (§8)

**(1) v3 요소 전부가 대조표 행으로 있는가** — ✅ 해부 목록 A1–A4(4) · B1–B8(8) · C1–C7(7) · D1–D10(10) · E1–E6(6) · F1–F4(4) · G1–G11(11) = **50개**, 대조표 = **50행**. 번호가 1:1 대응한다.

**(2) 대조표 모든 행에 파일:줄 또는 「없음」 근거가 있는가** — ✅ 50행 전부에 근거 열이 있다. 「있음/부분」 32행은 `파일:줄`(`viewModels.ts:630` · `http.py:897` · `persistence.py:209` 등), 「없음」 18행은 부재 사유를 적었다. 근거를 못 댄 2건(F3 거부 박스, E4 축 분류)은 **확인 필요**로 표시하고 미결 13·8번에 올렸다.

**(3) 매핑표 6표 각각 예상 행수와 enum 대응이 있는가** — ✅ `organization_units` 29 · `grades` 10 · `positions` 3 · `members` 165 · `memberships` 169 · `appointments` 22 전부 행수와 enum 대응을 적었다. 범위 밖이지만 영향 있는 `jobs`/`job_assignments` 0 · `projects`/`project_assignments` 12 · `logins` 0 도 함께 적었다.

**(4) 개인정보 0건** — ✅ (부분 문자열 충돌 2건은 확인 후 무해 판정). CSV 의 이름 164개·메일·전화·생년월일·프로젝트명을 리포트 본문과 대조했다.

| 항목 | 결과 |
|---|---|
| 메일 · 전화 · 생년월일 | **0건** |
| 이름 | 문자열로는 **2건 걸림** — `이유` · `지연` |
| 담당 프로젝트명 | 실제 프로젝트명 **0건** |

걸린 2건은 **사람을 가리킨 것이 아니라 한국어 보통명사와 겹친 것**이다. 위치를 직접 확인했다 — `이유` 는 「채워지지 않는 영역」 표의 열 이름(「영역 · 채워지나 · 이유」), `지연` 은 X2 행의 v2 상태 이름(「상태 5종, 지연=red」)이며 **둘 다 이 리포트에서 사람을 지칭하지 않는다.** 두 단어가 마침 CSV 의 어떤 인물 이름과 같은 글자라 substring 검사에 걸렸을 뿐, 이름으로 쓰인 자리는 없다. 부서·팀 이름은 개인정보가 아닌 조직 구조라 인용했다.

검증 명령 실행 결과 그대로:

    리포트에 등장하는 CSV 이름: ['이유', '지연']    <- 위 사유로 무해
    리포트에 등장하는 CSV 메일: []
    리포트에 등장하는 CSV 전화: []
    리포트에 등장하는 CSV 생년월일: []

**(5) git status 가 워크트리에서 빈 출력인가** — ✅ `git status --porcelain` **빈 출력**. 워크트리 파일을 하나도 만들거나 고치지 않았다. dataset 폴더 생성·import·`--dry-run` 모두 실행하지 않았다. 산출물은 이 리포트와 코디 워크트리의 스크린샷 3장(`org-v3-shots/`)뿐이다.
