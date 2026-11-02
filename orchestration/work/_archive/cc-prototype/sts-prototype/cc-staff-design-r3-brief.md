# [frontend · 시안 r3] 직원 시안 수정 — 방 이름 현황판 기준 · 「마취용」 숨김 · 고객 메모를 ⚠ 주의 맨 위로

너는 **cc-prototype `frontend` 워커**다. 이번 판도 **claude design 시안 작업**이다(DesignSync). 코드는 쓰지 않는다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/roles/cc-prototype/frontend/role.md` (+ 같은 폴더 나머지)

r2 의 연속이다. 맥락이 없으면 `cc-staff-design-r2-brief.md` · `design-staff-r2-report.md`(같은 폴더)부터 읽어라.

## 1. SSOT — 먼저 읽을 것

- 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/10-decision/decision-002-cc-poc.md` — D-13 · D-22(갱신됨)
- 피드백: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/design-feedback-batch-1.md` — **#5 · #6 · #7** 이 이번 판
- 방 대응표: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/room-map-provisional.md`
- 고객 메모 실제 내용: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/research-patient-detail-report.md` §A-5
- 시안: claude.ai/design 프로젝트 `dda9a931-097f-4780-9301-972d5ac1fc23` — `Ceramique 직원 - 의사` · `- 코디` (그리고 방 이름이 나오면 `- 통역 모달 상태` · `- 로그인`)

**기대는 개념** — 해당 없음.

## 2. 고칠 것

1. **#5 방 이름** — 직원 시안 전체(의사 첫 화면 · 코디 목록 · 환자 상세 상단 카드 · 동선 등)에서 KOS 원값(`A_룸6` 등)을 **대응표의 현황판 이름**(관리실 ○○ · 2인관리실 01 · 수면실 0n)으로 바꾼다
2. **#6 「마취용」** — 의사 칸에 「마취용」이 들어 있으면 표시하지 않는다(동선 · 상단 카드 원장 · 일정 어디서든). 그 결과 원장이 비면 「-」 대신 줄/칸을 숨긴다
3. **#7 고객 메모** — `visitor.memo` 값이 있으면 **① ⚠ 주의 맨 위에 「고객 메모」 라벨로 원문 그대로**. 없으면 안 보인다. r2 샘플 6명 중 값 있는 고객(박서윤 「*영주권*」)에 적용하고, 10-09 에 고객 메모가 있는 다른 고객이 있으면 그 원문도 샘플로 쓸 수 있다(이름만 가짜)

그 밖은 r2 그대로 둔다.

## 3. 계약

해당 없음.

## 4. allowed_paths — 이 밖은 건드리지 마라

- claude design 의 `Ceramique 직원 - …` 4개 파일 수정. 「현황판 v3」·「의사 모바일」 및 다른 파일 수정·삭제 금지
- 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/design-staff-r3-report.md`
- 그 외 로컬 파일 생성·수정 금지. 커밋·push·PR 금지

## 5. 산출물

리포트 `design-staff-r3-report.md`: 상태 · 고친 파일 · #5/#6/#7 각각 어떻게 고쳤나 · 내가 정한 것 · 이슈

## 6. 범위 제약

- 가리는 것은 고객·동행인 이름뿐(r2 규칙 그대로). 코드 작성 · KOS 호출 금지. 브리프에 없는 변경 금지

## 7. 검증

```
직원 시안 4개 파일에 `A_` 방 이름 0건 · 「마취용」 0건 · 고객 메모 있는 샘플 고객의 ① 맨 위에 「고객 메모」 · 없는 고객은 안 보임 · 고객 이름 대조 0건 · 기존 두 시안 무수정
```

## 8. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_a10169a1-7391-473c-a46f-c08315dd6775 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend(시안 r3) 완료: <한 줄>" \
  --body "고친 파일 / 요약 / 검증 결과 / 내가 정한 것 / 미결"

orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] frontend(시안 r3) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] frontend: <질문>" --enter`
