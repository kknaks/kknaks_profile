# [조사 · 읽기 전용] 원내 현황 카드 금액 — 이번 방문의 수납총액 · 결제총액 · 미수총액

너는 맥락이 없다고 생각하고 이 파일만 따른다. **코드 · 문서 · DB 를 고치지 않는다.** 결과는 리포트 하나.

## 배경
DAY 예약 현황 오른쪽 패널에 「원내 현황」 탭 카드를 만든다(다음 피처). 카드에 **이번 방문(visit) 하나** 기준 금액 세 개가 필요하다(사용자 용어 그대로):
- **수납총액** — 이번 방문에서 받아야 할 돈 합계(시안 「총 합계」)
- **결제총액** — 이번 방문에서 이미 낸 돈(시안 「수납 완료」)
- **미수총액** — 남은 돈(시안 「수납 필요」 금액)
시안: `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/20261113_예약현황_시연 (1).html` L1777 `stageCard` · L2160 수납 정보(가짜 값 `r.pay=[총액, 낸 돈]`).
상담 실장 표시(「상담 ○○ 실장」)도 같은 카드라 원천을 같이 본다.

## 물음 (각각 「그대로 / 가공 / 없음」으로 답하고 근거 file:line)
1. KOS 원천에 이 세 값(또는 계산 재료)이 있나? 어떤 API · 필드인가. 방문(접수 · 예약 그룹) 하나에 묶이나, 고객 단위 · 구매 단위인가.
   - 참고: `/Users/kknaks/git/ax-clinic-project`(KOS 문서) · DAY KOS 어댑터 `backend/day/emr/kos/`
2. DAY DB 에 지금 저장되나? 테이블 · 칼럼(구매 · 시술권 · 카드 · 결제 · `visit_task.payment_required` 등). 방문과 어떻게 이어지나(키). 동기화 코드 `services/emr_sale_sync.py` · `emr_sync.py` · `emr/sync_*.py` · `models/`.
3. 「이번 방문」 경계: 같은 고객의 다른 날 구매 · 선결제 시술권 · 환불 · 할인이 섞일 때 무엇을 넣고 빼야 하나 — 원천 필드로 가를 수 있는지만(추정 규칙을 지어내지 마라).
4. cc-prototype 은 어떻게 셌나: `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:<path>` (`procedure/back/app/service/*` · 원내 현황 / 수납 관련 · `ResvAside.tsx`). centurion(`/Users/kknaks/git/centurion`)에 같은 계산이 있으면 그것도.
5. 상담 실장: 방문의 상담 담당 직원을 DAY DB 어느 칸에서 읽나(`visit_task_staff` 역할 등).
6. 로컬 데모 DB 표본(읽기 전용 SELECT 만): 오늘 방문 몇 건으로 세 값을 실제 계산해 보고, 맞는지 볼 수 있는 근거(KOS 화면 값과 대조할 수 있는 형태 — 방문 id 앞 8자 · 금액만). 접속: 컨테이너 `day-local-521a3a9726-postgres-1`, DB `day`, schema `day_dev`, `psql -U "$POSTGRES_USER"`.
7. 빠진 것: 세 값 중 DB 에 없어 동기화를 더 받아야 하는 것이 있으면 무엇을 · 어느 KOS API 로.

## 금지
- 고치기 · 커밋 · push 금지. 스택(11040 · .run · docker 재시작) 건드리지 마라. INSERT/UPDATE 금지.
- 고객 이름 · 전화 · 메모 출력 금지(리포트에도). `deploy/*.env` 읽지도 출력하지도 마라. KOS 를 직접 호출하지 마라(DB · 코드 · 문서만).
- 없는 값을 다른 필드로 추정해 채우지 마라. 모르면 「없음 / 확인 못 함」.

워크트리(코드 읽기): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation`
리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/research-payment-1-report.md` — 맨 위에 물음 1 ~ 7 답 한 줄씩 표, 아래 근거. preamble 의 worker_done.
