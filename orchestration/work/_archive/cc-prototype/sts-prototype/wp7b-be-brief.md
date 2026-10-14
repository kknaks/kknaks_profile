# [backend] WORK-001 WP7b — 목데이터 시나리오 로더 · 상담 완료 이벤트 · [결제 완료] · 미결제 금액

너는 **cc-prototype `backend` 워커**다(WP7 를 한 같은 워커). 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype` — **`cc/back/` 만**.

## 1. SSOT
- **SPEC-001 0.2.1 §0-a**(새로 붙음): `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/20-spec/spec-001-cc-poc.md`
- **시나리오 형식(계약)**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/scenario-format.md`
- 흐름: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/reference/2026-10-12-cc-prototype/workflow.md` 「PoC 범위」 · 5단계(결제)
- 앞 판: `wp7-be-report.md`

## 2. 할 것
1. `seed build` → **시나리오 파일**(`data/scenario/seed.json`)을 읽어 개원 전 상태로. 캡처 직접 읽기는 없앤다(직원은 그대로 `kos-staff.json`). researcher 가 지금 시나리오 파일을 만들고 있다 — 오기 전엔 **형식대로 된 작은 샘플**을 시험 픽스처(`tests/`)로 만들어 써라
2. **상담 완료 이벤트**: 상담 단계 finish 때 `events/<scheduleId>.json` 의 `consultationDone` 적용 — 상담 기록 · 오더 메모 공개 · `tasks` 를 동선 단계로 추가(`paymentRequired=true`, 상태 planned, kosSequence 유지) · 미결제 금액
3. **`POST /api/desk/payment-complete {scheduleId}`**: `paymentDone` 적용 — 수납필요 해제 · 미결제 0 · `ticketId` 연결 · 차트 「오늘 결제」 공개. 주석 = KOS 결제 조회(공식 `getPurchaseSummariesByVisitor` · `getTicketBundlesQuery`)
4. **시술 완료 이벤트**: 시술 단계 finish 때 `taskDone[sequence].assigneeMemo` 공개
5. 응답: 방 · 고객에 `unpaidAmount` · 단계에 `paymentRequired` · 재내원 `pastSchedules` · 보유 시술권
6. README API 예시 갱신(WP8 front 가 본다)

## 3. 범위
- `cc/back/` 만 · KOS 호출 금지 · 커밋 금지 · 8600 서버 · `data/cc.db` 로 시험 금지(임시 DB)
- 끝나면 researcher 시나리오 파일이 `data/scenario/` 에 있으면 `seed build` 로 시드를 만들어 두고, 없으면 리포트에 「시나리오 대기」

## 4. 검증
```
cc/back 에서 uv run pytest · uv run ruff check . — 각 1회. KOS 호출 코드 0. 사용자 포트·프로세스 안 건드림
```
- 이번 항목만: 상담 완료 → 단계 추가 · 수납필요 · 금액 / 결제 완료 → 해제 · 0 · ticketId / 시술 완료 → 담당자 메모 / 재내원 시드 → 보유 시술권 후보
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/wp7b-be-report.md`

## 5. 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_eb0f5374-235a-4757-bb3a-1b2768c7e255 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
