# [frontend] SPEC-004 WP3 — 웹 로그인 계정 체계

같은 cc-prototype `frontend` 워커 · 같은 워크트리. backend 가 `procedure/back` 에서 WP1(계정 · 권한 · auth API)을 동시에 만든다 — **backend 의 '[WP1 완료]' 를 코디가 알려 줄 때까지 SPEC 계약대로 만들고, 실 back 확인은 그 뒤**.

- 계약: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md` §3.6(웹은 admin 카드만 · 세션에 role · name · 헤더 계정 이름 · 의국 수락 doctorId 그대로) · §3 auth API 모양. 작업: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/para/projects/summer-star/cc-prototype/30-work/work-004-procedure-app.md` WP3
- allowed_paths: `procedure/front/**` · 검증: tsc · lint · build 1회 · front 재기동 · 커밋 금지

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: SPEC-004 WP3" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
