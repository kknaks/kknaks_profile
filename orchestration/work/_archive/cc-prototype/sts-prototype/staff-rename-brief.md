# [researcher] 배포용 데이터 — 직원 이름 · 이메일 가짜로

너는 **cc-prototype `researcher` 워커**. 역할 문서 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/roles/cc-prototype/researcher/role.md`.
근거: **DEC-003 D-04** `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/10-decision/decision-003-cc-deploy.md`

## 할 것
1. `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype/cc/back/data/kos-staff.json`(KOS getAccounts 원본 88명) → 모든 직원 **이름 · 이메일만 가짜로**(같은 사람 = 어디서나 같은 가짜 이름, 한국 이름 꼴. 이메일은 `staffNN@example.invalid` 꼴). id · roleTags · activate 는 그대로. 원본은 `kos-staff.orig.json` 으로 옆에 남긴다(gitignore 폴더)
2. `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype/cc/back/data/scenario/seed.json` · `events/*.json` 안에 **그 직원 이름(88명 실명)이 나오는 곳**을 같은 가짜 이름으로(필드 값 · 메모 본문 모두). 원본은 `scenario.orig/` 로 복사해 둔다
3. **그 밖의 글은 건드리지 마라** — 고객 이름(이미 가짜) · 메모 원문 · 「어시 지민」 같은 표기(사용자: 회사 이름) 등은 그대로. 바꾸는 건 직원 실명 · 이메일뿐
4. 대응표(실명 → 가짜)는 **리포트에 쓰지 마라**(실명이 남는다). `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype/cc/back/data/staff-name-map.json` 에만(gitignore)

## 범위 · 검증
- `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype/cc/back/data/` 안 파일만. 코드 · 커밋 금지 · KOS 호출 금지
- 검증: 바꾼 뒤 `data/` 의 JSON 전체(orig · map 제외)에서 원본 직원 실명 88명 · 원본 이메일 0건 · JSON 파싱 OK · 직원 수 · 직군 태그 그대로
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/staff-rename-report.md`(실명 없이 — 건수만)

## 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_6aefc840-e29e-4b09-b06b-144dec5b0b7a \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] researcher: <질문>" --enter`
