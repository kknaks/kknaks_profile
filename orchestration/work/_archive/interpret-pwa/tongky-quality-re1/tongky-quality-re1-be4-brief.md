# [backend] WP30 수정 — 코드 검수 FAIL-1 · WARN-1 ~ 4
# [backend] WP28 — 끊김 기본값 2000 · -0.3 (D-67)

너는 **interpret-pwa `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/roles/interpret-pwa/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/tongky-quality-re1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

front/ 는 끝났다 — 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/review-wp30-31-code-report.md` ← 고칠 목록(파일:줄 · 재현)
- SPEC 0.9.5 §5.13 D · E · G · §9.1(앞 발주 그대로)

## 2. 처분(코디) — 이대로

- **FAIL-1**: 끼어들기 · `playback_stopped` 로 멈추면 재생 어림(`play_end` 등)을 멈춘 시점으로 되돌려, 다음 통키 차례의 재생 시작 · 되울림 구간 · agent text · 차례 끝이 밀리지 않게. §9.1 에 「멈춘 뒤 다음 차례의 재생 시작 · 되울림 구간 시각」 시험 한 줄(리포트 재현 조건: 4 s 번역을 0.5 s 에서 끊음 → 다음 차례 밀림 0).
- **WARN-1**: 실제 1초를 기다리는 기존 세션 시험은 주입 시계 · 상수 덮어쓰기로 바꿀 수 있으면 바꾼다(§9.1 「가짜 시계」). 크게 번지면 그대로 두고 보고.
- **WARN-2**: `audio_start` 를 보내는 순간 끼어들기가 겹쳐도 `audio_stop` id = 지금 재생 중인(방금 시작한) 발화 · 새 스트림에도 진행 중이면 `cancel`. 시험 한 줄.
- **WARN-3**: `playback_stopped` 의 `id` 가 문자열이 아니면 무시(세션 유지 · 로그 1줄). 시험 한 줄.
- **WARN-4**: 되울림 로그를 차례마다 정확히 — 마지막 차례 몫도 세션 끝에 한 줄.

## 3. 계약

WS 메시지 이름 · 모양 그대로.

## 4. 먼저 읽을 핵심 파일

`back/app/service/interpret/turn.py:300-330` · `session.py:510-540`(리포트 줄).

## 5. allowed_paths — 이 밖은 건드리지 마라

- `back/`
- `docker-compose.yml · .env.example (레포 루트)`

## 6. 구현 단계

위 처분만. 실물 Soniox 는 다시 안 해도 된다(재생 어림은 back 내부). pytest · ruff 1회.

## 7. 범위 제약 — 하지 말 것

- `front/` · 커밋 금지. 처분 밖 변경 금지.

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
  --to term_0cdc063d-4b42-4e5f-bc41-65528f81e60f --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
