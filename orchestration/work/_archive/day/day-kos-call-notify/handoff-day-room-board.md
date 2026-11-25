# 인수인계 — 새 작업 `day-room-board` (DAY · 2026-11-25)

넘긴 코디: `day-kos-call-notify`(워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술`) · 그 작업 `_RESUME.md` 「다음 작업 후보」가 원천.

## 사용자 지시 (2026-11-25 · 그대로)

- 「새코디로 코드 작업까지해」
- 「스펙 이슈 발행 까지 한번에 하고 검수 하고」
- 「이슈 발행 할때 머지 안하고 그냥 해 코드 작업 끝나면 머지 하고 할거니까」 — **스펙 PR(mediness) 은 코드 끝날 때까지 머지하지 않는다.** Delivery 는 머지 없이 발행.
- 「방이동할때 점유 이동 할때랑 충돌이 없는지도 검토가 필요해」 — 스펙 단계에서 방 옮기기(점유 이동 · 복귀하기 · hold) 와의 충돌 검토를 반드시 넣는다.

## 정해진 것 (되묻지 말 것)

### A. 방 배정(방 점유) 자동 완료 — 지금은 귀가 대기 때 「취소」
1. 고객이 **시술 대기(`procedure_waiting`)로 넘어올 때** 그 방문의 KOS 「방 배정」 작업(연결 설정의 방 배정 기타 작업 id = `is_room_assign`)을 **완료**로 쓴다. 시술 대기 진입은 주로 KOS 에서 → 동기화가 단계 변화를 보고 DAY 가 KOS 쓰기(쓰기 큐).
2. **귀가 대기 때** 아직 남은 「방 배정」도 **취소 → 완료**(`board_tasks.py` `home` 의 `CancelRoomTasksWriteData` 자리).
3. 이유(현장): KOS 카드에 「시술 진행중 + 방 배정 준비중」이 같이 떠서 불편.

### B. 시술 현황 「방별 순」 탭
1. 방 순서 = 방 목록 순(A_룸1 부터) · 끌기 없음(지금도 `ROOM_SORT` 면 grip 없음).
2. ① **빈 방** = 기존 `ui.html` `empty_state`(아이콘 `empty-inbox`) + 글자 「방이 비었어요」.
3. ② **시술 대기 이전**(접수 · 상담 대기 · 상담 진행 · 방 있음) = 지금 카드의 **머리(방 이름) · 고객 부분(이름 · 배지 · 나이 | 국적) 그대로** + 그 아래 한 줄 **`● 단계 이름 · 경과 시간`**.
   - 단계 이름 = 예약 현황 원내 현황 `policies/reservation_inhouse.py` `STAGES`(접수 · 상담 대기 · 상담 진행)
   - 점 색 = `styles/app.css` `--day-st-reception` · `--day-st-consult-wait` · `--day-st-consult`
   - 경과 시간 = **지금 단계로 바뀐 때부터**(`visit_flow_log`) · 표시 모양 = DAY 판의 기존 경과 시간 그대로
   - 오더 메모 · 시술 목록 · 아래 버튼 **없음** · 마취 칩 안 보임 · 방 옮기기 막음(기본값 — 충돌 검토에서 다르게 나오면 사용자 확인)
4. ③ **시술 대기 · 진행** = 지금 카드 그대로.
5. 「방 배정」 줄은 어디에도 안 보인다.
6. 앱(app/)도 같은 데이터 · 같은 분기(웹 · 앱 같게 — 기존 관례).
7. 다른 탭(확인 필요 · 수락 대기 · 시술 완료)은 그대로.

### 사용자 확인 대기 중 아닌 것 — 스펙에서 OQ + 기본값으로
- ② 카드가 한 방에 둘 이상(기본 = 같은 칸에 위아래 쌓기)
- 방 옮기기 · 점유 이동(hold · 복귀하기 · `ROOM_TAKEN_STEPS` · OQ-51 상담 단계 미결) 과의 충돌 — **검토 결과를 스펙에 표로**(사용자 지시)

## 진행 (사용자 지시 · 런북)

1. `scripts/new-work.sh day day-room-board --workers planner,reviewer_doc,backend,frontend,mobile,reviewer`(필요한 워커만) · origin/dev 최신 위(DAY 코드 전 dev fetch).
2. planner — SPEC-002(판 · 방별 순 · 방 배정 완료) · 필요하면 SPEC-003(앱) 개정 → reviewer_doc 검수(PASS 까지).
3. 스펙 PR 올림 · **머지 안 함** → planner Delivery 발행. 선례: 이번 작업 Delivery #283 — target SPEC 이 main 에 stable 이면 harness 가 pending 을 안 줌 → **baseline = origin/main ready 그대로 + 각 Issue review_surface · target_delta 첫 줄에 「계약 원천 = 스펙 PR #N 브랜치 sha · main 판은 개정 전 · 머지 뒤 같은 key · contract_version 2 재결속」**(사용자 2026-11-25 「우회해서 만들수 잇잖아」) · 승인 receipt 는 사용자.
4. 코드(be · fe · mobile) → reviewer(code) 검수 — **작은 지적도 전부 고친다**(사용자 2026-11-25).
5. 로컬 스택 + KOS DEMO 실물(방 배정 완료 · 방별 순 ①②③) → dev PR · 배포. prod 는 사용자 지시 때.

## 참고 — 오늘 prod 상태

- prod = `de0d0dab`(KOS 호출 알림 #285 + 메뉴 막음 #286) · DB 0028.
- 명동점 KOS 시스템 계정 직무 = 「시스템」(의사 태그) — 바로 시작 KOS 집도의 실패 원인 해결(16:02 DAY 반영).
- 로컬: `day-kos-call-notify` 코드 워크트리 스택이 11140 에 떠 있다 — 새 작업은 다른 포트 · 그 스택 건드리지 말 것.
