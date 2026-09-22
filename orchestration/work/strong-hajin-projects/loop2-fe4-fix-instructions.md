# FE-4 소수정 — 검수 FAIL 1 · WARN 5

**읽을 것**: `orchestration/work/strong-hajin-projects/review-loop2-fe4-report.md` (255줄)
**allowed_paths**: `frontend/` 만. **`backend/` 0줄** — 다른 워커가 `backend/tests/` 에서 작업 중이다.
커밋·push 금지. **개발 서버 금지** (`5173`·`8100` 은 사용자 E2E 스택).

검수: **계약(L-36·L-42~L-48)을 깨뜨린 자리는 없다.** 틀고정 다섯도 좌표계 0줄도 실측으로 참이다.
고칠 것은 **단언이 무르거나 값이 눈을 지나친 자리**다.

## FAIL-1 — 새 단언이 부하에서 흔들린다 (**반드시**)

`ProjectPage.test.tsx:328-336` 이 **패시브 effect**(`ProjectGantt.tsx:149-151`)가 쓴 `scrollLeft` 를
**`waitFor` 없이** 읽는다. 검수 실측: `make frontend-test` **9회 중 1회** `expected +0 to be 68` 빨강,
**파일 단독 실행에서도 8회 중 2회.** → **Phase FE-4 의 완료 판정이 항상 서지 않는다.**

→ 그 읽기를 **`await waitFor(...)`** 로 감싸라.
**고친 뒤 그 파일을 단독으로 10회 이상 돌려 전부 초록**인 것을 보여라(검수가 2/8 로 잡았으니 10회면 충분하다).

## WARN-1 — 「여백 2일」을 아무 단언도 붙들지 않는다

지금 기대값을 **`GANTT.openLead` 로 되계산**하는 **자기참조 단언**이다.
검수 뮤테이션: **`openLead` 를 2→0 으로 바꿔도 23건 전건 통과**한다(2→4 에서야 `not.toBe(0)` 이 잡는다).
즉 실제로 고정되는 것은 **「0 이 아니다」뿐**이고, 앞 판 리포트의 「실수치 68 로 잰다」는 **과한 주장**이었다.

→ **상수를 되계산하지 말고 «기대하는 수»를 직접 적어라.** 그리고 **뮤테이션으로 확인하라** —
`openLead` 를 0 이나 4 로 바꾸면 **빨강이 되는가**. 안 되면 여전히 무의미한 단언이다.

## WARN-3 — 완료 바 `opacity: .55` 가 톤을 지나쳤다

검수가 토큰 원값으로 계산했다 — fill 합성색 **휘도**가 `accent 0.216` · `danger 0.201` 인데
**`done .55` 는 0.552(2.5배)**, **채도는 0.48 로 셋 중 최저**(`.9` 였을 때 0.87).
흰 트랙 위에서 투명도를 낮추면 **채도만이 아니라 밝기가 오른다.**
검수 제안: **`.70~.72`** 면 채도 0.67 로 accent·danger 사이에 든다.

→ **`projects.css:110` 한 줄**을 그 범위로 고쳐라. **최종 판정은 사용자 눈**이니
리포트에 「고칠 곳은 이 한 줄」을 다시 적어라.

## WARN — 「오늘이 축 «왼쪽» 밖」인 경우가 비어 있다

검수 판정: 오른쪽 밖은 옳고 테스트도 있다. 그런데 **왼쪽 밖**(= **아직 시작 전 프로젝트**)이면
`scrollLeft = 0` 이 되어 **「기간의 첫날」**을 보이는데, 이는 **L-45 의 문면(「오늘이 보인다」)과 어긋나고
테스트도 0건**이다.

→ 그 경우를 **어떻게 할지 정하고 테스트를 더해라.**
「아직 시작 전이면 첫날을 보인다」가 맞다고 보면 **그렇게 적고 그것을 재는 테스트**를 넣어라
(계약 문면과 다르면 리포트에 올려라 — 코디가 SPEC 에 반영한다).

## 나머지 WARN 둘

검수 리포트의 WARN-2·WARN-4·WARN-5 를 읽고 **각각 닫거나, 닫지 않는 이유를 적어라.**

## ⚠ 검수가 발견한 «이 판 밖» 사실 — 고치지 말고 리포트에 옮겨만 적어라

- `make frontend-test` 9회에서 **기존 실패 4회**: `task checklist`(2) · `task checklist span/null` ·
  `adjustment and resubmission` · `product surfaces`. **전부 FE-4 밖**이다
- 1루프에 흔들렸던 `MeetingMaterials`·`ActionCenter` 는 **9회 모두 통과** —
  **흔들리는 자리가 옮겨갔다.** 이 사실을 리포트에 적어라(코디가 flaky 대장에 옮긴다)

## 검증

- **FAIL-1 은 단독 10회 이상** 전부 초록
- **WARN-1 은 뮤테이션으로** 단언이 실제로 잡는지 확인
- `make frontend-test` · `npx tsc --noEmit`. **기존 실패와 네 실패를 분리**
- ⚠ 기계에 사용자 E2E 스택이 떠 있어 부하가 높다. 부하로 흔들린 것은 분리해 보고만 해라

## 역할·맥락

너는 **strong-hajin `frontend` 워커**다. 먼저 읽어라:
- `.../roles/strong-hajin/frontend/role.md` (+ `rules.md`) · 코드 레포 `AGENTS.md`
- `review-loop2-fe4-report.md`(검수) · `loop2-fe4-report.md`(앞 판이 한 일)
- `spec-005-projects.md` §2.4 · §6 의 L-36·L-42~L-48

워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`.
**FE-5 몫(헤더 생성 버튼·모달 · 우 레일 업무 정보 · 상태 드롭다운 · 좌 레일 헤더 한 줄)은 건드리지 마라.**

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_7901a9f7-b7ea-4863-b662-d598242c7b29 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: FE-4 소수정" \
  --body "FAIL-1 단독 N회 결과 / WARN 각각 어떻게 닫았나 / 뮤테이션 결과 / 왼쪽 밖 처리 / 이 판 밖 flaky 목록 / git status"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] frontend 완료 — FE-4 소수정. 상세는 인박스." --enter
```
