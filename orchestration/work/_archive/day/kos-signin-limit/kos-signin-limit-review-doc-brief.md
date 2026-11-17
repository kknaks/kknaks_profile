
# [reviewer_doc] KOS 기기 제한 스펙(SPEC-001 ⑨ · SPEC-003 ⑱) 검수 (read-only)

너는 **day `reviewer_doc` 워커**다. 너는 앞 맥락이 없다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/kos-signin-limit-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

planner 는 끝났다. 파일을 고치지 마라 — 리포트 1개만.

## 1. SSOT — 먼저 읽을 것

- 결정 정본: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/kos-signin-limit-spec-brief.md` §1 결정 표 K-1 ~ K-6 · KOS 사실 · `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/_RESUME.md` §2.
- 리뷰 대상: `/Users/kknaks/orca/workspaces/mediness-mediness/kos-signin-limit-spec` 미커밋 diff(`products/day/` — spec-001 개정 ⑨ · spec-003 ⑱ · spec-000 · 20-spec · log).
- planner 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/spec-report.md` · Delivery `gh issue view 256 -R MediSolveAIDev/CENTURION_DAY`.
- 코드(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/kos-signin-limit`(dev `0c401726`) · 앞 조사 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/be-0-findings.md`.

기대는 개념: 해당 없음.

## 2. 배경

KOS 기기 5대 제한 처리 스펙. 다음은 코드(be · fe)다 — 이 스펙만 보고 짓는다.

## 3. 계약

해당 없음(검수).

## 4. 먼저 읽을 핵심 파일

위 §1.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정·생성 금지. 산출물은 브리프가 지정한 리뷰 리포트 파일 1개뿐)`

## 6. 검토 항목

1. K-1 ~ K-5 빠짐 · 넘침(화면 글자는 KOS 화면 문구만 — 「처음으로」 재사용(OQ-K10) 등 넘침 여부 판정).
2. 비밀번호 임시 보관(OQ-K3) — 기존 병원 고르기 pending 과 코드 사실 대조 · 비밀번호가 응답 · 화면 · URL · 로그 · DB 에 새는 자리가 없는지.
3. 시스템 계정 자동 해제(K-2 · OQ-K1 · K2) — api · worker 등 같은 환경 여러 프로세스가 서로의 토큰을 끊는 왕복 위험 · 사람 세션 보호 · 무한 재시도 없음.
4. 앱 영향(K-5) — 깔린 앱이 새 단계를 받으면 보이는 것(코드 사실 · 지금보다 나빠지는지) · 데모 넘김(OQ-K7).
5. 코드 착수를 막는 OQ 와 기본값이 지을 수 있을 만큼 닫혔나 · 코드 사실과 어긋남(파일:줄).
6. 문서에 비밀번호 · 이메일 · IP 없음 · `python3 scripts/lint-pipeline.py --strict` products/day ERROR 0.

## 7. 범위 제약 — 하지 말 것

- 파일 수정 금지(리포트 1개만) · 커밋 · Issue 수정 · 승인 금지.

## 8. 검증

```
SPEC·WORK 를 DEC·baseline 에 대조. lint-pipeline --strict 로 products/day/ ERROR 0. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
```

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/kos-signin-limit/review-doc-1-report.md`.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_94fbe396-828d-4fa4-8bd8-829294f10614 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_94fbe396-828d-4fa4-8bd8-829294f10614 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
