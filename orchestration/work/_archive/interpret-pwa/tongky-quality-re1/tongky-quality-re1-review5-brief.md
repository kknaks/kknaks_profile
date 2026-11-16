# [reviewer] WP33 코드 검수 — context 고유명사 74 · 정방향 + 역방향만 (D-71)

너는 **interpret-pwa `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/roles/interpret-pwa/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/tongky-quality-re1` · 브랜치 `kknaksss/tongky-quality-re1-dict` · 커밋 `c52ec83`(`git diff origin/main...HEAD`)

## 1. SSOT — 먼저 읽을 것

- 발주서(사용자 결정 그대로 · 대조 기준): `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/tongky-quality-re1-be5-brief.md` §2
- DEC D-71: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md`
- 대상 74 id: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/dict-classification.md` `## ① 고유명사 — 74개`
- backend 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/wp33-context-report.md`
- SPEC §4.2 · §4.5 · §4.6(아직 옛 규칙 — 문서는 뒤에 고친다. 이번 대조는 발주서 §2 가 기준. SPEC 과 다른 자리는 「문서 고칠 자리」 목록으로만)

기대는 개념: 해당 없음.

## 4. 볼 것

1. 발주서 §2 표가 코드에 그대로인가: general · text 그대로 · terms = proper ko 대표명만 · translation_terms = 정방향 + 역방향만 · 별칭 짝 0 · 일곱 언어 같은 규칙.
2. 시드 `.11`: `proper: true` 가 74 id 와 정확히 같은가(더 · 덜 0) · 이름 · 별칭 · wrong · 순서가 `.10` 과 같은가(`git diff` 로).
3. **바로잡기가 그대로 170개 · 별칭 · wrong 을 쓰는가** — `correct_terms` 쪽이 `build_context` 변경에 기대는 자리가 없는지(쓰는 곳 전부 grep).
4. 「조용히 통과하는 자리」: `invalid_request` 정방향만 재연결(`forward_only` · `is_forward_only`) · 줄이기 순서 · 역방향 중복 · yue · zh-Hant t2s · 로그 줄 · 품질 시험 스크립트 인자(`with_text` · `drop_reverse`) · 시드 로더 기동 검사.
5. `uv run pytest -q` · `uv run ruff check .` 1회.

## 4-1. 하지 말 것

- 파일 수정 · 커밋 금지. Soniox 실물 호출 하지 마라(backend 가 했다).

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정 금지. 산출물은 브리프가 지정한 리뷰 리포트 파일 1개뿐)`

## 6. 할 것

리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/review-wp33-code-report.md` — PASS · WARN · FAIL · 지적마다 파일:줄 + 근거.

## 8. 검증

```
각 지적에 파일:줄 + 근거(발주서 §2 · DEC D-71). 판정 FAIL · WARN · PASS. 「조용히 통과하는 자리」를 따로 본다
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
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
