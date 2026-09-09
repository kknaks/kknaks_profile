# [frontend] 조사 — 디자인 시스템 v2 ↔ 현재 프론트 대조 (read-only)

너는 **sc-ax `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/roles/sc-ax/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

이 태스크는 **조사 전용**이다. 워크트리 파일을 하나도 고치지 않는다. 산출물은 §6 의 리포트 파일 1개뿐.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system/docs/design/design-system-v2.dc.html` ← 디자인 시스템 v2 원본(Claude Design canvas, 160KB). **이 파일이 시각 규칙의 SoT 다.** 여기 없는 규칙을 발명하지 마라.
- `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system/docs/design/README.md` — 참조본의 위치와 「구현은 styles.css 가 소유」 원칙.
- `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system/README.md` — 화면·기능의 현재 동작 설명(「로그인과 세션」~「일일보고」).
- 화면 근거(필요할 때만): `/Users/kknaks/git/harness_works/mediness-mediness/products/sc-ax/20-spec/spec-001~010` (canonical 체크아웃 — **읽기만**, 절대 수정 금지). `21-screen/`·`21-html/` 은 비어 있다 — 화면 명세는 없는 것으로 친다.

**기대는 개념** — 해당 없음 (이번 조사에서 「토큰 소유는 styles.css 한 곳」 원칙만 지켜 판단한다).

## 2. 배경 / 무엇을 바꾸나

디자인 시스템 v2 가 2026-09-03 `docs/design/` 에 편입됐고 2026-09-07 사용자가 이 파일을 **확정본**으로 못박았다. 그런데 프론트(`frontend/src/styles.css` 901줄 + `*.tsx` 25개 + `chat/`)가 v2 를 어디까지 따르는지 아무도 대조하지 않았다.
이 조사는 **「프론트가 무엇을 바꿔야 하나」 목록**을 만드는 것이다. 바꾸는 건 다음 태스크다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음 (BE 와 무관. 조사 결과가 다음 구현 태스크의 입력이 된다).

## 4. 먼저 읽을 핵심 파일

- `docs/design/design-system-v2.dc.html` — 전체를 한 번에 읽지 말고 grep/sed 로 아트보드 제목·`<style>`·`--*` 변수·섹션 헤딩부터 잡고 구간별로 읽어라.
- `frontend/src/styles.css:1-40` — 현재 `:root` 토큰. 이게 v2 와 맞는지가 1차 질문.
- `frontend/src/App.tsx`, `frontend/src/WorkViews.tsx`, `frontend/src/WorkModals.tsx`, `frontend/src/ActionCenter.tsx`, `frontend/src/chat/` — 화면 골격과 공용 컴포넌트가 어떤 클래스·인라인 스타일을 쓰는지.

## 5. allowed_paths — 이 밖은 건드리지 마라

- (read-only — 워크트리 파일 수정·생성·삭제 금지. 산출물은 §6 의 리포트 파일 1개뿐 — 코디 워크트리 `orchestration/work/sc-design-system/` 아래)

## 6. 조사 단계

1. **디자인이 정의한 것**을 축별로 목록화한다: (a) 색 토큰 (b) 타이포(패밀리·크기·굵기·행간) (c) 간격·radius·shadow (d) 컴포넌트(버튼·칩/배지·입력·테이블/리스트·카드·모달·드로어·탭·사이드바/네비·토스트·빈 상태 등)와 상태(hover/active/disabled/selected) (e) 레이아웃(앱 셸·사이드바 폭·헤더·컨텐츠 폭) (f) 반응형(브레이크포인트·접힘) (g) 다크모드 유무. 각 항목에 **아트보드/섹션명**을 붙인다.
2. **프론트의 현재 값**을 같은 축으로 목록화한다: `styles.css` 의 `:root` 와 클래스, 각 tsx 의 className·inline style. 컴포넌트 안 hex 리터럴은 `grep -n '#[0-9a-fA-F]\{3,6\}' frontend/src/*.tsx frontend/src/chat/*` 로 전수 센다.
3. **대조표**: 「축 | 디자인 값(아트보드) | 현재 값(파일:줄) | 판정(일치 / 값 다름 / 누락 / 프론트에만 있음)」.
4. **바꿔야 할 것**을 영향 큰 순으로 정리한다. 항목마다 근거(디자인 섹션 + 프론트 파일:줄)를 붙이고, **CSS 토큰만 고치면 되는 것** 과 **컴포넌트 구조(마크업·새 컴포넌트)를 바꿔야 하는 것** 을 나눈다.
5. 디자인에는 있는데 프론트에 대응 화면/컴포넌트가 없는 것, 반대로 프론트엔 있는데 디자인이 정의 안 한 것을 따로 적는다.
6. 리포트를 `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/work/sc-design-system/fe-survey-report.md` 에 쓴다. 형식:
   - 요약(5줄 이내) / 디자인이 정의한 것(축별 한 문단) / 대조표 / 바꿔야 할 것 우선순위(토큰·구조 구분) / 디자인 미정의·프론트 전용 / 미결·확인 필요

## 7. 범위 제약 — 하지 말 것

- 워크트리 파일 수정·생성 금지. `styles.css` 를 고치기 시작하지 마라 — 그건 다음 태스크다.
- 디자인 파일에 없는 규칙을 「보통 이렇게 한다」로 채우지 마라. 못 읽은 것은 「확인 필요」로 남긴다.
- 스펙(`20-spec/`)은 화면이 무엇인지 확인하는 데만 쓴다. 스펙과 디자인이 어긋나면 고치지 말고 미결란에 적는다.
- 테스트·빌드를 돌리지 않는다 (조사 전용).

## 8. 검증

```
리포트에 (1) 디자인 축 (a)~(g) 전부에 대해 「정의됨/미정의」가 적혀 있는가 (2) 대조표의 모든 행에 파일:줄 또는 아트보드명이 있는가 (3) hex 리터럴 전수 개수가 grep 결과와 일치하는가 — 셋 다 스스로 확인하고 리포트 끝에 체크 결과를 남긴다. git status 가 리포트 파일 외에 깨끗한가.
```

- 워크트리에 변경이 생겼다면 되돌리고 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_05d3028b-5830-4523-9819-21785ea51f5b --from term_99679654-1a7c-470e-90a8-6978c0aa6c1a \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_05d3028b-5830-4523-9819-21785ea51f5b \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_05d3028b-5830-4523-9819-21785ea51f5b --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
