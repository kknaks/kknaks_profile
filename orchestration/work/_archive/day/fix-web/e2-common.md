### 사용자 결정 — E2E 1회차 수정(2026-11-12 · 정본)

원천: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/work/fix-web/e2e-feedback.md` 「E2E 피드백」 E1~E4 + 보충 · 조사 `research-2-report.md`(같은 폴더).

- **E1** 방 카드 오더 메모 펼침 아이콘(`.day-memo__more`) → **파란 글자 「펼치기」 / 「접기」**, 메모 **제목 줄 오른쪽 끝**.
- **E2** 오더 메모 글자 12px → **14px**(접힌 높이 `--day-memo-max-h` 를 14px 기준 5줄로 다시 계산).
- **E4** 오더 메모에 제목 줄: **「오더 메모」 + 상담사 이름 배지(작은 글씨 · 여러 명이면 여러 개)** … 오른쪽 끝 「펼치기/접기」. 그 아래 메모 내용. **구분선 없음.**
- **E3** 상담사 = **그 방문의 상담(`consultation`, 삭제 안 됨) 전부의 `counselor_id` 직원 이름** · 중복 제거 · 상담 시작 순. **migration 없음 · 동기화 변경 없음**(KOS 는 상담 하나에 상담사 여러 명 저장 안 됨 — 사용자). 희망 상담사(`requested_counselor_id`) 안 씀 · 상담사 없으면 제목 「오더 메모」만 · 메모가 없으면 지금처럼 메모 칸 자체 없음 · 비활성 직원도 이름 표시 · 상담 의사 범위 밖 · **앱 변경 0**(앱 방 상세 배지 안 넣음).

**계약(backend → frontend · 스펙)**: 스냅샷 `cards[]` 에 `counselors: [{"staffId": str, "name": str}]` (없으면 `[]`) — `orderMemo` 옆. 앱은 모르는 키를 무시(research-2 §5 `board.dart:210-224`).
