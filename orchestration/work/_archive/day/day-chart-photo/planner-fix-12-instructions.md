# [planner] fix-12 — C35 시스템 토큰 공유 · C36 사진 토스트 글자

**읽을 것**
- 결정 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/reference/2026-11-24-day-picture/chart-photo-decisions.md` 의 C35 · C36

## 고칠 곳

### C35 — 시스템 토큰 공유
- 어디에 적을지: KOS 시스템 계정 세션 규칙이 있는 곳.
  - DAY-SPEC-001 §3 「KOS 동시 로그인 제한」 · 시스템 계정 절
  - 그리고/또는 DAY-SPEC-000 · 40-architecture
  - 지금 문장을 찾아서 고친다.
- 적을 내용:
  - 병원마다 Redis 토큰 1개를 API · 워커가 같이 쓴다.
  - 토큰이 만료되거나 401 이면 잠금을 잡은 한 프로세스만 다시 받는다.
  - 5기기 한도에서 같은 표시 세션을 해제하는 규칙과의 관계를 적는다.
  - DAY-SPEC-002 규칙 31 의 KOS 읽기 문장은 이 규칙을 가리킨다.

### C36 — 사진 토스트 글자
- 토스트 표에 글자 2개를 넣는다.
- OQ-88 해당분을 닫는다.
- 일부 장이 빠지면 요약 토스트 1장만 띄운다.

## 작업 자리
- 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-chart-photo-spec`(커밋 `8ab5e2d2` 위)
- 커밋하지 마라.

## 검증
- lint `--strict` → `products/day` ERROR 0

## 보고
- `planner-fix-12-report.md`
- preamble worker_done 두 채널
