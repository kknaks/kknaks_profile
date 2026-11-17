# [pencil] 시술현황 시안 → OpenPencil 컴포넌트 세트 (리드 + 서브에이전트 분할)

너는 **cc-prototype `pencil` 워커(리드)**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/orchestration/roles/cc-prototype/pencil/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`) — **`tools.md` 의 OpenPencil 0.16.0 실측 API · eval 20초 제한을 꼭 지킨다**

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil` · 코디네이터와 같은 워크트리. **너는 앞 맥락이 없다** — 이 브리프와 아래 파일만 믿어라. 앞 판의 정정 문서(`pencil-correction-*.md`)는 읽지 마라(폐기된 방향).
사용자가 **지금 OpenPencil 앱에 `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/medikit/medikit.fig` 를 열어 두고 보고 있다.**

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-03-cc-day/screen/시술현황_프로토타입 (1).html` ← **생김새 정본(사용자 제공 시안, 3차 v11).** 컴포넌트의 모양 · 크기 · 색 · 글자 · 상태는 여기서 뽑는다. 3MB 단일 HTML — CSS 블록과 마크업을 grep 으로 읽어라(브라우저로 열어 봐도 된다).
- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-03-cc-day/screen/procedure-board-decisions.md` ← 같은 시안의 동작 결정(상태가 왜 있는지 참고용)
- 토큰: 변수 컬렉션 `medikit`(색 29, 이미 있음) · `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/medikit/SOURCE.txt` · `medikit-preset.json`(타이포 단계)
- 이미 있는 도구: `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/medikit/components/_lib.js` (앞 판이 만든 공통 함수 — 써도 되고 고쳐도 된다)
- ⚠ 다른 레포의 기존 구현 코드(DAY · cc-prototype)는 열지 않는다. 디자인 참고는 위 시안 하나.

**기대는 개념**
- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/para/areas/concept/design/design-system.md` · `design-token.md` — 시안 값을 그대로 옮기고, 색은 변수 바인딩.

## 2. 배경

시술현황 전체 화면 맵을 OpenPencil 에 그리려 한다. 그 전에 **시안에 나오는 컴포넌트부터** OpenPencil 컴포넌트 세트로 만든다. 화면 · 맵은 이번 범위가 아니다.
앞 판은 워커 혼자 한 번에 다 하려다 멈췄다. **이번엔 일을 쪼개고 서브에이전트를 쓴다.**

## 3. 계약 (다음 판이 이대로 소비)

- 「components」 페이지에 컴포넌트마다 섹션(이름표 + 세트). 세트 이름 PascalCase(시안 클래스 기준, 예 `Button` · `Badge` · `Card` · `RoomColumn` …), variant 속성은 `kind` · `size` · `state` 등 시안 클래스 축 그대로(`btn-solid` → `kind=solid`, `is-checked` → `state=checked`).
- 바뀌는 글자 자리는 TEXT 노드 이름 `label`. 모든 레이어에 의미 있는 이름(`Text` · `Frame` 같은 기본 이름 0).
- 색은 전부 변수 바인딩. 시안에만 있는 색(`--st-*` 상태색 등)은 컬렉션 `medikit` 에 변수로 **추가**(이름 `status/<이름>`)한 뒤 바인딩. 기존 29개 값은 바꾸지 않는다.
- 스크립트: `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/medikit/components/<Name>.js` (컴포넌트당 1개, 각각 20초 안에 끝나게) + `run-all.sh`(순서대로 실행 · 멱등 — 「components」 페이지를 지우고 다시 만든다).

## 4. 먼저 읽을 핵심 파일

- 시안 HTML 의 `<style>` 블록 — `.btn*` · `.cbadge` · `.card*` · `.room*` · `.ib-*`(인박스) · `.toggle` · `.checkbox` · `.search` · `.icon-btn` · `.proc*` · `.vital` · `.viewer-select` · `.cm-*`(모달) 등
- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/orchestration/roles/cc-prototype/pencil/tools.md`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/medikit/medikit.fig` — 「components」 페이지(새로) · 변수 컬렉션 `medikit` 에 `status/*` 추가 · 「medikit」 토큰 페이지의 린트 정리(`/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/medikit/import-medikit.js` 수정 후 재실행). 「Page 1」 은 비어 있게 둔다. 디스크 파일에 남은 옛 「시술현황 맵」 와이어 페이지는 폐기(저장 시 사라져도 된다)
- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/medikit/components/` — 스크립트
- 서브에이전트 시험용 임시 페이지 `draft/<그룹>` — 끝나면 지운다
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/orchestration/work/cc-procedure-map/pencil-components-report.md` (이것 하나)

## 6. 구현 단계 — 쪼개서

**A. 리드 — 인벤토리 (작게, 먼저)**
1. 시안에서 컴포넌트 목록을 뽑아 리포트 §인벤토리에 표로: 컴포넌트 · variant 축 · 상태 · 시안 근거(클래스 · CSS 줄) · 크기/패딩/모서리/글자/색 값. 시안에 반복되는 단위만(한 번만 나오는 레이아웃은 제외).
2. 컴포넌트를 **4~6개 그룹**으로 나눈다(예: 기본 입력류 / 배지 · 칩 / 버튼 / 카드 · 시술 줄 / 방 칸 · 인박스 / 모달 · 팝오버). 시안 상태색 변수(`status/*`)를 먼저 추가한다.

**B. 서브에이전트 — 그룹마다 1명, 병렬**
- 네 Agent 도구로 그룹 수만큼 띄운다. 각자에게 주는 것: 이 브리프 경로 · 자기 그룹 인벤토리 행 · `_lib.js` · tools.md.
- 각자 산출: 자기 그룹 `<Name>.js` 들. 시험은 자기 `draft/<그룹>` 페이지에서만(같은 페이지 동시 쓰기 금지), **자기 노드의 린트 오류 · 경고 0** 확인 후 draft 페이지 삭제.
- 서브에이전트는 「components」 페이지에 쓰지 않는다 — 합치기는 리드 몫.

**C. 리드 — 합치기**
- `run-all.sh` 로 「components」 페이지에 순서대로 렌더(두 번 돌려 노드 수 같음 = 멱등).
- `import-medikit.js` 를 고쳐 「medikit」 토큰 페이지 린트도 정리(배경 흰색 · 레이어 이름 · 대비).
- **문서 전체 린트: 오류 0 · 경고 0.** 시안 색 그대로는 대비 규칙에 걸려 0 을 못 만드는 경우가 있으면, **색을 바꾸기 전에** 그 목록(규칙 · 색 조합 · 건수)을 `[질문]` 으로 코디에게 보내고 답을 기다린다.
- `documents save` → 리포트.

## 7. 범위 제약 — 하지 말 것

- 화면 · 맵을 그리지 마라(다음 판). 컴포넌트만.
- 시안에 없는 컴포넌트 · 상태 · 문구를 지어내지 마라. 시안 문구를 샘플 label 로 쓴다.
- 한 번에 다 하려 하지 마라 — A → B(병렬) → C 순서. eval 은 20초 안에 끝나는 크기로.
- 기존 29개 색 변수 값 · 다른 파일 수정 금지. 커밋 · push 금지.

## 8. 검증

```
리포트에: 인벤토리 표 · 그룹 분할과 서브에이전트별 산출 · 컴포넌트 세트 목록(variant 수) · 린트 전/후 규칙별 건수(오류 0 · 경고 0) · run-all 두 번 노드 수 · 시안과 다르게 만든 곳
```
- 코디가 직접 `lint` 와 `info` 를 다시 돌려 대조한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_5f3a0622-cf65-40e8-bc2f-fdd1174707c9 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "pencil 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_5f3a0622-cf65-40e8-bc2f-fdd1174707c9 \
  --text "[worker_done] pencil 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_5f3a0622-cf65-40e8-bc2f-fdd1174707c9 --text "[질문] pencil: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
