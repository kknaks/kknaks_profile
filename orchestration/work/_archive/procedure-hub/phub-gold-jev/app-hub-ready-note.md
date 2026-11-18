# [코디 → app] 허브 준비 (11-16)

- 로컬 허브가 **코디 세션에서** 떠 있다: `http://127.0.0.1:18105` — **띄우거나 내리지 마라**(코디 몫).
- health = `/procedure-hub/gold/health` · REST = `/procedure-hub/gold/{resolve,scope,neighbors,facets,concern-candidates,pair,evidence}` · MCP = `/procedure-hub/gold-mcp/mcp`
- 응답 머리 `build.gold_hash` = `8accbb21…` 확인됨(코디 curl).
- backend 가 정한 꼴: 오류 본문 `{"detail":"<code>: <사유>"}` · 목록 쿼리 = 콤마 · `filters` = `칸=값` 되풀이.
- 이제 WORK-002 §11 대로 **E4(모의 ↔ 실물 꼴 대조) → WP-3 · WP-4 실물 · WP-6 답 키** 를 진행하라. 꼴이 SPEC-001 과 다르면 고치지 말고 코디에게 `[질문] app:` 로.
