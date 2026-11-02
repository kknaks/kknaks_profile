# [reviewer 코드 검수] WORK-012 WP3 (BE + FE)

기존 브리프(`strong-hajin-enhance-review-brief.md`)의 규칙 그대로 — **읽기 전용**, 리포트 한 장, 시험·빌드·서버 실행 금지(수치는 워커·코디가 낸다).

- 대상: 코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-enhance` 의 **미커밋 변경 전부**(`git diff` · `git status` — 새 파일 포함)
- 계약: `P/30-work/work-012-enhance.md` 「Phase WP3-BE」·「Phase WP3-FE」 의 체크박스 + Code Surface WP3 표 · SPEC-010 · SPEC-008 v0.6.0 해당 절
- 워커 리포트: `W/be-wp3-report.md` · `W/fe-wp3-report.md` · 기준선 `W/be-baseline.md` · `W/fe-baseline.md`

물음:
1. 계약 체크박스마다 구현됐나(파일:줄) — 빠진 것·다르게 한 것
2. **Code Surface 전수** — WP3 표의 자리를 네가 다시 grep 해 변경이 닿았나. 같은 심볼·패턴을 쓰는데 안 닿은 자리
3. BE↔FE 계약 일치 — 안건 `source` 페이로드 · `download=1` · 받기/원본 주소 · `integration.changed` 사건 모양
4. 회귀 위험 — 기한 규칙 변경이 다른 호출자에 · `download=1` 이 미리보기 경로에 · SVG 허용이 첨부(`_download`) 경로에 새지 않나 · 공유 상수 분리(「빠른 회의」)
5. 시험이 계약을 실제로 잡나(이름만 있고 단언이 약한 시험)
6. **사람 눈에 이상해 보일 자리** — 앱 E2E 에서 사용자가 걸릴 곳

리포트: `W/review-wp1-code-report.md` · 판정 PASS/WARN/FAIL · §끝에 FAIL/WARN 목록(워커 재발주용, BE/FE 구분).
완료 보고: 기존 브리프 §6 두 명령(subject 「reviewer 완료: WP3 코드 검수 <판정>」, 리포트 이름만 바꿔서).

## WP3 에서 특히 볼 것
- BE↔FE 계약 고정 문서 `W/wp3-contract-fixed.md` 네 항목이 양쪽에 그대로인가
- Connect 수정 경로: 방 유지 재확인 · `null` 취소 · 방 이동(PUT 또는 Idempotency-Key 울타리 새 예약) — 이중 예약·예약 유실 갈래 · Connect 예약행 id = 외부 번호 가정(BE 미결)
- 옛 `meeting.update` 가 새 재확인·409 를 비켜 가지 않나(AC-21)
- AX 회의 생성 카드: 업무 생성과 흐름·디자인만 같고 **내용은 회의 고유 필드**(OQ-901) — 프로젝트·연관 업무 필드가 새어 들어오지 않았나
- AI 맥락 목록이 AX 대화 매 턴에 실린다(조직 전체 — 코디 판정, D-13) — 대화 프롬프트 크기도 stdin 경로인가
- WP2 WARN W-r2-2·3·4 · WP1 W-2·W-3 이 고쳐졌나
- 상세 `room_reservation` 에 `room_id` 가 없다(BE 미결) — FE 가 기존 줄을 어떻게 아는가, 결함인가
