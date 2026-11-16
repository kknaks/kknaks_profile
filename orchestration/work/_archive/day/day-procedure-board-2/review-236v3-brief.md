# [reviewer] 코드 리뷰 — CENTURION_DAY#236 v3

같은 규칙(`review-236-be-brief.md` — 읽기만 · 수정 · 커밋 · KOS · 공유 DB 금지 · pytest/ruff 는 돌려도 됨). 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2` — `git diff`(커밋 a1c90b9d 이후 미커밋 전부: F1 · F5 디자인 · F6 시드 생년월일 · v3 구현).

## SSOT
Delivery #236 v3(승인 · `gh issue view 236 --repo MediSolveAIDev/CENTURION_DAY`) · SPEC-002 개정 ⑮(bd029f3c) · 결정 `_RESUME.md` §2 11-10 · `e2e-feedback.md` F1 ~ F8 · 지시 `code-236v3-brief.md`(같은 폴더).

## 볼 것
1. Acceptance A1 ~ A4 · A7 ~ A13 이 스펙대로이고 테스트가 실제로 막나 — 특히 호출 중 줄 새 호출(앞 호출에서 빠짐 · 빈 호출 닫힘 · KOS 쓰기 순서) · [재호출] 처음 대상 · 창 없음 · 판 카드에 없음 · 사이드 경과 무관 · 카드 순서 저장(board_card_order — 동시성 · 병원 잠금 · 그날 경계 · 끌기와의 충돌) · 「⋯」 반영 중 막기 · version(Redis 값 · 단조 증가 · 재시작 · 여러 api 프로세스 · 신호 건너뛰기가 다른 화면 갱신을 놓치는 자리 없나 — 「조용히 통과하는 자리」 1순위)
2. 워커 미결 ③ 10초 tick 신호 본문 없음 처리 · ④ 순서 행을 읽을 때 저장(GET 이 DB 를 쓰는 것 — 부작용 · 동시 요청)
3. OOB 조각: 화면 상태(체크 · 접힘 · 탭 · 스크롤 · 검색) 지키기 · 판에서 빠지는 카드 삭제 · 권한
4. 시드 생년월일(F6) — 개인 값 출력 없음 · 가드 그대로
5. 화면 글자 새로 지은 것 0 · 손 CSS · 인라인 스크립트 0 · test.sh 679 passed 직접 1회

## 산출물
`/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/review-236v3-report.md` · FAIL / WARN / PASS · 파일:줄 + 근거. 완료 보고 두 명령(코디 핸들 `term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd`).
