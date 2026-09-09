# [backend] 조직 화면 읽기 API — 구성원 6축 통합 조회 · 축별 이력 · 변경 기록 · 회수된 권한 · 계정 유무

너는 **sc-ax `backend` 워커**다(같은 세션). 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system` (HEAD `010a594`). frontend 워커가 같은 워크트리를 쓰지만 지금 idle. `frontend/`·`.design-sync/` 불변.

## 1. SSOT — 먼저 읽을 것
- 화면 요구: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/reference/2026-09-09-sc-ax-design/org-chart-template/HANDOFF.md` §State Management 「데이터」 항목과 §Screens ③ 6축 상세·하단 변경 기록.
- 조사 리포트 §「BE 가 새로 필요한 것」 BE-1·2·6·7: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/work/sc-design-system/org-screen-survey-report.md`
- 스펙: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/work/sc-design-system/ref-spec-main/spec-005-organization-people-access.md` §2(축마다 기간 보존 · 응답 필드는 Principal 권한에 맞게 제한) · `organization-access.md`
- 코드: `modules/organization_access/{application,administration,domain}.py` · `platform/organization_access.py`(`profile_for` 가 `revoked_at IS NULL` 로 거름 — 회수분이 응답에 없는 원인) · `platform/persistence.py`(memberships·appointments·grade_assignments·job_assignments·access_grants 의 valid_from/until·change_reason_ref·revoked_at · `ActivityEventRecord`) · `entrypoints/http.py` 의 `/api/organization*`·`/api/access*`
- 프론트 1단계가 소비하는 자리: `frontend/src/org/MemberAxesPanel.tsx`(읽기만 — 어떤 필드를 기다리는지)

## 2. 배경
조직 화면 1단계는 기존 API 4개로 현재값만 그렸다. 「이력」 버튼 비활성, 변경 기록 빈 상태, 회수된 권한 생략, 계정 유무 배지 생략 — 전부 읽기 API 가 없어서다. 이 태스크는 **읽기만** 연다. 소속·직책 변경 command 는 다음 태스크.

## 3. 계약 (코디 결정 2026-09-08)
- **BE-1 `GET /api/organization/members/{id}`** — 6축 통합: `member_id, display_name, employment_state, employment_type, has_account(bool), phone, birth_date, hierarchy_path[{unit_id,name,unit_type}], memberships[{unit_id,unit_name,kind,valid_from,valid_until}], appointments[{unit_id,unit_name,position,role_id,kind,valid_from,valid_until}], grade{id,name}, jobs[{id,name,kind}], grants[], revoked_grants[{role_id,role_label,scope_kind,scope_ref,scope_name,valid_from,revoked_at}]`.
  - 가시성: 기본 필드(계층·소속·직책·직급·직무·재직·계정 유무)는 **로그인한 누구나**(명부와 같은 기준). `phone`·`birth_date`·`grants`·`revoked_grants` 는 **본인 또는 그 구성원의 소속 unit 에 `organization.manage` 를 가진 Principal** 에게만 값, 아니면 `null`/빈 배열 — 기존 `_require_authority_over_member` 규칙 재사용, 예외를 던지지 말고 필드를 비운다.
- **BE-2 `GET /api/organization/members/{id}/history?axis=membership|appointment|grade|job|grant`** — 축별 기간 행 `[{value, unit_name?, valid_from, valid_until, reason(change_reason_ref 해석 또는 원문), actor?}]` 최신순. 가시성은 BE-1 의 민감 필드와 같음(본인 또는 관리 권한). 권한 없으면 403.
- **BE-6 `GET /api/organization/activity?unit_id=&limit=50&cursor=`** — 변경 기록: `ActivityEventRecord` 중 조직 축 사건(target_type 이 member/membership/appointment/grant 계열)을 `[{occurred_at, axis: '조직'|'소속'|'직책'|'권한', summary, reason, actor_id, actor_name, target_id}]` 로. `unit_id` 가 있으면 그 unit 이하 구성원 대상만. 가시성: 해당 unit(없으면 루트)에 `organization.manage` — 없으면 403. **event_kind → axis 매핑표를 코드 상수로 두고 보고에 붙인다.** 매핑 안 되는 kind 는 제외하고 개수 보고.
- **BE-7** 기존 `MemberResponse`(명부)에 `has_account` 추가. 사번은 여전히 `id`.
- 계층 규칙: entrypoint 는 application 만 부르고, SQL 은 repository(`platform/organization_access.py`)에. 도메인 예외 → HTTP 매핑은 http.py 기존 패턴. 새 테이블·스키마 변경 없음.
- 응답 스키마는 `docs/domain-model.md` 「조직·사람·권한」 Projection 줄에 한 줄씩 추가.

## 4. 핵심 파일
- `entrypoints/http.py:838-910` · `modules/organization_access/administration.py`(`member_access`, `_require_authority_over_member`) · `platform/organization_access.py`(`profile_for`, `member_units`) · `platform/persistence.py` 조직·ActivityEvent 모델 · `tests/contract/test_access_roles.py`·`test_organization_ledger.py`(픽스처·권한별 응답 패턴)

## 5. allowed_paths
- `backend/src/ax_workspace/{entrypoints/http.py, modules/organization_access/*, platform/organization_access.py}` · `backend/tests/contract/` · `docs/domain-model.md`
- **금지**: `platform/persistence.py` 스키마 변경 · `frontend/` · `Makefile` · 커밋·push · 실데이터(이름·메일·전화) 픽스처

## 6. 단계 / 8. 검증
1. 계약 테스트 RED: (a) BE-1 본인/관리자/타인 세 Principal 의 필드 가시성 (b) BE-2 축별 이력 + 403 (c) BE-6 관리자 200·직원 403 + axis 매핑 (d) 명부 `has_account`. 2. repository → application → entrypoint 순 구현. 3. `uv run pytest -q <만진 테스트> tests/architecture -m 'not integration'`. 4. 로컬 DB 실측(개인정보 미인용): 대표 1001 로 `members/1004`(G일본 팀장) 200 + grants 채워짐 · 팀원 1107 로 같은 요청 200 + grants 빈 배열 · `members/1004/history?axis=membership` · `activity` 관리자 200/직원 403 — 상태코드·개수 표. 5. `git status` 에 네 변경 = allowed 파일만. 검증 1회.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_4fcd67c5-63d2-409e-ae57-ef22b8fa5fb1 --from term_9ad0847d-9bbf-4d91-aeac-1ba4b4122d36 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_4fcd67c5-63d2-409e-ae57-ef22b8fa5fb1 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_4fcd67c5-63d2-409e-ae57-ef22b8fa5fb1 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
