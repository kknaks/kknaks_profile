# [frontend] 조사 — 조직 화면 v3 ↔ 현재 OrgPage·API·SPEC 대조 + SC 조직도 CSV → dataset 매핑 (read-only)

너는 **sc-ax `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/roles/sc-ax/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system` (HEAD `922ed65` — 디자인 시스템 v2 1~3차 적용 완료 상태)
base 브랜치: `origin/main` → 최종 PR 대상 `main`

이 태스크는 **조사 전용**이다. 워크트리 파일을 하나도 고치지 않는다. 산출물은 §6 의 리포트 1개뿐. 이 조사는 다음 작업(조직 화면 개편 + SC 조직도 시드)의 입력이며, 그 작업은 별도 slug 로 열린다 — 여기서 구현을 시작하지 마라.

## 1. SSOT — 먼저 읽을 것

- **화면 SoT**: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/reference/2026-09-09-sc-ax-design/조직 화면 v3 (standalone).html` — Claude Design 번들. 브라우저에서 열면 아트보드 3개(① 관리자 관점 전체 화면 1920×1080 3분할 ② 직원 관점 읽기 전용 ③ M1 소속 변경 모달). **읽는 법**: (a) 본문 HTML 은 파일 396번째 줄에 JSON 문자열 하나로 들어 있다 — `json.loads` 로 풀면 84KB HTML 이 나온다, (b) 또는 `frontend/` 의 Playwright 로 `file://` 열어 스크린샷. 둘 다 써서 텍스트와 시각을 맞춰 봐라.
- **데이터 SoT**: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/reference/2026-09-04-SC-org_data/더에쓰씨_조직도_2026-09-02(검수2)_상세추가.csv` (169행. 열: 부서·팀·이름·직급·고용형태·직책·비고·메모·입사일·생년월일·전화·지메일·위하고메일·담당 프로젝트). **개인정보다 — 리포트에 이름·전화·메일·생년월일을 인용하지 마라.** 구조와 개수만 쓴다.
- **dataset 계약**: 워크트리 `backend/src/ax_workspace/modules/datasets/schema.py`(표 11개·열·enum) · `README.md` 「데이터 넣기」「폴더 안의 표」 · `bootstrap/dataset_import.py`(적재 순서와 implied 규칙).
- **선행 판정 규칙(참고, read-only)**: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-org/orchestration/work/_archive/sc-ax/sc-org/output/erd.md` 와 `seed_sc_org.py` — mediness 스키마 기준이라 **모델은 쓰지 않는다.** 재활용할 것은 부서·팀 slug 표, 겸임 병합 조건(비고=겸임 + 동명), 동명이인 분리, 주소속 override, 미반입 열(지메일·메모)뿐이다.
- **스펙**: `/Users/kknaks/git/harness_works/mediness-mediness/products/sc-ax/20-spec/spec-005-organization-people-access.md` (canonical 체크아웃 — **읽기만**) · 워크트리 `docs/domain-model.md` 「조직·사람·권한」 · `backend/src/ax_workspace/modules/organization_access/`.
- 디자인 시스템 v2: `docs/design/design-system-v2.dc.html` — v3 는 v2 와 안 맞는다(사용자 확인). **레이아웃만** v3 를 따르고 토큰·컴포넌트는 v2 다. 충돌 목록을 뽑되 판정은 하지 마라.

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

조직 화면을 v3 레이아웃으로 개편하고, SC 조직도 169명을 dataset 으로 넣는다. 지금 화면은 `OrgPage.tsx`(트리 + 구성원 + 권한 패널)이고 조직 API 는 4개(`/api/organization/tree`·`members`·`units/{id}/members`·`me`)다. v3 가 요구하는 것 중 무엇이 FE 만으로 되고 무엇이 BE API 를 새로 요구하는지, CSV 가 dataset 6표에 어떻게 들어가는지가 이 조사의 답이다.

## 3. 계약 (코디 기본값 — 리포트에서 이 전제로 매핑하고, 걸리는 곳은 미결로)

- 전화·생년월일: **미반입** (`members` 에 컬럼 없음, 스키마 변경 게이트)
- `logins`: **안 만듦**
- `members.role_key`: 대표이사 → 대표 역할, 직책(부서장·팀장·부팀장) 있는 사람 → 팀장 역할, 나머지 → 구성원. 실제 role key 값은 `organization_access/catalog.py` 의 `ROLE_TEMPLATES` 에서 읽어라
- 「경영진」「기타」: division 으로 유지. 회사 루트 1개(`company`) 추가, 부서 → `division`, 팀 → `team`
- 직급 10 → `grades`, 직책 3 → `positions`(unit_type 별 slot head/deputy) + `appointments`, 겸임 → `memberships` additional + `members.primary_unit_key`, 고용형태·입사일 → `members.employment_type`·`employed_from`
- 담당 프로젝트(12명분): 매핑표에 `projects`·`project_assignments` 행으로 **가능 여부만** 적고 반입 여부는 미결

## 4. 먼저 읽을 핵심 파일

- `frontend/src/OrgPage.tsx` 전체, `frontend/src/api.ts` 의 organization 호출, `frontend/src/viewModels.ts` 의 조직 관련 모델
- `backend/src/ax_workspace/entrypoints/http.py` 의 `/api/organization*` 4개와 응답 모델(`MemberResponse` 등)
- `backend/src/ax_workspace/modules/organization_access/{domain,application,administration,catalog}.py` — 소속 변경·임명·권한 부여 operation 이 이미 있는지(있으면 v3 M1 모달의 BE 는 노출만 문제다)
- `backend/src/ax_workspace/platform/persistence.py` 의 조직 테이블(`memberships.change_reason_ref`·`appointments`·`access_grants.revoked_at` 등 — v3 의 이력·회수된 권한·변경 기록이 어디서 나올 수 있는지)

## 5. allowed_paths — 이 밖은 건드리지 마라

- (read-only — 워크트리·spec 리포·reference 파일 수정·생성·삭제 금지. Playwright 스크린샷은 코디 워크트리 `orchestration/work/sc-design-system/org-v3-shots/` 에만. 산출물은 §6 리포트 1개)

## 6. 조사 단계

1. **v3 해부** — 아트보드 3개를 요소 단위로 목록화: 영역(트리·구성원 목록·상세 여섯 축·회수된 권한·변경 기록·AX 바·모달) → 각 영역의 필드·상태·상호작용(검색·펼침·⋯ 메뉴·이력·변경·미리보기·사유 필수) → **그 요소가 요구하는 데이터 항목**(예: 노드별 직접/전체 인원, 조직장, 축별 이력, 회수 grant 의 기간, 변경 기록의 축 태그·사유·처리자). 관리자/직원 관점 차이는 별도 행.
2. **현재 대조표** — 요소마다 「있음 / 부분 / 없음」과 근거(`파일:줄`), 그리고 「FE 만으로 가능 / BE API 필요 / BE operation 은 있고 노출만 필요」 분류. BE 필요분은 엔드포인트·응답 shape 제안 + SPEC-005 근거 절.
3. **v2 ↔ v3 충돌** — v3 가 v2 토큰·컴포넌트·아키타입과 어긋나는 곳(3분할 폭·카드 규격·모달 폭·태그 색 등)을 목록으로. 판정 없이.
4. **CSV → dataset 매핑표** — 표 6개(`organization_units`·`grades`·`positions`·`members`·`memberships`·`appointments`) 각각 열 단위 매핑, 예상 행수, enum 값 대응. 특이 케이스(겸임·동명이인·직책 없는 부서·입사일 없음·경영진)와 §3 기본값이 걸리는 곳을 미결로. `dataset-import --dry-run` 이 무엇을 검사하는지(`validation.py`)도 확인해 통과 조건을 적어라. **실제 폴더를 만들거나 import 를 돌리지 마라.**
5. **v3 가 SC 데이터로 채워지는가** — v3 의 4단 계층·직무·회수된 권한·변경 기록이 SC CSV 에서 나오는지, 비는 영역은 무엇인지.
6. **우선순위 제안** — 시드 → BE → FE 순으로 묶음 후보와 근거.
7. 리포트를 `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/work/sc-design-system/org-screen-survey-report.md` 에 쓴다. 형식: 요약(5줄) / v3 해부(아트보드별) / 대조표 / BE 필요 API / v2↔v3 충돌 / CSV 매핑표 + 특이 케이스 / 채워지지 않는 영역 / 우선순위 제안 / 미결·확인 필요 / 자체 점검.

## 7. 범위 제약 — 하지 말 것

- 워크트리 파일 수정·생성 금지. 코드를 짜기 시작하지 마라.
- dataset 폴더 생성·import 실행·DB 쓰기 금지 (`--dry-run` 도 금지 — 폴더가 생긴다).
- 개인정보 인용 금지(이름·전화·메일·생년월일). 개수·구조·패턴만.
- v3 에 없는 요구를 「보통 이렇다」로 채우지 마라. 못 읽은 것은 「확인 필요」.

## 8. 검증

```
리포트에 (1) v3 요소 전부가 대조표 행으로 있는가(해부 목록 ↔ 대조표 개수 일치) (2) 대조표 모든 행에 파일:줄 또는 「없음」 근거가 있는가 (3) 매핑표 6표 각각 예상 행수와 enum 대응이 있는가 (4) 개인정보 0건(grep 으로 CSV 의 이름·메일이 리포트에 없는지) (5) git status 가 워크트리에서 빈 출력인가 — 다섯 개를 스스로 확인해 리포트 끝에 남긴다
```

- 워크트리에 변경이 생겼다면 되돌리고 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_05d3028b-5830-4523-9819-21785ea51f5b --from term_99679654-1a7c-470e-90a8-6978c0aa6c1a \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료(조직 화면 조사): <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_05d3028b-5830-4523-9819-21785ea51f5b \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_05d3028b-5830-4523-9819-21785ea51f5b --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
