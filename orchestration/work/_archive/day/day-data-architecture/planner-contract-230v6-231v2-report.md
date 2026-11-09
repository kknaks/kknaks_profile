# planner-contract-230v6-231v2 결과 보고 — done (승인 안 함)

| Issue | contract | plan_digest | 라벨 |
|---|---|---|---|
| [#230 ① 백엔드](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/230) | **v6** | `sha256:38741faeb785e87a8a567f1783f52ce413063628716db35e66ffea14773ddc66` | delivery-plan:review |
| [#231 ② 화면](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/231) | **v3**(지시는 v2 — #231 은 이미 v2 였다(W2 · W3 · W7 판) · CLI 가 「+1 이어야 함」으로 v2 를 거절 · v3 으로 적용) | `sha256:99fc33af1251446c1e7411691e944a05e97784a1de07a3ca95d7154884d3a0a2` | delivery-plan:review |

같은 Issue · 같은 key · `scope-delta-recorded`. 파일 `delivery/v2-board-backend.json`(v5 사본 `.v5.json`) · `.v6.plan/apply.json` / `v2-board-screen.json`(직전 사본 `.v1b.json`) · `.v3.plan/apply.json`. (`v2-board-screen.v2.apply.json` 은 거절 응답 — 무시)

## #230 v6 바뀐 것 (SPEC-002 ⑥ · ⑦ · PR #909 6386f746)

- **TD 동작 서비스**: F5 판 조건(`procedure_waiting` · `procedure` — 귀가 대기는 「시술 완료」 탭) · F3 호출 = 대기 시술(호출 · 수락됐어도) · 유효 호출 = 가장 최근 · 앞 수락 무효 · closed_at 기준 · F4 줄 순서 · F7 `customer.nationality` 스냅샷 · F8 오더 메모만.
- **TD KOS 쓰기**: HAR 확인 6 + **cc 근거로 엶** — 귀가 대기(cancel-flow-tasks + PROCEDURE_DONE) · 시작 취소(PROCEDURE_WAITING) · 완료 취소(complete=false) · 다시 호출 재전송(OQ-09). **cc 근거 값은 데모 실물 확인 전 운영 병원 미개방(설정으로 막음)**. W6 「닫음 · 되돌림 감수」 줄은 「멈춘 로컬 outbox 행 정리」 줄로 바꿈.
- **TD 토큰(F10)**: 누른 사람 토큰 · **`external_outbox.sender_staff_id` migration**(OQ-21) · 대리 수락 = 누른 간호사 토큰 · doctorIds = 수락한 의사.
- **Acceptance**: A2(새 판정들) · A4(sender_staff_id = 누른 사람) · A5(운영 연결 닫힘 · 데모 연결 열림) · A6(sender_staff_id migration · 다른 직원 토큰 금지) · **A8 실물 = 호출 → (대리) 수락 → 첫 시작 → 종료 → 시작 취소 · 완료 취소 · 다시 호출 · [귀가 대기] 각 1회** · 새 A11(판에 귀가 대기 없음 · nationality · 줄 순서) · 새 A12(멈춘 로컬 outbox 행 정리 건수).
- **Non-Goal**: 「HAR 미확인 쓰기 열기」 → 「cc 근거 쓰기를 실물 확인 전 운영에 열기」.
- **Review Surface**: baseline 커밋 6386f746 · HAR 요청 = OQ-03 · 12 · 13 만(08 · 09 · 10 닫힘) · L3 근거에 cc 근거 값 · migration · 내부 경로 + 새 값 조합 미확인 · 대리 수락 결과 줄 바로잡음. W8(데모 원장 계정) 줄은 그대로.

## #231 v3 바뀐 것

- TD 판 · 인박스: F3 대기 줄 체크 · F4 줄 순서 · F7 고객 줄 국적(입실 안 보임) · F8 오더 메모만 · F9 끌기 손잡이 아이콘(구현됨) · **F5 귀가 대기 → 판에서 빠지고 「시술 완료」 탭** · **F1 창 위치 = 누른 버튼 바로 아래 팝오버(덮개 없음 · 바깥 클릭 · Esc · X · 폭 약 640 — 구현됨)**.
- TD day.js 에서 「귀가 대기 카드 제외」 → 팝오버 위치 · TD 셸: **E09 · E10 뺌(자리도 안 그림)** · E06 · E08 자리만.
- A1 「뺌」에 E09 · E10 · **A3 「귀가 대기 흐림 맨 뒤」 → 「판에서 빠지고 시술 완료 탭에 보임」** + 줄 순서 · 다시 호출 체크 · 국적 · A5 팝오버 위치.
- Non-Goal E09 · E10 문구 · Review Surface baseline 6386f746.

## 주의

- **F1 은 SPEC-002 에 아직 없다** — U-4 는 원천 「화면 참고」의 「모달」 그대로다. #231 Review Surface 에 올렸다(SPEC 을 F1 에 맞출지 코디 판단).
- #231 지시 번호(v2)와 실제(v3)가 다르다 — 위 표.
