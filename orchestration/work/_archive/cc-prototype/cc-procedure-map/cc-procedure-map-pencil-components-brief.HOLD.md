> **보류 (2026-11-12)** — 사용자가 와이어프레임 맵을 먼저 원함. 맵 구조 확정 뒤 재개.


# [pencil] 메디킷 컴포넌트 21종을 OpenPencil(medikit.fig)에 컴포넌트 세트로 만든다

너는 **cc-prototype `pencil` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/orchestration/roles/cc-prototype/pencil/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디네이터와 같은 워크트리다. **너는 앞 맥락이 없다** — 이 브리프 · 역할 문서(특히 `tools.md` 의 0.16.0 실측 API) · 아래 파일만 믿어라. 사용자가 **지금 OpenPencil 앱에 `medikit.fig` 를 열어 두고 보고 있다.**

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/orchestration/work/cc-procedure-map/research-components.md` §5 「들여올 컴포넌트 목록(합계)」 ← **만들 목록의 원천.** §3·4 표는 각 조합이 어디서 왜 필요한지(근거).
- 메디킷 키트 원본(값의 원천): `/Users/kknaks/git/harness_works/medikit/src/ui/<컴포넌트>/` (tsx 의 tailwind 클래스 · props) · `/Users/kknaks/git/harness_works/medikit/src/styles/` · `/Users/kknaks/git/harness_works/medikit/tailwind.config.ts`
- 메디킷 시각 기준(눈으로 대조): `/Users/kknaks/git/harness_works/medikit/ds-bundle/_screenshots/ui__<컴포넌트>.png`
- 토큰 값 · CRM 덮기: `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/medikit/SOURCE.txt` · `medikit.css` · `day-override.css` · `medikit-preset.json`
- 토큰을 이미 올린 스크립트(패턴 참고): `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/medikit/import-medikit.js`

**기대는 개념**

- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/para/areas/concept/design/design-system.md` — 키트 값을 옮긴다. 새 디자인 언어를 만들지 않는다.
- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/para/areas/concept/design/design-token.md` — 색은 변수로 바인딩, 값 하드코딩 금지.

## 2. 배경 / 무엇을 바꾸나

cc 시술현황 전체 화면을 OpenPencil 캔버스에 맵처럼 그리고 화면 옆에 정책을 붙이려 한다. 그 화면들을 메디킷 컴포넌트 인스턴스로 짓기 위해, 먼저 **필요한 컴포넌트만** OpenPencil 컴포넌트 세트로 만든다.
지금 `medikit.fig` 에는 토큰만 있다: 변수 컬렉션 `medikit`(색 29) · 「medikit」 페이지(색 견본 · 타이포 컴포넌트 28 · 그림자 컴포넌트 3). 컴포넌트는 0개.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

다음 단계(화면 맵)가 이 컴포넌트를 인스턴스로 쓴다. 그래서 이름 규칙이 계약이다.

- 컴포넌트 세트 이름 = 메디킷 컴포넌트 이름 그대로(PascalCase): `Button` · `Badge` · `Popover` · `Command` · `Checkbox` · `ConfirmModal` · `Card` · `Table` · `Notify` · `BaseModal` · `Textarea` · `ComboBox` · `Banner` · `RadioGroup` · `Label` · `Tabs` · `Input` · `Divider` · `Accordion` · `DatePicker` · 아이콘은 `Icon`
- variant 속성 이름 = 메디킷 props 이름 그대로(`variant` · `color` · `size` · `state` …), 값도 props 값 그대로(`solid` · `blue` · `ss` …). 상태(disabled · checked · open …)는 `state` 속성으로.
- 텍스트가 바뀌는 자리(버튼 글자 · 배지 글자 등)는 TEXT 노드 이름을 `label` 로 둔다(인스턴스에서 덮어쓸 자리).

**사용자 확정 사항(2026-11-12) — research §6 기본값:**
- #6 오더 메모 · [이벤트] 는 Badge neutral sm 로 통일 → **Chip 은 만들지 않는다**(그래서 21종 · 60조합)
- #8 정보형 토스트는 만들지 않는다(Notify 는 키트대로 success · error 만)
- #11 타이머 · #12 보드 칸 · 줄 행 · 묶음 리스트는 컴포넌트로 만들지 않는다(다음 단계 몫)

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/orchestration/work/cc-procedure-map/research-components.md` §5 (L280 부근) — 21종의 조합 목록
- `/Users/kknaks/git/harness_works/medikit/src/ui/button/button.tsx` — variant × color × size 클래스 표가 있다. 이 패턴으로 나머지도 읽는다
- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/orchestration/roles/cc-prototype/pencil/tools.md` — **0.16.0 실측 API.** 공식 문서(개발판)의 `figma.variables` · `createTextStyle` 은 없다

## 5. allowed_paths — 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/medikit/medikit.fig` — **「components」 페이지(새로 만든다)** 와 「medikit」 페이지(아래 6-1 정리만). 「Page 1」 은 건드리지 않는다
- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/medikit/components/` — 새 폴더. 컴포넌트를 만드는 스크립트
- `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/medikit/import-medikit.js` — 6-1 정리만
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/orchestration/work/cc-procedure-map/pencil-components-report.md` (이것 하나)

## 6. 구현 단계

0. `bun ~/.bun/bin/openpencil documents list` 로 활성 문서 경로가 `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/medikit/medikit.fig` 인지 확인. 아니면 멈추고 묻는다. 첫 쓰기 때 `figma.notify("pencil 워커 작업 시작")` 를 띄운다(사용자 화면에 뜨는지 코디가 확인한다).
1. **(6-1) 토큰 페이지 정리** — `import-medikit.js` 를 고쳐 다시 돌린다: 「medikit」 페이지 배경 흰색(`#ffffff`), 타이포 줄 사이를 넓혀 컴포넌트 이름표가 윗줄과 겹치지 않게, 텍스트 레이어에 의미 있는 이름. 변수 · 컴포넌트 이름은 바꾸지 않는다.
2. **컴포넌트 값 뽑기** — 21종 각각 키트 소스에서 크기 · 패딩 · 모서리 · 테두리 · 글자(타이포 단계) · 색 토큰을 뽑는다. 키트가 `primary` 를 쓰면 변수 `primary/*`(CRM blue)에 바인딩. 스크린샷과 눈으로 대조.
3. **스크립트로 만들기** — `components/<컴포넌트>.js` 하나씩 + `components/run-all.js`(또는 순서 표). 「components」 페이지에 컴포넌트마다 섹션(이름표 + 세트), `combineAsVariants` 로 세트화. auto layout 을 쓸 수 있으면 쓴다(버튼 글자 길이가 바뀌어도 늘어나게). 색은 전부 `medikit` 변수 바인딩.
4. **멱등** — 다시 돌리면 「components」 페이지를 지우고 같은 결과를 만든다. 두 번 돌려 노드 수가 같은지 확인.
5. **저장** — `documents save`.
6. **리포트** — research §5 표의 행마다 「만든 조합 수 / 필요 조합 수」 대조표, 키트에 값이 없어 정한 곳, 바인딩 못 한 색.

## 7. 범위 제약 — 하지 말 것

- 화면(시술현황 고객 카드 · 보드 등)을 그리지 마라 — 다음 단계다. 컴포넌트만.
- 목록에 없는 컴포넌트 · 조합을 늘리지 마라. 필요해 보이면 리포트 「제안」으로.
- 이미 만들어진 시술현황 화면(DAY · cc-prototype 등)은 열지 마라.
- 「Page 1」 · 변수 컬렉션 값 · 다른 파일 수정 금지. 커밋 · push 금지.
- headless PNG 로 굵기 · 글자 폭을 판정하지 마라(Pretendard → Inter 대체). 배치 확인용만.

## 8. 검증

```
브리프 목록의 컴포넌트 · 조합이 전부 있다(항목별 대조표: 21종 · 60조합) · 색은 medikit 변수 바인딩 · 스크립트 재실행 시 같은 결과(노드 수 동일) · Page 1 무수정 · 저장됨
`bun ~/.bun/bin/openpencil info <fig>` 와 `lint` 결과 수치를 리포트에 붙인다
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
