# [backend] WP21 수정 1 — 품질 시험 스크립트 판정 3건 · v6 거절 순서 측정 (코드 검수 W-1 ~ W-4)

너는 WP21 을 쓴 **interpret-pwa `backend` 워커**다. 맥락이 없으면 `quality-wp21-be-brief.md` · `wp21-be-report.md` 부터.
작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea` · 검수 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/review-wp21-code-report.md`

## 고칠 것 (코디 처분 — 리포트 권고대로)

| # | 처분 |
|---|---|
| W-1 | 오류 · 실패로 끝난 문장(`failed` 또는 `errors` 있음 · 세션 `error` 종료)은 `machine = "error"` — pass · fail · none 집계에서 빼고 따로 센다. 시험 1건 |
| W-2 | `--rules` 를 주면 목록의 T 번호 집합 ⊆ 규칙 파일 번호 집합인지 확인 · 다르면 빠진 번호를 알려 주고 `SystemExit`. 시험 1건 |
| W-3 | **로컬 결과를 먼저** 쓰고(레포 밖 확인 뒤) 그다음 레포용을 대조해 쓴다. 대조는 JSON 의 **문자열 값만**(키 제외 · term id · 코드 값(`pass` · `fail` · 언어 코드 등) 제외). 시험 1건(짧은 발화 `no` 헛걸림 재현이 이제 통과) |
| W-4 | **측정만 — 운영 코드 고치지 마라.** v6 에 일부러 한도를 넘는 context(예: zh-Hant 를 줄이기 없이 · 또는 기준보다 큰 글자 수)를 보내, 거절(`invalid_request`)이 ① 첫 메시지로 오는지 ② 빈 `tokens` 메시지 뒤에 오는지 ③ 설정 뒤 몇 ms 에 오는지를 3회 재서 결과 JSON(레포 밖 scratchpad · 문장 0)과 보고에 남긴다. v5(`stt-rt-v5`)로도 1회 대조. ②면 「`_check_config` 가 빈 tokens 메시지를 건너뛰어야 함」 을 보고만 하라(SPEC 개정이 먼저다) |

- allowed_paths: `back/scripts/` · `back/tests/` (운영 `app/` 무수정)
- 검증: `cd back && uv run ruff check . && uv run pytest -q` 1회 · 키는 앞 판과 같은 방식(사용자 `.env` → 프로세스 env 만)
- 보고서: `wp21-be-report.md` 끝에 「수정 1」 절

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
