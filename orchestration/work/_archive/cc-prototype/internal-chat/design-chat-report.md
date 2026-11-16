# internal-chat 시안 결과 보고

## r2 — medikit 컴포넌트로 다시 그림 (사용자 반려 「디자인 시스템이 하나도 안 들어가 있다」)

### 상태: done

- 같은 파일 「Ceramique 의료진 앱 — 채팅.dc.html」을 덮어썼다(220,365 B). 장면 · 문구 · 데이터는 r1 과 같고, 바꾼 것은 그리는 방법뿐이다
- **장면 수 정정**: r1 리포트의 「25장(폰 21)」은 잘못 센 것이다. r1 과 r2 모두 **24장(폰 20 · 아이패드 4)** 이다. S10c 는 r1 「알림 끄기 시트」에서 r2 「알림 끈 방(Toggle 꺼짐)」으로 바꿨다(아래 4)
- ⚠ 원격 파일 목록에는 이름이 하이픈(`Ceramique 의료진 앱 - 채팅.dc.html`)으로 보인다. 그 이름의 파일은 하나뿐이고, 줄표(—) 경로로 읽으면 같은 내용이 나온다. 이름 표기는 코디가 확인해 주면 좋겠다
- ⚠ **기준 시안 정정**: x-import 122회는 「Ceramique 의료진 앱 **(구현 v3)**」이 아니라 확정 원본 「**Ceramique 의료진 앱.dc.html**」에 있다(원격본을 다시 받아 셌다). 구현 v3 는 0회이고 손으로 그린 HTML 이다. r1 이 구현 v3 의 손 CSS(.v3b 등)를 그대로 따라 한 것이 원인이었다. r2 는 원본처럼 x-import 로 그렸다

### 1. DS 컴포넌트 목록 (원천 = `_ds/medikit-aea7ac33…/README.md` · `_ds_manifest.json` · medikit 프로젝트 `components/ui/*/*.d.ts · *.prompt.md`)

medikit 1.4.0 · 42개: Accordion · ActionButton · AppTabs · AsyncBoundary · Badge · Banner · Button · Calendar · Card · Checkbox · Chip · ComboBox · Command · DatePicker · DeferredComponent · Dialog · Divider · Footer · Header · HoverCard · Input · Label · Loading · Logo · Menu · Modal · Notify · Pagination · Popover · Progress · RadioGroup · ResetButton · Spacing · Table · Tabs · Textarea · Toggle · Tooltip · (billing) AmountStepper · BillingBanner · CheckoutModal · PlanCard.

x-import 쓰는 법은 원본 「Ceramique 의료진 앱.dc.html」과 런타임 `support.js` 를 보고 맞췄다.
- 속성은 kebab 으로 쓰고 런타임이 camel 로 바꾼다(`class-name`→className, `left-icon`→leftIcon, `on-remove`→onRemove)
- x-import 의 `style` 은 위치값만 감싸는 div 로 간다
- ReactNode 를 받는 prop(Button `leftIcon` · Input `icon` · Banner `action` · Toggle `label`)은 원본처럼 script 의 `React.createElement` 값으로 넘겼다

### 2. 요소 → 컴포넌트

| 요소 | r1 (손 CSS) | r2 |
|---|---|---|
| 모든 버튼([새 대화] · [보내기] · [사진] · [다시 보내기] · [대화 시작/만들기/추가] · [취소] · [삭제] · [나가기] · [목록에서 숨기기] · [닫기] · ‹ 뒤로 · [+ 참여자 추가] · 시트 줄) | `.v3b` `<button>` | **Button** (solid/outlined/text · blue/gray/red · sm/md/lg · disabled · leftIcon) |
| 종 · ⓘ · ✕ 아이콘 버튼 | svg span | **Button** variant=icon + leftIcon |
| 역할 칩 · 안 읽음 수 · 탭/종 빨간 수 · 날짜 구분선 | `.v3tag` · span | **Badge** (primary/purple/neutral/danger · sm). 코디 · 상담사는 Badge `className` 으로 yellow-100 · cons(원본과 같은 프로젝트 색) |
| 메시지 입력 · 이름 검색 · 그룹 이름 | `.v3in` span | **Input** size=m (검색 = `icon`) · 그룹 이름 = **Label** + Input |
| 고른 사람 | span pill | **Chip** + onRemove |
| 사람 고르기 칸 | span ✓ | **Checkbox** |
| 사람 행 · 방 정보 칸 · 참여자 묶음 · 삭제 메뉴 · 대화상자 · 바텀 시트 | div | **Card** (padding · interactive · selected · indicator=none · shadow-pop-over-more) |
| 알림 끄기 | 「켜짐 ›」 행 + 시트 (확인할 것 6) | **Toggle** 켬/끔 — r1 의 「토글이 없어서」는 **틀렸다**. medikit 에 Toggle 이 있다 |
| 사진 올리는 중 | 손 진행 막대 | **Progress** tone=primary size=sm |
| 앱 앞 배너(S11 · S13d) | 원장 푸시 모양 카드 | **Banner** variant=primary + action [보기](원본 의료진 앱의 배너와 같은 꼴) |

### 3. DS 에 없음 → 유틸리티로 그림

모두 medikit 토큰 클래스(`bg-*` · `text-*` · `border-ms-gray-*` · `text-typo-*` · `bg-ms-overlay` · `shadow-pop-over-more`)로만 그렸고, 새 색은 없다.

| 요소 | 왜 DS 컴포넌트가 아닌가 |
|---|---|
| 폰 아래 탭바 5칸 | `Tabs` 는 위쪽 밑줄 탭이고 `AppTabs` 는 제품 전환 링크라 앱 하단 탭바가 아니다. 모양은 기준 시안(의료진 앱 「안 · 앱 메뉴」 · 모바일 v4)의 탭바 그대로 |
| 아이패드 왼쪽 레일 92px | `Menu` 는 웹 사이드바(274px · 메뉴 설정 · 경로)다. SPEC-004 §6.8 의 92px 글자 레일과 다르다. 모양은 기준 시안 그대로 |
| 공통 헤더(「Céramique」 + 종) · 대화 머리 · 아이패드 머리 | `Header` 는 웹 상단 바(지점 · 사용자 · 로그아웃)다. 안의 버튼 · 배지는 컴포넌트로 넣었다 |
| 방 목록 행 | 목록(list item) 컴포넌트가 없다. 안의 역할 칩 · 안 읽음 수는 Badge 다 |
| 말풍선(내 것 · 상대 · 삭제된 자리) | 메신저 말풍선 컴포넌트가 없다 |
| 시스템 한 줄(초대 · 나감) | 텍스트 한 줄이다 |
| 사진 썸네일 · 사진 크게 보기 화면 | 이미지 자리 컴포넌트가 없다 |
| 보내는 중 글자 · 보내기 실패 ! 아이콘 | 상태 글자다. `Loading` 은 크기 · 모양 prop 이 없는 로딩 그릇이라 말풍선 옆 한 줄에 맞지 않는다 |
| 바텀 시트 · 대화상자의 **위치와 뒤 가림막** | `Modal` · `Dialog` 는 isOpen 으로 페이지 전체를 덮는다. 캔버스 안 폰 틀 24개에 하나씩 넣을 수가 없다. 그래서 그릇은 Card 를 쓰고, 위치와 가림막(`bg-ms-overlay`)만 유틸리티로 했다 |
| 잠금 화면 푸시(S12) | iOS 시스템 화면이다(앱 화면이 아님). 기준 시안 원장 호출 푸시와 같은 모양 |
| 길게 누른 말풍선 띄우기 | 말풍선과 같은 이유 |
| 장면 틀(폰 · 아이패드 테두리 · 장면 번호 · 설명) | 캔버스 장치다. 기준 시안과 같다 |

### 4. r1 에서 DS 부재를 이유로 든 곳 다시 확인

| r1 | 번들에 있나 | r2 |
|---|---|---|
| 확인할 것 6 「토글이 없어서 시트로」 | **있다**(Toggle) | Toggle 로 바꿨다. S10c = 알림 끈 상태 |
| 확인할 것 5 「아바타 컴포넌트가 없어서」 | 없다(42개에 Avatar 없음) | 그대로(이름 + 역할 Badge) |
| 확인할 것 7 아이패드 방 정보 = 오른쪽 시트 | Modal · Dialog 는 페이지 전체를 덮음(위 표) | Card 그릇 + 유틸리티 위치 그대로 |

### 화면 대조

S1 ~ S13 대조표는 r1(아래)과 같다. 13항목 모두 있고, 장면은 24장이다.

### 검증 (수치)

**x-import 개수 · 컴포넌트별** — 원격본을 받아 셌다

| 컴포넌트 | 채팅 r2 | 원본 「Ceramique 의료진 앱」 | 「의료진 앱 (구현 v3)」 |
|---|---|---|---|
| Badge | 128 | 37 | 0 |
| Button | 86 | 58 | 0 |
| Card | 43 | 0 | 0 |
| Checkbox | 25 | 10 | 0 |
| Input | 17 | 0 | 0 |
| Chip | 7 | 5 | 0 |
| Toggle | 5 | 0 | 0 |
| Banner | 2 | 5 | 0 |
| Label | 2 | 0 | 0 |
| Progress | 1 | 4 | 0 |
| Tabs | 0 | 2 | 0 |
| Textarea | 0 | 1 | 0 |
| **합** | **316** | **122** | **0** |

- **손 CSS 버튼 · 입력 grep**: `.v3b` · `.v3in` · `.v3tag` · `.cc-btn` = **0**. 손으로 쓴 `<button>` = 0 · `<input>` = 0
- **`<style>` 에 남은 규칙**은 전부 원본 「Ceramique 의료진 앱 (구현 v3)」 helmet 과 같은 줄이다:
  - `html,body{margin:0}`: 캔버스 여백
  - `a` · `a:hover` 색: 링크 색(원본과 같음)
  - `.bg-cons` · `.bg-cons-100` · `.text-cons` · `.border-cons`: 상담사 색. medikit 에 success(초록)가 없어서 원본 의료진 앱이 이 프로젝트에 둔 4줄이다(medikit-patches [Token-1]). 상담사 역할 Badge 에 쓴다
- **실제 런타임으로 렌더 확인**: 프로젝트 `support.js` 에 같은 medikit 번들 전체(1,031,124 B)를 붙였다. DesignSync 로 받은 원격 번들 262,142 B 와 앞부분이 같은 로컬 사본이다. 이것을 로컬 헤드리스 크롬으로 띄웠다. 위 컴포넌트가 실제 medikit 모양으로 그려진 것을 장면마다 눈으로 봤다(시트 줄 아이콘 버그 1건은 찾아서 고쳤다). Claude Design 화면 안에서는 열어 보지 않았다
- **원격본 = 로컬 사본**: 바이트가 같다(sha256 `7148eb3fc0e0…` · 220,365 B)
- **기존 파일 무수정**: 두 번의 DesignSync 플랜 모두 쓰기 경로가 이 파일 하나뿐이고 지운 것은 0이다
- 실명 · 키 = 0 (비밀값 패턴 grep 0 · 가짜 이름 10개)

### 남은 확인할 것 (r1 목록에서 바뀐 것)

- 6번(토글)은 닫았다
- 5번(아바타 없음), 1 ~ 4번, 7 ~ 10번은 r1 그대로다
- 새로 1건: 안 읽음 수 Badge 는 medikit 모양(연한 바탕 + 진한 글자)이다. r1 의 꽉 찬 원 배지와 다르다. 꽉 찬 원이 필요하면 DS 밖 모양이다

---

## r1

## 상태: done (r2 로 대체)

## Claude Design 프로젝트 — id · 파일 이름 · 화면(장면) 목록

- 프로젝트 `dda9a931-097f-4780-9301-972d5ac1fc23`
- **새 파일** 「Ceramique 의료진 앱 — 채팅.dc.html」 (캔버스 · 228,137 B). 기존 파일은 읽기만 했다. DesignSync 플랜의 쓰기 경로는 이 파일 하나뿐이고, 지운 파일은 없다
- 로컬 사본: `orchestration/work/internal-chat/design/Ceramique 의료진 앱 — 채팅.dc.html` — 올린 뒤 원본을 다시 받아 비교했고 **바이트가 같다**(sha256 `a57a3a613521…`)
- 장면 25장(폰 21 · 아이패드 4), 7개 절:

| 절 | 장면 |
|---|---|
| 방 목록 · 새 대화 | S1 방 목록 · S2 방 목록 · 비어 있음 · S3a 새 대화 · 한 명 = 1:1 · S3b 새 대화 · 여러 명 = 그룹 · S3c 새 대화 · 검색 |
| 대화 | S4 대화 · 1:1 · S5 대화 · 그룹 · S6 보내는 중 · 보내기 실패 |
| 사진 | S7a 사진 고르기 · S7b 사진 올리는 중 · S8 사진 크게 보기 |
| 삭제 | S9a 내 메시지 길게 누르기 · S9b 삭제 확인 |
| 방 정보 | S10a 방 정보 · 그룹 · S10b 방 정보 · 1:1 · S10c 알림 끄기 · S10d 참여자 추가 · S10e 나가기 확인 |
| 알림 | S11 앱이 앞에 있을 때 — 다른 방 새 메시지 · S12 잠금 화면 푸시 |
| 아이패드 | S13a 두 칸 · S13b 방 고르기 전 · S13c 방 정보 · S13d 다른 방 배너 |

모양 기준: 「의료진 앱 (구현 v3)」의 「안 · 앱 메뉴」 절(탭바 · 레일 · 설정 목록 행), 「간호사 모바일 (구현 v3)」(버튼 `.v3b` · 바텀 시트 · 체크박스 · 입력칸 `.v3in` · 원장 호출 푸시 카드 · 잠금 화면), 「모바일 v4」(공통 헤더 「Céramique」 + 종 배지 · 상단 바 `‹ 뒤로 / 제목 / 오른쪽`). ⚠ 구현 v3 파일은 **10-22 시점(탭 없음)이라** 공통 헤더 · 탭바 · 종 배지는 같은 프로젝트의 「모바일 v4」와 의료진 앱 「안 · 앱 메뉴」 절에서 가져왔다. 기준 시안 3개의 원격본은 아카이브 사본(`_archive/.../design-sync/`)과 내용이 달라서 원격본을 읽었다.

## 화면 대조 — 브리프 화면 목록 항목별 있음/없음

| # | 브리프 | 있음 · 장면 | 보이는 것 |
|---|---|---|---|
| S1 | 방 목록 | 있음 · S1 | 1:1 4 · 그룹 3 섞임 · 이름 없는 그룹 「김도현, 박지윤, 이서아」(참여자 나열) · 미리보기 「사진」 · 「이서아: 삭제된 메시지예요」 · 시각 · 안 읽음 배지 · 알림 끈 방 = 종 빗금 + 회색 배지 · [새 대화] · 채팅 탭 배지 3 |
| S2 | 방 목록 비어 있음 | 있음 · S2 | 「아직 대화가 없어요」 안내 + [새 대화] |
| S3 | 새 대화 — 상대 고르기 | 있음 · S3a · S3b · S3c | 이름 + 역할 칩 · 검색 · 1명 = [대화 시작](1:1) · 여러 명 = [만들기] + 그룹 이름(선택) · 「나 포함 최대 20명」 |
| S4 | 대화 — 1:1 | 있음 · S4 | 내 것 / 상대 말풍선 · 날짜 구분선 · 시각 · 텍스트 · 사진 1장 · 「삭제된 메시지예요」 · 입력칸 + [사진] + [보내기] |
| S5 | 대화 — 그룹 | 있음 · S5 | 보낸 사람 이름 · 「정하늘 님이 이서아 님을 초대했어요」 · 「최민재 님이 나갔어요」 · 「한유리 (비활성)」 |
| S6 | 보내는 중 · 실패 | 있음 · S6 | 흐린 말풍선 + 「보내는 중…」 · 빨간 ! + 「보내지 못했어요」 [다시 보내기] |
| S7 | 사진 고르기 | 있음 · S7a · S7b | 카메라로 찍기 / 앨범에서 고르기 시트 · 「올리는 중 62%」 |
| S8 | 사진 크게 보기 | 있음 · S8 | 전체 화면 · 보낸 사람 · 시각 · [닫기]. 저장 · 공유 버튼 없음 |
| S9 | 내 메시지 길게 누르기 | 있음 · S9a · S9b | [삭제] 하나(설명에 「남의 메시지엔 메뉴 없음」) · 삭제 확인 대화상자 |
| S10 | 방 정보 | 있음 · S10a ~ S10e | 그룹 이름 · 알림(방마다) · 참여자 · [참여자 추가](그룹만) · [나가기](그룹) / [목록에서 숨기기](1:1) · 알림 끄기 시트 · 참여자 추가 목록 · 나가기 확인 |
| S11 | 앱 앞 다른 방 배너 | 있음 · S11 · S13d | 원장 호출 푸시와 같은 카드 · 「보고 있는 방 · 알림 끈 방이면 안 뜸」 설명 |
| S12 | 잠금 화면 푸시 | 있음 · S12 | 보낸 사람 + 본문 앞부분 · 「사진」 · 같은 방 묶음(겹친 카드) |
| S13 | 아이패드 | 있음 · S13a ~ S13d | 왼쪽 레일(채팅 = 5번째 · 배지) + 방 목록 360 + 대화 두 칸 |

검증 수치: 브리프 13항목 중 13 있음 · 장면 25 · 쓴 클래스 46종이 모두 medikit 번들(`_ds_bundle.css`) 또는 구현 v3 `<style>`(.v3b · .v3tag · .v3in)에 있다 · 새 색 0(`.bg-cons` 4줄은 구현 v3 의료진 앱과 같은 줄) · 실명 · 키 · 계정값 0(가짜 이름 10개, 비밀값 패턴 grep 0) · 태그 짝 오류 0 · 기존 파일 수정 0.

## 결정과 다르게 그린 곳 · 제안 · 코디가 확인할 것

### DEC 와 다르게 그린 곳

없다. DEC 에 값이 없어서 기본값으로 그린 곳은 아래 「확인할 것」에 모았다.

### 코디가 확인할 것 (DEC 에 없는 모양 값 — 기본값으로 그림)

1. **대화 화면에서도 탭바를 남겼다.** 「모바일 v4」 P2(룸 상세)가 탭바를 남긴 것을 따랐다. 메신저들처럼 대화 안에서 탭바를 숨길지는 사용자가 정할 일이다
2. **채팅 탭 배지에 알림 끈 방도 센다**(S1 = 3, 그중 하나가 알림 끈 방). D-20 은 「안 읽은 방 합」만 말한다. 끈 방을 뺄지 정해야 한다
3. **방 목록 안 읽음 배지 색**: 보통 방 = primary, 알림 끈 방 = 회색. 탭 · 종 배지는 기준 시안처럼 빨강이다
4. **푸시 · 배너 제목**: 1:1 = 「보낸 사람」, 그룹 = 「보낸 사람 · 방 이름」. D-27 은 「보낸 사람 + 본문」만 말하는데, 그룹에서는 방 이름이 없으면 어느 방인지 몰라서 붙였다
5. **아바타를 그리지 않았다.** 기준 시안에 사람 아바타 컴포넌트가 없어서 이름 + 역할 칩으로만 구분했다
6. **알림 끄기 = 시트 두 칸(알림 받기 / 알림 끄기)**. 기준 시안에 토글 스위치가 없어서 설정 화면의 「켜짐 ›」 행 + 바텀 시트 모양을 썼다
7. **아이패드 방 정보 = 오른쪽 시트**(SPEC-004 §6.13 알림 목록 태블릿 자리와 같게). 아이패드의 새 대화 · 사진 시트 · 삭제 확인은 따로 그리지 않았고, 「폰과 같은 내용 · 가운데」라고 설명에 적었다
8. **사진 크게 보기에서 확대 · 넘기기 제스처**는 그리지 않았다(정지 화면)
9. 1:1 방 정보에 「1:1 에는 참여자를 더할 수 없어요. 여럿이 이야기하려면 [새 대화] 에서 그룹을 만들어요」 안내 한 줄을 넣었다(D-02 · D-10 을 풀어 쓴 문구)
10. 공통 헤더는 SPEC-004 §6.8(가운데 「Céramique」 + 종)이고, 그 아래 「채팅 · [새 대화]」 줄을 더했다

### 제안 (DEC 밖 — 그리지 않음)

- 방 목록 위 검색(방 · 메시지)
- 방 목록 길게 누르기로 바로 알림 끄기 · 숨기기
- 사진 여러 장 한 번에 보내기(지금은 D-15 로 1장)
- 그룹 이름 바꾸기(D-09 는 만들 때만 정한다)

## git status --short (작업 후)

```
 M orchestration/config/projects/cc-prototype.json
 M para/projects/summer-star/cc-prototype/00-baseline/README.md
 M para/projects/summer-star/cc-prototype/10-decision/README.md
 M para/projects/summer-star/cc-prototype/log.md
?? orchestration/roles/cc-prototype/designer/
?? orchestration/work/internal-chat/
?? para/projects/summer-star/cc-prototype/00-baseline/baseline-010-internal-chat.md
?? para/projects/summer-star/cc-prototype/10-decision/decision-009-internal-chat.md
```

`M` 4줄 · `para/` `??` 2줄 · `roles/` 는 작업 전부터 있던 코디 변경이다(시작할 때 gitStatus 와 같다). 이 워커가 만든 것은 `orchestration/work/internal-chat/` 아래 `design/`(시안 사본 + README) 와 이 리포트뿐이다.
