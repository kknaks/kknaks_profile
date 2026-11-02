# [reviewer 재검수] WP2 수정 1 — 고친 자리만

기존 규칙 그대로(읽기 전용 · 실행 금지 · 리포트 한 장). 대상 = `W/be-wp2-fix1-report.md` 가 적은 변경(코드 워크트리 미커밋 diff 중 WP2 수정분).

- 네 리포트 `review-wp2-code-report.md` 의 F-1 · F-2 · W-1 · W-2 · W-3 · W-4 가 각각 고쳐졌나(PASS/FAIL · 파일:줄)
- **새로 생긴 위험**: lease heartbeat(연장 실패·스레드 정리) · 웜스타트를 락 안으로 옮긴 뒤 락 보유 시간(웜스타트 240초 동안 다른 경로가 막히나 — 회의 종료·재시도와 교착) · 세션 CAS 실패 갈래 · **stdin 전달**(쓰기 스레드 · 자식이 일찍 죽을 때 BrokenPipe · timeout 과 함께 · 큰 입력 교착 · 취소)
- 리포트: `W/review-wp2-r2-report.md` · 완료 보고: 기존 두 명령(subject 「reviewer 완료: WP2 재검수 <판정>」). **코디handle = term_367ca23a-f846-44c0-afc7-07b6655df214**
