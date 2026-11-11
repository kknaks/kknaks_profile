# [reviewer_doc] 로컬 API 정합 SPEC003 + WP v3 독립 검수
기존역할/read-only경계는review-ui-spec-brief.md, review-wp-v2-brief.md를따른다. 대상스펙트리 /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec. profilework /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app.
읽을것 local-alignment-brief.md(최신사용자진행지시·계약), planner-local-alignment-report.md, delivery-request-v3.json, SPEC003현재diff+1551fa22원본, WPv2원본, 옆SPEC002@e421b77b/코드@a1c90b9d 읽기전용.
검수: needs[]5상황server값/문구소비, canRecall노출·권한, 취소확인모달원문, lastSeconds→분표시형식(업무재계산없음), 반복마취·pickable서버값수용. 원장변경/방이동/차트쓰기등새기능없음. UI13항목/원장직접·간호대리/TW/토스트되돌리기없음/4필터4행4메뉴/배지서버없음 보존. 본문·U·표·A·OQ정합0모순. SPEC001/D1환경·보안·푸시·통역서버계약무관변경없음. WPv3같은235·riskL3·scope_delta·baselinepending정직·app/만·원래plan2최신local소비를이은정합이지범위확대아님. 옆세션미머지상태보존·선머지gate없음.
검증 gitdiff--check, lint--strict(DAY0), JSONschema/model검증. 판정PASS/WARN/FAIL 및근거file:line/JSON경로. 보고서profilework review-local-alignment-report.md 한개만생성. 스펙/JSON/코드/GitHub수정금지·하위워커/내부agent금지. livepreamble우선·worker_done한번·idle.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_4fc8346e-2c4e-4f56-a8a4-96120c073f8c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
