
# [docs] 소수정 — DEC-002 에 신설 개념 `pii-masking` 연결

너는 **ontology-demo `docs` 워커**다. 직전 태스크들과 같은 워크트리, 같은 규칙.

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/docs-baseline`

## 배경

네가 보고한 「개념 필요 ② PII 마스킹」을 코디네이터가 처리했다 — `para/areas/concept/db/pii-masking.md`
신설(출처: 기록 03 글로서리, 커밋 43dd669, origin/ontology-demo 에 푸시됨). `git fetch origin` 후
`git merge origin/ontology-demo` 없이도 파일 확인은 코디 워크트리 절대경로로 가능:
`/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/para/areas/concept/db/pii-masking.md` (read-only)

프론트 개념(①)은 출처 노트 부재로 규약상 생성 불가 판정 — DEC-004 는 `up:[]` + 사유 유지. 손대지 마라.

## 할 일 (이것만)

1. `para/projects/summer-star/ontology-demo/10-decision/decision-002-pii-masking-boundary.md`:
   - frontmatter `up:` 에 `pii-masking` 추가 (기존 `medallion-architecture` 유지)
   - 본문 「근거 개념」 절에 `[[pii-masking]]` 한 줄 추가 — 이 결정이 그 개념의 무엇을 딛는지
     한 줄로 (원값 보존 + 표면 마스킹 분리, 가리는 지점 단일화)
   - `updated_at` 은 2026-09-02 그대로
2. `log.md` 에 엔트리 1줄 (decision-update).

## 하지 말 것

- 다른 파일 수정 금지. `para/areas/` 수정 금지. 커밋·push 금지.

## 완료 보고 — 직전 태스크와 동일한 2채널 (preamble 의 taskId·dispatchId·코디handle 사용)

```bash
orca orchestration send --to term_45e793be-0adb-44c7-9d9a-eb35c4f48320 --from <네 워커handle> \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "docs 완료: DEC-002 up 연결" --body "변경 파일 / 요약"
orca terminal send --terminal term_45e793be-0adb-44c7-9d9a-eb35c4f48320 \
  --text "[worker_done] docs 완료 — DEC-002 up: pii-masking 연결. 상세는 인박스." --enter
```
