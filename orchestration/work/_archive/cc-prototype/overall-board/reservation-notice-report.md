# 예약 현황 공지 [수정하기] — KOS 공지 쓰기 (데모 HAR + 웹앱 JS + 데모 실호출 · 모양만)

- 조사일: 2026-10-27 (KST) · 조사자: cc-prototype researcher (task_c50f6d829c20)
- 원천
  - HAR `reference/2026-10-23-cc-overall-board/har/공지사항.har`(8항목 · 06:33:06Z ~ 06:33:16Z · **데모 테넌트** — 코디 확인)
  - KOS 웹앱 JS(같은 폴더 다른 HAR 안의 응답 본문 — 공식 문서가 없어 이것이 근거)
    - **[JS-R]** `예약그룹.har` #119 `tenant-meta/452.…tenant-meta-client_v0.0.42.js` — 공지 저장소 · 메시지 모양 · 유스케이스
    - **[JS-U]** `수납필요 확인.har` #23 `tenant-meta/588.…tenant-meta-client_v0.0.42.js` — 공지 화면(상태 · 버튼 · 모달)
    - 위치는 JS 본문 글자 위치(char offset)로 적는다. 압축 코드라 줄 번호가 없다
  - ccc 코드(읽기만): `procedure/back/app/kos/reservation_sync.py` · `app/repository/repo.py` · `app/schemas/reservations.py` · `front/components/reservations/ResvAside.tsx`
- 데모 실호출: 2026-10-27 · 날짜 **2026-11-10 (KST)** 하나 · 쓰기 3번(만들기 · 덮어쓰기 · 지우기) + 읽기 6번. 운영 키 0 · 실제 지점 호출 0
- **이 레포는 public** — 테넌트 id · 계정 · 토큰 · 공지 본문 실값 · 사람 이름 없음. 모양 · 필드 이름 · 타입 · 글자 수만
- 표기: **확인** = HAR · JS · 실호출로 본 것 · **추정** = 해석 · **문서에 없음** = 근거 없음

---

## 0. 결론

- **KOS 공지 = 날짜당 하나**(KOS 웹 기준 · 확인 [JS-U 12678] `dateToNoticeKey = format(date,"yyyy-MM-dd")` · 날짜 키 하나에 공지 하나). 서버가 같은 날 둘을 막는지는 **문서에 없음**(Q-138)
- 쓰기 명령은 **셋**이다 — HAR 에는 `change-content` 만 있었다(고치기 2번). 만들기 · 지우기는 JS 에서 찾고 데모로 확인
  | 명령 | 경로(내부 · `/tenants/{tenantId}/…`) | 요청 | 응답 |
  |---|---|---|---|
  | 고치기 | `meta/notice/v1/commands/change-content` | `{id, content}` | `{}` |
  | 새로 쓰기 | `meta/notice/v1/commands/create-notice` | `{content, releaseDateTimeUtc}` | `{data:{id, content, releaseDateTimeUtc, deleted}}` |
  | 지우기 | `meta/notice/v1/commands/delete-notice` | `{id}` | `{}` — **소프트 삭제**(`deleted:true` 로 남는다) |
- **날짜 바꾸기 명령은 없다**(확인 [JS-R 12040] 저장소 메서드 4개 = `getNotices` · `changeNoticeContent` · `deleteNotice` · `createNotice`)
- **일반 글자**(리치 텍스트 아님 · 확인) — 입력 `Input.TextArea` · `maxLength 2000` · 표시 `white-space:pre-line` [JS-U 8711 · 10000]
- **ccc 시스템 계정은 쓰기 권한이 있다**(데모 확인 — 셋 다 200 · 바로 다음 읽기에 반영)
- ccc 읽기와 쓰기 대상은 **같은 것**이다 — ccc 가 읽는 `get-notices` 의 `id` 를 `kos_id` 로 이미 저장한다. 단 ccc API 의 `Notice.id` 는 **ccc 내부 정수 id** 라 back 이 `kos_id` 로 바꿔 불러야 한다(§3)
- 정할 것 **7개**(Q-138 ~ Q-144)

---

## 1. HAR 해부 (확인)

| # | 요청 | 상태 | 본문 모양 | 응답 모양 |
|---|---|---|---|---|
| 0 | `role/v2/queries/get-roles` | 200 | 없음 | `{data:[{id, name, featureList?[], roleTags:int[], isDefault?:bool}] ×15}` |
| 1 | `meta/notice/v1/queries/get-notices` | 200 | `{startDateTimeUtc, endDateTimeUtc, deleted:false}` — 하루(KST 00:00 의 UTC ~ 다음날 같은 시각) | `{data:[{id:str(24), content:str, releaseDateTimeUtc:str, deleted:bool}] ×1}` |
| 3 | `meta/notice/v1/commands/change-content` | 200 | `{id, content}` — 짧은 시험 글자(2자) | `{}` |
| 5 | `get-notices` | 200 | #1 과 같음 | 같은 `id` · `content` 가 #3 값으로 바뀜 |
| 7 | `change-content` | 200 | `{id, content}` — #3 글자 + 줄바꿈 + 원래 내용 | `{}` |
| 2 · 6 | datadog RUM | 202 | — | — |
| 4 | `change-content` 의 OPTIONS(CORS) | 200 | — | — |

- `releaseDateTimeUtc` = **그 날짜 KST 00:00 의 UTC**(`…T15:00:00Z` · 전날 날짜) — 공지의 「날짜」가 이것이다. 응답은 밀리초 없는 `Z` 꼴
- 공지 여러 개인가 — 이 HAR 은 하루 범위에 1건. 범위를 한 달로 주면 여러 건이 온다(KOS 웹은 달을 고르면 `startOfMonth ~ endOfMonth` 로 부른다 [JS-U 3317 `selectDate`])
- **새 공지 쓰기는 HAR 에 없다.** `change-content` 2번이 전부 고치기다(같은 `id`)
- HAR 요청 헤더에 `authorization` · `cookie` 가 없다 — 내보내기 때 빠진 것으로 보인다(추정). ccc 는 `Bearer`(시스템 계정 sign-in)로 불렀고 됐다(§4)
- ⚠ **HAR 녹화가 데모 공지를 바꿔 둔 채 끝났다**: #7 뒤 2026-10-27 데모 공지 = 원래 내용 앞에 시험 글자 한 줄이 붙은 상태(확인 — #7 본문). 이번 조사는 그 날짜를 건드리지 않았다(되돌릴지는 사용자)

### 1.1 메시지 모양 (확인 [JS-R])

| 메시지 | 필드 | 위치 |
|---|---|---|
| Notice | `id:string` · `content:string` · `releaseDateTimeUtc:string` · `deleted:bool` | 5158 |
| GetNotices 요청 | `startDateTimeUtc:string` · `endDateTimeUtc:string` · `deleted?:bool`(선택) | 6678 |
| CreateNotice 요청 | `content:string` · `releaseDateTimeUtc:string` | 8861 |
| ChangeContent 요청 | `id:string` · `content:string` | 9911 |
| DeleteNotice 요청 | `id:string` | 10753 |
| CreateNotice 응답 | `{data: Notice}` — `data` 가 없으면 웹이 "Invalid response" 로 던진다 | 12040 · 10753 뒤 |

### 1.2 KOS 웹 동작 (확인 [JS-R] 유스케이스 · [JS-U] 화면)

- **[수정하기] 누름 → 그 날짜 공지를 먼저 다시 읽는다**(`fetchNoticeByDate` = 그 날 00:00 ~ +1일 · `deleted:false` · **결과의 첫 번째만** 쓴다 `const[t]=e` [JS-U 4989 · 5164]) → 모달
- **저장** = 그 날 공지가 있으면 `change-content({id, content})` · 없으면 `create-notice({content, date})`(확인 [JS-U 10109 `ne`]). 하나의 [저장] 버튼이 둘을 가른다
- **[삭제]** = 모달에 공지가 있을 때만 보인다 · 확인창 뒤 `delete-notice({id})` [JS-U 8711 `te`]
- **[수정하기] 는 지난 날짜에는 안 보인다** — `isAfter(startOfDay(오늘), startOfDay(고른 날))` 이면 버튼을 그리지 않는다 [JS-U 10109]. 오늘 · 앞날만
- 검사(클라이언트)
  | 명령 | 검사 | 실패 코드 | 서버 오류 매핑(`errorProperties[0]`) |
  |---|---|---|---|
  | create | `content.trim()` 비면 거절 · 고른 날이 오늘보다 앞이면 거절 · **보낼 때 `trim()` 한 값** · `releaseDateTimeUtc = date.toISOString()`(브라우저 시간대 00:00) | `NO_EMPTY_CONTENT` · `NO_PAST_DATE` | `content Required` → 빈 내용 · `releaseDateTimeUtc NotAvailable` → 지난 날짜 [JS-R 15950] |
  | change | `trim()` 비면 거절 · `trim()` 길이 > 2000 거절 · **보낼 때는 trim 안 한 원래 값** | `NO_EMPTY_CONTENT` · `TOO_LONG_CONTENT` | `content Required` · `content TooLong` [JS-R 14085] |
  | delete | 없음 | — | 전부 unknown [JS-R 13735] |
  | get | 시작 > 끝 거절 | `INVALID_TIME_RANGE` | `startDateTimeUtc InvalidTimeRange` [JS-R 12794] |
- **빈 내용으로 고치기는 KOS 가 막는다**(클라이언트 + 서버 `content Required` 매핑이 있음). 그래서 「비우기」 = **지우기**(`delete-notice`)다
- 표시 = 내용이 없거나 `deleted` 면 빈 상태 [JS-U `G`]

---

## 2. 데모 실호출 (2026-10-27 · 날짜 2026-11-10 KST)

- 시작 전 assert: `.env` 의 `KOS_TENANT_ID` == HAR(데모) 요청 경로 테넌트 → **OK**(값 출력 없음). `.env` 에 `KOS_API_tenent`(운영 명동점) 키는 없다
- 인증: 내부 `common/v1/user/commands/sign-in`(시스템 계정) → `Authorization: Bearer <token>` — workflow-v2 「인증 · 계정」과 같음. sign-in 200
- 그 날 처음엔 공지가 없었다 → HAR 에 없던 **새로 쓰기 경로(`create-notice`)** 로 갔다 · 되돌리기 = **지우기(`delete-notice`)**

| 단계 | 호출 | 상태 | 지연 | 응답 모양 | 반영 |
|---|---|---|---|---|---|
| ① 읽기 | `get-notices {11-09T15:00Z ~ 11-10T15:00Z, deleted:false}` | 200 | 28ms | `{data:[]}` | 0건 |
| ② 쓰기 | `create-notice {content:"[ccc 시험] 공지 쓰기 확인", releaseDateTimeUtc:"2026-11-09T15:00:00.000Z"}` | 200 | 39ms | `{data:{id:str(24), content:str(17), releaseDateTimeUtc:str(20), deleted:false}}` | 새 `id` 받음 |
| ③ 다시 읽기 | ① 과 같음 | 200 | 26ms | `{data:[Notice] ×1}` · `releaseDateTimeUtc = "2026-11-09T15:00:00Z"` | **바로 반영**(내용 같음 · `id` 같음) |
| ④ 덮어쓰기 | `change-content {id, content:"…— 덮어쓰기"}` | 200 | 28ms | `{}` | — |
| ④b 다시 읽기 | ① 과 같음 | 200 | 26ms | `{data:[Notice] ×1}` · content str(24) | **바로 반영**(`id` 그대로) |
| ⑤ 되돌리기 | `delete-notice {id}` | 200 | 28ms | `{}` | — |
| ⑤b 읽기 `deleted:false` | | 200 | 23ms | `{data:[]}` | 안 보임 |
| ⑤c 읽기 `deleted:true` | | 200 | 25ms | `{data:[Notice{deleted:true}] ×1}` | **행이 남아 있다**(소프트 삭제 · 마지막 내용 그대로) |
| ⑤d 읽기 `deleted` 뺌 | | 200 | 25ms | `{data:[Notice{deleted:true}] ×1}` | 지운 것도 같이 온다 |

- 반영 지연: 세 쓰기 모두 **바로 다음 읽기(수십 ms 뒤)에 보였다**(SPEC-005 §4.3 「쓰기 뒤 0 ~ 3초」 안)
- 지금 그 날짜 상태: `deleted:false` 로는 공지 없음(원래와 같음). 다만 KOS 안에 **`deleted:true` 행 1개**가 남았다(지우기 경로의 결과 — 완전히 없애는 명령은 없다)
- 하지 않은 것(허가 밖): 같은 날 둘째 `create-notice` · 지운 날에 다시 `create-notice` · 지난 날짜 쓰기 · 2000자 넘김 · 빈 내용 — 그래서 아래 「문서에 없음」이 남는다

---

## 3. ccc 지금 읽는 값 ↔ 쓰기 대상 (확인 — 코드 읽기)

| | 지금 ccc | 쓰기에 필요한 것 | 같은가 |
|---|---|---|---|
| 읽는 API | 내부 `get-notices {startDateTimeUtc, endDateTimeUtc, deleted:false}` = 그 날짜 KST 하루(`reservation_sync.py` `PATH_NOTICES` · `_notices`) | 쓰기도 내부(같은 Bearer) | 같음 |
| 공지 키 | KOS `id` → `notice.kos_id`(`_notices` · `repo.replace_notices`) | `change-content` · `delete-notice` 의 `id` | 같음 |
| 날짜 | `releaseDateTimeUtc` → `released_at` · 하루 범위 안만 | `create-notice` 의 `releaseDateTimeUtc` = 그 날짜 KST 00:00 의 UTC | 같음(같은 날짜 기준) |
| 지운 공지 | `deleted` 면 거르고, 범위 안 사본에 없으면 `deleted=1` | `delete-notice` 뒤 `deleted:false` 조회에서 빠짐 → 다음 조회가 사본에서 지움 | 맞물림 |
| front 에 주는 id | `schemas.Notice.id:int` = **ccc 행 id**(`service/reservations.py` 346 `"id": n.id`) | KOS `id`(str 24) | **다름** — back 이 행 id → `kos_id` 로 바꿔야 함(또는 응답에 KOS id 를 더함) |
| 여러 개 | front `ResvAside.tsx` 가 `board.notices` 를 **목록으로 전부** 그린다 | KOS 웹은 날짜당 **첫 번째 하나**만 | 다름 — Q-138 |

---

## 4. 권한 · `get-roles`

- `get-roles` 는 **공지 화면을 열 때 같이 불린 것**이다(#0 이 #1 보다 0.1초 앞 · 같은 화면 로드). 공지 코드([JS-R] 공지 부분 · [JS-U] 공지 화면)에는 **역할 · 권한 검사가 없다**(확인 — `role`/`feature` 참조 0). 그래서 「공지 쓰기 권한 확인용」이라는 근거는 **없다**. 무엇이 부르는지는 이 두 청크 밖이라 **문서에 없음**(같은 화면의 다른 부분으로 추정)
- 서버 쪽 권한: **ccc 시스템 계정은 만들기 · 고치기 · 지우기 셋 다 됐다**(§2 · 데모). 다른 역할이 막히는지 · 오류 모양(`AccessBlocked` 등)은 **문서에 없음**(다른 화면 코드에 `className === "AccessBlocked"` 매핑이 있다 [JS-R `fetchCodes` 부분] — 공지 유스케이스에는 없다)

---

## 5. 시안과 KOS 웹 차이 (참고만 — 배치는 구현본이 정본)

- 시안(`M:170-176` · 상태 `M:1892`): 공지 칸 = `Textarea` 하나 · 오른쪽 위 버튼 글자가 **「수정하기」 ↔ 「저장」** 으로 바뀌고 읽기 전용이 풀린다(제자리 편집) · 삭제 버튼 없음 · 공지 하나
- KOS 웹: [수정하기] → 다시 읽기 → **모달**(textarea · 글자 수 · [삭제] · [저장]) · 지난 날짜엔 버튼 없음

---

## 6. 정할 것 (결정 안 함)

| Q | 무엇 | 근거 · 갈래 |
|---|---|---|
| Q-138 | **같은 날 공지가 둘 이상**이면 ccc 는 무엇을 보이고 무엇을 고치나 | KOS 웹 = 날짜 키 하나 · 다시 읽기 결과 **첫 번째만**(§1.2). ccc front 는 지금 목록 전부(§3). 서버가 같은 날 둘째 `create-notice` 를 막는지는 시험 안 함(허가 밖 · 문서에 없음). 갈래: KOS 처럼 첫 번째 하나만 / 지금처럼 전부 보이고 첫 번째만 [수정하기] / 확인 시험 1회 더(허가 필요) |
| Q-139 | **저장 직전 다시 읽기**를 할까(동시 수정) | KOS 웹은 [수정하기] 누를 때 한 번 다시 읽고, 저장 때는 안 읽는다 · `change-content` 에 버전 · 이전 값 필드가 없다(§1.1) → **나중에 저장한 쪽이 덮는다**. 다른 사람이 그 사이 **새로 만들었으면** ccc 가 둘째 `create-notice` 를 부를 수 있다(Q-138 과 묶임) |
| Q-140 | **내용을 전부 지우고 저장**하면 | KOS = 빈 내용 고치기 거절(`content Required`) · 비우기 = `delete-notice`(소프트 삭제). 갈래: 빈 저장 = 지우기로 바꿈 / 막기(「내용을 입력하세요」) / [삭제] 버튼 따로(시안엔 없음) |
| Q-141 | **지난 날짜**에 [수정하기]를 보일까 | KOS 웹 = 오늘 · 앞날만 · 만들기는 서버도 지난 날짜 거절 매핑(`releaseDateTimeUtc NotAvailable`). 지난 날짜 **고치기**를 서버가 막는지는 문서에 없음 |
| Q-142 | 글자 제한 · 앞뒤 공백 | KOS 웹 = 2000자(`trim` 길이) · 만들기는 `trim` 해서 보내고 고치기는 원래 값. ccc 도 2000 을 쓸지 · trim 규칙을 KOS 와 같이 할지 |
| Q-143 | ccc API 공지 id | 지금 `Notice.id` = ccc 행 id(int). 쓰기 경로가 행 id 를 받고 back 이 `kos_id` 로 바꿀지 / 응답에 KOS id 를 실을지. 저장 뒤 캐시 비움 · 다시 읽기는 SPEC-005 §4.3 · §4.4 그대로 쓸지 |
| Q-144 | 데모에 남은 흔적 | ① 2026-11-10 `deleted:true` 행 1개(이번 시험 · 지우기 경로라 남음 · 화면엔 안 보임) ② 2026-10-27 데모 공지 앞에 HAR 녹화의 시험 글자 한 줄(사용자 녹화 · 이번 조사가 건드리지 않음) — 둘 다 둘지 · ② 를 사용자가 KOS 웹에서 고칠지 |

---

## 7. 검증

- API 마다 근거: `get-notices` = HAR #1 · #5 + [JS-R 6678 · 12794] / `change-content` = HAR #3 · #7 + [JS-R 9911 · 14085] / `create-notice` = [JS-R 8861 · 15950] + [JS-U 10109] / `delete-notice` = [JS-R 10753 · 13735] + [JS-U 8711] / `get-roles` = HAR #0
- 데모 호출: 9번 전부 200(sign-in 1 · 읽기 6 · 쓰기 3 — create · change · delete) · 반영 = ③ · ④b 바로 · ⑤b 사라짐 · ⑤c 소프트 삭제 행 확인
- 리포트에 테넌트 id · 계정 · 토큰 · 공지 실내용 · 사람 이름 없음(아래 grep)
