# planner 수정 1판 — SPEC-007 · WORK-011 (검수 FAIL 1 · WARN 6)

검수 리포트: `orchestration/work/agency-settlement/review-spec-007-report.md` — 먼저 전부 읽어라.
SoT `_RESUME.md` §2 를 코디가 고쳤다(W-1 · W-2 · W-3 줄). 그것을 근거로 인용한다.

1. **F-1** — 리포트 「고칠 것」 그대로: 없음 = HTTP 400 + `errorProperties` `{key: purchaseId|visitorId, reason: NotFound}` 일 때만. 다른 400 · 404 = `kos_rejected`. §6.4 · §4.3 · §9.1 #9 고치고 「400 다른 reason → 달 전체 502」 시험 추가. WORK WP-BE 완료 조건도 맞춘다
2. **W-1** — ③ = `findScheduleByPurchaseId` 확정(_RESUME §2). OQ-903 닫음 · 방문일 = `reservation.startDateTime`
3. **W-2** — 운영 키 · WP-LIVE 는 _RESUME §2 확장 줄을 근거로 단다
4. **W-3** — 정책: **품목 줄은 그 수납의 첫 승인 결제가 있는 달에만**, 다른 달엔 결제 · 취소 줄만(_RESUME §2). OQ-906 을 이 결정으로 닫고 §6.2 고침. WP-LIVE 에 「승인 결제가 두 달에 걸친 수납 수」 L 줄
5. **W-4** — §9.2 에 L10 추가(리포트 그대로). 444 의 정의: 코디가 10-28 수집본에서 **수납마다 「`purchaseStatus` ≠ REFUNDED 인 품목 `cost.totalAmount` 합」 = 「그 수납의 결제 행(APPROVED + CANCELED 음수) 전부 합」** 을 비교해 품목 있는 수납 444건 전부 일치. 즉 환불 품목 금액은 **원 가격**으로 보이고(REFUNDED 품목을 빼야 순액과 맞음) — 이 근거로 OQ-902 기본값을 적되, WP-LIVE L10 으로 실물 확인
6. **W-5** — (a) 로: `lines[].currency` · 수납 `currency` 추가. 통화가 섞인 수납은 합계 대신 `⚠` (10월은 전부 KRW)
7. **W-6** — OQ-906 에 「배지 문구 · 조건은 WP-LIVE L5 · L10 결과로 정함」 적기
8. **NOTE 2 · 3 · 4 · 5** 반영(오프셋 파싱 시험 · ③④ 응답에서 name · startDateTime 만 꺼내고 원본 캐시/로그 금지 · 토큰 재발급 잠금 · 번호 없는 기본값 OQ 로). NOTE 1(결제일)은 OQ-904 그대로 두고 상태를 「사용자」로
9. 판을 0.1.1 로 · 검증 §8(근거 태그 · public grep) 다시 돌려 보고에 적는다

allowed_paths · 하지 말 것은 원 브리프 그대로. 끝나면 원 브리프 §9 두 채널로 보고(subject 「planner 수정 1판 완료」).
