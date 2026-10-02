# [frontend] WORK-008 Phase 5 FE — AX 답변의 project 참조 열기

너는 **strong-hajin `frontend` 워커**다. 같은 워크트리(HEAD `94cacfd`)·같은 규칙. `frontend/` 만(backend 는 Phase 5 미커밋 변경이 있다 — 건드리지 마라). 코디 핸들 `term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44`.

## 배경
Phase 5 BE 가 AX 답변 참조에 `project` 종류를 더했다(`answer_documents.py` ResourceRef, 참조 문법 `project:<project_id>`). 그런데 FE 는 `lib/viewModels.ts:987` `AnswerResource.resource_type` 에 `"project"` 가 없고 `App.tsx:678-715` `onOpenResource` 에 project 분기가 없다 → 프로젝트 참조가 와도 **열리지 않는다**.

## 할 일
- `resource_type` 에 `"project"` 추가, 답변 안 참조 칩/링크가 project 를 다른 종류와 같은 모양으로 그리게
- 누르면 **프로젝트 화면으로 가서 그 프로젝트를 연다**(이미 있는 「보던 프로젝트」·focus 경로 재사용). 읽을 수 없으면 기존 「열 수 없음」 처리와 같게
- 참조 종류를 다루는 곳을 **전부** grep 으로 세어(빠진 switch·라벨·아이콘) 보고
- 테스트: project 참조 렌더 · 클릭 → 프로젝트 화면·그 프로젝트

검증: 직렬 vitest(바뀐 파일 + 전체 1회) · `npx tsc --noEmit` · `make frontend-build`. 커밋·서버·브라우저 금지.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send --to term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --from <네 워커handle> --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: WORK-008 Phase 5 project 참조" --body "변경 파일:줄 / 참조 종류 전수 / 테스트·tsc·build"
orca terminal send --terminal term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --text "[worker_done] frontend 완료 — Phase 5 project 참조. 상세는 인박스." --enter
```
