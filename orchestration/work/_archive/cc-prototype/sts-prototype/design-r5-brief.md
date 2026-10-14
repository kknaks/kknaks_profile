# [frontend · 시안 r5] E2E 2차 — 방 패널 2열 · 셀렉터 배정 · 예약 카드/상세 · 방문 카드 · 문구 정리

너는 **cc-prototype `frontend` 워커**(시안 담당). claude design 작업(DesignSync). 코드 금지.

## SSOT
- **SPEC-001 0.3.0 §0-b**(이번 판의 계약): `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/20-spec/spec-001-cc-poc.md`
- 피드백 원문 · 캡처 설명: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/e2e-feedback-batch-2.md` #1~#26
- 흐름 · 원칙: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/reference/2026-10-12-cc-prototype/workflow.md` — 「동선이 메인 데이터」 「메모 원칙」
- 앞 판: `design-r4-report.md` · `design-r4b-report.md`

## 그릴 것 — SPEC §0-b 7~12 전부
- `현황판 v5`(v4 복제 — v4 는 수정 금지): 방 패널 2열(왼쪽 동선 · 작업 / 오른쪽 메모: 오늘 · 히스토리 방문 카드) · 단계 줄 셀렉터 `[미배정 ▾]`(열린 상태 예시 1장 — 지정 직원 맨 위 「지정」 표시 · 각자 지금 일) · 오늘 시술 후보 칩(묶음 n/m) · 귀가 확인 모달(남은 단계 「진행 안 함」 목록) · 예약 탭 카드 한 줄 + 접수 전/귀가/노쇼 · **예약 상세**(카드 클릭) · 범례 「확인 필요」 · 메모 원문 + 위험 단어 · 직원 이름 강조 · 설명 문구 · 「KOS 순번」 없음
- 직원 화면(배정형 · 순회형): 로그아웃 · 「상담 내용」 원문 전체 · 방문 카드(오늘 / 지난) · 상담사 화면엔 오늘 오더 없음 · 동선에 담당자 메모 없음
- 샘플: 시나리오 고객(`/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype/cc/back/data/scenario/` — 이름 이미 가짜) — S2(재내원 · 지난 방문 · 보유 시술권 7/10) · S6 · S1 을 예시로

## 범위
- claude design 에 새 파일(`현황판 v5`) · 직원 파일 수정. v3 · v4 · 의사 모바일 원본 무수정. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/design-r5-report.md`. 코드 · 커밋 · KOS 금지

## 검증
SPEC §0-b 7~12 항목별 반영 표 · 설명 문구 · 「KOS 순번」 0 · 실제 고객 이름 0 · v3/v4 무수정

## 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_0b06bf42-18f0-4292-8d50-500c8bcc2cb6 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend(시안 r5) 완료: <한 줄>" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] frontend(시안 r5) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] frontend(시안 r5): <질문>" --enter`
