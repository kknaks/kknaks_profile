# [reviewer_doc] 리뷰 — SPEC-002 개정 ⑯ · SPEC-000 (차트 · 방 이동)

같은 규칙(`review-doc-fix2-brief.md` — 읽기만 · 수정 · 커밋 · KOS 금지 · 리포트 1개). 대상: `git -C /Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec diff`(커밋 bd029f3c 이후 — spec-002 · spec-000 · erd.md · log.md). 지시: 같은 폴더 `planner-spec16-brief.md`.

정본 = `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/_RESUME.md` §2 의 2026-11-10 **차트 · 방 이동 행 전부** + HAR 분석 `research-har-room-chart-report.md`.

## 볼 것
1. 결정이 빠짐없이 · 틀림없이: 차트(탭 · 표 · 직무별 첫 탭 · 담당자 DAY 만 · 필수 · 집도의 KOS · 메모 KOS 쓰기 · 저장 순서 · 자동 저장 시점 · 「최근 저장 : HH:MM」 · 이력 DAY · 동시성 4갈래 · 작성자 1명 · 일괄 적용 뺌) / 방 이동(점유 이동 · 복귀 · 전체 이동 — **완료 포함 전부** · 파란 띠 [복귀하기] · 기존 방 카드 없음 · 제한 없음 · 침대 수 없음 · 점유 = 계산) / 시술 완료 탭(원래 방 묶음 · 오늘만 · 관리실 기록 창 없음)
2. **결정에 없는 것을 새로 정한 곳** — 특히 새 칸 2개(started_room_id · visit_task_chart_log)가 값에서 나왔나 · 새 OQ-38 ~ 47 근거 · API(제안) · 오류 글자 · 메뉴 글자(OQ-40) · OQ-42(의사차트로 준비중 시술 집도의 바꾸면 호출 없이 시작 켜짐 — 앞 결정 「수락 → 시작 명시적」과 부딪히는지)
3. KOS 쓰기 표 확인 상태가 HAR 사실과 맞나(「확인 안 됨」을 「확인됨」으로 올린 곳 없나)
4. 앞 판(⑬ ~ ⑮) · 「뺌 U5」 · 「읽기만 U11」 반대 문장 남음 · 앞뒤 안 맞음
5. lint --strict products/day ERROR 0

## 산출물
`/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/review-doc-spec16-report.md` · FAIL / WARN / PASS · 파일:줄 + 근거 · 「사용자 확인 필요」 표 따로. 완료 보고 두 명령(코디 핸들 `term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd`).
