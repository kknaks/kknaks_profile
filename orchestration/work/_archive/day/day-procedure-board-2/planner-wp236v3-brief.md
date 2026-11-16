# [planner] Delivery #236 v3 — SPEC-002 개정 ⑮ 반영

같은 스펙 워크트리(PR #920 · 마지막 커밋 bd029f3c · 미머지). `start-delivery` 규칙. 파일 수정 · 커밋 금지 — Issue 만.

CENTURION_DAY#236 — 같은 key `day/board-plan-align-1` · contract_version +1(→ 3) · scope_delta(사유: 로컬 화면 확인 뒤 사용자 결정 2026-11-10 — `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/_RESUME.md` §2 11-10 행 · `e2e-feedback.md` F1 ~ F8).

## 결과 계약에서 바뀌는 것 (SPEC-002 ⑮ 기준)
- ① 체크박스: 준비중 → **준비중 · 호출 중(수락 전)** · 호출 줄 체크로 새로 호출 = 수락 전 원장 바꾸기(그 줄은 앞 호출에서 빠짐)
- ⑩ [재호출]: 「호출 중 줄에 늘 · 검정」 → **판 카드엔 없음 · 사이드에만 · 경과 상관없이 수락 전이면 어디서나 · 처음 대상 그대로 · 창 없음 · 글자 검정**
- ⑭ 원장 변경 글자: 「원장 교체」 → **「원장 변경」**(툴팁 · 목록 머리 · 버튼) · 바꿀 수 없을 때 토스트 「원장을 변경할 수 없습니다.」 · 원장 이름 = 평소 줄 글자 · 호버 때만 옅은 배경
- ⑥ 검색 칸 글자 「고객 · 원장 · 관리실」
- ⑯ 확인 창 = medikit ConfirmModal 경고형 · DAY 글자 크기
- **새**: 카드 순서 = 판에 처음 오른 순 · 자동으로 안 바뀜 · 그 뒤 사람(F2) · 「⋯」 [종료]와 같이 바로 · 반영 중이면 누를 때 막음(F7) · 동작하면 누른 카드만 바뀜(version · F8)
- 테스트 데이터 시드 생년월일(F6)은 개발 도구 — 「같은 PR 의 개발 도구 · 계약 범위 밖」 줄에
- Acceptance 를 위 변경에 맞게 · Execution 은 코드 레포 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2`(커밋 a1c90b9d 위 + 미커밋 F1 · F5 · F6 디자인/시드 변경 있음) 기준 backend/frontend phase
- baseline pending. 계약이 바뀌므로 `delivery-plan:review` 에서 **멈춘다**(승인 대행 금지)

## 완료 보고
version · plan_digest · 라벨 · 바뀐 Target Delta/Acceptance 요약. 코디 핸들 `term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd`(worker_done + terminal send).
