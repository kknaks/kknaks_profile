# [reviewer] 배포 전 재검수 — D-65 (F-1 · F-2 처분 확인 · 짧게)

너는 배포 전 검수를 한 **reviewer** 다(`review-predeploy-code-report.md`). read-only · 리포트 1개. 작업 워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea`

- 처분: DEC **D-65** · 지시 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/quality-wp27-fix3-instructions.md` · backend 보고 `wp27-be-report.md` 「수정 3」
- 볼 것: ① 네 F-1 · F-2 재현 문장이 전부 안 바뀌거나 조사를 보존하나(직접 함수에 넣어) ② 새로 생긴 빈틈(첫 음절 같은 일상 낱말 — 예: 「보통」 「써서」 「피부」 류가 이름 앞부분과 거리 1 이 되는지 · 시드의 3음절 이상 ko 이름 전부로 몇 개 직접 시도) ③ `ruff` · `pytest` 직접 1회
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/review-predeploy-code-report-2.md` — PASS / WARN / FAIL

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d181fbae-29f2-43bb-9a41-6bc888ca07de --from term_15cca63d-5a2d-4753-a247-cde1162df48f \
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
