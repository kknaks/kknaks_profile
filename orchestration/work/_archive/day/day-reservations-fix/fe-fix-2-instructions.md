# [frontend] qa-1 고침 — 링크 복사/열기 · CSP · [+] 칸 단위

같은 터미널이면 앞 맥락 그대로 · 같은 워크트리 · 같은 allowed_paths. **커밋 · push 하지 마라.** 로컬 스택 11340 이 떠 있다 — 시작 · 멈춤 금지(파일 바꾸면 리로드됨 · 그건 괜찮다).

읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/qa-1-report.md`(FAIL-1 · WARN-1 · W-a) · 스크린샷 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/qa-1/`

## 할 것
1. **FAIL-1**: `day.js:6120` `dpLinkAfterRequest` — 응답이 `#modal-root` 를 통째로 바꿔 폼이 떨어진 뒤라 `e.detail.elt` 로 못 고름 → `e.detail.requestConfig.elt` 로 폼을 찾거나 swap 전(`htmx:beforeSwap`)에 응답 조각에서 링크를 읽어라. 「링크 복사하기」 = 클립보드(ClipboardItem Promise · W-3 그대로) · 「링크 열기」 = 미리 연 탭이 그 링크로 바뀜. node 테스트로 이 경우(폼이 문서에서 떨어진 뒤 afterRequest)를 고정.
2. **WARN-1**: 팝오버 위치를 `style` 속성으로 넣어 htmx settle 이 속성을 옮기며 CSP `style-src-attr` 위반 — CSSOM(`el.style.setProperty`)은 되는지 · 안 되면 위치를 다시 그린 뒤 다시 계산하는 등 **콘솔 오류 0** 이 되게.
3. **W-a (코디 기본값 · `_RESUME.md` §2 맨 위)**: [+] 칸 · 빈 칸 누르기의 시각 단위 = **그 열 그룹 간격**(`interval_minutes` · 60분 그룹 = 정각만 · 30분 그룹 = 30분). 등록 창 「예약 시간」이 늘 골라진 채 열려야 한다. 끌어 놓기(옮기기) 단위는 지금 그대로.
4. 웹 화면 테스트 · node 테스트 · lint · build --check 각 1회.

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
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
