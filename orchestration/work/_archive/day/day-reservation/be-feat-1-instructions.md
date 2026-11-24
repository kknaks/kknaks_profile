# [backend] 기능 1 — 원내 현황 탭 데이터 · 금액 · 거래 매핑

너는 이 작업의 backend 다(앞 판 보고서 `be-*-report.md` · `research-payment-1-report.md` 가 이 폴더에 있다 — 먼저 읽어라). 결정 R46 ~ R53(`/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md` 끝 절) · 계약 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/contract-v2-inhouse.md` 이 정본.

할 일
1. 보기 모델 `inhouse`(계약 그대로) — queries / policies / presentation / dtos 기존 계층을 따른다. 오늘 방문만. 일반 응답 · `poll=1` 응답 둘 다.
2. 금액 R49 ~ R51 — 계산은 policies(순수 함수) · 재료는 queries. 같은 옵션 구성 여러 줄 = 1회, 같은 진료항목 2줄 = 2회(R50). VAT: `product_option.vat_amount` → 없으면 `treatment_item.taxation = taxable` 이면 10%.
3. 상담 실장 R48 — `consultation.counselor_id`(상담 시작 순 첫 줄, 시술 현황판 `queries/board.py` 와 같은 원천) → `visit.consultation_info_counselor_id`.
4. 거래 매핑 R53 — `emr/kos/mapper_sale_values.py` 등 · 필요하면 enum migration(다음 번호 0018 · dev head 뒤 · `alembic heads` 하나).
5. 시험: 금액 규칙 표 시험(R52 세 사례 — 신도윤 · 홍길사 · 선불카드 — 를 픽스처로 재현 · 결제 전 수납 건과 수납 필요 시술 겹침 · 취소 음수 · 환불 adjusted · REQUESTED/FAILED 미포함) · 대상 · 정렬 · 칩 수 · 폴링 응답. 관련 시험만(전체 check.sh 는 안 돌림).

frontend 와 같은 워크트리를 쓴다 — **템플릿 · day.js · CSS 는 frontend 몫**(건드리지 마라). 계약 밖 필드가 필요하면 짓지 말고 ask.
금지: 스택(11040 · docker · .run) 손대지 마라 · deploy/*.env 읽지 마라 · 커밋 · push 금지 · 고객 이름 · 전화 출력 금지(데모 DB 는 읽기 전용 SELECT 만).
워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation` · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/be-feat-1-report.md` · preamble 의 worker_done.
