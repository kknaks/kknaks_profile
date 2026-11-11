# [backend + frontend] CENTURION_DAY#236 v3 구현 — 로컬 확인 결정 반영

너는 이 작업의 day 워커다(앞서 #236 backend · frontend · 디자인 F1/F5 · 시드 생년월일을 한 세션). 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/backend/role.md` · `.../frontend/role.md` · 레포 `AGENTS.md`. 이번엔 backend 와 frontend 둘 다 네 몫이다(순서대로).

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2` — 커밋 a1c90b9d 위 + **미커밋 변경(F1 확인 창 · F5 원장 이름 · F6 시드 생년월일)이 있다 — 지우지 말고 그 위에서**.

## SSOT
- **Delivery #236 v3**(사용자 승인 2026-11-10): `gh issue view 236 --repo MediSolveAIDev/CENTURION_DAY` — Target Delta ① ~ ⑲ · Acceptance(A1 ~ A4 · A7 · A9 갱신 · A11 · A12 · A13 새) · Execution phase. **여기 없는 건 발명하지 마라.**
- 스펙: `/Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec/products/day/20-spec/spec-002-procedure-board.md` 개정 ⑮(커밋 bd029f3c) — U-2 · U-3 · U-5 · U-10 · 실시간 갱신(version) · 스냅샷 · 매트릭스 · 규칙 5 · 6 · 13 · 16 · 18 · 22
- 결정 · 피드백: 같은 폴더 `_RESUME.md` §2(11-10 행) · `e2e-feedback.md`(F2 · F3 · F4 · F7 · F8)

## 이번에 바꿀 것(v3 에서 바뀐 것 · 새 것)
1. 체크박스 = 준비중 · 호출 중(수락 전) · 호출 줄 체크해 [의사 호출] = 새 호출(그 줄은 앞 호출에서 빠짐 · 빈 호출 닫힘 · 사슬 아님) — KOS 쓰기는 스펙 KOS 쓰기 표대로
2. [재호출] = 처음 대상 그대로 · 창 없음 · 호출 통째 · **판 카드에서 뺌** · 사이드(인박스) 카드 어디서나 · 경과 상관없이 수락 전이면 · 글자 검정 · API 에서 target 뺌 · calls[].canRecall
3. 카드 순서(F2) = 판에 처음 오른 순으로 자리 저장 · 자동으로 안 바뀜 · 같이 오르면 입실 순 · 입실 빈 카드도 고정 · 사람이 끌면 그 순서 — 지금 `board_rules.py` card_created_at 의 `now` 대체 등
4. 「⋯」(F7) = 진행 중 줄에 [종료]와 같이 바로 · KOS 반영 중이면 메뉴는 보이되 누를 때 막음(스펙 문구 · 거절 코드 — 없으면 OQ-36 대로 · 지어내지 마라)
5. 갱신 범위(F8) = 동작 응답은 **누른 카드 조각 + OOB(인박스 칸 · 호출 탭 · 탭 숫자 · 원장 상태)** · version · board 신호는 version 만 · 화면은 가진 version 이하 신호 건너뜀 — 판 전체 두 번 그리기 없앰. 다른 화면 범위는 OQ-37 기본값(스펙대로)
6. 원장 변경 글자 · 토스트 · 검색 칸 글자 · 확인 창 · 원장 이름 호버 — 이미 반영된 것 확인만(F1 · F5)

## 하지 말 것
화면 문구 지어내기 · Non-Goals · 손 CSS · 인라인 스크립트 · 커밋 · push · PR · 사용자 포트/프로세스(로컬 day-local api/worker 다시 띄우기는 코디가 한다) · 공유 DB · KOS 호출.

## 검증
phase 마다 관련 테스트 · 끝에 `DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env scripts/test.sh -q` 1회 · ruff check · format · build-css · 손 CSS · 인라인 스크립트 grep 0. Acceptance 별 판정(테스트 이름).

## 완료 보고
`orca orchestration send --to term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "#236 v3 완료: <한 줄>" --body "<변경 파일 · 항목별 · Acceptance · 테스트 수 · 미결>"` + `orca terminal send --terminal term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd --text "[worker_done] #236 v3 완료 — <한 줄>" --enter`. 막히면 `[질문] …` 을 같은 터미널에 send.
