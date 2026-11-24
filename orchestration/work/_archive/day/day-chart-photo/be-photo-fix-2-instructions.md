# [backend] photo fix-2 — 결정 C25 · C27

## 읽을 것
- 결정 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md` 의 C25 · C27
- 검수 리포트 `review-code-3-report.md` 의 P2 · P3
- SPEC 고침 `planner-fix-9-report.md`

## 할 것
### C25 — 가져오기 작업에 KOS 삭제 다시 하기
- 대상: 그 방문의 지운 행(`deleted_at`) 중 external_ref 가 살아 있는 것
- 가져오기 작업이 그 행의 KOS 삭제를 다시 한다
- 성공하면 ref 를 정리한다(규칙대로)
- 실패하면 조용히 다음 번으로 넘긴다
- 테스트를 붙인다

### C27 — KOS 실패 토스트 글자
- `kos_error` 가 있으면 `message` 에 「KOS 반영에 실패했습니다」를 넣는다
- 대상: 올리기 · 삭제 · 다시 시도
- 글자 상수는 기존 메시지 모음 방식을 따른다
- 테스트를 붙인다

## 하지 마라
- 템플릿 · JS — frontend 몫
- 커밋

## 검증
- `scripts/test.sh -q backend/tests/day/board`
- ruff

## 보고
- `be-photo-fix-2-report.md`
- preamble 의 worker_done 두 채널
