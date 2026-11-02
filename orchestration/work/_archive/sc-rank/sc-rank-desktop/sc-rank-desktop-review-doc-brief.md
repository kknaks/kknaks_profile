
# [reviewer_doc] SC Rank SPEC-001 · WORK-001 문서 검수 (read-only)

너는 **sc-rank `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/roles/sc-rank/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ 이 워크트리는 **코디네이터의 작업 트리**다. 리포트 파일 1개 외에는 아무것도 만들거나 고치지 마라. 너는 앞 맥락이 없다 — 아래 파일이 전부다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/para/projects/summer-star/sc-rank/10-decision/decision-001-desktop-app.md` — 결정 14건 (검수 기준)
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/para/projects/summer-star/sc-rank/20-spec/spec-001-desktop-app.md` — **검수 대상 1**
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/para/projects/summer-star/sc-rank/30-work/work-001-desktop-port.md` — **검수 대상 2**
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/para/projects/summer-star/sc-rank/00-baseline/baseline-001-desktop-app.md` — 입력·사용자 원문
- PoC(동작 정본): `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/reference/2026-09-09-sc-prototype/server/*.mjs` · `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/reference/2026-09-09-sc-prototype/src/main.jsx` · `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/reference/2026-09-09-sc-prototype/tests/*.mjs` · `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/reference/2026-09-09-sc-prototype/README.md`

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

웹 PoC(Express + React, 포트 둘)를 서버 없는 Tauri 2 + Rust 데스크톱 앱으로 옮긴다. 이 문서 둘을 기준으로
워커 하나가 바로 구현에 들어간다. **워커가 추측으로 메워야 하는 빈칸, PoC 와 어긋난 서술, 빠진 이식 항목**을
구현 전에 잡는 것이 이번 검수의 목적이다.

## 3. 계약

해당 없음 (검수만).

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/reference/2026-09-09-sc-prototype/src/main.jsx` — 화면이 실제로 부르는 명령과 입력 필드 (SPEC §2·§5 대조)
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/reference/2026-09-09-sc-prototype/server/index.mjs` — 검증·동시 1건·간격·문구 (SPEC §2 대조)
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/reference/2026-09-09-sc-prototype/server/place.mjs` · `place-dom.mjs` · `blog.mjs` · `blog-browser.mjs` · `workbook.mjs` — SPEC §4 전수 대조
- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/reference/2026-09-09-sc-prototype/tests/place.test.mjs` · `blog.test.mjs` — SPEC §6 A-1 이 옮길 단언

## 5. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/work/sc-rank-desktop/review-doc-report.md` (이 파일 1개만 생성)

## 6. 구현 단계

1. 역할 `rules.md` 의 「문서 검수」 체크리스트를 전수로 돈다.
2. SPEC §4 표의 각 행을 PoC 코드에 대조한다 — PoC 에 있는데 표가 안 가리키는 판정·문구·제한값·타임아웃을 찾는다.
3. SPEC §2 명령 셋이 PoC 화면 호출과 1:1 인지, 입출력 키가 PoC 응답과 같다고 말할 근거가 되는지 본다.
4. WORK-001 Phase 끝 조건이 확인 가능한지, SPEC 인수조건 A-1~A-9 가 Phase 에 빠짐없이 배정됐는지 본다.
5. 리포트를 `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype/orchestration/work/sc-rank-desktop/review-doc-report.md` 에 역할 문서의 형식으로 쓴다.

## 7. 범위 제약 — 하지 말 것

- 문서·코드를 고치지 마라. 제안은 리포트에만.
- DEC-001 의 결정 자체(Tauri·서버 없음·파워링크 제외 등)를 다시 논의하지 마라. 문서가 결정과 어긋나는지만 본다.
- 네이버에 요청을 보내지 마라.

## 8. 검증

```
SPEC·WORK 를 PoC 코드와 DEC 에 대조. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_7f81f426-1d1d-4036-983d-a48b8b469147 --from term_f5bb51be-d024-4dcb-8ba9-1946a0f5eae9 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_7f81f426-1d1d-4036-983d-a48b8b469147 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_7f81f426-1d1d-4036-983d-a48b8b469147 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
