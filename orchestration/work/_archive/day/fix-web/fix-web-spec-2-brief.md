# [planner] E2E 1회차(E1~E4) — spec-002 보강

너는 **day planner 워커**다(역할 문서는 이미 읽었다 — 같은 규칙). 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/fix-web-spec` (개정 ⑳ 미커밋 위에 이어서).

## 1. SSOT

### 사용자 결정 — E2E 1회차 수정(2026-11-12 · 정본)

원천: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/work/fix-web/e2e-feedback.md` 「E2E 피드백」 E1~E4 + 보충 · 조사 `research-2-report.md`(같은 폴더).

- **E1** 방 카드 오더 메모 펼침 아이콘(`.day-memo__more`) → **파란 글자 「펼치기」 / 「접기」**, 메모 **제목 줄 오른쪽 끝**.
- **E2** 오더 메모 글자 12px → **14px**(접힌 높이 `--day-memo-max-h` 를 14px 기준 5줄로 다시 계산).
- **E4** 오더 메모에 제목 줄: **「오더 메모」 + 상담사 이름 배지(작은 글씨 · 여러 명이면 여러 개)** … 오른쪽 끝 「펼치기/접기」. 그 아래 메모 내용. **구분선 없음.**
- **E3** 상담사 = **그 방문의 상담(`consultation`, 삭제 안 됨) 전부의 `counselor_id` 직원 이름** · 중복 제거 · 상담 시작 순. **migration 없음 · 동기화 변경 없음**(KOS 는 상담 하나에 상담사 여러 명 저장 안 됨 — 사용자). 희망 상담사(`requested_counselor_id`) 안 씀 · 상담사 없으면 제목 「오더 메모」만 · 메모가 없으면 지금처럼 메모 칸 자체 없음 · 비활성 직원도 이름 표시 · 상담 의사 범위 밖 · **앱 변경 0**(앱 방 상세 배지 안 넣음).

**계약(backend → frontend · 스펙)**: 스냅샷 `cards[]` 에 `counselors: [{"staffId": str, "name": str}]` (없으면 `[]`) — `orderMemo` 옆. 앱은 모르는 키를 무시(research-2 §5 `board.dart:210-224`).

## 2. 할 일

1. spec-002 개정 ⑳ 에 E1~E4 를 더한다: U-1 카드 메모(:182 근처 — 제목 줄 「오더 메모」 · 상담사 배지 · 오른쪽 끝 「펼치기/접기」 · 14px · 5줄 · 구분선 없음) · E39(:166) · 스냅샷 `cards[].counselors`(:603) · 동기화 표 consultation 행(:747 — 「이 화면에서 쓰지 않는다」였다면 판 메모 제목 줄에 씀으로) · ⑳ 머리 메모 · 개정 ⑳ 차이표. spec-000 은 바꾸지 않는다(한 상담에 한 명 그대로 · KOS 가 여러 명 저장 안 함 — 사용자 근거 한 줄 OQ-13 에 남겨도 됨).
2. spec-003: 앱 변경 0 · 새 칸 무시 사실 한 줄.
3. 화면 문구는 사용자 말만: 「오더 메모」 · 「펼치기」 · 「접기」.
4. lint --strict 1회 · Delivery Issue 는 건드리지 마라(나중에 v2 재결속 때 함께).

## 3. 범위 · 리포트

- 코드 워크트리 수정 · 커밋 · push 금지.
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/work/fix-web/spec-2-report.md` (변경 파일:줄). 완료 보고는 1차와 같은 두 명령(코디 `term_b1db5638-c143-4f48-b35e-4550ff2d45d4`).
