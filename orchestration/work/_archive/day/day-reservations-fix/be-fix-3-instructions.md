# [backend] qa-2 관찰 — 링크 다시 쓰기는 시한 안에서만 · 시험 예약 취소

같은 터미널 · 같은 워크트리 · 같은 allowed_paths. **커밋 · push 하지 마라.** 스택 11340 떠 있음(리로드 괜찮음).

읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/qa-2-report.md` 「관찰」 첫 줄.

## 할 것
1. **D44 = 「열린(pending · opened · **시한 안**) 링크 다시 씀」** — 지금 `services/displays.py:339` `_open_link` 가 `opened` 요청을 만료 시각이 지나도 계속 다시 쓴다(1시간 넘은 링크 재사용). `expires_at > now` 조건을 더해 시한 지난 요청은 다시 쓰지 않고 새 요청을 만든다(고객 웹 토큰 · opened 상태 판정 자체는 바꾸지 마라). 테스트: opened + 시한 지남 → 새 pending · opened + 시한 안 → 다시 씀.
2. 관련 테스트 · ruff · mypy 각 1회.
3. **그다음 시험 예약 취소**: DEMO `def4cbab`(고객 b26e24e0 · 19:00) · `7511bbb0`(고객 1b9a7c0c · 19:30) 을 DAY 웹으로 취소 → KOS confirmed · 다음 동기화 canceled 확인 · 네 KOS 로그인 해제. 다른 예약 금지.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_99b025fc-f3ef-403e-8162-509c41545e2e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
