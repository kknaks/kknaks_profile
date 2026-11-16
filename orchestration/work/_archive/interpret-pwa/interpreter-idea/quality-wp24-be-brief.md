# [backend] WP23 마무리(D-56 한도 표) + WP24 ① — 조합 C · C2 로 T01 ~ T33 · 손님 쪽 21문장 초안 (멈춤 → 코디 확인 → ②)

너는 WP21 ~ WP23 을 한 **interpret-pwa `backend` 워커**다. 맥락이 없으면 `wp21-be-report.md` · `wp22-be-report.md` · `wp23-be-report.md` 부터.
작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea`(WP23 변경 미커밋 — 그대로 이어서)

## 1. 결정 (DEC — `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md`)

- **D-56**: `langs.py` `CONTEXT_MAX_CHARS` = v6 실측 통과 최대치 × 0.96 내림 — en 24,892 · ja 21,962 · zh 22,551 · zh-Hant 22,685 · th 23,215 · vi 24,349 · yue 22,825. 주석의 근거도 v6 · × 0.96 으로
- **D-55**: 조합 **C2** = C 와 같고 `max_endpoint_delay_ms` 만 2000(조합 인자 `--endpoint` — 운영 값은 안 바꿈)
- D-54 뺌(27개)을 적용한 시드 `.7` 그대로 둔다

## 2. 할 것

1. **D-56 반영** — `langs.py` 표 · 이 값에 기대는 시험만 고침 · `ruff` · `pytest` 1회 · **㉒ 다시**: v6 · 문안 · `.7` 로 7개 언어 연결 → 거절 0 · **7개 언어 모두 줄이기 0**(묶음별 뺀 수 0)을 표로. 하나라도 빠지면 멈추고 보고
2. **조합 C · C2 로 T01 ~ T33** — WP22 와 **같은 음성 파일**(해시 대조) · **같은 규칙 파일**(바꾸지 마라) · 울쎄라 T02 · T03 은 `.7` 그대로(E7 로 짝 이미 빠짐). 결과 레포용 → `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/wp24-C.json` · `wp24-C2.json` · 로컬용 → `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/reference/2026-11-12-interpreter-idea/quality-run/wp24-*-local.json`
3. **손님 쪽 21문장 초안**(D-50 · WORK WP24 ② 조건 그대로) — 시험 목록 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/reference/2026-11-12-interpreter-idea/test-sentences.md` 끝에 「6. 손님 쪽」 절로 T34 ~ T54(언어 순서 en · ja · zh · zh-Hant · th · vi · yue · 언어마다 3) · 시드 `.7` 그 언어 현지명이 든 시술명 1개 이상 · 손님이 클리닉에서 할 법한 짧은 문장 · 기대 = ko 대표명. 규칙 파일에 T34 ~ T54 추가(`negate` literal — 한국어 번역에 ko 대표명이 없으면 걸림 · 기대 발화 수). **음성은 만들되 실행은 하지 마라**
4. **여기서 멈춘다** — 코디가 손님 쪽 문장 · 규칙을 확인한 뒤 ②(T34 ~ T54 를 C · C2 로) 지시
5. 보고: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/wp24-be-report.md` — D-56 ㉒ 표 · C · C2 기계 FAIL(절별) · 3절 조각 수 · 지연 중앙값 · 손님 쪽 21문장의 번호 · 언어 · 쓴 term id(문장은 보고에 넣지 마라)

## 5. allowed_paths

- `back/app/service/interpret/langs.py` · `back/tests/` · `back/scripts/` · 위 로컬 경로 두 파일(목록 · 규칙)과 `quality-run/`

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
