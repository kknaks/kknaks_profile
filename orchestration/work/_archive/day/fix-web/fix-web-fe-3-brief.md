# [frontend] E1 · E2 · E4 — 방 카드 오더 메모 제목 줄 · 상담사 배지 · 펼치기/접기 · 14px

너는 **day frontend 워커**다(1차와 같은 규칙 · 같은 워크트리 · 1·2차 변경 위에 이어서). ⚠ backend 워커가 동시에 queries · dtos · services · 백엔드 테스트를 고친다 — 그쪽 파일 금지. 스냅샷 `cards[].counselors` 는 backend 가 만든다(계약대로 소비).

## 1. SSOT

### 사용자 결정 — E2E 1회차 수정(2026-11-12 · 정본)

원천: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/work/fix-web/e2e-feedback.md` 「E2E 피드백」 E1~E4 + 보충 · 조사 `research-2-report.md`(같은 폴더).

- **E1** 방 카드 오더 메모 펼침 아이콘(`.day-memo__more`) → **파란 글자 「펼치기」 / 「접기」**, 메모 **제목 줄 오른쪽 끝**.
- **E2** 오더 메모 글자 12px → **14px**(접힌 높이 `--day-memo-max-h` 를 14px 기준 5줄로 다시 계산).
- **E4** 오더 메모에 제목 줄: **「오더 메모」 + 상담사 이름 배지(작은 글씨 · 여러 명이면 여러 개)** … 오른쪽 끝 「펼치기/접기」. 그 아래 메모 내용. **구분선 없음.**
- **E3** 상담사 = **그 방문의 상담(`consultation`, 삭제 안 됨) 전부의 `counselor_id` 직원 이름** · 중복 제거 · 상담 시작 순. **migration 없음 · 동기화 변경 없음**(KOS 는 상담 하나에 상담사 여러 명 저장 안 됨 — 사용자). 희망 상담사(`requested_counselor_id`) 안 씀 · 상담사 없으면 제목 「오더 메모」만 · 메모가 없으면 지금처럼 메모 칸 자체 없음 · 비활성 직원도 이름 표시 · 상담 의사 범위 밖 · **앱 변경 0**(앱 방 상세 배지 안 넣음).

**계약(backend → frontend · 스펙)**: 스냅샷 `cards[]` 에 `counselors: [{"staffId": str, "name": str}]` (없으면 `[]`) — `orderMemo` 옆. 앱은 모르는 키를 무시(research-2 §5 `board.dart:210-224`).

## 2. 할 일

1. `templates/ui.html` `memo()` 매크로(:226-236) — 제목 줄: 「오더 메모」 + 상담사 배지들(작은 글씨 · 기존 배지 매크로 재사용 · 손 CSS 금지) + 오른쪽 끝 파란 글자 버튼 「펼치기」/「접기」(지금 아이콘 버튼 `.day-memo__more` 대체 · 5줄 넘을 때만 지금 규칙대로). 그 아래 내용 · 구분선 없음. 호출처 `board_parts.html:170` 에 `card.counselors` 넘김.
2. `static/day.js` 펼침 토글(:804-810 근처) — 글자 「펼치기」↔「접기」 전환 · aria 도 같은 글자.
3. `styles/app.css` — `.day-memo__box` 14px · `--day-memo-max-h` 14px 기준 5줄 · 제목 줄 · 파란 글자(기존 브랜드/링크 색 토큰) → `scripts/build-css.sh` 재빌드.
4. 견본 `routers/kit_board.py` · `kit_page.html` 메모 견본에 상담사 0 · 1 · 2명 사례.
5. 화면 문구 표 `tests/architecture/test_screen_copy.py` 에 「오더 메모」 · 「펼치기」 근거(사용자 E1 · E4 · 2026-11-12) 추가 · 안 쓰게 된 「메모 크게 보기」 등은 지운 문구로.
6. 화면 테스트: 제목 줄 · 배지 수(0/1/2) · 펼치기 글자 · 구분선 없음.

## 3. 검증 · 리포트

- 화면 테스트 + `-m "not infra"` 1회 · 인라인 스크립트 · style= · 손 CSS grep 0.
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/work/fix-web/fe-3-report.md`. 완료 보고는 1차와 같은 두 명령.
