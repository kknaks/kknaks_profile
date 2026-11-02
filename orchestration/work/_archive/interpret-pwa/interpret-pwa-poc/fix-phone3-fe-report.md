# 폰 피드백 3 — frontend 결과 보고 (D-31 언어 목록 뒤집힘)

## 상태: done (iPhone 실기기 확인은 pending — compose 재빌드 · 배포 뒤)

워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc`(폰 피드백 1 · 2 변경 위 · 커밋 없음). 범위 `front/**` 만.

## 원인 · 처리

- medikit 1.4.0 `ComboBox` 는 펼친 목록을 `PopoverContent` → `PopoverPrimitive.Portal` 로 **body 에 붙인다**. `ComboBoxProps` 에 portal 을 끄는 prop 이 없다(`dist/index.d.ts` · `index.js` 대조 — `classNames` · `size` 등뿐). 그래서 180° 돈 외국어 카드 밖에 그려져 안 뒤집혔다.
- → **카드 안에 그리는 자체 목록** `front/components/interpret/LangSelect.tsx`(새)로 바꿨다. 모양은 medikit 값 그대로:
  - 단추 = medikit `Button` outlined black · h44 · 최소 156 · `text-typo-heading-sm-500` · medikit `ChevronIcon` · 열리면 `border-primary`(ComboBox 와 같음)
  - 목록 = PopoverContent 클래스(`bg-ms-white rounded-[8px] shadow-pop-over`) · 항목 = CommandItem 값(`min-h-[50px] p-[15px] text-typo-heading-sm-400 hover:bg-ms-gray-100`) · 고른 것 `bg-primary-100 text-primary text-typo-heading-sm-500` + medikit `CheckIcon`
  - 카드(`relative`)째 돌아서 뒤집힘이면 **맞은편 사용자 기준 아래로** 펼쳐진다 · 바로 보기면 바로
  - 높이 = 카드 안 남은 높이(`offsetTop` — 회전과 무관한 레이아웃 값)까지 · 넘으면 목록 안 스크롤 → 화면 밖으로 안 잘림
  - 키보드: 단추 ↓ · Enter · Space 열기 / ↑ ↓ · Home · End · Enter 고르기 · Esc(단추로 포커스) · Tab 닫기 · `role=combobox` · `listbox` · `option` · `aria-activedescendant` / 바깥 누름 닫힘
- `InterpretScreen.tsx` — `ComboBox` → `LangSelect` · 카드에 `relative`. 언어 바꿈 흐름(stop → 새 start · 자막 지움)은 그대로.

## 검증

| 명령 | 결과 |
|---|---|
| `npx tsc --noEmit` | 통과 |
| `npm run lint` | 통과 |
| `npm run build` | 통과 |
| `npx vitest run` | 6 파일 · 28 통과 |
| 클래스 대조 | 191 · 없는 것 0 |

스크린샷 `fix-phone3-shots/`(390 × 844 · 운영 빌드):

| 파일 | 확인값 |
|---|---|
| `D31-flipped-open.png` | 목록이 외국어 카드 안 · 카드 transform `matrix(-1,0,0,-1)` · 단추 화면 y 320 ~ 364 · 목록 y 70 ~ 314(화면 위쪽 = 맞은편 기준 아래) · 화면 안 · 7개 중 5개 보이고 스크롤(244 / 350px) · 고른 「臺灣 · 繁體中文」 ✓ |
| `D31-upright-open.png` | 단추 y 82 ~ 126 · 목록 y 132 ~ 376(아래로) · 화면 안 · 바로 섬 |

키보드 · 닫힘: Esc 닫힘 ✓ · 바깥 누름 닫힘 ✓ · Home + Enter → `en` 고름(저장값 · 단추 「English」) ✓.

- 확인 방법: `:3800` · `:8800` 을 compose(`interpret-pwa-poc-front-1` · `-back-1`)가 쓰고 있어 **포트를 열지 않고** 운영 빌드(`.next`)를 헤드리스 Chrome request interception 으로 디스크에서 내줬다. back 호출(`/api/auth/config` · `/api/auth/me`)은 모양만 맞춘 가짜 응답 · WS 는 페이지 안 가짜(연결 중에 머묾). 
- ⚠ 첫 시도에서 운영 빌드의 서비스 워커가 interception 을 거치지 않고 실제 `:3800`(compose front)에 GET(문서 · 정적 파일)을 보냈다 — 읽기 요청뿐이고 compose 는 건드리지 않았다. 두 번째부터 `setBypassServiceWorker(true)` 로 막고 찍었다.

## 이슈 · 코디가 확인할 것

1. iPhone 실기기(Safari)에서 터치로 열기 · 고르기 · 바깥 탭 닫힘 — compose 재빌드 · 배포 뒤.
2. medikit `ComboBox` 를 이 화면에서 안 쓴다(DS 반영 요청 후보: `ComboBox` 에 portal 끄기 / `container` prop).
3. 목록이 카드 높이에 맞춰 줄어 7개 중 5개 정도 보이고 스크롤된다(390 × 844 기준).
