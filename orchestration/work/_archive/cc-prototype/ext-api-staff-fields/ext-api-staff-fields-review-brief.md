
# [reviewer] WP-REVIEW — ext 직원 목록 세 칸 코드 검수

너는 **cc-prototype `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-3/orchestration/roles/cc-prototype/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/ext-api-staff-fields`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

너는 앞 판 맥락이 없다 — 아래 파일만 믿어라. 같은 워크트리에 backend 워커가 있었지만 끝났다(지금 편집 없음). **read-only** — 리포트 파일 1개만 만든다.

## 1. SSOT — 먼저 읽을 것 (read-only 절대경로)

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-3/para/projects/summer-star/cc-prototype/20-spec/spec-008-product-ext-api.md` — 0.4.7 §6.17 · §6.1 「id」 · §8 · §9 T67 · T70
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-3/para/projects/summer-star/cc-prototype/30-work/work-015-ext-api-staff-fields.md` — WP-REVIEW 행 · 계약 고정점 표
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-3/para/projects/summer-star/cc-prototype/10-decision/decision-012-ext-api-charty1.md` — D-48
- 개념: 해당 없음

## 2. 배경

ext 직원 목록에 `email` · `realName` · `kosAccountId` 를 더했다(필드 추가만). 변경은 워크트리 미커밋 diff — `git diff` 로 본다(5파일 · +54 −8). backend 보고: 대상 시험 23 → 24 passed · 전체 767 passed · ruff 통과.

## 3. 볼 것 (WORK-015 WP-REVIEW 그대로)

1. SPEC 0.4.7 §6.17 · T67 · T70 ↔ 코드 · 시험
2. **필드 추가만**인가 — 기존 다섯 칸 · 행 고르기 · 차례 · 오류 code · KOS 호출 수 · 다른 ext 경로 · 직원 API · 사본 표 · 동기화 무변경
3. 세 값이 `ext_call` · 로그 · 사본에 안 남는가
4. Swagger 옛 문장이 지워졌나(`grep -rn "내지 않는다" procedure/back/app/api/ext.py` 등 전수)
5. 실명 · 이메일 · KOS id **실제 값** grep 0(가짜 값만)
6. 조용히 통과하는 자리 — 시험이 단언하지 않아 깨져도 초록인 곳. backend 가 짚은 것: `email` · `realName` 이 문자열 아닌 값으로 오면 검증 오류(500?)가 날 수 있음 — `roleName` 선례와 같은 동작인지 · SPEC 에 그 갈래가 있는지만 판정(새 계약 발명 금지)
7. 사용자가 실물(연동처 · Swagger)에서 만날 자리를 따로 모은다

검증 명령 관문 1개는 직접 돌려도 된다: (`procedure/back` 에서) `uv run pytest -q tests/test_ext_clinic.py tests/test_ext_docs.py tests/test_openapi_docs.py`. 파일 수정 금지.

## 4. 산출물

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype-3/orchestration/work/ext-api-staff-fields/review-code-r1.md` — 판정 PASS · WARN · FAIL · 각 지적에 파일:줄 + 근거(SPEC 절 · D-번호) · 고칠 방향 한 줄

## 5. allowed_paths

- (read-only — 위 리포트 파일 1개만 생성)

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_94d17da5-ee50-4f74-ade5-221f35a1ea02 --from term_4f9e8603-2a4c-442e-b8c4-d20f9fe6c741 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_94d17da5-ee50-4f74-ade5-221f35a1ea02 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_94d17da5-ee50-4f74-ade5-221f35a1ea02 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
