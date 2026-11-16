
# [reviewer_doc] SPEC-001 · WORK-001 문서 검수 — DEC-001 대조

너는 **interpret-pwa `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/roles/interpret-pwa/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

read-only. 이 워크트리는 코디네이터와 같이 쓴다 — 리포트 1개 말고는 아무것도 만들거나 고치지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` ← 기준(accepted, D-01~D-17)
- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/00-baseline/baseline-001-interpret-pwa.md` ← 사용자 원문 · 확인한 사실
- 검수 대상: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md`
- 작성 브리프(무엇을 요구했나): `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/interpret-pwa-poc-spec-brief.md` §6
- planner 리포트가 있으면: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/` 의 `*spec*report*.md`

## 2. 배경 / 무엇을 바꾸나

새 통역 PWA 의 계약(SPEC-001)과 구현 순서(WORK-001)를 backend · frontend 워커가 이대로 코드로 옮긴다.
워커가 추측으로 메워야 하는 빈칸이 남으면 코드가 갈린다 — 그걸 미리 잡는다.

## 3. 계약

해당 없음.

## 4. 먼저 읽을 핵심 파일

- 통역 원형(read-only, `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:<경로>`): `procedure/back/app/api/interpret.py` · `procedure/back/app/service/interpret/*.py` — SPEC 통역 WS 가 원형과 다른 자리에 이유가 있나 대조
- Soniox 공식 문서 `https://soniox.com/docs/llms.txt` — 언어 코드 · context · translation 필드가 문서와 맞나

## 5. allowed_paths — 이 밖은 건드리지 마라

- 리포트 1개만 생성: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/review-doc-report.md`

## 6. 구현 단계

1. reviewer `rules.md` 의 문서 검수 체크리스트를 전수로 돈다
2. 특히 본다: ① DEC D-01~D-17 이 SPEC 어딘가에 다 반영됐나(빠진 D 번호 = FAIL) ② SPEC 에 DEC 근거 없는 정책 ③ BE↔FE 계약(로그인 · 용어집 API · 통역 WS 메시지 · 오류 코드)이 양쪽이 같은 모양으로 읽히나 ④ env 이름 · 포트 · 경로가 한 벌로 일관되나 ⑤ 실물 확인 항목이 완료 조건으로 WORK 에 들어갔나 ⑥ 번체(D-17) · `yue` 처리가 닫혔거나 열린 것으로 명시됐나 ⑦ public 레포 — 키 · 비밀번호 · 실명 0(grep)
3. 리포트(판정 PASS/WARN/FAIL · 지적마다 파일:줄 + 근거 D-번호)

## 7. 범위 제약 — 하지 말 것

- 문서 수정 금지 · 취향 지적 금지 · 커밋 금지

## 8. 검증

```
SPEC·WORK 를 DEC 에 대조. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
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
  --to term_ce3ec37d-8f58-4bca-9420-d55b08c591e2 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ce3ec37d-8f58-4bca-9420-d55b08c591e2 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ce3ec37d-8f58-4bca-9420-d55b08c591e2 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
