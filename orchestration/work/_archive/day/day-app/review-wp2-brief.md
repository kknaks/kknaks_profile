
# [reviewer_doc] DAY 앱 SPEC 독립 검수

너는 **day `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

planner가 쓴 SPEC 단계 산출물만 검수한다. planner 완료 후 실행되는 태스크다. 너는 앞 대화 맥락이 없으며 원천은 아래 최종 발주 브리프다. WP·코드 작성 금지. 모든 소스는 읽기 전용이다.

## 1. 원천

- profile orchestration/work/day-app/wp-brief.md · _RESUME.md 최신 사용자 결정 · review-policy-report.md
- 같은 폴더 delivery-request.json · planner-wp-report.md
- 현재 spec 워크트리 products/day/20-spec/spec-003-mobile-app.md와 SPEC-001 변경은 리뷰된 제안. Stable main에 SPEC-003 없음.
- mediness .agents/skills/start-delivery/SKILL.md · rules/delivery-workflow.md · tools/harness/references/requests.md · delivery-request.schema.json

## 2. 목표

사용자가 요청한 WP는 GitHub Delivery Issue 1개다. 발행 전 request의 결과계약·실행계획을 독립 검수한다. 코드 구현이나 새 기능 결정 아님. 제안 초안을 Stable SPEC으로 둔갑시키면 안 된다.

## 3. 확인할 계약

risk L3, idempotency day/day-app, product day, target DAY-SPEC-003/001, exact fetched origin/main revision, main에003부재→pending. 코드 PR하나→dev·사용자지시전머지금지. 앱iOS폰아이패드·DAY기준·간호사대리수락·통역고객보기권한·푸시기존호출대상·상담사호출향후 범위. 앱/로그인D1만 이 작업의 코드범위. D2푸시서버/D3통역서버전체는 미승인 의존성, 앱더블검증과 실제연동 완료 구분. Apple서명/TestFlight·실제키·env는 사용자. 방이동/차트/seed는 옆세션. 새문구/번역/새의미 만들지않음.

## 4. 검수 방법

JSON parse·schema검증·필수 target_delta/acceptance/non_goals/review_surface/execution의 실제코드근거를 본다. 단계순서·code_surface·dependencies·verification·rollback이 구체적이고 범위를 늘리지 않는지 검수. SPEC-003의 AC와 실행검증 매핑을 대조한다. 명시적 앱코드완료/통합완료 기준이 섞이면 지적. baseline 미승격·계약사람승인을 구현승인으로 쓰면 안 된다. 새 정책결정 요구보다 기존원천을 따른다.

## 5. allowed_paths

- /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/review-wp2-report.md 한 파일만 작성. 다른 파일/JSON 읽기전용.

## 6. 검증

schema와 실제 문서 대조. PASS/WARN/FAIL, 지적은 JSON필드 또는 파일:줄+근거, 구체수정안을 쓴다. CLI apply·GitHub쓰기·승인receipt·코드·서버 조작 금지. 보고서는 최대2쪽.

## 7. 제약

WP 별도파일/새레거시WP/YAML원장 만들지 않는다. request는 CLI입력이고 생성될 GitHub Issue가 원장. 커밋·push·PR·Issue 생성 금지.

## 8. 완료

새 preamble의 id로 worker_done 보고. WP리뷰 PASS와 코드구현승인·실연동완료는 별개임을 명시.

## 이번 재검수 범위

이전 태스크 완료 뒤 새 발주다. 새 preamble id로만 보고한다. review-wp-report.md·wp-fix-brief.md·planner-wp-fix-report.md와 현재 delivery-request.json의 변경 필드만 대조한다. W-1 완료기준(머지전 PR head 더블/로컬·unsigned build vs 실물통합pending)·W-2 경로와 infra/시뮬레이터 담당·W-3 fail-closed 롤백이 해소됐는지 확인. 나머지 기능범위·risk·target·version·baseline이 유지됐는지 본다. 이미 검증한 광범위 원천을 다시 읽지 않아도 된다. report는 review-wp2-report.md 1쪽 이내로.

중요: skill/CLI 공식 흐름은 --apply로 최초 승인대기 이슈를 만든 뒤 코드구현 전에 사람 승인한다. “승인 전 이슈 생성 금지”로 잘못 게이트를 추가하지 않는다. 사용자 현재 지시는 이슈 생성이다. worker는 GitHub쓰기 없이 독립리뷰만. CLI plan은 코디가 다시 확인한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_781a6b8f-68da-447e-acb9-c2261321c190 --from term_bfb1afc9-97a0-4d5b-bcab-aa5b6b982f00 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_781a6b8f-68da-447e-acb9-c2261321c190 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
