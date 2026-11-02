
# [reviewer_code] 조직도(organization) 도메인 조사 — 문서·코드·테이블 구조 정리 (sc-ax 재사용성 판단 재료)

너는 **mediness `reviewer_code` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-org/orchestration/roles/mediness/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다 — **이번 작업은 read-only 조사라 PR 없음**)

이번 작업은 코드 리뷰가 아니라 **read-only 조사**다. diff 판정(PASS/FAIL)이 아니라 조사 리포트 1개가 산출물이다.
스펙 문서는 별도 워크트리를 read-only 로 읽는다: `/Users/kknaks/orca/workspaces/mediness-mediness/task-spec`
(다른 워커 없음 — 두 워크트리 모두 너 혼자 읽는다. 어느 쪽도 수정하지 마라.)

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/mediness-mediness/task-spec/products/mediness/20-spec/spec-002-rbac-org.md` ← 조직도 도메인 계약의 SoT
- `/Users/kknaks/orca/workspaces/mediness-mediness/task-spec/products/mediness/30-work/work-055-rbac-org.md`
- 같은 트리에서 조직도(organization·org chart·부서·직급) 관련 spec/work/html 을 grep 으로 더 찾아 보완해라 — 위 두 개가 전부라고 가정하지 마라

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

sc-ax 프로젝트(같은 회사, 별도 제품)에 **조직도 데이터를 넣어야 한다.** mediness 에는 이미
organization 도메인(조직도·부서·직급·멤버)이 문서와 코드로 존재한다. 코디네이터와 사용자는
**mediness 의 테이블 구조와 코드를 sc-ax 에 그대로 재사용할 수 있는지** 판단하려고 한다.

이번 조사는 그 판단 재료를 만드는 것이다: mediness 조직도가 문서에서 어떻게 정의되고,
코드에서 어떤 테이블·표면으로 구현돼 있으며, 다른 도메인과 얼마나 얽혀 있는지를 리포트 1개로 정리한다.
**아무것도 바꾸지 않는다** — 두 워크트리 모두 read-only.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음 — 단독 조사.

## 4. 먼저 읽을 핵심 파일

앱 워크트리 (`/Users/kknaks/orca/workspaces/mediness-app/task`):

- `back/app/models/organization.py` — 조직도 모델의 원장
- `back/alembic/versions/0059_organization_tenant_access.py` · `0061_organization_directory_foundation.py` · `0064_organization_position_role.py` · `0065_organization_job_function.py` · `0096_organization_member_lifecycle.py` — 테이블 구조의 변천. 이 밖에도 organization 관련 마이그레이션을 grep 으로 전수 확인해라 (0058 테넌트 시드 SQL 포함)
- `back/app/routers/organization_directory.py` · `back/app/routers/admin_organization.py` — API 표면
- `back/app/services/organization_directory.py` (+ `organization_directory_provider.py` · `organization_membership_scheduler.py` · `legacy_organization_directory_*.py`) — 도메인 로직과 legacy 브리지
- `back/app/repositories/organization_access_repo.py` · `back/app/schemas/organization_directory.py`
- `back/app/seeds/` 에서 조직 시드 (`seed_medi_users` 등)

스펙 워크트리 — §1 목록.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 두 워크트리 모두 리포 파일 수정·생성 금지. 산출물은 아래 리포트 파일 1개뿐)`
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-org/orchestration/work/sc-org/org-chart-survey-report.md`

## 6. 구현 단계

1. **문서 조사** — 스펙 워크트리에서 조직도 관련 spec·work·html 을 전수하고, 조직도 도메인의
   의도(무엇을 표현하나: 부서 트리·직급·역할·멤버 lifecycle 등)와 정책을 요약한다.
2. **테이블 구조** — 모델·마이그레이션에서 조직도 관련 **테이블 전수**: 테이블별 컬럼·타입·PK/FK·
   unique/index·enum 값·soft delete 여부를 표로 정리한다. 마이그레이션 이력에서 왜 그렇게
   바뀌었는지 한 줄씩. (DDL 전문 복사가 아니라 구조 요약 — 단, 컬럼은 누락 없이)
3. **코드 표면** — 라우터(엔드포인트 목록·요청/응답 shape 요약)·서비스·레포·스키마·시드가
   각각 무엇을 하는지, 파일 단위로 지도화한다.
4. **결합도** — 조직도 도메인이 무엇에 의존하나: tenant/user/RBAC/department_space 등 다른
   테이블·도메인과의 FK·import 관계. **떼어갈 때 같이 딸려오는 것**을 명시한다.
5. **재사용성 판단 재료** — ① 그대로 쓸 수 있는 단위(테이블·코드) ② 고쳐야 쓸 수 있는 지점과 이유
   ③ sc-ax 쪽 요구를 알아야 판단되는 미결 질문. **설계 제안은 하지 않는다** — 판단은 사용자 몫.
6. 위 1~5 를 리포트 1개로 작성한다. 모든 주장에 `파일:줄` 근거, 사실과 추측을 구분 표기.

## 7. 범위 제약 — 하지 말 것

- 두 워크트리의 파일 수정·생성·삭제 금지. 커밋·push 금지. 산출물은 리포트 1개뿐.
- 조직도와 무관한 도메인으로 조사를 넓히지 마라 (의존 관계로 닿는 지점까지만).
- sc-ax 를 위한 설계·마이그레이션 계획을 쓰지 마라 — 현황과 판단 재료까지가 범위다.
- 테스트 실행 금지. DB 접속 금지 — 코드와 마이그레이션 파일로만 판단한다.
- 리포트에 직원 실명 등 개인 식별 정보를 인용하지 마라 — 구조와 코드만.

## 8. 검증

```
리포트 self-check: (a) 조직도 관련 테이블 전수 — back/alembic/versions/ 를 organization 으로 grep 한 결과와 §2 표의 테이블 목록이 대조되는가 (b) 모든 주장에 파일:줄 근거가 있는가 (c) 사실/추측이 구분돼 있는가. 하나라도 아니면 보완 후 보고한다.
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_4d21fab2-947e-495f-9df5-0418f447a15b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_code 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_4d21fab2-947e-495f-9df5-0418f447a15b \
  --text "[worker_done] reviewer_code 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_4d21fab2-947e-495f-9df5-0418f447a15b --text "[질문] reviewer_code: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
