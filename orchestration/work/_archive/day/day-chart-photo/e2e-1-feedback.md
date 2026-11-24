# 최종 e2e 1회차 피드백 (2026-11-24 · 사용자) — 모아서 한 번에 2루프 발주

## E1 — 차트 저장 거절 때 토스트가 없다
- 원인: `chart_staff_required` · `staff_not_listed` · `chart_conflict` 가 글자 미정(`board_messages.py` UNSET · OQ-41 · OQ-90)이다.
- 실물: 07:49:50 · 07:50:53 409 — 화면 표시가 없었다.
- 글자 제안(사용자 답 대기):
  - 「담당자를 선택해 주세요」
  - 「다른 곳에서 먼저 수정된 내용이 있습니다. 확인 후 다시 저장해 주세요」
  - 「선택할 수 없는 담당자입니다」

## E2 — 사진 여러 장 올리기 → 결정 C28
- 지금: `board_photos.html:38` 에 `multiple` 없음 · 서버 file 1개.

## E3 — 차트 [저장]마다 KOS 시스템 계정이 새로 sign-in 한다(코디 로그 발견)
- 매번 「기기 5개 한도」 → 가장 오래된 같은 표시 세션 해제 → 재로그인(api.log 07:49:50 · 07:50:53).
- C17 저장 전 KOS 읽기가 시스템 토큰을 재사용하지 못하는 것으로 보인다 — 원인 확인 필요.

## E4 — KOS 웹 사진이 모달을 닫았다 다시 열어야 보인다
- 원인: 사진 탭은 모달에서 **처음** 고를 때만 GET `…/photos` + 가져오기 작업(`board_chart_parts.html:122` · `:147` · `hx-trigger="day:photos-load"`)
- 확인한 것: 모달을 닫았다 열면 KOS 에서 올린 「시술 후」 사진이 들어온다 — C23 가져오기 작동 확인(사용자)
- 고칠 것: 사진 탭을 고를 때마다 다시 읽는다(가져오기 작업 넣기 포함)

## E5 — [바로 시작] 후 KOS 집도의 = 시스템 → C32 그대로(고치지 않음)
## E6 — 시술 현황에 「방 배정」 줄 → 로컬 env 에 room_assign id 누락(코디 고침 · kos-demo.env + seed-demo · 코드 무관)
## E3 원인(코디 확인) — `services/board_charts.py:109` `_kos_now` 가 `build_adapter`(새 클라이언트 · 토큰 없음)를 쓴다 → 저장마다 sign-in. 동기화는 `emr/factory.py:93` `adapter_for`(병원별 캐시). KOS 는 IP 가 아니라 sign-in 마다 세션 → 5개 한도마다 오래된 것 해제. 고칠 것 = `adapter_for` 재사용(API 프로세스 안 캐시)
## 결정: E1 → C29 · E4 추가 → C30 · KOS 삭제 반영 → C31 · E5 → C32
