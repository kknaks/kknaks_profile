# [reviewer] 코드 리뷰 — CENTURION_DAY#236 backend 단계

너는 day **reviewer** 워커다. 역할 문서 먼저: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/reviewer/role.md`(+ 같은 폴더) · 레포 `AGENTS.md`. **읽기만** — 레포 파일 수정 · 커밋 금지 · KOS 호출 · 공유 DB 금지. pytest · ruff 는 돌려도 된다(로컬 compose postgres · redis 떠 있음 · `DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env scripts/test.sh -q`).

워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2` — `git diff`(미커밋 15파일 · 브랜치 기존 커밋 96fff917 이후). 템플릿 · 화면 라우터 · static · styles 는 아직 안 바뀜(frontend 몫 — 이번 대상 아님).

## SSOT
- Delivery #236 v2(승인됨): `gh issue view 236 --repo MediSolveAIDev/CENTURION_DAY`
- 스펙: `/Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec/products/day/20-spec/spec-002-procedure-board.md` 개정 ⑬ · ⑭
- 결정 정본: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/_RESUME.md` §2
- 워커 보고: 같은 폴더 `be-236-brief.md` 지시 · 보고 요약 = phase 1~3 · test.sh 612 passed · web 템플릿 테스트 25개 실패(frontend 몫)

## 볼 것
1. Acceptance A1~A9 백엔드분이 스펙대로인가(테스트가 실제로 막나) — 체크 가능 · 고객 검색(시술 완료 탭만 · 이름/원장/관리실) · 확인 필요 5상황(since · 풀리는 때 · 정렬 · 기준 분 env) · 마취 회차 · 귀가 대기 마취 닫기 · 원장 바꾸기(KOS change-tasks-doctors 1명 덮어쓰기 · 새 원장 표시 · 수락 뒤 미시작 다시 셈 · event_log) · 동시 수락(advisory lock)
2. 워커가 밝힌 미결 ① 원장 바꾸기가 DoctorCallAccept.doctor_staff_id 를 새 원장으로 고침(이전 원장은 event_log 에만) — 스펙 규칙 9 · 27 과 맞나 ② event_log 조회 성능 ③ ④ ⑤
3. outbox: 원장 바꾸기 op · 앞 수락 op 재전송 여부(touched 칸 묶음) · 중복 쓰기 · 순서
4. 조용히 통과하는 자리 · 화면 · API 계약 변경 중 스펙에 없는 것 · 지어낸 문구
5. web 템플릿 테스트 25개 실패가 정말 템플릿 몫뿐인가(백엔드 회귀 아님)

## 산출물
`/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/review-236-be-report.md` · FAIL / WARN / PASS · 지적마다 파일:줄 + 근거.

## 완료 보고 (두 명령 모두)
```bash
orca orchestration send --to term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "reviewer 완료: <판정>" --body "<요약>"
orca terminal send --terminal term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd --text "[worker_done] reviewer 완료 — <한 줄>. 상세는 인박스." --enter
```
핸들은 dispatch preamble 값이 맞다.
