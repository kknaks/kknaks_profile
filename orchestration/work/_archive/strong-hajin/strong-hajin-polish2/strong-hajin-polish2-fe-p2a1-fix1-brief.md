# [frontend] WORK-009 Phase 2a-1 — 검수 WARN 재수정 (fix1)

앞 판 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/strong-hajin-polish2-fe-p2a1-brief.md` 의 규칙이 그대로다(subject 「frontend 완료: WORK-009 Phase 2a-1 fix1」). 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/review-fe-p2a1-report.md` W-1~W-4 를 전부 읽어라. 코디 판단: **넷 다 고친다**, 권장 수정대로.

1. **W-1** 저장이 낡음(422 낡음 문장)으로 거부되면 **최신 회차를 다시 읽는다** — 채팅은 `refreshProjections()`, 홈·칩 창은 `onDone()`. 창 입력은 그대로 남고 문구는 창 안에. 다시 「저장」하면 새 base 로 통과(SPEC-002 §4·§6). **저장 경로만** — confirm 낡음(기존 부채)은 이번엔 손대지 않는다
2. **W-2** 저장 중에는 창이 닫히지 않는다 — `axDraft` 모드에서 `isWorking` 일 때 ×·Esc·바깥 클릭 무시 **그리고** 카드 「등록」·「거절」·「수정」을 저장 중 잠근다(카드 busy). 일반 「새 업무 추가」의 닫기 동작은 그대로
3. **W-3** 저장 성공 뒤 갱신(onDone·refreshProjections) 실패를 **저장 실패와 분리** — 저장은 성공으로 알리고(창 닫힘/카드 새 회차는 저장 응답 기준), 갱신 실패는 기존 staleProjection 띠·알림으로. 「저장했습니다」와 「저장 실패」가 같이 서지 않게
4. **W-4** 테스트를 실제 배선으로 — App 수준 성공 경로 1건(채팅 카드 수정 → 저장 → `/commands/save_draft` → 대화 재조회 → 카드 「N+1회차」 → 등록이 새 base) · AxDraftModal rerender 2건(옛 item 이 다시 와도 높은 회차 유지 / 더 높은 item 이면 따름) · W-1·W-2·W-3 각각 1건
