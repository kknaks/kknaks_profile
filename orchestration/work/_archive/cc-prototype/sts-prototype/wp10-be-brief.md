# [backend] WORK-001 WP10 — SPEC 0.3.0 §0-b 데이터 · 동작

너는 **cc-prototype `backend` 워커**. 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype` — **`cc/back/` 만**(시안 작업 중 · front 는 다음 판).

## SSOT
- **SPEC-001 0.3.0 §0-b**(원칙 + 1~6): `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/20-spec/spec-001-cc-poc.md`
- 피드백 원문: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/e2e-feedback-batch-2.md`
- 흐름: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/reference/2026-10-12-cc-prototype/workflow.md`
- 앞 판: `wp7-be-report.md` · `wp7b-be-report.md`

## 할 것 — §0-b 원칙 + 1~6
1. **메모 원문화**: 잘라 읽기 · 뽑기 제거(`memo_parse` 의 양식 의존 부분 — ⚠ 뽑기 · `------` 나누기 · OUT TIME · 빈 양식 줄 · 타 병원 이력 · 예약 메모 칸). 원문 그대로 내보낸다
2. **위험 단어 설정**(`CC_RISK_WORDS` 또는 설정 파일, 기본 목록 §0-b) · 응답에 `riskWords` · `mentionedStaffIds`(오늘 근무 직원 이름 문자열 일치)
3. **방문 카드 `visits[]`**(오늘 + 지난, 공개 시점 · 최근 위)
4. **상담 종료 이벤트 → 후보만**(동선에 안 붙임) · 원장 상담 후보 중복 제거 · 미결제 · [결제 완료] 유지(결제 완료 뒤 후보의 시술권 연결)
5. **후보 묶음 단위** `{bundleId, name, left, total, source}` · `add-procedures` 가 묶음 id 를 받아 다음 AVAILABLE 1장을 단계에 연결(1회 차감) · 접수 모달 후보도 같은 모양
6. **노쇼** `POST /api/desk/no-show` · 예약 목록 응답에 st 그대로(front 가 접수 전/귀가/노쇼로 거름)
7. 응답에서 `cautions` · 메모 유래 `outTime` · 동선 단계 담당자 메모 제거(담당자 메모는 visits 에만)
8. KOS 주석 유지 · 새 조작(no-show)에도 · README API 예시 갱신(front WP11 이 본다)

## 범위 · 검증
- `cc/back/` 만 · 커밋 · KOS 호출 금지 · 8600 · `data/cc.db` 로 시험 금지(임시 DB) · 끝나면 `seed build` 로 seed.json 갱신
```
cc/back 에서 uv run pytest · uv run ruff check . — 각 1회. KOS 호출 코드 0
```
- 이번 항목만: S2 visits(지난 카드 공개 · 오늘 잠금) · 상담 종료 → 후보만 · 묶음 n/m → 1회 차감 · 원장 상담 중복 없음 · 노쇼 · 원문 그대로(양식 문자열 가공 0 — grep) · 실명 0
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/wp10-be-report.md`

## 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_eb0f5374-235a-4757-bb3a-1b2768c7e255 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] backend: <질문>" --enter`
