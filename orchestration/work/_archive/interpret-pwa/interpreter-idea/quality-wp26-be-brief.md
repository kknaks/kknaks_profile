# [backend] WP26 — 시술명 바로잡기 · 시드 `.8` 틀린 꼴 (D-58 · SPEC 0.9.1 §5.12 · §4.2 · §4.2.5)

너는 WP21 ~ WP24 를 한 **interpret-pwa `backend` 워커**다. 맥락이 없으면 `wp21-be-report.md` ~ `wp24-be-report.md` 부터.
작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea`(WP23 · WP24 변경 미커밋 — 그대로 이어서)

## 1. SSOT

- WORK **WP26 행** — `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` · 이 행이 이번 일의 전부다
- SPEC **0.9.1**(코디 커밋 `b37783db`) — **§5.12 바로잡기**(걸리는 조건 · 찾기 ① ② ③ · ③ 범위(en · vi 한 → 외 제외) · 낱말 경계 · 순서(① ② 전부 먼저) · 자리 · `fixed` · `translation_before` · 못 찾음 로그) · §4.2(새 필드 `wrong` · `ko_wrong` · 검사 8) · §4.2.5 · §5.9 · §9.1 「바로잡기」 ① ~ ⑭
- DEC D-58 · 처분 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/quality-research-dispositions.md` **§11 · §12**

## 2. 틀린 꼴 첫 목록 — 코디 확인 끝

- **처분 §12 표 그대로** 시드 `.8` 에 넣는다(`version` = `2026-11-15.8`). 로컬 결과에서 따로 뽑지 마라 — 코디가 이미 뽑아 확인했다. 검사 8 에 걸리는 꼴은 그 꼴만 빼고 보고
- `ko_wrong` = 0

## 3. 할 것

1. WORK WP26 ① ~ ⑤(코드 · 시드 `.8` · 시험)
2. **연기 확인**: 6차 · 다국어 묶음에서 사전대로 안 나왔던 번역문(로컬 결과 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/reference/2026-11-12-interpreter-idea/quality-run/wp24-*-local.json` 의 captions)을 바로잡기 함수에 **그대로 넣어** 바뀌는지 표로(번호 · 언어 · term · 바뀜/안 바뀜 — 문장은 보고에 넣지 마라). Soniox 호출 없이 함수만
3. `ruff` · `pytest` 1회 · ㉒(7개 언어 연결 · 거절 0 · 줄이기 0 — `.8` 은 context 를 안 바꾸는지 확인)
4. 보고 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/wp26-be-report.md`

## 5. allowed_paths

- `back/app/service/`(바로잡기 · 기록 키 · 시드 로더 검사) · `back/seed/glossary.json` · `back/tests/` · `back/scripts/`

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
