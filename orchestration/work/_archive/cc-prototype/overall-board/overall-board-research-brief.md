# [researcher] Ceramique 전체현황판 디자인 가져오기 · 현황 탭 분석 (read-only 조사)

너는 **cc-prototype `researcher` 워커**다. **앞 판의 맥락이 없다** — 이 브리프와 아래 파일만 믿어라. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc` (코디 워크트리 — 코디와 공유. 지정한 경로 밖은 건드리지 마라)

⚠ 병렬로 **frontend 워커**가 코드 레포(`/Users/kknaks/orca/workspaces/cc-prototype/overall-board`)에서 「현재 PoC 현황판」 인벤토리를 만든다. 너는 **디자인 쪽만** 본다. 코드와의 차이 비교는 이번 판에서 하지 않는다(다음 판).

## 1. SSOT — 먼저 읽을 것

- **Claude Design 프로젝트** (이게 이번 조사의 원천):
  `https://claude.ai/design/p/dda9a931-097f-4780-9301-972d5ac1fc23?file=Ceramique+%EC%A0%84%EC%B2%B4%ED%98%84%ED%99%A9%ED%8C%90.dc.html`
  - 주 파일: `Ceramique 전체현황판.dc.html`
  - 함께 읽을 import: `_ds/medikit-aea7ac33-f044-4445-9164-87b8b69474dc/_ds_bundle.css` · `_ds_bundle.js` · `fonts/fonts.css` · `styles.css` · `assets/ceramique-logo-color.svg` · `ceramique-theme.css` · `medikit-patches.css` · `support.js`
  - 접근: claude_design MCP / `DesignSync` 도구(https://api.anthropic.com/v1/design/mcp). 인증이 안 되면 **혼자 우회하지 말고** §9 질문 채널로 「/design-login 필요」라고 물어라.
- 앞 PoC 의 시술 현황판 정본(비교 축을 맞추는 참고용 — 읽기만):
  - `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md`
  - `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/10-decision/decision-005-procedure-board.md`

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 하나

명동 PoC v2 의 「시술 현황판」(procedure/front)을 사용자가 Claude Design 에서 **「Ceramique 전체현황판」으로 다시 디자인**했다. 이번 작업 목적은 현황판을 전체현황판으로 업그레이드하는 것이고, **다른 탭은 만들지 않는다 — 「현황」 탭 하나만** 대상이다.
이번 판은 구현 전 조사다. 디자인을 레포로 가져오고, **현황 탭이 무엇으로 이루어졌는지**를 빠짐없이 적는다.

## 3. 계약

해당 없음 (조사).

## 4. 먼저 읽을 핵심 파일

§1 의 디자인 주 파일과 import 전부.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/design/` — 디자인 프로젝트 파일 **원본 그대로** 저장(§1 의 주 파일 + import 전부, 프로젝트 안 경로 구조 유지). 다른 탭 파일이 주 파일에서 import 되면 그것도 받는다.
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/design-analysis-report.md` — 리포트 1개.

## 6. 할 일

1. 디자인 파일을 §5 경로로 받는다. 받은 파일 목록 · 크기를 리포트 머리에 적는다.
2. 주 파일의 **탭 구조**를 적는다(어떤 탭이 있고, 현황 탭은 어디서 시작·끝나는지 — 줄 번호).
3. **현황 탭**을 아래 축으로 빠짐없이 적는다. 각 항목에 근거 `파일:줄`.
   - (a) 레이아웃 영역: 헤더 · 필터/툴바 · 본문 영역(칼럼·그리드·리스트) · 사이드 · 하단 등, 영역별 크기/배치
   - (b) 상태/칼럼 체계: 어떤 단계(칸)로 나뉘나, 순서, 라벨 원문, 개수 뱃지
   - (c) 카드(항목) 해부: 카드 종류마다 표시 필드(라벨 원문 · 예시값 · 형식), 칩/뱃지/아이콘, 색 규칙(어떤 조건에 어떤 색)
   - (d) 상호작용: 버튼 · 팝오버 · 모달 · 토스트 · 호버 · 드래그 · 클릭 시 동작(디자인/ support.js 에 정의된 것만)
   - (e) 데이터 필드 목록: 화면에 나오는 모든 데이터 항목을 표로(필드 · 어디에 보이나 · 예시값). **KOS 에서 오는지는 판단하지 마라** — 그건 다음 판
   - (f) 테마 · 디자인 시스템: medikit DS 토큰/컴포넌트 중 현황 탭이 쓰는 것, `ceramique-theme.css` · `medikit-patches.css` 가 덮는 것, 폰트 · 로고
   - (g) 상태 변형: 빈 상태 · 로딩 · 에러 · 반응형(폭별) 시안이 있으면
4. 디자인 안에 적힌 메모·주석·TODO 원문을 따로 모은다.
5. 「정할 것」: 디자인만으로는 동작이 정해지지 않는 자리(예: 클릭 결과 미정의, 데이터 출처 불명)를 목록으로. **결정하지 마라.**

## 7. 범위 제약 — 하지 말 것

- 디자인 프로젝트(Claude Design)에 **쓰지 마라** — 읽기만.
- 코드 레포 · para/ 문서 수정 금지. 다른 탭 분석 금지(구조 목록에 이름만).
- 디자인 파일을 리포트에 통째로 붙이지 마라 — 리포트는 요약 + `파일:줄`.
- 실명 · 연락처가 디자인 예시값에 있으면 리포트에 그대로 옮기지 말고 「실명 있음(n건)」으로만 적는다(public 레포).

## 8. 검증

```
질문마다 답 + 근거(파일:줄). 디자인에 없는 것은 「디자인에 없음」. 결정하지 않고 「정할 것」으로 모은다
```

- 받은 파일 수가 주 파일의 import 목록과 맞는지 직접 대조해 리포트에 적는다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 --from term_eb710953-fbec-464a-8394-4ac257a48ffd \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ef44ce2a-44a4-42b6-9e71-309c0dbab728 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
