# [frontend] MyWork 시안 — 변경 정리 3종 (읽기·분석만)

너는 방금 `.design-sync/screens/` 로 시안 12파일을 받아온 그 워커다. 그 시안을 그대로 쓴다.

## 1. SSOT — 세 갈래

| 갈래 | 입력 |
|---|---|
| A. 확정 시안 | `.design-sync/screens/` (이 워크트리, 네가 받은 것) |
| B. 현재 화면 | `frontend/src/features/work/` · `frontend/src/shell/` · `frontend/src/ds/` |
| C. v2 정책 | **아래 스냅샷 경로**(2026-09-17 14:29 동결본) |

```
/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/v2-snapshot-2026-09-17/
  정의_v2.md · 생명주기_v2.md · 작업계획서_v2.md · example.md · task-raw-notes.md
```

⚠ **v2 원본은 지금 다른 세션이 편집 중이다.** 위 스냅샷만 읽어라. `reference/` 나 코디 워크트리의
살아 있는 사본을 읽지 마라 — 작업 중 상태를 읽게 된다.

**시안이 정본이다.** 시안과 현재 코드가 다르면 「코드가 바뀔 것」이다. 시안을 현재 코드에 맞춰
깎지 마라. 시안과 v2 문서가 다르면 그것은 **양쪽에 보고할 사실**이지 네가 판정할 일이 아니다.

## 2. 산출물 — 3파일, `.design-sync/report/` 에

| 파일 | 무엇 |
|---|---|
| `01-현재화면-대-시안.md` | B → A 로 가려면 무엇을 바꾸나. 화면·부품·라우트·상태 단위 |
| `02-DS-gaps.md` | 시안이 쓰는데 우리 DS 35종·클래스 어휘에 **없는** 부품·토큰·패턴 |
| `03-시안-대-v2문서.md` | 시안이 그린 흐름과 C 가 정한 정책이 **어긋나는 자리** |

## 3. 전수조사로 시작하라 — 목록을 주지 않는다

「고칠 곳 N개」를 세어 주지 않는다. **네가 세라.** 빠진 것은 항상 남이 준 목록 밖에서 나온다.

시작 전에 이 넷을 각각 grep 으로 세고, 그 수를 리포트 머리에 적어라:

1. 현재 업무 화면의 표면 — `frontend/src/features/work/` 의 export 되는 컴포넌트·훅 전부
2. 시안이 쓰는 DS 표면 — `handoff/**/*.jsx`·`components.css` 의 `scax-*` 클래스와 `window.SCAX.*` 호출 전부
3. 우리 DS 가 가진 표면 — `.design-sync/config.json` 의 `componentSrcMap` 35종 + `frontend/src/styles/` 의 클래스
4. 시안이 그린 행위 — `data.js`·`work-data.js`·`work-modal.jsx` 의 `status`·`badge`·`actions` 값의 **서로 다른 값 전부**

그 다음 2↔3 의 차집합이 `02`, 1↔시안이 `01`, 4↔v2 가 `03` 이다.

## 4. 쓰는 법

- **지적마다 근거를 붙인다** — `파일:줄` 과 인용. 근거 없는 지적은 쓰지 않는다.
- **정하지 못한 것은 「Open Questions」로 남긴다.** 임의로 결정하지 마라. 특히 `03` 은
  「시안이 맞다/문서가 맞다」를 네가 판정하지 말고 **차이만** 적어라 — 판정은 사용자 몫이다.
- 우선순위나 공수 추정을 붙이지 마라. 시킨 것은 「무엇이 다른가」다.
- `01` 은 FE 발주서의 원료, `02` 는 DS 작업 원료, `03` 은 **지금 v2 문서를 쓰는 다른 세션이 바로 쓴다.**
  셋 다 그 사람이 혼자 읽고 이해할 수 있게 써라.

## 5. allowed_paths

**`.design-sync/report/` 만.** 새로 만드는 디렉토리다. 그 밖은 **전부 읽기만.**

- `frontend/`·`backend/`·`.design-sync/screens/` 및 기존 `.design-sync/` 파일 — **읽기만.** 한 글자도 고치지 마라.
- 코디 워크트리(`/Users/kknaks/…/strong_hajin/`) — §1 스냅샷 경로만 **읽기.** 쓰기 금지.
- 코드·테스트·DS·문서 **수정 없음.** 이번엔 분석만이다.

## 6. 제약

- 이 트리엔 W1 미커밋 변경 20여 파일이 살아 있고 다른 에이전트도 동시에 돈다.
  **`git stash`·`checkout`·`reset`·`clean` 금지.** 커밋·push·PR 금지.
- 테스트·빌드 실행 불필요.
- 시안의 못 받은 자산(PNG 3·woff2 2)은 이번 분석과 무관하다. 다시 받으려 하지 마라.

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 이 preamble 과 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_d0d0454a-1ab6-484f-b125-d67fe035c803 --from term_758e0ac7-53e6-4313-bf71-f39d7b971a19 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: 디자인 변경 정리 3종" \
  --body "머리에 적은 전수 4개 수치 / 01·02·03 각 항목 수 / Open Questions 수 / 못 본 것"

# (2) 직접 주입
orca terminal send --terminal term_d0d0454a-1ab6-484f-b125-d67fe035c803 \
  --text "[worker_done] frontend 완료 — 디자인 변경 정리 3종. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d0d0454a-1ab6-484f-b125-d67fe035c803 --text "[질문] frontend: <질문>" --enter`
