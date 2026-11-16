# [reviewer_doc] 리뷰 — SPEC-002 개정 ⑮ (로컬 확인 결정 반영)

같은 규칙(`review-doc-fix2-brief.md` — 읽기만 · 수정 · 커밋 · KOS 금지 · 산출물 리포트 1개). 대상: `git -C /Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec diff`(커밋 e421b77b 이후 · spec-002 · log.md). 지시: 같은 폴더 `planner-spec-fix3-brief.md`(+ 추가 지시 F7 · F8).

정본 = `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/_RESUME.md` §2 **2026-11-10 행 전부** + 같은 폴더 `e2e-feedback.md` F1 ~ F8 「결정」 칸.

## 볼 것
1. 호출 · 재호출 로직: 체크박스 준비중 · 호출 중 / 호출 중 줄 체크 = 수락 전 원장 바꾸기(그 줄은 앞 호출에서 빠짐) / [재호출] = 처음 대상 그대로 · 창 없음 · 호출 통째 / 판 카드 [재호출] 없음 · 사이드는 경과 상관없이 수락 전이면 어디서나 / 수락 뒤 = 「원장 변경」 — 앞 판(⑬ · ⑭)의 반대 문장이 **하나도** 안 남았나(grep 전수)
2. 카드 순서: 입실 순 처음 자리 저장 · 자동으로 안 바뀜 · 그 뒤 사람 — 입실 빈 카드 처리(OQ-35)가 근거 있나 · 지어낸 것 아닌가
3. F7 「⋯」 [종료]와 같이 바로 · 반영 중이면 누를 때 막음 / F8 누른 카드만 바뀜(SSE 절) — 결정과 맞나 · 구현 가능한 수준으로 적혔나
4. 화면 글자: 「원장 변경」 · 「원장을 변경할 수 없습니다.」 · 「고객 · 원장 · 관리실」 · 확인 창 모양 · 원장 이름 호버 — 결정에 없는 글자 · 새 규칙 지어낸 곳(새 OQ-34 ~ 37 포함 근거 확인)
5. lint --strict products/day ERROR 0

## 산출물
`/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/review-doc-fix3-report.md` · FAIL / WARN / PASS · 지적마다 파일:줄 + 근거. 완료 보고 두 명령(코디 핸들 `term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd`).
