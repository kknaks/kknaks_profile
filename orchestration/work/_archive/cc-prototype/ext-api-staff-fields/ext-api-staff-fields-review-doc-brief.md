
# [reviewer_doc] SPEC-008 0.4.7 · WORK-015 문서 검수 — ext 직원 목록 세 칸

너는 **cc-prototype `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-3/orchestration/roles/cc-prototype/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-3`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

너는 앞 판 맥락이 없다 — 아래 파일만 믿어라. 같은 워크트리에 다른 워커 없음. **read-only** — 리포트 파일 1개만 만든다.

## 1. SSOT — 먼저 읽을 것

- `para/projects/summer-star/cc-prototype/10-decision/decision-012-ext-api-charty1.md` — **D-48**(이번 결정) · D-15 고침 줄 · D-21 · D-29
- `para/projects/summer-star/cc-prototype/20-spec/spec-008-product-ext-api.md` — 0.4.7. 이번 diff 는 `git diff -- para/projects/summer-star/cc-prototype/20-spec/` 로 본다
- `para/projects/summer-star/cc-prototype/30-work/work-015-ext-api-staff-fields.md` — 새 WORK
- 코드(read-only, 현재 배포본 main `969f44f`): `/Users/kknaks/orca/workspaces/cc-prototype/ext-api-staff-fields/procedure/back/app/{schemas/ext.py,service/ext.py,api/ext.py}` · `tests/test_ext_clinic.py`
- 개념: 해당 없음

## 2. 배경

ext 직원 목록 `GET /api/ext/clinics/{clinicId}/staff` 에 `email` · `realName` · `kosAccountId` 를 더한다(D-48 · 필드 추가만). planner 가 SPEC 0.4.7 · WORK-015 를 썼다. planner 가 남긴 주의: kosAccountId 꼴(uuid) 미기재 · 원소 `id` 없으면 지금도 502 · 기존 T67 의 「새지 않음」 단언을 BE1 이 뒤집어야 함 · 부록 B Q2 는 기록이라 두고 §6.1 예외 줄 추가.

## 3. 볼 것

1. SPEC 0.4.7 이 D-48 을 빠짐없이 · 넘치지 않게 옮겼나(필드 셋 · 타입 · null 규칙 · 기존 칸 · 행 고르기 · KOS 호출 수 무변경 · 사본에 이메일 저장 안 함 · 응답 밖에 안 남김)
2. 이번 변경과 **어긋나는 남은 줄** — SPEC 전체에서 「이메일 · 실명 · KOS id 를 내지 않는다」 류 문장이 직원 목록에 대해 남아 있지 않은지 grep 전수(§0 · §1 · §6.1 · §6.17 · §7 · §8 · §9 · 부록). 다른 경로(lookup 등)에 대한 같은 규칙은 그대로가 맞다
3. T67 이 새 계약을 고정하나(키 집합 · null · `kosAccountId` = 내부 `id`) · 시험 데이터가 지어낸 값인가
4. WORK-015 WP 가 SPEC 절을 가리키고, 검증 명령 · 완료 기준이 실행 가능한가. BE1 이 고칠 파일 목록이 코드 실물과 맞나(`grep -rn "내지 않는다\|realName\|email" procedure/back/app/api/ext.py procedure/back/app/schemas/ext.py procedure/back/app/service/ext.py procedure/back/tests/test_ext_clinic.py` 로 전수)
5. public — 바뀐 줄에 실명 · 이메일 · KOS id 실값 0

## 4. 산출물

- 리포트 1개: `orchestration/work/ext-api-staff-fields/review-doc-r1.md` — 판정(PASS · WARN · FAIL) · 각 지적에 파일:줄 + 근거(D-번호 · SPEC 절) · 고칠 방향 한 줄
- 다른 파일은 고치지 않는다

## 5. allowed_paths

- (read-only — 위 리포트 파일 1개만 생성)

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_94d17da5-ee50-4f74-ade5-221f35a1ea02 --from term_e070a23e-f818-4e25-aef9-6879c05d58cb \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_94d17da5-ee50-4f74-ade5-221f35a1ea02 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_94d17da5-ee50-4f74-ade5-221f35a1ea02 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
