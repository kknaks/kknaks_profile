# [planner] UI 교정 스펙 WARN2 최소 정정
역할/경계/원천/13항목 계약은 ui-spec-brief.md 그대로. 읽을 것: /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/ui-spec-brief.md, planner-ui-spec-report.md, review-ui-spec-report.md. 스펙 트리 /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec. 앞 교정 diff가 미커밋으로 있다. 이번은 아래 WARN2만 최소 정정, WP/코드/서버/merge 금지.

## 1. W1
카드3행 기타정보를 gender만으로 확정한 해석을 UI선택 OQ로 표시(OQ-A21 통합 또는 새번호). isNew는 서버에 이미 존재하므로 「새 칸」 사실오류 정정. 새로운 카드항목/문구를 결정하지 않음. 기본표시는 기존제공값 기준 유지, 사용자의 확정4행 구조는 그대로.

## 2. W2
원장 A가 B지정 호출을 본인수락하면 현서버는 원장목록여부만 검사하므로 수락된다는 사실 명시. 케이스매트릭스에 성공가능 사실을 써 거절될거란 잘못된 전제를 없앰. 다른원장지정호출 버튼 노출여부는 후속확인점으로 보존, 이번에 차단정책/API를 추가하지 않음. 사용자확정 원장본인즉시수락을 기본으로 유지. 확인질문/승인게이트를 지금 새로 만들지 않음.

## 3. 경계·검증
수정허용 SPEC003 및 인덱스 최소정합뿐(가능하면 SPEC003만). log.md·30-work·WP·이슈·다른SPEC·코드 수정금지. git diff --check와 lint --strict 한 번. 하위위임/내부에이전트/커밋/push/merge 금지. 보고서는 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/planner-ui-spec-fix-report.md 한개. 수정위치/결과/남은확인점을 한국어로 보고. live preamble이 우선, 완료후 idle.

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
