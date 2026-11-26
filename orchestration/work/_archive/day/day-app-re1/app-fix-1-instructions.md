# [mobile] app-fix-1 — review-code-1 W1 · W2 · W8 + 사용자 확인 Q1 · Q2(추천값)

너는 day `mobile` 워커다. 역할 · allowed_paths · 검증 · 완료 보고는 같은 폴더 `day-app-re1-app-brief.md` 를 그대로 따른다(먼저 읽어라). 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1` — 커밋 `43ba40a3` 위. **backend 워커가 같은 시각 `backend/` 를 고친다 — 건드리지 마라.** 코디의 로컬 스택도 건드리지 마라.

읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/review-code-1-report.md` §W1 · §W2 · §W8 · §4 Q1 · Q2 · §9(사용자가 시뮬레이터에서 만날 자리 — 싸게 고칠 수 있는 것이 있으면 리포트에 목록만, 고치지는 마라).

할 것:
1. W1 — 삭제 · 다시 시도 · 올리기 중에는 10초 tick 을 건너뛰고, 조작 응답보다 먼저 시작한 GET 응답은 버린다(세대 번호) · 테스트
2. W2 — 받기 실패한 사진을 다시 그릴 때마다 다시 받지 않게(실패 캐시 · 목록이 바뀔 때만 다시) · 테스트
3. W8 — 셸 `NavigatorPopHandler` 뒤 「룸 상세 · Android 뒤로 = 목록」 회귀 위젯 테스트
4. **Q1(코디 추천 = 결정)** — 알림 행 · 원장 호출 푸시 · 채팅 푸시 · 채팅 배너 [보기] · 채팅 거절(`shell.dart` :165 · :173 · :182 근처 `popUntil`)이 **미저장 차트 위로 이동할 때 = ✕ 와 같은 확인 창**(「저장하지 않고 닫을까요?」 · [계속 쓰기] · [버리고 닫기] — SPEC 에 있는 글자). [버리고 닫기] → 원래 이동 · [계속 쓰기] → 이동 안 함. 미저장 없으면 지금처럼 바로 이동 · 테스트
5. **Q2(코디 추천 = 결정)** — 룸 상세가 닫히거나(목록으로) 그 방문 카드가 판에서 빠질 때, 그 방문에 대해 세션 Navigator 에 띄운 **확인 시트 · 창 · 원장 고르기 / 방 옮기기 팝오버는 같이 닫는다**(route 를 기억해 지움). **차트 창은 OQ-A69 대로 남긴다** · 테스트

하지 말 것: 브리프 §7 그대로 · 새 화면 글자 없음 · W3 · W4(크게 보기 꼴 · 저장 띠 자리)는 2루프 몫 — 건드리지 마라.
검증: 브리프 §8(analyze · test · build ios --no-codesign). 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-app/orchestration/work/day-app-re1/app-fix-1-report.md`. 커밋 · push 금지.
완료 보고: dispatch preamble 의 `worker_done`(`--report-path` 위 리포트) + 브리프 §9 (2) 직접 주입.
