# `DS-gaps` 최종 상태 — 무엇이 코드에 있고, 무엇이 DS 에 없나

작성 2026-09-14 (코디) · 출처 `work/_archive/sc-ax/sc-meeting-redesign/design/DS-gaps.md` 46건 +
바퀴 9·9-B·11 보고

## 한 줄 요약

> **코드에서는 46건이 전부 채워졌다.** 안 그랬으면 구 `styles.css` 1313줄을 못 지웠다.
> **DS(Claude Design `TheSC AX Design System`)에는 아직 없다.** 그것을 올리는 것이 이번 작업이다.

`DS-gaps.md` 의 「DS 에 추가 요청 36건」은 **작업 중 시점의 제안**이다. 그 뒤 바퀴 9·9-B 가
「없으면 새 DS 어휘로 만든다」로 규칙을 바꿔 전부 우리 코드에 만들었다. 그 문서만 보면 오해한다.

## A. 부품으로 만든 것 — `frontend/src/ds/` 에 있다

| gap | 무엇이 없었나 | 코드의 자리 |
|---|---|---|
| **G-43** | 이니셜 아바타(사진 없이 글자) | `ds/Avatar.tsx` — 크기 5단 |
| **G-15 · G-46** | 열 수에 안 묶인 읽기 표 | `ds/DataTable.tsx` |
| **G-28** | 문장 안에 들어가는 글자 단추 | `ds/Button.tsx` 의 inline 변형 |
| **G-29** | 테두리형 배지(채움형과 구분) | `ds/Badge.tsx` 의 outline 톤 |
| **G-17** | AX 표면의 경계선·글자 단계 | `ds/Button.tsx` 의 ai 변형 + `--scax-ai-*` |
| **G-13** | `Skeleton`·`Popover`·`Toast` 가 DS 부품이 아니다 | `ds/Skeleton.tsx` · `ds/Popover.tsx` · `ds/Modal.tsx` |
| **G-10** | `Drawer` 폭 두 단 | `ds/Modal.tsx` 의 `size` prop (`sm` 520 / `lg` 840) |
| **G-11** | `ConfirmModal` 이 CSS 골격만 | `ds/Modal.tsx` |
| **G-12** | `TimeChip` 이 CSS 만 | `ds/TimeChip.tsx` |
| **G-04** | 값 있는 진행 막대 | `ds/ProgressBar.tsx` |
| **G-07** | 인라인 빈 값 표기 | `ds/Empty.tsx` 의 `EmptyValue` |
| **G-08** | 시각 한 쌍 | `ds/TimeField.tsx` 의 `TimeRangeField` |
| **G-09** | 다중 선택(칩) | `ds/Select.tsx` 의 `MultiSelect` |
| **G-25** | 인라인 상태 한 줄 | `ds/StatusNote.tsx` |
| **G-26** | 2단 메타 목록 | `ds/GutterList.tsx` |
| **G-30** | 클래스 기반 datetime | `ds/DateField.tsx` · `DatePicker.tsx` · `TimeField.tsx` — 우리 것을 유지했다 |

## B. 토큰으로 올린 것 — `styles/scax.css`

`--graph-*`(G-06 · 14종) · `--ai-*`(G-17 · 8종) · 상태 soft(G-16·G-19·G-42) ·
그림자(G-24) · 중립 tint(G-23) · 히어로(G-18)

## C. 화면 CSS 로 간 것

구 `styles.css` 규칙 366개가 `components` · `screens-a` · `screens-b` · `meetings` · `ax` 로 갈라졌다.
G-14(칸반·타임라인) · G-21(breadcrumb) · G-44(28px 제목) · G-38(간격 리터럴) 등이 여기 속한다.

## D. 아직 안 닫힌 것 둘

| gap | 왜 |
|---|---|
| **G-05** `FieldMessage` 톤 | **채울 것이 없다.** 호출부 7곳이 `error`/`help` 둘만 쓰고 `warning`·`info` 는 부르는 자리가 **0곳**이다. 만들면 안 쓰는 API 를 지어내는 것 |
| **G-45** textarea | 폼용 여러 줄 입력. `.scax-composer` 는 채팅 어휘라 폼 필드가 아니다 |

## E. 폐기

`G-03b` `ban`·`pending` 글리프 — 사용처 0.
(⚠ 원 문서의 「폐기 5종」은 정정됐다. `square`·`circle`·`empty` 는 **살아 있다**)

## F. 사용자 판단이 남은 것

| gap | 무엇을 정해야 하나 |
|---|---|
| **G-35** | 업무 카드 「요청」 배지가 **주황(대기) → 보라(AX)** 로 **뜻이 바뀌었다** |
| **G-06** | 관계탐색 노드 8색이 DS 원칙(「악센트 하나, 나머지 중립」)과 **정면 충돌**한다. 예외로 공인할지 |
| **G-01** | 글꼴이 `Pretendard JP` 가 맞나 (한글 자형이 미세하게 다르다) |
| **G-02** | 폰트를 로컬 동봉으로 바꿨다(DS 는 jsDelivr 원격. 그중 비-JP URL 은 **404 죽은 링크**였다) |
| **G-14** | 칸반·타임라인 유지 여부 (사용처 100곳) |

## 올리는 순서 — 여러 화면이 쓰는 것부터

1. `Avatar` · `DataTable` — 새로 만든 부품. 다음 화면이 바로 꺼내 쓴다
2. `Button` inline/ai · `Badge` outline — 기존 부품의 변형
3. 토큰 묶음 (`--scax-graph-*` · `--scax-ai-*` · 상태 soft)
4. 나머지 부품 (이미 DS 에 대응이 있던 것들의 갱신)

---

## 추가 (2026-09-15, `sc-ax-fe`) — 제자리 편집

> **브리프가 가리킨 `design/DS-gaps.md` 는 이 워크트리에 없다.** 실물은 아카이브
> (`work/_archive/sc-ax/sc-meeting-redesign/design/DS-gaps.md`)이고 살아 있는 문서는 이 파일이라
> 여기에 적는다. 새 파일을 만들지 않았다 — 같은 주제의 문서가 둘이 되는 것이 더 나쁘다.

| gap | 없는 것 | 어디서 | 새 DS 에서 가장 가까운 것 | 어떻게 했나 |
|---|---|---|---|---|
| **G-47** | **제자리 편집(inline edit)** — 읽는 글자가 그 자리에서 입력칸이 되는 것 | 회의 상세의 안건 제목 (사람 벌) | **없다.** `.scax-textfield` 는 48px 최소 높이 + 1px 테두리 + 좌우 안여백을 가진 «껍데기» 라, 글자 위에 얹으면 줄이 통째로 밀린다 | `ds/InlineText.tsx` 를 만들었다. 닫힌 `<button>` 과 열린 `<input>` 이 같은 상자·같은 활자(`font:inherit`)이고 테두리·바탕·안여백이 없다 |

### 사용자가 판단할 것 — **누를 수 있다는 것을 무엇으로 말하나**

지금은 **마우스 커서(`cursor:text`)가 전부다** (2026-09-15 사용자 결정: hover 표시를 지어내지 마라).
그래서 **마우스를 올리기 전에는 고칠 수 있는 글자인지 알 방법이 없다.** 시안에 그 표시가 없어
만들지 않았지만, 실제로 쓰다 보면 「여기를 누를 수 있는 줄 몰랐다」가 나올 자리다.

고른다면 후보 셋 — **전부 DS 에 없다**:

1. **hover 에서 아주 연한 바탕** (`--scax-color-fill-weak`) — 가장 흔한 관용이고 줄을 안 민다
2. **hover 에서 점선 밑줄** — 「고칠 수 있는 글자」라는 뜻이 더 분명하지만 밑줄 어휘가 링크와 겹친다
3. **지금 그대로 (커서만)** — 화면이 가장 조용하다. 시안이 고른 쪽이다

**내가 정하지 않았다.** 결정되면 `.scax-inline-text:hover` 한 줄이면 끝난다.

### 곁에 남긴 것 — 키보드 초점 테두리는 지우지 않았다

`:focus-visible` 의 `--scax-focus-ring` 은 남겼다. 그것은 hover 꾸밈이 아니라 **키보드로 이 자리에
닿았다는 유일한 표시**라, 지우면 키보드 사용자는 자기가 어디 있는지 알 수 없다. 마우스로 누를 때는
뜨지 않으므로 「hover 표시를 지어내지 마라」와 부딪히지 않는다. 이견이 있으면 게이트로 올려 달라.
