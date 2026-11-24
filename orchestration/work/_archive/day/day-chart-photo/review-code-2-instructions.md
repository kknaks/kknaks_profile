# [reviewer] 재검수 2 — WP①·③ 고침 확인 (review-code-1 W1 ~ W7)

## 읽을 것
이 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/` 에서:
- 네 `review-code-1-report.md`
- `be-fix-1-instructions.md` · `be-fix-1-report.md`
- `fe-fix-2-instructions.md`(+ 인박스 보고)

결정 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md`:
- **C18 · C19 · C20 · C21** — C21 은 「매핑 뒤 DAY 직원 수」로 바뀌었다

SPEC 커밋 `b2005927`(mediness #960) 규칙 31.

## 작업 자리
워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-chart-photo` — read-only.

## 할 것
1. W1 ~ W7 이 결정대로 닫혔는지 본다(파일:줄 · 테스트 이름)
2. 새 테스트가 실제로 그 틈을 덮는지 본다. 예:
   - 409 뒤 동기화 이력이 쌓인 다음 다시 저장 → 200 · 글 한 번
   - 응답 유실 뒤 같은 저장 → 200 · 이력 1
   - CRLF 줄 → 409 아님
   - 보내는 중 칸 잠김
3. 고침이 만든 새 어긋남이 없는지 본다
4. 관문 명령 1회:
   - `scripts/test.sh -q backend/tests/day/board backend/tests/day/web`
   - ruff
   - `npm run -s check`

**범위 밖**: 사진 서버(WP②)는 아직 없다.

## 보고
- 리포트 `review-code-2-report.md`(같은 폴더) — 판정 · 지적
- 수정 · 커밋 금지
- 완료 = preamble worker_done 두 채널
