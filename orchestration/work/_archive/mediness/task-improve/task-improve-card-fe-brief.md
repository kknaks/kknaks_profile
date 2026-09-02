
# [frontend] 승인 카드 본문 렌더 — 배경·목표·체크리스트·기한·요청자·미기재

너는 **mediness `frontend` 워커**다. 사용자 확정 와이어프레임대로 승인 카드 본문을 렌더한다.
역할: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/frontend/role.md`
워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-improve` (**back/·mcp/ 금지 — BE 병렬**)

## 확정 와이어프레임 (_RESUME.md §2 «승인 카드 공용 본문»)

```
[승인 대기] WBS 업무 등록 확인  <제목>
버전 | 상위 PHASE | 담당자 | 기한
업무 | 요청자
── 배경 (없으면 «미기재») ── 목표 (불릿) ── 체크리스트 (☐ 항목·n항목) ── 첨부(있으면)
── 요약문 ── [승인][거절]
```

## 해야 할 일

1. `front/components/landing-chat/ApprovalCard.tsx`(+ 카드 facts 조각): review_surface 가 싣는 `background`·`goal`·`checklist`·`due`·`requester` 를 위 순서로 렌더. **없는 축은 배경·목표만 «미기재» 로 명시**(체크리스트·첨부는 있을 때만). goal 은 개행→불릿(상세와 같은 규칙 재사용)
2. BE 가 병렬로 필드를 싣는 중 — **fail-closed**: 필드 없으면 현행 렌더 그대로(회귀 0). shape 는 BE 완료 보고 후 코디가 정합 확인
3. 채팅 본문 카드(TaskDraftBody)와 겹치는 조각은 재사용 — 두 벌 금지
4. 검증: tsc·만진 파일 prettier·카드 렌더 회귀 테스트(본문 4축·미기재·필드 부재 fail-closed)

## 완료 보고 — 문구 변경 금지
> ⚠ preamble 핸들 우선. 커밋·push 금지.
```bash
orca orchestration send --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> --subject "frontend 카드 본문 완료: <한 줄>" --body "변경/검증 수치"
orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --text "[worker_done] frontend(카드 본문) — <한 줄>. 상세는 인박스." --enter
```
