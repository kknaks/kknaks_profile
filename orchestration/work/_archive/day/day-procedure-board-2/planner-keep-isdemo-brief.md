# [planner] 범위 변경 — crm_connection.is_demo 칸은 지우지 않는다 (스펙 #920 + Delivery #234 v2)

사용자 지시(2026-11-09): 「is demo 컬럼은 지우지 말아」. 동작 분기 제거(데모/운영 KOS 쓰기 · dev 거르기)는 그대로 두고, **칸은 「데모 병원 표시」 데이터로 남긴다 — 어떤 동작도 그 값으로 가르지 않는다.**

같은 스펙 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec`(브랜치 `kknaksss/day-procedure-board-2-spec` · PR #920).

## 1. 스펙
- SPEC-000: 「is_demo 칸 지움」 → 「칸 유지 · 데모 병원 표시(시드가 true) · 동작 분기에 쓰지 않는다」. 칸 정의 · ERD(40-architecture/erd.md 에 있으면) · 개정 줄 · 관련 OQ 문구 정리
- 그 밖에 「is_demo 칸 삭제」를 적은 자리 전부(`grep -rn is_demo products/day`) · log.md 해당 행 문구 갱신(새 행 추가 말고 같은 날 행 수정 — 사유 한 줄)
- lint --strict products/day ERROR 0
- **커밋 · push 는 하지 마라**(코디가 한다)

## 2. Delivery #234 v2
- `start-delivery` 규칙대로 같은 idempotency key `day/demo-live-unify` · version 2 · `scope_delta`(사유: 사용자 지시 — is_demo 칸 유지)로 결과 계약 수정: Target Delta (다) 칸 삭제 제거 · A4 를 「is_demo 칸은 남고 어떤 코드도 그 값으로 동작을 가르지 않는다(git grep 으로 칸 · 모델 · 시드 · 그 테스트만)」로 · migration 관련 execution(code_surface · verification · rollback) 정리. baseline 은 pending 그대로.
- 새 plan_digest 가 나오면 `delivery-plan:review` 에서 **멈추고 보고**(승인 대행 금지 — 코디가 사용자 확인 뒤 receipt 를 다시 지시한다)

## 완료 보고
바뀐 스펙 파일 · lint · #234 version · 새 plan_digest · 라벨. 코디 핸들 `term_b915fb18-742f-4779-962c-79848020b8d5`(원 브리프 §9 두 명령).
