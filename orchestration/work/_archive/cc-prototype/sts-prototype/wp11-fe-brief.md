# [frontend] WORK-001 WP11 — SPEC 0.3.0 §0-b 화면(시안 r5)

너는 **cc-prototype `frontend` 워커**(WP3 · WP4 · WP8 을 한 워커). 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype` — **`cc/front/` 만**. back 은 끝났다(읽기 · 실행만).

## SSOT
- **시안 r5(정본)** — claude design `dda9a931-…` 의 `Ceramique 현황판 v5` · `직원 - …`(DesignSync 로 받아라). 설명 `design-r5-report.md`(이 폴더)
- **SPEC-001 0.3.0 §0-b**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/20-spec/spec-001-cc-poc.md` — 7~12 가 화면
- **API**: `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype/cc/back/README.md`(WP10 갱신) · 리포트 `wp10-be-report.md`
- 피드백 원문: `e2e-feedback-batch-2.md` #1~#26 · 원칙: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/reference/2026-10-12-cc-prototype/workflow.md`
- 앞 판: `wp8-fe-report.md`

## 할 것 — §0-b 7~12 전부(시안 r5 대로)
방 패널 2열 · 단계 셀렉터 `[미배정 ▾]`(지정 맨 위 · 배정/해제 버튼 없음) · 아래로 펼치는 목록 없음 · 오늘 시술 후보 칩(묶음 n/m, 1회 차감) · 귀가 확인 모달 · 예약 카드 한 줄 + 접수 전/귀가/노쇼 · 예약 상세(카드 클릭, [접수] · [노쇼]) · 지연 표시 없음 · 「확인 필요」 · 메모 원문 + 위험 단어 · 직원 이름 강조 · 방문 카드(오늘 / 지난) · 「상담 내용」 원문 · 상담사 화면 오늘 오더 없음 · 동선에 담당자 메모 없음 · 로그아웃 · 설명 문구 · 「KOS 순번」 등 내부 용어 0 · 접수 모달 후보 묶음 n/m

## 범위 · 검증
- `cc/front/` 만 · 커밋 · KOS 금지 · 임시 포트(back 은 별도 DB) — 3600 · 8600 · `data/cc.db` · `seed.json` 금지
```
cc/front 에서 npx tsc --noEmit · npm run lint · npm run build — 각 1회
```
- 이번 항목만: 실제 back(임시)으로 headless 크롬 — S2(예약 상세 · 지난 방문 카드 · 보유 시술권 7/10 → 1회 접수) · S1(상담 종료 → 후보만 · 결제 완료 → 후보 칩으로 시술 추가 · 셀렉터 배정 · 귀가 모달) · S6(원장 상담 중복 없음 · 중간 귀가) · 노쇼 1건 캡처 · 콘솔 오류 0 · 화면 문자열에 「KOS 순번」 · 「고르면」 · 「↑↓ 로」 0(grep)
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/wp11-fe-report.md`

## 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_b8c9cf80-7ebb-4df8-8d9c-db451c88c768 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] frontend: <질문>" --enter`
