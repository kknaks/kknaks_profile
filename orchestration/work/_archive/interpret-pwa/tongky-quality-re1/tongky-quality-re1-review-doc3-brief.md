# [reviewer_doc] 마감 문서 검수 — DEC D-71 · SPEC 0.9.6 · WORK WP30 ~ 34 · 회고 · 개념

너는 **interpret-pwa `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/roles/interpret-pwa/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선` (`git diff` · `git status` — 미커밋 변경이 검수 대상)

## 1. 대조 기준

- planner 발주서 `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/tongky-quality-re1-spec6-brief.md` §1(사실 · 사용자 결정) · §2(할 일)
- 코드 리뷰의 「문서 고칠 자리」 D-1 ~ D-10: `…/tongky-quality-re1/review-wp33-code-report.md`
- §9.1 r2 몫: `…/tongky-quality-re1/review-wp30-31-code-r2-report.md`
- 실측: `wp33-context-report.md` · `research-price-update-report.md`
- 코드(실제 동작 확인용 · 읽기만): `/Users/kknaks/orca/workspaces/interpret-pwa/tongky-quality-re1/back/app/service/glossary.py` · `back/seed/glossary.json`(`.11`)

## 2. 검수 대상

- `para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` D-67 ~ D-71 · OQ-035 · OQ-040 · OQ-041
- `20-spec/spec-001-interpret-pwa.md` 0.9.6 변경(§4.2 · §4.5 · §4.6 · §9.1 · §9.5 · §9.6 · §10 · 머리 · 부록) · `20-spec/README.md`
- `30-work/work-001-interpret-pwa.md` WP28 ~ WP34 · `30-work/README.md`
- `00-baseline/baseline-001-interpret-pwa.md` 입력 6 · 7
- 회고 `orchestration/work/tongky-quality-re1/SUMMARY.md` · 개념 `para/areas/concept/ai/consecutive-interpreter-turn-taking.md`(새) · 보강 5(`front/half-duplex-echo-suppression.md` · `ai/context-catalog-injection.md` · `ai/translation-glossary-normalization.md` · `ai/golden-set-regression.md` · `back/empirical-limit-probing.md`) · `para/areas/area.md` 맵 536

기대는 개념: 위 6개 — 회고 §2 항목마다 `[[개념]]` 이 있고, 개념 노트의 `up:` · 출처에 `2026-11-16-tongky-quality-re1` 이 있는가.

## 3. 볼 것

1. SPEC 0.9.6 이 **배포된 코드와 같은가**(시드 `proper` · `build_context` 재료 · terms · translation_terms · 줄이기 순서 · 역방향 중복 · `None` 조건) — 문장 대 코드 대조
2. 리뷰 D-1 ~ D-10 · §9.1 네 자리가 빠짐없이 들어갔나(planner 보고의 줄 번호가 맞나)
3. DEC D-71 이 사용자 결정(애매 35 뺌 · 정방향 + 역방향만 · terms 74 · 바로잡기 170)을 그대로 적었나 · 새 결정을 지어 넣지 않았나 · OQ-040 / 041 은 처분 없이 열려 있나
4. 수치가 원천 리포트와 같은가(합성 · 실기기 · 요금)
5. **PUBLIC 레포** — 운영 통역 기록 문장 · 키 · 사람 이름 0(grep). 회고 · 개념도
6. 버전 · 머리 요약 · README 버전 줄 · 표 열 수 · 깨진 링크 · `python3 orchestration/scripts/sync-work-links.py --check`

## 4-1. 하지 말 것

- 파일 수정 · 커밋 금지. Soniox 호출 금지.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정 금지. 산출물은 브리프가 지정한 리뷰 리포트 파일 1개뿐)`

## 6. 할 것

리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/review-close-doc-report.md` — PASS · WARN · FAIL · 지적마다 파일:줄 + 근거.

## 8. 검증

```
각 지적에 파일:줄 + 근거. 판정 FAIL · WARN · PASS
```

- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_0cdc063d-4b42-4e5f-bc41-65528f81e60f --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
