# [reviewer] 배포 전 코드 검수 — 시드 `.9` · `.10` · 바로잡기 D-63 · D-64 (WP27 수정 1 · 2)

너는 WP23 · 24 · 26 을 검수한 **reviewer** 다(`review-wp26-code-report.md`). read-only · 리포트 1개. 작업 워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea`

- 변경: `git diff 0ec772d` + 새 파일(`seed_v9.py` · `seed_v10.py` · `test7.py` · `test7_page.html`)
- 기준: DEC D-61 ~ D-64 · 처분 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/quality-research-dispositions.md` §15 · §16 · backend 보고 `seed-v9-be-report.md` · `wp27-be-report.md`(수정 1 · 2)
- 볼 것: ① D-63 — 한자 언어 사이 한자 꼴 후보 제외가 정확한가(라틴 · 가나 꼴은 그대로) ② **D-64 한글 바로잡기가 멀쩡한 한국어 번역을 망가뜨리지 않나** — 직접 함수에 넣어: 일상 낱말 · 다른 term 이름 · 조사 보존 · 짧은 이름 · 한 → 외 무영향 ③ 시드 `.9` · `.10` 이 처분대로 · 재실행 같은 바이트 · 검사 통과 ④ 운영 경로에 시험 전용 코드가 섞이지 않았나 ⑤ `ruff` · `pytest` 직접 1회 ⑥ 배포 뒤 실물에서 볼 자리
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/review-predeploy-code-report.md` — PASS / WARN / FAIL

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
