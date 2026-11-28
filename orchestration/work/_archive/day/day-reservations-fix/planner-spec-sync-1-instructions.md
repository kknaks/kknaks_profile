# [planner · 마감 1] spec-sync — 코드 · e2e 에서 정한 것을 SPEC 에 (PR mediness#971)

같은 터미널 · 같은 SPEC 워크트리(브랜치 `kknaksss/day-reservations-fix-spec` · PR #971). 사용자 「dev 에 병합하고 작업 다 마무리하자」(11-28). 고친 뒤 **커밋 · push 해서 #971 에 얹어라**(머지는 코디).

## 반영할 것 (`/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/_RESUME.md` §2 11-28 행 · 코드 = CENTURION_DAY PR #303 `d1ce8ea8`)
1. **W-a**: [+] 칸 · 빈 칸 누르기 시각 단위 = **그 열 그룹 간격**(60분 그룹 = 정각만 · 등록 창 시간 늘 골라짐) — SPEC-007 `:109` 「열 × 30분 칸」 · SPEC-006 F1/U-10 해당 줄. 끌어 놓기(옮기기) 단위는 30분 그대로.
2. **D44 시한**: 링크 다시 쓰기 = 기기 없는 열린(pending · opened) 문진 요청 **중 시한 안**만 · 앱 JSON 경로는 늘 새 요청(F-1) — SPEC-007 규칙 2 · 7.
3. **OQ-D43 닫음**: 링크 요청 진행 칸 pending 줄 = 「남은 시간 mm:ss」만(카메라 글자 · [QR 닫기] 없앰) — OQ 표 닫힘 + 본문.
4. **KOS 문진 제출 실패 기록**: `crm_error` 에 KOS 오류 이름(className) 포함 — 해당 절에 한 줄.
5. **알고 감 / 다음 작업 OQ 로 남김**(열린 채): ⓑ 제출 500 인데 KOS 저장 → [다시 보내기] 이중 제출 · ⓒ 휴대폰 국가번호 빈 값(500 유력 원인 · `e2e-2-report.md`) · 「6개월 경과」 고객 건강정보에 옛 답 보임 · D45 · 기기 줄 · 태블릿 = dev 실기기 확인 대기 — 각각 근거 리포트 경로.
6. 코드와 SPEC 이 다른 곳이 더 있으면(`be-1-report.md` 「이슈」 · `review-code-1-report.md` 참고 · `qa-2-report.md` 관찰) 찾아 한 줄씩 — 지어내지 말고 코드 file:line 근거.
7. log 한 줄 · lint `--strict` products/day ERROR 0.

## 금지
결정 다시 열기 · 문구 짓기 · 코드 · PR 머지.

## 보고
`/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/planner-spec-sync-1-report.md` — 고친 줄 · 남긴 OQ · 커밋 sha · lint. 완료 보고 두 명령(subject 「planner 완료: spec-sync」 · 코디 `term_99b025fc-f3ef-403e-8162-509c41545e2e` — preamble 우선).
