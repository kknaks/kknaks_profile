# [backend] be-swagger-2 — `Idempotency-Key` 재시도 응답 = 처음 응답 그대로

맥락: `be-swagger-1-report.md` ④ 「코드를 고쳐야 맞을 수 있는 곳」. 워크트리 · 규칙 · 완료 보고는 be-swagger-1 그대로.

## 코디 결정 (11-27)

SPEC 대로 간다 — 같은 키 + 같은 본문 재시도는 **처음 응답(`requestId` · `version` · `kind` · `status`) 그대로**. 처음 E2 `cancel` 이 `canceled` 였으면 재시도도 `canceled`.

- 방법은 네가 고른다(처음 상태 저장 · 또는 그 버전에서 결정적으로 다시 계산). 칸을 더해야 하면 **이번 migration `20261125_0031_reservation_request` 안에서**(아직 배포 전 · 새 migration 파일 만들지 않음).
- 스웨거 E2 설명의 「`status` 는 `requested` 로 온다 · 지금 상태는 E5」 줄 → 「처음 응답 그대로」로 고친다.
- 시험: E2 `cancel` → `canceled` 경우의 재시도 시험 한 개 이상 · E1 재시도 기존 시험 그대로 통과.

## 검증 · 리포트

관련 시험 + `scripts/check.sh --pure`. 리포트 `be-swagger-2-report.md`: 고친 파일:줄 · 고른 방법과 이유 · 시험 수치. subject `backend 완료: ext 재시도 응답 처음 그대로`.
