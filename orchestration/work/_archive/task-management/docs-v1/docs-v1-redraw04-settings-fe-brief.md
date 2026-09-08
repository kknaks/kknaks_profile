# [frontend] REDRAW-04 — 설정 셸 · 업무 설정 · 연결 확인의 **시각만** 시안대로 고친다

너는 **task-management `frontend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

---

## ⛔ 0. 이 work 의 성격

**화면은 이미 완성되어 돌아간다.** 유형·프로젝트 CRUD, 인라인 추가·편집, 색 선택, 소프트 딜리트, 자동 저장이 전부 구현돼 있다.
**동작을 하나도 건드리지 마라. 틀린 것은 시각뿐이다.**

앞선 work 은 끝났다 — **REDRAW-00**(토큰) · **01**(로그인) · **02**(앱 셸·내 업무) · **03**(업무 상세). 되돌리지 마라.

### ⚠ 이 work 만의 특수 사정 — **업무 설정 화면은 시안이 없다**

`/settings/work`(유형·프로젝트 관리)는 **디자인이 그려진 적이 없다**(`design-requests.md` §B-1).
참고물 `work-settings-proposal.html` 이 있지만 **확정이 아니다 — 방향만이다.**

따라서 이 화면은 **두 가지로만 맞춘다.**

1. **설정 셸**(좌 메뉴 카드 + 우 패널 스택)은 시안이 있다 → 시안대로
2. **패널 내부**는 시안이 없다 → **디자인 시스템의 공통 규격**으로 맞춘다(카드·패널·인라인 행·셀렉터·팝오버·버튼)

**없는 화면을 발명하지 마라.** 공통 규격으로 설명이 안 되는 자리가 나오면 **고치지 말고 물어라.**

### 정본

| 순위 | 무엇 | 어디 |
|---|---|---|
| 1 | **사용자 승인 정정** | `orchestration/work/docs-v1/design-requests.md` §A |
| 2 | **시안 — 시각 정본** | `.dc.html` |
| 3 | **SPEC — 동작 정본** | `20-spec/spec-002-work-settings.md` |

### 🚫 되돌리지 마라

| 무엇 | 시안(낡음) | 코드(맞음) | 근거 |
|---|---|---|---|
| **업무 시간 셀렉터** | 프로필 패널에 있다 | **없다** | **A-14** — v1 제외. 쓰는 곳이 없다(캘린더 그리드 08–20 고정) |
| **유형 색** | 고정 4색 | **팔레트 8종 `colorToken`** | **A-1** — 값은 `SPEC-002 §4` |

### ⚠ 앞선 work 에서 배운 함정 3가지

1. **시안이 평평해 보여도 구조는 중첩이다.** gap 을 flat 하게 적용하지 마라
2. **「설명 그림」과 「설명 문장」이 다르면 문장이 맞다.** 축소 삽화의 그림자·크기를 값으로 읽지 마라
3. **`twMerge` 가 커스텀 프리셋을 버린다** — 새 프리셋을 추가하면 `lib/utils.ts` 에 **반드시 등록해라**

### 반드시 열 파일 (절대경로 · 읽기 전용)

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/00-design/로그인 · 계정 · 프로필.dc.html
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/00-design/디자인 시스템.dc.html
```

| 시안 화면 | 줄 | 대응 코드 |
|---|---|---|
| 설정 · 개인 설정 (**셸 규격의 정본**) | **115~264** | `(app)/settings/layout.tsx` · `SettingsMenuCard` · `SettingsPanel` |
| 설정 · 시간 선택 (셀렉터 열림) | **266~426** | `Selector` |
| 설정 · 경력 추가 인라인 | **427~594** | `InlineAddRow` · `InlineEditText` |
| 설정 · 연동 관리 | **1057~1229** | (화면 미구현 — 규격 참고만) |
| 공통 규격 | `디자인 시스템.dc.html` **05 · 06 · 07 · 10 RULES** | 전부 |

**`00-design/*.md` 요약본은 열지 마라.**

---

## 1. 확인된 앵커 — 설정 셸 (시안 138~168줄)

코디가 직접 확인한 값이다. **시안과 다르면 시안이 맞다.**

| 무엇 | 값 |
|---|---|
| breadcrumb | `left 240 / top 38` — 「홈 › 설정 › 개인 설정」 13px `#9EA2AE`, 현재만 `#757575`, chevron 11px `#B3B3B3`, `gap 7` |
| 페이지 타이틀 | `left 240 / top 66` — **28 / 700 / `-0.03em`** |
| **좌 메뉴 카드** | `left 240 / top 140` · **260 × 780** · 흰 배경 · border `#D9D9D9` · **r16** · `padding 16 12` · 항목 `gap 2` |
| 메뉴 항목 | **h38** · r8 · `padding 0 12` · **14px** · 아이콘 16px · `gap 10` · 비활성 `#5F6470` (hover `#F5F6F8`+`#1E1E1E`) |
| 메뉴 활성 | bg **`#F1F2F5`** · **14 / 700** · 아이콘 stroke `#1E1E1E` |
| 하단 묶음 | `margin-top:auto` · `border-top 1px #EBEBEB` · `padding-top 10` |
| 로그아웃 | **h36** · r8 · `padding 0 12` · 13px `#5F6470` · hover `#F5F6F8`+`#1E1E1E` |
| 계정 삭제 | **h36** · 13px `#757575` · hover bg **`#FEF8F7`** + `#E2685B` |
| 버전 캡션 | `border-top 1px #EBEBEB` · `padding 14 12 0 12` · `gap 6` · 12px — 「Managment v1.4.0」 `#757575` / 「마지막 저장 · 방금」 `#9EA2AE` |
| **우 패널 스택** | `left 524 / top 140` · **w1356** · 패널 사이 `gap 20` |
| 패널 | 흰 배경 · border `#D9D9D9` · **r16** |
| 패널 헤더 | **h60** · `padding 0 28` · `justify-between` · 제목 **16 / 700** · 우측 캡션 12px `#9EA2AE` |
| 패널 헤더 구분선 | `border-bottom 1px #F1F2F5` |
| 패널 헤더 버튼 | **h32** · r8 · border `#D9D9D9` · `padding 0 14` · 13px · hover `#F5F6F8` |
| 패널 본문 | `padding 24 28` |
| 목록 행 | **h64** · `padding 0 24` · `gap 14` · `border-top 1px #F1F2F5` |
| 행 아이콘 타일 | **34×34 · r9** · 13/800 |

> **두 컬럼의 아래 끝을 같은 y 에 맞춘다**(디자인 시스템 10 RULES 「설정은 패널 스택」).
> **자동 저장 화면엔 저장 버튼이 없다** — 패널 헤더에 「입력을 마치면 자동으로 저장됩니다」만 둔다(같은 절). 이미 그렇게 돼 있으면 그대로 둬라.

## 2. 업무 설정 패널 — 공통 규격으로만

시안이 없다. 아래 규격 밖으로 나가지 마라.

| 요소 | 규격 (디자인 시스템 05·06·07) |
|---|---|
| 패널 | r16 · border `#D9D9D9` — §1 과 동일 |
| 인라인 추가 행 | **h44** · bg `#FAFBFC` · 점선 체크박스/타일 · 「추가」 h28 r6 `#F1F2FE`/`#4B52A8` |
| 인라인 편집 행 | **h56** · bg `#FBFCFF` · 컨트롤 **h36** · 목록 컬럼과 **같은 순서**로 필드 나열, 필드를 합치지 않는다 |
| 셀렉터 | 닫힘 h42 border `#D9D9D9` / 열림 border `#7181F8` + ring `0 0 0 3px rgba(113,129,248,0.16)` · 목록은 트리거에 붙여서 같은 폭 · 항목 h36 · 현재값 `#F4F5FF`+`#4B52A8`+체크 |
| 색 선택 팝오버 | 팝오버 규격(200~400 · 트리거 아래 8px · 스크림 없음). 스와치 현재값은 **입력 포커스 글로우와 같은 토큰**(`--tm-focus-ring`) |
| 유형 배지 | h20 · r4 · 11/600 · `padding 0 7` — **색은 `colorToken`**(A-1) |
| 버튼 | 툴바 h34 / 패널 헤더 h30~32 · r8 |
| 빈 상태 | `EmptyState` 공통 |

**규칙(디자인 시스템 10)** — 「한 줄짜리 개체는 인라인」·「필드 4개 이하면 드로어를 열지 않는다」·「자동 저장 화면엔 저장 버튼이 없다」. 지금 코드가 이미 그렇다면 **그대로 둬라.**

## 3. 연결 확인 `/` — 규격만

`ConnectionCheckScreen` 은 시안이 없다. **디자인 시스템 05(카드·패널) + 06(버튼) 규격**으로만 맞춰라. 문구·동작은 그대로.

## 4. 범위

| 파일 |
|---|
| `app/(app)/settings/layout.tsx` |
| `features/settings/components/SettingsMenuCard.tsx` · `SettingsPanel.tsx` · `WorkSettingsScreen.tsx` · `WorkTypePanel.tsx` · `ProjectPanel.tsx` · `InlineAddRow.tsx` |
| `components/shared/ColorDot.tsx` · `ColorPickerPopover.tsx` · `AutoSaveFailureNotice.tsx` |
| `features/health/components/ConnectionCheckScreen.tsx` |
| `styles/tokens.css` · `tailwind.config.ts` · `lib/utils.ts` — **토큰 추가 + twMerge 등록만** |

**하지 않는 것**
- **동작·상태·조건·검증·라우팅·쿼리를 바꾸지 마라**
- `/settings`(개인 설정)·`/settings/integrations`(연동 관리) 의 **내용을 만들지 마라** — 지금 `<h1>` 뿐이고, 그건 **별도 신규 제작 work** 이다. 이 work 에서는 셸만 맞춘다
- 앞선 work 의 파일(로그인·내 업무·상세)을 건드리지 마라
- 기존 토큰 값을 고치지 마라. **더하기만** 한다
- **hex 리터럴을 컴포넌트에 쓰지 마라**

## 5. 검증

```bash
cd app/front && npx tsc --noEmit   # 0 에러. 전체 빌드 금지, 1회만
```

**캡처 4장** (`npm run dev`)
1. **1920** `/settings` — 셸(메뉴 카드 260 + 패널 자리 1356), 두 컬럼 아래 끝이 같은 y
2. **1920** `/settings/work` — 유형·프로젝트 패널
3. **1920** `/settings/work` — 인라인 추가 행 + 색 선택 팝오버 열린 상태
4. **1920** `/` 연결 확인

## 6. 지킬 것

1. **시각만 고친다.** 동작 코드를 한 줄도 바꾸지 마라
2. **없는 화면을 발명하지 마라.** 시안 없는 자리는 §2 의 공통 규격 안에서만 움직이고, 설명이 안 되면 **물어라**
3. **§0 의 「되돌리지 마라」를 지켜라** — A-14 업무 시간 없음, A-1 동적 색
4. **막히면 물어라** — `orca terminal send`. `orca orchestration ask` 는 답이 안 닿는다
5. **커밋·push 하지 마라**

## 7. Done Criteria

- [ ] 설정 셸이 시안 115~264줄과 일치 (메뉴 카드 260×780 r16 · 패널 1356 · gap 20 · 항목 h38 · 활성 `#F1F2F5`)
- [ ] 두 컬럼 아래 끝이 같은 y
- [ ] 업무 설정 패널이 §2 공통 규격 안에 있다 (발명 0)
- [ ] **A-14 업무 시간 없음 · A-1 동적 색 유지**
- [ ] `/settings`·`/settings/integrations` 의 내용을 만들지 않았다
- [ ] 동작 코드 diff **0줄** · 컴포넌트 hex 리터럴 0개 · 새 프리셋 twMerge 등록
- [ ] `npx tsc --noEmit` 0 에러 · 캡처 4장

---

## 8. 질문하는 법 — **`orca orchestration ask` 를 쓰지 마라**

```bash
orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[질문] frontend: <질문>" --enter
```

## 9. 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 / 셸 대조 결과 / 업무 설정 패널에 적용한 공통 규격 / 시안 없어 판단한 자리 목록 / 정정 유지 근거 / 동작 diff 0줄 근거 / tsc / 캡처 경로"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
