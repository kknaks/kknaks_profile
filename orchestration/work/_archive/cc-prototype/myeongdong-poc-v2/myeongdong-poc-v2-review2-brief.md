# [reviewer] r2 — 리뷰 r1 수정 확인 (read-only)

너는 같은 cc-prototype `reviewer` 워커다. 같은 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/myeongdong-poc-v2` 의 `procedure/`.

- 네 r1 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/review-wp1-5-report.md` 의 F1~F3 · W1~W14 가 **처분 `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/fix-decisions-r1.md`** 대로 고쳐졌는지 하나씩 판정(PASS · 남음 · 새 문제). SPEC 은 0.2.0(`para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md` — 부록 B)
- back 과 front 의 새 필드 이름이 맞물리는지(`limits.callMin` · `limits.anesMin` · 마취 `long`) — 실제 back 을 띄워 front 가 그 값을 읽는지 확인해도 된다(compose 로 띄우면 끝나고 내려라 · 사용자 포트 3700/8700 에 사용자 프로세스가 있으면 다른 포트로)
- 새로 생긴 문제만 새 지적으로. **r1 에서 PASS 였던 곳은 다시 훑지 마라**
- 산출물: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/review-r2-report.md` 하나 · 리포 수정 0 · KOS 쓰기 0 · 커밋 금지

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
  --subject "reviewer 완료: r2" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
