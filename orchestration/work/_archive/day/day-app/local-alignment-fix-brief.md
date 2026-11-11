# [planner] 로컬 API 정합 W1 최소 보완
원천/역할/allowed_paths는local-alignment-brief.md그대로. review-local-alignment-report.md W1과참고를읽는다. 스펙트리 /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec.
W1 표시중복정리: 전체완료에서needs.home「귀가 대기 전」과사용자확정머리「시술 모두 완료 · 귀가 대기 전」이겹침. **확정된합성머리한번만표시**, 같은home문구를별도chip/머리로중복하지않음. 서버needs.home를지우거나업무판정을바꾸지않고, 카드빨강테두리/필터확인필요집계는needs서버값그대로. 다른needs있으면기존원문표시규칙유지. 사용자확정전체완료강조박스+귀가대기버튼그대로. OQ-A29기본값에이표시우선순위명시하고본문/A조건/WPv3필요한최소행정합. 새문구/정책/API발명금지.
참고정정: 개정후A31/A32/WPv3A2실물검증dev→현재로컬a1c90b9d(D6전), acceptance[0]v2표기→누적v3로. exactSHA는코디커밋후결속할예정이라고유지.
스펙003·delivery-request-v3.json 최소변경, profile planner-local-alignment-fix-report.md한개. 20-spec/타SPEC/코드/GitHub/승인receipt수정금지. gitdiff--check와JSONparse1회, 전체lint/schema는의미있는정합외변경없으면반복불필요. 하위위임금지. livepreamble우선,worker_done한번후idle.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_3333de45-6039-44ec-b7af-76bbd3afdb0c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
