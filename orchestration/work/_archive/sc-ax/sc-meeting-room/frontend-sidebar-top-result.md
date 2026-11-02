# 사이드바 상단 시안 적용 — frontend 결과 보고

워크트리 `ax-workspace/sc-meeting-room` · 브랜치 `kknaksss/sc-meeting-room` · 커밋/push/PR 없음(미커밋).
시작 시 HEAD `5e7a41d`(앞 프론트 작업 커밋) 확인. **워크트리의 미커밋 변경은 backend 17개 파일뿐이었고
그것은 사용자 것이라 한 줄도 건드리지 않았다** — 이번 변경은 `frontend/src` 6개 파일이다.

| 항목 | 상태 |
|---|---|
| 아바타·이름·직책 좌측 / 접기 버튼 우측 | **완료** |
| 알림 행 → 설정 행 → 가로 구분선 | **완료** |
| 알림 **실제 disabled** (클릭·키보드 불가) | **완료** |
| 설정을 기존 동작에 연결(이동, 중복 제거) | **완료** |
| 접기/펼치기·축소 상태 동작 유지 | **완료** (접힌 상태 접근성 결함 하나를 발견해 함께 고침) |
| 실제 사용자 데이터 사용 | **부분** — 사진·직책이 API 에 없다(아래 §미비) |

---

## 구현

### 상단 신원 줄
`SideNav` 의 신원 줄은 이미 «아바타 → 이름/직책 → 접기(오른쪽)» 순서였다(`.scax-side-nav__collapse{order:3}`).
바꾼 것은 둘이다:
- **아바타 자리를 채웠다** — 사진 URL 이 있으면 `<img>`, 없으면 **DS `Avatar`(첫 글자)**.
  예전에는 URL 이 없으면 자리를 통째로 비웠다(시안 31 에는 아바타가 있다). 없는 주소로 `<img>` 를
  그려 깨진 이미지를 내지는 않는다. 구 `.avatar` 를 되살리지 않았다 — `ds/Avatar` 를 쓴다.
- `.scax-side-nav__who{flex:1 1 auto;min-width:0}` — 이름/직책 칸이 남는 폭을 먹어야 접기가 오른쪽 «끝» 에 선다.
  측정: 기둥 오른쪽 180 · 접기 오른쪽 163(= 기둥 여백 12 + 신원 여백 4) → 콘텐츠 오른쪽 끝.

### 알림 · 설정 · 구분선
자리는 `SideNav` 가 **이미 갖고 있던 `utilityItems`**(구분선 위 그룹)다 — 새 구조를 만들지 않았다.
`App.tsx` 가 두 줄을 넘긴다.

- **알림** — 갈 화면이 없으므로 **`<button disabled>`** 로 세웠다. `aria-disabled` 만 붙이는 방식과 다르다:
  `disabled` 는 클릭·Enter/Space·탭 순서를 **한꺼번에** 막는다. 접힌 상태에서도 여전히 못 누른다(검사로 잠금).
  **알림 점·미확인 건수는 넣지 않았다**(시안의 파란 점은 셀 값이 없다). 기능을 새로 만들지 않았다.
- **설정** — 기둥 **바닥에 있던 그 설정을 이 자리로 옮겼다.** 여는 것도 그대로다:
  `setCharacterPreferenceError(null); setIsCharacterPickerOpen(true)` →
  **`AssistantCharacterPicker`(dialog "내 AX 캐릭터")**. 새 설정 페이지를 만들지 않았고 다른 페이지로 추측 연결하지 않았다.
  화면 전환이 아니므로 `NavItem.onActivate` 로 직접 걸어 **`surface` 라우팅에 `settings` id 가 흘러들지 않게** 했다.
- **바닥은 로그아웃 하나만 남겼다** — 같은 것을 두 자리에 두지 않는다. 로그아웃 동작·자리는 그대로다.
- 구분선은 `utilityItems` 가 있을 때 서는 기존 `.scax-side-nav__divider` 를 그대로 쓴다.

### 아이콘 — DS 원본에서 가져왔다
- **`bell`** (알림) · **`setting`** (설정): 우리 세트에 없어서 DS 로컬 사본
  `design/components/icon/Icon.jsx` 의 path 를 **그대로** 옮겼다. 기하를 새로 그리지 않았다.
- **우리 `tune` 을 설정에 쓰지 않았다** — 그것은 3단 이퀄라이저이고 시안의 글리프는 «줄 둘 + 손잡이»
  (DS `setting`)다. 비슷하다고 바꿔 쓰지 않았다.

### 접힌 상태 — 접근성 결함 하나를 발견해 고쳤다
검사를 쓰다 드러났다: **접히면 나브 줄에 읽어 줄 이름이 하나도 없다.** 라벨 글자가 빠지고 남는
글리프는 `aria-hidden` 이라, 눈으로는 hover 툴팁(`data-label`, CSS)이 말해 주지만 스크린리더에는 빈 단추다.
이것은 내 변경이 만든 것이 아니라 **원래 있던 것**이고, 브리프의 「축소 상태 접근성 유지」에 걸려 있어
**접힌 동안만** `aria-label={item.label}` 을 붙였다(펴져 있으면 라벨 글자가 이미 그 일을 한다). 시각 변화 없음.

## 변경 파일 (6)

| 파일 | 무엇 |
|---|---|
| `frontend/src/App.tsx` | `utilityItems`(알림 disabled · 설정 onActivate) · 바닥 설정 제거 · `shellNav` 사용 |
| `frontend/src/shell/SideNav.tsx` | `NavItem.disabled`·`onActivate` · Avatar fallback · 접힘 `aria-label` |
| `frontend/src/ds/icons/glyphs.tsx` | `bell` · `setting` 글리프 (DS 원본 그대로) |
| `frontend/src/lib/labels.ts` | `shellNav`(알림·설정·로그아웃) — ds 안에 문구를 두지 않는다 |
| `frontend/src/styles/shell.css` | `.scax-nav-item:disabled` · 신원 줄 간격·`__who` flex·첫 글자 아바타 정렬 |
| `frontend/src/shell/AppShell.test.tsx` | 검증(아래) |

`backend/`·`api.ts` 구조·`viewModels`·권한 정책·`docs/`·`.design-sync/`·`frontend/ds-entry.tsx` **무수정.**
하단 메뉴 순서·이름·라우팅·로고·버전은 손대지 않았다(범위 밖).

## 실제 사용자 데이터 — API 미비 (보고)

`/api/auth/me` 의 `OrganizationProfile` 에는 **사진 URL 도 직책(job title)도 없다.**

| 값 | 지금 |
|---|---|
| 이름 | `display_name` — **실제 값** |
| 직책 | **없다.** 지금 줄에는 `organizations` 이름(예 「SCAX」)이 선다 — 소속이지 직책이 아니다 |
| 사진 | **없다.** DS `Avatar` 의 첫 글자로 선다 |

`roles?: string[]` 이 있지만 그것은 **권한 역할**(`organization_access` 의 role)이라 직책이 아니다 —
직책인 척 내면 사실이 아니므로 쓰지 않았다. **시안의 「유하람님/기획자」를 가짜로 넣지 않았다.**

직책 값 자체는 제품 안에 있다 — 조직 명부(`getOrganizationUnitMembers` → `positions[0].position` / `grade`,
`features/meetings/roster.ts` 가 쓰는 그 값)다. 다만 그것은 **다른 엔드포인트**라 여기서 끌어오면
세션 화면이 조직 트리 전체에 의존하게 된다. **BE 가 `/api/auth/me` 에 직책(과 사진 URL)을 실어 주면**
한 줄로 연결된다 — API 요청 사항으로 올린다.

## 검증

```
cd frontend && npx tsc --noEmit                      → 오류 0
cd frontend && npx vitest run --no-file-parallelism  → 50 files / 558 passed / 0 failed
```
직전과 같은 558 (검사를 **늘리지 않고 기존 셸 검사를 고쳤다**). 전체 실행은 **1회**만 했고 통과 후 반복하지 않았다.
병렬 부하 실패는 이번에 관찰되지 않았다.

**고친 기존 검사 둘 — 순수 스타일 복제가 아니라 «뜻이 바뀐 것» 이다:**
1. 「아바타 URL 이 없으니 img 를 안 그린다」 → **「`<img>` 는 안 그리고 첫 글자 아바타가 선다」**.
   원래 의도(깨진 이미지를 내지 않는다)는 그대로 지키면서 자리를 비우지 않게 됐다.
2. 「시안에만 있는 메뉴 넷(수신함·진행 현황·자료·**알림**)은 만들지 않았다」 →
   셋은 그대로 없음, **알림은 「자리는 서되 진짜 disabled」** 로 바뀌었다. 「없음」 단언으로 때우지 않고
   실제 상태를 검사한다.

**더한 검증(기능):** 설정을 누르면 「내 AX 캐릭터」 dialog 가 열리고 닫힌다 · 알림은 `disabled` ·
접으면 「메뉴 펴기」가 서고 **접힌 채로도 「회의」로 이동이 된다**(라벨 없이도 접근성 이름으로 찾힌다) ·
다시 펴진다. 스타일 값을 베끼는 검사는 넣지 않았다.

## 시각 확인 — 정적 harness (실제 앱 아님)

**스크린샷**: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-ax-workspace-sc-meeting-room/d8eabb9c-1303-46da-a32a-eb9cf9d2e588/scratchpad/sidebar.png`
(스크래치패드 — 리포에 파일을 남기지 않았다.)

**한계**: `styles/index.css` 의 `@import` 사슬을 펴서 **앱과 같은 CSS·같은 순서**로 싣고 사이드바 상단
마크업만 손으로 재현해 headless Chromium 으로 계산값을 읽은 것이다. **실제 앱을 띄우지 않았다.**
확인된 것은 배치·순서·색뿐이고, 실제 라우팅이 붙은 화면·hover 툴팁·실제 세션 데이터로 그린 모습은
확인되지 않았다. **실제 회의·업무를 생성하거나 변경하지 않았고 dev server 도 띄우지 않았다.**

측정:
- 아바타(16~48) → 이름(64~) → 접기(~163) **가로 순서 참**, 접기가 기둥 콘텐츠 오른쪽 끝(여백 17)
- 알림(top 66) → 설정(top 120) → 구분선(top 174) **세로 순서 참**
- 알림 `disabled=true` · 설정 `disabled=false`
- 이름 `rgb(23,23,25)` 대비 **17.9:1** · 설정 줄 **4.54:1** · 알림(비활성) **1.33:1**

## 미결 · 관찰

1. **알림의 비활성 색이 매우 흐리다** — `--scax-color-ink-disabled`(DS 의 disabled 토큰), 대비 **1.33:1**.
   브리프가 「비활성 색상」을 요구했고 DS 단추의 `:disabled` 와 같은 토큰이라 그대로 썼지만, 읽기에는
   거의 안 보인다. 한 단 진한 `--scax-color-ink-assistive`(1.69:1) 쪽이 나을지는 **사용자 판단**이 필요하다.
2. **직책·사진이 세션 API 에 없다** (위 §미비). BE 에 `/api/auth/me` 확장을 요청한다.
3. 시안의 **보라색 이미지 선택 테두리·상단 SCR 캡션**은 디자인 도구 UI 라 구현하지 않았다(브리프대로).
4. 앞선 미결 그대로: 완료 회의 정보 편집 진입점 · 진행 중 첨부 SPEC 어긋남 · `can_attach` 미노출 ·
   `ds/GutterList` 호출부 0곳 · 드로어 닫기 `×` 글리프 대비 1.69:1.
