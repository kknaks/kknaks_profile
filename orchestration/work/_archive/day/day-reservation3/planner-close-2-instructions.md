# [planner] SPEC-008 마감 고침 — review-doc-5 WARN 4 (planner-close-2)

같은 워크트리(`day-reservation3-spec` · rebase 끝남 · HEAD = 마감 한 커밋). 근거 = `review-doc-5-report.md` WARN 표(파일:줄 · 고칠 방향 그대로). **git 명령 금지** — 파일만. 코디가 amend 한다.

- X1 `log.md:50`(11-25 행) — origin/main 글 그대로 「개정 ⑭」로 되돌린다(`git show origin/main:products/day/log.md` 로 확인).
- X2 SPEC-008 `:290` · `:336` · `:538` · `:592` — 「스레드에 고객이 아직 없음(초진 생성 확인 대기) = 막지 않음 · 비교 = 스레드 고객 ↔ 새 판정 고객」 한 줄.
- X3 SPEC-008 `:455` · `:500` 409 칸 + SPEC-007 고침 7 같은 줄 — 오류 코드 `request_thread_write`.
- X4 SPEC-001 `:206` 대응표 칸 — 「로그인 뒤 갈 곳 = 예약 현황 → `reservation` view(모든 직무 기본값 · SPEC-006 R31)」. (사용자 11-27: 현황 화면은 모든 직원이 본다.)

검증 lint `--strict` ERROR 0. 보고는 terminal send 한 줄(파일:줄) — 리포트 파일 없어도 됨.
