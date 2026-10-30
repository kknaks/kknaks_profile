# [planner] 직원 앱 내부 채팅 — SPEC-007 · WORK-011 r2 (리뷰 r1 처분)

역할 · allowed_paths · 하지 말 것 · 검증 · 완료 보고(§9 두 명령)는 **앞 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/internal-chat-spec-brief.md` 그대로**다. 먼저 그 브리프와 역할 문서를 읽어라. 리포트만 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/spec-r2-report.md` 로 새로 쓴다(subject 「planner r2 완료: …」).

## 읽을 것
- 리뷰 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/review-doc-r1.md` (FAIL 4 · WARN 17 · 사용자 판단 후보 7)
- 앞 판 리포트 `spec-report.md`
- **DEC-009 에 새 줄 D-38 ~ D-44**(코디가 더함 — 리뷰 처분 · 사용자 결정): `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/10-decision/decision-009-internal-chat.md`

## 처분 (코디)

| 지적 | 처분 |
|---|---|
| F-1 헤더 | **D9-38** 대로: 폰 · 아이패드 = 지금 `AppHeader`([Céramique][채팅][종]) · 아래 줄 = 제목 없이 [새 대화] · 아이패드는 방 목록 칸 위 [새 대화]. 대화 칸 머리(뒤로 유무 · 폰 대화 화면 헤더)를 적는다. 시안과 다른 곳 표에 더한다 |
| F-2 시각 | 채팅 표 시각은 **밀리초**로 저장한다(`clock.to_db` 와 별도 함수 또는 인자 — 기존 표는 그대로). `since` 는 `>=` 로 받고 앱이 `id` 로 겹침을 지운다. 안 읽음 기준도 같은 꼴로 잃지 않게(예: 메시지 id 단조 증가면 `last_read_message_id` 도 검토 — 고른 것을 근거와 함께). API 시각 꼴(지금 `iso()` KST 오프셋인지)과 `since` 파싱(문자열 비교 금지 · parse 뒤 비교)을 적는다. 같은 밀리초 · 같은 초 경계 시험을 §13.1 에 |
| F-3 async | §6.1 에 「SSE · 푸시를 내는 경로는 `async def`」 · §12 에 `push.py:175-187` · `stream.py:59-75` · §13.1 에 「HTTP 경로로 보내서 가짜 APNs 에 닿음」 단언 |
| F-4 숨김 | **D9-44** 대로 · 배너 자리(셸 안 vs 루트 층)를 정하고 근거 · §12 에 `launchers.dart:86-98 · 103` · `main.dart:33-38` · §13.2 에 「예약 상세에서 연 QR 중」 |
| W-1 ~ W-17 | **전부 반영**. 리뷰의 「고칠 것」 · 근거 줄을 따른다. W-6 근거 없는 값은 근거를 달거나 「기본값」 + OQ 번호. W-7 은 기존 `Switch.adaptive` · `MiniChip` / `StatusChip` 재사용(안 쓰면 이유). W-12 는 앱이 늘 JPEG 로 다시 인코딩 + C5 에 「앨범 스크린샷(PNG) 1장」. W-17 SPEC-004 §6.8 「4칸」 · 「4탭」 두 줄에 「(채팅 더해 5 — SPEC-007)」 — SPEC-004 는 이 두 줄과 앞 판 3줄 말고 고치지 않는다 |
| 사용자 판단 후보 | 2 → D9-39 · 3 → D9-41 · 4 → D9-40 · 5 → D9-42(OQ-904 뒤집음) · 6 · 7 → D9-43. OQ 표에서 닫힌 것은 「닫힘 → D9-nn」 |
| 코디 몫 | OQ-920 경로 수: SPEC-007 은 코드 51 기준 그대로 · SPEC-004 §7.3 은 이번에 안 고침(열린 채로). OQ-931: WORK-011 WP-E2E 첫 줄에 확인 단계(W-16) |

## 검증 (앞 브리프 §8 + 아래)
- DEC D-01 ~ D-44 → SPEC 대조 빠짐 0 (부록 A 갱신)
- 리뷰 FAIL 4 · WARN 17 → 고친 곳(파일:줄) 대조표 · 처분 못 한 것 0
- SPEC-007 0.1.0 → **0.2.0** · 바뀐 줄 끝 `(r2)` · 머리 변경 표
