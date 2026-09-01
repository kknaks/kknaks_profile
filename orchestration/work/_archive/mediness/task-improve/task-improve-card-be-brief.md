
# [backend] 승인 카드 본문 확장 — WBS 등록 카드에 배경·목표·기한·체크리스트·요청자

너는 **mediness `backend` 워커**다. 사용자 실기동 반려 — WBS 업무 등록 승인 카드가 4칸(버전·PHASE·업무·담당자)뿐이다. 확정 와이어프레임대로 본문을 채운다.
역할: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/backend/role.md`
워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-improve` (**front/ 금지 — FE 병렬**)

## 확정 계약 (사용자 와이어프레임 — _RESUME.md §2 «승인 카드 공용 본문»)

태스크를 만드는 승인 카드는 전부: 버전/PHASE/담당자/**기한**/**요청자** + **배경** + **목표** + **체크리스트** + 요약문. 못 채운 자리는 «미기재»(빈 값 명시) — 조용한 생략 금지. 승인 시 본문이 실제 태스크로 착지(tasks.background/goal — WP-130 컬럼·task_check_items·due).

## 해야 할 일

1. **MCP `wbs_task_create`(`mcp/app/tools/wbs_task_create.py` + server.py 등록)**: optional 인자 `background`·`goal`·`checklist: list[str]`·`due` 추가. 툴 설명에 «대화 문맥에서 채워라 — 비우면 카드에 미기재로 뜬다» 명시(에이전트가 채우게 유도). `wbs_task_update` 도 동형이면 함께
2. **wbs_task 워크플로**(`back/app/services/action_runtime/workflow/wbs_task/`): 접수 payload 에 4축 보존 → review_surface 에 배경/목표/체크리스트/기한/요청자 실어 카드가 렌더할 수 있게(기존 facts/primary_fields 골격 위에 additive — 다른 카드 타입 응답 불변)
3. **승인 실행 seam**: 승인 시 생성되는 태스크에 background/goal(컬럼)·checklist(task_check_items)·due 착지 — WP-130 이 만든 canonical seam 재사용, 새 원장 금지
4. **task.draft 카드 확인**: SPEC-155 계약상 이미 배경·목표·체크리스트를 실어야 함 — review_surface 에 실제로 실리는지 확인, 빠졌으면 같은 방식으로
5. 테스트: 카드 review_surface 본문 4축·승인 착지·미기재(빈 값) 각 1건 이상

**하지 말 것**: migration 금지(컬럼 다 있음)·기존 카드 타입 응답 파괴 금지·전체 스위트 금지(영향 파일만 1회).

## 완료 보고 — 문구 변경 금지
> ⚠ preamble 핸들 우선. 커밋·push 금지.
```bash
orca orchestration send --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "backend 카드 본문 완료: <한 줄>" --body "변경/테스트 수치"
orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --text "[worker_done] backend(카드 본문) — <한 줄>. 상세는 인박스." --enter
```
