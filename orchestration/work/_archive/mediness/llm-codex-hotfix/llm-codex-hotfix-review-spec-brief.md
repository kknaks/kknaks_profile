# [reviewer_spec] 서버 LLM codex 핫픽스 — SPEC 4건 + WP-133 검수 (read-only)

너는 **mediness `reviewer_spec` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스/orchestration/roles/mediness/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/llm-codex-hotfix-spec`
base 브랜치: `origin/mediness` → 최종 PR 대상 `mediness` (PR 은 코디네이터가 올린다)

⚠ 이 워크트리에 planner 의 **미커밋 산출물**이 있다. 검수 대상이다 — **고치지 마라.** 너는 앞 맥락이 없다.

## 1. SSOT — 먼저 읽을 것

- 작업 브리프(planner 가 받은 지시 — 사용자 결정 D1~D4·계약 요구가 여기 있다): `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스/orchestration/work/llm-codex-hotfix/llm-codex-hotfix-spec-brief.md`
- 운영 실측 리포트(사실의 원천): `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스/orchestration/work/llm-codex-hotfix/survey-prod-claude-usage.md`
- 레포 규칙: `AGENTS.md` · `rules/document-pipeline.md`
- 코드(운영 = mediness-app `origin/main`, read-only): `git -C /Users/kknaks/git/harness_works/mediness-app show origin/main:<경로>`

## 2. 배경 / 무엇을 검수하나

서버 claude 호출이 11-10 부터 조직 차단으로 실패 중이라, B(결정 게이트)·C(데일리 브리프)·D(주간보고)를 codex 로 바꾸는 main 핫픽스를 준비한다. planner 가 SPEC-111/070/130/116 을 고치고 WP-133 을 새로 썼다. 다음 단계는 코드 워커가 **WP-133 만 보고** 구현하는 것이다.

## 3. 계약

해당 없음.

## 4. 검수 대상 (`git status` / `git diff` 로 범위 산정)

- `products/mediness/30-work/work-133-server-llm-codex-hotfix.md` (신규)
- `products/mediness/20-spec/spec-070-briefing.md` · `spec-111-decision-intake-slack.md` · `spec-130-weekly-report.md` · `spec-116-okknaks-v2-migration.md`
- `products/mediness/30-work.md` · `products/mediness/log.md`

## 5. allowed_paths — 이 밖은 건드리지 마라

- read-only. 산출물은 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스/orchestration/work/llm-codex-hotfix/review-spec-report.md`

## 6. 검수 항목

1. **사실 정확성** — WP-133 이 인용한 파일:줄·현 claude 제출 스펙(provider·model·provider_options·options)이 `origin/main` 코드와 **실제로 일치**하는가. 직접 `git show` 로 대조하라.
2. **선례 일치** — codex 대응표가 `meeting_v2_submission.py`·`landing_chat/submission.py` 의 실제 모양과 맞는가(키 이름·`-c` 오버라이드·MCP 주입·모델 기본값·system_prompt 처리). 선례에 없는 방식을 발명한 곳이 있으면 FAIL.
3. **전수성** — B·B′·C·D 의 claude 의존을 빠짐없이 덮었나. `git grep -nE 'provider=|"claude"|claude-|meeting_llm_batch|AgentClient\(' origin/main -- back/app` 로 이 세 경로에 닿는 claude 의존(모델명·옵션·파싱·계측)을 세고 WP 밖에 남는 것이 있는지.
4. **구현 가능성** — 코드 워커가 WP-133 만으로 구현할 수 있나(모호한 지시·서로 충돌하는 지시·Open 으로 남겨 막히는 지점). Open Issues 5건 각각이 **구현을 막는지/진행하며 실측으로 닫을 수 있는지** 판정.
5. **결정 준수** — D1~D4(범위 B·C·D, A·agent·DEPLOY §4-4 후속, main 핫픽스)를 벗어나거나 되묻는 서술이 없나.
6. **수용 기준** — 실물 codex 호출 1회씩(B·C·D)이 운영 같은 조건에서 검증 가능하게 적혔나.
7. **SPEC 정합** — SPEC 개정이 WP 와 모순 없고, 개정 노트(날짜·근거)가 있으며, 관련 없는 절을 건드리지 않았나.
8. 레포 문서 규칙(frontmatter·번호·인덱스) 위반.

## 7. 범위 제약 — 하지 말 것

- 파일 수정 금지(리포트 1개만). 테스트·코드 실행 금지(lint 만 허용).

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict 실행 → 이번 제품 범위 ERROR 0 확인 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 리뷰는 read-only — 문서를 고치지 않는다
```

리포트 형식: 판정(PASS / WARN / FAIL) · 위반 목록(파일:줄 + 근거 + 수정 제안) · Open Issues 5건 판정표 · 「사용자에게 물어야 할 것」(있으면 — 추측으로 메우지 마라).

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_4d39f44d-7335-41dc-bd4a-b274304b05d9 --from term_b9963c8b-5ebc-46cd-a18f-6897c9485cc2 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_spec 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_4d39f44d-7335-41dc-bd4a-b274304b05d9 \
  --text "[worker_done] reviewer_spec 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_4d39f44d-7335-41dc-bd4a-b274304b05d9 --text "[질문] reviewer_spec: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
