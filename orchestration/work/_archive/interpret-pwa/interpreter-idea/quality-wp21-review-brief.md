# [reviewer] WP21 코드 검수 — v6 · context 문안 · 빈 원문 막기 · 품질 시험 스크립트 (D-43 · D-45 · D-48 · D-49 · SPEC 0.8.1)

너는 **interpret-pwa `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/roles/interpret-pwa/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea`
base 브랜치: `origin/main`(`e0fbda8`) → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

앞 맥락이 없다. **read-only** — 레포 파일 수정 금지 · 산출은 리포트 1개. backend 는 끝났다(병렬 작업 없음).

## 1. SSOT

- SPEC `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` **0.8.1**(코디 커밋 `b0892cbb` — 지금 워크트리 파일은 planner 가 0.8.2 로 고치는 중일 수 있다. **`git -C /Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토 show b0892cbb:para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` 로 0.8.1 을 보라**) — §4.5 · §4.6 · §5.10 · §5.11 · §9.1 · §9.3 「6차」(조합을 바꾸는 길 · 규칙 종류 · 결과)
- WORK WP21 행(같은 커밋의 `30-work/work-001-interpret-pwa.md`)
- DEC D-43 · D-45 · D-47 · D-48 · D-49
- backend 보고: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/wp21-be-report.md`

## 2. 무엇을 보나 (`git -C /Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea diff` + 새 파일 3개)

1. **운영 기본값이 곧 고친 동작인가** — 인자를 안 주면 v6 · 문안 포함 · 막기 켬. 조합(A · B)을 바꾸는 길이 선택 인자뿐이고 env · `config.py` · WS `start` · API 경로로는 못 바꾸나. `stt_config` 가 모델 이름 말고 0.7.0 과 같나
2. **§4.5 문안** S1 ~ S4 가 SPEC 0.8.1 코드블록과 글자 그대로 · `to_soniox` 키 순서 · 줄이기 대상 아님 · `forward_only` · `describe` · 일반 낱말 짝 0
3. **§5.11 빈 원문 막기** — 판정 함수(글자 L · 숫자 N 0) 경계(문장부호 · 공백 · 이모지 · 전각 · 한자/가나는 글자로 보나) · `final:false` · 이미 나간 id · TTS 큐 · 기록(줄 없음 · `utterances` 안 셈) · 로그에 문장 0 · WS 모양 · front 무변경 전제가 맞나(front 가 빈 `final:true` 를 어떻게 그리나 — `front/lib` 읽기만)
4. **조용히 통과하는 자리** — 시험이 기대값을 코드에서 다시 계산해 늘 맞는 식 · 막기가 `final:true` 만 보고 `final:false` 를 놓치는 식 · v6 첫 빈 `tokens` 메시지(보고 이슈 5)가 확인 로직을 우연히 통과하는 식
5. **품질 시험 스크립트** — 레포에 목록 문장 0(스크립트 · 시험 · 기본 경로) · 레포용 결과 쓰기 전 문장 대조가 실제로 막나 · 음성 · 로컬 결과가 레포 안이면 거절 · 키가 출력 · 로그에 안 나가나 · 규칙 4종 판정이 SPEC §9.3 과 같나 · 보고 이슈 1 ~ 4(규칙 파일 형식 · 쉼 길이 · 지연 정의 · drop_reverse 표기)가 SPEC 과 어긋나지 않나
6. allowed_paths(`back/`, 시드 읽기만) 밖 변경 0 · `GENERAL` · `TRIM_ORDER` · `CONTEXT_MAX_CHARS` 무변경
7. 관문 명령을 직접 1회: `cd back && uv run ruff check . && uv run pytest -q`
8. 배포(WP25) 때 운영에서 볼 자리 — 「사용자가 실물에서 만날 자리」 한두 줄

## 3. 산출

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/review-wp21-code-report.md` — 판정 **PASS / WARN / FAIL** · 지적마다 `파일:줄` + 근거(SPEC 절 · D-번호)

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d181fbae-29f2-43bb-9a41-6bc888ca07de --from term_023c5b4c-6d18-4fb0-a27b-ec8fa0acf608 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
