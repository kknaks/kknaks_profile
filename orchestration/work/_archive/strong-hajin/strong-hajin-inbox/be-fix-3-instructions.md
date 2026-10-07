# [backend] BE 수정 판 3 — FE 가 요청한 응답 칸 (2026-10-06)

수정 판 1·2 에 이어 같은 판으로. 근거 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/fe-report.md` 「BE 요청」. SPEC-008 범위 안에서:
- 방 메시지 응답에 **사용자 이름표**(보낸 사람 id → 이름·아바타 — 응답에 users 맵) · 슬랙 멘션 이름 풀기에 씀
- 메시지 **퍼머링크**(슬랙 「슬랙에서 열기」 — 워크스페이스 domain 포함)
- `/me` 에 **직책·직무**(명부 값, 프로필 머리 읽기 전용용)
- F-2 `available-rooms` 는 판 2 에서 만든다 — 모양을 fe-report 의 기대와 맞춰라
바뀐 응답 모양은 보고에 표로. 끝나면 §9.
