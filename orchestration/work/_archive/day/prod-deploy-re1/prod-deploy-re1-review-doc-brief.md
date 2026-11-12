
# [reviewer_doc] prod 첫 배포 스펙 개정 ④ · Delivery #243 문서 리뷰

너는 **day `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/prod-deploy-re1-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ 이 워크트리에는 planner 의 **미커밋 스펙 개정**이 있다 — 읽기만. 수정 · 커밋 · stash 금지.

## 1. SSOT — 먼저 읽을 것

- planner 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/delivery-report.md`
- 변경: `git -C /Users/kknaks/orca/workspaces/mediness-mediness/prod-deploy-re1-spec diff` — `products/day/20-spec/spec-000-data-model.md` · `40-architecture/deployment.md` · `log.md`
- Delivery Issue: `gh issue view 243 -R MediSolveAIDev/CENTURION_DAY`(본문 · 라벨 — 읽기만)
- 사실 대조용 코드(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1` — `deploy/config/prod.env`(미커밋 · 값 출력 금지) · `deploy/Dockerfile` · `scripts/deploy/day_vm.py` · `.github/workflows/*prod*` · `docs/development/deployment.md` · `backend/day/services/crm_connections.py` · `backend/day/public.py` · `backend/tests/deploy/test_chat_env_contract.py`

기대는 개념: 해당 없음.

## 2. 배경

DAY prod 첫 배포. 사용자 결정(2026-11-11): 운영 연결은 운영용 등록 진입점으로 `is_demo=false` · prod api 컨테이너 안에서 · 값은 레포 밖 · 브랜드 코드 `ceramique` · 실제 병원 1곳. planner 가 이것으로 SPEC-000 OQ-01-2 를 닫고 deployment.md 에 prod 첫 배포 절차를 적고 Delivery #243 을 발행했다(승인 전).

코디 실물 확인(근거로 써도 됨): 운영 KOS 내부 API 가 VM 나가는 IP 에서 **403 `IPBlocked`**(로그인 · open API 는 됨) — KOS IP 허용은 「필요 여부 미확인」이 아니라 **필요**하다. Key Vault prod 비밀 8개는 넣었고 배포 스크립트 `validate_secrets` 통과. GitHub `prod` Environment 는 레포 권한 부족으로 못 만듦(승인 규칙 없음).

## 3. 계약

해당 없음.

## 4. 먼저 읽을 핵심 파일

위 §1.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정·생성 금지. 산출물은 브리프가 지정한 리뷰 리포트 파일 1개뿐)`

## 6. 구현 단계

1. 스펙 개정이 사용자 결정과 같은가 — 결정에 없는 정책을 지어 넣었나 · 열린 것을 닫았나.
2. deployment.md 「prod 첫 배포 절차」 · env 표 · Key Vault 행이 레포 사실(워크플로 · 배포 스크립트 · Dockerfile · prod.env 칸 이름)과 맞나. 위 코디 실물(IPBlocked · Key Vault 8 · Environment 권한)과 어긋나는 문장.
3. Delivery #243: Target Delta 가 브리프 두 건 + 스펙 개정과 같은 범위인가 · Non-Goals · Acceptance 가 확인 가능한가 · risk L3 근거 · 열어 둔 질문 세 개(데모 연결 이름 겹침 · 모듈/env 이름 · KOS IP) 중 기본값으로 닫을 수 있는 것.
4. 공개 레포 아님(mediness 는 회사 레포)이지만 비밀값 · 계정 이메일 · 키가 문서 · Issue 에 없는지.

## 7. 범위 제약 — 하지 말 것

- 파일 수정 · 커밋 · Issue 댓글 · 라벨 변경 금지.
- prod.env · 비밀 값 출력 금지.

## 8. 검증

```
SPEC·WORK 를 DEC·baseline 에 대조. lint-pipeline --strict 로 products/day/ ERROR 0. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
```

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/review-doc-1-report.md` — 판정(PASS/WARN/FAIL) · 지적마다 파일:줄 + 근거 + 고칠 문장 제안.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_e62e850f-aae8-4092-a945-6f9406c2af07 --from term_483a198e-c87e-442c-be28-620ce9692a0f \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_e62e850f-aae8-4092-a945-6f9406c2af07 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_e62e850f-aae8-4092-a945-6f9406c2af07 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
