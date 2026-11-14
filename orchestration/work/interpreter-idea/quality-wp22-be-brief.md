# [backend] WP22 ① — 품질 시험 「전」: 규칙 파일 만들기 · 음성 파일 만들기 (여기서 멈춤 → 코디 확인 뒤 ② 실행)

너는 WP21 을 쓴 **interpret-pwa `backend` 워커**다. 맥락이 없으면 `quality-wp21-be-brief.md` · `wp21-be-report.md`(수정 1 포함)부터.
작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea`(WP21 커밋 `37aafa9`)

## 1. SSOT

- WORK **WP22 행**: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` — ① ~ ⑦. **이번 발주는 ① · ② 만**
- SPEC §9.3 「6차」(규칙 종류 넷 · 기대 확정 발화 수 · 손님 쪽은 WP24): 같은 폴더 `20-spec/spec-001-interpret-pwa.md`(지금 planner 가 0.8.3 으로 §4.2.4 만 고치는 중 — §9.3 은 0.8.1 그대로)
- 시험 목록(로컬 전용): `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/reference/2026-11-12-interpreter-idea/test-sentences.md` — T01 ~ T33

## 2. 할 것

1. **규칙 파일** `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/reference/2026-11-12-interpreter-idea/test-rules.json`(git 제외 처리됨 · WP21 스크립트 형식 `format: 1`)
   - 33문장 전부 — 「나오면 FAIL」 칸을 규칙 넷으로만(글자 그대로 · 정규식 · 발화 수 · 없음). **애매하면 「없음」 — 억지로 옮기지 마라**
   - 문장마다 `expected_finals`(3절 T23 ~ T26 은 문장마다 다르다 — 목록의 「기대」 칸 그대로) · 찾을 쪽(원문 · 번역) · 대소문자
   - zh 계열 정규식은 간체로(WP21 수정 1 보고 미결)
   - 「기대」 칸의 시술명이 사전 보정(WP23) 결과를 따른다고 적힌 문장은 **FAIL 문구만** 규칙으로(정답 표기를 짓지 마라)
2. **음성 파일** — 33문장(+ 3절 쉼 · T29 무음) 한 번 만든다. 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/reference/2026-11-12-interpreter-idea/quality-run/audio/`(git 제외) · manifest 해시. WP24 가 같은 파일을 쓴다
3. **여기서 멈춘다** — 조합 A · B 는 **돌리지 마라.** 코디가 규칙 파일을 확인한 뒤 따로 지시한다(WORK 「규칙 파일은 코디가 확인한 뒤 조합 A 실행」)
4. 보고: 문장마다 규칙 종류 · 기대 발화 수 표(번호만 · **문장 · FAIL 문구는 보고에 넣지 마라** — 코디는 파일을 직접 연다) · 「없음」 으로 둔 번호와 이유 한 줄 · 음성 파일 수 · 총 길이. 보고서 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/wp22-be-report.md`

## 5. allowed_paths

- 위 두 로컬 경로(규칙 파일 · `quality-run/`) · 스크립트가 모자라면 `back/scripts/` · `back/tests/` 만(운영 `app/` 무수정)

## 8. 검증

```
back 에서 uv run pytest · uv run ruff check . — Phase 범위에 맞게 1회씩, 통과하면 반복하지 마라. Soniox · Procedure Hub 경로는 실물 호출 1회(키 없으면 pending). 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending 으로 보고
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
  --to term_d181fbae-29f2-43bb-9a41-6bc888ca07de --from term_1408924f-69e8-469c-b6b1-8e4fe8ed9c6b \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
