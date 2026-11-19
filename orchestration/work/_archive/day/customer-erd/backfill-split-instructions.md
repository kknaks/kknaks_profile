# backend — 백필 분리 · DEMO 고객 확인 조회 (사용자 2026-11-19 「백필 내가 한다」)

컨텍스트가 압축됐으면 이 파일만 다시 읽고 이어 한다. 원 브리프 `customer-erd-be-3-brief.md` 의 금지 규칙은 그대로다.

## 1. 확인 조회 (지금 코드로 · 먼저)

- 로컬 DEMO 스택을 다시 띄운다. 테스트 계정 · DEMO 테넌트만 쓴다. **컨테이너는 지우지 말고 남긴다.**
- 기준 정보 → 일정 → 메뉴 → 오늘 회차 → 백필(`--from 2026-08` · 어제까지) 순서로 돌린다.
- 조회할 고객: 사용자가 대화로 지정한 DEMO 고객 1명(이름은 적지 않음).
  - 시술권: 번들 · 세트 · 티켓 상태 · 회차.
  - 선불카드: 잔액 · 포인트 · 만료 · 이력 · 공유 고객.
  - 같은 고객의 KOS `get-ticket-bundles` · `get-prepaid-card-summaries` 와 건수를 대조한다.
- **이름 · 값은 파일 · 리포트 · 커밋에 쓰지 않는다**(공개 레포). 아래 터미널 보고로만 알린다.
- 남겨 둔 컨테이너 이름 · 포트를 함께 알린다. 끝나면 KOS 세션을 해제한다.

```bash
orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --text "[조회 완료] <요약>" --enter
```

## 2. 백필을 PR 에서 뺀다

1. 빼기 전에 백필 관련 변경 전부를 `git diff` 로 아래 경로에 저장한다. 비밀값 · 이름이 없는지 확인한다.
   - `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/backfill-reference.patch`
2. 뺄 것:
   - `runtime/backfill` 진입점
   - PacedTransport · KosPacer
   - 진행 위치
   - 백필 테스트
   - 0010 의 `visit(hospital_id, reserved_start_at)` 인덱스
   - `review-code-5-report.md` 끝 「PR 에서 함께 빼야 할 백필 관련 조각」 목록
3. 남길 것:
   - 검수 4 WARN-A · B · D
   - 빈 본문 수정(2단계 오늘 회차 · 시술권 · 카드 요약)
   - 그 테스트들
4. 뺀 뒤 각 1회씩 돌린다: 전체 테스트 · `check.sh --pure` · 마이그레이션 왕복. 백필 흔적이 남았는지 `grep -rn backfill backend/` 로 본다.
5. `be-3-report.md` 맨 위에 「백필은 PR 에서 뺌 — 참고 패치 경로」 한 단락을 단다.
6. 완료 보고:

```bash
orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --text "[worker_done] backend 백필 분리 완료 — <한 줄>" --enter
```
