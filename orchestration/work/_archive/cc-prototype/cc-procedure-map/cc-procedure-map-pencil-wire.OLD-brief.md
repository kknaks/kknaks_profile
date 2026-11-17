
# [pencil] cc 시술현황 프로덕트 맵 — 와이어프레임 화면 · 연결 화살표 · 정책 메모

너는 **cc-prototype `pencil` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/orchestration/roles/cc-prototype/pencil/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디네이터와 같은 워크트리다. **너는 앞 맥락이 없다** — 이 브리프 · 역할 문서(특히 `tools.md` 의 OpenPencil 0.16.0 실측 API) · 아래 파일만 믿어라. 사용자가 **지금 OpenPencil 앱에 `medikit.fig` 를 열어 두고 보고 있다.**

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/git/ax-clinic-project/para/projects/clinic-myeongdong-ax/phase-1/clinic-os/cc/cc-기획안-시술현황.md` ← **원천.** 화면 · 버튼 · 이동 · 정책은 전부 여기서만. 없는 것은 발명하지 마라.
- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/orchestration/work/cc-procedure-map/research-components.md` ← 앞 판 조사. **§1 화면 표(screenId 56행)와 §2 화면별 정책 줄 범위를 그대로 쓴다**(screenId 를 새로 짓지 마라). §6 「정할 것」의 사용자 확정은 §3 아래.
- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/프로덕트 맵 공동 캔버스 — 개발 도전 문서.md` ← 이 맵의 설계 의도: 맵 · 메모를 **데이터 파일로 두고 `screenId` 로 잇고, 캔버스는 렌더러가 그린다.**
- ⚠ **이미 만들어진 시술현황 페이지(DAY · cc-prototype 등 다른 레포 구현 · 기존 시안)는 절대 열지 않는다** — 사용자 지시.

**기대는 개념**

- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/para/areas/concept/design/design-system.md` — 이번 판은 DS 이전의 와이어(회색 박스). 메디킷 색 · 컴포넌트를 입히지 않는다.

## 2. 배경 / 무엇을 바꾸나

사용자가 원하는 것: 기획을 **페이지 · 버튼 단위로 시각화**한 프로덕트 맵.

```
[화면] ──(버튼 이름)──▶ [화면]      [정책 · 기획 메모]
```

- 화면은 와이어프레임(회색 박스 + 기획안 문구). 화면 안의 버튼 · 요소마다 **번호 마커 ①②③**.
- 화면과 화면은 **화살표**로 잇고, 화살표에 「무엇을 누르면」(트리거 버튼 이름)을 적는다.
- 각 화면 옆에 **정책 · 기획 메모 카드**: 마커 번호별로 그 버튼 · 요소의 정책을 기획안 **원문 인용 + 줄 번호**로.
- 기획안 절(1 시술 현황 보기 · 2 시술 준비 · 3 호출 · 4 시술 진행 · 5 귀가 대기 · 6 관리실 기록 · 7 고도화)마다 섹션으로 묶는다.

## 3. 계약 (다음 판이 이대로 소비)

**데이터 파일이 원본, 캔버스는 렌더 결과.** 다음 판(메디킷 입히기 · 메모 추가 · 재생성)이 이 파일을 읽는다. 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/cc-procedure-map/`:

- `screens.json` — `[{ "screenId", "name", "kind"(화면/패널/모달/토스트/상태), "section"(기획안 절 번호), "source"(기획안 줄 범위), "elements": [{ "no"(마커 번호), "label"(기획안 문구 그대로), "type"(button/badge/input/list/text/…), "source" }] }]`
- `edges.json` — `[{ "from"(screenId), "to"(screenId), "trigger"(elements 의 no 또는 문구), "source"(줄) }]`
- `notes.json` — `[{ "id", "screenId", "elementNo"(없으면 null = 화면 전체), "author": {"type":"doc","name":"cc-기획안-시술현황"}, "kind"("policy"/"memo"/"open-question"), "body"(기획안 원문 인용 — 요약 · 재작성 금지, 길면 앞부분 + 「…」), "source"(줄) }]`
- `render.js` — 위 셋을 읽어 그리는 렌더러(`eval --stdin` 로 돈다 — JSON 은 스크립트 안에 주입하는 빌드 스텝이 필요하면 `build.sh` 로)
- 캔버스 노드 이름에 `screenId` 를 넣는다: 화면 프레임 `screen/<screenId>`, 메모 `note/<id>`, 화살표 `edge/<from>→<to>`.

**사용자 확정(2026-11-12 · research §6 기본값):** #3 CC 모바일 3행은 맵 가장자리 「CC 모바일(참고)」 묶음 · #4 의국 화면 하나로(관리실별은 7 고도화) · #5 「귀가 대기 취소」는 「⋯」 더보기 안(P:L656) · #9 지정 호출은 라디오 + 「호출」, 시작 · 담당 변경은 클릭 즉시 반영. **#2 변경 이력 · #7 적용 확인 창 문구 · #10 담당자 목록 원천은 미정** → 화면은 빈 자리 + `kind:"open-question"` 메모로만.

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/git/ax-clinic-project/para/projects/clinic-myeongdong-ax/phase-1/clinic-os/cc/cc-기획안-시술현황.md` — 각 절의 「화면 구성」 표(요소 · 문구)와 「누르면 … 열린다/이동한다」 문장이 elements · edges 의 원천
- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/orchestration/work/cc-procedure-map/research-components.md` §1(L25 부근) · §2 · §3·4(화면별 UI 요소 표 — elements 초안으로 써도 된다)
- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/orchestration/roles/cc-prototype/pencil/tools.md` — 0.16.0 API

## 5. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/cc-procedure-map/` — 새 폴더(데이터 · 렌더러 · 빌드 스크립트)
- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/medikit/medikit.fig` 의 **새 페이지 「시술현황 맵」만.** 「Page 1」 · 「medikit」 페이지 · 변수는 건드리지 않는다
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/orchestration/work/cc-procedure-map/pencil-map-report.md` (이것 하나)

## 6. 구현 단계

0. `bun ~/.bun/bin/openpencil documents list` 로 활성 문서가 `medikit.fig` 인지 확인(아니면 멈추고 묻는다). 첫 쓰기 때 `figma.notify("pencil: 시술현황 맵 그리는 중")` — 사용자 화면에 뜨는지 코디가 확인한다.
1. **먼저 한 섹션만**(1. 시술 현황 보기) 데이터 → 렌더 → 저장하고, **코디에게 `[질문]` 으로 「1절 렌더 완료, 확인 요청」을 보낸 뒤 답을 기다린다.** 사용자가 모양을 보고 고칠 것을 준다. 승인 전에 나머지 절로 넘어가지 마라.
2. 승인되면 2~7절 + CC 모바일(참고)까지 데이터 확장 → 렌더.
3. 레이아웃: 섹션은 위에서 아래로, 섹션 안 화면은 흐름 순서대로 왼쪽→오른쪽. 화면 프레임은 데스크톱 비율(예 960×600, 모달 · 패널은 실제 비율로 작게), 메모 카드는 그 화면 바로 아래 또는 오른쪽에 붙여 겹치지 않게. 화살표는 커넥터 API 가 있으면 쓰고, 없으면 선 + 화살촉 벡터로 — 어느 쪽인지 리포트에 적는다.
4. 와이어 스타일: 흰 바탕 · 회색 박스(gray 변수 바인딩 가능하면) · 버튼은 테두리 박스 + 글자 · 마커는 작은 원 숫자. 메모 카드는 연노랑, `open-question` 은 빨간 테두리.
5. **멱등** — render 를 다시 돌리면 「시술현황 맵」 페이지를 지우고 같은 결과(노드 수 동일).
6. `documents save` → 리포트: 화면 수 · 엣지 수 · 메모 수(종류별) · research §1 56행 대조(맵에 있음/없음) · 기획안에서 이동 대상을 못 찾은 버튼 목록.

## 7. 범위 제약 — 하지 말 것

- 기획안에 없는 화면 · 버튼 · 문구 · 이동을 지어내지 마라. 화면 안 문구는 기획안 문구 그대로, 없으면 빈 박스.
- 정책을 요약 · 재작성하지 마라 — 원문 인용 + 줄.
- 메디킷 색 · 컴포넌트를 입히지 마라(다음 판).
- 기존 시술현황 페이지 · 시안 열람 금지. 「Page 1」 · 「medikit」 페이지 · 다른 파일 수정 금지. 커밋 · push 금지.
- 1절 확인 승인 전에 전체로 넘어가지 마라.

## 8. 검증

```
research §1 56행이 맵에 전부 있다(대조표) · 모든 note 에 source 줄 · 모든 edge 의 from/to 가 screens.json 에 있다(고아 0) · render 재실행 시 노드 수 동일 · 기존 페이지 무수정 · 저장됨
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
