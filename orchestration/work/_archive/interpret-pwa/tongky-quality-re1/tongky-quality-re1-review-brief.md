# [reviewer] WP28 코드 검수 — 끊김 기본값 2000 · -0.3 (D-67)
# [reviewer] <한 줄 제목>

너는 **interpret-pwa `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/roles/interpret-pwa/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/tongky-quality-re1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)


## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` 0.9.4 §5.10 · §9.1 · `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` D-67 · `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` WP28

기대는 개념: 해당 없음.

## 2. 배경

backend 워커가 워크트리에 미커밋 변경을 남겼다(`git diff` — `back/app/service/interpret/soniox.py` · `back/scripts/quality_check.py` · `back/tests/test_quality.py`). 운영 STT 기본값을 2000 · -0.3 으로 바꾸는 작업이다.

## 3. 계약

해당 없음.

## 4. 볼 것

- 기본 `stt_config` 가 SPEC 0.9.4 §5.10 과 같은가(두 값 · `endpoint_latency_adjustment_level` 안 보냄 · 다른 키 그대로)
- 끊김 값을 쓰는 곳 전부(`git grep -n -E "MAX_ENDPOINT_DELAY_MS|max_endpoint_delay_ms|endpoint_sensitivity|ENDPOINT_KEYS"`)가 일관한가 — 「조용히 통과하는 자리」: 재연결(§4.6.1 「정방향 기본만」) 설정이 새 키를 그대로 갖는가 · 품질 시험 덮어쓰기 길
- 시험이 새 기본값을 실제로 고정하는가 · `uv run pytest` · `uv run ruff check .` 1회씩(back)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정 금지. 산출물은 브리프가 지정한 리뷰 리포트 파일 1개뿐)`

## 6. 할 것

리뷰 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/review-wp28-code-report.md` — 판정 PASS · WARN · FAIL · 지적마다 파일:줄 + 근거.

## 7. 하지 말 것

- 레포 파일 수정 · 커밋 금지. Soniox 실물 호출은 코디가 따로 한다(하지 마라).

## 8. 검증

```
각 지적에 파일:줄 + 근거(SPEC 절 · DEC D-번호). 판정 FAIL · WARN · PASS. 「조용히 통과하는 자리」를 따로 본다
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
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
