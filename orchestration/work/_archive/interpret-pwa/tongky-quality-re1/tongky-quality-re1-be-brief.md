
# [backend] WP28 — 끊김 기본값 2000 · -0.3 (D-67)

너는 **interpret-pwa `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/roles/interpret-pwa/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/tongky-quality-re1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

이 워크트리에 다른 워커는 없다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` **0.9.4** §5.10 「끊김」 · §9.1 · 변경 이력 맨 위 ← 계약의 SoT(코디 워크트리 · read-only). **여기 없는 건 발명하지 마라.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` D-67 · `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` WP28

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 바꾸나

운영 STT 설정은 `max_endpoint_delay_ms: 1000` 만 보낸다(`soniox.py:30`). 실기기에서 손님 쪽 발화가 문장 중간에서 잘려 D-67 로 기본값을 **`max_endpoint_delay_ms` 2000 · `endpoint_sensitivity` -0.3** 으로 바꾼다. `endpoint_latency_adjustment_level` 은 계속 보내지 않는다. 품질 시험용 `endpoint_config` 덮어쓰기 길은 그대로 둔다.

## 3. 계약

해당 없음 — WS 메시지 · env · 허용 경로 · 기록 줄 모양 · front 그대로. 새 env 를 만들지 않는다(상수).

## 4. 먼저 읽을 핵심 파일

- `back/app/service/interpret/soniox.py:23-67` — `MAX_ENDPOINT_DELAY_MS` · `ENDPOINT_KEYS` · `stt_config`. 30줄 주석 「= Soniox 기본」 은 틀렸다(Soniox 기본은 2000) — 바로잡는다.
- **값을 쓰는 곳 전부를 직접 grep 해서 센다**(목록을 믿지 말 것): `git grep -n -E "MAX_ENDPOINT_DELAY_MS|max_endpoint_delay_ms|endpoint_sensitivity|endpoint_latency_adjustment_level|ENDPOINT_KEYS"`. 코디가 본 곳: `back/scripts/quality_check.py`(89 · 90 · 605 — 결과 기록용 기본 끊김 값 표기) · `back/tests/test_quality.py`(68 · 73 — 기본 설정에 `endpoint_sensitivity` 가 **없다고** 고정한 시험) · `back/tests/test_quality_script.py`.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `back/`
- `docker-compose.yml · .env.example (레포 루트)`

## 6. 구현 단계

1. `soniox.py`: `MAX_ENDPOINT_DELAY_MS = 2000` · `ENDPOINT_SENSITIVITY = -0.3` 상수(§5.10 · D-67 주석) · `stt_config` 기본 설정에 두 값. `endpoint_config` 가 주어지면 지금처럼 덮어쓴다.
2. 결과 기록 · 스크립트에서 「기본 끊김 값」 을 적는 곳이 두 값을 다 적게(grep 결과 전부).
3. 시험 고침: 기본 설정 = 2000 · -0.3 · `endpoint_latency_adjustment_level` 없음 · `enable_agent_text_input` 없음. 덮어쓰기 시험은 그대로 통과.

## 7. 범위 제약 — 하지 말 것

- front · 반이중 · 끼어들기 · 시드 · 다른 STT 키를 건드리지 않는다.
- Soniox 키가 로컬에 없다(`back/.env` 없음) — 실물 호출은 **pending** 으로 보고(운영 배포 뒤 코디 · 사용자 실기기로 확인한다). 키를 찾으러 다니지 않는다.
- 사용자 포트 · 프로세스 · docker 를 건드리지 않는다.

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
