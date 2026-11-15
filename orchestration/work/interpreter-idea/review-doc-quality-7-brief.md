# [reviewer_doc] SPEC 0.9.1 확인 — 0.9.0 검수 처분(§11) 반영만 (짧게)

너는 0.9.0 을 검수한 **reviewer_doc** 다. **read-only** — 리포트 1개만. 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토`

- 처분: `orchestration/work/interpreter-idea/quality-research-dispositions.md` §11(끝의 낱말 경계 확정 줄 포함) · planner 보고 `quality-spec-report.md` 「0.9.1」
- 볼 것: ① §11 처분이 SPEC · WORK 에 그대로(`파일:줄`) — 특히 F-1 ③ 범위 · 낱말 경계 · W-1 · W-2 순서 · `translation_before` · ko_wrong 첫 목록 0 ② 네가 짚은 F-1 위험(en · vi 일상 낱말)이 이제 막혔나 — 시드 `.7` 로 다시 걸어 보기 ③ 새 어긋남 0 · public 0
- 리포트: `orchestration/work/interpreter-idea/review-quality-doc-report-7.md` — PASS / WARN / FAIL

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d181fbae-29f2-43bb-9a41-6bc888ca07de --from term_84f40940-7d19-4ce7-b55c-2f76c48155c8 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
