# [reviewer 코드 검수] WORK-012 WP4 (BE + FE) + SHELL

기존 브리프(`strong-hajin-enhance-review-brief.md`)의 규칙 그대로 — **읽기 전용**, 리포트 한 장, 시험·빌드·서버 실행 금지(수치는 워커·코디가 낸다).

- 대상: 코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-enhance` 의 **미커밋 변경 전부**(`git diff` · `git status` — 새 파일 포함)
- 계약: `P/30-work/work-012-enhance.md` 「Phase WP4-BE」·「Phase WP4-FE」·「Phase SHELL」(011 만) 의 체크박스 + Code Surface WP4 · SHELL 표 · SPEC-010 · SPEC-008 v0.6.0 해당 절
- 워커 리포트: `W/be-wp4-report.md` · `W/fe-wp4-report.md` · `W/fe-shell-report.md` · 기준선 `W/be-baseline.md` · `W/fe-baseline.md`

물음:
1. 계약 체크박스마다 구현됐나(파일:줄) — 빠진 것·다르게 한 것
2. **Code Surface 전수** — WP3 표의 자리를 네가 다시 grep 해 변경이 닿았나. 같은 심볼·패턴을 쓰는데 안 닿은 자리
3. BE↔FE 계약 일치 — 안건 `source` 페이로드 · `download=1` · 받기/원본 주소 · `integration.changed` 사건 모양
4. 회귀 위험 — 기한 규칙 변경이 다른 호출자에 · `download=1` 이 미리보기 경로에 · SVG 허용이 첨부(`_download`) 경로에 새지 않나 · 공유 상수 분리(「빠른 회의」)
5. 시험이 계약을 실제로 잡나(이름만 있고 단언이 약한 시험)
6. **사람 눈에 이상해 보일 자리** — 앱 E2E 에서 사용자가 걸릴 곳

리포트: `W/review-wp1-code-report.md` · 판정 PASS/WARN/FAIL · §끝에 FAIL/WARN 목록(워커 재발주용, BE/FE 구분).
완료 보고: 기존 브리프 §6 두 명령(subject 「reviewer 완료: WP4 코드 검수 <판정>」, 리포트 이름만 바꿔서).

## WP4 · SHELL 에서 특히 볼 것
- BE↔FE 계약 고정 `W/wp4-contract-fixed.md`(참고 자료 한 줄 `turn_id`·`label`) · SPEC-008 §4.8 메시지 맥락 모양(줄 = at·sender·text·attachments 이름·thread_reply_count · target · 원문 JSON 제외)
- `inbox_message` 참고 자료 나열 지점 다섯 전부 · 남의 메시지/지운 방 404 · 100줄 경계 · 스레드 답글 = 스레드 전체 · 메일 = 안전본 글자(HTML·추적 이미지 안 실림)
- 업무 출처 `source_inbox_message_id` + 운영 SQL 2개(`2026-10-07-inbox-message-origin*.sql`, CONCURRENTLY 갈래) 와 ORM 일치 · `inbox.message_updated` 는 커밋 뒤
- 012 나간 방: 그 회원 방만 / 보관·삭제는 고른 회원 전부 · 즉시 paused · 다른 회원에게 새지 않나
- 호버 막대: 로컬(보내는 중) 줄 없음 · 키보드 포커스 · 패널 안 답글은 스레드 아이콘 없음 · AX 서랍 새 대화
- **SHELL 011**: `guard::navigation_verdict` — about:blank·srcdoc 허용이 외부 origin 차단·`/api/` 가로채기를 깨지 않나 · 주 프레임 about:blank 허용이 안전하다는 FE 근거(`fe-shell-report.md` §2)가 맞나
