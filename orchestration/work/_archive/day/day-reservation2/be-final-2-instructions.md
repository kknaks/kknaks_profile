# [backend · 마무리 2] W13 시술만 진행 [시술 대기] 완성 + 남은 실패 2개

같은 터미널 · 같은 맥락 · 질문 없이.

1. **W13 완성**(지금 400 으로 막아 둔 것): 계획 단계에서 KOS `ticket/v1/queries/get-ticket-bundles {visitorId}` 원문을 읽어 시술권 작업 본문을 채운다(be-probe-3 ⓐ · HAR `시술권사용.har` #15 · #28 모양 · round = D48 · 여러 장 한 요청 가능). 순서 = 「방 배정」 작업 → 방 지정 → 시술권 작업들 → **`add-flow-tasks` 2xx 뒤 바로 상세 조회로 새 시술 작업 sequence 를 찾아**(방 배정 연쇄 `_chain_room_assign` 와 같은 예외 · SPEC-002 ㉘) 같은 방 지정 → 오더 메모(빈 글이면 건너뜀 · D56) → `PROCEDURE_WAITING`. 확인 · D53 즉시 확인 · `write_confirmed` 는 다른 쓰기와 같게. 시술 중 귀가(W14) 는 이미 했으면 확인만
2. `test_alembic::test_unknown_ticket_price_migration` — 0024 칸 때문에 옛 revision ORM insert 가 깨짐 → 고쳐라(그 테스트가 쓰는 ORM 모델 · migration 순서 확인)
3. architecture `test_web_rules` CSS 빌드 실패 — frontend 가 끝났으니 `scripts/build-css.sh` 1회 뒤 다시(되면 끝 · 화면 몫이면 리포트에)

검증 = `scripts/check.sh` 1회(전체) — 실패 0 이 목표 · 무관 실패는 이유. 완료 보고 두 명령(subject 「backend 완료: 마무리 2」 · 이번 dispatch 값).
